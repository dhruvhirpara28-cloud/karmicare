# R95 · the combined rating "4.7/5 (110)" on the hero badge and the PDP strip

**Date**: 30 Oct 2026 (Victor's decision of 29 Oct) · **Branch**: `karmicare/soft-launch-reviews` · **Base**: merge of `karmicare/soft-launch` @ c996d23 (32d41ab) · **Change**: 1413f48 · **Worker**: reviews lane, Orca task task_12110204c666

## 1. What changed, per file

| File | Change |
|------|--------|
| `templates/index.json` | hero block `testimonial_badge_h8d3WL`: `rating_text` "4.8 (234)" → "4.7/5 (110)". Nothing else. |
| `sections/hero-karmicare.liquid` | schema default of `rating_text` → "4.7/5 (110)", plus an `info` line naming the combined figure and the NL/FR path. Markup, CSS, rotation script untouched. |
| `snippets/product-category-strip.liquid` | a `rating_source` branch. `fixed` (default) prints the block's `rating_value` and `rating_count`; `metafield` prints `reviews.rating` / `reviews.rating_count` as before and stays hidden with no reviews. Both print `value/scale (count)`, scale 5 for fixed and `rating.scale_max` for the metafield. The `show_rating` checkbox stays the master switch. Same classes, same CSS, `role="img"` kept, no link. The accessible name now reads `accessibility.star_reviews_info` + `accessibility.total_reviews` (the literal word "reviews" the snippet printed before is gone, no new keys). The header comment names the current Figma frames (`4121:142856`, `4121:144413`, `4121:145970`). |
| `sections/main-product.liquid` | `category_strip` block schema: `rating_source` select (fixed / metafield, default fixed), `rating_value` text (default "4.7"), `rating_count` number (default 110). The `show_rating` info line that described only the metafield moved to the select's info. |
| `templates/product.subscription-item.json` | `category_strip_block` settings: `rating_source` "fixed", `rating_value` "4.7", `rating_count` 110 (next to the existing `show_rating` true). |
| `docs/reviews/PLAN.md` | changelog row (29 Oct), §0 bullet "Decided and built", §3 "Data path since R95", §6 "D-2 decided 29 Oct". |
| `docs/reviews/fixture/` | the liquidjs render and layout fixture (render.mjs, fixture.css, fixture.js, README.md, .gitignore for `out/`). Committed with this report. |

Not touched: `config/settings_data.json`, the Loop widget files, `locales/*.json`, `docs/localization/*`, `docs/source-copy/*`, `assets/kc-category-strip.css`, `assets/section-hero-karmicare.css`. No review section, no Judge.me markup; the `preview_badge` app block stays disabled.

## 2. The decimal separator

**Chosen for the strip: render from the settings and swap the point for a comma in Liquid** when `request.locale.iso_code` starts with `nl` or `fr` (`slice: 0, 2`, so `nl-BE` style codes work too). `rating_value` is a text setting ("4.7") because a Shopify `number` setting holds integers only and a `range` would need a step; the Liquid escapes and strips it. The same swap runs on the metafield path (`4.6` → `4,6`).

Why: the value is one number, not copy, so a source-copy registration per language would be three copies of the same figure to keep in step with the hero. The rule is already written in PLAN.md §1.2 (22 Oct). It works the same for whatever Victor later types into the setting.

**The hero stays as it was**: `rating_text` is a text setting that source-copy registers per language (`docs/localization/registration/plan-nl.json` and `plan-fr.json`, today "4,8 (234)"). Those files were not edited; the landing desk hands the new EN value "4.7/5 (110)" to source-copy, whose NL and FR value is "4,7/5 (110)". Until that lands, `/nl` and `/fr` keep showing the old translated value on the homepage. The fixture renders the NL badge with "4,7/5 (110)" to show the fit.

## 3. Verification

### 3.1 Theme Check

`shopify theme check --fail-level error` from the worktree root: exit 0, 490 files, 19 warnings (the baseline), 0 errors. Run after the merge, after the theme edits and before the commit.

### 3.2 Old value gone from the theme

`git grep -n '4.8 (234)' -- assets layout sections snippets templates locales config` returns nothing. The remaining hits are historical docs (PLAN.md, claims and localization records, utopia data).

### 3.3 Render proof: liquidjs fixture plus the Orca browser

`shopify theme dev` was not used: the worker sandbox cannot start a dev theme (and the brief allows the fixture route). **liquidjs cannot prove Shopify objects**: `product.metafields`, `request.locale`, `image_url`, `image_tag`, `placeholder_svg_tag`, `inline_asset_content`, `asset_url` and `t` are stubbed in `docs/reviews/fixture/render.mjs`. The stub for `escape` leaves `image_tag` output alone, as Shopify does (checked on the live homepage HTML, 30 Oct: the badge `<img>` prints as an element). What the fixture proves is the Liquid logic of the two files and the layout of the printed markup under the theme's own CSS (`base.css`, `kc-tokens.css`, `kc-surface.css`, `section-hero-karmicare.css`, `kc-category-strip.css`, the label size token from `layout/theme.liquid` L221 at its schema default 12 px, proxima-nova from Typekit, Nunito from Google Fonts in place of Shopify's font files). The first live render after landing should be grepped for "Liquid error".

