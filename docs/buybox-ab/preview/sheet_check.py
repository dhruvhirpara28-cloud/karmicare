"""/candidate/: the (i) sheet on a phone for every (i) on the Duo page (Victor, 27 Nov: first the Year's side
panel, then all of them), and the Year's side panel as a sheet from the bottom. At 390 (EN, NL), with
60-Day selected so its pill and the receipt rows show: every visible (i) on the page and the two in the
side panel open the sheet (heading = the words next to the (i), text at body size, 24 px extra room at the
bottom), a click outside closes it after sliding down, focus back on the (i); Esc too; the panel slides
down on its close button. At 1440: no sheet, a comparison table's (i) still toggles its popover, the side
panel comes from the right. Screenshots. Usage: python3 -I sheet_check.py <page-id> <port> <shots> <out.json>"""
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path

PAGE, PORT, SHOTS, OUT = sys.argv[1], sys.argv[2], Path(sys.argv[3]), Path(sys.argv[4])
URL = 'http://127.0.0.1:{port}/candidate/{lang}/products/karmicare-biorhythmic-oral-care-system'
TIPS = r"""(() => { window.__tips = Array.from(document.querySelectorAll('.info-tip')).filter((t) => t.querySelector('.info-tip-popover') && t.checkVisibility() && !t.closest('dialog'));
  return JSON.stringify(window.__tips.map((t) => [t.getAttribute('aria-label'), t.getAttribute('role'), t.closest('.kc-pricing-summary') ? 'receipt' : t.closest('.loop-subscription-group') ? 'plan card' : t.closest('[class*="compare"]') ? 'comparison' : 'other'])); })()"""
SHEET = r"""JSON.stringify((() => {
  const s = document.querySelector('dialog.kc-info-sheet');
  if (!s || !s.open) return { open: false };
  const inner = s.querySelector('.kc-info-sheet__inner'), p = s.querySelector('.kc-info-sheet__text p');
  const cs = getComputedStyle(inner);
  return { open: true, inBody: s.parentElement === document.body, animation: cs.animationName, paddingBottom: cs.paddingBottom, paddingSide: cs.paddingLeft,
    heading: (s.querySelector('.kc-info-sheet__heading') || {}).textContent || '', text: s.querySelector('.kc-info-sheet__text').textContent.trim().slice(0, 70),
    textSize: p && getComputedStyle(p).fontSize, pageLocked: getComputedStyle(document.documentElement).overflow === 'hidden',
    popoverShown: Array.from(document.querySelectorAll('.info-tip-popover')).some((x) => getComputedStyle(x).display !== 'none' && getComputedStyle(x).visibility === 'visible' && getComputedStyle(x).opacity !== '0') };
})())"""
STATE = r"""JSON.stringify({ sheetOpen: !!(document.querySelector('dialog.kc-info-sheet') || {}).open, panelOpen: !!(document.querySelector('.kc-buybox dialog.kc-plan-dialog') || {}).open,
  focusOnTip: !!(document.activeElement && document.activeElement.classList.contains('info-tip')), focus: document.activeElement ? (document.activeElement.getAttribute('aria-label') || document.activeElement.className) : '' })"""
OUTSIDE = "document.querySelector('dialog.kc-info-sheet').dispatchEvent(new MouseEvent('click', { bubbles: true }))"
RADIO = "(() => { const r = Array.from(document.querySelectorAll('.kc-buybox input[name=loop_purchase_option]')).filter((x) => x.closest('.loop-one-time-purchase-option-position, .loop-subscription-group').checkVisibility()); r[1].click(); return 1; })()"


def orca(*args):
    out = subprocess.run(['orca', *args, '--page', PAGE, '--json'], capture_output=True, text=True, timeout=120)
    return json.loads(out.stdout)


def ev(expr):
    raw = orca('eval', '--expression', expr)['result']['result']
    return json.loads(raw) if isinstance(raw, str) and raw and raw[0] in '{[' else raw


def view(width):
    orca('viewport', '--width', str(width), '--height', '844', *(['--mobile'] if width < 750 else []))


def shot(name):
    orca('screenshot')
    shutil.copy(orca('screenshot')['result']['path'], SHOTS / name)


def load(lang, width):
    orca('goto', '--url', URL.format(port=PORT, lang=lang))
    view(width)
    for _ in range(6):
        orca('screenshot')
    time.sleep(3)


