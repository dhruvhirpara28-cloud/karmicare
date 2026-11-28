# ASTRA R4 — shared close button

Reviewed 28 November 2026 on `karmicare/buybox-ab`, HEAD `d503921`. Scope: the change in `c168123` after R3 approved `72d5a52`, plus the requested dialog regressions. Read AGENTS.md, ASTRA-R1/R2/R3 and NOTES.md result 30. README.md remains absent in this checkout.

**Verdict: ready with fixes — 0 P0, 0 P1, 0 P2, 3 nit findings.** The current single-section close button and dialog flows pass; the fixes below are nonblocking markup/maintenance cleanup. The requested duplicate-section and strictly-needed-template checks do not pass literally. No new purchase-flow defect was found or purchase transaction exercised.

## Findings

### nit — The new template ID is not unique across sections for the same product

**Location:** `sections/main-product.liquid:677`, lookup at `assets/loop-widget.js:3101`.

**Failure scenario:** render two main-product section instances for the same product with popup/panel enabled. Both emit `id="kc-icon-close-<product.id>"`, since neither section nor block identity participates. The block's schema `limit: 1` prevents two Loop blocks within one section, not this collision between section instances. `document.getElementById` selects the first template globally.

Confirmed the emitted identity in source and reproduced the DOM consequence by temporarily appending a clone of the served template: count 2, lookup still returned the first. Removed the clone afterward. This is a conditional duplicate-section markup defect, not an independently rendered two-section Shopify test. Both templates currently hold the identical inert SVG, so no wrong icon or customer-visible malfunction was demonstrated; severity is nit, not P2. The supplied single-section page has one such template.

**Suggested fix:** use a section-scoped template marker and look it up within the existing `box`, or include section identity in both the ID and its lookup. Keep the existing missing-template guard. Adjust the preview's injected template location/identity to match if adopting the scoped lookup. Existing product-keyed configuration and the shared SVG's internal IDs predate this change; this finding concerns the newly introduced template ID only.

### nit — Template rendering checks the dialog preference, not whether the feature can run

**Location:** `sections/main-product.liquid:676`; runtime guard at `assets/loop-widget.js:2967`.

**Failure scenario:** retain `plan_link_opens = panel` and switch Try once back to Link, or leave `plans_as_link` empty. The template is still emitted, although `kcPlanExtras` disables the dialog feature in Link mode and no plan link can open it with no linked plans. The new condition does correctly omit it for `plan_link_opens = card` and stays inside the existing Loop-template guard.

**Suggested fix:** additionally require the active card layout and a nonblank linked-plan configuration before emitting the template. An enclosing Liquid condition can keep the popup/panel `or` check easy to read. This is unnecessary inert markup, not a rollback interaction failure; no script executes inside the template.

### nit — Header documentation still specifies the removed 44 px button

**Location:** `assets/kc-buybox.css:460`.

**Failure scenario:** a maintainer uses the header comment to calculate its spacing or test expectations and expects 44 px, while the button and body-padding formula now correctly use the 40 px token.

**Suggested fix:** describe the small-button height token instead of a hardcoded 44 px measurement.

## Verified, no finding

### Button parity

Used a fresh Orca Chromium tab on the supplied EN candidate. The served `kc-buybox.css` and `loop-widget.js` matched the worktree byte for byte (SHA-256 respectively `aa2eace3e02691ad14905ff5415ef96dc83f928fd328415aa03e9819b2e08414` and `1475818bdf1566a58bdc1c87302260447fbcb5a9fa15528f1e0d27eea33d48b8`). Did not run the lane's `close_check.py` or reuse its result JSON.

Compared the actual professionals' dialog button with the actual Year dialog button at **390 × 844 and 1440 × 1000**, in **Day and Night**, for **panel and popup**, **with and without the title bar**: all 16 Year configurations matched the professionals' button for computed size, radius, border, background, text/icon colour, accessible label, and complete SVG markup. Day/Night used the existing body classes. Popup used a temporary change to the existing extras JSON; title-free cases temporarily cleared the source badge text during the real link handler's call. Those changes were restored immediately, and final navigation discarded the fixtures.

| Property | Both buttons |
| --- | --- |
| Size | 40 × 40 px |
| Radius / border | 8 px / none |
| Default background | `rgb(127, 185, 255)` |
| Icon colour | `rgb(10, 22, 40)` |
| Hover background | `rgb(116, 168, 232)` |
| Icon | Identical `kc-icon-close.svg`, 16 × 16 px, `aria-hidden="true"`, `focusable="false"` |
| Accessible name | `Close` in EN |
| Focus rule | Same 1.5 px solid focus token, 2 px offset; Day `#191f38`, Night `#fffbf6` |

