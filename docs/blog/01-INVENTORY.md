# Blog lane · 01 · Inventory and current state

Blog lane, branch `karmicare/soft-launch-blog` from `karmicare/soft-launch` @ ee00446. Audit run on 26 Oct 2026 against the live store (`www.karmicare.com`, theme `karmicare/main`, id 187295564157, role main), read in an isolated Orca browser profile with no login. The pages were fetched from inside that tab (same origin), and no bot check appeared. Nothing was written to the store.

## 1. What exists

| | |
|---|---|
| Blogs | **One**: `news`, title "News". The sitemap lists `/blogs/news`, `/nl/blogs/news` and `/fr/blogs/news`, and no other blog. |
| Articles | **8**, all in `news`. |
| Index pagination | 6 per page (`main-blog` paginates by 6), so page 1 shows 6 and `?page=2` shows 2. |
| Template | `templates/article.json` (featured image, title with date and no author, share, content) and `templates/blog.json` (`main-blog`, layout "collage", medium image height, date on, author off). |
| `featured-blog` section | **Not used.** No template or section group places it; `featured-blog` only appears in the schema locale files. |
| KC tokens in the blog files | **Zero.** `main-article`, `main-blog`, `article-card` and the three blog CSS files are stock Dawn. |
| Comments | No comment block in the template. The comment form in `main-article.liquid` renders only if the blog has comments switched on in Admin. |

## 2. Per article

Words are the article body only. Heading counts are inside the body; the page also prints its own `h1` title. "Thumb" means the RTE image is a legacy `_480x480` or `_600x600` size from the Shopify file URL. The originals are larger (checked: `charcoal-toothbrushes.jpg` 1200×802, `Untitled_image_2.jpg` 1920×1080).

| Article (handle) | Published | Words | Body headings | Body images | Featured image | Lists | Quotes | Study links | Other links |
|---|---|---|---|---|---|---|---|---|---|
| `nano-hydroxyapatite` | 21 Dec 2023 | 2,985 | **5 × h1**, 5 × h2, 1 × h3 | 4 thumbs, 600 px wide (1.50, 1.50, 1.78, 1.61), alt filled | **520×416** (1.25) | 4 ul, 16 li | 3 | 3 (PMC, ScienceDirect, PubMed) | 4 internal (old paths), 1 cda.org PDF |
| `benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood` | 25 Oct 2024 | 1,961 | 5 × h2, 8 × h3 | 2 thumbs, 480 px (16:9), alt empty | 1920×1080 | 7 ul, 27 li | 0 | 14 | 5 internal, 7 consumer sites (Healthline, WebMD, Forbes, …) |
| `how-oral-health-impacts-your-overall-wellness` | 25 Oct 2024 | 1,647 | 5 × h2, **1 × h5** | 2 thumbs, 480 px, alt empty | 1920×1080 | 8 ul, 28 li | 0 | 4 | 8 internal, 5 org/news sites |
| `3-reasons-why-you-should-look-for-an-sls-free-toothpaste` | 25 Oct 2024 | 1,293 | 2 × h2, 5 × h3 | 2 thumbs, 480 px, alt empty | 1920×1080 | 3 ul, 8 li | 0 | 3 | 4 internal |
| `5-reasons-you-should-avoid-fluoride-in-toothpaste` | 25 Oct 2024 | 1,132 | 4 × h2, 7 × h3 | 2 thumbs, 480 px, alt empty | 1920×1080 | 5 ul, 18 li | 0 | 7 | 7 internal, 5 other |
| `headaches-and-tooth-pain-understanding-the-connection` | 25 Oct 2024 | 1,104 | 5 × h2, 4 × h3 | 1 thumb, 480 px, alt empty | 1920×1080 | 4 ul, 19 li | 0 | 1 | 9 internal, Wikipedia, a dental practice |
| `top-natural-whitening-toothpaste-for-a-brighter-smile` | 25 Oct 2024 | 896 | 6 × h2, 6 × h3 | 1 thumb, 480 px, alt empty | 1920×1080 | 2 ul, 16 li | 1 (used as a shop link) | 4 | 9 internal |
| `morning-and-night-time-brushing-why-timing-matters` | 25 Oct 2024 | 756 | 2 × h2, 8 × h3 | 2 thumbs, 480 px, alt empty | 1920×1080 | 6 ul, 6 li | 0 | 0 | 1 internal |

Seven of the eight were published on 25 Oct 2024 within eight minutes of each other (a bulk import), so the index shows the same date on almost every card.

