# B3 report · FR translation payloads

Task `task_064a318d44e7`, Orca run `run_32dd5602b983`, branch `karmicare/soft-launch-fr` (from `karmicare/soft-launch-source-copy` at 40b0641, the B1a inventory). 19 Oct 2026.

**Scope status:** batches 01, 02 and 03 are translated. Batches 04–08 do not exist yet: the NL worker is still extending the EN inventory on `karmicare/soft-launch-source-copy` (still at 40b0641 when this report was written). I merge and translate each one as it lands, following the coordinator's instruction.

## Preflight

| Check | Result |
|---|---|
| `orca status --json` | runtime `ready`, `reachable: true`, connection `connected` |
| `git status --short` / branch | clean tree on `karmicare/soft-launch-fr`, HEAD 40b0641 |
| Model / permission mode | Claude Opus 5.5 (`claude-opus-5-5`) in Claude Code, bypass-permissions mode, every Bash command sandboxed |
| `AGENTS.md` | read. README, `docs/pdp/RUNBOOK.md` and `docs/design-tokens/` are not in this repo, so COMMON-RULES and BRIEF apply |
| Network, Admin, theme files | none. No store request, no Figma call, no Admin write, no file outside `docs/localization/fr/` |
| Astra review | the coordinator dispatches it after `worker_done` (coordinator reply, 19 Oct). I did not start Codex or any other agent |

## What changed

| Commit | What |
|---|---|
| `b89ec56` | `batch-02-pdp.json` (477 entries) and `check.py` |
| `b782e4d` | `batch-01-homepage.json` (221 entries) |
| `1a54eb8` | `batch-03-header-footer.json` (41 entries) |
| this commit | `REPORT.md`, plus a corrected note on the SLS research card badge in both batch files |

### File format

Each `docs/localization/fr/<batch>.json` holds:

- **Batch header**: `source_digest` (the batch digest it was translated from), `source_entries`, `counts`, `flag_counts`.
- **One entry per source entry**, in source order: `{id, resource_type, file_or_handle, key_path, en, en_sha1, fr, status, flags, notes, source_status, claims?}`. `en_sha1` equals the source entry's `sha1`. So when an EN string changes, only that entry goes stale.

`status` says how the FR reaches the store:

| status | Meaning | Who registers it |
|---|---|---|
| `translated` | template or section-group setting | localization worker, through Translate & Adapt / theme translations |
| `admin` | product, metafield, metaobject, selling plan, navigation, shop or app text | Admin owner, through Shopify's translation resources |
| `theme-key` | hardcoded Liquid/JS text (`needs-key`) | localization worker, as a new key in `locales/fr.json` |
| `locale-present` | Dawn key that `locales/fr.json` already has; `fr` is copied from there, not re-translated | nothing to do |
| `held` | `fr: null`, reason in `notes` | no FR is registered, so Shopify falls back to EN |

`flags`:

| flag | Meaning |
|---|---|
| `pending-claim-review` | carries a needs-review claim (CLAIMS-REVIEW.md); translated as written, neither softened nor strengthened |
| `pending-en-review` | the EN itself is under review (offer conflicts, FAQ category mapping, slogan, Year sub-line); translated as written |
| `fit-risk` | longer than the EN in a button, chip, plan card, table cell, timeline row or sticky bar; `fr` holds the best short form, `notes` the full one |
| `source-defect` | the EN has a defect; `notes` says how the FR handles it |
| `legal-review` | needs Victor's or a lawyer's review before it ships |
| `gendered-title` | French would need a gender; written in an epicene form (see decision 3) |
| `wording-adapted` | the literal French would use a banned word (*produit, utiliser, acheter*…); `notes` gives the wording used instead |
| `not-rendered` | block disabled in the template |

## Counts

| Batch | Source digest | Entries | translated | admin | theme-key | locale-present | held |
|---|---|---:|---:|---:|---:|---:|---:|
| `batch-02-pdp` | `03dd18b9d41a21772da2e26b7060c42f6b2364d1` | 477 | 141 | 249 | 36 | 15 | 36 |
| `batch-01-homepage` | `b685b73d4dcdfddd153d4f130c0aa6806b9715ed` | 221 | 170 | 2 | 26 | 2 | 21 |
| `batch-03-header-footer` | `e17cadb5e223dd62b25e30e901091d8a8634aaf3` | 41 | 6 | 11 | 10 | 9 | 5 |
| **Total** | | **739** | **317** | **262** | **72** | **26** | **62** |

