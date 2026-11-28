# ASTRA R1 — buybox v2

Reviewed 27 November 2026, branch `karmicare/buybox-ab`, HEAD `e8884fc282abd070815cee461974cd8d57ecaed1`, against `main...HEAD` in the requested eleven files. Read AGENTS.md, PLAN.md (including 4c/4d/4f/4g), and NOTES.md results 20–26. README.md is absent in this checkout. Other lanes' changes were excluded, including the plaque wording in the subscription template from `b144e42`.

At completion HEAD had advanced externally to `a8d8d3b` (a PLAN.md-only change about Terms timing); the eleven reviewed implementation files are unchanged from `e8884fc`.

Read-only review: no theme edits, commits, staging, admin changes, real cart requests or checkout. Browser checks used the local candidate/off pages in Orca Chromium. Purchase probes replaced `fetch` and `KCPlanSelect.replaceChoice` in page memory to capture payloads without running cart mutations or navigation; consequently those probes verify callers/payloads, not the live cart transaction. The replacement queue and attribute synchronization were reviewed in source. NOTES 24/26's real-cart results are prior evidence, not tests independently repeated here.

## Findings

### P1 — Link rollback leaves the new mobile tooltip behavior enabled

**Location:** `layout/theme.liquid:94`, `assets/kc-info-sheet.js:140`, `assets/kc-info-sheet.js:193`, `assets/kc-info-sheet.css:115`.

The new stylesheet and script load for product/index/collection/article templates independently of the Loop block's layout. The script always adds `html.kc-info-sheets`, decorates tooltips and intercepts their clicks below 750 px. Its CSS hides the existing popovers. Neither clearing the new settings nor choosing Link disables this behavior.

**Concrete failure:** load `/off/en/products/karmicare-biorhythmic-oral-care-system` at 390 px with `data-kc-once-layout="link"`, then tap a visible `(i)`. Independently reproduced: `kc-info-sheets` remains on `<html>`, the old popover computes to `display:none`, and `.kc-info-sheet[open]` appears. The merchant's specified rollback therefore does not restore the pre-branch mobile interaction or its page-scroll behavior. A screenshot comparison with every tooltip closed misses this difference.

**Suggested fix:** gate both activation and popover suppression behind the intended feature switch, and make Link restore the old tooltip interaction. If the universal sheets are intended to remain a separate feature, give them an explicit rollback switch and update the release contract; the present “Link equals today's live behavior” promise is not true.

### P2 — A Loop bottom-option re-render retains stepper markup but loses its listener

**Location:** `assets/loop-widget.js:3303` (listener registered at 3310); interaction with `showOneTimePurchaseOptionAtBottomLoop` at 715–717 and `kcRenderOnceCard` at 3368.

The stepper receives its click listener only when its element is first created. Loop's supported “one-time at bottom” path copies the top option using `innerHTML` and empties the original. This copies `.kc-once-stepper` markup but drops the listener. The card renderer moves those new nodes back to the top, finds an existing stepper, and never binds it again.

**Concrete failure:** on the candidate, increase Try once to 2; set `loopPropsUI.displayOneTimePurchaseOptionAtBottom = true` in page memory, call `applyLoopSettings({productId})` followed by `updatePriceInParentElementsLoop({productId})` (the existing update path), then press `+`. Independently reproduced: there is exactly one stepper, but `data-kc-chosen` stays `"2"`; the displayed quantity and submitted quantity can no longer be changed with either button. The same path can run on a subsequent Loop initialization with that setting enabled. Current recorded admin configuration has it disabled, so this is a supported-configuration/re-render defect rather than a failure of the current initial page.

**Suggested fix:** delegate stepper clicks from a stable ancestor, resolving the current quantity input inside the handler, or bind each actual stepper node idempotently using a non-serialized marker/WeakSet. A copied `data-*` binding flag would reproduce the problem. Recheck after two successive Loop initializations with “at bottom” enabled.

### P2 — Loop's preset-bundle add path does not read the new one-time quantity

**Location:** `assets/loop-widget.js:3247`–3254; consumer at `assets/loop-widget.js:4326`–4330 and default at 4679.

The new quantity input is `input[name="quantity"].kc-once-quantity`. Loop's own overridden add button still reads the document's `.quantity__input` (`PRODUCT_QUANTITY_SELECTOR`). On this page there is no such input. It passes `undefined` to `loopHandleAddToCart`, which defaults to 1; `quantityFor` preserves that 1 for one-time orders. A different Dawn quantity input elsewhere could instead supply an unrelated value. This contradicts PLAN 4d's assertion that this path takes the new form quantity.

**Concrete failure:** with Try once showing 3 and the form input holding 3, enable/use Loop's preset-bundle button override. Its handler sends an undefined quantity, so a one-time bundle purchase proceeds at 1 instead of the 3 shown. Independently probed the actual override with `loopHandleAddToCart` replaced by a recorder: form quantity was `"3"`, while the handler's quantity argument was undefined. No bundle transaction was run. `isProductBundle(productId)` is currently false in the candidate, so the normal Duo CTAs are unaffected today.

**Suggested fix:** make the override read its own product form's `input[name="quantity"]`, or explicitly use `KCOnceQuantity.get(productId)` for the card's one-time selection. Keep `quantityFor` authoritative for subscriptions. Add a focused intercepted test of this path rather than treating the buybox CTA test as coverage of it.

