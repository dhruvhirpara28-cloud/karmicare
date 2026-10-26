# Round 7 · PDP trust pills, practitioner form

**Restarted 26 Oct against release 12 (live main `2f58500` = merchant-edit `be375ba`: fonts/colours, blog, practitioner form, clock).** Integration merged; the lane's theme files equal `2f58500`. `live/tools/live_vs_source.py` against `2f58500` finds two changes:
- the clock `hint_label` on `index` and `product.subscription-item` now reads *DRAG THE DOT · EXPLORE 24 HOURS*;
- the new blog template `templates/article.json` has a featured product block that repeats the homepage buy box.

The other text settings without a source row are not copy: Klaviyo IDs, colours, file names and Liquid references. The plans now hold:

| Item | NL | FR |
|---|---:|---:|
| PDP pills `text_1` (changed), `text_5` (new) | 2 | 2 |
| Practitioner form, 13 new `request_*` settings on both product templates (Klaviyo IDs out) | 26 | 24 (FR *Profession* equals the EN) |
| Clock hint, NL *SLEEP DE BOL · VERKEN 24 UUR*, FR *GLISSEZ LE POINT · 24 HEURES* | 2 | 2 |
| Blog featured product block, 11 copy settings (`article:featured_product_kc_blog/…`, batch 08 because batch 07 is held as blog content), NL/FR from their exact homepage twins, which are already registered | 11 | 11 |
| **Expected** | **41** | **39** |

The dry run can add byte-only re-registers. The blog keys of direction D are already in the locales (`b8b0331`).

The trigger text was re-checked live on release 12 in the Orca browser, read only. curl now gets a 403 from www, probably Shopify's bot protection after the day's checks.
- **NL:** the theme renders `data-trigger-text` "studiedossier", and both links contain it: "Vraag het studiedossier, …" and "Studiedossier en proefpakketten voor zorgverleners beschikbaar →".
- **FR:** "dossier scientifique", in "Demandez le dossier scientifique, …" and "Dossier scientifique et échantillons disponibles pour les praticiens →".

FR `check.py`: 75, NL `validate.py`: 62, both unchanged. `digest.py` passes.

**Clock footer text on the homepage out (landing desk 26 Oct, Victor: "may go for now").** `index:chronobiology_clock_karmicare/footer_text` ("Formulated for both shifts: Awake by day, Asleep by night.") is empty on the homepage branch, so it is `retired` in the EN source and held in NL/FR, as `footer_link_text` was. It was already registered, so the expected keys do not change: still NL 41, FR 39. The PDP row `product.subscription-item:…/footer_text` stays in the plan until the desk confirms.

**Parked 26 Oct (landing desk, Victor: "translations come last"):** the plans stay as committed at `1aaae63`, and no dry run has been made. Round 7 restarts against the new live text once the font/token change and the blog have landed. At the restart:
1. merge `karmicare/soft-launch`;
2. compare the source with the new live main;
3. rebuild the plans;
4. re-check the trigger text in the live NL/FR FAQ.

