"""Blog layout fixture: builds the preview pages for docs/blog/02-PROPOSAL.md.

usage (from the repo root): python3 -I docs/blog/fixture/build.py

Input: docs/blog/fixture/data/live.json, written by tools/fetch.js from the live store (page shells,
the eight articles, the Duo). Output: docs/blog/fixture/site/*.html. Serve the repo root with
  python3 -I -m http.server 9390 --bind 127.0.0.1
and open http://127.0.0.1:9390/docs/blog/fixture/site/index.html

The shell is the live page with its scripts removed: header, footer and every inline <style> that
Liquid printed (theme settings, button styles, Day/Night variables) stay as they are live. Theme
stylesheets that exist in assets/ load from this worktree, so the previews use the repo's CSS.
The markup in <main> is what the Liquid in Phase 2 would print, written here by hand.
"""
import html, json, math, os, re
from urllib.parse import urlparse

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
HERE = os.path.dirname(os.path.abspath(__file__))
LIVE = "https://www.karmicare.com"
FIX = "/docs/blog/fixture"

data = json.load(open(os.path.join(HERE, "data", "live.json")))
articles = data["articles"]
order = [i["handle"] for i in data["index"]]
excerpts = {i["handle"]: i["excerpt"] for i in data["index"]}
product = data["product"]

# ---- copy that already exists on the site (no new claims) ----------------------------------------
BLOG_TITLE = "News"  # blog.title
CTA = {
    # templates/index.json: two-formulas subheading, heading and hero text; locales cta_rhythm_html
    "eyebrow": "Biorhythmic oral care",
    "heading": "Two formulas. One system.",
    "heading_muted": "Designed around you.",
    "text": "Karmicare is a day-and-night oral care system designed around your mouth’s 24-hour rhythm. Awake for activation. Asleep for restoration.",
    "button": "Begin your 60-Day Rhythm",
    "url": LIVE + "/products/karmicare-biorhythmic-oral-care-system",
}
# New UI strings (proposed locale keys in 02-PROPOSAL.md §6)
T = {
    "min_read": "{n} min read",
    "sources": "Sources",
    "on_this_page": "On this page",
    "related": "Keep reading",
    "pagination": "Pagination",
    "page": "Page {n}",
    "next": "Next page",
    "opens_new": "Opens in a new window.",
    "share": "Share",  # existing: the article template's share block label
}

STUDY_HOSTS = [
    ("ncbi.nlm.nih.gov/pmc", "PubMed Central"),
    ("pubmed.ncbi.nlm.nih.gov", "PubMed"),
    ("sciencedirect.com", "ScienceDirect"),
    ("mdpi.com", "MDPI"),
    ("researchgate.net", "ResearchGate"),
    ("diabetesjournals.org", "Diabetes Care"),
    ("jech.bmj.com", "Journal of Epidemiology & Community Health"),
    ("biomedcentral.com", "BMC Public Health"),
    ("healthopenresearch.org", "Health Open Research"),
    ("jebms.org", "JEBMS"),
    ("hindawi.com", "Hindawi"),
    ("intechopen.com", "IntechOpen"),
    ("biointerfaceresearch.com", "Biointerface Research"),
]

ARROW = '<svg aria-hidden="true" focusable="false" width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M3 8h10m0 0L9 4m4 4-4 4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>'
EXTERNAL = '<svg aria-hidden="true" focusable="false" width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M14 6V2H10M14 2L6.66667 9.33334M12 8.66667V12.6667C12 13.0203 11.8595 13.3594 11.6095 13.6095C11.3594 13.8595 11.0203 14 10.6667 14H3.33333C2.97971 14 2.64057 13.8595 2.39052 13.6095C2.14048 13.3594 2 13.0203 2 12.6667V5.33333C2 4.97971 2.14048 4.64057 2.39052 4.39053C2.64057 4.14048 2.97971 4 3.33333 4H7.33333" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>'
CHEVRON = '<svg aria-hidden="true" focusable="false" width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="m4 6 4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>'

