"""Recompute and check the EN source digests.

Usage, from the repo root:  python3 docs/source-copy/digest.py
Each entry's sha1 is sha1(en) over UTF-8. A batch digest is the sha1 over its entries' sha1 values,
sorted and joined with a newline, so a changed EN string changes only the digest of its own batch.
Exit code 1 when a stored value no longer matches."""
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def sha1(text):
    return hashlib.sha1(text.encode("utf-8")).hexdigest()


def batch_digest(entries):
    return sha1("\n".join(sorted(sha1(e["en"]) for e in entries)))


def main():
    source = json.load(open(os.path.join(HERE, "en-source.json"), encoding="utf-8"))
    ok = True
    for e in source["entries"]:
        if e["sha1"] != sha1(e["en"]):
            print("entry sha1 out of date:", e["id"])
            ok = False
    for name, meta in source["batches"].items():
        entries = [e for e in source["entries"] if e["batch"] == name]
        digest = batch_digest(entries)
        batch_file = json.load(open(os.path.join(HERE, "batches", name + ".json"), encoding="utf-8"))
        state = "ok" if digest == meta["digest"] == batch_file["digest"] and len(entries) == len(batch_file["entries"]) else "CHANGED"
        ok = ok and state == "ok"
        print("%-24s %4d entries  %s  %s" % (name, len(entries), digest, state))
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
