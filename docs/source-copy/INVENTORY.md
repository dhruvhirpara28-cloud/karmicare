# EN source inventory · homepage, Duo PDP, header and footer (B1a)

The English that the live store renders on the homepage and the Duo PDP, one entry per string, with the corrections of this batch applied. NL and FR translators start from here.

- **Captured**: 2026-10-19 19:15 CEST (karmicares.myshopify.com, live theme = 3bae259). Theme text comes from this branch (`karmicare/soft-launch-source-copy`); admin-held text comes from the public live pages and `/products/<handle>.js`.
- **Machine-readable**: `en-source.json` (all entries) and `batches/<batch>.json` (one file per batch, with its digest).
- **Digest rule**: a batch digest is the sha1 over its entries' `sha1(en)` values, sorted and joined with `\n`. A later EN change alters only the digest of the batch that holds the string. `python3 docs/source-copy/digest.py` recomputes and checks every value.

| Batch | Entries | Digest |
|---|---:|---|
| `batch-01-homepage` | 221 | `b685b73d4dcdfddd153d4f130c0aa6806b9715ed` |
| `batch-02-pdp` | 477 | `03dd18b9d41a21772da2e26b7060c42f6b2364d1` |
| `batch-03-header-footer` | 41 | `e17cadb5e223dd62b25e30e901091d8a8634aaf3` |

## How to read an entry

`{id, batch, page, resource_type, file_or_handle, key_path, en, sha1, status, never_translate, notes}` as the brief asks, plus, where they apply: `old_en`/`old_sha1` (corrected strings), `claims` (ids in CLAIMS-REVIEW.md), `blocked` (no approved copy), `setting_type`, `section_type`, `rendered` (false for disabled blocks).

| status | Meaning for translators |
|---|---|
| `approved` | The live EN, accepted as the source. Translate. |
| `corrected` | Changed in this batch; `old_en` holds the previous text. Translate the new `en`. |
| `needs-review` | EN may still change: a claim waits for sign-off or an open defect is listed in `notes`. Translate, and expect a re-run when the batch digest changes. Entries with `blocked` hold `[NEEDS APPROVED COPY]`: do not translate. |
| `needs-key` | Hardcoded English in theme code (`key_path` = file:line). The localization worker must turn it into a translation key before it can be translated. |
| `admin-held` | Lives in the Shopify admin (product, metafield, metaobject, selling plan, menu, shop settings). Translate through Translate & Adapt; changes go through the admin owner. |

`resource_type` uses the brief's values plus two the brief has no slot for: `shop` (homepage title and meta description in the online-store preferences) and `navigation` (menus). Admin text captured from the live page is stored one rendered segment per entry (`key_path` ends in `#nn`), because the field structure is only visible in the admin.

## Counts

By resource type:

| Batch | template_setting | section_group | theme_locale | app | product | metafield | metaobject | shop | navigation | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `batch-01-homepage` | 189 | 0 | 21 | 9 | 0 | 0 | 0 | 2 | 0 | 221 |
| `batch-02-pdp` | 156 | 0 | 53 | 14 | 16 | 175 | 63 | 0 | 0 | 477 |
| `batch-03-header-footer` | 0 | 6 | 24 | 1 | 0 | 0 | 0 | 0 | 10 | 41 |
| **All** | **345** | **6** | **98** | **24** | **16** | **175** | **63** | **2** | **10** | **739** |

By status:

| Batch | approved | corrected | needs-review | needs-key | admin-held | never_translate |
|---|---:|---:|---:|---:|---:|---:|
| `batch-01-homepage` | 156 | 8 | 28 | 27 | 2 | 16 |
| `batch-02-pdp` | 156 | 0 | 17 | 36 | 268 | 32 |
| `batch-03-header-footer` | 17 | 1 | 2 | 10 | 11 | 5 |

Text settings: `templates/index.json` 189, `templates/product.subscription-item.json` 156, `sections/header-group.json` 2, `sections/footer-group.json` 4. The brief estimated about 149 and 119; these counts take every non-empty `text`, `textarea`, `richtext`, `inline_richtext` and non-SVG `html` value, including the sections that repeat on both templates and two disabled PDP blocks (marked `rendered: false`). Left out: 7 settings whose value is a Liquid pointer to a metafield (their text is inventoried as admin-held) and 11 technical text settings (CSS gradients, file names, a product handle, the empty Welcome Kit plan list).

| File | text | textarea | richtext | inline_richtext | html |
|---|---:|---:|---:|---:|---:|
| `templates/index.json` | 125 | 6 | 22 | 36 | 0 |
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
| 01 | `assets/chronobiology-clock-karmicare.js:91` | . Release to return to now. | aria-valuetext tail while dragging; '. Current local time.' at rest (same line) |
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
| 01 | `assets/loop-widget.js:2452` | / {{ days }} days | plan card short label ('/ year' on the Year); off-limits Loop widget file |
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
| 02 | `sections/main-product.liquid:1024` | Begin the Karmicare Year | sticky bar: schema default of sticky_cart setting 'cta_year'. The PDP template stores only button_text, so this default renders and is invisible to Translate &… |
| 02 | `sections/main-product.liquid:1030` | Try once | sticky bar: schema default of sticky_cart setting 'cta_once'. The PDP template stores only button_text, so this default renders and is invisible to Translate &… |
| 02 | `sections/main-product.liquid:1036` | Free delivery · 1–3 working days in Benelux | sticky bar: schema default of sticky_cart setting 'delivery_free'. The PDP template stores only button_text, so this default renders and is invisible to Transl… |
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

