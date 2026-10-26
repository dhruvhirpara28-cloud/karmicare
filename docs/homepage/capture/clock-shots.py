#!/usr/bin/env python3
"""Shots of the homepage clock with the branch's knob halo and explore pill injected.

Live www.karmicare.com in one Orca tab; the CSS from clock-invite-after.css is injected and the
section gets .is-inviting (what the script sets on a first visit). Two frames per width and mode,
0.3 s and 0.9 s into the pulse, so the ring shows.

Usage: python3 -I docs/homepage/capture/clock-shots.py <page-id> <out-dir> <width> [<width> ...]
"""
import base64
import json
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
PAGE, OUT, WIDTHS = sys.argv[1], Path(sys.argv[2]), [int(w) for w in sys.argv[3:]]
HEIGHT = 900
CSS = (HERE / 'clock-invite-after.css').read_text() + '\n#shopify-pc__banner,.shopify-pc__banner__dialog{display:none!important}'


def orca(*args):
    proc = subprocess.run(['orca', *args, '--page', PAGE, '--json'], capture_output=True, text=True, timeout=90)
    data = json.loads(proc.stdout)
    if not data.get('ok'):
        raise SystemExit(json.dumps(data.get('error')))
    return data['result']


def evaluate(js):
    guarded = ('JSON.stringify((()=>{if(location.host!=="www.karmicare.com")return ["blank"];'
               'try{return ["ok",' + js + ']}catch(e){return ["error",String(e)]}})())')
    for _ in range(20):
        found = json.loads(orca('eval', '--expression', guarded)['result'])
        if found[0] == 'ok':
            return found[1]
        if found[0] == 'error':
            raise SystemExit(found[1])
        time.sleep(0.5)
    raise SystemExit('eval kept landing outside the storefront')


def frame(width):
    orca('exec', '--command', f'set viewport {width} {HEIGHT}')
    png = base64.b64decode(orca('screenshot', '--format', 'png')['data'], validate=True)
    assert png.startswith(b'\x89PNG\r\n\x1a\n')
    return png


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    orca('goto', '--url', 'https://www.karmicare.com/')
    time.sleep(2)
    for width in WIDTHS:
        for mode in ('day', 'night'):
            frame(width)
            evaluate('(()=>{const e=document.querySelector(".kc_' + mode + '");if(e&&!document.body.classList.contains("' + mode + '-mode"))e.click();return 1})()')
            time.sleep(0.8)
            frame(width)
            evaluate('(()=>{let s=document.getElementById("kc-clock-qa");if(!s){s=document.createElement("style");s.id="kc-clock-qa";document.head.append(s)}'
                     's.textContent=' + json.dumps(CSS) + ';const c=document.querySelector(".chronobiology-clock");c.classList.add("is-inviting");'
                     'const d=c.querySelector(".dial");scrollTo(0,d.getBoundingClientRect().top+scrollY-60);return 1})()')
            frame(width)
            state = evaluate('[innerWidth,document.body.className.match(/(day|night)-mode/)?.[0],'
                             'getComputedStyle(document.querySelector(".chronobiology-clock .hint")).display,'
                             'getComputedStyle(document.querySelector(".chronobiology-clock .dial")).touchAction,'
                             'getComputedStyle(document.querySelector(".chronobiology-clock .knob")).touchAction]')
            print(json.dumps({'width': width, 'mode': mode, 'state': state}), flush=True)
            if state[0] != width or state[1] != mode + '-mode':
                raise SystemExit(f'wrong state: {state}')
            for i, wait in enumerate((0.3, 0.6)):
                time.sleep(wait)
                (OUT / f'clock-{width}-{mode}-after-{i + 1}.png').write_bytes(frame(width))


if __name__ == '__main__':
    main()
