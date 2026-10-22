# NL translation payloads · report (B2)

Task `task_25fdff87b2e8`, Orca run `run_32dd5602b983`, branch `karmicare/soft-launch-source-copy`. 19 Oct 2026. Ready for Astra's review.

Dutch for every page of the live store, translated from the approved EN inventory. The files are payloads only. Nothing is in the theme, `locales/` or the Shopify admin yet; the localization worker registers them later.

**R1 update (task `task_07508030e174`).** After the B1a review fixes, batch 01 has a new digest (`a09219ae1af8`, 225 entries). The four new runtime strings (F3) are translated as `theme-key`. Statuses are refreshed for the F1/F2 claim links: the research result lines, evidence counts and leave-on safety lines are now `pending-claim-review`, and the "Radiant calm gums" heading is held with the rest of benefit card 06.

**R2 update (task `task_7dc91e6a67f1`).** The independent NL review `docs/runtime-review/B2-NL-ASTRA.md` returned FAIL with ten findings. All ten are fixed; the section "R2 fixes" below lists them with their commits. In short:
- the sleep/wake lines and a competitor block are held;
- the nHAp body heading is a new entry (batch 06 digest `3dee3b56341f`);
- 16 entries are reclassified to needs-review;
- legal meaning, claim strength, addresses and repeated strings follow the EN again;
- `validate.py` now checks every hold and gate.

**R6 update (task `task_e2db4c0f9717`).** The re-review `docs/runtime-review/B2-NL-R6-ASTRA.md` (PASS WITH FIXES) raised R6-01 to R6-03, and all three are fixed; the section "R6 fixes" below has the details.
- 30 more blog blocks are pending-claim-review, among them wellness `#b081`.
- Commodity compounds and the later uses of *tandpasta* are gone from the nine NL articles.
- The R2 claim aggregate is corrected.
- `validate.py` gains the W1 commodity-word check.

**Delivery times (20 Oct, Victor).** Benelux is now *binnen 24 uur* and the rest of the EU *2–3 werkdagen*, in six entries: the delivery sections of consumer rights and the terms, and the policies terms-of-service `#b104`, shipping-policy `#b006`, refund-policy `#b080`/`#b081`. The PDP sticky line mirrors the nav child's locale value: *Gratis snelle levering: 24 uur in de Benelux. 2–3 dagen in de rest van Europa*. Statuses are unchanged.

The theme templates are changed in `6414e4c`. The three Shopify policies are Admin text, so Victor edits the live EN (Settings > Policies), and the NL below is registered with the rest of batch 04:

| Policy field | EN before | EN after | NL after |
|---|---|---|---|
| terms-of-service `#b104`, shipping-policy `#b006` | Delivery times (estimates): Belgium, the Netherlands and Luxembourg 1–3 working days; rest of the European Union 2–5 working days. | Delivery times (estimates): Belgium, the Netherlands and Luxembourg: within 24 hours; rest of the European Union: 2–3 working days. | Levertijden (schattingen): België, Nederland en Luxemburg: binnen 24 uur; rest van de Europese Unie: 2–3 werkdagen. |
| refund-policy `#b080` | Belgium, the Netherlands and Luxembourg: 1–3 working days | Belgium, the Netherlands and Luxembourg: within 24 hours | België, Nederland en Luxemburg: binnen 24 uur |
| refund-policy `#b081` | Rest of the European Union: 2–5 working days | Rest of the European Union: 2–3 working days | Rest van de Europese Unie: 2–3 werkdagen |

The NL before was the same text with *1–3 werkdagen* and *2–5 werkdagen*. The labels in bold (*Delivery times (estimates):*, the country names) stay bold.

**Duo name (20 Oct, Victor; PDP `50ad819`).** The Duo's name is the Shopify product title, so three entries are `retired` in the source and held here:
- the two `subscription_title` settings (homepage and PDP featured product);
- the sticky-bar `package_name` default `liquid:sections/main-product.liquid:1098`.

Their NL was *Awake & Asleep AM/PM-mondzorgsysteem*. The naming source is now `admin:karmicare-biorhythmic-oral-care-system:title`, NL *Awake & Asleep tandpastasysteem voor ochtend en avond* (`admin`, in the plan). `validate.py` H8 holds every retired entry. The NL plan drops two items (1825, first wave 520).

**Homepage copy (21 Oct, integration `41ae772`, homepage lane merchant-edit `97ce2b7`).** The EN source follows the new homepage text, and the NL follows it (batch 01 digest `46f2753b65fd`, 228 entries; batch 02 digest `2846c75e4df9`):

| Entry | EN now | NL now | Status |
|---|---|---|---|
| stat-strip tagline | CHOSEN BY KPNI PRACTITIONERS, FUNCTIONAL DENTISTS, HEALTH PROFESSIONALS | GEKOZEN DOOR KPNI-THERAPEUTEN, FUNCTIONELE TANDARTSEN, ZORGPROFESSIONALS | pending-claim-review (C80) |
| practitioner titles, homepage and PDP (6) | *Therapist* → *Practitioner* | unchanged: *kPNI-therapeut*, *orthomoleculair therapeut*, *Voedingstherapeut* (the usual Dutch titles) | translated |
| FAQ `kLMHax` | The ritual · How long does one duo last? · About 64 days — one full cycle… | Het ritueel · Hoe lang gaat één duo mee? · Ongeveer 64 dagen — één volledige cyclus… | translated (C07, approved) |
| FAQ `7jmEGi` (disabled) | Ingredients & safety · Can I combine Karmicare with fluoride toothpaste or rinses? · Better not… | Ingrediënten & veiligheid · Kan ik Karmicare combineren met fluoridetandpasta of -mondspoelingen? · Liever niet… | pending-claim-review (C101) |
| FAQ `AL3DKF` (disabled) | Ingredients & safety · Is Karmicare fluoride-free? · Karmicare is fluoride-free, and always will be… | Ingrediënten & veiligheid · Is Karmicare fluoridevrij? · Karmicare is fluoridevrij, en dat blijft zo… | pending-claim-review (C102) |
| FAQ `Pz4mRk` (new) | Plans & Return on Care · Can I pause, skip or cancel? · Your membership is completely in your hands. Amend when desired. | Plannen & Return on Care · Kan ik pauzeren, overslaan of opzeggen? · Je lidmaatschap ligt volledig in jouw handen. Pas het aan wanneer je wilt. | translated |
| FAQ `qUxYCn` | Shipping & guarantee · What does the money-back guarantee cover? · Every first order comes with a money-back guarantee… | Verzending & garantie · Wat dekt de geld-terug-garantie? · the same NL as the guarantee line in the legal texts | translated |
| FAQ `4KMG6C` (removed) | — | held, `retired` | held |

The two former `[NEEDS APPROVED COPY]` answers are filled, so decision S1 on the review page (two missing FAQ answers) no longer applies. The claims C13, C23, C24 and C93 have left the homepage FAQ (`docs/claims/REPORT.md`). Two PDP step numbers in a disabled section are empty at `41ae772` and are retired. Already translated before this update, and unchanged: `fluoride, SLS`, `05 · Xylitol`, `08 · Leave-on` (the same in Dutch). Still held or pending:
- the ingredient list with *VEGAN & HALAL* (pending-claim-review, C30 and C33);
- benefit card 06 *Radiant calm gums* (held, unsupported C35).

The NL plan is now 1827 items, of which 523 are in the first wave.

**Theme keys (21 Oct, release QA B-03/B-04).** `theme_keys.py` no longer holds a key for pending-claim-review or legal-review: Victor waived those holds for translation, and the reviews gate publication and registration instead. They stay on the entries, and `theme-keys.json` lists them per key in `nl_review` / `fr_review`. `locales/nl.json` now carries the NL for `kc.clock.window_1` (C54) and for `kc.clock.loading`. That key is inventoried as `locale:kc.clock.loading` (*Huidige lokale tijd wordt geladen*, theme-key). `locales/fr.json` carries the FR of 66f0c68 for the seven clock windows and the four footer legal keys. `write` now keeps the key order of each locale file, so the 29 other locales are unchanged.

**Announcement line and e-mail placeholder (21 Oct, Victor G-1 and G-3, global lane).**
- The announcement EN is now *COMPLIMENTARY SHIPPING & 60-DAY MONEY-BACK GUARANTEE FOR MEMBERS · BELGIAN-MADE · CIRCADIAN ORAL CARE SINCE 2017* (`3c03acb`, `corrected`, batch 03 digest `a853d438d503`). The NL is *GRATIS VERZENDING & 60 DAGEN GELD TERUG VOOR LEDEN · GEMAAKT IN BELGIË · CIRCADIAANSE MONDVERZORGING SINDS 2017*, `pending-claim-review` (C103: the date has no source in the repo). *Voor leden* solves the offer conflict the old line had.
- Later that day Victor chose the short line (global-nav `1bfe574`): *FREE SHIPPING & 60-DAY GUARANTEE FOR MEMBERS · BELGIAN-MADE · EST. 2017*, NL *GRATIS VERZENDING & 60 DAGEN GELD TERUG VOOR LEDEN · GEMAAKT IN BELGIË · SINDS 2017* (batch 03 digest `d5353b16cc57`). He then confirmed the year (“EST. 2017 is bevestigd”), so C103 is `confirmed` and the NL entry is `translated`.
- The newsletter placeholder `kc.footer.email_placeholder` is *jij@voorbeeld.be* (NL) and *vous@exemple.be* (FR), as in `4954820`. `theme-keys.json` records both under `decided`, and `theme_keys.py refresh` keeps a decided value whatever the payload says, so `write` no longer returns to *you@example.com*.

**Sticky-bar key retired (21 Oct, global-nav `27691cb`, NV-13).** The desktop sticky bar becomes the mobile card, and the setting `kit_free` and its markup are gone. `kc.sticky_cart.kit_free_html` (*Gratis*) leaves `theme-keys.json` and all 31 locales. `theme-keys.json` lists it under `retired_keys`: `write` removes a retired key and `check` fails while one is still in a locale. The entry `liquid:sections/main-product.liquid:1104` is `retired` in the source and held here. Until global-nav lands, `snippets/sticky-cart-block.liquid:70` on this branch still reads the key, so Theme Check on this branch alone reports one `TranslationKeyExists` error. On `27691cb` with these locales it reports 0 errors.

**Claim holds waived (20 Oct, Victor, via the landing desk).** Victor's instruction was to translate everything that exists in English and to ignore the claim checks for now. The claims review still gates publication. Accordingly:
- The 119 entries held on an unsupported claim now carry `claim_hold_waived: "2026-10-20 Victor, translation only"` in the EN source. The EN is unchanged.
- In NL they are translated faithfully and flagged `pending-claim-review`. Each note starts with *claim hold waived by Victor 20 Oct for translation; claims review still pending for publication*.
- The 119 are: benefit card 06 (C35), Sietske Hamelink's quote on both templates (C85, held again, see below), 6 product blocks, 2 content-page blocks and 107 article blocks.
- `validate.py` H1 accepts a translated unsupported claim only with the waiver in the source and the `pending-claim-review` flag. Two self-test cases prove both.
- The brand rules still apply: *formule* after the first *tandpasta*, no commodity words, *je*. The notes list each change.

NL now covers 2,151 of the 2,154 translatable entries (99.86 %). Not translatable are 53 never-translate, 350 legacy legal, 9 retired and 9 empty entries. Three translatable entries stay held:
- **Sietske Hamelink's quote** (C85, homepage and PDP). The landing desk wrote that "the Sietske quote stays as it is" (msg_67b031a3a2dc), because they are her own words: an NL version needs her wording or her approval. The waiver covers claims, not a person's quote. The NL draft is in commit `986c1d9`; FR translated the quote in `3ec7a5e`.
- **The SLS article block `#b035`.** It names four competitors, which is a brand rule, not a claim, and the FR lane holds it too. It waits for Victor or for a compliant EN.

Counts below are current.

## What is here

| File | Content |
|---|---|
| `batch-0{1..8}-*.json` | One file per EN batch: `source_digest` (the EN batch it was translated from), `counts`, `fit_risk` ids, and one entry per EN entry: `{id, resource_type, file_or_handle, key_path, en, en_sha1, nl, status, flags, notes}`. |
| `validate.py` | `python3 docs/localization/nl/validate.py` checks every file against `docs/source-copy/en-source.json`. It checks digests, coverage, `en_sha1`, and Dutch present except on held entries. It checks that each status is the strongest of its flags and that counts and fit lists match. Since R2 it also enforces the hold and gate invariants H1–H8 (unsupported, unless waived and flagged; needs-review, legal, legacy, never-translate, blocked, a reason for every hold, retired), the exact-span checks S1 (addresses) and S2 (`(*)` markers), and since R6 the commodity-word check W1. It exits 0 today. |
| `validate_selftest.py` | Plants one defect per check in a temporary copy and confirms that `validate.py` rejects it (19 cases, among them a new gate added in the source only, a waived claim without its flag and two W1 cases that must pass). It exits 0 today. |
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

   This report first said that only the two trust-row short forms still differed. R2 grouped every identical EN and found 17 groups with different Dutch. 14 are harmonised now, and 3 differ on purpose (see "R2 fixes", F9).
6. **Claims.** A claims review of batches 05–07 judged 541 blocks by hand: 33 approved, 261 needs-review, 113 unsupported, 134 without a claim (`CLAIMS-REVIEW.md`). After R2 the totals are 30 approved, 274 needs-review and 115 unsupported: 6 blocks were added and 9 reclassified. Needs-review blocks are translated faithfully and flagged. Unsupported blocks were held until Victor's waiver of 20 Oct; since then they are translated and flagged in the same way.
7. **Dawn keys.** 64 Dawn keys render on the inventoried pages. All 64 are present in `locales/nl.json`. The five that equal the EN (*Menu*, *Blog*, *Link*, *Filter*, *Filter:*) are correct Dutch. Since R2 the two brand keys (Facebook, Instagram) are held as never-translate; their locale values stay as they are.

## Held entries, and why

- **never-translate (53):** selling-plan IDs, the Subscription Name keys "60-Day Supply" / "Year Supply", INCI lists, practitioners' names, citations, Awake/Asleep labels, brand aria-labels and the two Dawn social keys (R2 F10). These keep their EN value.
- **needs-approved-copy (1):** the SLS article block that names four competitors (R2 F6; `blocked` in the source). The two homepage FAQ placeholders got approved answers on 21 Oct (integration `41ae772`) and are translated.
- **practitioner quote (2):** Sietske Hamelink's quote on both templates stays in her EN words (landing desk, 20 Oct).
- **unsupported-claim (0 since 20 Oct):** the 119 entries held here until then are translated under Victor's waiver and flagged `pending-claim-review` (see the update at the top), except the quote above:
  - four from B1a: homepage benefit card 06 (heading and text) and Sietske Hamelink's quote on both templates;
  - 107 article blocks;
  - 6 product-page blocks, among them the two sleep/wake description lines (R2 F1);
  - 2 content-page blocks.
- **held-legacy (350):** the three pre-2.0 legal pages (coordinator, 19 Oct). Each is replaced by a page that is translated:

| Legacy page (held) | Replaced by (translated, legal-review) |
|---|---|
| `/pages/consumer-rights` | `/pages/new-consumer-rights` |
| `/pages/privacy` | `/pages/privacy-policy` |
| `/pages/terms-and-conditions` | `/pages/terms-and-conditions-1` |

Decided 20 Oct (F5, Victor): each old handle redirects to its replacement, so the legacy set stays held after the translate-everything instruction, because outdated legal text would mislead. Each NL note reads *legacy page, redirects to the 2.0 page (F5, Victor)*, as in FR (`66f0c68`). The redirects themselves are an Admin step (Online Store > Navigation > URL redirects).

- **empty EN (9):** article summaries that contain only an image.

## Counts per batch and status

| Batch | Source entries | Source digest | translated | admin | theme-key | legal-review | pending-claim-review | dawn-nl | held | fit-risk |
|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `batch-02-pdp` | 477 | `87edec28e25f` | 119 | 230 | 34 | 0 | 41 | 15 | 38 | 27 |
| `batch-01-homepage` | 229 | `5286628ff7c8` | 142 | 2 | 31 | 0 | 31 | 2 | 21 | 19 |
| `batch-03-header-footer` | 41 | `d5353b16cc57` | 5 | 11 | 10 | 0 | 1 | 9 | 5 | 4 |
| `batch-04-legal` | 974 | `98fda69496b9` | 0 | 3 | 0 | 621 | 0 | 0 | 350 | 12 |
| `batch-05-products` | 77 | `5ab678a91ffc` | 14 | 38 | 0 | 0 | 25 | 0 | 0 | 0 |
| `batch-06-content-pages` | 22 | `3dee3b56341f` | 0 | 15 | 0 | 0 | 7 | 0 | 0 | 1 |
| `batch-07-collections-blog` | 709 | `9597904c4ef8` | 1 | 312 | 0 | 0 | 386 | 0 | 10 | 0 |
| `batch-08-system` | 46 | `306f141fadf2` | 3 | 7 | 0 | 0 | 0 | 36 | 0 | 0 |
| **All** | **2575** | | **284** | **618** | **75** | **621** | **491** | **62** | **424** | **63** |

