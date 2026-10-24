# Admin steps: withdrawal function and legal-guarantee notice

**Created**: 2026-10-24 (lane gate-withdrawal, R58). Paste-ready for Victor. Nothing below was done by the lane: no admin writes, no installs. Do the steps in order; step 4 before step 4f, or the success page promises an email that does not go out.

Texts in NL and FR for every step: `TRANSLATIONS-HANDOFF.md`.

## 1. Create the page

Online Store → Pages → **Add page**

| Field | Value |
|---|---|
| Title | `Withdrawal` |
| Content | leave empty (the template carries everything) |
| Search engine listing → Edit → URL handle | `withdrawal` (so the page is `/pages/withdrawal`; the theme, the terms and the emails link to that handle) |
| Theme template (right column) | `page.withdrawal` |
| Visibility | Visible |

Save. Then Apps → **Translate & Adapt** → Pages → Withdrawal: Dutch title `Herroeping`, French title `Rétractation` (handle stays `withdrawal`).

Preview: Online Store → Themes → the dev theme → Customize → open `/pages/withdrawal`. The section "Withdrawal function" is already in the template; its texts are in the section settings.

## 2. Translate the theme texts

Apps → **Translate & Adapt** → Dutch → **Theme content** → filter on "Withdrawal function" (and on "Legal guarantee notice" for the product-page block). Paste the NL column from `TRANSLATIONS-HANDOFF.md` §1 and §2, then the same for French. Copy the cells, do not retype the French ones (they carry no-break spaces before `?` and `:`).

## 3. Put the function in the footer and the legal menu

Content → **Menus** (Online Store → Navigation on older admin) → the footer's legal menu (the one with Terms, Privacy, Consumer Rights):

| Field | Value |
|---|---|
| Add menu item → Name | `Withdraw from contract here` |
| Link | Pages → Withdrawal |

Save. Translate & Adapt → Navigation → that menu: NL `Hier de overeenkomst herroepen`, FR `Renoncer au contrat ici`. These are the statutory words; keep them exact.

Optional, same menu: `Your legal guarantee rights` → Pages → Consumer Rights (section 4), the site-wide reminder of the notice.

## 4. The acknowledgement of receipt (Klaviyo transactional flow)

The theme form sends one event to Klaviyo when the consumer presses Confirm withdrawal; this flow turns it into the email the law requires (content, date and time, without delay).

**4a. Plan check.** Klaviyo → Settings → Billing. Transactional status is available on paid plans only. If the account is on the free plan and stays there, skip to **4h** (Revoq) instead.

**4b. Sender.** Klaviyo → Settings → Email → sender: use `care@karmicare.com` as the from and reply-to for this flow (the account default is we@karmicare.com; care@ is the address the Terms give for withdrawals). The sending domain must be authenticated (Settings → Domains); it is, if Klaviyo campaigns already send.

**4c. Create the metric with one test event** (the flow builder needs the metric to exist). Run once from any terminal, with your own email:

```sh
curl -s -o /dev/null -w "%{http_code}\n" -X POST "https://a.klaviyo.com/client/events/?company_id=XfYq2r" \
  -H "Content-Type: application/json" -H "revision: 2026-10-15" \
  -d '{"data":{"type":"event","attributes":{"metric":{"data":{"type":"metric","attributes":{"name":"Withdrawal statement submitted"}}},"profile":{"data":{"type":"profile","attributes":{"email":"victor@karmicare.com","first_name":"Victor"}}},"properties":{"statement":"I hereby give notice that I withdraw from my contract of sale for the order below.","name":"Victor Test","order_number":"#0000","items":"","email":"victor@karmicare.com","submitted_at_local":"24 October 2026 at 15:00","submitted_at_utc":"2026-10-24T13:00:00.000Z","timezone":"Europe/Brussels","language":"en","page":"https://karmicares.myshopify.com/pages/withdrawal"},"time":"2026-10-24T13:00:00.000Z","unique_id":"test-0001"}}}'
```

