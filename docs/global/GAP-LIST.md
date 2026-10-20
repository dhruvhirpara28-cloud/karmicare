# Global elements · gap list

**Created**: 2026-10-20

### Changelog
| Date | Change |
|------|--------|
| 2026-10-20 | First version, for Victor's review. No code yet. |

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

## Decisions for Victor

| Id | Question | Options | Recommendation |
|---|---|---|---|
| G-1 | Announcement offer vs Try Once | a qualify (your wording) · b only claims that hold for every order until then · c keep | a, b in the meantime |
| G-2 | Footer `#` links | a Coming soon + 3 real Admin links · b hide · c keep | a |
| G-3 | Email placeholder NL/FR | a `jij@voorbeeld.be` / `vous@exemple.be` · b keep | a |
| G-4 | FR legal labels + consent line | a release · b keep EN | a |
| G-5 | Payment icons | a keep · b Figma 5 · c real list, mono style | c |
| G-6 | Screenshots | a allow `orca browser` captures now · b wait for Codex to set up the browser helper | a |

## Before ready-to-land

- Reconcile `sections/header-group.json` and `sections/footer-group.json` with live `#187295564157` (read-only pull to a temp directory, diff, carry over Victor's live editor edits).
- Merge the navigation child after review; one Astra review; Theme Check 0 errors; lane preview pushed and captured.
