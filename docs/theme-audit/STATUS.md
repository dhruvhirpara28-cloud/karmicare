# Theme audit: status and recommended order of work

**Audit**: 9 October 2026 on `3febb1a` (then the tip of `main`, `DH/Development` and `mearchant-edit`). Static review of the whole theme, `shopify theme check`, a file-by-file diff against a clean Dawn 15.5.0, and live fetches of karmicares.myshopify.com. Three delegated reviews (Liquid, JavaScript, performance) are compiled in [AUDIT.md](AUDIT.md).
**Re-checked**: 19 October 2026 08:20 UTC on `mearchant-edit` `d95d9c4`. Live theme karmicare/main is `origin/main` `c5f6cd8` (17 Oct), 19 commits behind `mearchant-edit`, 0 ahead.
**Contract for pick-up**: `AGENTS.md`. No push, no PR, no merge, no admin writes. `config/settings_data.json` and the Loop widget files (`assets/loop-widget.js`, `assets/loop-widget.css`, `snippets/loop-widget*.liquid`) are off-limits. Brand rules for copy. Token contract. `shopify theme check --fail-level error` must exit 0.
**Written by**: Claude Code (Victor's main checkout, session c5e4f316). This folder is untracked in the main checkout; copy or commit it into the task worktree.

## Where things stand

| # | Finding (9 Oct) | Severity | `mearchant-edit` d95d9c4 (19 Oct) | Live `main` c5f6cd8 |
|---|---|---|---|---|
| 1 | Hero inline script is a SyntaxError: homepage live clock and Awake/Asleep pill dead | High | Fixed. `sections/hero-karmicare.liquid:380-397` is a clean clock-only script; the duplicate Day/Night handler is gone | Fixed |
| 2 | ipinfo.io and api.sunrisesunset.io geolocate every visitor, no consent, not in the privacy policy | High (GDPR) | Fixed. Day/Night is computed locally: `assets/day-night-sun.js` inlined at `layout/theme.liquid:38`; `assets/day-night-mode.js` makes no external calls | Fixed in code. DH's `f1240f2` (17 Oct, "change") reformatted `layout/theme.liquid`; the restore `120a840` is on `mearchant-edit` only. Verify Day/Night behaviour on the live site before closing |
| 3 | Footer Instagram and Facebook icons swapped; LinkedIn always links to `#` | High | Fixed (`config/settings_schema.json:1922`, `sections/footer.liquid:706-760`) | Fixed |
| 4 | Welcome Kit free product and discount code `Welcome Kit` enforced client-side only | High (revenue) | Open. `snippets/welcome-kit.liquid:34,68` still hardcodes the code; `assets/karmi-add-to-cart.js` still redirects to `/checkout?discount=Welcome%20Kit`. The cart sync was reworked on 16 Oct (Astra rounds 1-7) but still monkeypatches `window.fetch` (`welcome-kit.liquid:148`) and clears every discount code with `discount: ''` (`:110`) | Open. Shopify admin discount rules were never verified (Victor only) |
| 5 | Store served on karmicares.myshopify.com; checkout.karmicare.com returns a 301 to it; canonical and hreflang point at the myshopify domain | Decision | Deferred by Victor on 16 Oct: revisit at the website migration, not in theme work. Shop Pay redirect stays | n/a |
| 6 | Fonts double-loaded: Montserrat `font_face` and two preloads, then overridden by Typekit Proxima Nova (render-blocking); Gotham Rounded as four TTF faces; three woff2 files in `assets/` unused | Medium (perf) | Open (`layout/theme.liquid:100-104, 389, 400-421, 452-457`) | Open |
| 7 | `loop-widget.js` (145 KB) and `karmi-add-to-cart.js` load on collection pages that have no subscription UI | Medium (perf) | Open (`layout/theme.liquid:74-87`) | Open |
| 8 | About 80 KB of inline CSS and JS per page in Liquid instead of cacheable assets; product HTML 690 KB, home 437 KB | Medium (perf) | Open. Live on 19 Oct: product HTML 769 KB, home 504 KB | Open |
| 9 | Orb images 232 KB for a 440 px slot; four sections lack `widths`/`sizes` | Low (perf) | Open | Open |
| 10 | Dead files: 44 Dawn `icon-*.svg`, `gotham-rounded-medium.woff2`, `proxima-nova-medium.woff2`, `proxima-nova-regular.woff2`, `component-progress-bar.css`, snippets `customer-portal-link-v2`, `loop_loader`, `loop-widget.css`; `sparkle.gif` (179 KB) is referenced only by a CSS variable nothing consumes | Low | Open. `sections/footer.liquid.backup` and `professional-testimonials.css` are gone | Open |
| 11 | `assets/loop-widget.js` is a fork with about 650 lines of Karmicare code and no version marker, so Loop updates cannot be applied | Medium (maint) | Open, and now off-limits under `AGENTS.md` §2. Needs Victor's decision | Open |
| 12 | Copy-paste: the drag-scroll script in 3 sections, slider boilerplate in 5, add-to-cart wiring in 3 places, "Subscription Name" computed in 3 places, journey markup duplicated | Medium (maint) | Open (not re-measured) | Open |
| 13 | Schema hygiene: about 20 dead or undeclared settings; `featured-product` reads block settings that do not exist; product-only sections addable on any template; Hinglish merchant-facing `info` text | Medium | Open (not re-measured) | Open |
| 14 | About 30 hardcoded English UI strings in custom Liquid while the store serves en, fr and nl | Medium (i18n) | Open | Open |
| 15 | Accessibility: click-only tooltips, FAQ filters and sticky-cart plan picker; heading levels chosen for styling; two `<main>` landmarks on legal pages | Medium | Open. The sticky bar was rebuilt on 18 Oct (`karmicare/pdp-sticky-bar`); re-review it rather than the audit's line numbers | Open |
| 16 | Scaffolding: no README, `.gitignore`, Theme Check config or CI; a 1 MB theme zip in git history; commit messages "change" and "Pull to main" | Low | Mostly fixed: `.gitignore`, `.theme-check.yml`, `AGENTS.md`, `.github/workflows/theme-check.yml`. README and `docs/` live on task branches and are stripped at landing | DH still commits "change" directly to `main` (`f1240f2`) |
| 17 | Theme Check | 20 errors, 23 warnings | 0 errors (baseline ignores), 21 warnings | Not run |

The Theme Check `MissingTemplate` error on `render 'loop-widget.css.liquid'` is a false positive: the live page renders that 20 KB style block. It stays baselined in `.theme-check.yml`.

## Recommended order of work

### A. Close out now: small, independent, one worker each

1. **Welcome Kit enforcement** (Victor, admin only, no code). Confirm the "Welcome Kit" discount is a Buy X Get Y rule where X is the bundle products with purchase type subscription and Y is the kit variants, quantity 1 at 100%, one use per customer, not combinable. Confirm the `FREE WELCOME KIT RECEIVED` tag is set by Flow or the app, not by the theme. Record the result here. Until then, treat the kit as unprotected.
2. **Welcome-kit sync hardening** (worker, theme code only). Replace the `window.fetch` patch with a subscription to Dawn's `PUB_SUB_EVENTS.cartUpdate`. Rebuild the discount list from `cart.discount_codes` minus `Welcome Kit` instead of sending `discount: ''`. Trust only responses that carry `token` and `item_count`, otherwise fetch `/cart.js`. Check `response.ok` and back off after a failure. Queue a re-run instead of dropping a concurrent sync. Leave the Loop files untouched. Reviewer runs a cart smoke test on the dev theme, no payment.
3. **Verify Day/Night on live**. Confirm `f1240f2` did not break the inlined `day-night-sun.js` on karmicare/main. If it did, DH lands `120a840`.
4. **Dead files**. Delete the row 10 list with `git grep` proof per file (cleanup-check rule). While there, fix `assets/base.css:30`, where the Nunito Regular TTF fallback points at the Medium file.

### B. Performance package: one worker, one branch, measured before and after on the dev theme

5. Fonts. Remove the Montserrat `font_face` lines and preloads, or set the type settings to system fonts. Self-host Proxima Nova from the woff2 already in `assets/` if the Adobe licence allows; otherwise keep Typekit and add `preconnect`. Serve Gotham Rounded as woff2.
6. Load `loop-widget.js` and `karmi-add-to-cart.js` only where a Loop container exists (product, plus index for featured-product). Make the cart-drawer CSS bundle and `loop-widget.css` non-blocking.
7. Move the large inline blocks into assets, keeping only setting-driven rules inline: header 9 KB, footer 8 KB, hero 6.5 KB, stat-strip 4.8 KB, km-faq 4.3 KB, button-styles 4.2 KB, sticky-cart JS 14.6 KB, welcome-kit JS 6.3 KB.
8. Images. Resize the orbs to about 880 px. Add `widths` and `sizes` to product-benefits, research-behind-system and trusted-professionals.

### C. Structural: needs Victor's decisions first

9. **Loop fork.** Decide whether Karmicare code may be split out of `assets/loop-widget.js` into a separate hook file. `AGENTS.md` §2 currently forbids touching it. Without this, every Loop update is a manual merge.
10. Consolidate the duplicated scripts (row 12) and prune the schemas (row 13). Fix the `featured-product` settings that are read but never declared.
11. Translation keys for the hardcoded strings (row 14), then fr and nl values.
12. Accessibility pass (row 15).
13. Process. Move the repo to a company-owned GitHub org. Stop code edits in the admin code editor (they arrive as bot commits on `.liquid` files). Require PRs with Theme Check for `main`.

## How to pick this up

- Create the task worktree from `mearchant-edit`, following the pattern in `docs/analytics/CONTEXT.md` on `karmicare/analytics`:

  ```sh
  orca worktree create --repo path:/Users/iamvictorious/IdeaProjects/karmicare-shopify-theme --name theme-audit --base-branch mearchant-edit --parent-worktree branch:mearchant-edit --setup skip --json
  ```

  Then copy `docs/theme-audit/` from this checkout into the worktree and commit it there.
- One dev theme and one port per worktree (see `README.md` on the task branches). Never type into checkout.
- Line numbers in AUDIT.md are from `3febb1a`. 133 files changed since, so re-locate before editing.
- Reviewer brief pattern: `/Users/iamvictorious/IdeaProjects/orca-workspaces/karmicare-shopify-theme/pdp-mobile/.coordinator/astra-pdp-mobile.md`.
- Figures for the architecture map (`docs/architecture/README.md` on `karmicare/buybox`) were measured on 11 Oct and still describe the Day/Night mechanism as ipinfo-based. That row is stale.

## Not covered by the audit

Shopify admin configuration (discounts, Flow, Loop), app-managed settings and pixels, Lighthouse or real-device performance, the Webflow site at www.karmicare.com, and checkout.
