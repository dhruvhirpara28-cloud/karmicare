# Request: plan card labels in NL and FR, two new `kc.receipt.*` keys (13 Nov 2026)

From: the nl-buybox-labels lane (`karmicare/nl-buybox-labels`). For: the source-copy lane, wording by the NL voice lane.
Status: open. Delete this file once the keys and the two snippet lines are live.

## What changed

On /nl and /fr product pages the two plan cards mix languages. The plan names and Loop's option text are in the
page language, the labels the theme adds were English literals in `assets/loop-widget.js`. The cards now look
their labels up in the page language, the way the receipt under them does: the `kc.receipt.*` keys, rendered as
data attributes on `.kc-pricing-summary` by `snippets/kc-receipt-labels.liquid`, read through `kcLabelText`.
Where an attribute is missing the script writes the English text it wrote before.

Two of the four labels reuse keys that exist. Two need new keys:

| Label on the card | Key | Status |
|---|---|---|
| Right, 60-day card | `kc.receipt.per_days`, [count] = the plan's billing days | exists in EN, NL, FR |
| Right, year card | `kc.receipt.per_year` | exists in EN, NL, FR |
| Left, year card, first line | `kc.receipt.renews_year` | **new** |
| Left, both cards, price line | `kc.receipt.per_brushing`, [price] = the plan's price per brushing | **new** |

## Decision

The English values are the texts the cards show today. The NL and FR values are **proposed**: they mirror the
words the receipt already uses ("poetsbeurt", "brossage"). The NL voice lane decides the wording.

| Key | EN (as today) | NL (proposed) | FR (proposed) |
|---|---|---|---|
| `kc.receipt.renews_year` | Renews every year | Vernieuwt elk jaar | Se renouvelle chaque année |
| `kc.receipt.per_brushing` | [price] / brushing | [price] / poetsbeurt | [price] / brossage |

No new claims and no numbers: the price is the one the script computes, and [price] stays in the text as it is.

## Asked of source-copy

1. Add `kc.receipt.renews_year` and `kc.receipt.per_brushing` to `locales/en.default.json`, `locales/nl.json` and
   `locales/fr.json`, in the `kc.receipt` block next to `per_days`, with the values above once the NL voice lane
   has decided the NL (and the FR has its OK).
2. Plain text only, no markup and no `&` or `<`: the script writes these two texts into the card as HTML, next to
   the formatted price. Keep the placeholder `[price]` in square brackets, as `one_time_note` has it.
3. The right-hand label needs no new text: `per_days` is already "/ [count] dagen" and "/ [count] jours",
   `per_year` "/ jaar" and "/ an".
4. Land the keys in `karmicare/soft-launch` and tell the landing desk, so this lane can add its follow-up below.

## Then, this lane (the order)

The two attributes can only be added after the keys exist. Before that, Theme Check fails on them
(`TranslationKeyExists`: no entry in `locales/en.default.json`) and the storefront would have no text for them.

1. Now, commit 1 on `karmicare/nl-buybox-labels`: `assets/loop-widget.js` and this request.
2. After the keys are in `karmicare/soft-launch`: sync this lane from it and add these two lines to
   `snippets/kc-receipt-labels.liquid`, after `data-kc-one-time-note`, with the comment updated:

   ```liquid
   data-kc-renews-year="{{ 'kc.receipt.renews_year' | t }}"
   data-kc-per-brushing="{{ 'kc.receipt.per_brushing' | t }}"
   ```

   Theme Check `--fail-level error` exits 0, commit 2.
3. The landing desk lands the JS, the keys and the two snippet lines together.

## What a visitor sees at each step

- English pages: no change at any step.
- /nl and /fr with commit 1 alone: the right-hand label turns Dutch or French at once, because it reads the
  existing `per_days` and `per_year` attributes ("/ 60 dagen", "/ jaar", "/ 60 jours", "/ an"). The left lines
  stay English ("Renews every year", "€0,49 / brushing") until the keys and the two snippet lines land. That is
  why the desk lands them together.
- /nl and /fr with everything landed: "Vernieuwt elk jaar", "€0,49 / poetsbeurt", "Se renouvelle chaque année",
  "€0,49 / brossage" (or the wording the NL voice lane decides).
- Not touched: the `ships → Renews` replacement on the 60-day card applies to the English option text only. Loop's
  own option texts ("levering om de 60 dagen", "expédition tous les 60 jours") stay as they are; Loop keeps its
  own copies of those.

Check /nl and /fr product pages on www.karmicare.com after landing: both plan cards, 60-day and year.
