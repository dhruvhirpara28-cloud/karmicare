"""The branch on a real Shopify render: an unpublished test theme (Victor, 27 Nov: "je mag gerust ook een
dev theme test aanmaken"), opened with ?preview_theme_id in an isolated Orca profile. Per page: the theme
really is the test theme, no "Liquid error", the cards render. Then three real adds to this profile's own
cart, never to checkout: Shopify.routes.root is pointed at a path that does not exist before each buy, so
the theme's redirect lands on a 404 instead of /checkout, and /cart.js is read after it. The cart is
cleared at the end. Usage: python3 -I theme_test.py <page-id> <theme-id> <out.json>"""
import json
import subprocess
import sys
import time
from pathlib import Path

PAGE, THEME, OUT = sys.argv[1], sys.argv[2], Path(sys.argv[3])
BASE = 'https://www.karmicare.com'
HANDLE = 'karmicare-biorhythmic-oral-care-system'
STOP = '/kc-lane-test-no-checkout/'
RENDER = r"""JSON.stringify((() => {
  const box = document.querySelector('.kc-buybox');
  const html = document.documentElement.outerHTML;
  const once = box && box.querySelector('.loop-one-time-purchase-option');
  const sticky = document.getElementById('stickyCta');
  return {
    theme: window.Shopify && Shopify.theme ? [Shopify.theme.id, Shopify.theme.role] : null,
    liquidErrors: (html.match(/Liquid error[^<]{0,120}/g) || []).slice(0, 5),
    onceCard: !!(box && box.querySelector('.kc-once-card')),
    onceChecked: !!(once && once.closest('.loop-one-time-purchase-option-position').querySelector('input:checked')),
    title: once && once.querySelector('.loop-one-time-purchase-option-label').textContent,
    stepper: !!(once && once.querySelector('.kc-once-stepper')),
    yearLink: (box && box.querySelector('.kc-plan-link') || {}).textContent,
    badge: (box && box.querySelector('.kc-plan-badge') || {}).textContent,
    cta: (box && box.querySelector('.product-form__custom-submit[data-plan-labels]') || {}).textContent,
    extras: (document.querySelector('script[id^="kc-plan-extras-"]') || {}).textContent,
    onceMax: (document.querySelector('[id^="kc-try-once-container-"]') || { dataset: {} }).dataset.kcOnceMax,
    stickyTryOnceQuantityAttr: sticky ? sticky.querySelector('[data-sc="try-once"]').hasAttribute('data-kc-once-quantity') : null,
  };
})())"""
CART = "fetch('/cart.js').then(r => r.json()).then(c => JSON.stringify({ attributes: c.attributes, items: c.items.map(i => ({ id: i.variant_id, qty: i.quantity, plan: i.selling_plan_allocation ? i.selling_plan_allocation.selling_plan.id : null, props: i.properties, price: i.final_line_price })), total: c.total_price }))"


def orca(*args):
    out = subprocess.run(['orca', *args, '--page', PAGE, '--json'], capture_output=True, text=True, timeout=120)
    return json.loads(out.stdout)


def ev(expr):
    for _ in range(4):
        try:
            raw = orca('eval', '--expression', expr)['result']['result']
            return json.loads(raw) if isinstance(raw, str) and raw and raw[0] in '{[' else raw
        except (KeyError, json.JSONDecodeError):
            time.sleep(1.5)
    return None


def load(path):
    orca('goto', '--url', f'{BASE}{path}?preview_theme_id={THEME}')
    orca('viewport', '--width', '390', '--height', '900', '--mobile')
    for _ in range(6):
        orca('screenshot')
    time.sleep(4)


def no_checkout():
    ev(f"(() => {{ window.Shopify.routes = window.Shopify.routes || {{}}; window.Shopify.routes.root = '{STOP}'; return 1; }})()")


def cart_after_buy():
    time.sleep(5)
    href = ev('location.href')
    return {'landedOn': href, 'cart': ev(CART)}


result = {}
for lang in ('', '/nl', '/fr'):
    load(f'{lang}/products/{HANDLE}')
    result[f'render {lang or "/en"}'] = ev(RENDER)

ev("fetch('/cart/clear.js', { method: 'POST' }).then(() => 1)")
load(f'/products/{HANDLE}')
for _ in range(2):
    ev("document.querySelector('.kc-buybox .kc-once-stepper__button[data-step=\"1\"]').click()")
    time.sleep(0.5)
no_checkout()
ev("document.querySelector('.kc-buybox .product-form__custom-submit[data-plan-labels]').click()")
result['buy Try once x3'] = cart_after_buy()

load(f'/products/{HANDLE}')
ev("(() => { const r = Array.from(document.querySelectorAll('.kc-buybox input[name=loop_purchase_option]')).filter((x) => x.closest('.loop-one-time-purchase-option-position, .loop-subscription-group').checkVisibility()); r[1].click(); return 1; })()")
time.sleep(1.5)
no_checkout()
ev("document.querySelector('.kc-buybox .product-form__custom-submit[data-plan-labels]').click()")
result['buy 60-Day'] = cart_after_buy()

load(f'/products/{HANDLE}')
ev("document.querySelector('.kc-buybox .kc-plan-link__btn').click()")
time.sleep(1)
no_checkout()
ev("document.querySelector('.kc-buybox dialog.kc-plan-dialog .kc-plan-dialog__footer button').click()")
result['buy Year from the side panel'] = cart_after_buy()

ev("fetch('/cart/clear.js', { method: 'POST' }).then(() => 1)")
result['cart cleared'] = ev(CART)
for key, value in result.items():
    print(key, json.dumps(value, ensure_ascii=False))
OUT.write_text(json.dumps(result, indent=1, ensure_ascii=False))
