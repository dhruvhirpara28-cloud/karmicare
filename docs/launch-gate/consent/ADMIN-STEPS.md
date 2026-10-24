# Consent: admin and app steps for Victor (R60, 24 Oct 2026)

Lane gate-consent, launch blocker 4 of LR1 (`docs/launch-gate/input/LR1-LAUNCH-READINESS.md`, blocker 4 and the "Cookies / Hotjar before consent" row). The measurement behind these steps is in `REPORT.md` next to this file.

Nothing below was done by the lane. Every step is a Shopify admin or app setting that only Victor can change. Settings saved in the live theme editor land on `main`; the landing desk brings them into merchant-edit before the next push.

## 0. What is wrong, in one paragraph

Shopify's own consent banner works, the footer link reopens it, and every pixel registered under Settings → Customer events waits for consent (GA4, Google Ads, Meta, TikTok, Judge.me, Klaviyo's pixel, the Triple Whale custom pixel). Three things bypass it because they do not run through Customer events: the **Hotjar app embed** (an inline snippet that loads Hotjar and sets two cookies on every page view), **Klaviyo's onsite script** (a legacy ScriptTag of the Klaviyo app, with analytics modules and local storage) and **UpPromote's affiliate script** (a legacy ScriptTag, with a 365-day cookie). All three load before any choice, after Reject and after consent is withdrawn. The privacy page promises the opposite ("No non-essential cookies or tracking scripts run before you opt in").

## 1. Fastest lawful route (do these first, in this order)

### 1.1 Hotjar app embed off

| | |
|---|---|
| Path | Online Store → Themes → (live theme) **Customize** → left sidebar, bottom icon **App embeds** |
| Field | **Hotjar** (block `hotjar-install/blocks/global`) |
| Old value | On |
| New value | **Off** → **Save** |

Effect: the inline Hotjar snippet disappears from `content_for_header`; no more `static.hotjar.com`, `script.hotjar.com`, `content.hotjar.io` requests and no `_hjSession_1364127` / `_hjSessionUser_1364127` cookies. Existing Hotjar cookies in visitors' browsers expire by themselves (session 30 min, user 365 days); Shopify cannot delete them.

**R61 (24 Oct, later):** Victor switched the embed back on in the live editor. The theme now carries its own consent-gated Hotjar loader (`snippets/kc-hotjar-consent.liquid`, see §2.3), so Hotjar keeps working for everyone who may be tracked. **The embed must go off again once the R61 release is live**; the loader skips itself while the embed is on (it sees `window.hj`), so there is no double load, but the embed itself still tracks EU visitors before consent until it is off. Switch it off right away if there should be no EU exposure in the meantime; EU recordings simply stop until the release ships.

Note for the landing desk: this toggles `config/settings_data.json` → `current.blocks.8669066016853369741.disabled` from `false` to `true` on `main`. Bring it into merchant-edit before the next theme push, or the push switches Hotjar back on.

### 1.2 Klaviyo onsite tracking off (removes the ScriptTag)

| | |
|---|---|
| Path | Klaviyo (klaviyo.com) → **Integrations** → **Shopify** → **Settings** (or **Manage settings**) → section **Onsite tracking** |
| Field | "Enable onsite tracking" / "Add Klaviyo onsite tracking (klaviyo.js) to your store" |
| Old value | On (klaviyo.js loads on every page via a Shopify ScriptTag, company `XfYq2r`) |
| New value | **Off** → Save |

What keeps working: the Klaviyo **web pixel** registered in Shopify Customer events (`Klaviyo`, purposes analytics + marketing) still records Viewed Product, Added to Cart and Started Checkout, and Shopify gates it behind consent; e-mail flows, lists and the footer newsletter (our own form) are untouched. What stops: Klaviyo signup **forms**, back-in-stock buttons and onsite personalisation. We use none of them today (the footer newsletter is our own form, see REPORT.md §5).

If the Klaviyo settings page instead offers "Honour Shopify's customer privacy consent" (Klaviyo has been rolling this out), switch that **on** as an alternative and re-measure (section 3); if klaviyo.js still loads before a choice, use the Off setting above.

### 1.3 UpPromote: uninstall, or at least stop its storefront script

| | |
|---|---|
| Path | Settings → **Apps and sales channels** → **UpPromote** (listed as "UpPromote: Affiliate Marketing" or "UpPromote Affiliate Marketing") |
| If no affiliate programme is running | **Uninstall** (⋯ → Uninstall). This removes the ScriptTag and the UpPromote web pixel together. Recommended. |
| If the programme is needed | Open the app → **Settings** → **Tracking** (names vary: "Tracking settings", "Cookie / tracking", "Install tracking script") → set the storefront tracking script **off** or to "Shopify web pixel only", and raise a ticket with UpPromote asking for a Shopify Customer Privacy consent check. Until they confirm it, the cookie `_up_clid` is set before consent. |

