#!/usr/bin/env python3
"""Offline self-test for register.py: a fake Admin API, a small plan, no network and no Keychain.

Run from the repo root:  python3 docs/localization/registration/register_selftest.py

Each case runs register.main against the fake store in a temporary folder and checks the result:
matching on the EN sha1 and the theme hints, overwrite and same, stale EN, selling plans skipped, held
items left out, split bodies assembled, JSON segments replaced as whole strings, never-translate keys
listed for removal, the checksum gate on write, removals only with --remove-never, and that neither the
client secret nor the token appears in any output or file.
"""
import contextlib
import hashlib
import io
import json
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import register  # noqa: E402

SECRET = "shpss_SELFTEST_SECRET_42"
TOKEN = "shpat_SELFTEST_TOKEN_42"


def sha1(text):
    return hashlib.sha1(text.encode("utf-8")).hexdigest()


def content(key, value, kind="STRING"):
    return {"key": key, "value": value, "digest": "d-" + sha1(value)[:8], "locale": "en", "type": kind}


METAFIELD_JSON = json.dumps({"type": "root", "children": [{"type": "text", "value": "What you'll feel"},
                                                        {"type": "text", "value": "Freedom"},
                                                        {"type": "text", "value": "Free"}]})
STORE = {
    "ONLINE_STORE_THEME_JSON_TEMPLATE": [
        {"resourceId": "gid://shopify/OnlineStoreThemeJsonTemplate/index?theme=1",
         "translatableContent": [content("section.hero.heading:aa", "Your mouth has a rhythm"),
                                 content("section.cards.card_1.title:bb", "Begin"),
                                 content("section.cards.card_2.title:cc", "Begin"),
                                 content("section.faq.question:dd", "Changed live EN")],
         "translations": {"nl": [{"key": "section.hero.heading:aa", "value": "Uw mond heeft een ritme", "outdated": False}]}},
        {"resourceId": "gid://shopify/OnlineStoreThemeJsonTemplate/product?theme=1",
         "translatableContent": [content("section.compare.handle_item:ee", "year")],
         "translations": {"nl": [{"key": "section.compare.handle_item:ee", "value": "jaar", "outdated": False}]}},
    ],
    "METAOBJECT": [
        {"resourceId": "gid://shopify/Metaobject/515475276157",
         "translatableContent": [content("title", "The Karmicare Year"), content("handle_item", "try-once")],
         "translations": {"nl": [{"key": "title", "value": "Het Karmicare-jaar", "outdated": False},
                                 {"key": "handle_item", "value": "eenmalig", "outdated": False}]}},
    ],
    "PAGE": [
        {"resourceId": "gid://shopify/Page/7",
         "translatableContent": [content("handle", "manifesto"), content("body_html", "<p>First block.</p><p>Second block.</p>", "HTML")],
         "translations": {}},
    ],
    "PRODUCT": [
        {"resourceId": "gid://shopify/Product/1",
         "translatableContent": [content("handle", "duo"), content("title", "Awake & Asleep")],
         "translations": {}},
    ],
}
BY_ID = {"gid://shopify/Metafield/9": {"resourceId": "gid://shopify/Metafield/9",
                                       "translatableContent": [content("value", METAFIELD_JSON, "JSON")], "translations": {}},
         "gid://shopify/SellingPlan/5": {"resourceId": "gid://shopify/SellingPlan/5",
                                         "translatableContent": [content("name", "Year")], "translations": {}}}
PRODUCT_METAFIELDS = {"gid://shopify/Product/1": ["gid://shopify/Metafield/9"]}


def item(iid, en, value, kind="match", key=None, field="f", hint=None, hold=()):
    out = {"id": iid, "kind": kind, "key": key, "field": field, "en": en, "en_sha1": sha1(en), "value": value,
           "gates": [], "hold": list(hold), "how": "", "status": {"drafted": True, "registered": False}}
    if hint:
        out["hint"] = hint
    return out


