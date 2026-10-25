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


# ---- wave 2b: metaobject fields through typed references, field proposals and reviewed field bindings ----------

REF = "list.metaobject_reference"
ONE = "metaobject_reference"
TXT = "single_line_text_field"
MTXT = "multi_line_text_field"
MO = lambda n: "gid://shopify/Metaobject/%s" % n


def w2b_objects(**overrides):
    objs = {
        MO(800): ("faq_item", "how-to-use", {"title": (TXT, "How to use"), "steps": (REF, json.dumps([MO(802)])),
                                              "section_content": (MTXT, '<div class="bf-step"><b>One pump</b> Full dose</div><p>Leave it on &amp; relax</p>')}),
        MO(801): ("faq_item", "quality", {"title": (TXT, "Quality")}),
        MO(802): ("faq_step", "step-1", {"text": (TXT, "Step one")}),
        MO(810): ("table", "main-table", {"compare_plans": (REF, json.dumps([MO(830)])), "compare_rows": (REF, json.dumps([MO(840)]))}),
        MO(830): ("plan", "rhythm", {"name": (TXT, "Rhythm plan")}),
        MO(840): ("row", "shipping", {"label": (TXT, "Shipping")}),
        MO(820): ("compare_value", "cell-rhythm-shipping", {"value": (TXT, "Free"), "compare_plan": (ONE, MO(830)), "compare_row": (ONE, MO(840))}),
        MO(821): ("compare_value", "cell-other", {"value": (TXT, "Free"), "compare_plan": (ONE, MO(831)), "compare_row": (ONE, MO(840))}),
    }
    for gid, change in overrides.items():
        typ, handle, fields = objs[MO(gid)]
        objs[MO(gid)] = (typ, handle, dict(fields, **change))
    return objs


def w2b_store(objs, roots=None):
    store = base_store()
    store["types"]["METAOBJECT"] += [{"resourceId": g, "translatableContent": [c(k, v) for k, (ft, v) in f.items() if "reference" not in ft],
                                      "translations": {}} for g, (_, _, f) in objs.items()]
    store["product_metafields"]["gid://shopify/Product/1"] += roots if roots is not None else [
        {"id": "gid://shopify/Metafield/30", "namespace": "custom", "key": "faq_items", "type": REF, "value": json.dumps([MO(800), MO(801)])},
        {"id": "gid://shopify/Metafield/31", "namespace": "custom", "key": "ct", "type": ONE, "value": MO(810)}]
    store["w2b"] = objs
    return store


class W2BFake(Fake):
    def post(self, path, body, headers):
        q, objs = body.get("query", ""), self.store.get("w2b", {})
        page = {"hasNextPage": False, "endCursor": None}
        shape = lambda g: None if g not in objs else {"id": g, "type": objs[g][0], "handle": objs[g][1],
                                                      "fields": [{"key": k, "type": ft, "value": v} for k, (ft, v) in objs[g][2].items()]}
        if path != "/admin/oauth/access_token" and "metaobjectByHandle" in q:
            v = body["variables"]
            g = next((g for g, (ty, h, _) in objs.items() if ty == v["type"] and h == v["handle"]), None)
            return 200, {"data": {"metaobjectByHandle": shape(g) if g else None}}, None
        if path != "/admin/oauth/access_token" and "metaobjects(" in q:
            nodes = [{"id": g, "handle": h} for g, (ty, h, _) in objs.items() if ty == body["variables"]["type"]]
            return 200, {"data": {"metaobjects": {"nodes": nodes, "pageInfo": page}}}, None
        if path != "/admin/oauth/access_token" and "metaobject(" in q:
            return 200, {"data": {"metaobject": shape(body["variables"]["id"])}}, None
        return super().post(path, body, headers)


def w2b_plan(extra_mf=(), extra_mo=(), hold=None):
    mf = lambda n, en, nl, **kw: item("b%s" % n, en, nl, key="value", field="custom.faq_items#%02d" % n, **kw)
    mfs = [mf(1, "How to use", "Gebruik"), mf(2, "One pump", "Eén pomp"), mf(3, "Full dose", "Volle dosis"),
           mf(4, "Leave it on & relax", "Laat het zitten & ontspan"), mf(5, "Step one", "Stap één")] + list(extra_mf)
    mos = [item("c1", "Free", "Gratis", field="custom.ct|shop.metaobjects.compare_value#01"),
           item("c2", "Shipping", "Verzending", field="custom.ct|shop.metaobjects.compare_value#02")] + list(extra_mo)
    return {"lang": "nl", "resources": [{"shopify_type": "METAFIELD", "owner": "duo", "items": mfs},
                                        {"shopify_type": "METAOBJECT", "owner": "duo", "items": mos}]}


SHOP_OK = {"objects": {"compare_value": [{"handle": "cell-rhythm-shipping", "gid": MO(820), "match": {"compare_plan": "compare_plans", "compare_row": "compare_rows"}},
                                {"handle": "cell-other", "gid": MO(821), "match": {"compare_plan": "compare_plans", "compare_row": "compare_rows"}}]}}


def run2b(store, plan, field_bindings=None, shop=None, item_bindings=None, argv=("--lang", "nl", "--theme-id", THEME), fake=None):
    """main() on the wave 2b fixtures: (exit code, output, dry-run JSON or None, fields-proposed JSON or None, fake)."""
    with tempfile.TemporaryDirectory() as sub:
        fb, so = os.path.join(sub, "bindings-fields.json"), os.path.join(sub, "shop-objects.json")
        if field_bindings is not None:
            json.dump({"bindings": {"nl": field_bindings}}, open(fb, "w", encoding="utf-8"))
        if shop is not None:
            json.dump(shop, open(so, "w", encoding="utf-8"))
        json.dump(plan, open(os.path.join(sub, "plan-nl.json"), "w", encoding="utf-8"))
        bp = os.path.join(sub, "bindings.json")
        if item_bindings:
            json.dump({"bindings": item_bindings}, open(bp, "w", encoding="utf-8"))
        fake = fake or W2BFake(store)
        extra = {"field_bindings_path": fb, "shop_objects_path": so} if "field_bindings_path" in register.main.__code__.co_varnames else {}
        out = io.StringIO()
        code = 0
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(out):
            try:
                register.main(list(argv), transport=fake, credentials=lambda: ("client-id", register.Secret(SECRET)), out=sub,
                              plans=os.path.join(sub, "plan-%s.json"), bindings_path=bp, **extra)
            except SystemExit as e:
                code = e.code if isinstance(e.code, int) else 1
        load = lambda n: json.load(open(os.path.join(sub, n), encoding="utf-8")) if os.path.exists(os.path.join(sub, n)) else None
        return code, out.getvalue(), load("dry-run-nl.json"), load("fields-proposed-nl.json"), fake


def bind(props, *fkeys):
    """Reviewed field bindings made from proposals, as a reviewer would copy them."""
    out = {}
    for k in [k for k in fkeys if k in props]:
        ev = {x: v for x, v in props[k].items() if x not in ("current", "proposal_hash")}
        out[k] = {"proposal_hash": props[k]["proposal_hash"], "evidence": ev}
    return out


def proposed(objs=None, plan=None, roots=None, **kw):
    code, text, d, f, _ = run2b(w2b_store(objs or w2b_objects(), roots), plan or w2b_plan(), **kw)
    WROTE.clear()
    WROTE.update("%s|%s" % (o["resource"], o["key"]) for o in (d or {}).get("ops", []))
    return code, text, d, (f or {}).get("proposals", {}), (f or {}).get("exceptions", [])


WROTE = set()  # resource|key of the operations of the last proposed() run: never a metaobject field without a binding


