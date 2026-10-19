# B3 report · FR translation payloads (batches 01–08)

Task `task_064a318d44e7`, Orca run `run_32dd5602b983`, branch `karmicare/soft-launch-fr` (from `karmicare/soft-launch-source-copy` at 40b0641). 19 Oct 2026.

## Preflight

| Check | Result |
|---|---|
| `orca status --json` | runtime `ready`, `reachable: true`, connection `connected` |
| `git status --short` / branch | clean tree on `karmicare/soft-launch-fr`, HEAD 40b0641 |
| Model / permission mode | Claude Opus 5.5 (`claude-opus-5-5`) in Claude Code, bypass-permissions mode; every Bash command sandboxed |
| `AGENTS.md` | Read. README, `docs/pdp/RUNBOOK.md` and `docs/design-tokens/` are not in this repo, so COMMON-RULES and BRIEF apply. |
| Network, Admin, theme files | None used: no store request, no Figma call, no Admin write, no file written outside `docs/localization/fr/`. |
| Astra review | The coordinator dispatches it after `worker_done` (coordinator reply, 19 Oct). I started no Codex or other agent. |

## Commits

| Commit | What |
|---|---|
| `b89ec56` | `batch-02-pdp.json` (477 entries) and `check.py` |
| `b782e4d` | `batch-01-homepage.json` (221) |
| `1a54eb8` | `batch-03-header-footer.json` (41) |
| `09ff34e`, `e290026` | First report and one homepage wording fix |
| `910e309` | Merge of `karmicare/soft-launch-source-copy` 42f5f12: EN batches 04–08 |
| `135ee5b` | `batch-04-legal.json` (974) |
| `6ad67b6` | `batch-05-products.json` (77), `batch-06-content-pages.json` (21), `batch-08-system.json` (46) |
| `dfec9ed` | `batch-07-collections-blog.json` (709) |
| `933c1fb` | Merge of the claims review for batches 05–07 (5e4f426) and the NL payloads |
| `a440834` | Batches 05–07 rebuilt on the reviewed claim statuses |
| this commit | This report |

### File format

Each `docs/localization/fr/<batch>.json` has a batch header and one entry per source entry.

- **Header**: `source_digest` (the batch digest translated from), `source_entries`, `counts`, `flag_counts`.
- **Entries**, in source order: `{id, resource_type, file_or_handle, key_path, en, en_sha1, fr, status, flags, notes, source_status, claims?}`.
  - `en_sha1` equals the source entry's `sha1`, so an EN change makes only that entry stale.

`status` is the delivery channel, and `flags` holds the review gates:

| status | Meaning | Registered by |
|---|---|---|
| `translated` | Template or section-group setting | Localization worker (theme translations) |
| `admin` | Product, metafield, metaobject, selling plan, page, policy, article, collection, menu, shop or app text | Admin owner (Shopify translation resources) |
| `theme-key` | Hardcoded Liquid/JS text | Localization worker, as a new key in `locales/fr.json` |
| `locale-present` | Dawn key already in `locales/fr.json`; `fr` is copied from there | Nobody: nothing to do |
| `held` | `fr: null`, reason in `notes` | Nobody: Shopify falls back to EN |

| flag | Meaning |
|---|---|
| `pending-claim-review` | Carries a needs-review claim (CLAIMS-REVIEW.md, batches 01–03 and the 05–07 review). Translated as written. |
| `legal-review` | Legal text. Needs Victor's or a lawyer's review before publishing. |
| `pending-en-review` | The EN itself is under review. Translated as written. |
| `fit-risk` | Longer than the EN in a tight spot. `fr` is the short form; `notes` gives the full one. |
| `source-defect` | Defect in the EN. `notes` says how the FR handles it. |
| `gendered-title` | French would need a gender. Written in an epicene form. |
| `wording-adapted` | A literal translation would use a banned word. `notes` gives the wording used. |
| `not-rendered` | Disabled block. |

**Mapping to the NL files.** The NL worker puts the review gates in `status` (`pending-claim-review`, `legal-review`) and calls the Dawn keys `dawn-nl`. FR keeps the channel in `status` and the gates in `flags`; FR `locale-present` matches NL `dawn-nl`. The localization worker can read both from the same fields (`status`, `flags`, `notes`).

## Counts

