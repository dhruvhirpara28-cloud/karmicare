#!/usr/bin/env python3
"""Astra R93 recheck on the local previews (branch clock CSS/JS, option E markup).

B1: with the knob held (keyboard preview, scaled 1.1), at all 24 hours, the time badge must not
touch the knob's circle, must stay inside the dial, and must not touch the copy in the orb (from
750) or the 06:40 / 22:00 time labels. B2: the explore pill holds one line, with the current
label and with round 7's French 'GLISSEZ LE POINT · 24 HEURES'.

Usage: python3 -I docs/homepage/preview-clock/retest-r93.py <page-id> [widths]
"""
import base64
import json
import subprocess
import sys
import time

PAGE = sys.argv[1]
WIDTHS = [int(w) for w in (sys.argv[2] if len(sys.argv) > 2 else '360,390,780,1440').split(',')]
HEIGHT = 900
PAGES = {'en': 'index.html', 'nl': 'index-nl.html', 'fr': 'index-fr.html'}
ROUND7_FR = 'GLISSEZ LE POINT · 24 HEURES'


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


KEY = ('(k=>{document.querySelector(".chronobiology-clock .knob").dispatchEvent(new KeyboardEvent("keydown",'
       '{key:k,bubbles:true,cancelable:true}));return 1})(%s)')
CHECK = '''(()=>{const c=document.querySelector(".chronobiology-clock"),k=c.querySelector(".knob").getBoundingClientRect(),
  b=c.querySelector(".knob-time").getBoundingClientRect(),d=c.querySelector(".dial").getBoundingClientRect();
  const kx=k.left+k.width/2,ky=k.top+k.height/2,kr=k.width/2;
  const nx=Math.max(b.left,Math.min(kx,b.right)),ny=Math.max(b.top,Math.min(ky,b.bottom));
  const knobGap=Math.hypot(nx-kx,ny-ky)-kr;
  const dx=d.left+d.width/2,dy=d.top+d.height/2,dr=d.width/2;
  const outside=Math.max(...[[b.left,b.top],[b.right,b.top],[b.left,b.bottom],[b.right,b.bottom]].map(([x,y])=>Math.hypot(x-dx,y-dy)))-dr;
  const hit=(a,r)=>a.left<r.right&&a.right>r.left&&a.top<r.bottom&&a.bottom>r.top;
  const orb=c.querySelector(".orb-text"),inOrb=getComputedStyle(orb).position==="absolute";
  const lines=[];if(inOrb){const w=document.createTreeWalker(orb,NodeFilter.SHOW_TEXT);let n;while((n=w.nextNode())){const r=document.createRange();r.selectNodeContents(n);lines.push(...r.getClientRects())}}
  const labels=[...c.querySelectorAll(".time-label")].filter(e=>getComputedStyle(e).display!=="none").map(e=>e.getBoundingClientRect());
  return {time:c.querySelector(".clock-time").textContent,knobGap:Math.round(knobGap*10)/10,outsideDial:Math.round(outside*10)/10,
    hitsCopy:lines.some(r=>hit(b,r)),hitsTimeLabel:labels.some(r=>hit(b,r)),scale:getComputedStyle(c.querySelector(".knob")).transform}})()'''
PILL = '''(t=>{const h=document.querySelector(".chronobiology-clock .hint"),s=h.querySelector("span");if(t)s.textContent=t;
  const r=document.createRange();r.selectNodeContents(s);const lines=new Set([...r.getClientRects()].map(x=>Math.round(x.top))).size;
  return {text:s.textContent,lines,pill:Math.round(h.getBoundingClientRect().width),fits:h.scrollWidth<=h.clientWidth}})(%s)'''

failures = 0
for lang, page in PAGES.items():
    orca('goto', '--url', f'http://127.0.0.1:9360/{page}?day&t={time.time()}')
    time.sleep(2)
    for width in WIDTHS:
        frame(width)
        evaluate('(()=>{try{sessionStorage.setItem("kc-clock-explored","1")}catch(e){};return 1})()')
        evaluate('(()=>{const d=document.querySelector(".chronobiology-clock .dial");scrollTo(0,d.getBoundingClientRect().top+scrollY-80);return 1})()')
        frame(width)
        worst = {'knobGap': 99, 'outsideDial': -99}
        bad = []
        evaluate(KEY % json.dumps('Home'))
        for hour in range(24):
            if hour:
                evaluate(KEY % json.dumps('PageUp'))
            frame(width)
            m = evaluate(CHECK)
            worst['knobGap'] = min(worst['knobGap'], m['knobGap'])
            worst['outsideDial'] = max(worst['outsideDial'], m['outsideDial'])
            if m['knobGap'] < 0 or m['outsideDial'] > 0 or m['hitsCopy'] or m['hitsTimeLabel']:
                bad.append(m)
        evaluate('(()=>{document.querySelector(".chronobiology-clock .knob").dispatchEvent(new KeyboardEvent("keyup",{key:"PageUp",bubbles:true}));return 1})()')
        pills = [evaluate(PILL % 'null')]
        if lang == 'fr':
            pills.append(evaluate(PILL % json.dumps(ROUND7_FR)))
        ok = not bad and all(p['lines'] == 1 and p['fits'] for p in pills)
        failures += not ok
        print(json.dumps({'lang': lang, 'width': width, 'ok': ok, 'minKnobGap': worst['knobGap'],
                          'maxOutsideDial': worst['outsideDial'], 'badPositions': bad[:3],
                          'pills': [(p['text'][:22], p['lines'], p['pill']) for p in pills]}, ensure_ascii=False), flush=True)
print('failures', failures)