**Liquid results** (`node render.mjs`, 38 PASS, 0 FAIL; `out/liquid-results.txt`):

| Case | Printed | Accessible name |
|------|---------|-----------------|
| fixed, EN (template values) | `4.7/5 (110)` | "4.7 out of 5 stars, 110 total reviews" |
| fixed, NL | `4,7/5 (110)` | "4,7 van de 5 sterren, 110 totaal aantal recensies" |
| fixed, FR | `4,7/5 (110)` | "4,7 sur 5 étoiles, 110 total des critiques" |
| metafield, EN (stub rating 4.6 / 5, count 12) | `4.6/5 (12)` | "4.6 out of 5 stars, 12 total reviews" |
| metafield, NL | `4,6/5 (12)` | "4,6 van de 5 sterren, 12 totaal aantal recensies" |
| metafield, no metafield | artwork only, no rating span | |
| fixed, count 0 · show_rating off | artwork only, no rating span | |
| hero EN (index.json) · hero NL ("4,7/5 (110)") | rating text as given; the whole badge is still the Trusted Professionals link; no link inside the rating line | |

Plus: the template JSON holds the four strip settings, index.json and the schema default hold "4.7/5 (110)", every strip variant has no `<a>`, the artwork keeps `role="img"` with its label, the rating span keeps `role="img"`, the star icon and the count span.

**Layout** (Orca browser tab, the fixture in iframes of the given width, checks run in the page, Day and Night by the `body` class as `day-night-mode.js` sets it):

| Width | Mode | Hero badge | Strip row |
|-------|------|-----------|-----------|
| 1440 | Day, Night | "4.7/5 (110)" one line, text 58.3×16.8 at 14 px, badge 225×72, link kept; NL "4,7/5 (110)" same size | one row in the 484 px buybox column (artwork 252.4, gap 16, rating 91.8); score Nunito 12 px 700 uppercase; count and star colours per mode |
| 750 | Night | one line, text 54.2×15.6 at 13 px, badge 225×72 (in flow, centred) | one row in 720 px |
| 390 | Day, Night | badge `display: none` (phones have no badge, D-3 of 20 Oct) | one row in 360 px: the row needs 356.2 on phones (gap 12) |
| 375 | Day | hidden | **wraps**: rating under the artwork (345 px column) |
| 320 | Day, Night | hidden | wraps (290 px column) |

The measured need of the strip row on phones is 356.2 px with "4.7/5 (110)" and 343.2 px with the old "4.8 (234)". With the page's 1.5 rem padding each side the row wraps below a 386 px viewport now, below 373 px before. So 390 and 393 phones keep one row, 375 phones (iPhone SE, mini) now get the rating on a second line, which `flex-wrap: wrap` in `kc-category-strip.css` handles cleanly (strip 49 px tall, star and text aligned left). Figma mobile `4121:145970` is 353 wide with "4.8 (234)" on one row. Not changed here (the brief keeps the strip CSS); if Victor wants one row on 375 the options are letting the artwork shrink on phones (`flex-wrap: nowrap` and `min-width: 0` on the brand, about 5 % smaller) or a smaller gap.

Screenshots (gitignored, in the worktree):
- `docs/reviews/shots/r95-1440-day.png`
- `docs/reviews/shots/r95-1440-night.png`
- `docs/reviews/shots/r95-390-320-day-night.png` (390 Day, 390 Night, 320 Day, 320 Night side by side)
- `docs/reviews/shots/r95-375-day-750-night.png`
- `docs/reviews/shots/probe-1440-day.png` (first run, before the stubs were corrected; kept for the record)

Re-run: `cd docs/reviews/fixture && npm install --no-save liquidjs@10.21.0 && node render.mjs`, then open `out/frame-1440.html` or `out/frame-multi.html?frames=390:day,390:night,320:day,320:night&h=560`.

### 3.4 Figma

`4121:142856` (EN strip, 448 wide) and `4121:145970` (mobile, 353 wide) show star + "4.8" + "(234)" on one row; `4121:34333` (badge, 307×72) shows "4.8 (234)" above the heading. The "/5" is not in Figma: it is Victor's wording of 29 Oct. In the strip it inherits the uppercase Label/Small style and renders as digits, so nothing looks different from the number itself; in the badge it is the same 14 px body text as before. Not a blocker. The rating column in the Figma badge is 206 px; ours is 155 (heading max-width 200 from R49), unchanged by R95.

## 4. Not proven, and open points

- **Shopify-only objects**: `request.locale.iso_code`, the metafield objects, `image_tag` with its named arguments and the translation filter were stubbed. A dev theme or the first landed render is the real proof (grep "Liquid error", check `/nl` and `/fr`).
- **Theme editor**: the three new block settings were not opened in the editor (no dev theme). Their schema is plain Shopify JSON and Theme Check accepts it.
- **NL and FR hero value**: needs the source-copy registration ("4,7/5 (110)"); the homepage on `/nl` and `/fr` shows "4,8 (234)" until then.
- **375 px phones**: the strip rating moves under the artwork (§3.3). Victor's call whether that stands.
- **Observed, pre-existing**: in the fixture the count's colour token (`--kc-mapped-text-default-body`) computes to the same value as the heading colour in both modes, so the count is not lighter than the value as Figma's 68 % opacity shows. Not touched by R95.
