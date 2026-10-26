# Blog lane · 02 · Layout proposal

Three layout directions for every article page and the blog index, built as rendered previews. Nothing is changed in the theme yet. Inventory and findings: `01-INVENTORY.md`. Branch `karmicare/soft-launch-blog` from `karmicare/soft-launch` @ ee00446, 26 Oct 2026.

## 1. How to look at it

Start the fixture server from the worktree root (it is running now on Victor's Mac):

```sh
python3 -I -m http.server 9390 --bind 127.0.0.1
```

| What | URL |
|---|---|
| **Side by side, every screenshot** (Day/Night and width switches) | http://127.0.0.1:9390/docs/blog/fixture/site/compare.html |
| All live fixture pages | http://127.0.0.1:9390/docs/blog/fixture/site/index.html |
| A · article / index | `…/site/a-article.html` · `…/site/a-blog.html` |
| B · article / index | `…/site/b-article.html` · `…/site/b-blog.html` |
| C · article / index | `…/site/c-article.html` · `…/site/c-blog.html` |

Any page takes `?mode=night`, `?labels=site` (the site's Nunito uppercase labels, D2), `?noimage=1` (an article without a featured image) and `?fluid=1` (the "Fluid type (preview)" setting). Every article exists in every direction (`a-article-<handle>.html`), so the short ones (`…-morning-and-night-time-b.html`, 756 words) can be compared with the long nano article (2,985 words).

**What the fixture is.** The live page's header, footer and every inline style Liquid printed (theme settings, button styles, Day/Night variables), with the live scripts removed. The theme stylesheets load from this worktree's `assets/`, so the previews use the repo's real CSS and tokens. The article bodies, titles, dates, excerpts and images are the live store's (fetched 26 Oct, `fixture/data/live.json`). The markup inside `<main>` is what the Phase 2 Liquid would print, written by `fixture/build.py`. Rebuild with `python3 -I docs/blog/fixture/build.py`.

**Screenshots:** `docs/blog/shots/`, named `<direction>-<page>-<part>-<width>-<mode>.png`. For every direction:
- article and index top at 390, 750, 1100 and 1440, in Day and Night;
- the article's body (the first quote), Sources, CTA and related at 390 and 1440, in Day and Night;
- extras: `b-article-toc-390-day.png` (the phone "On this page"), `b-article-short-1440-day.png` (a short article without the rail), `a-article-noimage-390-day.png`, and `a-article-cta-390-day-labels-site.png` (D2).

The repo ignores PNGs under `docs/` (`.gitignore` line 39), so the shots live in the worktree and `compare.html` is the way to view them. They are rebuilt with `fixture/tools/shots.py <pageId> matrix`.

**Before:** `shots/00-live-article-desktop-top.png` (the live nano article: the 520 px hero stretched to about 1,200 px) and `shots/00-live-article-390-full.png`.

## 2. What all three share

These are in `fixture/css/kc-blog-base.css`, scoped to `.kc-blog`, so nothing outside the blog changes.

- **Reading column:** 680 px, the legal page's column (`kc-policy-page.css`), about 70 characters at 20 px. On phones it is the screen minus the page gutter.
- **Body type:** `--kc-responsive-body-lg-*`, 18/26 on phones and 20/28 from 750 px, in `--kc-mapped-text-default-body` (76 % of navy by Day, 68 % of cream by Night). That is about 7.6:1 contrast by Day and 8.5:1 by Night on the page colour.
- **The editor's inline styles are neutralised inside the body only.** The 2024 articles set font sizes, link colours (`#004aad`, `#333399`), margins on every line and a 90 % width. The base CSS resets exactly those properties with `!important`, scoped to `.kc-blog__body`, and documents why. Without it no layout holds (D8).
- **Headings by their place.** Section headings use the h4 size (20 → 28) and sub-headings body-lg semibold. When a body uses `h1` for its sections (the nano article), `h1` becomes the section level and `h2` the sub level. The wellness article's `h5` reads as a sub-heading.
- **Quotes** are blocks with an accent rule, upright. Dawn's `.rte blockquote { display: inline-flex }` laid the nano quote out as two narrow columns side by side, and the base CSS undoes that.
- **Lists** use the legal page's indent, with markers in the caption colour.
- **Tables** scroll inside their own box on phones, with the legal page's row style. No article has one today.
- **Body images** are never wider than the file (480 and 600 px thumbnails today) and sit centred. They have no `width`/`height` in the body HTML, so they still shift the text when they load (D7).
- **Featured images** come from `image_url` + `image_tag` with the file's width and height, so they never jump.
- **Meta row:** date · reading time, author off as today. Reading time is words ÷ 200, rounded up (D9): nano 16 min, morning 4 min.
- **Links** are underlined in the heading colour, with a 2 px focus ring in `--kc-mapped-border-focus-strong`. On hover the text keeps its colour and the underline thickens in the accent blue (see §2a for why the site's hover colour is not used).
- **Sources** (the research-card pattern): the study links the body already contains, collected into one card at the end. The link text is the article's own anchor text, and the publisher name comes from the link's host (PubMed, PubMed Central, ScienceDirect, MDPI and nine more). Consumer sites (Healthline, Forbes, WebMD) are left out. Each source opens in a new tab, like the research cards. Nano shows 3 sources, wellness 3, fluoride 8, nootropics 18, morning none (so no card) (D4).
- **End CTA to the Duo** reuses copy that is already on the homepage (D5):
  - eyebrow "Biorhythmic oral care";
  - heading "Two formulas. One system. / Designed around you.";
  - text "Karmicare is a day-and-night oral care system designed around your mouth's 24-hour rhythm. Awake for activation. Asleep for restoration.";
  - the existing primary button `.karmicare__btn-primary` with "Begin your 60-Day Rhythm", linking to the Duo.
- **Related:** "Keep reading" with the three newest other articles (D6).
- **Index:** blog title as `h1`, then the cards, then numbered pagination.
- **Reduced motion:** every transition in the blog CSS switches off. Nothing in the blog animates on its own, and nothing switches Day/Night on scroll.

## 2a. Contrast in Day and Night

Computed from the token values (`fixture/tools/contrast.py`). Translucent text is blended over the surface it sits on: page, accent (the gradient's far end) and card. Text needs 4.5:1; focus rings and control edges need 3:1.

| Pair | Day: page / accent / card | Night: page / accent / card |
|---|---|---|
| Title, headings, links (`text-default-heading`) | 15.8 / 15.2 / 16.2 | 15.8 / 10.8 / 13.7 |
| Body, meta, captions (`text-default-body`) | 7.3 / 7.1 / 7.4 | 7.9 / 6.0 / 7.1 |
| Focus ring (`border-focus-strong`) | 15.8 / 15.2 / 16.2 | 15.8 / 10.8 / 13.7 |
| Rail dots, pagination edge (`border-control-default`) | 7.3 / 7.1 / 7.4 | 7.9 / 6.0 / 7.1 |
| Primary button label (normal / hover) | 15.8 / 13.7 | 15.8 / 13.8 |
| Site link hover `link-default-hover` (#7fb9ff), **not used** | **2.0 / 1.9 / 2.0** | 8.0 / 5.5 / 6.9 |

Night passes everywhere. Its weakest pair is body text on the accent end of the gradient, at 6.0:1. By Day only the site's link-hover colour fails, at 2:1, and the legal pages use it too. The blog CSS therefore does not change link colour on hover: the text stays navy or cream and the underline thickens in the accent blue (`shots/a-blog-hover-1440-day.png`). The quote rule and hairlines are decorative and carry no meaning. Whether the site-wide hover colour should change too is decision D15.

## 2b. The global lane's token change (landing desk note, 26 Oct)

`docs/blog/NOTE-GLOBAL-TOKEN-CHANGES.md`: the global lane (worktree `global-klaviyo-on`, not landed) makes `--kc-mapped-text-default-body` and `-caption` solid (Day `#191f38`, Night `#fffbf6`, new `-rgb` companions) and puts `proxima-nova` first in `--kc-font-role-backbone` and `--kc-font-use-heading/body/ui`. What the blog did about it:

- **Colours.** The blog CSS had no literal colour, alpha or "68 % / 76 % of the heading" value (checked with grep). Every text colour reads `--kc-mapped-text-default-heading`, `-body` or `-caption`, so the solid values arrive by themselves. Secondary text (date, reading time, publisher, list markers) now goes through one hook, `--kc-blog-soft-text`, which is the caption token.
- **Fonts.** Font families now come from the tokens: body `--kc-font-use-body`, title and body headings `--kc-font-use-heading`, the brief's button label `--kc-font-use-ui`, and eyebrows `--kc-font-use-brand` (Nunito). Before, they came from the theme variables `--font-body-family`, `--font-heading-family` and `--kc-font-family-Nunito`. The contents menu keeps the theme's own `.subtitle-item`, as the legal pages do.
- **Both states in the fixture.** `?tokens=next` applies the global lane's values exactly as in its diff, and `?soft=muted` additionally puts secondary text on the solid, softer `--kc-mapped-text-primary-default-muted` (`#2c3a60` / `#dddbd9`). Screens: `shots/d-tokens-{now,next,next-muted}-{top,body,sources,related}-{390,1440}-{day,night}.png`. Measured with `fixture/tools/probe-tokens.js`: now body/meta `rgba(25,31,56,0.76)` with "Proxima Nova" first; next `rgb(25,31,56)` with `proxima-nova` first; next-muted meta `rgb(44,58,96)`.
- **Findings.**
  1. **The token font stack in today's order breaks the line spacing on a machine with a desktop Proxima Nova.** That is the R70b problem, and the reason `kc-policy-page.css` stayed off the font tokens. In `d-tokens-now-body-1440-day.png` the nano article's paragraphs and quote close up: their line height is `normal` (T4) and the desktop font has no line gap. With `proxima-nova` first (`d-tokens-next-*`) the Typekit font wins and the lines open up again. So the blog must not land before the token change, or T4 must be fixed first. Both, preferably.
  2. **Solid text changes the hierarchy very little.** Date, reading time, publisher and the Keep reading meta stay lighter through size (13/14 against 18) and weight, and the standfirst through size. The muted variant is barely different by Day (`#191f38` against `#2c3a60`) and a little softer by Night. No new token is needed (D23).
  3. **Contrast (§2a) goes up.** Body and caption on page are 15.8:1 Day and Night. The contents links keep their 70 % (`.opacity-xl`, as on the legal pages), which is about 7:1 by Day.
- **Landing order.** If the token change lands first, the blog inherits it. If the blog lands first, nothing locks in the old alpha (there is no literal), but the font stack needs the token change for finding 1. So the blog lands **after or together with** the token change.

## 3. The directions

### D · Editorial, after Victor's reference (26 Oct, now the recommendation)

Victor: "design the exact layout of this blog for ours while staying in our branding. Pay attention to the image size, behaviour of content table and line height and styling of headers", with openai.com/index/scaling-storage-one-billion-users-part-two as the reference. Also: keep "Keep reading" and replace the "Two formulas" CTA with the homepage's end CTA. The reference was measured in an isolated Orca profile at 1440 and 390 (`fixture/tools/probe-ref*.js`, `shots/ref-openai-*.png`). Its cookie banner was left alone.

| | Reference (measured) | Ours (D) |
|---|---|---|
| Header | centred: date + category, title 48/55.7 (1.16) weight 500, standfirst, byline, a rule with "Listen" left and Share right | centred: date + "News", title on the h1 token (32 → 52) at line height 1.16, standfirst, a rule with the reading time left and **Share** right (the article template's existing share block). No byline: author stays off |
| Featured picture | wide figure 1280 px (80 px from each edge at 1440), 4 px corners | wide, up to 1280 px, never wider than the file (the nano file stays 520 px, D18), `radius-md`. On phones edge to edge |
| Body pictures | in the text column (676 px), about 88 px of air | in the 680 px column, `layout-3xl` (40 → 64) of air. On phones edge to edge. The original files, not the thumbnails (D7) |
| Text column | 676 px, centred on the page | 680 px, centred on the page |
| Body type | 17/28 (1.65), 24 px between paragraphs | 18 px (body-lg on phones, body-md from 750: both 18), **line height 1.6**, `layout-lg` (20 → 24) between paragraphs |
| Section heading | 30/39.6 (1.32) weight 500, 64 above, 24 below | 24 on phones (h3 token), 28 from 750 (h4 token), **line height 1.3**, weight 500, `layout-3xl` above, `layout-lg` below |
| Sub-heading | 22/27.7 weight 500 | h5 token (20 → 24) with its line height, weight 500, the same spacing |
| Contents | sticky list in the left margin (sticky 112 px from the top, about 210 px wide). Sections plus sub-sections indented 14 px, 12/15 type, the one being read in full colour, the rest at 60 %. No rules. Phones: a bar under the header naming the current section, which opens the list | the same behaviour. From 1200 px the list is sticky in the left margin (220 px), sections plus indented sub-sections, label-lg type (13/16), the current one in full colour and semibold, the rest at 70 % (the theme's `.opacity-xl`). "Sources" is the last item. Below 1200 px it is a bar that sticks under our floating navigation (veil and glass blur), names the section being read, opens the list, and closes after a choice. Fewer than three sections: no contents (`js/kc-blog-contents.js`) |
| End | related articles | **Sources** card (the studies the body links to), then the **homepage end CTA**: the `featured-product` section exactly as the homepage prints it ("Your welcome kit includes", the Loop plan picker, "Begin your 60-Day Rhythm", the three promises). Then **Keep reading** as before, with thumbnails |
| Index | — | the same rows as Keep reading (thumbnail, date · reading time, title, excerpt), under a centred "News" |

**Round 2 (Victor, 26 Oct): "use our table of content layout from legal pages", "images should have the width like the interaction section from openAI … the table of content disappears while it's on that large section".**
- **Contents = the legal pages' menu**, `sections/legal-toc-section.liquid`:
  - the same grid: a 1416 px page width with 20 px sides, a 250 px sidebar below 990 px and 332 px from 990 px, 16 px, then the text. At 1440 the text starts at 380 px, exactly as on the legal pages;
  - "On this page" and the links in the theme's own `.subtitle-item` and `.opacity-xl` (Nunito, uppercase, as on the legal pages);
  - a 1 px rule left of each link; the section being read in full colour with the 2 px rule;
  - sticky 100 px from the top;
  - top-level sections only, then "Sources";
  - at 640 px and below, the legal two-column list above the text.

  This replaces the reference's contents list and the phone bar (`d-article-body-1440-day.png`, `d-article-toc-390-day.png`).
- **Body pictures as wide as the reference's interactive figure:** 1280 px, centred on the page whatever the sidebar does (80 px from each edge at 1440), corners `radius-md`, edge to edge on phones. While a wide picture passes the sticky sidebar, the sidebar fades out and comes back after it (`d-article-image-1440-day.png`, `d-article-image-1100-day.png`).
- **Fonts: none changed.** Measured on the fixture and the live article (`fixture/tools/probe-fonts.js`). Both load the same Proxima Nova (kit `kss0igj`, 400/500/600) and Nunito Bold. The blog sets text in Proxima Nova like the site: title 52 px, body 18 px (live 16 px), body headings 28 px (live 44 px, Dawn's h2). The contents labels and the end CTA button are Nunito uppercase, as on the legal pages and the homepage. The only label style that differs from the site is the date row above the title: Proxima sentence case, 14 px, where the live article prints a 10 px uppercase date (D2).

**Screens:** `d-article-top-{390,750,1100,1440}-{day,night}.png`, `d-article-body-1440-day.png` (contents in the margin), `d-article-body-390-day.png` (the phone bar), `d-article-image-*.png`, `d-article-cta-1440-day.png` (homepage end CTA), `d-article-related-*.png`, `d-article-short-1440-day.png` (a wide 16:9 featured picture, no contents with two sections), `d-blog-top-*.png`.

**In the fixture the end CTA is static.** The live scripts are removed, so the Loop plan picker shows its Liquid state and the button does nothing. In Phase 2 it is the real section with its scripts. One theme change goes with it: `layout/theme.liquid` prints Loop's widget styles only on product, index and collection templates, so `article` joins that condition (D21; the Loop widget files themselves stay untouched).

### A · Quiet column (the legal family)

| | |
|---|---|
| **What it is** | The article reads like the legal pages: a title block fades page → accent, then the body fades accent → page in a 680 px text column. **Round 2 (Victor, 26 Oct):** (1) **Pictures leave the text column.** On phones they run edge to edge. From 990 px they fill the column with large rounded corners, and from 1200 px they reach 160 px further to the left, so a picture is 840 px wide next to 680 px of text. They load the original files (1920×1080 and 1200×802), not the 480/600 px thumbnails, so they stay sharp. (2) **"On this page" on the right**, as the legal pages' menu: an eyebrow, one link per section with a rule on its left, the section being read in full colour with a 2 px rule, "Sources" as the last item, sticky under the floating bar. On phones it is the legal pages' two-column list above the text. Articles with fewer than three sections get no menu. (3) **"Keep reading" stays a list**, with a thumbnail on each row (96 px on phones, 160 px from 750 px). The one memorable element is still the **Sources card** at the end; the CTA follows behind a rule. |
| **Index** | The same rows as "Keep reading": thumbnail, date · reading time, title, a two-line excerpt, an arrow. |
| **Has** | Featured picture (wide, out of the column) · body pictures out of the column · meta row · headings, lists, quotes, tables · "On this page" menu (right, legal style) · Sources card · end CTA · related rows with thumbnails |
| **Pros** | The same family as the legal pages (column, menu, rules), so the long-form pages read as one system. Pictures now carry the page without taking over the text. The menu helps the 16-minute nano article. Works the same with or without a featured picture. |
| **Cons** | The nano article's featured picture is a 520×416 file, so it cannot go wide and stays at its own size (D18). Body pictures have no width and height in the body HTML, so they still push the text down as they load (D7). |
| **Screens** | `a-article-top-*.png`, `a-article-image-{390,1100,1440}-*.png`, `a-article-body-1440-day.png` (menu), `a-article-nav-390-day.png` (phone menu), `a-article-related-1440-night.png`, `a-blog-top-1440-*.png` |

### B · Editorial with a reading rail

| | |
|---|---|
| **What it is** | A split hero: title, standfirst and meta on the left, the featured image in a 4:3 frame on the right from 990 px (under the title on phones). Below it the body column sits beside a **reading rail**, the one memorable element: the Figma "path stop" (a hairline with a dot per section, Shopify Store `3592:130087`). The section being read fills its dot. On phones and tablets the rail is an "On this page" disclosure above the body. An article with fewer than three sections gets no rail and keeps its column (the short articles). After the body come the Sources card, then a CTA card with the Duo packshot on the accent tint, then "Keep reading" as three 16:9 picture cards. Hero, rail, body, CTA and related all align to one frame (rail + gap + column). |
| **Index** | A lead article (picture left, text right from 990 px), then a grid of 16:9 picture cards with meta, title and a three-line excerpt (three columns from 990, two from 750). |
| **Has** | Hero image (large, cropped to 4:3) · meta row · headings, lists, quotes, tables · table of contents (rail and disclosure) · Sources card · CTA card with packshot · related picture cards |
| **Pros** | Best for the long articles: the nano article has five sections and 16 minutes of reading, and the rail shows where you are. The packshot CTA is the most persuasive end of the three. The index looks like a magazine. |
| **Cons** | Most new parts: a script for the rail (`kc-blog-toc.js`, about 90 lines) and three card types. The legacy stock photos (red lips, flowers) become big and prominent on the index and in the hero. The nano hero is cropped and slightly scaled up (520 → about 560 px at 1440). Two strong elements on one page (rail and packshot CTA) bend the "one memorable element" rule. |
| **Screens** | `b-article-top-1440-*.png`, `b-article-body-1440-day.png` (rail), `b-article-toc-390-day.png`, `b-article-cta-1440-*.png`, `b-blog-top-1440-day.png` |

### C · Research notebook

| | |
|---|---|
| **What it is** | The whole article sits on one "paper" card: the research-card surface (`surface/page-secondary`, radius lg, hairline, elevation md), floating over the page → accent → page gradient. Title, picture, body, Sources and the CTA are all on that card, quotes are accent panels inside it, and the CTA is an accent panel at its foot. The paper card is the one memorable element. "Keep reading" and the index use the Figma `WEB/Article card` (Shopify Store `3592:128276`): white card, hairline, a 16:9 picture, title, then meta and an arrow at the foot. |
| **Index** | A grid of those cards (three columns from 990, two from 750, one on phones), no excerpt, as in Figma. |
| **Has** | Hero image (contained, on the card) · meta row · headings, lists, quotes as panels, tables · Sources (a list on the card) · CTA panel · related Figma cards · no table of contents |
| **Pros** | The most "science" feeling: the article reads as a document on a desk, and it ties directly to the research cards on the homepage and PDP. The Figma article card gets used as designed. |
| **Cons** | On phones the card costs width: the text column is about 342 px instead of 350, and the card edge runs 8 px from the screen. By Night the white card becomes `#212a49`, darker than the accent gradient behind it, so the "paper" reads less clearly. A card inside a card (quote panel, CTA panel) is busier than A. |
| **Screens** | `c-article-top-1440-*.png`, `c-article-body-390-day.png`, `c-article-cta-1440-day.png`, `c-blog-top-1440-day.png` |

### Token mapping (all three)

| Role | Token |
|---|---|
| Page / accent surfaces and gradients | `--kc-mapped-surface-page`, `--kc-mapped-gradient-section-accent`; sections join the chain with `data-kc-surface` and `snippets/kc-surface.liquid` |
| Cards (Sources, C paper, B CTA, C article card) | `--kc-mapped-surface-page-secondary`, `--kc-mapped-border-primary-hairline`, `--kc-shape-radius-lg` / `-md`, `--kc-elevation-md` (C only) |
| Title | `--kc-responsive-h1-text-size` / `-line-height` / `-letter-spacing`, `--font-500-weight` |
| Section heading in the body | `--kc-responsive-h4-*` (letter-spacing `-h4-letter-spacing-sm`) |
| Sub-heading | `--kc-responsive-body-lg-*`, `--font-600-weight` |
| Body | `--kc-responsive-body-lg-*`, `--kc-mapped-text-default-body` |
| Meta, eyebrow, labels | `--kc-responsive-label-lg-*`, `--kc-mapped-text-default-caption` |
| Index card title | `--kc-responsive-h5-*`; B lead `--kc-responsive-h3-*` |
| Related / section heading | `--kc-responsive-h3-*` |
| Spacing | `--kc-responsive-spacing-layout-xs … 3xl`, `-section-xs`, `-section-comfortable`, `-page-gutter`, `-grid-gutter` |
| Links and focus | `--kc-mapped-text-default-heading`, `--kc-mapped-text-link-default-hover`, `--kc-mapped-border-focus-strong` |
| Quote rule | `--kc-mapped-surface-accent-default`, `--kc-shape-stroke-thick` |
| Rail dots (B) | `--kc-mapped-border-control-default`, `--kc-mapped-border-primary-rule`, `--kc-shape-radius-full` (a dot, not a button) |
| Buttons | existing `.karmicare__btn-primary` colours and states (`snippets/button-styles.liquid`), radius `--kc-shape-radius-sm` |

**Values without a token** (D16). Each is commented in the CSS.
- **Reading column 680 px:** the legal page's own value. It equals `size/grid/columns-6` at desktop, but that token is 361 px below 750, so it cannot be used directly.
- **Rail 240 px (B):** no grid token.
- **List indent 22 px:** the legal page's value.
- **Table minimum column 120 px.**
- **Rail dot 9 px.**
- **Packshot width 320 px (B).**
- **Long-form line height:** body-lg's token is 1.44. A long read would like 1.5–1.6, and there is no long-form line-height token in the theme. The library has a `long-form` font role (Noto Serif) but no matching line height. I kept the token rather than invent one.

## 4. Recommendation

**Update 26 Oct: Direction D**, the layout of Victor's reference in our tokens, with A's Sources card and Keep reading rows and the homepage end CTA. The reasoning below was written for A before the reference came in. It still explains why D keeps A's quiet type, the Sources card and the list-style related rows.

Earlier recommendation: **Direction A for the articles and the index.** The content decides it more than taste. The eight articles are legacy texts with small pictures, inline-style debris and many claims that need the evidence track (01-INVENTORY §6). A layout that puts their stock photos and titles big on the page (B, C) makes them louder before they are fixed. A is calm, joins the legal pages as one long-form family, gives the nano article's small image a natural place, and its one memorable element (the Sources card) points at the thing Karmicare wants to be known for: the studies.

Two things I'd take from the others, each as its own yes or no:
- **B's "On this page" disclosure** for long articles only (three or more sections), as a quiet list under the meta row and not as a rail. That helps the 16-minute nano article without a second memorable element (D3b).
- **C's Figma article card for the index**, once there are articles with good pictures. Today A's text rows are kinder to the legacy images (D1b).

## 5. Decision list

| # | Decision | Options | My recommendation |
|---|---|---|---|
| D1 | Direction for article and index | D (reference) · A · B · C | **D** |
| D19 | Body pictures in D | the text column, as the reference (as built) · 160 px further out on the left, as A round 2 | **The column**, as the reference. The featured picture is the wide one |
| D20 | Contents side | left margin, as the reference and the legal pages' own menu (as built) · right | **Left** |
| D21 | End CTA | the homepage's `featured-product` section in `templates/article.json`, plus `article` in theme.liquid's Loop-styles condition · A's text CTA | **The homepage section** |
| D22 | Line heights the tokens do not have | body 1.6, headings 1.3, title 1.16, as measured on the reference (as built) · the tokens' own (body-lg 1.44, h4 1.14) | **As built**, and add long-form line-height tokens to the KC library (with D16) |
| D23 | Secondary text once body and caption are solid | keep the caption token (solid, as built) · `--kc-mapped-text-primary-default-muted` (`?soft=muted`) | **Keep the caption token.** Size already carries the hierarchy, and muted is barely different by Day |
| D1b | Index cards | A text rows · C Figma cards with pictures | **A rows now**, C cards once the pictures are replaced |
| D2 | Labels and buttons | the brief: Proxima Nova, sentence case (default in the previews) · the site today: Nunito, uppercase, letter-spaced (`?labels=site`, `shots/a-article-cta-390-day-labels-site.png`) | **The brief's style** on the blog, with a separate yes for the rest of the site. Otherwise the blog's buttons differ from the header's "BEGIN NOW" |
| D3 | Standfirst under the title (`article.excerpt`) | show when the article has one · never | **Show**, but only after the nano excerpt is fixed ("Dive deep into the benefits of NASA's favorite supplement…", D11) |
| D3b | "On this page" for long articles | off · a disclosure under the meta row (from 3 sections) · B's rail | **Disclosure** |
| D4 | Sources card | yes, collected from the study links in the body (13 publisher hosts, consumer sites left out) · no | **Yes**, label "Sources" |
| D5 | End CTA | reuse the homepage copy above with "Begin your 60-Day Rhythm" · no CTA · different copy (needs Figma or your text) | **Reuse** |
| D6 | Related | "Keep reading" with the three newest other articles · none | **Yes** |
| D7 | Body images | as built in A round 2: the theme prints the original file instead of the thumbnail (`article.content \| replace: '_480x480.', '.' \| replace: '_600x600.', '.'`, served at most 1600 px wide, lazy), out of the column · plus a source-copy request to re-insert the pictures with width and height, so they stop shifting the text | **Both** |
| D8 | Editor inline styles | neutralise in CSS inside the body (as built) · clean the bodies in Admin (source-copy) | **CSS now**, cleanup when the articles are rewritten |
| D9 | Reading time | 200 words a minute, rounded up · leave out | **200 wpm** |
| D10 | Quotes | upright with an accent rule (A, B) · accent panel (C) · italic like today | **Upright with the rule** |
| D11 | The content itself (claims, dead links, competitor names, untranslated NL/FR) | route to the evidence track and source-copy (01-INVENTORY §5, §6, and §7 below) · also hide some articles until they are rewritten | **Route now. Hiding articles is your call**, and the layout should not wait for it |
| D12 | Index page size | 6 per page (today, so 8 articles = 2 pages) · 12 | **12**, so all eight fit on one page |
| D13 | `lang` on untranslated bodies | add `lang="en"` on the body wrapper on `/nl` and `/fr` until source-copy translates · leave | **Leave** for now: Liquid cannot tell whether an article body is translated. Better to translate |
| D14 | Day/Night | follows the clock with the manual override, as everywhere (no change) | no decision needed |
| D15 | Link hover by Day | blog: text keeps its colour, underline thickens in the accent (as built) · site's `link-default-hover` #7fb9ff (2:1 on cream) · also fix the site-wide hover (legal pages and others, another lane) | **As built for the blog**, and a separate item for the site-wide token |
| D17 | Glossary of terms used in an article | build a glossary block (definitions per article, shown under the menu or at the end) · leave out | **Waiting for Victor's reference page.** No article or theme file has glossary text today, and the lane writes no new copy |
| D18 | The nano featured picture (520×416, an outdated pump bottle, Victor 26 Oct) | **1** the Nano-HAp research card's picture `kc-research-nhap-tubules-2000x2400-v1.jpg` (Victor picked it 24 Oct, cf7d749; live on the homepage and PDP card), cropped to the 16:9 frame · **2** the homepage hero kit `kc-hero-kit.png` (3936×2960), whole on the accent tint · **3** the Duo packshot `karmicare-duo-pack-transparent.png` (2048²), whole on the accent tint. **4** the 2000×2000 master of the Kulal card's tubule picture, which Victor uploaded to Files on 26 Oct as `kc-research-nhap-dentinal-tubule-occlusion-2000_copy.png` (the 400 px `Picture_1.png` crop is too small; IMAGE-PLAN.md rejected the picture because it reads as a measured before/after, Victor's call), cropped to the 16:9 frame. Previews: `site/d-article-hero-{1,2,3,4}.html`, `shots/d-hero-option-*.png`. The featured picture is now always a 16:9 frame; the 2024 pictures already are | **Decided: 4** (Victor, 26 Oct: "ja die afbeelding is goed"). Victor sets it as the article's image in Admin (Online Store → Blog posts) once the new layout is live; the current Dawn template would show the square file full width |
| D16 | Values without a token (§3) | keep as commented literals · add tokens to the KC library first | **Literals now**, and add a long-form line-height token to the library when it is next exported |

## 6. New UI strings

**Proposed new keys** (EN only, for source-copy to add with NL/FR; `locales/*` belongs to that lane):

| Key | EN |
|---|---|
| `blogs.article.reading_time` | `{{ count }} min read` |
| `blogs.article.sources` | `Sources` |
| `blogs.article.on_this_page` | `On this page` (only with D3b) |
| `blogs.article.keep_reading` | `Keep reading` |
| `blogs.article.cta_eyebrow` | `Biorhythmic oral care` (homepage two-formulas subheading) |
| `blogs.article.cta_heading` | `Two formulas. One system.` (homepage) |
| `blogs.article.cta_heading_muted` | `Designed around you.` (homepage) |
| `blogs.article.cta_text` | `Karmicare is a day-and-night oral care system designed around your mouth's 24-hour rhythm. Awake for activation. Asleep for restoration.` (homepage hero) |

**Existing keys reused:**
- the CTA button: the key that holds "Begin your 60-Day Rhythm" in `locales/en.default.json` line 80, `…cta_rhythm_html`;
- "Opens in a new window.": `accessibility.link_messages.new_window`;
- pagination: `general.pagination.*`;
- the eyebrow link: `blog.title`.

No UI label goes into section settings: a setting equal to its schema default is not stored, so it cannot be translated.

## 7. Claim notes for the evidence track

Everything in 01-INVENTORY §6 stands. Building the previews added these, and the layout makes them more visible:

- **Nano excerpt** (the standfirst in all three directions): "Dive deep into the benefits of NASA's favorite supplement for oral health". This is an unsupported association, and it would be the first sentence under the title.
- **Nano body, under the founder quote:** "Read on and discover everything you need to know about this medical marvel for better teeth, bones and overall health. It's research-based and the claims are factual." This is a medical framing.
- **Nano founder quote:** "can fuse with your enamel, replace lost minerals, whiten teeth, reduce sensitivity … could be the answer to your dental health problems". It is a real quote with Victor's name, so a claim review should decide on it with Victor.
- **Article titles on the index and in "Keep reading":** "Benefits of Nootropics: Ease Stress, Boost Focus and Improve Mood." is a focus and mood claim in a title, and every card and related row repeats it. "5 Reasons You Should Avoid Fluoride in Toothpaste" and "Top Natural Whitening Toothpaste…" are the next to check.
- **Index excerpts:** whitening "Brighten your smile naturally with nontoxic, eco-friendly toothpaste" and fluoride "If you're fighting bad breath, hoping for whiter teeth, or trying to improve dental sensitivity…" show on every index card in A and B.

## 8. Phase 2 plan (after your yes)

- **Files:**
  - `sections/main-article.liquid` and `sections/main-blog.liquid` rewritten on the chosen direction;
  - `snippets/article-card.liquid` (or a new `kc-blog-card` snippet, if other templates keep Dawn's card);
  - the CSS moves into `assets/section-blog-post.css` and `assets/section-main-blog.css` (or one `kc-blog.css`), and the old Dawn rules they replace are removed;
  - `templates/article.json` and `templates/blog.json` only if blocks change;
  - Sources and related in Liquid (the study links are split out of `article.content` server-side, no script);
  - `kc-blog-toc.js` only with D3b.
- **Not touched:** `config/settings_data.json`, the Loop widget, `locales/*` (key list to the landing desk for source-copy), article content.
- **Checks:**
  - 360, 390, 750, 990 and 1440, in Day and Night, EN/NL/FR;
  - heading order, focus rings, contrast and alt text;
  - responsive image widths and no layout shift;
  - an article without a picture, the shortest and the longest article, and the index with 1, 2 and many articles;
  - fluid type on and off;
  - Theme Check 0 errors against the baseline.
