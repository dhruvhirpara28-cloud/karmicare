#!/usr/bin/env python3
"""Offline self-test for register.py: a fake Admin API, small plans, no network and no Keychain.

Run from the repo root:  python3 docs/localization/registration/register_selftest.py

The cases cover the basic flow (new, overwrite, same, stale, Loop skipped, held left out, split bodies,
metaobjects through the product's references) and one regression per R18 finding: F1 approval binds the
current translations, F2 identity before EN (failed hints, other templates, ambiguity, conflicts), F3 only
the published theme, F4 protected targets never registered, F5 JSON fields kept whole, F6 JSON values
matched as decoded strings by path, F7 no dummy secret or token in output, exceptions or files on any
error path, F8 full values and target identity in the report, F9 a journal that keeps confirmed writes,
F10 null content skipped; and per R18b finding: A a resource the re-read omits fails, B metaobject fields only
through a reviewed binding, C a numeric, proven-published theme (read or same-day attestation) with the exact
GID parameter, D held leaves veto before structural keys and structural differences are shown, N1 a null or
incomplete mutation payload is unknown, N2 scalar and array JSON roots; and per R18c finding: 1 conflicting
items on a structural leaf veto the field and a lone structural item is not counted as applied, 2 receipts
with a missing, null or wrong locale, an extra or a duplicate entry are unknown (register and remove), 3 the
generated write command round-trips through a shell and an attestation needs a name; and per R18e: the real
HttpTransport sends a form-encoded token request and JSON GraphQL, refused token requests show only a fixed line
whatever the body echoes (JSON, text, HTML, invalid UTF-8, cut; literal, percent, form, entity-encoded, split or cut
credentials, Bearer), and no sink (stdout, stderr, exception chain, reports, journal) carries response text with
credential material; and per R18f: credentials hidden in HTML attributes, comments or entity-encoded angle
brackets, or spaced and form-encoded, are withheld in message, code and field, also through a read error and the
writer's journal; and per R18g: errors show only allowlisted codes, field paths and messages (else their length), a
token behind nested entities stays out of a read error and the journal, and long unclosed markup is handled in
linear time; and per R18h: a receipt's own keys are never journaled (unrequested, duplicate, wrong locale), a
malformed GID is dropped, an HTTPError body that fails to read stays a data-free transport error, and an unexpected
exception prints its category only; and per R18i: the SystemExit carries no context; and for wave 2a: section-level settings match exact ids,
selling-plan names, descriptions and shared groups are registered while the Subscription Name values and other
selling-plan content stay protected (B-01), and an owner GID must match its type. Credentials are synthetic sentinels.
"""
import contextlib
import copy
import email.message
import hashlib
import html
import io
import json
import os
import re
import sys
import tempfile
import time
import traceback
import urllib.error
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import register  # noqa: E402

SECRET = "shpss_SELFTESTSECRET42"
TOKEN = "shpat_SELFTESTTOKEN42"
THEME = "111"
IDX = "gid://shopify/OnlineStoreThemeJsonTemplate/index?theme_id=111"
IDX_OTHER = "gid://shopify/OnlineStoreThemeJsonTemplate/index?theme_id=222"
PDP = "gid://shopify/OnlineStoreThemeJsonTemplate/product.subscription-item?theme_id=111"
LONG_NL = "Lange tekst " + "x" * 170 + " EINDE-SUFFIX"


def sha1(text):
    return hashlib.sha1(text.encode("utf-8")).hexdigest()


def c(key, value, kind="STRING"):
    return {"key": key, "value": value, "digest": None if value is None else "d-" + sha1(value)[:8], "locale": "en", "type": kind}


def tr(key, value, outdated=False):
    return {"key": key, "value": value, "outdated": outdated}


FAQ_JSON = json.dumps([{"question": "Hello", "answer": "Held claim"}])
JOURNEY_JSON = json.dumps({"type": "root", "children": [{"type": "text", "value": "What you'll feel"}, {"type": "text", "value": "Free"},
                                                        {"type": "text", "value": "€0.49"},
                                                        {"type": "link", "url": "https://karmicare.com/a", "children": [{"type": "text", "value": "Free"}]}]})
JOURNEY_NL = JOURNEY_JSON.replace("https://karmicare.com/a", "https://karmicare.com/nl/a").replace("Free", "Gratis")
FAQ_LINK_JSON = json.dumps({"title": "Hello", "link": "Held claim"})
ROOTS = {"14": json.dumps("Hello"), "15": "42", "16": "true", "17": "null", "18": json.dumps(["Hello", "Hello"])}
TRICKY_JSON = '{"Free":"Free","list":["Hello","Hallo"],"name":"caf\\u00e9","url":"https:\\/\\/x.test\\/b"}'


def base_store():
    return {
        "types": {
            "ONLINE_STORE_THEME_JSON_TEMPLATE": [
                {"resourceId": IDX, "translatableContent": [
                    c("section.hero.heading:aa", None),
                    c("section.hero.heading:ab", "Your mouth has a rhythm"),
                    c("section.cards.card_1.title:bb", "Begin"),
                    c("section.cards.card_2.title:cc", "Begin"),
                    c("section.faq.q1.question:dd", "Changed live EN"),
                    c("section.gift.g1.label:ee", "Gift, pause or cancel"),
                    c("section.gift.g2.label:ef", "Gift, pause or cancel"),
                    c("section.long.l1.text:ff", "Long EN"),
                    c("section.compare.handle_item:gg", "Year")],
                 "translations": {"nl": [tr("section.hero.heading:ab", "Uw mond heeft een ritme")]}},
                {"resourceId": IDX_OTHER, "translatableContent": [c("section.hero.heading:ab", "Your mouth has a rhythm"),
                                                                  c("section.compare.handle_item:gg", "year")],
                 "translations": {"nl": [tr("section.compare.handle_item:gg", "jaar")]}},
                {"resourceId": PDP, "translatableContent": [c("section.other.x.title:zz", "Old EN at capture"),
                                                            c("section.compare.handle_item:hh", "try-once")],
                 "translations": {"nl": [tr("section.compare.handle_item:hh", "eenmalig")]}},
            ],
            "METAOBJECT": [
                {"resourceId": "gid://shopify/Metaobject/515475276157",
                 "translatableContent": [c("title", "The Karmicare Year"), c("handle_item", "try-once")],
                 "translations": {"nl": [tr("title", "Het Karmicare-jaar"), tr("handle_item", "eenmalig")]}},
                {"resourceId": "gid://shopify/Metaobject/700",
                 "translatableContent": [c("role", "Pharmacist"), c("name", "Sietske")],
                 "translations": {}},
                {"resourceId": "gid://shopify/Metaobject/701",
                 "translatableContent": [c("role", "Pharmacist")], "translations": {}},
            ],
            "PAGE": [{"resourceId": "gid://shopify/Page/7", "translatableContent": [c("handle", "manifesto"),
                     c("body_html", "<p>First block.</p><p>Second block.</p>", "HTML")], "translations": {}}],
            "PRODUCT": [{"resourceId": "gid://shopify/Product/1", "translatableContent": [c("handle", "duo"), c("title", "Awake & Asleep")],
                         "translations": {}},
                        {"resourceId": "gid://shopify/Product/2", "translatableContent": [c("handle", "supply"), c("title", "60-Day Supply")],
                         "translations": {}}],
            "SHOP": [{"resourceId": "gid://shopify/Shop/1", "translatableContent": [c("meta_title", "KARMICARE")], "translations": {}}],
            "LINK": [{"resourceId": "gid://shopify/Link/1", "translatableContent": [c("title", "Manifesto")], "translations": {}}],
        },
        "ids": {
            "gid://shopify/Metafield/9": {"resourceId": "gid://shopify/Metafield/9", "translatableContent": [c("value", JOURNEY_JSON, "JSON")],
                                          "translations": {"nl": [tr("value", JOURNEY_NL)]}},
            "gid://shopify/Metafield/13": {"resourceId": "gid://shopify/Metafield/13", "translatableContent": [c("value", FAQ_LINK_JSON, "JSON")],
                                           "translations": {"nl": [tr("value", json.dumps({"title": "Oud", "link": "Existing approved NL"}))]}},
            **{"gid://shopify/Metafield/%s" % n: {"resourceId": "gid://shopify/Metafield/%s" % n,
                                                 "translatableContent": [c("value", v, "JSON")], "translations": {}} for n, v in ROOTS.items()},
            "gid://shopify/Metafield/10": {"resourceId": "gid://shopify/Metafield/10", "translatableContent": [c("value", FAQ_JSON, "JSON")],
                                           "translations": {"nl": [tr("value", json.dumps([{"question": "Oud", "answer": "Existing approved NL"}]))]}},
            "gid://shopify/Metafield/11": {"resourceId": "gid://shopify/Metafield/11", "translatableContent": [c("value", TRICKY_JSON, "JSON")],
                                           "translations": {}},
            "gid://shopify/SellingPlan/5": {"resourceId": "gid://shopify/SellingPlan/5", "translatableContent": [c("name", "Year")],
                                            "translations": {}},
            "gid://shopify/MediaImage/3": {"resourceId": "gid://shopify/MediaImage/3", "translatableContent": [c("alt", "A duo")],
                                           "translations": {"nl": [tr("alt", "Een duo")]}},
        },
        "product_metafields": {"gid://shopify/Product/1": [
            {"id": "gid://shopify/Metafield/9", "namespace": "custom", "key": "treatment_journey_feel", "type": "rich_text_field", "value": JOURNEY_JSON},
            {"id": "gid://shopify/Metafield/10", "namespace": "custom", "key": "product_faq", "type": "json", "value": FAQ_JSON},
            {"id": "gid://shopify/Metafield/11", "namespace": "custom", "key": "tricky", "type": "json", "value": TRICKY_JSON},
            {"id": "gid://shopify/Metafield/12", "namespace": "custom", "key": "professional_testimonials", "type": "list.metaobject_reference",
             "value": json.dumps(["gid://shopify/Metaobject/700"])},
            {"id": "gid://shopify/Metafield/13", "namespace": "custom", "key": "faq_link", "type": "json", "value": FAQ_LINK_JSON}] +
            [{"id": "gid://shopify/Metafield/%s" % n, "namespace": "custom", "key": "root_%s" % n, "type": "json", "value": v} for n, v in ROOTS.items()]},
        "metaobjects": None,
    }


