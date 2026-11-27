"""Buybox-ab localhost preview builder.

Takes the live Duo PDP HTML (EN/NL/FR, fetched cookie-less) and writes, per language, a switch OFF
and a switch ON page: the lane's assets (loop-widget.js, kc-plan-select.js, kc-buybox.css, karmi-add-to-cart.js) replace
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
ASSETS = ['loop-widget.js', 'kc-plan-select.js', 'kc-buybox.css', 'karmi-add-to-cart.js']
PAGES = {'en': 'duo.html', 'nl': 'duo-nl.html', 'fr': 'duo-fr.html'}
LOCALES = {'en': 'en.default.json', 'nl': 'nl.json', 'fr': 'fr.json'}


def locale(lang):
    text = (WORKTREE / 'locales' / LOCALES[lang]).read_text()
    text = re.sub(r'^\s*/\*.*?\*/', '', text, flags=re.S)
    data = json.loads(text)
    kc = data['kc']
    quantity = data['products']['product']['quantity']
    return dict(kc['sticky_cart'], plans_or=kc['plans']['or'], close=data['accessibility']['close'],
                qty_label=quantity['label'], qty_decrease=quantity['decrease'], qty_increase=quantity['increase'])


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


# Loop block "Plan popup / side panel: text per plan" for the Year, as the lane drafted it (VOORSTEL,
# EN, 27 Nov, from Victor's brief, second version: the customer's benefit, "We are there day and
# night", no heading)
PROMISE_VOORSTEL = (
    "Your dentist sees you once or twice a year. We are there day and night, from the moment you leave "
    "the chair until you sit back down. So you can walk into every check-up ready, and out with peace "
    "of mind."
)


def fresh_stock(page):
    """The Year's "6 duos a year (3 now, 3 in month 6)" line with ", guaranteed fresh stock" (Victor, 27 Nov):
    a Loop admin text, so emulated in Loop's product JSON as that edit would deliver it (EN only)."""
    pattern = r'(<script class="loopProductQuickJson-' + PID + r'" type="application/json">)(.*?)(</script>)'
    count = 0

    def patch(match):
        nonlocal count
        product = json.loads(match.group(2))
        for group in product['selling_plan_groups']:
            for plan in group['selling_plans']:
                if str(plan['id']) == '712155431293' and '(3 now, 3 in month 6)</div>' in plan['description']:
                    plan['description'] = plan['description'].replace(
                        '(3 now, 3 in month 6)</div>', '(3 now, 3 in month 6), guaranteed fresh stock</div>', 1)
                    count += 1
        return match.group(1) + json.dumps(product, ensure_ascii=False) + match.group(3)

    page = re.sub(pattern, patch, page, flags=re.S)
    assert count == 2, f'fresh stock: {count}'
    return page


