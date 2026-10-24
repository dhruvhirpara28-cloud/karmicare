# Online withdrawal function and the harmonised legal-guarantee notice: requirements

**Created**: 2026-10-24 (lane gate-withdrawal, R58, LR1 blocker 2)
**Read date for every source**: 24 October 2026. Official texts were read in full from the Publications Office (EUR-Lex cellar), Justel and the Commission's own files; secondary sources (law-firm notes, app listings) are marked as such.
**Scope**: what the law demands of the withdrawal function and of the guarantee notice, how the theme meets each point, which route sends the acknowledgement of receipt, and what stays with Victor or another lane.

### Changelog

| Date | Change |
|------|--------|
| 2026-10-24 | Created with the build (`sections/kc-withdrawal.liquid`, `snippets/kc-legal-guarantee-notice.liquid`, product-page block). |

---

## Part A: the online withdrawal function

### A1. Legal basis and dates

| Instrument | What it does | Dates | Source |
|---|---|---|---|
| Directive (EU) 2023/2673 of 22 November 2023, Art. 1(3) | Inserts **Article 11a** "Exercise of the right of withdrawal from distance contracts concluded by the means of an online interface" into Directive 2011/83/EU (the Consumer Rights Directive, CRD). Art. 1(2) rewrites Art. 6(1)(h): the pre-contractual information must include "information about the existence and placement of the withdrawal function". | Transposition by 19 December 2025; Member States apply the measures from **19 June 2026** (Art. 2(1)). | [EUR-Lex, EN](https://eur-lex.europa.eu/eli/dir/2023/2673/oj/eng) · [NL](https://eur-lex.europa.eu/eli/dir/2023/2673/oj/nld) · [FR](https://eur-lex.europa.eu/eli/dir/2023/2673/oj/fra) |
| Belgium: Act of 19 July 2026 (Justel W 2026-07-19/05) | Art. 23 inserts **Art. VI.61/2** in the Code of Economic Law (WER/CDE), a word-for-word copy of Art. 11a; Art. 22 adds the function to the distance-contract information list, **Art. VI.45 §1, 8°** ("informatie over de beschikbaarheid en de plaats van de herroepingsfunctie bedoeld in artikel VI.61/2"); Art. 24 extends the trader's burden of proof, Art. VI.62. | In force **14 August 2026**. | [Justel, WER consolidated, NL](https://www.ejustice.just.fgov.be/cgi_loi/change_lg_2.pl?language=nl&nm=2013A11134&la=N) · [FR](https://www.ejustice.just.fgov.be/cgi_loi/change_lg_2.pl?language=fr&nm=2013A11134&la=F) (Boek VI, Titel 3, Hoofdstuk 2, Afdeling 4) |
| FPS Economy | Confirms the duty for Belgian shops since 14 August 2026 and describes it as a button or link, easy to find, easy to use, available for the whole period, never behind an app download, followed by a confirmation. | | [news.economie.fgov.be, "Een impulsieve online aankoop? Er is een weg terug"](https://news.economie.fgov.be/270128-een-impulsieve-online-aankoop-er-is-een-weg-terug/) |
| Who must comply | Every trader that concludes distance contracts through an online interface where a right of withdrawal exists. Karmicare: every order on the Shopify store, Try Once and memberships alike (the 14 days run from delivery, for a membership from the first delivery). | | Art. VI.61/2 §1 WER; Art. VI.47 WER |

Secondary sources that agree on article number and date: [Flamée & Partners](https://www.flamee.be/kenniscentrum/herroepingsknop-verplicht-voor-webshops-wat-moet-u-doen/) and [trustyourwebsite.com/be](https://trustyourwebsite.com/be/nl/guides/herroepingsknop-webshop-juni-2026) (the latter gives the Belgisch Staatsblad publication as 4 August 2026). Older notes that say Belgium had not yet transposed (Certifisc, Unizo) predate the Act.

### A2. What the function must be, and how the theme meets it

Statutory wording, verbatim from Art. VI.61/2 WER (Justel) and Art. 11a CRD (EUR-Lex):

| Language | The function's label (§1) | The confirmation function (§3) |
|---|---|---|
| EN (Art. 11a) | "withdraw from contract here" or an unambiguous corresponding formulation | only the words "confirm withdrawal" or an unambiguous corresponding formulation |
| NL (Art. VI.61/2, Art. 11 bis) | "hier de overeenkomst herroepen" of een ondubbelzinnige overeenkomstige formulering | alleen met de woorden "herroeping bevestigen" of met een andere ondubbelzinnige overeenkomstige formulering |
| FR (Art. VI.61/2, Art. 11 bis) | "renoncer au contrat ici" ou une formule analogue dénuée d'ambiguïté | les seuls mots "confirmer la rétractation" ou une formule tout aussi dénuée d'ambiguïté |

| # | Requirement | Source | How the theme meets it |
|---|---|---|---|
| 1 | The function is labelled with the words above, "in an easily legible way". | §1, second sentence | The page heading is the statutory label in each language (section setting `heading`, NL/FR in the handoff); the menu link to the page carries the same words (ADMIN-STEPS step 3). |
| 2 | "Prominently displayed on the online interface and easily accessible"; "continuously available throughout the withdrawal period"; the consumer must not have to download an app or go through procedures to find it; hyperlinks may lead to it. | §1, third and fourth sentences; Directive 2023/2673 recital on the function | A public page `/pages/withdrawal` (template `page.withdrawal`), no login, reachable from every page through the footer and legal menus, from the order confirmation and from Loop's emails (ADMIN-STEPS steps 3, 5, 6). It stays published permanently. |
| 3 | The online withdrawal statement lets the consumer easily provide or confirm: (a) name; (b) details identifying the contract; (c) details of the electronic means by which the confirmation will be sent. | §2 | Step 1: name, order number (with help text: as on the order confirmation), email address for the acknowledgement. One optional field, "Which items", for a partial withdrawal; nothing else is asked, no reason, no account. Logged-in customers get name and email prefilled ("confirm"). |
| 4 | After completing the statement, a confirmation function labelled only "confirm withdrawal" submits it. | §3 | Step 2 shows the statement back, then one button "Confirm withdrawal" (`button_confirm`, statutory words in NL and FR). Without JavaScript the fields and that button render together, which is still statement plus confirmation function. |
| 5 | Once confirmed, the trader sends "an acknowledgement of receipt of the withdrawal on a durable medium, including its content and the date and time of its submission, without undue delay". | §4 | Two copies leave on confirm: (i) Shopify's own contact form posts the statement to the store inbox (time-stamped by Shopify, the trader's record); (ii) one event to Klaviyo, whose transactional flow emails the consumer the acknowledgement with statement, name, order number, items, email, date and time in Europe/Brussels and in UTC (A4 below, ADMIN-STEPS step 4). The success view tells the consumer the email is on its way and to keep it as proof. |
| 6 | A statement submitted before the period expires counts as timely. | §5 | The success copy and the acknowledgement state the submission date and time; the aside says "the day you tell us counts". |
| 7 | Pre-contractual information must mention the existence and placement of the function. | Art. VI.45 §1, 8° WER; Art. 6(1)(h) CRD | Handoff to gate-legal: Terms clause 4.1 and Consumer Rights 3.1 name the function and link `/pages/withdrawal` (see Handoffs). |
| 8 | The trader bears the burden of proof that it met the information and acknowledgement duties. | Art. VI.62 WER | Records: the inbox email (Shopify) and the Klaviyo event on the profile (content, time, `unique_id`). Keep both; ADMIN-STEPS step 7. |
| 9 | Consequence of missing or wrong information: the withdrawal period runs up to 12 months longer; sanctions under Book XV WER. | Art. VI.48 WER; Book XV (fines reported from €260 to €100 000 or 4 % of turnover, secondary source: the 5 October legal audit) | Reason to ship this before the domain switch. |

Data minimisation (GDPR Art. 5(1)(c)): the statement collects only what §2 requires plus the optional item list; the privacy note under the form links the Privacy Policy. gate-legal should list Klaviyo as processor for the acknowledgement if the policy does not already (it is the store's email system).

### A3. Design choices inside the law

- **Two steps with JavaScript, one step without.** The law requires a statement and a separate confirmation function, not a review page; the review step is good practice (the FPS Economy and the Commission both describe "fill in, then confirm"). The no-JavaScript fallback keeps the statutory minimum.
- **No CAPTCHA wall by the theme.** Shopify's own spam protection may show its challenge page after the post; it then returns to the page. Keep it on, but if care@ ever sees a complaint that the challenge blocked a withdrawal, treat the email route as the fallback (the aside names it).
- **No tracking by the page.** The page loads only the theme's own CSS and JS. The single outbound request it makes itself is the Klaviyo event, after the consumer presses Confirm, with the data the consumer typed. No cookies, no pixel. Global app embeds (Hotjar, analytics) are the consent lane's matter and are not touched here.
- **Language.** The page, its texts and the acknowledgement follow the storefront language (EN at the root, NL and FR in subfolders); the Klaviyo event carries `language` so the flow can pick the right email.

### A4. The acknowledgement of receipt: routes compared

Shopify's `{% form 'contact' %}` delivers the statement to the store inbox only; the consumer gets nothing. Four ways to send the legally required acknowledgement, read on 24 October 2026:

| Route | Cost | What Victor installs or configures | Content, date and time on a durable medium, without undue delay | Verdict |
|---|---|---|---|---|
| **Shopify Flow** (native) | Free | A workflow | No trigger exists for the theme's contact form. Flow's "Send internal email" action cannot take a variable as recipient ("variables can't be used to customize the address an email is sent to … best used to send emails to staff"), and "Send marketing email" reaches subscribed customers only. [Shopify Help, Send internal email](https://help.shopify.com/en/manual/shopify-flow/reference/actions/send-email) | Does not meet §4 on its own. Usable only with a third-party email action app. |
| **Shopify Forms** (+ Flow) | Free app | Build the form in the app, place its app block, add a Flow on "Metaobject entry created" | Forms is a sign-up/lead tool: one submit step, no confirmation step, submissions become customers and metaobjects, no acknowledgement email to the submitter. Flow then has the recipient problem above. [Shopify Help, Forms](https://help.shopify.com/en/manual/promoting-marketing/create-marketing/forms-app) · [Forms with Flow](https://help.shopify.com/en/manual/promoting-marketing/create-marketing/forms-app/flow) | Does not meet §3 (confirmation function) or §4. |
| **EU withdrawal-button app** (App Store) | Revoq: free plan (with "Powered by Revoq" on the form), Essential $9/month, Professional $25/month. Nayvo: free, $7.99 or $22/month. | Install, set texts per language, add the app block to a page, set the sender | Revoq (BuschBytes, launched 11 March 2026, 4.8 from 577 reviews): two-step form, no login, automatic confirmation email, order matching, EU hosting, EN/NL/FR among 11 languages. Nayvo (launched 3 June 2026, 4.7 from 60): two-step, confirmation email to customer and merchant, 13 languages. Neither listing states that the email carries the date and time of submission; the free plans carry vendor branding; the form is the app's, not the theme's. [Revoq](https://apps.shopify.com/eu-withdrawal-form) · [Nayvo](https://apps.shopify.com/eu-withdrawal-button-form) | Meets the function in one package. Fallback route if Klaviyo cannot send transactional email (below). The page template keeps an app-block slot for it. |
| **Klaviyo transactional flow** (recommended) | Existing Klaviyo account (Karmicare, public key `XfYq2r`, sender we@karmicare.com, time zone Europe/Brussels). Transactional status needs a **paid** Klaviyo plan. | A metric-triggered flow with one email, marked transactional (Klaviyo reviews the request, about one business day), the public key pasted into the section setting | The theme form sends one event to Klaviyo's client endpoint (public key, built for browsers: [Create Client Event](https://developers.klaviyo.com/en/reference/create_client_event)); the flow email interpolates statement, name, order number, items, email and the submission time in Europe/Brussels and UTC. Transactional emails reach profiles regardless of marketing consent or unsubscribe ([Klaviyo Help, transactional flows](https://help.klaviyo.com/hc/en-us/articles/360003165732)). Send is immediate (no delay step, Smart Sending off). | **Meets §4** with the theme's own on-brand form and no new vendor, and the store inbox keeps the trader's record. |

**Recommendation**: the theme form with the Klaviyo transactional flow. Reasons: the form stays in the theme (tokens, Day and Night, three languages, no vendor branding), the consumer's data goes to a processor the store already uses, the acknowledgement's content and time stamps are under Karmicare's control, and the store inbox copy is a second durable record. Condition: the Klaviyo account must be on a paid plan so the email can be marked transactional; if it is not and Victor does not want to upgrade, install Revoq (free) and drop its block into the withdrawal page (the section has an app-block slot and a "Show the theme form" switch). Built accordingly: `sections/kc-withdrawal.liquid`, `assets/kc-withdrawal.js`, settings `klaviyo_company_id` and `klaviyo_metric`.

Why not Shopify-only: nothing in Shopify sends a non-marketing email to a form submitter without an app.

---

## Part B: the harmonised notice on the legal guarantee of conformity

### B1. Legal basis and dates

| Instrument | What it does | Dates | Source |
|---|---|---|---|
| Directive (EU) 2024/825 of 28 February 2024, Art. 2 | Amends the CRD: Art. 5(1)(e) and Art. 6(1)(l) now read "a reminder of the existence of the legal guarantee of conformity for goods and its main elements, including its minimum duration of two years as provided in Directive (EU) 2019/771, **in a prominent manner, using the harmonised notice** referred to in Article 22a"; new **Art. 22a** (harmonised notice and label; the Commission fixes design and content by implementing act). Recital 28: "displayed in a prominent manner, for example, on a poster … next to the checkout counter or, in cases of online sale, placed as a general reminder on the website of the trader selling goods." | Member States apply the measures from **27 September 2026**. | [EUR-Lex](https://eur-lex.europa.eu/eli/dir/2024/825/oj/eng) |
| Commission Implementing Regulation (EU) 2025/1960 of 25 September 2025 | Art. 1: the notice "shall comply with the design and content set out in Annex I". Art. 3: applies from **27 September 2026**. Annex I notes: (1) "None of the elements of the harmonised notice can be edited"; (2) reference colours Blue #003399, Yellow #FFED00, Black #000000, White #FFFFFF; (3) the QR code leads to the language section on the Your Europe portal and must scan on a standard phone; (4) off line: colour or black and white, minimum A4; (5) "For distance contracts concluded through an online interface, the harmonised notice … shall be in colour (RGB)." | Applies from 27 September 2026. | [EUR-Lex, EN](https://eur-lex.europa.eu/eli/reg_impl/2025/1960/oj/eng) · [NL](https://eur-lex.europa.eu/eli/reg_impl/2025/1960/oj/nld) · [FR](https://eur-lex.europa.eu/eli/reg_impl/2025/1960/oj/fra) |
| Commission, "Practical guidelines on the harmonised notice and label" (DG JUST, 1 April 2026) | §2.1: no element or text may be edited; proportions kept; use the official files. §2.3 digital display: the colour RGB version, the full notice, "must always be legible at default display size", and "a clickable link to the same destination as the QR code should always be available"; examples: on the product page, the site header or the checkout page "add a sentence informing consumers about their legal guarantee rights (e.g. 'Your legal guarantee rights'), where the harmonised notice shall then appear on the first mouse click or mouse roll-over"; "the harmonised notice should also be included in the confirmation email". Language destinations: EN `europa.eu/youreurope/guarantees`, NL `europa.eu/youreurope/garantie`, FR `europa.eu/youreurope/garanties`. | | [PDF](https://commission.europa.eu/document/download/3e4dbee6-8184-4256-923d-c52551c7e9f0_en?filename=Practical+guidelines+Harmonised+Label%26Notice+product+guarantees_ARES+27042026.pdf) |
| Commission, official files | SVG, PNG/JPG and PDF sets in all 24 languages, colour and black and white. | Published 19 March 2026. | [High-resolution vector files](https://commission.europa.eu/publications/high-resolution-vector-files-eu-notice-and-label-product-guarantees_en) |
| Belgium: Act of 22 July 2026 (Justel W 2026-07-22/06) | **Art. VI.2, 5°** (general information duty) and **Art. VI.45 §1, 12°** (distance contracts): the reminder of the legal guarantee "die op een in het oog springende manier wordt verstrekt met behulp van de … geharmoniseerde kennisgeving"; **Art. VI.2/2** and **Art. VI.45 §1/1**: form and content "identiek aan de vorm en de inhoud bepaald in de Uitvoeringsverordening (EU) 2025/1960". Art. VI.45 §1, 22° and §1/1 do the same for the durability label. | In force **27 September 2026**. | Justel, links above (Boek VI, Titel 2 and Titel 3) |

### B2. What the notice must be

| Point | Rule | Applied |
|---|---|---|
| Layout and text | Fixed: the Commission's file, no edits, no cropping, no colour change, proportions kept (A4, 595.28 × 841.89 units). The text is the one in the file per language (EN "Legal guarantee / Minimum two-year legal guarantee protection for goods sold in the European Union …", NL "Wettelijke garantie / Minimaal twee jaar bescherming dankzij de wettelijke garantie …", FR "Garantie légale / Protection offerte par la garantie légale minimale de deux ans …"; full wording in the snippet's accessible description). | The three official SVGs are in the theme unchanged: `assets/kc-legal-guarantee-notice-en.svg`, `-nl.svg`, `-fr.svg` (SHA-256 of the EN file equals the Commission's download). Rendered as `<img>` from the theme's assets: no hotlink. |
| Graphic | The shield-with-G logo, the EU stars, the QR code and the GARAN example are part of the file; none may be lifted out or reused on its own. | The summary line that opens the notice uses no logo, only text and a chevron. |
| Colour | Online: colour RGB. | Colour files only; the image sits on the white the Regulation prescribes (#FFFFFF), on Day and Night alike. |
| Size | Off line: minimum A4. Online: no pixel minimum; legible at default display size; the whole notice visible. | On the product page the notice opens at the buybox width (about 520 px on desktop; 350 px at 390 px wide, zoomable). A "full size" link opens the file itself, and the legal page can show it at 720 px (handoff). |
| Link | A clickable link to the same destination as the QR code, always available. | Under the image, in the storefront language (`link_label`); the destination follows the language. |
| Language | The language of the offer. | `request.locale` picks EN, NL or FR. |
| Accessibility | (Guidelines are silent.) | The image has a short alt and an `aria-describedby` transcript of the full wording. |
| When and where | Before the consumer is bound (pre-contractual, Art. VI.45 §1 WER): prominently, as a general reminder on the website; Commission examples: product page, header or checkout behind a "Your legal guarantee rights" line; plus the confirmation email. The notice is **not** among the items Art. 8(2) CRD requires "directly before the consumer places his order" (those are (a), (e), (la), (o), (p)), so the checkout step is an example, not a duty. | Product pages: block "Legal guarantee notice (EU)" in `sections/main-product.liquid`, placed in both product templates after the trust row and before the treatment journey, under the plan card; the Loop widget and the buy button keep their places. Cart: this theme has no cart page (`templates/cart.json` redirects to checkout) and the drawer is not rendered, so nothing to add there. Checkout: on a non-Plus plan the information step takes no custom content; the order confirmation email gets the notice and the link instead (ADMIN-STEPS step 5). Site-wide reminder: handoffs to the global lane (footer line) and gate-legal (Consumer Rights §4). |
| Not to confuse with | The GARAN durability label is for a producer's commercial guarantee of durability of more than two years, at no extra cost, covering the whole good. Karmicare offers none; the 60-day money-back guarantee is a different commercial guarantee. | No GARAN label anywhere; the money-back guarantee keeps its own wording and never borrows the notice's look. |

---

## Part C: checks run on this build

| Check | Result |
|---|---|
| Theme Check (`shopify theme check --fail-level error`) | 0 errors, 19 warnings (baseline), exit 0. |
| JavaScript syntax (`node --check assets/kc-withdrawal.js`) | OK. |
| Template JSON (`product.json`, `product.subscription-item.json`, `page.withdrawal.json`) | Parse OK; block present in both product templates. |
| Keyboard and focus | Every control is a native `button`, `input`, `textarea`, `details/summary` or `a`. Focus moves to the step title when a step opens, to the first invalid field on an error, to the status box after the redirect (`autofocus`, `tabindex="-1"`). Focus rings: 2 px `--kc-mapped-border-focus-strong` with offset on fields, buttons (via `button-styles.liquid`), links, summary and the status boxes. Enter in a field goes to the review step, not past it. |
| Day and Night | Only mapped tokens (`--kc-mapped-*`, `--kc-responsive-*`, `--kc-shape-*`); no hex except the Regulation's white behind the notice. Status surfaces: `surface-status-default` with `text-status-body` (Day #efece8/#212a49, Night #212a49/#efece8). Error messages keep the heading colour with a red mark, so contrast holds on both. |
| 390 and 1440 px | One column, 720 px max, 20 px gutter; at 390 the form is 350 px wide, buttons full width, review rows stack, step markers wrap. At 1440 the column centres; nothing stretches. Headless Chrome cannot start inside this sandbox (process-singleton socket refused) and theme dev is out of bounds, so this is by construction, not by screenshot: Victor's preview on the dev theme is the visual check. |
| EN, NL and FR lengths | TRANSLATIONS-HANDOFF.md §4: longest button "Vérifier votre déclaration" fits 350 px; NL/FR headings wrap to two lines by design. |
| Error states | Client: required name, order number, email; email format; messages inline with `aria-invalid`, `aria-describedby`, live region. Server: Shopify's `form.errors` renders an alert with links to the fields. Network: if the Klaviyo event fails the native post still goes out and the success text falls back to "we acknowledge receipt by email" (care@ sends it by hand from the inbox copy). Double submit blocked. |
| No tracking | The page's own code makes no request before Confirm and one request after it (Klaviyo event, only when the key is set). No cookies, no storage except one sessionStorage key that is removed on the next page view. |
| Not verified here | Rendering in Shopify (no `theme dev`, no admin), Shopify's spam-challenge round trip, the actual Klaviyo delivery and its transactional approval. These are Victor's steps in ADMIN-STEPS.md with a test plan. |

---

## Handoffs

- **gate-legal**: (1) Terms 4.1 and Consumer Rights 3.1 must name the function and its place, with a link to `/pages/withdrawal` (Art. VI.45 §1, 8° WER); the model-form caption should use the statutory heading only. (2) Show the notice on the Consumer Rights page at full column width: `{% render 'kc-legal-guarantee-notice', id: section.id, layout: 'inline', link_label: '…', full_size_label: '…' %}` inside section 4, or a block that calls it. (3) Keep the refund sentence in `success_next_steps` in step with the corrected clause (14 days from the day of notice; may withhold until the goods or proof of sending arrive, Art. VI.50 WER). (4) Privacy Policy: Klaviyo as processor for the acknowledgement; the withdrawal statement as a processing purpose with its retention.
- **Global lane (footer)**: add the menu link "Withdraw from contract here" (NL "Hier de overeenkomst herroepen", FR "Renoncer au contrat ici") to the footer legal menu, and optionally a "Your legal guarantee rights" link to the Consumer Rights section 4 as the site-wide reminder. The menu step for Victor is in ADMIN-STEPS step 3; `sections/footer.liquid` is untouched here.
- **gate-consent**: the withdrawal page itself loads no tracker; app embeds still load site-wide.
- **Victor**: ADMIN-STEPS.md (page, menus, emails, Klaviyo, test).