def item(iid, en, value, kind="match", key=None, field="f", hint=None, hold=()):
    out = {"id": iid, "kind": kind, "key": key, "field": field, "en": en, "en_sha1": sha1(en), "value": value,
           "gates": [], "hold": list(hold), "how": "", "status": {"drafted": True, "registered": False}}
    if hint is not None:
        out["hint"] = hint
    return out


def base_plan():
    return {"lang": "nl", "resources": [
        {"shopify_type": "ONLINE_STORE_THEME_JSON_TEMPLATE", "owner": "templates/index.json", "items": [
            item("hero", "Your mouth has a rhythm", "Je mond heeft een ritme", hint=["hero", "heading"]),
            item("card2", "Begin", "Begin nu", hint=["cards", "card_2", "title"]),
            item("cardX", "Begin", "Begin nu", hint=["cards", "card_9", "title"]),
            item("faq", "Old EN at capture", "Oude NL", hint=["faq", "q1", "question"]),
            item("gift1", "Gift, pause or cancel", "Pauzeren of opzeggen", hint=["gift", "label"]),
            item("long", "Long EN", LONG_NL, hint=["long", "l1", "text"]),
            item("yearlabel", "Year", "Jaar", hint=["compare"]),
            item("held", "Begin", "Begin", hint=["cards", "card_1", "title"], hold=["pending-claim-review"]),
        ]},
        {"shopify_type": "ONLINE_STORE_THEME_JSON_TEMPLATE", "owner": "templates/product.subscription-item.json", "items": [
            item("other-template", "Old EN at capture", "Oude NL", hint=["other", "x", "title"])]},
        {"shopify_type": "SELLING_PLAN", "owner": "gid://shopify/SellingPlan/5", "items": [item("sp", "Year", "Jaar", kind="direct", key="name")]},
        {"shopify_type": "MEDIA_IMAGE", "owner": "gid://shopify/SellingPlan/5", "items": [item("disguised", "Year", "Jaar", kind="direct", key="name")]},
        {"shopify_type": "MEDIA_IMAGE", "owner": "gid://shopify/MediaImage/3", "items": [item("alt", "A duo", "Een duo", kind="direct", key="alt")]},
        {"shopify_type": "PAGE", "owner": "manifesto", "assembled_field": {"blocks": 2, "drafted": 2, "missing_or_held": 0, "gated": 0}, "items": [
            item("b1", "<p>First block.</p>", "<p>Eerste blok.</p>", kind="assemble", key="body", field="body_html#b001"),
            item("b2", "<p>Second block.</p>", "<p>Tweede blok.</p>", kind="assemble", key="body", field="body_html#b002")]},
        {"shopify_type": "METAFIELD", "owner": "duo", "items": [
            item("j1", "What you'll feel", "Wat je voelt", key="value", field="custom.treatment_journey_*#01"),
            item("j2", "Free", "Gratis", key="value", field="custom.treatment_journey_*#02"),
            item("j3", "€0.49", "€0,49", key="value", field="custom.treatment_journey_*#03"),
            item("f1", "Hello", "Hallo", key="value", field="custom.product_faq#01"),
            item("f2", "Held claim", "Vastgehouden claim", key="value", field="custom.product_faq#02", hold=["pending-claim-review"]),
            item("t1", "Free", "Gratis", key="value", field="custom.tricky#01"),
            item("t2", "Hello", "Hallo", key="value", field="custom.tricky#02"),
            item("t3", "Hallo", "Bonjour", key="value", field="custom.tricky#03"),
            item("t4", "café", "koffiehuis", key="value", field="custom.tricky#04"),
            item("fl1", "Hello", "Hallo", key="value", field="custom.faq_link#01"),
            item("fl2", "Held claim", "Vastgehouden claim", key="value", field="custom.faq_link#02", hold=["pending-claim-review"]),
            item("r1", "Hello", "Hallo", key="value", field="custom.root_*#01")]},
        {"shopify_type": "METAOBJECT", "owner": "duo", "items": [
            item("role", "Pharmacist", "Apotheker", field="custom.professional_testimonials#01")]},
        {"shopify_type": "PRODUCT", "owner": "duo", "items": [item("title", "Awake & Asleep", "Awake & Asleep", kind="direct", key="title")]},
        {"shopify_type": "PRODUCT", "owner": "supply", "items": [item("supply", "60-Day Supply", "60-daagse voorraad", kind="direct", key="title")]},
        {"shopify_type": "LINK", "owner": "navigation:new-main-menu", "items": [item("link", "Manifesto", "Manifest", key="title")]},
    ]}


class Fake:
    """The fake store. Hooks inject errors: token_status, graphql_error, user_error, mutation_status, raise_on."""

    def __init__(self, store, **hooks):
        self.store, self.hooks, self.mutations, self.calls = store, hooks, [], 0

    def view(self, node, locale):
        tl = node.get("translations") or {}
        return dict(node, translations=tl.get(locale, []) if isinstance(tl, dict) else [])

    def post(self, path, body, headers):
        page = {"hasNextPage": False, "endCursor": None}
        if path == "/admin/oauth/access_token":
            if self.hooks.get("token_status"):
                return self.hooks["token_status"], {"error": "bad " + body["client_secret"]}, None
            ok = body.get("client_secret") == SECRET and body.get("grant_type") == "client_credentials"
            scope = self.hooks.get("scope", "read_translations,write_translations,read_products")
            body_out = {"access_token": TOKEN} if scope is None else {"access_token": TOKEN, "scope": scope}
            return (200, body_out, None) if ok else (401, {}, None)
        assert headers.get("X-Shopify-Access-Token") == TOKEN
        self.calls += 1
        if self.hooks.get("raise_on") and self.hooks["raise_on"](body):
            raise register.TransportError("URLError")
        if self.hooks.get("graphql_error"):
            return 200, {"errors": [{"message": "token %s rejected" % TOKEN, "extensions": {"code": "BAD"}}]}, None
        q, v = body["query"], body["variables"]
        locale = v.get("locale")
        if "translationsRegister" in q or "translationsRemove" in q:
            self.mutations.append(("register" if "Register" in q else "remove", v["id"], v.get("translations") or v.get("keys")))
            status = self.hooks.get("mutation_status")
            if status and status(len(self.mutations)):
                return status(len(self.mutations)), {"errors": "server error"}, None
            name = "translationsRegister" if "Register" in q else "translationsRemove"
            keys = [t["key"] for t in v["translations"]] if "Register" in q else v["keys"]
            errs = [{"field": ["translations"], "message": "echo " + TOKEN, "code": "INVALID"}] if self.hooks.get("user_error") else []
            return 200, {"data": {name: {"translations": [] if errs else [{"key": k, "locale": "nl"} for k in keys], "userErrors": errs}}}, None
        if "translatableResourcesByIds" in q:
            nodes = [self.view(self.store["ids"][i], locale) for i in v["ids"] if i in self.store["ids"]]
            for t in self.store["types"].values():
                nodes += [self.view(n, locale) for n in t if n["resourceId"] in v["ids"]]
            return 200, {"data": {"translatableResourcesByIds": {"nodes": nodes, "pageInfo": page}}}, None
        if "translatableResources" in q:
            nodes = [self.view(n, locale) for n in self.store["types"].get(v["type"], [])]
            return 200, {"data": {"translatableResources": {"nodes": nodes, "pageInfo": page}}}, None
        if "metafields" in q:
            return 200, {"data": {"product": {"metafields": {"nodes": self.store["product_metafields"].get(v["id"], []), "pageInfo": page}}}}, None
        if "themes(" in q:
            main = self.hooks.get("main_theme", THEME)
            if main == "denied":
                return 200, {"errors": [{"message": "Access denied", "extensions": {"code": "ACCESS_DENIED"}}]}, None
            return 200, {"data": {"themes": {"nodes": [{"id": "gid://shopify/OnlineStoreTheme/%s" % main}]}}}, None
        if "metaobject" in q:
            return 200, {"errors": [{"message": "Access denied", "extensions": {"code": "ACCESS_DENIED"}}]}, None
        raise AssertionError("unexpected query")