MONTHS = "January February March April May June July August September October November December".split()


def esc(s):
    return html.escape(s or "", quote=True)


def date_label(iso):
    y, m, d = iso[:10].split("-")
    return f"{MONTHS[int(m) - 1]} {int(d)}, {y}"  # time_tag format: 'date' in English


def words(a):
    text = re.sub(r"<[^>]+>", " ", a["content"])
    return len(html.unescape(text).split())


def minutes(a):
    return max(1, math.ceil(words(a) / 200))  # 200 words a minute, decision D9


def img_url(src, width):
    src = src if not src.startswith("//") else "https:" + src
    src = re.sub(r"([?&])width=\d+&?", r"\1", src).rstrip("?&")
    return src + ("&" if "?" in src else "?") + f"width={width}"


def picture(image, sizes, widths=(350, 550, 750, 1100, 1500), cls="kc-blog__media", lazy=True, cap=False):
    """What image_url + image_tag print: width/height from the file, so the box never jumps."""
    ws = [w for w in widths if w <= image["width"]] or [image["width"]]
    srcset = ", ".join(f"{img_url(image['src'], w)} {w}w" for w in ws)
    style = f' style="--kc-media-natural-width: {image["width"] / 10}rem"' if cap else ""
    loading = 'loading="lazy"' if lazy else 'fetchpriority="high"'
    return (f'<div class="{cls}"{style}><img src="{img_url(image["src"], ws[-1])}" srcset="{srcset}" sizes="{sizes}" '
            f'width="{image["width"]}" height="{image["height"]}" alt="{esc(image["alt"])}" {loading}></div>')


def meta(a, tag="ul"):
    return (f'<{tag} class="kc-blog__meta"><li><time datetime="{a["published_at"]}">{date_label(a["published_at"])}</time></li>'
            f'<li>{T["min_read"].format(n=minutes(a))}</li></{tag}>')


def sources(a):
    seen, items = set(), []
    for href, text in re.findall(r'<a\b[^>]*href="([^"]+)"[^>]*>(.*?)</a>', a["content"], re.S):
        href = html.unescape(href)
        label = next((name for host, name in STUDY_HOSTS if host in href), None)
        key = href.split("#")[0]
        if not label or key in seen:
            continue
        seen.add(key)
        text = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", text))).strip(" ,.")
        if len(text) < 4:
            text = label
        items.append(
            f'<li class="kc-blog-sources__item"><a class="kc-blog-sources__link" href="{esc(href)}" target="_blank" rel="noopener">'
            f'<span class="kc-blog-sources__title">{esc(text)}</span><span class="kc-blog-sources__host">{esc(label)}</span>'
            f'{EXTERNAL}<span class="kc-visually-hidden">{T["opens_new"]}</span></a></li>')
    if not items:
        return ""
    return (f'<aside class="kc-blog-sources" aria-labelledby="kc-blog-sources-title"><h2 class="kc-blog-sources__heading" id="kc-blog-sources-title" data-kc-blog-toc-extra>{T["sources"]}</h2>'
            f'<ul class="kc-blog-sources__list" role="list">{"".join(items)}</ul></aside>')


def body(a):
    """The body as Phase 2 prints it: the legacy size suffix dropped from the file URLs (the files
    exist at full size: 1920x1080 and 1200x802 checked), served at most 1600px wide, lazy. In Liquid:
    article.content | replace: '_480x480.', '.' | replace: '_600x600.', '.'
                    | replace: '.jpg?v=', '.jpg?width=1600&v=' | replace: '<img ', '<img loading="lazy" decoding="async" '"""
    c = a["content"]
    c = c.replace("_480x480.", ".").replace("_600x600.", ".")
    c = c.replace(".jpg?v=", ".jpg?width=1600&v=")
    return c.replace("<img ", '<img loading="lazy" decoding="async" ')


