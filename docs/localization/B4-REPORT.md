# B4 · Localization integration: theme keys, registration route, payloads, dry run

## Status 22 Oct

The rows of the lane that concern this report; the whole lane is in `docs/source-copy/REPORT.md` (same row numbers).

"In merchant-edit" is checked with `git merge-base --is-ancestor <sha> merchant-edit` against `2ef9b5c` (22 Oct). merchant-edit is not pushed yet, so none of it is live.

| Status | Rows |
|---|---:|
| In merchant-edit | 4 |
| Ready to land | 1 |
| In progress | 0 |
| Waiting for Victor | 5 |
| Parked / after launch | 3 |
| Dropped | 2 |

| # | Status | What | Commits / where |
|---|---|---|---|
| 5 | In merchant-edit | 64 `kc.*` theme keys in all 31 locales: footer, plans, clock, FAQ "ALL", sticky bar, hero, stat strip, PDP labels; EN, NL and FR values | `16decc4` … `1630eef`, `c348c72`, `61efa65` |
| 8 | In merchant-edit | Sticky-bar key `kc.sticky_cart.kit_free_html` removed from all 31 locales (NV-13) | `d72d791` |
| 11 | In merchant-edit | Offline registration plan for NL and FR, the app set-up steps for Victor (`APP-SETUP.md`) and the first version of `register.py` | `8a7548d` … `060de0e`, `2f9a83f`, `0e21a1f` |
| 13 | In merchant-edit | `register.py` reworked after reviews R18, R18b and R18c; R18d (21 Oct): approve, no new findings, selftest 80/80 | `93e1850`, `44bb619`, `59c281e` |
| 14 | Waiting for Victor | Translations app for the registration | `APP-SETUP.md` |
| 15 | Waiting for Victor | Writing the first wave of translations to Shopify (not asked yet: it comes after the dry run and the bindings review) | `register.py --write` |
| 16 | Waiting for Victor | NL and FR stay published while the first wave is not in | B4 decision 3 |
| 17 | Waiting for Victor | Legacy translated product handles (12 URLs, e.g. `/nl/products/compleet-hygiene-kit`) | B4 decision 4 |
| 18 | Waiting for Victor | Browser-language redirect on product pages | B4 decision 5, manual check 3 |
| 51 | Ready to land | Victor's admin EN edits of 22 Oct in the EN source and the NL: the Duo's title, SEO title and meta description, the footer menu link "Why hydroxyapatite", six fields of the nano-hydroxyapatite article; its twin article is hidden and redirected, so its 79 entries are retired. His own NL/FR Duo texts are recorded as registered (`registration/registered.json`), so the plan never overwrites them. The FR payload follows in the FR lane | reported 22 Oct to the global coordinator |
| 42 | Parked / after launch | Loop widget strings (off-limits files): the 11 strings of the B4 Loop table, handed to the Loop owner; NL and FR are in the payloads | B4 report, Loop handoff |
| 43 | Parked / after launch | Navigation links and Shopify policies: no proven API route in the runner yet (LINK, SHOP_POLICY); after the first wave, or through Translate & Adapt | `register.py`, B4 Part 2 |
| 44 | Parked / after launch | Rendered check of the keyed strings on /nl and /fr (B4 manual checks 1–5): after the theme ships | preview gate |
| 47 | Dropped | Clock gates (B4 decision 6): review gates no longer hold theme keys, after Victor's waiver | `c348c72` |
| 50 | Dropped | Choice of access path (B4 decision 1): the Dev Dashboard app route was chosen | desk, 21 Oct |

### Waiting for Victor: the questions

**14. Translations app for the registration.** Will you create the Dev Dashboard app "Karmicare translations" as in `APP-SETUP.md`, install it on karmicares.myshopify.com, store the client secret in your Keychain, and then say "app klaar" with the published theme's ID?
- (a) With the extra scope `read_themes`: the runner reads the published theme itself and proves the ID.
- (b) Without it: you confirm the theme ID yourself on the day of each run (`--theme-attested "<date> Victor"`).
- *Advice*: (a): one manual step less, and the runner checks the theme instead of trusting a typed ID.

**15. Writing the first wave of translations to Shopify (not asked yet: it comes after the dry run and the bindings review).** After the read-only dry run and the review of the metaobject bindings, may the runner write the first wave (NL 504, FR 502 items)?
- (a) Yes, the whole first wave.
- (b) Yes, but theme text (homepage, PDP, header, footer) first, products and metafields in a second run.
- (c) No, not before launch.
- *Advice*: Decide on the dry-run report, which shows every current value it would overwrite. NL and FR are already published, so each registered translation is live at once; (a) if the report is clean.

**16. NL and FR stay published while the first wave is not in.** /nl and /fr are published today and show mostly English. Keep them published?
- (a) Keep them published and register quickly.
- (b) Unpublish NL and FR in the admin until the first wave is in.
- *Advice*: (a): unpublishing is an admin change that takes /nl and /fr away from visitors who already use them, and the first wave is ready.