| Batch | Source digest | Entries | translated | admin | theme-key | locale-present | held |
|---|---|---:|---:|---:|---:|---:|---:|
| `batch-02-pdp` | `03dd18b9…` | 477 | 141 | 249 | 36 | 15 | 36 |
| `batch-01-homepage` | `b685b73d…` | 221 | 170 | 2 | 26 | 2 | 21 |
| `batch-03-header-footer` | `e17cadb5…` | 41 | 6 | 11 | 10 | 9 | 5 |
| `batch-04-legal` | `83fed281…` | 974 | 143 | 481 | 0 | 0 | 350 |
| `batch-05-products` | `5ab678a9…` | 77 | 16 | 57 | 0 | 0 | 4 |
| `batch-06-content-pages` | `f78c391a…` | 21 | 0 | 19 | 0 | 0 | 2 |
| `batch-07-collections-blog` | `9597904c…` | 709 | 1 | 591 | 0 | 0 | 117 |
| `batch-08-system` | `306f141f…` | 46 | 3 | 7 | 0 | 36 | 0 |
| **Total** | | **2,566** | **480** | **1,417** | **72** | **62** | **535** |

Every source entry is covered: 2,031 carry FR and 535 are held. The full digests are in each file's header and match `docs/source-copy/digest.py` (all eight `ok`).

| Flag | 01 | 02 | 03 | 04 | 05 | 06 | 07 | 08 | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| legal-review | 1 | 1 | 5 | 956 | 0 | 0 | 0 | 0 | 963 |
| pending-claim-review | 30 | 27 | 1 | 0 | 14 | 4 | 243 | 0 | 319 |
| pending-en-review | 7 | 9 | 2 | 3 | 1 | 0 | 0 | 0 | 22 |
| source-defect | 2 | 7 | 1 | 3 | 9 | 0 | 0 | 0 | 22 |
| wording-adapted | 3 | 14 | 2 | 0 | 3 | 7 | 0 | 1 | 30 |
| gendered-title | 7 | 14 | 0 | 0 | 0 | 0 | 0 | 0 | 21 |
| fit-risk | 3 | 8 | 0 | 0 | 0 | 0 | 0 | 0 | 11 |
| not-rendered | 0 | 6 | 0 | 0 | 1 | 0 | 0 | 0 | 7 |

The blog's `wording-adapted` changes are described in each entry's notes and in the batch-07 commit, but not flagged one by one.

### Held (535)

| Batch | Reason | Count | What |
|---|---|---:|---|
| 04 | legacy | 350 | `/pages/privacy` (269), `/pages/terms-and-conditions` (76), `/pages/consumer-rights` (5): pre-2.0 legal pages, held in NL/FR (INVENTORY.md) |
| 07 | unsupported claim (05–07 review) | 107 | Blog blocks such as "prevents tooth decay", "ingesting poison", fluoride and IQ, NASA history |
| 01–03 | never-translate | 54 | Formula, practitioner and brand names, citations, INCI, `nHAp`, `SCCS/1677/25`, Subscription Names, Return on Care |
| 07 | empty | 9 | Empty article excerpts (`summary_html`) |
| 05 | unsupported claim | 4 | "Unlike fluoride-based oral hygiene products that disturb your wake/sleep cycles…" in the Awake/Asleep 2.0 descriptions and meta descriptions |
| 01–02 | unsupported claim | 3 | C35 benefit card 06; C84/C85 Sietske Hamelink quote on both templates |
| 01 | needs approved copy | 2 | Homepage FAQ rows 2 and 3 |
| 06 | unsupported claim | 2 | "NASA's favorite supplement for oral health" (`/pages/nhap-technology`) |
| 02 | source defect | 1 | Treatment journey `#29` stops mid-phrase |
| 02 | gendered title | 1 | Mission card "founder" (decision 3) |
| 01 | integration | 1 | "Rendering loop-subscriptions": the theme tests for this exact text |
| 07 | competitor names | 1 | SLS article `b035` names Colgate, Biotene, Sensodyne Pronamel and Tom's of Maine |

## Evidence

**`python3 docs/localization/fr/check.py`: exit 0, 0 errors, 17 warnings.** For every file it checks:

- the batch digest against the source, and `en_sha1` against `sha1(en)`;
- one entry per source id, in order;
- the status and flag vocabulary;
- that EN and FR carry the same HTML tags, Liquid, `[tokens]`, `&nbsp;` count and runtime price spans;
- that the selling-plan IDs are unchanged;
- French spacing and apostrophes.

For entries that are not legal, it also flags banned words, claim verbs and *tu* forms.

**The 17 warnings, each checked by hand:**

