# Theme audit, 9 October 2026: compiled findings

Measured on `3febb1a`. Line numbers refer to that commit; see [STATUS.md](STATUS.md) for what has changed since. Severity: High = visible breakage, revenue or compliance exposure; Medium = wrong under realistic conditions, or real maintenance cost; Low = hygiene.

## 1. Method

- Whole-tree static review by three delegated reviewers (custom Liquid, JavaScript, performance and assets), each verifying claims by reading code; `node --check` on inline scripts.
- `shopify theme check -o json`: 20 errors (19 `MatchingTranslations` in schema locales for the `gallery_layout.options__5.label` key, 1 `MissingTemplate`), 23 warnings (`OrphanedSnippet` ×4, `UnusedAssign` ×4, `UndefinedObject` ×4, `RemoteAsset` ×3, `LiquidNestingDepth` ×3, `LiquidComplexity` ×2, `VariableName` ×2, `HardcodedRoutes` ×1).
- Diff against a clean Dawn 15.5.0 tarball.
- Live fetches of karmicares.myshopify.com (home, product, collection) with every stylesheet, script, font and inline block counted.
- All JSON (78 files) valid; every `| t` key used exists in `en.default.json`; no custom translation keys were ever added.

## 2. Fork profile against Dawn 15.5.0

| | identical | modified | new |
|---|---|---|---|
| assets | 172 | 19 | 37 |
| sections | 47 | 8 | 14 |
| snippets | 33 | 6 | 21 |
| templates | 0 | 20 | 4 |
| layout | 0 | 2 | 0 |
| config | 0 | 2 | 0 |
| locales | 0 | 51 | 0 |

No Dawn file was deleted. Largest divergences: `sections/main-product.liquid` 2326 to 3410 lines (+1089), `sections/footer.liquid` +713/-422, `sections/featured-product.liquid` +583, `sections/header.liquid` +493/-137, `assets/section-main-product.css` +491, `config/settings_schema.json` +728, `layout/theme.liquid` +188.

## 3. Live measurements (9 Oct, karmicare/main)

| Page | HTML | Stylesheets | Scripts (src) | Inline scripts | Inline styles | Inline SVG |
|---|---|---|---|---|---|---|
| Home | 437 KB | 41 | 36 | 50 (122 KB) | 24 (80 KB) | |
| Product | 690 KB | 56 | 41 | 56 (170 KB) | 28 (77 KB) | 167 blocks, 125 KB |
| Collection | 362 KB | 37 | 31 | 38 | 16 | |

Largest inline blocks on the product page: Judge.me settings 32 KB, Shopify web pixels loader 20 KB, Loop product JSON 16 KB twice, sticky-cart script 14 KB, Loop CSS 19 KB, Montserrat font faces 14 KB. Fonts per page: Montserrat n4/n6 (declared and preloaded, never used), Proxima Nova via Typekit (render-blocking), Nunito 400/500/700 from `base.css`, Gotham Rounded as four TTF faces, JudgemeStar. App embeds seen: Loop Subscriptions, Judge.me. Images: home 72 `<img>`, 0 without alt; product 116, 3 without alt.

## 4. Liquid findings (custom sections and snippets)

### High
1. `sections/hero-karmicare.liquid:303-316`. Inline script is a SyntaxError: a formatter merged `//` comments with code and `{{- section.id -}}` collapsed three lines into one comment. The live clock and the Awake/Asleep pill never ran. Fixed since.
2. `sections/footer.liquid:389-426`. Instagram link renders the Facebook path and vice versa. Fixed since.
3. `sections/footer.liquid:427-431`. `settings.social_linkedin_link` not declared in `config/settings_schema.json`, so the LinkedIn icon always links to `#`. Fixed since.

