# R57b · Admin steps for Victor (consumer-rights text, durable-medium gate, legacy pages, redirects)

**Created**: 2026-10-24 (R57), rewritten for R57b the same day · lane gate-legal · do these in this order. Nothing here was done by the lane; every step is a Shopify, Loop or mail write and is yours. Expected time: about 90 minutes plus the test orders.

**Go/no-go for opening the corrected sales flow** (LR1 blocker 1, audit P0-11):

| Gate | What must be true | Evidence |
|---|---|---|
| G1 | Step 0 is done: the order confirmation and Loop's first-membership email carry the Terms, the withdrawal information, the model form and the guarantee conditions in a retainable form, in the customer's language | a real received email per plan and per language, saved as `.eml` or PDF |
| G2 | `/pages/withdrawal` is live in EN, NL and FR (gate-withdrawal) and the links in the new text open it | step 9 |
| G3 | The theme release with the R57b templates, the policy pastes (steps 1 and 2), the NL/FR theme translations (step 3) and the withdrawal page go live in the same window | step 9 |

**Before you start**: keep a copy of the current policy bodies (Settings → Policies → each policy → `<>` → select all → copy into a text file). The live bodies of 24 Oct are also the “Old” text in `CHANGES.md`.

## 0. Launch gate G1: confirmation on a durable medium

**Why**: Art. VI.46 §7 WER requires the confirmation of the contract on a durable medium within a reasonable time and at the latest at delivery, containing all the pre-contract information of Art. VI.45 §1: the Terms, the withdrawal conditions and procedure, the model form and the place of the online withdrawal function. Art. 1649septies §2 of the old Civil Code requires the commercial-guarantee conditions (Terms 4.2 to 4.5) on a durable medium by delivery. Terms 2.6 and 3.3 promise exactly that “with your order confirmation”. A link to a page we can change is not a durable medium (CJEU C-49/11, Content Services); the text itself in the email is. This is separate from the immediate acknowledgement the withdrawal function sends (Art. VI.61/2 §4, gate-withdrawal). Do not treat an email defect as automatically extending the withdrawal period; that consequence attaches to missing withdrawal information specifically.

**Shopify order confirmation** (every Try Once order and the first order of every membership). Path: **Settings → Notifications → Customer notifications → Order confirmation → Edit code**.

| Field | Old value | New value |
|---|---|---|
| Email body, below the order summary and above the footer | no legal text (verify in Preview) | a block headed “Your contract and your rights” containing, in this order: (a) the line “Terms and Conditions, version 4.5 of [paste date], KARMICA BV”; (b) the **full Terms text** (paste the EN HTML from `POLICIES-PASTE.md`, “English · Terms of service”; it includes clause 4 with the withdrawal information and the Annex with the model form); (c) the links `https://[store]/policies/terms-of-service`, `https://[store]/pages/withdrawal` (“Withdraw from contract here”) and the model-form PDF (step 8), as additional conveniences, not as the only carrier |
| Same, Dutch | — | Translate & Adapt → Notifications → Order confirmation → Dutch: the same block with the NL body from `POLICIES-PASTE.md` and the `/nl/` links |
| Same, French | — | Translate & Adapt → Notifications → Order confirmation → French: the FR body and the `/fr/` links |

Option if you prefer Liquid: `{{ shop.terms_of_service.body }}` inserted in the template renders the policy text at send time; accept it only if **Preview** shows the full text in each language, because a Liquid include that renders empty or in the wrong language fails the gate. Whichever option, log in `legal/CHANGELOG.md` that the email carries v4.5 and re-paste when the Terms change.

**Loop first-membership email** (the email Loop sends when a 60-Day rhythm or Year membership is created; Shopify's order confirmation also goes out, but the membership contract and its renewal rules must reach the member with Loop's confirmation). Path: **Apps → Loop Subscriptions → Settings → Notifications → Emails → the “subscription created / activated” template → Edit**.

| Field | Old value | New value |
|---|---|---|
| Body, below the subscription summary | no legal text (verify) | the same “Your contract and your rights” block: version line, full Terms text, the three links. Loop keeps its own copy per language (it ignores Shopify translations): paste the NL and FR blocks in the Dutch and French tabs |

**Acceptance check (the evidence for G1)**: with the authorised real-order test LR1 already foresees, place one Try Once order and one membership order (60-Day rhythm; the Year if a test is feasible) in each of EN, NL and FR. Open each received email in a mail client, not in the admin preview. Confirm that it contains the version line, the full Terms with clause 4 (withdrawal: 14 days, refund within 14 days of notice, return within 14 days, loss-of-value rule), the Annex model form, the withdrawal-page link and the guarantee conditions, in the right language, and that the Loop email arrived for the membership. Save each email as `.eml` or PDF under `docs/launch-gate/legal/evidence/` with the order number and the send time. Until this evidence exists, the corrected sales flow is not open.

