#!/usr/bin/env python3
"""Offline payload builder and dry run for registering the NL/FR payloads in Shopify.

Reads the EN source (docs/source-copy/en-source.json) and the payloads
(docs/localization/nl/batch-*.json, docs/localization/fr/batch-*.json or --fr-dir) and writes:

  docs/localization/registration/plan-<lang>.json   per Shopify resource, the translationsRegister
                                                    input that can be built offline
  docs/localization/registration/DRY-RUN.md          counts, first wave, held back, run-time lookups

Nothing here talks to Shopify. Resource GIDs, translatable content keys and digests are fetched at
run time by register.py (translatableResources / translatableResourcesByIds, API 2026-10; product
metafields by GID through translatableResourcesByIds), by the owner, with read_translations. Every item carries the EN sha1 of the B1a capture: at run time the
live value must have the same sha1, or the item is stale and is skipped. Translations already registered by hand
(registration/registered.json) are left out while their EN sha1 matches, so no run overwrites them. Items held
by a review decision (registration/holds.json) stay in the plan with the reason in 'hold' and are never written.
Gates Victor released for publication (registration/releases.json) no longer hold an item.

Run from the repo root:  python3 docs/localization/registration/build_payloads.py [--fr-dir DIR]
"""
import argparse
import glob
import hashlib
import json
import os
import re
from collections import Counter, OrderedDict

SOURCE = "docs/source-copy/en-source.json"
OUT = "docs/localization/registration"
REGISTERED = os.path.join(OUT, "registered.json")
HOLDS = os.path.join(OUT, "holds.json")
RELEASES = os.path.join(OUT, "releases.json")
LANG_DIRS = {"nl": "docs/localization/nl", "fr": "docs/localization/fr"}

# The first wave (brief B4 part 3): PDP, homepage, header/footer, products, system.
FIRST_WAVE_BATCHES = {"batch-01-homepage", "batch-02-pdp", "batch-03-header-footer", "batch-05-products", "batch-08-system"}
LATER = {
    "batch-04-legal": "legal (batch 04)",
    "batch-06-content-pages": "content pages (batch 06), not in the first-wave list",
    "batch-07-collections-blog": "collections and blog (batch 07)",
}
GATES = ("legal-review", "pending-claim-review")
# Selling-plan names and descriptions are Shopify translations (Loop's Multilingual content has no field for them,
# checked 22 Oct); since wave 2 register.py writes them, keeping the Subscription Name values protected (B-01).

# Inventory field -> Shopify translatable content key, per Shopify type (TranslatableResourceType, 2026-10)
FIELD_KEYS = {
    "title": "title",
    "seo.title": "meta_title",
    "seo.description": "meta_description",
    "summary_html": "summary_html",
    "body_html": "body_html",
    "online_store.preferences.homepage_title": "meta_title",
    "online_store.preferences.homepage_meta_description": "meta_description",
}
OWNER_TYPES = {"product": "PRODUCT", "page": "PAGE", "article": "ARTICLE", "blog": "BLOG", "collection": "COLLECTION"}


def sha1(text):
    return hashlib.sha1(text.encode("utf-8")).hexdigest()


def load_payload(folder):
    out = OrderedDict()
    for path in sorted(glob.glob(os.path.join(folder, "batch-*.json"))):
        for entry in json.load(open(path, encoding="utf-8"))["entries"]:
            out[entry["id"]] = entry
    return out


