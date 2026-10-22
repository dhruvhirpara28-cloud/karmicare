# R2 source changes, for the FR payload

The NL review `docs/runtime-review/B2-NL-ASTRA.md` (19 Oct, verdict FAIL) led to these changes in the EN source. Merge `karmicare/soft-launch-source-copy` to receive them. This file lists every source-level change since `2194ef3` (the R1 state FR merged in `71b3c5a`), so the FR payload can follow it exactly.

How the list was made: `en-source.json` at `2194ef3` was compared with the current file entry by entry. The result is 1 entry added (needs-review), 0 removed, 3 newly held, 16 reclassified to needs-review, 3 changed in notes only, and 84 more entries with a derived `claim_status`. `python3 docs/source-copy/digest.py` exits 0.

## Digests

Only batch 06 changed. FR `batch-06-content-pages.json` is stale until it has the new entry; every other FR `source_digest` stays valid.

| Batch | Before (2194ef3) | Now |
|---|---|---|
| `batch-06-content-pages` | 21 entries, `f78c391aa267b82eb0c85af36edea6e4583651bf` | 22 entries, `3dee3b56341f67b113dcd59eb85d3a2e3f21d628` |
| all other batches | unchanged | unchanged |

## 1. Added: translate it

| Id | Batch | EN | Gate | FR action |
|---|---|---|---|---|
| `admin:page:nhap-technology:body_html#b000` | 06 | `Discover the Wonderful Inner World of Nano Hydroxyapatite and Why You Need it in Your Toothpaste<br><br>` | `claim_status: needs-review` (necessity wording) | Insert it before `#b001` and mark it pending-claim-review. NL reused its translation of `admin:article:news/nano-hydroxyapatite:title` (the same EN) and kept the trailing `<br><br>`. |

This is the `h1` inside `.rte` on `/pages/nhap-technology`. The B2 builder skipped it because the text equals an article title. A sweep of every capture found no other block lost this way.

## 2. Newly held: do not translate

| Id | Batch | Source change | NL note (FR can use the same reason) |
|---|---|---|---|
| `admin:product:asleep-evening-toothpaste-2-0:body_html#b002` | 05 | `claim_status: unsupported`, basis added | `unsupported-claim: sleep/wake effect; same hold as this resource's seo.description` |
| `admin:product:awake-morning-toothpaste-2-0:body_html#b002` | 05 | `claim_status: unsupported`, basis added | as above |
| `admin:article:news/3-reasons-why-you-should-look-for-an-sls-free-toothpaste:body_html#b035` | 07 | `blocked: "NEEDS APPROVED COPY"` (four competitor names) | `needs-approved-copy: competitor names prohibited; EN owner must supply compliant source` |

FR already holds the two sleep/wake lines (`58755f7`). Only the SLS block is new for FR.

## 3. Reclassified to needs-review: pending-claim-review in FR

| Id | Batch | Before → now | Why (full basis in `claim_basis` / CLAIMS-REVIEW.md) |
|---|---|---|---|
| `admin:whitening-charcoal-dental-floss:title` | 02 | none → needs-review, `claims: ["C100"]` | Floss-whitening wording, new register claim C100 |
| `admin:karmicare-biorhythmic-oral-care-system:custom.compare_table:welcome_kit_row.products` | 02 | none → needs-review, C100 | as above |
| `admin:karmicare-biorhythmic-oral-care-system:media.69271648010621.alt` | 02 | none → needs-review, C100 | as above (kit image alt) |
| `admin:karmicare-biorhythmic-oral-care-system:media.69884688236925.alt` | 02 | none → needs-review, C100 | as above (kit animation alt) |
| `product:main/highlights_slider_9wAjAb/text_1` | 05 | none → needs-review; `status` approved → needs-review | "+100 kPNI practitioners", the same endorsement count as C81 |
| `admin:product:complete-hygiene-kit:body_html#b001` | 05 | none → needs-review | Floss-whitening wording |
| `admin:product:complete-hygiene-kit:seo.description` | 05 | none → needs-review | Floss-whitening wording |
| `admin:product:morning-toothbrush:body_html#b001` | 05 | none → needs-review | Retired "2 to 4 applications" dose; keep the source number |
| `admin:product:morning-toothbrush-2-0:body_html#b001` | 05 | none → needs-review | as above |
| `admin:article:news/nano-hydroxyapatite:body_html#b069` | 07 | approved → needs-review | "remineralizes teeth from the inside" mechanism |
| `admin:article:news/nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste:body_html#b041` | 07 | approved → needs-review | "saliva isn't enough on its own" (necessity) |
| `admin:article:news/headaches-and-tooth-pain-understanding-the-connection:body_html#b019` | 07 | approved → needs-review | "Bestselling" (unverified superlative) |
| `admin:article:news/nano-hydroxyapatite:title` | 07 | none → needs-review | "Why You Need it in Your Toothpaste" (necessity) |
| `admin:article:news/nano-hydroxyapatite:text#01` | 07 | none → needs-review | the same title as image alt |
| `admin:article:news/nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste:title` | 07 | none → needs-review | "Why You Need It In Your Toothpaste" |
| `admin:article:news/nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste:seo.title` | 07 | none → needs-review | as above |

