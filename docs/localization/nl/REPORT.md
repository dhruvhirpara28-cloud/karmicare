# NL translation payloads · report (B2)

Task `task_25fdff87b2e8`, Orca run `run_32dd5602b983`, branch `karmicare/soft-launch-source-copy`. 19 Oct 2026. Ready for Astra's review.

Dutch for every page of the live store, translated from the approved EN inventory. The files are payloads only. Nothing is in the theme, `locales/` or the Shopify admin yet; the localization worker registers them later.

**R1 update (task `task_07508030e174`).** After the B1a review fixes, batch 01 has a new digest (`a09219ae1af8`, 225 entries). The four new runtime strings (F3) are translated as `theme-key`. Statuses are refreshed for the F1/F2 claim links: the research result lines, evidence counts and leave-on safety lines are now `pending-claim-review`, and the "Radiant calm gums" heading is held with the rest of benefit card 06. Counts below are current.

## What is here

| File | Content |
|---|---|
| `batch-0{1..8}-*.json` | One file per EN batch: `source_digest` (the EN batch it was translated from), `counts`, `fit_risk` ids, and one entry per EN entry: `{id, resource_type, file_or_handle, key_path, en, en_sha1, nl, status, flags, notes}`. |
| `validate.py` | `python3 docs/localization/nl/validate.py` checks every file against `docs/source-copy/en-source.json`: digests, coverage, `en_sha1`, Dutch present except on held entries. It exits 0 today. |
| `REPORT.md` | This file. |

**Statuses.** Each status names the strongest flag on the entry; `flags` lists all of them.
- `translated`: ready to register.
- `admin`: register through Shopify's translation resources (product, metafield, metaobject, page, policy, article, collection, menu, selling plan, app).
- `theme-key`: hardcoded EN; goes into `locales/nl.json` once the key exists.
- `legal-review`: needs Victor's or a lawyer's review before publishing.
- `pending-claim-review`: translated faithfully; the EN claim is waiting for sign-off.
- `dawn-nl`: Dawn's own key, already in `locales/nl.json` (verified, not re-translated).
- `held`: not translated; the reason is in `notes`.

## How it was made

1. **Order** (brief):
   - First, the EN inventory was extended with batches 04–08, the whole sitemap plus the seven Shopify policy pages (commits `42f5f12`, `5e4f426`).
   - Then NL was translated in the order 02, 01, 03, 04–08.
2. **Translators.**
   - Five translator agents worked from one rulebook: `docs/source-copy/GLOSSARY.md` (binding), *je/jouw*, EN brand terms, the never-translate list, the number format, markup and tokens, cosmetic claim verbs, fit, and Belgian legal Dutch.
   - The chunks were the PDP; homepage, header, footer, products, content and system pages; and the three legal groups. Each legal text was translated together with its Shopify policy twin.
   - I translated the two blog chunks (593 entries) myself.
3. **Checker.** Every chunk passed it with 0 errors. It checks:
   - HTML tags in the same order, unchanged `href`s, tokens, protected terms;
   - e-mail and company numbers, and numbers;
   - *u/uw*, banned commodity words, claim verbs that were not in the EN;
   - fit length.

   All remaining warnings are explained in the entry notes: section numbers next to €, article subheadings, and *voorkomt* meaning "occurs".
4. **Approved NL reused.** The approved Figma translation *Dutch offer 2.0 · NL* (`3738:27474`, 2 Oct, read-only) replaced the translator's wording in 62 entries where the EN matches exactly. Exceptions:
   - The buy-box trust row keeps Figma's own short forms (*60 dagen geld terug*, *Pauzeren of opzeggen*).
   - The site-wide glossary term *controlebeloning* wins over Figma's one-off *tandartscontrole-beloning*.
5. **Consistency.** Where the same EN got different Dutch in different chunks, one form was chosen:
   - product titles that were inventoried twice;
   - the research cards;
   - the members' disclaimer;
   - *Abonneer en bespaar*;
   - repeated legal lines (the refund policy follows the terms).

   Only the two deliberate trust-row short forms still differ.
6. **Claims.** A claims review of batches 05–07 judged 541 blocks by hand: 33 approved, 261 needs-review, 113 unsupported, 134 without a claim (`CLAIMS-REVIEW.md`). Unsupported blocks are held; needs-review blocks are translated faithfully and flagged.
7. **Dawn keys.** 64 Dawn keys render on the inventoried pages. All 64 are present in `locales/nl.json`. The five that equal the EN (*Menu*, *Blog*, *Link*, *Filter*, *Filter:*) are correct Dutch.

## Held entries, and why

- **never-translate (51):** selling-plan IDs, the Subscription Name keys "60-Day Supply" / "Year Supply", INCI lists, practitioners' names, citations, Awake/Asleep labels and brand aria-labels. These keep their EN value.
- **needs-approved-copy (2):** homepage FAQ rows 2 and 3 (`[NEEDS APPROVED COPY]` in EN).
- **unsupported-claim (117):**
  - four from B1a: homepage benefit card 06 (heading and text) and Sietske Hamelink's quote on both templates;
  - 107 article blocks;
  - 4 product-page blocks;
  - 2 content-page blocks.
- **held-legacy (350):** the three pre-2.0 legal pages (coordinator, 19 Oct). Each is replaced by a page that is translated:

| Legacy page (held) | Replaced by (translated, legal-review) |
|---|---|
| `/pages/consumer-rights` | `/pages/new-consumer-rights` |
| `/pages/privacy` | `/pages/privacy-policy` |
| `/pages/terms-and-conditions` | `/pages/terms-and-conditions-1` |

A 301 redirect from each old handle to its replacement is the one-line decision that makes the held set unnecessary.

- **empty EN (9):** article summaries that contain only an image.

## Counts per batch and status

| Batch | Source entries | Source digest | translated | admin | theme-key | legal-review | pending-claim-review | dawn-nl | held | fit-risk |
|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `batch-02-pdp` | 477 | `03dd18b9d41a` | 122 | 234 | 36 | 0 | 37 | 15 | 33 | 22 |
| `batch-01-homepage` | 225 | `a09219ae1af8` | 140 | 2 | 30 | 0 | 30 | 2 | 21 | 18 |
| `batch-03-header-footer` | 41 | `e17cadb5e223` | 5 | 11 | 10 | 0 | 1 | 11 | 3 | 4 |
| `batch-04-legal` | 974 | `83fed281915f` | 0 | 3 | 0 | 621 | 0 | 0 | 350 | 12 |
| `batch-05-products` | 77 | `5ab678a91ffc` | 15 | 44 | 0 | 0 | 14 | 0 | 4 | 0 |
| `batch-06-content-pages` | 21 | `f78c391aa267` | 0 | 15 | 0 | 0 | 4 | 0 | 2 | 1 |
| `batch-07-collections-blog` | 709 | `9597904c4ef8` | 1 | 349 | 0 | 0 | 243 | 0 | 116 | 0 |
| `batch-08-system` | 46 | `306f141fadf2` | 3 | 7 | 0 | 0 | 0 | 36 | 0 | 0 |
| **All** | **2570** | | **286** | **665** | **76** | **621** | **329** | **64** | **529** | **57** |

A status names the strongest flag; `flags` in each entry lists all of them (an `admin` entry can also be `pending-claim-review` and `fit-risk`).

## Held entries by batch

| Batch | Reason | Entries |
|---|---|---:|
| `batch-01-homepage` | needs-approved-copy | 2 |
| `batch-01-homepage` | never-translate | 16 |
| `batch-01-homepage` | unsupported-claim | 3 |
| `batch-02-pdp` | never-translate | 32 |
| `batch-02-pdp` | unsupported-claim | 1 |
| `batch-03-header-footer` | never-translate | 3 |
| `batch-04-legal` | held-legacy | 350 |
| `batch-05-products` | unsupported-claim | 4 |
| `batch-06-content-pages` | unsupported-claim | 2 |
| `batch-07-collections-blog` | empty EN | 9 |
| `batch-07-collections-blog` | unsupported-claim | 107 |

## Fit risks