def target(src):
    """(shopify_type, owner, kind, key, how) for an EN source entry; kind is direct, match, assemble or none."""
    rt, owner, kp = src["resource_type"], src["file_or_handle"], src["key_path"]
    split = re.match(r"^(body_html|body|main|banner|[a-z_]+\.[a-z_*]+(?:\|[a-z_.]+)?)#b?\d+$", kp)
    if rt == "template_setting":
        return "ONLINE_STORE_THEME_JSON_TEMPLATE", owner, "match", None, "key of the published theme's template (GID proves --theme-id), every hint a key token, then the EN sha1"
    if rt == "section_group":
        return "ONLINE_STORE_THEME_SECTION_GROUP", owner, "match", None, "key of the published theme's section group (GID proves --theme-id), every hint a key token, then the EN sha1"
    if rt == "theme_locale":
        return None, owner, "none", None, "locale file (Part 1 theme keys or Dawn's own key), not registered"
    if rt == "app":
        m = re.match(r"^selling_plan\.(\d+)\.(name|description|option[123])$", kp)
        if m:
            return "SELLING_PLAN", "gid://shopify/SellingPlan/" + m.group(1), "direct", m.group(2), "GID from the inventory id"
        if kp.startswith("selling_plan_group."):
            return "SELLING_PLAN_GROUP", "name: " + src["en"], "match", "name", "every group with this EN name (groups are shared by products)"
        if kp.startswith(("snippets/", "assets/")):
            return None, owner, "none", None, "Loop widget file: Loop owner handoff"
        return None, owner, "none", None, "app or Shopify content (%s): translated in the app or by Shopify" % owner
    if rt == "product" and kp.startswith("media."):
        media_id = kp.split(".")[1]
        return "MEDIA_IMAGE", "gid://shopify/MediaImage/" + media_id, "direct", "alt", "GID from the inventory id"
    if rt in OWNER_TYPES or rt in ("policy", "shop"):
        stype = OWNER_TYPES.get(rt) or {"policy": "SHOP_POLICY", "shop": "SHOP"}[rt]
        if src["id"].startswith("admin:system:") or (rt == "collection" and owner == "all"):
            if kp == "seo.description":
                return "SHOP", "shop", "match", "meta_description", "the shop meta description, as on the homepage"
            return None, owner, "none", None, "system page title composed by the theme and Shopify; verify after publishing"
        if split and split.group(1) in ("body_html", "body"):
            return stype, owner, "assemble", "body", "block replaced inside the live %s value" % ("body" if rt == "policy" else "body_html")
        if split:
            return stype, owner, "match", None, "text inside '%s' (title, metafield or app data): matched on the EN value at run time" % split.group(1)
        if rt == "policy" and kp != "body":
            return None, owner, "none", None, "SHOP_POLICY translates only body; policy titles come from Shopify"
        key = FIELD_KEYS.get(kp)
        if key:
            return stype, owner, "direct", key, "owner GID from translatableResources(%s), matched on handle" % stype
        return stype, owner, "match", None, "field %s matched on the EN value" % kp
    if rt == "metafield":
        return "METAFIELD", owner, "match", "value", "the product's metafield by namespace and key, translatableResourcesByIds (2026-10); whole value, or every JSON text leaf mapped"
    if rt == "metaobject":
        return "METAOBJECT", owner, "match", None, "metaobject reached through the product's metafield reference, field matched on the EN sha1"
    if rt == "navigation":
        return "LINK", owner, "match", "title", "menu link matched on its EN title"
    return None, owner, "none", None, "no Shopify target for resource_type " + str(rt)


def gates_of(entry, lang, released=()):
    """The review gates on a payload entry, minus the ones Victor released for publication (releases.json)."""
    status, flags = entry.get("status"), entry.get("flags") or []
    return [g for g in GATES if (status == g or g in flags) and g not in released]


def match_hint(src):
    """Section, block and setting ids for a theme setting: Shopify's dynamic key contains them."""
    m = re.match(r"^sections\.([^.]+)(?:\.blocks\.([^.]+))?\.settings\.([^.]+)$", src["key_path"])
    return [p for p in m.groups() if p] if m else None


def dedupe(res):
    """One item per (key or field, EN): the same text registered once; different translations of it are held."""
    seen = OrderedDict()
    for item in res["items"]:
        ident = (item["key"] if item["kind"] == "direct" or item["key"] == "meta_description" else item["field"], item["en_sha1"])
        if item["kind"] == "match" and item.get("hint"):
            ident = (tuple(item["hint"]), item["en_sha1"])
        first = seen.get(ident)
        if first is None:
            seen[ident] = item
        elif first["value"] == item["value"]:
            first.setdefault("same_as", []).append(item["id"])
        else:
            for i in (first, item):
                if "conflicting translations of the same EN" not in i["hold"]:
                    i["hold"].append("conflicting translations of the same EN")
            seen[ident + (item["id"],)] = item
    res["items"] = list(seen.values())


