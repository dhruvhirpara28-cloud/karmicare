# Nav child: report

Task `task_cd7f661028f8`, dispatch `ctx_aee03e18a874`, run `run_32dd5602b983`. Branch `karmicare/soft-launch-global-nav`, base `1c01dc5`. Date 2026-10-20.

## Preflight

- `orca status --json`: runtime `ready`, `reachable: true`.
- Branch `karmicare/soft-launch-global-nav`, tree clean at the start.
- Model Claude Opus 5.5 (`claude-opus-5-5`), permission mode Manual/default, Bash sandboxed.
- AGENTS.md read; `.coordinator/BRIEF.md`, `COMMON-RULES.md`, `BROWSER-WORKFLOW.md` read.

## What changed

All rows were Victor's direct instructions in this terminal (see `NAV-AUDIT.md`, NV-01 to NV-08).

| Commit | Change |
|---|---|
| `734b62e` | PDP nav hides on scroll down, returns on scroll up (NV-01) |
| `a6000c4` | Sticky bar shows once the first plan card leaves the screen; EN delivery line (NV-02, NV-03) |
| `e21ee67` | Library glass values in the held-back tokens; glass border on the nav (NV-04; border later removed) |
| `1571898` | Nav: no border, token surface, larger mobile logo; section lookup by id (NV-01, NV-05, NV-07) |
| `f46d511` | Nav on the secondary surface (NV-05) |
| `1a475df` | Nav shadow `--kc-elevation-md`; hide offset covers the shadow (NV-06) |
| `de58e27` | Mobile nav 8px lower (NV-08) |

Files: `sections/header.liquid`, `snippets/sticky-cart-block.liquid`, `snippets/day-night-color-variables.liquid`, `locales/en.default.json`.

## Evidence

- Theme Check `shopify theme check --path . --fail-level error`: exit 0 before every commit, no new ignores, no offenses in the changed files.
- Rendered on the lane localhost `http://127.0.0.1:16197` (theme `189890265469`, run by the landing desk), Orca browser, Day unless noted:
  - NV-01: hidden at scrollY 600/900 (bar bottom 0, later -28 with the shadow offset), back after 100px up, shown at the top; works again after a simulated section swap.
  - NV-02: at 2176 and 393 wide, bar hidden with the first card 20px on screen, shown 5px past it.
  - NV-03: panel text read back from `[data-sc=delivery]`.
  - NV-05: 393 Day `rgba(255,255,255,0.9)`, 393 and desktop Night `rgba(33,42,73,0.9)`; `manualTheme` cleared after the Night test.
  - NV-07: logo 140 at 393 (25px clear of BEGIN NOW), 110 at 360, 98 at 320 (as before).
  - NV-08: 12px below the announcement bar at the top, 12px from the top when it returns mid-page.
- Screenshots (gitignored): `docs/global/nav/shots/nav-393-day-top-after.png`, `nav-393-night-top-after.png`, `nav-393-day-top-shadow-after.png`, `nav-393-day-menu-open-after.png` (with the since-removed border), `nav-1440-day-top-after.png` (with the since-removed border).

## Cleanup check

- Removed in `a6000c4`: the `gallery` variable and its rule in `checkBuybox` (`git grep -n "gallery" snippets/sticky-cart-block.liquid`: no match).
- Removed in `1571898`: the `glass_bg_day` / `glass_bg_night` Liquid variables (`git grep -n glass_bg_ -- sections snippets`: no match) and the border rules from `e21ee67`.
- Now obsolete for the bar, kept and reported: the header settings `bg_color_day`, `bg_color_night`, `product_bg_color_day`, `product_bg_color_night` still feed `sections/header.liquid` L346-371 and `snippets/product-header-css.liquid` L19-30, but the glass background rules after them override every case. They sit in `sections/header-group.json` (Victor's editor values), which needs the coordinator's approval. Decision below.

## Pending

- Astra review of this branch, requested from the coordinator (the orchestrator launches Astra).
- Merge into `karmicare/soft-launch-global`: the coordinator's worktree holds that branch.
- NL/FR delivery line: `[NEEDS APPROVED COPY]` for "Free Fast Delivery: 24 hours in Benelux. 3 days in rest of Europe"; NL/FR still show the old line.
- Brief phase 1 audit (D-12, drawer, desktop menus, Coming soon, current page): not started.
- Preview theme `189890265469` was created by this worker's first `shopify-preview.py dev` attempt (failed twice on "Premature close"); the landing desk now serves localhost 16197 from it.

## Handoffs

- `snippets/sticky-cart-block.liquid`, `locales/en.default.json` (PDP lane) and `snippets/day-night-color-variables.liquid` (tokens) are outside this brief's file list; changed at Victor's direct request. Tell their owners before merging.
- `assets/kc-tokens.css`: `--kc-brand-glass-bg-light` (0.9), `-bg-dark` (0.85), `-border-light` (white 0.4) lag the library (0.93, 0.93, `rgba(25,31,56,0.15)`). Generated file; the generator `docs/design-tokens/generate.py` is no longer in the repo. No theme file reads these names today.
- Delivery times: the new line (24 h Benelux, 3 days rest of Europe) differs from `templates/page.consumer-rights.json` and Terms (1–3 working days Benelux, 2–5 rest of the EU). Legal/content owner.
- `assets/kc-gallery.js`: the desktop gallery sticks below the header height; with the nav away there is a band above it. Left as is because the nav comes back on scroll up.

## Open decisions for Victor

1. Remove the now-unused bar colour settings (`bg_color_*`, `product_bg_color_*`) from the header schema and `header-group.json`? Recommendation: yes, after the Astra review, so the editor stops offering knobs that do nothing.
2. Delivery line copy for NL and FR.
