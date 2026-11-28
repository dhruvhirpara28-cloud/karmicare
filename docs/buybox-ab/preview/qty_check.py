"""/candidate/: the Try once quantity end to end. + twice: title, card price, Total today, the buybox
form's quantity, the sticky bar's title and quantity field; then the real buy path (buybox CTA ->
karmiAddToCart -> replaceChoice) with fetch replaced by a recorder for /cart/add.js (nothing reaches a
cart; the recorded body is kept in sessionStorage across the page's move to /checkout). Then the same
with 60-Day selected and the quantity field still at 3: the add must carry the plan's own quantity.
NL and FR titles at quantity 2. Usage: python3 -I qty_check.py <page-id> <port> <shots> <out.json>"""
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path

PAGE, PORT, SHOTS, OUT = sys.argv[1], sys.argv[2], Path(sys.argv[3]), Path(sys.argv[4])
URL = 'http://127.0.0.1:{port}/candidate/{lang}/products/karmicare-biorhythmic-oral-care-system'

STATE = r"""JSON.stringify((() => {
  const box = document.querySelector('.kc-buybox');
  const card = box.querySelector('.loop-one-time-purchase-option');
  const form = box.querySelector('form[id^="product-form-"]');
  const sc = document.getElementById('scCtaForm');
  const summary = box.querySelector('.kc-pricing-summary[id^="kc-pricing-summary-"]');
  return {
    title: card.querySelector('.loop-one-time-purchase-option-label').textContent.trim(),
    cardPrice: card.querySelector('#loop-price-one-time').textContent.trim(),
    stepper: card.querySelector('.kc-once-stepper__value') && card.querySelector('.kc-once-stepper__value').textContent,
    stepperShown: !!card.querySelector('.kc-once-stepper') && card.querySelector('.kc-once-stepper').checkVisibility(),
    total: summary.querySelector('.kc-pricing-summary__price').textContent.trim(),
    perBrushing: summary.querySelector('.kc-pricing-summary__per-brushing').textContent.trim(),
    formQuantity: (form.querySelector('input[name="quantity"]') || {}).value,
    stickyTitle: Array.from(document.querySelectorAll('[data-sc-field="name"], [data-sc-field="rest"]')).map((e) => e.textContent).join(''),
    stickyQuantity: sc && sc.querySelector('input[name="quantity"]').value,
  };
})())"""
RECORD = r"""(() => {
  sessionStorage.removeItem('kcAdds');
  const real = window.fetch;
  window.fetch = (url, options) => {
    const u = String(url);
    if (u.includes('/cart/add')) {
      const adds = JSON.parse(sessionStorage.getItem('kcAdds') || '[]');
      adds.push(JSON.parse(options.body));
      sessionStorage.setItem('kcAdds', JSON.stringify(adds));
      return Promise.resolve(new Response(JSON.stringify({ items: [] }), { status: 200, headers: { 'Content-Type': 'application/json' } }));
    }
    if (u.includes('/cart/update') || u.includes('/cart/change') || u.includes('/cart/clear')) {
      return Promise.resolve(new Response(JSON.stringify({ items: [], attributes: {} }), { status: 200, headers: { 'Content-Type': 'application/json' } }));
    }
    return real(url, options);
  };
  document.querySelector('.kc-buybox .product-form__custom-submit[data-plan-labels]').click();
  return 1;
})()"""


def orca(*args):
    out = subprocess.run(['orca', *args, '--page', PAGE, '--json'], capture_output=True, text=True, timeout=120)
    return json.loads(out.stdout)


def ev(expr):
    raw = orca('eval', '--expression', expr)['result']['result']
    return json.loads(raw) if isinstance(raw, str) and raw and raw[0] in '{[' else raw


def frames(n=2):
    for _ in range(n):
        orca('screenshot')


def load(lang, width=390):
    orca('goto', '--url', URL.format(port=PORT, lang=lang))
    orca('viewport', '--width', str(width), '--height', '900', *(['--mobile'] if width < 750 else []))
    frames(6)
    time.sleep(2.5)


def plus(times):
    for _ in range(times):
        ev("document.querySelector('.kc-buybox .kc-once-stepper__button[data-step=\"1\"]').click()")
        time.sleep(0.4)
    time.sleep(0.6)
    frames()


result = {}
load('en')
result['en start'] = ev(STATE)
plus(2)
result['en quantity 3'] = ev(STATE)
ev("(() => { const h = document.querySelector('.kc-buybox .loop-purchase-options-label'); window.scrollTo(0, h.getBoundingClientRect().top + scrollY - 90); return 1; })()")
orca('viewport', '--width', '390', '--height', '900', '--mobile')
frames(2)
shutil.copy(orca('screenshot')['result']['path'], SHOTS / 'candidate-en-390-day-once-quantity-3.png')
ev(RECORD)
time.sleep(3)
frames()
result['en buy Try once x3'] = ev("sessionStorage.getItem('kcAdds')")

load('en')
plus(2)
ev("(() => { const r = Array.from(document.querySelectorAll('.kc-buybox input[name=loop_purchase_option]')).filter((x) => x.closest('.loop-one-time-purchase-option-position, .loop-subscription-group').checkVisibility()); r[1].click(); return 1; })()")
time.sleep(1.5)
frames()
result['en 60-Day with field at 3'] = ev(STATE)
ev(RECORD)
time.sleep(3)
frames()
result['en buy 60-Day'] = ev("sessionStorage.getItem('kcAdds')")

for lang in ('nl', 'fr'):
    load(lang)
    plus(1)
    result[f'{lang} quantity 2'] = ev(STATE)

for key, value in result.items():
    print(key, json.dumps(value, ensure_ascii=False))
OUT.write_text(json.dumps(result, indent=1, ensure_ascii=False))
