# Science imagery · image plan

**Created**: 2026-10-20

### Changelog
| Date | Change |
|------|--------|
| 2026-10-20 | First plan: card spots, claim status, candidates, rendered size, decisions B-0 to B-5. No code. |
| 2026-10-21 | SCI-R2 fixes (F1–F6): eligibility per file, V3 08 no longer an interim, release gates G1–G4, claims dependencies C61/C63/C68, corrected crop and box sizes, decisions B-1 to B-7 with single-meaning tokens and owners, K4/K5 recorded as operative. |
| 2026-10-22 | SCI-R2 recheck: B-6 applies only with B-5 = `noot`; staging on the branch preview separated from release, G4 checked after staging. |

Branch `karmicare/science-imagery` from `origin/mearchant-edit` `61d59bc` (= live). Lane brief: `.coordinator/BRIEF-COORDINATOR.md`. Local review page with thumbnails: `.coordinator/out/review/index.html` (published copy: `http://127.0.0.1:8790/review/science/`).

**All candidate images are AI-generated editorial concepts**, not study photography, SEM images or measurement data. Nothing in this plan is dental, histological, regulatory or legal sign-off, and an owner's choice to publish is not scientific clearance.

## Inputs

| Input | Path |
|---|---|
| V3 round (9 Oct), 17 images, native 1145 × 1374 | `.coordinator/source/imagery/clinical-research-v3-20261009/` (`native/`, `manifest.json`) |
| V2 round (29 Sep) and the 1 Oct source-fidelity review | `.coordinator/source/imagery/clinical-research-v2-20260929/scientific-review-20261001.md` |
| Earlier rounds, incl. the source of live `Sleep_airway.png` | `.coordinator/source/imagery/scientific-imagery/03c-sleep-airway-clean-background-2000.png` |
| Claims review CR1 (C60–C64, C68) | `.coordinator/source/claims/CLINICAL-REVIEW.md` |
| Astra reviews | `docs/runtime-review/SCI-R1-IMAGERY-ASTRA.md` (V3 set), `docs/runtime-review/SCI-R2-IMAGE-PLAN-ASTRA.md` (this plan at `42965c4`); both git-excluded |
| Live images (read-only fetch, 20 Oct) | `Picture_1.png` (`?v=1790538751`), `Sleep_airway.png` (`?v=1790535784`) |

`delivery/` PNGs (2000 × 2400) are mechanical upscales of `native/`; derivatives are made from `native/` so nothing is upscaled.

## What is live today

Live `Picture_1.png` is a crop of `scientific-imagery/02-nhap-dentinal-tubule-occlusion-2000.png`: open tubules on the left, filled ones on the right. It reads as a measured before/after, the thing the 1 Oct guardrail 3 rules out, and it sits on four cards, including the xylitol and canker-sore cards where it has nothing to do with the study. Live `Sleep_airway.png` is a translucent head with a dental arch and a lit airway: a conceptual anatomical composite that suggests an airway mechanism Lei & Hu did not study.

The live homepage on 20 Oct still renders all five cards (four `Picture_1`, one `Sleep_airway`).

## Claim decisions

- **K4 = remove** (xylitol and canker-sore cards) and **K5 = hide** (Kulal 98 % card until its source is in the library) are the operative decisions supplied to this lane (lane task; recorded in SCI-R1 l. 11). They are not reopened here.
- **K2 = CR1 rewordings apply** is the relayed acceptance of the wording; it is not proof that the reworded copy has landed.
- Implementing K2, K4 and K5 (card text, removing and hiding blocks) is the claims lane's (`karmicare/soft-launch-source-copy`) and Victor's live editor's. This lane changes only the `image` lines of the surviving cards. Leaving the image lines of the removed and hidden cards untouched is not the same as removing them.

## Card spots

Section `research_behind_system_EkjATL` (homepage l. 469, PDP l. 496), marquee on (l. 591 / l. 616). Line numbers are on `61d59bc`.