**17. Legacy translated product handles (12 URLs, e.g. `/nl/products/compleet-hygiene-kit`).** The old NL/FR product URLs answer with a 301 to translated handles. Keep or remove them?
- (a) Keep them: both URL forms work.
- (b) Remove them, so handles stay English everywhere.
- *Advice*: (a) for launch; nothing breaks, and removing them is an admin change that can wait.

**18. Browser-language redirect on product pages.** A browser set to English is sent from `/nl/products/…` to the EN product. Will you run manual check 3 of the B4 report (2 minutes, a new English browser profile) to see whether the language selector still keeps a visitor on NL?
- (a) Check it before launch; if it fails, change the setting in Markets or the app behind it.
- (b) Leave it until after launch.
- *Advice*: (a): Dutch customers with an English browser would otherwise land on the EN product.

**Translation script (`register.py`).** R18d (21 Oct) approved `59c281e`: no new findings, selftest 80/80. Nothing has run live. The order from here:
1. Victor says "app klaar" and gives the published theme ID (row 14).
2. A read-only dry run with theme proof; its report shows every current value and the API contract.
3. Review of the binding proposals for the metaobject fields (48 NL, 50 FR) into `bindings.json`, with the full old and new translations.
4. A fresh dry run.
5. Its checksum and Victor's explicit yes (row 15); only then `--write`.

**Changelog.** 22 Oct: this status block added at Victor's request (via the landing desk). 22 Oct, later: rows 12 and 13 landed in merchant-edit `2ef9b5c`; rows 39, 51 and 52 for Victor's admin edits of that day; rows 26 and 53 for his dentist and slogan decisions.

Task `task_427cfe23005d` (dispatch `ctx_505619d6c8e5`), brief `.coordinator/BRIEF-B4.md`. Nothing was registered, pushed or changed in Shopify.

## Preflight

| Check | Result |
|---|---|
| Orca | `orca status` ready and reachable; heartbeats sent through `orca orchestration send` |
| Workspace | `soft-launch-source-copy`, branch `karmicare/soft-launch-source-copy`, clean tree, HEAD `2194ef3` at start |
| Model and mode | Opus 5.5 (`claude-opus-5-5`), auto mode, sandbox on, no unsandboxed retries |
| Rules read | `.coordinator/BRIEF-B4.md`, `COMMON-RULES.md`, `BROWSER-WORKFLOW.md` |
| Browser helper | `python3 .orca/mission-runtime/browser.py`: the first `status` timed out (60 s), then `goto` and `metrics` worked |
| Off limits, untouched | Loop widget files, `config/settings_data.json`, Shopify Admin, theme push/dev |
| Shared worktree | A second session (the R2 fixer, `Claude-Session 012gB8Y9…`) committed R2 fixes on this branch while B4 ran (`3ef6ba8` … `fb46dd1`). My `218fe9d` picked up its staged files by accident. I reset that commit and re-committed only my files (`e850bc4`). The R2 F1 batch-05 hold then landed inside its `8ed5ed1` (F5) commit. From then on I committed only with explicit paths. Reported to the coordinator. |

## Summary

- **Part 1.** 64 `kc.*` locale keys now cover the 64 in-scope `needs-key` strings. They are written to all 31 storefront locale files: EN, NL and FR from the reviewed payloads, English in the other 28. Nine commits; Theme Check exits 0 after every theme commit.
  - 12 keys stay English in NL or FR because of a gate.
  - The other 13 `needs-key` strings are Loop (handed off), Coming soon (homepage branch) and one never-translate placeholder.
- **Part 2.** The route is the GraphQL Admin API `2026-10`: `translatableResources` → `translationsRegister`. It needs a Dev Dashboard app that reads its token at run time. The Translate & Adapt CSV import is the fallback.
- **Part 3.** The offline plan builds 1,827 NL and 1,821 FR registration items. The first wave is 522 NL and 529 FR items; GIDs and digests come at run time.
- **Part 4.** Every NL/FR URL in the tables loads, either directly or through a 301 to a legacy translated product handle. All 126 pages that answer 200 carry `hreflang` en/fr/nl/x-default. The footer form is present on all of them except `/cart`, which has no footer by design. Three findings change the plan:
  - **NL and FR are already published.**
  - **Legacy NL/FR product translations and translated handles already exist.**
  - **Product pages redirect on the browser's language.**

## Part 1 · Theme keys

### Commits

