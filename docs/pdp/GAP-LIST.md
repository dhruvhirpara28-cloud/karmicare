# Duo PDP gap list against Figma PDP V15

**Task**: soft-launch A2, branch `karmicare/soft-launch-pdp`, baseline `3bae259` (= live theme karmicare/main #187295564157; the live CSS matches the repo up to CDN minification, checked rule by rule on 19 Oct).
**Page**: `https://karmicares.myshopify.com/products/karmicare-biorhythmic-oral-care-system` (`templates/product.subscription-item.json`).
**Reference**: Figma `3rOMJvQZTzyYjnCV6oggV3`, desktop V15 `2673:8186`, mobile `4023:29018`, sticky bar `4034:29675`. The proposed ramp `4042:29938` was not used.
**Widths**: 393, 450, 768, 1024, 1440, 1920, 2560, Night and Day.

Priority: **P0** broken, clipped or unreadable · **P1** visibly off-design · **P2** refinement.
Owner: pdp · homepage · utopia · source-copy · assets · Victor.
Screenshots: `docs/pdp/shots/<section>-<viewport>-<mode>-<before|after>.png` (local, gitignored). See REPORT.md for how each set was captured.

## Status 22 Oct

**In merchant-edit** means the theme change is in `merchant-edit` `31407fb`, checked with `git merge-base --is-ancestor <sha> merchant-edit`. That branch is not pushed yet, so none of it is live. Rows 28 and 35 have one part done and one part open, so each is split in two.

| # | Status | Detail |
|---|---|---|
| 1 | In merchant-edit | `4a2e1b3`, popovers `051bb3b` |
| 2 | In merchant-edit | `4a2e1b3` |
| 3 | In merchant-edit | `9dfef5a` |
| 4 | Dropped | D4: Victor, 20 Oct, "twee kolommen is ok" |
| 5 | Dropped | D6: arrows stay |
| 6 | Dropped | D6: stacked chips stay |
| 7 | Dropped | D6: Victor keeps the "Brushing & Beyond" badge |
| 8 | Parked / after launch | P2 title wrap, nothing built |
| 9 | Parked / after launch | The cards show from 990 px only (D5). The cut fourth card at 1440+ is in `component-professional-testimonials.css` (22rem minimum), which the homepage lane owns |
| 10 | In merchant-edit | D5, `629c591` |
| 11 | Parked / after launch | Asset owner |
| 12 | Parked / after launch | Theme-wide cookie banner, global lane |
| 13 | Parked / after launch | Copy, source-copy. The title is the Shopify product title since `50ad819` |
| 14 | In merchant-edit | D3, `8a555de`, `e5814b6` |
| 15 | Dropped | No gap found |
| 16 | In merchant-edit | D2, `82f9549`; the section is also hidden for the soft launch (`60912f6`) |
| 17 | Parked / after launch | The section is hidden (`60912f6`); the step media matter again when it comes back |
| 18 | Dropped | No gap found |
| 19 | Parked / after launch | D1: Victor, 20 Oct, "je hoeft mobiele koopbox niet aan te raken". The tables keep their sideways scroll for the soft launch |
| 20 | Parked / after launch | Follows D1 |
| 21 | Parked / after launch | P2 |
| 22 | Parked / after launch | Follows D1. The table buttons now go straight to checkout (`59ece89`, in merchant-edit) |
| 23 | Parked / after launch | `transition: all 0.4s` is still in `product-compare-plans.css:63` |
| 24 | Parked / after launch | P2 |
| 25 | Dropped | No gap found |
| 26 | Parked / after launch | Homepage and utopia own it. Its status is in their report, not checked here |
| 27 | In merchant-edit | D2, `82f9549` |
| 28a | In merchant-edit | Prices by language, `8a555de` |
| 28b | Parked / after launch | The wording "Care Credits back" is still in `templates/index.json:690` and `product.subscription-item.json:657`. Source-copy owns the text |
| 29 | Parked / after launch | Homepage and utopia own it |
| 30 | Dropped | Cut at the viewport edges by design |
| 31 | Waiting for Victor | See below |
| 32 | Parked / after launch | Victor, 22 Oct: "FAQ kunnen we even parkeren". The links keep `href="#"` for now; the options stay below for later |
| 33 | In progress | The plan is ready, but nothing is built. It waits for the desk's go |
| 34 | In progress | Still at `chronobiology-clock-karmicare.liquid:102` in merchant-edit. Waiting for the desk to say who changes it: homepage or pdp |
| 35a | In merchant-edit | Clock callouts are `h3.h4`, homepage `75de9a4` |
| 35b | In progress | The buybox `h5` is still at `treatment-journey.liquid:19`, `:69`. The plan is ready and waits for the desk's go |
| 36 | Parked / after launch | Info; recheck after 33–35 |
| 37 | Parked / after launch | Loop widget, off-limits |
| 38 | Parked / after launch | Amounts in other currencies than the euro. Victor decided the €40 reward on 22 Oct: A + C. It gets built later, together with the price per brushing. Nothing built yet |
| 39 | Parked / after launch | NL Welcome Kit names break in the middle of a word (release QA, live). The proposal waits for a go or the next fix moment |

**Counts (41 lines)**: in merchant-edit 9 · ready to land 0 · in progress 3 · waiting for Victor 1 · parked / after launch 20 · dropped 8.

### Waiting for Victor

**Row 32 (parked by Victor on 22 Oct; the options are kept for when it comes back): what should the 8 evidence links in the FAQ do while they have no document?** Today they point to `#`. Their text: View assessment summary, View notification, Read the opinion, View report, Read our science, See every document, Request the evidence pack, Practitioner evidence pack. The links sit in the FAQ content in Shopify admin, not in the theme.
- a) You fill in the real document links in admin. No theme change.
- b) The theme shows them as "Coming soon": visible but not clickable, with the same tooltip as in the header and the research section. No new copy.
- c) The theme hides each link until it has a real address.