def cta_copy(heading_tag="h2"):
    return (f'<p class="kc-blog__eyebrow">{CTA["eyebrow"]}</p>'
            f'<{heading_tag} class="kc-blog-cta__heading">{CTA["heading"]} <span>{CTA["heading_muted"]}</span></{heading_tag}>'
            f'<p class="kc-blog-cta__text">{CTA["text"]}</p>'
            f'<a class="karmicare__btn-primary kc-blog__button" href="{CTA["url"]}">{CTA["button"]}</a>')


def related_for(handle, n=3):
    return [h for h in order if h != handle][:n]


def link(handle, d):
    return f"{d}-article.html" if handle == "nano-hydroxyapatite" else f"{d}-article-{handle[:24]}.html"


def section(inner, surface, n):
    return f'<div class="shopify-section" id="shopify-section-kc-blog-{n}"><div class="kc-surface" data-kc-surface="{surface}">{inner}</div></div>'


# ---- Direction A ---------------------------------------------------------------------------------
def a_row(handle, d, heading="h3", excerpt=True):
    a = articles[handle]
    ex = f'<p class="kc-blog-a-row__excerpt">{esc(excerpts.get(handle))}</p>' if excerpt and excerpts.get(handle) else ""
    thumb = ""
    if a["image"]:
        # decorative: the title next to it names the article
        img = dict(a["image"], alt="")
        thumb = f'<div class="kc-blog-a-row__thumb">{picture(img, "(min-width: 750px) 160px, 96px", widths=(200, 320, 480))}</div>'
    return (f'<li class="kc-blog-a-row"><a class="kc-blog-a-row__link" href="{link(handle, d)}" data-fixture-link>'
            f'{thumb}<div class="kc-blog-a-row__text">{meta(a, "ul")}<{heading} class="kc-blog-a-row__title">{esc(a["title"])}</{heading}>{ex}</div>'
            f'<span class="kc-blog-a-row__arrow">{ARROW}</span></a></li>')


def a_article(handle):
    a = articles[handle]
    fig = ""
    if a["image"]:
        fig = f'<figure class="kc-blog-a__figure" data-kc-featured>{picture(a["image"], "(min-width: 1200px) 840px, (min-width: 990px) 680px, 100vw", lazy=False, cap=True)}</figure>'
    standfirst = f'<p class="kc-blog__standfirst">{esc(excerpts.get(handle))}</p>' if excerpts.get(handle) else ""
    nav = (f'<nav class="kc-blog-a__nav" aria-labelledby="kc-blog-toc-title" data-kc-blog-toc-box>'
           f'<p class="kc-blog__eyebrow" id="kc-blog-toc-title">{T["on_this_page"]}</p>'
           f'<ol class="kc-blog-a__nav-list" role="list" data-kc-blog-toc></ol></nav>')
    s1 = (f'<article class="kc-blog kc-blog-a">'
          f'<header class="kc-blog-a__head"><div class="kc-blog-a__grid"><div class="kc-blog-a__text">'
          f'<a class="kc-blog__eyebrow" href="a-blog.html" data-fixture-link>{BLOG_TITLE}</a>'
          f'<h1 class="kc-blog__title">{esc(a["title"])}</h1>{standfirst}{meta(a)}</div>{fig}</div></header>'
          f'<div class="kc-blog-a__body"><div class="kc-blog-a__grid">{nav}<div class="kc-blog-a__text">'
          f'<div class="kc-blog__body rte">{body(a)}</div>'
          f'<div class="kc-blog-a__end">{sources(a)}<div class="kc-blog-a__cta">{cta_copy()}</div></div>'
          f'</div></div></div></article>')
    rows = "".join(a_row(h, "a", excerpt=False) for h in related_for(handle))
    s2 = (f'<div class="kc-blog kc-blog-a kc-blog-a__related"><div class="kc-blog-a__grid"><div class="kc-blog-a__text">'
          f'<h2 class="kc-blog__section-heading">{T["related"]}</h2><ul class="kc-blog-a-list" role="list">{rows}</ul></div></div></div>')
    return section(s1, "page", 1) + section(s2, "transition", 2)


