"""Check the NL batch files against the EN source.

Usage, from the repo root:  python3 docs/localization/nl/validate.py [--source FILE] [--nl-dir DIR]
Integrity, for every batch: the file exists, its source_digest and source_entries equal the EN batch, every EN entry is
present once, each en_sha1 equals sha1(en) and the source entry's sha1, held entries carry no Dutch, and all others do.
Bookkeeping: a status names the strongest of its flags, and counts and fit_risk match the entries.
Hold and gate invariants: the source decides, the payload follows (a hold is always stricter than a flag).
  H1  claim_status unsupported     -> held
  H2  claim_status needs-review    -> held, or flagged pending-claim-review
  H3  legal                        -> held, or flagged legal-review
  H4  legacy                       -> held
  H5  never_translate              -> held
  H6  blocked (needs approved copy) -> held
  H7  held                         -> a reason in notes
  H8  retired (the theme no longer reads it) -> held
Exact spans in translated entries:
  S1  every postal address in the EN appears unchanged in the NL
  S2  the NL has as many (*) markers as the EN
Brand words in ordinary copy (translated entries that are not legal text and not Dawn keys):
  W1  no commodity word, compounds included: product, tube, gebruik, (aan/in)koop, kopen, (ge)kocht. Not commodity words, and so
      not matched: productie/productief/productiviteit, verkoop, YouTube. Official and approved exceptions are listed
      in WORD_EXCEPTIONS with their reason. "tandpasta" is not checked here: it is allowed at first contact (titles,
      SEO, opening questions, the first mention), which depends on context a pattern cannot see; REPORT.md records
      the manual pass.
Exit code 1 on any failure, so a later EN change shows up as a stale entry here, and a new gate in the source shows up
as an entry the payload does not hold yet. `validate_selftest.py` proves each check with a planted defect."""
import argparse
import hashlib
import json
import os
import re
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "..", "..", "source-copy", "en-source.json")
PRIORITY = ["legal-review", "pending-claim-review", "admin", "theme-key"]
COMMODITY = re.compile(r"\w*(?:product(?!ie|iv)|(?<!you)tube|gebruik|\b(?:aan|in)?ko(?:op|pen)|\b(?:ge)?kocht)\w*", re.I)
# official names, legal titles and approved copy that keep a commodity word on purpose: (entry id or "*", word) -> reason
WORD_EXCEPTIONS = {
    ("*", "gebruiksvoorwaarden"): "legal document title (Terms of Use)",
    ("admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#60", "producten"): "official name: EU-portaal voor cosmetische producten (CPNP)",
    ("footer-group:footer/copyright_text", "product"): "compliance statement mirroring the EN regulatory line; copy owner decides (REPORT.md)",
    ("product.subscription-item:main/treatment_journey_block/disclaimer_text", "gebruik"): "approved Figma NL (3738:27474); conflict listed for the copy owner",
    ("product:main/treatment_journey_block/disclaimer_text", "gebruik"): "approved Figma NL (3738:27474); conflict listed for the copy owner",
}
# street and number, optional box, postcode, optional city and country: "Vizierstraat 28, 8000 Bruges, Belgium"
ADDRESS = re.compile(r"[A-Z][^,<>·().:;]{2,60}?\d+[a-z]?(?:, (?:box|bus) \d+)?, \d{4}(?: [A-Z][a-zé]+)?(?:, [A-Z][a-z]+)?")


def plain(s):
    return " ".join(re.sub(r"<[^>]+>", " ", s or "").replace("\xa0", " ").split())


def gates(e, r):
    """Hold/gate violations of one NL entry r against its source entry e."""
    held = r["status"] == "held"
    flags = r.get("flags") or []
    out = []
    if e.get("claim_status") == "unsupported" and not held:
        out.append("H1 unsupported claim not held")
    if e.get("claim_status") == "needs-review" and not held and "pending-claim-review" not in flags:
        out.append("H2 needs-review claim neither held nor pending-claim-review")
    if e.get("legal") and not held and "legal-review" not in flags:
        out.append("H3 legal entry neither held nor legal-review")
    if e.get("legacy") and not held:
        out.append("H4 legacy entry not held")
    if e.get("never_translate") and not held:
        out.append("H5 never-translate entry not held")
    if e.get("blocked") and not held:
        out.append("H6 blocked entry (needs approved copy) not held")
    if held and not (r.get("notes") or "").strip():
        out.append("H7 held entry without a reason")
    if e.get("retired") and not held:
        out.append("H8 retired entry not held")
    if not held and r["nl"]:
        en, nl = plain(r["en"]), plain(r["nl"])
        for m in ADDRESS.finditer(en):
            if m.group(0) not in nl:
                out.append("S1 address changed: " + m.group(0))
        if r["en"].count("(*)") != r["nl"].count("(*)"):
            out.append("S2 (*) markers %d in EN, %d in NL" % (r["en"].count("(*)"), r["nl"].count("(*)")))
        if ordinary(e, r):
            for word in commodity_words(r):
                out.append("W1 commodity word in ordinary copy: " + word)
    return out


