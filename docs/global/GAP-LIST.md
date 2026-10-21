# Global elements · gap list

**Created**: 2026-10-20

### Changelog
| Date | Change |
|------|--------|
| 2026-10-20 | First version, for Victor's review. No code yet. |
| 2026-10-21 | Victor's answers G-1..G-6; built AN-01, AN-02, FT-02, FT-03, FT-04, FT-06 (theme part), FT-07, FT-08 (`3c03acb`, `95b56d6`, `4954820`). G-2 target pages checked. |
| 2026-10-21 | Added CK-03 (klaviyo.js before consent, from global-footer Phase 1), CK-04 and LY-03 (inherited sticky-card overlaps, Astra R16 on NV-13). |
| 2026-10-21 | Added TY-01 / G-7 (body bold 700 vs Figma Semibold 600), forwarded from the homepage lane. |
| 2026-10-21 | Accessibility check of the global elements, Day and Night, 2176 and 393 px, EN/NL/FR (axe-core 4.10.2 + own contrast and static checks): text contrast passes everywhere (lowest 5.97:1 Night, 7.06:1 Day), input border and focus ring ≥ 10:1. Added A11Y-01, A11Y-02. |

Branch `karmicare/soft-launch-global` @ `1c01dc5`. Compared: the integration preview `189882925437` (home, `/nl`, `/fr`, HTML checked for `Shopify.theme.id`) and the live theme, against Figma `3rOMJvQZTzyYjnCV6oggV3`: header `2928:19881` (1440) and `3027:21407` (393), announcement `2928:19882` / `3027:20793`, footer `2928:20208` (1440, Day) and `3027:21262` (393), and the footer on the Consumer Rights legal frames in `3664:39482` (`3718:25736`, 1440 Night). Figma references are under `docs/global/shots/figma/` (gitignored).

**Evidence limit.** This worktree has no browser helper yet (BRIEF-COORDINATOR "Not ready yet"), so the rows below come from rendered HTML, code and Figma. Rows marked *capture* still need a screenshot at the COMMON-RULES widths, Day and Night. Header and footer HTML is the same on live and the integration preview, apart from one copyright word (FT-11).

Priority: **P0** blocks the soft launch (wrong offer, dead link, privacy) · **P1** visible quality · **P2** polish or note. Owner "this lane" means it's built here once Victor approves; Victor's decisions are `G-n`.

## Announcement bar

| Id | What we see | Figma | P | Owner | Recommendation |
|---|---|---|---|---|---|
| AN-01 | Bar is 39 px at 768: the ≥990 (28 px) and <750 (30 px) rules both miss tablets (`sections/announcement-bar.liquid` L52). From homepage AN-01. | `2928:19882`, `3027:20793` | P1 | this lane | `min-width: 990px` → `750px`. Build. |
| AN-02 | "COMPLIMENTARY SHIPPING · 60-DAY MONEY-BACK GUARANTEE" shows to everyone, but Try Once pays shipping and has 14 days (`kc.sticky_cart.delivery_once_html`, `guarantee_once_html`). The NL batch notes it too. | same text in Figma | P0 | Victor (G-1) | **G-1** (a) qualify the offer with wording Victor approves (we must not write it) · (b) keep only claims that hold for every order until that wording exists · (c) keep. Recommend **a**, with **b** in the meantime. |
| AN-03 | `/nl` and `/fr` show the English bar. It's a setting, so it waits for translation registration (NL is ready: "GRATIS VERZENDING · 60 DAGEN GELD TERUG · GEMAAKT IN BELGIË"). | — | P1 | landing desk (registration) | Note. G-1 changes the source text, so register after G-1. |
| AN-04 | Phone marquee exists (`announcement-bar--marquee`, 20 s); Figma asks for an auto-scroll on one line. | `3027:20793` | P2 | this lane | *capture* at 393/450, check `prefers-reduced-motion`. |

## Header

