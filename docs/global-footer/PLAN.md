# Footer newsletter → Klaviyo: plan (Phase 1)

**Created**: 2026-10-21 · worker global-footer, branch `karmicare/global-footer` (from `karmicare/soft-launch-global` 68dba1f)

### Changelog
| Date | Change |
|------|--------|
| 2026-10-21 | Phase 1: theme inventory, read-only Klaviyo inventory via the `klaviyo` MCP (`?read-only=true`), route, payload, settings, notice proposal, decisions D1–D6 for Victor. No theme code. |

Everything marked **verified** was checked today (theme files, the live storefront HTML fetched once, the Klaviyo MCP, one CORS preflight with no data). Everything marked *open* is for Victor in Klaviyo's or Shopify's UI (§8).

## 0. Short version

- Route **b**: the footer form keeps Shopify's native `{% form 'customer' %}`; a small theme script intercepts submit and posts to Klaviyo's browser endpoint `POST https://a.klaviyo.com/client/subscriptions?company_id=XfYq2r` with the public key only. No klaviyo.js of our own, no cookie, no request before submit. If JS is off, the key is empty or Klaviyo is unreachable, the native form submits as today.
- Lists: one double-opt-in list per language. Reuse **Dutch Speakers** `UPaLXW` and **English Speakers** `YiN3Ba` (both DOI, created 5 Jan 2026), create **French Speakers** (DOI) in Klaviyo's UI. Keep the **Shopify** list `TNLGVv` as the Shopify-sync target for checkout opt-ins.
- Payload: email + `locale` (`nl-BE` / `fr-BE` / `en`) + `custom_source` `Footer newsletter · <lang>` + properties `signup_path`, `consent_text_version`. No name, no `external_id`.
- Found on the way: klaviyo.js is **already live** on the storefront through a Shopify ScriptTag without a consent check (not from the theme); a Webflow-era Klaviyo banner form is still live (URL-targeted); the Klaviyo account address says "United States". All three are Victor's to fix in the UI (§8), none blocks this build.

## 1. Theme inventory (verified)

### 1.1 Footer form
`sections/footer.liquid` L702–747, shown when `section.settings.newsletter_enable` (true in `sections/footer-group.json`).

| Part | Today |
|------|-------|
| Form | `{% form 'customer', id: 'FooterNewsletterForm', class: 'km-footer-field' %}` → Shopify posts to `/contact` and reloads the page. Hidden `contact[tags]=newsletter`. |
| Field | `<label for="FooterNewsletterEmail">` (`kc.footer.email` = "Email"), `<input type="email" name="contact[email]" required autocomplete="email">`, placeholder `kc.footer.email_placeholder` (`you@example.com` / `jij@voorbeeld.be` / `vous@exemple.be`), submit `kc.footer.join` ("Join" / "Doe mee" / "S’inscrire"). |
| Error state | Liquid only: `aria-invalid="true"` + `aria-describedby="FooterNewsletterEmail-message"`, `<p role="alert">` with Shopify's `form.errors` text. |
| Success state | Liquid only: `<p role="status">` with `newsletter.success` ("Thanks for subscribing" / "Bedankt voor het abonneren" / "Merci de votre inscription"). |
| Notice | `<p class="km-footer-newsletter__note">` with `kc.footer.consent_html`: EN "By subscribing you agree to the Terms of Use & Privacy Policy." NL "Door je in te schrijven, ga je akkoord met de Gebruiksvoorwaarden en het Privacybeleid." FR "En vous inscrivant, vous acceptez les conditions d’utilisation et la politique de confidentialité." Links from `legal_terms` / `legal_privacy` (L626–639: section page setting → `pages['privacy-policy']` → `shop.privacy_policy`). The notice is **not** linked to the input with `aria-describedby`. |
| No-JS | Works today: plain POST, page reload, Shopify renders error or success. Nothing in the theme touches this form with JS (`git grep` for `FooterNewsletterForm` hits only the section). |
| Section settings | Only `newsletter_enable` and `newsletter_heading` (schema L1047–1062). No Klaviyo key or list settings yet. |
| Styles | `.km-footer-field__message` L257–270 (one style for error and success), submit hover/focus L247–256. |

