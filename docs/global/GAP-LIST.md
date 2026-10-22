# Global elements · gap list

**Created**: 2026-10-20

## Status 22 Oct

merchant-edit is `2ef9b5c` (updated from `31407fb`). It isn't pushed yet, so nothing below is live. "In merchant-edit" was checked with `git merge-base --is-ancestor <sha> merchant-edit`.

**Counts (41 rows):** In merchant-edit 15 · Done in Admin (live) 2 · Ready to land 0 · In progress 4 · Waiting for Victor 11 · Parked / after launch 7 · Dropped 2.

| Id | Status | Proof / note |
|---|---|---|
| AN-01 | In merchant-edit | `3c03acb` |
| AN-02 (G-1) | In merchant-edit | `3c03acb`. The NL/FR text is tracked under AN-03. |
| AN-03 | In progress | Landing desk: translation registration |
| AN-04 | Parked / after launch | P2: capture the phone marquee and check reduced motion |
| HD-01 | In merchant-edit | global-nav floating nav `b0c9fd2`; NV-13 `27691cb` |
| HD-02 | In merchant-edit | global-nav audit fixes; the last one is `3441bac` |
| HD-03 | Waiting for Victor | Professionals or Atlas (question 7) |
| HD-04 | Waiting for Victor | Phone logo position (question 8) |
| HD-05 | Parked / after launch | Markets are set in Admin. Log in stays. |
| HD-06 | In progress | Landing desk: registration |
| FT-02 | In merchant-edit | `95b56d6` |
| FT-03 (G-5) | In merchant-edit | `95b56d6` |
| FT-04 | In merchant-edit | `95b56d6` |
| FT-05 | Parked / after launch | Handed to the Utopia lane; its report has the status |
| FT-06 (G-2), theme part | In merchant-edit | `95b56d6`: `#` links show Coming soon |
| FT-06, Admin links | Done in Admin (live) | Victor, 22 Oct. Read back on the storefront: Shop Karmicare → `/products/karmicare-biorhythmic-oral-care-system`, Contact → `/pages/contact`, Articles → `/blogs/news`. Why Karmicare and nHAp Technology stay `#`. They show Coming soon only once `95b56d6` (in merchant-edit) is live. |
| FT-07 (G-3) | In merchant-edit | `4954820` |
| FT-08 (G-4) | In merchant-edit | `4954820` |
| FT-09 | Done in Admin (live) | Victor, 22 Oct: renamed to "Why hydroxyapatite", linked to the article `/blogs/news/nano-hydroxyapatite`. Victor edited the article the same day. Changed: the SEO title (typo fixed, keyword first), the meta description, and three decay/sensitivity sentences plus heading 4 (now "helps protect …"). Read back on the storefront. Victor approved it for publication as it is. The following were left in on his decision:
- heading 3 "Reduces …"
- in the intro: "medical marvel for better teeth, bones and overall health"
- "chemicals that prevent natural healing"
- "Swap fluoride for nano HAp"
- "first discovered by NASA"
- "nontoxic"

Victor hid the near-duplicate twin article `nano-hydroxyapatite-and-why-you-need-it-in-your-toothpaste` and added a URL redirect to `/blogs/news/nano-hydroxyapatite`. The redirect was tested on EN, `/nl` and `/fr` (all three redirect and return 200). |
| LY-04 | Waiting for Victor | Page title suffix (question 9) |
| FT-10 | Parked / after launch | Legal text is kept for launch |
| FT-11 | In merchant-edit | "Belgian product" is in merchant-edit `sections/footer-group.json` (source-copy) |
| FT-12 | In progress | Landing desk: registration |
| FT-13 | Dropped | Not a gap: the Cookie preferences link stays |
| CK-01 | Parked / after launch | P2 capture. It needs a browser that hasn't given consent yet. |
| CK-02 | Parked / after launch | The banner texts are set in Admin; check them with CK-01 |
| CK-03 | Waiting for Victor | Klaviyo before consent (question 4) |
| CK-04 | Waiting for Victor | Sticky card overlaps, G-10 (question 3) |
| LY-01 | Dropped | Not a gap |
| LY-02 | Parked / after launch | Handed to the Utopia lane |
| LY-03 | Waiting for Victor | Sticky card overlaps, G-10 (question 3) |
| TY-01 (G-7) | In progress | Child global-type (status 22 Oct, not committed yet). Done: the `b`/`strong` rule in `assets/base.css` (headings excluded); `--font-body-weight-bold` = `var(--font-600-weight)` in `layout/theme.liquid`; the dead `body_font_weight` removed from `config/settings_schema.json`; Theme Check 0 errors. "Before" measured at 700. Open: the rendered "after" check on preview `189947838845` (390/1440, Day/Night, EN/NL/FR, cart drawer), then one commit and Ready to land. |
| A11Y-01, A11Y-02, A11Y-03 (3 rows) | In merchant-edit | `361a06c`, landed with `a8f931d`, source-copy `59c281e` and FR `e883509` (integration `7b8d33c`, merchant-edit `2ef9b5c`). Astra R19: no regression. On :9298, EN, NL and FR return 200, the legal pages have one `main`, and the filter ids are scoped per position. |
| PDP end CTA "Begin your 60-Day Rhythm" | In merchant-edit | `361a06c`, as above |
| LC-01, LC-02, LC-03, LC-04 (4 rows, G-9) | Waiting for Victor | Country selector bugs (question 2) |
| Button capitals (G-8, `BUTTON-CASE.md`) | Waiting for Victor | Question 1 |

