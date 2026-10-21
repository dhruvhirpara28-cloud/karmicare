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
| `ffbe9b4` | This report (reviewed by Astra) |
| `f85fe81` … `5f8bf1f` | R3 fixes F1–F10, one commit per finding (section below) |
| `71b3c5a`, `8bc3d96` | Merge of source-copy `2194ef3` (R1) and the FR that follows it |
| `85ad0a7` | Merge of source-copy `fb46dd1` (R2 source changes, NL R2 payloads, B4 theme keys) |
| `841e05b` … `7760231` | R2 mirror (section below) |
| `2aeb6af` | Merge of source-copy `a0dee86` (R6 additions, NL R6 payloads, offline registration plan) |
| `0a0a182`, `c12aed7` | R6 mirror (section below) |

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

## R3 fixes

Astra review `docs/runtime-review/B3-FR-ASTRA.md` (verdict: pass with fixes) at `ffbe9b4`. All ten findings are applied, one commit each, with the reviewer's exact FR where one was given. No held entry was translated and no hold was added or released (0 differences in the held set against `ffbe9b4`); 146 FR values changed.

| Finding | Commit | What changed |
|---|---|---|
| F1 · evening brush whitening | `f85fe81` | Four batch-05 entries (evening brush and evening brush 2.0, SEO description and body): « Cela aide vos dents à retrouver leur blancheur nacrée, sans polissage ni blanchiment. » `pending-claim-review` kept. |
| F2 · blog qualifiers | `45be545` | Nootropics `b062` « pour vous aider à améliorer… », nano-hydroxyapatite `b053` « susceptibles de provoquer », SLS `b012` and `b028` « pour lesquelles vous pourriez souhaiter… » (b028 also « les soins contenant du SLS »). Flags kept. |
| F3 · skip, not postpone | `b19b89a` | `compare_value#11` « Sauter une livraison, suspendre ou résilier », plus `fit-risk`. |
| F4 · canker-sore duration | `6c534cd` | Research card `card_JeERX6` heading on the homepage and the PDP: « Sans SLS, les aphtes étaient moins nombreux et duraient moins longtemps. », plus `fit-risk` (72 vs 44 chars). |
| F5 · legal metadata | `668d3bf` | `legal-review` on the 16 legal SEO fields (ten translated, six held legacy). FR values unchanged. Batch 04 has 972 `legal-review` entries; the total is 979. Only the contact page's two fields stay outside. |
| F6 · check.py gates | `d376bd3` | The checker enforces source holds, claim and legal gates, delivery channel, resource addressing, batch presence and `flag_counts` (see Evidence). `--self-test` runs 12 in-memory mutations, the reviewer's four plus eight more, and all fail as expected. The reviewer's four mutations written to scratch copies on disk each exit 1. |
| F7 · first-mention rule | `23bf6b1` | The reviewer's exact fixes, plus about 120 blog and content-page edits. *dentifrice* now appears only in titles, SEO titles, image alts, the first SEO-description mention and the first body mention per page. Later mentions read *formule*, *soin* or *soin bucco-dentaire*, with agreement fixed. No non-legal string repeats it. The REPORT exception is withdrawn. Legal text, INCI headings and PDP titles/alts are untouched. |
| F8 · fit coverage | `29d20e5` | `fit-risk` on the 11 listed entries, exact FR kept: four « Commencer maintenant » buttons, three sticky lines, two plan names, compare cells `#14` and `#25`. `fit-risk` now covers 25 entries. The fit table is extended and the batch 04–08 statement is replaced by the reviewer's wording. Note fallbacks use U+00A0. |
| F9 · email placeholder | `85f60ce` | `footer.liquid:667` is `you@example.com` again. |
| F10 · English labels in legal prose | `5f8bf1f` | Every lowercase *airless* in the 12 listed entries now reads « sans entrée d'air », and « soft opt-in » reads « exception applicable aux clients existants » in the two listed entries. Policy segments are regenerated from the page text, so both copies match. |

**Where I departed from the exact wording:**

- **F7**: I applied the reviewer's blog fix `b027` to « le dentifrice Awake » as well as « le dentifrice Asleep », because the article's first body mention is in `b014`.
- **F10**: in the two headings, *hermétique* moves before the new words (« Protection hermétique sans entrée d'air », « Emballage hermétique sans entrée d'air »), so it qualifies the noun rather than *air*. Everywhere else the substitution is exact.

**Verification after R3:**

- `check.py --self-test`: exit 0, 0 errors, 17 warnings, 0 mutations uncaught.
- `digest.py`: all eight batches `ok`.
- `shopify theme check --fail-level error`: exit 0 (244 files, 21 warnings, no errors).

**After R3 (coordinator follow-ups, 19 Oct):**

