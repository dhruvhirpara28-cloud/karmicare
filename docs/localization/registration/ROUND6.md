# Round 6 · product names, descriptions, Evening Toothbrush SEO title

**Built** 25 Oct 2026 after the round 5 writes (`RUNS.md`), on the domain www.karmicare.com (live since 25 Oct). The EN was checked against the live `/products/<handle>.js`. Victor runs the dry runs; the write follows the review.

## What changed in the Admin (source-copy at Victor's request, 25 Oct, read back live)

- **Names without "2.0":** Awake Morning Toothpaste, Asleep Evening Toothpaste, Morning Toothbrush, Evening Toothbrush. The handles stay `…-2-0`. Six old products are named "… 1.0" and archived: Awake and Asleep toothpaste, Morning and Evening toothbrush, the Duo and the Complete Hygiene Kit.
- **Descriptions** of Morning Toothbrush, Evening Toothbrush and Whitening Charcoal Floss, as Victor approved them ("ja graag productteksten opschonen"):
  - clean `<p>` markup and the typos corrected;
  - no activated charcoal on the evening brush;
  - "It perfectly fits one pump of Awake or Asleep" back in;
  - the unsourced claims gone: pearly white, coffee stains, tartar, "nourished by each mineral";
  - links to the 2.0 brushes on the shop itself.
- **Evening Toothbrush SEO title:** "KARMICARE Ultra-soft Evening Toothbrush", without "Detoxifying".
- **Asleep Evening Toothpaste:** markup only (registered in round 5). Its text still carries claims that Victor has not reviewed.

## Source and payloads

- **Titles:** six rows lose " 2.0" in EN, NL and FR. Two of the rows are the same Shopify key for the brushes.
- **Descriptions:** one row per paragraph, the way the runner assembles blocks, as for Asleep. Morning and Evening have 5 paragraphs, the floss has 3; 10 rows are new.
  - NL/FR come from the existing translations with the same cuts.
  - "one pump" follows the FAQ: *één pompje*, *une pression*.
  - The links go to `/nl/products/…-2-0` and `/fr/products/…-2-0`. In FR, Shopify redirects those to the translated handle. FR `check.py` reports the two link blocks as a markup difference from the EN, as it does for the legal pages; that is intended.
- **Evening SEO title:** NL "KARMICARE ultrazachte avondtandenborstel", FR "Brosse à dents du soir ultra-douce KARMICARE". The claim gate (*ontgiftende*, *détoxifiante*) falls away with the word.
- **Homepage SEO protected:** `admin:system:search:seo.description` and `admin:system:collections:seo.description` map to the same shop `meta_description` as the homepage description, which Victor set by hand (`registered.json`). Once the homepage row left the plan, the search row entered the wave with the old EN, so both are `retired`. No SHOP item is left in the plans.

**Expected:** 8 keys per language, plus the byte-only re-registers:
- 4 product titles;
- 3 descriptions (one assembled key per product);
- the Evening Toothbrush SEO title.

## Not in this round

- **PDP pills of R78** (`text_1` shortened, `text_5` "Recommended by functional dentists"). They are in integration (`cfa7005`) but not live yet: the live PDP still shows "Used by 100+ kPNI practitioners & functional dentists". They follow after the deploy, with R78b's wording "Used and recommended by…" if that lands. Victor's NL is "Gebruikt en aanbevolen door 100+ kPNI therapeuten". The FR draft is "Adopté et recommandé par plus de 100 praticiens kPNI". Three questions are open with Victor: W1 "gebruik", the recommendation claim on 100+, and the hyphen.
- **Practitioner form R76e+f:** 13 new `request_*` keys and 3 removed ones. The desk reports them when they land.

FR `check.py`: 75 errors (73 before; the 2 link blocks). NL `validate.py`: 62, unchanged. `digest.py` passes.
