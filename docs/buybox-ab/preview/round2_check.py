"""/candidate/ (27 Nov, second round): the rings (::before animation per selected card), the Loop
container no longer clipping (overflow), the space between the CTA and the next block for Try once and
60-Day (equal), and in the side panel the image frame (90 % of the inner width), the text without a
heading, the glass footer (backdrop-filter, background) with content under it. Screenshots of the
cards per state and of the panel scrolled. Usage: python3 -I round2_check.py <page-id> <port> <shots> <out>"""
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


def shot(name, width):
    orca('viewport', '--width', str(width), '--height', '900', *(['--mobile'] if width < 750 else []))
    frames(2)
    shutil.copy(orca('screenshot')['result']['path'], SHOTS / f'{name}.png')


STATE = """JSON.stringify((() => {
  const box = document.querySelector('.kc-buybox');
  const once = box.querySelector('.loop-one-time-purchase-option-position');
  const sixty = Array.from(box.querySelectorAll('.loop-subscription-group')).find((g) => g.querySelector('.kc-plan-badge') && g.checkVisibility());
  const ring = (el) => { const b = getComputedStyle(el, '::before'); return b.content === 'none' ? null : b.animationName + ' ' + b.animationDuration; };
  const cta = box.querySelector('.product-form__custom-submit[data-plan-labels]').getBoundingClientRect();
  const next = box.querySelector('.icon-with-text').nextElementSibling;
  const row = box.querySelector('.icon-with-text');
  return { onceRing: ring(once), sixtyRing: ring(sixty), containerOverflow: getComputedStyle(box.querySelector('.loop-subscription-container')).overflow,
    promises: getComputedStyle(row).visibility, ctaToNext: next ? Math.round(next.getBoundingClientRect().top - cta.bottom) : null };
})())"""
PICK = "(() => { const r = Array.from(document.querySelectorAll('.kc-buybox input[name=loop_purchase_option]')).filter((x) => x.closest('.loop-one-time-purchase-option-position, .loop-subscription-group').checkVisibility()); r[%d].click(); return 1; })()"
PANEL = """JSON.stringify((() => {
  const d = document.querySelector('.kc-buybox dialog.kc-plan-dialog'); const body = d.querySelector('.kc-plan-dialog__body');
  const frame = d.querySelector('.kc-plan-dialog__image'); const cs = getComputedStyle(body);
  const inner = body.clientWidth - parseFloat(cs.paddingLeft) - parseFloat(cs.paddingRight);
  const footer = d.querySelector('.kc-plan-dialog__footer'); const fs = getComputedStyle(footer);
  const text = d.querySelector('.kc-plan-dialog__text');
  return { frameShare: frame ? +(frame.getBoundingClientRect().width / inner).toFixed(3) : null,
    frameTopFromBody: frame ? Math.round(frame.getBoundingClientRect().top - body.getBoundingClientRect().top) : null,
    heading: !!d.querySelector('.kc-plan-dialog__text-heading'), text: text && text.innerText.trim(),
    footerBlur: fs.backdropFilter, footerBg: fs.backgroundColor, footerLine: fs.borderTopColor, footerPosition: fs.position,
    contentUnderFooter: body.scrollHeight > body.clientHeight };
})())"""

result = {}
for width in (390, 1440):
    orca('goto', '--url', URL)
    orca('viewport', '--width', str(width), '--height', '900', *(['--mobile'] if width < 750 else []))
    frames(6)
    time.sleep(2.5)
    result[f'{width} Try once'] = ev(STATE)
    ev("(() => { const h = document.querySelector('.kc-buybox .loop-purchase-options-label'); window.scrollTo(0, h.getBoundingClientRect().top + scrollY - 90); return 1; })()")
    shot(f'candidate-en-{width}-day-rings-once', width)
    ev(PICK % 1)
    time.sleep(1.5)
    frames()
    result[f'{width} 60-Day'] = ev(STATE)
    ev("(() => { const g = document.querySelector('.kc-buybox .loop-subscription-group:has(.kc-plan-badge)'); window.scrollTo(0, g.getBoundingClientRect().top + scrollY - 120); return 1; })()")
    shot(f'candidate-en-{width}-day-rings-60day', width)
    for mode in ('day', 'night'):
        ev("(() => { document.body.classList.remove('day-mode', 'night-mode'); document.body.classList.add('%s-mode'); "
           "const open = document.querySelector('.kc-buybox dialog.kc-plan-dialog[open]'); if (open) open.close(); "
           "document.querySelector('.kc-buybox .kc-plan-link__btn').click(); return 1; })()" % mode)
        frames()
        result[f'{width} panel {mode}'] = ev(PANEL)
        shot(f'candidate-en-{width}-{mode}-panel-top', width)
        ev("(() => { const b = document.querySelector('.kc-plan-dialog__body'); b.scrollTop = b.scrollHeight * 0.45; return 1; })()")
        shot(f'candidate-en-{width}-{mode}-panel-scrolled', width)
for key, value in result.items():
    print(key, json.dumps(value, ensure_ascii=False))
OUT.write_text(json.dumps(result, indent=1, ensure_ascii=False))