ROLE_BINDING = {"role": {"resource": "gid://shopify/Metaobject/700", "key": "role", "en_sha1": sha1("Pharmacist")}}


def run(argv, fake, folder, plan=None, bindings=ROLE_BINDING):
    with open(os.path.join(folder, "plan-nl.json"), "w", encoding="utf-8") as f:
        json.dump(plan or base_plan(), f)
    bpath = os.path.join(folder, "bindings.json")
    if bindings is not None:
        with open(bpath, "w", encoding="utf-8") as f:
            json.dump({"bindings": bindings}, f)
    elif os.path.exists(bpath):
        os.remove(bpath)
    out, err = io.StringIO(), io.StringIO()
    code = 0
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        try:
            register.main(argv, transport=fake, credentials=lambda: ("client-id", register.Secret(SECRET)),
                          out=folder, plans=os.path.join(folder, "plan-%s.json"), bindings_path=bpath)
        except SystemExit as e:
            code = e.code if isinstance(e.code, int) else 1
    return code, out.getvalue() + err.getvalue()


def files_text(folder):
    return "".join(open(os.path.join(folder, n), encoding="utf-8").read() for n in sorted(os.listdir(folder)))


def dry(folder, store=None, argv=("--lang", "nl", "--theme-id", THEME), bindings=ROLE_BINDING, **hooks):
    fake = Fake(store or base_store(), **hooks)
    code, text = run(list(argv), fake, folder, bindings=bindings)
    data = json.load(open(os.path.join(folder, "dry-run-nl.json"), encoding="utf-8")) if code == 0 else None
    return code, text, fake, data


# ---- R18e: the real HTTP transport, refused token requests and every output sink ----------------------------

CID = "cid-R18E-0123456789abcdef"
SEC2 = "shpss_R18e/Sec+ret=V&al ue"


def echoes(value):
    """The spellings an echoed credential can arrive in."""
    q = urllib.parse.quote(value, safe="")
    return {"literal": value, "percent": q, "percent-lower": re.sub(r"%[0-9A-F]{2}", lambda m: m.group(0).lower(), q),
            "form": urllib.parse.quote_plus(value), "entity": "&#%d;" % ord(value[0]) + value[1:],
            "split": value[:6] + "<b></b>" + value[6:], "cut": value[:-3]}


def leaked(text):
    """Any 8 characters in a row of a credential, raw or percent/form-encoded, in the text or in any stage of
    decoding it (percent and HTML entities, to a fixed point), or a credential header word."""
    stages, x = [text], text
    for _ in range(200):
        y = html.unescape(urllib.parse.unquote(x))
        if y == x:
            break
        stages.append(y)
        x = y
    low = "\n".join(stages).lower()
    for cred in (CID, SEC2, TOKEN, SECRET):
        for form in (cred, urllib.parse.quote(cred, safe=""), urllib.parse.quote_plus(cred)):
            if any(form[i:i + 8].lower() in low for i in range(len(form) - 7)):
                return cred[:4] + "… as " + ("raw" if form == cred else "encoded")
    return "header word" if re.search(r"bearer|authori[sz]ation|x-shopify-access-token", low) else None


class Resp:
    def __init__(self, status, body):
        self.status, self.body, self.headers = status, body, email.message.Message()

    def read(self):
        return self.body

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


@contextlib.contextmanager
def wire(responder):
    """Patch urlopen under the real HttpTransport; responder(request, n) gives (status, bytes) or an exception."""
    calls, original = [], register.urllib.request.urlopen

    def fake(req, timeout=60):
        calls.append(req)
        answer = responder(req, len(calls))
        if isinstance(answer, Exception):
            raise answer
        status, body = answer
        if status >= 400:
            raise urllib.error.HTTPError(req.full_url, status, "error", email.message.Message(), io.BytesIO(body))
        return Resp(status, body)
    register.urllib.request.urlopen = fake
    try:
        yield calls
    finally:
        register.urllib.request.urlopen = original


def refuse(body, status=400):
    """main() against a token endpoint that refuses with body: (exit code, all output, token attempts, files)."""
    with tempfile.TemporaryDirectory() as sub, wire(lambda req, n: (status, body)) as calls:
        out = io.StringIO()
        code = 0
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(out):
            try:
                register.main(["--lang", "nl", "--theme-id", THEME], transport=register.HttpTransport(),
                              credentials=lambda: (CID, register.Secret(SEC2)), out=os.path.join(sub, "live"),
                              plans=os.path.join(sub, "plan-%s.json"), bindings_path=os.path.join(sub, "bindings.json"))
            except SystemExit as e:
                code = e.code if isinstance(e.code, int) else 1
        files = [os.path.join(d, f) for d, _, fs in os.walk(sub) for f in fs]
        attempts = len(calls)
        try:
            register.Admin(register.HttpTransport(), CID, register.Secret(SEC2))
            chain = ""
        except register.RunnerError as err:
            chain, e = "", err  # every message in the exception chain (source paths left out: they name this file)
            while e is not None:
                chain += "".join(traceback.format_exception_only(type(e), e))
                e = e.__cause__ or e.__context__
    return code, out.getvalue(), attempts, files, chain


def r18e(check):
    # 1. Wire format through the real transport
    ok_token = json.dumps({"access_token": TOKEN, "scope": "read_translations"}).encode()
    with wire(lambda req, n: (200, ok_token) if n == 1 else (200, b'{"data": {}}')) as calls:
        admin = register.Admin(register.HttpTransport(), CID, register.Secret(SEC2))
        admin._post("query { shop { id } }", {"a": 1})
    tok, gql = calls
    sent = urllib.parse.parse_qs(tok.data.decode("ascii"), strict_parsing=True)
    check("R18e wire: token POST to the fixed HTTPS endpoint, form-encoded",
          tok.full_url == "https://karmicares.myshopify.com/admin/oauth/access_token" and tok.get_method() == "POST"
          and tok.get_header("Content-type") == register.FORM, (tok.full_url, tok.get_header("Content-type")))
    check("R18e wire: form body round-trips reserved characters",
          sent == {"client_id": [CID], "client_secret": [SEC2], "grant_type": ["client_credentials"]}, sent)
    check("R18e wire: no credential in the URL or an Authorization header",
          not leaked(tok.full_url) and tok.get_header("Authorization") is None and gql.get_header("Authorization") is None)
    check("R18e wire: GraphQL stays JSON with the token header only",
          gql.get_header("Content-type") == "application/json" and json.loads(gql.data) == {"query": "query { shop { id } }", "variables": {"a": 1}}
          and gql.get_header("X-shopify-access-token") == TOKEN and CID not in gql.full_url)
    once = []
    for label, answer in (("400", (400, b'{"error": "invalid_client"}')), ("429", (429, b"slow down")), ("500", (500, b"<h1>oops</h1>")),
                          ("transport", urllib.error.URLError("down " + SEC2))):
        with wire(lambda req, n, a=answer: a) as calls:
            try:
                register.Admin(register.HttpTransport(), CID, register.Secret(SEC2))
            except register.RunnerError as e:
                if len(calls) != 1 or leaked(str(e)):
                    once.append(label)
    check("R18e wire: one token attempt on 400, 429, 500 and a transport failure", not once, once)

    # 2. Refusal matrix: every body shape x every credential x every spelling
    lines = {"Token request refused (HTTP 400)%s. Check that the app is installed on %s." % (register.oauth_error({"error": c}), register.SHOP)
             for c in list(register.OAUTH_ERRORS) + [None]}
    bad, total = [], 0
    for cred in (CID, SEC2, TOKEN):
        for form, e in echoes(cred).items():
            bodies = {
                "JSON description": json.dumps({"error": "invalid_client", "error_description": "bad " + e}).encode(),
                "JSON code": json.dumps({"error": e}).encode(),
                "JSON key": json.dumps({e: 1}).encode(),
                "plain text": ("bad " + e).encode(),
                "HTML": ("<html><body><h1>Oauth error application_cannot_be_found: Could not find " + e + "</h1></body></html>").encode(),
                "invalid UTF-8": b"\xff\xfe bad " + e.encode(),
                "truncated JSON": ('{"error": "invalid_client", "client_secret": "' + e).encode(),
                "Bearer": ("Authorization: Bearer " + urllib.parse.quote(e) + "\nX-Shopify-Access-Token: " + e).encode(),
            }
            for shape, body in bodies.items():
                total += 1
                code, text, attempts, files, chain = refuse(body)
                why = leaked(text) or leaked(chain)
                if code != 2 or attempts != 1 or files or text.strip() not in lines or why:
                    bad.append("%s/%s/%s: %s" % (cred[:4], form, shape, why or text.strip()[:80]))
    check("R18e refusals: %d bodies give a fixed line, exit 2, one attempt, no files, no leak" % total, not bad, bad[:3])
    code, text, _, _, _ = refuse(b"<h1>Oauth error application_cannot_be_found: Could not find Shopify A</h1>")
    check("R18e refusals: a known code in an HTML body is named with our own text",
          code == 2 and "application_cannot_be_found (Shopify knows no app" in text, text)
    code, text, _, _, _ = refuse(json.dumps({"error": "shop_not_permitted", "error_description": "whatever"}).encode())
    check("R18e refusals: a known JSON code is named, its description is not",
          "shop_not_permitted (client credentials" in text and "whatever" not in text, text)

    # 3. Every sink: non-JSON and JSON echoes through the shared parser into the writer, journal and reports
    sinks = []
    for label, reply in (
            ("non-JSON 500", lambda: (500, register.HttpTransport._json(("Authorization: Bearer " + urllib.parse.quote(TOKEN)).encode()), None)),
            ("non-JSON 400", lambda: (400, register.HttpTransport._json(("<p>" + urllib.parse.quote_plus(SECRET) + "</p>").encode()), None)),
            ("JSON error echo", lambda: (200, {"errors": [{"message": "bad " + urllib.parse.quote(TOKEN), "extensions": {"code": "X"}}]}, None)),
            ("userErrors echo", None)):
        class Echo(Fake):
            def post(self, path, body, headers, reply=reply):
                if reply and "translationsRegister" in body.get("query", ""):
                    self.mutations.append(("register", body["variables"]["id"], body["variables"]["translations"]))
                    return reply()
                if reply is None and "translationsRegister" in body.get("query", ""):
                    self.mutations.append(("register", body["variables"]["id"], body["variables"]["translations"]))
                    errs = [{"field": ["translations", "&#%d;" % ord(TOKEN[0]) + TOKEN[1:]], "message": "x", "code": "INVALID"}]
                    return 200, {"data": {"translationsRegister": {"translations": [], "userErrors": errs}}}, None
                return super().post(path, body, headers)
        with tempfile.TemporaryDirectory() as sub:
            code, _, _, dd = dry(sub)
            echo = Echo(base_store())
            code, text = run(["--lang", "nl", "--theme-id", THEME, "--write", "--approve", dd["checksum"]], echo, sub)
            journal = open(os.path.join(sub, "journal-nl.jsonl"), encoding="utf-8").read()
            why = leaked(text) or leaked(files_text(sub))
            if code == 0 or len(echo.mutations) != 1 or '"event": "end"' in journal or why:
                sinks.append("%s: code %s, %d mutations, %s" % (label, code, len(echo.mutations), why))
    check("R18e sinks: stdout, reports and journal stay clean, the write stops (4 cases)", not sinks, sinks)
    with tempfile.TemporaryDirectory() as sub:
        err_obj = register.HttpTransport._json(("<b>" + urllib.parse.quote(SECRET, safe="") + "</b>").encode())
        safe = register.safe_errors([{"message": "echo " + urllib.parse.quote_plus(TOKEN)}, {"message": "Translation key is invalid"}])
        register.write_text(os.path.join(sub, "r.md"), json.dumps(err_obj) + json.dumps(safe))
        register.write_json(os.path.join(sub, "r.json"), {"e": err_obj, "s": safe})
        check("R18e sinks: report writers get no response text, and credential-like messages are withheld",
              not leaked(files_text(sub)) and safe[0]["message"].startswith("withheld (") and safe[1]["message"] == "Translation key is invalid",
              safe)
    check("R18e-2 the client ID is scrubbed once a token is requested", register.scrub("id " + CID) == "id [redacted]")
    r18f(check)
    r18g(check)
    r18h(check)


