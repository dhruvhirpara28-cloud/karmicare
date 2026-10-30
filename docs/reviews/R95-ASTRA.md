# Astra review R95 · the combined rating "4.7/5 (110)" on the hero badge and the PDP strip

**Verdict: APPROVE** (no blocker; two should-fix items, neither in the shipped path, and one layout decision for Victor).

**Date**: 30 Oct 2026, 01:40 CET · **Branch**: `karmicare/soft-launch-reviews` · **Range**: 32d41ab..af5da5c (1413f48 theme change, af5da5c report and fixture) · **Base**: merge of `karmicare/soft-launch` @ c996d23, not reviewed · **Reviewer**: Astra (Orca task task_d07808f28574), read-only on theme files, effort xhigh.

Read first: `AGENTS.md`, `docs/reviews/R95-REPORT.md`, `docs/reviews/PLAN.md` §0, §2, §3, §6 (D-1, D-2, D-3). Victor's decision of 29 Oct 2026 as briefed: exactly two places, hero badge and PDP strip inside the buybox, "4.7/5 (110)" EN and "4,7/5 (110)" NL/FR, no explanation, no link on the rating, badge keeps its Trusted Professionals link. Count 110 reviews, 522 stars, mean 4.745 (rounds to 4.7).

## Findings

| # | Severity | Where | Finding |
|---|----------|-------|---------|
| 1 | should-fix (dormant path) | `snippets/product-category-strip.liquid:37` | On the metafield path `rating_max = rating.scale_max \| default: 5` very likely prints **5.0**, not 5, on Shopify. The fixture stubbed `scale_max: 5` as an integer, so liquidjs could not show it. Shopify stores the rating type as `{"scale_min": "1.0", "scale_max": "5.0", "value": "4.5"}`, and Dawn's own rating block in this repo prints `rating.value.scale_max` straight (`sections/main-product.liquid:669`, `snippets/card-product.liquid:197`), which is the familiar "4.5 / 5.0" on Dawn stores. With the select on "metafield" the strip would read "4.6/5.0 (12)" and the accessible name "4.6 out of 5.0 stars", unlike the fixed path's "4.7/5 (110)". Nothing ships through this path (the template says `fixed`), so not blocking. Smallest fix: `assign rating_max = rating.scale_max \| default: 5 \| round` (round with no argument returns an integer, and still gives 5 when the metafield has no scale). Prove it on the first real render with the select set to metafield on a product that has a rating. |
| 2 | should-fix (sequencing, not code) | `templates/index.json:55`, `docs/localization/registration/plan-nl.json:162`, `plan-fr.json:162` | The NL and FR values of the hero `rating_text` are Shopify translations that source-copy registers; they still say "4,8 (234)". After this lands, `/nl` and `/fr` show either the old "4,8 (234)" (if Shopify keeps the outdated translation) or the EN "4.7/5 (110)" with a point (if it drops it), while the NL/FR PDP strip already says "4,7/5 (110)". `R95-REPORT.md` §2 and §4 name this. The landing desk should ship this commit and the source-copy registration "4,7/5 (110)" in the same step, or accept the gap and say for how long. No change to the diff. |
| 3 | nit / Victor's call | `assets/kc-category-strip.css:4-10` (not in the diff) | Confirmed: the strip row wraps under a 386 px viewport, so on 375 px phones (iPhone SE, 12/13 mini) and at 320 the rating sits on a second line under the artwork. 390 and up keep one row. The wrapped state is clean (strip 345×49 at 375, 290×49 at 320, star and text left-aligned, nothing clipped, nothing overlapping) and I do not rate it a blocker: the old text fitted 375 by 2 px only (343.2 of 345). If Victor wants one row on 375, the smallest CSS fix is in §5 below (measured, not implemented). Figma mobile `4121:145970` is 353 wide with the shorter "4.8 (234)" on one row, so Figma does not settle it. |
| 4 | nit (noted, not blocking) | `templates/index.json:55`, strip line 77 | The "/5" is Victor's wording of 29 Oct, not Figma's (`4121:142856` and `4121:34333` show "4.8 (234)"). Rendered as digits in the strip's uppercase label style and as the badge's 14 px text, it reads as the number itself. Recorded in `PLAN.md` §3. |
| 5 | nit (fixture only) | `docs/reviews/fixture/fixture.js:69` | The INFO line "the row wraps below a N viewport" adds the phone gap only when the frame is a phone frame; at 1440 it prints "1316.2" and at 750 "390.2", which mean nothing (the desktop column is fixed at 48.4 rem). Read that line from the 390 or 375 frame only, as the R95 report did. Optional: print it only under 750. |
| 6 | observation (pre-existing, out of scope) | `templates/product.json:21-24` | The default product template has no `category_strip` block and is untouched by R95, so nothing to make consistent. Its Judge.me `preview_badge` app block is **enabled** there (the subscription-item template has it `"disabled": true`). Any product that would use the default template shows Judge.me's own product rating, a third figure. No product does today as far as this lane knows (the Duo product uses `product.subscription-item.json`). Noted for the PLAN §7 switch list, not for R95. |

