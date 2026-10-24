# Consent audit of the live store (R60, 24 Oct 2026)

Lane gate-consent, launch blocker 4 of LR1 (`docs/launch-gate/input/LR1-LAUNCH-READINESS.md`). Admin and app steps for Victor: `ADMIN-STEPS.md` next to this file.

## 1. Verdict

- **Shopify's consent machinery works.** The banner shows in Belgium in EN and NL, Reject sits next to Accept on the first layer, granular choices exist, the footer link reopens the panel, and `window.Shopify.customerPrivacy` carries the choice. Every pixel registered under Settings → Customer events (Google GA4 and Ads, Meta, TikTok, Judge.me, Klaviyo's pixel, the Triple Whale custom pixel) is silent before consent, fires after Accept and is silent again after withdrawal.
- **Three scripts bypass it**, because they are injected by apps outside Customer events: the **Hotjar app embed** (script plus two cookies), **Klaviyo's onsite script** (legacy ScriptTag, analytics modules, local storage) and **UpPromote's affiliate script** (legacy ScriptTag). They load before any choice, after Reject and after withdrawal. This is the blocker LR1 saw, and it is wider than Hotjar.
- **Our theme code loads no tracker.** `git grep` over `layout/`, `sections/`, `snippets/`, `assets/` finds no Hotjar, gtag, fbq, TikTok, Klaviyo or Triple Whale call, no `document.cookie` or storage write outside the Loop widget (off-limits) and no third-party script tag except Adobe Fonts (§6). The only Klaviyo code in the theme (`assets/kc-footer-newsletter.js`) sends one request on submit and is inactive on the live site (no key configured). **R60 needed no theme change.** R61 (same day, on Victor's decision) added a consent-gated Hotjar loader to the theme so the app embed can go off: §4.2.
- **Fastest lawful route**, as LR1 allowed: switch the Hotjar app embed off, switch Klaviyo onsite tracking off in Klaviyo, uninstall or silence UpPromote. Exact paths in `ADMIN-STEPS.md` §1. Victor's decisions (Hotjar yes/no, Klaviyo onsite yes/no, UpPromote keep/uninstall) were sent to the coordinator as one question with recommendation a/a/a; the report assumes a/a/a.

## 2. Matrix: tracker × state

States, each in a fresh isolated Orca profile, Belgian IP, English homepage unless noted: **Before** = page loaded, nothing clicked. **Reject** = Decline on the first layer, then one more page view. **Accept** = Accept on the first layer, then one more page view. **Withdrawn** = after Accept, footer "Cookie preferences" → Decline, then one more page view. "Req" = a request to the vendor; "Store" = a cookie or Web Storage entry written on `karmicares.myshopify.com`.

| Tracker (ids) | Source | Before: req / store | Reject: req / store | Accept: req / store | Withdrawn: req / store | Verdict |
|---|---|---|---|---|---|---|
| **Hotjar** (site 1364127) | App embed `hotjar-install/blocks/global` (`config/settings_data.json` block `8669066016853369741`, enabled) | **yes** `static.hotjar.com`, `script.hotjar.com` / **yes** cookies `_hjSession_1364127`, `_hjSessionUser_1364127` (365 d) | **yes** + `content.hotjar.io` / **yes**, cookies refreshed | yes / yes (+ `hjActiveViewportIds`, `hjViewportId`) | **yes** / **yes** | **Not compliant.** Snippet has no consent check. |
| **Klaviyo onsite** (company `XfYq2r`) | Legacy ScriptTag of the Klaviyo app, loaded by Shopify's `asyncLoad` in `content_for_header` | **yes** ~20 scripts from `static.klaviyo.com` incl. `static-tracking.klaviyo.com` `fender_analytics`, `telemetry`, `post_identification_sync`; `static-forms.klaviyo.com`; `fast.a.klaviyo.com`; pulls Google Fonts `Inter` / **yes** localStorage `klaviyoOnsite`, sessionStorage `klaviyoPagesVisitCountV2` | **yes** / **yes** | yes / yes + cookie `__kla_id` (400 d), `__kl_key`, `$referrer`, `$last_referrer`, `kl-post-identification-sync` | **yes** / `__kla_id` remains | **Not compliant** before consent (script, analytics modules, storage). |
| **Klaviyo web pixel** (`2032075133`) | Customer events app pixel, purposes analytics + marketing | no / no | no / no | yes (sandbox worker) / see row above | no / — | Compliant. |
| **UpPromote** affiliate script | Legacy ScriptTag, `d1639lhkj5l89m.cloudfront.net/js/storefront/uppromote.js` via `cdn.shopify.com/proxy/…` | **yes** / sets `scaaf_*` cookies only on affiliate clicks (none in test) | **yes** / — | yes / — | **yes** / — | **Not compliant**: third-party marketing script before consent, no consent check in the code. |
| `_up_clid` cookie (365 d), localStorage `__up_exposeActionContext`, `ba_msg_active` | Writer not identified (not in uppromote.js, Hotjar, Klaviyo, Loop, Judge.me or Shopify's pixel manager code) | **yes** written | yes | yes | yes | Open: identify via Settings → Customer events app names (ADMIN-STEPS §1.4). |
| **Google** GA4 `G-BLM8L43EY4`, Ads `AW-716557562`, tag `GT-WF3GVG9W`, Merchant Center `MC-PMXVYMEW9Z` | Google & YouTube channel pixel `535953590` (open runtime) | pixel loader only, **no Google request** / no | no / no | **yes** `googletagmanager.com`, `region1.analytics.google.com` (`gcs=G111`), `google.com/ccm`, `googleadservices.com`, `doubleclick.net`, `merchant-center-analytics.goog` / cookies `_ga`, `_ga_BLM8L43EY4`, `_ga_PMXVYMEW9Z`, `_gcl_au`, localStorage `_gcl_ls` | **no request**; cookies remain until expiry | Compliant (residual cookies are a browser fact, not a request). |
| **Meta pixel** `315581617586129` | Facebook & Instagram channel pixel `247529654` (open runtime); server-side CAPI flagged on in Shopify's config | no / no | no / no | yes `connect.facebook.net` fbevents + config, `fbq` defined / no `_fbp` seen | no / — | Compliant. |
| **TikTok pixel** `CBEGLDJC77U5BM7P39EG` | TikTok app pixel `438567094` (sandbox worker) | no / no | no / no | yes / cookies `_ttp`, `ttcsid`, `ttcsid_CBEGLDJC77U5BM7P39EG` (90 d), sessionStorage `tt_*` | no / cookies remain | Compliant. **Not named in the privacy page** (handoff). |
| **Triple Whale** (TriplePixel) | Custom pixel `shopify-custom-pixel` (lax sandbox), permission required: analytics + marketing | no / no | no / no | yes (sandbox document) / localStorage `TW_EXT_page^viewed_*` | no / — | Compliant. |
| **Judge.me** | App embed `judgeme_core` (settings + `loader.js` from `cdn.shopify.com`) and app pixel `2839052669` (analytics) | loader script from Shopify's CDN, **no judge.me host request**, no cookie / no | same | pixel worker yes / no | pixel no / — | Compliant; loader is functional. |
| **Loop Subscriptions** | Theme `assets/loop-widget.js` (off-limits) → `api.loopwork.co` selling plans; app embeds referral banner and capture → `cdn.loopwork.co/…/store.json`, `d217z8zw4dqir.cloudfront.net/….json`; probably app pixel `1979744637` (analytics + marketing) | yes (plan data, config) / localStorage `loop_cdn_timestamp_store`, sessionStorage `loop_ui_props_*`, `loop_store_json_*`; no cookie | yes / same | yes + pixel worker / same | yes, pixel no / same | Functional for the purchase flow; no cookie. Name Loop in the privacy page. |
| **Unidentified app pixel** `1566343549` (app client `2773553`, config `shopId 199395`, **no privacy purposes declared**) | Customer events app pixel, sandbox worker | **runs** | **runs** | runs | **runs** | Open: a pixel that declares no purposes is never gated. Identify and disconnect if not needed (ADMIN-STEPS §1.4). Cannot set cookies from the worker. |
| Shopify platform: trekkie/monorail, `otlp-http-production.shopifysvc.com`, Shop Pay `shop.app` session, Sign in with Shop | Shopify (`content_for_header`, shop-js) | yes / `_shopify_essential` (HttpOnly), `localization`, `cart_currency`, localStorage `signInWithShop:*` | yes / same | yes / + `_shopify_analytics`, `_shopify_marketing`, `shopify_client_id` | yes / the three consent cookies **deleted by Shopify** | Essential per Shopify; outside our control. |
| **Adobe Fonts** kit `kss0igj` | Theme `layout/theme.liquid` line 394 | yes `use.typekit.net` (CSS + 3 fonts), `p.typekit.net` licence beacon / no | yes / no | yes / no | yes / no | Third-party request before consent, no cookie. Decision for Victor (§6). |
| Google Fonts `Inter` | Pulled by Klaviyo's forms runtime, not by the theme | yes / no | yes / no | yes / no | yes / no | Disappears with Klaviyo onsite off. |
| Stale ScriptTag `loy_64261423286.js` | Legacy ScriptTag of a loyalty app; file returns 404 | request yes, 404 / no | same | same | same | Housekeeping (ADMIN-STEPS §1.5). |

Dutch homepage (`/nl`, separate fresh profile): same pre-consent set (Hotjar function present, Klaviyo object present, `_up_clid` cookie, the two Hotjar cookies) and the same gating after Afwijzen. Banner copy and the panel labels are Dutch ("Accepteren", "Afwijzen", "Voorkeuren beheren", "Vereist / Personalisatie / Marketing / Analyse", footer "Cookievoorkeuren").

## 3. Cookie banner checks

| Check | Result |
|---|---|
| Shown in Belgium and the EU | Yes. Shopify's banner (`privacy-banner.js`), region reported by `customerPrivacy.getRegion()` = `BEVLG`; `shouldShowBanner()` = true. The EU-wide region list itself lives in Settings → Customer privacy and must be confirmed by Victor (ADMIN-STEPS §2.1). |
| Reject as easy as Accept on the first layer | Yes. The theme's `assets/kc-cookie-preferences.js` turns Shopify's banner into a panel whose first layer shows **Accept**, **Decline** and **Manage preferences** as equal buttons; no pre-ticked optional category. |
| Granular choices | Yes. Manage preferences reveals Required (fixed on), Personalisation, Marketing, Analytics and **Save my choices**. |
| Footer link reopens the preferences | Yes. `Cookie preferences` / `Cookievoorkeuren` (`href="#shopifyReshowConsentBanner"`, rendered from `shop.policies` in `sections/footer.liquid`) reopens the panel with the saved state (all three ticked after Accept, none after Decline); Decline inside it closes the panel (wrapper `display:none`, dialog not visible). |
| Signal reaches `window.Shopify.customerPrivacy` | Yes. `currentVisitorConsent()` = `""` before a choice, `analytics/marketing/preferences = "no"` after Decline, `"yes"` after Accept, `"no"` after withdrawal; `analyticsProcessingAllowed()` / `marketingAllowed()` follow. Withdrawal fires two `api/unstable/graphql.json` calls and Shopify deletes `_shopify_analytics`, `_shopify_marketing`, `shopify_client_id`. |
| Privacy page promise | §9.2: "No non-essential cookies or tracking scripts run before you opt in. You can change or withdraw your choice at any time through the “Cookie settings” link in our footer." The first sentence is false today (Hotjar, Klaviyo onsite, UpPromote). The link is called "Cookie preferences", not "Cookie settings" (handoff). |

## 4. What was fixed in the theme

### 4.1 R60: nothing had to be

The theme contained no tracker to gate. Verified with:

```sh
git grep -nE 'hotjar|gtag\(|googletagmanager|fbq\(|ttq\.|_learnq|klaviyo\.com|triplewhale|TriplePixel' -- layout sections snippets assets ':!assets/loop-widget.js'
git grep -nE 'document\.cookie|localStorage|sessionStorage' -- layout sections snippets assets ':!assets/loop-widget.js'
```

The first returns one line, the footer newsletter's Klaviyo endpoint in `assets/kc-footer-newsletter.js` (used on submit only, inactive on the live theme); the second returns nothing. The one third-party request the theme makes on its own is Adobe Fonts (§6). Theme Check was not run for R60 because no theme file changed.

### 4.2 R61: Hotjar only with consent, as a theme loader

Victor (24 Oct, via the landing desk): "I want it to load for customers outside the EU region, following Shopify's recommendation. Otherwise, if they don't accept cookies, it is not loaded." Built as `snippets/kc-hotjar-consent.liquid`, rendered once from `layout/theme.liquid` right after `content_for_header` with `site_id: 1364127` (the only layout change). The Hotjar **app embed must be off** for this to be lawful; `ADMIN-STEPS.md` §1.1 and §2.3.

What the snippet does:

- Waits for `window.Shopify.customerPrivacy`. Shopify's banner and pixel scripts provide it asynchronously (on this store at API version 0.1); the snippet checks at `DOMContentLoaded`, at `load`, then every 500 ms for 8 s, and only then asks `Shopify.loadFeatures([{ name: 'consent-tracking-api', version: '0.1' }])` itself. Reason: asking for another version while Shopify's own copy is loading fails; measured on the live page: `Error: consent-tracking-api@0.2 has already been loaded at version 0.1`.
- Injects the standard Hotjar snippet for site 1364127 only when `analyticsProcessingAllowed()` is true.
- Listens for the document event `visitorConsentCollected` and runs the same check, so Hotjar starts the moment analytics consent is given (banner or footer link). The API, not `event.detail`, is the source of truth.
- Loads nothing on the next page view after withdrawal. Limit: the page on which consent is withdrawn keeps the already running script until navigation; Hotjar publishes no stop call we could verify, so none is called.
- Never loads twice: does nothing if `window.hj` is already a function (a forgotten app embed) or if it ran already on this page.
- Not rendered in the theme editor (`request.design_mode`), and the script also returns on `Shopify.designMode`. No other tracker, no personal data, no cookie read or write of its own.

Regions, per Shopify's documentation (quoted in `ADMIN-STEPS.md` §2.3): where the store's cookie banner is configured, "non-essential purposes are not allowed by default until consent is given"; "For other regions, the default behavior is to allow all processing purposes." With Shopify's automated banner regions (UK and EEA, Switzerland grouped with Europe) Hotjar therefore waits for consent in the EU/EEA, the UK and Switzerland and loads at once elsewhere, for example in the US, unless the visitor opted out ("Your privacy choices" / Global Privacy Control). The controlling setting is Settings → Customer privacy → Cookie banner → Regions.

Verification, file:// harness (the snippet's script with the site id filled in, `Shopify.customerPrivacy` stubbed per state, run in a fresh isolated Orca profile; Hotjar's loader is a real request to `static.hotjar.com`):

| State | Hotjar loader request | When |
|---|---|---|
| EU, no choice yet, Accept simulated at 1.5 s | yes, once | 0 ms after the consent event |
| EU, no choice | **no** | — |
| EU, declined earlier | **no** | — |
| EU, accepted earlier | yes, once | at page start |
| EU, accepted, withdrawn on this page at 1.5 s | once at start, nothing after | documented limit |
| EU, withdrawn earlier, next page view | **no** | — |
| Non-EU default (no banner region) | yes, once | at page start |
| Non-EU, opted out | **no** | — |
| API appears 2 s after load (Shopify's async scripts) | yes, once | 26 ms after the API appeared |
| API never provided; `loadFeatures` fallback | yes, once | `loadFeatures` called at 8.0 s, Hotjar at 8.3 s |
| Theme editor (`designMode`) | **no** | — |
| `window.hj` already present (app embed on) | **no second load** | — |

Verification, live homepage with the real Shopify banner (fresh isolated profile, the same gate logic injected with a recorder instead of the Hotjar snippet, because the live theme still carries the app embed): before any choice `analyticsProcessingAllowed()` = false (no load); Decline → event, false; footer link → Accept → event, true (would load immediately); reload → true at start; footer link → Decline → event, false; reload → false. On the live page `window.hj` already exists from the embed, so the real snippet would skip itself there until the embed is off.

Theme Check after the change: 0 errors, 19 warnings, the same baseline as before (the two in `layout/theme.liquid`, RemoteAsset for Adobe Fonts and UndefinedObject `scheme_classes`, predate R61).

## 5. The footer newsletter form today (not changed; global lane owns it)

- On the live theme the Klaviyo key and list are empty (`data-klaviyo-key=""`), so `assets/kc-footer-newsletter.js` exits immediately and the plain Shopify customer form posts to `/contact` with `contact[tags]=newsletter`; the address lands in Shopify Customers, tagged `newsletter`, not in Klaviyo. No request leaves the page before submit.
- The note under the field reads "By subscribing you agree to the Terms of Use & Privacy Policy" (locale key `kc.footer.consent_html`, NL "Door je in te schrijven, ga je akkoord met …"): consent bundled with terms, as LR1 flagged. The global lane is rewording it with Klaviyo.
- Shopify's hCaptcha bootstrap guards this form (`captcha-bootstrap` in `content_for_header`); the hCaptcha script loads only when a guarded form is focused. Not a consent issue.

## 6. Handoffs and decisions

**Victor (decisions, sent as one question to the coordinator):** Hotjar keep/drop; Klaviyo onsite tracking off; UpPromote uninstall/keep. Recommendation was: drop Hotjar for launch, Klaviyo onsite off, UpPromote uninstalled unless an affiliate programme runs. Victor chose to keep Hotjar with consent; R61 built the theme loader (§4.2). Still open for Victor: switch the Hotjar app embed off once R61 is live (§4.2, `ADMIN-STEPS.md` §1.1), Klaviyo onsite tracking, UpPromote.

**Victor / design (fonts):** Adobe Fonts is loaded from Adobe's servers on every page view before any choice (IP to Adobe, licence beacon, no cookie). Adobe's web licence requires Adobe's loader, so moving to self-hosted fonts means a font licence decision. Low risk compared with the three trackers; decide after launch.

**gate-legal (privacy page):** align "Cookie settings" with the real link text "Cookie preferences"; add TikTok, Klaviyo (web pixel), Judge.me, Loop and, if kept, UpPromote to the processor list; drop Hotjar if the embed stays off; note that GA cookies set after consent remain in the browser after withdrawal until they expire.

**Landing desk:** any app-embed toggle Victor makes in the live editor is saved on `main` in `config/settings_data.json`; bring it into merchant-edit before the next push or the push re-enables Hotjar.

**Global lane:** footer newsletter consent wording (§5), unchanged here.

## 7. Method and limits

- Live store `karmicares.myshopify.com`, 24 Oct 2026 ~12:50 to 13:35 UTC, three fresh isolated Orca browser profiles (`gate-consent-anon-1`, `-2-accept`, `-3-nl`), never logged in, no form submitted, no cart, no checkout. One static fetch each of `/`, `/nl` and `/pages/privacy-policy`, spaced; browser page loads spaced by minutes. No Shopify admin access; app names behind pixel ids are inferred from their configuration and must be confirmed in Settings → Customer events.
- Network capture is Orca's page-level capture: requests from Shopify's pixel sandbox workers (TikTok, Klaviyo pixel, Judge.me pixel, Triple Whale) are not visible there; their effect was read from cookies and storage instead. Requests from the top page (Hotjar, Klaviyo onsite, Google, Meta, UpPromote) are complete.
- Vendor scripts were downloaded read-only to confirm behaviour: Hotjar snippet (inline in the page), `uppromote.js`, Loop referral scripts, Judge.me loader, `klaviyo.js`, Hotjar modules, Shopify's pixel manager. None of them calls `Shopify.customerPrivacy` except Shopify's own pixel manager.
- Raw captures and the summariser stay in the lane's scratchpad and are not committed (they contain full request URLs with session tokens).
