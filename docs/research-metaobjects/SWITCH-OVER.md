# Research cards as metaobjects · switch-over (R67)

Victor, 24 Oct 2026: "the cards must be seen as global components that can be used
everywhere". He chose metaobjects. The five research cards were duplicated as blocks in
`templates/index.json` and `templates/product.subscription-item.json`, so every edit
happened twice. R67 teaches the theme to read the cards from `research_card` metaobject
entries instead; a parallel admin task creates the definition and the five entries.

**Nothing changes on the storefront until a template is switched over.** The switch is a
template edit (§3) that Victor or the landing desk makes after the launch. Until then the
section renders its blocks exactly as at b0bb4fb (proven in §9).

## 1. What R67 built (theme side)

| File | Change |
|---|---|
| `sections/research-behind-system.liquid` | New setting **Research cards** (`cards`, type `metaobject_list`, `metaobject_type: "research_card"`) under a "Cards" header. When set, the entries render in the picker's order; when empty, the section's Research Card blocks render as before. The card list is built once (`card_items`) and placed in the marquee or the grid/slider, so the three layouts cannot drift apart. |
| `snippets/research-card.liquid` | Accepts either `block:` (a section block) or `card:` (a `research_card` entry) and prints the card body as before; the section keeps the `<li>` wrapper, so the block path is byte-identical to b0bb4fb. Same HTML, classes and behaviour: the study link opens in a new tab with the screen-reader text, a blank or `#` URL prints a plain label, an image switches the `<li>` to `research-card--media` (the wide variant), the marquee's keyboard focus and clones work unchanged. |
| `snippets/kc-rich-text-inline.liquid` | New. Prints a `rich_text_field` as inline HTML (`strong`, `em`, `a`, `<br>` between paragraphs) so it can sit inside the card's `<h3>`; Shopify's `metafield_tag` would wrap it in `<div><p>`. Falls back to escaped text with `<br>` for a multi-line field. Links become an `<a>` only for `http`, `https`, `mailto`, `tel` and scheme-less relative, query or anchor URLs; `javascript:`, `data:`, `vbscript:` and every other scheme print their text without a link, whatever the case or surrounding whitespace. Every attribute is escaped; `target` is printed only as `_blank`, with `rel="noopener"`. Reusable for any metaobject heading. |

Field mapping (the shared contract, type handle `research_card`):

| Entry field | Type | Prints as | Block setting it replaces |
|---|---|---|---|
| `subheading` | single line | escaped text | `subheading` (text) |
| `heading` | rich text | inline HTML via `kc-rich-text-inline` | `heading` (inline_richtext) |
| `subtext` | multi-line | escaped, line breaks as `<br>` | `subtext` (text) |
| `result_label`, `method_label` | single line | escaped text | same (text) |
| `result_text`, `method_text` | multi-line | escaped, `<br>` | same (inline_richtext) |
| `link_label` | single line | escaped text, never translated | `link_label` (text) |
| `link_url` | URL | `href`, `target="_blank" rel="noopener"`; blank or `#` → plain label | `link_url` (url) |
| `logo` | file (image) | `image_url: width: 200` + `image_tag` | `logo` (image_picker) |
| `image` | file (image) | `image_url: width: 800` + `image_tag`, wide card | `image` (image_picker) |
| `image_badge` | single line | escaped text, only with an image | `image_badge` (text) |

Two deliberate differences from the block path, invisible on the five cards: entry text is
HTML-escaped (a block's `text` setting prints raw, so `Lei & Hu` becomes `Lei &amp; Hu`
in the source, the same on screen), and `result_text` / `method_text` lose the
inline_richtext bold and italic (the contract made them multi-line text).

**Where the component can be used.** The section has a preset, so "Add section" offers
Research Behind System on every template; pick the entries in the Research cards setting
and the same cards appear with the same markup and CSS. That is the global component. A
single-card block for other sections is a proposal only (§7).

## 2. Prerequisites (admin side, done 24 Oct 2026 by the parallel R67 admin task)

