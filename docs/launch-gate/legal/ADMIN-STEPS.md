# R57 · Admin steps for Victor (consumer-rights text, legacy pages, redirects)

**Created**: 2026-10-24 · lane gate-legal · do these in this order. Nothing here was done by the lane; every step is a Shopify admin write and is yours. Expected time: about 45 minutes.

**Before you start**

- The theme release that contains R57 (the corrected `page.terms-and-conditions` and `page.consumer-rights` templates) and the gate-withdrawal release (`/pages/withdrawal`) should go live in the same window as steps 1 and 2, because the new policy text links `/pages/withdrawal` and the designed pages must say the same as the policies. If the withdrawal page is not published yet, do steps 4 to 7 now and steps 1 to 3 together with that page.
- Keep a copy of the current policy bodies before pasting: Settings → Policies → each policy → `<>` → select all → copy into a text file. The live bodies of 24 Oct are also the “Old” text in `CHANGES.md`.

## 1. Paste the corrected English policies

Path: **Settings → Policies**.

| Policy | Field | Old value | New value |
|---|---|---|---|
| Terms of service | body (rich text; click `<>` “Show HTML” in the toolbar, select all, paste) | the body published on 24 Oct (v4.3 + 24-hour delivery times) | `POLICIES-PASTE.md` → “English · Terms of service” block |
| Refund policy | same | the body published on 24 Oct | `POLICIES-PASTE.md` → “English · Refund policy” block |

Save each. Leave Privacy policy, Shipping policy, Purchase options cancellation policy, Contact information and Legal notice as they are. Do not switch Privacy policy to “Automated”.

## 2. Paste the Dutch and French policies

Path: **Apps → Translate & Adapt → Store policies** (or Settings → Languages → Translate & Adapt) → the policy → language tab.

| Policy | Language | Field | New value |
|---|---|---|---|
| Terms of service | Dutch | body → `<>` → select all → paste | `POLICIES-PASTE.md` → “Nederlands · Terms of service” |
| Terms of service | French | same | “Français · Terms of service” |
| Refund policy | Dutch | same | “Nederlands · Refund policy” |
| Refund policy | French | same | “Français · Refund policy” |

The NL and FR blocks are the live 24 Oct translations (batch-04, legal-review status) with exactly the R57 corrections applied, so the legal review of the NL/FR text (`docs/localization/*/REPORT.md` item 41) is still open after this paste.

## 3. Theme-page translations (NL and FR of the designed pages)

Nothing to do by hand if source-copy runs its registration from `TRANSLATIONS-HANDOFF.md` (14 settings). If you prefer to do it by hand: Translate & Adapt → Online store → Theme (the live theme) → Templates → `page.terms-and-conditions` and `page.consumer-rights` → the settings listed in `TRANSLATIONS-HANDOFF.md` → paste the NL and FR values. The EN values arrive with the theme release.

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

Shopify applies the redirect to the `/nl/` and `/fr/` paths as well. Check the migration redirect CSV (LR1, `03-REDIRECTS.csv`): any row that targets a legacy handle must target the designed page instead, and the Webflow rows `/en/pages/terms-and-conditions`, `/en/pages/privacy`, `/en/pages/consumer-rights` (and `/nl/…`, `/fr/…`) must point at the designed pages.

## 6. Page titles without “New” (optional, LR1 metadata item)

Path: **Online Store → Pages** → the page → Title. Keep the handle unchanged (the footer and the redirects use it).

| Page | Old title | New title |
|---|---|---|
| `terms-and-conditions-1` | New Terms and Conditions | Terms and Conditions |
| `new-consumer-rights` | New Consumer Rights | Consumer Rights |
| `privacy-policy` | New Privacy Policy | Privacy Policy |

Also the “Search engine listing” page title of each, if it was edited separately. The NL/FR titles live in Translate & Adapt → Pages (batch-04 `admin:page:*:title` entries).

## 7. Withdrawal form PDFs

Path: **Content → Files → Upload files**: `docs/launch-gate/input/legal-offer/legal/forms/karmicare-withdrawal-form-en.pdf`, `-nl.pdf`, `-fr.pdf`. Copy each file's URL. Then:

- Settings → Policies → Terms of service and Refund policy → in the Annex / section 10, select “Download the form (PDF)” → link it to the EN file URL; the same in Translate & Adapt for NL (`-nl.pdf`) and FR (`-fr.pdf`).
- The designed pages: the same link sits in the template settings (`content_section_fz6KEQ/content` on the Terms page, `content_section_at3pLy/content` on the Consumer Rights page) with `href="#"`. Either set it in the theme editor (Customize → the page → block “Annex – Model withdrawal form” / “10. Model withdrawal form” → the link in the content field) or send the three URLs to the theme lane for a one-line commit.

## 8. Check, publicly, before the domain switch

Open in a private window, slowly (the store rate-limits):

- `/policies/terms-of-service`, `/policies/refund-policy`, and the `/nl/…` and `/fr/…` versions: clause 4.1 says the refund runs from “the day we are informed”, 4.6.3 starts “Primed pumps and your right of withdrawal”, 3.1 of the charter names the online withdrawal function, section 2 says the toothbrushes and the floss are not cosmetics, clause 7 says you choose between repair and replacement.
- `/pages/terms-and-conditions-1`, `/pages/new-consumer-rights` (EN, NL, FR): the same text as the policies.
- The links “Withdraw from contract here” open `/pages/withdrawal` (gate-withdrawal) in each language.
- `/pages/consumer-rights`, `/pages/privacy`, `/pages/terms-and-conditions` redirect (301) to the designed pages; `sitemap_pages_1.xml` no longer lists them.
- Checkout footer links (Refund policy, Terms of service, Privacy policy) open the corrected policies.

## 9. Then (not this lane)

- Order confirmation and Loop's first-membership email: attach or paste the corrected Terms with the withdrawal information and the model form (durable medium, audit P0-11).
- Legal-offer branch: log v4.5 in `legal/CHANGELOG.md`, update `legal/*/en.md` and the Figma legal frames from `CHANGES.md`.
- The NL/FR legal review (counsel or Victor) of the whole legal text stays open.
