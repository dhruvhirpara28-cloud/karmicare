# Round 8 · dashes out of customer copy

**Created**: 2026-10-26

### Changelog
| Date | Change |
|------|--------|
| 2026-10-26 | Inventory (read only) and batch plan. The rewrite tables follow per batch. Brief: landing desk, Victor 26 Oct. |

Rule (Victor, 26 Oct):
- No em dash (—) and no spaced en dash (–) as a pause, aside or separator, in EN, NL or FR.
- An en dash between numbers ("2–3 dagen") stays, and so do hyphens in compound words.
- Rewrite the sentence; don't just swap the character:
  - an explanation or consequence becomes a full stop or a colon;
  - an aside becomes commas or its own sentence;
  - a label with its explanation takes a colon or the middle dot "·".
- Legal text keeps exactly the same meaning and gets an extra check.

Round 8 starts after round 7 is written.

## Inventory (26 Oct)

Scan: `docs/localization/registration/live/tools/round8_dash_scan.py` (output `round8-scan.json`, untracked). It covers:
- the EN source, admin content included (captured 19–25 Oct);
- the NL/FR payloads (values not held);
- `locales/` EN, NL and FR, all keys, and the other 28 locales for `kc.*` keys only.

**512 rows** carry an em dash or an en dash that is not a number range: 336 em dashes and 213 en dashes. Another 15 rows only have a spaced hyphen " - " used as a dash; they are candidates.

| Area | EN | NL | FR |
|---|---:|---:|---:|
| Theme templates (home, PDP, product, legal templates) | 27 | in the payloads below | in the payloads below |
| Theme locale keys (`kc.clock.window_2/4/6`) and Dawn keys (`gift_cards.issued.qr_image_alt`, `products.product.value_unavailable`) | 3 + 4 | 4 | 4 |
| Product, metafields, metaobjects (PDP FAQ, comparison, treatment journey, compare table, mission card) | 1 + 22 + 6 | in the payloads | in the payloads |
| Policies (desk paste) | 28 | in the payloads | in the payloads |
| Legal page body, other pages, collections, apps | 1 + 5 + 4 + 2 | | |
| Blog articles (batch 07, not registered) | 40 | in the payloads | in the payloads |
| Shopify system titles "Search – KARMICARE" etc. (the shop-name suffix Shopify adds, not our copy) | 3 | | |
| NL/FR payload rows with a dash, all statuses (admin 54/111, legal-review 44, pending-claim-review 22, translated 10/27, theme-key 3/3) | | 133 | 141 |
| The other 28 locales: EN fallback of the three `kc.clock` keys | | | |

Legal rows (terms, privacy, consumer rights, withdrawal, policies): 46 in each language.

Special cases:
- **Dash only in NL/FR:** 7 rows have a dash in the translation while the EN has none (NL 2, FR 5), mostly old blog articles, and in FR the Dawn key `products.product.value_unavailable` ("{{ option_value }} – indisponible").
- **Unspaced dash between words:** EN 17, NL 3, FR 8, for example "Oral–gut–brain axis", "ORAL–SLEEP CONNECTION" and "Low–medium abrasivity". These are compounds, not pauses. Proposal: a hyphen ("oral-gut-brain", "low-to-medium") or keep. Victor decides once for all of them.
- **Terms clause headings** "Clause 1 – Identity of the vendor", 15 headings plus the annex: they become "Clause 1. Identity of the vendor", the same in NL/FR. The meaning does not change; this is part of the legal check.

## Batch plan

Each batch gets a table with location, current text, and proposed EN, NL and FR. Victor approves per batch.

| Batch | Content | Channel after approval |
|---|---|---|
| 1 | Homepage, PDP and footer: theme templates (not legal), `kc.clock` keys, Dawn keys | EN through a lane commit and review; NL/FR through `register.py` and `locales/` |
| 2 | Product content: PDP FAQ, comparison, treatment journey, compare table, mission card, product body | EN paste list for Victor (Admin); NL/FR through `register.py` |
| 3 | Legal: terms clause headings, privacy, consumer rights, withdrawal, policies (marked "legal") | EN legal templates through a lane commit; policies through the desk paste; NL/FR through `register.py` and the paste |
| 4 | Blog articles and other pages | EN paste list; NL/FR for the articles once batch 07 is released |

Guard: after the first batch, `fr/check.py` and `nl/validate.py` get a rule that flags any new em dash, or spaced en dash outside a number range, in EN/NL/FR values.
