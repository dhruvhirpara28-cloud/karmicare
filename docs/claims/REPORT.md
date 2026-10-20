# CR1 report · Clinical Research advisory review

Task `task_f75b35ea2400`, dispatch `ctx_fc1123304bbe`, run `run_32dd5602b983`. Brief: `.coordinator/BRIEF-CR1.md`. Deliverable: `docs/claims/CLINICAL-REVIEW.md` (per-claim verdicts, summary at the top). These verdicts are advice: Victor decides, and regulatory and legal sign-off is separate.

## 1. Preflight

| Check | Result |
|---|---|
| `orca status --json` | runtime `ready`, `reachable: true`, `connected` (runtime `dd11e98a…`, app 1.4.230) |
| `git status --short` | clean |
| Branch | `karmicare/soft-launch-source-copy` at `060de0e` |
| Model · permission mode | Claude Opus 5.5 (`claude-opus-5-5`) · auto mode |
| `AGENTS.md` | read; COMMON-RULES replace the README/RUNBOOK/design-token files it points to |
| Allowed paths | `docs/claims/**` only. Nothing else was written; no copy, batch, payload or theme file was touched. |

## 2. What was done

1. Read the role and method (`clinical-research-agent.md`), the rules (`regulatory.md`, `products.md` Do/Don't say, the 60-day brief front sheet and don'ts), every summary in the evidence library, and the claim register.
2. Pulled the full EN context of every claim entry from `docs/source-copy/en-source.json`, the neighbouring admin FAQ, comparison and treatment-journey fields, and the seven clock messages (`locales/en.default.json`), so that each claim was judged in its sentence and its row.
3. Gave one verdict per claim for the 47 needs-review and 3 unsupported claims of batches 01–03 and for the 9 bracketed onboarding lines, with the library evidence, the claim type, the evidence qualification and, where one exists, compliant EN wording.
4. Counted what the claims hold back in the NL payloads (this branch) and the FR payloads (`karmicare/soft-launch-fr` at `272f340`, read with `git show`), per section and per claim.

## 3. Results

| Verdict | Batches 01–03 | Onboarding |
|---|---:|---:|
| supported as worded | 4 | 2 |
| supported if reworded | 27 | 6 |
| needs a source we do not have | 10 | 1 |
| not supportable | 9 | 0 |

- NL and FR each hold **76 entries (1,496 EN words)** behind these claims. The research cards (22 entries) and the practitioner block (476 words, 32 % of the held words) are the largest blocks.
- Accepting the supported verdicts with their wording and removing or replacing the not-supportable claims releases **63 of 76 entries (1,286 words) per language**. The remaining 13 entries wait on documents: C60, C80, C81, C82, C90, C91, C93, C99.
- The five changes that clear the most held text, and every row, are in `CLINICAL-REVIEW.md` §1.

## 4. Method

- **Verdicts.** *Supported as worded*: cosmetic scope, library evidence, allowed verbs. *Supported if reworded*: a rewording within the evidence exists, and it is given. *Needs a source we do not have*: a named kind of study or document would settle it. *Not supportable*: disease or medical framing, a nootropic or sleep effect, a systemic effect of a cosmetic, a felt outcome or timeline without data, or a claim the evidence contradicts.
- **Evidence.** Only summaries in `.coordinator/source/clinical/evidence/`, cited by path (keys in `CLINICAL-REVIEW.md` §5). Strength follows the role document’s hierarchy and the three dimensions (clinical, psychological, sensory); sensory claims were not held to RCT standard. Each summary’s own “validated claims” section was not relied on: several overreach (NASA origin, “superior to fluoride”, “clinically proven”, valerian sleep benefits), and I judged from the reported findings instead.
- **Binding brand rules** taken over the role document’s examples: don’t #16 (no focus, energy, calm or sleep effect from guarana or valerian), don’t #13 (no superiority over fluoride), don’t #2 (no competitor), don’t #10 (no manufacturer whitepaper data in public copy). The role document’s worked examples cite Kennedy 2004, Haskell 2007, Bent 2006 for calming, Harks 2022 and others; these were not used where they conflict with the rules or are not in the library.
- **Wording.** Suggested EN reuses approved register wording, products.md Do-say lines or existing site copy where possible, otherwise it trims the original. New sentences are limited to restating a library finding with its study named. Where neither works, no wording is proposed.
- **Payload counts.** An entry counts as held when it carries at least one needs-review or unsupported claim from the register; words are EN words with HTML stripped. NL and FR hold identical entry sets.

## 5. What I could not assess, and why

| Item | Why | Affects |
|---|---|---|
| Kulal 2016 (the 98 % tubule card) | No summary in the library; only a logo row in `STUDY-LOGOS.md`. The role document ties the same figures to a manufacturer whitepaper naming competitor brands. | C60 |
| CPSR, SCCS opinion SCCS/1677/25, leaflet | None is in the sources; the PDP cites the CPSR and the SCCS opinion. The leaflet is being rewritten for the 1-pump dose (products.md). | C90, C91, C93, NEW-01 |
| FAQ files and the 45 brief | Not in this repo or the sources; I relied on the register’s quotes of FAQ-0206 and of the 45 brief. | C81, C90 |
| Whether the RDA batches are the v2 formula | The report (December 2025) names no formula version; INCI v2 dates from 3 June 2026. | C92 |
| Practitioner consent, review data, packaging specifications | Not clinical questions and no documents in the sources. | C80, C81, C82, C99 |
| The practitioner evidence pack | Its contents are not in the sources, so “Five studies in the pack” cannot be checked. | C43, C44 |
| Original papers | Only the summaries were available; the summaries were not checked against the PDFs (the xylitol summary was already corrected once, 6 March 2026). | all |
| New literature | Not searched: the brief limits citations to the library. | all |

