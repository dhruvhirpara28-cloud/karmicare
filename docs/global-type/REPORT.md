# TY-01 / G-7: bold in body copy renders Semibold 600

Worker report, 22 Oct 2026. Branch `karmicare/global-type` on `karmicare/soft-launch-global` 279389c,
merged with `karmicare/soft-launch` 1ca2168 (merge b13c957). Victor, 21 Oct: "ja body tekst naar 600".

## Change

| File | What | Before | After |
| --- | --- | --- | --- |
| `layout/theme.liquid:195` | `--font-body-weight-bold` | body weight + 300 = 700 | `var(--font-600-weight)` = 600 |
| `assets/base.css:354` | new rule: `b`/`strong` outside `h1`-`h6` and `.h0`-`.h6` | browser `bolder` (700 in 400 copy, 900 in 600 copy) | `var(--font-body-weight-bold)` = 600 |
| `config/settings_schema.json:243` | `body_font_weight` setting | present, read nowhere | removed |

Headings are excluded from the new rule, so `h2 strong` (`base.css:424`, h2 weight), the two-tone
`.kc-surface` rule (`base.css:431`) and Marlide at 300 are untouched. The rule has specificity (0,0,1):
every rule that sets its own weight on `b`/`strong` keeps winning.

`body_font_weight`: `git grep body_font_weight` matched only `config/settings_schema.json` and the gap
row; `config/settings_data.json` holds no value for it (not edited). `header_font_weight` is also read
nowhere, but `settings_data.json:27` holds 500, so it stays.

## Every reader of `--font-body-weight-bold` and every `b`/`strong` rule

| Reader | Before | After | Rendered on the checked pages |
| --- | --- | --- | --- |
| `assets/base.css:2969` `.font-body-bold` | 700 | 600 | no element uses the class on home, PDP, legal |
| `assets/component-cart-items.css:273` `.cart-disclosure-modal__title` | 700 | 600 | never: no theme cart (`layout/theme.liquid:459`) |
| `assets/component-cart-items.css:319` `.cart-disclosure-modal__item-title` | 700 | 600 | never: same |
| `assets/component-disclosures.css:59` `.disclosures-summary-item__open-title` | 700 | 600 | not on the checked pages |
| `assets/component-disclosures.css:130` `.disclosures-item__header span` | 700 | 600 | not on the checked pages |

Rules with their own weight, unchanged (`git grep -nE '(^|[ >])(b|strong)\s*[,{]'`):
`assets/kc-buybox.css:65` (700), `:802` (600), `:1040` (700), `:1050` (600);
`assets/product-compare-plans.css:1012` `.pc-foot strong, b` (700);
`assets/section-hero-karmicare.css:41` and `assets/section-trusted-professionals.css:68` (inherit);
`sections/legal-toc-section.liquid:299` `.legal-toc__body strong` (600);
`sections/hero-karmicare.liquid:31`, `sections/two-formulas-karmicare.liquid:35`,
`sections/trusted-professionals.liquid:41` and `legal-toc-section.liquid:57-64/94` set colour or
opacity only, and the first three sit inside headings.

## Rendered check

Preview theme `KC preview karmicare-global-type 0e7d4b38` #189947838845 (pushed by the global
coordinator from this worktree), hosted `https://karmicares.myshopify.com/?preview_theme_id=189947838845`,
Orca built-in browser, isolated anonymous profile `global-type-anon-20261021`, no login, nothing typed.
The page's stamped `base.css?v=…3188` contains the new rule (checked by fetching it). "Before" is the
parent lane preview #189917069693 (same files minus this change). Computed `font-weight` per element,
grouped: body bold = `b`/`strong` outside headings; heading bold = inside headings.

