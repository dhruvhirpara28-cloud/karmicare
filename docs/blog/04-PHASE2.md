# Blog lane · 04 · Phase 2: direction D in the theme

Victor approved direction D and T1–T4 on 26 Oct (02-PROPOSAL.md, 03-TYPE-AUDIT.md). The four locale keys came from source-copy on `karmicare/soft-launch` f280dae (merged in 75d0e00).

**Landing order:** after the global lane's token change (solid body/caption text, `proxima-nova` first; NOTE-GLOBAL-TOKEN-CHANGES.md). With today's font order a desktop Proxima Nova can win the font stack, and the body's line spacing closes up (02-PROPOSAL §2b).

## What changed

| File | Change |
|---|---|
| `sections/main-article.liquid` | Rewritten on D:
<ul><li>header: homepage eyebrow, title, standfirst (`article.excerpt`), and a rule with date, reading time and Dawn's Share button;</li><li>the featured picture in a wide 16:9 frame;</li><li>the legal contents menu;</li><li>the body with the original files instead of the 480/600 px thumbnails;</li><li>Sources, built server-side from the body's study links;</li><li>Keep reading, the three newest other articles.</li></ul>The blocks keep their editor role (picture on/off, date, Share, content); app blocks print after the body. Dawn's comment block, the JSON-LD and the schema are unchanged. |
| `sections/main-blog.liquid` | Centred title and rows with thumbnails, 12 per page (D12). The old settings stay in the schema, so saved values still validate. |
| `snippets/kc-blog-row.liquid` | New: one row (thumbnail, date · reading time, title, excerpt, arrow) for Keep reading and the index. |
| `assets/kc-blog.css` | New: all blog styles, scoped to `.kc-blog`, from the tokens. T1 body-md, T2 h3 section headings, T3 token line heights plus 1.6 for running text, and T4 fixed: the line height now also applies to `p`, `li` and `blockquote`. |
| `assets/kc-blog-contents.js` | New: the menu (a link per section plus Sources, the current one marked, eases there like the legal pages, hides while a wide picture passes). |
| `templates/article.json` | Adds the homepage's `featured-product` section (end CTA) after `main`, copied from `templates/index.json` `featured_product_3XpDKw`. |
| `layout/theme.liquid` | `article` added to the two Loop conditions (widget CSS/JS, `loop-widget.css.liquid` styles) so the end CTA's plan picker works. Loop's own files are untouched. |
| `assets/section-main-blog.css` | Removed: Dawn's index grid, no longer referenced (`git grep section-main-blog -- . ':!docs'` → 0). |

**Kept:**
- `section-blog-post.css`: Dawn's comment form still uses it.
- `snippets/article-card.liquid` and `component-article-card.css`: search results and `featured-blog` still use them.

## Checks

- **Theme Check** (`shopify theme check --fail-level error`): exit 0, **0 errors, 19 warnings** (the baseline). The only warning in the blog files is Dawn's existing `anchorId` in the comment block.
- **Real Liquid render.** `docs/blog/fixture/render-liquid.mjs` renders the theme's own `main-article`, `main-blog`, `kc-blog-row`, `share-button` and `pagination` with liquidjs 10.21.0 and the live articles. `build.py` puts the output in the live page shell (`site/theme-*.html`).
  - Reading times: nano 16 min, short 4, headaches 6.
  - Sources: nano 3, headaches 1, short none (no card).
  - Keep reading: 3 rows. No missing translation, no Liquid error, no thumbnail URL left.
- **Shots** (`docs/blog/shots/theme-*.png`, gitignored, 94 in all). Shot with the global lane's token values (`?tokens=next`):
  - 90 from `tools/shots.py <page> theme`: 360, 390, 750, 990 and 1440 px, Day and Night; the nano article (long, picture), the morning article (short, no menu), the headaches article without a picture, and the index with 8, 2 and 1 articles; nano body, picture, Sources, Keep reading and end CTA at 390, 990 and 1440;
  - 4 for NL and FR: `theme-article-noimage-{nl,fr}-top-360-day.png` and `theme-article-nano-{nl,fr}-related-1440-day.png`.