| Entry | EN | NL | Why |
|---|---|---|---|
| `product.subscription-item:main/loop_subscriptions_WEk4XJ/welcome_kit_title` | Welcome Kit · with first order | Welkomstpakket · bij je eerste bestelling | Glossary NL (binding), 30 → 41 chars. Short fallback if it wraps: 'Welkomstpakket · bij 1e bestelling'. |
| `product.subscription-item:main/loop_subscriptions_WEk4XJ/try_once_text` | Try once | Eenmalig proberen | Approved plan name (Figma NL), 8 → 17 chars; check the buy-box link. |
| `product.subscription-item:main/loop_subscriptions_WEk4XJ/pricing_summary_welcome_kit_title` | Welcome Kit on first order (value [value]) | Welkomstpakket bij eerste bestelling (waarde [value]) | 42 → 53 chars; 'Welkomstpakket' is 3 chars longer than 'Welcome Kit' and cannot shrink. |
| `product.subscription-item:featured_product_Eb93Xa/loop_subscriptions_gPKypi/care_credit_text_1` | 10% / order | 10% / bestelling | 11 → 16 chars; no shorter Dutch word for 'order' that reads well in Flanders. |
| `product.subscription-item:care_comes_back/step_next_order/title` | Your next order | Je volgende bestelling | 15 → 22 chars; 'order' is not neutral Dutch. |
| `liquid:sections/main-product.liquid:943` | Try Once · 1 Duo | Eenmalig proberen · 1 duo | Approved plan name (Figma NL), 16 → 25 chars in the sticky bar. |
| `liquid:sections/main-product.liquid:1030` | Try once | Eenmalig proberen | Approved plan name (Figma NL), 8 → 17 chars on the sticky-bar button. |
| `admin:morning-toothbrush-2-0:title` | Morning Toothbrush 2.0 | Ochtendtandenborstel 2.0 | revised in assembly: same Shopify product title inventoried twice; faithful title (the Figma 'Ultrazachte ochtendborste… |
| `admin:evening-toothbrush-2-0:title` | Evening Toothbrush 2.0 | Avondtandenborstel 2.0 | revised in assembly: same Shopify product title inventoried twice; faithful title |
| `admin:whitening-charcoal-dental-floss:title` | Whitening Charcoal Floss | Whitening floss met houtskool | revised in assembly: same Shopify product title inventoried twice (B1a kit item, B2 product page); Figma NL wording |
| `admin:karmicare-biorhythmic-oral-care-system:custom.treatment_journey_*#04` | First brush | Eerste poetsbeurt | 11 → 17 chars; Dutch has no shorter noun for 'brush' as an event. |
| `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#32` | No artificial colours | Geen kunstmatige kleurstoffen | 21 → 29 chars; 'kleurstoffen' cannot be shortened without changing the meaning. |
| `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#55` | Quality & safety | Kwaliteit & veiligheid | 16 → 22 chars; no shorter Dutch pair. Accordion title, probably full width. |
| `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#96` | Safe to swallow | Veilig bij inslikken | 15 → 20 chars; same wording as 'Veilig bij inslikken' in the leave-on text. |
| `admin:karmicare-biorhythmic-oral-care-system:custom.comparison_section#13` | One dose fits all | Eén dosis voor iedereen | 17 → 23 chars. |
| `admin:karmicare-biorhythmic-oral-care-system:custom.comparison_section#29` | Skin only | Alleen de huid | 9 → 14 chars; 'Alleen huid' (11) if the cell is tight. |
| `admin:karmicare-biorhythmic-oral-care-system:custom.comparison_section#34` | Surface renewal only | Alleen oppervlaktevernieuwing | 20 → 29 chars; the Dutch compound has no shorter form. |
| `admin:karmicare-biorhythmic-oral-care-system:custom.compare_table_header_footer#03` | Three ways to begin. | Drie manieren om te beginnen. | 20 → 29 chars; heading line. |
| `admin:karmicare-biorhythmic-oral-care-system:custom.compare_table|shop.metaobjects.compare_value#11` | Skip, pause or cancel | Overslaan, pauzeren of opzeggen | 21 → 31 chars; the trust-row short form 'Pauzeren of opzeggen' would drop 'skip'. |
| `admin:karmicare-biorhythmic-oral-care-system:custom.compare_table|shop.metaobjects.compare_value#14` | Try Once | Eenmalig proberen | Approved plan name (Figma NL), 8 → 17 chars as a column header. |
| `admin:karmicare-biorhythmic-oral-care-system:custom.compare_table_header_footer#04` | Every subscription earns | Met elk lidmaatschap verdien je | TERM: subscription → lidmaatschap (offer wording). Fragments #04–#06 join: 'Met elk lidmaatschap verdien je Care Credit… |
| `admin:karmicare-biorhythmic-oral-care-system:custom.compare_table_header_footer#06` | a return on the care you keep. | een rendement op de zorg die je volhoudt. | 'return' → 'rendement' (echoes Return on Care); 30 → 41 chars. |
| `index:hero_karmicare_XKKLDK/buttons_DpYxth/button_label_2` | WHY TWO FORMULAS? | WAAROM TWEE FORMULES? | 21 vs 17 chars; no shorter natural Dutch for 'why two formulas' |
| `index:stat_strip_karmicare/stat_5/heading` | No rinse | Niet spoelen | 12 vs 8 chars; shortest natural form, matches the approved 'Spugen, niet spoelen' |
| `index:product_benefits_karmicare_bcQ6tp/card_aXhzDi/heading` | Naturally brighter | Natuurlijk stralender | 21 vs 18 chars; 'stralender' is the idiom for teeth; shorter 'Natuurlijk witter' would turn 'brighter' into 'whiter' |
| `index:product_benefits_karmicare_bcQ6tp/card_jN7XcL/heading` | One pump, one dose | Eén pompje, één dosis | 21 vs 18 chars; 'Eén pomp, één dosis' (19) fits if 'pompje' may go |
| `index:trusted_professionals_HAqYth/card_HFdkaD/text` | Holistic Dentist | Holistisch tandarts | 19 vs 16 chars; no shorter Dutch title |
| `index:research_behind_system_EkjATL/card_bDxUVT/result_label` | RESULT | RESULTAAT | 9 vs 6 chars; standard term, no shorter Dutch label |
| `index:research_behind_system_EkjATL/card_yMiD9D/result_label` | RESULT | RESULTAAT | 9 vs 6 chars; standard term |
| `index:research_behind_system_EkjATL/card_fmFMFd/result_label` | Result | Resultaat | 9 vs 6 chars; standard term |
| `index:research_behind_system_EkjATL/card_Hi7YUD/result_label` | RESULT | RESULTAAT | 9 vs 6 chars; standard term |
| `index:research_behind_system_EkjATL/card_JeERX6/result_label` | RESULT | RESULTAAT | 9 vs 6 chars; standard term |
| `index:km_faq_accordion_FYcArV/faq_item_kLMHax/category` | Ingredients & safety | Ingrediënten & veiligheid | 25 vs 20 chars (filter tab); 'Ingrediënten' alone would drop 'safety' |
| `index:km_faq_accordion_FYcArV/faq_item_AL3DKF/category` | Results | Resultaten | 10 vs 7 chars (filter tab); no shorter equivalent |
| `index:featured_product_3XpDKw/loop_subscriptions_7dde8c/shipping_value_html` | Varies Free | Variabel Gratis | 15 vs 11 chars; 'Wisselt' (7) is shorter but reads less clearly |
| `index:featured_product_3XpDKw/loop_subscriptions_7dde8c/care_credit_text_1` | 10% / order | 10% / bestelling | 16 vs 11 chars; '10% / order' fits exactly (Dutch 'order' is correct but less consumer-friendly) |
| `index:care_comes_back/step_next_order/title` | Your next order | Je volgende bestelling | 22 vs 15 chars; 'Je volgende order' (17) fits if space is tight |
| `liquid:snippets/loop-widget-standard.liquid:123` | One time Purchase | Eenmalige bestelling | 20 vs 17 chars; 'one-time order' per the glossary. If this label shows the Try Once plan, use the approved 'Eenmalig pr… |
| `liquid:snippets/loop-widget-standard.liquid:140` | each | per stuk | 8 vs 4 chars; Dawn's NL locale uses '/st' if space is tight |
| `liquid:assets/loop-widget.js:2463` | Renews | Verlengd | The word that replaces 'ships' in the plan's option text. Dutch puts it at the end of the line, so the Loop owner shoul… |
| `liquid:sections/footer.liquid:679` | Join | Doe mee | 7 vs 4 chars; no four-letter Dutch verb for 'Join' ('Aanmelden' 9) |
| `liquid:sections/footer.liquid:1058` | Consumer Rights | Consumentenrechten | 18 vs 15 chars; standard term |
| `admin:navigation:new-main-menu:links[2].title` | Science | Wetenschap | 10 vs 7 chars; no shorter Dutch word |
| `admin:navigation:company:links[3].title` | Why Karmicare | Waarom Karmicare | 16 vs 13 chars; no shorter form |
| `page.privacy-policy:policy_banner_Pgpxip/eyebrow` | LEGAL | JURIDISCH | Eyebrow: 9 vs 5 chars, no shorter Dutch word; it sits alone above the banner heading. |
| `page.privacy-policy:legal_toc_section_gYznx3/content_section_g6nYeY/title` | 2. Data controller | 2. Verwerkingsverantwoordelijke | TERM: data controller → verwerkingsverantwoordelijke (AVG term). 31 vs 18 chars; no shorter correct legal term, the hea… |
| `page.privacy-policy:legal_toc_section_gYznx3/content_section_EAKJLC/nav_label` | Retention | Bewaartermijn | 13 vs 9 chars; shorter 'Bewaring' is possible but less clear. |
| `page.privacy-policy:legal_toc_section_gYznx3/content_section_qyyKHX/nav_label` | Security | Beveiliging | 11 vs 8 chars; no shorter Dutch word. |
| `page.privacy-policy:legal_toc_section_gYznx3/content_section_qyyKHX/title` | 10. Data security | 10. Gegevensbeveiliging | 23 vs 17 chars; 'Beveiliging' alone would drop 'data'. The heading can wrap. |
| `page.privacy-policy:legal_toc_section_gYznx3/content_section_pjNTAq/nav_label` | Changes | Wijzigingen | 11 vs 7 chars; no shorter Dutch word. |
| `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_g6nYeY/nav_label` | Scope | Toepassing | fit-risk: "Scope" (5 chars) has no Dutch legal equivalent of that length; "Toepassing" (10) is the shortest clear form. |
| `admin:policy:privacy-policy:body#b011` | 2. Data controller | 2. Verwerkingsverantwoordelijke | 31 vs 18 chars; no shorter correct legal term, the heading may wrap. |
| `admin:policy:privacy-policy:body#b128` | 10. Data security | 10. Gegevensbeveiliging | 23 vs 17 chars; 'Beveiliging' alone would drop 'data'. The heading can wrap. |
| `admin:policy:refund-policy:title` | Refund policy | Terugbetalingsbeleid | Shopify policy title; 20 vs 13 chars. No shorter correct term: 'Retourbeleid' would mean return policy. Title links wra… |
| `admin:policy:legal-notice:title` | Legal notice | Wettelijke vermeldingen | TERM: Legal notice → Wettelijke vermeldingen (usual Belgian title). 23 vs 12 chars; shorter alternative 'Juridische inf… |
| `admin:policy:legal-notice:seo.title` | Legal notice – KARMICARE | Wettelijke vermeldingen – KARMICARE | 35 vs 24 chars (page title, not a UI slot); see legal-notice title. |
| `admin:page:why-karmicare:title` | Why Karmicare | Waarom Karmicare | 16 vs 13 chars; no shorter form |

## Terms decided during translation

| Term (EN → NL) | First used in |
|---|---|
| kPNI practitioners → kPNI-therapeuten (products.md) | `product.subscription-item:main/highlights_slider_9wAjAb/text_1` |
| (Dental) Check-up Reward → controlebeloning (glossary). | `product.subscription-item:main/loop_subscriptions_WEk4XJ/try_once_note` |
| member products → formules (en accessoires) voor leden, to avoid 'producten' (rule 26) | `product.subscription-item:main/loop_subscriptions_WEk4XJ/pricing_summary_care_credit_tooltip` |
| 'On the Year' → 'Met het Karmicare-jaar' (bare 'het jaar' reads as 'the year'). Offer conflict 'confirmed by your dentist' kept as written. | `product.subscription-item:main/info_card_FnBcaN/body_text` |
| Karmicare credit → Karmicare-tegoed (never 'korting'). | `product.subscription-item:main/info_card_FnBcaN/footer_text` |
| (practitioner/professional) sample → proefpakket ('staal' is Flemish, 'monster' Dutch). | `product.subscription-item:trusted_professionals_HAqYth/button_label` |
| floss → tandzijde. 'toothbrushes' → 'borstels' to fit (as the Figma NL ochtend-/avondborstel). | `liquid:sections/main-product.liquid:1049` |
| Actives Awake/Asleep → Actief in Awake/Asleep (fits the label). | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#04` |
| oral–gut–brain axis → mond-darm-hersenas. | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#100` |
| subscription → lidmaatschap (offer wording). Fragments #04–#06 join: 'Met elk lidmaatschap verdien je Care Credit: een rendement op de zorg die je volhoudt.' Word order needed the subject change | `admin:karmicare-biorhythmic-oral-care-system:custom.compare_table_header_footer#04` |
| 60-day ritual → 60-dagenritueel (built like the glossary's 60-dagenritme) | `index:hero_karmicare_XKKLDK/buttons_DpYxth/button_label_1` |
| brushing ritual → poetsritueel | `index:two_formulas_karmicare/button_subtext` |
| practitioner → zorgverlener | `index:trusted_professionals_HAqYth/bottom_text` |
| trials → trials (klinische trials), kept apart from 'studies' as in the EN | `index:research_behind_system_EkjATL/card_fmFMFd/subtext` |
| Cancel anytime → Altijd opzegbaar | `index:featured_product_3XpDKw/icon_with_text_wUdX3G/heading_2` |
| credit (store credit) → tegoed | `index:care_comes_back/fine_print` |
| Selling Plans (fieldset legend) → Plannen | `liquid:snippets/loop-widget-standard.liquid:109` |
| nootropics → noötropica (as in products.md NL). 'tandpasta' twice as in the EN (SEO) | `admin:shop:online_store.preferences.homepage_meta_description` |
| Terms of Use → Gebruiksvoorwaarden | `liquid:sections/footer.liquid:694` |
| Terms and Conditions → Algemene voorwaarden | `liquid:sections/footer.liquid:1034` |
| charter → handvest. | `page.consumer-rights:policy_banner_Pgpxip/heading` |
| Bruges / Brussels / Belgium → Brugge / Brussel / België (official Dutch place names | `page.consumer-rights:policy_banner_Pgpxip/company_info` |
| money-back guarantee → geld-terug-garantie (glossary). | `page.consumer-rights:policy_banner_Pgpxip/benefit_card_hiciT4/card_description` |
| refund → terugbetaling / terugbetalen. | `page.consumer-rights:policy_banner_Pgpxip/benefit_card_3DXGyT/card_description` |
| legal guarantee (of conformity) → wettelijke garantie / wettelijke conformiteitsgarantie. | `page.consumer-rights:policy_banner_Pgpxip/benefit_card_Q4tabr/card_description` |
| commitment → engagement. | `page.consumer-rights:legal_toc_section_gYznx3/content_section_GLa7AN/nav_label` |
| Belgian Code of Economic Law → (Belgische) Wetboek van economisch recht (WER) | `page.consumer-rights:legal_toc_section_gYznx3/content_section_GLa7AN/content` |
| member → lid | `page.consumer-rights:legal_toc_section_gYznx3/content_section_GLa7AN/content` |
| one-time order → eenmalige bestelling. EN 'an eligible, unopened contract' is ambiguous (a contract cannot be unopened) | `page.consumer-rights:legal_toc_section_gYznx3/content_section_at3pLy/content` |
| Privacy Policy / this policy → Privacybeleid / dit beleid | `page.privacy-policy:policy_banner_Pgpxip/heading` |
| personal data → persoonsgegevens | `page.privacy-policy:policy_banner_Pgpxip/description` |
| trading as → handelend onder de naam. Place names in their official Dutch form (Brugge, Gent, Brussel, België) | `page.privacy-policy:policy_banner_Pgpxip/company_info` |
| GDPR → AVG | `page.privacy-policy:legal_toc_section_gYznx3/content_section_GLa7AN/content` |
| “we”, “us”, “our” → “we”, “ons”, “onze” | `page.privacy-policy:legal_toc_section_gYznx3/content_section_GLa7AN/content` |
| ePrivacy Directive → e-privacyrichtlijn (EC → EG) | `page.privacy-policy:legal_toc_section_gYznx3/content_section_GLa7AN/content` |
| customer care → klantenservice. Both Belgian acts under their official Dutch titles. 'as amended' left as ambiguous as the EN (Directive or Act). | `page.privacy-policy:legal_toc_section_gYznx3/content_section_GLa7AN/content` |
| data controller → verwerkingsverantwoordelijke (AVG term). 31 vs 18 chars | `page.privacy-policy:legal_toc_section_gYznx3/content_section_g6nYeY/title` |
| Dental Check-up Reward → controlebeloning (glossary) | `page.privacy-policy:legal_toc_section_gYznx3/content_section_iDEfUH/content` |
| Year members → leden van het Karmicare-jaar | `page.privacy-policy:legal_toc_section_gYznx3/content_section_iDEfUH/content` |
| explicit consent → uitdrukkelijke toestemming | `page.privacy-policy:legal_toc_section_gYznx3/content_section_iDEfUH/content` |
| health data / special category → gezondheidsgegevens / bijzondere categorie van persoonsgegevens (art. 9 AVG wording) | `page.privacy-policy:legal_toc_section_gYznx3/content_section_iDEfUH/content` |
| follow-up of your oral health → het volgen van je mondgezondheid | `page.privacy-policy:legal_toc_section_gYznx3/content_section_iDEfUH/content` |
| Day/Night preference → dag/nacht-voorkeur | `page.privacy-policy:legal_toc_section_gYznx3/content_section_iDEfUH/content` |
| cart → winkelwagen | `page.privacy-policy:legal_toc_section_gYznx3/content_section_iDEfUH/content` |
| at any time → op elk moment. | `page.privacy-policy:legal_toc_section_gYznx3/content_section_iDEfUH/content` |
| purposes → doeleinden | `page.privacy-policy:legal_toc_section_gYznx3/content_section_FcEDdA/title` |
| legal basis → rechtsgrond | `page.privacy-policy:legal_toc_section_gYznx3/content_section_FcEDdA/title` |
| legitimate interest → gerechtvaardigd belang | `page.privacy-policy:legal_toc_section_gYznx3/content_section_FcEDdA/content` |
| consent → toestemming | `page.privacy-policy:legal_toc_section_gYznx3/content_section_FcEDdA/content` |
| legal obligation/duty → wettelijke verplichting | `page.privacy-policy:legal_toc_section_gYznx3/content_section_FcEDdA/content` |
| performance of a contract → uitvoering van een overeenkomst | `page.privacy-policy:legal_toc_section_gYznx3/content_section_FcEDdA/block_content` |
| explicit prior consent → uitdrukkelijke voorafgaande toestemming | `page.privacy-policy:legal_toc_section_gYznx3/content_section_FcEDdA/block_content` |
| legal guarantee → wettelijke garantie. Article references kept in the EN notation art. 6(1)(b) | `page.privacy-policy:legal_toc_section_gYznx3/content_section_FcEDdA/block_content` |
| service provider → dienstverlener | `page.privacy-policy:legal_toc_section_gYznx3/content_section_xKcNPj/content` |
| processor / sub-processor → verwerker / subverwerker | `page.privacy-policy:legal_toc_section_gYznx3/content_section_xKcNPj/content` |
| data processing agreement (DPA) → verwerkersovereenkomst (DPA's) | `page.privacy-policy:legal_toc_section_gYznx3/content_section_xKcNPj/content` |
| opt in → instemmen. FPS Finance → FOD Financiën (official Dutch name) | `page.privacy-policy:legal_toc_section_gYznx3/content_section_xKcNPj/content` |
| (data) transfer → doorgifte (AVG chapter V term) | `page.privacy-policy:legal_toc_section_gYznx3/content_section_rnPj6g/title` |
| adequate level of protection → passend beschermingsniveau | `page.privacy-policy:legal_toc_section_gYznx3/content_section_rnPj6g/content` |
| adequacy decision → adequaatheidsbesluit | `page.privacy-policy:legal_toc_section_gYznx3/content_section_rnPj6g/content` |
| EU-U.S. Data Privacy Framework → EU-VS-gegevensprivacykader (wording of the Dutch Implementing Decision | `page.privacy-policy:legal_toc_section_gYznx3/content_section_rnPj6g/content` |
| Standard Contractual Clauses → modelcontractbepalingen (Dutch title of Decision 2021/914) | `page.privacy-policy:legal_toc_section_gYznx3/content_section_rnPj6g/content` |
| safeguard → waarborg. | `page.privacy-policy:legal_toc_section_gYznx3/content_section_rnPj6g/content` |
| retention duties → wettelijke bewaarplichten. CIR92 (French abbreviation) given as WIB 92, the Dutch abbreviation of the same code. Lawyer: check 'art. III.86 WER' | `page.privacy-policy:legal_toc_section_gYznx3/content_section_EAKJLC/content` |
| data subject → betrokkene | `page.privacy-policy:legal_toc_section_gYznx3/content_section_dGmgBJ/content` |
| Belgian Data Protection Authority → Belgische Gegevensbeschermingsautoriteit (the bilingual official name in brackets kept as in the EN) | `page.privacy-policy:legal_toc_section_gYznx3/content_section_dGmgBJ/content` |
| supervisory authority → toezichthoudende autoriteit | `page.privacy-policy:legal_toc_section_gYznx3/content_section_dGmgBJ/content` |
| check-up questionnaires → controlevragenlijsten. Right names follow the Dutch AVG (inzage, rectificatie, wissing, beperking, overdraagbaarheid, bezwaar). 'KARMICA BV — Privacy Operations' kept as a postal department name. | `page.privacy-policy:legal_toc_section_gYznx3/content_section_dGmgBJ/content` |
| the shop → de webshop | `page.privacy-policy:legal_toc_section_gYznx3/content_section_CDtWCV/content` |
| consent banner → toestemmingsbanner | `page.privacy-policy:legal_toc_section_gYznx3/content_section_CDtWCV/content` |
| checkout → afrekenen. “Cookie-instellingen” must match the NL label of the footer link. | `page.privacy-policy:legal_toc_section_gYznx3/content_section_CDtWCV/content` |
| plan → plan | `page.terms-and-conditions:policy_banner_Pgpxip/description` |
| trading as → handelend onder de naam | `page.terms-and-conditions:policy_banner_Pgpxip/company_info` |
| Clause → Artikel (also in cross-references: "clause 4.4" → "artikel 4.4" | `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_GLa7AN/title` |
| Enterprise number → Ondernemingsnummer | `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_GLa7AN/content` |
| General Terms and Conditions (“Terms”) → Algemene Voorwaarden (“Voorwaarden”), capitalised wherever the EN capitalises Terms | `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_g6nYeY/content` |
| Consumer → Consument (wording of art. I.1, 2° WER) | `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_g6nYeY/content` |
| cosmetics → cosmetische producten (term of Verordening (EG) nr. 1223/2009) | `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_iDEfUH/content` |
| formula → formule | `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_iDEfUH/content` |
| money-back guarantee → geld-terug-garantie (glossary) | `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_FcEDdA/content` |
| (statutory) right of withdrawal → (wettelijk) herroepingsrecht | `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_FcEDdA/content` |
| refund / reimbursement → terugbetaling | `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_FcEDdA/content` |
| renewal → verlenging (renews → wordt verlengd) | `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_FcEDdA/content` |
| prime / priming (a pump) → activeren / activering | `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_FcEDdA/content` |
| legal guarantee of conformity → wettelijke conformiteitsgarantie | `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_FcEDdA/content` |
| member price → ledenprijs (glossary) | `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_xKcNPj/content` |
| defect → gebrek (manufacturing defect → fabricagefout) | `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_EAKJLC/content` |
| Period After Opening (PAO) → houdbaarheidsperiode na opening (PAO) | `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_EAKJLC/content` |
| remedy → oplossing | `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_EAKJLC/content` |
| cancel (a membership) → opzeggen | `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_CDtWCV/content` |
| Consumer Mediation Service → Consumentenombudsdienst | `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_m4qTXH/content` |
| Annex → Bijlage | `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_fz6KEQ/title` |
| Terms of service (Shopify policy title) → Servicevoorwaarden (Shopify's NL policy name) | `admin:policy:terms-of-service:title` |
| Contact information → Contactgegevens | `admin:policy:contact-information:title` |
| Terms and Conditions / the Terms → Algemene Voorwaarden / de Voorwaarden | `admin:policy:contact-information:body#b001` |
| clause → artikel. Must match the legal-terms chunk word for word (clause 1 and 15.1 are quoted from it). href unchanged: it points to the EN terms page (/en/) | `admin:policy:contact-information:body#b001` |
| vendor → verkoper. Heading must match clause 1 in the legal-terms chunk. | `admin:policy:contact-information:body#b002` |
| Legal notice → Wettelijke vermeldingen (usual Belgian title). 23 vs 12 chars | `admin:policy:legal-notice:title` |
| Cancellation policy → Opzeggingsbeleid (a membership is "opgezegd", clause 9.6), not "Annuleringsbeleid". | `admin:policy:subscription-policy:title` |
| Kit → pakket (as welkomstpakket) | `admin:product:complete-hygiene-kit:title` |
| Morning Toothbrush (product title) → Ochtendtandenborstel | `admin:product:morning-toothbrush:title` |
| Evening Toothbrush (product title) → Avondtandenborstel | `admin:product:evening-toothbrush:title` |
| Asleep Evening Toothpaste → Asleep-avondtandpasta (brand + noun with a hyphen, as Het Karmicare-jaar) | `admin:product:asleep-evening-toothpaste-2-0:title` |
| Products (collection title) → Assortiment (avoids 'producten') | `admin:collection:all:seo.title` |

## URLs to check

Handles stay English (Victor has not decided to translate them), so each page lives at the same path behind the language prefix. NL and FR sitemaps exist (`/nl/sitemap.xml`, `/fr/sitemap.xml`).

| Page | EN | NL | FR | Batch | NL state |
|---|---|---|---|---|---|
| Homepage | `/` | `/nl` | `/fr` | 01 | translated; 3 blocks held (unsupported claims); 30 pending-claim-review |
| Duo PDP | `/products/karmicare-biorhythmic-oral-care-system` | `/nl/products/karmicare-biorhythmic-oral-care-system` | `/fr/products/karmicare-biorhythmic-oral-care-system` | 02 | translated; 1 block held (unsupported claims); 37 pending-claim-review |
| contact | `/pages/contact` | `/nl/pages/contact` | `/fr/pages/contact` | 04 | translated |
| new-consumer-rights | `/pages/new-consumer-rights` | `/nl/pages/new-consumer-rights` | `/fr/pages/new-consumer-rights` | 04 | legal-review |
| privacy-policy | `/pages/privacy-policy` | `/nl/pages/privacy-policy` | `/fr/pages/privacy-policy` | 04 | legal-review |
| terms-and-conditions-1 | `/pages/terms-and-conditions-1` | `/nl/pages/terms-and-conditions-1` | `/fr/pages/terms-and-conditions-1` | 04 | legal-review |
| consumer-rights | `/pages/consumer-rights` | `/nl/pages/consumer-rights` | `/fr/pages/consumer-rights` | 04 | held-legacy |
| privacy | `/pages/privacy` | `/nl/pages/privacy` | `/fr/pages/privacy` | 04 | held-legacy |
| terms-and-conditions | `/pages/terms-and-conditions` | `/nl/pages/terms-and-conditions` | `/fr/pages/terms-and-conditions` | 04 | held-legacy |
| policy-privacy-policy | `/policies/privacy-policy` | `/nl/policies/privacy-policy` | `/fr/policies/privacy-policy` | 04 | legal-review |
| policy-terms-of-service | `/policies/terms-of-service` | `/nl/policies/terms-of-service` | `/fr/policies/terms-of-service` | 04 | legal-review |
| policy-refund-policy | `/policies/refund-policy` | `/nl/policies/refund-policy` | `/fr/policies/refund-policy` | 04 | legal-review |
| policy-shipping-policy | `/policies/shipping-policy` | `/nl/policies/shipping-policy` | `/fr/policies/shipping-policy` | 04 | legal-review |
| policy-contact-information | `/policies/contact-information` | `/nl/policies/contact-information` | `/fr/policies/contact-information` | 04 | legal-review |
| policy-legal-notice | `/policies/legal-notice` | `/nl/policies/legal-notice` | `/fr/policies/legal-notice` | 04 | legal-review |
| policy-subscription-policy | `/policies/subscription-policy` | `/nl/policies/subscription-policy` | `/fr/policies/subscription-policy` | 04 | legal-review |
| complete-hygiene-kit | `/products/complete-hygiene-kit` | `/nl/products/complete-hygiene-kit` | `/fr/products/complete-hygiene-kit` | 05 | translated |
| morning-toothbrush | `/products/morning-toothbrush` | `/nl/products/morning-toothbrush` | `/fr/products/morning-toothbrush` | 05 | translated |
| evening-toothbrush | `/products/evening-toothbrush` | `/nl/products/evening-toothbrush` | `/fr/products/evening-toothbrush` | 05 | translated; 3 pending-claim-review |
| whitening-charcoal-dental-floss | `/products/whitening-charcoal-dental-floss` | `/nl/products/whitening-charcoal-dental-floss` | `/fr/products/whitening-charcoal-dental-floss` | 05 | translated; 5 pending-claim-review |
| evening-toothbrush-2-0 | `/products/evening-toothbrush-2-0` | `/nl/products/evening-toothbrush-2-0` | `/fr/products/evening-toothbrush-2-0` | 05 | translated; 3 pending-claim-review |
| morning-toothbrush-2-0 | `/products/morning-toothbrush-2-0` | `/nl/products/morning-toothbrush-2-0` | `/fr/products/morning-toothbrush-2-0` | 05 | translated |
| asleep-evening-toothpaste-2-0 | `/products/asleep-evening-toothpaste-2-0` | `/nl/products/asleep-evening-toothpaste-2-0` | `/fr/products/asleep-evening-toothpaste-2-0` | 05 | translated; 2 blocks held (unsupported claims); 1 pending-claim-review |
| awake-morning-toothpaste-2-0 | `/products/awake-morning-toothpaste-2-0` | `/nl/products/awake-morning-toothpaste-2-0` | `/fr/products/awake-morning-toothpaste-2-0` | 05 | translated; 2 blocks held (unsupported claims); 1 pending-claim-review |
| why-karmicare | `/pages/why-karmicare` | `/nl/pages/why-karmicare` | `/fr/pages/why-karmicare` | 06 | translated |
| why-use-hydroxyapatite-toothpaste | `/pages/why-use-hydroxyapatite-toothpaste` | `/nl/pages/why-use-hydroxyapatite-toothpaste` | `/fr/pages/why-use-hydroxyapatite-toothpaste` | 06 | translated |
| why-stop-using-fluoride-toothpaste | `/pages/why-stop-using-fluoride-toothpaste` | `/nl/pages/why-stop-using-fluoride-toothpaste` | `/fr/pages/why-stop-using-fluoride-toothpaste` | 06 | translated; 4 pending-claim-review |
| nhap-technology | `/pages/nhap-technology` | `/nl/pages/nhap-technology` | `/fr/pages/nhap-technology` | 06 | translated; 2 blocks held (unsupported claims) |
| articles | `/pages/articles` | `/nl/pages/articles` | `/fr/pages/articles` | 06 | translated |
| collections-biorhythmic-oral-hygiene-kit | `/collections/biorhythmic-oral-hygiene-kit` | `/nl/collections/biorhythmic-oral-hygiene-kit` | `/fr/collections/biorhythmic-oral-hygiene-kit` | 07 | translated |
| collections-vgbc2025 | `/collections/vgbc2025` | `/nl/collections/vgbc2025` | `/fr/collections/vgbc2025` | 07 | translated |
| collections-karmicare-collection | `/collections/karmicare-collection` | `/nl/collections/karmicare-collection` | `/fr/collections/karmicare-collection` | 07 | translated |
| blogs-news | `/blogs/news` | `/nl/blogs/news` | `/fr/blogs/news` | 07 | translated |
| nano-hydroxyapatite | `/blogs/news/nano-hydroxyapatite` | `/nl/blogs/news/nano-hydroxyapatite` | `/fr/blogs/news/nano-hydroxyapatite` | 07 | translated; 21 blocks held (unsupported claims); 37 pending-claim-review |
| morning-and-night-time-brushing-why-timing-matters | `/blogs/news/morning-and-night-time-brushing-why-timing-matters` | `/nl/blogs/news/morning-and-night-time-brushing-why-timing-matters` | `/fr/blogs/news/morning-and-night-time-brushing-why-timing-matters` | 07 | translated; 3 blocks held (unsupported claims); 10 pending-claim-review |
| benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood | `/blogs/news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood` | `/nl/blogs/news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood` | `/fr/blogs/news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood` | 07 | translated; 28 blocks held (unsupported claims); 32 pending-claim-review |
| nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste | `/blogs/news/nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste` | `/nl/blogs/news/nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste` | `/fr/blogs/news/nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste` | 07 | translated; 13 blocks held (unsupported claims); 26 pending-claim-review |
| how-oral-health-impacts-your-overall-wellness | `/blogs/news/how-oral-health-impacts-your-overall-wellness` | `/nl/blogs/news/how-oral-health-impacts-your-overall-wellness` | `/fr/blogs/news/how-oral-health-impacts-your-overall-wellness` | 07 | translated; 8 blocks held (unsupported claims); 28 pending-claim-review |
| top-natural-whitening-toothpaste-for-a-brighter-smile | `/blogs/news/top-natural-whitening-toothpaste-for-a-brighter-smile` | `/nl/blogs/news/top-natural-whitening-toothpaste-for-a-brighter-smile` | `/fr/blogs/news/top-natural-whitening-toothpaste-for-a-brighter-smile` | 07 | translated; 8 blocks held (unsupported claims); 30 pending-claim-review |
| 5-reasons-you-should-avoid-fluoride-in-toothpaste | `/blogs/news/5-reasons-you-should-avoid-fluoride-in-toothpaste` | `/nl/blogs/news/5-reasons-you-should-avoid-fluoride-in-toothpaste` | `/fr/blogs/news/5-reasons-you-should-avoid-fluoride-in-toothpaste` | 07 | translated; 15 blocks held (unsupported claims); 31 pending-claim-review |
| headaches-and-tooth-pain-understanding-the-connection | `/blogs/news/headaches-and-tooth-pain-understanding-the-connection` | `/nl/blogs/news/headaches-and-tooth-pain-understanding-the-connection` | `/fr/blogs/news/headaches-and-tooth-pain-understanding-the-connection` | 07 | translated; 7 blocks held (unsupported claims); 23 pending-claim-review |
| 3-reasons-why-you-should-look-for-an-sls-free-toothpaste | `/blogs/news/3-reasons-why-you-should-look-for-an-sls-free-toothpaste` | `/nl/blogs/news/3-reasons-why-you-should-look-for-an-sls-free-toothpaste` | `/fr/blogs/news/3-reasons-why-you-should-look-for-an-sls-free-toothpaste` | 07 | translated; 4 blocks held (unsupported claims); 26 pending-claim-review |
| search | `/search` | `/nl/search` | `/fr/search` | 08 | translated |
| 404 | `/pages/any-missing-page` | `/nl/pages/any-missing-page` | `/fr/pages/any-missing-page` | 08 | translated |
| collections-list | `/collections` | `/nl/collections` | `/fr/collections` | 08 | translated |
| collections-all | `/collections/all` | `/nl/collections/all` | `/fr/collections/all` | 08 | translated |
| cart | `/cart` | `/nl/cart` | `/fr/cart` | 08 | translated |
| customers/*.json | `/account/login` | `/nl/account/login` | `/fr/account/login` | 08 | not theme-rendered: 302 to Shopify's hosted customer accounts: the theme templates do not render (new customer accounts) |
| password.json | `/password` | `/nl/password` | `/fr/password` | 08 | not theme-rendered: 302 to the homepage: the store is not password-protected; the template renders only when a password is set |
| gift_card.liquid | `/gift_cards/<token>` | `/nl/gift_cards/<token>` | `/fr/gift_cards/<token>` | 08 | not theme-rendered: reachable only with a gift-card link; Dawn locale keys (gift_cards.*) only |

## Open questions for Victor

1. **The nine legacy blog articles.**
   - They predate the 2026 claim rules: 107 of their blocks are unsupported (disease prevention, fluoride harm stated as fact, "NASA", "medical marvel", toddler safety, insomnia/ADHD/weight-loss claims for nootropics), so a Dutch article would have holes.
   - They also name competitors (Colgate, Biotene, Sensodyne Pronamel, Tom's of Maine) and prescription drugs (Adderall, modafinil). Their links point to the old Webflow paths (`karmicare.com/en/…`).
   - *Recommendation*: do not publish the NL (or FR) articles until the EN is rewritten or the articles are unpublished. The rest of the translation is in place and can be updated through the digests.
2. **products.md vs regulatory.md.** `products.md` allows "helps prevent" cavities and says xylitol "prevents cavities"; `regulatory.md` forbids prevention claims. The claims review followed `regulatory.md`. *Recommendation*: confirm `regulatory.md` wins and correct `products.md`.
3. **Brush and floss titles.** They are translated faithfully (*Ochtendtandenborstel 2.0*, *Avondtandenborstel 2.0*, *Whitening floss met houtskool*). The Figma buy-box labels *Ultrazachte ochtendborstel* / *Dieptereinigende avondborstel* belong to different EN ("Ultrasoft Morning Toothbrush") and stay labels. *Recommendation*: keep it this way.
4. **Check-up reward term.** *Controlebeloning* (glossary) is used everywhere; Figma's plan card once says *tandartscontrole-beloning*. *Recommendation*: keep *controlebeloning*.
5. **Copy that conflicts with the offer, translated as written and flagged:**
   - "verified/confirmed by your dentist" (no dentist involvement is needed);
   - the announcement bar's shipping and guarantee promise to everyone;
   - "Inflation-proof member price".

   The B1a open decisions still apply.
6. **Meta descriptions.** Several EN meta descriptions end mid-word: Shopify generated them from the body, because the SEO field is empty. Where that is the case, Shopify will generate the NL one from the translated body. *Recommendation*: the integrator registers `seo.description` only where the field really holds text.
7. **Store-level items outside the theme**, for the localization worker:
   - The checkout button name "Nu betalen" must match Shopify's NL checkout.
   - The footer's "Cookie preferences" link label comes from the consent app.
   - Shopify's own filter and sort labels and article dates are translated by Shopify.

## For the lawyer first (legal-review, from the legal translators)

- **Citations to check:**
  - "Art. VI.19/1 WER": the reference-price rule is VI.18.
  - "Art. III.86 WER" for 7-year retention: usually III.88.
  - Art. 1649quater §2/§4 (old Civil Code) next to art. 5.226 (new Civil Code).
  - Book VI WER does not transpose Directive 2019/771.
- **Content:**
  - Refund timing: 3.1 says 14 days from receiving the goods, 3.6 says 14 days from approval; art. VI.50 counts from the withdrawal notice.
  - Whether an unprimed pump counts as a hygiene seal under VI.53, 5°.
  - The model withdrawal form adds an "unopened" condition.
  - Replacement only, with no repair choice (clause on conformity).
  - "No lock-in" next to the prepaid Year.
  - The withdrawal steps cover one-time orders only.
  - "You receive €5" does not say it is Care Credit.
- **EN wording translated by intended meaning:** "presumption of conformity" (the law presumes *non*-conformity at delivery) and "an unopened contract".
- **Presentation:**
  - SEO titles still say "New Consumer Rights / New Privacy Policy / New Terms and Conditions".
  - Several policy links point to English `/en/` pages, and the PDF link is "#".
  - E-mail links also wrap the phone number.
  - "Data Privacy Lead" must not read as an appointed DPO.
- Clauses quoted in several documents (clause 1, 15.1 and the shipping clauses) are translated identically everywhere.

## Pending

| Item | Owner or gate |
|---|---|
| Legal review of 621 `legal-review` entries | Victor / lawyer |
| Claim sign-off of 329 `pending-claim-review` entries | Victor / Clinical Research |
| Register `admin` entries, add `theme-key` strings to `locales/nl.json`, store the sticky-bar and footer schema defaults | localization worker |
| Rendered check of every `/nl/` URL below | preview gate / localization check |
| FR worker merges this branch for batches 04–08 | FR worker |


## Translator notes for the reviewer

<details><summary>Every non-empty note on a translated entry</summary>

| Entry | Note |
|---|---|
| `product.subscription-item:main/highlights_slider_9wAjAb/text_3` | 'niet spoelen' as in the approved Figma NL 'Spugen, niet spoelen'. |
| `product.subscription-item:main/loop_subscriptions_WEk4XJ/welcome_kit_title` | Glossary NL (binding), 30 → 41 chars. Short fallback if it wraps: 'Welkomstpakket · bij 1e bestelling'. |
| `product.subscription-item:main/loop_subscriptions_WEk4XJ/try_once_text` | Approved plan name (Figma NL), 8 → 17 chars; check the buy-box link. |
| `product.subscription-item:main/loop_subscriptions_WEk4XJ/pricing_summary_checkup_tooltip` | Offer conflict carried over from the EN ('verified by your dentist'); translated as written. Same wording in every check-up tooltip. |
| `product.subscription-item:main/loop_subscriptions_WEk4XJ/testimonial_button_text` | Approved badge (Figma NL). |
| `product.subscription-item:main/loop_subscriptions_WEk4XJ/pricing_summary_welcome_kit_title` | 42 → 53 chars; 'Welkomstpakket' is 3 chars longer than 'Welcome Kit' and cannot shrink. |
| `product.subscription-item:main/buy_buttons/custom_button_text_by_plan` | Selling-plan IDs unchanged; first-person 'mijn' kept as in the EN. |
| `product.subscription-item:main/icon_with_text_xhaDGB/heading_1` | Approved trust-row short form (Figma NL). |
| `product.subscription-item:main/icon_with_text_xhaDGB/heading_2` | Approved trust-row short form (Figma NL); drops 'gift' to fit. |
| `product.subscription-item:main/icon_with_text_xhaDGB/heading_3` | Approved trust-row form (Figma NL), checked there for fit. |
| `product.subscription-item:main/treatment_journey_block/disclaimer_text` | revised in assembly: approved Figma NL (3738:27474); same on product.json and the Duo PDP |
| `product.subscription-item:chronobiology_clock_karmicare/title` | revised in assembly: approved NL from Figma 'Dutch offer 2.0 · NL' (3738:27474); translator had: Je mond draait op een 24-uursklok. |
| `product.subscription-item:chronobiology_clock_karmicare/description` | 'hij' = je mond (title above), as the EN 'it'. |
| `product.subscription-item:chronobiology_clock_karmicare/night_text` | revised in assembly: approved NL from Figma 'Dutch offer 2.0 · NL' (3738:27474); translator had: Melatonine stijgt en speeksel komt nog maar mondjesmaat. Wat om 22:00 op je glazuur zit, zit er om 07:00 nog. |
| `product.subscription-item:chronobiology_clock_karmicare/hint_label` | revised in assembly: approved NL from Figma 'Dutch offer 2.0 · NL' (3738:27474); translator had: SLEEP AAN DE RING · ONTDEK 24 UUR |
| `product.subscription-item:chronobiology_clock_karmicare/footer_link_text` | As the approved Figma NL link 'Lees het onderzoek'. |
| `product.subscription-item:trusted_professionals_HAqYth/bottom_text` | 'prevented' → 'voorkomt', literal as the rules require; the glossary notes the JEP/DETIC objection to 'voorkomt', so the claims reviewer must decide (it is said of an outcome, not of Karmicare). |
| `product.subscription-item:trusted_professionals_HAqYth/card_8dRing/hover_text` | Practitioner quote: if she gave it in Dutch, use her original words instead of this translation. |
| `product.subscription-item:how_it_works_steps_aAgVmF/bottom_text` | First sentence as in the NL usage text (products.md). |
| `product.subscription-item:how_it_works_steps_aAgVmF/step_EBicgt/title` | Approved how-to step 3 (Figma NL). Block disabled, not rendered. |
| `product.subscription-item:how_it_works_steps_aAgVmF/step_EBicgt/description` | revised in assembly: approved NL from Figma 'Dutch offer 2.0 · NL' (3738:27474); translator had: Spuug het overschot uit. Spoel daarna niet na. |
| `product.subscription-item:research_behind_system_EkjATL/button_label` | revised in assembly: approved NL from Figma 'Dutch offer 2.0 · NL' (3738:27474); translator had: Ontdek de volledige onderbouwing |
| `product.subscription-item:research_behind_system_EkjATL/card_bDxUVT/heading` | Approved research card 1 (Figma NL). |
| `product.subscription-item:research_behind_system_EkjATL/card_bDxUVT/result_text` | revised in assembly: approved NL from Figma 'Dutch offer 2.0 · NL' (3738:27474); translator had: 98% afsluiting tegenover 82% en 65% bij twee andere desensibiliserende technologieën |
| `product.subscription-item:research_behind_system_EkjATL/card_bDxUVT/method_text` | revised in assembly: approved NL from Figma 'Dutch offer 2.0 · NL' (3738:27474); translator had: In-vitrovergelijking met SEM van drie pasta's, ~1% nHAp. |
| `product.subscription-item:research_behind_system_EkjATL/card_yMiD9D/heading` | revised in assembly: approved NL from Figma 'Dutch offer 2.0 · NL' (3738:27474); translator had: Slechtere mondgezondheid hing samen met slechtere slaap. |
| `product.subscription-item:research_behind_system_EkjATL/card_yMiD9D/image_badge` | revised in assembly: approved NL from Figma 'Dutch offer 2.0 · NL' (3738:27474); translator had: SLAAP · LUCHTWEGEN EN MONDHOLTE |
| `product.subscription-item:research_behind_system_EkjATL/card_fmFMFd/heading` | revised in assembly: approved NL from Figma 'Dutch offer 2.0 · NL' (3738:27474); translator had: Xylitol verminderde tandbederf in vergelijking met controlegroepen. |
| `product.subscription-item:research_behind_system_EkjATL/card_fmFMFd/subtext` | revised in assembly: approved NL from Figma 'Dutch offer 2.0 · NL' (3738:27474); translator had: 1.478 mensen · 7 studies |
| `product.subscription-item:research_behind_system_EkjATL/card_fmFMFd/result_text` | revised in assembly: approved Figma NL (3738:27474) |
| `product.subscription-item:research_behind_system_EkjATL/card_fmFMFd/image_badge` | EN repeats the dentine badge on the xylitol card; check the image. |
| `product.subscription-item:research_behind_system_EkjATL/card_Hi7YUD/heading` | revised in assembly: approved NL from Figma 'Dutch offer 2.0 · NL' (3738:27474); translator had: Nano-HAp deed het beter dan fluoride bij tandgevoeligheid. |
| `product.subscription-item:research_behind_system_EkjATL/card_Hi7YUD/result_text` | revised in assembly: approved Figma NL (3738:27474), same on homepage and PDP |
| `product.subscription-item:research_behind_system_EkjATL/card_JeERX6/heading` | revised in assembly: approved NL from Figma 'Dutch offer 2.0 · NL' (3738:27474); translator had: Geen SLS betekende minder en kortere aften. |
| `product.subscription-item:research_behind_system_EkjATL/card_JeERX6/subtext` | revised in assembly: approved NL from Figma 'Dutch offer 2.0 · NL' (3738:27474); translator had: 124 mensen · 4 crossover-RCT's |
| `product.subscription-item:research_behind_system_EkjATL/card_JeERX6/method_text` | revised in assembly: approved NL from Figma 'Dutch offer 2.0 · NL' (3738:27474); translator had: Systematische review en meta-analyse van 4 crossover-RCT's. |
| `product.subscription-item:research_behind_system_EkjATL/card_JeERX6/image_badge` | EN has '-' here and '·' on the other cards; NL uses '·' throughout. Also the dentine badge on the SLS card; check the image. |
| `product.subscription-item:featured_product_Eb93Xa/loop_subscriptions_gPKypi/pricing_summary_care_credit_title` | EN plural 'Care Credits' corrected to the program name 'Care Credit'. |
| `product.subscription-item:featured_product_Eb93Xa/loop_subscriptions_gPKypi/subscription_title` | AM/PM kept: common in Dutch beauty copy ('AM/PM-routine'). |
| `product.subscription-item:featured_product_Eb93Xa/loop_subscriptions_gPKypi/care_credit_text_1` | 11 → 16 chars; no shorter Dutch word for 'order' that reads well in Flanders. |
| `product.subscription-item:featured_product_Eb93Xa/loop_subscriptions_gPKypi/care_credit_text_2` | 'purchase' → 'bestelling' (no 'aankoop/koop', rule 26). |
| `product.subscription-item:featured_product_Eb93Xa/icon_with_text_endcta/heading_1` | Approved trust-row short form (Figma NL). |
| `product.subscription-item:featured_product_Eb93Xa/icon_with_text_endcta/heading_2` | Approved trust-row form (Figma NL), checked there for fit. |
| `product.subscription-item:featured_product_Eb93Xa/icon_with_text_endcta/heading_3` | revised in assembly: approved NL from Figma 'Dutch offer 2.0 · NL' (3738:27474); translator had: Pauzeren of opzeggen |
| `product.subscription-item:care_comes_back/terms_link_label` | 'clauses' → 'art.' to fit; must match the article numbering of the NL Terms. |
| `product.subscription-item:care_comes_back/step_next_order/title` | 15 → 22 chars; 'order' is not neutral Dutch. |
| `product.subscription-item:care_comes_back/line_year/note` | 'the Year' → 'je jaar' to fit and avoid 'per year' reading. |
| `liquid:snippets/product-highlights.liquid:160` | aria-label; avoids 'product' (rule 26). |
| `liquid:sections/main-product.liquid:943` | Approved plan name (Figma NL), 16 → 25 chars in the sticky bar. |
| `liquid:sections/main-product.liquid:995` | Offer conflict carried over from the EN ('verified by your dentist'). |
| `liquid:sections/main-product.liquid:1030` | Approved plan name (Figma NL), 8 → 17 chars on the sticky-bar button. |
| `liquid:sections/main-product.liquid:1055` | revised in assembly: approved NL from Figma 'Dutch offer 2.0 · NL' (3738:27474); translator had: 60 dagen geld terug |
| `liquid:sections/main-product.liquid:1073` | 'stop anytime before renewal' → 'opzegbaar tot de verlenging' to fit. |
| `liquid:sections/main-product.liquid:1087` | 'Not ready for a membership?' → 'Nog geen lidmaatschap?' to fit the sticky bar. |
| `liquid:sections/product-compare-plans.liquid:39` | aria-label, not visible. |
| `admin:karmicare-biorhythmic-oral-care-system:selling_plan_group:Subscribe and Save` | revised in assembly: one form for every legacy 'Subscribe and Save' group |
| `admin:karmicare-biorhythmic-oral-care-system:selling_plan.712387363197.name` | Leading space and trailing '_' in the EN are source defects; left out. |
| `admin:karmicare-biorhythmic-oral-care-system:selling_plan.712192164221.name` | 'ships' → 'levering' to fit (glossary: every 60 days → om de 60 dagen). |
| `admin:karmicare-biorhythmic-oral-care-system:selling_plan.712106115453.name` | 'ships' → 'levering' to fit. |
| `admin:karmicare-biorhythmic-oral-care-system:selling_plan.712106115453.description` | revised in assembly: approved Figma NL wording 'Inflatievaste ledenprijs' (3738:27474) |
| `admin:karmicare-biorhythmic-oral-care-system:selling_plan.712155431293.description` | revised in assembly: approved Figma NL wording 'Inflatievaste ledenprijs' (3738:27474) |
| `admin:karmicare-biorhythmic-oral-care-system:selling_plan_group:Yearly Plan` | Legacy group; should stay hidden. |
| `admin:karmicare-biorhythmic-oral-care-system:body_html` | Stray meta/empty span tags kept as in the source. |
| `admin:karmicare-biorhythmic-oral-care-system:media.69840178020733.alt` | Reordered morning before evening (brand rule Awake before Asleep); the EN has evening first (handoff). |
| `admin:karmicare-biorhythmic-oral-care-system:media.69840177987965.alt` | 'How to use … use 1 pump' → 'Zo poets je … neem 1 pompje' (no 'gebruik', rule 26). |
| `admin:morning-toothbrush-2-0:title` | revised in assembly: same Shopify product title inventoried twice; faithful title (the Figma 'Ultrazachte ochtendborstel' is a buy-box label for a different EN) |
| `admin:evening-toothbrush-2-0:title` | revised in assembly: same Shopify product title inventoried twice; faithful title |
| `admin:whitening-charcoal-dental-floss:title` | revised in assembly: same Shopify product title inventoried twice (B1a kit item, B2 product page); Figma NL wording |
| `admin:karmicare-biorhythmic-oral-care-system:custom.treatment_journey_*#01` | Joins with #02: 'Wat je voelt (en je tandarts merkt het)'. |
| `admin:karmicare-biorhythmic-oral-care-system:custom.treatment_journey_*#03` | revised in assembly: approved NL from Figma 'Dutch offer 2.0 · NL' (3738:27474); translator had: Eerste 60 dagen |
| `admin:karmicare-biorhythmic-oral-care-system:custom.treatment_journey_*#04` | 11 → 17 chars; Dutch has no shorter noun for 'brush' as an event. |
| `admin:karmicare-biorhythmic-oral-care-system:custom.treatment_journey_*#05` | revised in assembly: approved NL from Figma 'Dutch offer 2.0 · NL' (3738:27474); translator had: — gladder gepoetst, een extra laagje dat je voelt |
| `admin:karmicare-biorhythmic-oral-care-system:custom.treatment_journey_*#07` | revised in assembly: approved NL from Figma 'Dutch offer 2.0 · NL' (3738:27474); translator had: — voel het herstel, het werkt door terwijl je slaapt |
| `admin:karmicare-biorhythmic-oral-care-system:custom.treatment_journey_*#09` | revised in assembly: approved NL from Figma 'Dutch offer 2.0 · NL' (3738:27474); translator had: — gevoeligheid begint af te nemen, de minerale laag groeit |
| `admin:karmicare-biorhythmic-oral-care-system:custom.treatment_journey_*#11` | revised in assembly: approved NL from Figma 'Dutch offer 2.0 · NL' (3738:27474); translator had: — rustiger tandvlees, frissere adem, ochtend en avond |
| `admin:karmicare-biorhythmic-oral-care-system:custom.treatment_journey_*#18` | Glossary (Figma NL). |
| `admin:karmicare-biorhythmic-oral-care-system:custom.treatment_journey_*#21` | revised in assembly: approved NL from Figma 'Dutch offer 2.0 · NL' (3738:27474); translator had: — je gaat beide nodig hebben |
| `admin:karmicare-biorhythmic-oral-care-system:custom.treatment_journey_*#22` | Glossary (Figma NL). |
| `admin:karmicare-biorhythmic-oral-care-system:custom.treatment_journey_*#23` | Approved Figma NL short form; drops 'arrive resilient' to fit. |
| `admin:karmicare-biorhythmic-oral-care-system:custom.treatment_journey_*#24` | Glossary (Figma NL). |
| `admin:karmicare-biorhythmic-oral-care-system:custom.treatment_journey_*#25` | Approved Figma NL line, already shortened after a visual check of this timeline (28 → 38 chars). |
| `admin:karmicare-biorhythmic-oral-care-system:custom.treatment_journey_*#29` | EN line is cut off ('…to the', handoff). Once the EN is complete, check 'de/het/je' against the missing word. |
| `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#02` | No final full stop, as in the EN. |
| `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#32` | 21 → 29 chars; 'kleurstoffen' cannot be shortened without changing the meaning. |
| `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#33` | 'How to use' → 'Zo poets je' (no 'gebruik', rule 26). |
| `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#34` | Glossary (products.md). |
| `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#37` | EN typo 'dosep' read as 'dose' (handoff). |
| `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#38` | Approved how-to step 3 (Figma NL), shortened there after a visual check. |
| `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#41` | Joins with #42: 'Glijd met je tong over je tanden: dat gladde randje, dát is schoon'. |
| `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#43` | 'dental clinics use in-office' → 'tandartsen in hun praktijk toepassen' (no 'gebruiken'). |
| `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#45` | Lead-in for #46, which starts in lower case as in the EN. |
| `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#46` | 'that's your before' (before/after) → 'je ‘vóór’'; accent marks the meaning. |
| `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#55` | 16 → 22 chars; no shorter Dutch pair. Accordion title, probably full width. |
| `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#56` | 'for leave-on use' → 'als leave-on' (no 'gebruik'). |
| `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#59` | 'assessment' dropped to fit; the CPSR line above names it. |
| `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#60` | 'producten' kept: it is the portal's official name (CPNP), not commodity copy. |
| `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#61` | 'verantwoordelijke persoon' is the term in the Dutch text of Reg. 1223/2009. |
| `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#67` | SCCS 'opinion' is 'advies' in Dutch EU texts. |
| `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#82` | AM/PM kept, as in 'AM/PM-mondzorgsysteem'. |
| `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#90` | Ph. Eur. monograph name kept in English. |
| `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#96` | 15 → 20 chars; same wording as 'Veilig bij inslikken' in the leave-on text. |
| `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#99` | revised in assembly: approved NL from Figma 'Dutch offer 2.0 · NL' (3738:27474); translator had: Voor kPNI- en orthomoleculaire therapeuten |
| `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#105` | Joins with #106, which starts with '. '. |
| `admin:karmicare-biorhythmic-oral-care-system:custom.comparison_section#01` | revised in assembly: approved NL from Figma 'Dutch offer 2.0 · NL' (3738:27474); translator had: ZORG DIE ZICH OPBOUWT |
| `admin:karmicare-biorhythmic-oral-care-system:custom.comparison_section#02` | maintains → houdt in stand (glossary claim verbs). |
| `admin:karmicare-biorhythmic-oral-care-system:custom.comparison_section#03` | 'This one' → 'Dit ritueel' (a bare 'Deze' has no clear antecedent in Dutch). Echoes 'Versterk je tanden. Versterk jezelf.' |
| `admin:karmicare-biorhythmic-oral-care-system:custom.comparison_section#04` | revised in assembly: approved NL from Figma 'Dutch offer 2.0 · NL' (3738:27474); translator had: Awake beschermt de dag. Asleep herstelt de nacht. Zorg afgestemd op je biologie — die nog lang doorwerkt nadat je de bor |
| `admin:karmicare-biorhythmic-oral-care-system:custom.comparison_section#08` | Approved table header (Figma NL). |
| `admin:karmicare-biorhythmic-oral-care-system:custom.comparison_section#09` | Approved table header (Figma NL). |
| `admin:karmicare-biorhythmic-oral-care-system:custom.comparison_section#12` | revised in assembly: approved NL from Figma 'Dutch offer 2.0 · NL' (3738:27474); translator had: Zelfde formule, elk uur |
| `admin:karmicare-biorhythmic-oral-care-system:custom.comparison_section#13` | 17 → 23 chars. |
| `admin:karmicare-biorhythmic-oral-care-system:custom.comparison_section#16` | revised in assembly: approved NL from Figma 'Dutch offer 2.0 · NL' (3738:27474); translator had: Guarana overdag, valeriaan 's nachts |
| `admin:karmicare-biorhythmic-oral-care-system:custom.comparison_section#18` | revised in assembly: approved NL from Figma 'Dutch offer 2.0 · NL' (3738:27474); translator had: Merkbaar na weken |
| `admin:karmicare-biorhythmic-oral-care-system:custom.comparison_section#21` | revised in assembly: approved NL from Figma 'Dutch offer 2.0 · NL' (3738:27474); translator had: Mond-darm-hersenen, dieper dan glazuur |
| `admin:karmicare-biorhythmic-oral-care-system:custom.comparison_section#23` | revised in assembly: approved NL from Figma 'Dutch offer 2.0 · NL' (3738:27474); translator had: Systemisch, niet oraal |
| `admin:karmicare-biorhythmic-oral-care-system:custom.comparison_section#25` | revised in assembly: approved NL from Figma 'Dutch offer 2.0 · NL' (3738:27474); translator had: Het werkt door als jij stopt |
| `admin:karmicare-biorhythmic-oral-care-system:custom.comparison_section#29` | 9 → 14 chars; 'Alleen huid' (11) if the cell is tight. |
| `admin:karmicare-biorhythmic-oral-care-system:custom.comparison_section#30` | revised in assembly: approved NL from Figma 'Dutch offer 2.0 · NL' (3738:27474); translator had: Het voedt én reinigt |
| `admin:karmicare-biorhythmic-oral-care-system:custom.comparison_section#33` | revised in assembly: approved NL from Figma 'Dutch offer 2.0 · NL' (3738:27474); translator had: Niets bereikt het glazuur |
| `admin:karmicare-biorhythmic-oral-care-system:custom.comparison_section#34` | 20 → 29 chars; the Dutch compound has no shorter form. |
| `admin:karmicare-biorhythmic-oral-care-system:custom.comparison_section#35` | revised in assembly: approved NL from Figma 'Dutch offer 2.0 · NL' (3738:27474); translator had: Wie je erdoor wordt |
| `admin:karmicare-biorhythmic-oral-care-system:custom.comparison_section#37` | revised in assembly: approved NL from Figma 'Dutch offer 2.0 · NL' (3738:27474); translator had: Iemand die iets afvinkt |
| `admin:karmicare-biorhythmic-oral-care-system:custom.comparison_section#38` | revised in assembly: approved NL from Figma 'Dutch offer 2.0 · NL' (3738:27474); translator had: Iemand die het wel wil |
| `admin:karmicare-biorhythmic-oral-care-system:custom.mission_card#02` | Brand promise (binding). |
| `admin:karmicare-biorhythmic-oral-care-system:custom.mission_card#04` | revised in assembly: approved NL from Figma 'Dutch offer 2.0 · NL' (3738:27474); translator had: Ik bouwde Karmicare vanuit mijn eigen reset — toen de zorg voor mijn mond zorg voor heel mezelf werd. |
| `admin:karmicare-biorhythmic-oral-care-system:custom.how_it_works_steps#02` | revised in assembly: approved NL from Figma 'Dutch offer 2.0 · NL' (3738:27474); translator had: Spoel je mond voor je poetst. |
| `admin:karmicare-biorhythmic-oral-care-system:custom.compare_table_header_footer#03` | 20 → 29 chars; heading line. |
| `admin:karmicare-biorhythmic-oral-care-system:custom.compare_table|shop.metaobjects.compare_value#01` | revised in assembly: approved NL from Figma 'Dutch offer 2.0 · NL' (3738:27474); translator had: Begin met één set, vul aan om de 60 dagen of kies het volledige jaar — het ritueel blijft hetzelfde: Awake 's ochtends, |
| `admin:karmicare-biorhythmic-oral-care-system:custom.compare_table|shop.metaobjects.compare_value#02` | revised in assembly: approved NL from Figma 'Dutch offer 2.0 · NL' (3738:27474); translator had: Duo's per jaar |
| `admin:karmicare-biorhythmic-oral-care-system:custom.compare_table|shop.metaobjects.compare_value#04` | revised in assembly: approved NL from Figma 'Dutch offer 2.0 · NL' (3738:27474); translator had: Leverritme |
| `admin:karmicare-biorhythmic-oral-care-system:custom.compare_table|shop.metaobjects.compare_value#06` | EN is cut off mid-word ('We believe preven'); NL cut at the same point. Full NL once the EN is fixed: '… Wij vinden dat preventie moet lonen voor wie zelf de zorg draagt.' |
| `admin:karmicare-biorhythmic-oral-care-system:custom.compare_table|shop.metaobjects.compare_value#07` | revised in assembly: approved NL from Figma 'Dutch offer 2.0 · NL' (3738:27474); translator had: Verdiende Care Credit per jaar |
| `admin:karmicare-biorhythmic-oral-care-system:custom.compare_table|shop.metaobjects.compare_value#10` | Offer conflict carried over from the EN ('verified by your dentist'). |
| `admin:karmicare-biorhythmic-oral-care-system:custom.compare_table|shop.metaobjects.compare_value#11` | 21 → 31 chars; the trust-row short form 'Pauzeren of opzeggen' would drop 'skip'. |
| `admin:karmicare-biorhythmic-oral-care-system:custom.compare_table|shop.metaobjects.compare_value#14` | Approved plan name (Figma NL), 8 → 17 chars as a column header. |
| `admin:karmicare-biorhythmic-oral-care-system:custom.compare_table|shop.metaobjects.compare_value#17` | revised in assembly: approved NL from Figma 'Dutch offer 2.0 · NL' (3738:27474); translator had: Berekend bij afrekenen |
| `admin:karmicare-biorhythmic-oral-care-system:custom.compare_table|shop.metaobjects.compare_value#18` | Approved badge (Figma NL). |
| `admin:karmicare-biorhythmic-oral-care-system:custom.compare_table|shop.metaobjects.compare_value#21` | revised in assembly: approved NL from Figma 'Dutch offer 2.0 · NL' (3738:27474); translator had: Om de 60 dagen |
| `admin:karmicare-biorhythmic-oral-care-system:custom.compare_table|shop.metaobjects.compare_value#23` | revised in assembly: approved NL from Figma 'Dutch offer 2.0 · NL' (3738:27474); translator had: Te upgraden |
| `admin:karmicare-biorhythmic-oral-care-system:custom.compare_table|shop.metaobjects.compare_value#26` | Approved badge (Figma NL). |
| `admin:karmicare-biorhythmic-oral-care-system:custom.compare_table_header_footer#06` | 'return' → 'rendement' (echoes Return on Care); 30 → 41 chars. |
| `admin:karmicare-biorhythmic-oral-care-system:shop.metaobjects.compare_value:year.cost_per_brushing` | Wrong in the EN too: the Year is €0,49 per poetsbeurt (admin fix, handoff). Translated as is. |
| `admin:karmicare-biorhythmic-oral-care-system:custom.compare_table:welcome_kit_row.products` | Glossary (Figma NL) brush names, same as the product titles. |
| `index:hero_karmicare_XKKLDK/buttons_DpYxth/button_label_2` | 21 vs 17 chars; no shorter natural Dutch for 'why two formulas' |
| `index:stat_strip_karmicare/tagline` | 'health enthusiasts' → 'gezondheidsbewuste mensen' (neutral; 'gezondheidsfanaten' reads pejorative) |
| `index:stat_strip_karmicare/stat_3/text` | EN says +36 studies here, 39 on the product page highlight and 'more than 38,000 people' in the research section; kept as EN, the numbers need one source |
| `index:stat_strip_karmicare/stat_4/text` | AM/PM kept to fit (common in Dutch beauty copy); if space allows: 'ochtend- en avondzorg per duo' |
| `index:stat_strip_karmicare/stat_5/heading` | 12 vs 8 chars; shortest natural form, matches the approved 'Spugen, niet spoelen' |
| `index:chronobiology_clock_karmicare/title` | revised in assembly: approved NL from Figma 'Dutch offer 2.0 · NL' (3738:27474); translator had: Je mond volgt een 24-uursklok. |
| `index:chronobiology_clock_karmicare/morning_text` | revised in assembly: approved NL from Figma 'Dutch offer 2.0 · NL' (3738:27474); translator had: Cortisol stijgt; koffie, ontbijt en de eerste zuren van de dag volgen. Glazuur heeft eerst zijn schild nodig. |
| `index:chronobiology_clock_karmicare/night_text` | revised in assembly: approved NL from Figma 'Dutch offer 2.0 · NL' (3738:27474); translator had: Melatonine stijgt en je speeksel vloeit nog maar mondjesmaat. Wat om 22:00 op je glazuur zit, zit er om 07:00 nog. |
| `index:chronobiology_clock_karmicare/footer_link_text` | Same link text as the approved Figma NL ('Lees het onderzoek') |
| `index:two_formulas_karmicare/ingredients_list` | BIOFILM PREVENTION translated literally (C33) as the EN says it; the JEP/DETIC code bans prevention wording, allowed form would be 'helpt biofilm verminderen' |
| `index:product_benefits_karmicare_bcQ6tp/text` | 'settle gums' → 'tandvlees tot rust brengen' (not 'kalmeren' = soothe, to keep the claim as is) |
| `index:product_benefits_karmicare_bcQ6tp/card_aXhzDi/heading` | 21 vs 18 chars; 'stralender' is the idiom for teeth; shorter 'Natuurlijk witter' would turn 'brighter' into 'whiter' |
| `index:product_benefits_karmicare_bcQ6tp/card_KRCrBY/heading` | EN has a double space after the comma; not carried over |
| `index:product_benefits_karmicare_bcQ6tp/card_jN7XcL/heading` | 21 vs 18 chars; 'Eén pomp, één dosis' (19) fits if 'pompje' may go |
| `index:trusted_professionals_HAqYth/bottom_text` | 'prevented' rendered literally ('voorkomen') because the EN says it (C70); JEP/DETIC bans 'voorkomt' in claims, claims reviewer to check. TERM: practitioner → zorgverlener |
| `index:trusted_professionals_HAqYth/button_label` | Noun form ('sample pack for practitioners') to fit; 'staal' (BE) / 'monster' (NL) avoided as regional |
| `index:trusted_professionals_HAqYth/card_8dRing/hover_text` | Practitioner quote: if she gave it in Dutch originally, use her own wording instead of this back-translation |
| `index:trusted_professionals_HAqYth/card_HFdkaD/text` | 19 vs 16 chars; no shorter Dutch title |
| `index:research_behind_system_EkjATL/button_label` | revised in assembly: approved NL from Figma 'Dutch offer 2.0 · NL' (3738:27474); translator had: Ontdek het volledige bewijs |
| `index:research_behind_system_EkjATL/card_bDxUVT/heading` | Approved Figma NL wording (research card 1) |
| `index:research_behind_system_EkjATL/card_bDxUVT/result_label` | 9 vs 6 chars; standard term, no shorter Dutch label |
| `index:research_behind_system_EkjATL/card_bDxUVT/result_text` | revised in assembly: approved NL from Figma 'Dutch offer 2.0 · NL' (3738:27474); translator had: 98% afsluiting vs. 82% en 65% bij twee andere desensibiliserende technologieën |
| `index:research_behind_system_EkjATL/card_bDxUVT/method_text` | revised in assembly: approved NL from Figma 'Dutch offer 2.0 · NL' (3738:27474); translator had: SEM-vergelijking in vitro van drie pasta's, ~1% nHAp. |
| `index:research_behind_system_EkjATL/card_yMiD9D/heading` | revised in assembly: approved NL from Figma 'Dutch offer 2.0 · NL' (3738:27474); translator had: Een slechtere mondgezondheid hing samen met slechter slapen. |
| `index:research_behind_system_EkjATL/card_yMiD9D/result_label` | 9 vs 6 chars; standard term |
| `index:research_behind_system_EkjATL/card_yMiD9D/image_badge` | revised in assembly: approved NL from Figma 'Dutch offer 2.0 · NL' (3738:27474); translator had: SLAAP · LUCHTWEGEN EN MONDHOLTE |
| `index:research_behind_system_EkjATL/card_fmFMFd/result_label` | 9 vs 6 chars; standard term |
| `index:research_behind_system_EkjATL/card_fmFMFd/result_text` | revised in assembly: approved Figma NL (3738:27474) |
| `index:research_behind_system_EkjATL/card_fmFMFd/method_text` | revised in assembly: approved NL from Figma 'Dutch offer 2.0 · NL' (3738:27474); translator had: Systematische review en meta-analyse van 7 klinische trials. |
| `index:research_behind_system_EkjATL/card_fmFMFd/image_badge` | EN repeats the nHAp card's badge on the xylitol card (also on the SLS card); likely a placeholder in the EN |
| `index:research_behind_system_EkjATL/card_Hi7YUD/heading` | revised in assembly: approved NL from Figma 'Dutch offer 2.0 · NL' (3738:27474); translator had: Nano-HAp deed beter dan fluoride bij tandgevoeligheid. |
| `index:research_behind_system_EkjATL/card_Hi7YUD/result_label` | 9 vs 6 chars; standard term |
| `index:research_behind_system_EkjATL/card_Hi7YUD/result_text` | revised in assembly: approved Figma NL (3738:27474), same on homepage and PDP |
| `index:research_behind_system_EkjATL/card_JeERX6/heading` | revised in assembly: approved NL from Figma 'Dutch offer 2.0 · NL' (3738:27474); translator had: Geen SLS betekende minder en kortere aften. |
| `index:research_behind_system_EkjATL/card_JeERX6/subtext` | revised in assembly: approved NL from Figma 'Dutch offer 2.0 · NL' (3738:27474); translator had: 124 mensen · 4 cross-over-RCT's |
| `index:research_behind_system_EkjATL/card_JeERX6/result_label` | 9 vs 6 chars; standard term |
| `index:research_behind_system_EkjATL/card_JeERX6/result_text` | revised in assembly: approved NL from Figma 'Dutch offer 2.0 · NL' (3738:27474); translator had: Minder zweertjes, kortere duur, minder opstoten, minder pijn |
| `index:research_behind_system_EkjATL/card_JeERX6/method_text` | revised in assembly: approved NL from Figma 'Dutch offer 2.0 · NL' (3738:27474); translator had: Systematische review en meta-analyse van 4 cross-over-RCT's. |
| `index:research_behind_system_EkjATL/card_JeERX6/image_badge` | Same placeholder badge as the nHAp card (see the xylitol card) |
| `index:km_faq_accordion_FYcArV/faq_item_kLMHax/category` | 25 vs 20 chars (filter tab); 'Ingrediënten' alone would drop 'safety' |
| `index:km_faq_accordion_FYcArV/faq_item_AL3DKF/category` | 10 vs 7 chars (filter tab); no shorter equivalent |
| `index:km_faq_accordion_FYcArV/faq_item_AL3DKF/answer` | Numbers warning: '1980s' → 'de jaren tachtig' (Dutch idiom, same period). 'gebruikt' refers to the mineral in Japan, not to the customer |
| `index:km_faq_accordion_FYcArV/faq_item_4KMG6C/answer` | 'in 4–6' made explicit as 'binnen 4–6 weken'. 'bookend effect' → 'boekensteuneffect' (image kept; uncommon in Dutch, alternative 'het effect van je twee vaste momenten') |
| `index:featured_product_3XpDKw/loop_subscriptions_7dde8c/pricing_summary_care_credit_title` | EN plural 'Care Credits'; the program name stays singular |
| `index:featured_product_3XpDKw/loop_subscriptions_7dde8c/subscription_title` | revised in assembly: approved NL from Figma 'Dutch offer 2.0 · NL' (3738:27474); translator had: Awake & Asleep mondzorgsysteem voor ochtend en avond |
| `index:featured_product_3XpDKw/loop_subscriptions_7dde8c/shipping_value_html` | 15 vs 11 chars; 'Wisselt' (7) is shorter but reads less clearly |
| `index:featured_product_3XpDKw/loop_subscriptions_7dde8c/care_credit_text_1` | 16 vs 11 chars; '10% / order' fits exactly (Dutch 'order' is correct but less consumer-friendly) |
| `index:featured_product_3XpDKw/loop_subscriptions_7dde8c/care_credit_text_2` | 'purchase' → 'bestelling' (avoids aankoop/kopen) |
| `index:featured_product_3XpDKw/icon_with_text_wUdX3G/heading_1` | Approved Figma NL short form |
| `index:featured_product_3XpDKw/icon_with_text_wUdX3G/heading_3` | 17 vs 13 chars, but this is the approved Figma NL short form, checked in the Figma trust row |
| `index:care_comes_back/terms_link_label` | clauses → artikelen (art.); align with the term the legal chunk uses for the Terms |
| `index:care_comes_back/step_ritual/text` | 'the Year' → 'het Karmicare-jaar' here: '20% van het jaar' would read as '20% of the year' |
| `index:care_comes_back/step_next_order/title` | 22 vs 15 chars; 'Je volgende order' (17) fits if space is tight |
| `liquid:sections/hero-karmicare.liquid:149` | aria-label; design jargon 'Hero' dropped |
| `liquid:sections/hero-karmicare.liquid:251` | Suffix becomes '-modus' (Dutch compound: 'AWAKE-modus'); the code appends ' mode' with a space, so the NL key needs the hyphen form |
| `liquid:assets/chronobiology-clock-karmicare.js:91:live` | Live branch of the clock's aria-valuetext; pairs with '. Laat los om terug te gaan naar nu.' (preview branch, same line). Added in R1 (F3). |
| `liquid:assets/chronobiology-clock-karmicare.js:17` | 'clearance' (oral clearance) → 'zelfreiniging' (of the mouth) |
| `liquid:snippets/loop-widget-standard.liquid:123` | 20 vs 17 chars; 'one-time order' per the glossary. If this label shows the Try Once plan, use the approved 'Eenmalig proberen' (17) |
| `liquid:snippets/loop-widget-standard.liquid:140` | 8 vs 4 chars; Dawn's NL locale uses '/st' if space is tight |
| `liquid:assets/loop-widget.js:2452:annual` | Year plan-card label; approved Figma NL '/ jaar' (3738:27474). Added in R1 (F3). |
| `liquid:assets/loop-widget.js:2463` | The word that replaces 'ships' in the plan's option text. Dutch puts it at the end of the line, so the Loop owner should key the whole line: 'Renews every {{ days }} days' → 'Elke {{ days }} dagen verlengd' (approved Fi… |
| `liquid:assets/loop-widget.js:2464` | Per-brushing line on the plan cards; approved Figma NL '€0,49 / poetsbeurt'. {{ amount }} comes from the store money format. Added in R1 (F3). |
| `liquid:assets/loop-widget.js:2468` | revised in assembly: approved NL from Figma 'Dutch offer 2.0 · NL' (3738:27474); translator had: Jaarlijks verlengd |
| `liquid:assets/loop-widget.js:2213` | 't.w.v.' (ter waarde van) is the usual shop abbreviation in NL and BE |
| `liquid:snippets/loop-subscriptions.liquid:10` | Kept in English on purpose: featured-product.liquid:542 and main-product.liquid:616 test for this exact text, so translating it could break that check. Hidden placeholder |
| `header-group:announcement-bar/announcement-bar-0/text` | Shorter than the EN. Offer accuracy point from the inventory still applies to the NL: free shipping and the 60-day guarantee are memberships only |
| `footer-group:footer/slogan` | revised in assembly: approved Figma NL (3738:27474) |
| `footer-group:footer/copyright_text` | Compliance line: 'product' kept as in the EN (regulatory statement). EN address lacks the city (8000 Brugge); kept as EN |
| `liquid:sections/footer.liquid:667` | Placeholder address kept (the check treats e-mail addresses as fixed); 'jij@voorbeeld.be' if a Dutch placeholder is wanted |
| `liquid:sections/footer.liquid:679` | 7 vs 4 chars; no four-letter Dutch verb for 'Join' ('Aanmelden' 9) |
| `liquid:sections/footer.liquid:1058` | 18 vs 15 chars; standard term |
| `admin:navigation:new-main-menu:links[2].title` | 10 vs 7 chars; no shorter Dutch word |
| `admin:navigation:new-main-menu:links[3].title` | Dutch uses 'professionals' as is |
| `admin:navigation:company:links[1].title` | 'Shop' → 'Ontdek' (avoids buy wording) |
| `admin:navigation:company:links[2].title` | EN typo 'hydroxapatite' fixed; banned 'use' dropped |
| `admin:navigation:company:links[3].title` | 16 vs 13 chars; no shorter form |
| `page.consumer-rights:policy_banner_Pgpxip/benefit_card_MptPUi/card_description` | 'To change your mind' rendered as 'Om je te bedenken' (cooling-off idea), shorter than a literal 'Om van gedachten te veranderen'. |
| `page.consumer-rights:policy_banner_Pgpxip/benefit_card_MptPUi/card_bottom_text` | Try Once → Eenmalig proberen (glossary), capitalised as a plan name throughout. |
| `page.consumer-rights:policy_banner_Pgpxip/benefit_card_3DXGyT/card_description` | 'To receive your refund' → 'Tot je terugbetaling' (reads '14 dagen tot je terugbetaling'), to fit the card. TERM: refund → terugbetaling / terugbetalen. |
| `page.consumer-rights:legal_toc_section_gYznx3/content_section_g6nYeY/content` | Product names translated descriptively (Awake-ochtendtandpasta, Asleep-avondtandpasta, flosdraad met houtskool, tandenborstels); align with the NL product titles once they exist. 'diagnose, treat or cure' is a disclaime… |
| `page.consumer-rights:legal_toc_section_gYznx3/content_section_iDEfUH/content` | WARN 'decimal point next to a euro amount' = section numbers 3.1–3.7, not amounts. TERMs: withdraw / right of withdrawal → herroepen / herroepingsrecht; Year (plan) → het Karmicare-jaar everywhere (glossary long form; b… |
| `page.consumer-rights:legal_toc_section_gYznx3/content_section_FcEDdA/content` | Heading 4.1: EN 'presumption of conformity' is imprecise (the law presumes the lack of conformity existed at delivery); translated the intended meaning ('vermoeden van non-conformiteit'). TERMs: defect → gebrek; repair … |
| `page.consumer-rights:legal_toc_section_gYznx3/content_section_xKcNPj/content` | TERMs: delivery → levering; shipping → verzending / verzendkosten; working days → werkdagen; calendar days → kalenderdagen; checkout → afrekenen. 'additional reasonable period' → 'aanvullende redelijke termijn' (Art. VI… |
| `page.consumer-rights:legal_toc_section_gYznx3/content_section_rnPj6g/content` | TERMs: cancel (membership) → opzeggen; cancel (deliveries) → annuleren; customer portal → klantenportaal; member price → ledenprijs (approved glossary sentence reused in 'Prijsbescherming'); Terms and Conditions → algem… |
| `page.consumer-rights:legal_toc_section_gYznx3/content_section_EAKJLC/content` | 'was' price → “van”-prijs (as in 'van €X voor €Y'). 'kortingen' here means price reductions, not Care Credit. Lawyer: check the reference 'Art. VI.19/1 WER'; to my knowledge the Omnibus reference-price rule sits in Art.… |
| `page.consumer-rights:legal_toc_section_gYznx3/content_section_dGmgBJ/content` | TERMs: Consumer Mediation Service → Consumentenombudsdienst (NL name leads, FR and EN names kept in brackets); European Consumer Centre → Europees Centrum voor de Consument (its official Belgian Dutch name); out-of-cour… |
| `page.consumer-rights:legal_toc_section_gYznx3/content_section_CDtWCV/title` | jurisdiction → bevoegde rechter (standard Belgian heading). |
| `page.consumer-rights:legal_toc_section_gYznx3/content_section_at3pLy/title` | Official Dutch title of the statutory model form. |
| `page.consumer-rights:legal_toc_section_gYznx3/content_section_at3pLy/content` | Form wording follows the official Dutch model form (WER annex / Dir. 2011/83 Annex I(B)), written without 'u'; Dutch needs the verb alternatives, so (*) also follows deel/delen and herroep/herroepen as in the official f… |
| `page.privacy-policy:policy_banner_Pgpxip/eyebrow` | Eyebrow: 9 vs 5 chars, no shorter Dutch word; it sits alone above the banner heading. |
| `page.privacy-policy:policy_banner_Pgpxip/company_last_updated` | “Laatst bijgewerkt” is quoted again in section 11. |
| `page.privacy-policy:legal_toc_section_gYznx3/content_section_g6nYeY/content` | 'Data Privacy Lead' kept as an internal role title. It must not be read as a 'functionaris voor gegevensbescherming' (DPO); lawyer to confirm. |
| `page.privacy-policy:legal_toc_section_gYznx3/content_section_FcEDdA/nav_label` | Short nav form; the section title uses the AVG term 'doeleinden'. |
| `page.privacy-policy:legal_toc_section_gYznx3/content_section_EAKJLC/nav_label` | 13 vs 9 chars; shorter 'Bewaring' is possible but less clear. |
| `page.privacy-policy:legal_toc_section_gYznx3/content_section_qyyKHX/nav_label` | 11 vs 8 chars; no shorter Dutch word. |
| `page.privacy-policy:legal_toc_section_gYznx3/content_section_qyyKHX/title` | 23 vs 17 chars; 'Beveiliging' alone would drop 'data'. The heading can wrap. |
| `page.privacy-policy:legal_toc_section_gYznx3/content_section_qyyKHX/content` | 'data transfers' here is technical traffic, so 'gegevensoverdrachten', not the legal 'doorgifte'. |
| `page.privacy-policy:legal_toc_section_gYznx3/content_section_pjNTAq/nav_label` | 11 vs 7 chars; no shorter Dutch word. |
| `page.terms-and-conditions:policy_banner_Pgpxip/heading` | Standard Dutch page title; the document calls itself "Algemene Voorwaarden" (clause 2.1). Sentence case per the heading rule; in running text the document name keeps its capitals. |
| `page.terms-and-conditions:policy_banner_Pgpxip/description` | Same NL as the matching terms-of-service policy blocks. \| TERM: plan → plan |
| `page.terms-and-conditions:policy_banner_Pgpxip/company_info` | Same NL as the matching terms-of-service policy blocks. \| TERM: trading as → handelend onder de naam; VAT → btw-nummer. Place names in their Dutch form throughout (Bruges → Brugge, Belgium → België, Brussels → Brussel)… |
| `page.terms-and-conditions:policy_banner_Pgpxip/company_last_updated` | Same NL as the matching terms-of-service policy blocks. |
| `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_GLa7AN/content` | Same NL as the matching terms-of-service policy blocks. \| TERM: Enterprise number → Ondernemingsnummer; Enterprise Court of Ghent, division Bruges → Ondernemingsrechtbank Gent, afdeling Brugge |
| `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_g6nYeY/nav_label` | fit-risk: "Scope" (5 chars) has no Dutch legal equivalent of that length; "Toepassing" (10) is the shortest clear form. |
| `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_g6nYeY/content` | Same NL as the matching terms-of-service policy blocks. \| TERM: General Terms and Conditions (“Terms”) → Algemene Voorwaarden (“Voorwaarden”), capitalised wherever the EN capitalises Terms; purchaser → koper; customer … |
| `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_iDEfUH/content` | Same NL as the matching terms-of-service policy blocks. \| TERM: cosmetics → cosmetische producten (term of Verordening (EG) nr. 1223/2009); medicines / medicinal products → geneesmiddelen \| TERM: formula → formule; fo… |
| `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_FcEDdA/content` | Same NL as the matching terms-of-service policy blocks. \| TERM: money-back guarantee → geld-terug-garantie (glossary); Try Once → Eenmalig proberen; 60-Day rhythm → 60-dagenritme; the Year → het Karmicare-jaar (the glo… |
| `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_xKcNPj/title` | "discounts" here means price reductions (5.5), not Care Credit; "kortingen" is the plain word. |
| `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_xKcNPj/content` | Same NL as the matching terms-of-service policy blocks. \| TERM: member price → ledenprijs (glossary); price protection → prijsbescherming \| TERM: checkout → het afrekenen / afrekenproces \| Lawyer: please verify the a… |
| `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_rnPj6g/content` | Same NL as the matching terms-of-service policy blocks. |
| `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_EAKJLC/content` | Same NL as the matching terms-of-service policy blocks. \| TERM: defect → gebrek (manufacturing defect → fabricagefout); covered → gedekt; excluded → uitgesloten \| TERM: Belgian Civil Code → Belgisch Burgerlijk Wetboek… |
| `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_EAKJLC/block_content` | Same NL as the matching terms-of-service policy blocks. |
| `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_dGmgBJ/content` | Same NL as the matching terms-of-service policy blocks. |
| `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_CDtWCV/content` | Same NL as the matching terms-of-service policy blocks. \| "No lock-in" → "Je zit nergens aan vast". Lawyer: the Year is paid for a full year and, once renewed, ends with one month's notice (9.9); check that "no lock-in… |
| `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_nEOBgC/content` | Same NL as the matching terms-of-service policy blocks. \| TERM: Dental Check-up Reward → controlebeloning (glossary); starting questionnaire → startvragenlijst; follow-up questionnaire → vervolgvragenlijst \| EN ambigu… |
| `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_CXUxDh/content` | Same NL as the matching terms-of-service policy blocks. |
| `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_at3pLy/content` | Same NL as the matching terms-of-service policy blocks. |
| `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_qyyKHX/content` | Same NL as the matching terms-of-service policy blocks. |
| `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_pjNTAq/content` | Same NL as the matching terms-of-service policy blocks. |
| `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_m4qTXH/content` | Same NL as the matching terms-of-service policy blocks. \| TERM: Consumer Mediation Service → Consumentenombudsdienst; European Consumer Centre → Europees Centrum voor de Consument \| Ombudsdienst address given with its… |
| `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_fz6KEQ/content` | Same NL as the matching terms-of-service policy blocks. \| EN "an eligible, unopened contract": a contract cannot be unopened; translated as the intended "a contract for unopened goods that is eligible". Lawyer: the sta… |
| `admin:page:new-consumer-rights:body_html#b001` | The admin body_html was captured as a single 'Date:' block; looks like a leftover in the page body. |
| `admin:page:new-consumer-rights:seo.title` | 'New' in the EN title looks like an admin leftover from the handle new-consumer-rights; translated as written. Without it: 'Consumentenrechten – KARMICARE'. |
| `admin:page:privacy-policy:seo.title` | EN 'New' looks like a leftover from the page's draft name; translated faithfully. Suggest 'Privacybeleid – KARMICARE' (as the policy SEO title) once the EN drops 'New'. |
| `admin:page:terms-and-conditions-1:body_html#b001` | The admin page body holds only this label (looks like a leftover of the withdrawal form); translated as is. |
| `admin:page:terms-and-conditions-1:seo.title` | EN "New Terms and Conditions" looks like a leftover from when the page was created; translated faithfully, consider dropping "Nieuwe". |
| `admin:policy:privacy-policy:body#b008` | Official Dutch title of the act. |
| `admin:policy:privacy-policy:body#b009` | Official Dutch title of the act; EC → EG. |
| `admin:policy:privacy-policy:body#b011` | 31 vs 18 chars; no shorter correct legal term, the heading may wrap. |
| `admin:policy:privacy-policy:body#b014` | EN source: the mailto link also wraps the phone number (the page-settings version links only the e-mail). Kept as in the EN. |
| `admin:policy:privacy-policy:body#b044` | 'voorkomen' here is fraud prevention (EN 'preventing'), not a cosmetic claim. |
| `admin:policy:privacy-policy:body#b094` | CIR92 → WIB 92 (Dutch abbreviation of the same code). Lawyer: check art. III.86 vs III.88 WER (see page-settings note). |
| `admin:policy:privacy-policy:body#b127` | “Cookie-instellingen” must match the NL footer link label. |
| `admin:policy:privacy-policy:body#b128` | 23 vs 17 chars; 'Beveiliging' alone would drop 'data'. The heading can wrap. |
| `admin:policy:terms-of-service:body#b015` | Link (href and visible URL) still points to the English page /en/…; kept unchanged per the rules. Needs the NL URL once the Dutch page exists. |
| `admin:policy:terms-of-service:body#b020` | “Pay now” → “Nu betalen”: check that this is the exact label of the final button in the Dutch Shopify checkout. |
| `admin:policy:terms-of-service:body#b049` | Lawyer: whether priming an airless pump counts as "unsealing" under art. VI.53, 5° WER is a legal judgement in the EN itself; the translation keeps it as written. |
| `admin:policy:terms-of-service:body#b052` | EN gap: this procedure (and the Annex) covers withdrawal from a one-time order only, while 4.1.1 also grants withdrawal for memberships. Lawyer to confirm. |
| `admin:policy:terms-of-service:body#b053` | EN inconsistency: only 4.4 is named, but 4.3, 4.6 (loss of value, art. VI.51 §2 WER) and 4.7 (spent Care Credit) also allow deductions. Translated as written. |
| `admin:policy:terms-of-service:body#b055` | "discounts" here means price reductions (5.5), not Care Credit; "kortingen" is the plain word. |
| `admin:policy:terms-of-service:body#b061` | Lawyer: please verify the article number; as far as I know the Belgian reference-price rule for announced price reductions sits in art. VI.18 WER. |
| `admin:policy:terms-of-service:body#b069` | Lawyer: arts. 1649bis–1649octies are in the "oud Burgerlijk Wetboek" and art. 5.226 (clause 12) in the new Burgerlijk Wetboek; the EN calls both "Belgian Civil Code". Also check that the §2 (notification) and §4 (nature… |
| `admin:policy:terms-of-service:body#b071` | EN "present at or arising from delivery" is loose; translated literally ("bij de levering aanwezig zijn of eruit voortvloeien"). |
| `admin:policy:terms-of-service:body#b072` | Lawyer: under Belgian consumer-sales law the consumer chooses between repair and replacement; the EN offers replacement only. Translated as written. |
| `admin:policy:terms-of-service:body#b101` | revised in assembly: identical legal passage: same NL as the Terms of Service |
| `admin:policy:terms-of-service:body#b107` | "No lock-in" → "Je zit nergens aan vast". Lawyer: the Year is paid for a full year and, once renewed, ends with one month's notice (9.9); check that "no lock-in" holds. |
| `admin:policy:terms-of-service:body#b121` | EN ambiguity: "you receive €5" does not say that the €5 is paid as Care Credit or whether non-members qualify; translated literally. |
| `admin:policy:terms-of-service:body#b147` | Ombudsdienst address given with its official Dutch street name (Boulevard du Roi Albert II 8, box 1 = Koning Albert II-laan 8, bus 1); numbers unchanged. The NL parenthesis repeats "Consumentenombudsdienst" because the … |
| `admin:policy:terms-of-service:body#b153` | EN "an eligible, unopened contract": a contract cannot be unopened; translated as the intended "a contract for unopened goods that is eligible". Lawyer: the statutory model form has no "unopened" condition. |
| `admin:policy:terms-of-service:body#b155` | Follows the official Dutch model form, without its "u" (je register) and with the (*) marks at the EN positions. |
| `admin:policy:terms-of-service:body#b161` | revised in assembly: identical legal passage: same NL as the Terms of Service |
| `admin:policy:terms-of-service:body#b164` | revised in assembly: identical legal passage: same NL as the Terms of Service |
| `admin:policy:refund-policy:title` | Shopify policy title; 20 vs 13 chars. No shorter correct term: 'Retourbeleid' would mean return policy. Title links wrap in the checkout footer. |
| `admin:policy:refund-policy:body#b018` | 'biological formulations' → 'op de biologie gebaseerde formules' (Dutch 'biologisch' = organic); see the page item. |
| `admin:policy:refund-policy:body#b027` | Product names translated descriptively; align with the NL product titles once they exist. |
| `admin:policy:refund-policy:body#b031` | Lawyer/claims: free-from claim (parabens, endocrine disruptors); see the page item. |
| `admin:policy:refund-policy:body#b032` | 'diagnose, treat or cure' is a disclaimer, translated literally. |
| `admin:policy:refund-policy:body#b037` | Lawyer: refund deadline and 'unopened' condition vs Art. VI.50 WER; see the page item. |
| `admin:policy:refund-policy:body#b054` | Capture artefact kept: in the policy the mailto link wraps the phone number too (the page has separate mailto and tel links). Plain text matches the page. |
| `admin:policy:refund-policy:body#b061` | Lawyer: 'unprimed pump = seal' for the hygiene exception (Art. VI.53, 5° WER); see the page item. |
| `admin:policy:refund-policy:body#b065` | EN 'presumption of conformity' is imprecise; translated the intended meaning (presumption that the lack of conformity existed at delivery). Same as the page item. |
| `admin:policy:refund-policy:body#b074` | revised in assembly: identical legal passage: same NL as the Terms of Service |
| `admin:policy:refund-policy:body#b086` | EN check: the per-pause cap equals the yearly total; translated as written (see the page item). |
| `admin:policy:refund-policy:body#b094` | Lawyer: check 'Art. VI.19/1 WER' (see the page item). |
| `admin:policy:refund-policy:body#b100` | Capture artefact kept: the mailto link wraps the phone number too (separate links on the page). The EN comma after the number is not needed in Dutch. |
| `admin:policy:refund-policy:body#b103` | Official Dutch street name (Boulevard du Roi Albert II = Koning Albert II-laan); number, 'bus 1' and postcode unchanged. See the page item. |
| `admin:policy:refund-policy:body#b113` | Capture artefact kept: the mailto link wraps the phone number too (separate links on the page). |
| `admin:policy:refund-policy:body#b114` | Official Dutch model-form wording without 'u'; (*) added after the Dutch verb alternatives as in the official form (all EN marks kept). |
| `admin:policy:refund-policy:body#b120` | revised in assembly: identical legal passage: same NL as the Terms of Service |
| `admin:policy:refund-policy:body#b122` | EN 'an eligible, unopened contract' is ambiguous; see the page item. |
| `admin:policy:refund-policy:body#b123` | revised in assembly: identical legal passage: same NL as the Terms of Service |
| `admin:policy:shipping-policy:body#b001` | Link still points to the English page /en/… (href unchanged). |
| `admin:policy:shipping-policy:body#b002` | Identical to terms-of-service b100. |
| `admin:policy:shipping-policy:body#b003` | revised in assembly: identical legal passage: same NL as the Terms of Service |
| `admin:policy:shipping-policy:body#b004` | Identical to terms-of-service b102. |
| `admin:policy:shipping-policy:body#b005` | Identical to terms-of-service b103. |
| `admin:policy:shipping-policy:body#b006` | Identical to terms-of-service b104. |
| `admin:policy:shipping-policy:body#b007` | Identical to terms-of-service b105. |
| `admin:policy:shipping-policy:body#b008` | Same NL as terms-of-service b060 (clause 5.4), plus the clause reference. |
| `admin:policy:contact-information:body#b005` | EN source: the mailto link also wraps the phone number. Kept as in the EN. |
| `admin:policy:contact-information:body#b006` | EN source: the mailto link wraps 'or call +32 …' (a phone number inside an e-mail link); kept, link text translated. |
| `admin:policy:legal-notice:body#b001` | href unchanged (EN terms page); see contact-information b001. |
| `admin:policy:legal-notice:seo.title` | 35 vs 24 chars (page title, not a UI slot); see legal-notice title. |
| `admin:policy:subscription-policy:body#b001` | Link still points to the English page /en/… (href unchanged). |
| `admin:policy:subscription-policy:body#b002` | Identical to terms-of-service b106. |
| `admin:policy:subscription-policy:body#b003` | Identical to terms-of-service b107. \| "No lock-in" → "Je zit nergens aan vast". Lawyer: the Year is paid for a full year and, once renewed, ends with one month's notice (9.9); check that "no lock-in" holds. |
| `admin:policy:subscription-policy:body#b004` | Identical to terms-of-service b108. |
| `admin:policy:subscription-policy:body#b005` | Identical to terms-of-service b109. |
| `admin:policy:subscription-policy:body#b006` | Identical to terms-of-service b110. |
| `admin:policy:subscription-policy:body#b007` | Identical to terms-of-service b111. |
| `admin:policy:subscription-policy:body#b008` | Identical to terms-of-service b112. |
| `admin:policy:subscription-policy:body#b009` | Identical to terms-of-service b113. |
| `admin:policy:subscription-policy:body#b010` | Identical to terms-of-service b114. |
| `admin:policy:subscription-policy:body#b011` | Identical to terms-of-service b115. |
| `admin:policy:subscription-policy:body#b012` | Identical to terms-of-service b116. |
| `admin:policy:subscription-policy:body#b013` | Identical to terms-of-service b117. |
| `product:main/highlights_slider_9wAjAb/text_1` | EN 'Used' is a banned word in customer copy; kept literal ('gebruikt' by practitioners, not the customer). 'kPNI practitioners' → 'kPNI-therapeuten' (the usual Dutch title) |
| `product:main/highlights_slider_9wAjAb/text_3` | 39 here vs '+36 studies' on the homepage stat strip; kept as EN |
| `product:main/icon_with_text_xhaDGB/heading_1` | revised in assembly: added in assembly (the keyword scan had held it; the claims review cleared it); same trust-row form as the Duo buy box (Figma NL) |
| `product:main/icon_with_text_xhaDGB/heading_3` | 17 vs 13 chars, but this is the approved Figma NL short form, checked in the Figma trust row |
| `product:main/treatment_journey_block/disclaimer_text` | revised in assembly: approved Figma NL (3738:27474); same on product.json and the Duo PDP |
| `product:main/professional_testimonials_block/heading` | EN 'Used' kept literal (professionals, not the customer); EN could be reworded |
| `product:main/info_card_FnBcaN/body_text` | 'Health Rewards' kept as a name: legacy program name next to Care Credit, EN needs a decision. 'purchase' → 'bestelling', 'products' → 'artikelen' |
| `product:disclosures/heading` | Section holds safety warnings and regulatory disclosures; 'Wettelijke vermeldingen' is clearer if space allows |
| `admin:app:judge-me:preview_badge.review_count` | 'review' is standard Dutch; Judge.me may also offer 'beoordeling(en)' |
| `admin:product:morning-toothbrush:seo.description` | EN meta is the body cut mid-word ('by ea'); NL completes the sentence from the body. EN typos read as intended: 'dispurge' = disperse, 'of' = or, 'nurished' = nourished |
| `admin:product:evening-toothbrush:seo.description` | EN meta cut mid-word ('applicati'); NL completes the sentence. '2 to 4 applications' predates the 1-pump dose (products.md, 4 Aug) |
| `admin:product:whitening-charcoal-dental-floss:seo.description` | EN meta cut mid-word ('removi'); NL completes the sentence from the body |
| `admin:product:evening-toothbrush-2-0:seo.description` | EN meta cut mid-word; NL completes the sentence. '2 to 4 applications' predates the 1-pump dose |
| `admin:product:morning-toothbrush-2-0:seo.description` | EN meta cut mid-word; NL completes the sentence from the body |
| `admin:product:morning-toothbrush:body_html#b001` | EN typos read as intended ('dispurge' = disperse, 'of' = or, 'nurished' = nourished). '2 to 4 applications' predates the 1-pump dose. Link still points to the old /en/product/ URL (kept) |
| `admin:product:evening-toothbrush:body_html#b001` | '2 to 4 applications' predates the 1-pump dose. Link still points to the old /en/product/ URL (kept) |
| `admin:product:evening-toothbrush:media.27295901221046.alt` | EN alt is already Dutch ('Karmicare Avond Tandenborstel'); the EN source should read 'Karmicare Evening Toothbrush' |
| `admin:product:whitening-charcoal-dental-floss:title` | revised in assembly: same Shopify product title inventoried twice (B1a kit item, B2 product page); Figma NL wording |
| `admin:product:whitening-charcoal-dental-floss:body_html#b001` | The '*' has no footnote in the EN either |
| `admin:app:whitening-charcoal-dental-floss:selling_plan_group:Subscribe and Save` | revised in assembly: one form for every legacy 'Subscribe and Save' group |
| `admin:app:whitening-charcoal-dental-floss:selling_plan.712456601981.name` | EN typo 'month' → plural |
| `admin:app:whitening-charcoal-dental-floss:selling_plan.712460992893.name` | EN has a leading space (admin typo); NL without |
| `admin:product:evening-toothbrush-2-0:title` | revised in assembly: same Shopify product title inventoried twice; faithful title |
| `admin:product:evening-toothbrush-2-0:body_html#b001` | '2 to 4 applications' predates the 1-pump dose. Link points to the old /en/product/ URL and to the legacy brush (kept) |
| `admin:product:evening-toothbrush-2-0:media.27295901221046.alt` | EN alt is already Dutch; the EN source should read 'Karmicare Evening Toothbrush' |
| `admin:app:evening-toothbrush-2-0:selling_plan_group:Subscribe and Save` | revised in assembly: one form for every legacy 'Subscribe and Save' group |
| `admin:app:evening-toothbrush-2-0:selling_plan.712456634749.name` | EN typo 'month' → plural |
| `admin:app:evening-toothbrush-2-0:selling_plan.712460992893.name` | EN leading space dropped |
| `admin:product:morning-toothbrush-2-0:title` | revised in assembly: same Shopify product title inventoried twice; faithful title (the Figma 'Ultrazachte ochtendborstel' is a buy-box label for a different EN) |
| `admin:product:morning-toothbrush-2-0:body_html#b001` | EN typos read as intended ('dispurge', 'of', 'nurished'). '2 to 4 applications' predates the 1-pump dose. Link points to the old /en/product/ URL (kept) |
| `admin:app:morning-toothbrush-2-0:selling_plan_group:Subscribe and Save` | revised in assembly: one form for every legacy 'Subscribe and Save' group |
| `admin:app:morning-toothbrush-2-0:selling_plan.712456667517.name` | EN typo 'month' → plural |
| `admin:app:morning-toothbrush-2-0:selling_plan.712460992893.name` | EN leading space dropped |
| `admin:product:asleep-evening-toothpaste-2-0:body_html#b002` | Sleep-effect claim, but this block is not flagged pending-claim-review in the input; claims reviewer to check |
| `admin:app:asleep-evening-toothpaste-2-0:selling_plan_group:Subscribe and Save` | revised in assembly: one form for every legacy 'Subscribe and Save' group |
| `admin:app:asleep-evening-toothpaste-2-0:selling_plan.712456700285.name` | EN typo 'month' → plural |
| `admin:app:asleep-evening-toothpaste-2-0:selling_plan.712460992893.name` | EN leading space dropped |
| `admin:product:awake-morning-toothpaste-2-0:body_html#b002` | Wake-effect claim, not flagged pending-claim-review in the input; claims reviewer to check |
| `admin:app:awake-morning-toothpaste-2-0:selling_plan_group:Subscribe and Save` | revised in assembly: one form for every legacy 'Subscribe and Save' group |
| `admin:app:awake-morning-toothpaste-2-0:selling_plan.712456733053.name` | EN typo 'month' → plural |
| `admin:app:awake-morning-toothpaste-2-0:selling_plan.712460992893.name` | EN leading space dropped |
| `admin:page:why-karmicare:title` | 16 vs 13 chars; no shorter form |
| `admin:page:why-karmicare:body_html#b001` | No final full stop, as in the EN |
| `admin:page:why-use-hydroxyapatite-toothpaste:title` | 'use' → 'kiezen voor' (avoids 'gebruiken') |
| `admin:page:why-use-hydroxyapatite-toothpaste:body_html#b001` | 'start using' → 'overstappen op' (avoids 'gebruiken') |
| `admin:page:why-stop-using-fluoride-toothpaste:seo.description` | Full stop added between the two joined body blocks (the EN runs them together) |
| `admin:collection:vgbc2025:text#02` | Collection title is a code; kept as is. |
| `admin:article:news/nano-hydroxyapatite:body_html#b005` | Article subheading, no UI length limit. |
| `admin:article:news/nano-hydroxyapatite:body_html#b027` | EN 'phosphorous oxygen' read as 'phosphorus, oxygen'. |
| `admin:article:news/nano-hydroxyapatite:body_html#b036` | 'voorkomt' here means 'occurs', not 'prevents'. |
| `admin:article:news/nano-hydroxyapatite:body_html#b074` | The EN article has no heading 2 between 1 and 3. |
| `admin:article:news/nano-hydroxyapatite:seo.title` | EN typo 'Hydroxapatite' (SEO title); the NL uses the correct spelling. |
| `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:body_html#b005` | Article subheading, no UI length limit. |
| `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:body_html#b051` | Article subheading, no UI length limit. |
| `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:seo.description` | The EN meta description is cut off ('m…'); the NL stops at the same point. |
| `admin:article:news/nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste:body_html#b005` | Article subheading, no UI length limit. |
| `admin:article:news/nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste:body_html#b049` | The EN article has no heading 2 between 1 and 3. |
| `admin:article:news/nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste:body_html#b067` | EN 'Shop Now' rendered with 'Begin' (no 'kopen' in customer copy). |
| `admin:article:news/nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste:seo.description` | The EN meta description is cut off mid-word ('fl…'); the NL completes the last word. |
| `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b005` | Article subheading, no UI length limit. |
| `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b078` | EN 'Shop Now' rendered as 'Begin nu' (no 'kopen' in customer copy). |
| `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b095` | EN 'in a tube': rendered 'in één flacon' (Karmicare comes in pump bottles; 'tube' is a banned word). |
| `admin:article:news/how-oral-health-impacts-your-overall-wellness:seo.description` | The EN meta description is cut off; the NL stops at the same point. |
| `admin:article:news/top-natural-whitening-toothpaste-for-a-brighter-smile:body_html#b002` | The EN sentence is incomplete ('With more people shifting…'); translated as a complete sentence. |
| `admin:article:news/top-natural-whitening-toothpaste-for-a-brighter-smile:body_html#b011` | EN 'Shop' rendered as 'Ontdek'. |
| `admin:article:news/top-natural-whitening-toothpaste-for-a-brighter-smile:body_html#b051` | EN 'Shop Our Bestselling' rendered as 'Ontdek onze populairste'. |
| `admin:article:news/top-natural-whitening-toothpaste-for-a-brighter-smile:seo.description` | The EN meta description is cut off; the NL stops at the same point. |
| `admin:article:news/5-reasons-you-should-avoid-fluoride-in-toothpaste:body_html#b005` | Article subheading, no UI length limit. |
| `admin:article:news/5-reasons-you-should-avoid-fluoride-in-toothpaste:body_html#b015` | 'voorkomt' here means 'occurs', not 'prevents'. |
| `admin:article:news/5-reasons-you-should-avoid-fluoride-in-toothpaste:body_html#b070` | EN 'Shop' rendered as 'Ontdek' (no 'kopen' in customer copy). |
| `admin:article:news/headaches-and-tooth-pain-understanding-the-connection:body_html#b010` | EN 'Shop' rendered as 'Ontdek'. |
| `admin:article:news/headaches-and-tooth-pain-understanding-the-connection:body_html#b019` | EN 'Shop Our Bestselling' rendered as 'Ontdek onze populairste'. |
| `admin:article:news/headaches-and-tooth-pain-understanding-the-connection:body_html#b043` | EN 'Shop Now' rendered as 'Begin nu'. |
| `admin:article:news/headaches-and-tooth-pain-understanding-the-connection:seo.description` | The EN meta description is cut off; the NL stops at the same point. |
| `admin:article:news/3-reasons-why-you-should-look-for-an-sls-free-toothpaste:body_html#b005` | Article subheading, no UI length limit. |
| `admin:article:news/3-reasons-why-you-should-look-for-an-sls-free-toothpaste:body_html#b035` | The EN names competitors (Colgate, Biotene, Sensodyne Pronamel, Tom's of Maine); kept as in the EN. Brand rules forbid naming competitors: flag for Victor. 'before you buy' rendered without 'kopen'. |
| `admin:article:news/3-reasons-why-you-should-look-for-an-sls-free-toothpaste:body_html#b043` | EN 'Shop … Now' rendered as 'Ontdek nu'. |
| `admin:article:news/3-reasons-why-you-should-look-for-an-sls-free-toothpaste:seo.description` | The EN meta description is cut off; the NL stops at the same word. |

</details>