### 1.2 Other signup forms
- `sections/newsletter.liquid` (Dawn): same `form 'customer'` + `contact[tags]=newsletter`. Not placed in any template or section group.
- `sections/email-signup-banner.liquid` (Dawn): same form. Placed only in `templates/password.json`.
- Checkout marketing opt-in: a Shopify checkout setting, not in the theme. It feeds Shopify's consent status, which Klaviyo's Shopify sync reads (§2.4, §4).
- Klaviyo forms: none embedded in the theme. `config/settings_data.json` has only Judge.me and Loop app embeds (L206–223). But see §1.4: klaviyo.js is live, so Klaviyo-hosted forms *can* render.

### 1.3 Consent banner
- The live page loads Shopify's banner `cdn/shopifycloud/privacy-banner/storefront-banner.js` (Shopify Customer Privacy, a Shopify admin setting).
- `assets/kc-cookie-preferences.js` (loaded from `layout/theme.liquid` L444–445) only restyles that banner into a preferences panel. No theme code reads `Shopify.customerPrivacy` / `trackingConsent` (`grep` over layout, snippets, assets, sections: 0 hits besides `Shopify.loadFeatures` in `product-model.js`).
- The footer form itself needs no consent gate: route b sends one request on submit and sets no cookie.

### 1.4 Klaviyo on the live storefront today
- The homepage HTML contains a Shopify **ScriptTag** loader (`function asyncLoad() { var urls = ["https://static.klaviyo.com/onsite/js/XfYq2r/klaviyo.js?company_id=XfYq2r&shop=karmicares.myshopify.com", …] }`, run on `window.onload`). That block has no consent check (0 hits for `customerPrivacy`, `trackingConsent`, `marketingAllowed` in the page). Whether klaviyo.js itself waits for consent before setting `__kla_id` cannot be read from HTML: *open*, checklist §8 item 8.
- Shopify's web-pixels manager is present; which pixels (Klaviyo's) run is admin-side.
- Consequence for this plan: route b does not add a third-party script. It also does not depend on klaviyo.js, so it keeps working if Victor later gates or removes the ScriptTag.

### 1.5 Privacy policy (`templates/page.privacy-policy.json`)
Already says what the footer needs: Klaviyo, Inc. (US) as processor for "transactional and promotional email, cart reminders (only if you opted in) and list management"; newsletter legal basis "explicit prior consent (Art. 6(1)(a) GDPR)"; newsletter data kept "until you withdraw consent or unsubscribe", removed after 24 months of inactivity; right to withdraw consent for newsletters at any time; marketing cookies including Klaviyo "only after your explicit consent". No policy change needed for route b.

### 1.6 Related open items in other lanes
- `docs/global/GAP-LIST.md` FT-08 / G-4: the FR consent line and legal labels were held for legal review; 4954820 shipped the FR texts. The new notice (§9) replaces `kc.footer.consent_html` in all three languages, so FT-08's text becomes obsolete when Phase 2 lands.
- Locale keys are written only by `docs/localization/theme_keys.py` (source-copy lane). Phase 2 lists new keys in `docs/global-footer/KEYS.md`.

## 2. Klaviyo inventory (read-only MCP, 21 Oct 2026)

### 2.1 Account
| Item | Value |
|------|-------|
| Account / public key (company_id) | `XfYq2r` (`get_account_details.public_api_key`) |
| Organisation, sender | Karmicare · KARMICARE `<we@karmicare.com>` |
| Sending domain | `send.karmicare.com`, status active, purpose marketing (since 26 Nov 2024) |
| Timezone, currency, account locale | Europe/Brussels · EUR · en-US |
| Address | Vizierstraat 28, 8000 Bruges, West Flanders, **country "United States"** → §8 item 7 |
| Webhooks | none |
| Tags | blackfriday, bleedinggums, fair, ORTH-therapeut, postpurchase, science, VGBC2025 |

