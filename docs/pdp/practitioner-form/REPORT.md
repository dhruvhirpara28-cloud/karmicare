# R76: practitioner request form in the kPNI FAQ item

Victor, 24 Oct: "the Practitioner evidence pack and samples available → inside the kpni accordion
needs a form capture … now it can sent a request straight to victor@karmicare.com".

Branch `karmicare/practitioner-form`, base f4dce75. Theme files only, nothing in Admin.

## What changed

| File | Change |
| --- | --- |
| `snippets/kc-practitioner-request.liquid` (new) | The form: Shopify's native `{% form 'contact' %}`, as on the withdrawal page. Success and error states. |
| `assets/kc-practitioner-request.js` (new) | Turns the trigger link into a toggle button and checks the fields before the post. After the reload it moves focus and scroll to the thank-you or the alert. |
| `assets/kc-practitioner-request.css` (new) | KC tokens only, Proxima Nova (`--kc-font-role-backbone`). Fields follow `assets/kc-withdrawal.css` at the FAQ answer's scale. |
| `snippets/product-faq.liquid` | Finds the FAQ item whose answer has the trigger link and renders the form inside it, once. Opens that item after a post. Nothing else changed. |
| `sections/main-product.liquid` | `product_faq` block schema only (one hunk at line 3306): an on/off checkbox, the two trigger settings and 25 copy settings. |
| `templates/product.subscription-item.json`, `templates/product.json` | The EN value of every visible string written into `product_faq_block.settings`, so Translate & Adapt gets a key for each (R73). |

## What the live link is today

The brief expected `mailto:victor@karmicare.com`. It is `href="#"`, a link that goes nowhere:

```html
<a href="#">Practitioner evidence pack and samples available →</a>
```

The store answered HTTP 429 to both anonymous fetches I made (more than 5 s apart). So the evidence
is the saved live captures in the other lanes, every one from 22 Oct to 24 Oct 20:30 CEST: EN, NL and
FR all show `href="#"`. The NL and FR pages still show the English answer text.

What that means here:

- **Matching.** The URL trigger keeps the brief's default `mailto:victor@karmicare.com`, but today
  no link matches it. The fallback "link text contains `evidence pack`" is what finds the link. The
  search covers only the answer text (`item.description`) and takes the first item with a match, so
  the "For dentists" item's link ("Request the evidence pack, patient-ready materials…") cannot catch
  it, because that link sits in `section_content`. The fixture checks this.
- **Without JavaScript.** Keeping the link "as it works today" would leave a dead `#`. So the
  form is not hidden without JavaScript: it shows under the answer text, with native `required`
  checks on name, profession and email. The link itself stays exactly as it is. With JavaScript the
  form starts hidden and the link becomes the toggle.
- **NL and FR.** `request_trigger_text` is written into both templates. If source-copy later
  translates the answer text in Admin, it should translate this setting too (for example
  "bewijsdossier"). Otherwise the form still renders, but it stays open under the answer.

## How it behaves

- The theme renders the form once, inside the matching item, right after the answer text. The
  script swaps the link for a `<button type="button">` with the same content, `aria-expanded` and
  `aria-controls`. Enter and Space toggle it. The accordion opens and closes as before
  (`name="faq-accordion"`, the existing click handler unchanged).
- **Fields.**
  - Required: name, profession and practice, email.
  - Optional: phone, message.
  - "What would you like?" (Evidence pack / Samples for my practice) needs at least one ticked.
  - Practice address is required only when Samples is ticked. The label says so and the script
    sets `required`/`aria-required`.
  - Errors show under each field, `aria-invalid` is set and focus goes to the first problem.
  - No newsletter or marketing box.
- **Inbox keys** are fixed English, so every language arrives the same way:
  - `contact[name]`, `contact[email]`, `contact[phone]`, `contact[body]` (message);
  - `contact[Profession and practice]`, `contact[Evidence pack]` = Yes,
    `contact[Samples for my practice]` = Yes, `contact[Practice address for samples]`;
  - hidden: `contact[Type]` = "Practitioner request: evidence pack / samples",
    `contact[Language]` (`request.locale.iso_code`), `contact[Page]` (origin + path).