### Medium
4. `snippets/welcome-kit.liquid:35,39`, `snippets/custom-button-script.liquid:20`, `snippets/sticky-cart-block.liquid:576`: discount code `Welcome Kit` and tag `FREE WELCOME KIT RECEIVED` hardcoded in four places. Make them theme settings next to `enable_welcome_kit`.
5. `sections/featured-product.liquid:164-212` reads `loop_block.settings.try_once_text`, `try_once_shipping`, `try_once_note` and `pricing_summary_*`, none declared in its `loop_subscriptions` block schema, so they are always blank.
6. `sections/featured-product.liquid:529-535,562,572,581`: business constants hardcoded (care credit `times: 0.1`, `divided_by: 120.0` brushings, `/ 60 days`, `/ year`, `Free`, `#78b5fa`). Read from the `duos_count` metaobject or block settings.
7. `sections/product-benefits-karmicare.liquid:130,219`: `<slider-component>` opens under `show_slider` but closes only under `show_slider and show_slider_arrows`; with arrows off (as on the homepage) the element is never closed.
8. `sections/how-it-works-steps.liquid:56`: `{% if blocks.size != 0 %}` uses an undefined `blocks`, always truthy. Use `section.blocks.size`.
9. `sections/how-it-works-steps.liquid:165,190`, schema 575-601: step number output as `<h2>`, title hardcoded `<h4>`, while `heading_tag`/`heading_size` are declared and never read; `text_color_day/night` and `card_bg_color_day` (517-536) unused.
10. `sections/how-it-works-steps.liquid:172-178`: Figma-exported SVG with `foreignObject`, `data-figma-bg-blur-radius` and a fixed `id="bgblur_0_4002_231_clip_path"` repeated per card (duplicate IDs).
11. `sections/how-it-works-steps.liquid:1-8,297-307,569` and `sections/km-faq-accordion.liquid:4`: Hinglish and Gujarati comments; line 569 is merchant-facing schema `info`.
12. `sections/comparison-table.liquid:79`, `sections/product-compare-plans.liquid:2`: depend on `product.metafields` but have presets without `enabled_on: {"templates": ["product"]}`.
13. `sections/comparison-table.liquid:125-203`: table built from `<div>`s, no `<table>` or `<th scope>`.
14. `sections/product-compare-plans.liquid:43,52` vs schema 376-379: label promises a metaobject-title fallback that does not exist.
15. `sections/product-compare-plans.liquid:179-190`: scans all `shop.metaobjects.compare_value.values` for every plan by row cell (cubic). Build a lookup once.
16. Tooltips at `sections/product-compare-plans.liquid:136-145,211-220` and `sections/main-product.liquid:185-203` (CSS `product-compare-plans.css:226`, `section-main-product.css:1799`): trigger is a non-focusable `<span>`, icon `aria-hidden`, popover on hover or click only. Use `<button type="button" aria-describedby>` and `:focus-within`.
17. `sections/km-faq-accordion.liquid:173-177,229-257`: filter buttons are `<span>`s with no role, tabindex or `aria-pressed`; the script queries the whole document, so two instances cross-filter.
18. `sections/policy-banner.liquid:98`: always emits `<h1>`, duplicating the page heading.
19. `sections/legal-toc-section.liquid:186,198`: `<main>` inside a section while `layout/theme.liquid:492` already has `<main id="MainContent">`; article titles are `<h5>`.
20. `sections/header.liquid:258-264`: with `bg_color_night` set, every `.header__icon` svg and path takes the header background colour, so cart, account and search icons vanish in night mode. Latent: the setting is empty on live.
21. `sections/header.liquid:866-903`: `btn_bg_day`, `btn_text_day`, `btn_bg_night`, `btn_text_night` declared, never used.
22. `sections/footer.liquid:366-376`: newsletter `{% form 'customer' %}` has no `form.errors` or `form.posted_successfully?` feedback.
23. `sections/footer.liquid:484,550`: country flags fetched from flagcdn.com (third party, outage and privacy surface). Self-host or drop.
24. `sections/footer.liquid:365-380,512,536`: hardcoded "Email", "Join", "Language", "Country/Region" and a literal `/policies/terms-of-service` path. Use `shop.terms_of_service.url` and the existing locale keys.
25. `sections/main-product.liquid:620-631`: the Loop widget snippet is rendered twice (once captured to test a sentinel string that is always true).
26. `sections/main-product.liquid` schema: `default_to_subscription` copied onto the section and six block types where nothing reads it; sticky_cart `show_variants`/`show_subscriptions` (969-979) and info_card `border_color` (1041) unused; highlights `font_size_mobile`/`border_radius` (1108-1127) write CSS variables no rule consumes.
27. `snippets/professional-testimonials.liquid:43` uses undeclared `block.settings.heading_color_day`; the block schema (main-product 2943-3160) declares `show_border_*`, `bg_color_night`, `subheading`, `heading_bold_opacity`, `bottom_text`, `button_*`, `padding_*` that the snippet never reads.
28. `snippets/product-highlights.liquid:160-162,75`: marquee clone lacks `aria-hidden="true"`; `height: 1.4;` missing unit.
29. `snippets/mission-card.liquid:46-76`: design-mode placeholder sits inside `{% if mission_card != blank %}`, so it never shows when empty and duplicates the card when filled.
30. `snippets/sticky-cart-block.liquid:7-29` vs `70-102`, `158-223`, `274`, `321-338`, `185`, `229`: bundle detection computed twice; `role="listbox"/"option"` on click-only `<div>`s; `€` and reward strings hardcoded in JS; Loop app id `5284869` hardcoded (also `loop-widget-standard.liquid:144`); `action="/cart/add"` instead of `routes.cart_add_url`. The sticky bar was rebuilt on 18 Oct; re-review.
31. `snippets/welcome-kit.liquid:150-171`: global `window.fetch` monkeypatch; header detection misses `Headers` instances.
32. `snippets/loop-widget-standard.liquid:1-7,95-99,212,216-247,268-274`: header says "DO NOT modify, auto-generated" but carries Karmicare customisations; `data-position="{{ option.position }}"` references an undefined `option`.
33. `snippets/treatment-journey.liquid:15-99` vs `101-188`, `251-263`, `80,169`: journey markup copy-pasted (~85 lines); global click and change listeners plus 500 ms polling; toggles lack `aria-expanded` and `type="button"`.
34. Copy-pasted drag-scroll script: `product-benefits-karmicare.liquid:236-270`, `trusted-professionals.liquid:205-240`, `research-behind-system.liquid:207-242` (the benefits copy lacks the `scrollWidth` guard); `slider_classes`/`show_slider` boilerplate repeated in five files.
35. Large inline CSS: `km-faq-accordion.liquid:6-149`, `policy-banner.liquid:1-83,158-296`, `legal-toc-section.liquid:1-142,230-558`, `footer.liquid:8-322` (~300 lines while `section-footer.css` is already loaded); commented-out CSS at legal-toc 276-279, 301-310 and policy-banner 44-51.
36. `sections/two-formulas-karmicare.liquid:154`: `alt: section.settings.heading` passes inline rich text that may contain `<strong>`. Add `| strip_html | escape`.
37. `sections/chronobiology-clock-karmicare.liquid:179-181`: absolute, locale-pinned fallback URL `https://karmicare.com/en/why-karmicare` with `target="_blank"` on an internal link.

