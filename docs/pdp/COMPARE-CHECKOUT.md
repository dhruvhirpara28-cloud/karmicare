# Comparison table buttons: straight to checkout

Victor, 20 Oct: "alle knoppen in de vergelijkingstabel moeten meteen naar checkout met het correcte plan".

Commits on `karmicare/soft-launch-pdp`: 59ece89 (plans table), d6a8120 (comparison table "Begin now").
Preview theme 189885940093.

## What each button does

| Table | Button | Buys | Path |
| --- | --- | --- | --- |
| Comparison table | Begin now | the plans table's featured plan: 60-Day Rhythm, 712106115453 | `KCPlanSelect.buy` |
| Plans table | Try Once | one time, no selling plan | `KCPlanSelect.tryOnce` (unchanged) |
| Plans table | Begin 60-Day Rhythm | 712106115453 | `KCPlanSelect.buy` |
| Plans table | Begin (The Karmicare Year) | 712155431293 | `KCPlanSelect.buy` |

`buy()` calls `karmiAddToCart(buyboxForm, button, { sellingPlanId, isBundleProduct, welcomeKitVariantIds })`.
That is the fixed-offer call the end CTA makes, with the kit lines from `kitLines()` that the buybox form
path (`assets/product-form.js`) uses. Cart logic, plan IDs, the Loop widget and the buybox flow are unchanged.

- A real `table_button_url` in the comparison metaobject still wins. '#' or empty buys the featured plan.
- A plan the page cannot sell (unknown, not public, wrong group, not offered for the variant) buys nothing. It is chosen in the buybox instead, with a `[KC plans]` console warning.
- Double clicks: `karmiAddToCart` disables the button and sets `.loading` on the first click. The click handler ignores a button that is disabled or loading. `replaceChoice` sends only the last of several quick choices to checkout.
- Loading state: a spinner beside the label, drawn in `currentColor` (R13 F1).

## Evidence: request payloads

The theme's own `assets/kc-plan-select.js` and `assets/karmi-add-to-cart.js` were run in jsdom on the
server HTML of the dev server (127.0.0.1:9293), EN `/`, NL `/nl/`, FR `/fr/`. `fetch` was stubbed with an
empty cart and recorded every call. The checkout redirect was captured instead of followed. Every button was
clicked twice in a fresh page. All three locales give the same lines:

```
Begin now / Begin 60-Day Rhythm
  add.js: Duo 58451672170877 qty 1 selling_plan 712106115453
          + kit 58801117200765, 58801116840317, 42732469092534 (qty 1, _welcome_kit, parent_id Duo)
          attributes { "Subscription Name": "60-Day Supply" }
  redirect: <root>checkout?discount=Welcome%20Kit
Begin (The Karmicare Year)
  add.js: Duo 58451672170877 qty 3 selling_plan 712155431293 + the same 3 kit lines
          attributes { "Subscription Name": "Year Supply" }
  redirect: <root>checkout?discount=Welcome%20Kit
Try Once
  add.js: Duo 58451672170877 qty 1, no selling plan, no kit
  redirect: <root>checkout
```

`<root>` is `/`, `/nl/` or `/fr/`. Each run made 1 `cart/add.js` call per button (the second click added
nothing), and the button was loading and disabled right after the first click. With a non-public plan forced
onto the buttons (712192164221), there were 0 add calls and no redirect: the plan was chosen in the buybox instead.

Not checked: the real checkout (agents never open it), Loop running on the page, mobile, the spinner on screen.

## R14 fixes (docs/runtime-review/R14-PDP-ASTRA.md F1-F3)

`attempt()` in `assets/kc-plan-select.js` wraps every table click. The cart and the redirect stay karmiAddToCart's.

- **F1, Back from checkout:** the buttons this attempt made busy are tracked. A persisted `pageshow` makes them usable again: not disabled, not loading, spinner hidden, no `aria-busy`.
- **F2, cart error:** after an attempt that did not go to checkout, the buybox error line is read (karmiAddToCart hides it at every start). When it is shown, its text goes into the table's own `role="alert"` line (`snippets/kc-plan-feedback.liquid`). A new click clears it.
- **F3, accessibility:**
  - Names via `aria-labelledby`: the visible label, plus the plan title when the label does not say it ("Begin The Karmicare Year", "Begin now 60-Day Rhythm").
  - `aria-busy="true"` while the attempt runs, and a visually hidden `role="status"` line with `accessibility.loading` ("Loading...", "Bezig met laden...", "Chargement en cours...").
  - The spinner is `aria-hidden` (`snippets/kc-plan-spinner.liquid`).

Evidence: the same jsdom run, EN/NL/FR, all four buttons, all as expected:
- During the attempt: busy, disabled, spinner shown, status text set.
- After a persisted `pageshow`: everything reset, and a second click adds and redirects again.
- A rejected `cart/add.js` ("Only 2 left"): the message shows at the table, the button is free again, and there is no redirect.
- A new click hides the error line.

Not checked: Back in a real browser (the helper cannot click, and the checkout may not be opened), and a screen reader.

## Steps for Victor (preview 189885940093)

For each of `/`, `/nl/`, `/fr/`:
`https://karmicares.myshopify.com/<locale>products/karmicare-biorhythmic-oral-care-system?preview_theme_id=189885940093`

1. Scroll to the comparison table (Karmicare vs others) and click **Begin now**. The button shows a spinner, then the checkout opens in the page language. Check:
   - Awake & Asleep, 60-Day Rhythm, quantity 1, €59.
   - Welcome Kit under it: Morning Toothbrush, Evening Toothbrush, Floss, free.
   - Subscription Name "60-Day Supply" (order attribute, Admin order view after a test order only).

   Go back to the page.
2. In the plans table, click **Begin 60-Day Rhythm**: same checkout as step 1.
3. Click **Begin** under The Karmicare Year: Year plan, quantity 3, €354, the same Welcome Kit, Subscription Name "Year Supply".
4. Click **Try Once**: Duo one time, quantity 1, €67, no Welcome Kit.
5. Double-click any plan button: one checkout, the Duo once.
6. From a checkout, press the browser's Back button: the table button you clicked works again (no reload needed).

Each new click replaces the earlier choice in the cart, so the steps can run one after another.
