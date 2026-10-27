#!/usr/bin/env python3
"""Variant D contrast, measured on real pixels: the orb text is made transparent (shadow off),
the frame is captured, and the orb pixels under every text line are compared with the text colour
(#191f38). Small text needs 4.5:1, large text (the time, 22px+) 3:1. Also checks that the copy box
stays inside the orb's visible disc. Uses the longest window message of the language.

Usage: python3 -I docs/homepage/preview-clock/contrast-sample.py <page-id> <langs> <widths>
"""
import base64
import json
import struct
import subprocess
import sys
import time
import zlib

PAGE = sys.argv[1]
LANGS = sys.argv[2].split(',')
WIDTHS = [int(w) for w in sys.argv[3].split(',')]
EXTRA = sys.argv[4] if len(sys.argv) > 4 else ''
HEIGHT = 900
PAGES = {'en': 'index.html', 'nl': 'index-nl.html', 'fr': 'index-fr.html'}
INK = (0x19, 0x1f, 0x38)


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


def shot(width):
    for _ in range(5):
        orca('exec', '--command', f'set viewport {width} {HEIGHT}')
        png = base64.b64decode(orca('screenshot', '--format', 'png')['data'], validate=True)
        if len(png) > 30000:
            return png
        time.sleep(0.8)
    return png


