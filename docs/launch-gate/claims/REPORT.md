# Claims cleanup · R59 report (lane gate-claims, 24 Oct 2026)

Launch blocker 3 of `docs/launch-gate/input/LR1-LAUNCH-READINESS.md`: the claims on the cleanup list (`input/claims/02-PRIORITEITEN-VICTOR.md` §2, items a–p; reasoning in `input/claims/CLINICAL-REVIEW.md`, CR1). Branch `karmicare/gate-claims` over `karmicare/soft-launch` @ `5bab3ad`.

Victor reviewed the first pass in the session on 24 Oct and kept seven items as they were; §1 shows the result per item. His keeps are decisions, not oversights.

## Summary

- **Theme (done, both templates where the block exists):** three research cards hidden (xylitol tooth decay, SLS canker sores, 98 % tubules), the guarana/valerian benefit card reworded, the practitioner footer without "the one prevented" and "twelve hundred brushings", the gum card with Victor's line, the leave-on card with Victor's line, "+36 studies" and "36 peer-reviewed studies" without the number, "Used by 100+" → "Chosen by", BIOFILM PREVENTION → HELPS REDUCE BIOFILM. Four section schema defaults carry the same wording so a freshly added block no longer starts from a removed claim.
- **Kept on Victor's instruction (24 Oct):** "Nano-HAp beat fluoride on tooth sensitivity" with its result line, the research intro ("Meta-analyses … more than 38,000 people"), "Cold or hot, no hesitation", "settle gums" in the benefits intro, Sietske Hamelink's practitioner card, "Midwest University" on the PDP.
- **Admin (paste-ready in `ADMIN-STEPS.md`):** j (oral-gut-brain row) and k (First night line) still live; a and b already right on the live page; c kept by Victor. Four blog posts to unpublish now, four to rewrite or unpublish at the switch.
- **Checks:** Theme Check 0 errors, 19 baseline warnings; both templates parse as JSON; the two-card research marquee checked at 1440 and 390, Day and Night (screens in `screens/`).
- **Open:** one question to Victor on Dr. Spreuwers' quote (guarana energy, valerian calm), sent through the coordinator; the v2-formula question on the RDA report.

## 1. Items a–p

