"""/candidate/ (27 Nov round): promises hidden with Try once and back with 60-Day; the closed 60-Day card's
height and the gap above its badge; the selected 60-Day card's silver ring (::before, animation); the
side panel locking the page (html class, overflow, a scroll attempt) and releasing it on close; the
footer line's colour. Screenshots of the selected 60-Day card. Usage:
python3 -I round_check.py <page-id> <port> <shots-dir> <out.json>"""
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path

PAGE, PORT, SHOTS, OUT = sys.argv[1], sys.argv[2], Path(sys.argv[3]), Path(sys.argv[4])
URL = f'http://127.0.0.1:{PORT}/candidate/en/products/karmicare-biorhythmic-oral-care-system'


def orca(*args):
    out = subprocess.run(['orca', *args, '--page', PAGE, '--json'], capture_output=True, text=True, timeout=120)
    return json.loads(out.stdout)


def ev(expr):
    raw = orca('eval', '--expression', expr)['result']['result']
    return json.loads(raw) if isinstance(raw, str) and raw and raw[0] in '{[' else raw


def frames(n=2):
    for _ in range(n):
        orca('screenshot')


CARD = """(() => { const g = Array.from(document.querySelectorAll('.kc-buybox .loop-subscription-group')).find((x) => x.querySelector('.kc-plan-badge') && x.checkVisibility());
  const sub = g.querySelector('.kc-plan-subrow').getBoundingClientRect(); const b = g.querySelector('.kc-plan-badge').getBoundingClientRect();
  const before = getComputedStyle(g, '::before');
  const row = document.querySelector('.kc-buybox .icon-with-text');
  return JSON.stringify({ checked: g.querySelector('input').checked, height: Math.round(g.getBoundingClientRect().height),
    gapSubToBadge: Math.round(b.top - sub.bottom), ring: before.content !== 'none' ? { animation: before.animationName, mask: before.maskComposite || before.webkitMaskComposite } : null,
    border: getComputedStyle(g).borderTopColor, promises: row.checkVisibility() ? Array.from(row.querySelectorAll('.icon-with-text__item')).map((li) => li.innerText.trim()) : 'hidden' }); })()"""

result = {}
for width in (390, 1440):
    orca('goto', '--url', URL)
    orca('viewport', '--width', str(width), '--height', '900', *(['--mobile'] if width < 750 else []))
    frames(6)
    time.sleep(2.5)
    result[f'{width} Try once'] = ev(CARD)
    ev("(() => { const r = Array.from(document.querySelectorAll('.kc-buybox input[name=loop_purchase_option]')).filter((x) => x.closest('.loop-one-time-purchase-option-position, .loop-subscription-group').checkVisibility()); r[1].click(); return 1; })()")
    time.sleep(1.5)
    frames()
    result[f'{width} 60-Day'] = ev(CARD)
    for mode in ('day', 'night'):
        ev("(() => { document.body.classList.remove('day-mode', 'night-mode'); document.body.classList.add('%s-mode'); "
           "const g = document.querySelector('.kc-buybox .loop-subscription-group:has(.kc-plan-badge)'); "
           "window.scrollTo(0, g.getBoundingClientRect().top + scrollY - 120); return 1; })()" % mode)
        orca('viewport', '--width', str(width), '--height', '900', *(['--mobile'] if width < 750 else []))
        frames(2)
        shutil.copy(orca('screenshot')['result']['path'], SHOTS / f'candidate-en-{width}-{mode}-60day-silver.png')
    # The side panel: the page locked while open, free after closing
    ev("(() => { window.scrollTo(0, 600); return 1; })()")
    frames()
    ev("document.querySelector('.kc-buybox .kc-plan-link__btn').click()")
    frames()
    before = ev("window.scrollY")
    ev("(() => { window.scrollBy(0, 400); return 1; })()")
    frames()
    result[f'{width} panel open'] = ev("""JSON.stringify({ htmlClass: document.documentElement.classList.contains('kc-plan-dialog-open'),
      overflow: getComputedStyle(document.documentElement).overflow, scrollBefore: %s, scrollAfterScrollBy: window.scrollY,
      footerLine: getComputedStyle(document.querySelector('.kc-plan-dialog__footer')).borderTopColor,
      bodyOverscroll: getComputedStyle(document.querySelector('.kc-plan-dialog__body')).overscrollBehaviorY })""" % before)
    shutil.copy(orca('screenshot')['result']['path'], SHOTS / f'candidate-en-{width}-day-panel-footer.png')
    orca('keypress', '--key', 'Escape')
    frames()
    result[f'{width} panel closed'] = ev("JSON.stringify({ htmlClass: document.documentElement.classList.contains('kc-plan-dialog-open'), overflow: getComputedStyle(document.documentElement).overflow })")
for key, value in result.items():
    print(key, json.dumps(value, ensure_ascii=False))
OUT.write_text(json.dumps(result, indent=1, ensure_ascii=False))
