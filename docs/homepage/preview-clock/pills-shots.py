#!/usr/bin/env python3
"""Shots of the glass pills (clock explore pill, Two Formulas ingredient pills) on the local
preview, in Day and Night, with their computed border, fill and blur.

Usage: python3 -I docs/homepage/preview-clock/pills-shots.py <page-id> <out-dir> <width> [page]
"""
import base64
import json
import subprocess
import sys
import time
from pathlib import Path

PAGE, OUT, WIDTH = sys.argv[1], Path(sys.argv[2]), int(sys.argv[3])
FILE = sys.argv[4] if len(sys.argv) > 4 else 'index.html'
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


def frame():
    for _ in range(5):
        orca('exec', '--command', f'set viewport {WIDTH} {HEIGHT}')
        png = base64.b64decode(orca('screenshot', '--format', 'png')['data'], validate=True)
        if len(png) > 30000:
            return png
        time.sleep(0.8)
    return png


STYLE = '''(s=>{const e=document.querySelector(s);const c=getComputedStyle(e);
  return {border:c.borderTopWidth+" "+c.borderTopColor,fill:c.backgroundColor,blur:c.backdropFilter}})(%s)'''

OUT.mkdir(parents=True, exist_ok=True)
orca('goto', '--url', f'http://127.0.0.1:9360/{FILE}?day&t={time.time()}')
time.sleep(2)
for mode in ('day', 'night'):
    for _ in range(6):
        frame()
        if evaluate('document.body.classList.contains("%s-mode")' % mode):
            break
        evaluate('(()=>{const e=document.querySelector(".kc_%s");if(e)e.click();return 1})()' % mode)
        time.sleep(0.6)
    for name, selector in (('clock-pill', '.chronobiology-clock .hint'), ('two-formulas-pills', '.two-formulas__pills li')):
        evaluate('(()=>{const e=document.querySelector(%s);scrollTo(0,e.getBoundingClientRect().top+scrollY-260);return 1})()'
                 % json.dumps(selector))
        frame()
        time.sleep(0.4)
        (OUT / f'{name}-{WIDTH}-{mode}.png').write_bytes(frame())
        print(json.dumps({'mode': mode, 'pill': name, **evaluate(STYLE % json.dumps(selector))}), flush=True)