LONG_RUN = 400000  # characters per long-markup case (R18g-2)


def nested_token():
    """A once-encoded token behind enough nested entities to exhaust any bounded decoding search (R18g-1)."""
    # 65 entity levels, then the token with every fourth character percent-encoded: under 300 characters, so a
    # 300-character cut cannot hide it, and no 8 raw characters of it in a row
    return "&" + "amp;" * 65 + "lt; " + "".join("%%%02X" % ord(ch) if i % 4 == 0 else ch for i, ch in enumerate(TOKEN))


def r18g(check):
    nested = nested_token()
    got = register.safe_errors([{"message": nested, "extensions": {"code": nested}, "field": ["translations", nested]}])[0]
    check("R18g a token behind nested entities is withheld in message, code and field",
          all(str(v).startswith("withheld (") for v in (got["message"], got["code"], got["field"][1])) and not leaked(json.dumps(got)), got)

    class NestedRead(Fake):
        def post(self, path, body, headers):
            if path != "/admin/oauth/access_token" and "translatableResources(" in body.get("query", ""):
                return 200, {"errors": [{"message": nested, "extensions": {"code": "BAD_USER_INPUT"}}]}, None
            return super().post(path, body, headers)
    with tempfile.TemporaryDirectory() as sub:
        code, text = run(["--lang", "nl", "--theme-id", THEME], NestedRead(base_store()), sub)
        check("R18g read error with the nested-entity token: exit 2, code kept, no leak",
              code == 2 and "BAD_USER_INPUT" in text and not leaked(text) and not leaked(files_text(sub)), (code, leaked(text)))

    class NestedWrite(Fake):
        def post(self, path, body, headers):
            if "translationsRegister" in body.get("query", ""):
                self.mutations.append(("register", body["variables"]["id"], body["variables"]["translations"]))
                errs = [{"field": ["translations", "0", "value"], "message": nested, "code": "INVALID"}]
                return 200, {"data": {"translationsRegister": {"translations": [], "userErrors": errs}}}, None
            return super().post(path, body, headers)
    with tempfile.TemporaryDirectory() as sub:
        _, _, _, dd = dry(sub)
        echo = NestedWrite(base_store())
        code, text = run(["--lang", "nl", "--theme-id", THEME, "--write", "--approve", dd["checksum"]], echo, sub)
        journal = open(os.path.join(sub, "journal-nl.jsonl"), encoding="utf-8").read()
        check("R18g userErrors with the nested-entity token: write stops, journal keeps code and field, no leak",
              code == 2 and len(echo.mutations) == 1 and '"event": "end"' not in journal and '"INVALID"' in journal
              and '"value"' in journal and not leaked(text + files_text(sub)), (code, len(echo.mutations), leaked(text + files_text(sub))))

    slow = []
    n = LONG_RUN
    for label, text in (("unclosed tag", "<" + "a" * n), ("many opening brackets", "<" * n),
                        ("unclosed entity run", "&" * n), ("percent run", "%" * n)):
        started = time.monotonic()
        register.safe_errors([{"message": text, "extensions": {"code": text}, "field": [text, "translations"]}])
        register.HttpTransport._json(text.encode() + b"\xff")
        if time.monotonic() - started > 1.0:
            slow.append(label)
    check("R18g long unclosed markup and entity runs are handled in under a second each", not slow, slow)

    ordinary = register.safe_errors([{"message": "Translation key is invalid", "code": "INVALID_KEY_FOR_MODEL",
                                      "field": ["translations", 0, "key"]}, {"message": "Some new wording", "code": "NEW_CODE"}])
    check("R18g allowlisted messages, codes and paths stay readable; anything else shows only its length",
          ordinary[0] == {"code": "INVALID_KEY_FOR_MODEL", "field": ["translations", "0", "key"], "message": "Translation key is invalid"}
          and ordinary[1] == {"code": "withheld (8 chars)", "field": None, "message": "withheld (16 chars)"}, ordinary)


# ---- wave 2a: exact section ids and selling plans (metaobjects wait for the R30 rework) ------------------------

def w2a_store():
    store = base_store()
    store["types"]["ONLINE_STORE_THEME_JSON_TEMPLATE"][0]["translatableContent"] += [
        c("section.index.json.benefits.heading:k1", "Clean is not healthy"),
        c("section.index.json.benefits.card_1.heading:k2", "Clean is not healthy")]
    store["types"]["SELLING_PLAN_GROUP"] = [
        {"resourceId": "gid://shopify/SellingPlanGroup/%s" % n, "translatableContent": [c("name", v)], "translations": {}}
        for n, v in (("1", "60-Day Rhythm"), ("2", "60-Day Rhythm"), ("3", "60-Day Supply"))]
    store["ids"]["gid://shopify/SellingPlan/6"] = {"resourceId": "gid://shopify/SellingPlan/6", "translatableContent": [
        c("description", '<div class="kc-return_care">10% back</div>'), c("option1", "Year Supply"), c("billing_note", "Billed yearly")],
        "translations": {}}
    return store


def w2a_plan():
    return {"lang": "nl", "resources": [
        {"shopify_type": "ONLINE_STORE_THEME_JSON_TEMPLATE", "owner": "templates/index.json", "items": [
            item("w2sec", "Clean is not healthy", "Schoon is niet gezond", hint=["benefits", "heading"])]},
        {"shopify_type": "SELLING_PLAN_GROUP", "owner": "name: 60-Day Rhythm", "items": [item("w2g", "60-Day Rhythm", "60-dagenritme", key="name")]},
        {"shopify_type": "SELLING_PLAN_GROUP", "owner": "name: 60-Day Supply", "items": [item("w2gs", "60-Day Supply", "60-dagenvoorraad", key="name")]},
        {"shopify_type": "SELLING_PLAN", "owner": "gid://shopify/SellingPlan/6", "items": [
            item("w2d", '<div class="kc-return_care">10% back</div>', '<div class="kc-return_care">10% terug</div>', kind="direct", key="description"),
            item("w2o", "Year Supply", "Jaarvoorraad", kind="direct", key="option1"),
            item("w2b", "Billed yearly", "Jaarlijks gefactureerd", kind="direct", key="billing_note")]},
        {"shopify_type": "SELLING_PLAN", "owner": "gid://shopify/MediaImage/3", "items": [item("w2x", "A duo", "Een duo", kind="direct", key="alt")]},
    ]}


