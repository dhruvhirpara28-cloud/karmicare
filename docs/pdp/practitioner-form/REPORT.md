# R76: practitioner request form in the kPNI FAQ item

## R76b: the form opens in a popup (Victor, 25 Oct)

"The practitioner capture form needs to come in a popup, not inline." Built on a3e8789 (merge of
`karmicare/soft-launch` a8406f5, where R76 landed). Copy, fields and settings are unchanged. The
R76 notes below still hold, except where this section says otherwise.

**How it works.** The pattern is the professionals quote panel's (`assets/trusted-professionals-quote-panel.js`):

- native `<dialog>` + `showModal()`;
- the page's scrim token `--kc-mapped-surface-overlay-scrim`;
- `body.overflow-hidden` for the scroll lock;
- the KC/Button close (40 × 40 on surface/accent, `kc-icon-close.svg`), labelled with the existing
  locale key `accessibility.close` (Close / Sluiten / Fermer). That is why no new setting was needed.

What the script does (`assets/kc-practitioner-request.js`):

- builds the dialog on `body` and moves the form panel into it. A dialog inside a closed `<details>`
  would not render.
- swaps the link for a button with `aria-haspopup="dialog"` and `aria-controls` pointing to the
  dialog. The dialog has `aria-labelledby` (the form title) and `aria-describedby` (the intro).
  After a success they point to the thank-you title and text instead.
- on open, focus goes to the form title (`tabindex="-1"`). On phones that also keeps the keyboard
  from popping up before the visitor taps a field.
- Tab and Shift+Tab wrap inside the dialog. Escape, the close button and a click on the scrim close
  it. A press that starts in a field and ends outside it (a dragged text selection) does not.
- on close, focus returns to the button and the scroll lock lifts. For the close button and the
  scrim this happens at once; Escape goes through the browser's `close` event.
- after the reload that follows a post, the FAQ item is already open behind (Liquid, as R76) and
  the dialog opens again by itself:
  - success: the thank-you (`role="status"`, announced) is focused;
  - Shopify refused it: the alert is focused, the values are kept (from Shopify plus this tab's
    sessionStorage, as R76).

**Layout** (`assets/kc-practitioner-request.css`):

- 750px and up: a centred panel, `min(560px, 100vw − 32px)` wide, up to `100dvh − 48px` tall,
  scrolling inside, radius md, page surface.
- under 750px: a full-width sheet from the bottom edge, radius on top. The form is taller than a
  phone screen, so it fills the full height. The short thank-you stays a small sheet over the scrim
  instead of a mostly empty screen.
- the close button sits on a zero-height sticky bar beside the title, so it floats top right and
  stays in reach while the panel scrolls.
- fields keep the R76 styling. Inside the popup the thank-you drops its box, since the panel is
  the box.
- opening fades and rises 16px over 0.3s, only under `prefers-reduced-motion: no-preference`.
  Closing has no animation.

**Without JavaScript** nothing changes from R76: the form shows inline under the answer and the link
stays `href="#"`. The `<template>` holding the close button is inert, so it shows nothing. Browsers
without `<dialog>` support also keep the inline form.

**Files:**

- `snippets/kc-practitioner-request.liquid`: the close-button `<template>`, plus ids on the intro
  and the thank-you title and text.
- `assets/kc-practitioner-request.js` and `assets/kc-practitioner-request.css`: the dialog.
- `snippets/product-faq.liquid` needed no change.

**Removed by this change:**

- the inline toggle in the script: `setOpen`, `aria-expanded` and the `kc-pr--js` class on the
  trigger;
- the CSS rule `.kc-pr[hidden]`. Nothing sets `hidden` on the panel any more.

Proof: `git grep -n "aria-expanded\|kc-pr--js\|setOpen\|kc-pr\[hidden\]" -- sections snippets layout templates config assets`
finds only `snippets/sticky-cart-block.liquid`'s own `setOpen` and other components'
`aria-expanded`. Nothing in the practitioner snippet, CSS or JS, or in `product-faq.liquid`.

### R76b checks

Same fixture as R76, updated: `t` and `inline_asset_content` are stubbed, so the close label and
icon render. Every variant ran in Day and Night at 390, 750 and 1440.

| Check | Result |
| --- | --- |
| Trigger: `aria-haspopup="dialog"`, `aria-controls` → the dialog; starts shut, form not inline | pass |
| Click opens a modal dialog (`:modal`), focus on the title, scroll locked, labelledby/describedby targets exist, close button labelled | pass |
| Close button: closes, focus back on the trigger, scroll unlocked | pass |
| Scrim click closes (750 and 1440); a click on the panel padding or a drag out of a field keeps it open; the 390 form fills the screen, so there is no scrim to click | pass |
| Size: centred, ≤ 560px, inside the viewport (750, 1440); 390: full width on the bottom edge, full height for the form, content height for the thank-you | pass |
| Close button still visible and on top when the panel is scrolled to the end | pass |
| Validation, samples → address, valid Send (all R76 checks) inside the dialog | pass |
| Success reload: item open behind, dialog open, thank-you focused, labelledby the thank-you title | pass |
| Error reload: item open behind, dialog open, alert focused, values kept, email message next to the field | pass |
| No-JS: no dialog, link `href="#"`, form inline, native `required` | pass |
| No element wider than the panel, no horizontal scroll, EN/NL/FR | pass |
| Contrast Day/Night (close button included) | AA pass |
| Real keys: see below | pass |

Real keys (`orca keypress` at 1440, focus started on the trigger), with focus and state after
each key:

| Key | Focus | Dialog | Page scroll |
| --- | --- | --- | --- |
| Enter | form title | open | locked |
| Tab, Tab | name, then profession | open | locked |
| Escape | trigger | shut | free |
| Space | form title | open | locked |
| Shift+Tab | close button | open | locked |
| Shift+Tab | Send (wrapped to the end) | open | locked |
| Tab | close button (wrapped to the start) | open | locked |
| Tab | name | open | locked |
| Escape | trigger | shut | free |

As in R76, `:focus-visible` is not observable because the Orca window has no OS focus. The rings
are in the CSS. The matrix ran 24 variant × mode × width runs, plus NL/FR at 390 and FR Night at
750: all pass. Theme Check: exit 0, 19 warnings (baseline), none in these files.

The fixture finishes CSS animations before measuring and screenshotting. The Orca tab
renders no frames between screenshots, so the open animation would otherwise sit on its first frame.

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
