# R2 source changes, for the FR payload

The NL review `docs/runtime-review/B2-NL-ASTRA.md` (19 Oct, verdict FAIL) led to these changes in the EN source. Merge `karmicare/soft-launch-source-copy` to receive them. This file lists every source-level change since `2194ef3` (the R1 state FR merged in `71b3c5a`), so the FR payload can follow it exactly.

How the list was made: `en-source.json` at `2194ef3` was compared with the current file entry by entry. The result is 1 entry added (needs-review), 0 removed, 3 newly held, 16 reclassified to needs-review, 3 changed in notes only, and 84 more entries with a derived `claim_status`. `python3 docs/source-copy/digest.py` exits 0.

## Digests

Only batch 06 changed. FR `batch-06-content-pages.json` is stale until it has the new entry; every other FR `source_digest` stays valid.

| Batch | Before (2194ef3) | Now |
|---|---|---|
| `batch-06-content-pages` | 21 entries, `f78c391aa267b82eb0c85af36edea6e4583651bf` | 22 entries, `3dee3b56341f67b113dcd59eb85d3a2e3f21d628` |
| all other batches | unchanged | unchanged |

## 1. Added: translate it

| Id | Batch | EN | Gate | FR action |
|---|---|---|---|---|
| `admin:page:nhap-technology:body_html#b000` | 06 | `Discover the Wonderful Inner World of Nano Hydroxyapatite and Why You Need it in Your Toothpaste<br><br>` | `claim_status: needs-review` (necessity wording) | Insert it before `#b001` and mark it pending-claim-review. NL reused its translation of `admin:article:news/nano-hydroxyapatite:title` (the same EN) and kept the trailing `<br><br>`. |

This is the `h1` inside `.rte` on `/pages/nhap-technology`. The B2 builder skipped it because the text equals an article title. A sweep of every capture found no other block lost this way.

## 2. Newly held: do not translate

| Id | Batch | Source change | NL note (FR can use the same reason) |
|---|---|---|---|
| `admin:product:asleep-evening-toothpaste-2-0:body_html#b002` | 05 | `claim_status: unsupported`, basis added | `unsupported-claim: sleep/wake effect; same hold as this resource's seo.description` |
| `admin:product:awake-morning-toothpaste-2-0:body_html#b002` | 05 | `claim_status: unsupported`, basis added | as above |
| `admin:article:news/3-reasons-why-you-should-look-for-an-sls-free-toothpaste:body_html#b035` | 07 | `blocked: "NEEDS APPROVED COPY"` (four competitor names) | `needs-approved-copy: competitor names prohibited; EN owner must supply compliant source` |

FR already holds the two sleep/wake lines (`58755f7`). Only the SLS block is new for FR.

## 3. Reclassified to needs-review: pending-claim-review in FR

| Id | Batch | Before → now | Why (full basis in `claim_basis` / CLAIMS-REVIEW.md) |
|---|---|---|---|
| `admin:whitening-charcoal-dental-floss:title` | 02 | none → needs-review, `claims: ["C100"]` | Floss-whitening wording, new register claim C100 |
| `admin:karmicare-biorhythmic-oral-care-system:custom.compare_table:welcome_kit_row.products` | 02 | none → needs-review, C100 | as above |
| `admin:karmicare-biorhythmic-oral-care-system:media.69271648010621.alt` | 02 | none → needs-review, C100 | as above (kit image alt) |
| `admin:karmicare-biorhythmic-oral-care-system:media.69884688236925.alt` | 02 | none → needs-review, C100 | as above (kit animation alt) |
| `product:main/highlights_slider_9wAjAb/text_1` | 05 | none → needs-review; `status` approved → needs-review | "+100 kPNI practitioners", the same endorsement count as C81 |
| `admin:product:complete-hygiene-kit:body_html#b001` | 05 | none → needs-review | Floss-whitening wording |
| `admin:product:complete-hygiene-kit:seo.description` | 05 | none → needs-review | Floss-whitening wording |
| `admin:product:morning-toothbrush:body_html#b001` | 05 | none → needs-review | Retired "2 to 4 applications" dose; keep the source number |
| `admin:product:morning-toothbrush-2-0:body_html#b001` | 05 | none → needs-review | as above |
| `admin:article:news/nano-hydroxyapatite:body_html#b069` | 07 | approved → needs-review | "remineralizes teeth from the inside" mechanism |
| `admin:article:news/nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste:body_html#b041` | 07 | approved → needs-review | "saliva isn't enough on its own" (necessity) |
| `admin:article:news/headaches-and-tooth-pain-understanding-the-connection:body_html#b019` | 07 | approved → needs-review | "Bestselling" (unverified superlative) |
| `admin:article:news/nano-hydroxyapatite:title` | 07 | none → needs-review | "Why You Need it in Your Toothpaste" (necessity) |
| `admin:article:news/nano-hydroxyapatite:text#01` | 07 | none → needs-review | the same title as image alt |
| `admin:article:news/nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste:title` | 07 | none → needs-review | "Why You Need It In Your Toothpaste" |
| `admin:article:news/nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste:seo.title` | 07 | none → needs-review | as above |

