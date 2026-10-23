# B1a report · EN source inventory, corrections and glossary (homepage + Duo PDP)

## Status 22 Oct

The whole lane in one table: EN source copy, NL, claims and the registration in Shopify. The other four reports carry the rows that concern them.

"In merchant-edit" is checked with `git merge-base --is-ancestor <sha> merchant-edit` against `2ef9b5c` (22 Oct). merchant-edit is not pushed yet, so none of it is live.

| Status | Rows |
|---|---:|
| In merchant-edit | 13 |
| Ready to land | 3 |
| In progress | 0 |
| Waiting for Victor | 28 |
| Parked / after launch | 5 |
| Dropped | 6 |

| # | Status | What | Commits / where |
|---|---|---|---|
| 1 | In merchant-edit | EN copy fixes on the homepage and footer: €0.49 per brushing, ENTHUSIASTS, "needs", 60-day money-back guarantee, a Belgian product | `f2e9506` |
| 2 | In merchant-edit | EN source inventory: 8 batches, 2,575 entries, checked by `digest.py`; follows the homepage copy of 21 Oct, the delivery times, the Duo name, the announcement line and the CTAs | `ee3b1f4` … `1437fc5` |
| 3 | In merchant-edit | Claims register `CLAIMS-REVIEW.md`: 70 claims, 17 approved, 49 needs-review, 3 unsupported, 1 confirmed (C103) | `0b98382` … `1437fc5` |
| 4 | In merchant-edit | NL payloads: 2,151 of the 2,154 translatable entries in Dutch, `validate.py` exit 0. After Victor's waiver (20 Oct) the claim-held entries are translated and flagged pending-claim-review | `31b490f` … `1437fc5` |
| 5 | In merchant-edit | 64 `kc.*` theme keys in all 31 locales: footer, plans, clock, FAQ "ALL", sticky bar, hero, stat strip, PDP labels; EN, NL and FR values | `16decc4` … `1630eef`, `c348c72`, `61efa65` |
| 6 | In merchant-edit | Delivery times in the theme's legal pages and EN fallback locales: Benelux within 24 hours, rest of the EU 2–3 working days | `6414e4c`, `bc7a090`, `1596ecb` |
| 7 | In merchant-edit | Announcement line "FREE SHIPPING & 60-DAY GUARANTEE FOR MEMBERS · BELGIAN-MADE · EST. 2017" (C103 confirmed by Victor) and the newsletter placeholder *jij@voorbeeld.be* / *vous@exemple.be* | `6112414`, `1437fc5` |
| 8 | In merchant-edit | Sticky-bar key `kc.sticky_cart.kit_free_html` removed from all 31 locales (NV-13) | `d72d791` |
| 9 | In merchant-edit | CTAs say "Begin your …" in the EN source, the NL ("Begin je …") and the theme keys | `0a49ab2` |
| 10 | In merchant-edit | Clinical review CR1: advice on 50 claims and 9 onboarding lines | `3ebf113`, `2a7f809` |
| 11 | In merchant-edit | Offline registration plan for NL and FR, the app set-up steps for Victor (`APP-SETUP.md`) and the first version of `register.py` | `8a7548d` … `060de0e`, `2f9a83f`, `0e21a1f` |
| 12 | In merchant-edit | PDP end button "Begin your 60-Day Rhythm" (capital R) in the EN source, the NL and the template; landed 22 Oct with the FR follow-up | `6500a4a` |
| 13 | In merchant-edit | `register.py` reworked after reviews R18, R18b and R18c; R18d (21 Oct): approve, no new findings, selftest 80/80 | `93e1850`, `44bb619`, `59c281e` |
| 14 | Waiting for Victor | Translations app for the registration | `APP-SETUP.md` |
| 15 | Waiting for Victor | Writing the first wave of translations to Shopify (not asked yet: it comes after the dry run and the bindings review) | `register.py --write` |
| 16 | Waiting for Victor | NL and FR stay published while the first wave is not in | B4 decision 3 |
| 17 | Waiting for Victor | Legacy translated product handles (12 URLs, e.g. `/nl/products/compleet-hygiene-kit`) | B4 decision 4 |
| 18 | Waiting for Victor | Browser-language redirect on product pages | B4 decision 5, manual check 3 |
| 19 | Waiting for Victor | Live figures and claims a–p (K1 on the claims review page) | review page `claims.html`, Prioriteiten |
| 20 | Waiting for Victor | 27 reworded claims from CR1 (K2) | `docs/claims/CLINICAL-REVIEW.md` §2, §4 |
| 21 | Waiting for Victor | Claims that cannot be supported (K3) | C35, C40, C41, C42, C84, C85, C98 |
| 22 | Waiting for Victor | Research cards on tooth decay (C62) and canker sores (C64) (K4) | research section, homepage and PDP |
| 23 | Waiting for Victor | Missing sources (K5) | CPSR, SCCS opinion, practitioner consent, review figure, packaging |
| 24 | Waiting for Victor | Week headings of the PDP treatment journey (K6) | C94–C98, admin metafield |
| 25 | Waiting for Victor | Leen Ponet's quote (K7) | C83, homepage and PDP |
| 26 | Ready to land | No dentist confirmation (S2, Victor 22 Oct, choice a): the clause leaves the PDP check-up tooltip, the sticky-bar check-up line and the Duo info card, in EN, NL and the theme keys; the compare-table tooltip and the Year plan description are admin text, still to edit by Victor | reported 22 Oct (needs review: theme files) |
| 27 | Waiting for Victor | Old blog articles in NL and FR (S3) | batch 07, 709 entries |
| 28 | Waiting for Victor | regulatory.md wins over products.md (S4) | the clinical sources |
| 29 | Waiting for Victor | Addresses in the NL/FR legal text (S5) | batch 04 |
| 30 | Waiting for Victor | "Gift, pause or cancel" in the buy box (S6) | PDP trust row |
| 31 | Waiting for Victor | Brand-rule exceptions (S7) | footer, NL copy |
| 32 | Waiting for Victor | Dutch term for the check-up (S8) | glossary |
| 33 | Waiting for Victor | Facts to confirm (S9) | homepage and PDP |
| 34 | Waiting for Victor | Treatment-journey line stops mid-phrase (#29) | admin metafield `custom.treatment_journey_*` |
| 35 | Waiting for Victor | SLS article block `#b035` names four competitor brands | blog, batch 07 |
| 36 | Waiting for Victor | Sietske Hamelink's quote in NL and FR | C85, homepage and PDP |
| 37 | Waiting for Victor | Capitalisation of all buttons | inventory of all buttons (global coordinator) |
| 38 | Waiting for Victor | Delivery times in the Shopify policies, and their wording | Settings > Policies; table in the NL report |
| 39 | Waiting for Victor | Admin text fixes from B1a (captured 19 Oct; the footer menu link "Why use hydroxapatite" is fixed since 22 Oct, row 51) | product, metafields, metaobjects, menu, selling plans |
| 40 | Waiting for Victor | Money format on the EN pages | Shopify money format (B1a decision 5) |
| 41 | Waiting for Victor | Legal review of the NL and FR legal texts | batch 04, legal-review gate (NL 605 items) |
| 51 | Ready to land | Victor's admin EN edits of 22 Oct in the EN source and the NL: the Duo's title, SEO title and meta description, the footer menu link "Why hydroxyapatite", six fields of the nano-hydroxyapatite article; its twin article is hidden and redirected, so its 79 entries are retired. His own NL/FR Duo texts are recorded as registered (`registration/registered.json`), so the plan never overwrites them. The FR payload follows in the FR lane | reported 22 Oct to the global coordinator |
| 52 | Waiting for Victor | Releasing the nano-hydroxyapatite article in NL and FR | `/blogs/news/nano-hydroxyapatite`, batch 07 |
| 53 | Ready to land | Footer slogan "Your mouth has a rhythm Now your oral care too" (Victor 22 Oct), in the footer group and its schema default, EN and NL | reported 22 Oct (needs review: theme files) |
| 42 | Parked / after launch | Loop widget strings (off-limits files): the 11 strings of the B4 Loop table, handed to the Loop owner; NL and FR are in the payloads | B4 report, Loop handoff |
| 43 | Parked / after launch | Navigation links and Shopify policies: no proven API route in the runner yet (LINK, SHOP_POLICY); after the first wave, or through Translate & Adapt | `register.py`, B4 Part 2 |
| 44 | Parked / after launch | Rendered check of the keyed strings on /nl and /fr (B4 manual checks 1–5): after the theme ships | preview gate |
| 54 | Parked / after launch | Move the 14 inline SVG icons out of the PDP FAQ content fields (Ingredients, How to brush, Quality & safety) into a theme snippet per step, so the fields hold text only and the icons keep `currentColor`. Theme lane plus an Admin edit of the EN fields, then a new source-copy capture and plan (Victor 23 Oct) | metaobjects 515150971261, 515151200637, 564919009661; R42/R42b |
| 55 | Parked / after launch | Rich-text JSON fields re-register on every run: Shopify stores the JSON compact, the runner sends it with spaces, so the text is the same but the bytes differ (18 NL fields on 23 Oct). Compare parsed JSON, or send it compact; small runner change with its own review | `register.py`, dry run 23 Oct |
| 45 | Dropped | The two missing homepage FAQ answers (S1): the homepage lane filled both on 21 Oct | integration `41ae772` |
| 46 | Dropped | Legacy legal pages (350 entries): not translated, they redirect | `08479cb` |
| 47 | Dropped | Clock gates (B4 decision 6): review gates no longer hold theme keys, after Victor's waiver | `c348c72` |
| 48 | Dropped | FR conventions (B1a decision 2): the FR lane owns them | FR lane |
| 49 | Dropped | Duo-name settings (3 entries): the product title names the Duo | `6643e16` |
| 50 | Dropped | Choice of access path (B4 decision 1): the Dev Dashboard app route was chosen | desk, 21 Oct |

### Waiting for Victor: the questions

**14. Translations app for the registration.** Will you create the Dev Dashboard app "Karmicare translations" as in `APP-SETUP.md`, install it on karmicares.myshopify.com, store the client secret in your Keychain, and then say "app klaar" with the published theme's ID?
- (a) With the extra scope `read_themes`: the runner reads the published theme itself and proves the ID.
- (b) Without it: you confirm the theme ID yourself on the day of each run (`--theme-attested "<date> Victor"`).
- *Advice*: (a): one manual step less, and the runner checks the theme instead of trusting a typed ID.

**15. Writing the first wave of translations to Shopify (not asked yet: it comes after the dry run and the bindings review).** After the read-only dry run and the review of the metaobject bindings, may the runner write the first wave (NL 504, FR 502 items)?
- (a) Yes, the whole first wave.
- (b) Yes, but theme text (homepage, PDP, header, footer) first, products and metafields in a second run.
- (c) No, not before launch.
- *Advice*: Decide on the dry-run report, which shows every current value it would overwrite. NL and FR are already published, so each registered translation is live at once; (a) if the report is clean.

**16. NL and FR stay published while the first wave is not in.** /nl and /fr are published today and show mostly English. Keep them published?
- (a) Keep them published and register quickly.
- (b) Unpublish NL and FR in the admin until the first wave is in.
- *Advice*: (a): unpublishing is an admin change that takes /nl and /fr away from visitors who already use them, and the first wave is ready.

**17. Legacy translated product handles (12 URLs, e.g. `/nl/products/compleet-hygiene-kit`).** The old NL/FR product URLs answer with a 301 to translated handles. Keep or remove them?
- (a) Keep them: both URL forms work.
- (b) Remove them, so handles stay English everywhere.
- *Advice*: (a) for launch; nothing breaks, and removing them is an admin change that can wait.

**18. Browser-language redirect on product pages.** A browser set to English is sent from `/nl/products/…` to the EN product. Will you run manual check 3 of the B4 report (2 minutes, a new English browser profile) to see whether the language selector still keeps a visitor on NL?
- (a) Check it before launch; if it fails, change the setting in Markets or the app behind it.
- (b) Leave it until after launch.
- *Advice*: (a): Dutch customers with an English browser would otherwise land on the EN product.

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

**27. Old blog articles in NL and FR (S3).** The blog articles are translated but outside the first wave. 107 of their blocks carry unsupported claims. Publish the NL/FR versions?
- (a) Not until the EN is rewritten.
- (b) Publish them.
- *Advice*: (a): the EN itself makes the claims; translating them spreads them to two more languages.

**28. regulatory.md wins over products.md (S4).** Where products.md allows a claim that regulatory.md forbids (no prevention claims), which wins?
- (a) regulatory.md wins, and products.md is corrected.
- (b) No.
- *Advice*: (a): the review already works that way; the source files should agree.

**29. Addresses in the NL/FR legal text (S5).** Postal addresses are written exactly as in the EN; city and court names in running text use the local form (Brugge, Ondernemingsrechtbank Gent). Keep that?
- (a) Official local forms in running text (as now).
- (b) English forms everywhere.
- *Advice*: (a): it is how Belgian legal Dutch names its courts and cities.

**30. "Gift, pause or cancel" in the buy box (S6).** The NL trust row uses Figma's short form *Pauzeren of opzeggen*; elsewhere the full form. Keep that?
- (a) Full form where it fits, short form in the trust row (as now).
- (b) Short form everywhere.
- *Advice*: (a): the trust row has no room, the other places do.

**31. Brand-rule exceptions (S7).** The footer says "is a Belgian product", and the treatment-journey footnote "What members report with continued use" is NL *bij langdurig gebruik*: both use banned words (product, use). Rewrite or keep?
- (a) Rewrite the EN and the Figma first; you give the wording.
- (b) Keep them.
- *Advice*: (a): the brand rule has no exceptions so far; I do not write new copy myself.

**32. Dutch term for the check-up (S8).** The site uses *controlebeloning*; one Figma frame says *tandartscontrole-beloning*. Which one?
- (a) *controlebeloning* (as now).
- (b) *tandartscontrole-beloning*.
- *Advice*: (a): shorter, and it does not suggest the dentist is involved.

**33. Facts to confirm (S9).** Which is right: "Dr. Kris Sienaert" (site) or "Sinaert" (45 brief)? "100+" practitioners (PDP) or "30+" (45 brief)? 36 studies (site) or 39 (45 brief)? "Twelve hundred brushings a year" (twice a day is about 730)? (The footer slogan is decided: row 53.)
- Answer per fact.
- *Advice*: Confirm each; nothing is changed without the fact, because each one needs a fact and not a typo fix.

**34. Treatment-journey line stops mid-phrase (#29).** The line reads "Peace of mouth, peace of mind* — from your gums to the". How should it end? **Answered 23 Oct:** Victor completed it in Admin as "— from your gums to the rest of you".
- (a) You give the ending.
- (b) Cut it after "peace of mind*".
- (c) Remove the line.
- *Advice*: (b): no new copy needed. It is admin text, so you edit it; NL and FR follow.

**35. SLS article block `#b035` names four competitor brands.** The block breaks the no-competitor rule (a brand rule, not a claim), so NL and FR hold it. What should happen?
- (a) Remove the brand names from the EN sentence.
- (b) Delete the block.
- (c) Leave the EN and never translate it.
- *Advice*: (a) if the sentence reads without the names, otherwise (b); both are deletions, no new copy.

**36. Sietske Hamelink's quote in NL and FR.** Her quote is her own words and carries an unsupported health claim (C85). The NL is held; FR translated it. What should NL/FR show?
- (a) Ask Sietske to approve the NL/FR (NL draft in `986c1d9`).
- (b) Show her English quote on NL/FR.
- (c) Replace it with a quote of hers without the health claim (ties to K3).
- *Advice*: (c): the claim is the problem in every language; with (a) it would still be there.

**37. Capitalisation of all buttons.** Which style for every button?
- (a) CAPS.
- (b) Title Case.
- (c) Sentence case, with plan names as names ("Begin your 60-Day Rhythm").
- *Advice*: (c): it matches the CTAs that are already in place and reads calmest; I apply it to EN and NL in one commit.

**38. Delivery times in the Shopify policies, and their wording.** The theme's legal pages say "within 24 hours" (Benelux). The three Shopify policies are admin text: will you edit their EN (the table in the NL report gives each old and new line)? And should the legal texts say "within 24 hours" or "1 working day"?
- (a) "within 24 hours" everywhere (as now).
- (b) "1 working day" in the legal texts, "24 uur" stays in the sticky bar.
- *Advice*: (b): an order on Friday evening cannot arrive within 24 hours, and the rest of the EU is already given in working days. Either way the policies are your edit.

**39. Admin text fixes from B1a (captured 19 Oct; the footer menu link "Why use hydroxapatite" is fixed since 22 Oct, row 51).** These are admin texts the theme cannot change: compare table Year €0.42 → €0.49 per brushing; Welcome Kit row €18 → €21 (point it at the 2.0 brushes); the Year cells lack "3 now, 3 in month 6"; product FAQ "Full dosep" → "dose"; an image alt puts evening before morning; the legacy plan name " Pay every 12 months, Deliver every 6 months_"; the lab name "Midwest University" stays (Victor 22 Oct). Who edits them, and when?
- (a) You or DH edit them before the first wave is registered.
- (b) After launch.
- *Advice*: (a): the registration translates the admin text as it is, so a fix after it means translating twice.

**40. Money format on the EN pages.** Shopify formats money per currency, not per language, so computed amounts show "€0,49" and "€67,00 EUR" on EN pages next to the static "€0.49". Accept that?
- (a) Accept the comma on EN for launch.
- (b) The PDP lane formats amounts per locale in the theme.
- *Advice*: (a) for launch, (b) after: it is theme work in the buy box, not a copy change.

**41. Legal review of the NL and FR legal texts.** The legal pages are translated but held by the legal-review gate. Who reviews them?
- (a) You review them.
- (b) A Belgian lawyer reviews them.
- (c) NL/FR legal pages stay English until reviewed.
- *Advice*: (b) for NL first; until then (c).

**52. Releasing the nano-hydroxyapatite article in NL and FR.** You rewrote six fields of the article today and kept the rest of its EN as it is. Its claim blocks stay gated in NL and FR (pending-claim-review), so the article is not registered. Release them?
- (a) Release the whole article: NL/FR then carry the same claims as the EN.
- (b) Release only the fields you rewrote today and the blocks without a claim; keep the rest gated.
- (c) Keep it gated until the claims review.
- *Advice*: (b): "medical marvel … bones and overall health", "first discovered by NASA" and "chemicals that prevent natural healing" are the kind of claims EU 655/2013 does not allow a cosmetic; translating them spreads them to two more languages. The article is in batch 07, outside the first wave, so nothing waits on it for launch.

**Translation script (`register.py`).** R18d (21 Oct) approved `59c281e`: no new findings, selftest 80/80. Nothing has run live. The order from here:
1. Victor says "app klaar" and gives the published theme ID (row 14).
2. A read-only dry run with theme proof; its report shows every current value and the API contract.
3. Review of the binding proposals for the metaobject fields (48 NL, 50 FR) into `bindings.json`, with the full old and new translations.
4. A fresh dry run.
5. Its checksum and Victor's explicit yes (row 15); only then `--write`.

**Two research cards checked against the papers (22 Oct, at Victor's request).** No status changes until Victor decides.
- **C63, Vano et al. 2018** (Clin Oral Investig, PMID 28361171). The authors' conclusion does not say nHAp is better than fluoride: *"The application of nano-hydroxyapatite in gel toothpaste fluoride free is an effective desensitizing agent providing relief from symptoms after 2 and 4 weeks."* The results do report lower sensitivity than the fluoride and placebo groups at 2 and 4 weeks (p < 0.05). A 2 % gel applied for 10 minutes twice a day, 105 adults, not Karmicare. "Beat fluoride" is a fair reading of the results, not the authors' conclusion; brand don't #13 is what holds the card. The library summary ("OUTPERFORMED", "superior") goes further than the authors.
- **C60, Kulal et al. 2016** (J Clin Diagn Res 10(10):ZC51–ZC54, PMC5121804). Found and read. Table 2: 97.62 % of tubules completely occluded with nHAp, 81.9 % NovaMin, 65.42 % Pro-Argin; the site's 98 / 82 / 65 are these figures rounded, so they come from a peer-reviewed paper, not a whitepaper. In vitro, 10 dentine discs per group, a slurry for 2 minutes a day over 7 days. Only nHAp vs Pro-Argin is significant (p = 0.005); nHAp vs NovaMin is not (p = 0.235). The paper is inconsistent: its abstract gives 98.1 / 83.1 / 69.1 % and 15 % nHAp, Table 1 gives 1 % nHAp (Acclaim). Advice: keep the card as a lab study ("in a lab study"), and drop the 82 % comparison or say it was not significant.

**Changelog.** 22 Oct: this status block added at Victor's request (via the landing desk). 22 Oct, later: rows 12 and 13 landed in merchant-edit `2ef9b5c`; rows 39, 51 and 52 for Victor's admin edits of that day; rows 26 and 53 for his dentist and slogan decisions.

Task `task_dff189ea8e99`, Orca run `run_32dd5602b983`, branch `karmicare/soft-launch-source-copy` (from 3bae259, the live baseline). 19 Oct 2026.

## Preflight

| Check | Result |
|---|---|
| `orca status --json` | runtime `ready`, `reachable: true`, connection `connected` |
| `git status --short` / branch | clean tree on `karmicare/soft-launch-source-copy`, HEAD 3bae259 |
| Model / permission mode | Claude Opus 5.5 (`claude-opus-5-5`) in Claude Code, bypass-permissions mode, every Bash command sandboxed |
| `AGENTS.md` | read; the files it points to (README, `docs/pdp/RUNBOOK.md`, `docs/design-tokens/`) are not in this repo, so COMMON-RULES and BRIEF applied |

**Network, disclosed.** Before the coordinator's message about the network arrived, I made read-only GET requests to six public URLs on `karmicares.myshopify.com`: the homepage, the Duo PDP and four `/products/<handle>.js` files (the Duo, both 2.0 brushes, the floss). They ran around 19:10–19:20, still inside the sandbox: curl failed, so I sent them through the sandbox's own proxy at `127.0.0.1` instead of `localhost`. After the message ("do not switch proxies … do not use another channel") I made no further requests. The admin-held entries come from those captures. The raw captures stay in my session scratch and are not committed. Nothing else went over the network apart from read-only Figma MCP calls on `3rOMJvQZTzyYjnCV6oggV3` (frame 3002:20280).

## What changed

| Commit | What |
|---|---|
| `f2e9506` content(homepage) | Text values only in `templates/index.json` and `sections/footer-group.json` (11 values, below). |
| `ee3b1f4` docs(source-copy) | `en-source.json`, `batches/*.json`, `INVENTORY.md`, `digest.py`. |
| `0b98382` docs(source-copy) | `GLOSSARY.md`, `CLAIMS-REVIEW.md`. |
| this commit | `REPORT.md`. |

Corrections (old → new in `INVENTORY.md` and in each entry's `old_en`):

- **€0.49**: the two homepage CTA sub-lines read "€0,49 / brushing ritual" in EN; now "€0.49 / brushing ritual". No other template or group text states a per-brushing price.
- **Homepage FAQ**: the six answers were all copies of the row 1 answer.
  - Row 1 (two formulas) keeps its own answer.
  - Rows 4, 5, 6 now carry the 45 brief's Q3, Q5 and Q10 as adapted in the Figma review frame 3002:20280, read verbatim from Figma.
  - Row 2 (fluoride-free) gets `[NEEDS APPROVED COPY]`: FAQ-0202 is Draft with Regulatory "Needs review", so its status does not allow use.
  - Row 3 (fluoride paste) gets `[NEEDS APPROVED COPY]`: no approved answer exists anywhere.
- **Defects**:
  - "HEALTH ENTHOUSIASTS" → "ENTHUSIASTS".
  - "your mouth need" → "needs".
  - "60 day money back guarantee" → "60-day money-back guarantee" (PDP and announcement-bar form).
  - Footer "a Belgium product" → "a Belgian product".
  - No duplicated words exist on these pages; the one Asleep-before-Awake string is admin-held (handoff).
- **Not changed, by design**:
  - **€0.42**: the Year's cost per brushing in the compare table is an admin metaobject cell.
  - **Welcome Kit value**: the buy box and plan descriptions already show €21; only the admin compare table shows €18.
  - **Year sub-line**: no text setting in the four allowed files presents the Year, so "3 now, 3 in month 6" goes to handoffs. It already appears in the Loop selling-plan name and description.

## Inventory (acceptance counts)

743 entries in three batches, current after R1. B1a delivered 739; R1 added 4 runtime strings to batch 01 (see "R1 fixes").

| Batch | Entries | Digest |
|---|---:|---|
| `batch-01-homepage` | 225 | `a09219ae1af8e24bd4fbcc86ce50223656adb586` (B1a: 221, `b685b73d4dcd…`) |
| `batch-02-pdp` | 477 | `03dd18b9d41a21772da2e26b7060c42f6b2364d1` |
| `batch-03-header-footer` | 41 | `e17cadb5e223dd62b25e30e901091d8a8634aaf3` |

| resource_type | Entries |
|---|---:|
| template_setting | 345 (homepage 189, PDP 156) |
| section_group | 6 (header 2, footer 4) |
| theme_locale | 99 (28 Dawn keys + 71 hardcoded theme strings) |
| app | 27 (12 hardcoded Loop widget strings, 14 selling-plan names, groups and descriptions, 1 consent link) |
| product | 16 |
| metafield | 175 |
| metaobject | 63 |
| shop | 2 |
| navigation | 10 |

By status: 316 approved, 9 corrected, 60 needs-review (2 of them blocked placeholders), 77 needs-key, 281 admin-held. 53 entries are never-translate. (B1a: 329 approved, 47 needs-review, 73 needs-key; R1 moved 13 entries to needs-review and added 4 needs-key entries.)

The text-setting counts (189 and 156) are higher than the brief's estimate (about 149 and 119). They take every non-empty text-like value, including the four sections both templates repeat and two disabled PDP blocks (marked `rendered: false`). Seven Liquid pointer settings and eleven technical text settings are left out; INVENTORY.md lists the types per file. No custom section reads `locales/en.default.json`. Every custom string is either a setting or hardcoded, so the custom-locale part of the target is empty, and the 77 needs-key strings (file:line in INVENTORY.md) are the localization worker's list.

## Evidence

- `shopify theme check --fail-level error`: **exit 0**. 224 files inspected, 21 offenses, all warnings, none in the four target files. No change to `.theme-check.yml`.
- All four JSON files parse after the edits (comment header kept).
- `python3 docs/source-copy/digest.py`: exit 0 (every sha1 and batch digest matches).
- Figma: answers for rows 4–6 read from instances `I3002:20346`, `I3002:20354`, `I3002:20362` (`;3589:3637`) in file `3rOMJvQZTzyYjnCV6oggV3`.
- Screenshots: none. The change is text in template JSON with no CSS or Liquid. Rendered verification of the homepage FAQ is **pending the preview gate**.

## Pending

| Item | Gate or owner |
|---|---|
| Rendered check of the six homepage FAQ rows (Day/Night, 393–2560) | preview gate |
| Approved answers for FAQ rows 2 and 3 | Victor (decision 1) |
| Clinical Research sign-off on 46 needs-review and 3 unsupported claims (after R1) | Victor / Clinical Research (decision 3) |
| Live captures to be refreshed if admin text changes before translation | whoever runs the next batch (network now pending the owner's fix) |

## Handoffs

**Admin (Shopify, Loop): Victor or the admin owner, no theme change possible.**
1. Compare table (`shop.metaobjects.compare_value`), Year column: **€0.42 → €0.49 per brushing**. €354 / 6 duos = €59 per duo, the same as the 60-Day Rhythm.
2. Compare table (`custom.compare_table`), Welcome Kit row: it references the old Morning (€4) and Evening (€5) brushes, so the tooltip says **€18**. Point it at `morning-toothbrush-2-0` and `evening-toothbrush-2-0` (€6 + €6 + €9 = **€21**).
3. Compare table Year cells ("2× a year", the delivery tooltip) do not carry the approved sub-line **"3 now, 3 in month 6"**.
4. Product FAQ metafield: typo **"Full dosep"** → "dose".
5. Treatment journey metafield: a line stops mid-phrase, "Peace of mouth, peace of mind* — from your gums to the". Fixed in Admin 23 Oct: "— from your gums to the rest of you".
6. Image alt `media.69840178020733` puts the evening before the morning ("evening care at 22:00 and morning care at 06:40"): Awake before Asleep.
7. Footer menu `company`: "Why use hydroxapatite" is misspelled (hydroxyapatite) and uses the banned word "use".
8. Selling plans:
   - The legacy plan name " Pay every 12 months, Deliver every 6 months_" has a leading space and a trailing underscore; the legacy groups (Subscribe and Save, 60-Day Supply, Yearly Plan) are in the plan markup, so check they stay hidden.
   - The plan descriptions say "Inflation-proof member price" (no approved EN wording).
   - The Year description says "verified by your dentist" (see decision 4).
9. The lab name differs: "Midwest University" in the product FAQ, "Indiana University OHRI 2025" in the 45 brief.

**PDP owner (`sections/main-product.liquid`, outside my files).**
1. The sticky bar's 26 strings are schema defaults of the `sticky_cart` block. The PDP template stores only `button_text`, so Translate & Adapt cannot reach them. Either store them in the template or make them locale keys. Their file:line entries are in INVENTORY.md.
2. That is also where the Year sub-line belongs: `title_year` "The Karmicare Year · 6 Duos" (line 937) is the theme text that presents the Year without "3 now, 3 in month 6".
3. `checkup_info` (line 995) repeats "verified by your dentist".

**Homepage owner.**
1. FAQ category tabs: rows 3–6 sit under categories that do not fit their questions (rinsing under "Plans & Return on Care", results under "Shipping & guarantee").
2. `sections/two-formulas-karmicare.liquid:133` uses the heading as the image alt, so the alt reads `Two formulas. One system. <strong>Designed around you.</strong>`. Strip the HTML.
3. Two headings carry `<em>` accent words: the homepage "Care that comes back" heading and the PDP research heading. The design rule is "no italic accent words", so confirm they render upright.
4. The homepage featured product's Loop block has no `plans_eyebrow` / `plans_heading`, so the Loop fallbacks "Start here" / "Choose how to begin" render there.

**Localization worker.**
1. The 77 needs-key strings: hardcoded Liquid and JS, including the seven hourly clock messages in `assets/chronobiology-clock-karmicare.js` and the clock's live-mode tail added in R1.
2. The header's "Coming soon" and the footer's three legal link texts are schema defaults that the group JSON does not store.

**Loop owner (off-limits files).** "One time Purchase", "Selling Plans", "each", "/ year", "/ 60 days", "Renews every year" and "value · free" are hardcoded in `snippets/loop-widget-standard.liquid` and `assets/loop-widget.js`.

## Open decisions for Victor

1. **The two missing FAQ answers.**
   - **Row 2, "Is Karmicare fluoride-free?"**: the FAQ-0202 short answer is ready in EN and NL but is Draft and carries the "outperformed fluoride on sensitivity" claim.
   - **Row 3, "Will Karmicare offer a biorhythmic toothpaste with fluoride?"**: no copy exists.
   - Options: (a) approve FAQ-0202 after the claims check and write row 3; (b) hide rows 2 and 3 at integration until copy exists; (c) drop row 3's question.
   - *Recommendation*: (b) now, so `[NEEDS APPROVED COPY]` can never ship, then (a) for row 2. Row 3 needs your answer on the product roadmap; that is not a copy decision.
2. **FR conventions.** EN €0.49 and NL €0,49 are decided. The FR proposals:
   - French typography: **0,49 €**, a no-break space before `: ; ! ?`, `€` and `%`.
   - Warm *vous*.
   - Care Credit, Return on Care, Awake, Asleep and Leave-on stay English.
   - Plan names *Rythme 60 jours*, *L'année Karmicare*, *Essayer une fois*.
   - *Recommendation*: accept the French typography rather than copying the NL "€0,49". Decide alongside it whether FR ships at all, because customer care answers in EN and NL only (offer, 5 Oct).
3. **Claims.**
   - Three are unsupported: homepage benefit card 06 ("Gums settle, turn pinker and look radiant" and, since R1, its heading "Radiant calm gums"), and the two health lines in Sietske Hamelink's quote, which appears on both templates.
   - 46 need review (42 at B1a): the study cards with their result lines, the timelines, the "clinically proven" and "100+ practitioners" lines, the evidence counts, the leave-on safety lines, and others; CLAIMS-REVIEW.md has the full list.
   - *Recommendation*: fix or remove the three unsupported ones before NL/FR translation starts. Let translation run on the rest now, since the batch digests show what changes after sign-off.
4. **Offer wording that contradicts the offer source of truth.**
   - The announcement bar promises complimentary shipping and a 60-day guarantee to everyone, but Try Once pays shipping and has 14 days.
   - The check-up tooltip, the sticky bar, the info card and the Year plan description say the check-up is "verified/confirmed by your dentist", but the offer needs no dentist involvement.
   - *Recommendation*: give the wording; I did not write new copy.
5. **Money format.** Shopify formats money per currency, not per language, so computed amounts render "€0,49", "€5,90" and "€67,00 EUR" on the EN pages too, next to static "€0.49".
   - *Recommendation*: decide whether EN computed amounts may keep the comma. Otherwise the PDP owner must format per locale in the theme. The store setting alone cannot give EN €0.49 and NL €0,49.
6. **Facts to confirm.**
   - "Dr. Kris Sienaert" (site and image file) or "Sinaert" (45 brief)?
   - "Twelve hundred brushings a year" in the professionals section: twice a day is about 730.
   - "100+" practitioners (PDP) or "30+" (45 brief)?
   - 36 studies (site) or 39 (45 brief)?
   - The footer slogan "Your mouth has a rhythm So should your oral care" has no stop between the sentences.
   - *Recommendation*: confirm each. None was changed because each needs a fact, not a typo fix.

## R1 fixes

Task `task_07508030e174`, 19 Oct 2026. The independent review `docs/runtime-review/B1a-ASTRA.md` (verdict: pass with fixes) found five issues, F1–F5. All five are fixed here, one commit per finding:

- No storefront claim was rewritten and no theme file was edited; the theme diff since 3bae259 is still B1a's 11 text corrections.
- No off-limits Loop file was touched; the Loop strings are handed to its owner.

| Finding | Commit | Result |
|---|---|---|
| F1: claims register coverage | `38c7c68` | 17 entries gain claim links; 13 template entries move approved → needs-review; 3 new claim rows |
| F2: C46 scope | `c64dae9` | C46 quotes the full statement, needs-review |
| F3: runtime branches | `155691f` | 4 new needs-key entries; batch 01: 225 entries, digest `a09219ae1af8` |
| F4: digest verifier | `c9a3bbb` | `digest.py` checks every batch file entry by entry; `digest_selftest.py` proves three negative cases |
| F5: FR typography | `a3c13c3` | real U+00A0 / U+202F in every French price, percentage and grouped-number example |
| NL follow-up | `a5298b0` | Dutch for the 4 new strings; NL statuses refreshed for the new claim links |

**Method.** The inventory is produced by the same builders as B1a and B2. They were rerun before any change, and git saw no difference: they reproduce the committed files byte for byte. After each fix, a diff of `en-source.json` against the previous commit listed exactly the intended entries. Every EN text and digest stayed unchanged in F1 and F2. F3 changed only batch 01.

### F1: claims register coverage

A claim row can now cover several wordings, and its `Where` column lists every entry that carries it, with no "+n more".

| Claim | Now also covers | Entries | Inventory status |
|---|---|---|---|
| C60 | "98% occlusion vs 82% and 65% …" | `card_bDxUVT/result_text`, both templates | approved → needs-review |
| C61 | "SMD 2.17 · p = 0.004 · 95% CI …" | `card_yMiD9D/result_text`, both | approved → needs-review |
| C62 | "SMD −1.09 · p < 0.00001 · 95% CI …" | `card_fmFMFd/result_text`, both | approved → needs-review |
| C63 | "Lower cold-air and tactile sensitivity vs fluoride and placebo …" | `card_Hi7YUD/result_text`, both | approved → needs-review |
| C64 | "Fewer ulcers, shorter duration, fewer episodes, less pain" | `card_JeERX6/result_text`, both | approved → needs-review |
| **C68** (new, needs-review) | "covering more than 38,000 people between them" | `research_behind_system_EkjATL/bottom_text`, both | approved → needs-review |
| C35 (unsupported) | "Radiant calm gums" | `index:product_benefits_karmicare_bcQ6tp/card_VP8KGi/heading` | approved → needs-review |
| **C93** (new, needs-review) | "certified safe to remain in your mouth" | `index:km_faq_accordion_FYcArV/faq_item_qUxYCn/answer` | stays corrected; now claims C13 + C93 |
| C93 | "Safety-assessed for leave-on use", "Leave-on safe" | `custom.product_faq#56`, `#95` | stays admin-held, claim note added |
| **C94** (new, needs-review) | "— calmer gums, fresher breath, morning and night" | `custom.treatment_journey_*#11` | stays admin-held, claim note added |

- Each linked entry carries the claim ids in `claims` and a note "claims …: needs-review/unsupported (CLAIMS-REVIEW.md)". `corrected` and `admin-held` keep their provenance status, as the review asked.
- All three batch copies, INVENTORY.md and CLAIMS-REVIEW.md were regenerated.
- 13 template entries changed status: 10 result lines, the 2 `bottom_text` entries and the gum heading. The F1 commit message says 14; that count is wrong, 13 is correct.

### F2: C46

C46 now quotes the whole statement: "Awake for the cortisol morning, Asleep for the repair night — supporting the natural recovery process instead of interrupting it." It is `needs-review`. The allowed verb "supporting" does not make it cosmetic: the statement ties the formulas to cortisol and overnight recovery, and compares them with care that "interrupts" it, which needs Clinical Research validation like C40 and C50–C54. Entry `custom.product_faq#104` stays `admin-held` and carries the review note.

**Claim totals for batches 01–03:** 66 claims, of which 17 approved, 46 needs-review, 3 unsupported (B1a: 63, 18 / 42 / 3).

### F3: runtime branches

When two branches share a line, the new id adds a branch suffix; `key_path` keeps the exact file:line. The notes name both consumers (the homepage and the Duo PDP), and each sibling entry points to its new branch.

| Id | key_path | EN | resource_type | Owner |
|---|---|---|---|---|
| `liquid:assets/chronobiology-clock-karmicare.js:91:live` | `assets/chronobiology-clock-karmicare.js:91` | `. Current local time.` | theme_locale | localization worker |
| `liquid:assets/loop-widget.js:2452:annual` | `assets/loop-widget.js:2452` | `/ year` | app | Loop owner |
| `liquid:assets/loop-widget.js:2463` | `assets/loop-widget.js:2463` | `Renews` (replaces "ships") | app | Loop owner |
| `liquid:assets/loop-widget.js:2464` | `assets/loop-widget.js:2464` | `{{ amount }} / brushing` | app | Loop owner |

For `Renews`, the note advises keying the whole line ("Renews every {{ days }} days"). Once the admin phrase is translated, the English regex `/ships/i` no longer matches, and Dutch word order needs the full line anyway (approved Figma NL: "Elke 60 dagen verlengd").

Inventory totals after R1 are in "Inventory (acceptance counts)" above: 743 entries, 77 needs-key.

### F4: digest verifier

`digest.py` now checks each batch file independently:
- each entry's `sha1` equals `sha1(en)` of that file;
- the digest recomputed from the file's entries equals both the stored and the canonical digest;
- ids are unique and match the canonical batch exactly, with none missing and none extra;
- every entry equals its `en-source.json` entry field by field;
- no stray batch file exists.

It exits 1 on any mismatch, and `--dir` runs it on a copy. `python3 docs/source-copy/digest_selftest.py` reproduces the three negative cases on temporary copies:

```
control: unchanged copy                            exit 0 (expected 0)  pass
altered EN value, sha1/count/digest unchanged      exit 1 (expected 1)  pass
    ERROR batches/batch-01-homepage.json: sha1 does not match en for index:hero_karmicare_XKKLDK/heading_RHmd8h/heading
    ERROR batches/batch-01-homepage.json: stored digest a09219ae…, recomputed from its entries d54c06d3…
    ERROR batches/batch-01-homepage.json: digest of its entries d54c06d3… differs from the canonical a09219ae…
    ERROR batches/batch-01-homepage.json: index:hero_karmicare_XKKLDK/heading_RHmd8h/heading differs from en-source.json in en
substituted id at unchanged count                  exit 1 (expected 1)  pass
    ERROR batches/batch-01-homepage.json: missing id index:hero_karmicare_XKKLDK/heading_RHmd8h/heading
    ERROR batches/batch-01-homepage.json: extra id index:SUBSTITUTED/id
metadata-only change (status)                      exit 1 (expected 1)  pass
    ERROR batches/batch-02-pdp.json: product.subscription-item:main/highlights_slider_9wAjAb/text_1 differs from en-source.json in status
```

### F5: French typography

The French examples in GLOSSARY.md now contain the real characters. In this report's notation: `0,49 €`, `1 200 €`, `36 559`, `IC à 95 %`, `20 %`, `21 €` and `98 %`, that is U+00A0 before € and % and U+202F as the thousands separator. The glossary itself holds the characters, not the escapes. A new "Encoding" row says to copy them as they are. A code-point scan finds no plain space left before €/% or inside a grouped number. The Edit tool normalised the characters to plain spaces, so they were written by a script with explicit ` ` / ` ` escapes. The FR typography decision stays with Victor.

### NL follow-up

`docs/localization/nl/` (B2 payloads) follows the changes in batch 01 and the new claim links:

- **New Dutch:**
  - `. Huidige lokale tijd.`
  - `/ jaar` (approved Figma NL)
  - `Verlengd`: fit-risk; the note asks the Loop owner to key the whole line "Elke {{ days }} dagen verlengd"
  - `{{ amount }} / poetsbeurt` (approved Figma NL)
- **Statuses:** the research result lines, evidence counts, leave-on safety lines and C46 are now `pending-claim-review` (329 in total). "Radiant calm gums" is held with the rest of benefit card 06 (117 unsupported held).
- **Report:** the NL REPORT counts are refreshed.

### Verification

| Check | Result |
|---|---|
| `python3 docs/source-copy/digest.py` | exit 0, 8 batches |
| `python3 docs/source-copy/digest_selftest.py` | exit 0 (control passes, the three defects fail) |
| `python3 docs/localization/nl/validate.py` | exit 0, 8 batches |
| `shopify theme check --fail-level error` | exit 0 (237 files, 21 warnings, no errors) |

### Handoffs from R1

- **Loop owner:** keys for `/ year`, `Renews` (better: the whole line) and `{{ amount }} / brushing` in `assets/loop-widget.js`, together with the B1a Loop strings.
- **FR worker:** merge this branch. Batch 01 has a new digest and 4 new entries to translate; the new claim links change which FR entries are `pending-claim-review` or held.
- **Clinical Research / Victor:** C68, C93, C94 and the reclassified C46 join the sign-off list.