def pagination(d):
    return (f'<nav aria-label="{T["pagination"]}"><ul class="kc-blog-pagination" role="list">'
            f'<li><span aria-current="page">1</span></li><li><a href="{d}-blog.html" aria-label="{T["page"].format(n=2)}">2</a></li>'
            f'<li><a href="{d}-blog.html" aria-label="{T["next"]}">{ARROW}</a></li></ul></nav>')


def a_blog(page):
    rows = "".join(a_row(h, "a", heading="h2") for h in page)
    s1 = (f'<div class="kc-blog kc-blog-a-index"><header class="kc-blog-a-index__head"><div class="kc-blog__wrap">'
          f'<h1 class="kc-blog__title">{BLOG_TITLE}</h1></div></header>'
          f'<div class="kc-blog-a-index__list"><div class="kc-blog__wrap"><ul class="kc-blog-a-list" role="list">{rows}</ul>{pagination("a")}</div></div></div>')
    return section(s1, "page", 1)


# ---- Direction B ---------------------------------------------------------------------------------
def b_card(handle, d, heading="h3", lead=False):
    a = articles[handle]
    sizes = "(min-width: 990px) 760px, calc(100vw - 40px)" if lead else "(min-width: 990px) 440px, (min-width: 750px) 50vw, calc(100vw - 40px)"
    media = picture(a["image"], sizes) if a["image"] else ""
    ex = f'<p class="kc-blog-b-card__excerpt">{esc(excerpts.get(handle))}</p>' if excerpts.get(handle) else ""
    return (f'<li class="kc-blog-b-card{" kc-blog-b-lead" if lead else ""}"><a class="kc-blog-b-card__link" href="{link(handle, d)}" data-fixture-link>'
            f'{media}<div class="kc-blog-b-card__text">{meta(a)}<{heading} class="kc-blog-b-card__title">{esc(a["title"])}</{heading}>{ex}</div></a></li>')


def b_article(handle):
    a = articles[handle]
    fig = ""
    if a["image"]:
        fig = f'<div data-kc-featured>{picture(a["image"], "(min-width: 990px) 560px, calc(100vw - 40px)", lazy=False)}</div>'
    standfirst = f'<p class="kc-blog__standfirst">{esc(excerpts.get(handle))}</p>' if excerpts.get(handle) else ""
    toc = (f'<aside class="kc-blog-b__rail" data-kc-blog-toc-box><details class="kc-blog-toc">'
           f'<summary>{T["on_this_page"]}{CHEVRON}</summary>'
           f'<p class="kc-blog-toc__title" aria-hidden="true">{T["on_this_page"]}</p>'
           f'<ol class="kc-blog-toc__list" role="list" data-kc-blog-toc></ol></details></aside>')
    s1 = (f'<article class="kc-blog kc-blog-b">'
          f'<header class="kc-blog-b__hero"><div class="kc-blog__wrap kc-blog-b__frame"><div class="kc-blog-b__hero-grid">'
          f'<div><a class="kc-blog__eyebrow" href="b-blog.html" data-fixture-link>{BLOG_TITLE}</a>'
          f'<h1 class="kc-blog__title">{esc(a["title"])}</h1>{standfirst}{meta(a)}</div>{fig}</div></div></header>'
          f'<div class="kc-blog-b__main"><div class="kc-blog__wrap kc-blog-b__frame"><div class="kc-blog-b__layout">{toc}'
          f'<div class="kc-blog-b__column"><div class="kc-blog__body rte">{a["content"]}</div>'
          f'<div class="kc-blog-b__end">{sources(a)}</div></div></div></div></div></article>')
    shot = ""
    if product and product.get("featured_image"):
        src = product["featured_image"]
        shot = f'<div class="kc-blog-b__cta-media"><img src="{img_url(src, 640)}" width="640" height="640" alt="" loading="lazy"></div>'
    s2 = (f'<div class="kc-blog kc-blog-b__cta"><div class="kc-blog__wrap kc-blog-b__frame"><div class="kc-blog-b__cta-card">{shot}'
          f'<div class="kc-blog-b__cta-copy">{cta_copy()}</div></div></div></div>')
    cards = "".join(b_card(h, "b") for h in related_for(handle))
    s3 = (f'<div class="kc-blog kc-blog-b__related"><div class="kc-blog__wrap kc-blog-b__frame">'
          f'<h2 class="kc-blog__section-heading">{T["related"]}</h2><ul class="kc-blog-b-grid" role="list">{cards}</ul></div></div>')
    return section(s1, "page", 1) + section(s2, "transition", 2) + section(s3, "transition", 3)