1. Metaobject definition **Research card**, handle `research_card`, with the contract's
   twelve fields. Capabilities: **Storefront access on** (without it the theme cannot read
   the entries and the theme editor shows an error on the setting), **Translations on**,
   **Publishing on**. Deviation from the contract: the display name is `link_label`, not
   `heading` (Shopify refuses a rich text field as display name); `heading` is a rich text
   field, which the theme renders inline. Neither changes the theme side.
2. Five entries, status **Active**, content from `templates/index.json` →
   `research_behind_system_EkjATL` at b0bb4fb. Handles, as used in `TRANSLATIONS.md`:
   `kulal-2016`, `lei-hu-2025`, `janakiram-2017`, `vano-2018`, `alli-2019`. Known content
   state: Lei & Hu `result_text` without the stray `&nbsp;`; Janakiram carries the new
   xylitol photo `kc-research-xylitol-1122x1402-v1.jpg` (R66) but still the dentine-tubules
   `image_badge`, which the landing desk fixes in admin before the switch (§4).
3. A **Draft** entry is not visible to the storefront (Shopify: the setting "returns blank if
   no selection has been made, the selection isn't visible, or the selection no longer
   exists"). A draft is not a per-card rollback (§8).
4. The R67 theme code landed and shipped by DH. The theme editor shows a notice on the
   Research cards setting for as long as the definition is missing or not storefront-
   accessible; the page itself still renders the blocks.

## 3. The template change

Both templates have the same section id and the same block order, so the change is the
same JSON on both pages: add the `cards` array to the section's `settings`. Order on the
homepage and on the PDP, as `block_order` today:

| # | Entry handle | Study | Block id today |
|---|---|---|---|
| 1 | `kulal-2016` | Kulal et al. 2016 (nano-HAp, dentine tubules) | `card_bDxUVT` |
| 2 | `lei-hu-2025` | Lei & Hu 2025 (oral health and sleep) | `card_yMiD9D` |
| 3 | `janakiram-2017` | Janakiram et al. 2017 (xylitol, caries) | `card_fmFMFd` |
| 4 | `vano-2018` | Vano et al. 2018 (nano-HAp, sensitivity) | `card_Hi7YUD` |
| 5 | `alli-2019` | Alli et al. 2019 (SLS-free, canker sores) | `card_JeERX6` |

In `templates/index.json`, section `research_behind_system_EkjATL`, inside `"settings": {`
(line 565 at b0bb4fb), after the `"heading"` line:

```json
        "heading": "The research behind the system",
        "cards": [
          "gid://shopify/Metaobject/<id of kulal-2016>",
          "gid://shopify/Metaobject/<id of lei-hu-2025>",
          "gid://shopify/Metaobject/<id of janakiram-2017>",
          "gid://shopify/Metaobject/<id of vano-2018>",
          "gid://shopify/Metaobject/<id of alli-2019>"
        ],
```

In `templates/product.subscription-item.json`, the same section id, `"settings": {` at
line 620, after `"heading": "The research <em>behind the system</em>",` (line 622): the
same `cards` array, the same five ids in the same order.

The numeric id is the last path segment of the entry's admin URL
(`…/content/entries/research_card/<id>`); the GID is `gid://shopify/Metaobject/<id>`. The
other route is the theme editor: open the section, pick the five entries in Research cards
in that order, save, and pull the template; the editor writes the same array. Either way
the switch is Victor's or the landing desk's: agents make no admin writes, and DH ships
`main`.

Leave `blocks` and `block_order` in place for this first release. They are ignored while
`cards` is set and they are the rollback (§8).

## 4. What changes on screen at the switch

The entries are built from the homepage blocks, so the homepage keeps its text. The two
templates had drifted, and one entry now serves both, so these are the visible changes:

| Card | Homepage today | PDP today | Entry | Change on screen |
|---|---|---|---|---|
| `janakiram-2017` `image` | `Picture_1.png` (dentine tubules, nothing to do with the study; `docs/science-imagery/IMAGE-PLAN.md` K4 = remove) | none | `kc-research-xylitol-1122x1402-v1.jpg` (R66) | homepage: the xylitol photo instead of the tubules; PDP: the card becomes the wide variant |
| `janakiram-2017` `image_badge` | `DENTINE TUBULES · OPEN AND OCCLUDED` | same | still the tubules label: **the landing desk replaces it in admin before the switch** (the badge sits on the xylitol photo) | homepage and PDP: the new badge text |
| `alli-2019` `image` | `Picture_1.png` (K4 = remove) | none | **check the entry**; recommended: none, as on the PDP and per K4 | homepage: text-only (380 wide) card if none |
| `kulal-2016`, `vano-2018` `image` | `Picture_1.png` | `Picture_1.png` | `Picture_1.png` as today (K5 "hide Kulal until its source is in the library" is not reopened here) | none |
| `alli-2019` `image_badge` | `DENTINE TUBULES · OPEN AND OCCLUDED` | `DENTINE TUBULES - OPEN AND OCCLUDED` (hyphen) | a badge only shows with an image | none while the card has no image |
| `janakiram-2017` labels | `Result` / `Method` | same | `RESULT` / `METHOD` like the other cards | none (the CSS uppercases) |
| `lei-hu-2025` `result_text` | ends in `&nbsp;` | same | without the trailing space | none |
| Theme editor | click a card → block panel | same | the cards are edited in Content > Metaobjects; clicking a card in the editor selects the section | editor only |

Everything else prints the same: the fixture compares the entries' DOM with the blocks'
DOM card by card (§9).

## 5. What to remove afterwards

After one release with `cards` set on both templates and checked on the live store (EN,
NL, FR):

1. **The duplicated blocks.** In both templates, delete the section's `blocks` object (ids
   `card_bDxUVT`, `card_yMiD9D`, `card_fmFMFd`, `card_Hi7YUD`, `card_JeERX6`) and the
   `block_order` array. Nothing else in the template refers to them.