def wave2b(check):
    code, text, d, props, exc = proposed(shop=SHOP_OK)
    check("2b: dry run exits 0 and writes no metaobject field without a binding", code == 0
          and not any("Metaobject" in o["resource"] for o in d["ops"]), text)
    sc = props.get(MO(800) + "|section_content", {})
    check("2b: an HTML field is proposed span by span, tags and entities kept",
          sc.get("assembled") == '<div class="bf-step"><b>Eén pomp</b> Volle dosis</div><p>Laat het zitten &amp; ontspan</p>', sc.get("assembled"))
    check("2b: plain fields of referenced and nested objects are proposed", props.get(MO(800) + "|title", {}).get("assembled") == "Gebruik"
          and props.get(MO(802) + "|text", {}).get("assembled") == "Stap één")
    check("2b: a proposal carries its typed path, spans and proposal hash",
          [e["via"] for e in (props.get(MO(802) + "|text", {}).get("paths") or [[]])[0]] == ["custom.faq_items", "steps"]
          and (props.get(MO(800) + "|section_content", {}).get("spans") or [{}])[0].get("items") == ["b2"]
          and len(props.get(MO(800) + "|title", {}).get("proposal_hash", "")) == 64)
    check("2b: the reviewed shop object selected by the product's table is proposed; another plan's cell is not",
          MO(820) + "|value" in props and MO(821) + "|value" not in props and MO(840) + "|label" in props, sorted(props))
    _, _, _, props_noshop, _ = proposed()
    check("2b: without the reviewed shop-object list no shop-level cell is proposed", MO(820) + "|value" not in props_noshop)

    # Reviewed field bindings: written with the evidence hash; changed evidence aborts the whole write
    fb = bind(props, MO(800) + "|section_content", MO(800) + "|title")
    code, text, dbound, _, _ = run2b(w2b_store(w2b_objects()), w2b_plan(), field_bindings=fb, shop=SHOP_OK)
    sec = next((o for o in (dbound or {"ops": []})["ops"] if o["resource"] == MO(800) and o["key"] == "section_content"), None)
    check("2b: a bound field is written, its evidence hash in the approval", code == 0 and sec is not None
          and sec["value"].startswith('<div class="bf-step"><b>Eén pomp</b>')
          and any(o.get("evidence") == fb.get(MO(800) + "|section_content", {}).get("proposal_hash", "-") for o in dbound["snapshot"]["ops"]), text)
    changed = w2b_objects(**{"800": {"title": (TXT, "How to use it")}})
    code, text, dstale, fstale, _ = run2b(w2b_store(changed), w2b_plan(), field_bindings=fb, shop=SHOP_OK)
    check("2b: a bound field whose EN changed is reported stale in the dry run", code == 0 and any(s["field"] == MO(800) + "|title" for s in (fstale or {}).get("stale", [])))
    fake = W2BFake(w2b_store(changed))
    code_w, text_w, _, _, fake = run2b(None, w2b_plan(), field_bindings=fb, shop=SHOP_OK, fake=fake,
                                       argv=("--lang", "nl", "--theme-id", THEME, "--write", "--approve", (dstale or {}).get("checksum", "x")))
    check("2b: a write with a stale field binding aborts before any mutation", code_w == 2 and not fake.mutations
          and "no longer match" in text_w, text_w)
    moved = w2b_objects(**{"800": {"steps": (REF, json.dumps([]))}})
    fb2 = bind(props, MO(802) + "|text")
    _, _, _, fmoved, _ = run2b(w2b_store(moved), w2b_plan(), field_bindings=fb2, shop=SHOP_OK)
    check("2b: a bound field the product no longer reaches is stale", any(s["field"] == MO(802) + "|text" for s in (fmoved or {}).get("stale", [])))

    # R30-1: escapes from the product family and retargeting
    textroot = [{"id": "gid://shopify/Metafield/30", "namespace": "custom", "key": "faq_items", "type": TXT,
                 "value": "see %s for more" % MO(800)}]
    _, _, _, p, _ = proposed(roots=textroot)
    check("R30-1: a GID inside a text metafield is no reference", not any(k.startswith(MO(800)) for k in p) and not any(k.startswith(MO(800)) for k in WROTE), sorted(p))
    noroot = [{"id": "gid://shopify/Metafield/30", "namespace": "custom", "key": "faq_items", "type": REF, "value": json.dumps([MO(800)])}]
    _, _, _, p, _ = proposed(roots=noroot, shop=SHOP_OK)
    check("R30-1: without the table root no shop-level cell is reached", MO(820) + "|value" not in p and MO(800) + "|title" not in WROTE and MO(820) + "|value" not in WROTE, sorted(p))
    bound_item = {"b1": {"resource": MO(800), "key": "reviewed_title", "en_sha1": sha1("How to use")}}
    _, _, _, p, exc = proposed(item_bindings=bound_item)
    check("R30-1: an item bound elsewhere vetoes the field the route would propose", MO(800) + "|title" not in p and MO(800) + "|title" not in WROTE and MO(820) + "|value" not in WROTE
          and any("binding elsewhere" in "; ".join(e["reasons"]) for e in exc))
    retarget = w2b_objects(**{"800": {"title": (TXT, "Changed title"), "other_title": (TXT, "How to use")}})
    fbt = bind(props, MO(800) + "|title")
    _, _, dret, fret, _ = run2b(w2b_store(retarget), w2b_plan(), field_bindings=fbt)
    check("R30-1: a bound field never moves to a sibling with the same EN (stale, not written)",
          not any(o["key"] in ("title", "other_title") and o["resource"] == MO(800) for o in (dret or {"ops": []})["ops"])
          and any(s["field"] == MO(800) + "|title" for s in (fret or {}).get("stale", [])))

    # R30-2: held and gated siblings veto
    for label, extra in (("held", dict(hold=["legal-review"])), ("gated", {})):
        it = item("b9", "One pump", "Pomp", key="value", field="custom.faq_items#09", **extra)
        if label == "gated":
            it["gates"] = ["legal-review"]
        _, _, _, p, _ = proposed(plan=w2b_plan(extra_mf=[it]))
        check("R30-2: a %s sibling with the same EN vetoes the field" % label, MO(800) + "|section_content" not in p
              and MO(800) + "|section_content" not in WROTE)
        mo = item("c9", "Shipping", "Levering", field="custom.ct|shop.metaobjects.compare_value#09", **extra)
        if label == "gated":
            mo["gates"] = ["legal-review"]
        _, _, _, p, _ = proposed(plan=w2b_plan(extra_mo=[mo]), shop=SHOP_OK)
        check("R30-2: a %s sibling vetoes the field in the metaobject route too" % label, MO(840) + "|label" not in p
              and MO(840) + "|label" not in WROTE)

    # R30-3 / R31: markup, attributes, comments, Liquid, entities, malformed markup, split sentences
    def field_case(value, en="Free", nl="Gratis"):
        objs = w2b_objects(**{"801": {"body": (MTXT, value)}})
        _, _, _, p, exc = proposed(objs=objs, plan=w2b_plan(extra_mf=[item("bx", en, nl, key="value", field="custom.faq_items#20")]))
        if MO(801) + "|body" in WROTE:
            return "WRITTEN WITHOUT REVIEW", exc
        return p.get(MO(801) + "|body", {}).get("assembled"), exc
    out, _ = field_case('<a href="/Free" class="Free" data-x="Free">Free</a>')
    check("R30-3: href, class and data attributes stay byte for byte", out == '<a href="/Free" class="Free" data-x="Free">Gratis</a>', out)
    out, _ = field_case('<!-- Free --><p>Free</p>')
    check("R30-3: a comment stays byte for byte", out == '<!-- Free --><p>Gratis</p>', out)
    for value in ('{{ "Free" }} Free', '<p>{% if x %}Free{% endif %}</p>', json.dumps({"type": "root", "children": [{"type": "text", "value": "{{ Free }}"}]})):
        out, exc = field_case(value)
        check("R31: a Liquid-bearing field is not proposed (%s)" % value[:18], out is None and any("Liquid" in "; ".join(e["reasons"]) for e in exc))
    out, _ = field_case("<p>Free &amp; easy</p>", en="Free & easy", nl="Gratis & makkelijk")
    check("R31: an entity is decoded for matching and the translation re-escaped", out == "<p>Gratis &amp; makkelijk</p>", out)
    for value, why in (("<p>Free</p", "unclosed tag"), ("<p>Free></p>", "stray >"), ("<!-- Free <p>Free</p>", "unterminated comment"),
                       ("<p>Free &bogus; </p>", "bad entity"), ("<script>Free</script>", "script")):
        out, _ = field_case(value)
        check("R31: malformed markup is not proposed (%s)" % why, out is None, out)
    out, exc = field_case("<p>Leave it <b>on</b> &amp; relax</p>", en="Leave it on & relax", nl="Laat het zitten & ontspan")
    check("R31: a sentence split by inline markup is reported, not proposed", out is None
          and any("split sentence" in "; ".join(e["reasons"]) for e in exc))
    for value, why in (("<p>Free 健康</p>", "CJK"), ("<p>Free υγεία</p>", "Greek"), ("<p>Free здоровье</p>", "Cyrillic"),
                       ("<p>Free</p><p>Café</p>", "combining mark"), ("<p>Free</p><p>★</p>", "symbol"), ("<p>Free</p><p>🙂</p>", "emoji")):
        out, _ = field_case(value)
        check("R30-4: unmapped %s text keeps the field unproposed" % why, out is None, out)


SHOP_820 = {"objects": {"compare_value": [SHOP_OK["objects"]["compare_value"][0]]}}
WRITE = ("--lang", "nl", "--theme-id", THEME, "--write", "--approve")


def bound_write(objs, plan, key, shop=None, item_bindings=None, change=None, plan_after=None, fake=None, prep=None, roots=None):
    """A reviewer binds the clean proposal of key (a list binds several) and approves the bound dry run; then the
    store changes (change(store)) or the plan does, and the write runs with the approved checksum:
    (proposed, write exit, mutations, output, stale). prep(store) sets up every store, roots replaces the product's."""
    def make():
        store = w2b_store(copy.deepcopy(objs), copy.deepcopy(roots))
        if prep:
            prep(store)
        return store
    _, _, _, f, _ = run2b(make(), plan, shop=shop, item_bindings=item_bindings)
    props = (f or {}).get("proposals", {})
    keys = key if isinstance(key, list) else [key]
    if not all(k in props for k in keys):
        return False, None, None, "", []
    fb = bind(props, *keys)
    _, _, d, _, _ = run2b(make(), plan, shop=shop, item_bindings=item_bindings, field_bindings=fb)
    store = make()
    if change:
        change(store)
    _, _, _, fafter, _ = run2b(copy.deepcopy(store), plan_after or plan, shop=shop, item_bindings=item_bindings, field_bindings=fb)
    fake = fake(store) if fake else W2BFake(store)
    code, text, _, _, fake = run2b(None, plan_after or plan, shop=shop, item_bindings=item_bindings, field_bindings=fb, fake=fake,
                                   argv=WRITE + ((d or {}).get("checksum", "x"),))
    return True, code, len(fake.mutations), text, (fafter or {}).get("stale", [])


def set_object(gid, _handle=None, **fields):
    def change(store):
        typ, handle, old = store["w2b"][MO(gid)]
        store["w2b"][MO(gid)] = (typ, _handle or handle, dict(old, **fields))
    return change


