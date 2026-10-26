#!/usr/bin/env python3
"""Astra R92 B1 recheck: load at one side of 750, resize to the other, then show all seven window
messages and confirm the dial does not move and the copy reservation fits the new typography.

Runs on the local previews (index.html, index-nl.html, index-fr.html with the branch clock JS/CSS).
Usage: python3 -I docs/homepage/preview-clock/retest-r92.py <page-id>
"""
import base64
import json
import subprocess
import sys
import time

PAGE = sys.argv[1]
HEIGHT = 900
PAGES = {'en': 'index.html', 'nl': 'index-nl.html', 'fr': 'index-fr.html'}


def orca(*args):
    proc = subprocess.run(['orca', *args, '--page', PAGE, '--json'], capture_output=True, text=True, timeout=90)
    data = json.loads(proc.stdout)
    if not data.get('ok'):
        raise SystemExit(json.dumps(data.get('error')))
    return data['result']


def evaluate(js):
    guarded = ('JSON.stringify((()=>{if(location.host!=="127.0.0.1:9360")return ["blank"];'
               'try{return ["ok",' + js + ']}catch(e){return ["error",String(e)]}})())')
    for _ in range(20):
        found = json.loads(orca('eval', '--expression', guarded)['result'])
        if found[0] == 'ok':
            return found[1]
        if found[0] == 'error':
            raise SystemExit(found[1])
        time.sleep(0.5)
    raise SystemExit('eval kept landing outside the preview')


def frame(width):
    orca('exec', '--command', f'set viewport {width} {HEIGHT}')
    base64.b64decode(orca('screenshot', '--format', 'png')['data'], validate=True)


# One step per message: show it, then report the dial top (relative to the section) and the copy box
SHOW = '''(i=>{const c=document.querySelector(".chronobiology-clock"),p=c.querySelector(".state-copy"),
  r=c.querySelector(".readout");p.textContent=r.getAttribute("data-window-"+i);
  return 1})(%d)'''
MEASURE = '''(()=>{const c=document.querySelector(".chronobiology-clock"),p=c.querySelector(".state-copy"),
  d=c.querySelector(".dial");const s=getComputedStyle(p);
  const probe=p.cloneNode(true);probe.style.minHeight="0";probe.style.position="absolute";probe.style.visibility="hidden";
  probe.style.width=p.clientWidth+"px";p.parentElement.append(probe);let natural=0;
  for(let i=1;i<=7;i++){probe.textContent=c.querySelector(".readout").getAttribute("data-window-"+i);natural=Math.max(natural,probe.getBoundingClientRect().height)}
  probe.remove();
  return {width:innerWidth,dialTop:Math.round((d.getBoundingClientRect().top-c.getBoundingClientRect().top)*10)/10,
  copyH:Math.round(p.getBoundingClientRect().height*10)/10,minHeight:p.style.minHeight,tallestNatural:Math.ceil(natural),
  fontSize:s.fontSize,lineHeight:s.lineHeight,copyWidth:p.clientWidth}})()'''

failures = 0
for lang, page in PAGES.items():
    for start, end in ((750, 749), (749, 750)):
        frame(start)
        evaluate('(()=>{try{sessionStorage.setItem("kc-clock-explored","1")}catch(e){};return 1})()')
        orca('goto', '--url', f'http://127.0.0.1:9360/{page}?v={time.time()}')
        time.sleep(2)
        frame(start)
        evaluate('document.fonts.ready.then(()=>1)&&1')
        time.sleep(1)
        frame(start)
        loaded = evaluate(MEASURE)
        frame(end)
        time.sleep(0.4)
        frame(end)
        tops, heights = [], []
        for i in range(1, 8):
            evaluate(SHOW % i)
            frame(end)
            m = evaluate(MEASURE)
            tops.append(m['dialTop'])
            heights.append(m['copyH'])
        ok = (len(set(tops)) == 1 and m['width'] == end and
              int(m['minHeight'].rstrip('px') or 0) == m['tallestNatural'])
        failures += not ok
        print(json.dumps({'lang': lang, 'load': start, 'resize': end, 'ok': ok,
                          'loadedMinHeight': loaded['minHeight'], 'minHeight': m['minHeight'],
                          'tallestNatural': m['tallestNatural'], 'copyWidth': m['copyWidth'],
                          'font': m['fontSize'] + '/' + m['lineHeight'], 'dialTops': sorted(set(tops)),
                          'copyHeights': sorted(set(heights))}), flush=True)
print('failures', failures)