2. **The block path in the code**, so the cards can only come from the entries, which is
   what "global component" means: the `card` block type and the `presets.blocks` in the
   section schema, the `{% else %}` branch of the `card_items` capture, and the `block`
   branch of `snippets/research-card.liquid` (the `else` of its `liquid` block and of the
   `card_heading` capture). Keep `item_class`. Prove with
   `git grep -n "research-card" -- sections snippets templates` that only the section renders
   the snippet, and with `git grep -n '"type": "card"' templates` that no template still
   carries a card block. Recommended, not required: a page that needs a one-off card can
   get its own entry.
3. **The template translations of the blocks.** 45 NL and 45 FR entries per template
   (`index:research_behind_system_EkjATL/card_*/*` in `docs/localization/{nl,fr}/batch-01-homepage.json`,
   `product.subscription-item:…/card_*/*` in `batch-02-pdp.json`) and the matching
   `docs/source-copy/en-source.json` rows describe settings that no longer exist. Retire
   them through a source-copy request, the way the retired article entries were handled,
   once their values live on the entries (§6).

## 6. Translation plan (source-copy handoff)

Today the NL and FR of the card texts are **template-setting translations**, planned per
block setting in the localization batches and written by `docs/localization/registration/register.py`
as theme JSON template resources. Once `cards` is set, the storefront prints the entries,
and the entries are translated on the **metaobject resource**: Translate & Adapt → Content →
Metaobjects → Research card → entry → NL / FR, or `register.py`'s field route (`METAOBJECT`,
one binding per `gid|field` in `registration/bindings-fields.json`, WAVE2B-PLAN.md). The
block translations keep working for as long as the blocks render, and stop mattering at the
switch.

What moves, per entry (`TRANSLATIONS.md` has every value with its status, generated by
`docs/research-metaobjects/handoff.py`):

| Field | Translate? | Note |
|---|---|---|
| `subheading`, `subtext`, `result_label`, `result_text`, `method_label`, `method_text`, `image_badge` | yes | plain text, same values as the batch |
| `heading` | yes | rich text: the translation is the same JSON tree with translated `value` leaves. Translate & Adapt does that in its editor; `register.py`'s `translate_json` handles rich text leaves (WAVE2B §"What counts as text") |
| `link_label` | **no** | authors · year · journal; `held` / never-translate in both batches |
| `link_url`, `logo`, `image` | n/a | URL and files are not translatable resources |

