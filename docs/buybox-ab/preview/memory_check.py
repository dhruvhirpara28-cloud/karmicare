"""/candidate/: the Try once card keeps its quantity while a plan is selected (Victor, 27 Nov), and the
side panel's title bar stays put over the scrolling content. EN 390: + twice, 60-Day selected (card
still "3 Duos" EUR 201, form field 1, sticky "Try once" buys 1), Try once selected again (field 3, total
EUR 201, buybox CTA buys 3). Adds go to a fetch recorder (nothing reaches a cart). Then the panel at 390
and 1440: bar position before and after scrolling the body, room around the close button. Screenshots.
Usage: python3 -I memory_check.py <page-id> <port> <shots> <out.json>"""
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path

PAGE, PORT, SHOTS, OUT = sys.argv[1], sys.argv[2], Path(sys.argv[3]), Path(sys.argv[4])
URL = f'http://127.0.0.1:{PORT}/candidate/en/products/karmicare-biorhythmic-oral-care-system'
STATE = r"""JSON.stringify((() => {
  const box = document.querySelector('.kc-buybox');
  const card = box.querySelector('.loop-one-time-purchase-option');
  const form = box.querySelector('form[id^="product-form-"]');
  const stepper = card.querySelector('.kc-once-stepper');
  return {
    title: card.querySelector('.loop-one-time-purchase-option-label').textContent.trim(),
    cardPrice: card.querySelector('#loop-price-one-time').textContent.trim(),
    stepper: stepper && stepper.querySelector('.kc-once-stepper__value').textContent,
    stepperShown: !!stepper && stepper.checkVisibility(),
    formQuantity: (form.querySelector('input[name="quantity"].kc-once-quantity') || {}).value,
    total: box.querySelector('.kc-pricing-summary__price').textContent.trim(),
    cta: (box.querySelector('.product-form__custom-submit[data-plan-labels]') || {}).textContent.trim(),
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
  window.addEventListener('beforeunload', (event) => { event.preventDefault(); });
  return 1;
})()"""
RADIO = "(() => { const r = Array.from(document.querySelectorAll('.kc-buybox input[name=loop_purchase_option]')).filter((x) => x.closest('.loop-one-time-purchase-option-position, .loop-subscription-group').checkVisibility()); r[%d].click(); return 1; })()"
PANEL = r"""JSON.stringify((() => {
  const d = document.querySelector('.kc-buybox dialog.kc-plan-dialog');
  const inner = d.querySelector('.kc-plan-dialog__inner').getBoundingClientRect();
  const h = d.querySelector('.kc-plan-dialog__header').getBoundingClientRect();
  const c = d.querySelector('.kc-plan-dialog__close').getBoundingClientRect();
  const img = d.querySelector('.kc-plan-dialog__image').getBoundingClientRect();
  const cs = getComputedStyle(d.querySelector('.kc-plan-dialog__header'));
  return { scrollTop: Math.round(d.querySelector('.kc-plan-dialog__body').scrollTop),
    barTop: Math.round(h.top - inner.top), barHeight: Math.round(h.height),
    closeRoom: [Math.round(c.top - h.top), Math.round(inner.right - c.right), Math.round(h.bottom - c.bottom)],
    imageTopBelowBar: Math.round(img.top - h.bottom), blur: cs.backdropFilter, border: cs.borderBottomWidth + ' ' + cs.borderBottomStyle };
})())"""


def orca(*args):
    out = subprocess.run(['orca', *args, '--page', PAGE, '--json'], capture_output=True, text=True, timeout=120)
    return json.loads(out.stdout)


def ev(expr):
    raw = orca('eval', '--expression', expr)['result']['result']
    return json.loads(raw) if isinstance(raw, str) and raw and raw[0] in '{[' else raw


def frames(n=2):
    for _ in range(n):
        orca('screenshot')


def view(width):
    orca('viewport', '--width', str(width), '--height', '900', *(['--mobile'] if width < 750 else []))


def shot(name):
    shutil.copy(orca('screenshot')['result']['path'], SHOTS / name)


def load(width):
    orca('goto', '--url', URL)
    view(width)
    frames(6)
    time.sleep(2.5)


def at_three_then_60day():
    load(390)
    ev(RECORD)
    for _ in range(2):
        ev("document.querySelector('.kc-buybox .kc-once-stepper__button[data-step=\"1\"]').click()")
        time.sleep(0.4)
    state = ev(STATE)
    ev(RADIO % 1)
    time.sleep(1)
    return state


def adds_after_move():
    # The add moves the page on to /checkout (a 404 here); sessionStorage stays with the origin
    time.sleep(2.5)
    for _ in range(5):
        try:
            return ev("sessionStorage.getItem('kcAdds')")
        except KeyError:
            time.sleep(1)
    return None


result = {}
result['1 Try once at 3'] = at_three_then_60day()
result['2 60-Day selected'] = ev(STATE)
ev("(() => { const h = document.querySelector('.kc-buybox .loop-purchase-options-label'); window.scrollTo(0, h.getBoundingClientRect().top + scrollY - 90); return 1; })()")
view(390)
frames(2)
shot('candidate-en-390-day-once-kept-60day.png')
ev("(() => { const b = Array.from(document.querySelectorAll('[data-kc-plan-choose=\"once\"]')).find((x) => !x.closest('[data-kc-plan-feedback-scope]')); b.click(); return !!b; })()")
result['3 sticky Try once adds'] = adds_after_move()
at_three_then_60day()
ev(RADIO % 0)
time.sleep(1)
result['4 Try once selected again'] = ev(STATE)
frames(2)
shot('candidate-en-390-day-once-kept-again.png')
ev("document.querySelector('.kc-buybox .product-form__custom-submit[data-plan-labels]').click()")
result['5 buybox CTA adds'] = adds_after_move()

for width in (390, 1440):
    load(width)
    ev("document.querySelector('.kc-buybox .kc-plan-link__btn').click()")
    view(width)
    frames(2)
    result[f'panel {width} top'] = ev(PANEL)
    ev("(() => { document.querySelector('.kc-buybox dialog.kc-plan-dialog .kc-plan-dialog__body').scrollTop = 260; return 1; })()")
    view(width)
    frames(2)
    result[f'panel {width} scrolled'] = ev(PANEL)
    shot(f'candidate-en-{width}-day-panel-bar-scrolled.png')
for key, value in result.items():
    print(key, json.dumps(value, ensure_ascii=False))
OUT.write_text(json.dumps(result, indent=1, ensure_ascii=False))