## 4. Notes only: a translation rule, no gate change

| Id | Batch | Note | FR action |
|---|---|---|---|
| `page.consumer-rights:legal_toc_section_gYznx3/content_section_FcEDdA/content` | 04 | Heading 4.1 "Two-year presumption of conformity" reads as the opposite of the rule it introduces; the legal owner approves or corrects the EN. | Translate the heading as written, a presumption of *conformity*, not of non-conformity. Change only the heading text and keep `legal-review`. |
| `admin:policy:refund-policy:body#b065` | 04 | as above | as above |
| `admin:article:news/nano-hydroxyapatite:body_html#b036` | 07 | "naturally occurring organic biomaterial": the EN or clinical owner resolves "organic". | Keep "organic" as written; the entry stays pending-claim-review. |

## 5. Metadata only: no FR action

- **`claim_status` on every claim-bearing entry.** 84 more entries in batches 01–03 have it now, as the strictest status of their `claims`. Together with the 4 C100 entries in section 3, that makes 88: 12 approved, 72 needs-review, 4 unsupported. Their gates are unchanged. A checker can now read every gate from the entry itself.
- **CLAIMS-REVIEW.md.** The batch 01–03 register has 67 claims (17 approved, 47 needs-review, 3 unsupported). After R2, batches 05–07 contain 30 approved, 274 needs-review and 115 unsupported blocks. Twelve blocks were newly entered in the claim register: eleven previously unclassified entries and the newly inventoried nHAp heading. Three previously approved blocks were reclassified to needs-review. (Wording from the R6 re-review, R6-03; "now" reads "after R2" because the R6 additions below change the totals again.)

## 6. NL payload rules from R2 that apply to FR too

These are not source changes. They are the review's payload findings, which FR can check against its own files. The NL commits and `docs/localization/nl/REPORT.md` ("R2 fixes") have the details.

| Finding | Rule | Where to look in FR |
|---|---|---|
| F3 | Translate a legal proposition as written. A correction belongs to the legal owner. | the two entries in section 4 |
| F4 | Keep the EN's hedges ("can", "may", "will help", "may want to") and every source assertion. | SLS article `#b056` and `#b028`, nano-hydroxyapatite `#b036` |
| F6 | No competitor names. Keep commodity words (product, use, buy, tube) out of promotional prose: the morning-brush bodies, "Used by …" headings, "everyday products" (nootropics `#b012`, `#b051`, `#b064`), fluoride `#b016`. Official names (the EU CPNP portal), legal document titles, the footer compliance line and approved Figma text stay as they are. | NL changed 24 entries, the held SLS block included |
| F7 | `fit-risk` on constrained strings that grow; title flags are contextual QA. | both `research_behind_system_EkjATL/button_label`, PDP `loop_subscriptions_gPKypi/shipping_value_html`, `icon_with_text_endcta/heading_3`, `custom.comparison_section#18` and `#23` |
| F8 | Addresses exactly as in the EN, including "box 1" and the EN city and country names. | `Vizierstraat 28, 8000 Bruges, Belgium`; `Boulevard du Roi Albert II 8, box 1, 1000 Brussels` (and `, Belgium`); `Koning Albert II-laan 16, 1000 Brussels`; `Drukpersstraat 35, 1000 Brussels, Belgium`; footer `Vizierstraat 28, 8000, Belgium`. These are 33 spans in 29 entries. |
| F9 | The same EN gets the same translation. Check identical homepage/PDP twins and repeated legal passages. | the model withdrawal sentence (terms `#b155`, refund `#b114`, consumer-rights `content_section_at3pLy`) keeps the EN's `(*)` markers |
| F10 | Every `never_translate` entry is held, including the two Dawn keys `locale:general.social.links.facebook` and `.instagram`. | batch 03 |