def wave2a(check):
    with tempfile.TemporaryDirectory() as sub:
        code, text = run(["--lang", "nl", "--theme-id", THEME], Fake(w2a_store()), sub, w2a_plan(), bindings=None)
        d = json.load(open(os.path.join(sub, "dry-run-nl.json"), encoding="utf-8")) if code == 0 else {"ops": [], "rows": []}
    ops = {(o["resource"], o["key"]): o for o in d["ops"]}
    res = {}
    for r in d["rows"]:
        res.setdefault(r["id"], r["result"])
    check("wave 2a: dry run exits 0", code == 0, text)
    check("wave 2a: a section-level setting matches its exact ids, not its blocks' settings",
          (IDX, "section.index.json.benefits.heading:k1") in ops and (IDX, "section.index.json.benefits.card_1.heading:k2") not in ops)
    check("wave 2a: every selling-plan group with the EN name gets the translation",
          ("gid://shopify/SellingPlanGroup/1", "name") in ops and ("gid://shopify/SellingPlanGroup/2", "name") in ops)
    check("wave 2a (B-01): the Subscription Name values stay untranslated",
          ("gid://shopify/SellingPlanGroup/3", "name") not in ops and ("gid://shopify/SellingPlan/6", "option1") not in ops
          and res.get("w2gs") == "not written" and res.get("w2o") == "not written", res)
    check("wave 2a: a selling-plan description is registered whole",
          ops.get(("gid://shopify/SellingPlan/6", "description"), {}).get("value") == '<div class="kc-return_care">10% terug</div>')
    check("wave 2a: selling-plan content other than name, description and options is protected",
          ("gid://shopify/SellingPlan/6", "billing_note") not in ops and res.get("w2b") == "not written")
    check("wave 2a: an owner GID of another type is refused", res.get("w2x") == "not written"
          and ("gid://shopify/MediaImage/3", "alt") not in ops)


def encoded_token():
    return "".join("%%%02X" % ord(ch) for ch in TOKEN)


def r18h(check):
    enc = encoded_token()

    # R18h-1: a receipt's own keys never reach the journal
    def receipt(kind):
        def reply(keys):
            if kind == "unrequested key":
                return [{"key": enc, "locale": "nl"}], []
            if kind == "unrequested key with userErrors":
                return [{"key": enc, "locale": "nl"}], [{"field": ["translations", "0", "key"], "message": "x", "code": "INVALID"}]
            if kind == "duplicate key":
                return [{"key": k, "locale": "nl"} for k in keys + keys[:1]] + [{"key": enc, "locale": "nl"}], []
            return [{"key": enc, "locale": "fr"}], []  # wrong locale
        return reply
    bad = []
    for kind in ("unrequested key", "unrequested key with userErrors", "duplicate key", "wrong locale"):
        class Receipt(Fake):
            def post(self, path, body, headers, reply=receipt(kind)):
                if "translationsRegister" in body.get("query", ""):
                    v = body["variables"]
                    self.mutations.append(("register", v["id"], v["translations"]))
                    entries, errs = reply([t["key"] for t in v["translations"]])
                    return 200, {"data": {"translationsRegister": {"translations": entries, "userErrors": errs}}}, None
                return super().post(path, body, headers)
        with tempfile.TemporaryDirectory() as sub:
            _, _, _, dd = dry(sub)
            fake = Receipt(base_store())
            code, text = run(["--lang", "nl", "--theme-id", THEME, "--write", "--approve", dd["checksum"]], fake, sub)
            journal = [json.loads(line) for line in open(os.path.join(sub, "journal-nl.jsonl"), encoding="utf-8")]
            results = [j for j in journal if j.get("event") == "result"]
            if (code != 2 or len(fake.mutations) != 1 or len(results) != 1 or results[0]["confirmed"] != []
                    or any(j.get("event") == "end" for j in journal) or "0 keys confirmed so far" not in text
                    or leaked(text + files_text(sub))):
                bad.append("%s: code %s, confirmed %s, leak %s" % (kind, code, results[0]["confirmed"] if results else "-",
                                                                   leaked(text + files_text(sub))))
    check("R18h-1 receipts with unrequested, duplicate or wrong-locale keys journal nothing as confirmed (4)", not bad, bad)

    # R18h-2: a malformed resource ID is dropped before anything parses or prints it
    bad_gid = "gid://" + enc + "℀/OnlineStoreThemeJsonTemplate/index?theme_id=111"
    store = base_store()
    store["types"]["ONLINE_STORE_THEME_JSON_TEMPLATE"].append(dict(copy.deepcopy(store["types"]["ONLINE_STORE_THEME_JSON_TEMPLATE"][0]), resourceId=bad_gid))
    with tempfile.TemporaryDirectory() as sub:
        code, text, _, _ = dry(sub, store)
        check("R18h-2 a malformed GID carrying an encoded token is ignored: no crash, no leak",
              code == 0 and not register.valid_gid(bad_gid) and not register.theme_owned(bad_gid, THEME, "index")
              and not leaked(text + files_text(sub)), (code, leaked(text + files_text(sub))))
    check("R18h-2 real GIDs of every shape the runner reads stay valid",
          all(register.valid_gid(g) for g in (IDX, PDP, "gid://shopify/OnlineStoreThemeSectionGroup/footer-group?theme_id=187295564157",
                                                "gid://shopify/MediaImage/27295901057206", "gid://shopify/Metafield/1", "gid://shopify/Shop/64261423286")))

    # R18h-2: an HTTPError whose body read fails stays inside the transport boundary
    class FailingBody(io.BytesIO):
        def read(self, *a):
            raise OSError("read failed " + enc)

    def http_error(req, n):
        return urllib.error.HTTPError(req.full_url, 400, "error", email.message.Message(), FailingBody())
    with wire(http_error) as calls:
        try:
            register.Admin(register.HttpTransport(), CID, register.Secret(SEC2))
            tb, msg = "", ""
        except register.RunnerError as err:
            # formatted chain without source paths (they name this file, whose name looks like the test token)
            tb, msg = "".join(traceback.format_exception(type(err), err, None)), str(err)
    check("R18h-2 a failing HTTPError body read becomes a data-free transport error",
          len(calls) == 1 and msg == "Token request failed: network error (OSError)." and not leaked(tb), (msg, leaked(tb)))
    code, text, _, _, _ = refuse_with(http_error)
    check("R18h-2 the same failure through main(): exit 2, fixed line, no leak", code == 2 and not leaked(text) and "OSError" in text, text)

    # R18h-2: the outermost handler shows only a category
    class Exploding(Fake):
        def post(self, path, body, headers):
            if path != "/admin/oauth/access_token":
                raise ValueError("unexpected " + enc)
            return super().post(path, body, headers)
    with tempfile.TemporaryDirectory() as sub:
        code, text = run(["--lang", "nl", "--theme-id", THEME], Exploding(base_store()), sub)
        check("R18h-2 an unexpected exception prints its category only", code == 3 and "Internal error (ValueError)" in text
              and not leaked(text) and not leaked(files_text(sub)), text)
        out = io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(out):
            try:
                register.main(["--lang", "nl", "--theme-id", THEME], transport=Exploding(base_store()),
                              credentials=lambda: ("client-id", register.Secret(SECRET)), out=sub,
                              plans=os.path.join(sub, "plan-%s.json"), bindings_path=os.path.join(sub, "bindings.json"))
                formatted = ""
            except SystemExit as stop:
                formatted = "".join(traceback.format_exception(type(stop), stop, None))
        check("R18i-1 a formatted SystemExit carries no original exception or token",
              formatted.startswith("SystemExit: 3") and "ValueError" not in formatted and not leaked(formatted), formatted[:200])


def refuse_with(responder):
    """main() against a patched urlopen: (exit code, output, attempts, files, '')."""
    with tempfile.TemporaryDirectory() as sub, wire(responder) as calls:
        out = io.StringIO()
        code = 0
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(out):
            try:
                register.main(["--lang", "nl", "--theme-id", THEME], transport=register.HttpTransport(),
                              credentials=lambda: (CID, register.Secret(SEC2)), out=os.path.join(sub, "live"),
                              plans=os.path.join(sub, "plan-%s.json"), bindings_path=os.path.join(sub, "bindings.json"))
            except SystemExit as e:
                code = e.code if isinstance(e.code, int) else 1
        return code, out.getvalue(), len(calls), [f for _, _, fs in os.walk(sub) for f in fs], ""


def entities(value):
    return "".join("&#%d;" % ord(ch) for ch in value)


def markup_echoes():
    """Credentials hidden in HTML that is removed only after decoding (R18f-1)."""
    spaced = "ab cd ef gh ij kl mn op"
    register.Secret(spaced)
    return {
        "attribute, entity token": '<span data-value="&#115;' + TOKEN[1:] + '">text</span>',
        "attribute, percent client ID": '<a title="' + urllib.parse.quote(CID, safe="").replace("-", "%2D") + '">x</a>',
        "comment, entity secret": "ok <!-- " + entities(SECRET) + " --> done",
        "encoded angle brackets": "&lt;" + entities(TOKEN) + "&gt;",
        "spaced secret, form-encoded": "bad " + urllib.parse.quote_plus(spaced),
    }