def decode(png):
    pos, idat = 8, b''
    while pos < len(png):
        n, kind = struct.unpack('>I4s', png[pos:pos + 8])
        body = png[pos + 8:pos + 8 + n]
        if kind == b'IHDR':
            w, h, depth, ctype = struct.unpack('>IIBB', body[:10])
        elif kind == b'IDAT':
            idat += body
        pos += 12 + n
    assert depth == 8 and ctype in (2, 6), (depth, ctype)
    bpp = 4 if ctype == 6 else 3
    raw, stride = zlib.decompress(idat), w * bpp
    rows, prev, i = [], bytearray(stride), 0
    for _ in range(h):
        f, line = raw[i], bytearray(raw[i + 1:i + 1 + stride])
        i += 1 + stride
        if f == 1:
            for x in range(bpp, stride):
                line[x] = (line[x] + line[x - bpp]) & 255
        elif f == 2:
            for x in range(stride):
                line[x] = (line[x] + prev[x]) & 255
        elif f == 3:
            for x in range(stride):
                line[x] = (line[x] + ((line[x - bpp] if x >= bpp else 0) + prev[x]) // 2) & 255
        elif f == 4:
            for x in range(stride):
                a = line[x - bpp] if x >= bpp else 0
                b, c = prev[x], (prev[x - bpp] if x >= bpp else 0)
                p = a + b - c
                pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
                line[x] = (line[x] + (a if pa <= pb and pa <= pc else (b if pb <= pc else c))) & 255
        rows.append(line)
        prev = line
    return w, h, bpp, rows


def lum(rgb):
    def ch(c):
        c /= 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (ch(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


LONGEST = '''(()=>{const r=document.querySelector(".chronobiology-clock .readout"),c=document.querySelector(".chronobiology-clock .state-copy");
  let best=1;for(let i=1;i<=7;i++){if((r.getAttribute("data-window-"+i)||"").length>(r.getAttribute("data-window-"+best)||"").length)best=i}
  c.textContent=r.getAttribute("data-window-"+best);return best})()'''
LINES = '''(()=>{const box=document.querySelector(".orb-text"),out=[];
  const walker=document.createTreeWalker(box,NodeFilter.SHOW_TEXT);let n;
  while((n=walker.nextNode())){if(!n.textContent.trim())continue;const el=n.parentElement,size=parseFloat(getComputedStyle(el).fontSize);
    if(size<1)continue;const range=document.createRange();range.selectNodeContents(n);
    for(const r of range.getClientRects())out.push({x:r.left,y:r.top,w:r.width,h:r.height,size,large:size>=22,cls:el.className})}
  const d=document.querySelector(".chronobiology-clock .dial").getBoundingClientRect(),b=box.getBoundingClientRect(),
    orbR=d.width*0.27;const cx=d.left+d.width/2,cy=d.top+d.height/2;
  const corners=out.flatMap(r=>[[r.x,r.y],[r.x+r.w,r.y],[r.x,r.y+r.h],[r.x+r.w,r.y+r.h]]).map(([x,y])=>Math.hypot(x-cx,y-cy)/orbR);
  const hit=(a,r)=>a.left<r.x+r.w&&a.right>r.x&&a.top<r.y+r.h&&a.bottom>r.y;
  const overlaps=[".shift-awake",".shift-asleep",".knob-time"].filter(s=>{const e=document.querySelector(".chronobiology-clock "+s);
    if(!e||getComputedStyle(e).display==="none"||+getComputedStyle(e).opacity===0)return false;const a=e.getBoundingClientRect();return out.some(r=>hit(a,r))});
  return {lines:out,boxCornerToOrbRadius:Math.max(...corners),boxH:b.height,boxW:b.width,overlaps}})()'''
HIDE = ('(()=>{let s=document.getElementById("kc-qa-hide");if(!s){s=document.createElement("style");s.id="kc-qa-hide";document.head.append(s)}'
        's.textContent=".orb-text,.orb-text *{color:transparent!important;text-shadow:none!important}'
        '.knob-time,.chronobiology-clock .shift-label,.chronobiology-clock .knob{visibility:hidden!important}";return 1})()')
SHOW = '(()=>{document.getElementById("kc-qa-hide")?.remove();return 1})()'

for lang in LANGS:
    query = EXTRA.lstrip('&') if 'variant=' in EXTRA else 'variant=d' + EXTRA
    orca('goto', '--url', f'http://127.0.0.1:9360/{PAGES[lang]}?{query}&t={time.time()}')
    time.sleep(2)
    for width in WIDTHS:
        for mode in ('day', 'night'):
            for _ in range(6):
                shot(width)
                if evaluate('document.body.classList.contains("%s-mode")' % mode):
                    break
                evaluate('(()=>{const e=document.querySelector(".kc_%s");if(e)e.click();return 1})()' % mode)
                time.sleep(0.6)
            evaluate('(()=>{try{sessionStorage.setItem("kc-clock-explored","1")}catch(e){};'
                     'const d=document.querySelector(".chronobiology-clock .dial");scrollTo(0,d.getBoundingClientRect().top+scrollY-100);return 1})()')
            window = evaluate(LONGEST)
            shot(width)
            geo = evaluate(LINES)
            result = {'lang': lang, 'width': width, 'mode': mode, 'longestWindow': window,
                      'boxCornerToOrbRadius': round(geo['boxCornerToOrbRadius'], 2), 'overlaps': geo['overlaps'],
                      'box': [round(geo['boxW']), round(geo['boxH'])]}
            # Bare: text and shadow hidden. Halo: text hidden, its light shadow kept, which is the
            # background the glyphs actually sit on
            for label, css in (('bare', 'color:transparent!important;text-shadow:none!important'),
                               ('halo', 'color:transparent!important')):
                evaluate(HIDE.replace('color:transparent!important;text-shadow:none!important', css))
                w, h, bpp, rows = decode(shot(width))
                evaluate(SHOW)
                worst = {}
                for line in geo['lines']:
                    key = 'large' if line['large'] else 'small'
                    for yy in range(int(line['y']) + 1, int(line['y'] + line['h']) - 1, 2):
                        for xx in range(int(line['x']) + 1, int(line['x'] + line['w']) - 1, 3):
                            if 0 <= xx < w and 0 <= yy < h:
                                px = rows[yy][xx * bpp:xx * bpp + 3]
                                ratio = contrast(INK, tuple(px))
                                if ratio < worst.get(key, (99,))[0]:
                                    worst[key] = (round(ratio, 2), '#%02x%02x%02x' % tuple(px))
                result[label] = {'small': worst.get('small'), 'large': worst.get('large')}
            print(json.dumps(result), flush=True)