- **Batches 01–02 (9):**
  - 8 × the noun *prévention*: the EN "Prevention" in the check-up and plan tooltips and the compare table, and C33.
  - 1 × *produits cosmétiques*: the official portal name.
- **Batch 07 (8):**
  - *produit* or *produits*, five of them the verb *produire* and three *produits chimiques/ménagers* (chemicals, household products).
  - *prévenir les caries*: a statement about fluoride, not a Karmicare claim.
  - *guérison*: the EN "healing cycles", a needs-review claim kept as written.

**Other checks:**

- `python3 docs/source-copy/digest.py`: all eight batches `ok`.
- `shopify theme check --fail-level error`: **exit 0**. 244 files inspected, 21 offenses, all warnings. No theme file changed and `.theme-check.yml` is untouched.
- Rendered check: none possible yet. It waits for integration by the localization worker and the preview gate.

## Conventions applied

- **Register**: warm *vous*. No *tu*.
- **Gender**:
  - No inclusive dot, and no gendered adjective addressed to the reader ("Le duo ne vous convainc pas ?", "vous bénéficiez d'une protection…").
  - Masculine plural kept as the generic for mixed groups.
- **Typography**:
  - U+00A0 before `: ; ! ? € % »` and after `«`; U+202F as thousands separator.
  - Decimal comma, « » quotation marks, typographic ’.
  - Times stay 06:40 / 22:00.
- **Exceptions**: the `ID: label` lines of `custom_button_text_by_plan`, and the runtime price spans in Loop plan descriptions (`€5.90`, `10%`, `€21`), kept verbatim.
- **Stay English**: Awake, Asleep, Care Credit, Return on Care, Leave-on, Karmicare, the KARMICARE™ legal product name, INCI, citations, nHAp, SCCS, Ph. Eur.
- **Awake before Asleep**: the evening-first image alt is reordered in FR.
- **Banned words**:
  - In customer copy, *produit, tube, acheter/achat, utiliser* are avoided ("Découvrir" for Shop, *soins*, *choisir*, *appliquer*).
  - "toothpaste" (*dentifrice*) appears only at first-contact moments: titles, SEO titles, image alts, the first mention in an SEO description and the first mention in a page body. After that the FR says *formule*, *soin* or *soin bucco-dentaire*, even where the pre-2.0 blog and the old product texts repeat "toothpaste" (R3 F7; the earlier "FR follows the EN" exception is withdrawn).
  - **Legal text is the exception.** It is translated faithfully and completely, so *produits*, *utilisation*, *achat* and *traiter (des données)* stay where the law or the EN needs them.
- **Claims**: EU cosmetic verbs in Karmicare copy. Needs-review claims are translated as written, and the reviewed unsupported ones are held.
- **Legal FR (Belgian)**:
  - Terms: *droit de rétractation*, *garantie légale de conformité*, *garantie satisfait ou remboursé*.
  - "WER" becomes CDE (the French abbreviation of the same code); "WER/CDE" is kept where the EN has both. RGPD, CIR 92, SPF Finances, RPM, *tribunal de l'entreprise de Gand, division Bruges*.
  - The *Service de Médiation pour le Consommateur*, the *Centre Européen des Consommateurs* and the *Autorité de protection des données* use their official French names.
  - "Clause N" becomes *Article N*, which matches "Conditions, articles 10 et 11" in batch 01/02.
  - The model withdrawal form uses the official French wording of Directive 2011/83/EU, Annex I(B).
  - Company name, enterprise, VAT and EORI numbers, IBAN/BIC, emails, phones, periods and amounts are exactly as in EN. In addresses, street, number and postcode are kept, and city and country names are in French (Bruxelles, Belgique; Bruges is the same).
  - Link targets are kept as in EN, for example `consumerombudsman.be/en` (a `/fr` version exists).
- **Policy pages**: 314 of the Shopify policy segments are the 2.0 page text cut into blocks. They reuse the page FR word for word, so the two copies of the legal text cannot drift.

## Proposed terms (for Victor, one pass)

No approved FR copy exists, so every FR term is proposed.

**From the glossary FR column, applied as written:**

| EN | FR |
|---|---|
| Plan names | *Rythme 60 jours*, *L'année Karmicare*, *Essayer une fois* |
| Welcome Kit | *kit de bienvenue* |
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
| Science terms | as in the glossary |

**Terms I had to decide:**