Native Orca hover commands verified `:hover` and the resulting background for both buttons at both widths and in both tones. Hover/focus declarations are identical to `assets/section-trusted-professionals.css:610` and `:614`; neither depends on the Year header being present. The small-icon declaration also matches exactly. EN/NL/FR preview HTML supplies matching translated names for the two buttons: `Close`, `Sluiten`, `Fermer`; both Liquid paths use `accessibility.close`.

**Focus-ring coverage limit:** rule parity and resolved focus tokens were verified, but an actual keyboard-visible ring was not independently observed. Orca's background page reported `document.hasFocus() === false`; programmatic focus and attempted Tab probes did not activate `:focus-visible`. The successful initial-focus/return checks below concern `document.activeElement`, not proof of a painted keyboard ring. No keyboard-navigation defect is inferred from that tooling limitation.

The implementation reuses the existing icon asset and the same design tokens. It duplicates the small CSS rule set rather than introducing a shared button class, consistent with the requested appearance reuse; no new token or icon artwork was added.

### Header, popup and bottom sheet

| Viewport | Header height | Body top padding with header | Without header | Settled panel bounds |
| --- | --- | --- | --- | --- |
| 390 × 844 | 65 px | 73 px | 20 px | x=0, y=24, 390 × 820 |
| 1440 × 1000 | 73 px | 81 px | 24 px | x=1000, y=0, 440 × 1000 |

The body padding remains the measured header height plus an 8 px gap. Replacing 44 px with the actual 40 px button token reduces both header and padding by 4 px; it does not leave content under the bar. Header-free branches keep their previous body padding and position the same 40 px button absolutely. The sibling selector still applies because the header directly precedes the body. Measurements above use settled animation geometry; initial automated measurements caught the opening transform, so the active opening animations were finished in memory before remeasuring.

Popup mode still opens through the actual Year link after changing `linkOpens` in the in-memory extras: centered 358 × 780 at x=16/y=32 on the phone with the title, and 480 × 744 at x=480/y=128 on desktop. Header-free popup also opens and closes correctly. Mobile panel retains `kc-sheet-in`/`kc-sheet-out`; popup closes without that sheet animation. Desktop panel closes without the mobile exit animation. Scrolling bodies, fixed header/footer structure, and page scroll locking are unchanged by the diff.

### Dismissal and focus

- In all 16 button-parity cases, opening focused the named close button. Clicking it closed the dialog, returned focus to the Year link, and removed `kc-plan-dialog-open`.
- Real Orca Escape keypresses closed both panel and popup at both widths, restored focus, and released the lock.
- Dispatching a click whose target was the dialog itself exercised the existing backdrop/outside handler for both modes at both widths, without a title bar. All closed and restored focus/unlocked. On mobile panel the immediate exit animation was `kc-sheet-out`; all four were closed after the animation/fallback interval. This verifies the handler, not a separately calibrated physical backdrop tap.
- Missing-template probe: temporarily removed the template, opened via the real link, and clicked close. No exception; the modal opened, retained the `Close` name, closed, and returned focus. The button has **no visible cross** in that abnormal state. The guard is runtime-safe but is not a visual fallback; valid normal popup/panel renders include the template. Restored it afterward.
- The EN `/off/` preview reports layout `link`, zero Year-link buttons and zero plan dialogs. The new styles do not activate a dialog in the rollback configuration.

### Liquid and scope

The new `if`/`or`, numeric product-ID interpolation, `inline_asset_content`, and closing tags are valid Liquid. The SVG is static theme content, not interpolated customer input. `cloneNode(true)` clones the template fragment rather than moving or consuming it; repeated open/close cases retained the icon, and a missing/non-template element is guarded by the content check. Duplication and over-broad emission are the nits above.

`git diff 72d5a52..HEAD -- assets config layout locales sections snippets templates` changes **only** `assets/kc-buybox.css`, `assets/loop-widget.js`, and `sections/main-product.liquid`, with the same implementation diff as `72d5a52..c168123`. `git diff c168123..HEAD` over those theme directories is empty. `726fff1` and `d503921` contain only files under `docs/` (the latter includes a preview inspection script). No other lane/theme change has appeared since R3.

## Validation and limits

- `node --check assets/loop-widget.js`: passed.
- `shopify theme check --fail-level error`: exit 0, 260 files inspected, 19 warnings, zero errors. No baseline edits.
- `git diff --check 72d5a52..HEAD` over all theme directories: passed.
- Local preview is captured live HTML with branch assets and emulated Liquid output, not a fresh Shopify render. In particular, `preview/build.py:127` injects the icon template unconditionally at the end of the body, even on `/off/`; preview presence cannot prove the real Liquid guard or placement. Those were reviewed in source. No real theme-editor setting changes, duplicate-section Shopify rendering, iOS/VoiceOver, or cart/checkout test was performed.
- Only this report was written. No theme edits, staging, commits, branch switches, stash, push, admin writes or cart mutations. HEAD remained `d503921`.
