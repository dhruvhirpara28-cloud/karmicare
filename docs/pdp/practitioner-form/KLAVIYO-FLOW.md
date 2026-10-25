# Practitioner request: Klaviyo confirmation and team alert (R76d)

**Created**: 25 Oct 2026, lane practitioner-form. **Decision**: Victor, 25 Oct: "we need this to be sent from karmicare domain, and the confirmation to the customer via Klaviyo". He then chose: a Klaviyo alert to the team as well as Shopify's copy; the event only after Shopify accepted the post; one test event to create the metric.

## 1. What was there (checked 25 Oct, nothing changed in Shopify)

- Shopify admin → Settings → Notifications → Sender email is `info@karmicare.com`. Domain authentication shows "Update recommended". The three original CNAMEs (`mailer17w`, `17w._domainkey`, `17w2._domainkey`) match. The three newer backup records (`mailerfww`, `pdk1._domainkey.mailerfww`, `pdk2._domainkey.mailerfww`) are missing from DNS. DNS for karmicare.com is at Namecheap (`dns1/dns2.registrar-servers.com`), with DMARC set to `p=none`.
- Contact-form posts reach `info@karmicare.com` as "New customer message", **from `mailer@shopify.com`**. Victor's withdrawal test at 12:20 that day arrived that way. Shopify sets that sender for contact forms, and no setting changes it. So the only way to get a karmicare.com sender is to send the mail from somewhere else, which here means Klaviyo.
- Klaviyo (account XfYq2r) sends from `we@karmicare.com` ("KARMICARE") over the sending domain `send.karmicare.com`, whose status is active.

## 2. What the theme sends

`assets/kc-practitioner-request.js` builds the event; the block settings `request_klaviyo_company_id` (`XfYq2r` in both product templates) and `request_klaviyo_metric` (`Practitioner Request Submitted`) say where it goes. On a valid Send, the script saves the request in this tab's sessionStorage. Shopify then posts as before. On the thank-you reload (`form.posted_successfully?`), the script sends one `POST https://a.klaviyo.com/client/events/?company_id=XfYq2r` (headers `Content-Type: application/json`, `revision: 2026-10-15`, `keepalive`) and clears the snapshot. The endpoint, revision and key are the same ones the withdrawal page uses.

Nothing is sent when the key is empty, when the post fails, when hCaptcha stops it, or when storage is blocked. In every case the request still arrives at info@ through Shopify. Reloading the thank-you page does not send the event again.

| Path | Value |
|---|---|
| `metric…name` | `Practitioner Request Submitted` (Klaviyo metric id `UaYZem`, created by the test event of 25 Oct) |
| `profile…email` | the email typed. The profile gets nothing else: practitioners type titles ("Dr. An Peeters"), so a split first name would be wrong. |
| `properties.name` | name as typed |
| `properties.profession` | the radio chosen, always the English value: `Dentist`, `Dental hygienist`, `kPNI therapist`, `Orthomolecular or naturopathic practitioner`, `General practitioner`, `Pharmacist` or `Other` (R76e) |
| `properties.profession_other` | the text typed under Other, else empty |
| `properties.profession_label` | the profession as the visitor read it (the radio label in the page language, or the typed text for Other), for the confirmation email |
| `properties.practice_name` | practice name |
| `properties.email` | email |
| `properties.phone` | phone, or empty |
| `properties.evidence_pack` / `properties.samples` | `true` / `false` |
| `properties.practice_address` | the address, only when samples is ticked, else empty |
| `properties.message` | message, or empty |
| `properties.language` | `en`, `nl` or `fr` (`request.locale.iso_code`) |
| `properties.page` | origin plus path of the product page |
| `time` / `unique_id` | the moment of Send / a UUID made at Send |

In Klaviyo templates every property is `{{ event.<name> }}`.

## 3. The flow (Victor, in Klaviyo)

**State on 25 Oct, 14:30 Brussels time** (built in the Orca browser, checked with the Klaviyo API).
Flow `UAY2YB`, "Practitioner request: confirmation and alert", in **Draft**:

- **Trigger**: metric `Practitioner Request Submitted`, re-entry allowed, no filters.
- **Email #1**, "Confirmation to practitioner":
  - subject "Request received", preview text "Thank you. We reply by email to the address you gave.";
  - from `KARMICARE <we@karmicare.com>`, reply-to `victor@karmicare.com`;
  - Smart Sending off, UTM off, transactional not applied for yet;
  - template: plain. The KARMICARE logo from the Klaviyo image library sits on top (160 px,
    centred, alt "KARMICARE") with no header bar. Below it is one text block with the §4 body,
    then a small grey unsubscribe line (`{% unsubscribe %}`). White background, text and links
    `#222222`, font Helvetica.
  - The default template's purple header bar, white body text, social icons and grey footer
    were removed.
  - Preview with the test event renders every field: the empty phone is skipped, and pack and
    samples join with "and".
- **Internal alert #1** (`send-internal-alert`):
  - to `victor@karmicare.com`, from `KARMICARE <we@karmicare.com>`;
  - subject `Practitioner request from {{ event.name }} ({{ event.language }})`;
  - message: the §4 alert fields.
  - Klaviyo first emails each recipient an opt-in for internal alerts, which Victor confirms once.