| EN | FR (proposed) | Why |
|---|---|---|
| plan | *offre* | *formule* would clash with "two formulas" |
| subscription | *abonnement* | |
| your plan | *votre adhésion* | |
| the Year (running text) | *l'année Karmicare* | |
| AM/PM | *matin/soir* | |
| Begin/Start CTAs | infinitive *Commencer…* | Header *COMMENCER* |
| Care Credit back | *Care Credit reversé* | |
| Free (price) / FREE (kit) / Free (shipping) | *Gratuit* / *OFFERT* / *Offerte* | |
| with first order | *1re commande* | |
| one-time (compare table) | *en une fois* | |
| One time Purchase | *Commande unique* | |
| Read more / Read less | *Lire la suite* / *Réduire* | |
| Trusted by professionals | *La confiance des professionnels* | |
| Care that comes back | *Le soin qui vous revient* | |
| evidence pack | *dossier scientifique* | |
| RCT / SEM / CI | *ECR / MEB / IC* | |
| Shop Karmicare / Shop Now | *Boutique Karmicare* / *Découvrir* | |
| Why use hydroxapatite | *Pourquoi choisir l'hydroxyapatite* | |
| Legal page titles | *Conditions générales*, *Politique de confidentialité*, *Droits des consommateurs* | Batch-03 link texts |
| Banner and policies | *Charte des droits des consommateurs et de transparence*; *Politique de remboursement / d'expédition / de résiliation*, *Coordonnées*, *Mentions légales* | |
| LEGAL eyebrow | *MENTIONS LÉGALES* | |
| customer portal | *espace client* | |
| Founder (blog attributions) | *à l'origine de Karmicare* | Neutral |
| my partner (founder quotes) | *la personne qui partage ma vie* | Neutral |
| News (blog) | *Actualités* | |
| Health Rewards (old product.json card) | kept in English, as written | |

## Fit risks (25 entries; textual triage, not measured overflow)

| Entry | EN chars | FR chars | Fallback |
|---|---:|---:|---|
| Hero, two-formulas and benefits button "BEGIN YOUR 60-DAY RITUAL" | 24 | 31 | COMMENCER LE RITUEL |
| Buy box `welcome_kit_title` | 30 | 31 | Glossary long form (47) if there is room |
| Buy box `try_once_note` | 42 | 56 | 0 € Care Credit · 0 € récompense contrôle |
| Care receipt `line_year/note` | 20 | 31 | 20 % reversés |
| Sticky bar `credit_checkup` | 44 | 49 (short form) | Full form 63 |
| Sticky bar `stop_year` | 43 | 51 | |
| Sticky bar `try_once` | 48 | 53 | |
| Treatment journey `#23` | 44 | 48 | Full form in notes |
| Comparison `#18` "Weeks to notice" | 15 | 22 | |
| Buy and sticky button "Begin Now" (PDP and `product.json`, 4 entries) | 9 | 20 | exact FR kept (R3 F8) |
| Sticky bar `cta_rhythm` (`main-product.liquid:1018`) | 24 | 31 | exact FR kept (R3 F8) |
| Sticky bar `kit` (`:1049`) | 37 | 54 | exact FR kept (R3 F8) |
| Sticky bar `stop_rhythm` (`:1067`) | 21 | 34 | exact FR kept (R3 F8) |
| Plan name "ships every 60 days" (2 selling plans) | 19 | 28 | exact FR kept (R3 F8) |
| Compare table `#14` "Try Once" | 8 | 16 | exact FR kept (R3 F8) |
| Compare table `#25` "Begin 60-Day Rhythm" | 19 | 28 | exact FR kept (R3 F8) |
| Compare table `#11` "Skip, pause or cancel" | 21 | 43 | full meaning kept (R3 F3) |
| Research card `card_JeERX6` heading (homepage and PDP) | 44 | 72 | full meaning kept (R3 F4) |

Batch 05 also contains buy-button and sticky-button labels requiring fit review; legal navigation labels can expand too. Character counts identify risks, while rendered French fit remains pending integration and preview.

## Source defects and observations

The B1a defects (€0.42, the Welcome Kit row, legacy plan names, "dosep", the truncated journey line, the evening-first alt, the menu spelling) are carried in `notes`.

**New in B3:**

