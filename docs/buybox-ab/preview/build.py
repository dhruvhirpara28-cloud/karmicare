"""Buybox-ab localhost preview builder.

Takes the live Duo PDP HTML (EN/NL/FR, fetched cookie-less) and writes, per language, a switch OFF
and a switch ON page: the lane's assets (loop-widget.js, kc-plan-select.js, kc-buybox.css) replace
the live ones, and the Liquid output of the lane's main-product.liquid / kc-plan-config.liquid
changes is emulated (data-kc-once-* on the buybox Try once container, defaultToSubscription false
for the buybox when ON). Usage: python3 -I build.py <live-html-dir> <worktree> <serve-dir>
"""
import html
import json
import re
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import copy_proposals  # noqa: E402

LIVE, WORKTREE, SERVE = (Path(a) for a in sys.argv[1:4])
PID = '15977093923197'
HANDLE = 'karmicare-biorhythmic-oral-care-system'
ASSETS = ['loop-widget.js', 'kc-plan-select.js', 'kc-buybox.css']
PAGES = {'en': 'duo.html', 'nl': 'duo-nl.html', 'fr': 'duo-fr.html'}
LOCALES = {'en': 'en.default.json', 'nl': 'nl.json', 'fr': 'fr.json'}


def locale(lang):
    text = (WORKTREE / 'locales' / LOCALES[lang]).read_text()
    text = re.sub(r'^\s*/\*.*?\*/', '', text, flags=re.S)
    return json.loads(text)['kc']['sticky_cart']


def build_live(lang):
    # The live page untouched (only its relative URLs made absolute): the "before" for the OFF check
    page = (LIVE / PAGES[lang]).read_text()
    page = page.replace('"//www.karmicare.com/', '"https://www.karmicare.com/')
    page = page.replace(' //www.karmicare.com/', ' https://www.karmicare.com/')
    page = page.replace(',//www.karmicare.com/', ',https://www.karmicare.com/')
    page = re.sub(r'(href|src|action)="/(?!/)', r'\1="https://www.karmicare.com/', page)
    out = SERVE / 'live' / lang / 'products' / f'{HANDLE}.html'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page)
    return out


def build(lang, layout):
    page = (LIVE / PAGES[lang]).read_text()
    sticky = locale(lang)
    note = re.search(r'class="ft-note">([^<]*)', page).group(1).strip()
    attrs = {
        'data-kc-once-layout': layout,
        'data-kc-once-title': sticky['title_once_html'],
        'data-kc-once-delivery': sticky['delivery_once_html'],
        'data-kc-once-guarantee': sticky['guarantee_once_html'],
        'data-kc-once-note': html.unescape(note),
        'data-kc-once-cta': sticky['cta_once_html'],
    }
    attr_text = ''.join(f'\n                    {k}="{html.escape(v, quote=True)}"' for k, v in attrs.items())
    anchor = f'id="kc-try-once-container-{PID}"\n                    class="tertiary-try-once-link figma-tryonce v9bb"\n                    data-active-plan="once"'
    assert page.count(anchor) == 1, 'try once container anchor'
    page = page.replace(anchor, anchor + attr_text, 1)

    if layout == 'card':
        # kc-plan-config: default_to_subscription and try_once_layout != 'card'
        configs = list(re.finditer(r'<script type="application/json" data-kc-plan-config>(.*?)</script>', page, flags=re.S))
        buybox = [m for m in configs if '"role": "buybox"' in m.group(1)]
        assert len(buybox) == 1, 'buybox plan config'
        body = buybox[0].group(1)
        assert '"defaultToSubscription": true' in body
        page = page[: buybox[0].start(1)] + body.replace('"defaultToSubscription": true', '"defaultToSubscription": false', 1) + page[buybox[0].end(1):]

    # Loop block "Plan badges" and "One-time price struck through" filled in as Victor asked (24 Nov), on
    # OFF too: the link layout must ignore them
    extras = (f'<script type="application/json" id="kc-plan-extras-{PID}">'
              '{"badges": "712106115453: Most picked", "compareOnce": "712106115453"}</script>')
    assert page.count('</body>') == 1
    page = page.replace('</body>', extras + '</body>', 1)

    # Title block "Title line 1" filled in (Victor, 24 Nov): snippets/kc-product-title.liquid's output with
    # the card layout; the link layout keeps the product title
    if layout == 'card':
        match = re.search(r'<h1 class="h4">([^<]*)</h1>', page)
        title = html.unescape(match.group(1))
        leave_out = 'Awake & Asleep'
        line_2 = title[len(leave_out):].strip() if title.startswith(leave_out) else title
        line_2 = line_2[:1].upper() + line_2[1:]
        two_lines = ('<h1 class="h4 kc-product-title">\n    <span class="kc-product-title__name">'
                     + html.escape('Karmicare Duet: Awake & Asleep') + '</span>\n    <span class="kc-product-title__line">'
                     + html.escape(line_2) + '</span>\n  </h1>')
        page = page[: match.start()] + two_lines + page[match.end():]

    for name in ASSETS:
        pattern = r'//www\.karmicare\.com/cdn/shop/t/\d+/assets/' + re.escape(name) + r'\?v=\d+'
        page, count = re.subn(pattern, f'/assets/{name}?lane=buybox-ab', page)
        assert count >= 1, name

    # Everything else from the live store
    page = page.replace('"//www.karmicare.com/', '"https://www.karmicare.com/')
    page = page.replace(' //www.karmicare.com/', ' https://www.karmicare.com/')
    page = page.replace(',//www.karmicare.com/', ',https://www.karmicare.com/')
    page = re.sub(r'(href|src|action)="/(?!/|assets/)', r'\1="https://www.karmicare.com/', page)

    out = SERVE / ('on' if layout == 'card' else 'off') / lang / 'products' / f'{HANDLE}.html'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page)
    if layout == 'card' and lang == 'en':
        # /copy/: switch ON plus the copy proposals of PLAN.md 4b (copy_proposals.py)
        copy_out = SERVE / 'copy' / lang / 'products' / f'{HANDLE}.html'
        copy_out.parent.mkdir(parents=True, exist_ok=True)
        copy_out.write_text(copy_proposals.apply(page))
        print(copy_out)
    return out