All 739 source entries are covered: 677 carry FR and 62 are held.

| Flag | 02 | 01 | 03 |
|---|---:|---:|---:|
| pending-claim-review | 27 | 30 | 1 |
| pending-en-review | 9 | 7 | 2 |
| fit-risk | 8 | 3 | 0 |
| source-defect | 7 | 2 | 1 |
| legal-review | 1 | 1 | 5 |
| gendered-title | 14 | 7 | 0 |
| wording-adapted | 14 | 3 | 2 |
| not-rendered | 6 | 0 | 0 |

The same EN string always gets the same FR: the homepage and the PDP share the clock, professionals, research, featured-product and Care Credit sections.

### Held (62)

| Reason | Count | Entries |
|---|---:|---|
| never-translate | 54 | Formula names (AWAKE, ASLEEP, Awake, Asleep, `Awake:`/`Asleep:`), practitioner names, study citations, both INCI lists, `nHAp`, `SCCS/1677/25`, the Subscription Names "60-Day Supply" / "Year Supply" and the matching plan group, Return on Care, Facebook/Instagram/LinkedIn |
| needs-approved-copy | 2 | homepage FAQ rows 2 and 3 (`[NEEDS APPROVED COPY]`) |
| unsupported-claim | 3 | homepage benefit card 06 text (C35); Sietske Hamelink's quote on both templates (C84, C85) |
| source-defect | 1 | treatment journey `#29` "— from your gums to the" (the EN stops mid-phrase) |
| gendered-title | 1 | mission card `#06` "founder" (decision 3) |
| integration | 1 | `snippets/loop-subscriptions.liquid:10` "Rendering loop-subscriptions": `featured-product.liquid:542` and `main-product.liquid:616` test for this exact text |

Two of the never-translate holds are mine. `compare_value#05` "Return on Care" is a program name that stays English, but its source entry lacks the flag. `Dr. Kris Sienaert` is held as a name; its spelling is still to be confirmed (B1a decision 6).

## Evidence

- `python3 docs/localization/fr/check.py`: **exit 0, 0 errors, 11 warnings.** The script checks:
  - every batch digest against the source and every `en_sha1` against `sha1(en)`;
  - one entry per source id, in order;
  - the status and flag vocabulary;
  - that the HTML tags, Liquid, `[tokens]`, `&nbsp;` count and the `kc-dynamic_price` / `dynamic_free_welcome_price` spans are the same in EN and FR;
  - that the selling-plan IDs in `custom_button_text_by_plan` are unchanged;
  - French spacing and apostrophes.
- The 11 warnings, each checked by hand:
  - **8 × *prévention***: the noun, translating the EN "Prevention" or "prevention" in the check-up tooltips, the plan tooltips (twice in the Year description), the compare table and C33 "BIOFILM PREVENTION". The forbidden form is the claim verb (*prévient*), and no FR entry uses it.
  - **2 × *produits***: "portail européen des produits cosmétiques" and "règlement (CE) n° 1223/2009 relatif aux produits cosmétiques". Both are official names.
  - **1 × *utilisation***: "conditions d'utilisation", a legal document name.
- `shopify theme check --fail-level error`: **exit 0**. 227 files inspected, 21 offenses, all warnings. No theme file changed and `.theme-check.yml` is untouched.
- Rendered check: none possible or needed here. Nothing is integrated yet, so this is pending the localization worker and the preview gate.

## Conventions applied

