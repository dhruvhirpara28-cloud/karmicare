# Homepage gap list (soft launch, A1)

## Status 22 Oct

One status per row. **In merchant-edit**: the theme change is in local `merchant-edit` 31407fb (checked with `git merge-base --is-ancestor <sha> merchant-edit`); merchant-edit is not pushed, so none of it is live yet. **Ready to land**: committed on `karmicare/soft-launch-homepage` and reported to the landing desk. The original 19 Oct scan follows below this block, unchanged.

| Status | Rows |
|---|---|
| In merchant-edit | 43 |
| Ready to land | 0 |
| In progress | 0 |
| Waiting for Victor | 5 |
| Parked / after launch | 30 |
| Dropped | 10 |
| **Total** | **88** (the 74 scan rows plus 14 later items) |

### Waiting for Victor

| Row | Question | Options | Advice |
|---|---|---|---|
| F1 · FAQ "Is Karmicare fluoride-free?" (hidden since 65ff2a8) | The answer reads "Karmicare is fluoride-free, and always will be. Fluoride's benefits don't outweigh its known drawbacks." Review R11 F1 calls the second sentence a blanket claim without support. | (a) keep only the first sentence and show the row; (b) keep both sentences and show the row; (c) keep the row hidden | (a): the first sentence is a fact about the formula and needs no evidence |
| F3 · FAQ "Why two formulas instead of one?" (visible, also live) | The answer ends "…so Asleep soothes, rebalances and remineralises while you sleep." Review R11 F3 calls "while you sleep" an overnight action claim without support. | (a) drop "while you sleep"; (b) Victor's own wording; (c) hide the row | (a): the smallest change that removes the claim |
| 0205 · FAQ "Can I combine Karmicare with fluoride toothpaste or rinses?" (hidden since 65ff2a8) | The answer is verbatim from the brand FAQ base (FAQ-0205): fluoride and nano-hydroxyapatite "compete for the same enamel surface". Has it been cleared clinically? | (a) cleared: show the row; (b) not yet: keep it hidden until checked | (b) until someone has checked the claim; (a) as soon as it is cleared |
| Clock help text (a11y, axe) | The clock knob points `aria-describedby` at `clock-help-…`, an element that no longer exists (it was dropped in bb6d231 "pull to main"). Home and PDP share the section. | (a) put the old screen-reader-only sentence back ("Drag the knob around the ring to preview a local time. Release to return to the current time. Hold an arrow key… Home selects midnight; End selects 23:59…"), with NL/FR translations; (b) drop the `aria-describedby`, so the slider keeps only its label and live value; (c) leave it (axe keeps flagging it) | (a): it is existing copy and tells keyboard users how the control works; agree with the PDP lane who builds it |
| PR-01 · professionals name holders at 393 | Headless Chrome showed the glass name holders blank on phones; the text is in the DOM. Probably a capture artefact, never checked on a real phone. | (a) Victor opens the homepage on his phone and confirms the names show: row closed; (b) they are blank: the homepage moves the `backdrop-filter` onto a `::before` | (a): a two-minute check |

### All rows

