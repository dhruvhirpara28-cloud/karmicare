#!/usr/bin/env python3
"""Shots and checks of the three clock readout options (BRIEF-CLOCK-READOUT-UX.md) on the local
previews: per variant, language, width and mode one frame at rest and one mid-drag (the knob held
at 07:30), then a drag through the seven windows that records the dial top (it must not move).

Usage: python3 -I docs/homepage/preview-clock/variants-shots.py <page-id> <out-dir> [variants] [langs] [widths]
       e.g. ... abc en,nl,fr 390,1440
"""
import base64
import json
import math
import subprocess
import sys
import time
from pathlib import Path

PAGE, OUT = sys.argv[1], Path(sys.argv[2])
VARIANTS = sys.argv[3] if len(sys.argv) > 3 else 'abc'
LANGS = (sys.argv[4] if len(sys.argv) > 4 else 'en,nl,fr').split(',')
WIDTHS = [int(w) for w in (sys.argv[5] if len(sys.argv) > 5 else '390,1440').split(',')]
EXTRA = sys.argv[6] if len(sys.argv) > 6 else ''
HEIGHT = 900
PAGES = {'en': 'index.html', 'nl': 'index-nl.html', 'fr': 'index-fr.html'}
# Window midpoints (minutes) for the drag sweep: 06:30, 09:30, 12:30, 15:30, 18:30, 21:30, 02:00
SWEEP = [390, 570, 750, 930, 1110, 1290, 120]


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
    # The Orca pane sometimes hands back a blank one-colour frame (a few KB); take it again
    for _ in range(5):
        orca('exec', '--command', f'set viewport {width} {HEIGHT}')
        png = base64.b64decode(orca('screenshot', '--format', 'png')['data'], validate=True)
        assert png.startswith(b'\x89PNG\r\n\x1a\n')
        if len(png) > 30000:
            return png
        time.sleep(0.8)
    return png


def point_for(minutes):
    # The clock script's angle: noon on top, clockwise; the knob rides at 178/604 of the dial
    angle = (((minutes / 60) + 12) % 24) / 24 * 2 * math.pi
    return ('(()=>{const d=document.querySelector(".chronobiology-clock .dial").getBoundingClientRect();'
            'const r=d.width*178/604;return [d.left+d.width/2+r*%f,d.top+d.height/2-r*%f]})()'
            % (math.sin(angle), math.cos(angle)))


PRESS = ('(()=>{const k=document.querySelector(".chronobiology-clock .knob"),b=k.getBoundingClientRect();'
         'k.dispatchEvent(new PointerEvent("pointerdown",{isPrimary:true,button:0,pointerId:7,bubbles:true,'
         'clientX:b.left+b.width/2,clientY:b.top+b.height/2}));return 1})()')
MOVE = ('(p=>{document.dispatchEvent(new PointerEvent("pointermove",{isPrimary:true,pointerId:7,bubbles:true,'
        'cancelable:true,clientX:p[0],clientY:p[1]}));return 1})(%s)')
RELEASE = '(()=>{document.dispatchEvent(new PointerEvent("pointerup",{pointerId:7,bubbles:true}));return 1})()'
STATE = ('(()=>{const c=document.querySelector(".chronobiology-clock");const d=c.querySelector(".dial").getBoundingClientRect();'
         'return {width:innerWidth,mode:(document.body.className.match(/(day|night)-mode/)||[])[0],variant:document.documentElement.dataset.kcVariant,'
         'dialTop:Math.round((d.top-c.getBoundingClientRect().top)*10)/10,time:c.querySelector(".clock-time").textContent,'
         'copy:c.querySelector(".state-copy").textContent.slice(0,40),docW:document.documentElement.scrollWidth}})()')


def settle(width, mode):
    for _ in range(8):
        frame(width)
        state = evaluate('[innerWidth,document.body.classList.contains("%s-mode")]' % mode)
        if state == [width, True]:
            return
        if not state[1]:
            evaluate('(()=>{const e=document.querySelector(".kc_%s");if(e)e.click();return 1})()' % mode)
        time.sleep(0.6)
    raise SystemExit(f'could not settle {width} {mode}')


OUT.mkdir(parents=True, exist_ok=True)
rows = []
for variant in VARIANTS:
    for lang in LANGS:
        frame(WIDTHS[0])
        evaluate('(()=>{try{sessionStorage.setItem("kc-clock-explored","1")}catch(e){};return 1})()')
        orca('goto', '--url', f'http://127.0.0.1:9360/{PAGES[lang]}?variant={variant}{EXTRA}&t={time.time()}')
        time.sleep(2)
        for width in WIDTHS:
            for mode in ('day', 'night'):
                settle(width, mode)
                evaluate('(()=>{const d=document.querySelector(".chronobiology-clock .dial");'
                         'scrollTo(0,d.getBoundingClientRect().top+scrollY-(innerWidth<750?150:60));return 1})()')
                frame(width)
                time.sleep(0.4)
                name = f'{variant}-{lang}-{width}-{mode}'
                (OUT / f'{name}-rest.png').write_bytes(frame(width))
                rest = evaluate(STATE)
                evaluate(PRESS)
                tops = []
                for minutes in SWEEP:
                    evaluate(MOVE % point_for(minutes))
                    frame(width)
                    tops.append(evaluate(STATE)['dialTop'])
                evaluate(MOVE % point_for(450))
                frame(width)
                time.sleep(0.3)
                (OUT / f'{name}-drag.png').write_bytes(frame(width))
                held = evaluate(STATE)
                evaluate(RELEASE)
                row = {'variant': variant, 'lang': lang, 'width': width, 'mode': mode, 'restTime': rest['time'],
                       'heldTime': held['time'], 'dialTops': sorted(set(tops + [rest['dialTop'], held['dialTop']])),
                       'docW': held['docW'], 'ok': len(set(tops + [rest['dialTop'], held['dialTop']])) == 1 and held['docW'] == width}
                rows.append(row)
                print(json.dumps(row), flush=True)
(OUT / f'variants-{VARIANTS}-{"-".join(LANGS)}.json').write_text(json.dumps(rows, indent=1) + '\n')
