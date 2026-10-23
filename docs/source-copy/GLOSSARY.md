# Glossary · EN → NL → FR (homepage, Duo PDP, header and footer)

For the translators of batches 01–03 (`INVENTORY.md`). One row per term that recurs in those strings.

**Sources for NL**: *Figma NL* = the approved NL translation of Dutch offer 2.0 (Figma `3738:27474`, 2 Oct 2026, `dutch-offer-2-nl-translation-figma.md`); *products.md* = the NL product texts; *FAQ* = the NL website answers in the FAQ knowledge base; *offer* = the offer source of truth. Where none of them has the term, the NL is marked **proposed**.

**FR**: no approved FR copy exists. Every FR entry is **proposed**, and the FR conventions below are a working convention, not a decision.

## Conventions

| | EN | NL | FR (proposed) |
|---|---|---|---|
| Register | you | *je / jouw*; neutral Dutch that reads naturally in Flanders and the Netherlands (Figma NL) | warm *vous* (working convention) |
| Price per brushing | €0.49 | €0,49 | 0,49 € |
| Decimals and thousands | €1,200 · 36,559 · SMD 2.17 · p = 0.004 | €1.200 · 36.559 · SMD 2,17 · p = 0,004 (Figma NL) | 1 200 € · 36 559 · SMD 2,17 · p = 0,004 (narrow no-break space U+202F as thousands separator) |
| Confidence interval | 95% CI | 95%-BI (Figma NL) | IC à 95 % |
| Percent | 20% | 20% | 20 % (no-break space) |
| Punctuation | — | as EN | no-break space (U+00A0) before `:` `;` `!` `?` and before `€` and `%` |
| Encoding | — | — | the FR examples in this file contain the real characters (U+00A0, U+202F): copy them as they are. FR typography stays pending Victor |
| Times | 06:40 · 22:00 | 06:40 · 22:00 | 06:40 · 22:00 (design element; keep the digits) |
| Billing year | one full year | *volledig jaar*, never *volledig kalenderjaar* (offer, 2 Oct) | une année complète |
| Plan interval | every 60 days (never eight weeks or two months) | om de 60 dagen | tous les 60 jours |
| Capitals in names | Title Case in plan names | only the first word, brand + noun with a hyphen: *Het Karmicare-jaar* (Figma NL, decision 2 Oct) | only the first word: *L'année Karmicare* |

**Open for Victor**: EN renders €0.49 and NL €0,49 (COMMON-RULES §3), while French typography puts the euro sign after the amount: 0,49 €. Confirm that FR follows the French convention and is not a copy of the NL €0,49. A related point for the store: the money format renders computed amounts with a comma in EN too (buy box "€0,49 per brushing", "€5,90"), so static EN text (€0.49) and computed amounts (€0,49) disagree on the same page. That is a store/Loop money-format setting, not template text (handoff in REPORT.md).

## Do not translate