| Row | Status | Detail |
|---|---|---|
| AN-01 | In merchant-edit | global lane `3c03acb` (announcement one line on tablets) |
| HD-01 | In merchant-edit | global lane `3ea647a`, floating navigation (D-12) |
| HE-01 | In merchant-edit | `81e2edb`: D-1, Victor kept the photo; HQ kit (3936×2960) from Files |
| HE-02 | In merchant-edit | `1506cab` |
| HE-03 | In merchant-edit | `6664a71`: D-2, "WHY TWO FORMULAS?" jumps to the clock |
| HE-04 | In merchant-edit | `1506cab` |
| HE-05 | In merchant-edit | `d0c1130` (picture fills its wrapper, contained) and `81e2edb` (`sizes` 900px / 92vw) |
| HE-06 | Parked / after launch | P2; at 1440 the avatar still sits about 12 px above the switch |
| HE-07 | Parked / after launch | P2, not rechecked since 19 Oct |
| HE-08 | Parked / after launch | P2, not rechecked since 19 Oct |
| HE-09 | In merchant-edit | `f3d2391`: D-3, no badge below 750 |
| Hero/strip seams | In merchant-edit | `68527fc`: Victor 21 Oct; 120 px under the switch on desktop, 48-50 px on phones (Figma V15) |
| SS-01 | In merchant-edit | `37ab3bc`, then `f2f65d0` (D-14: one drifting, swipeable row at every width) |
| SS-02 | In merchant-edit | `37ab3bc`, superseded by `f2f65d0` |
| SS-03 | Parked / after launch | P2: hairlines still run the full width |
| SS-04 | Parked / after launch | utopia (type line heights) |
| R13 F2 / B-13 | In merchant-edit | `8def726` and `55e9db2`: the marquee is a focusable region, keys move it, no-JS scroll |
| R9 F3 | Dropped | Victor: no pause button on the stat strip |
| CL-01 | In merchant-edit | `b314fd8` |
| CL-02 | Dropped | D-4: keep as is |
| CL-03 | Dropped | D-5: keep as is |
| CL-04 | Parked / after launch | P2 setting |
| CL-05 | Parked / after launch | assets (orb files) |
| Clock callout headings | In merchant-edit | `419fbfc`: h4 → h3 (also on the PDP) |
| TF-01 | In merchant-edit | `39a00a8`, srcset to 1600 in `aca9611` (R11 F2) |
| TF-02 | In merchant-edit | `39a00a8` (size), `81e2edb` (the uncut duo with its shadow replaces the tight crop) |
| TF-03 | In merchant-edit | `39a00a8` |
| TF-04 | In merchant-edit | `39a00a8` |
| TF-05 | In merchant-edit | `39a00a8` |
| TF-06 | In merchant-edit | `42a913b`: Night dims the ring |
| TF-07 | Parked / after launch | utopia / global gutter |
| TF-08 | Parked / after launch | utopia |
| TF-09 | Parked / after launch | P2 |
| TF-10 | In merchant-edit | `39a00a8` |
| B-08 | In merchant-edit | `92a6a4d`: "SEE WHAT'S INSIDE" shows Coming soon (rule H8) |
| BE-01 | In merchant-edit | `6860d74` |
| BE-02 | Dropped | live follows the approved card component |
| BE-03 | Parked / after launch | the pictures are off since `59db4e2` until proper images exist |
| BE-04 | Parked / after launch | no gain while the pictures are off |
| BE-05 | Parked / after launch | source-copy: card 07 still has the U+2028 line separator |
| BE-06 | Parked / after launch | utopia |
| Benefit images off | In merchant-edit | `59db4e2`: Victor 21 Oct, section switch off, the nine images stay set |
| Benefit card headings | In merchant-edit | `419fbfc`: h5 → h3 |
| R19-01 | In merchant-edit | `add1429`: the card titles inherit their letter spacing again (merchant-edit `2ef9b5c`) |
| PR-01 | Waiting for Victor | phone check, see above |
| PR-02 | Dropped | D-6: keep the marquee |
| PR-03 | In merchant-edit | `4f8024c` |
| PR-04 | Parked / after launch | P2 |
| PR-05 | Dropped | D-6: accept the 2560 repeat |
| PR-06 | Parked / after launch | assets (portraits) |
| RE-01 | In merchant-edit | `bf5d314`, `eefb0a9` |
| RE-02 | In merchant-edit | `4f8024c` |
| RE-03 | Parked / after launch | assets |
| RE-04 | Parked / after launch | assets |
| RE-05 | Parked / after launch | D-9: Victor updates the research cards in his own branch |
| RE-06 | Parked / after launch | P2 |
| RE-07 | Parked / after launch | utopia |
| CC-01 | In merchant-edit | `7ff0562`, reversed by `6dcf6aa` (H-2: 01/02/03 back, as in Figma) |
| CC-02 | Dropped | D-10: keep as is |
| CC-03 | Dropped | D-10: keep as is |
| CC-04 | Parked / after launch | source-copy: the eyebrow reads "Return on Care" now; the step titles were not rechecked |
| CC-05 | Parked / after launch | P2 |
| FQ-01 | In merchant-edit | `17e5247`, `9dbafdf`, `6c5ae47`, `65ff2a8`: answers from the brand FAQ base; two rows held, see F1 and 0205 |
| FQ-02 | In merchant-edit | `174997e`, `2aa89c0` |
| FQ-03 | In merchant-edit | `706d597`: FAQ cards on the research card surface token (the colour setting is empty) |
| FQ-04 | In merchant-edit | `d7232f7`: Victor wants pills in Nunito capitals (reverses `37ead46`) |
| FQ-05 | Parked / after launch | utopia |
| F1 | Waiting for Victor | see above |
| F3 | Waiting for Victor | see above |
| 0205 | Waiting for Victor | see above |
| FP-01 | In merchant-edit | `2124ebb` |
| FP-02 | In merchant-edit | `2124ebb` |
| FP-03 | In merchant-edit | `2124ebb` |
| FP-04 | In merchant-edit | `2124ebb` |
| FP-05 | Parked / after launch | assets |
| FP-06 | Dropped | D-13: keep |
| FP-07 | Parked / after launch | assets |
| FP-08 | Parked / after launch | source-copy |
| End-CTA icon alt | In merchant-edit | `984ba8a`: decorative icons `alt=""` (also the PDP) |
| FT-01 | In merchant-edit | `82a0a51` |
| FT-02 | Parked / after launch | P2; the footer belongs to the global lane now |
| FT-03 | In merchant-edit | global lane `95b56d6` (mono payment icons) |
| FT-04 | In merchant-edit | global lane `95b56d6` (Shopify flags, no `flagcdn.com`) |
| FT-05 | Parked / after launch | utopia |
| GL-01 | Dropped | expected consent behaviour |
| GL-02 | Parked / after launch | source-copy |
| R9 F2 | In merchant-edit | `ab34477`: in-page glide only for section anchors |
| Clock help text | Waiting for Victor | see above |