- **Register**: warm *vous* everywhere. No *tu*-forms (check.py looks for them).
- **Typography**:
  - U+00A0 before `: ; ! ? € % »` and after `«`.
  - U+202F as thousands separator (36 559, 38 000, 1 478, 1 700).
  - Decimal comma (0,49 €, SMD 2,17, p = 0,004), `IC à 95 %`.
  - French quotation marks « ».
  - Typographic apostrophe ’. Dawn's `fr.json` uses `'`, so a revert is a one-line change in the build if Victor prefers it.
  - Times stay 06:40 / 22:00 (glossary).
- **Exceptions to French spacing**:
  - the `ID: label` lines of `custom_button_text_by_plan` (parse syntax);
  - the runtime price spans in the Loop plan descriptions (`€5.90`, `10%`, `€21`), which stay verbatim as never-translate tokens.
- **Stay English**: Awake, Asleep, Care Credit, Return on Care, Leave-on, Karmicare, the KARMICARE™ legal product name, INCI, citations, nHAp, SCCS, Ph. Eur.
- **Order**: Awake before Asleep, morning before evening. The image alt `media.69840178020733`, which names the evening first in EN, is reordered in FR.
- **Banned words**: "toothpaste" → *dentifrice* only where the EN has it (SEO title and description, product title, alts, the FAQ question about a fluoride version, the admin description). No *produit, tube, acheter/achat, utiliser/utilisation* in customer copy, except the official names listed under Evidence.
- **Claims**: EU cosmetic verbs. Needs-review claims are translated as written and flagged. The three unsupported ones are held.

## Proposed terms (for Victor, one pass)

Every FR term is proposed: no approved FR copy exists.

**From the glossary FR column, applied as written:**

| EN | FR |
|---|---|
| 60-Day Rhythm | *Rythme 60 jours* |
| The Karmicare Year | *L'année Karmicare* |
| Try Once | *Essayer une fois* |
| Welcome Kit | *kit de bienvenue* |
| Care Credit / Return on Care | stay English |
| Dental Check-up Reward | *récompense contrôle dentaire* |
| 3 now, 3 in month 6 | *3 maintenant, 3 au 6e mois* |
| brushing | *brossage* |
| every 60 days | *tous les 60 jours* |
| 60-day money-back guarantee | *Satisfait ou remboursé 60 jours* |
| Gift, pause or cancel | *Offrir, suspendre ou résilier* |
| Free shipping | *Livraison offerte* |
| Most Picked | *★ Le plus choisi* |
| Brushing & Beyond | *Au-delà du brossage* |
| member / membership | *membre / adhésion* |
| member price | *prix membre* |
| Total today | *Total aujourd'hui* |
| one pump | *une pression* |
| Spit, don't rinse | *Crachez, ne rincez pas* |
| The Karmicare effect | *L'effet Karmicare* |
| Strengthen your teeth. Strengthen yourself. | *Renforcez vos dents. Renforcez-vous.* |
| Calmer check-ups / Evenings that wind down | as in the glossary |

Science terms (*tubules dentinaires, reminéralisation, microbiome buccal, charbon actif, argile bentonite, glycolipides, sans fluor, sans SLS*) are as in the glossary.

**Terms I had to decide (not in the glossary):**

| EN | FR (proposed) | Why |
|---|---|---|
| plan (Compare plans, Plans & Return on Care, Selling Plans) | *offre* | *formule* would clash with "two formulas" |
| subscription | *abonnement* | only where the EN says subscription |
| your plan (tooltip) | *votre adhésion* | |
| the Year (in running text) | *l'année Karmicare* | *l'année* alone reads as "the year" |
| AM/PM | *matin/soir* | glossary morning/evening; "Système de soin matin/soir Awake & Asleep" |
| Begin / Start CTAs | infinitive: *Commencer*, *Commencer maintenant*, *Commencer votre Rythme 60 jours* | header CTA *COMMENCER* drops "now" to fit |
| Start here / Choose how to begin | *Commencez ici* / *Choisissez comment commencer* | |
| Care Credit back | *Care Credit reversé* | *10 % reversés* in table cells |
| Free (price label) / FREE (kit) / Free (shipping) | *Gratuit* / *OFFERT* / *Offerte* | gender agreement with *prix*, *kit*, *livraison* |
| with first order | *1re commande* | fit; the glossary long form is in `notes` |
| one-time (compare table) | *en une fois* | glossary *unique* reads as "only" after a price |
| One time Purchase (Loop) | *Commande unique* | "purchase" is banned |
| Read more / Read less | *Lire la suite* / *Réduire* | |
| Trusted by professionals | *La confiance des professionnels* | |
| Care that comes back | *Le soin qui vous revient* | |
| evidence pack | *dossier scientifique* | |
| RCT / SEM / CI | *ECR / MEB / IC* | French scientific abbreviations |
| clauses 10 and 11 | *articles 10 et 11* | legal-review: must match the FR Terms |
| Terms and Conditions / Privacy Policy / Consumer Rights | *Conditions générales / Politique de confidentialité / Droits des consommateurs* | legal-review: must match the FR legal page titles (batch 04) |
| supplements / skincare (comparison) | *Compléments quotidiens / Soins de la peau* | glossary short forms |
| Shop Karmicare (menu) | *Boutique Karmicare* | noun, not "buy" |
| Why use hydroxapatite (menu) | *Pourquoi choisir l'hydroxyapatite* | fixes the spelling and avoids "use" |

## Fit risks (11)

| Batch | Entry | EN (chars) | FR used (chars) | Fallback in notes |
|---|---|---|---|---|
| 01 | hero, two-formulas and benefits `button_label` | BEGIN YOUR 60-DAY RITUAL (24) | COMMENCER VOTRE RITUEL 60 JOURS (31) | COMMENCER LE RITUEL |
| 02 | buy box `welcome_kit_title` | Welcome Kit · with first order (30) | Kit de bienvenue · 1re commande (31) | glossary long form (47) if there is room |
| 02 | buy box `try_once_note` | €0 Care Credit · €0 Dental Check-up Reward (42) | 0 € de Care Credit · 0 € de récompense contrôle dentaire (56) | 0 € Care Credit · 0 € récompense contrôle |
| 02 | Care receipt `line_year/note` | 20% back on the Year (20) | 20 % reversés · année Karmicare (31) | 20 % reversés |
| 02 | sticky bar `credit_checkup` (`main-product.liquid:983`) | 44 | 49 (short form) | full form 63 |
| 02 | sticky bar `stop_year` (`:1073`) | 43 | 51 | |
| 02 | sticky bar `try_once` (`:1087`) | 48 | 53 | |
| 02 | treatment journey `#23` | — arrive resilient, you did the work at home (44) | — en confiance : le travail est fait à la maison (48) | full form in notes |
| 02 | comparison `#18` | Weeks to notice (15) | Des semaines d'attente (22) | |