PLAN = {"lang": "nl", "resources": [
    {"shopify_type": "ONLINE_STORE_THEME_JSON_TEMPLATE", "owner": "templates/index.json", "items": [
        item("index:hero/heading", "Your mouth has a rhythm", "Je mond heeft een ritme"),
        item("index:cards/card_2/title", "Begin", "Begin nu", hint=["cards", "card_2", "title"]),
        item("index:faq/question", "Old EN at capture", "Oude NL"),
        item("index:held", "Begin", "Begin", hold=["pending-claim-review"]),
    ]},
    {"shopify_type": "SELLING_PLAN", "owner": "gid://shopify/SellingPlan/5", "items": [
        item("admin:selling_plan.5.name", "Year", "Jaar", kind="direct", key="name")]},
    {"shopify_type": "PAGE", "owner": "manifesto", "items": [
        item("admin:page:manifesto:body_html#b001", "<p>First block.</p>", "<p>Eerste blok.</p>", kind="assemble", key="body", field="body_html#b001"),
        item("admin:page:manifesto:body_html#b002", "<p>Second block.</p>", "<p>Tweede blok.</p>", kind="assemble", key="body", field="body_html#b002")]},
    {"shopify_type": "METAFIELD", "owner": "duo", "items": [
        item("admin:duo:custom.journey#01", "What you'll feel", "Wat je voelt"),
        item("admin:duo:custom.journey#02", "Free", "Gratis")]},
    {"shopify_type": "METAOBJECT", "owner": "duo", "items": [
        item("admin:duo:custom.compare_plans#01", "The Karmicare Year", "Het Karmicare-jaar")]},
    {"shopify_type": "PRODUCT", "owner": "duo", "items": [
        item("admin:duo:title", "Awake & Asleep", "Awake & Asleep", kind="direct", key="title")]},
]}


class FakeTransport:
    def __init__(self):
        self.mutations = []

    def post(self, path, body, headers):
        if path == "/admin/oauth/access_token":
            ok = body.get("client_secret") == SECRET and body.get("grant_type") == "client_credentials"
            return (200, {"access_token": TOKEN, "scope": "read_translations,write_translations,read_products"}) if ok else (401, {})
        assert headers.get("X-Shopify-Access-Token") == TOKEN
        q, v = body["query"], body["variables"]
        locale = v.get("locale")

        def view(node):
            return dict(node, translations=node["translations"].get(locale, []) if isinstance(node["translations"], dict) else [])

        page = {"hasNextPage": False, "endCursor": None}
        if "translationsRegister" in q:
            self.mutations.append(("register", v["id"], v["translations"]))
            return 200, {"data": {"translationsRegister": {"translations": [{"key": t["key"], "locale": t["locale"], "value": t["value"]}
                                                                            for t in v["translations"]], "userErrors": []}}}
        if "translationsRemove" in q:
            self.mutations.append(("remove", v["id"], v["keys"]))
            return 200, {"data": {"translationsRemove": {"translations": [], "userErrors": []}}}
        if "translatableResourcesByIds" in q:
            nodes = [view(BY_ID[i]) for i in v["ids"] if i in BY_ID]
            return 200, {"data": {"translatableResourcesByIds": {"nodes": nodes, "pageInfo": page}}}
        if "translatableResources" in q:
            nodes = [view(n) for n in STORE.get(v["type"], [])]
            return 200, {"data": {"translatableResources": {"nodes": nodes, "pageInfo": page}}}
        if "metafields" in q:
            nodes = [{"id": i, "namespace": "custom", "key": "journey"} for i in PRODUCT_METAFIELDS.get(v["id"], [])]
            return 200, {"data": {"product": {"metafields": {"nodes": nodes, "pageInfo": page}}}}
        raise AssertionError("unexpected query")


def run(argv, transport, folder):
    out, err = io.StringIO(), io.StringIO()
    code = 0
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        try:
            register.main(argv, transport=transport, credentials=lambda: ("client-id", register.Secret(SECRET)),
                          out=folder, plans=os.path.join(folder, "plan-%s.json"))
        except SystemExit as e:
            code = e.code if isinstance(e.code, int) else 1
            err.write(str(e.code))
    return code, out.getvalue() + err.getvalue()


