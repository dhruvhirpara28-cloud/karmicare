#!/usr/bin/env python3
"""Check the clock preview swing and the halo pulse on the live homepage with the branch script.

The live clock element is replaced by a fresh clone (no listeners), the branch's
assets/chronobiology-clock-karmicare.js runs on it, and the branch halo rules are injected. The
page then scrolls the ring into view and frames are taken through the swing and the pulses, with
the knob position and the halo state per frame.

Usage: python3 -I docs/homepage/capture/clock-preview-check.py <page-id> <out-dir> <width>
"""
import base64
import json
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PAGE, OUT, WIDTH = sys.argv[1], Path(sys.argv[2]), int(sys.argv[3])
HEIGHT = 900
SCRIPT = (ROOT / 'assets/chronobiology-clock-karmicare.js').read_text()
# The live stylesheet still has the old infinite pulse; the branch rule wins here with !important
CSS = '''
#shopify-pc__banner,.shopify-pc__banner__dialog{display:none!important}
.chronobiology-clock .dial{touch-action:auto!important}
.chronobiology-clock .knob::after{inset:-4px;opacity:0}
.chronobiology-clock.is-inviting .knob::after{animation:kc-qa-invite 1.4s ease-out 3!important}
@keyframes kc-qa-invite{0%{opacity:.7;transform:scale(1)}70%,100%{opacity:0;transform:scale(1.35)}}
'''


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


def frame():
    orca('exec', '--command', f'set viewport {WIDTH} {HEIGHT}')
    png = base64.b64decode(orca('screenshot', '--format', 'png')['data'], validate=True)
    assert png.startswith(b'\x89PNG\r\n\x1a\n')
    return png


STATE = '''(()=>{const c=document.querySelector(".chronobiology-clock"),k=c.querySelector(".knob"),
  a=getComputedStyle(k,"::after");return {inviting:c.classList.contains("is-inviting"),left:k.style.left,top:k.style.top,
  time:c.querySelector(".clock-time").textContent,haloOpacity:a.opacity,haloTransform:a.transform,haloAnim:a.animationName,
  explored:sessionStorage.getItem("kc-clock-explored"),width:innerWidth}})()'''


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    orca('goto', '--url', 'https://www.karmicare.com/')
    time.sleep(2)
    frame()
    # Start well above the section so the observer sees the ring come into view
    evaluate('(()=>{sessionStorage.removeItem("kc-clock-explored");const c=document.querySelector(".chronobiology-clock");'
             'const f=c.cloneNode(true);f.classList.remove("is-inviting");c.replaceWith(f);'
             'let s=document.getElementById("kc-clock-qa");if(!s){s=document.createElement("style");s.id="kc-clock-qa";document.body.append(s)}'
             's.textContent=' + json.dumps(CSS) + ';scrollTo(0,f.getBoundingClientRect().top+scrollY-1600);return 1})()')
    frame()
    evaluate('(function(){' + SCRIPT + '\n;return 1})()')
    frame()
    before = evaluate(STATE)
    print(json.dumps({'t': 'loaded, out of view', **before}), flush=True)
    evaluate('(()=>{const d=document.querySelector(".chronobiology-clock .dial");'
             'scrollTo(0,d.getBoundingClientRect().top+scrollY-60);return scrollY})()')
    start = time.time()
    for i in range(16):
        png = frame()
        state = evaluate(STATE)
        t = round(time.time() - start, 2)
        (OUT / f'clock-preview-{WIDTH}-{i:02d}.png').write_bytes(png)
        print(json.dumps({'t': t, **state}), flush=True)
        time.sleep(0.25)


if __name__ == '__main__':
    main()
