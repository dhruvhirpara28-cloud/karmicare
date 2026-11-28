"""Awake / Asleep: live vs the lane's assets (switch default). Buybox text, CTA, script errors, buybox
layout read by kc-plan-select. Usage: python3 -I single_check.py <page-id> <out.json>"""
import json
import subprocess
import sys
import time
from pathlib import Path

PAGE, OUT = sys.argv[1], Path(sys.argv[2])
PROBE = """JSON.stringify({
  buybox: (document.querySelector('.kc-buybox') || {}).innerText?.replace(/\\s+/g, ' ').trim(),
  tryOnceShown: !!document.querySelector('[id^="kc-try-once-container-"]')?.checkVisibility(),
  loopWidget: !!document.querySelector('.loop-subscription-container'),
  errors: window.__errs,
})"""


def orca(*args):
    out = subprocess.run(['orca', *args, '--page', PAGE, '--json'], capture_output=True, text=True, timeout=120)
    return json.loads(out.stdout)


result = {}
for handle in ('awake-morning-toothpaste-2-0', 'asleep-evening-toothpaste-2-0'):
    for variant in ('live', 'off'):
        orca('goto', '--url', f'http://127.0.0.1:9372/{variant}/en/products/{handle}')
        orca('viewport', '--width', '1440', '--height', '900')
        for _ in range(5):
            orca('screenshot')
            time.sleep(1)
        result[f'{variant}/{handle}'] = json.loads(orca('eval', '--expression', PROBE)['result']['result'])
    live, off = result[f'live/{handle}'], result[f'off/{handle}']
    print(handle, 'buybox same:', live['buybox'] == off['buybox'], '| try once shown:', live['tryOnceShown'], off['tryOnceShown'],
          '| loop widget:', live['loopWidget'], off['loopWidget'], '| errors live/off:', live['errors'], off['errors'])
OUT.write_text(json.dumps(result, indent=1, ensure_ascii=False))