| Id | What we see | Figma | P | Owner | Recommendation |
|---|---|---|---|---|---|
| HD-01 | `.section-header` is always sticky with an opaque band, although `sticky_header_type` is `none` (homepage HD-01 / D-12). | `2928:19881` (glass pill) | P1 | child **navigation** (NV rows) | The child sets out the D-12 options in `docs/global/nav/NAV-AUDIT.md`; Victor decides from that. |
| HD-02 | Drawer, dropdowns, focus, Escape, scroll lock and the active page: behaviour audit. | — | P1 | child **navigation** | Running (task `task_cd7f661028f8`). |
| HD-03 | Menu: Manifesto · Science · **Professionals** · Members. Figma: Manifesto · Science · **Atlas** · Members. | `2928:19881` | P2 | Victor (Admin menu `new-main-menu`) | Victor: is "Professionals" the newer name or should it be "Atlas"? No theme change. |
| HD-04 | Phone: Figma has the logo left, BEGIN NOW + menu button right; `header-group.json` has `mobile_logo_position: center`. | `3027:21407` | P1 | this lane | *capture* at 393; if the logo is centred, follow Figma (it's a setting in `header-group.json`, carried during the live reconcile). |
| HD-05 | Drawer has a "Log in" link (customer accounts) and a country list with 14 markets, including SEK/CHF/GBP/USD. Not in Figma. | — | P2 | Victor (Markets in Admin) | Keep Log in. Markets: note for Victor only. |
| HD-06 | BEGIN NOW and the menu labels are English on `/nl` and `/fr` (settings and Admin menu: registration). Coming soon is translated ("Binnenkort" / "Bientôt disponible"). | — | P1 | landing desk (registration) | Note. |

## Footer

| Id | What we see | Figma | P | Owner | Recommendation |
|---|---|---|---|---|---|
| FT-06 | All 6 Company links go to `#` (`/nl#`, `/fr#`): Shop Karmicare, Why use hydroxapatite, Why Karmicare, nHAp Technology, Contact, Articles. The footer renders them as plain links (`sections/footer.liquid` L650); the header already uses Coming soon (rule H8). Real targets exist for 3: the PDP, `/pages/contact` (page, no contact form) and `/blogs/news` (articles). | `2928:20208` (same 6 items) | P0 | this lane + Victor (G-2) | **G-2** (a) theme shows Coming soon for every `#` link (same pattern and detection as the header), and Victor points Shop Karmicare → PDP, Contact → contact page, Articles → blog in the Admin menu · (b) hide `#` items · (c) keep. Recommend **a**. |
| FT-07 | Email placeholder `you@example.com` in every language (`kc.footer.email_placeholder`). | `2928:20225` (EN) | P2 | this lane (G-3) | **G-3** (a) NL `jij@voorbeeld.be`, FR `vous@exemple.be` (your proposal) · (b) keep. Recommend **a**. Note: unlike `example.com`, those domains aren't reserved; as a placeholder that's fine. |
| FT-08 | `/fr` footer: consent line and the 3 legal labels are English (held for legal review in B4). FR text is ready: "En vous inscrivant, vous acceptez les conditions d’utilisation et la politique de confidentialité." · Conditions générales · Politique de confidentialité · Droits des consommateurs. | `3718:25736` (EN) | P1 | Victor (G-4), then this lane | **G-4** (a) release the FR texts now · (b) keep EN until legal review. Recommend **a**: they're the standard names, and a half-English FR footer looks broken. |
| FT-03 | Payment icons: 13 colour icons from `shop.enabled_payment_types` (incl. USDC, TWINT, MobilePay). Figma: 5 mono (Apple Pay, Visa, Mastercard, **Amex**, PayPal); Amex isn't enabled. Homepage D-13 (part). | `2928:20252` | P2 | Victor (G-5), then this lane | **G-5** (a) keep as is · (b) Figma's fixed 5 (would show Amex, which isn't accepted) · (c) the real enabled list in Figma's monochrome style. Recommend **c**. |
| FT-04 | Flags load from `flagcdn.com` (L827, L885): a third-party request before cookie consent. | `KC/Icon/flag-belgium` | P0 | this lane | Swap for a source that makes no third-party request; check it renders before building. Build. |
| FT-02 | Menu links are 18-20 px tall inline anchors on phones (15 small tap targets at 393). | — | P2 | this lane | Make each link a ≥24 px target without changing the look. Build. |
| FT-05 | Legal text is 15 px on phones vs 12 px in Figma (footer ~197 px taller). | `3027:21262` | P2 | Utopia lane (type) | Handoff via the landing desk. |
| FT-09 | Menu items "Why **use** hydroxapatite" (typo, and "use" is a banned word): Admin menu. NL already fixed it ("Waarom hydroxyapatiet"). | Figma has the same text | P1 | Victor (Admin menu) | Victor renames it in Admin, e.g. "Why hydroxyapatite" (fixes the typo, drops "use"). |
| FT-10 | Copyright text uses "Toothpaste Kit" and "product" (brand rule) and "Packaging … are recyclable". It's legal company info, the same in Figma. | `2928:20244` | P2 | Victor | Keep it for launch (legal text); change only with your own wording. |
| FT-11 | Live says "Belgium product", the integration has the source-copy fix "Belgian product". | — | P2 | this lane | When reconciling `footer-group.json` with live, keep "Belgian" and carry over any other live editor edits. |
| FT-12 | Slogan, "Company", "Newsletter", menu labels and copyright are English on `/nl` and `/fr` (settings: registration). | — | P1 | landing desk (registration) | Note. |
| FT-13 | "Cookie preferences" link in the legal row isn't in Figma. | — | — | — | Not a gap: it reopens the consent banner (GDPR). Keep. |

## Cookie banner and layout

| Id | What we see | Figma | P | Owner | Recommendation |
|---|---|---|---|---|---|
| CK-01 | Shopify's banner is styled with tokens (`assets/kc-cookie-preferences.css`, glass, radius, type). On phones it covers most of the hero on the first visit (homepage GL-01). | no Figma frame | P2 | this lane | *capture* at 393 and 1440, Day/Night, NL/FR texts. Fix only what's broken. |
| CK-02 | Banner texts come from Shopify's privacy settings (Admin), not from the theme. | — | P2 | Victor | Check NL/FR in the capture; texts can only change in Admin. |
| LY-01 | Day/Night: `day-night-sun.js` renders inline on preview and live (`KCDayNight` present). | — | — | — | Not a gap (the 17 Oct formatter bug isn't in this branch). |
| LY-02 | Page gutter: Dawn's 15 px on phones vs the 20 px token in the footer/clock (homepage TF-07). | `3027:20922` | P1 | Utopia lane | Handoff, already with Utopia. |
| CK-03 | klaviyo.js loads on every page through a Shopify ScriptTag (`asyncLoad`, `window.onload`) with no consent check; not theme code (global-footer `PLAN.md` §1.4). | — | P0 | Victor (Klaviyo/Shopify admin), then this lane | Victor runs the cookie check in `PLAN.md` §8 item 8. If klaviyo.js or `__kla_id` arrive before consent: move Klaviyo onsite to the consent-aware app embed or remove the ScriptTag. |
| CK-04 | Open sticky card (PDP) and the consent panel overlap at 750/990/1200; the panel drops to z-index 199 below the card instead of moving (`assets/kc-cookie-preferences.css:281`). Inherited, not NV-13 (R16). | — | P2 | this lane | Follow-up: place or hide the panel against the open card's height instead of stacking only. |
| TY-01 | Bold in body copy renders 700; Figma "Text/* (Strong)" is Semibold 600 (Text/Medium (Strong) `038b709c…`, hero subtext V15 `2928:19894`). `assets/base.css` sets no weight for `b`/`strong` (browser "bolder" = 700; Typekit `kss0igj` serves 600 and 700), and `layout/theme.liquid:195` sets `--font-body-weight-bold` = body + 300 = 700 (read by `base.css:2960`, `component-cart-items.css:273/:319`, `component-disclosures.css:59/:130`). Setting `body_font_weight` (`settings_schema.json:245`) is read nowhere. From the homepage lane, verified here. | `2928:19894` | P1 | Victor (G-7), then a child | **G-7** (a) `b`/`strong` in body copy and `--font-body-weight-bold` → `var(--font-600-weight)`; headings keep their own rules (two-tone `strong` `base.css:424/:431`, Marlide stays 300); remove the dead `body_font_weight` setting · (b) 600 only, keep the setting · (c) keep 700. Recommend **a**. |
| A11Y-01 | The header logo link (`.header__heading-link`, inline SVG logo) has no accessible name: screen readers announce an empty link on every page, EN/NL/FR, Day and Night (axe `link-name`, serious; WCAG 2.4.4 / 4.1.2). Accessibility check 21 Oct on merchant-edit preview `189891674493`. | — | P1 | this lane | Give the link `aria-label="{{ shop.name }}"` (or visually hidden text) in `sections/header.liquid`; SVG stays `aria-hidden`. No new copy. |
| A11Y-02 | Drawer country filter: `aria-owns` / `aria-controls="country-results"` point to an id that doesn't exist; the list is `{{ localPosition }}-country-results` (`snippets/country-localization.liquid:55-56` vs `:88`, Dawn). | — | P2 | this lane | Point both attributes at `{{ localPosition }}-country-results`. |
| LY-03 | `--header-height` is not set where the sticky card reads it (`assets/component-sticky-cart.css:62` falls back to 0): at 1200×500 the open card reaches y=20 under the floating header; at 1200×700 it overlaps the second Loop card. Inherited (R16). | — | P2 | this lane (header) | Follow-up: publish the floating nav's real clearance as `--header-height` and use it for the card's height cap; keep the first-card trigger. |

## Decisions for Victor

| Id | Question | Options | Recommendation |
|---|---|---|---|
| G-1 | Announcement offer vs Try Once | a qualify (your wording) · b only claims that hold for every order until then · c keep | a, b in the meantime |
| G-2 | Footer `#` links | a Coming soon + 3 real Admin links · b hide · c keep | a |
| G-3 | Email placeholder NL/FR | a `jij@voorbeeld.be` / `vous@exemple.be` · b keep | a |
| G-4 | FR legal labels + consent line | a release · b keep EN | a |
| G-5 | Payment icons | a keep · b Figma 5 · c real list, mono style | c |
| G-6 | Screenshots | a allow `orca browser` captures now · b wait for Codex to set up the browser helper | a |

## Victor's answers (21 Oct) and what was built

| Id | Answer | Result |
|---|---|---|
| G-1 | "complimentary shipping & 60 day.. for members", plus "Circadian oral care since 2017" | `3c03acb`: COMPLIMENTARY SHIPPING & 60-DAY MONEY-BACK GUARANTEE FOR MEMBERS · BELGIAN-MADE · CIRCADIAN ORAL CARE SINCE 2017. The line is ~1000px, so the marquee runs up to 1199px (AN-01 solved the same way: one line at 768). NL/FR text needs new translations and registration (landing desk). |
| G-2 | Find the targets in Admin or on the live site | `95b56d6`: `#` links show Coming soon. Targets found on live (sitemap), see below; the menu itself is Admin (Victor). |
| G-3 | a | `4954820`: `jij@voorbeeld.be` / `vous@exemple.be` |
| G-4 | a | `4954820`: FR consent line and legal labels released |
| G-5 | c | `95b56d6`: the 15 enabled methods with `grayscale(1) contrast(0.6) brightness(1.25)`. Visa, Mastercard, Shop Pay and Twint keep a grey chip (Shopify's icons have a coloured fill); an exact Figma match needs a KC icon set. |
| G-6 | a | Captures with `orca` browser commands under `docs/global/shots/` (viewport emulation is unreliable in the tab: 393 and 768 worked, wider ones render at the pane's 2176px). |

FT-02 (`95b56d6`): footer menu links are inline-block, each fills its 26/28px line. FT-04 (`95b56d6`): flags from `country | image_url` (cdn.shopify.com), no flagcdn request.

### G-2: footer targets on the live site (Admin menu `company`)

| Menu item | Page on live | What is there (21 Oct) | Advice |
|---|---|---|---|
| Shop Karmicare | `/products/karmicare-biorhythmic-oral-care-system` | the PDP | link it |
| Why use hydroxapatite | `/pages/why-use-hydroxyapatite-toothpaste` | heading + one line (12 words) | keep `#` (Coming soon) until it has content |
| Why Karmicare | `/pages/why-karmicare` | heading + one line (17 words) | keep `#` |
| nHAp Technology | `/pages/nhap-technology` | heading + "NASA's favorite supplement" line (30 words) | keep `#`; that line is a claim to review |
| Contact | `/pages/contact` | contact form (name, email, phone, comment) | link it |
| Articles | `/blogs/news` (9 posts) or `/pages/articles` (heading only) | 2024 posts incl. nootropics, "avoid fluoride", whitening | keep `#` until the posts are reviewed against the brand rules |

## Before ready-to-land

- Reconcile `sections/header-group.json` and `sections/footer-group.json` with live `#187295564157` (read-only pull to a temp directory, diff, carry over Victor's live editor edits).
- Merge the navigation child after review; one Astra review; Theme Check 0 errors; lane preview pushed and captured.
