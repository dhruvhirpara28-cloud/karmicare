"""Check the NL batch files against the EN source.

Usage, from the repo root:  python3 docs/localization/nl/validate.py
For every batch: the file exists, its source_digest equals the EN batch digest, every EN entry is present once,
each en_sha1 equals sha1(en) and the source entry's sha1, held entries carry no Dutch, and all others do.
Exit code 1 on any failure, so a later EN change shows up as a stale entry here."""
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "..", "..", "source-copy", "en-source.json")


def main():
    src = json.load(open(SOURCE, encoding="utf-8"))
    by_batch = {}
    for e in src["entries"]:
        by_batch.setdefault(e["batch"], {})[e["id"]] = e
    ok = True
    for batch, meta in src["batches"].items():
        path = os.path.join(HERE, batch + ".json")
        if not os.path.exists(path):
            print("%-26s missing" % batch)
            ok = False
            continue
        doc = json.load(open(path, encoding="utf-8"))
        errors = []
        if doc["source_digest"] != meta["digest"]:
            errors.append("source digest changed: re-translate the changed entries")
        seen = set()
        for r in doc["entries"]:
            e = by_batch[batch].get(r["id"])
            if e is None:
                errors.append("unknown id " + r["id"])
                continue
            if r["id"] in seen:
                errors.append("duplicate id " + r["id"])
            seen.add(r["id"])
            if r["en_sha1"] != e["sha1"] or r["en_sha1"] != hashlib.sha1(r["en"].encode("utf-8")).hexdigest():
                errors.append("stale entry " + r["id"])
            if r["status"] == "held" and r["nl"]:
                errors.append("held entry has Dutch " + r["id"])
            if r["status"] != "held" and not (r["nl"] or "").strip():
                errors.append("no Dutch " + r["id"])
        missing = set(by_batch[batch]) - seen
        if missing:
            errors.append("%d EN entries not covered" % len(missing))
        print("%-26s %4d entries  %s" % (batch, len(doc["entries"]), "ok" if not errors else "; ".join(errors[:3])))
        ok = ok and not errors
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