ERRORS = '<script>window.__errs = []; addEventListener("error", (e) => window.__errs.push(String(e.message)));</script>'


def build_single(handle, pid, lane):
    """Awake / Asleep (templates/product.json, no Loop block): live as is, or with the lane's assets and
    the container attributes main-product.liquid renders without a Loop block (layout 'link', blank note).
    Both record script errors in window.__errs."""
    page = (LIVE / f'{handle}.html').read_text()
    if lane:
        anchor = f'id="kc-try-once-container-{pid}"\n                    class="tertiary-try-once-link figma-tryonce v9bb"\n                    data-active-plan="once"'
        assert page.count(anchor) == 1, handle
        en = locale('en')
        attrs = {'data-kc-once-layout': 'link', 'data-kc-once-title': en['title_once_html'], 'data-kc-once-delivery': en['delivery_once_html'],
                 'data-kc-once-guarantee': en['guarantee_once_html'], 'data-kc-once-note': '', 'data-kc-once-cta': en['cta_once_html']}
        page = page.replace(anchor, anchor + ''.join(f'\n                    {k}="{html.escape(v, quote=True)}"' for k, v in attrs.items()), 1)
        for name in ASSETS:
            pattern = r'//www\.karmicare\.com/cdn/shop/t/\d+/assets/' + re.escape(name) + r'\?v=\d+'
            page = re.sub(pattern, f'/assets/{name}?lane=buybox-ab', page)
    page = page.replace('<head>', '<head>' + ERRORS, 1)
    page = page.replace('"//www.karmicare.com/', '"https://www.karmicare.com/')
    page = page.replace(' //www.karmicare.com/', ' https://www.karmicare.com/')
    page = page.replace(',//www.karmicare.com/', ',https://www.karmicare.com/')
    page = re.sub(r'(href|src|action)="/(?!/|assets/)', r'\1="https://www.karmicare.com/', page)
    out = SERVE / ('off' if lane else 'live') / 'en' / 'products' / f'{handle}.html'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page)
    return out


(SERVE / 'assets').mkdir(parents=True, exist_ok=True)
for handle, pid in (('awake-morning-toothpaste-2-0', '16060347875709'), ('asleep-evening-toothpaste-2-0', '16060345450877')):
    print(build_single(handle, pid, False))
    print(build_single(handle, pid, True))
for name in ASSETS:
    shutil.copy(WORKTREE / 'assets' / name, SERVE / 'assets' / name)
shutil.copy(Path(__file__).with_name('copy-overlay.js'), SERVE / 'assets' / 'copy-overlay.js')
for lang in PAGES:
    print(build_live(lang))
    for layout in ('link', 'card'):
        print(build(lang, layout))