### Low
38. `hero-karmicare.liquid:144` `accessibility_label` undeclared; 442-450 `heading_size` unused; 273 whitespace inside `datetime`.
39. Hardcoded English UI strings: hero 237; stat-strip 93; chronobiology 112-113, 123, 128, 166; km-faq 173 "ALL"; product-compare-plans 60, 103, 105, 194, 201, 235; legal-toc 225; main-product 165 "Or"; loop-widget-standard 95-98, 104, 118, 135 ("Choose your supply", "Continue", "each", "One time Purchase", "Selling Plans"); loop-subscriptions 29; sticky-cart 138, 166, 173; treatment-journey 20, 106.
40. Heading hierarchy: product-benefits 160 `<h5>`, trusted-professionals 132 `<h5>`, chronobiology 139/151 `<h4>` directly under h2, testimonials 82 `<h6>`, treatment-journey 19/105 `<h5>`, footer 333/337/345 headings used for styling.
41. Checkbox tested with `!= blank` (product-benefits 7/228, trusted-professionals 8/196, research 4/198); works only because `false == blank`.
42. Prefix soup: `kc-`, `km-`, `karmicare__`, `karmi`, `pc-`, `sc-`, `ft-`, `figma-tryonce v9bb` (main-product 161).
43. Figma leftovers: header 176-191 comments; how-it-works 172; footer `clip0_2906_*` ids.
44. Hardcoded colours and fonts bypassing settings: header 197 `#C4DFFF`; policy-banner 175, 214; legal-toc 261, 287 `'Gotham Rounded'`; footer SVG `fill="#191F38"` (397, 416, 438) not night-aware.
45. `product-faq.liquid:11` native `name="faq-accordion"` duplicated by JS 34-50.
46. `product-compare-plans.liquid:178` `assign ... = null` (use `nil`); comparison-table 79/84 double assign, 151 `class=""`.
47. `day-night-color-variables.liquid:36,49` `--color-background-contrast` uses background channels, so no contrast.
48. Typos and stale defaults: "Policy Bannner" (policy-banner 300, 452), "ENTHOUSIASTS" (stat-strip 185), "Last updated October 2026" plus a legal entity in a schema default (policy-banner 324).
49. trusted-professionals quote only on `:hover` (`section-trusted-professionals.css:178,200`), no keyboard or touch path.
50. No `disabled_on`/`enabled_on`: two-formulas, product-benefits, trusted-professionals, research, km-faq, how-it-works, comparison-table, product-compare-plans, policy-banner, legal-toc; policy-banner lacks `tag`/`class`.
51. `loop-subscriptions.liquid:25-30` `<button>` nested in `<a>`; footer 479 inline `onclick`; footer line 1 `theme-check-disable`.
52. Polling to sync with the Loop DOM: main-product 632-664 (100 ms × 50), treatment-journey 257-263, sticky-cart 495, loop-widget-standard 307.

