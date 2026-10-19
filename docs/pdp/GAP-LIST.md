# Duo PDP gap list against Figma PDP V15

**Task**: soft-launch A2, branch `karmicare/soft-launch-pdp`, baseline `3bae259` (= live theme karmicare/main #187295564157; the live CSS matches the repo up to CDN minification, checked rule by rule on 19 Oct).
**Page**: `https://karmicares.myshopify.com/products/karmicare-biorhythmic-oral-care-system` (`templates/product.subscription-item.json`).
**Reference**: Figma `3rOMJvQZTzyYjnCV6oggV3`, desktop V15 `2673:8186`, mobile `4023:29018`, sticky bar `4034:29675`. The proposed ramp `4042:29938` was not used.
**Widths**: 393, 450, 768, 1024, 1440, 1920, 2560, Night and Day.

Priority: **P0** broken, clipped or unreadable · **P1** visibly off-design · **P2** refinement.
Owner: pdp · homepage · utopia · source-copy · assets · Victor.
Screenshots: `docs/pdp/shots/<section>-<viewport>-<mode>-<before|after>.png` (local, gitignored). See REPORT.md for how each set was captured.

## Summary

- No P0 on the PDP. Nothing overflows the page horizontally at any width from 393 to 2560, Day or Night. Text is clipped only at the edges of the marquee rows (trusted professionals, research), which is by design.
- From 1920 px every PDP section is capped at the 1480 px page width (content 252–1668 at 1920, 572–1988 at 2560), so nothing stretches. The marquee rows run full-bleed by design.
- Three P1 buybox and layout gaps are fixed on this branch (rows 1–3). The other P1 rows need markup, copy or a decision, so they are listed for Victor or for their owner.

## main-product: gallery, buybox, plan cards, mission card

| # | Observed on live | Reference | P | Owner | Acceptance shot | Status |
|---|---|---|---|---|---|---|
| 1 | Care Credit and Check-up chips in the plan cards break between whole items (Loop renders a wrapping flex row: amount, label, ⓘ). At 393/450 the ⓘ sits alone on a second line (chip 291×64). At 768 the amount sits alone above the label. At 1024 the chip runs to three lines (264×91). | Mobile `4023:29061`, desktop `2673:8338`: amount, label and ⓘ on one line | P1 | pdp | `buybox-plans-393-night-after`, `buybox-plans-768-night-after`, `buybox-plans-1024-night-after` | **Fixed** (kc-buybox.css): the label wraps inside its own item, the ⓘ stays on line 1, one-line chips are unchanged (Check-up chip 243 px before and after); 1024 with row 3: 60-Day chip on one line (316×39), Year chip on two with the ⓘ on line 1 |
| 2 | Welcome Kit names cut by Loop's two-line clamp where the buybox is narrow: "Morning Toothbrush…", "Evening Toothbrush…" at 990–1199 (92 px tiles). | KC/Kit_item: the full name under the tile (three lines on mobile) | P1 | pdp | `buybox-plans-1024-night-after` | **Fixed** (kc-buybox.css): full names |
| 3 | At 990–1160 the buybox column is 384 px (344 px of content) at 1024, narrower than on a phone (363). This is what breaks rows 1 and 2 and wraps the highlight chips. | Desktop right column 448 (`2673:8256`) | P1 | pdp | `buybox-plans-1024-night-before/after` | **Fixed** (section-main-product.css): buybox at least 44rem from 990 px, gallery takes the rest (1024: 520/440); from about 1160 the 60/40 split applies as before (1440: 826/550, unchanged) |
| 4 | Tablet 750–989: two columns of about 350 px; the hero is about 340 px tall, the buybox 369 px wide, and the 44 px professionals heading wraps in a 370 px column. No Figma tablet frame. | none | P2 | Victor | `main-product-768-night-before` | Decision D4 |
| 5 | Mobile gallery keeps the 44 px arrows beside the thumbnails (3.5 thumbnails visible at 393). | `4023:29029`: thumbnails swipe, arrows dropped | P2 | Victor | `main-product-393-night-before` | Decision D6 (arrows shipped on purpose on 18 Oct, so not changed) |
| 6 | Highlight chips stacked in four rows (block setting `static_layout`). | `4023:29061`: one swipe row | P2 | Victor | `main-product-393-night-before` | Decision D6 (setting choice) |
| 7 | "Brushing & Beyond" badge on the Year card at 393. | pdp-mobile open item 3: hidden on mobile (clashes with "Most Picked") | P2 | Victor | `main-product-393-night-before` | Decision D6 |
| 8 | "What you'll feel (and your dentist notices)" wraps at 393 and 768, and its divider shrinks to a short stub before the "First 60 days" chip. | `4023:29061`: title, subtitle and chip on one row | P2 | pdp | `main-product-393-night-before` | Open (P2) |
| 9 | Professional mini cards under the gallery (from 750 px): the fourth card is cut at the column edge at 1440–2560 (cards have a 22rem minimum, 4 × 220 + gaps > 826), with slider arrows. | `2838:14861`: four 216 px cards, no arrows, "Meet the professionals ↓" | P2 | pdp | `main-product-1440-night-before` | Handoff (rule lives in `component-professional-testimonials.css`, outside A2's file list) |
| 10 | "Trusted by professionals" appears twice from 750 px: the block under the gallery and section 03. | pdp-mobile brief; the block is hidden on phones since 50cdf63 | P2 | Victor | `main-product-1440-night-before`, `trusted-professionals-1440-night-before` | Decision D5 |
| 11 | Day: a faint lighter rectangle behind the first gallery image on the cream page. | V15 hero has no panel | P2 | assets | `main-product-1440-day-before` | Asset |
| 12 | First visit: the cookie banner covers the bottom 230 px at 393 (over the plan cards) and, at 1024, the next-thumbnail arrow and part of the buybox. | none | P2 | Victor | `buybox-plans-393-night-before`, `buybox-plans-1024-night-before` | Info (theme-wide component) |
| 13 | Copy differs from V15: title "Awake & Asleep Morning & Night Toothpaste System" (V15 "AM/PM Oral Care System"), chip set, no rating line, "Upgrade after your first cycle" line absent. | `2673:8195` | P2 | source-copy | n/a | Not changed (copy) |

## Sticky buy bar (`snippets/sticky-cart-block.liquid`)

| # | Observed on live | Reference | P | Owner | Acceptance shot | Status |
|---|---|---|---|---|---|---|
| 14 | The bar shows "+ €5,90 Care Credit back" (the shop money format, comma) while the buybox shows "€5.90". The run's rule is "EN renders €0.49". | COMMON-RULES §3 | P1 | Victor | `sticky-bar-393-night-before`, `sticky-bar-1440-night-before` | Decision D3 (the format comes from the shop money format) |
| 15 | Layout checked: 393 is a 369×106 card above the safe area and below the cookie banner, no overlap; 1440 is a centred 1026 px card (768: 448 px, 2560: 1026 px, measured). It shows between sections and hides at CTAs as designed. | `4034:29675` | none | none | `sticky-bar-393-night-before`, `sticky-bar-1440-night-before` | No gap |

## how-it-works-steps

| # | Observed on live | Reference | P | Owner | Acceptance shot | Status |
|---|---|---|---|---|---|---|
| 16 | Step numbers "01 / 02 / 03" on the media. They are in V15, but the brand rules ban 01/02/03 step labels. | COMMON-RULES §3; `3162:35665` | P1 | Victor | `how-it-works-steps-1440-night-before` | Decision D2 |
| 17 | The step media show a product still on near-black panels instead of the V15 footage; the black sits heavy on the Accent surface. | `3162:35665` | P2 | assets | `how-it-works-steps-1440-night-before` | Asset |
| 18 | Layout matches V15 at every width: 3 columns from 990, 2-card swipe at 768, 1.3-card swipe at 393/450, capped at 1480. | `3162:35657`, `4026:29555` | none | none | `how-it-works-steps-*-before` | No gap |

## comparison-table

| # | Observed on live | Reference | P | Owner | Acceptance shot | Status |
|---|---|---|---|---|---|---|
| 19 | 393–749: the five-column table scrolls sideways under a sticky label column; at 393 you see the labels, Karmicare and half of "Regular brushing". | `4027:29433`: three columns (label · Karmicare · one competitor) with chips to switch the third | P1 | pdp | `comparison-table-393-night-before` | Decision D1 (needs markup and JS, not a safe CSS fix) |
| 20 | 750–989: still a sideways strip (table minimum 900 px). | none | P2 | pdp | `comparison-table-768-night-before` | Follows D1 |
| 21 | Desktop: cell text semibold (600) where V15 is regular; the Karmicare column has no row hairlines; the first header cell reads "Compare" (blank in V15). | `3077:35199` | P2 | pdp / source-copy | `comparison-table-1440-night-before` | Open (P2) |

## product-compare-plans

| # | Observed on live | Reference | P | Owner | Acceptance shot | Status |
|---|---|---|---|---|---|---|
| 22 | 393–749: the table scrolls sideways; at 393 you see Try Once and a sliver of the featured 60-Day column, and the Year is off-screen. Each CTA sits in its column. | `4030:29780`: label 104, the plans share the rest, CTAs stacked under the table; Year button "Begin the Karmicare Year" (copy pending Victor) | P1 | pdp | `product-compare-plans-393-night-before` | Decision D1 (markup plus a copy decision) |
| 23 | `.pc-col { transition: all 0.4s }` animates column widths whenever the layout reflows (rotation, resize, late font load). A capture caught the label column at 178 px mid-animation. | none | P2 | pdp | none | Open (P2) |
| 24 | Welcome Kit thumbnails in the label cell are three 25 px dim circles, hard to read in Night. | `3182:38950` | P2 | pdp | `product-compare-plans-1440-night-before` | Open (P2) |
| 25 | Desktop matches V15: 284 + 3 × 282 = 1130 px table. V15 shows Year "Duos in a year 7"; live shows 6, which matches the offer. | `3182:38945` | none | none | `product-compare-plans-1440-night-before` | No gap |

## Shared sections (owner: homepage, relayed by the orchestrator)

| # | Section | Observed on live | Reference | P | Owner | Acceptance shot |
|---|---|---|---|---|---|---|
| 26 | research-behind-system | Card labels and badges are 10 px and citations 11 px at 393/450; citations stay 11 px up to 1440. | none | P1 | homepage / utopia | `research-behind-system-393-night-before` |
| 27 | care-comes-back | Step labels "01 / 02 / 03" in circles; the brand rules ban them. | COMMON-RULES §3 | P1 | homepage / Victor | `care-comes-back-1440-night-before` |
| 28 | featured-product (end CTA) | "Care Credits back" (the term is Care Credit); "€0,49 per brushing" and "€5,90" with commas where the buybox uses "€0.49"/"€5.90"; V15's end CTA is "Start your day-and-night ritual" with KC/Ritual offer. | `3139:21752` | P1 | homepage / source-copy | `featured-product-1440-night-before` |
| 29 | chronobiology-clock | "DRAG THE RING · EXPLORE 24 HOURS" is 11 px at 768; layout fine at every width. | none | P2 | homepage / utopia | `chronobiology-clock-karmicare-768-night-before` |
| 30 | trusted-professionals | Marquee cards cut at the viewport edges (by design). Duplicate heading: see row 10. | none | P2 | homepage | `trusted-professionals-2560-night-before` |
| 31 | page as a whole | V15 sections 08 testimonials (`2673:9320`) and 09 cost of waiting (`3272:50601`) are not on the PDP; care-comes-back stands where 09 was. | `2673:8186` | P2 | Victor | none |

## Checked with no gap

- Horizontal overflow: none at 393, 450, 768, 1024, 1440, 1920, 2560, Night and Day (`documentElement.scrollWidth` = viewport).
- Wide screens: header, main-product, how-it-works, comparison, plans, care-comes-back and footer share the 1480 px page width and its 32 px gutter. Their left edges line up at 252 (1920) and 572 (2560).
- Mission card (Marlide 300, "Strengthen your teeth. Strengthen yourself."): fits at every width, Day and Night.
