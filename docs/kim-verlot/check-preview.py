"""Read-only browser QA of the branch preview; no Shopify writes.

Run from this checkout with the Orca page ID as argument. --fixture additionally
substitutes only Kim's photo and NL/FR quote in the browser DOM for layout review.
That mode is not evidence of Shopify Files upload or translation registration.
"""
import base64
import json
from pathlib import Path
import subprocess
import shutil
import sys
import time

HERE = Path(__file__).resolve().parent
PAGE = sys.argv[1]
FIXTURE = '--fixture' in sys.argv
TEXTS = json.loads((HERE / 'testimonials.json').read_text())
CARD = '[data-block-id="card_qAPajg"]:not([data-marquee-clone])'


def orca(*args):
    p = subprocess.run(['orca', *args, '--page', PAGE, '--json'], capture_output=True, text=True)
    data = json.loads(p.stdout)
    assert data.get('ok'), data
    return data['result']


def js(code):
    result = orca('eval', '--expression', code)['result']
    if isinstance(result, str):
        try:
            return json.loads(result)
        except json.JSONDecodeError:
            return result
    return result


def shot(name):
    result = orca('exec', '--command', 'screenshot')
    (HERE / 'shots').mkdir(exist_ok=True)
    shutil.copyfile(result['path'], HERE / 'shots' / (name + '.png'))


results = []
for route in ['/', '/products/karmicare-biorhythmic-oral-care-system']:
    orca('goto', '--url', 'http://127.0.0.1:17145' + route)
    orca('wait', '--selector', CARD)
    time.sleep(1)
    assert js('Shopify.theme.id') == 190213947773
    assert js('Shopify.theme.role') == 'unpublished'
    for width in ([393, 1440] if FIXTURE or '--captures' in sys.argv else [393, 768, 1024, 1440, 1920, 2560]):
        orca('exec', '--command', f'set viewport {width} 1000')
        for lang in (['nl', 'fr'] if FIXTURE else ['en']):
            if FIXTURE:
                photo = 'http://127.0.0.1:17146/kc-professional-kim-verlot.png'
                js('(()=>{for(const c of document.querySelectorAll("[data-block-id=card_qAPajg]")){c.querySelector(".trusted-professionals__card-quote-text").innerHTML=' + json.dumps('<p>“' + TEXTS[lang] + '”</p>') + ';const i=c.querySelector("img");i.removeAttribute("srcset");i.src=' + json.dumps(photo) + ';}return true})()')
            for mode in ['day', 'night']:
                js('(()=>{const b=document.querySelector(".kc_' + mode + '");if(b){b.click()}else{document.body.classList.remove("day-mode","night-mode");document.body.classList.add("' + mode + '-mode")}const c=document.querySelector(' + json.dumps(CARD) + ');c.scrollIntoView({block:"center",inline:"center"});c.focus();return true})()')
                time.sleep(0.8)
                # Orca's offscreen tab advances paint/RAF when captured.
                # Exercise the real ResizeObserver/RAF path, never call measure().
                orca('exec', '--command', 'screenshot --full')
                time.sleep(0.2)
                orca('exec', '--command', 'screenshot --full')
                data = js('(()=>{const c=document.querySelector(' + json.dumps(CARD) + '),q=c.querySelector(".trusted-professionals__card-quote-text"),i=c.querySelector("img"),h=c.querySelector(".trusted-professionals__card-quote-inner");return {count:document.querySelectorAll(' + json.dumps(CARD) + ').length,name:c.querySelector("h3").textContent.trim(),title:c.querySelector(".trusted-professionals__card-title").textContent.trim(),quote:q.textContent.trim(),imageLoaded:i.complete&&i.naturalWidth>0,imageWidth:i.naturalWidth,cardWidth:c.clientWidth,cardHeight:c.clientHeight,long:c.hasAttribute("data-long-quote"),quoteHeight:q.clientHeight,quoteScroll:q.scrollHeight,overflow:getComputedStyle(h).overflowY,mode:document.body.className,pageOverflow:document.documentElement.scrollWidth>innerWidth}})()')
                assert data['count'] == 1 and data['name'] == 'Kim Verlot', data
                assert data['title'] == 'Breathing Coach, Heart Coherence Specialist', data
                assert data['quote'] == '“' + TEXTS[lang] + '”', data
                assert data['imageLoaded'] and mode + '-mode' in data['mode'], data
                assert not data['pageOverflow'], data
                if width < 750:
                    assert data['long'], data
                    js('document.querySelector(' + json.dumps(CARD) + ').querySelector("button").click()')
                    time.sleep(0.3)
                    panel = js('(()=>{const p=document.querySelector("dialog.trusted-professionals__panel[open]");p.scrollTop=p.scrollHeight;return {quote:p.querySelector("[data-quote-panel-quote]").textContent.trim(),name:p.querySelector("[data-quote-panel-name]").textContent,scrollTop:p.scrollTop,scrollHeight:p.scrollHeight,height:p.clientHeight,width:p.clientWidth,focusInside:p.contains(document.activeElement)}})()')
                    assert panel['quote'] == data['quote'] and panel['name'] == data['name'] and panel['focusInside'], panel
                    data['panel'] = panel
                else:
                    assert data['overflow'] == 'auto', data
                label = ('pdp' if route != '/' else 'home') + f'-{width}-{mode}-{lang}' + ('-fixture' if FIXTURE else '')
                if width in [393, 1440]:
                    shot(label)
                if width < 750:
                    orca('keypress', '--key', 'Escape')
                    time.sleep(0.15)
                    assert js('document.activeElement.classList.contains("trusted-professionals__card-eye")')
                results.append(dict(route=route,width=width,lang=lang,mode=mode,fixture=FIXTURE,**{'checks':data}))
                print(label, 'PASS', flush=True)
(HERE / ('qa-fixture.json' if FIXTURE else 'qa-captures.json' if '--captures' in sys.argv else 'qa-preview.json')).write_text(json.dumps(results, indent=2, ensure_ascii=False) + '\n')