Security: no `request.*` values or URL parameters reach HTML or JS; visible settings are escaped; JSON uses `| json`. Residual risk is merchant-controlled raw CSS and HTML settings only.

## 5. JavaScript findings

### High
- H1. Hero inline script SyntaxError (same as Liquid 1). Fixed since.
- H2. Welcome Kit enforced only client-side. `snippets/welcome-kit.liquid:35` hardcodes the code; `assets/karmi-add-to-cart.js:84` redirects to `/checkout?discount=Welcome%20Kit`; `_welcome_kit` (`karmi-add-to-cart.js:57`, `welcome-kit.liquid:115`) is an ordinary line-item property anyone can set; the "already received" check is a customer-tag test that only gates auto-add (`welcome-kit.liquid:39`); `snippets/cart-drawer.liquid` has no `_welcome_kit` handling, so the free line's quantity can be raised. A customer can enter the code manually, remove the subscription after checkout starts (sync runs only on storefront `/cart/*` fetches), or add kit plus code without any subscription. Server side must enforce: a Buy X Get Y discount (X = bundle products, purchase type subscription; Y = kit, qty 1, 100% off), one use per customer, not combinable; the tag set by Flow or the app.
- H3. `assets/day-night-mode.js:98,82`: IP geolocation of every visitor via ipinfo.io, then sunrisesunset.io, with no consent gating and a "WEBFLOW CUSTOM CODE" header. Fixed since.