| Page | `--font-body-weight-bold` before → after | Body bold before → after | Heading bold, headings, buttons |
| --- | --- | --- | --- |
| Home EN, Day and Night, 390 and 1440 | 700 → 600 | 18: 12×500 + 6×600 → same (all inside the buybox, own rules) | 3 at 500 in 500 headings → same; heading tallies identical; buttons 24 (2×400, 2×500, 3×600, 17×700) → same |
| PDP EN, Day, 390 and 1440 | 700 → 600 | buybox 26×600 + 11×700 → same (own rules); compare footer "Care Credit" 700 → same (`.pc-foot b`); featured product 5×600 + 1×500 → same; **Welcome Kit tooltip 4×`<b>` 900 → 600** (parent 600, no own rule) | 1 at 500/500 → same; headings identical; buttons 26 (6×400, 2×500, 4×600, 14×700) → same |
| Privacy EN, Day, 390 and 1440 | 700 → 600 | 65 in `.legal-toc__body` at 600 → same (own rule); **33 in `.legal-toc__blockbody` ("Data:", "Legal basis:", …) 700 → 600** in 400 copy, the body-copy case this change is for | none; headings identical; buttons 7 (1×400, 1×500, 3×600, 2×700) → same |
| Consumer rights EN (parent preview only) | 700 | 76, all in `.legal-toc__body` at 600 (own rule) | none |
| Home NL, PDP NL, Privacy NL | 600 | same tallies as EN | same as EN |
| Home FR, PDP FR, Privacy FR | 600 | same tallies as EN | same as EN |

Day/Night: the homepage was switched with the `.kc_night` control (`body.night-mode`); numbers identical.
The PDP and the legal pages have no Day/Night control, so they follow the clock (Day at capture time).
No `b`/`strong` rule depends on the mode.

Screenshots (Orca viewport 390×844 and 1440×900) in the session scratchpad
`/private/tmp/claude-501/-Users-iamvictorious-IdeaProjects-orca-workspaces-karmicare-shopify-theme-global-type/68e8e345-a287-4a5b-85cc-7a4e7406fcc9/scratchpad/`:
`home-en-day-390.png`, `home-en-day-1440.png`, `home-en-night-390.png`, `home-en-night-1440.png`,
`pdp-en-day-390.png` (gallery images not painted at that width), `pdp-en-day-1440.png`,
`privacy-en-day-390.png`, `privacy-en-day-1440.png`.

Cart drawer: not applicable. `layout/theme.liquid:459-462`: no theme cart, `/cart` redirects to the
checkout (observed: `/cart` landed on `/checkouts/cn/…`; left at once, nothing typed).

Theme Check: `shopify theme check --fail-level error` exit 0, 19 baseline warnings, 0 errors.
`config/settings_schema.json` parses (`python3 -I`).

## For Victor / the coordinator

1. PDP buybox lead-ins stay 700: "€5.90", "Run your tongue over your teeth:", "Before you start",
   "Awake:", "Asleep:", "The first week:", "Hormone-aware.", "Built on the body's rhythm.",
   "Oral–gut–brain axis" and the RDA table "Awake"/"Asleep" read `assets/kc-buybox.css:65-67`
   ("Bold is the strongest weight Figma uses"). If "body tekst" includes these, that one line moves to
   `var(--font-600-weight, 600)` (PDP lane).
2. Welcome Kit tooltip in the compare table (`sections/product-compare-plans.liquid:109/135`): the
   `<b>` parts drop from 900 (Black, browser bolder of the 600 label) to 600, the same weight as the
   label; the hierarchy is left to the 0.8-opacity second line and the struck price. If Bold is wanted:
   `.plan-compare--kc .pc-kit-poptitle b, .plan-compare--kc .pc-kit-itxt b { font-weight: var(--font-700-weight, 700); }`.
3. `header_font_weight` (`config/settings_schema.json:230`) is dead too but has a saved value.

## Notes

- The Orca runtime restarted during the FR pass (22 Oct 13:43, new socket `o-71600-ed81.sock`); every
  `orca` command failed with `runtime_access_denied` (EPERM) until the session sandbox picked up the
  new socket a few minutes later. The FR pass and the privacy "before" measurement were then completed.
- The anonymous profile's cart (one line added for the cart check) was emptied with `POST /cart/clear.js`.
- `docs/global/GAP-LIST.md` row TY-01 is the coordinator's; not edited here.
