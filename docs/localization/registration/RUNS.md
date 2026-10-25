# Registration runs

Every write `register.py` made, read from `live/journal-<lang>.jsonl` (that folder stays untracked: it holds the per-run reports). Counts only; the values are in the plans and payloads at the commit named in the review. Translations registered by hand are in `registered.json`.

| Run (Belgian time) | Lang | Checksum | Operations | Resources confirmed | Keys confirmed | Errors | Note |
|---|---|---|---:|---:|---:|---:|---|
| 2026-10-22 19:29 | NL | `0622fa0b0947ab6f` | 284 | 28 confirmed | 284 | 0 |  |
| 2026-10-22 19:54 | NL | `3eb0d1a95500b9c6` | 62 | 12 confirmed | 62 | 0 |  |
| 2026-10-22 20:53 | NL | `6089aa3992b39f8b` | 4 | 3 confirmed | 4 | 0 |  |
| 2026-10-23 10:49 | NL | `c9a89b8098ed4460` | 29 | 21 confirmed | 29 | 0 |  |
| 2026-10-23 12:46 | NL | `c382c2a3f027a76f` | 89 | 55 confirmed | 89 | 0 |  |
| 2026-10-23 14:34 | NL | `2b86cbe113aec3b9` | 25 | 24 confirmed | 25 | 0 |  |
| 2026-10-23 15:37 | NL | `49a7c79ccc1cd59f` | 161 | 24 confirmed | 161 | 0 |  |
| 2026-10-23 15:50 | NL | `69477d42ea706224` | 27 | 27 confirmed | 27 | 0 |  |
| 2026-10-24 21:37 | NL | `ae11381daa1f46f7` | 49 | 24 confirmed | 49 | 0 | R71: 10 homepage (R59/R59b claims, FAQ one-duo without dosage), 19 legal (R57b), 20 byte-only metaobject re-registers; Astra R74 approve; verified live 24 Oct (curl, NL homepage, terms-and-conditions-1, new-consumer-rights, privacy-policy) |
| 2026-10-25 11:26 | NL | `b9bec66f44983c1d` | 60 | 24 confirmed | 60 | 0 | Round 2, plan c1d1bc2: 20 byte-only metaobject re-registers, 31 withdrawal page (R73), 3 consumer-rights guarantee labels, 6 practitioner hover quotes from the Dutch originals (2 Ponet overwrites); Astra R80 approve; verified live 25 Oct (curl, NL withdrawal, new-consumer-rights, homepage) |
| 2026-10-25 12:43 | NL | `07affccdbe47aeb9` | 82 | 24 confirmed | 82 | 0 | Round 3, plan 17b31d7 against live main d5b514d (ROUND3.md): 20 byte-only metaobject re-registers, 3 Care Credit lines, homepage SEO title, 6 research image badges, 52 practitioner request form texts (both product templates); verified live 25 Oct (curl, NL homepage and PDP) |
| 2026-10-22 19:33 | FR | `54845f48d52df704` | 219 | 25 confirmed | 219 | 0 |  |
| 2026-10-22 19:54 | FR | `17fb04ffe2dc0b54` | 58 | 11 confirmed | 58 | 0 |  |
| 2026-10-23 10:50 | FR | `12886b07fddae153` | 33 | 25 confirmed | 33 | 0 |  |
| 2026-10-23 12:52 | FR | `3a233ef752f374f3` | 94 | 52 confirmed | 94 | 0 |  |
| 2026-10-23 15:41 | FR | `59d0626ff808ef60` | 120 | 22 confirmed | 120 | 0 |  |
| 2026-10-23 15:52 | FR | `c6ccabd95ff00361` | 24 | 24 confirmed | 24 | 0 |  |
| 2026-10-23 15:57 | FR | `ee406a899e43a0c7` | 18 | 18 confirmed | 18 | 0 |  |
| 2026-10-23 19:49 | FR | `7da703e1eb51c492` | 30 | 26 confirmed | 30 | 0 |  |
| 2026-10-24 21:40 | FR | `54e4717b22c00c4d` | 50 | 26 confirmed | 50 | 0 | R71: as NL with 18 legal, plus the PDP info card FR ('un contrôle dentaire', product.subscription-item and product); Astra R74 approve; verified live 24 Oct (curl, FR homepage and legal pages) |
| 2026-10-25 11:29 | FR | `8f328b78f8bc3c43` | 60 | 25 confirmed | 60 | 0 | Round 2, plan c1d1bc2: as NL, with 5 hover quotes (Spreuwers FR released 24 Oct, Sietske homepage overwrite) and Leen Ponet's metaobject designation; Astra R80 approve; verified live 25 Oct (curl, FR withdrawal, new-consumer-rights, homepage, PDP) |
| 2026-10-25 12:45 | FR | `6d2128d6befd4fad` | 84 | 24 confirmed | 84 | 0 | Round 3, plan 17b31d7: as NL, plus Leen Ponet's card title 'Pharmacienne…' on homepage and PDP; verified live 25 Oct (curl, FR homepage and PDP) |