- **Privacy note.** `[privacy]` in the note becomes a link to `pages['privacy-policy'].url`, else
  `shop.privacy_policy.url`, the same lookup the footer uses. Shopify prefixes that URL with the
  page language.
- **After the post** Shopify reloads the page at `#KcPractitionerRequest`:
  - Success (`form.posted_successfully?`): the Liquid renders the kPNI item `open` with a thank-you
    in place of the fields (`role="status"`, `aria-live="polite"`). The script sets the text again
    so screen readers announce it, then focuses it and scrolls it into view.
  - Errors (`form.errors`): the item is open and an alert lists Shopify's messages with links to the
    fields. The email field gets `aria-invalid` and its message. Name, email, phone and message come
    back from `form.*`. Profession, the ticks and the address are not returned by Shopify, so the
    script keeps them in this tab's `sessionStorage` for that one reload and clears them at once.
    Any other page load also clears them.
- **No clash with other forms.** `form.posted_successfully?` and `form.errors` belong to the form
  type. The footer newsletter is `{% form 'customer' %}`, which Shopify answers with
  `customer_posted`, so neither form shows the other's state. No other contact form renders on the
  PDP templates (`grep "form 'contact'"`: only `sections/contact-form.liquid` and the withdrawal
  section). If a second contact form were ever added to the PDP, both would show success together.
- **Kill switch.** Untick "Show the request form" on the block and the snippet renders nothing. The
  link stays as it is (fixture variant `en-disabled`).

## Where the requests go (Victor checks, nothing changed in Admin)

Shopify sends every contact-form post to the store's customer-facing email address: **Settings →
General → Store details**, shown as "Sender email" in the current admin (older admins called it
"Customer email"). The withdrawal statements go to the same inbox. The email arrives as Shopify's
"New customer message" with the fields above. `Type: Practitioner request: evidence pack / samples`
tells it apart.

- If that address is victor@karmicare.com, nothing to do.
- If it is care@ (or another inbox), changing it also changes the From address of every order
  email. The lighter route is a Gmail filter on that inbox: messages containing "Practitioner
  request: evidence pack" forward to victor@karmicare.com. That is Victor's call.
- Shopify may show its hCaptcha check before accepting a contact post. That is Shopify's flow and
  the theme cannot change it.

Victor can confirm the route with one real request from the live PDP once DH has shipped it. I sent
nothing to the store.

## Copy for Victor's approval (EN)

Peer to peer and evidence first, with few colons or dashes. No commodity words, no claims, numbers
or new promises. "A person reads every…" follows the withdrawal page's "A person reads every
message".

| Setting | EN |
| --- | --- |
| Title | Request the practitioner pack |
| Intro | Tell us about your practice and what you need. The evidence pack holds the studies referenced above. A person reads every request and replies by email. |
| Name | Name |
| Profession | Profession and practice |
| Profession help | For example kPNI therapist, practice name |
| Email | Email |
| Phone | Phone (optional) |
| Choice question | What would you like? |
| Choice help | Choose one or both. |
| Choices | Evidence pack / Samples for my practice |
| Address | Practice address (needed for samples) |
| Message | Message (optional) |
| Privacy note | We only process these details to answer your request. More in our [privacy]. (link text "Privacy Policy") |
| Button | Send request |
| Errors | Please fill in your name. / Please fill in your profession and practice. / Please fill in your email address. / Please enter a valid email address. / Choose the evidence pack, samples or both. / Please fill in the practice address for the samples. |
| Shopify refused it | Your request was not sent. Please check the details below and try again. |
| Thank-you | Request received / Thank you. We reply by email to the address you gave. |

Open points for Victor:

1. **Button.** "Send request" is a form action, not a plan CTA, so I did not use "Begin your …".
   If the Begin rule covers form buttons too, change `request_button`.