def r18f(check):
    hidden = markup_echoes()
    bad = []
    for label, echo in hidden.items():
        for where in ("message", "code", "field"):
            err = {"message": "Translation key is invalid", "extensions": {"code": "INVALID_KEY_FOR_MODEL"}, "field": ["translations", "0", "key"]}
            if where == "message":
                err["message"] = echo
            elif where == "code":
                err["extensions"]["code"] = echo
            else:
                err["field"] = ["translations", echo]
            got = register.safe_errors([err])[0]
            kept = {"message": got["message"], "code": got["code"], "field": got["field"]}
            want_withheld = (kept[where] if where != "field" else got["field"][1]).startswith("withheld (")
            others = [k for k in ("message", "code") if k != where]
            useful = all(kept[k] in ("Translation key is invalid", "INVALID_KEY_FOR_MODEL") for k in others) and (
                where == "field" or got["field"] == ["translations", "0", "key"])
            if not want_withheld or not useful:
                bad.append("%s in %s: %s" % (label, where, kept))
    check("R18f markup-hidden credentials are withheld in message, code and field (%d)" % (len(hidden) * 3), not bad, bad[:2])

    class AttrRead(Fake):
        def post(self, path, body, headers):
            if path != "/admin/oauth/access_token" and "translatableResources(" in body.get("query", ""):
                return 200, {"errors": [{"message": hidden["attribute, entity token"], "extensions": {"code": "BAD_REQUEST"}}]}, None
            return super().post(path, body, headers)
    with tempfile.TemporaryDirectory() as sub:
        code, text = run(["--lang", "nl", "--theme-id", THEME], AttrRead(base_store()), sub)
        check("R18f read error with an attribute-hidden token: exit 2, no leak in output or files",
              code == 2 and not leaked(text) and not leaked(files_text(sub)), (code, leaked(text), leaked(files_text(sub))))

    class AttrWrite(Fake):
        def post(self, path, body, headers):
            if "translationsRegister" in body.get("query", ""):
                self.mutations.append(("register", body["variables"]["id"], body["variables"]["translations"]))
                errs = [{"field": ["translations", "0", "value"], "message": hidden["attribute, entity token"], "code": "INVALID"}]
                return 200, {"data": {"translationsRegister": {"translations": [], "userErrors": errs}}}, None
            return super().post(path, body, headers)
    with tempfile.TemporaryDirectory() as sub:
        _, _, _, dd = dry(sub)
        echo = AttrWrite(base_store())
        code, text = run(["--lang", "nl", "--theme-id", THEME, "--write", "--approve", dd["checksum"]], echo, sub)
        journal = open(os.path.join(sub, "journal-nl.jsonl"), encoding="utf-8").read()
        check("R18f userErrors with an attribute-hidden token: write stops, journal keeps code and field, no leak",
              code == 2 and len(echo.mutations) == 1 and '"event": "end"' not in journal and not leaked(text + files_text(sub))
              and '"INVALID"' in journal and '"value"' in journal, (code, len(echo.mutations), leaked(text + files_text(sub))))


