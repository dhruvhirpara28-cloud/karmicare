"""Astra R1 fixes, /candidate/ at 390: (P2) the Try once stepper keeps working after Loop's "one-time at
bottom" path copies the option's markup, twice; (P2) Loop's own add button override passes the Try once
quantity; (P1) the (i) sheet script loads only with the theme setting (the preview always injects it, so
this checks the gate in layout/theme.liquid by source). Purchases go to an in-page recorder: nothing reaches
a cart. Usage: python3 -I astra_r1_check.py <page-id> <port> <out.json>"""
import json
import re
import subprocess
import sys
import time
from pathlib import Path

PAGE, PORT, OUT = sys.argv[1], sys.argv[2], Path(sys.argv[3])
URL = f'http://127.0.0.1:{PORT}/candidate/en/products/karmicare-biorhythmic-oral-care-system'
PID = '15977093923197'
STATE = r"""JSON.stringify((() => {
  const box = document.querySelector('.kc-buybox');
  const steppers = box.querySelectorAll('.kc-once-stepper');
  const input = box.querySelector('input[name="quantity"].kc-once-quantity');
  const o = box.querySelector('.loop-one-time-purchase-option');
  return { steppers: steppers.length, value: steppers[0] && steppers[0].querySelector('.kc-once-stepper__value').textContent,
    chosen: input && input.dataset.kcChosen, field: input && input.value,
    title: o && o.querySelector('.loop-one-time-purchase-option-label').textContent,
    onTop: !!document.querySelector('#loop-one-time-purchase-option-at-top .kc-once-stepper') };
})())"""
PLUS = "document.querySelector('.kc-buybox .kc-once-stepper__button[data-step=\"1\"]').click()"
BOTTOM = ("(() => { window.loopPropsUI.displayOneTimePurchaseOptionAtBottom = true; applyLoopSettings({ productId: '%s' }); "
          "updatePriceInParentElementsLoop({ productId: '%s' }); return 1; })()" % (PID, PID))


def orca(*args):
    out = subprocess.run(['orca', *args, '--page', PAGE, '--json'], capture_output=True, text=True, timeout=120)
    return json.loads(out.stdout)


def ev(expr):
    raw = orca('eval', '--expression', expr)['result']['result']
    return json.loads(raw) if isinstance(raw, str) and raw and raw[0] in '{[' else raw


result = {}
orca('goto', '--url', URL)
orca('viewport', '--width', '390', '--height', '844', '--mobile')
for _ in range(6):
    orca('screenshot')
time.sleep(3)
ev(PLUS)
time.sleep(0.5)
result['at 2'] = ev(STATE)
for round_ in (1, 2):
    ev(BOTTOM)
    time.sleep(1)
    result[f'after one-time-at-bottom re-render {round_}'] = ev(STATE)
    ev(PLUS)
    time.sleep(0.5)
    result[f'after + ({round_})'] = ev(STATE)
# Loop's own add button override: bind it on the buybox form, record what it hands to loopHandleAddToCart
result['override quantity'] = ev(
    "(() => { window.__kcAdd = null; const real = window.loopHandleAddToCart; window.loopHandleAddToCart = (e, p, q) => { e.preventDefault(); window.__kcAdd = { product: p, quantity: q }; };"
    " overrideAddToCartButtonLoop('" + PID + "'); const form = document.querySelector('.kc-buybox [data-loop-product-id=\"" + PID + "\"]');"
    " const btn = form && (form.querySelector('button[type=submit]') || form.querySelector('button')); if (!btn) return JSON.stringify({ noButton: true });"
    " btn.click(); window.loopHandleAddToCart = real; return JSON.stringify(Object.assign({ field: (document.querySelector('.kc-buybox input.kc-once-quantity') || {}).value }, window.__kcAdd)); })()")
# Astra R2 P2: another product's bundle form (quantity 2) never takes the Duo's Try once quantity, with
# the buybox's installment form first (as served) and with its purchase form first (installment id renamed)
result['other product, both form orders'] = ev(
    "(() => { const res = {}; const real = window.loopHandleAddToCart; const other = document.createElement('form');"
    " other.setAttribute('data-loop-product-id', 'kc-r2-other'); other.innerHTML = '<input class=\"quantity__input\" value=\"2\"><button type=\"submit\">x</button>';"
    " document.body.appendChild(other);"
    " const run = (label) => { window.__kcAdd = null; window.loopHandleAddToCart = (e, p, q) => { e.preventDefault(); window.__kcAdd = q; };"
    " overrideAddToCartButtonLoop('kc-r2-other'); other.querySelector('button').click(); res[label] = window.__kcAdd; };"
    " run('installment form first'); const inst = Array.from(document.querySelectorAll('.kc-buybox form[id^=\"product-form-\"]')).find((f) => !f.querySelector('.kc-once-quantity'));"
    " const oldId = inst && inst.id; if (inst) inst.id = 'kc-r2-renamed'; res.helperFieldWithPurchaseFirst = (kcOnceQuantityInput('kc-r2-other', false) || {}).value || null;"
    " run('purchase form first'); if (inst) inst.id = oldId; window.loopHandleAddToCart = real; other.remove(); return JSON.stringify(res); })()")
layout = Path(__file__).resolve().parents[3] / 'layout' / 'theme.liquid'
text = layout.read_text()
gate = re.search(r"\{%-\s*if settings\.kc_info_sheets\s*-%\}(.*?)\{%-\s*endif\s*-%\}", text, flags=re.S)
result['layout gate around both files'] = bool(gate and 'kc-info-sheet.css' in gate.group(1) and 'kc-info-sheet.js' in gate.group(1))
for key, value in result.items():
    print(key, json.dumps(value, ensure_ascii=False))
OUT.write_text(json.dumps(result, indent=1, ensure_ascii=False))