| Card (block) | Study · V3 # | Homepage `index.json` | PDP `product.subscription-item.json` | Claim status (K-decision · CR1) |
|---|---|---|---|---|
| 98 % tubules (`card_bDxUVT`) | Kulal 2016 · 08 | l. 485 `Picture_1.png` | l. 512 `Picture_1.png` | **K5 hide** · C60 "needs a source we do not have" |
| Oral health ↔ sleep (`card_yMiD9D`) | Lei & Hu 2025 · 01 | l. 502 `Sleep_airway.png` | l. 529 `Sleep_airway.png` | **stays** · C61 "supported as worded", with the observational / not-Karmicare footnote |
| Xylitol caries (`card_fmFMFd`) | Janakiram 2017 · 11 | l. 519 `Picture_1.png` | no image line | **K4 remove** · C62 "not supportable" |
| Nano-HAp sensitivity (`card_Hi7YUD`) | Vano 2018 · 07 | l. 536 `Picture_1.png` | l. 562 `Picture_1.png` | **stays, to be reworded** · C63 "supported if reworded"; baseline still says "beat fluoride" (l. 527 / l. 553) |
| SLS-free canker sores (`card_JeERX6`) | Alli 2019 · 14 | l. 553 `Picture_1.png` | no image line | **K4 remove** · C64 "not supportable" |

## Eligibility of each file

| Status | Meaning |
|---|---|
| **Eligible with gates** | May go on once gates G1–G4 below are met. |
| **Held** | Not to be used until a stated fix (refinement, reference, expert review) is done; a label does not lift it. |
| **Rejected** | Comparison and history only. |

### Lei & Hu (01) · homepage l. 502, PDP l. 529

| File | Status | 1 Oct ask · fixed? | Notes |
|---|---|---|---|
| **V3 01** `clinical-research-v3-20261009/native/01-lei-oral-health-sleep-v3.png` | **Eligible with gates** | Teeth-through-cheek overlay; no causal pathway · **fixed** | No internal anatomy depicted. Oral-health cue now carried by the card text only. The old "01 dental review" gate is not closed by this; see G3. Mobile crop: see "Rendered size". |
| No image (empty `image`) | **Eligible** (fallback) | — | Card renders as the "Image=None" variant. Used while G1–G3 are open. |
| V2 01 `clinical-research-v2-20260929/native/01-lei-oral-health-sleep-v2.png` | Rejected | same · not fixed | Teeth visible through the cheek. |
| Live `Sleep_airway.png` (`scientific-imagery/03c-…`) | Rejected | (older round) | Translucent anatomy and lit airway imply an airway mechanism; square 1:1. |
| Earlier `scientific-imagery/08-poorer-oral-health-poorer-sleep-2000.png` | Rejected | (older round) | Tooth-and-bone cutaway through the cheek. |

Astra SCI-R1: "V3 01 is the strongest of these three candidates", verdict "use only with an approved illustration label".

### Vano (07) · homepage l. 536, PDP l. 562

| File | Status | 1 Oct ask · fixed? | Notes |
|---|---|---|---|
| **No image** (empty `image`) | **Eligible** | — | Card renders as "Image=None" (badge is hidden with the image: `snippets/research-card.liquid` l. 56–63). |
| V3 07 `clinical-research-v3-20261009/native/07-vano-dentine-sensitivity-v3.png` | **Held**: refine first | Machined-looking lumens; credible dentine and restrained occlusion · **not fixed** | Two dominant open channels, recoloured ivory. Needs a verified dentine reference and dental/histology review. |
| V3 08 `clinical-research-v3-20261009/native/08-kulal-dentine-tubule-occlusion-v3.png` | **Held**: refine first | No dominant open hole · **partly fixed** | Sponge-like, unverified texture. Its image-level verdict follows the file to any card; it is not an interim for Vano. Kept as a reference for a future reviewed round. |
| V2 07 `clinical-research-v2-20260929/native/07-vano-dentine-sensitivity-v1.png` | Rejected | same as V3 07 · not fixed | Same geometry, monochrome. |
| Live `Picture_1.png` | Rejected | (older round) | Open vs filled side by side: reads as a measured before/after. |

