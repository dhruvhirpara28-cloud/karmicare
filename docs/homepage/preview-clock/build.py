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

# Swap the clock's two assets for the branch versions
for name in ('chronobiology-clock-karmicare.js', 'section-chronobiology-clock-karmicare.css'):
    found = re.findall(r'https://www\.karmicare\.com/cdn/shop/t/\d+/assets/' + re.escape(name) + r'\?v=\d+', html)
    assert found, name
    for url in set(found):
        html = html.replace(url, name)
    shutil.copy(ROOT / 'assets' / name, HERE / name)

BAR = '''
<div id="kc-preview-bar" style="position:fixed;z-index:2147483647;left:50%;bottom:16px;transform:translateX(-50%);
  display:flex;gap:8px;align-items:center;padding:8px 10px 8px 16px;border-radius:999px;background:#191f38;color:#fffbf6;
  font:500 13px/1.2 system-ui,sans-serif;box-shadow:0 6px 20px rgba(0,0,0,.25)">
  <span>Preview klok (homepage 8ea081b)</span>
  <button type="button" onclick="try{sessionStorage.removeItem('kc-clock-explored')}catch(e){};location.hash='klok';location.reload()"
    style="border:0;border-radius:999px;padding:8px 14px;background:#7fb5ff;color:#191f38;font:inherit;cursor:pointer">Opnieuw afspelen</button>
</div>
<script>
  // The live HTML still has the readout under the dial: put it above the stage, with the pill
  // after the copy, as the branch's section markup does (runs before the deferred clock script)
  (() => {
    const readout = document.querySelector('.chronobiology-clock .readout');
    const stage = document.querySelector('.chronobiology-clock .stage');
    const hint = readout && readout.querySelector('.hint');
    const copy = readout && readout.querySelector('.state-copy');
    if (!readout || !stage || !hint || !copy) return;
    stage.before(readout);
    copy.after(hint);
  })();
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
