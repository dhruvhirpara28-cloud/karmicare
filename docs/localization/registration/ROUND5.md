# Round 5 · department names, legal page titles

**Built** 25 Oct 2026 against live main `d5b514d`, theme `187295564157`, after the round 4 write (`RUNS.md`). Victor's decision, via the landing desk: "ja gate legal in een keer laten rechtzetten". The EN stays as it is.

## Department names, as in gate-legal's policies (6da5b37)

| EN | FR | NL |
|---|---|---|
| Returns Department | Service des retours | afdeling Retouren (was *Retourafdeling* in the terms) |
| Privacy Operations | Service Vie privée | afdeling Privacy |

The changed rows:
- NL: `page.terms-and-conditions` FcEDdA and `page.privacy-policy` dGmgBJ. `page.consumer-rights` iDEfUH already read *afdeling Retouren*.
- FR: `page.consumer-rights` iDEfUH, `page.terms-and-conditions` FcEDdA and `page.privacy-policy` dGmgBJ.
- The held policy payload rows carry the same names, so the payloads match what the desk pasted: NL privacy #b112 and terms #b052, FR privacy #b112, terms #b052 and refund #b057.

## Legal page titles

The three designed legal pages have no SEO title in the Admin, so their `<title>` is the page title. Live it was English in NL for all three, and in FR for terms and privacy (curl, 25 Oct). The former `seo.title` rows, captured from that `<title>`, never matched a live key, so they are `retired`. Three `title` rows take their place, with NL/FR from those rows minus " – KARMICARE":

| Page | EN | NL | FR |
|---|---|---|---|
| `terms-and-conditions-1` | New Terms and Conditions | Nieuwe algemene voorwaarden | Nouvelles conditions générales |
| `new-consumer-rights` | New Consumer Rights | Nieuwe consumentenrechten | Nouveaux droits des consommateurs (already live) |
| `privacy-policy` | New Privacy Policy | Nieuw privacybeleid | Nouvelle politique de confidentialité |

The EN titles start with "New", left over from when the pages were made. Dropping it, in the Admin and then in NL/FR, is Victor's choice.

**Expected:** NL 5 and FR 6 new or changed keys. FR consumer rights already has its title live, so it will show as "same". The dry run can add byte-only re-registers.

FR `check.py`: 73 errors (75 before). The retired legal rows (the three `seo.title` rows, the two footer-group labels) keep the flag `legal-review`. NL `validate.py`: 62, unchanged.