def open_close(key, tip, shoot=None):
    ev(f"{tip}.scrollIntoView({{ block: 'center' }})")
    ev(f"{tip}.click()")
    result[key] = ev(SHEET)
    time.sleep(0.4)
    if shoot:
        view(390)
        shot(shoot)
    ev(OUTSIDE)
    result[key]['closing'] = ev("document.querySelector('dialog.kc-info-sheet').classList.contains('is-closing')")
    time.sleep(0.6)
    result[key]['after outside click'] = ev(STATE)


result = {}
for lang in ('en', 'nl'):
    load(lang, 390)
    ev(RADIO)
    time.sleep(1.5)
    tips = ev(TIPS)
    result[f'{lang} 390 visible (i)s'] = tips
    for index, (label, _role, where) in enumerate(tips):
        open_close(f'{lang} 390 (i) {index + 1} {where}', f'window.__tips[{index}]',
                   f'candidate-{lang}-390-day-info-sheet-{where.replace(" ", "-")}.png' if index == 0 or where == 'comparison' else None)
    ev(f'window.__tips[0].click()')
    time.sleep(0.4)
    ev("document.querySelector('dialog.kc-info-sheet').dispatchEvent(new Event('cancel', { cancelable: true }))")
    time.sleep(0.6)
    result[f'{lang} 390 Esc'] = ev(STATE)
    # The Year's side panel and its (i)s
    ev("window.scrollTo(0, 0)")
    ev("document.querySelector('.kc-buybox .kc-plan-link__btn') ? document.querySelector('.kc-buybox .kc-plan-link__btn').click() : null")
    time.sleep(0.3)
    result[f'{lang} 390 panel animation'] = ev("getComputedStyle(document.querySelector('.kc-buybox dialog.kc-plan-dialog .kc-plan-dialog__inner')).animationName")
    count = int(ev("String(document.querySelectorAll('.kc-buybox dialog.kc-plan-dialog .info-tip').length)"))
    for index in range(count):
        open_close(f'{lang} 390 panel (i) {index + 1}', f"document.querySelectorAll('.kc-buybox dialog.kc-plan-dialog .info-tip')[{index}]",
                   f'candidate-{lang}-390-day-info-sheet-panel.png' if index == 0 else None)
        result[f'{lang} 390 panel (i) {index + 1}']['panel still open'] = ev("document.querySelector('.kc-buybox dialog.kc-plan-dialog').open")
    ev("document.querySelector('.kc-buybox dialog.kc-plan-dialog .kc-plan-dialog__close').click()")
    result[f'{lang} 390 panel closing'] = ev("document.querySelector('.kc-buybox dialog.kc-plan-dialog').classList.contains('is-closing')")
    time.sleep(0.6)
    result[f'{lang} 390 panel after close'] = ev(STATE)

load('en', 1440)
ev(RADIO)
time.sleep(1.5)
tips = ev(TIPS)
result['en 1440 visible (i)s'] = tips
compare = next((i for i, t in enumerate(tips) if t[2] == 'comparison'), None)
if compare is not None:
    ev(f"window.__tips[{compare}].scrollIntoView({{ block: 'center' }})")
    ev(f"window.__tips[{compare}].click()")
    result['en 1440 comparison (i) click'] = ev(f"JSON.stringify({{ activeTip: window.__tips[{compare}].classList.contains('active-tip'), sheet: !!(document.querySelector('dialog.kc-info-sheet') || {{}}).open }})")
ev("window.__tips[0].click()")
result['en 1440 first (i) click'] = ev("JSON.stringify({ sheet: !!(document.querySelector('dialog.kc-info-sheet') || {}).open })")
ev("window.scrollTo(0, 0)")
ev("document.querySelector('.kc-buybox .kc-plan-link__btn').click()")
time.sleep(0.2)
result['en 1440 panel animation'] = ev("getComputedStyle(document.querySelector('.kc-buybox dialog.kc-plan-dialog .kc-plan-dialog__inner')).animationName")
ev("document.querySelector('.kc-buybox dialog.kc-plan-dialog .kc-plan-dialog__close').click()")
result['en 1440 panel closed at once'] = ev("!document.querySelector('.kc-buybox dialog.kc-plan-dialog').open")
for key, value in result.items():
    print(key, json.dumps(value, ensure_ascii=False))
OUT.write_text(json.dumps(result, indent=1, ensure_ascii=False))