def r32(check):
    """R32 regressions: each one fails against the first wave 2b candidate (negative proof in the notes)."""
    cell = MO(820) + "|value"
    # 821's row is outside the table, so moving 820 to plan 831 tests the evidence, not the uniqueness check (C6)
    two_plans = w2b_objects(**{"810": {"compare_plans": (REF, json.dumps([MO(830), MO(831)]))}, "821": {"compare_row": (ONE, MO(841))}})
    two_plans[MO(831)] = ("plan", "year", {"name": (TXT, "Year plan")})

    # R32-1: the storefront selection, root and intermediate identities are part of the evidence
    ok, code, muts, text, stale = bound_write(two_plans, w2b_plan(), cell, shop=SHOP_820, change=set_object(820, compare_plan=(ONE, MO(831))))
    check("R32-1: a cell moved to another valid plan of the table is stale; the old approval writes nothing",
          ok and code == 2 and muts == 0 and any(s["field"] == cell and "evidence differs" in s["why"] for s in stale), (ok, code, muts, stale))
    ok, code, muts, text, stale = bound_write(two_plans, w2b_plan(), cell, shop=SHOP_820, change=set_object(820, compare_plan=(TXT, MO(830))))
    check("R32-1: a cell whose plan reference becomes plain text is no longer selected; nothing written",
          ok and code == 2 and muts == 0 and any(s["field"] == cell for s in stale), (ok, code, muts, stale))
    ok, code, muts, text, stale = bound_write(w2b_objects(), w2b_plan(), cell, shop=SHOP_820,
                                              change=set_object(810, compare_plans=(REF, json.dumps([MO(830), MO(831)]))))
    check("R32-1: a change to the table's plan list is stale for its cells", ok and code == 2 and muts == 0
          and any(s["field"] == cell for s in stale), (ok, code, muts, stale))
    out_row = w2b_objects(**{"820": {"compare_row": (ONE, MO(999))}})
    _, _, _, p, _ = proposed(objs=out_row, shop=SHOP_OK)
    check("R32-1: a cell whose row is not in the table is not selected", cell not in p and cell not in WROTE, sorted(p))
    weak = {"objects": {"compare_value": [dict(SHOP_OK["objects"]["compare_value"][0], match={"compare_plan": "compare_plans"})]}}
    code, text, _, _, fake = run2b(w2b_store(w2b_objects()), w2b_plan(), shop=weak)
    check("R32-1: a shop-objects entry without the full storefront selector is refused", code == 2 and "storefront selector" in text
          and not fake.mutations, text)
    other = {"objects": {"compare_plan": [{"handle": "rhythm", "gid": MO(830), "match": {"compare_plan": "compare_plans"}}]}}
    code, text, _, _, _ = run2b(w2b_store(w2b_objects()), w2b_plan(), shop=other)
    check("R32-1: a shop-level type without a known storefront selector is refused", code == 2 and "storefront selector" in text, text)
    twice = w2b_objects(**{"821": {"compare_plan": (ONE, MO(830))}})
    _, _, _, p, exc = proposed(objs=twice, shop=SHOP_OK)
    check("R32-1: two reviewed cells with the same selection are both blocked", cell not in p and MO(821) + "|value" not in p
          and any("selected twice" in "; ".join(e["reasons"]) for e in exc), sorted(p))
    ok, code, muts, text, stale = bound_write(w2b_objects(), w2b_plan(), MO(802) + "|text", change=set_object(800, _handle="renamed-faq"))
    check("R32-1: a changed intermediate handle is stale; nothing written", ok and code == 2 and muts == 0
          and any(s["field"] == MO(802) + "|text" for s in stale), (ok, code, muts, stale))

    def new_root_gid(store):
        next(m for m in store["product_metafields"]["gid://shopify/Product/1"] if m["key"] == "faq_items")["id"] = "gid://shopify/Metafield/999"
    ok, code, muts, text, stale = bound_write(w2b_objects(), w2b_plan(), MO(802) + "|text", change=new_root_gid)
    check("R32-1: a replaced root metafield (same key and value) is stale; nothing written", ok and code == 2 and muts == 0
          and any(s["field"] == MO(802) + "|text" for s in stale), (ok, code, muts, stale))
    shared = w2b_objects(**{"801": {"steps": (REF, json.dumps([MO(802)]))}})
    _, _, _, p, _ = proposed(objs=shared)
    paths = p.get(MO(802) + "|text", {}).get("paths") or []
    check("R32-1: every path found to a shared object is kept, with each destination's type and handle",
          len(paths) == 2 and all(e.get("to_handle") for path in paths for e in path) and paths[0][0].get("metafield") == "gid://shopify/Metafield/30",
          paths)
    _, _, _, p, _ = proposed(shop=SHOP_OK)
    sel = next((e for path in p.get(cell, {}).get("paths") or [] for e in path if e["type"] == "selection"), {})
    check("R32-1: the selection edge records the pinned entry, the resolved plan and row and the table members",
          sel.get("pinned") == {"handle": "cell-rhythm-shipping", "gid": MO(820)}
          and [(s["cell_field"], s["value"], s["table_members"]) for s in sel.get("selector", [])]
          == [("compare_plan", MO(830), [MO(830)]), ("compare_row", MO(840), [MO(840)])], sel)

    # R32-2: legacy-bound, held, gated and conflicting rows veto in both routes, structural JSON leaves included
    label = MO(840) + "|label"
    for status in ("hold", "gates", "conflict"):
        sib = item("c9", "Shipping", "Anders", field="custom.ct|shop.metaobjects.compare_value#09")
        if status != "conflict":
            sib[status] = ["legal-review"]
        ib = {"c9": {"resource": MO(999), "key": "elsewhere", "en_sha1": sha1("Shipping")}}
        _, _, _, p, _ = proposed(plan=w2b_plan(extra_mo=[sib]), shop=SHOP_OK, item_bindings=ib)
        ok, code, muts, text, stale = bound_write(w2b_objects(), w2b_plan(), label, shop=SHOP_OK, item_bindings=ib,
                                                  plan_after=w2b_plan(extra_mo=[sib]))
        check("R32-2: a legacy-bound %s sibling vetoes the field; a binding made before writes nothing" % status,
              label not in p and ok and code == 2 and muts == 0, (sorted(p), ok, code, muts))
    own = {"c2": {"resource": MO(840), "key": "label", "en_sha1": sha1("Shipping")}}
    _, _, d, p, exc = proposed(item_bindings=own)
    check("R32-2: a field a legacy item is bound to stays with that route (written once, not proposed again)",
          label not in p and any(o["resource"] == MO(840) and o["key"] == "label" and "bindings.json" in o["how"] for o in d["ops"])
          and not any(e["field"] == label for e in exc), (sorted(p), exc))
    rich = json.dumps({"type": "root", "children": [{"type": "text", "value": "Free"}, {"type": "link", "url": "Held claim", "children": []}]})
    free = item("bx", "Free", "Gratis", key="value", field="custom.faq_items#20")
    for status in ("hold", "gates"):
        claim = item("hc", "Held claim", "Vastgehouden", key="value", field="custom.faq_items#21")
        claim[status] = ["legal-review"]
        objs = w2b_objects(**{"801": {"body": (MTXT, rich)}})
        _, _, _, p, exc = proposed(objs=objs, plan=w2b_plan(extra_mf=[free, claim]))
        ok, code, muts, text, stale = bound_write(objs, w2b_plan(extra_mf=[free]), MO(801) + "|body", plan_after=w2b_plan(extra_mf=[free, claim]))
        check("R32-2: a %s row on a structural JSON leaf vetoes the field; a binding made before writes nothing" % status,
              MO(801) + "|body" not in p and any("held segment" in "; ".join(e["reasons"]) for e in exc) and ok and code == 2 and muts == 0,
              (sorted(p), ok, code, muts))

    # R32-3: quote-aware tags; uncertain markup refuses
    def body(value, en="Free", nl="Gratis"):
        objs = w2b_objects(**{"801": {"body": (MTXT, value)}})
        _, _, _, p, exc = proposed(objs=objs, plan=w2b_plan(extra_mf=[item("bx", en, nl, key="value", field="custom.faq_items#20")]))
        return ("WRITTEN WITHOUT REVIEW" if MO(801) + "|body" in WROTE else p.get(MO(801) + "|body", {}).get("assembled")), exc
    for value, why in (('<a title="unclosed>Free</a>', "unclosed double quote"), ("<a title='unclosed>Free</a>", "unclosed single quote"),
                       ('<a title="x"class="y">Free</a>', "attributes without whitespace"), ("<!-->Free<!-- x -->", "abrupt comment <!-->"),
                       ("<!--->Free<!-- x -->", "abrupt comment <!--->"), ("<!-- a --!><p>Free</p> -->", "comment closed by --!>"),
                       ("<textarea>Free</textarea>", "textarea"), ("<title>Free</title>", "title"), ("<svg><text>Free</text></svg>", "svg"),
                       ("<!DOCTYPE html><p>Free</p>", "doctype"), ("<?php x ?><p>Free</p>", "processing instruction"),
                       ('<a title=x"y>Free</a>', "stray quote in an unquoted value")):
        out, exc = body(value)
        check("R32-3: %s is not proposed" % why, out is None and any("markup" in "; ".join(e["reasons"]) for e in exc), (out, exc))
    out, _ = body("<a title=\"a>b\" data-x='c>d' href=/x>Free</a>")
    check("R32-3: a quoted '>' stays inside its tag, the attributes byte for byte", out == "<a title=\"a>b\" data-x='c>d' href=/x>Gratis</a>", out)

    # R32-4: Liquid behind JSON escapes or entities refuses
    esc = lambda tree: json.dumps(tree).replace("{{", "\\u007b\\u007b").replace("}}", "\\u007d\\u007d")
    for value, why in ((esc({"type": "root", "children": [{"type": "text", "value": "Free"}, {"type": "link", "url": "https://x.test/{{ s }}", "children": []}]}), "an escaped structural URL"),
                       (esc({"type": "root", "children": [{"type": "text", "value": "{{ Free }}"}]}), "an escaped text leaf"),
                       (esc({"{{ k }}": "Free"}), "an escaped object key"),
                       ("<p>&#123;&#123; x &#125;&#125;</p><p>Free</p>", "HTML entities")):
        out, exc = body(value)
        check("R32-4: Liquid in %s keeps the field unproposed" % why, out is None and any("Liquid" in "; ".join(e["reasons"]) for e in exc), (out, exc))

    # R32-5: the writer re-reads provenance, uncached, before the first mutation and before each chunk
    plan = w2b_plan()

    class Detach(W2BFake):
        """Detaches the product's FAQ root on the content re-read of `on` (the writer's last read before a mutation)."""
        on = [MO(800)]

        def post(self, path, body_, headers):
            if "translatableResourcesByIds" in body_.get("query", "") and body_["variables"]["ids"] == self.on:
                for mf in self.store["product_metafields"]["gid://shopify/Product/1"]:
                    if mf["key"] == "faq_items":
                        mf["value"] = "[]"
            return super().post(path, body_, headers)
    ok, code, muts, text, _ = bound_write(w2b_objects(), plan, MO(800) + "|title", fake=Detach)
    check("R32-5: a reference detached at the writer's last re-read stops the chunk: nothing written",
          ok and code == 2 and muts == 0 and "provenance" in text, (ok, code, muts, text))
    _, _, _, f, _ = run2b(w2b_store(w2b_objects()), plan)
    fb = bind(f["proposals"], MO(800) + "|title", MO(802) + "|text")
    _, _, d, _, _ = run2b(w2b_store(w2b_objects()), plan, field_bindings=fb)

    class Unlink(W2BFake):
        """Unlinks step 802 from 800 when the second PRODUCT listing starts: the writer's first provenance read."""
        def post(self, path, body_, headers):
            if "translatableResources(" in body_.get("query", "") and body_["variables"].get("type") == "PRODUCT":
                self.listings = getattr(self, "listings", 0) + 1
                if self.listings == 2:
                    typ, handle, old = self.store["w2b"][MO(800)]
                    self.store["w2b"][MO(800)] = (typ, handle, dict(old, steps=(REF, "[]")))
            return super().post(path, body_, headers)
    fake = Unlink(w2b_store(w2b_objects()))
    code, text, _, _, fake = run2b(None, plan, field_bindings=fb, fake=fake, argv=WRITE + (d["checksum"],))
    check("R32-5: provenance of all bound fields is checked before the first mutation", code == 2 and not fake.mutations
          and "before any write" in text, (code, fake.mutations, text))

    class Later(W2BFake):
        """Unlinks step 802 at 800's content re-read: 800's chunk is still right, 802's chunk must stop."""
        def post(self, path, body_, headers):
            if "translatableResourcesByIds" in body_.get("query", "") and body_["variables"]["ids"] == [MO(800)]:
                typ, handle, old = self.store["w2b"][MO(800)]
                self.store["w2b"][MO(800)] = (typ, handle, dict(old, steps=(REF, "[]")))
            return super().post(path, body_, headers)
    fake = Later(w2b_store(w2b_objects()))
    code, text, _, _, fake = run2b(None, plan, field_bindings=fb, fake=fake, argv=WRITE + (d["checksum"],))
    check("R32-5: a later chunk re-checks its own provenance (one write, then a stop)", code == 2 and len(fake.mutations) == 1
          and fake.mutations[0][1] == MO(800), (code, fake.mutations, text))

    # R32-6: whitespace spelled as entities stays as spelled
    for value, want_ in (("<p>&nbsp;Free&nbsp;</p>", "<p>&nbsp;Gratis&nbsp;</p>"), ("<p>&#160; Free &#xA0;</p>", "<p>&#160; Gratis &#xA0;</p>"),
                         ("<p>&nbsp;</p><p>Free</p>", "<p>&nbsp;</p><p>Gratis</p>"), ("<p> &NonBreakingSpace;Free</p>", "<p> &NonBreakingSpace;Gratis</p>")):
        out, _ = body(value)
        check("R32-6: entity whitespace kept as spelled (%s)" % value[:22], out == want_, out)