## Full inventory

Flags: **NT** never translate · **C** claim ids (CLAIMS-REVIEW.md) · **B** blocked placeholder.

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
| 11 | `index:stat_strip_karmicare/tagline` | template_setting | CHOSEN BY KPNI THERAPISTS, FUNCTIONAL DENTISTS, HEALTH ENTHUSIASTS | corrected | C C80 |
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
| 67 | `index:product_benefits_karmicare_bcQ6tp/card_VP8KGi/heading` | template_setting | Radiant calm gums | approved |  |
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
| 83 | `index:trusted_professionals_HAqYth/card_h8d3WL/text` | template_setting | Functional Dentist, kPNI Therapist | approved |  |
| 84 | `index:trusted_professionals_HAqYth/card_jcnr7Q/heading` | template_setting | Mariama Banjai | approved | NT |
| 85 | `index:trusted_professionals_HAqYth/card_jcnr7Q/text` | template_setting | Dental Hygienist, Oral Care Quality Manager | approved |  |
| 86 | `index:trusted_professionals_HAqYth/card_8dRing/heading` | template_setting | Leen Ponet | approved | NT |
| 87 | `index:trusted_professionals_HAqYth/card_8dRing/text` | template_setting | Pharmacist, Orthomolecular Therapist, kPNI Coordinator | approved |  |
| 88 | `index:trusted_professionals_HAqYth/card_8dRing/hover_text` | template_setting | “Karmicare offers fluoride-free oral care in a thoughtful way, with hydroxyapatite as a scientifica… | needs-review | C C83 |
| 89 | `index:trusted_professionals_HAqYth/card_HFdkaD/heading` | template_setting | Dr. Iveta Pleša Rutule | approved | NT |
| 90 | `index:trusted_professionals_HAqYth/card_HFdkaD/text` | template_setting | Holistic Dentist | approved |  |
| 91 | `index:trusted_professionals_HAqYth/card_Ah46TM/heading` | template_setting | Dr. Kris Sienaert | needs-review | NT |
| 92 | `index:trusted_professionals_HAqYth/card_Ah46TM/text` | template_setting | Former GP, Lifestyle Medicine | approved |  |
| 93 | `index:trusted_professionals_HAqYth/card_CtQgU9/heading` | template_setting | Sietske Hamelink | approved | NT |
| 94 | `index:trusted_professionals_HAqYth/card_CtQgU9/text` | template_setting | Nutritional Therapist, Menstrual Cycle Expert | approved |  |
| 95 | `index:trusted_professionals_HAqYth/card_CtQgU9/hover_text` | template_setting | “As a nutritional therapist specialized in female hormones, I’m extremely careful about what I put … | needs-review | C C84,C85 |
| 96 | `index:trusted_professionals_HAqYth/card_qAPajg/heading` | template_setting | Kim Verlot | approved | NT |
| 97 | `index:trusted_professionals_HAqYth/card_qAPajg/text` | template_setting | Breathing Coach, Heart Coherence Specialist | approved |  |
| 98 | `index:research_behind_system_EkjATL/subheading` | template_setting | CLINICALLY BACKED ORAL CARE | approved |  |
| 99 | `index:research_behind_system_EkjATL/heading` | template_setting | The research behind the system | approved |  |
| 100 | `index:research_behind_system_EkjATL/bottom_text` | template_setting | Built for people who read the label, check the research and want their daily care to hold up. Meta-… | approved |  |
| 101 | `index:research_behind_system_EkjATL/button_label` | template_setting | Explore the full evidence base | approved |  |
| 102 | `index:research_behind_system_EkjATL/card_bDxUVT/subheading` | template_setting | NANO-HYDROXYAPATITE | approved |  |
| 103 | `index:research_behind_system_EkjATL/card_bDxUVT/heading` | template_setting | Nano-HAp sealed 98% of open dentine tubules. | needs-review | C C60 |
| 104 | `index:research_behind_system_EkjATL/card_bDxUVT/subtext` | template_setting | Human dentine discs · 7 days | approved |  |
| 105 | `index:research_behind_system_EkjATL/card_bDxUVT/result_label` | template_setting | RESULT | approved |  |
| 106 | `index:research_behind_system_EkjATL/card_bDxUVT/result_text` | template_setting | 98% occlusion vs 82% and 65% for two other desensitising technologies | approved |  |
| 107 | `index:research_behind_system_EkjATL/card_bDxUVT/method_label` | template_setting | METHOD | approved |  |
| 108 | `index:research_behind_system_EkjATL/card_bDxUVT/method_text` | template_setting | In vitro SEM comparison of three pastes, ~1% nHAp. | approved |  |
| 109 | `index:research_behind_system_EkjATL/card_bDxUVT/link_label` | template_setting | Kulal et al. · 2016 · J Clin Diagn Res | approved | NT |
| 110 | `index:research_behind_system_EkjATL/card_bDxUVT/image_badge` | template_setting | DENTINE TUBULES · OPEN AND OCCLUDED | approved |  |
| 111 | `index:research_behind_system_EkjATL/card_yMiD9D/subheading` | template_setting | ORAL–SLEEP CONNECTION | approved |  |
| 112 | `index:research_behind_system_EkjATL/card_yMiD9D/heading` | template_setting | Poorer oral health was linked with poorer sleep. | needs-review | C C61 |
| 113 | `index:research_behind_system_EkjATL/card_yMiD9D/subtext` | template_setting | 36,559 people · 8 studies | approved |  |
| 114 | `index:research_behind_system_EkjATL/card_yMiD9D/result_label` | template_setting | RESULT | approved |  |
| 115 | `index:research_behind_system_EkjATL/card_yMiD9D/result_text` | template_setting | SMD 2.17 · p = 0.004 · 95% CI 0.68–3.66&nbsp; | approved |  |
| 116 | `index:research_behind_system_EkjATL/card_yMiD9D/method_label` | template_setting | METHOD | approved |  |
| 117 | `index:research_behind_system_EkjATL/card_yMiD9D/method_text` | template_setting | Meta-analysis of 8 studies, 2015–2023. | approved |  |
| 118 | `index:research_behind_system_EkjATL/card_yMiD9D/link_label` | template_setting | Lei & Hu · 2025 · Biomedical Reports | approved | NT |
| 119 | `index:research_behind_system_EkjATL/card_yMiD9D/image_badge` | template_setting | SLEEP · AIRWAY AND ORAL CAVITY | approved |  |
| 120 | `index:research_behind_system_EkjATL/card_fmFMFd/subheading` | template_setting | XYLITOL | approved |  |
| 121 | `index:research_behind_system_EkjATL/card_fmFMFd/heading` | template_setting | Xylitol lowered tooth decay compared with controls. | needs-review | C C62 |
| 122 | `index:research_behind_system_EkjATL/card_fmFMFd/subtext` | template_setting | 1,478 people · 7 trials | approved |  |
| 123 | `index:research_behind_system_EkjATL/card_fmFMFd/result_label` | template_setting | Result | approved |  |
| 124 | `index:research_behind_system_EkjATL/card_fmFMFd/result_text` | template_setting | SMD −1.09 · p < 0.00001 · 95% CI −1.34 to −0.83 | approved |  |
| 125 | `index:research_behind_system_EkjATL/card_fmFMFd/method_label` | template_setting | Method | approved |  |
| 126 | `index:research_behind_system_EkjATL/card_fmFMFd/method_text` | template_setting | Systematic review and meta-analysis of 7 clinical trials. | approved |  |
| 127 | `index:research_behind_system_EkjATL/card_fmFMFd/link_label` | template_setting | Janakiram et al. · 2017 · J Nat Sci Biol Med | approved | NT |
| 128 | `index:research_behind_system_EkjATL/card_fmFMFd/image_badge` | template_setting | DENTINE TUBULES · OPEN AND OCCLUDED | approved |  |
| 129 | `index:research_behind_system_EkjATL/card_Hi7YUD/subheading` | template_setting | NANO-HYDROXYAPATITE | approved |  |
| 130 | `index:research_behind_system_EkjATL/card_Hi7YUD/heading` | template_setting | Nano-HAp beat fluoride on tooth sensitivity. | needs-review | C C63 |
| 131 | `index:research_behind_system_EkjATL/card_Hi7YUD/subtext` | template_setting | 105 people · 4 weeks | approved |  |
| 132 | `index:research_behind_system_EkjATL/card_Hi7YUD/result_label` | template_setting | RESULT | approved |  |
| 133 | `index:research_behind_system_EkjATL/card_Hi7YUD/result_text` | template_setting | Lower cold-air and tactile sensitivity vs fluoride and placebo, p < 0.05 | approved |  |
| 134 | `index:research_behind_system_EkjATL/card_Hi7YUD/method_label` | template_setting | METHOD | approved |  |
| 135 | `index:research_behind_system_EkjATL/card_Hi7YUD/method_text` | template_setting | Double-blind randomised controlled trial, three arms. | approved |  |
| 136 | `index:research_behind_system_EkjATL/card_Hi7YUD/link_label` | template_setting | Vano et al. · 2018 · Clin Oral Investig | approved | NT |
| 137 | `index:research_behind_system_EkjATL/card_Hi7YUD/image_badge` | template_setting | DENTINE TUBULES · OPEN AND OCCLUDED | approved |  |
| 138 | `index:research_behind_system_EkjATL/card_JeERX6/subheading` | template_setting | SLS-FREE | approved |  |
| 139 | `index:research_behind_system_EkjATL/card_JeERX6/heading` | template_setting | No SLS meant fewer and shorter canker sores. | needs-review | C C64 |
| 140 | `index:research_behind_system_EkjATL/card_JeERX6/subtext` | template_setting | 124 people · 4 crossover RCTs | approved |  |
| 141 | `index:research_behind_system_EkjATL/card_JeERX6/result_label` | template_setting | RESULT | approved |  |
| 142 | `index:research_behind_system_EkjATL/card_JeERX6/result_text` | template_setting | Fewer ulcers, shorter duration, fewer episodes, less pain | approved |  |
| 143 | `index:research_behind_system_EkjATL/card_JeERX6/method_label` | template_setting | METHOD | approved |  |
| 144 | `index:research_behind_system_EkjATL/card_JeERX6/method_text` | template_setting | Systematic review and meta-analysis of 4 crossover RCTs. | approved |  |
| 145 | `index:research_behind_system_EkjATL/card_JeERX6/link_label` | template_setting | Alli et al. · 2019 · J Oral Pathol Med | approved | NT |
| 146 | `index:research_behind_system_EkjATL/card_JeERX6/image_badge` | template_setting | DENTINE TUBULES · OPEN AND OCCLUDED | approved |  |
| 147 | `index:km_faq_accordion_FYcArV/heading` | template_setting | Before you start | approved |  |
| 148 | `index:km_faq_accordion_FYcArV/subtext` | template_setting | Everything people usually ask before switching to a day-and-night oral care system. | approved |  |
| 149 | `index:km_faq_accordion_FYcArV/faq_item_TNnqTQ/category` | template_setting | The system | approved |  |
| 150 | `index:km_faq_accordion_FYcArV/faq_item_TNnqTQ/question` | template_setting | Why two formulas instead of one? | approved |  |
| 151 | `index:km_faq_accordion_FYcArV/faq_item_TNnqTQ/answer` | template_setting | Because your mouth doesn’t do the same job all day. Daytime is exposure — acids, sugars, coffee — s… | approved | C C25 |
| 152 | `index:km_faq_accordion_FYcArV/faq_item_kLMHax/category` | template_setting | Ingredients & safety | approved |  |
| 153 | `index:km_faq_accordion_FYcArV/faq_item_kLMHax/question` | template_setting | Is Karmicare fluoride-free? | approved |  |
| 154 | `index:km_faq_accordion_FYcArV/faq_item_kLMHax/answer` | template_setting | [NEEDS APPROVED COPY] | needs-review | B |
| 155 | `index:km_faq_accordion_FYcArV/faq_item_7jmEGi/category` | template_setting | The ritual | needs-review |  |
| 156 | `index:km_faq_accordion_FYcArV/faq_item_7jmEGi/question` | template_setting | Will Karmicare offer a biorhythmic toothpaste with fluoride? | approved |  |
| 157 | `index:km_faq_accordion_FYcArV/faq_item_7jmEGi/answer` | template_setting | [NEEDS APPROVED COPY] | needs-review | B |
| 158 | `index:km_faq_accordion_FYcArV/faq_item_AL3DKF/category` | template_setting | Results | needs-review |  |
| 159 | `index:km_faq_accordion_FYcArV/faq_item_AL3DKF/question` | template_setting | What is nano-hydroxyapatite? | approved |  |
| 160 | `index:km_faq_accordion_FYcArV/faq_item_AL3DKF/answer` | template_setting | A bioidentical mineral — the same substance your enamel is made of. It remineralises teeth, reduces… | corrected | C C23 |
| 161 | `index:km_faq_accordion_FYcArV/faq_item_qUxYCn/category` | template_setting | Plans & Return on Care | needs-review |  |
| 162 | `index:km_faq_accordion_FYcArV/faq_item_qUxYCn/question` | template_setting | Should I rinse after brushing? | approved |  |
| 163 | `index:km_faq_accordion_FYcArV/faq_item_qUxYCn/answer` | template_setting | No — spit and carry on. Karmicare formulas are certified safe to remain in your mouth, giving nHAp … | corrected | C C13 |
| 164 | `index:km_faq_accordion_FYcArV/faq_item_4KMG6C/category` | template_setting | Shipping & guarantee | needs-review |  |
| 165 | `index:km_faq_accordion_FYcArV/faq_item_4KMG6C/question` | template_setting | How quickly will I notice a difference? | approved |  |
| 166 | `index:km_faq_accordion_FYcArV/faq_item_4KMG6C/answer` | template_setting | Mineral remineralisation takes time — most members feel the sensitivity shift in 2–4 weeks and see … | corrected | C C24 |
| 167 | `index:featured_product_3XpDKw/title_4znD88/custom_title` | template_setting | Your welcome kit includes | approved |  |
| 168 | `index:featured_product_3XpDKw/loop_subscriptions_7dde8c/pricing_summary_care_credit_title` | template_setting | Care Credits back | approved |  |
| 169 | `index:featured_product_3XpDKw/loop_subscriptions_7dde8c/subscription_title` | template_setting | Awake & Asleep AM/PM Oral Care System | approved |  |
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
| 202 | `liquid:assets/chronobiology-clock-karmicare.js:11` | theme_locale | saliva is only now picking up after the night, and the enamel is least protected before your first … | needs-key | C C54 |
| 203 | `liquid:assets/chronobiology-clock-karmicare.js:12` | theme_locale | breakfast and coffee dropped the pH within minutes — saliva spends the next half hour bringing it b… | needs-key |  |
| 204 | `liquid:assets/chronobiology-clock-karmicare.js:13` | theme_locale | lunch restarts the cycle: every eating occasion opens a fresh acid window, whatever its size | needs-key |  |
| 205 | `liquid:assets/chronobiology-clock-karmicare.js:14` | theme_locale | grazing hours — the most frequent acid challenge of the day, and it is how often, not how much | needs-key |  |
| 206 | `liquid:assets/chronobiology-clock-karmicare.js:15` | theme_locale | the last big acid window of the day; after this, saliva starts winding down | needs-key |  |
| 207 | `liquid:assets/chronobiology-clock-karmicare.js:16` | theme_locale | melatonin is rising and salivary flow is dropping — what is left on the enamel now stays for hours | needs-key |  |
| 208 | `liquid:assets/chronobiology-clock-karmicare.js:17` | theme_locale | saliva is near its minimum and clearance has almost stopped: the longest unguarded stretch, and the… | needs-key |  |
| 209 | `liquid:sections/km-faq-accordion.liquid:155` | theme_locale | ALL | needs-key |  |
| 210 | `liquid:sections/featured-product.liquid:627` | theme_locale | Free | needs-key |  |
| 211 | `liquid:snippets/loop-widget-standard.liquid:101` | app | Start here | needs-key |  |
| 212 | `liquid:snippets/loop-widget-standard.liquid:103` | app | Choose how to begin | needs-key |  |
| 213 | `liquid:snippets/loop-widget-standard.liquid:109` | app | Selling Plans | needs-key |  |
| 214 | `liquid:snippets/loop-widget-standard.liquid:123` | app | One time Purchase | needs-key |  |
| 215 | `liquid:snippets/loop-widget-standard.liquid:140` | app | each | needs-key |  |
| 216 | `liquid:assets/loop-widget.js:2452` | app | / {{ days }} days | needs-key |  |
| 217 | `liquid:assets/loop-widget.js:2468` | app | Renews every year | needs-key |  |
| 218 | `liquid:assets/loop-widget.js:2213` | app | {{ value }} value · free | needs-key |  |
| 219 | `liquid:snippets/loop-subscriptions.liquid:10` | app | Rendering loop-subscriptions | needs-key |  |
| 220 | `admin:shop:online_store.preferences.homepage_title` | shop | KARMICARE - Biorhythmic Oral Health | admin-held |  |
| 221 | `admin:shop:online_store.preferences.homepage_meta_description` | shop | Karmicare designs biorhythmic toothpastes formulated with clean ingredients, nootropics and plant e… | admin-held |  |

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
| 20 | `product.subscription-item:main/buy_buttons/custom_button_text_by_plan` | template_setting | 712106115453: Start my 60-Day rhythm 712155431293: Start my Karmicare Year | approved |  |
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
| 49 | `product.subscription-item:trusted_professionals_HAqYth/card_h8d3WL/text` | template_setting | Functional Dentist, kPNI Therapist | approved |  |
| 50 | `product.subscription-item:trusted_professionals_HAqYth/card_jcnr7Q/heading` | template_setting | Mariama Banjai | approved | NT |
| 51 | `product.subscription-item:trusted_professionals_HAqYth/card_jcnr7Q/text` | template_setting | Dental Hygienist, Oral Care Quality Manager | approved |  |
| 52 | `product.subscription-item:trusted_professionals_HAqYth/card_8dRing/heading` | template_setting | Leen Ponet | approved | NT |
| 53 | `product.subscription-item:trusted_professionals_HAqYth/card_8dRing/text` | template_setting | Pharmacist, Orthomolecular Therapist, kPNI Coordinator | approved |  |
| 54 | `product.subscription-item:trusted_professionals_HAqYth/card_8dRing/hover_text` | template_setting | “Karmicare offers fluoride-free oral care in a thoughtful way, with hydroxyapatite as a scientifica… | needs-review | C C83 |
| 55 | `product.subscription-item:trusted_professionals_HAqYth/card_HFdkaD/heading` | template_setting | Dr. Iveta Pleša Rutule | approved | NT |
| 56 | `product.subscription-item:trusted_professionals_HAqYth/card_HFdkaD/text` | template_setting | Holistic Dentist | approved |  |
| 57 | `product.subscription-item:trusted_professionals_HAqYth/card_Ah46TM/heading` | template_setting | Dr. Kris Sienaert | needs-review | NT |
| 58 | `product.subscription-item:trusted_professionals_HAqYth/card_Ah46TM/text` | template_setting | Former GP, Lifestyle Medicine | approved |  |
| 59 | `product.subscription-item:trusted_professionals_HAqYth/card_CtQgU9/heading` | template_setting | Sietske Hamelink | approved | NT |
| 60 | `product.subscription-item:trusted_professionals_HAqYth/card_CtQgU9/text` | template_setting | Nutritional Therapist, Menstrual Cycle Expert | approved |  |
| 61 | `product.subscription-item:trusted_professionals_HAqYth/card_CtQgU9/hover_text` | template_setting | “As a nutritional therapist specialized in female hormones, I’m extremely careful about what I put … | needs-review | C C84,C85 |
| 62 | `product.subscription-item:trusted_professionals_HAqYth/card_qAPajg/heading` | template_setting | Kim Verlot | approved | NT |
| 63 | `product.subscription-item:trusted_professionals_HAqYth/card_qAPajg/text` | template_setting | Breathing Coach, Heart Coherence Specialist | approved |  |
| 64 | `product.subscription-item:how_it_works_steps_aAgVmF/subtitle` | template_setting | The Ritual | approved |  |
| 65 | `product.subscription-item:how_it_works_steps_aAgVmF/title` | template_setting | How Karmicare works. | approved |  |
| 66 | `product.subscription-item:how_it_works_steps_aAgVmF/description` | template_setting | Become a pro at brushing. Feel your teeth by sliding your tongue. | approved |  |
| 67 | `product.subscription-item:how_it_works_steps_aAgVmF/hint_text` | template_setting | Preview · sound off | approved |  |
| 68 | `product.subscription-item:how_it_works_steps_aAgVmF/bottom_text` | template_setting | Not to be combined with fluoride oral care. One duo lasts 64 days at two brushings a day. | approved | C C07 |
| 69 | `product.subscription-item:how_it_works_steps_aAgVmF/step_U7HiXT/number` | template_setting | 02 | approved |  |
| 70 | `product.subscription-item:how_it_works_steps_aAgVmF/step_U7HiXT/title` | template_setting | Pump and brush | approved |  |
| 71 | `product.subscription-item:how_it_works_steps_aAgVmF/step_U7HiXT/description` | template_setting | Apply one pump and brush gently for two minutes. | approved |  |
| 72 | `product.subscription-item:how_it_works_steps_aAgVmF/step_EBicgt/number` | template_setting | 03 | approved |  |
| 73 | `product.subscription-item:how_it_works_steps_aAgVmF/step_EBicgt/title` | template_setting | Spit, no rinse | approved |  |
| 74 | `product.subscription-item:how_it_works_steps_aAgVmF/step_EBicgt/description` | template_setting | Spit out the excess. Do not rinse afterwards. | approved |  |
| 75 | `product.subscription-item:research_behind_system_EkjATL/subheading` | template_setting | CLINICALLY BACKED ORAL CARE | approved |  |
| 76 | `product.subscription-item:research_behind_system_EkjATL/heading` | template_setting | The research behind the system | approved |  |
| 77 | `product.subscription-item:research_behind_system_EkjATL/bottom_text` | template_setting | Built for people who read the label, check the research and want their daily care to hold up. Meta-… | approved |  |
| 78 | `product.subscription-item:research_behind_system_EkjATL/button_label` | template_setting | Explore the full evidence base | approved |  |
| 79 | `product.subscription-item:research_behind_system_EkjATL/card_bDxUVT/subheading` | template_setting | NANO-HYDROXYAPATITE | approved |  |
| 80 | `product.subscription-item:research_behind_system_EkjATL/card_bDxUVT/heading` | template_setting | Nano-HAp sealed 98% of open dentine tubules. | needs-review | C C60 |
| 81 | `product.subscription-item:research_behind_system_EkjATL/card_bDxUVT/subtext` | template_setting | Human dentine discs · 7 days | approved |  |
| 82 | `product.subscription-item:research_behind_system_EkjATL/card_bDxUVT/result_label` | template_setting | RESULT | approved |  |
| 83 | `product.subscription-item:research_behind_system_EkjATL/card_bDxUVT/result_text` | template_setting | 98% occlusion vs 82% and 65% for two other desensitising technologies | approved |  |
| 84 | `product.subscription-item:research_behind_system_EkjATL/card_bDxUVT/method_label` | template_setting | METHOD | approved |  |
| 85 | `product.subscription-item:research_behind_system_EkjATL/card_bDxUVT/method_text` | template_setting | In vitro SEM comparison of three pastes, ~1% nHAp. | approved |  |
| 86 | `product.subscription-item:research_behind_system_EkjATL/card_bDxUVT/link_label` | template_setting | Kulal et al. · 2016 · J Clin Diagn Res | approved | NT |
| 87 | `product.subscription-item:research_behind_system_EkjATL/card_bDxUVT/image_badge` | template_setting | DENTINE TUBULES · OPEN AND OCCLUDED | approved |  |
| 88 | `product.subscription-item:research_behind_system_EkjATL/card_yMiD9D/subheading` | template_setting | ORAL–SLEEP CONNECTION | approved |  |
| 89 | `product.subscription-item:research_behind_system_EkjATL/card_yMiD9D/heading` | template_setting | Poorer oral health was linked with poorer sleep. | needs-review | C C61 |
| 90 | `product.subscription-item:research_behind_system_EkjATL/card_yMiD9D/subtext` | template_setting | 36,559 people · 8 studies | approved |  |
| 91 | `product.subscription-item:research_behind_system_EkjATL/card_yMiD9D/result_label` | template_setting | RESULT | approved |  |
| 92 | `product.subscription-item:research_behind_system_EkjATL/card_yMiD9D/result_text` | template_setting | SMD 2.17 · p = 0.004 · 95% CI 0.68–3.66&nbsp; | approved |  |
| 93 | `product.subscription-item:research_behind_system_EkjATL/card_yMiD9D/method_label` | template_setting | METHOD | approved |  |
| 94 | `product.subscription-item:research_behind_system_EkjATL/card_yMiD9D/method_text` | template_setting | Meta-analysis of 8 studies, 2015–2023. | approved |  |
| 95 | `product.subscription-item:research_behind_system_EkjATL/card_yMiD9D/link_label` | template_setting | Lei & Hu · 2025 · Biomedical Reports | approved | NT |
| 96 | `product.subscription-item:research_behind_system_EkjATL/card_yMiD9D/image_badge` | template_setting | SLEEP · AIRWAY AND ORAL CAVITY | approved |  |
| 97 | `product.subscription-item:research_behind_system_EkjATL/card_fmFMFd/subheading` | template_setting | XYLITOL | approved |  |
| 98 | `product.subscription-item:research_behind_system_EkjATL/card_fmFMFd/heading` | template_setting | Xylitol lowered tooth decay compared with controls. | needs-review | C C62 |
| 99 | `product.subscription-item:research_behind_system_EkjATL/card_fmFMFd/subtext` | template_setting | 1,478 people · 7 trials | approved |  |
| 100 | `product.subscription-item:research_behind_system_EkjATL/card_fmFMFd/result_label` | template_setting | Result | approved |  |
| 101 | `product.subscription-item:research_behind_system_EkjATL/card_fmFMFd/result_text` | template_setting | SMD −1.09 · p < 0.00001 · 95% CI −1.34 to −0.83 | approved |  |
| 102 | `product.subscription-item:research_behind_system_EkjATL/card_fmFMFd/method_label` | template_setting | Method | approved |  |
| 103 | `product.subscription-item:research_behind_system_EkjATL/card_fmFMFd/method_text` | template_setting | Systematic review and meta-analysis of 7 clinical trials. | approved |  |
| 104 | `product.subscription-item:research_behind_system_EkjATL/card_fmFMFd/link_label` | template_setting | Janakiram et al. · 2017 · J Nat Sci Biol Med | approved | NT |
| 105 | `product.subscription-item:research_behind_system_EkjATL/card_fmFMFd/image_badge` | template_setting | DENTINE TUBULES · OPEN AND OCCLUDED | approved |  |
| 106 | `product.subscription-item:research_behind_system_EkjATL/card_Hi7YUD/subheading` | template_setting | NANO-HYDROXYAPATITE | approved |  |
| 107 | `product.subscription-item:research_behind_system_EkjATL/card_Hi7YUD/heading` | template_setting | Nano-HAp beat fluoride on tooth sensitivity. | needs-review | C C63 |
| 108 | `product.subscription-item:research_behind_system_EkjATL/card_Hi7YUD/subtext` | template_setting | 105 people · 4 weeks | approved |  |
| 109 | `product.subscription-item:research_behind_system_EkjATL/card_Hi7YUD/result_label` | template_setting | RESULT | approved |  |
| 110 | `product.subscription-item:research_behind_system_EkjATL/card_Hi7YUD/result_text` | template_setting | Lower cold-air and tactile sensitivity vs fluoride and placebo, p < 0.05 | approved |  |
| 111 | `product.subscription-item:research_behind_system_EkjATL/card_Hi7YUD/method_label` | template_setting | METHOD | approved |  |
| 112 | `product.subscription-item:research_behind_system_EkjATL/card_Hi7YUD/method_text` | template_setting | Double-blind randomised controlled trial, three arms. | approved |  |
| 113 | `product.subscription-item:research_behind_system_EkjATL/card_Hi7YUD/link_label` | template_setting | Vano et al. · 2018 · Clin Oral Investig | approved | NT |
| 114 | `product.subscription-item:research_behind_system_EkjATL/card_Hi7YUD/image_badge` | template_setting | DENTINE TUBULES · OPEN AND OCCLUDED | approved |  |
| 115 | `product.subscription-item:research_behind_system_EkjATL/card_JeERX6/subheading` | template_setting | SLS-FREE | approved |  |
| 116 | `product.subscription-item:research_behind_system_EkjATL/card_JeERX6/heading` | template_setting | No SLS meant fewer and shorter canker sores. | needs-review | C C64 |
| 117 | `product.subscription-item:research_behind_system_EkjATL/card_JeERX6/subtext` | template_setting | 124 people · 4 crossover RCTs | approved |  |
| 118 | `product.subscription-item:research_behind_system_EkjATL/card_JeERX6/result_label` | template_setting | RESULT | approved |  |
| 119 | `product.subscription-item:research_behind_system_EkjATL/card_JeERX6/result_text` | template_setting | Fewer ulcers, shorter duration, fewer episodes, less pain | approved |  |
| 120 | `product.subscription-item:research_behind_system_EkjATL/card_JeERX6/method_label` | template_setting | METHOD | approved |  |
| 121 | `product.subscription-item:research_behind_system_EkjATL/card_JeERX6/method_text` | template_setting | Systematic review and meta-analysis of 4 crossover RCTs. | approved |  |
| 122 | `product.subscription-item:research_behind_system_EkjATL/card_JeERX6/link_label` | template_setting | Alli et al. · 2019 · J Oral Pathol Med | approved | NT |
| 123 | `product.subscription-item:research_behind_system_EkjATL/card_JeERX6/image_badge` | template_setting | DENTINE TUBULES - OPEN AND OCCLUDED | approved |  |
| 124 | `product.subscription-item:featured_product_Eb93Xa/title_GDDYEK/custom_title` | template_setting | Your welcome kit includes | approved |  |
| 125 | `product.subscription-item:featured_product_Eb93Xa/loop_subscriptions_gPKypi/pricing_summary_care_credit_title` | template_setting | Care Credits back | approved |  |
| 126 | `product.subscription-item:featured_product_Eb93Xa/loop_subscriptions_gPKypi/subscription_title` | template_setting | Awake & Asleep AM/PM Oral Care System | approved |  |
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
| 189 | `liquid:sections/main-product.liquid:1024` | theme_locale | Begin the Karmicare Year | needs-key |  |
| 190 | `liquid:sections/main-product.liquid:1030` | theme_locale | Try once | needs-key |  |
| 191 | `liquid:sections/main-product.liquid:1036` | theme_locale | Free delivery · 1–3 working days in Benelux | needs-key |  |
| 192 | `liquid:sections/main-product.liquid:1042` | theme_locale | Shipping calculated at checkout | needs-key |  |
| 193 | `liquid:sections/main-product.liquid:1049` | theme_locale | Welcome Kit: two toothbrushes + floss | needs-key |  |
| 194 | `liquid:sections/main-product.liquid:1055` | theme_locale | 60-day money-back guarantee | needs-key |  |
| 195 | `liquid:sections/main-product.liquid:1061` | theme_locale | 14-day money-back guarantee | needs-key |  |
| 196 | `liquid:sections/main-product.liquid:1067` | theme_locale | Pause or stop anytime | needs-key |  |
| 197 | `liquid:sections/main-product.liquid:1073` | theme_locale | Renews yearly · stop anytime before renewal | needs-key |  |
| 198 | `liquid:sections/main-product.liquid:1080` | theme_locale | [per_brushing] per brushing | needs-key |  |
| 199 | `liquid:sections/main-product.liquid:1087` | theme_locale | Not ready for a membership? Try once for [price] | needs-key |  |
| 200 | `liquid:sections/main-product.liquid:1098` | theme_locale | Awake & Asleep AM/PM Oral Care System | needs-key |  |
| 201 | `liquid:sections/main-product.liquid:1104` | theme_locale | Free | needs-key |  |
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
| 228 | `admin:karmicare-biorhythmic-oral-care-system:media.69271648010621.alt` | product | Karmicare Biorhythmic Oral Care Kit: fluoride-free, SLS-free Awake morning and Asleep evening tooth… | admin-held |  |
| 229 | `admin:karmicare-biorhythmic-oral-care-system:media.69248905085309.alt` | product | Karmicare Biorhythmic Oral Care Duo Set: Awake morning and Asleep evening toothpaste, fluoride-free… | admin-held |  |
| 230 | `admin:karmicare-biorhythmic-oral-care-system:media.69840178282877.alt` | product | Karmicare Awake morning and Asleep evening toothpaste, fluoride-free, SLS-free and rich in nano-hyd… | admin-held |  |
| 231 | `admin:karmicare-biorhythmic-oral-care-system:media.69840178020733.alt` | product | Karmicare chronobiology infographic: your mouth runs on a 24-hour clock, with evening care at 22:00… | admin-held |  |
| 232 | `admin:karmicare-biorhythmic-oral-care-system:media.69840178250109.alt` | product | Karmicare Awake morning toothpaste, fluoride-free, SLS-free and rich in nano-hydroxyapatite, with g… | admin-held |  |
| 233 | `admin:karmicare-biorhythmic-oral-care-system:media.69840178315645.alt` | product | Karmicare Asleep evening toothpaste, fluoride-free, SLS-free and rich in nano-hydroxyapatite, with … | admin-held |  |
| 234 | `admin:karmicare-biorhythmic-oral-care-system:media.69840177987965.alt` | product | How to use Karmicare: rinse first, use 1 pump, spit and don't rinse. Leave-on toothpaste, fluoride-… | admin-held |  |
| 235 | `admin:karmicare-biorhythmic-oral-care-system:media.69840178381181.alt` | product | Karmicare nano-hydroxyapatite explainer showing nHAp crystals at the enamel surface | admin-held |  |
| 236 | `admin:karmicare-biorhythmic-oral-care-system:media.69884688236925.alt` | product | Animated view of the Karmicare Biorhythmic Oral Care Kit: fluoride-free, SLS-free Awake morning and… | admin-held |  |
| 237 | `admin:morning-toothbrush-2-0:title` | product | Morning Toothbrush 2.0 | admin-held |  |
| 238 | `admin:evening-toothbrush-2-0:title` | product | Evening Toothbrush 2.0 | admin-held |  |
| 239 | `admin:whitening-charcoal-dental-floss:title` | product | Whitening Charcoal Floss | admin-held |  |
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
| 250 | `admin:karmicare-biorhythmic-oral-care-system:custom.treatment_journey_*#11` | metafield | — calmer gums, fresher breath, morning and night | admin-held |  |
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
| 324 | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#56` | metafield | Safety-assessed for leave-on use | admin-held |  |
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
| 363 | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#95` | metafield | Leave-on safe | admin-held |  |
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
| 477 | `admin:karmicare-biorhythmic-oral-care-system:custom.compare_table:welcome_kit_row.products` | metaobject | Morning Toothbrush · Evening Toothbrush · Whitening Charcoal Floss | admin-held |  |

### `batch-03-header-footer`

| # | id | type | EN | status | flags |
|---:|---|---|---|---|---|
| 1 | `header-group:announcement-bar/announcement-bar-0/text` | section_group | COMPLIMENTARY SHIPPING · 60-DAY MONEY-BACK GUARANTEE · BELGIAN-MADE | needs-review |  |
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
