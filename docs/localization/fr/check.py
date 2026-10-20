"""Check the FR translation payloads against the EN source.

Usage, from the repo root:
  python3 docs/localization/fr/check.py              validate the committed FR files
  python3 docs/localization/fr/check.py --self-test  also prove that known-bad payloads fail (in memory only)

Errors (exit code 1):
- source: a batch missing or extra, a batch digest or an entry sha1 that no longer matches the EN source,
  a missing or extra entry, an entry whose resource_type, file_or_handle, key_path or source_status
  differs from its source entry;
- gates the source requires: a hold (never-translate, [NEEDS APPROVED COPY], unsupported claim in
  CLAIMS-REVIEW.md or in the 05-07 claim_status, legacy page), pending-claim-review on a translated
  needs-review claim (claims table for 01-03, claim_status for 05-07), legal-review on every legal entry
  (source `legal` flag, and every batch-04 entry outside the contact page);
- delivery: a status outside the vocabulary or not matching the source channel (admin-held -> admin,
  needs-key -> theme-key, Dawn key -> locale-present with the value from locales/fr.json), counts or
  flag_counts that do not match the entries;
- FR text: markup, Liquid, [tokens] or runtime price spans that differ from the EN, changed selling-plan
  IDs, French typography slips (plain or missing space before : ; ! ? € % », straight apostrophes,
  €-before-amount), a postal address of the EN missing from the FR (S1) or a different number of (*)
  markers (S2), the NL validator's invariants from CHANGES-R2 §6;
- brand words in ordinary copy (translated, not legal text, not a Dawn key), CHANGES-R2 "R6 additions" W1: no
  commodity word, inside a word included: produit(s) (sous-produit), tube, utilis-, emploi/employ-, (r)achat/(r)achet-.
  Not matched: produire/produisent/production, YouTube, sachet. Official names and the verb produire are listed in
  WORD_EXCEPTIONS with their reason. "dentifrice" is not checked here: it is allowed at first contact (titles, SEO,
  alt texts, opening questions, the first mention), which a pattern cannot see; REPORT.md records the manual pass.
Warnings: forbidden claim verbs and tu-forms outside legal text, for a human."""
import copy
import glob
import hashlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "..", "..", "source-copy")
LOCALE = os.path.join(HERE, "..", "..", "..", "locales", "fr.json")

STATUSES = {"translated", "admin", "theme-key", "locale-present", "held"}
FLAGS = {"pending-claim-review", "pending-en-review", "fit-risk", "source-defect", "legal-review",
         "gendered-title", "wording-adapted", "not-rendered"}
LEGAL_BATCH = "batch-04-legal"
LEGAL_EXEMPT_PAGES = {"/pages/contact", "templates/page.contact.json"}
DYNAMIC = re.compile(r'<span class="(?:kc-dynamic_price|dynamic_free_welcome_price)">[^<]*</span>')
SKIP = re.compile(r"(<[^>]*>|\{\{.*?\}\}|\{%.*?%\}|&[a-zA-Z#0-9]+;|\[[a-z_]+\])", re.S)
COMMODITY = re.compile(r"[\w-]*(?:produits?\b|(?<!you)tubes?\b|utilis|emploi|employ)[\w-]*|\br?ach[ae]t\w*", re.I)
# Official names and verbs that keep a commodity stem on purpose: (entry id or "*", word) -> reason.
WORD_EXCEPTIONS = {
    ("admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#60", "produits"): "official name: portail européen des produits cosmétiques (CPNP), as NL",
    ("admin:article:news/nano-hydroxyapatite:body_html#b101", "produits"): "verb produire: 'the harmful acids produced by bad bacteria'",
    ("admin:article:news/benefits-of-nootropics-ease-stress-boost-focus-and-improve-mood:body_html#b054", "produit"): "verb produire: 'It produces fruits' (the guarana plant)",
    ("admin:article:news/5-reasons-you-should-avoid-fluoride-in-toothpaste:body_html#b049", "produit"): "verb produire: 'It produces the thyroid hormones' (the gland)",
}
FORBIDDEN = re.compile(r"\b(prévien\w*|préven\w*|prévenir|guéri\w*|traite|traiter|traitent)\b", re.I)
TU = re.compile(r"\b(tu|ton|ta|tes|toi)\b", re.I)
# Street and number, optional box, postcode, optional city and country: "Vizierstraat 28, 8000 Bruges, Belgium".
# The same pattern as docs/localization/nl/validate.py (S1).
ADDRESS = re.compile(r"[A-Z][^,<>·().:;]{2,60}?\d+[a-z]?(?:, (?:box|bus) \d+)?, \d{4}(?: [A-Z][a-zé]+)?(?:, [A-Z][a-z]+)?")