def build(lang, payload, sources, registered=None, holds=None, released=()):
    skipped = Counter()
    resources = OrderedDict()
    registered = registered or {}
    holds = holds or {}
    for eid, entry in payload.items():
        src = sources.get(eid)
        if src is None:
            skipped["not in the EN source (stale payload id)"] += 1
            continue
        if src.get("retired"):
            skipped["retired in the EN source"] += 1
            continue
        done = registered.get(eid)
        if done and done["en_sha1"] == src["sha1"]:
            skipped["already registered by hand (registered.json)"] += 1
            continue
        value = entry.get(lang)
        status = entry.get("status")
        stype, owner, kind, key, how = target(src)
        if status == "held":
            skipped["held"] += 1
            continue
        if src.get("never_translate"):
            skipped["never_translate"] += 1
            continue
        if status in ("theme-key", "dawn-nl", "locale-present"):
            skipped["%s: locale file, not registered" % status] += 1
            continue
        if not value:
            skipped["no %s value" % lang.upper()] += 1
            continue
        if value.strip() == src["en"].strip():
            skipped["unchanged (same as EN)"] += 1
            continue
        if kind == "none":
            skipped["no registration route: " + how.split(":")[0]] += 1
            continue
        if entry.get("en_sha1") and entry["en_sha1"] != src["sha1"]:
            skipped["payload EN differs from the source (re-translate)"] += 1
            continue
        gates = gates_of(entry, lang, released)
        batch = src["batch"]
        hold = list(gates)
        if batch not in FIRST_WAVE_BATCHES:
            hold.append(LATER.get(batch, batch))
        if eid in holds:
            hold.append("review hold (holds.json): " + holds[eid])
        rid = "%s|%s" % (stype, owner)
        res = resources.setdefault(rid, OrderedDict(
            shopify_type=stype, owner=owner, batch=batch, page=src.get("page"), items=[]))
        item = OrderedDict(
            id=eid, kind=kind, key=key, field=src["key_path"], en=src["en"], en_sha1=src["sha1"],
            value=value, gates=gates, hold=hold, how=how,
            status=OrderedDict(drafted=True, registered=False))
        if stype.startswith("ONLINE_STORE_THEME"):
            item["hint"] = match_hint(src)
        res["items"].append(item)
    for res in resources.values():
        dedupe(res)
    # Assembled fields: one translation per field, held when any of its blocks is held or missing, or carries a
    # gate (pending-claim-review, legal-review): registering the field would publish the gated block with it
    for res in resources.values():
        blocks = [i for i in res["items"] if i["kind"] == "assemble"]
        if not blocks:
            continue
        src_blocks = [s for s in sources.values() if s["file_or_handle"] == res["owner"]
                      and target(s)[0] == res["shopify_type"] and target(s)[2] == "assemble"]
        ready = {i["id"] for i in blocks}
        missing = [s["id"] for s in src_blocks if s["id"] not in ready]
        gated = [i["id"] for i in blocks if i["gates"]]
        res["assembled_field"] = OrderedDict(blocks=len(src_blocks), drafted=len(blocks), missing_or_held=len(missing),
                                             gated=len(gated))
        if missing:
            for i in blocks:
                i["hold"].append("partial field: %d of %d blocks held or untranslated" % (len(missing), len(src_blocks)))
        elif gated:
            for i in blocks:
                if not i["gates"]:
                    i["hold"].append("gated field: %d of %d blocks wait for a review" % (len(gated), len(src_blocks)))
    return resources, skipped


def wave_counts(resources):
    first, held = Counter(), Counter()
    for res in resources.values():
        for i in res["items"]:
            if i["hold"]:
                for h in sorted(set(re.sub(r"\d+ of \d+", "n of m", h) for h in i["hold"])):
                    held[h] += 1
            else:
                first[res["shopify_type"]] += 1
    return first, held


