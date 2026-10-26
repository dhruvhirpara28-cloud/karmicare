# Professionals page v1: audit and proposal (phase 1)

**Created**: 26 Oct 2026, lane practitioner-form. **Brief**: `BRIEF-PROFESSIONALS-PAGE-V1.md`.

**Victor's ask, 26 Oct**: "I think we should direct all entry links to the professional page and
simply have the form there for v1 before we build out the whole professional page. PDP should stay
clean for quick high conversion."

**Base**: `karmicare/practitioner-form` at `2ea51a6`, which merges `karmicare/soft-launch` `9a34a45`
(R76h included). **No theme file was changed in phase 1.** The preview is a prototype in
`fixture/` (see §6).

## 1. Summary

- **The page.** There is no professionals page on the live store yet. I propose:
  - the handle `professionals`;
  - a template `templates/page.professionals.json` with one section, `kc-professionals-request`.
    It shows the page title as the H1, then the existing request form inline;
  - the legal page's 720px column, the same family as the withdrawal page.
- **The form stays the same.** Same fields, checks, inbox mail, Klaviyo event and 8 s abort. It is
  the same snippet; it only gets the page section's settings instead of the FAQ block's.
- **The PDP gets clean.**
  - No form, no dialog, and no `kc-practitioner-request.js` or `.css`.
  - The two FAQ links and the Trusted Professionals button become plain links to the page.
- **Entry links keep their language.** They are built from the page object, so `/nl` and `/fr`
  stay in their language.
  - While the page does not exist they fall back to `/pages/contact`, which is live in EN, NL
    and FR.
  - They carry `?from=` so the request still says where it came from.
- **Victor does three things in the Admin** (§3.3): he creates the page, links the header menu item
  "Professionals" to it, and translates the page title.

## 2. Entry points (live, checked anonymously on 26 Oct)

Snapshots of www.karmicare.com were fetched with `fixture/fetch-live.sh`: home and PDP in EN, NL
and FR.

| # | Where | Template / section / setting | Today (href, text) | Proposal |
|---|---|---|---|---|
| E1 | PDP FAQ, kPNI answer | metafield `custom.product_faq` (Admin-held, item `description`), matched by `request_trigger_text` of the `product_faq` block in `templates/product.json` and `product.subscription-item.json` | `href="#"`. EN "Practitioner evidence pack and samples available →", NL "Studiedossier en proefpakketten voor zorgverleners beschikbaar →", FR "Dossier scientifique et échantillons disponibles pour les praticiens →". JavaScript turns it into the dialog button | The theme rewrites the href in Liquid to the page, `?from=pdp-faq-kpni`. Matched the same way as today (URL first, else text). The live trigger text is already translated: EN "evidence pack", NL "studiedossier", FR "dossier scientifique" |
| E2 | PDP FAQ, "For dentists" note | same metafield, item `section_content`, `a.rda-link` with `data-scroll=".founder-quote"` | `href="#"`. EN "Request the evidence pack, patient-ready materials, professional samples and technical documentation →", NL "Vraag het studiedossier, kant-en-klaar patiëntenmateriaal, proefpakketten voor professionals en technische documentatie →", FR "Demandez le dossier scientifique, des supports prêts pour vos patients, des échantillons professionnels et la documentation…". Live: no form (R76g, landed after this snapshot, makes it a dialog button) | Same rewrite, `?from=pdp-faq-dentists`; `data-scroll` is dropped |
| E3 | Trusted Professionals button | `sections/trusted-professionals.liquid`, `button_label` / `button_link`, in `templates/index.json` and `templates/product.subscription-item.json` | `button_link` is empty, so it shows the shared "Coming soon" state. EN "REQUEST A PRACTITIONER SAMPLE", NL "PROEFPAKKET VOOR ZORGVERLENERS", **FR still English** | When `button_link` is empty, the button links to the page: `?from=home-trusted` on the homepage, `?from=pdp-trusted` on the PDP. "Coming soon" stays only when the page does not exist either. The FR label goes to source-copy |
| E4 | Header menu "Professionals" / FR "Professionnels" | Admin menu (main menu), not a theme file | No link, so it shows "Coming soon" in all three languages, desktop and drawer | **Victor, in the Admin**: link the item to the page. A page link follows the language by itself. No `?from=` (a menu item to a page cannot carry one) |
| E5 | Hero badge "Backed by health professionals" | `sections/hero-karmicare.liquid`, `testimonial_badge.link` in `templates/index.json` | Anchor to the Trusted Professionals section on the same page | Keep: it is about the ambassadors' cards, not the request |
| E6 | Texts without links | `stat-strip-karmicare` tagline, PDP `highlights_slider` "Used by +100 kPNI practitioners", `professional_testimonials` heading | No link | Keep |
| E7 | Evidence links, not professionals | "Explore the full evidence base" (`research-behind-system`, Coming soon); PDP `bf-see-all` / `bf-evidence-link` (`href="#"`, NL "Bekijk alle documenten →", FR "VOIR LE RÉSUMÉ DE L'ÉVALUATION", "DÉCOUVRIR NOTRE SCIENCE") | — | Out of scope: these belong to the Science page that comes later (memory: "Read the science" is held) |
| E8 | The form itself | `snippets/product-faq.liquid` renders `kc-practitioner-request` in the kPNI item | Live on EN, NL and FR (R76e/f: radios, Klaviyo key; R76g "Opened from" not yet live) | Removed from the PDP |

