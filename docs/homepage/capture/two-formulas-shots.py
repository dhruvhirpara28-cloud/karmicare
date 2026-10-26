#!/usr/bin/env python3
"""Before/after shots and measurements of the two-formulas tubes vs the feature headings.

Runs on one Orca browser page (isolated profile) against the live storefront. "before" is
the live page; "after" injects two-formulas-mobile-after.css (the branch rule); "square"
emulates iOS Safari on the live page, where the box stays as high as it is wide. Per width,
mode and language it writes a viewport PNG of the section and one JSON row of measurements.

Usage: python3 -I docs/homepage/capture/two-formulas-shots.py <page-id> <out-dir> [tag ...]
"""
import base64
import json
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
PAGE, OUT = sys.argv[1], Path(sys.argv[2])
TAGS = sys.argv[3:] or ['before', 'after']
LANGS = {'en': 'https://www.karmicare.com/', 'nl': 'https://www.karmicare.com/nl',
         'fr': 'https://www.karmicare.com/fr'}
WIDTHS = [360, 390, 414, 450, 700, 768, 989, 990, 1080]
HEIGHT = 1000
AFTER_CSS = (HERE / 'two-formulas-mobile-after.css').read_text()
# Same in before and after: Shopify's cookie banner covers the lower viewport on a fresh profile
QA_CSS = '#shopify-pc__banner{display:none!important}'
# Opaque tube rows in kc-two-formulas-duo.png (1600 x 1956), measured from its alpha channel
TUBE_TOP, TUBE_BASE, FILE_H = 145, 1763, 1956


def orca(*args):
    proc = subprocess.run(['orca', *args, '--page', PAGE, '--json'],
                          capture_output=True, text=True, timeout=90)
    data = json.loads(proc.stdout)
    if not data.get('ok'):
        raise SystemExit(json.dumps(data.get('error')))
    return data['result']


def evaluate(js, expect_host='www.karmicare.com'):
    # orca eval sometimes runs in an about:blank context: check the host before running js
    guarded = ('JSON.stringify((()=>{if(location.host!==' + json.dumps(expect_host) + ')return [location.host];'
               'try{return [location.host,' + js + ']}catch(e){return [location.host,{evalError:String(e)}]}})())')
    for _ in range(20):
        found = json.loads(orca('eval', '--expression', guarded)['result'])
        if found[0] == expect_host:
            result = found[1] if len(found) > 1 else None
            if isinstance(result, dict) and 'evalError' in result:
                raise SystemExit(result['evalError'])
            return result
        time.sleep(0.5)
    raise SystemExit('eval kept landing outside the storefront')


def set_css(css):
    evaluate('(()=>{let s=document.getElementById("kc-tf-qa");if(!s){s=document.createElement("style");'
             's.id="kc-tf-qa";document.head.append(s)}s.textContent=' + json.dumps(css) + ';return 1})()')


MEASURE = '''(()=>{
  const q=s=>document.querySelector(s), r=e=>e?e.getBoundingClientRect():null;
  const stage=q('.two-formulas__stage'), wrap=q('.two-formulas__image-wrap'), img=q('.two-formulas__image');
  const hs=[...document.querySelectorAll('.two-formulas__feature-heading')].map(r);
  const head=r(q('.two-formulas__header')), w=r(wrap), i=r(img);
  return {width:innerWidth, mode:document.body.className.match(/(day|night)-mode/)?.[0]||'',
    lang:document.documentElement.lang, imgDone:img.complete&&img.naturalWidth>0,
    imgTop:i.top, imgH:i.height, wrapTop:w.top, wrapH:w.height, wrapW:w.width,
    headerBottom:head.bottom, headingTops:hs.map(h=>h.top), headingLefts:hs.map(h=>h.left),
    headingRights:hs.map(h=>h.right), headings:[...document.querySelectorAll('.two-formulas__feature-heading')].map(e=>e.textContent.trim()),
    stageTop:r(stage).top+scrollY, stageH:r(stage).height, docW:document.documentElement.scrollWidth}
})()'''


