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
3. **Shop-level objects** (the compare-table cells, which the table does not reference): only the handles listed in a reviewed file `registration/shop-objects.json`, each pinned type + handle → GID, together with the selection the storefront makes: the table root reached from the product, and the plan and row IDs a cell must carry (`sections/product-compare-plans.liquid`, `snippets/kc-plan-config.liquid`). A cell whose plan or row is not in the current table selection is not a target. The file's hash is part of the approval. No scan of all objects of a type.
4. **Scope of the evidence.** A bounded outgoing walk cannot prove every other consumer of a shared metaobject. Each proposal states what is known (the products and objects found referencing it in this walk) and marks the scope "incomplete" when it cannot know more; an incomplete scope is shown to the reviewer and never approved automatically.

## 2. Field proposals

Each text field of a reached metaobject is parsed:

- **Single-line or plain text:** the whole value is one segment.
- **Rich text (JSON):** text leaves only; node types, URLs and other structural keys stay as they are (existing `translate_json` rules).
- **HTML / multi-line:** a raw-span scanner of our own (not `html.parser`'s callbacks, which tolerate broken markup and split text at entities) divides the value into tag spans, comment spans and text spans with their byte offsets. The spans must cover the whole value exactly once; otherwise there is no proposal. Tags and comments are opaque bytes, attributes included. `<script>` and `<style>` content, an unclosed `<`, a stray `>`, an unterminated comment or an entity that is not a well-formed named or numeric reference means no proposal.
- **Entities.** A text span is decoded once, for comparison only. The replacement is HTML-escaped and inserted at the original offsets; leading and trailing whitespace of the span and every byte outside replaced spans stay untouched.
- **Liquid.** Any field that contains `{{`, `{%`, `}}` or `%}` anywhere (plain, HTML or a JSON rich-text leaf) is not proposed in wave 2b; such fields are listed for a separate decision. A translation that would introduce those sequences is rejected too.

**What counts as text.** Every text span (and every JSON rich-text leaf) that is not whitespace-only must equal exactly one plan segment after collapsing whitespace: letters, digits, marks, punctuation, symbols and emoji of any script all count. Whitespace-only spans are kept as they are. The only structural exceptions are the ones `translate_json` already keeps (URLs, GIDs, numbers in the structural keys, the Subscription Name values); no other span is exempt. One unmapped span, one held, gated or conflicting segment, or two values for one segment means no proposal, with the reason in the report. The lookup keeps every plan row of the family, whatever its status; colliding rows are kept side by side, never overwritten.

**Split sentences stay blocked.** When inline markup (a link, bold) or rich-text leaves divide one approved sentence, the span map cannot place it: the field is reported as "split sentence" and not proposed. Such fields go forward only with explicitly reviewed segment locations and translations, or with an approved whole-field translation that passes the same structural check; fragments are never inferred.

A proposal records, per locale: the product GID and root metafield (namespace, key, declared type), the typed edge path, the destination GID, type and handle, the field key and its EN digest and sha1, every span (raw offsets, or JSON path) with its item id, EN, translation and status, the full assembled translation, the current translation, and the evidence scope (§1.4). Its hash, over all of that, is the proposal hash.

## 3. Review

The dry run writes `live/fields-proposed-<lang>.json` and a report section per language, grouped by family (FAQ, comparison section, treatment journey, professionals, mission card, compare table). Each group lists its unique resource/key proposals with EN / current / new side by side, coverage, the shared-use scope and any exception, with the full evidence linked. Astra reviews every proposed field; Victor gets the grouped summary to spot-check per group. Evidence is deduplicated, targets are not.

Approved proposals go into `registration/bindings-fields.json`, per locale, with the whole reviewed evidence of each field (or its immutable proposal hash plus the evidence file it was taken from, committed alongside). That file is committed and its hash is part of the approval.

## 4. Write

Only fields in `bindings-fields.json` are written, in both the metafield and the metaobject route. Before any mutation the run rebuilds the evidence of every bound field and compares it with the reviewed baseline: a changed field EN, edge, destination, span map, shop-object pin or table selection aborts the whole run before the first mutation (exit 2, the differences in the report). There is no per-item skip and no fallback to equal text elsewhere. The approval snapshot binds, per target, the proposal hash, the edge path and the span-to-item map. The writer, re-read, journal and receipts stay as reviewed in R18e–R18i.

## 5. Tests

- The R30 reproductions as regressions, each with negative proof against the parked first attempt: retargeting to a sibling field with the same EN; a GID in a text metafield; a missing root with a shop type; a reviewed binding ignored by the metafield route; held and gated siblings; `href`, `class`, `data-*`, comments, Liquid output and control tags, escaped text; CJK, Greek, Cyrillic and combining marks.
- R31 additions: stale provenance (changed edge, destination, shop-object pin or table selection) aborts the run before any mutation; Liquid in plain, HTML and JSON leaves is not proposed; entities split and rejoined with offsets kept; malformed HTML (unclosed tag, stray `>`, unterminated comment, bad entity, script/style); a split sentence is reported and not proposed; symbol-only and emoji spans must map; colliding held/active rows both kept.
- Happy paths: plain, rich text, HTML with inline tags whose spans each map, nested references, shop objects from the reviewed list; and the split-sentence case kept separate as an intended rejection.

## 6. Order of work

| Step | Who | Gate |
|---|---|---|
| 1. This plan | source-copy lane | Astra design check R31: ok with changes (folded in above) |
| 2. Build discovery, parser, proposals, field bindings, tests | source-copy lane | Astra code review |
| 3. Read-only dry run | Victor, own Terminal | — |
| 4. Review of the field proposals into `bindings-fields.json` | Astra (Victor spot-check) | review report |
| 5. Fresh dry run with the bindings | Victor | Astra dry-run review |
| 6. Write NL, then FR | Victor | his explicit yes on each checksum |

Wave 2b does not change the selling-plan or theme routes of wave 2a, nor the credential handling.