1. `compare_value#06` is cut off in EN ("…We believe preven"). The FR completes it with the sentence `compare_value#08` carries.
2. `compare_value#05` "Return on Care" lacks the never-translate flag. Held.
3. The SLS research card carries the nHAp card's "DENTINE TUBULES" badge.
4. The homepage card 07 heading has a double space.
5. The 2.0 T&C (clause 2) and the Terms of Service policy link to `/en/pages/terms-and-conditions`, the **legacy** handle; the 2.0 text lives at `/pages/terms-and-conditions-1`. Four policy pages (shipping, contact, legal notice, cancellation) link the same legacy URL. The Admin owner should fix the link or redirect the old handle, then the FR links to `/fr/pages/terms-and-conditions-1`.
6. The SEO titles of the three 2.0 legal pages start with "New" ("New Privacy Policy – KARMICARE"). Translated as written.
7. The privacy policy names the footer link "Cookie settings"; the footer shows "Cookie preferences". The FR names the FR footer link.
8. The admin bodies of `/pages/new-consumer-rights` and `/pages/terms-and-conditions-1` hold only "Date:". The page text comes from the template.
9. The legacy evening brush alt is in Dutch ("Karmicare Avond Tandenborstel").
10. Old product texts have typos ("dispurge", "nurished", "Awake of Asleep", "every 6 month") and a leading space in a plan name. The FR translates the intended meaning.
11. Several meta descriptions are the description cut at about 320 characters. The FR translates to the end of the sentence.
12. The blog title `nano-hydroxyapatite` SEO has "Hydroxapatite". The SLS article names four competitors (held).
13. The footer address has no city after 8000 (kept).

## Integration notes (for the localization worker)

- **`theme-key` (72)**:
  - The 26 sticky-bar defaults in `main-product.liquid` need the PDP owner to store them or make them keys.
  - The 8 Loop strings are in off-limits files, so the Loop owner integrates them.
- **`locale-present` (62)**: nothing to do; `locales/fr.json` already has them.
- **`admin` (1,417)**:
  - Long bodies (pages, policies, articles, product descriptions) are block segments (`#bNNN`). Join them back in order.
  - The page and policy segments follow the 2.0 legal page text.
  - The runtime price spans in the plan descriptions stay EN-formatted unless the theme rewrites them, as in B1a decision 5.
- **Held**: no FR is registered, so EN shows.
  - The homepage benefit card 06 would show a FR heading over EN text until C35 is resolved.
  - Blog articles would show EN paragraphs where blocks are held. **Recommendation: do not publish the FR blog until the claims are resolved** (see decision 2).

## URL table

Handles stay English (no decision to translate them). The NL and FR prefixes come from the live `/nl/` and `/fr/` sitemaps.

| Page | Batch | EN URL | NL URL | FR URL | Note |
|---|---|---|---|---|---|
| Homepage | 01, 03 | `/` | `/nl` | `/fr` | |
| Duo PDP | 02, 03 | `/products/karmicare-biorhythmic-oral-care-system` | `/nl/products/karmicare-biorhythmic-oral-care-system` | `/fr/products/karmicare-biorhythmic-oral-care-system` | |
| Contact | 04 | `/pages/contact` | `/nl/pages/contact` | `/fr/pages/contact` | |
| Consumer rights (2.0) | 04 | `/pages/new-consumer-rights` | `/nl/pages/new-consumer-rights` | `/fr/pages/new-consumer-rights` | legal-review |
| Privacy policy (2.0) | 04 | `/pages/privacy-policy` | `/nl/pages/privacy-policy` | `/fr/pages/privacy-policy` | legal-review |
| Terms and conditions (2.0) | 04 | `/pages/terms-and-conditions-1` | `/nl/pages/terms-and-conditions-1` | `/fr/pages/terms-and-conditions-1` | legal-review |
| Consumer rights (legacy) | 04 | `/pages/consumer-rights` | `/nl/pages/consumer-rights` | `/fr/pages/consumer-rights` | held (legacy) |
| Privacy (legacy) | 04 | `/pages/privacy` | `/nl/pages/privacy` | `/fr/pages/privacy` | held (legacy) |
| Terms (legacy) | 04 | `/pages/terms-and-conditions` | `/nl/pages/terms-and-conditions` | `/fr/pages/terms-and-conditions` | held (legacy) |
| Shopify policies | 04 | `/policies/privacy-policy`, `terms-of-service`, `refund-policy`, `shipping-policy`, `contact-information`, `legal-notice`, `subscription-policy` | `/nl/policies/…` | `/fr/policies/…` | legal-review |
| Complete Hygiene Kit | 05 | `/products/complete-hygiene-kit` | `/nl/products/complete-hygiene-kit` | `/fr/products/complete-hygiene-kit` | |
| Morning / Evening Toothbrush (legacy) | 05 | `/products/morning-toothbrush`, `/products/evening-toothbrush` | `/nl/products/…` | `/fr/products/…` | |
| Morning / Evening Toothbrush 2.0 | 05 | `/products/morning-toothbrush-2-0`, `/products/evening-toothbrush-2-0` | `/nl/products/…` | `/fr/products/…` | |
| Whitening Charcoal Floss | 05 | `/products/whitening-charcoal-dental-floss` | `/nl/products/whitening-charcoal-dental-floss` | `/fr/products/whitening-charcoal-dental-floss` | |
| Awake / Asleep 2.0 | 05 | `/products/awake-morning-toothpaste-2-0`, `/products/asleep-evening-toothpaste-2-0` | `/nl/products/…` | `/fr/products/…` | 4 blocks held |
| Content pages | 06 | `/pages/why-karmicare`, `/pages/why-use-hydroxyapatite-toothpaste`, `/pages/why-stop-using-fluoride-toothpaste`, `/pages/nhap-technology`, `/pages/articles` | `/nl/pages/…` | `/fr/pages/…` | nhap body held |
| Collections | 07 | `/collections/biorhythmic-oral-hygiene-kit`, `/collections/vgbc2025`, `/collections/karmicare-collection` | `/nl/collections/…` | `/fr/collections/…` | |
| Blog and 9 articles | 07 | `/blogs/news`, `/blogs/news/<handle>` | `/nl/blogs/news/…` | `/fr/blogs/news/…` | 117 blocks held |
| System pages | 08 | `/search`, `/pages/<missing>` (404), `/collections`, `/collections/all`, `/cart` | `/nl/…` | `/fr/…` | |
| Header and footer | 03 | every page | every `/nl/…` page | every `/fr/…` page | |

