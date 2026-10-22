# CR1 report · Clinical Research advisory review

## Status 22 Oct

The rows of the lane that concern this report; the whole lane is in `docs/source-copy/REPORT.md` (same row numbers).

"In merchant-edit" is checked with `git merge-base --is-ancestor <sha> merchant-edit` against `2ef9b5c` (22 Oct). merchant-edit is not pushed yet, so none of it is live.

| Status | Rows |
|---|---:|
| In merchant-edit | 3 |
| Ready to land | 1 |
| In progress | 0 |
| Waiting for Victor | 10 |
| Parked / after launch | 0 |
| Dropped | 0 |

| # | Status | What | Commits / where |
|---|---|---|---|
| 3 | In merchant-edit | Claims register `CLAIMS-REVIEW.md`: 70 claims, 17 approved, 49 needs-review, 3 unsupported, 1 confirmed (C103) | `0b98382` … `1437fc5` |
| 7 | In merchant-edit | Announcement line "FREE SHIPPING & 60-DAY GUARANTEE FOR MEMBERS · BELGIAN-MADE · EST. 2017" (C103 confirmed by Victor) and the newsletter placeholder *jij@voorbeeld.be* / *vous@exemple.be* | `6112414`, `1437fc5` |
| 10 | In merchant-edit | Clinical review CR1: advice on 50 claims and 9 onboarding lines | `3ebf113`, `2a7f809` |
| 19 | Waiting for Victor | Live figures and claims a–p (K1 on the claims review page) | review page `claims.html`, Prioriteiten |
| 20 | Waiting for Victor | 27 reworded claims from CR1 (K2) | `docs/claims/CLINICAL-REVIEW.md` §2, §4 |
| 21 | Waiting for Victor | Claims that cannot be supported (K3) | C35, C40, C41, C42, C84, C85, C98 |
| 22 | Waiting for Victor | Research cards on tooth decay (C62) and canker sores (C64) (K4) | research section, homepage and PDP |
| 23 | Waiting for Victor | Missing sources (K5) | CPSR, SCCS opinion, practitioner consent, review figure, packaging |
| 24 | Waiting for Victor | Week headings of the PDP treatment journey (K6) | C94–C98, admin metafield |
| 25 | Waiting for Victor | Leen Ponet's quote (K7) | C83, homepage and PDP |
| 28 | Waiting for Victor | regulatory.md wins over products.md (S4) | the clinical sources |
| 36 | Waiting for Victor | Sietske Hamelink's quote in NL and FR | C85, homepage and PDP |
| 51 | Ready to land | Victor's admin EN edits of 22 Oct in the EN source and the NL: the Duo's title, SEO title and meta description, the footer menu link "Why hydroxyapatite", six fields of the nano-hydroxyapatite article. His own NL/FR Duo texts are recorded as registered (`registration/registered.json`), so the plan never overwrites them. The FR payload follows in the FR lane | reported 22 Oct to the global coordinator |
| 52 | Waiting for Victor | Releasing the nano-hydroxyapatite article in NL and FR | `/blogs/news/nano-hydroxyapatite`, batch 07 |

### Waiting for Victor: the questions

**19. Live figures and claims a–p (K1 on the claims review page).** The Prioriteiten page lists 16 live figures and claims with the exact text now and a proposed text. Who changes them, and when?
- (a) You change them live in the theme editor and the admin (about 20 minutes).
- (b) They go with the landing (theme text) and you change only the admin text.
- (c) Per letter, with a note.
- *Advice*: (b): theme text then goes through review and Theme Check like every other change, and you only touch the admin.

**20. 27 reworded claims from CR1 (K2).** Accept the 27 rewordings that keep a claim within the evidence (leave-on duration, sensitivity, ingredients, clock texts, counts, the practitioner block, C63 and others)?
- (a) Yes, all 27.
- (b) One by one.
- *Advice*: (a): I then apply the EN, the NL follows, and those entries leave pending-claim-review and join the registration.

**21. Claims that cannot be supported (K3).** Remove or replace the gum card (C35), the focus/calm card (C40, C41), the oral-gut-brain row (C42), the nutritional therapist's quote (C84, C85) and "feel the repair" (C98), with the replacement lines from CR1?
- (a) Yes, replace them with the CR1 lines.
- (b) No, keep them.
- *Advice*: (a): they make health effects a cosmetic may not claim (EU 655/2013); the CR1 replacements use existing site copy.

**22. Research cards on tooth decay (C62) and canker sores (C64) (K4).** Both cards report a disease result. The figures match the studies, but next to a cosmetic they read as "prevents tooth decay" and "prevents ulcers". Keep them?
- (a) Remove both cards.
- (b) Keep them with the softened CR1 wording, after a legal check.
- *Advice*: (a): the safest for launch; (b) needs the regulatory reviewer first.

**23. Missing sources (K5).** Some lines need a document we do not have: the CPSR conclusion for leave-on use, the SCCS opinion SCCS/1677/25, the practitioners' consent and a dated count, the review-platform figure, the packaging specifications. Kulal 2016 (the 98% card) is now found and checked, see the claims report.
- (a) You (Victor) provide the documents.
- (b) Hide the lines until a source exists.
- *Advice*: (b) now, (a) when the documents are at hand; each line comes back as soon as its source is in the library.