**Children.**
- **global-nav:** everything up to `1aab847` is in merchant-edit (checked again against `65eb83b`), and nothing of it is open. It didn't answer the request to update its own `docs/global/nav/REPORT.md`, so this line is its status.
- **global-footer:** the Phase 1 plan `43351f9` is docs only and in merchant-edit. The newsletter build (Phase 2) waits for Victor's D1–D6. Its status block is `0b45fad` on `karmicare/global-footer` (`docs/global-footer/PLAN.md`), with the questions in words.
- **global-type:** see TY-01.

### Waiting for Victor: the questions

1. **Button capitals (G-8).** Buttons already render in capitals, except the footer Join button. The source texts are mixed (BEGIN NOW, Begin Now, Begin now).
   - a. Everything in capitals. Join gets the same CSS capitals, and the source texts are written in normal case through source-copy, so screen readers read words instead of spelling letters.
   - b. Title Case ("Begin Your 60-Day Rhythm"). Remove the CSS capitals and rewrite about 20 EN texts. NL and FR stay in sentence case, so the languages look different.
   - c. Sentence case ("Begin your 60-Day Rhythm"). Remove the CSS capitals and rewrite the texts that are now in capitals. This differs from Figma.
   - **Advice: a.**
2. **Country selector bugs (G-9: LC-01..LC-04).** These are older bugs in the country and currency picker, and only keyboard and screen reader users notice them:
   - Duplicate ids.
   - Arrow keys stop working after filtering.
   - A crash when 0 countries match.
   - A wrong count ("2 countries found" for one).
   - The footer picker doesn't close with Escape or respond to arrow keys.

   Options:
   - a. Fix all four now, as one small change in this lane.
   - b. Fix them after launch.
   - **Advice: a.**
3. **Sticky card overlaps (G-10: CK-04, LY-03).** These problems were already there; they aren't new.
   - On the PDP, the open sticky card and the cookie panel overlap at 750, 990 and 1200 px wide.
   - At laptop heights (1200×700), the card runs under the floating nav and over the second plan card.

   Options:
   - a. Fix both before launch in this lane. The card reads the nav's real height, and the cookie panel moves above the card.
   - b. Fix them after launch.
   - **Advice: a**, because the card covers a plan card on common laptop screens.
4. **Klaviyo before consent (CK-03).** klaviyo.js loads on every page through a Shopify ScriptTag, without waiting for cookie consent.
   - a. You run the 5-minute check in `docs/global-footer/PLAN.md` §8 item 8: open a private window, don't accept cookies, and look for klaviyo.js and the `__kla_id` cookie. If they appear, switch Klaviyo's onsite script to the consent-aware app embed, or remove the ScriptTag in Admin.
   - b. Accept it for launch.
   - **Advice: a.** It's a privacy issue (P0).
5. **Footer Admin links (FT-06, G-2).**
   - a. In the Admin menu `company`, point Shop Karmicare to `/products/karmicare-biorhythmic-oral-care-system` and Contact to `/pages/contact`. The theme then shows them as links instead of Coming soon.
   - b. Keep Coming soon.
   - **Advice: a.**
   - **Victor, 22 Oct:** Articles links to the blog (`/blogs/news`) too; Victor makes the change in Admin. Note: those 9 posts are from 2024, and some of them (nootropics, "avoid fluoride", whitening) haven't been checked against the brand and cosmetic-claim rules.
6. **Menu name (FT-09).** The footer item "Why use hydroxapatite" has a typo and contains the banned word "use".
   - a. Rename it in Admin to "Why hydroxyapatite".
   - b. Keep it.
   - **Advice: a.** It stays Coming soon until its page has content.
7. **Professionals or Atlas (HD-03).** The header menu says Professionals; Figma says Atlas.
   - a. Keep Professionals. It matches the homepage section and "Request a practitioner sample".
   - b. Rename it to Atlas in the Admin menu.
   - **Advice: a**, unless Atlas is the newer name.
