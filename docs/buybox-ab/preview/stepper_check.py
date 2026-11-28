"""/candidate/: where the Try once stepper sits (Victor, 27 Nov: between title and price, or right next to
the pill, never a row of its own), per language and width at quantity 3; and the side panel's top
(title instead of the badge, the image under it). Screenshots. Usage:
python3 -I stepper_check.py <page-id> <port> <shots> <out.json>"""
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
  const rect = (el) => el.getBoundingClientRect();
  const s = rect(o.querySelector('.kc-once-stepper')), p = rect(o.querySelector('.loop-one-time-purchase-option-price-container'));
  const c = rect(o.querySelector('.kc-once-chips')), card = rect(o);
  const range = document.createRange(); range.selectNodeContents(o.querySelector('.loop-one-time-purchase-option-label'));
  const titleRects = Array.from(range.getClientRects()).filter((r) => r.height > 0);
  const t = range.getBoundingClientRect();
  const lineTops = new Set(titleRects.map((r) => Math.round(r.top)));
  return { title: o.querySelector('.loop-one-time-purchase-option-label').textContent, titleLines: lineTops.size,
    stepper: [Math.round(s.left - card.left), Math.round(s.top - card.top), Math.round(s.width), Math.round(s.height)],
    onTitleLine: Math.abs((s.top + s.height / 2) - (t.top + Math.min(t.height, 28) / 2)) < 6,
    gapToTitle: Math.round(s.left - t.right), gapToPrice: Math.round(p.left - s.right),
    onPillRow: Math.abs((s.top + s.height / 2) - (c.top + c.height / 2)) < c.height / 2,
    rightEdgeToCard: Math.round(card.right - s.right) };
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


result = {}
for lang in ('en', 'nl'):
    for width in (390, 1440):
        orca('goto', '--url', URL.format(port=PORT, lang=lang))
        view(width)
        frames(6)
        time.sleep(2.5)
        for _ in range(2):
            ev("document.querySelector('.kc-buybox .kc-once-stepper__button[data-step=\"1\"]').click()")
            time.sleep(0.4)
        frames()
        result[f'{lang} {width}'] = ev(PLACE)
        ev("(() => { const h = document.querySelector('.kc-buybox .loop-purchase-options-label'); window.scrollTo(0, h.getBoundingClientRect().top + scrollY - 90); return 1; })()")
        view(width)
        frames(2)
        shutil.copy(orca('screenshot')['result']['path'], SHOTS / f'candidate-{lang}-{width}-day-stepper.png')
        if lang == 'en':
            ev("document.querySelector('.kc-buybox .kc-plan-link__btn').click()")
            view(width)
            frames(2)
            result[f'{lang} {width} panel'] = ev("""JSON.stringify((() => { const d = document.querySelector('.kc-buybox dialog.kc-plan-dialog');
              const h = d.querySelector('.kc-plan-dialog__header'); const img = d.querySelector('.kc-plan-dialog__image');
              return { title: h && h.querySelector('.kc-plan-dialog__header-title').textContent, goldStrip: !!d.querySelector('.kc-plan-dialog__header.kc-testimonial-button'),
                imageTop: Math.round(img.getBoundingClientRect().top), closeFocused: document.activeElement === d.querySelector('.kc-plan-dialog__close'),
                closeSize: [Math.round(d.querySelector('.kc-plan-dialog__close').getBoundingClientRect().width), Math.round(d.querySelector('.kc-plan-dialog__close').getBoundingClientRect().height)] }; })())""")
            shutil.copy(orca('screenshot')['result']['path'], SHOTS / f'candidate-en-{width}-day-panel-title.png')
for key, value in result.items():
    print(key, json.dumps(value, ensure_ascii=False))
OUT.write_text(json.dumps(result, indent=1, ensure_ascii=False))
