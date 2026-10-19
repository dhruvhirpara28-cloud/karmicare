"""Prove that digest.py rejects corrupt batch files.

Usage, from the repo root:  python3 docs/source-copy/digest_selftest.py
Copies en-source.json and batches/ into a temporary folder four times, plants one defect per copy, and runs
digest.py --dir on each. Expected: the unchanged control exits 0; the altered EN value, the substituted id and
the metadata-only change each exit 1. The self-test exits 1 if any outcome differs."""
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))


def make_copy(base, name, batch=None, change=None):
    d = os.path.join(base, name)
    os.makedirs(os.path.join(d, "batches"))
    shutil.copy(os.path.join(HERE, "en-source.json"), d)
    for f in os.listdir(os.path.join(HERE, "batches")):
        shutil.copy(os.path.join(HERE, "batches", f), os.path.join(d, "batches"))
    if batch:
        path = os.path.join(d, "batches", batch + ".json")
        doc = json.load(open(path, encoding="utf-8"))
        doc["entries"][0].update(change)
        json.dump(doc, open(path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    return d


def main():
    cases = [
        ("control: unchanged copy", None, None, 0),
        ("altered EN value, sha1/count/digest unchanged", "batch-01-homepage", {"en": "SENTINEL"}, 1),
        ("substituted id at unchanged count", "batch-01-homepage", {"id": "index:SUBSTITUTED/id"}, 1),
        ("metadata-only change (status)", "batch-02-pdp", {"status": "needs-key"}, 1),
    ]
    ok = True
    with tempfile.TemporaryDirectory() as base:
        for i, (label, batch, change, expected) in enumerate(cases):
            d = make_copy(base, str(i), batch, change)
            r = subprocess.run([sys.executable, os.path.join(HERE, "digest.py"), "--dir", d], capture_output=True, text=True)
            errors = [line for line in r.stdout.splitlines() if line.startswith("ERROR")]
            passed = r.returncode == expected
            ok = ok and passed
            print("%-50s exit %d (expected %d)  %s" % (label, r.returncode, expected, "pass" if passed else "FAIL"))
            for line in errors:
                print("    " + line)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
