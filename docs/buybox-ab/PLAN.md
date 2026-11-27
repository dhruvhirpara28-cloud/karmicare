# Buybox: Try once as the first card (lane buybox-ab)

Desk run run_32dd5602b983, 24 Nov 2026. Plan and prototype only: nothing lands, merges or goes live
until Victor says so through the desk.

Goal (Victor): on the Duo PDP the buybox shows **Try once first**, as a real card on top and
**preselected**, then the 60-Day rhythm, then the Karmicare Year, for every visitor. One theme-editor
switch flips between today's layout and the new one, so the before/after read (same Meta budget, no
A/B split, no per-variant URLs) can run in both directions.

## 0. What I checked (desk findings, verified)

| Desk finding | Verified in the code / live |
|---|---|
| Loop renders its own one-time option on top | Yes. `#loop-one-time-purchase-option-at-top` in `snippets/loop-widget-standard.liquid` l.102, radio `#loop-one-time-purchase-<product id>`, `data-id="loop-one-time-purchase"`, same radio group (`name="loop_purchase_option"`) as the plan cards. It sits before the plan groups in the fieldset, so "on top" needs no move. |
| Our code hides it and shows our own link | Yes. `injectOrUpdateKcTryOnceLink` (`assets/loop-widget.js` l.2826) sets `display: none !important` on the top card; the link is `#kc-try-once-container-<id>` in the `price` block of `sections/main-product.liquid` l.150, and its button goes to `KCPlanSelect.tryOnce` (one time, straight to checkout). |
| CSS already styles the one-time option like the cards | Partly. `snippets/loop-widget.css.liquid` gives it the same padding, radio and checked border/label colour, but a different box (`--surface-2`, 1 px `--border`) and a lighter label (body-xl 600, no `h5`). The card needs the plan card box, label and price styles. |
| Default selection | Yes: `default_to_subscription` -> `data-default-to-subscription` -> `applyDefaultSelectionBasedOnLoopSettings` (l.1293), theme OR Loop admin `byDefaultChooseSubscriptionOption`. A second check with the same rule sits in the bundle path (l.3204). On top of Loop, `KCPlanSelect.startOnSubscription` (`assets/kc-plan-select.js` l.1246) moves a one-time selection to the first public plan 800 ms after Loop settles when the plan config says `defaultToSubscription`. Both must stand down for "preselected". **Correction:** the `true` lives in `templates/product.subscription-item.json` (the Duo template, block `loop_subscriptions_WEk4XJ`), not in `templates/product.json`, which has no Loop block. |
| Sticky bar reads the one-time radio | Yes, `snippets/sticky-cart-block.liquid` l.320 to 343: a checked `loop-one-time-purchase` radio gives state `once` (title "Try Once · 1 Duo", CTA "Try once", 14-day guarantee, shipping at checkout). Nothing to change. |
| Hotjar on the normal buy button with one time selected | Yes, it fires. Buybox CTA (`snippets/custom-button-script.liquid`) -> `karmiAddToCart` reads the checked radio, `isLoopOneTime` -> no selling plan -> `KCPlanSelect.replaceChoice(productId, '', …)` -> `trackCheckout('')` -> `kc_checkout` + `kc_checkout_once`. Same for the sticky CTA, the compare tables, the end CTA and Loop's own add (`shopifyAddToCartByLoopWidget`, l.3973). |
| Card labels per language (80a9736) | Yes: `kcLabelText` reads `kc.receipt.*` from data attributes on the pricing summary (`snippets/kc-receipt-labels.liquid`). |

Read-only check of Loop's widget settings (public JSON `d217z8zw4dqir.cloudfront.net/karmicares.myshopify.com.json`,
24 Nov): `byDefaultChooseSubscriptionOption = false`, `displayOneTimePurchaseOptionAtBottom = false`,
one-time label "One Time Purchase", one-time button text "Add to cart" (that one goes to Dawn's hidden
submit button, not our CTA).

Products (live, 24 Nov): the **Duo** (`karmicare-biorhythmic-oral-care-system`, template
`product.subscription-item`) has the Loop block and the plan cards. **Awake** and **Asleep**
(`awake-morning-toothpaste-2-0`, `asleep-evening-toothpaste-2-0`) use `templates/product.json`: no Loop
block, no plan cards, one-time only. Their page has an empty, hidden `#kc-try-once-container` from the
price block and nothing else of this feature.

## 1. Native or custom card: native (recommendation)

**Use Loop's native one-time option, restyled as the third card (shown first).** Reasons:

| Point | Native one-time option | Custom card like the plan cards |
|---|---|---|
| Cart line | Already right: `karmiAddToCart` sees the checked `loop-one-time-purchase` radio, sends no `selling_plan`, keeps the form quantity (1 Duo). | A radio outside Loop's group: every buy path (`karmi-add-to-cart.js`, `kc-plan-select.js`, sticky bar, Loop's add) reads Loop's radio, so each would need a second rule. |
| Price | Loop keeps `#loop-price-one-time` on the variant price on every variant change. | Own price code. |
| Button label | `updateKcPlanButtonLabel(productId, isOneTime)` already knows "one time". | Own state. |
| Sticky bar | Reads it today (state `once`). | Would show nothing or the last plan. |
| Hotjar | `kc_checkout_once` on every path (section 0). | Needs its own call per path. |
| Care Credit "Subscription Name" | `syncCartSubscriptionName` clears it for a one-time cart; nothing else to do. | Same, only if every path learns the new radio. |
| Welcome Kit nesting | Added only for a subscription; one time adds no kit lines. | Same risk as the cart line. |
| Loop updates | Loop owns the element; a widget re-save in Loop admin regenerates `loop-widget-standard.liquid` but keeps this element (it is in Loop's own template). We do not edit that file. | Independent of Loop, but duplicates Loop's state. |
| NL/FR labels | Loop's label is replaced by our theme texts (existing `kc.sticky_cart.*` / `kc.receipt.*` keys, NL/FR already translated). | Same keys. |
| Day and Night | Same tokens as the plan cards (`--kc-mapped-*`); the Night radio rule exists already. | Same. |
| 390 px | Same flex row as a plan card. | Same. |

One source of truth for "what is selected" stays Loop's radio group. The cost of native: our card text
must be (re)written after Loop sets its own label (`addLoopOneTimePurchaseOptionLabelText` runs on every
`loopInit`), which our existing per-update hook (`injectOrUpdateKcTryOnceLink`, called from
`updatePriceInParentElementsLoop`) already does for the link.

## 2. Files and functions

Changed (switch OFF keeps today's behaviour in each):

| File | Change |
|---|---|
| `sections/main-product.liquid` | Loop block schema: new `select` setting `try_once_layout`. The `price` block's `#kc-try-once-container-<id>` gets `data-kc-once-layout` plus the card texts as data attributes (title, details, CTA, from existing locale keys and the existing block settings). The `kc-plan-config` render also passes `try_once_layout`. |
| `snippets/kc-plan-config.liquid` | `defaultToSubscription` is false when `try_once_layout` is `card` (the `if` sits here so `main-product.liquid` keeps its Liquid complexity of 124). |
| `assets/loop-widget.js` | `kcOnceCard(productId)` helper (reads the attribute above). `applyDefaultSelectionBasedOnLoopSettings` and the bundle default (l.3204): card layout selects one time, whatever the theme or Loop admin "default to subscription" says. `injectOrUpdateKcTryOnceLink`: card layout shows the top option as a card (class `kc-once-card` on the buybox container, plan card structure: label + sub-row, price + "one-time", details when selected), hides the link; link layout as today, plus it now also hides a one-time option Loop moved to the bottom. `updateKcPricingSummary`: keeps the link hidden in card layout. `updateKcPlanButtonLabel`: buybox CTA label for one time in card layout. |
| `assets/kc-buybox.css` | New rules scoped to `.kc-once-card`, next to the plan card rules they copy (that is where the plan cards get their look, not the Loop CSS): plan card box, radio, type, selected state, details shown only when selected. Same specificity as the plan card rules, so the Day rules in `section-main-product.css` apply to both alike. Plus the selected one-time price colour (accent in Night, heading colour in Day, as the plan cards). |
| `assets/kc-plan-select.js` | `syncCartSubscriptionName` also keeps the cart attribute `Buybox layout` (section 5) on the page's layout; `trackCheckout` adds `kc_layout_link` / `kc_layout_card`. |

Untouched: `snippets/loop-widget-standard.liquid` (Loop-generated; not needed), `snippets/loop-widget.css.liquid`, `assets/loop-widget.css`,
`assets/karmi-add-to-cart.js`, `snippets/sticky-cart-block.liquid`, `snippets/custom-button-script.liquid`,
`sections/featured-product.liquid` (end CTA keeps its fixed 60-Day offer), all templates,
`config/settings_data.json`, `assets/kc-tokens.css`, every locale file.

## 3. The switch and its default

Loop Subscriptions block (main product section), new setting:

- **Try once** (`try_once_layout`, select)
  - `link`: "Link under the cards" (**default**, today's layout)
  - `card`: "Card on top, preselected"

Merging changes nothing: no template sets the value, so every product page renders `link` until Victor
picks `card` in the theme editor. The flip is Victor's admin action and writes
`templates/product.subscription-item.json` (block `loop_subscriptions_WEk4XJ`, `"try_once_layout": "card"`)
in the live theme; DH's next `main` sync should carry that line back into the repo, or the next deploy
from `main` resets it to `link`.

Which products follow it: every product on `product.subscription-item` with plan cards, so the **Duo**.
**Awake** and **Asleep** (`product.json`, no Loop block) show no plan cards and sell one time already;
the setting does not reach them. If they get plan cards later, their template gets its own setting.

In `card`, "Default to first subscription" is ignored for this widget (the card is preselected by
definition); back on `link` it works as before.

## 4. Copy for the Try once card

Only existing texts, EN shown, NL/FR already in the locales or the block settings:

| Card line | Source | EN |
|---|---|---|
| Title | `kc.sticky_cart.title_once_html` | Try Once · 1 Duo |
| Price, right | Loop's one-time price + `kc.receipt.one_time` | €67 / one-time |
| Sub-row | `kc.receipt.per_brushing` (price / 120 brushings, as the summary) + block setting `try_once_shipping` | €0.56 / brushing + shipping |
| Chip, always shown, as the plan cards' Care Credit chips | block setting `try_once_note` | €0 Care Credit · €0 Dental Check-up Reward |

Victor (24 Nov): "+ shipping" right after the per-brushing price instead of a sentence of its own, no
guarantee line on the Try once card, the €0 sentence as a chip for consistency with the other cards.
| Buybox CTA with Try once selected | Loop block setting "Try once: button text (card on top only)", blank = `kc.sticky_cart.cta_once_html` | Try once, purchase now (Victor, 24 Nov) |

Open copy point, **VOORSTEL**: the CTA rule is "Begin your …", and "Try once" is the sticky bar's
existing CTA. If Victor wants the rule here too: EN "Begin your first Duo" (VOORSTEL), NL/FR through the
source-copy lane via the desk. Today's fallback "Begin Now" (`custom_button_text`) is not used in card
layout.

**60-Day badge (Victor, 24 Nov, in the lane chat):** "bij de 60 day mag er ook een badge onder aan
met 'most picked' of een equivalent ervan". New Loop block setting **Plan badges (card on top only)**,
one line per plan, `712106115453: Most picked`, matched by selling plan ID (as the per-plan CTA
labels). It shows only with "Try once: card on top", at the bottom right of the card in the look of the
Year's "Brushing & Beyond" (`.kc-testimonial-button`), so one flip still turns the whole new layout on
or off. No template sets it: Victor fills it in the editor with the flip. Two open points:
- **Claim:** "Most picked" says most buyers choose the 60-Day plan. Under EU consumer law that has to
  be true and provable (order data). If it is not, or not yet, a wording without a popularity claim
  is safer (VOORSTEL, to choose with Victor).
- **NL/FR:** the text is a block setting value, so NL/FR come through Translate & Adapt like "Brushing
  & Beyond"; until then /nl and /fr show the English text. Wording via the source-copy lane.

**Two-line title and struck €67 (Victor, 24 Nov, lane chat):**
- Title block, new settings "Title line 1 (Try once card on top only)" and "Line 2: leave out at the
  start of the product title" (default "Awake & Asleep"), in `snippets/kc-product-title.liquid`. With the
  card layout and line 1 filled: one H1 with line 1 "Karmicare Duet: Awake & Asleep" and line 2 the
  product title in the page language minus "Awake & Asleep" ("Fluoride-Free Nano-Hydroxyapatite
  Toothpaste, Day & Night System"; NL and FR from the product's own translation) in
  `--kc-heading-second-tone`, the second tone of the section titles. The SEO keywords stay in the H1;
  the product title in Shopify does not change. Line 1 needs NL/FR through Translate & Adapt.
  Open point: the title says "Duet", every card, the sticky bar and the receipt say "Duo".
- Loop block, new setting "One-time price struck through (card on top only)", plan IDs
  (`712106115453`): "~~€67~~ €59", the one-time price of the plan's Duos (1 for the 60-Day) before the
  plan price (Victor, 24 Nov), body colour at 70 % (contrast 6.0:1 Day, 7.5:1 Night), hidden from screen readers as it
  repeats the Try once price. Open point: a struck price reads as a price reduction. €67 is today's
  one-time price of the same Duo, shown in the card above, so it is a comparison of two current
  offers, not an earlier price; the Terms' Omnibus clause (lowest price of the last 30 days) is about
  reductions. Worth a yes from whoever checks the legal pages before it goes live.

## 4b. Copy proposals for the membership cards (VOORSTEL, EN only)

Goal (Victor): make the plans foolproof. What a first-time visitor has to understand in five seconds:
what arrives and when, what it costs and when it is charged, what Care Credit is, and that they can
stop. Every line below comes from text already on the site or in the Terms; no new claims or numbers
(the "€59 per Duo" is the Year price divided by its 6 Duos).

| Where | Today | VOORSTEL | Why | Lives in |
|---|---|---|---|---|
| 60-Day sub-row | Renews every 60 days | A new Duo every 60 days | Says what arrives; "renews" is subscription jargon | theme (loop-widget.js, kc.receipt key) |
| 60-Day chip | €5.90 Care Credit back in your account | €5.90 Care Credit back, to spend on more care | Says what Care Credit is for (sticky bar: "spend it on more care") | Loop plan description |
| 60-Day list | Awake + Asleep duo one complete 60-day cycle | 1 Duo, Awake + Asleep, for 60 days | Shorter, same fact | Loop plan description |
| 60-Day list | Gift, pause or cancel anytime | Pause or stop anytime, no lock-in | "No lock-in" is the Terms' own promise | Loop plan description |
| 60-Day list | (none) | An email 5 days before every renewal | Takes away the fear of a forgotten charge (Terms, "Renewal reminder") | Loop plan description |
| 60-Day list | Inflation-proof member price | Your price stays the same while you stay | Plain words for Terms "member price protection" | Loop plan description |
| 60-Day list | €5.90 Care Credit back on orders | (drop) | Repeats the chip | Loop plan description |
| 60-Day list | Free Welcome Kit (on first order) | Welcome Kit with your first order: two toothbrushes + floss, free | Says what is in it (sticky bar text) | Loop plan description |
| Year sub-row | Renews every year | 6 Duos a year: 3 now, 3 in month 6 | What arrives (Loop's own option text); Victor removed the deliveries line on 16 Oct, so his call | theme (loop-widget.js) |
| Year price | €354 / year | €354 / year, billed once (€59 per Duo) | Makes the year comparable with the 60-Day | theme |
| Year chip | €40 Dental Check-up Reward | €40 Care Credit after a dental check-up from month 6 | The tooltip text, without needing the tooltip | Loop plan description |
| Year list | (none) | An email 30 and 7 days before your renewal | Same reassurance (Terms, "Renewal reminder") | Loop plan description |
| Tooltips | "… Care Credit — in euros …", "20% Return on Care — 2× the bi-monthly rate —" | No em dashes, no "Return on Care" next to "Care Credit": one name for one thing | Brand style; two names for one thing confuse | Loop plan description |
| Everywhere | Duo / duo / Duet | One spelling: Duo | Consistency with the new title | all |

**Below the cards (Victor: "de volledige buy box, ook de receipt details & CTA knop"):** the
receipt says what you pay today, when you pay next and what comes back; the CTA says what starts; the
trust row says what protects you, per plan.

| Where | Today | VOORSTEL | Why | Lives in |
|---|---|---|---|---|
| Receipt, Try once | "€0.56 per brushing · no Care Credit" under "Total today €67" | "Shipping calculated at checkout" | €67 is not all you pay; per brushing and €0 Care Credit are already on the card | kc.receipt.one_time_note |
| Receipt, members | "Care Credit back in your account" | "Care Credit back, to spend on more care" | Same words as the card chip | Loop block setting |
| Receipt, Year | "Dental Check-up Reward" | "After a dental check-up from month 6" | Says when it comes, as the chip | Loop block setting |
| Receipt, members | "Welcome Kit on first order (value €21) FREE" | "Welcome Kit with your first order (€21 value) FREE" | Same words as the card list | Loop block setting |
| Receipt, members | (none) | New row "Shipping FREE" | Try once pays shipping, members do not; now the difference shows | theme (new row, kc key) |
| Receipt, 60-Day | "Billed every 60 days" + "/ 60 days" | "Then €59 every 60 days. Pause or stop anytime." | Says the next charge and the way out; drops the double interval | kc.receipt.billed_days |
| Receipt, Year | "Billed yearly" + "/ year" | "Then €354 once a year. Stop anytime before your renewal." | Same, from the sticky bar's "stop anytime before renewal" | kc.receipt.billed_year |
| Receipt tooltip | "Care Credit is Return on Care in euros — spendable on …" | "Care Credit is Karmicare credit in euros, to spend on member products and accessories. It lands in your account with your plan, so caring for your teeth pays you back." | No em dash, one name for one thing | Loop block setting |
| CTA, Try once | "Try once" | "Try once, purchase now" (Victor, 24 Nov; replaces my "Begin your first Duo") | Says that this button buys at once | Loop block setting "Try once: button text" |
| CTA, 60-Day / Year | "Begin your 60-Day Rhythm" / "Begin your Karmicare Year" | unchanged | Already clear | buy buttons block |
| Trust row, Try once | "60-day money-back guarantee · Gift, pause or cancel · Free shipping" | "14-day money-back guarantee · One Duo, no renewal" | **Today's row is wrong for Try once** (see below) | theme, per plan |
| Trust row, 60-Day | "60-day money-back guarantee · Gift, pause or cancel · Free shipping" | "60-day money-back guarantee · Pause or stop anytime · Free shipping" | Same words as the card list | icon with text block |
| Trust row, Year | same as 60-Day | "60-day money-back guarantee · Stop anytime before renewal · Free shipping" | The Year renews once a year | theme, per plan |

**Must fix before the card layout goes live, copy or not:** the trust row under the CTA is one fixed
block ("60-day money-back guarantee · Gift, pause or cancel · Free shipping"). It was only ever seen
with a membership selected, because Try once could not be selected in the buybox. With the Try once
card preselected it now tells a Try once buyer about a 60-day guarantee (Try once has 14 days), about
pausing (there is nothing to pause) and free shipping (Try once pays shipping). The `/on/` prototype
shows exactly that (`shots/on-en-390-day-once-buy.png`). Fix: the row follows the selected plan, from
existing texts (kc.sticky_cart.guarantee_once_html, …), in assets/loop-widget.js with the card layout.
The pause icon next to "One Duo, no renewal" would need another icon.

Loop plan descriptions are Loop admin texts with their own Loop Multilingual copies per language, so
they change in Loop admin (Victor or a lane with that go), never from the theme. The theme lines can
go in this lane after Victor's OK; NL/FR of everything go through source-copy via the desk.

The summary box under the cards already has a one-time state ("Total today €67 one-time", "€0.56 per
brushing · no Care Credit", no rewards rows). No other new text.

## 4c. Badges, card size and the Year as a link (Victor, 24 Nov)

**Two gold badges clash.** Built (Victor, 27 Nov, after a light-blue ribbon on the top edge on 24
Nov): "Most picked" is the Year's "Brushing & Beyond" badge, same look and place (bottom right of the
card, flush with the edge), with a silver gradient shine instead of gold. Same setting "Plan badges".

**Candidate (Victor, 27 Nov):** compact (chips on the selected card only, no chevrons) with the Year
as a link that opens the side panel: `/candidate/`. An opened plan leaves out the benefit line that
repeats its Care Credit pill.

**Side panel, 27 Nov (Victor):** badges ("Brushing & Beyond") on top above the image; the button in a
footer fixed at the bottom, a line above it and the content fading out under it; under the Year's
title and price the block's text for the plan (new setting "Plan popup / side panel: text per plan").
VOORSTEL (EN, from Victor's brief; NL/FR through source-copy):

> Your dentist sees you once or twice a year. We are there day and night, from the moment you leave
> the chair until you sit back down. So you can walk into every check-up ready, and out with peace of
> mind.

(Second version, 27 Nov: the customer's benefit, "We are there day and night", no heading above it.)

"6 duos a year (3 now, 3 in month 6), guaranteed fresh stock": the line is the Year's plan description
in Loop admin. That edit is not the theme's: it goes live at once for every visitor (today's layout
too) and needs its NL/FR copies in Loop Multilingual. `/candidate/` shows it as that edit would (EN).
"Guaranteed fresh stock" is a promise; it has to hold for the second delivery in month 6.

**Promises under the CTA follow the plan** (Victor, 24 Nov), in the theme with the card layout
(`kcUpdatePromises`): Try once shows only "14-day money-back guarantee"
(kc.sticky_cart.guarantee_once_html); pause and free shipping go. A plan shows the block's own three.

**Nothing said twice.** The previews are built from the live page each time; the Loop admin texts
(plan lists) are the live ones in `/on/` and `/year/`, so the live duplicates show there (guarantee
and pause in the list and in the promises, Care Credit in the chip and the receipt). `/copy/` and
`/full/` apply PLAN.md 4b without them: the lists leave out guarantee and pause / stop (the promises
hold them per plan), the receipt uses short labels ("Care Credit back", "Check-up Reward", "Welcome
Kit (€21 value)"), no shipping row (the promises say free shipping), the line under "Total today" is
"Then €59 every 60 days" / "Then €354 once a year" / for Try once "+ shipping" without "one-time".
`preview/state_check.py` finds no line twice in `/full/` with Try once or 60-Day selected.

**The options are large.** Measured at 390 px (NOTES.md result 11). VOORSTEL, most effect first:
1. The Year as a link under the cards (built, below): the whole Year card goes until it is chosen.
2. Chips only on the selected card (built, Victor 24 Nov: Loop block setting "Plan chips: selected
   card only"): closed cards show name, sub-row and price, plus a down chevron under the price as a
   sign there is more; Care Credit and Check-up chips appear when the card is chosen. Preview `/chips/`.
3. One sub-row line: "€0.49 / brushing · every 60 days" instead of two lines.
4. The badge as a tab on the edge (above) instead of a row at the bottom.
5. Card padding at 390 from the "comfortable / lg" spacing to "md".

**Year as a link (built):** Loop block setting "Plans as a link under the cards (card on top only)",
plan IDs (`712155431293`). With the card layout the plan's card stays out and a tertiary link follows
the cards in the old Try once link's look: "Or The Karmicare Year · €354 / year", under it "+ €70.80
Care Credit + €40 Check-up Reward" (the sticky bar's text, all three languages). A click opens the Year
card, selects it, and the receipt and CTA follow; once opened it stays a card on that page view (no
jumping back). Chosen another way (compare table, sticky bar) it opens too. Preview `/year/` in EN, NL
and FR. Open point: the link could also go straight to checkout as the old Try once link did; for a
€354 plan I kept the receipt in between.

**Plan cards stay live (Victor, 26 Nov):** "ik wil zoiezo de tekst en waarden zelfde zoals live in de
plan kaarten, ook de bullets benefits lijnen". The copy proposals of 4b stay a record (`/copy/`) and are
not part of the candidate versions.

**The Year link in a popup or a side panel (built, Victor 26 Nov):** Loop block setting "Plan link opens
(card on top only)": its card (default), a popup in the middle of the screen over a soft blur, or a side
panel with the landed still of the kit (the hero animation's own still, Day and Night) above the plan.
Inside is the Year card itself (live texts, prices, chips, benefit lines, kit tiles); its button is the
buybox CTA for the Year, which chooses the Year and buys through the buybox's own path.

## 4d. Try once quantity, and what still has to change (Victor, 27 Nov)

**Built.** Loop block setting "Try once: maximum quantity (card on top only)", 1 to 6, default 1 (no
control, as before). Above 1, a − / + stepper on the Try once card while it is selected. The quantity
lives in a hidden `quantity` field of the buybox form. A stepper over a dropdown: one tap per Duo,
compact on a phone, and the number stays in view next to the price.

What follows the quantity, verified in `/candidate/` with max 4 (`preview/qty_check.py`,
`shots/quantity.json`); the add to cart is recorded, nothing reaches a cart:

| Place | What it does | Verified |
|---|---|---|
| Try once card | Title "Try Once · 3 Duos" (NL "Eenmalig proberen · 3 duo's", FR "Essayer une fois · 3 duos", built from the existing "1 Duo" and "6 Duos" titles), price €201, per brushing stays €0.56 | yes |
| Receipt | "Total today €201", per brushing per Duo | yes |
| Sticky bar | Title "Try Once · 3 Duos" also in the closed bar, its button text as the buybox's ("Try once, purchase now"), its own form buys 3 | yes |
| Buy (buybox CTA → karmiAddToCart → replaceChoice) | One line, quantity 3, no selling plan, no kit, no Subscription Name | yes |
| 60-Day / Year selected | The field goes back to 1; the plan adds its own Duos per delivery with the kit and Subscription Name. The Try once card keeps showing the chosen quantity ("3 Duos", €201), and selecting it again puts the field back at 3 (Victor, 27 Nov; `preview/memory_check.py`) | yes |
| Sticky "Try once for …" link (a plan selected) | Follows the card: "Try once for €201" at 3, and buys 3 (`tryOnce` passes the quantity its button carries) | yes (`preview/sticky_check.py`) |
| Comparison tables' Try once | Show one Duo and buy one, whatever the buybox's quantity | yes |

**Still to change or decide, so it keeps working:**

| # | Where | What | Who |
|---|---|---|---|
| 1 | Terms (legal) | The Terms say "Try Once is a single duo without renewal" and the 14-day guarantee is for "the duo". More Duos per Try once order needs those clauses changed (guarantee per order or per Duo, "one money-back guarantee per customer"). Victor set the maximum to 6 for the MVP (27 Nov, 4f): the Terms change has to be live before or with it. | legal lane via desk, Victor |
| 2 | Shopify admin, shipping | Try once pays shipping by zone; check that the rates still fit 2 to 4 Duos (weight or price tiers). Read only from here. | Victor |
| 3 | Shopify admin, inventory | Above the Duo's stock Shopify refuses the add; the buybox shows Shopify's message and keeps the earlier cart. Set the maximum below normal stock. | Victor |
| 4 | Loop, nothing to change | One-time lines are not Loop subscriptions; Loop Loyalty gives no Care Credit on them; the Welcome Kit and Subscription Name stay on plans only (verified). | none |
| 5 | Loop widget updates | Loop writes its unit price into the Try once price after every update; the theme writes the total right after it (`setTimeout 0`). A Loop update of `loop-widget.js` must keep that order; retest the price after any Loop update. | lane, at Loop updates |
| 6 | Loop's own add path | `shopifyAddToCartByLoopWidget` (Loop's preset bundle event) takes the form; with a plan selected the field is 1, so a plan can never be multiplied by a Try once quantity. | none (covered) |
| 7 | Express checkout | Off on the Duo template. If it is turned on, Shopify's button buys the form, quantity included, only while Try once is selected. | decide if turned on |
| 8 | Copy | No new text: titles from existing keys, the control's labels from Dawn ("Quantity", "Decrease / Increase quantity for …", translated). | none |
| 9 | Tracking | Hotjar `kc_checkout_once` and the "Buybox layout" attribute stay as they are; the quantity is in the order line. | none |

**Everything still open before this goes live (all decisions, nothing pushed):**

| Area | Item |
|---|---|
| Theme settings | In git since 27 Nov (4f): `templates/product.subscription-item.json` holds the MVP values, maximum 6. |
| Loop admin (Victor or a lane with that go) | Year description "6 duos a year (3 now, 3 in month 6), guaranteed fresh stock" + Loop Multilingual NL/FR (goes live at once for everyone); the dashes in the Care Credit tooltips (copy lane). |
| Copy lane via desk | NL/FR: the promise text, "Try once, purchase now", "Most picked"; the dashes (product description, tooltips), sent 27 Nov. |
| Legal | Struck "€67" next to "€59" (two current offers, not a reduction); "Most picked" needs order data behind it; "guaranteed fresh stock" is a promise for the month 6 delivery; Try once quantity vs the Terms (#1). |
| Test on a dev theme with a cart, no payment | One time 1 and 3 Duos, 60-Day, Year from the panel: cart lines, kit nested, Subscription Name, "Buybox layout" attribute, Hotjar events; NL and FR; iOS Safari. |

## 4e. Quantities and people (VOORSTEL, nothing built)

**Victor's direction (27 Nov):** with Try once people think in amounts, with a plan in people. The Year is
**one person per checkout** in this phase: a second person checks out again, separately, so each Year is
its own membership and the €40 Dental Check-up Reward lands on the right person.

One Duo is 120 brushings: one person, twice a day, 60 days (the 60-Day card's own "one complete 60-day
cycle"). So a person on a plan is one Duo per 60 days, and a Year is 6 Duos (3 now, 3 in month 6).

### What each card counts, and what it buys

| People / Duos | Try once (counts Duos, built) | 60-Day Rhythm (counts people, proposal) | The Karmicare Year (no count) |
|---|---|---|---|
| 1 | 1 Duo, €67 | 1 Duo / 60 days, €59 | 1 membership, 6 Duos, €354 / year |
| 2 | 2 Duos, €134 | 2 Duos / 60 days, €118 | a second checkout |
| 3 | 3 Duos, €201 | 3 Duos / 60 days, €177 | a third checkout |
| 4 (max) | 4 Duos, €268 | 4 Duos / 60 days, €236 | a fourth checkout |
| Per brushing | €0.56 | €0.49 | €0.49 |
| Care Credit | none | €5.90 per person | €70.80 per membership |
| Check-up Reward | none | none | €40 per membership |

### The Year: one per checkout, already enforced

Nothing to build for this. The buybox and the side panel buy one Year. A new choice replaces the earlier
one in the cart (`assets/kc-plan-select.js` replaceChoice), and the cart locks a plan line's quantity
(`kc_quantity_locked` in `sections/main-cart-items.liquid` and `snippets/cart-drawer.liquid`). So a cart
never holds two Years; a second person is a second order.

What a second Year checkout by the same customer means today:

| What | Today | Who |
|---|---|---|
| Welcome Kit | **One per person (Victor, 27 Nov).** Today it is withheld for a logged-in customer tagged `FREE WELCOME KIT RECEIVED` (`snippets/kc-plan-config.liquid`), so a second Year bought from the same account brings no kit; as a guest, or with the second person's own email, it does. Simplest fit with "per person" and no build: the second person checks out with their own email (kit, Care Credit and reward then all land with them). A kit per membership on one account would need a different rule than the customer tag. | Victor |
| €40 Check-up Reward | Per membership: both memberships sit under the buyer's account, so the claim must say which membership (person) it is for. | Victor, legal lane |
| Care Credit | Loop Loyalty credits the account that bought: both memberships' credit lands with the buyer. | Victor (Loop admin, read) |
| Copy | Nothing on the page says a Year is for one person. If that needs saying ("per person", "for a second person, check out again"), the copy lane writes it. | copy lane via desk |

### 60-Day: a people count (proposal)

- **Where:** on the selected 60-Day card, at the right of its pill, where the Try once stepper is. The same
  stepper with a person icon before the number (Lucide "user", the icon set the sticky bar already uses),
  so a count of people never reads as a count of Duos.
- **The card follows the count:** "60-Day Rhythm · 2 people", €118 / 60 days, per brushing unchanged, the
  Care Credit pill x 2. Receipt and sticky bar follow, as they do for Try once.
- **In the cart:** 1 line, the 60-Day plan, quantity N; kit lines quantity N, nested. One subscription for
  the household: one parcel, one skip/pause/cancel. One person cannot move to the Year on their own later.
- **Next to a Year of one person:** "2 people €118" on the 60-Day card and "€354" on the Year (one
  person) compare unevenly. Either the Year says it is per person (copy), or the 60-Day also stays at one
  person in this phase and households check out per person there too. Recommendation: the latter until
  the copy exists; it keeps every plan "one person, one membership" and needs no new rules.

Before the 60-Day count is built:

| Area | What | Who |
|---|---|---|
| Care Credit (Loop Loyalty) | A percentage of the amount (Victor, 27 Nov), so it follows N; to be read in Loop admin: on which amount, and none on one-time orders. | lane, Loop admin read |
| Welcome Kit | One per person (Victor, 27 Nov): N kits for N people (N x €21 value). | decided |
| Terms | Plan per household, guarantee per subscription; Try once more than one Duo (4d #1). | legal lane |
| Shipping, stock | Free plan shipping with N Duos per parcel. | Victor |
| Copy | "person / people", "persoon / personen", "personne / personnes", "Number of people": none exists in EN/NL/FR. Blocked until the copy lane writes them (AGENTS.md §3). | copy lane via desk |
| Test | The count is a new variable: its own A/B arm, after this switch has run. | Victor |

Theme work then: `assets/loop-widget.js` (control on the 60-Day card, price and pill x N),
`assets/kc-plan-select.js` (quantityFor x N for the 60-Day, kit lines x N), the sticky bar, the receipt,
Hotjar (people as a property).

## 4f. MVP (Victor, 27 Nov)

**In:** the card layout as in `/candidate/`: Try once first and preselected, with its quantity (several Duos
in one order); 60-Day with "Most picked" and the struck "€67"; the Year as a link that opens the side panel
(promise text, kit image, glass title bar and footer); chips on the selected card only. **Later:** more
people on the 60-Day (4e). **Not in this phase:** a Year for more than one person in one checkout.

Loop block settings for it (theme editor, Duo template), the values `/candidate/` runs on:

| Setting | Value |
|---|---|
| Try once | Card on top |
| Try once: maximum quantity | 6 (Victor, 27 Nov) |
| Try once: button text | Try once, purchase now |
| Plan badges | `712106115453: Most picked` |
| One-time price struck through | `712106115453` |
| Plans as a link under the cards | `712155431293` |
| Plan link opens | Side panel |
| Plan popup / side panel: text per plan | `712155431293: Your dentist sees you once or twice a year. …` (the promise, 4c) |
| Plan chips: selected card only | on |

**Maximum quantity.** No hard reason for 4: it was the preview's value. The setting goes to 6, the code caps
it there. What limits it in practice: stock (above it Shopify refuses the add), shipping rates for a heavier
parcel, and the Terms (4d #1). 6 is a Year's worth of Duos: at 6, Try once is €402 against €354 for the Year,
so the plan stays the visibly better choice.

**Before it goes live:**

| Item | Who |
|---|---|
| Terms: Try once for more than one Duo (4d #1). **Victor, 27 Nov: the maximum stays 6, the Terms are updated after launch** (not a release gate) | legal lane via desk, after launch |
| NL/FR of the three new setting texts (button, badge, panel text). They are block settings like "+ shipping" and the €0 note, which are already translated on /nl and /fr (Translate & Adapt); until then those pages show the English values. Translations keep the plan ID prefix. | copy lane via desk |
| Loop admin: Year description "…, guaranteed fresh stock" + Loop Multilingual (the preview only emulates it) | Victor |
| A render on a real Shopify theme with a cart, no payment: **done 27 Nov** on an unpublished test theme (NOTES 24), EN/NL/FR render, Try once x3, 60-Day, Year from the panel in a real cart | done |
| Stepper or dropdown (4g): Victor tests the stepper on his iPhone first | Victor |
| How it goes on: **in git** (Victor, 27 Nov). The values above are in `templates/product.subscription-item.json`, so DH's deploy switches it on, and the theme editor is the way back ("Try once" to Link). The (i) sheets on phones are their own feature with their own way back: Theme settings > Tooltips, "Phones: (i) tooltips as a sheet from the bottom" (on by default; Astra R1 P1). The deploy writes the whole template: settings changed in the live editor since main took it back last would be lost, so compare the live template with main before it ships. | DH, desk |

**Loop admin, read on 27 Nov (nothing changed):**

- **Care Credit** is Loop Loyalty, two active programs on "Order placed with Loop" and "Checkout order placed
  with subscriptions", matched on the order attribute `Subscription Name`: "60-Day Supply" earns 10 %,
  "Year Supply" 20 % (or one of Loop's checkout link IDs), as a percentage of the order. So it follows the
  amount, as Victor said. The buybox sets that attribute: the Year bought from the side panel sends
  "Year Supply" with the plan and the kit, Try once at 3 clears it (`preview/year_attr_check.py`,
  `shots/year-attributes.json`). The "Buybox layout" attribute is not a condition, so it changes nothing.
- A third program, "Onetime- 10%" (draft), is for reactivating migrated older customers (Victor, 27 Nov),
  not part of the buybox.
- **Year plan text** in Loop (selling plan "New Year Supply (Prepaid): (59*6) = €354", the storefront one):
  "6 duos a year (3 now, 3 in month 6)", without "guaranteed fresh stock" yet. Its Check-up Reward tooltip
  says "€40 in Care Credit is added to your account": per account, so a second person on their own email
  gets their own reward, kit and Care Credit.

## 4g. Stepper or dropdown for the quantity (question from Victor, 27 Nov, nothing built)

Victor's idea: a dropdown, so the control can say what it counts ("Personen: N" on the 60-Day later, the
amount on Try once). What has to be checked if it replaces the stepper:

| # | Check | How |
|---|---|---|
| 1 | iOS Safari zooms the whole page when a `<select>` under 16 px font size gets focus. The control needs 16 px on phones. | real iPhone |
| 2 | The native picker (iOS wheel, Android sheet) only shows on a real phone; the Orca browser is Chromium on a desktop. | real iPhone and Android, the preview on the LAN or a dev theme |
| 3 | Width in the pill's row: "Aantal: 6 ▾", "Personen: 4 ▾", FR "Personnes : 4 ▾" are wider than the 90 px stepper, so the €0 pill gets narrower and may take 3 lines at 360 / 390 px. | EN, NL, FR at 360, 390, 1440 |
| 4 | Loop rewrites the widget on every update and the card is one big tap target. Tapping the select must not reselect the card or move the select while its picker is open (iOS closes it). | real iPhone, plus a click test |
| 5 | Night mode: the option list takes the OS colours; the closed select needs the theme's colours and its own chevron. | Day and Night |
| 6 | Screen readers: a select with a visible label reads well by itself ("Aantal, 3"); check VoiceOver and the label. | VoiceOver |
| 7 | Copy: for Try once Dawn's "Quantity" / "Aantal" / "Quantité" exists. "Personen" / "personnes" does not: copy lane. Option texts "1 persoon", "2 personen" need no colon (Victor's style asks for few). FR needs a no-break space before a colon. | copy lane |
| 8 | Everything the stepper feeds stays: title "· 3 Duos", card price, receipt, sticky bar, the remembered quantity, the buy paths (`qty_check`, `memory_check`, `sticky_check`, new selectors). | preview checks |
| 9 | Hotjar shows native selects poorly in recordings; an event with the chosen number keeps it measurable. | Hotjar |
| 10 | "Personen" on the 60-Day is the later step (4e): quantityFor x N, a kit per person, Terms. Care Credit follows by itself (a percentage, read in Loop). | when 60-Day people is built |

## 5. Tracking

- **Hotjar per plan, every buy path:** `kc_checkout` + `kc_checkout_once` / `_60day` / `_year` already
  fire on the buybox CTA, sticky CTA, Try once link, compare tables, end CTA and Loop's own add
  (section 0). New: the same call adds `kc_layout_link` or `kc_layout_card`, so a Hotjar filter can split
  recordings by layout as well as by date.
- **Layout on the order:** cart attribute **`Buybox layout`** = `link` | `card` (name VOORSTEL), set
  in `syncCartSubscriptionName`, which every add path runs before checkout. It reaches the order's
  "Additional details" and the order export ("Note Attributes"), so a before/after read groups orders
  by layout instead of guessing from the flip date. Shopify checkout does not show cart attributes.
  Loop Loyalty reads only "Subscription Name".
- Before/after read: Victor notes the date and hour of the flip; orders before the merge have no
  attribute (all `link` by definition).

## 6. Risks

- **Loop admin (read only, 24 Nov):** "choose subscription by default" off and "one-time at bottom" off.
  If someone turns "at bottom" on, Loop moves the option under the plans: card layout moves it back to
  the top; link layout now hides it at either position.
- **Loop widget updates:** a re-save of the widget design in Loop regenerates `loop-widget-standard.liquid`
  (we do not depend on edits there). A Loop update of `loop-widget.js` would overwrite our KC functions
  as today; the new code sits in the existing KC CUSTOM block.
- **Shop Pay / express buttons:** `show_dynamic_checkout` is off on the Duo template. If it is turned on,
  `kc-express-allowed` shows Shopify's button only while one time is selected, which with the card is the
  default state: Shop Pay would then be visible at first paint. Keep it off, or decide that on purpose.
- **End CTA (`featured-product.liquid`):** a second Loop widget of the same product with the same
  element ids and a fixed 60-Day offer. The card code only touches the first container (the buybox) and
  the button inside `.kc-buybox`. To test: the end CTA's own default must not uncheck the buybox card
  (all Loop radios share one name).
- **Loop Multilingual:** Loop's own one-time label (EN "One Time Purchase") is replaced by our key, so
  Loop's translation tabs do not matter for the card.
- **NL/FR:** all card texts exist in NL/FR. Only the CTA VOORSTEL would need source-copy.
- **Flip written in the live theme only** (section 3): the repo must take the editor's change back.

## 7. Test list

For each: switch OFF and ON (ON only where the product has plan cards).

1. Duo, Awake, Asleep: OFF identical to live today (cards, link, summary, CTA labels, sticky bar).
2. Duo ON: card first, preselected on load (also with `?variant=`), then 60-Day rhythm, then Year.
3. Duo ON: selecting 60-Day / Year and back to Try once; price, sub-row, summary, CTA label and
   sticky bar follow each time.
4. EN, NL, FR: card texts in the page language; no English left.
5. Day and Night (body `day-mode` / `night-mode`): card box, border, selected state, radio.
6. 390 px and desktop (1440): card height and wrapping match the plan cards; no overflow.
7. Cart and checkout line items (on a dev theme, cart only, no payment): one time = 1 Duo, no
   selling plan, no kit lines, no "Subscription Name", `Buybox layout` = `card`; 60-Day and Year as
   today plus `Buybox layout`.
8. Hotjar (consent given): `kc_checkout_once` + `kc_layout_card` on CTA, sticky CTA, compare table.
9. End CTA still offers its 60-Day plan; using it does not change the buybox selection.
10. Theme Check `--fail-level error` exit 0.