def markdown(results, sources, args):
    lines = ["# Registration dry run (B4 part 3)", "",
             "Generated by `docs/localization/registration/build_payloads.py`. Offline: nothing was sent to Shopify, "
             "no IDs or digests are known yet. Status per item: **drafted** (payload exists) / **registered** "
             "(translationsRegister accepted it) / **published** (the locale is published in Settings > Languages). "
             "Today every item is drafted and none is registered by the runner; entries already registered by hand "
             "(`registered.json`) are left out of the plan. **NL and FR are already published** (the live "
             "`/nl` and `/fr` URLs serve 200 with `lang` and `hreflang`, B4-REPORT part 4), so a registered item is "
             "public at once: there is no separate publish step left to hold it back.", "",
             "Inputs (sha1 of each file, so a rerun can be compared): %s." % "; ".join(
                 "%s `%s`" % (label, digest) for label, digest in input_digests(args).items()), "",
             "Regenerate right before a registration run: the plan is only as current as these inputs.", ""]
    for lang, (resources, skipped) in results.items():
        first, held = wave_counts(resources)
        items = sum(len(r["items"]) for r in resources.values())
        lines += ["## %s" % lang.upper(), "",
                  "%d payload entries become %d registration items on %d Shopify resources; %d are first wave, %d held back." % (
                      sum(skipped.values()) + items, items, len(resources), sum(first.values()), items - sum(first.values())), "",
                  "### Items per Shopify type", "",
                  "| Shopify type | Resources | Items | First wave | Held back |", "|---|---:|---:|---:|---:|"]
        per_type = OrderedDict()
        for res in resources.values():
            t = per_type.setdefault(res["shopify_type"], [0, 0, 0])
            t[0] += 1
            t[1] += len(res["items"])
            t[2] += sum(1 for i in res["items"] if not i["hold"])
        for stype, (nres, nitems, nfirst) in sorted(per_type.items()):
            lines.append("| `%s` | %d | %d | %d | %d |" % (stype, nres, nitems, nfirst, nitems - nfirst))
        lines += ["", "### Items per batch", "", "| Batch | Items | First wave |", "|---|---:|---:|"]
        per_batch = Counter()
        per_batch_first = Counter()
        for res in resources.values():
            for i in res["items"]:
                per_batch[sources[i["id"]]["batch"]] += 1
                per_batch_first[sources[i["id"]]["batch"]] += 0 if i["hold"] else 1
        for b in sorted(per_batch):
            lines.append("| `%s` | %d | %d |" % (b, per_batch[b], per_batch_first[b]))
        lines += ["", "### Held back (an item can have several reasons)", "", "| Reason | Items |", "|---|---:|"]
        for reason, n in held.most_common():
            lines.append("| %s | %d |" % (reason, n))
        lines += ["", "### Not registered at all", "", "| Reason | Entries |", "|---|---:|"]
        for reason, n in skipped.most_common():
            lines.append("| %s | %d |" % (reason, n))
        lines += ["", "### First-wave resources", "", "| Shopify type | Owner | Items | How the key is found |", "|---|---|---:|---|"]
        for res in resources.values():
            n = sum(1 for i in res["items"] if not i["hold"])
            if n:
                hows = sorted(set(i["kind"] for i in res["items"] if not i["hold"]))
                lines.append("| `%s` | `%s` | %d | %s |" % (res["shopify_type"], res["owner"], n, ", ".join(hows)))
        lines.append("")
    lines += ["## Fetched at run time by register.py (API 2026-10; nothing stored but the reports)", "",
              "This file is an offline planning summary, not an approval. The approval is the live dry run of "
              "`register.py` (`live/dry-run-<lang>.md`, review R18): it resolves every target by identity first and EN second "
              "and writes only what one checksum covers.", "",
              "| Shopify type | Query | Identity rule |", "|---|---|---|",
              "| `ONLINE_STORE_THEME_JSON_TEMPLATE`, `ONLINE_STORE_THEME_SECTION_GROUP` | `translatableResources(resourceType: …)` | only resources whose GID names the template and carries the supplied numeric `--theme-id` in the `theme_id` parameter, the theme proven published (`themes(roles: MAIN)` with read_themes, or a same-day `--theme-attested`); every hint a token of the key; then the EN sha1 |",
              "| `PRODUCT`, `PAGE`, `ARTICLE`, `BLOG`, `COLLECTION` | `translatableResources(resourceType: …)` | exactly one resource with the `handle`; the plan's key |",
              "| `MEDIA_IMAGE` | `translatableResourcesByIds(resourceIds: …)` | the GID in the plan; the plan's key |",
              "| Metafields | `product { metafields { id namespace key type value } }`, then `translatableResourcesByIds` on their GIDs (key `value`) | namespace and key of the field; a JSON field only when every text leaf maps to an approved item |",
              "| `METAOBJECT` (and the metaobjects behind reference metafields) | the product's reference-typed metafields, then reference-typed fields to depth 3 (`metaobject` reads, read_metaobjects); shop-level cells only from the reviewed `shop-objects.json`, pinned to GID and selected by the product's table | written only on a field the inventory names, an item a reviewed `bindings.json` binds, or a field a reviewed `bindings-fields.json` binds with unchanged evidence; otherwise the dry run proposes the field with its spans, path and translations (`live/fields-proposed-<lang>.json`); a changed bound field aborts the write before any mutation; Liquid, uncertain markup and split sentences are never proposed |",
              "| `SHOP` | `translatableResources(resourceType: SHOP)` | the single shop resource; the plan's key |",
              "| `LINK`, `SHOP_POLICY` | none yet | owner route not verified: never written |",
              "| `SELLING_PLAN`, `SELLING_PLAN_GROUP` | the plan's GID; every group with the EN name | name, description and options only; the Subscription Name values '60-Day Supply' / 'Year Supply' stay untranslated (B-01) |",
              "| Existing translations | `translations(locale: \"nl\" / \"fr\")` on each resource | part of the approval: a translation edited after the dry run stops the write |",
              "", "Write: rebuild the snapshot and compare its checksum, re-read each resource right before its mutation, then "
              "`translationsRegister(resourceId, translations)` with `{key, locale, value, translatableContentDigest}` in chunks of 50; "
              "every attempt and result goes to `live/journal-<lang>.jsonl`. Never-translate translations (`handle_item`, "
              "`selling_plan_id`, Subscription Name values) are removed only with `--remove-never` in both the dry run and the write. "
              "Handles are not in the payloads.", ""]
    return "\n".join(lines)