| Kind | Values |
|---|---|
| Brand and program names | KARMICARE, Karmicare, KARMICA BV, **Awake**, **Asleep**, **Care Credit**, **Return on Care** (™), **Leave-on** (NL keeps it; FR proposed to keep it as *leave-on*, as `products.md` FR does), *KARMICARE™ Biorhythmic Toothpaste Kit* (legal product name, Figma NL keeps it) |
| Science and references | nHAp, kPNI, INCI lists (never translated, the same on every EU market), study citations (authors · year · journal), CPNP, CPSR, SCCS/1677/25, ISO 11609, RDA values, Ph. Eur. |
| People | Practitioners' names (Dr. Stephanie Spreuwers, Mariama Banjai, Leen Ponet, Dr. Iveta Pleša Rutule, Dr. Kris Sienaert, Sietske Hamelink, Kim Verlot), Victor |
| Integration keys | Selling-plan IDs (712106115453, 712155431293, …) and the text before `:` in `custom_button_text_by_plan`; `handle_item` values (`once`); product handles (`karmicare-biorhythmic-oral-care-system`, `morning-toothbrush-2-0`, `evening-toothbrush-2-0`, `whitening-charcoal-dental-floss`); the Subscription Name values **"60-Day Supply"** and **"Year Supply"** (`snippets/kc-plan-loyalty.liquid:41/43`, read by Loop's Care Credit rules); the discount code **"Welcome Kit"** (`snippets/welcome-kit.liquid:34`) |
| Tokens and markup | `[value]`, `[price]`, `[credit]`, `[per_brushing]`, `{{ … }}`, HTML tags, the `kc-dynamic_price` spans in the selling-plan descriptions |
| Placeholders | `[NEEDS APPROVED COPY]`: wait for the approved EN |

The selling-plan group named "60-Day Supply" carries the same text as a Subscription Name key; leave that group name untranslated until someone confirms the two are separate.

## Offer and plans

| EN | NL | NL source | FR (proposed) | Notes |
|---|---|---|---|---|
| 60-Day Rhythm (plan, buy box) | 60-dagenritme | Figma NL | Rythme 60 jours | |
| 60-Day Supply (compare-table label) | 60-dagenvoorraad | Figma NL | Réserve 60 jours | the visible label only; the Subscription Name key stays "60-Day Supply" |
| The Karmicare Year / the Year | Het Karmicare-jaar / het jaar | Figma NL | L'année Karmicare / l'année | not *Het Karmicare Jaar* (the NL FAQ-0402 answer still has that spelling) |
| 3 now, 3 in month 6 (Year sub-line) | 3 nu, 3 in maand 6 | **proposed** | 3 maintenant, 3 au 6e mois | approved EN sub-line (COMMON-RULES §3) |
| Try Once | Eenmalig proberen | Figma NL | Essayer une fois | "one-time order" in account pages and emails (offer) |
| one-time | eenmalig | Figma NL | unique | |
| membership / member | lidmaatschap / lid | offer | adhésion / membre | |
| member price | ledenprijs | offer | prix membre | approved NL: "Je ledenprijs blijft gelijk zolang je lid blijft, ook als onze prijzen stijgen." |
| duo (Awake + Asleep) | duo | FAQ | duo | |
| Welcome Kit | welkomstpakket | Figma NL | kit de bienvenue | value €21 / €21 / 21 € |
| Welcome Kit · with first order | Welkomstpakket · bij je eerste bestelling | **proposed** | Kit de bienvenue · avec votre première commande | |
| Morning Toothbrush / Evening Toothbrush | Ultrazachte ochtendborstel / Dieptereinigende avondborstel (buy box, shortened) | Figma NL | brosse à dents du matin / du soir | product titles are admin-held |
| Care Credit | Care Credit | Figma NL | Care Credit | always in €; never "discount", "cashback", "points" |
| Return on Care | Return on Care | Figma NL | Return on Care | program name |
| Check-up Reward / Dental Check-up Reward | controlebeloning | Figma NL | récompense contrôle dentaire | €40, paid as Care Credit |
| check-up (dental) | controle (bij de tandarts) | FAQ / Figma NL | contrôle dentaire | |
| money-back guarantee | geld-terug-garantie | FAQ | garantie satisfait ou remboursé | 60 days on memberships, 14 days on Try Once |
| 60-day money-back guarantee (trust row) | 60 dagen geld terug | Figma NL (shortened) | Satisfait ou remboursé 60 jours | |
| Gift, pause or cancel | Pauzeren of opzeggen (trust row, shortened) | Figma NL | Offrir, suspendre ou résilier | the NL short form drops "gift" to fit |
| Free shipping / Complimentary shipping | Gratis verzending | Figma NL | Livraison offerte | |
| Most Picked (badge) | ★ Meest gekozen | Figma NL | ★ Le plus choisi | |
| Brushing & Beyond (badge) | Meer dan poetsen | Figma NL | Au-delà du brossage | |
| — (comparison message, approved in NL only) | Dezelfde prijs per duo. Kies je betaalritme en je extra voordelen. | offer (approved NL) | Le même prix par duo. Choisissez votre rythme de paiement et vos avantages. | no EN version is approved; not on these pages yet |
| Begin / Start (CTA) | Begin / Start | **proposed** | Commencer | never "buy" |
| Total today | Totaal vandaag | **proposed** | Total aujourd'hui | |
| renews | wordt verlengd | **proposed** | se renouvelle | |
| delivery / shipment | levering / zending | FAQ | livraison / envoi | |

## Ritual and use

| EN | NL | NL source | FR (proposed) | Notes |
|---|---|---|---|---|
| brushing (per brushing) | poetsbeurt (per poetsbeurt) | Figma NL | brossage (par brossage) | |
| ritual | ritueel | FAQ | rituel | |
| formula | formule | FAQ | formule | |
| system | systeem | products.md | système | |
| oral care | mondzorg / mondverzorging | Figma NL | soin bucco-dentaire | |
| biorhythmic | bioritmisch | products.md | biorythmique | |
| morning / evening | ochtend / avond | products.md | matin / soir | always Awake (morning) before Asleep (evening) |
| by day / by night | overdag / 's nachts | products.md | le jour / la nuit | |
| one pump | één pompje (0,45 ml) | products.md | une pression (0,45 ml) | |
| Rinse first | Eerst spoelen | Victor 23 Oct | Rincez-vous la bouche | |
| Spit, don't rinse | Spugen, niet spoelen | Figma NL (how-to step 3) | Crachez, ne rincez pas | |
| leave-on | leave-on | Figma NL | leave-on | |
| toothpaste (first mention only) | tandpasta | products.md | dentifrice | category word once, then formula / system / care / ritual |
| Strengthen your teeth. Strengthen yourself. | Versterk je tanden. Versterk jezelf. | brief | Renforcez vos dents. Renforcez-vous. | brand promise |
| The Karmicare effect | Het Karmicare-effect | Figma NL | L'effet Karmicare | |
| Week 1 / Day 60 | Week 1 / Dag 60 | Figma NL | Semaine 1 / Jour 60 | |
| Calmer check-ups — arrive resilient, you did the work at home | Rustigere controles — je staat er sterk voor, je deed het werk al thuis | Victor 23 Oct (full form) | Des contrôles plus sereins — vous avez fait le travail à la maison | |
| Evenings that wind down — no sting, nothing to rinse | Rustige avonden — niets dat prikt, niets na te spoelen | Figma NL (shortened) | Des soirées apaisées — rien qui pique, rien à rincer | |

## Ingredients and science

| EN | NL | NL source | FR (proposed) |
|---|---|---|---|
| nano-hydroxyapatite (nHAp) | nano-hydroxyapatiet (nHAp) | products.md | nano-hydroxyapatite (nHAp) |
| Nano-HAp sealed 98% of open dentine tubules. | Nano-HAp dichtte 98% van de open dentinekanaaltjes. | Figma NL (research card 1) | La nano-HAp a obturé 98 % des tubules dentinaires ouverts. |
| dentine tubules | dentinekanaaltjes | Figma NL | tubules dentinaires |
| enamel | (tand)glazuur | products.md | émail |
| remineralise / remineralisation | remineraliseren / remineralisatie | products.md | reminéraliser / reminéralisation |
| sensitivity | gevoeligheid | products.md | sensibilité |
| gums | tandvlees | products.md | gencives |
| plaque | tandplak | products.md | plaque dentaire |
| oral microbiome | mondmicrobioom | products.md | microbiome buccal |
| xylitol | xylitol | products.md | xylitol |
| guarana | guarana | products.md | guarana |
| valerian (root) | valeriaan(wortel) | products.md | (racine de) valériane |
| activated charcoal | actieve kool / geactiveerde houtskool | products.md | charbon actif |
| bentonite clay | bentonietklei | products.md | argile bentonite |
| glycolipids | glycolipiden | FAQ-0208 | glycolipides |
| fluoride-free | fluoridevrij / zonder fluoride | products.md | sans fluor |
| SLS-free | SLS-vrij / zonder SLS | products.md | sans SLS |
| supplements · skincare (comparison headers) | Supplementen · Huidverzorging | Figma NL (shortened) | Compléments · Soins de la peau |
| canker sores | aften | dutch-offer doc | aphtes |
| circadian / 24-hour clock | circadiaan / 24-uursklok | **proposed** | circadien / horloge de 24 heures |

## Claim verbs (EU cosmetic wording)

Translate claims with the allowed verbs only (`regulatory.md`); never *cures / treats / prevents*.

| EN | NL | FR (proposed) |
|---|---|---|
| helps reduce | helpt verminderen | aide à réduire |
| supports | ondersteunt | soutient |
| contributes to | draagt bij aan | contribue à |
| maintains | behoudt / houdt in stand | maintient |
| soothes | kalmeert | apaise |
| refreshes | verfrist | rafraîchit |
| strengthens | versterkt | renforce |

Never in NL: *voorkomt* (the Belgian JEP/DETIC code bans it), *geneest*, *behandelt*. Never in FR: *prévient*, *guérit*, *traite*.

## Known conflicts in the sources

- The NL website answers for FAQ-0301 and FAQ-0302 use *u/uw*; the convention is *je/jouw*.
- The NL answer for FAQ-0402 writes *Het Karmicare Jaar*; the decision is *Het Karmicare-jaar*.
- The NL product texts in `products.md` say *de eerste tandpastaset* and *geen gewone tandpasta*; the 2026 rules forbid "the first" claims and negating the category. Do not reuse those lines.