- **Locales:** NL and FR labels from source-copy render and fit ("Op deze pagina", "Bronnen", "Lees verder", "min lezen"; "Sur cette page", "min de lecture").
- **Earlier checks that still hold** (02-PROPOSAL §2a and D):
  - contrast in Day and Night;
  - focus rings on links, the menu and Share;
  - featured picture with width and height (no shift), body pictures lazy at most 1600 px wide;
  - tables scroll in their own box;
  - reduced motion: no transitions, the menu jumps instead of easing.

## Not in this lane / still open

- **Admin (Victor):** set the nano article's image to `kc-research-nhap-dentinal-tubule-occlusion-2000_copy.png` once this is live (D18). Fix or redirect the 7 dead Webflow links (01-INVENTORY §5).
- **The template's Share label** is the block setting "Share" in `templates/article.json`, translated through Translate & Adapt like before (not a locale key).
- **The fixture's dates print in English;** Shopify's `time_tag` localizes them on the store.
- **Evidence track:** the claims in the article bodies (01-INVENTORY §6, 02-PROPOSAL §7).
- **KC library:** add a long-form line-height token (1.6) and point `--kc-blog-long-line-height` at it (D22).
- **D17 glossary:** waits for Victor's reference.

## R90b: Astra's REWORK fixed (26 Oct)

Report: `docs/runtime-review/R90-BLOG-LAYOUT-ASTRA.md`. Note: `docs/blog/REWORK-R90.md`.

### B1: wide body pictures were clipped

**Cause:** the paragraph reset `:is(p, …, div[style])` had specificity 0,2,1 and beat the breakout.

**Fix in `assets/kc-blog.css`:**
- The reset is now `:where(…)`, at 0,1,0. `!important` still beats the inline styles.
- The breakout is measured in `cqw` of `.kc-blog__main`, now a size container: the page width without a scrollbar, where `100vw` included it.
- `overflow-x: clip` is gone, so nothing is hidden any more.

**Measured** (`fixture/tools/r90_check.py`): real picture edges in the nano (EN/NL/FR), short and headaches articles. Each picture is centred at its expected width, and the page never scrolls sideways (`scrollWidth` = viewport):

| Viewport | Picture left → right |
|---|---|
| 360 | 0 → 360 |
| 390 | 0 → 390 |
| 750 | 32 → 718 |
| 990 | 32 → 958 |
| 1440, 1920 px files | 80 → 1360 |
| 1440, 1200 px nano files (not stretched) | 120 → 1320 |

### B2: body pictures shifted the layout

**Fix in `sections/main-article.liquid`:**
- All 16 body pictures of the 8 articles are also in this store's Files at full size (`fixture/tools/probe-bodyimgs.js`).
- The section looks each one up with `images['name.jpg']` and prints it with `image_tag`: the file's width and height, a srcset up to 1920, lazy, the body's alt kept.
- A picture not in Files keeps its tag, gets the original file instead of the thumbnail, and loads lazily.
- The CSS sets no `width`, so the attribute sizes the box before the file loads.

**Measured** (picture not yet loaded, box against the file ratio):

| Viewport | File | Box | Ratio check |
|---|---|---|---|
| 390 | 1200×802 | 390×261 | equal |
| 1440 | 1200×802 | 1200×803 | ±1 px |
| 1440 | 1920×1080 | 1280×721 | ±1 px |

**Contents jump:** one smooth scroll now lands exactly on the 90 px scroll margin (before: 944 px off without re-aiming). The corrective re-aiming is removed from `kc-blog-contents.js`.

### B3: six h1s in the nano article

**Fix in `sections/main-article.liquid`:**
- The title is the only h1.
- A body that uses h1 for its sections moves down one level.
- Each heading is at most one level below the one before it (the title counts as h1), and at most h4.
- A heading with no text becomes a paragraph. The wellness article opens with an h5 holding only `&nbsp;`.
- Wording and order are unchanged: the nano headings' text equals the source, 11 of 11.