def file_sha1(path):
    with open(path, "rb") as f:
        return hashlib.sha1(f.read()).hexdigest()[:12]


def input_digests(args):
    out = OrderedDict([("en-source.json", file_sha1(args.source))])
    for path in (REGISTERED, HOLDS, RELEASES):
        if os.path.exists(path):
            out[os.path.basename(path)] = file_sha1(path)
    for lang, folder in (("nl", args.nl_dir), ("fr", args.fr_dir)):
        for path in sorted(glob.glob(os.path.join(folder or "", "batch-*.json"))) if folder else []:
            out["%s/%s" % (lang, os.path.basename(path))] = file_sha1(path)
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--source", default=SOURCE)
    parser.add_argument("--nl-dir", default=LANG_DIRS["nl"])
    parser.add_argument("--fr-dir", default=LANG_DIRS["fr"] if os.path.isdir(LANG_DIRS["fr"]) else None)
    args = parser.parse_args()
    source_doc = json.load(open(args.source, encoding="utf-8"))
    sources = OrderedDict((e["id"], e) for e in source_doc["entries"])
    dirs = {"nl": args.nl_dir}
    if args.fr_dir:
        dirs["fr"] = args.fr_dir
    registered = json.load(open(REGISTERED, encoding="utf-8"))["registered"] if os.path.exists(REGISTERED) else {}
    holds = json.load(open(HOLDS, encoding="utf-8"))["holds"] if os.path.exists(HOLDS) else {}
    released = tuple(json.load(open(RELEASES, encoding="utf-8"))["released"]) if os.path.exists(RELEASES) else ()
    results = OrderedDict()
    for lang, folder in dirs.items():
        resources, skipped = build(lang, load_payload(folder), sources, registered.get(lang), holds.get(lang), released)
        results[lang] = (resources, skipped)
        doc = OrderedDict(
            lang=lang,
            inputs=OrderedDict((k, v) for k, v in input_digests(args).items() if not k[:3] in ("nl/", "fr/") or k.startswith(lang + "/")),
            batches={b: v["digest"] for b, v in source_doc["batches"].items()},
            published="already published on the live store (observed 2026-10-19, B4-REPORT part 4)",
            resources=list(resources.values()))
        with open(os.path.join(OUT, "plan-%s.json" % lang), "w", encoding="utf-8") as f:
            json.dump(doc, f, ensure_ascii=False, indent=1)
            f.write("\n")
    with open(os.path.join(OUT, "DRY-RUN.md"), "w", encoding="utf-8") as f:
        f.write(markdown(results, sources, args))
    for lang, (resources, skipped) in results.items():
        first, _ = wave_counts(resources)
        items = sum(len(r["items"]) for r in resources.values())
        print("%s: %d items on %d resources, %d first wave; %d entries not registered" % (
            lang, items, len(resources), sum(first.values()), sum(skipped.values())))


if __name__ == "__main__":
    main()
