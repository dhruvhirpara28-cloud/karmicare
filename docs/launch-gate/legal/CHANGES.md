# R57 · Launch blocker 1: consumer-rights text (gate-legal)

**Created**: 2026-10-24 · lane gate-legal · base `karmicare/soft-launch` @ 5bab3ad
**Scope**: LR1 blocker 1 (`docs/launch-gate/input/LR1-LAUNCH-READINESS.md`) = audit items P0-1, P0-5, P0-6, P0-8, P0-9, P0-14 (withdrawal information), P0-15 (the NL/FR of the changed strings) from `input/legal-offer/work/2026-10-05/legal-audit-terms-consumer-rights-privacy.md`.
**Decisions applied**: D1 option A (Victor, 24 Oct: priming exemption dropped, loss-of-value rule), D7 and D8 (Consumer Rights is a plain-language summary that points to the Terms; the canonical texts are `input/legal-offer/legal/*`), D2 and D5 (unchanged, already in the text). D3 is discussed in §5 and not applied by this lane.

**Deliverables in this folder**

| File | What |
|---|---|
| `CHANGES.md` (this file) | Where each text lives, the canonical place and redirects, every change with old → new, reason and legal source, what was verified, what is left |
| `POLICIES-PASTE.md` | Full corrected body of the two Shopify policies that change (Terms of service, Refund policy), EN first, then NL and FR for Translate & Adapt |
| `TRANSLATIONS-HANDOFF.md` | The 14 changed theme-page settings with template, block id, key path and the full EN, NL and FR value, for source-copy |
| `ADMIN-STEPS.md` | What Victor does in admin, in order: policy pastes, legacy pages to hide, redirects, titles, withdrawal PDFs, checks |

Theme files changed: `templates/page.terms-and-conditions.json` and `templates/page.consumer-rights.json` (EN setting values only). `templates/page.privacy-policy.json` has no blocker-1 item and is unchanged. The three legacy pages, the policies and all NL/FR are admin work (`ADMIN-STEPS.md`).

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


## 3. The changes, one by one (EN old → new)

The NL and FR of every change are in `TRANSLATIONS-HANDOFF.md` (theme pages) and `POLICIES-PASTE.md` (policies). Old text is quoted from the live policy body on 24 Oct 2026; tags are stripped here for readability.


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


## 4. What was verified, and where (24 Oct 2026)

