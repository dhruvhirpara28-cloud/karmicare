"""Prove that validate.py rejects every hold/gate, span and bookkeeping defect.

Usage, from the repo root:  python3 docs/localization/nl/validate_selftest.py
Copies en-source.json and the NL batch files into a temporary folder once per case, plants one defect, and runs
validate.py --source/--nl-dir on the copy. Expected: the unchanged control exits 0; every other case exits 1 and reports
its own check. Counts and fit_risk are recomputed after each defect (except in the counts case), so a case fails on its
own check, not on bookkeeping. The self-test exits 1 if any outcome differs."""
import glob
import json
import os
import shutil
import subprocess
import sys
import tempfile
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "..", "..", "source-copy", "en-source.json")
PRIORITY = ["legal-review", "pending-claim-review", "admin", "theme-key"]


def first(src, nl, test):
    """The first (source entry, NL entry) pair that passes test."""
    for e in src["entries"]:
        r = nl.get(e["id"])
        if r and test(e, r):
            return e, r
    raise LookupError("no entry for this case")


def unhold(r, nl_text, flags):
    r["nl"], r["flags"], r["notes"] = nl_text, flags, "planted"
    r["status"] = next((p for p in PRIORITY if p in flags), "translated")


def drop_flag(r, flag):
    r["flags"] = [f for f in r["flags"] if f != flag]
    r["status"] = next((p for p in PRIORITY if p in r["flags"]), "translated")


def h1(src, nl):
    e, r = first(src, nl, lambda e, r: e.get("claim_status") == "unsupported")
    unhold(r, "X", [])


def h2(src, nl):
    e, r = first(src, nl, lambda e, r: e.get("claim_status") == "needs-review" and r["status"] == "pending-claim-review")
    drop_flag(r, "pending-claim-review")


def h3(src, nl):
    e, r = first(src, nl, lambda e, r: e.get("legal") and r["status"] == "legal-review")
    drop_flag(r, "legal-review")


def h4(src, nl):
    e, r = first(src, nl, lambda e, r: e.get("legacy"))
    unhold(r, "X", ["legal-review"])


def h5(src, nl):
    e, r = first(src, nl, lambda e, r: e.get("never_translate"))
    unhold(r, e["en"], [])


def h6(src, nl):
    e, r = first(src, nl, lambda e, r: e.get("blocked"))
    unhold(r, "X", [])


def h7(src, nl):
    e, r = first(src, nl, lambda e, r: r["status"] == "held")
    r["notes"] = ""


def s1(src, nl):
    e, r = first(src, nl, lambda e, r: r["status"] != "held" and "8000 Bruges" in (r["nl"] or ""))
    r["nl"] = r["nl"].replace("8000 Bruges", "8000 Brugge", 1)


def s2(src, nl):
    e, r = first(src, nl, lambda e, r: r["status"] != "held" and "(*)" in (r["nl"] or ""))
    r["nl"] = r["nl"].replace("(*)", "(*) (*)", 1)


def new_gate(src, nl):
    """The source gains a gate that the payload does not follow yet."""
    e, r = first(src, nl, lambda e, r: r["status"] == "translated" and not e.get("claim_status"))
    e["claim_status"] = "unsupported"


def status(src, nl):
    e, r = first(src, nl, lambda e, r: r["status"] == "legal-review")
    r["status"] = "admin"


def stale(src, nl):
    e, r = first(src, nl, lambda e, r: r["status"] == "translated")
    r["en"] = r["en"] + " "


def counts(src, nl):
    pass  # the case below edits the counts after the recompute


CASES = [
    ("control: unchanged copy", None, 0, None),
    ("H1 unsupported claim translated", h1, 1, "H1 "),
    ("H2 needs-review claim without the flag", h2, 1, "H2 "),
    ("H3 legal entry without legal-review", h3, 1, "H3 "),
    ("H4 legacy legal page translated", h4, 1, "H4 "),
    ("H5 never-translate entry translated", h5, 1, "H5 "),
    ("H6 blocked entry translated", h6, 1, "H6 "),
    ("H7 held entry without a reason", h7, 1, "H7 "),
    ("S1 address in Dutch form", s1, 1, "S1 "),
    ("S2 extra (*) marker", s2, 1, "S2 "),
    ("new unsupported gate in the source", new_gate, 1, "H1 "),
    ("status weaker than its flags", status, 1, "status admin, its flags make it legal-review"),
    ("stale EN in the payload", stale, 1, "stale entry"),
    ("counts edited", counts, 1, "counts do not match"),
]


def run(base, i, mutate, label):
    d = os.path.join(base, str(i))
    os.makedirs(os.path.join(d, "nl"))
    src = json.load(open(SOURCE, encoding="utf-8"))
    docs = {os.path.basename(p): json.load(open(p, encoding="utf-8")) for p in glob.glob(os.path.join(HERE, "batch-*.json"))}
    nl = {r["id"]: r for doc in docs.values() for r in doc["entries"]}
    if mutate:
        mutate(src, nl)
    for name, doc in docs.items():
        doc["counts"] = dict(Counter(r["status"] for r in doc["entries"]))
        doc["fit_risk"] = [r["id"] for r in doc["entries"] if "fit-risk" in r["flags"]]
        if mutate is counts and name.startswith("batch-01"):
            doc["counts"]["translated"] += 1
        json.dump(doc, open(os.path.join(d, "nl", name), "w", encoding="utf-8"), ensure_ascii=False)
    json.dump(src, open(os.path.join(d, "en-source.json"), "w", encoding="utf-8"), ensure_ascii=False)
    return subprocess.run([sys.executable, os.path.join(HERE, "validate.py"), "--source", os.path.join(d, "en-source.json"),
                           "--nl-dir", os.path.join(d, "nl")], capture_output=True, text=True)


def main():
    ok = True
    with tempfile.TemporaryDirectory() as base:
        for i, (label, mutate, expected, code) in enumerate(CASES):
            r = run(base, i, mutate, label)
            errors = [line for line in r.stdout.splitlines() if line.startswith("ERROR")]
            passed = r.returncode == expected and (code is None or any(code in line for line in errors))
            ok = ok and passed
            print("%-42s exit %d (expected %d)  %s" % (label, r.returncode, expected, "pass" if passed else "FAIL"))
            for line in errors:
                print("    " + line[:200])
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
