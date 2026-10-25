# R57 / R57b · Launch blocker 1: consumer-rights text (gate-legal)

**Created**: 2026-10-24 · lane gate-legal · base `karmicare/soft-launch` @ 5bab3ad · R57 = commit 31306f8, reviewed by Astra (`docs/runtime-review/R57-CONSUMER-RIGHTS-TEXT-ASTRA.md`, verdict REWORK); R57b = the rework, §3b, §3c and §8; R57c = Victor's Care Credit decision, §3d and §8; R57d = the retained-benefit rework after Astra's R57c review (`docs/runtime-review/R57C-CARE-CREDIT-RULE-ASTRA.md`, verdict REWORK, B4), §3e and §8, plus gate-consent's privacy handoff (R61b, commit 857c500), §3f; R57e = the final privacy round (gate-consent commit 938811c after Astra's R57d B1 and B2), §3g and §8; R57f = the rework after Astra's R57e review (`docs/runtime-review/R57E-PRIVACY-FINAL-ASTRA.md`: controller framing in section 5, conditional-reload withdrawal sentence), §3h and §8; R57g = wording only, the single withdrawal sentence of 9.2 from Astra's combined R61e/R57f report, §3i.
**Scope**: LR1 blocker 1 (`docs/launch-gate/input/LR1-LAUNCH-READINESS.md`) = audit items P0-1, P0-5, P0-6, P0-8, P0-9, P0-14 (withdrawal information), P0-15 (the NL/FR of the changed strings) from `input/legal-offer/work/2026-10-05/legal-audit-terms-consumer-rights-privacy.md`.
**Decisions applied**: D1 option A (Victor, 24 Oct: priming exemption dropped, loss-of-value rule), D7 and D8 (Consumer Rights is a plain-language summary that points to the Terms; the canonical texts are `input/legal-offer/legal/*`), D2 and D5 (unchanged, already in the text). D3 is discussed in §5 and not applied by this lane.

**Deliverables in this folder**

| File | What |
|---|---|
| `CHANGES.md` (this file) | Where each text lives, the canonical place and redirects, every change with old → new, reason and legal source (§3 R57, §3b and §3c R57b, §3d R57c), what was verified, what is left, Astra's review items and Victor's Care Credit decision (§8) |
| `POLICIES-PASTE.md` | Full corrected body of the four Shopify policies that change (Terms of service, Refund policy, Privacy policy, Purchase options cancellation policy), EN first, then NL and FR for Translate & Adapt |
| `TRANSLATIONS-HANDOFF.md` | The 19 changed theme-page settings with template, block id, key path and the full EN, NL and FR value, for source-copy |
| `ADMIN-STEPS.md` | What Victor does in admin, in order, starting with the launch gate (durable-medium confirmation): policy pastes, legacy pages to hide, redirects, titles, legacy Terms links, checks |

Theme files changed: `templates/page.terms-and-conditions.json`, `templates/page.consumer-rights.json` and `templates/page.privacy-policy.json` (EN setting values only; the privacy changes are two lines for the withdrawal acknowledgement, §3c, and the regional consent wording from gate-consent, §3f, finalised in §3g: no opt-out promise while the Data Sharing Opt-Out Page is inactive, immediate withdrawal, Shopify Network Intelligence). The three legacy pages, the policies and all NL/FR are admin work (`ADMIN-STEPS.md`).

---

## 1. Where each text lives today (public read, 24 Oct 2026, karmicares.myshopify.com)

Every page below returned HTTP 200 unless noted. The three designed pages carry the same text as the policy slots (plus the key-number cards and the left menu); the NL and FR versions of the policies and of the designed pages are live and carry the same wrong clauses in translation.

| Document | Designed theme page (footer links here) | Shopify policy slot (checkout and order emails link here) | Legacy copy, still published and in the sitemap | NL / FR |
|---|---|---|---|---|
| Terms and Conditions | `/pages/terms-and-conditions-1` · template `page.terms-and-conditions` · admin title “New Terms and Conditions” | `/policies/terms-of-service` | `/pages/terms-and-conditions` · pre-2.0 terms (24 delivery countries incl. US, we@ address, 30-day refund, old clauses) | both live |
| Consumer Rights & Transparency Charter | `/pages/new-consumer-rights` · template `page.consumer-rights` · “New Consumer Rights” | `/policies/refund-policy` | `/pages/consumer-rights` · a two-link stub (mediation service, disputes committee) | both live |
| Privacy Policy | `/pages/privacy-policy` · template `page.privacy-policy` · “New Privacy Policy” | `/policies/privacy-policy` | `/pages/privacy` · 2021 policy with template placeholders and bundled consent | both live |
| Shipping policy | – (Terms clause 8 and 5.4, word for word) | `/policies/shipping-policy` | – | – |
| Subscription (purchase options cancellation) policy | – (Terms clause 9, word for word) | `/policies/subscription-policy` (page title “Cancellation policy”) | – | – |
| Contact information | – (Terms 1 and 15.1) | `/policies/contact-information` | – | – |
| Legal notice | – (Terms 1) | `/policies/legal-notice` | – | – |
| Online withdrawal function | `/pages/withdrawal` → **404 today**; the gate-withdrawal lane builds it under that handle | – | – | – |

`sitemap_pages_1.xml` lists all six legal page handles: `consumer-rights`, `new-consumer-rights`, `privacy`, `privacy-policy`, `terms-and-conditions`, `terms-and-conditions-1`.

The footer (`sections/footer.liquid`, not touched) links the page-picker settings, falls back to the pages `terms-and-conditions-1`, `privacy-policy` and `new-consumer-rights`, and only then to `shop.terms_of_service`, `shop.privacy_policy` and `shop.refund_policy`.

## 2. One canonical place per document, and a redirect for every other copy

**Proposal.** One text per document; the source is the repo file (D8: `input/legal-offer/legal/terms-and-conditions/en.md`, `consumer-rights/en.md`, `privacy-policy/en.md`, plus `shopify/*.md` for the four short policies). It is published in two places by necessity, and both must be identical:

1. **The policy slot `/policies/*` is the canonical URL of the document.** Shopify requires it, checkout and the order and subscription emails link it, it exists per language (`/nl/policies/…`, `/fr/policies/…`) and it cannot be unpublished. Terms clause 2.6 now names it (`karmicare.com/policies/terms-of-service`) instead of a dead `/en/pages/…` address; the Consumer Rights pointer line (C2) links it too.
2. **The designed page `/pages/*` is the reading copy** (menu, key cards, Day/Night styling) and the footer destination. It stays, kept word for word identical to the slot through this process (`POLICIES-PASTE.md` is generated from the same change list as the templates).
3. **The three legacy pages are hidden and redirected** to their replacements, as Victor decided on 20 Oct (F5 in `docs/localization/nl/REPORT.md`): `/pages/consumer-rights` → `/pages/new-consumer-rights`, `/pages/privacy` → `/pages/privacy-policy`, `/pages/terms-and-conditions` → `/pages/terms-and-conditions-1`. A Shopify redirect only works once the source page is no longer published, so hiding comes first (`ADMIN-STEPS.md` steps 4 and 5). The 67-row migration redirect map must point its Webflow legal rows (`/en/pages/terms-and-conditions`, `/en/pages/privacy`, `/en/pages/consumer-rights` and the NL/FR variants) at the designed pages, never at the legacy handles.
4. **Later, after the domain switch**: once the legacy pages are deleted, the designed pages can take the clean handles (`terms-and-conditions`, `consumer-rights`), with the footer fallbacks in `sections/footer.liquid` and the footer page pickers updated in the same release. Not in this round: the footer is frozen for this lane and a handle change during cutover adds risk for no legal gain.

Why not make the designed pages canonical and leave the slots as “copies”? The slots cannot be removed or redirected, and the law looks at what the customer is shown at checkout and in the confirmation: that is the slot. Why not drop the designed pages? They carry the translations, the menu and the key cards, and the footer falls back to the plain slots only when they are missing.


## 3. R57, the changes reviewed by Astra (24 Oct): the changes, one by one (EN old → new)

The NL and FR of every change are in `TRANSLATIONS-HANDOFF.md` (theme pages) and `POLICIES-PASTE.md` (policies). Old text is quoted from the live policy body on 24 Oct 2026 (round B: from the R57 text); tags are stripped here for readability.


### T1 · Terms clause 2.2 (consumer definition)

**Setting**: `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_g6nYeY/content` · policy `terms-of-service`

**Why**: The "specific B2B conditions" do not exist; stating that they apply is an untrue statement in the contract (audit P0-9).

**Legal basis**: Art. VI.97 WER (misleading commercial practice). Audit 5 Oct, P0-9.

**Old**

> If you order as a dental professional, clinic or reseller, specific B2B conditions apply in addition to these Terms.

**New**

> These Terms are written for consumers. Orders by dental professionals, clinics or resellers follow a separate written agreement.


### T2 · Terms clause 2.6 (where the Terms live)

**Setting**: `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_g6nYeY/content` · policy `terms-of-service`

**Why**: The address karmicare.com/en/pages/terms-and-conditions does not exist on the Shopify store (EN has no /en prefix) and /pages/terms-and-conditions is the legacy page. The Terms now point to their canonical, language-aware record in Settings → Policies, which checkout also links.

**Legal basis**: Art. VI.45 §1 WER (pre-contractual information must be clear and reachable); CHANGELOG open point on Terms 2.6.

**Old**

> these Terms are always available at karmicare.com/en/pages/terms-and-conditions and are provided

**New**

> these Terms are always available at karmicare.com/policies/terms-of-service and are provided


### T3 · Terms clause 3.1 (product classification)

**Setting**: `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_iDEfUH/content` · policy `terms-of-service`

**Why**: Toothbrushes and floss are articles, not a "substance or mixture", so they are not cosmetic products and are not notified on the CPNP. Saying so is a false statement about regulatory status (audit P0-9; LR1 blocker 1).

**Legal basis**: Art. 2(1)(a) Regulation (EC) No 1223/2009 (definition of cosmetic product); Regulation (EU) 2023/988 (general product safety); Art. VI.97 WER.

**Old**

> EU cosmetic status: KARMICARE products (including our oral care systems, personal hygiene formulations and related accessories) are classified and notified as cosmetics under Regulation (EC) No 1223/2009 and manufactured under Good Manufacturing Practices (ISO 22716). They are not medicinal products or medical devices.

**New**

> Product classification: Awake and Asleep are cosmetic products under Regulation (EC) No 1223/2009, notified on the Cosmetic Product Notification Portal (CPNP) and manufactured under Good Manufacturing Practice (ISO 22716). They are not medicinal products or medical devices. The toothbrushes and the floss are not cosmetics: they are general consumer products covered by Regulation (EU) 2023/988 on general product safety.


### T4 · Terms clause 4.1 (statutory right of withdrawal), items 1 to 4 → 1 to 5

**Setting**: `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_FcEDdA/content` · policy `terms-of-service`

**Why**: The refund deadline ran from receipt of "unopened" goods; the law counts 14 days from the day we are informed, allows us only to withhold until the goods or proof of sending arrive, and knows no "unopened" condition. The online withdrawal function (mandatory since 14 August 2026) was not named, and the consumer's own obligations (return within 14 days, loss-of-value rule) were missing (audit P0-5, P0-14; LR1 blocker 1).

**Legal basis**: Art. VI.47, VI.49, VI.50 §1 and §3, VI.51 §1 and §2, VI.45 §1 8° and VI.61/2 WER (Justel, consolidated 24 Oct 2026); Art. 13 and 14 Directive 2011/83/EU; Art. 11a as inserted by Directive (EU) 2023/2673.

**Old**

> • 14-day withdrawal period: you may withdraw from a contract concluded online without giving a reason within 14 calendar days of physical delivery (Article VI.47 WER). For a membership, the period runs from your first delivery. Tell us by email at care@karmicare.com, by phone on +32 (0) 478 57 27 61, or with the form in the Annex.
> • Reimbursement: we reimburse all payments received from you, including standard delivery charges, within 14 calendar days of receiving the returned unopened goods or proof of return shipment.
> • Same payment method: we reimburse via the same payment method you used. We never substitute a voucher unless you expressly ask for one.
> • Relation to our guarantees: the money-back guarantees in clauses 4.2 to 4.5 are voluntary commercial guarantees. They come on top of your statutory rights and never limit them.

**New**

> • 14-day withdrawal period: you may withdraw from a contract concluded online without giving a reason within 14 calendar days of physical delivery (Article VI.47 WER). For a membership, the period runs from your first delivery. Tell us before the period ends: through the online withdrawal function (Withdraw from contract here), by email at care@karmicare.com, by phone on +32 (0) 478 57 27 61, or with the model form in the Annex (Article VI.49 WER). Any clear statement is enough; you do not need our approval.
> • Reimbursement: we reimburse all payments received from you, including the standard delivery charge, without undue delay and at the latest within 14 calendar days of the day we are informed of your withdrawal (Article VI.50 §1 WER). We may withhold the reimbursement until we have received the goods back or until you have supplied proof that you sent them, whichever comes first (Article VI.50 §3 WER).
> • Same payment method: we reimburse via the same payment method you used, at no cost to you. We never substitute a voucher unless you expressly ask for one.
> • Returning the goods: send the goods back without undue delay and at the latest 14 days after the day you told us; the address and the cost are in clause 4.7 (Article VI.51 §1 WER). You may handle the goods as you would in a shop, to establish their nature, characteristics and functioning. You are liable only for any diminished value that results from handling beyond that (Article VI.51 §2 WER); clause 4.6 explains what this means for a primed pump.
> • Relation to our guarantees: the money-back guarantees in clauses 4.2 to 4.5 are voluntary commercial guarantees. They come on top of your statutory rights and never limit them.


### T5 · Terms clauses 4.2.3 and 4.3.3 (Try Once and 60-Day rhythm refunds)

**Setting**: `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_FcEDdA/content` · policy `terms-of-service`

**Why**: "Of approval" suggests the refund under the money-back guarantee is discretionary. A commercial guarantee binds on its stated conditions; the objective trigger is the customer's request within the period (audit P0-5, key card row).

**Legal basis**: Art. 1649septies §1 old Civil Code (a commercial guarantee binds on the terms of the guarantee statement and its advertising).

**Old**

> of approval, to your original payment method.

**New**

> of your request, to your original payment method.


### T6 · Terms clause 4.4.3 (Year guarantee, return window)

**Setting**: `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_FcEDdA/content` · policy `terms-of-service`

**Why**: Same "approval" wording in the Year guarantee. The unopened-duo condition itself stays: it is a condition of the voluntary 60-day guarantee, not of the statutory right, and clause 4.1.5 keeps the two apart.

