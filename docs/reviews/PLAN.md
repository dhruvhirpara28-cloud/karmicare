# Reviews: real Judge.me ratings on brand · plan (Phase 1)

**Created**: 2026-10-22 · reviews lane coordinator, branch `karmicare/soft-launch-reviews` (from `karmicare/soft-launch` fe6367a), Orca Run `run_6cc0fb311604`

### Changelog
| Date | Change |
|------|--------|
| 2026-10-22 | Phase 1: theme inventory, live storefront read (two pages, one fetch each), Judge.me settings as the live page prints them, Figma frames on "Production Design 20.10.2026", claims list, decisions D-1 to D-5 for Victor. No theme code. |
| 2026-10-22 | Second read-only storefront pass on the landing desk's request (Victor: "wij hebben toch in Judge.me al onze gezamenlijke reviews geupload?"): §1.5 and §7 items 2, 3 and 8. D-1 and D-2 unchanged. |
| 2026-10-25 | D-1 decided by Victor (via the landing desk): the hero rating stays, without a link; the link to the reviews comes in Phase 2 with the review section. §0, §6 D-1, §7 item 1 and §8 W1 updated. No theme code. |

Everything marked **verified** was read today from the repo at fe6367a, from the live storefront HTML (`karmicares.myshopify.com`, theme `karmicare/main` id 187295564157, Dawn 15.5.0; homepage and `/products/karmicare-biorhythmic-oral-care-system`, fetched once each, plus `/pages/reviews`), from Judge.me's loader script, or from Figma `3rOMJvQZTzyYjnCV6oggV3` read-only. Everything marked *unverified* needs the Judge.me admin or a rendered dev theme (§7), neither of which this lane may touch or had yet.

## 0. Short version

- **The homepage shows "4.8 (234)" live today** (hero badge, `templates/index.json` L55). No source backs it (claims register C82). **Victor's decision, 25 Oct 2026 (D-1): the hero rating stays, without a link; the link to the reviews is added in Phase 2 together with the review section.** The badge's existing link to Trusted Professionals stays as it is. C82 stays open in the claims register until the number is backed by Judge.me data.
- **Judge.me gives the theme two numbers without scripts**: per product `product.metafields.reviews.rating` + `reviews.rating_count` (Shopify standard, the PDP strip already reads them), and shop-wide `shop.metafields.judgeme.all_reviews_rating` + `all_reviews_count` (names verified from Judge.me's own settings on the live page; values unverified). On the live PDP the strip renders **without** a rating, so the Duo product has no rating metafield yet (or the block's switch is off there). Whether the 238 bol.com imports sit on the Duo product or elsewhere is a Judge.me-admin question for Victor (§7).
- **Review bodies are not reachable from Liquid.** A review section on brand therefore means Judge.me's review widget (app block) inside a KC wrapper section that owns the header, the rating line, the footnote and the empty state, with theme CSS restyling Judge.me's cards to the tokens. Figma has this section on the PDP only (desktop EN+NL, mobile), between the comparison table and the research cards. Nothing on the homepage.
- **Recommendation**: hero and strip show one and the same Judge.me number (shop-wide at soft launch, product-level once the Duo product has its own reviews), formatted per locale, hidden automatically under 10 reviews, with the source in the accessible name and a click that lands on the review section. Review section = Judge.me review widget in the KC wrapper, PDP only, Figma's topic chips dropped for now.
- **Six of the seven Figma quotes make a health or medical claim** (cavities, remineralising, mouth ulcers, sensitivity, gums) and the seventh is borderline. They are listed in §5 for the claims owner and are never featured.

## 1. Data path (what the theme can read)

### 1.1 What is installed (verified)

