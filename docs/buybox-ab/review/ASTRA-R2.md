# ASTRA R2 — buybox v2

Reviewed 27 November 2026 on `karmicare/buybox-ab`, HEAD `09fc2e4ddf763070f754ff82928ce3f39766b6ef`. Scope: the R1 fixes in `git diff e8884fc..09fc2e4 -- assets/loop-widget.js assets/kc-buybox.css layout/theme.liquid config/settings_schema.json`, plus their immediate callers and dependencies. Read AGENTS.md, ASTRA-R1.md, PLAN.md §4f and NOTES.md result 27. README.md is absent in this checkout.

**Verdict: ready with fixes — 0 P0, 0 P1, 1 P2, 0 nit.** The rollback, stepper and comment fixes pass. The original Duo bundle-quantity reproduction is fixed, but the new call also exposes an unscoped quantity fallback to other products in a conditional layout; fix that before claiming product isolation.

## R1 disposition

### P1 — Link rollback leaves mobile sheets enabled: resolved under the revised contract

- `config/settings_schema.json:2162`–2166 defines the independent `kc_info_sheets` checkbox, default `true`, with the rollback location and behavior in its help text.
- `layout/theme.liquid:98`–105 gates **both** the stylesheet and script on that setting. There is no `default: true` filter that would override an explicit false. Repository search found no alternative loader or activation site: `assets/kc-info-sheet.js:193` adds the HTML class, and that script also installs the capture handlers and exports `KCSheet`.
- PLAN.md §4f, line 416, now explicitly separates the two switches. Link rolls back the Try once layout; Theme settings → Tooltips rolls back the sheets. This meets the separate-feature/switch remedy offered in R1. Link alone intentionally leaves sheets on; restoring both behaviors requires both switches.
- Browser verification at 390 px with the two sheet asset tags omitted from a fresh page: no sheet CSS or JS tags, no `html.kc-info-sheets`, no decorated tips, and `typeof KCSheet === 'undefined'`. The old comparison-table popover appeared on hover (`display:block`, `visibility:visible`, `opacity:1`), and a tip click opened no sheet. The Year panel opened; its close button made `dialog.open` false synchronously, without `is-closing`, through the fallback at `assets/loop-widget.js:3041`–3043. The page lock cleared. The Link page with the same omission had layout `link`, zero steppers, zero sheet assets and no activation class or `KCSheet`.

**Coverage boundary:** the supplied preview always injects the sheet files. I used a temporary, memory-only localhost GET proxy that removed exactly those two HTML tags before loading a fresh page, leaving all other assets unchanged. This tests the runtime consequence of the Liquid false branch; it is not an independently rendered Shopify setting-off test or a theme-editor toggle. The schema default and Liquid condition were inspected in source; NOTES 27's real-theme default-on result was not independently repeated.

### P2 — Bottom-option re-render loses the stepper listener: resolved

`assets/loop-widget.js:3293`–3311 installs the document delegate once behind `window.kcOnceStepperBound`. New markup carries `data-kc-product-id` at line 3333; Loop's `innerHTML` copy preserves it. The handler resolves the input at click time rather than retaining the detached node. Repository search found no remaining `stepper.addEventListener` or second stepper click registration.

Independent browser probes on the supplied candidate, whose served `loop-widget.js` matched the worktree byte for byte:

| Probe | Observed result |
| --- | --- |
| Initial `+` | Chosen quantity and form field 1 → 2; one `kc:once-quantity` event |
| Set `displayOneTimePurchaseOptionAtBottom = true`; call `applyLoopSettings({productId})`, then `updatePriceInParentElementsLoop({productId})`; press `+` | 2 → 3, one stepper, one additional event |
| Repeat that bottom-option render and press `+` | 3 → 4, one stepper, one additional event |
| Append a `cloneNode(true)` stepper, click its minus, then remove the probe copy | Correct product's chosen value and form field decrement once; copied node needs no listener binding |
| Call `setupLoopDomListeners(productId)` twice more, then press `+` | One increment and one additional quantity event |
| Disabled minus at 1; disabled plus at the preview's maximum 6 | Native `.click()` does nothing; no quantity event or quantity change |

The clamp at line 3300 additionally enforces 1–maximum. The parent option's radio click does not match `.kc-once-stepper__button`, so it does not cause another increment. Buttons contain no child markup that would complicate native disabled-click handling. These checks cover supported copied markup and repeated listener setup, not arbitrary third-party interception of bubbling events.

### P2 — Loop override ignores Try once quantity: partly resolved

