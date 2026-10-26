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