### 2.2 Lists (11)
| List | ID | Created | Opt-in | Profiles | Note |
|------|----|---------|--------|----------|------|
| Dutch Speakers | `UPaLXW` | 2026-01-05 | double | 1 351 | candidate NL footer list |
| English Speakers | `YiN3Ba` | 2026-01-05 | double | 1 106 | candidate EN footer list |
| Non-dutch speakers (EN as default) (list) | `SRkitd` | 2025-10-07 | double | 2 167 | overlaps English Speakers; not touched |
| MA \| Bleeding Gums \| 26/2/25 | `UVKDNX` | 2025-02-26 | double | 1 | tag bleedinggums; triggers draft flow `RSdfrs` |
| **Webflow** | `Y8tAjz` | 2025-01-22 | double | 31 | Webflow-era; no proof of consent assumed; never import as subscribed |
| Shopify | `TNLGVv` | 2024-11-21 | **single** | 2 640 | name of the list Klaviyo's Shopify integration creates; probably the sync target (*open*) |
| KARMICARE | `V5SyfZ` | 2024-11-21 | double | 1 543 | origin unknown |
| Mailchimp | `YriynH` | 2024-11-21 | single | 1 541 | Mailchimp import (Mailchimp metrics exist) |
| Preview List | `TqZBVQ` | 2024-11-15 | double | 0 | Klaviyo default |
| Email List | `UF3Hb6` | 2024-11-15 | double | 0 | Klaviyo default |
| SMS List | `UUVudg` | 2024-11-15 | double | — | not relevant |

No French list exists. The two language lists are from January 2026; how they were filled (import or split) is not visible: *open*, §8 item 4. The DOI setting of a list applies to new signups only.

### 2.3 Segments (3) and flows (5)
- Segments: `[TOTAL profiles]` `Sagwcw` (starred) · `Post Purchase | Past profiles - 96 days` `V8fuqF` · `Never Engaged (Email)` `Vz6UKR`.
- Flows: Abandoned checkout `RjSTNU` live (metric) · Post-Purchase Followup `TaNMrL` live (metric) · Never Engaged sunset `XXWQN6` live (trigger: segment `Vz6UKR`) · MA Bleeding Gums `RSdfrs` draft (list `UVKDNX`) · MA Post purchase past profiles `TNFMKm` draft (segment `V8fuqF`).
- **No welcome flow** is attached to any language list. Not a blocker; Victor's choice later (Klaviyo UI).

### 2.4 Forms (8) and integrations
- Forms: 7 drafts (BF2024 Offer, Oral Lead Magnet ×2, Offer today-only deals, Black Friday deals, Holiday Sale Snowfall, MA Bleeding Gums). **"Free shipping banner" `WbGdHc` has a live version**: bottom banner, "FREE shipping on all orders over $150.", shown to unidentified visitors on URLs matching `*/en/pages/privacy*` or `utm_campaign=testwebflow`. With klaviyo.js live (§1.4) it can appear on `/en/pages/privacy-policy`. → §8 item 5.
- Metrics show these integrations: Shopify (orders, checkout, Added to Cart since Aug 2026, Viewed Collection since Sep 2026 → onsite tracking is on), Loop Subscriptions (Aug 2026 →), API (Active on Site, Viewed Product, form metrics from the Webflow era), Mailchimp and Stripe (Nov 2024, historic).

### 2.5 What the MCP cannot show
Shopify-integration settings (subscriber sync on/off and target list, Klaviyo→Shopify sync, onsite tracking mode), per-list double-opt-in email text and language, Shopify's "Customer marketing confirmation" setting, the Webflow connection, cookies set before consent. All in §8.

## 3. Route and why

