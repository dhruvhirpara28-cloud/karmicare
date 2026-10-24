# Claims cleanup · R59 report (lane gate-claims, 24 Oct 2026)

Launch blocker 3 of `docs/launch-gate/input/LR1-LAUNCH-READINESS.md`: the claims on the cleanup list (`input/claims/02-PRIORITEITEN-VICTOR.md` §2, items a–p; reasoning in `input/claims/CLINICAL-REVIEW.md`, CR1). Branch `karmicare/gate-claims` over `karmicare/soft-launch` @ `5bab3ad`.

Victor reviewed the first pass in the session on 24 Oct and decided three times: he kept seven items as they were, then asked for the product page to be restored entirely (it was already approved) and for all five research cards to come back on the homepage, and finally extended the gum card line to "A velvety foam nurturing your gums through fermentation." §1 shows the result per item. His keeps are decisions, not oversights.

## Summary

- **Theme (homepage only, `templates/index.json`):** the guarana/valerian benefit card reworded (heading as advised, text Victor's: "Guarana helps keep plaque from sticking (in vitro). Valerian soothes the mouth by night."), the practitioner footer without "the one prevented" and "twelve hundred brushings", the gum card and the leave-on card with Victor's lines, "+36 studies" without the number, BIOFILM PREVENTION → HELPS REDUCE BIOFILM. The stat-strip and two-formulas section defaults carry the same two wordings.
- **Unchanged on Victor's instruction (24 Oct):** the whole product page template; the five research cards and the research intro ("Meta-analyses … more than 38,000 people"); "Nano-HAp beat fluoride on tooth sensitivity"; "Cold or hot, no hesitation"; "settle gums" in the benefits intro; Sietske Hamelink's card; Dr. Spreuwers' full quote; "Midwest University" on the PDP.
- **Admin (paste-ready in `ADMIN-STEPS.md`):** j (oral-gut-brain row) and k (First night line) still live; a and b already right on the live page; c kept by Victor. Four blog posts to unpublish now, four to rewrite or unpublish at the switch.
- **Checks:** Theme Check 0 errors, 19 baseline warnings; both templates parse as JSON; no block hidden, no layout change, so no visual check needed.
- **Open:** the v2-formula question on the RDA report (`ADMIN-STEPS.md`, item c).

## 1. Items a–p

| # | Item | Result |
|---|---|---|
| a | Year cost per brushing €0.42 → €0.49 (metaobject) | Live already shows €0.49 (the theme computes it from the price). Stored value: `ADMIN-STEPS.md` step a, low priority. |
| b | Welcome Kit €18 → €21 (compare_table) | Live already shows "€21 Value". Verify only. |
| c | "Midwest University" → "Indiana University (OHRI)" | **Kept** (Victor, 24 Oct: the lab does not want to be named in marketing). Note in `ADMIN-STEPS.md`. |
| d | Gum card "Radiant calm gums" | Heading kept; text now **"A velvety foam nurturing your gums through fermentation."** (Victor's line, replaces "No SLS. Gums settle, turn pinker and look radiant."). `index.json` `card_VP8KGi`. |
| e | "Focus by day, calm by night" card | Heading as advised: "Guarana by day, valerian by night". Text, Victor's choice (24 Oct, measured to fit three lines in EN, NL and FR on the desktop card): **"Guarana helps keep plaque from sticking (in vitro). Valerian soothes the mouth by night."** The guarana half keeps CR1's in-vitro qualifier (Yamaguti-Sasaki 2007, adherence of S. mutans to glass). "Soothes" is on the allowed list in `regulatory.md`; it is a local, sensory claim, not a calm or sleep effect, so don't #16 is not touched. The library holds no oral study on valerian, so this is **Victor's decision**: the safety assessor should confirm the soothing / skin-conditioning function of valerian root extract in the product file. `card_KRCrBY`. |
| f | Xylitol research card | **Kept visible** (Victor, 24 Oct: all five research cards back), both templates. |
| g | SLS research card | **Kept visible** (same). |
| h | 98 % research card | **Kept visible** (same). |
| i | Sietske Hamelink card | **Kept visible** (Victor, 24 Oct). |
| j | Oral-gut-brain comparison row | Admin: `ADMIN-STEPS.md` step j. Still live on 24 Oct. |
| k | "First night — feel the repair…" | Admin: `ADMIN-STEPS.md` step k. Still live on 24 Oct. |
| l | "Nano-HAp beat fluoride on tooth sensitivity" | **Kept** with its result line (Victor, 24 Oct). |
| m | Research intro "38,000 people / top of the evidence hierarchy" | **Kept** (Victor, 24 Oct: research facts; no "not tested on Karmicare" sentence). With all five cards visible the line matches the cards again. |
| n | Leave-on card "It works all night" | Now **"Spit, don’t rinse. With you all night. Feel it before breakfast."** (Victor's line). `card_AGFiEX`. |
| o | "Cold or hot, no hesitation" | **Kept** (Victor, 24 Oct). |
| p | Practitioner footer | Done as advised on the **homepage**: "These practitioners recommend Karmicare between visits. Not to replace their care, but to make the brushings between appointments count for something." The product page keeps its approved text ("The best outcome is the one prevented … twelve hundred brushings a year"), so the two pages differ in this one sentence. |

## 2. Changed beyond a–p (clear cases from the scan, brief step 3)

| Where | Was | Now | Rule |
|---|---|---|---|
| `index.json` `stat_strip_karmicare/stat_3/text` | Formulated on +36 studies | Formulated on peer-reviewed studies | unsupported number (CR1 C65) |
| `index.json` `two_formulas_karmicare/ingredients_list` | BIOFILM PREVENTION | HELPS REDUCE BIOFILM | "prevents" (CR1 C33; NL/FR payloads already hold this form) |
| `sections/stat-strip-karmicare.liquid` default + preset | Formulated on +36 studies | Formulated on peer-reviewed studies | schema default |
| `sections/two-formulas-karmicare.liquid` default | BIOFILM PREVENTION | HELPS REDUCE BIOFILM | schema default |

Reverted on Victor's instruction (product page already approved): the PDP highlights chips "Used by 100+ kPNI practitioners & functional dentists" and "Clinically proven ingredients · 36 peer-reviewed studies" (CR1 C81, C66) and the matching `sections/main-product.liquid` defaults; the `sections/research-behind-system.liquid` card defaults. They are listed in §3 as R14 and R15 so the register keeps them.

Not touched: `link_url` of every research card (study-links lane, R55).

## 3. Scanned, listed only (proposed fix, not changed)

Both templates and every `sections/*` default were read for disease words, fluoride superiority, detox, hormones, "prevents", "repairs", guarana or valerian effects and unsupported numbers. What remains, with a proposed fix; none of these were changed.

| # | Where | Text | Why it is listed | Proposed |
|---|---|---|---|---|
| R1 | Dr. Stephanie Spreuwers quote, `trusted_professionals_HAqYth/card_h8d3WL/hover_text`, both templates | "(with guarana for morning energy)" and "(with valerian, which contributes to calm and relaxation)" | Guarana energy and valerian calm effects in a testimonial (brand don't #16; the cosmetic claims criteria say a testimonial does not bypass substantiation, LR1) | **Accepted risk, Victor 24 Oct:** he approved her full quote including these lines ("het is haar ervaring"); the quote stays as it is, not hidden, not edited. Listed so the decision stays visible to the regulatory reviewer. |
| R2 | Chronobiology clock `morning_text`, both templates | "Cortisol rises; coffee, breakfast and the day's first acids follow…" | Hormone named with no primary source (CR1 C53, supported if reworded) | "Morning brings coffee, breakfast and the day's first acids. Enamel needs its shield on first." |
| R3 | Chronobiology clock `night_text`, both | "Melatonin rises and saliva slows to a trickle. What's on your enamel at 22:00 is still there at 07:00." | Second sentence has no source and the overnight biofilm changes (CR1 C52) | "Melatonin rises and saliva slows while you sleep." |
| R4 | Chronobiology clock `night_title`, both, and the section default | "Your mouth switches to repair" | "repair" is the body's own; not a product claim. Reviewed, kept. | Keep. |
| R5 | FAQ `faq_item_TNnqTQ/answer` and the `km-faq-accordion` default | "Night is repair … so Asleep soothes, rebalances and remineralises while you sleep." | Same duration claim as C12/C14 ("while you sleep"); consistent with Victor's "With you all night" on the card. | If the card line ever changes: "…remineralises after the brush." |
| R6 | PDP `loop_subscriptions_WEk4XJ/pricing_summary_checkup_tooltip` and the `main-product` default | "Prevention, rewarded." | "Prevention" next to the formula reads as a prevention claim (CR1 C70 reasoning). Here it is the dental check-up that is rewarded, which is Victor's deliberate framing. | Keep, or "The visit, rewarded." |
| R7 | `stat_strip_karmicare/tagline`, index | "CHOSEN BY KPNI PRACTITIONERS, FUNCTIONAL DENTISTS, HEALTH PROFESSIONALS" | Endorsement; needs consent records, not a health claim (CR1 C80). | Keep once the consent file exists. |
| R8 | Hero `testimonial_badge/rating_text`, index | "4.8 (234)" | No review data behind it (CR1 C82; LR1 "unsupported review totals"). Reviews lane owns it. | Handoff to the reviews lane. |
| R9 | `stat_3/heading` "Clinically backed" and research `subheading` "CLINICALLY BACKED ORAL CARE", both | CR1 did not rule on it; defensible as ingredient evidence. | Keep; if a reviewer objects: "Peer-reviewed" / "THE RESEARCH". |
| R10 | Clock messages 1–7 (`locales/en.default.json`, `kc.clock.window_*`) | "least protected", "repair window", pH timings | CR1 C54: trim 1, 6, 7, hold 2–5. Locales are off-limits for this lane. | Handoff to source-copy. |
| R11 | `card_jN7XcL/text`, index | "All the minerals your mouth needs in one press." | Absolute, but a dosing line, not a health claim. | Keep. |
| R12 | `two_formulas_karmicare/right_heading`, index | "Purified and restored by night" | Brand framing (Awake activation, Asleep restoration); not detox. | Keep. |
| R13 | Disabled FAQ items `faq_item_7jmEGi` ("Fluoride and nano-hydroxyapatite compete…") and `faq_item_AL3DKF` ("Fluoride's benefits don't outweigh its known drawbacks") | Hidden already. | Keep hidden; re-enabling needs a review. |
| R14 | PDP `highlights_slider_9wAjAb/text_1` | "Used by 100+ kPNI practitioners & functional dentists" | Unsupported number and the banned word "used" (CR1 C81). Victor, 24 Oct: the product page is approved as it is. | "Chosen by kPNI practitioners & functional dentists" when a dated count or the consent file exists. |
| R15 | PDP `highlights_slider_9wAjAb/text_2` | "Clinically proven ingredients · 36 peer-reviewed studies" | Unsupported number, "clinically proven" (CR1 C66). Same decision. | "Formulated on peer-reviewed studies", as the homepage stat strip now says. |
| R16 | Research cards `card_fmFMFd` (xylitol, tooth decay), `card_JeERX6` (SLS, canker sores), `card_bDxUVT` (98 % tubules), both templates | Disease endpoints next to the formula (CR1 C62, C64) and whitepaper figures without the paper in the library (C60). Victor, 24 Oct: all five cards stay. | CR1's qualified wordings if a reviewer requires them: "In trials of xylitol gum, lozenges and syrup, xylitol was linked with less tooth decay than controls." and "In people prone to mouth ulcers, SLS-free formulas meant fewer and shorter ulcers."; add Kulal 2016 to the library for the 98 % card. |

## 4. Blog articles (Shopify sitemap, read 24 Oct)

`sitemap_articles_1.xml` lists eight posts in `blogs/news`; the `/nl/` and `/fr/` article maps are the translations of the same eight. Each was fetched once (rate-limited to one request per three seconds) and read in full.

| Handle | Verdict | One-line reason against `regulatory.md` and CR1 |
|---|---|---|
| `nano-hydroxyapatite` (Dec 2023, 3,100 words) | **rewrite** (keep the URL; the nHAp explainer is the brand's core topic) | "help prevent tooth decay", "repairs areas of decay", "ingesting poison everyday", "zero side effects", "toddler could swallow it", "work all night", NASA origin story, guarana/valerian as energy and wind-down aids. |
| `morning-and-night-time-brushing-why-timing-matters` | **rewrite** (short; the Awake/Asleep timing story) | "prevents cavities", "reduces tooth decay and gum disease", "medical-grade activated charcoal", "immediately repairs and remineralizes", "soothes gums", "24/7 protection". |
| `benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood` | **unpublish** | Entire article is guarana/valerian focus, energy and sleep claims in a toothpaste (don't #16), ADHD/Alzheimer's treatment, "fluoride disturbs your wake/sleep cycles"; LR1 already drops the nootropics paths from the redirect map. |
| `how-oral-health-impacts-your-overall-wellness` | **unpublish** | Fluoride "neurotoxicant", "prevent gum disease, fight tooth decay", "protection against cavities and gum disease", nootropic cognition and sleep claims, coconut oil not in the formula, "complete wellness in a tube". |
| `top-natural-whitening-toothpaste-for-a-brighter-smile` | **rewrite** (whitening through remineralisation is an allowed cosmetic topic) | "preventing/prevents cavities", "safe for everyone, including kids and pregnant women", "detoxifying", "removing toxins", aloe vera and coconut oil not in the formula, "revolutionary". |
| `5-reasons-you-should-avoid-fluoride-in-toothpaste` | **unpublish** | Anti-fluoride medical claims (IQ, thyroid, bones, pineal, sleep), "superior to fluoride" (don't #13), "repairs areas of decay", "safe to swallow", "guarantees"; fluoride-free stays factual only. |
| `headaches-and-tooth-pain-understanding-the-connection` | **unpublish** | Medical content closing on "prevents and manages dental abscesses", "protect against cavities", "prevent gingivitis and periodontitis". |
| `3-reasons-why-you-should-look-for-an-sls-free-toothpaste` | **rewrite** (SLS vs glycolipids is a keep-worthy explainer) | "say goodbye to persistent canker sores", "safe to swallow", named competitors (don't #2), "the most effective SLS-free toothpaste", charcoal floss "whitens". |

The unpublish list, and the rule "rewrite before the switch or unpublish at the switch" for the other four, are in `ADMIN-STEPS.md` §2. Rewrites are a later task.

## 5. Translations

`TRANSLATIONS-HANDOFF.md`: seven changed strings, all in `templates/index.json`, with block id, setting key, EN, NL and FR. Includes the warning that a registered translation of a changed key goes outdated in Shopify, so NL and FR register with the theme release.

## 6. Checks run

- `shopify theme check --fail-level error --output json`: exit 0, 0 errors, 19 warnings (the baseline). Run on the final theme state.
- Both templates parsed as JSON after the edits; `product.subscription-item.json` is byte-identical to `5bab3ad`.
- The earlier two-card research marquee was checked live at 1440 and 390, Day and Night, in an anonymous Orca profile (profile deleted after); with all five cards back that state no longer exists, so the screenshots were dropped from the lane folder.
- Live reads, 24 Oct, one request each: homepage (browser), Duo page (HTML), sitemap index, articles sitemap, eight articles.
- No admin writes, no app installs, no CLI login, no `theme dev`, no form, cart or checkout.

## 7. Handoffs

| To | What |
|---|---|
| source-copy | Register the seven strings in `TRANSLATIONS-HANDOFF.md` in `en-source.json`, the batches and the NL/FR payloads; update the CLAIMS-REVIEW register (C33, C40, C41, C65, C70 applied on the homepage; C12, C21, C34, C35, C52, C53, C60–C64, C66, C68, C81, C84, C85, C92 decided by Victor as "keep" on 24 Oct); the clock messages (R10). |
| reviews lane | "4.8 (234)" in the hero badge (R8). |
| study-links (R55) | Nothing changed in the research cards or their `link_url`. |
| gate-consent | The anonymous homepage load showed the Shopify cookie banner (Accept / Decline / Manage preferences); no consent was given. For their record only. |
| Victor | `ADMIN-STEPS.md` steps a (low), j, k; the four unpublishes; the v2-formula question on the RDA report. |

## 8. Input files

`docs/launch-gate/input/` is untracked in this worktree (placed by the coordinator); this lane did not commit it. The three outputs live in `docs/launch-gate/claims/`.
