"""Recompute and check the EN source digests, in en-source.json and in every batch file.

Usage, from the repo root:  python3 docs/source-copy/digest.py [--dir <folder holding en-source.json and batches/>]

Each entry's sha1 is sha1(en) over UTF-8. A batch digest is the sha1 over its entries' sha1 values, sorted and
joined with a newline (no trailing newline), so a changed EN string changes only the digest of its own batch.

Checks:
- en-source.json: unique ids; every entry's sha1 equals sha1(en); every batch digest and entry count in
  "batches" equals the value recomputed from its entries.
- every batch file, independently: it exists for each canonical batch and names that batch; its ids are
  unique; each entry's sha1 equals sha1(en) of that file's own en; the digest recomputed from the file's
  entries equals the file's stored digest and the canonical digest; its ids are exactly the canonical
  batch's ids (none missing, none extra); and each entry equals the canonical entry field by field.
- no batch file exists for a batch that en-source.json does not define.
Exit code 1 on any failure, 0 when everything matches."""
import argparse
import glob
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def sha1(text):
    return hashlib.sha1(text.encode("utf-8")).hexdigest()


def batch_digest(entries):
    return sha1("\n".join(sorted(sha1(e["en"]) for e in entries)))


def check_entries(label, entries, problems):
    """Unique ids and sha1(en) for a list of entries; returns {id: entry}."""
    by_id = {}
    for e in entries:
        if e["id"] in by_id:
            problems.append("%s: duplicate id %s" % (label, e["id"]))
        by_id[e["id"]] = e
        if e.get("sha1") != sha1(e["en"]):
            problems.append("%s: sha1 does not match en for %s" % (label, e["id"]))
    return by_id


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--dir", default=HERE, help="folder that holds en-source.json and batches/ (default: this script's folder)")
    root = parser.parse_args().dir
    source = json.load(open(os.path.join(root, "en-source.json"), encoding="utf-8"))
    problems = []

    canonical = check_entries("en-source.json", source["entries"], problems)
    by_batch = {}
    for e in source["entries"]:
        by_batch.setdefault(e["batch"], []).append(e)

    for name in sorted(set(by_batch) - set(source["batches"])):
        problems.append("en-source.json: entries for undeclared batch %s" % name)
    files = {os.path.basename(p)[:-5] for p in glob.glob(os.path.join(root, "batches", "*.json"))}
    for name in sorted(files - set(source["batches"])):
        problems.append("batches/%s.json: no such batch in en-source.json" % name)

    for name, meta in source["batches"].items():
        before = len(problems)
        entries = by_batch.get(name, [])
        digest = batch_digest(entries)
        if digest != meta["digest"]:
            problems.append("en-source.json: %s digest %s, recomputed %s" % (name, meta["digest"], digest))
        if len(entries) != meta["entries"]:
            problems.append("en-source.json: %s declares %d entries, holds %d" % (name, meta["entries"], len(entries)))

        path = os.path.join(root, "batches", name + ".json")
        if not os.path.exists(path):
            problems.append("batches/%s.json: missing" % name)
            print("%-26s %4d entries  %s  MISSING FILE" % (name, len(entries), digest))
            continue
        batch_file = json.load(open(path, encoding="utf-8"))
        label = "batches/%s.json" % name
        if batch_file.get("batch") != name:
            problems.append("%s: names batch %r" % (label, batch_file.get("batch")))
        file_entries = batch_file.get("entries", [])
        in_file = check_entries(label, file_entries, problems)
        file_digest = batch_digest(file_entries)
        if file_digest != batch_file.get("digest"):
            problems.append("%s: stored digest %s, recomputed from its entries %s" % (label, batch_file.get("digest"), file_digest))
        if file_digest != meta["digest"]:
            problems.append("%s: digest of its entries %s differs from the canonical %s" % (label, file_digest, meta["digest"]))
        want = {e["id"] for e in entries}
        for i in sorted(want - set(in_file)):
            problems.append("%s: missing id %s" % (label, i))
        for i in sorted(set(in_file) - want):
            problems.append("%s: extra id %s" % (label, i))
        for i in sorted(want & set(in_file)):
            a, b = canonical[i], in_file[i]
            fields = sorted(k for k in set(a) | set(b) if a.get(k) != b.get(k))
            if fields:
                problems.append("%s: %s differs from en-source.json in %s" % (label, i, ", ".join(fields)))
        state = "ok" if len(problems) == before else "MISMATCH"
        print("%-26s %4d entries  %s  %s" % (name, len(entries), digest, state))

    for p in problems:
        print("ERROR", p)
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