**Also in at the restart: clock hint (Victor approved 26 Oct, via the landing desk).** `chronobiology_clock_karmicare/hint_label`, on both `index` and `product.subscription-item` (INVENTORY #31, #41):

| | Now (source and registered) | New, approved |
|---|---|---|
| EN | DRAG THE RING · EXPLORE 24 HOURS | DRAG THE DOT · EXPLORE 24 HOURS |
| NL | SLEEP AAN DE RING · VERKEN 24 UUR | SLEEP DE BOL · VERKEN 24 UUR |
| FR | GLISSEZ L’ANNEAU · EXPLOREZ 24 HEURES | GLISSEZ LE POINT · 24 HEURES (Victor 26 Oct, shortened to fit one line at 360; replaces "GLISSEZ LE POINT · EXPLOREZ 24 HEURES") |

At the restart, take the EN from the live template. It must read exactly as above. Then the row becomes `corrected` (`old_en` kept), and NL/FR get the approved text. The registration overwrites the earlier NL/FR value.

**Change reversed 26 Oct (landing desk, Victor):** the form stays on the PDP as the popup, opened from both FAQ links; the professionals page is parked. The 52 holds are lifted, and the plans are again identical to `1ec484d`: pills 1 and 5 plus the 13 new `request_*` settings on both product templates. The Klaviyo ID settings stay out. Expected again: NL 28 keys, FR 26. The trigger text was re-checked live the same day: both NL links contain *studiedossier*, both FR links *dossier scientifique*.

**Earlier the same day, pills only (landing desk, Victor):** the practitioner form moves off the PDP to a new professionals page, so its `request_*` settings will leave the product templates. The 13 new `request_*` settings of this round are held in `holds.json` on both templates in NL and FR (52 holds). Their translations below stay in the payloads for the new page. The round 3 `request_*` keys were registered earlier and are left as they are. The plans now register only the two pills. Expected: **2 keys per language** (`text_1` changed, `text_5` new), plus the byte-only re-registers.

**Built** 26 Oct 2026 against live main `57e6588` (release 11; merchant-edit `6486f4b`, landings 68–69), theme `187295564157`. Brief from the landing desk, 26 Oct. Victor runs the dry runs; the desk checks them before the write. No Admin edits between dry run and write.

## PDP trust pills (`product.subscription-item`, highlights slider)

| Slot | EN (live) | NL | FR |
|---|---|---|---|
| `text_1` | Used and recommended by 100+ kPNI practitioners | Gebruikt en aanbevolen door 100+ kPNI-therapeuten | Adopté et recommandé par plus de 100 praticiens kPNI |
| `text_5` (new) | Recommended by functional dentists | Aanbevolen door functionele tandartsen | Recommandé par des dentistes fonctionnels |

Victor, 25 Oct, via the PDP lane:
- two pills, with "100+" only on the kPNI pill;
- "Used en Gebruikt is ok", recorded as a W1 exception in `nl/validate.py`;
- "kPNI-therapeuten" with a hyphen.

The FR keeps "Adopté", because FR rule W1 does not allow *utilis-*.

Claims:
- **C81** stays *kept* on Victor's decision. The source for "100+" is still open.
- **C104** ("Recommended by functional dentists") is *confirmed*: Victor named the dentists who are professional ambassadors on the site.

`templates/product.json` keeps its own single pill ("Used by +100 kPNI practitioners"), unchanged.

## Practitioner form (`product_faq_block`, both product templates)

13 new settings (R76e+f); R76g added none:

| Setting | EN | NL | FR |
|---|---|---|---|
| `request_legend_profession` | Profession | Beroep | Profession (equal to the EN, so the runner skips it) |
| `request_profession_dentist` | Dentist | Tandarts | Dentiste |
| `request_profession_hygienist` | Dental hygienist | Mondhygiënist | Hygiéniste dentaire |
| `request_profession_kpni` | kPNI therapist | kPNI-therapeut | Thérapeute kPNI |
| `request_profession_natural` | Orthomolecular or naturopathic practitioner | Orthomoleculair of natuurgeneeskundig therapeut | Praticien orthomoléculaire ou naturopathe |
| `request_profession_gp` | General practitioner | Huisarts | Médecin généraliste |
| `request_profession_pharmacist` | Pharmacist | Apotheker | Pharmacien |
| `request_profession_other` | Other | Andere | Autre |
| `request_label_profession_other` | Your profession | Je beroep | Votre profession |
| `request_label_practice` | Practice name | Naam van de praktijk | Nom du cabinet |
| `request_error_profession_choice` | Choose your profession. | Kies je beroep. | Choisissez votre profession. |
| `request_error_profession_other` | Please fill in your profession. | Vul je beroep in. | Veuillez indiquer votre profession. |
| `request_error_practice` | Please fill in your practice name. | Vul de naam van je praktijk in. | Veuillez indiquer le nom de votre cabinet. |

- The radio labels are short, so the user knows quickly which option fits.
- The values the form posts stay English; they come from the code.
- FR uses the generic masculine where a form needs it (*Pharmacien*, *Praticien*). The other labels are epicene.
- **Never translated:** `request_klaviyo_company_id` and `request_klaviyo_metric` are Klaviyo IDs. They are inventoried as `never_translate` and held in NL/FR.
- **Retired:** `request_label_profession`, `request_help_profession` and `request_error_profession` left the template. Their NL/FR translations stay in Shopify without a key that uses them.
- **Trigger text unchanged:** NL *studiedossier*, FR *dossier scientifique*, both from round 3. The live NL and FR FAQ links both contain the term (curl, 26 Oct):
  - NL: "Studiedossier en proefpakketten voor zorgverleners beschikbaar →" and "Vraag het studiedossier, …";
  - FR: "Dossier scientifique et échantillons disponibles pour les praticiens →" and "Demandez le dossier scientifique, …".

  `product-faq.liquid` and `kc-practitioner-request.js` both match case-insensitively on "contains", so the NL/FR links open the form.

**Expected:** NL 28 keys (2 pills, 26 form texts) and FR 26 (2 pills, 24 form texts). The dry run can add byte-only re-registers.

FR `check.py`: 75 and NL `validate.py`: 62, both unchanged. The `text_1`/`text_2` claim lines were already there before this round. `digest.py` passes.
