# ASTRA R3 — buybox v2

Reviewed 27 November 2026 on `karmicare/buybox-ab`, HEAD `72d5a521b875add8234bc10b70661ea0cc2bf5f7`. Primary scope: `git diff 09fc2e4..72d5a52 -- assets/loop-widget.js`, resolving R2's remaining P2. Read AGENTS.md, ASTRA-R1.md, ASTRA-R2.md, NOTES.md result 28 and PLAN.md §4f. README.md is absent in this checkout.

**Verdict: ready — 0 P0, 0 P1, 0 P2, 0 nit new findings. R2's P2 is resolved.** This is the requested code-review verdict, not a live deployment or device-test sign-off.

## R2 P2 disposition: resolved

At `assets/loop-widget.js:4348`–4354, the override accepts the Try once input only when its actual owning form exists and `form.dataset.loopProductId === String(productId)`. A field returned by the helper's generic buybox fallback is therefore rejected for another product. The existing `document.querySelector(PRODUCT_QUANTITY_SELECTOR)` fallback remains intact. The purchase form supplies this product identifier through `snippets/buy-buttons.liquid:46`; numeric and string product IDs are handled consistently.

### Independent reproduction and regression control

Used a fresh Orca Chromium tab at `http://127.0.0.1:9377/candidate/en/products/karmicare-biorhythmic-oral-care-system`. Did not run or reuse the lane's `astra_r1_check.py`. The served `loop-widget.js` matched the worktree byte for byte (SHA-256 `0f7ba2bbffd2e7ede5d55c2632d0e14888d8ea2bf85ef9714520a39aa89e19ba`).

In page memory, incremented the actual Try once stepper from 1 to 4 and appended an unrelated product form (`data-loop-product-id="r3-other-product"`) with `.quantity__input` value 2 and a submit button. Exercised the original installment-first order, then moved the installment form after the purchase form. Replaced `loopHandleAddToCart` with a recorder that cancels the click before submission. Compared the actual override functions read directly from `main`, `09fc2e4` and the loaded HEAD asset, invoking each against the same fixture and clicking its newly overridden button.

| Form order | Generic helper for other product | Pre-branch `main` quantity | R2 quantity | R3 quantity |
| --- | --- | --- | --- | --- |
| Installment before purchase | No Try once field | 2 | 2 | **2** |
| Purchase before installment | Duo field, value 4 | 2 | **4 — reproduces R2** | **2** |

The Duo's own overridden button passed **4 in both orders**, also when `overrideAddToCartButtonLoop` received its product ID as a number. Removing the other product's quantity input yielded `undefined`, rather than the Duo's 4. Restored the installment position, removed the fixture and restored the recorder; subsequent navigation discarded the temporary button overrides.

This is a conditional multi-product layout fixture, not a claim that a second bundle is configured in the supplied Duo page. It reproduces R2 with the old function and demonstrates that the new ownership guard removes that regression.

### Duo bundle path retains plan quantities

Exercised the actual `loopHandleAddToCart` through HEAD's overridden Duo submit button. Stubbed only the bundle prerequisites (`getLoopWidgetBundleVariantInfo`, `getLoopWidgetProductBundleData`) and replaced `handleBundleTransactionLoopWidget` with a recorder returning no transaction ID, so execution stopped before any transaction or cart request. Selected 60-Day and Year through the real, awaited `KCPlanSelect.choose`; both returned success. A temporary fetch guard rejected mutating requests during this probe; none was attempted.

| Selection | Override argument | Transaction-stage quantity | Transaction-stage selling plan | Remembered Try once quantity |
| --- | --- | --- | --- | --- |
| Try once | `"4"` | **4** | None | 4 |
| 60-Day | `"1"` | **1** | `712106115453` | 4 |
| Year | `"1"` | **3** | `712155431293` | 4 |

The hidden form input resets to 1 on subscription selection. `quantityFor` remains authoritative downstream at `assets/loop-widget.js:4724`; the ownership fix does not multiply subscription units by the remembered one-time quantity. Restored all intercepted functions after the probe.

### Products without a Try once field

On the supplied `/off/en/products/karmicare-biorhythmic-oral-care-system` page, confirmed layout `link` and zero `.kc-once-quantity` fields. Compared the actual pre-branch `main` override with HEAD against that page's product form:

| Input configuration | Pre-branch argument | HEAD argument |
| --- | --- | --- |
| No quantity input | `undefined` | `undefined` |
| In-memory `.quantity__input`, value 5 | `"5"` | `"5"` |

The absent-input argument still reaches the unchanged default parameter `quantity = 1` in the real handler. The global Dawn selector's pre-existing behavior is deliberately preserved; the change does not turn it into a newly scoped selector. No additional regression established from this diff.

## Final lane sanity review — P0/P1 only

Reviewed `main...HEAD` for the eleven buybox implementation files: `assets/karmi-add-to-cart.js`, `assets/kc-buybox.css`, `assets/kc-info-sheet.css`, `assets/kc-info-sheet.js`, `assets/kc-plan-select.js`, `assets/loop-widget.js`, `layout/theme.liquid`, `sections/main-product.liquid`, `snippets/kc-plan-config.liquid`, `snippets/sticky-cart-block.liquid`, and `templates/product.subscription-item.json`; also reviewed `config/settings_schema.json`. Excluded unrelated lane changes, including the previously excluded plaque wording in the subscription template.

No additional P0/P1 blocker found. Checked the one-time quantity propagation and fixed-link override, plan-ID selection and unit authority, Year panel CTA selection, shared Welcome Kit extraction, card/default-selection guards, sticky quantity synchronization, independent sheet asset switch, modal dismissal/scroll-lock handling, and the separate layout cart attribute. R1/R2's resolved findings remain consistent with the final implementation. This was a final source sanity pass, not a repeat of every R1 interaction or real-cart check.

## Validation and limits

- `shopify theme check --fail-level error`: **exit 0**, 259 files inspected, 19 warnings, zero errors; baseline unchanged.
- `node --check` passed for all four changed JavaScript assets: `loop-widget.js`, `kc-plan-select.js`, `kc-info-sheet.js`, `karmi-add-to-cart.js`.
- `git diff --check main...HEAD` for the twelve reviewed implementation files: passed.
- Browser probes covered EN candidate and Link fallback in Chromium. No fresh NL/FR, iOS/VoiceOver, real Shopify setting toggle, real bundle/cart transaction or checkout test was performed. Prior lane live-theme/cart evidence was not independently repeated.
- No theme files edited, staging, commits, branch changes, admin writes or cart mutations. HEAD remained `72d5a52`. This report is the sole file written by this review.