**Not present in any article:** tables, ordered lists, embedded video or iframes, `figure`/`figcaption`, footnotes or `sup`. The layout still styles tables (scrolling in their own box on phones) and ordered lists, so a future article cannot break it.

## 3. Languages

`/nl/…` and `/fr/…` answer 200 for the index and all eight articles, with `lang="nl"` and `lang="fr"` on the page. **Every title, excerpt and body is still the English text** (same word counts, same headings). No article content is translated yet. That is store content and belongs to source-copy. For the layout it means one thing: a reader on `/nl` gets Dutch UI labels around an English article, and a screen reader reads that English body with a Dutch voice. A `lang` attribute on the body wrapper (from the article's own language) would fix the second part, so it is on the decision list in 02-PROPOSAL.

## 4. What the layout has to cope with

1. **Inline styles from the editor.** The 2024 articles carry hundreds of `style` attributes pasted in with the text. They set font sizes on headings (`font-size: 18px`, `20px`), link colours (`#004aad`, `#333399`), margins on every `p`, `li` and heading, `font-weight: 400` on spans, and centred image paragraphs. Without an override they beat any token we set. The nano article has two `div style="width: 90%"` wrappers. Counts: nootropics 164, fluoride 102, wellness 83, whitening 76, SLS 72, headaches 64, morning 48, nano 3.
2. **Heading levels are wrong in places.** The nano article uses `h1` for five body headings, the wellness article jumps to an `h5`, and two articles go straight from the title to `h3`. The layout should size headings by their place in the article, not by tag alone. The heading order itself only gets fixed in the body (source-copy or Admin).
3. **Images are small and have no size.** The body images are 480 or 600 px thumbnails without `width`/`height`, so they push the text down when they load (layout shift) and blur if stretched. Their source is in the body HTML, which we do not edit, so the layout has to show them at most at their natural width, or reserve space for them.
4. **The nano featured image is 520×416.** The current template stretches it across the page (about 1,200 px at desktop), and it reads soft and washed out (`docs/blog/shots/00-live-article-desktop-top.png`). The other seven are 1920×1080 and can carry a large hero.
5. **`<br>` instead of paragraphs.** The headaches article has 19 `br` and only 19 `p`, and the nano article has 13 `br`.
6. **Blockquotes are used for three different things.** In the nano article they hold a founder quote with a name, a first-person story, and a saying. In the whitening article a blockquote holds a shop link.
7. **"Key takeaways" and "Self reflection" blocks.** Five articles open with a "Self Reflection" question list and/or "Key takeaways", as plain paragraphs and lists. They look like a summary box, but they are body text, so the layout can only style them if it recognises them. That stays a manual choice (decision list).
8. **Long article.** The nano article is about 15 minutes of reading (2,985 words). That is where a table of contents earns its place. The shortest article is 756 words (about 4 minutes).

## 5. Links that no longer work

The bodies link to paths from the old Webflow site. Checked on the live store on 26 Oct:

| Path in the body | Result |
|---|---|
| `/en/product/biorhythmic-oral-care-duo` (nano article, the Duo link) | **404** |
| `/en/why-stop-using-fluoride-toothpaste` | **404** |
| `/en/why-use-hydroxyapatite-toothpaste` | **404** |
| `/en/articles/benefits-of-nootropics`, `/en/articles/nano-hydroxyapatite`, `/en/articles/sls-free-toothpaste`, `/en/article/nano-hydroxyapatite` | **404** |
| `/en/product/biorhythmic-oral-hygiene-set` | 200, redirects to `/products/karmicare-biorhythmic-oral-care-system` |
| `/en/product/morning-toothbrush` | 200, redirects to `/products/morning-toothbrush-2-0` |
| `/en/product/whitening-charcoal-dental-floss` | 200, redirects to `/products/whitening-charcoal-dental-floss` |
| `/en` | 200, redirects to `/` |

Seven of the eleven old paths are dead. The fix is either URL redirects in Admin (Online Store → Navigation → URL redirects) or relinking in the bodies. Both are outside this lane, so this goes to the landing desk.

## 6. Claim and brand notes for the evidence track

I do not edit article bodies. These are what I found while reading them, against the EU cosmetic claim rules and Victor's brand rules in the lane brief. A word search plus reading the hits, not a full legal review.

- **Guarana and valerian for focus, energy, calm and sleep** (banned): nootropics article throughout ("guarana … spark your mind to life", "valerian to enhance sleep quality", 26 guarana and 17 sleep mentions); wellness article ("guarana … enhancing mental clarity and focus", "valerian support relaxation and improve sleep quality", "boost energy and mental clarity"); whitening article ("Valerian: Soothing and Calming", "Guarana: Energizing"); nano article ("guarana helps jump start your day and valerian assists in winding down"); fluoride article (valerian for sleep).
- **"Prevents" claims** (banned): "nano hydroxyapatite can help prevent tooth decay" (nano); "strengthens enamel and prevents cavities" (morning); "Xylitol prevents cavities" (whitening, fluoride); "prevent gum disease" (wellness); "prevent gingivitis and periodontitis" (headaches); "preventing cavities and sensitivity" (whitening).
- **"Medical-grade"** (banned): "medical-grade activated charcoal" (morning).
- **Health effects beyond cosmetics**: the fluoride article says fluoride "impairs sleep quality", calcifies the pineal gland, and causes thyroid and neurotoxic effects, and calls fluoride "a harmful substance". The headaches article frames itself around "treating" pain.
- **Competitors named** (banned): SLS article names Colgate, Biotene and Sensodyne Pronamel.
- **Commodity and old names**: bodies use "Morning toothpaste" / "Evening toothpaste", "Biorhythmic Oral Hygiene Set", "Shop Our Bestselling …", and "product" many times. Awake and Asleep appear as names only in the nano article and its new meta description.
- **Founder quote and first-person story** in the nano article: real quote with a name, so it is kept as content. Its styling is a layout question (decision list).

Styling the blog makes these articles easier to read and more prominent. Whether some articles should be hidden or rewritten before the new layout goes live is a content decision for Victor and the evidence track, not for this lane.

## 7. Design system inputs found

- **Tokens:** `assets/kc-tokens.css` (generated). Day on `:root`/`body.day-mode`, Night on `body.night-mode`. Page `--kc-mapped-surface-page` (#fffbf6 / #191f38), accent `--kc-mapped-gradient-section-accent` (#f2f8ff / #2c3a60), the same values the brief names. Type ramp `--kc-responsive-*` (body-lg 18/26 → 20/28 from 750 px, h1 32/36 → 52/52). Fluid type (`kc-fluid.css`, `kc-fluid-wide.css`) loads only when the theme setting `kc_fluid_type` is on, and it is off in `config/settings_data.json`, so the previews use the stepped ramp and I check them with fluid on as well.
- **Surfaces:** `assets/kc-surface.css` + `snippets/kc-surface.liquid`. A section declares `data-kc-surface="page|accent|transition"` and the resolver writes its edges. Blog sections can join the chain the same way, with no new CSS for the gradients.
- **Long-form precedent:** `assets/kc-policy-page.css`. Title block page → accent, body accent → page, 720 px column (680 px text), clause titles at h5 size with a hairline above, 18 px body at 68 % of the heading colour from 750 px, underlined links in the full colour, print rules.
- **Research card:** `snippets/research-card.liquid` + `assets/section-research-behind-system.css`. White card (`surface-page-secondary`), radius-lg 20 px, hairline, uppercase Nunito subheading and labels, a pill-shaped source chip.
- **Buttons:** `snippets/button-styles.liquid`. `.karmicare__btn-primary` (navy by Day, light by Night) and `-secondary` (outline), radius 8 px (`--kc-shape-radius-sm`), **Nunito, uppercase, letter-spaced**.
- **Eyebrows:** `.kc-caption-subheading.subtitle-item`, **Nunito 700 uppercase**.
- **Navigation:** floating bar; the first section gets `--kc-navigation-clearance` as top padding (`kc-navigation.css`).

Two of Victor's rules in the lane brief do not match what the site does today: "Proxima Nova only" and "buttons in sentence case in the brand sans" against Nunito uppercase eyebrows, labels and buttons, and "no pills" against the research card's pill-shaped source chip. The previews show both ways, and 02-PROPOSAL puts it to Victor as a decision.

## 8. Earlier Figma concepts (input only)

KC | Shopify Store, page `3298:3`, section `WEB — News & Articles` (`3298:37`). Read with 6 Figma calls, nothing edited. Five concepts for the **index**, none for the article page: The Current Issue, Topic Rivers, The Research Notebook, The Living Index, and Choose Your Reading Journey. The finalist comparison (`3565:129450`) ranks Choose Your Reading Journey first (30.33/40) and marks it "Proposed final, awaiting Victor review". It is a guided hub: goal picker, a path of stops, topic cards with "Nothing published yet" states, a "How we publish" block and a newsletter. Most of its copy is new and was never approved, and with eight legacy articles most of its topic cards would be empty. What carries over: the `WEB/Article card` component (`3592:128276`): white card, hairline, small eyebrow, title, a "type · topic" meta line, an arrow, and an image variant with the accent tint behind a packshot.
