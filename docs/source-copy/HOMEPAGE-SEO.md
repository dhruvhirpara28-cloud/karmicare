# Homepage SEO · title and meta description for www.karmicare.com

**Created**: 2026-10-25

### Changelog
| Date | Change |
|------|--------|
| 2026-10-25 | First version: recommended EN pair and two alternatives, NL for /nl and FR for /fr in the same layout, checks against claims, offer and tone. Request from Victor via the landing desk ("have a SEO ready homepage title and meta description"). |

Lane `karmicare/soft-launch-source-copy`. Not published. If Victor approves the EN, he enters it himself in Online Store → Preferences (title and meta description only; the social sharing image stays as he saved it). NL and FR then go through the next registration round of this lane (`admin:shop:online_store.preferences.homepage_title` and `…homepage_meta_description`).

## What is live now

| Field | Live EN (25 Oct) | Problem |
|---|---|---|
| Title | KARMICARE - Biorhythmic Oral Care | Brand only. "Biorhythmic" has no search demand and reads as a claim. Nobody searches for "biorhythmic oral care". |
| Meta description | Karmicare designs biorhythmic toothpastes formulated with clean ingredients, nootropics and plant extracts to elevate your morning and night. Nano Hydroxyapatite, fluoride free toothpaste. | "nootropics … to elevate your morning and night" is a nootropic-benefit claim (memo CL24, KD05); "clean ingredients" is vague. It also says "toothpaste" twice. |

## Search intent

The homepage gets the brand searches ("karmicare") and the broad category search: **fluoride-free toothpaste**, with morning and evening as the difference. The narrower term *fluoride-free nano-hydroxyapatite toothpaste* belongs to the product page, whose SEO title already leads with it ("Fluoride-Free Nano-Hydroxyapatite Toothpaste | Awake & Asleep", 22 Oct). The homepage therefore leads with the brand and the broad term, so the two pages do not compete for the same query. Shopify adds no shop-name suffix to the homepage title, so the brand has to be in the field itself.

## Claims, offer and tone: what every variant keeps to

- Only these safe wordings from `karmicare/science-imagery:docs/evidence-strategy/DECISION-MEMO.md` §5:
  - "formulated without fluoride or SLS" (CL43, supported);
  - "formulated with nano-hydroxyapatite" (CL19);
  - "Awake for the morning. Asleep for the evening." (CL24);
  - "Two different formulas, designed for morning and evening care" (CL42);
  - "Awake with guarana. Asleep with valerian." (KD05, ingredient only).
- Not used: any effect on sleep, focus, energy, calm or the body, any nootropic benefit, any disease or medical effect, any "only"/"best" superlative. Guarana and valerian are named only as ingredients.
- Offer: no price, no "discount", "cashback" or "save". The Duo price (€59) and Care Credit are not in the snippet: a price in a meta description goes stale, and Google already shows the price from the product data.
- Tone: "toothpaste" appears once, in the title, as the search term. The description says "formulas". Awake comes before Asleep. There are no colons in the descriptions.

## EN

**Recommended**

| Field | Text | Characters |
|---|---|---:|
| Title | Karmicare \| Fluoride-Free Toothpaste for Morning & Evening | 58 |
| Meta description | Awake for the morning, Asleep for the evening. Two formulas with nano-hydroxyapatite, made without fluoride or SLS, for your daily care ritual. | 143 |

Intent: brand plus "fluoride-free toothpaste", with the morning/evening difference visible in the result.

**Alternative A: keyword first** (only if the product page gets another SEO title; otherwise the two pages compete)

| Field | Text | Characters |
|---|---|---:|
| Title | Fluoride-Free Nano-Hydroxyapatite Toothpaste \| Karmicare | 56 |
| Meta description | Two formulas designed for morning and evening care. Awake with guarana, Asleep with valerian, both with nano-hydroxyapatite and without fluoride or SLS. | 152 |

**Alternative B: product names first**

| Field | Text | Characters |
|---|---|---:|
| Title | Karmicare \| Awake & Asleep Morning and Evening Toothpaste | 57 |
| Meta description | Morning and evening care in one daily ritual. Awake and Asleep are formulated with nano-hydroxyapatite and without fluoride or SLS. | 131 |

## NL (/nl)

Je-vorm. Glossary terms: *fluoridevrij*, *nano-hydroxyapatiet*, *ochtend / avond*, *ritueel*.

**Recommended**

| Field | Text | Characters |
|---|---|---:|
| Title | Karmicare \| Fluoridevrije tandpasta voor ochtend en avond | 57 |
| Meta description | Awake voor de ochtend, Asleep voor de avond. Twee formules met nano-hydroxyapatiet, zonder fluoride en zonder SLS, voor je dagelijkse ritueel. | 142 |

Intent: "fluoridevrije tandpasta", the term used in Dutch-language searches.

**Alternative A**

| Field | Text | Characters |
|---|---|---:|
| Title | Fluoridevrije nano-hydroxyapatiet tandpasta \| Karmicare | 55 |
| Meta description | Twee formules voor ochtend- en avondzorg. Awake met guarana, Asleep met valeriaan, allebei met nano-hydroxyapatiet en zonder fluoride of SLS. | 141 |

**Alternative B**

| Field | Text | Characters |
|---|---|---:|
| Title | Karmicare \| Awake & Asleep tandpasta voor ochtend en avond | 58 |
| Meta description | Ochtend- en avondzorg in één dagelijks ritueel. Awake en Asleep bevatten nano-hydroxyapatiet en geen fluoride of SLS. | 117 |

## FR (/fr)

Vous. Glossary terms: *sans fluor*, *nano-hydroxyapatite*, *matin / soir*, *rituel*. No colon, so no non-breaking space is needed.

**Recommended**

| Field | Text | Characters |
|---|---|---:|
| Title | Karmicare \| Dentifrice sans fluor pour le matin et le soir | 58 |
| Meta description | Awake pour le matin, Asleep pour le soir. Deux formules à la nano-hydroxyapatite, sans fluor ni SLS, pour votre rituel de soin quotidien. | 137 |

Intent: "dentifrice sans fluor".

**Alternative A**

| Field | Text | Characters |
|---|---|---:|
| Title | Dentifrice sans fluor à la nano-hydroxyapatite \| Karmicare | 58 |
| Meta description | Deux formules pensées pour le soin du matin et du soir. Awake au guarana, Asleep à la valériane, à la nano-hydroxyapatite et sans fluor ni SLS. | 143 |

**Alternative B**

| Field | Text | Characters |
|---|---|---:|
| Title | Karmicare \| Awake & Asleep, dentifrices du matin et du soir | 59 |
| Meta description | Le soin du matin et du soir en un rituel quotidien. Awake et Asleep sont formulés à la nano-hydroxyapatite, sans fluor ni SLS. | 126 |

## After Victor's choice

1. Victor enters the EN title and description in Online Store → Preferences. The social sharing image is not touched.
2. Source-copy reads the live EN back (curl on www.karmicare.com) and updates the EN source rows. NL and FR of the same variant go into the next registration round, with a dry run first.
3. If he picks alternative A, the product page's SEO title has to change first, so the two pages do not compete. That change is a separate decision.

Counts are Unicode characters, measured with Python `len()`. Google truncates by pixel width, so on mobile even a 58-character title can be cut short a little earlier.
