# Round 4 · addresses, drafted products, SEO titles

**Built** 25 Oct 2026 against live main `d5b514d`, theme `187295564157`, after the round 3 write (`RUNS.md`). Victor runs the dry runs; the write follows the review.

## Decisions (Victor, 25 Oct)

1. **Addresses in their local form** ("Belgique", then "FR Belgique, NL België"). This reverses R2 F8 decision 7, which kept every postal address exactly as in the EN. Inside each address span:
   - FR: Belgium → *Belgique*, Brussels → *Bruxelles*, box → *boîte*;
   - NL: Belgium → *België*, Brussels → *Brussel*, Bruges → *Brugge*, box → *bus*.

   S1 in `fr/check.py` and `nl/validate.py` now expects that form, and each self-test carries a mutation back to the EN form. Street names stay as the EN writes them, so the NL keeps *Boulevard du Roi Albert II* and the FR keeps *Koning Albert II-laan*. Using the street name in the reader's language is a further choice for Victor.
2. **Only the 2.0 products, the floss and the Awake & Asleep system stay sellable.** Source-copy set three products to Draft in the Admin at Victor's request: *Complete Hygiene Kit*, *Morning Toothbrush* and *Evening Toothbrush* (the versions without 2.0). Their storefront URLs return 404. Their 14 rows are `retired`.

## What the plans change

| Item | NL | FR |
|---|---:|---:|
| Footer copyright line (address) | 1 | 1 |
| Legal pages: company banners and contents with an address (consumer rights, privacy, terms) | 12 | 12 |
| SEO titles of Awake / Asleep toothpaste 2.0, without the " – KARMICARE" that only the page `<title>` adds (the Admin search engine listing has none) | 2 | 2 |
| Image alts of the two 2.0 toothbrushes, which return to the wave now that the 1.0 twins are retired | 2 | 2 |
| **Expected** | **17** | **17** |

The dry run can add byte-only re-registers.

The SHOP_POLICY bodies stay held, because the desk pastes them from `docs/launch-gate/legal/POLICIES-PASTE.md`. The NL/FR payload rows of the policies carry the local addresses now. The paste file is still in the EN form.

## Still open, not in this round

- **2.0 toothbrush and floss descriptions.** The live HTML wraps every sentence in `<span>` and starts with `<meta charset>`, so the source block no longer matches. The EN also has typos ("dispurge", "nurished", "Awake of Asleep"). Two ways out: clean the HTML in the Admin and correct the EN, or capture the HTML exactly as it is.
- **SEO descriptions.** The three sellable non-system products and the two 2.0 toothpastes have none in the Admin; Shopify shows the description instead. The same holds for the SEO titles of the three designed legal pages.
- **Loop selling-plan descriptions.** Loop keeps its own NL/FR copies (Multilingual), so a Shopify translation does not reach the widget.
- **"Date:" blocks** of the legacy Admin pages `new-consumer-rights` and `terms-and-conditions-1`. The designed templates render these pages.
- **check.py.** FR now has 75 errors and NL 62, both two fewer than before (the S1 address lines). `fr/check.py --self-test` already crashed before round 4 (a `drop_flag` mutation on a flag the claims release removed). The control of `nl/validate_selftest.py` expects data without errors, so it fails as well. Neither comes from this round.