Advice: **b** for the launch, because it uses the "Coming soon" state the site already has elsewhere. Switch to **a** as soon as the documents are online. The theme needs no change for a.

**Row 31: should the PDP get Figma's sections 08 (testimonials) and 09 (cost of waiting)?** Today they are not on the page, and care-comes-back stands where 09 was.
- a) Keep the page as it is for the soft launch.
- b) Add both sections. That needs approved texts and real testimonials, and neither is in the repo yet.

Advice: **a**, because building b needs content we do not have; revisit it after launch.

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

## Accessibility (axe-core 4.10.2, global coordinator, merchant-edit-preview, Day/Night, 393/2176; relayed 21 Oct)

Re-checked on this branch in the NL server HTML of the dev server (127.0.0.1:9293). Nothing is built before Victor chooses.

| # | Observed | Cause | P | Owner | Plan | Status |
|---|---|---|---|---|---|---|
| 32 | 8 links with `href="#"` in the FAQ evidence content: VIEW ASSESSMENT SUMMARY, VIEW NOTIFICATION, READ THE OPINION, VIEW REPORT, READ OUR SCIENCE, "See every document →", "Request the evidence pack…" (`.rda-link`), "Practitioner evidence pack and samples available →". | The links are HTML in the product FAQ metaobjects (`custom.product_faq` → `section_content`, `snippets/product-faq.liquid:25`), not theme markup. Same source as B-06. | P1 | Victor | a) Victor fills in the real document URLs in admin; no theme change. b) Shared Coming soon state (`snippets/kc-coming-soon.liquid`, as in the header and research CTA): `product-faq.liquid` turns `href="#"` inside `section_content` into a non-clickable link with the `kc.general.coming_soon` tooltip; no new copy. c) Hide them: `product-faq.liquid` drops `href="#"` links from `section_content` until a URL is set. | Parked (Victor, 22 Oct) |
| 33 | Gallery thumbnails 2–7: `aria-describedby="Thumbnail-…__main-N"` points to no id. | The id is built with `{%- capture thumbnail_id -%}` and renders with a trailing newline (`id="Thumbnail-…-2\n"`), so the reference never matches (`snippets/product-media-gallery.liquid:342`, `:404`). The hero thumbnail uses `assign` and is fine. | P2 | pdp | Build `thumbnail_id` with `assign` (or `\| strip`) in both places. | Open |
| 34 | chronobiology-clock: the slider's `aria-describedby="clock-help-…"` has no target (home and PDP). | No element with that id, and no help-text key exists (`sections/chronobiology-clock-karmicare.liquid:102`). | P2 | homepage / pdp | Remove the attribute (no copy needed), or add a visually hidden help line, which needs approved copy. Shared section: agree with the homepage lane who changes it. | Open (coordinate): still present after homepage 419fbfc (merchant-edit 75de9a4, line 102) |
| 35 | Heading jumps: h2 → h5 in the buybox (NL "Wat je zult voelen…", "Het Karmicare-effect", `snippets/treatment-journey.liquid:19`, `:69`); h2 → h4 in the clock callouts (`chronobiology-clock-karmicare.liquid`). | Tag chosen for size: `base.css` sizes the `h5` element itself. | P2 | pdp / homepage | `<h5 class="kc-journey-title">` → `<h3 class="kc-journey-title h5">` (Dawn's `.h5` class keeps the size); before/after shots to show nothing moves. | Clock part fixed by homepage 419fbfc (callouts `h3.h4`, merchant-edit 75de9a4). Buybox h2 → h5: open (pdp) |
| 36 | Other heading order: h2 "Land/regio" and "Taal" (localization drawer) and h2 "Trusted by professionals" with seven h3 come before the h1; the h1 is followed by an h2 with the same product title. | Header drawers and the professionals block render before the product section. | P2 | pdp | Note only; check after rows 33–35. | Info |
| 37 | Loop widget: duplicate ids. | `snippets/loop-widget*.liquid` / `assets/loop-widget.js`, off-limits. | P2 | Victor | Note only. | Off-limits |

## Currency (Victor, 22 Oct, via the desk and source-copy; parked, nothing built)

The shop also sells in CHF, GBP, USD and SEK. Product and plan prices are converted, but some amounts are fixed euro text or fixed euro cents.

| # | Observed | Where | P | Owner | Approach | Status |
|---|---|---|---|---|---|---|
| 38 | **a) Price per brushing.** It stays in euro when the visitor pays in another currency. **b) The €40 Dental Check-up Reward.** It is printed as a fixed amount, and in the Loop widget it takes the visitor's currency without being converted: 4000 cents go through `loopFormatMoney`, so a CHF visitor would see "CHF 40". | a) `templates/index.json:207`, `:332` `button_subtext` "€0.49 / brushing ritual" (two-formulas-karmicare, product-benefits-karmicare, also their schema defaults), and the compare_value metaobjects "Cost per brushing". b) `assets/loop-widget.js:2722` (receipt chip), `sections/care-comes-back.liquid` ("€40.00" and the check-up text), the check-up tooltip in `main-product.liquid`, and the sticky bar keys `kc.sticky_cart.credit_checkup_html` ("+ [credit] Care Credit + €40 Check-up Reward") and `checkup_info_html` | P2 | pdp, source-copy (keys) | b) decided A + C (below) | Parked / after launch: built later with a) |

