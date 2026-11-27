"""/candidate/: the Year's side panel as a sheet from the bottom on a phone, and its (i)s as small sheets
(Victor, 27 Nov). At 390 (EN, NL): the panel's animation and place, each (i) opens a sheet with the chip's
words and the tooltip text in body size, a click outside closes it after sliding down, focus back on the
(i), Esc closes it too; the panel slides down on its close button. At 1440: the side panel as before and
an (i) opens no sheet. Screenshots. Usage: python3 -I sheet_check.py <page-id> <port> <shots> <out.json>"""
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path

PAGE, PORT, SHOTS, OUT = sys.argv[1], sys.argv[2], Path(sys.argv[3]), Path(sys.argv[4])
URL = 'http://127.0.0.1:{port}/candidate/{lang}/products/karmicare-biorhythmic-oral-care-system'
PANEL = r"""JSON.stringify((() => {
  const d = document.querySelector('.kc-buybox dialog.kc-plan-dialog');
  const inner = d.querySelector('.kc-plan-dialog__inner'), r = inner.getBoundingClientRect();
  return { open: d.open, animation: getComputedStyle(inner).animationName, rect: [Math.round(r.left), Math.round(r.top), Math.round(r.width), Math.round(r.bottom)],
    viewport: [innerWidth, innerHeight], radius: getComputedStyle(inner).borderTopLeftRadius,
    tips: d.querySelectorAll('.info-tip[role=button]').length };
})())"""
SHEET = r"""JSON.stringify((() => {
  const s = document.querySelector('.kc-buybox dialog.kc-info-sheet');
  if (!s) return { sheet: null };
  const inner = s.querySelector('.kc-info-sheet__inner'), r = inner.getBoundingClientRect();
  const p = s.querySelector('.kc-info-sheet__text p');
  return { open: s.open, animation: getComputedStyle(inner).animationName, rect: [Math.round(r.top), Math.round(r.width), Math.round(r.bottom)],
    heading: s.querySelector('.kc-info-sheet__heading').textContent, text: s.querySelector('.kc-info-sheet__text').textContent.trim().slice(0, 90),
    textSize: p && getComputedStyle(p).fontSize, popoverShown: Array.from(document.querySelectorAll('.kc-plan-dialog .info-tip-popover')).some((x) => x.checkVisibility()) };
})())"""
STATE = r"""JSON.stringify({ sheetOpen: !!(document.querySelector('.kc-info-sheet') || {}).open, panelOpen: document.querySelector('.kc-buybox dialog.kc-plan-dialog').open,
  focus: document.activeElement ? document.activeElement.className + ' ' + (document.activeElement.getAttribute('aria-label') || '') : '' })"""


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


def tip(index):
    return f"document.querySelectorAll('.kc-buybox dialog.kc-plan-dialog .info-tip[role=button]')[{index}]"


result = {}
for lang, width in (('en', 390), ('nl', 390), ('en', 1440)):
    orca('goto', '--url', URL.format(port=PORT, lang=lang))
    view(width)
    for _ in range(6):
        orca('screenshot')
    time.sleep(2.5)
    key = f'{lang} {width}'
    ev("document.querySelector('.kc-buybox .kc-plan-link__btn').click()")
    result[f'{key} panel'] = ev(PANEL)
    time.sleep(0.6)
    view(width)
    shot(f'candidate-{lang}-{width}-day-sheet-panel.png')
    tips = result[f'{key} panel']['tips']
    for index in range(tips):
        ev(f"{tip(index)}.scrollIntoView({{ block: 'center' }})")
        ev(f"{tip(index)}.click()")
        result[f'{key} (i) {index + 1}'] = ev(SHEET)
        time.sleep(0.5)
        if index == 0 and width < 750:
            view(width)
            shot(f'candidate-{lang}-{width}-day-info-sheet.png')
        if width < 750:
            # A click outside the sheet's content is a click on the sheet element itself
            ev("document.querySelector('.kc-info-sheet').dispatchEvent(new MouseEvent('click', { bubbles: true }))")
            result[f'{key} (i) {index + 1} closing'] = ev("document.querySelector('.kc-info-sheet').classList.contains('is-closing')")
            time.sleep(0.6)
            result[f'{key} (i) {index + 1} after outside click'] = ev(STATE)
    if width < 750 and tips:
        ev(f"{tip(0)}.click()")
        time.sleep(0.4)
        ev("document.querySelector('.kc-info-sheet').dispatchEvent(new Event('cancel', { cancelable: true }))")
        time.sleep(0.6)
        result[f'{key} Esc on the (i) sheet'] = ev(STATE)
        ev("document.querySelector('.kc-buybox dialog.kc-plan-dialog .kc-plan-dialog__close').click()")
        result[f'{key} panel closing'] = ev("document.querySelector('.kc-buybox dialog.kc-plan-dialog').classList.contains('is-closing')")
        time.sleep(0.6)
        result[f'{key} panel after close'] = ev(STATE)
for key, value in result.items():
    print(key, json.dumps(value, ensure_ascii=False))
OUT.write_text(json.dumps(result, indent=1, ensure_ascii=False))