## 1. Paste the corrected English policies

Path: **Settings → Policies**.

| Policy | Field | Old value | New value |
|---|---|---|---|
| Terms of service | body (rich text; click `<>` “Show HTML” in the toolbar, select all, paste) | the body published on 24 Oct (v4.3 + 24-hour delivery times) | `POLICIES-PASTE.md` → “English · Terms of service” block |
| Refund policy | same | the body published on 24 Oct | `POLICIES-PASTE.md` → “English · Refund policy” block |

Save each. Leave Privacy policy, Shipping policy, Purchase options cancellation policy, Contact information and Legal notice as they are (their intro link is step 7). Do not switch Privacy policy to “Automated”.

## 2. Paste the Dutch and French policies

Path: **Apps → Translate & Adapt → Store policies** (or Settings → Languages → Translate & Adapt) → the policy → language tab.

| Policy | Language | Field | New value |
|---|---|---|---|
| Terms of service | Dutch | body → `<>` → select all → paste | `POLICIES-PASTE.md` → “Nederlands · Terms of service” |
| Terms of service | French | same | “Français · Terms of service” |
| Refund policy | Dutch | same | “Nederlands · Refund policy” |
| Refund policy | French | same | “Français · Refund policy” |

The NL and FR blocks are the live 24 Oct translations (batch-04, legal-review status) with exactly the R57 and R57b corrections applied, so the legal review of the NL/FR text (`docs/localization/*/REPORT.md` item 41) is still open after this paste.

## 3. Theme-page translations (NL and FR of the designed pages)

Source-copy registers the 15 settings in `TRANSLATIONS-HANDOFF.md`. If you do it by hand: Translate & Adapt → Online store → Theme (the live theme) → Templates → `page.terms-and-conditions` and `page.consumer-rights` → the settings listed in `TRANSLATIONS-HANDOFF.md` → paste the NL and FR values. The EN values arrive with the theme release. A handoff file or a registration log is not proof: open `/nl/pages/terms-and-conditions-1` and `/fr/pages/new-consumer-rights` afterwards (step 9).

## 4. Hide the three legacy pages

Path: **Online Store → Pages**. For each page: open → right-hand card “Visibility” → **Hidden** → Save. Hidden pages return 404 and leave the sitemap; nothing is deleted.

| Page (admin title) | Handle | Why |
|---|---|---|
| Consumer Rights | `consumer-rights` | a two-link stub from the old site, listed in the sitemap next to the current charter |
| Privacy Policy | `privacy` | the 2021 policy with template placeholders and bundled consent |
| Terms and Conditions | `terms-and-conditions` | the pre-2.0 terms (24 countries incl. US, we@ address, 30-day refund, void clauses) |

Do not hide “New Consumer Rights” (`new-consumer-rights`), “New Privacy Policy” (`privacy-policy`) or “New Terms and Conditions” (`terms-and-conditions-1`): those are the current pages the footer links.

## 5. Add the redirects

Path: **Online Store → Navigation → View URL redirects → Create URL redirect** (in newer admins: Content → Menus → URL redirects). Shopify refuses a redirect whose source is still a published page, hence step 4 first.

| Redirect from | Redirect to |
|---|---|
| `/pages/consumer-rights` | `/pages/new-consumer-rights` |
| `/pages/privacy` | `/pages/privacy-policy` |
| `/pages/terms-and-conditions` | `/pages/terms-and-conditions-1` |

