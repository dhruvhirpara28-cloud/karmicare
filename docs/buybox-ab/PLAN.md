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
| `sections/main-product.liquid` | Loop block schema: new `select` setting `try_once_layout`. The `price` block's `#kc-try-once-container-<id>` gets `data-kc-once-layout` plus the card texts as data attributes (title, details, CTA, from existing locale keys and the existing block settings). The `kc-plan-config` render passes `default_to_subscription: false` when the layout is `card`. |
| `assets/loop-widget.js` | `kcOnceCard(productId)` helper (reads the attribute above). `applyDefaultSelectionBasedOnLoopSettings` and the bundle default (l.3204): card layout selects one time, whatever the theme or Loop admin "default to subscription" says. `injectOrUpdateKcTryOnceLink`: card layout shows the top option as a card (class `kc-once-card` on the buybox container, plan card structure: label + sub-row, price + "one-time", details when selected), hides the link; link layout as today, plus it now also hides a one-time option Loop moved to the bottom. `updateKcPricingSummary`: keeps the link hidden in card layout. `updateKcPlanButtonLabel`: buybox CTA label for one time in card layout. |
| `snippets/loop-widget.css.liquid` | New rules scoped to `.kc-once-card`: plan card box, border and selected state for the one-time option, details shown only when selected. Nothing outside that scope changes. |
| `assets/kc-plan-select.js` | `syncCartSubscriptionName` also keeps the cart attribute `Buybox layout` (section 5) on the page's layout; `trackCheckout` adds `kc_layout_link` / `kc_layout_card`. |

Untouched: `snippets/loop-widget-standard.liquid` (Loop-generated; not needed), `assets/loop-widget.css`,
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
| Sub-row 1 | `kc.receipt.per_brushing` (price / 120 brushings, as the summary) | €0.56 / brushing |
| Sub-row 2 | `kc.sticky_cart.delivery_once_html` | Shipping calculated at checkout |
| Details, when selected | `kc.sticky_cart.guarantee_once_html` | 14-day money-back guarantee |
| Details, when selected | block setting `try_once_note` | €0 Care Credit · €0 Dental Check-up Reward |
| Buybox CTA with Try once selected | `kc.sticky_cart.cta_once_html` (the sticky bar's CTA) | Try once |

Open copy point, **VOORSTEL**: the CTA rule is "Begin your …", and "Try once" is the sticky bar's
existing CTA. If Victor wants the rule here too: EN "Begin your first Duo" (VOORSTEL), NL/FR through the
source-copy lane via the desk. Today's fallback "Begin Now" (`custom_button_text`) is not used in card
layout.

The summary box under the cards already has a one-time state ("Total today €67 one-time", "€0.56 per
brushing · no Care Credit", no rewards rows). No other new text.

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