2. **Speed of reply.** No time is promised ("within two working days" would be a new promise).
3. **Dentists link.** The "For dentists" item's link scrolls to the founder quote. It could open
   the same form later, but that is not in scope here.

NL and FR: send the 26 template keys `sections.main.blocks.product_faq_block.settings.request_*`
(both product templates) to source-copy once Victor approves the EN. The fixture's NL and FR
strings are placeholders for the length test only.

## Checks

Fixture: liquidjs renders this branch's `snippets/product-faq.liquid` and the new snippet, with
`{% form %}` stubbed to mock `form` objects (default, success, error). The FAQ items come from a
saved DOM of the live PDP (24 Oct 17:18 CEST, `live-pdp.html` from the xylitol-image lane), and the
output is spliced into that DOM. The form action points at the localhost server and a fixture
listener stops every submit, so nothing reaches the store. Served with `python3 -m http.server`
on 127.0.0.1:9376 and run in Orca's browser with an isolated anonymous profile.

| Check | Result |
| --- | --- |
| Toggle: button, `aria-controls`, starts closed, click opens right under the link, click closes | pass |
| Required fields: empty Send blocked, errors on name, profession, email and the choice, focus on name | pass |
| Typing clears an error; bad email shows the format message | pass |
| Samples ticked: address required, only the address error, focus there; unticked: optional again | pass |
| No choice ticked: choice error, focus on the first box; ticking clears it | pass |
| Valid Send goes through (stopped by the fixture) with all inbox keys and hidden fields | pass |
| Success: item open, thank-you focused, `role=status` + `aria-live`, other items closed, footer newsletter not in success | pass |
| Error: item open, alert focused, email `aria-invalid` + message, values kept, alert links to the field | pass |
| Labels on every field, `aria-describedby` targets exist, legend on the choices | pass |
| No-JS (all scripts stripped): link untouched (`href="#"`), no button, form visible, native `required` | pass |
| Block setting off: no form, link untouched | pass |
| No horizontal overflow at 390 / 750 / 1440, EN, NL and FR (FR has the longest strings) | pass |
| Contrast, Day / Night: labels and input text 15.75, help and note 7.28 / 7.94, alert and thank-you 11.95, input border 7.28 / 7.94 | AA pass |
| Real keys (`orca keypress`): Enter and Space toggle; Tab goes name → profession → email → phone → pack → samples → address; Enter in a field runs the checks | pass |

Not observable in this setup:

- The `:focus-visible` ring. The Orca window had no OS focus (`document.hasFocus()` false), so the
  pseudo-class never matched. The rings are in the CSS: a 2px `--kc-mapped-border-focus-strong`
  outline on fields, boxes, the toggle, links and the alert/thank-you, 15.75:1 against the
  background in Day and Night.
- A real Shopify post, hCaptcha and Shopify's own error wording. No submissions to the live store.

Theme Check (`shopify theme check --fail-level error`): exit 0, 0 errors, 19 warnings (the
baseline), none in the changed files.

Screenshots (22) and the fixture scripts are in the session scratchpad
`/private/tmp/claude-501/-Users-iamvictorious-IdeaProjects-orca-workspaces-karmicare-shopify-theme-practitioner-form/278123b6-4698-4965-9305-76380fe130fe/scratchpad/fx/`
(`render.mjs`, `fx.js`, `run.sh`, `shot.sh`, `keys.sh`, `shots/`, `results/`).

## Cleanup check

Nothing became obsolete: the diff adds only. No class, setting, snippet or asset was removed or
renamed (`git diff f4dce75 --stat` shows two lines replaced, both in the templates' `product_faq_block`
settings, where `"default_to_subscription": true` gained a comma). The new names are referenced:
`git grep -n "kc-practitioner-request"` hits only `snippets/product-faq.liquid` (render) and
`snippets/kc-practitioner-request.liquid` (the CSS and JS tags).