Shopify normally applies a redirect to the `/nl/` and `/fr/` paths too; do not assume it: step 9 checks all nine locale paths one by one. Check the migration redirect CSV (LR1, `03-REDIRECTS.csv`; not part of this lane's inputs): any row that targets a legacy handle must target the designed page instead, and the Webflow rows `/en/pages/terms-and-conditions`, `/en/pages/privacy`, `/en/pages/consumer-rights` (and `/nl/…`, `/fr/…`) must point at the designed pages.

## 6. Page titles without “New” (optional, LR1 metadata item)

Path: **Online Store → Pages** → the page → Title. Keep the handle unchanged (the footer and the redirects use it).

| Page | Old title | New title |
|---|---|---|
| `terms-and-conditions-1` | New Terms and Conditions | Terms and Conditions |
| `new-consumer-rights` | New Consumer Rights | Consumer Rights |
| `privacy-policy` | New Privacy Policy | Privacy Policy |

Also the “Search engine listing” page title of each, if it was edited separately. The NL/FR titles live in Translate & Adapt → Pages (batch-04 `admin:page:*:title` entries).

## 7. Legacy Terms link in the four short policies (EN, NL, FR)

The first sentence of Shipping policy, Purchase options cancellation policy, Contact information and Legal notice links “Terms and Conditions” to `https://www.karmicare.com/en/pages/terms-and-conditions`, in all three languages (Astra, R57 review, observation 2). That address loses the language and will only work through the legacy redirect. Path: **Settings → Policies → the policy → select the link text “Terms and Conditions” → edit link**, then the same in Translate & Adapt for Dutch and French.

| Language | Old link target | New link target |
|---|---|---|
| English | `https://www.karmicare.com/en/pages/terms-and-conditions` | `/policies/terms-of-service` |
| Dutch (“Algemene Voorwaarden”) | same | `/nl/policies/terms-of-service` |
| French (“Conditions générales”) | same | `/fr/policies/terms-of-service` |

Four policies × three languages = twelve link edits; the text of those policies does not change.

## 8. Withdrawal form PDFs, last

Do this only after steps 1, 2 and 3 are complete and verified, because a whole-body paste or a translation registration overwrites these links (Astra, observation 3). Path: **Content → Files → Upload files**: `docs/launch-gate/input/legal-offer/legal/forms/karmicare-withdrawal-form-en.pdf`, `-nl.pdf`, `-fr.pdf`. Copy each file's URL. Then:

| Where | Field | Old value | New value |
|---|---|---|---|
| Settings → Policies → Terms of service, Annex | the words “Download the form (PDF)” | plain text, no link | link to the EN file URL |
| Settings → Policies → Refund policy, section 10 | same | plain text | link to the EN file URL |
| Translate & Adapt → Store policies → both policies → Dutch / French | “Download het formulier (PDF)” / “Télécharger le formulaire (PDF)” | plain text | link to the NL / FR file URL |
| Theme, EN: Customize → page “New Terms and Conditions” → block “Annex – Model withdrawal form” → content; page “New Consumer Rights” → block “10. Model withdrawal form” → content | the link “Download the form (PDF)” | `href="#"` | the EN file URL (or send the three URLs to the theme lane for a one-line commit on `content_section_fz6KEQ/content` and `content_section_at3pLy/content`) |
| Translate & Adapt → Theme → Templates → the same two settings → Dutch / French | the same link | `href="#"` | the NL / FR file URL |

Then open all twelve places (two policies and two designed pages, three languages) and click each PDF link. The inline model form is complete on every page, so the PDF is a convenience, not the only statutory form.

## 9. Check, publicly, before the domain switch

Open in a private window, slowly (the store rate-limits; one request every two seconds):

- `/policies/terms-of-service`, `/policies/refund-policy`, and the `/nl/…` and `/fr/…` versions: clause 4.1 says the refund runs from “the day we are informed”, 4.6.3 starts “Primed pumps and your right of withdrawal”, 4.7.4 starts “Care Credit and refunds” and says the statutory refund is never reduced, 10.6 says the same, 3.1 of the charter names the online withdrawal function, section 2 says the toothbrushes and the floss are not cosmetics, clause 7 says you choose between repair and replacement.
- `/pages/terms-and-conditions-1`, `/pages/new-consumer-rights` (EN, NL, FR): the same text as the policies, including the NL and FR of the 15 settings.
- The links “Withdraw from contract here” / “Hier de overeenkomst herroepen” / “Renoncer au contrat ici” open `/pages/withdrawal`, `/nl/pages/withdrawal`, `/fr/pages/withdrawal` (gate-withdrawal).
- Each of `/pages/consumer-rights`, `/pages/privacy`, `/pages/terms-and-conditions` and their `/nl/` and `/fr/` paths (nine URLs) returns a 301 to the designed page; `sitemap_pages_1.xml` no longer lists the three legacy handles.
- Checkout footer links (Refund policy, Terms of service, Privacy policy) open the corrected policies; the four short policies' first link opens the Terms in the page's language (step 7).
- The PDF links of step 8 work in all twelve places.

## 10. Then (not this lane)

- Legal-offer branch: log v4.5 in `legal/CHANGELOG.md`, update `legal/*/en.md` and the Figma legal frames from `CHANGES.md` §3 and §3b, add `nl.md` and `fr.md`.
- The NL/FR legal review (counsel or Victor) of the whole legal text stays open.
- Business setting: consider releasing earned Care Credit only after the 14-day withdrawal period (Loop), see `CHANGES.md` §6.
