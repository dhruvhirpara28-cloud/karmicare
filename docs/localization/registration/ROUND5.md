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
| `terms-and-conditions-1` | Terms and Conditions | Algemene voorwaarden | Conditions générales |
| `new-consumer-rights` | Consumer Rights | Consumentenrechten | Droits des consommateurs |
| `privacy-policy` | Privacy Policy | Privacybeleid | Politique de confidentialité |

**Admin, 25 Oct (source-copy in the Orca browser, at Victor's request: "ja wil new schrappen"):**
- "New" is dropped from the three page titles. The handles are unchanged, read back from `/pages/<handle>.json`.
- The legacy pages *Terms and Conditions*, *Privacy Policy* and *Consumer Rights* (28 Feb 2024; handles `terms-and-conditions`, `privacy`, `consumer-rights`) are Hidden.
- The existing URL redirects send their URLs to `terms-and-conditions-1`, `privacy-policy` and `new-consumer-rights` (301, checked by curl). The page sitemap now lists only the designed pages.

**Expected:** NL 5 and FR 6 new or changed keys. The dry run can add byte-only re-registers.

FR `check.py`: 73 errors (75 before). The retired legal rows (the three `seo.title` rows, the two footer-group labels) keep the flag `legal-review`. NL `validate.py`: 62, unchanged.