Other entries in tight places grow less than 30 % or are shorter than the EN.

## Source defects and observations

The B1a ones are carried into `notes`:

- €0.42 is translated as written (0,42 €).
- The compare-table Welcome Kit row points at the old brushes.
- The legacy plan name has stray characters.
- "Full dosep" is translated as the intended "La dose complète".
- Treatment journey `#29` is truncated, so it is held.
- The image alt is reordered so Awake comes first.
- The menu link misspells hydroxyapatite.

**New in B3:**

1. `compare_value#06` (the compare-table Return on Care tooltip) is cut off in EN ("…We believe preven"). The FR completes it with the sentence that `compare_value#08` and both plan tooltips carry, and is flagged `source-defect` so the Admin owner checks the EN value.
2. `compare_value#05` "Return on Care" is admin text without the `never_translate` flag that the same string carries on the template. Held as never-translate.
3. The SLS research card (`card_JeERX6`) carries the nHAp card's "DENTINE TUBULES · OPEN AND OCCLUDED" image badge, with a hyphen on the PDP. Translated as written; the homepage/PDP owners should confirm the badge.
4. Homepage benefit card 07 heading "Focus by day,  calm by night" has a double space. The FR has one.
5. Product FAQ `#54` says "Two seconds, twice a day, and you know". Kept as written; maybe intended, maybe "two minutes".
6. The footer address "Vizierstraat 28, 8000, Belgium" has no city. Kept, with only the country translated.

## Integration notes (for the localization worker)

- **`theme-key` entries**: 72 strings for new keys in `locales/fr.json`.
  - The **26 sticky-bar defaults** in `main-product.liquid` only reach FR after the PDP owner stores them in the template or turns them into keys (B1a handoff).
  - The **Loop strings** (`snippets/loop-widget-standard.liquid`, `assets/loop-widget.js`) are in off-limits files, so the Loop owner integrates them.
- **`locale-present` entries** need nothing: `locales/fr.json` already has them.
- **Selling-plan descriptions** keep their markup and the runtime price spans verbatim. If the theme does not rewrite those spans per locale, FR pages show "€5.90" and "10%" inside French text. That is the same open point as B1a decision 5 (money format).
- **Held entries** register no FR, so Shopify shows the EN. That is correct for names and keys.
- **Card 06 on the homepage** would show a FR heading over EN text until C35 is resolved. Hide or fix the card at integration.