| Rule used in the text | Source read today | Link |
|---|---|---|
| 14-day period; start at physical possession; for a contract for regular delivery of goods, at the first delivery | Art. VI.47 §1 and §2 WER, consolidated Justel text | https://www.ejustice.just.fgov.be/eli/wet/2013/02/28/2013A11134/justel |
| How to withdraw: model form or any other unambiguous statement; sending before the end of the period is enough | Art. VI.49 §1 and §2 WER (same text) | same |
| Refund of all payments including delivery costs, without undue delay and within 14 days of the day the trader is informed; same payment means; may withhold until the goods are back or proof of sending is supplied, whichever first | Art. VI.50 §1 and §3 WER (same text); FPS Economy news page and ConsumerConnect (“binnen de 14 dagen nadat je … hebt laten weten”) | https://news.economie.fgov.be/270128-een-impulsieve-online-aankoop-er-is-een-weg-terug/ · https://consumerconnect.be/nl/themas/aankoop-product-of-dienst/herroepingsrecht/aankoop-op-afstand/geld-niet-terug |
| Consumer returns within 14 days and pays the direct return cost; liable only for diminished value from handling beyond what is needed to establish nature, characteristics and functioning; never liable if the withdrawal information was missing | Art. VI.51 §1 and §2 WER (same text) | same as Justel |
| Hygiene exception needs sealed goods whose seal was broken after delivery | Art. VI.53, 5° WER (same text); CJEU C-681/17 (slewo) as cited in the audit | same |
| Pre-contract information must say that the withdrawal function exists and where it is | Art. VI.45 §1, 8° WER as amended (“… en, in voorkomend geval, informatie over de beschikbaarheid en de plaats van de herroepingsfunctie bedoeld in artikel VI.61/2”) | same |
| The online withdrawal function: label “hier de overeenkomst herroepen”, available during the whole period, name + contract data + e-mail, “herroeping bevestigen”, acknowledgement on a durable medium with content, date and time | Art. VI.61/2 WER, inserted by the Act of 19 July 2026 (W 2026-07-19/05, art. 23), in force 14 August 2026 (Justel annotation); FPS Economy: “Sinds 14 augustus 2026 zijn ondernemingen verplicht een herroepingsfunctie aan te bieden” | same; https://www.droitbelge.be/news_detail.asp?id=1199 (FR label “renoncer au contrat ici”) |
| EU basis of the above | Art. 13, 14 and 16(e) of Directive 2011/83/EU (text checked on the legislation.gov.uk mirror because EUR-Lex refuses automated reads); Art. 11a inserted by Directive (EU) 2023/2673, applicable 19 June 2026 | https://eur-lex.europa.eu/eli/dir/2011/83/oj · https://eur-lex.europa.eu/eli/dir/2023/2673/oj |
| Conformity requirements (description, fitness, quality and durability normal for the goods, public statements) | Art. 1649ter old Civil Code, as replaced by the Law of 20 March 2022 (in force 1 June 2022) | https://www.kustcodex.be/kustcodex-consult/plainWettekstServlet?wettekstId=31650&lang=nl |
| Two-year liability (§1), two-month notification (§2), two-year presumption “tot bewijs van het tegendeel”, unless incompatible with the nature of the goods or of the defect (§4) | Art. 1649quater old Civil Code | …wettekstId=31651 |
| Consumer chooses repair or replacement unless impossible or disproportionate (§§1–2); price reduction or termination when not done, refused, persisting, serious (§5); no termination for a minor defect, seller proves it is minor | Art. 1649quinquies old Civil Code; FPS Economy and ConsumerConnect guarantee pages | …wettekstId=31652 · https://news.economie.fgov.be/214976-wettelijke-garantie-consument-is-beter-beschermd/ |
| A commercial guarantee binds on its stated terms and advertising; must say the legal guarantee is unaffected | Art. 1649septies old Civil Code | …wettekstId=31654 |
| Terms that limit the consumer's rights are void | Art. 1649octies old Civil Code | …wettekstId=31655 |
| EU basis of the above | Directive (EU) 2019/771, Art. 6, 7, 10, 11, 12, 13, 21 | https://eur-lex.europa.eu/eli/dir/2019/771/oj |
| A cosmetic product is a substance or mixture; a toothbrush or floss is an article | Art. 2(1)(a) Regulation (EC) No 1223/2009 (mirror read); General Product Safety Regulation (EU) 2023/988 covers the articles | https://eur-lex.europa.eu/eli/reg/2009/1223/oj · https://eur-lex.europa.eu/eli/reg/2023/988/oj |
| Compliance may not be presented as a benefit; free-from claims | Regulation (EU) No 655/2013, common criterion 1; Commission technical document 2017 (as cited in the audit) | https://eur-lex.europa.eu/eli/reg/2013/655/oj |

Limits: EUR-Lex returned empty pages to automated reads, so the EU articles were read on legislation.gov.uk (identical text of the original directives) and through the Belgian transposition. This is drafting against the published law by an AI, not a signed opinion; the five counsel points of the 5 Oct audit stay open, with the withdrawal function (point 4) now partly answered by the published Act.

## 5. Not changed, and why

