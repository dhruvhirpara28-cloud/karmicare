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
| `640ada3` | Unused bar colour settings removed: schema, CSS, `header-group.json` values (Victor: clean up unused code) |
| `756a668` | NL and FR delivery line (Victor: translate right away) |
| `25e2ca5` | Merge of `karmicare/soft-launch` (72a84ab): mobile 12px kept; integration desktop +1.6rem, CTA states, kit/money code, receipt keys kept |
| `9a96945` | Astra R10 F1: sticky bar remeasures the first plan card at every decision (+ ResizeObserver) |
| `60c91b6` | NV-09: nav 16px from the top after scrolling on every page but the PDP |
| `b0c9fd2` | NV-10: floating navigation, independent of the page structure |
| `57f8f0e` | Merge of `karmicare/soft-launch` (db46f0a, landing 65ff2a8) before the R12 fixes, no conflicts |
| `a2c13e5` | R12 M1: desktop bar 12px under the announcement bar, as mobile (Victor chose it on localhost, 20 Oct); `padding_top` removed |
| `854348b` | R12 F1: pre-script clearance and position equal the measured ones |
| `70364f6` | R12 F3: nav position without an announcement bar |
| `310bf26` | R12 F2: mega-menu height cap follows the floating nav; dead Dawn header classes removed |
| `63b03d7` | R12 F4 + F5: mobile menu Tab wraps on shown controls; drawer closes past its breakpoint (one file, one commit) |
| `11a6237` | R12 F6: `#fragment` targets land below the nav |
| `4102b4d` | R10 F2 decided: delivery line "2–3 days" rest of Europe, EN/NL/FR + 28 locales on EN |
| `b69aa86` | R12b remaining P2 (F4): drawer Tab endpoints measured on every Tab (desktop drawer resized while open; submenu scope) |
| `3441bac` | R12c regression (P2): scope only `details[open].menu-opening`, controls with `visibility: hidden` left out |
| `27691cb` | NV-13 (21 Oct, after landing): desktop sticky bar is the centred mobile card; desktop package removed |