def main():
    failures = []

    def check(name, ok, detail=""):
        print("%-66s %s%s" % (name, "pass" if ok else "FAIL", "" if ok else "  " + str(detail)[:300]))
        if not ok:
            failures.append(name)

    with tempfile.TemporaryDirectory() as folder:
        code, text, fake, d = dry(folder)
        check("dry run exits 0", code == 0, text)
        if code != 0:
            print("%d failures" % (len(failures)))
            sys.exit(1)
        rows = {}
        for r in d["rows"]:
            rows.setdefault(r["id"], []).append(r)
        ops = {(o["action"], o["resource"], o["key"]): o for o in d["ops"]}
        res = lambda i: rows[i][0]["result"] if i in rows else None
        check("dry run sends no mutation", not fake.mutations)
        check("basic: machine NL is overwritten, old NL in the snapshot",
              res("hero") == "overwrite" and ops[("register", IDX, "section.hero.heading:ab")]["current"]["value"] == "Uw mond heeft een ritme")
        check("basic: card_2 by its hints", ("register", IDX, "section.cards.card_2.title:cc") in ops and ("register", IDX, "section.cards.card_1.title:bb") not in ops)
        check("basic: held item left out", "held" not in rows)
        check("wave 2a: a selling plan's name is registered (no longer skipped for Loop)", res("sp") == "new"
              and ("register", "gid://shopify/SellingPlan/5", "name") in ops)
        check("basic: split body assembled in order",
              ops.get(("register", "gid://shopify/Page/7", "body_html"), {}).get("value") == "<p>Eerste blok.</p><p>Tweede blok.</p>")
        check("basic: bound metaobject field through the product's reference", ("register", "gid://shopify/Metaobject/700", "role") in ops
              and ("register", "gid://shopify/Metaobject/701", "role") not in ops)
        code_b, _, _, db = dry(folder, bindings=None)
        prop = json.load(open(os.path.join(folder, "bindings-proposed-nl.json"), encoding="utf-8"))["bindings"]
        check("R18b-B an unbound metaobject item is proposed, not written", code_b == 0
              and not any(o["resource"].startswith("gid://shopify/Metaobject/700") for o in db["ops"])
              and prop.get("role", {}).get("key") == "role")
        store = base_store()
        mo = next(n for n in store["types"]["METAOBJECT"] if n["resourceId"] == "gid://shopify/Metaobject/700")
        mo["translatableContent"] = [c("role", "Changed live role"), c("other_field", "Pharmacist"), c("name", "Sietske")]
        _, _, _, dbb = dry(folder, store)
        check("R18b-B a bound field with changed EN is stale, never another field",
              not any(o["key"] == "other_field" for o in dbb["ops"]) and any(r["id"] == "role" and r["result"] == "stale" for r in dbb["rows"]))
        stale_binding = {"role": dict(ROLE_BINDING["role"], en_sha1=sha1("older EN"))}
        _, _, _, dsb = dry(folder, bindings=stale_binding)
        check("R18b-B a binding made for another EN is not used", not any(o["resource"] == "gid://shopify/Metaobject/700" for o in dsb["ops"]))
        code_c, text_c, _, _ = dry(folder, argv=("--lang", "nl", "--theme-id", "222"))
        check("R18b-C a theme ID that is not the published one stops the run", code_c == 2 and "not the published theme" in text_c, text_c)
        code_c, text_c, _, _ = dry(folder, argv=("--lang", "nl", "--theme-id", "111x"))
        check("R18b-C a non-numeric theme ID stops the run", code_c == 2, text_c)
        check("R18b-C only the exact theme parameter proves ownership",
              not register.theme_owned("gid://shopify/OnlineStoreThemeJsonTemplate/index?previous_theme_id=111", "111", "index")
              and register.theme_owned(IDX, "111", "index"))
        code_c, text_c, _, _ = dry(folder, main_theme="denied")
        check("R18b-C without read_themes an attestation is required", code_c == 2 and "--theme-attested" in text_c, text_c)
        today = __import__("time").strftime("%Y-%m-%d")
        code_c, _, _, dc = dry(folder, argv=("--lang", "nl", "--theme-id", THEME, "--theme-attested", today + " Victor"), main_theme="denied")
        check("R18b-C a same-day attestation is accepted and bound to the approval", code_c == 0 and dc["snapshot"]["theme_proof"] == "operator: %s Victor" % today)
        code_c, _, _, _ = dry(folder, argv=("--lang", "nl", "--theme-id", THEME, "--theme-attested", "2026-01-01 Victor"), main_theme="denied")
        check("R18b-C an old attestation is refused", code_c == 2)
        check("R18b-C the read proof is bound to the approval", d["snapshot"]["theme_proof"] == "read: themes(roles: MAIN)")
        check("R18b-D a held leaf under a structural-looking key keeps the field whole",
              ("register", "gid://shopify/Metafield/13", "value") not in ops and rows["fl1"][0]["result"] == "not written")
        jop = ops.get(("register", "gid://shopify/Metafield/9", "value"), {})
        check("R18b-D a structural value that differs from the current NL is shown", any("url" in n and "nl/a" in n for n in jop.get("notes", [])), jop.get("notes"))
        check("R18b-N2 a string root is translated", ops.get(("register", "gid://shopify/Metafield/14", "value"), {}).get("value") == json.dumps("Hallo"))
        check("R18b-N2 an array root is translated", ops.get(("register", "gid://shopify/Metafield/18", "value"), {}).get("value") == json.dumps(["Hallo", "Hallo"]))
        check("R18b-N2 number, bool and null roots are left alone", not any(o["resource"] in ("gid://shopify/Metafield/15", "gid://shopify/Metafield/16",
                                                                                            "gid://shopify/Metafield/17") for o in d["ops"]))
        check("basic: equal translation counts as same, no operation", res("alt") == "same"
              and not any(o["resource"] == "gid://shopify/MediaImage/3" for o in d["ops"]))
        check("F2 failed hints never fall back to equal EN elsewhere", res("cardX") == "missing")
        pdp_op = ops.get(("register", PDP, "section.other.x.title:zz"))
        check("F2 a stale item never takes an equal EN on another template", res("faq") == "stale"
              and pdp_op is not None and pdp_op["items"] == ["other-template"], pdp_op)
        check("F2 changed live EN is stale", res("faq") == "stale" and ("register", IDX, "section.faq.q1.question:dd") not in ops)
        check("F2 two keys pass identity: ambiguous, not written", res("gift1") == "ambiguous"
              and not any(k[2].startswith("section.gift") for k in ops))
        conflict_plan = base_plan()
        conflict_plan["resources"][0]["items"].append(item("card2b", "Begin", "Start", hint=["cards", "card_2", "title"]))
        fake2 = Fake(base_store())
        run(["--lang", "nl", "--theme-id", THEME], fake2, folder, conflict_plan)
        d2 = json.load(open(os.path.join(folder, "dry-run-nl.json"), encoding="utf-8"))
        check("F2 two plan items, two values, one target: conflict, not written",
              any(r["result"] == "conflict" for r in d2["rows"]) and not any(o["key"] == "section.cards.card_2.title:cc" for o in d2["ops"]))
        check("F3 only the published theme's template is a target", not any(o["resource"] == IDX_OTHER for o in d["ops"]))
        code3, _, _, d3 = dry(folder, argv=("--lang", "nl"))
        check("F3 without --theme-id theme items are not written", code3 == 0 and res("hero") and
              not any("OnlineStoreTheme" in o["resource"] for o in d3["ops"]))
        check("F4 an allowed label never lands on handle_item", res("yearlabel") == "not written"
              and not any(o["key"].endswith("handle_item:gg") and o["action"] == "register" for o in d["ops"]))
        check("F4 a Subscription Name value is never registered", res("supply") == "not written"
              and not any(o["resource"] == "gid://shopify/Product/2" for o in d["ops"]))
        check("F4 a selling-plan GID under another type is never registered", res("disguised") == "not written")
        check("F4 removals proposed but not approved without --remove-never", not any(o["action"] == "remove" for o in d["ops"]))
        code4, _, _, d4 = dry(folder, argv=("--lang", "nl", "--theme-id", THEME, "--remove-never"))
        removes = {(o["resource"], o["key"]) for o in d4["ops"] if o["action"] == "remove"}
        check("F4/F3 removals: metaobject + published theme only", removes == {("gid://shopify/Metaobject/515475276157", "handle_item"),
                                                                               (PDP, "section.compare.handle_item:hh")}, removes)
        check("F4 register and remove sets do not overlap",
              not ({(o["resource"], o["key"]) for o in d4["ops"] if o["action"] == "register"} & removes))
        check("F5 a JSON field with a held segment is kept whole", ("register", "gid://shopify/Metafield/10", "value") not in ops
              and rows["f1"][0]["result"] == "not written" and "held segment" in rows["f1"][0]["why"])
        journey = ops.get(("register", "gid://shopify/Metafield/9", "value"))
        check("F5/F6 every leaf mapped: JSON field written by path, price too", journey is not None and
              [x.get("value") for x in json.loads(journey["value"])["children"]] == ["Wat je voelt", "Gratis", "€0,49", None]
              and json.loads(journey["value"])["children"][3] == {"type": "link", "url": "https://karmicare.com/a",
                                                                  "children": [{"type": "text", "value": "Gratis"}]}, journey)
        tricky = ops.get(("register", "gid://shopify/Metafield/11", "value"))
        tv = json.loads(tricky["value"]) if tricky else {}
        check("F6 object keys stay, values translated in one pass", tv.get("Free") == "Gratis" and "Gratis" not in tv, tv)
        check("F6 no chained translation (Hello->Hallo, Hallo->Bonjour)", tv.get("list") == ["Hallo", "Bonjour"], tv)
        check("F6 \\u-escaped EN matches as a decoded string", tv.get("name") == "koffiehuis" and tv.get("url") == "https://x.test/b", tv)
        md = open(os.path.join(folder, "dry-run-nl.md"), encoding="utf-8").read()
        dry(folder)
        md = open(os.path.join(folder, "dry-run-nl.md"), encoding="utf-8").read()
        check("F8 a long value is shown whole", "EINDE-SUFFIX" in md)
        check("F8 every mutation names its resource and key", "`%s` · `section.long.l1.text:ff`" % IDX in md)
        check("F8 menu link reported as owner not proven", res("link") == "not written" and "owner not proven" in rows["link"][0]["why"])
        check("F10 a null content value does not stop the scan", ("register", IDX, "section.hero.heading:ab") in ops)

        # F1: approval binds the current translations
        store = base_store()
        store["types"]["ONLINE_STORE_THEME_JSON_TEMPLATE"][0]["translations"]["nl"][0]["value"] = "Changed by editor"
        fake = Fake(store)
        code, text = run(["--lang", "nl", "--theme-id", THEME, "--write", "--approve", d["checksum"]], fake, folder)
        check("F1 an edited NL after approval: write stops, zero mutations", code == 2 and not fake.mutations, text)
        store = base_store()
        store["types"]["METAOBJECT"][0]["translations"]["nl"][1]["value"] = "edited"
        fake = Fake(store)
        code, text = run(["--lang", "nl", "--theme-id", THEME, "--remove-never", "--write", "--approve", d4["checksum"]], fake, folder)
        check("F1 an edited translation set for removal: write stops", code == 2 and not fake.mutations, text)
        fake = Fake(base_store())
        code, text = run(["--lang", "nl", "--theme-id", THEME, "--remove-never", "--write", "--approve", d["checksum"]], fake, folder)
        check("F1 the removal choice is part of the approval", code == 2 and not fake.mutations, text)
        live = register.Live(register.Admin(Fake(base_store()), "client-id", register.Secret(SECRET)), "nl")
        ops_list, _, _ = register.build(base_plan(), live, THEME, False)
        live.admin.transport.store["types"]["ONLINE_STORE_THEME_JSON_TEMPLATE"][0]["translations"]["nl"][0]["value"] = "raced"
        ok, _ = register.preconditions_hold(live, [o for o in ops_list if o["key"] == "section.hero.heading:ab"])
        check("F1 the re-read right before a mutation catches a change", not ok)
        fake = Fake(base_store())
        code, text = run(["--lang", "nl", "--theme-id", THEME, "--write", "--approve", d["checksum"]], fake, folder)
        regs = [m for m in fake.mutations if m[0] == "register"]
        check("write: approved snapshot registers every register op", code == 0 and sum(len(m[2]) for m in regs) == len(d["ops"]), text)
        check("write: every translation carries locale nl and its digest",
              all(t["locale"] == "nl" and t["translatableContentDigest"].startswith("d-") for m in regs for t in m[2]))
        fake = Fake(base_store(), scope=None)
        code, text = run(["--lang", "nl", "--theme-id", THEME, "--write", "--approve", d["checksum"]], fake, folder)
        check("write refused when the token shows no scope", code == 2 and not fake.mutations, text)

        # F9: journal keeps confirmed writes when a later mutation fails
        saved = register.REGISTER_CHUNK
        register.REGISTER_CHUNK = 1
        for name in os.listdir(folder):
            if name.startswith("journal"):
                os.remove(os.path.join(folder, name))
        fake = Fake(base_store(), mutation_status=lambda n: 500 if n == 2 else None)
        code, text = run(["--lang", "nl", "--theme-id", THEME, "--write", "--approve", d["checksum"]], fake, folder)
        register.REGISTER_CHUNK = saved
        journal = [json.loads(l) for l in open(os.path.join(folder, "journal-nl.jsonl"), encoding="utf-8")]
        results = [j for j in journal if j["event"] == "result"]
        check("F9 a failure after a confirmed chunk stops the run", code == 2 and len(fake.mutations) == 2, text)
        check("F9 the journal keeps the confirmed chunk and marks the next unknown",
              len(results) == 2 and results[0]["state"] == "confirmed" and results[0]["confirmed"] and results[1]["state"] == "unknown", results)

        # R18b-N1: a null or incomplete mutation payload is unknown, stops the run and writes no end record
        class Hollow(Fake):
            def __init__(self, store, mode):
                super().__init__(store)
                self.mode = mode

            def post(self, path, body, headers):
                if "translationsRegister" in body.get("query", ""):
                    self.mutations.append(("register", body["variables"]["id"], body["variables"]["translations"]))
                    payload = None if self.mode == "null" else {"translations": [], "userErrors": []}
                    return 200, {"data": {"translationsRegister": payload}}, None
                return super().post(path, body, headers)
        for mode in ("null", "empty"):
            os.remove(os.path.join(folder, "journal-nl.jsonl"))
            fake = Hollow(base_store(), mode)
            code, text = run(["--lang", "nl", "--theme-id", THEME, "--write", "--approve", d["checksum"]], fake, folder)
            journal = [json.loads(l) for l in open(os.path.join(folder, "journal-nl.jsonl"), encoding="utf-8")]
            check("R18b-N1 %s payload: unknown, stops after one call, no end record" % mode,
                  code == 2 and len(fake.mutations) == 1 and journal[-1]["event"] == "result" and journal[-1]["state"] == "unknown"
                  and not any(j["event"] == "end" for j in journal), (code, len(fake.mutations), journal[-1]))

        # R18c-2: every returned entry needs a string key and exactly the requested locale, once, nothing extra
        class Receipt(Fake):
            def __init__(self, store, action, mode):
                super().__init__(store)
                self.action, self.mode = action, mode

            def post(self, path, body, headers):
                q = body.get("query", "")
                name = "translationsRegister" if self.action == "register" else "translationsRemove"
                if name in q:
                    v = body["variables"]
                    keys = [t["key"] for t in v["translations"]] if self.action == "register" else v["keys"]
                    self.mutations.append((self.action, v["id"], keys))
                    entries = [{"key": k, "locale": "nl"} for k in keys]
                    if self.mode == "no locale":
                        entries = [{"key": k} for k in keys]
                    elif self.mode == "null locale":
                        entries = [{"key": k, "locale": None} for k in keys]
                    elif self.mode == "extra entry":
                        entries.append({"key": "unrequested", "locale": "fr"})
                    elif self.mode == "duplicate":
                        entries.append(dict(entries[0]))
                    return 200, {"data": {name: {"translations": entries, "userErrors": []}}}, None
                return super().post(path, body, headers)
        for action, check_sum, extra in (("register", d["checksum"], []), ("remove", d4["checksum"], ["--remove-never"])):
            for mode in ("no locale", "null locale", "extra entry", "duplicate"):
                os.remove(os.path.join(folder, "journal-nl.jsonl")) if os.path.exists(os.path.join(folder, "journal-nl.jsonl")) else None
                fake = Receipt(base_store(), action, mode)
                code, text = run(["--lang", "nl", "--theme-id", THEME] + extra + ["--write", "--approve", check_sum], fake, folder)
                journal = [json.loads(l) for l in open(os.path.join(folder, "journal-nl.jsonl"), encoding="utf-8")]
                bad = [m for m in fake.mutations if m[0] == action]
                check("R18c-2 %s receipt with %s: unknown, stop, no end record" % (action, mode),
                      code == 2 and len(bad) == 1 and journal[-1]["state"] == "unknown" and not any(j["event"] == "end" for j in journal),
                      (code, len(bad), journal[-1]))
        check("R18c-2 confirmation() rejects an extra null entry",
              register.confirmation("confirmed", {"translationsRegister": {"translations": [{"key": "a", "locale": "nl"}, None], "userErrors": []}},
                                    "register", ["a"], "nl")[0] == "unknown")

        # R18c-1: plan items that disagree on a structural leaf veto the field; a lone one is not counted as applied
        p1 = base_plan()
        meta = next(r for r in p1["resources"] if r["shopify_type"] == "METAFIELD")
        meta["items"] += [item("u1", "https://karmicare.com/a", "https://karmicare.com/nl/a", key="value", field="custom.treatment_journey_*#05"),
                          item("u2", "https://karmicare.com/a", "https://karmicare.com/nl/b", key="value", field="custom.treatment_journey_*#06")]
        run(["--lang", "nl", "--theme-id", THEME], Fake(base_store()), folder, p1)
        d5 = json.load(open(os.path.join(folder, "dry-run-nl.json"), encoding="utf-8"))
        r5 = {r["id"]: r for r in d5["rows"]}
        check("R18c-1 conflicting items on a structural URL keep the field whole",
              not any(o["resource"] == "gid://shopify/Metafield/9" for o in d5["ops"]) and "conflicting" in r5["j1"].get("why", ""), r5.get("j1"))
        p2 = base_plan()
        meta = next(r for r in p2["resources"] if r["shopify_type"] == "METAFIELD")
        meta["items"].append(item("u1", "https://karmicare.com/a", "https://karmicare.com/nl/a", key="value", field="custom.treatment_journey_*#05"))
        run(["--lang", "nl", "--theme-id", THEME], Fake(base_store()), folder, p2)
        d6 = json.load(open(os.path.join(folder, "dry-run-nl.json"), encoding="utf-8"))
        op6 = next((o for o in d6["ops"] if o["resource"] == "gid://shopify/Metafield/9"), None)
        r6 = {r["id"]: r for r in d6["rows"]}
        check("R18c-1 a lone structural item is not credited as applied", op6 is not None and "u1" not in op6["items"]
              and "https://karmicare.com/a" in op6["value"] and r6["u1"]["result"] == "not written", (op6 and op6["items"], r6.get("u1")))

        # R18c-3: the generated command reproduces the exact arguments in a shell; the attestation needs a name
        today = __import__("time").strftime("%Y-%m-%d")
        nasty = today + " Reviewer $(printf R18C_SENTINEL) `echo tick` \"dq\" 'sq' \\back"
        cmd = register.write_command("nl", THEME, nasty, True, "abc123")
        argv = register.write_argv("nl", THEME, nasty, True, "abc123")
        import shlex
        import subprocess
        prefix = shlex.join(["python3", "docs/localization/registration/register.py"])
        captured = subprocess.run(["/bin/sh", "-c", "printf '%s\\0' " + cmd[len(prefix):]], capture_output=True, text=True).stdout.split("\0")[:-1]
        check("R18c-3 the write command round-trips quotes, $() and backticks", cmd.startswith(prefix) and captured == argv, captured)
        code_c, _, _, _ = dry(folder, argv=("--lang", "nl", "--theme-id", THEME, "--theme-attested", today), main_theme="denied")
        check("R18c-3 an attestation without a name is refused", code_c == 2)

        # R18b-A: a resource the re-read omits fails the precondition, zero mutations
        fake = Fake(base_store())
        live = register.Live(register.Admin(fake, "client-id", register.Secret(SECRET)), "nl")
        a_ops, _, _ = register.build(base_plan(), live, THEME, False, ROLE_BINDING)
        hero = [o for o in a_ops if o["key"] == "section.hero.heading:ab"]
        fake.store["types"]["ONLINE_STORE_THEME_JSON_TEMPLATE"] = [n for n in fake.store["types"]["ONLINE_STORE_THEME_JSON_TEMPLATE"] if n["resourceId"] != IDX]
        ok, why = register.preconditions_hold(live, hero)
        check("R18b-A a resource missing from the re-read fails the precondition", not ok and "not returned" in (why or ""), why)
        try:
            with tempfile.TemporaryDirectory() as sub:
                register.write(live.admin, live, "nl", hero, register.Journal(os.path.join(sub, "j.jsonl"), "t"))
            stopped = False
        except register.RunnerError:
            stopped = True
        check("R18b-A write sends zero mutations for it", stopped and not fake.mutations)

        # F7: dummy secret and token never leave the process
        leaks = []
        for name, hooks in (("token refused", {"token_status": 401}), ("GraphQL error echoes the token", {"graphql_error": True}),
                            ("transport failure", {"raise_on": lambda b: True})):
            with tempfile.TemporaryDirectory() as sub:
                code, text = run(["--lang", "nl", "--theme-id", THEME], Fake(base_store(), **hooks), sub)
                if code == 0 or SECRET in text or TOKEN in text or SECRET in files_text(sub) or TOKEN in files_text(sub):
                    leaks.append(name)
        with tempfile.TemporaryDirectory() as sub:
            code, _, _, dd = dry(sub)
            code, text = run(["--lang", "nl", "--theme-id", THEME, "--write", "--approve", dd["checksum"]], Fake(base_store(), user_error=True), sub)
            if code == 0 or TOKEN in text or TOKEN in files_text(sub):
                leaks.append("userErrors echo the token")
        check("F7 no secret or token on any error path (4 cases)", not leaks, leaks)
        check("F7 scrub removes registered secrets and token shapes",
              register.scrub({"a": ["x " + SECRET, "shpca_ABCDEFGH1234"]}) == {"a": ["x [redacted]", "[redacted]"]})
        try:
            raise register.RunnerError("boom " + TOKEN)
        except register.RunnerError as e:
            check("F7 RunnerError messages are scrubbed", TOKEN not in str(e))
        check("F7 no secret or token in the normal files", SECRET not in files_text(folder) and TOKEN not in files_text(folder))
        check("Secret hides its value in repr and str", SECRET not in repr(register.Secret(SECRET)) + str(register.Secret(SECRET)))

        # F10 / malformed responses
        store = base_store()
        long_c = next(x for x in store["types"]["ONLINE_STORE_THEME_JSON_TEMPLATE"][0]["translatableContent"] if x["key"] == "section.long.l1.text:ff")
        long_c["digest"] = None
        code, _, _, d10 = dry(folder, store)
        check("F10 content without digest is never an operation", code == 0 and ("register", IDX, "section.long.l1.text:ff") in ops
              and not any(o["key"] == "section.long.l1.text:ff" for o in d10["ops"]))

        class Broken(Fake):
            def post(self, path, body, headers):
                if "translatableResources(" in body.get("query", ""):
                    return 200, {"data": {"translatableResources": {"nodes": "oops"}}}, None
                return super().post(path, body, headers)
        with tempfile.TemporaryDirectory() as sub:
            code, text = run(["--lang", "nl", "--theme-id", THEME], Broken(base_store()), sub)
            check("F10 a malformed page stops with a clean message", code == 2 and "malformed" in text, text)

    r18e(check)
    wave2a(check)
    print("%d failures" % len(failures))
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