Not counted (other owners): bold body text renders 700 against the library's Semibold 600, forwarded to the global lane on 21 Oct. The live `templates/index.json` reconcile is closed: `origin/main` has no index.json change after `8596548`, which this branch already contains, so there are no live editor edits to keep.

**Changelog**
- 22 Oct: status block added (42 in merchant-edit, 1 ready to land, 5 waiting for Victor, 30 parked, 10 dropped).
- 22 Oct, later: R19-01 (`add1429`) is in merchant-edit `2ef9b5c`; now 43 in merchant-edit, 0 ready to land.

**Scanned**: 19 October 2026, live homepage `https://karmicares.myshopify.com/` (theme `karmicare/main` 187295564157, assets equal to branch base `3bae259` after Shopify minification), with the merged benefit hover state (6aa0e71) served in place of the live file and its veil emulated.
**Viewports**: 393 (phone, DPR 3, touch), 768 (tablet, DPR 2, touch), 1024 (DPR 2), 1440 (DPR 2), 1920 and 2560 (DPR 1). Day and Night forced through the theme's `.kc_day` / `.kc_night` switch.
**References**: Figma KC | Shopify Store `3rOMJvQZTzyYjnCV6oggV3`, Homepage V15 Day `2928:19880` and Night `2590:9728` (1440), mobile `3027:20792` (393, Day). Care-comes-back has no V15 band; its reference is `4013:29078` (earlier Day frame). No Figma exists for 768, 1024, 1920 or 2560: those are judged against the 1440/393 intent (gutters, container, no clipping, balanced alignment, sensible max widths). Brief = `.coordinator/source/45-HOMEPAGE-LAUNCH.md` plus COMMON-RULES §3.
**Evidence**: `docs/homepage/shots/<section>-<vw>-<mode>-before.png` (live), `docs/homepage/shots/figma/<section>-<vw>-<mode>-figma.png`, full-page overviews `page-<vw>-<mode>-before.png`. Binaries are gitignored; regenerate with the capture notes in REPORT.md.
**Method**: headless Chrome per viewport, per-section clips and layout metrics (content extent, overflow, clipped boxes, smallest text, tap targets, image pixels needed vs served). Five section reviews compared every capture with Figma and the code; I checked the high-impact rows myself (FP-01, PR-01, TF-01, FQ-05, the empty links).

