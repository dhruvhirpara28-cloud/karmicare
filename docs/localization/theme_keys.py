#!/usr/bin/env python3
"""Theme locale keys (kc.*) for the hardcoded strings of the B1a inventory.

docs/localization/theme-keys.json maps each key to its inventory ids and holds the EN, NL and FR
values. Run from the repo root:

  python3 docs/localization/theme_keys.py refresh [--fr-dir DIR]   values and holds from the sources
  python3 docs/localization/theme_keys.py check [--fr-dir DIR] [--area A ...]
  python3 docs/localization/theme_keys.py write [--area A ...]     the kc block of every storefront locale

Values: en.default.json gets en. nl.json and fr.json get their language unless *_hold is set (no
translated value, or an entry status that is not theme-key), then en. pending-claim-review and
legal-review do not hold a key (Victor, 20 Oct: translate everything; the reviews gate publication
and registration): they are listed in *_review as the record of the open review. Every other
storefront locale gets en, so Theme Check MatchingTranslations finds the same keys everywhere.
A row's "decided" ({lang: value, "by": who and where}) records a value Victor chose; it wins over the
payload, so refresh keeps it whatever the payload says.

write merges into the existing "kc" object in its current key order (other kc keys, such as
kc.general.coming_soon and kc.receipt, stay where they are; new keys go at the end of their area)
and leaves the rest of each file as it is. FR payloads live in docs/localization/fr; until that folder is
on this branch, pass --fr-dir (refresh and check skip FR without it).
"""
import argparse
import glob
import json
import os
import re
import sys

MAP = "docs/localization/theme-keys.json"
SOURCE = "docs/source-copy/en-source.json"
NL_DIR = "docs/localization/nl"
FR_DIR = "docs/localization/fr"
GATES = ("pending-claim-review", "legal-review")
THEME_DIRS = ("assets", "blocks", "layout", "sections", "snippets", "templates")


def load_payload(folder):
    out = {}
    for path in sorted(glob.glob(os.path.join(folder, "batch-*.json"))):
        for entry in json.load(open(path, encoding="utf-8"))["entries"]:
            out[entry["id"]] = entry
    return out


def resolve(payload, ids, lang, src):
    """The one value the ids share in this language, what holds it back (None: it can ship), and the
    open reviews that do not hold it (None: none)."""
    values, holds, reviews = set(), [], []
    for i in ids:
        entry = payload.get(i)
        if not entry or not entry.get(lang):
            holds.append("no %s value for %s" % (lang.upper(), i))
            continue
        values.add(entry[lang])
        if entry.get("status") not in ("theme-key",) + GATES:
            holds.append("status " + str(entry.get("status")))
        for gate in GATES:
            if entry.get("status") == gate or gate in (entry.get("flags") or []):
                claims = src.get(i, {}).get("claims") or []
                reviews.append(gate + (" (" + ", ".join(claims) + ")" if claims and gate == "pending-claim-review" else ""))
    if not ids:
        holds.append("not in the B1a inventory [NEEDS APPROVED COPY]")
    if len(values) > 1:
        sys.exit("%s ids disagree on %s: %s" % (lang, ids, sorted(values)))
    return ((values.pop() if values else None), ("; ".join(sorted(set(holds))) or None),
            ("; ".join(sorted(set(reviews))) or None))


def refreshed(doc, fr_dir):
    src = {e["id"]: e for e in json.load(open(SOURCE, encoding="utf-8"))["entries"]}
    payloads = {"nl": load_payload(NL_DIR)}
    if fr_dir:
        payloads["fr"] = load_payload(fr_dir)
    rows = []
    for row in doc["keys"]:
        row = dict(row)
        ens = {src[i]["en"] for i in row["ids"]}
        if len(ens) > 1:
            sys.exit("EN disagrees for " + row["key"])
        if ens:
            row["en"] = ens.pop()
        for lang, payload in payloads.items():
            row[lang], row[lang + "_hold"], row[lang + "_review"] = resolve(payload, row["ids"], lang, src)
            if lang in row.get("decided", {}):
                row[lang], row[lang + "_hold"] = row["decided"][lang], None
        rows.append(row)
    return dict(doc, keys=rows)


def value(row, lang):
    text = row[lang] if lang in ("nl", "fr") and row.get(lang) and not row.get(lang + "_hold") else row["en"]
    for name in row.get("href", []):
        if "<a>" not in text:
            sys.exit("%s: fewer <a> tags than href names" % row["key"])
        text = text.replace("<a>", '<a href="{{ %s }}">' % name, 1)
    if "<a>" in text:
        sys.exit("%s: more <a> tags than href names" % row["key"])
    return text


def storefront_locales():
    return sorted(p for p in glob.glob("locales/*.json") if not p.endswith(".schema.json"))


def lang_of(path):
    name = os.path.basename(path)[: -len(".json")]
    return {"en.default": "en", "nl": "nl", "fr": "fr"}.get(name, "en")


