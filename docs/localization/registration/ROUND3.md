# Round 3 · scope and check.py triage

**Built** 25 Oct 2026 against live main `d5b514d` (merchant-edit `02d73c4`; the theme files equal integration `5922b8b` apart from `config/settings_data.json`), theme `187295564157`. The plans are `plan-nl.json` and `plan-fr.json` at the commit that adds this file. Victor runs the dry runs; the write follows the review.

## What the plans add

| Item | NL | FR | Source |
|---|---:|---:|---|
| Care Credit fine print (homepage, PDP) and `info_card_FnBcaN/footer_text`, without "never on your dental bill" | 3 | 3 | data from `b8d8d69` (Victor, 25 Oct) |
| Research image badges, xylitol / Vano / Alli cards, homepage and PDP (landing 55) | 6 | 6 | EN from live main; NL/FR from the glossary (*dentinekanaaltjes*, *tubules dentinaires*) |
| Practitioner request form `product_faq_block.request_*`, 26 settings on `product.subscription-item` and on `product` (landings 58–59) | 52 | 52 | NL/FR in the wording of the withdrawal form and the FAQ term *studiedossier* / *dossier scientifique* |
| Homepage SEO title, now *KARMICARE - Biorhythmic Oral Care* | 1 | 1 | live `<title>`, curl 25 Oct; NL/FR as the approved "Biorhythmic Oral Care" strings |
| Leen Ponet's role title on the cards, homepage and PDP | – | 2 | *Pharmacienne, thérapeute orthomoléculaire, coordinatrice kPNI* (Victor 24 and 25 Oct) |
| **Expected new or changed keys** | **62** | **64** | the dry run can add byte-only re-registers |

Left out: the footer-group legal labels (they go through `kc.footer.legal_*` in the locales since `fe24325`), the stale items of the round 2 dry run outside this scope (two Loop selling-plan descriptions, toothbrush and kit product bodies, the "Date:" blocks of two legal pages, three product SEO titles whose live key differs from the visible title), the SHOP_POLICY bodies (the desk pastes them) and the research metaobjects (after launch).

## check.py (FR): 128 errors before, 77 after

| Group | Before | After | Verdict |
|---|---:|---:|---|
| `source_status` differs from the source status | 36 | 0 | fixed in the data: FR mirrors the EN source status; no value changes, no registration effect |
| unknown flag `admin` (product FAQ #114, #115) | 2 | 0 | fixed: flag dropped, `source_status` added; the status was already `admin` |
| held entries carry `fr = null` | 13 | 0 | fixed: the retire scripts wrote `""`; six of the 13 were the badges that round 3 un-retires |
| needs-review claim translated without `pending-claim-review` | 39 | 39 | no action: the claims gate was released on 22 Oct (`releases.json`); the rule predates the release |
| W1 commodity word (*utilise*, *produit* …) | 20 | 20 | no action: all inside the practitioners' own quotes (Spreuwers, Banjai, Sietske), approved by Victor |
| unsupported claim requires a hold | 4 | 4 | no action: Sietske's quote (C84, C85) and the C35 card carry Victor's waiver of 20 Oct, and the gate was released 22 Oct |
| legal entry without `legal-review` | 5 | 5 | no action: two `kc.footer.legal_*` locale keys (theme-key channel), two retired footer-group rows, the hand-registered withdrawal page title; the legal gate was released 23 Oct |
| markup differs from the EN | 7 | 7 | no action: links point to `/nl/…` and `/fr/…` pages instead of the EN paths |
| S1 address not exactly as in the EN | 2 | 2 | no action: the withdrawal page FR (R73 handoff, registered in round 2) names the country *Belgique*; the FR terms and consumer-rights pages keep *Belgium*. One form everywhere is Victor's choice |

None of the 77 changes what the runner writes. The NL validator reports 64 errors, the same as before round 3.

## Known

- `register_selftest.py` fails on "approved snapshot registers every register op" (100 field bindings no longer match its fixture), on the committed state before round 3 as well; `register.py` and `bindings-fields.json` are untouched in this round.