def build(lang, layout):
    page = (LIVE / PAGES[lang]).read_text()
    sticky = locale(lang)
    note = re.search(r'class="ft-note">([^<]*)', page).group(1).strip()
    product_title = html.unescape(re.search(r'<h1 class="h4">([^<]*)</h1>', page).group(1))
    attrs = {
        'data-kc-once-layout': layout,
        'data-kc-once-title': sticky['title_once_html'],
        'data-kc-once-shipping': html.unescape(re.search(r'class="ft-ship">([^<]*)', page).group(1).strip()),
        'data-kc-once-note': html.unescape(note),
        'data-kc-once-max': '1',
        'data-kc-title-many': sticky['title_year_html'],
        'data-kc-qty-label': sticky['qty_label'],
        'data-kc-qty-decrease': sticky['qty_decrease'].replace('{{ product }}', product_title),
        'data-kc-qty-increase': sticky['qty_increase'].replace('{{ product }}', product_title),
        # Loop block "Try once: button text" filled in by Victor (24 Nov), EN only: until it is translated
        # Shopify shows the English value on /nl and /fr too
        'data-kc-once-cta': 'Try once, purchase now',
        'data-kc-or': sticky['plans_or'],
        'data-kc-credit': sticky['credit_html'],
        'data-kc-credit-checkup': sticky['credit_checkup_html'],
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
    # OFF too: the link layout must ignore them. The rest at its default; the variants below change it.
    extras = (f'<script type="application/json" id="kc-plan-extras-{PID}">'
              + json.dumps({'badges': '712106115453: Most picked', 'compareOnce': '712106115453', 'asLink': '',
                            'chipsSelectedOnly': False, 'linkOpens': 'card', 'closeLabel': sticky['close'],
                            'panelText': ''},
                           ensure_ascii=False)
              + '</script>'
              # The plan dialog's close icon, as sections/main-product.liquid renders it for popup / panel
              + f'<template id="kc-icon-close-{PID}">' + (WORKTREE / 'assets' / 'kc-icon-close.svg').read_text() + '</template>')
    assert page.count('</body>') == 1
    page = page.replace('</body>', extras + '</body>', 1)

    # snippets/sticky-cart-block.liquid renders its script into the page: the lane's two changes (the Try
    # once quantity in the title and the bar's quantity field, and a render on kc:once-quantity), as Liquid
    # would render them
    title_line = "      var title = plain ? cfg.productTitle || '' : copy['title_' + state.type] || '';"
    assert page.count(title_line) == 1, 'sticky title line'
    page = page.replace(title_line, title_line + """
      var onceQuantity = state.type === 'once' && window.KCOnceQuantity ? window.KCOnceQuantity.get(cfg.productId) : 1;
      if (onceQuantity > 1) title = window.KCOnceQuantity.titleFor(title, copy.title_year, onceQuantity);
      var quantityInput = form.querySelector('input[name="quantity"]');
      if (quantityInput && quantityInput.value !== String(onceQuantity)) quantityInput.value = String(onceQuantity);""", 1)
    change_line = "if (event.target && event.target.closest && event.target.closest('.product__info-container')) queueRender();\n      });"
    assert page.count(change_line) == 1, 'sticky change line'
    page = page.replace(change_line, change_line + "\n      on(document, 'kc:once-quantity', queueRender);", 1)
    # ... and its Try once link with a plan selected: the card's chosen quantity, in the price and the buy
    try_line = "var tryOnceText = !once && !cfg.requiresPlan && state.oneTimePrice != null ? fill(copy.try_once, { price: money(state.oneTimePrice) }) : '';"
    assert page.count(try_line) == 1, 'sticky try once line'
    page = page.replace(try_line, "var onceChosen = window.KCOnceQuantity && window.KCOnceQuantity.chosen ? window.KCOnceQuantity.chosen(cfg.productId) : 1;\n      "
                        + try_line.replace('money(state.oneTimePrice)', 'money(state.oneTimePrice * onceChosen)'), 1)
    cut_line = "var cut = plain ? -1 : title.indexOf(' · ');"
    assert page.count(cut_line) == 1, 'sticky cut line'
    page = page.replace(cut_line, "var cut = plain || onceQuantity > 1 ? -1 : title.indexOf(' · ');", 1)
    cta_line = "setText('cta', plain ? cfg.buttonText || '' : copy['cta_' + state.type]);"
    assert page.count(cta_line) == 1, 'sticky cta line'
    page = page.replace(cta_line, "var onceContainer = state.type === 'once' && document.getElementById('kc-try-once-container-' + cfg.productId);\n"
                        "      var onceCta = onceContainer && onceContainer.getAttribute('data-kc-once-layout') === 'card'\n"
                        "        ? onceContainer.getAttribute('data-kc-once-cta') || ''\n"
                        "        : '';\n"
                        "      setText('cta', plain ? cfg.buttonText || '' : onceCta || copy['cta_' + state.type]);", 1)
    try_set = "setText('try-once', tryOnceText);"
    assert page.count(try_set) == 1, 'sticky try once set'
    page = page.replace(try_set, try_set + "\n      field('try-once').dataset.kcOnceQuantity = String(onceChosen);", 1)

    for name in ASSETS:
        pattern = r'//www\.karmicare\.com/cdn/shop/t/\d+/assets/' + re.escape(name) + r'\?v=\d+'
        page, count = re.subn(pattern, f'/assets/{name}?lane=buybox-ab', page)
        assert count >= 1, name
    page = with_info_sheet(page, sticky['close'])

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
    if layout == 'card':
        # /compact/: switch ON, three cards, chips on the selected card only (the lane's preference, 26 Nov)
        compact_page = page.replace('"chipsSelectedOnly": false', '"chipsSelectedOnly": true', 1)
        assert compact_page != page, 'compact'
        compact_out = SERVE / 'compact' / lang / 'products' / f'{HANDLE}.html'
        compact_out.parent.mkdir(parents=True, exist_ok=True)
        compact_out.write_text(compact_page)
        print(compact_out)
        # /year/: switch ON plus "Plans as a link under the cards" = the Year (Victor, 24 Nov)
        year_out = SERVE / 'year' / lang / 'products' / f'{HANDLE}.html'
        year_out.parent.mkdir(parents=True, exist_ok=True)
        year_page = page.replace('"asLink": ""', '"asLink": "712155431293"', 1)
        assert year_page != page, 'asLink'
        year_out.write_text(year_page)
        print(year_out)
        # On /year/, with the plan cards' live texts (Victor, 26 Nov: "zoiezo de tekst en waarden zelfde
        # zoals live in de plan kaarten"): /chips/ chips on the selected card only, /popup/ and /panel/
        # the Year link opening a popup or a side panel
        chips = ('"chipsSelectedOnly": false', '"chipsSelectedOnly": true')
        popup = ('"linkOpens": "card"', '"linkOpens": "popup"')
        panel = ('"linkOpens": "card"', '"linkOpens": "panel"')
        # /candidate/: Victor's lean (27 Nov), compact (chips on the selected card only) with the Year as a
        # link that opens the side panel
        for variant, changes in (
            ('chips', [chips]),
            ('popup', [popup]),
            ('panel', [panel]),
            ('candidate', [chips, panel, (
                '"panelText": ""',
                '"panelText": ' + json.dumps('712155431293: ' + PROMISE_VOORSTEL, ensure_ascii=False),
            ), (
                # "Try once: maximum quantity" 6 (Victor, 27 Nov: 4 as a proposal, then 6 for the MVP)
                'data-kc-once-max="1"', 'data-kc-once-max="6"',
            )]),
        ):
            variant_page = year_page
            for old, new in changes:
                changed = variant_page.replace(old, new, 1)
                assert changed != variant_page, variant
                variant_page = changed
            variant_out = SERVE / variant / lang / 'products' / f'{HANDLE}.html'
            variant_out.parent.mkdir(parents=True, exist_ok=True)
            # The Loop admin edit is EN; NL and FR come through Loop Multilingual
            if variant == 'candidate' and lang == 'en':
                variant_page = fresh_stock(variant_page)
            variant_out.write_text(variant_page)
            print(variant_out)
    return out


ERRORS = '<script>window.__errs = []; addEventListener("error", (e) => window.__errs.push(String(e.message)));</script>'


def with_info_sheet(page, close_label):
    """The lane's new files as layout/theme.liquid loads them on product, index and article pages: the (i)
    sheet on a phone (assets/kc-info-sheet.css / .js, Victor 27 Nov)."""
    tags = ('<link rel="stylesheet" href="/assets/kc-info-sheet.css?lane=buybox-ab">'
            f'<script src="/assets/kc-info-sheet.js?lane=buybox-ab" data-close-label="{html.escape(close_label, quote=True)}" defer="defer"></script>')
    assert page.count('</head>') == 1, 'head'
    return page.replace('</head>', tags + '</head>', 1)


def build_single(handle, pid, lane):
    """Awake / Asleep (templates/product.json, no Loop block): live as is, or with the lane's assets and
    the container attributes main-product.liquid renders without a Loop block (layout 'link', blank note).
    Both record script errors in window.__errs."""
    page = (LIVE / f'{handle}.html').read_text()
    if lane:
        anchor = f'id="kc-try-once-container-{pid}"\n                    class="tertiary-try-once-link figma-tryonce v9bb"\n                    data-active-plan="once"'
        assert page.count(anchor) == 1, handle
        en = locale('en')
        attrs = {'data-kc-once-layout': 'link', 'data-kc-once-title': en['title_once_html'], 'data-kc-once-shipping': '',
                 'data-kc-once-note': '', 'data-kc-once-cta': en['cta_once_html']}
        page = page.replace(anchor, anchor + ''.join(f'\n                    {k}="{html.escape(v, quote=True)}"' for k, v in attrs.items()), 1)
        for name in ASSETS:
            pattern = r'//www\.karmicare\.com/cdn/shop/t/\d+/assets/' + re.escape(name) + r'\?v=\d+'
            page = re.sub(pattern, f'/assets/{name}?lane=buybox-ab', page)
        page = with_info_sheet(page, en['close'])
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
for name in ASSETS + ['kc-info-sheet.css', 'kc-info-sheet.js']:
    shutil.copy(WORKTREE / 'assets' / name, SERVE / 'assets' / name)
shutil.copy(Path(__file__).with_name('copy-overlay.js'), SERVE / 'assets' / 'copy-overlay.js')
for lang in PAGES:
    print(build_live(lang))
    for layout in ('link', 'card'):
        print(build(lang, layout))