**Route b, verified today**:
- `OPTIONS https://a.klaviyo.com/client/subscriptions?company_id=XfYq2r` with `Origin: https://karmicares.myshopify.com`, `Access-Control-Request-Method: POST`, `Access-Control-Request-Headers: content-type,revision` → `200`, `access-control-allow-origin: *`, `access-control-allow-headers: content-type, revision`, `access-control-max-age: 86400`, `allow: GET, POST, HEAD, OPTIONS`. CORS from the storefront works (the research's *unverified* item is closed). No data was sent.
- Reference page `create_client_subscription`: default `revision` **`2026-10-15`**, body media type `application/vnd.api+json`, success `202`, limits 350/s burst and 750/min. With a list in `relationships`, the **list's** opt-in setting decides (account default ignored).
- Klaviyo's double-opt-in article: for API submissions no profile is created until the person confirms; the confirmation mail is valid 72 h.

Why not **a** (native form + Shopify subscriber sync only): language not guaranteed on form-created profiles, no source, one sync target for all languages, and a second confirmation mail if Shopify's own confirmation is on.
Why not **c** (Klaviyo-hosted form via klaviyo.js): copy, states and accessibility would live in Klaviyo, not in the theme; cookie behaviour before consent is unverified; klaviyo.js may later be gated or removed.

Fallback rule: the native form stays the fallback. The script only takes over when the section has a public key **and** a list ID for the current language (§7).

## 4. List design

| Purpose | List | Action |
|---------|------|--------|
| Footer NL | Dutch Speakers `UPaLXW` (DOI) | reuse |
| Footer FR | **French Speakers** (new, DOI) | Victor creates it in Klaviyo's UI; ID goes into the setting |
| Footer EN | English Speakers `YiN3Ba` (DOI) | reuse |
| Checkout / Shopify consent | Shopify `TNLGVv` (single opt-in) | keep as the Shopify-sync target; optionally rename to "Shopify · checkout opt-in" (ID unchanged) |

- Alternative (D2-b): three fresh "Footer · NL/FR/EN" lists. Cleaner provenance, but campaigns and flows would need a fifth and sixth audience. Recommended: reuse + one new FR list, because the footer signups carry their own consent record (`custom_source`, `consent_text_version`, Klaviyo's `consent_timestamp`, `double_optin`) whatever list they land in.
- Per list Victor checks the double-opt-in confirmation mail language (NL / FR / EN): §8 item 3. The language of that mail is the reason for one list per language.
- Campaign audience stays a segment (can receive email marketing + language list or `locale`), as today.
- `Non-dutch speakers (EN as default)` `SRkitd`: overlap with English Speakers; decide later, not needed for the footer.
- Webflow `Y8tAjz`: untouched; never imported as subscribed (APD §87, no proof of consent).

## 5. Request payload (exact)

Headers: `Content-Type: application/vnd.api+json`, `revision: 2026-10-15`. Query: `company_id=XfYq2r` (public key). Method `POST`, no credentials, no cookies.

```json
{
  "data": {
    "type": "subscription",
    "attributes": {
      "custom_source": "Footer newsletter · nl",
      "profile": {
        "data": {
          "type": "profile",
          "attributes": {
            "email": "<the address typed>",
            "locale": "nl-BE",
            "properties": {
              "signup_path": "/nl/products/oral-care",
              "consent_text_version": "footer-2026-10"
            },
            "subscriptions": {
              "email": { "marketing": { "consent": "SUBSCRIBED" } }
            }
          }
        }
      }
    },
    "relationships": {
      "list": { "data": { "type": "list", "id": "UPaLXW" } }
    }
  }
}
```

| Field | Source | Values |
|-------|--------|--------|
| list id | section setting for the language (§7) | `UPaLXW` · `<FR id>` · `YiN3Ba` |
| `locale` | `request.locale.iso_code` rendered as `data-locale` | `nl` → `nl-BE`, `fr` → `fr-BE`, `en` and anything else → `en` (the live shop publishes exactly `en`, `nl`, `fr`, verified from `hreflang`) |
| `custom_source` | fixed per language | `Footer newsletter · nl` / `· fr` / `· en` |
| `signup_path` | `location.pathname` at submit | e.g. `/fr/pages/contact` |
| `consent_text_version` | constant in the asset, bumped when the notice text changes | `footer-2026-10` |
| `consent` | fixed | `SUBSCRIBED` (the list's double opt-in turns it into pending until confirmed) |

Not sent: name, `external_id`, phone, IP, user agent, `$source` (legacy). Klaviyo adds `consent_timestamp`, `method` (API), `method_detail`, `custom_method_detail` (= `custom_source`), `double_optin`.

## 6. Behaviour

Progressive enhancement on `#FooterNewsletterForm`; markup stays `{% form 'customer' %}`.

1. **Activation**: the script runs only when the form has `data-klaviyo-key` and `data-klaviyo-list` (both non-empty). Otherwise it does nothing and the native POST runs as today.
2. **Submit**: `preventDefault`, `input.checkValidity()` (browser validation stays: `type="email"`, `required`), set busy (`aria-busy="true"` on the form, submit `disabled`, label kept), `fetch` with an 8 s `AbortController` timeout.
3. **202** → clear the input, re-enable, write one neutral message into the existing `role="status"` region: *"Check your inbox to confirm your subscription."* The same text for new, already subscribed, unsubscribed and suppressed addresses (all return 202).
4. **4xx** (Klaviyo rejects the address) → `aria-invalid="true"`, `aria-describedby` → message id, `role="alert"` text *"Check the email address."*, focus back on the input, no native submit.
5. **429, 5xx, network error, timeout** → D5: submit the native form (`form.submit()`), so the signup still lands in Shopify and the person sees Shopify's result page. Alternative: show the error only.
6. **No request before submit**: the asset has no top-level network call; `fetch` exists only inside the submit handler; no script is loaded from Klaviyo. Proof in Phase 2: DevTools Network filtered on `klaviyo` on page load shows only the pre-existing ScriptTag (§1.4), none from the theme, plus `grep -n fetch assets/kc-footer-newsletter.js` in the commit body showing one call inside the handler.
7. **Accessibility**: visible label stays; the notice gets `id="FooterNewsletterEmail-note"` and the input always carries it in `aria-describedby` (error/success id added when shown); the status element exists in the DOM from render (empty) so the injected text is announced (WCAG 4.1.3); errors as text + `aria-invalid` (WCAG 3.3.1); busy button stays readable (the theme's "pending stays opaque" rule, 99342f0).
8. **Reload/back**: nothing stored client-side; a second submit is a second request (Klaviyo dedupes by email).

Files in Phase 2: `sections/footer.liquid` (settings, data attributes, note id, messages) and one asset `assets/kc-footer-newsletter.js` (≈80 lines, no dependencies, loaded `defer`). No locale edits (keys via `KEYS.md`).

## 7. Where the key and list IDs live

New section settings under the existing "Newsletter Settings" header in `sections/footer.liquid`:

| Setting | Type | Default | Info text |
|---------|------|---------|-----------|
| `klaviyo_public_key` | text | empty | "Klaviyo public API key / Site ID (6 characters, e.g. XfYq2r). Empty = native Shopify form. Never a private key." |
| `klaviyo_list_nl` | text | empty | "Klaviyo list ID for Dutch signups (double opt-in)." |
| `klaviyo_list_fr` | text | empty | "… French …" |
| `klaviyo_list_en` | text | empty | "… English …" |

Liquid picks the list by `request.locale.iso_code`; with an empty key or an empty list for that language the form renders without `data-klaviyo-*` and stays native. The public key and list IDs are public identifiers (they appear in every Klaviyo form on the web); no private key or token anywhere.

Values: the schema defaults stay empty. For Victor's test on the dev theme he fills them in that theme's editor. After the test the values go into `sections/footer-group.json` in a commit (D6-b), so a later theme push cannot wipe them; alternative D6-a: Victor sets them in the live theme's editor after DH ships and nobody commits them.

## 8. Checklist for Victor (UI only, the MCP cannot see these)

1. **Klaviyo → Integrations → Shopify**: is "Sync your Shopify email subscribers" on, and which list? Expected: Shopify `TNLGVv`. Is "Sync Klaviyo profiles to Shopify" on, and in which mode? Is onsite tracking on via app embed or the old ScriptTag (§1.4)?
2. **Shopify admin → Settings → Customer privacy / Notifications**: is "Customer marketing confirmation" (Shopify's own double opt-in) on? If on, native-fallback signups get Shopify's mail *and*, after sync, maybe Klaviyo's. Recommended: off for the online store once route b is live, unless you want Shopify's mail for the fallback.
3. **Each language list → Settings → Double opt-in**: confirmation email and success page in that list's language (NL for `UPaLXW`, FR for the new list, EN for `YiN3Ba`); sender KARMICARE `<we@karmicare.com>`.
4. **Dutch Speakers / English Speakers**: how were the 1 351 / 1 106 profiles added (import, split, migration)? Only needed to know whether a welcome flow on these lists is safe.
5. **Form "Free shipping banner" `WbGdHc`**: unpublish or archive (Webflow test, prices in $).
6. **Webflow list `Y8tAjz` and the Webflow integration**: disconnect if still connected; do not import the 31 profiles as subscribed.
7. **Account → Contact information**: country "United States" → Belgium (this address goes into every email footer).
8. **Cookie check** (private window, `/nl`, before touching the banner): DevTools → Application → Cookies for `__kla_id`, and Network for `klaviyo.js`. If klaviyo.js loads or the cookie is set before consent, that is a separate task for the global lane (move Klaviyo to the consent-aware app embed or gate the ScriptTag), not this child.
9. **Settings → API keys**: confirm the public key `XfYq2r`.
10. Later: decide what `Non-dutch speakers (EN as default)` `SRkitd` is for next to English Speakers.

## 9. Notice proposal (EN)

Today: "By subscribing you agree to the Terms of Use & Privacy Policy." (bundles consent with the terms; says nothing about what people get or how to leave).

Proposed `kc.footer.consent_html`:

> Occasional emails from KARMICARE about Awake & Asleep, the Dental Check-up Reward and member offers. Unsubscribe any time with the link in every email. <a href="{{ privacy_url }}">Privacy Policy</a>.

- Who: KARMICARE. What: product news, the Check-up Reward, member offers (all already on the site: PDP, privacy policy, announcement bar). Withdrawal: "Unsubscribe any time". Privacy link visible. No terms link, no "agree".
- Brand rules: Awake before Asleep; no commodity words; no claims; Care Credit not mentioned.
- Shorter variant if the column is tight: "Occasional emails from KARMICARE: Awake & Asleep news, the Check-up Reward, member offers. Unsubscribe any time. Privacy Policy."
- New keys for `KEYS.md` in Phase 2 (EN text; NL and FR via the source-copy lane): `kc.footer.consent_html` (above), `kc.footer.check_inbox` "Check your inbox to confirm your subscription.", `kc.footer.email_invalid` "Check the email address."

## 10. Decisions for Victor

| # | Decision | Options | Recommendation |
|---|----------|---------|----------------|
| D1 | Route | **a** native form + Shopify sync only · **b** theme script → `client/subscriptions`, native fallback · **c** Klaviyo-hosted form | **b** (§3) |
| D2 | Footer lists | **a** reuse Dutch Speakers `UPaLXW` + English Speakers `YiN3Ba`, create French Speakers (DOI) · **b** three new footer lists | **a** (§4) |
| D3 | Checkout list | **a** keep Shopify `TNLGVv` as the sync target (rename optional) · **b** point the sync at a language list | **a** |
| D4 | Notice text | **a** the proposal in §9 · **b** the short variant · **c** your own wording | **a** |
| D5 | When Klaviyo is unreachable (429/5xx/network/timeout) | **a** submit the native Shopify form · **b** show an error only | **a** (no signup lost) |
| D6 | Where key and list IDs live after your dev-theme test | **a** you set them in the live theme editor · **b** committed in `sections/footer-group.json` | **b** (survives theme pushes) |

Not decisions, just to do in the UI: checklist §8 items 1–9. Items 5, 7 and 8 are worth doing before launch regardless of this build.

## 11. Phase 2 outline (after "ja" and after global R15 has landed)

1. `git merge karmicare/soft-launch-global`.
2. `sections/footer.liquid`: four settings (§7), `data-klaviyo-key`, `data-klaviyo-list`, `data-locale`, `data-source`, note id + `aria-describedby`, status/alert elements in the DOM, script tag `defer`.
3. `assets/kc-footer-newsletter.js` (§6), `node --check`.
4. `docs/global-footer/KEYS.md` with the three keys (§9).
5. `shopify theme check --fail-level error` → 0 errors; commit by pathspec; commit body with the "no request before submit" proof and the Theme Check line.
6. Preview on the dev theme: `/nl`, `/fr`, `/en` footer with settings filled in the dev theme's editor; JS off → native; invalid address → error state; Victor does the one live test with his own address and checks the DOI mail language.
7. `worker_done` with the SHA → global coordinator → "Ready to land: global-footer" → landing desk (Astra review).
