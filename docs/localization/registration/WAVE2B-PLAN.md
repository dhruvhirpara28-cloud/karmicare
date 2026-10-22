# Wave 2b · metaobject translations, plan after Astra R30

Wave 2a (selling-plan names and descriptions, exact section headings) is in review on its own. Wave 2b registers the text that lives in metaobjects: the product FAQ, the comparison section, the treatment journey, the professionals' roles, the mission card and the compare table. About 140 inventory items per language. NL and FR translations already exist in the payloads; only the route to the right field is missing.

R30 rejected the first attempt for four reasons. This plan answers each one.

| R30 finding | Answer in wave 2b |
|---|---|
| R30-1 coverage does not prove the target; the route escapes the product family | Discovery only proposes. A field is written only through a reviewed field binding. Edges are typed references only, and shop-level objects come from a reviewed handle list, never a type-wide scan. |
| R30-2 held and gated items dropped before the check | The segment lookup holds every item of the family, whatever its status; a held, gated or conflicting segment vetoes the field first. |
| R30-3 URLs, attributes and Liquid changed | Values are parsed into a text-node map. Only text nodes are replaced. Tags, attributes, comments and Liquid are opaque bytes. Anything the parser cannot place with certainty is not proposed. |
| R30-4 Latin-only coverage | Every text node must equal one plan segment exactly. Unicode categories (letters and digits of any script, combining marks) decide what is text. |
| R30-5 docs promise the old protection | Runner header, `build_payloads.py` and `DRY-RUN.md` describe the reviewed-binding rule. |

## 1. Discovery (dry run, read only, writes nothing)

For each inventory family of the Duo product (`custom.product_faq`, `custom.comparison_section`, `custom.treatment_journey_*`, `custom.professional_testimonials`, `custom.mission_card`, `custom.how_it_works_steps`, `custom.compare_table…`):

1. **Root.** The product's metafields whose namespace and key match the family, and whose declared type is `metaobject_reference` or `list.metaobject_reference`. Any other type is not a root: a GID written inside a text field never counts.
2. **Edges.** From each metaobject, only fields whose declared type is a metaobject reference are followed, to depth 3. Each edge is recorded: from GID, field key, to GID, to type and handle. An unreadable object blocks every target below it.
3. **Shop-level objects** (the compare-table cells, which the table does not reference): only the handles listed in a reviewed file `registration/shop-objects.json`, with the storefront code that selects them (`sections/product-compare-plans.liquid`, `snippets/kc-plan-config.liquid`). No scan of all objects of a type.

## 2. Field proposals

Each text field of a reached metaobject is parsed:

- **Single-line or plain text:** the whole value is one segment.
- **Rich text (JSON):** text leaves only; node types, URLs and other structural keys stay as they are (existing `translate_json` rules).
- **HTML / multi-line:** `html.parser` builds a map of text nodes with their offsets. Start and end tags with their attributes, comments, and Liquid `{{ … }}` / `{% … %}` stay byte for byte. Malformed markup, Liquid inside a tag, or a node the map cannot place means no proposal.

Every text node (whitespace collapsed, entities decoded for comparison only) must equal exactly one plan segment. One unmapped node, one held or gated segment, or two values for one segment means no proposal, with the reason in the report.

A proposal records: item ids, EN and NL per segment, the node offsets, the edge path from the product, the field's EN digest and sha1, the full assembled NL, the current NL, and every other product or object that uses the same metaobject.

## 3. Review

The dry run writes `live/fields-proposed-<lang>.json` and a report section that lists each proposal in full. Astra reviews them; Victor may spot-check a few. Approved proposals go into `registration/bindings-fields.json` (resource, key, field EN sha1, item ids). That file is committed and its hash is part of the approval.

## 4. Write

Only fields in `bindings-fields.json` are written, in both the metafield and the metaobject route. A changed field EN or a changed edge stops that field: no fallback to equal text elsewhere. The approval snapshot also binds, per target, the edge path and the segment-to-item map. The writer, re-read, journal and receipts stay as reviewed in R18e–R18i.

## 5. Tests

- The R30 reproductions as regressions, each with negative proof against the parked first attempt: retargeting to a sibling field with the same EN; a GID in a text metafield; a missing root with a shop type; a reviewed binding ignored by the metafield route; held and gated siblings; `href`, `class`, `data-*`, comments, Liquid output and control tags, escaped text; CJK, Greek, Cyrillic and combining marks.
- Happy paths: plain, rich text, HTML with inline tags, nested references, shop objects from the reviewed list, a bound field with a changed EN stops.

## 6. Order of work

| Step | Who | Gate |
|---|---|---|
| 1. This plan | source-copy lane | short Astra design check |
| 2. Build discovery, parser, proposals, field bindings, tests | source-copy lane | Astra code review |
| 3. Read-only dry run | Victor, own Terminal | — |
| 4. Review of the field proposals into `bindings-fields.json` | Astra (Victor spot-check) | review report |
| 5. Fresh dry run with the bindings | Victor | Astra dry-run review |
| 6. Write NL, then FR | Victor | his explicit yes on each checksum |

Wave 2b does not change the selling-plan or theme routes of wave 2a, nor the credential handling.
