#!/usr/bin/env python3
"""Measure the clock arrival on the local preview: knob time before the dial is in view, its run
to now once scrolled in, and the halo state until a pointerdown on the knob.

Usage: python3 -I docs/homepage/preview-clock/check.py <page-id> <width>
"""
import base64
import json
import subprocess
import sys
import time

PAGE, WIDTH = sys.argv[1], int(sys.argv[2])
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
    orca('exec', '--command', f'set viewport {WIDTH} {HEIGHT}')
    base64.b64decode(orca('screenshot', '--format', 'png')['data'], validate=True)


# Knob angle back to clock minutes (noon on top), and the halo state
STATE = '''(()=>{const c=document.querySelector(".chronobiology-clock"),k=c.querySelector(".knob"),
  a=+k.dataset.angle,m=Math.round(((a/360*24+12)%24)*60),f=x=>String(Math.floor(x/60)).padStart(2,"0")+":"+String(x%60).padStart(2,"0");
  const h=getComputedStyle(k,"::after");return {knob:f(m),readout:c.querySelector(".clock-time").textContent,
  inviting:c.classList.contains("is-inviting"),halo:h.animationName+" "+h.animationIterationCount,haloOpacity:(+h.opacity).toFixed(2)}})()'''

frame()
evaluate('(()=>{sessionStorage.removeItem("kc-clock-explored");return 1})()')
orca('goto', '--url', 'http://127.0.0.1:9360/index.html?v=%d' % time.time())
time.sleep(2)
frame()
print(json.dumps({'t': 'top of page', **evaluate(STATE)}), flush=True)
evaluate('(()=>{const d=document.querySelector(".chronobiology-clock .dial");scrollTo(0,d.getBoundingClientRect().top+scrollY-60);return 1})()')
start = time.time()
for _ in range(12):
    frame()
    print(json.dumps({'t': round(time.time() - start, 2), **evaluate(STATE)}), flush=True)
    time.sleep(0.3)
time.sleep(6)
frame()
print(json.dumps({'t': 'after 10 s', **evaluate(STATE)}), flush=True)
evaluate('(()=>{const k=document.querySelector(".chronobiology-clock .knob");'
         'k.dispatchEvent(new PointerEvent("pointerdown",{isPrimary:true,button:0,pointerId:1,bubbles:true}));'
         'document.dispatchEvent(new PointerEvent("pointerup",{pointerId:1,bubbles:true}));return 1})()')
frame()
print(json.dumps({'t': 'after taking the knob', **evaluate(STATE),
                  'explored': evaluate('sessionStorage.getItem("kc-clock-explored")')}), flush=True)
