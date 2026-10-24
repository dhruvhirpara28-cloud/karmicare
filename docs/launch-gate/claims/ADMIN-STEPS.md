# Claims cleanup · admin steps for Victor (R59, 24 Oct 2026)

Lane gate-claims. Everything below happens in Shopify admin, which the lane may not write. Each step gives the menu path, the field, the old value and the new value, ready to paste. Items a–k follow section 2 of `docs/launch-gate/input/claims/02-PRIORITEITEN-VICTOR.md`; the reasoning is in `docs/launch-gate/input/claims/CLINICAL-REVIEW.md` (CR1). The theme items are in `REPORT.md`.

Live state was read once on the public Duo page on 24 Oct 2026 (`https://karmicares.myshopify.com/products/karmicare-biorhythmic-oral-care-system`, HTTP 200). "Verified" below means that read.

## 1. The five admin items from the priorities list

| # | Where | Status 24 Oct | What to do |
|---|---|---|---|
| a | Plans table, row "The Karmicare Year", cost per brushing | **Live shows €0.49** (three times on the page, no €0.42). The theme computes the brushing row from the plan price (`sections/product-compare-plans.liquid`, €354 ÷ 720 brushings), so the stored value is only the fallback. | Low priority, 1 min: fix the stored value so the fallback is right. See step a. |
| b | Comparison table, Welcome Kit tooltip | **Live shows "Welcome Kit · €21 Value · Free"**. The €18 value is gone. | Nothing to change. Optional check: step b. |
| c | PDP safety block, RDA line | Live: "Midwest University · RDA 93 Awake, 72 Asleep · ISO 11609 limit 250". | **No change (Victor, 24 Oct):** the lab does not want to be named in marketing, so "Midwest University" stays. Open question below. |
| j | Comparison table, row "It reaches past your teeth" | **Still live**: "It reaches past your teeth · Oral-gut-brain, deeper than enamel · Mechanical cleaning only · Systemic, not oral · Stops at the skin". | Step j, 2 min. |
| k | Treatment journey, "First night" | **Still live**: "First night — feel the repair, it keeps working while you sleep". | Step k, 1 min. |

### Step a · Year cost per brushing (stored value)

- Path: Admin → Content → Metaobjects → **Compare value** (`compare_value`) → the entry whose plan is **The Karmicare Year** and whose row is the **cost per brushing** row (handle contains `brushing`).
- Field: **value**
- Old: `€0.42`
- New: `€0.49`
- Why: the Year costs €59 per duo as well (€354 ÷ 6 duos ÷ 120 brushings = €0.49). The theme already shows €0.49 because it calculates this row; the stored value only shows if that calculation is ever switched off.

### Step b · Welcome Kit value (verify only)

- Path: Admin → Products → **Karmicare Biorhythmic Oral Care System** → Metafields → **Compare table** (`custom.compare_table`) → **Welcome Kit row** → **products**
- Expected: Morning Toothbrush 2.0 (`morning-toothbrush-2-0`), Evening Toothbrush 2.0 (`evening-toothbrush-2-0`) and the charcoal floss. Together they make the €21 the page shows today.
- If the list still names the old €4 and €5 brushes, replace them with the 2.0 brushes. Nothing else.

### Item c · RDA lab name (kept)

- Victor, 24 Oct: keep "Midwest University"; the lab (Indiana University School of Dentistry, OHRI, report 25-RDA-123) does not want to be mentioned in marketing. No admin change.
- For the record: CR1 (C92) and the launch audit LR1 flagged the name as not matching the report. If a reviewer asks, the answer is that the name is deliberate; a neutral form such as "Independent university laboratory · RDA 93 Awake, 72 Asleep · ISO 11609 limit 250" would avoid both naming the lab and a name that does not exist. Victor's call.
- **Open question (Victor):** was the formula tested in 25-RDA-123 already v2? The report names no formula version and INCI v2 dates from 3 June 2026 (CR1 §5). If the tested batches were v1, plan a re-review of the RDA line.

### Step j · Remove the oral-gut-brain row

- Path: Admin → Products → **Karmicare Biorhythmic Oral Care System** → Metafields → **Comparison section** (`custom.comparison_section`, metaobject) → rows → the row labelled **It reaches past your teeth** (CR1 index `comparison_section#21`).
- Action: **delete the row** (or set it to hidden if the metaobject has a show/hide field).
- Old values in that row: label `It reaches past your teeth` · Karmicare `Oral-gut-brain, deeper than enamel` · other columns `Mechanical cleaning only`, `Systemic, not oral`, `Stops at the skin`.
- Why: no study shows an oral-care formula acting on the gut–brain axis; no compliant wording keeps "reaches past your teeth" (CR1, C42, not supportable).

### Step k · First night line of the treatment journey

- Path: Admin → Products → **Karmicare Biorhythmic Oral Care System** → Metafields → **Treatment journey list** (`custom.treatment_journey_list_one`, or `..._list_two` if "First night" sits in the second list) → the item that starts with **First night**.
- Old: `First night — feel the repair, it keeps working while you sleep`
- New: `First night — Leave-on: it works after the brush`
- Why: no source for a felt repair or for activity through the night; "repair" is restorative framing (CR1, C98, not supportable). The new line is the approved leave-on wording (C10).

## 2. Blog posts to unpublish

