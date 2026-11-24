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
BASE = 'http://127.0.0.1:9376'
HANDLE = 'karmicare-biorhythmic-oral-care-system'

SHOTS_LIST = []
for switch in ('live', 'off', 'on'):
    for width in (390, 1440):
        for mode in ('day', 'night'):
            SHOTS_LIST.append((f'{switch}-en-{width}-{mode}', switch, 'en', width, mode))
for lang in ('nl', 'fr'):
    SHOTS_LIST.append((f'on-{lang}-390-day', 'on', lang, 390, 'day'))
# "-top": scrolled to the product title instead of the plans header
for switch in ('off', 'on'):
    for width in (390, 1440):
        for mode in ('day', 'night'):
            SHOTS_LIST.append((f'{switch}-en-{width}-{mode}-top', switch, 'en', width, mode))
for lang in ('nl', 'fr'):
    SHOTS_LIST.append((f'on-{lang}-390-day-top', 'on', lang, 390, 'day'))
# /copy/ (PLAN.md 4b proposals); "-60day" / "-year": that card selected, scrolled to it
for width in (390, 1440):
    for mode in ('day', 'night'):
        for suffix in ('', '-60day', '-year'):
            SHOTS_LIST.append((f'copy-en-{width}-{mode}{suffix}', 'copy', 'en', width, mode))
            if suffix:
                SHOTS_LIST.append((f'on-en-{width}-{mode}{suffix}', 'on', 'en', width, mode))
# /year/ (Year as a link under the cards): plans header and lower buybox, EN Day/Night, NL/FR
for width in (390, 1440):
    for mode in ('day', 'night'):
        SHOTS_LIST.append((f'year-en-{width}-{mode}', 'year', 'en', width, mode))
        SHOTS_LIST.append((f'year-en-{width}-{mode}-once-buy', 'year', 'en', width, mode))
for lang in ('nl', 'fr'):
    SHOTS_LIST.append((f'year-{lang}-390-day', 'year', lang, 390, 'day'))
# /full/ (Year as a link + copy proposals): plans header, lower buybox per state (60-Day as a card)
for width in (390, 1440):
    for mode in ('day', 'night'):
        SHOTS_LIST.append((f'full-en-{width}-{mode}', 'full', 'en', width, mode))
        SHOTS_LIST.append((f'full-en-{width}-{mode}-once-buy', 'full', 'en', width, mode))
        SHOTS_LIST.append((f'full-en-{width}-{mode}-60day-buy', 'full', 'en', width, mode))
# /chips/ (/full/ with chips on the selected card only): plans header per state
for width in (390, 1440):
    for mode in ('day', 'night'):
        for state in ('', '-60day'):
            SHOTS_LIST.append((f'chips-en-{width}-{mode}{state}', 'chips', 'en', width, mode))
# "-buy": the lower buybox (end of the cards, receipt, CTA, trust row) per state, before (on) and after (copy)
for switch in ('on', 'copy'):
    for width in (390, 1440):
        for mode in ('day', 'night'):
            for state in ('-once', '-60day', '-year'):
                SHOTS_LIST.append((f'{switch}-en-{width}-{mode}{state}-buy', switch, 'en', width, mode))


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
    pick = 1 if '-60day' in name else 2 if '-year' in name else 0
    if pick:
        evaluate(
            "(() => { const radios = Array.from(document.querySelectorAll('.kc-buybox input[name=loop_purchase_option]'))"
            ".filter((r) => r.closest('.loop-one-time-purchase-option-position, .loop-subscription-group').checkVisibility());"
            " radios[%d].click(); return radios[%d].checked; })()" % (pick, pick)
        )
        shot()
        time.sleep(1.5)
    evaluate(
        "(() => { document.body.classList.remove('day-mode', 'night-mode'); document.body.classList.add('%s-mode');"
        " const el = %s;"
        " window.scrollTo(0, el.getBoundingClientRect().top + scrollY - %d); return scrollY; })()" % (
            mode,
            "document.querySelector('.kc-buybox .icon-with-text')" if name.endswith('-buy')
            else "document.querySelector('.kc-buybox .product__title')" if name.endswith('-top')
            else "document.querySelector('.kc-buybox input[name=loop_purchase_option]:checked').closest('.loop-subscription-group')" if pick
            else "document.querySelector('.kc-buybox .loop-purchase-options-label') || document.querySelector('#loop-selling-plan-fieldset')",
            # "-buy": the trust row near the bottom of the 900 px frame, the receipt and CTA above it
            760 if name.endswith('-buy') else 90 if width < 750 else 140,
        )
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