def split_locale(text):
    """Shopify's comment header, and the JSON body."""
    start = text.index("*/") + 2 if text.startswith("/*") else 0
    return text[:start], text[start:]


def expected_kc(rows, lang, kc):
    kc = json.loads(json.dumps(kc))
    for row in rows:
        _, area, name = row["key"].split(".", 2)
        kc.setdefault(area, {})[name] = value(row, lang)
    return kc


def write_locale(path, rows):
    text = open(path, encoding="utf-8").read()
    header, body = split_locale(text)
    data = json.loads(body)
    kc = expected_kc(rows, lang_of(path), data.get("kc", {}))
    dumped = json.dumps(kc, ensure_ascii=False, indent=2).split("\n")
    block = ['  "kc": ' + dumped[0]] + ["  " + line for line in dumped[1:]]
    lines = body.split("\n")
    if "kc" in data:
        start = lines.index('  "kc": {')
        end = next(n for n in range(start + 1, len(lines)) if lines[n] in ("  },", "  }"))
        block[-1] += "," if lines[end].endswith(",") else ""
        lines[start : end + 1] = block
    else:
        opening = lines.index("{")
        block[-1] += ","
        lines[opening + 1 : opening + 1] = block
    new_body = "\n".join(lines)
    new_data = json.loads(new_body)
    rest = {k: v for k, v in data.items() if k != "kc"}
    if {k: v for k, v in new_data.items() if k != "kc"} != rest or new_data["kc"] != kc:
        sys.exit("write check failed for " + path)
    if header + new_body != text:
        with open(path, "w", encoding="utf-8") as f:
            f.write(header + new_body)
        return True
    return False


def theme_text():
    chunks = []
    for folder in THEME_DIRS:
        for path in glob.glob(os.path.join(folder, "**", "*"), recursive=True):
            if os.path.isfile(path) and path.endswith((".liquid", ".json", ".js")):
                chunks.append(open(path, encoding="utf-8").read())
    return "\n".join(chunks)


def check(doc, fr_dir, rows):
    problems = []
    fresh = {r["key"]: r for r in refreshed(doc, fr_dir)["keys"]}
    langs = ["en", "nl"] + (["fr"] if fr_dir else [])
    fields = [f for lang in langs for f in ((lang, lang + "_hold", lang + "_review") if lang != "en" else ("en",))]
    for row in rows:
        for field in fields:
            if fresh[row["key"]].get(field) != row.get(field):
                problems.append("%s: %s is %r, the sources give %r" % (row["key"], field, row.get(field), fresh[row["key"]].get(field)))
    code = theme_text()
    for row in rows:
        if "'%s'" % row["key"] not in code:
            problems.append("%s: no '%s' | t in the theme" % (row["key"], row["key"]))
    known = {r["key"] for r in doc["keys"]}
    for key in sorted(set(re.findall(r"'(kc\.[a-z0-9_.]+)'\s*\|\s*t\b", code)) - known):
        print("note: %s is used in the theme and not in %s" % (key, MAP))
    for path in storefront_locales():
        data = json.loads(split_locale(open(path, encoding="utf-8").read())[1])
        for row in rows:
            _, area, name = row["key"].split(".", 2)
            got = data.get("kc", {}).get(area, {}).get(name)
            if got != value(row, lang_of(path)):
                problems.append("%s: %s is %r" % (path, row["key"], got))
    return problems


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("command", choices=("refresh", "check", "write"))
    parser.add_argument("--area", action="append", help="only these areas (check, write)")
    parser.add_argument("--fr-dir", default=FR_DIR if os.path.isdir(FR_DIR) else None)
    args = parser.parse_args()
    doc = json.load(open(MAP, encoding="utf-8"))
    rows = [r for r in doc["keys"] if not args.area or r["area"] in args.area]
    if args.area and not rows:
        sys.exit("no keys in area " + ", ".join(args.area))

    if args.command == "refresh":
        new = refreshed(doc, args.fr_dir)
        with open(MAP, "w", encoding="utf-8") as f:
            json.dump(new, f, ensure_ascii=False, indent=1)
            f.write("\n")
        held = [r["key"] for r in new["keys"] if r.get("nl_hold") or r.get("fr_hold")]
        print("%d keys refreshed (FR %s); %d with a hold" % (len(new["keys"]), args.fr_dir or "skipped", len(held)))
    elif args.command == "write":
        changed = [p for p in storefront_locales() if write_locale(p, rows)]
        print("%d keys; %d of %d storefront locale files changed" % (len(rows), len(changed), len(storefront_locales())))
    else:
        problems = check(doc, args.fr_dir, rows)
        for p in problems:
            print(p)
        print("%d keys checked (FR %s): %s" % (len(rows), args.fr_dir or "skipped", "%d problems" % len(problems) if problems else "ok"))
        sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
