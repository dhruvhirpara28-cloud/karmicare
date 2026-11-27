"""/candidate/: the stepper at the right of the EUR 0 pill on every screen (Victor, 27 Nov), and the sticky
bar following the Try once card. Per language and width at quantity 3: stepper and pill on one row,
stepper's right edge at the card's padding, after the pill in the DOM. EN 390: the sticky bar with Try
once selected (title, its form's quantity), with 60-Day selected (its Try once link at 3 x EUR 67 and
the quantity it buys), and a comparison table's Try once (buys 1). Adds go to a fetch recorder
(nothing reaches a cart). Usage: python3 -I sticky_check.py <page-id> <port> <shots> <out.json>"""
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path

PAGE, PORT, SHOTS, OUT = sys.argv[1], sys.argv[2], Path(sys.argv[3]), Path(sys.argv[4])
URL = 'http://127.0.0.1:{port}/candidate/{lang}/products/karmicare-biorhythmic-oral-care-system'
PLACE = r"""JSON.stringify((() => {
  const o = document.querySelector('.kc-buybox .loop-one-time-purchase-option');
  const s = o.querySelector('.kc-once-stepper').getBoundingClientRect(), c = o.querySelector('.kc-once-chips');
  const pill = c.querySelector('.kc-return_care').getBoundingClientRect(), card = o.getBoundingClientRect();
  const label = o.querySelector('.loop-one-time-purchase-option-label').getBoundingClientRect();
  return { title: o.querySelector('.loop-one-time-purchase-option-label').textContent,
    titleOneLine: label.height < 30,
    sameRow: Math.abs((s.top + s.height / 2) - (pill.top + pill.height / 2)) < 2,
    gapPillToStepper: Math.round(s.left - pill.right),
    rightPadding: [Math.round(card.right - s.right), parseInt(getComputedStyle(o).paddingRight, 10)],
    afterPillInDom: c.nextElementSibling === o.querySelector('.kc-once-stepper') };
})())"""
STICKY = r"""JSON.stringify((() => {
  const t = (k) => { const e = document.querySelector('#stickyCta [data-sc="' + k + '"]'); return e ? e.textContent.trim() : null; };
  const link = document.querySelector('#stickyCta [data-sc="try-once"]');
  return { shown: !document.getElementById('stickyCta').inert, title: (t('name') || '') + (t('rest') || ''), cta: t('cta'),
    tryOnce: link.hidden ? '' : t('try-once'), tryOnceQuantity: link.dataset.kcOnceQuantity,
    formQuantity: document.querySelector('#scCtaForm input[name="quantity"]').value };
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
  return 1;
})()"""
RADIO = "(() => { const r = Array.from(document.querySelectorAll('.kc-buybox input[name=loop_purchase_option]')).filter((x) => x.closest('.loop-one-time-purchase-option-position, .loop-subscription-group').checkVisibility()); r[%d].click(); return 1; })()"
PAST_BUYBOX = "(() => { const b = document.querySelector('.kc-buybox .product-form__custom-submit[data-plan-labels]'); window.scrollTo(0, b.getBoundingClientRect().bottom + scrollY + 500); return 1; })()"


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


def load(lang, width):
    orca('goto', '--url', URL.format(port=PORT, lang=lang))
    view(width)
    frames(6)
    time.sleep(2.5)


def plus_twice():
    for _ in range(2):
        ev("document.querySelector('.kc-buybox .kc-once-stepper__button[data-step=\"1\"]').click()")
        time.sleep(0.4)


def adds_after_move():
    time.sleep(2.5)
    for _ in range(5):
        try:
            return ev("sessionStorage.getItem('kcAdds')")
        except KeyError:
            time.sleep(1)
    return None


result = {}
for lang in ('en', 'nl'):
    for width in (390, 1440):
        load(lang, width)
        plus_twice()
        result[f'{lang} {width} stepper'] = ev(PLACE)
        ev("(() => { const h = document.querySelector('.kc-buybox .loop-purchase-options-label'); window.scrollTo(0, h.getBoundingClientRect().top + scrollY - 90); return 1; })()")
        view(width)
        frames(2)
        shot(f'candidate-{lang}-{width}-day-stepper-pill.png')

load('en', 390)
ev(RECORD)
plus_twice()
ev(PAST_BUYBOX)
time.sleep(1)
frames(2)
result['sticky, Try once at 3'] = ev(STICKY)
shot('candidate-en-390-day-sticky-once-3.png')
ev(RADIO % 1)
time.sleep(1)
ev(PAST_BUYBOX)
time.sleep(1)
frames(2)
result['sticky, 60-Day selected'] = ev(STICKY)
shot('candidate-en-390-day-sticky-60day-link.png')
ev("document.querySelector('#stickyCta [data-sc=\"try-once\"]').click()")
result['sticky Try once link adds'] = adds_after_move()

load('nl', 390)
plus_twice()
ev(PAST_BUYBOX)
time.sleep(1)
frames(2)
result['nl sticky, Try once at 3'] = ev(STICKY)
shot('candidate-nl-390-day-sticky-once-3.png')

load('en', 390)
ev(RECORD)
plus_twice()
result['table Try once, Try once at 3, adds'] = ev("(() => { const b = document.querySelector('[data-kc-plan-feedback-scope] [data-kc-plan-choose=\"once\"]'); if (!b) return 'no table button'; b.click(); return 'clicked'; })()")
if result['table Try once, Try once at 3, adds'] == 'clicked':
    result['table Try once, Try once at 3, adds'] = adds_after_move()
for key, value in result.items():
    print(key, json.dumps(value, ensure_ascii=False))
OUT.write_text(json.dumps(result, indent=1, ensure_ascii=False))
