# Buttons and CTAs: capitalisation inventory

**Created**: 2026-10-21

**Status 22 Oct: Waiting for Victor (G-8).** Nothing has been built. Every button renders in capitals except the footer Join button. Options:
- a. Everything in capitals, with the source texts in normal case through source-copy.
- b. Title Case.
- c. Sentence case.

Advice: **a**. The options are explained under "The choice for Victor" below.

### Changelog
| Date | Change |
|------|--------|
| 2026-10-21 | First version, for Victor's choice (landing desk: "check ook dat alle knoppen capitalized zijn"). Measured on preview `189917069693` (karmicare/soft-launch-global `361a06c` = integration `1ca2168` + A11Y fixes), home, PDP and privacy, EN/NL/FR, at 1440 and 390 px. |
| 2026-10-22 | Status block added; the choice is still open, now id G-8 on the gap list. |

**How it was measured.** Every `button`, `.button`, `[role=button]`, `*cta*` and `*btn*` element with text, outside the Loop widget; `text-transform` read with `getComputedStyle` on the label. 1440 and 390 give the same result for every button.

**Result in one line.** Every button already *renders* in capitals through CSS, whatever its source text, except the footer **Join** button. The two "Try once" items are text links, not buttons. The source texts themselves are mixed: `BEGIN NOW`, `Begin Now`, `Begin now`, `Begin your 60-Day Rhythm`, `Try Once`, `Try once`.

**NL/FR.** Most template and section texts still render in English on `/nl` and `/fr` until the Admin registration runs; the NL/FR column shows the prepared translation where one exists.

| # | Where | Source (file:key) | EN source text | NL / FR | Rendered |
|---|-------|-------------------|----------------|---------|----------|
| 1 | Header | `sections/header-group.json:55` `cta_text` | BEGIN NOW | (EN until registration) | CAPS (CSS) |
| 2 | Home hero, primary | `templates/index.json:37` `button_label_1` | BEGIN YOUR 60-DAY RHYTHM | BEGIN JE 60-DAGENRITME / COMMENCER VOTRE RYTHME 60 JOURS | CAPS |
| 3 | Home hero, secondary | `templates/index.json:39` `button_label_2` | WHY TWO FORMULAS? | (EN) | CAPS |
| 4 | Two formulas | `templates/index.json:205` `button_label` | BEGIN YOUR 60-DAY RHYTHM | as 2 | CAPS |
| 5 | Two formulas, 2× Coming soon | `templates/index.json:211, :215` | SEE WHAT'S INSIDE | (EN) | CAPS |
| 6 | Benefits | `templates/index.json:330` `button_label` | BEGIN YOUR 60-DAY RHYTHM | as 2 | CAPS |
| 7 | Professionals, Coming soon (home + PDP) | `templates/index.json:446`, `templates/product.subscription-item.json:376` | REQUEST A PRACTITIONER SAMPLE | (EN) | CAPS |
| 8 | FAQ filters | `kc.faq.all` + FAQ categories in `templates/index.json` | ALL · The system · The ritual · Plans & Return on Care · Shipping & guarantee | ALLE / TOUT; categories (EN) | CAPS |
| 9 | Home featured product | `templates/index.json:704` `custom_button_text` | Begin your 60-Day Rhythm | (EN) | CAPS |
| 10 | PDP buybox, per plan | `templates/product.subscription-item.json:115` `custom_button_text_by_plan` | Begin your 60-Day Rhythm · Begin your Karmicare Year | Begin je 60-dagenritme · Begin je Karmicare-jaar / Commencer votre Rythme 60 jours · Commencer votre année Karmicare | CAPS |
| 11 | PDP buybox, Try once | `templates/product.subscription-item.json:86` `try_once_text` | Try once · €67 | (EN) | as typed (text link) |
| 12 | PDP Read more (2×) | `templates/product.subscription-item.json:144` `read_more_text` | Read more | (EN) | CAPS |
| 13 | Comparison table | Admin metaobject `comparison.table_button_text` | Begin now (+ plan name) | (EN) | CAPS |
| 14 | Compare plans table | Admin metaobject `compare_value` `cta_button` | Try Once · Begin your 60-Day Rhythm · Begin | Begin / Commencer for the last | CAPS |
| 15 | PDP end CTA | `templates/product.subscription-item.json:672` `custom_button_text` | Begin your 60-Day Rhythm | (EN) | CAPS |
| 16 | Sticky bar | `templates/product.subscription-item.json:211` `button_text` (default `Begin now`) | Begin Now | (EN) | CAPS |
| 17 | Sticky panel | `kc.sticky_cart.cta_rhythm_html` / `cta_year_html` | Begin your 60-Day Rhythm · Begin your Karmicare Year | Begin je 60-dagenritme / Commencer votre Rythme 60 jours | CAPS |
| 18 | Sticky Change | `kc.sticky_cart.change_label_html` | Change | Wijzigen / Modifier | CAPS |
| 19 | Sticky, Try once | `kc.sticky_cart.*` try-once line | Not ready for a membership? Try once for €67 | translated | as typed (text link) |
| 20 | **Footer newsletter** | `kc.footer.join` | Join | Doe mee / S’inscrire | **as typed** |
| 21 | Footer currency/language | footer locale selector | EUR/EN | — | CAPS |

Legal pages have no buttons of their own; they show 1, 20 and 21.

## The choice for Victor

- **a. Everything in capitals, like BEGIN NOW and the homepage buttons.** This is how the site renders today, apart from Join. Build: Join gets the same CSS capitals (one rule in `sections/footer.liquid`). Recommended extra: write the source texts in normal case ("Begin now", "All", "Begin your 60-Day Rhythm") and let CSS make the capitals, so screen readers read words instead of spelling "ALL", and NL/FR translations stay natural. That text change goes through source-copy.
- **b. Title Case, "Begin Your 60-Day Rhythm".** Remove the CSS capitals from every button style and rewrite all ~20 EN texts in Title Case. NL and FR don't use Title Case, so they would stay in sentence case: the three languages would look different.
- **c. Sentence case with the plan name capitalised, "Begin your 60-Day Rhythm" (today's PDP source text).** Remove the CSS capitals; rewrite the capitalised sources (1–8) in sentence case. Matches how NL/FR are written; differs from Figma, where the buttons are in capitals.

Recommendation: **a**, with the source texts in normal case.
