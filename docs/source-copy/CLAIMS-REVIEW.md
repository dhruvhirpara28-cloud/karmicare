# Claims review · batches 01–03

Every health or cosmetic claim found in the homepage, Duo PDP, header and footer strings, isolated and not rewritten. Each claim is checked against `products.md` (Do say / Don't say) and `regulatory.md` (allowed: helps reduce, supports, contributes to, maintains, soothes, refreshes, strengthens; forbidden: cures, treats disease, prevents disease, guaranteed results, diagnoses, prescribes, medical-grade).

- `approved`: wording sits inside the Do-say list or the allowed verbs, at cosmetic scope, without numbers, timelines, comparisons or superlatives.
- `needs-review`: a number, timeline, comparison, study result, endorsement, safety statement or wording that goes beyond the Do-say list. Needs the Clinical Research sign-off before it ships.
- `unsupported`: on the Don't-say side, or no basis in `products.md` at all.

`regulatory.md` requires the Clinical Research sign-off for **all** health claims before publication, `approved` ones included; `approved` here means only that the wording is inside the rules. The `Where` column lists inventory ids; the same claim often appears on both templates.

| Status | Claims |
|---|---:|
| approved | 18 |
| needs-review | 42 |
| unsupported | 3 |

| Id | Topic | Claim (verbatim excerpt) | Status | Basis | Where |
|---|---|---|---|---|---|
| C01 | composition | “fluoride, SLS” | **approved** | products.md: fluoride-free & SLS-free (product overview). | `index:stat_strip_karmicare/stat_1/text` |
| C02 | composition | “FLUORIDE-FREE & SLS-FREE” | **approved** | products.md: fluoride-free & SLS-free. | `index:two_formulas_karmicare/ingredients_list` |
| C03 | composition | “Nano-hydroxyapatite, fluoride-free” | **approved** | products.md: nHAp; fluoride-free. Do say: 'fluoride-free alternative'. | `product.subscription-item:main/highlights_slider_9wAjAb/text_4` |
| C04 | dosing | “the full dose” | **approved** | products.md: 1 pump = 0.45 ml carries the full mineral dose (2026-08-04). | `index:stat_strip_karmicare/stat_2/text` |
| C05 | dosing | “All the minerals your mouth needs in one press” | **approved** | products.md: 'one pump (0.45 ml) contains all essential minerals'. | `index:product_benefits_karmicare_bcQ6tp/card_jN7XcL/text` |
| C06 | supply | “of AM/PM care per duo” | **approved** | faq/01-PRODUCT.md FAQ-0101 (Regulatory: Clean): ~64 days, never 71. | `index:stat_strip_karmicare/stat_4/text` |
| C07 | supply | “One duo lasts 64 days at two brushings a day” | **approved** | FAQ-0101 (Clean). Usage warning matches products.md 'do not combine with fluoride'. | `product.subscription-item:how_it_works_steps_aAgVmF/bottom_text` |
| C10 | leave-on | “works after the brush” | **approved** | products.md Do say: 'Leave-on technology for extended benefits'. | `index:stat_strip_karmicare/stat_5/text` |
| C11 | leave-on | “Leave-on, no rinse” | **approved** | products.md Do say: leave-on technology. | `product.subscription-item:main/highlights_slider_9wAjAb/text_3` |
| C12 | leave-on | “It works all night” | **needs-review** | Duration claim ('all night') goes beyond products.md 'extended benefits'; needs Clinical Research sign-off (regulatory.md). | `index:product_benefits_karmicare_bcQ6tp/card_AGFiEX/text` |
| C13 | leave-on | “Hours of active mineral care instead of seconds” | **needs-review** | Duration claim; homepage FAQ source (45 brief Q5) not yet through the Clinical Research pass (regulatory.md). | `index:km_faq_accordion_FYcArV/faq_item_qUxYCn/answer` |
| C14 | leave-on | “keep working — even while you sleep” | **needs-review** | Duration claim in the admin product description; regulatory.md sign-off. | `admin:karmicare-biorhythmic-oral-care-system:body_html` |
| C20 | enamel | “strengthen enamel” | **approved** | regulatory.md allows 'strengthens'; products.md Do say 'Remineralizes enamel naturally'. | `index:product_benefits_karmicare_bcQ6tp/text` |
| C21 | sensitivity | “Cold or hot, no hesitation” | **needs-review** | Absolute sensitivity outcome; products.md Do say is 'Reduces sensitivity'. Needs sign-off. | `index:product_benefits_karmicare_bcQ6tp/card_qMHDBq/text` |
| C22 | whitening | “Remineralisation lifts the surface. No bleach, no strips.” | **approved** | products.md: whitening only 'naturally through remineralization' — this ties brightness to remineralisation. | `index:product_benefits_karmicare_bcQ6tp/card_aXhzDi/text` |
| C23 | nHAp | “It remineralises teeth, reduces sensitivity, and whitens naturally” | **needs-review** | Do say covers remineralises / reduces sensitivity / natural whitening, but 'the most researched … in the world' is an unsourced superlative. Source 45 brief Q3; homepage-faq note: not yet through Clinical Research. | `index:km_faq_accordion_FYcArV/faq_item_AL3DKF/answer` |
| C24 | timeline | “most members feel the sensitivity shift in 2–4 weeks” | **needs-review** | Member-outcome timeline (45 brief Q10, adapted in Figma 3002:20280); homepage-faq note flags it for the Clinical Research pass. | `index:km_faq_accordion_FYcArV/faq_item_4KMG6C/answer` |
| C25 | Awake USP | “so Awake protects, activates and brightens” | **approved** | products.md: USP lines 'Protects. Activates. Brightens.' / 'Detoxifies. Soothes. Regenerates.' | `index:km_faq_accordion_FYcArV/faq_item_TNnqTQ/answer` |
| C26 | shield | “a mineral shield for everything ahead” | **approved** | products.md: 'extra protective layer of nano-hydroxyapatite … like a natural shield'. | `index:two_formulas_karmicare/left_text` |
| C27 | shield | “Enamel needs its shield on first” | **approved** | products.md: protective nHAp layer for the day. | `index:chronobiology_clock_karmicare/morning_text`, `product.subscription-item:chronobiology_clock_karmicare/morning_text` |
| C30 | microbiome | “MICROBIOME-CONSCIOUS” | **approved** | products.md Do say: 'Supports oral microbiome balance'. | `index:two_formulas_karmicare/ingredients_list` |
| C31 | microbiome | “Supports your mouth’s own balance. Less plaque” | **approved** | products.md: xylitol supports microbiome balance and 'actively reduces plaque'; regulatory.md 'supports'. | `index:product_benefits_karmicare_bcQ6tp/card_QdCWaE/text` |
| C32 | microbiome | “keep your mouth in balance” | **approved** | products.md Do say: 'Supports oral microbiome balance'. | `index:product_benefits_karmicare_bcQ6tp/text` |
| C33 | biofilm | “BIOFILM PREVENTION” | **needs-review** | 'Prevention' without 'helps' reads as a prevention claim; regulatory.md forbids 'prevents disease' and the Belgian JEP/DETIC code bans 'voorkomt'. Allowed verb would be 'helps reduce'. | `index:two_formulas_karmicare/ingredients_list` |
| C34 | gums | “settle gums” | **needs-review** | Gum benefit is not in products.md benefits (only the indication 'care of teeth, gums and microbiome'). Needs sign-off. | `index:product_benefits_karmicare_bcQ6tp/text` |
| C35 | gums | “Gums settle, turn pinker and look radiant” | **unsupported** | No source in products.md; the SLS evidence (Alli 2019) concerns canker sores, not gum colour. | `index:product_benefits_karmicare_bcQ6tp/card_VP8KGi/text` |
| C36 | gums | “for stronger teeth, calmer gums and fresher breath” | **needs-review** | 'calmer gums' not in products.md benefits (admin product description). | `admin:karmicare-biorhythmic-oral-care-system:body_html` |
| C37 | microbiome | “Xylitol, balances the oral microbiome” | **needs-review** | 'balances' is stronger than products.md Do say 'Supports oral microbiome balance' (admin metafield). | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#14` |
| C40 | nootropic | “Guarana for a bright start, valerian for an evening” | **needs-review** | Focus/calm effects of a cosmetic go beyond oral-care function; products.md Do say only 'Nootropic extracts aligned with your body’s rhythms'. | `index:product_benefits_karmicare_bcQ6tp/card_KRCrBY/text` |
| C41 | nootropic | “Focus by day” | **needs-review** | Same as C40 (card heading). | `index:product_benefits_karmicare_bcQ6tp/card_KRCrBY/heading` |
| C42 | systemic | “Oral-gut-brain, deeper than enamel” | **needs-review** | Systemic effect of a cosmetic (admin comparison metafield). | `admin:karmicare-biorhythmic-oral-care-system:custom.comparison_section#21` |
| C43 | systemic | “What settles in the mouth is swallowed all night” | **needs-review** | Oral–gut–brain mechanism statement (admin product FAQ metafield). | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#106` |
| C44 | systemic | “Formulated without fluoride and without known endocrine-active ingredients” | **needs-review** | 'Free from' claim on endocrine-active ingredients needs substantiation (admin product FAQ metafield). | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#102` |
| C45 | systemic | “You feel it straight away” | **needs-review** | Immediate-effect claim (admin comparison metafield). | `admin:karmicare-biorhythmic-oral-care-system:custom.comparison_section#15` |
| C46 | rhythm | “supporting the natural recovery process” | **approved** | regulatory.md 'supports'. | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#104` |
| C50 | physiology | “Neisseria peaks” | **needs-review** | Study-derived timestamp (Chellappa 2022); 45 brief launch gate 4: Clinical Research sign-off on the science sections. | `index:chronobiology_clock_karmicare/morning_badge`, `product.subscription-item:chronobiology_clock_karmicare/morning_badge` |
| C51 | physiology | “Fusobacterium peaks” | **needs-review** | As C50. | `index:chronobiology_clock_karmicare/night_badge`, `product.subscription-item:chronobiology_clock_karmicare/night_badge` |
| C52 | physiology | “Melatonin rises and saliva slows to a trickle” | **needs-review** | Physiology statement; gate 4 sign-off. | `index:chronobiology_clock_karmicare/night_text`, `product.subscription-item:chronobiology_clock_karmicare/night_text` |
| C53 | physiology | “Cortisol rises; coffee, breakfast” | **needs-review** | Physiology statement; gate 4 sign-off. | `index:chronobiology_clock_karmicare/morning_text`, `product.subscription-item:chronobiology_clock_karmicare/morning_text` |
| C54 | physiology | “saliva is only now picking up after the night” | **needs-review** | Seven hourly clock messages (assets/chronobiology-clock-karmicare.js); physiology statements, gate 4 sign-off. | `liquid:assets/chronobiology-clock-karmicare.js:11` |
| C60 | study | “Nano-HAp sealed 98% of open dentine tubules.” | **needs-review** | In-vitro result (Kulal 2016, ~1% nHAp) shown as a headline; gate 4 sign-off. regulatory.md: never overstate findings. | `index:research_behind_system_EkjATL/card_bDxUVT/heading`, `product.subscription-item:research_behind_system_EkjATL/card_bDxUVT/heading` |
| C61 | study | “Poorer oral health was linked with poorer sleep.” | **needs-review** | Observational meta-analysis (Lei & Hu 2025); gate 4. | `index:research_behind_system_EkjATL/card_yMiD9D/heading`, `product.subscription-item:research_behind_system_EkjATL/card_yMiD9D/heading` |
| C62 | study | “Xylitol lowered tooth decay compared with controls.” | **needs-review** | Disease endpoint (caries) next to a cosmetic; FAQ-0203 note: do not claim superiority. Gate 4. | `index:research_behind_system_EkjATL/card_fmFMFd/heading`, `product.subscription-item:research_behind_system_EkjATL/card_fmFMFd/heading` |
| C63 | study | “Nano-HAp beat fluoride on tooth sensitivity.” | **needs-review** | Comparative claim (Vano 2018); the same claim keeps FAQ-0202 at 'Needs review'. | `index:research_behind_system_EkjATL/card_Hi7YUD/heading`, `product.subscription-item:research_behind_system_EkjATL/card_Hi7YUD/heading` |
| C64 | study | “No SLS meant fewer and shorter canker sores.” | **needs-review** | Disease endpoint (aphthous ulcers); the Farmaline review dropped condition outcomes as claims under EU 655/2013 (dutch-offer doc). | `index:research_behind_system_EkjATL/card_JeERX6/heading`, `product.subscription-item:research_behind_system_EkjATL/card_JeERX6/heading` |
| C65 | evidence count | “Formulated on +36 studies” | **needs-review** | Study count differs across the site: '+36' here, '36 peer-reviewed studies' on the PDP, '39 peer-reviewed studies' in the 45 brief, '15 peer-reviewed studies' under the 45 brief Cascade. | `index:stat_strip_karmicare/stat_3/text` |
| C66 | evidence count | “Clinically proven ingredients · 36 peer-reviewed studies” | **needs-review** | 'Clinically proven' is reserved for validated claims (regulatory.md); study count conflicts (see C65). | `product.subscription-item:main/highlights_slider_9wAjAb/text_2` |
| C67 | evidence count | “Formulated on 36 peer-reviewed studies” | **needs-review** | Study count conflict (see C65); admin metafield. | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#72` |
| C70 | prevention | “The best outcome is the one prevented.” | **needs-review** | Prevention framing beside product recommendation; memory rule (13-14 Oct): prevention belongs to the person, value through the Check-up Reward. Also '1,200 brushings a year' conflicts with twice a day (730). | `index:trusted_professionals_HAqYth/bottom_text`, `product.subscription-item:trusted_professionals_HAqYth/bottom_text` |
| C80 | endorsement | “CHOSEN BY KPNI THERAPISTS, FUNCTIONAL DENTISTS, HEALTH ENTHUSIASTS” | **needs-review** | Endorsement; 45 brief launch gate 3 (practitioner consent and current titles). | `index:stat_strip_karmicare/tagline` |
| C81 | endorsement | “Used by 100+ kPNI practitioners & functional dentists” | **needs-review** | Number unsourced; the 45 brief says '30+ practitioners in BE & NL'. | `product.subscription-item:main/highlights_slider_9wAjAb/text_1` |
| C82 | rating | “4.8 (234)” | **needs-review** | Rating and count have no visible source (the Judge.me block is disabled on the PDP). | `index:hero_karmicare_XKKLDK/testimonial_badge_h8d3WL/rating_text` |
| C83 | testimonial | “hydroxyapatite as a scientifically supported choice” | **needs-review** | Leen Ponet's English quote is a draft translation, not author-approved (Figma library notes). | `index:trusted_professionals_HAqYth/card_8dRing/hover_text`, `product.subscription-item:trusted_professionals_HAqYth/card_8dRing/hover_text` |
| C84 | testimonial | “supportive of detox pathways and nervous system regulation” | **unsupported** | Testimonial attributes hormonal, nervous-system and detox effects to a cosmetic; no source in products.md; regulatory.md forbids medical claims. | `index:trusted_professionals_HAqYth/card_CtQgU9/hover_text`, `product.subscription-item:trusted_professionals_HAqYth/card_CtQgU9/hover_text` |
| C85 | testimonial | “support rather than burden the nervous system and hormonal balance” | **unsupported** | As C84 (same quote). | `index:trusted_professionals_HAqYth/card_CtQgU9/hover_text`, `product.subscription-item:trusted_professionals_HAqYth/card_CtQgU9/hover_text` |
| C90 | safety | “Safe for children. Safe when swallowed.” | **needs-review** | FAQ-0206: 'from age 3 under supervision', must match the leaflet; admin product FAQ metafield. | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#43` |
| C91 | safety | “Safe to swallow” | **needs-review** | As C90 (admin metafield chip). | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#96` |
| C92 | safety | “Midwest University · RDA 93 Awake, 72 Asleep” | **needs-review** | Lab name conflicts with the 45 brief ('Indiana University OHRI 2025'); values match (93.25 / 72.32). | `admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#69` |
| C95 | timeline | “— sensitivity starts to fade, the mineral layer builds” | **needs-review** | Week-by-week outcome timeline (treatment journey metafields), framed as member-reported; Clinical Research sign-off. | `admin:karmicare-biorhythmic-oral-care-system:custom.treatment_journey_*#09` |
| C96 | timeline | “— less plaque, mouth bacteria back in balance (oral microbiome)” | **needs-review** | As C95. | `admin:karmicare-biorhythmic-oral-care-system:custom.treatment_journey_*#13` |
| C97 | timeline | “— weak spots remineralised, enamel stronger” | **needs-review** | As C95. | `admin:karmicare-biorhythmic-oral-care-system:custom.treatment_journey_*#15` |
| C98 | timeline | “— feel the repair, it keeps working while you sleep” | **needs-review** | As C95. | `admin:karmicare-biorhythmic-oral-care-system:custom.treatment_journey_*#07` |
| C99 | environment | “are recyclable” | **needs-review** | Environmental claim in the footer; needs substantiation (EU green-claims rules). | `footer-group:footer/copyright_text` |

## Offer statements that conflict with the offer source of truth

Not health claims, but customer-facing promises that the confirmed offer (5 Oct 2026) contradicts. Listed so translators do not lock them in.

| Where | Text | Conflict |
|---|---|---|
| `header-group:announcement-bar/announcement-bar-0/text` | COMPLIMENTARY SHIPPING · 60-DAY MONEY-BACK GUARANTEE · BELGIAN-MADE | Memberships ship free and carry the 60-day guarantee; Try Once pays shipping and has a 14-day guarantee. |
| `product.subscription-item:main/loop_subscriptions_WEk4XJ/pricing_summary_checkup_tooltip`, sticky bar `checkup_info`, compare-table tooltip, Year selling-plan description | “…verified by your dentist” | Proof is an appointment confirmation or invoice plus the questionnaire; no dentist involvement is required. |
| `product.subscription-item:main/info_card_FnBcaN/body_text` | “…completing your dental check-up — confirmed by your dentist — adds €40…” | As above. |
| Selling-plan descriptions (Loop, admin) | “Inflation-proof member price” | The approved wording is the price-protection line (NL: “Je ledenprijs blijft gelijk zolang je lid blijft, ook als onze prijzen stijgen.”); no EN equivalent is approved yet. |
| Compare table, Year column (admin) | €0.42 cost per brushing | Same €59 per duo as the 60-Day Rhythm, so €0.49. |
| Compare table, Welcome Kit row (admin) | · €18 Value · | €21 at shop prices (2.0 brushes €6 + €6, floss €9). |