class Listings(W2BFake):
    """Runs hook(store) when the n-th PRODUCT listing starts. In a write the listings are: 1 the build, 2 the global
    provenance check before the first mutation, 3 the first chunk's provenance check after its content re-read."""
    n, hook = None, None

    def post(self, path, body_, headers):
        if "translatableResources(" in body_.get("query", "") and body_["variables"].get("type") == "PRODUCT":
            self.listings = getattr(self, "listings", 0) + 1
            if self.listings == self.n:
                self.hook(self.store)
        return super().post(path, body_, headers)


def listing_fake(n, hook):
    return lambda store: type("Hooked", (Listings,), {"n": n, "hook": staticmethod(hook)})(store)


def set_nl(gid, key, value):
    def prep(store):
        node = next(x for x in store["types"]["METAOBJECT"] if x["resourceId"] == MO(gid))
        node["translations"] = {"nl": [tr(key, value)]}
    return prep


def r32c(check):
    """R32c regressions: each fails on candidate 2 and passes on candidate 3 (the two parser controls pass on both)."""
    # C1: a current translation the provenance re-read returns as changed stops the write
    ok, code, muts, text, _ = bound_write(w2b_objects(), w2b_plan(), MO(800) + "|title",
                                          fake=listing_fake(3, set_nl(800, "title", "Victor edited this")))
    check("R32c-C1: a manual NL edit seen by the chunk's provenance re-read is not overwritten",
          ok and code == 2 and muts == 0 and "provenance re-read" in text, (ok, code, muts, text))

    # C2: a legacy binding to the target itself still meets the family veto
    own = {"c2": {"resource": MO(840), "key": "label", "en_sha1": sha1("Shipping")}}
    for status in ("hold", "gates", "conflict"):
        sib = item("c9", "Shipping", "Anders", field="custom.ct|shop.metaobjects.compare_value#09")
        if status != "conflict":
            sib[status] = ["legal-review"]
        plan = w2b_plan(extra_mo=[sib])
        _, _, d, _, _ = run2b(w2b_store(w2b_objects()), plan, item_bindings=own)
        code, text, _, _, fake = run2b(w2b_store(w2b_objects()), plan, item_bindings=own, argv=WRITE + ((d or {}).get("checksum", "x"),))
        check("R32c-C2: a %s sibling stops the legacy item bound to the same field" % status,
              d is not None and not any(o["resource"] == MO(840) for o in d["ops"]) and not any(m[1] == MO(840) for m in fake.mutations)
              and any(r["id"] == "c2" and r["result"] == "not written" for r in d["rows"]), (code, fake.mutations))

    # C3: every known root edge to an unreadable object stays in the evidence
    roots = [{"id": "gid://shopify/Metafield/30", "namespace": "custom", "key": "faq_items", "type": REF, "value": json.dumps([MO(800)])},
             {"id": "gid://shopify/Metafield/32", "namespace": "custom", "key": "faq_other", "type": REF, "value": json.dumps([MO(800)])}]
    star = {"lang": "nl", "resources": [{"shopify_type": "METAFIELD", "owner": "duo",
                                         "items": [item("q1", "How to use", "Gebruik", key="value", field="custom.faq_*#01")]}]}
    unreadable = lambda store: store["w2b"].pop(MO(800))

    def second_root(store):
        next(m for m in store["product_metafields"]["gid://shopify/Product/1"] if m["key"] == "faq_other")["id"] = "gid://shopify/Metafield/999"
    ok, code, muts, text, stale = bound_write(w2b_objects(), star, MO(800) + "|title", roots=roots, prep=unreadable, change=second_root)
    check("R32c-C3: a changed second root to an unreadable object is stale; nothing written",
          ok and code == 2 and muts == 0 and any(s["field"] == MO(800) + "|title" for s in stale), (ok, code, muts, stale))

    # C4: a JSON string scalar is decoded for the Liquid check
    scalar = '"\\u007b\\u007b Free \\u007d\\u007d"'
    objs = w2b_objects(**{"801": {"body": (MTXT, scalar)}})
    plan = w2b_plan(extra_mf=[item("bx", scalar, "Gratis", key="value", field="custom.faq_items#20")])
    _, _, _, p, exc = proposed(objs=objs, plan=plan)
    ok, code, muts, _, _ = bound_write(objs, plan, MO(801) + "|body")
    check("R32c-C4: escaped Liquid in a JSON string scalar keeps the field unproposed",
          MO(801) + "|body" not in p and not ok and any("Liquid" in "; ".join(e["reasons"]) for e in exc), (sorted(p), exc))

    # C5: the global check covers every reviewed binding, also one that needs no operation
    plan = w2b_plan(extra_mf=[item("b6", "Quality", "Kwaliteit", key="value", field="custom.faq_items#06")])

    def detach_801(store):
        next(m for m in store["product_metafields"]["gid://shopify/Product/1"] if m["key"] == "faq_items")["value"] = json.dumps([MO(800)])
    ok, code, muts, text, _ = bound_write(w2b_objects(), plan, [MO(800) + "|title", MO(801) + "|title"], prep=set_nl(801, "title", "Kwaliteit"),
                                          fake=listing_fake(2, detach_801))
    check("R32c-C5: a bound field already current that the product no longer reaches stops the whole write",
          ok and code == 2 and muts == 0 and "before any write" in text, (ok, code, muts, text))

    # C6: a reviewed cell counts only when no other object of the type has its selection
    shadow = w2b_objects(**{"821": {"compare_plan": (ONE, MO(830))}})
    cell = MO(820) + "|value"
    _, _, _, p, exc = proposed(objs=shadow, shop=SHOP_820)
    ok, _, _, _, _ = bound_write(shadow, w2b_plan(), cell, shop=SHOP_820)
    check("R32c-C6: an unlisted cell with the same selection blocks the reviewed cell", cell not in p and not ok, sorted(p))

    class NoList(W2BFake):
        def post(self, path, body_, headers):
            if "metaobjects(" in body_.get("query", ""):
                return 200, {"errors": [{"message": "Access denied", "extensions": {"code": "ACCESS_DENIED"}}]}, None
            return super().post(path, body_, headers)
    code, text, _, f, _ = run2b(None, w2b_plan(), shop=SHOP_820, fake=NoList(w2b_store(w2b_objects())))
    check("R32c-C6: without the full list of the type no cell is proposed", code == 0 and cell not in (f or {}).get("proposals", {}), text)

    # Parser controls Astra asked to keep (they pass on candidate 2 as well)
    for value, want_ in (("<p>Free", "<p>Gratis"), ('<a title="x > y">Free</a>', '<a title="x > y">Gratis</a>')):
        objs = w2b_objects(**{"801": {"body": (MTXT, value)}})
        _, _, _, p, _ = proposed(objs=objs, plan=w2b_plan(extra_mf=[item("bx", "Free", "Gratis", key="value", field="custom.faq_items#20")]))
        check("R32c control: %s is proposed as %s" % (value, want_), p.get(MO(801) + "|body", {}).get("assembled") == want_)