| Item | State | Where |
|------|-------|-------|
| App embed `judgeme_core` | enabled | `config/settings_data.json` L207–211 |
| App embed `cart_drawer_widget` | disabled | L222–228 |
| App block `preview_badge` on the PDP | present, **disabled** | `templates/product.subscription-item.json` L28–32, block order L218; also `templates/product.json` L21–24 (enabled there, but that template is not the Duo's) |
| Category strip, `show_rating` | **true** | `templates/product.subscription-item.json` L15–20; snippet `snippets/product-category-strip.liquid` L19–26 |
| Hero badge `rating_text` | `"4.8 (234)"` hard-coded | `templates/index.json` L55; schema default `sections/hero-karmicare.liquid` L777–781 |
| Judge.me all-reviews page | not installed (`/pages/reviews` → 404) | live |
| Judge.me elements in live HTML | none (`jdgm-` classes appear only inside Judge.me's settings and CSS) | live homepage + PDP |

The Judge.me app embed puts on **every page**: an inline `window.jdgmSettings` JSON (639 keys), an inline bootstrap script, a `<noscript>` CSS link, and `loader.js` (9.9 KB, `defer`) from `cdn.shopify.com/extensions/…/judgeme-809/assets/`. The loader maps page selectors to widget files and loads a widget's JS and CSS from `cdnwidget.judge.me/widget_v3/` **only when a matching element exists** (verified in the loader: `.jdgm-preview-badge` → `main.js`; `.jdgm-review-widget` / `[data-widget="review"]` → base + main + others + write-review modal; `.jdgm-all-reviews-widget`, `.jdgm-all-reviews-page` → `arp.js`; carousel, reviews tab, all-reviews rating/text badge, medals, verified badge, popup, review snippet → `others.js`). Today no element matches, so only the loader runs.

### 1.2 Numbers the theme can read without scripts

| Source | Liquid | Scope | State today |
|--------|--------|-------|-------------|
| Shopify standard product rating | `product.metafields.reviews.rating.value.rating` (1–5, `scale_max`), `product.metafields.reviews.rating_count.value` | one product | **verified empty or hidden** on the live Duo PDP: the strip prints the artwork and no `kc-category-strip__rating` span. Either the metafield is blank / count 0, or the live block has `show_rating` off (the repo has it on; unverified which). |
| Judge.me shop rating | `shop.metafields.judgeme.all_reviews_rating` (round to 1 decimal), `shop.metafields.judgeme.all_reviews_count` | all products in Judge.me, imports included | names **verified**: Judge.me's own "all reviews text badge" template on the live page reads exactly these (`"Customers rate us {{ shop.metafields.judgeme.all_reviews_rating \| round: 1 }}/5 based on {{ shop.metafields.judgeme.all_reviews_count }} reviews."`). Values *unverified*: nothing renders them today. |
| Judge.me legacy HTML metafields (`product.metafields.judgeme.widget`, `.badge`) | HTML blobs from the old Liquid install | one product | *unverified*, not expected on a v3 app-embed install. Not a basis for this lane. |
| Hero via `all_products['karmicare-biorhythmic-oral-care-system']` | same product metafields, read on the homepage | one product | possible (Liquid allows 20 handle lookups per page); same emptiness as the strip today. |

Locale formatting: `round: 1` prints `4.8`; NL and FR need `4,8` (Figma NL shows "4,8"; the NL/FR localization batches translate the placeholder as "4,8 (234)"). Rule: when `request.locale.iso_code` starts with `nl` or `fr`, replace the decimal point. The count is an integer.

### 1.3 Judge.me settings as the live page prints them (verified, read-only)

| Setting | Live value | Matters for |
|---------|-----------|-------------|
| `widget_version` | `3.0`, `review_widget_revamp_enabled` true | the review widget is the 2025 "revamp" markup (`[data-widget="review"]`) |
| `locale` / `shop_locale` | `en` / `en`; `enable_multi_locales_translations` false | widget UI strings are English on `/nl` and `/fr` unless Victor turns on Judge.me's translations |
| `widget_translate_review_content_enabled` | false | review bodies show in the reviewer's language (bol.com imports: Dutch) |
| `widget_primary_color` | `#7FB9FF` | already the KC accent (`--kc-mapped-icon-accent-default`) |
| `review_widget_number_of_columns_desktop` | 3; `review_widget_corner_styling` soft; `review_widget_header_theme` minimal; `review_widget_reviews_section_theme` standard | starting point for the restyle |
| `verified_badge_text` / placement | "Verified", left of reviewer name | the verified label stays |
| `transparency_badges_collected_by_verified_review_provider` | true | label for Judge.me-collected reviews |
| `transparency_badges_from_another_provider` | **false** (text "Review collected from another provider") | **imported bol.com reviews are not labelled today** → Victor's switch (§7) |
| `transparency_badges_written_in_google_text` | "Review written in Google" | exists only for reviews Judge.me collected through Google |
| `preview_badge_product_page_install_preference` | false | consistent with the disabled block |
| `review_widget_install_preference` | `""`; `all_reviews_widget_v2025_enabled` false; `trust_badge_enabled` false; `judgeme_medals_install_preference` false; `verified_reviews_count_badge_install_preference` false | nothing installed beyond the core |
| `all_reviews_widget_v2025_no_review_text` | "Be the first to write a review" | Judge.me's own empty state (English) |
| `hostname_allowlist` | empty; the bootstrap's `_jdgmBlocked` is a hostname check | **no consent gate** in Judge.me's loader; it is an app embed and runs on every page today regardless of the banner |

App block handles: `judgeme_core`, `cart_drawer_widget` and `preview_badge` are verified from the repo. The handles of the review widget, all-reviews widget, carousel and the badges are *unverified* (Theme Check cannot check them; a wrong handle renders nothing). They are read in the theme editor under "Add block → Apps", or from the template JSON after Victor adds one there.

### 1.4 Which number where

| Place | Candidate numbers |
|-------|-------------------|
| Homepage hero badge | (a) shop-wide Judge.me rating + count · (b) Duo product rating + count · (c) none |
| PDP strip | (a) Duo product rating + count (as built) · (b) shop-wide, the same figure as the hero · (c) Judge.me preview badge block |
| Review section | Judge.me review widget (one product's reviews) · Judge.me all-reviews widget (every product) |

### 1.5 Second storefront pass (22 Oct, read-only, on the landing desk's request)

Victor's question, verbatim: "wij hebben toch in Judge.me al onze gezamenlijke reviews geupload?" What the live storefront gives away without admin access or login (same two saved pages as §1.1, plus four route probes 3 s apart):

| Check | Homepage | PDP (Duo) |
|-------|----------|-----------|
| Judge.me scripts | `loader.js` (defer), inline `jdgmSettings`, inline bootstrap | same |
| Judge.me elements in the DOM (`jdgm-prev-badge`, `jdgm-preview-badge`, `jdgm-widget`, `jdgm-review-widget`, `jdgm-all-reviews-*`) | **none**; the class names occur only inside Judge.me's CSS and settings | same |
| `data-number-of-reviews` / `data-average-rating` on an element | none; the only hit is Judge.me's CSS rule `.jdgm-prev-badge[data-average-rating='0.00']{display:none}` | none |
| JSON-LD | Organization, WebSite, Product: no `aggregateRating`, `ratingValue`, `reviewCount` | Organization + Product (offer €67.00, SKU KC-DUO-002, GTIN 05419980169303): no `aggregateRating`. The theme's own JSON-LD (`sections/main-product.liquid` L893) never adds one, and Judge.me's rich-snippet injection is absent |
| A review count anywhere in the HTML | only the hard-coded hero "4.8 (234)" | none; the strip prints the artwork without the rating span |
| Judge.me settings carrying a count or an identifier | none. `widget_rating_metafield_value_type` is true (Judge.me writes Shopify's `reviews.rating` in the standard rating format for products that have reviews). No shop domain, shop id or token in the settings, so Judge.me's widget API cannot be queried from outside | same |
| All-reviews routes | `/pages/reviews` 404 · `/pages/all-reviews` 404 · `/apps/judgeme` 404 (0 bytes: no app proxy at that path) · `/apps/judgeme/reviews` 404 · `judge.me/reviews/karmicares` unreachable from the sandbox (timeout) | — |

Reading: the storefront shows **no review data at all**, from Judge.me or anyone else. For the Duo product that means one of three things, and the HTML cannot tell which: Judge.me holds no published reviews on that product (then it writes no `reviews.rating` metafield and no rich snippet), the metafield sync is off, or the live block's `show_rating` is off. For the shop total nothing is printed anywhere. So "all our reviews are in Judge.me" can neither be confirmed nor denied from outside; it is a Judge.me-admin question (§7, items 2, 3 and 8). What is known: 238 rows were imported on 11 Sep 2026 from bol.com; whether the Google Business Profile reviews (5.0 / 24) were imported as well is not visible from the storefront.

## 2. Hero badge (`sections/hero-karmicare.liquid`, block `testimonial_badge`)

**Figma** (verified): Day `4121:34333`, Night `4121:141116`, both "Feature Icon" 307×72 at (32, 952) in the 1440 hero: avatar 56×72 radius-md · star 16 px + `4.8 (234)` in Label/Small (identity font, 700, 12/12, 1.7 px tracking, uppercase) · "Backed by health professionals" in Text/Medium strong (18/24) · arrow-right 16 px. Gap 20 px, rating column 206 px. Mobile: "Professional trust · V15" `4121:141945` exists in the mobile hero frame but renders empty (hidden layer), so decision D-3 of 20 Oct (no badge under 750 px, `assets/section-hero-karmicare.css` L332–337) stands.

**Code today** (verified): the badge prints `rating_text` verbatim when set (L355–371), the heading links to the Trusted Professionals section with the anchor rebuilt on the template id (L311–319; HE-02 fixed). Star colour from the `star_color` setting (`#7FB9FF`), text 1.3/1.4 rem 500.

### Rendered result per option (1440 Day and Night identical in layout; 390: nothing, by D-3)

| Option | EN | NL | FR | When the data is empty |
|--------|----|----|----|------------------------|
| (a) shop-wide Judge.me rating | ★ `4.7 (298)` *(figures illustrative; the real values are unverified)* · "Backed by health professionals →" | ★ `4,7 (298)` · "Gesteund door zorgprofessionals →" (NL batch) | ★ `4,7 (298)` · "Soutenu par des professionnels de santé →" | star line not rendered; the badge is avatar + heading + arrow |
| (b) Duo product rating | same shape, product figures | same | same | **today: no star line** (the live PDP shows the product without a rating) |
| (c) no number | avatar · "Backed by health professionals →" | avatar · "Gesteund door zorgprofessionals →" | avatar · "Soutenu par des professionnels de santé →" | n/a |

With (a) or (b) the rating line gets its own accessible name that names the source and the scale ("Customer rating 4.7 out of 5 on Judge.me, 298 reviews"; EN text to source-copy), and the line links to the review section on the PDP (`/products/karmicare-biorhythmic-oral-care-system#<section id>`), while the heading keeps its link to the professionals section. The visible text stays as Figma (number and count only). Below a minimum count (proposal: 10) the line is not rendered: that is a sample-size rule, never a rule on the rating value.

**Recommendation**: (a), built with (c) as its automatic empty state. It is real, verifiable, and labelled with its source. `rating_text` (schema L777–781, `templates/index.json` L55) is removed and replaced by a `rating_source` select (`shop` / `product` / `none`) and a `rating_min_count` range, so Victor can switch the source in the editor without code. The NL/FR localization entries for `rating_text` (`docs/localization/nl|fr/batch-01-homepage.json`) become obsolete; the source-copy lane retires them.

## 3. PDP strip (`snippets/product-category-strip.liquid`, block `category_strip`)

**Figma** (verified): `4121:142856` (EN), `4121:144413` (NL), mobile `4121:145970` (353 wide). The old reference `3391:12111` no longer exists in the file. Content: artwork 252.375×21 · gap 16 · star 16 px + `4.8` (Label/Small) + `(234)` at 68 % opacity. No link in Figma. The current markup matches this one to one (score + count span; the count uses `--kc-mapped-text-default-body`, 76 % alpha of the heading colour, close to Figma's 68 %).

| Option | What renders | Fit |
|--------|--------------|-----|
| (a) keep the product metafields (as built) | star + product rating + count; nothing while the product has no reviews | Figma yes; **empty today** |
| (b) the shop-wide Judge.me number, same figure as the hero | star + rating + count, accessible name "all Karmicare reviews" | Figma yes; shows a number now if the shop metafields are filled |
| (c) Judge.me preview badge block (enable the disabled block) | Judge.me's own stars markup, rendered by `main.js` after load (layout shift), styled by Judge.me settings, English "no reviews" text | off brand; the block would also need re-ordering next to the artwork |

**Recommendation**: own strip (as today) with the same `rating_source` setting as the hero (default: the same source Victor picks in D-1), so the two places never disagree. The rating becomes a link to the review section on the same page (smooth scroll, `aria-label` with source). Switch the strip to `product` as soon as the Duo product carries its own reviews (≥ 10).

## 4. Review section

### 4.1 Figma (verified)

PDP desktop EN `4121:143192`, NL `4121:144749` (1440×1204), mobile `4121:146253` (393×1102). No FR frame. No homepage frame: `06 · Customer-reported outcomes` (`4137:40480`) is the benefits grid and `Testimonials/LargeCard` (`4121:35191`) / `KC/Professional quote carousel` are the professional quote carousel, not customer reviews.

Position in the PDP flow: after `Table` (comparison) and before `Value & Features` (research cards). In `templates/product.subscription-item.json` that is between `comparison_table_r8CDbT` and `research_behind_system_EkjATL` (order L788–798). Mobile Figma numbers it "06" at the same place.

Content: caption "CUSTOMER EXPERIENCE" / "KLANTERVARINGEN" · heading "What they noticed," + dimmed "and their dentist did too" / "Wat zij merkten," + "en hun tandarts ook" · five stars + "4.8" / "4,8" · filter chips All · Less sensitivity · Whiter teeth · Calmer gums · Cavity-free check-ups · The AM/PM ritual · Gentle & fluoride-free · On the price · 3 stars and under (NL: Alle · Minder gevoeligheid · Wittere tanden · Rustiger tandvlees · Controles zonder gaatjes · Het AM/PM-ritueel · Zacht & fluoridevrij · Over de prijs · 3 sterren en minder) · three masonry columns of cards (`4121:143220`: surface-secondary, radius 16, padding 24, gap 12; meta line = accent stars + optional source word "Google" in the science font 12/12; quote 15/20; name 14/16, first name + initial) · button "Show all 84 reviews" / "Bekijk alle 84 reviews" · footnote "Customer testimonials describe individual experiences and are not guaranteed outcomes." / "Klantgetuigenissen beschrijven individuele ervaringen en zijn geen gegarandeerde resultaten." Mobile: single column, chips swipe. The numbers 4.8 and 84 are placeholders (84 ≠ 238 imports).

### 4.2 Options

| Option | How | What it gives | Limits |
|--------|-----|---------------|--------|
| (a) Judge.me **review widget** app block inside a KC wrapper section | new `sections/kc-reviews.liquid` renders caption, heading, rating line (from §1.2), the `{% render block %}` app block, footnote, empty state; `assets/kc-reviews.css` restyles `.jdgm-*` / `[data-widget="review"]` to the tokens | all of one product's reviews, Judge.me's rating filter and search, verified and transparency labels, pagination, write-a-review, dates | the block handle must be verified in the editor; Judge.me UI strings English unless Victor turns on translations; restyle is CSS over Judge.me markup (keep it to colours, fonts, radii, spacing) |
| (b) Judge.me **all-reviews widget** in the same wrapper | same wrapper, other block | every product's reviews, so the bol.com imports show whatever product they sit on | `all_reviews_widget_v2025_enabled` is false today (Victor's switch); per-review "about <product>" labels |
| (c) curated quote blocks in the theme (static) | section blocks with quote, name, date, source, Judge.me review id | full brand control | **not a review section**: static, hand-picked, each quote needs a traceable Judge.me id, a source label and the claims owner's approval; the Figma quotes are not in the repo or on the site, so under AGENTS.md §3 they are new copy. Only as a featured layer on top of (a)/(b), never alone |
| (d) own markup fed by Judge.me's widget API in the browser | JS fetch to `api.judge.me` with the public token | full control of markup | needs the public token (not in the page), a third-party request per view, duplicates what (a) does |

### 4.3 Recommendation: (a), PDP only

- **Wrapper owns**: caption, heading, rating line (same `rating_source` as the strip), "Show all" is Judge.me's own pagination (no count button of ours, so no placeholder number), footnote, a one-line source note, empty state. Day and Night through the surface tokens.
- **Judge.me owns**: cards, stars, verified/transparency labels, filters, pagination, the write-a-review form and its GDPR statement.
- **Figma topic chips** (Less sensitivity, …): not derivable from Liquid; Judge.me's keyword and highlight features are Judge.me settings (`review_widget_show_review_highlights` false today). Soft launch: Judge.me's rating filter and search instead (D-4).
- **Imported reviews**: Judge.me labels them only when "Review collected from another provider" is on; it is off today (§1.3). Victor's switch, before the section goes live.
- **NL/FR**: theme strings (caption, heading, rating label, footnote, source note, empty state) through the source-copy lane; Judge.me's own strings through Judge.me's translation setting (Victor). Review bodies stay in the reviewer's language.
- **Empty state**: rating line hidden when count is 0 or below the minimum; the wrapper shows one short line (copy from source-copy) above Judge.me's own "Be the first to write a review".
- **Performance**: nothing new on pages without the section. On the PDP the widget adds Judge.me's `widget_v3` JS and CSS from `cdnwidget.judge.me` (the CDN answers curl with 403, so the sizes are *unverified*; the Phase 2 worker measures them in the browser's network panel, Day and Night, and reports). The loader already defers; the widget renders after load, so the wrapper reserves height to avoid a layout jump.
- **Consent**: Judge.me's loader has no consent gate and runs today on every page as an app embed; the theme cannot change that. Whether the widget sets cookies or storage is *unverified*; the Phase 2 worker checks the browser's storage panel before and after the widget renders and reports. If it sets cookies, the wrapper can inject the widget element only after Shopify's `trackingConsent` allows it (the loader rescans on `jdgm.docReady`; to be tested).
- **Homepage**: no review section (not in Figma). The hero badge links to the PDP section.

## 5. Claims in the reviews (for the claims owner)

Customer reviews shown by the brand are brand communication. Of the seven quotes in the Figma section, six state a health or medical effect and one is borderline. None of these may be featured (no snippet, carousel, hero quote or static block). Whether Judge.me keeps publishing them in the full widget is Victor's call with the claims owner; a positive review may be unpublished, a negative one never.

| # | Quote (Figma EN, verbatim) | Name shown | Source tag in Figma | Claim type |
|---|----------------------------|------------|---------------------|-----------|
| R1 | "I've had cavities so many times. Since brushing with this: my first check-up without cavities, after 3 months!" | Marijke Z. | Google | caries prevention |
| R2 | "Your formula works wonders on mouth ulcers. I also feel more 'calm' in my mouth, if that doesn't sound strange." | Mariëlle V.d. | — | treats ulcers (medical) |
| R3 | "The most pleasant toothpaste I've ever tried. My gums look healthier, and that without aggressive bleach or abrasives." | Annelies S. | — | gum health ("look healthier": borderline, cosmetic wording) |
| R4 | "A glowing report from my dentist after a few months of Karmicare. First check-up in ages without cavities and barely any tartar. Dentist visits are actually fun again :-) Thank you!" | Lien D. | Google | caries and tartar prevention; dentist endorsement |
| R5 | "My teeth are no longer sensitive and I see a clear difference. They've become visibly whiter." | Geruza A. | Google | treats sensitivity; whitening (cosmetic, fine) |
| R6 | "I've had very sensitive gums for years. Since I started, my gums are calm and the worn spots are remineralising." | Danny V. | — | remineralisation; gum treatment |
| R7 | "After my last dentist visit: no cavities for the first time in 5 years!" | Gert K. | — | caries prevention |

Also for the claims owner: the heading line "and their dentist did too" (dentist endorsement framing), the chips "Cavity-free check-ups", "Calmer gums", "Less sensitivity" (prevention / treatment wording as filter labels), and the "Google" source tag: Google Business Profile reviews (5.0 / 24) are not in Judge.me; a "Google" label can only render for reviews Judge.me itself collected through Google (*unverified* whether any exist). The Google and bol.com figures stay out of every Judge.me badge; they can only appear with their own source named (not planned for soft launch).

Register: C82 (`"4.8 (234)"`, "needs a source we do not have") closes when Phase 2 lands; C80/C81 (endorsement wording) are untouched by this lane.

## 6. Decisions for Victor

**D-1 · Which number in the hero badge?**
(a) The shop-wide Judge.me rating with the review count, all products, imports included, formatted per language (4,7 in NL/FR), hidden automatically while Judge.me holds fewer than 10 reviews or no number; the accessible name says "Customer rating … out of 5 on Judge.me, … reviews"; the star line links to the review section on the PDP, the heading keeps its link to the professionals. (b) The Duo product's own Judge.me rating: same rendering, but today the product has no rating, so the badge shows no number until reviews are attached to it. (c) No number: avatar, "Backed by health professionals", arrow. **Recommendation: (a)**, with (c) as its built-in empty state. The placeholder "4.8 (234)" is removed in every case.

**Decision (Victor, 25 Oct 2026, via the landing desk)**: "Hero rating mag blijven; zonder link. De link maken we later samen met de review sectie." So: the rating "4.8 (234)" in the hero badge stays as it is, the rating gets no separate link to a review section now, and the whole badge keeps its existing link to Trusted Professionals. The link from the rating to the reviews is built in Phase 2 together with the review section (D-3). Whether the number is then fed by Judge.me data (options a or b above) is settled with that section; until then claims register C82 stays open. No theme code changes from this decision.

**D-2 · Which number on the PDP strip?**
(a) The product's own rating (as built today, empty until the Duo product has reviews). (b) The same shop-wide number as the hero, so both places always agree. (c) Judge.me's preview badge block: Judge.me's stars markup, rendered after page load, styled by Judge.me, off brand. **Recommendation: (b) for the soft launch, switching to (a) in the editor once the Duo product carries 10 or more of its own reviews.** The strip rating becomes a link to the review section.

**D-3 · Review section: how and where?**
(a) Judge.me's review widget (this product's reviews) inside a KC wrapper section on the PDP, between the comparison table and the research cards as in Figma, restyled with theme CSS to the tokens; the wrapper owns caption, heading, rating line, footnote, source note and empty state. (b) Judge.me's all-reviews widget (every product's reviews) in the same wrapper; needed if the bol.com imports do not sit on the Duo product. (c) Static curated quotes as theme blocks: hand-picked, each with a Judge.me review id and source label; not a review section, only possible as a featured layer later. (d) No review section at soft launch; the badges then link nowhere. **Recommendation: (a), or (b) if Judge.me shows the imports on another product. PDP only; nothing on the homepage.**

**D-4 · Figma's topic chips (Less sensitivity, Whiter teeth, …)?**
(a) Leave them out for the soft launch; Judge.me's own rating filter and search take their place. (b) Use Judge.me's review-highlights / keyword feature (a Judge.me setting, plan-dependent, unverified) and style it as chips. **Recommendation: (a).** Three of the chip labels are claims wording anyway (§5).

**D-5 · Language of Judge.me's own texts on /nl and /fr?**
Today the widget strings are English on every locale ("Verified", "Write a review", filters, dates). (a) Accept English widget strings at soft launch; the wrapper's caption, heading, footnote and source note are NL/FR through the theme. (b) Victor turns on Judge.me's widget translations for NL and FR before the section goes live; the theme part is the same. **Recommendation: (b) if the Judge.me plan allows it, else (a).** Review bodies stay in the language they were written in either way.

## 7. Victor's checks and switches (Judge.me admin and theme editor; not for this lane)

1. ~~**Now, on the live theme**: blank the hero badge's "Rating Text" in the editor (Hero · Professionals Badge) so "4.8 (234)" stops showing before Phase 2 lands.~~ Closed by Victor's D-1 decision of 25 Oct 2026: the hero rating stays as it is (§6 D-1).
2. **Judge.me → Reviews, filtered per product**: on which product do the published reviews sit (Duo, Awake, Asleep, no product), how many are published versus hidden or pending, and what is each review's source (bol.com import, Google, a Judge.me request email)? The storefront shows no review data at all (§1.5), so the assumption that all joint reviews are in Judge.me cannot be checked from outside. This decides (a) versus (b) in D-2 and D-3.
3. **Judge.me → Settings, Shopify integration**: is the sync of reviews to Shopify's product metafields (`reviews.rating`, `reviews.rating_count`) on, and are the shop-wide `judgeme.all_reviews_rating` / `all_reviews_count` metafields being written? The live PDP prints no product rating and no rich snippet; the Phase 2 dev theme renders both metafields first and reports what comes back.
4. **Judge.me → transparency badges**: turn on "Review collected from another provider" so imported reviews are labelled (off today).
5. **Judge.me → translations**: NL and FR widget strings (D-5 b).
6. **Claims owner**: §5 list; decide which reviews stay published.
7. **Theme editor, after Phase 2**: add nothing; the app block arrives in the template JSON from this lane. Only the block handle has to be confirmed first (read it once under "Add block → Apps").
8. **Google reviews**: are the Google Business Profile reviews (5.0 / 24) in Judge.me too (imported or collected through Judge.me's Google connection), or is only the bol.com import there? This decides whether the "Google" source word in the Figma cards can ever render, and whether the shop-wide number includes them.

## 8. Phase 2 build plan (after Victor's "ja")

Preconditions: `git merge karmicare/soft-launch`; each worker on its own child worktree and its own unpublished dev theme (`shopify theme dev`, a free port); fetches on the live store ≥ 2.5 s apart; anonymous browser profile; no admin writes; no edits to `config/settings_data.json`, the Loop widget files, `locales/*.json`, `docs/source-copy/*`, `docs/localization/*`.

| Wave | Worker | Target | Change | Acceptance |
|------|--------|--------|--------|------------|
| 1 | W0 rating snippet | new `snippets/kc-rating.liquid` | one snippet that takes `source` (`shop` / `product` / `none`), `product`, `min_count`, returns rating (1 decimal, locale decimal mark), count and a boolean `show`; renders the star + score + count markup used by hero and strip, with the accessible name from a locale key (EN text to source-copy, key agreed first) | renders the **real** metafield values on the dev theme and reports them (shop-wide and Duo product) before anything else; Theme Check 0 errors |
| 2 | W1 hero badge | `sections/hero-karmicare.liquid`, `assets/section-hero-karmicare.css`, `templates/index.json` (block settings only) | **Scope after D-1 (25 Oct)**: the rating line and the badge's link to Trusted Professionals stay as they are. W1 only adds the link from the rating line to the PDP review section, in the same wave as W3 and only once W3's section exists on the template. The earlier scope (`rating_text` replaced by `rating_source` + `rating_min_count`, star line via W0's snippet) applies only if Victor settles the number's source with the review section | before/after at 390 and 1440, Day and Night, EN/NL/FR; Theme Check 0 |
| 2 | W2 PDP strip | `snippets/product-category-strip.liquid`, `assets/kc-category-strip.css`, `sections/main-product.liquid` (category_strip schema), `templates/product.subscription-item.json` (block settings) | `show_rating` → `rating_source` (+ min count), snippet reuse, rating as a link to the section, count at Figma opacity | same captures; Theme Check 0 |
| 2 | W3 review section | new `sections/kc-reviews.liquid`, `assets/kc-reviews.css`, `templates/product.subscription-item.json` (new section inserted after `comparison_table_r8CDbT`) | wrapper per §4.3 with the Judge.me app block (handle confirmed by Victor), restyle, reserved height, empty state; strings as keys agreed with source-copy; network and storage measurements reported | captures at 390 and 1440, Day and Night, EN/NL/FR with the widget rendered; JS/CSS sizes and cookie/storage findings in the report; Theme Check 0 |

Then one `merge_ready` to the landing desk: "Ready to land: reviews <sha>".

**Copy needed from the source-copy lane** (EN given here, NL/FR theirs): the rating accessible name; caption "CUSTOMER EXPERIENCE"; heading "What they noticed, and their dentist did too" (claims owner may reword the second line); footnote "Customer testimonials describe individual experiences and are not guaranteed outcomes."; a source note naming Judge.me and the bol.com import (new copy, not in Figma: **blocked until source-copy writes it**); an empty-state line (new copy, same). NL for caption, heading, footnote exists in the Figma NL frame.

**Cleanup**: the `show_rating` checkbox if replaced. The `rating_text` setting, its `templates/index.json` value and the NL/FR `rating_text` localization entries (`index:hero_karmicare_XKKLDK/testimonial_badge_h8d3WL/rating_text`) stay after D-1 (25 Oct); they are retired only if Victor later settles the number's source with the review section.