## 6. Findings beyond the per-claim rows

1. **Daas 2018 is not fluoride-free evidence.** Its “nano-HAP paste” also contained 9,000 ppm fluoride. The 60-day brief §5.1 cites Daas 2018 for “Nano-hydroxyapatite remineralises enamel”, and the library’s other in vivo remineralisation evidence for fluoride-free nHAp is an uncontrolled study whose SEM found no significant change (Tekrawala 2022). Remineralisation claims therefore rest on a review (Pepla 2014) and in vitro data.
2. **Two §5.1 citations of the 60-day brief do not hold in the library.** “The oral microbiome influences gut-brain signalling — Herbert 2022”: Herbert is a survey of self-reported oral and mental health and does not test gut–brain signalling (Rajasekaran 2024 is the closer source, at review level). “Tschoppe 2011” has no summary in the library (“Erlind 2014” is Pepla 2014, cited by the author’s first name).
3. **Whitening through remineralisation has no study in the library.** The approved C22 and the products.md wording rest on product truth only; Harks 2022, the study the role document uses for it, is not in the library.
4. **No study in the library measures leave-on retention.** Every duration claim (“all night”, “while you sleep”, “hours”) lacks support; “extended contact time” and “works after the brush” are the defensible forms.
5. **No primary source in the library for salivary flow by time of day, melatonin or cortisol rhythms.** They appear only as background in two study discussions; the circadian folder README lists them as gaps.
6. **Disease endpoints on product pages.** Two research cards report a caries result (C62) and an ulcer result (C64). Accurate as study reports, but next to the formula they imply disease prevention; this is a regulatory decision, not a wording one.
7. **The RDA lab name on the PDP is wrong** (“Midwest University”; the report is Indiana University School of Dentistry OHRI), and the test predates INCI v2.

## 7. Decisions for Victor

**Accept as worded** (footnotes in `CLINICAL-REVIEW.md`): C50, C51, C61 on the site; C61 and NEW-02 in onboarding; C83, once Leen Ponet approves the EN, NL and FR.

**Accept the reworded EN** (wording in `CLINICAL-REVIEW.md` §2 and §4):
- Leave-on duration: C12, C13, C14 and onboarding C14.
- Sensitivity: C21, C24, C63, C95; onboarding C21, C24, NEW-01 (fingertip application only if the leaflet covers it).
- Ingredients and mechanism: C23, C33, C37, C43, C44, C97; onboarding C97.
- Clock texts: C52, C53, and C54 messages 1, 6 and 7 (trims).
- Comparison table and practitioner FAQ: C45 (with its row label as flavours), C46.
- Counts: C65, C66, C67 (“Formulated on peer-reviewed studies”), C68.
- Practitioner block: C70.
- Gums out, breath kept: C36, C94 and onboarding C94.
- Plaque and balance: C96.
- Lab name: C92 (after the v2 batch check and your RDA release decision).
- Floss name: C100.

**Remove or replace**: C35 (gum card), C40 and C41 (focus/calm card), C42 (oral-gut-brain row), C84 and C85 (nutritional-therapist quote), C98 (“feel the repair”). Replacement lines are in §2 of the review.

**Decide with the regulatory reviewer**: C62 and C64. Recommendation: remove both cards; if they stay, use the qualified wording given.

**Obtain documents**: the CPSR conclusion for leave-on use (C90, C91, C93); a summary of the SCCS opinion SCCS/1677/25; a summary of Kulal 2016 (C60; hide the card meanwhile); practitioner consent and a dated count (C70 “recommend”, C80, C81); the review-platform figure (C82); packaging specifications (C99); a cariology and salivary-flow source (C54 messages 2–5); a gum study of the formula if a gum benefit is wanted (C34).

**Structure**: drop the week headings of the PDP treatment journey (C94–C98). Untimed lines are supportable; timed member outcomes are not.

## 8. Handoffs

| Owner | What |
|---|---|
| Source-copy owner | Apply the EN wording Victor accepts to `en-source.json` and the batches, and update the register statuses. |
| NL and FR localization | Re-translate the reworded lines once the EN changes. The payloads already hold the C33 forms (“helpt biofilm verminderen”, “AIDE À RÉDUIRE LE BIOFILM”). |
| Admin (Victor or DH) | Product title “Whitening Charcoal Floss” (C100), the PDP metafields (C37, C42–C46, C90–C93, C94–C98), the RDA lab name (C92). |
| Onboarding owner | Replace or cut the 9 bracketed lines per §4 of the review; `check.py` expects every bracketed row to stay listed until its tag is removed. |
| Regulatory / legal | Disease endpoints (C62, C64), the free-from claim (C44), “safety-assessed” wording (C93), consumer reviews (C82), recyclability (C99). |
| Evidence library | Add summaries for Kulal 2016, the SCCS opinion, a salivary-flow / cariology source and a xylitol microbiome study; correct the 60-day brief §5.1 citations (§6.2). |

## 9. Commits

All on `karmicare/soft-launch-source-copy`, pathspec only, under `docs/claims/`:

- `docs(claims): CR1 clinical review of held claims and onboarding lines` (`CLINICAL-REVIEW.md`)
- `docs(claims): CR1 report with preflight, method and decisions` (this file)

No theme files changed, so Theme Check was not run.