The footer has no professional or evidence link.

## 3. The page

### 3.1 Handle and template

- `curl` without cookies returns **404** on all of these, so no page exists:
  - `/pages/professionals`, `/pages/professional`, `/pages/practitioners`;
  - `/pages/for-professionals`, `/pages/professionals-1`;
  - `/nl/pages/professionals`, `/fr/pages/professionals`.
- **Handle `professionals`**: the same word as the menu item in EN and NL. In FR, Translate & Adapt
  can give the page its own URL handle, for example `professionnels`. That is optional; the
  English handle works on `/fr/` too.
- **`templates/page.professionals.json`**: one section, `kc-professionals-request`, as in the
  preview (`fixture/proto/kc-professionals-page.liquid`):
  - the eyebrow (a setting);
  - `page.title` as the H1 (Admin, translatable under Pages);
  - the snippet `kc-practitioner-request`, with `s: section.settings`, no trigger and inline.
  - The page body (`page.content`) is not shown in v1.
- **v1 does not block the full page** (Figma `3810:3`). The template has one section; the later
  sections are added above or below it, and the form section keeps its own settings.

### 3.2 Links that cannot break

All entry links use the footer withdrawal link's pattern: an optional page picker in the
settings, else `pages['professionals']`.

- Then `page.url` plus `?from=…`. Shopify localises `page.url` (`/nl/pages/…`, `/fr/pages/…`).
- Until the page exists, the links point to **`/pages/contact`** in the page's language, without
  `?from=`. That page is live in EN, NL and FR.
- The Trusted button keeps "Coming soon" in that case. The FAQ links cannot: they are text in the
  metafield, and a "Coming soon" would read oddly there.
- **Order of the rollout.** The template has to be in the published theme before the page can
  pick it. So:
  1. DH ships the theme;
  2. Victor creates the page (§3.3), and every link turns to it at once;
  3. Victor links the menu item.

  Between steps 1 and 2 the FAQ links go to the contact page, and the PDP has no form any more.

### 3.3 Victor's Admin steps (store writes, his to do)

1. **Online Store → Pages → Add page.**
   - Title `Professionals`; content empty.
   - Search engine listing: URL handle `professionals`.
   - Theme template `page.professionals`; Visible. Save.
2. **Online Store → Navigation → Main menu.**
   - Edit the item "Professionals": Link = Pages → Professionals. Save.
   - The NL and FR menu labels already exist in the store.
3. **Translate & Adapt → Pages → Professionals.**
   - Title NL `Professionals`, FR `Professionnels`. These are the menu's own labels.
   - Optional: FR URL handle `professionnels`.
4. **After step 1, a check:** open `/pages/professionals`, `/nl/pages/professionals` and
   `/fr/pages/professionals` in a private window.

## 4. Settings and translations

### 4.1 What moves

