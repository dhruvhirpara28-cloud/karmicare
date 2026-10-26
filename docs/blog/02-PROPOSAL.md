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
- **Links** are underlined in the heading colour, with the KC hover colour and a 2 px focus ring in `--kc-mapped-border-focus-strong`.
- **Sources** (the research-card pattern): the study links the body already contains, collected into one card at the end. The link text is the article's own anchor text, and the publisher name comes from the link's host (PubMed, PubMed Central, ScienceDirect, MDPI and nine more). Consumer sites (Healthline, Forbes, WebMD) are left out. Each source opens in a new tab, like the research cards. Nano shows 3 sources, wellness 3, fluoride 8, nootropics 18, morning none (so no card) (D4).
- **End CTA to the Duo** reuses copy that is already on the homepage (D5):
  - eyebrow "Biorhythmic oral care";
  - heading "Two formulas. One system. / Designed around you.";
  - text "Karmicare is a day-and-night oral care system designed around your mouth's 24-hour rhythm. Awake for activation. Asleep for restoration.";
  - the existing primary button `.karmicare__btn-primary` with "Begin your 60-Day Rhythm", linking to the Duo.
- **Related:** "Keep reading" with the three newest other articles (D6).
- **Index:** blog title as `h1`, then the cards, then numbered pagination.
- **Reduced motion:** every transition in the blog CSS switches off. Nothing in the blog animates on its own, and nothing switches Day/Night on scroll.

## 3. The three directions

### A · Quiet column (the legal family)

| | |
|---|---|
| **What it is** | The article reads like the legal pages. A title block fades page → accent, then the body fades accent → page in one centred 680 px column. The featured image sits under the title at no more than its own width (the nano image stays 520 px, the others fill the column). The one memorable element is the **Sources card** at the end: a white research card with the studies as rows. The CTA follows behind a rule, then "Keep reading" as text rows with an arrow. |
| **Index** | Text rows on hairlines: date · reading time, title, a two-line excerpt, an arrow. No pictures. |
| **Has** | Hero image (small, under the title) · meta row · headings, lists, quotes, tables · Sources card · end CTA · related rows · no table of contents |
| **Pros** | Calmest of the three, and the same family as the legal pages, so the long-form pages read as one system. The weak legacy pictures (480 px thumbnails, stock photos) take the least room, and the nano article's small hero stops looking broken. Fewest new parts: one new CSS file and the Sources card. Works the same with or without a featured image. |
| **Cons** | The index has no pictures, so it looks more like a list of documents than a magazine. At 1440 a lot of the page is empty margin around the column. The 16-minute nano article has no way to jump to a section. |
| **Screens** | `a-article-top-*.png`, `a-article-sources-1440-day.png`, `a-blog-top-1440-day.png` |

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

**Direction A for the articles and the index.** The content decides it more than taste. The eight articles are legacy texts with small pictures, inline-style debris and many claims that need the evidence track (01-INVENTORY §6). A layout that puts their stock photos and titles big on the page (B, C) makes them louder before they are fixed. A is calm, joins the legal pages as one long-form family, gives the nano article's small image a natural place, and its one memorable element (the Sources card) points at the thing Karmicare wants to be known for: the studies.

Two things I'd take from the others, each as its own yes or no:
- **B's "On this page" disclosure** for long articles only (three or more sections), as a quiet list under the meta row and not as a rail. That helps the 16-minute nano article without a second memorable element (D3b).
- **C's Figma article card for the index**, once there are articles with good pictures. Today A's text rows are kinder to the legacy images (D1b).

## 5. Decision list

| # | Decision | Options | My recommendation |
|---|---|---|---|
| D1 | Direction for article and index | A · B · C (or a mix) | **A** |
| D1b | Index cards | A text rows · C Figma cards with pictures | **A rows now**, C cards once the pictures are replaced |
| D2 | Labels and buttons | the brief: Proxima Nova, sentence case (default in the previews) · the site today: Nunito, uppercase, letter-spaced (`?labels=site`, `shots/a-article-cta-390-day-labels-site.png`) | **The brief's style** on the blog, with a separate yes for the rest of the site. Otherwise the blog's buttons differ from the header's "BEGIN NOW" |
| D3 | Standfirst under the title (`article.excerpt`) | show when the article has one · never | **Show**, but only after the nano excerpt is fixed ("Dive deep into the benefits of NASA's favorite supplement…", D11) |
| D3b | "On this page" for long articles | off · a disclosure under the meta row (from 3 sections) · B's rail | **Disclosure** |
| D4 | Sources card | yes, collected from the study links in the body (13 publisher hosts, consumer sites left out) · no | **Yes**, label "Sources" |
| D5 | End CTA | reuse the homepage copy above with "Begin your 60-Day Rhythm" · no CTA · different copy (needs Figma or your text) | **Reuse** |
| D6 | Related | "Keep reading" with the three newest other articles · none | **Yes** |
| D7 | Body images | layout as built (never stretched, they still shift on load) · plus a source-copy request to re-insert the images at full size with width and height | **Both** |
| D8 | Editor inline styles | neutralise in CSS inside the body (as built) · clean the bodies in Admin (source-copy) | **CSS now**, cleanup when the articles are rewritten |
| D9 | Reading time | 200 words a minute, rounded up · leave out | **200 wpm** |
| D10 | Quotes | upright with an accent rule (A, B) · accent panel (C) · italic like today | **Upright with the rule** |
| D11 | The content itself (claims, dead links, competitor names, untranslated NL/FR) | route to the evidence track and source-copy (01-INVENTORY §5, §6, and §7 below) · also hide some articles until they are rewritten | **Route now. Hiding articles is your call**, and the layout should not wait for it |
| D12 | Index page size | 6 per page (today, so 8 articles = 2 pages) · 12 | **12**, so all eight fit on one page |
| D13 | `lang` on untranslated bodies | add `lang="en"` on the body wrapper on `/nl` and `/fr` until source-copy translates · leave | **Leave** for now: Liquid cannot tell whether an article body is translated. Better to translate |
| D14 | Day/Night | follows the clock with the manual override, as everywhere (no change) | no decision needed |
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