The NL validator `docs/localization/nl/validate.py` now checks these invariants. FR's `check.py` can apply them to the `fr` field:

- **H1**: `claim_status` unsupported → held.
- **H2**: needs-review → held or pending-claim-review.
- **H3**: `legal` → held or legal-review.
- **H4**: `legacy` → held.
- **H5**: `never_translate` → held.
- **H6**: `blocked` → held.
- **H7**: every hold has a reason.
- **S1**: EN addresses unchanged.
- **S2**: `(*)` count kept.

## R6 additions

The R6 re-review `docs/runtime-review/B2-NL-R6-ASTRA.md` (20 Oct, pass with fixes) led to one more source change, R6-01. `en-source.json` was compared with the state before R6 (`2aa84e4`) entry by entry. The result is 30 entries reclassified to needs-review, and nothing else: no entry added, removed or newly held, and no EN text changed. Every digest is unchanged, so FR `source_digest` values stay valid. `python3 docs/source-copy/digest.py` exits 0.

### Reclassified to needs-review: pending-claim-review in FR

The first row is the reviewer's R6-01 entry, with its exact basis. The reviewer asked for the rest of that article to be rechecked semantically. That recheck gated 28 more of its blocks, and the copy check found one more missed "Bestselling" claim. Each entry's full basis is in `claim_basis` and CLAIMS-REVIEW.md. All rows share the prefix `admin:article:news/`; "W" stands for `how-oral-health-impacts-your-overall-wellness`.

| Id | Before → now | Claim wording |
|---|---|---|
| W `:body_html#b081` | unclassified → needs-review | "The morning toothpaste, Awake, is suited to boost energy and mental clarity …" and "completely free from harmful chemicals" |
| W `:seo.description` | unclassified → needs-review | "Did you know oral health directly impacts" |
| W `:body_html#b007` | unclassified → needs-review | oral health directly impacts mental, physical and social well-being |
| W `:body_html#b015` | unclassified → needs-review | "a critical component of our overall wellness" |
| W `:body_html#b016` | unclassified → needs-review | "choosing the right toothpaste is crucial for complete wellness" |
| W `:body_html#b020` | unclassified → needs-review | "Cognitive decline." (list item under b019) |
| W `:body_html#b021` | unclassified → needs-review | "Reduced mental clarity." (list item under b019) |
| W `:body_html#b022` | unclassified → needs-review | "Depression." (list item under b019) |
| W `:body_html#b024` | none → needs-review | "Long-lasting inflammation leads to chronic gum disease." |
| W `:body_html#b038` | none → needs-review | "This increases the risk of heart attack and stroke." |
| W `:body_html#b047` | unclassified → needs-review | an attributed study finding on attractive smiles |
| W `:body_html#b049` | unclassified → needs-review | "28% of young adults" (attributed statistic) |
| W `:body_html#b051` | unclassified → needs-review | the pull quote of the b047 finding |
| W `:body_html#b055` | unclassified → needs-review | "an essential instrument that enhances and preserves overall health" |
| W `:body_html#b057` | unclassified → needs-review | "the right toothpaste should support your mental and psychological well-being" |
| W `:body_html#b062` | unclassified → needs-review | "your toothpaste should support your physical health" |
| W `:body_html#b066` | unclassified → needs-review | "without exposing your body to harmful chemicals" |
| W `:body_html#b067` | unclassified → needs-review | "your toothpaste should also support your social well-being" |
| W `:body_html#b068` | unclassified → needs-review | "ensure fresh breath, strengthen your teeth" |
| W `:body_html#b073` | unclassified → needs-review | "improves bad breath" |
| W `:body_html#b076` | unclassified → needs-review | "enhancing your overall well-being" |
| W `:body_html#b082` | unclassified → needs-review | "supports your overall health in the most wholesome way possible" |
| W `:body_html#b085` | unclassified → needs-review | "Improved mental performance" (benefit list) |
| W `:body_html#b087` | unclassified → needs-review | "Energised mornings." (benefit list) |
| W `:body_html#b090` | unclassified → needs-review | "Enhanced self-esteem and social interactions." (benefit list) |
| W `:body_html#b091` | unclassified → needs-review | "Wellness while ensuring safety." (benefit list) |
| W `:body_html#b092` | unclassified → needs-review | "The benefits are impressive!" |
| W `:body_html#b094` | unclassified → needs-review | "can support your whole-body wellness" |
| W `:body_html#b095` | unclassified → needs-review | "Order complete wellness in a tube" |
| `top-natural-whitening-toothpaste-for-a-brighter-smile:body_html#b051` | none → needs-review | "Shop Our Bestselling Natural Toothpaste", the same claim as headaches `#b019` (R2 F5) |