## URL table (batches 01–03)

Handles stay English (no decision to translate them).

| Page | Batches | EN URL | NL URL | FR URL |
|---|---|---|---|---|
| Homepage | 01, 03 | `/` | `/nl` | `/fr` |
| Duo PDP | 02, 03 | `/products/karmicare-biorhythmic-oral-care-system` | `/nl/products/karmicare-biorhythmic-oral-care-system` | `/fr/products/karmicare-biorhythmic-oral-care-system` |
| Header and footer | 03 | every page | every `/nl/…` page | every `/fr/…` page |

Batches 04–08 add their pages to this table when they are translated.

## Pending

| Item | Gate or owner |
|---|---|
| Batches 04–08 | the NL worker's EN inventory on `karmicare/soft-launch-source-copy`; I merge and translate as each lands |
| Astra review of the FR payloads | coordinator, after `worker_done` |
| Claims sign-off: 58 entries `pending-claim-review` | Victor / Clinical Research (B1a decision 3) |
| Claims covered | C02, C12–C14, C20, C21, C23, C24, C27, C30, C32–C34, C36, C37, C40–C45, C50–C54, C60–C67, C70, C80–C83, C90–C92, C95–C99 |
| Offer and EN wording fixes: 18 entries `pending-en-review` | Victor (B1a decisions 1, 4, 6). Each EN change makes its FR entry stale through `en_sha1` |
| Legal review: 7 entries (footer legal text, consent line, legal link labels, "Terms, clauses 10 and 11") | Victor or a lawyer |
| Native French read-through | Victor, or a native reviewer before publishing. FR is a working convention without approved copy, and customer care answers in EN and NL only (B1a decision 2) |
| Rendered FR check | localization worker, preview gate |

## Handoffs

- **Admin owner**: `compare_value#06` is truncated in EN, and `compare_value#05` lacks its never-translate flag (new). The B1a admin handoffs (€0.42, Welcome Kit row, Year sub-line, "dosep", truncated journey line, alt order, menu spelling, legacy plans, "Inflation-proof", "verified by your dentist") all change FR entries once fixed.
- **Homepage / PDP owners**: confirm the SLS card's image badge (new). The rest is as in B1a.
- **Localization worker**: the integration notes above.
- **Loop owner**: 8 of the 9 hardcoded Loop strings have FR in `batch-01` (`theme-key`). The ninth, the "Rendering loop-subscriptions" placeholder, is held.

## Open decisions for Victor

1. **Confirm the proposed FR terms** (table above), above all the plan names *Rythme 60 jours*, *L'année Karmicare*, *Essayer une fois*, plus *offre* for "plan" and *matin/soir* for AM/PM.
   - *Recommendation*: accept them as a set, so the NL/FR terms stay parallel. *offre* matters most, because *formule* is already the word for Awake and Asleep.
2. **Does FR ship?** This repeats B1a decision 2: customer care answers in EN and NL only.
   - *Recommendation*: get one native French read-through of the PDP batch before FR is published. The payloads are ready for it.
3. **Gendered titles.** French job titles are gendered, and the EN gives no gender.
   - **Practitioner titles**: I wrote epicene forms, for example "Pharmacie, thérapie orthomoléculaire, coordination kPNI", "Ex-médecin généraliste" and "spécialiste".
   - **"founder"** on the mission card is held, because *fondateur* and *fondatrice* have no neutral alternative.
   - *Recommendation*: ask each practitioner for their French title when you confirm consent and current titles (45 brief gate 3), and pick the founder form yourself.
4. **French punctuation on held strings.** "Awake:" and "Asleep:" (product FAQ) are held as formula names, so FR pages show "Awake:" without the French space.
   - *Recommendation*: leave them held. The difference is cosmetic, and registering them would mean translating never-translate entries.
5. **Typographic apostrophe.** I used ’ throughout. Dawn's `fr.json` uses `'`.
   - *Recommendation*: keep ’. It is the French standard, and it is safe inside JS strings.

## Re-running

The FR files were generated from the per-entry translation tables of this session and checked with `check.py`. When an EN batch changes, `check.py` names the stale entries (en_sha1 mismatch), and only those need new FR.