Verdicts and reasons per article are in `REPORT.md` §5. Path for each: Admin → Online Store → **Blog posts** → open the post → **Visibility: Hidden** → Save. Hiding the post hides its NL and FR versions too (they are translations of the same post).

Unpublish now (no compliant core remains):

| Handle | Title | One-line reason |
|---|---|---|
| `benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood` | Benefits of Nootropics: Ease Stress, Boost Focus and Improve Mood | The whole article sells guarana and valerian in a toothpaste as focus, energy and sleep aids (brand don't #16), cites ADHD and Alzheimer's treatment, and says fluoride "disturbs your wake/sleep cycles". |
| `how-oral-health-impacts-your-overall-wellness` | How Oral Health Impacts Your Overall Wellness | Calls fluoride a "human developmental neurotoxicant", promises "prevent gum disease, fight tooth decay", "protection against cavities and gum disease", guarana and valerian for cognition and sleep, "complete wellness in a tube"; the association part is already covered by the sleep research card. |
| `5-reasons-you-should-avoid-fluoride-in-toothpaste` | 5 Reasons You Should Avoid Fluoride in Toothpaste | Anti-fluoride medical claims (IQ, thyroid, bones, pineal gland, sleep), "superior to fluoride" (brand don't #13), "repairs areas of decay", "safe to swallow", "guarantees the quality and safety". |
| `headaches-and-tooth-pain-understanding-the-connection` | Headaches and Tooth Pain: Understanding the Connection | Medical content (abscesses, migraines, referred pain) ending in "prevents and manages dental abscesses", "protect against cavities", "prevent gingivitis and periodontitis": disease treatment and prevention claims. |

Unpublish **at the domain switch unless rewritten by then** (topic worth keeping, text not):

| Handle | Title | Why it cannot stay as it is |
|---|---|---|
| `nano-hydroxyapatite` | Discover the Wonderful Inner World of Nano Hydroxyapatite… | "help prevent tooth decay", "repairs areas of decay", "ingesting poison everyday", "zero side effects", "your toddler could swallow it", "work all night", NASA origin story, guarana and valerian as energy and wind-down aids. |
| `morning-and-night-time-brushing-why-timing-matters` | Morning and Night Time Brushing: Why Timing Matters | "prevents cavities", "reduces tooth decay and gum disease", "medical-grade activated charcoal", "immediately repairs and remineralizes", "soothes gums", "24/7 protection". |
| `top-natural-whitening-toothpaste-for-a-brighter-smile` | Top Natural Whitening Toothpaste For a Brighter Smile | "preventing cavities", "prevents cavities", "safe for everyone, including kids and pregnant women", "detoxifying", "removing toxins", aloe vera and coconut oil that are not in the formula, "revolutionary". |
| `3-reasons-why-you-should-look-for-an-sls-free-toothpaste` | 3 Reasons Why you Should look for an SLS Free Toothpaste | "say goodbye to persistent canker sores" (condition endpoint), "safe to swallow", named competitors (Colgate, Biotene, Sensodyne, Tom's of Maine; brand don't #2), "the most effective SLS-free toothpaste", charcoal floss "whitens". |

## 3. Recommended, not in a–k (CR1 advice, Victor decides)

These sit in the same admin metafields and were flagged by CR1 but are not on the priorities list. No deadline from the lane; listed so they are not forgotten.

| Where (CR1 id) | Live now (24 Oct) | CR1 wording |
|---|---|---|
| `custom.treatment_journey_list_*`, week headings (C94–C98) | "Week 1 — sensitivity starts to fade, the mineral layer builds", "Week 2 — calmer gums, fresher breath…", "Week 4 — …", "Week 6 — weak spots remineralised, enamel stronger", "By day 60 — …" | Drop the week headings; keep untimed lines: "— nano-hydroxyapatite helps reduce sensitivity", "— fresher breath, morning and night", "— less plaque; supports your mouth's own balance", "— helps remineralise and strengthen enamel". |
| `custom.product_faq#43` and `#96` (C90, C91) | "Safe for children. Safe when swallowed." and the chip "Safe to swallow" | Cut "Safe when swallowed" and the chip until the CPSR supports them; replace "Safe for children" with the leaflet's age line (from age 3, under supervision). |
| `custom.product_faq#72` (C67) | "Formulated on 36 peer-reviewed studies" | "Formulated on peer-reviewed studies" (same change as the theme's stat strip and highlights, done in R59). |
| `custom.product_faq#14` (C37) | "Xylitol, balances the oral microbiome" | "Xylitol, supports oral microbiome balance". |
| `custom.product_faq#102` (C44) | "Formulated without fluoride and without known endocrine-active ingredients" | "Formulated without fluoride, for practitioners who run thyroid- and pineal-aware protocols…" (full line in CR1). |
| `custom.product_faq#104` (C46) | "Awake for the cortisol morning, Asleep for the repair night — supporting the natural recovery process instead of interrupting it." | "Awake for the morning, Asleep for the night: care timed to your biology." |
| `custom.comparison_section#15–16` (C45) | "You feel it straight away" in the guarana/valerian row | "You feel the smooth finish straight away", row label as flavours "Mint and lime by day, cinnamon and orange by night". |
| Product title of the floss (C100) | "Whitening Charcoal Floss" | "Charcoal Floss" (handle stays). |