def wait_for_section():
    # The Day/Night control can re-render the page; wait until the section is back
    for _ in range(40):
        try:
            if evaluate('document.readyState=="complete"&&!!document.querySelector(".two-formulas__image")'):
                return
        except SystemExit:
            pass
        time.sleep(0.5)
    raise SystemExit('two-formulas section did not come back')


VIEWPORT = []


def render():
    # The Orca tab only lays out and paints a new frame when a screenshot is taken, and it
    # sometimes drops the viewport override, so re-apply it first
    if VIEWPORT:
        orca('exec', '--command', 'set viewport %d %d' % (VIEWPORT[0], HEIGHT))
    png = base64.b64decode(orca('screenshot', '--format', 'png')['data'], validate=True)
    assert png.startswith(b'\x89PNG\r\n\x1a\n')
    return png


def settle(width, mode):
    VIEWPORT[:] = [width]
    for _ in range(8):
        render()
        wait_for_section()
        state = evaluate('[innerWidth, document.body.classList.contains("' + mode + '-mode")]')
        if state == [width, True]:
            return
        if not state[1]:
            evaluate('(()=>{const e=document.querySelector(".kc_' + mode + '");if(e)e.click();return 1})()')
        time.sleep(0.8)
    raise SystemExit(f'could not settle {width} {mode}: {state}')


def shoot(lang, width, mode, tag):
    settle(width, mode)
    set_css(QA_CSS + ('\n' + AFTER_CSS if tag == 'after' else ''))
    render()
    if tag == 'square':
        # Chrome grows the square box to the picture; iOS Safari keeps it square (Victor's
        # screenshot). Emulate that by fixing the box height to its width.
        side = evaluate('document.querySelector(".two-formulas__image-wrap").getBoundingClientRect().width')
        set_css(QA_CSS + '\n.two-formulas__image-wrap{height:%.2fpx!important;min-height:0!important}' % side)
        render()
    # Put the tubes just under the fixed header
    evaluate('(()=>{const w=document.querySelector(".two-formulas__image-wrap");'
             'scrollTo(0,w.getBoundingClientRect().top+scrollY-90);return scrollY})()')
    for _ in range(20):
        render()
        m = evaluate(MEASURE)
        if m['imgDone']:
            break
        time.sleep(0.5)
    time.sleep(0.6)
    render()
    m = evaluate(MEASURE)
    png = render()
    check = evaluate(MEASURE)
    if (check['width'], check['mode'], check['wrapH'], check['imgTop']) != (m['width'], m['mode'], m['wrapH'], m['imgTop']):
        raise SystemExit(f'layout moved during the shot: {m} vs {check}')
    if m['width'] != width or m['mode'] != mode + '-mode':
        raise SystemExit(f'wrong state for {width} {mode}: {m}')
    name = f'two-formulas-{width}-{mode}-{lang}-{tag}'
    (OUT / f'{name}.png').write_bytes(png)
    k = m['imgH'] / FILE_H
    m.update(tag=tag, file=f'{name}.png', tubeTop=round(m['imgTop'] + TUBE_TOP * k, 1),
             tubeBase=round(m['imgTop'] + TUBE_BASE * k, 1))
    # Stacked: headings sit under the tubes, so the gap is heading top minus tube base
    m['gapBaseToHeading'] = round(min(m['headingTops']) - m['tubeBase'], 1)
    m['gapHeaderToTube'] = round(m['tubeTop'] - m['headerBottom'], 1)
    return m


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    rows = []
    for lang, url in LANGS.items():
        orca('goto', '--url', url)
        time.sleep(2)
        render()
        wait_for_section()
        if evaluate('document.documentElement.lang') != lang:
            raise SystemExit(f'{url} is not in {lang}')
        for width in WIDTHS:
            for mode in ('day', 'night'):
                for tag in TAGS:
                    row = shoot(lang, width, mode, tag)
                    rows.append(row)
                    print(json.dumps({k: row[k] for k in ('file', 'mode', 'wrapH', 'gapBaseToHeading',
                                                          'gapHeaderToTube')}), flush=True)
    (OUT / ('two-formulas-measurements-%s.json' % '-'.join(TAGS))).write_text(json.dumps(rows, indent=1, ensure_ascii=False) + '\n')


if __name__ == '__main__':
    main()
