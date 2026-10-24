# Claims cleanup · translations handoff (R59, 24 Oct 2026)

For source-copy. Every EN string that R59 changed, with the NL and FR to register. All changes are in `templates/index.json`; `templates/product.subscription-item.json` is unchanged (Victor, 24 Oct: the product page was already approved). No block is hidden. Section schema defaults changed in R59 are not translatable settings and are listed for completeness only.

Victor's keeps of 24 Oct are applied: the five research cards, the research intro, the "Cold or hot" card, the "settle gums" line, Sietske Hamelink's card and the whole product page are unchanged, so they are not in this list.

Conventions used: NL je-form, "peer-reviewed" stays English in NL (as in batch-02), FR uses vous; Awake, Asleep, Leave-on, Care Credit and Return on Care stay English. FR thin spaces before `:` are written as plain spaces here; apply the FR spacing convention when registering (the Write tool drops no-break spaces).

Note for registration: a registered NL or FR translation of a key whose EN changed becomes outdated in Shopify and stops being served, so register the new NL and FR together with the theme release. The existing "translated" NL and FR entries for `stat_3/text` and `ingredients_list` were translations of the old EN and must not be registered as they stand.

## 1. Changed strings · `templates/index.json`

| # | Section · block · key | EN (new) | NL | FR |
|---|---|---|---|---|
| 1 | `stat_strip_karmicare` · `stat_3` · `text` | Formulated on peer-reviewed studies | Geformuleerd op basis van peer-reviewed studies | Formulé sur la base d’études à comité de lecture |
| 2 | `two_formulas_karmicare` · (section) · `ingredients_list` | `<ul><li>FLUORIDE-FREE & SLS-FREE</li><li>MICROBIOME-CONSCIOUS</li><li>NANO-HYDROXYAPATITE (NHAP)</li><li>SYNERGETIC EFFECT</li><li>VELVETY FOAM</li><li>GLYCOLIPID CLEANSING</li><li>HELPS REDUCE BIOFILM</li><li>BELGIAN FORMULATION</li><li>VEGAN & HALAL</li></ul>` (only the seventh pill changed: BIOFILM PREVENTION → HELPS REDUCE BIOFILM) | `<ul><li>FLUORIDEVRIJ & SLS-VRIJ</li><li>MICROBIOOMBEWUST</li><li>NANO-HYDROXYAPATIET (NHAP)</li><li>SYNERGETISCH EFFECT</li><li>FLUWEELZACHT SCHUIM</li><li>REINIGING MET GLYCOLIPIDEN</li><li>HELPT BIOFILM VERMINDEREN</li><li>BELGISCHE FORMULERING</li><li>VEGAN & HALAL</li></ul>` | `<ul><li>SANS FLUOR & SANS SLS</li><li>RESPECTUEUX DU MICROBIOME</li><li>NANO-HYDROXYAPATITE (NHAP)</li><li>EFFET SYNERGIQUE</li><li>MOUSSE VELOUTÉE</li><li>NETTOYAGE AUX GLYCOLIPIDES</li><li>AIDE À RÉDUIRE LE BIOFILM</li><li>FORMULATION BELGE</li><li>VEGAN & HALAL</li></ul>` |
| 3 | `product_benefits_karmicare_bcQ6tp` · `card_VP8KGi` · `text` (heading "Radiant calm gums" unchanged) | `<p>A velvety foam nurturing your gums through fermentation.</p>` | `<p>Een fluweelzacht schuim uit fermentatie dat je tandvlees verzorgt.</p>` | `<p>Une mousse veloutée issue de la fermentation, qui prend soin de vos gencives.</p>` |
| 4 | `product_benefits_karmicare_bcQ6tp` · `card_KRCrBY` · `heading` | Guarana by day, valerian by night | Guarana overdag, valeriaan ’s nachts | Guarana le jour, valériane la nuit |
| 5 | `product_benefits_karmicare_bcQ6tp` · `card_KRCrBY` · `text` | `<p>Guarana helps keep plaque from sticking (in vitro). Valerian soothes the mouth by night.</p>` | `<p>Guarana remt het hechten van plaque (in vitro). Valeriaan verzacht de mond ’s nachts.</p>` ("verzacht", not "kalmeert": no calming-you reading; no "voorkomen": JEP/DETIC) | `<p>Le guarana freine l’adhésion de la plaque (in vitro). La valériane apaise la bouche le soir.</p>` |
| 6 | `product_benefits_karmicare_bcQ6tp` · `card_AGFiEX` · `text` | `<p>Spit, don’t rinse. With you all night. Feel it before breakfast.</p>` | `<p>Spugen, niet spoelen. De hele nacht bij je. Voel het nog voor het ontbijt.</p>` | `<p>Crachez, ne rincez pas. Avec vous toute la nuit. Sentez-le avant le petit-déjeuner.</p>` |
| 7 | `trusted_professionals_HAqYth` · (section) · `bottom_text` (homepage only; the product page keeps its approved text) | `<p>These practitioners recommend Karmicare between visits. Not to replace their care, but to make the brushings between appointments count for something.</p>` | `<p>Deze zorgverleners raden Karmicare aan voor de periode tussen twee bezoeken. Niet om hun zorg te vervangen, maar om de poetsbeurten tussen de afspraken door iets te laten betekenen.</p>` | `<p>Ces praticiens recommandent Karmicare entre deux visites. Non pas pour remplacer leurs soins, mais pour que les brossages entre deux rendez-vous comptent vraiment.</p>` |