def ordinary(e, r):
    """Translated customer copy that is neither legal text nor a Dawn key."""
    return (r["status"] not in ("held", "dawn-nl") and bool(r["nl"]) and not e.get("legal")
            and "legal-review" not in (r.get("flags") or []))


def commodity_words(r):
    """Commodity words in the NL text (tags and link URLs left out), minus the listed exceptions."""
    words = [m.group(0).lower() for m in COMMODITY.finditer(plain(r["nl"]))]
    return [w for w in words if ("*", w) not in WORD_EXCEPTIONS and (r["id"], w) not in WORD_EXCEPTIONS]


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--source", default=SOURCE, help="en-source.json to check against (default: the repo's)")
    parser.add_argument("--nl-dir", default=HERE, help="folder that holds the NL batch files (default: this script's folder)")
    args = parser.parse_args()
    src = json.load(open(args.source, encoding="utf-8"))
    by_batch = {}
    for e in src["entries"]:
        by_batch.setdefault(e["batch"], {})[e["id"]] = e
    errors = []
    checked = Counter()
    for batch, meta in src["batches"].items():
        path = os.path.join(args.nl_dir, batch + ".json")
        if not os.path.exists(path):
            print("%-26s missing" % batch)
            errors.append("%s: missing" % batch)
            continue
        doc = json.load(open(path, encoding="utf-8"))
        before = len(errors)
        def err(msg):
            errors.append("%s: %s" % (batch, msg))
        if doc["source_digest"] != meta["digest"]:
            err("source digest changed: re-translate the changed entries")
        if doc.get("source_entries") != meta["entries"]:
            err("source_entries %s, the EN batch has %d" % (doc.get("source_entries"), meta["entries"]))
        seen = set()
        for r in doc["entries"]:
            e = by_batch[batch].get(r["id"])
            if e is None:
                err("unknown id " + r["id"])
                continue
            if r["id"] in seen:
                err("duplicate id " + r["id"])
            seen.add(r["id"])
            if r["en_sha1"] != e["sha1"] or r["en_sha1"] != hashlib.sha1(r["en"].encode("utf-8")).hexdigest():
                err("stale entry " + r["id"])
            if r["status"] == "held" and r["nl"]:
                err("held entry has Dutch " + r["id"])
            if r["status"] != "held" and not (r["nl"] or "").strip():
                err("no Dutch " + r["id"])
            if r["status"] not in ("held", "dawn-nl"):
                want = next((p for p in PRIORITY if p in r["flags"]), "translated")
                if r["status"] != want:
                    err("status %s, its flags make it %s: %s" % (r["status"], want, r["id"]))
            for g in gates(e, r):
                err("%s: %s" % (g, r["id"]))
            for key, on in (("H1", e.get("claim_status") == "unsupported"), ("H2", e.get("claim_status") == "needs-review"),
                            ("H3", e.get("legal")), ("H4", e.get("legacy")), ("H5", e.get("never_translate")),
                            ("H6", e.get("blocked")), ("H7", r["status"] == "held"), ("H8", e.get("retired"))):
                if on:
                    checked[key] += 1
            if r["status"] != "held" and r["nl"]:
                checked["S1"] += len(ADDRESS.findall(plain(r["en"])))
                checked["S2"] += r["en"].count("(*)")
            if ordinary(e, r):
                checked["W1"] += 1
        missing = set(by_batch[batch]) - seen
        if missing:
            err("%d EN entries not covered" % len(missing))
        if doc.get("counts") != dict(Counter(r["status"] for r in doc["entries"])):
            err("counts do not match the entries")
        if doc.get("fit_risk") != [r["id"] for r in doc["entries"] if "fit-risk" in r["flags"]]:
            err("fit_risk does not match the fit-risk flags")
        n = len(errors) - before
        print("%-26s %4d entries  %s" % (batch, len(doc["entries"]), "ok" if not n else "%d errors" % n))
    print("entries under each gate: " + ", ".join("%s %d" % (k, checked[k]) for k in ("H1", "H2", "H3", "H4", "H5", "H6", "H7", "H8"))
          + "; addresses checked S1 %d, (*) markers S2 %d; ordinary-copy entries checked W1 %d (%d listed exceptions)"
          % (checked["S1"], checked["S2"], checked["W1"], len(WORD_EXCEPTIONS)))
    for e in errors:
        print("ERROR " + e)
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
