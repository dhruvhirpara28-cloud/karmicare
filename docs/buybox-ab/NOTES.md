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

- Switch ON: http://127.0.0.1:9376/on/en/products/karmicare-biorhythmic-oral-care-system
  (also `/on/nl/…`, `/on/fr/…`)
- Switch OFF: http://127.0.0.1:9376/off/en/products/karmicare-biorhythmic-oral-care-system
- Live, untouched, for comparison: http://127.0.0.1:9376/live/en/products/karmicare-biorhythmic-oral-care-system
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

8. **Copy proposals on the preview** (Victor: "pas jouw voorstellen toe op de preview"): variant
   `/copy/en/…` = switch ON plus PLAN.md 4b, EN only, built by `preview/copy_proposals.py`: the two
   plan descriptions replaced in Loop's product JSON (what a Loop admin edit would deliver), the 60-Day
   option text "A new Duo every 60 days", the Year sub-row via `data-kc-renews-year`, and the Year's
   "€59 per Duo, billed once a year" drawn by `preview/copy-overlay.js` (no source in the theme yet).
   Theme code untouched. Shots `copy-en-{390,1440}-{day,night}{,-60day,-year}.png`, with `on-en-*-60day`
   / `-year` for before. Card heights at 390 (closed / open): 60-Day 206 / 545 (was 206 / 567), Year
   315 / 628 (was 249 / 592): the Year gets two sub-row lines and longer chips. The receipt rows under
   the cards still say "Care Credit back in your account" and "Dental Check-up Reward" (block
   settings, not in the proposals).

