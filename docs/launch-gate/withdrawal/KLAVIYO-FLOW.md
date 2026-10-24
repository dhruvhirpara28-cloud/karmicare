# Klaviyo flow for the acknowledgement of receipt: everything ready for step 4

**Created**: 2026-10-24 (lane gate-withdrawal, R73). **Decision**: Victor, 24 Oct: "de ontvangstbevestiging moet via klaviyo" (decision 2f: Klaviyo, not Revoq).
**For**: Victor or the landing desk, executing ADMIN-STEPS.md step 4 (4a–4g). This file holds the texts and commands; it makes no Klaviyo call itself. Nothing here is a secret: `XfYq2r` is the account's public API key, the one every onsite Klaviyo snippet exposes. It must not go into the theme template until step 4f.

## 1. What the page does today, and when to switch the key on

Checked in `sections/kc-withdrawal.liquid` and `assets/kc-withdrawal.js` (24 Oct):

| State | What happens on "Confirm withdrawal" | What the consumer reads on the success view |
|---|---|---|
| **Key unset or empty** (now: `klaviyo_company_id` is not stored in `templates/page.withdrawal.json`) | `sendAcknowledgement()` returns `false` at once (`if (!company …) return Promise.resolve(false)`): no request to Klaviyo. The form posts natively to Shopify's contact endpoint; the statement arrives in the store inbox ("New customer message", Type: Withdrawal statement, with the stamped time). sessionStorage records `failed`. | `success_ack_default`: "We acknowledge receipt by email, with the content, date and time of your statement. Keep that email: it is your proof." **care@ sends that email by hand, the same day, from the inbox copy** (ADMIN-STEPS 4f, last paragraph). The promise is kept by a person, so this state is honest. |
| **Key filled** (`klaviyo_company_id` = `XfYq2r`) | One `POST https://a.klaviyo.com/client/events/?company_id=XfYq2r` (8 s timeout, `keepalive`). If the response is 2xx (Klaviyo answers `202 Accepted` as soon as the event is valid), sessionStorage records `sent`; otherwise `failed`. Then the native post to Shopify as above. | `sent`: `success_ack_sent`, "An acknowledgement of receipt is on its way to [email], with the content, date and time of your statement. Keep that email: it is your proof." `failed`: the default line above. |

**Does a filled key fit a flow that is not approved yet? No.** Klaviyo's `202` only says the event was accepted; it says nothing about a flow. With the key filled while the flow is in draft, or live but not marked transactional, the page tells the consumer an email "is on its way" and none goes out: a non-transactional flow skips profiles without email consent, and every profile this event creates has none. That is a false statement on a statutory acknowledgement. So the order is fixed: 4c (metric) → 4d (flow) → 4e (transactional approval, flow Live) → 4g test with a curl event (§5) and a check that the email arrived → only then 4f (key into the section settings, together with the metric name). Until then the page keeps the manual promise, which care@ must keep.

## 2. The event, exactly as `assets/kc-withdrawal.js` sends it

Endpoint `POST https://a.klaviyo.com/client/events/?company_id=<public key>`, headers `Content-Type: application/json` and `revision: 2026-10-15`, body:

| Path in the JSON | Value | Source in the code |
|---|---|---|
| `data.type` | `event` | fixed |
| `data.attributes.metric.data.attributes.name` | `Withdrawal statement submitted` | section setting `klaviyo_metric` (schema default), JavaScript falls back to the same string when empty |
| `data.attributes.profile.data.attributes.email` | the email typed in the form | field `email` |
| `…profile…first_name` / `…last_name` | first word of the name / the rest | field `name`, split on spaces |
| `data.attributes.properties.statement` | "I hereby give notice that I withdraw from my contract of sale for the order below." | `data-kc-statement` = section setting `statement_text` (in the page's language) |
| `properties.name` | the name as typed | field `name` |
| `properties.order_number` | as typed, for example `#1234` | field `order` |
| `properties.email` | as typed | field `email` |
| `properties.items` | as typed, or an empty string for the whole order | field `items` (optional) |
| `properties.submitted_at_local` | for example `October 24, 2026 at 3:42 PM` (`Intl.DateTimeFormat`, dateStyle long, timeStyle short, in the page's locale) | stamped on Confirm |
| `properties.submitted_at_utc` | ISO 8601, for example `2026-10-24T13:42:03.166Z` | same instant |
| `properties.timezone` | `Europe/Brussels` | `data-kc-timezone` |
| `properties.language` | `en`, `nl` or `fr` | `data-kc-locale` = `request.locale.iso_code` |
| `properties.page` | origin plus path, for example `https://karmicares.myshopify.com/nl/pages/withdrawal` | `window.location` |
| `data.attributes.time` | the ISO UTC instant above | stamped on Confirm |
| `data.attributes.unique_id` | a new ID for every confirmed submission: a UUID (`crypto.randomUUID()`), or where that is missing the timestamp plus a random hex string | generated on each Confirm; it is not kept across a reload, so a consumer who submits again after reloading the page creates a second event (and a second acknowledgement) |

In the Klaviyo template every property is reachable as `{{ event.<name> }}` (no spaces in the names, so no `lookup` filter is needed). `submitted_at_local` is already in the consumer's language and in Brussels time; `submitted_at_utc` is the machine-readable proof.

## 3. One flow email for the three languages

Flow: `Withdrawal acknowledgement (Art. VI.61/2 WER)`, trigger Metric → `Withdrawal statement submitted`, no filters, Smart Sending off, no quiet hours, from and reply-to `care@karmicare.com` (ADMIN-STEPS 4d). One email, text-only template, branches on `event.language`; the English branch is the fallback, so an unexpected value still produces an acknowledgement.

**Subject**

```
{% if event.language == "nl" %}Ontvangstbevestiging: je herroeping van {{ event.submitted_at_local }}{% elif event.language == "fr" %}Accusé de réception : votre rétractation du {{ event.submitted_at_local }}{% else %}Acknowledgement of receipt: your withdrawal of {{ event.submitted_at_local }}{% endif %}
```

**Body** (paste as one block into a text email; the French punctuation carries no-break spaces, so copy, do not retype)

```
{% if event.language == "nl" %}
Dag {{ event.name }},

We hebben je herroepingsverklaring ontvangen. Deze e-mail is je ontvangstbevestiging (art. VI.61/2 WER).

Ingediend op: {{ event.submitted_at_local }} ({{ event.timezone }}; UTC {{ event.submitted_at_utc }})
Verklaring: {{ event.statement }}
Naam: {{ event.name }}
Bestelnummer: {{ event.order_number }}
Artikelen: {{ event.items|default:"de volledige bestelling" }}
E-mailadres: {{ event.email }}

Wat er nu gebeurt: stuur de goederen binnen 14 dagen terug naar KARMICA BV, Retouren, Vizierstraat 28, 8000 Brugge, België. We betalen alles wat je betaalde terug, inclusief de standaard leveringskosten, binnen 14 dagen na de dag waarop je het ons liet weten; we mogen wachten tot de goederen terug zijn of tot je hebt aangetoond dat je ze hebt verzonden.

Vragen? Antwoord op deze e-mail of schrijf naar care@karmicare.com. Een mens leest elk bericht.

KARMICA BV · Vizierstraat 28, 8000 Brugge, België · btw BE 0676.972.896
{% elif event.language == "fr" %}
Bonjour {{ event.name }},

Nous avons reçu votre déclaration de rétractation. Cet e-mail est votre accusé de réception (art. VI.61/2 CDE).

Soumise le : {{ event.submitted_at_local }} ({{ event.timezone }} ; UTC {{ event.submitted_at_utc }})
Déclaration : {{ event.statement }}
Nom : {{ event.name }}
Numéro de commande : {{ event.order_number }}
Articles : {{ event.items|default:"toute la commande" }}
Adresse e-mail : {{ event.email }}

La suite : renvoyez les biens dans les 14 jours à KARMICA BV, Retours, Vizierstraat 28, 8000 Bruges, Belgique. Nous remboursons tout ce que vous avez payé, frais de livraison standard compris, dans les 14 jours suivant le jour où vous nous avez informés ; nous pouvons attendre d’avoir récupéré les biens ou que vous ayez prouvé leur renvoi.

Des questions ? Répondez à cet e-mail ou écrivez à care@karmicare.com. Une personne lit chaque message.

KARMICA BV · Vizierstraat 28, 8000 Bruges, Belgique · TVA BE 0676.972.896
{% else %}
Hello {{ event.name }},

We have received your withdrawal statement. This email is your acknowledgement of receipt (Art. VI.61/2 WER).

Submitted on: {{ event.submitted_at_local }} ({{ event.timezone }}; UTC {{ event.submitted_at_utc }})
Statement: {{ event.statement }}
Name: {{ event.name }}
Order number: {{ event.order_number }}
Items: {{ event.items|default:"the whole order" }}
Email address: {{ event.email }}

What happens next: send the goods back within 14 days to KARMICA BV, Returns, Vizierstraat 28, 8000 Bruges, Belgium. We refund everything you paid, including the standard delivery charge, within 14 days of the day you told us; we may wait until the goods are back or you have shown that you sent them.

Questions? Reply to this email or write to care@karmicare.com. A person reads every message.

KARMICA BV · Vizierstraat 28, 8000 Bruges, Belgium · VAT BE 0676.972.896
{% endif %}
```

The texts are the ones in TRANSLATIONS-HANDOFF.md §3 (NL je-form, FR vous). The statement line repeats the statutory statement the consumer confirmed, in the page's language, because `event.statement` carries the section's `statement_text` of that storefront language. Preview in Klaviyo with a test event of each language (§5) before requesting approval; editing the email after approval removes the transactional status (ADMIN-STEPS 4e).

## 4. The transactional approval request

Klaviyo → Help (?) → Contact support, or Customer Success → subject **Transactional Email Request**. Text to send, with the flow link filled in:

> Account: KARMICARE (karmicares.myshopify.com, public key XfYq2r). Flow: "Withdrawal acknowledgement (Art. VI.61/2 WER)", link: <flow URL>.
>
> Please mark the single email in this flow as transactional. It is the acknowledgement of receipt that Belgian law requires us to send to a consumer who withdraws from an online purchase through our withdrawal function (Act of 19 July 2026, Art. VI.61/2 §4 WER, implementing Art. 11a of Directive 2011/83/EU): the acknowledgement must reach the consumer on a durable medium, with the content, date and time of the statement, without undue delay. The flow is triggered only by the metric "Withdrawal statement submitted", which our shop page sends when the consumer presses "Confirm withdrawal"; one email per submission. The email contains only the consumer's own statement, its date and time, the next steps for the return and refund, and our contact details. It contains no marketing, no product recommendations and no promotional link, and it must be sent regardless of the profile's subscription status, because the law requires it for every withdrawal. Subject line: "Acknowledgement of receipt: your withdrawal of <date>" (Dutch and French versions for /nl and /fr). Sender: care@karmicare.com.

Approval takes about one business day. After approval: set the flow Live, run the §5 test, then ADMIN-STEPS 4f.

## 5. Test commands (no theme change; run from any terminal)

**5a. Create the metric and check the branches.** One event per language, with your own email (replace `victor@karmicare.com` if another inbox should receive the test). Expect `202` each time; after a minute the metric shows under Klaviyo → Analytics → Metrics, and the profile's activity shows the three events.

```sh
for lang in en nl fr; do
curl -s -o /dev/null -w "$lang %{http_code}\n" -X POST "https://a.klaviyo.com/client/events/?company_id=XfYq2r" \
  -H "Content-Type: application/json" -H "revision: 2026-10-15" \
  -d "{\"data\":{\"type\":\"event\",\"attributes\":{\"metric\":{\"data\":{\"type\":\"metric\",\"attributes\":{\"name\":\"Withdrawal statement submitted\"}}},\"profile\":{\"data\":{\"type\":\"profile\",\"attributes\":{\"email\":\"victor@karmicare.com\",\"first_name\":\"Victor\",\"last_name\":\"Test\"}}},\"properties\":{\"statement\":\"I hereby give notice that I withdraw from my contract of sale for the order below.\",\"name\":\"Victor Test\",\"order_number\":\"#0000\",\"email\":\"victor@karmicare.com\",\"items\":\"\",\"submitted_at_local\":\"October 24, 2026 at 3:42 PM\",\"submitted_at_utc\":\"2026-10-24T13:42:03.166Z\",\"timezone\":\"Europe/Brussels\",\"language\":\"$lang\",\"page\":\"https://karmicares.myshopify.com/pages/withdrawal\"},\"time\":\"2026-10-24T13:42:03.166Z\",\"unique_id\":\"r73-test-$lang-$(date +%s)\"}}}"
done
```

Each run sends the same statement with `language` en, nl and fr: with the flow Live the three emails must arrive in the three languages. `unique_id` changes per run, so a repeat produces new events; the `#0000` order number marks them as tests. Delete the test profile afterwards (Klaviyo → Profiles → victor@karmicare.com → Delete) so it never counts as a customer.

**5b. Before approval** (flow in draft or live but not transactional): the events above are accepted (`202`) but no email arrives for a profile without consent. That is the state §1 describes; do not fill the key in the theme yet.

**5c. After approval and 4f**: the real test on the live page (ADMIN-STEPS 4g): fill in the form with your own email, press Confirm withdrawal, expect the store-inbox copy and the acknowledgement within minutes, with the same content, date and time. Then delete the test profile again.

**5d. Reading an event back** (optional, for the landing desk, needs a private API key with `events:read`; never paste that key in a file or log): Klaviyo → Analytics → Metrics → "Withdrawal statement submitted" → Activity feed shows every property of §2.

## 6. Open points

- Plan: transactional status needs a paid Klaviyo plan (ADMIN-STEPS 4a). If the account stays on the free plan, the acknowledgement stays manual from the inbox copy, and the page copy already fits that.
- Consent: the event creates or updates a profile with the consumer's email without any marketing consent; the flow may send to it only because it is transactional. Nothing else in Klaviyo may use this metric or profile for marketing; the Privacy Policy names Klaviyo as processor for the acknowledgement (gate-legal handoff in REQUIREMENTS.md).
- Retention: the store-inbox copy and the Klaviyo event both hold the statement; the retention period is a gate-legal/Privacy item, not a theme one.