def sha1(text):
    return hashlib.sha1(text.encode("utf-8")).hexdigest()


def text_nodes(value):
    value = DYNAMIC.sub(" ", value)
    return [p for p in SKIP.split(value) if p and not SKIP.fullmatch(p)]


def plain(value):
    return " ".join(re.sub(r"<[^>]+>", " ", value or "").replace(" ", " ").replace(" ", " ").split())


def structure(value):
    return (re.findall(r"<[^>]*>", value), sorted(re.findall(r"\{\{.*?\}\}|\{%.*?%\}", value)),
            sorted(re.findall(r"\[[a-z_]+\]", value)), DYNAMIC.findall(value), value.count("&nbsp;"))


def typography(value, key_path):
    problems = []
    for node in text_nodes(value):
        if re.search(r" [:;!?€%»]", node):
            problems.append("plain space before : ; ! ? € % or »")
        if re.search(r"[^\s  \d;!?][;!?»]", node):
            problems.append("no space before ; ! ? or »")
        if re.search(r"[A-Za-zÀ-ÿ)][:](?!//)", node) and not key_path.endswith("custom_button_text_by_plan"):
            problems.append("no space before :")
        if "«" in node or "»" in node:
            problems.append("guillemets: use the quotes of the EN source (Victor, 20 Oct)")
        if "'" in node:
            problems.append("straight apostrophe")
        if re.search(r"€\s?\d", node):
            problems.append("€ before the amount")
        if re.search(r"\d €|\d€", node):
            problems.append("amount and € not joined by U+00A0")
    return problems


def lookup(tree, key):
    for part in key.split("."):
        if not isinstance(tree, dict) or part not in tree:
            return None
        tree = tree[part]
    return tree


def load_sources():
    source = json.load(open(os.path.join(SOURCE, "en-source.json"), encoding="utf-8"))
    batches = {}
    for name in source["batches"]:
        batches[name] = json.load(open(os.path.join(SOURCE, "batches", name + ".json"), encoding="utf-8"))
    claims = {}
    for line in open(os.path.join(SOURCE, "CLAIMS-REVIEW.md"), encoding="utf-8"):
        m = re.match(r"\| (C\d+) \|.*\| \*\*(approved|needs-review|unsupported)\*\* \|", line)
        if m:
            claims[m.group(1)] = m.group(2)
    text = open(LOCALE, encoding="utf-8").read()
    locale = json.loads(re.sub(r"^\s*/\*.*?\*/", "", text, flags=re.S))
    return {"source": source, "batches": batches, "claims": claims, "locale": locale}


def load_fr():
    docs = {}
    for path in sorted(glob.glob(os.path.join(HERE, "batch-*.json"))):
        doc = json.load(open(path, encoding="utf-8"))
        docs[doc["batch"]] = doc
    return docs


def required_holds(s, claims):
    reasons = []
    if s["never_translate"]:
        reasons.append("never-translate")
    if s.get("blocked") or "[NEEDS APPROVED COPY]" in s["en"]:
        reasons.append("needs-approved-copy")
    if any(claims.get(c) == "unsupported" for c in s.get("claims") or []):
        reasons.append("unsupported claim (CLAIMS-REVIEW.md)")
    if s.get("claim_status") == "unsupported":
        reasons.append("unsupported claim (claims review 05-07)")
    if s.get("legacy"):
        reasons.append("legacy page")
    return reasons


