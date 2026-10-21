# Science imagery · image plan

**Created**: 2026-10-20

### Changelog
| Date | Change |
|------|--------|
| 2026-10-20 | First plan: card spots, claim status, candidates, rendered size, decisions B-1 to B-5. No code. |

Branch `karmicare/science-imagery` from `origin/mearchant-edit` `61d59bc` (= live). Lane brief: `.coordinator/BRIEF-COORDINATOR.md`. Local review page with thumbnails: `.coordinator/out/review/index.html`.

**All candidate images are AI-generated editorial concepts**, not study photography, SEM images or measurement data. Nothing in this plan is dental, histological, regulatory or legal sign-off.

## Inputs

| Input | Path |
|---|---|
| V3 round (9 Oct), 17 images, native 1145 × 1374 | `.coordinator/source/imagery/clinical-research-v3-20261009/` (`native/`, `manifest.json`) |
| V2 round (29 Sep) and the 1 Oct source-fidelity review | `.coordinator/source/imagery/clinical-research-v2-20260929/scientific-review-20261001.md` |
| Earlier rounds, incl. the source of live `Sleep_airway.png` | `.coordinator/source/imagery/scientific-imagery/03c-sleep-airway-clean-background-2000.png` |
| Claims review CR1 (C60–C64, C68) | `.coordinator/source/claims/CLINICAL-REVIEW.md` |
| Astra fidelity review of the V3 set | `docs/runtime-review/SCI-R1-IMAGERY-ASTRA.md` (git-excluded) |
| Live images (read-only fetch, 20 Oct) | `Picture_1.png` (`?v=1790538751`), `Sleep_airway.png` (`?v=1790535784`) |

`delivery/` PNGs (2000 × 2400) are mechanical upscales of `native/`; derivatives are made from `native/` so nothing is upscaled.

## What is live today

Live `Picture_1.png` is a crop of `scientific-imagery/02-nhap-dentinal-tubule-occlusion-2000.png`: open tubules on the left, filled ones on the right. It reads as a measured before/after, the thing the 1 Oct guardrail 3 rules out, and it sits on four cards, including the xylitol and canker-sore cards where it has nothing to do with the study. Live `Sleep_airway.png` is a translucent head with a dental arch and a lit airway: a conceptual anatomical composite that suggests an airway mechanism Lei & Hu did not study.

The live homepage on 20 Oct still renders all five cards (four `Picture_1`, one `Sleep_airway`).

## Card spots

Section `research_behind_system_EkjATL`, marquee on, in both templates. Line numbers are on `61d59bc`.

| Card (block) | Study · V3 # | Homepage `index.json` | PDP `product.subscription-item.json` | Claim status (K-decision · CR1) |
|---|---|---|---|---|
| 98 % tubules (`card_bDxUVT`) | Kulal 2016 · 08 | l. 485 `Picture_1.png` | l. 512 `Picture_1.png` | **K5 = hide** until the source is in the library · C60 "needs a source we do not have" |
| Oral health ↔ sleep (`card_yMiD9D`) | Lei & Hu 2025 · 01 | l. 502 `Sleep_airway.png` | l. 529 `Sleep_airway.png` | **stays** · C61 "supported as worded" (+ footnote) |
| Xylitol caries (`card_fmFMFd`) | Janakiram 2017 · 11 | l. 519 `Picture_1.png` | no image line | **K4 = remove** · C62 "not supportable" |
| Nano-HAp sensitivity (`card_Hi7YUD`) | Vano 2018 · 07 | l. 536 `Picture_1.png` | l. 562 `Picture_1.png` | **stays, reworded** (K2) · C63 "supported if reworded" |
| SLS-free canker sores (`card_JeERX6`) | Alli 2019 · 14 | l. 553 `Picture_1.png` | no image line | **K4 = remove** · C64 "not supportable" |