Everything else in the brief checks out; the evidence per item follows.

## 1. Liquid in `snippets/product-category-strip.liquid`

Read line by line (L27-55 logic, L69-80 markup), plus the fixture (`node render.mjs`: 38 PASS, 0 FAIL, re-run by me at 01:17 CET with a fresh `liquidjs@10.21.0`).

| Case | Result | How I know |
|------|--------|------------|
| fixed path, template values | `4.7/5 (110)`, aria "4.7 out of 5 stars, 110 total reviews" | fixture `strip fixed-en` |
| metafield path, rating 4.6 / count 12 | `4.6/5 (12)` in the fixture; **on Shopify likely `4.6/5.0 (12)`** (finding 1) | fixture `strip metafield-en`; Dawn's own rating markup in this repo |
| show_rating off | artwork only, no rating span | fixture `strip fixed-off-en`; L30 gates the whole block |
| count 0 | artwork only | fixture `strip fixed-count-0-en`; L42 `rating_count > 0` |
| empty `rating_value` ("" or spaces) | `strip` makes it "", `!= blank` false, hidden | L40-42, by reading; Liquid `strip` on nil gives "" |
| metafield object with `scale_max` 5 | `/5` (fixture) | L37 |
| metafield object without `scale_max` | `default: 5` catches nil, `/5` | L37, by reading |
| no metafield at all | `rating` nil, `!= blank` false, hidden; `rating_count` nil → `plus: 0` → 0 | fixture `strip metafield-empty-en`, L32-34 |
| `request.locale.iso_code` en | point kept | fixture |
| nl, fr | comma, `4,7` | fixture `fixed-nl`, `fixed-fr`, `metafield-nl` |
| nl-BE, fr-BE | `slice: 0, 2` gives "nl" / "fr", comma | L50, by reading (Shopify's iso_code is lowercase language, optionally `-REGION`) |
| de | "de", no swap, point kept | L51 |

- `block.settings.rating_count | plus: 0`: a `number` setting is an integer in Liquid, `plus: 0` leaves it; an unset or cleared setting is nil, and Shopify's `plus` turns nil into 0, so the comparison `> 0` is always integer against integer. Behaves.
- `rating.rating | round: 1 | append: ''`: Shopify's `round: 1` returns a float; Ruby prints 4.6 as "4.6", never "4.60". It does print 4.0 as "4.0" and 5 as "5" (an integer stays an integer), so a product rated exactly 4 would read "4.0/5": pre-existing (the old line did the same), harmless. `append: ''` makes it a string so the later `replace` is safe.
- The comma swap touches `rating_value` only (L52). `rating_count` is a separate integer variable printed as `{{ rating_count }}`; `rating_max` is never swapped either (a "5.0" from finding 1 would show a point in NL, one more reason for `round`).
- `escape` runs before the swap, so `&`, `<` typed into the text setting cannot break the attribute; the `t:` interpolation does not escape again, so no double escape.
- The `# comment` line inside `{%- liquid -%}` is valid Shopify Liquid (Theme Check passes it).
- What liquidjs cannot prove (stubs: `product.metafields`, `request.locale`, `t`, `inline_asset_content`, `asset_url`, `image_url`, `image_tag`, `placeholder_svg_tag`, `escape` on `image_tag` output): on Shopify the only behaviour I expect to differ is finding 1 (scale_max as 5.0). The `t` filter with named arguments, `request.locale.iso_code` and `metafield.value` on a rating type are all standard Dawn usage already present in this theme. First landed render: grep "Liquid error" on `/`, `/products/karmicare-biorhythmic-oral-care-system`, `/nl/...`, `/fr/...`.

## 2. Schema in `sections/main-product.liquid`

L1337-1372 read. `show_rating` keeps `default: true`, its old info line now lives on the select (moved, not duplicated: `git grep "Reads the product's reviews.rating"` finds nothing). `rating_source` is a `select` with two options, `default: "fixed"`, matches the template value. `rating_value` is `text`, default `"4.7"`, matches. `rating_count` is `number`, default `110` as a JSON integer (not a string), matches. The hero `rating_text` default is `"4.7/5 (110)"` (`sections/hero-karmicare.liquid:1090`) and matches `templates/index.json:55`.

```
shopify theme check --fail-level error     (worktree root, 01:16 CET)
490 files inspected with 19 total offenses found across 14 files.
19 warnings.
exit 0
```

`.theme-check.yml` is not in the range.

## 3. Accessible name

`aria-label="{{ 'accessibility.star_reviews_info' | t: rating_value: rating_value, rating_max: rating_max }}, {{ rating_count }} {{ 'accessibility.total_reviews' | t }}"` (L73). Keys exist, no new key added, `locales/` not in the range:

```
locales/en.default.json:193  "total_reviews": "total reviews"
locales/en.default.json:194  "star_reviews_info": "{{ rating_value }} out of {{ rating_max }} stars"
locales/nl.json:193          "total_reviews": "totaal aantal recensies"
locales/nl.json:194          "star_reviews_info": "{{ rating_value }} van de {{ rating_max }} sterren"
locales/fr.json:193          "total_reviews": "total des critiques"
locales/fr.json:194          "star_reviews_info": "{{ rating_value }} sur {{ rating_max }} étoiles"
```

Rendered (fixture): EN "4.7 out of 5 stars, 110 total reviews", NL "4,7 van de 5 sterren, 110 totaal aantal recensies", FR "4,7 sur 5 étoiles, 110 total des critiques". `role="img"` kept on the rating span, the visible digits are `aria-hidden`, the star SVG is decorative. The literal English word "reviews" the old snippet printed into NL and FR names is gone.

## 4. Templates and config

- `templates/index.json:55` `rating_text` "4.7/5 (110)" (fixture PASS); nothing else in the file changed.
- `templates/product.subscription-item.json:17-21` `category_strip_block` settings `show_rating` true, `rating_source` "fixed", `rating_value` "4.7", `rating_count` 110 (integer).
- `templates/product.json`: untouched, and it has no `category_strip` block, so there is nothing to keep consistent (observation 6 on its Judge.me badge).
- `config/settings_data.json`: not in the range (`git diff --stat 32d41ab..af5da5c -- config` empty).
- `git grep -nF "4.8 (234)" -- assets blocks config layout locales sections snippets templates` returns nothing (exit 1). Remaining hits are docs only.

## 5. Layout

Fixture re-run, then measured in the Orca browser (isolated profile `astra-r95`, `frame-multi.html` iframes of the given width, the fixture's own in-page checks run per frame with `fxRun()`, Day and Night by the body class). Screenshots under `docs/reviews/shots/` (gitignored by `docs/**/*.png`):

- `astra-r95-1440-day-night.png`
- `astra-r95-390-375-day-night.png`
- `astra-r95-320-day-night.png`
- `astra-r95-live-pdp-375.png` (the live PDP at 375 for the column width; the first screen only)
- 750: the tab stopped drawing frames after the measurement (`Screenshot timed out — the browser page did not draw a frame`, then the tab was gone from `orca tab list`), so the 750 numbers below come from the in-page report read before that; no 750 PNG.

| Width | Mode | Hero badge | Strip row (fixed EN; NL and FR identical in width) |
|-------|------|------------|------|
| 1440 | Day, Night | "4.7/5 (110)" one line, text 58.3×16.8 at 14 px, badge 225.1×72, whole badge is the link; NL "4,7/5 (110)" same | one row, strip 484×21 in the 484 column (artwork 252.4 + gap 16 + rating 91.8 = 360.2 needed); score Nunito 12 px 700 uppercase |
| 750 | Day, Night | one line, text 54.2×15.6 at 13 px, badge 225.1×72 | one row, 720 column, 360.2 needed |
| 390 | Day, Night | wrapper `display: none` (no badge on phones, D-3 of 20 Oct) | one row, strip 360×21 in the 360 column; needs 356.2 (gap 12 on phones) |
| 375 | Day, Night | hidden | **wraps**: strip 345×49, rating on a second line under the artwork, left-aligned, nothing clipped |
| 320 | Day, Night | hidden | **wraps**: strip 290×49, same shape |

Colours as expected per mode: Day text rgb(25, 31, 56), Night rgb(255, 251, 246), star rgb(127, 185, 255) in both. The count colour equals the value colour in both modes (pre-existing, noted in R95 §4).

**Threshold confirmed**: the row needs 356.2 px on phones with "4.7/5 (110)" and 343.2 with the old "4.8 (234)"; with the page's 15 px padding each side it wraps below a 386.2 px viewport now, below 373.2 before. The worker's numbers hold. The column model is right: on the live PDP at 375 (`www.karmicare.com/products/karmicare-biorhythmic-oral-care-system`, isolated profile, 01:33 CET) `.page-width` padding is `0 15px`, `.product__info-wrapper` and `.product__info-container.kc-buybox` are 345 wide with 0 padding, the strip is 345 wide, the artwork 252.375, gap 12 px. The live page has no rating span today and no "Liquid error" in its HTML.

**Judgement**: not a blocker (finding 3). The wrap is handled by the existing `flex-wrap: wrap`, the second line is 16 px tall under a 21 px artwork with the 12 px row gap, and no CSS in the diff is involved. It is a design call for Victor because 375 is a common phone width.

**Smallest fix, measured in the 375 and 320 frames, not implemented** (`assets/kc-category-strip.css`, inside a `@media screen and (max-width: 749px)` block):

- **A, recommended**: `.kc-category-strip__brand { width: clamp(220px, calc(100% - 104px), 252.375px); }` (104 = gap 12 + rating 91.8, rounded up). At 375 the artwork shrinks to 241 px (4.5 % smaller) and the row holds: strip 345×20. At 320 the clamp floor keeps the artwork at 220 px and the row still wraps (strip 290×46), which keeps the artwork legible on the smallest phones. `aspect-ratio` keeps the mask in proportion.
- **B**: `.kc-category-strip { flex-wrap: nowrap; } .kc-category-strip__brand { min-width: 0; }`. One row at 375 (artwork 241.2) and at 320 (artwork 186.2, 74 % of its size). I would not take B: 186 px makes the "Biorhythmic Oral Care" lettering about 9 px tall.
- **C**: `gap: 8px` on phones does nothing (352.2 needed, 345 available: still wraps).

If the count changes later (three digits stay three digits until 1000), nothing shifts; a four-digit count would need about 7 px more.

## 6. Brand and claims

The diff adds no customer-facing words. Visible strings added: "4.7/5 (110)" (`templates/index.json`, hero schema default), "4.7" and 110 (strip template and schema defaults), "/" and the existing locale keys. The figure is a statement of fact from Victor's count (kc-ai-master `work/2026-10-29/01-webflow-reviews-teruggehaald.md`, as briefed: 110 reviews, 522 stars, mean 4.745, which rounds to 4.7). No claim words, no "discount", no dashes in customer copy (the two dashes in the diff are list bullets inside the snippet's Liquid comment and the merchant-facing schema `info` strings). The "/5" against Figma is finding 4, noted, not blocking. Awake/Asleep order and commodity words are not touched.

## 7. Cleanup

- The old `show_rating` info line (metafield wording) was moved to the select's info and exists once (`git grep "filled by the review app"` → the select info only).
- `docs/reviews/fixture/.gitignore` ignores `out/` and `node_modules/`; `git ls-files docs/reviews/fixture` lists only `.gitignore`, `README.md`, `fixture.css`, `fixture.js`, `render.mjs`.
- No screenshot is tracked (`git ls-files docs/reviews/shots` empty; `docs/**/*.png` is in the root `.gitignore`).
- Nothing else became obsolete: the metafield path is kept deliberately behind the select (PLAN §3), `assets/kc-category-strip.css` is unchanged and every class it styles is still printed.
- `npm install --no-save` needs `--cache "$TMPDIR/npm-cache"` inside the worker sandbox (the shared `~/.npm` cache is read-only there); worth one line in the fixture README, optional.

## Rework needed

None for landing. Recommended before the next pass on this snippet: finding 1 (`| round` on `rating_max`). Finding 2 is for the landing desk's ship order. Finding 3 waits for Victor; if he wants one row at 375, apply candidate A in `assets/kc-category-strip.css` as a separate small commit with the strip CSS as its scope.
