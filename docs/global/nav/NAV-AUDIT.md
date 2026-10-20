# Navigation behaviour: audit rows (global lane, nav child)

Branch `karmicare/soft-launch-global-nav` (from `karmicare/soft-launch-global` @ `1c01dc5`). Task `task_cd7f661028f8`, run `run_32dd5602b983`.

The phase 1 audit of the brief (D-12 options, drawer, desktop menus, Coming soon, current page) has not been written yet. Before it, Victor gave direct instructions in this terminal on 20 Oct 2026. The landing desk put those in scope ("record them as NV rows"). Each row below is one of them, built and committed.

| Id | Behaviour | Before | Now | Source | Commit |
|---|---|---|---|---|---|
| NV-01 | PDP nav hide on scroll | `.section-header` always `position: sticky` on every page (`sections/header.liquid` ~L43) | Product pages only: shown on landing; slides up (0.3s) as soon as the page scrolls down; slides back from the top after 0.15s once the visitor scrolls up 10px; always shown within 10px of the top. It stays while a menu is open or keyboard focus is inside it. Reduced motion: no transition. Without JS the bar stays sticky. Looked up by section id on every update, so a theme editor or theme dev section swap keeps it working. | Victor, 20 Oct | `734b62e`, `1571898`, `1a475df` |
| NV-02 | Sticky buy bar trigger | Shown after the buybox CTA, and from 750px only after the sticky gallery column, had left the screen | Shown once the first plan card on screen (Loop's first `.loop-subscription-group` in the buybox) is above the screen; products without plan cards still use the buybox CTA. Other rules unchanged (ready, no other begin section on screen). | Victor, 20 Oct | `a6000c4` |
| NV-03 | Sticky bar delivery line (EN) | "Free delivery · 1–3 working days in Benelux" | "Free Fast Delivery: 24 hours in Benelux. 3 days in rest of Europe" (Victor's copy) | Victor, 20 Oct | `a6000c4` |
| NV-04 | Glass token values | `surface/glass/default` 0.8 Day/Night; `border/glass/border` Day white 0.4 (invisible on cream) | Library values: surface 0.93 Day/Night; border Day `rgba(25,31,56,0.15)`, Night unchanged | KC Brand Design Library `gcWcgYxS1nmheciKYOjOGx`, read 20 Oct | `e21ee67` |
| NV-05 | Nav surface | Bar colour from section settings (`bg_color_*`, `product_bg_color_*`) at the glass opacity | Library `surface/secondary/default` (Day `#ffffff`, Night `#212a49`) via `--kc-mapped-surface-page-secondary-rgb` at the glass opacity setting (90%), blur setting behind it, opaque with the open mobile menu. No border (a border was added in `e21ee67` and removed in `1571898` at Victor's request). | Victor, 20 Oct | `1571898`, `f46d511` |
| NV-06 | Nav shadow | none | `--kc-elevation-md` | Victor, 20 Oct | `1a475df` |
| NV-07 | Mobile logo size | 105px (Figma PDP V15 node 4023:29024) | `clamp(105px, 100vw - 250px, 140px)`: 140 from 390px, 110 at 360 | Victor, 20 Oct | `1571898` |
| NV-08 | Mobile bar offset | 4px below the announcement bar (Figma 2766:10918) | 12px | Victor, 20 Oct | `de58e27` |
| NV-09 | Stuck offset off the PDP | Sticky at the bar's own margin (12px mobile, 24px desktop) | 16px from the top edge after scrolling, every page but the PDP | Victor, 20 Oct | `60c91b6` |
| NV-10 | Floating navigation | Header section in the page flow, sticky, painting a full-width band (`section_bg_color_*`, `product_section_bg_color_*`) | Fixed and transparent; only the compact bar paints and takes clicks; it starts at the announcement bar's bottom and floors at NV-09 (16px) or 0 on the PDP; the first `#MainContent` section owns its background under the bar and gets the measured bar height as top padding. One controller (`assets/kc-navigation.js`) replaces Dawn's StickyHeader and the inline PDP script with the same NV-01 thresholds. Band settings, `show_line_separator`, `margin_bottom`, `product-header-css` and `transparent-header` removed; `sticky_header_type` none → always. | Victor, 20 Oct (draft by the R10 review session, adapted) | `b0c9fd2` |

## Still to audit (brief phase 1)

D-12 sticky header options for non-product pages, mobile drawer (focus trap, Escape, scroll lock, link tap, breakpoint), desktop menus, Coming soon items, current-page state on `/nl` and `/fr`. Not started.