Vano measured cold-air and tactile sensitivity, not deposits in tubules; any future tubule picture is a mechanism illustration, not trial imaging.

### Cards that go or wait (no change in this lane)

| Card | Best file if it ever returns | Why not now |
|---|---|---|
| Kulal (08) | V3 08 (held: refine first) | K5: source not in the library; the paper's 1 % / 15 % and 98.1 / 97.62 % conflict is unresolved. A render cannot show "98 %". Source reconciliation would not fix the image anatomy. |
| Janakiram (11) | V3 11 | K4. An intact molar beside a caries heading implies prevention by the formula. |
| Alli (14) | V3 14 | K4. Still very glossy (1 Oct asked to reduce it); a lesion-free lip beside the heading reads as a healed result. |

## Release gates for any AI-generated image

Two steps. **Staging**: once Victor has picked an eligible image (B-1) and uploaded it to Files with the B-7 alt decision, this lane sets it in the branch templates and pushes the unpublished branch preview, so G4 can be checked on the real render. **Release**: the branch is ready to land only when G1–G4 all hold and the landing desk has confirmed the claims dependencies below on both templates. If G1 or G3 is still open at landing time, the image line goes back to empty (no image) before "Ready to land".

| Gate | What | Owner | State |
|---|---|---|---|
| G1 | Visible disclosure: wording approved by Victor (B-4) and placed (B-5) | Wording: Victor. Placement and edit: claims lane | `[NEEDS APPROVED COPY]` |
| G2 | Accessible image text decided (B-7). `image_tag` outputs the image's alt text from Shopify Files, so it is set on upload | Victor (in Files) | open |
| G3 | Old 01 dental gate: written close-out by a dentist (B-3 `expert`), or Victor's recorded owner exception (B-3 `uitzondering`) with the expert verdict still open | Expert / Victor | open |
| G4 | In-context check of the actual desktop and mobile crop with the final badge state, on the staged branch preview (the crop arithmetic below does not satisfy it) | This lane | after staging |

## Claims dependencies before release

The image change can land on its own, but the section must not go live with images next to copy that CR1 says must change. The claims lane owns the wording and edits; the landing desk confirms the integrated state on both templates before release.

| CR1 | What still stands at `61d59bc` | Where |
|---|---|---|
| C68 | Section note: "the top of the evidence hierarchy" and "more than 38,000 people" (the 38,266 total includes the two removed studies; with Kulal hidden no laboratory study is shown) | `index.json` l. 569, `product.subscription-item.json` l. 594 |
| C63 | Vano heading "Nano-HAp beat fluoride on tooth sensitivity." and result line; footnote on the tested 2 % gel | `index.json` l. 527/530, `product.subscription-item.json` l. 553/556 |
| C61 | Lei footnote (observational, varied results, not a test of Karmicare) not present | Lei card / section, both templates |
| K4 / K5 | Xylitol and canker-sore blocks still present; Kulal block still visible | `card_fmFMFd`, `card_JeERX6`, `card_bDxUVT`, both templates |
| Badges | Lei `SLEEP · AIRWAY AND ORAL CAVITY` no longer matches V3 01 (B-6). Vano `DENTINE TUBULES · OPEN AND OCCLUDED` describes a before/after; hidden while Vano has no image, must change before any image returns | `index.json` l. 503 / 537, `product.subscription-item.json` l. 530 / 563 |

## Rendered size and derivative spec

`snippets/research-card.liquid` l. 58: `image_url: width: 800`, `widths: '400, 640, 800'`, `sizes: '(min-width: 750px) 400px, 320px'`. Marquee widths from `assets/section-research-behind-system.css` l. 124–133 and l. 425, at body scale 100 % and a 10 px rem:

- **< 750 px**: card `min(32rem, 100cqw − 2 × gutter)`, at most 320 px; picture under the body, 20rem = 200 px high (l. 359), `object-fit: cover`. A 5:6 image at 320 px wide is 384 px high, so the 200 px window keeps **52.1 %** of the height and cuts **47.9 %** (24.0 % top and bottom, centred). In native pixels the visible band is about y = 329 to 1045. The theme has no focal-point setting and the CSS sets no `object-position`, so this is the default centred case.
- **≥ 750 px**: media card `min(78rem, 100cqw − 3rem)`, picture 400/780 of it. At a 750 px viewport the card is 720 px and the picture about 369 px wide; the full 780 / 400 px is reached at 810 px. Picture height is the card height, **at least** 480 px (`min-height: 48rem`). A card without image is at most 380 px wide.
- The 990 / 1440 px rules apply to the grid/slider layout, not to the marquee these templates use.

**Derivative**: sRGB JPEG **1000 × 1200** (5:6), downscaled to 87.3 % of `native/` (1145 × 1374), quality tuned to ≤ 350 KB (checked on export). Name `kc-research-<nn>-<study>-1000x1200-v3.jpg`, in `.coordinator/out/upload/`. Shopify's CDN serves WebP/AVIF from the JPEG.
**Limit**: the snippet never requests more than 800 px wide, so the browser gets at most 800 × 960. That is 2× for a 400 × 480 box, but only 1.6× if the card grows to 400 × 600. The extra source pixels are headroom; raising the snippet's cap is a separate scope decision, not part of this lane.

## Decisions for Victor

Each token has one meaning. Files marked held or rejected above are not options.

| Id | Question | Tokens | Recommendation |
|---|---|---|---|
| B-1 | Lei card image (home + PDP) | `v3` = V3 01: staged on the branch preview after upload, released only when G1–G4 are met (otherwise no image at landing) · `geen` = no image | **v3** |
| B-2 | Vano card image (home + PDP) | `geen` = no image now, no further step · `geen+v4` = no image now, and ask the brand repo for a reference-grounded refinement of 07 for dental/histology review | **geen+v4** |
| B-3 | Old 01 dental gate (G3) | `expert` = ask a dentist for a written close-out of V3 01 first · `uitzondering` = publish V3 01 with the approved label as an owner exception; the expert verdict stays open and is recorded in REPORT.md | **expert** (a face-only image is a short check) |
| B-4 | Disclosure wording (G1) | `1okt` = approve the 1 Oct proposal "AI-generated scientific illustrations. Not study photographs or measured before-and-after results." · `anders` = you give other wording | **1okt** |
| B-5 | Disclosure placement (G1) | `noot` = once in the section note (claims lane, with C68) · `badge` = on each image card's badge (claims lane) | **noot** |
| B-6 | Lei badge `SLEEP · AIRWAY AND ORAL CAVITY`. **Only answered when B-5 = `noot`**; with B-5 = `badge` the Lei badge always carries the B-4 disclosure and B-6 does not apply | `leeg` = claims lane empties it · `herschrijf` = claims lane proposes new wording for your approval | **leeg** |
| B-7 | Accessible image text (G2) | `leeg` = empty alt in Files: decorative, the card text carries the meaning · `tekst` = you give alt text per image | **leeg** |

One-line answer, for example: `BEELDEN: B-1=v3, B-2=geen+v4, B-3=expert, B-4=1okt, B-5=noot, B-6=leeg, B-7=leeg`.

## Handoffs (not this lane)

| To | What |
|---|---|
| Claims lane | C68 section note, C63 Vano rewording and footnote, C61 Lei footnote, K4 removal, K5 hiding (both templates); disclosure placement (B-5); Lei badge (B-6); Vano badge before any image returns. |
| Landing desk | Confirm the claims dependencies are integrated on both templates before release. |
| Brand repo (kc-ai-master `karmicare/science-imagery`) | If B-2 = `geen+v4`: reference-grounded refinement of 07 (and 08 if Kulal returns) from a verified dentine reference. |
| Dentist / dental histologist | If B-3 = `expert`: written close-out of V3 01; later, any refined tubule image. |
| Evidence owner | Kulal source into the library (C60). |
| Victor | Upload derivatives to Files, alt text per B-7. |