"Unclassified" means the claims pass never judged the block. "none" means it was judged to make no claim: `#b024` and `#b038` are links in the disease chain whose neighbours `#b025`, `#b036` and `#b037` are already gated. CLAIMS-REVIEW.md batches 05–07 now hold 30 approved, 304 needs-review and 115 unsupported blocks.

### NL payload rules from R6 that apply to FR too

These are not source changes. FR has already been told to gate `#b081` and to sweep its own blog bodies.

| Finding | Rule | NL change, for comparison |
|---|---|---|
| R6-01 | The 30 entries above are pending-claim-review. Keep the assertions as written; only category words change. | `#b081`: *ochtendformule* / *avondformule*. Top-whitening `#b051`: *meest verkochte natuurlijke formule*. |
| R6-02 | Commodity compounds count as commodity words: product(s) inside a word (*-producten*, FR *produits de …*). Category word: "toothpaste" stays only at first-contact moments, as tone-of-voice.md puts it: "a door, not a carpet", never negated. That means titles, SEO and alt texts, the opening self-reflection questions and one first prose mention per article. There is no blanket blog exemption. | 8 compounds as the reviewer gave them, and 120 later uses in the nine articles replaced by *formule(s)*, *mondverzorging* or *verzorging* (111 entries). Official names, legal titles, the footer compliance line and the approved Figma disclaimers stay. |
| R6 W1 | The NL validator now rejects product, tube, use and buy stems anywhere in a word in non-legal copy, with link URLs left out. Its 5 listed exceptions name the official and approved terms. Run on the payloads before R6, it flags exactly the reviewer's 8 compounds. | `docs/localization/nl/validate.py` W1 |

## 21 Oct: CTA wording "Begin your"

Victor (21 Oct): every CTA uses *Begin*, in the form *Begin your*. Three EN strings in `batch-02-pdp` changed; each entry keeps the previous text in `old_en` / `old_sha1`. No entry added, removed or reclassified. On top of `karmicare/soft-launch` (with the NV-13 `kit_free` retirement, `d72d791`): `batch-02-pdp` digest `2846c75e4df9f09cca9026b613cfddc61f307f5d` → `e3e79339215ffcf134b6813f1b46310a1c380fc8`; every other digest unchanged. NL and FR payloads already follow (`source_digest` updated); FR now also holds the retired `liquid:sections/main-product.liquid:1104` as NL does. `digest.py`, `nl/validate.py` and `fr/check.py` exit 0.

| Id | Before | Now | NL | FR |
|---|---|---|---|---|
| `product.subscription-item:main/buy_buttons/custom_button_text_by_plan` | `712106115453: Start my 60-Day rhythm` / `712155431293: Start my Karmicare Year` | `712106115453: Begin your 60-Day Rhythm` / `712155431293: Begin your Karmicare Year` | Begin je 60-dagenritme / Begin je Karmicare-jaar | Commencer votre Rythme 60 jours / Commencer votre année Karmicare |
| `liquid:sections/main-product.liquid:1024` (`kc.sticky_cart.cta_year_html`) | Begin the Karmicare Year | Begin your Karmicare Year | Begin je Karmicare-jaar | Commencer votre année Karmicare |
| `admin:…:custom.compare_table\|shop.metaobjects.compare_value#25` (Compare Plan "60-Day Rhythm", CTA Button) | Begin 60-Day Rhythm | Begin your 60-Day Rhythm (changed in the admin by Victor, 21 Oct) | Begin je 60-dagenritme | Commencer votre Rythme 60 jours |

The template setting and the metaobject reach `/nl` and `/fr` only once the payload is registered (`registration/DRY-RUN.md`: regenerate it first; nothing is registered yet); registration matches on the live EN, so these entries carry the new text. The locale key ships with the theme. Not changed: `compare_value#31`, the Year column's CTA "Begin" (live admin text on 21 Oct).