A status names the strongest flag; `flags` in each entry lists all of them (an `admin` entry can also be `pending-claim-review` and `fit-risk`).

## Held entries by batch

| Batch | Reason | Entries |
|---|---|---:|
| `batch-01-homepage` | never-translate | 16 |
| `batch-01-homepage` | practitioner quote in her own words (C85, desk 20 Oct) | 1 |
| `batch-01-homepage` | retired (Duo name is the product title) | 1 |
| `batch-01-homepage` | retired (FAQ block `4KMG6C` removed, 21 Oct) | 3 |
| `batch-02-pdp` | never-translate | 32 |
| `batch-02-pdp` | practitioner quote in her own words (C85, desk 20 Oct) | 1 |
| `batch-02-pdp` | retired (Duo name is the product title) | 2 |
| `batch-02-pdp` | retired (step numbers emptied in a disabled section, 21 Oct) | 2 |
| `batch-02-pdp` | retired (sticky-bar setting `kit_free` removed, NV-13, 21 Oct) | 1 |
| `batch-03-header-footer` | never-translate | 3 |
| `batch-03-header-footer` | never-translate; existing Dawn locale value remains unchanged | 2 |
| `batch-04-legal` | legacy page, redirects to the 2.0 page (F5, Victor) | 350 |
| `batch-07-collections-blog` | empty EN | 9 |
| `batch-07-collections-blog` | needs-approved-copy: competitor names prohibited; EN owner must supply compliant source | 1 |

## Fit risks

`Kind`: **slot** is a button, chip, tab, cell, plan card, sticky bar, badge, eyebrow or menu label with a fixed width; **contextual QA** is a page, SEO or policy title or a heading that can wrap, to look at in context rather than an established overflow (R2, review F7). No overflow is measured yet: unpublished NL is not rendered (preview gate).

