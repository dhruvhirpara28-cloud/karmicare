"""/popup/ and /panel/: the Year link opens the dialog (content, image, label), screenshot with it open per
width and Day/Night, closing by Esc and by a click on the blur, and the dialog's button: it chooses the
Year in the buybox and presses the buybox CTA, which calls karmiAddToCart with the Year's selling plan in
the form. karmiAddToCart is replaced by a recorder first, so no cart or checkout is touched.
Usage: python3 -I dialog_check.py <page-id> <port> <shots-dir> <out.json>"""
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path

PAGE, PORT, SHOTS, OUT = sys.argv[1], sys.argv[2], Path(sys.argv[3]), Path(sys.argv[4])
URL = 'http://127.0.0.1:{port}/{variant}/en/products/karmicare-biorhythmic-oral-care-system'

INFO = r"""JSON.stringify((() => {
  const d = document.querySelector('.kc-buybox dialog.kc-plan-dialog');
  if (!d) return { open: false };
  const r = d.querySelector('.kc-plan-dialog__inner').getBoundingClientRect();
  const img = d.querySelector('.kc-plan-dialog__image');
  return {
    open: d.open, mode: d.className, title: (d.querySelector('.loop-subscription-group-label') || {}).textContent?.trim(),
    labelledBy: d.getAttribute('aria-labelledby'),
    price: (d.querySelector('.loop-subscription-group-price-amount') || {}).textContent?.trim(),
    chips: Array.from(d.querySelectorAll('.kc-return_care')).filter((c) => c.checkVisibility()).map((c) => c.innerText.replace(/\s+/g, ' ').trim()),
    bullets: Array.from(d.querySelectorAll('.kc-description-list')).filter((c) => c.checkVisibility()).map((c) => c.innerText.replace(/\s+/g, ' ').trim()),
    kitItems: d.querySelectorAll('.block__show-welcome-kit a, .block__show-welcome-kit img').length,
    image: img ? { src: img.src.split('/').pop().split('?')[0], shown: img.checkVisibility() && img.naturalWidth > 0 } : null,
    cta: (d.querySelector('.kc-plan-dialog__cta') || {}).textContent,
    close: d.querySelector('.kc-plan-dialog__close')?.getAttribute('aria-label'),
    focused: document.activeElement && document.activeElement.className,
    box: [Math.round(r.left), Math.round(r.top), Math.round(r.width), Math.round(r.height)],
    blur: getComputedStyle(d, '::backdrop').backdropFilter,
    ids: d.querySelectorAll('[id]').length,
  };
})())"""
OPEN = "document.querySelector('.kc-buybox .kc-plan-link__btn').click()"


def orca(*args):
    out = subprocess.run(['orca', *args, '--page', PAGE, '--json'], capture_output=True, text=True, timeout=120)
    return json.loads(out.stdout)


def evaluate(expr):
    return orca('eval', '--expression', expr)['result']['result']


def frames(n=2):
    for _ in range(n):
        orca('screenshot')


def load(variant, width, mode):
    orca('goto', '--url', URL.format(port=PORT, variant=variant))
    orca('viewport', '--width', str(width), '--height', '900', *(['--mobile'] if width < 750 else []))
    frames(6)
    time.sleep(2.5)
    evaluate("(() => { document.body.classList.remove('day-mode', 'night-mode'); document.body.classList.add('%s-mode'); "
             "const l = document.querySelector('.kc-buybox .kc-plan-link'); l.scrollIntoView({block: 'center'}); return 1; })()" % mode)
    frames()


result = {}
for variant in ('popup', 'panel'):
    for width in (390, 1440):
        for mode in ('day', 'night'):
            load(variant, width, mode)
            evaluate(OPEN)
            time.sleep(1)
            orca('viewport', '--width', str(width), '--height', '900', *(['--mobile'] if width < 750 else []))
            frames(2)
            time.sleep(0.5)
            path = orca('screenshot')['result']['path']
            name = f'{variant}-en-{width}-{mode}-open'
            shutil.copy(path, SHOTS / f'{name}.png')
            result[name] = json.loads(evaluate(INFO))
            print(name, json.dumps(result[name], ensure_ascii=False)[:600])

    # Closing: Esc, then a click on the blur (outside the content box)
    load(variant, 390, 'day')
    evaluate(OPEN)
    frames()
    orca('keypress', '--key', 'Escape')
    frames()
    esc = json.loads(evaluate(INFO))
    evaluate(OPEN)
    frames()
    evaluate("(() => { const d = document.querySelector('.kc-buybox dialog.kc-plan-dialog'); "
             "d.dispatchEvent(new MouseEvent('click', {bubbles: true})); return d.open; })()")
    frames()
    blur = json.loads(evaluate(INFO))
    # The dialog's button: the purchase through the buybox CTA, with the Year's plan in the form
    evaluate(OPEN)
    frames()
    evaluate("(() => { window.__kcAdds = []; window.karmiAddToCart = (form, button, options) => { "
             "window.__kcAdds.push({ plan: (form.querySelector('[name=selling_plan]') || {}).value, "
             "checked: (document.querySelector('.kc-buybox input[name=loop_purchase_option]:checked') || {}).dataset?.id, "
             "button: button && button.id, options: options || null }); return Promise.resolve(); }; "
             "document.querySelector('.kc-buybox .kc-plan-dialog__cta').click(); return 1; })()")
    time.sleep(1.5)
    frames()
    after = json.loads(evaluate("""JSON.stringify({
      dialogOpen: document.querySelector('.kc-buybox dialog.kc-plan-dialog').open,
      yearCard: !document.querySelector('.kc-buybox .kc-plan-as-link'),
      link: !!document.querySelector('.kc-buybox .kc-plan-link'),
      cta: document.querySelector('.kc-buybox .kc-cta-label').textContent.trim(),
      adds: window.__kcAdds })"""))
    result[f'{variant} closing and buying'] = {'after Esc open': esc.get('open'), 'after blur click open': blur.get('open'), 'buy': after}
    print(variant, 'closing and buying', json.dumps(result[f'{variant} closing and buying'], ensure_ascii=False))
OUT.write_text(json.dumps(result, indent=1, ensure_ascii=False))