**Already correct**: the plan prices, the Loop plan cards ("{{ amount }} / brushing"), and the Care Credit you earn (10 % or 20 %), which follows the payment currency. The amounts computed in the end CTA, the sticky bar and the plans table go through `snippets/kc-money.liquid`. It writes the euro by language, and any other currency in the shop money format. That is right for converted amounts. It would be wrong for a fixed euro amount passed in cents.

**a) Price per brushing.** Approach: calculate it instead of writing it.
- `button_subtext` gets an amount placeholder, for example "[price] / brushing ritual". Its two sections fill it with the plan price ÷ (Duos × 120 brushings) through the money filters, the same sum the Loop widget makes. The keys are new, so source-copy gets their names for NL and FR.
- The "Cost per brushing" row in the plans table is calculated the same way in `product-compare-plans.liquid`, in place of the metaobject text.
- Alternative: Victor limits the four non-EUR markets for the soft launch, and nothing changes in the theme.

**b) €40 Dental Check-up Reward.** What is fixed: Terms art. 11 says "€40 in Care Credit, eenmaal per lidmaatschapsjaar", only for Year members in an EU member state. The €5 for the questionnaire and the €59 refund per Duo are also in euro. So the reward does not apply in CHF, GBP or USD, and SEK (EU) needs a converted display.
- **Option a: €40 stays the legal amount, with the local equivalent next to it** (SEK: "€40 (≈ 4xx kr)"). Approach: the theme writes the €40 in euro and adds the amount converted at Shopify's rate, labelled as an approximation. The Loop widget stops passing 4000 as local cents. `loop-widget.js` is off-limits, so this needs Victor's OK for that file. No legal change.
- **Option b: fixed local amounts** (for example 400 kr), with the Terms changed for each currency. Approach: one amount per currency as a setting or metaobject, which the theme reads by `cart.currency`. This needs a legal change to the Terms first, plus new copy in every language.
- **Option c: hide the reward line outside the EU.** Approach: the theme and the Loop widget skip the check-up chip, the receipt row, the tooltip and the care-comes-back step when the market's country is not in the EU (CHF, GBP, USD). The line stays for EU markets, including SEK, which then still needs a or b.