class Pager(W2BFake):
    """Serves the compare_value list in pages: first(after) -> (nodes, pageInfo) or None for the normal answer."""
    first = None

    def post(self, path, body_, headers):
        q = body_.get("query", "")
        if "metaobjects(" in q and body_["variables"].get("type") == "compare_value" and self.first:
            got = self.first(body_["variables"].get("after"))
            if got is not None:
                nodes, info = got
                return 200, {"data": {"metaobjects": {"nodes": [{"id": g, "handle": self.store["w2b"][g][1]} for g in nodes], "pageInfo": info}}}, None
        return super().post(path, body_, headers)


def pager(first):
    return lambda store: type("Paged", (Pager,), {"first": staticmethod(first)})(store)


def r32d(check):
    """R32d regressions: each fails on candidate 3 and passes on candidate 4 (the controls pass on both)."""
    body_en = "<p>Free</p><p>Held claim</p>"
    objs = w2b_objects(**{"840": {"body": (MTXT, body_en)}})
    fam = "custom.ct|shop.metaobjects.compare_value#%02d"
    legacy = item("L", body_en, "<p>Gratis</p><p>Vastgehouden claim</p>", field=fam % 30)
    ib = {"L": {"resource": MO(840), "key": "body", "en_sha1": sha1(body_en)}}
    body_written = lambda fake: any(m[1] == MO(840) and any(t["key"] == "body" for t in m[2]) for m in fake.mutations)

    def legacy_write(plan, item_bindings):
        _, _, d, _, _ = run2b(w2b_store(copy.deepcopy(objs)), plan, item_bindings=item_bindings)
        code, text, _, _, fake = run2b(w2b_store(copy.deepcopy(objs)), plan, item_bindings=item_bindings,
                                       argv=WRITE + ((d or {}).get("checksum", "x"),))
        return d or {"ops": [], "rows": []}, code, fake

    # D1: a veto inside the target's segments removes the legacy whole-field op
    for status in ("hold", "gates", "conflict"):
        extra = [legacy]
        if status == "conflict":
            extra += [item("h1", "Held claim", "Claim A", field=fam % 31), item("h2", "Held claim", "Claim B", field=fam % 32)]
        else:
            held = item("h1", "Held claim", "Vastgehouden claim", field=fam % 31)
            held[status] = ["legal-review"]
            extra.append(held)
        d, code, fake = legacy_write(w2b_plan(extra_mo=extra), ib)
        check("R32d-D1: a %s segment in the target stops the legacy whole-field write" % status,
              not body_written(fake) and not any(o["resource"] == MO(840) and o["key"] == "body" for o in d["ops"])
              and any(r["id"] == "L" and r["result"] == "not written" for r in d["rows"]), (code, fake.mutations))
    d, code, fake = legacy_write(w2b_plan(extra_mo=[legacy, item("h1", "Held claim", "Vastgehouden claim", field=fam % 31)]), ib)
    check("R32d control: without a veto the legacy whole-field item is still written", code == 0 and body_written(fake), (code, fake.mutations))
    held_mf = item("bh", "How to use", "Gebruik", key="value", field="custom.faq_items#09", hold=["legal-review"])
    plan = w2b_plan(extra_mf=[held_mf], extra_mo=[item("L2", "How to use", "Gebruik", field="custom.faq_items#99")])
    ib2 = {"L2": {"resource": MO(800), "key": "title", "en_sha1": sha1("How to use")}}
    _, _, d, _, _ = run2b(w2b_store(w2b_objects()), plan, item_bindings=ib2)
    code, text, _, _, fake = run2b(w2b_store(w2b_objects()), plan, item_bindings=ib2, argv=WRITE + ((d or {}).get("checksum", "x"),))
    check("R32d-D1: a hold in the METAFIELD group stops the same family's legacy item in the METAOBJECT group",
          not any(m[1] == MO(800) for m in fake.mutations) and not any(o["resource"] == MO(800) for o in (d or {"ops": []})["ops"]),
          (code, fake.mutations))

    # D2 / N1: only an explicit hasNextPage false ends the list; repeated cursors and endless lists stop cleanly
    cell, plan = MO(820) + "|value", w2b_plan()
    _, _, _, f, _ = run2b(w2b_store(w2b_objects()), plan, shop=SHOP_820)
    fb = bind(f["proposals"], cell)
    _, _, approved, _, _ = run2b(w2b_store(w2b_objects()), plan, shop=SHOP_820, field_bindings=fb)
    shadow = w2b_objects(**{"821": {"compare_plan": (ONE, MO(830))}})
    for label, info in (("missing", {"endCursor": "p2"}), ("null", {"hasNextPage": None, "endCursor": "p2"}),
                        ("invalid (0)", {"hasNextPage": 0, "endCursor": "p2"})):
        paged = pager(lambda after, info=info: ([MO(820)], info) if after is None else ([MO(821)], {"hasNextPage": False, "endCursor": None}))
        code, text, _, f, _ = run2b(None, plan, shop=SHOP_820, fake=paged(w2b_store(copy.deepcopy(shadow))))
        cw, tw, _, _, fw = run2b(None, plan, shop=SHOP_820, field_bindings=fb, fake=paged(w2b_store(copy.deepcopy(shadow))),
                                 argv=WRITE + (approved["checksum"],))
        check("R32d-D2: a %s hasNextPage leaves the list unknown: no proposal, and a bound write stops" % label,
              cell not in (f or {}).get("proposals", {}) and cw == 2 and not fw.mutations, (sorted((f or {}).get("proposals", {})), cw, fw.mutations))
    calls = {"n": 0}

    def same_cursor(after):
        calls["n"] += 1
        return ([MO(820)], {"hasNextPage": calls["n"] < 30, "endCursor": "same"})
    code, text, _, f, _ = run2b(None, plan, shop=SHOP_820, fake=pager(same_cursor)(w2b_store(w2b_objects())))
    check("R32d-N1: a repeated cursor stops the list read cleanly; the cell is not proposed", code == 0 and cell not in (f or {}).get("proposals", {}),
          (code, sorted((f or {}).get("proposals", {}))))
    bound_pages = getattr(register, "MAX_TYPE_PAGES", 200)
    code, text, _, f, _ = run2b(None, plan, shop=SHOP_820, fake=pager(
        lambda after: ([MO(820)] if after is None else [], {"hasNextPage": int((after or "p0")[1:]) < bound_pages + 5,
                                                            "endCursor": "p%d" % (int((after or "p0")[1:]) + 1)}))(w2b_store(w2b_objects())))
    check("R32d-N1: a list longer than the page bound counts as unknown; the cell is not proposed", code == 0
          and cell not in (f or {}).get("proposals", {}), (code, sorted((f or {}).get("proposals", {}))))
    two = pager(lambda after: ([MO(820)], {"hasNextPage": True, "endCursor": "p2"}) if after is None else ([MO(821)], {"hasNextPage": False, "endCursor": None}))
    code, text, _, f, _ = run2b(None, plan, shop=SHOP_820, fake=two(w2b_store(w2b_objects())))
    check("R32d control: a proper two-page list without a duplicate still proposes the cell", cell in (f or {}).get("proposals", {}), text)