| Commit | Area | Keys | What changed |
|---|---|---:|---|
| `3129f1d` | tooling | – | `docs/localization/theme-keys.json` (key → inventory ids, EN/NL/FR, holds) and `docs/localization/theme_keys.py` (`refresh`, `check`, `write`) |
| `16decc4` | footer | 9 | `sections/footer.liquid`: newsletter label, placeholder, Join, consent line (`consent_html`, links passed as `terms_url`/`privacy_url`), picker titles. The 3 legal link labels lose their schema default: blank uses the key. |
| `c95d964` | plans | 7 | `product-compare-plans.liquid` (label, Compare, kit value, Free, Included, Not included), `featured-product.liquid` (Free), `main-product.liquid` (Or) |
| `571ab49` | clock | 13 | `chronobiology-clock-karmicare.liquid` renders the copy as data attributes on `.readout`. `assets/chronobiology-clock-karmicare.js` keeps only the window ranges and reads `data-window-N`, the captions and the valuetext tails. No English copy is left in the JS except the brand names Awake/Asleep. |
| `a93ddb5` | FAQ | 1 | `km-faq-accordion.liquid` "ALL" tab; the filter keys on `data-filter="all"` |
| `7ad66ce` | sticky bar | 26 | The 26 `sticky_cart` defaults leave the `main-product.liquid` schema; one paragraph setting explains that a blank setting uses the key. `snippets/sticky-cart-block.liquid` assigns the keys; a setting value overrides its key. |
| `e850bc4` | hero, stat strip | 5 | hero aria-label and alt fallback (setting overrides), switcher label, `{{ label }} mode` for both pills; stat strip aria-label |
| `e040dca` | PDP labels | 3 | category strip and highlights aria-labels, "PROFESSIONAL PARTNERS" |
| `1630eef` | FR refresh | – | The FR branch merged R1 (`c7aed28`). FR `valuetext_live` gets ". Heure locale actuelle." and the FR placeholder becomes `you@example.com`, as in the FR payload. |

Keys per area: clock 13, faq 1, footer 9, hero 4, pdp 3, plans 7, stat_strip 1, sticky_cart 26 (64). They are sorted, all in one `kc` object at the top of each locale file, where the homepage branch puts `kc.general.coming_soon`. I did not add that key.

### How the strings reach Liquid and JS

- **Settings with a translated default** (footer legal labels, hero aria/alt, sticky bar): same pattern as the homepage's Coming soon. The schema default is removed; a blank setting uses the key and a filled one overrides it. Shopify HTML-escapes `t` output ([locale files doc](https://shopify.dev/docs/storefronts/themes/architecture/locales/storefront-locale-files): "Translated content is escaped by default"), so the override joins it with `escape_once`.
- **Sticky bar.** Its copy goes through a JSON block that the script reads as `textContent`. An escaped `&` or `'` would show up literally there. The 26 keys therefore end in `_html`, so `t` returns them unescaped. The 3 spots in HTML keep `| escape`.
- **Clock JS.** The strings are data attributes, which the browser decodes, so the JS gets plain text.
- **Not keyed, never translated:** `Awake`/`Asleep`/`AWAKE`/`ASLEEP`, selling-plan names and IDs, `Rendering loop-subscriptions` (the code tests for it).

### Values and holds

`theme_keys.py write` puts EN in `en.default.json`, and NL/FR in `nl.json`/`fr.json` unless the key has a hold, in which case that locale gets EN. Every other storefront locale gets EN, so Theme Check finds the same keys everywhere (`MatchingTranslations` stays at 0, no new ignores).

| Key | NL | FR |
|---|---|---|
| `kc.clock.loading` | EN: not in the B1a inventory **[NEEDS APPROVED COPY]** | same |
| `kc.clock.window_1` | EN: pending-claim-review (C54) | EN: pending-claim-review (C54) |
| `kc.clock.window_2` … `window_7` | translated | EN: the FR payload flags all seven pending-claim-review (the source links only C54 to window 1) |
| `kc.footer.consent_html`, `legal_terms`, `legal_privacy`, `legal_consumer_rights` | translated | EN: legal-review in the FR payload |

`kc.clock.loading` is the knob's `aria-valuetext` before the script runs ("Loading current local time"). The B1a inventory missed it; it should be added at the next inventory refresh.

### Checks run

- `shopify theme check --fail-level error`: exit 0 after every theme commit (21 warnings, the same as before B4).
- `python3 docs/localization/theme_keys.py check --fr-dir <FR payloads>`: ok for all 64 keys. It checks the values against the EN source, NL payload and FR payload, that each key is used in the theme, and the 31 locale files. It was rerun after the R2 commits (`fb46dd1`) and the FR merge (`c7aed28`).
- The clock JS was run on a stub DOM with the NL attributes: live caption, hour window and tail; Home/arrow preview; Escape back to live.
- The `main-product.liquid` schema parses; `button_text` is the only `sticky_cart` default left. `legal_*_label` and the sticky settings are not stored in any template, section group or `settings_data.json`.
- **Not done:** a rendered check of the Liquid. `shopify theme dev` and pushes are not allowed here, so it waits for the preview gate.

### Merging with the other branches

`git merge-tree` against the current heads:

- **PDP (`985710e`), FR (`c7aed28`), Utopia:** merge cleanly.
- **Homepage (`cd20941`):** conflicts in the 31 locale files, because both branches add a `kc` block at the same place. It also conflicts in `sections/km-faq-accordion.liquid`, where the homepage turns the "ALL" `<span>` into a `<button>`.
  1. Resolve the locales by taking the homepage side, then run `python3 docs/localization/theme_keys.py write`. It merges the 64 keys into the existing `kc` object and keeps `kc.general.coming_soon`. Tested on the homepage branch's 31 locale files: all keys present, `general` kept, the rest of each file unchanged.
  2. In the FAQ, keep the homepage's `<button …>` with `{{ 'kc.faq.all' | t }}` as its text.

**Locale files and Translate & Adapt.** Editing a `kc.*` value in the admin (default theme content) writes to the live theme's locale file. The next push from `main` overwrites that edit unless it is pulled back. Change values in `theme-keys.json` and rerun `write` instead.

## Part 2 · Registration route (official docs, accessed 19 Oct 2026)

### API

- **Version.** `2026-10` is the latest stable GraphQL Admin API version: released 1 Oct 2026, supported until at least 16 Oct 2027 ([release notes](https://shopify.dev/changelog/release-notes/2026-10)).
- **Reading content.**
  - `translatableResources(resourceType:, first:, after:)` returns each resource's `resourceId` and its `translatableContent { key value digest locale }` ([query](https://shopify.dev/docs/api/admin-graphql/latest/queries/translatableResources)).
  - `translatableResource(resourceId:)` and `translatableResourcesByIds(resourceIds:)` fetch known GIDs.
  - `TranslatableResource.translations(locale:, outdated:, marketId:)` shows what is already registered ([object](https://shopify.dev/docs/api/admin-graphql/latest/objects/TranslatableResource)).
- **Writing.** `translationsRegister(resourceId:, translations: [TranslationInput!]!)` ([mutation](https://shopify.dev/docs/api/admin-graphql/latest/mutations/translationsRegister)).
  - `TranslationInput` has the fields `key`, `locale` (must be in `shopLocales`), `value`, `translatableContentDigest` and an optional `marketId` ([input](https://shopify.dev/docs/api/admin-graphql/latest/input-objects/TranslationInput)).
  - "Each translation requires a digest value from the resource's translatable content."
- **Metafields in 2026-10.**
  - Corrected 21 Oct (review R18): the bundled 2026-10 Admin schema has no `Metafield.translatable` field, keeps `METAFIELD` as a non-deprecated `TranslatableResourceType`, and registration uses the digest from the metafield's own `translatableContent`. `register.py` therefore reads the product's metafield GIDs (`product { metafields { id namespace key } }`) and fetches them with `translatableResourcesByIds` (key `value`). This is a schema snapshot, not proof of live behaviour: the first read-only dry run confirms it.
  - Text types only: single/multi-line text, rich text, html ([changelog](https://shopify.dev/changelog/metafield-translations-now-available-via-graphql-admin-api)).
- **Theme content.**
  - `ONLINE_STORE_THEME_JSON_TEMPLATE`, `…_SECTION_GROUP`, `…_LOCALE_CONTENT`, `…_SETTINGS_CATEGORY`, `…_SETTINGS_DATA_SECTIONS` and `…_APP_EMBED` have "dynamic keys based on theme data" ([enum](https://shopify.dev/docs/api/admin-graphql/latest/enums/TranslatableResourceType)).
  - Shopify treats the exact key format as an implementation detail. The plan therefore stores the section, block and setting ids plus the EN sha1, and matches the live key at run time.
- **Scopes.**
  - The docs list `read_translations` (queries) and `write_translations` (mutation).
  - The translations guide also lists `read_products` and `write_locales` ([guide](https://shopify.dev/docs/apps/build/markets/manage-translated-content)). `read_products` is needed to read the product's metafields. `write_locales` is only for enabling or publishing a language, and NL and FR are already published.
  - The docs name no extra scope for theme resources. Corrected 21 Oct (R18): `translatableResources` has no theme-ID argument. `register.py` takes the published theme's ID as `--theme-id` and accepts a theme resource only if its GID names that theme and the template; otherwise theme content is not written.
- **Locales.**
  - `shopLocaleEnable` and `shopLocaleUpdate(published:)`; at most 20 published locales on non-Plus plans ([requirements](https://help.shopify.com/en/manual/international/languages/requirements)).
  - Market-specific theme content is stored as a theme override, not a translation ([guide](https://shopify.dev/docs/apps/build/markets/manage-translated-content)).

### Inventory resource types → Shopify

| Inventory `resource_type` | Shopify type | Key | How the GID and digest are found at run time |
|---|---|---|---|
| `template_setting` | `ONLINE_STORE_THEME_JSON_TEMPLATE` | dynamic | the template resource whose GID proves the published theme (`--theme-id`); every section/block/setting id a token of the key, then the EN sha1 |
| `section_group` | `ONLINE_STORE_THEME_SECTION_GROUP` | dynamic | as above, header and footer groups |
| `theme_locale` | (`ONLINE_STORE_THEME_LOCALE_CONTENT`) | – | not registered: Part 1 keys and Dawn's own keys ship in `locales/*.json` |
| `product` | `PRODUCT` | `title`, `body_html`, `meta_title`, `meta_description` | `translatableResources(PRODUCT)`, matched on the `handle` content |
| `product` `media.<id>.alt` | `MEDIA_IMAGE` | `alt` | GID from the inventory id |
| `metafield` | `METAFIELD` | `value` | the product's metafield GIDs by namespace and key, then `translatableResourcesByIds` |
| `metaobject` | `METAOBJECT` | field keys | metaobjects referenced by the product's metafield (nested references need `read_metaobjects`); only the field the inventory names or a reviewed binding in `registration/bindings.json` binds (the dry run proposes them), then the EN sha1 |
| `app` selling plans | `SELLING_PLAN` / `SELLING_PLAN_GROUP` | `name`, `description`, `option1-3` | not registered here: Loop translates them (PDP lane, 21 Oct) |
| `navigation` | `LINK` (and `MENU`) | `title` | not registered yet: no verified menu → link owner route |
| `page` | `PAGE` | `title`, `body_html`, `meta_*` | matched on `handle` |
| `article`, `blog` | `ARTICLE`, `BLOG` | `title`, `body_html`, `summary_html`, `meta_*` | matched on `handle` |
| `collection` | `COLLECTION` | `title`, `body_html`, `meta_*` | matched on `handle`; `/collections/all` is virtual (not registered) |
| `policy` | `SHOP_POLICY` | `body` only | matched on the body; policy titles are not translatable through the API |
| `shop` | `SHOP` | `meta_title`, `meta_description` | single resource; system page titles are composed by Shopify (not registered) |

Split fields (`body_html#bNNN`, `body#bNNN`) are rebuilt at run time: each block's EN is replaced in the live value. A field registers only when all of its blocks can register.

### A token-safe access path

- **Custom apps now come from the Dev Dashboard.** "If you have legacy custom apps created before January 1, 2026, you can manage them from your Shopify admin"; new ones are made in the Dev Dashboard, and "store owners automatically have full access" ([custom apps](https://help.shopify.com/en/manual/apps/app-types/custom-apps)).
- **Token.** A Dev Dashboard app installed on a store of the same organization exchanges its client ID and secret for an Admin token: `POST https://{shop}.myshopify.com/admin/oauth/access_token` with `grant_type=client_credentials`. The token lasts 24 h (`expires_in` 86399). Scopes come from the app version ([access tokens](https://shopify.dev/docs/apps/build/dev-dashboard/get-api-access-tokens)).
- **Proposed setup, Victor only:**
  1. App "Karmicare translations" in Karmicare's organization, with scopes `read_translations`, `write_translations` and `read_products`; installed on `karmicares.myshopify.com`.
  2. Victor stores the client secret in the macOS Keychain in a Terminal of their own (`security add-generic-password -s karmicare-translations -a <client id> -w`, which prompts for the value).
  3. At run time the runner reads it with `security find-generic-password -s karmicare-translations -w` inside its own process, fetches the 24 h token and keeps it in memory.
- **Runner (21 Oct).** `docs/localization/registration/register.py`, reworked after review R18 (`docs/runtime-review/R18-REGISTER-ASTRA.md` on the landing branch): identity before EN, protected targets, whole JSON fields, an approval checksum over a snapshot that includes the current translations, a re-read before every mutation, a journal, and a scrubber on every output. `register_selftest.py` covers each finding offline. No live run yet: a read-only contract run comes after the re-review.

### Fallback: Translate & Adapt CSV ([help](https://help.shopify.com/en/manual/international/languages/csv-translations))

- **Export.** Settings > Languages > Export: one language or all; All content / Metafields / Outdated / Untranslated. The file is emailed.
- **Columns.** `Type`, `Identification` (resource ID), `Field`, `Locale`, `Market`, `Status` (outdated), `Default content`, `Translated content`. Only `Translated content` should be edited; use comma delimiters.
- **Import.** Settings > Languages > Import.
  - With **overwrite on**, CSV translations replace the existing ones. With **overwrite off**, only new translations are imported.
  - Errors stop the import; a confirmation email lists failed or skipped rows.
  - Import works for secondary languages only.
- **Not documented:** the row-matching key, what an empty cell does, and whether theme content and section groups are in the export. A trial export answers these before relying on it.
- **No token needed.** The plan files can fill an exported CSV (match on `Default content` and the EN sha1).

### What Shopify translates, and what stays with apps

- **Shopify:**
  - Checkout has pre-translated content for 33 languages. Dutch and French are among the languages with professional translations of checkout, cookie banner, privacy policy and default theme content ([requirements](https://help.shopify.com/en/manual/international/languages/requirements)).
  - After publishing, checkout and email notifications show in the customer's language; notification translations can be edited per language ([localization](https://help.shopify.com/en/manual/international/localization-and-translation)).
  - Customer accounts are hosted: `/nl/account/login` redirects to `shopify.com/…/account?locale=nl`.
  - Dawn's own keys (62 entries) are already in `nl.json`/`fr.json`.
- **Consent banner.** It is Shopify's own Customer Privacy banner. `assets/kc-cookie-preferences.js` copies its translated text into the restyled panel, so it needs no key.
- **Apps:**
  - **Loop.** The theme widget strings are handed off below. Selling plans and groups are Shopify resources and are in the plan. The Loop portal and emails are translated in Loop.
  - **Judge.me.** The review badge strings ("stars", review count) are app content, translated in Judge.me.

## Part 3 · Payload builder and dry run

`docs/localization/registration/build_payloads.py` (offline) writes `plan-nl.json`, `plan-fr.json` and `DRY-RUN.md`, all committed in `8a7548d`. Inputs:

- **EN source and NL:** this branch after R2 (`fb46dd1`).
- **FR:** `karmicare/soft-launch-fr` `c7aed28`, read with `git show`, not merged.

**What it leaves out.** Entries with status `held`, `never_translate`, `theme-key`, `dawn-nl` or `locale-present` are left out, as are entries whose value equals the EN, entries with no value and entries with no API route. `legal-review` and `pending-claim-review` are kept but marked, so a run can filter them. Since 22 Oct it also leaves out translations already registered by hand, listed in `registration/registered.json` with their EN sha1: Victor's own NL and FR for the Duo's title, SEO title and meta description. A later EN change brings such an entry back into the plan. Items held by a review decision are listed in `registration/holds.json` per language and stay in the plan with their reason, never written: since R23 (22 Oct) the two dentist-confirmation fields, the legacy “Health Rewards” card and the footer slogan in both languages, and seven FR homepage strings whose current wording stays until it is reviewed, plus the PDP twins of six of them, so homepage and PDP keep one FR wording (the FR lane rewords all of them in a second round).

**Statuses.** Each item has `drafted` and `registered`. `published` is per locale; see Part 4.

| | NL | FR |
|---|---:|---:|
| Payload entries | 2,555 | 2,554 |
| Registration items | 1,827 on 82 resources | 1,821 on 81 resources |
| **First wave** | **522** | **529** |
| Held back | 1,305 | 1,292 |
| Not registered at all | 728 | 733 |

**First wave** (batches 01 homepage, 02 PDP, 03 header/footer, 05 products and 08 system; no gate; no partial field):

| | NL | FR |
|---|---:|---:|
| Homepage | 137 | 135 |
| PDP | 335 | 342 |
| Header/footer | 13 | 11 |
| Products | 34 | 39 |
| System | 3 | 2 |

By resource, NL: `templates/index.json` 135, `templates/product.subscription-item.json` 119, Duo metafields 140, metaobjects 51, 13 selling plans and 4 groups, product titles/SEO and media alts, header/footer groups, 2 menus, `product.json` 14, password 2, list-collections 1.

**Held back:**

- legal: batch 04 and the legal-review gate (NL 605, FR 606);
- collections and blog: batch 07 (NL 589, FR 588);
- pending-claim-review (NL 343, FR 326);
- content pages: batch 06 (NL 20, FR 17);
- partial body fields: a field with a held block (NL 690, FR 688; most are legal and blog).

**Fetched at run time.** GIDs; the theme template keys and digests; the metafields' translatable content (key `value` and its digest, by GID); and the existing NL/FR translations, which are part of the approval snapshot, so the run shows every value it would overwrite and stops if one changes before writing. The full counts and per-resource table are in `docs/localization/registration/DRY-RUN.md`.

**First wave registered (22 Oct 2026).** Victor ran both writes himself after Astra R23: NL 19:29 CEST, checksum `0622fa0b0947ab6f`, 284 keys confirmed in 28 chunks; FR 19:33 CEST, checksum `54845f48d52df704`, 219 keys confirmed in 25 chunks. Both journals have a start and an end record and only confirmed results (`live/journal-<lang>.jsonl`, untracked). Theme text, section groups, media alts, product titles and shop SEO only; no metaobject, metafield, menu, claim-gated, held or Victor-registered entry. The plans are rebuilt afterwards with the decisions of 22 Oct (dentist clause, slogan) for the second round.

**Claims released for publication (22 Oct, Victor).** `registration/releases.json` releases the `pending-claim-review` gate (review later, in all three languages). Plan first wave after the rebuild: NL 600 (was 500), FR 581 (was 484); metaobject fields still need the routing fix.

**Released claims registered (22 Oct 2026).** After Astra R26 Victor wrote the claim-release batch: NL 19:54 CEST, checksum `3eb0d1a95500b9c6`, 62 keys confirmed in 12 chunks; FR, checksum `17fb04ffe2dc0b54`, 58 keys confirmed. Both journals end cleanly. Registered today in total: NL 346, FR 277. Plans rebuilt afterwards with the admin edits of 22 Oct.

## Part 4 · URL and selector baseline (H10)

**Method.** Captured 19 Oct 2026, 22:04 UTC (429 re-check 22:45 UTC), on `karmicares.myshopify.com`.

- Public GETs (`urllib`) of the 49 pages in the NL URL table × EN/NL/FR (147 URLs). Each check records the status without following redirects, `<html lang>`, `hreflang`, canonical and the footer form markup.
- Product pages, home and one content page were also requested with `Accept-Language` en/nl/fr.
- The browser helper checked `/nl` (form 144×40 in the footer, rendered), the NL Duo PDP and an FR legacy-handle product.
- Nothing was clicked or submitted.

| Result | EN | NL | FR |
|---|---:|---:|---:|
| 200 | 46 | 42 | 38 |
| 301 to a legacy translated handle (then 200) | – | 4 | 8 |
| 302 (`/account/login` → hosted accounts, `/password` → home: expected) | 2 | 2 | 2 |
| 404 (`/pages/any-missing-page`, expected) | 1 | 1 | 1 |

- **Every page is reachable at `/nl/…` and `/fr/…`.** All 126 pages that answer 200 have `<html lang>` matching the prefix, a self canonical and `hreflang` en, fr, nl and x-default.
- **NL and FR are already published.** The live `/nl` and `/fr` pages serve 200 with `lang` and `hreflang`, mostly with English content. The homepage, Duo PDP and pages show EN; the older products show legacy NL/FR titles, for example "Complete hygiënekit" and "Brosse à dents du matin". **A registered translation is therefore public at once.**
- **Legacy translated product handles.** These 12 URLs answer 301:
  - NL: `/nl/products/complete-hygiene-kit` → `compleet-hygiene-kit`; `whitening-charcoal-dental-floss` → `whitening-charcoal-flosdraad`; `asleep-evening-toothpaste-2-0` → `asleep-avond-tandpasta-1`; `awake-morning-toothpaste-2-0` → `awake-ochtend-tandpasta-1`.
  - FR: `complete-hygiene-kit` → `kit-d-hygiene-complet`; `morning-toothbrush` → `brosse-a-dents-du-matin`; `evening-toothbrush` → `brosse-a-dents-du-soir`; `whitening-charcoal-dental-floss` → `fil-de-charbon-de-bois-blanchissant`; `evening-toothbrush-2-0` → `brosse-a-dents-du-soir-1`; `morning-toothbrush-2-0` → `brosse-a-dents-du-matin-1`; `asleep-evening-toothpaste-2-0` → `asleep-dentifrice-du-soir-1`; `awake-morning-toothpaste-2-0` → `awake-dentifrice-du-matin-1`.
  - The URL tables in the NL and FR reports assume English handles; both forms work.
- **Browser-language redirect.** Without a locale cookie:
  - A browser asking for `nl` or `fr` is sent (302) to that language on every page type checked.
  - A browser asking for `en` is sent from `/nl/products/…` and `/fr/products/…` to the EN product. On `/nl` and `/nl/pages/…` it stays put.
  - Requests without `Accept-Language` (crawlers) get 200.
  - The browser helper, which had visited `/nl` first, stayed on `/nl/products/…`.
  - Whether the selector's choice overrides the redirect for a new English-browser visitor is untested. The setting behind the redirect is in the admin, not the theme.
- **Footer selector** (`km-footer-locale`):
  - On 123 of the 126 pages that answer 200 (all but `/cart`, whose `kc-redirect` layout has no footer), the form is `POST /localization` with `form_type=localization`, `_method=put`, `return_to` = the current path including the locale prefix, `country_code`, `locale_code`, and links for en/fr/nl and 14 countries.
  - The script copies the clicked value into the hidden input and submits.
  - The group titles render "Language" / "Country/Region" in English on NL/FR today; Part 1 keys them.

### Manual checks for Victor or the preview gate

1. In a new browser profile set to English, open `/nl`, open the footer selector and choose Français. Expect `/fr` (same page).
2. On `/nl/products/karmicare-biorhythmic-oral-care-system`, choose Français. Expect `/fr/products/…`, not `/nl/…`: `return_to` carries `/nl`, and Shopify must re-prefix it.
3. In the same English profile, choose Nederlands on an EN product page. Expect `/nl/products/…`, staying in NL. Check that the browser-language redirect does not send it back to EN, and reload.
4. Switch the country BE → NL, then NL → FR. The language and the page stay.
5. After the theme ships: the picker titles read "Taal / Land/regio" on `/nl` and "Langue / Pays/région" on `/fr`. Spot-check the keyed strings on `/nl` and `/fr`:
   - footer newsletter and consent line;
   - compare table;
   - sticky bar (Duo PDP, scroll);
   - clock captions and messages (drag the knob);
   - FAQ "ALLE"/"TOUT";
   - hero aria-labels.

## Loop handoff (off-limits files)

These are the Loop strings from the inventory. The NL/FR values are in the payloads; FR is now complete for the three R1 strings.

| Where | EN | NL | FR | Note |
|---|---|---|---|---|
| `snippets/loop-widget-standard.liquid:101` | Start here | Begin hier | Commencez ici | homepage fallback (plans_eyebrow empty) |
| `snippets/loop-widget-standard.liquid:103` | Choose how to begin | Kies hoe je begint | Choisissez comment commencer | homepage fallback (plans_heading) |
| `snippets/loop-widget-standard.liquid:109` | Selling Plans | Plannen | Offres | fieldset legend |
| `snippets/loop-widget-standard.liquid:123` | One time Purchase | Eenmalige bestelling | Commande unique | also `assets/loop-widget.js:694`; fit-risk (NL) |
| `snippets/loop-widget-standard.liquid:140` | each | per stuk | l’unité | also line 196; fit-risk (NL) |
| `assets/loop-widget.js:2452` | / {{ days }} days | / {{ days }} dagen | / {{ days }} jours | 60-day plan card |
| `assets/loop-widget.js:2452` (annual) | / year | / jaar | / an | Year plan card |
| `assets/loop-widget.js:2463` | Renews | Verlengd | Se renouvelle | replaces "ships" via `/ships/i`. Once the selling-plan names are registered in NL/FR ("levering om de 60 dagen") the English regex stops matching: key the whole line (NL suggestion "Elke {{ days }} dagen verlengd") |
| `assets/loop-widget.js:2464` | {{ amount }} / brushing | {{ amount }} / poetsbeurt | {{ amount }} / brossage | per-brushing line |
| `assets/loop-widget.js:2468` | Renews every year | Elk jaar verlengd | Se renouvelle chaque année | Year plan card |
| `assets/loop-widget.js:2213` | {{ value }} value · free | t.w.v. {{ value }} · gratis | {{ value }} de valeur · offert | Welcome Kit badge |

Suggested pattern for the Loop owner: the same as the clock. Render `kc.loop.*` keys as data attributes or a decoded JSON block from Liquid and read them in `loop-widget.js`; values can be added to `theme-keys.json` and written with `theme_keys.py`. Never translate: `snippets/loop-subscriptions.liquid:10` "Rendering loop-subscriptions", selling-plan IDs, `handle_item`, "60-Day Supply", "Year Supply".

## Owner decisions needed

1. **Access path.**
   - **A (recommended):** a Dev Dashboard app "Karmicare translations" (scopes `read_translations`, `write_translations`, `read_products`), installed on `karmicares.myshopify.com`, with the client secret in Victor's Keychain and a 24 h token fetched at run time and held in memory.
   - **B:** Translate & Adapt CSV (export emailed to Victor, filled from the plan, imported with overwrite). It needs no token, but its coverage of theme content must be confirmed by a trial export.
   - Choosing A unlocks the online runner task; B needs one export file from Victor.
2. **First-wave scope.** NL 522 / FR 529 items: homepage, Duo PDP, header/footer, products, system, minus legal, blog, content pages, claim-pending and partial fields.
   - NL and FR are already published, so registering is going live.
   - The run will overwrite the legacy NL/FR product titles and texts it touches; the run report lists them first.
   - Recommendation: register the first wave together with the theme keys shipping on `main`.
3. **Published languages.** Keep NL and FR published (today they show mostly English under `/nl` and `/fr`) or unpublish them until the first wave is in. Recommendation: keep them published and register quickly. Unpublishing is an admin action.
4. **Legacy translated handles** (12 URLs above). Keep them (both URL forms work, through 301s), or remove them to match "handles stay English". Recommendation: keep for now, and update the URL tables to the live handles.
5. **Browser-language redirect.** If manual check 3 shows an English-browser visitor cannot stay on `/nl/products/…`, find and change the setting (Markets/domains or an app). This is an admin gate.
6. **Clock gates.** FR holds windows 2–7 as pending-claim-review, but the source links only window 1 (C54). Either the FR reviewer drops the flag on 2–7, or the claims owner confirms them; then run `theme_keys.py refresh` and `write`.

## Files

- `docs/localization/theme-keys.json`, `docs/localization/theme_keys.py` (Part 1 tooling)
- `locales/*.json` (31 storefront files): the `kc` block
- `sections/footer.liquid`, `sections/product-compare-plans.liquid`, `sections/featured-product.liquid`, `sections/main-product.liquid`, `sections/chronobiology-clock-karmicare.liquid`, `assets/chronobiology-clock-karmicare.js`, `sections/km-faq-accordion.liquid`, `snippets/sticky-cart-block.liquid`, `sections/hero-karmicare.liquid`, `sections/stat-strip-karmicare.liquid`, `snippets/product-category-strip.liquid`, `snippets/product-highlights.liquid`, `snippets/professional-testimonials.liquid`
- `docs/localization/registration/build_payloads.py`, `plan-nl.json`, `plan-fr.json`, `DRY-RUN.md` (Part 3)
- `docs/localization/B4-REPORT.md` (this file)
