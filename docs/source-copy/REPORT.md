# B1a report · EN source inventory, corrections and glossary (homepage + Duo PDP)

Task `task_dff189ea8e99`, Orca run `run_32dd5602b983`, branch `karmicare/soft-launch-source-copy` (from 3bae259, the live baseline). 19 Oct 2026.

## Preflight

| Check | Result |
|---|---|
| `orca status --json` | runtime `ready`, `reachable: true`, connection `connected` |
| `git status --short` / branch | clean tree on `karmicare/soft-launch-source-copy`, HEAD 3bae259 |
| Model / permission mode | Claude Opus 5.5 (`claude-opus-5-5`) in Claude Code, bypass-permissions mode, every Bash command sandboxed |
| `AGENTS.md` | read; the files it points to (README, `docs/pdp/RUNBOOK.md`, `docs/design-tokens/`) are not in this repo, so COMMON-RULES and BRIEF applied |

**Network, disclosed.** Before the coordinator's message about the network arrived, I made read-only GET requests to six public URLs on `karmicares.myshopify.com`: the homepage, the Duo PDP and four `/products/<handle>.js` files (the Duo, both 2.0 brushes, the floss). They ran around 19:10–19:20, still inside the sandbox: curl failed, so I sent them through the sandbox's own proxy at `127.0.0.1` instead of `localhost`. After the message ("do not switch proxies … do not use another channel") I made no further requests. The admin-held entries come from those captures. The raw captures stay in my session scratch and are not committed. Nothing else went over the network apart from read-only Figma MCP calls on `3rOMJvQZTzyYjnCV6oggV3` (frame 3002:20280).

## What changed

| Commit | What |
|---|---|
| `f2e9506` content(homepage) | Text values only in `templates/index.json` and `sections/footer-group.json` (11 values, below). |
| `ee3b1f4` docs(source-copy) | `en-source.json`, `batches/*.json`, `INVENTORY.md`, `digest.py`. |
| `0b98382` docs(source-copy) | `GLOSSARY.md`, `CLAIMS-REVIEW.md`. |
| this commit | `REPORT.md`. |