## 21 Oct: short announcement line

Victor (21 Oct): first "Circadian" became "Biorhythmic" (global-nav `ac822db`), then he chose the short line, because the long one (114 characters) ran too long. One EN string in `batch-03-header-footer` changed. `old_en` / `old_sha1` stay on the live text (`COMPLIMENTARY SHIPPING · 60-DAY MONEY-BACK GUARANTEE · BELGIAN-MADE`), because neither long line went live. `batch-03-header-footer` digest `a853d438d503867882d711cd4fa5a4a93c29759f` → `d5353b16cc57ea2181626f9f9cfa79dda0cb107d` (`a02de10a…` in between); every other digest unchanged. NL and FR payloads follow (`source_digest` updated) and keep their established guarantee phrases, because a bare *garantie* reads as the legal warranty. `digest.py`, `nl/validate.py` and `fr/check.py` exit 0. Claim C103 stays `needs-review`: the year still has no source in the repo.

| Id | Before | Now | NL | FR |
|---|---|---|---|---|
| `header-group:announcement-bar/announcement-bar-0/text` | COMPLIMENTARY SHIPPING & 60-DAY MONEY-BACK GUARANTEE FOR MEMBERS · BELGIAN-MADE · CIRCADIAN ORAL CARE SINCE 2017 | FREE SHIPPING & 60-DAY GUARANTEE FOR MEMBERS · BELGIAN-MADE · EST. 2017 | GRATIS VERZENDING & 60 DAGEN GELD TERUG VOOR LEDEN · GEMAAKT IN BELGIË · SINDS 2017 | LIVRAISON OFFERTE & SATISFAIT OU REMBOURSÉ 60 JOURS POUR LES MEMBRES · FABRIQUÉ EN BELGIQUE · DEPUIS 2017 |

## 21 Oct: homepage CTAs name the plan, "60-Day Rhythm"

Victor (21 Oct): every CTA names the plan the PDP sells, *Rhythm*, not *Ritual*. Four EN strings in `batch-01-homepage` changed; each keeps the live Ritual text in `old_en` / `old_sha1`. No entry added, removed or reclassified. `batch-01-homepage` digest `7694e7acce33a1e22a90de53273f2c90a8ddd70a` → `5286628ff7c87962782903bc9e1ce3350dd61469`; every other digest unchanged. NL and FR payloads follow (`source_digest` updated) with the plan names the PDP already uses. The schema defaults in `hero-karmicare`, `product-benefits-karmicare` and `two-formulas-karmicare` follow too. `digest.py`, `nl/validate.py` and `fr/check.py` exit 0.

| Id | Before | Now | NL | FR |
|---|---|---|---|---|
| `index:hero_karmicare_XKKLDK/buttons_DpYxth/button_label_1`, `index:two_formulas_karmicare/button_label`, `index:product_benefits_karmicare_bcQ6tp/button_label` | BEGIN YOUR 60-DAY RITUAL | BEGIN YOUR 60-DAY RHYTHM | BEGIN JE 60-DAGENRITME | COMMENCER VOTRE RYTHME 60 JOURS |
| `index:featured_product_3XpDKw/buy_buttons_UQznij/custom_button_text` | Begin your 60-day ritual | Begin your 60-Day Rhythm | Begin je 60-dagenritme | Commencer votre Rythme 60 jours |

## 21 Oct: PDP end button "Rhythm"

Victor (21 Oct, via the landing desk and the global coordinator): the button at the bottom of the PDP says *Rhythm* with a capital R, as every other CTA. One EN string in `batch-02-pdp` changed (`corrected`, `old_en` kept); NL and FR stay. `batch-02-pdp` digest `e3e79339215ffcf134b6813f1b46310a1c380fc8` → `87edec28e25fcae4bdef2adf127d761b0a725bc4`; every other digest unchanged. The template (`templates/product.subscription-item.json`) follows on `karmicare/soft-launch-global`.

| Id | Before | Now | NL | FR |
|---|---|---|---|---|
| `product.subscription-item:featured_product_Eb93Xa/buy_buttons_Ffxhap/custom_button_text` | Begin your 60-Day rhythm | Begin your 60-Day Rhythm | Begin je 60-dagenritme | Commencer votre Rythme 60 jours |

## 22 Oct: Victor's EN edits in the Shopify admin

