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

| | Opening | Awake | Asleep | Close |
|---|---|---|---|---|
| NL (main session's proposal) | Ga met je tong over je tanden. Dat lichte laagje is je nulpunt. | frisse pepermunt en limoen, met guarana eronder. Een fluwelen schuim, niets prikt, niets droogt uit. Spuwen, niet spoelen. Tong er nog eens over: elke tand een gladde, glazige rand. | warme sinaasappel en cassiakaneel, valeriaan op de achtergrond, bewust zonder munt. Spuwen en laten zitten. Glad, met een fijn, egaal laagje, alsof de dag is afgesloten. | Twee seconden, twee keer per dag, en je weet het. |
| FR (new) | Passez la langue sur vos dents. Ce léger voile, c’est votre point de départ. | menthe poivrée et citron vert éclatants, guarana en fond. Une mousse veloutée, rien ne pique, rien ne dessèche. Crachez, ne rincez pas. Repassez la langue : chaque dent est lisse comme du verre. | orange chaude et cannelle cassia, valériane en fond, volontairement sans menthe. Crachez et laissez agir. Lisse, avec un voile fin et régulier, comme si la journée avait été refermée. | Deux secondes, deux fois par jour, et vous savez. |

The Taste & feel field binding is only added after Victor's OK. Until then the field is proposed and never written.

## Effect on the pending NL H1 write

The admin change of 13 Nov voids the NL dry run `d0f1203e7b09898a` (hero H1 back to "Nu je mondzorg ook"). With the old bindings, any write would also abort on the stale fields. The H1 now goes in with this round's dry run.

Checks: FR `check.py` 75, NL `validate.py` 62, both unchanged. `digest.py` passes. `plan_delta.py HEAD`: per language 2 added (#127 #128), 10 removed (retired), 6 changed (#45 #48 #50 #54 #105 #106).