Statuses to carry over unchanged (per language: 30 `translated`, 10 `pending-claim-review`
in NL on the five headings and the five result texts, where the EN claims wait for
CLAIMS-REVIEW sign-off, 5 `held` link labels; FR 40 `translated`, 5 `held`). The NL
RESULTAAT row also carries the batch flag `fit-risk` (9 characters against 6). The PDP batch
carried one different FR value (Alli's `image_badge` with a hyphen); the homepage value is
the one to use. Entities in the batch values are content, not spelling: the entry fields
are plain text that the theme escapes, so a `&nbsp;` copied literally would show as
`&nbsp;` on screen. Type the character (or drop the trailing one, as the entry already does)
and write `&` as `&`.

The handoff, in order:

1. The source-copy lane adds the `research_card` family (entries `kulal-2016`, `lei-hu-2025`,
   `janakiram-2017`, `vano-2018`, `alli-2019`) to `plan-nl.json` / `plan-fr.json` as
   `METAOBJECT` rows keyed by entry GID and field key, EN sha1 from the entry's field value,
   carrying the batch statuses. The Janakiram `image_badge` gets its EN from the corrected
   entry (§4), not from the batch.
2. `register.py` dry run proposes the field bindings (`live/fields-proposed-<lang>.json`);
   review into `bindings-fields.json`.
3. Victor writes (as on 22 Oct) or the runner writes with his go.
4. Check `/nl` and `/fr` on the homepage and PDP: card texts, the rich text heading, the
   badge. The EN link labels must stay EN.

Until step 3 is done, the switched-over section shows the **EN** card texts on `/nl` and
`/fr`. So: either register the entry translations before the switch (steps 1 to 3 run on
Draft entries too; the translation resource does not need the entry Active), or accept the
gap for a release. Recommended: before.

## 7. Optional: a card usable anywhere (proposal, not built)

- **Already possible, built by R67.** Add the Research Behind System section to any
  template, pick the entries. Marquee, slider or grid, Day and Night, surface setting: all
  shared. This answers "used everywhere" without new code.
- **A single "Research card" block inside other sections** (buy box, article, FAQ) would
  need a `metaobject` (single) block setting in each host section's schema, that host
  loading `section-research-behind-system.css`, and a width rule per host (the card is 380
  or 780 px and sized by the marquee/grid CSS). One host is a small change; "any section" is
  a theme-blocks architecture this Dawn-based theme does not have. Build it when a concrete
  placement is decided.
- **A standalone one-card section**: trivial but a duplicate of the section with one entry.
  Not proposed.

## 8. Rollback

| Situation | Rollback |
|---|---|
| Cards look wrong after the switch, blocks still in the templates | Set `"cards": []` (or delete the key) in the template, or clear the picker in the theme editor. The blocks render again, byte-identical to b0bb4fb (§9, the raw-byte gate: absent, null, empty string and empty list all proven). |
| After the blocks were removed (§5.1) | `git revert` the removal commit (the blocks return), then clear `cards`. |
| One card must disappear | Edit the `cards` array (or the picker). Setting the entry to Draft also removes it from the storefront, but the behaviour of a list with a hidden member was not tested; prefer the array. |
| The theme code itself | `git revert` the R67 commit. A `cards` key left in a template is then an unknown setting and is ignored. |

## 9. Test record (24 Oct 2026)

Theme Check: `shopify theme check --fail-level error` exit 0, 0 errors, 19 warnings (the
baseline; none in the changed files).

**Liquid identity** (`docs/research-metaobjects/fixture/render.mjs`, liquidjs with the
Shopify filters stubbed; `out/liquid-results.txt`): 63 PASS, 0 FAIL (R67b rerun).

- **Raw bytes, the R67-B1 gate**: the real five-card homepage and PDP sections, rendered by
  the new section and snippet with the setting absent, null, an empty string and an empty
  list, equal the b0bb4fb render byte for byte, no decoding and no whitespace normalisation
  (homepage 13,231 bytes, SHA-256 `8e6a08d5…`; PDP 12,871 bytes, SHA-256 `9ee3f82d…`, the
  same hashes Astra's review measured for the baseline). The same holds for the grid/slider
  and the plain-grid layouts. Astra's own reproduction script reports `equal: true` for both;
- new section + snippet with the six-card fixture set == old section + snippet at b0bb4fb,
  for the homepage marquee, the PDP marquee and a grid/slider variant;
- cards from stubbed `research_card` entries == cards from blocks, same three variants,
  after decoding entities (the only difference is `&amp;` for `&` and the like);
- an empty `cards` setting renders the blocks;
- a sixth fixture card with `#` URL and no image prints the plain label and no image
  wrapper; five `target="_blank" rel="noopener"` study links; a multi-line entry field prints
  `<br>` between its lines; an empty entry field prints no element;
- the rich text walker: bold, italic, link with `&` in the URL and title, two paragraphs
  joined with `<br>`, a list, the multi-line fallback, a missing field;
- **Rich text links, the R67-B2 gate**: an `<a>` for `https`, upper-case `HTTP`, a URL with
  surrounding whitespace, `mailto`, `tel`, root-relative (also with a colon in the query),
  anchor, query, dot-relative and bare relative URLs; escaped `href` and `title`, `target`
  only as `_blank` with `rel="noopener"` (another target value is dropped). Text without a
  link for `javascript:` plain, mixed case, with leading whitespace, with a tab, a newline or
  a null byte inside the scheme name, with a leading control character, for `data:` (two
  spellings), `vbscript:`, `file:`, `ftp:`, an empty, whitespace-only or missing URL. An
  entity-spelled `javascript&colon;` stays a harmless relative path because the `&` is
  escaped.

**Browser** (`out/frame-1440.html` and `out/frame-390.html`, Day and `?mode=night`, in
Orca's isolated browser profile; the blocks and the entries side by side for the marquee
and for the grid/slider, a sixth card with `#` URL and no image in both). Every check PASS
in all four runs; the fixture's own report lines, condensed:

| Check | 1440 Day | 1440 Night | 390 Day | 390 Night |
|---|---|---|---|---|
| DOM of the entries' cards == DOM of the blocks' cards (browser-serialised, originals only), marquee and grid | PASS | PASS | PASS | PASS |
| Card sizes equal, marquee | 780×482 ×5, 380×482 | same | 320×666 ×6 | same |
| Card sizes equal, grid/slider | 592×558 ×6 | same | 298×694 ×6 | same |
| Colours equal (card, text, source chip, detail) | white, #191f38, #dddbd9, 0.76 | #212a49, #fffbf6, #2c3a60, 0.68 | as 1440 Day | as 1440 Night |
| Wide (image) cards 5 vs 5; `slider__slide` 0 vs 0 (marquee), 6 vs 6 (grid) | PASS | PASS | PASS | PASS |
| Five study links `target="_blank" rel="noopener"` with "Opens in a new window." (5/5 each side); one plain label for `#` (1/1) | PASS | PASS | PASS | PASS |
| Both marquees `is-running`, 6 clones each, the track moved in 600 ms, no reduced-motion | PASS | PASS | PASS | PASS |
| Keyboard order: 5 tabbable study links in the originals, 6/6 clones `aria-hidden`, clone links `tabindex="-1"` | PASS | PASS | PASS | PASS |

Keyboard focus on the entries' marquee (`out/fixture.html` at the browser's own width, the
document focused by a click, then `fxFocusPrep()`, a real Tab key, `fxFocusCheck()`): Tab
reached the third card's link, `:focus-visible` true, the band glided the card into view
and held still. PASS. (Without document focus the ring does not show and `reveal()` keeps
the band where it is, by design in `assets/kc-marquee.js`.)

Screenshots of the four runs, scrolled to the marquee pair and to the grid pair, are in the
lane's scratchpad (`shots/<width>-<mode>-<pair>.png`), not in the repo.

R67b re-run (same four frames, after the rework): every DOM, size, colour, wide-card,
study-link, plain-label, `slider__slide` and clone/tab-order check PASS again. The one
check that could not execute was the marquee drift: the browser pane had stopped painting
(0 `requestAnimationFrame` frames in 500 ms, the display asleep or the pane occluded), so
no band moved and the IntersectionObserver never started the loop. `assets/kc-marquee.js`
is untouched by R67 and R67b, the card DOM is unchanged since the passing run above, and
the block path is byte-identical to b0bb4fb, so the earlier drift and keyboard results
stand; re-run `out/frame-1440.html` on a lit screen to see it move.