### Medium
- M1. `welcome-kit.liquid:163-164`: `/cart/add.js` response misread as the full cart (multi-item adds return only `{items: [added]}`); Loop's own add path (`loop-widget.js:3879-3884`) hits this, so `hasBundleSubscription` and the "already in cart" check see only the just-added lines: duplicate kit or skipped removal.
- M2. `welcome-kit.liquid:96-104`: removal path sends `discount: ''`, clearing every discount code in the cart, including customer-entered ones. Still present at `:110` on 19 Oct.
- M3. `welcome-kit.liquid:42-53,55-63,96` and `karmi-add-to-cart.js:89`: no `response.ok` checks; an unavailable kit variant (422) fails silently and every later cart mutation retries the POST plus discount call.
- M4. `welcome-kit.liquid:65-67`: `isUpdating` drops concurrent calls instead of queuing, so removing the subscription mid-sync leaves the kit.
- M5. `welcome-kit.liquid:149-170`: global `window.fetch` monkeypatch on every page; header detection reads a plain object only and `URL` objects yield `''`. Still present at `:148` on 19 Oct. Subscribe to `PUB_SUB_EVENTS.cartUpdate` instead.
- M6. `karmi-add-to-cart.js:49`: duplicate guard is DOM-based (`cart-drawer [data-variant-id]`); a stale drawer, the notification cart preset or another tab produces a duplicate free line. Fetch `/cart.js` before building `items`.
- M7. Fragile plan detection by text: `karmi-add-to-cart.js:19,28,71` matches `'one time'` and falls back to the first `input[name="selling_plan"]` on the page; `product-compare-plans.liquid:266-300` picks a Loop radio by fuzzy word scoring; `treatment-journey.liquid:236` keys on `name.includes('year')`. Renaming a plan in Loop silently changes behaviour. Key off `data-id === 'loop-one-time-purchase'` and selling-plan IDs emitted by Liquid.
- M8. `sticky-cart-block.liquid:505-509`: MutationObserver on the whole Loop fieldset (`subtree`, `characterData`, `childList`, `attributes`) runs `syncFromLoop` unthrottled; `:494-497` polls every 300 ms forever when no fieldset exists; `:542-543` scroll handler does `getBoundingClientRect` plus style writes per event. Rebuilt 18 Oct; re-review.
- M9. Three competing "default plan" pollers: `main-product.liquid:634-662` (100 ms × 50, re-dispatches `change` so every handler runs twice), `featured-product.liquid:614-640` and `:853-857` (200 ms forever when no Loop container), sticky `:637-651`.
- M10. Every-page cost: `welcome-kit.liquid:173` fires `GET /cart.js` on every DOMContentLoaded; `:176-182` two more fetches on back navigation; `theme.liquid:72-80` loads `loop-widget.js` plus `karmi-add-to-cart.js` on `collection` though `templates/collection.json` has `quick_add: none` and no Loop block.
- M11. `theme.liquid:559` loaded `day-night-mode.js` deferred at the end of body, so night-mode users got a flash. Superseded by the inline `day-night-sun.js` in the head.
- M12. `assets/loop-widget.js` is a fork, not vendor code: no version marker; `APP_ID = "5284869"` (`:3`); about 650 lines of "KC CUSTOM" (`:78-125` testimonials, `:1853-1870` Subscription Name attribute, `:2059-2750` welcome-kit popup, kc-pricing-summary, kc-try-once, kc-plan-subrow, `:3782`) across 13 commits from 7 Aug to 6 Oct. Endpoints: `cdn.loopwork.co/{shop}`, `d217z8zw4dqir.cloudfront.net/{shop}.json`, `apiv2.loopwork.co/bundleStorefront/*`, `api.loopwork.co/api/merchant/sellingPlanGroups/*`, `api-service.loopwork.co/bundleTransaction`. 36 `innerHTML` writes including unescaped product title and URL template strings (`:2186-2200, 2224`); 18 unconditional `console.log` via `widgetLogger` (`:118-123`). Vendor updates cannot be applied. Now off-limits under `AGENTS.md`.

