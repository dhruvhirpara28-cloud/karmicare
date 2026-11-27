"""/candidate/: the Year bought from the side panel carries the order attribute Loop Loyalty's Care Credit
programs match on ("Subscription Name" = "Year Supply" for 20 %, "60-Day Supply" for 10 %; read in Loop
admin 27 Nov), and Try once at 3 carries none. Records the bodies of /cart/add and /cart/update (nothing
reaches a cart). Usage: python3 -I year_attr_check.py <page-id> <port> <out.json>"""
import json
import subprocess
import sys
import time
from pathlib import Path

PAGE, PORT, OUT = sys.argv[1], sys.argv[2], Path(sys.argv[3])
URL = f'http://127.0.0.1:{PORT}/candidate/en/products/karmicare-biorhythmic-oral-care-system'
RECORD = r"""(() => {
  sessionStorage.removeItem('kcCalls');
  const real = window.fetch;
  const keep = (u, body) => {
    const calls = JSON.parse(sessionStorage.getItem('kcCalls') || '[]');
    calls.push({ url: u.replace(/^.*\/cart\//, '/cart/'), body: body });
    sessionStorage.setItem('kcCalls', JSON.stringify(calls));
  };
  window.fetch = (url, options) => {
    const u = String(url);
    if (u.includes('/cart/add') || u.includes('/cart/update') || u.includes('/cart/change') || u.includes('/cart/clear')) {
      let body = options && options.body;
      try { body = JSON.parse(body); } catch (e) { body = String(body); }
      keep(u, body);
      return Promise.resolve(new Response(JSON.stringify({ items: [], attributes: {} }), { status: 200, headers: { 'Content-Type': 'application/json' } }));
    }
    return real(url, options);
  };
  return 1;
})()"""


def orca(*args):
    out = subprocess.run(['orca', *args, '--page', PAGE, '--json'], capture_output=True, text=True, timeout=120)
    return json.loads(out.stdout)


def ev(expr):
    raw = orca('eval', '--expression', expr)['result']['result']
    return json.loads(raw) if isinstance(raw, str) and raw and raw[0] in '{[' else raw


def load():
    orca('goto', '--url', URL)
    orca('viewport', '--width', '1440', '--height', '900')
    for _ in range(6):
        orca('screenshot')
    time.sleep(2.5)


def calls_after_move():
    time.sleep(3)
    for _ in range(5):
        try:
            return ev("sessionStorage.getItem('kcCalls')")
        except KeyError:
            time.sleep(1)
    return None


result = {}
load()
ev(RECORD)
ev("document.querySelector('.kc-buybox .kc-plan-link__btn').click()")
time.sleep(1)
ev("document.querySelector('.kc-buybox dialog.kc-plan-dialog .kc-plan-dialog__footer button').click()")
result['Year from the side panel'] = calls_after_move()

load()
ev(RECORD)
for _ in range(2):
    ev("document.querySelector('.kc-buybox .kc-once-stepper__button[data-step=\"1\"]').click()")
    time.sleep(0.4)
ev("document.querySelector('.kc-buybox .product-form__custom-submit[data-plan-labels]').click()")
result['Try once at 3'] = calls_after_move()
for key, value in result.items():
    print(key, json.dumps(value, ensure_ascii=False))
OUT.write_text(json.dumps(result, indent=1, ensure_ascii=False))
