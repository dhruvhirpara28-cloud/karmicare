"""The Year panel's close button against the professionals' quote panel close button (Victor, 27 Nov: one
close button across the site). /candidate/ EN at 390, Day: computed size, radius, colours, icon and focus
ring of both, and screenshots of both panels. Usage: python3 -I close_check.py <page-id> <port> <shots> <out.json>"""
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path

PAGE, PORT, SHOTS, OUT = sys.argv[1], sys.argv[2], Path(sys.argv[3]), Path(sys.argv[4])
URL = f'http://127.0.0.1:{PORT}/candidate/en/products/karmicare-biorhythmic-oral-care-system'
STYLE = r"""(sel) => { const b = document.querySelector(sel); if (!b) return null; const cs = getComputedStyle(b); const r = b.getBoundingClientRect();
  const svg = b.querySelector('svg'); const s = svg && svg.getBoundingClientRect();
  return { size: [Math.round(r.width), Math.round(r.height)], radius: cs.borderTopLeftRadius, background: cs.backgroundColor, color: cs.color, border: cs.borderTopWidth,
    icon: svg ? [svg.getAttribute('class'), Math.round(s.width), Math.round(s.height)] : null, label: b.getAttribute('aria-label') }; }"""


def orca(*args):
    out = subprocess.run(['orca', *args, '--page', PAGE, '--json'], capture_output=True, text=True, timeout=120)
    return json.loads(out.stdout)


def ev(expr):
    raw = orca('eval', '--expression', expr)['result']['result']
    return json.loads(raw) if isinstance(raw, str) and raw and raw[0] in '{[' else raw


def shot(name):
    orca('viewport', '--width', '390', '--height', '844', '--mobile')
    orca('screenshot')
    shutil.copy(orca('screenshot')['result']['path'], SHOTS / name)


result = {}
orca('goto', '--url', URL)
orca('viewport', '--width', '390', '--height', '844', '--mobile')
for _ in range(6):
    orca('screenshot')
time.sleep(3)
ev("document.querySelector('.kc-buybox .kc-plan-link__btn').click()")
time.sleep(0.6)
result['year panel close'] = ev(f"JSON.stringify(({STYLE})('.kc-buybox dialog.kc-plan-dialog[open] .kc-plan-dialog__close'))")
shot('candidate-en-390-day-year-close.png')
ev("document.querySelector('.kc-buybox dialog.kc-plan-dialog .kc-plan-dialog__close').click()")
time.sleep(0.6)
opened = ev("(() => { const b = Array.from(document.querySelectorAll('.trusted-professionals__card:not([data-marquee-clone]) .trusted-professionals__card-eye')).find((x) => x.checkVisibility()); if (!b) return 'no visible eye'; b.scrollIntoView({ block: 'center' }); b.click(); return 'ok'; })()")
time.sleep(0.8)
result['professionals opener'] = opened
result['professionals panel close'] = ev(f"JSON.stringify(({STYLE})('.trusted-professionals__panel[open] .trusted-professionals__panel-close'))")
shot('candidate-en-390-day-professionals-close.png')
for key, value in result.items():
    print(key, json.dumps(value, ensure_ascii=False))
OUT.write_text(json.dumps(result, indent=1, ensure_ascii=False))
