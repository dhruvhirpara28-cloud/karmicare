"""Buybox-ab screenshots through the Orca browser tab: per shot goto, viewport, wait for the Loop widget
to settle, set Day/Night (body class, as assets/day-night-mode.js), scroll the plans header under the
site header, two screenshots (the tab paints per screenshot), copy the second to the shots folder and
keep the page probe next to it. Usage: python3 -I shoot.py <page-id> <shots-dir> <probe.js> [name ...]"""
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path

PAGE, SHOTS, PROBE = sys.argv[1], Path(sys.argv[2]), Path(sys.argv[3]).read_text()
ONLY = set(sys.argv[4:])
BASE = 'http://127.0.0.1:9372'
HANDLE = 'karmicare-biorhythmic-oral-care-system'

SHOTS_LIST = []
for switch in ('live', 'off', 'on'):
    for width in (390, 1440):
        for mode in ('day', 'night'):
            SHOTS_LIST.append((f'{switch}-en-{width}-{mode}', switch, 'en', width, mode))
for lang in ('nl', 'fr'):
    SHOTS_LIST.append((f'on-{lang}-390-day', 'on', lang, 390, 'day'))


def orca(*args):
    out = subprocess.run(['orca', *args, '--page', PAGE, '--json'], capture_output=True, text=True, timeout=120)
    try:
        return json.loads(out.stdout)
    except json.JSONDecodeError:
        raise RuntimeError(out.stdout + out.stderr)


def evaluate(expr):
    return orca('eval', '--expression', expr).get('result', {}).get('result')


def shot():
    return orca('screenshot').get('result', {}).get('path')


results = {}
for name, switch, lang, width, mode in SHOTS_LIST:
    if ONLY and name not in ONLY:
        continue
    url = f'{BASE}/{switch}/{lang}/products/{HANDLE}'
    orca('goto', '--url', url)
    viewport = ['viewport', '--width', str(width), '--height', '900']
    if width < 750:
        viewport.append('--mobile')
    orca(*viewport)
    probe = {}
    for _ in range(20):
        shot()
        raw = evaluate(PROBE)
        probe = json.loads(raw) if isinstance(raw, str) else {}
        if probe.get('loopGroup') and probe.get('cards'):
            break
        time.sleep(1)
    # kc-plan-select settles 800 ms after Loop; give the end CTA and the guard their time too
    time.sleep(2.5)
    evaluate(
        "(() => { document.body.classList.remove('day-mode', 'night-mode'); document.body.classList.add('%s-mode');"
        " const el = document.querySelector('.kc-buybox .loop-purchase-options-label') || document.querySelector('#loop-selling-plan-fieldset');"
        " window.scrollTo(0, el.getBoundingClientRect().top + scrollY - %d); return scrollY; })()" % (mode, 90 if width < 750 else 140)
    )
    orca(*viewport)
    shot()
    time.sleep(0.5)
    path = shot()
    raw = evaluate(PROBE)
    probe = json.loads(raw) if isinstance(raw, str) else probe
    target = SHOTS / f'{name}.png'
    shutil.copy(path, target)
    results[name] = probe
    first = probe.get('cards', [{}])[0]
    print(name, probe.get('w'), probe.get('mode'), probe.get('layout'), 'cta=', probe.get('cta'), 'first=', first.get('text', '')[:40], 'checked=', [c['checked'] for c in probe.get('cards', [])])

probe_file = SHOTS / 'probes.json'
old = json.loads(probe_file.read_text()) if probe_file.exists() else {}
old.update(results)
probe_file.write_text(json.dumps(old, indent=1, ensure_ascii=False))