### Low
- L1. `karmi-add-to-cart.js:72` sends `attributes` in a `/cart/add.js` body (undocumented; attributes belong to `/cart/update.js`).
- L2. Listener leaks on theme-editor re-render: `sticky-cart-block.liquid:542-543,625-627`, `treatment-journey.liquid:253-254`, `product-compare-plans.liquid:347`, `chronobiology-clock-karmicare.js:48-52` (body observer never disconnected); `km-faq-accordion.liquid:230` and `product-compare-plans.liquid:249` bind on `DOMContentLoaded` so never re-init on `shopify:section:load`.
- L3. `day-night-mode.js:51,122,144-145` bare `localStorage` writes without try/catch. Superseded.
- L4. Hygiene: `product-info.js:133` `console.log`; `cart:refresh` dispatched (`welcome-kit.liquid:135`) with no listener; unused `hasChanges` (sticky `:473-489`) and a duplicate `welcome_kit_variant_id` block (sticky `:82-91` vs `:19-28`); `Shopify.formatMoney` (sticky `:271-275`) does not exist in Dawn so the hardcoded `€` fallback always runs; "Subscription Name" computed in three places (`loop-widget.js:1853`, `product-form.js:33-45`, `karmi-add-to-cart.js:65-74`); add-to-cart wiring in three places (`custom-button-script.liquid`, `sticky-cart-block.liquid`, `product-form.js`); globals `karmiAddToCart`, `refreshDawnCartUI`, `karmiWelcomeKitSync`, `loopWelcomeKitExpanded`. `theme-editor.js`, `global.js`, `cart.js`, `cart-drawer.js` carried no custom additions; `product-form.js:33-45` was the only modified Dawn core file. `standard-actions-override.js` is sound.

## 6. Performance and assets

### Payload per template (uncompressed, from `wc -c`)

| Page | External CSS | Inline `<style>` | External JS | Inline `<script>` |
|---|---|---|---|---|
| Global (every page) | 154 KB / 19 files | ~45 KB in `<head>` | 271 KB / 18 files (145 KB is `loop-widget.js` on index, product, collection) | |
| Home (`templates/index.json`) | 254 KB / 33 files | ~95 KB | 320 KB / 25 files | ~27 KB |
| Product (`templates/product.json`) | 256 KB / 32 files | ~74 KB | 310 KB / 25 files | ~37 KB |
| `product.subscription-item.json` | +31 KB | +~12 KB | +11 KB | +~14 KB |

Render-blocking in `<head>` (`layout/theme.liquid`): Typekit `https://use.typekit.net/kss0igj.css` (392, cross-origin, no preconnect), `base.css` 81 KB (433), `loop-widget.css` plain link (72), the cart-drawer bundle of five synchronous stylesheets (440-444), plus the inline `:root` block (88-389), Gotham `@font-face` (393-428), `day-night-color-variables` (431), `button-styles` (434) and `loop-widget.css.liquid` (436-438). No external libraries (no Swiper, GSAP or CDN scripts); the "Swiper slider version" comment in `how-it-works-steps.liquid:2` is stale. `section-main-product.css` (43 KB) is pulled onto the home page by `featured-product.liquid:20` for one CTA card (52 KB CSS plus 38 KB JS).

### Images
- Hero LCP (`hero-karmicare.liquid:207-221`): correct (`width: 1800`, `widths`, `sizes`, explicit dimensions, eager, `fetchpriority="high"`, preload).
- `product-benefits-karmicare.liquid:146`, `research-behind-system.liquid:159,165`, `trusted-professionals.liquid:118`: `image_url: width: 800/600` with no `widths`/`sizes`, so mobile downloads the full file.
- `chronobiology-clock-karmicare.liquid:86-94`: raw `<img>` of `orb-blue.webp` and `orb-white.webp`, 232 KB for a 440 px slot, on the home page and the subscription-item product template.
- Clock background at `two-formulas-karmicare.liquid:25/33` is a CSS `background-image` (1400/800 px), fetched eagerly below the fold.
- `sparkle.gif` (179 KB): only reference is `base.css:3332` `--sparkle: url('./sparkle.gif')`, consumed nowhere.