| Entry | Kind | EN | NL | Why |
|---|---|---|---|---|
| `product.subscription-item:main/loop_subscriptions_WEk4XJ/welcome_kit_title` | slot | Welcome Kit · with first order | Welkomstpakket · bij je eerste bestelling | Glossary NL (binding), 30 → 41 chars. Short fallback if it wraps: 'Welkomstpakket · bij 1e bestelling'. |
| `product.subscription-item:main/loop_subscriptions_WEk4XJ/try_once_text` | slot | Try once | Eenmalig proberen | Approved plan name (Figma NL), 8 → 17 chars; check the buy-box link. |
| `product.subscription-item:main/loop_subscriptions_WEk4XJ/pricing_summary_welcome_kit_title` | slot | Welcome Kit on first order (value [value]) | Welkomstpakket bij eerste bestelling (waarde [value]) | 42 → 53 chars; 'Welkomstpakket' is 3 chars longer than 'Welcome Kit' and cannot shrink. |
| `product.subscription-item:research_behind_system_EkjATL/button_label` | slot | Explore the full evidence base | Ontdek de volledige wetenschappelijke basis | revised in assembly: approved NL from Figma 'Dutch offer 2.0 · NL' (3738:27474); translator had: Ontdek de volledige onderbouwing; Button label, 30 → 43 chars;… |
| `product.subscription-item:featured_product_Eb93Xa/loop_subscriptions_gPKypi/shipping_value_html` | slot | Varies Free | Variabel Gratis | Plan-card shipping value, 11 → 15 chars, like its homepage counterpart (already flagged); kept (R2, review F7) |
| `product.subscription-item:featured_product_Eb93Xa/loop_subscriptions_gPKypi/care_credit_text_1` | slot | 10% / order | 10% / bestelling | 11 → 16 chars; no shorter Dutch word for 'order' that reads well in Flanders. |
| `product.subscription-item:featured_product_Eb93Xa/icon_with_text_endcta/heading_3` | slot | Gift, pause or cancel | Schenken, pauzeren of opzeggen | revised in assembly: approved NL from Figma 'Dutch offer 2.0 · NL' (3738:27474); translator had: Pauzeren of opzeggen; Trust-row chip, 21 → 30 chars; approved … |
| `product.subscription-item:care_comes_back/step_next_order/title` | slot | Your next order | Je volgende bestelling | 15 → 22 chars; 'order' is not neutral Dutch. |
| `liquid:sections/main-product.liquid:943` | slot | Try Once · 1 Duo | Eenmalig proberen · 1 duo | Approved plan name (Figma NL), 16 → 25 chars in the sticky bar. |
| `liquid:sections/main-product.liquid:1030` | slot | Try once | Eenmalig proberen | Approved plan name (Figma NL), 8 → 17 chars on the sticky-bar button. |
| `admin:morning-toothbrush-2-0:title` | slot | Morning Toothbrush 2.0 | Ochtendtandenborstel 2.0 | revised in assembly: same Shopify product title inventoried twice; faithful title (the Figma 'Ultrazachte ochtendborstel' is a buy-box label for a different EN… |
| `admin:evening-toothbrush-2-0:title` | slot | Evening Toothbrush 2.0 | Avondtandenborstel 2.0 | revised in assembly: same Shopify product title inventoried twice; faithful title; Width, not length (R2, review F7): 22 chars in both languages, but 'Avondtan… |
| `admin:whitening-charcoal-dental-floss:title` | slot | Whitening Charcoal Floss | Whitening floss met houtskool | revised in assembly: same Shopify product title inventoried twice (B1a kit item, B2 product page); Figma NL wording; R2 (review F5): pending-claim-review, same… |
| `admin:karmicare-biorhythmic-oral-care-system:custom.treatment_journey_*#04` | slot | First brush | Eerste poetsbeurt | 11 → 17 chars; Dutch has no shorter noun for 'brush' as an event. |
| `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#32` | slot | No artificial colours | Geen kunstmatige kleurstoffen | 21 → 29 chars; 'kleurstoffen' cannot be shortened without changing the meaning. |
| `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#55` | contextual QA | Quality & safety | Kwaliteit & veiligheid | Contextual QA, not a fixed slot (R2, review F7): accordion title that wraps. 16 → 22 chars; no shorter Dutch pair. Accordion title, probably full width. |
| `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#96` | slot | Safe to swallow | Veilig bij inslikken | 15 → 20 chars; same wording as 'Veilig bij inslikken' in the leave-on text. |
| `admin:karmicare-biorhythmic-oral-care-system:custom.comparison_section#13` | slot | One dose fits all | Eén dosis voor iedereen | 17 → 23 chars. |
| `admin:karmicare-biorhythmic-oral-care-system:custom.comparison_section#18` | slot | Weeks to notice | Weken voor je iets merkt | revised in assembly: approved NL from Figma 'Dutch offer 2.0 · NL' (3738:27474); translator had: Merkbaar na weken; Comparison-table cell, 15 → 24 chars; appro… |
| `admin:karmicare-biorhythmic-oral-care-system:custom.comparison_section#23` | slot | Systemic, not oral | Systemisch, niet in de mond | revised in assembly: approved NL from Figma 'Dutch offer 2.0 · NL' (3738:27474); translator had: Systemisch, niet oraal; Comparison-table cell, 18 → 27 chars; … |
| `admin:karmicare-biorhythmic-oral-care-system:custom.comparison_section#29` | slot | Skin only | Alleen de huid | 9 → 14 chars; 'Alleen huid' (11) if the cell is tight. |
| `admin:karmicare-biorhythmic-oral-care-system:custom.comparison_section#34` | slot | Surface renewal only | Alleen oppervlaktevernieuwing | 20 → 29 chars; the Dutch compound has no shorter form. |
| `admin:karmicare-biorhythmic-oral-care-system:custom.compare_table_header_footer#03` | contextual QA | Three ways to begin. | Drie manieren om te beginnen. | Contextual QA, not a fixed slot (R2, review F7): section heading line that wraps. 20 → 29 chars; heading line. |
| `admin:karmicare-biorhythmic-oral-care-system:custom.compare_table|shop.metaobjects.compare_value#11` | slot | Skip, pause or cancel | Overslaan, pauzeren of opzeggen | 21 → 31 chars; the trust-row short form 'Pauzeren of opzeggen' would drop 'skip'. |
| `admin:karmicare-biorhythmic-oral-care-system:custom.compare_table|shop.metaobjects.compare_value#14` | slot | Try Once | Eenmalig proberen | Approved plan name (Figma NL), 8 → 17 chars as a column header. |
| `admin:karmicare-biorhythmic-oral-care-system:custom.compare_table_header_footer#04` | contextual QA | Every subscription earns | Met elk lidmaatschap verdien je | Contextual QA, not a fixed slot (R2, review F7): heading fragment that wraps with #05 and #06. TERM: subscription → lidmaatschap (offer wording). Fragments #04… |
| `admin:karmicare-biorhythmic-oral-care-system:custom.compare_table_header_footer#06` | contextual QA | a return on the care you keep. | een rendement op de zorg die je volhoudt. | Contextual QA, not a fixed slot (R2, review F7): heading fragment that wraps with #04 and #05. 'return' → 'rendement' (echoes Return on Care); 30 → 41 chars. |
| `index:hero_karmicare_XKKLDK/buttons_DpYxth/button_label_2` | slot | WHY TWO FORMULAS? | WAAROM TWEE FORMULES? | 21 vs 17 chars; no shorter natural Dutch for 'why two formulas' |
| `index:stat_strip_karmicare/stat_5/heading` | slot | No rinse | Niet spoelen | 12 vs 8 chars; shortest natural form, matches the approved 'Spugen, niet spoelen' |
| `index:product_benefits_karmicare_bcQ6tp/card_aXhzDi/heading` | slot | Naturally brighter | Natuurlijk stralender | 21 vs 18 chars; 'stralender' is the idiom for teeth; shorter 'Natuurlijk witter' would turn 'brighter' into 'whiter' |
| `index:product_benefits_karmicare_bcQ6tp/card_jN7XcL/heading` | slot | One pump, one dose | Eén pompje, één dosis | 21 vs 18 chars; 'Eén pomp, één dosis' (19) fits if 'pompje' may go |
| `index:trusted_professionals_HAqYth/card_HFdkaD/text` | slot | Holistic Dentist | Holistisch tandarts | 19 vs 16 chars; no shorter Dutch title |
| `index:research_behind_system_EkjATL/button_label` | slot | Explore the full evidence base | Ontdek de volledige wetenschappelijke basis | revised in assembly: approved NL from Figma 'Dutch offer 2.0 · NL' (3738:27474); translator had: Ontdek het volledige bewijs; Button label, 30 → 43 chars; appr… |
| `index:research_behind_system_EkjATL/card_bDxUVT/result_label` | slot | RESULT | RESULTAAT | 9 vs 6 chars; standard term, no shorter Dutch label |
| `index:research_behind_system_EkjATL/card_yMiD9D/result_label` | slot | RESULT | RESULTAAT | 9 vs 6 chars; standard term |
| `index:research_behind_system_EkjATL/card_fmFMFd/result_label` | slot | Result | Resultaat | 9 vs 6 chars; standard term |
| `index:research_behind_system_EkjATL/card_Hi7YUD/result_label` | slot | RESULT | RESULTAAT | 9 vs 6 chars; standard term |
| `index:research_behind_system_EkjATL/card_JeERX6/result_label` | slot | RESULT | RESULTAAT | 9 vs 6 chars; standard term |
| `index:km_faq_accordion_FYcArV/faq_item_7jmEGi/category` | slot | Ingredients & safety | Ingrediënten & veiligheid | 25 vs 20 chars (filter tab); 'Ingrediënten' alone would drop 'safety' (block disabled since 21 Oct) |
| `index:km_faq_accordion_FYcArV/faq_item_AL3DKF/category` | slot | Ingredients & safety | Ingrediënten & veiligheid | 25 vs 20 chars (filter tab); 'Ingrediënten' alone would drop 'safety' (block disabled since 21 Oct) |
| `index:featured_product_3XpDKw/loop_subscriptions_7dde8c/shipping_value_html` | slot | Varies Free | Variabel Gratis | 15 vs 11 chars; 'Wisselt' (7) is shorter but reads less clearly |
| `index:featured_product_3XpDKw/loop_subscriptions_7dde8c/care_credit_text_1` | slot | 10% / order | 10% / bestelling | 16 vs 11 chars; '10% / order' fits exactly (Dutch 'order' is correct but less consumer-friendly) |
| `index:care_comes_back/step_next_order/title` | slot | Your next order | Je volgende bestelling | 22 vs 15 chars; 'Je volgende order' (17) fits if space is tight |
| `liquid:snippets/loop-widget-standard.liquid:123` | slot | One time Purchase | Eenmalige bestelling | 20 vs 17 chars; 'one-time order' per the glossary. If this label shows the Try Once plan, use the approved 'Eenmalig proberen' (17) |
| `liquid:snippets/loop-widget-standard.liquid:140` | slot | each | per stuk | 8 vs 4 chars; Dawn's NL locale uses '/st' if space is tight |
| `liquid:assets/loop-widget.js:2463` | slot | Renews | Verlengd | The word that replaces 'ships' in the plan's option text. Dutch puts it at the end of the line, so the Loop owner should key the whole line: 'Renews every {{ d… |
| `liquid:sections/footer.liquid:679` | slot | Join | Doe mee | 7 vs 4 chars; no four-letter Dutch verb for 'Join' ('Aanmelden' 9) |
| `liquid:sections/footer.liquid:1058` | slot | Consumer Rights | Consumentenrechten | 18 vs 15 chars; standard term |
| `admin:navigation:new-main-menu:links[2].title` | slot | Science | Wetenschap | 10 vs 7 chars; no shorter Dutch word |
| `admin:navigation:company:links[3].title` | slot | Why Karmicare | Waarom Karmicare | 16 vs 13 chars; no shorter form |
| `page.privacy-policy:policy_banner_Pgpxip/eyebrow` | slot | LEGAL | JURIDISCH | Eyebrow: 9 vs 5 chars, no shorter Dutch word; it sits alone above the banner heading. |
| `page.privacy-policy:legal_toc_section_gYznx3/content_section_g6nYeY/title` | contextual QA | 2. Data controller | 2. Verwerkingsverantwoordelijke | Contextual QA, not a fixed slot (R2, review F7): legal section heading that wraps. TERM: data controller → verwerkingsverantwoordelijke (AVG term). 31 vs 18 ch… |
| `page.privacy-policy:legal_toc_section_gYznx3/content_section_EAKJLC/nav_label` | slot | Retention | Bewaartermijn | 13 vs 9 chars; shorter 'Bewaring' is possible but less clear. |
| `page.privacy-policy:legal_toc_section_gYznx3/content_section_qyyKHX/nav_label` | slot | Security | Beveiliging | 11 vs 8 chars; no shorter Dutch word. |
| `page.privacy-policy:legal_toc_section_gYznx3/content_section_qyyKHX/title` | contextual QA | 10. Data security | 10. Gegevensbeveiliging | Contextual QA, not a fixed slot (R2, review F7): legal section heading that wraps. 23 vs 17 chars; 'Beveiliging' alone would drop 'data'. The heading can wrap. |
| `page.privacy-policy:legal_toc_section_gYznx3/content_section_pjNTAq/nav_label` | slot | Changes | Wijzigingen | 11 vs 7 chars; no shorter Dutch word. |
| `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_g6nYeY/nav_label` | slot | Scope | Toepassing | fit-risk: "Scope" (5 chars) has no Dutch legal equivalent of that length; "Toepassing" (10) is the shortest clear form. |
| `admin:policy:privacy-policy:body#b011` | contextual QA | 2. Data controller | 2. Verwerkingsverantwoordelijke | Contextual QA, not a fixed slot (R2, review F7): policy body heading that wraps. 31 vs 18 chars; no shorter correct legal term, the heading may wrap. |
| `admin:policy:privacy-policy:body#b128` | contextual QA | 10. Data security | 10. Gegevensbeveiliging | Contextual QA, not a fixed slot (R2, review F7): policy body heading that wraps. 23 vs 17 chars; 'Beveiliging' alone would drop 'data'. The heading can wrap. |
| `admin:policy:refund-policy:title` | contextual QA | Refund policy | Terugbetalingsbeleid | Contextual QA, not a fixed slot (R2, review F7): policy title; its checkout-footer link wraps. Shopify policy title; 20 vs 13 chars. No shorter correct term: '… |
| `admin:policy:legal-notice:title` | contextual QA | Legal notice | Wettelijke vermeldingen | Contextual QA, not a fixed slot (R2, review F7): policy title; its checkout-footer link wraps. TERM: Legal notice → Wettelijke vermeldingen (usual Belgian titl… |
| `admin:policy:legal-notice:seo.title` | contextual QA | Legal notice – KARMICARE | Wettelijke vermeldingen – KARMICARE | Contextual QA, not a fixed slot (R2, review F7): browser-tab and search-result title. 35 vs 24 chars (page title, not a UI slot); see legal-notice title. |
| `admin:page:why-karmicare:title` | contextual QA | Why Karmicare | Waarom Karmicare | Contextual QA, not a fixed slot (R2, review F7): page title that wraps. 16 vs 13 chars; no shorter form |

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
| Duo PDP | `/products/karmicare-biorhythmic-oral-care-system` | `/nl/products/karmicare-biorhythmic-oral-care-system` | `/fr/products/karmicare-biorhythmic-oral-care-system` | 02 | translated; 1 block held (unsupported claims); 41 pending-claim-review |
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
| complete-hygiene-kit | `/products/complete-hygiene-kit` | `/nl/products/complete-hygiene-kit` | `/fr/products/complete-hygiene-kit` | 05 | translated; 2 pending-claim-review |
| morning-toothbrush | `/products/morning-toothbrush` | `/nl/products/morning-toothbrush` | `/fr/products/morning-toothbrush` | 05 | translated; 1 pending-claim-review |
| evening-toothbrush | `/products/evening-toothbrush` | `/nl/products/evening-toothbrush` | `/fr/products/evening-toothbrush` | 05 | translated; 3 pending-claim-review |
| whitening-charcoal-dental-floss | `/products/whitening-charcoal-dental-floss` | `/nl/products/whitening-charcoal-dental-floss` | `/fr/products/whitening-charcoal-dental-floss` | 05 | translated; 5 pending-claim-review |
| evening-toothbrush-2-0 | `/products/evening-toothbrush-2-0` | `/nl/products/evening-toothbrush-2-0` | `/fr/products/evening-toothbrush-2-0` | 05 | translated; 3 pending-claim-review |
| morning-toothbrush-2-0 | `/products/morning-toothbrush-2-0` | `/nl/products/morning-toothbrush-2-0` | `/fr/products/morning-toothbrush-2-0` | 05 | translated; 1 pending-claim-review |
| asleep-evening-toothpaste-2-0 | `/products/asleep-evening-toothpaste-2-0` | `/nl/products/asleep-evening-toothpaste-2-0` | `/fr/products/asleep-evening-toothpaste-2-0` | 05 | translated; 3 blocks held (unsupported claims); 1 pending-claim-review |
| awake-morning-toothpaste-2-0 | `/products/awake-morning-toothpaste-2-0` | `/nl/products/awake-morning-toothpaste-2-0` | `/fr/products/awake-morning-toothpaste-2-0` | 05 | translated; 3 blocks held (unsupported claims); 1 pending-claim-review |
| why-karmicare | `/pages/why-karmicare` | `/nl/pages/why-karmicare` | `/fr/pages/why-karmicare` | 06 | translated |
| why-use-hydroxyapatite-toothpaste | `/pages/why-use-hydroxyapatite-toothpaste` | `/nl/pages/why-use-hydroxyapatite-toothpaste` | `/fr/pages/why-use-hydroxyapatite-toothpaste` | 06 | translated |
| why-stop-using-fluoride-toothpaste | `/pages/why-stop-using-fluoride-toothpaste` | `/nl/pages/why-stop-using-fluoride-toothpaste` | `/fr/pages/why-stop-using-fluoride-toothpaste` | 06 | translated; 4 pending-claim-review |
| nhap-technology | `/pages/nhap-technology` | `/nl/pages/nhap-technology` | `/fr/pages/nhap-technology` | 06 | translated; 2 blocks held (unsupported claims); 1 pending-claim-review |
| articles | `/pages/articles` | `/nl/pages/articles` | `/fr/pages/articles` | 06 | translated |
| collections-biorhythmic-oral-hygiene-kit | `/collections/biorhythmic-oral-hygiene-kit` | `/nl/collections/biorhythmic-oral-hygiene-kit` | `/fr/collections/biorhythmic-oral-hygiene-kit` | 07 | translated |
| collections-vgbc2025 | `/collections/vgbc2025` | `/nl/collections/vgbc2025` | `/fr/collections/vgbc2025` | 07 | translated |
| collections-karmicare-collection | `/collections/karmicare-collection` | `/nl/collections/karmicare-collection` | `/fr/collections/karmicare-collection` | 07 | translated |
| blogs-news | `/blogs/news` | `/nl/blogs/news` | `/fr/blogs/news` | 07 | translated |
| nano-hydroxyapatite | `/blogs/news/nano-hydroxyapatite` | `/nl/blogs/news/nano-hydroxyapatite` | `/fr/blogs/news/nano-hydroxyapatite` | 07 | translated; 21 blocks held (unsupported claims); 40 pending-claim-review |
| morning-and-night-time-brushing-why-timing-matters | `/blogs/news/morning-and-night-time-brushing-why-timing-matters` | `/nl/blogs/news/morning-and-night-time-brushing-why-timing-matters` | `/fr/blogs/news/morning-and-night-time-brushing-why-timing-matters` | 07 | translated; 3 blocks held (unsupported claims); 10 pending-claim-review |
| benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood | `/blogs/news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood` | `/nl/blogs/news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood` | `/fr/blogs/news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood` | 07 | translated; 28 blocks held (unsupported claims); 32 pending-claim-review |
| nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste | `/blogs/news/nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste` | `/nl/blogs/news/nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste` | `/fr/blogs/news/nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste` | 07 | translated; 13 blocks held (unsupported claims); 29 pending-claim-review |
| how-oral-health-impacts-your-overall-wellness | `/blogs/news/how-oral-health-impacts-your-overall-wellness` | `/nl/blogs/news/how-oral-health-impacts-your-overall-wellness` | `/fr/blogs/news/how-oral-health-impacts-your-overall-wellness` | 07 | translated; 8 blocks held (unsupported claims); 57 pending-claim-review |
| top-natural-whitening-toothpaste-for-a-brighter-smile | `/blogs/news/top-natural-whitening-toothpaste-for-a-brighter-smile` | `/nl/blogs/news/top-natural-whitening-toothpaste-for-a-brighter-smile` | `/fr/blogs/news/top-natural-whitening-toothpaste-for-a-brighter-smile` | 07 | translated; 8 blocks held (unsupported claims); 31 pending-claim-review |
| 5-reasons-you-should-avoid-fluoride-in-toothpaste | `/blogs/news/5-reasons-you-should-avoid-fluoride-in-toothpaste` | `/nl/blogs/news/5-reasons-you-should-avoid-fluoride-in-toothpaste` | `/fr/blogs/news/5-reasons-you-should-avoid-fluoride-in-toothpaste` | 07 | translated; 15 blocks held (unsupported claims); 31 pending-claim-review |
| headaches-and-tooth-pain-understanding-the-connection | `/blogs/news/headaches-and-tooth-pain-understanding-the-connection` | `/nl/blogs/news/headaches-and-tooth-pain-understanding-the-connection` | `/fr/blogs/news/headaches-and-tooth-pain-understanding-the-connection` | 07 | translated; 7 blocks held (unsupported claims); 24 pending-claim-review |
| 3-reasons-why-you-should-look-for-an-sls-free-toothpaste | `/blogs/news/3-reasons-why-you-should-look-for-an-sls-free-toothpaste` | `/nl/blogs/news/3-reasons-why-you-should-look-for-an-sls-free-toothpaste` | `/fr/blogs/news/3-reasons-why-you-should-look-for-an-sls-free-toothpaste` | 07 | translated; 4 blocks held (unsupported claims); 25 pending-claim-review |
| search | `/search` | `/nl/search` | `/fr/search` | 08 | translated |
| 404 | `/pages/any-missing-page` | `/nl/pages/any-missing-page` | `/fr/pages/any-missing-page` | 08 | translated |
| collections-list | `/collections` | `/nl/collections` | `/fr/collections` | 08 | translated |
| collections-all | `/collections/all` | `/nl/collections/all` | `/fr/collections/all` | 08 | translated |
| cart | `/cart` | `/nl/cart` | `/fr/cart` | 08 | translated |
| customers/*.json | `/account/login` | `/nl/account/login` | `/fr/account/login` | 08 | not theme-rendered: 302 to Shopify's hosted customer accounts: the theme templates do not render (new customer accounts) |
| password.json | `/password` | `/nl/password` | `/fr/password` | 08 | not theme-rendered: 302 to the homepage: the store is not password-protected; the template renders only when a password is set |
| gift_card.liquid | `/gift_cards/<token>` | `/nl/gift_cards/<token>` | `/fr/gift_cards/<token>` | 08 | not theme-rendered: reachable only with a gift-card link; Dawn locale keys (gift_cards.*) only |

## R2 fixes

Task `task_7dc91e6a67f1`, Orca run `run_32dd5602b983`, 19–20 Oct 2026. The review `docs/runtime-review/B2-NL-ASTRA.md` (Codex GPT-6 Astra, xhigh, verdict FAIL) gave ten findings, F1–F10. All ten are fixed with the reviewer's exact corrections where it gave them. I wrote no new claims and no new copy.

| Preflight | Result |
|---|---|
| `orca status --json` | runtime `ready`, `reachable: true`, connection `connected` |
| `git status --short` / branch | clean tree on `karmicare/soft-launch-source-copy`, HEAD `2194ef3` |
| Model / permission mode | Claude Opus 5.5 (`claude-opus-5-5`) in Claude Code, auto mode, every Bash command sandboxed |
| Shared workspace | The B4 localization worker commits here too. I committed only `docs/source-copy/**` and `docs/localization/nl/**`, by explicit pathspec. |

| Finding | Commit | Result |
|---|---|---|
| F1 sleep/wake claims | `3ef6ba8` + `8ed5ed1` (see the note below) | Both 2.0 description lines are `claim_status: unsupported` in the source and held in NL with the reviewer's note. No milder wording. |
| F2 missing nHAp heading | `3ef6ba8` | New entry `admin:page:nhap-technology:body_html#b000` before `#b001`, with the article title's Dutch, pending-claim-review. Batch 06: 22 entries, digest `3dee3b56341f`. |
| F3 legal proposition | `4cde4e5` | Heading 4.1 is "Vermoeden van conformiteit gedurende twee jaar" in the template and in refund `#b065`. Both keep legal-review, and the EN entries ask the legal owner to approve or correct the heading. |
| F4 claim strength | `2714912` | The reviewer's exact NL for SLS `#b056` and `#b028` and for nano-hydroxyapatite `#b036` ("organisch" restored). |
| F5 classifications | `8ed5ed1` | The five named gates, plus the copies sweep: the floss wording in the kit body and SEO text, register claim C100 for its 4 Duo PDP copies, and "Why You Need It" in 4 titles and alts. 16 entries are now pending-claim-review. |
| F6 brand restrictions | `c664970` | The SLS competitor block is `blocked` in the source and held in NL. The reviewer's replacements cover 10 entries, among them the two morning-brush SEO texts that repeat the body. The sweep reworded 13 more promotional entries: FAQ row 4 and 12 blog blocks. |
| F7 fit metadata | `636ed50` | `fit-risk` on the 6 named strings (63 flags). The two brush titles get a width reason. 12 title and heading flags are marked contextual QA (the `Kind` column below). |
| F8 addresses | `23ca298` | 33 address spans in 29 entries are restored to the EN form, beyond the 4 named. Legal labels stay translated. |
| F9 harmonisation | `a461102`, `8e1998f` | 14 of 17 groups harmonised, including the reviewer's clock description and model-form sentence. The model form's "unopened contract" sentence is also in one form now. 3 groups differ on purpose (table below). |
| F10 never-translate | `41d513b` | Facebook and Instagram are held: 53 never-translate entries, all held. |
| Validation | `ddeba5d`, `7a91f30` | Every claim-bearing source entry carries `claim_status`: 84 more entries in batches 01–03, derived from their claim ids, with digests unchanged. `validate.py` enforces H1–H7, S1 and S2, and `validate_selftest.py` proves each check. |
| FR propagation | `2eacf9e` | `docs/source-copy/CHANGES-R2.md` lists every source-level change, generated by comparing `en-source.json` with `2194ef3`. |

**Commit history note (F1).** This workspace shares one git index with the B4 worker.
- I staged the five F1 files. Before my pathspec commit ran, B4's commit `218fe9d` took them in. B4 then rewrote that commit as `e850bc4`, which holds the hero and stat-strip changes only.
- The F1 changes to `en-source.json`, `CLAIMS-REVIEW.md` and `INVENTORY.md` went into my F2 commit `3ef6ba8`. The two batch-05 files followed in the F5 commit `8ed5ed1`.
- So at `3ef6ba8`, `4cde4e5` and `2714912` the batch-05 copy lags `en-source.json` by the two F1 metadata fields, and `digest.py` would flag those three commits. HEAD passes every check.
- After that, nothing of mine sat in the index: tracked files were committed by pathspec, and new files were added and committed in one command. History was not rewritten.

### Sweeps beyond the named entries

- **F2: blocks dropped because they equal an article title.** Every live capture was re-run through the extractor. Only the nHAp page lost a block; on the article pages the matching text is the article's own title, which is inventoried.
- **F5: the same claim wording in other fields.** Three checks ran:
  - the B1a claim wordings against batches 04–08;
  - the batch 05–07 claim excerpts against every entry;
  - unclassified entries whose whole text sits inside a gated block.

  The 10 copies found are gated. The remaining hits were reviewed and left alone:
  - plain questions and kit or intro sentences that only sit inside a gated multi-sentence SEO description;
  - the fluoride-free composition sentence;
  - "The best way to use nano HAp is in a specially formulated toothpaste";
  - "Fluoride is commonly added to toothpaste to prevent tooth decay", which describes fluoride and is not a Karmicare claim.
- **F6: commodity words** (product, use, buy, tube and their Dutch forms) in non-legal, non-Dawn NL. These stay, listed for the copy owner:
  - the two treatment-journey disclaimers with *gebruik*: approved Figma NL that conflicts with the general brand rule;
  - *EU-portaal voor cosmetische producten*: the CPNP's official name;
  - the footer compliance line "is een Belgisch product": it mirrors the EN regulatory statement;
  - *Gebruiksvoorwaarden*: a legal document title.

  Also: the evening brushes keep "Awake/Asleep-tandpasta", their only and first mention. *Productief* and *productiviteit* are not commodity words. (R6 replaced the blog part of this sweep: see "R6 fixes".)
- **F8: addresses.** The validator's S1 check finds 33 address spans in translated entries, all as in the EN. A city alone ("KARMICA BV, Brugge" in a product-FAQ chip), the court ("Ondernemingsrechtbank Gent, afdeling Brugge"), "Brussel I bis" and the country lists stay translated.
- **F9: exceptions kept on purpose.**

| EN | Entries | Why they differ |
|---|---|---|
| 60-day money-back guarantee | three trust rows *60 dagen geld terug*; sticky bar `main-product.liquid:1055` *60 dagen geld-terug-garantie* | Both are approved Figma NL: the trust rows use Figma's short form. |
| Gift, pause or cancel | buy-box trust row *Pauzeren of opzeggen*; end CTA *Schenken, pauzeren of opzeggen* | The trust row uses Figma's approved short form, which drops "Gift" (question 9). |
| Email | Dawn `newsletter.label` *E‑mail* (non-breaking hyphen); footer `footer.liquid:660` *E-mail* | Dawn's own value, not re-translated. |

The F9 sweep compared whole entries, plus the model form's sentences. Other legal sentences that repeat inside differently scoped blocks (a template section next to its policy paragraph) were not compared sentence by sentence.

### Verification

| Check | Result |
|---|---|
| `python3 docs/source-copy/digest.py` | exit 0, 8 batches (batch 06: 22 entries, `3dee3b56341f67b113dcd59eb85d3a2e3f21d628`) |
| `python3 docs/source-copy/digest_selftest.py` | exit 0: the control passes and the three defects fail |
| `python3 docs/localization/nl/validate.py` | exit 0. Entries under each gate: H1 119, H2 346, H3 956, H4 350, H5 53, H6 3, H7 534. Checked: 33 addresses (S1) and 28 `(*)` markers (S2). |
| `python3 docs/localization/nl/validate_selftest.py` | exit 0: the control passes; H1–H7, S1, S2, a new source-only gate, a weak status, a stale EN and edited counts each fail on their own check |
| `shopify theme check` | not run: R2 commits touch no theme files (AGENTS.md §5 covers theme files) |
| Live pages | not reopened. F2 rests on the 20:15 capture (`h1.kc_article_single-title` inside `.rte`), which the reviewer's live check of 19 Oct confirms. Rendered NL fit stays pending the preview gate. |

### Handoffs from R2

- **FR worker:** follow `docs/source-copy/CHANGES-R2.md`. Batch 06 has a new entry and digest. The SLS competitor block is newly held, and 16 entries are newly pending-claim-review. The NL payload rules from R2 (section 6 there) apply to FR too.
- **Localization worker (B4):** rebuild anything derived from the NL payloads after `8e1998f`. Since `2194ef3`, 1 entry was added, 76 NL texts changed and 21 statuses changed. No `theme-key` text changed. The two Dawn social keys are now held, and their `locales/nl.json` values stay as they are.
- **EN owner:**
  - the morning-brush "2 to 4 applications" dose;
  - "organic biomaterial";
  - compliant copy for the SLS competitor block;
  - "Bestselling";
  - the "Why You Need It" headings;
  - the two sleep/wake description lines.
- **Legal owner:** approve or correct the EN heading 4.1, then both languages are regenerated. Also question 8.
- **Clinical Research:** the pending-claim-review entries (375 since R6), the new C100 and the R2 reclassifications.

## R6 fixes

Task `task_e2db4c0f9717`, Orca run `run_32dd5602b983`, 20 Oct 2026. The re-review `docs/runtime-review/B2-NL-R6-ASTRA.md` (Codex GPT-6 Astra, xhigh, verdict PASS WITH FIXES) found 8 of the 10 R2 findings fixed and F5/F6 partly fixed, and raised R6-01 to R6-03. All three are fixed, with the reviewer's exact corrections; I wrote no new claims and no new copy.

| Preflight | Result |
|---|---|
| `orca status --json` | runtime `ready`, `reachable: true`, connection `connected` |
| `git status --short` / branch | clean tree on `karmicare/soft-launch-source-copy`, HEAD `2aa84e4`. B4 has finished, so I am the only writer here. |
| Model / permission mode | Claude Opus 5.5 (`claude-opus-5-5`) in Claude Code, auto mode, every Bash command sandboxed |

| Item | Commit | Result |
|---|---|---|
| R6-03 aggregate count | `30c9062` | CLAIMS-REVIEW.md and CHANGES-R2.md carry the reviewer's text: after R2, 30 / 274 / 115, twelve blocks newly entered and three reclassified. "Now" reads "after R2", because R6-01 changes the totals again. |
| R6-01 claim gate | `5642a49` | Wellness `#b081` is needs-review with the reviewer's basis. Its NL is pending-claim-review, with *ochtendformule* / *avondformule*. The semantic recheck of the same article gates 28 more blocks (below), and the copy check found top-whitening `#b051` ("Bestselling", the same claim as headaches `#b019`). That makes 30 entries; CLAIMS-REVIEW batches 05–07 now hold 30 / 304 / 115. Metadata only, digests unchanged. |
| R6-02 category words | `b8eb917` | The reviewer's 8 compounds and SLS `#b057`, exact. Then a full pass over the nine NL articles: 120 later uses of *tandpasta* became *formule(s)*, *mondverzorging* or *verzorging*, in 111 entries in all. |
| Validator W1 | `ed753b8` | `validate.py` rejects commodity words, compounds included, in non-legal copy, with 5 listed exceptions. The self-test has 17 cases. |
| FR propagation | `a48bcbd` | "R6 additions" in `docs/source-copy/CHANGES-R2.md`: the 30 reclassified entries, generated by comparing `en-source.json` with `2aa84e4`, plus the payload rules for FR. |
| Registration plan | `6c9db1f` | `plan-nl.json`, `plan-fr.json` and `DRY-RUN.md` rebuilt offline. |
| Report | this commit | This section. The blanket blog exemption is removed from "Sweeps beyond the named entries". |

**R6-01: the semantic recheck of `how-oral-health-impacts-your-overall-wellness`.** I read every block of the article. Blocks that make a health, wellness, efficacy, safety or study claim, and had no gate, are now needs-review, each with a basis that names its gated sibling:
- **The opening fact:** `#b007`, and the SEO description that repeats it.
- **Toothpaste framed as a wellness or health instrument:** `#b015`, `#b016`, `#b055`, `#b057`, `#b062`, `#b067`, `#b076`, `#b082`, `#b094` and `#b095`.
- **List items that continue gated sentences:** `#b020`–`#b022` under `#b019`, and `#b085`, `#b087`, `#b090`, `#b091` and `#b092` under `#b083`.
- **Attributed study results and numbers:** `#b047`, `#b049` and the `#b051` pull quote.
- **Harmful-chemicals and efficacy wording:** `#b066`, `#b068` and `#b073`.
- **Two links of the disease chain that the B2 pass had judged "none":** `#b024` (inflammation to gum disease) and `#b038` (plaque to heart attack and stroke). Their neighbours `#b025`, `#b036` and `#b037` are gated.

These stay ungated: the questions, headings and calls to action, and general oral-health statements with no product, study or number (`#b010`, `#b011`, `#b013`, `#b043`, `#b045`, `#b050`, `#b053`, `#b054`, `#b070`, `#b079`). *Limit:* the other eight articles were checked only for copies of claims (that check found `#b051`), not re-read block by block in R6. They keep their R2 classification, and question 1 (do not publish the legacy articles) still stands.

**R6-02: the category-word rule as applied.** The rule is from `tone-of-voice.md`: "toothpaste" at first-contact clarity moments only, "a door, not a carpet", and never negated.
- **Kept:** per article, the title, the SEO title and description, the image alt, the opening self-reflection questions (the FAQ-question case) and one first prose mention. These are 29 entries.
- **Replaced:** every later use, by *formule(s)*, or *mondverzorging* where the EN means the category ("fluoride in toothpaste").
- **Unchanged:** claims, hedges, numbers, links and gates.
- **Outside the blog,** *tandpasta* appears only in titles, SEO texts, alts, the product names in the Duo FAQ, the homepage FAQ question, the Duo description's opening line, the content-page headlines and the brush bodies' first mention. All of these are first contact or names.
- **Still listed for the copy owner:** the official and approved exceptions (CPNP portal name, *Gebruiksvoorwaarden*, the footer compliance line, the two approved Figma disclaimers).

**W1, and why "tandpasta" is not in it.**
- **What W1 checks:** it flags product, tube, *gebruik* and buy stems anywhere in a word, in translated copy that is neither legal text nor a Dawn key, with tags and link URLs left out.
- **Not matched, by design:** *productie*, *productief*, *productiviteit*, *verkoop* and *YouTube*.
- **Exceptions:** the 5 listed in `WORD_EXCEPTIONS` are each used today.
- **Evidence:** run on the payloads before R6 (`2aa84e4`), W1 flags exactly the reviewer's 8 compounds. On HEAD it passes all 1,354 ordinary-copy entries.
- **Why "tandpasta" is not checked:** the word is allowed at first contact, which depends on context a pattern cannot see. The pass above is the check, and the scan in this report lists what remains.

### Verification

| Check | Result |
|---|---|
| `python3 docs/source-copy/digest.py` | exit 0, 8 batches, every digest unchanged by R6 |
| `python3 docs/source-copy/digest_selftest.py` | exit 0 |
| `python3 docs/localization/nl/validate.py` | exit 0. Entries under each gate: H1 119, H2 376 (346 + 30), H3 956, H4 350, H5 53, H6 3, H7 534. Checked: S1 33 addresses, S2 28 `(*)` markers, W1 1,354 entries. |
| `python3 docs/localization/nl/validate_selftest.py` | exit 0, 17 cases: the control and the two W1 no-false-positive cases (legal text, a link URL) pass; the 14 defects each fail on their own check |
| `python3 -I docs/localization/registration/build_payloads.py --fr-dir <export>` | NL: 1,827 items, 522 first wave (unchanged: the blog is a later wave), pending-claim-review hold 343 → 373. FR: 1,822 items, 520 first wave. |
| `python3 -I docs/localization/theme_keys.py check --fr-dir <export>` | ok for all 64 keys. `write` was not run; `locales/` and theme files are untouched. |

The FR input for both runs is `karmicare/soft-launch-fr` at `841e05b` (FR's R2 merge). It was exported with `git archive` to my scratch folder and not merged; B4 had used `c7aed28`. The FR first-wave change (529 → 520) comes from FR's own R2 holds, not from this task.

### Status after R6, and handoffs

- **NL totals:** 375 pending-claim-review, 621 legal-review, 534 held, 63 fit-risk (the table above).
- **Readiness:** R6-01, R6-02 and R6-03 are closed on this branch, and the reviewer's gating condition (fix, update FR propagation, rerun the checks) is met. A re-review, or the orchestrator, confirms before Victor's registration gate. The existing holds and the legal and claim gates still apply.
- **FR worker:** "R6 additions" in `CHANGES-R2.md`: 30 entries newly pending-claim-review, and the compound and first-contact rule for its own blog bodies.
- **Clinical Research:** 30 more blog blocks to sign off, all in batch 07, which registers after the first wave.

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
8. **Address forms in NL (and FR) legal text** (R2 F8).
   - Today the payload keeps every address exactly as in the EN, as the brief asks: "Vizierstraat 28, 8000 Bruges, Belgium", "Boulevard du Roi Albert II 8, box 1, 1000 Brussels".
   - The alternative is the official local-language forms ("8000 Brugge, België", "Koning Albert II-laan 8, bus 1, 1000 Brussel"), which are what the Belgian registers use.
   - *Recommendation*: allow the official local forms in NL and FR, because a Dutch legal page that says "Bruges, Belgium" reads as unedited. Until you decide, the EN form stays. Switching back is one mapping of five strings, already scripted for R2.
9. **"Gift, pause or cancel" in the buy-box trust row.** Figma's approved short form *Pauzeren of opzeggen* drops "Gift"; the end CTA says *Schenken, pauzeren of opzeggen*. *Recommendation*: check the trust row at the preview. If the full form fits, use it everywhere.
10. **Brand-rule exceptions to confirm** (R2 F6):
    - the treatment-journey disclaimer *bij langdurig gebruik* (approved Figma NL);
    - the footer compliance line "is een Belgisch product".

    *Recommendation*: keep the CPNP portal name and legal titles as they are. Let the copy owner reword the two lines above in EN and Figma first, then NL follows.

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
- **EN wording to correct at the source:**
  - "Two-year presumption of conformity": the law presumes the lack of conformity existed at delivery. Since R2 the NL translates the heading as written; please approve or correct the EN, and both languages follow.
  - "an eligible, unopened contract": rendered as a contract for unopened goods, in one form in all four texts.
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
| Claim sign-off of 491 `pending-claim-review` entries (117 of them under Victor's translation waiver) | Victor / Clinical Research |
| Register `admin` entries, add `theme-key` strings to `locales/nl.json`, store the sticky-bar and footer schema defaults; rebuild anything derived from the payloads after R2 | localization worker |
| Rendered check of every `/nl/` URL below, including the 63 fit-risk strings | preview gate / localization check |
| FR follows `docs/source-copy/CHANGES-R2.md` | FR worker |
| EN corrections listed under "Handoffs from R2" | EN owner, legal owner |


## Translator notes for the reviewer

The 117 entries translated under Victor's waiver (20 Oct) are not repeated in this table. Their notes, in the payload, open with the waiver sentence, followed by the earlier hold reason and any wording change made for the brand rules.

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
| `product.subscription-item:chronobiology_clock_karmicare/description` | 'hij' = je mond (title above), as the EN 'it'.; R2 (review F9): harmonised with index:chronobiology_clock_karmicare/description, the homepage's clearer 'je mond' (review F9) |
| `product.subscription-item:chronobiology_clock_karmicare/night_text` | revised in assembly: approved NL from Figma 'Dutch offer 2.0 · NL' (3738:27474); translator had: Melatonine stijgt en speeksel komt nog maar mondjesmaat. Wat om 22:00 op je glazuur zit, zit er om 07:00 nog. |
| `product.subscription-item:chronobiology_clock_karmicare/hint_label` | revised in assembly: approved NL from Figma 'Dutch offer 2.0 · NL' (3738:27474); translator had: SLEEP AAN DE RING · ONTDEK 24 UUR |
| `product.subscription-item:chronobiology_clock_karmicare/footer_link_text` | As the approved Figma NL link 'Lees het onderzoek'. |
| `product.subscription-item:trusted_professionals_HAqYth/bottom_text` | 'prevented' → 'voorkomt', literal as the rules require; the glossary notes the JEP/DETIC objection to 'voorkomt', so the claims reviewer must decide (it is said of an outcome, not of Karmicare).; R2 (review F9): harmoni… |
| `product.subscription-item:trusted_professionals_HAqYth/card_8dRing/hover_text` | Practitioner quote: if she gave it in Dutch, use her original words instead of this translation. |
| `product.subscription-item:how_it_works_steps_aAgVmF/bottom_text` | First sentence as in the NL usage text (products.md). |
| `product.subscription-item:how_it_works_steps_aAgVmF/step_EBicgt/title` | Approved how-to step 3 (Figma NL). Block disabled, not rendered. |
| `product.subscription-item:how_it_works_steps_aAgVmF/step_EBicgt/description` | revised in assembly: approved NL from Figma 'Dutch offer 2.0 · NL' (3738:27474); translator had: Spuug het overschot uit. Spoel daarna niet na. |
| `product.subscription-item:research_behind_system_EkjATL/bottom_text` | R2 (review F9): harmonised with index:research_behind_system_EkjATL/bottom_text, the homepage form ('de toets doorstaat' for 'hold up') |
| `product.subscription-item:research_behind_system_EkjATL/button_label` | revised in assembly: approved NL from Figma 'Dutch offer 2.0 · NL' (3738:27474); translator had: Ontdek de volledige onderbouwing; Button label, 30 → 43 chars; approved Figma NL (3738:27474), kept; visual QA decides whe… |
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
| `product.subscription-item:featured_product_Eb93Xa/loop_subscriptions_gPKypi/shipping_value_html` | Plan-card shipping value, 11 → 15 chars, like its homepage counterpart (already flagged); kept (R2, review F7) |
| `product.subscription-item:featured_product_Eb93Xa/loop_subscriptions_gPKypi/care_credit_text_1` | 11 → 16 chars; no shorter Dutch word for 'order' that reads well in Flanders. |
| `product.subscription-item:featured_product_Eb93Xa/loop_subscriptions_gPKypi/care_credit_text_2` | 'purchase' → 'bestelling' (no 'aankoop/koop', rule 26). |
| `product.subscription-item:featured_product_Eb93Xa/icon_with_text_endcta/heading_1` | Approved trust-row short form (Figma NL). |
| `product.subscription-item:featured_product_Eb93Xa/icon_with_text_endcta/heading_2` | Approved trust-row form (Figma NL), checked there for fit. |
| `product.subscription-item:featured_product_Eb93Xa/icon_with_text_endcta/heading_3` | revised in assembly: approved NL from Figma 'Dutch offer 2.0 · NL' (3738:27474); translator had: Pauzeren of opzeggen; Trust-row chip, 21 → 30 chars; approved Figma NL (3738:27474), kept; visual QA decides whether the s… |
| `product.subscription-item:care_comes_back/intro` | R2 (review F9): harmonised with index:care_comes_back/intro, the homepage form ('gaandeweg' for 'as you go') |
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
| `admin:karmicare-biorhythmic-oral-care-system:media.69271648010621.alt` | R2 (review F5): pending-claim-review, same claim wording as a gated field |
| `admin:karmicare-biorhythmic-oral-care-system:media.69840178020733.alt` | Reordered morning before evening (brand rule Awake before Asleep); the EN has evening first (handoff). |
| `admin:karmicare-biorhythmic-oral-care-system:media.69840177987965.alt` | 'How to use … use 1 pump' → 'Zo poets je … neem 1 pompje' (no 'gebruik', rule 26). |
| `admin:karmicare-biorhythmic-oral-care-system:media.69884688236925.alt` | R2 (review F5): pending-claim-review, same claim wording as a gated field |
| `admin:morning-toothbrush-2-0:title` | revised in assembly: same Shopify product title inventoried twice; faithful title (the Figma 'Ultrazachte ochtendborstel' is a buy-box label for a different EN); Width (R2, review F7): 22 → 24 chars, and 'Ochtendtandenb… |
| `admin:evening-toothbrush-2-0:title` | revised in assembly: same Shopify product title inventoried twice; faithful title; Width, not length (R2, review F7): 22 chars in both languages, but 'Avondtandenborstel' is one 18-letter word with no break point, where… |
| `admin:whitening-charcoal-dental-floss:title` | revised in assembly: same Shopify product title inventoried twice (B1a kit item, B2 product page); Figma NL wording; R2 (review F5): pending-claim-review, same claim wording as a gated field |
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
| `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#55` | Contextual QA, not a fixed slot (R2, review F7): accordion title that wraps. 16 → 22 chars; no shorter Dutch pair. Accordion title, probably full width. |
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
| `admin:karmicare-biorhythmic-oral-care-system:custom.comparison_section#18` | revised in assembly: approved NL from Figma 'Dutch offer 2.0 · NL' (3738:27474); translator had: Merkbaar na weken; Comparison-table cell, 15 → 24 chars; approved Figma NL (3738:27474), kept; visual QA decides whether t… |
| `admin:karmicare-biorhythmic-oral-care-system:custom.comparison_section#21` | revised in assembly: approved NL from Figma 'Dutch offer 2.0 · NL' (3738:27474); translator had: Mond-darm-hersenen, dieper dan glazuur |
| `admin:karmicare-biorhythmic-oral-care-system:custom.comparison_section#23` | revised in assembly: approved NL from Figma 'Dutch offer 2.0 · NL' (3738:27474); translator had: Systemisch, niet oraal; Comparison-table cell, 18 → 27 chars; approved Figma NL (3738:27474), kept; visual QA decides whet… |
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
| `admin:karmicare-biorhythmic-oral-care-system:custom.compare_table_header_footer#03` | Contextual QA, not a fixed slot (R2, review F7): section heading line that wraps. 20 → 29 chars; heading line. |
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
| `admin:karmicare-biorhythmic-oral-care-system:custom.compare_table_header_footer#04` | Contextual QA, not a fixed slot (R2, review F7): heading fragment that wraps with #05 and #06. TERM: subscription → lidmaatschap (offer wording). Fragments #04–#06 join: 'Met elk lidmaatschap verdien je Care Credit: een… |
| `admin:karmicare-biorhythmic-oral-care-system:custom.compare_table_header_footer#06` | Contextual QA, not a fixed slot (R2, review F7): heading fragment that wraps with #04 and #05. 'return' → 'rendement' (echoes Return on Care); 30 → 41 chars. |
| `admin:karmicare-biorhythmic-oral-care-system:shop.metaobjects.compare_value:year.cost_per_brushing` | Wrong in the EN too: the Year is €0,49 per poetsbeurt (admin fix, handoff). Translated as is. |
| `admin:karmicare-biorhythmic-oral-care-system:custom.compare_table:welcome_kit_row.products` | Glossary (Figma NL) brush names, same as the product titles.; R2 (review F5): pending-claim-review, same claim wording as a gated field |
| `index:hero_karmicare_XKKLDK/buttons_DpYxth/button_label_2` | 21 vs 17 chars; no shorter natural Dutch for 'why two formulas' |
| `index:stat_strip_karmicare/tagline` | 'health professionals' → 'zorgprofessionals'; kPNI practitioners → kPNI-therapeuten (glossary); claim C80 pending; EN updated 21 Oct (41ae772) |
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
| `index:trusted_professionals_HAqYth/card_8dRing/hover_text` | Practitioner quote: if she gave it in Dutch originally, use her own wording instead of this back-translation; R2 (review F9): harmonised with product.subscription-item:trusted_professionals_HAqYth/card_8dRing/hover_text… |
| `index:trusted_professionals_HAqYth/card_HFdkaD/text` | 19 vs 16 chars; no shorter Dutch title |
| `index:research_behind_system_EkjATL/button_label` | revised in assembly: approved NL from Figma 'Dutch offer 2.0 · NL' (3738:27474); translator had: Ontdek het volledige bewijs; Button label, 30 → 43 chars; approved Figma NL (3738:27474), kept; visual QA decides whether … |
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
| `index:km_faq_accordion_FYcArV/faq_item_kLMHax/question` | as the PDP line 'Eén duo gaat 64 dagen mee'; EN updated 21 Oct (41ae772) |
| `index:km_faq_accordion_FYcArV/faq_item_kLMHax/answer` | one pump → één pompje (0,45 ml) (glossary); supply claim C07 (approved); EN updated 21 Oct (41ae772) |
| `index:km_faq_accordion_FYcArV/faq_item_7jmEGi/category` | 25 vs 20 chars (filter tab); 'Ingrediënten' alone would drop 'safety'; EN updated 21 Oct (41ae772) |
| `index:km_faq_accordion_FYcArV/faq_item_7jmEGi/question` | 'toothpaste' at first contact (an opening question) → 'tandpasta', as the EN; EN updated 21 Oct (41ae772) |
| `index:km_faq_accordion_FYcArV/faq_item_7jmEGi/answer` | claim C101 pending (mechanism: nHAp and fluoride compete for the enamel surface); EN updated 21 Oct (41ae772) |
| `index:km_faq_accordion_FYcArV/faq_item_AL3DKF/category` | 25 vs 20 chars (filter tab); 'Ingrediënten' alone would drop 'safety'; EN updated 21 Oct (41ae772) |
| `index:km_faq_accordion_FYcArV/faq_item_AL3DKF/answer` | claim C102 pending (comparison: fluoride's benefits against its drawbacks); EN updated 21 Oct (41ae772) |
| `index:km_faq_accordion_FYcArV/faq_item_qUxYCn/answer` | same NL as the guarantee line in the terms, consumer rights and refund policy (legal-review there): keep them in step; EN updated 21 Oct (41ae772) |
| `index:featured_product_3XpDKw/loop_subscriptions_7dde8c/pricing_summary_care_credit_title` | EN plural 'Care Credits'; the program name stays singular |
| `index:featured_product_3XpDKw/loop_subscriptions_7dde8c/shipping_value_html` | 15 vs 11 chars; 'Wisselt' (7) is shorter but reads less clearly |
| `index:featured_product_3XpDKw/loop_subscriptions_7dde8c/care_credit_text_1` | 16 vs 11 chars; '10% / order' fits exactly (Dutch 'order' is correct but less consumer-friendly) |
| `index:featured_product_3XpDKw/loop_subscriptions_7dde8c/care_credit_text_2` | 'purchase' → 'bestelling' (avoids aankoop/kopen) |
| `index:featured_product_3XpDKw/icon_with_text_wUdX3G/heading_1` | Approved Figma NL short form |
| `index:featured_product_3XpDKw/icon_with_text_wUdX3G/heading_3` | 17 vs 13 chars, but this is the approved Figma NL short form, checked in the Figma trust row |
| `index:care_comes_back/terms_link_label` | clauses → artikelen (art.); align with the term the legal chunk uses for the Terms |
| `index:care_comes_back/step_ritual/text` | 'the Year' → 'het Karmicare-jaar' here: '20% van het jaar' would read as '20% of the year' |
| `index:care_comes_back/step_checkup/text` | R2 (review F9): harmonised with product.subscription-item:care_comes_back/step_checkup/text, the PDP form, which follows the TERM 'On the Year' → 'Met het Karmicare-jaar' |
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
| `footer-group:footer/copyright_text` | Compliance line: 'product' kept as in the EN (regulatory statement). EN address lacks the city (8000 Brugge); kept as EN; R2 (review F8): addresses exactly as in the EN (brief); official Dutch address forms only if Vict… |
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
| `page.consumer-rights:legal_toc_section_gYznx3/content_section_FcEDdA/content` | Heading 4.1 translated as the EN reads, 'Vermoeden van conformiteit' (R2, review F3): the law presumes that the lack of conformity existed at delivery, so the legal owner should approve or correct the EN heading; NL fol… |
| `page.consumer-rights:legal_toc_section_gYznx3/content_section_xKcNPj/content` | TERMs: delivery → levering; shipping → verzending / verzendkosten; working days → werkdagen; calendar days → kalenderdagen; checkout → afrekenen. 'additional reasonable period' → 'aanvullende redelijke termijn' (Art. VI… |
| `page.consumer-rights:legal_toc_section_gYznx3/content_section_rnPj6g/content` | TERMs: cancel (membership) → opzeggen; cancel (deliveries) → annuleren; customer portal → klantenportaal; member price → ledenprijs (approved glossary sentence reused in 'Prijsbescherming'); Terms and Conditions → algem… |
| `page.consumer-rights:legal_toc_section_gYznx3/content_section_EAKJLC/content` | 'was' price → “van”-prijs (as in 'van €X voor €Y'). 'kortingen' here means price reductions, not Care Credit. Lawyer: check the reference 'Art. VI.19/1 WER'; to my knowledge the Omnibus reference-price rule sits in Art.… |
| `page.consumer-rights:legal_toc_section_gYznx3/content_section_dGmgBJ/content` | TERMs: Consumer Mediation Service → Consumentenombudsdienst (NL name leads, FR and EN names kept in brackets); European Consumer Centre → Europees Centrum voor de Consument (its official Belgian Dutch name); out-of-cour… |
| `page.consumer-rights:legal_toc_section_gYznx3/content_section_CDtWCV/title` | jurisdiction → bevoegde rechter (standard Belgian heading). |
| `page.consumer-rights:legal_toc_section_gYznx3/content_section_at3pLy/title` | Official Dutch title of the statutory model form. |
| `page.consumer-rights:legal_toc_section_gYznx3/content_section_at3pLy/content` | Form wording follows the official Dutch model form (WER annex / Dir. 2011/83 Annex I(B)), written without 'u'; Dutch needs the verb alternatives, so (*) also follows deel/delen and herroep/herroepen as in the official f… |
| `page.privacy-policy:policy_banner_Pgpxip/eyebrow` | Eyebrow: 9 vs 5 chars, no shorter Dutch word; it sits alone above the banner heading. |
| `page.privacy-policy:policy_banner_Pgpxip/company_last_updated` | “Laatst bijgewerkt” is quoted again in section 11.; R2 (review F9): 'Laatst bijgewerkt oktober' → 'Laatst bijgewerkt in oktober', as in the other legal texts |
| `page.privacy-policy:legal_toc_section_gYznx3/content_section_g6nYeY/title` | Contextual QA, not a fixed slot (R2, review F7): legal section heading that wraps. TERM: data controller → verwerkingsverantwoordelijke (AVG term). 31 vs 18 chars; no shorter correct legal term, the heading may wrap. |
| `page.privacy-policy:legal_toc_section_gYznx3/content_section_g6nYeY/content` | 'Data Privacy Lead' kept as an internal role title. It must not be read as a 'functionaris voor gegevensbescherming' (DPO); lawyer to confirm.; R2 (review F8): addresses exactly as in the EN (brief); official Dutch addr… |
| `page.privacy-policy:legal_toc_section_gYznx3/content_section_FcEDdA/nav_label` | Short nav form; the section title uses the AVG term 'doeleinden'. |
| `page.privacy-policy:legal_toc_section_gYznx3/content_section_EAKJLC/nav_label` | 13 vs 9 chars; shorter 'Bewaring' is possible but less clear. |
| `page.privacy-policy:legal_toc_section_gYznx3/content_section_qyyKHX/nav_label` | 11 vs 8 chars; no shorter Dutch word. |
| `page.privacy-policy:legal_toc_section_gYznx3/content_section_qyyKHX/title` | Contextual QA, not a fixed slot (R2, review F7): legal section heading that wraps. 23 vs 17 chars; 'Beveiliging' alone would drop 'data'. The heading can wrap. |
| `page.privacy-policy:legal_toc_section_gYznx3/content_section_qyyKHX/content` | 'data transfers' here is technical traffic, so 'gegevensoverdrachten', not the legal 'doorgifte'. |
| `page.privacy-policy:legal_toc_section_gYznx3/content_section_pjNTAq/nav_label` | 11 vs 7 chars; no shorter Dutch word. |
| `page.terms-and-conditions:policy_banner_Pgpxip/heading` | Standard Dutch page title; the document calls itself "Algemene Voorwaarden" (clause 2.1). Sentence case per the heading rule; in running text the document name keeps its capitals. |
| `page.terms-and-conditions:policy_banner_Pgpxip/description` | Same NL as the matching terms-of-service policy blocks. \| TERM: plan → plan |
| `page.terms-and-conditions:policy_banner_Pgpxip/company_info` | Same NL as the matching terms-of-service policy blocks. \| TERM: trading as → handelend onder de naam; VAT → btw-nummer. Place names in their Dutch form throughout (Bruges → Brugge, Belgium → België, Brussels → Brussel)… |
| `page.terms-and-conditions:policy_banner_Pgpxip/company_last_updated` | Same NL as the matching terms-of-service policy blocks. |
| `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_GLa7AN/content` | Same NL as the matching terms-of-service policy blocks. \| TERM: Enterprise number → Ondernemingsnummer; Enterprise Court of Ghent, division Bruges → Ondernemingsrechtbank Gent, afdeling Brugge; R2 (review F8): addresse… |
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
| `admin:policy:privacy-policy:body#b002` | R2 (review F8): addresses exactly as in the EN (brief); official Dutch address forms only if Victor decides so |
| `admin:policy:privacy-policy:body#b003` | R2 (review F9): 'Laatst bijgewerkt oktober' → 'Laatst bijgewerkt in oktober', as in the other legal texts |
| `admin:policy:privacy-policy:body#b008` | Official Dutch title of the act. |
| `admin:policy:privacy-policy:body#b009` | Official Dutch title of the act; EC → EG. |
| `admin:policy:privacy-policy:body#b011` | Contextual QA, not a fixed slot (R2, review F7): policy body heading that wraps. 31 vs 18 chars; no shorter correct legal term, the heading may wrap. |
| `admin:policy:privacy-policy:body#b014` | EN source: the mailto link also wraps the phone number (the page-settings version links only the e-mail). Kept as in the EN.; R2 (review F8): addresses exactly as in the EN (brief); official Dutch address forms only if … |
| `admin:policy:privacy-policy:body#b044` | 'voorkomen' here is fraud prevention (EN 'preventing'), not a cosmetic claim. |
| `admin:policy:privacy-policy:body#b094` | CIR92 → WIB 92 (Dutch abbreviation of the same code). Lawyer: check art. III.86 vs III.88 WER (see page-settings note). |
| `admin:policy:privacy-policy:body#b112` | R2 (review F8): addresses exactly as in the EN (brief); official Dutch address forms only if Victor decides so |
| `admin:policy:privacy-policy:body#b116` | R2 (review F8): addresses exactly as in the EN (brief); official Dutch address forms only if Victor decides so |
| `admin:policy:privacy-policy:body#b127` | “Cookie-instellingen” must match the NL footer link label. |
| `admin:policy:privacy-policy:body#b128` | Contextual QA, not a fixed slot (R2, review F7): policy body heading that wraps. 23 vs 17 chars; 'Beveiliging' alone would drop 'data'. The heading can wrap. |
| `admin:policy:terms-of-service:body#b002` | R2 (review F8): addresses exactly as in the EN (brief); official Dutch address forms only if Victor decides so; R2 (review F9): 'Btw-nummer BE 0676' → 'btw BE 0676', as in the other legal texts |
| `admin:policy:terms-of-service:body#b006` | R2 (review F9): 'geëxploiteerd door' → 'beheerd door', as in the other legal texts |
| `admin:policy:terms-of-service:body#b007` | R2 (review F8): addresses exactly as in the EN (brief); official Dutch address forms only if Victor decides so; R2 (review F9): 'Btw-nummer BE 0676' → 'btw BE 0676', as in the other legal texts |
| `admin:policy:terms-of-service:body#b015` | Link (href and visible URL) still points to the English page /en/…; kept unchanged per the rules. Needs the NL URL once the Dutch page exists. |
| `admin:policy:terms-of-service:body#b020` | “Pay now” → “Nu betalen”: check that this is the exact label of the final button in the Dutch Shopify checkout. |
| `admin:policy:terms-of-service:body#b049` | Lawyer: whether priming an airless pump counts as "unsealing" under art. VI.53, 5° WER is a legal judgement in the EN itself; the translation keeps it as written. |
| `admin:policy:terms-of-service:body#b052` | EN gap: this procedure (and the Annex) covers withdrawal from a one-time order only, while 4.1.1 also grants withdrawal for memberships. Lawyer to confirm.; R2 (review F8): addresses exactly as in the EN (brief); offici… |
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
| `admin:policy:terms-of-service:body#b150` | R2 (review F9): 'Het Europese platform voor onlinegeschillenbeslechting' → 'Het EU-platform voor onlinegeschillenbeslechting', as in the other legal texts |
| `admin:policy:terms-of-service:body#b153` | EN "an eligible, unopened contract": a contract cannot be unopened; translated as the intended "a contract for unopened goods that is eligible". Lawyer: the statutory model form has no "unopened" condition. |
| `admin:policy:terms-of-service:body#b154` | R2 (review F8): addresses exactly as in the EN (brief); official Dutch address forms only if Victor decides so |
| `admin:policy:terms-of-service:body#b155` | Follows the official Dutch model form, without its "u" (je register) and with the (*) marks at the EN positions. |
| `admin:policy:terms-of-service:body#b161` | revised in assembly: identical legal passage: same NL as the Terms of Service |
| `admin:policy:terms-of-service:body#b164` | revised in assembly: identical legal passage: same NL as the Terms of Service |
| `admin:policy:refund-policy:title` | Contextual QA, not a fixed slot (R2, review F7): policy title; its checkout-footer link wraps. Shopify policy title; 20 vs 13 chars. No shorter correct term: 'Retourbeleid' would mean return policy. Title links wrap in … |
| `admin:policy:refund-policy:body#b002` | R2 (review F8): addresses exactly as in the EN (brief); official Dutch address forms only if Victor decides so |
| `admin:policy:refund-policy:body#b018` | 'biological formulations' → 'op de biologie gebaseerde formules' (Dutch 'biologisch' = organic); see the page item. |
| `admin:policy:refund-policy:body#b027` | Product names translated descriptively; align with the NL product titles once they exist. |
| `admin:policy:refund-policy:body#b031` | Lawyer/claims: free-from claim (parabens, endocrine disruptors); see the page item. |
| `admin:policy:refund-policy:body#b032` | 'diagnose, treat or cure' is a disclaimer, translated literally. |
| `admin:policy:refund-policy:body#b037` | Lawyer: refund deadline and 'unopened' condition vs Art. VI.50 WER; see the page item. |
| `admin:policy:refund-policy:body#b054` | Capture artefact kept: in the policy the mailto link wraps the phone number too (the page has separate mailto and tel links). Plain text matches the page. |
| `admin:policy:refund-policy:body#b057` | R2 (review F8): addresses exactly as in the EN (brief); official Dutch address forms only if Victor decides so |
| `admin:policy:refund-policy:body#b061` | Lawyer: 'unprimed pump = seal' for the hygiene exception (Art. VI.53, 5° WER); see the page item. |
| `admin:policy:refund-policy:body#b065` | Translated as the EN reads (R2, review F3), same as the page item; the legal owner should approve or correct the EN heading (the law presumes the lack of conformity existed at delivery). |
| `admin:policy:refund-policy:body#b074` | revised in assembly: identical legal passage: same NL as the Terms of Service |
| `admin:policy:refund-policy:body#b086` | EN check: the per-pause cap equals the yearly total; translated as written (see the page item). |
| `admin:policy:refund-policy:body#b094` | Lawyer: check 'Art. VI.19/1 WER' (see the page item). |
| `admin:policy:refund-policy:body#b100` | Capture artefact kept: the mailto link wraps the phone number too (separate links on the page). The EN comma after the number is not needed in Dutch. |
| `admin:policy:refund-policy:body#b103` | Official Dutch street name (Boulevard du Roi Albert II = Koning Albert II-laan); number, 'bus 1' and postcode unchanged. See the page item.; R2 (review F8): addresses exactly as in the EN (brief); official Dutch address… |
| `admin:policy:refund-policy:body#b105` | R2 (review F8): addresses exactly as in the EN (brief); official Dutch address forms only if Victor decides so |
| `admin:policy:refund-policy:body#b113` | Capture artefact kept: the mailto link wraps the phone number too (separate links on the page).; R2 (review F8): addresses exactly as in the EN (brief); official Dutch address forms only if Victor decides so |
| `admin:policy:refund-policy:body#b114` | Official Dutch model-form wording without 'u'; (*) added after the Dutch verb alternatives as in the official form (all EN marks kept).; R2 (review F9): harmonised with admin:policy:terms-of-service:body#b155, terms-of-… |
| `admin:policy:refund-policy:body#b120` | revised in assembly: identical legal passage: same NL as the Terms of Service |
| `admin:policy:refund-policy:body#b122` | EN 'an eligible, unopened contract' is ambiguous; see the page item.; R2 (review F9): the model form's 'eligible, unopened contract' sentence as in terms-of-service #b153 |
| `admin:policy:refund-policy:body#b123` | revised in assembly: identical legal passage: same NL as the Terms of Service |
| `admin:policy:shipping-policy:body#b001` | Link still points to the English page /en/… (href unchanged). |
| `admin:policy:shipping-policy:body#b002` | Identical to terms-of-service b100. |
| `admin:policy:shipping-policy:body#b003` | revised in assembly: identical legal passage: same NL as the Terms of Service |
| `admin:policy:shipping-policy:body#b004` | Identical to terms-of-service b102. |
| `admin:policy:shipping-policy:body#b005` | Identical to terms-of-service b103. |
| `admin:policy:shipping-policy:body#b006` | Identical to terms-of-service b104. |
| `admin:policy:shipping-policy:body#b007` | Identical to terms-of-service b105. |
| `admin:policy:shipping-policy:body#b008` | Same NL as terms-of-service b060 (clause 5.4), plus the clause reference. |
| `admin:policy:contact-information:body#b005` | EN source: the mailto link also wraps the phone number. Kept as in the EN.; R2 (review F8): addresses exactly as in the EN (brief); official Dutch address forms only if Victor decides so |
| `admin:policy:contact-information:body#b006` | EN source: the mailto link wraps 'or call +32 …' (a phone number inside an e-mail link); kept, link text translated. |
| `admin:policy:legal-notice:title` | Contextual QA, not a fixed slot (R2, review F7): policy title; its checkout-footer link wraps. TERM: Legal notice → Wettelijke vermeldingen (usual Belgian title). 23 vs 12 chars; shorter alternative 'Juridische info'. |
| `admin:policy:legal-notice:body#b001` | href unchanged (EN terms page); see contact-information b001. |
| `admin:policy:legal-notice:body#b005` | R2 (review F8): addresses exactly as in the EN (brief); official Dutch address forms only if Victor decides so |
| `admin:policy:legal-notice:seo.title` | Contextual QA, not a fixed slot (R2, review F7): browser-tab and search-result title. 35 vs 24 chars (page title, not a UI slot); see legal-notice title. |
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
| `product:main/highlights_slider_9wAjAb/text_1` | R2 (review F5/F6): endorsement count, pending claim review like C81 on the Duo PDP; 'Used by' rendered without 'gebruikt' (brand rule). 'kPNI practitioners' → 'kPNI-therapeuten' (the usual Dutch title) |
| `product:main/highlights_slider_9wAjAb/text_3` | 39 here vs '+36 studies' on the homepage stat strip; kept as EN |
| `product:main/icon_with_text_xhaDGB/heading_1` | revised in assembly: added in assembly (the keyword scan had held it; the claims review cleared it); same trust-row form as the Duo buy box (Figma NL) |
| `product:main/icon_with_text_xhaDGB/heading_3` | 17 vs 13 chars, but this is the approved Figma NL short form, checked in the Figma trust row |
| `product:main/treatment_journey_block/disclaimer_text` | revised in assembly: approved Figma NL (3738:27474); same on product.json and the Duo PDP |
| `product:main/professional_testimonials_block/heading` | R2 (review F6): 'Used by professionals' → 'In de praktijk bij professionals' (brand rule; the earlier 'professionals, not the customer' exception has no basis in the brief) |
| `product:main/info_card_FnBcaN/body_text` | 'Health Rewards' kept as a name: legacy program name next to Care Credit, EN needs a decision. 'purchase' → 'bestelling', 'products' → 'artikelen' |
| `product:disclosures/heading` | Section holds safety warnings and regulatory disclosures; 'Wettelijke vermeldingen' is clearer if space allows |
| `admin:product:complete-hygiene-kit:seo.description` | R2 (review F5): pending-claim-review, same claim wording as a gated field |
| `admin:app:judge-me:preview_badge.review_count` | 'review' is standard Dutch; Judge.me may also offer 'beoordeling(en)' |
| `admin:product:morning-toothbrush:seo.description` | EN meta is the body cut mid-word ('by ea'); NL completes the sentence from the body. EN typos read as intended: 'dispurge' = disperse, 'of' = or, 'nurished' = nourished; R2 (review F6): 'onze tandpasta' → 'onze formule'… |
| `admin:product:evening-toothbrush:seo.description` | EN meta cut mid-word ('applicati'); NL completes the sentence. '2 to 4 applications' predates the 1-pump dose (products.md, 4 Aug) |
| `admin:product:whitening-charcoal-dental-floss:seo.description` | EN meta cut mid-word ('removi'); NL completes the sentence from the body |
| `admin:product:evening-toothbrush-2-0:seo.description` | EN meta cut mid-word; NL completes the sentence. '2 to 4 applications' predates the 1-pump dose |
| `admin:product:morning-toothbrush-2-0:seo.description` | EN meta cut mid-word; NL completes the sentence from the body; R2 (review F6): 'onze tandpasta' → 'onze formule', as in the body (brand rule) |
| `admin:product:complete-hygiene-kit:body_html#b001` | R2 (review F5): pending-claim-review, same claim wording as a gated field |
| `admin:product:morning-toothbrush:body_html#b001` | EN typos read as intended ('dispurge' = disperse, 'of' = or, 'nurished' = nourished). '2 to 4 applications' predates the 1-pump dose. Link still points to the old /en/product/ URL (kept); R2 (review F5): pending-claim-r… |
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
| `admin:product:morning-toothbrush-2-0:body_html#b001` | EN typos read as intended ('dispurge', 'of', 'nurished'). '2 to 4 applications' predates the 1-pump dose. Link points to the old /en/product/ URL (kept); R2 (review F5): pending-claim-review for the retired '2 to 4' dos… |
| `admin:app:morning-toothbrush-2-0:selling_plan_group:Subscribe and Save` | revised in assembly: one form for every legacy 'Subscribe and Save' group |
| `admin:app:morning-toothbrush-2-0:selling_plan.712456667517.name` | EN typo 'month' → plural |
| `admin:app:morning-toothbrush-2-0:selling_plan.712460992893.name` | EN leading space dropped |
| `admin:app:asleep-evening-toothpaste-2-0:selling_plan_group:Subscribe and Save` | revised in assembly: one form for every legacy 'Subscribe and Save' group |
| `admin:app:asleep-evening-toothpaste-2-0:selling_plan.712456700285.name` | EN typo 'month' → plural |
| `admin:app:asleep-evening-toothpaste-2-0:selling_plan.712460992893.name` | EN leading space dropped |
| `admin:app:awake-morning-toothpaste-2-0:selling_plan_group:Subscribe and Save` | revised in assembly: one form for every legacy 'Subscribe and Save' group |
| `admin:app:awake-morning-toothpaste-2-0:selling_plan.712456733053.name` | EN typo 'month' → plural |
| `admin:app:awake-morning-toothpaste-2-0:selling_plan.712460992893.name` | EN leading space dropped |
| `admin:page:why-karmicare:title` | Contextual QA, not a fixed slot (R2, review F7): page title that wraps. 16 vs 13 chars; no shorter form |
| `admin:page:why-karmicare:body_html#b001` | No final full stop, as in the EN |
| `admin:page:why-use-hydroxyapatite-toothpaste:title` | 'use' → 'kiezen voor' (avoids 'gebruiken') |
| `admin:page:why-use-hydroxyapatite-toothpaste:body_html#b001` | 'start using' → 'overstappen op' (avoids 'gebruiken') |
| `admin:page:why-stop-using-fluoride-toothpaste:seo.description` | Full stop added between the two joined body blocks (the EN runs them together) |
| `admin:page:nhap-technology:body_html#b000` | R2 (review F2): body heading added to the inventory; NL as admin:article:news/nano-hydroxyapatite:title (same EN), with the source's trailing |
| `admin:article:news/nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste:title` | R2 (review F5): pending-claim-review, same claim wording as a gated field |
| `admin:article:news/nano-hydroxyapatite:title` | R2 (review F5): pending-claim-review, same claim wording as a gated field |
| `admin:collection:vgbc2025:text#02` | Collection title is a code; kept as is. |
| `admin:article:news/nano-hydroxyapatite:text#01` | R2 (review F5): pending-claim-review, same claim wording as a gated field |
| `admin:article:news/nano-hydroxyapatite:body_html#b005` | Article subheading, no UI length limit. |
| `admin:article:news/nano-hydroxyapatite:body_html#b009` | R6 (review R6-02): category word after first contact: 'in onze Awake- of Asleep-tandpasta.' → 'in onze Awake- of Asleep-formule.' (brand rule) |
| `admin:article:news/nano-hydroxyapatite:body_html#b027` | EN 'phosphorous oxygen' read as 'phosphorus, oxygen'. |
| `admin:article:news/nano-hydroxyapatite:body_html#b036` | 'voorkomt' here means 'occurs', not 'prevents'.; R2 (review F4): 'organic' restored as in the EN; hydroxyapatite is usually called inorganic, so the EN or clinical owner resolves the source term, the translation does not |
| `admin:article:news/nano-hydroxyapatite:body_html#b042` | R6 (review R6-02): category word after first contact: 'toxines in hun tandpasta stoppen' → 'toxines in hun formules stoppen' (brand rule) |
| `admin:article:news/nano-hydroxyapatite:body_html#b053` | R6 (review R6-02): category word after first contact: 'door te poetsen met een tandpasta met nano-hydroxyapatiet' → 'door te poetsen met een formule op basis…', 'ook een natuurlijke tandpasta met andere' → 'ook een natu… |
| `admin:article:news/nano-hydroxyapatite:body_html#b054` | R6 (review R6-02): category word after first contact: 'bij de keuze van je tandpasta' → 'bij de keuze van je formule', 'Overstappen op een fluoridevrije tandpasta' → 'Overstappen op een fluoridevrije formule' (brand rul… |
| `admin:article:news/nano-hydroxyapatite:body_html#b056` | R6 (review R6-02): category word after first contact: 'poetst met een tandpasta met nano-HAp' → 'poetst met een formule met nano-HAp' (brand rule) |
| `admin:article:news/nano-hydroxyapatite:body_html#b057` | R6 (review R6-02): category word after first contact: 'Tandpastaformules (zoals tandpasta en re…' → 'Poetsformules (zoals pasta’s en reminera…' (brand rule) |
| `admin:article:news/nano-hydroxyapatite:body_html#b064` | R2 (review F6): 'producten' → 'formules' (brand rule) |
| `admin:article:news/nano-hydroxyapatite:body_html#b066` | R2 (review F6): 'producten … gebruikt' → 'met zulke formules poetst' (brand rule); R6 (review R6-02): category word after first contact: 'Andere whiteningtandpasta’s' → 'Andere whiteningformules' (brand rule) |
| `admin:article:news/nano-hydroxyapatite:body_html#b067` | R6 (review R6-02): the reviewer's compound replacement: 'whiteningproducten' → 'whiteningformules' (brand rule); R6 (review R6-02): category word after first contact: 'Weinig schurende tandpasta’s met nano-HAp' → 'Weini… |
| `admin:article:news/nano-hydroxyapatite:body_html#b069` | R2 (review F5): pending-claim-review, same claim wording as a gated field |
| `admin:article:news/nano-hydroxyapatite:body_html#b072` | R6 (review R6-02): category word after first contact: 'met Karmicare-tandpasta,' → 'met Karmicare,' (brand rule) |
| `admin:article:news/nano-hydroxyapatite:body_html#b074` | The EN article has no heading 2 between 1 and 3. |
| `admin:article:news/nano-hydroxyapatite:body_html#b087` | R6 (review R6-02): category word after first contact: 'met de nano-hydroxyapatiettandpasta van Karmicare' → 'met de formule met nano-hydroxyapatiet van Karmicare' (brand rule) |
| `admin:article:news/nano-hydroxyapatite:body_html#b089` | R6 (review R6-02): category word after first contact: 'Poetsen met een tandpasta met nano-hydroxyapatiet' → 'Poetsen met een formule met nano-hydroxyapatiet' (brand rule) |
| `admin:article:news/nano-hydroxyapatite:body_html#b097` | R6 (review R6-02): category word after first contact: 'tandpasta’s of mondspoelingen met fluoride' → 'formules of mondspoelingen met fluoride' (brand rule) |
| `admin:article:news/nano-hydroxyapatite:body_html#b102` | R6 (review R6-02): category word after first contact: 'Je tandpasta doet er meer toe' → 'Je formule doet er meer toe' (brand rule) |
| `admin:article:news/nano-hydroxyapatite:body_html#b111` | R6 (review R6-02): category word after first contact: 'De biorhythmische nano-HAp-tandpasta van Karmicare' → 'De bioritmische nano-HAp-formule van Karmicare' (brand rule) |
| `admin:article:news/nano-hydroxyapatite:body_html#b113` | R6 (review R6-02): category word after first contact: 'Overstappen op een tandpasta met nano-HAp' → 'Overstappen op een formule met nano-HAp' (brand rule) |
| `admin:article:news/nano-hydroxyapatite:body_html#b115` | R6 (review R6-02): category word after first contact: 'in een speciaal geformuleerde tandpasta.' → 'in een speciaal ontwikkelde formule.' (brand rule) |
| `admin:article:news/nano-hydroxyapatite:body_html#b116` | R6 (review R6-02): category word after first contact: 'wel meer tandpasta’s met nano-hydroxyapatiet' → 'wel meer formules met nano-hydroxyapatiet' (brand rule) |
| `admin:article:news/nano-hydroxyapatite:body_html#b117` | R6 (review R6-02): category word after first contact: 'Laat de nano-HAp-tandpasta daarna' → 'Laat de nano-HAp-formule daarna', ' fluoridetandpasta ' → ' een formule met fluoride ' (brand rule) |
| `admin:article:news/nano-hydroxyapatite:seo.title` | EN typo 'Hydroxapatite' (SEO title); the NL uses the correct spelling. |
| `admin:article:news/morning-and-night-time-brushing-why-timing-matters:body_html#b027` | R6 (review R6-02): category word after first contact: 'versterkt de Awake-tandpasta het glazuur' → 'versterkt de Awake-formule het glazuur', 'remineraliseert de Asleep-tandpasta en' → 'remineraliseert de Asleep-formule … |
| `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:body_html#b005` | Article subheading, no UI length limit. |
| `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:body_html#b012` | R2 (review F6): 'producten' → 'artikelen' (brand rule) |
| `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:body_html#b027` | R6 (review R6-02): category word after first contact: 'de Awake-ochtendtandpasta' → 'de Awake-ochtendformule' (brand rule) |
| `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:body_html#b051` | Article subheading, no UI length limit.; R2 (review F6): 'producten' → 'artikelen' (brand rule) |
| `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:body_html#b055` | R2 (review F6): 'gebruiken' → 'nemen' (brand rule) |
| `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:body_html#b064` | R2 (review F6): 'producten' → 'artikelen' (brand rule) |
| `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:body_html#b075` | R2 (review F6): 'gebruikt' → 'genomen' (brand rule) |
| `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:body_html#b076` | R2 (review F6): 'producten met cafeïne' → 'alles wat cafeïne bevat' (brand rule) |
| `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:body_html#b093` | R2 (review F6): 'producten' → 'middelen' (supplements) (brand rule) |
| `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:body_html#b096` | R6 (review R6-02): the reviewer's compound replacement: 'kwaliteitsproducten' → 'kwaliteitsmiddelen' (brand rule) |
| `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:body_html#b097` | R6 (review R6-02): category word after first contact: 'bevat de tandpastaset van Karmicare' → 'bevat de set van Karmicare' (brand rule) |
| `admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:seo.description` | The EN meta description is cut off ('m…'); the NL stops at the same point. |
| `admin:article:news/nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste:body_html#b005` | Article subheading, no UI length limit. |
| `admin:article:news/nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste:body_html#b019` | R6 (review R6-02): category word after first contact: 'alternatief voor fluoride in tandpasta.' → 'alternatief voor fluoride in mondverzorging.' (brand rule) |
| `admin:article:news/nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste:body_html#b020` | R6 (review R6-02): category word after first contact: 'de keuze voor een tandpasta met dit krachtige mineraal' → 'de keuze voor een formule met dit krachtige mineraal' (brand rule) |
| `admin:article:news/nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste:body_html#b033` | R6 (review R6-02): the reviewer's compound replacement: 'tandverzorgingsproducten' → 'mondzorgformules' (brand rule); R6 (review R6-02): category word after first contact: 'een vaste waarde in tandpasta en mondzorgformu… |
| `admin:article:news/nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste:body_html#b041` | R2 (review F5): pending-claim-review, same claim wording as a gated field; R6 (review R6-02): category word after first contact: 'Tandpasta met nano-HAp helpt' → 'Een formule met nano-HAp helpt' (brand rule) |
| `admin:article:news/nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste:body_html#b045` | R6 (review R6-02): the reviewer's compound replacement: 'whiteningproducten' → 'whiteningformules' (brand rule) |
| `admin:article:news/nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste:body_html#b049` | The EN article has no heading 2 between 1 and 3. |
| `admin:article:news/nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste:body_html#b061` | R6 (review R6-02): category word after first contact: 'Je tandpasta doet er meer toe' → 'Je formule doet er meer toe' (brand rule) |
| `admin:article:news/nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste:body_html#b066` | R6 (review R6-02): category word after first contact: 'Overstappen op een tandpasta met nano-HAp' → 'Overstappen op een formule met nano-HAp' (brand rule) |
| `admin:article:news/nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste:body_html#b067` | EN 'Shop Now' rendered with 'Begin' (no 'kopen' in customer copy). |
| `admin:article:news/nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste:body_html#b069` | R6 (review R6-02): category word after first contact: 'in een speciaal geformuleerde tandpasta.' → 'in een speciaal ontwikkelde formule.' (brand rule) |
| `admin:article:news/nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste:body_html#b072` | R6 (review R6-02): category word after first contact: 'Niet elke tandpasta met nano-hydroxyapatiet is dezelfde.' → 'Niet elke formule met nano-hydroxyapatiet is hetzelfde.' (brand rule) |
| `admin:article:news/nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste:body_html#b073` | R6 (review R6-02): category word after first contact: 'Laat de nano-HAp-tandpasta daarna' → 'Laat de nano-HAp-formule daarna' (brand rule) |
| `admin:article:news/nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste:body_html#b074` | R6 (review R6-02): category word after first contact: 'nooit met fluoridetandpasta!' → 'nooit met een formule met fluoride!' (brand rule) |
| `admin:article:news/nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste:seo.title` | R2 (review F5): pending-claim-review, same claim wording as a gated field |
| `admin:article:news/nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste:seo.description` | The EN meta description is cut off mid-word ('fl…'); the NL completes the last word. |
| `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b005` | Article subheading, no UI length limit. |
| `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b007` | R6 (review R6-01): pending-claim-review, the claim waits for sign-off |
| `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b015` | R2 (review F6): 'product' → 'middel' (brand rule); R6 (review R6-01): pending-claim-review, the claim waits for sign-off; R6 (review R6-02): category word after first contact: 'De tandpasta waarmee we poetsen' → 'De for… |
| `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b016` | R6 (review R6-01): pending-claim-review, the claim waits for sign-off; R6 (review R6-02): category word after first contact: 'waarom de juiste tandpasta kiezen' → 'waarom de juiste formule kiezen' (brand rule) |
| `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b020` | R6 (review R6-01): pending-claim-review, the claim waits for sign-off |
| `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b021` | R6 (review R6-01): pending-claim-review, the claim waits for sign-off |
| `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b022` | R6 (review R6-01): pending-claim-review, the claim waits for sign-off |
| `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b024` | R6 (review R6-01): pending-claim-review, the claim waits for sign-off |
| `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b027` | R6 (review R6-02): category word after first contact: 'in de meeste gangbare tandpasta’s' → 'in de meeste gangbare formules' (brand rule) |
| `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b031` | R6 (review R6-02): category word after first contact: '>tandpasta met natuurlijke noötropica ' → '>een formule met natuurlijke noötropica ' (brand rule) |
| `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b038` | R6 (review R6-01): pending-claim-review, the claim waits for sign-off |
| `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b047` | R6 (review R6-01): pending-claim-review, the claim waits for sign-off |
| `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b049` | R6 (review R6-01): pending-claim-review, the claim waits for sign-off |
| `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b051` | R6 (review R6-01): pending-claim-review, the claim waits for sign-off |
| `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b052` | R6 (review R6-02): category word after first contact: 'Waarom doet je tandpasta ertoe?' → 'Waarom doet je formule ertoe?' (brand rule) |
| `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b055` | R2 (review F6): 'een cosmetisch product' → 'iets puur cosmetisch' (brand rule); R6 (review R6-01): pending-claim-review, the claim waits for sign-off; R6 (review R6-02): category word after first contact: 'Tandpasta mag… |
| `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b057` | R6 (review R6-01): pending-claim-review, the claim waits for sign-off; R6 (review R6-02): category word after first contact: 'hoort de juiste tandpasta ook' → 'hoort de juiste formule ook' (brand rule) |
| `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b058` | R6 (review R6-02): category word after first contact: 'Tandpasta met noötropica zoals guarana' → 'Een formule met noötropica zoals guarana' (brand rule) |
| `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b062` | R6 (review R6-01): pending-claim-review, the claim waits for sign-off; R6 (review R6-02): category word after first contact: 'hoort je tandpasta je lichamelijke' → 'hoort je formule je lichamelijke' (brand rule) |
| `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b066` | R6 (review R6-01): pending-claim-review, the claim waits for sign-off |
| `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b067` | R6 (review R6-01): pending-claim-review, the claim waits for sign-off; R6 (review R6-02): category word after first contact: 'hoort je tandpasta ook je sociale' → 'hoort je formule ook je sociale' (brand rule) |
| `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b068` | R6 (review R6-01): pending-claim-review, the claim waits for sign-off; R6 (review R6-02): category word after first contact: 'en munt in tandpasta zorgen' → 'en munt in een formule zorgen' (brand rule) |
| `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b070` | R6 (review R6-02): category word after first contact: 'van bioritmische tandpasta.' → 'van bioritmische formules.' (brand rule) |
| `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b071` | R6 (review R6-02): category word after first contact: '>Bioritmische tandpasta’s zijn geformuleerd' → '>Bioritmische formules zijn ontworpen' (brand rule) |
| `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b072` | R6 (review R6-02): category word after first contact: 'Onze ochtendtandpasta bevat' → 'Onze ochtendformule bevat' (brand rule) |
| `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b073` | R6 (review R6-01): pending-claim-review, the claim waits for sign-off; R6 (review R6-02): category word after first contact: 'De Awake-tandpasta helpt ook' → 'De Awake-formule helpt ook' (brand rule) |
| `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b074` | R6 (review R6-02): category word after first contact: 'De avondtandpasta bevat' → 'De avondformule bevat' (brand rule) |
| `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b076` | R6 (review R6-01): pending-claim-review, the claim waits for sign-off |
| `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b078` | EN 'Shop Now' rendered as 'Begin nu' (no 'kopen' in customer copy). |
| `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b079` | R6 (review R6-02): category word after first contact: 'De Awake- en Asleep-tandpasta’s van' → 'De Awake- en Asleep-formules van' (brand rule) |
| `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b081` | R6 (review R6-01): pending-claim-review, assertions kept for review; 'ochtendtandpasta'/'avondtandpasta' → 'ochtendformule'/'avondformule' (category word) |
| `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b082` | R6 (review R6-01): pending-claim-review, the claim waits for sign-off |
| `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b083` | R6 (review R6-02): category word after first contact: 'Kies je een tandpasta die je glimlach' → 'Kies je een formule die je glimlach' (brand rule) |
| `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b085` | R6 (review R6-01): pending-claim-review, the claim waits for sign-off |
| `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b087` | R6 (review R6-01): pending-claim-review, the claim waits for sign-off |
| `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b090` | R6 (review R6-01): pending-claim-review, the claim waits for sign-off |
| `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b091` | R6 (review R6-01): pending-claim-review, the claim waits for sign-off |
| `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b092` | R6 (review R6-01): pending-claim-review, the claim waits for sign-off |
| `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b093` | R6 (review R6-02): category word after first contact: 'De Awake- en Asleep-tandpasta van Karmic…' → 'De Awake- en Asleep-formules van Karmica…' (brand rule) |
| `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b094` | R6 (review R6-01): pending-claim-review, the claim waits for sign-off; R6 (review R6-02): category word after first contact: 'hoe onze bioritmische tandpasta vandaag' → 'hoe onze bioritmische verzorging vandaag' (brand … |
| `admin:article:news/how-oral-health-impacts-your-overall-wellness:body_html#b095` | EN 'in a tube': rendered 'in één flacon' (Karmicare comes in pump bottles; 'tube' is a banned word).; R6 (review R6-01): pending-claim-review, the claim waits for sign-off |
| `admin:article:news/how-oral-health-impacts-your-overall-wellness:seo.description` | The EN meta description is cut off; the NL stops at the same point.; R6 (review R6-01): pending-claim-review, the claim waits for sign-off |
| `admin:article:news/top-natural-whitening-toothpaste-for-a-brighter-smile:body_html#b002` | The EN sentence is incomplete ('With more people shifting…'); translated as a complete sentence. |
| `admin:article:news/top-natural-whitening-toothpaste-for-a-brighter-smile:body_html#b003` | R6 (review R6-02): category word after first contact: 'traditionele whiteningtandpasta vol' → 'traditionele whiteningformules vol', 'bioritmische tandpasta van Karmicare ' → 'bioritmische formules van Karmicare ' (brand… |
| `admin:article:news/top-natural-whitening-toothpaste-for-a-brighter-smile:body_html#b004` | R6 (review R6-02): category word after first contact: 'de voordelen van natuurlijke whiteningtandpasta' → 'de voordelen van natuurlijke whiteningformules' (brand rule) |
| `admin:article:news/top-natural-whitening-toothpaste-for-a-brighter-smile:body_html#b005` | R6 (review R6-02): category word after first contact: 'Natuurlijke whiteningtandpasta' → 'Natuurlijke whiteningformules' (brand rule) |
| `admin:article:news/top-natural-whitening-toothpaste-for-a-brighter-smile:body_html#b006` | R6 (review R6-02): category word after first contact: 'Natuurlijke whiteningtandpasta verwijdert' → 'Een natuurlijke whiteningformule verwijdert' (brand rule) |
| `admin:article:news/top-natural-whitening-toothpaste-for-a-brighter-smile:body_html#b007` | R6 (review R6-02): category word after first contact: 'Deze milde tandpasta’s zijn veilig' → 'Deze milde formules zijn veilig', 'ondersteunt natuurlijke tandpasta ook' → 'ondersteunt een natuurlijke formule ook' (brand … |
| `admin:article:news/top-natural-whitening-toothpaste-for-a-brighter-smile:body_html#b008` | R6 (review R6-02): category word after first contact: 'Waarom kiezen voor natuurlijke whiteningtandpasta?' → 'Waarom kiezen voor een natuurlijke whiteningformule?' (brand rule) |
| `admin:article:news/top-natural-whitening-toothpaste-for-a-brighter-smile:body_html#b009` | R6 (review R6-02): category word after first contact: 'In tegenstelling tot gangbare tandpasta’s vol' → 'In tegenstelling tot gangbare formules vol', 'natuurlijke whiteningtandpasta veili…' → 'een natuurlijke whiteningf… |
| `admin:article:news/top-natural-whitening-toothpaste-for-a-brighter-smile:body_html#b010` | R6 (review R6-02): category word after first contact: 'Met natuurlijke whiteningtandpasta kies …' → 'Met een natuurlijke whiteningformule kie…' (brand rule) |
| `admin:article:news/top-natural-whitening-toothpaste-for-a-brighter-smile:body_html#b011` | EN 'Shop' rendered as 'Ontdek'. |
| `admin:article:news/top-natural-whitening-toothpaste-for-a-brighter-smile:body_html#b013` | R6 (review R6-02): category word after first contact: 'Gewone tandpasta’s bevatten vaak' → 'Gewone formules bevatten vaak' (brand rule) |
| `admin:article:news/top-natural-whitening-toothpaste-for-a-brighter-smile:body_html#b015` | R6 (review R6-02): category word after first contact: 'Natuurlijke whiteningtandpasta is niet-toxisch' → 'Een natuurlijke whiteningformule is niet-toxisch' (brand rule) |
| `admin:article:news/top-natural-whitening-toothpaste-for-a-brighter-smile:body_html#b016` | R2 (review F6): 'gebruiken' → 'bevatten' (brand rule); R6 (review R6-02): category word after first contact: 'Natuurlijke whiteningtandpasta’s bevatten' → 'Natuurlijke whiteningformules bevatten' (brand rule) |
| `admin:article:news/top-natural-whitening-toothpaste-for-a-brighter-smile:body_html#b021` | R6 (review R6-02): category word after first contact: 'Omdat onze tandpasta vrij is' → 'Omdat onze formule vrij is' (brand rule) |
| `admin:article:news/top-natural-whitening-toothpaste-for-a-brighter-smile:body_html#b030` | R6 (review R6-02): category word after first contact: 'toevoeging aan een ochtendtandpasta.' → 'toevoeging aan een ochtendformule.' (brand rule) |
| `admin:article:news/top-natural-whitening-toothpaste-for-a-brighter-smile:body_html#b038` | R6 (review R6-02): category word after first contact: '>Tandpasta met pepermuntolie ' → '>Een formule met pepermuntolie ' (brand rule) |
| `admin:article:news/top-natural-whitening-toothpaste-for-a-brighter-smile:body_html#b044` | R6 (review R6-02): category word after first contact: 'geeft je tandpasta een warme' → 'geeft je formule een warme' (brand rule) |
| `admin:article:news/top-natural-whitening-toothpaste-for-a-brighter-smile:body_html#b051` | EN 'Shop Our Bestselling' rendered as 'Ontdek onze populairste'.; R6 (review R6-01): 'Bestselling' kept as a sales claim (meest verkocht, as headaches b019) and pending review; 'formule' for the category word |
| `admin:article:news/top-natural-whitening-toothpaste-for-a-brighter-smile:body_html#b052` | R6 (review R6-02): category word after first contact: 'de natuurlijke whiteningtandpasta die bij je past' → 'de natuurlijke whiteningformule die bij je past' (brand rule) |
| `admin:article:news/top-natural-whitening-toothpaste-for-a-brighter-smile:body_html#b057` | R6 (review R6-02): category word after first contact: 'Zorg dat de tandpasta die je kiest' → 'Zorg dat de formule die je kiest' (brand rule) |
| `admin:article:news/top-natural-whitening-toothpaste-for-a-brighter-smile:body_html#b059` | R6 (review R6-02): category word after first contact: 'Je wilt een doeltreffende tandpasta,' → 'Je wilt een doeltreffende formule,' (brand rule) |
| `admin:article:news/top-natural-whitening-toothpaste-for-a-brighter-smile:body_html#b061` | R6 (review R6-02): category word after first contact: 'Natuurlijke whiteningtandpasta’s zijn een veiligere' → 'Natuurlijke whiteningformules zijn een veiligere', 'Kies de tandpasta die bij je past' → 'Kies de formule di… |
| `admin:article:news/top-natural-whitening-toothpaste-for-a-brighter-smile:body_html#b062` | R6 (review R6-02): category word after first contact: 'natuurlijke whiteningtandpasta’s die aansluiten' → 'natuurlijke whiteningformules die aansluiten' (brand rule) |
| `admin:article:news/top-natural-whitening-toothpaste-for-a-brighter-smile:seo.description` | The EN meta description is cut off; the NL stops at the same point. |
| `admin:article:news/5-reasons-you-should-avoid-fluoride-in-toothpaste:body_html#b003` | R6 (review R6-02): category word after first contact: 'gezonder dan tandpasta met fluoride?' → 'gezonder dan een variant met fluoride?' (brand rule) |
| `admin:article:news/5-reasons-you-should-avoid-fluoride-in-toothpaste:body_html#b005` | Article subheading, no UI length limit. |
| `admin:article:news/5-reasons-you-should-avoid-fluoride-in-toothpaste:body_html#b006` | R6 (review R6-02): category word after first contact: 'vaak aan tandpasta toegevoegd' → 'vaak aan formules voor mondverzorging toegevoegd' (brand rule) |
| `admin:article:news/5-reasons-you-should-avoid-fluoride-in-toothpaste:body_html#b009` | R6 (review R6-02): the reviewer's compound replacement: 'mondverzorgingsproducten' → 'mondzorgformules' (brand rule); R6 (review R6-02): category word after first contact: 'heel wat tandpastamerken bekeken' → 'heel wat … |
| `admin:article:news/5-reasons-you-should-avoid-fluoride-in-toothpaste:body_html#b012` | R2 (review F6): 'het gebruik' → 'de toepassing' (brand rule) |
| `admin:article:news/5-reasons-you-should-avoid-fluoride-in-toothpaste:body_html#b014` | R6 (review R6-02): category word after first contact: 'Wat is fluoride in tandpasta?' → 'Wat is fluoride in mondverzorging?' (brand rule) |
| `admin:article:news/5-reasons-you-should-avoid-fluoride-in-toothpaste:body_html#b015` | 'voorkomt' here means 'occurs', not 'prevents'. |
| `admin:article:news/5-reasons-you-should-avoid-fluoride-in-toothpaste:body_html#b016` | R2 (review F6): 'producten' → 'formules'; R6 (review R6-02): category word after first contact: 'Veel tandpastamerken voegen' → 'Veel mondzorgmerken voegen' (brand rule) |
| `admin:article:news/5-reasons-you-should-avoid-fluoride-in-toothpaste:body_html#b019` | R6 (review R6-02): category word after first contact: 'Sommige tandpasta’s combineren' → 'Sommige formules combineren' (brand rule) |
| `admin:article:news/5-reasons-you-should-avoid-fluoride-in-toothpaste:body_html#b021` | R6 (review R6-02): category word after first contact: 'nuttig zijn in tandpasta,' → 'nuttig zijn in mondverzorging,' (brand rule) |
| `admin:article:news/5-reasons-you-should-avoid-fluoride-in-toothpaste:body_html#b022` | R6 (review R6-02): category word after first contact: 'fluoridevrije tandpasta’s aan.' → 'fluoridevrije formules aan.' (brand rule) |
| `admin:article:news/5-reasons-you-should-avoid-fluoride-in-toothpaste:body_html#b024` | R6 (review R6-02): category word after first contact: 'van fluoride in tandpasta' → 'van fluoride in mondverzorging' (brand rule) |
| `admin:article:news/5-reasons-you-should-avoid-fluoride-in-toothpaste:body_html#b047` | R6 (review R6-02): category word after first contact: 'fluoridevrije tandpasta.' → 'fluoridevrije formule.' (brand rule) |
| `admin:article:news/5-reasons-you-should-avoid-fluoride-in-toothpaste:body_html#b056` | R6 (review R6-02): category word after first contact: 'Tandpasta met nano-HAp, zoals' → 'Een formule met nano-HAp, zoals' (brand rule) |
| `admin:article:news/5-reasons-you-should-avoid-fluoride-in-toothpaste:body_html#b070` | EN 'Shop' rendered as 'Ontdek' (no 'kopen' in customer copy).; R6 (review R6-02): category word after first contact: 'Ontdek de fluoridevrije tandpasta van Karmicare.' → 'Ontdek de fluoridevrije formules van Karmicare.'… |
| `admin:article:news/5-reasons-you-should-avoid-fluoride-in-toothpaste:body_html#b074` | R6 (review R6-02): category word after first contact: 'de beste natuurlijke tandpasta ' → 'de beste natuurlijke formule ' (brand rule) |
| `admin:article:news/headaches-and-tooth-pain-understanding-the-connection:body_html#b010` | EN 'Shop' rendered as 'Ontdek'. |
| `admin:article:news/headaches-and-tooth-pain-understanding-the-connection:body_html#b019` | R2 (review F5): 'Bestselling' kept as a sales claim (meest verkocht, not populairst) and pending review; 'formule' avoids a second commodity mention |
| `admin:article:news/headaches-and-tooth-pain-understanding-the-connection:body_html#b043` | EN 'Shop Now' rendered as 'Begin nu'. |
| `admin:article:news/headaches-and-tooth-pain-understanding-the-connection:seo.description` | The EN meta description is cut off; the NL stops at the same point. |
| `admin:article:news/3-reasons-why-you-should-look-for-an-sls-free-toothpaste:body_html#b002` | R6 (review R6-02): the reviewer's compound replacement: 'verzorgingsproducten' → 'verzorgingsformules' (brand rule) |
| `admin:article:news/3-reasons-why-you-should-look-for-an-sls-free-toothpaste:body_html#b005` | Article subheading, no UI length limit. |
| `admin:article:news/3-reasons-why-you-should-look-for-an-sls-free-toothpaste:body_html#b006` | R6 (review R6-02): category word after first contact: 'Veel commerciële tandpasta’s' → 'Veel commerciële formules' (brand rule) |
| `admin:article:news/3-reasons-why-you-should-look-for-an-sls-free-toothpaste:body_html#b007` | R6 (review R6-02): category word after first contact: 'verwerkt bijna niemand ze in tandpasta.' → 'verwerkt bijna niemand ze in mondverzorging.' (brand rule) |
| `admin:article:news/3-reasons-why-you-should-look-for-an-sls-free-toothpaste:body_html#b008` | R6 (review R6-02): category word after first contact: 'Tandpasta met natriumlaurylsulfaat' → 'Een formule met natriumlaurylsulfaat' (brand rule) |
| `admin:article:news/3-reasons-why-you-should-look-for-an-sls-free-toothpaste:body_html#b009` | R6 (review R6-02): category word after first contact: 'de ingrediëntenlijst van je tandpasta' → 'de ingrediëntenlijst van je formule' (brand rule) |
| `admin:article:news/3-reasons-why-you-should-look-for-an-sls-free-toothpaste:body_html#b011` | R6 (review R6-02): category word after first contact: 'voor een fluoridevrije tandpasta kiezen' → 'voor een fluoridevrije formule kiezen' (brand rule) |
| `admin:article:news/3-reasons-why-you-should-look-for-an-sls-free-toothpaste:body_html#b012` | R6 (review R6-02): category word after first contact: 'voor een SLS-vrije tandpasta kiest' → 'voor een SLS-vrije formule kiest', 'glycolipiden in onze tandpasta verwerken' → 'glycolipiden in onze formules verwerken' (br… |
| `admin:article:news/3-reasons-why-you-should-look-for-an-sls-free-toothpaste:body_html#b014` | R6 (review R6-02): the reviewer's compound replacement: 'verzorgingsproducten' → 'verzorgingsformules' (brand rule) |
| `admin:article:news/3-reasons-why-you-should-look-for-an-sls-free-toothpaste:body_html#b016` | R6 (review R6-02): category word after first contact: 'in je whiteningtandpasta zitten' → 'in je whiteningformule zitten' (brand rule) |
| `admin:article:news/3-reasons-why-you-should-look-for-an-sls-free-toothpaste:body_html#b019` | R2 (review F6): 'product' → 'formule' (brand rule) |
| `admin:article:news/3-reasons-why-you-should-look-for-an-sls-free-toothpaste:body_html#b022` | R6 (review R6-02): category word after first contact: 'het schuimende effect van tandpasta.' → 'het schuimende effect van een formule.' (brand rule) |
| `admin:article:news/3-reasons-why-you-should-look-for-an-sls-free-toothpaste:body_html#b025` | R6 (review R6-02): category word after first contact: 'Kiezen voor een SLS-vrije tandpasta is' → 'Kiezen voor een SLS-vrije formule is' (brand rule) |
| `admin:article:news/3-reasons-why-you-should-look-for-an-sls-free-toothpaste:body_html#b026` | R6 (review R6-02): category word after first contact: 'om voor een SLS-vrije tandpasta te kiezen' → 'om voor een SLS-vrije formule te kiezen' (brand rule) |
| `admin:article:news/3-reasons-why-you-should-look-for-an-sls-free-toothpaste:body_html#b028` | R2 (review F4): 'may want to avoid' kept as a suggestion, not an instruction; 'products' → 'formules' (brand rule) |
| `admin:article:news/3-reasons-why-you-should-look-for-an-sls-free-toothpaste:body_html#b030` | R6 (review R6-02): category word after first contact: 'het echte werk doen in je tandpasta,' → 'het echte werk doen in je mondverzorging,' (brand rule) |
| `admin:article:news/3-reasons-why-you-should-look-for-an-sls-free-toothpaste:body_html#b032` | R6 (review R6-02): category word after first contact: 'een must is in je tandpasta.' → 'een must is in je formule.' (brand rule) |
| `admin:article:news/3-reasons-why-you-should-look-for-an-sls-free-toothpaste:body_html#b034` | R6 (review R6-02): category word after first contact: 'andere tandpasta’s met fluoride' → 'andere formules met fluoride' (brand rule) |
| `admin:article:news/3-reasons-why-you-should-look-for-an-sls-free-toothpaste:body_html#b037` | R6 (review R6-02): category word after first contact: 'kies je voor een SLS-vrije tandpasta?' → 'kies je voor een SLS-vrije formule?' (brand rule) |
| `admin:article:news/3-reasons-why-you-should-look-for-an-sls-free-toothpaste:body_html#b038` | R2 (review F6): 'producten' → 'formules' (brand rule) |
| `admin:article:news/3-reasons-why-you-should-look-for-an-sls-free-toothpaste:body_html#b039` | R6 (review R6-02): category word after first contact: 'en kies tandpasta met pure ingrediënten' → 'en kies een formule met pure ingrediënten', 'wat je in standaardtandpasta vindt' → 'wat je in standaardformules vindt' (… |
| `admin:article:news/3-reasons-why-you-should-look-for-an-sls-free-toothpaste:body_html#b041` | R6 (review R6-02): category word after first contact: 'vast te houden aan tandpasta met SLS' → 'vast te houden aan een formule met SLS' (brand rule) |
| `admin:article:news/3-reasons-why-you-should-look-for-an-sls-free-toothpaste:body_html#b043` | EN 'Shop … Now' rendered as 'Ontdek nu'.; R6 (review R6-02): category word after first contact: 'Ontdek nu de SLS-vrije tandpasta van Karmicare' → 'Ontdek nu de SLS-vrije formules van Karmicare' (brand rule) |
| `admin:article:news/3-reasons-why-you-should-look-for-an-sls-free-toothpaste:body_html#b045` | R6 (review R6-02): category word after first contact: '(zoals gewone tandpasta met SLS en fluoride)' → '(zoals gewone formules met SLS en fluoride)', 'heb je geen speciale kindertandpasta nodig' → 'heb je geen aparte fo… |
| `admin:article:news/3-reasons-why-you-should-look-for-an-sls-free-toothpaste:body_html#b046` | R6 (review R6-02): category word after first contact: 'Poetsen met SLS-vrije tandpasta helpt' → 'Poetsen met een SLS-vrije formule helpt' (brand rule) |
| `admin:article:news/3-reasons-why-you-should-look-for-an-sls-free-toothpaste:body_html#b048` | R6 (review R6-02): category word after first contact: 'de verkeerde tandpastaformule' → 'de verkeerde formule' (brand rule) |
| `admin:article:news/3-reasons-why-you-should-look-for-an-sls-free-toothpaste:body_html#b051` | R6 (review R6-02): category word after first contact: 'Tandpasta met SLS kan ook' → 'Een formule met SLS kan ook' (brand rule) |
| `admin:article:news/3-reasons-why-you-should-look-for-an-sls-free-toothpaste:body_html#b056` | R2 (review F4): as hedged as the EN ('can safely', 'will help', 'may miss'); the earlier NL stated outcomes as facts |
| `admin:article:news/3-reasons-why-you-should-look-for-an-sls-free-toothpaste:body_html#b057` | R6 (review R6-02): category word after first contact: 'Niet elke tandpasta is hetzelfde. Sommig…' → 'Niet elke formule is hetzelfde. Sommige …' (brand rule) |
| `admin:article:news/3-reasons-why-you-should-look-for-an-sls-free-toothpaste:seo.description` | The EN meta description is cut off; the NL stops at the same word.; R6 (review R6-02): the reviewer's compound replacement: 'verzorgingsproducten' → 'verzorgingsformules' (brand rule); R6 (review R6-02): category word a… |

</details>
