"""ON preview: shopper clicks 60-Day, Year, then Try once again (real pointer clicks through orca), probing
after each; also after a variant-free reload whether the card is still selected 6 s later (end CTA,
kc-plan-select guard). Usage: python3 -I interact.py <page-id> <probe.js> <out.json>"""
import json
import subprocess
import sys
import time
from pathlib import Path

PAGE, PROBE, OUT = sys.argv[1], Path(sys.argv[2]).read_text(), Path(sys.argv[3])
URL = 'http://127.0.0.1:9371/on/en/products/karmicare-biorhythmic-oral-care-system'


def orca(*args):
    out = subprocess.run(['orca', *args, '--page', PAGE, '--json'], capture_output=True, text=True, timeout=120)
    return json.loads(out.stdout)


def probe():
    orca('screenshot')
    raw = orca('eval', '--expression', PROBE)['result']['result']
    p = json.loads(raw)
    return {k: p[k] for k in ('cta', 'summary', 'sellingPlan', 'loopGroup', 'sticky', 'linkShown')} | {
        'checked': [c['text'][:22] for c in p['cards'] if c['checked']],
        'onceCardH': p['cards'][0]['h'],
    }


def click(index):
    # A real pointer click on the title of the index-th visible card (0 = first), as a shopper
    rect = orca('eval', '--expression',
                "(() => { const labels = Array.from(document.querySelectorAll('.kc-buybox .loop-one-time-purchase-option-label, .kc-buybox .loop-subscription-group-label')).filter((el) => el.checkVisibility());"
                " const el = labels[%d]; el.scrollIntoView({block: 'center'});"
                " const r = el.getBoundingClientRect(); return JSON.stringify([r.left + Math.min(40, r.width / 2), r.top + r.height / 2]); })()"
                % index)['result']['result']
    orca('screenshot')
    x, y = json.loads(rect)
    # orca mouse lands at twice the given coordinates in this tab (seen: 991,450 -> clientX/Y 1982,900)
    orca('mouse', 'move', '--x', str(round(x / 2)), '--y', str(round(y / 2)))
    orca('mouse', 'down')
    orca('mouse', 'up')
    orca('screenshot')
    time.sleep(1.5)


steps = {}
orca('goto', '--url', URL)
orca('viewport', '--width', '1440', '--height', '900')
time.sleep(6)
steps['load+6s'] = probe()
click(1)
steps['click 60-Day'] = probe()
click(2)
steps['click Year'] = probe()
click(0)
steps['click Try once'] = probe()
click(1)
steps['click 60-Day again'] = probe()
click(0)
steps['click Try once again'] = probe()
OUT.write_text(json.dumps(steps, indent=1, ensure_ascii=False))
print(json.dumps(steps, indent=1, ensure_ascii=False))