### Fonts
| Family | Source | Issue |
|---|---|---|
| Montserrat n4/n6 | Shopify `font_face` ×5 (theme.liquid 91-95) and two preloads (451, 456) | Overridden to `"proxima-nova"` at 394-399 because `enable_custom_font` is true; two preloaded woff2 never used |
| Proxima Nova | Typekit CSS (392) | Render-blocking, no preconnect; `proxima-nova-medium/regular.woff2` sit unused in `assets/` |
| Nunito 400/500/700 | `base.css:6-33` | Regular face's TTF fallback points at `Nunito-Medium.ttf` (`base.css:30`) |
| Gotham Rounded 300/400/500/700 | four TTF `@font-face` (theme.liquid 400-427) | TTF is about twice woff2; `gotham-rounded-medium.woff2` unused; fetched only on legal pages |

### CSS
`base.css` is 3,628 lines / 81 KB, about 93% stock Dawn; custom additions are about 5.6 KB (Nunito block, `--kc-*` letter-spacing, a tail at 3454-3628 that duplicates `component-progress-bar.css`). The real custom CSS lives in inline `{% style %}` blocks (~80 KB per page). `!important`: 46 in assets, 20 in Liquid. Day/Night: 146 `.day-mode` and 221 `.night-mode` selector occurrences across 20+ files, each section exposing its own `*_color_day/_night` settings; no token layer at the time (the `kc-tokens.css` pipeline has since landed).

### Third-party origins
Typekit (all pages), `cdn.shopify.com/storefront/standard-events.js` (all), ipinfo.io and sunrisesunset.io (all, removed since), Loop (`cdn.loopwork.co`, `api*.loopwork.co`, `d217z8zw4dqir.cloudfront.net`; index, product, collection), flagcdn.com (footer country selector), youtube-nocookie.com and player.vimeo.com (how-it-works iframes, lazy), Judge.me and Loop app embeds.

### Top performance wins (as ranked on 9 Oct)
| # | Win | Impact | Effort |
|---|---|---|---|
| 1 | Drop the Montserrat face and preloads; self-host Proxima Nova or add `preconnect` to Typekit | one render-blocking cross-origin request, two wasted font requests | S/M |
| 2 | Load `loop-widget.js` only where a Loop container exists; move `loop-widget.css.liquid` to a cached asset | 145 KB JS off collection pages; 20 KB HTML per page | M |
| 3 | Day/Night class set in `<head>` without network calls | done since | S |
| 4 | Move inline style and script blocks to assets | 60-70 KB HTML per page becomes cacheable | M |
| 5 | Replace `featured-product` on the home page with a light CTA section, or split `section-main-product.css` | 52 KB CSS, 38 KB JS on home | M |
| 6 | Resize the orbs; add `widths`/`sizes` to three sections | 150-200 KB per home load | S |
| 7 | Make the cart-drawer CSS bundle and `loop-widget.css` non-blocking; lazy-load `cart.js` and `quantity-popover.js` on first drawer open | six render-blocking requests | S |
| 8 | Delete dead files; fix `base.css:30`; gate the welcome-kit `/cart.js` fetch to cart events | repo size, one XHR per page | S |

## 7. Governance and process (9 Oct)

- Remote `dhruvhirpara28-cloud/karmicare` is a contractor's personal account (Arctic Grey developer, two git identities). The live theme is GitHub-connected to `main`.
- 812 commits; 661 are "Update from Shopify" bot commits from admin edits, touching Liquid files (`comparison-table.liquid` 157 times, `legal-toc-section.liquid` 126, `policy-banner.liquid` 73): code edited in the admin code editor on the live theme. 227 bot commits on 5 Oct alone.
- Human commit messages mostly "change", "Pull to main", "PDP Change".
- `theme_export__checkout-karmicare-com-devlopment-theme__06JUL2026-0724pm.zip` (1 MB) remains in history.
- No README, `.gitignore`, Theme Check config, CI or CLAUDE.md at the time; since added (see STATUS.md row 16).
