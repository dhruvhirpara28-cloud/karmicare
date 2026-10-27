#!/usr/bin/env python3
"""Local preview of the clock preview swing and halo: the live homepage with the branch's clock
script and stylesheet swapped in. Serve this folder with http.server and open /index.html.

Usage: curl -sSL -o docs/homepage/preview-clock/live.html https://www.karmicare.com/
       python3 -I docs/homepage/preview-clock/build.py            (writes index.html)
       curl -sSL -o docs/homepage/preview-clock/live-nl.html https://www.karmicare.com/nl
       python3 -I docs/homepage/preview-clock/build.py nl         (writes index-nl.html)
"""
import re
import shutil
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
LIVE = 'https://www.karmicare.com'
LANG = sys.argv[1] if len(sys.argv) > 1 else 'en'
SUFFIX = '' if LANG == 'en' else '-' + LANG

# Shopify answers 429 to Python's urllib, so the page comes from curl
html = (HERE / f'live{SUFFIX}.html').read_text(encoding='utf-8')
html = html.replace('//www.karmicare.com/', LIVE + '/').replace('https:' + LIVE, LIVE)
html = re.sub(r'(href|src|action)="/(?!/)', r'\1="' + LIVE + '/', html)

# Swap the clock's two assets for the branch versions; a build stamp keeps browsers from reusing
# an older copy of these and of the variant files
STAMP = str(int(time.time()))
for name in ('chronobiology-clock-karmicare.js', 'section-chronobiology-clock-karmicare.css',
             'section-two-formulas-karmicare.css'):
    found = re.findall(r'https://www\.karmicare\.com/cdn/shop/t/\d+/assets/' + re.escape(name) + r'\?v=\d+', html)
    assert found, name
    for url in set(found):
        html = html.replace(url, f'{name}?v={STAMP}')
    shutil.copy(ROOT / 'assets' / name, HERE / name)

BAR = '''
<div id="kc-preview-bar" style="position:fixed;z-index:2147483647;left:50%;bottom:16px;transform:translateX(-50%);
  display:flex;gap:8px;align-items:center;padding:8px 10px 8px 16px;border-radius:999px;background:#191f38;color:#fffbf6;
  font:500 13px/1.2 system-ui,sans-serif;box-shadow:0 6px 20px rgba(0,0,0,.25)">
  <span>Klok E</span>
  <a href="?day#klok" style="color:#fffbf6">Nu</a>
  <a href="?day&amp;fix=up,halo&amp;shift=4&amp;weight=500&amp;cap=14#klok" style="color:#fffbf6;font-weight:700">Voorstel</a>
  <span style="opacity:.5">|</span>
  <a href="#" onclick="const p=new URLSearchParams(location.search);const n=p.has('night');p.delete('day');p.delete('night');p.set(n?'day':'night','');location.search=p.toString().replace(/=(&|$)/g,'$1');return false" style="color:#fffbf6">Day/Night</a>
  <button type="button" onclick="try{sessionStorage.removeItem('kc-clock-explored')}catch(e){};location.hash='klok';location.reload()"
    style="border:0;border-radius:999px;padding:8px 14px;background:#7fb5ff;color:#191f38;font:inherit;cursor:pointer">Opnieuw afspelen</button>
</div>
<style>
  /* The two contrast options for the text in the orb (Victor, 26 Oct), preview only:
     ?fix=up moves the block onto the lighter part of the orb, ?fix=halo adds a thin light rim to
     the letters (no glow around the block). ?shift=N sets how far up, in % of the dial. */
  @media screen and (min-width: 750px) {
    html[data-kc-fix~="up"] .chronobiology-clock .orb-text {
      top: calc(var(--dial-size) * (.5 - var(--kc-shift, .04)));
    }
    html[data-kc-fix~="halo"] .chronobiology-clock .orb-text .time-line,
    html[data-kc-fix~="halo"] .chronobiology-clock .orb-text .state-copy {
      text-shadow: 0 0 1px rgba(255, 251, 246, .95), 0 0 2px rgba(255, 251, 246, .8);
    }
    /* ?cap=14: the caption one size step up (Nunito Bold 700 is already the heaviest loaded) */
    html[data-kc-cap] .chronobiology-clock .orb-text .time-line {
      font-size: var(--kc-cap);
    }
    /* ?weight=500|600: the copy in the orb a touch heavier (Proxima Nova Medium / Semibold) */
    html[data-kc-weight] .chronobiology-clock .orb-text .state-copy {
      font-weight: var(--kc-weight);
    }
  }
</style>
<script>
  (() => {
    const params = new URLSearchParams(location.search);
    // ?at=HH:MM pins the clock's "now" for the preview (new Date() without arguments)
    const at = /^(\d{1,2}):(\d{2})$/.exec(params.get('at') || '');
    if (at) {
      const RealDate = Date;
      window.Date = class extends RealDate {
        constructor(...args) {
          super(...args);
          if (!args.length) this.setHours(Number(at[1]), Number(at[2]), 0, 0);
        }
      };
      window.Date.now = RealDate.now;
    }
    if (params.get('fix')) document.documentElement.dataset.kcFix = params.get('fix').replace(/,/g, ' ');
    if (params.get('shift')) document.documentElement.style.setProperty('--kc-shift', params.get('shift') / 100);
    if (params.get('cap')) {
      document.documentElement.dataset.kcCap = '';
      document.documentElement.style.setProperty('--kc-cap', params.get('cap') + 'px');
    }
    if (params.get('weight')) {
      document.documentElement.dataset.kcWeight = '';
      document.documentElement.style.setProperty('--kc-weight', params.get('weight'));
    }
  })();
  // Rebuild the live clock markup as the branch's section renders it (option E), before the
  // deferred clock script runs: the pill above the stage, the time as a badge in the dial, the
  // caption and copy in .orb-text after the timeline
  (() => {
    const section = document.querySelector('.chronobiology-clock');
    const readout = section && section.querySelector('.readout');
    const stage = section && section.querySelector('.stage');
    if (!readout || !stage) return;
    const time = section.querySelector('.clock-time');
    const caption = section.querySelector('.clock-caption');
    const timeLine = section.querySelector('.time-line');
    const copy = section.querySelector('.state-copy');
    stage.before(readout);
    time.classList.add('knob-time');
    time.setAttribute('aria-hidden', 'true');
    section.querySelector('.dial').append(time);
    timeLine.replaceChildren(caption);
    const orb = document.createElement('div');
    orb.className = 'orb-text';
    orb.append(timeLine, copy);
    section.querySelector('.timeline').after(orb);
  })();
</script>
<script>
  // ?day / ?night: force the theme for the test (the site picks Night by itself in the evening)
  addEventListener('load', () => {
    const params = new URLSearchParams(location.search);
    const mode = params.has('day') ? 'day' : params.has('night') ? 'night' : '';
    const toggle = mode && document.querySelector('.kc_' + mode);
    if (toggle && !document.body.classList.contains(mode + '-mode')) toggle.click();
  });
  // Land a little above the clock, so the swing starts when the dial scrolls into view
  addEventListener('load', () => {
    if (location.hash !== '#klok') return;
    const dial = document.querySelector('.chronobiology-clock .dial');
    if (dial) scrollTo(0, dial.getBoundingClientRect().top + scrollY - innerHeight * 0.9);
    setTimeout(() => scrollTo({ top: dial.getBoundingClientRect().top + scrollY - 80, behavior: 'smooth' }), 600);
  });
</script>
'''
html = html.replace('</body>', BAR + '</body>', 1)
(HERE / f'index{SUFFIX}.html').write_text(html, encoding='utf-8')
print('ok', len(html))