Victor changed ten admin texts on 22 Oct; the global coordinator read them back on the storefront, and this lane re-read the article and the product title. Each entry stays `admin-held` and keeps its old text in `old_en` / `old_sha1`. No entry was added, removed or reclassified, and no claim status changed. Digests: `batch-02-pdp` `2468bab432715f0aea7f7b6aea815a8f65f70721`, `batch-03-header-footer` `18cdaec0fb18d1f00aa688c83d6bc0393b350319`, `batch-07-collections-blog` `c73c6f51bc707ba7944e4a30a465b2e5d17b9bfa`.

- **The three Duo texts are already registered in FR**: Victor entered the FR himself in Translate & Adapt (live). Take the FR in the table into the FR payload as it is. `registration/registered.json` keeps them out of `plan-fr.json` whatever the payload says.
- **The article's gated blocks stay gated** in FR as in NL: releasing them is Victor's decision.
- The twin article `news/nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste` was not edited: Victor hid it and redirected it to `/blogs/news/nano-hydroxyapatite`. All 79 of its entries are `retired` (EN and digest unchanged). Hold them in FR; the plan leaves them out either way.

| Id | Before | Now | NL | FR |
|---|---|---|---|---|
| `admin:karmicare-biorhythmic-oral-care-system:seo.title` | Fluoride-Free Morning & Night Toothpaste System \| KARMICARE | Fluoride-Free Nano-Hydroxyapatite Toothpaste \| Awake & Asleep | Fluoridevrije nano-hydroxyapatiet tandpasta \| Awake & Asleep | Dentifrice sans fluor à la nano-hydroxyapatite \| Awake & Asleep (Victor, live) |
| `admin:karmicare-biorhythmic-oral-care-system:seo.description` | Awake for the morning, Asleep for the night: two nano-hydroxyapatite toothpastes you don't rinse off. Fluoride-free, SLS-free. From €0.49 a brushing. | Awake for the morning, Asleep for the night: two fluoride-free nano-hydroxyapatite toothpastes in one Day & Night System. You don't rinse them off. | Awake voor de ochtend, Asleep voor de nacht: twee fluoridevrije nano-hydroxyapatiet tandpasta's in één dag- en nachtsysteem. Je spoelt ze niet uit. | Awake pour le matin, Asleep pour la nuit. Deux dentifrices sans fluor à la nano-hydroxyapatite, un système jour et nuit, sans rinçage. (Victor, live) |
| `admin:karmicare-biorhythmic-oral-care-system:title` | Awake & Asleep Morning & Night Toothpaste System | Awake & Asleep Fluoride-Free Nano-Hydroxyapatite Toothpaste, Day & Night System | Awake & Asleep fluoridevrije nano-hydroxyapatiet tandpasta, dag- en nachtsysteem | Awake & Asleep dentifrice sans fluor à la nano-hydroxyapatite, système jour et nuit (Victor, live) |
| `admin:navigation:company:links[2].title` | Why use hydroxapatite | Why hydroxyapatite | Waarom hydroxyapatiet | unchanged, *Pourquoi choisir l’hydroxyapatite* (update `en` / `en_sha1` only) |
| `admin:article:news/nano-hydroxyapatite:body_html#b016` | It guards against tooth decay by providing total protection against harmful dietary acids | It helps protect against tooth decay and harmful dietary acids | Het helpt beschermen tegen tandbederf en schadelijke zuren uit je voeding | re-translate |
| `admin:article:news/nano-hydroxyapatite:body_html#b088` | Nano HAp plugs the exposed dentin with deposits of hydroxyapatite nanoparticles. This works as a protective shield that prevents the nerve endings from getting stimulated by elements. | Nano HAp plugs the exposed dentin with deposits of hydroxyapatite nanoparticles. This works as a protective shield that helps keep the nerve endings from being stimulated. | Nano-HAp dicht het blootliggende dentine af met afzettingen van hydroxyapatiet-nanodeeltjes. Dat werkt als een beschermend schild dat de zenuwuiteinden helpt afschermen tegen prikkels. | re-translate |
| `admin:article:news/nano-hydroxyapatite:body_html#b090` | 4. Nano Hydroxyapatite Protects Your Enamel From Acidic Food and Drinks | 4. Nano Hydroxyapatite Helps Protect Your Enamel From Acidic Food | 4. Nano-hydroxyapatiet helpt je glazuur beschermen tegen zure voeding | re-translate |
| `admin:article:news/nano-hydroxyapatite:body_html#b100` | It remineralizes the enamel by reconstructing the lost deposits of calcium and phosphate, while also shielding the tooth surface from daily acid attacks. Plus, nano HAp protects your teeth against decay by grouping the disease-causing microbes together, which you can then spit out. | It remineralizes the enamel by reconstructing the lost deposits of calcium and phosphate, while also shielding the tooth surface from daily acid attacks. Plus, nano HAp helps protect your teeth against decay by binding bacteria together, so you can spit them out. | Het remineraliseert het glazuur door de verloren calcium- en fosfaatafzettingen weer op te bouwen, en schermt het tandoppervlak tegelijk af tegen de dagelijkse zuuraanvallen. Bovendien helpt nano-HAp je tanden beschermen tegen tandbederf door bacteriën aan elkaar te binden, zodat je ze kunt uitspugen. | re-translate |
| `admin:article:news/nano-hydroxyapatite:seo.title` | Why you need Nano Hydroxapatite in your toothpaste – KARMICARE | Nano-Hydroxyapatite Toothpaste: What It Is and How It Works \| KARMICARE | Tandpasta met nano-hydroxyapatiet: wat het is en hoe het werkt \| KARMICARE | re-translate |
| `admin:article:news/nano-hydroxyapatite:seo.description` | Here's everything you need to know about nano-hydroxyapatite, a medical marvel ingredient for better teeth, bones, and overall health. | What nano-hydroxyapatite is, how it works on enamel, and why Karmicare uses it in Awake and Asleep, two fluoride-free toothpastes. | Wat nano-hydroxyapatiet is, hoe het op je glazuur werkt en waarom Karmicare het in Awake en Asleep verwerkt, twee fluoridevrije tandpasta's. | re-translate |