R12c (Astra on `b69aa86`): resize cases pass; one regression, fixed in `3441bac`. Rendered with a temporary nested submenu injected into the drawer and reduced motion emulated (the test tab draws no frames, so Dawn's transitionend focus never runs otherwise): Back then immediate Tab → menu button while the closing panel is still `[open]`; Escape in the submenu then immediate Tab → menu button, `aria-expanded=false`; submenu loop Back ↔ Child B; settled states and root Escape correct; desktop-drawer 989 ↔ 990 and 393 flat cases unchanged.

R12b (Astra fix check on `c8acab1`): M1, F1, F2, F3, F5, F6 resolved; F4 partly, fixed in `b69aa86`. Rendered: desktop drawer simulated with a temporary style (no settings changed), opened at 989 → 990: Tab Members → Facebook, Instagram → menu button, Shift+Tab button → Instagram; shrunk to 989 open: Shift+Tab → Members, Tab → button, Escape closes with `aria-expanded=false`; saved dropdown at 393 unchanged; 989 → 990 close still moves focus to the logo. Submenus: none in the current menu, not tested.

Files: `sections/header.liquid`, `sections/header-group.json`, `snippets/product-header-css.liquid`, `snippets/sticky-cart-block.liquid`, `snippets/day-night-color-variables.liquid`, `locales/en.default.json`, `locales/nl.json`, `locales/fr.json`.

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

### Floating navigation (`b0c9fd2`), localhost 16197, Orca browser

- Theme Check `--fail-level error`: exit 0 (459 files, 0 errors, 21 pre-existing warnings).
- Homepage 393: nav fixed at the announcement bottom (30px), bar 42–90, no band (section background transparent), first section starts at 30 with 72px clearance, first content at 102; scrollY 15 → bar 27, 40/800/790 → 16. Hero background runs under the bar in Day and Night (`float-home-393-top.png`, `float-home-393-day-top.png`, `float-home-393-scrolled.png`).
- PDP 393: hidden at 11, 600, 591; back at 590 (bar 12–60); hidden again at 591; 3000 hidden with the sticky bar shown; top restored. Hidden bar bottom −28 (shadow clear).
- 750 / 990 / 1440, homepage and PDP: content starts where it did with the in-flow header (111 / 114 / 114); off the PDP the stuck bar is at 16; on the PDP hidden on scroll down, back at 12 (750) or 24 (990, 1440). No horizontal overflow.
- Mobile menu opened mid-PDP: nav stays (hidden class set, transform none), panel opaque `rgb(33,42,73)` (Night), body locked; Escape closes it, focus returns to the menu button, lock released (`float-pdp-393-menu-open.png`).
- Anchor (homepage, clock section): lands 24px under the bar.
- Resize 393 → 1440 → 393 without reload: clearance 72 → 86 → 72, bar 42–90 → 52–102 → 42–90.
- Collection, terms page and search at 393: first heading 33–39px under the bar.
- Not checked in a browser: reduced motion (CSS only), real overscroll bounce (JS clamp, R10 probe), theme editor section reload, keyboard Tab order through the bar.

### R12-NAV fixes, localhost 16197

- Theme Check `--fail-level error`: exit 0 before every commit.
- M1: at 1440 the bar sits 12px under the announcement bar (40), stuck at 16 off the PDP, revealed at 12 on the PDP; clearance 74.
- F1: with the script's values removed vs measured, homepage: 393 72/30, 750 72/39, 989 72/39, 990 74/28, 1440 74/28 (clearance/top), all equal.
- F3: announcement section removed: homepage 393/1440 bar at 16 at the top and after scrolling; PDP at 12.
- F2: mega-menu stylesheet and a 3000px panel injected at 1440×600: max-height 458px, overflow-y auto.
- F4: 393, keyboard: 30 focusables / 5 shown; Shift+Tab from the menu button → Members; Tab from Members → menu button; Escape closes, `aria-expanded=false`, focus on the button.
- F5: open at 989 with focus on a link, resize to 990: closed, `aria-expanded=false`, no scroll lock, focus on the logo, PDP hides on scroll; back at 989 still closed; 749 → 750 stays open.
- F6: clock heading and stat-strip section targets: 24px under the bar at 393 and 990.
- Regression pass after all fixes, Night, homepage and PDP at 393/750/990/1440: top 42/51/40/40, content 102/111/102/102, no horizontal overflow; off the PDP stuck at 16; PDP hidden on scroll down with the sticky bar shown, revealed at 12. Day at 393/1440: bar `rgba(255,255,255,0.9)`, text `rgb(25,31,56)`, no band. Reduced motion emulated: nav transition none.
- Delivery line rendered on `/`, `/nl`, `/fr`.

### NV-13 desktop sticky bar (`27691cb`), localhost 16197, Orca browser, Day

- Theme Check `--fail-level error`: exit 0. `theme_keys.py check --area sticky_cart`: 24 keys ok.
- Collapsed card: 1000, 1440 and 1920 all 448×114, centred (centre 500/720/960), 20px from the bottom, flex layout, no package; 393 unchanged (369×106, 12px from the edges).
- Trigger at 393/1000/1920: hidden with the first plan card 20px on screen, shown 5px past it.
- Open at 1440: card 448×528, panel stacked as on mobile, Change shown, bar CTA hidden, kit row shown, delivery line read back; closes back to 114.
- Screenshots: the Orca pane tiles its capture at this size, so none saved; geometry above read from the page.

## Cleanup check

- Removed in `a6000c4`: the `gallery` variable and its rule in `checkBuybox` (`git grep -n "gallery" snippets/sticky-cart-block.liquid`: no match).
- Removed in `1571898`: the `glass_bg_day` / `glass_bg_night` Liquid variables (`git grep -n glass_bg_ -- sections snippets`: no match) and the border rules from `e21ee67`.
- Removed in `640ada3` (Victor's go): header settings `bg_color_day`, `bg_color_night`, `product_bg_color_day`, `product_bg_color_night`, their CSS in `sections/header.liquid` and `snippets/product-header-css.liquid`, and their values in `sections/header-group.json`. `git grep -n "product_bg_color\|section.settings.bg_color_day\|section.settings.bg_color_night" -- sections snippets layout templates config assets`: only `sections/announcement-bar.liquid` (its own settings of the same name).
- Removed in `b0c9fd2`: `snippets/product-header-css.liquid` (with its `.scrolled-past-header` rule), `snippets/transparent-header.liquid` (`body.is-scrolled`), Dawn's `StickyHeader` and the inline PDP script, the `header_tag` switch, header settings `section_bg_color_*`, `product_section_bg_color_*`, `show_line_separator`, `margin_bottom` (schema and `header-group.json`), and the `data-kc-surface-edge` reader in `snippets/kc-surface.liquid`. `git grep` for each in sections, snippets, layout, templates, config, assets: only other sections' own settings of the same name (announcement bar `show_line_separator`, product-benefits and `templates/index.json` `section_bg_color_*`).
- Removed in `310bf26` once F2 replaced their last reader: `assets/base.css` `.shopify-section-header-sticky`, `.shopify-section-header-hidden(.menu-open)`, `.section-header.animate`, `.header-wrapper--border-bottom`; the `.header-wrapper--border-bottom` rule in `component-mega-menu.css`; `HeaderDrawer.borderOffset` in `assets/global.js`. `git grep` in assets, sections, snippets, layout: no match.
- Removed in `a2c13e5`: header setting `padding_top` (schema and `header-group.json`); `git grep settings.padding_top` in the header: no match.
- Removed in `27691cb`: the desktop package (`.sc-package*`, `.sc-kit*`, `.sc-kit-line`, the 1081px grid), the `data-sc-kit` / `kit-line` JS, block setting `kit_free` with its "Desktop package" header, `kc.sticky_cart.kit_free_html` in 31 locales and its `theme-keys.json` row. `git grep -e sc-package -e sc-kit -e kit_free_html -e '"kit_free"' -e data-sc-kit` outside `docs/`: no match. `snippets/kc-kit-value.liquid` stays (comparison table, featured product).

## Pending

- Astra review of this branch, requested from the coordinator (the orchestrator launches Astra).
- Merge into `karmicare/soft-launch-global`: the coordinator's worktree holds that branch.
- Brief phase 1 audit (D-12, drawer, desktop menus, Coming soon, current page): not started.
- Preview theme `189890265469` was created by this worker's first `shopify-preview.py dev` attempt (failed twice on "Premature close"); the landing desk now serves localhost 16197 from it.

## Handoffs

- `snippets/sticky-cart-block.liquid`, `locales/en.default.json` (PDP lane) and `snippets/day-night-color-variables.liquid` (tokens) are outside this brief's file list; changed at Victor's direct request. Tell their owners before merging.
- `assets/kc-tokens.css`: `--kc-brand-glass-bg-light` (0.9), `-bg-dark` (0.85), `-border-light` (white 0.4) lag the library (0.93, 0.93, `rgba(25,31,56,0.15)`). Generated file; the generator `docs/design-tokens/generate.py` is no longer in the repo. No theme file reads these names today.
- Delivery times: the new line (24 h Benelux, 3 days rest of Europe) differs from `templates/page.consumer-rights.json` and Terms (1–3 working days Benelux, 2–5 rest of the EU). Legal/content owner.
- `assets/kc-gallery.js`: the desktop gallery sticks below the header height; with the nav away there is a band above it. Left as is because the nav comes back on scroll up.

## Open decisions for Victor

None open. Settled on 20 Oct: unused bar colour settings removed (`640ada3`); NL/FR delivery line translated by this worker at Victor's request (`756a668`), not by a translator.
