"""Unlisted test (Victor, 27 Nov: "put Awake to unlisted and see if it's available in Loop portal"):
reload an open Loop customer portal page every 90 s and report whether Awake is still offered in its
add-on section ("Goes well with your next order"). Prints product names only, no customer data. Stops when
Awake is gone or after the given minutes. Usage: python3 -I unlisted_portal_watch.py <page-id> <minutes>"""
import json
import subprocess
import sys
import time

PAGE, MINUTES = sys.argv[1], float(sys.argv[2])
NAMES = ['Awake Morning Toothpaste', 'Asleep Evening Toothpaste', 'Morning Toothbrush', 'Evening Toothbrush',
         'Whitening Charcoal Floss']
CHECK = ("(() => { const t = document.body.innerText; const i = t.search(/Goes well/i); const block = i >= 0 ? "
         "t.slice(i, t.indexOf('Subscription details', i)) : ''; return JSON.stringify({ found: i >= 0, names: "
         + json.dumps(NAMES) + ".filter((n) => block.includes(n)) }); })()")


def orca(*args):
    out = subprocess.run(['orca', *args, '--page', PAGE, '--json'], capture_output=True, text=True, timeout=120)
    return json.loads(out.stdout)


start = time.time()
while True:
    orca('eval', '--expression', 'location.reload()')
    time.sleep(12)
    orca('screenshot')
    try:
        state = json.loads(orca('eval', '--expression', CHECK)['result']['result'])
    except (KeyError, json.JSONDecodeError):
        state = {'found': False, 'names': []}
    elapsed = round((time.time() - start) / 60, 1)
    print(time.strftime('%H:%M:%S', time.gmtime()), 'UTC', f'+{elapsed} min', json.dumps(state), flush=True)
    if state['found'] and 'Awake Morning Toothpaste' not in state['names']:
        print('Awake no longer offered', flush=True)
        break
    if elapsed >= MINUTES:
        print('Awake still offered after', MINUTES, 'min', flush=True)
        break
    time.sleep(78)
