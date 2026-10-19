"""Check the FR translation payloads against the EN source.

Usage, from the repo root:  python3 docs/localization/fr/check.py
Errors (exit code 1): a batch digest or an entry sha1 that no longer matches the EN source, a missing or
extra entry, a status outside the vocabulary, a FR value that drops or changes markup, Liquid, [tokens]
or the runtime price spans, and French typography slips (plain space or no space before : ; ! ? € % »,
straight apostrophes, €-before-amount). Warnings: words the brand rules ban, forbidden claim verbs and
tu-forms, for a human to confirm."""
import glob
import hashlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "..", "..", "source-copy")

STATUSES = {"translated", "admin", "theme-key", "locale-present", "held"}
FLAGS = {"pending-claim-review", "pending-en-review", "fit-risk", "source-defect", "legal-review",
         "gendered-title", "wording-adapted", "not-rendered"}
DYNAMIC = re.compile(r'<span class="(?:kc-dynamic_price|dynamic_free_welcome_price)">[^<]*</span>')
SKIP = re.compile(r"(<[^>]*>|\{\{.*?\}\}|\{%.*?%\}|&[a-zA-Z#0-9]+;|\[[a-z_]+\])", re.S)
BANNED = re.compile(r"\b(produits?|tubes?|achats?|achet\w*|utilis\w*|emploi)\b", re.I)
FORBIDDEN = re.compile(r"\b(prévien\w*|préven\w*|prévenir|guéri\w*|traite|traiter|traitent)\b", re.I)
TU = re.compile(r"\b(tu|ton|ta|tes|toi)\b", re.I)


def sha1(text):
    return hashlib.sha1(text.encode("utf-8")).hexdigest()


def text_nodes(value):
    value = DYNAMIC.sub(" ", value)
    return [p for p in SKIP.split(value) if p and not SKIP.fullmatch(p)]


def structure(value):
    return (re.findall(r"<[^>]*>", value), sorted(re.findall(r"\{\{.*?\}\}|\{%.*?%\}", value)),
            sorted(re.findall(r"\[[a-z_]+\]", value)), DYNAMIC.findall(value), value.count("&nbsp;"))


def typography(value, key_path):
    problems = []
    for node in text_nodes(value):
        if re.search(r" [:;!?€%»]", node):
            problems.append("plain space before : ; ! ? € % or »")
        if re.search(r"[^\s  \d][;!?»]", node):
            problems.append("no space before ; ! ? or »")
        if re.search(r"[A-Za-zÀ-ÿ)][:](?!//)", node) and not key_path.endswith("custom_button_text_by_plan"):
            problems.append("no space before :")
        if "«" in node and not re.search("« ", node):
            problems.append("no space after «")
        if "'" in node:
            problems.append("straight apostrophe")
        if re.search(r"€\s?\d", node):
            problems.append("€ before the amount")
        if re.search(r"\d €|\d€", node):
            problems.append("amount and € not joined by U+00A0")
    return problems


def main():
    source = json.load(open(os.path.join(SOURCE, "en-source.json"), encoding="utf-8"))
    errors, warnings = [], []
    files = sorted(glob.glob(os.path.join(HERE, "batch-*.json")))
    if not files:
        sys.exit("no FR batch files found")
    for path in files:
        doc = json.load(open(path, encoding="utf-8"))
        name = doc["batch"]
        src = json.load(open(os.path.join(SOURCE, "batches", name + ".json"), encoding="utf-8"))
        digest = sha1("\n".join(sorted(sha1(e["en"]) for e in src["entries"])))
        if not (doc["source_digest"] == src["digest"] == digest == source["batches"][name]["digest"]):
            errors.append("%s: source digest changed (FR built from %s, EN now %s)" % (name, doc["source_digest"], digest))
        src_ids = [e["id"] for e in src["entries"]]
        fr_ids = [e["id"] for e in doc["entries"]]
        if src_ids != fr_ids:
            errors.append("%s: entry ids differ from the source batch (missing %d, extra %d)" % (
                name, len(set(src_ids) - set(fr_ids)), len(set(fr_ids) - set(src_ids))))
        by_id = {e["id"]: e for e in src["entries"]}
        counts = {}
        for e in doc["entries"]:
            where = "%s %s" % (name, e["id"])
            s = by_id.get(e["id"])
            if s is None:
                continue
            if e["en"] != s["en"] or e["en_sha1"] != s["sha1"] or e["en_sha1"] != sha1(e["en"]):
                errors.append(where + ": EN text or en_sha1 out of date")
            if e["status"] not in STATUSES:
                errors.append(where + ": unknown status " + e["status"])
            for f in e["flags"]:
                if f not in FLAGS:
                    errors.append(where + ": unknown flag " + f)
            counts[e["status"]] = counts.get(e["status"], 0) + 1
            if e["status"] == "held":
                if e["fr"] is not None or not e["notes"]:
                    errors.append(where + ": held entries carry fr = null and a reason in notes")
                continue
            if not e["fr"]:
                errors.append(where + ": empty FR")
                continue
            if e["status"] == "locale-present":
                continue
            if structure(e["en"]) != structure(e["fr"]):
                errors.append(where + ": markup, Liquid, [tokens] or runtime spans differ from the EN")
            if e["key_path"].endswith("custom_button_text_by_plan"):
                ids_en = re.findall(r"^(\d+): ", e["en"], re.M)
                if ids_en != re.findall(r"^(\d+): ", e["fr"], re.M):
                    errors.append(where + ": selling-plan IDs changed")
            for p in typography(e["fr"], e["key_path"]):
                errors.append(where + ": " + p)
            nodes = " ".join(text_nodes(e["fr"]))
            for m in BANNED.findall(nodes):
                warnings.append(where + ": banned-word check: '" + m + "'")
            for m in FORBIDDEN.findall(nodes):
                warnings.append(where + ": claim-verb check: '" + m + "'")
            for m in TU.findall(nodes):
                warnings.append(where + ": tu-form check: '" + m + "'")
        if counts != doc["counts"]:
            errors.append(name + ": counts block does not match the entries")
        print("%-24s %4d entries  %s  %s" % (name, len(doc["entries"]), doc["source_digest"], json.dumps(counts, sort_keys=True)))
    for w in warnings:
        print("warning:", w)
    for e in errors:
        print("ERROR:", e)
    print("%d errors, %d warnings" % (len(errors), len(warnings)))
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