def b_blog(page):
    lead = b_card(page[0], "b", heading="h2", lead=True)
    cards = "".join(b_card(h, "b", heading="h2") for h in page[1:])
    s1 = (f'<div class="kc-blog kc-blog-b-index"><header class="kc-blog-b-index__head"><div class="kc-blog__wrap kc-blog__wrap--wide">'
          f'<h1 class="kc-blog__title">{BLOG_TITLE}</h1></div></header>'
          f'<div class="kc-blog-b-index__body"><div class="kc-blog__wrap kc-blog__wrap--wide"><ul class="kc-blog-b-grid kc-blog-b-grid--lead" role="list">{lead}</ul>'
          f'<ul class="kc-blog-b-grid" role="list">{cards}</ul>{pagination("b")}</div></div></div>')
    return section(s1, "page", 1)


# ---- Direction C ---------------------------------------------------------------------------------
def c_card(handle, d, heading="h3"):
    a = articles[handle]
    media = picture(a["image"], "(min-width: 990px) 440px, (min-width: 750px) 50vw, calc(100vw - 40px)") if a["image"] else ""
    return (f'<li class="kc-blog-c-card"><a class="kc-blog-c-card__link" href="{link(handle, d)}" data-fixture-link>{media}'
            f'<div class="kc-blog-c-card__body"><{heading} class="kc-blog-c-card__title">{esc(a["title"])}</{heading}>'
            f'<div class="kc-blog-c-card__foot">{meta(a)}{ARROW}</div></div></a></li>')


def c_article(handle):
    a = articles[handle]
    fig = ""
    if a["image"]:
        fig = f'<figure class="kc-blog-c__figure" data-kc-featured>{picture(a["image"], "(min-width: 750px) 680px, calc(100vw - 40px)", lazy=False, cap=True)}</figure>'
    standfirst = f'<p class="kc-blog__standfirst">{esc(excerpts.get(handle))}</p>' if excerpts.get(handle) else ""
    s1 = (f'<div class="kc-blog kc-blog-c__stage"><article class="kc-blog-c__paper">'
          f'<header><a class="kc-blog__eyebrow" href="c-blog.html" data-fixture-link>{BLOG_TITLE}</a>'
          f'<h1 class="kc-blog__title">{esc(a["title"])}</h1>{standfirst}{meta(a)}{fig}</header>'
          f'<div class="kc-blog__body rte">{a["content"]}</div>{sources(a)}'
          f'<div class="kc-blog-c__cta">{cta_copy()}</div></article></div>')
    cards = "".join(c_card(h, "c") for h in related_for(handle))
    s2 = (f'<div class="kc-blog kc-blog-c__related"><div class="kc-blog__wrap kc-blog__wrap--wide">'
          f'<h2 class="kc-blog__section-heading">{T["related"]}</h2><ul class="kc-blog-c-grid" role="list">{cards}</ul></div></div>')
    return section(s1, "page", 1) + section(s2, "transition", 2)


