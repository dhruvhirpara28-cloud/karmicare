# Footer newsletter → Klaviyo: research

**Created**: 2026-10-21

### Changelog
| Date | Change |
|------|--------|
| 2026-10-21 | Research by the landing desk (web sources only, no account access). Starting point for the global-footer child; items marked *unverified* must be checked before they are relied on. |

## Recommendation

Footer form → Klaviyo's browser endpoint `POST /client/subscriptions`, called from theme JS with the **public** key only and no klaviyo.js. Double opt-in lists, one per language (NL, FR, EN). Keep Klaviyo's Shopify subscriber sync, but pointed at a separate list for checkout opt-ins.

Why: it is the only route that sets list, consent, source and language exactly, with nothing running before cookie consent.

## 1. Klaviyo remote MCP

- URL `https://mcp.klaviyo.com/mcp`, Streamable HTTP, OAuth with automatic client registration (no API key). Needs Owner, Admin or Manager on the Klaviyo account. [Klaviyo](https://developers.klaviyo.com/en/docs/connect_to_the_klaviyo_mcp_server)
- URL options: `read-only=true` turns off every writing tool; `toolsets=lists:read,profiles:read` limits the tool set; `disable-tools-with-user-generated-content=true`; `core-tools-only=true`. Same page.
- OAuth scopes of the remote server are not documented (*unverified*).
- This child's connection is read-only: `claude mcp add --transport http --scope local klaviyo "https://mcp.klaviyo.com/mcp?read-only=true"`, then `/mcp` to log in. Klaviyo does not document Claude Code; command form from [Claude Code docs](https://code.claude.com/docs/en/mcp).
- Read tools: `get_lists`, `get_list`, `get_segments`, `get_profiles`, `get_profile`, `get_forms`, `get_form`, `get_flows`, `get_flow`, `query_form_values`. [Tool list](https://developers.klaviyo.com/en/docs/klaviyo_mcp_server_available_tools)
- Write tools (disabled by read-only): subscribe/unsubscribe, list add/remove/create/update/delete, profile create/update/import/suppress/merge, form and flow create/update/delete, `send_campaign`, `request_profile_deletion`. Never use a subscribe tool to create consent for a real person.

## 2. Routes

### a. Shopify native form + Klaviyo "Sync your Shopify email subscribers"
- Real-time sync of footer signups; target must be a list, not a segment; turning it on imports past subscribers; on conflict the newer consent timestamp wins. [Klaviyo](https://help.klaviyo.com/hc/en-us/articles/115005080667)
- Reads Shopify's consent status, not the deprecated "Accepts Marketing" field, so the `newsletter` tag decides nothing. Unsubscribing in Shopify does not unsubscribe in Klaviyo. A consent change made by hand in Shopify admin does not subscribe in Klaviyo. [community](https://community.klaviyo.com/questions/13845)
- Optional Klaviyo→Shopify sync can push status and locale back; its "all profiles" option creates a Shopify customer per Klaviyo profile. [Klaviyo](https://help.klaviyo.com/hc/en-us/articles/115005080407)
- Shopify "Customer marketing confirmation" = Shopify-side double opt-in for online-store signups; records `CONFIRMED_OPT_IN` vs `SINGLE_OPT_IN`. [Shopify help](https://help.shopify.com/en/manual/promoting-marketing/create-marketing/customer-contact-information), [enum](https://shopify.dev/docs/api/admin-graphql/latest/enums/CustomerMarketingOptInLevel). Whether pending people sync, and the language of Shopify's confirmation mail: *unverified*.
- Locale: synced from Shopify, but form-created profiles "may not always include" it. [Klaviyo](https://help.klaviyo.com/hc/en-us/articles/45224022467739). Workaround via a language tag read as "Shopify Tags" [Klaviyo](https://help.klaviyo.com/hc/en-us/articles/115005080907); multiple tags on the form *unverified*.
- Pros: no JS, no cookies. Cons: language not guaranteed, no source naming, risk of two confirmation mails.

### b. `POST https://a.klaviyo.com/client/subscriptions?company_id=PUBLIC_KEY`
- Header `revision: 2026-10-15` (GA per [changelog](https://developers.klaviyo.com/en/docs/changelog_)); body type `subscription`, list in `relationships.list`, `attributes.custom_source`, profile `email`, `locale` (e.g. `nl-BE`), custom `properties`. 202 on success; 350/s burst, 750/min steady. [Reference](https://developers.klaviyo.com/en/reference/create_client_subscription)
- Public key is safe in the theme; a private key never goes in browser code. [Klaviyo](https://developers.klaviyo.com/en/v2026-07-15/docs/authenticate)
- The list's single/double opt-in setting applies; pending profiles are not consented yet. [Guide](https://developers.klaviyo.com/en/docs/collect_email_and_sms_consent_via_api)
- CORS: built for browsers, not documented explicitly (*unverified*, test it).
- Pros: exact list, source, language; no cookie (plain request on submit). Cons: own JS to maintain; no Shopify customer unless Klaviyo→Shopify sync is on.

### c. Klaviyo forms via klaviyo.js / app embed — not recommended
- Sets `__kla_id` unless consent blocks it. [Klaviyo](https://help.klaviyo.com/hc/en-us/articles/360034666712). Klaviyo says it follows Shopify's Customer Privacy API for EU onsite events [Klaviyo](https://help.klaviyo.com/hc/en-us/articles/4425956184731); a 2024 report saw the cookie before consent [community](https://community.klaviyo.com/marketing-30/privacy-issue-in-shopify-klaviyo-integration-6664) (*unverified today*). Gating it behind `marketingAllowed()` would hide the footer form for non-consenting visitors.

## 3. Data and consent (Belgium/EU)
- Belgian DPA direct-marketing Recommendation 01/2025 (cover 01/2026) replaces 01/2020 (§07); pre-ticked boxes and silence are not consent (§84); controller keeps proof of consent (§87). [GBA/APD](https://autoriteprotectiondonnees.be/publications/recommandation-01-2025-relative-aux-traitements-de-donnees-a-caractere-personnel-dans-le-cadre-du-marketing-direct.pdf). Publication date *unverified*.
- Double opt-in: yes. Not legally required as far as found, but the APD names a confirmation mail as evidence the address belongs to the person (§164).
- Klaviyo stores `consent`, `consent_timestamp`, `method`, `method_detail`, `custom_method_detail` (= `custom_source`), `double_optin`, suppressions; no IP mentioned. Add own properties such as `consent_text_version`, `signup_path`.
- Notice next to the field: who collects, what will be sent, unsubscribe any time, a clearly visible privacy-policy link. [GDPR Art. 7(3), 13](https://eur-lex.europa.eu/eli/reg/2016/679/oj), [CMS on APD](https://cms.law/en/bel/legal-updates/belgian-dpa-publishes-new-detailed-guidelines-on-direct-marketing)
- Minimise: email + language only.
- Language: Klaviyo's built-in `locale` (not `$locale`, not custom); Smart Translations reads it and supports nl-BE. [Klaviyo](https://help.klaviyo.com/hc/en-us/articles/38068161225243). Derive `nl-BE` / `fr-BE` / `en` from `request.locale`. [Shopify](https://shopify.dev/docs/api/liquid/objects/request)
- Source: `custom_source` = legacy `$source`; e.g. `Footer newsletter · nl`.
- Duplicates: profiles match by email; don't send `external_id` from the theme (anecdotal duplicate report, [DEV](https://dev.to/khalit_hartmann_17e573503/klaviyo-profiles-newsletter-where-the-docs-wont-save-you-783)). Welcome-flow filters per [Klaviyo](https://help.klaviyo.com/hc/en-us/articles/115005080667).
- Checkout opt-ins subscribe at "Checkout Started"; a Klaviyo-unsubscribed person is resubscribed if they opt in at checkout. Same page.
- 202 for already subscribed / unsubscribed / suppressed → one neutral "check your inbox" message for every case. Suppressed + API resubscribe: *unverified*.
- Accessibility: visible label; notice linked with `aria-describedby`; errors as text + `aria-invalid` ([WCAG 3.3.1](https://www.w3.org/WAI/WCAG22/Understanding/error-identification.html)); success via `role="status"` ([WCAG 4.1.3](https://www.w3.org/WAI/WCAG22/Understanding/status-messages.html)); EAA applies ([EAA](https://eur-lex.europa.eu/eli/dir/2019/882/oj)).

## 4. Pitfalls
- DOI on in both Shopify and Klaviyo → two confirmation mails. [community](https://community.klaviyo.com/marketing-30/double-opt-in-sending-twice-12265)
- Klaviyo's confirmation-mail language is per list, parts fixed, no je/u or tu/vous choice ([community](https://community.klaviyo.com/marketing-30/editing-translating-confirmation-email-1124)) → one list per language (*unverified in current docs*).
- DOI links expire after 72 h. [Klaviyo](https://help.klaviyo.com/hc/en-us/articles/115005251108)
- Existing Shopify customers must place an order before being subscribed via sync. [Klaviyo](https://help.klaviyo.com/hc/en-us/articles/115005080667)
- An old integration left connected can mail DOI requests to a whole existing list (check the Webflow-era one). Shopify Tags edited in Klaviyo are overwritten on next sync. [Klaviyo](https://help.klaviyo.com/hc/en-us/articles/115005080407)
- The Webflow-era list probably has no proof of consent (APD §87): never import it as subscribed.
- Sync targets a list; campaigns go to a segment of everyone who can receive email.