def needs_claim_gate(s, claims):
    return any(claims.get(c) == "needs-review" for c in s.get("claims") or []) or s.get("claim_status") == "needs-review"


def needs_legal_gate(s, batch):
    return bool(s.get("legal")) or (batch == LEGAL_BATCH and s.get("page") not in LEGAL_EXEMPT_PAGES)


def expected_channel(s):
    if s["id"].startswith("locale:"):
        return "locale-present"
    return {"admin-held": "admin", "needs-key": "theme-key"}.get(s["status"], "translated")


def validate(docs, ctx):
    errors, warnings = [], []
    source, batches, claims = ctx["source"], ctx["batches"], ctx["claims"]
    for name in source["batches"]:
        if name not in docs:
            errors.append("%s: FR batch file missing" % name)
    for name in docs:
        if name not in source["batches"]:
            errors.append("%s: FR batch has no EN source batch" % name)
    for name in sorted(docs):
        if name not in batches:
            continue
        doc, src = docs[name], batches[name]
        digest = sha1("\n".join(sorted(sha1(e["en"]) for e in src["entries"])))
        if not (doc["source_digest"] == src["digest"] == digest == source["batches"][name]["digest"]):
            errors.append("%s: source digest changed (FR built from %s, EN now %s)" % (name, doc["source_digest"], digest))
        src_ids = [e["id"] for e in src["entries"]]
        fr_ids = [e["id"] for e in doc["entries"]]
        if src_ids != fr_ids:
            errors.append("%s: entry ids differ from the source batch (missing %d, extra %d)" % (
                name, len(set(src_ids) - set(fr_ids)), len(set(fr_ids) - set(src_ids))))
        by_id = {e["id"]: e for e in src["entries"]}
        counts, flag_counts = {}, {}
        for e in doc["entries"]:
            where = "%s %s" % (name, e["id"])
            s = by_id.get(e["id"])
            if s is None:
                continue
            if e["en"] != s["en"] or e["en_sha1"] != s["sha1"] or e["en_sha1"] != sha1(e["en"]):
                errors.append(where + ": EN text or en_sha1 out of date")
            for field in ("resource_type", "file_or_handle", "key_path"):
                if e.get(field) != s.get(field):
                    errors.append("%s: %s %r differs from the source %r" % (where, field, e.get(field), s.get(field)))
            if e.get("source_status") != s["status"]:
                errors.append(where + ": source_status differs from the source status")
            if e["status"] not in STATUSES:
                errors.append(where + ": unknown status " + str(e["status"]))
            for f in e["flags"]:
                if f not in FLAGS:
                    errors.append(where + ": unknown flag " + f)
            if len(set(e["flags"])) != len(e["flags"]):
                errors.append(where + ": duplicated flag")
            counts[e["status"]] = counts.get(e["status"], 0) + 1
            for f in e["flags"]:
                flag_counts[f] = flag_counts.get(f, 0) + 1
            if needs_legal_gate(s, name) and "legal-review" not in e["flags"]:
                errors.append(where + ": legal entry without legal-review")
            holds = required_holds(s, claims)
            if e["status"] == "held":
                if e["fr"] is not None or not e["notes"]:
                    errors.append(where + ": held entries carry fr = null and a reason in notes")
                continue
            if holds:
                errors.append(where + ": the source requires a hold (" + ", ".join(holds) + ")")
            if e["status"] != expected_channel(s):
                errors.append("%s: status %s, the source channel is %s" % (where, e["status"], expected_channel(s)))
            if needs_claim_gate(s, claims) and "pending-claim-review" not in e["flags"]:
                errors.append(where + ": needs-review claim translated without pending-claim-review")
            if not e["fr"]:
                errors.append(where + ": empty FR")
                continue
            if e["status"] == "locale-present":
                if e["fr"] != lookup(ctx["locale"], e["id"][len("locale:"):]):
                    errors.append(where + ": locale-present value differs from locales/fr.json")
                continue
            if structure(e["en"]) != structure(e["fr"]):
                errors.append(where + ": markup, Liquid, [tokens] or runtime spans differ from the EN")
            for address in ADDRESS.findall(plain(e["en"])):
                if address not in plain(e["fr"]):
                    errors.append(where + ": S1 address not exactly as in the EN: " + address)
            if e["en"].count("(*)") != e["fr"].count("(*)"):
                errors.append("%s: S2 (*) markers %d in EN, %d in FR" % (where, e["en"].count("(*)"), e["fr"].count("(*)")))
            if e["key_path"].endswith("custom_button_text_by_plan"):
                if re.findall(r"^(\d+): ", e["en"], re.M) != re.findall(r"^(\d+): ", e["fr"], re.M):
                    errors.append(where + ": selling-plan IDs changed")
            for p in typography(e["fr"], e["key_path"]):
                errors.append(where + ": " + p)
            nodes = " ".join(text_nodes(e["fr"]))
            # Legal text is translated faithfully and completely (BRIEF), so the brand-word and claim-verb scans
            # skip it: there "produits", "utilisation" or "traiter (des données)" are the legal wording.
            if "legal-review" not in e["flags"]:
                for m in COMMODITY.finditer(nodes):
                    word = m.group(0).lower()
                    if ("*", word) not in WORD_EXCEPTIONS and (e["id"], word) not in WORD_EXCEPTIONS:
                        errors.append(where + ": W1 commodity word in ordinary copy: '" + m.group(0) + "'")
                for m in FORBIDDEN.findall(nodes):
                    warnings.append(where + ": claim-verb check: '" + m + "'")
            for m in TU.findall(nodes):
                warnings.append(where + ": tu-form check: '" + m + "'")
        if counts != doc["counts"]:
            errors.append(name + ": counts block does not match the entries")
        if flag_counts != doc["flag_counts"]:
            errors.append(name + ": flag_counts block does not match the entries")
    return errors, warnings