- **Territorial scope (EU only) and the UK.** The brief lists D3 as “all 27 EU states plus the UK”. The record in `input/legal-offer/work/2026-10-06/legal-proposals-countries-and-open-decisions.md` adds a 9 Oct revision by Victor: UK excluded for now; cover all EU member states in the Terms. The live Terms, Consumer Rights, shipping and subscription policies say “member states of the European Union”, and the Markets question is LR1 blocker 5. This lane changed nothing here. If Victor confirms the UK is in, Terms 2.3, 5.1, 8.2, 9.10, 11.1, 15.3 and 15.4, Consumer Rights 5 and 9 and the shipping policy change together with Markets, shipping zones and the UK items of the 6 Oct file.
- **What a member sends back on a statutory withdrawal, and the Welcome Kit** (audit P0-5, open point). The corrected text says “send the goods back”, which under Art. VI.51 means everything delivered under the contract, the kit included, with the loss-of-value rule for anything used. If Victor prefers that a withdrawing member keeps the kit, one sentence in Terms 4.1.4 does it; his call.
- **“For a membership, the period runs from your first delivery”** is kept (Art. VI.47 §2, 2° c). The audit's counsel point on the Year (two deliveries) stays open.
- **The Year money-back guarantee keeps “unopened (pump never primed)”** and the €59 deduction. They are conditions of the voluntary 60-day guarantee, which may be narrower than the law as long as the statutory right is untouched; clauses 4.1.5 and 4.5 and section 3.5 say so.
- **Clause 4.6.1 and section 3.7.1 (“without harsh chemical preservatives” / “without relying on harsh preservatives”)** are a free-from claim inside a legal text (audit P2-2). Not a blocker-1 item; recommended deletion in the next legal round (handoff to gate-claims).
- **Privacy Policy**: no blocker-1 item. The cookie-law citation (audit P0-3 text fix) is gate-consent's.
- **“Download the form (PDF)” still links `#`** on both pages and in both policies: the PDFs exist in `input/legal-offer/legal/forms/` and must be uploaded to Files and linked (ADMIN-STEPS step 7).
- **“Last updated October 2026”** stays; a dated version line (audit P2-13) belongs to the legal-offer branch when it logs v4.5.

## 6. Handoffs

- **gate-withdrawal**: the page handle `/pages/withdrawal` and the labels used in the links: EN “Withdraw from contract here”, NL “Hier de overeenkomst herroepen” (statutory wording, Art. VI.61/2 §1), FR “Renoncer au contrat ici” (wording quoted by Belgian counsel for the CDE; verify against the Moniteur text of the Act of 19 July 2026 before the FR page goes live). Terms 4.7.2 now says we acknowledge a withdrawal by email and confirm the return address; the function's acknowledgement (content, date, time, Art. VI.61/2 §4) must do that. The three model-form PDFs.
- **source-copy**: register the 14 changed settings in `TRANSLATIONS-HANDOFF.md` (NL and FR given), refresh the EN digests of batch-04 for those settings, and keep the `legal-review` status on them. The policy bodies are admin (Translate & Adapt), `POLICIES-PASTE.md`.
- **legal-offer branch (canonical files, D8)**: apply §3 to `legal/terms-and-conditions/en.md` and `legal/consumer-rights/en.md`, log v4.5 in `legal/CHANGELOG.md`, add the NL and FR files, and update the Figma legal frames. This lane did not edit the input copies.
- **gate-claims**: the free-from line in 4.6.1 / 3.7.1.
- **Victor / notifications (audit P0-11)**: the order confirmation and Loop's first-membership email must carry the corrected Terms and withdrawal information on a durable medium; a link is not enough.

## 7. Files changed in this branch

- `templates/page.terms-and-conditions.json`: EN values of six settings (clause 2, 3, 4, 7 content, 7 examples, Annex).
- `templates/page.consumer-rights.json`: EN values of eight settings (key card 3, sections 1, 2 content + title + menu label, 3, 4, 10).
- `docs/launch-gate/legal/CHANGES.md`, `POLICIES-PASTE.md`, `TRANSLATIONS-HANDOFF.md`, `ADMIN-STEPS.md` (new).

Checks: `shopify theme check --fail-level error` (0 errors, baseline warnings), the two templates still parse as JSON, every replacement anchored exactly once (or the stated count) in the template, in the live EN/NL/FR policy bodies and in the batch-04 NL/FR values; grep of the new templates and policy bodies for “unopened goods”, “of approval”, “return authorisation”, “notified as cosmetics”, “eligible, unopened”: none left in the statutory clauses.