## 4. Notes only: a translation rule, no gate change

| Id | Batch | Note | FR action |
|---|---|---|---|
| `page.consumer-rights:legal_toc_section_gYznx3/content_section_FcEDdA/content` | 04 | Heading 4.1 "Two-year presumption of conformity" reads as the opposite of the rule it introduces; the legal owner approves or corrects the EN. | Translate the heading as written, a presumption of *conformity*, not of non-conformity. Change only the heading text and keep `legal-review`. |
| `admin:policy:refund-policy:body#b065` | 04 | as above | as above |
| `admin:article:news/nano-hydroxyapatite:body_html#b036` | 07 | "naturally occurring organic biomaterial": the EN or clinical owner resolves "organic". | Keep "organic" as written; the entry stays pending-claim-review. |

## 5. Metadata only: no FR action

- **`claim_status` on every claim-bearing entry.** 84 more entries in batches 01–03 have it now, as the strictest status of their `claims`. Together with the 4 C100 entries in section 3, that makes 88: 12 approved, 72 needs-review, 4 unsupported. Their gates are unchanged. A checker can now read every gate from the entry itself.
- **CLAIMS-REVIEW.md.** The batch 01–03 register has 67 claims (17 approved, 47 needs-review, 3 unsupported). Batches 05–07 hold 30 approved, 274 needs-review and 115 unsupported blocks: 6 blocks were added and 9 reclassified.

## 6. NL payload rules from R2 that apply to FR too

These are not source changes. They are the review's payload findings, which FR can check against its own files. The NL commits and `docs/localization/nl/REPORT.md` ("R2 fixes") have the details.

| Finding | Rule | Where to look in FR |
|---|---|---|
| F3 | Translate a legal proposition as written. A correction belongs to the legal owner. | the two entries in section 4 |
| F4 | Keep the EN's hedges ("can", "may", "will help", "may want to") and every source assertion. | SLS article `#b056` and `#b028`, nano-hydroxyapatite `#b036` |
| F6 | No competitor names. Keep commodity words (product, use, buy, tube) out of promotional prose: the morning-brush bodies, "Used by …" headings, "everyday products" (nootropics `#b012`, `#b051`, `#b064`), fluoride `#b016`. Official names (the EU CPNP portal), legal document titles, the footer compliance line and approved Figma text stay as they are. | NL changed 24 entries, the held SLS block included |
| F7 | `fit-risk` on constrained strings that grow; title flags are contextual QA. | both `research_behind_system_EkjATL/button_label`, PDP `loop_subscriptions_gPKypi/shipping_value_html`, `icon_with_text_endcta/heading_3`, `custom.comparison_section#18` and `#23` |
| F8 | Addresses exactly as in the EN, including "box 1" and the EN city and country names. | `Vizierstraat 28, 8000 Bruges, Belgium`; `Boulevard du Roi Albert II 8, box 1, 1000 Brussels` (and `, Belgium`); `Koning Albert II-laan 16, 1000 Brussels`; `Drukpersstraat 35, 1000 Brussels, Belgium`; footer `Vizierstraat 28, 8000, Belgium`. These are 33 spans in 29 entries. |
| F9 | The same EN gets the same translation. Check identical homepage/PDP twins and repeated legal passages. | the model withdrawal sentence (terms `#b155`, refund `#b114`, consumer-rights `content_section_at3pLy`) keeps the EN's `(*)` markers |
| F10 | Every `never_translate` entry is held, including the two Dawn keys `locale:general.social.links.facebook` and `.instagram`. | batch 03 |

The NL validator `docs/localization/nl/validate.py` now checks these invariants. FR's `check.py` can apply them to the `fr` field:

- **H1**: `claim_status` unsupported → held.
- **H2**: needs-review → held or pending-claim-review.
- **H3**: `legal` → held or legal-review.
- **H4**: `legacy` → held.
- **H5**: `never_translate` → held.
- **H6**: `blocked` → held.
- **H7**: every hold has a reason.
- **S1**: EN addresses unchanged.
- **S2**: `(*)` count kept.
