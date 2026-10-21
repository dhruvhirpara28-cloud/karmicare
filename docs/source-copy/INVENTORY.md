# EN source inventory · every page of the live store

The English that the live store renders, one entry per string. Batches 01–03 (homepage, Duo PDP, header and footer) come from B1a, with its corrections applied; batches 04–08 (legal, other products, content pages, collections and blog, system pages) come from B2 and are inventoried as they are, without corrections. NL and FR translators start from here.

- **Captured**: batches 01-03: 2026-10-19 19:15 CEST; batches 04-08: 2026-10-19 20:15 CEST (karmicares.myshopify.com, live theme = 3bae259). Theme text comes from this branch (`karmicare/soft-launch-source-copy`); admin-held text comes from the public live pages and `/products/<handle>.js`.
- **Updated 21 Oct** from the integration branch at `41ae772` (homepage lane, merchant-edit `97ce2b7`):
  - the stat-strip tagline and the three practitioner titles (on both templates: *Therapist* → *Practitioner*) are `corrected`;
  - the homepage FAQ rows `kLMHax`, `7jmEGi`, `AL3DKF` and `qUxYCn` carry new questions and answers (`corrected`, `old_en` kept), and the two former placeholders are no longer `blocked`;
  - the new FAQ block `Pz4mRk` adds three entries at the end of batch 01 (#226–228), so the earlier numbers stay;
  - the removed block `4KMG6C` and the two emptied PDP step numbers are `retired`;
  - the theme key `kc.clock.loading` (the clock's aria-valuetext before its script runs) is inventoried as `locale:kc.clock.loading` (#229), for release QA B-03/B-04;
  - the announcement line is `corrected` to Victor's G-1 text from `karmicare/soft-launch-global` `3c03acb` (“… FOR MEMBERS · BELGIAN-MADE · CIRCADIAN ORAL CARE SINCE 2017”, claim C103). `sections/header-group.json` on this branch keeps the old text until the global lane lands;
  - the sticky-bar default `liquid:sections/main-product.liquid:1104` (*Free*, setting `kit_free`) is `retired`: global-nav `27691cb` (NV-13) removes the setting and its markup, and the key `kc.sticky_cart.kit_free_html` leaves every locale;
  - two PDP CTAs follow Victor's "Begin your" (global-nav `6c07148`): the buy-box text per plan (*Begin your 60-Day Rhythm* / *Begin your Karmicare Year*, `corrected`) and the sticky-bar default `main-product.liquid:1024` (*Begin your Karmicare Year*), both with `old_en`.
- **Machine-readable**: `en-source.json` (all entries) and `batches/<batch>.json` (one file per batch, with its digest).
- **Digest rule**: a batch digest is the sha1 over its entries' `sha1(en)` values, sorted and joined with `\n`. A later EN change alters only the digest of the batch that holds the string. `python3 docs/source-copy/digest.py` recomputes and checks every value, in `en-source.json` and independently in each batch file (entry hashes, file digest, ids and metadata against the canonical entries), and exits 1 on any mismatch; `python3 docs/source-copy/digest_selftest.py` proves that it rejects an altered EN value, a substituted id and a metadata-only change.

| Batch | Entries | Digest |
|---|---:|---|
| `batch-01-homepage` | 229 | `7694e7acce33a1e22a90de53273f2c90a8ddd70a` |
| `batch-02-pdp` | 477 | `e4709cc6bbf22152ae64461abc1ea69bcca08839` |
| `batch-03-header-footer` | 41 | `a853d438d503867882d711cd4fa5a4a93c29759f` |
| `batch-04-legal` | 974 | `98fda69496b9cbe0ad39d2b7099549341113349c` |
| `batch-05-products` | 77 | `5ab678a91ffc223be63e7f87a68783bacc62a744` |
| `batch-06-content-pages` | 22 | `3dee3b56341f67b113dcd59eb85d3a2e3f21d628` |
| `batch-07-collections-blog` | 709 | `9597904c4ef875006a7d8a76bebbaa43d0faaca0` |
| `batch-08-system` | 46 | `306f141fadf2231629b14eff578e01fc228ff7a3` |

## How to read an entry

`{id, batch, page, resource_type, file_or_handle, key_path, en, sha1, status, never_translate, notes}` as the brief asks, plus, where they apply: `old_en`/`old_sha1` (corrected strings), `claims` (claim ids in CLAIMS-REVIEW.md, batches 01–03), `claim_status` (every entry that carries a claim: in batches 01–03 the strictest status of its `claims`, in batches 05–07 the hand review), `claim_basis` (batches 05–07), `claim_hold_waived` (on the 119 unsupported-claim entries: "2026-10-20 Victor, translation only"; NL/FR translate them and flag pending-claim-review, the claims review still gates publication), `blocked` (no approved copy: a placeholder, or EN that breaks a brand rule),`legal` (legal text: legal-review before publishing), `legacy` (pre-2.0 page, held in NL/FR), `retired` (the theme no longer reads the setting or key; held in NL/FR and left out of registration, with the reason), `setting_type`, `section_type`, `rendered` (false for disabled blocks).

| status | Meaning for translators |
|---|---|
| `approved` | The live EN, accepted as the source. Translate. |
| `corrected` | Changed in this batch; `old_en` holds the previous text. Translate the new `en`. |
| `needs-review` | EN may still change: a claim waits for sign-off or an open defect is listed in `notes`. Translate, and expect a re-run when the batch digest changes. Entries with `blocked` hold `[NEEDS APPROVED COPY]`: do not translate. |
| `needs-key` | Hardcoded English in theme code (`key_path` = file:line). The localization worker must turn it into a translation key before it can be translated. |
| `admin-held` | Lives in the Shopify admin (product, metafield, metaobject, selling plan, menu, shop settings). Translate through Translate & Adapt; changes go through the admin owner. |

`resource_type` uses the brief's values plus the ones the brief has no slot for: `shop` (shop-level SEO and system-page titles), `navigation` (menus), `page`, `policy`, `article`, `blog` and `collection` (Shopify resources whose text lives in the admin). Admin text captured from the live page is stored one rendered segment per entry (`key_path` ends in `#nn`), because the field structure is only visible in the admin. Long bodies (pages, policies, articles, product descriptions) are split into block-level segments (`#bNNN`, in document order, inline markup kept) so they can be translated paragraph by paragraph and joined back in order.

## Counts

By resource type:

| Batch | template_setting | section_group | theme_locale | app | product | metafield | metaobject | shop | navigation | page | policy | article | blog | collection | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `batch-01-homepage` | 192 | 0 | 23 | 12 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 229 |
| `batch-02-pdp` | 156 | 0 | 53 | 14 | 16 | 175 | 63 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 477 |
| `batch-03-header-footer` | 0 | 6 | 24 | 1 | 0 | 0 | 0 | 0 | 10 | 0 | 0 | 0 | 0 | 0 | 41 |
| `batch-04-legal` | 143 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 357 | 474 | 0 | 0 | 0 | 974 |
| `batch-05-products` | 16 | 0 | 0 | 18 | 43 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 77 |
| `batch-06-content-pages` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 22 | 0 | 0 | 0 | 0 | 22 |
| `batch-07-collections-blog` | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 698 | 1 | 9 | 709 |
| `batch-08-system` | 3 | 0 | 36 | 0 | 0 | 0 | 0 | 6 | 0 | 0 | 0 | 0 | 0 | 1 | 46 |
| **All** | **511** | **6** | **136** | **45** | **59** | **175** | **63** | **8** | **10** | **379** | **474** | **698** | **1** | **10** | **2575** |

By status:

| Batch | approved | corrected | needs-review | needs-key | admin-held | never_translate |
|---|---:|---:|---:|---:|---:|---:|
| `batch-01-homepage` | 145 | 21 | 30 | 31 | 2 | 16 |
| `batch-02-pdp` | 146 | 4 | 23 | 36 | 268 | 32 |
| `batch-03-header-footer` | 17 | 2 | 1 | 10 | 11 | 5 |
| `batch-04-legal` | 143 | 0 | 0 | 0 | 831 | 0 |
| `batch-05-products` | 14 | 0 | 2 | 0 | 61 | 0 |
| `batch-06-content-pages` | 0 | 0 | 0 | 0 | 22 | 0 |
| `batch-07-collections-blog` | 1 | 0 | 0 | 0 | 708 | 0 |
| `batch-08-system` | 39 | 0 | 0 | 0 | 7 | 0 |

Text settings: `templates/index.json` 192 (189 at capture, plus the FAQ block added on 21 Oct), `templates/product.subscription-item.json` 156, `sections/header-group.json` 2, `sections/footer-group.json` 4. The brief estimated about 149 and 119; these counts take every non-empty `text`, `textarea`, `richtext`, `inline_richtext` and non-SVG `html` value, including the sections that repeat on both templates and two disabled PDP blocks (marked `rendered: false`). Left out: 7 settings whose value is a Liquid pointer to a metafield (their text is inventoried as admin-held) and 11 technical text settings (CSS gradients, file names, a product handle, the empty Welcome Kit plan list).

| File | text | textarea | richtext | inline_richtext | html |
|---|---:|---:|---:|---:|---:|
| `templates/index.json` | 127 | 6 | 23 | 36 | 0 |
| `templates/product.subscription-item.json` | 104 | 6 | 7 | 39 | 0 |
| `sections/header-group.json` | 2 | 0 | 0 | 0 | 0 |
| `sections/footer-group.json` | 0 | 0 | 1 | 3 | 0 |

No custom section reads `locales/en.default.json`: every custom string is either a setting or hardcoded. The `theme_locale` entries with status `approved` are Dawn keys seen on these pages; NL and FR for them already ship in `locales/nl.json` and `locales/fr.json`. Global strings outside the page sections (skip links, cart drawer, `<title>` pattern) are batch B1b.

## Corrections in this batch

Text values only, in `templates/index.json` and `sections/footer-group.json`; keys and structure unchanged.

| Entry | Old | New | Why |
|---|---|---|---|
| `index:stat_strip_karmicare/tagline` | …NAL DENTISTS, HEALTH ENTHOUSIASTS | …NAL DENTISTS, HEALTH ENTHUSIASTS | Spelling: ENTHOUSIASTS → ENTHUSIASTS. |
| `index:two_formulas_karmicare/button_subtext` | €0,49 / brushing ritual | €0.49 / brushing ritual | Price per brushing renders €0.49 in EN (COMMON-RULES §3); the comma is the NL/FR format. |
| `index:product_benefits_karmicare_bcQ6tp/button_subtext` | €0,49 / brushing ritual | €0.49 / brushing ritual | As above. |
| `index:product_benefits_karmicare_bcQ6tp/card_jN7XcL/text` | …minerals your mouth need in one press. Hygienic, precise, nothing wasted. | …minerals your mouth needs in one press. Hygienic, precise, nothing wasted. | Grammar: 'your mouth need' → 'your mouth needs'. |
| `index:km_faq_accordion_FYcArV/faq_item_kLMHax/answer` | Because your mouth doesn’t do the same job all day. Daytime is exposure — acids, sug… | [NEEDS APPROVED COPY] | Boilerplate (row 1's answer) replaced by a placeholder: FAQ-0202 is Draft with Regulatory 'Needs review', so its status does not allow use. |
| `index:km_faq_accordion_FYcArV/faq_item_7jmEGi/answer` | Because your mouth doesn’t do the same job all day. Daytime is exposure — acids, sug… | [NEEDS APPROVED COPY] | Boilerplate replaced by a placeholder: no approved answer exists (homepage-faq-on-accordion-component.md row 3). |
| `index:km_faq_accordion_FYcArV/faq_item_AL3DKF/answer` | Because your mouth doesn’t do the same job all day. Daytime is exposure — acids, sug… | A bioidentical mineral — the same substance your enamel is made of. It remineralises teeth, reduces sensitivi… | 45 brief Q3 as adapted in Figma 3002:20280 row 4 (British spelling). |
| `index:km_faq_accordion_FYcArV/faq_item_qUxYCn/answer` | Because your mouth doesn’t do the same job all day. Daytime is exposure — acids, sug… | No — spit and carry on. Karmicare formulas are certified safe to remain in your mouth, giving nHAp and xylito… | 45 brief Q5 as adapted to the question in Figma 3002:20280 row 5. |
| `index:km_faq_accordion_FYcArV/faq_item_4KMG6C/answer` | Because your mouth doesn’t do the same job all day. Daytime is exposure — acids, sug… | Mineral remineralisation takes time — most members feel the sensitivity shift in 2–4 weeks and see visible br… | 45 brief Q10 as adapted in Figma 3002:20280 row 6. |
| `index:featured_product_3XpDKw/icon_with_text_wUdX3G/heading_1` | 60 day money back guarantee | 60-day money-back guarantee | Format: matches the PDP and the announcement bar ('60-day money-back guarantee'). |
| `footer-group:footer/copyright_text` | …wake + Asleep) is a Belgium product formulated by certified chemists and manufacture… | …wake + Asleep) is a Belgian product formulated by certified chemists and manufactured under GMP. Formulations… | Grammar: 'a Belgium product' → 'a Belgian product'. |

Not changed, because no text setting in the allowed files carries it:

- **€0.42 per brushing** on the Year: an admin metaobject cell (`shop.metaobjects.compare_value`), see the handoff in REPORT.md. The homepage and PDP template text already say €0.49 after this batch.
- **Welcome Kit €21**: the buy box fills `[value]` at runtime from the kit items' prices (`assets/loop-widget.js:2749`); the 2.0 brushes and floss cost €6 + €6 + €9 = €21 in the live product JSON, and the selling-plan descriptions say €21. Only the compare table shows €18, because its Welcome Kit row references the older €4 and €5 brushes (admin).
- **'3 now, 3 in month 6'**: already in the Year selling-plan name and description (Loop, admin). The theme text that presents the Year without it is the sticky bar default `The Karmicare Year · 6 Duos` in `sections/main-product.liquid` (PDP owner) and the compare-table Year cells (admin).

## Hardcoded strings that need keys

| Batch | File:line | EN | Notes |
|---|---|---|---|
| 01 | `sections/hero-karmicare.liquid:149` | Karmicare Oral Rhythm Hero | aria-label fallback; section setting accessibility_label is blank, so this renders |
| 01 | `sections/hero-karmicare.liquid:209` | Karmicare Oral Care System | img alt fallback when the hero image has no alt (renders live) |
| 01 | `sections/hero-karmicare.liquid:242` | Day and Night Oral Rhythm Switcher | aria-label |
| 01 | `sections/hero-karmicare.liquid:251` | {{ label }} mode | aria-label suffix ' mode' after the AWAKE / ASLEEP label (also line 261) |
| 01 | `sections/stat-strip-karmicare.liquid:84` | Karmicare Stats and Highlights | aria-label |
| 01 | `sections/chronobiology-clock-karmicare.liquid:101` | Explore your mouth's 24-hour clock | aria-label of the clock slider; also on the PDP |
| 01 | `sections/chronobiology-clock-karmicare.liquid:153` | your mouth right now: | clock caption; the JS sets the same text (assets/chronobiology-clock-karmicare.js:88); also on the PDP |
| 01 | `assets/chronobiology-clock-karmicare.js:88` | your mouth at this hour: | clock caption while dragging (JS) |
| 01 | `assets/chronobiology-clock-karmicare.js:91` | . Release to return to now. | aria-valuetext tail while dragging (preview branch); the live branch '. Current local time.' is its own entry, liquid:assets/chronobiology-clock-karmicare.js:9… |
| 01 | `assets/chronobiology-clock-karmicare.js:91` | . Current local time. | aria-valuetext tail at rest (live branch, not dragging); the preview branch is liquid:assets/chronobiology-clock-karmicare.js:91. Clock on the homepage and the… |
| 01 | `assets/chronobiology-clock-karmicare.js:11` | saliva is only now picking up after the night, and the enamel is least protecte… | hourly clock message shown under the clock (JS array 'windows'); also on the PDP; claims C54: needs-review (CLAIMS-REVIEW.md) |
| 01 | `assets/chronobiology-clock-karmicare.js:12` | breakfast and coffee dropped the pH within minutes — saliva spends the next hal… | hourly clock message shown under the clock (JS array 'windows'); also on the PDP |
| 01 | `assets/chronobiology-clock-karmicare.js:13` | lunch restarts the cycle: every eating occasion opens a fresh acid window, what… | hourly clock message shown under the clock (JS array 'windows'); also on the PDP |
| 01 | `assets/chronobiology-clock-karmicare.js:14` | grazing hours — the most frequent acid challenge of the day, and it is how ofte… | hourly clock message shown under the clock (JS array 'windows'); also on the PDP |
| 01 | `assets/chronobiology-clock-karmicare.js:15` | the last big acid window of the day; after this, saliva starts winding down | hourly clock message shown under the clock (JS array 'windows'); also on the PDP |
| 01 | `assets/chronobiology-clock-karmicare.js:16` | melatonin is rising and salivary flow is dropping — what is left on the enamel … | hourly clock message shown under the clock (JS array 'windows'); also on the PDP |
| 01 | `assets/chronobiology-clock-karmicare.js:17` | saliva is near its minimum and clearance has almost stopped: the longest unguar… | hourly clock message shown under the clock (JS array 'windows'); also on the PDP |
| 01 | `sections/km-faq-accordion.liquid:155` | ALL | FAQ filter tab |
| 01 | `sections/featured-product.liquid:627` | Free | Welcome Kit item price label in the featured product (homepage and PDP end CTA) |
| 01 | `snippets/loop-widget-standard.liquid:101` | Start here | fallback renders on the homepage because its loop_subscriptions block has no plans_eyebrow value (the PDP sets it). Off-limits Loop widget file: Loop/PDP owner |
| 01 | `snippets/loop-widget-standard.liquid:103` | Choose how to begin | as above (plans_heading) |
| 01 | `snippets/loop-widget-standard.liquid:109` | Selling Plans | fieldset legend; off-limits Loop widget file |
| 01 | `snippets/loop-widget-standard.liquid:123` | One time Purchase | one-time option label (also assets/loop-widget.js:694 fallback); off-limits Loop widget file |
| 01 | `snippets/loop-widget-standard.liquid:140` | each | price unit (also line 196); off-limits Loop widget file |
| 01 | `assets/loop-widget.js:2452` | / {{ days }} days | plan card short label on 60-day plans; the Year branch '/ year' is its own entry, liquid:assets/loop-widget.js:2452:annual. Plan cards in the homepage featured… |
| 01 | `assets/loop-widget.js:2452` | / year | plan card short label on the Year (isAnnual branch); the 60-day branch is liquid:assets/loop-widget.js:2452. Plan cards in the homepage featured product and th… |
| 01 | `assets/loop-widget.js:2463` | Renews | replaces 'ships' in the selling-plan option text on non-annual plans ('ships every 60 days' → 'Renews every 60 days', regex /ships/i). Once the admin phrase is… |
| 01 | `assets/loop-widget.js:2464` | {{ amount }} / brushing | per-brushing line on every plan card; {{ amount }} is the plan price ÷ brushings, formatted by the store money format (EN shows €0,49, see B1a decision 5). Pla… |
| 01 | `assets/loop-widget.js:2468` | Renews every year | Year plan card line; off-limits Loop widget file |
| 01 | `assets/loop-widget.js:2213` | {{ value }} value · free | Welcome Kit badge; off-limits Loop widget file |
| 01 | `snippets/loop-subscriptions.liquid:10` | Rendering loop-subscriptions | placeholder text in the markup (featured-product.liquid:542 and main-product.liquid:616 test for it); not meant to be read. Check it stays hidden |
| 02 | `sections/main-product.liquid:147` | Or | joins the buy button and the 'Try once' link |
| 02 | `snippets/professional-testimonials.liquid:61` | PROFESSIONAL PARTNERS | eyebrow of the buy-box professionals carousel |
| 02 | `snippets/product-category-strip.liquid:36` | Karmicare, Biorhythmic Oral Care | aria-label |
| 02 | `snippets/product-highlights.liquid:160` | Product highlights | aria-label |
| 02 | `sections/main-product.liquid:931` | 60-Day Rhythm · Awake + Asleep | sticky bar: schema default of sticky_cart setting 'title_rhythm'. The PDP template stores only button_text, so this default renders and is invisible to Transla… |
| 02 | `sections/main-product.liquid:937` | The Karmicare Year · 6 Duos | sticky bar: schema default of sticky_cart setting 'title_year'. The PDP template stores only button_text, so this default renders and is invisible to Translate… |
| 02 | `sections/main-product.liquid:943` | Try Once · 1 Duo | sticky bar: schema default of sticky_cart setting 'title_once'. The PDP template stores only button_text, so this default renders and is invisible to Translate… |
| 02 | `sections/main-product.liquid:954` | [price] every 60 days | sticky bar: schema default of sticky_cart setting 'price_rhythm'. The PDP template stores only button_text, so this default renders and is invisible to Transla… |
| 02 | `sections/main-product.liquid:960` | [price] per year | sticky bar: schema default of sticky_cart setting 'price_year'. The PDP template stores only button_text, so this default renders and is invisible to Translate… |
| 02 | `sections/main-product.liquid:966` | [price] one time | sticky bar: schema default of sticky_cart setting 'price_once'. The PDP template stores only button_text, so this default renders and is invisible to Translate… |
| 02 | `sections/main-product.liquid:977` | + [credit] Care Credit back | sticky bar: schema default of sticky_cart setting 'credit'. The PDP template stores only button_text, so this default renders and is invisible to Translate & A… |
| 02 | `sections/main-product.liquid:983` | + [credit] Care Credit + €40 Check-up Reward | sticky bar: schema default of sticky_cart setting 'credit_checkup'. The PDP template stores only button_text, so this default renders and is invisible to Trans… |
| 02 | `sections/main-product.liquid:989` | Care Credit is Karmicare credit: spend it on more care, never on your dental bi… | sticky bar: schema default of sticky_cart setting 'credit_info'. The PDP template stores only button_text, so this default renders and is invisible to Translat… |
| 02 | `sections/main-product.liquid:995` | Complete a dental check-up from month 6 or onwards, verified by your dentist. €… | sticky bar: schema default of sticky_cart setting 'checkup_info'. The PDP template stores only button_text, so this default renders and is invisible to Transla… |
| 02 | `sections/main-product.liquid:1006` | Delivery & what's included | sticky bar: schema default of sticky_cart setting 'panel_label'. The PDP template stores only button_text, so this default renders and is invisible to Translat… |
| 02 | `sections/main-product.liquid:1012` | Change | sticky bar: schema default of sticky_cart setting 'change_label'. The PDP template stores only button_text, so this default renders and is invisible to Transla… |
| 02 | `sections/main-product.liquid:1018` | Begin your 60-Day Rhythm | sticky bar: schema default of sticky_cart setting 'cta_rhythm'. The PDP template stores only button_text, so this default renders and is invisible to Translate… |
| 02 | `sections/main-product.liquid:1024` | Begin your Karmicare Year | sticky bar: schema default of sticky_cart setting 'cta_year'. The PDP template stores only button_text, so this default renders and is invisible to Translate &… |
| 02 | `sections/main-product.liquid:1030` | Try once | sticky bar: schema default of sticky_cart setting 'cta_once'. The PDP template stores only button_text, so this default renders and is invisible to Translate &… |
| 02 | `sections/main-product.liquid:1036` | Free Fast Delivery: 24 hours in Benelux. 2–3 days in rest of Europe | sticky bar: schema default of sticky_cart setting 'delivery_free'. The PDP template stores only button_text, so this default renders and is invisible to Transl… |
| 02 | `sections/main-product.liquid:1042` | Shipping calculated at checkout | sticky bar: schema default of sticky_cart setting 'delivery_once'. The PDP template stores only button_text, so this default renders and is invisible to Transl… |
| 02 | `sections/main-product.liquid:1049` | Welcome Kit: two toothbrushes + floss | sticky bar: schema default of sticky_cart setting 'kit'. The PDP template stores only button_text, so this default renders and is invisible to Translate & Adap… |
| 02 | `sections/main-product.liquid:1055` | 60-day money-back guarantee | sticky bar: schema default of sticky_cart setting 'guarantee_member'. The PDP template stores only button_text, so this default renders and is invisible to Tra… |
| 02 | `sections/main-product.liquid:1061` | 14-day money-back guarantee | sticky bar: schema default of sticky_cart setting 'guarantee_once'. The PDP template stores only button_text, so this default renders and is invisible to Trans… |
| 02 | `sections/main-product.liquid:1067` | Pause or stop anytime | sticky bar: schema default of sticky_cart setting 'stop_rhythm'. The PDP template stores only button_text, so this default renders and is invisible to Translat… |
| 02 | `sections/main-product.liquid:1073` | Renews yearly · stop anytime before renewal | sticky bar: schema default of sticky_cart setting 'stop_year'. The PDP template stores only button_text, so this default renders and is invisible to Translate … |
| 02 | `sections/main-product.liquid:1080` | [per_brushing] per brushing | sticky bar: schema default of sticky_cart setting 'per_brushing'. The PDP template stores only button_text, so this default renders and is invisible to Transla… |
| 02 | `sections/main-product.liquid:1087` | Not ready for a membership? Try once for [price] | sticky bar: schema default of sticky_cart setting 'try_once'. The PDP template stores only button_text, so this default renders and is invisible to Translate &… |
| 02 | `sections/main-product.liquid:1098` | Awake & Asleep AM/PM Oral Care System | sticky bar: schema default of sticky_cart setting 'package_name'. The PDP template stores only button_text, so this default renders and is invisible to Transla… |
| 02 | `sections/main-product.liquid:1104` | Free | sticky bar: schema default of sticky_cart setting 'kit_free'. The PDP template stores only button_text, so this default renders and is invisible to Translate &… |
| 02 | `sections/product-compare-plans.liquid:39` | Compare plans | aria-label |
| 02 | `sections/product-compare-plans.liquid:55` | Compare | label-column head |
| 02 | `sections/product-compare-plans.liquid:98` | · {{ total_value }} Value | Welcome Kit tooltip; total from the referenced products (live: €18, see handoff) |
| 02 | `sections/product-compare-plans.liquid:100` | Free | Welcome Kit tooltip (also line 115 per item) |
| 02 | `sections/product-compare-plans.liquid:234` | Not included | aria-label of the '—' cell (also line 243) |
| 02 | `sections/product-compare-plans.liquid:241` | Included | aria-label of the '✓' cell |
| 03 | `sections/header.liquid:1077` | Coming soon | schema default of a header setting that sections/header-group.json does not store, so the default renders on menu links without a page (header.liquid, header-d… |
| 03 | `sections/footer.liquid:660` | Email | newsletter field label |
| 03 | `sections/footer.liquid:667` | you@example.com | newsletter placeholder |
| 03 | `sections/footer.liquid:679` | Join | newsletter submit button |
| 03 | `sections/footer.liquid:694` | By subscribing you agree to the Terms of Use & Privacy Policy . | consent line, two links (lines 694-695) |
| 03 | `sections/footer.liquid:850` | Language | locale picker group title |
| 03 | `sections/footer.liquid:868` | Country/Region | locale picker group title |
| 03 | `sections/footer.liquid:1034` | Terms and Conditions | legal link text: schema default, not stored in footer-group.json |
| 03 | `sections/footer.liquid:1046` | Privacy Policy | legal link text: schema default, not stored in footer-group.json |
| 03 | `sections/footer.liquid:1058` | Consumer Rights | legal link text: schema default, not stored in footer-group.json |

Fallbacks that exist in code but do not render today (the setting is filled): `sections/hero-karmicare.liquid:302` 'Backed by health professionals', `:320` 'Health professional', `sections/main-product.liquid:192` Welcome Kit row, `snippets/buy-buttons.liquid:102/196` 'Begin Now', `sections/product-compare-plans.liquid:289` 'Choose plan' and `:425` footer default, `snippets/treatment-journey.liquid:55/108/130-131` 'Read more' / 'Read less', and the section schema defaults of the custom sections. The localization worker should key them together with the rendered ones.

## Brand-rule scan (Awake before Asleep, banned words, duplicated words)

- **Duplicated words**: none found in any entry (the brief's example 'you look you look forward to' does not occur on these pages).
- **Asleep before Awake**: one hit, the admin image alt 'with evening care at 22:00 and morning care at 06:40' (`media.69840178020733.alt`). Handoff.
- **Banned words** in customer copy (excluding legal names, meta tags, FAQ questions and the first-contact uses that tone-of-voice allows):

| Entry | Word | Text |
|---|---|---|
| `index:two_formulas_karmicare/ingredients_list` | prevention | FLUORIDE-FREE & SLS-FREE MICROBIOME-CONSCIOUS NANO-HYDROXYAPATITE (NHAP) SYNERGETIC EFFECT VELVETY FOAM GLYCO… |
| `index:trusted_professionals_HAqYth/card_CtQgU9/hover_text` | products | “As a nutritional therapist specialized in female hormones, I’m extremely careful about what I put into my bo… |
| `index:trusted_professionals_HAqYth/card_CtQgU9/hover_text` | use | “As a nutritional therapist specialized in female hormones, I’m extremely careful about what I put into my bo… |
| `index:km_faq_accordion_FYcArV/faq_item_AL3DKF/answer` | used | A bioidentical mineral — the same substance your enamel is made of. It remineralises teeth, reduces sensitivi… |
| `product.subscription-item:main/highlights_slider_9wAjAb/text_1` | used | Used by 100+ kPNI practitioners & functional dentists |
| `product.subscription-item:main/loop_subscriptions_WEk4XJ/pricing_summary_care_credit_tooltip` | products | Care Credit is Return on Care in euros — spendable on member products and accessories. It lands in your accou… |
| `product.subscription-item:main/loop_subscriptions_WEk4XJ/pricing_summary_checkup_tooltip` | prevention | Complete a dental check-up from month 6 or onwards, verified by your dentist. €40 in Care Credit is added to … |
| `product.subscription-item:main/treatment_journey_block/disclaimer_text` | use | * What members report with continued use — individual experiences vary. |
| `product.subscription-item:trusted_professionals_HAqYth/card_CtQgU9/hover_text` | products | “As a nutritional therapist specialized in female hormones, I’m extremely careful about what I put into my bo… |
| `product.subscription-item:trusted_professionals_HAqYth/card_CtQgU9/hover_text` | use | “As a nutritional therapist specialized in female hormones, I’m extremely careful about what I put into my bo… |
| `admin:karmicare-biorhythmic-oral-care-system:body_html` | toothpastes | Your mouth doesn’t stay the same from morning to night. Two toothpastes, one system. Formulated around your m… |
| `admin:karmicare-biorhythmic-oral-care-system:media.69840177987965.alt` | use | How to use Karmicare: rinse first, use 1 pump, spit and don't rinse. Leave-on toothpaste, fluoride-free, SLS-… |
| `admin:karmicare-biorhythmic-oral-care-system:selling_plan.712106115453.description` | products | 10% Care Credit back in your account i Return on Care is our give-back: 10% of every 60-day supply comes back… |
| `admin:karmicare-biorhythmic-oral-care-system:selling_plan.712106115453.description` | prevention | 10% Care Credit back in your account i Return on Care is our give-back: 10% of every 60-day supply comes back… |
| `admin:karmicare-biorhythmic-oral-care-system:selling_plan.712155431293.description` | products | 20% Care Credit back in your account i The year plan earns 20% Return on Care — 2× the bi-monthly rate — in C… |
| `admin:karmicare-biorhythmic-oral-care-system:selling_plan.712155431293.description` | prevention | 20% Care Credit back in your account i The year plan earns 20% Return on Care — 2× the bi-monthly rate — in C… |
| `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#17` | toothpaste | Awake Morning Toothpaste (2.0) |
| `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#19` | toothpaste | Asleep Evening Toothpaste (2.0) |
| `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#33` | use | How to use |
| `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#43` | use | Rinsing ends it the moment it starts; the minerals leave with the water. Left on, the contact carries on long… |
| `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#56` | use | Safety-assessed for leave-on use |
| `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#60` | products | Notified on the EU cosmetic products portal |
| `admin:karmicare-biorhythmic-oral-care-system:custom.compare_table|shop.metaobjects.compare_value#06` | products | Return on Care is our give-back: a share of every delivery comes back to you as Care Credit — in euros, spend… |
| `admin:karmicare-biorhythmic-oral-care-system:custom.compare_table|shop.metaobjects.compare_value#08` | products | Care Credit is what Return on Care pays out — in euros, spendable on member products and accessories. We beli… |
| `admin:karmicare-biorhythmic-oral-care-system:custom.compare_table|shop.metaobjects.compare_value#08` | prevention | Care Credit is what Return on Care pays out — in euros, spendable on member products and accessories. We beli… |
| `admin:karmicare-biorhythmic-oral-care-system:custom.compare_table|shop.metaobjects.compare_value#10` | prevention | Complete a dental check-up from month 6 or onwards, verified by your dentist. €40 in Care Credit is added to … |
| `admin:navigation:company:links[2].title` | use | Why use hydroxapatite |

Quotes from practitioners keep their own words. 'toothpaste' in product titles, alt texts and meta tags is the first-contact clarity use that tone-of-voice.md allows; whether every alt text needs it is Victor's call.

## Batches 04–08: pages, templates and links

Every URL in the live sitemap (19 Oct) outside batches 01–03, plus the seven Shopify policy pages, which are not in the sitemap but which checkout and order emails link. Method as in B1a: template settings come from the theme JSON; page, product, article, collection and policy text comes from the public pages, `/products/<handle>.js` and `/blogs/news.atom`. Batches 04–08 are inventoried as they are: no EN corrections, typos only noted.

`Entries`: the page's own text plus the template settings only that page renders; settings of shared templates (`page.json`, `product.json`, `collection.json`, `article.json` …) are counted once under the template in the full inventory. `Linked from`: how many other inventoried pages link to it, by region (header, footer, page body), counted over the homepage, the Duo PDP and every page below.

| URL | Batch | Template | Entries | Linked from | Notes |
|---|---|---|---:|---|---|
| `/pages/contact` | 04 | `page.contact.json` | 7 | not linked |  |
| `/pages/new-consumer-rights` | 04 | `page.consumer-rights.json` | 50 | footer 46 | current legal page (Karmicare 2.0 text, linked from the footer) |
| `/pages/privacy-policy` | 04 | `page.privacy-policy.json` | 41 | footer 46 | current legal page (Karmicare 2.0 text, linked from the footer) |
| `/pages/terms-and-conditions-1` | 04 | `page.terms-and-conditions.json` | 57 | footer 46, body 2 | current legal page (Karmicare 2.0 text, linked from the footer) |
| `/pages/consumer-rights` | 04 | `page.json` | 5 | not linked | LEGACY: pre-2.0 legal text, still published; duplicate of /pages/new-consumer-rights |
| `/pages/privacy` | 04 | `page.json` | 269 | not linked | LEGACY: pre-2.0 legal text, still published; duplicate of /pages/privacy-policy |
| `/pages/terms-and-conditions` | 04 | `page.json` | 76 | body 6 | LEGACY: pre-2.0 legal text, still published; duplicate of /pages/terms-and-conditions-1 |
| `/policies/privacy-policy` | 04 | `(Shopify policy page)` | 141 | not linked | Shopify Settings → Policies; used by checkout and order emails; not in the sitemap |
| `/policies/terms-of-service` | 04 | `(Shopify policy page)` | 167 | not linked | Shopify Settings → Policies; used by checkout and order emails; not in the sitemap |
| `/policies/refund-policy` | 04 | `(Shopify policy page)` | 126 | not linked | Shopify Settings → Policies; used by checkout and order emails; not in the sitemap |
| `/policies/shipping-policy` | 04 | `(Shopify policy page)` | 10 | body 9 | Shopify Settings → Policies; used by checkout and order emails; not in the sitemap |
| `/policies/contact-information` | 04 | `(Shopify policy page)` | 8 | not linked | Shopify Settings → Policies; used by checkout and order emails; not in the sitemap |
| `/policies/legal-notice` | 04 | `(Shopify policy page)` | 7 | not linked | Shopify Settings → Policies; used by checkout and order emails; not in the sitemap |
| `/policies/subscription-policy` | 04 | `(Shopify policy page)` | 15 | not linked | Shopify Settings → Policies; used by checkout and order emails; not in the sitemap |
| `/products/complete-hygiene-kit` | 05 | `product.json` | 4 | body 3 (/collections/all, /collections/karmicare-collection, /collections/vgbc2025) |  |
| `/products/morning-toothbrush` | 05 | `product.json` | 5 | body 5 | LEGACY: older brush, replaced by morning-toothbrush-2-0 (the compare table still references it) |
| `/products/evening-toothbrush` | 05 | `product.json` | 5 | body 5 | LEGACY: older brush, replaced by evening-toothbrush-2-0 (the compare table still references it) |
| `/products/whitening-charcoal-dental-floss` | 05 | `product.json` | 8 | body 4 |  |
| `/products/evening-toothbrush-2-0` | 05 | `product.json` | 8 | body 5 |  |
| `/products/morning-toothbrush-2-0` | 05 | `product.json` | 8 | body 5 |  |
| `/products/asleep-evening-toothpaste-2-0` | 05 | `product.json` | 10 | body 3 (/collections/all, /collections/karmicare-collection, /collections/vgbc2025) |  |
| `/products/awake-morning-toothpaste-2-0` | 05 | `product.json` | 10 | body 4 |  |
| `/pages/why-karmicare` | 06 | `page.json` | 4 | not linked |  |
| `/pages/why-use-hydroxyapatite-toothpaste` | 06 | `page.json` | 4 | not linked |  |
| `/pages/why-stop-using-fluoride-toothpaste` | 06 | `page.json` | 5 | body 1 (/search?q=awake) |  |
| `/pages/nhap-technology` | 06 | `page.json` | 5 | not linked |  |
| `/pages/articles` | 06 | `page.json` | 4 | not linked |  |
| `/collections/biorhythmic-oral-hygiene-kit` | 07 | `collection.json` | 3 | body 1 (/collections) |  |
| `/collections/vgbc2025` | 07 | `collection.json` | 3 | body 1 (/collections) |  |
| `/collections/karmicare-collection` | 07 | `collection.json` | 3 | body 1 (/collections) |  |
| `/blogs/news` | 07 | `blog.json` | 3 | body 9 |  |
| `/blogs/news/nano-hydroxyapatite` | 07 | `article.json` | 122 | not linked |  |
| `/blogs/news/morning-and-night-time-brushing-why-timing-matters` | 07 | `article.json` | 35 | body 1 (/blogs/news) |  |
| `/blogs/news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood` | 07 | `article.json` | 102 | body 1 (/blogs/news) |  |
| `/blogs/news/nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste` | 07 | `article.json` | 79 | body 1 (/blogs/news) |  |
| `/blogs/news/how-oral-health-impacts-your-overall-wellness` | 07 | `article.json` | 100 | body 1 (/search?q=awake) |  |
| `/blogs/news/top-natural-whitening-toothpaste-for-a-brighter-smile` | 07 | `article.json` | 67 | body 1 (/blogs/news) |  |
| `/blogs/news/5-reasons-you-should-avoid-fluoride-in-toothpaste` | 07 | `article.json` | 79 | body 1 (/blogs/news) |  |
| `/blogs/news/headaches-and-tooth-pain-understanding-the-connection` | 07 | `article.json` | 51 | not linked |  |
| `/blogs/news/3-reasons-why-you-should-look-for-an-sls-free-toothpaste` | 07 | `article.json` | 63 | body 1 (/blogs/news) |  |
| `/search` | 08 | `search.json` | 2 | body 1 (/search?q=awake) |  |
| `/pages/<missing>` | 08 | `404.json` | 2 | not linked |  |
| `/collections` | 08 | `list-collections.json` | 3 | not linked |  |
| `/collections/all` | 08 | `collection.json` | 2 | body 1 (/pages/<missing>) | automatic 'all products' collection |
| `/cart` | 08 | `cart.json` | 1 | not linked | redirects to checkout (kc-cart-redirect) |

Templates that do not render for a visitor today (their settings are still inventoried in batch 08):

- `/account/login, /account/register, /account` (`customers/*.json`): 302 to Shopify's hosted customer accounts: the theme templates do not render (new customer accounts).
- `/password` (`password.json`): 302 to the homepage: the store is not password-protected; the template renders only when a password is set.
- `/gift_cards/<token>` (`gift_card.liquid`): reachable only with a gift-card link; Dawn locale keys (gift_cards.*) only.

Not inventoried as store text, because Shopify or an app supplies and translates it: filter and sort labels on collections and search ("Availability", "In stock (n products)", "Price, low to high" …), article dates, and the Judge.me badge texts (listed once as `app` entries for the record). Listing pages (blog, search results, `/collections`, `/collections/all`) only repeat titles, images and excerpts that are inventoried with their own resource.

**Duplicates and legacy pages for Victor** (inventoried in full; the NL/FR files hold the legacy pages):

- `/pages/consumer-rights`, `/pages/privacy`, `/pages/terms-and-conditions`: pre-2.0 legal text, still published, not linked from the header or footer. Replaced by `/pages/new-consumer-rights`, `/pages/privacy-policy`, `/pages/terms-and-conditions-1` (the footer's links). A redirect from each old handle to its new page is a one-line admin decision.
- `/policies/*`: Shopify's policy pages hold the same 2.0 legal text again (checkout and order emails use them), so the legal text exists twice: as theme settings on the new pages and as policy bodies.
- `/products/morning-toothbrush`, `/products/evening-toothbrush`: older brushes next to the 2.0 versions; the PDP compare table still references the old ones (B1a handoff).
- `/pages/articles` (a page) next to `/blogs/news` (the blog itself); `/pages/nhap-technology` and the article `/blogs/news/nano-hydroxyapatite` share the same headline.
- `/collections/vgbc2025`: an event collection with a code-like title.

Claims in batches 05–07: 449 entries carry a claim (304 needs-review, 115 unsupported, 30 approved); see CLAIMS-REVIEW.md.

## Full inventory

Flags: **NT** never translate · **C** claim ids (CLAIMS-REVIEW.md) · **B** blocked placeholder · **R** retired (the theme no longer reads it).

### `batch-01-homepage`

| # | id | type | EN | status | flags |
|---:|---|---|---|---|---|
| 1 | `index:hero_karmicare_XKKLDK/heading_RHmd8h/heading` | template_setting | Your mouth has a rhythm Now your oral care too | approved |  |
| 2 | `index:hero_karmicare_XKKLDK/text_Y7L3hV/text` | template_setting | Karmicare is a day-and-night oral care system designed around your mouth’s 24-hour rhythm. Awake fo… | approved |  |
| 3 | `index:hero_karmicare_XKKLDK/buttons_DpYxth/button_label_1` | template_setting | BEGIN YOUR 60-DAY RITUAL | approved |  |
| 4 | `index:hero_karmicare_XKKLDK/buttons_DpYxth/button_label_2` | template_setting | WHY TWO FORMULAS? | approved |  |
| 5 | `index:hero_karmicare_XKKLDK/rhythm_toggle_ffWVXt/awake_label` | template_setting | AWAKE | approved | NT |
| 6 | `index:hero_karmicare_XKKLDK/rhythm_toggle_ffWVXt/asleep_label` | template_setting | ASLEEP | approved | NT |
| 7 | `index:hero_karmicare_XKKLDK/rhythm_toggle_ffWVXt/status_day_text` | template_setting | DAYTIME PROTECTION | approved |  |
| 8 | `index:hero_karmicare_XKKLDK/rhythm_toggle_ffWVXt/status_night_text` | template_setting | NIGHTTIME RESTORATION | approved |  |
| 9 | `index:hero_karmicare_XKKLDK/testimonial_badge_h8d3WL/rating_text` | template_setting | 4.8 (234) | needs-review | C C82 |
| 10 | `index:hero_karmicare_XKKLDK/testimonial_badge_h8d3WL/heading` | template_setting | Backed by health professionals | approved |  |
| 11 | `index:stat_strip_karmicare/tagline` | template_setting | CHOSEN BY KPNI PRACTITIONERS, FUNCTIONAL DENTISTS, HEALTH PROFESSIONALS | corrected | C C80 |
| 12 | `index:stat_strip_karmicare/stat_1/heading` | template_setting | 0% | approved |  |
| 13 | `index:stat_strip_karmicare/stat_1/text` | template_setting | fluoride, SLS | approved | C C01 |
| 14 | `index:stat_strip_karmicare/stat_2/heading` | template_setting | 1 pump | approved |  |
| 15 | `index:stat_strip_karmicare/stat_2/text` | template_setting | the full dose | approved | C C04 |
| 16 | `index:stat_strip_karmicare/stat_3/heading` | template_setting | Clinically backed | approved |  |
| 17 | `index:stat_strip_karmicare/stat_3/text` | template_setting | Formulated on +36 studies | needs-review | C C65 |
| 18 | `index:stat_strip_karmicare/stat_4/heading` | template_setting | 64 days | approved |  |
| 19 | `index:stat_strip_karmicare/stat_4/text` | template_setting | of AM/PM care per duo | approved | C C06 |
| 20 | `index:stat_strip_karmicare/stat_5/heading` | template_setting | No rinse | approved |  |
| 21 | `index:stat_strip_karmicare/stat_5/text` | template_setting | works after the brush | approved | C C10 |
| 22 | `index:chronobiology_clock_karmicare/eyebrow` | template_setting | CHRONOBIOLOGY | approved |  |
| 23 | `index:chronobiology_clock_karmicare/title` | template_setting | Your mouth runs on a 24-hour clock. | approved |  |
| 24 | `index:chronobiology_clock_karmicare/description` | template_setting | Bacteria, saliva and acids each keep their own hours. What it needs at 07:00 is not what it needs a… | approved |  |
| 25 | `index:chronobiology_clock_karmicare/morning_badge` | template_setting | ≈ 06:40 · Neisseria peaks | needs-review | C C50 |
| 26 | `index:chronobiology_clock_karmicare/morning_title` | template_setting | Your mouth wakes up | approved |  |
| 27 | `index:chronobiology_clock_karmicare/morning_text` | template_setting | Cortisol rises; coffee, breakfast and the day's first acids follow. Enamel needs its shield on firs… | needs-review | C C27,C53 |
| 28 | `index:chronobiology_clock_karmicare/night_badge` | template_setting | ≈ 22:00 · Fusobacterium peaks | needs-review | C C51 |
| 29 | `index:chronobiology_clock_karmicare/night_title` | template_setting | Your mouth switches to repair | approved |  |
| 30 | `index:chronobiology_clock_karmicare/night_text` | template_setting | Melatonin rises and saliva slows to a trickle. What's on your enamel at 22:00 is still there at 07:… | needs-review | C C52 |
| 31 | `index:chronobiology_clock_karmicare/hint_label` | template_setting | DRAG THE RING · EXPLORE 24 HOURS | approved |  |
| 32 | `index:chronobiology_clock_karmicare/footer_text` | template_setting | Formulated for both shifts: Awake by day, Asleep by night. | approved |  |
| 33 | `index:chronobiology_clock_karmicare/footer_link_text` | template_setting | Read the science | approved |  |
| 34 | `index:two_formulas_karmicare/subheading` | template_setting | BIORHYTHMIC ORAL CARE | approved |  |
| 35 | `index:two_formulas_karmicare/heading` | template_setting | Two formulas. One system. Designed around you. | approved |  |
| 36 | `index:two_formulas_karmicare/button_label` | template_setting | BEGIN YOUR 60-DAY RITUAL | approved |  |
| 37 | `index:two_formulas_karmicare/button_subtext` | template_setting | €0.49 / brushing ritual | corrected |  |
| 38 | `index:two_formulas_karmicare/left_heading` | template_setting | Activated and strengthened by day | approved |  |
| 39 | `index:two_formulas_karmicare/left_text` | template_setting | Guarana, mint and lime — a mineral shield for everything ahead. Your morning ritual, activated. | approved | C C26 |
| 40 | `index:two_formulas_karmicare/left_button_label` | template_setting | SEE WHAT'S INSIDE | approved |  |
| 41 | `index:two_formulas_karmicare/right_heading` | template_setting | Purified and restored by night | approved |  |
| 42 | `index:two_formulas_karmicare/right_text` | template_setting | Valerian, cinnamon and orange — a gentle reset for everything behind. Your evening ritual, complete. | approved |  |
| 43 | `index:two_formulas_karmicare/right_button_label` | template_setting | SEE WHAT'S INSIDE | approved |  |
| 44 | `index:two_formulas_karmicare/ingredients_list` | template_setting | FLUORIDE-FREE & SLS-FREE MICROBIOME-CONSCIOUS NANO-HYDROXYAPATITE (NHAP) SYNERGETIC EFFECT VELVETY … | needs-review | C C02,C30,C33 |
| 45 | `index:product_benefits_karmicare_bcQ6tp/subheading` | template_setting | the benefits | approved |  |
| 46 | `index:product_benefits_karmicare_bcQ6tp/heading` | template_setting | Clean is not the same as healthy. | approved |  |
| 47 | `index:product_benefits_karmicare_bcQ6tp/text` | template_setting | You brush every day. Karmicare makes those two minutes do more: strengthen enamel, settle gums, kee… | needs-review | C C20,C32,C34 |
| 48 | `index:product_benefits_karmicare_bcQ6tp/button_label` | template_setting | BEGIN YOUR 60-DAY RITUAL | approved |  |
| 49 | `index:product_benefits_karmicare_bcQ6tp/button_subtext` | template_setting | €0.49 / brushing ritual | corrected |  |
| 50 | `index:product_benefits_karmicare_bcQ6tp/bottom_note` | template_setting | *Reported outcomes vary. Mechanisms and published evidence are shown separately. | approved |  |
| 51 | `index:product_benefits_karmicare_bcQ6tp/card_qMHDBq/label` | template_setting | 01 · NANO-HYDROXYAPATITE | approved |  |
| 52 | `index:product_benefits_karmicare_bcQ6tp/card_qMHDBq/heading` | template_setting | Teeth that feel strong | approved |  |
| 53 | `index:product_benefits_karmicare_bcQ6tp/card_qMHDBq/text` | template_setting | New minerals with every brush. Cold or hot, no hesitation. | needs-review | C C21 |
| 54 | `index:product_benefits_karmicare_bcQ6tp/card_pceBAE/label` | template_setting | 02 · Essential oils | approved |  |
| 55 | `index:product_benefits_karmicare_bcQ6tp/card_pceBAE/heading` | template_setting | Fresh that lasts | approved |  |
| 56 | `index:product_benefits_karmicare_bcQ6tp/card_pceBAE/text` | template_setting | Mint and lime by day, cinnamon and orange by night. | approved |  |
| 57 | `index:product_benefits_karmicare_bcQ6tp/card_tM7UH3/label` | template_setting | 03 · Gentle foam | approved |  |
| 58 | `index:product_benefits_karmicare_bcQ6tp/card_tM7UH3/heading` | template_setting | A velvet mouthfeel | approved |  |
| 59 | `index:product_benefits_karmicare_bcQ6tp/card_tM7UH3/text` | template_setting | Soft foam and a smooth finish that stays. Two minutes you enjoy. | approved |  |
| 60 | `index:product_benefits_karmicare_bcQ6tp/card_aXhzDi/label` | template_setting | 04 · mineral whitening | approved |  |
| 61 | `index:product_benefits_karmicare_bcQ6tp/card_aXhzDi/heading` | template_setting | Naturally brighter | approved |  |
| 62 | `index:product_benefits_karmicare_bcQ6tp/card_aXhzDi/text` | template_setting | Remineralisation lifts the surface. No bleach, no strips. | approved | C C22 |
| 63 | `index:product_benefits_karmicare_bcQ6tp/card_QdCWaE/label` | template_setting | 05 · Xylitol | approved |  |
| 64 | `index:product_benefits_karmicare_bcQ6tp/card_QdCWaE/heading` | template_setting | A mouth in balance | approved |  |
| 65 | `index:product_benefits_karmicare_bcQ6tp/card_QdCWaE/text` | template_setting | Supports your mouth’s own balance. Less plaque, day and night. | approved | C C31 |
| 66 | `index:product_benefits_karmicare_bcQ6tp/card_VP8KGi/label` | template_setting | 06 · No SLS | approved |  |
| 67 | `index:product_benefits_karmicare_bcQ6tp/card_VP8KGi/heading` | template_setting | Radiant calm gums | needs-review | C C35 |
| 68 | `index:product_benefits_karmicare_bcQ6tp/card_VP8KGi/text` | template_setting | No SLS. Gums settle, turn pinker and look radiant. | needs-review | C C35 |
| 69 | `index:product_benefits_karmicare_bcQ6tp/card_KRCrBY/label` | template_setting | 07 · Guarana & valerian | approved |  |
| 70 | `index:product_benefits_karmicare_bcQ6tp/card_KRCrBY/heading` | template_setting | Focus by day, calm by night | needs-review | C C41 |
| 71 | `index:product_benefits_karmicare_bcQ6tp/card_KRCrBY/text` | template_setting | Guarana for a bright start, valerian for an evening that doesn't fight your night. | needs-review | C C40 |
| 72 | `index:product_benefits_karmicare_bcQ6tp/card_AGFiEX/label` | template_setting | 08 · Leave-on | approved |  |
| 73 | `index:product_benefits_karmicare_bcQ6tp/card_AGFiEX/heading` | template_setting | Wake up smoother | approved |  |
| 74 | `index:product_benefits_karmicare_bcQ6tp/card_AGFiEX/text` | template_setting | Spit, don’t rinse. It works all night. Feel it before breakfast. | needs-review | C C12 |
| 75 | `index:product_benefits_karmicare_bcQ6tp/card_jN7XcL/label` | template_setting | 09 · One pump | approved |  |
| 76 | `index:product_benefits_karmicare_bcQ6tp/card_jN7XcL/heading` | template_setting | One pump, one dose | approved |  |
| 77 | `index:product_benefits_karmicare_bcQ6tp/card_jN7XcL/text` | template_setting | All the minerals your mouth needs in one press. Hygienic, precise, nothing wasted. | corrected | C C05 |
| 78 | `index:trusted_professionals_HAqYth/subheading` | template_setting | PROFESSIONAL PARTNERS | approved |  |
| 79 | `index:trusted_professionals_HAqYth/heading` | template_setting | Trusted by professionals who look beyond the teeth | approved |  |
| 80 | `index:trusted_professionals_HAqYth/bottom_text` | template_setting | The best outcome is the one prevented. These practitioners recommend Karmicare between visits. Not … | needs-review | C C70 |
| 81 | `index:trusted_professionals_HAqYth/button_label` | template_setting | REQUEST A PRACTITIONER SAMPLE | approved |  |
| 82 | `index:trusted_professionals_HAqYth/card_h8d3WL/heading` | template_setting | Dr. Stephanie Spreuwers | approved | NT |
| 83 | `index:trusted_professionals_HAqYth/card_h8d3WL/text` | template_setting | Functional Dentist, kPNI Practitioner | corrected |  |
| 84 | `index:trusted_professionals_HAqYth/card_jcnr7Q/heading` | template_setting | Mariama Banjai | approved | NT |
| 85 | `index:trusted_professionals_HAqYth/card_jcnr7Q/text` | template_setting | Dental Hygienist, Oral Care Quality Manager | approved |  |
| 86 | `index:trusted_professionals_HAqYth/card_8dRing/heading` | template_setting | Leen Ponet | approved | NT |
| 87 | `index:trusted_professionals_HAqYth/card_8dRing/text` | template_setting | Pharmacist, Orthomolecular Practitioner, kPNI Coordinator | corrected |  |
| 88 | `index:trusted_professionals_HAqYth/card_8dRing/hover_text` | template_setting | “Karmicare offers fluoride-free oral care in a thoughtful way, with hydroxyapatite as a scientifica… | needs-review | C C83 |
| 89 | `index:trusted_professionals_HAqYth/card_HFdkaD/heading` | template_setting | Dr. Iveta Pleša Rutule | approved | NT |
| 90 | `index:trusted_professionals_HAqYth/card_HFdkaD/text` | template_setting | Holistic Dentist | approved |  |
| 91 | `index:trusted_professionals_HAqYth/card_Ah46TM/heading` | template_setting | Dr. Kris Sienaert | needs-review | NT |
| 92 | `index:trusted_professionals_HAqYth/card_Ah46TM/text` | template_setting | Former GP, Lifestyle Medicine | approved |  |
| 93 | `index:trusted_professionals_HAqYth/card_CtQgU9/heading` | template_setting | Sietske Hamelink | approved | NT |
| 94 | `index:trusted_professionals_HAqYth/card_CtQgU9/text` | template_setting | Nutritional Practitioner, Menstrual Cycle Expert | corrected |  |
| 95 | `index:trusted_professionals_HAqYth/card_CtQgU9/hover_text` | template_setting | “As a nutritional therapist specialized in female hormones, I’m extremely careful about what I put … | needs-review | C C84,C85 |
| 96 | `index:trusted_professionals_HAqYth/card_qAPajg/heading` | template_setting | Kim Verlot | approved | NT |
| 97 | `index:trusted_professionals_HAqYth/card_qAPajg/text` | template_setting | Breathing Coach, Heart Coherence Specialist | approved |  |
| 98 | `index:research_behind_system_EkjATL/subheading` | template_setting | CLINICALLY BACKED ORAL CARE | approved |  |
| 99 | `index:research_behind_system_EkjATL/heading` | template_setting | The research behind the system | approved |  |
| 100 | `index:research_behind_system_EkjATL/bottom_text` | template_setting | Built for people who read the label, check the research and want their daily care to hold up. Meta-… | needs-review | C C68 |
| 101 | `index:research_behind_system_EkjATL/button_label` | template_setting | Explore the full evidence base | approved |  |
| 102 | `index:research_behind_system_EkjATL/card_bDxUVT/subheading` | template_setting | NANO-HYDROXYAPATITE | approved |  |
| 103 | `index:research_behind_system_EkjATL/card_bDxUVT/heading` | template_setting | Nano-HAp sealed 98% of open dentine tubules. | needs-review | C C60 |
| 104 | `index:research_behind_system_EkjATL/card_bDxUVT/subtext` | template_setting | Human dentine discs · 7 days | approved |  |
| 105 | `index:research_behind_system_EkjATL/card_bDxUVT/result_label` | template_setting | RESULT | approved |  |
| 106 | `index:research_behind_system_EkjATL/card_bDxUVT/result_text` | template_setting | 98% occlusion vs 82% and 65% for two other desensitising technologies | needs-review | C C60 |
| 107 | `index:research_behind_system_EkjATL/card_bDxUVT/method_label` | template_setting | METHOD | approved |  |
| 108 | `index:research_behind_system_EkjATL/card_bDxUVT/method_text` | template_setting | In vitro SEM comparison of three pastes, ~1% nHAp. | approved |  |
| 109 | `index:research_behind_system_EkjATL/card_bDxUVT/link_label` | template_setting | Kulal et al. · 2016 · J Clin Diagn Res | approved | NT |
| 110 | `index:research_behind_system_EkjATL/card_bDxUVT/image_badge` | template_setting | DENTINE TUBULES · OPEN AND OCCLUDED | approved |  |
| 111 | `index:research_behind_system_EkjATL/card_yMiD9D/subheading` | template_setting | ORAL–SLEEP CONNECTION | approved |  |
| 112 | `index:research_behind_system_EkjATL/card_yMiD9D/heading` | template_setting | Poorer oral health was linked with poorer sleep. | needs-review | C C61 |
| 113 | `index:research_behind_system_EkjATL/card_yMiD9D/subtext` | template_setting | 36,559 people · 8 studies | approved |  |
| 114 | `index:research_behind_system_EkjATL/card_yMiD9D/result_label` | template_setting | RESULT | approved |  |
| 115 | `index:research_behind_system_EkjATL/card_yMiD9D/result_text` | template_setting | SMD 2.17 · p = 0.004 · 95% CI 0.68–3.66&nbsp; | needs-review | C C61 |
| 116 | `index:research_behind_system_EkjATL/card_yMiD9D/method_label` | template_setting | METHOD | approved |  |
| 117 | `index:research_behind_system_EkjATL/card_yMiD9D/method_text` | template_setting | Meta-analysis of 8 studies, 2015–2023. | approved |  |
| 118 | `index:research_behind_system_EkjATL/card_yMiD9D/link_label` | template_setting | Lei & Hu · 2025 · Biomedical Reports | approved | NT |
| 119 | `index:research_behind_system_EkjATL/card_yMiD9D/image_badge` | template_setting | SLEEP · AIRWAY AND ORAL CAVITY | approved |  |
| 120 | `index:research_behind_system_EkjATL/card_fmFMFd/subheading` | template_setting | XYLITOL | approved |  |
| 121 | `index:research_behind_system_EkjATL/card_fmFMFd/heading` | template_setting | Xylitol lowered tooth decay compared with controls. | needs-review | C C62 |
| 122 | `index:research_behind_system_EkjATL/card_fmFMFd/subtext` | template_setting | 1,478 people · 7 trials | approved |  |
| 123 | `index:research_behind_system_EkjATL/card_fmFMFd/result_label` | template_setting | Result | approved |  |
| 124 | `index:research_behind_system_EkjATL/card_fmFMFd/result_text` | template_setting | SMD −1.09 · p < 0.00001 · 95% CI −1.34 to −0.83 | needs-review | C C62 |
| 125 | `index:research_behind_system_EkjATL/card_fmFMFd/method_label` | template_setting | Method | approved |  |
| 126 | `index:research_behind_system_EkjATL/card_fmFMFd/method_text` | template_setting | Systematic review and meta-analysis of 7 clinical trials. | approved |  |
| 127 | `index:research_behind_system_EkjATL/card_fmFMFd/link_label` | template_setting | Janakiram et al. · 2017 · J Nat Sci Biol Med | approved | NT |
| 128 | `index:research_behind_system_EkjATL/card_fmFMFd/image_badge` | template_setting | DENTINE TUBULES · OPEN AND OCCLUDED | approved |  |
| 129 | `index:research_behind_system_EkjATL/card_Hi7YUD/subheading` | template_setting | NANO-HYDROXYAPATITE | approved |  |
| 130 | `index:research_behind_system_EkjATL/card_Hi7YUD/heading` | template_setting | Nano-HAp beat fluoride on tooth sensitivity. | needs-review | C C63 |
| 131 | `index:research_behind_system_EkjATL/card_Hi7YUD/subtext` | template_setting | 105 people · 4 weeks | approved |  |
| 132 | `index:research_behind_system_EkjATL/card_Hi7YUD/result_label` | template_setting | RESULT | approved |  |
| 133 | `index:research_behind_system_EkjATL/card_Hi7YUD/result_text` | template_setting | Lower cold-air and tactile sensitivity vs fluoride and placebo, p < 0.05 | needs-review | C C63 |
| 134 | `index:research_behind_system_EkjATL/card_Hi7YUD/method_label` | template_setting | METHOD | approved |  |
| 135 | `index:research_behind_system_EkjATL/card_Hi7YUD/method_text` | template_setting | Double-blind randomised controlled trial, three arms. | approved |  |
| 136 | `index:research_behind_system_EkjATL/card_Hi7YUD/link_label` | template_setting | Vano et al. · 2018 · Clin Oral Investig | approved | NT |
| 137 | `index:research_behind_system_EkjATL/card_Hi7YUD/image_badge` | template_setting | DENTINE TUBULES · OPEN AND OCCLUDED | approved |  |
| 138 | `index:research_behind_system_EkjATL/card_JeERX6/subheading` | template_setting | SLS-FREE | approved |  |
| 139 | `index:research_behind_system_EkjATL/card_JeERX6/heading` | template_setting | No SLS meant fewer and shorter canker sores. | needs-review | C C64 |
| 140 | `index:research_behind_system_EkjATL/card_JeERX6/subtext` | template_setting | 124 people · 4 crossover RCTs | approved |  |
| 141 | `index:research_behind_system_EkjATL/card_JeERX6/result_label` | template_setting | RESULT | approved |  |
| 142 | `index:research_behind_system_EkjATL/card_JeERX6/result_text` | template_setting | Fewer ulcers, shorter duration, fewer episodes, less pain | needs-review | C C64 |
| 143 | `index:research_behind_system_EkjATL/card_JeERX6/method_label` | template_setting | METHOD | approved |  |
| 144 | `index:research_behind_system_EkjATL/card_JeERX6/method_text` | template_setting | Systematic review and meta-analysis of 4 crossover RCTs. | approved |  |
| 145 | `index:research_behind_system_EkjATL/card_JeERX6/link_label` | template_setting | Alli et al. · 2019 · J Oral Pathol Med | approved | NT |
| 146 | `index:research_behind_system_EkjATL/card_JeERX6/image_badge` | template_setting | DENTINE TUBULES · OPEN AND OCCLUDED | approved |  |
| 147 | `index:km_faq_accordion_FYcArV/heading` | template_setting | Before you start | approved |  |
| 148 | `index:km_faq_accordion_FYcArV/subtext` | template_setting | Everything people usually ask before switching to a day-and-night oral care system. | approved |  |
| 149 | `index:km_faq_accordion_FYcArV/faq_item_TNnqTQ/category` | template_setting | The system | approved |  |
| 150 | `index:km_faq_accordion_FYcArV/faq_item_TNnqTQ/question` | template_setting | Why two formulas instead of one? | approved |  |
| 151 | `index:km_faq_accordion_FYcArV/faq_item_TNnqTQ/answer` | template_setting | Because your mouth doesn’t do the same job all day. Daytime is exposure — acids, sugars, coffee — s… | approved | C C25 |
| 152 | `index:km_faq_accordion_FYcArV/faq_item_kLMHax/category` | template_setting | The ritual | corrected |  |
| 153 | `index:km_faq_accordion_FYcArV/faq_item_kLMHax/question` | template_setting | How long does one duo last? | corrected |  |
| 154 | `index:km_faq_accordion_FYcArV/faq_item_kLMHax/answer` | template_setting | About 64 days — one full cycle. One pump (0.45 ml) per ritual, Awake in the morning and Asleep at n… | corrected | C C07 |
| 155 | `index:km_faq_accordion_FYcArV/faq_item_7jmEGi/category` | template_setting | Ingredients & safety | corrected |  |
| 156 | `index:km_faq_accordion_FYcArV/faq_item_7jmEGi/question` | template_setting | Can I combine Karmicare with fluoride toothpaste or rinses? | corrected |  |
| 157 | `index:km_faq_accordion_FYcArV/faq_item_7jmEGi/answer` | template_setting | Better not. Fluoride and nano-hydroxyapatite compete for the same enamel surface, so alternating di… | corrected | C C101 |
| 158 | `index:km_faq_accordion_FYcArV/faq_item_AL3DKF/category` | template_setting | Ingredients & safety | corrected |  |
| 159 | `index:km_faq_accordion_FYcArV/faq_item_AL3DKF/question` | template_setting | Is Karmicare fluoride-free? | corrected |  |
| 160 | `index:km_faq_accordion_FYcArV/faq_item_AL3DKF/answer` | template_setting | Karmicare is fluoride-free, and always will be. Fluoride’s benefits don’t outweigh its known drawba… | corrected | C C102 |
| 161 | `index:km_faq_accordion_FYcArV/faq_item_qUxYCn/category` | template_setting | Shipping & guarantee | corrected |  |
| 162 | `index:km_faq_accordion_FYcArV/faq_item_qUxYCn/question` | template_setting | What does the money-back guarantee cover? | corrected |  |
| 163 | `index:km_faq_accordion_FYcArV/faq_item_qUxYCn/answer` | template_setting | Every first order comes with a money-back guarantee: 14 days on Try Once, your first cycle on the 6… | corrected |  |
| 164 | `index:km_faq_accordion_FYcArV/faq_item_4KMG6C/category` | template_setting | Shipping & guarantee | needs-review | R |
| 165 | `index:km_faq_accordion_FYcArV/faq_item_4KMG6C/question` | template_setting | How quickly will I notice a difference? | approved | R |
| 166 | `index:km_faq_accordion_FYcArV/faq_item_4KMG6C/answer` | template_setting | Mineral remineralisation takes time — most members feel the sensitivity shift in 2–4 weeks and see … | corrected | C C24 R |
| 167 | `index:featured_product_3XpDKw/title_4znD88/custom_title` | template_setting | Your welcome kit includes | approved |  |
| 168 | `index:featured_product_3XpDKw/loop_subscriptions_7dde8c/pricing_summary_care_credit_title` | template_setting | Care Credits back | approved |  |
| 169 | `index:featured_product_3XpDKw/loop_subscriptions_7dde8c/subscription_title` | template_setting | Awake & Asleep AM/PM Oral Care System | approved | R |
| 170 | `index:featured_product_3XpDKw/loop_subscriptions_7dde8c/shipping_text` | template_setting | Shipping | approved |  |
| 171 | `index:featured_product_3XpDKw/loop_subscriptions_7dde8c/shipping_value_html` | template_setting | Varies Free | approved |  |
| 172 | `index:featured_product_3XpDKw/loop_subscriptions_7dde8c/care_credit_text_1` | template_setting | 10% / order | approved |  |
| 173 | `index:featured_product_3XpDKw/loop_subscriptions_7dde8c/care_credit_text_2` | template_setting | 10% each purchase | approved |  |
| 174 | `index:featured_product_3XpDKw/loop_subscriptions_7dde8c/per_brushing_text` | template_setting | per brushing | approved |  |
| 175 | `index:featured_product_3XpDKw/buy_buttons_UQznij/custom_button_text` | template_setting | Begin your 60-day ritual | approved |  |
| 176 | `index:featured_product_3XpDKw/icon_with_text_wUdX3G/heading_1` | template_setting | 60-day money-back guarantee | corrected |  |
| 177 | `index:featured_product_3XpDKw/icon_with_text_wUdX3G/heading_2` | template_setting | Cancel anytime | approved |  |
| 178 | `index:featured_product_3XpDKw/icon_with_text_wUdX3G/heading_3` | template_setting | Free shipping | approved |  |
| 179 | `index:care_comes_back/eyebrow` | template_setting | Return on Care | approved | NT |
| 180 | `index:care_comes_back/heading` | template_setting | The care you already do. Now designed to give back. | approved |  |
| 181 | `index:care_comes_back/intro` | template_setting | Karmicare is a care system: the ritual arrives on your rhythm, and your care builds Care Credit as … | approved |  |
| 182 | `index:care_comes_back/fine_print` | template_setting | Care Credit is Karmicare credit: spend it on more care, never on your dental bill. It rewards the v… | approved |  |
| 183 | `index:care_comes_back/terms_link_label` | template_setting | Terms, clauses 10 and 11 | approved |  |
| 184 | `index:care_comes_back/step_ritual/title` | template_setting | Your ritual | approved |  |
| 185 | `index:care_comes_back/step_ritual/text` | template_setting | Two minutes, morning and night. Your membership returns Care Credit: 10% of every 60-Day Rhythm, 20… | approved |  |
| 186 | `index:care_comes_back/step_checkup/title` | template_setting | Your check-up | approved |  |
| 187 | `index:care_comes_back/step_checkup/text` | template_setting | On the Year, a check-up after month six adds €40 in Care Credit, once per membership year. You walk… | approved |  |
| 188 | `index:care_comes_back/step_next_order/title` | template_setting | Your next order | approved |  |
| 189 | `index:care_comes_back/step_next_order/text` | template_setting | Spend Care Credit on any order. It stays valid while you are a member, and for 12 months after. | approved |  |
| 190 | `locale:blogs.article.read_more_title` | theme_locale | Read more: {{ title }} | approved |  |
| 191 | `locale:products.product.add_to_cart` | theme_locale | Add to cart | approved |  |
| 192 | `liquid:sections/hero-karmicare.liquid:149` | theme_locale | Karmicare Oral Rhythm Hero | needs-key |  |
| 193 | `liquid:sections/hero-karmicare.liquid:209` | theme_locale | Karmicare Oral Care System | needs-key |  |
| 194 | `liquid:sections/hero-karmicare.liquid:242` | theme_locale | Day and Night Oral Rhythm Switcher | needs-key |  |
| 195 | `liquid:sections/hero-karmicare.liquid:251` | theme_locale | {{ label }} mode | needs-key |  |
| 196 | `liquid:sections/stat-strip-karmicare.liquid:84` | theme_locale | Karmicare Stats and Highlights | needs-key |  |
| 197 | `liquid:sections/chronobiology-clock-karmicare.liquid:88` | theme_locale | Awake | approved | NT |
| 198 | `liquid:sections/chronobiology-clock-karmicare.liquid:101` | theme_locale | Explore your mouth's 24-hour clock | needs-key |  |
| 199 | `liquid:sections/chronobiology-clock-karmicare.liquid:153` | theme_locale | your mouth right now: | needs-key |  |
| 200 | `liquid:assets/chronobiology-clock-karmicare.js:88` | theme_locale | your mouth at this hour: | needs-key |  |
| 201 | `liquid:assets/chronobiology-clock-karmicare.js:91` | theme_locale | . Release to return to now. | needs-key |  |
| 202 | `liquid:assets/chronobiology-clock-karmicare.js:91:live` | theme_locale | . Current local time. | needs-key |  |
| 203 | `liquid:assets/chronobiology-clock-karmicare.js:11` | theme_locale | saliva is only now picking up after the night, and the enamel is least protected before your first … | needs-key | C C54 |
| 204 | `liquid:assets/chronobiology-clock-karmicare.js:12` | theme_locale | breakfast and coffee dropped the pH within minutes — saliva spends the next half hour bringing it b… | needs-key |  |
| 205 | `liquid:assets/chronobiology-clock-karmicare.js:13` | theme_locale | lunch restarts the cycle: every eating occasion opens a fresh acid window, whatever its size | needs-key |  |
| 206 | `liquid:assets/chronobiology-clock-karmicare.js:14` | theme_locale | grazing hours — the most frequent acid challenge of the day, and it is how often, not how much | needs-key |  |
| 207 | `liquid:assets/chronobiology-clock-karmicare.js:15` | theme_locale | the last big acid window of the day; after this, saliva starts winding down | needs-key |  |
| 208 | `liquid:assets/chronobiology-clock-karmicare.js:16` | theme_locale | melatonin is rising and salivary flow is dropping — what is left on the enamel now stays for hours | needs-key |  |
| 209 | `liquid:assets/chronobiology-clock-karmicare.js:17` | theme_locale | saliva is near its minimum and clearance has almost stopped: the longest unguarded stretch, and the… | needs-key |  |
| 210 | `liquid:sections/km-faq-accordion.liquid:155` | theme_locale | ALL | needs-key |  |
| 211 | `liquid:sections/featured-product.liquid:627` | theme_locale | Free | needs-key |  |
| 212 | `liquid:snippets/loop-widget-standard.liquid:101` | app | Start here | needs-key |  |
| 213 | `liquid:snippets/loop-widget-standard.liquid:103` | app | Choose how to begin | needs-key |  |
| 214 | `liquid:snippets/loop-widget-standard.liquid:109` | app | Selling Plans | needs-key |  |
| 215 | `liquid:snippets/loop-widget-standard.liquid:123` | app | One time Purchase | needs-key |  |
| 216 | `liquid:snippets/loop-widget-standard.liquid:140` | app | each | needs-key |  |
| 217 | `liquid:assets/loop-widget.js:2452` | app | / {{ days }} days | needs-key |  |
| 218 | `liquid:assets/loop-widget.js:2452:annual` | app | / year | needs-key |  |
| 219 | `liquid:assets/loop-widget.js:2463` | app | Renews | needs-key |  |
| 220 | `liquid:assets/loop-widget.js:2464` | app | {{ amount }} / brushing | needs-key |  |
| 221 | `liquid:assets/loop-widget.js:2468` | app | Renews every year | needs-key |  |
| 222 | `liquid:assets/loop-widget.js:2213` | app | {{ value }} value · free | needs-key |  |
| 223 | `liquid:snippets/loop-subscriptions.liquid:10` | app | Rendering loop-subscriptions | needs-key |  |
| 224 | `admin:shop:online_store.preferences.homepage_title` | shop | KARMICARE - Biorhythmic Oral Health | admin-held |  |
| 225 | `admin:shop:online_store.preferences.homepage_meta_description` | shop | Karmicare designs biorhythmic toothpastes formulated with clean ingredients, nootropics and plant e… | admin-held |  |
| 226 | `index:km_faq_accordion_FYcArV/faq_item_Pz4mRk/category` | template_setting | Plans & Return on Care | approved |  |
| 227 | `index:km_faq_accordion_FYcArV/faq_item_Pz4mRk/question` | template_setting | Can I pause, skip or cancel? | approved |  |
| 228 | `index:km_faq_accordion_FYcArV/faq_item_Pz4mRk/answer` | template_setting | Your membership is completely in your hands. Amend when desired. | approved |  |
| 229 | `locale:kc.clock.loading` | theme_locale | Loading current local time | approved |  |

### `batch-02-pdp`

| # | id | type | EN | status | flags |
|---:|---|---|---|---|---|
| 1 | `product.subscription-item:main/highlights_slider_9wAjAb/text_1` | template_setting | Used by 100+ kPNI practitioners & functional dentists | needs-review | C C81 |
| 2 | `product.subscription-item:main/highlights_slider_9wAjAb/text_2` | template_setting | Clinically proven ingredients · 36 peer-reviewed studies | needs-review | C C66 |
| 3 | `product.subscription-item:main/highlights_slider_9wAjAb/text_3` | template_setting | Leave-on, no rinse | approved | C C11 |
| 4 | `product.subscription-item:main/highlights_slider_9wAjAb/text_4` | template_setting | Nano-hydroxyapatite, fluoride-free | approved | C C03 |
| 5 | `product.subscription-item:main/loop_subscriptions_WEk4XJ/welcome_kit_title` | template_setting | Welcome Kit · with first order | approved |  |
| 6 | `product.subscription-item:main/loop_subscriptions_WEk4XJ/try_once_text` | template_setting | Try once | approved |  |
| 7 | `product.subscription-item:main/loop_subscriptions_WEk4XJ/try_once_shipping` | template_setting | + shipping | approved |  |
| 8 | `product.subscription-item:main/loop_subscriptions_WEk4XJ/try_once_note` | template_setting | €0 Care Credit · €0 Dental Check-up Reward | approved |  |
| 9 | `product.subscription-item:main/loop_subscriptions_WEk4XJ/pricing_summary_total_title` | template_setting | Total today | approved |  |
| 10 | `product.subscription-item:main/loop_subscriptions_WEk4XJ/pricing_summary_care_credit_title` | template_setting | Care Credit back in your account | approved |  |
| 11 | `product.subscription-item:main/loop_subscriptions_WEk4XJ/pricing_summary_care_credit_tooltip` | template_setting | Care Credit is Return on Care in euros — spendable on member products and accessories. It lands in … | approved |  |
| 12 | `product.subscription-item:main/loop_subscriptions_WEk4XJ/pricing_summary_checkup_title` | template_setting | Dental Check-up Reward | approved |  |
| 13 | `product.subscription-item:main/loop_subscriptions_WEk4XJ/pricing_summary_checkup_tooltip` | template_setting | Complete a dental check-up from month 6 or onwards, verified by your dentist. €40 in Care Credit is… | needs-review |  |
| 14 | `product.subscription-item:main/loop_subscriptions_WEk4XJ/testimonial_button_text` | template_setting | Brushing & Beyond | approved |  |
| 15 | `product.subscription-item:main/loop_subscriptions_WEk4XJ/plans_eyebrow` | template_setting | Start here | approved |  |
| 16 | `product.subscription-item:main/loop_subscriptions_WEk4XJ/plans_heading` | template_setting | Choose how to begin | approved |  |
| 17 | `product.subscription-item:main/loop_subscriptions_WEk4XJ/pricing_summary_welcome_kit_title` | template_setting | Welcome Kit on first order (value [value]) | approved |  |
| 18 | `product.subscription-item:main/loop_subscriptions_WEk4XJ/pricing_summary_welcome_kit_value` | template_setting | FREE | approved |  |
| 19 | `product.subscription-item:main/buy_buttons/custom_button_text` | template_setting | Begin Now | approved |  |
| 20 | `product.subscription-item:main/buy_buttons/custom_button_text_by_plan` | template_setting | 712106115453: Begin your 60-Day Rhythm 712155431293: Begin your Karmicare Year | corrected |  |
| 21 | `product.subscription-item:main/icon_with_text_xhaDGB/heading_1` | template_setting | 60-day money-back guarantee | approved |  |
| 22 | `product.subscription-item:main/icon_with_text_xhaDGB/heading_2` | template_setting | Gift, pause or cancel | approved |  |
| 23 | `product.subscription-item:main/icon_with_text_xhaDGB/heading_3` | template_setting | Free shipping | approved |  |
| 24 | `product.subscription-item:main/treatment_journey_block/read_more_text` | template_setting | Read more | approved |  |
| 25 | `product.subscription-item:main/treatment_journey_block/read_less_text` | template_setting | Read less | approved |  |
| 26 | `product.subscription-item:main/treatment_journey_block/disclaimer_text` | template_setting | * What members report with continued use — individual experiences vary. | approved |  |
| 27 | `product.subscription-item:main/info_card_FnBcaN/header_text` | template_setting | More than two formulas | approved |  |
| 28 | `product.subscription-item:main/info_card_FnBcaN/body_text` | template_setting | Karmicare is a care system, not a shelf item: the ritual arrives on your rhythm, and your care buil… | needs-review |  |
| 29 | `product.subscription-item:main/info_card_FnBcaN/footer_text` | template_setting | Care Credit is Karmicare credit: spend it on more care, never on your dental bill. It rewards the v… | approved |  |
| 30 | `product.subscription-item:main/professional_testimonials_block/heading` | template_setting | Trusted by professionals | approved |  |
| 31 | `product.subscription-item:main/sticky_cart_block/button_text` | template_setting | Begin Now | approved |  |
| 32 | `product.subscription-item:chronobiology_clock_karmicare/eyebrow` | template_setting | CHRONOBIOLOGY | approved |  |
| 33 | `product.subscription-item:chronobiology_clock_karmicare/title` | template_setting | Your mouth runs on a 24-hour clock. | approved |  |
| 34 | `product.subscription-item:chronobiology_clock_karmicare/description` | template_setting | Bacteria, saliva and acids each keep their own hours. What it needs at 07:00 is not what it needs a… | approved |  |
| 35 | `product.subscription-item:chronobiology_clock_karmicare/morning_badge` | template_setting | ≈ 06:40 · Neisseria peaks | needs-review | C C50 |
| 36 | `product.subscription-item:chronobiology_clock_karmicare/morning_title` | template_setting | Your mouth wakes up | approved |  |
| 37 | `product.subscription-item:chronobiology_clock_karmicare/morning_text` | template_setting | Cortisol rises; coffee, breakfast and the day's first acids follow. Enamel needs its shield on firs… | needs-review | C C27,C53 |
| 38 | `product.subscription-item:chronobiology_clock_karmicare/night_badge` | template_setting | ≈ 22:00 · Fusobacterium peaks | needs-review | C C51 |
| 39 | `product.subscription-item:chronobiology_clock_karmicare/night_title` | template_setting | Your mouth switches to repair | approved |  |
| 40 | `product.subscription-item:chronobiology_clock_karmicare/night_text` | template_setting | Melatonin rises and saliva slows to a trickle. What's on your enamel at 22:00 is still there at 07:… | needs-review | C C52 |
| 41 | `product.subscription-item:chronobiology_clock_karmicare/hint_label` | template_setting | DRAG THE RING · EXPLORE 24 HOURS | approved |  |
| 42 | `product.subscription-item:chronobiology_clock_karmicare/footer_text` | template_setting | Formulated for both shifts: Awake by day, Asleep by night. | approved |  |
| 43 | `product.subscription-item:chronobiology_clock_karmicare/footer_link_text` | template_setting | Read the science | approved |  |
| 44 | `product.subscription-item:trusted_professionals_HAqYth/subheading` | template_setting | PROFESSIONAL PARTNERS | approved |  |
| 45 | `product.subscription-item:trusted_professionals_HAqYth/heading` | template_setting | Trusted by professionals who look beyond the teeth | approved |  |
| 46 | `product.subscription-item:trusted_professionals_HAqYth/bottom_text` | template_setting | The best outcome is the one prevented. These practitioners recommend Karmicare between visits. Not … | needs-review | C C70 |
| 47 | `product.subscription-item:trusted_professionals_HAqYth/button_label` | template_setting | REQUEST A PRACTITIONER SAMPLE | approved |  |
| 48 | `product.subscription-item:trusted_professionals_HAqYth/card_h8d3WL/heading` | template_setting | Dr. Stephanie Spreuwers | approved | NT |
| 49 | `product.subscription-item:trusted_professionals_HAqYth/card_h8d3WL/text` | template_setting | Functional Dentist, kPNI Practitioner | corrected |  |
| 50 | `product.subscription-item:trusted_professionals_HAqYth/card_jcnr7Q/heading` | template_setting | Mariama Banjai | approved | NT |
| 51 | `product.subscription-item:trusted_professionals_HAqYth/card_jcnr7Q/text` | template_setting | Dental Hygienist, Oral Care Quality Manager | approved |  |
| 52 | `product.subscription-item:trusted_professionals_HAqYth/card_8dRing/heading` | template_setting | Leen Ponet | approved | NT |
| 53 | `product.subscription-item:trusted_professionals_HAqYth/card_8dRing/text` | template_setting | Pharmacist, Orthomolecular Practitioner, kPNI Coordinator | corrected |  |
| 54 | `product.subscription-item:trusted_professionals_HAqYth/card_8dRing/hover_text` | template_setting | “Karmicare offers fluoride-free oral care in a thoughtful way, with hydroxyapatite as a scientifica… | needs-review | C C83 |
| 55 | `product.subscription-item:trusted_professionals_HAqYth/card_HFdkaD/heading` | template_setting | Dr. Iveta Pleša Rutule | approved | NT |
| 56 | `product.subscription-item:trusted_professionals_HAqYth/card_HFdkaD/text` | template_setting | Holistic Dentist | approved |  |
| 57 | `product.subscription-item:trusted_professionals_HAqYth/card_Ah46TM/heading` | template_setting | Dr. Kris Sienaert | needs-review | NT |
| 58 | `product.subscription-item:trusted_professionals_HAqYth/card_Ah46TM/text` | template_setting | Former GP, Lifestyle Medicine | approved |  |
| 59 | `product.subscription-item:trusted_professionals_HAqYth/card_CtQgU9/heading` | template_setting | Sietske Hamelink | approved | NT |
| 60 | `product.subscription-item:trusted_professionals_HAqYth/card_CtQgU9/text` | template_setting | Nutritional Practitioner, Menstrual Cycle Expert | corrected |  |
| 61 | `product.subscription-item:trusted_professionals_HAqYth/card_CtQgU9/hover_text` | template_setting | “As a nutritional therapist specialized in female hormones, I’m extremely careful about what I put … | needs-review | C C84,C85 |
| 62 | `product.subscription-item:trusted_professionals_HAqYth/card_qAPajg/heading` | template_setting | Kim Verlot | approved | NT |
| 63 | `product.subscription-item:trusted_professionals_HAqYth/card_qAPajg/text` | template_setting | Breathing Coach, Heart Coherence Specialist | approved |  |
| 64 | `product.subscription-item:how_it_works_steps_aAgVmF/subtitle` | template_setting | The Ritual | approved |  |
| 65 | `product.subscription-item:how_it_works_steps_aAgVmF/title` | template_setting | How Karmicare works. | approved |  |
| 66 | `product.subscription-item:how_it_works_steps_aAgVmF/description` | template_setting | Become a pro at brushing. Feel your teeth by sliding your tongue. | approved |  |
| 67 | `product.subscription-item:how_it_works_steps_aAgVmF/hint_text` | template_setting | Preview · sound off | approved |  |
| 68 | `product.subscription-item:how_it_works_steps_aAgVmF/bottom_text` | template_setting | Not to be combined with fluoride oral care. One duo lasts 64 days at two brushings a day. | approved | C C07 |
| 69 | `product.subscription-item:how_it_works_steps_aAgVmF/step_U7HiXT/number` | template_setting | 02 | approved | R |
| 70 | `product.subscription-item:how_it_works_steps_aAgVmF/step_U7HiXT/title` | template_setting | Pump and brush | approved |  |
| 71 | `product.subscription-item:how_it_works_steps_aAgVmF/step_U7HiXT/description` | template_setting | Apply one pump and brush gently for two minutes. | approved |  |
| 72 | `product.subscription-item:how_it_works_steps_aAgVmF/step_EBicgt/number` | template_setting | 03 | approved | R |
| 73 | `product.subscription-item:how_it_works_steps_aAgVmF/step_EBicgt/title` | template_setting | Spit, no rinse | approved |  |
| 74 | `product.subscription-item:how_it_works_steps_aAgVmF/step_EBicgt/description` | template_setting | Spit out the excess. Do not rinse afterwards. | approved |  |
| 75 | `product.subscription-item:research_behind_system_EkjATL/subheading` | template_setting | CLINICALLY BACKED ORAL CARE | approved |  |
| 76 | `product.subscription-item:research_behind_system_EkjATL/heading` | template_setting | The research behind the system | approved |  |
| 77 | `product.subscription-item:research_behind_system_EkjATL/bottom_text` | template_setting | Built for people who read the label, check the research and want their daily care to hold up. Meta-… | needs-review | C C68 |
| 78 | `product.subscription-item:research_behind_system_EkjATL/button_label` | template_setting | Explore the full evidence base | approved |  |
| 79 | `product.subscription-item:research_behind_system_EkjATL/card_bDxUVT/subheading` | template_setting | NANO-HYDROXYAPATITE | approved |  |
| 80 | `product.subscription-item:research_behind_system_EkjATL/card_bDxUVT/heading` | template_setting | Nano-HAp sealed 98% of open dentine tubules. | needs-review | C C60 |
| 81 | `product.subscription-item:research_behind_system_EkjATL/card_bDxUVT/subtext` | template_setting | Human dentine discs · 7 days | approved |  |
| 82 | `product.subscription-item:research_behind_system_EkjATL/card_bDxUVT/result_label` | template_setting | RESULT | approved |  |
| 83 | `product.subscription-item:research_behind_system_EkjATL/card_bDxUVT/result_text` | template_setting | 98% occlusion vs 82% and 65% for two other desensitising technologies | needs-review | C C60 |
| 84 | `product.subscription-item:research_behind_system_EkjATL/card_bDxUVT/method_label` | template_setting | METHOD | approved |  |
| 85 | `product.subscription-item:research_behind_system_EkjATL/card_bDxUVT/method_text` | template_setting | In vitro SEM comparison of three pastes, ~1% nHAp. | approved |  |
| 86 | `product.subscription-item:research_behind_system_EkjATL/card_bDxUVT/link_label` | template_setting | Kulal et al. · 2016 · J Clin Diagn Res | approved | NT |
| 87 | `product.subscription-item:research_behind_system_EkjATL/card_bDxUVT/image_badge` | template_setting | DENTINE TUBULES · OPEN AND OCCLUDED | approved |  |
| 88 | `product.subscription-item:research_behind_system_EkjATL/card_yMiD9D/subheading` | template_setting | ORAL–SLEEP CONNECTION | approved |  |
| 89 | `product.subscription-item:research_behind_system_EkjATL/card_yMiD9D/heading` | template_setting | Poorer oral health was linked with poorer sleep. | needs-review | C C61 |
| 90 | `product.subscription-item:research_behind_system_EkjATL/card_yMiD9D/subtext` | template_setting | 36,559 people · 8 studies | approved |  |
| 91 | `product.subscription-item:research_behind_system_EkjATL/card_yMiD9D/result_label` | template_setting | RESULT | approved |  |
| 92 | `product.subscription-item:research_behind_system_EkjATL/card_yMiD9D/result_text` | template_setting | SMD 2.17 · p = 0.004 · 95% CI 0.68–3.66&nbsp; | needs-review | C C61 |
| 93 | `product.subscription-item:research_behind_system_EkjATL/card_yMiD9D/method_label` | template_setting | METHOD | approved |  |
| 94 | `product.subscription-item:research_behind_system_EkjATL/card_yMiD9D/method_text` | template_setting | Meta-analysis of 8 studies, 2015–2023. | approved |  |
| 95 | `product.subscription-item:research_behind_system_EkjATL/card_yMiD9D/link_label` | template_setting | Lei & Hu · 2025 · Biomedical Reports | approved | NT |
| 96 | `product.subscription-item:research_behind_system_EkjATL/card_yMiD9D/image_badge` | template_setting | SLEEP · AIRWAY AND ORAL CAVITY | approved |  |
| 97 | `product.subscription-item:research_behind_system_EkjATL/card_fmFMFd/subheading` | template_setting | XYLITOL | approved |  |
| 98 | `product.subscription-item:research_behind_system_EkjATL/card_fmFMFd/heading` | template_setting | Xylitol lowered tooth decay compared with controls. | needs-review | C C62 |
| 99 | `product.subscription-item:research_behind_system_EkjATL/card_fmFMFd/subtext` | template_setting | 1,478 people · 7 trials | approved |  |
| 100 | `product.subscription-item:research_behind_system_EkjATL/card_fmFMFd/result_label` | template_setting | Result | approved |  |
| 101 | `product.subscription-item:research_behind_system_EkjATL/card_fmFMFd/result_text` | template_setting | SMD −1.09 · p < 0.00001 · 95% CI −1.34 to −0.83 | needs-review | C C62 |
| 102 | `product.subscription-item:research_behind_system_EkjATL/card_fmFMFd/method_label` | template_setting | Method | approved |  |
| 103 | `product.subscription-item:research_behind_system_EkjATL/card_fmFMFd/method_text` | template_setting | Systematic review and meta-analysis of 7 clinical trials. | approved |  |
| 104 | `product.subscription-item:research_behind_system_EkjATL/card_fmFMFd/link_label` | template_setting | Janakiram et al. · 2017 · J Nat Sci Biol Med | approved | NT |
| 105 | `product.subscription-item:research_behind_system_EkjATL/card_fmFMFd/image_badge` | template_setting | DENTINE TUBULES · OPEN AND OCCLUDED | approved |  |
| 106 | `product.subscription-item:research_behind_system_EkjATL/card_Hi7YUD/subheading` | template_setting | NANO-HYDROXYAPATITE | approved |  |
| 107 | `product.subscription-item:research_behind_system_EkjATL/card_Hi7YUD/heading` | template_setting | Nano-HAp beat fluoride on tooth sensitivity. | needs-review | C C63 |
| 108 | `product.subscription-item:research_behind_system_EkjATL/card_Hi7YUD/subtext` | template_setting | 105 people · 4 weeks | approved |  |
| 109 | `product.subscription-item:research_behind_system_EkjATL/card_Hi7YUD/result_label` | template_setting | RESULT | approved |  |
| 110 | `product.subscription-item:research_behind_system_EkjATL/card_Hi7YUD/result_text` | template_setting | Lower cold-air and tactile sensitivity vs fluoride and placebo, p < 0.05 | needs-review | C C63 |
| 111 | `product.subscription-item:research_behind_system_EkjATL/card_Hi7YUD/method_label` | template_setting | METHOD | approved |  |
| 112 | `product.subscription-item:research_behind_system_EkjATL/card_Hi7YUD/method_text` | template_setting | Double-blind randomised controlled trial, three arms. | approved |  |
| 113 | `product.subscription-item:research_behind_system_EkjATL/card_Hi7YUD/link_label` | template_setting | Vano et al. · 2018 · Clin Oral Investig | approved | NT |
| 114 | `product.subscription-item:research_behind_system_EkjATL/card_Hi7YUD/image_badge` | template_setting | DENTINE TUBULES · OPEN AND OCCLUDED | approved |  |
| 115 | `product.subscription-item:research_behind_system_EkjATL/card_JeERX6/subheading` | template_setting | SLS-FREE | approved |  |
| 116 | `product.subscription-item:research_behind_system_EkjATL/card_JeERX6/heading` | template_setting | No SLS meant fewer and shorter canker sores. | needs-review | C C64 |
| 117 | `product.subscription-item:research_behind_system_EkjATL/card_JeERX6/subtext` | template_setting | 124 people · 4 crossover RCTs | approved |  |
| 118 | `product.subscription-item:research_behind_system_EkjATL/card_JeERX6/result_label` | template_setting | RESULT | approved |  |
| 119 | `product.subscription-item:research_behind_system_EkjATL/card_JeERX6/result_text` | template_setting | Fewer ulcers, shorter duration, fewer episodes, less pain | needs-review | C C64 |
| 120 | `product.subscription-item:research_behind_system_EkjATL/card_JeERX6/method_label` | template_setting | METHOD | approved |  |
| 121 | `product.subscription-item:research_behind_system_EkjATL/card_JeERX6/method_text` | template_setting | Systematic review and meta-analysis of 4 crossover RCTs. | approved |  |
| 122 | `product.subscription-item:research_behind_system_EkjATL/card_JeERX6/link_label` | template_setting | Alli et al. · 2019 · J Oral Pathol Med | approved | NT |
| 123 | `product.subscription-item:research_behind_system_EkjATL/card_JeERX6/image_badge` | template_setting | DENTINE TUBULES - OPEN AND OCCLUDED | approved |  |
| 124 | `product.subscription-item:featured_product_Eb93Xa/title_GDDYEK/custom_title` | template_setting | Your welcome kit includes | approved |  |
| 125 | `product.subscription-item:featured_product_Eb93Xa/loop_subscriptions_gPKypi/pricing_summary_care_credit_title` | template_setting | Care Credits back | approved |  |
| 126 | `product.subscription-item:featured_product_Eb93Xa/loop_subscriptions_gPKypi/subscription_title` | template_setting | Awake & Asleep AM/PM Oral Care System | approved | R |
| 127 | `product.subscription-item:featured_product_Eb93Xa/loop_subscriptions_gPKypi/shipping_text` | template_setting | Shipping | approved |  |
| 128 | `product.subscription-item:featured_product_Eb93Xa/loop_subscriptions_gPKypi/shipping_value_html` | template_setting | Varies Free | approved |  |
| 129 | `product.subscription-item:featured_product_Eb93Xa/loop_subscriptions_gPKypi/care_credit_text_1` | template_setting | 10% / order | approved |  |
| 130 | `product.subscription-item:featured_product_Eb93Xa/loop_subscriptions_gPKypi/care_credit_text_2` | template_setting | 10% each purchase | approved |  |
| 131 | `product.subscription-item:featured_product_Eb93Xa/loop_subscriptions_gPKypi/per_brushing_text` | template_setting | per brushing | approved |  |
| 132 | `product.subscription-item:featured_product_Eb93Xa/buy_buttons_Ffxhap/custom_button_text` | template_setting | Begin your 60-Day rhythm | approved |  |
| 133 | `product.subscription-item:featured_product_Eb93Xa/icon_with_text_endcta/heading_1` | template_setting | 60-day money-back guarantee | approved |  |
| 134 | `product.subscription-item:featured_product_Eb93Xa/icon_with_text_endcta/heading_2` | template_setting | Free shipping | approved |  |
| 135 | `product.subscription-item:featured_product_Eb93Xa/icon_with_text_endcta/heading_3` | template_setting | Gift, pause or cancel | approved |  |
| 136 | `product.subscription-item:care_comes_back/eyebrow` | template_setting | Return on Care | approved | NT |
| 137 | `product.subscription-item:care_comes_back/heading` | template_setting | Care that comes back. | approved |  |
| 138 | `product.subscription-item:care_comes_back/intro` | template_setting | Karmicare is a care system: the ritual arrives on your rhythm, and your care builds Care Credit as … | approved |  |
| 139 | `product.subscription-item:care_comes_back/receipt_title` | template_setting | Your first Year in Care Credit | approved |  |
| 140 | `product.subscription-item:care_comes_back/receipt_column_label` | template_setting | Received | approved |  |
| 141 | `product.subscription-item:care_comes_back/total_label` | template_setting | Up to | approved |  |
| 142 | `product.subscription-item:care_comes_back/total` | template_setting | €110.80 | approved |  |
| 143 | `product.subscription-item:care_comes_back/fine_print` | template_setting | Care Credit is Karmicare credit: spend it on more care, never on your dental bill. It rewards the v… | approved |  |
| 144 | `product.subscription-item:care_comes_back/terms_link_label` | template_setting | Terms, clauses 10 and 11 | approved |  |
| 145 | `product.subscription-item:care_comes_back/step_ritual/title` | template_setting | Your ritual | approved |  |
| 146 | `product.subscription-item:care_comes_back/step_ritual/text` | template_setting | Two minutes, morning and night. Your membership returns Care Credit: 10% of every 60-Day Rhythm, 20… | approved |  |
| 147 | `product.subscription-item:care_comes_back/step_checkup/title` | template_setting | Your check-up | approved |  |
| 148 | `product.subscription-item:care_comes_back/step_checkup/text` | template_setting | On the Year, a check-up after month six adds €40 in Care Credit, once per membership year. You walk… | approved |  |
| 149 | `product.subscription-item:care_comes_back/step_next_order/title` | template_setting | Your next order | approved |  |
| 150 | `product.subscription-item:care_comes_back/step_next_order/text` | template_setting | Spend Care Credit on any order. It stays valid while you are a member, and for 12 months after. | approved |  |
| 151 | `product.subscription-item:care_comes_back/line_year/label` | template_setting | Return on Care | approved | NT |
| 152 | `product.subscription-item:care_comes_back/line_year/note` | template_setting | 20% back on the Year | approved |  |
| 153 | `product.subscription-item:care_comes_back/line_year/amount` | template_setting | €70.80 | approved |  |
| 154 | `product.subscription-item:care_comes_back/line_checkup/label` | template_setting | Dental Check-up Reward | approved |  |
| 155 | `product.subscription-item:care_comes_back/line_checkup/note` | template_setting | after month six | approved |  |
| 156 | `product.subscription-item:care_comes_back/line_checkup/amount` | template_setting | €40.00 | approved |  |
| 157 | `locale:products.product.media.gallery_viewer` | theme_locale | Gallery Viewer | approved |  |
| 158 | `locale:accessibility.skip_to_product_info` | theme_locale | Skip to product information | approved |  |
| 159 | `locale:products.product.media.open_media` | theme_locale | Open media {{ index }} in modal | approved |  |
| 160 | `locale:general.slider.previous_slide` | theme_locale | Slide left | approved |  |
| 161 | `locale:general.slider.next_slide` | theme_locale | Slide right | approved |  |
| 162 | `locale:products.product.media.load_video` | theme_locale | Play video {{ index }} in gallery view | approved |  |
| 163 | `locale:products.product.media.load_image` | theme_locale | Load image {{ index }} in gallery view | approved |  |
| 164 | `locale:products.product.price.regular_price` | theme_locale | Regular price | approved |  |
| 165 | `locale:products.product.price.sale_price` | theme_locale | Sale price | approved |  |
| 166 | `locale:products.product.on_sale` | theme_locale | Sale | approved |  |
| 167 | `locale:products.product.sold_out` | theme_locale | Sold out | approved |  |
| 168 | `locale:products.product.taxes_included` | theme_locale | Taxes included. | approved |  |
| 169 | `locale:products.product.shipping_policy_html` | theme_locale | Shipping calculated at checkout. | approved |  |
| 170 | `locale:products.product.view_full_details` | theme_locale | View full details | approved |  |
| 171 | `locale:products.modal.label` | theme_locale | Media gallery | approved |  |
| 172 | `liquid:sections/main-product.liquid:147` | theme_locale | Or | needs-key |  |
| 173 | `liquid:snippets/professional-testimonials.liquid:61` | theme_locale | PROFESSIONAL PARTNERS | needs-key |  |
| 174 | `liquid:snippets/product-category-strip.liquid:36` | theme_locale | Karmicare, Biorhythmic Oral Care | needs-key |  |
| 175 | `liquid:snippets/product-highlights.liquid:160` | theme_locale | Product highlights | needs-key |  |
| 176 | `liquid:sections/main-product.liquid:931` | theme_locale | 60-Day Rhythm · Awake + Asleep | needs-key |  |
| 177 | `liquid:sections/main-product.liquid:937` | theme_locale | The Karmicare Year · 6 Duos | needs-key |  |
| 178 | `liquid:sections/main-product.liquid:943` | theme_locale | Try Once · 1 Duo | needs-key |  |
| 179 | `liquid:sections/main-product.liquid:954` | theme_locale | [price] every 60 days | needs-key |  |
| 180 | `liquid:sections/main-product.liquid:960` | theme_locale | [price] per year | needs-key |  |
| 181 | `liquid:sections/main-product.liquid:966` | theme_locale | [price] one time | needs-key |  |
| 182 | `liquid:sections/main-product.liquid:977` | theme_locale | + [credit] Care Credit back | needs-key |  |
| 183 | `liquid:sections/main-product.liquid:983` | theme_locale | + [credit] Care Credit + €40 Check-up Reward | needs-key |  |
| 184 | `liquid:sections/main-product.liquid:989` | theme_locale | Care Credit is Karmicare credit: spend it on more care, never on your dental bill. | needs-key |  |
| 185 | `liquid:sections/main-product.liquid:995` | theme_locale | Complete a dental check-up from month 6 or onwards, verified by your dentist. €40 in Care Credit is… | needs-key |  |
| 186 | `liquid:sections/main-product.liquid:1006` | theme_locale | Delivery & what's included | needs-key |  |
| 187 | `liquid:sections/main-product.liquid:1012` | theme_locale | Change | needs-key |  |
| 188 | `liquid:sections/main-product.liquid:1018` | theme_locale | Begin your 60-Day Rhythm | needs-key |  |
| 189 | `liquid:sections/main-product.liquid:1024` | theme_locale | Begin your Karmicare Year | needs-key |  |
| 190 | `liquid:sections/main-product.liquid:1030` | theme_locale | Try once | needs-key |  |
| 191 | `liquid:sections/main-product.liquid:1036` | theme_locale | Free Fast Delivery: 24 hours in Benelux. 2–3 days in rest of Europe | needs-key |  |
| 192 | `liquid:sections/main-product.liquid:1042` | theme_locale | Shipping calculated at checkout | needs-key |  |
| 193 | `liquid:sections/main-product.liquid:1049` | theme_locale | Welcome Kit: two toothbrushes + floss | needs-key |  |
| 194 | `liquid:sections/main-product.liquid:1055` | theme_locale | 60-day money-back guarantee | needs-key |  |
| 195 | `liquid:sections/main-product.liquid:1061` | theme_locale | 14-day money-back guarantee | needs-key |  |
| 196 | `liquid:sections/main-product.liquid:1067` | theme_locale | Pause or stop anytime | needs-key |  |
| 197 | `liquid:sections/main-product.liquid:1073` | theme_locale | Renews yearly · stop anytime before renewal | needs-key |  |
| 198 | `liquid:sections/main-product.liquid:1080` | theme_locale | [per_brushing] per brushing | needs-key |  |
| 199 | `liquid:sections/main-product.liquid:1087` | theme_locale | Not ready for a membership? Try once for [price] | needs-key |  |
| 200 | `liquid:sections/main-product.liquid:1098` | theme_locale | Awake & Asleep AM/PM Oral Care System | needs-key | R |
| 201 | `liquid:sections/main-product.liquid:1104` | theme_locale | Free | needs-key | R |
| 202 | `liquid:sections/product-compare-plans.liquid:39` | theme_locale | Compare plans | needs-key |  |
| 203 | `liquid:sections/product-compare-plans.liquid:55` | theme_locale | Compare | needs-key |  |
| 204 | `liquid:sections/product-compare-plans.liquid:98` | theme_locale | · {{ total_value }} Value | needs-key |  |
| 205 | `liquid:sections/product-compare-plans.liquid:100` | theme_locale | Free | needs-key |  |
| 206 | `liquid:sections/product-compare-plans.liquid:234` | theme_locale | Not included | needs-key |  |
| 207 | `liquid:sections/product-compare-plans.liquid:241` | theme_locale | Included | needs-key |  |
| 208 | `liquid:snippets/kc-plan-loyalty.liquid:41` | theme_locale | 60-Day Supply | approved | NT |
| 209 | `liquid:snippets/kc-plan-loyalty.liquid:43` | theme_locale | Year Supply | approved | NT |
| 210 | `admin:karmicare-biorhythmic-oral-care-system:selling_plan_group:Subscribe and Save` | app | Subscribe and Save | admin-held |  |
| 211 | `admin:karmicare-biorhythmic-oral-care-system:selling_plan.712387363197.name` | app | Pay every 12 months, Deliver every 6 months_ | admin-held |  |
| 212 | `admin:karmicare-biorhythmic-oral-care-system:selling_plan.712387330429.name` | app | 6 duos a year (3 now, 3 in month 6) | admin-held |  |
| 213 | `admin:karmicare-biorhythmic-oral-care-system:selling_plan.712387297661.name` | app | Deliver every 60 days | admin-held |  |
| 214 | `admin:karmicare-biorhythmic-oral-care-system:selling_plan_group:60-Day Supply` | app | 60-Day Supply | admin-held | NT |
| 215 | `admin:karmicare-biorhythmic-oral-care-system:selling_plan.712192164221.name` | app | ships every 60 days | admin-held |  |
| 216 | `admin:karmicare-biorhythmic-oral-care-system:selling_plan_group:60-Day Rhythm` | app | 60-Day Rhythm | admin-held |  |
| 217 | `admin:karmicare-biorhythmic-oral-care-system:selling_plan.712106115453.name` | app | ships every 60 days | admin-held |  |
| 218 | `admin:karmicare-biorhythmic-oral-care-system:selling_plan.712106115453.description` | app | 10% Care Credit back in your account i Return on Care is our give-back: 10% of every 60-day supply … | admin-held |  |
| 219 | `admin:karmicare-biorhythmic-oral-care-system:selling_plan_group:The Karmicare Year` | app | The Karmicare Year | admin-held |  |
| 220 | `admin:karmicare-biorhythmic-oral-care-system:selling_plan.712155431293.name` | app | 6 duos a year (3 now, 3 in month 6) | admin-held |  |
| 221 | `admin:karmicare-biorhythmic-oral-care-system:selling_plan.712155431293.description` | app | 20% Care Credit back in your account i The year plan earns 20% Return on Care — 2× the bi-monthly r… | admin-held |  |
| 222 | `admin:karmicare-biorhythmic-oral-care-system:selling_plan_group:Yearly Plan` | app | Yearly Plan | admin-held |  |
| 223 | `admin:karmicare-biorhythmic-oral-care-system:selling_plan.712370356605.name` | app | 6 duos a year (3 now, 3 in month 6) | admin-held |  |
| 224 | `admin:karmicare-biorhythmic-oral-care-system:seo.title` | product | Fluoride-Free Morning & Night Toothpaste System \| KARMICARE | admin-held |  |
| 225 | `admin:karmicare-biorhythmic-oral-care-system:seo.description` | product | Awake for the morning, Asleep for the night: two nano-hydroxyapatite toothpastes you don't rinse of… | admin-held |  |
| 226 | `admin:karmicare-biorhythmic-oral-care-system:title` | product | Awake & Asleep Morning & Night Toothpaste System | admin-held |  |
| 227 | `admin:karmicare-biorhythmic-oral-care-system:body_html` | product | Your mouth doesn’t stay the same from morning to night. Two toothpastes, one system. Formulated aro… | admin-held | C C14,C36 |
| 228 | `admin:karmicare-biorhythmic-oral-care-system:media.69271648010621.alt` | product | Karmicare Biorhythmic Oral Care Kit: fluoride-free, SLS-free Awake morning and Asleep evening tooth… | admin-held | C C100 |
| 229 | `admin:karmicare-biorhythmic-oral-care-system:media.69248905085309.alt` | product | Karmicare Biorhythmic Oral Care Duo Set: Awake morning and Asleep evening toothpaste, fluoride-free… | admin-held |  |
| 230 | `admin:karmicare-biorhythmic-oral-care-system:media.69840178282877.alt` | product | Karmicare Awake morning and Asleep evening toothpaste, fluoride-free, SLS-free and rich in nano-hyd… | admin-held |  |
| 231 | `admin:karmicare-biorhythmic-oral-care-system:media.69840178020733.alt` | product | Karmicare chronobiology infographic: your mouth runs on a 24-hour clock, with evening care at 22:00… | admin-held |  |
| 232 | `admin:karmicare-biorhythmic-oral-care-system:media.69840178250109.alt` | product | Karmicare Awake morning toothpaste, fluoride-free, SLS-free and rich in nano-hydroxyapatite, with g… | admin-held |  |
| 233 | `admin:karmicare-biorhythmic-oral-care-system:media.69840178315645.alt` | product | Karmicare Asleep evening toothpaste, fluoride-free, SLS-free and rich in nano-hydroxyapatite, with … | admin-held |  |
| 234 | `admin:karmicare-biorhythmic-oral-care-system:media.69840177987965.alt` | product | How to use Karmicare: rinse first, use 1 pump, spit and don't rinse. Leave-on toothpaste, fluoride-… | admin-held |  |
| 235 | `admin:karmicare-biorhythmic-oral-care-system:media.69840178381181.alt` | product | Karmicare nano-hydroxyapatite explainer showing nHAp crystals at the enamel surface | admin-held |  |
| 236 | `admin:karmicare-biorhythmic-oral-care-system:media.69884688236925.alt` | product | Animated view of the Karmicare Biorhythmic Oral Care Kit: fluoride-free, SLS-free Awake morning and… | admin-held | C C100 |
| 237 | `admin:morning-toothbrush-2-0:title` | product | Morning Toothbrush 2.0 | admin-held |  |
| 238 | `admin:evening-toothbrush-2-0:title` | product | Evening Toothbrush 2.0 | admin-held |  |
| 239 | `admin:whitening-charcoal-dental-floss:title` | product | Whitening Charcoal Floss | admin-held | C C100 |
| 240 | `admin:karmicare-biorhythmic-oral-care-system:custom.treatment_journey_*#01` | metafield | What you'll feel | admin-held |  |
| 241 | `admin:karmicare-biorhythmic-oral-care-system:custom.treatment_journey_*#02` | metafield | (and your dentist notices) | admin-held |  |
| 242 | `admin:karmicare-biorhythmic-oral-care-system:custom.treatment_journey_*#03` | metafield | First 60 days | admin-held |  |
| 243 | `admin:karmicare-biorhythmic-oral-care-system:custom.treatment_journey_*#04` | metafield | First brush | admin-held |  |
| 244 | `admin:karmicare-biorhythmic-oral-care-system:custom.treatment_journey_*#05` | metafield | — a smoother clean, an extra layer you can feel | admin-held |  |
| 245 | `admin:karmicare-biorhythmic-oral-care-system:custom.treatment_journey_*#06` | metafield | First night | admin-held |  |
| 246 | `admin:karmicare-biorhythmic-oral-care-system:custom.treatment_journey_*#07` | metafield | — feel the repair, it keeps working while you sleep | admin-held | C C98 |
| 247 | `admin:karmicare-biorhythmic-oral-care-system:custom.treatment_journey_*#08` | metafield | Week 1 | admin-held |  |
| 248 | `admin:karmicare-biorhythmic-oral-care-system:custom.treatment_journey_*#09` | metafield | — sensitivity starts to fade, the mineral layer builds | admin-held | C C95 |
| 249 | `admin:karmicare-biorhythmic-oral-care-system:custom.treatment_journey_*#10` | metafield | Week 2 | admin-held |  |
| 250 | `admin:karmicare-biorhythmic-oral-care-system:custom.treatment_journey_*#11` | metafield | — calmer gums, fresher breath, morning and night | admin-held | C C94 |
| 251 | `admin:karmicare-biorhythmic-oral-care-system:custom.treatment_journey_*#12` | metafield | Week 4 | admin-held |  |
| 252 | `admin:karmicare-biorhythmic-oral-care-system:custom.treatment_journey_*#13` | metafield | — less plaque, mouth bacteria back in balance (oral microbiome) | admin-held | C C96 |
| 253 | `admin:karmicare-biorhythmic-oral-care-system:custom.treatment_journey_*#14` | metafield | Week 6 | admin-held |  |
| 254 | `admin:karmicare-biorhythmic-oral-care-system:custom.treatment_journey_*#15` | metafield | — weak spots remineralised, enamel stronger | admin-held | C C97 |
| 255 | `admin:karmicare-biorhythmic-oral-care-system:custom.treatment_journey_*#16` | metafield | By day 60 | admin-held |  |
| 256 | `admin:karmicare-biorhythmic-oral-care-system:custom.treatment_journey_*#17` | metafield | — smoother, brighter, calmer care that strengthens more than your teeth | admin-held |  |
| 257 | `admin:karmicare-biorhythmic-oral-care-system:custom.treatment_journey_*#18` | metafield | The Karmicare effect | admin-held |  |
| 258 | `admin:karmicare-biorhythmic-oral-care-system:custom.treatment_journey_*#19` | metafield | Beyond 60 days | admin-held |  |
| 259 | `admin:karmicare-biorhythmic-oral-care-system:custom.treatment_journey_*#20` | metafield | Awake protects the day, Asleep restores the night* | admin-held |  |
| 260 | `admin:karmicare-biorhythmic-oral-care-system:custom.treatment_journey_*#21` | metafield | — you start needing both | admin-held |  |
| 261 | `admin:karmicare-biorhythmic-oral-care-system:custom.treatment_journey_*#22` | metafield | Calmer check-ups* | admin-held |  |
| 262 | `admin:karmicare-biorhythmic-oral-care-system:custom.treatment_journey_*#23` | metafield | — arrive resilient, you did the work at home | admin-held |  |
| 263 | `admin:karmicare-biorhythmic-oral-care-system:custom.treatment_journey_*#24` | metafield | Evenings that wind down* | admin-held |  |
| 264 | `admin:karmicare-biorhythmic-oral-care-system:custom.treatment_journey_*#25` | metafield | — no sting, nothing to rinse | admin-held |  |
| 265 | `admin:karmicare-biorhythmic-oral-care-system:custom.treatment_journey_*#26` | metafield | You smile more* | admin-held |  |
| 266 | `admin:karmicare-biorhythmic-oral-care-system:custom.treatment_journey_*#27` | metafield | — and think about it less | admin-held |  |
| 267 | `admin:karmicare-biorhythmic-oral-care-system:custom.treatment_journey_*#28` | metafield | Peace of mouth, peace of mind* | admin-held |  |
| 268 | `admin:karmicare-biorhythmic-oral-care-system:custom.treatment_journey_*#29` | metafield | — from your gums to the | admin-held |  |
| 269 | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#01` | metafield | Why Karmicare | admin-held |  |
| 270 | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#02` | metafield | Karmicare cares for both your mouth and your state of mind through two distinct brushing experience… | admin-held |  |
| 271 | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#03` | metafield | Ingredients | admin-held |  |
| 272 | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#04` | metafield | Actives Awake | admin-held |  |
| 273 | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#05` | metafield | Guarana | admin-held |  |
| 274 | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#06` | metafield | Peppermint + Lime | admin-held |  |
| 275 | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#07` | metafield | Bentonite clay | admin-held |  |
| 276 | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#08` | metafield | Actives Asleep | admin-held |  |
| 277 | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#09` | metafield | Valerian | admin-held |  |
| 278 | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#10` | metafield | Orange + Cinnamon | admin-held |  |
| 279 | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#11` | metafield | Activated charcoal | admin-held |  |
| 280 | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#12` | metafield | Foundation of both formulas | admin-held |  |
| 281 | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#13` | metafield | Nano-hydroxyapatite (nHAp), the mineral your teeth are made of | admin-held |  |
| 282 | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#14` | metafield | Xylitol, balances the oral microbiome | admin-held | C C37 |
| 283 | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#15` | metafield | Glycolipids, fermented sugar | admin-held |  |
| 284 | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#16` | metafield | Full ingredient list (INCI) | admin-held |  |
| 285 | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#17` | metafield | Awake Morning Toothpaste (2.0) | admin-held |  |
| 286 | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#18` | metafield | Aqua, Glycerin, Xylitol, Sorbitol, Calcium Carbonate, Hydroxyapatite [Nano], Hydrated Silica, Bento… | admin-held | NT |
| 287 | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#19` | metafield | Asleep Evening Toothpaste (2.0) | admin-held |  |
| 288 | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#20` | metafield | Aqua, Glycerin, Xylitol, Sorbitol, Calcium Carbonate, Hydroxyapatite [Nano], Hydrated Silica, Bento… | admin-held | NT |
| 289 | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#21` | metafield | What's not in it | admin-held |  |
| 290 | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#22` | metafield | Fluoride-free | admin-held |  |
| 291 | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#23` | metafield | SLS & sulfate-free | admin-held |  |
| 292 | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#24` | metafield | Sodium benzoate-free | admin-held |  |
| 293 | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#25` | metafield | Triclosan-free | admin-held |  |
| 294 | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#26` | metafield | Paraben-free | admin-held |  |
| 295 | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#27` | metafield | Microplastic-free | admin-held |  |
| 296 | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#28` | metafield | Alcohol-free | admin-held |  |
| 297 | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#29` | metafield | PEG-free | admin-held |  |
| 298 | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#30` | metafield | Saccharin-free | admin-held |  |
| 299 | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#31` | metafield | Vegan · animal-free | admin-held |  |
| 300 | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#32` | metafield | No artificial colours | admin-held |  |
| 301 | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#33` | metafield | How to use | admin-held |  |
| 302 | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#34` | metafield | Rinse first | admin-held |  |
| 303 | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#35` | metafield | Clean start | admin-held |  |
| 304 | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#36` | metafield | One pump | admin-held |  |
| 305 | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#37` | metafield | Full dosep | admin-held |  |
| 306 | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#38` | metafield | Spit, no rinse | admin-held |  |
| 307 | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#39` | metafield | Let it work | admin-held |  |
| 308 | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#40` | metafield | One precise, hygienic pump. Brush gently for 1–2 minutes. Spit, don’t rinse. | admin-held |  |
| 309 | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#41` | metafield | Run your tongue over your teeth: | admin-held |  |
| 310 | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#42` | metafield | that smooth edge is the clean | admin-held |  |
| 311 | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#43` | metafield | Rinsing ends it the moment it starts; the minerals leave with the water. Left on, the contact carri… | admin-held | C C90 |
| 312 | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#44` | metafield | Taste & feel | admin-held |  |
| 313 | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#45` | metafield | Before you start | admin-held |  |
| 314 | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#46` | metafield | a faint fuzz in the morning, the day’s coffee and talking in the evening. Don’t judge it — that’s y… | admin-held |  |
| 315 | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#47` | metafield | Awake: | admin-held | NT |
| 316 | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#48` | metafield | bright peppermint and lime, guarana underneath — a velvety foam, made with fermentation-derived gly… | admin-held |  |
| 317 | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#49` | metafield | Asleep: | admin-held | NT |
| 318 | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#50` | metafield | warm orange and cassia cinnamon, valerian in the background, intentionally mint-free. Spit and leav… | admin-held |  |
| 319 | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#51` | metafield | Tongue over teeth: | admin-held |  |
| 320 | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#52` | metafield | smooth, and a fine, even coat — as if the day had been closed. | admin-held |  |
| 321 | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#53` | metafield | The first week: | admin-held |  |
| 322 | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#54` | metafield | the velvety foam and the leave-on feel are what people notice first. By the fifth brush it’s the sm… | admin-held |  |
| 323 | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#55` | metafield | Quality & safety | admin-held |  |
| 324 | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#56` | metafield | Safety-assessed for leave-on use | admin-held | C C93 |
| 325 | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#57` | metafield | Independent EU-qualified assessor · Reg. 1223/2009 Annex I | admin-held |  |
| 326 | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#58` | metafield | CPSR · 2026 | admin-held |  |
| 327 | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#59` | metafield | VIEW ASSESSMENT SUMMARY | admin-held |  |
| 328 | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#60` | metafield | Notified on the EU cosmetic products portal | admin-held |  |
| 329 | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#61` | metafield | CPNP · Responsible Person KARMICA BV, Bruges | admin-held |  |
| 330 | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#62` | metafield | CPNP · 2026 | admin-held |  |
| 331 | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#63` | metafield | VIEW NOTIFICATION | admin-held |  |
| 332 | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#64` | metafield | nHAp within the EU SCCS-assessed specification | admin-held |  |
| 333 | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#65` | metafield | Rod-shaped, uncoated · Annex III entry 372 | admin-held |  |
| 334 | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#66` | metafield | SCCS/1677/25 | admin-held | NT |
| 335 | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#67` | metafield | READ THE OPINION | admin-held |  |
| 336 | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#68` | metafield | Abrasivity measured, not asserted | admin-held |  |
| 337 | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#69` | metafield | Midwest University · RDA 93 Awake, 72 Asleep · ISO 11609 limit 250 | admin-held | C C92 |
| 338 | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#70` | metafield | Report 25-RDA-123 · Dec 2025 | admin-held |  |
| 339 | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#71` | metafield | VIEW REPORT | admin-held |  |
| 340 | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#72` | metafield | Formulated on 36 peer-reviewed studies | admin-held | C C67 |
| 341 | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#73` | metafield | Every ingredient has a published reason · evidence library with DOIs | admin-held |  |
| 342 | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#74` | metafield | Evidence library · 2026 | admin-held |  |
| 343 | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#75` | metafield | READ OUR SCIENCE | admin-held |  |
| 344 | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#76` | metafield | See every document | admin-held |  |
| 345 | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#77` | metafield | For dentists | admin-held |  |
| 346 | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#78` | metafield | Formula | admin-held |  |
| 347 | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#79` | metafield | RDA | admin-held |  |
| 348 | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#80` | metafield | Safety · ISO 11609 | admin-held |  |
| 349 | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#81` | metafield | Awake | admin-held | NT |
| 350 | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#82` | metafield | · AM | admin-held |  |
| 351 | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#83` | metafield | 63% below limit | admin-held |  |
| 352 | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#84` | metafield | Asleep | admin-held | NT |
| 353 | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#85` | metafield | · PM | admin-held |  |
| 354 | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#86` | metafield | 71% below limit | admin-held |  |
| 355 | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#87` | metafield | ISO 11609 limit | admin-held |  |
| 356 | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#88` | metafield | Maximum allowed | admin-held |  |
| 357 | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#89` | metafield | Activated charcoal, in Asleep only. | admin-held |  |
| 358 | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#90` | metafield | Pharmaceutical grade (Ph. Eur. “Charcoal, Activated”), steam-activated from a 100% natural, renewab… | admin-held |  |
| 359 | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#91` | metafield | nHAp | admin-held | NT |
| 360 | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#92` | metafield | 100 nm · rod-shaped, per SCCS | admin-held |  |
| 361 | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#93` | metafield | Low–medium abrasivity | admin-held |  |
| 362 | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#94` | metafield | Mineral whitening | admin-held |  |
| 363 | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#95` | metafield | Leave-on safe | admin-held | C C93 |
| 364 | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#96` | metafield | Safe to swallow | admin-held | C C91 |
| 365 | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#97` | metafield | EU CPNP-notified | admin-held |  |
| 366 | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#98` | metafield | Request the evidence pack, patient-ready materials, professional samples and technical documentatio… | admin-held |  |
| 367 | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#99` | metafield | For kPNI / Orthomolecular practitioners | admin-held |  |
| 368 | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#100` | metafield | The missing oral-care piece in your protocols — biorhythmic, fluoride-free and connected through th… | admin-held |  |
| 369 | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#101` | metafield | Hormone-aware. | admin-held |  |
| 370 | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#102` | metafield | Formulated without fluoride and without known endocrine-active ingredients, for practitioners who r… | admin-held | C C44 |
| 371 | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#103` | metafield | Built on the body’s rhythm. | admin-held |  |
| 372 | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#104` | metafield | Awake for the cortisol morning, Asleep for the repair night — supporting the natural recovery proce… | admin-held | C C46 |
| 373 | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#105` | metafield | Oral–gut–brain axis | admin-held |  |
| 374 | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#106` | metafield | . What settles in the mouth is swallowed all night; the oral microbiome sits upstream of the gut an… | admin-held | C C43 |
| 375 | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#107` | metafield | Practitioner evidence pack and samples available → | admin-held |  |
| 376 | `admin:karmicare-biorhythmic-oral-care-system:custom.comparison_section#01` | metafield | CARE THAT COMPOUNDS | admin-held |  |
| 377 | `admin:karmicare-biorhythmic-oral-care-system:custom.comparison_section#02` | metafield | Everything else in your routine maintains. | admin-held |  |
| 378 | `admin:karmicare-biorhythmic-oral-care-system:custom.comparison_section#03` | metafield | This one strengthens your teeth, and yourself. | admin-held |  |
| 379 | `admin:karmicare-biorhythmic-oral-care-system:custom.comparison_section#04` | metafield | Awake protects the day. Asleep restores the night. Care timed to your biology — still working long … | admin-held |  |
| 380 | `admin:karmicare-biorhythmic-oral-care-system:custom.comparison_section#05` | metafield | Begin now | admin-held |  |
| 381 | `admin:karmicare-biorhythmic-oral-care-system:custom.comparison_section#06` | metafield | Compare | admin-held |  |
| 382 | `admin:karmicare-biorhythmic-oral-care-system:custom.comparison_section#07` | metafield | Regular brushing | admin-held |  |
| 383 | `admin:karmicare-biorhythmic-oral-care-system:custom.comparison_section#08` | metafield | Daily supplements | admin-held |  |
| 384 | `admin:karmicare-biorhythmic-oral-care-system:custom.comparison_section#09` | metafield | Skincare routine | admin-held |  |
| 385 | `admin:karmicare-biorhythmic-oral-care-system:custom.comparison_section#10` | metafield | It’s timed to your biology | admin-held |  |
| 386 | `admin:karmicare-biorhythmic-oral-care-system:custom.comparison_section#11` | metafield | Your mouth’s own 24-hour cycle | admin-held |  |
| 387 | `admin:karmicare-biorhythmic-oral-care-system:custom.comparison_section#12` | metafield | Same formula, any hour | admin-held |  |
| 388 | `admin:karmicare-biorhythmic-oral-care-system:custom.comparison_section#13` | metafield | One dose fits all | admin-held |  |
| 389 | `admin:karmicare-biorhythmic-oral-care-system:custom.comparison_section#14` | metafield | AM/PM by convention | admin-held |  |
| 390 | `admin:karmicare-biorhythmic-oral-care-system:custom.comparison_section#15` | metafield | You feel it straight away | admin-held | C C45 |
| 391 | `admin:karmicare-biorhythmic-oral-care-system:custom.comparison_section#16` | metafield | Guarana by day, valerian by night | admin-held |  |
| 392 | `admin:karmicare-biorhythmic-oral-care-system:custom.comparison_section#17` | metafield | Mint, then nothing | admin-held |  |
| 393 | `admin:karmicare-biorhythmic-oral-care-system:custom.comparison_section#18` | metafield | Weeks to notice | admin-held |  |
| 394 | `admin:karmicare-biorhythmic-oral-care-system:custom.comparison_section#19` | metafield | Nothing to feel | admin-held |  |
| 395 | `admin:karmicare-biorhythmic-oral-care-system:custom.comparison_section#20` | metafield | It reaches past your teeth | admin-held |  |
| 396 | `admin:karmicare-biorhythmic-oral-care-system:custom.comparison_section#21` | metafield | Oral-gut-brain, deeper than enamel | admin-held | C C42 |
| 397 | `admin:karmicare-biorhythmic-oral-care-system:custom.comparison_section#22` | metafield | Mechanical cleaning only | admin-held |  |
| 398 | `admin:karmicare-biorhythmic-oral-care-system:custom.comparison_section#23` | metafield | Systemic, not oral | admin-held |  |
| 399 | `admin:karmicare-biorhythmic-oral-care-system:custom.comparison_section#24` | metafield | Stops at the skin | admin-held |  |
| 400 | `admin:karmicare-biorhythmic-oral-care-system:custom.comparison_section#25` | metafield | It keeps working after you stop | admin-held |  |
| 401 | `admin:karmicare-biorhythmic-oral-care-system:custom.comparison_section#26` | metafield | Leave-on. No rinse. Extended contact time. | admin-held |  |
| 402 | `admin:karmicare-biorhythmic-oral-care-system:custom.comparison_section#27` | metafield | Rinsed away in seconds | admin-held |  |
| 403 | `admin:karmicare-biorhythmic-oral-care-system:custom.comparison_section#28` | metafield | Nothing local | admin-held |  |
| 404 | `admin:karmicare-biorhythmic-oral-care-system:custom.comparison_section#29` | metafield | Skin only | admin-held |  |
| 405 | `admin:karmicare-biorhythmic-oral-care-system:custom.comparison_section#30` | metafield | It feeds, not just cleans | admin-held |  |
| 406 | `admin:karmicare-biorhythmic-oral-care-system:custom.comparison_section#31` | metafield | One pump, minerals and balance | admin-held |  |
| 407 | `admin:karmicare-biorhythmic-oral-care-system:custom.comparison_section#32` | metafield | Squeeze, guess, rinse away | admin-held |  |
| 408 | `admin:karmicare-biorhythmic-oral-care-system:custom.comparison_section#33` | metafield | Nothing reaches enamel | admin-held |  |
| 409 | `admin:karmicare-biorhythmic-oral-care-system:custom.comparison_section#34` | metafield | Surface renewal only | admin-held |  |
| 410 | `admin:karmicare-biorhythmic-oral-care-system:custom.comparison_section#35` | metafield | The person it makes you | admin-held |  |
| 411 | `admin:karmicare-biorhythmic-oral-care-system:custom.comparison_section#36` | metafield | Someone who tends to themselves | admin-held |  |
| 412 | `admin:karmicare-biorhythmic-oral-care-system:custom.comparison_section#37` | metafield | Someone who ticks a box | admin-held |  |
| 413 | `admin:karmicare-biorhythmic-oral-care-system:custom.comparison_section#38` | metafield | Someone who means to | admin-held |  |
| 414 | `admin:karmicare-biorhythmic-oral-care-system:custom.comparison_section#39` | metafield | Someone who tends the surface | admin-held |  |
| 415 | `admin:karmicare-biorhythmic-oral-care-system:custom.professional_testimonials#01` | metaobject | Leen Ponet | admin-held | NT |
| 416 | `admin:karmicare-biorhythmic-oral-care-system:custom.professional_testimonials#02` | metaobject | Pharmacist, Orthomolecular Therapist, kPNI Coordinator | admin-held |  |
| 417 | `admin:karmicare-biorhythmic-oral-care-system:custom.professional_testimonials#03` | metaobject | Sietske Hamelink | admin-held | NT |
| 418 | `admin:karmicare-biorhythmic-oral-care-system:custom.professional_testimonials#04` | metaobject | Nutritional Therapist, Menstrual Cycle Expert | admin-held |  |
| 419 | `admin:karmicare-biorhythmic-oral-care-system:custom.professional_testimonials#05` | metaobject | Mariama Banjai | admin-held | NT |
| 420 | `admin:karmicare-biorhythmic-oral-care-system:custom.professional_testimonials#06` | metaobject | Dental Hygienist, Oral Care Quality Manager | admin-held |  |
| 421 | `admin:karmicare-biorhythmic-oral-care-system:custom.professional_testimonials#07` | metaobject | Kim Verlot | admin-held | NT |
| 422 | `admin:karmicare-biorhythmic-oral-care-system:custom.professional_testimonials#08` | metaobject | Breathing Coach, Heart Coherence Specialist | admin-held |  |
| 423 | `admin:karmicare-biorhythmic-oral-care-system:custom.professional_testimonials#09` | metaobject | Dr. Kris Sienaert | admin-held | NT |
| 424 | `admin:karmicare-biorhythmic-oral-care-system:custom.professional_testimonials#10` | metaobject | Former GP, Lifestyle Medicine | admin-held |  |
| 425 | `admin:karmicare-biorhythmic-oral-care-system:custom.professional_testimonials#11` | metaobject | Dr. Iveta Pleša Rutule | admin-held | NT |
| 426 | `admin:karmicare-biorhythmic-oral-care-system:custom.professional_testimonials#12` | metaobject | Holistic Dentist | admin-held |  |
| 427 | `admin:karmicare-biorhythmic-oral-care-system:custom.professional_testimonials#13` | metaobject | Dr. Stephanie Spreuwers | admin-held | NT |
| 428 | `admin:karmicare-biorhythmic-oral-care-system:custom.professional_testimonials#14` | metaobject | Functional Dentist, kPNI Therapist | admin-held |  |
| 429 | `admin:karmicare-biorhythmic-oral-care-system:custom.mission_card#01` | metaobject | OUR MISSION | admin-held |  |
| 430 | `admin:karmicare-biorhythmic-oral-care-system:custom.mission_card#02` | metaobject | Strengthen your teeth. | admin-held |  |
| 431 | `admin:karmicare-biorhythmic-oral-care-system:custom.mission_card#03` | metaobject | Strengthen yourself. | admin-held |  |
| 432 | `admin:karmicare-biorhythmic-oral-care-system:custom.mission_card#04` | metaobject | I built Karmicare from my own reset — when caring for my mouth became caring for my whole self. | admin-held |  |
| 433 | `admin:karmicare-biorhythmic-oral-care-system:custom.mission_card#05` | metaobject | — Victor, | admin-held |  |
| 434 | `admin:karmicare-biorhythmic-oral-care-system:custom.mission_card#06` | metaobject | founder | admin-held |  |
| 435 | `admin:karmicare-biorhythmic-oral-care-system:custom.how_it_works_steps#01` | metaobject | Rinse before | admin-held |  |
| 436 | `admin:karmicare-biorhythmic-oral-care-system:custom.how_it_works_steps#02` | metaobject | Start with a rinse before brushing. | admin-held |  |
| 437 | `admin:karmicare-biorhythmic-oral-care-system:custom.compare_table_header_footer#01` | metaobject | choose your rhythm | admin-held |  |
| 438 | `admin:karmicare-biorhythmic-oral-care-system:custom.compare_table_header_footer#02` | metaobject | One system. | admin-held |  |
| 439 | `admin:karmicare-biorhythmic-oral-care-system:custom.compare_table_header_footer#03` | metaobject | Three ways to begin. | admin-held |  |
| 440 | `admin:karmicare-biorhythmic-oral-care-system:custom.compare_table|shop.metaobjects.compare_value#01` | metaobject | Start with one set, refill every 60 days, or choose the full year — the ritual stays the same: Awak… | admin-held |  |
| 441 | `admin:karmicare-biorhythmic-oral-care-system:custom.compare_table|shop.metaobjects.compare_value#02` | metaobject | Duos in a year | admin-held |  |
| 442 | `admin:karmicare-biorhythmic-oral-care-system:custom.compare_table|shop.metaobjects.compare_value#03` | metaobject | Cost per brushing | admin-held |  |
| 443 | `admin:karmicare-biorhythmic-oral-care-system:custom.compare_table|shop.metaobjects.compare_value#04` | metaobject | Delivery rhythm | admin-held |  |
| 444 | `admin:karmicare-biorhythmic-oral-care-system:custom.compare_table|shop.metaobjects.compare_value#05` | metaobject | Return on Care | admin-held |  |
| 445 | `admin:karmicare-biorhythmic-oral-care-system:custom.compare_table|shop.metaobjects.compare_value#06` | metaobject | Return on Care is our give-back: a share of every delivery comes back to you as Care Credit — in eu… | admin-held |  |
| 446 | `admin:karmicare-biorhythmic-oral-care-system:custom.compare_table|shop.metaobjects.compare_value#07` | metaobject | Care Credit earned in a year | admin-held |  |
| 447 | `admin:karmicare-biorhythmic-oral-care-system:custom.compare_table|shop.metaobjects.compare_value#08` | metaobject | Care Credit is what Return on Care pays out — in euros, spendable on member products and accessorie… | admin-held |  |
| 448 | `admin:karmicare-biorhythmic-oral-care-system:custom.compare_table|shop.metaobjects.compare_value#09` | metaobject | Welcome Kit | admin-held |  |
| 449 | `admin:karmicare-biorhythmic-oral-care-system:custom.compare_table|shop.metaobjects.compare_value#10` | metaobject | Complete a dental check-up from month 6 or onwards, verified by your dentist. €40 in Care Credit is… | admin-held |  |
| 450 | `admin:karmicare-biorhythmic-oral-care-system:custom.compare_table|shop.metaobjects.compare_value#11` | metaobject | Skip, pause or cancel | admin-held |  |
| 451 | `admin:karmicare-biorhythmic-oral-care-system:custom.compare_table|shop.metaobjects.compare_value#12` | metaobject | Shipping | admin-held |  |
| 452 | `admin:karmicare-biorhythmic-oral-care-system:custom.compare_table|shop.metaobjects.compare_value#13` | metaobject | Money-back guarantee | admin-held |  |
| 453 | `admin:karmicare-biorhythmic-oral-care-system:custom.compare_table|shop.metaobjects.compare_value#14` | metaobject | Try Once | admin-held |  |
| 454 | `admin:karmicare-biorhythmic-oral-care-system:custom.compare_table|shop.metaobjects.compare_value#15` | metaobject | one-time | admin-held |  |
| 455 | `admin:karmicare-biorhythmic-oral-care-system:custom.compare_table|shop.metaobjects.compare_value#16` | metaobject | One delivery | admin-held |  |
| 456 | `admin:karmicare-biorhythmic-oral-care-system:custom.compare_table|shop.metaobjects.compare_value#17` | metaobject | Calculated at checkout | admin-held |  |
| 457 | `admin:karmicare-biorhythmic-oral-care-system:custom.compare_table|shop.metaobjects.compare_value#18` | metaobject | ★ Most Picked | admin-held |  |
| 458 | `admin:karmicare-biorhythmic-oral-care-system:custom.compare_table|shop.metaobjects.compare_value#19` | metaobject | 60-Day Rhythm | admin-held |  |
| 459 | `admin:karmicare-biorhythmic-oral-care-system:custom.compare_table|shop.metaobjects.compare_value#20` | metaobject | /60 days | admin-held |  |
| 460 | `admin:karmicare-biorhythmic-oral-care-system:custom.compare_table|shop.metaobjects.compare_value#21` | metaobject | Every 60 days | admin-held |  |
| 461 | `admin:karmicare-biorhythmic-oral-care-system:custom.compare_table|shop.metaobjects.compare_value#22` | metaobject | 10% back | admin-held |  |
| 462 | `admin:karmicare-biorhythmic-oral-care-system:custom.compare_table|shop.metaobjects.compare_value#23` | metaobject | Upgradable | admin-held |  |
| 463 | `admin:karmicare-biorhythmic-oral-care-system:custom.compare_table|shop.metaobjects.compare_value#24` | metaobject | 60 days | admin-held |  |
| 464 | `admin:karmicare-biorhythmic-oral-care-system:custom.compare_table|shop.metaobjects.compare_value#25` | metaobject | Begin 60-Day Rhythm | admin-held |  |
| 465 | `admin:karmicare-biorhythmic-oral-care-system:custom.compare_table|shop.metaobjects.compare_value#26` | metaobject | Brushing & Beyond | admin-held |  |
| 466 | `admin:karmicare-biorhythmic-oral-care-system:custom.compare_table|shop.metaobjects.compare_value#27` | metaobject | /year | admin-held |  |
| 467 | `admin:karmicare-biorhythmic-oral-care-system:custom.compare_table|shop.metaobjects.compare_value#28` | metaobject | 2× a year | admin-held |  |
| 468 | `admin:karmicare-biorhythmic-oral-care-system:custom.compare_table|shop.metaobjects.compare_value#29` | metaobject | Two shipments a year — the first at signup, the second around month 6. Each is a six-month supply o… | admin-held |  |
| 469 | `admin:karmicare-biorhythmic-oral-care-system:custom.compare_table|shop.metaobjects.compare_value#30` | metaobject | 20% back | admin-held |  |
| 470 | `admin:karmicare-biorhythmic-oral-care-system:custom.compare_table|shop.metaobjects.compare_value#31` | metaobject | Begin | admin-held |  |
| 471 | `admin:karmicare-biorhythmic-oral-care-system:custom.compare_table_header_footer#04` | metaobject | Every subscription earns | admin-held |  |
| 472 | `admin:karmicare-biorhythmic-oral-care-system:custom.compare_table_header_footer#05` | metaobject | Care Credit: | admin-held |  |
| 473 | `admin:karmicare-biorhythmic-oral-care-system:custom.compare_table_header_footer#06` | metaobject | a return on the care you keep. | admin-held |  |
| 474 | `admin:karmicare-biorhythmic-oral-care-system:shop.metaobjects.compare_value:try_once.cost_per_brushing` | metaobject | €0.56 | admin-held |  |
| 475 | `admin:karmicare-biorhythmic-oral-care-system:shop.metaobjects.compare_value:rhythm.cost_per_brushing` | metaobject | €0.49 | admin-held |  |
| 476 | `admin:karmicare-biorhythmic-oral-care-system:shop.metaobjects.compare_value:year.cost_per_brushing` | metaobject | €0.42 | admin-held |  |
| 477 | `admin:karmicare-biorhythmic-oral-care-system:custom.compare_table:welcome_kit_row.products` | metaobject | Morning Toothbrush · Evening Toothbrush · Whitening Charcoal Floss | admin-held | C C100 |

### `batch-03-header-footer`

| # | id | type | EN | status | flags |
|---:|---|---|---|---|---|
| 1 | `header-group:announcement-bar/announcement-bar-0/text` | section_group | COMPLIMENTARY SHIPPING & 60-DAY MONEY-BACK GUARANTEE FOR MEMBERS · BELGIAN-MADE · CIRCADIAN ORAL CARE SINCE 2017 | corrected | C C103 |
| 2 | `header-group:header/cta_text` | section_group | BEGIN NOW | approved |  |
| 3 | `footer-group:footer/slogan` | section_group | Your mouth has a rhythm So should your oral care | needs-review |  |
| 4 | `footer-group:footer/copyright_text` | section_group | Copyright © ∞ KARMICARE. All rights reserved. KARMICARE™ Biorhythmic Toothpaste Kit (Awake + Asleep… | corrected | C C99 |
| 5 | `footer-group:footer/newsletter_heading` | section_group | Newsletter | approved |  |
| 6 | `footer-group:footer/link_list_Yna7wT/heading` | section_group | Company | approved |  |
| 7 | `locale:sections.announcements.announcement` | theme_locale | Announcement | approved |  |
| 8 | `locale:sections.header.menu` | theme_locale | Menu | approved |  |
| 9 | `locale:customer.log_in` | theme_locale | Log in | approved |  |
| 10 | `locale:localization.country_label` | theme_locale | Country/region | approved |  |
| 11 | `locale:general.search.search` | theme_locale | Search | approved |  |
| 12 | `locale:general.search.reset` | theme_locale | Clear search term | approved |  |
| 13 | `locale:accessibility.close` | theme_locale | Close | approved |  |
| 14 | `locale:localization.language_label` | theme_locale | Language | approved |  |
| 15 | `locale:general.social.links.facebook` | theme_locale | Facebook | approved | NT |
| 16 | `locale:general.social.links.instagram` | theme_locale | Instagram | approved | NT |
| 17 | `locale:newsletter.label` | theme_locale | Email | approved |  |
| 18 | `liquid:sections/header.liquid:1077` | theme_locale | Coming soon | needs-key |  |
| 19 | `liquid:sections/footer.liquid:660` | theme_locale | Email | needs-key |  |
| 20 | `liquid:sections/footer.liquid:667` | theme_locale | you@example.com | needs-key |  |
| 21 | `liquid:sections/footer.liquid:679` | theme_locale | Join | needs-key |  |
| 22 | `liquid:sections/footer.liquid:694` | theme_locale | By subscribing you agree to the Terms of Use & Privacy Policy . | needs-key |  |
| 23 | `liquid:sections/footer.liquid:850` | theme_locale | Language | needs-key |  |
| 24 | `liquid:sections/footer.liquid:868` | theme_locale | Country/Region | needs-key |  |
| 25 | `liquid:sections/footer.liquid:1034` | theme_locale | Terms and Conditions | needs-key |  |
| 26 | `liquid:sections/footer.liquid:1046` | theme_locale | Privacy Policy | needs-key |  |
| 27 | `liquid:sections/footer.liquid:1058` | theme_locale | Consumer Rights | needs-key |  |
| 28 | `liquid:sections/footer.liquid:706` | theme_locale | Instagram | approved | NT |
| 29 | `liquid:sections/footer.liquid:733` | theme_locale | Facebook | approved | NT |
| 30 | `liquid:sections/footer.liquid:760` | theme_locale | LinkedIn | approved | NT |
| 31 | `admin:customer-privacy:footer.cookie_preferences` | app | Cookie preferences | admin-held |  |
| 32 | `admin:navigation:new-main-menu:links[1].title` | navigation | Manifesto | admin-held |  |
| 33 | `admin:navigation:new-main-menu:links[2].title` | navigation | Science | admin-held |  |
| 34 | `admin:navigation:new-main-menu:links[3].title` | navigation | Professionals | admin-held |  |
| 35 | `admin:navigation:new-main-menu:links[4].title` | navigation | Members | admin-held |  |
| 36 | `admin:navigation:company:links[1].title` | navigation | Shop Karmicare | admin-held |  |
| 37 | `admin:navigation:company:links[2].title` | navigation | Why use hydroxapatite | admin-held |  |
| 38 | `admin:navigation:company:links[3].title` | navigation | Why Karmicare | admin-held |  |
| 39 | `admin:navigation:company:links[4].title` | navigation | nHAp Technology | admin-held |  |
| 40 | `admin:navigation:company:links[5].title` | navigation | Contact | admin-held |  |
| 41 | `admin:navigation:company:links[6].title` | navigation | Articles | admin-held |  |

### `batch-04-legal`

| # | id | type | EN | status | flags |
|---:|---|---|---|---|---|
| 1 | `page.consumer-rights:policy_banner_Pgpxip/eyebrow` | template_setting | LEGAL | approved |  |
| 2 | `page.consumer-rights:policy_banner_Pgpxip/heading` | template_setting | Consumer Rights & Transparency Charter | approved |  |
| 3 | `page.consumer-rights:policy_banner_Pgpxip/description` | template_setting | Your rights under Belgian and EU law, together with the promises Karmicare adds on top. | approved |  |
| 4 | `page.consumer-rights:policy_banner_Pgpxip/company_info` | template_setting | KARMICA BV, trading as KARMICARE · Vizierstraat 28, 8000 Bruges, Belgium · VAT BE 0676.972.896 · EO… | approved |  |
| 5 | `page.consumer-rights:policy_banner_Pgpxip/company_last_updated` | template_setting | care@karmicare.com · Last updated October 2026 | approved |  |
| 6 | `page.consumer-rights:policy_banner_Pgpxip/benefit_card_MptPUi/card_title` | template_setting | 14 days | approved |  |
| 7 | `page.consumer-rights:policy_banner_Pgpxip/benefit_card_MptPUi/card_description` | template_setting | To change your mind | approved |  |
| 8 | `page.consumer-rights:policy_banner_Pgpxip/benefit_card_MptPUi/card_bottom_text` | template_setting | Legal right, plus Try Once money-back | approved |  |
| 9 | `page.consumer-rights:policy_banner_Pgpxip/benefit_card_hiciT4/card_title` | template_setting | 60 days | approved |  |
| 10 | `page.consumer-rights:policy_banner_Pgpxip/benefit_card_hiciT4/card_description` | template_setting | Money-back guarantee | approved |  |
| 11 | `page.consumer-rights:policy_banner_Pgpxip/benefit_card_hiciT4/card_bottom_text` | template_setting | Karmicare promise · memberships | approved |  |
| 12 | `page.consumer-rights:policy_banner_Pgpxip/benefit_card_3DXGyT/card_title` | template_setting | 14 days | approved |  |
| 13 | `page.consumer-rights:policy_banner_Pgpxip/benefit_card_3DXGyT/card_description` | template_setting | To receive your refund | approved |  |
| 14 | `page.consumer-rights:policy_banner_Pgpxip/benefit_card_3DXGyT/card_bottom_text` | template_setting | After approval · same payment method | approved |  |
| 15 | `page.consumer-rights:policy_banner_Pgpxip/benefit_card_Q4tabr/card_title` | template_setting | 2 years | approved |  |
| 16 | `page.consumer-rights:policy_banner_Pgpxip/benefit_card_Q4tabr/card_description` | template_setting | Legal guarantee | approved |  |
| 17 | `page.consumer-rights:policy_banner_Pgpxip/benefit_card_Q4tabr/card_bottom_text` | template_setting | Legal right · every order | approved |  |
| 18 | `page.consumer-rights:legal_toc_section_gYznx3/nav_title` | template_setting | On this page | approved |  |
| 19 | `page.consumer-rights:legal_toc_section_gYznx3/content_section_GLa7AN/nav_label` | template_setting | Our commitment | approved |  |
| 20 | `page.consumer-rights:legal_toc_section_gYznx3/content_section_GLa7AN/title` | template_setting | 1. Our commitment to trust and transparency | approved |  |
| 21 | `page.consumer-rights:legal_toc_section_gYznx3/content_section_GLa7AN/content` | template_setting | Your rights come from the law, not from our goodwill. This page sets them out in one place, alongsi… | approved |  |
| 22 | `page.consumer-rights:legal_toc_section_gYznx3/content_section_g6nYeY/nav_label` | template_setting | Safety and standards | approved |  |
| 23 | `page.consumer-rights:legal_toc_section_gYznx3/content_section_g6nYeY/title` | template_setting | 2. EU cosmetic safety and standards | approved |  |
| 24 | `page.consumer-rights:legal_toc_section_gYznx3/content_section_g6nYeY/content` | template_setting | Awake and Asleep are notified EU cosmetics, made under Good Manufacturing Practice and assessed by … | approved |  |
| 25 | `page.consumer-rights:legal_toc_section_gYznx3/content_section_iDEfUH/nav_label` | template_setting | Refunds and guarantees | approved |  |
| 26 | `page.consumer-rights:legal_toc_section_gYznx3/content_section_iDEfUH/title` | template_setting | 3. Refunds, withdrawal and money-back guarantees | approved |  |
| 27 | `page.consumer-rights:legal_toc_section_gYznx3/content_section_iDEfUH/content` | template_setting | Every first order comes with a money-back guarantee: 14 days on Try Once, your first cycle on the 6… | approved |  |
| 28 | `page.consumer-rights:legal_toc_section_gYznx3/content_section_FcEDdA/nav_label` | template_setting | Two-year guarantee | approved |  |
| 29 | `page.consumer-rights:legal_toc_section_gYznx3/content_section_FcEDdA/title` | template_setting | 4. Two-year legal guarantee of conformity | approved |  |
| 30 | `page.consumer-rights:legal_toc_section_gYznx3/content_section_FcEDdA/content` | template_setting | If something is faulty, you are covered for two years from delivery, and the law assumes the fault … | approved |  |
| 31 | `page.consumer-rights:legal_toc_section_gYznx3/content_section_xKcNPj/nav_label` | template_setting | Delivery | approved |  |
| 32 | `page.consumer-rights:legal_toc_section_gYznx3/content_section_xKcNPj/title` | template_setting | 5. Delivery and risk in transit | approved |  |
| 33 | `page.consumer-rights:legal_toc_section_gYznx3/content_section_xKcNPj/content` | template_setting | Until your parcel is in your hands, it is our responsibility. Where we deliver: to every member sta… | approved |  |
| 34 | `page.consumer-rights:legal_toc_section_gYznx3/content_section_rnPj6g/nav_label` | template_setting | Your membership | approved |  |
| 35 | `page.consumer-rights:legal_toc_section_gYznx3/content_section_rnPj6g/title` | template_setting | 6. Your membership: renewals, pauses and cancelling | approved |  |
| 36 | `page.consumer-rights:legal_toc_section_gYznx3/content_section_rnPj6g/content` | template_setting | No lock-in. Your member price stays the same, we remind you before every renewal, and you can gift,… | approved |  |
| 37 | `page.consumer-rights:legal_toc_section_gYznx3/content_section_EAKJLC/nav_label` | template_setting | Pricing | approved |  |
| 38 | `page.consumer-rights:legal_toc_section_gYznx3/content_section_EAKJLC/title` | template_setting | 7. Pricing transparency | approved |  |
| 39 | `page.consumer-rights:legal_toc_section_gYznx3/content_section_EAKJLC/content` | template_setting | The price you see includes VAT. A “was” price is always our lowest price of the previous 30 days, a… | approved |  |
| 40 | `page.consumer-rights:legal_toc_section_gYznx3/content_section_dGmgBJ/nav_label` | template_setting | Complaints | approved |  |
| 41 | `page.consumer-rights:legal_toc_section_gYznx3/content_section_dGmgBJ/title` | template_setting | 8. Complaints and dispute resolution | approved |  |
| 42 | `page.consumer-rights:legal_toc_section_gYznx3/content_section_dGmgBJ/content` | template_setting | Write to us first: we reply within 2 working days and give you a solution or a substantiated answer… | approved |  |
| 43 | `page.consumer-rights:legal_toc_section_gYznx3/content_section_CDtWCV/nav_label` | template_setting | Applicable law | approved |  |
| 44 | `page.consumer-rights:legal_toc_section_gYznx3/content_section_CDtWCV/title` | template_setting | 9. Applicable law and jurisdiction | approved |  |
| 45 | `page.consumer-rights:legal_toc_section_gYznx3/content_section_CDtWCV/content` | template_setting | Belgian law applies, but never at the expense of the protection your own country gives you. Contrac… | approved |  |
| 46 | `page.consumer-rights:legal_toc_section_gYznx3/content_section_at3pLy/nav_label` | template_setting | Withdrawal form | approved |  |
| 47 | `page.consumer-rights:legal_toc_section_gYznx3/content_section_at3pLy/title` | template_setting | 10. Model withdrawal form | approved |  |
| 48 | `page.consumer-rights:legal_toc_section_gYznx3/content_section_at3pLy/content` | template_setting | Changed your mind about a one-time order? Send us this form, or simply email us a clear statement. … | approved |  |
| 49 | `page.privacy-policy:policy_banner_Pgpxip/eyebrow` | template_setting | LEGAL | approved |  |
| 50 | `page.privacy-policy:policy_banner_Pgpxip/heading` | template_setting | Privacy Policy | approved |  |
| 51 | `page.privacy-policy:policy_banner_Pgpxip/description` | template_setting | How we collect, use and protect your personal data, and how you stay in control of it. | approved |  |
| 52 | `page.privacy-policy:policy_banner_Pgpxip/company_info` | template_setting | KARMICA BV, trading as KARMICARE · Vizierstraat 28, 8000 Bruges, Belgium · VAT BE 0676.972.896 · RP… | approved |  |
| 53 | `page.privacy-policy:policy_banner_Pgpxip/company_last_updated` | template_setting | care@karmicare.com · Last updated October 2026 | approved |  |
| 54 | `page.privacy-policy:legal_toc_section_gYznx3/nav_title` | template_setting | On this page | approved |  |
| 55 | `page.privacy-policy:legal_toc_section_gYznx3/content_section_GLa7AN/nav_label` | template_setting | Introduction | approved |  |
| 56 | `page.privacy-policy:legal_toc_section_gYznx3/content_section_GLa7AN/title` | template_setting | 1. Introduction and scope | approved |  |
| 57 | `page.privacy-policy:legal_toc_section_gYznx3/content_section_GLa7AN/content` | template_setting | This policy explains what we collect about you, why we need it, who helps us process it, and how yo… | approved |  |
| 58 | `page.privacy-policy:legal_toc_section_gYznx3/content_section_g6nYeY/nav_label` | template_setting | Who we are | approved |  |
| 59 | `page.privacy-policy:legal_toc_section_gYznx3/content_section_g6nYeY/title` | template_setting | 2. Data controller | approved |  |
| 60 | `page.privacy-policy:legal_toc_section_gYznx3/content_section_g6nYeY/content` | template_setting | KARMICA BV in Bruges is responsible for your personal data. Every privacy question goes to one addr… | approved |  |
| 61 | `page.privacy-policy:legal_toc_section_gYznx3/content_section_iDEfUH/nav_label` | template_setting | Data we process | approved |  |
| 62 | `page.privacy-policy:legal_toc_section_gYznx3/content_section_iDEfUH/title` | template_setting | 3. Personal data we process | approved |  |
| 63 | `page.privacy-policy:legal_toc_section_gYznx3/content_section_iDEfUH/content` | template_setting | We collect what we need to deliver your order, run your membership and answer your questions. Oral-… | approved |  |
| 64 | `page.privacy-policy:legal_toc_section_gYznx3/content_section_FcEDdA/nav_label` | template_setting | Purposes | approved |  |
| 65 | `page.privacy-policy:legal_toc_section_gYznx3/content_section_FcEDdA/title` | template_setting | 4. Purposes and legal bases | approved |  |
| 66 | `page.privacy-policy:legal_toc_section_gYznx3/content_section_FcEDdA/content` | template_setting | Every use of your data rests on a legal basis: your contract, a legal duty, a legitimate interest o… | approved |  |
| 67 | `page.privacy-policy:legal_toc_section_gYznx3/content_section_FcEDdA/block_content` | template_setting | Order processing and fulfilment Processing orders, delivering, sending order updates and managing r… | approved |  |
| 68 | `page.privacy-policy:legal_toc_section_gYznx3/content_section_xKcNPj/nav_label` | template_setting | Service providers | approved |  |
| 69 | `page.privacy-policy:legal_toc_section_gYznx3/content_section_xKcNPj/title` | template_setting | 5. Service providers and recipients | approved |  |
| 70 | `page.privacy-policy:legal_toc_section_gYznx3/content_section_xKcNPj/content` | template_setting | We never sell your data. A small set of service providers helps us run the shop, each under a writt… | approved |  |
| 71 | `page.privacy-policy:legal_toc_section_gYznx3/content_section_rnPj6g/nav_label` | template_setting | Transfers | approved |  |
| 72 | `page.privacy-policy:legal_toc_section_gYznx3/content_section_rnPj6g/title` | template_setting | 6. International data transfers | approved |  |
| 73 | `page.privacy-policy:legal_toc_section_gYznx3/content_section_rnPj6g/content` | template_setting | When your data leaves the European Economic Area, it travels under an EU-approved safeguard. When p… | approved |  |
| 74 | `page.privacy-policy:legal_toc_section_gYznx3/content_section_EAKJLC/nav_label` | template_setting | Retention | approved |  |
| 75 | `page.privacy-policy:legal_toc_section_gYznx3/content_section_EAKJLC/title` | template_setting | 7. How long we keep your data | approved |  |
| 76 | `page.privacy-policy:legal_toc_section_gYznx3/content_section_EAKJLC/content` | template_setting | We keep your data only as long as the purpose or the law requires, then delete or anonymise it. We … | approved |  |
| 77 | `page.privacy-policy:legal_toc_section_gYznx3/content_section_dGmgBJ/nav_label` | template_setting | Your rights | approved |  |
| 78 | `page.privacy-policy:legal_toc_section_gYznx3/content_section_dGmgBJ/title` | template_setting | 8. Your rights under the GDPR | approved |  |
| 79 | `page.privacy-policy:legal_toc_section_gYznx3/content_section_dGmgBJ/content` | template_setting | You can see, correct, delete, move or limit your data, and object to marketing at any time. We answ… | approved |  |
| 80 | `page.privacy-policy:legal_toc_section_gYznx3/content_section_CDtWCV/nav_label` | template_setting | Cookies | approved |  |
| 81 | `page.privacy-policy:legal_toc_section_gYznx3/content_section_CDtWCV/title` | template_setting | 9. Cookies and tracking | approved |  |
| 82 | `page.privacy-policy:legal_toc_section_gYznx3/content_section_CDtWCV/content` | template_setting | Essential cookies keep the shop working. Everything else waits for your consent, and you can change… | approved |  |
| 83 | `page.privacy-policy:legal_toc_section_gYznx3/content_section_qyyKHX/nav_label` | template_setting | Security | approved |  |
| 84 | `page.privacy-policy:legal_toc_section_gYznx3/content_section_qyyKHX/title` | template_setting | 10. Data security | approved |  |
| 85 | `page.privacy-policy:legal_toc_section_gYznx3/content_section_qyyKHX/content` | template_setting | Your data travels encrypted, and only the people who need it can reach it. KARMICA BV uses technica… | approved |  |
| 86 | `page.privacy-policy:legal_toc_section_gYznx3/content_section_pjNTAq/nav_label` | template_setting | Changes | approved |  |
| 87 | `page.privacy-policy:legal_toc_section_gYznx3/content_section_pjNTAq/title` | template_setting | 11. Changes to this policy | approved |  |
| 88 | `page.privacy-policy:legal_toc_section_gYznx3/content_section_pjNTAq/content` | template_setting | When this policy changes, the date at the top changes too, and we tell you first about anything imp… | approved |  |
| 89 | `page.terms-and-conditions:policy_banner_Pgpxip/eyebrow` | template_setting | LEGAL | approved |  |
| 90 | `page.terms-and-conditions:policy_banner_Pgpxip/heading` | template_setting | Terms and Conditions | approved |  |
| 91 | `page.terms-and-conditions:policy_banner_Pgpxip/description` | template_setting | The terms that apply to every order and plan on karmicare.com, including your rights to withdraw, r… | approved |  |
| 92 | `page.terms-and-conditions:policy_banner_Pgpxip/company_info` | template_setting | KARMICA BV, trading as KARMICARE · Vizierstraat 28, 8000 Bruges, Belgium · VAT BE 0676.972.896 · EO… | approved |  |
| 93 | `page.terms-and-conditions:policy_banner_Pgpxip/company_last_updated` | template_setting | care@karmicare.com · Last updated October 2026 | approved |  |
| 94 | `page.terms-and-conditions:legal_toc_section_gYznx3/nav_title` | template_setting | On this page | approved |  |
| 95 | `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_GLa7AN/nav_label` | template_setting | Vendor | approved |  |
| 96 | `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_GLa7AN/title` | template_setting | Clause 1 – Identity of the vendor | approved |  |
| 97 | `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_GLa7AN/content` | template_setting | You buy from KARMICA BV, a Belgian company in Bruges. The webshop karmicare.com and its checkout su… | approved |  |
| 98 | `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_g6nYeY/nav_label` | template_setting | Scope | approved |  |
| 99 | `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_g6nYeY/title` | template_setting | Clause 2 – Applicability and international scope | approved |  |
| 100 | `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_g6nYeY/content` | template_setting | These terms apply to every order and membership you place on karmicare.com. These General Terms and… | approved |  |
| 101 | `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_iDEfUH/nav_label` | template_setting | Offers and contract | approved |  |
| 102 | `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_iDEfUH/title` | template_setting | Clause 3 – Product classification, offers and contract formation | approved |  |
| 103 | `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_iDEfUH/content` | template_setting | Awake and Asleep are cosmetics, not medicines. Your order becomes a contract once we confirm it by … | approved |  |
| 104 | `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_FcEDdA/nav_label` | template_setting | Withdrawal and guarantees | approved |  |
| 105 | `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_FcEDdA/title` | template_setting | Clause 4 – Withdrawal, money-back guarantees and refunds | approved |  |
| 106 | `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_FcEDdA/content` | template_setting | Every first order comes with a money-back guarantee: 14 days on Try Once, your first cycle on the 6… | approved |  |
| 107 | `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_xKcNPj/nav_label` | template_setting | Prices and shipping | approved |  |
| 108 | `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_xKcNPj/title` | template_setting | Clause 5 – Prices, shipping and discounts | approved |  |
| 109 | `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_xKcNPj/content` | template_setting | Prices include VAT, your member price is protected while you stay, and memberships ship free. Price… | approved |  |
| 110 | `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_rnPj6g/nav_label` | template_setting | Payment | approved |  |
| 111 | `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_rnPj6g/title` | template_setting | Clause 6 – Payment methods and security | approved |  |
| 112 | `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_rnPj6g/content` | template_setting | You pay through certified payment providers. We never see or store your full card details. Accepted… | approved |  |
| 113 | `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_EAKJLC/nav_label` | template_setting | Warranty | approved |  |
| 114 | `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_EAKJLC/title` | template_setting | Clause 7 – Legal guarantee of conformity | approved |  |
| 115 | `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_EAKJLC/content` | template_setting | A faulty pump, a defective formula or a broken brush is covered for two years. Using up a formula i… | approved |  |
| 116 | `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_EAKJLC/block_content` | template_setting | Normal product depletion: excluded Example: asking for a replacement because the formula has been u… | approved |  |
| 117 | `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_dGmgBJ/nav_label` | template_setting | Delivery | approved |  |
| 118 | `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_dGmgBJ/title` | template_setting | Clause 8 – Delivery and transfer of risk | approved |  |
| 119 | `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_dGmgBJ/content` | template_setting | Until your parcel is in your hands, it is our responsibility. Transfer of risk (Art. VI.44 WER): th… | approved |  |
| 120 | `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_CDtWCV/nav_label` | template_setting | Memberships | approved |  |
| 121 | `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_CDtWCV/title` | template_setting | Clause 9 – Memberships | approved |  |
| 122 | `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_CDtWCV/content` | template_setting | No lock-in, a protected price and a reminder before every renewal. Gift, pause, skip or stop whenev… | approved |  |
| 123 | `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_nEOBgC/nav_label` | template_setting | Care Credit | approved |  |
| 124 | `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_nEOBgC/title` | template_setting | Clause 10 – Care Credit | approved |  |
| 125 | `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_nEOBgC/content` | template_setting | Members earn Care Credit with every payment and can spend it on any order. It stays valid while you… | approved |  |
| 126 | `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_CXUxDh/nav_label` | template_setting | Dental Check-up Reward | approved |  |
| 127 | `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_CXUxDh/title` | template_setting | Clause 11 – Dental Check-up Reward (Year) | approved |  |
| 128 | `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_CXUxDh/content` | template_setting | Year members who have their oral health checked after six months receive €40 in Care Credit, once p… | approved |  |
| 129 | `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_at3pLy/nav_label` | template_setting | Force majeure | approved |  |
| 130 | `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_at3pLy/title` | template_setting | Clause 12 – Force majeure | approved |  |
| 131 | `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_at3pLy/content` | template_setting | If something truly beyond anyone’s control blocks the contract for more than 30 days, either of us … | approved |  |
| 132 | `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_qyyKHX/nav_label` | template_setting | Intellectual property | approved |  |
| 133 | `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_qyyKHX/title` | template_setting | Clause 13 – Intellectual property | approved |  |
| 134 | `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_qyyKHX/content` | template_setting | The Karmicare name, formulas, designs and content belong to KARMICA BV. All elements of the KARMICA… | approved |  |
| 135 | `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_pjNTAq/nav_label` | template_setting | Reviews and use | approved |  |
| 136 | `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_pjNTAq/title` | template_setting | Clause 14 – Reviews and acceptable use | approved |  |
| 137 | `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_pjNTAq/content` | template_setting | Every review comes from a verified order, and the site is for lawful use only. Review authenticity:… | approved |  |
| 138 | `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_m4qTXH/nav_label` | template_setting | Complaints and law | approved |  |
| 139 | `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_m4qTXH/title` | template_setting | Clause 15 – Complaints, applicable law and courts | approved |  |
| 140 | `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_m4qTXH/content` | template_setting | Write to us first. If we cannot agree, independent mediation is available, and the consumer law of … | approved |  |
| 141 | `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_fz6KEQ/nav_label` | template_setting | Withdrawal form | approved |  |
| 142 | `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_fz6KEQ/title` | template_setting | Annex – Model withdrawal form | approved |  |
| 143 | `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_fz6KEQ/content` | template_setting | Changed your mind about a one-time order? Send us this form, or simply email us a clear statement. … | approved |  |
| 144 | `admin:page:contact:title` | page | Contact | admin-held |  |
| 145 | `admin:page:contact:seo.title` | page | Contact – KARMICARE | admin-held |  |
| 146 | `admin:page:new-consumer-rights:body_html#b001` | page | Date: | admin-held |  |
| 147 | `admin:page:new-consumer-rights:seo.title` | page | New Consumer Rights – KARMICARE | admin-held |  |
| 148 | `admin:page:privacy-policy:seo.title` | page | New Privacy Policy – KARMICARE | admin-held |  |
| 149 | `admin:page:terms-and-conditions-1:body_html#b001` | page | Date: | admin-held |  |
| 150 | `admin:page:terms-and-conditions-1:seo.title` | page | New Terms and Conditions – KARMICARE | admin-held |  |
| 151 | `admin:page:consumer-rights:title` | page | Consumer Rights | admin-held |  |
| 152 | `admin:page:consumer-rights:body_html#b001` | page | Consumer mediation service | admin-held |  |
| 153 | `admin:page:consumer-rights:body_html#b002` | page | European Disputes Committee | admin-held |  |
| 154 | `admin:page:consumer-rights:seo.title` | page | Consumer Rights – KARMICARE | admin-held |  |
| 155 | `admin:page:consumer-rights:seo.description` | page | Consumer mediation service European Disputes Committee | admin-held |  |
| 156 | `admin:page:privacy:title` | page | Privacy Policy | admin-held |  |
| 157 | `admin:page:privacy:body_html#b001` | page | This Privacy Policy is based on article 13 of the General Data Protection Regulation and contains t… | admin-held |  |
| 158 | `admin:page:privacy:body_html#b002` | page | This "Privacy Policy" regulates the processing of your personal data by the data controller: KARMIC… | admin-held |  |
| 159 | `admin:page:privacy:body_html#b003` | page | Article 1 – Collected personal data | admin-held |  |
| 160 | `admin:page:privacy:body_html#b004` | page | 1.1. KARMICARE processes your Personal Data in the context of its activities. This concerns: | admin-held |  |
| 161 | `admin:page:privacy:body_html#b005` | page | Category 1 , based on cookies: your IP address and details about your visit to our Website [to supp… | admin-held |  |
| 162 | `admin:page:privacy:body_html#b006` | page | Category 2 , upon registration or via one of the entry forms on our Website: your surname and first… | admin-held |  |
| 163 | `admin:page:privacy:body_html#b007` | page | Category 3 , if you call or email us: your email address and/or telephone number, as well as the da… | admin-held |  |
| 164 | `admin:page:privacy:body_html#b008` | page | Category 4 , if you subscribe to our newsletter: your email address; | admin-held |  |
| 165 | `admin:page:privacy:body_html#b009` | page | Category 5 , when placing an order: your surname and first name, possibly the name of your company … | admin-held |  |
| 166 | `admin:page:privacy:body_html#b010` | page | 1.2. KARMICARE may collect your Personal Data in various ways: | admin-held |  |
| 167 | `admin:page:privacy:body_html#b011` | page | through your registration and use of our Website; | admin-held |  |
| 168 | `admin:page:privacy:body_html#b012` | page | our Website uses cookies and similar techniques to collect a number of Personal Data. For the provi… | admin-held |  |
| 169 | `admin:page:privacy:body_html#b013` | page | Article 2 – Purposes of the processing of data | admin-held |  |
| 170 | `admin:page:privacy:body_html#b014` | page | 2.1. General purposes: | admin-held |  |
| 171 | `admin:page:privacy:body_html#b015` | page | KARMICARE will use your Personal Data exclusively for: | admin-held |  |
| 172 | `admin:page:privacy:body_html#b016` | page | Category 1 : the maintenance and improvement of our Website and the inclusion of Personal Data in a… | admin-held |  |
| 173 | `admin:page:privacy:body_html#b017` | page | Categories 2 and 3 : being able to answer the question you have asked on the legal basis of your ex… | admin-held |  |
| 174 | `admin:page:privacy:body_html#b018` | page | Categories 2, 3 and 4: direct marketing, newsletters, actions and promotions by KARMICARE, with as … | admin-held |  |
| 175 | `admin:page:privacy:body_html#b019` | page | Category 5 : the delivery and invoicing of products or services ordered by you, with as legal basis… | admin-held |  |
| 176 | `admin:page:privacy:body_html#b020` | page | 2.2. Direct marketing: | admin-held |  |
| 177 | `admin:page:privacy:body_html#b021` | page | We also use your personal data for direct marketing purposes, but only if you give us your explicit… | admin-held |  |
| 178 | `admin:page:privacy:body_html#b022` | page | You can revoke your consent to direct marketing at any time, at no cost and without stating any rea… | admin-held |  |
| 179 | `admin:page:privacy:body_html#b023` | page | Article 3 - How we share your information with third parties – STRIPE captures payment details | admin-held |  |
| 180 | `admin:page:privacy:body_html#b024` | page | We do not transfer your Personal Data to third parties, except with your prior consent. | admin-held |  |
| 181 | `admin:page:privacy:body_html#b025` | page | If we ever cease our activities or transfer them to someone else, for example because we go bankrup… | admin-held |  |
| 182 | `admin:page:privacy:body_html#b026` | page | In exceptional cases, we may be required to disclose Personal Data on the basis of a court order or… | admin-held |  |
| 183 | `admin:page:privacy:body_html#b027` | page | Article 4 – Duration of the processing | admin-held |  |
| 184 | `admin:page:privacy:body_html#b028` | page | We retain your Personal Data as long as necessary in function of the purposes of the processing. | admin-held |  |
| 185 | `admin:page:privacy:body_html#b029` | page | For legal reasons we keep your billing data for at least 7 years after the last invoice date. | admin-held |  |
| 186 | `admin:page:privacy:body_html#b030` | page | Article 5 – Your rights | admin-held |  |
| 187 | `admin:page:privacy:body_html#b031` | page | You have the right to access your Personal Data and the ways in which we use them at any time, free… | admin-held |  |
| 188 | `admin:page:privacy:body_html#b032` | page | You can exercise your rights by e-mail to we@karmicare.com or by post to KARMICA BV, Vizierstraat 2… | admin-held |  |
| 189 | `admin:page:privacy:body_html#b033` | page | You have the right to file a complaint with the Belgian Data Protection Authority: | admin-held |  |
| 190 | `admin:page:privacy:body_html#b034` | page | Drukpersstraat 35, 1000 Brussels Tel : +32 (0)2 274 48 00 contact@apd-gba.be. | admin-held |  |
| 191 | `admin:page:privacy:body_html#b035` | page | If necessary, you can also file a claim for damages before the civil court. | admin-held |  |
| 192 | `admin:page:privacy:body_html#b036` | page | Article 6 – How we secure your personal data | admin-held |  |
| 193 | `admin:page:privacy:body_html#b037` | page | We have taken the appropriate technical and organisational security measures to ensure the safety o… | admin-held |  |
| 194 | `admin:page:privacy:body_html#b038` | page | Article 7 – Cookies | admin-held |  |
| 195 | `admin:page:privacy:body_html#b039` | page | Our Website uses cookies and similar technologies. This helps us to provide you with a better user … | admin-held |  |
| 196 | `admin:page:privacy:body_html#b040` | page | The cookie list below gives you an overview of the cookies that our Website uses. | admin-held |  |
| 197 | `admin:page:privacy:body_html#b041` | page | Cookie list | admin-held |  |
| 198 | `admin:page:privacy:body_html#b042` | page | A cookie is a small text file containing data that a website (when a user visits it) wants to store… | admin-held |  |
| 199 | `admin:page:privacy:body_html#b043` | page | Strictly necessary cookies | admin-held |  |
| 200 | `admin:page:privacy:body_html#b044` | page | These cookies do not store any personally identifiable information, but are necessary for the opera… | admin-held |  |
| 201 | `admin:page:privacy:body_html#b045` | page | Name | admin-held |  |
| 202 | `admin:page:privacy:body_html#b046` | page | Origin | admin-held |  |
| 203 | `admin:page:privacy:body_html#b047` | page | Function | admin-held |  |
| 204 | `admin:page:privacy:body_html#b048` | page | Retention period | admin-held |  |
| 205 | `admin:page:privacy:body_html#b049` | page | __stripe_sid | admin-held |  |
| 206 | `admin:page:privacy:body_html#b050` | page | .stripe.com | admin-held |  |
| 207 | `admin:page:privacy:body_html#b051` | page | 2021-08-11T21:50:32.000Z | admin-held |  |
| 208 | `admin:page:privacy:body_html#b052` | page | site_sid | admin-held |  |
| 209 | `admin:page:privacy:body_html#b053` | page | .stripe.com | admin-held |  |
| 210 | `admin:page:privacy:body_html#b054` | page | 2021-08-11T23:20:32.020Z | admin-held |  |
| 211 | `admin:page:privacy:body_html#b055` | page | merchant | admin-held |  |
| 212 | `admin:page:privacy:body_html#b056` | page | .stripe.com | admin-held |  |
| 213 | `admin:page:privacy:body_html#b057` | page | Session | admin-held |  |
| 214 | `admin:page:privacy:body_html#b058` | page | _gid | admin-held |  |
| 215 | `admin:page:privacy:body_html#b059` | page | .stripe.com | admin-held |  |
| 216 | `admin:page:privacy:body_html#b060` | page | 2021-08-12T21:20:40.000Z | admin-held |  |
| 217 | `admin:page:privacy:body_html#b061` | page | expanded-topics | admin-held |  |
| 218 | `admin:page:privacy:body_html#b062` | page | .stripe.com | admin-held |  |
| 219 | `admin:page:privacy:body_html#b063` | page | 2022-07-09T05:53:50.000Z | admin-held |  |
| 220 | `admin:page:privacy:body_html#b064` | page | 1P_JAR | admin-held |  |
| 221 | `admin:page:privacy:body_html#b065` | page | .gstatic.com | admin-held |  |
| 222 | `admin:page:privacy:body_html#b066` | page | 2021-09-08T06:04:45.308Z | admin-held |  |
| 223 | `admin:page:privacy:body_html#b067` | page | _ga_SEKFWD1C9J | admin-held |  |
| 224 | `admin:page:privacy:body_html#b068` | page | .stripe.com | admin-held |  |
| 225 | `admin:page:privacy:body_html#b069` | page | 2023-06-02T10:00:55.000Z | admin-held |  |
| 226 | `admin:page:privacy:body_html#b070` | page | docs.prefs | admin-held |  |
| 227 | `admin:page:privacy:body_html#b071` | page | .stripe.com | admin-held |  |
| 228 | `admin:page:privacy:body_html#b072` | page | 2022-08-10T21:48:46.000Z | admin-held |  |
| 229 | `admin:page:privacy:body_html#b073` | page | TfXMWj95u2_Zf1Kmv_GCUOjlGG8 | admin-held |  |
| 230 | `admin:page:privacy:body_html#b074` | page | .paypal.com | admin-held |  |
| 231 | `admin:page:privacy:body_html#b075` | page | 2031-04-29T02:39:25.399Z | admin-held |  |
| 232 | `admin:page:privacy:body_html#b076` | page | lang | admin-held |  |
| 233 | `admin:page:privacy:body_html#b077` | page | .stripe.com | admin-held |  |
| 234 | `admin:page:privacy:body_html#b078` | page | 2022-03-31T04:51:09.899Z | admin-held |  |
| 235 | `admin:page:privacy:body_html#b079` | page | __stripe_mid | admin-held |  |
| 236 | `admin:page:privacy:body_html#b080` | page | karmicare.com | admin-held |  |
| 237 | `admin:page:privacy:body_html#b081` | page | 2022-08-11T21:25:37.000Z | admin-held |  |
| 238 | `admin:page:privacy:body_html#b082` | page | _ga | admin-held |  |
| 239 | `admin:page:privacy:body_html#b083` | page | .paypal.com | admin-held |  |
| 240 | `admin:page:privacy:body_html#b084` | page | 2023-08-11T21:14:33.000Z | admin-held |  |
| 241 | `admin:page:privacy:body_html#b085` | page | QSI_SI_1TFFrIy0dgKqN3U_intercept | admin-held |  |
| 242 | `admin:page:privacy:body_html#b086` | page | www.paypal.com | admin-held |  |
| 243 | `admin:page:privacy:body_html#b087` | page | 2021-08-11T22:14:44.000Z | admin-held |  |
| 244 | `admin:page:privacy:body_html#b088` | page | __stripe_mid | admin-held |  |
| 245 | `admin:page:privacy:body_html#b089` | page | .stripe.com | admin-held |  |
| 246 | `admin:page:privacy:body_html#b090` | page | 2022-08-11T21:20:32.000Z | admin-held |  |
| 247 | `admin:page:privacy:body_html#b091` | page | scfc | admin-held |  |
| 248 | `admin:page:privacy:body_html#b092` | page | .stripe.com | admin-held |  |
| 249 | `admin:page:privacy:body_html#b093` | page | 2022-03-24T03:34:14.902Z | admin-held |  |
| 250 | `admin:page:privacy:body_html#b094` | page | locale | admin-held |  |
| 251 | `admin:page:privacy:body_html#b095` | page | .stripe.com | admin-held |  |
| 252 | `admin:page:privacy:body_html#b096` | page | Session | admin-held |  |
| 253 | `admin:page:privacy:body_html#b097` | page | cid | admin-held |  |
| 254 | `admin:page:privacy:body_html#b098` | page | .stripe.com | admin-held |  |
| 255 | `admin:page:privacy:body_html#b099` | page | Session | admin-held |  |
| 256 | `admin:page:privacy:body_html#b100` | page | machine_identifier | admin-held |  |
| 257 | `admin:page:privacy:body_html#b101` | page | .stripe.com | admin-held |  |
| 258 | `admin:page:privacy:body_html#b102` | page | 2026-03-23T21:50:56.330Z | admin-held |  |
| 259 | `admin:page:privacy:body_html#b103` | page | ts | admin-held |  |
| 260 | `admin:page:privacy:body_html#b104` | page | .paypal.com | admin-held |  |
| 261 | `admin:page:privacy:body_html#b105` | page | 2024-08-10T21:25:36.780Z | admin-held |  |
| 262 | `admin:page:privacy:body_html#b106` | page | akavpau_ppsd | admin-held |  |
| 263 | `admin:page:privacy:body_html#b107` | page | .www.paypal.com | admin-held |  |
| 264 | `admin:page:privacy:body_html#b108` | page | Session | admin-held |  |
| 265 | `admin:page:privacy:body_html#b109` | page | ui_experience | admin-held |  |
| 266 | `admin:page:privacy:body_html#b110` | page | .paypal.com | admin-held |  |
| 267 | `admin:page:privacy:body_html#b111` | page | 2023-07-22T12:18:05.799Z | admin-held |  |
| 268 | `admin:page:privacy:body_html#b112` | page | _fbp | admin-held |  |
| 269 | `admin:page:privacy:body_html#b113` | page | .stripe.com | admin-held |  |
| 270 | `admin:page:privacy:body_html#b114` | page | 2021-11-09T21:20:32.000Z | admin-held |  |
| 271 | `admin:page:privacy:body_html#b115` | page | private_machine_identifier | admin-held |  |
| 272 | `admin:page:privacy:body_html#b116` | page | .stripe.com | admin-held |  |
| 273 | `admin:page:privacy:body_html#b117` | page | 2022-03-24T21:50:56.330Z | admin-held |  |
| 274 | `admin:page:privacy:body_html#b118` | page | x-pp-s | admin-held |  |
| 275 | `admin:page:privacy:body_html#b119` | page | .paypal.com | admin-held |  |
| 276 | `admin:page:privacy:body_html#b120` | page | Session | admin-held |  |
| 277 | `admin:page:privacy:body_html#b121` | page | _gid | admin-held |  |
| 278 | `admin:page:privacy:body_html#b122` | page | .paypal.com | admin-held |  |
| 279 | `admin:page:privacy:body_html#b123` | page | 2021-08-12T21:14:33.000Z | admin-held |  |
| 280 | `admin:page:privacy:body_html#b124` | page | cookie_prefs | admin-held |  |
| 281 | `admin:page:privacy:body_html#b125` | page | .paypal.com | admin-held |  |
| 282 | `admin:page:privacy:body_html#b126` | page | 2022-08-11T21:25:36.698Z | admin-held |  |
| 283 | `admin:page:privacy:body_html#b127` | page | disable_cmd_f_override | admin-held |  |
| 284 | `admin:page:privacy:body_html#b128` | page | .stripe.com | admin-held |  |
| 285 | `admin:page:privacy:body_html#b129` | page | 2022-03-30T03:14:24.000Z | admin-held |  |
| 286 | `admin:page:privacy:body_html#b130` | page | navlns | admin-held |  |
| 287 | `admin:page:privacy:body_html#b131` | page | .paypal.com | admin-held |  |
| 288 | `admin:page:privacy:body_html#b132` | page | 2023-08-11T21:14:35.648Z | admin-held |  |
| 289 | `admin:page:privacy:body_html#b133` | page | __stripe_orig_props | admin-held |  |
| 290 | `admin:page:privacy:body_html#b134` | page | .stripe.com | admin-held |  |
| 291 | `admin:page:privacy:body_html#b135` | page | 2022-03-24T03:34:16.902Z | admin-held |  |
| 292 | `admin:page:privacy:body_html#b136` | page | _gcl_au | admin-held |  |
| 293 | `admin:page:privacy:body_html#b137` | page | .stripe.com | admin-held |  |
| 294 | `admin:page:privacy:body_html#b138` | page | 2021-08-22T00:59:09.000Z | admin-held |  |
| 295 | `admin:page:privacy:body_html#b139` | page | tsrce | admin-held |  |
| 296 | `admin:page:privacy:body_html#b140` | page | .paypal.com | admin-held |  |
| 297 | `admin:page:privacy:body_html#b141` | page | 2021-08-14T21:25:36.698Z | admin-held |  |
| 298 | `admin:page:privacy:body_html#b142` | page | navcmd | admin-held |  |
| 299 | `admin:page:privacy:body_html#b143` | page | .paypal.com | admin-held |  |
| 300 | `admin:page:privacy:body_html#b144` | page | Session | admin-held |  |
| 301 | `admin:page:privacy:body_html#b145` | page | user | admin-held |  |
| 302 | `admin:page:privacy:body_html#b146` | page | .stripe.com | admin-held |  |
| 303 | `admin:page:privacy:body_html#b147` | page | Session | admin-held |  |
| 304 | `admin:page:privacy:body_html#b148` | page | _ga | admin-held |  |
| 305 | `admin:page:privacy:body_html#b149` | page | .stripe.com | admin-held |  |
| 306 | `admin:page:privacy:body_html#b150` | page | 2023-08-11T21:20:40.000Z | admin-held |  |
| 307 | `admin:page:privacy:body_html#b151` | page | enforce_policy | admin-held |  |
| 308 | `admin:page:privacy:body_html#b152` | page | .paypal.com | admin-held |  |
| 309 | `admin:page:privacy:body_html#b153` | page | 2022-08-11T21:25:36.698Z | admin-held |  |
| 310 | `admin:page:privacy:body_html#b154` | page | LANG | admin-held |  |
| 311 | `admin:page:privacy:body_html#b155` | page | .paypal.com | admin-held |  |
| 312 | `admin:page:privacy:body_html#b156` | page | 2021-08-12T06:11:31.698Z | admin-held |  |
| 313 | `admin:page:privacy:body_html#b157` | page | site-auth | admin-held |  |
| 314 | `admin:page:privacy:body_html#b158` | page | .stripe.com | admin-held |  |
| 315 | `admin:page:privacy:body_html#b159` | page | Session | admin-held |  |
| 316 | `admin:page:privacy:body_html#b160` | page | id_token | admin-held |  |
| 317 | `admin:page:privacy:body_html#b161` | page | .paypal.com | admin-held |  |
| 318 | `admin:page:privacy:body_html#b162` | page | Session | admin-held |  |
| 319 | `admin:page:privacy:body_html#b163` | page | X-PP-ADS | admin-held |  |
| 320 | `admin:page:privacy:body_html#b164` | page | .paypal.com | admin-held |  |
| 321 | `admin:page:privacy:body_html#b165` | page | 2022-07-22T00:40:34.799Z | admin-held |  |
| 322 | `admin:page:privacy:body_html#b166` | page | SEGM | admin-held |  |
| 323 | `admin:page:privacy:body_html#b167` | page | .paypal.com | admin-held |  |
| 324 | `admin:page:privacy:body_html#b168` | page | Session | admin-held |  |
| 325 | `admin:page:privacy:body_html#b169` | page | DPz73K5mY4nlBaZpzRkjI3ZzAY3QMmrP | admin-held |  |
| 326 | `admin:page:privacy:body_html#b170` | page | .paypal.com | admin-held |  |
| 327 | `admin:page:privacy:body_html#b171` | page | Session | admin-held |  |
| 328 | `admin:page:privacy:body_html#b172` | page | fn_dt | admin-held |  |
| 329 | `admin:page:privacy:body_html#b173` | page | .paypal.com | admin-held |  |
| 330 | `admin:page:privacy:body_html#b174` | page | Session | admin-held |  |
| 331 | `admin:page:privacy:body_html#b175` | page | ts_c | admin-held |  |
| 332 | `admin:page:privacy:body_html#b176` | page | .paypal.com | admin-held |  |
| 333 | `admin:page:privacy:body_html#b177` | page | 2024-08-10T21:25:36.780Z | admin-held |  |
| 334 | `admin:page:privacy:body_html#b178` | page | login_email | admin-held |  |
| 335 | `admin:page:privacy:body_html#b179` | page | .paypal.com | admin-held |  |
| 336 | `admin:page:privacy:body_html#b180` | page | 2023-07-22T12:18:05.799Z | admin-held |  |
| 337 | `admin:page:privacy:body_html#b181` | page | x-csrf-jwt | admin-held |  |
| 338 | `admin:page:privacy:body_html#b182` | page | .paypal.com | admin-held |  |
| 339 | `admin:page:privacy:body_html#b183` | page | 2021-08-18T06:55:00.435Z | admin-held |  |
| 340 | `admin:page:privacy:body_html#b184` | page | -1ILhdyICORs4hS4xTUr41S8iP0 | admin-held |  |
| 341 | `admin:page:privacy:body_html#b185` | page | .paypal.com | admin-held |  |
| 342 | `admin:page:privacy:body_html#b186` | page | 2041-07-13T00:17:40.436Z | admin-held |  |
| 343 | `admin:page:privacy:body_html#b187` | page | cwrClyrK4LoCV1fydGbAxiNL6iG | admin-held |  |
| 344 | `admin:page:privacy:body_html#b188` | page | .paypal.com | admin-held |  |
| 345 | `admin:page:privacy:body_html#b189` | page | Session | admin-held |  |
| 346 | `admin:page:privacy:body_html#b190` | page | x-cdn | admin-held |  |
| 347 | `admin:page:privacy:body_html#b191` | page | .paypal.com | admin-held |  |
| 348 | `admin:page:privacy:body_html#b192` | page | Session | admin-held |  |
| 349 | `admin:page:privacy:body_html#b193` | page | _gcl_au | admin-held |  |
| 350 | `admin:page:privacy:body_html#b194` | page | .paypal.com | admin-held |  |
| 351 | `admin:page:privacy:body_html#b195` | page | 2021-11-09T21:14:33.000Z | admin-held |  |
| 352 | `admin:page:privacy:body_html#b196` | page | recent-views | admin-held |  |
| 353 | `admin:page:privacy:body_html#b197` | page | .stripe.com | admin-held |  |
| 354 | `admin:page:privacy:body_html#b198` | page | 2022-08-11T21:20:32.000Z | admin-held |  |
| 355 | `admin:page:privacy:body_html#b199` | page | session | admin-held |  |
| 356 | `admin:page:privacy:body_html#b200` | page | .stripe.com | admin-held |  |
| 357 | `admin:page:privacy:body_html#b201` | page | 2021-08-17T21:20:37.276Z | admin-held |  |
| 358 | `admin:page:privacy:body_html#b202` | page | jIHSLr4M5Yy4U-3CrkGq73ovwuW | admin-held |  |
| 359 | `admin:page:privacy:body_html#b203` | page | .paypal.com | admin-held |  |
| 360 | `admin:page:privacy:body_html#b204` | page | Session | admin-held |  |
| 361 | `admin:page:privacy:body_html#b205` | page | KHcl0EuY7AKSMgfvHl7J5E7hPtK | admin-held |  |
| 362 | `admin:page:privacy:body_html#b206` | page | .paypal.com | admin-held |  |
| 363 | `admin:page:privacy:body_html#b207` | page | 2041-08-06T21:25:36.769Z | admin-held |  |
| 364 | `admin:page:privacy:body_html#b208` | page | rmuc | admin-held |  |
| 365 | `admin:page:privacy:body_html#b209` | page | .paypal.com | admin-held |  |
| 366 | `admin:page:privacy:body_html#b210` | page | 2031-08-10T21:13:35.831Z | admin-held |  |
| 367 | `admin:page:privacy:body_html#b211` | page | stripe.csrf | admin-held |  |
| 368 | `admin:page:privacy:body_html#b212` | page | .stripe.com | admin-held |  |
| 369 | `admin:page:privacy:body_html#b213` | page | Session | admin-held |  |
| 370 | `admin:page:privacy:body_html#b214` | page | cookie_check | admin-held |  |
| 371 | `admin:page:privacy:body_html#b215` | page | .paypal.com | admin-held |  |
| 372 | `admin:page:privacy:body_html#b216` | page | 2031-03-31T22:15:26.625Z | admin-held |  |
| 373 | `admin:page:privacy:body_html#b217` | page | l7_az | admin-held |  |
| 374 | `admin:page:privacy:body_html#b218` | page | .paypal.com | admin-held |  |
| 375 | `admin:page:privacy:body_html#b219` | page | 2021-08-11T21:50:36.057Z | admin-held |  |
| 376 | `admin:page:privacy:body_html#b220` | page | __stripe_sid | admin-held |  |
| 377 | `admin:page:privacy:body_html#b221` | page | karmicare.com | admin-held |  |
| 378 | `admin:page:privacy:body_html#b222` | page | 2021-08-11T21:55:37.000Z | admin-held |  |
| 379 | `admin:page:privacy:body_html#b223` | page | nsid | admin-held |  |
| 380 | `admin:page:privacy:body_html#b224` | page | www.paypal.com | admin-held |  |
| 381 | `admin:page:privacy:body_html#b225` | page | Session | admin-held |  |
| 382 | `admin:page:privacy:body_html#b226` | page | d_id | admin-held |  |
| 383 | `admin:page:privacy:body_html#b227` | page | .paypal.com | admin-held |  |
| 384 | `admin:page:privacy:body_html#b228` | page | 2031-04-29T02:39:14.096Z | admin-held |  |
| 385 | `admin:page:privacy:body_html#b229` | page | _ga | admin-held |  |
| 386 | `admin:page:privacy:body_html#b230` | page | karmicare.com | admin-held |  |
| 387 | `admin:page:privacy:body_html#b231` | page | 2023-08-10T03:44:35.000Z | admin-held |  |
| 388 | `admin:page:privacy:body_html#b232` | page | Local Storage | admin-held |  |
| 389 | `admin:page:privacy:body_html#b233` | page | Name | admin-held |  |
| 390 | `admin:page:privacy:body_html#b234` | page | Function | admin-held |  |
| 391 | `admin:page:privacy:body_html#b235` | page | _at.cww | admin-held |  |
| 392 | `admin:page:privacy:body_html#b236` | page | at-lojson-cache-ra-5cf78d8da27962eb | admin-held |  |
| 393 | `admin:page:privacy:body_html#b237` | page | __belter_experiment_storage__ | admin-held |  |
| 394 | `admin:page:privacy:body_html#b238` | page | at-rand | admin-held |  |
| 395 | `admin:page:privacy:body_html#b239` | page | _at.hist.0812 | admin-held |  |
| 396 | `admin:page:privacy:body_html#b240` | page | __paypal_storage__ | admin-held |  |
| 397 | `admin:page:privacy:body_html#b241` | page | _hjid | admin-held |  |
| 398 | `admin:page:privacy:body_html#b242` | page | enable_cookies | admin-held |  |
| 399 | `admin:page:privacy:body_html#b243` | page | Used to track whether the user has accepted cookies | admin-held |  |
| 400 | `admin:page:privacy:body_html#b244` | page | Session Storage | admin-held |  |
| 401 | `admin:page:privacy:body_html#b245` | page | Name | admin-held |  |
| 402 | `admin:page:privacy:body_html#b246` | page | Function | admin-held |  |
| 403 | `admin:page:privacy:body_html#b247` | page | cart | admin-held |  |
| 404 | `admin:page:privacy:body_html#b248` | page | Storing the cart data so that it still appears even if the user refreshes the page | admin-held |  |
| 405 | `admin:page:privacy:body_html#b249` | page | currency | admin-held |  |
| 406 | `admin:page:privacy:body_html#b250` | page | Storing the users currency to show shipping info even if the page is refreshed | admin-held |  |
| 407 | `admin:page:privacy:body_html#b251` | page | @@scroll\|/ | admin-held |  |
| 408 | `admin:page:privacy:body_html#b252` | page | Gatsby creates these to watch scroll and page position, multiple are added per session | admin-held |  |
| 409 | `admin:page:privacy:body_html#b253` | page | interval | admin-held |  |
| 410 | `admin:page:privacy:body_html#b254` | page | Used to store the payment interval for the products added to cart | admin-held |  |
| 411 | `admin:page:privacy:body_html#b255` | page | Performance cookies | admin-held |  |
| 412 | `admin:page:privacy:body_html#b256` | page | These cookies enable us to count visitors and their origin so that we can analyse and improve the p… | admin-held |  |
| 413 | `admin:page:privacy:body_html#b257` | page | Functional cookies | admin-held |  |
| 414 | `admin:page:privacy:body_html#b258` | page | These cookies enable our Website to offer additional features and personal settings. They may be se… | admin-held |  |
| 415 | `admin:page:privacy:body_html#b259` | page | Marketing cookies | admin-held |  |
| 416 | `admin:page:privacy:body_html#b260` | page | These cookies can be set by our advertisers on our Website. They may use these cookies to create a … | admin-held |  |
| 417 | `admin:page:privacy:body_html#b261` | page | If you notice that other cookies are placed through our Website, we would appreciate it if you woul… | admin-held |  |
| 418 | `admin:page:privacy:body_html#b262` | page | We will give you as much information as possible about cookies placed by third parties. However, if… | admin-held |  |
| 419 | `admin:page:privacy:body_html#b263` | page | On your first visit to our Website, you will be asked to accept our cookies. You can manage your ch… | admin-held |  |
| 420 | `admin:page:privacy:body_html#b264` | page | If you have any further questions or comments regarding the processing of your Personal Data, pleas… | admin-held |  |
| 421 | `admin:page:privacy:body_html#b265` | page | More information about cookies can also be found at: http://www.allaboutcookies.org/ . | admin-held |  |
| 422 | `admin:page:privacy:body_html#b266` | page | More information about online behavioural advertising and online privacy can be found here: http://… | admin-held |  |
| 423 | `admin:page:privacy:seo.title` | page | Privacy Policy – KARMICARE | admin-held |  |
| 424 | `admin:page:privacy:seo.description` | page | Privacy statement of Karmicare | admin-held |  |
| 425 | `admin:page:terms-and-conditions:title` | page | Terms and Conditions | admin-held |  |
| 426 | `admin:page:terms-and-conditions:body_html#b001` | page | Table of contents | admin-held |  |
| 427 | `admin:page:terms-and-conditions:body_html#b002` | page | Clause 1 – Identity of the vendor Clause 2 – Applicability Clause 3 – Our offer and your order Clau… | admin-held |  |
| 428 | `admin:page:terms-and-conditions:body_html#b003` | page | Clause 1 Identity of the vendor | admin-held |  |
| 429 | `admin:page:terms-and-conditions:body_html#b004` | page | We are: | admin-held |  |
| 430 | `admin:page:terms-and-conditions:body_html#b005` | page | KARMICA BV, trading as KARMICARE, the brand Established at Vizierstraat 28, 8000 Bruges, West-Fland… | admin-held |  |
| 431 | `admin:page:terms-and-conditions:body_html#b006` | page | Company number: 0676.972.896 VAT-number: BE 0676.972.896 Bank account number: BE73 0689 0664 2960 | admin-held |  |
| 432 | `admin:page:terms-and-conditions:body_html#b007` | page | Email address: we@karmicare.com Telephone number: +32478572761 | admin-held |  |
| 433 | `admin:page:terms-and-conditions:body_html#b008` | page | Clause 2 Applicability and conditions | admin-held |  |
| 434 | `admin:page:terms-and-conditions:body_html#b009` | page | Our terms and conditions are applicable to every offer from us as a webshop to you as Consumer (eve… | admin-held |  |
| 435 | `admin:page:terms-and-conditions:body_html#b010` | page | We deliver exclusively in Austria, Belgium, Denmark, France, Germany, Greece, Iceland, Ireland, Ita… | admin-held |  |
| 436 | `admin:page:terms-and-conditions:body_html#b011` | page | To be able to place an order, you must above the age of 18. If you are younger than 18, we ask you … | admin-held |  |
| 437 | `admin:page:terms-and-conditions:body_html#b012` | page | Placing an online order on the website constitutes a formal acceptance of our terms and conditions,… | admin-held |  |
| 438 | `admin:page:terms-and-conditions:body_html#b013` | page | If you ordered online, we provide you in addition and together with the order confirmation or at th… | admin-held |  |
| 439 | `admin:page:terms-and-conditions:body_html#b014` | page | If in addition to these terms and conditions, additional special conditions apply, the above applie… | admin-held |  |
| 440 | `admin:page:terms-and-conditions:body_html#b015` | page | Clause 3 our offer and your order | admin-held |  |
| 441 | `admin:page:terms-and-conditions:body_html#b016` | page | We explicitly state in our offer when the latter is only valid for a constrained period of time or … | admin-held |  |
| 442 | `admin:page:terms-and-conditions:body_html#b017` | page | We always describe as complete and accurate as possible what we sell to you as well as the course o… | admin-held |  |
| 443 | `admin:page:terms-and-conditions:body_html#b018` | page | Your order is complete and the contract between us is final once we confirm your order by mail and … | admin-held |  |
| 444 | `admin:page:terms-and-conditions:body_html#b019` | page | In order to purchase a product, you add it to your shopping basket. Afterwards you submit your cont… | admin-held |  |
| 445 | `admin:page:terms-and-conditions:body_html#b020` | page | Clause 4 Right of withdrawal | admin-held |  |
| 446 | `admin:page:terms-and-conditions:body_html#b021` | page | If you buy goods from us, you have the right to decide that you do not want to keep the goods for 1… | admin-held |  |
| 447 | `admin:page:terms-and-conditions:body_html#b022` | page | The direct costs of the return of the goods will thus be at your expense. We will indicate the cost… | admin-held |  |
| 448 | `admin:page:terms-and-conditions:body_html#b023` | page | We can refuse repayment as long as we have not received the returned goods or until you have shown … | admin-held |  |
| 449 | `admin:page:terms-and-conditions:body_html#b024` | page | We expect you to handle the order as well as the packaging with the utmost care during the first 14… | admin-held |  |
| 450 | `admin:page:terms-and-conditions:body_html#b025` | page | You can return you package through post or courier. | admin-held |  |
| 451 | `admin:page:terms-and-conditions:body_html#b026` | page | In order to exercise your right to withdrawal quickly and correctly, both in case of delivery of se… | admin-held |  |
| 452 | `admin:page:terms-and-conditions:body_html#b027` | page | “MODEL WITHDRAWAL FORM” | admin-held |  |
| 453 | `admin:page:terms-and-conditions:body_html#b028` | page | (Only fill out and sent this form if you wish the withdrawal the agreement) - To [KARMICA BV, Vizie… | admin-held |  |
| 454 | `admin:page:terms-and-conditions:body_html#b029` | page | I/We (*) hereby notice that I/We (*) withdraw from my/our (*) contract of sales of the following go… | admin-held |  |
| 455 | `admin:page:terms-and-conditions:body_html#b030` | page | Ordered on (*)/received on (*), | admin-held |  |
| 456 | `admin:page:terms-and-conditions:body_html#b031` | page | Name of consumer(s), | admin-held |  |
| 457 | `admin:page:terms-and-conditions:body_html#b032` | page | Address of consumer(s), | admin-held |  |
| 458 | `admin:page:terms-and-conditions:body_html#b033` | page | Signature of consumer(s) (only if this form is notified on paper), | admin-held |  |
| 459 | `admin:page:terms-and-conditions:body_html#b034` | page | Date | admin-held |  |
| 460 | `admin:page:terms-and-conditions:body_html#b035` | page | (*) Delete as appropriate. | admin-held |  |
| 461 | `admin:page:terms-and-conditions:body_html#b036` | page | Clause 5 Price | admin-held |  |
| 462 | `admin:page:terms-and-conditions:body_html#b037` | page | During the period we mention in our offer, our prices do not change, except for price changes resul… | admin-held |  |
| 463 | `admin:page:terms-and-conditions:body_html#b038` | page | Our prices include all taxes, VAT and all other levies. Hence, je will never experience unpleasant … | admin-held |  |
| 464 | `admin:page:terms-and-conditions:body_html#b039` | page | Clause 6 Payment | admin-held |  |
| 465 | `admin:page:terms-and-conditions:body_html#b040` | page | We only accept advance payment through our website using the payment methods indicated there. | admin-held |  |
| 466 | `admin:page:terms-and-conditions:body_html#b041` | page | In order to guarantee safe online payment and the safety of your personal data, the transaction dat… | admin-held |  |
| 467 | `admin:page:terms-and-conditions:body_html#b042` | page | Clause 7 Conformity and Warranty | admin-held |  |
| 468 | `admin:page:terms-and-conditions:body_html#b043` | page | We guarantee that our products are in accordance with your order and meet the normal expectations y… | admin-held |  |
| 469 | `admin:page:terms-and-conditions:body_html#b044` | page | As a consumer, you dispose over a statutory 2-year warranty on goods purchased from us if this good… | admin-held |  |
| 470 | `admin:page:terms-and-conditions:body_html#b045` | page | To the extent of what is possible or reasonable, you have a choice between replacement or repair. O… | admin-held |  |
| 471 | `admin:page:terms-and-conditions:body_html#b046` | page | During the first six months, you can in all cases call upon the guarantee. Afterwards you have to p… | admin-held |  |
| 472 | `admin:page:terms-and-conditions:body_html#b047` | page | Clause 8 Delivery and execution | admin-held |  |
| 473 | `admin:page:terms-and-conditions:body_html#b048` | page | All goods and services are delivered to the address provided by you when ordering. | admin-held |  |
| 474 | `admin:page:terms-and-conditions:body_html#b049` | page | When a good is in stock it will be delivered to the delivery address within the peroid mentioned on… | admin-held |  |
| 475 | `admin:page:terms-and-conditions:body_html#b050` | page | Deliveries are made between 8-19 am, Monday through Sunday. | admin-held |  |
| 476 | `admin:page:terms-and-conditions:body_html#b051` | page | The delivery to your country may result in additional custom duty fees. | admin-held |  |
| 477 | `admin:page:terms-and-conditions:body_html#b052` | page | If we are not able to deliver on time, we will always notify you before the to the end of the deliv… | admin-held |  |
| 478 | `admin:page:terms-and-conditions:body_html#b053` | page | The shipment of goods and gift vouchers is always at our risk. So you do not have to worry about go… | admin-held |  |
| 479 | `admin:page:terms-and-conditions:body_html#b054` | page | If the delivered goods were damaged during transport, do not correspond to the goods mentioned on t… | admin-held |  |
| 480 | `admin:page:terms-and-conditions:body_html#b055` | page | We cannot be held responsible for any consequential damage suffered due to late delivery or non-del… | admin-held |  |
| 481 | `admin:page:terms-and-conditions:body_html#b056` | page | Clause 9 Duration | admin-held |  |
| 482 | `admin:page:terms-and-conditions:body_html#b057` | page | The Consumer has the right to terminate a contract of indefinite duration at any time, with due obs… | admin-held |  |
| 483 | `admin:page:terms-and-conditions:body_html#b058` | page | A contract which was entered into for a definite period of time has a duration of maximum two years. | admin-held |  |
| 484 | `admin:page:terms-and-conditions:body_html#b059` | page | If a sale of goods contract for a definite period of time stipulates that in the case of non-action… | admin-held |  |
| 485 | `admin:page:terms-and-conditions:body_html#b060` | page | If a contract for the provision of services for a definite period of time was concluded between the… | admin-held |  |
| 486 | `admin:page:terms-and-conditions:body_html#b061` | page | This clause will contain the consequences of a tacit renewal, among which are the provision of the … | admin-held |  |
| 487 | `admin:page:terms-and-conditions:body_html#b062` | page | Clause 10 Force majeure | admin-held |  |
| 488 | `admin:page:terms-and-conditions:body_html#b063` | page | In case of force majeure, we are not obliged to fulfil our obligations. In that case we may either … | admin-held |  |
| 489 | `admin:page:terms-and-conditions:body_html#b064` | page | Events of force majeure are all circumstances external to our will and control that render the resp… | admin-held |  |
| 490 | `admin:page:terms-and-conditions:body_html#b065` | page | Clause 11 Intellectual property | admin-held |  |
| 491 | `admin:page:terms-and-conditions:body_html#b066` | page | Our website, logos, texts, photographs, names, and in general all our communications are protected … | admin-held |  |
| 492 | `admin:page:terms-and-conditions:body_html#b067` | page | It is forbidden to use and/or change any of the intellectual property rights as described in the pr… | admin-held |  |
| 493 | `admin:page:terms-and-conditions:body_html#b068` | page | Clause 12. Complaints procedure and conflicts | admin-held |  |
| 494 | `admin:page:terms-and-conditions:body_html#b069` | page | We do hope that all our customers are always 100% satisfied. If nevertheless you would have complai… | admin-held |  |
| 495 | `admin:page:terms-and-conditions:body_html#b070` | page | All contracts we conclude with our customers are, regardless of their place of residence, exclusive… | admin-held |  |
| 496 | `admin:page:terms-and-conditions:body_html#b071` | page | In case of out of court commercial dispute settlements, the consumer ombudsman of the FPS economy i… | admin-held |  |
| 497 | `admin:page:terms-and-conditions:body_html#b072` | page | In case of a cross-border dispute you can make use of the Online Dispute Resolution platform of the… | admin-held |  |
| 498 | `admin:page:terms-and-conditions:body_html#b073` | page | If we do not manage to reach agreement through our personal complaints department on we@karmicare.c… | admin-held |  |
| 499 | `admin:page:terms-and-conditions:seo.title` | page | Terms and Conditions – KARMICARE | admin-held |  |
| 500 | `admin:page:terms-and-conditions:seo.description` | page | General terms & conditions | admin-held |  |
| 501 | `admin:policy:privacy-policy:title` | policy | Privacy policy | admin-held |  |
| 502 | `admin:policy:privacy-policy:body#b001` | policy | How we collect, use and protect your personal data, and how you stay in control of it. | admin-held |  |
| 503 | `admin:policy:privacy-policy:body#b002` | policy | KARMICA BV, trading as KARMICARE · Vizierstraat 28, 8000 Bruges, Belgium · VAT BE 0676.972.896 · RP… | admin-held |  |
| 504 | `admin:policy:privacy-policy:body#b003` | policy | care@karmicare.com · Last updated October 2026 | admin-held |  |
| 505 | `admin:policy:privacy-policy:body#b004` | policy | 1. Introduction and scope | admin-held |  |
| 506 | `admin:policy:privacy-policy:body#b005` | policy | This policy explains what we collect about you, why we need it, who helps us process it, and how yo… | admin-held |  |
| 507 | `admin:policy:privacy-policy:body#b006` | policy | KARMICA BV (“KARMICARE”, “we”, “us” or “our”) respects your fundamental right to privacy and is com… | admin-held |  |
| 508 | `admin:policy:privacy-policy:body#b007` | policy | The General Data Protection Regulation (EU) 2016/679 (“GDPR”); | admin-held |  |
| 509 | `admin:policy:privacy-policy:body#b008` | policy | The Belgian Data Protection Act of 30 July 2018 ; | admin-held |  |
| 510 | `admin:policy:privacy-policy:body#b009` | policy | The Belgian Electronic Communications Act of 13 June 2005 , transposing the ePrivacy Directive 2002… | admin-held |  |
| 511 | `admin:policy:privacy-policy:body#b010` | policy | This policy explains how we collect, process, store, disclose and safeguard your personal data when… | admin-held |  |
| 512 | `admin:policy:privacy-policy:body#b011` | policy | 2. Data controller | admin-held |  |
| 513 | `admin:policy:privacy-policy:body#b012` | policy | KARMICA BV in Bruges is responsible for your personal data. Every privacy question goes to one addr… | admin-held |  |
| 514 | `admin:policy:privacy-policy:body#b013` | policy | The data controller responsible for the processing of your personal data is: | admin-held |  |
| 515 | `admin:policy:privacy-policy:body#b014` | policy | KARMICA BV , Vizierstraat 28, 8000 Bruges, Belgium · Company and VAT number BE 0676.972.896 · Regis… | admin-held |  |
| 516 | `admin:policy:privacy-policy:body#b015` | policy | For all questions, privacy requests or to exercise your rights under the GDPR, write to our Data Pr… | admin-held |  |
| 517 | `admin:policy:privacy-policy:body#b016` | policy | 3. Personal data we process | admin-held |  |
| 518 | `admin:policy:privacy-policy:body#b017` | policy | We collect what we need to deliver your order, run your membership and answer your questions. Oral-… | admin-held |  |
| 519 | `admin:policy:privacy-policy:body#b018` | policy | Depending on how you interact with KARMICARE, we process the following categories of personal data: | admin-held |  |
| 520 | `admin:policy:privacy-policy:body#b019` | policy | Identification and contact data: first name, last name, billing and delivery address, email address… | admin-held |  |
| 521 | `admin:policy:privacy-policy:body#b020` | policy | Transaction and order data: what you ordered, your membership (Awake and Asleep frequency, interval… | admin-held |  |
| 522 | `admin:policy:privacy-policy:body#b021` | policy | Account and membership data: customer portal login, delivery schedule preferences, pauses and skipp… | admin-held |  |
| 523 | `admin:policy:privacy-policy:body#b022` | policy | Care Credit data: your Care Credit balance, the credit you earn and spend, and your reward status. | admin-held |  |
| 524 | `admin:policy:privacy-policy:body#b023` | policy | Check-up data (Year members, only with your explicit consent): your answers to the starting and fol… | admin-held |  |
| 525 | `admin:policy:privacy-policy:body#b024` | policy | Communication data: records of your messages by email or contact form, including product questions,… | admin-held |  |
| 526 | `admin:policy:privacy-policy:body#b025` | policy | Marketing and newsletter data: email address, first name, communication preferences, newsletter sta… | admin-held |  |
| 527 | `admin:policy:privacy-policy:body#b026` | policy | Technical, navigation and cookie data: IP address (anonymised where applicable), browser and versio… | admin-held |  |
| 528 | `admin:policy:privacy-policy:body#b027` | policy | Your questionnaire answers about your oral health are health data , a special category of personal … | admin-held |  |
| 529 | `admin:policy:privacy-policy:body#b028` | policy | 4. Purposes and legal bases | admin-held |  |
| 530 | `admin:policy:privacy-policy:body#b029` | policy | Every use of your data rests on a legal basis: your contract, a legal duty, a legitimate interest o… | admin-held |  |
| 531 | `admin:policy:privacy-policy:body#b030` | policy | Under Articles 6 and 9 GDPR, we only process your personal data when a valid legal basis exists: | admin-held |  |
| 532 | `admin:policy:privacy-policy:body#b031` | policy | Order processing and fulfilment | admin-held |  |
| 533 | `admin:policy:privacy-policy:body#b032` | policy | Processing orders, delivering, sending order updates and managing returns. | admin-held |  |
| 534 | `admin:policy:privacy-policy:body#b033` | policy | Data: identification, contact, transaction, order | admin-held |  |
| 535 | `admin:policy:privacy-policy:body#b034` | policy | Legal basis: performance of a contract (Art. 6(1)(b) GDPR) | admin-held |  |
| 536 | `admin:policy:privacy-policy:body#b035` | policy | Membership management | admin-held |  |
| 537 | `admin:policy:privacy-policy:body#b036` | policy | Managing your deliveries, renewals, pauses and reminders, and providing the customer portal. | admin-held |  |
| 538 | `admin:policy:privacy-policy:body#b037` | policy | Data: account, membership, transaction, contact | admin-held |  |
| 539 | `admin:policy:privacy-policy:body#b038` | policy | Legal basis: performance of a contract (Art. 6(1)(b) GDPR) | admin-held |  |
| 540 | `admin:policy:privacy-policy:body#b039` | policy | Care Credit | admin-held |  |
| 541 | `admin:policy:privacy-policy:body#b040` | policy | Granting, showing and redeeming Care Credit, and reversing it after refunds. | admin-held |  |
| 542 | `admin:policy:privacy-policy:body#b041` | policy | Data: account, transaction, Care Credit | admin-held |  |
| 543 | `admin:policy:privacy-policy:body#b042` | policy | Legal basis: performance of a contract (Art. 6(1)(b) GDPR) | admin-held |  |
| 544 | `admin:policy:privacy-policy:body#b043` | policy | Payment processing and fraud prevention | admin-held |  |
| 545 | `admin:policy:privacy-policy:body#b044` | policy | Authenticating transactions, managing chargebacks and preventing payment fraud. | admin-held |  |
| 546 | `admin:policy:privacy-policy:body#b045` | policy | Data: transaction, identification, technical | admin-held |  |
| 547 | `admin:policy:privacy-policy:body#b046` | policy | Legal basis: performance of a contract (Art. 6(1)(b)) and legitimate interest in fraud prevention (… | admin-held |  |
| 548 | `admin:policy:privacy-policy:body#b047` | policy | Customer care | admin-held |  |
| 549 | `admin:policy:privacy-policy:body#b048` | policy | Handling questions, complaints, refund requests and legal guarantee claims. | admin-held |  |
| 550 | `admin:policy:privacy-policy:body#b049` | policy | Data: contact, communication, order | admin-held |  |
| 551 | `admin:policy:privacy-policy:body#b050` | policy | Legal basis: performance of a contract (Art. 6(1)(b)) and legitimate interest in efficient customer… | admin-held |  |
| 552 | `admin:policy:privacy-policy:body#b051` | policy | Dental Check-up Reward and oral-health follow-up | admin-held |  |
| 553 | `admin:policy:privacy-policy:body#b052` | policy | Checking eligibility for the €40 Dental Check-up Reward and following up your oral health over time. | admin-held |  |
| 554 | `admin:policy:privacy-policy:body#b053` | policy | Data: questionnaire answers (health data), visit proof, account | admin-held |  |
| 555 | `admin:policy:privacy-policy:body#b054` | policy | Legal basis: your explicit consent (Art. 9(2)(a) and Art. 6(1)(a) GDPR), which you can withdraw at … | admin-held |  |
| 556 | `admin:policy:privacy-policy:body#b055` | policy | Legal and tax obligations | admin-held |  |
| 557 | `admin:policy:privacy-policy:body#b056` | policy | Bookkeeping, invoicing, VAT compliance, product liability and regulatory reporting. | admin-held |  |
| 558 | `admin:policy:privacy-policy:body#b057` | policy | Data: identification, transaction, invoicing | admin-held |  |
| 559 | `admin:policy:privacy-policy:body#b058` | policy | Legal basis: legal obligation (Art. 6(1)(c) GDPR; Belgian Code of Economic Law and Income Tax Code) | admin-held |  |
| 560 | `admin:policy:privacy-policy:body#b059` | policy | Direct marketing to existing customers | admin-held |  |
| 561 | `admin:policy:privacy-policy:body#b060` | policy | Relevant updates and recommendations about similar KARMICARE products. | admin-held |  |
| 562 | `admin:policy:privacy-policy:body#b061` | policy | Data: contact, order history | admin-held |  |
| 563 | `admin:policy:privacy-policy:body#b062` | policy | Legal basis: legitimate interest (Art. 6(1)(f) GDPR and Art. XII.13 WER, “soft opt-in”), with an op… | admin-held |  |
| 564 | `admin:policy:privacy-policy:body#b063` | policy | Newsletter and promotional campaigns | admin-held |  |
| 565 | `admin:policy:privacy-policy:body#b064` | policy | Newsletters and promotional offers to prospects. | admin-held |  |
| 566 | `admin:policy:privacy-policy:body#b065` | policy | Data: contact, first name, marketing data | admin-held |  |
| 567 | `admin:policy:privacy-policy:body#b066` | policy | Legal basis: explicit prior consent (Art. 6(1)(a) GDPR) | admin-held |  |
| 568 | `admin:policy:privacy-policy:body#b067` | policy | Website performance and analytics | admin-held |  |
| 569 | `admin:policy:privacy-policy:body#b068` | policy | Aggregated traffic analysis, conversion tracking, site optimisation and debugging. | admin-held |  |
| 570 | `admin:policy:privacy-policy:body#b069` | policy | Data: technical, navigation, analytics cookies | admin-held |  |
| 571 | `admin:policy:privacy-policy:body#b070` | policy | Legal basis: explicit prior consent (Art. 6(1)(a) GDPR and ePrivacy Directive) | admin-held |  |
| 572 | `admin:policy:privacy-policy:body#b071` | policy | Targeted advertising and retargeting | admin-held |  |
| 573 | `admin:policy:privacy-policy:body#b072` | policy | Measuring ad performance, audience segmentation and relevant social ads. | admin-held |  |
| 574 | `admin:policy:privacy-policy:body#b073` | policy | Data: marketing cookies, pixel data | admin-held |  |
| 575 | `admin:policy:privacy-policy:body#b074` | policy | Legal basis: explicit prior consent (Art. 6(1)(a) GDPR and ePrivacy Directive) | admin-held |  |
| 576 | `admin:policy:privacy-policy:body#b075` | policy | 5. Service providers and recipients | admin-held |  |
| 577 | `admin:policy:privacy-policy:body#b076` | policy | We never sell your data. A small set of service providers helps us run the shop, each under a writt… | admin-held |  |
| 578 | `admin:policy:privacy-policy:body#b077` | policy | We never sell, rent or lease your personal data to data brokers or unrelated third parties. We shar… | admin-held |  |
| 579 | `admin:policy:privacy-policy:body#b078` | policy | E-commerce and hosting: Shopify Inc. (Canada / US), e-commerce engine, checkout and order managemen… | admin-held |  |
| 580 | `admin:policy:privacy-policy:body#b079` | policy | Payments: Stripe Payments Europe, Ltd. (Ireland / US), card, Apple Pay, Google Pay, Bancontact and … | admin-held |  |
| 581 | `admin:policy:privacy-policy:body#b080` | policy | Email and marketing automation: Klaviyo, Inc. (US), transactional and promotional email, cart remin… | admin-held |  |
| 582 | `admin:policy:privacy-policy:body#b081` | policy | Logistics: fulfilment warehouses and carriers (for example Bpost, DHL Express, PostNL and national … | admin-held |  |
| 583 | `admin:policy:privacy-policy:body#b082` | policy | Analytics and optimisation: Google Ireland Limited (Google Analytics 4), web metrics · Meta Platfor… | admin-held |  |
| 584 | `admin:policy:privacy-policy:body#b083` | policy | Authorities: tax authorities (FPS Finance), customs (EORI BE0676972896), courts or law enforcement,… | admin-held |  |
| 585 | `admin:policy:privacy-policy:body#b084` | policy | 6. International data transfers | admin-held |  |
| 586 | `admin:policy:privacy-policy:body#b085` | policy | When your data leaves the European Economic Area, it travels under an EU-approved safeguard. | admin-held |  |
| 587 | `admin:policy:privacy-policy:body#b086` | policy | When personal data is transferred outside the European Economic Area (EEA), in particular to the Un… | admin-held |  |
| 588 | `admin:policy:privacy-policy:body#b087` | policy | Adequacy decisions: transfers to countries the European Commission recognises as adequate, such as … | admin-held |  |
| 589 | `admin:policy:privacy-policy:body#b088` | policy | EU-U.S. Data Privacy Framework (DPF): where US providers (such as Shopify, Google, Meta, Klaviyo, S… | admin-held |  |
| 590 | `admin:policy:privacy-policy:body#b089` | policy | Standard Contractual Clauses (SCCs): where providers are not DPF-certified, transfers follow the Co… | admin-held |  |
| 591 | `admin:policy:privacy-policy:body#b090` | policy | You can ask for a copy of the relevant safeguards at care@karmicare.com . | admin-held |  |
| 592 | `admin:policy:privacy-policy:body#b091` | policy | 7. How long we keep your data | admin-held |  |
| 593 | `admin:policy:privacy-policy:body#b092` | policy | We keep your data only as long as the purpose or the law requires, then delete or anonymise it. | admin-held |  |
| 594 | `admin:policy:privacy-policy:body#b093` | policy | We store personal data only as long as necessary for the purpose it was collected for, or to meet l… | admin-held |  |
| 595 | `admin:policy:privacy-policy:body#b094` | policy | Order, invoicing and accounting records: kept for 7 years after the end of the financial year (Art.… | admin-held |  |
| 596 | `admin:policy:privacy-policy:body#b095` | policy | Membership and Care Credit records: kept while your membership is active, then 7 years after it end… | admin-held |  |
| 597 | `admin:policy:privacy-policy:body#b096` | policy | Check-up questionnaires and visit proof: proof of your dental visit is deleted 60 days after we hav… | admin-held |  |
| 598 | `admin:policy:privacy-policy:body#b097` | policy | Customer care messages: kept for 2 years after resolution, to handle legal guarantee claims and dis… | admin-held |  |
| 599 | `admin:policy:privacy-policy:body#b098` | policy | Newsletter and marketing data: kept until you withdraw consent or unsubscribe. After 24 months of i… | admin-held |  |
| 600 | `admin:policy:privacy-policy:body#b099` | policy | Analytics and cookie data: kept for at most 13 months , then deleted or permanently anonymised. | admin-held |  |
| 601 | `admin:policy:privacy-policy:body#b100` | policy | 8. Your rights under the GDPR | admin-held |  |
| 602 | `admin:policy:privacy-policy:body#b101` | policy | You can see, correct, delete, move or limit your data, and object to marketing at any time. We answ… | admin-held |  |
| 603 | `admin:policy:privacy-policy:body#b102` | policy | As a data subject, you have the following rights: | admin-held |  |
| 604 | `admin:policy:privacy-policy:body#b103` | policy | Access (Art. 15): ask whether we process your data and receive a free copy of it. | admin-held |  |
| 605 | `admin:policy:privacy-policy:body#b104` | policy | Rectification (Art. 16): have inaccurate data corrected or incomplete data completed. | admin-held |  |
| 606 | `admin:policy:privacy-policy:body#b105` | policy | Erasure (Art. 17): have your data deleted when it is no longer needed, when you withdraw consent or… | admin-held |  |
| 607 | `admin:policy:privacy-policy:body#b106` | policy | Restriction (Art. 18): have processing frozen while the accuracy or lawfulness of the data is conte… | admin-held |  |
| 608 | `admin:policy:privacy-policy:body#b107` | policy | Portability (Art. 20): receive your data in a structured, machine-readable format (JSON, CSV) and h… | admin-held |  |
| 609 | `admin:policy:privacy-policy:body#b108` | policy | Objection (Art. 21): object at any time, without giving a reason, to direct marketing, and object t… | admin-held |  |
| 610 | `admin:policy:privacy-policy:body#b109` | policy | Withdrawing consent (Art. 7(3)): withdraw consent for newsletters, marketing cookies or the check-u… | admin-held |  |
| 611 | `admin:policy:privacy-policy:body#b110` | policy | No automated decisions (Art. 22): KARMICARE does not use automated decision-making or profiling tha… | admin-held |  |
| 612 | `admin:policy:privacy-policy:body#b111` | policy | How to exercise your rights | admin-held |  |
| 613 | `admin:policy:privacy-policy:body#b112` | policy | Email care@karmicare.com or write to KARMICA BV — Privacy Operations , Vizierstraat 28, 8000 Bruges… | admin-held |  |
| 614 | `admin:policy:privacy-policy:body#b113` | policy | We respond without undue delay and at the latest within one month of receipt. Where necessary, give… | admin-held |  |
| 615 | `admin:policy:privacy-policy:body#b114` | policy | Your right to complain | admin-held |  |
| 616 | `admin:policy:privacy-policy:body#b115` | policy | If you believe our processing breaks data protection law, you can lodge a complaint with the Belgia… | admin-held |  |
| 617 | `admin:policy:privacy-policy:body#b116` | policy | Belgian Data Protection Authority (Gegevensbeschermingsautoriteit / Autorité de protection des donn… | admin-held |  |
| 618 | `admin:policy:privacy-policy:body#b117` | policy | 9. Cookies and tracking | admin-held |  |
| 619 | `admin:policy:privacy-policy:body#b118` | policy | Essential cookies keep the shop working. Everything else waits for your consent, and you can change… | admin-held |  |
| 620 | `admin:policy:privacy-policy:body#b119` | policy | Our website uses cookies and similar technologies (local storage, session tokens, pixel tags) to ma… | admin-held |  |
| 621 | `admin:policy:privacy-policy:body#b120` | policy | 9.1 Cookie categories | admin-held |  |
| 622 | `admin:policy:privacy-policy:body#b121` | policy | Strictly necessary: core operation of the shop, security, sessions, cart and checkout. These need n… | admin-held |  |
| 623 | `admin:policy:privacy-policy:body#b122` | policy | Functional: remember your language (en, nl, fr), country and Day/Night preference. | admin-held |  |
| 624 | `admin:policy:privacy-policy:body#b123` | policy | Performance and analytics: measure traffic, referrers and site performance (for example Google Anal… | admin-held |  |
| 625 | `admin:policy:privacy-policy:body#b124` | policy | Marketing and advertising: set by advertising partners (for example Meta Pixel, TriplePixel, Klaviy… | admin-held |  |
| 626 | `admin:policy:privacy-policy:body#b125` | policy | 9.2 Your consent choices | admin-held |  |
| 627 | `admin:policy:privacy-policy:body#b126` | policy | On your first visit, our consent banner lets you accept all cookies, decline all non-essential cook… | admin-held |  |
| 628 | `admin:policy:privacy-policy:body#b127` | policy | No non-essential cookies or tracking scripts run before you opt in. You can change or withdraw your… | admin-held |  |
| 629 | `admin:policy:privacy-policy:body#b128` | policy | 10. Data security | admin-held |  |
| 630 | `admin:policy:privacy-policy:body#b129` | policy | Your data travels encrypted, and only the people who need it can reach it. | admin-held |  |
| 631 | `admin:policy:privacy-policy:body#b130` | policy | KARMICA BV uses technical and organisational measures to protect personal data against accidental l… | admin-held |  |
| 632 | `admin:policy:privacy-policy:body#b131` | policy | TLS encryption for all web traffic and data transfers; | admin-held |  |
| 633 | `admin:policy:privacy-policy:body#b132` | policy | role-based access controls and multi-factor authentication (MFA) for administrative systems; | admin-held |  |
| 634 | `admin:policy:privacy-policy:body#b133` | policy | anonymisation and pseudonymisation of analytics data; | admin-held |  |
| 635 | `admin:policy:privacy-policy:body#b134` | policy | regular system audits, automatic security patching and vulnerability management; | admin-held |  |
| 636 | `admin:policy:privacy-policy:body#b135` | policy | data processing agreements with every sub-processor, requiring confidentiality and GDPR compliance. | admin-held |  |
| 637 | `admin:policy:privacy-policy:body#b136` | policy | 11. Changes to this policy | admin-held |  |
| 638 | `admin:policy:privacy-policy:body#b137` | policy | When this policy changes, the date at the top changes too, and we tell you first about anything imp… | admin-held |  |
| 639 | `admin:policy:privacy-policy:body#b138` | policy | We may update this policy to reflect changes in how we work, new formulas or new law. The “Last upd… | admin-held |  |
| 640 | `admin:policy:privacy-policy:body#b139` | policy | Questions about your data? Write to care@karmicare.com . A person reads every message. | admin-held |  |
| 641 | `admin:policy:privacy-policy:seo.title` | policy | Privacy policy – KARMICARE | admin-held |  |
| 642 | `admin:policy:terms-of-service:title` | policy | Terms of service | admin-held |  |
| 643 | `admin:policy:terms-of-service:body#b001` | policy | The terms that apply to every order and plan on karmicare.com, including your rights to withdraw, r… | admin-held |  |
| 644 | `admin:policy:terms-of-service:body#b002` | policy | KARMICA BV, trading as KARMICARE · Vizierstraat 28, 8000 Bruges, Belgium · VAT BE 0676.972.896 · EO… | admin-held |  |
| 645 | `admin:policy:terms-of-service:body#b003` | policy | care@karmicare.com · Last updated October 2026 | admin-held |  |
| 646 | `admin:policy:terms-of-service:body#b004` | policy | Clause 1 – Identity of the vendor | admin-held |  |
| 647 | `admin:policy:terms-of-service:body#b005` | policy | You buy from KARMICA BV, a Belgian company in Bruges. | admin-held |  |
| 648 | `admin:policy:terms-of-service:body#b006` | policy | The webshop karmicare.com and its checkout subdomains are operated by: | admin-held |  |
| 649 | `admin:policy:terms-of-service:body#b007` | policy | KARMICA BV (trading as KARMICARE ), Vizierstraat 28, 8000 Bruges, Belgium · Enterprise number (KBO/… | admin-held |  |
| 650 | `admin:policy:terms-of-service:body#b008` | policy | Clause 2 – Applicability and international scope | admin-held |  |
| 651 | `admin:policy:terms-of-service:body#b009` | policy | These terms apply to every order and membership you place on karmicare.com. | admin-held |  |
| 652 | `admin:policy:terms-of-service:body#b010` | policy | These General Terms and Conditions (“Terms”) apply to all offers, orders, contracts of sale and mem… | admin-held |  |
| 653 | `admin:policy:terms-of-service:body#b011` | policy | A “Consumer” is any natural person acting for purposes outside their trade, business, craft or prof… | admin-held |  |
| 654 | `admin:policy:terms-of-service:body#b012` | policy | Territorial scope: we deliver to consumers in the member states of the European Union. We do not de… | admin-held |  |
| 655 | `admin:policy:terms-of-service:body#b013` | policy | Non-discrimination and geo-blocking (Regulation (EU) 2018/302): we do not apply discriminatory cond… | admin-held |  |
| 656 | `admin:policy:terms-of-service:body#b014` | policy | Age: by placing an order, you confirm that you are at least 18 years old or have the consent of a p… | admin-held |  |
| 657 | `admin:policy:terms-of-service:body#b015` | policy | Access to these Terms: these Terms are always available at karmicare.com/en/pages/terms-and-conditi… | admin-held |  |
| 658 | `admin:policy:terms-of-service:body#b016` | policy | Clause 3 – Product classification, offers and contract formation | admin-held |  |
| 659 | `admin:policy:terms-of-service:body#b017` | policy | Awake and Asleep are cosmetics, not medicines. Your order becomes a contract once we confirm it by … | admin-held |  |
| 660 | `admin:policy:terms-of-service:body#b018` | policy | EU cosmetic status: KARMICARE products (including our oral care systems, personal hygiene formulati… | admin-held |  |
| 661 | `admin:policy:terms-of-service:body#b019` | policy | Offers: product descriptions, formulations and illustrations on our website are presented as precis… | admin-held |  |
| 662 | `admin:policy:terms-of-service:body#b020` | policy | Contract formation: selecting products and completing checkout is an offer to buy. As Belgian and E… | admin-held |  |
| 663 | `admin:policy:terms-of-service:body#b021` | policy | Clause 4 – Withdrawal, money-back guarantees and refunds | admin-held |  |
| 664 | `admin:policy:terms-of-service:body#b022` | policy | Every first order comes with a money-back guarantee: 14 days on Try Once, your first cycle on the 6… | admin-held |  |
| 665 | `admin:policy:terms-of-service:body#b023` | policy | 4.1 Statutory right of withdrawal (14 days) | admin-held |  |
| 666 | `admin:policy:terms-of-service:body#b024` | policy | 14-day withdrawal period: you may withdraw from a contract concluded online without giving a reason… | admin-held |  |
| 667 | `admin:policy:terms-of-service:body#b025` | policy | Reimbursement: we reimburse all payments received from you, including standard delivery charges, wi… | admin-held |  |
| 668 | `admin:policy:terms-of-service:body#b026` | policy | Same payment method: we reimburse via the same payment method you used. We never substitute a vouch… | admin-held |  |
| 669 | `admin:policy:terms-of-service:body#b027` | policy | Relation to our guarantees: the money-back guarantees in clauses 4.2 to 4.5 are voluntary commercia… | admin-held |  |
| 670 | `admin:policy:terms-of-service:body#b028` | policy | 4.2 Try Once: 14-day money-back guarantee | admin-held |  |
| 671 | `admin:policy:terms-of-service:body#b029` | policy | Period: 14 calendar days from delivery. | admin-held |  |
| 672 | `admin:policy:terms-of-service:body#b030` | policy | Opened formulas qualify: you may open and try the duo and keep it. No return is required. | admin-held |  |
| 673 | `admin:policy:terms-of-service:body#b031` | policy | Refund: everything you paid for the order, including the shipping charge, within 14 days of approva… | admin-held |  |
| 674 | `admin:policy:terms-of-service:body#b032` | policy | 4.3 60-Day rhythm: money-back guarantee for your first cycle | admin-held |  |
| 675 | `admin:policy:terms-of-service:body#b033` | policy | Scope: the guarantee applies to new members and covers the first 60-day cycle only. | admin-held |  |
| 676 | `admin:policy:terms-of-service:body#b034` | policy | Deadline: your request must reach us before your first renewal is charged (60 days after your order… | admin-held |  |
| 677 | `admin:policy:terms-of-service:body#b035` | policy | Refund: your first membership payment, minus any Care Credit you already spent that was earned from… | admin-held |  |
| 678 | `admin:policy:terms-of-service:body#b036` | policy | What you keep: the duo and the Welcome Kit. Nothing has to be returned. Your membership ends and no… | admin-held |  |
| 679 | `admin:policy:terms-of-service:body#b037` | policy | 4.4 Year: 60-day money-back guarantee | admin-held |  |
| 680 | `admin:policy:terms-of-service:body#b038` | policy | Deadline: within 60 calendar days of your first delivery . | admin-held |  |
| 681 | `admin:policy:terms-of-service:body#b039` | policy | Refund: your annual payment, minus any Care Credit you already spent that was earned from that paym… | admin-held |  |
| 682 | `admin:policy:terms-of-service:body#b040` | policy | Return: you keep the opened duo and the Welcome Kit. The other duos come back unopened (pump never … | admin-held |  |
| 683 | `admin:policy:terms-of-service:body#b041` | policy | Deductions: for each additional duo that comes back opened, or does not come back, €59 is deducted … | admin-held |  |
| 684 | `admin:policy:terms-of-service:body#b042` | policy | Lost return parcels: we carry the transport risk of our prepaid label. The refund is paid once the … | admin-held |  |
| 685 | `admin:policy:terms-of-service:body#b043` | policy | Timing: the refund follows within 14 days of receiving and inspecting the returned duos, to your or… | admin-held |  |
| 686 | `admin:policy:terms-of-service:body#b044` | policy | 4.5 One money-back guarantee per customer | admin-held |  |
| 687 | `admin:policy:terms-of-service:body#b045` | policy | Each customer is entitled to one money-back guarantee in total, whichever option they start with (T… | admin-held |  |
| 688 | `admin:policy:terms-of-service:body#b046` | policy | 4.6 Packaging notice: airless pump and first-use priming | admin-held |  |
| 689 | `admin:policy:terms-of-service:body#b047` | policy | Hermetic airless packaging: where KARMICARE formulas come in airless packaging, the pump creates a … | admin-held |  |
| 690 | `admin:policy:terms-of-service:body#b048` | policy | Unprimed factory state and priming: the pumps are not pre-pumped. On first use, press the pump head… | admin-held |  |
| 691 | `admin:policy:terms-of-service:body#b049` | policy | Sealed delivery and opened formulas: Awake and Asleep are delivered sealed. The pump is unprimed an… | admin-held |  |
| 692 | `admin:policy:terms-of-service:body#b050` | policy | 4.7 How to request a refund or return | admin-held |  |
| 693 | `admin:policy:terms-of-service:body#b051` | policy | Email care@karmicare.com, or call +32 (0) 478 57 27 61, with your order number and the option you c… | admin-held |  |
| 694 | `admin:policy:terms-of-service:body#b052` | policy | For a statutory withdrawal of a one-time order, we send you a return authorisation and the warehous… | admin-held |  |
| 695 | `admin:policy:terms-of-service:body#b053` | policy | All refunds are issued without deductions or administrative fees other than those set out in clause… | admin-held |  |
| 696 | `admin:policy:terms-of-service:body#b054` | policy | Orders paid partly with Care Credit: the money paid goes back to your original payment method and t… | admin-held |  |
| 697 | `admin:policy:terms-of-service:body#b055` | policy | Clause 5 – Prices, shipping and discounts | admin-held |  |
| 698 | `admin:policy:terms-of-service:body#b056` | policy | Prices include VAT, your member price is protected while you stay, and memberships ship free. | admin-held |  |
| 699 | `admin:policy:terms-of-service:body#b057` | policy | Prices: prices are shown on our website and at checkout. For deliveries within the European Union, … | admin-held |  |
| 700 | `admin:policy:terms-of-service:body#b058` | policy | Member price protection: the price of your membership stays the same for as long as your membership… | admin-held |  |
| 701 | `admin:policy:terms-of-service:body#b059` | policy | Personal offers: we may make you a personal offer, such as a member price, by email or in your acco… | admin-held |  |
| 702 | `admin:policy:terms-of-service:body#b060` | policy | Shipping charges: memberships ship free within the European Union. For Try Once, the shipping charg… | admin-held |  |
| 703 | `admin:policy:terms-of-service:body#b061` | policy | Price reductions (Omnibus Directive): under Article VI.19/1 WER, when we advertise a price reductio… | admin-held |  |
| 704 | `admin:policy:terms-of-service:body#b062` | policy | Clause 6 – Payment methods and security | admin-held |  |
| 705 | `admin:policy:terms-of-service:body#b063` | policy | You pay through certified payment providers. We never see or store your full card details. | admin-held |  |
| 706 | `admin:policy:terms-of-service:body#b064` | policy | Accepted methods: Bancontact / Payconiq, iDEAL, credit and debit cards (Visa, Mastercard, American … | admin-held |  |
| 707 | `admin:policy:terms-of-service:body#b065` | policy | Security and encryption: payments are encrypted with TLS and processed by PCI-DSS Level 1 certified… | admin-held |  |
| 708 | `admin:policy:terms-of-service:body#b066` | policy | Strong customer authentication: under the revised Payment Services Directive (PSD2), online card pa… | admin-held |  |
| 709 | `admin:policy:terms-of-service:body#b067` | policy | Clause 7 – Legal guarantee of conformity | admin-held |  |
| 710 | `admin:policy:terms-of-service:body#b068` | policy | A faulty pump, a defective formula or a broken brush is covered for two years. Using up a formula i… | admin-held |  |
| 711 | `admin:policy:terms-of-service:body#b069` | policy | Legal framework: European consumers have a legal guarantee of conformity under Articles 1649bis to … | admin-held |  |
| 712 | `admin:policy:terms-of-service:body#b070` | policy | Consumable oral care (nature of the goods): under Article 1649quater, §4 of the Belgian Civil Code … | admin-held |  |
| 713 | `admin:policy:terms-of-service:body#b071` | policy | What is covered: latent manufacturing defects and mechanical non-conformities present at or arising… | admin-held |  |
| 714 | `admin:policy:terms-of-service:body#b072` | policy | Remedies: for a verified manufacturing or packaging defect, KARMICARE provides a free replacement o… | admin-held |  |
| 715 | `admin:policy:terms-of-service:body#b073` | policy | Notification: tell us within two months of discovering a lack of conformity (Art. 1649quater, §2 Be… | admin-held |  |
| 716 | `admin:policy:terms-of-service:body#b074` | policy | Exclusions: normal depletion of the formula; natural wear of toothbrush bristles; damage from impro… | admin-held |  |
| 717 | `admin:policy:terms-of-service:body#b075` | policy | Examples | admin-held |  |
| 718 | `admin:policy:terms-of-service:body#b076` | policy | Normal product depletion: excluded | admin-held |  |
| 719 | `admin:policy:terms-of-service:body#b077` | policy | Example: asking for a replacement because the formula has been used up. | admin-held |  |
| 720 | `admin:policy:terms-of-service:body#b078` | policy | Why: consumable cosmetics are designed to be used up; normal exhaustion fulfils the contract. | admin-held |  |
| 721 | `admin:policy:terms-of-service:body#b079` | policy | Normal bristle wear: excluded | admin-held |  |
| 722 | `admin:policy:terms-of-service:body#b080` | policy | Example: bristles splaying or softening after 2–3 months of daily brushing. | admin-held |  |
| 723 | `admin:policy:terms-of-service:body#b081` | policy | Why: routine wear and tear; dentists recommend replacing a toothbrush every 2–3 months. | admin-held |  |
| 724 | `admin:policy:terms-of-service:body#b082` | policy | Expired Period After Opening (PAO): excluded | admin-held |  |
| 725 | `admin:policy:terms-of-service:body#b083` | policy | Example: a bottle opened 18 months ago dries out. | admin-held |  |
| 726 | `admin:policy:terms-of-service:body#b084` | policy | Why: stability is certified only within the indicated PAO. | admin-held |  |
| 727 | `admin:policy:terms-of-service:body#b085` | policy | Improper storage: excluded | admin-held |  |
| 728 | `admin:policy:terms-of-service:body#b086` | policy | Example: a bottle left on a radiator or in a hot car separates. | admin-held |  |
| 729 | `admin:policy:terms-of-service:body#b087` | policy | Why: heat damage caused by storage against the storage guidelines. | admin-held |  |
| 730 | `admin:policy:terms-of-service:body#b088` | policy | Airless pump failure: covered | admin-held |  |
| 731 | `admin:policy:terms-of-service:body#b089` | policy | Example: the piston jams or the head breaks in week 2 under normal use while formula remains inside. | admin-held |  |
| 732 | `admin:policy:terms-of-service:body#b090` | policy | Remedy: free replacement unit. | admin-held |  |
| 733 | `admin:policy:terms-of-service:body#b091` | policy | Formulation or batch defect: covered | admin-held |  |
| 734 | `admin:policy:terms-of-service:body#b092` | policy | Example: curdled, separated or discoloured formula on first use. | admin-held |  |
| 735 | `admin:policy:terms-of-service:body#b093` | policy | Remedy: free replacement or full refund. | admin-held |  |
| 736 | `admin:policy:terms-of-service:body#b094` | policy | Unopened stock within shelf life: covered | admin-held |  |
| 737 | `admin:policy:terms-of-service:body#b095` | policy | Example: a properly stored, unopened plan bottle goes bad before its printed expiry date. | admin-held |  |
| 738 | `admin:policy:terms-of-service:body#b096` | policy | Remedy: replacement. | admin-held |  |
| 739 | `admin:policy:terms-of-service:body#b097` | policy | Structural toothbrush or floss defect: covered | admin-held |  |
| 740 | `admin:policy:terms-of-service:body#b098` | policy | Example: a handle snaps on day 4 or bristles shed on first use. | admin-held |  |
| 741 | `admin:policy:terms-of-service:body#b099` | policy | Remedy: replacement. | admin-held |  |
| 742 | `admin:policy:terms-of-service:body#b100` | policy | Clause 8 – Delivery and transfer of risk | admin-held |  |
| 743 | `admin:policy:terms-of-service:body#b101` | policy | Until your parcel is in your hands, it is our responsibility. | admin-held |  |
| 744 | `admin:policy:terms-of-service:body#b102` | policy | Transfer of risk (Art. VI.44 WER): the risk of loss, theft or damage in transit stays with KARMICA … | admin-held |  |
| 745 | `admin:policy:terms-of-service:body#b103` | policy | Delivery area: we deliver to addresses in the member states of the European Union. Please make sure… | admin-held |  |
| 746 | `admin:policy:terms-of-service:body#b104` | policy | Delivery times (estimates): Belgium, the Netherlands and Luxembourg: within 24 hours; rest of the E… | admin-held |  |
| 747 | `admin:policy:terms-of-service:body#b105` | policy | Delays: unless another date was agreed, we deliver within 30 days of the contract. If we do not, yo… | admin-held |  |
| 748 | `admin:policy:terms-of-service:body#b106` | policy | Clause 9 – Memberships | admin-held |  |
| 749 | `admin:policy:terms-of-service:body#b107` | policy | No lock-in, a protected price and a reminder before every renewal. Gift, pause, skip or stop whenev… | admin-held |  |
| 750 | `admin:policy:terms-of-service:body#b108` | policy | The options: Try Once is a single duo without renewal. The 60-Day rhythm delivers one duo and renew… | admin-held |  |
| 751 | `admin:policy:terms-of-service:body#b109` | policy | Authorisation: when you start a membership, you authorise KARMICARE (through our payment processor,… | admin-held |  |
| 752 | `admin:policy:terms-of-service:body#b110` | policy | Welcome Kit: your first membership order includes a Welcome Kit with a morning toothbrush, an eveni… | admin-held |  |
| 753 | `admin:policy:terms-of-service:body#b111` | policy | Renewal reminder: we email you at least 5 days before every 60-Day rhythm renewal, and 30 days and … | admin-held |  |
| 754 | `admin:policy:terms-of-service:body#b112` | policy | Pausing: you can pause for up to 60 days at a time, and for up to 60 days in total within any 12 mo… | admin-held |  |
| 755 | `admin:policy:terms-of-service:body#b113` | policy | Cancelling: you can cancel at any time in your customer portal or by email. Cancelling stops your n… | admin-held |  |
| 756 | `admin:policy:terms-of-service:body#b114` | policy | End of your membership: your membership ends when the last period you paid for runs out. | admin-held |  |
| 757 | `admin:policy:terms-of-service:body#b115` | policy | Switching plans: to move from the 60-Day rhythm to the Year, cancel your 60-Day rhythm and start a … | admin-held |  |
| 758 | `admin:policy:terms-of-service:body#b116` | policy | Renewal orders and ending a renewed Year: renewal orders are dispatched two working days after the … | admin-held |  |
| 759 | `admin:policy:terms-of-service:body#b117` | policy | Gifting: you can send a delivery as a gift to another address in the European Union from your custo… | admin-held |  |
| 760 | `admin:policy:terms-of-service:body#b118` | policy | Clause 10 – Care Credit | admin-held |  |
| 761 | `admin:policy:terms-of-service:body#b119` | policy | Members earn Care Credit with every payment and can spend it on any order. It stays valid while you… | admin-held |  |
| 762 | `admin:policy:terms-of-service:body#b120` | policy | Earning: you earn Care Credit worth 10% of each 60-Day rhythm payment and 20% of each Year payment.… | admin-held |  |
| 763 | `admin:policy:terms-of-service:body#b121` | policy | Other Care Credit: Year members can earn the Dental Check-up Reward as Care Credit (clause 11), and… | admin-held |  |
| 764 | `admin:policy:terms-of-service:body#b122` | policy | Spending: you can apply Care Credit to any product, including membership orders. It is deducted fro… | admin-held |  |
| 765 | `admin:policy:terms-of-service:body#b123` | policy | No cash value: Care Credit is never paid out in cash and cannot be transferred. | admin-held |  |
| 766 | `admin:policy:terms-of-service:body#b124` | policy | Validity: Care Credit stays valid while your membership continues and for 12 months after it ends (… | admin-held |  |
| 767 | `admin:policy:terms-of-service:body#b125` | policy | Refunds: if an order is refunded, the Care Credit you used on it returns to your balance; Care Cred… | admin-held |  |
| 768 | `admin:policy:terms-of-service:body#b126` | policy | Clause 11 – Dental Check-up Reward (Year) | admin-held |  |
| 769 | `admin:policy:terms-of-service:body#b127` | policy | Year members who have their oral health checked after six months receive €40 in Care Credit, once p… | admin-held |  |
| 770 | `admin:policy:terms-of-service:body#b128` | policy | Who: members of the Year, in any EU member state. | admin-held |  |
| 771 | `admin:policy:terms-of-service:body#b129` | policy | When: for a dental visit from six months after your first delivery until your membership anniversar… | admin-held |  |
| 772 | `admin:policy:terms-of-service:body#b130` | policy | What we need: proof of the visit (an appointment confirmation or invoice) and the follow-up questio… | admin-held |  |
| 773 | `admin:policy:terms-of-service:body#b131` | policy | Reward: €40 in Care Credit, once per membership year. | admin-held |  |
| 774 | `admin:policy:terms-of-service:body#b132` | policy | Clause 12 – Force majeure | admin-held |  |
| 775 | `admin:policy:terms-of-service:body#b133` | policy | If something truly beyond anyone’s control blocks the contract for more than 30 days, either of us … | admin-held |  |
| 776 | `admin:policy:terms-of-service:body#b134` | policy | Neither party is liable for delay or failure caused by force majeure (Article 5.226 of the Belgian … | admin-held |  |
| 777 | `admin:policy:terms-of-service:body#b135` | policy | During force majeure, our obligations are suspended. If it lasts more than 30 consecutive days , ei… | admin-held |  |
| 778 | `admin:policy:terms-of-service:body#b136` | policy | Clause 13 – Intellectual property | admin-held |  |
| 779 | `admin:policy:terms-of-service:body#b137` | policy | The Karmicare name, formulas, designs and content belong to KARMICA BV. | admin-held |  |
| 780 | `admin:policy:terms-of-service:body#b138` | policy | All elements of the KARMICARE brand, website and range, including the name “KARMICARE”, trademarks,… | admin-held |  |
| 781 | `admin:policy:terms-of-service:body#b139` | policy | Any reproduction, distribution, imitation, commercial use, decompilation or reverse engineering of … | admin-held |  |
| 782 | `admin:policy:terms-of-service:body#b140` | policy | Clause 14 – Reviews and acceptable use | admin-held |  |
| 783 | `admin:policy:terms-of-service:body#b141` | policy | Every review comes from a verified order, and the site is for lawful use only. | admin-held |  |
| 784 | `admin:policy:terms-of-service:body#b142` | policy | Review authenticity: reviews published on karmicare.com are collected only from verified purchasers… | admin-held |  |
| 785 | `admin:policy:terms-of-service:body#b143` | policy | Acceptable use: you agree to use our website and customer portal only for lawful purposes and in li… | admin-held |  |
| 786 | `admin:policy:terms-of-service:body#b144` | policy | Clause 15 – Complaints, applicable law and courts | admin-held |  |
| 787 | `admin:policy:terms-of-service:body#b145` | policy | Write to us first. If we cannot agree, independent mediation is available, and the consumer law of … | admin-held |  |
| 788 | `admin:policy:terms-of-service:body#b146` | policy | Complaints: for questions, feedback or complaints, write to our customer care at care@karmicare.com… | admin-held |  |
| 789 | `admin:policy:terms-of-service:body#b147` | policy | Out-of-court dispute resolution: if we cannot reach an amicable solution, European consumers can tu… | admin-held |  |
| 790 | `admin:policy:terms-of-service:body#b148` | policy | Applicable law: all agreements between KARMICA BV and its customers are governed by Belgian law . U… | admin-held |  |
| 791 | `admin:policy:terms-of-service:body#b149` | policy | Competent courts: for consumers domiciled in the European Union, the jurisdiction rules of the Brus… | admin-held |  |
| 792 | `admin:policy:terms-of-service:body#b150` | policy | The EU Online Dispute Resolution (ODR) platform closed on 20 July 2025, so it is no longer a route … | admin-held |  |
| 793 | `admin:policy:terms-of-service:body#b151` | policy | Annex – Model withdrawal form | admin-held |  |
| 794 | `admin:policy:terms-of-service:body#b152` | policy | Changed your mind about a one-time order? Send us this form, or simply email us a clear statement. … | admin-held |  |
| 795 | `admin:policy:terms-of-service:body#b153` | policy | Complete and return this form only if you wish to withdraw from an eligible, unopened contract. | admin-held |  |
| 796 | `admin:policy:terms-of-service:body#b154` | policy | To: KARMICA BV (trading as KARMICARE), Vizierstraat 28, 8000 Bruges, Belgium, care@karmicare.com, +… | admin-held |  |
| 797 | `admin:policy:terms-of-service:body#b155` | policy | I/We (*) hereby give notice that I/We (*) withdraw from my/our (*) contract of sale of the followin… | admin-held |  |
| 798 | `admin:policy:terms-of-service:body#b156` | policy | Product name(s): | admin-held |  |
| 799 | `admin:policy:terms-of-service:body#b157` | policy | Ordered on (*) / Received on (*): | admin-held |  |
| 800 | `admin:policy:terms-of-service:body#b158` | policy | Order reference number: | admin-held |  |
| 801 | `admin:policy:terms-of-service:body#b159` | policy | Name of consumer(s): | admin-held |  |
| 802 | `admin:policy:terms-of-service:body#b160` | policy | Address of consumer(s): | admin-held |  |
| 803 | `admin:policy:terms-of-service:body#b161` | policy | Signature of consumer(s), only if this form is sent on paper: | admin-held |  |
| 804 | `admin:policy:terms-of-service:body#b162` | policy | Date: | admin-held |  |
| 805 | `admin:policy:terms-of-service:body#b163` | policy | (*) Delete as appropriate. | admin-held |  |
| 806 | `admin:policy:terms-of-service:body#b164` | policy | Download the form (PDF) | admin-held |  |
| 807 | `admin:policy:terms-of-service:body#b165` | policy | Questions about these terms? Write to care@karmicare.com . A person reads every message. | admin-held |  |
| 808 | `admin:policy:terms-of-service:seo.title` | policy | Terms of service – KARMICARE | admin-held |  |
| 809 | `admin:policy:refund-policy:title` | policy | Refund policy | admin-held |  |
| 810 | `admin:policy:refund-policy:body#b001` | policy | Your rights under Belgian and EU law, together with the promises Karmicare adds on top. | admin-held |  |
| 811 | `admin:policy:refund-policy:body#b002` | policy | KARMICA BV, trading as KARMICARE · Vizierstraat 28, 8000 Bruges, Belgium · VAT BE 0676.972.896 · EO… | admin-held |  |
| 812 | `admin:policy:refund-policy:body#b003` | policy | care@karmicare.com · Last updated October 2026 | admin-held |  |
| 813 | `admin:policy:refund-policy:body#b004` | policy | 14 days | admin-held |  |
| 814 | `admin:policy:refund-policy:body#b005` | policy | To change your mind | admin-held |  |
| 815 | `admin:policy:refund-policy:body#b006` | policy | Legal right, plus Try Once money-back | admin-held |  |
| 816 | `admin:policy:refund-policy:body#b007` | policy | 60 days | admin-held |  |
| 817 | `admin:policy:refund-policy:body#b008` | policy | Money-back guarantee | admin-held |  |
| 818 | `admin:policy:refund-policy:body#b009` | policy | Karmicare promise · memberships | admin-held |  |
| 819 | `admin:policy:refund-policy:body#b010` | policy | 14 days | admin-held |  |
| 820 | `admin:policy:refund-policy:body#b011` | policy | To receive your refund | admin-held |  |
| 821 | `admin:policy:refund-policy:body#b012` | policy | After approval · same payment method | admin-held |  |
| 822 | `admin:policy:refund-policy:body#b013` | policy | 2 years | admin-held |  |
| 823 | `admin:policy:refund-policy:body#b014` | policy | Legal guarantee | admin-held |  |
| 824 | `admin:policy:refund-policy:body#b015` | policy | Legal right · every order | admin-held |  |
| 825 | `admin:policy:refund-policy:body#b016` | policy | 1. Our commitment to trust and transparency | admin-held |  |
| 826 | `admin:policy:refund-policy:body#b017` | policy | Your rights come from the law, not from our goodwill. This page sets them out in one place, alongsi… | admin-held |  |
| 827 | `admin:policy:refund-policy:body#b018` | policy | At KARMICARE, we believe in radical transparency, both in the biological formulations we craft and … | admin-held |  |
| 828 | `admin:policy:refund-policy:body#b019` | policy | The Belgian Code of Economic Law (WER/CDE), notably Book VI on market practices and consumer protec… | admin-held |  |
| 829 | `admin:policy:refund-policy:body#b020` | policy | The EU Consumer Rights Directive (2011/83/EU); | admin-held |  |
| 830 | `admin:policy:refund-policy:body#b021` | policy | The EU Omnibus Directive (2019/2161) on modernised consumer protection rules; | admin-held |  |
| 831 | `admin:policy:refund-policy:body#b022` | policy | The EU Sale of Goods Directive (2019/771), transposed into Belgian law by the Law of 20 March 2022; | admin-held |  |
| 832 | `admin:policy:refund-policy:body#b023` | policy | The EU Cosmetics Regulation (EC) No 1223/2009. | admin-held |  |
| 833 | `admin:policy:refund-policy:body#b024` | policy | Whether you try a single duo or become a member, your legal rights are fully protected. | admin-held |  |
| 834 | `admin:policy:refund-policy:body#b025` | policy | 2. EU cosmetic safety and standards | admin-held |  |
| 835 | `admin:policy:refund-policy:body#b026` | policy | Awake and Asleep are notified EU cosmetics, made under Good Manufacturing Practice and assessed by … | admin-held |  |
| 836 | `admin:policy:refund-policy:body#b027` | policy | All KARMICARE products, including Awake Morning Toothpaste, Asleep Evening Toothpaste, Charcoal Flo… | admin-held |  |
| 837 | `admin:policy:refund-policy:body#b028` | policy | Formulated and manufactured in accordance with European Good Manufacturing Practices (GMP / ISO 227… | admin-held |  |
| 838 | `admin:policy:refund-policy:body#b029` | policy | Registered and notified on the European Cosmetic Product Notification Portal (CPNP) in compliance w… | admin-held |  |
| 839 | `admin:policy:refund-policy:body#b030` | policy | Subject to a Cosmetic Product Safety Report (CPSR) signed by a qualified European safety assessor; | admin-held |  |
| 840 | `admin:policy:refund-policy:body#b031` | policy | 100% free of SLS, parabens, artificial dyes, endocrine disruptors and controversial abrasives. | admin-held |  |
| 841 | `admin:policy:refund-policy:body#b032` | policy | Regulatory classification: KARMICARE oral care products are cosmetics intended for daily oral hygie… | admin-held |  |
| 842 | `admin:policy:refund-policy:body#b033` | policy | 3. Refunds, withdrawal and money-back guarantees | admin-held |  |
| 843 | `admin:policy:refund-policy:body#b034` | policy | Every first order comes with a money-back guarantee: 14 days on Try Once, your first cycle on the 6… | admin-held |  |
| 844 | `admin:policy:refund-policy:body#b035` | policy | 3.1 Your legal right to withdraw (14 days) | admin-held |  |
| 845 | `admin:policy:refund-policy:body#b036` | policy | You can withdraw from an online order within 14 calendar days of delivery, without giving a reason … | admin-held |  |
| 846 | `admin:policy:refund-policy:body#b037` | policy | We reimburse all payments received from you, including standard delivery charges, within 14 calenda… | admin-held |  |
| 847 | `admin:policy:refund-policy:body#b038` | policy | This right comes from the law. Our money-back guarantees below come on top of it and never limit it. | admin-held |  |
| 848 | `admin:policy:refund-policy:body#b039` | policy | 3.2 Try Once: 14-day money-back guarantee | admin-held |  |
| 849 | `admin:policy:refund-policy:body#b040` | policy | Not convinced? Tell us within 14 days of delivery and we refund everything you paid, including ship… | admin-held |  |
| 850 | `admin:policy:refund-policy:body#b041` | policy | You may open and try the duo, and keep it. Nothing has to be sent back. | admin-held |  |
| 851 | `admin:policy:refund-policy:body#b042` | policy | 3.3 60-Day rhythm: your first cycle | admin-held |  |
| 852 | `admin:policy:refund-policy:body#b043` | policy | The guarantee covers your first 60-day cycle . Tell us before your first renewal (60 days after you… | admin-held |  |
| 853 | `admin:policy:refund-policy:body#b044` | policy | Care Credit you already spent from that payment is deducted; unused credit from it is removed. | admin-held |  |
| 854 | `admin:policy:refund-policy:body#b045` | policy | You keep the duo and the Welcome Kit. Your membership ends and nothing renews. | admin-held |  |
| 855 | `admin:policy:refund-policy:body#b046` | policy | We remind you 5 days before your first renewal. Continuing into your second cycle ends the guarante… | admin-held |  |
| 856 | `admin:policy:refund-policy:body#b047` | policy | 3.4 Year: 60 days from your first delivery | admin-held |  |
| 857 | `admin:policy:refund-policy:body#b048` | policy | Tell us within 60 days of your first delivery and we refund your annual payment, minus any Care Cre… | admin-held |  |
| 858 | `admin:policy:refund-policy:body#b049` | policy | You keep the opened duo and the Welcome Kit. Send the other duos back unopened (pump never primed) … | admin-held |  |
| 859 | `admin:policy:refund-policy:body#b050` | policy | For each extra duo that comes back opened, or does not come back, €59 is deducted. If the return pa… | admin-held |  |
| 860 | `admin:policy:refund-policy:body#b051` | policy | 3.5 One money-back guarantee per customer | admin-held |  |
| 861 | `admin:policy:refund-policy:body#b052` | policy | Each customer has one money-back guarantee, whichever option you start with. Switching to another p… | admin-held |  |
| 862 | `admin:policy:refund-policy:body#b053` | policy | 3.6 How refunds work | admin-held |  |
| 863 | `admin:policy:refund-policy:body#b054` | policy | Email care@karmicare.com, or call +32 (0) 478 57 27 61, with your order number. | admin-held |  |
| 864 | `admin:policy:refund-policy:body#b055` | policy | We refund within 14 days of approving your request or, for a Year refund, of receiving your returne… | admin-held |  |
| 865 | `admin:policy:refund-policy:body#b056` | policy | If you paid partly with Care Credit, that credit returns to your balance. Care Credit is never paid… | admin-held |  |
| 866 | `admin:policy:refund-policy:body#b057` | policy | To withdraw from a one-time order under your legal right, we send you a return authorisation and th… | admin-held |  |
| 867 | `admin:policy:refund-policy:body#b058` | policy | 3.7 Packaging notice: airless pump and first-use priming | admin-held |  |
| 868 | `admin:policy:refund-policy:body#b059` | policy | Hermetic airless protection. Our formulas are housed in hygienic airless pump dispensers that shiel… | admin-held |  |
| 869 | `admin:policy:refund-policy:body#b060` | policy | First-use priming (3 to 10 pumps). Our pumps are not pre-pumped. On first use, press the pump head … | admin-held |  |
| 870 | `admin:policy:refund-policy:body#b061` | policy | Sealed delivery: the unprimed pump is the seal. Priming it opens the formula, and an opened formula… | admin-held |  |
| 871 | `admin:policy:refund-policy:body#b062` | policy | 4. Two-year legal guarantee of conformity | admin-held |  |
| 872 | `admin:policy:refund-policy:body#b063` | policy | If something is faulty, you are covered for two years from delivery, and the law assumes the fault … | admin-held |  |
| 873 | `admin:policy:refund-policy:body#b064` | policy | Under Belgian law (Article 1649bis and following of the Civil Code and Book VI WER, implementing Di… | admin-held |  |
| 874 | `admin:policy:refund-policy:body#b065` | policy | 4.1 Two-year presumption of conformity | admin-held |  |
| 875 | `admin:policy:refund-policy:body#b066` | policy | If a delivered item is defective, non-conforming or damaged on delivery, you are protected for two … | admin-held |  |
| 876 | `admin:policy:refund-policy:body#b067` | policy | Any defect that appears within those two years is presumed to have existed at the time of delivery … | admin-held |  |
| 877 | `admin:policy:refund-policy:body#b068` | policy | 4.2 Your remedies | admin-held |  |
| 878 | `admin:policy:refund-policy:body#b069` | policy | Free replacement or repair. You choose between a free replacement and a repair, provided the remedy… | admin-held |  |
| 879 | `admin:policy:refund-policy:body#b070` | policy | Price reduction or ending the contract. If replacement is impossible, or cannot be carried out with… | admin-held |  |
| 880 | `admin:policy:refund-policy:body#b071` | policy | 4.3 Telling us about a defect | admin-held |  |
| 881 | `admin:policy:refund-policy:body#b072` | policy | Let us know within two months of discovering a defect (Article 1649quater, §2 of the Belgian Civil … | admin-held |  |
| 882 | `admin:policy:refund-policy:body#b073` | policy | 5. Delivery and risk in transit | admin-held |  |
| 883 | `admin:policy:refund-policy:body#b074` | policy | Until your parcel is in your hands, it is our responsibility. | admin-held |  |
| 884 | `admin:policy:refund-policy:body#b075` | policy | Where we deliver: to every member state of the European Union. | admin-held |  |
| 885 | `admin:policy:refund-policy:body#b076` | policy | Shipping: memberships ship free. For Try Once, the shipping charge for your zone is shown at checko… | admin-held |  |
| 886 | `admin:policy:refund-policy:body#b077` | policy | Risk in transit (Art. VI.44 WER). The risk of loss, damage or theft in transit stays with KARMICARE… | admin-held |  |
| 887 | `admin:policy:refund-policy:body#b078` | policy | Delayed deliveries. Unless we agreed another date, we deliver within 30 days. If we do not, you can… | admin-held |  |
| 888 | `admin:policy:refund-policy:body#b079` | policy | Delivery times (estimates) | admin-held |  |
| 889 | `admin:policy:refund-policy:body#b080` | policy | Belgium, the Netherlands and Luxembourg: within 24 hours | admin-held |  |
| 890 | `admin:policy:refund-policy:body#b081` | policy | Rest of the European Union: 2–3 working days | admin-held |  |
| 891 | `admin:policy:refund-policy:body#b082` | policy | 6. Your membership: renewals, pauses and cancelling | admin-held |  |
| 892 | `admin:policy:refund-policy:body#b083` | policy | No lock-in. Your member price stays the same, we remind you before every renewal, and you can gift,… | admin-held |  |
| 893 | `admin:policy:refund-policy:body#b084` | policy | Billing: the 60-Day rhythm renews every 60 days. The Year renews once a year on its anniversary, wi… | admin-held |  |
| 894 | `admin:policy:refund-policy:body#b085` | policy | Renewal reminder: we email you 5 days before every 60-Day rhythm renewal, and 30 days and 7 days be… | admin-held |  |
| 895 | `admin:policy:refund-policy:body#b086` | policy | Pausing: pause for up to 60 days at a time, and for up to 60 days in total within any 12 months. On… | admin-held |  |
| 896 | `admin:policy:refund-policy:body#b087` | policy | Cancelling: cancel at any time in your customer portal . Cancelling stops your next renewal; it is … | admin-held |  |
| 897 | `admin:policy:refund-policy:body#b088` | policy | Renewals: renewal orders are dispatched two working days after the charge; cancel before dispatch a… | admin-held |  |
| 898 | `admin:policy:refund-policy:body#b089` | policy | Gifting: send a delivery as a gift to another address in the EU from your customer portal. Your mem… | admin-held |  |
| 899 | `admin:policy:refund-policy:body#b090` | policy | Price protection: your member price stays the same for as long as you stay a member, also during a … | admin-held |  |
| 900 | `admin:policy:refund-policy:body#b091` | policy | Care Credit: members earn 10% (60-Day rhythm) or 20% (Year) of every membership payment as Care Cre… | admin-held |  |
| 901 | `admin:policy:refund-policy:body#b092` | policy | 7. Pricing transparency | admin-held |  |
| 902 | `admin:policy:refund-policy:body#b093` | policy | The price you see includes VAT. A “was” price is always our lowest price of the previous 30 days, a… | admin-held |  |
| 903 | `admin:policy:refund-policy:body#b094` | policy | In accordance with the EU Omnibus Directive (2019/2161) and the Belgian Code of Economic Law (Art. … | admin-held |  |
| 904 | `admin:policy:refund-policy:body#b095` | policy | All-inclusive pricing. Prices shown to European consumers include VAT and all applicable levies. Sh… | admin-held |  |
| 905 | `admin:policy:refund-policy:body#b096` | policy | Genuine discounts. When we announce a price reduction, the reference price is the lowest price KARM… | admin-held |  |
| 906 | `admin:policy:refund-policy:body#b097` | policy | Authentic reviews. We only collect and publish reviews from verified purchasers. Reviews are never … | admin-held |  |
| 907 | `admin:policy:refund-policy:body#b098` | policy | 8. Complaints and dispute resolution | admin-held |  |
| 908 | `admin:policy:refund-policy:body#b099` | policy | Write to us first: we reply within 2 working days and give you a solution or a substantiated answer… | admin-held |  |
| 909 | `admin:policy:refund-policy:body#b100` | policy | Email care@karmicare.com, or call +32 (0) 478 57 27 61, about any issue with an order, a delivery o… | admin-held |  |
| 910 | `admin:policy:refund-policy:body#b101` | policy | If we cannot reach an amicable solution, you have access to independent out-of-court dispute resolu… | admin-held |  |
| 911 | `admin:policy:refund-policy:body#b102` | policy | 8.1 Belgian Consumer Mediation Service | admin-held |  |
| 912 | `admin:policy:refund-policy:body#b103` | policy | For Belgian and cross-border European disputes: Consumer Mediation Service (Consumentenombudsdienst… | admin-held |  |
| 913 | `admin:policy:refund-policy:body#b104` | policy | 8.2 European Consumer Centre | admin-held |  |
| 914 | `admin:policy:refund-policy:body#b105` | policy | For a dispute across EU borders, the European Consumer Centre in your country can help. In Belgium:… | admin-held |  |
| 915 | `admin:policy:refund-policy:body#b106` | policy | The EU Online Dispute Resolution (ODR) platform closed on 20 July 2025, so it is no longer a route … | admin-held |  |
| 916 | `admin:policy:refund-policy:body#b107` | policy | 9. Applicable law and jurisdiction | admin-held |  |
| 917 | `admin:policy:refund-policy:body#b108` | policy | Belgian law applies, but never at the expense of the protection your own country gives you. | admin-held |  |
| 918 | `admin:policy:refund-policy:body#b109` | policy | Contracts concluded with KARMICARE are governed by Belgian law. Under Article 6 of the Rome I Regul… | admin-held |  |
| 919 | `admin:policy:refund-policy:body#b110` | policy | Under Article 18 of the Brussels I bis Regulation (EU) No 1215/2012, you can bring a claim before t… | admin-held |  |
| 920 | `admin:policy:refund-policy:body#b111` | policy | 10. Model withdrawal form | admin-held |  |
| 921 | `admin:policy:refund-policy:body#b112` | policy | Changed your mind about a one-time order? Send us this form, or simply email us a clear statement. … | admin-held |  |
| 922 | `admin:policy:refund-policy:body#b113` | policy | To: KARMICA BV (KARMICARE), Vizierstraat 28, 8000 Bruges, Belgium, care@karmicare.com, +32 (0) 478 … | admin-held |  |
| 923 | `admin:policy:refund-policy:body#b114` | policy | I/We (*) hereby give notice that I/We (*) withdraw from my/our (*) contract of sale of the followin… | admin-held |  |
| 924 | `admin:policy:refund-policy:body#b115` | policy | Goods: | admin-held |  |
| 925 | `admin:policy:refund-policy:body#b116` | policy | Ordered on (*) / Received on (*): | admin-held |  |
| 926 | `admin:policy:refund-policy:body#b117` | policy | Order reference number: | admin-held |  |
| 927 | `admin:policy:refund-policy:body#b118` | policy | Name of consumer(s): | admin-held |  |
| 928 | `admin:policy:refund-policy:body#b119` | policy | Address of consumer(s): | admin-held |  |
| 929 | `admin:policy:refund-policy:body#b120` | policy | Signature of consumer(s), only if this form is sent on paper: | admin-held |  |
| 930 | `admin:policy:refund-policy:body#b121` | policy | Date: | admin-held |  |
| 931 | `admin:policy:refund-policy:body#b122` | policy | (*) Delete as appropriate. Complete and return this form only if you wish to withdraw from an eligi… | admin-held |  |
| 932 | `admin:policy:refund-policy:body#b123` | policy | Download the form (PDF) | admin-held |  |
| 933 | `admin:policy:refund-policy:body#b124` | policy | Questions about your rights? Write to care@karmicare.com . A person reads every message. | admin-held |  |
| 934 | `admin:policy:refund-policy:seo.title` | policy | Refund policy – KARMICARE | admin-held |  |
| 935 | `admin:policy:shipping-policy:title` | policy | Shipping policy | admin-held |  |
| 936 | `admin:policy:shipping-policy:body#b001` | policy | This text is taken word for word from clauses 8 and 5.4 of our Terms and Conditions . The Terms are… | admin-held |  |
| 937 | `admin:policy:shipping-policy:body#b002` | policy | Clause 8 – Delivery and transfer of risk | admin-held |  |
| 938 | `admin:policy:shipping-policy:body#b003` | policy | Until your parcel is in your hands, it is our responsibility. | admin-held |  |
| 939 | `admin:policy:shipping-policy:body#b004` | policy | Transfer of risk (Art. VI.44 WER): the risk of loss, theft or damage in transit stays with KARMICA … | admin-held |  |
| 940 | `admin:policy:shipping-policy:body#b005` | policy | Delivery area: we deliver to addresses in the member states of the European Union. Please make sure… | admin-held |  |
| 941 | `admin:policy:shipping-policy:body#b006` | policy | Delivery times (estimates): Belgium, the Netherlands and Luxembourg: within 24 hours; rest of the E… | admin-held |  |
| 942 | `admin:policy:shipping-policy:body#b007` | policy | Delays: unless another date was agreed, we deliver within 30 days of the contract. If we do not, yo… | admin-held |  |
| 943 | `admin:policy:shipping-policy:body#b008` | policy | Shipping charges (clause 5.4): memberships ship free within the European Union. For Try Once, the s… | admin-held |  |
| 944 | `admin:policy:shipping-policy:seo.title` | policy | Shipping policy – KARMICARE | admin-held |  |
| 945 | `admin:policy:contact-information:title` | policy | Contact information | admin-held |  |
| 946 | `admin:policy:contact-information:body#b001` | policy | This text is taken word for word from clauses 1 and 15.1 of our Terms and Conditions . The Terms ar… | admin-held |  |
| 947 | `admin:policy:contact-information:body#b002` | policy | Clause 1 – Identity of the vendor | admin-held |  |
| 948 | `admin:policy:contact-information:body#b003` | policy | You buy from KARMICA BV, a Belgian company in Bruges. | admin-held |  |
| 949 | `admin:policy:contact-information:body#b004` | policy | The webshop karmicare.com and its checkout subdomains are operated by: | admin-held |  |
| 950 | `admin:policy:contact-information:body#b005` | policy | KARMICA BV (trading as KARMICARE ), Vizierstraat 28, 8000 Bruges, Belgium · Enterprise number (KBO/… | admin-held |  |
| 951 | `admin:policy:contact-information:body#b006` | policy | Complaints and questions (clause 15.1): for questions, feedback or complaints, write to our custome… | admin-held |  |
| 952 | `admin:policy:contact-information:seo.title` | policy | Contact information – KARMICARE | admin-held |  |
| 953 | `admin:policy:legal-notice:title` | policy | Legal notice | admin-held |  |
| 954 | `admin:policy:legal-notice:body#b001` | policy | This text is taken word for word from clause 1 of our Terms and Conditions . The Terms are the cont… | admin-held |  |
| 955 | `admin:policy:legal-notice:body#b002` | policy | Clause 1 – Identity of the vendor | admin-held |  |
| 956 | `admin:policy:legal-notice:body#b003` | policy | You buy from KARMICA BV, a Belgian company in Bruges. | admin-held |  |
| 957 | `admin:policy:legal-notice:body#b004` | policy | The webshop karmicare.com and its checkout subdomains are operated by: | admin-held |  |
| 958 | `admin:policy:legal-notice:body#b005` | policy | KARMICA BV (trading as KARMICARE ), Vizierstraat 28, 8000 Bruges, Belgium · Enterprise number (KBO/… | admin-held |  |
| 959 | `admin:policy:legal-notice:seo.title` | policy | Legal notice – KARMICARE | admin-held |  |
| 960 | `admin:policy:subscription-policy:title` | policy | Cancellation policy | admin-held |  |
| 961 | `admin:policy:subscription-policy:body#b001` | policy | This text is taken word for word from clause 9 of our Terms and Conditions . The Terms are the cont… | admin-held |  |
| 962 | `admin:policy:subscription-policy:body#b002` | policy | Clause 9 – Memberships | admin-held |  |
| 963 | `admin:policy:subscription-policy:body#b003` | policy | No lock-in, a protected price and a reminder before every renewal. Gift, pause, skip or stop whenev… | admin-held |  |
| 964 | `admin:policy:subscription-policy:body#b004` | policy | The options: Try Once is a single duo without renewal. The 60-Day rhythm delivers one duo and renew… | admin-held |  |
| 965 | `admin:policy:subscription-policy:body#b005` | policy | Authorisation: when you start a membership, you authorise KARMICARE (through our payment processor,… | admin-held |  |
| 966 | `admin:policy:subscription-policy:body#b006` | policy | Welcome Kit: your first membership order includes a Welcome Kit with a morning toothbrush, an eveni… | admin-held |  |
| 967 | `admin:policy:subscription-policy:body#b007` | policy | Renewal reminder: we email you at least 5 days before every 60-Day rhythm renewal, and 30 days and … | admin-held |  |
| 968 | `admin:policy:subscription-policy:body#b008` | policy | Pausing: you can pause for up to 60 days at a time, and for up to 60 days in total within any 12 mo… | admin-held |  |
| 969 | `admin:policy:subscription-policy:body#b009` | policy | Cancelling: you can cancel at any time in your customer portal or by email. Cancelling stops your n… | admin-held |  |
| 970 | `admin:policy:subscription-policy:body#b010` | policy | End of your membership: your membership ends when the last period you paid for runs out. | admin-held |  |
| 971 | `admin:policy:subscription-policy:body#b011` | policy | Switching plans: to move from the 60-Day rhythm to the Year, cancel your 60-Day rhythm and start a … | admin-held |  |
| 972 | `admin:policy:subscription-policy:body#b012` | policy | Renewal orders and ending a renewed Year: renewal orders are dispatched two working days after the … | admin-held |  |
| 973 | `admin:policy:subscription-policy:body#b013` | policy | Gifting: you can send a delivery as a gift to another address in the European Union from your custo… | admin-held |  |
| 974 | `admin:policy:subscription-policy:seo.title` | policy | Cancellation policy – KARMICARE | admin-held |  |

### `batch-05-products`

| # | id | type | EN | status | flags |
|---:|---|---|---|---|---|
| 1 | `product:main/highlights_slider_9wAjAb/text_1` | template_setting | Used by +100 kPNI practitioners | needs-review |  |
| 2 | `product:main/highlights_slider_9wAjAb/text_2` | template_setting | Leave-on Technology | approved |  |
| 3 | `product:main/highlights_slider_9wAjAb/text_3` | template_setting | Backed by 39 peer-reviewed studies | needs-review |  |
| 4 | `product:main/buy_buttons/custom_button_text` | template_setting | Begin Now | approved |  |
| 5 | `product:main/icon_with_text_xhaDGB/heading_1` | template_setting | 60 day money back guarantee | approved |  |
| 6 | `product:main/icon_with_text_xhaDGB/heading_2` | template_setting | Cancel anytime | approved |  |
| 7 | `product:main/icon_with_text_xhaDGB/heading_3` | template_setting | Free shipping | approved |  |
| 8 | `product:main/treatment_journey_block/read_more_text` | template_setting | Read more | approved |  |
| 9 | `product:main/treatment_journey_block/read_less_text` | template_setting | Read less | approved |  |
| 10 | `product:main/treatment_journey_block/disclaimer_text` | template_setting | * What members report with continued use — individual experiences vary. | approved |  |
| 11 | `product:main/professional_testimonials_block/heading` | template_setting | Approved by nature. Used by professionals | approved |  |
| 12 | `product:main/info_card_FnBcaN/header_text` | template_setting | OUR COMMITMENT TO YOU | approved |  |
| 13 | `product:main/info_card_FnBcaN/body_text` | template_setting | With each purchase, we reward you . You invest in your health. We reinvest in you. Long-term health… | approved |  |
| 14 | `product:main/sticky_cart_block/button_text` | template_setting | Begin Now | approved |  |
| 15 | `product:disclosures/heading` | template_setting | Disclosures | approved |  |
| 16 | `product:related-products/heading` | template_setting | You may also like | approved |  |
| 17 | `admin:product:complete-hygiene-kit:seo.title` | product | Karmicare Complete Hygiene Kit – KARMICARE | admin-held |  |
| 18 | `admin:product:complete-hygiene-kit:seo.description` | product | Get the full hygiene kit including the Biorhythmic Oral Hygiene Set, Morning Toothbrush, Evening To… | admin-held |  |
| 19 | `admin:app:judge-me:preview_badge.stars` | app | [span aria-label] {{ rating }} stars | admin-held |  |
| 20 | `admin:app:judge-me:preview_badge.review_count` | app | {{ count }} review(s) | admin-held |  |
| 21 | `admin:product:morning-toothbrush:seo.title` | product | KARMICARE Ultra Soft Morning Toothbrush | admin-held |  |
| 22 | `admin:product:morning-toothbrush:seo.description` | product | The bristles are extremely soft so you can gently clean teeth and gums with ultimate care.The ultra… | admin-held |  |
| 23 | `admin:product:evening-toothbrush:seo.title` | product | KARMICARE Ultra-soft Detoxifying Evening Toothbrush | admin-held |  |
| 24 | `admin:product:evening-toothbrush:seo.description` | product | The bristles are extremely soft and coated with activated charcoal.The ultra thin, featherlight bri… | admin-held |  |
| 25 | `admin:product:whitening-charcoal-dental-floss:seo.title` | product | KARMICARE Whitening Charcoal Floss | admin-held |  |
| 26 | `admin:product:whitening-charcoal-dental-floss:seo.description` | product | Ultrathin bamboo charcoal dental floss without flavour.Helps remove tenacious plaque without damagi… | admin-held |  |
| 27 | `admin:app:judge-me:preview_badge.no_reviews` | app | No reviews | admin-held |  |
| 28 | `admin:product:evening-toothbrush-2-0:seo.title` | product | KARMICARE Ultra-soft Detoxifying Evening Toothbrush | admin-held |  |
| 29 | `admin:product:evening-toothbrush-2-0:seo.description` | product | The bristles are extremely soft and coated with activated charcoal.The ultra thin, featherlight bri… | admin-held |  |
| 30 | `admin:product:morning-toothbrush-2-0:seo.title` | product | KARMICARE Ultra Soft Morning Toothbrush | admin-held |  |
| 31 | `admin:product:morning-toothbrush-2-0:seo.description` | product | The bristles are extremely soft so you can gently clean teeth and gums with ultimate care.The ultra… | admin-held |  |
| 32 | `admin:product:asleep-evening-toothpaste-2-0:seo.title` | product | Karmicare Asleep Evening Toothpaste – KARMICARE | admin-held |  |
| 33 | `admin:product:asleep-evening-toothpaste-2-0:seo.description` | product | Something for your mind, your mouth and your soul. A toothpaste that helps you fall asleep at night… | admin-held |  |
| 34 | `admin:product:awake-morning-toothpaste-2-0:seo.title` | product | Karmicare Awake Morning Toothpaste – KARMICARE | admin-held |  |
| 35 | `admin:product:awake-morning-toothpaste-2-0:seo.description` | product | Something for your mind, your mouth and your soul. A toothpaste that helps you get up in the mornin… | admin-held |  |
| 36 | `admin:product:complete-hygiene-kit:title` | product | Complete Hygiene Kit | admin-held |  |
| 37 | `admin:product:complete-hygiene-kit:body_html#b001` | product | Get the full hygiene kit including the Biorhythmic Oral Hygiene Set, Morning Toothbrush, Evening To… | admin-held |  |
| 38 | `admin:product:morning-toothbrush:title` | product | Morning Toothbrush | admin-held |  |
| 39 | `admin:product:morning-toothbrush:body_html#b001` | product | The bristles are extremely soft so you can gently clean teeth and gums with ultimate care. The ultr… | admin-held |  |
| 40 | `admin:product:morning-toothbrush:media.27295901057206.alt` | product | Karmicare Morning Toothbrush | admin-held |  |
| 41 | `admin:product:evening-toothbrush:title` | product | Evening Toothbrush | admin-held |  |
| 42 | `admin:product:evening-toothbrush:body_html#b001` | product | The bristles are extremely soft and coated with activated charcoal. The ultra thin, featherlight br… | admin-held |  |
| 43 | `admin:product:evening-toothbrush:media.27295901221046.alt` | product | Karmicare Avond Tandenborstel | admin-held |  |
| 44 | `admin:product:whitening-charcoal-dental-floss:title` | product | Whitening Charcoal Floss | admin-held |  |
| 45 | `admin:product:whitening-charcoal-dental-floss:body_html#b001` | product | Ultrathin bamboo charcoal dental floss without flavour. Helps remove tenacious plaque without damag… | admin-held |  |
| 46 | `admin:product:whitening-charcoal-dental-floss:media.27295901876406.alt` | product | Karmicare Whitening Charcoal Floss | admin-held |  |
| 47 | `admin:app:whitening-charcoal-dental-floss:selling_plan_group:Subscribe and Save` | app | Subscribe and Save | admin-held |  |
| 48 | `admin:app:whitening-charcoal-dental-floss:selling_plan.712456601981.name` | app | Deliver every 6 month | admin-held |  |
| 49 | `admin:app:whitening-charcoal-dental-floss:selling_plan.712460992893.name` | app | Deliver every 60 days | admin-held |  |
| 50 | `admin:product:evening-toothbrush-2-0:title` | product | Evening Toothbrush 2.0 | admin-held |  |
| 51 | `admin:product:evening-toothbrush-2-0:body_html#b001` | product | The bristles are extremely soft and coated with activated charcoal. The ultra thin, featherlight br… | admin-held |  |
| 52 | `admin:product:evening-toothbrush-2-0:media.27295901221046.alt` | product | Karmicare Avond Tandenborstel | admin-held |  |
| 53 | `admin:app:evening-toothbrush-2-0:selling_plan_group:Subscribe and Save` | app | Subscribe and Save | admin-held |  |
| 54 | `admin:app:evening-toothbrush-2-0:selling_plan.712456634749.name` | app | Deliver every 6 month | admin-held |  |
| 55 | `admin:app:evening-toothbrush-2-0:selling_plan.712460992893.name` | app | Deliver every 60 days | admin-held |  |
| 56 | `admin:product:morning-toothbrush-2-0:title` | product | Morning Toothbrush 2.0 | admin-held |  |
| 57 | `admin:product:morning-toothbrush-2-0:body_html#b001` | product | The bristles are extremely soft so you can gently clean teeth and gums with ultimate care. The ultr… | admin-held |  |
| 58 | `admin:product:morning-toothbrush-2-0:media.27295901057206.alt` | product | Karmicare Morning Toothbrush | admin-held |  |
| 59 | `admin:app:morning-toothbrush-2-0:selling_plan_group:Subscribe and Save` | app | Subscribe and Save | admin-held |  |
| 60 | `admin:app:morning-toothbrush-2-0:selling_plan.712456667517.name` | app | Deliver every 6 month | admin-held |  |
| 61 | `admin:app:morning-toothbrush-2-0:selling_plan.712460992893.name` | app | Deliver every 60 days | admin-held |  |
| 62 | `admin:product:asleep-evening-toothpaste-2-0:title` | product | Asleep Evening Toothpaste 2.0 | admin-held |  |
| 63 | `admin:product:asleep-evening-toothpaste-2-0:body_html#b001` | product | Something for your mind, your mouth and your soul. | admin-held |  |
| 64 | `admin:product:asleep-evening-toothpaste-2-0:body_html#b002` | product | A toothpaste that helps you fall asleep at night. | admin-held |  |
| 65 | `admin:product:asleep-evening-toothpaste-2-0:body_html#b003` | product | With superior minerals like Nano-HAp, and active Nootropics, Karmicare helps you achieve an optimum… | admin-held |  |
| 66 | `admin:product:asleep-evening-toothpaste-2-0:body_html#b004` | product | Unlike fluoride-based oral hygiene products that disturb your wake/sleep cycles, Karmicare actually… | admin-held |  |
| 67 | `admin:app:asleep-evening-toothpaste-2-0:selling_plan_group:Subscribe and Save` | app | Subscribe and Save | admin-held |  |
| 68 | `admin:app:asleep-evening-toothpaste-2-0:selling_plan.712456700285.name` | app | Deliver every 6 month | admin-held |  |
| 69 | `admin:app:asleep-evening-toothpaste-2-0:selling_plan.712460992893.name` | app | Deliver every 60 days | admin-held |  |
| 70 | `admin:product:awake-morning-toothpaste-2-0:title` | product | Awake Morning Toothpaste 2.0 | admin-held |  |
| 71 | `admin:product:awake-morning-toothpaste-2-0:body_html#b001` | product | Something for your mind, your mouth and your soul. | admin-held |  |
| 72 | `admin:product:awake-morning-toothpaste-2-0:body_html#b002` | product | A toothpaste that helps you get up in the morning. | admin-held |  |
| 73 | `admin:product:awake-morning-toothpaste-2-0:body_html#b003` | product | With superior minerals like Nano-HAp, and active Nootropics, Karmicare helps you achieve an optimum… | admin-held |  |
| 74 | `admin:product:awake-morning-toothpaste-2-0:body_html#b004` | product | Unlike fluoride-based oral hygiene products that disturb your wake/sleep cycles, Karmicare actually… | admin-held |  |
| 75 | `admin:app:awake-morning-toothpaste-2-0:selling_plan_group:Subscribe and Save` | app | Subscribe and Save | admin-held |  |
| 76 | `admin:app:awake-morning-toothpaste-2-0:selling_plan.712456733053.name` | app | Deliver every 6 month | admin-held |  |
| 77 | `admin:app:awake-morning-toothpaste-2-0:selling_plan.712460992893.name` | app | Deliver every 60 days | admin-held |  |

### `batch-06-content-pages`

| # | id | type | EN | status | flags |
|---:|---|---|---|---|---|
| 1 | `admin:page:why-karmicare:title` | page | Why Karmicare | admin-held |  |
| 2 | `admin:page:why-karmicare:body_html#b001` | page | The moments before you sleep and after you wake determine the quality of your life | admin-held |  |
| 3 | `admin:page:why-karmicare:seo.title` | page | Why Karmicare – KARMICARE | admin-held |  |
| 4 | `admin:page:why-karmicare:seo.description` | page | The moments before you sleep and after you wake determine the quality of your life | admin-held |  |
| 5 | `admin:page:why-use-hydroxyapatite-toothpaste:title` | page | Why use Hydroxyapatite Toothpaste | admin-held |  |
| 6 | `admin:page:why-use-hydroxyapatite-toothpaste:body_html#b001` | page | Here’s why you should start using hydroxyapatite toothpaste | admin-held |  |
| 7 | `admin:page:why-use-hydroxyapatite-toothpaste:seo.title` | page | Why use Hydroxyapatite Toothpaste – KARMICARE | admin-held |  |
| 8 | `admin:page:why-use-hydroxyapatite-toothpaste:seo.description` | page | Here’s why you should start using hydroxyapatite toothpaste | admin-held |  |
| 9 | `admin:page:why-stop-using-fluoride-toothpaste:title` | page | Why stop using fluoride toothpaste | admin-held |  |
| 10 | `admin:page:why-stop-using-fluoride-toothpaste:body_html#b001` | page | There’s no fluoride in our Awake or Asleep toothpaste. Nor will there ever be | admin-held |  |
| 11 | `admin:page:why-stop-using-fluoride-toothpaste:body_html#b002` | page | Here’s why you should stop using fluoride toothpaste | admin-held |  |
| 12 | `admin:page:why-stop-using-fluoride-toothpaste:seo.title` | page | Why stop using fluoride toothpaste – KARMICARE | admin-held |  |
| 13 | `admin:page:why-stop-using-fluoride-toothpaste:seo.description` | page | There’s no fluoride in our Awake or Asleep toothpaste. Nor will there ever be Here’s why you should… | admin-held |  |
| 14 | `admin:page:nhap-technology:title` | page | nHAp Technology | admin-held |  |
| 15 | `admin:page:nhap-technology:body_html#b000` | page | Discover the Wonderful Inner World of Nano Hydroxyapatite and Why You Need it in Your Toothpaste | admin-held |  |
| 16 | `admin:page:nhap-technology:body_html#b001` | page | Dive deep into the benefits of NASA’s favorite supplement for oral health | admin-held |  |
| 17 | `admin:page:nhap-technology:seo.title` | page | nHAp Technology – KARMICARE | admin-held |  |
| 18 | `admin:page:nhap-technology:seo.description` | page | Discover the Wonderful Inner World of Nano Hydroxyapatite and Why You Need it in Your Toothpaste Di… | admin-held |  |
| 19 | `admin:page:articles:title` | page | Articles | admin-held |  |
| 20 | `admin:page:articles:body_html#b001` | page | Discover our latest articles | admin-held |  |
| 21 | `admin:page:articles:seo.title` | page | Articles – KARMICARE | admin-held |  |
| 22 | `admin:page:articles:seo.description` | page | Discover our latest articles | admin-held |  |

### `batch-07-collections-blog`

| # | id | type | EN | status | flags |
|---:|---|---|---|---|---|
| 1 | `article:main/share/share_label` | template_setting | Share | approved |  |
| 2 | `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:title` | article | Benefits of Nootropics: Ease Stress, Boost Focus and Improve Mood. | admin-held |  |
| 3 | `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:summary_html` | article |  | admin-held |  |
| 4 | `admin:article:news/3-reasons-why-you-should-look-for-an-sls-free-toothpaste:title` | article | 3 Reasons Why you Should look for an SLS Free Toothpaste | admin-held |  |
| 5 | `admin:article:news/3-reasons-why-you-should-look-for-an-sls-free-toothpaste:summary_html` | article |  | admin-held |  |
| 6 | `admin:article:news/nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste:title` | article | Nano-Hydroxyapatite and Why You Need It In Your Toothpaste. | admin-held |  |
| 7 | `admin:article:news/nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste:summary_html` | article |  | admin-held |  |
| 8 | `admin:article:news/top-natural-whitening-toothpaste-for-a-brighter-smile:title` | article | Top Natural Whitening Toothpaste For a Brighter Smile. | admin-held |  |
| 9 | `admin:article:news/top-natural-whitening-toothpaste-for-a-brighter-smile:summary_html` | article |  | admin-held |  |
| 10 | `admin:article:news/morning-and-night-time-brushing-why-timing-matters:title` | article | Morning and Night Time Brushing: Why Timing Matters. | admin-held |  |
| 11 | `admin:article:news/morning-and-night-time-brushing-why-timing-matters:summary_html` | article |  | admin-held |  |
| 12 | `admin:article:news/5-reasons-you-should-avoid-fluoride-in-toothpaste:title` | article | 5 Reasons You Should Avoid Fluoride in Toothpaste | admin-held |  |
| 13 | `admin:article:news/5-reasons-you-should-avoid-fluoride-in-toothpaste:summary_html` | article |  | admin-held |  |
| 14 | `admin:article:news/how-oral-health-impacts-your-overall-wellness:title` | article | How Oral Health Impacts Your Overall Wellness | admin-held |  |
| 15 | `admin:article:news/how-oral-health-impacts-your-overall-wellness:summary_html` | article |  | admin-held |  |
| 16 | `admin:article:news/headaches-and-tooth-pain-understanding-the-connection:title` | article | Headaches and Tooth Pain: Understanding the Connection | admin-held |  |
| 17 | `admin:article:news/headaches-and-tooth-pain-understanding-the-connection:summary_html` | article |  | admin-held |  |
| 18 | `admin:article:news/nano-hydroxyapatite:title` | article | Discover the Wonderful Inner World of Nano Hydroxyapatite and Why You Need it in Your Toothpaste | admin-held |  |
| 19 | `admin:article:news/nano-hydroxyapatite:summary_html` | article |  | admin-held |  |
| 20 | `admin:collection:biorhythmic-oral-hygiene-kit:text#01` | collection | Collection: | admin-held |  |
| 21 | `admin:collection:biorhythmic-oral-hygiene-kit:text#02` | collection | Complete Oral Hygiene Kit | admin-held |  |
| 22 | `admin:collection:biorhythmic-oral-hygiene-kit:seo.title` | collection | Complete Oral Hygiene Kit – KARMICARE | admin-held |  |
| 23 | `admin:collection:vgbc2025:text#01` | collection | Collection: | admin-held |  |
| 24 | `admin:collection:vgbc2025:text#02` | collection | VGBC2025 | admin-held |  |
| 25 | `admin:collection:vgbc2025:seo.title` | collection | VGBC2025 – KARMICARE | admin-held |  |
| 26 | `admin:collection:karmicare-collection:text#01` | collection | Collection: | admin-held |  |
| 27 | `admin:collection:karmicare-collection:text#02` | collection | Karmicare Collection | admin-held |  |
| 28 | `admin:collection:karmicare-collection:seo.title` | collection | Karmicare Collection – KARMICARE | admin-held |  |
| 29 | `admin:blog:news:seo.title` | blog | News – KARMICARE | admin-held |  |
| 30 | `admin:article:news/nano-hydroxyapatite:text#01` | article | [img alt] Discover the Wonderful Inner World of Nano Hydroxyapatite and Why You Need it in Your Too… | admin-held |  |
| 31 | `admin:article:news/nano-hydroxyapatite:body_html#b001` | article | Self reflection: | admin-held |  |
| 32 | `admin:article:news/nano-hydroxyapatite:body_html#b002` | article | Does the toothpaste I’m using support my oral health? | admin-held |  |
| 33 | `admin:article:news/nano-hydroxyapatite:body_html#b003` | article | How can I use brushing my teeth in the morning and evening as a way to nourish my body? | admin-held |  |
| 34 | `admin:article:news/nano-hydroxyapatite:body_html#b004` | article | Is there a way to safely remineralize my teeth and enhance my smile? | admin-held |  |
| 35 | `admin:article:news/nano-hydroxyapatite:body_html#b005` | article | Key takeaways: | admin-held |  |
| 36 | `admin:article:news/nano-hydroxyapatite:body_html#b006` | article | Nano hydroxyapatite has powerful remineralizing effects on enamel lesions while being safe, nontoxi… | admin-held |  |
| 37 | `admin:article:news/nano-hydroxyapatite:body_html#b007` | article | A review of literature found nano hydroxyapatite is an effective remineralizing agent, and demonstr… | admin-held |  |
| 38 | `admin:article:news/nano-hydroxyapatite:body_html#b008` | article | Choosing a natural toothpaste formulation with nano hydroxyapatite can help prevent tooth decay, wh… | admin-held |  |
| 39 | `admin:article:news/nano-hydroxyapatite:body_html#b009` | article | “There’s no fluoride in our Awake or Asleep toothpaste. Nor will there ever be.” — Victor Popov, Fo… | admin-held |  |
| 40 | `admin:article:news/nano-hydroxyapatite:body_html#b010` | article | WHY? Because as well as resisting negative self-talk, I avoid putting chemicals into my system. Esp… | admin-held |  |
| 41 | `admin:article:news/nano-hydroxyapatite:body_html#b011` | article | Read on and discover everything you need to know about this medical marvel for better teeth, bones … | admin-held |  |
| 42 | `admin:article:news/nano-hydroxyapatite:body_html#b012` | article | 10-Second Nano HAp Need-to-Know Truths | admin-held |  |
| 43 | `admin:article:news/nano-hydroxyapatite:body_html#b013` | article | Nano HAp dives into your enamel and refills the lost minerals every time you brush your teeth | admin-held |  |
| 44 | `admin:article:news/nano-hydroxyapatite:body_html#b014` | article | It smoothes and whitens teeth by gently repairing your tooth surface with native minerals | admin-held |  |
| 45 | `admin:article:news/nano-hydroxyapatite:body_html#b015` | article | It plugs exposed dentin tubules to effectively reduce tooth sensitivity | admin-held |  |
| 46 | `admin:article:news/nano-hydroxyapatite:body_html#b016` | article | It guards against tooth decay by providing total protection against harmful dietary acids | admin-held |  |
| 47 | `admin:article:news/nano-hydroxyapatite:body_html#b017` | article | It’s bioactive, osteoconductive, and nontoxic | admin-held |  |
| 48 | `admin:article:news/nano-hydroxyapatite:body_html#b018` | article | And much more — skip to our frequently asked questions to learn more little-known facts | admin-held |  |
| 49 | `admin:article:news/nano-hydroxyapatite:body_html#b019` | article | Expand Your Dental Knowledge | admin-held |  |
| 50 | `admin:article:news/nano-hydroxyapatite:body_html#b020` | article | Enamel — the outer shell of the tooth that protects against tooth decay . Ninety-seven percent of t… | admin-held |  |
| 51 | `admin:article:news/nano-hydroxyapatite:body_html#b021` | article | Dentin — the second layer of the tooth situated right under the enamel. Seventy percent of dentin i… | admin-held |  |
| 52 | `admin:article:news/nano-hydroxyapatite:body_html#b022` | article | Dentin tubules — microscopic channels that connect the enamel surface to the dental pulp. These cha… | admin-held |  |
| 53 | `admin:article:news/nano-hydroxyapatite:body_html#b023` | article | Tooth erosion — refers to the loss of tooth enamel due to exposure to acid. | admin-held |  |
| 54 | `admin:article:news/nano-hydroxyapatite:body_html#b024` | article | Micropores — the enamel might look smooth but has thousands of pores. It’s these pores that absorb … | admin-held |  |
| 55 | `admin:article:news/nano-hydroxyapatite:body_html#b025` | article | Enamel lesions — any damage or abnormal change to enamel. | admin-held |  |
| 56 | `admin:article:news/nano-hydroxyapatite:body_html#b026` | article | Dental pulp — the innermost part of the tooth. It’s soft and full of nerves and blood vessels. | admin-held |  |
| 57 | `admin:article:news/nano-hydroxyapatite:body_html#b027` | article | Hydroxyapatite — a naturally occurring mineral form of calcium apatite ( calcium , phosphorous oxyg… | admin-held |  |
| 58 | `admin:article:news/nano-hydroxyapatite:body_html#b028` | article | Nano hydroxyapatite — nano-sized version of hydroxyapatite that’s commonly used in dentistry , oste… | admin-held |  |
| 59 | `admin:article:news/nano-hydroxyapatite:body_html#b029` | article | Micro HAp — particles of HA that are slightly bigger than nano HAp. | admin-held |  |
| 60 | `admin:article:news/nano-hydroxyapatite:body_html#b030` | article | So, What Is Nano Hydroxyapatite? | admin-held |  |
| 61 | `admin:article:news/nano-hydroxyapatite:body_html#b031` | article | “Hydroxy-WHAT?!” — we get it. It’s a bit of a mouthful to speak and to spell. But while it may seem… | admin-held |  |
| 62 | `admin:article:news/nano-hydroxyapatite:body_html#b032` | article | There are a few essential characteristics of nano HAp that make this mineral so indispensable to ou… | admin-held |  |
| 63 | `admin:article:news/nano-hydroxyapatite:body_html#b033` | article | Biocompatible — It exists in harmony with its surrounding tissues. | admin-held |  |
| 64 | `admin:article:news/nano-hydroxyapatite:body_html#b034` | article | Bioactive — Nano HAp is already in a bioavailable, usable form. | admin-held |  |
| 65 | `admin:article:news/nano-hydroxyapatite:body_html#b035` | article | Osteoconductive — Nano HAp serves as a scaffold for new bone growth. | admin-held |  |
| 66 | `admin:article:news/nano-hydroxyapatite:body_html#b036` | article | Nontoxic and non-inflammatory — Since hydroxyapatite is a naturally occurring organic biomaterial i… | admin-held |  |
| 67 | `admin:article:news/nano-hydroxyapatite:body_html#b037` | article | Formed By Nature. Refined By NASA. Utilized By Karmicare. | admin-held |  |
| 68 | `admin:article:news/nano-hydroxyapatite:body_html#b038` | article | Nano hydroxyapatite has a colorful history that spans across four decades. Believe it or not, NASA … | admin-held |  |
| 69 | `admin:article:news/nano-hydroxyapatite:body_html#b039` | article | Why would a space agency spend their time creating nano HAp? | admin-held |  |
| 70 | `admin:article:news/nano-hydroxyapatite:body_html#b040` | article | The astronauts returning home from the space mission were experiencing mineral loss from teeth and … | admin-held |  |
| 71 | `admin:article:news/nano-hydroxyapatite:body_html#b041` | article | Since then, nano HAp has cemented itself as the hallmark in the medical field and in oral care glob… | admin-held |  |
| 72 | `admin:article:news/nano-hydroxyapatite:body_html#b042` | article | But sadly, it’s not widely available in the mainstream. This is something we want to see changed, e… | admin-held |  |
| 73 | `admin:article:news/nano-hydroxyapatite:body_html#b043` | article | 4 Powerful Benefits of Nano Hydroxyapatite | admin-held |  |
| 74 | `admin:article:news/nano-hydroxyapatite:body_html#b044` | article | 1. Renews Your Teeth From the Inside Out | admin-held |  |
| 75 | `admin:article:news/nano-hydroxyapatite:body_html#b045` | article | Your teeth have microscopic holes (known as dentin tubules) present throughout the underside of the… | admin-held |  |
| 76 | `admin:article:news/nano-hydroxyapatite:body_html#b046` | article | When you indulge in sweet food or drink, the sugar-loving microbes metabolize the sugar and release… | admin-held |  |
| 77 | `admin:article:news/nano-hydroxyapatite:body_html#b047` | article | FYI: The pH level in Karmicare Biorhythmic Oral Health (both the Awake and Asleep formulations) is … | admin-held |  |
| 78 | `admin:article:news/nano-hydroxyapatite:body_html#b048` | article | Such an acidic environment is caustic to both enamel and dentin because it dissolves calcium and ph… | admin-held |  |
| 79 | `admin:article:news/nano-hydroxyapatite:body_html#b049` | article | This is known as demineralization. | admin-held |  |
| 80 | `admin:article:news/nano-hydroxyapatite:body_html#b050` | article | Since enamel isn’t a living tissue, it cannot regrow. But slight damage can be repaired through rem… | admin-held |  |
| 81 | `admin:article:news/nano-hydroxyapatite:body_html#b051` | article | It turns out that our body has its own natural buffer system — saliva. It prevents the pH level fro… | admin-held |  |
| 82 | `admin:article:news/nano-hydroxyapatite:body_html#b052` | article | Saliva keeps our enamel continuously bathed in a nourishing solution. | admin-held |  |
| 83 | `admin:article:news/nano-hydroxyapatite:body_html#b053` | article | But relying on saliva isn’t enough. You must take proactive measures to promote remineralization by… | admin-held |  |
| 84 | `admin:article:news/nano-hydroxyapatite:body_html#b054` | article | Keep in mind there are other reasons to be choosy with your toothpaste selection. Preservatives and… | admin-held |  |
| 85 | `admin:article:news/nano-hydroxyapatite:body_html#b055` | article | How Nano HAp Repairs Your Teeth | admin-held |  |
| 86 | `admin:article:news/nano-hydroxyapatite:body_html#b056` | article | Whenever you brush your teeth with a nano HAp toothpaste, it replaces the lost minerals by binding … | admin-held |  |
| 87 | `admin:article:news/nano-hydroxyapatite:body_html#b057` | article | An in vitro study using a scanning electron microscope (SEM) found a “formation of bone-like apatit… | admin-held |  |
| 88 | `admin:article:news/nano-hydroxyapatite:body_html#b058` | article | Nano HAp penetrates the enamel’s surface area and directly restores the amount of calcium and phosp… | admin-held |  |
| 89 | `admin:article:news/nano-hydroxyapatite:body_html#b059` | article | It also fills up the microscopic fissures present on the enamel surface. Nano HAp’s innate biocompa… | admin-held |  |
| 90 | `admin:article:news/nano-hydroxyapatite:body_html#b060` | article | 2. Nano Hydroxyapatite Whitens Your Teeth Without Hurting Your Enamel | admin-held |  |
| 91 | `admin:article:news/nano-hydroxyapatite:body_html#b061` | article | Stained yellow teeth are like a scarlet chain of shame for many people. | admin-held |  |
| 92 | `admin:article:news/nano-hydroxyapatite:body_html#b062` | article | They are reminded of it every time they look in the mirror, pose for a photo, or go for an intervie… | admin-held |  |
| 93 | `admin:article:news/nano-hydroxyapatite:body_html#b063` | article | From buying an expensive teeth whitening kit to brushing with baking soda to using apple cider vine… | admin-held |  |
| 94 | `admin:article:news/nano-hydroxyapatite:body_html#b064` | article | Most of the products available only give temporary results and leave behind a weak and demineralize… | admin-held |  |
| 95 | `admin:article:news/nano-hydroxyapatite:body_html#b065` | article | Bleaching agents like hydrogen peroxide cause tooth sensitivity and chemical burns. So while you’ll… | admin-held |  |
| 96 | `admin:article:news/nano-hydroxyapatite:body_html#b066` | article | Other whitening toothpaste has minute particles that work like sandpaper, exfoliating the stains fr… | admin-held |  |
| 97 | `admin:article:news/nano-hydroxyapatite:body_html#b067` | article | Low-abrasive toothpastes (like Karmicare) that contain nano HAp are a far safer alternative to comm… | admin-held |  |
| 98 | `admin:article:news/nano-hydroxyapatite:body_html#b068` | article | How Nano HAp Whitens Your Teeth | admin-held |  |
| 99 | `admin:article:news/nano-hydroxyapatite:body_html#b069` | article | Nano HAp remineralizes teeth from the inside, which smooths the tooth’s surface and makes it glossi… | admin-held |  |
| 100 | `admin:article:news/nano-hydroxyapatite:body_html#b070` | article | The whitening effect of nano HAp on teeth is not the result of a mechanical or chemical reaction. | admin-held |  |
| 101 | `admin:article:news/nano-hydroxyapatite:body_html#b071` | article | It’s the result of the filling of micropores in the tooth enamel. By restoring necessary minerals b… | admin-held |  |
| 102 | `admin:article:news/nano-hydroxyapatite:body_html#b072` | article | Karmicare Nano HAp can be used every day for whitening with no adverse side effects. Brushing with … | admin-held |  |
| 103 | `admin:article:news/nano-hydroxyapatite:body_html#b073` | article | Then, when you brush again in the morning, you are fortifying the brightness even more. | admin-held |  |
| 104 | `admin:article:news/nano-hydroxyapatite:body_html#b074` | article | 3. Nano Hydroxyapatite Reduces Your Tooth Hypersensitivity by Blocking Dentinal Tubules | admin-held |  |
| 105 | `admin:article:news/nano-hydroxyapatite:body_html#b075` | article | Tooth sensitivity, or dental hypersensitivity, occurs when your mouth mirrors the harsh elements of… | admin-held |  |
| 106 | `admin:article:news/nano-hydroxyapatite:body_html#b076` | article | Imagine being anxious after every sip of hot beverage, every bite of ice cream, or every crunch of … | admin-held |  |
| 107 | `admin:article:news/nano-hydroxyapatite:body_html#b077` | article | The sharp, stabbing pain that makes your jaw tighten and eyes squeeze shut is the reality for milli… | admin-held |  |
| 108 | `admin:article:news/nano-hydroxyapatite:body_html#b078` | article | The worst part is that the pain can strike anytime. Even brushing or flossing can be anxiety-induci… | admin-held |  |
| 109 | `admin:article:news/nano-hydroxyapatite:body_html#b079` | article | Dental hypersensitivity occurs when gums pull away from the gum line, leaving the dentin exposed. I… | admin-held |  |
| 110 | `admin:article:news/nano-hydroxyapatite:body_html#b080` | article | Dentin contains tiny pores called dentinal tubules, which lead directly to dental pulp. This is the… | admin-held |  |
| 111 | `admin:article:news/nano-hydroxyapatite:body_html#b081` | article | With the enamel removed, the dentinal tubules’ nerve endings are exposed to hot, cold, and acidic f… | admin-held |  |
| 112 | `admin:article:news/nano-hydroxyapatite:body_html#b082` | article | Nano HAp has shown promising results when it comes to alleviating tooth sensitivity — something I’v… | admin-held |  |
| 113 | `admin:article:news/nano-hydroxyapatite:body_html#b083` | article | How Nano HAp Soothes Your Dental Hypersensitivity | admin-held |  |
| 114 | `admin:article:news/nano-hydroxyapatite:body_html#b084` | article | Nano HAp reduces sensitivity by occluding the open dentinal tubules. | admin-held |  |
| 115 | `admin:article:news/nano-hydroxyapatite:body_html#b085` | article | The nanocrystals that make up nano hydroxyapatite are hydrophilic. This means that it has hydrating… | admin-held |  |
| 116 | `admin:article:news/nano-hydroxyapatite:body_html#b086` | article | When it comes to exposed dentine, instead of numbing your nerves with potassium nitrate, nano HAp a… | admin-held |  |
| 117 | `admin:article:news/nano-hydroxyapatite:body_html#b087` | article | After using Karmicare nano hydroxyapatite toothpaste, the toughness of your enamel will noticeably … | admin-held |  |
| 118 | `admin:article:news/nano-hydroxyapatite:body_html#b088` | article | Nano HAp plugs the exposed dentin with deposits of hydroxyapatite nanoparticles. This works as a pr… | admin-held |  |
| 119 | `admin:article:news/nano-hydroxyapatite:body_html#b089` | article | Using a toothpaste with nano hydroxyapatite can make a significant difference in dentin hypersensit… | admin-held |  |
| 120 | `admin:article:news/nano-hydroxyapatite:body_html#b090` | article | 4. Nano Hydroxyapatite Protects Your Enamel From Acidic Food and Drinks | admin-held |  |
| 121 | `admin:article:news/nano-hydroxyapatite:body_html#b091` | article | Did you know that sour candies are as acidic as battery acid? | admin-held |  |
| 122 | `admin:article:news/nano-hydroxyapatite:body_html#b092` | article | Their pH levels are very similar. And yet, many adults and kids alike love snacking on bags of Sour… | admin-held |  |
| 123 | `admin:article:news/nano-hydroxyapatite:body_html#b093` | article | This is known as tooth erosion — it’s a gateway to a myriad of dental problems like developing an a… | admin-held |  |
| 124 | `admin:article:news/nano-hydroxyapatite:body_html#b094` | article | Eating sugary food holds the same fate for our teeth. The harmful microbes in your mouth digest the… | admin-held |  |
| 125 | `admin:article:news/nano-hydroxyapatite:body_html#b095` | article | Wiping out all bacteria isn’t the solution because good bacteria are necessary to keep your oral fl… | admin-held |  |
| 126 | `admin:article:news/nano-hydroxyapatite:body_html#b096` | article | Most oral care ingredients, like fluoride, chlorhexidine, stannous salts, and quaternary ammonium s… | admin-held |  |
| 127 | `admin:article:news/nano-hydroxyapatite:body_html#b097` | article | We suggest you avoid toothpaste or mouthwash formulations that contain fluoride and these other ing… | admin-held |  |
| 128 | `admin:article:news/nano-hydroxyapatite:body_html#b098` | article | How Nano HAp Protects You Against Erosion | admin-held |  |
| 129 | `admin:article:news/nano-hydroxyapatite:body_html#b099` | article | Nano hydroxyapatite shields your teeth from acid erosion while also restoring their structure from … | admin-held |  |
| 130 | `admin:article:news/nano-hydroxyapatite:body_html#b100` | article | It remineralizes the enamel by reconstructing the lost deposits of calcium and phosphate, while als… | admin-held |  |
| 131 | `admin:article:news/nano-hydroxyapatite:body_html#b101` | article | This reduces the likelihood of your teeth getting attacked by the harmful acids produced by bad bac… | admin-held |  |
| 132 | `admin:article:news/nano-hydroxyapatite:body_html#b102` | article | Your Toothpaste Matters More Than You Think | admin-held |  |
| 133 | `admin:article:news/nano-hydroxyapatite:body_html#b103` | article | The saying, “As within, so without. As above, so below” is ancient wisdom. It’s what we believe and… | admin-held |  |
| 134 | `admin:article:news/nano-hydroxyapatite:body_html#b104` | article | This is because your oral health is priceless to your overall well-being. | admin-held |  |
| 135 | `admin:article:news/nano-hydroxyapatite:body_html#b105` | article | Even a slight deviation from the normal puts you at a high risk for a myriad of medical disorders, … | admin-held |  |
| 136 | `admin:article:news/nano-hydroxyapatite:body_html#b106` | article | In fact, compromised oral health increases the mortality rate among the most vulnerable population … | admin-held |  |
| 137 | `admin:article:news/nano-hydroxyapatite:body_html#b107` | article | Your oral health is in your hands. Although open access to the best medical care is everyone’s birt… | admin-held |  |
| 138 | `admin:article:news/nano-hydroxyapatite:body_html#b108` | article | Sadly, universal dental care is still a far-fetched dream in many parts of the world, like the U.S.… | admin-held |  |
| 139 | `admin:article:news/nano-hydroxyapatite:body_html#b109` | article | The problem is made worse by the fact that most commercially available toothpaste does a poor job a… | admin-held |  |
| 140 | `admin:article:news/nano-hydroxyapatite:body_html#b110` | article | And if your toothpaste contains fluoride, sodium laureth sulfate (SLS), saccharin, or triclosan, yo… | admin-held |  |
| 141 | `admin:article:news/nano-hydroxyapatite:body_html#b111` | article | Karmicare Biorhythmic nano HAp toothpaste, on the other hand, repairs and strengthens your teeth, b… | admin-held |  |
| 142 | `admin:article:news/nano-hydroxyapatite:body_html#b112` | article | It’s nontoxic, highly effective, and has zero side effects. In fact, your toddler could swallow it … | admin-held |  |
| 143 | `admin:article:news/nano-hydroxyapatite:body_html#b113` | article | Did you know? Switching to a nano HAp toothpaste is the smartest decision you can make for you and … | admin-held |  |
| 144 | `admin:article:news/nano-hydroxyapatite:body_html#b114` | article | Where and How Do You Add Nano-HAp to Your Routine? | admin-held |  |
| 145 | `admin:article:news/nano-hydroxyapatite:body_html#b115` | article | The best way to use nano HAp is in a specially formulated toothpaste. We suggest our Biorhythmic Or… | admin-held |  |
| 146 | `admin:article:news/nano-hydroxyapatite:body_html#b116` | article | Keep in mind that while there are several toothpastes made with nano hydroxyapatite, some of those … | admin-held |  |
| 147 | `admin:article:news/nano-hydroxyapatite:body_html#b117` | article | Brush your teeth mindfully for at least 2 minutes twice a day. Then, leave nano HAp toothpaste in y… | admin-held |  |
| 148 | `admin:article:news/nano-hydroxyapatite:seo.title` | article | Why you need Nano Hydroxapatite in your toothpaste – KARMICARE | admin-held |  |
| 149 | `admin:article:news/nano-hydroxyapatite:seo.description` | article | Here's everything you need to know about nano-hydroxyapatite, a medical marvel ingredient for bette… | admin-held |  |
| 150 | `admin:article:news/morning-and-night-time-brushing-why-timing-matters:text#01` | article | [img alt] Brushing Your Teeth Both Morning and Night Is Important For Your Oral Health. | admin-held |  |
| 151 | `admin:article:news/morning-and-night-time-brushing-why-timing-matters:body_html#b001` | article | Oral hygiene is more than just a daily ritual. It is a vital aspect of your overall health and well… | admin-held |  |
| 152 | `admin:article:news/morning-and-night-time-brushing-why-timing-matters:body_html#b002` | article | Does the timing of brushing matter? | admin-held |  |
| 153 | `admin:article:news/morning-and-night-time-brushing-why-timing-matters:body_html#b003` | article | This guide will explore why brushing in the morning and at night is crucial, and how timing impacts… | admin-held |  |
| 154 | `admin:article:news/morning-and-night-time-brushing-why-timing-matters:body_html#b004` | article | Why Brushing in the Morning is Important | admin-held |  |
| 155 | `admin:article:news/morning-and-night-time-brushing-why-timing-matters:body_html#b005` | article | Brushing your teeth in the morning is often the first thing people do. No one wants to start the da… | admin-held |  |
| 156 | `admin:article:news/morning-and-night-time-brushing-why-timing-matters:body_html#b006` | article | Freshens Breath After a Night's Sleep | admin-held |  |
| 157 | `admin:article:news/morning-and-night-time-brushing-why-timing-matters:body_html#b007` | article | Saliva acts as a natural cleanser for your mouth. But during sleep, saliva production reduces. This… | admin-held |  |
| 158 | `admin:article:news/morning-and-night-time-brushing-why-timing-matters:body_html#b008` | article | Removes Plaque and Bacteria That Build-up Overnight | admin-held |  |
| 159 | `admin:article:news/morning-and-night-time-brushing-why-timing-matters:body_html#b009` | article | Bacteria forms a sticky, colourless film called plaque overnight. If left unchecked, plaque can har… | admin-held |  |
| 160 | `admin:article:news/morning-and-night-time-brushing-why-timing-matters:body_html#b010` | article | Protects Teeth All Day Long | admin-held |  |
| 161 | `admin:article:news/morning-and-night-time-brushing-why-timing-matters:body_html#b011` | article | Beyond simply cleaning your mouth, brushing in the morning protects your teeth throughout the day. … | admin-held |  |
| 162 | `admin:article:news/morning-and-night-time-brushing-why-timing-matters:body_html#b012` | article | The timing of your morning brushing can greatly affect its effectiveness. A common debate revolves … | admin-held |  |
| 163 | `admin:article:news/morning-and-night-time-brushing-why-timing-matters:body_html#b013` | article | 1. Brushing Before Breakfast | admin-held |  |
| 164 | `admin:article:news/morning-and-night-time-brushing-why-timing-matters:body_html#b014` | article | Brushing your teeth before breakfast removes overnight bacteria and plaque, which gives you a clean… | admin-held |  |
| 165 | `admin:article:news/morning-and-night-time-brushing-why-timing-matters:body_html#b015` | article | 2. Brushing After Breakfast | admin-held |  |
| 166 | `admin:article:news/morning-and-night-time-brushing-why-timing-matters:body_html#b016` | article | Brushing after breakfast removes food particles and sugars. This can be especially important if you… | admin-held |  |
| 167 | `admin:article:news/morning-and-night-time-brushing-why-timing-matters:body_html#b017` | article | Why is Nighttime Brushing Important? | admin-held |  |
| 168 | `admin:article:news/morning-and-night-time-brushing-why-timing-matters:body_html#b018` | article | It is important to start your day with a healthy, clean mouth. | admin-held |  |
| 169 | `admin:article:news/morning-and-night-time-brushing-why-timing-matters:body_html#b019` | article | While morning brushing is essential for starting your day with a clean mouth, night brushing is equ… | admin-held |  |
| 170 | `admin:article:news/morning-and-night-time-brushing-why-timing-matters:body_html#b020` | article | Removes Food Particles and Plaque | admin-held |  |
| 171 | `admin:article:news/morning-and-night-time-brushing-why-timing-matters:body_html#b021` | article | Throughout the day, your teeth are exposed to various foods, drinks, and environmental factors that… | admin-held |  |
| 172 | `admin:article:news/morning-and-night-time-brushing-why-timing-matters:body_html#b022` | article | Reduces Tooth Decay and Gum Disease | admin-held |  |
| 173 | `admin:article:news/morning-and-night-time-brushing-why-timing-matters:body_html#b023` | article | Skipping nighttime brushing allows bacteria to linger in your mouth. They produce acids that weaken… | admin-held |  |
| 174 | `admin:article:news/morning-and-night-time-brushing-why-timing-matters:body_html#b024` | article | Prevents Morning Breath | admin-held |  |
| 175 | `admin:article:news/morning-and-night-time-brushing-why-timing-matters:body_html#b025` | article | Bad breath is often caused by bacteria that accumulate in your mouth overnight. Night-time brushing… | admin-held |  |
| 176 | `admin:article:news/morning-and-night-time-brushing-why-timing-matters:body_html#b026` | article | Karmicare's Asleep Toothpaste , with valerian, hydroxyapatite, and medical-grade activated charcoal… | admin-held |  |
| 177 | `admin:article:news/morning-and-night-time-brushing-why-timing-matters:body_html#b027` | article | During the day, the Awake Toothpaste strengthens enamel and fights plaque, while at night, the Asle… | admin-held |  |
| 178 | `admin:article:news/morning-and-night-time-brushing-why-timing-matters:body_html#b028` | article | Brushing your teeth in the morning and at night is essential for keeping your teeth and gums health… | admin-held |  |
| 179 | `admin:article:news/morning-and-night-time-brushing-why-timing-matters:body_html#b029` | article | Brushing at the right time, using the right brushing techniques, and incorporating other oral hygie… | admin-held |  |
| 180 | `admin:article:news/morning-and-night-time-brushing-why-timing-matters:body_html#b030` | article | To upgrade your oral care routine, consider exploring Karmicare's range of products designed to sup… | admin-held |  |
| 181 | `admin:article:news/morning-and-night-time-brushing-why-timing-matters:seo.title` | article | Morning and Night Time Brushing: Why Timing Matters. – KARMICARE | admin-held |  |
| 182 | `admin:article:news/morning-and-night-time-brushing-why-timing-matters:seo.description` | article | Explore the benefits of morning and night brushing for optimal oral health. Learn why timing matter… | admin-held |  |
| 183 | `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:text#01` | article | [img alt] Nootropics Boost Mental Clarity | admin-held |  |
| 184 | `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:body_html#b001` | article | Self-reflection: | admin-held |  |
| 185 | `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:body_html#b002` | article | Can the toothpaste I use benefit both my oral and brain health? | admin-held |  |
| 186 | `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:body_html#b003` | article | Is there a toothpaste that could help me improve my mental performance? | admin-held |  |
| 187 | `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:body_html#b004` | article | Can brushing my teeth help me stay more active during the day or get better sleep at night? | admin-held |  |
| 188 | `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:body_html#b005` | article | Key takeaways: | admin-held |  |
| 189 | `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:body_html#b006` | article | Nootropics are substances that optimize brain functioning, making you smarter, focused, motivated, … | admin-held |  |
| 190 | `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:body_html#b007` | article | Nootropics are growing in popularity as people strive to improve their mental performance. | admin-held |  |
| 191 | `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:body_html#b008` | article | Consuming nootropics may help support better focus, memory, improved sleep quality, and reduced str… | admin-held |  |
| 192 | `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:body_html#b009` | article | We live in a busy and competitive world today in which peak mental performance is crucial. Being ab… | admin-held |  |
| 193 | `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:body_html#b010` | article | It's no surprise therefore that so many people are looking for ways to enhance their mental capabil… | admin-held |  |
| 194 | `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:body_html#b011` | article | If this is you, you might want to consider nootropics. Nootropics promise to make you smarter, shar… | admin-held |  |
| 195 | `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:body_html#b012` | article | This article will explore the benefits of nootropics, provide examples, and highlight where you can… | admin-held |  |
| 196 | `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:body_html#b013` | article | What Are Nootropics? | admin-held |  |
| 197 | `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:body_html#b014` | article | Nootropics are substances that may help improve cognitive functions including memory, focus, and mo… | admin-held |  |
| 198 | `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:body_html#b015` | article | Originally used to treat mental conditions like Alzheimer’s disease, stroke, narcolepsy, schizophre… | admin-held |  |
| 199 | `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:body_html#b016` | article | There is a growing interest in nootropics, especially as people seek natural ways to improve their … | admin-held |  |
| 200 | `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:body_html#b017` | article | 5 Benefits of Nootropics | admin-held |  |
| 201 | `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:body_html#b018` | article | Taking nootropics could have some positive effects on your health. Here are five benefits of nootro… | admin-held |  |
| 202 | `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:body_html#b019` | article | 1. Boost Cognitive Performance | admin-held |  |
| 203 | `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:body_html#b020` | article | One of the most common reasons people use nootropic supplements is to promote brain health. Researc… | admin-held |  |
| 204 | `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:body_html#b021` | article | Nootropics may enhance mental performance because they: | admin-held |  |
| 205 | `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:body_html#b022` | article | Improve blood flow to the brain | admin-held |  |
| 206 | `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:body_html#b023` | article | Stimulate the action of neurotransmitters such as glutamate by binding to their receptors | admin-held |  |
| 207 | `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:body_html#b024` | article | Suppress depressant neurotransmitters such as GABA (a chemical in your brain that helps you relax, … | admin-held |  |
| 208 | `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:body_html#b025` | article | Apart from boosting mental performance, nootropics may also slow down age-related cognitive decline… | admin-held |  |
| 209 | `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:body_html#b026` | article | An excellent, regular source of nootropics is Karmicare’s Awake Morning toothpaste . Awake Morning … | admin-held |  |
| 210 | `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:body_html#b027` | article | Infused with lime and mint flavors, Awake Morning toothpaste tastes and smells zesty and fresh, giv… | admin-held |  |
| 211 | `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:body_html#b028` | article | 2. Improve Sleep Quality | admin-held |  |
| 212 | `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:body_html#b029` | article | Good sleep is essential for your physical and mental health. Taking a nootropic could help you slee… | admin-held |  |
| 213 | `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:body_html#b030` | article | Research published in the National Library of Medicine supports the use of nootropics like valerian… | admin-held |  |
| 214 | `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:body_html#b031` | article | This sets the stage for quality sleep. A good night’s sleep comes with other cognitive benefits suc… | admin-held |  |
| 215 | `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:body_html#b032` | article | Again, with Karmicare’s Asleep evening toothpaste , you can enjoy the best quality sleep just by br… | admin-held |  |
| 216 | `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:body_html#b033` | article | 3. Increase Attention Span and Concentration | admin-held |  |
| 217 | `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:body_html#b034` | article | Scientists have proven that nootropics can enhance attention and concentration in kids with attenti… | admin-held |  |
| 218 | `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:body_html#b035` | article | Aside from their clinical indications, you can use nootropics to enhance your focus and concentrati… | admin-held |  |
| 219 | `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:body_html#b036` | article | In recent times, the internet has popularised the use of nootropics as “study drugs” because they e… | admin-held |  |
| 220 | `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:body_html#b037` | article | These drugs modify the levels of neurotransmitters such as dopamine and GABA. By doing so, they imp… | admin-held |  |
| 221 | `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:body_html#b038` | article | However, it is important to note that you are more likely to experience side effects while using th… | admin-held |  |
| 222 | `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:body_html#b039` | article | Natural nootropics are the safer alternative because they are free from toxic synthetic compounds a… | admin-held |  |
| 223 | `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:body_html#b040` | article | 4. Ease Stress and Boost Mood | admin-held |  |
| 224 | `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:body_html#b041` | article | Nootropics can boost your mood and reduce the symptoms of mental anxiety and stress. This is mainly… | admin-held |  |
| 225 | `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:body_html#b042` | article | Dopamine is the brain’s “reward chemical” and is closely linked to feelings of contentment and plea… | admin-held |  |
| 226 | `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:body_html#b043` | article | Nootropics Help Improve Mental Fatigue | admin-held |  |
| 227 | `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:body_html#b044` | article | 5. Reduce Mental Fatigue | admin-held |  |
| 228 | `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:body_html#b045` | article | Your brain is a busy factory that uses a lot of energy. It’s common to feel mentally drained to the… | admin-held |  |
| 229 | `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:body_html#b046` | article | Taking nootropics help keep you moving. | admin-held |  |
| 230 | `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:body_html#b047` | article | Nootropics improve blood flow to your brain. | admin-held |  |
| 231 | `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:body_html#b048` | article | Facilitate energy production by your brain cells. | admin-held |  |
| 232 | `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:body_html#b049` | article | Reduce stress hormones that cause fatigue. | admin-held |  |
| 233 | `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:body_html#b050` | article | By relieving brain fatigue, they supercharge your performance and improve your overall quality of l… | admin-held |  |
| 234 | `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:body_html#b051` | article | Where to Find Nootropics in Everyday Products | admin-held |  |
| 235 | `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:body_html#b052` | article | If you’re ready to boost your brain power, mood, sleep quality, and focus, here are a few rich sour… | admin-held |  |
| 236 | `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:body_html#b053` | article | 1. Guarana | admin-held |  |
| 237 | `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:body_html#b054` | article | Guarana, also known as Paullinia cupana , is a Brazilian plant found mostly within the Amazon basin… | admin-held |  |
| 238 | `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:body_html#b055` | article | Guarana is famous for its health benefits. For millennia, Amazonian tribes have used guarana powder… | admin-held |  |
| 239 | `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:body_html#b056` | article | Guarana extract is rich in stimulants such as caffeine, theophylline, and theobromine. | admin-held |  |
| 240 | `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:body_html#b057` | article | The health benefits of guarana are: | admin-held |  |
| 241 | `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:body_html#b058` | article | Improves brain power: Guarana consumption has been shown to boost learning and memory . A study com… | admin-held |  |
| 242 | `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:body_html#b059` | article | Lowers the risk of heart disease: Similar to green tea, guarana contains antioxidants like tannins,… | admin-held |  |
| 243 | `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:body_html#b060` | article | May promote weight loss: Guarana may help you lose weight and avoid obesity. Studies show that comp… | admin-held |  |
| 244 | `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:body_html#b061` | article | May reduce mental fatigue and help you focus: Guarana is an awesome source of caffeine. Caffeine ha… | admin-held |  |
| 245 | `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:body_html#b062` | article | Without a doubt, guarana is one of those healthy foods you want to consume to help you improve both… | admin-held |  |
| 246 | `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:body_html#b063` | article | But since guarana is mainly added to energy drinks and soft drinks, you risk consuming too much pro… | admin-held |  |
| 247 | `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:body_html#b064` | article | So where can you find a healthy and regular source of guarana in everyday products? | admin-held |  |
| 248 | `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:body_html#b065` | article | Toothpaste is an easy and effective means to add guarana to your routine. Karmicare’s Awake Morning… | admin-held |  |
| 249 | `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:body_html#b066` | article | For a boost of guarana, choose Karmicare’s Awake Morning toothpaste to ensure you don’t miss out on… | admin-held |  |
| 250 | `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:body_html#b067` | article | 2. Valerian | admin-held |  |
| 251 | `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:body_html#b068` | article | Valerian is an herb native to Europe and Northern Asia. It’s a common herbal nootropic used to indu… | admin-held |  |
| 252 | `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:body_html#b069` | article | Research shows that taking valerian can help you fall asleep faster and stay asleep longer. In addi… | admin-held |  |
| 253 | `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:body_html#b070` | article | Apart from promoting healthy sleep, valerian helps to reduce stress and anxiety. We've all had thos… | admin-held |  |
| 254 | `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:body_html#b071` | article | Valerian-infused Asleep Evening toothpaste from Karmicare will help you drift into slumberland in n… | admin-held |  |
| 255 | `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:body_html#b072` | article | With superior minerals like nano HAp along with active nootropics, Karmicare helps you achieve an o… | admin-held |  |
| 256 | `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:body_html#b073` | article | Unlike fluoride-based oral hygiene products that disturb your wake/sleep cycles, Karmicare actually… | admin-held |  |
| 257 | `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:body_html#b074` | article | 3. Caffeine | admin-held |  |
| 258 | `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:body_html#b075` | article | You’ve probably used caffeine before to stay alert and enhance your performance. Caffeine boosts th… | admin-held |  |
| 259 | `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:body_html#b076` | article | Common sources of caffeine include coffee, tea, guarana, soda, and energy drinks. While taking caff… | admin-held |  |
| 260 | `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:body_html#b077` | article | Other nootropics you should take note of are: | admin-held |  |
| 261 | `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:body_html#b078` | article | L-theanine: Found in tea, L-theanine will help you improve your cognitive performance, boost your i… | admin-held |  |
| 262 | `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:body_html#b079` | article | Creatine: Creatine supplements are mainly used by athletes because they enhance athletic performanc… | admin-held |  |
| 263 | `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:body_html#b080` | article | Bacopa monnieri: This is an herb that may also boost brain function, reduce anxiety, and ease infla… | admin-held |  |
| 264 | `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:body_html#b081` | article | Panax ginseng: Panax ginseng is considered an adaptogen. Adaptogens are substances that are believe… | admin-held |  |
| 265 | `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:body_html#b082` | article | Ginkgo biloba: Ginkgo biloba extract may improve cardiovascular health, reduce inflammation, enhanc… | admin-held |  |
| 266 | `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:body_html#b083` | article | Rhodiola rosea: Also an adaptogen, rhodiola rosea may help manage stress and anxiety, reduce the sy… | admin-held |  |
| 267 | `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:body_html#b084` | article | Are Nootropics Safe to Use? | admin-held |  |
| 268 | `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:body_html#b085` | article | Yes. Nootropics are safe to use in the correct dosage and with guidance from a health care provider. | admin-held |  |
| 269 | `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:body_html#b086` | article | It’s important to note that prescription and over-the-counter nootropics will almost always have si… | admin-held |  |
| 270 | `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:body_html#b087` | article | The potential side effects of nootropics are: | admin-held |  |
| 271 | `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:body_html#b088` | article | High blood pressure | admin-held |  |
| 272 | `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:body_html#b089` | article | Increased heart rate | admin-held |  |
| 273 | `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:body_html#b090` | article | Addiction | admin-held |  |
| 274 | `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:body_html#b091` | article | Insomnia | admin-held |  |
| 275 | `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:body_html#b092` | article | Natural nootropics are generally safer because their actions in the body are more subtle compared t… | admin-held |  |
| 276 | `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:body_html#b093` | article | In the U.S., for example, the FDA regulates dietary supplements differently from other foods and dr… | admin-held |  |
| 277 | `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:body_html#b094` | article | Bottomline | admin-held |  |
| 278 | `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:body_html#b095` | article | Nootropics are substances that improve cognitive function. They can be used to improve memory, focu… | admin-held |  |
| 279 | `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:body_html#b096` | article | Generally, natural nootropics are safer than drugs because they are less likely to cause side effec… | admin-held |  |
| 280 | `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:body_html#b097` | article | If you’re looking for a healthy, mild/moderate source of nootropics, choose Karmicare’s Biorhythmic… | admin-held |  |
| 281 | `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:seo.title` | article | Benefits of Nootropics: Ease Stress, Boost Focus and Improve Mood. – KARMICARE | admin-held |  |
| 282 | `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:seo.description` | article | Self-reflection: Can the toothpaste I use benefit both my oral and brain health? Is there a toothpa… | admin-held |  |
| 283 | `admin:article:news/nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste:text#01` | article | [img alt] Nano-Hydroxyapatite Is an Effective Remineralizing Agent | admin-held |  |
| 284 | `admin:article:news/nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste:body_html#b001` | article | Self-reflection: | admin-held |  |
| 285 | `admin:article:news/nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste:body_html#b002` | article | Does my toothpaste support my oral health? | admin-held |  |
| 286 | `admin:article:news/nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste:body_html#b003` | article | How can my morning and evening oral care routine nourish my body? | admin-held |  |
| 287 | `admin:article:news/nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste:body_html#b004` | article | Is there a way to safely remineralize my teeth and enhance my smile? | admin-held |  |
| 288 | `admin:article:news/nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste:body_html#b005` | article | Key takeaways: | admin-held |  |
| 289 | `admin:article:news/nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste:body_html#b006` | article | Nano hydroxyapatite has powerful remineralizing effects on tooth enamel lesions and is safe, non-to… | admin-held |  |
| 290 | `admin:article:news/nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste:body_html#b007` | article | Research shows that nano-hydroxyapatite is an effective remineralizing agent. | admin-held |  |
| 291 | `admin:article:news/nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste:body_html#b008` | article | Using natural toothpaste with nano-hydroxyapatite helps prevent tooth decay, whitens teeth without … | admin-held |  |
| 292 | `admin:article:news/nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste:body_html#b009` | article | 10-Second Nano HAp Need-to-Know Truths | admin-held |  |
| 293 | `admin:article:news/nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste:body_html#b010` | article | Nano HAp deeply penetrates your enamel to refill lost minerals every time you brush your teeth. | admin-held |  |
| 294 | `admin:article:news/nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste:body_html#b011` | article | It smoothes and whitens teeth by gently repairing them with native minerals. | admin-held |  |
| 295 | `admin:article:news/nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste:body_html#b012` | article | It plugs exposed dentin tubules, effectively reducing tooth sensitivity | admin-held |  |
| 296 | `admin:article:news/nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste:body_html#b013` | article | It protects against tooth decay by providing total protection against harmful dietary acids. | admin-held |  |
| 297 | `admin:article:news/nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste:body_html#b014` | article | It supports bone health and is completely non-toxic. | admin-held |  |
| 298 | `admin:article:news/nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste:body_html#b015` | article | What is Nano Hydroxyapatite? | admin-held |  |
| 299 | `admin:article:news/nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste:body_html#b016` | article | We get it. Nano-hydroxyapatite is a bit of a mouthful. | admin-held |  |
| 300 | `admin:article:news/nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste:body_html#b017` | article | But while it may seem strange to you, your body is familiar with this magic mineral. | admin-held |  |
| 301 | `admin:article:news/nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste:body_html#b018` | article | Hydroxyapatite (HA) is a natural form of calcium that makes up 97% of your tooth enamel, 70% of den… | admin-held |  |
| 302 | `admin:article:news/nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste:body_html#b019` | article | It’s an excellent alternative to fluoride in toothpaste. In modern dentistry, HA keeps your bones a… | admin-held |  |
| 303 | `admin:article:news/nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste:body_html#b020` | article | This article will give you an insight into nano-hydroxyapatite; what it is and why it is superior f… | admin-held |  |
| 304 | `admin:article:news/nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste:body_html#b021` | article | Why Nano-Hydroxyapatite is Better | admin-held |  |
| 305 | `admin:article:news/nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste:body_html#b022` | article | Nano-hydroxyapatite (nano HAp) is a smaller, more effective form that naturally fuses with hydroxya… | admin-held |  |
| 306 | `admin:article:news/nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste:body_html#b023` | article | Recent studies show that nano HAp builds a stronger structure that resists acid attacks more effect… | admin-held |  |
| 307 | `admin:article:news/nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste:body_html#b024` | article | Key Benefits of Nano-Hydroxyapatite. | admin-held |  |
| 308 | `admin:article:news/nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste:body_html#b025` | article | Biocompatible — It works well with your body’s tissues. | admin-held |  |
| 309 | `admin:article:news/nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste:body_html#b026` | article | Bioactive — Your body can easily absorb and use nano HAp. | admin-held |  |
| 310 | `admin:article:news/nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste:body_html#b027` | article | Osteoconductive — It supports and guides the growth of new bone. | admin-held |  |
| 311 | `admin:article:news/nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste:body_html#b028` | article | Nontoxic — Since your body naturally produces hydroxyapatite, nano HAp causes no harmful reactions … | admin-held |  |
| 312 | `admin:article:news/nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste:body_html#b029` | article | Nano hydroxyapatite has an interesting history that spans four decades. NASA invented the first ver… | admin-held |  |
| 313 | `admin:article:news/nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste:body_html#b030` | article | Why would a space agency spend time creating nano HAp? | admin-held |  |
| 314 | `admin:article:news/nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste:body_html#b031` | article | Astronauts returning home from space experienced mineral loss from teeth and bones due to prolonged… | admin-held |  |
| 315 | `admin:article:news/nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste:body_html#b032` | article | With the help of nanotechnology, scientists turned hydroxyapatite into tiny particles that actively… | admin-held |  |
| 316 | `admin:article:news/nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste:body_html#b033` | article | Since then, nano HAp has become a staple in toothpaste and dental products, especially in Japan and… | admin-held |  |
| 317 | `admin:article:news/nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste:body_html#b034` | article | 4 Powerful Benefits of Nano Hydroxyapatite | admin-held |  |
| 318 | `admin:article:news/nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste:body_html#b035` | article | Nano Hap Strengthens and Remineralize the Tooth Enamel | admin-held |  |
| 319 | `admin:article:news/nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste:body_html#b036` | article | 1. Repairs Teeth From the Inside | admin-held |  |
| 320 | `admin:article:news/nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste:body_html#b037` | article | Your teeth have tiny holes called dentin tubules under your enamel. Minerals and other substances, … | admin-held |  |
| 321 | `admin:article:news/nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste:body_html#b038` | article | When you eat sugary foods, bacteria process the sugar and release acids as waste products. These ac… | admin-held |  |
| 322 | `admin:article:news/nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste:body_html#b039` | article | FYI: The pH level in Karmicare Biorhythmic Oral Health (both the Awake and Asleep formulations) is … | admin-held |  |
| 323 | `admin:article:news/nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste:body_html#b040` | article | Since enamel isn’t a living tissue, it cannot regrow. However, slight damage can be repaired throug… | admin-held |  |
| 324 | `admin:article:news/nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste:body_html#b041` | article | Saliva helps by neutralizing acids and restoring calcium and phosphate to teeth. However, saliva is… | admin-held |  |
| 325 | `admin:article:news/nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste:body_html#b042` | article | It does this by bonding with your teeth, replacing lost minerals, and strengthening weak enamel. Na… | admin-held |  |
| 326 | `admin:article:news/nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste:body_html#b043` | article | It also fills up microscopic cracks in the enamel. | admin-held |  |
| 327 | `admin:article:news/nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste:body_html#b044` | article | 2. Nano Hydroxyapatite Whitens Your Teeth Without Hurting Your Enamel | admin-held |  |
| 328 | `admin:article:news/nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste:body_html#b045` | article | Stained yellow teeth are embarrassing. Most whitening products available only give temporary result… | admin-held |  |
| 329 | `admin:article:news/nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste:body_html#b046` | article | Bleaching agents like hydrogen peroxide whiten teeth but often cause tooth sensitivity and chemical… | admin-held |  |
| 330 | `admin:article:news/nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste:body_html#b047` | article | So while you’ll have whiter teeth, they’ll become sensitive and cause pain when you’re eating or dr… | admin-held |  |
| 331 | `admin:article:news/nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste:body_html#b048` | article | Nano HAp offers a better solution, naturally whitening teeth without harsh chemicals. It fills the … | admin-held |  |
| 332 | `admin:article:news/nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste:body_html#b049` | article | 3. Nano Hydroxyapatite Reduces Your Tooth Hypersensitivity by Blocking Dentinal Tubules | admin-held |  |
| 333 | `admin:article:news/nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste:body_html#b050` | article | Tooth sensitivity occurs when your gum pulls away and exposes your dentin. Dentin contains tubules … | admin-held |  |
| 334 | `admin:article:news/nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste:body_html#b051` | article | Dental hypersensitivity is often triggered by brushing or flossing. This condition frustrates denti… | admin-held |  |
| 335 | `admin:article:news/nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste:body_html#b052` | article | According to dental professionals, nano HAp toothpaste is more effective in preventing cavities and… | admin-held |  |
| 336 | `admin:article:news/nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste:body_html#b053` | article | Nano HAp has shown promising results in alleviating tooth sensitivity — something I’ve experienced … | admin-held |  |
| 337 | `admin:article:news/nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste:body_html#b054` | article | Nano Hap gets Rid of Teeth Sensitivity | admin-held |  |
| 338 | `admin:article:news/nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste:body_html#b055` | article | Nano HAp reduces sensitivity by blocking the open dentinal tubules in teeth. The nanocrystals that … | admin-held |  |
| 339 | `admin:article:news/nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste:body_html#b056` | article | 4. Nano Hydroxyapatite Protects Your Enamel From Acidic Food and Drinks | admin-held |  |
| 340 | `admin:article:news/nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste:body_html#b057` | article | Foods like citrus, soda, lemon, tomatoes, and candy are highly acidic. They slowly chip away the en… | admin-held |  |
| 341 | `admin:article:news/nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste:body_html#b058` | article | Wiping out all bacteria isn't the solution because good bacteria are necessary to keep oral flora b… | admin-held |  |
| 342 | `admin:article:news/nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste:body_html#b059` | article | Nano hydroxyapatite forms a protective layer on your teeth. It also rebuilds lost calcium and phosp… | admin-held |  |
| 343 | `admin:article:news/nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste:body_html#b060` | article | This reduces the likelihood of harmful acids attacking your teeth. | admin-held |  |
| 344 | `admin:article:news/nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste:body_html#b061` | article | Your Toothpaste Matters More Than You Think | admin-held |  |
| 345 | `admin:article:news/nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste:body_html#b062` | article | Your oral health is priceless to your overall well-being. | admin-held |  |
| 346 | `admin:article:news/nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste:body_html#b063` | article | Minor oral health issues can lead to serious health issues like heart disease, pneumonia, and even … | admin-held |  |
| 347 | `admin:article:news/nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste:body_html#b064` | article | Most oral care products do little to protect your teeth. Many contain harmful ingredients like fluo… | admin-held |  |
| 348 | `admin:article:news/nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste:body_html#b065` | article | Karmicare Biorhythmic nano HAp toothpaste is your surest bet. It is safe for all ages, even your to… | admin-held |  |
| 349 | `admin:article:news/nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste:body_html#b066` | article | Did you know? Switching to a nano HAp toothpaste is the smartest decision you can make for your and… | admin-held |  |
| 350 | `admin:article:news/nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste:body_html#b067` | article | Shop Now to Transform Your Oral Health! | admin-held |  |
| 351 | `admin:article:news/nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste:body_html#b068` | article | How To Use Nano Hydroxyapatite | admin-held |  |
| 352 | `admin:article:news/nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste:body_html#b069` | article | The best way to use nano HAp is in a specially formulated toothpaste. | admin-held |  |
| 353 | `admin:article:news/nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste:body_html#b070` | article | We suggest our Biorhythmic Oral Hygiene Set . It combines nano HAp with health-conscious, low-abras… | admin-held |  |
| 354 | `admin:article:news/nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste:body_html#b071` | article | We also include herbs like guarana for energy in the morning and valerian to help you unwind at nig… | admin-held |  |
| 355 | `admin:article:news/nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste:body_html#b072` | article | Not all nano-hydroxyapatite toothpaste are the same. Some contain fluoride and other questionable i… | admin-held |  |
| 356 | `admin:article:news/nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste:body_html#b073` | article | For best results, brush your teeth mindfully for at least 2 minutes twice daily. Then, leave nano H… | admin-held |  |
| 357 | `admin:article:news/nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste:body_html#b074` | article | Note: Never, ever do this with fluoride toothpaste! | admin-held |  |
| 358 | `admin:article:news/nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste:seo.title` | article | Nano-Hydroxyapatite and Why You Need It In Your Toothpaste. – KARMICARE | admin-held |  |
| 359 | `admin:article:news/nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste:seo.description` | article | Self-reflection: Does my toothpaste support my oral health? How can my morning and evening oral car… | admin-held |  |
| 360 | `admin:article:news/how-oral-health-impacts-your-overall-wellness:text#01` | article | [img alt] Oral Health Impacts Physical Health | admin-held |  |
| 361 | `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b001` | article | Self Reflection Questions: | admin-held |  |
| 362 | `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b002` | article | How does my current oral care routine make me feel? | admin-held |  |
| 363 | `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b003` | article | Do I feel confident about the ingredients that make up my toothpaste, floss, etc? | admin-held |  |
| 364 | `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b004` | article | What changes can I make to my oral care routine to improve my health? | admin-held |  |
| 365 | `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b005` | article | Key Takeaways: | admin-held |  |
| 366 | `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b006` | article | Why is oral hygiene important? | admin-held |  |
| 367 | `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b007` | article | Did you know oral health directly impacts your mental, physical, and social well-being? | admin-held |  |
| 368 | `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b008` | article | How would this knowledge affect your routine and the products you use? | admin-held |  |
| 369 | `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b009` | article | Why Oral Hygiene is Important | admin-held |  |
| 370 | `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b010` | article | Oral care has always been perceived as a routine task limited to brushing, flossing, and occasional… | admin-held |  |
| 371 | `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b011` | article | Consequently, we associate a healthy mouth with cosmetic benefits like fresh breath and a bright sm… | admin-held |  |
| 372 | `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b012` | article | However, emerging research reveals that oral health has far-reaching implications that affect our p… | admin-held |  |
| 373 | `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b013` | article | An understanding of this connection is crucial to attaining general wellness. | admin-held |  |
| 374 | `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b014` | article | Including oral care in your overall wellness strategy goes beyond preventing cavities and having fr… | admin-held |  |
| 375 | `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b015` | article | Therefore, the toothpaste we use is not merely a cosmetic product but a critical component of our o… | admin-held |  |
| 376 | `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b016` | article | In this article, we will explore the deep connection between oral health and general health. We wil… | admin-held |  |
| 377 | `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b017` | article | How is oral health linked to mental health? | admin-held |  |
| 378 | `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b018` | article | Your Mental Health is Linked to Your Oral Health | admin-held |  |
| 379 | `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b019` | article | The link between oral health and mental wellness runs deeper than we realize. Studies have shown th… | admin-held |  |
| 380 | `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b020` | article | Cognitive decline. | admin-held |  |
| 381 | `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b021` | article | Reduced mental clarity. | admin-held |  |
| 382 | `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b022` | article | Depression. | admin-held |  |
| 383 | `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b023` | article | Anxiety. | admin-held |  |
| 384 | `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b024` | article | The primary process through which this occurs is inflammation; swelling and irritation in the gum. … | admin-held |  |
| 385 | `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b025` | article | This inflammation does not remain within the mouth but spreads throughout the body, causing widespr… | admin-held |  |
| 386 | `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b026` | article | Research has demonstrated that individuals with chronic gum disease are more likely to experience c… | admin-held |  |
| 387 | `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b027` | article | A recent study has found that fluoride, a standard ingredient in most conventional toothpastes, is … | admin-held |  |
| 388 | `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b028` | article | This simply implies a substance that is poisonous to the brain, spinal cord, and nervous system. It… | admin-held |  |
| 389 | `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b029` | article | Furthermore, recent research links poor oral health conditions such as gum disease to anxiety and d… | admin-held |  |
| 390 | `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b030` | article | This is sure to lead to worsened conditions like gum disease and tooth decay which further intensif… | admin-held |  |
| 391 | `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b031` | article | We advise a mindful oral care routine with products designed to support mental clarity and reduce s… | admin-held |  |
| 392 | `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b032` | article | “Chronic gum disease has been shown to increase the risk of cognitive decline over ten years” | admin-held |  |
| 393 | `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b033` | article | How is oral health linked to physical health? | admin-held |  |
| 394 | `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b034` | article | Your Physical Health Depends On Your Oral Health | admin-held |  |
| 395 | `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b035` | article | Oral health is an integral component of physical wellness. The oral cavity is not an isolated organ… | admin-held |  |
| 396 | `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b036` | article | For instance, The American Heart Association reports that gum disease is a significant risk factor … | admin-held |  |
| 397 | `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b037` | article | Bacteria from gum infections can penetrate the bloodstream and induce inflammation of the blood ves… | admin-held |  |
| 398 | `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b038` | article | Plaque can also obstruct blood flow. This increases the risk of heart attack and stroke. | admin-held |  |
| 399 | `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b039` | article | Gum infection is also linked to diabetes. | admin-held |  |
| 400 | `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b040` | article | An infection in the gum can make it difficult for individuals battling with diabetes to control the… | admin-held |  |
| 401 | `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b041` | article | According to the American Diabetes Association , individuals with diabetes are more prone to severa… | admin-held |  |
| 402 | `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b042` | article | Research in Diabetes Care found that individuals with periodontal disease find it more difficult to… | admin-held |  |
| 403 | `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b043` | article | This shows the importance of maintaining good oral health for overall physical wellness. | admin-held |  |
| 404 | `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b044` | article | How is oral health linked with social Well-being? | admin-held |  |
| 405 | `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b045` | article | Although often overlooked, oral health plays an important role in social wellness. The state of you… | admin-held |  |
| 406 | `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b046` | article | Oral health problems such as bad breath or stained teeth often lead to social anxiety. This conditi… | admin-held |  |
| 407 | `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b047` | article | According to The Society of Personality and Social Psychology , individuals with healthy and attrac… | admin-held |  |
| 408 | `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b048` | article | In contrast, issues such as bad breath and visible decay are associated with feelings of embarrassm… | admin-held |  |
| 409 | `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b049` | article | The American Dental Association found that 28% of young adults feel that the appearance of their te… | admin-held |  |
| 410 | `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b050` | article | This shows the crucial role of oral care in maintaining social relationships. | admin-held |  |
| 411 | `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b051` | article | “People with healthy, attractive smiles are viewed more favorably in both personal and professional… | admin-held |  |
| 412 | `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b052` | article | Why does your toothpaste matter? | admin-held |  |
| 413 | `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b053` | article | As established in the previous paragraphs, oral hygiene is a key component of a holistic approach t… | admin-held |  |
| 414 | `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b054` | article | The primary oral hygiene practices that ensure this care are brushing, flossing, and doing so frequ… | admin-held |  |
| 415 | `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b055` | article | Therefore, toothpaste should not be regarded merely as a cosmetic product but as an essential instr… | admin-held |  |
| 416 | `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b056` | article | Choose products made with nontoxic, natural ingredients that support a holistic approach to oral ca… | admin-held |  |
| 417 | `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b057` | article | Building on the aforementioned connections to holistic health, the right toothpaste should support … | admin-held |  |
| 418 | `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b058` | article | Toothpaste formulated with nootropics like guarana sets the foundation for a productive day by enha… | admin-held |  |
| 419 | `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b059` | article | Calming ingredients like valerian support relaxation and improve sleep quality. | admin-held |  |
| 420 | `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b060` | article | Sleep plays an instrumental role in mental wellness by giving the brain enough time to rest, repair… | admin-held |  |
| 421 | `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b061` | article | Given the adverse effects of fluoride on cognitive function and other vital systems, it is only log… | admin-held |  |
| 422 | `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b062` | article | Furthermore, your toothpaste should support your physical health. | admin-held |  |
| 423 | `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b063` | article | Ingredients such as nano-hydroxyapatite reduce tooth sensitivity, refill lost minerals in your enam… | admin-held |  |
| 424 | `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b064` | article | Xylitol, a natural sweetener, reduces the risk of cavities by holding back the growth of harmful ba… | admin-held |  |
| 425 | `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b065` | article | Coconut oil has antimicrobial properties that can help protect against gum disease . | admin-held |  |
| 426 | `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b066` | article | You can protect your physical wellness by choosing products that support oral health without exposi… | admin-held |  |
| 427 | `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b067` | article | In addition to supporting your mental, psychological, and physical health, your toothpaste should a… | admin-held |  |
| 428 | `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b068` | article | Cinnamon, lime, orange, and mint in toothpaste ensure fresh breath, strengthen your teeth and enhan… | admin-held |  |
| 429 | `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b069` | article | Nano hydroxyapatite in toothpaste also whitens teeth. This is sure to significantly boost your conf… | admin-held |  |
| 430 | `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b070` | article | An important innovation in advancing holistic health through oral care is the development of biorhy… | admin-held |  |
| 431 | `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b071` | article | Biorhythmic toothpastes are formulated to align with the body’s natural biological cycles. This mea… | admin-held |  |
| 432 | `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b072` | article | Energizing ingredients like guarana, lime, and mint are infused in our Morning toothpaste. These ac… | admin-held |  |
| 433 | `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b073` | article | The Awake toothpaste also improves bad breath, allowing for clean, fresh breath. | admin-held |  |
| 434 | `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b074` | article | Evening toothpaste includes calming ingredients like valerian, cinnamon, and orange. | admin-held |  |
| 435 | `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b075` | article | These ingredients help reduce stress, promote relaxation, prevent gum disease, and fight tooth deca… | admin-held |  |
| 436 | `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b076` | article | This approach ensures that your oral care routine supports your body’s needs at different times of … | admin-held |  |
| 437 | `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b077` | article | Karmicare for Overall Wellness | admin-held |  |
| 438 | `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b078` | article | Shop Now | admin-held |  |
| 439 | `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b079` | article | Karmicare’s Awake and Asleep toothpastes are designed with this holistic approach in mind. | admin-held |  |
| 440 | `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b080` | article | We carefully craft the formulas to work with your body’s natural rhythms. This ensures that your bo… | admin-held |  |
| 441 | `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b081` | article | The morning toothpaste, Awake, is suited to boost energy and mental clarity, while the evening toot… | admin-held |  |
| 442 | `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b082` | article | This ensures that your oral care routine supports your overall health in the most wholesome way pos… | admin-held |  |
| 443 | `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b083` | article | Oral health is more than just a bright smile - it is a fundamental aspect of mind-body wellness. Se… | admin-held |  |
| 444 | `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b084` | article | Think: | admin-held |  |
| 445 | `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b085` | article | Improved mental performance | admin-held |  |
| 446 | `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b086` | article | Reduced stress through better sleep. | admin-held |  |
| 447 | `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b087` | article | Energised mornings. | admin-held |  |
| 448 | `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b088` | article | Protection against cavities and gum disease | admin-held |  |
| 449 | `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b089` | article | Reduced tooth sensitivity. | admin-held |  |
| 450 | `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b090` | article | Enhanced self-esteem and social interactions. | admin-held |  |
| 451 | `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b091` | article | Wellness while ensuring safety. | admin-held |  |
| 452 | `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b092` | article | The benefits are impressive! | admin-held |  |
| 453 | `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b093` | article | Karmicare’s Awake and Asleep toothpaste is designed to meet these needs. We offer formulas that wor… | admin-held |  |
| 454 | `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b094` | article | Take control of your wellness journey by including thoughtful, clean oral care in your daily routin… | admin-held |  |
| 455 | `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b095` | article | Take a chance at wellness. Order complete wellness in a tube . | admin-held |  |
| 456 | `admin:article:news/how-oral-health-impacts-your-overall-wellness:seo.title` | article | How Oral Health Impacts Your Overall Wellness – KARMICARE | admin-held |  |
| 457 | `admin:article:news/how-oral-health-impacts-your-overall-wellness:seo.description` | article | Self Reflection Questions: How does my current oral care routine make me feel? Do I feel confident … | admin-held |  |
| 458 | `admin:article:news/top-natural-whitening-toothpaste-for-a-brighter-smile:text#01` | article | [img alt] Bright Smiles Leave a Lasting Impression | admin-held |  |
| 459 | `admin:article:news/top-natural-whitening-toothpaste-for-a-brighter-smile:body_html#b001` | article | A bright, confident smile can leave a lasting impression. It's more than just an aesthetic feature—… | admin-held |  |
| 460 | `admin:article:news/top-natural-whitening-toothpaste-for-a-brighter-smile:body_html#b002` | article | With more people shifting toward natural whitening toothpaste—products that use natural ingredients… | admin-held |  |
| 461 | `admin:article:news/top-natural-whitening-toothpaste-for-a-brighter-smile:body_html#b003` | article | Unlike traditional whitening toothpaste loaded with artificial additives, natural options like Karm… | admin-held |  |
| 462 | `admin:article:news/top-natural-whitening-toothpaste-for-a-brighter-smile:body_html#b004` | article | In this article, we’ll discuss the benefits of using natural whitening toothpaste, highlight key in… | admin-held |  |
| 463 | `admin:article:news/top-natural-whitening-toothpaste-for-a-brighter-smile:body_html#b005` | article | Natural Whitening Toothpaste | admin-held |  |
| 464 | `admin:article:news/top-natural-whitening-toothpaste-for-a-brighter-smile:body_html#b006` | article | Natural whitening toothpaste uses plant and mineral-based ingredients to remove surface stains and … | admin-held |  |
| 465 | `admin:article:news/top-natural-whitening-toothpaste-for-a-brighter-smile:body_html#b007` | article | These gentle toothpastes are safe for daily use. Besides whitening, natural toothpaste also support… | admin-held |  |
| 466 | `admin:article:news/top-natural-whitening-toothpaste-for-a-brighter-smile:body_html#b008` | article | Why Choose Natural Whitening Toothpaste? | admin-held |  |
| 467 | `admin:article:news/top-natural-whitening-toothpaste-for-a-brighter-smile:body_html#b009` | article | Unlike conventional toothpastes that are loaded with artificial additives, natural whitening toothp… | admin-held |  |
| 468 | `admin:article:news/top-natural-whitening-toothpaste-for-a-brighter-smile:body_html#b010` | article | With natural whitening toothpaste, you're choosing a product that's gentle on your enamel and the e… | admin-held |  |
| 469 | `admin:article:news/top-natural-whitening-toothpaste-for-a-brighter-smile:body_html#b011` | article | Shop Karmicare Biorhythmic Oral Hygiene Set | admin-held |  |
| 470 | `admin:article:news/top-natural-whitening-toothpaste-for-a-brighter-smile:body_html#b012` | article | Benefits of Using Natural Ingredients in Oral Care | admin-held |  |
| 471 | `admin:article:news/top-natural-whitening-toothpaste-for-a-brighter-smile:body_html#b013` | article | The main advantage is the ingredients. Regular toothpastes often include synthetic chemicals, such … | admin-held |  |
| 472 | `admin:article:news/top-natural-whitening-toothpaste-for-a-brighter-smile:body_html#b014` | article | Although they clean teeth, these additives can irritate, cause allergic reactions, and disrupt your… | admin-held |  |
| 473 | `admin:article:news/top-natural-whitening-toothpaste-for-a-brighter-smile:body_html#b015` | article | Natural Whitening Toothpaste is Nontoxic | admin-held |  |
| 474 | `admin:article:news/top-natural-whitening-toothpaste-for-a-brighter-smile:body_html#b016` | article | Natural whitening toothpastes, however, use clean, health-conscious ingredients that prioritize you… | admin-held |  |
| 475 | `admin:article:news/top-natural-whitening-toothpaste-for-a-brighter-smile:body_html#b017` | article | Our ingredients reflect these principles: | admin-held |  |
| 476 | `admin:article:news/top-natural-whitening-toothpaste-for-a-brighter-smile:body_html#b018` | article | Gentle on Enamel: | admin-held |  |
| 477 | `admin:article:news/top-natural-whitening-toothpaste-for-a-brighter-smile:body_html#b019` | article | Natural remineralizing agents like nano-hydroxyapatite and gentle abrasives like hydrated silica an… | admin-held |  |
| 478 | `admin:article:news/top-natural-whitening-toothpaste-for-a-brighter-smile:body_html#b020` | article | Non-toxic: | admin-held |  |
| 479 | `admin:article:news/top-natural-whitening-toothpaste-for-a-brighter-smile:body_html#b021` | article | Because our toothpaste is free from harmful chemicals, it is safe for everyone, including kids and … | admin-held |  |
| 480 | `admin:article:news/top-natural-whitening-toothpaste-for-a-brighter-smile:body_html#b022` | article | Sustainable: | admin-held |  |
| 481 | `admin:article:news/top-natural-whitening-toothpaste-for-a-brighter-smile:body_html#b023` | article | Ingredients like coconut oil and cocos nucifera water are sourced in sustainable conditions. This s… | admin-held |  |
| 482 | `admin:article:news/top-natural-whitening-toothpaste-for-a-brighter-smile:body_html#b024` | article | Holistic Health: | admin-held |  |
| 483 | `admin:article:news/top-natural-whitening-toothpaste-for-a-brighter-smile:body_html#b025` | article | Natural ingredients like peppermint oil, and valerian extract offer antimicrobial and anti-inflamma… | admin-held |  |
| 484 | `admin:article:news/top-natural-whitening-toothpaste-for-a-brighter-smile:body_html#b026` | article | Key Ingredients and Their Benefits | admin-held |  |
| 485 | `admin:article:news/top-natural-whitening-toothpaste-for-a-brighter-smile:body_html#b027` | article | Nano Hydroxyapatite: Strengthening and Whitening | admin-held |  |
| 486 | `admin:article:news/top-natural-whitening-toothpaste-for-a-brighter-smile:body_html#b028` | article | Nano hydroxyapatite is a revolutionary ingredient in natural whitening toothpaste. This mineral mak… | admin-held |  |
| 487 | `admin:article:news/top-natural-whitening-toothpaste-for-a-brighter-smile:body_html#b029` | article | Guarana: Energizing and Refreshing | admin-held |  |
| 488 | `admin:article:news/top-natural-whitening-toothpaste-for-a-brighter-smile:body_html#b030` | article | Guarana, a plant from the Amazon basin, adds a refreshing boost to your morning routine, making it … | admin-held |  |
| 489 | `admin:article:news/top-natural-whitening-toothpaste-for-a-brighter-smile:body_html#b031` | article | Xylitol: Fighting Cavities Naturally | admin-held |  |
| 490 | `admin:article:news/top-natural-whitening-toothpaste-for-a-brighter-smile:body_html#b032` | article | Xylitol prevents cavities by starving harmful bacteria that feed on sugar, reducing plaque and cavi… | admin-held |  |
| 491 | `admin:article:news/top-natural-whitening-toothpaste-for-a-brighter-smile:body_html#b033` | article | Perlite: Gentle Polishing for a Radiant Smile | admin-held |  |
| 492 | `admin:article:news/top-natural-whitening-toothpaste-for-a-brighter-smile:body_html#b034` | article | Perlite, a natural abrasive, gently removes stains, keeping teeth free from buildup for a polished … | admin-held |  |
| 493 | `admin:article:news/top-natural-whitening-toothpaste-for-a-brighter-smile:body_html#b035` | article | Calcium Carbonate: Natural Whitening and Strengthening | admin-held |  |
| 494 | `admin:article:news/top-natural-whitening-toothpaste-for-a-brighter-smile:body_html#b036` | article | Calcium Carbonate gently scrubs surface stains and supports remineralization , strengthening teeth. | admin-held |  |
| 495 | `admin:article:news/top-natural-whitening-toothpaste-for-a-brighter-smile:body_html#b037` | article | Mentha Piperita (Peppermint) Oil: Freshness and Oral Health | admin-held |  |
| 496 | `admin:article:news/top-natural-whitening-toothpaste-for-a-brighter-smile:body_html#b038` | article | Peppermint oil provides a cooling sensation, freshening breath while offering natural antimicrobial… | admin-held |  |
| 497 | `admin:article:news/top-natural-whitening-toothpaste-for-a-brighter-smile:body_html#b039` | article | Bentonite Clay: Gentle Cleaning | admin-held |  |
| 498 | `admin:article:news/top-natural-whitening-toothpaste-for-a-brighter-smile:body_html#b040` | article | Bentonite clay offers detoxifying benefits , cleaning the mouth effectively while being rich in min… | admin-held |  |
| 499 | `admin:article:news/top-natural-whitening-toothpaste-for-a-brighter-smile:body_html#b041` | article | Valerian: Soothing and Calming | admin-held |  |
| 500 | `admin:article:news/top-natural-whitening-toothpaste-for-a-brighter-smile:body_html#b042` | article | Valerian is known for its calming properties, enhancing your nighttime brushing routine. Beneficial… | admin-held |  |
| 501 | `admin:article:news/top-natural-whitening-toothpaste-for-a-brighter-smile:body_html#b043` | article | Cinnamon Cassia Bark Extract: Warmth and Antimicrobial Protection | admin-held |  |
| 502 | `admin:article:news/top-natural-whitening-toothpaste-for-a-brighter-smile:body_html#b044` | article | Cinnamon Cassia Bark Extract adds a warm, spicy flavor and antimicrobial benefits to your toothpast… | admin-held |  |
| 503 | `admin:article:news/top-natural-whitening-toothpaste-for-a-brighter-smile:body_html#b045` | article | Citrus Sinensis (Orange) Peel Oil Expressed: Brightness and Antioxidants | admin-held |  |
| 504 | `admin:article:news/top-natural-whitening-toothpaste-for-a-brighter-smile:body_html#b046` | article | Orange Peel Oil adds a citrus flavor and delivers natural antioxidants to support oral health, maki… | admin-held |  |
| 505 | `admin:article:news/top-natural-whitening-toothpaste-for-a-brighter-smile:body_html#b047` | article | Activated Charcoal | admin-held |  |
| 506 | `admin:article:news/top-natural-whitening-toothpaste-for-a-brighter-smile:body_html#b048` | article | Activated charcoal binds to stains, removing toxins and bacteria for a whiter, healthier mouth. | admin-held |  |
| 507 | `admin:article:news/top-natural-whitening-toothpaste-for-a-brighter-smile:body_html#b049` | article | Aloe Vera | admin-held |  |
| 508 | `admin:article:news/top-natural-whitening-toothpaste-for-a-brighter-smile:body_html#b050` | article | Aloe Vera calms inflamed gums, providing moisture and supporting minor healing. | admin-held |  |
| 509 | `admin:article:news/top-natural-whitening-toothpaste-for-a-brighter-smile:body_html#b051` | article | Shop Our Bestselling Natural Toothpaste | admin-held |  |
| 510 | `admin:article:news/top-natural-whitening-toothpaste-for-a-brighter-smile:body_html#b052` | article | How to Choose the Right Natural Whitening Toothpaste for You | admin-held |  |
| 511 | `admin:article:news/top-natural-whitening-toothpaste-for-a-brighter-smile:body_html#b053` | article | With so many options available, here's how to find the best one for you: | admin-held |  |
| 512 | `admin:article:news/top-natural-whitening-toothpaste-for-a-brighter-smile:body_html#b054` | article | Consider Your Specific Oral Health Needs | admin-held |  |
| 513 | `admin:article:news/top-natural-whitening-toothpaste-for-a-brighter-smile:body_html#b055` | article | If you have sensitive teeth, look for a toothpaste that contains hydroxyapatite or other enamel-str… | admin-held |  |
| 514 | `admin:article:news/top-natural-whitening-toothpaste-for-a-brighter-smile:body_html#b056` | article | Check for Certifications and Ingredient Transparency | admin-held |  |
| 515 | `admin:article:news/top-natural-whitening-toothpaste-for-a-brighter-smile:body_html#b057` | article | Ensure that the toothpaste you choose is genuinely natural and safe. Look for USDA organic, non-GMO… | admin-held |  |
| 516 | `admin:article:news/top-natural-whitening-toothpaste-for-a-brighter-smile:body_html#b058` | article | Evaluate the Flavor | admin-held |  |
| 517 | `admin:article:news/top-natural-whitening-toothpaste-for-a-brighter-smile:body_html#b059` | article | Although you want an effective toothpaste, flavor matters. Choose a flavor you enjoy to make your r… | admin-held |  |
| 518 | `admin:article:news/top-natural-whitening-toothpaste-for-a-brighter-smile:body_html#b060` | article | Conclusion | admin-held |  |
| 519 | `admin:article:news/top-natural-whitening-toothpaste-for-a-brighter-smile:body_html#b061` | article | Whitening your smile shouldn’t cost your oral health. Natural whitening toothpastes offer a safer, … | admin-held |  |
| 520 | `admin:article:news/top-natural-whitening-toothpaste-for-a-brighter-smile:body_html#b062` | article | Karmicare has a range of natural whitening toothpaste options to suit your preferences. They’re flu… | admin-held |  |
| 521 | `admin:article:news/top-natural-whitening-toothpaste-for-a-brighter-smile:seo.title` | article | Top Natural Whitening Toothpaste For a Brighter Smile. – KARMICARE | admin-held |  |
| 522 | `admin:article:news/top-natural-whitening-toothpaste-for-a-brighter-smile:seo.description` | article | A bright, confident smile can leave a lasting impression. It's more than just an aesthetic feature—… | admin-held |  |
| 523 | `admin:article:news/5-reasons-you-should-avoid-fluoride-in-toothpaste:text#01` | article | [img alt] Fluoride in Toothpaste Is More Harmful than It Is Beneficial | admin-held |  |
| 524 | `admin:article:news/5-reasons-you-should-avoid-fluoride-in-toothpaste:body_html#b001` | article | Self Reflection: | admin-held |  |
| 525 | `admin:article:news/5-reasons-you-should-avoid-fluoride-in-toothpaste:body_html#b002` | article | How do the ingredients in my toothpaste affect my health? | admin-held |  |
| 526 | `admin:article:news/5-reasons-you-should-avoid-fluoride-in-toothpaste:body_html#b003` | article | Is fluoride-free toothpaste healthier than fluoride toothpaste? | admin-held |  |
| 527 | `admin:article:news/5-reasons-you-should-avoid-fluoride-in-toothpaste:body_html#b004` | article | What is the best alternative to fluoride in toothpaste? | admin-held |  |
| 528 | `admin:article:news/5-reasons-you-should-avoid-fluoride-in-toothpaste:body_html#b005` | article | Key takeaways: | admin-held |  |
| 529 | `admin:article:news/5-reasons-you-should-avoid-fluoride-in-toothpaste:body_html#b006` | article | Fluoride is commonly added to toothpaste to prevent tooth decay. | admin-held |  |
| 530 | `admin:article:news/5-reasons-you-should-avoid-fluoride-in-toothpaste:body_html#b007` | article | Fluoride in toothpaste leads to several detrimental health effects. | admin-held |  |
| 531 | `admin:article:news/5-reasons-you-should-avoid-fluoride-in-toothpaste:body_html#b008` | article | Nano hydroxyapatite is a natural, safer, and more effective alternative to fluoride. | admin-held |  |
| 532 | `admin:article:news/5-reasons-you-should-avoid-fluoride-in-toothpaste:body_html#b009` | article | In your quest for good oral health, fresh breath, and whiter teeth, you have likely sifted through … | admin-held |  |
| 533 | `admin:article:news/5-reasons-you-should-avoid-fluoride-in-toothpaste:body_html#b010` | article | While it's a common ingredient, most people are awakening to the fact that fluoride is a harmful su… | admin-held |  |
| 534 | `admin:article:news/5-reasons-you-should-avoid-fluoride-in-toothpaste:body_html#b011` | article | Studies suggest that fluoride ingestion can cause various side effects. | admin-held |  |
| 535 | `admin:article:news/5-reasons-you-should-avoid-fluoride-in-toothpaste:body_html#b012` | article | In this article, we will discuss the science behind fluoride use and its harmful effects. | admin-held |  |
| 536 | `admin:article:news/5-reasons-you-should-avoid-fluoride-in-toothpaste:body_html#b013` | article | We’ll also introduce you to Karmicare, the world’s only biorhythmic toothpaste. An excellent fluori… | admin-held |  |
| 537 | `admin:article:news/5-reasons-you-should-avoid-fluoride-in-toothpaste:body_html#b014` | article | What is Fluoride in Toothpaste? | admin-held |  |
| 538 | `admin:article:news/5-reasons-you-should-avoid-fluoride-in-toothpaste:body_html#b015` | article | Fluoride is a natural mineral found in soil and water. It’s a chemical form of fluorine, the thirte… | admin-held |  |
| 539 | `admin:article:news/5-reasons-you-should-avoid-fluoride-in-toothpaste:body_html#b016` | article | Many toothpaste brands have included fluoride in their products for several reasons: | admin-held |  |
| 540 | `admin:article:news/5-reasons-you-should-avoid-fluoride-in-toothpaste:body_html#b017` | article | Fluoride, especially in combination with other ingredients like zinc citrate, slows down the demine… | admin-held |  |
| 541 | `admin:article:news/5-reasons-you-should-avoid-fluoride-in-toothpaste:body_html#b018` | article | Fluoride also has antiplaque properties. It prevents tartar from forming when plaque hardens. | admin-held |  |
| 542 | `admin:article:news/5-reasons-you-should-avoid-fluoride-in-toothpaste:body_html#b019` | article | Some toothpaste combines fluoride with calcium carbonate to effectively remove plaque. | admin-held |  |
| 543 | `admin:article:news/5-reasons-you-should-avoid-fluoride-in-toothpaste:body_html#b020` | article | Experts also argue that fluoride supports remineralization, the process by which teeth naturally re… | admin-held |  |
| 544 | `admin:article:news/5-reasons-you-should-avoid-fluoride-in-toothpaste:body_html#b021` | article | While fluoride can be useful in toothpaste, it is linked to potential side effects. | admin-held |  |
| 545 | `admin:article:news/5-reasons-you-should-avoid-fluoride-in-toothpaste:body_html#b022` | article | This has led many healthcare providers to recommend fluoride-free toothpaste options. | admin-held |  |
| 546 | `admin:article:news/5-reasons-you-should-avoid-fluoride-in-toothpaste:body_html#b023` | article | Fluoride Affects Your Oral Health Negatively | admin-held |  |
| 547 | `admin:article:news/5-reasons-you-should-avoid-fluoride-in-toothpaste:body_html#b024` | article | Harmful Effects of Fluoride in Toothpaste | admin-held |  |
| 548 | `admin:article:news/5-reasons-you-should-avoid-fluoride-in-toothpaste:body_html#b025` | article | Despite the role of fluoride in dental care, it comes with significant downsides. | admin-held |  |
| 549 | `admin:article:news/5-reasons-you-should-avoid-fluoride-in-toothpaste:body_html#b026` | article | Did you know? When you brush for 2 minutes, twice a day, as you should, you are exposed to chemical… | admin-held |  |
| 550 | `admin:article:news/5-reasons-you-should-avoid-fluoride-in-toothpaste:body_html#b027` | article | 1. Fluoride Impairs Sleep Quality | admin-held |  |
| 551 | `admin:article:news/5-reasons-you-should-avoid-fluoride-in-toothpaste:body_html#b028` | article | Up to 30% of adults suffer from short-term insomnia. | admin-held |  |
| 552 | `admin:article:news/5-reasons-you-should-avoid-fluoride-in-toothpaste:body_html#b029` | article | While stress and screen time can impact your sleep, fluoride might be another culprit. | admin-held |  |
| 553 | `admin:article:news/5-reasons-you-should-avoid-fluoride-in-toothpaste:body_html#b030` | article | It disrupts your circadian rhythm, the body’s biological clock that governs your sleep-wake cycle. … | admin-held |  |
| 554 | `admin:article:news/5-reasons-you-should-avoid-fluoride-in-toothpaste:body_html#b031` | article | If you find yourself wide awake after brushing at night, switching to a fluoride-free toothpaste co… | admin-held |  |
| 555 | `admin:article:news/5-reasons-you-should-avoid-fluoride-in-toothpaste:body_html#b032` | article | Karmicare’s Asleep toothpaste is the best fluoride-free toothpaste for this purpose. It contains va… | admin-held |  |
| 556 | `admin:article:news/5-reasons-you-should-avoid-fluoride-in-toothpaste:body_html#b033` | article | 2. Fluoride May Cause Dental Fluorosis | admin-held |  |
| 557 | `admin:article:news/5-reasons-you-should-avoid-fluoride-in-toothpaste:body_html#b034` | article | Dental fluorosis is the discoloration of the teeth caused by overexposure to fluoride. | admin-held |  |
| 558 | `admin:article:news/5-reasons-you-should-avoid-fluoride-in-toothpaste:body_html#b035` | article | Reduced mineralization of teeth causes fluorosis discoloration. | admin-held |  |
| 559 | `admin:article:news/5-reasons-you-should-avoid-fluoride-in-toothpaste:body_html#b036` | article | Kids and teenagers are more susceptible to this condition as their teeth are still developing. | admin-held |  |
| 560 | `admin:article:news/5-reasons-you-should-avoid-fluoride-in-toothpaste:body_html#b037` | article | Excess fluoride calcifies developing teeth, resulting in discoloration. | admin-held |  |
| 561 | `admin:article:news/5-reasons-you-should-avoid-fluoride-in-toothpaste:body_html#b038` | article | While mostly cosmetic, the effects of fluorosis can be damaging to dental health. It can also incre… | admin-held |  |
| 562 | `admin:article:news/5-reasons-you-should-avoid-fluoride-in-toothpaste:body_html#b039` | article | 3. Fluoride May Weaken Bones | admin-held |  |
| 563 | `admin:article:news/5-reasons-you-should-avoid-fluoride-in-toothpaste:body_html#b040` | article | While fluoride increases bone density, it may also weaken bone quality. | admin-held |  |
| 564 | `admin:article:news/5-reasons-you-should-avoid-fluoride-in-toothpaste:body_html#b041` | article | Research shows that bone quality reduces with increasing fluoride content . | admin-held |  |
| 565 | `admin:article:news/5-reasons-you-should-avoid-fluoride-in-toothpaste:body_html#b042` | article | Too much fluoride may also lead to skeletal fluorosis . This further weakens the bones. | admin-held |  |
| 566 | `admin:article:news/5-reasons-you-should-avoid-fluoride-in-toothpaste:body_html#b043` | article | 4. Fluoride May Lead to Reduced IQ in Kids | admin-held |  |
| 567 | `admin:article:news/5-reasons-you-should-avoid-fluoride-in-toothpaste:body_html#b044` | article | Studies show that exposure to fluoride during childhood is associated with reduced IQ scores. | admin-held |  |
| 568 | `admin:article:news/5-reasons-you-should-avoid-fluoride-in-toothpaste:body_html#b045` | article | Pregnant women who consume fluoride may also extend this risk to their unborn children. | admin-held |  |
| 569 | `admin:article:news/5-reasons-you-should-avoid-fluoride-in-toothpaste:body_html#b046` | article | Since children’s brains are still developing, they are at a greater risk of experiencing fluoride n… | admin-held |  |
| 570 | `admin:article:news/5-reasons-you-should-avoid-fluoride-in-toothpaste:body_html#b047` | article | Tip: We advise you to use a safe, fluoride-free toothpaste for kids. | admin-held |  |
| 571 | `admin:article:news/5-reasons-you-should-avoid-fluoride-in-toothpaste:body_html#b048` | article | 5. Fluoride May Disrupt Thyroid Function | admin-held |  |
| 572 | `admin:article:news/5-reasons-you-should-avoid-fluoride-in-toothpaste:body_html#b049` | article | The thyroid gland is a small organ located in front of the neck. It produces thyroid hormones, whic… | admin-held |  |
| 573 | `admin:article:news/5-reasons-you-should-avoid-fluoride-in-toothpaste:body_html#b050` | article | Fluoride disrupts the production of thyroid hormones . This may lead to hypothyroidism, which affec… | admin-held |  |
| 574 | `admin:article:news/5-reasons-you-should-avoid-fluoride-in-toothpaste:body_html#b051` | article | In 2012, British scientists reported higher levels of hypothyroidism in areas with fluoridated wate… | admin-held |  |
| 575 | `admin:article:news/5-reasons-you-should-avoid-fluoride-in-toothpaste:body_html#b052` | article | Alternative Options to Fluoride | admin-held |  |
| 576 | `admin:article:news/5-reasons-you-should-avoid-fluoride-in-toothpaste:body_html#b053` | article | Given the health concerns around fluoride, consider switching to a healthier alternative. | admin-held |  |
| 577 | `admin:article:news/5-reasons-you-should-avoid-fluoride-in-toothpaste:body_html#b054` | article | Nano hydroxyapatite (nano HAp) stands out as an excellent alternative to fluoride . Nano HAp is the… | admin-held |  |
| 578 | `admin:article:news/5-reasons-you-should-avoid-fluoride-in-toothpaste:body_html#b055` | article | HA is the most abundant compound in teeth. It’s composed of calcium and phosphate ions. It makes up… | admin-held |  |
| 579 | `admin:article:news/5-reasons-you-should-avoid-fluoride-in-toothpaste:body_html#b056` | article | Toothpaste that contains nano HAp, such as Karmicare , protects and strengthens teeth, without the … | admin-held |  |
| 580 | `admin:article:news/5-reasons-you-should-avoid-fluoride-in-toothpaste:body_html#b057` | article | Tip: 3-year-olds can use 1 pump of Karmicare, and toddlers through 6-year-olds can use it as a regu… | admin-held |  |
| 581 | `admin:article:news/5-reasons-you-should-avoid-fluoride-in-toothpaste:body_html#b058` | article | Nano Hap is a Safe and More Effective Fluoride Alternative. | admin-held |  |
| 582 | `admin:article:news/5-reasons-you-should-avoid-fluoride-in-toothpaste:body_html#b059` | article | Nano HAp is superior to fluoride in tooth remineralization because it remineralizes teeth from with… | admin-held |  |
| 583 | `admin:article:news/5-reasons-you-should-avoid-fluoride-in-toothpaste:body_html#b060` | article | Nano HAp holds many other valuable benefits for your teeth, such as: | admin-held |  |
| 584 | `admin:article:news/5-reasons-you-should-avoid-fluoride-in-toothpaste:body_html#b061` | article | Decreased tooth sensitivity: 1 in 8 adults complain about sensitive teeth . Nano HAp reduces sensit… | admin-held |  |
| 585 | `admin:article:news/5-reasons-you-should-avoid-fluoride-in-toothpaste:body_html#b062` | article | Teeth whitening: Nano HAp whitens teeth by adding native minerals to the surface. You’ll no longer … | admin-held |  |
| 586 | `admin:article:news/5-reasons-you-should-avoid-fluoride-in-toothpaste:body_html#b063` | article | Protects enamel from acid overexposure: Foods like citrus and lemons contain acids that react with … | admin-held |  |
| 587 | `admin:article:news/5-reasons-you-should-avoid-fluoride-in-toothpaste:body_html#b064` | article | Refills small lesions: It repairs areas of decay and makes teeth stronger. | admin-held |  |
| 588 | `admin:article:news/5-reasons-you-should-avoid-fluoride-in-toothpaste:body_html#b065` | article | Safe for children and pregnant women: Kids and pregnant women are more susceptible to the effects o… | admin-held |  |
| 589 | `admin:article:news/5-reasons-you-should-avoid-fluoride-in-toothpaste:body_html#b066` | article | You don’t need fluoride for healthy teeth. | admin-held |  |
| 590 | `admin:article:news/5-reasons-you-should-avoid-fluoride-in-toothpaste:body_html#b067` | article | Nano Hydroxyapatite is a superior and safer alternative to fluoride. Nano HAp whitens teeth, streng… | admin-held |  |
| 591 | `admin:article:news/5-reasons-you-should-avoid-fluoride-in-toothpaste:body_html#b068` | article | Why Karmicare Toothpaste Stands Out | admin-held |  |
| 592 | `admin:article:news/5-reasons-you-should-avoid-fluoride-in-toothpaste:body_html#b069` | article | Most traditional brands of toothpaste contain fluoride, but Karmicare offers a better solution. Swi… | admin-held |  |
| 593 | `admin:article:news/5-reasons-you-should-avoid-fluoride-in-toothpaste:body_html#b070` | article | Shop Karmicare Fluoride-free Toothpaste. | admin-held |  |
| 594 | `admin:article:news/5-reasons-you-should-avoid-fluoride-in-toothpaste:body_html#b071` | article | Apart from nano HAp, Karmicare contains other healthy natural ingredients. Xylitol prevents cavity-… | admin-held |  |
| 595 | `admin:article:news/5-reasons-you-should-avoid-fluoride-in-toothpaste:body_html#b072` | article | With Karmicare, it’s a win-win — you get fresh breath, and stronger and whiter teeth without riskin… | admin-held |  |
| 596 | `admin:article:news/5-reasons-you-should-avoid-fluoride-in-toothpaste:body_html#b073` | article | Switch to Karmicare Biorhythmic Oral Hygiene Set Now | admin-held |  |
| 597 | `admin:article:news/5-reasons-you-should-avoid-fluoride-in-toothpaste:body_html#b074` | article | Karmicare is the best natural toothpaste that guarantees the quality and safety you deserve. | admin-held |  |
| 598 | `admin:article:news/5-reasons-you-should-avoid-fluoride-in-toothpaste:seo.title` | article | 5 Reasons You Should Avoid Fluoride in Toothpaste – KARMICARE | admin-held |  |
| 599 | `admin:article:news/5-reasons-you-should-avoid-fluoride-in-toothpaste:seo.description` | article | Self Reflection: How do the ingredients in my toothpaste affect my health? Is fluoride-free toothpa… | admin-held |  |
| 600 | `admin:article:news/headaches-and-tooth-pain-understanding-the-connection:text#01` | article | [img alt] Tooth pain is linked to headaches | admin-held |  |
| 601 | `admin:article:news/headaches-and-tooth-pain-understanding-the-connection:body_html#b001` | article | It's a common and often frustrating experience—waking up with a headache that feels like it’s comin… | admin-held |  |
| 602 | `admin:article:news/headaches-and-tooth-pain-understanding-the-connection:body_html#b002` | article | Understanding the link between these seemingly unrelated pains is key to treating them. This blog p… | admin-held |  |
| 603 | `admin:article:news/headaches-and-tooth-pain-understanding-the-connection:body_html#b003` | article | Tooth pain can have many causes, each affecting your body differently. Because dental health is key… | admin-held |  |
| 604 | `admin:article:news/headaches-and-tooth-pain-understanding-the-connection:body_html#b004` | article | Common Causes of Tooth Pain | admin-held |  |
| 605 | `admin:article:news/headaches-and-tooth-pain-understanding-the-connection:body_html#b005` | article | Cavities: Cavities are a major cause of tooth pain. Bacteria break down sugar into acid, eroding th… | admin-held |  |
| 606 | `admin:article:news/headaches-and-tooth-pain-understanding-the-connection:body_html#b006` | article | Gum Infection: Gingivitis and periodontitis cause tooth pain by inflaming gums, due to plaque build… | admin-held |  |
| 607 | `admin:article:news/headaches-and-tooth-pain-understanding-the-connection:body_html#b007` | article | Tooth Sensitivity: Enamel wear or gum recession exposes the dentin. This causes a painful sensation… | admin-held |  |
| 608 | `admin:article:news/headaches-and-tooth-pain-understanding-the-connection:body_html#b008` | article | Cracked or Damaged Teeth: Trauma, grinding, or biting down on hard objects can crack or damage teet… | admin-held |  |
| 609 | `admin:article:news/headaches-and-tooth-pain-understanding-the-connection:body_html#b009` | article | Dental Abscesses: Abscesses are bacterial infections that form painful pus pockets. They often lead… | admin-held |  |
| 610 | `admin:article:news/headaches-and-tooth-pain-understanding-the-connection:body_html#b010` | article | Shop Our Ultra Soft Morning and Evening Toothbrush | admin-held |  |
| 611 | `admin:article:news/headaches-and-tooth-pain-understanding-the-connection:body_html#b011` | article | Symptoms of Tooth Pain | admin-held |  |
| 612 | `admin:article:news/headaches-and-tooth-pain-understanding-the-connection:body_html#b012` | article | Tooth pain can vary from mild to severe, depending on the cause. Recognizing the symptoms early can… | admin-held |  |
| 613 | `admin:article:news/headaches-and-tooth-pain-understanding-the-connection:body_html#b013` | article | Sharp Throbbing or Constant Pain: This often points to a cavity, cracked tooth, or abscess. You may… | admin-held |  |
| 614 | `admin:article:news/headaches-and-tooth-pain-understanding-the-connection:body_html#b014` | article | Pain When Biting or Chewing: This could mean a cracked tooth, a cavity, or a loose filling. | admin-held |  |
| 615 | `admin:article:news/headaches-and-tooth-pain-understanding-the-connection:body_html#b015` | article | Sensitivity to Temperature or Sweets: Sharp pain from hot, cold, or sweet foods might signal sensit… | admin-held |  |
| 616 | `admin:article:news/headaches-and-tooth-pain-understanding-the-connection:body_html#b016` | article | Swelling Around Tooth or Gumline: Swelling suggests gum disease or a dental abscess. It might inclu… | admin-held |  |
| 617 | `admin:article:news/headaches-and-tooth-pain-understanding-the-connection:body_html#b017` | article | Bad Breath or Unpleasant Taste: Persistent bad breath or taste could indicate an abscess or advance… | admin-held |  |
| 618 | `admin:article:news/headaches-and-tooth-pain-understanding-the-connection:body_html#b018` | article | Good oral hygiene —regular brushing, using fluoride-free toothpaste , and flossing—can prevent many… | admin-held |  |
| 619 | `admin:article:news/headaches-and-tooth-pain-understanding-the-connection:body_html#b019` | article | Shop Our Bestselling Fluoride-Free Toothpaste | admin-held |  |
| 620 | `admin:article:news/headaches-and-tooth-pain-understanding-the-connection:body_html#b020` | article | Headaches and Their Types | admin-held |  |
| 621 | `admin:article:news/headaches-and-tooth-pain-understanding-the-connection:body_html#b021` | article | Toothaches and headaches often go hand in hand. Like tooth pains, headaches come in many forms. Kno… | admin-held |  |
| 622 | `admin:article:news/headaches-and-tooth-pain-understanding-the-connection:body_html#b022` | article | Tension Headaches: This is the most common type of headache. It feels like a dull, tight band aroun… | admin-held |  |
| 623 | `admin:article:news/headaches-and-tooth-pain-understanding-the-connection:body_html#b023` | article | Migraines: Intense, throbbing pain, usually on one side, lasting hours or days. They often come wit… | admin-held |  |
| 624 | `admin:article:news/headaches-and-tooth-pain-understanding-the-connection:body_html#b024` | article | Sinus Headaches: These are caused by inflamed sinuses from infection or allergies. These lead to fa… | admin-held |  |
| 625 | `admin:article:news/headaches-and-tooth-pain-understanding-the-connection:body_html#b025` | article | Cluster Headaches: This is a rare but severe headache that occurs in cycles, often waking people fr… | admin-held |  |
| 626 | `admin:article:news/headaches-and-tooth-pain-understanding-the-connection:body_html#b026` | article | Identifying your headache type can determine if it’s related to dental issues. Improving your denta… | admin-held |  |
| 627 | `admin:article:news/headaches-and-tooth-pain-understanding-the-connection:body_html#b027` | article | The Connection Between Headaches and Tooth Pain | admin-held |  |
| 628 | `admin:article:news/headaches-and-tooth-pain-understanding-the-connection:body_html#b028` | article | Tooth pain and headaches are often linked through referred pain . This occurs when pain from one pa… | admin-held |  |
| 629 | `admin:article:news/headaches-and-tooth-pain-understanding-the-connection:body_html#b029` | article | Referred pain can make it challenging to pinpoint the exact source of discomfort. This is because t… | admin-held |  |
| 630 | `admin:article:news/headaches-and-tooth-pain-understanding-the-connection:body_html#b030` | article | Dental Problems Can Impact Headaches Through Referred Pain | admin-held |  |
| 631 | `admin:article:news/headaches-and-tooth-pain-understanding-the-connection:body_html#b031` | article | According to the National Library of Medicine , referred pain is common in dental issues, particula… | admin-held |  |
| 632 | `admin:article:news/headaches-and-tooth-pain-understanding-the-connection:body_html#b032` | article | Dental Issues Impacting Headaches | admin-held |  |
| 633 | `admin:article:news/headaches-and-tooth-pain-understanding-the-connection:body_html#b033` | article | Cavities and Headaches: Untreated cavities can irritate the tooth’s pulp and lead to headaches. The… | admin-held |  |
| 634 | `admin:article:news/headaches-and-tooth-pain-understanding-the-connection:body_html#b034` | article | Wisdom Teeth and Headaches: As wisdom teeth erupt, they can press on surrounding teeth, blood vesse… | admin-held |  |
| 635 | `admin:article:news/headaches-and-tooth-pain-understanding-the-connection:body_html#b035` | article | Nerve Sensitivity: Infections, like abscesses, can spread to the sinuses. The resulting inflammatio… | admin-held |  |
| 636 | `admin:article:news/headaches-and-tooth-pain-understanding-the-connection:body_html#b036` | article | Exposed Nerves: Exposed nerves from tooth decay, cracks, or trauma can send pain signals that sprea… | admin-held |  |
| 637 | `admin:article:news/headaches-and-tooth-pain-understanding-the-connection:body_html#b037` | article | Bruxism (Teeth Grinding): Bruxism, or teeth grinding, is a common dental issue during sleep. The co… | admin-held |  |
| 638 | `admin:article:news/headaches-and-tooth-pain-understanding-the-connection:body_html#b038` | article | Understanding this link can help you address tooth pain and headaches simultaneously. | admin-held |  |
| 639 | `admin:article:news/headaches-and-tooth-pain-understanding-the-connection:body_html#b039` | article | Karmicare’s range of oral care products effectively targets the underlying causes of tooth pain. Ou… | admin-held |  |
| 640 | `admin:article:news/headaches-and-tooth-pain-understanding-the-connection:body_html#b040` | article | This helps remineralize enamel and protect against cavities, reducing the sensitivity that often le… | admin-held |  |
| 641 | `admin:article:news/headaches-and-tooth-pain-understanding-the-connection:body_html#b041` | article | Essential oils like lime and cinnamon oil fight plaque to prevent gingivitis and periodontitis. | admin-held |  |
| 642 | `admin:article:news/headaches-and-tooth-pain-understanding-the-connection:body_html#b042` | article | Our biorhythmic oral hygiene set helps maintain oral hygiene. It prevents and manages dental absces… | admin-held |  |
| 643 | `admin:article:news/headaches-and-tooth-pain-understanding-the-connection:body_html#b043` | article | Shop Now | admin-held |  |
| 644 | `admin:article:news/headaches-and-tooth-pain-understanding-the-connection:body_html#b044` | article | Conclusion | admin-held |  |
| 645 | `admin:article:news/headaches-and-tooth-pain-understanding-the-connection:body_html#b045` | article | Headaches and tooth pain are closely connected. Good oral hygiene practices such as brushing regula… | admin-held |  |
| 646 | `admin:article:news/headaches-and-tooth-pain-understanding-the-connection:body_html#b046` | article | Additionally, regular dental checkups help catch problems early before they become more significant… | admin-held |  |
| 647 | `admin:article:news/headaches-and-tooth-pain-understanding-the-connection:seo.title` | article | Headaches and Tooth Pain: Understanding the Connection – KARMICARE | admin-held |  |
| 648 | `admin:article:news/headaches-and-tooth-pain-understanding-the-connection:seo.description` | article | It's a common and often frustrating experience—waking up with a headache that feels like it’s comin… | admin-held |  |
| 649 | `admin:article:news/3-reasons-why-you-should-look-for-an-sls-free-toothpaste:text#01` | article | [img alt] SLS-Free Toothpaste is a Healthy Option | admin-held |  |
| 650 | `admin:article:news/3-reasons-why-you-should-look-for-an-sls-free-toothpaste:body_html#b001` | article | Self Reflection: | admin-held |  |
| 651 | `admin:article:news/3-reasons-why-you-should-look-for-an-sls-free-toothpaste:body_html#b002` | article | Do I pay attention to the ingredients in my personal care products? | admin-held |  |
| 652 | `admin:article:news/3-reasons-why-you-should-look-for-an-sls-free-toothpaste:body_html#b003` | article | Could the ingredients in my toothpaste be harming my oral health? | admin-held |  |
| 653 | `admin:article:news/3-reasons-why-you-should-look-for-an-sls-free-toothpaste:body_html#b004` | article | What’s an easy way to upgrade my wellness routine? | admin-held |  |
| 654 | `admin:article:news/3-reasons-why-you-should-look-for-an-sls-free-toothpaste:body_html#b005` | article | Key takeaways: | admin-held |  |
| 655 | `admin:article:news/3-reasons-why-you-should-look-for-an-sls-free-toothpaste:body_html#b006` | article | Many commercial toothpastes contain unnecessary additives, like sodium lauryl sulfate (SLS). | admin-held |  |
| 656 | `admin:article:news/3-reasons-why-you-should-look-for-an-sls-free-toothpaste:body_html#b007` | article | Glycolipids are a natural, eco-friendly ingredient that can replace common foaming agents such as S… | admin-held |  |
| 657 | `admin:article:news/3-reasons-why-you-should-look-for-an-sls-free-toothpaste:body_html#b008` | article | Toothpaste containing sodium lauryl sulfate (or SLS) can compromise oral health. | admin-held |  |
| 658 | `admin:article:news/3-reasons-why-you-should-look-for-an-sls-free-toothpaste:body_html#b009` | article | When was the last time you took a closer look at the ingredient list on your toothpaste? | admin-held |  |
| 659 | `admin:article:news/3-reasons-why-you-should-look-for-an-sls-free-toothpaste:body_html#b010` | article | Believe it or not, you may want to keep an eye out for more than just fluoride. | admin-held |  |
| 660 | `admin:article:news/3-reasons-why-you-should-look-for-an-sls-free-toothpaste:body_html#b011` | article | More people are learning about why they may want to choose fluoride-free toothpaste over standard t… | admin-held |  |
| 661 | `admin:article:news/3-reasons-why-you-should-look-for-an-sls-free-toothpaste:body_html#b012` | article | Keep reading to learn more about sodium lauryl sulfate, why you may want to choose an SLS-free toot… | admin-held |  |
| 662 | `admin:article:news/3-reasons-why-you-should-look-for-an-sls-free-toothpaste:body_html#b013` | article | What Is Sodium Lauryl Sulfate (SLS)? | admin-held |  |
| 663 | `admin:article:news/3-reasons-why-you-should-look-for-an-sls-free-toothpaste:body_html#b014` | article | If you’ve spent time reading the ingredient lists on your personal care products, there’s a good ch… | admin-held |  |
| 664 | `admin:article:news/3-reasons-why-you-should-look-for-an-sls-free-toothpaste:body_html#b015` | article | Another place you’re likely to find SLS? Check out your household cleaning products. Yep, you read … | admin-held |  |
| 665 | `admin:article:news/3-reasons-why-you-should-look-for-an-sls-free-toothpaste:body_html#b016` | article | The same ingredient in your laundry soap, dishwashing liquid, and bathroom cleaners could lurk in y… | admin-held |  |
| 666 | `admin:article:news/3-reasons-why-you-should-look-for-an-sls-free-toothpaste:body_html#b017` | article | So what’s it doing there? | admin-held |  |
| 667 | `admin:article:news/3-reasons-why-you-should-look-for-an-sls-free-toothpaste:body_html#b018` | article | In a nutshell, sodium lauryl sulfate is a surfactant that acts as an emulsifier. | admin-held |  |
| 668 | `admin:article:news/3-reasons-why-you-should-look-for-an-sls-free-toothpaste:body_html#b019` | article | Think of it this way: When a product contains oil and water, the only way to get those ingredients … | admin-held |  |
| 669 | `admin:article:news/3-reasons-why-you-should-look-for-an-sls-free-toothpaste:body_html#b020` | article | It’s not just about SLS acting as a thickener, however; it’s also about it being used as a foaming … | admin-held |  |
| 670 | `admin:article:news/3-reasons-why-you-should-look-for-an-sls-free-toothpaste:body_html#b021` | article | Many times, it’s sodium lauryl sulfate that’s responsible for the foamy shampoo experience you get … | admin-held |  |
| 671 | `admin:article:news/3-reasons-why-you-should-look-for-an-sls-free-toothpaste:body_html#b022` | article | SLS is responsible for the foamy experience in toothpaste. | admin-held |  |
| 672 | `admin:article:news/3-reasons-why-you-should-look-for-an-sls-free-toothpaste:body_html#b023` | article | While it might seem like the amount of bubbles you see correlates to how clean something is getting… | admin-held |  |
| 673 | `admin:article:news/3-reasons-why-you-should-look-for-an-sls-free-toothpaste:body_html#b024` | article | More often than not, lathering agents are used as a psychological trigger that gives you the illusi… | admin-held |  |
| 674 | `admin:article:news/3-reasons-why-you-should-look-for-an-sls-free-toothpaste:body_html#b025` | article | If your goal is to nurture and support your oral health, you might want to think twice about what y… | admin-held |  |
| 675 | `admin:article:news/3-reasons-why-you-should-look-for-an-sls-free-toothpaste:body_html#b026` | article | 3 Reasons Why You Should Choose SLS-Free Toothpaste | admin-held |  |
| 676 | `admin:article:news/3-reasons-why-you-should-look-for-an-sls-free-toothpaste:body_html#b027` | article | Staving off gum disease and maintaining healthy teeth (and a bright smile) doesn’t have to come at … | admin-held |  |
| 677 | `admin:article:news/3-reasons-why-you-should-look-for-an-sls-free-toothpaste:body_html#b028` | article | Here are three reasons you may want to avoid products with SLS in your dental health routine. | admin-held |  |
| 678 | `admin:article:news/3-reasons-why-you-should-look-for-an-sls-free-toothpaste:body_html#b029` | article | 1. SLS is an Unnecessary Additive | admin-held |  |
| 679 | `admin:article:news/3-reasons-why-you-should-look-for-an-sls-free-toothpaste:body_html#b030` | article | Sometimes it isn’t clear which ingredients do the heavy lifting in your toothpaste, and the more ad… | admin-held |  |
| 680 | `admin:article:news/3-reasons-why-you-should-look-for-an-sls-free-toothpaste:body_html#b031` | article | Sodium lauryl sulfate is one of several unnecessary additives, including detergents, dyes, parabens… | admin-held |  |
| 681 | `admin:article:news/3-reasons-why-you-should-look-for-an-sls-free-toothpaste:body_html#b032` | article | But don’t be fooled into thinking SLS is a must in your toothpaste. It isn’t. | admin-held |  |
| 682 | `admin:article:news/3-reasons-why-you-should-look-for-an-sls-free-toothpaste:body_html#b033` | article | Glycolipids are an excellent sulfate-free swap for the foaming action provided by sodium lauryl sul… | admin-held |  |
| 683 | `admin:article:news/3-reasons-why-you-should-look-for-an-sls-free-toothpaste:body_html#b034` | article | Made from fermented sugars, glycolipids are also biocompatible, so there’s no harm in swallowing (u… | admin-held |  |
| 684 | `admin:article:news/3-reasons-why-you-should-look-for-an-sls-free-toothpaste:body_html#b035` | article | FYI: SLS isn’t just lurking in big brands like Colgate and Biotene. Even if you do see a toothpaste… | admin-held | B |
| 685 | `admin:article:news/3-reasons-why-you-should-look-for-an-sls-free-toothpaste:body_html#b036` | article | 2. Support Your Oral Microbiome | admin-held |  |
| 686 | `admin:article:news/3-reasons-why-you-should-look-for-an-sls-free-toothpaste:body_html#b037` | article | Why not skip the chemical cocktail and choose an SLS-free toothpaste? Better yet, pick one with hig… | admin-held |  |
| 687 | `admin:article:news/3-reasons-why-you-should-look-for-an-sls-free-toothpaste:body_html#b038` | article | If you visit a natural dentist, they’re likely to recommend looking for products with more recogniz… | admin-held |  |
| 688 | `admin:article:news/3-reasons-why-you-should-look-for-an-sls-free-toothpaste:body_html#b039` | article | Pass on artificial flavors and look for toothpaste made with pure ingredients. Fresh mint flavoring… | admin-held |  |
| 689 | `admin:article:news/3-reasons-why-you-should-look-for-an-sls-free-toothpaste:body_html#b040` | article | Regardless of your oral care goals: sensitivity relief, extra whitening, or maintaining fresh breat… | admin-held |  |
| 690 | `admin:article:news/3-reasons-why-you-should-look-for-an-sls-free-toothpaste:body_html#b041` | article | You don’t have to stick with SLS-based toothpaste for effective cleaning of your mouth. SLS-free al… | admin-held |  |
| 691 | `admin:article:news/3-reasons-why-you-should-look-for-an-sls-free-toothpaste:body_html#b042` | article | Karmicare’s Biorhythmic Oral Hygiene Set is the most effective SLS-free toothpaste option for whole… | admin-held |  |
| 692 | `admin:article:news/3-reasons-why-you-should-look-for-an-sls-free-toothpaste:body_html#b043` | article | Shop Karmicare SLS-Free Toothpaste Now | admin-held |  |
| 693 | `admin:article:news/3-reasons-why-you-should-look-for-an-sls-free-toothpaste:body_html#b044` | article | Being natural compounds, glycolipids help maintain a healthy balance in your mouth while being gent… | admin-held |  |
| 694 | `admin:article:news/3-reasons-why-you-should-look-for-an-sls-free-toothpaste:body_html#b045` | article | Pro Tip: Karmicare is safe for the whole family. It’s designed to be left on your teeth instead of … | admin-held |  |
| 695 | `admin:article:news/3-reasons-why-you-should-look-for-an-sls-free-toothpaste:body_html#b046` | article | Brushing with SLS-free Toothpaste Helps Improve Your Oral Health | admin-held |  |
| 696 | `admin:article:news/3-reasons-why-you-should-look-for-an-sls-free-toothpaste:body_html#b047` | article | 3. SLS May Cause Oral Irritation | admin-held |  |
| 697 | `admin:article:news/3-reasons-why-you-should-look-for-an-sls-free-toothpaste:body_html#b048` | article | Despite your resolve to take terrific care of your teeth, the wrong toothpaste formula can undermin… | admin-held |  |
| 698 | `admin:article:news/3-reasons-why-you-should-look-for-an-sls-free-toothpaste:body_html#b049` | article | SLS is a known irritant and may be causing oral issues you didn't know could be connected to sodium… | admin-held |  |
| 699 | `admin:article:news/3-reasons-why-you-should-look-for-an-sls-free-toothpaste:body_html#b050` | article | Using toothpaste with SLS leads to canker sores, dry mouth, bad breath, and sensitive teeth. Sodium… | admin-held |  |
| 700 | `admin:article:news/3-reasons-why-you-should-look-for-an-sls-free-toothpaste:body_html#b051` | article | Using toothpaste with SLS can also cause tissue sloughing, which is precisely what it sounds like. | admin-held |  |
| 701 | `admin:article:news/3-reasons-why-you-should-look-for-an-sls-free-toothpaste:body_html#b052` | article | The skin inside your mouth is thin and delicate, hence, the skin of your inner cheeks and lips beco… | admin-held |  |
| 702 | `admin:article:news/3-reasons-why-you-should-look-for-an-sls-free-toothpaste:body_html#b053` | article | Consider switching from your old brand to an SLS-free toothpaste and say goodbye to persistent cank… | admin-held |  |
| 703 | `admin:article:news/3-reasons-why-you-should-look-for-an-sls-free-toothpaste:body_html#b054` | article | Make That Switch Now | admin-held |  |
| 704 | `admin:article:news/3-reasons-why-you-should-look-for-an-sls-free-toothpaste:body_html#b055` | article | Did You Know? | admin-held |  |
| 705 | `admin:article:news/3-reasons-why-you-should-look-for-an-sls-free-toothpaste:body_html#b056` | article | Karmicare's dental floss contains activated charcoal, so you can safely get an even brighter smile.… | admin-held |  |
| 706 | `admin:article:news/3-reasons-why-you-should-look-for-an-sls-free-toothpaste:body_html#b057` | article | Not all toothpastes are created equal. While some toothpastes may appear to support your oral healt… | admin-held |  |
| 707 | `admin:article:news/3-reasons-why-you-should-look-for-an-sls-free-toothpaste:body_html#b058` | article | Moreso, they can take wellness one step further than oral health and can support your whole body. | admin-held |  |
| 708 | `admin:article:news/3-reasons-why-you-should-look-for-an-sls-free-toothpaste:seo.title` | article | 3 Reasons Why you Should look for an SLS Free Toothpaste – KARMICARE | admin-held |  |
| 709 | `admin:article:news/3-reasons-why-you-should-look-for-an-sls-free-toothpaste:seo.description` | article | Self Reflection: Do I pay attention to the ingredients in my personal care products? Could the ingr… | admin-held |  |

### `batch-08-system`

| # | id | type | EN | status | flags |
|---:|---|---|---|---|---|
| 1 | `list-collections:main/title` | template_setting | Collections | approved |  |
| 2 | `password:main/heading/heading` | template_setting | Opening soon | approved |  |
| 3 | `password:main/paragraph/text` | template_setting | Be the first to know when we launch. | approved |  |
| 4 | `admin:system:search:seo.title` | shop | Search – KARMICARE | admin-held |  |
| 5 | `admin:system:search:seo.description` | shop | Karmicare designs biorhythmic toothpastes formulated with clean ingredients, nootropics and plant e… | admin-held |  |
| 6 | `admin:system:404:seo.title` | shop | 404 Not Found – KARMICARE | admin-held |  |
| 7 | `admin:system:collections:seo.title` | shop | Collections – KARMICARE | admin-held |  |
| 8 | `admin:system:collections:seo.description` | shop | Karmicare designs biorhythmic toothpastes formulated with clean ingredients, nootropics and plant e… | admin-held |  |
| 9 | `admin:collection:all:seo.title` | collection | Products – KARMICARE | admin-held |  |
| 10 | `admin:system:cart:seo.title` | shop | KARMICARE | admin-held |  |
| 11 | `locale:accessibility.link_messages.new_window` | theme_locale | Opens in a new window. | approved |  |
| 12 | `locale:accessibility.refresh_page` | theme_locale | Choosing a selection results in a full page refresh. | approved |  |
| 13 | `locale:accessibility.skip_to_text` | theme_locale | Skip to content | approved |  |
| 14 | `locale:blogs.article.back_to_blog` | theme_locale | Back to blog | approved |  |
| 15 | `locale:blogs.article.blog` | theme_locale | Blog | approved |  |
| 16 | `locale:blogs.article.message` | theme_locale | Comment | approved |  |
| 17 | `locale:blogs.article.name` | theme_locale | Name | approved |  |
| 18 | `locale:general.continue_shopping` | theme_locale | Continue shopping | approved |  |
| 19 | `locale:general.pagination.label` | theme_locale | Pagination | approved |  |
| 20 | `locale:general.pagination.next` | theme_locale | Next page | approved |  |
| 21 | `locale:general.pagination.page` | theme_locale | Page {{ number }} | approved |  |
| 22 | `locale:general.share.close` | theme_locale | Close share | approved |  |
| 23 | `locale:general.share.copy_to_clipboard` | theme_locale | Copy link | approved |  |
| 24 | `locale:general.share.share_url` | theme_locale | Link | approved |  |
| 25 | `locale:products.facets.apply` | theme_locale | Apply | approved |  |
| 26 | `locale:products.facets.clear` | theme_locale | Clear | approved |  |
| 27 | `locale:products.facets.clear_all` | theme_locale | Remove all | approved |  |
| 28 | `locale:products.facets.filter_and_sort` | theme_locale | Filter and sort | approved |  |
| 29 | `locale:products.facets.filter_button` | theme_locale | Filter | approved |  |
| 30 | `locale:products.facets.filter_by_label` | theme_locale | Filter: | approved |  |
| 31 | `locale:products.facets.filters_selected.one` | theme_locale | {{ count }} selected | approved |  |
| 32 | `locale:products.facets.max_price` | theme_locale | The highest price is {{ price }} | approved |  |
| 33 | `locale:products.facets.product_count_simple.other` | theme_locale | {{ count }} products | approved |  |
| 34 | `locale:products.facets.reset` | theme_locale | Reset | approved |  |
| 35 | `locale:products.facets.sort_by_label` | theme_locale | Sort by: | approved |  |
| 36 | `locale:products.product.inventory_in_stock` | theme_locale | In stock | approved |  |
| 37 | `locale:products.product.inventory_out_of_stock` | theme_locale | Out of stock | approved |  |
| 38 | `locale:products.product.nested_label` | theme_locale | {{ title }} for {{ parent_title }} | approved |  |
| 39 | `locale:products.product.quantity.label` | theme_locale | Quantity | approved |  |
| 40 | `locale:sections.cart.headings.price` | theme_locale | Price | approved |  |
| 41 | `locale:templates.contact.form.phone` | theme_locale | Phone number | approved |  |
| 42 | `locale:templates.contact.form.send` | theme_locale | Send | approved |  |
| 43 | `locale:templates.contact.form.title` | theme_locale | Contact form | approved |  |
| 44 | `locale:templates.search.page` | theme_locale | Page | approved |  |
| 45 | `locale:templates.search.products` | theme_locale | Products | approved |  |
| 46 | `locale:templates.search.results_with_count.other` | theme_locale | {{ count }} results | approved |  |