def find(docs, entry_id):
    for doc in docs.values():
        for e in doc["entries"]:
            if e["id"] == entry_id:
                return doc, e
    raise KeyError(entry_id)


def recount(doc):
    doc["counts"], doc["flag_counts"] = {}, {}
    for e in doc["entries"]:
        doc["counts"][e["status"]] = doc["counts"].get(e["status"], 0) + 1
        for f in e["flags"]:
            doc["flag_counts"][f] = doc["flag_counts"].get(f, 0) + 1
    doc["counts"] = dict(sorted(doc["counts"].items()))
    doc["flag_counts"] = dict(sorted(doc["flag_counts"].items()))


def self_test(docs, ctx):
    """Each mutation is applied to an in-memory copy; validate() must report the expected error."""
    def drop_flag(entry_id, flag):
        def run(d):
            doc, e = find(d, entry_id)
            e["flags"].remove(flag)
            recount(doc)
        return run

    def release_held(entry_id, fr, status):
        def run(d):
            doc, e = find(d, entry_id)
            e["status"], e["fr"] = status, fr
            recount(doc)
        return run

    def set_field(entry_id, field, value):
        def run(d):
            find(d, entry_id)[1][field] = value
        return run

    def remove_batch(name):
        def run(d):
            del d[name]
        return run

    def replace_fr(entry_id, old, new):
        def run(d):
            e = find(d, entry_id)[1]
            e["fr"] = e["fr"].replace(old, new, 1)
        return run

    def tamper_flag_counts(name):
        def run(d):
            d[name]["flag_counts"]["legal-review"] = d[name]["flag_counts"].get("legal-review", 0) - 1
        return run

    legacy = next(e["id"] for e in docs[LEGAL_BATCH]["entries"] if e["status"] == "held" and e["notes"].startswith("legacy"))
    unsupported = next(e["id"] for e in docs["batch-07-collections-blog"]["entries"]
                       if e["status"] == "held" and e["notes"].startswith("unsupported-claim"))
    SLS = "admin:article:news/3-reasons-why-you-should-look-for-an-sls-free-toothpaste:"
    cases = [
        ("remove pending-claim-review (Astra F6)", drop_flag("product.subscription-item:main/highlights_slider_9wAjAb/text_1", "pending-claim-review"), "without pending-claim-review"),
        ("remove legal-review (Astra F6)", drop_flag("page.consumer-rights:policy_banner_Pgpxip/heading", "legal-review"), "without legal-review"),
        ("translate a never-translate entry (Astra F6)", release_held("index:hero_karmicare_XKKLDK/rhythm_toggle_ffWVXt/awake_label", "AWAKE", "translated"), "requires a hold (never-translate"),
        ("change file_or_handle (Astra F6)", set_field("product.subscription-item:main/highlights_slider_9wAjAb/text_1", "file_or_handle", "templates/index.json"), "file_or_handle"),
        ("remove legal-review from a held legacy SEO field (Astra F5)", drop_flag("admin:page:privacy:seo.title", "legal-review"), "without legal-review"),
        ("translate a legacy legal entry", release_held(legacy, "Texte", "admin"), "requires a hold (legacy"),
        ("translate an unsupported 05-07 claim", release_held(unsupported, "Texte", "admin"), "requires a hold (unsupported claim"),
        ("translate a [NEEDS APPROVED COPY] placeholder", release_held("index:km_faq_accordion_FYcArV/faq_item_kLMHax/answer", "<p>Texte</p>", "translated"), "requires a hold (needs-approved-copy"),
        ("wrong delivery channel", set_field("admin:karmicare-biorhythmic-oral-care-system:title", "status", "translated"), "source channel"),
        ("change key_path", set_field("footer-group:footer/slogan", "key_path", "sections.footer.settings.other"), "key_path"),
        ("flag_counts out of step", tamper_flag_counts(LEGAL_BATCH), "flag_counts"),
        ("remove a batch file", remove_batch("batch-08-system"), "FR batch file missing"),
        ("translate an address (R2 F8)", replace_fr("admin:policy:refund-policy:body#b103", "1000 Brussels, Belgium", "1000 Bruxelles, Belgique"), "S1 address"),
        ("drop a (*) marker (R2 F9)", replace_fr("admin:policy:refund-policy:body#b114", " (*)", ""), "S2 (*) markers"),
        ("commodity compound in blog copy (R6-02)", replace_fr(SLS + "body_html#b015", "nettoyants ménagers", "produits ménagers"), "W1 commodity"),
        ("product stem inside a word (R6 W1)", replace_fr("admin:article:news/nano-hydroxyapatite:body_html#b094", "au passage des acides qui", "des acides comme sous-produit, ce qui"), "W1 commodity"),
    ]
    failures = 0
    for label, mutate, expected in cases:
        mutated = copy.deepcopy(docs)
        mutate(mutated)
        errors, _ = validate(mutated, ctx)
        caught = [e for e in errors if expected in e]
        print("self-test %-62s %s (%d errors)" % (label, "FAILS AS EXPECTED" if caught else "NOT CAUGHT", len(errors)))
        if not caught:
            failures += 1
    return failures


def main():
    ctx = load_sources()
    docs = load_fr()
    if not docs:
        sys.exit("no FR batch files found")
    errors, warnings = validate(docs, ctx)
    for name in sorted(docs):
        doc = docs[name]
        print("%-26s %4d entries  %s  %s" % (name, len(doc["entries"]), doc["source_digest"], json.dumps(doc["counts"], sort_keys=True)))
    for w in warnings:
        print("warning:", w)
    for e in errors:
        print("ERROR:", e)
    print("%d errors, %d warnings" % (len(errors), len(warnings)))
    failures = 0
    if "--self-test" in sys.argv[1:]:
        failures = self_test(docs, ctx)
        print("self-test: %d mutation(s) not caught" % failures)
    sys.exit(1 if errors or failures else 0)


if __name__ == "__main__":
    main()