def r39(check):
    """Wave 2c: an <svg> without text is one opaque span, a '<' that opens no markup is text, and invariant rows map
    spans that stay as in EN without ever being written on their own. Each fails on 4ded872 (controls excepted)."""
    def body(value, extra=()):
        objs = w2b_objects(**{"801": {"body": (MTXT, value)}})
        rows = [item("bx", "Free", "Gratis", key="value", field="custom.faq_items#20")] + list(extra)
        _, _, d, p, exc = proposed(objs=objs, plan=w2b_plan(extra_mf=rows))
        return ("WRITTEN WITHOUT REVIEW" if MO(801) + "|body" in WROTE else p.get(MO(801) + "|body", {}).get("assembled")), exc, d
    icon = '<svg fill="none" viewBox="0 0 64 64" aria-hidden="true"><g><path d="M2 2h60v60" stroke="#000"/><circle cx="3" cy="3" r="1"/></g></svg>'
    out, _, _ = body('<div class="bf-step"><div class="bf-step-icon">%s</div><p>Free</p></div>' % icon)
    check("R39: an svg without text stays byte for byte; the text beside it is translated",
          out == '<div class="bf-step"><div class="bf-step-icon">%s</div><p>Gratis</p></div>' % icon, out)
    out, _, _ = body('<p>Free</p><svg viewBox="0 0 1 1"><svg x="0"><path d="M0 0"/></svg><rect width="1"/></svg>')
    check("R39: nested svg elements are counted and kept whole", out == '<p>Gratis</p><svg viewBox="0 0 1 1"><svg x="0"><path d="M0 0"/></svg><rect width="1"/></svg>', out)
    out, _, _ = body('<p>Free</p><svg viewBox="0 0 1 1"/>')
    check("R39: a self-closing svg is one opaque tag", out == '<p>Gratis</p><svg viewBox="0 0 1 1"/>', out)
    out, _, _ = body('<p>Free</p><svg><path d="M0 0" id="a>b"/></svg>')
    check("R39: a quoted '>' inside an svg tag stays inside it", out == '<p>Gratis</p><svg><path d="M0 0" id="a>b"/></svg>', out)
    for value, why in (('<p>Free</p><svg><text x="1">Free</text></svg>', "svg text element"),
                       ('<p>Free</p><svg><title>Free</title></svg>', "svg title"),
                       ('<p>Free</p><svg><desc>d</desc></svg>', "svg desc"),
                       ('<p>Free</p><svg><foreignObject><p>Free</p></foreignObject></svg>', "svg foreignObject"),
                       ('<p>Free</p><svg><style>p{}</style></svg>', "svg style"),
                       ('<p>Free</p><svg><a href="/x"><path/></a></svg>', "svg link"),
                       ('<p>Free</p><svg>Free</svg>', "text inside svg"),
                       ('<p>Free</p><svg><!-- c --><path/></svg>', "comment inside svg"),
                       ('<p>Free</p><svg><path d="M0 0"/>', "unclosed svg"),
                       ('<p>Free</p><svg><path d="M0/></svg>', "unclosed quote inside svg"),
                       ('<p>Free</p></svg>', "stray svg end tag"),
                       ('<p>Free</p><math><mi>x</mi></math>', "math (still refused)")):
        out, exc, _ = body(value)
        check("R39: %s is not proposed" % why, out is None and any("markup" in "; ".join(e["reasons"]) for e in exc), (out, exc))
    out, _, _ = body("<p>nHAp <100 nm</p><p>Free</p>", [item("bn", "nHAp <100 nm", "nHAp <100 nm (nl)", key="value", field="custom.faq_items#21")])
    check("R39: a '<' before a digit is text (as in the HTML tokenizer); the translation is escaped",
          out == "<p>nHAp &lt;100 nm (nl)</p><p>Gratis</p>", out)
    out, _, _ = body("<p>a < b</p><p>Free</p>", [item("bs", "a < b", "a < b (nl)", key="value", field="custom.faq_items#22")])
    check("R39: a '<' before a space is text", out == "<p>a &lt; b (nl)</p><p>Gratis</p>", out)
    for value, why in (("<p>Free</p><", "a '<' at the very end"), ("<p>Free</p><a", "an unclosed tag after the change")):
        out, exc, _ = body(value)
        check("R39: %s is not proposed" % why, out is None and any("markup" in "; ".join(e["reasons"]) for e in exc), (out, exc))
    inv = lambda iid, en, n: dict(item(iid, en, en, key="value", field="custom.faq_items#%02d" % n), invariant=True)
    out, _, _ = body("<p>Free</p><p>Guarana</p>", [inv("ig", "Guarana", 30)])
    check("R39: an invariant row maps its span unchanged; the rest is translated", out == "<p>Gratis</p><p>Guarana</p>", out)
    out, exc, d = body("<p>Guarana</p><p>CPSR · 2026</p>", [inv("ig", "Guarana", 30), inv("ic", "CPSR · 2026", 31)])
    check("R39: a field of invariant spans only is neither proposed nor written", out is None and MO(801) + "|body" not in WROTE
          and not any(e["field"] == MO(801) + "|body" for e in exc), (out, exc))
    check("R39: invariant rows make no report rows", not any(r["id"] in ("ig", "ic") for r in (d or {"rows": []})["rows"]))
    store = w2b_store(w2b_objects())
    store["types"]["METAFIELD"] = store["types"].get("METAFIELD", []) + [{"resourceId": "gid://shopify/Metafield/77", "translatableContent": [c("value", "Guarana")], "translations": {}}]
    store["product_metafields"]["gid://shopify/Product/1"].append({"id": "gid://shopify/Metafield/77", "namespace": "custom", "key": "faq_items_extra", "type": TXT, "value": "Guarana"})
    plan = w2b_plan(extra_mf=[dict(item("ig", "Guarana", "Guarana", key="value", field="custom.faq_items_extra#01"), invariant=True)])
    _, _, d, _, _ = run2b(store, plan)
    check("R39: a whole-value metafield equal to an invariant row is never registered",
          d is not None and not any(o["resource"] == "gid://shopify/Metafield/77" for o in d["ops"]), (d or {}).get("ops"))
    try:
        import build_payloads as bp
    except ImportError:
        bp = None
    src = {"id": "admin:karmicare-biorhythmic-oral-care-system:custom.product_faq#900", "batch": "batch-02-pdp", "page": "pdp",
           "resource_type": "metafield", "file_or_handle": "karmicare-biorhythmic-oral-care-system", "key_path": "custom.product_faq#900",
           "en": "Guarana", "sha1": sha1("Guarana"), "status": "admin-held", "never_translate": False}
    row_ = {"en": "Guarana", "en_sha1": sha1("Guarana"), "nl": "Guarana", "status": "admin", "flags": ["admin"]}
    def built(entry):
        res, skipped = bp.build("nl", {src["id"]: entry}, {src["id"]: src})
        return [i for r in res.values() for i in r["items"]], skipped
    items, skipped = built(row_) if bp else ([], {})
    check("R39 builder control: a same-as-EN row without the flag is still skipped", bp is not None and not items, skipped)
    items, _ = built(dict(row_, flags=["admin", "invariant"])) if bp else ([], {})
    check("R39 builder: a flagged invariant row is kept and marked", len(items) == 1 and items[0].get("invariant") is True, items)
    try:
        items, skipped = built(dict(row_, nl="Guaraná", flags=["admin", "invariant"])) if bp else ([], {})
        raised = False
    except Exception as err:  # noqa: BLE001 - the builder's PlanError (R42-3)
        raised, items = type(err).__name__ == "PlanError", []
    check("R39/R42-3 builder: an invariant row whose value differs from the EN stops plan generation", raised, items)