## 22 Oct: no dentist confirmation, new footer slogan

Victor (22 Oct): the check-up reward needs no dentist, so the dentist clause is deleted (S2, choice a); the footer slogan is "Your mouth has a rhythm Now your oral care too", two sentences without a stop. Four EN strings changed (`corrected`, `old_en` kept): batch-02 digest `55340f9dc6dd5f8865fc1093937c727c0f1a3045`, batch-03 `d8fb1b30ea2f5be901b89205707d850a3f458452`. The theme key `kc.sticky_cart.checkup_info_html` already carries the FR with the clause deleted (`decided` in `theme-keys.json`); please confirm it in the payload.

| Id | Before | Now | NL |
|---|---|---|---|
| `product.subscription-item:main/info_card_FnBcaN/body_text` | <p>Karmicare is a care system, not a shelf item: the ritual arrives on your rhythm, and your care builds Care Credit as you go. On the Year, completing your dental check-up — confirmed by your dentist — adds €40 of it. You walk in with something to gain, not only something to pay. Care that comes back.</p> | <p>Karmicare is a care system, not a shelf item: the ritual arrives on your rhythm, and your care builds Care Credit as you go. On the Year, completing your dental check-up adds €40 of it. You walk in with something to gain, not only something to pay. Care that comes back.</p> | <p>Karmicare is een zorgsysteem, geen artikel uit het schap: het ritueel komt aan op jouw ritme, en je zorg bouwt onderweg Care Credit op. Met het Karmicare-jaar levert een afgeronde tandartscontrole nog eens €40 op. Je stapt binnen met iets te winnen, niet alleen met iets te betalen. Zorg die terugkomt.</p> |
| `product.subscription-item:main/loop_subscriptions_WEk4XJ/pricing_summary_checkup_tooltip` | Complete a dental check-up from month 6 or onwards, verified by your dentist. €40 in Care Credit is added to your account. Prevention, rewarded. | Complete a dental check-up from month 6 or onwards. €40 in Care Credit is added to your account. Prevention, rewarded. | Ga vanaf maand 6 op controle bij je tandarts. Er komt €40 Care Credit op je account. Preventie, beloond. |
| `liquid:sections/main-product.liquid:995` | Complete a dental check-up from month 6 or onwards, verified by your dentist. €40 in Care Credit is added to your account. | Complete a dental check-up from month 6 or onwards. €40 in Care Credit is added to your account. | Ga vanaf maand 6 op controle bij je tandarts. Er komt €40 Care Credit op je account. |
| `footer-group:footer/slogan` | Your mouth has a rhythm So should your oral care | Your mouth has a rhythm Now your oral care too | Je mond heeft een ritme Nu je mondverzorging ook |