## Pending

| Item | Gate or owner |
|---|---|
| Astra review of the FR payloads | coordinator, after `worker_done` |
| Legal review of 963 legal entries | Victor or a lawyer, before any FR legal page is published |
| Claims sign-off: 319 `pending-claim-review` entries; 116 held as unsupported (3 in 01–02, 113 in 05–07) | Victor / Clinical Research |
| EN wording fixes: 22 `pending-en-review` entries, plus the defects above | Victor and the Admin owner |
| Native French read-through | Victor or a native reviewer, before publishing; customer care answers in EN and NL only (B1a decision 2) |
| Rendered FR check | localization worker and preview gate |

## Handoffs

- **Admin owner**:
  - Fix or redirect the legacy T&C link (`/en/pages/terms-and-conditions`) in the 2.0 T&C and five policy pages.
  - Fix the truncated `compare_value#06`.
  - Give the legacy evening brush image an English alt.
  - Consider dropping "New" from the 2.0 legal SEO titles.
  - Remove or rewrite the blog block that names competitors.
  - The B1a admin handoffs still stand.
- **Homepage / PDP owners**: the SLS card badge, plus the B1a items.
- **Localization worker**: the integration notes above.
- **Loop owner**: 8 Loop strings in batch 01 (`theme-key`).

## Open decisions for Victor

1. **Confirm the proposed FR terms** (table above), above all the plan names, *offre* for "plan" and *matin/soir* for AM/PM.
   - *Recommendation*: accept them as a set, so NL and FR stay parallel.
2. **Does FR ship, and which parts first?**
   - The PDP, homepage, header/footer, products and system pages are ready for a native read-through.
   - The legal pages need legal review.
   - The pre-2.0 blog is heavy with claims: 243 needs-review blocks translated, 117 held.
   - *Recommendation*: publish FR in that order, and keep the FR blog unpublished until its claims are rewritten in EN.
3. **Gendered titles.**
   - **Practitioner titles** are written in epicene forms.
   - **The mission card "founder"** is held. *À l'origine de Karmicare*, already used in the blog quotes, would be a neutral alternative.
   - *Recommendation*: ask each practitioner for their French title at the consent check (gate 3), and choose the founder wording.
4. **Legacy legal pages** (`/pages/privacy`, `/pages/terms-and-conditions`, `/pages/consumer-rights`): held in FR.
   - *Recommendation*: redirect them to the 2.0 pages, so no FR visitor lands on the untranslated pre-2.0 text.
5. **Customer care languages.** The FR legal pages state "Le service client répond en anglais et en néerlandais", as the EN does.
   - *Recommendation*: keep it, unless French customer care is added before FR ships.
6. **Typographic apostrophe.** I used ’ throughout; Dawn's `fr.json` uses `'`.
   - *Recommendation*: keep ’.

## Re-running

When an EN batch changes, `check.py` names the stale entries (en_sha1 mismatch), and only those need new FR.