Expect `202`. (`XfYq2r` is the account's public API key, the one every Klaviyo onsite snippet exposes; it is not a secret.) After a minute, Klaviyo → Analytics → Metrics shows "Withdrawal statement submitted".

**4d. Build the flow.** Klaviyo → Flows → Create flow → Build your own → name `Withdrawal acknowledgement (Art. VI.61/2 WER)`.

| Setting | Value |
|---|---|
| Trigger | Metric → `Withdrawal statement submitted` |
| Flow filters | none (every event must send) |
| Profile filters | none |
| First step | Email (no time delay in front of it) |
| Email → Smart Sending | **off** |
| Email → Skip recently emailed / quiet hours | off |
| Email → From / reply-to | KARMICARE `care@karmicare.com` |
| Email → Subject | `Acknowledgement of receipt: your withdrawal of {{ event.submitted_at_local }}` |
| Email → Body | plain text, the EN body from `TRANSLATIONS-HANDOFF.md` §3 |

One email serves the three languages: wrap the three bodies in the Klaviyo template as

```
{% if event.language == "nl" %} …NL body… {% elif event.language == "fr" %} …FR body… {% else %} …EN body… {% endif %}
```

and do the same in the subject line. Alternatively, a conditional split on `event.language` with three emails; either is fine, one email means one transactional review.

**4e. Mark it transactional.** In the email action: mark as transactional (Klaviyo asks you to request approval: Help → contact Customer Success with subject "Transactional Email Request", the flow link, the flow name and the subject line). Approval takes about one business day. Editing the email afterwards removes the status; re-request if you change it. Then set the flow **Live**.

**4f. Switch the theme on.** Online Store → Themes → Customize → `/pages/withdrawal` → section "Withdrawal function" → "Acknowledgement of receipt (Klaviyo)":

| Setting | Value |
|---|---|
| Klaviyo public API key (company ID) | `XfYq2r` |
| Klaviyo metric name | `Withdrawal statement submitted` (must equal the metric in 4c) |

Save. Until this key is filled, the page sends the statement to the store inbox only and tells the consumer the acknowledgement follows by email: care@ then sends it by hand, the same day, from the inbox copy.

**4g. Test on the live page** (only after 4e): fill in the form with your own email and a real order number, press Confirm withdrawal. Expect, within minutes: (1) a store-inbox email "New customer message" with Type: Withdrawal statement, name, order number, email, items, Submitted at; (2) the acknowledgement in your inbox with the same content and the date and time. Delete the test profile in Klaviyo afterwards if you like; keep the inbox email as the record of the test. Repeat once on `/nl/pages/withdrawal` to see the NL acknowledgement.

**4h. Alternative: the Revoq app instead of Klaviyo.** Apps → Shopify App Store → "Revoq EU Withdrawal Button" (free plan) → Install → in the app: texts per language (label "Withdraw from contract here" / NL / FR, confirm button "Confirm withdrawal" / "Herroeping bevestigen" / "Confirmer la rétractation"), sender care@karmicare.com, confirmation email on. Then Customize → `/pages/withdrawal` → section "Withdrawal function" → untick **Show the theme form** → Add block → the Revoq block. Check that its confirmation email states the date and time of submission (the law requires it); if it does not, switch to the Essential plan's custom template or keep the theme form with Klaviyo.

## 5. Order confirmation email: the link and the notice

Settings → **Notifications** → Customer notifications → **Order confirmation** → Edit code. Below the order summary add:

```html
<p style="margin:24px 0 8px;font-size:14px;line-height:1.5;">
  Changed your mind? <a href="{{ shop.url }}/pages/withdrawal">Withdraw from contract here</a> (14 days from delivery).
</p>
<p style="margin:0 0 24px;font-size:14px;line-height:1.5;">
  Your legal guarantee rights: <a href="https://europa.eu/youreurope/guarantees">europa.eu/youreurope/guarantees</a>
</p>
<img src="NOTICE-PNG-URL" width="300" alt="Legal guarantee: minimum two-year legal guarantee protection for goods sold in the European Union" style="display:block;max-width:100%;height:auto;border:1px solid #dddbd9;">
```

For `NOTICE-PNG-URL`: download the Commission's PNG set ([PNG and JPG.zip](https://commission.europa.eu/document/download/dbd46ba2-77d2-4a74-ad52-120bc7bf02ea_en?filename=PNG%20and%20JPG.zip)), take the colour EN file, upload it under Content → Files, copy its URL. If the notification editor shows a language selector, add the NL and FR sentences and files there (NL `/nl/pages/withdrawal`, `europa.eu/youreurope/garantie`, NL PNG; FR `/fr/pages/withdrawal`, `europa.eu/youreurope/garanties`, FR PNG); otherwise paste all three sentences under each other. Send yourself a test from the template page.

Also check Settings → Notifications → **Sender email**: contact-form submissions (the withdrawal statements) arrive at this address; it must be an inbox care@ reads every working day.

## 6. Loop's emails

Apps → **Loop Subscriptions** → Settings → Notifications → Emails: in "Subscription created" and "Order placed" (and the renewal reminder), add the sentence `Changed your mind? Withdraw from contract here: https://www.karmicare.com/pages/withdrawal (14 days from delivery).` Loop keeps its own copy per language tab: paste the NL and FR sentences from the handoff into the NL and FR tabs by hand. Until the domain switch the host is `karmicares.myshopify.com`.

## 7. Records and operations

- Keep every withdrawal: the store-inbox email (Shopify) and the Klaviyo event on the profile are the proof that the acknowledgement went out (Art. VI.62 WER puts the burden of proof on the trader).
- When the acknowledgement did not go out automatically (the success page showed the fallback line, or the Klaviyo flow was off), reply to the inbox email the same day with the content, date and time: that is the acknowledgement.
- Never unpublish the page or remove the footer link: the function must be available for the whole withdrawal period of every order.
- Online Store → Preferences → Spam protection: leave it on; the challenge page returns to the withdrawal page after the post.

## 8. Checkout (optional, Plus only)

On a non-Plus plan Shopify's information, shipping and payment steps take no custom content, and the law does not require the notice there (REQUIREMENTS.md B2). If the store moves to Plus: Settings → Checkout → Customize → add a text block "Your legal guarantee rights" linking to `/pages/consumer-rights` section 4 on the information step. The Thank-you / Order-status pages accept a text block on every plan: add "Changed your mind? Withdraw from contract here" with the link there now.
