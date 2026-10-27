#!/usr/bin/env python3
"""Measure the knob arrival (Victor, 26 Oct): hidden until 15% of the section is in view, then in
2.4 s the run from two hours early to now while it fades in and its icon turns 360 degrees, then
the halo until the knob is taken.

Usage: python3 -I docs/homepage/preview-clock/arrival-check.py <page-id> <width> [query]
"""
import base64
import json
import subprocess
import sys
import time

PAGE, WIDTH = sys.argv[1], int(sys.argv[2])
QUERY = sys.argv[3] if len(sys.argv) > 3 else 'variant=d'
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


STATE = '''(()=>{const c=document.querySelector(".chronobiology-clock"),k=c.querySelector(".knob"),
  a=+k.dataset.angle,m=Math.round(((a/360*24+12)%24)*60),f=x=>String(Math.floor(x/60)).padStart(2,"0")+":"+String(x%60).padStart(2,"0");
  const s=c.getBoundingClientRect(),d=c.querySelector(".dial").getBoundingClientRect();
  return {knob:f(m),angle:Math.round(a),opacity:getComputedStyle(k).opacity,iconTurn:k.querySelector("svg").style.transform||"none",readout:c.querySelector(".clock-time").textContent,
  inviting:c.classList.contains("is-inviting"),sectionVisible:Math.round(Math.max(0,Math.min(innerHeight,s.bottom)-Math.max(0,s.top))/s.height*100)+"%",
  dialOnScreen:d.top<innerHeight}})()'''

frame()
evaluate('(()=>{sessionStorage.removeItem("kc-clock-explored");return 1})()')
orca('goto', '--url', f'http://127.0.0.1:9360/index.html?{QUERY}&t={time.time()}')
time.sleep(2)
frame()
print(json.dumps({'t': 'top of page', **evaluate(STATE)}), flush=True)
# Bring the section in until about 20% of it shows: the heading, not yet the dial
evaluate('(()=>{const c=document.querySelector(".chronobiology-clock"),r=c.getBoundingClientRect();'
         'scrollTo(0,r.top+scrollY-innerHeight+r.height*0.2);return 1})()')
start = time.time()
for _ in range(14):
    frame()
    print(json.dumps({'t': round(time.time() - start, 2), **evaluate(STATE)}), flush=True)
    time.sleep(0.15)
time.sleep(2)
frame()
print(json.dumps({'t': 'later', **evaluate(STATE)}), flush=True)
