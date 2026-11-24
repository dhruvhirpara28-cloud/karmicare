"""/year/ variant: on load (Try once selected, Year folded into the link), after the link's click (Year card
open and selected) and after choosing Try once again (Year card stays open). Also the buybox height from
the plans header to the trust row, against /on/. Usage: python3 -I year_check.py <page-id> <port> [lang]"""
import json
import subprocess
import sys
import time

PAGE, PORT = sys.argv[1], sys.argv[2]
LANG = sys.argv[3] if len(sys.argv) > 3 else 'en'
STATE = """JSON.stringify((() => {
  const box = document.querySelector('.kc-buybox');
  const cards = Array.from(box.querySelectorAll('.loop-one-time-purchase-option-position, .loop-subscription-group'))
    .filter((c) => c.checkVisibility())
    .map((c) => (c.querySelector('.loop-one-time-purchase-option-label, .loop-subscription-group-label').textContent.trim()
      + (c.querySelector('input[type=radio]').checked ? ' [x]' : '')));
  const link = box.querySelector('.kc-plan-link');
  const head = box.querySelector('.loop-purchase-options-label').getBoundingClientRect();
  const trust = box.querySelector('.icon-with-text').getBoundingClientRect();
  return {
    cards,
    link: link && link.checkVisibility() ? link.innerText.replace(/\\s+/g, ' ').trim() : null,
    cta: box.querySelector('.kc-cta-label').textContent.trim(),
    summary: box.querySelector('.kc-pricing-summary[id^="kc-pricing-summary-"]').innerText.replace(/\\s+/g, ' ').trim(),
    height: Math.round(trust.bottom - head.top),
  };
})())"""


def orca(*args):
    out = subprocess.run(['orca', *args, '--page', PAGE, '--json'], capture_output=True, text=True, timeout=120)
    return json.loads(out.stdout)


def state():
    orca('screenshot')
    return json.loads(orca('eval', '--expression', STATE)['result']['result'])


def load(variant, width):
    orca('goto', '--url', f'http://127.0.0.1:{PORT}/{variant}/{LANG}/products/karmicare-biorhythmic-oral-care-system')
    orca('viewport', '--width', str(width), '--height', '900', *(['--mobile'] if width < 750 else []))
    for _ in range(6):
        orca('screenshot')
    time.sleep(2.5)


result = {}
for width in (390, 1440):
    load('on', width)
    result[f'on {width}'] = state()
    load('year', width)
    result[f'year {width} load'] = state()
    if width == 390:
        orca('eval', '--expression', "document.querySelector('.kc-buybox .kc-plan-link__btn').click()")
        time.sleep(1.5)
        result['year 390 after link'] = state()
        orca('eval', '--expression', "document.querySelector('.kc-buybox .loop-one-time-purchase-option-radio').click()")
        time.sleep(1.5)
        result['year 390 back to Try once'] = state()
for key, value in result.items():
    print(key, json.dumps(value, ensure_ascii=False))