K-decisions as relayed from the NL lane (`K2=ja`, `K4=weg`, `K5=verberg`); possibly never submitted, so they are confirmed with Victor first (B-0). Card text, removal and hiding belong to the claims lane (`karmicare/soft-launch-source-copy`) and Victor's live editor. This lane changes only the `image` lines of the surviving cards.

## Candidates per surviving card

### Lei & Hu (01) · homepage l. 502, PDP l. 529

| Candidate | File | 1 Oct ask | Fixed in this file? | Risks |
|---|---|---|---|---|
| **V3 01** | `clinical-research-v3-20261009/native/01-lei-oral-health-sleep-v3.png` | Teeth-through-cheek overlay too literal; no causal pathway | **Yes**: intact sleeping face, closed lips, no anatomy | None anatomical. Oral-health cue now carried by the card text only. Old "01 dental review" gate needs an explicit close-out (no internal anatomy left to check). Mobile crop (320 × 200 centre band) shows cheek, nose and lips; the closed eye is at the top edge. |
| V2 01 | `clinical-research-v2-20260929/native/01-lei-oral-health-sleep-v2.png` | same | No: teeth visible through the cheek | Anatomically wrong, monochrome |
| Live `Sleep_airway.png` | `scientific-imagery/03c-sleep-airway-clean-background-2000.png` | (older round, not in the 1 Oct grid) | n/a | Translucent anatomy and lit airway imply an airway mechanism; square 1:1, not the 5:6 card format |
| Earlier 08 | `scientific-imagery/08-poorer-oral-health-poorer-sleep-2000.png` | (older round) | n/a | Teeth-and-bone cutaway through the cheek, same problem as V2 |

Astra: "V3 01 is the strongest of these three candidates", verdict "use only with an approved illustration label".
**Recommendation: V3 01** on both templates.

### Vano (07) · homepage l. 536, PDP l. 562

| Candidate | File | 1 Oct ask | Fixed in this file? | Risks |
|---|---|---|---|---|
| V3 07 | `clinical-research-v3-20261009/native/07-vano-dentine-sensitivity-v3.png` | Large machined-looking lumens dominate; show credible dentine and restrained, visible occlusion | **No**: same two dominant open channels, recoloured ivory | Exaggerated anatomy; the open channels are the focal point. Dental/histology review required (1 Oct list 06–09, Astra "refine first"). |
| V3 08 (made for Kulal) | `clinical-research-v3-20261009/native/08-kulal-dentine-tubule-occlusion-v3.png` | Avoid a dominant open hole as the "sealed" end state | **Partly**: no dominant hole, most mouths hold deposits, a few stay dark | Still sponge-like, unverified texture. Dental/histology review required. Astra "refine first". If Kulal comes back later, both cards would share one picture. |
| V2 07 | `clinical-research-v2-20260929/native/07-vano-dentine-sensitivity-v1.png` | same as V3 07 | No | Same geometry, monochrome |
| Live `Picture_1.png` | crop of `scientific-imagery/02-nhap-dentinal-tubule-occlusion-2000.png` | (older round) | n/a | Open vs filled side by side: reads as a measured before/after |
| No image | — | — | — | The card renders as the designed "Image=None" variant (380 px wide). Honest; less visual weight in the marquee. |

Vano measured cold-air and tactile sensitivity, not deposits in tubules; any tubule picture is a mechanism illustration, not trial imaging.
**Recommendation: no image for now** (empty `image` on both templates) and a reference-grounded refinement of 07 in the brand repo, checked by a dentist or dental histologist before it goes on. Second choice: V3 08 with an approved illustration label as an interim.

### Cards that go or wait (no change in this lane)

| Card | Best candidate if it ever returns | Why not now |
|---|---|---|
| Kulal (08) | V3 08 (refine first) | K5: source not in the library; the paper's 1 % / 15 % and 98.1 / 97.62 % conflict is unresolved. A render cannot show "98 %". |
| Janakiram (11) | V3 11 | K4. An intact molar beside a caries heading implies prevention by the formula. |
| Alli (14) | V3 14 | K4. Still very glossy (1 Oct asked to reduce it); a lesion-free lip beside the heading reads as a healed result. |