### 1.4 Identify and, if not needed, disconnect the ungated app pixel

| | |
|---|---|
| Path | Settings → **Customer events** → tab **App pixels** |
| What to look for | The pixel whose app declares **no privacy purposes** (in the storefront config: id `1566343549`, app client `2773553`, configuration `shopId 199395, env production`). In admin it shows under its app name; the likeliest candidates are UpPromote (the affiliate order attribution pixel) or a loyalty app. |
| Action | If the app is one we do not use for launch: **⋯ → Disconnect**. If it is needed, leave it (it runs in Shopify's sandbox worker and cannot set cookies), but record the app name in the privacy page processor list (handoff to gate-legal). |

Also note there: the second unidentified pixel (id `1979744637`, app client `2753413`, configuration `shopId karmicares.myshopify.com`, purposes analytics + marketing) is consent-gated and only loaded after Accept in our test. Record its app name as well; it is most likely Loop Subscriptions.

### 1.5 Stale ScriptTag `loy_64261423286.js` (housekeeping, not a consent issue)

`content_for_header` also loads `https://cdn.shopify.com/s/files/1/0642/6142/3286/t/1/assets/loy_64261423286.js`, which returns 404. That is a loyalty app's ScriptTag whose file no longer exists. Settings → Apps and sales channels: if a loyalty app is still installed and unused, uninstall it; if none is installed, ask Shopify Support to delete the orphaned ScriptTag (merchants cannot delete ScriptTags themselves).

### 1.6 Re-measure (5 minutes, no tools needed)

1. Open a **private/incognito window** (no Shopify admin login), open DevTools → Network, filter "hotjar", then "klaviyo", then "uppromote" / "cloudfront".
2. Load `https://karmicares.myshopify.com/` and `https://karmicares.myshopify.com/nl`. **Expected: no request to any of the three before you click anything.**
3. Click **Decline** (NL: **Afwijzen**). Reload. Expected: still none. In DevTools → Application → Cookies, only `_shopify_essential`, `localization`, `cart_currency` (and `_shopify_essential` is HttpOnly).
4. Click the footer link **Cookie preferences** (NL: **Cookievoorkeuren**) → **Accept**. Expected: gtag/GA4, Google Ads, Meta, TikTok requests appear now, not earlier.
5. Footer link again → **Decline**. Reload. Expected: Google, Meta and TikTok requests stop. Their cookies stay in the browser until they expire; that is normal, Shopify deletes only its own (`_shopify_analytics`, `_shopify_marketing`, `shopify_client_id` disappear).

## 2. The proper fix per tool (after 1.1 to 1.4)

### 2.1 Shopify Customer privacy (verify, probably already right)

| | |
|---|---|
| Path | Settings → **Customer privacy** → **Cookie banner** |
| Check 1 | Banner is **on** and the region list covers **European Union / EEA**, **United Kingdom** and **Switzerland** (the market selector offers UK and CH; LR1 blocker 5). Our test saw the banner in Belgium (region `BEVLG`). |
| Check 2 | If the card offers a data-collection mode, it must be the one that **waits for consent** in those regions (wording in admin: "Collect data only after consent" / not "Collect before consent"). The observed behaviour (`analyticsProcessingAllowed() === false` before a choice, no GA/Meta/TikTok request) says this is already the case. |
| Check 3 | Privacy policy link in the banner points to `/pages/privacy-policy` (observed: yes). |
| Leave alone | Settings → Customer privacy → **Data sales** (US only) and the banner **appearance**; the theme file `assets/kc-cookie-preferences.js` restyles Shopify's banner into the panel you see; it does not change what Shopify stores. |

### 2.2 Customer events (verify)

| | |
|---|---|
| Path | Settings → **Customer events** |
| App pixels | Expect: Judge.me, Klaviyo, Google & YouTube, Facebook & Instagram (Meta), TikTok, Loop Subscriptions (probably), and one more (1.4). Each shows the permission it declares; Shopify applies it. Disconnect what is not needed for launch; fewer processors is less to explain in the privacy page. |
| Custom pixel | Open the Triple Whale (TriplePixel) custom pixel → **Settings** → **Permission** must be **Required** with **Analytics** and **Marketing** ticked (observed in the storefront config: yes), **Data sale** as appropriate (EU: "Does not qualify as data sale"). Do not paste Hotjar or Klaviyo into a custom pixel: custom pixels run in a sandbox and Hotjar cannot record from there. |

### 2.3 Hotjar: the theme loader (R61, built) and what it needs from admin

Hotjar's Shopify app has no consent setting; its snippet is unconditional (observed, `REPORT.md` §2). Since R61 the theme loads Hotjar itself, consent-gated: `snippets/kc-hotjar-consent.liquid`, rendered once from `layout/theme.liquid` with site id 1364127.

What the loader does: waits for Shopify's Customer Privacy API (`window.Shopify.customerPrivacy`, loading it with `Shopify.loadFeatures([{ name: 'consent-tracking-api', version: '0.2' }])` if the banner script has not), injects the standard Hotjar snippet only when `analyticsProcessingAllowed()` is true, listens for Shopify's `visitorConsentCollected` event so Hotjar starts the moment analytics consent is given, loads nothing on the next page view after withdrawal, never loads twice (it does nothing if `window.hj` already exists), and does not run in the theme editor.

Who gets Hotjar, and which admin setting decides it:

| Visitor | Behaviour | Why |
|---|---|---|
| EU/EEA, UK, Switzerland (regions where the banner is active) | Nothing until Accept, or Manage preferences with **Analytics** ticked. Decline or withdrawal: no Hotjar on the next page view. | Shopify: "non-essential purposes are not allowed by default until consent is given" in regions configured to require consent (shopify.dev, Customer Privacy API). |
| Everyone else, for example the US | Hotjar loads at once, unless the visitor opted out through "Your privacy choices" or a Global Privacy Control browser signal. | Shopify: "For other regions, the default behavior is to allow all processing purposes" (same page). |

The region list is **Settings → Customer privacy → Cookie banner → Regions**. Shopify's automated option "automatically configure[s] your cookie banner for visitors in the UK and EEA regions" when those markets are active; Switzerland is grouped with Europe by Shopify and should be in the list as long as the market selector offers CH. Adding regions manually (even "all regions") makes the loader wait for consent there too, so Victor's choice of regions is also the choice of where Hotjar waits. For US-state opt-outs, Shopify's **Data Sharing Opt-Out Page** setting on the same screen adds the "Your privacy choices" link and honours GPC; the loader follows whatever `analyticsProcessingAllowed()` then says.

Admin prerequisites for the loader to be lawful: (1) the Hotjar **app embed off** (§1.1), otherwise the embed still tracks EU visitors before consent; (2) keep Hotjar's own privacy settings as advised: Hotjar → Settings → Sites & Organizations → site 1364127 → **Privacy** / **Data suppression**: keystroke masking on (promised in the privacy page), IP anonymisation on, suppress text where possible. Those settings reduce what Hotjar stores; they do not replace the consent gate.

Known limit: when a visitor withdraws consent on a page where Hotjar is already running, the current page keeps recording until the next navigation; Hotjar publishes no stop call we could verify, so the loader does not call one. From the next page view on, nothing loads.

### 2.4 Klaviyo, proper state

Keep 1.2 (onsite script off) unless a Klaviyo form is ever added to the theme. If it is, Klaviyo's consent option ("Honour Shopify customer privacy", in the same Shopify integration settings) must be on and re-measured; and the privacy page must name Klaviyo as processor for analytics, not only e-mail.

### 2.5 Google, Meta, TikTok

Already consent-gated through Customer events; nothing to change for launch. Google's gtag sends `gcs=G111` (all granted) after Accept and nothing before, so consent mode is in "basic" behaviour, which is the stricter one. Before enabling ads campaigns, the LR1 channel gate still applies.

### 2.6 Privacy page copy (handoff to gate-legal, not this lane)

- Section 9.2 says "the “Cookie settings” link in our footer"; the footer link reads **Cookie preferences** / **Cookievoorkeuren** / FR per Shopify. Align the wording.
- The processor list under "Analytics and optimisation" names GA4, Meta Pixel, Hotjar and TriplePixel. Missing today: **TikTok** (pixel `CBEGLDJC77U5BM7P39EG`), **Klaviyo** (as web pixel), **Judge.me** (web pixel, reviews), **Loop Subscriptions** (plan data, referral banner) and **UpPromote** if kept. Remove Hotjar from the list if 1.1 is kept permanently.
- "Google Analytics 4 … with your consent" is correct as measured. Keep.

## 3. What Victor cannot change and we should know

- **Adobe Fonts** (`use.typekit.net`, `p.typekit.net`) is loaded by our theme (`layout/theme.liquid`, Adobe kit `kss0igj`). No cookie, but a third-party request with the visitor's IP and a licence beacon on every page view, before any choice. Adobe's web licence requires loading through Adobe's servers, so self-hosting is a licence question, not a code change. Decision for Victor and design; see REPORT.md §6.
- **Shopify platform** requests (`monorail-edge.shopifysvc.com`, `otlp-http-production.shopifysvc.com`, `shop.app` Shop Pay session, Sign in with Shop recognition) run in every state. Shopify treats them as essential; they are covered by Shopify's processor role. Shop Pay / Sign in with Shop can be reduced under Settings → Checkout → **Shop Pay** and **Customer accounts → Sign in with Shop** if Victor wants fewer calls, but that is a commerce decision, not a consent defect.
- **Google Fonts (Inter)** was requested by Klaviyo's forms runtime, not by the theme; it disappears with 1.2.