- **To the page section** `kc-professionals-request`:
  - every visible `request_*` key, with the same names, so the snippet does not change: title,
    intro, labels, the seven professions, help texts, privacy, button, errors and thank-you;
  - `request_klaviyo_company_id` and `request_klaviyo_metric`;
  - a new `eyebrow`.
  - The EN values go into `templates/page.professionals.json`.
- **Stays in the `product_faq` block**, for finding the two FAQ links:
  - `request_trigger_url` and `request_trigger_text`. Their live NL/FR translations ("studiedossier",
    "dossier scientifique") stay as they are;
  - plus a page picker `professionals_page` (empty uses `pages['professionals']`).
  - The checkbox `request_enabled` becomes "Link the FAQ to the professionals page" (same id) or
    goes; see D7.
- **Removed from both product templates and from the `product_faq` schema**: all other `request_*`
  keys. That is 37 of the 38 `request_*` values in `templates/product.json` today, all but
  `request_trigger_text`. `request_trigger_url` is a schema default and stays in the schema. Phase
  2 adds a `git grep` proof.

### 4.2 Translations (source-copy, on hold for these keys)

Translate & Adapt keeps translations per template and section, so the keys on the new page section
start without NL and FR.

- **Carried 1:1**: 16 keys have a live NL/FR value today, and source-copy can re-enter it unchanged.
  The fixture matched them automatically (`fixture/out/settings-carried.json`, from
  `fixture/live/form-texts-live.json`):
  - name, email, phone and message labels;
  - the choice question and help, "Evidence pack" / "Studiedossier" / "Dossier scientifique",
    samples and address;
  - the button;
  - the name, email, format, choice and address errors;
  - the title.
- **Also translated live** but not visible in the empty form: the privacy note and link, the
  generic error and the thank-you. Source-copy has those in its records.
- **Never translated** (still EN on /nl and /fr today), 13 R76e keys:
  - `request_legend_profession`;
  - the seven `request_profession_*` keys;
  - `request_label_profession_other` and `request_label_practice`;
  - `request_error_profession_choice`, `request_error_profession_other` and
    `request_error_practice`.
- **New**: `eyebrow` (EN "PROFESSIONAL PARTNERS", the existing Trusted Professionals subheading)
  and the changed `request_intro` (D4). The page title is Victor's, in Translate & Adapt Pages.
- **Separately**: the Trusted button's FR label is still English ("REQUEST A PRACTITIONER SAMPLE").

### 4.3 The PDP and the assets

- `snippets/product-faq.liquid` no longer renders the form. Its pre-pass stays only to find the
  two links and rewrite their href; the snippet's `<link>` and `<script>` go with it. So
  `kc-practitioner-request.js` and `.css` no longer load on the PDP.
- **Dead code after the move** (cleanup rule, removed in phase 2 with proof): in the script, the
  dialog, the trigger buttons, `findTriggers()`, `backInline()` and the focus return to the
  opener (R76b, c and g); in the CSS, the dialog, scrim, sheet and trigger styles.
- **What stays**: the inline form, the checks, the Other field, the error restore from
  sessionStorage, the Klaviyo event on the thank-you reload, and the 8 s abort.
- **The purchase controls and the Loop widget are not touched.**

## 5. "Opened from" without the dialog

- Each entry link carries one fixed slug:
  - `?from=pdp-faq-kpni`, `pdp-faq-dentists`, `pdp-trusted` or `home-trusted`;
  - nothing from the header menu or a direct visit.
- On the page, the script reads `from` and accepts it only if it is in that list. It writes the slug
  into the hidden `contact[Opened from]` (in the inbox mail) and into the sessionStorage snapshot.
- The snapshot carries it through Shopify's post and reload, where `?from` is gone. It then goes to
  Klaviyo as `opened_from`, which the internal alert already shows.
- **No personal data in the URL.** An unknown value is ignored.
- The fixture's `fx.js` has a prototype of this; with `?from=pdp-faq-kpni` the hidden field reads
  `pdp-faq-kpni`.
- **Klaviyo**: nothing to change in the flow. The values become slugs instead of FAQ titles (D5).

## 6. Preview (localhost)