def r42(check):
    """R42 regressions: each fails on wave2c-candidate (candidate 1) and passes here (controls excepted)."""
    def body(value):
        objs = w2b_objects(**{"801": {"body": (MTXT, value)}})
        _, _, d, p, exc = proposed(objs=objs, plan=w2b_plan(extra_mf=[item("bx", "Free", "Gratis", key="value", field="custom.faq_items#20")]))
        return ("WRITTEN WITHOUT REVIEW" if MO(801) + "|body" in WROTE else p.get(MO(801) + "|body", {}).get("assembled")), exc
    icon = ('<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 64 64" aria-hidden="true" width="64" height="64">'
            '<g clip-path="url(#clip0_1)" id="Assets"><path d="M1 1" stroke="#7FB9FF" stroke-width="2" stroke-linecap="round" '
            'stroke-linejoin="round" fill="currentColor"/><rect width="1" height="1" fill="white"/></g><defs><clipPath id="clip0_1">'
            '<rect width="64" height="64" fill="white"/></clipPath></defs></svg>')
    out, _ = body("<p>Free</p>" + icon)
    check("R42-1 control: an icon in the shape of the live ones stays byte for byte", out == "<p>Gratis</p>" + icon, out)
    for value, why in (('<p>Free</p><svg role="img" aria-label="Free shipping"><path/></svg>', "an aria-label on the svg root"),
                       ('<p>Free</p><svg><g role="img" aria-label="Free shipping"><path/></g></svg>', "an aria-label on a child"),
                       ('<p>Free</p><svg role="img" aria-label="Free shipping"/>', "a labelled self-closing svg"),
                       ('<p>Free</p><svg aria-labelledby="english-label"><path/></svg>', "aria-labelledby"),
                       ('<p>Free</p><svg aria-describedby="d"><path/></svg>', "aria-describedby"),
                       ('<p>Free</p><svg aria-hidden="false"><path/></svg>', "aria-hidden other than true"),
                       ('<p>Free</p><svg><use href="https://example.invalid/i.svg#x"/></svg>', "a use element with an external href"),
                       ('<p>Free</p><svg><path xlink:href="javascript:alert(1)"/></svg>', "an xlink:href"),
                       ('<p>Free</p><svg onload="x()"><path/></svg>', "an event attribute"),
                       ('<p>Free</p><svg><path style="fill:red"/></svg>', "a style attribute"),
                       ('<p>Free</p><svg><path fill="url(#p)"/></svg>', "paint from url(...)"),
                       ('<p>Free</p><svg><g clip-path="url(https://x.test/c)"><path/></g></svg>', "a non-local clip-path"),
                       ('<p>Free</p><svg><div><input value="Free shipping"></div></svg>', "a foreign tag inside svg"),
                       ('<p>Free</p><svg><g><path/></svg>', "mismatched nesting"),
                       ('<p>Free</p><svg><image href="a.png"/></svg>', "an image element"),
                       ('<p>Free</p><svg xmlns="http://example.invalid/ns"><path/></svg>', "a foreign xmlns")):
        out, exc = body(value)
        check("R42-1: %s is not proposed" % why, out is None and any("markup" in "; ".join(e["reasons"]) for e in exc), (out, exc))

    # R42-2: an invariant item alone never makes an operation, also through a legacy item binding
    objs = w2b_objects(**{"801": {"body": (TXT, "Guarana")}})
    ib = {"ig": {"resource": MO(801), "key": "body", "en_sha1": sha1("Guarana")}}
    manual = set_nl(801, "body", "Victor manual text")
    for invariant, label in ((True, "an invariant legacy-bound item"), (False, "control: an ordinary legacy-bound item")):
        row_ = item("ig", "Guarana", "Guarana" if invariant else "Guarana NL", field="custom.faq_items#31")
        if invariant:
            row_["invariant"] = True
        plan = w2b_plan(extra_mo=[row_])
        store = w2b_store(copy.deepcopy(objs))
        manual(store)
        _, _, d, _, _ = run2b(store, plan, item_bindings=ib)
        store = w2b_store(copy.deepcopy(objs))
        manual(store)
        code, text, _, _, fake = run2b(store, plan, item_bindings=ib, argv=WRITE + ((d or {}).get("checksum", "x"),))
        wrote = any(m[1] == MO(801) for m in fake.mutations)
        if invariant:
            check("R42-2: %s never overwrites the manual NL (no op, no mutation)" % label, d is not None and not wrote
                  and not any(o["resource"] == MO(801) for o in d["ops"]), (code, fake.mutations))
        else:
            check("R42-2 %s still writes" % label, wrote, (code, fake.mutations))
    # an invariant row in a mixed bound field gets no result row of its own (R42 non-blocker 1)
    objs = w2b_objects(**{"801": {"body": (MTXT, "<p>Free</p><p>Guarana</p>")}})
    rows = [item("bx", "Free", "Gratis", key="value", field="custom.faq_items#20"),
            dict(item("ig", "Guarana", "Guarana", key="value", field="custom.faq_items#30"), invariant=True)]
    _, _, _, f, _ = run2b(w2b_store(objs), w2b_plan(extra_mf=rows))
    fb = bind((f or {}).get("proposals", {}), MO(801) + "|body")
    _, _, d, _, _ = run2b(w2b_store(objs), w2b_plan(extra_mf=rows), field_bindings=fb)
    check("R42 follow-up: a mixed bound field is written, without a result row for its invariant item",
          d is not None and any(o["resource"] == MO(801) for o in d["ops"]) and not any(r["id"] == "ig" for r in d["rows"]),
          (d or {}).get("rows"))


def r42b(check):
    """R42b regressions: each fails on wave2c-candidate-2 and passes here (controls excepted)."""
    def body(value):
        objs = w2b_objects(**{"801": {"body": (MTXT, value)}})
        _, _, d, p, exc = proposed(objs=objs, plan=w2b_plan(extra_mf=[item("bx", "Free", "Gratis", key="value", field="custom.faq_items#20")]))
        return ("WRITTEN WITHOUT REVIEW" if MO(801) + "|body" in WROTE else p.get(MO(801) + "|body", {}).get("assembled")), exc
    for value, why in (('<p>Free</p><svg width="1"/>', "a quoted self-closing svg"),
                       ('<p>Free</p><svg width=1 />', "an unquoted value with a separated '/>'"),
                       ('<p>Free</p><svg><path d="M0 0"/><g><path d="M0 0" /></g></svg>', "quoted self-closing descendants"),
                       ('<p>Free</p><svg><path fill="&#110;one"/></svg>', "an encoded paint keyword")):
        out, _ = body(value)
        check("R42b control: %s stays byte for byte" % why, out == value.replace("Free", "Gratis", 1), out)
    labelled = '<p>Free</p><svg width=1/><g role="img" aria-label="Free shipping"><path d="M0 0h10v10z"/></g>'
    hidden = '<p>Free</p><svg aria-hidden=true/>'
    for value, why in ((labelled, "an svg whose unquoted width ends in '/' (not self-closing) before a labelled g"),
                       (hidden, "aria-hidden=true/ (its value is 'true/')"),
                       ('<p>Free</p><svg><path d=M0/><g role="img" aria-label="Free shipping"><path/></g></svg>', "a descendant whose unquoted value ends in '/'"),
                       ('<p>Free</p><svg><path fill="u&#114;l(#g)"/></svg>', "an entity-encoded url() paint"),
                       ('<p>Free</p><svg><path fill="&#117;rl(https://example.invalid/p.svg#x)"/></svg>', "an encoded external url() paint"),
                       ('<p>Free</p><svg><path fill="u\\72l(#g)"/></svg>', "a CSS-escaped url() paint"),
                       ('<p>Free</p><svg><path stroke="url(#g)"/></svg>', "url() stroke"),
                       ('<p>Free</p><svg><path fill="&#x55;RL(#g)"/></svg>', "a hex-entity, upper-case url() paint")):
        out, exc = body(value)
        check("R42b: %s is not proposed" % why, out is None and any("markup" in "; ".join(e["reasons"]) for e in exc), (out, exc))

    # R42b-1 through the writer: a binding made by the previous parser (self-closing read from the byte before '>')
    # is stale under the lexical flag and aborts before any mutation.
    def previous(value, i, scan=register.scan_tag):
        tag, reason = scan(value, i)
        if tag and len(tag) == 3:  # a two-field tag is already the previous parser's own (candidate 2)
            tag = (tag[0], tag[1], value[i + 1] != "/" and value[tag[1] - 2] == "/")
        return tag, reason
    rows = [item("bx", "Free", "Gratis", key="value", field="custom.faq_items#20")]
    for value, label in ((labelled, "the labelled-g field"), (hidden, "the aria-hidden=true/ field")):
        objs = w2b_objects(**{"801": {"body": (MTXT, value)}})
        register.scan_tag = previous
        try:
            _, _, _, f, _ = run2b(w2b_store(copy.deepcopy(objs)), w2b_plan(extra_mf=rows))
        finally:
            register.scan_tag = previous.__defaults__[0]
        fb = bind((f or {}).get("proposals", {}), MO(801) + "|body")
        _, _, d, _, _ = run2b(w2b_store(copy.deepcopy(objs)), w2b_plan(extra_mf=rows), field_bindings=fb)
        code, _, _, _, fake = run2b(w2b_store(copy.deepcopy(objs)), w2b_plan(extra_mf=rows), field_bindings=fb,
                                    argv=WRITE + ((d or {}).get("checksum", "x"),))
        check("R42b-1: a previous-parser binding for %s aborts with no mutation" % label,
              bool(fb) and code != 0 and not any(m[1] == MO(801) for m in fake.mutations), (bool(fb), code, fake.mutations))

    # R42b-N2: an invariant item in a vetoed legacy target gets no result row (the veto itself still holds)
    body_en = "<p>Free</p><p>Held claim</p>"
    objs = w2b_objects(**{"840": {"body": (MTXT, body_en)}})
    fam = "custom.ct|shop.metaobjects.compare_value#%02d"
    held = item("h1", "Held claim", "Vastgehouden claim", field=fam % 31)
    held["hold"] = ["legal-review"]
    plan = w2b_plan(extra_mo=[dict(item("L", body_en, body_en, field=fam % 30), invariant=True), held])
    _, _, d, _, _ = run2b(w2b_store(objs), plan, item_bindings={"L": {"resource": MO(840), "key": "body", "en_sha1": sha1(body_en)}})
    check("R42b-N2: a vetoed invariant target makes no op and no result row for its invariant item",
          d is not None and not any(o["resource"] == MO(840) for o in d["ops"]) and not any(r["id"] == "L" for r in d["rows"]),
          (d or {}).get("rows"))


