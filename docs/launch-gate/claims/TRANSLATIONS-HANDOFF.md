# Claims cleanup · translations handoff (R59, 24 Oct 2026)

For source-copy. Every EN string that R59 changed in `templates/index.json` and `templates/product.subscription-item.json`, with the NL and FR to register. Hidden blocks need no translation and are listed at the end. Section schema defaults changed in R59 are not translatable settings and are listed for completeness only.

Victor's keeps of 24 Oct are already applied: the sensitivity research card, the research intro, the "Cold or hot" card, the "settle gums" line and Sietske Hamelink's card are unchanged, so they are not in this list.

Conventions used: NL je-form, "peer-reviewed" stays English in NL (as in batch-02), FR uses vous and "revues à comité de lecture" (as in batch-02); Awake, Asleep, Leave-on, Care Credit and Return on Care stay English. FR thin spaces before `:` are written as plain spaces here; apply the FR spacing convention when registering (the Write tool drops no-break spaces).

Note for registration: a registered NL or FR translation of a key whose EN changed becomes outdated in Shopify and stops being served, so register the new NL and FR together with the theme release. The existing "translated" NL and FR entries for `stat_3/text`, `ingredients_list`, `highlights_slider_9wAjAb/text_1` and `text_2` were translations of the old EN and must not be registered as they stand.

Where "both" is given, the same block id and key exist in `templates/index.json` and `templates/product.subscription-item.json`; register both.

## 1. Changed strings

### 1.1 `templates/index.json`

| # | Section · block · key | EN (new) | NL | FR |
|---|---|---|---|---|
| 1 | `stat_strip_karmicare` · `stat_3` · `text` | Formulated on peer-reviewed studies | Geformuleerd op basis van peer-reviewed studies | Formulé sur la base d’études à comité de lecture |
| 2 | `two_formulas_karmicare` · (section) · `ingredients_list` | `<ul><li>FLUORIDE-FREE & SLS-FREE</li><li>MICROBIOME-CONSCIOUS</li><li>NANO-HYDROXYAPATITE (NHAP)</li><li>SYNERGETIC EFFECT</li><li>VELVETY FOAM</li><li>GLYCOLIPID CLEANSING</li><li>HELPS REDUCE BIOFILM</li><li>BELGIAN FORMULATION</li><li>VEGAN & HALAL</li></ul>` (only the seventh pill changed: BIOFILM PREVENTION → HELPS REDUCE BIOFILM) | `<ul><li>FLUORIDEVRIJ & SLS-VRIJ</li><li>MICROBIOOMBEWUST</li><li>NANO-HYDROXYAPATIET (NHAP)</li><li>SYNERGETISCH EFFECT</li><li>FLUWEELZACHT SCHUIM</li><li>REINIGING MET GLYCOLIPIDEN</li><li>HELPT BIOFILM VERMINDEREN</li><li>BELGISCHE FORMULERING</li><li>VEGAN & HALAL</li></ul>` | `<ul><li>SANS FLUOR & SANS SLS</li><li>RESPECTUEUX DU MICROBIOME</li><li>NANO-HYDROXYAPATITE (NHAP)</li><li>EFFET SYNERGIQUE</li><li>MOUSSE VELOUTÉE</li><li>NETTOYAGE AUX GLYCOLIPIDES</li><li>AIDE À RÉDUIRE LE BIOFILM</li><li>FORMULATION BELGE</li><li>VEGAN & HALAL</li></ul>` |
| 3 | `product_benefits_karmicare_bcQ6tp` · `card_VP8KGi` · `text` (heading "Radiant calm gums" unchanged) | `<p>A velvety foam nurturing your gums.</p>` | `<p>Een fluweelzacht schuim dat je tandvlees verzorgt.</p>` | `<p>Une mousse veloutée qui prend soin de vos gencives.</p>` |
| 4 | `product_benefits_karmicare_bcQ6tp` · `card_KRCrBY` · `heading` | Guarana by day, valerian by night | Guarana overdag, valeriaan ’s nachts | Guarana le jour, valériane la nuit |
| 5 | `product_benefits_karmicare_bcQ6tp` · `card_KRCrBY` · `text` | `<p>Guarana helps keep plaque bacteria from sticking (in vitro). Valerian root, chosen for the evening formula.</p>` | `<p>Guarana helpt het hechten van plaquebacteriën te beperken (in vitro). Valeriaanwortel, gekozen voor de avondformule.</p>` (no "voorkomen": JEP/DETIC) | `<p>Le guarana aide à limiter l’adhésion des bactéries de la plaque (in vitro). La racine de valériane, choisie pour la formule du soir.</p>` |
| 6 | `product_benefits_karmicare_bcQ6tp` · `card_AGFiEX` · `text` | `<p>Spit, don’t rinse. With you all night. Feel it before breakfast.</p>` | `<p>Spugen, niet spoelen. De hele nacht bij je. Voel het nog voor het ontbijt.</p>` | `<p>Crachez, ne rincez pas. Avec vous toute la nuit. Sentez-le avant le petit-déjeuner.</p>` |
| 7 | `trusted_professionals_HAqYth` · (section) · `bottom_text` (both) | `<p>These practitioners recommend Karmicare between visits. Not to replace their care, but to make the brushings between appointments count for something.</p>` | `<p>Deze zorgverleners raden Karmicare aan voor de periode tussen twee bezoeken. Niet om hun zorg te vervangen, maar om de poetsbeurten tussen de afspraken door iets te laten betekenen.</p>` | `<p>Ces praticiens recommandent Karmicare entre deux visites. Non pas pour remplacer leurs soins, mais pour que les brossages entre deux rendez-vous comptent vraiment.</p>` |