### nit — Comments and destructuring retain superseded behavior

**Location:** `assets/loop-widget.js:3329`, `assets/loop-widget.js:3087`, `assets/loop-widget.js:2158`, `assets/kc-buybox.css:413`.

The stepper comment still says the sticky “Try once for €67” link buys one while a plan is selected; the implemented sticky link now displays/buys the remembered quantity. Dialog comments still describe a footer fade that was replaced by glass. The extracted Welcome Kit code destructures unused `title` and `productsHtml` in `updateWelcomeKitUI`.

**Concrete consequence:** a maintainer following the stepper comment would write an expectation of quantity 1 after choosing 3 and switching to 60-Day, while the intentional result is 3 (independently captured). These leftovers obscure the final behavior but do not themselves change checkout.

**Suggested fix:** describe the field's reset separately from fixed-link quantities, update the footer comments, and destructure only `totalValue` there.

## Verified, no finding

### Purchase correctness in the active configuration

The following actual UI handlers were exercised against in-memory request capture:

| Path/state | Captured result |
| --- | --- |
| Buybox Try once after two increments | Variant `58451672170877`, quantity 3, no selling plan or kit |
| Sticky CTA with Try once selected | Same one-time quantity 3 |
| Buybox 60-Day after remembering 3 | Plan `712106115453`, quantity 1, three kit lines each quantity 1 and `parent_id:58451672170877`, `Subscription Name:60-Day Supply` |
| Sticky “Try once for …” with 60-Day selected | One-time quantity 3, no kit |
| Comparison table Try once in that state | One-time quantity 1, no kit |
| Year side-panel CTA | Plan `712155431293`, quantity 3, three nested kit lines, `Subscription Name:Year Supply` |
| Sticky CTA with Year selected | Same Year plan, quantity and nested kit |

The hidden buybox input resets to 1 for a plan while `data-kc-chosen` remains 3, and restores 3 on returning to Try once. Plan units come from `quantityFor`, not multiplication by remembered one-time quantity. The Year panel CTA selects its plan before invoking the existing buybox handler. No new ID/name-based selection mismatch found.

Source inspection of `replaceChoice`, `clearPurchaseChoice`, recovery, `nestKit` and `syncCartSubscriptionName` found no new regression: the existing serialized replacement removes earlier product/kit choices, restores rejected choices where possible, and sets/clears `Subscription Name` by actual plan identity. The added `Buybox layout` attribute is separate. One-time captured payloads omit the name; clearing the existing cart attribute is performed by the reviewed replacement/sync code, not proved by the mocked payload tests.

### Rollback apart from the sheet finding

Card defaults, quantity maximum, badge/strike/link configuration, selected-only chips, one-time CTA override and promise hiding are guarded by `kcOnceCard` or its data/config equivalent. The Link preview reports Link and retains the subscription-oriented layout. The shared Welcome Kit extraction preserves its original markup/listener logic. No additional rollback defect established. No claim of an independent full pixel comparison is made.

### Re-rendering apart from the stepper finding

Repeated ordinary selection/quantity updates did not duplicate the stepper, Year link or dialog. Text/class updates generally compare current values before writing, and the info-sheet observer watches child-list changes rather than its own attribute decoration. No self-sustaining MutationObserver loop was observed during these checks. Full replacement of arbitrary widget/form nodes was not exhaustively simulated.

### Dialogs and sheets

In the mobile candidate, the Year dialog opened with the accessible name “The Karmicare Year” and initial focus on its named close button. An info sheet opened above it with `aria-labelledby="kc-info-sheet-heading"`. Exercising the cancel handler closed the info sheet, returned focus to its `(i)`, removed only its scroll lock and left the Year dialog open/locked; the panel's outside-click handler then closed it, restored focus and released its lock. An ordinary off-page sheet also returned focus and released its lock. Native `<dialog>` supplies modal focus containment; CSS animation rules are restricted to `prefers-reduced-motion: no-preference` and closing has a timeout fallback.

This is Chromium plus source review, not an iOS Safari/VoiceOver sign-off. Real-device scrolling, safe-area behavior and assistive-technology announcements remain device-test coverage gaps. No additional verified dialog defect is asserted from those gaps.

### Liquid, schema, CSS and cleanliness

- `shopify theme check --fail-level error`: exit 0, 258 files inspected, 19 warnings, zero errors. No baseline modification.
- `node --check`: passed for all four changed JavaScript assets.
- New settings JSON and the conditional `defaultToSubscription` render use standard Liquid constructs; added attribute text is escaped and configuration is JSON-serialized. No new Shopify-object/filter or schema error found.
- Existing single-language block-setting translation gate is unchanged; no separate translation finding added.
- New card, badge, strike and dialog styling is principally scoped to the new classes. Day/Night token usage and reduced-motion selectors were inspected; no further concrete cross-layout CSS regression established beyond global mobile popover suppression. Pixel parity and real-device rendering were not independently exhaustively retested.
- No theme files were edited. This report is the sole file written by this review.

## Verdict

**Ready with fixes — 0 P0, 1 P1, 2 P2, 1 nit.** Resolve the Link rollback mismatch before release. Fix the two conditional Loop integration gaps before claiming all supported Loop configurations and add paths are covered; the current primary purchase flows passed the intercepted checks above.