**Decided by Victor, 22 Oct (via source-copy): A + C.** The Terms do not change.
- **A, EU markets with another currency (today Sweden, SEK).** €40 stays the official amount. The theme writes "€40" and adds the local amount next to it as an approximation at the active rate, for example "€40 (ca. 451 kr)". The converted amount is 4000 cents × `Shopify.currency.rate` in JS, or the cart currency's rate in Liquid, written in the shop money format. The euro part goes through the euro branch of `kc-money` whatever the cart currency.
- **C, markets outside the EU (today CH, GB and US).** The reward line is hidden: the check-up chip, the receipt row, the tooltip, the sticky bar's "+ €40 Check-up Reward" and the care-comes-back step. A market counts as EU by `localization.country.iso_code` (Liquid) or `Shopify.country` (JS), checked against a list of the 27 EU country codes in one snippet, so no copy is needed for it.
- **New key for source-copy** (sent on 22 Oct): `kc.general.approx_amount`, EN "(approx. [amount])". `[amount]` is filled with the local amount, the same placeholder style as `kc.receipt.*`. Source-copy has agreed the wording: NL "(ca. [amount])", FR "(env. [amount])"; the FR lane still confirms the FR. `theme_keys.py check` fails on a key that no theme file reads. So the build commit is sent to source-copy, and they add the key to all 31 locales on top of it. The theme puts it after the euro amount with a no-break space. No new settings.
- `loop-widget.js` (receipt chip, line 2722) is in scope of this decision, so the edit there is covered when it gets built.

## NL Welcome Kit names (release QA, live, 22 Oct; parked, nothing built)

| # | Observed | Cause | P | Owner | Proposal | Status |
|---|---|---|---|---|---|---|
| 39 | NL Welcome Kit names break in the middle of a word in the buybox: "Ochtendtandenb\|orstel 2.0", "Avondtandenbor\|stel 2.0" at 390 (100 px name column) and at 1024 (111 px). At 1440 (147 px) they fit on one line. In the plans-table popover (260 px wide), all three names fit on one line at 390 and 1440 (24 px, one line, on the live theme with the popover held open). QA's plans-table case is not reproduced; it needs QA's width. | Loop's `.loop-welcome-kit-product-link { word-break: break-word }` (`snippets/loop-widget.css.liquid:594`, off-limits). A long Dutch compound has no space, so it is cut wherever the line ends. | P2 | pdp (CSS), source-copy (only for option 3) | See below | Parked / after launch |

Tested on the live theme (karmicare/main, `/nl/`, Night) with CSS injected through the approved helper. Shots are in `docs/pdp/shots/kitnames-nl-*`.
1. **`hyphens: auto` (proposal).** `kc-buybox.css` sets `word-break: normal; overflow-wrap: break-word; hyphens: auto` on `.kc-buybox .loop-welcome-kit-product-link`. The page already has `lang="nl"`. Result at 390 and 1024: "Ochtendtanden-/borstel 2.0" and "Avondtandenbor-/stel 2.0", with a hyphen at a syllable. At 1440 nothing changes. The heights stay the same (390: 44 px, 1024: 40 px), so nothing below moves. It is one theme rule with no copy, and it also covers FR and later names.
2. **Wrap at spaces only** (`word-break: normal`, no hyphens). The full word does not fit: at 390, "Ochtendtandenborstel" and "Avondtandenborstel" run into each other. Rejected.
3. **`&shy;` in the NL product titles** (source-copy, in Translate & Adapt): "Ochtend&shy;tanden&shy;borstel". The break then falls at the compound boundary ("Ochtend-/tandenborstel 2.0"). That is the neatest, but it changes store data that also shows in checkout and emails. It could be added on top of 1 later, because with `hyphens: auto` the soft hyphens are used first.

Proposal: **1** at the next fix moment; 3 only if Victor wants the breaks at the compound boundary.

## Checked with no gap

- Horizontal overflow: none at 393, 450, 768, 1024, 1440, 1920, 2560, Night and Day (`documentElement.scrollWidth` = viewport).
- Wide screens: header, main-product, how-it-works, comparison, plans, care-comes-back and footer share the 1480 px page width and its 32 px gutter. Their left edges line up at 252 (1920) and 572 (2560).
- Mission card (Marlide 300, "Strengthen your teeth. Strengthen yourself."): fits at every width, Day and Night.

## Changelog

- 22 Oct: added "Status 22 Oct", with one status per row, counts and the questions for Victor. Every theme row was checked against merchant-edit `31407fb` with `git merge-base --is-ancestor`.
- 22 Oct: row 32 (FAQ evidence links) is parked at Victor's request ("FAQ kunnen we even parkeren").
- 22 Oct: row 38 added and parked: the price per brushing and the €40 Dental Check-up Reward in other currencies (desk, for Victor; nothing built).
- 22 Oct: row 38: Victor decided A + C for the €40 reward; the key `kc.general.approx_amount` went to source-copy. Row 39 added: NL Welcome Kit names, with a proposal (parked).