def r47(check):
    """R47/R47b shop policies: the reviewed shop-policies.json pins each policy handle to its GID; the body is written
    only when every non-blank text of the live body lies in exactly one approved block, matched on text boundaries,
    with the markup kept byte for byte. Positive checks fail on ea323f8 (no route); the R47b regressions fail on
    wave policy-candidate (body search by content)."""
    REFUND = "<p><strong>Refunds</strong></p><p>Return within 30 days.</p><p>Refund within 14 days.</p>"
    WANT = "<p><strong>Terugbetalingen</strong></p><p>Terugsturen binnen 30 dagen.</p><p>Terugbetaling binnen 14 dagen.</p>"
    BLOCKS = [("b1", "<strong>Refunds</strong>", "<strong>Terugbetalingen</strong>"),
              ("b2", "Return within 30 days.", "Terugsturen binnen 30 dagen."),
              ("b3", "Refund within 14 days.", "Terugbetaling binnen 14 dagen.")]
    PIN = {"refund-policy": "gid://shopify/ShopPolicy/2"}

    def policies(*bodies):
        return [{"resourceId": "gid://shopify/ShopPolicy/%d" % (n + 1), "translatableContent": [c("title", "Policy %d" % n), c("body", b, "HTML")],
                 "translations": {}} for n, b in enumerate(bodies)]

    def plan_for(blocks=BLOCKS, held=0, extra_groups=(), extra_items=()):
        items = [item(i, en, nl, kind="assemble", key="body", field="body#%s" % i) for i, en, nl in blocks] + list(extra_items)
        return {"lang": "nl", "resources": [{"shopify_type": "SHOP_POLICY", "owner": "refund-policy", "batch": "batch-04-legal",
                                              "assembled_field": {"blocks": len(blocks), "drafted": len(blocks), "missing_or_held": held, "gated": 0},
                                              "items": items}] + list(extra_groups)}

    def main_run(fake, sub, plan, pins, argv):
        with open(os.path.join(sub, "plan-nl.json"), "w", encoding="utf-8") as f:
            json.dump(plan, f)
        pp = os.path.join(sub, "shop-policies.json")
        if pins is not None:
            with open(pp, "w", encoding="utf-8") as f:
                json.dump({"policies": pins}, f)
        extra = {"shop_policies_path": pp} if "shop_policies_path" in register.main.__code__.co_varnames else {}
        out, code = io.StringIO(), 0
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(out):
            try:
                register.main(list(argv), transport=fake, credentials=lambda: ("client-id", register.Secret(SECRET)), out=sub,
                              plans=os.path.join(sub, "plan-%s.json"), bindings_path=os.path.join(sub, "bindings.json"), **extra)
            except SystemExit as e:
                code = e.code if isinstance(e.code, int) else 1
        return code

    def policy_run(live, plan=None, pins=PIN, approve=False, fake_cls=None):
        store = base_store()
        store["types"]["SHOP_POLICY"] = live
        argv = ("--lang", "nl", "--theme-id", THEME)
        with tempfile.TemporaryDirectory() as sub:
            fake = Fake(copy.deepcopy(store))
            code = main_run(fake, sub, plan or plan_for(), pins, argv)
            path = os.path.join(sub, "dry-run-nl.json")
            d = json.load(open(path, encoding="utf-8")) if os.path.exists(path) else None
            if approve and d:
                fake = (fake_cls or Fake)(copy.deepcopy(store))
                code = main_run(fake, sub, plan or plan_for(), pins, argv + ("--write", "--approve", d["checksum"]))
        return code, d or {"ops": [], "rows": []}, fake

    no_op = lambda d: not any("ShopPolicy" in o["resource"] for o in d["ops"])
    _, d, _ = policy_run(policies("<p>Shipping.</p>", REFUND))
    ops = [(o["resource"], o["key"], o["value"]) for o in d["ops"]]
    check("R47: the pinned policy's body is assembled on key 'body'", ops == [("gid://shopify/ShopPolicy/2", "body", WANT)], ops)
    code, _, fake = policy_run(policies("<p>Shipping.</p>", REFUND), approve=True)
    check("R47: the approved write registers that body only", code == 0 and [(m[1], [t["key"] for t in m[2]]) for m in fake.mutations]
          == [("gid://shopify/ShopPolicy/2", ["body"])], (code, fake.mutations))
    _, d, _ = policy_run(policies("<p>Shipping.</p>", "<p><strong>Refunds</strong></p><!-- note --><p>Return within 30 days.</p>\n<p>Refund within 14 days.</p>"))
    check("R47b control: a comment and whitespace between blocks stay as they are",
          [o["value"] for o in d["ops"]] == ["<p><strong>Terugbetalingen</strong></p><!-- note --><p>Terugsturen binnen 30 dagen.</p>\n<p>Terugbetaling binnen 14 dagen.</p>"],
          [o["value"] for o in d["ops"]])
    nested = [("n1", "Refund within <strong>14 days</strong>.", "Terugbetaling binnen <strong>14 dagen</strong>."),
              ("n2", "<strong>14 days</strong>", "<strong>14 dagen</strong>")]
    _, d, _ = policy_run(policies("<p>Shipping.</p>", "<p>Refund within <strong>14 days</strong>.</p><p><strong>14 days</strong></p>"),
                         plan=plan_for(nested))
    check("R47b control: a short block's EN may also sit inside another approved block (refund '14 days')",
          [o["value"] for o in d["ops"]] == ["<p>Terugbetaling binnen <strong>14 dagen</strong>.</p><p><strong>14 dagen</strong></p>"],
          [o["value"] for o in d["ops"]])
    for live, why in ((policies("<p>Shipping.</p>", REFUND + "<p>UNREVIEWED LEGAL TEXT.</p>"), "R47-1: unreviewed text after the blocks"),
                      (policies("<p>Shipping.</p>", REFUND.replace("<p>Return", "<p>UNREVIEWED. Return")), "R47-1: unreviewed text inside a block's paragraph"),
                      (policies("<p>Shipping.</p>", REFUND.replace("30 days.</p>", "30 days. Return within 30 days.</p>")), "R47-1: a block's EN twice"),
                      (policies(REFUND, "<p>Other.</p>"), "R47-1: the pinned GID holds another policy (the blocks live elsewhere)"),
                      (policies("<p>Shipping.</p>", REFUND.replace('<p>Return', '<p data-copy="Return within 30 days.">Return')), "R47-2: the EN also in an attribute"),
                      (policies("<p>Shipping.</p>", REFUND.replace('<p>Return', '<!--Return within 30 days.--><p>Return')), "R47-2: the EN also in a comment"),
                      ([{"resourceId": "gid://shopify/ShopPolicy/2", "translatableContent": [c("body", REFUND, "HTML"), c("body", REFUND, "HTML")],
                         "translations": {}}], "R47-4: the pinned policy offers two body keys")):
        _, d, _ = policy_run(live)
        check("%s: no operation" % why, no_op(d), d["ops"])
    _, d, _ = policy_run(policies("<p>Shipping.</p>", REFUND), pins={})
    check("R47-1: without a reviewed GID for the handle nothing is written", no_op(d), d["ops"])
    marked = [BLOCKS[0], ("b2", "Return within 30 days.", "Terugsturen binnen <em>30</em> dagen."), BLOCKS[2]]
    _, d, _ = policy_run(policies("<p>Shipping.</p>", REFUND), plan=plan_for(marked))
    check("R47-2: a translation that changes the block's markup is not written", no_op(d), d["ops"])
    for status in ("hold", "gates"):
        dup = item("h1", "Return within 30 days.", "Vastgehouden", kind="assemble", key="body", field="body#b2")
        dup[status] = ["legal-review"]
        group = {"shopify_type": "SHOP_POLICY", "owner": "refund-policy", "batch": "batch-04-legal",
                 "assembled_field": {"blocks": 1, "drafted": 1, "missing_or_held": 0, "gated": 0}, "items": [dup]}
        _, d, _ = policy_run(policies("<p>Shipping.</p>", REFUND), plan=plan_for(extra_groups=[group]))
        check("R47-3: a %s row of the policy in another plan group stops the policy" % status, no_op(d), d["ops"])
    _, d, _ = policy_run(policies("<p>Shipping.</p>", REFUND), plan=plan_for(extra_items=[item("t1", "Policy 1", "Beleid", kind="direct", key="title")]))
    check("R47 non-blocker: a direct title item on a policy is never written", not any(o["key"] == "title" for o in d["ops"])
          and any(r["id"] == "t1" and r["result"] == "not written" for r in d["rows"]), d["ops"])

    class SecondBody(Fake):
        """Adds a second body key to the pinned policy once the writer re-reads it (R47-4)."""
        reads = 0

        def post(self, path, body, headers):
            if "translatableResourcesByIds" in body.get("query", ""):
                SecondBody.reads += 1
                if SecondBody.reads >= 2:
                    node = next(n for n in self.store["types"]["SHOP_POLICY"] if n["resourceId"] == "gid://shopify/ShopPolicy/2")
                    if sum(x["key"] == "body" for x in node["translatableContent"]) == 1:
                        node["translatableContent"].append(c("body", REFUND, "HTML"))
            return super().post(path, body, headers)
    code, _, fake = policy_run(policies("<p>Shipping.</p>", REFUND), approve=True, fake_cls=SecondBody)
    check("R47-4: a second body key appearing before the mutation stops the write", code == 2 and not fake.mutations, (code, fake.mutations))


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
        fprop = json.load(open(os.path.join(folder, "fields-proposed-nl.json"), encoding="utf-8"))["proposals"]
        check("R18b-B / 2b: an unbound metaobject item is proposed as a field, not written", code_b == 0
              and not any(o["resource"].startswith("gid://shopify/Metaobject/700") for o in db["ops"])
              and "gid://shopify/Metaobject/700|role" in fprop and "gid://shopify/Metaobject/701|role" not in fprop, sorted(fprop))
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
    wave2b(check)
    r32(check)
    r32c(check)
    r32d(check)
    r39(check)
    r42(check)
    r42b(check)
    r47(check)
    print("%d failures" % len(failures))
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