def c_blog(page):
    cards = "".join(c_card(h, "c", heading="h2") for h in page)
    s1 = (f'<div class="kc-blog kc-blog-c-index"><header class="kc-blog-c-index__head"><div class="kc-blog__wrap kc-blog__wrap--wide">'
          f'<h1 class="kc-blog__title">{BLOG_TITLE}</h1></div></header>'
          f'<div class="kc-blog-c-index__body"><div class="kc-blog__wrap kc-blog__wrap--wide"><ul class="kc-blog-c-grid" role="list">{cards}</ul>{pagination("c")}</div></div></div>')
    return section(s1, "page", 1)


# ---- Direction D ---------------------------------------------------------------------------------
SHARE = '<svg aria-hidden="true" focusable="false" width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M6.67 8.67a3.33 3.33 0 0 0 5.02.36l2-2a3.33 3.33 0 0 0-4.71-4.71l-1.15 1.14M9.33 7.33a3.33 3.33 0 0 0-5.02-.36l-2 2a3.33 3.33 0 0 0 4.71 4.71l1.14-1.14" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>'
HOME_PATH = os.path.join(HERE, "data", "home-cta.json")
home = json.load(open(HOME_PATH)) if os.path.exists(HOME_PATH) else None


def end_cta():
    """The homepage's end CTA: the featured-product section exactly as the live homepage prints it
    (Phase 2: the same section in templates/article.json). Its scripts are removed like the shell's,
    so the Loop plan picker shows its Liquid state only, except the two that run the kit animation:
    the kc-hero-animation element and the script that lands the kit on the button line."""
    if not home or not home["section"]:
        return ""
    keep = [m.group(0) for m in re.finditer(r"<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>", home["section"], re.S)
            if "kc-hero-animation" in m.group(1) or "--kc-hero-lift" in m.group(1)]
    s = rewrite(home["section"])
    s = s.replace('id="shopify-section-template--', 'id="shopify-section-kc-blog-endcta-template--', 1)
    return s + "".join(keep)


# Featured-picture alternatives for the nano article (Victor, 26 Oct: the 520px picture is small and
# shows an outdated pump bottle). All three are live in Files today.
CDN = "https://www.karmicare.com/cdn/shop/files/"
HERO_OPTIONS = {
    "1": ({"src": CDN + "kc-research-nhap-tubules-2000x2400-v1.jpg", "width": 2000, "height": 2400,
           "alt": "Illustration of dentine tubules"}, None,
          "The Nano-HAp research card's picture (Victor picked it 24 Oct, live on the homepage and PDP card)"),
    "2": ({"src": CDN + "kc-hero-kit.png", "width": 3936, "height": 2960,
           "alt": "The Karmicare kit: Awake and Asleep toothpaste, two toothbrushes and floss"}, "contain",
          "The homepage hero kit (kc-hero-kit.png), whole on the accent tint"),
    "3": ({"src": CDN + "karmicare-duo-pack-transparent.png", "width": 2048, "height": 2048,
           "alt": "Awake and Asleep toothpaste with their box"}, "contain",
          "The Duo packshot (the product's first picture), whole on the accent tint"),
}