def main():
    failures = []

    def check(name, ok, detail=""):
        print("%-60s %s%s" % (name, "pass" if ok else "FAIL", "" if ok else "  " + detail))
        if not ok:
            failures.append(name)

    with tempfile.TemporaryDirectory() as folder:
        with open(os.path.join(folder, "plan-nl.json"), "w", encoding="utf-8") as f:
            json.dump(PLAN, f)
        fake = FakeTransport()
        code, text = run(["--lang", "nl"], fake, folder)
        check("dry run exits 0", code == 0, text)
        check("dry run sends no mutation", not fake.mutations, str(fake.mutations))
        dry = json.load(open(os.path.join(folder, "dry-run-nl.json"), encoding="utf-8"))
        rows = {r["id"]: r for r in dry["rows"]}
        ops = {(o["op"], o["resource"], o["key"]): o for o in dry["ops"]}
        idx = "gid://shopify/OnlineStoreThemeJsonTemplate/index?theme=1"
        check("machine NL is overwritten, with the old NL shown",
              rows["index:hero/heading"]["result"] == "overwrite" and rows["index:hero/heading"]["before"] == "Uw mond heeft een ritme")
        check("hint picks card_2 among two equal EN values",
              rows["index:cards/card_2/title"]["key"] == "section.cards.card_2.title:cc" and ("register", idx, "section.cards.card_1.title:bb") not in ops)
        check("changed live EN is stale and not written",
              rows["index:faq/question"]["result"] == "stale" and ("register", idx, "section.faq.question:dd") not in ops)
        check("held item is not in the run", "index:held" not in rows)
        check("selling plan is skipped (Loop)", rows["admin:selling_plan.5.name"]["result"] == "skipped"
              and not any(o["resource"] == "gid://shopify/SellingPlan/5" for o in dry["ops"]))
        page = ops.get(("register", "gid://shopify/Page/7", "body_html"))
        check("split body assembled in order", page is not None and page["value"] == "<p>Eerste blok.</p><p>Tweede blok.</p>", str(page))
        meta = ops.get(("register", "gid://shopify/Metafield/9", "value"))
        meta_value = json.loads(meta["value"]) if meta else None
        check("two JSON segments in one metafield, whole strings only", meta_value is not None and
              [c["value"] for c in meta_value["children"]] == ["Wat je voelt", "Freedom", "Gratis"], str(meta))
        check("translation equal to the plan counts as same", rows["admin:duo:custom.compare_plans#01"]["result"] == "same"
              and ("register", "gid://shopify/Metaobject/515475276157", "title") not in ops)
        check("translated handle_item listed for removal (metaobject and theme)",
              ("remove", "gid://shopify/Metaobject/515475276157", "handle_item") in ops
              and ("remove", "gid://shopify/OnlineStoreThemeJsonTemplate/product?theme=1", "section.compare.handle_item:ee") in ops)
        check("register ops carry the live digest", page is not None and page["digest"] == "d-" + sha1("<p>First block.</p><p>Second block.</p>")[:8])
        report = open(os.path.join(folder, "dry-run-nl.md"), encoding="utf-8").read()
        check("report names the checksum and the write command", dry["checksum"] in report and "--approve " + dry["checksum"] in report)

        fake = FakeTransport()
        code, text = run(["--lang", "nl", "--write", "--approve", "0000000000000000"], fake, folder)
        check("write with another checksum stops and writes nothing", code != 0 and not fake.mutations, text)
        code, text = run(["--lang", "both", "--write", "--approve", dry["checksum"]], fake, folder)
        check("write refuses --lang both", code != 0 and not fake.mutations, text)

        fake = FakeTransport()
        code, text = run(["--lang", "nl", "--write", "--approve", dry["checksum"]], fake, folder)
        regs = [m for m in fake.mutations if m[0] == "register"]
        check("write registers every register op", code == 0 and sum(len(m[2]) for m in regs) == sum(o["op"] == "register" for o in dry["ops"]), text)
        check("write sends locale and digest", all(t["locale"] == "nl" and t["translatableContentDigest"].startswith("d-") for m in regs for t in m[2]))
        check("no removal without --remove-never", not any(m[0] == "remove" for m in fake.mutations))

        fake = FakeTransport()
        code, text = run(["--lang", "nl", "--write", "--approve", dry["checksum"], "--remove-never"], fake, folder)
        removes = sorted((m[1], tuple(m[2])) for m in fake.mutations if m[0] == "remove")
        check("--remove-never removes the listed keys", code == 0 and len(removes) == 2, str(removes))

        leaked = [name for name in os.listdir(folder) if SECRET in open(os.path.join(folder, name), encoding="utf-8").read()
                  or TOKEN in open(os.path.join(folder, name), encoding="utf-8").read()]
        check("no secret or token in any file", not leaked, str(leaked))
        check("no secret or token in the output", SECRET not in text and TOKEN not in text)
        check("Secret hides its value in repr and str", SECRET not in repr(register.Secret(SECRET)) + str(register.Secret(SECRET)))

    print("%d failures" % len(failures))
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