**Rendered body levels:**

| Article | Levels |
|---|---|
| nano | 23232333322 |
| headaches | 232322332 |
| morning | 2333332333 |
| wellness | 22222 |

No skips, no empty headings, tags balanced, one h1 in EN/NL/FR. The contents still list the 5 nano sections plus Sources. Without JS the server HTML has the same headings and the empty menu is hidden.

### N1: embeds and small pictures

- A legacy 560×315 iframe stays inside the column: 350×197 at 390 and 680×383 at 1440.
- An 80×40 picture stays 80 px wide.

### N2: focus after a contents jump

Focus moves to the target heading (`tabindex="-1"`, `focus({preventScroll: true})`), with no ring for a mouse click and the focus ring for keyboard.

### Verification

- **Theme Check:** exit 0, 0 errors, 19 warnings (baseline).
- **Shots:** 110 `theme-*` shots at 360, 390, 750, 990 and 1440, Day and Night. The nano body, picture, Sources, Keep reading and end CTA are shot at all five widths.

## R90c: B4, the fallback for pictures not in Files (26 Oct)

Report: `docs/runtime-review/R90B-BLOG-LAYOUT-ASTRA.md`.

**Problem:** for a picture not found in Files, the fallback also stripped `_480x480` and `_600x600` from the tag, so a valid external URL ending in `_480x480.jpg` became a missing file.

**Fix in `sections/main-article.liquid`:**
- The lookup tries the file's own name first, then the name without the thumbnail suffix.
- A picture that is still not found keeps its tag exactly as written.
- It only gets `loading="lazy"` and `decoding="async"`, and only when the tag has neither.

**Retested** with `fixture/tools/probe-b4.js` on `site/theme-article-b4.html`, a test article rendered by `render-liquid.mjs`. All three pictures load and decode:

| Picture | Result |
|---|---|
| A valid local URL `kc-b4-external_480x480.png`, not in Files | src untouched, loads at 1440×900 |
| The nano thumbnail `charcoal-toothbrushes_600x600.jpg`, in Files | resolved to the Files file with width/height 1200×802, loads |
| An external tag with its own `loading="eager"` | src untouched, no duplicate attribute, loads |

**Regression:** `r90_check.py` ran 25 cases (nano EN/NL/FR, short, headaches × 360/390/750/990/1440). Picture edges, reserved heights, one h1 and no sideways scroll are unchanged. Theme Check: exit 0, 0 errors, 19 warnings in the theme. Astra's untracked `docs/runtime-review/r90b-tmp` export adds lint noise in this worktree only.

## Hotfix: Liquid error in place of the body pictures (26 Oct, after landing)

**Found on the live store** (release 12, main 2f58500), checked with `fixture/tools/probe-live*.js`. Every body picture of every article printed `Liquid error (sections/main-article line 120): invalid url input`. The Files lookup `images['name.jpg'] | image_url` worked in the local liquidjs render, where both are stubbed, but fails on Shopify. Everything else was live as built:
- one h1, headings 23232333322;
- "On this page" / "Op deze pagina";
- Sources 3, Keep reading 3, the end CTA;
- the index with 8 rows;
- the global tokens live.

**Hotfix:** the lookup is removed. Every body picture keeps its tag exactly as the article wrote it, with lazy loading and async decoding added when missing. The rendered tags equal the source (nano 4 of 4, morning 2 of 2), there is no Liquid error, and Theme Check gives 0 errors and 19 warnings.

**Reopened: R90 B2** (pictures reserve no space). The way back is width/height for the 16 known files, checked on a real Shopify render (dev theme or preview) before it lands; or source-copy re-inserts the pictures with their sizes (D7).

**Lesson:** the liquidjs fixture cannot prove Shopify-only objects and filters (`images`, `image_url` on Files). A change that relies on them needs a real Shopify render.
