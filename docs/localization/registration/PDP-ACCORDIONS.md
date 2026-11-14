# PDP accordions 8 → 6 · registration round (13 Nov 2026)

**Asked** by Victor's main session on 13 Nov (`REQUEST-2026-11-13-pdp-accordions.md`, untracked in this worktree). The EN changed in Shopify admin that afternoon:
- Taste & feel was rewritten.
- For dentists became For professionals, with the kPNI text merged in.
- Why Karmicare and kPNI left the product's `custom.product_faq` list.

The new EN was read from the live PDP (www.karmicare.com, Orca same-origin fetch, 13 Nov). `live/tools/apply_pdp_accordions.py` checks that every new or reused EN segment is a text run of that page before it writes.

## Source rows (`custom.product_faq#NN`)

| Change | Rows | Notes |
|---|---|---|
| EN corrected | #45 #48 #50 #54 | Taste & feel: the opening line, the Awake and Asleep runs (each starts with ": " after the bold name) and the closing line |
| EN corrected | #105 #106 | kPNI: the bold run now ends with the full stop ("Oral–gut–brain axis."). Same words. NL/FR moved the full stop the same way. |
| New | #127 | "For professionals" (title). NL *Voor professionals*, FR *Pour les professionnels*. |
| New | #128 | "For kPNI and orthomolecular practitioners" (label). NL *Voor kPNI- en orthomoleculaire therapeuten*, FR *Pour les praticiens kPNI et orthomoléculaires*. |
| Kept | #77 | "For dentists" is now the dentists label inside For professionals; NL/FR unchanged. |
| Reused | dentists rows, kPNI #100–#104, link #98 | Byte-identical runs inside For professionals. The closing link keeps *studiedossier* / *dossier scientifique*, the triggers of the practitioner form. |
| Retired | #01 #02, #99 #107, #46 #51 #52 #53 #125 #126 | Why Karmicare; the kPNI title and its dropped link; the old Taste & feel runs. Payload rows held, old value kept in the notes. |

Field bindings removed from `bindings-fields.json` (NL and FR, 7 each), because a changed or unreached bound field aborts every write:
- Why Karmicare `515150872957|title`, `|description`;
- kPNI `564919959933|title`, `|description`;
- Taste & feel `564940013949|description`;
- For professionals `515151397245|title`, `|section_content`.

The next dry run proposes the new fields (`live/fields-proposed-<lang>.json`). Reviewed proposals go back into `bindings-fields.json`, and a second dry run gives the checksum for the write.

## Taste & feel NL and FR: wait for Victor's OK

Victor's choices for the NL on 13 Nov (via the other source-copy chat): *Spugen* (not *spuwen*), *startpunt*, and the words the live NL already uses (*Glijd met je tong*, *ruw laagje*, *fluweelzacht schuim*, *Nog eens met je tong*, *een gladde rand, als glas*, *alsof de dag werd afgesloten*). The opener #45 has its NL. #54 is unchanged.

**NL Awake #48 and Asleep #50: Victor chose version A on 14 Nov** (`live/tools/apply_taste_feel_a.py`): *met een activerende ondertoon van guarana* and *met een rustgevende ondertoon van valeriaan*.
- Flagged before his choice, by both source-copy chats: *rustgevend* is the calming effect brand rule #16 rules out (C40/C41), and the pair reads like the dropped "Focus by day, calm by night".
- The alternative B was *verfrissende* / *verzachtende ondertoon*. Victor chose A knowingly: *activerend* follows the approved hero line "Awake activeert".
- The NL is final.

Still open: **FR**, Victor's OK on the whole Taste & feel. The FR mirrors A: *une note tonifiante de guarana* and *une note apaisante de valériane* (no *vive*, which reads as "living", like *levendig*).

| | Opening | Awake | Asleep | Close |
|---|---|---|---|---|
| NL | Glijd met je tong over je tanden. Dat lichte, ruwe laagje is je startpunt. | frisse pepermunt en limoen, met een activerende ondertoon van guarana. Een fluweelzacht schuim, niets prikt, niets droogt uit. Spugen, niet spoelen. Nog eens met je tong: elke tand een gladde rand, als glas. | warme sinaasappel en cassiakaneel, met een rustgevende ondertoon van valeriaan, bewust zonder munt. Spugen en laten zitten. Glad, met een fijn, egaal laagje, alsof de dag werd afgesloten. | Twee seconden, twee keer per dag, en je weet het. |
| FR (draft) | Passez la langue sur vos dents. Ce léger voile, c’est votre point de départ. | menthe poivrée et citron vert éclatants, avec une note tonifiante de guarana. Une mousse veloutée, rien ne pique, rien ne dessèche. Crachez, ne rincez pas. Repassez la langue : chaque dent est lisse comme du verre. | orange chaude et cannelle cassia, avec une note apaisante de valériane, volontairement sans menthe. Crachez et laissez agir. Lisse, avec un voile fin et régulier, comme si la journée avait été refermée. | Deux secondes, deux fois par jour, et vous savez. |

The Taste & feel field binding is added per language: NL from the next dry run's proposal, FR only after Victor's OK. Until then the field is proposed and never written.

## Dry run of 13 Nov 15:05 and the follow-up

Victor ran `register.py --theme-id 187295564157` (NL `39ddfe4a31848cca`, FR `976a585e5dffc1fb`; never written):
- 17 byte-only ops per language;
- 3 field proposals (For professionals title and section_content, Taste & feel description);
- 1 stale binding, Kris `564998570365|designation`. Victor had already changed that designation in Admin to "GP, Sports & Lifestyle Medicine", so the field no longer matched its row.

Follow-up (`live/tools/apply_dryrun_followup.py`):
- **Kris**: row `custom.professional_testimonials#10` takes that EN (sha1 `6d0ee676…`) and the NL/FR Victor approved on 2 Nov. The stale binding is removed, so the next dry run proposes the field again. The metaobject's placeholder description stays untranslated.
- **For professionals**: both proposals were reviewed and bound, NL and FR. The assembly is the registered dentists HTML plus the two labels and the registered kPNI text.

## The NL H1 was written on 10 Nov

This section first said the admin change voided the NL dry run `d0f1203e7b09898a`. That was wrong: Victor wrote it on 10 Nov at 13:45 (`live/journal-nl.jsonl`, 21 of 21 confirmed). The H1 shows `same` in the dry run of 13 Nov. The run is now in `RUNS.md`. There was no FR run that day.

Checks: FR `check.py` 75, NL `validate.py` 62, both unchanged. `digest.py` passes. `plan_delta.py HEAD`:
- at c5d6202, per language: 2 added (#127 #128), 10 removed (retired), 6 changed (#45 #48 #50 #54 #105 #106);
- in the follow-up: Kris #10 changed (NL and FR), #45 changed (NL).
