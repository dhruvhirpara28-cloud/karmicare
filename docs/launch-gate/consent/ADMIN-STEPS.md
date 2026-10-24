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

**Status 24 Oct, ~15:40 UTC: done.** Victor switched the embed off again; verified with one anonymous fetch of the live homepage (theme t/35): no `hotjar-install` block, no `hjid:1364127` snippet, no `static.hotjar.com` reference. Until the R61 release is live nobody gets Hotjar; after it ships the theme's consent-gated loader (`snippets/kc-hotjar-consent.liquid`, §2.3) takes over. **Keep the embed off.** The loader skips itself while the embed is on (it sees `window.hj`), so there is never a double load, but an embed that is on tracks EU visitors before consent. The off state lives in `config/settings_data.json` (block `8669066016853369741`, `disabled: true`) on `main`; the landing desk carries it into merchant-edit so no later release restores the embed.

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

What the loader does, exactly (R61b): waits for Shopify's Customer Privacy API (`window.Shopify.customerPrivacy`, provided by Shopify's own scripts; only if it is still missing 8 s after load does the loader request it with `Shopify.loadFeatures([{ name: 'consent-tracking-api', version: '0.1' }])`, the version Shopify's scripts use on this store). It injects the standard Hotjar snippet only when **both** hold: `analyticsProcessingAllowed()` is `true`, and `saleOfDataAllowed()` is not `false` (a missing method counts as allowed). It runs the same check on page start and on every `visitorConsentCollected` event, so Hotjar starts the moment the visitor accepts. It never loads twice (nothing happens if `window.hj` already exists), and it does not run in the theme editor.

Who gets Hotjar, and which admin setting decides it:

| Visitor | Behaviour | Why |
|---|---|---|
| In a region where the cookie banner is active (EU/EEA and UK with Shopify's automated regions; Switzerland once it is in the list) | Nothing until **Accept**, or Manage preferences with **Analytics** ticked. Decline: nothing. | Shopify: in regions configured to require consent, "non-essential purposes are not allowed by default until consent is given" (shopify.dev, Customer Privacy API). |
| Everywhere else, for example the US | Hotjar loads by default on the first page, **unless** the visitor has opted out of data sale/sharing through the "Your privacy choices" link or a Global Privacy Control (GPC) browser signal; then `saleOfDataAllowed()` is `false` and the loader stays closed. | Shopify: "For other regions, the default behavior is to allow all processing purposes"; GPC "is honored automatically" in the configured opt-out regions and sets `sale_of_data` to `false` (same page). |
| Withdrawal (footer link → Decline, or the privacy-choices opt-out) | **Takes effect at once (R61d).** When the loader started Hotjar on the page the visitor is on, it expires Hotjar's cookies for site 1364127 (`_hjSession_1364127`, `_hjSessionUser_1364127`; on the host, the dotted host and the registrable domain) and reloads the page once; the reloaded page sees the refusal and loads nothing. A sessionStorage stamp refuses a second reload within 5 s, so no loop. Withdrawing when Hotjar never loaded does nothing extra. Hotjar's generic storage keys (`hjActiveViewportIds`, `hjViewportId`) are left; they hold no identifier. | Hotjar publishes no call that stops a running recorder (checked 24 Oct 2026), so a controlled reload is the reliable way; GDPR art. 7(3) needs withdrawal to take effect now (Astra R57d B2). Hotjar started by the app embed is not ours to stop: keep the embed off. |

Two settings decide it, both under **Settings → Customer privacy**:

- **Cookie banner → Regions and content → Regions.** Shopify's automated option "automatically configure[s] your cookie banner for visitors in the UK and EEA regions" when those markets are active. **Verify that Switzerland is in the list** (Astra N4: Shopify's page does not promise CH automatically); add it manually if the store sells to CH. Adding regions, up to "all regions", makes the loader wait for consent there too: Victor's region list is also the list of places where Hotjar waits.
- **Data Sharing Opt-Out Page** (same screen). Turning it on for the configured opt-out regions (usually US states) adds the "Your privacy choices" link and makes Shopify honour GPC there. Without it, visitors outside banner regions have no opt-out for Hotjar other than their browser's blocking tools, and the privacy-page wording in `PRIVACY-HANDOFF.md` must not promise one.

**Before deployment, verify (R61c, after Astra R61b B1).** The loader never reads the browser's GPC signal itself; it reads only the permission Shopify derives from it, and Shopify derives it only where the Data Sharing Opt-Out Page is active. So the privacy page may promise "Your privacy choices" and GPC handling only after these checks pass, in this order:

1. Settings → Customer privacy → **Cookie banner → Regions**: the list contains every EU/EEA country, the UK and Switzerland (today: "Austria, Belgium and 21 other regions" = 23, which is fewer than EU-27 + EEA + UK + CH; open the list, add what is missing or switch to manual). Expected on the storefront, in a private window from Belgium: the banner shows and `Shopify.customerPrivacy.analyticsProcessingAllowed()` is false before any choice.
2. **Status 24 Oct (Victor's admin): inactive**, Shopify says it "will be active when you add markets that require it". The US market is off and this page is a US-state mechanism, so nothing to do now; the privacy text is published without the "Your privacy choices" and GPC clauses (`PRIVACY-HANDOFF.md`). On the day a US market opens: Settings → Customer privacy → **Data sharing opt out page**: automated settings **on**, regions = the intended opt-out regions (Shopify's 15 US states), navigation menu = **Company** (our footer renders only that menu and the legal row, not Shopify's "Footer menu"), saved. Expected: the page exists and the "Your privacy choices" link is visible in the live footer; note the NL and FR labels Shopify renders for it and give them to gate-legal for `PRIVACY-HANDOFF.md`.
3. Only on that same day (conditional on a market that requires the opt-out page; nothing to test today): GPC reflected by Shopify. In a browser with Global Privacy Control on (Firefox or Brave setting), appearing from one of the opt-out regions (VPN or a test by someone there), `Shopify.customerPrivacy.currentVisitorConsent().sale_of_data` reads "no" and Hotjar makes no request. Without a visitor in such a region this cannot be tested from Belgium; then the GPC clause stays out of the privacy text until it is.
4. Hotjar → site 1364127 → Privacy / Data suppression: keystroke masking and IP anonymisation on (item (2) below). If not, "with keystroke masking" leaves the privacy text.

If 2 or 3 fails or cannot be done, gate-legal publishes the texts **without** the "Your privacy choices" and GPC clauses (the handoff says where to cut).

Admin prerequisites for the loader to be lawful: (1) the Hotjar **app embed off** (§1.1, done 24 Oct ~15:40 UTC, verified); (2) **still open for Victor:** check Hotjar's own privacy settings for site 1364127: Hotjar → Settings → Sites & Organizations → site 1364127 → **Privacy** / **Data suppression**: keystroke masking on (promised in the privacy page), IP anonymisation on, suppress text where possible. The loader contains no masking configuration, so only Hotjar's settings establish it. Those settings reduce what Hotjar stores; they do not replace the consent gate.

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
