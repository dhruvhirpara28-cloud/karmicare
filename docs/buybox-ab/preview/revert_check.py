"""Lost click or reverted selection? Fresh load, a log of pointer events and radio changes, then one click
on 60-Day, and the log 4 s later. Usage: python3 -I revert_check.py <page-id> <runs>"""
import json
import subprocess
import sys
import time

PAGE, RUNS = sys.argv[1], int(sys.argv[2])
URL = 'http://127.0.0.1:9371/on/en/products/karmicare-biorhythmic-oral-care-system'
LOG = """(() => { window.__log = []; const t0 = performance.now();
  const note = (s) => window.__log.push(Math.round(performance.now() - t0) + 'ms ' + s);
  document.addEventListener('pointerdown', (e) => note('pointerdown ' + e.isTrusted + ' ' + Math.round(e.clientX) + ',' + Math.round(e.clientY) + ' ' + String(e.target.className).slice(0, 30)), true);
  document.addEventListener('change', (e) => { if (e.target.name === 'loop_purchase_option') note('change ' + e.target.dataset.id + ' trusted=' + e.isTrusted); }, true);
  document.addEventListener('click', (e) => { if (e.target.name === 'loop_purchase_option') note('radio click ' + e.target.dataset.id + ' trusted=' + e.isTrusted); }, true);
  const labels = Array.from(document.querySelectorAll('.kc-buybox .loop-one-time-purchase-option-label, .kc-buybox .loop-subscription-group-label')).filter((el) => el.checkVisibility());
  const el = labels[1]; el.scrollIntoView({block: 'center'}); const r = el.getBoundingClientRect();
  return JSON.stringify([r.left + 40, r.top + r.height / 2]); })()"""
READ = "JSON.stringify({log: window.__log, checked: document.querySelector('.kc-buybox input[name=loop_purchase_option]:checked')?.dataset.id})"


def orca(*args):
    out = subprocess.run(['orca', *args, '--page', PAGE, '--json'], capture_output=True, text=True, timeout=120)
    return json.loads(out.stdout)


for run in range(RUNS):
    orca('goto', '--url', URL)
    orca('viewport', '--width', '1440', '--height', '900')
    time.sleep(6)
    orca('screenshot')
    x, y = json.loads(orca('eval', '--expression', LOG)['result']['result'])
    orca('screenshot')
    orca('mouse', 'move', '--x', str(round(x)), "--y", str(round(y)))
    orca('screenshot')
    orca('mouse', 'down')
    orca('mouse', 'up')
    for _ in range(4):
        orca('screenshot')
        time.sleep(1)
    print(run, orca('eval', '--expression', READ)['result']['result'])
