# ASTRA R5 — R4 nit fixes

Reviewed 28 November 2026 on `karmicare/buybox-ab`, HEAD `9de5fd9`, against R4's `d503921`. Read AGENTS.md and ASTRA-R4.md; README.md is absent in this checkout.

**Verdict: ready — 0 P0, 0 P1, 0 P2, 0 nits.** All three R4 nits are resolved; no regression found in this diff.

| R4 nit | Result and evidence |
| --- | --- |
| Product-keyed template identity / global lookup | **Resolved.** `sections/main-product.liquid:679` emits `<template data-kc-icon-close>` without an ID. `assets/loop-widget.js:3102` queries the existing `box` first, then falls back to a page template containing the same static SVG. An in-memory probe placed a distinguishable foreign template earlier in the DOM and the intended template inside the buybox: both panel and popup cloned the buybox's own icon. |
| Over-broad template emission | **Resolved.** `sections/main-product.liquid:677–681` requires `try_once_layout == 'card'` **and** `plans_as_link != blank`, enclosing the separate popup/panel condition. It remains inside `template_exists`. Thus Link layout, blank linked-plan configuration, and inline-card opening omit the template. The nested conditions avoid mixed `and`/`or` precedence ambiguity. |
| Stale 44 px comment | **Resolved.** `assets/kc-buybox.css:460` now names `--kc-responsive-size-button-sm-height`; no CSS behavior changed. |

## Regression checks

- Fresh Orca Chromium tab on the supplied EN candidate; served `loop-widget.js` and `kc-buybox.css` matched the worktree byte for byte (SHA-256). The actual Year link opened the panel with the shared 16 px SVG, a 40 × 40 px close button and accessible name `Close`.
- Through the real link handler, tested panel and popup with the page-level fallback, then with the scoped template and earlier foreign template. All four openings retained the icon and focused Close; clicking Close dismissed the dialog, returned focus to Year and released the scroll lock.
- Removed all icon templates temporarily and repeated both modes: no captured exception, named Close remained functional, focus returned and scrolling unlocked. As in R4, this guard supplies no visible cross when the template is absent; it is runtime protection, not a visual fallback. `closeIcon && closeIcon.content` and `cloneNode(true)` remain intact. All temporary DOM/configuration changes were restored.
- Liquid nesting, attribute markup and unchanged `inline_asset_content` use are valid. `shopify theme check --fail-level error`: **exit 0**, 260 files, 19 warnings, zero errors. `node --check assets/loop-widget.js` and `git diff --check d503921..HEAD` over theme directories passed.
- `git diff --name-only d503921..HEAD -- assets config layout locales sections snippets templates` lists **only** `assets/kc-buybox.css`, `assets/loop-widget.js`, and `sections/main-product.liquid`. No other theme file or Theme Check baseline changed.

## Limits

The local preview emulates Liquid and injects its template outside the buybox unconditionally; its normal icon check exercises the global fallback. The scoped lookup was verified with temporary DOM placement, while the emission guard was reviewed in Liquid source and checked by Theme Check. The lane's reported real Shopify render (one template, icon present, no Liquid error) is supplied evidence, not a render independently repeated here. This focused review does not repeat R4's full viewport/theme matrix or exercise cart/checkout.

Only this report was written; no theme edits, staging, commits, branch changes or remote writes.