## 2. Section schema defaults changed (not translatable, for the record)

| File | Default |
|---|---|
| `sections/stat-strip-karmicare.liquid` | stat `text` default and preset: "Formulated on +36 studies" → "Formulated on peer-reviewed studies" |
| `sections/two-formulas-karmicare.liquid` | `ingredients_list` default: BIOFILM PREVENTION → HELPS REDUCE BIOFILM |

## 3. R59b · Victor's choices of 24 Oct (homepage only)

Astra's open R59 homepage items (landing desk, 24 Oct), shown to Victor on the localhost preview. He kept the clock's night text and the seven ring messages, kept "Cortisol rises" and added the morning line, and took the FAQ answer without dashes and colons. The PDP clock keeps its current texts. The same FAQ wording is the default in `sections/km-faq-accordion.liquid`.

| # | Section · block · key | EN (new) | NL | FR |
|---|---|---|---|---|
| 10 | `chronobiology_clock_karmicare` · (section) · `morning_text` | Cortisol rises. Morning brings coffee, breakfast and the day's first acids. Enamel needs its shield on first. | Cortisol stijgt. De ochtend brengt koffie, ontbijt en de eerste zuren van de dag. Je glazuur heeft eerst zijn schild nodig. | Le cortisol monte. Le matin apporte le café, le petit-déjeuner et les premiers acides de la journée. L’émail a d’abord besoin de son bouclier. |
| 11 | `km_faq_accordion_FYcArV` · `faq_item_TNnqTQ` · `answer` | `<p>Because your mouth doesn’t do the same job all day. Daytime is exposure to acids, sugars and coffee, so Awake protects, activates and brightens. Night is repair, when saliva drops and your body regenerates, so Asleep soothes, supports your mouth’s balance and helps remineralise. Spit, don’t rinse. Left on after the evening brush, it gets extended contact time.</p>` | `<p>Omdat je mond niet de hele dag hetzelfde werk doet. Overdag draait het om blootstelling aan zuren, suikers en koffie, dus Awake beschermt, activeert en maakt stralender. ’s Nachts draait het om herstel, je speeksel neemt af en je lichaam regenereert, dus Asleep verzacht, ondersteunt de balans van je mond en helpt remineraliseren. Spugen, niet spoelen. Blijft het na het avondpoetsen zitten, dan krijgt het een verlengde contacttijd.</p>` ("verzacht" for soothes, as on the valerian card; the registered NL had "kalmeert") | `<p>Parce que votre bouche ne fait pas le même travail toute la journée. Le jour, c’est l’exposition aux acides, aux sucres et au café, alors Awake protège, active et éclaircit. La nuit, c’est la réparation, la salive diminue et votre corps se régénère, alors Asleep apaise, soutient l’équilibre de votre bouche et aide à reminéraliser. Crachez, ne rincez pas. Laissé en place après le brossage du soir, il bénéficie d’un temps de contact prolongé.</p>` |

Basis for row 11: CR1 C10/C11/C13 ("extended contact time", "after the brush"), C31 ("supports your mouth's own balance"), products.md "helps remineralise"; "rebalances" and "while you sleep" dropped; "soothes" is an allowed verb. Victor's style rule of 24 Oct: as few colons, semicolons and dashes as possible, so the copy reads as written by a person.

## 4. Clock messages `kc.clock.window_1`–`7` · no change (Victor, 24 Oct)

A trimmed EN set per CR1 C54 was shown on the localhost preview. Victor keeps the seven original messages: their point is the whole mouth across the day (enamel, teeth, gums, taste buds, saliva), and the trimmed set reduced them to saliva. Nothing for source-copy here. CR1 C54 stays an evidence item in the register (a cariology source for the pH and timing statements in messages 2–5).