9. **Page title suffix (LY-04).** `layout/theme.liquid:25` adds " – KARMICARE" to every title that doesn't already contain the shop name. The PDP SEO title is "Fluoride-Free Nano-Hydroxyapatite Toothpaste | Awake & Asleep", so the browser title becomes 73 characters, and Google cuts it around 60. Google already shows "Karmicare" as the site name above the result.
   - a. Skip the suffix when the SEO title already has its own " | " brand part. One condition, in this lane.
   - b. Keep it.
   - **Advice: a.**
8. **Phone logo (HD-04, G-11).** In Figma (393 px), the logo is on the left, with BEGIN NOW and the menu button on the right. The theme centres the logo (`mobile_logo_position: center`), and you tuned that nav on localhost (NV-07, NV-08).
   - a. Keep it centred.
   - b. Move the logo left with one setting in `header-group.json`. Dawn keeps the menu button on the left, so this only moves the logo.
   - **Advice: a.**

### Changelog
| Date | Change |
|------|--------|
| 2026-10-20 | First version, for Victor's review. No code yet. |
| 2026-10-21 | Victor's answers G-1..G-6; built AN-01, AN-02, FT-02, FT-03, FT-04, FT-06 (theme part), FT-07, FT-08 (`3c03acb`, `95b56d6`, `4954820`). G-2 target pages checked. |
| 2026-10-21 | Added CK-03 (klaviyo.js before consent, from global-footer Phase 1), CK-04 and LY-03 (inherited sticky-card overlaps, Astra R16 on NV-13). |
| 2026-10-21 | Added TY-01 / G-7 (body bold 700 vs Figma Semibold 600), forwarded from the homepage lane. |
| 2026-10-21 | Accessibility check of the global elements, Day and Night, 2176 and 393 px, EN/NL/FR (axe-core 4.10.2 + own contrast and static checks): text contrast passes everywhere (lowest 5.97:1 Night, 7.06:1 Day), input border and focus ring ≥ 10:1. Added A11Y-01, A11Y-02. |
| 2026-10-21 | Built A11Y-01 (shop name as hidden link text, SVG `aria-hidden`), A11Y-02 (filter ids scoped per `localPosition`), A11Y-03 (legal TOC `main` → `div`); PDP end button "Begin your 60-Day Rhythm" (template; EN source row requested from source-copy). |
| 2026-10-21 | Astra R19 on `361a06c`: no regression. Added LC-01..LC-04 (older country-selector keyboard and id bugs, R19-02..05) as G-9. Report: `global-nav/docs/runtime-review/R19-GLOBAL-A11Y-ASTRA.md`. |
| 2026-10-22 | Added the "Status 22 Oct" block: one status per row against merchant-edit `31407fb`, the counts, and the 8 open questions for Victor in words. New ids: G-8 (button capitals), G-10 (CK-04 and LY-03), G-11 (HD-04). No theme change. |
| 2026-10-22 | A11Y-01..03 and the PDP end CTA moved to In merchant-edit (`361a06c` landed, merchant-edit `2ef9b5c`). Counts: In merchant-edit 15, Ready to land 0. |
| 2026-10-22 | Victor changed the Company menu in Admin: FT-06 Admin links and FT-09 are done, read back on the storefront. The new PDP title and SEO fields were checked on the storefront (title, meta description, og:title, H1, JSON-LD). Added LY-04 (title suffix, question 9) and the rewrite note for the hydroxyapatite article. |

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
| A11Y-03 | Privacy (and every page with the legal TOC section) has two `main` landmarks: `.legal-toc__content` is a `<main>` inside the layout's `<main>` (`sections/legal-toc-section.liquid:165`). | — | P2 | this lane | `<main>` → `<div>`; styles use the class. Built with A11Y-01/02 (landing desk for Victor, 21 Oct). |
| LC-01 | Country selector: duplicate ids for the live region and country options (e.g. "Netherlands" twice, header and drawer), so `aria-activedescendant` can point into the hidden drawer; some ids contain spaces. Older, not from A11Y-02 (Astra R19-02). | — | P2 | this lane (G-9) | Scope every id per `localPosition` and slug the country names. |
| LC-02 | Arrow keys stop working when a popular country is filtered out; with 0 results ArrowDown throws a TypeError (`assets/localization-form.js:54-73`) (R19-03). | — | P2 | this lane (G-9) | Walk only visible options; guard the empty list. |
| LC-03 | Result count is wrong ("2 countries found" for one) (R19-04). | — | P2 | this lane (G-9) | Count visible options once, not per list. |
| LC-04 | Footer currency/language picker has no Escape and no arrow keys (R19-05). | — | P2 | this lane (G-9) | Escape closes and returns focus; arrows move between options. |
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