- **Left for Victor**:
  - approve the copy;
  - apply for transactional status (§5);
  - then set the flow Live and delete the test profile.

Template decision, Victor, 25 Oct:
- For now, use something simple that already exists, with no branding except the logo on top.
- Use the website's font. The body font is Proxima Nova, from the Adobe Fonts kit `kss0igj`, and
  that kit is served only to the shop's own domains, so it cannot load in an inbox. The email
  therefore uses Helvetica, the closest web-safe face.
- The branded transactional template comes later, with the marketing nurture work. Both
  transactional flows (withdrawal and practitioner) can move to it then.

Steps:

1. Flows → Create flow → Build your own. Name it `Practitioner request: confirmation and alert`. Trigger: Metric → `Practitioner Request Submitted`, with no filters.
2. Add an **Email**, the confirmation to the practitioner: from `we@karmicare.com` "KARMICARE", reply-to `victor@karmicare.com` (or info@). Turn Smart Sending off and UTM tracking off. The texts are in §4.
3. Add an **Internal alert** (email), the team copy, to `victor@karmicare.com`. It is the message from karmicare.com that replaces reading Shopify's `mailer@shopify.com` copy. The texts are in §4.
4. Leave both in Draft until the transactional approval in §5 comes back, then set the flow Live.
5. Delete the test profile `victor+practitioner-test@karmicare.com` (Profiles → that address → Delete) so it never counts as a contact.

## 4. Texts: an EN draft from copy already on the site, waiting for Victor's OK

Every sentence comes from the form (`templates/product.json`, the `request_*` values) or from the withdrawal email footer, with no new claims. NL and FR come through source-copy. Until they exist, the EN email is the fallback for every language, as in the withdrawal flow. When they arrive, wrap each text in `{% if event.language == "nl" %}…{% elif event.language == "fr" %}…{% else %}EN{% endif %}`.

**Confirmation: subject** `Request received`

**Confirmation: preview text** `Thank you. We reply by email to the address you gave.`

**Confirmation: body** (text block)

```
Hello {{ event.name }},

Thank you. We reply by email to the address you gave. A person reads every request.

Your request

Name
{{ event.name }}

Profession
{{ event.profession_label }}

Practice name
{{ event.practice_name }}

Email
{{ event.email }}
{% if event.phone %}
Phone
{{ event.phone }}
{% endif %}
What would you like?
{% if event.evidence_pack %}Evidence pack{% endif %}{% if event.evidence_pack and event.samples %} and {% endif %}{% if event.samples %}Samples for my practice{% endif %}
{% if event.samples %}
Practice address
{{ event.practice_address }}
{% endif %}{% if event.message %}
Message
{{ event.message }}
{% endif %}
KARMICA BV · Vizierstraat 28, 8000 Bruges, Belgium
```

**Internal alert: subject** `Practitioner request from {{ event.name }} ({{ event.language }})`

**Internal alert: body**

```
Name: {{ event.name }}
Profession: {{ event.profession }}{% if event.profession_other %} ({{ event.profession_other }}){% endif %}
Practice name: {{ event.practice_name }}
Email: {{ event.email }}
Phone: {{ event.phone|default:"-" }}
Evidence pack: {% if event.evidence_pack %}yes{% else %}no{% endif %}
Samples: {% if event.samples %}yes{% else %}no{% endif %}
Practice address: {{ event.practice_address|default:"-" }}
Message: {{ event.message|default:"-" }}
Language: {{ event.language }}
Page: {{ event.page }}
```

## 5. The transactional approval

The event creates profiles without email consent. A flow that is not marked transactional skips them, so without approval the confirmation reaches nobody new. The internal alert goes to a fixed address and is not affected. The request goes the same way as the withdrawal one: Klaviyo → Help → Contact support, subject **Transactional Email Request**.

> Account KARMICARE (public key XfYq2r). Flow "Practitioner request: confirmation and alert", link: <flow URL>. Please mark the confirmation email in this flow as transactional. It is the receipt for a request a health professional makes on our product page (evidence pack and/or samples for their practice): one email per request, triggered only by the metric "Practitioner Request Submitted", which our page sends after the request has been accepted. It repeats the request back and says we reply by email. It contains no marketing, no product recommendations and no promotional links.

After approval, set the flow Live. Then make one real request on the live product page (once DH has shipped) with your own address. Expect Shopify's copy at info@, the Klaviyo alert at victor@, and the confirmation in your inbox. Then delete that test profile.

## 6. Open points

- **Privacy Policy**: it must name Klaviyo as processor for practitioner requests (the confirmation and alert), as gate-legal did for the withdrawal acknowledgement. The form's note ("We only process these details to answer your request") stays true.
- **Shopify DNS (optional)**: add the three `mailerfww` CNAMEs from Shopify → Notifications → Email domain authentication at Namecheap. They only matter when Shopify falls back to its backup sender. They don't affect this flow.
- **Plan**: transactional status needs a paid Klaviyo plan (see withdrawal ADMIN-STEPS 4a).