- `58755f7` · NL review R2 F1: the Awake and Asleep 2.0 sleep/wake body lines (`body_html#b002`) are held. Note: "unsupported-claim: sleep/wake effect; same hold as this resource's seo.description".
- `71b3c5a` · merge of `karmicare/soft-launch-source-copy` at `2194ef3` (source-copy R1 fixes). `3129f1d` (the B4 theme-key map) is not merged.
- `8bc3d96` · FR follows that merge:
  - **Four new batch-01 runtime strings**: « . Heure locale actuelle. », « / an », « Se renouvelle » and « {{ amount }} / brossage ».
    - For « Se renouvelle », the note says to key the whole line « Se renouvelle tous les {{ days }} jours », because the FR plan name defeats the widget's 'ships' regex.
  - **Re-derived claim gates**: `pending-claim-review` added on the C60–C64 and C68 result lines (homepage and PDP) and on the C46, C93 and C94 metafields. The total is now 335.
  - **Card 06**: the heading is now held with its text, because C35 covers it.
- Batch-01 digest is now `a09219ae`. `check.py --self-test` exits 0 (0 errors, 12/12 caught), `digest.py` reports all eight `ok`, and Theme Check exits 0 (245 files, 21 warnings).
- **For the B4 localization worker**: `docs/localization/theme-keys.json` was refreshed from FR at `d376bd3`. The FR theme-key values changed since then (R3 F7, F9 and the four new strings), so run `theme_keys.py refresh` before `write`.

**Not changed:** the reviewer's source-owned issues and release limits stay with their owners. These are the €0.42 cell, the 2–4 applications in the brush texts, the Asleep 2.0 "helps you fall asleep" line, « les soulager » in the headaches article (do not release either version), the truncated EN SEO strings, the legacy T&C links and the URL manifest to expand before page-by-page QA.

## R2 mirror

Task `task_386825779698`, brief B3-R2, 20 Oct 2026. The NL review (R2, verdict FAIL) changed the EN source. `docs/source-copy/CHANGES-R2.md` at source-copy `fb46dd1` lists every source change since `2194ef3`, and FR now follows all of it. No held entry was translated and no hold was released: the held set is the same 538 ids as at `c7aed28`.

| Preflight | Result |
|---|---|
| `orca status --json` | runtime `ready`, `reachable: true`, connection `connected` |
| `git status --short` / branch | clean tree on `karmicare/soft-launch-fr`, HEAD `c7aed28` |
| Model / permission mode | Claude Opus 5.5 (`claude-opus-5-5`), auto mode; every Bash command sandboxed; no subagents |

