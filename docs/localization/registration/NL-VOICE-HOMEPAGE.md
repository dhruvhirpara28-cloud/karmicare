# NL voice batch homepage · registration plan

**Built** 27 Oct 2026. The batch comes from `soft-launch-nl-voice` `docs/nl-voice/03-BATCH-homepage.md` @ `ebd4bd7`, approved by Victor on 27 Oct and passed on by the landing desk. The live main is `fff913d` (release 13), which equals the EN source: `live/tools/live_vs_source.py`, 0 changed. The plans combine this batch with the parked round 7, without its form part: the form registers on its own section group after release 14 (`ROUND7.md`).

## How the 48 rows go in

`live/tools/apply_nlvoice_homepage.py` parses the batch, checks every row against the NL payload, and applies it.

| Channel | Rows | Notes |
|---|---:|---|
| `index` template rows, through `register.py` | 35 | hero 4, stat strip 2, clock title and morning text 2, two formulas 7, benefits 9, professionals 2, research 3, FAQ 4, Care comes back 2 |
| Homepage SEO title, through `register.py` | 1 | "KARMICARE \| Fluoridevrije tandpasta met nano-hydroxyapatiet". Victor had registered the NL by hand, so the NL entry leaves `registered.json` and the runner writes it. The FR stays registered by hand. |
| Clock window keys `kc.clock.window_1` to `_7`, through `locales/nl.json` | 7 | Commit `d4d12ec`, theme files, through the landing desk |
| Loop widget labels (`loop-widget-standard.liquid:123`, `loop-widget.js:2463`, `:2468`) | 3 | NL payload only, as a record: "Eenmalig proberen" (the one-time option, `loop-one-time-purchase-option-label`), "Vernieuwt", "Vernieuwt elk jaar". These strings are hardcoded in the off-limits Loop widget files (`needs-key`), so there is no live channel. |
| Held (landing desk) | 2 | `card_qMHDBq/text` "Koud of warm, zonder pijn." goes to the claims review first (fallback "zonder angst voor die pijnscheut"). `faq_item_7jmEGi/answer` stays pending C101. |
| Not changed in the batch itself | 2 | `step_next_order/title`, `care_credit_text_1` |

Not in this batch: the Loop key `:103` "Kies je ritme". It waits for the PDP batch.

**Markup.** The batch shows the NL without the payload's HTML. Each new text gets the same markup as the current NL:
- a whole-text `<p>…</p>` around 13 rows;
- the inline `<strong>` in the professionals heading and the `<em>` in the Care comes back heading, around the same part of the new sentence.

The script checks that the current text in the batch matches the payload with the tags left out, that the tag structure stays the same, and that no new NL contains an em dash or a spaced en dash.

## Expected keys

| | NL | FR |
|---|---:|---:|
| NL voice homepage (35 template rows + SEO title) | 36 | – |
| Round 7 without the form: pills 1 and 5, clock hint, blog featured product block (11) | 15 | 15 |
| **Total** | **51** | **15** |

The dry run can add byte-only re-registers. The round 7 form keys are held in `holds.json` (52 holds) until release 14.

Checks: FR `check.py` 75, NL `validate.py` 62, both unchanged. `digest.py` passes. `theme_keys.py check` is ok. Theme Check (`--fail-level error`) exits 0.
