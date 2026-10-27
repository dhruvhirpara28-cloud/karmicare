#!/usr/bin/env python3
"""Astra R93b B3 recheck on the local previews: on phones the time badge must never cover the
Awake or Asleep word, while it keeps clear of the held knob and inside the ring. Every 5 minutes
(288 positions) per language and width; the glide is switched off so the end positions count.

Usage: python3 -I docs/homepage/preview-clock/retest-r93b.py <page-id> [widths]
"""
import base64
import json
import subprocess
import sys
import time

PAGE = sys.argv[1]
WIDTHS = [int(w) for w in (sys.argv[2] if len(sys.argv) > 2 else '360,374,390').split(',')]
HEIGHT = 900
PAGES = {'en': 'index.html', 'nl': 'index-nl.html', 'fr': 'index-fr.html'}


def orca(*args):
    proc = subprocess.run(['orca', *args, '--page', PAGE, '--json'], capture_output=True, text=True, timeout=120)
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


SWEEP = '''(()=>{const c=document.querySelector(".chronobiology-clock"),k=c.querySelector(".knob"),t=c.querySelector(".knob-time");
  let s=document.getElementById("kc-qa-noglide");if(!s){s=document.createElement("style");s.id="kc-qa-noglide";document.head.append(s)}
  s.textContent=".knob-time.is-switching{transition:none!important}";
  const key=k2=>k.dispatchEvent(new KeyboardEvent("keydown",{key:k2,bubbles:true,cancelable:true}));
  const hit=(a,r)=>a.left<r.right&&a.right>r.left&&a.top<r.bottom&&a.bottom>r.top;
  const labels=[...c.querySelectorAll(".shift-label")].filter(e=>getComputedStyle(e).display!=="none");
  const out={positions:0,labelHits:[],knobMin:99,outsideRing:0,switches:0};let last=null;
  key("Home");
  for(let i=0;i<288;i++){if(i)key("ArrowRight");
    const b=t.getBoundingClientRect(),kb=k.getBoundingClientRect(),d=c.querySelector(".dial").getBoundingClientRect();
    out.positions++;
    labels.forEach(l=>{if(hit(b,l.getBoundingClientRect()))out.labelHits.push(t.textContent+" "+l.textContent)});
    const kx=kb.left+kb.width/2,ky=kb.top+kb.height/2,nx=Math.max(b.left,Math.min(kx,b.right)),ny=Math.max(b.top,Math.min(ky,b.bottom));
    out.knobMin=Math.min(out.knobMin,Math.hypot(nx-kx,ny-ky)-kb.width/2);
    const cx=d.left+d.width/2,cy=d.top+d.height/2,ring=d.width*178/604;
    if(Math.max(...[[b.left,b.top],[b.right,b.top],[b.left,b.bottom],[b.right,b.bottom]].map(([x,y])=>Math.hypot(x-cx,y-cy)))>ring)out.outsideRing++;
    const side=Math.sign((b.left+b.width/2-cx)*(ky-cy)-(b.top+b.height/2-cy)*(kx-cx));if(last!==null&&side!==last)out.switches++;last=side}
  k.dispatchEvent(new KeyboardEvent("keyup",{key:"ArrowRight",bubbles:true}));s.remove();
  out.knobMin=Math.round(out.knobMin*10)/10;return out})()'''

failures = 0
for lang, page in PAGES.items():
    orca('goto', '--url', f'http://127.0.0.1:9360/{page}?day&t={time.time()}')
    time.sleep(2)
    for width in WIDTHS:
        frame(width)
        evaluate('(()=>{try{sessionStorage.setItem("kc-clock-explored","1")}catch(e){};'
                 'const d=document.querySelector(".chronobiology-clock .dial");scrollTo(0,d.getBoundingClientRect().top+scrollY-80);return 1})()')
        frame(width)
        r = evaluate(SWEEP)
        ok = not r['labelHits'] and r['knobMin'] > 0 and r['outsideRing'] == 0
        failures += not ok
        print(json.dumps({'lang': lang, 'width': width, 'ok': ok, **r}, ensure_ascii=False), flush=True)
print('failures', failures)