**Where**: `fixture/` in this worktree (README). Serve `out/` on `127.0.0.1:9376`.

| Page | URL |
|---|---|
| The page, EN (try `?mode=night`, `&from=pdp-faq-kpni`) | http://127.0.0.1:9376/page-en.html |
| NL, FR (live NL/FR values where they exist, else EN, as it would be today) | `page-nl.html`, `page-fr.html` |
| States | `page-en-success.html`, `page-en-error.html`, `page-en-nojs.html` |
| The PDP before (live) and after | `pdp-before.html`, `pdp-after.html` (open "For dentists" in the FAQ) |

- **Checks** (`fixture/checks.sh`, `fixture/results/v1-checks.txt`): **28 of 28 runs pass**: 7
  variants × 390 / 1440 × Day / Night.
  - The page has one H1, no dialog and no trigger, the form inline, 7 radios, a column of at most
    720px with a 20px gutter, and no horizontal overflow.
  - The error alert and the thank-you show.
  - Without JavaScript, the native `required` is in place.
  - With `?from`, the hidden field follows.
  - The PDP after has no form and no form assets; the two FAQ links and the Trusted button go to
    the page with their slug.
- **Screenshots** (`fixture/shots/`):
  - `page-390-day.png`, `page-390-night.png`, `page-1440-day.png`, `page-1440-night.png`;
  - `page-form-390-*.png`;
  - `pdp-before-faq-390.png`, `pdp-after-faq-390.png`, and the same at 1440.
- **Not in the preview**: real Shopify posts and hCaptcha, inbox and Klaviyo delivery. These are
  unchanged from R76h. The header menu link is Victor's Admin step (E4).

## 7. Decisions for Victor

| # | Decision | My recommendation |
|---|---|---|
| D1 | The page's handle | `professionals`, the menu's own word. FR handle `professionnels` optional |
| D2 | The page head | The H1 is the page title "Professionals" (Admin, translatable), with the eyebrow "PROFESSIONAL PARTNERS" (existing copy) above it. Without the eyebrow is fine too |
| D3 | Where the links go while the page does not exist | `/pages/contact` in the page's language. The Trusted button keeps "Coming soon" until then |
| D4 | The form intro on the page | Drop "The evidence pack holds the studies referenced above." (it points at the PDP FAQ) and keep the two other sentences as they are: "Tell us about your practice and what you need. A person reads every request and replies by email." A new sentence would be new copy |
| D5 | "Opened from" | `?from=` with the four fixed slugs, checked against a list, kept through the post; slugs instead of FAQ titles in the inbox and Klaviyo |
| D6 | The header menu | You link "Professionals" to the page in the Admin (§3.3). A page link follows the language by itself |
| D7 | The FAQ switch | Keep `request_enabled` under a new label, "Link the FAQ to the professionals page", so the rewrite can be turned off in the editor. Or drop it and always link when the page exists |
| D8 | The dialog code | Remove it from the script and the CSS (cleanup rule). The professionals page never needs it, and the git history keeps it |
| D9 | Rollout order | The theme first (the template has to exist), then you create the page and link the menu. Until then the FAQ links go to the contact page |
| D10 | Translations | Source-copy re-enters the 16 carried NL/FR values on the new section and translates the 13 R76e keys, the eyebrow, the intro and the Trusted button's FR label in one batch |

## 8. Phase 2 (after Victor's yes)

**Build**:
- `sections/kc-professionals-request.liquid` and `templates/page.professionals.json`;
- the page variant of the form CSS;
- `product-faq.liquid`: no form, rewrite the two links;
- `trusted-professionals.liquid`: the page as the fallback link, slug from `request.page_type`;
- the script: `?from` in, the dialog code out;
- schema and template clean-up, with `git grep` proof.

**Commits**: by pathspec.

**Checks**:
- Theme Check: 0 errors, 19 baseline warnings;
- the fixture suites: page EN/NL/FR, success, error, no-JS, Klaviyo abort, long labels, `?from`;
- the PDP without the form, with the purchase controls and the Loop widget unchanged.

**Then**: `merge_ready` "NEEDS REVIEW: professionals page v1 over <base>..<head>".
