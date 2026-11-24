# Buybox-ab prototype notes (24 Nov 2026)

Plan: [PLAN.md](PLAN.md). Prototype on branch `karmicare/buybox-ab`, switch default **link** (today).
Nothing pushed, no theme uploaded, no admin or Loop admin change, no cart or checkout opened.

## How to view it

A localhost preview, no `shopify theme dev` (Victor's preference, and the dev theme is shared):
the live Duo page (cookie-less fetch of www.karmicare.com, theme `karmicare/main` 187295564157, 24 Nov)
with this branch's `loop-widget.js`, `kc-plan-select.js` and `kc-buybox.css`, and the Liquid output of
the branch's `main-product.liquid` / `kc-plan-config.liquid` changes emulated in the HTML
(`preview/build.py`). Loop, prices and the sticky bar run for real; `/cart.js` answers an empty cart,
so nothing can be bought from it.

- Switch ON: http://127.0.0.1:9372/on/en/products/karmicare-biorhythmic-oral-care-system
  (also `/on/nl/…`, `/on/fr/…`)
- Switch OFF: http://127.0.0.1:9372/off/en/products/karmicare-biorhythmic-oral-care-system
- Live, untouched, for comparison: http://127.0.0.1:9372/live/en/products/karmicare-biorhythmic-oral-care-system
- Day/Night: the PDP has no toggle; it follows the clock (`assets/day-night-mode.js`). The shots set
  the body class `day-mode` / `night-mode`.

If the server is gone, from the repo root:

```sh
python3 -I docs/buybox-ab/preview/build.py <dir with duo.html duo-nl.html duo-fr.html and the Awake/Asleep pages> . <serve dir>
python3 -I docs/buybox-ab/preview/server.py <serve dir> 9372
```

The page has to be served at a path ending in the product handle: Loop only updates the receipt
when the last path part is the handle (`getCurrentPathLoop`).

## Shots (`docs/buybox-ab/shots/`, PNGs are gitignored, local only)

| Shot | What |
|---|---|
| `off-en-390-day.png`, `off-en-390-night.png`, `off-en-1440-day.png`, `off-en-1440-night.png` | Switch OFF: 60-Day preselected, link under the cards, as today |
| `on-en-390-day.png`, `on-en-390-night.png`, `on-en-1440-day.png`, `on-en-1440-night.png` | Switch ON: Try once card first and selected, then 60-Day, then Year; CTA "Try once" |
| `on-nl-390-day.png`, `on-fr-390-day.png` | Switch ON in NL ("Eenmalig proberen · 1 duo") and FR ("Essayer une fois · 1 duo") |
| `live-en-*.png` | The live page, for the OFF comparison |
| `probes.json` | Per shot: language, mode, width, layout, CTA text, summary text, selling plan in the form, Loop group, sticky bar title, every visible card with position, height, checked state and text |

## Results

1. **ON, all languages, Day and Night, 390 and 1440:** the Try once card is first and checked on load
   (also 6 s after load, past kc-plan-select's 800 ms default and the end CTA widget); form
   `selling_plan` empty, Loop group `loop-one-time-purchase`; CTA "Try once" / "Eenmalig proberen" /
   "Essayer une fois"; summary "Total today €67 · €0.56 per brushing · no Care Credit · one-time";
   sticky bar "Try Once · 1 Duo"; the link under the cards is hidden.
2. **Switching (ON, 1440):** choosing 60-Day gives CTA "Begin your 60-Day Rhythm", plan 712106115453,
   sticky "60-Day Rhythm · Awake + Asleep", receipt with Care Credit and Welcome Kit; choosing Year gives
   "Begin your Karmicare Year", plan 712155431293, sticky "The Karmicare Year · 6 Duos"; back to Try
   once restores the one-time state each time. The Try once card's guarantee and €0 lines show only
   while it is selected (card 160 px selected, 112 px not). A scripted click on 60-Day right after a
   fresh load stays selected 4 s later (no revert by Loop, kc-plan-select or the end CTA).
   `shots/interaction.json` is the last pointer run: the Orca tab mapped mouse coordinates at 1x or 2x
   from one call to the next, so some pointer clicks landed elsewhere (logged with a pointerdown
   listener: no change event, so no selection was made and none was reverted). Every click that reached
   a card switched everything above correctly.
3. **OFF = live** (EN, `preview/compare.py`): every probe field equal (cards, positions, heights, texts,
   CTA, summary, sticky bar, link) at 390 and 1440, Day and Night. Pixels in the buybox area (below the
   80 px header; at 1440 from x 880): 390 Day 0 %, 390 Night 0 %, 1440 Night 0 %, 1440 Day 0.29 %, all
   in one vertical strip at x 880 to 913 on every row from 80 to 800, also in rows without a card, i.e.
   the gallery column's background edge, not the cards.
4. **Awake, Asleep** (`templates/product.json`, no Loop block): with the branch's assets the buybox text
   is identical to live, the Try once container stays hidden, no Loop widget, and the same two
   cross-origin "Script error." entries as on live (`shots/awake-asleep.json`).
5. **Theme Check** `--fail-level error`: exit 0, 19 warnings as on the base commit (`main-product.liquid`
   Liquid complexity 124 before and after).

6. **60-Day badge** (Victor's follow-up, PLAN.md section 4): the preview fills "Plan badges" with
   `712106115453: Most picked` on both OFF and ON pages. ON: "MOST PICKED" at the bottom right of the
   60-Day card only, Day and Night, 390 and 1440, also below the opened description when 60-Day is
   selected (`on-en-390-day-60day-selected.png`, badge row 356 px in a 360 px card, flush with the
   edges like the Year's). OFF: no badge (`probes.json`, off-en-390-day and off-en-1440-day). NL and FR
   show the English text until it is translated. Theme Check exit 0, 19 warnings, complexity 124.

7. **Two-line title and struck €67** (Victor's follow-up, PLAN.md section 4): the preview fills "Title
   line 1" with "Karmicare Duet: Awake & Asleep" and "One-time price struck through" with
   712106115453. ON: H1 in two lines, line 2 in the section titles' second tone, EN/NL/FR from the
   product's own title (`on-*-top.png`); "€59 €67" on the 60-Day card only, one line also in NL
   ("€ 59 € 67" wrapped at 390 px before `white-space: nowrap`), contrast 6.0:1 Day and 7.5:1 Night.
   OFF: title and prices as live (`off-*-top.png`, `off-*.png`). Theme Check exit 0, 19 warnings,
   complexity 124.

## Not tested here (needs a dev theme with a cart, no payment)

- Cart and checkout lines for one time (1 Duo, no selling plan, no kit, no "Subscription Name") and the
  new `Buybox layout` attribute on every path.
- Hotjar `kc_checkout_once` + `kc_layout_card` (needs consent and a real add).
- The theme editor itself: the new "Try once" select on the Loop block and its flip writing
  `templates/product.subscription-item.json`.
- iOS Safari (Chromium only here).

## Harness notes

- Orca screenshots sometimes came back as a half-size frame in the top-left quarter (live 1440 Night,
  twice); a retake after a Day shot painted normally. Compare only shots of the same size and look at
  them.
- `orca mouse` coordinates mapped at 1x or 2x in the same tab between calls; verify with a pointerdown
  listener before trusting a click result.