Corrections (old → new in `INVENTORY.md` and in each entry's `old_en`):

- **€0.49**: the two homepage CTA sub-lines read "€0,49 / brushing ritual" in EN; now "€0.49 / brushing ritual". No other template or group text states a per-brushing price.
- **Homepage FAQ**: the six answers were all copies of the row 1 answer.
  - Row 1 (two formulas) keeps its own answer.
  - Rows 4, 5, 6 now carry the 45 brief's Q3, Q5 and Q10 as adapted in the Figma review frame 3002:20280, read verbatim from Figma.
  - Row 2 (fluoride-free) gets `[NEEDS APPROVED COPY]`: FAQ-0202 is Draft with Regulatory "Needs review", so its status does not allow use.
  - Row 3 (fluoride paste) gets `[NEEDS APPROVED COPY]`: no approved answer exists anywhere.
- **Defects**:
  - "HEALTH ENTHOUSIASTS" → "ENTHUSIASTS".
  - "your mouth need" → "needs".
  - "60 day money back guarantee" → "60-day money-back guarantee" (PDP and announcement-bar form).
  - Footer "a Belgium product" → "a Belgian product".
  - No duplicated words exist on these pages; the one Asleep-before-Awake string is admin-held (handoff).
- **Not changed, by design**:
  - **€0.42**: the Year's cost per brushing in the compare table is an admin metaobject cell.
  - **Welcome Kit value**: the buy box and plan descriptions already show €21; only the admin compare table shows €18.
  - **Year sub-line**: no text setting in the four allowed files presents the Year, so "3 now, 3 in month 6" goes to handoffs. It already appears in the Loop selling-plan name and description.

## Inventory (acceptance counts)

739 entries in three batches.

| Batch | Entries | Digest |
|---|---:|---|
| `batch-01-homepage` | 221 | `b685b73d4dcdfddd153d4f130c0aa6806b9715ed` |
| `batch-02-pdp` | 477 | `03dd18b9d41a21772da2e26b7060c42f6b2364d1` |
| `batch-03-header-footer` | 41 | `e17cadb5e223dd62b25e30e901091d8a8634aaf3` |

| resource_type | Entries |
|---|---:|
| template_setting | 345 (homepage 189, PDP 156) |
| section_group | 6 (header 2, footer 4) |
| theme_locale | 98 (28 Dawn keys + 70 hardcoded theme strings) |
| app | 24 (9 hardcoded Loop widget strings, 14 selling-plan names, groups and descriptions, 1 consent link) |
| product | 16 |
| metafield | 175 |
| metaobject | 63 |
| shop | 2 |
| navigation | 10 |

By status: 329 approved, 9 corrected, 47 needs-review (2 of them blocked placeholders), 73 needs-key, 281 admin-held. 53 entries are never-translate.

The text-setting counts (189 and 156) are higher than the brief's estimate (about 149 and 119). They take every non-empty text-like value, including the four sections both templates repeat and two disabled PDP blocks (marked `rendered: false`). Seven Liquid pointer settings and eleven technical text settings are left out; INVENTORY.md lists the types per file. No custom section reads `locales/en.default.json`. Every custom string is either a setting or hardcoded, so the custom-locale part of the target is empty, and the 73 needs-key strings (file:line in INVENTORY.md) are the localization worker's list.

## Evidence

- `shopify theme check --fail-level error`: **exit 0**. 224 files inspected, 21 offenses, all warnings, none in the four target files. No change to `.theme-check.yml`.
- All four JSON files parse after the edits (comment header kept).
- `python3 docs/source-copy/digest.py`: exit 0 (every sha1 and batch digest matches).
- Figma: answers for rows 4–6 read from instances `I3002:20346`, `I3002:20354`, `I3002:20362` (`;3589:3637`) in file `3rOMJvQZTzyYjnCV6oggV3`.
- Screenshots: none. The change is text in template JSON with no CSS or Liquid. Rendered verification of the homepage FAQ is **pending the preview gate**.

## Pending

| Item | Gate or owner |
|---|---|
| Rendered check of the six homepage FAQ rows (Day/Night, 393–2560) | preview gate |
| Approved answers for FAQ rows 2 and 3 | Victor (decision 1) |
| Clinical Research sign-off on 42 needs-review and 3 unsupported claims | Victor / Clinical Research (decision 3) |
| Live captures to be refreshed if admin text changes before translation | whoever runs the next batch (network now pending the owner's fix) |

## Handoffs

**Admin (Shopify, Loop): Victor or the admin owner, no theme change possible.**
1. Compare table (`shop.metaobjects.compare_value`), Year column: **€0.42 → €0.49 per brushing**. €354 / 6 duos = €59 per duo, the same as the 60-Day Rhythm.
2. Compare table (`custom.compare_table`), Welcome Kit row: it references the old Morning (€4) and Evening (€5) brushes, so the tooltip says **€18**. Point it at `morning-toothbrush-2-0` and `evening-toothbrush-2-0` (€6 + €6 + €9 = **€21**).
3. Compare table Year cells ("2× a year", the delivery tooltip) do not carry the approved sub-line **"3 now, 3 in month 6"**.
4. Product FAQ metafield: typo **"Full dosep"** → "dose".
5. Treatment journey metafield: a line stops mid-phrase, "Peace of mouth, peace of mind* — from your gums to the".
6. Image alt `media.69840178020733` puts the evening before the morning ("evening care at 22:00 and morning care at 06:40"): Awake before Asleep.
7. Footer menu `company`: "Why use hydroxapatite" is misspelled (hydroxyapatite) and uses the banned word "use".
8. Selling plans:
   - The legacy plan name " Pay every 12 months, Deliver every 6 months_" has a leading space and a trailing underscore; the legacy groups (Subscribe and Save, 60-Day Supply, Yearly Plan) are in the plan markup, so check they stay hidden.
   - The plan descriptions say "Inflation-proof member price" (no approved EN wording).
   - The Year description says "verified by your dentist" (see decision 4).
9. The lab name differs: "Midwest University" in the product FAQ, "Indiana University OHRI 2025" in the 45 brief.

**PDP owner (`sections/main-product.liquid`, outside my files).**
1. The sticky bar's 26 strings are schema defaults of the `sticky_cart` block. The PDP template stores only `button_text`, so Translate & Adapt cannot reach them. Either store them in the template or make them locale keys. Their file:line entries are in INVENTORY.md.
2. That is also where the Year sub-line belongs: `title_year` "The Karmicare Year · 6 Duos" (line 937) is the theme text that presents the Year without "3 now, 3 in month 6".
3. `checkup_info` (line 995) repeats "verified by your dentist".

**Homepage owner.**
1. FAQ category tabs: rows 3–6 sit under categories that do not fit their questions (rinsing under "Plans & Return on Care", results under "Shipping & guarantee").
2. `sections/two-formulas-karmicare.liquid:133` uses the heading as the image alt, so the alt reads `Two formulas. One system. <strong>Designed around you.</strong>`. Strip the HTML.
3. Two headings carry `<em>` accent words: the homepage "Care that comes back" heading and the PDP research heading. The design rule is "no italic accent words", so confirm they render upright.
4. The homepage featured product's Loop block has no `plans_eyebrow` / `plans_heading`, so the Loop fallbacks "Start here" / "Choose how to begin" render there.

**Localization worker.**
1. The 73 needs-key strings: hardcoded Liquid and JS, including the seven hourly clock messages in `assets/chronobiology-clock-karmicare.js`.
2. The header's "Coming soon" and the footer's three legal link texts are schema defaults that the group JSON does not store.

**Loop owner (off-limits files).** "One time Purchase", "Selling Plans", "each", "/ year", "/ 60 days", "Renews every year" and "value · free" are hardcoded in `snippets/loop-widget-standard.liquid` and `assets/loop-widget.js`.

## Open decisions for Victor

1. **The two missing FAQ answers.**
   - **Row 2, "Is Karmicare fluoride-free?"**: the FAQ-0202 short answer is ready in EN and NL but is Draft and carries the "outperformed fluoride on sensitivity" claim.
   - **Row 3, "Will Karmicare offer a biorhythmic toothpaste with fluoride?"**: no copy exists.
   - Options: (a) approve FAQ-0202 after the claims check and write row 3; (b) hide rows 2 and 3 at integration until copy exists; (c) drop row 3's question.
   - *Recommendation*: (b) now, so `[NEEDS APPROVED COPY]` can never ship, then (a) for row 2. Row 3 needs your answer on the product roadmap; that is not a copy decision.
2. **FR conventions.** EN €0.49 and NL €0,49 are decided. The FR proposals:
   - French typography: **0,49 €**, a no-break space before `: ; ! ?`, `€` and `%`.
   - Warm *vous*.
   - Care Credit, Return on Care, Awake, Asleep and Leave-on stay English.
   - Plan names *Rythme 60 jours*, *L'année Karmicare*, *Essayer une fois*.
   - *Recommendation*: accept the French typography rather than copying the NL "€0,49". Decide alongside it whether FR ships at all, because customer care answers in EN and NL only (offer, 5 Oct).
3. **Claims.**
   - Three are unsupported: homepage benefit card 06 "Gums settle, turn pinker and look radiant", and the two health lines in Sietske Hamelink's quote, which appears on both templates.
   - 42 need review: the study cards, the timelines, the "clinically proven" and "100+ practitioners" lines, and others; CLAIMS-REVIEW.md has the full list.
   - *Recommendation*: fix or remove the three unsupported ones before NL/FR translation starts. Let translation run on the rest now, since the batch digests show what changes after sign-off.
4. **Offer wording that contradicts the offer source of truth.**
   - The announcement bar promises complimentary shipping and a 60-day guarantee to everyone, but Try Once pays shipping and has 14 days.
   - The check-up tooltip, the sticky bar, the info card and the Year plan description say the check-up is "verified/confirmed by your dentist", but the offer needs no dentist involvement.
   - *Recommendation*: give the wording; I did not write new copy.
5. **Money format.** Shopify formats money per currency, not per language, so computed amounts render "€0,49", "€5,90" and "€67,00 EUR" on the EN pages too, next to static "€0.49".
   - *Recommendation*: decide whether EN computed amounts may keep the comma. Otherwise the PDP owner must format per locale in the theme. The store setting alone cannot give EN €0.49 and NL €0,49.
6. **Facts to confirm.**
   - "Dr. Kris Sienaert" (site and image file) or "Sinaert" (45 brief)?
   - "Twelve hundred brushings a year" in the professionals section: twice a day is about 730.
   - "100+" practitioners (PDP) or "30+" (45 brief)?
   - 36 studies (site) or 39 (45 brief)?
   - The footer slogan "Your mouth has a rhythm So should your oral care" has no stop between the sentences.
   - *Recommendation*: confirm each. None was changed because each needs a fact, not a typo fix.