**24. Week headings of the PDP treatment journey (K6).** The journey promises outcomes per week ("week 2: calmer gums …"). Timed member outcomes have no data. Remove the week headings?
- (a) Remove the week headings, keep the untimed lines.
- (b) Keep them.
- *Advice*: (a): the lines themselves are supportable without the timeline.

**25. Leen Ponet's quote (K7).** Her English quote is a draft translation she has not approved. Ask her to approve the EN, NL and FR?
- (a) Yes, ask her.
- (b) No.
- *Advice*: (a): it is her name on the page; until she answers, the quote stays as it is in EN.

**28. regulatory.md wins over products.md (S4).** Where products.md allows a claim that regulatory.md forbids (no prevention claims), which wins?
- (a) regulatory.md wins, and products.md is corrected.
- (b) No.
- *Advice*: (a): the review already works that way; the source files should agree.

**36. Sietske Hamelink's quote in NL and FR.** Her quote is her own words and carries an unsupported health claim (C85). The NL is held; FR translated it. What should NL/FR show?
- (a) Ask Sietske to approve the NL/FR (NL draft in `986c1d9`).
- (b) Show her English quote on NL/FR.
- (c) Replace it with a quote of hers without the health claim (ties to K3).
- *Advice*: (c): the claim is the problem in every language; with (a) it would still be there.

**52. Releasing the nano-hydroxyapatite article in NL and FR.** You rewrote six fields of the article today and kept the rest of its EN as it is. Its claim blocks stay gated in NL and FR (pending-claim-review), so the article is not registered. Release them?
- (a) Release the whole article: NL/FR then carry the same claims as the EN.
- (b) Release only the fields you rewrote today and the blocks without a claim; keep the rest gated.
- (c) Keep it gated until the claims review.
- *Advice*: (b): "medical marvel … bones and overall health", "first discovered by NASA" and "chemicals that prevent natural healing" are the kind of claims EU 655/2013 does not allow a cosmetic; translating them spreads them to two more languages. The article is in batch 07, outside the first wave, so nothing waits on it for launch.

**Two research cards checked against the papers (22 Oct, at Victor's request).** No status changes until Victor decides.
- **C63, Vano et al. 2018** (Clin Oral Investig, PMID 28361171). The authors' conclusion does not say nHAp is better than fluoride: *"The application of nano-hydroxyapatite in gel toothpaste fluoride free is an effective desensitizing agent providing relief from symptoms after 2 and 4 weeks."* The results do report lower sensitivity than the fluoride and placebo groups at 2 and 4 weeks (p < 0.05). A 2 % gel applied for 10 minutes twice a day, 105 adults, not Karmicare. "Beat fluoride" is a fair reading of the results, not the authors' conclusion; brand don't #13 is what holds the card. The library summary ("OUTPERFORMED", "superior") goes further than the authors.
- **C60, Kulal et al. 2016** (J Clin Diagn Res 10(10):ZC51–ZC54, PMC5121804). Found and read. Table 2: 97.62 % of tubules completely occluded with nHAp, 81.9 % NovaMin, 65.42 % Pro-Argin; the site's 98 / 82 / 65 are these figures rounded, so they come from a peer-reviewed paper, not a whitepaper. In vitro, 10 dentine discs per group, a slurry for 2 minutes a day over 7 days. Only nHAp vs Pro-Argin is significant (p = 0.005); nHAp vs NovaMin is not (p = 0.235). The paper is inconsistent: its abstract gives 98.1 / 83.1 / 69.1 % and 15 % nHAp, Table 1 gives 1 % nHAp (Acclaim). Advice: keep the card as a lab study ("in a lab study"), and drop the 82 % comparison or say it was not significant.

**Changelog.** 22 Oct: this status block added at Victor's request (via the landing desk). 22 Oct, later: rows 12 and 13 landed in merchant-edit `2ef9b5c`; rows 39, 51 and 52 for Victor's admin edits of that day.

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

**Homepage FAQ update (21 Oct, integration `41ae772`).** The homepage lane rewrote the FAQ, so three CR1 rows are no longer on the homepage:
- C13 and C93: the row `faq_item_qUxYCn` now asks about the money-back guarantee;
- C23: the row `faq_item_AL3DKF` now holds the fluoride-free answer;
- C24: the block `faq_item_4KMG6C` is removed, and its entries are retired.

The CR1 rewordings for C13, C23 and C24 therefore no longer change homepage text. C24's onboarding line and C93's admin FAQ fields remain. Two new claims, which CR1 has not reviewed, sit in disabled FAQ blocks: C101 (fluoride and nHAp compete for the enamel surface) and C102 (fluoride's benefits do not outweigh its drawbacks, close to don't #13).

The NL claim hold for batches 01–03 is now 75 entries:
- 61 that the K-decisions release;
- 12 that wait on documents;
- 2 waiting on a verdict for C101 and C102.

FR follows once it re-translates the changed entries.

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