def d_article(handle, image=None, fit=None):
    a = dict(articles[handle])
    if image:
        a["image"] = image  # a featured-picture alternative (02-PROPOSAL D18)
    fig = ""
    if a["image"]:
        fit_attr = f' data-fit="{fit}"' if fit else ""
        fig = (f'<figure class="kc-blog-d__figure"{fit_attr} data-kc-featured>'
               f'{picture(a["image"], "(min-width: 1344px) 1280px, (min-width: 750px) calc(100vw - 64px), 100vw", widths=(550, 750, 1100, 1500, 1920), lazy=False, cap=True)}</figure>')
    standfirst = f'<p class="kc-blog__standfirst">{esc(excerpts.get(handle))}</p>' if excerpts.get(handle) else ""
    # the legal pages' menu (sections/legal-toc-section.liquid), with its theme classes
    toc = (f'<aside class="kc-blog-d__toc" data-kc-blog-contents-box>'
           f'<p class="kc-blog-d-toc__eyebrow subtitle-item opacity-xl" aria-hidden="true">{T["on_this_page"]}</p>'
           f'<nav aria-label="{T["on_this_page"]}"><ul class="kc-blog-d-toc__list" role="list" data-kc-blog-contents></ul></nav>'
           f'</aside>')
    s1 = (f'<article class="kc-blog kc-blog-d">'
          f'<header class="kc-blog-d__head"><div class="kc-blog__wrap kc-blog__wrap--wide">'
          # the homepage's section eyebrow (kc-caption-subheading subtitle-item), Victor 26 Oct
          f'<a class="kc-blog-d__eyebrow kc-caption-subheading subtitle-item" href="d-blog.html" data-fixture-link>{BLOG_TITLE}</a>'
          f'<h1 class="kc-blog__title">{esc(a["title"])}</h1>{standfirst}'
          f'<div class="kc-blog-d__bar">{meta(a)}'
          f'<button type="button" class="kc-blog-d__share">{SHARE}<span>{T["share"]}</span></button></div>'
          f'</div></header>{fig}'
          f'<div class="kc-blog-d__main"><div class="kc-blog-d__layout">{toc}<div class="kc-blog-d__text">'
          f'<div class="kc-blog__body rte">{body(a)}</div>'
          f'<div class="kc-blog-d__end">{sources(a)}</div></div></div></div></article>')
    rows = "".join(a_row(h, "d", excerpt=False) for h in related_for(handle))
    s3 = (f'<div class="kc-blog kc-blog-d-related"><div class="kc-blog-d__layout"><div class="kc-blog-d__text">'
          f'<h2 class="kc-blog__section-heading">{T["related"]}</h2><ul class="kc-blog-a-list" role="list">{rows}</ul></div></div></div>')
    # Victor (26 Oct): Keep reading first, the homepage end CTA last
    return section(s1, "page", 1) + section(s3, "transition", 3) + end_cta()


def d_blog(page):
    rows = "".join(a_row(h, "d", heading="h2") for h in page)
    s1 = (f'<div class="kc-blog kc-blog-d-index"><header class="kc-blog-d-index__head"><div class="kc-blog__wrap">'
          f'<h1 class="kc-blog__title">{BLOG_TITLE}</h1></div></header>'
          f'<div class="kc-blog-d-index__list"><div class="kc-blog__wrap"><ul class="kc-blog-a-list" role="list">{rows}</ul>{pagination("d")}</div></div></div>')
    return section(s1, "page", 1)


# ---- Shell ---------------------------------------------------------------------------------------
SURFACE_JS = re.search(r"<script>(.*?)</script>", open(os.path.join(ROOT, "snippets", "kc-surface.liquid")).read(), re.S).group(1)


def asset(m):
    name = m.group(1)
    if name.endswith(".css") and os.path.exists(os.path.join(ROOT, "assets", name)):
        return f"/assets/{name}"
    return "https:" + m.group(0) if m.group(0).startswith("//") else m.group(0)


def rewrite(s):
    """Live HTML -> fixture HTML: no scripts, root-relative URLs to the live store, theme CSS that
    exists in this worktree from assets/."""
    s = re.sub(r"<script\b[^>]*>.*?</script>", "", s, flags=re.S | re.I)
    s = re.sub(r'<link[^>]+rel="(?:modulepreload|preload)"[^>]*as="script"[^>]*>', "", s)
    s = re.sub(r'(href|action|src)="/(?!/)', rf'\1="{LIVE}/', s)
    s = re.sub(r"(?:https?:)?//www\.karmicare\.com/cdn/shop/t/\d+/assets/([^\"'?\s)]+)(?:\?v=\d+)?", asset, s)
    return re.sub(r'(?<=[\s,"(=])//(?=[a-z0-9.-]+\.[a-z]{2,}/)', "https://", s)


