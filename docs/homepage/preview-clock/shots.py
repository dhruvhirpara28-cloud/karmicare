#!/usr/bin/env python3
"""Shots of the clock section on the local preview, with the readout and pill geometry.

Usage: python3 -I docs/homepage/preview-clock/shots.py <page-id> <out-dir> <width> [<width> ...]
"""
import base64
import json
import subprocess
import sys
import time
from pathlib import Path

PAGE, OUT, WIDTHS = sys.argv[1], Path(sys.argv[2]), [int(w) for w in sys.argv[3:]]
HEIGHT = 900


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
    png = base64.b64decode(orca('screenshot', '--format', 'png')['data'], validate=True)
    assert png.startswith(b'\x89PNG\r\n\x1a\n')
    return png


# Vertical steps between the blocks, in CSS px
GEOMETRY = '''(()=>{const c=document.querySelector(".chronobiology-clock"),r=s=>c.querySelector(s).getBoundingClientRect();
  const h=r(".heading"),t=r(".time-line"),p=r(".state-copy"),b=r(".hint"),d=r(".dial"),sun=r(".sun"),tl=r(".timeline");
  return {width:innerWidth,headingToTime:Math.round(t.top-h.bottom),timeToCopy:Math.round(p.top-t.bottom),
  copyHeight:Math.round(p.height),copyToPill:Math.round(b.top-p.bottom),pillToTimeline:Math.round(tl.top-b.bottom),
  pillToSun:Math.round(sun.top-b.bottom),order:[...c.querySelector(".readout").children].map(e=>e.className.split(" ")[0]).join(">")}})()'''

OUT.mkdir(parents=True, exist_ok=True)
orca('goto', '--url', 'http://127.0.0.1:9360/index.html?v=%d' % time.time())
time.sleep(2)
for width in WIDTHS:
    frame(width)
    evaluate('(()=>{try{sessionStorage.setItem("kc-clock-explored","1")}catch(e){}'
             'const c=document.querySelector(".chronobiology-clock .heading");scrollTo(0,c.getBoundingClientRect().top+scrollY-70);return 1})()')
    frame(width)
    print(json.dumps(evaluate(GEOMETRY)), flush=True)
    (OUT / f'clock-readout-above-{width}.png').write_bytes(frame(width))