**Legal basis**: Art. 1649septies §1 old Civil Code; Art. VI.37 §2 WER (ambiguity is read in the consumer's favour).

**Old**

> within 14 days of approval, with the prepaid return label

**New**

> within 14 days of your request, with the prepaid return label


### T7 · Terms clause 4.6.3 (primed pump)

**Setting**: `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_FcEDdA/content` · policy `terms-of-service`

**Why**: Decision D1, option A (Victor, 24 Oct): the priming exemption is dropped. The hygiene exception needs sealed goods whose seal is broken after delivery; the pack has no seal and an unprimed pump is not one the customer can recognise. Telling consumers their right ends when it does not is a misleading practice and can extend the withdrawal period by 12 months. The loss-of-value rule gives the same economic protection without a seal (audit P0-6; LR1 blocker 1).

**Legal basis**: Art. VI.51 §2 WER (liability for diminished value only); Art. VI.53, 5° WER and CJEU C-681/17 slewo (sealed goods); Art. VI.48 WER (extension of the period); Art. 14(2) and 16(e) Directive 2011/83/EU.

**Old**

> Sealed delivery and opened formulas: Awake and Asleep are delivered sealed. The pump is unprimed and the nozzle holds no formula; priming the pump breaks that seal. Once primed, a formula can no longer be sold for hygiene reasons, so the statutory right of withdrawal no longer applies to it (Art. VI.53, 5° WER). Should that exception not apply in your case, we may deduct the loss of value caused by the use from your refund, up to the full price of the formula (Art. VI.51 §2 WER). Our money-back guarantees in clauses 4.2 to 4.4 are more generous and are not affected.

**New**

> Primed pumps and your right of withdrawal: priming the pump and using a formula goes beyond what is needed to establish its nature, characteristics and functioning. Your statutory right of withdrawal remains. If you withdraw after priming or using a formula, we may deduct the resulting loss of value from your refund, up to the full price of that formula (Article VI.51 §2 WER). An unprimed pump and the packaging can be checked freely. Our money-back guarantees in clauses 4.2 to 4.4 are more generous and are not affected.


### T8 · Terms clause 4.7.2 (how to return)

**Setting**: `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_FcEDdA/content` · policy `terms-of-service`

**Why**: A statutory withdrawal needs no "return authorisation" from us, and it is not limited to one-time orders. The customer must know the return deadline and address; we only confirm them (audit P0-5).

**Legal basis**: Art. VI.49 §1 and VI.51 §1 WER; Art. VI.45 §1 8° WER (conditions and procedure for exercising the right).

**Old**

> For a statutory withdrawal of a one-time order, we send you a return authorisation and the warehouse address: KARMICA BV, Returns Department, Vizierstraat 28, 8000 Bruges, Belgium. You pay the direct cost of return shipping, unless the return is due to a defect or our shipping error.

**New**

> For a statutory withdrawal, send the goods back within 14 days of telling us to: KARMICA BV, Returns Department, Vizierstraat 28, 8000 Bruges, Belgium. You need no return authorisation; we acknowledge your withdrawal by email and confirm the address. You pay the direct cost of return shipping, unless the return is due to a defect or our shipping error.


### T9 · Terms clause 4.7.3 (deductions)

**Setting**: `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_FcEDdA/content` · policy `terms-of-service`

**Why**: "No deductions other than clause 4.4" contradicted clauses 4.3.3, 4.7.4 and, after this change, the loss-of-value rule in 4.6.3. An unclear term is read against us (audit P2-3, made necessary by T7).

**Legal basis**: Art. VI.37 §2 WER.

**Old**

> All refunds are issued without deductions or administrative fees other than those set out in clause 4.4.

**New**

> We never charge administrative fees on a refund. The only deductions are those set out in clauses 4.3, 4.4, 4.6 and 4.7.4.


### T10 · Terms clause 7, items 1 to 6 (legal guarantee of conformity)

**Setting**: `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_EAKJLC/content` · policy `terms-of-service`

**Why**: The clause narrowed the legal guarantee to "latent manufacturing defects", required a "verified" defect, let us choose replacement as the only remedy and listed "exclusions". Conformity also covers the description, fitness for purpose and normal durability; the two-year presumption puts the burden on the seller; the consumer chooses between repair and replacement; and any term limiting these rights is void (audit P0-8; LR1 blocker 1). Article references corrected: 1649ter (conformity), 1649quater §1 (two years), §2 (notification), §4 (presumption), 1649quinquies (remedies), 1649octies (mandatory). "Book VI WER" removed: it does not transpose Directive 2019/771.

**Legal basis**: Art. 1649ter, 1649quater §1, §2 and §4, 1649quinquies §§1, 2 and 5, 1649octies old Civil Code, as replaced by the Law of 20 March 2022 (in force 1 June 2022), transposing Art. 6, 7, 10, 11, 12, 13 and 21 Directive (EU) 2019/771. Verified on kustcodex.be (consolidated text) and FPS Economy, 24 Oct 2026.

**Old**

> • Legal framework: European consumers have a legal guarantee of conformity under Articles 1649bis to 1649octies of the Belgian Civil Code and Book VI WER, transposing Directive (EU) 2019/771 (Law of 20 March 2022).
> • Consumable oral care (nature of the goods): under Article 1649quater, §4 of the Belgian Civil Code, the guarantee applies taking into account the nature of the goods. KARMICARE formulas are consumable cosmetic goods designed for an intended cycle of daily use (for example 30 to 60 days, depending on volume and frequency). The guarantee does not mean a formula lasts two years once opened. Normal depletion, natural bristle wear, or use beyond the Period After Opening (PAO) or minimum durability date is not a lack of conformity.
> • What is covered: latent manufacturing defects and mechanical non-conformities present at or arising from delivery: failure, jamming or breakage of the airless pump while formula remains inside under normal use; formulation defects such as premature separation, contamination, abnormal discolouration or instability before the expiry date or PAO when stored as recommended; defective seals, leaking containers or structural defects in toothbrush handles or floss dispensers.
> • Remedies: for a verified manufacturing or packaging defect, KARMICARE provides a free replacement of the defective unit (or a replacement bottle or pump). If replacement is impossible or disproportionate, you are entitled to a proportionate price reduction, or to end the contract with a full refund.
> • Notification: tell us within two months of discovering a lack of conformity (Art. 1649quater, §2 Belgian Civil Code) by emailing care@karmicare.com with your order number, a description, and photos or a video of the defect.
> • Exclusions: normal depletion of the formula; natural wear of toothbrush bristles; damage from improper storage (extreme temperatures, direct sunlight, moisture or tampering with the bottle); use after the PAO or expiry date.

**New**

> • Legal framework: as a consumer you have a legal guarantee of conformity under Articles 1649bis to 1649octies of the Belgian (old) Civil Code, as replaced by the Law of 20 March 2022 transposing Directive (EU) 2019/771. Nothing in this clause limits that guarantee; any term that did would be void (Article 1649octies).
> • What conformity means: the goods must match our description, be fit for the purposes goods of that type are normally used for, and have the quality and durability that is normal for such goods and that you can reasonably expect, including on the basis of our advertising and labelling (Article 1649ter). Awake and Asleep are consumable cosmetic goods designed to be used up over a cycle of daily use (for example 30 to 60 days, depending on volume and frequency). The guarantee does not mean a formula lasts two years once opened. Normal depletion, natural bristle wear, and use beyond the Period After Opening (PAO) or the minimum durability date are not a lack of conformity.
> • Two years, presumed from delivery: we are liable for any lack of conformity that exists at delivery and becomes apparent within two years of delivery (Article 1649quater §1). A lack of conformity that appears within those two years is presumed to have existed at delivery, unless we prove otherwise or that is incompatible with the nature of the goods or of the defect (Article 1649quater §4). It is not up to you to prove the cause.
> • Your remedies: you choose between a free repair and a free replacement, unless the remedy you choose is impossible or would impose disproportionate costs on us compared with the other (Article 1649quinquies §§1 and 2). If we do not repair or replace within a reasonable time and without significant inconvenience to you, if we refuse, if the defect persists, or if it is serious enough, you are entitled to a proportionate price reduction or to end the contract and be refunded (Article 1649quinquies §5). Ending the contract is not possible for a minor defect, and it is up to us to prove that a defect is minor.
> • Notification: tell us within two months of discovering a lack of conformity (Article 1649quater §2) by emailing care@karmicare.com with your order number, a description, and photos or a video of the defect. We handle every claim free of charge.
> • Not a lack of conformity: normal depletion of a formula; natural wear of toothbrush bristles; damage caused after delivery by improper storage (extreme temperatures, direct sunlight, moisture or tampering with the pump); use after the PAO or the expiry date.
> The examples below illustrate the guarantee. They never limit your legal rights.


### T11 · Terms clause 7, examples (remedies)

**Setting**: `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_EAKJLC/block_content` · policy `terms-of-service`

**Why**: The examples named replacement as the only remedy; the consumer chooses between repair and replacement (audit P0-8).

**Legal basis**: Art. 1649quinquies §2 old Civil Code.

**Old**

> Remedy: free replacement unit.

**New**

> Remedy: free replacement, or repair if you prefer.

**Old**

> Remedy: replacement.

**New**

> Remedy: free replacement.


### T12 · Terms Annex (model withdrawal form, caption)

**Setting**: `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_fz6KEQ/content` · policy `terms-of-service`

**Why**: The model form is for every distance contract, memberships included, and the law attaches no "eligible, unopened" condition to it. The statutory caption is restored and the online withdrawal function is named next to the form (audit P0-5, P0-14).

**Legal basis**: Annex 2 to Book VI WER (model withdrawal form, statutory wording); Art. VI.45 §1 8° and VI.61/2 WER.

**Old**

> Changed your mind about a one-time order? Send us this form, or simply email us a clear statement. Either is enough.
> Complete and return this form only if you wish to withdraw from an eligible, unopened contract.

**New**

> Changed your mind? Send us this form, use the online withdrawal function, or simply email us a clear statement. Any of these is enough.
> Complete and return this form only if you wish to withdraw from the contract. Online: Withdraw from contract here.


### C1 · Consumer Rights, key card 3 ("14 days · To receive your refund")

**Setting**: `page.consumer-rights:policy_banner_Pgpxip/benefit_card_3DXGyT/card_bottom_text` · policy `refund-policy`

**Why**: "After approval" suggests a discretionary refund; the statutory clock runs from the day we are told (audit P0-5).

**Legal basis**: Art. VI.50 §1 WER.

**Old**

> After approval · same payment method

**New**

> After you tell us · same payment method


### C2 · Consumer Rights section 1 (pointer to the Terms)

**Setting**: `page.consumer-rights:legal_toc_section_gYznx3/content_section_GLa7AN/content` · policy `refund-policy`

**Why**: Decision D7: Consumer Rights is a plain-language summary; the Terms are the contract, and where the two differ the version more favourable to the consumer applies. The line removes the risk of two drifting contract texts (audit P1-4).

**Legal basis**: Art. VI.37 §2 WER (interpretation in the consumer's favour).

**Old**

> Your rights come from the law, not from our goodwill. This page sets them out in one place, alongside the promises Karmicare adds on top.

**New**

> Your rights come from the law, not from our goodwill. This page sets them out in one place, alongside the promises Karmicare adds on top.
> This page explains your rights in plain words. The Terms and Conditions are the contract. If the two ever differ, whichever is more favourable to you applies.


### C3 · Consumer Rights section 2 (product classification), content, title and menu label

**Setting**: `page.consumer-rights:legal_toc_section_gYznx3/content_section_g6nYeY/content` (+ legal_toc_section_gYznx3/content_section_g6nYeY/title, legal_toc_section_gYznx3/content_section_g6nYeY/nav_label) · policy `refund-policy`

**Why**: The section said floss and toothbrushes are CPNP-notified cosmetics with a CPSR (false: they are articles, not substances or mixtures), presented GMP, CPNP and CPSR as reasons to trust the product (compliance may not be presented as a benefit), carried a free-from claim ("100% free of ... parabens, endocrine disruptors") that the EU claims criteria do not allow, and put a claim ("biorhythmic remineralisation") inside the regulatory classification (audit P0-9; LR1 blocker 1).

**Legal basis**: Art. 2(1)(a) Regulation (EC) No 1223/2009; Regulation (EU) No 655/2013 common criteria for claims (criterion 1, legal compliance; free-from guidance 2017); Regulation (EU) 2023/988; Art. VI.97 WER.

**Old**

> Awake and Asleep are notified EU cosmetics, made under Good Manufacturing Practice and assessed by a qualified safety assessor.
> All KARMICARE products, including Awake Morning Toothpaste, Asleep Evening Toothpaste, Charcoal Floss and the Toothbrushes, are:
> • Formulated and manufactured in accordance with European Good Manufacturing Practices (GMP / ISO 22716);
> • Registered and notified on the European Cosmetic Product Notification Portal (CPNP) in compliance with Regulation (EC) No 1223/2009;
> • Subject to a Cosmetic Product Safety Report (CPSR) signed by a qualified European safety assessor;
> • 100% free of SLS, parabens, artificial dyes, endocrine disruptors and controversial abrasives.
> Regulatory classification: KARMICARE oral care products are cosmetics intended for daily oral hygiene, biorhythmic remineralisation and enamel support. They are not medicinal products or medical devices and do not claim to diagnose, treat or cure medical conditions.

**New**

> Awake and Asleep are cosmetic products under EU law. The toothbrushes and the floss are general consumer products.
> Awake Morning Toothpaste and Asleep Evening Toothpaste are cosmetic products under Regulation (EC) No 1223/2009, notified on the European Cosmetic Product Notification Portal (CPNP). They are cosmetics for daily oral care. They are not medicinal products or medical devices and do not claim to diagnose, treat or cure medical conditions.
> The Toothbrushes and the Charcoal Floss are not cosmetics. They are general consumer products covered by Regulation (EU) 2023/988 on general product safety.

**Old**

> 2. EU cosmetic safety and standards

**New**

> 2. Product classification

**Theme only** (left menu label): “Safety and standards” → “Classification”


### C4 · Consumer Rights section 3.1 (legal right to withdraw)

**Setting**: `page.consumer-rights:legal_toc_section_gYznx3/content_section_iDEfUH/content` · policy `refund-policy`

**Why**: Same corrections as Terms 4.1: refund clock from the day we are told, withholding only until the goods or proof of sending arrive, no "unopened" condition, no approval, the online withdrawal function named, the return deadline and the loss-of-value rule stated (audit P0-5, P0-14; LR1 blocker 1).

**Legal basis**: Art. VI.47, VI.49, VI.50 §1 and §3, VI.51 §1 and §2, VI.61/2 WER.

**Old**

> Tell us by email at care@karmicare.com, by phone on

**New**

> Tell us through the online withdrawal function (Withdraw from contract here), by email at care@karmicare.com, by phone on

**Old**

> , or with the form in section 10.
> • We reimburse all payments received from you, including standard delivery charges, within 14 calendar days of receiving the returned unopened goods or proof of return.
> • This right comes from the law.

**New**

> , or with the form in section 10. You do not need our approval.
> • We reimburse all payments received from you, including standard delivery charges, within 14 calendar days of the day you tell us (Article VI.50 WER). We may wait until we have received the goods back or until you have shown that you sent them, whichever comes first.
> • Send the goods back within 14 days of telling us. You may check them as you would in a shop. If you handled or used them beyond that, for example by priming a pump, we may deduct the resulting loss of value from your refund (Article VI.51 §2 WER); see section 3.7.
> • This right comes from the law.


### C5 · Consumer Rights section 3.6, step 2 (refund timing)

**Setting**: `page.consumer-rights:legal_toc_section_gYznx3/content_section_iDEfUH/content` · policy `refund-policy`

**Why**: One sentence mixed the statutory refund (from the day we are told) with the guarantee refunds ("of approving your request"). The two are now stated separately (audit P0-5; brief: keep the voluntary guarantee separate).

**Legal basis**: Art. VI.50 §1 and §3 WER; Art. 1649septies old Civil Code.

**Old**

> We refund within 14 days of approving your request or, for a Year refund, of receiving your returned duos.

**New**

> Under your legal right, we refund within 14 days of the day you tell us; we may wait until the goods are back or you have shown that you sent them. Under our money-back guarantees, we refund within 14 days of your request or, for a Year refund, of receiving your returned duos.


### C6 · Consumer Rights section 3.6, step 4 (returning the goods)

**Setting**: `page.consumer-rights:legal_toc_section_gYznx3/content_section_iDEfUH/content` · policy `refund-policy`

**Why**: No return authorisation is needed for a statutory withdrawal, and it is not limited to one-time orders (audit P0-5).

**Legal basis**: Art. VI.49 §1 and VI.51 §1 WER.

**Old**

> To withdraw from a one-time order under your legal right, we send you a return authorisation and the address: KARMICA BV, Returns Department, Vizierstraat 28, 8000 Bruges, Belgium. Return shipping is yours, unless the item arrived damaged or defective.

**New**

> To return goods after a legal withdrawal, send them within 14 days of telling us to: KARMICA BV, Returns Department, Vizierstraat 28, 8000 Bruges, Belgium. No return authorisation is needed. Return shipping is yours, unless the item arrived damaged or defective.


### C7 · Consumer Rights section 3.7, third bullet (primed pump)

**Setting**: `page.consumer-rights:legal_toc_section_gYznx3/content_section_iDEfUH/content` · policy `refund-policy`

**Why**: Decision D1, option A: the priming exemption is dropped and replaced by the loss-of-value rule (see T7).

**Legal basis**: Art. VI.51 §2 WER; Art. VI.53, 5° WER and CJEU C-681/17.

**Old**

> Sealed delivery: the unprimed pump is the seal. Priming it opens the formula, and an opened formula cannot be returned under the legal right of withdrawal for hygiene reasons; if that rule did not apply, we could still deduct its loss of value, up to its full price. Our money-back guarantees above are more generous and are not affected.

**New**

> Primed pumps and your legal right: priming a pump and using a formula goes beyond checking it. Your right to withdraw remains, but we may deduct the loss of value this causes from your refund, up to the full price of that formula (Article VI.51 §2 WER). Our money-back guarantees above are more generous and are not affected.


### C8 · Consumer Rights section 4 (two-year legal guarantee)

**Setting**: `page.consumer-rights:legal_toc_section_gYznx3/content_section_FcEDdA/content` · policy `refund-policy`

**Why**: Aligned with the corrected Terms clause 7: "Book VI WER" does not transpose Directive 2019/771; the 4.1 heading announced a presumption of conformity instead of a presumption that the defect existed at delivery; the price-reduction remedy named replacement only and omitted the seller's refusal, the persisting defect and the minor-defect rule; what is not a defect was missing (audit P0-8, P1-4).

**Legal basis**: Art. 1649quater §1 and §4, 1649quinquies §§2 and 5 old Civil Code.

**Old**

> (Article 1649bis and following of the Civil Code and Book VI WER, implementing Directive (EU) 2019/771)

**New**

> (Articles 1649bis and following of the Civil Code, implementing Directive (EU) 2019/771)

**Old**

> 4.1 Two-year presumption of conformity

**New**

> 4.1 Two years, presumed from delivery

**Old**

> If a delivered item is defective, non-conforming or damaged on delivery, you are protected for two full years (24 months) from the date of delivery.

**New**

> If an item does not conform, for example a faulty pump, a defective formula, a broken brush or goods that do not match our description, you are protected for two years from delivery (Article 1649quater §1 of the Civil Code).

**Old**

> unless proven otherwise or incompatible with the nature of the goods.

**New**

> unless we prove otherwise or that is incompatible with the nature of the goods or of the defect (Article 1649quater §4). You do not have to prove the cause.

**Old**

> Price reduction or ending the contract. If replacement is impossible, or cannot be carried out within a reasonable time and without significant inconvenience, you can ask for an appropriate price reduction or a full refund and end the contract.

**New**

> Price reduction or ending the contract. If repair or replacement is impossible, is refused, is not done within a reasonable time and without significant inconvenience, or does not solve the problem, you can ask for a proportionate price reduction or end the contract and be refunded. Ending the contract is not possible for a minor defect, and we must prove that a defect is minor (Article 1649quinquies).
> • Not a defect. Using up a formula, normal bristle wear and use after the Period After Opening are not lacks of conformity. Clause 7 of the Terms has the full rules and examples.


### C9 · Consumer Rights section 10 (model withdrawal form, caption)

**Setting**: `page.consumer-rights:legal_toc_section_gYznx3/content_section_at3pLy/content` · policy `refund-policy`

**Why**: Same as T12: the statutory caption, no "eligible, unopened" condition, the online function named (audit P0-5, P0-14).

**Legal basis**: Annex 2 to Book VI WER; Art. VI.45 §1 8° and VI.61/2 WER.

**Old**

> Changed your mind about a one-time order? Send us this form, or simply email us a clear statement. Either is enough.

**New**

> Changed your mind? Send us this form, use the online withdrawal function, or simply email us a clear statement. Any of these is enough.

**Old**

> (*) Delete as appropriate. Complete and return this form only if you wish to withdraw from an eligible, unopened contract.

**New**

> (*) Delete as appropriate. Complete and return this form only if you wish to withdraw from the contract. Online: Withdraw from contract here.


## 3b. R57b, the rework after Astra's R57 review (24 Oct): the changes, one by one (EN old → new)


### TB1 · Terms clause 4.1.4 (what a withdrawing member returns)

**Setting**: `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_FcEDdA/content` · policy `terms-of-service`

**Why**: Astra, open point 1 (non-blocker): say expressly that “the goods” of a membership withdrawal are everything delivered under it, Welcome Kit included; the permission to keep the kit belongs to the voluntary guarantees. No kit-value fee, no €59 deduction on the statutory route.

**Legal basis**: Art. VI.51 §1 and §5 WER; Terms 9.3 (the kit is part of the first membership order).

**Old**

> the address and the cost are in clause 4.7 (Article VI.51 §1 WER). You may handle

**New**

> the address and the cost are in clause 4.7 (Article VI.51 §1 WER). For a membership, the goods are everything delivered under it, the Welcome Kit included. You may handle


### TB2 · Terms clause 4.4.6 (Year guarantee, refund timing)

**Setting**: `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_FcEDdA/content` · policy `terms-of-service`

**Why**: Astra, observation 6 (non-blocker): “receiving and inspecting” could postpone the receipt-based deadline that Consumer Rights 3.6 promises for the Year refund. The two texts now say the same: 14 days from receipt of the returned duos.

**Legal basis**: Art. VI.37 §2 WER (the consumer gets the more favourable reading); Art. 1649septies §1 old Civil Code.

**Old**

> Timing: the refund follows within 14 days of receiving and inspecting the returned duos, to your original payment method.

**New**

> Timing: the refund follows within 14 days of receiving the returned duos, to your original payment method.


### TB3 · Terms clause 4.7.3 (which deductions on which refund route)

**Setting**: `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_FcEDdA/content` · policy `terms-of-service`

**Why**: Astra B1: 4.7.3 incorporated the deductions of 4.7.4 for every refund. It now names the only possible deduction per route: diminished value on a statutory withdrawal, none on a legal-guarantee refund, the stated ones under the voluntary guarantees.

**Legal basis**: Art. VI.50 §1, VI.51 §2 and §5 WER; Art. 1649quinquies and 1649octies old Civil Code.

**Old**

> We never charge administrative fees on a refund. The only deductions are those set out in clauses 4.3, 4.4, 4.6 and 4.7.4.

**New**

> We never charge administrative fees on a refund. On a statutory withdrawal, the only possible deduction is for diminished value under clause 4.6 (Article VI.51 §2 WER); on a refund under the legal guarantee of conformity there is none. Under our voluntary guarantees, the deductions are those set out in clauses 4.3, 4.4 and 4.7.4.


### TB4 · Terms clause 4.7.4 (Care Credit and refunds)

**Setting**: `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_FcEDdA/content` · policy `terms-of-service`

**Why**: Astra B1 (blocker; audit P1-2): spent Care Credit could be deducted from any refund, statutory withdrawal and legal-guarantee refunds included. The clause now keeps apart credit spent to pay for the order (restored), credit earned from the refunded payment (lapses from the balance, a change to the balance and never a deduction), the statutory routes (full refund, nothing deducted, spent credit not claimed back, because a consumer bears no liability for exercising the right of withdrawal and a term limiting the guarantee is void) and the voluntary routes (clauses 4.3, 4.4 and 9.9, where spent earned credit is deducted as those clauses state). Business note for Victor: releasing earned Care Credit only after the 14-day withdrawal period would remove the exposure; that is a Loop setting, not legal text.

**Legal basis**: Art. VI.50 §1 WER (reimbursement of all payments); Art. VI.51 §5 WER (“kan de consument in geen enkel opzicht aansprakelijk worden gesteld ingevolge de uitoefening van zijn herroepingsrecht”); Art. VI.63 WER (waivers deemed unwritten); Art. 13 and 14(5) Directive 2011/83/EU; Art. 1649quinquies and 1649octies old Civil Code.

**Old**

> Orders paid partly with Care Credit: the money paid goes back to your original payment method and the Care Credit you used returns to your balance. Care Credit earned from the refunded order is removed, or deducted from the refund if you already spent it. Care Credit is never paid out in cash.

**New**

> Care Credit and refunds: if you paid part of an order with Care Credit, the money you paid goes back to your original payment method and the Care Credit you used returns to your balance. Care Credit earned from a payment that is refunded lapses from your balance, because the payment it rewarded no longer exists. Under your statutory right of withdrawal (clause 4.1) and under the legal guarantee of conformity (clause 7), you always receive the full refund the law requires: we never deduct Care Credit from it, and we do not claim back Care Credit you already spent (Articles VI.50 §1, VI.51 §5 and VI.63 WER; Articles 1649quinquies and 1649octies of the old Civil Code). Only under our voluntary money-back guarantees (clauses 4.3 and 4.4) and the renewal refunds in clause 9.9 is Care Credit that was earned from the refunded payment and already spent deducted from the refund, as those clauses say. Care Credit is never paid out in cash.


### TB5 · Terms clause 7.6 (not a lack of conformity: PAO)

**Setting**: `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_EAKJLC/content` · policy `terms-of-service`

**Why**: Astra, observation 6 (non-blocker): a conformity defect that appeared before the Period After Opening or expiry date passed must not be refused because that date later passed.

**Legal basis**: Art. 1649quater §1 and §4 old Civil Code.

**Old**

> use after the PAO or the expiry date.

**New**

> use after the PAO or the expiry date, although a lack of conformity that appeared before that date stays covered.


### TB6 · Terms clause 10.6 (Care Credit, refunds)

**Setting**: `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_nEOBgC/content` · policy `terms-of-service`

**Why**: Astra B1: clause 10.6 repeated the blanket clawback for “an order that is refunded”. It now follows 4.7.4: credit used is restored, credit earned from the refunded payment lapses, nothing is deducted and nothing claimed back on the statutory routes, deduction only under the voluntary guarantees and clause 9.9.

**Legal basis**: Same as TB4.

**Old**

> Refunds: if an order is refunded, the Care Credit you used on it returns to your balance; Care Credit earned from it is removed, or deducted from the refund if you already spent it (clause 4.7).

**New**

> Refunds: if an order is refunded, the Care Credit you used on it returns to your balance and the Care Credit earned from the refunded payment lapses. On a statutory withdrawal or a refund under the legal guarantee, nothing is deducted from your refund and spent Care Credit is not claimed back; only under our voluntary guarantees and clause 9.9 is spent Care Credit earned from the refunded payment deducted (clause 4.7.4).


### CB1 · Consumer Rights section 3.1, third bullet (what a withdrawing member returns)

**Setting**: `page.consumer-rights:legal_toc_section_gYznx3/content_section_iDEfUH/content` · policy `refund-policy`

**Why**: Same as TB1, in the summary.

**Legal basis**: Art. VI.51 §1 and §5 WER.

**Old**

> • Send the goods back within 14 days of telling us. You may check them

**New**

> • Send the goods back within 14 days of telling us; for a membership that is everything delivered under it, the Welcome Kit included. You may check them


### CB2 · Consumer Rights section 3.6, step 3 (Care Credit and refunds)

**Setting**: `page.consumer-rights:legal_toc_section_gYznx3/content_section_iDEfUH/content` · policy `refund-policy`

**Why**: Astra B1, in the summary: the statutory routes refund in full with nothing deducted and spent credit not claimed back; only the money-back guarantees deduct spent credit.

**Legal basis**: Same as TB4.

**Old**

> If you paid partly with Care Credit, that credit returns to your balance. Care Credit is never paid out in cash.

**New**

> If you paid partly with Care Credit, that credit returns to your balance, and the Care Credit earned from the refunded payment lapses. Under your legal rights, nothing is deducted from your refund and spent Care Credit is not claimed back; only under our money-back guarantees (3.3 and 3.4) is spent Care Credit deducted. Care Credit is never paid out in cash.


### CB3 · Consumer Rights section 4.2.2 (serious defect)

**Setting**: `page.consumer-rights:legal_toc_section_gYznx3/content_section_FcEDdA/content` · policy `refund-policy`

**Why**: Astra, observation 5 (non-blocker): the summary omitted the serious-defect trigger for price reduction or termination that Terms 7.4 states.

**Legal basis**: Art. 1649quinquies §5, 3° old Civil Code.

**Old**

> or does not solve the problem, you can ask for a proportionate price reduction

**New**

> or does not solve the problem, or if the defect is serious enough to justify it at once, you can ask for a proportionate price reduction


## 3c. R57b add-ons from the landing desk (24 Oct): PDF links removed on Victor's instruction, gate-withdrawal handoffs: the changes, one by one (EN old → new)


### TC1 · Terms Annex (“Download the form (PDF)” placeholder)

**Setting**: `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_fz6KEQ/content` · policy `terms-of-service`

**Why**: Victor's instruction (24 Oct, through gate-withdrawal): the placeholder PDF link is removed from the designed page; the plain line is removed from the policy body so both say the same. The model form stays inline, which is what the law requires; the PDFs remain available for the confirmation email.

**Legal basis**: Art. VI.45 §1 8° and Annex 2 to Book VI WER (the model form must be provided; a download is not required).

**Old**

> Download the form (PDF)

**New**

> (removed)

**Theme only** (left menu label): “<p><a href="#" title="#"><span style="text-decoration:underline">Download the form (PDF)</span></a></p>” → “”


### CC1 · Consumer Rights section 10 (“Download the form (PDF)” placeholder)

**Setting**: `page.consumer-rights:legal_toc_section_gYznx3/content_section_at3pLy/content` · policy `refund-policy`

**Why**: Same as TC1.

**Legal basis**: Same as TC1.

**Old**

> Download the form (PDF)

**New**

> (removed)

**Theme only** (left menu label): “<p><a href="#" title="#"><span style="text-decoration:underline">Download the form (PDF)</span></a></p>” → “”


### PC1 · Privacy Policy section 5 (service providers: Klaviyo)

**Setting**: `page.privacy-policy:legal_toc_section_gYznx3/content_section_xKcNPj/content` · policy `privacy-policy`

**Why**: gate-withdrawal's handoff: the acknowledgement of an online withdrawal (Art. VI.61/2 §4 WER) is sent through Klaviyo, so Klaviyo is named as the processor of that transactional email.

**Legal basis**: Art. 13(1)(e) GDPR (recipients of the personal data); Art. 28 GDPR (processor).

**Old**

> Email and marketing automation: Klaviyo, Inc. (US), transactional and promotional email, cart reminders (only if you opted in) and list management.

**New**

> Email and marketing automation: Klaviyo, Inc. (US), transactional email (order and membership confirmations, and the acknowledgement of a withdrawal sent through the online withdrawal function), promotional email, cart reminders (only if you opted in) and list management.


### PC2 · Privacy Policy section 3 (communication data)

**Setting**: `page.privacy-policy:legal_toc_section_gYznx3/content_section_iDEfUH/content` · policy `privacy-policy`

**Why**: The online withdrawal function collects a name, an order reference and an email address (Art. VI.61/2 §2 WER); the categories of data in section 3 now say so.

**Legal basis**: Art. 13(1)(c) and 14 GDPR (categories and purposes); Art. VI.61/2 §2 WER.

**Old**

> Communication data: records of your messages by email or contact form, including product questions, after-sales questions and feedback.

**New**

> Communication data: records of your messages by email, contact form or the online withdrawal function (your name, the order reference and your email address), including product questions, after-sales questions and feedback.


## 3d. R57c, Victor's Care Credit decision (24 Oct): the linked-order choice replaces “nothing claimed back”: the changes, one by one (EN old → new)


### TD3 · Terms clause 4.7.3 (which deductions on which refund route)

**Setting**: `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_FcEDdA/content` · policy `terms-of-service`

**Why**: R57c: the statutory routes now carry one more possible item, the Care Credit set-off of clause 4.7.4 when the customer keeps the items bought with credit earned from the refunded payment.

**Legal basis**: See TD4.

**Old**

> We never charge administrative fees on a refund. On a statutory withdrawal, the only possible deduction is for diminished value under clause 4.6 (Article VI.51 §2 WER); on a refund under the legal guarantee of conformity there is none. Under our voluntary guarantees, the deductions are those set out in clauses 4.3, 4.4 and 4.7.4.

**New**

> We never charge administrative fees on a refund. On a statutory withdrawal, the only possible deductions are for diminished value under clause 4.6 (Article VI.51 §2 WER) and the Care Credit set-off under clause 4.7.4, if you keep items you bought with Care Credit earned from the refunded payment; on a refund under the legal guarantee of conformity, only that set-off. Under our voluntary guarantees, the deductions are those set out in clauses 4.3, 4.4 and 4.7.4.


### TD4 · Terms clause 4.7.4 (Care Credit and refunds: Victor's rule)

**Setting**: `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_FcEDdA/content` · policy `terms-of-service`

**Why**: R57c replaces R57b's “nothing claimed back” with Victor's narrower rule in its most defensible form: credit spent to pay is restored; credit earned from the refunded payment lapses with nothing deducted for the unused part; where that credit had already paid for another order, that order is linked and the customer chooses, when giving notice, between returning the credit-funded items at no cost (prepaid label, their money refunded, nothing set off) and keeping them and paying the credit value, which is the only amount set off against the refund; silence means set-off; the refund confirmation names the linked order and the amount; the same choice applies on every refund route; apart from it the statutory refund of the price and the standard delivery charge stays complete.

**Legal basis**: Victor's decision (landing desk, 24 Oct): “We do deduct the used credit, unless the customer also returns the product the credits were used for.” Legal basis relied on: Art. VI.50 §1 WER (we refund every payment received; the credit was never a payment received, so its lapse is not a deduction from one); Art. VI.52 §2 WER and Art. 15 CRD (withdrawal ends every linked contract at no cost to the consumer, hence the cost-free return of the credit-funded items, prepaid label included, with their money refunded); Art. VI.51 §2 WER (the set-off is not a diminished-value claim and is therefore kept on its own footing: the price reduction on the linked order was conditional on the payment that earned the credit, and when that payment is refunded the reduction falls away, so the credit value becomes due for the goods the consumer keeps and is set off against the refund under Articles 5.254–5.255 (legal set-off) or 5.263 (contractual set-off) of the new Civil Code; an earlier draft cited Art. 5.258, which concerns sureties, corrected in R57d); Art. VI.45 §1 8° WER (the conditions of withdrawal, this choice included, are stated before the contract); Art. 1649septies old Civil Code for the voluntary guarantees. Residual risk for counsel, one line: a set-off against the statutory refund of an amount that exists only because the consumer withdrew may be read as a cost imposed as a consequence of withdrawal (Art. VI.51 §5 and VI.52 §2 WER, Art. 14(5) CRD) or, on the legal guarantee, as a term limiting the remedy (Art. 1649octies); the defence is that the credit was a conditional price reduction on the linked order, the consumer keeps goods of that value or may return them at no cost, and the choice is stated before purchase (Art. VI.45 §1 8°) and on the refund confirmation.

**Old**

> Care Credit and refunds: if you paid part of an order with Care Credit, the money you paid goes back to your original payment method and the Care Credit you used returns to your balance. Care Credit earned from a payment that is refunded lapses from your balance, because the payment it rewarded no longer exists. Under your statutory right of withdrawal (clause 4.1) and under the legal guarantee of conformity (clause 7), you always receive the full refund the law requires: we never deduct Care Credit from it, and we do not claim back Care Credit you already spent (Articles VI.50 §1, VI.51 §5 and VI.63 WER; Articles 1649quinquies and 1649octies of the old Civil Code). Only under our voluntary money-back guarantees (clauses 4.3 and 4.4) and the renewal refunds in clause 9.9 is Care Credit that was earned from the refunded payment and already spent deducted from the refund, as those clauses say. Care Credit is never paid out in cash.

**New**

> Care Credit and refunds: if you paid part of an order with Care Credit, the money you paid goes back to your original payment method and the Care Credit you used returns to your balance. Care Credit earned from a payment that is refunded lapses from your balance, because the payment it rewarded no longer exists; nothing is deducted for credit you had not used. If you had already used Care Credit earned from the refunded payment to pay for another order, that order is linked to your refund and you choose, when you tell us you withdraw or ask for the refund: either you send the items you bought with that credit back to us within 14 days of telling us, with the prepaid return label we send you, and nothing is set off (we also refund any money you paid for them); or you keep them and pay the value of the Care Credit used for them, which is the only amount we set off against your refund. If you do not tell us, we apply the set-off. The refund confirmation names the linked order and the amount. This choice applies on every refund route: our voluntary guarantees (clauses 4.3 and 4.4), the renewal refunds in clause 9.9, a statutory withdrawal (clause 4.1) and a refund under the legal guarantee of conformity (clause 7). Apart from this set-off, your statutory refund of the price and the standard delivery charge is always complete (Articles VI.50 §1 and VI.51 WER; Articles 1649quinquies and 1649octies of the old Civil Code). Care Credit is never paid out in cash.


### TD6 · Terms clause 10.6 (Care Credit, refunds)

**Setting**: `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_nEOBgC/content` · policy `terms-of-service`

**Why**: R57c: clause 10.6 follows the new 4.7.4 (the linked-order choice on every refund route).

**Legal basis**: See TD4.

**Old**

> Refunds: if an order is refunded, the Care Credit you used on it returns to your balance and the Care Credit earned from the refunded payment lapses. On a statutory withdrawal or a refund under the legal guarantee, nothing is deducted from your refund and spent Care Credit is not claimed back; only under our voluntary guarantees and clause 9.9 is spent Care Credit earned from the refunded payment deducted (clause 4.7.4).

**New**

> Refunds: if an order is refunded, the Care Credit you used on it returns to your balance and the Care Credit earned from the refunded payment lapses; nothing is deducted for credit you had not used. If you had already used that credit on another order, you choose between sending the items bought with it back (nothing is set off) and keeping them (the value of the credit used for them is set off against your refund). Clause 4.7.4 has the full rule; it applies on every refund route, statutory withdrawal and legal guarantee included.


### CD2 · Consumer Rights section 3.6, step 3 (Care Credit and refunds)

**Setting**: `page.consumer-rights:legal_toc_section_gYznx3/content_section_iDEfUH/content` · policy `refund-policy`

**Why**: R57c, in the summary: the same choice, in plain words, pointing to Terms 4.7.4.

**Legal basis**: See TD4.

**Old**

> If you paid partly with Care Credit, that credit returns to your balance, and the Care Credit earned from the refunded payment lapses. Under your legal rights, nothing is deducted from your refund and spent Care Credit is not claimed back; only under our money-back guarantees (3.3 and 3.4) is spent Care Credit deducted. Care Credit is never paid out in cash.

**New**

> If you paid partly with Care Credit, that credit returns to your balance, and the Care Credit earned from the refunded payment lapses; nothing is deducted for credit you had not used. If you had already used that credit on another order, you choose: send those items back within 14 days with our prepaid label and nothing is set off, or keep them and the value of the credit used for them is set off against your refund, shown on your refund confirmation. That is the only Care Credit set-off, on every refund route, your legal rights included; clause 4.7.4 of the Terms has the full rule. Care Credit is never paid out in cash.


## 3e. R57d, the retained-benefit model after Astra's R57c review (24 Oct): no automatic statutory set-off, no silence, proportional allocation, return reconciliation: the changes, one by one (EN old → new)


### TE1 · Terms clause 4.3.3 (60-Day rhythm guarantee refund)

**Setting**: `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_FcEDdA/content` · policy `terms-of-service`

**Why**: The older unconditional deduction sentence is qualified by the return-or-keep choice of 4.7.6; “removed” becomes “lapses”.

**Legal basis**: See TE4.

**Old**

> Refund: your first membership payment, minus any Care Credit you already spent that was earned from that payment. Unused Care Credit earned from that payment is removed. The refund follows

**New**

> Refund: your first membership payment, minus the Care Credit earned from that payment that you already used on another order, unless you return the articles you bought with it (clause 4.7.6). Unused Care Credit earned from that payment lapses. The refund follows


### TE2 · Terms clause 4.4.2 (Year guarantee refund)

**Setting**: `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_FcEDdA/content` · policy `terms-of-service`

**Why**: Same as TE1.

**Legal basis**: See TE4.

**Old**

> Refund: your annual payment, minus any Care Credit you already spent that was earned from that payment. Unused Care Credit earned from that payment is removed, remaining deliveries

**New**

> Refund: your annual payment, minus the Care Credit earned from that payment that you already used on another order, unless you return the articles you bought with it (clause 4.7.6). Unused Care Credit earned from that payment lapses, remaining deliveries


### TE3 · Terms clause 4.7.3 (which deductions on which refund route)

**Setting**: `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_FcEDdA/content` · policy `terms-of-service`

**Why**: On the statutory routes a Care Credit amount is never an automatic deduction: only with the customer's express agreement under 4.7.5. The voluntary routes keep their stated deductions, now read with 4.7.6.

**Legal basis**: See TE4.

**Old**

> We never charge administrative fees on a refund. On a statutory withdrawal, the only possible deductions are for diminished value under clause 4.6 (Article VI.51 §2 WER) and the Care Credit set-off under clause 4.7.4, if you keep items you bought with Care Credit earned from the refunded payment; on a refund under the legal guarantee of conformity, only that set-off. Under our voluntary guarantees, the deductions are those set out in clauses 4.3, 4.4 and 4.7.4.

**New**

> We never charge administrative fees on a refund. On a statutory withdrawal, the only possible deduction is for diminished value under clause 4.6 (Article VI.51 §2 WER); on a refund under the legal guarantee of conformity there is none. A Care Credit amount is set off against a statutory refund only with your express agreement under clause 4.7.5. Under our voluntary guarantees and the renewal refunds, the deductions are those set out in clauses 4.3, 4.4, 9.9 and 4.7.6.


### TE4 · Terms clause 4.7.4 rewritten, 4.7.5 and 4.7.6 added (Care Credit: retained-benefit model)

**Setting**: `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_FcEDdA/content` · policy `terms-of-service`

**Why**: Astra B4. 4.7.4: tendered credit restored; earned credit lapses in proportion to the refunded amount; identification of the order, the articles and the attributable amount before the choice; return with a prepaid label within 14 days of receiving it, nothing deducted, money refunded, provisional set-off reversed; partial returns; no double counting; the attributable credit as ceiling. 4.7.5 (statutory routes): refund in full and on time whatever the choice; keep-and-pay only by express agreement after the information; silence is not agreement; no choice means refund in full and ask again; any agreed set-off limited to an enforceable amount for the articles kept. 4.7.6 (voluntary guarantees and renewal refunds): explicit return-or-keep choice; deduction if kept; return within the period reverses it.

**Legal basis**: Astra's R57c review, B4: the R57c rule made a Care Credit amount due and set off on every statutory refund, by silence, without an enforceable retained-goods obligation. R57d keeps Victor's intent (credit that has already bought something is not kept for free) in the narrower retained-benefit model: the credit tendered for the refunded order is restored; the credit earned on the amount actually refunded lapses in proportion; where part of it paid for articles on another order, we identify the order, the articles and the attributable amount before asking for a choice; the articles can be returned with a prepaid label within 14 days of receiving it, with nothing deducted for them, their money refunded and any provisional set-off reversed; partial returns count only the articles kept; no double counting, never more than the attributable credit. On the statutory routes the refund is paid in full within the legal period whatever the customer decides, a keep-and-pay arrangement needs an express agreement given after that information, silence is never agreement, and an unanswered question means refund in full and ask again. On the voluntary routes the choice is explicit and the older deduction sentences are qualified by it. Legal basis relied on: Art. VI.50 §1 and VI.51 §5 WER (the statutory refund stays intact; no liability consequent on withdrawal); CJEU C-583/18 Verbraucherzentrale Berlin v DB Vertrieb, paras 35–37 (a conditional price benefit on a legally distinct retained transaction may be recovered after withdrawal from the contract that granted it: an analogy, not a ruling on these Terms); Art. 5.20 new Civil Code (silence is not acceptance); Art. 5.254–5.255 (legal set-off needs reciprocal, certain, liquid and due debts) and Art. 5.263 (contractual set-off) new Civil Code, replacing the wrong reference to Art. 5.258, which concerns sureties; Art. 1649quinquies and 1649octies old Civil Code; Art. VI.45 §1 8° WER (stated before the contract); Art. 1649septies old Civil Code for the voluntary guarantees. Residual risk for counsel, one line: whether a loyalty credit spent on a later order creates an enforceable restitution debt for the retained articles at all is undecided in Belgian law; C-583/18 is an analogy, so even an expressly agreed set-off on a statutory refund could be challenged under Art. VI.51 §5 and VI.63 WER or Art. 1649octies, and the conservative alternative remains the b8d5ef3 statutory exclusion with Victor's return option kept for the contractual routes.

**Old**

> Care Credit and refunds: if you paid part of an order with Care Credit, the money you paid goes back to your original payment method and the Care Credit you used returns to your balance. Care Credit earned from a payment that is refunded lapses from your balance, because the payment it rewarded no longer exists; nothing is deducted for credit you had not used. If you had already used Care Credit earned from the refunded payment to pay for another order, that order is linked to your refund and you choose, when you tell us you withdraw or ask for the refund: either you send the items you bought with that credit back to us within 14 days of telling us, with the prepaid return label we send you, and nothing is set off (we also refund any money you paid for them); or you keep them and pay the value of the Care Credit used for them, which is the only amount we set off against your refund. If you do not tell us, we apply the set-off. The refund confirmation names the linked order and the amount. This choice applies on every refund route: our voluntary guarantees (clauses 4.3 and 4.4), the renewal refunds in clause 9.9, a statutory withdrawal (clause 4.1) and a refund under the legal guarantee of conformity (clause 7). Apart from this set-off, your statutory refund of the price and the standard delivery charge is always complete (Articles VI.50 §1 and VI.51 WER; Articles 1649quinquies and 1649octies of the old Civil Code). Care Credit is never paid out in cash.

**New**

> Care Credit and refunds: if you paid part of an order with Care Credit, the money you paid goes back to your original payment method and the Care Credit you used returns to your balance. Care Credit earned on an amount that is refunded lapses from your balance in proportion to that amount (a partial refund cancels only the credit earned on the part refunded), because the payment it rewarded no longer exists; nothing is deducted for lapsed credit you had not used, and we never recover unused credit in cash. If you had already used part of that credit to pay for articles on another order, we identify that order, the articles concerned and the Care Credit attributable to the amount being refunded before asking for your choice. You may return those articles with the prepaid label we send you, within 14 days of receiving it: no Care Credit is deducted for the articles returned, we refund the money you paid for them, and any set-off already applied for them is reversed. If you return some of the articles, only the credit attributable to the articles you keep can be counted. The same credit is never counted twice, and no amount ever exceeds the credit attributable to the articles you keep. What applies when you keep the articles depends on the refund route: clause 4.7.5 for your statutory rights, clause 4.7.6 for our voluntary guarantees and renewal refunds. Care Credit is never paid out in cash.
> • Care Credit on a statutory withdrawal or a legal-guarantee refund: your statutory refund (clauses 4.1 and 7) is paid in full and within the legal period whatever you decide about the articles. Any arrangement to keep the articles and pay the Care Credit attributable to them must be lawful and expressly agreed by you after we have given you the information in clause 4.7.4. We do not treat silence as agreement, and we do not delay or reduce the refund required by your statutory rights while seeking that agreement; if you do not choose, we refund in full and ask you again about the articles. Any agreed set-off is limited to an enforceable amount for the articles you keep and never recovers the same credit twice (Articles VI.50 §1 and VI.51 §5 WER; Articles 1649quinquies and 1649octies of the old Civil Code; Articles 5.254, 5.255 and 5.263 of the Civil Code).
> • Care Credit under our voluntary guarantees and renewal refunds: under the money-back guarantees in clauses 4.3 and 4.4 and the renewal refunds in clause 9.9, you choose, after we have given you the information in clause 4.7.4, between returning the articles you bought with the credit attributable to the refunded amount (nothing is deducted for them) and keeping them, in which case that credit is deducted from the refund, as those clauses say. If you do not choose, we deduct it; if you still return the articles within the period in clause 4.7.4, we reverse the deduction. The deduction never exceeds the credit attributable to the articles you keep.


### TE5 · Terms clause 9.9 (renewal refunds, Care Credit sentence)

**Setting**: `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_CDtWCV/content` · policy `terms-of-service`

**Why**: The renewal-refund sentence now names the return alternative and points to 4.7.6; it keeps the narrower “refunded amount” formulation Astra praised. The subscription policy quotes clause 9 word for word and changes with it.

**Legal basis**: See TE4.

**Old**

> Care Credit earned on a refunded amount is removed, or deducted if you already spent it (clause 4.7).

**New**

> Care Credit earned on the refunded amount lapses; if you had already used it to pay for articles on another order, you may return those articles instead of having that credit deducted (clause 4.7.6).


### SE1 · Purchase options cancellation policy (subscription policy = Terms clause 9, word for word), 9.9

**Setting**: none (policy body only) · policy `subscription-policy`

**Why**: Same sentence as TE5 in the policy that quotes clause 9.

**Legal basis**: See TE4.

**Old**

> Care Credit earned on a refunded amount is removed, or deducted if you already spent it (clause 4.7).

**New**

> Care Credit earned on the refunded amount lapses; if you had already used it to pay for articles on another order, you may return those articles instead of having that credit deducted (clause 4.7.6).


### TE6 · Terms clause 10.6 (Care Credit, refunds)

**Setting**: `page.terms-and-conditions:legal_toc_section_gYznx3/content_section_nEOBgC/content` · policy `terms-of-service`

**Why**: Follows the new 4.7.4 to 4.7.6: proportional lapse, information before the choice, express agreement on the statutory routes, deduction on the voluntary routes.

**Legal basis**: See TE4.

**Old**

> Refunds: if an order is refunded, the Care Credit you used on it returns to your balance and the Care Credit earned from the refunded payment lapses; nothing is deducted for credit you had not used. If you had already used that credit on another order, you choose between sending the items bought with it back (nothing is set off) and keeping them (the value of the credit used for them is set off against your refund). Clause 4.7.4 has the full rule; it applies on every refund route, statutory withdrawal and legal guarantee included.

**New**

> Refunds: if an order is refunded, the Care Credit you used on it returns to your balance and the Care Credit earned on the refunded amount lapses in proportion; nothing is deducted for credit you had not used. If you had already used that credit on articles of another order, we tell you which order, which articles and which amount before you choose: return those articles (nothing deducted, your money for them refunded) or keep them. On a statutory withdrawal or a legal-guarantee refund, keeping them and paying the credit needs your express agreement and never delays or reduces your statutory refund; under our voluntary guarantees and renewal refunds, that credit is deducted. Clauses 4.7.4 to 4.7.6 have the full rule.


### CE1 · Consumer Rights section 3.3, second bullet (60-Day rhythm guarantee)

**Setting**: `page.consumer-rights:legal_toc_section_gYznx3/content_section_iDEfUH/content` · policy `refund-policy`

**Why**: Same as TE1, in the summary.

**Legal basis**: See TE4.

**Old**

> Care Credit you already spent from that payment is deducted; unused credit from it is removed.

**New**

> Care Credit from that payment that you already used on another order is deducted, unless you return what you bought with it (Terms 4.7.6); unused credit from it lapses.


### CE2 · Consumer Rights section 3.4, first bullet (Year guarantee)

**Setting**: `page.consumer-rights:legal_toc_section_gYznx3/content_section_iDEfUH/content` · policy `refund-policy`

**Why**: Same as TE2, in the summary.

**Legal basis**: See TE4.

**Old**

> we refund your annual payment, minus any Care Credit you already spent from it. Unused credit from it is removed, and your remaining deliveries are cancelled.

**New**

> we refund your annual payment, minus any Care Credit from it that you already used on another order, unless you return what you bought with it (Terms 4.7.6). Unused credit from it lapses, and your remaining deliveries are cancelled.


### CE3 · Consumer Rights section 3.6, step 3 (Care Credit and refunds)

**Setting**: `page.consumer-rights:legal_toc_section_gYznx3/content_section_iDEfUH/content` · policy `refund-policy`

**Why**: The summary of 4.7.4 to 4.7.6 in plain words: proportional lapse, information before the choice, prepaid return with money refunded, express agreement on the legal routes with no silence and no delay, deduction under the money-back guarantees.

**Legal basis**: See TE4.

**Old**

> If you paid partly with Care Credit, that credit returns to your balance, and the Care Credit earned from the refunded payment lapses; nothing is deducted for credit you had not used. If you had already used that credit on another order, you choose: send those items back within 14 days with our prepaid label and nothing is set off, or keep them and the value of the credit used for them is set off against your refund, shown on your refund confirmation. That is the only Care Credit set-off, on every refund route, your legal rights included; clause 4.7.4 of the Terms has the full rule. Care Credit is never paid out in cash.

**New**

> If you paid partly with Care Credit, that credit returns to your balance, and the Care Credit earned on the refunded amount lapses in proportion; nothing is deducted for credit you had not used. If you had already used that credit on articles of another order, we tell you which order, which articles and which amount before you choose. You may return those articles with our prepaid label within 14 days of receiving it: nothing is deducted for them and we refund the money you paid for them. Under your legal rights, keeping them and paying that credit needs your express agreement, given after that information; we never treat silence as agreement and never delay or reduce your legal refund while asking. Under our money-back guarantees (3.3 and 3.4), that credit is deducted if you keep them. Clauses 4.7.4 to 4.7.6 of the Terms have the full rule. Care Credit is never paid out in cash.


## 3f. R61b privacy handoff from gate-consent (24 Oct, commit 857c500), applied in R57d: regional consent wording for Hotjar and the cookie section: the changes, one by one (EN old → new)


### PF1 · Privacy Policy section 9 (cookies): lead, 9.1 analytics and marketing bullets, 9.2 second paragraph

**Setting**: `page.privacy-policy:legal_toc_section_gYznx3/content_section_CDtWCV/content` · policy `privacy-policy`

**Why**: The page promised everyone that nothing non-essential runs before opt-in; the loader is regional since R61. 9.2 now states the regional rule, the opt-out link and GPC, the real footer label (“Cookie preferences”) and the effect of a withdrawal from the next page; the lead and the two 9.1 bullets are qualified so they no longer contradict 9.2 (handoff item 3, gate-legal's call).

**Legal basis**: gate-consent's `docs/launch-gate/consent/PRIVACY-HANDOFF.md` (commit 857c500, after Astra's R61 review, N1): since R61 the theme loads Hotjar by region, following Shopify's Customer Privacy defaults (banner regions EU/EEA, UK and Switzerland: only after Accept; elsewhere by default unless “Your privacy choices” or a Global Privacy Control signal); the universal promise had to become regional. Art. 13(1)(c) and (e) GDPR (purposes, recipients); Art. 5(3) ePrivacy Directive and Art. 10/2 of the Belgian Data Protection Act of 30 July 2018 (prior consent in the EEA). Conditions for Victor before the paste: the Customer-privacy region list contains EU/EEA, UK and Switzerland (else drop “Switzerland”); the Data Sharing Opt-Out Page is on for the opt-out regions (else drop the “Your privacy choices” clause); keystroke masking is on in Hotjar for site 1364127 (else drop “with keystroke masking”).

**Old**

> Everything else waits for your consent, and you can change your mind at any time.

**New**

> Everything else waits for your consent where the law requires it, and you can change your mind at any time.

**Old**

> Active only after your explicit consent.

**New**

> Active only after your explicit consent in the regions named in 9.2.

**Old**

> No non-essential cookies or tracking scripts run before you opt in. You can change or withdraw your choice at any time through the “Cookie settings” link in our footer.

**New**

> In the European Economic Area, the United Kingdom and Switzerland, no non-essential cookies or tracking scripts run before you opt in. Elsewhere, analytics and advertising technologies may run by default; where the law gives you a right to opt out of the sale or sharing of your data, you can use the “Your privacy choices” link in our footer or a Global Privacy Control signal in your browser, and we honour it. You can change or withdraw your choice at any time through the “Cookie preferences” link in our footer. A withdrawal takes effect from the next page you open; the page you are on keeps running until you leave it.


### PF2 · Privacy Policy section 5, “Analytics and optimisation”, the Hotjar clause

**Setting**: `page.privacy-policy:legal_toc_section_gYznx3/content_section_xKcNPj/content` · policy `privacy-policy`

**Why**: Same regional rule for the Hotjar recipient entry (handoff item 2); “with keystroke masking” stays only if Victor confirms it in Hotjar.

**Legal basis**: gate-consent's `docs/launch-gate/consent/PRIVACY-HANDOFF.md` (commit 857c500, after Astra's R61 review, N1): since R61 the theme loads Hotjar by region, following Shopify's Customer Privacy defaults (banner regions EU/EEA, UK and Switzerland: only after Accept; elsewhere by default unless “Your privacy choices” or a Global Privacy Control signal); the universal promise had to become regional. Art. 13(1)(c) and (e) GDPR (purposes, recipients); Art. 5(3) ePrivacy Directive and Art. 10/2 of the Belgian Data Protection Act of 30 July 2018 (prior consent in the EEA). Conditions for Victor before the paste: the Customer-privacy region list contains EU/EEA, UK and Switzerland (else drop “Switzerland”); the Data Sharing Opt-Out Page is on for the opt-out regions (else drop the “Your privacy choices” clause); keystroke masking is on in Hotjar for site 1364127 (else drop “with keystroke masking”).

**Old**

> Hotjar Ltd. (Malta), heatmaps and session analysis, with your consent and keystroke masking

**New**

> Hotjar Ltd. (Malta), heatmaps and session analysis, with keystroke masking; in the EEA, the UK and Switzerland only with your consent, elsewhere by default unless you opt out


## 3g. R57e, final privacy round (24 Oct, gate-consent commit 938811c, Astra R57d B1 and B2): page-off text without an opt-out promise, immediate withdrawal, Shopify Network Intelligence: the changes, one by one (EN old → new)


### PG1 · Privacy Policy section 9: the two 9.1 bullets and the 9.2 second paragraph (page-off text, immediate withdrawal)

**Setting**: `page.privacy-policy:legal_toc_section_gYznx3/content_section_CDtWCV/content` · policy `privacy-policy`

**Why**: Astra R57d B1 and B2: the published text may not promise the opt-out link or GPC handling while the Data Sharing Opt-Out Page is inactive, and a withdrawal must take effect at once. The 9.1 bullets carry the regional ending without an opt-out clause; 9.2 ends its second sentence after “may run by default”, keeps the real “Cookie preferences” label and says the withdrawal takes effect immediately, the page refreshing once (this lane stops there and does not promise cookie deletion, as the handoff allows).

**Legal basis**: gate-consent's `docs/launch-gate/consent/PRIVACY-HANDOFF.md` at commit 938811c (R61b, R61c, R61d), after Astra's R57d review: B1, the Data Sharing Opt-Out Page is inactive (Victor's admin, 24 Oct), so the text may promise neither a “Your privacy choices” link nor Global Privacy Control handling (the loader only reads the permission Shopify derives, and Shopify derives it only where that page is active); B2, the loader now expires Hotjar's site cookies and reloads the page once, so a withdrawal takes effect immediately. Art. 13(1)(c) and (e) GDPR; Art. 7(3) GDPR (withdrawal as easy as consent); Art. 5(3) ePrivacy Directive and Art. 10/2 Belgian Data Protection Act. Shopify Network Intelligence: enabled (Victor, 24 Oct); Shopify requires the cookie banner to name Shopify and the privacy policy to link the Shopify Consumer Privacy Policy; roles under Shopify's Data Processing Addendum of 7 July 2026 and the lawful basis for enabling the feature are for counsel.

**Old**

> Active only after your explicit consent in the regions named in 9.2.

**New**

> In the European Economic Area, the United Kingdom and Switzerland active only after your explicit consent; elsewhere by default (see 9.2).

**Old**

> In the European Economic Area, the United Kingdom and Switzerland, no non-essential cookies or tracking scripts run before you opt in. Elsewhere, analytics and advertising technologies may run by default; where the law gives you a right to opt out of the sale or sharing of your data, you can use the “Your privacy choices” link in our footer or a Global Privacy Control signal in your browser, and we honour it. You can change or withdraw your choice at any time through the “Cookie preferences” link in our footer. A withdrawal takes effect from the next page you open; the page you are on keeps running until you leave it.

**New**

> In the European Economic Area, the United Kingdom and Switzerland, no non-essential cookies or tracking scripts run before you opt in. Elsewhere, analytics and advertising technologies may run by default. You can change or withdraw your choice at any time through the “Cookie preferences” link in our footer. A withdrawal takes effect immediately: the page refreshes once.


### PG2 · Privacy Policy section 5, the Hotjar clause (page-off)

**Setting**: `page.privacy-policy:legal_toc_section_gYznx3/content_section_xKcNPj/content` · policy `privacy-policy`

**Why**: Same as PG1: no “unless you opt out” while the opt-out page is inactive (Astra R61c N2).

**Legal basis**: gate-consent's `docs/launch-gate/consent/PRIVACY-HANDOFF.md` at commit 938811c (R61b, R61c, R61d), after Astra's R57d review: B1, the Data Sharing Opt-Out Page is inactive (Victor's admin, 24 Oct), so the text may promise neither a “Your privacy choices” link nor Global Privacy Control handling (the loader only reads the permission Shopify derives, and Shopify derives it only where that page is active); B2, the loader now expires Hotjar's site cookies and reloads the page once, so a withdrawal takes effect immediately. Art. 13(1)(c) and (e) GDPR; Art. 7(3) GDPR (withdrawal as easy as consent); Art. 5(3) ePrivacy Directive and Art. 10/2 Belgian Data Protection Act. Shopify Network Intelligence: enabled (Victor, 24 Oct); Shopify requires the cookie banner to name Shopify and the privacy policy to link the Shopify Consumer Privacy Policy; roles under Shopify's Data Processing Addendum of 7 July 2026 and the lawful basis for enabling the feature are for counsel.

**Old**

> , elsewhere by default unless you opt out

**New**

> , elsewhere by default


### PG3 · Privacy Policy section 5, new paragraph after the processor list: Shopify Network Intelligence

**Setting**: `page.privacy-policy:legal_toc_section_gYznx3/content_section_xKcNPj/content` · policy `privacy-policy`

**Why**: Victor keeps Shopify Network Intelligence enabled (24 Oct) and wants the privacy policy to say so; Shopify requires the link to its Consumer Privacy Policy when the feature is on. The paragraph states what Shopify does with customer and device data from the shop, that no other merchant can access it, the effect of declining non-essential cookies, and Shopify's own opt-out. The sale/sharing sentence waits for the opt-out page.

**Legal basis**: gate-consent's `docs/launch-gate/consent/PRIVACY-HANDOFF.md` at commit 938811c (R61b, R61c, R61d), after Astra's R57d review: B1, the Data Sharing Opt-Out Page is inactive (Victor's admin, 24 Oct), so the text may promise neither a “Your privacy choices” link nor Global Privacy Control handling (the loader only reads the permission Shopify derives, and Shopify derives it only where that page is active); B2, the loader now expires Hotjar's site cookies and reloads the page once, so a withdrawal takes effect immediately. Art. 13(1)(c) and (e) GDPR; Art. 7(3) GDPR (withdrawal as easy as consent); Art. 5(3) ePrivacy Directive and Art. 10/2 Belgian Data Protection Act. Shopify Network Intelligence: enabled (Victor, 24 Oct); Shopify requires the cookie banner to name Shopify and the privacy policy to link the Shopify Consumer Privacy Policy; roles under Shopify's Data Processing Addendum of 7 July 2026 and the lawful basis for enabling the feature are for counsel.

**Old**

> only where the law strictly requires it.

**New**

> only where the law strictly requires it.
> Shopify Network Intelligence. Our shop runs on Shopify. We have enabled Shopify Network Intelligence, which means Shopify uses customer and device data from our shop together with data from other Shopify shops to generate insights that power Shopify's enhanced services: improved products and personalisation, shop performance, and advertising and discovery tools such as Shopify Audiences, the Shop app, Shopify Email, Shopify Collabs and Search & Discovery. No other merchant can access our customer data. If you decline non-essential cookies on our site, the device data from your visit to our shop is not used for these non-essential purposes, advertising included. Shopify describes this processing in the Shopify Consumer Privacy Policy and offers its own opt-out for marketing based on your interactions with Shopify shops at privacy.shopify.com.


## 3h. R57f, after Astra's R57e review (24 Oct): controller framing in privacy section 5, conditional-reload withdrawal sentence in 9.2: the changes, one by one (EN old → new)


### PH1 · Privacy Policy section 5: lead, the recipients sentence, and the role sentence in the Network Intelligence paragraph

**Setting**: `page.privacy-policy:legal_toc_section_gYznx3/content_section_xKcNPj/content` · policy `privacy-policy`

**Why**: Astra R57e B2 (controller framing): the blanket “processors who act on our written instructions” description contradicted the Network Intelligence disclosure that follows it. Astra's wording, mirrored in EN/NL/FR.

**Legal basis**: Astra's R57e review (`docs/runtime-review/R57E-PRIVACY-FINAL-ASTRA.md`), exact wording. B2: section 5 described every recipient as a processor acting on our written instructions, while Shopify's Data Processing Addendum of 7 July 2026 (Purpose and Appendix E, Enhanced Services) makes Shopify a controller for Network Intelligence; the instructions/DPA statement is now confined to processing on our behalf and Shopify's documented role is stated. Art. 13(1)(e) GDPR (recipients); Art. 4(7) and (8) GDPR (controller, processor). B1: the loader could drop a repeat withdrawal inside its five-second guard; gate-consent corrects it (R61e) and the sentence now describes the actual trigger (a reload only when Hotjar is running and analytics consent is withdrawn). Belgian DPA, withdrawal of consent and cookie checklist p. 3; Art. 7(3) GDPR. Counsel still confirms the governing agreement version, the roles, the lawful basis and consents for Network Intelligence, the disclosure duties under Shopify's Terms §9.2.5, and the lawful basis for default analytics outside the banner regions.

**Old**

> We never sell your data. A small set of service providers helps us run the shop, each under a written data processing agreement.

**New**

> We never sell your data. The service providers and other recipients below help us run the shop.

**Old**

> We share data strictly on a need-to-know basis with vetted service providers (processors) who act on our written instructions under data processing agreements (DPAs):

**New**

> Where a service provider processes personal data on our behalf, it acts on our written instructions under a data processing agreement. Recipients include:

**Old**

> Shopify Collabs and Search & Discovery. No other merchant

**New**

> Shopify Collabs and Search & Discovery. For these enhanced services, Shopify acts as a data controller under its Data Processing Addendum. No other merchant


### PH2 · Privacy Policy section 9.2, the withdrawal sentence (conditional reload)

**Setting**: `page.privacy-policy:legal_toc_section_gYznx3/content_section_CDtWCV/content` · policy `privacy-policy`

**Why**: Astra R57e B1: the sentence now describes the actual trigger, a single reload only when analytics consent is withdrawn while Hotjar is running, in Astra's wording; the corrected loader (gate-consent R61e, a repeat withdrawal within the guard window is never dropped) deploys with it.

**Legal basis**: Astra's R57e review (`docs/runtime-review/R57E-PRIVACY-FINAL-ASTRA.md`), exact wording. B2: section 5 described every recipient as a processor acting on our written instructions, while Shopify's Data Processing Addendum of 7 July 2026 (Purpose and Appendix E, Enhanced Services) makes Shopify a controller for Network Intelligence; the instructions/DPA statement is now confined to processing on our behalf and Shopify's documented role is stated. Art. 13(1)(e) GDPR (recipients); Art. 4(7) and (8) GDPR (controller, processor). B1: the loader could drop a repeat withdrawal inside its five-second guard; gate-consent corrects it (R61e) and the sentence now describes the actual trigger (a reload only when Hotjar is running and analytics consent is withdrawn). Belgian DPA, withdrawal of consent and cookie checklist p. 3; Art. 7(3) GDPR. Counsel still confirms the governing agreement version, the roles, the lawful basis and consents for Network Intelligence, the disclosure duties under Shopify's Terms §9.2.5, and the lawful basis for default analytics outside the banner regions.

**Old**

> A withdrawal takes effect immediately: the page refreshes once.

**New**

> A withdrawal takes effect immediately. If you withdraw analytics consent while Hotjar is running, the page refreshes once to stop it.


## 3i. R57g, wording only (24 Oct, Astra's combined R61e/R57f report): the single withdrawal sentence in 9.2: the changes, one by one (EN old → new)


### PI1 · Privacy Policy section 9.2, the withdrawal sentence (one sentence, Astra's exact text)

**Setting**: `page.privacy-policy:legal_toc_section_gYznx3/content_section_CDtWCV/content` · policy `privacy-policy`

**Why**: Astra's combined R61e/R57f report (gate-consent `docs/runtime-review/R61E-R57F-WITHDRAWAL-PRIVACY-FINAL-ASTRA.md`, lines 34–42): one sentence that keeps the Hotjar condition and states the measured timing (cookies deleted at once, reload within a few seconds), dropping the separate blanket “A withdrawal takes effect immediately”; the footer-choice sentence before it stays.

**Legal basis**: Art. 7(3) GDPR; Belgian DPA, withdrawal of consent. The condition assumes the deployment configuration (this loader owns Hotjar, the app embed is off); counsel keeps the assessment of the short teardown interval.

**Old**

> A withdrawal takes effect immediately. If you withdraw analytics consent while Hotjar is running, the page refreshes once to stop it.

**New**

> If you withdraw analytics consent while Hotjar is running, the analytics cookies Hotjar set on our site are deleted immediately, and the page refreshes within a few seconds to stop recording.


## 3j. R57h, landing desk (24 Oct): the Terms link in the Purchase options cancellation policy points to the designed Terms page: the changes, one by one (EN old → new)


### SJ1 · Purchase options cancellation policy, first sentence: the “Terms and Conditions” link target (EN/NL/FR)

**Setting**: none (policy body only) · policy `subscription-policy`

**Why**: Landing desk, 24 Oct, after pasting the four EN policies: the link pointed to https://www.karmicare.com/en/pages/terms-and-conditions, which today still serves the old Webflow terms, so the checkout policy sent customers to the outdated conditions. The link now goes to the designed Terms page, relative and per language, like the /pages/withdrawal links; 03-REDIRECTS.csv sends the old URL there after the cutover. No words change.

**Legal basis**: Art. VI.45 §1 WER (the pre-contractual information must reach the current terms); LR1 standard “checkout links must reach the current terms”.

**Old**

> Terms and Conditions

**New**

> Terms and Conditions


## 3k. R57i, NL/FR addresses in local form (Victor 25 Oct, source-copy round 4): the changes, one by one (EN old → new)


### AK1 · Terms of service (NL/FR): header, clause 1, clause 4.7.2 return address, clause 15.2 mediation and ECC, Annex

**Setting**: `page.terms-and-conditions:(policy only)` · policy `terms-of-service`

**Why**: Victor (25 Oct, landing desk “2a, ga je gang”): NL and FR write postal addresses in their local form, as source-copy round 4 (0baa6f4, ROUND4.md) does in the legal template rows: NL Belgium → België, Bruges → Brugge, Brussels → Brussel, box → bus; FR Belgium → Belgique, Brussels → Bruxelles, box → boîte. Street names stay as in the EN (Vizierstraat, Boulevard du Roi Albert II, Koning Albert II-laan, Drukpersstraat); EN stays “Bruges, Belgium”. Only address spans change; “Brussel I bis” / “Bruxelles I bis”, the court seat “afdeling Brugge” / “division Bruges” and running text are untouched. Policy bodies only: the theme NL/FR values are source-copy's.

**Legal basis**: Victor's decision of 25 Oct; source-copy `docs/localization/registration/ROUND4.md` at 0baa6f4 (decision 1) and its NL/FR batch-04 rows, read only.


### AK2 · Refund policy (NL/FR): header, 3.6.4 return address, 8.1 mediation, 8.2 ECC, section 10

**Setting**: `page.consumer-rights:(policy only)` · policy `refund-policy`

**Why**: Victor (25 Oct, landing desk “2a, ga je gang”): NL and FR write postal addresses in their local form, as source-copy round 4 (0baa6f4, ROUND4.md) does in the legal template rows: NL Belgium → België, Bruges → Brugge, Brussels → Brussel, box → bus; FR Belgium → Belgique, Brussels → Bruxelles, box → boîte. Street names stay as in the EN (Vizierstraat, Boulevard du Roi Albert II, Koning Albert II-laan, Drukpersstraat); EN stays “Bruges, Belgium”. Only address spans change; “Brussel I bis” / “Bruxelles I bis”, the court seat “afdeling Brugge” / “division Bruges” and running text are untouched. Policy bodies only: the theme NL/FR values are source-copy's.

**Legal basis**: Victor's decision of 25 Oct; source-copy `docs/localization/registration/ROUND4.md` at 0baa6f4 (decision 1) and its NL/FR batch-04 rows, read only.


### AK3 · Privacy policy (NL/FR): header, section 2 controller, section 8 postal address and Data Protection Authority

**Setting**: `page.privacy-policy:(policy only)` · policy `privacy-policy`

**Why**: Victor (25 Oct, landing desk “2a, ga je gang”): NL and FR write postal addresses in their local form, as source-copy round 4 (0baa6f4, ROUND4.md) does in the legal template rows: NL Belgium → België, Bruges → Brugge, Brussels → Brussel, box → bus; FR Belgium → Belgique, Brussels → Bruxelles, box → boîte. Street names stay as in the EN (Vizierstraat, Boulevard du Roi Albert II, Koning Albert II-laan, Drukpersstraat); EN stays “Bruges, Belgium”. Only address spans change; “Brussel I bis” / “Bruxelles I bis”, the court seat “afdeling Brugge” / “division Bruges” and running text are untouched. Policy bodies only: the theme NL/FR values are source-copy's.

**Legal basis**: Victor's decision of 25 Oct; source-copy `docs/localization/registration/ROUND4.md` at 0baa6f4 (decision 1) and its NL/FR batch-04 rows, read only.


## 3l. R57j, NL/FR department names and the addresses in Contact information and Legal notice (Victor 25 Oct): the changes, one by one (EN old → new)


### DL1 · Terms of service (NL/FR), clause 4.7.2: the returns department

**Setting**: `page.terms-and-conditions:(policy only)` · policy `terms-of-service`

**Why**: Victor (25 Oct, landing desk “ja gate legal in een keer laten rechtzetten”): FR “Returns Department” becomes “Service des retours”; NL uses “afdeling Retouren” everywhere (the Terms had “Retourafdeling”); “Privacy Operations” becomes FR “Service Vie privée” and NL “afdeling Privacy”. EN keeps “Returns Department” and “Privacy Operations”. Source-copy applies the same terms to the legal template rows of the theme pages (the landing desk aligns the two).

**Legal basis**: Victor's decision of 25 Oct.


### DL2 · Refund policy (FR), section 3.6.4: the returns department (NL already “afdeling Retouren”)

**Setting**: `page.consumer-rights:(policy only)` · policy `refund-policy`

**Why**: Victor (25 Oct, landing desk “ja gate legal in een keer laten rechtzetten”): FR “Returns Department” becomes “Service des retours”; NL uses “afdeling Retouren” everywhere (the Terms had “Retourafdeling”); “Privacy Operations” becomes FR “Service Vie privée” and NL “afdeling Privacy”. EN keeps “Returns Department” and “Privacy Operations”. Source-copy applies the same terms to the legal template rows of the theme pages (the landing desk aligns the two).

**Legal basis**: Victor's decision of 25 Oct.


### DL3 · Privacy policy (NL/FR), section 8: the privacy department

**Setting**: `page.privacy-policy:(policy only)` · policy `privacy-policy`

**Why**: Victor (25 Oct, landing desk “ja gate legal in een keer laten rechtzetten”): FR “Returns Department” becomes “Service des retours”; NL uses “afdeling Retouren” everywhere (the Terms had “Retourafdeling”); “Privacy Operations” becomes FR “Service Vie privée” and NL “afdeling Privacy”. EN keeps “Returns Department” and “Privacy Operations”. Source-copy applies the same terms to the legal template rows of the theme pages (the landing desk aligns the two).

**Legal basis**: Victor's decision of 25 Oct.


### AL1 · Contact information (NL/FR), clause 1 address

**Setting**: none (policy body only) · policy `contact-information`

**Why**: Victor (25 Oct, landing desk “2a, ga je gang”): NL and FR write postal addresses in their local form, as source-copy round 4 (0baa6f4, ROUND4.md) does in the legal template rows: NL Belgium → België, Bruges → Brugge, Brussels → Brussel, box → bus; FR Belgium → Belgique, Brussels → Bruxelles, box → boîte. Street names stay as in the EN (Vizierstraat, Boulevard du Roi Albert II, Koning Albert II-laan, Drukpersstraat); EN stays “Bruges, Belgium”. Only address spans change; “Brussel I bis” / “Bruxelles I bis”, the court seat “afdeling Brugge” / “division Bruges” and running text are untouched. Policy bodies only: the theme NL/FR values are source-copy's. Extended on 25 Oct to Contact information and Legal notice, which in Translate & Adapt still had “8000 Bruges, Belgium” in NL and FR; both join the paste file in NL and FR only (EN unchanged). Shipping policy has no postal address (“Belgium/België/Belgique” there is a delivery zone) and does not change.

**Legal basis**: Victor's decision of 25 Oct; source-copy `docs/localization/registration/ROUND4.md` at 0baa6f4 (decision 1) and its NL/FR batch-04 rows, read only.


### AL2 · Legal notice (NL/FR), clause 1 address

**Setting**: none (policy body only) · policy `legal-notice`

**Why**: Victor (25 Oct, landing desk “2a, ga je gang”): NL and FR write postal addresses in their local form, as source-copy round 4 (0baa6f4, ROUND4.md) does in the legal template rows: NL Belgium → België, Bruges → Brugge, Brussels → Brussel, box → bus; FR Belgium → Belgique, Brussels → Bruxelles, box → boîte. Street names stay as in the EN (Vizierstraat, Boulevard du Roi Albert II, Koning Albert II-laan, Drukpersstraat); EN stays “Bruges, Belgium”. Only address spans change; “Brussel I bis” / “Bruxelles I bis”, the court seat “afdeling Brugge” / “division Bruges” and running text are untouched. Policy bodies only: the theme NL/FR values are source-copy's. Extended on 25 Oct to Contact information and Legal notice, which in Translate & Adapt still had “8000 Bruges, Belgium” in NL and FR; both join the paste file in NL and FR only (EN unchanged). Shipping policy has no postal address (“Belgium/België/Belgique” there is a delivery zone) and does not change.

**Legal basis**: Victor's decision of 25 Oct; source-copy `docs/localization/registration/ROUND4.md` at 0baa6f4 (decision 1) and its NL/FR batch-04 rows, read only.


## 4. What was verified, and where (24 Oct 2026)

| Rule used in the text | Source read today | Link |
|---|---|---|
| 14-day period; start at physical possession; for a contract for regular delivery of goods, at the first delivery | Art. VI.47 §1 and §2 WER, consolidated Justel text | https://www.ejustice.just.fgov.be/eli/wet/2013/02/28/2013A11134/justel |
| How to withdraw: model form or any other unambiguous statement; sending before the end of the period is enough | Art. VI.49 §1 and §2 WER (same text) | same |
| Refund of all payments including delivery costs, without undue delay and within 14 days of the day the trader is informed; same payment means; may withhold until the goods are back or proof of sending is supplied, whichever first | Art. VI.50 §1 and §3 WER (same text); FPS Economy news page and ConsumerConnect (“binnen de 14 dagen nadat je … hebt laten weten”) | https://news.economie.fgov.be/270128-een-impulsieve-online-aankoop-er-is-een-weg-terug/ · https://consumerconnect.be/nl/themas/aankoop-product-of-dienst/herroepingsrecht/aankoop-op-afstand/geld-niet-terug |
| Consumer returns within 14 days and pays the direct return cost; liable only for diminished value from handling beyond what is needed to establish nature, characteristics and functioning; never liable if the withdrawal information was missing; **no other liability whatsoever for exercising the right (§5)** | Art. VI.51 §1, §2 and §5 WER (same text: “kan de consument in geen enkel opzicht aansprakelijk worden gesteld ingevolge de uitoefening van zijn herroepingsrecht”) | same as Justel |
| Terms by which the consumer waives the rights of this section are deemed unwritten | Art. VI.63 WER (same text) | same |
| Confirmation of the contract on a durable medium within a reasonable time and at the latest at delivery, containing all the Art. VI.45 §1 information (withdrawal information and model form included) unless already given on a durable medium before the contract | Art. VI.46 §7 WER (same text); CJEU C-49/11 Content Services (a link to a website is not a durable medium) | same; https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX%3A62011CJ0049 |
| Hygiene exception needs sealed goods whose seal was broken after delivery | Art. VI.53, 5° WER (same text); CJEU C-681/17 (slewo) as cited in the audit | same |
| Pre-contract information must say that the withdrawal function exists and where it is | Art. VI.45 §1, 8° WER as amended (“… en, in voorkomend geval, informatie over de beschikbaarheid en de plaats van de herroepingsfunctie bedoeld in artikel VI.61/2”) | same |
| The online withdrawal function: label “hier de overeenkomst herroepen” / “renoncer au contrat ici”, available during the whole period, name + contract data + e-mail, “herroeping bevestigen” / “confirmer la rétractation”, acknowledgement on a durable medium with content, date and time | Art. VI.61/2 WER, inserted by the Act of 19 July 2026 (W 2026-07-19/05, art. 23), in force 14 August 2026 (Justel annotation); Astra verified both labels against the Moniteur of 4 August 2026, p. 56 | same; https://www.ejustice.just.fgov.be/mopdf/2026/08/04_1.pdf#page=56 |
| EU basis of the above | Art. 13, 14 and 16(e) of Directive 2011/83/EU (text checked on the legislation.gov.uk mirror because EUR-Lex refuses automated reads); Art. 11a inserted by Directive (EU) 2023/2673, applicable 19 June 2026 | https://eur-lex.europa.eu/eli/dir/2011/83/oj · https://eur-lex.europa.eu/eli/dir/2023/2673/oj |
| Conformity requirements (description, fitness, quality and durability normal for the goods, public statements) | Art. 1649ter old Civil Code, as replaced by the Law of 20 March 2022 (in force 1 June 2022) | https://www.kustcodex.be/kustcodex-consult/plainWettekstServlet?wettekstId=31650&lang=nl |
| Two-year liability (§1), two-month notification (§2), two-year presumption “tot bewijs van het tegendeel”, unless incompatible with the nature of the goods or of the defect (§4) | Art. 1649quater old Civil Code | …wettekstId=31651 |
| Consumer chooses repair or replacement unless impossible or disproportionate (§§1–2); price reduction or termination when not done, refused, persisting, serious (§5); no termination for a minor defect, seller proves it is minor | Art. 1649quinquies old Civil Code; FPS Economy and ConsumerConnect guarantee pages | …wettekstId=31652 · https://news.economie.fgov.be/214976-wettelijke-garantie-consument-is-beter-beschermd/ |
| A commercial guarantee binds on its stated terms and advertising; must be given on a durable medium at the latest at delivery and say the legal guarantee is unaffected | Art. 1649septies §1 and §2 old Civil Code | …wettekstId=31654 |
| Terms that limit the consumer's rights are void | Art. 1649octies old Civil Code | …wettekstId=31655 |
| EU basis of the above | Directive (EU) 2019/771, Art. 6, 7, 10, 11, 12, 13, 21 | https://eur-lex.europa.eu/eli/dir/2019/771/oj |
| A cosmetic product is a substance or mixture; a toothbrush or floss is an article | Art. 2(1)(a) Regulation (EC) No 1223/2009 (mirror read); General Product Safety Regulation (EU) 2023/988 covers the articles | https://eur-lex.europa.eu/eli/reg/2009/1223/oj · https://eur-lex.europa.eu/eli/reg/2023/988/oj |
| Compliance may not be presented as a benefit; free-from claims | Regulation (EU) No 655/2013, common criterion 1; Commission technical document 2017 (as cited in the audit) | https://eur-lex.europa.eu/eli/reg/2013/655/oj |

Limits: EUR-Lex returned empty pages to automated reads, so the EU articles were read on legislation.gov.uk (identical text of the original directives) and through the Belgian transposition. This is drafting against the published law by an AI, not a signed opinion; the counsel points in §8 stay open.

## 5. Not changed, and why

- **Territorial scope: EU only, decided.** Victor decided on 24 Oct (landing desk, R57e): EU only for now. The Terms (2.3, 5.1, 8.2, 9.10, 11.1, 15.3, 15.4), Consumer Rights (5, 9), the shipping and subscription policies all say “member states of the European Union” and stay as they are; Victor removes the UK and Switzerland from the market selector in admin. This closes the UK question under LR1 blocker 5 for this text. The privacy policy's “European Economic Area, the United Kingdom and Switzerland” refers to Shopify's consent-banner region list (Settings → Customer privacy), not to the markets we sell to, so it stays while that list contains them (ADMIN-STEPS step 1, condition a).
- **“For a membership, the period runs from your first delivery”** is kept (Art. VI.47 §2, 2° c). Whether the Year (two deliveries) is a regular-delivery contract or one order delivered in parts stays a counsel point.
- **The Year money-back guarantee keeps “unopened (pump never primed)”** and the €59 deduction. They are conditions of the voluntary 60-day guarantee, which may be narrower than the law as long as the statutory right is untouched; clauses 4.1.5 and 4.5 and section 3.5 say so, and Astra confirmed they are confined to the voluntary route.
- **Clause 9.9 (renewal refunds)** now reads “Care Credit earned on the refunded amount lapses; if you had already used it to pay for articles on another order, you may return those articles instead of having that credit deducted (clause 4.7.6)” (R57d, TE5). A renewal refund is a contractual route, so the deduction stays its default, with the return alternative explicit. The subscription policy quotes clause 9 word for word and carries the same sentence (SE1), so it is now in `POLICIES-PASTE.md`.
- **Clause 4.6.1 and section 3.7.1 (“without harsh chemical preservatives” / “without relying on harsh preservatives”)** are a free-from claim inside a legal text (audit P2-2). Not a blocker-1 item; routed to gate-claims.
- **Privacy Policy**: no blocker-1 item of its own. It carries gate-consent's handoffs: Klaviyo and the withdrawal-function data (§3c), the regional consent wording (§3f) and its final form (§3g: no “Your privacy choices” or Global Privacy Control promise while the Data Sharing Opt-Out Page is inactive, withdrawal effective at once, the Shopify Network Intelligence paragraph with the Shopify Consumer Privacy Policy link). The cookie-law citation in section 1 (audit P0-3 text fix: the Electronic Communications Act of 2005 → the Data Protection Act of 30 July 2018) and the processor-list completeness from R60 (TikTok, Klaviyo web pixel, Judge.me, Loop Subscriptions, UpPromote) stay with gate-consent.
- **“Download the form (PDF)”**: on Victor's instruction (24 Oct, through gate-withdrawal) the two placeholder links are removed from both pages and the plain line from both policy bodies (§3c); the model form stays inline, which is what Art. VI.45 §1 8° and Annex 2 to Book VI WER require. The three PDFs in `input/legal-offer/legal/forms/` remain available for the confirmation email (ADMIN-STEPS step 0), and Astra's point about pastes overwriting the links is moot.
- **“Last updated October 2026”** stays; a dated version line (audit P2-13) belongs to the legal-offer branch when it logs v4.5.

## 6. Handoffs

- **gate-withdrawal** (their handoffs to this lane, taken on 24 Oct, §3c): the withdrawal function is named with the verified labels in Terms 4.1.1 and the Annex and in Consumer Rights 3.1 and section 10 (EN “Withdraw from contract here”, NL “Hier de overeenkomst herroepen”, FR “Renoncer au contrat ici”; done in R57); Klaviyo is named in the Privacy Policy as the processor of the acknowledgement email and the withdrawal-function data is listed (PC1, PC2); the refund wording to keep in sync on the withdrawal page is Terms 4.1.2 and Consumer Rights 3.1 second bullet, verbatim (refund within 14 days of the day we are informed, standard delivery included, withholding until the goods are back or proof of sending arrives, same payment method). The harmonised legal-guarantee notice (Implementing Regulation (EU) 2025/1960) is pre-contractual information to show prominently at the point of sale, that is on the product page and in the ordering flow (Art. 6(1)(l) CRD as amended by Directive (EU) 2024/825, transposed by the Act of 22 July 2026); the law does not require it on the Consumer Rights page, which already states the two-year guarantee in words, and the prescribed design is an image this lane cannot reproduce in a richtext setting, so it stays with gate-withdrawal and is not added to section 4. The function's acknowledgement (content, date, time, Art. VI.61/2 §4) must also confirm the return address, as Terms 4.7.2 promises.
- **source-copy**: register the 17 changed settings in `TRANSLATIONS-HANDOFF.md` (NL and FR given), refresh the EN digests of batch-04 for those settings, and keep the `legal-review` status on them. The policy bodies are admin (Translate & Adapt), `POLICIES-PASTE.md`.
- **legal-offer branch (canonical files, D8)**: apply §3 and §3b to `legal/terms-and-conditions/en.md` and `legal/consumer-rights/en.md`, log v4.5 in `legal/CHANGELOG.md`, add the NL and FR files, and update the Figma legal frames. Until that is done, a republish from the canonical files would restore the defects (Astra, observation 7). This lane did not edit the input copies.
- **gate-claims**: the free-from line in 4.6.1 / 3.7.1.
- **Victor, launch gate G1 (audit P0-11, Astra B2)**: the order confirmation and Loop's first-membership email must carry the Terms with the withdrawal information, the model form and the commercial-guarantee conditions in a retainable form, in the customer's language, by delivery at the latest; evidence is a real received email. Steps and acceptance check in `ADMIN-STEPS.md` step 0. A link to a changeable page is not a durable medium (CJEU C-49/11).
- **Victor, customer care and Loop (R57d)**: when a refund request or withdrawal comes in, customer care first identifies the other order, the articles and the Care Credit attributable to the amount being refunded (proportionally: at 20 % a €10 partial refund of a €100 payment concerns €2 of credit, not €20) and tells the customer before asking for a choice; sends a prepaid label (14 days to return run from its receipt); on a statutory withdrawal or legal-guarantee refund pays the refund in full within the legal period whatever the customer decides, records an express agreement before any keep-and-pay set-off, and asks again (never deducts) when the customer does not answer; on the voluntary routes deducts the attributable credit if the customer keeps the articles and reverses it on a timely return; never counts the same credit twice. Releasing earned Care Credit only after the 14-day withdrawal period (a Loop setting) would make these cases rare, but it changes the “available immediately” promise in clause 10.1 and does not remove later conformity cases.

## 7. Files changed in this branch

- `templates/page.terms-and-conditions.json`: EN values of eight settings (clause 2, 3, 4, 7 content, 7 examples, 9, 10, Annex).
- `templates/page.consumer-rights.json`: EN values of eight settings (key card 3, sections 1, 2 content + title + menu label, 3, 4, 10).
- `templates/page.privacy-policy.json`: EN values of three settings (section 3 communication data; section 5 Klaviyo and Hotjar; section 9 cookies).
- `docs/launch-gate/legal/CHANGES.md`, `POLICIES-PASTE.md`, `TRANSLATIONS-HANDOFF.md`, `ADMIN-STEPS.md`.

Checks: `shopify theme check --fail-level error` (0 errors, 19 baseline warnings), the three templates still parse as JSON, every replacement anchored exactly once (or the stated count) in the templates (from the 5bab3ad base, R57, then R57b, then the add-ons), in the live EN/NL/FR policy bodies and in the batch-04 NL/FR values; grep of the new templates and policy bodies for “unopened goods”, “of approval”, “return authorisation”, “notified as cosmetics”, “eligible, unopened”, “deducted from the refund if you already spent it”, “Download the form”: none left.

## 8. R57b: Astra's R57 review, what was done

| Astra item | Class | Done in R57b |
|---|---|---|
| B1 spent Care Credit could reduce a statutory refund (4.7.3, 4.7.4, 10.6) | blocker | R57b (TB3, TB4, TB6, CB2): the credit spent to pay (restored) and the credit earned from the refunded payment (lapses) kept apart; statutory routes refunded in full, nothing claimed back. Superseded by R57c (TD3, TD4, TD6, CD2), Victor's rule, which Astra's R57c review found too broad (B4); **now R57d (TE1–TE6, SE1, CE1–CE3)**, the retained-benefit model, see “R57d” below |
| B2 durable-medium confirmation deferred beyond the release checks | launch gate | `ADMIN-STEPS.md` step 0 is now the first item and a go/no-go gate: which Shopify notification and which Loop email, what they carry, how, and the acceptance check (a real received email in each language shows the Terms, the withdrawal information, the model form and the links) |
| Welcome Kit on a membership withdrawal | non-blocker | TB1, CB1: “the goods” of a membership are everything delivered under it, kit included; no fee, no €59 on the statutory route |
| NL/FR withdrawal labels | verified, closed | unchanged; confirm-step labels added to the gate-withdrawal handoff |
| 1 subscription policy keeps the 9.9 credit sentence and points to 4.7 | non-blocker | 4.7.4 scopes the deduction to 4.3, 4.4 and 9.9 by name; 9.9 unchanged (§5) |
| 2 NL/FR shipping and subscription policies link the legacy `/en/pages/terms-and-conditions` | non-blocker, admin | `ADMIN-STEPS.md` step 7: the designed Terms page `/pages/terms-and-conditions-1` (NL `/nl/…`, FR `/fr/…`) in the four short policies, EN/NL/FR (landing desk, 24 Oct); the subscription policy already has it through the paste of b417b33 (§3j) |
| 3 PDF links would be overwritten by later whole-body pastes | non-blocker, rollout | moot: Victor had the placeholder links removed (24 Oct); TC1 and CC1 remove them from the templates and the policy bodies; no PDF step remains |
| Landing desk (24 Oct): mirror the PDF-link removal; take gate-withdrawal's handoffs | add-on | §3c: TC1, CC1 (links removed), PC1, PC2 (Klaviyo and the withdrawal-function data in the Privacy Policy); labels already in place; refund-wording sync and the guarantee notice answered in §6 |
| 4 per-locale redirect checks; one release window | non-blocker, rollout | `ADMIN-STEPS.md` steps 5 and 9: `/nl/` and `/fr/` legacy paths checked one by one; release-window rule kept |
| 5 charter 4.2 abbreviates the serious-defect trigger | non-blocker | CB3 adds it |
| 6 actual diminished value, PAO carve-out, Year “receiving and inspecting” | non-blocker | 4.6.3 already says “the resulting loss of value” (actual, not fixed); TB5 adds the PAO carve-out; TB2 drops “and inspecting” |
| 7 canonical files still old; harsh-preservatives claim | non-blocker, handoff | §6: legal-offer branch and gate-claims |

**R57c, Victor's Care Credit decision (24 Oct).** Victor: “We do deduct the used credit, unless the customer also returns the product the credits were used for.” Applied in §3d as a linked-order choice: credit spent to pay for the refunded order is restored; credit earned from the refunded payment lapses, with nothing deducted for the unused part; where that credit had already paid for another order, the customer chooses, when giving notice, between returning the credit-funded items at no cost (prepaid label, their money refunded, nothing set off) and keeping them and paying the credit value, which is the only amount set off against the refund; silence means set-off; the refund confirmation names the linked order and the amount; the same choice applies on every refund route; apart from it the statutory refund of the price and the standard delivery charge stays complete. Legal basis relied on: Art. VI.50 §1 WER (every payment received is refunded; the credit was never a payment received), Art. VI.52 §2 WER and Art. 15 CRD (withdrawal ends a linked contract at no cost, hence the cost-free return branch), Art. VI.51 §2 WER (the set-off is not a diminished-value claim; it rests on the conditional price reduction of the linked order falling away when the payment that earned it is refunded, set off under Art. 5.258 ff. of the new Civil Code), Art. VI.45 §1 8° WER (stated before the contract), Art. 1649septies old Civil Code (voluntary guarantees). Residual risk for counsel, one line: a set-off against the statutory refund of an amount that exists only because the consumer withdrew may be read as a cost imposed as a consequence of withdrawal (Art. VI.51 §5 and VI.52 §2 WER, Art. 14(5) CRD) or, on the legal guarantee, as a term limiting the remedy (Art. 1649octies); the defence is that the credit was a conditional price reduction on the linked order, the consumer keeps goods of that value or may return them at no cost, and the choice is stated before purchase and on the refund confirmation.

**R57d, the retained-benefit model (24 Oct, after Astra's R57c review, B4).** Astra: the R57c rule made a Care Credit amount due and set off on every statutory refund, by silence, without an enforceable retained-goods obligation; the cited bases (VI.50 §1, VI.52 §2, VI.51 §2, VI.63) do not create one, and the Civil Code set-off reference was wrong (5.258 concerns sureties). R57d keeps Victor's intent and narrows the rule to what Astra's favourable authority supports (§3e: TE1–TE6, SE1, CE1–CE3). Statutory routes (withdrawal 4.1, legal guarantee 7): the refund is paid in full and within the legal period whatever the customer decides; a deduction exists only for the Care Credit attributable to the refunded amount that the customer actually used on articles they keep, after we have identified the other order, the articles and the amount, and only with the customer's express agreement given after that information; silence is never agreement; no answer means refund in full and ask again. Proportional allocation: credit earned on the amount actually refunded lapses, not the whole payment's reward. Return reconciliation: the prepaid label, 14 days from its receipt, nothing deducted for returned articles, their money refunded, any provisional set-off reversed, partial returns counted per article, no double counting, the attributable credit as ceiling, unused credit never recovered in cash. Voluntary routes (4.3, 4.4, 9.9): the return-or-keep choice is explicit (4.7.6) and the older unconditional deduction sentences in 4.3.3, 4.4.2, 9.9, charter 3.3 and 3.4 are qualified by it. Civil Code references corrected to 5.254–5.255 (legal set-off), 5.263 (contractual set-off) and 5.20 (silence). Basis relied on: Art. VI.50 §1 and VI.51 §5 WER; CJEU C-583/18 (Verbraucherzentrale Berlin v DB Vertrieb, paras 35–37) as an analogy for recovering a conditional price benefit on a retained, legally distinct transaction; Art. 5.20, 5.254–5.255 and 5.263 new Civil Code; Art. 1649quinquies and 1649octies old Civil Code; Art. VI.45 §1 8° WER; Art. 1649septies for the voluntary guarantees. Residual risk for counsel, one line: whether a loyalty credit spent on a later order creates an enforceable restitution debt for the retained articles is undecided in Belgian law and C-583/18 is an analogy, so even an expressly agreed set-off on a statutory refund can be challenged under Art. VI.51 §5 and VI.63 WER or Art. 1649octies; the conservative alternative remains the b8d5ef3 statutory exclusion with Victor's return option kept for the contractual routes.

**R61b privacy handoff from gate-consent (24 Oct), applied in R57d (§3f).** Since R61 the theme loads Hotjar by region, following Shopify's Customer Privacy defaults; the Privacy Policy promised everyone that nothing non-essential runs before opt-in. Section 9.2 now states the regional rule (EEA, UK and Switzerland: only after Accept; elsewhere by default, with the “Your privacy choices” link and Global Privacy Control honoured), the real footer label “Cookie preferences” / “Cookievoorkeuren”, and that a withdrawal takes effect from the next page; the Hotjar entry in section 5 says the same; the section lead and the two 9.1 bullets are qualified so they no longer contradict 9.2. Three conditions for Victor before the privacy paste (ADMIN-STEPS step 1): the Customer-privacy region list contains EU/EEA, UK and Switzerland (else drop “Switzerland”); the Data Sharing Opt-Out Page is on for the opt-out regions (else drop the “Your privacy choices” clause); keystroke masking is on in Hotjar for site 1364127 (else drop “with keystroke masking”). Verify the FR footer label before publishing FR.

**R57e, the final privacy round (24 Oct, gate-consent commit 938811c; Astra R57d B1 and B2; §3g).** Astra's R57d found two privacy blockers: B1, the text promised a “Your privacy choices” link and Global Privacy Control handling while the Data Sharing Opt-Out Page is inactive (Victor's admin, 24 Oct: “will be active when you add markets that require it”; the US market is off), and B2, a withdrawal that only took effect on the next page. gate-consent fixed the loader (R61d: a withdrawal expires Hotjar's site cookies and reloads the page once) and wrote the final wording. §3g applies the page-off texts: 9.2 ends its second sentence after “may run by default”, names the real “Cookie preferences” label and says a withdrawal takes effect immediately, the page refreshing once (this lane stops there and does not promise cookie deletion, as the handoff allows); the two 9.1 bullets carry the same regional ending without an opt-out clause; the Hotjar entry in section 5 loses “unless you opt out”; and a new paragraph in section 5 covers Shopify Network Intelligence, which Victor keeps enabled (24 Oct): what Shopify does with customer and device data from the shop, that no other merchant can access it, that declining non-essential cookies keeps the device data of the visit out of the non-essential uses, advertising included, with the Shopify Consumer Privacy Policy link Shopify requires and Shopify's own opt-out at privacy.shopify.com. The fuller texts (opt-out link, GPC, “unless you opt out”, the sale/sharing sentence for Network Intelligence) stay in the handoff for the day the opt-out page is active and verified. For counsel, from the handoff: the controller roles under Shopify's Data Processing Addendum of 7 July 2026 and its Appendix E, our lawful basis for enabling Network Intelligence and any consent it requires, the disclosures the DPA and the Additional Services Terms require, the lawful basis for default analytics outside the banner regions, and the withdrawal mechanics. Residual risk, one line: the regional rule relies on Shopify's region list and on Victor's three conditions (Switzerland in the list, keystroke masking on, the opt-out page kept off until verified); if any of them changes without the text, the policy over-promises again.

**R57f, after Astra's R57e review (24 Oct; §3h).** Astra closed R57d B1 in every version and language and found two new blockers. B1: the loader at 938811c could ignore a second withdrawal given within its five-second guard after a fresh acceptance, so “the page refreshes once” over-promised; gate-consent is fixing the loader (R61e: a repeat withdrawal within the guard window is never dropped) and the 9.2 sentence now describes the actual trigger with Astra's wording: “A withdrawal takes effect immediately. If you withdraw analytics consent while Hotjar is running, the page refreshes once to stop it.” (PH2, EN/NL/FR). The corrected loader and this text deploy together (ADMIN-STEPS step 1, condition e); if Astra's R61e review changes the wording, the delta is applied the same way. B2: section 5 described every recipient as a processor acting on our written instructions, while Shopify's Data Processing Addendum of 7 July 2026 (Appendix E, Enhanced Services) makes Shopify a controller for Network Intelligence; the lead now says the service providers and other recipients below help us run the shop, the instructions/DPA sentence is confined to processing on our behalf (“Where a service provider processes personal data on our behalf, it acts on our written instructions under a data processing agreement. Recipients include:”), and the Network Intelligence paragraph says that for these enhanced services Shopify acts as a data controller under its Data Processing Addendum (PH1, EN/NL/FR). Basis: Art. 13(1)(e) GDPR (recipients) and Art. 4(7) and (8) GDPR (controller, processor); Shopify DPA, Purpose and Appendix E. Counsel still confirms the governing agreement version, the parties' actual roles, the lawful basis and consents for Network Intelligence, the disclosure duties under Shopify's Terms §9.2.5 (Terms and privacy policy), and the lawful basis for default analytics outside the banner regions. Publication gate kept hard (Astra): verify every EU/EEA country, the UK and Switzerland in the consent-region list before release; deleting “Switzerland” from the text cures only a missing Switzerland, never missing EU/EEA or UK coverage; the Hotjar app embed stays off. Terms, Consumer Rights and the subscription policy are untouched and keep their R57d approval.

**Decided by Victor, 24 Oct (R57e): territorial scope stays EU only.** No text change; the UK and Switzerland leave the market selector in admin. Recorded here so the open question under LR1 blocker 5 is closed for the legal text (§5 has the clause list).

Follow-ups, not in this lane: the migration redirect CSV (not in the input set; cannot be certified here); counsel on any alternative to removing the statutory clawback, on the Year as a regular-delivery contract, on actual loss-of-value and kit handling, and on the complete multilingual contract in its operational context; the NL model-form style differences between theme and policy (equivalent in meaning, left as they are); LR1 blockers 2 to 7.