### 1.2 `templates/product.subscription-item.json`

| # | Section · block · key | EN (new) | NL | FR |
|---|---|---|---|---|
| 8 | `main` · `highlights_slider_9wAjAb` · `text_1` | Chosen by kPNI practitioners & functional dentists | Gekozen door kPNI-therapeuten & functionele tandartsen | Choisi par des praticiens kPNI et des dentistes fonctionnels |
| 9 | `main` · `highlights_slider_9wAjAb` · `text_2` | Formulated on peer-reviewed studies | Geformuleerd op basis van peer-reviewed studies | Formulé sur la base d’études à comité de lecture |
| 7 | `trusted_professionals_HAqYth` · (section) · `bottom_text`: as row 7 above | | | |

## 2. Hidden blocks (no translation)

`"disabled": true` on the block, in both templates:

| Section · block | What it was |
|---|---|
| `research_behind_system_EkjATL` · `card_fmFMFd` | Xylitol research card (tooth decay) |
| `research_behind_system_EkjATL` · `card_JeERX6` | SLS-free research card (canker sores) |
| `research_behind_system_EkjATL` · `card_bDxUVT` | 98 % tubule occlusion card (Kulal 2016, not in the library) |

Their existing NL and FR entries in `docs/localization/*/batch-01` and `batch-02` can stay as they are; nothing is served while the block is hidden.

## 3. Section schema defaults changed (not translatable, for the record)

| File | Default |
|---|---|
| `sections/stat-strip-karmicare.liquid` | stat `text` default and preset: "Formulated on +36 studies" → "Formulated on peer-reviewed studies" |
| `sections/two-formulas-karmicare.liquid` | `ingredients_list` default: BIOFILM PREVENTION → HELPS REDUCE BIOFILM |
| `sections/research-behind-system.liquid` | card defaults: the 98 % Kulal card → the Vano 2018 sensitivity card as it is live (heading, subtext, result, method, link label) |
| `sections/main-product.liquid` | highlights `text_1` default "Used by +100 kPNI practitioners" → "Chosen by kPNI practitioners & functional dentists"; `text_2` default "Backed by 39 peer-reviewed studies" → "Formulated on peer-reviewed studies" |