The original reproduction is fixed by `assets/loop-widget.js:4347`: with Try once at 4, the actual overridden Duo submit handler passed quantity `"4"` to an in-memory `loopHandleAddToCart` recorder.

I also exercised the real `loopHandleAddToCart` through that override with bundle prerequisites stubbed and `handleBundleTransactionLoopWidget` replaced by a recorder that returns no transaction ID, stopping before any network transaction. After awaiting actual plan selection, the captured inputs to the transaction stage were:

| Selection | Quantity | Selling plan |
| --- | --- | --- |
| Try once | 4 | none |
| 60-Day | 1 | `712106115453` |
| Year | 3 | `712155431293` |

The remembered one-time quantity stayed 4 and the form field reset to 1 for plans. `quantityFor` remains authoritative at `assets/loop-widget.js:4720`; subscriptions are not multiplied by the remembered quantity. However, other-product isolation fails under the form ordering described in the new P2 below.

### Nit — Stale comments/destructuring: resolved

`assets/loop-widget.js:2158` now destructures only `totalValue`; the dialog comment at line 3087 and `assets/kc-buybox.css:413` describe the glass title/footer. The quantity comment at `assets/loop-widget.js:3345`–3348 correctly distinguishes the plan-selected form value from the sticky link's remembered quantity and the comparison table's fixed 1. No remaining instance of the specific R1 leftovers was found.

## New finding introduced by the fix

### P2 — An unrelated bundle can inherit the main buybox's quantity

**Location:** `assets/loop-widget.js:4347` (new call), using the existing unscoped fallback at `assets/loop-widget.js:3244`–3245.

`overrideAddToCartButtonLoop(productId)` now calls `kcOnceQuantityInput(productId, false)` for every overridden product. When that product has no form inside `.kc-buybox`, the helper falls back to the first `.kc-buybox form[id^="product-form-"]` without verifying its product ID. If that is the main purchase form, its `.kc-once-quantity` wins over the other product's quantity. The helper existed before R2, but this diff newly uses it on the general bundle-add path, where its fallback is not product-safe.

**Failure scenario:** a page has the Duo card at 4 and another Loop preset-bundle form at 2. The main purchase form precedes the installment form, for example with Buy buttons ordered before Price in the product section. Adding the other bundle passes 4 instead of 2; for an unmanaged product or a one-time order, `quantityFor` preserves the wrong 4.

**Independent reproduction, entirely in page memory:**

1. Set the candidate's Duo quantity to 4. Move its installment form after its purchase form, preserving both nodes; this emulates the relevant form order without editing a template.
2. Append a second form with `data-loop-product-id="r2-other-product"`, a `.quantity__input` holding `2`, and a submit button. This is an isolated other-product fixture, not a claim that the current page has another preset bundle configured.
3. Replace `loopHandleAddToCart` with a recorder, run the actual `overrideAddToCartButtonLoop('r2-other-product')`, and click that form's submit button.
4. The old `document.querySelector(PRODUCT_QUANTITY_SELECTOR)` resolves to `2`. The new helper resolves to the Duo form (`data-loop-product-id="15977093923197"`) and value `4`. The handler records `{ product: 'r2-other-product', quantity: '4' }`; `quantityFor('r2-other-product', '', '4')` returns 4.
5. Restore the recorder, form order and DOM. No bundle/cart request was made.

**Scope:** with the candidate's original form order, its installment form happens to match the generic fallback first and has no `.kc-once-quantity`; the same other-product probe correctly passes 2. Thus this is a conditional supported-layout/multi-product regression, not a demonstrated failure of the current Duo-only configuration. That accidental ordering protection is not a product-identity check.

**Suggested fix:** in the override, prefer only a quantity field from a form whose `data-loop-product-id` actually matches `productId` (or from the current matching `form` itself). If none exists, retain the old fallback; do not accept the generic buybox helper's field unless its owning form is verified to belong to this product. Keep `quantityFor` unchanged. Recheck a second product with a different quantity in both form orders, plus the one-time/60-Day/Year captures above.

## Validation and limits

- `node --check assets/loop-widget.js`: passed.
- `shopify theme check --fail-level error`: exit 0, 259 files inspected, 19 warnings, zero errors; no baseline changes.
- `git diff --check` for the four implementation files over the requested range: passed.
- Chromium checks used EN at 390 px. No iOS/VoiceOver, real Shopify setting-off render, live bundle transaction or fresh real-cart validation was performed. R1's unaffected flows were not re-reviewed wholesale.
- No theme files edited, staging, commits, branch changes, admin writes, cart mutations or checkout. This report is the sole file written by this review.