def shell(kind, title, main, direction):
    s = rewrite(data["shell"][kind])
    s = re.sub(r"<title>.*?</title>", f"<title>{esc(title)}</title>", s, flags=re.S)
    css = ["kc-blog-base.css", f"kc-blog-{direction}.css"]
    if direction == "d":
        css.insert(1, "kc-blog-a.css")  # the Keep reading and index rows
    head_add = f'<script>{SURFACE_JS}</script>' + "".join(f'<link rel="stylesheet" href="{FIX}/css/{c}">' for c in css)
    if direction == "d" and home:
        # what the homepage head adds for its end CTA: Loop's widget styles (theme.liquid prints
        # them for product, index and collection only; Phase 2 adds article)
        head_add += '<link rel="stylesheet" href="/assets/loop-widget.css">' + (home["loopStyle"] or "")
    head_add += f'<link rel="stylesheet" href="{FIX}/css/fixture.css">'
    s = s.replace("</head>", head_add + "</head>", 1)
    s = re.sub(r"(<main\b[^>]*>).*?(</main>)", lambda m: m.group(1) + main + m.group(2), s, count=1, flags=re.S)
    # the theme's own navigation script: it publishes the floating bar's position and clearance
    tail = f'<script src="{FIX}/js/fixture.js"></script><script src="/assets/kc-navigation.js"></script>'
    if direction in ("a", "b"):
        tail += f'<script src="{FIX}/js/kc-blog-toc.js"></script>'
    if direction == "d":
        tail += f'<script src="{FIX}/js/kc-blog-contents.js"></script>'
    s = s.replace("</body>", tail + "</body>", 1)
    return s


def write(name, text):
    out = os.path.join(HERE, "site", name)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w").write(text)
    print("wrote", os.path.relpath(out, ROOT), len(text))


builders = {"a": (a_article, a_blog), "b": (b_article, b_blog), "c": (c_article, c_blog), "d": (d_article, d_blog)}
names = {"a": "Quiet column", "b": "Editorial with a reading rail", "c": "Research notebook", "d": "Editorial (reference)"}
for d, (art, blog) in builders.items():
    for handle in order:
        write(link(handle, d), shell("article", f"Blog {d.upper()} · {names[d]} · {articles[handle]['title'][:40]}", art(handle), d))
    write(f"{d}-blog.html", shell("blog", f"Blog {d.upper()} · {names[d]} · index", blog(order[:6]), d))

for k, (img, fit, label) in HERO_OPTIONS.items():
    write(f"d-article-hero-{k}.html", shell("article", f"Blog D · featured picture option {k}", d_article("nano-hydroxyapatite", img, fit), "d"))

idx = ["<!doctype html><meta charset=utf-8><meta name=viewport content='width=device-width,initial-scale=1'><title>Blog fixture</title>",
       "<style>body{font:16px/1.5 system-ui;margin:24px;max-width:760px}a{color:#191f38}li{margin:4px 0}</style>",
       "<h1>Blog layout fixture</h1><p>Add <code>?mode=night</code>, <code>?labels=site</code>, <code>?noimage=1</code> or <code>?fluid=1</code> to any page.</p>"]
for d in "dabc":
    idx.append(f"<h2>{d.upper()} · {names[d]}</h2><ul>")
    idx.append(f'<li><a href="{d}-article.html">Article: nano-hydroxyapatite (long, small featured image)</a> · <a href="{d}-article.html?mode=night">night</a></li>')
    idx.append(f'<li><a href="{link("morning-and-night-time-brushing-why-timing-matters", d)}">Article: morning and night brushing (short)</a></li>')
    idx.append(f'<li><a href="{d}-blog.html">Index</a> · <a href="{d}-blog.html?mode=night">night</a></li></ul>')
write("index.html", "".join(idx))