9. **Whole buybox in the copy variant** (Victor: "de volledige buy box, ook de receipt details & CTA
   knop"): `preview/copy-overlay.js` also rewrites, per selected plan, the receipt (labels, tooltip, a
   "Shipping FREE" row for members, the line under "Total today"), the Try once CTA ("Begin your first
   Duo") and the trust row under the CTA. Shots `{on,copy}-en-{390,1440}-{day,night}-{once,60day,year}-buy.png`
   (on = before, copy = after), framed on the end of the cards, the receipt, the CTA and the trust row.
   Found on the way: in `/on/` with Try once selected the trust row still says "60-day money-back
   guarantee · Gift, pause or cancel · Free shipping" (PLAN.md 4b, must fix before live).
   `preview/below_cards.js` lists the visible buybox below the cards per state.

10. **Alignment and Try once card** (Victor, 24 Nov): struck price before the price ("€67 €59"); the
    radio, plan name and price on one line, measured with `preview/align.js` (canvas font metrics: the
    centre of the name's capitals against the radio's centre and the price's capitals). Before, at
    1440: radio 1.8 px high, €59 0.5 px low next to the struck price; after, at 390 and 1440, on and
    copy: radio ≤ 0.2 px, price 0 px, struck price ≤ 0.3 px. With the card layout only; the link
    layout keeps its radio offset (OFF still equals live). Try once card: "€0.56 / brushing +
    shipping" (the block's Try once shipping text, NL "+ verzending", FR "+ livraison"), no guarantee
    line, the €0 note as a chip like the plan cards' chips. Copy variant receipt for Try once: "€0.56
    per brushing + shipping". Theme Check exit 0, 19 warnings, complexity 124.

11. **Year as a link, badge tab, card sizes, Try once CTA** (Victor, 24 Nov; PLAN.md 4c):
    - `/year/` (EN, NL, FR): Try once and 60-Day as cards, then "Or The Karmicare Year · €354 / year"
      with "+ €70.80 Care Credit + €40 Check-up Reward". `preview/year_check.py`: on load Try once
      selected and no Year card; a click on the link opens the Year card, selects it, CTA "Begin your
      Karmicare Year", receipt with Care Credit, Check-up Reward and Welcome Kit; back to Try once the
      Year card stays. Shots `year-*.png`.
    - `/badge/`: "Most picked" as a light-blue tab on the 60-Day card's top edge (`preview/badge-tab.css`,
      preview only). Shots `badge-*.png`, `-year` with the Year card open next to it.
    - Card parts at 390, Try once selected (`preview/card_parts.js`), plans header to trust row:
      `/on/` 877 px, `/year/` 722 px, `/badge/` 847 px. Per card (total / padding / sub-row / chips /
      badge row): Try once 154/32/22/62/0, 60-Day 206/32/44/62/38 (badge tab: 176, badge 20 on the
      edge), Year 249/32/44/105/38.
    - CTA with Try once selected: Loop block setting "Try once: button text (card on top only)", the
      preview filled with "Try once, purchase now" on every language (Shopify shows the English
      value on /nl and /fr until it is translated).
    Theme Check exit 0, 19 warnings, complexity 124.

12. **Ribbon, promises per plan, `/full/`** (Victor, 24 Nov): `preview/state_check.py` per variant
    (on, year, full), width (390, 1440) and selected plan (Try once, 60-Day, Year, Try once again), in
    `shots/states.json`:
    - Promises: Try once "14-day money-back guarantee" only (theme); 60-Day and Year the block's
      three; in `/full/` the copy proposals on top.
    - Ribbon "Most picked": centre on the 60-Day card's top border 0 px; 1440 px 52 px from the
      title's end, 48 px to the price; 390 px the gap is narrower than the ribbon (-4 / -9 px), it
      stays on the border line above both.
    - Text twice between the plans header and the promises: `/full/` none with Try once or 60-Day
      selected; with the Year card open only the same line on two plans ("€0.49 / brushing", the
      Care Credit chip label). `/on/` and `/year/` show the live duplicates (live Loop texts).
    - `/badge/` (tab idea) is gone, replaced by the ribbon in the theme. Shots `full-*.png`.
    Theme Check exit 0, 19 warnings, complexity 124.

13. **Chips on the selected card only, `/chips/`** (Victor, 24 Nov): `/full/` with the Loop block
    setting "Plan chips: selected card only" on. Closed cards keep name, sub-row and price, and show a
    down chevron under the price (`/ 60 days`, `one-time`). At 390 px with Try once selected the 60-Day
    card goes from 176 to 114 px; with 60-Day selected its chip shows and Try once folds to 100 px with
    the chevron. Shots `chips-en-{390,1440}-{day,night}{,-60day}.png`. OFF still equals live (probes
    equal, 390 px 0 % pixels). Theme Check exit 0, 19 warnings, complexity 124.

14. **Live card texts, smaller slanted strike, Year in a popup or side panel** (Victor, 26 Nov):
    - The plan cards keep Loop's live texts and values, benefit lines included, in every variant
      except `/copy/` (kept as the record of PLAN.md 4b). `/full/` is gone; `/chips/` is now `/year/`
      with chips on the selected card only. The live page was fetched again on 26 Nov (theme
      `karmicare/main`); its `loop-widget.js`, `kc-plan-select.js`, `karmi-add-to-cart.js` and
      `kc-buybox.css` still have the branch base's content (same functions, only minifier changes).
    - Struck "€67": one size smaller (body-md), the line slanted (−12°), on the price's baseline;
      `align.js`: price 0 px at 390 and 1440, the smaller struck price 0.9 / −0.1 px.
    - Loop block "Plan link opens": `/popup/` (popup in the middle over an 8 px blur) and `/panel/`
      (side panel, 440 px on desktop, full width on a phone, the hero animation's landed still,
      Awake in Day and Asleep in Night, above the plan, the button kept in view at the bottom).
      `preview/dialog_check.py` (`shots/dialogs.json`, `popup-*-open.png`, `panel-*-open.png`): the
      dialog shows the Year's live title, price, both chips, all six benefit lines and the three kit
      tiles; "Close" in the page language; Esc and a click on the blur close it; its button "Begin
      your Karmicare Year" chooses the Year and presses the buybox CTA, which calls karmiAddToCart
      with selling plan 712155431293 and the Welcome Kit (recorded, no cart touched).
    - The Welcome Kit tiles are built by one helper for the buybox and the dialog
      (`kcWelcomeKitParts`); the buybox still shows its three clickable tiles in the selected plan.
    Theme Check exit 0, 19 warnings, complexity 124.
15. **`/compact/`** (the lane's preference, 26 Nov): switch ON, three cards with live texts, chips on
    the selected card only. At 390 px with Try once selected, plans header to promises 680 px (today's
    card layout 877, Year as a link 722); cards 154 / 114 / 144 px. Shot `compact-en-390-day.png`.

16. **`/candidate/`, silver badge, no chevrons, no pill twice** (Victor, 27 Nov: "ik ben geneigd om
    voor compact te gaan en de karmicare year als tertiery link die een zijpaneel opent"):
    - `/candidate/` = switch ON, chips on the selected card only, the Year as a link that opens the
      side panel. Shots `candidate-*.png`, `candidate-en-*-open.png` (panel), checks
      `shots/states-candidate.json`, `shots/dialogs-candidate.json`.
    - Chevrons removed (code and CSS). "Most picked" is the "Brushing & Beyond" badge (look and place,
      bottom right of the card, flush with the edge) with a silver gradient shine; the ribbon and its
      positioning code are removed.
    - An opened plan leaves out the benefit line that repeats its Care Credit pill ("€5.90 / €70.80
      Care Credit back on orders"), in the cards and in the panel (5 lines instead of 6 for the Year).
    - Still said twice with 60-Day open (live texts, not pill against list): "Care Credit back in your
      account" in the pill and the receipt; "Gift, pause or cancel" and "60-day money-back guarantee"
      in the list and the promises; "/ 60 days" on the card and in the receipt.
    - Purchase from the panel: karmiAddToCart with plan 712155431293 and the Welcome Kit (recorded).
      OFF equals live at 390 Day and Night (0 % pixels). Theme Check exit 0, 19 warnings, complexity 124.

17. **Side panel layout, promise text, fresh stock** (Victor, 27 Nov): the dialog is a scrolling
    body and a footer with the button (line above, fade under); badges on top above the image; the
    Year's text from "Plan popup / side panel: text per plan" (VOORSTEL in PLAN.md) under its title
    and price; "guaranteed fresh stock" emulated as the Loop admin edit (EN, `/candidate/` only).
    `dialog_check.py candidate`: kit 3 tiles, landed still per mode, first benefit line with
    "guaranteed fresh stock", Esc and blur close, purchase through the buybox CTA with plan
    712155431293 (recorded). Shots `candidate-en-*-open.png`. Theme Check exit 0, 19 warnings,
    complexity 124.

18. **No promises with Try once, tighter closed card, silver ring, page lock** (Victor, 27 Nov;
    `preview/round_check.py`, `shots/round-27nov.json`):
    - With Try once selected the promises row under the CTA is hidden; with a plan its three promises
      and icons are back. The data attribute for the Try once guarantee is removed (no longer read).
    - Compact, closed cards: no gap above the badge; the closed 60-Day card 128 px (was 144).
    - The selected 60-Day card (the one with the silver badge): its border is a silver ring with a
      light band running round (`kc-silver-shine`, 2.8 s), still silver with reduced motion. Shots
      `candidate-en-*-60day-silver.png` (a still cannot show the motion).
    - Side panel: the page behind is locked (html.kc-plan-dialog-open, overflow hidden, scrollbar room
      kept). With a real mouse wheel: without the panel the page scrolls 600 → 1100; with it open,
      the wheel over the blur leaves the page at 600; inside the panel the panel scrolls to its end
      (253 px) and the page stays at 600. Esc releases the lock.
    - The footer line: body text colour at 25 % (the colour scheme's foreground was cream on the cream
      panel), and the fade above it no longer covers it. Shots `candidate-en-*-day-panel-footer.png`.
    Theme Check exit 0, 19 warnings, complexity 124.

19. **Calmer rings, room under the CTA, promise text, bigger kit, glass footer** (Victor, 27 Nov;
    `preview/round2_check.py`, `shots/round2-27nov.json`):
    - One ring rule for the selected card: 60-Day in silver, Try once a light band over its own blue
      border. The band is softer (white at 55 %), crosses in 60 % of a 7 s cycle and rests. The Loop
      container is `overflow: visible` with the card layout, so the cards' shadows are no longer cut.
    - With Try once the promises row is invisible but keeps its room: CTA to "What you'll feel" 100 px
      for Try once and for 60-Day (390 px).
    - The Year's text (VOORSTEL, no heading): "Your dentist sees you once or twice a year. We are
      there day and night, from the moment you leave the chair until you sit back down. So you can
      walk into every check-up ready, and out with peace of mind." The setting takes "ID: text" or
      "ID: heading | text".
    - Panel image: cropped to the kit (x 154-938, y 162-835 of 1080 x 960 in both stills) in a frame
      90 % of the panel's inner width (measured 0.900 at 390 and 1440).
    - Panel footer: glass over the scrolling content (`--kc-mapped-surface-glass-default`, hairline
      `--kc-mapped-border-glass-border`, blur `--kc-shape-blur-md` 20 px), as the sticky bar and the
      professional cards; the fade is gone. Shots `candidate-en-*-panel-top.png`, `-panel-scrolled.png`,
      `candidate-en-*-day-rings-*.png`.
    Theme Check exit 0, 19 warnings, complexity 124.

20. **Product name as live, panel strip, 8 px, Try once quantity** (Victor, 27 Nov):
    - The two-line title code is removed (snippet, settings, CSS, preview emulation); the title block
      is back as on main. History: commit 1f4df7d.
    - 8 px between the struck "€67" and "€59" (`--kc-responsive-spacing-layout-xs`).
    - Side panel: the badge ("Brushing & Beyond") is a strip across the top, full width, bottom corners
      12 px, with the close button in it: 44 x 44, the strip's dark text colour on gold, a focus ring,
      focused on opening, "Close" / "Sluiten" / "Fermer". Shots `candidate-en-390-*-panel-header.png`.
    - Try once quantity (PLAN.md 4d): `preview/qty_check.py`, `shots/quantity.json`, max 4 in
      `/candidate/`: at 3 the card says "Try Once · 3 Duos" €201, Total today €201, the sticky bar
      "Try Once · 3 Duos" and its form 3; the recorded add is one line, quantity 3. With 60-Day
      selected the field is 1 and the add is the plan (quantity 1, kit nested, Subscription Name).
      NL "Eenmalig proberen · 2 duo's", FR "Essayer une fois · 2 duos". Shot
      `candidate-en-390-day-once-quantity-3.png`.
    - The dashes (product description EN/NL/FR, Loop tooltips, receipt tooltip) went to the desk for the
      copy lane (message msg_c12815e2af50).

21. **Stepper in the card's row, panel title** (Victor, 27 Nov), `preview/stepper_check.py`,
    `shots/stepper.json`, at quantity 3:
    - From 750 px the stepper sits on the title line, 8 px before the price (EN and NL title on one
      line at 1440; the price column takes only its own width now). On a phone title, stepper and price
      do not fit one line (288 px for 322), so the stepper sits at the right of the €0 pill's row,
      20 px from the card edge, and the pill takes the rest (EN and NL at 390).
    - Fixed on the way: the stepper was looked up in the title column after it moved, so every Loop
      update added another one. It is looked up in the card row now; one stepper.
    - Side panel: no gold strip. "Brushing & Beyond" is a plain title (h5 size, bold) with the close
      button (44 x 44, focused on opening) on its line; the image starts right under it (60 px from
      the top at 390, 64 at 1440). Shots `candidate-{en,nl}-{390,1440}-day-stepper.png`,
      `candidate-en-*-day-panel-title.png`.
    - `qty_check.py` re-run: Try once x3 adds one line quantity 3, 60-Day adds the plan at 1 with the
      kit. Theme Check exit 0, 19 warnings.

22. **Try once keeps its quantity, panel title bar fixed** (Victor, 27 Nov), `preview/memory_check.py`,
    `shots/memory.json`, EN 390, adds recorded (nothing reaches a cart):
    - At 3, then 60-Day selected: the Try once card still says "Try Once · 3 Duos" €201 (stepper hidden
      with the card unselected), Total today €59. The sticky "Try once" link then adds quantity 1, as it
      shows €67. Try once selected again: stepper 3, Total today €201, the buybox CTA adds quantity 3.
      The chosen quantity sits in the field's `data-kc-chosen`; the field is 1 while a plan is selected.
    - Side panel: the title bar stays at the top while the body scrolls under it (scrollTop 170 at 390,
      193 at 1440, bar at 0), glass as the footer (blur 20 px, 1 px hairline below). Room around the
      close button: 12 px at 390, 16 px at 1440. Shots `candidate-en-*-day-panel-bar-scrolled.png`,
      `candidate-en-390-day-once-kept-*.png`.
    - `qty_check.py` re-run: same adds as result 21. Theme Check exit 0, 19 warnings.

23. **Stepper by the pill everywhere, sticky bar follows the card** (Victor, 27 Nov),
    `preview/sticky_check.py`, `shots/sticky.json`, at quantity 3:
    - Stepper at the right of the €0 pill on every screen (EN, NL at 390 and 1440): same row, 8 px
      after the pill at 390, right edge at the card's padding (20 / 24 px), after the pill in the DOM so
      the tab order follows the screen. Titles on one line. Shots `candidate-{en,nl}-*-day-stepper-pill.png`.
    - Sticky bar, Try once at 3: the closed bar shows "Try Once · 3 Duos" (NL "Eenmalig proberen · 3 duo's",
      a no-break space keeps "3 duo's" together), button text as the buybox's, its form 3.
    - Sticky bar, 60-Day selected: "Not ready for a membership? Try once for €201", and the link buys 3.
      A comparison table's Try once buys 1 (it shows one Duo). `karmi-add-to-cart.js` now takes the
      quantity from a fixed one time's button; the preview serves the lane's copy of it.
    - The buybox's Try once button text is a block setting: one text for every language ("Try once,
      purchase now" on the NL page too, also in the sticky bar now). It needs a locale key from the copy
      lane before the switch goes on.
    - `qty_check.py` re-run: same adds. Theme Check exit 0, 19 warnings.

24. **Real Shopify render and cart, MVP settings** (Victor, 27 Nov: "je mag gerust ook een dev theme test
    aanmaken"), `preview/theme_test.py`, `shots/theme-test.json`:
    - The branch at 91d3eba+ pushed as an **unpublished** theme "buybox-ab test 27 Nov (lane test, delete
      after)", id 191258984829 (`shopify theme push --unpublished`; not the shared development theme).
      Opened with `?preview_theme_id=` in an isolated Orca profile.
    - EN, NL, FR: the test theme renders (Shopify.theme 191258984829, unpublished), no "Liquid error",
      Try once card preselected with the stepper, "Most picked", the Year link, maximum 6, the extras JSON
      with the template's values, the sticky link's quantity attribute. Button "Try once, purchase now"
      in all three (a block setting, translated later).
    - Real adds to the profile's own cart, never to checkout (the theme's redirect pointed at a 404):
      Try once x3 = one line, quantity 3, €201, no plan, no Subscription Name; 60-Day = plan 712106115453
      quantity 1 + three kit lines, "60-Day Supply"; the Year from the side panel = plan 712155431293
      quantity 3, €354 + kit, "Year Supply". Each choice replaced the one before. "Buybox layout: card" on
      all. Cart cleared at the end.
    - Not from this branch: on the test theme the inline `day-night-sun.js` renders empty (the asset itself
      is there on the CDN, 200), so no Day/Night class: the selected card shows Night's accent colours and
      the menu icon is missing. The branch does not touch those files; the live theme has the script.
      DH may want to know for unpublished-theme previews.
    - Preview on the wifi network for Victor's iPhone: `server.py <dir> 9377 0.0.0.0`.

25. **Year panel as a bottom sheet, (i) sheets** (Victor, 27 Nov), `preview/sheet_check.py`, `shots/sheets.json`:
    - Below 750 px the side panel comes up from the bottom (`kc-sheet-in`), full width, 24 px of the
      blurred page above it, 12 px top corners; it slides down on the close button, Esc and a tap on the
      blur (`kcCloseSheet`, 0.25 s, at once with reduced motion). The buy button closes it at once, as before.
      From 750 px the side panel is unchanged (from the right; no sheet).
    - The two (i)s in the panel (Care Credit, Check-up Reward) are buttons there: on a phone each opens a
      small sheet over the panel with the chip's words as the heading and the tooltip text at body size
      (15 px at 390, it was the popover's small size), a handle on top, the panel dimmed behind it. A tap
      outside slides it down; Esc too; focus goes back to the (i). EN and NL checked. The hover popover is
      off in the panel on a phone. A "Close" button for keyboards and screen readers shows only on
      keyboard focus.
    - Only in the Year's side panel for now (Victor: try it there before every (i) on a phone).
    - The tooltip texts come from Loop and still hold dashes (copy lane, msg_c12815e2af50).

26. **Every (i) on a phone, review, full regression** (Victor, 27 Nov: "doortrekken voor alle (i)tjes op
    mobile", 24 px extra at the bottom; then "verifiëren of dit volledig bugvrij is en de code clean"):
    - `assets/kc-info-sheet.js` + `.css`, loaded by `layout/theme.liquid` with the Loop widget (product,
      index, article): every `.info-tip` with a popover is a button on a phone and opens the sheet (pills in
      the plan cards, receipt rows, comparison tables, the Year panel). Bottom padding 20 + 24 px. The
      Year-only code left `loop-widget.js` and `kc-buybox.css`; the side panel's slide-down uses
      `KCSheet.close`. From 750 px nothing changes (the tables' own tap toggle works up to 768 px as before).
    - `preview/sheet_check.py`, `shots/sheets.json`, EN + NL at 390: 6 visible (i)s on the page + 2 in the
      panel, each opens with its words as heading, 15 px text, the page locked, closes on a tap outside
      and on Esc, focus back on its own (i); the panel stays open under it. At 1440: no sheet, the panel
      closes at once.
    - Fixed on the way: a closed sheet's late `close` event could unlock the page or take focus while the
      next one was open (now ignored when open again; the (i) has focus before the sheet opens, so the
      browser gives it back). On desktop the side panel waited 0.4 s before closing (its opening animation
      was taken for a closing one).
    - Code review (`/code-review high`, main...HEAD): fixed the sticky bar using the card-only button text
      in the link layout too, the "Plan badges" help text (still said ribbon), a joined attribute line.
      Open, not code: NL/FR of the three new setting texts (copy lane), Terms for Try once above 1 Duo,
      "Most picked" needs data (legal); kc-gallery.css translate note is merchant-edit's commit 468ce3a.
    - Regression: qty, memory, sticky, year_attr checks as before; switch on Link = live (probe same,
      pixels 0 % at 390 and 1440 Day, 0.007 % 1440 Night); Awake/Asleep same as live (only the live
      cross-origin "Script error." twice). Test theme 191258984829 updated: EN/NL/FR render without Liquid
      errors, real cart Try once x3 / 60-Day / Year from the panel as in result 24, the sheet loads there
      (close label "Close", 4 decorated (i)s, opens). `node --check` on the changed scripts; Theme Check
      exit 0, 19 warnings.

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