Their `image` lines stay as they are; when the claims lane removes or hides those blocks, the image lines go with them.

## Rendered size and derivative spec

`snippets/research-card.liquid` l. 58: `image_url: width: 800`, `widths: '400, 640, 800'`, `sizes: '(min-width: 750px) 400px, 320px'`. `assets/section-research-behind-system.css`:

- **≥ 750 px**: picture on the right, `flex: 0 0 calc(400 / 780 * 100%)` of a 780 px card, card `min-height: 48rem` → a 400 × ≥ 480 CSS px box (5:6 at minimum height), `object-fit: cover`. At 2× DPR: 800 × 960 device px.
- **< 750 px**: picture under the body, `flex: 0 0 20rem` in a 320 px card → a **320 × 200 landscape** box; `cover` shows only the centre band (about 62 % of the height is cut). The theme has no focal-point setting, so the centre of each image has to work on its own.
- The largest file the srcset ever asks for is 800 px wide.

**Derivative**: sRGB JPEG, **1000 × 1200** (5:6, covers the 800 w srcset and a card taller than 480 px), downscaled from `native/` (1145 × 1374), quality tuned to ≤ 350 KB. Name `kc-research-<nn>-<study>-1000x1200-v3.jpg`, in `.coordinator/out/upload/`. Shopify's CDN serves WebP/AVIF from the JPEG itself, so a JPEG upload is enough.

## Decisions for Victor

| Id | Question | Options | Recommendation |
|---|---|---|---|
| B-0 | Confirm the claim decisions | `K4=weg`, `K5=verberg`, `K2=ja` as relayed · other | Confirm as relayed |
| B-1 | Lei card image (home + PDP) | `v3` V3 01 · `live` keep `Sleep_airway.png` · `v2` V2 01 | **v3** |
| B-2 | Vano card image (home + PDP) | `geen` no image until a refined 07 · `v3-08` V3 08 interim · `v3-07` V3 07 · `live` keep `Picture_1.png` | **geen** |
| B-3 | Expert review (1 Oct: dental/histology for 01, 02, 06–09) | `wacht` wait for an expert before any tubule image goes on · `label` publish with an illustration label you approve | **01: close the gate yourself** (no anatomy left in V3 01); **tubule images: wacht** |
| B-4 | Visible "illustration" disclosure | approve the 1 Oct wording "AI-generated scientific illustrations. Not study photographs or measured before-and-after results." · other wording · none | Approve the 1 Oct wording; placement (section note or badge) is copy and goes to the claims lane `[NEEDS APPROVED COPY]` until then |
| B-5 | Lei badge `SLEEP · AIRWAY AND ORAL CAVITY` describes the airway that V3 01 no longer shows | claims lane rewrites or empties the badge · keep | Hand to the claims lane; this lane does not touch copy |

Victor answers in one line, for example `BEELDEN: B-0=ja, B-1=v3, B-2=geen, B-3=01-ok/wacht, B-4=ja, B-5=claims`.

## Handoffs (not this lane)

- **Claims lane**: Lei badge text (B-5); disclosure placement (B-4); Vano badge `DENTINE TUBULES · OPEN AND OCCLUDED` describes a before/after and goes stale if B-2 = geen; removal/hiding of the Kulal, Janakiram and Alli blocks, with their image lines.
- **Brand repo (kc-ai-master `karmicare/science-imagery`)**: a reference-grounded refinement of 07 (and 08 if Kulal returns), from a verified dentine reference.
- **Dental/histology reviewer**: tubule images before they go on; explicit close-out of the old 01 gate.
- **Evidence owner**: Kulal source into the library (C60).