| CHANGES-R2 | Commit | FR result |
|---|---|---|
| Merge | `85ad0a7` | `karmicare/soft-launch-source-copy` at `fb46dd1`, no conflicts. It also brings B4's theme-key map and the FR theme keys built from `c7aed28` (`locales/*.json`, keyed sections). I did not edit them. |
| §1 new entry | `841e05b` | `admin:page:nhap-technology:body_html#b000`, before `#b001`: « Découvrez le monde fascinant de la nano-hydroxyapatite et pourquoi votre dentifrice en a besoin<br><br> ». This is the FR of the same EN article title, plus the block's `<br><br>`. `admin`, `pending-claim-review`. Batch 06 has 22 entries, digest `3dee3b56341f…`. It is the page's first body mention, so *dentifrice* stays (R3 F7 rule). |
| §2 holds | `841e05b` | SLS `#b035` was already held in FR. Its note now gives NL's reason: "needs-approved-copy: competitor names prohibited … EN owner must supply compliant source". The two 2.0 sleep/wake lines (`58755f7`) are confirmed: the source now carries `claim_status: unsupported`, and the FR note cites the source basis. |
| §3 reclassified | `841e05b` | All 16 are `pending-claim-review`, with the FR text unchanged. The 4 C100 entries carry `claims: ["C100"]`, and `product:main/highlights_slider_9wAjAb/text_1` has source status `needs-review`. |
| §4 notes | `ea017a9`, `c435196` | Heading 4.1 already read « 4.1 Présomption de conformité de deux ans » in the consumer-rights template and refund `#b065`: a presumption of conformity, as written. The notes now say so, and `legal-review` stays. Nano-hydroxyapatite `#b036` keeps « biomatériau organique » and stays `pending-claim-review`. |
| §5 metadata | `841e05b` | No FR action. The build now checks that each `claim_status` on a claim-bearing entry equals the strictest status of its claims. All 88 agree, so no second note or hold is added. |
| §6 F4 hedges | `c435196` | SLS `#b056` now reads « pour que vous puissiez obtenir en toute sécurité … Le charbon vous aidera à enlever les taches … que votre brosse à dents peut manquer » ("can safely", "will help lift", "may miss"). SLS `#b028` already said « vous pourriez souhaiter éviter les soins » (R3 F2), and `#b036` keeps "organic". |
| §6 F6 brand words | checked | No FR value names a competitor. The named NL fixes were already in FR: the morning-brush bodies say « notre formule » and « la formule Awake/Asleep », the three "Used by" lines say « Adopté par », nootropics `#b012`, `#b051`, `#b064` say « au quotidien », and fluoride `#b016` says « à leurs formules ». |
| §6 F7 fit | `c435196` | `fit-risk` on the named strings that grow in FR: both research buttons (30 → 31), the PDP shipping value (11 → 16), the end-CTA chip (21 → 29) and comparison `#23` (18 → 22); `#18` was already flagged. Also on their same-EN twins (homepage shipping value, buy-box chip) and on the 7 trust-row chips in the same rows. That is 14 entries, 39 in total. The fit table has a Kind column now. |
| §6 F8 addresses | `ea017a9` | 33 address spans in 29 entries used French forms (Bruxelles, Belgique, boîte 1). All are back to the EN form; legal labels stay French (Tél., TVA, « À l'attention de »). The FR build applies one table of six address strings, so the official French forms can return if Victor allows them (decision 7). |
| §6 F9 harmonisation | checked | FR has one value per EN string (the build enforces it), so no identical-EN group differs. The model-form sentence is identical in terms `#b155`, refund `#b114` and consumer-rights `content_section_at3pLy`, with the EN's 4 `(*)` markers. The "unopened contract" sentence has one form in all four places. |
| §6 F10 never-translate | checked | Every never-translate entry is held, Facebook and Instagram included (since B3). |
| §6 H1–H7, S1, S2 | `987f6fb` | `check.py` already enforced H1–H7. It now also checks S1 (every EN postal address appears unchanged in the FR, with the NL pattern) and S2 (the `(*)` count). Two new self-test mutations prove them, and run on the `841e05b` files S1 reports the 33 spans. |
| R6 addendum (coordinator) | `7760231` | From R6-01, source gate follows on the source branch: wellness `#b081` is `pending-claim-review`, translation kept. R6-02, one sweep of every FR body in batches 05–07: *dentifrice* appears once per page, at the first body mention. The only commodity word in ordinary copy was SLS `#b015` « produits ménagers », now « nettoyants ménagers ». Kept: the verb *produire* and *sous-produit* (nano-hydroxyapatite `#b094`, `#b101`, nootropics `#b054`, fluoride `#b049`), « produits chimiques » (a chemistry term, `#b048`) and the CPNP portal's official name (PDP FAQ `#60`). R6 W1 later replaced *sous-produit* and « produits chimiques » (R6 mirror). |

**New totals:** 2,571 entries, 2,033 with FR, 538 held. `legal-review` 979, `pending-claim-review` 353, `fit-risk` 39, `pending-en-review` 22.

**Not applied:** nothing in CHANGES-R2. The heading 4.1 and "organic" items need no FR change until their owners rule. Since `c7aed28`, 31 FR values changed and 1 entry was added; no `theme-key` value changed. 13 of the changed values are template settings (the footer compliance line and 12 legal template sections, all addresses), which the localization worker registers.

**Verification:**
- `python3 -I docs/source-copy/digest.py`: exit 0, all eight `ok` (batch 06: 22 entries, `3dee3b56341f67b113dcd59eb85d3a2e3f21d628`).
- `python3 -I docs/localization/fr/check.py --self-test`: exit 0, 0 errors, 16 warnings, 14/14 mutations caught.
- `shopify theme check --fail-level error`: exit 0 (246 files, 21 warnings). The merge brought theme and locale files; my FR commits touch only `docs/localization/fr/`.

## R6 mirror

Task `task_2dcd85e98542`, brief B3-R6, 20 Oct 2026. The NL re-review R6 (`docs/runtime-review/B2-NL-R6-ASTRA.md`, pass with fixes) led to one more source change set: "R6 additions" at the end of `docs/source-copy/CHANGES-R2.md` (source-copy `a0dee86`). It reclassifies 30 entries to needs-review and changes no EN text and no digest. FR now follows it. No held entry was translated and no hold was added or released: the held set is the same 538 ids as at `037706c`.

| Preflight | Result |
|---|---|
| `orca status --json` | runtime `ready`, `reachable: true`, connection `connected` |
| `git status --short` / branch | clean tree on `karmicare/soft-launch-fr`, HEAD `037706c` |
| Model / permission mode | Claude Opus 5.5 (`claude-opus-5-5`), auto mode; every Bash command sandboxed; no subagents |

| R6 additions | Commit | FR result |
|---|---|---|
| Merge | `2aeb6af` | `karmicare/soft-launch-source-copy` at `a0dee86`, no conflicts. It brings the R6-01 source gate, the NL R6 payloads and validator W1, `docs/localization/B4-REPORT.md` and the offline registration plan in `docs/localization/registration/`. I did not edit or rebuild the plan. The merge leaves `docs/localization/fr/**` untouched. |
| 30 reclassified | `0a0a182` | All 30 are `pending-claim-review`, with the FR text unchanged and not softened: 29 blocks of the wellness article (`seo.description` and `#b007` … `#b095`) and top-whitening `#b051` ("Bestselling"). The build reads the gate from the source `claim_status`, so each note reads "Claims review of batches 05-07 (CLAIMS-REVIEW.md): needs-review". |
| `#b081` | `0a0a182` | Confirmed: `pending-claim-review` since the addendum (`7760231`). The hand-set flag in the FR build is gone, because the source gate now sets the same flag. |
| R6-01 category words | checked | FR already uses the category word in both NL comparison entries. Wellness `#b081` reads « La formule du matin, Awake … la formule du soir, Asleep … Les deux formules » (NL *ochtendformule* / *avondformule*). Top-whitening `#b051` reads « Découvrir notre formule naturelle best-seller » (NL *meest verkochte natuurlijke formule*), and headaches `#b019` reads « notre formule sans fluor best-seller ». The assertions stay as written. |
| R6-02 "toothpaste" | checked | Manual pass over every translated FR value outside legal text. Outside titles, SEO and alt texts, *dentifrice* appears 21 times, each at a first-contact moment: the first body mention in each of the 9 articles (mostly the opening questions), the headings of the three content pages that carry one (nHAp `#b000` included), the 4 brush bodies (one block each), the homepage FAQ question about a fluoride toothpaste, the homepage meta description, the PDP body « Deux dentifrices, un système » and the FAQ product names « Dentifrice du matin Awake (2.0) » and « Dentifrice du soir Asleep (2.0) ». None negates the category; the why-stop page heading rejects fluoride toothpaste, as its EN does. FR has followed this rule since R3 F7 (`23bf6b1`), so R6-02 changes nothing here. |
| R6-02 compounds, R6 W1 | `c12aed7` | `check.py` now applies W1. The old banned-word warning is now an error and matches inside words too: *produit(s)* (so *sous-produit*), *tube*, *utilis-*, *emploi/employ-*, *(r)achat/(r)achet-*. It skips legal text and Dawn keys, as NL does. Four exceptions are listed with their reason: the CPNP portal name (as NL) and three uses of the verb *produire* (nano-hydroxyapatite `#b101`, nootropics `#b054`, fluoride `#b049`). It found 3 entries, now worded the way NL words them. Nano-hydroxyapatite `#b094`: « produisent des acides comme sous-produit, ce qui abîme » became « produisent au passage des acides qui abîment » (NL *daarbij*). Nano-HAp article `#b048`: « sans produits chimiques agressifs » became « sans substances chimiques agressives », as in wellness `#b081` (NL *chemicaliën*). Nano-hydroxyapatite `#b028`: « couramment employée en dentisterie » became « couramment appliquée en dentisterie » (NL *toegepast*). Two new self-test mutations prove W1. Run on the `0a0a182` files, it reports exactly these 3 entries and exits 1. |

**New totals:** 2,571 entries, 2,033 with FR, 538 held. `legal-review` 979, `pending-claim-review` 382, `fit-risk` 39, `pending-en-review` 22.

**Not applied:** nothing in "R6 additions". Since `037706c`, 3 FR values changed (Admin article bodies in batch 07) and 29 entries gained `pending-claim-review`. No entry was added, and no `theme-key` or template-setting value changed.

**Verification:**
- `python3 -I docs/source-copy/digest.py`: exit 0, all eight `ok` (digests unchanged by R6).
- `python3 -I docs/localization/fr/check.py --self-test`: exit 0, 0 errors, 10 warnings, 16/16 mutations caught.
- `shopify theme check --fail-level error`: exit 0 (248 files, 21 warnings) after the merge. My FR commits touch only `docs/localization/fr/`.

## Victor's decisions F1–F7 (20 Oct)

Answered on the review page `review/fr.html`: `F1=ja, F2=fr, F3=alles, F4=fondateur, F5=ja, F6=houden, F7=ja`.

| Decision | Answer | Effect on FR |
|---|---|---|
| F1 · FR terms as a set | accepted | No change; the "Proposed terms" table below is now approved. |
| F2 · French notation | 0,49 € and U+00A0 before `: ; ! ?` | Already applied; `check.py` enforces it. |
| F3 · publication order | everything at once | Not a payload change. Passed to the landing desk. The `legal-review` (979) and `pending-claim-review` (382) flags stay in the payloads until Victor clears those gates. |
| F4 · mission card "founder" | *fondateur* | `custom.mission_card#06` released from held to `admin`, FR "fondateur". |
| F5 · legacy legal pages | redirect to the 2.0 pages | Not a payload change: the redirect is an Admin action. The legacy pages stay held in FR. |
| F6 · customer care languages | keep | No change: "répond en anglais et en néerlandais" stays. |
| F7 · apostrophe | typographic ’ | Already applied; `check.py` flags straight apostrophes. |

Address forms in FR legal text (decision 7 below) was not on the review page and is still open.

## Delivery times (20 Oct)

Victor decided on delivery within 24 hours in the Benelux and in 2–3 working days in the rest of Europe. The NL lane changed seven EN entries in source-copy `b904fcd`, which this branch merged. `check.py` named the same seven entries as stale, and FR now follows them:

| Entry | FR change |
|---|---|
| Consumer rights `content_section_xKcNPj`, T&C `content_section_dGmgBJ`, policies `terms-of-service#b104` and `shipping-policy#b006` | « 1 à 3 jours ouvrables » → « dans les 24 heures »; « 2 à 5 jours ouvrables » → « 2 à 3 jours ouvrables » |
| `refund-policy#b080` / `#b081` | the same two changes, one per line |
| PDP sticky line `main-product.liquid:1036` | « Livraison rapide offerte : 24 heures au Benelux. 2 à 3 jours dans le reste de l’Europe », the same as the nav child's `delivery_free_html` in `locales/fr.json` |

The six legal entries keep `legal-review`. The legacy T&C entry ("8-14 working days") stays held. New digests: batch 02 `666785ab…`, batch 04 `98fda694…`.

## Retired Duo-name entries (Astra R12, 20 Oct)

PDP `50ad819` removed the settings `subscription_title` and `package_name`; the Duo's name is now the Shopify product title (Victor). Source-copy `6643e16` keeps the three entries with their ids and digests but marks them `retired`, and FR holds them with that reason:

- `index:featured_product_3XpDKw/loop_subscriptions_7dde8c/subscription_title` (was translated)
- `product.subscription-item:featured_product_Eb93Xa/loop_subscriptions_gPKypi/subscription_title` (was translated)
- `liquid:sections/main-product.liquid:1098`, the `package_name` default (was `theme-key`)

All three read « Système de soin matin/soir Awake & Asleep ». The naming source is `admin:karmicare-biorhythmic-oral-care-system:title`, already in FR as « Système de dentifrice matin et soir Awake & Asleep ». `check.py` now treats `retired` as a required hold, and its self-test has a 17th mutation for it. The next `build_payloads.py` run drops the two `subscription_title` items from `plan-fr.json`.

## Claim holds waived (Victor, 20 Oct)

Victor, through the landing desk (20 Oct): ignore the claim checks for now and translate everything that exists in English on the site, and leave the English unchanged. FR translates the 119 entries that were held on a claim, and they now carry `pending-claim-review`. They also carry the note "claim hold waived by Victor 20 Oct for translation; claims review still pending for publication", followed by the old hold reason. The 119 entries are:

- 107 blog blocks (batch 07)
- 6 Awake/Asleep 2.0 product lines (batch 05)
- 2 `/pages/nhap-technology` lines (batch 06)
- C35 benefit card 06, heading and text (batch 01)
- the C84/C85 practitioner quote on the homepage and the PDP

The translations follow the EN faithfully, claims included. They keep the FR conventions: "formule du matin Awake" and "formule du soir Asleep", product links unchanged, and no commodity words. Where an SEO description is cut off at 320 characters, the FR ends at the last complete clause, as in the rest of batch 07. That is why 25 claim-verb warnings now show ("prévenir"), and they are expected.

The treatment journey `#29` ("— from your gums to the") is translated exactly as it stands: "— de vos gencives jusqu’à". It keeps `source-defect`, and NL does the same.

`check.py` now accepts an unsupported claim when the entry carries both `pending-claim-review` and the waiver note. Two self-test mutations take the place of the old "translate an unsupported claim": dropping the flag fails, and so does dropping the note.

These stay held:
- **The two `[NEEDS APPROVED COPY]` placeholders on the homepage FAQ:** there is no EN text to translate. (Since 21 Oct both have approved EN and are translated; see the next section.)
- **"Rendering loop-subscriptions":** the theme tests for this exact text.
- **SLS article `b035`:** the source has it `blocked` because it names four competitors, a brand rule rather than a claim. It can be released only if the source owner unblocks it.
- **The 350 legacy legal entries:** the landing desk confirmed they stay held (20 Oct), because F5 redirects those pages to the 2.0 pages and translating outdated legal text would mislead. Each entry's note now gives that reason.

## Homepage copy at 41ae772 (source-copy 0ba9de3, 21 Oct)

The homepage lane rewrote part of the homepage (integration `41ae772`, merchant-edit `97ce2b7`). Source-copy `0ba9de3` brings the new EN into batches 01 and 02, and FR follows it. Victor's 20 Oct rule still applies: claims don't block translation, and names and quotes stay as they are.

- **Stat strip tagline:** "CHOISI PAR DES PRATICIENS KPNI, DES DENTISTES FONCTIONNELS ET DES PROFESSIONNELS DE SANTÉ". "Praticiens kPNI" matches the PDP stat line. The entry keeps `pending-claim-review` (C80).
- **Professional card titles (homepage and PDP, three each):** in the EN, "Therapist" became "Practitioner". The FR is unchanged. It keeps the epicene "thérapeute kPNI" and "Thérapeute en nutrition" and the field form "thérapie orthomoléculaire", because "praticien" would assume a gender (NL likewise keeps "therapeut"). The entries keep `gendered-title`.
- **FAQ, rendered:**
  - `kLMHax`, "Combien de temps dure un duo ?": the answer replaces the earlier placeholder. C07 is approved.
  - `qUxYCn`, "Que couvre la garantie satisfait ou remboursé ?": the answer is the same FR as the guarantee line in the terms, consumer rights and refund policy.
  - `Pz4mRk`, "Puis-je suspendre, sauter une livraison ou résilier ?": a new item.
- **FAQ, disabled** (`not-rendered`):
  - `7jmEGi`, "fluor + Karmicare": `pending-claim-review` (C101). The answer replaces the earlier placeholder.
  - `AL3DKF`, "Karmicare est-il sans fluor ?": `pending-claim-review` (C102).
  - Their category tabs now match their questions, so `pending-en-review` is gone from those tabs.
- **Retired, now held:**
  - FAQ `4KMG6C`, all three fields: the block was removed.
  - The two empty `how_it_works` step numbers on the PDP.
- **check.py:** no `[NEEDS APPROVED COPY]` placeholder remains in the source, so the placeholder self-test now releases the `blocked` SLS article `b035`. That fails for the same reason.

The source note on `qUxYCn/answer` still names claims C13 and C93. Those belonged to the old answer, and the entry has no `claims` field, so FR sets no claim flag there.

## Counts

| Batch | Source digest | Entries | translated | admin | theme-key | locale-present | held |
|---|---|---:|---:|---:|---:|---:|---:|
| `batch-02-pdp` | `2846c75e…` | 477 | 139 | 251 | 35 | 15 | 37 |
| `batch-01-homepage` | `46f2753b…` | 228 | 173 | 2 | 30 | 2 | 21 |
| `batch-03-header-footer` | `e17cadb5…` | 41 | 6 | 11 | 10 | 9 | 5 |
| `batch-04-legal` | `98fda694…` | 974 | 143 | 481 | 0 | 0 | 350 |
| `batch-05-products` | `5ab678a9…` | 77 | 16 | 61 | 0 | 0 | 0 |
| `batch-06-content-pages` | `3dee3b56…` | 22 | 0 | 22 | 0 | 0 | 0 |
| `batch-07-collections-blog` | `9597904c…` | 709 | 1 | 698 | 0 | 0 | 10 |
| `batch-08-system` | `306f141f…` | 46 | 3 | 7 | 0 | 36 | 0 |
| **Total** | | **2,574** | **481** | **1,533** | **75** | **62** | **423** |

Every source entry is covered: 2,151 carry FR and 423 are held (after the source-copy R6 merge, a0dee86, decision F4, the three retired entries, 6643e16, the claim holds Victor waived on 20 Oct, and the homepage copy at 41ae772, 0ba9de3). The full digests are in each file's header and match `docs/source-copy/digest.py` (all eight `ok`).

| Flag | 01 | 02 | 03 | 04 | 05 | 06 | 07 | 08 | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| legal-review | 1 | 1 | 5 | 972 | 0 | 0 | 0 | 0 | 979 |
| pending-claim-review | 39 | 42 | 1 | 0 | 25 | 7 | 387 | 0 | 501 |
| pending-en-review | 2 | 9 | 2 | 3 | 1 | 0 | 0 | 0 | 17 |
| source-defect | 2 | 8 | 1 | 3 | 9 | 0 | 0 | 0 | 23 |
| wording-adapted | 2 | 14 | 2 | 0 | 3 | 7 | 0 | 1 | 29 |
| gendered-title | 7 | 14 | 0 | 0 | 0 | 0 | 0 | 0 | 21 |
| fit-risk | 9 | 28 | 0 | 0 | 2 | 0 | 0 | 0 | 39 |
| not-rendered | 6 | 6 | 0 | 0 | 1 | 0 | 0 | 0 | 13 |

The blog's `wording-adapted` changes are described in each entry's notes and in the batch-07 commit, but not flagged one by one.

### Held (423)

| Batch | Reason | Count | What |
|---|---|---:|---|
| 04 | legacy | 350 | `/pages/privacy` (269), `/pages/terms-and-conditions` (76), `/pages/consumer-rights` (5): pre-2.0 legal pages, held in NL/FR (INVENTORY.md) |
| 01–03 | never-translate | 54 | Formula, practitioner and brand names, citations, INCI, `nHAp`, `SCCS/1677/25`, Subscription Names, Return on Care |
| 07 | empty | 9 | Empty article excerpts (`summary_html`) |
| 01–02 | retired | 8 | The Duo-name settings `subscription_title` (homepage, PDP) and the `package_name` default `main-product.liquid:1098` (Astra R12, source-copy `6643e16`); FAQ `4KMG6C` (3 fields) and the two empty PDP `how_it_works` step numbers (41ae772, source-copy `0ba9de3`) |
| 01 | integration | 1 | "Rendering loop-subscriptions": the theme tests for this exact text |
| 07 | needs approved copy (competitor names) | 1 | SLS article `b035` names Colgate, Biotene, Sensodyne Pronamel and Tom's of Maine; source `blocked` since R2 |

## Evidence

**`python3 docs/localization/fr/check.py --self-test`: exit 0, 0 errors, 25 warnings, 18/18 bad payloads caught.** For every file it checks (R3 F6 added the gates, R2 the S1/S2 text checks, R6 the W1 brand words):

- every source batch has an FR file; the batch digest against the source, and `en_sha1` against `sha1(en)`;
- one entry per source id, in order, with the source `resource_type`, `file_or_handle`, `key_path` and status;
- the holds the source requires (never-translate, placeholder, unsupported claim in CLAIMS-REVIEW.md or the 05–07 `claim_status`, legacy page);
- `pending-claim-review` on every translated needs-review claim, `legal-review` on every legal entry (source `legal`, and all of batch 04 outside the contact page);
- the delivery channel per source status, Dawn values equal to `locales/fr.json`, and `counts` / `flag_counts` recomputed from the entries;
- the status and flag vocabulary;
- that EN and FR carry the same HTML tags, Liquid, `[tokens]`, `&nbsp;` count and runtime price spans;
- that the selling-plan IDs are unchanged;
- that every EN postal address appears unchanged in the FR (S1) and the `(*)` count matches (S2);
- that ordinary copy (translated, not legal, not a Dawn key) has no commodity word, inside a word too (W1): *produit(s)*, *tube*, *utilis-*, *emploi/employ-*, *(r)achat/(r)achet-*, with 4 listed exceptions (the CPNP portal name and three uses of the verb *produire*);
- French spacing and apostrophes.

For entries that are not legal, it also warns on claim verbs and *tu* forms.

**The 10 warnings, each checked by hand:**

- **Batches 01–02 (8):** the noun *prévention*: the EN "Prevention" in the check-up and plan tooltips and the compare table, and C33.
- **Batch 07 (2):**
  - *prévenir les caries*: a statement about fluoride, not a Karmicare claim.
  - *guérison*: the EN "healing cycles", a needs-review claim kept as written.

**Other checks:**

- `python3 docs/source-copy/digest.py`: all eight batches `ok`.
- `shopify theme check --fail-level error`: **exit 0**. 248 files inspected, 21 offenses, all warnings, after the R6 merge. FR commits change no theme file, and `.theme-check.yml` is untouched.
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
  - Company name, enterprise, VAT and EORI numbers, IBAN/BIC, emails, phones, periods and amounts are exactly as in EN. Postal addresses are exactly as in EN too, city and country names and "box 1" included (R2 F8; the French forms wait for decision 7).
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

## Fit risks (39 entries; textual triage, not measured overflow)

`Kind`, as in the NL report (R2 F7): **slot** is a button, chip, cell, plan card, sticky bar or label with a fixed width; **contextual QA** is a heading that can wrap, to look at in context rather than an established overflow.

| Entry | Kind | EN chars | FR chars | Fallback |
|---|---|---:|---:|---|
| Hero, two-formulas and benefits button "BEGIN YOUR 60-DAY RITUAL" | slot | 24 | 31 | COMMENCER LE RITUEL |
| Buy box `welcome_kit_title` | slot | 30 | 31 | Glossary long form (47) if there is room |
| Buy box `try_once_note` | slot | 42 | 56 | 0 € Care Credit · 0 € récompense contrôle |
| Care receipt `line_year/note` | slot | 20 | 31 | 20 % reversés |
| Sticky bar `credit_checkup` | slot | 44 | 49 (short form) | Full form 63 |
| Sticky bar `stop_year` | slot | 43 | 51 | |
| Sticky bar `try_once` | slot | 48 | 53 | |
| Treatment journey `#23` | slot | 44 | 48 | Full form in notes |
| Comparison `#18` "Weeks to notice" | slot | 15 | 22 | |
| Buy and sticky button "Begin Now" (PDP and `product.json`, 4 entries) | slot | 9 | 20 | exact FR kept (R3 F8) |
| Sticky bar `cta_rhythm` (`main-product.liquid:1018`) | slot | 24 | 31 | exact FR kept (R3 F8) |
| Sticky bar `kit` (`:1049`) | slot | 37 | 54 | exact FR kept (R3 F8) |
| Sticky bar `stop_rhythm` (`:1067`) | slot | 21 | 34 | exact FR kept (R3 F8) |
| Plan name "ships every 60 days" (2 selling plans) | slot | 19 | 28 | exact FR kept (R3 F8) |
| Compare table `#14` "Try Once" | slot | 8 | 16 | exact FR kept (R3 F8) |
| Compare table `#25` "Begin 60-Day Rhythm" | slot | 19 | 28 | exact FR kept (R3 F8) |
| Compare table `#11` "Skip, pause or cancel" | slot | 21 | 43 | full meaning kept (R3 F3) |
| Research card `card_JeERX6` heading (homepage and PDP) | contextual QA | 44 | 72 | full meaning kept (R3 F4) |
| Research button "Explore the full evidence base" (homepage and PDP, 2 entries) | slot | 30 | 31 | exact FR kept (R2 F7) |
| Plan-card shipping value "Varies Free" (homepage and PDP, 2 entries) | slot | 11 | 16 | exact FR kept (R2 F7) |
| Trust-row chip "Gift, pause or cancel" (PDP buy box and end CTA, 2 entries) | slot | 21 | 29 | exact FR kept (R2 F7) |
| Trust-row chip "60-day money-back guarantee" (homepage, PDP buy box, end CTA, 3 entries) | slot | 27 | 31 | same row (R2 F7) |
| Trust-row chip "Cancel anytime" (homepage) | slot | 14 | 24 | same row (R2 F7) |
| Trust-row chip "Free shipping" (homepage, PDP buy box, end CTA, 3 entries) | slot | 13 | 17 | same row (R2 F7) |
| Comparison `#23` "Systemic, not oral" | slot | 18 | 22 | exact FR kept (R2 F7) |

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

- **`theme-key` (75)**:
  - The 25 sticky-bar defaults (the retired `package_name` default `:1098` is held) in `main-product.liquid` need the PDP owner to store them or make them keys.
  - The 8 Loop strings are in off-limits files, so the Loop owner integrates them.
- **`locale-present` (62)**: nothing to do; `locales/fr.json` already has them.
- **`admin` (1,416)**:
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
| Content pages | 06 | `/pages/why-karmicare`, `/pages/why-use-hydroxyapatite-toothpaste`, `/pages/why-stop-using-fluoride-toothpaste`, `/pages/nhap-technology`, `/pages/articles` | `/nl/pages/…` | `/fr/pages/…` | nhap: heading `b000` translated, `b001` and SEO description held |
| Collections | 07 | `/collections/biorhythmic-oral-hygiene-kit`, `/collections/vgbc2025`, `/collections/karmicare-collection` | `/nl/collections/…` | `/fr/collections/…` | |
| Blog and 9 articles | 07 | `/blogs/news`, `/blogs/news/<handle>` | `/nl/blogs/news/…` | `/fr/blogs/news/…` | 117 blocks held |
| System pages | 08 | `/search`, `/pages/<missing>` (404), `/collections`, `/collections/all`, `/cart` | `/nl/…` | `/fr/…` | |
| Header and footer | 03 | every page | every `/nl/…` page | every `/fr/…` page | |

## Pending

| Item | Gate or owner |
|---|---|
| Astra review of the FR payloads | coordinator, after `worker_done` |
| Legal review of 979 legal entries | Victor or a lawyer, before any FR legal page is published |
| Claims sign-off: 382 `pending-claim-review` entries (the R2 and R6 reclassifications and C100 included); 119 held as unsupported (4 in 01–02, 115 in 05–07) | Victor / Clinical Research |
| Heading 4.1 "presumption of conformity" (consumer-rights template, refund `#b065`) | legal owner approves or corrects the EN, then FR is regenerated |
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
- **Localization worker**: the integration notes above. After R2, refresh from this branch's tip: no `theme-key` value changed since `c7aed28`, but 13 template-setting values did (the footer compliance line and 12 legal template sections, addresses back to the EN form) and the nHAp page heading `b000` is new (Admin). After R6, only 3 Admin article bodies changed (batch 07) and 29 entries gained `pending-claim-review`; no `theme-key` or template-setting value changed.
- **Loop owner**: 8 Loop strings in batch 01 (`theme-key`).
- **EN owner (R2, R6)**: compliant copy for the SLS competitor block `b035`; the "Why You Need It" headings; the morning-brush "2 to 4 applications" dose; "organic biomaterial"; "Bestselling" (headaches `#b019`, top-whitening `#b051`); the two sleep/wake description lines; the 29 wellness blocks R6-01 gated. FR follows by digest.
- **Source owner (Astra R12)**: rebuild `plan-fr.json` with `build_payloads.py` from this branch's tip, so the two retired `subscription_title` items leave the FR plan (section "Retired Duo-name entries").
- **Source owner**: rebuild the offline registration plan (`docs/localization/registration/plan-fr.json`) from this branch's new tip. FR did not edit or rebuild it, and since `037706c` only `fr/batch-07-collections-blog.json` (3 values, 29 gates) and `fr/check.py` changed. The `#b081` source gate is in place (`a0dee86`), so that earlier handoff is closed.

## Open decisions for Victor

Decisions 1–6 were answered on 20 Oct as F1–F7 (section "Victor's decisions F1–F7"). Only decision 7 is still open. The text below is kept as the record of what was asked.

1. **Confirm the proposed FR terms** (table above), above all the plan names, *offre* for "plan" and *matin/soir* for AM/PM.
   - *Recommendation*: accept them as a set, so NL and FR stay parallel.
2. **Does FR ship, and which parts first?**
   - The PDP, homepage, header/footer, products and system pages are ready for a native read-through.
   - The legal pages need legal review.
   - The pre-2.0 blog is heavy with claims: 280 needs-review blocks translated, 117 held.
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
7. **Address forms in FR legal text** (R2 F8, as NL question 8).
   - Today FR keeps every address exactly as in the EN: "Vizierstraat 28, 8000 Bruges, Belgium", "Boulevard du Roi Albert II 8, box 1, 1000 Brussels".
   - The alternative is the official French forms ("Boulevard du Roi Albert II 8, boîte 1, 1000 Bruxelles, Belgique"), which FR used before R2.
   - *Recommendation*: allow the official local forms in NL and FR, since "box 1, 1000 Brussels, Belgium" reads as unedited on a French legal page. Switching back is the FR build's six-string address table read backwards, then a rebuild; S1 in `check.py` would then need the same exception.

## Re-running

When an EN batch changes, `check.py` names the stale entries (en_sha1 mismatch), and only those need new FR.