| # | Item | Result |
|---|---|---|
| a | Year cost per brushing €0.42 → €0.49 (metaobject) | Live already shows €0.49 (the theme computes it from the price). Stored value: `ADMIN-STEPS.md` step a, low priority. |
| b | Welcome Kit €18 → €21 (compare_table) | Live already shows "€21 Value". Verify only. |
| c | "Midwest University" → "Indiana University (OHRI)" | **Kept** (Victor, 24 Oct: the lab does not want to be named in marketing). Note in `ADMIN-STEPS.md`. |
| d | Gum card "Radiant calm gums" | Heading kept; text now **"A velvety foam nurturing your gums."** (Victor's line, replaces "No SLS. Gums settle, turn pinker and look radiant."). `index.json` `card_VP8KGi`. |
| e | "Focus by day, calm by night" card | Done as advised: "Guarana by day, valerian by night" · "Guarana helps keep plaque bacteria from sticking (in vitro). Valerian root, chosen for the evening formula." `card_KRCrBY`. |
| f | Xylitol research card | Hidden (`"disabled": true`), `card_fmFMFd`, both templates. |
| g | SLS research card | Hidden, `card_JeERX6`, both. |
| h | 98 % research card | Hidden, `card_bDxUVT`, both. |
| i | Sietske Hamelink card | **Kept visible** (Victor, 24 Oct). |
| j | Oral-gut-brain comparison row | Admin: `ADMIN-STEPS.md` step j. Still live on 24 Oct. |
| k | "First night — feel the repair…" | Admin: `ADMIN-STEPS.md` step k. Still live on 24 Oct. |
| l | "Nano-HAp beat fluoride on tooth sensitivity" | **Kept** with its result line (Victor, 24 Oct). |
| m | Research intro "38,000 people / top of the evidence hierarchy" | **Kept** (Victor, 24 Oct: research facts; no "not tested on Karmicare" sentence). |
| n | Leave-on card "It works all night" | Now **"Spit, don’t rinse. With you all night. Feel it before breakfast."** (Victor's line). `card_AGFiEX`. |
| o | "Cold or hot, no hesitation" | **Kept** (Victor, 24 Oct). |
| p | Practitioner footer | Done as advised: "These practitioners recommend Karmicare between visits. Not to replace their care, but to make the brushings between appointments count for something." Both templates. |

After f, g and h the research section shows two cards: sleep (Lei & Hu 2025) and sensitivity (Vano 2018). The kept intro still says "alongside laboratory studies" and "more than 38,000 people"; the 38,000 add up only with the hidden xylitol and SLS trials (CR1, C68). Victor keeps the line as a statement about the evidence base; if he would rather have the cards back than the line without them, that is a one-line change (remove the three `"disabled": true`).

## 2. Changed beyond a–p (clear cases from the scan, brief step 3)

| Where | Was | Now | Rule |
|---|---|---|---|
| `index.json` `stat_strip_karmicare/stat_3/text` | Formulated on +36 studies | Formulated on peer-reviewed studies | unsupported number (CR1 C65) |
| `index.json` `two_formulas_karmicare/ingredients_list` | BIOFILM PREVENTION | HELPS REDUCE BIOFILM | "prevents" (CR1 C33; NL/FR payloads already hold this form) |
| `product.subscription-item.json` `highlights_slider_9wAjAb/text_1` | Used by 100+ kPNI practitioners & functional dentists | Chosen by kPNI practitioners & functional dentists | unsupported number, banned word "used" (CR1 C81 interim) |
| `product.subscription-item.json` `highlights_slider_9wAjAb/text_2` | Clinically proven ingredients · 36 peer-reviewed studies | Formulated on peer-reviewed studies | unsupported number (CR1 C66) |
| `sections/stat-strip-karmicare.liquid` default + preset | Formulated on +36 studies | Formulated on peer-reviewed studies | schema default |
| `sections/two-formulas-karmicare.liquid` default | BIOFILM PREVENTION | HELPS REDUCE BIOFILM | schema default |
| `sections/research-behind-system.liquid` card defaults | the 98 % Kulal card (whitepaper figures, competitor comparison) | the Vano 2018 card as it is live | schema default |
| `sections/main-product.liquid` highlights defaults | Used by +100 kPNI practitioners · Backed by 39 peer-reviewed studies | Chosen by kPNI practitioners & functional dentists · Formulated on peer-reviewed studies | schema default |

Not touched: `link_url` of every research card (study-links lane, R55).

## 3. Scanned, listed only (proposed fix, not changed)

Both templates and every `sections/*` default were read for disease words, fluoride superiority, detox, hormones, "prevents", "repairs", guarana or valerian effects and unsupported numbers. What remains, with a proposed fix; none of these were changed.

| # | Where | Text | Why it is listed | Proposed |
|---|---|---|---|---|
| R1 | Dr. Stephanie Spreuwers quote, `trusted_professionals_HAqYth/card_h8d3WL/hover_text`, both templates | "(with guarana for morning energy)" and "(with valerian, which contributes to calm and relaxation)" | Guarana energy and valerian calm effects in a testimonial (brand don't #16; testimonials do not bypass the cosmetic claims criteria, LR1) | **Question sent to Victor:** a) ask her to approve dropping the two parentheses; b) hide her hover text until she does; c) leave it. Recommendation a, b as the interim. |
| R2 | Chronobiology clock `morning_text`, both templates | "Cortisol rises; coffee, breakfast and the day's first acids follow…" | Hormone named with no primary source (CR1 C53, supported if reworded) | "Morning brings coffee, breakfast and the day's first acids. Enamel needs its shield on first." |
| R3 | Chronobiology clock `night_text`, both | "Melatonin rises and saliva slows to a trickle. What's on your enamel at 22:00 is still there at 07:00." | Second sentence has no source and the overnight biofilm changes (CR1 C52) | "Melatonin rises and saliva slows while you sleep." |
| R4 | Chronobiology clock `night_title`, both, and the section default | "Your mouth switches to repair" | "repair" is the body's own; not a product claim. Reviewed, kept. | Keep. |
| R5 | FAQ `faq_item_TNnqTQ/answer` and the `km-faq-accordion` default | "Night is repair … so Asleep soothes, rebalances and remineralises while you sleep." | Same duration claim as C12/C14 ("while you sleep"); Victor kept "With you all night" on the card, so this stays consistent with his choice. | If the card line ever changes: "…remineralises after the brush." |
| R6 | PDP `loop_subscriptions_WEk4XJ/pricing_summary_checkup_tooltip` and the `main-product` default | "Prevention, rewarded." | "Prevention" next to the formula reads as a prevention claim (CR1 C70 reasoning). Here it is the dental check-up that is rewarded, which is Victor's deliberate framing. | Keep, or "The visit, rewarded." |
| R7 | `stat_strip_karmicare/tagline`, index | "CHOSEN BY KPNI PRACTITIONERS, FUNCTIONAL DENTISTS, HEALTH PROFESSIONALS" | Endorsement; needs consent records, not a health claim (CR1 C80). | Keep once the consent file exists. |
| R8 | Hero `testimonial_badge/rating_text`, index | "4.8 (234)" | No review data behind it (CR1 C82; LR1 "unsupported review totals"). Reviews lane owns it. | Handoff to the reviews lane. |
| R9 | `stat_3/heading` "Clinically backed" and research `subheading` "CLINICALLY BACKED ORAL CARE", both | With the kept cards (an RCT on a nano-HAp gel, an observational meta-analysis) "clinically backed" is defensible as ingredient evidence; CR1 did not rule on it. | Keep; if a reviewer objects: "Peer-reviewed" / "THE RESEARCH". |
| R10 | Clock messages 1–7 (`locales/en.default.json`, `kc.clock.window_*`) | "least protected", "repair window", pH timings | CR1 C54: trim 1, 6, 7, hold 2–5. Locales are off-limits for this lane. | Handoff to source-copy. |
| R11 | `card_jN7XcL/text`, index | "All the minerals your mouth needs in one press." | Absolute, but a dosing line, not a health claim. | Keep. |
| R12 | `two_formulas_karmicare/right_heading`, index | "Purified and restored by night" | Brand framing (Awake activation, Asleep restoration); not detox. | Keep. |
| R13 | Disabled FAQ items `faq_item_7jmEGi` ("Fluoride and nano-hydroxyapatite compete…") and `faq_item_AL3DKF` ("Fluoride's benefits don't outweigh its known drawbacks") | Hidden already. | Keep hidden; re-enabling needs a review. |

## 4. Visual check of the two-card research section

Done on the live homepage in an anonymous isolated Orca profile (one page load), with the DOM patched to the branch state: three cards removed, Sietske's card removed at the time, footer texts replaced. The marquee (`assets/kc-marquee.js`) clones the set until the band covers the viewport twice, so two cards work the same as five: at 1440 the band shows sleep · sensitivity · sleep…, at 390 one card at a time. Day and Night both fine. Screens in `screens/` (`research-1440-day.jpg`, `research-1440-night.jpg`, `research-390-day.jpg`, `research-390-day-2.jpg` for the footer, `professionals-1440-day.jpg`).

Two notes. The screens were taken before Victor's keeps, so they show the longer heading "In a clinical trial, nano-hydroxyapatite helped reduce tooth sensitivity." (three lines at 380 px) and six practitioner cards; the live heading is shorter and the seventh card is back, which only makes the band longer. With two cards the pair repeats every ~1,600 px at 1440; if that reads as thin, `marquee: false` with `columns_desktop: "2"` shows both cards side by side, static.

## 5. Blog articles (Shopify sitemap, read 24 Oct)

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

## 6. Translations

`TRANSLATIONS-HANDOFF.md`: nine changed strings with template, block id, setting key, EN, NL and FR; three hidden blocks need none. Includes the warning that a registered translation of a changed key goes outdated in Shopify, so NL and FR register with the theme release.

## 7. Checks run

- `shopify theme check --fail-level error --output json`: exit 0, 0 errors, 19 warnings (the baseline). Run after the final theme state.
- Both templates parsed as JSON after the edits; disabled blocks listed and confirmed.
- Live reads, 24 Oct, one request each: homepage (browser), Duo page (HTML), sitemap index, articles sitemap, eight articles.
- No admin writes, no app installs, no CLI login, no `theme dev`, no form, cart or checkout.

## 8. Handoffs

| To | What |
|---|---|
| source-copy | Register the nine strings in `TRANSLATIONS-HANDOFF.md` in `en-source.json`, the batches and the NL/FR payloads; update the CLAIMS-REVIEW register (C33, C40, C41, C65, C66, C70, C81 applied; C12, C21, C34, C35, C52, C53, C60–C64, C68, C84, C85, C92 decided by Victor as "keep" on 24 Oct); the clock messages (R10). |
| reviews lane | "4.8 (234)" in the hero badge (R8). |
| study-links (R55) | Nothing changed in `link_url`; the three hidden cards keep their settings, so their links can still be filled. |
| gate-consent | The anonymous homepage load showed the Shopify cookie banner (Accept / Decline / Manage preferences) over the research section; no consent was given. For their record only. |
| Victor | `ADMIN-STEPS.md` steps a (low), j, k; the four unpublishes; the Spreuwers question; the v2-formula question on the RDA report. |

## 9. Input files

`docs/launch-gate/input/` is untracked in this worktree (placed by the coordinator); this lane did not commit it. The three outputs and the screens live in `docs/launch-gate/claims/`.