**Result**: 74 rows across all ten sections plus announcement, header and footer. There is no horizontal page overflow at any width, and the header nav pill is correct and centred at every width.
- **Priorities**: 5 P0, 34 P1 (one of them, HD-01, still needs a scrolled capture) and 34 P2. A sixth P0 row, PR-01, is suspected and needs a device check.
- **Status**: 21 rows fixed on this branch, 15 decision rows (14 decisions), 21 handoffs and 2 pending a check. 13 homepage rows are left open: 12 P2, plus TF-06 (P1), whose opacity has to be tuned on a rendered page.
- **P0 detail**: FP-01 and RE-01 are fixed. PR-03 and RE-02 (dead CTA links) show the shared "Coming soon" state since A1b (`4f8024c`, Victor's rule H8). FQ-01 (FAQ answers) is copy.

Priority: **P0** broken, clipped, unreadable or unusable · **P1** visibly off-design · **P2** refinement.
Owner: **homepage** (this task) · **utopia** (type tokens and type sizes) · **source-copy** (text) · **assets** (image files) · **Victor** (decision) · **handoff** (another code owner).
Status column: *fixed `hash`* = homepage fix on this branch (rendered after-shots pending the browser route, Liquid parts pending the preview gate; see REPORT.md) · *open* = homepage P2 not done in this pass · *decision* · *handoff* · *pending* (needs a browser or device check first).

## Announcement bar and header

| ID | Section | Viewport · mode | Observed problem (evidence) | Reference | Prio | Owner | Status | Acceptance shot |
|---|---|---|---|---|---|---|---|---|
| AN-01 | announcement | 768 · both | The bar is 39 px tall at 768. The ≥990 rule (28 px) and the <750 rule (30 px) both miss tablets, so Dawn's default applies (`announcement-768-day-before.png`, metrics). | `3027:20793`, `2928:19882` | P1 | handoff (`sections/announcement-bar.liquid` L52: `min-width: 990px` → `750px`) | handoff | announcement-768-day-after.png |
| HD-01 | header | scrolled · both | `.section-header` is always `position: sticky` (`sections/header.liquid` L40-45) although `sticky_header_type` is `none`; its band is opaque (L373-384). On cream sections a blue strip probably shows behind the glass pill. Not captured: every capture is at scroll 0. | `2928:19881` | P1? | Victor | pending (scrolled capture), then decision D-12 | header-1440-day-after.png (scrolled) |

The nav pill itself matches Figma at every width: centred (gaps 162/370/610/930 px at 1024/1440/1920/2560), 12 px from the edges at 393 and 768, about 48 px tall, band colour equal to the top of the hero in both modes.

## Hero (`hero-karmicare`)

| ID | Section | Viewport · mode | Observed problem (evidence) | Reference | Prio | Owner | Status | Acceptance shot |
|---|---|---|---|---|---|---|---|---|
| HE-01 | hero | all · both | The hero shows the product still `KARMICARE_Hero-shot_001-p-1.png` (682 px wide, needs 1089-1364 px on phones and retina laptops). COMMON-RULES §3 says the homepage hero is the AM/PM animation; `hero-karmicare` only has an image block. Changing what the hero shows is a decision. | COMMON-RULES §3; `2928:19884` | P1 | Victor | decision D-1 | hero-1440-day-after.png |
| HE-02 | hero | all · both | The "Backed by health professionals" badge links to `#shopify-section-template--27582179377533__trusted_professionals_HAqYth` (`templates/index.json` L58); the live section id is `…27120739549565__…`, so the click goes nowhere. | `2928:19884` | P1 | homepage | fixed `1506cab` | hero-1440-day-after.png |
| HE-03 | hero | all · both | "WHY TWO FORMULAS?" has an empty `button_link_2`: it renders `href="#"` with `aria-disabled` but looks like an active button. | `2928:19884`; brief §2 secondary CTA | P1 | Victor (destination) | decision D-2 | hero-1440-day-after.png |
| HE-04 | hero | 393-1440 · both | The badge avatar is served as a 56 px file (`image_tag width: 56` caps the srcset) but shows at 56×72 and needs 112-168 px; the source is 332×479. Soft on every phone and retina screen. | `2928:19884` | P1 | homepage | fixed `1506cab` | hero-393-day-after.png |
| HE-05 | hero | all · both | Displayed image width follows the file's own width (682 px, no CSS width) while `sizes` says 840 px. A higher-resolution export would grow the picture and break the layout, so assets cannot swap it safely yet. | — | P2 | homepage | open (prerequisite for an assets swap) | hero-1440-day-after.png |
| HE-06 | hero | ≥990 · both | The badge sits about 8 px high against the Day/Night switch (avatar top 14 px above it; Figma 6 px). | `2928:19884` | P2 | homepage | open | hero-1440-day-after.png |
| HE-07 | hero | 768-1920 · both | The subtext breaks inside "24-/hour" because the text column is 640 px; the Figma line is about 668 px. | `2928:19884` | P2 | homepage | open | hero-1440-day-after.png |
| HE-08 | hero | 393 · both | Heading sits about 19 px lower than Figma (`padding_top_mobile` 45). | `3027:20795` | P2 | homepage (setting) | open | hero-393-day-after.png |
| HE-09 | hero | 393, 768 · both | The badge shows under the switch on phones and tablets; Figma mobile has no badge. | `3027:20795` | P2 | Victor | decision D-3 | hero-393-day-after.png |

Not a gap: the hero content extent (left 32 / right 270 at 1440) is the badge at the page gutter plus the centred 900 px heading column, as in Figma; at 1920/2560 the badge stays on the same left edge as the stat strip and footer.

## Stat strip (`stat-strip-karmicare`)

| ID | Section | Viewport · mode | Observed problem (evidence) | Reference | Prio | Owner | Status | Acceptance shot |
|---|---|---|---|---|---|---|---|---|
| SS-01 | stat-strip | 393 · both | Fixed 180 px items show exactly two stats with no third peeking in, and the scroller stops at the 15 px gutter. Figma uses content-width items with "Clinically backed" peeking in at x≈306, running to the screen edge (`stat-strip-393-day-before.png` vs `stat-strip-393-day-figma.png`). | `3027:20817` | P1 | homepage | fixed `37ab3bc` (swipe with peek; auto-scroll is decision D-14) | stat-strip-393-day-after.png |
| SS-02 | stat-strip | 990-1199 · both | Five 172 px columns: three labels wrap and, because items are centred vertically, the values sit at different heights (`stat-strip-1024-day-before.png`). | design intent | P1 | homepage | fixed `37ab3bc` | stat-strip-1024-day-after.png |
| SS-03 | stat-strip | ≥990 · both | Top and bottom hairlines run the full border box; Figma insets them to the content width (32-1408 at 1440). | `2928:19908` | P2 | homepage | open | stat-strip-1440-day-after.png |
| SS-04 | stat-strip | all · both | Strip is 235 px tall against 216 px in Figma, from label line heights. | `2928:19908` | P2 | utopia | handoff | — |

## 24-hour clock (`chronobiology-clock-karmicare`, also on the PDP)

| ID | Section | Viewport · mode | Observed problem (evidence) | Reference | Prio | Owner | Status | Acceptance shot |
|---|---|---|---|---|---|---|---|---|
| CL-01 | clock | 768, 1024 · both | When a callout badge fits on one line it keeps `min-height: 40px` plus a 40 px bottom margin: an empty band of about 64 px between badge and title (`clock-1024-day-before.png`, `clock-768-day-before.png`). Same on the PDP. | `3027:20840` (badge→title ≈24 px) | P1 | homepage | fixed `b314fd8` | clock-768-day-after.png, clock-1024-night-after.png |
| CL-02 | clock | 1440-2560 · day | Evening leader 120 px, callout at x=972; the Day V15 frame has a 58 px leader at x=895, while the Night frame matches live. | `2928:19943` vs `2590:9791` | P2 | Victor | decision D-4 | clock-1440-day-after.png |
| CL-03 | clock | ≥750 · both | "Drag the ring" hint is a fully rounded pill; present in the Night frame, absent in the Day frame. Brand rule: no pill buttons. | COMMON-RULES §3 | P2 | Victor | decision D-5 | clock-1440-day-after.png |
| CL-04 | clock | all · both | The readout uses label-lg (283 px wide); both 1440 frames are label-sm (249 px). The PDP already sets `time_label_size: small`. | `2928:19943`, `2590:9791` | P2 | homepage (setting) | open | clock-1440-night-after.png |
| CL-05 | clock | 393-1440 | `orb-blue.webp` / `orb-white.webp` are 880 px; 1123-1293 px needed. | — | P2 | assets | handoff | — |

Not gaps: the `div.timeline` overflow at 393 is the planned crop of the rotated orb's transparent corners (nothing visible is cut), and the 9.8 px AWAKE/ASLEEP labels are Figma's 70 % mobile scale, decorative and aria-hidden.

## Two formulas (`two-formulas-karmicare`, homepage only)

| ID | Section | Viewport · mode | Observed problem (evidence) | Reference | Prio | Owner | Status | Acceptance shot |
|---|---|---|---|---|---|---|---|---|
| TF-01 | two-formulas | 393-1440 · both | The tubes are served as a 220 px file for a 220 px slot on DPR 2-3 screens: `image_url: width: 220` (L126) caps the srcset although the source is 518×1057 px. Soft on every phone and retina screen. | — | P1 | homepage | fixed `39a00a8` | two-formulas-393-day-after.png |
| TF-02 | two-formulas | ≥990 · both | Tubes render 220×449; Figma 1440 ≈260×528. The file is cropped tight so its shadow ends in hard edges. | `2928:20020`, `2590:9868` | P1 | homepage (size) + assets (crop) | fixed `39a00a8` (size); crop handoff | two-formulas-1440-day-after.png |
| TF-03 | two-formulas | ≥990 · both | "SEE WHAT'S INSIDE" buttons stretch to the column (325 px); Figma buttons fit the label (≈204 px). | `2928:20020` | P1 | homepage | fixed `39a00a8` | two-formulas-1440-night-after.png |
| TF-04 | two-formulas | ≥1200 · both | Text columns at x 190-515 and 925-1250; Figma 148-478 and 960-1290. | `2928:20020` | P1 | homepage | fixed `39a00a8` | two-formulas-1440-day-after.png |
| TF-05 | two-formulas | 990-1199 · both | Left H3 wraps to 3 lines in a 275 px column; headings and buttons sit 20 px apart in height (`two-formulas-1024-day-before.png`). | design intent | P1 | homepage | fixed `39a00a8` | two-formulas-1024-day-after.png |
| TF-06 | two-formulas | 1024-2560 · night | Clock-ring ticks are bright white; the Night frame shows them faint. | `2590:9868` | P1 | homepage | open: the setting-driven background image has to move to a `::before` with a Night opacity (~0.35). The value needs tuning against `2590:9868` on a rendered page, which waits for the browser route | two-formulas-1440-night-after.png |
| TF-07 | two-formulas | 393, 768 · both | 15 px gutters; Figma and the clock above use 20 px. Not section-specific: Dawn's `--page-gutter` is 1.5rem on phones for most sections (hero, stat strip, benefits, FAQ, featured product all measure 15 px), while the clock and footer use the 20 px `--kc-responsive-spacing-page-gutter`. One global gutter value is a token decision. | `3027:20922` | P1 | utopia (global page gutter) | handoff (moved from homepage: global) | two-formulas-393-day-after.png |
| TF-08 | two-formulas | <1200 · both | Ingredient chips are 10 px text; Figma mobile ≈12 px. Body text 15/22 against Figma 20/28 (body-lg) at 1440. | `3027:20922`, `2928:20020` | P1 | utopia | handoff | two-formulas-768-day-after.png |
| TF-09 | two-formulas | ≥1200 · both | Chip row up to 750 px wide (3 rows); Figma ≈600 px. | `2928:20020` | P2 | homepage | open | two-formulas-1440-day-after.png |
| TF-10 | two-formulas | all | `alt: section.settings.heading` probably carries `<strong>` markup into the alt text. | — | P2 | homepage | fixed `39a00a8` (with TF-01) | — |

## Benefits (`product-benefits-karmicare`, 9 cards, homepage only)

| ID | Section | Viewport · mode | Observed problem (evidence) | Reference | Prio | Owner | Status | Acceptance shot |
|---|---|---|---|---|---|---|---|---|
| BE-01 | benefits | 768, 1024 · both | The grid drops to 2 columns, so 9 cards make 5 rows with card 09 alone; the section is 1984 px tall at 768 and 1642 px at 1024 (1066 at 1440). At 1024 the 30 % left column squeezes the H2 to 3 lines. Cause: `columns_tablet` and `columns_laptop` = 2 and the side-by-side row at 990-1199. | `2928:20061` (3×3 grid) | P1 | homepage | fixed `6860d74` | benefits-768-day-after.png, benefits-1024-day-after.png |
| BE-02 | benefits | 393 · both | Swipe cards are 276×280; the 393 frame draws 280×320, but the approved card component (KC/Benefit card State=Mobile, instance `2608:48221`) is 297×277, which live follows. The 1.3-card peek matches. | `3027:20981` vs `2608:48221` | P2 | homepage | no change (live follows the approved component) | benefits-393-day-after.png |
| BE-03 | benefits | all | All 9 pictures are 297 px files (594-827 px needed). | — | P1 | assets | handoff | benefits-393-day-after.png |
| BE-04 | benefits | all | Card picture `image_tag` has no `sizes`/`widths`, so the browser assumes 100vw. | — | P2 | homepage | open (no gain until BE-03) | — |
| BE-05 | benefits | all | Card 07 heading contains U+2028: Chrome shows a double space and orphans "night" at 1440. Copy also differs from Figma ("Focus by day" vs "Bright by day", "one dose" vs "full dose"). | `2928:20061` | P1 | source-copy | handoff | benefits-1440-day-after.png |
| BE-06 | benefits | 393 · both | Note and price line use the desktop small size (14 px) on phones; Figma ≈12 px. Caption text at 0.70 opacity is lighter than Figma. | `3027:20981` | P2 | utopia | handoff | — |

Not a gap: the navy veil on the cards (approved component, 6aa0e71) although the 393 Figma frame still shows a light veil.

## Trusted professionals (`trusted-professionals`, also on the PDP)

| ID | Section | Viewport · mode | Observed problem (evidence) | Reference | Prio | Owner | Status | Acceptance shot |
|---|---|---|---|---|---|---|---|---|
| PR-01 | professionals | 393 · both | The glass name holders render blank (no name, no title) in the 393 captures; the DOM has the text (H3 "Dr. Stephanie Spreuwers", 18 px, x=19) and 768+ render fine. Probably a headless compositing artefact (backdrop-filter inside the `will-change: transform` marquee at DPR 3), not confirmed. | `3027:21056` | P0 if reproduced | homepage | pending (real iPhone/Android check) | professionals-393-day-after.png |
| PR-02 | professionals | ≥750 · both | Structure differs from V15: live is one drifting row of 7 cards; Figma Day has a featured-quote carousel plus a 4×2 grid (Night puts the grid first). | `2928:20081`, `2590:9974` | P1 | Victor | decision D-6 | professionals-1440-day-after.png |
| PR-03 | professionals | all | "REQUEST A PRACTITIONER SAMPLE" links to `#` (`button_link` empty on the homepage and the PDP); it shows on mobile only (`footer_display` default) while both desktop frames show it. | `2928:20081`, `3027:21056` | P0 (dead link) | homepage (Victor's rule H8) | fixed `4f8024c`: shared "Coming soon" state while the link is blank or `#` (D-7 decided 19 Oct); desktop visibility (`footer_display`) unchanged | professionals-393-day-after.png (pending preview gate) |
| PR-04 | professionals | 393-2560 | Full-bleed band is deliberate (same marquee as research), but card 1 starts at the viewport edge while the heading starts on the page gutter. | `3027:21056` | P2 | homepage | open | professionals-1920-day-after.png |
| PR-05 | professionals | 2560 · both | The 7-card set (2436 px) is narrower than the viewport, so Stephanie shows at both edges at once. | — | P2 | Victor | decision D-6 | professionals-2560-day-after.png |
| PR-06 | professionals | 393-1440 | Mariama, Kris and Kim portraits are 332 px files (664-840 px needed); Stephanie (718) and Iveta (761) are short at 393. | image list §2 rows 1-3 | P1 | assets | handoff | professionals-393-day-after.png |

## Research behind the system (`research-behind-system`, also on the PDP)

| ID | Section | Viewport · mode | Observed problem (evidence) | Reference | Prio | Owner | Status | Acceptance shot |
|---|---|---|---|---|---|---|---|---|
| RE-01 | research | all · both | All five source chips render `href="#"` under an external-link icon (`link_url` empty on the homepage and the PDP; `snippets/research-card.liquid` fell back to `'#'`): a tap jumps to the top of the page. | broken | P0 | homepage | fixed `bf5d314` | research-393-day-after.png, research-1440-day-after.png |
| RE-02 | research | all · both | "Explore the full evidence base" links to `#` (`button_link` empty on both templates). | brief §7/§8 ("/our-science") | P0 (dead link) | homepage (Victor's rule H8) | fixed `4f8024c`: shared "Coming soon" state while the link is blank or `#` (D-8 decided 19 Oct) | research-1440-day-after.png (pending preview gate) |
| RE-03 | research | 393-1920 | `Sleep_airway.png` (232 px) fills a 400×482 box; `Picture_1.png` is 400 px where 757-960 px is needed. | image list §2 rows 13-14 | P1 | assets | handoff | research-1440-day-after.png |
| RE-04 | research | all | Source logos are 95 px files shown at 1× only; the JCDR logo is a grey box with unreadable text. Logo `<img>` has no `widths`/`sizes`. | image list §2 row 18 | P2 | assets (+ homepage attributes) | handoff | research-1440-night-after.png |
| RE-05 | research | homepage | The same "DENTINE TUBULES" picture and badge sit on 4 of 5 cards, including Xylitol and SLS (twice on screen at 2560). | `2928:20143` | P2 | Victor / assets | decision D-9 | research-2560-day-after.png |
| RE-06 | research | 768 | The card is 738 of 768 px and the next card peeks 3 px, so nothing signals a row. | reflow | P2 | homepage | open | research-768-day-after.png |
| RE-07 | research | all | 10-11 px literals (mobile subheading, badge, chip) under the 12 px label-sm. | `3027:21117` | P2 | utopia | handoff | — |

Not a gap: the near edge-to-edge band at 2560 is the deliberate full-bleed marquee; card sizes match Figma (780 = 380 + 400, 482 tall).

## Care comes back (`care-comes-back`, also on the PDP)

| ID | Section | Viewport · mode | Observed problem (evidence) | Reference | Prio | Owner | Status | Acceptance shot |
|---|---|---|---|---|---|---|---|---|
| CC-01 | care-comes-back | all · both | Step markers print "01", "02", "03" (`sections/care-comes-back.liquid` L63-65). COMMON-RULES §3 bans 01/02/03 step labels. | COMMON-RULES §3 | P1 | homepage | fixed `7ff0562` (orchestrator OK) | care-comes-back-1440-day-after.png, care-comes-back-393-night-after.png |
| CC-02 | care-comes-back | 1024-2560 · both | Composition differs from `4013:29078`: Figma has the heading left in the page container, a CTA right and three equal columns with hairlines and icons; live centres everything in a 760 px column with a vertical loop. | `4013:29078` | P1 | Victor | decision D-10 | care-comes-back-1440-day-after.png |
| CC-03 | care-comes-back | all | No CTA; Figma has "BEGIN NOW" plus a price line, and the schema has no button setting. | `4013:29078` | P1 | Victor | decision D-10 | care-comes-back-1440-day-after.png |
| CC-04 | care-comes-back | all | Copy differs from Figma: eyebrow shows the placeholder "SUBTITLE", different step titles, intro and fine print not in Figma. | `4013:29078` | P1 | source-copy | handoff | care-comes-back-1440-day-after.png |
| CC-05 | care-comes-back | 393, 768 | "Terms, clauses 10 and 11" link is a 157×22 tap target. | — | P2 | homepage | open | care-comes-back-393-day-after.png |

Not a gap: the Accent surface against Figma's Page colour is a deliberate hold continuing the research band.

## FAQ (`km-faq-accordion`, homepage only)

| ID | Section | Viewport · mode | Observed problem (evidence) | Reference | Prio | Owner | Status | Acceptance shot |
|---|---|---|---|---|---|---|---|---|
| FQ-01 | faq | all · both | All six answers are the same text (the "two formulas" answer); "Is Karmicare fluoride-free?" and the others answer a different question. Category mapping also looks arbitrary ("Should I rinse after brushing?" under "Plans & Return on Care"). | brief §14 | P0 | source-copy | handoff | faq-1440-day-after.png |
| FQ-02 | faq | all · both | The filter chips are `<span>`s with click handlers: no focus, no Enter/Space, no pressed state (theme audit row 15). | a11y | P1 | homepage | fixed `174997e` | faq-1440-day-after.png + keyboard check |
| FQ-03 | faq | all · night | Card colour is `#2c3a60` (`card_bg_color_night`); Figma cards are `#212a49` (sampled), so live cards read lighter than the section instead of darker. | `2995:23222` | P1 | homepage (colour setting) | fixed `174997e` (#2c3a60 → #212a49, orchestrator OK) | faq-1440-night-after.png |
| FQ-04 | faq | all | Chips are 33 px tall against 28 in Figma (`line-height: normal`). They are pills; brand rule says no pill buttons. | `2995:23657` | P2 | Victor | decision D-11 | faq-1440-day-after.png |
| FQ-05 | faq | all | Question text about 10 % larger and answer text smaller than Figma. | `2995:23657` | P2 | utopia | handoff | — |

Matches Figma: centred heading, 680 px accordion, card spacing, section padding, and the 393 chip row that scrolls to the screen edge.

## Welcome kit end CTA (`featured-product`, also on the PDP)

| ID | Section | Viewport · mode | Observed problem (evidence) | Reference | Prio | Owner | Status | Acceptance shot |
|---|---|---|---|---|---|---|---|---|
| FP-01 | featured-product | 768 · both | The homepage used the `inline` benefits row (~513 px) in a 353 px offer column: it spills over the picture (content starts at x=320) and "Free shipping" is cut to "Free" at the screen edge (`featured-product-768-day-before.png`). | `2928:20190` | P0 | homepage | fixed `2124ebb` | featured-product-768-day-after.png |
| FP-02 | featured-product | 1024-2560 · both | V15 shows the three benefits as three columns with the icon above the label; live shows one inline row. | `2928:20190`, `2590:10048` | P1 | homepage | fixed `2124ebb` | featured-product-1440-day-after.png |
| FP-03 | featured-product | 990-1439 · both | The offer column is fixed at 564 px, so the picture column shrinks to 316 px (kit 369×328 at 1024) against Figma's 55:45 split. Same on the PDP. | `2928:20190` | P1 | homepage | fixed `2124ebb` | featured-product-1024-day-after.png |
| FP-04 | featured-product | 1920, 2560 · both | The 1346 px row is left-aligned in the 1416 px container: gutters 196/322 (1920) and 516/642 (2560), 63 px left of centre. Same on the PDP. | 1440 Figma composition | P1 | homepage | fixed `2124ebb` | featured-product-1920-day-after.png, featured-product-2560-day-after.png |
| FP-05 | featured-product | 2560 · day | The animation frame paints a lighter rectangle than the section background around the kit (`featured-product-2560-day-before.png`). | `2928:20190` | P2 | assets (video/poster background) | handoff | featured-product-2560-day-after.png |
| FP-06 | featured-product | 1440 · both | The kit renders about 18 % larger than Figma (toothbrush ≈515 px vs ≈435 px); shadow reaches x≈0. | `2928:20190` | P2 | Victor | decision D-13 | featured-product-1440-day-after.png |
| FP-07 | featured-product | 393-1440 | Poster `kc-anim-am-hero-1080x960-poster-v1.webp` is 1080 px; 1273-1640 px needed. | — | P2 | assets | handoff | — |
| FP-08 | featured-product | all | Benefit labels, order and item names differ from Figma ("Free shipping" second in Figma; "Ultra Soft … Toothbrush" vs "… Toothbrush 2.0"; "Varies" struck through). | `2928:20190` | P2 | source-copy | handoff | — |

Not gaps: the media column at 768 is present (353 px, vertically centred); 1440 matches Figma; the Page surface hold into the footer is deliberate (listed for Victor only as D-13 context).

## Footer (`footer`, global)

| ID | Section | Viewport · mode | Observed problem (evidence) | Reference | Prio | Owner | Status | Acceptance shot |
|---|---|---|---|---|---|---|---|---|
| FT-01 | footer | 1200-1439 · both | Copyright and legal links are 8 px apart (`gap: layout-xs`, `sections/footer.liquid` L557) and read as one sentence ("…Belgium product Terms and Conditions"); Figma ≈80 px. | `2928:20208` | P1 | homepage | fixed `82a0a51` | footer-1440-day-after.png |
| FT-02 | footer | 393, 768 · both | Menu links are 18-20 px tall inline anchors (15 small tap targets at 393); they pass WCAG 2.5.8 only by spacing. | — | P2 | homepage | open | footer-393-day-after.png |
| FT-03 | footer | all | Payment icons: 13 colour icons live vs 5 monochrome in Figma. | `2928:20208` | P2 | Victor | decision D-13 | footer-1440-day-after.png |
| FT-04 | footer | all | Currency flags load from `flagcdn.com`, a third-party request before cookie consent. | GDPR (theme audit row 2 context) | P1 | assets + Victor | handoff | — |
| FT-05 | footer | 393 · both | Legal body-sm is 15 px on mobile against 12 px in Figma, so the mobile footer is about 197 px taller. | `3027:21262` | P2 | utopia | handoff | — |

## Global

| ID | Section | Viewport · mode | Observed problem (evidence) | Reference | Prio | Owner | Status | Acceptance shot |
|---|---|---|---|---|---|---|---|---|
| GL-01 | cookie banner | 393 · both | Shopify's privacy banner covers most of the hero on first visit on phones (seen in the first 393 capture). Expected consent behaviour; noted only. | — | P2 | Victor | noted | — |
| GL-02 | all copy | all | Nav "Professionals" vs Figma "Atlas"; Night status "NIGHTTIME RESTORATION" vs "OVERNIGHT RESTORATION"; FAQ question "…biorhythmic toothpaste with fluoride" uses the category word beyond its first mention. | `2928:19881`, brief §2 | P2 | source-copy | handoff | — |

## Decisions for Victor (summary; options and recommendations in REPORT.md)

D-1 hero still vs AM/PM animation · D-2 "Why two formulas?" destination · D-3 hero badge on phones · D-4 clock evening callout (Day vs Night frame) · D-5 clock hint pill · D-6 professionals structure and the 2560 repeat · D-7 practitioner-sample link (decided: Coming soon, rule H8) · D-8 evidence-base link (decided: Coming soon, rule H8) · D-9 repeated research picture · D-10 care-comes-back desktop layout and CTA · D-11 FAQ pill chips · D-12 sticky header band · D-13 end CTA kit scale, surface and footer payment icons · D-14 phone stat strip: swipe (built) or auto-scroll (Figma frame name).
