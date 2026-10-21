#!/usr/bin/env python3
"""Register the NL/FR plans in Shopify through the Admin GraphQL API (B4 access path A, review R18).

Reads docs/localization/registration/plan-<lang>.json and the live store, and writes per language:

  docs/localization/registration/live/dry-run-<lang>.md     every mutation in full, for Victor
  docs/localization/registration/live/dry-run-<lang>.json   the approval snapshot, machine-readable
  docs/localization/registration/live/journal-<lang>.jsonl  appended during a write: every attempt and result

Run from the repo root:

  python3 docs/localization/registration/register.py [--lang nl|fr|both] [--theme-id N] [--remove-never]
  python3 docs/localization/registration/register.py --lang nl [--theme-id N] [--remove-never] --write --approve <checksum>

Dry run (the default) sends only queries. Targets are resolved by identity first and EN second:
- theme content only in resources whose GID proves the published theme (--theme-id) and the template, with
  every hint as an exact token of the key; without --theme-id, theme items are out of scope;
- direct items only on their own key; product metafields only by namespace and key; metaobjects only
  through the product's metafield references (nested references need read_metaobjects);
- menu links and shop policies have no proven owner route yet and are never written.
Exactly one target is written. None is stale or missing, several are ambiguous, and two plan items that
want different values on one target are a conflict: none of these is written. Protected targets
(selling plans and groups, handle_item, selling_plan_id, the Subscription Name values) are never
registered; existing translations on them are proposed for removal, which is part of the approval only
with --remove-never. A JSON field is written only when every text leaf maps to an approved item.

Approval binds a snapshot: store, API version, theme, plan file, removal choice, and per target the live
EN digest, the current NL/FR (present, value, outdated) and the new value. Write rebuilds the snapshot
and writes only if its checksum is the approved one, re-reads each resource right before its mutation,
and stops at the first difference. A translation edited between that re-read and the mutation is not
detected: the API digest protects the EN only. NL and FR are published: a registered translation is
live at once.

Credentials (APP-SETUP.md): client ID and secret come from the macOS Keychain item
"karmicare-translations", read inside this process; the 24 h token from client_credentials lives in
memory only. Every message, report and journal line passes a scrubber that removes both, and API error
text is reduced to an allowlist of fields.
"""
import argparse
import fnmatch
import hashlib
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

SHOP = "karmicares.myshopify.com"
API_VERSION = "2026-10"
KEYCHAIN_SERVICE = "karmicare-translations"
PLAN = "docs/localization/registration/plan-%s.json"
LIVE = "docs/localization/registration/live"
LOOP_TYPES = ("SELLING_PLAN", "SELLING_PLAN_GROUP")
LOOP_GIDS = ("SellingPlan", "SellingPlanGroup")
NEVER_KEYS = ("handle_item", "selling_plan_id")
NEVER_VALUES = ("60-Day Supply", "Year Supply")
THEME_TYPES = ("ONLINE_STORE_THEME_JSON_TEMPLATE", "ONLINE_STORE_THEME_SECTION_GROUP")
HANDLE_TYPES = ("PRODUCT", "PAGE", "ARTICLE", "BLOG", "COLLECTION")
UNPROVEN_TYPES = {"LINK": "menu links: no verified owner route (menu -> link) yet",
                  "SHOP_POLICY": "shop policies: no verified owner route (policy type -> resource) yet"}
BODY_KEYS = {"body_html": "body_html", "summary_html": "summary_html", "body": "body_html"}
STRUCTURAL_KEYS = {"type", "url", "target", "listType", "level", "id", "handle", "href", "icon", "image", "link"} | set(NEVER_KEYS)
STRUCTURAL_VALUE = re.compile(r"^(gid://|https?://|/|#|mailto:|tel:)|^[\d\s.,:;%€$+\-/()]*$")
REGISTER_CHUNK = 50
REMOVE_CHUNK = 50
READ_RETRIES = 4

CONTENT = "resourceId translatableContent { key value digest locale type } translations(locale: $locale) { key value outdated }"
Q_LIST = """query($type: TranslatableResourceType!, $after: String, $locale: String!) {
  translatableResources(first: 100, after: $after, resourceType: $type) {
    nodes { %s } pageInfo { hasNextPage endCursor } } }""" % CONTENT
Q_IDS = """query($ids: [ID!]!, $after: String, $locale: String!) {
  translatableResourcesByIds(first: 100, after: $after, resourceIds: $ids) {
    nodes { %s } pageInfo { hasNextPage endCursor } } }""" % CONTENT
Q_METAFIELDS = """query($id: ID!, $after: String) {
  product(id: $id) { metafields(first: 250, after: $after) { nodes { id namespace key type value } pageInfo { hasNextPage endCursor } } } }"""
Q_METAOBJECT = """query($id: ID!) { metaobject(id: $id) { id type handle fields { key type value } } }"""
Q_METAOBJECT_HANDLE = """query($type: String!, $handle: String!) {
  metaobjectByHandle(handle: {type: $type, handle: $handle}) { id type handle fields { key type value } } }"""
M_REGISTER = """mutation($id: ID!, $translations: [TranslationInput!]!) {
  translationsRegister(resourceId: $id, translations: $translations) {
    translations { key locale value } userErrors { field message code } } }"""
M_REMOVE = """mutation($id: ID!, $keys: [String!]!, $locales: [String!]!) {
  translationsRemove(resourceId: $id, translationKeys: $keys, locales: $locales) {
    translations { key locale } userErrors { field message code } } }"""


# ---- secrecy -------------------------------------------------------------------------------------

_SECRETS = set()
_TOKEN_PATTERN = re.compile(r"shp[a-z]{2}_[A-Za-z0-9]{8,}")


def scrub(value):
    """A copy of value (str, list or dict) with every known secret and every Shopify token shape removed."""
    if isinstance(value, str):
        for s in sorted(_SECRETS, key=len, reverse=True):
            value = value.replace(s, "[redacted]")
        return _TOKEN_PATTERN.sub("[redacted]", value)
    if isinstance(value, list):
        return [scrub(v) for v in value]
    if isinstance(value, dict):
        return {scrub(k) if isinstance(k, str) else k: scrub(v) for k, v in value.items()}
    return value


class Secret:
    """Holds a credential without ever showing it in a repr, a traceback or a log line."""

    def __init__(self, value):
        self._value = value
        if value:
            _SECRETS.add(value)

    def reveal(self):
        return self._value

    def __repr__(self):
        return "Secret(***)"

    __str__ = __repr__


class RunnerError(Exception):
    """A failure whose message has been scrubbed; main() prints it and exits 2."""

    def __init__(self, message):
        super().__init__(scrub(message))


def say(message):
    print(scrub(message))


def write_text(path, text):
    with open(path, "w", encoding="utf-8") as f:
        f.write(scrub(text))


def write_json(path, data):
    write_text(path, json.dumps(scrub(data), ensure_ascii=False, indent=1) + "\n")


def safe_errors(errors):
    """Only code, field and a scrubbed, shortened message of each API error."""
    out = []
    for e in errors if isinstance(errors, list) else [errors]:
        if isinstance(e, dict):
            code = (e.get("extensions") or {}).get("code") or e.get("code")
            out.append({"code": scrub(str(code)) if code else None, "field": scrub(e.get("field")) if isinstance(e.get("field"), list) else None,
                        "message": scrub(str(e.get("message", "")))[:300]})
        else:
            out.append({"code": None, "field": None, "message": scrub(str(e))[:300]})
    return out


def keychain_credentials(run=subprocess.run):
    """Client ID (the item's account, not secret) and client secret, from the Keychain item."""
    attrs = run(["security", "find-generic-password", "-s", KEYCHAIN_SERVICE], capture_output=True, text=True)
    if attrs.returncode != 0:
        raise RunnerError("No Keychain item '%s'. Follow docs/localization/registration/APP-SETUP.md step 4." % KEYCHAIN_SERVICE)
    m = re.search(r'"acct"<blob>="([^"]+)"', attrs.stdout)
    if not m:
        raise RunnerError("The Keychain item '%s' has no account (client ID)." % KEYCHAIN_SERVICE)
    secret = run(["security", "find-generic-password", "-s", KEYCHAIN_SERVICE, "-w"], capture_output=True, text=True)
    value = secret.stdout.strip() if secret.returncode == 0 else ""
    if not value:
        raise RunnerError("macOS did not release the secret of '%s' (denied, or empty)." % KEYCHAIN_SERVICE)
    return m.group(1), Secret(value)


# ---- transport -----------------------------------------------------------------------------------

class TransportError(Exception):
    """No HTTP response: the request may or may not have reached Shopify."""


class HttpTransport:
    """POSTs to the store over HTTPS; returns (status, json, retry_after). Never raises with request data."""

    def post(self, path, body, headers):
        req = urllib.request.Request("https://%s%s" % (SHOP, path), data=json.dumps(body).encode("utf-8"),
                                     headers=dict(headers, **{"Content-Type": "application/json"}), method="POST")
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                return resp.status, self._json(resp.read()), resp.headers.get("Retry-After")
        except urllib.error.HTTPError as err:
            return err.code, self._json(err.read()), err.headers.get("Retry-After") if err.headers else None
        except Exception as err:  # noqa: BLE001 - every transport failure becomes a fixed, data-free error
            raise TransportError(type(err).__name__) from None

    @staticmethod
    def _json(raw):
        try:
            return json.loads(raw.decode("utf-8"))
        except (ValueError, UnicodeDecodeError):
            return {"errors": [{"message": "response is not JSON"}]}


class Admin:
    def __init__(self, transport, client_id, secret):
        self.transport = transport
        try:
            status, data, _ = transport.post("/admin/oauth/access_token", {
                "client_id": client_id, "client_secret": secret.reveal(), "grant_type": "client_credentials"}, {})
        except TransportError as err:
            raise RunnerError("Token request failed: network error (%s)." % err) from None
        token = data.get("access_token") if isinstance(data, dict) else None
        if status != 200 or not isinstance(token, str) or not token:
            raise RunnerError("Token request refused (HTTP %d). Check that the app is installed on %s." % (status, SHOP))
        self._token = Secret(token)
        scope = data.get("scope")
        self.scopes = set(s.strip() for s in scope.split(",") if s.strip()) if isinstance(scope, str) else None

    def __repr__(self):
        return "Admin(%s)" % SHOP

    def _post(self, query, variables):
        return self.transport.post("/admin/api/%s/graphql.json" % API_VERSION, {"query": query, "variables": variables},
                                   {"X-Shopify-Access-Token": self._token.reveal()})

    def query(self, query, variables, allow_denied=False):
        """A read, retried on throttling, 5xx and transport failures. Returns data, or None if access is denied and allowed."""
        for attempt in range(READ_RETRIES + 1):
            try:
                status, data, retry_after = self._post(query, variables)
            except TransportError as err:
                if attempt == READ_RETRIES:
                    raise RunnerError("Admin API read failed: network error (%s)." % err) from None
                time.sleep(2 ** attempt)
                continue
            data = data if isinstance(data, dict) else {}
            errors = data.get("errors")
            throttled = status == 429 or "THROTTLED" in json.dumps(errors or "")
            if throttled or status >= 500:
                if attempt == READ_RETRIES:
                    raise RunnerError("Admin API kept failing (HTTP %d); try again later." % status)
                time.sleep(float(retry_after) if retry_after and str(retry_after).replace(".", "", 1).isdigit() else 2 ** attempt)
                continue
            if errors and allow_denied and "ACCESS_DENIED" in json.dumps(errors):
                return None
            if status != 200 or errors or not isinstance(data.get("data"), dict):
                raise RunnerError("Admin API error, HTTP %d: %s" % (status, json.dumps(safe_errors(errors or [{"message": "no data"}]))))
            throttle = (data.get("extensions") or {}).get("cost", {}).get("throttleStatus") or {}
            available = throttle.get("currentlyAvailable")
            if isinstance(available, (int, float)) and available < 200:
                time.sleep((200 - available) / max(throttle.get("restoreRate") or 50, 1))
            return data["data"]
        raise RunnerError("Admin API kept throttling; try again in a minute.")

    def mutate(self, query, variables):
        """One mutation, never retried. Returns (state, payload): confirmed / rejected / unknown."""
        try:
            status, data, _ = self._post(query, variables)
        except TransportError as err:
            return "unknown", {"error": "network error (%s)" % err}
        data = data if isinstance(data, dict) else {}
        if status != 200 or data.get("errors") or not isinstance(data.get("data"), dict):
            state = "unknown" if status >= 500 or status == 0 else "rejected"
            return state, {"status": status, "errors": safe_errors(data.get("errors") or [{"message": "no data"}])}
        return "confirmed", data["data"]

    def pages(self, query, variables, field, allow_denied=False):
        after = None
        while True:
            data = self.query(query, dict(variables, after=after), allow_denied)
            if data is None:
                return
            for part in field.split("."):
                data = data.get(part) if isinstance(data, dict) else None
            if not isinstance(data, dict) or not isinstance(data.get("nodes"), list) or not isinstance(data.get("pageInfo"), dict):
                raise RunnerError("Admin API returned a malformed page for %s." % field)
            for node in data["nodes"]:
                if isinstance(node, dict):
                    yield node
            if not data["pageInfo"].get("hasNextPage"):
                return
            after = data["pageInfo"].get("endCursor")
            if not after:
                raise RunnerError("Admin API returned a next page without a cursor for %s." % field)


# ---- live store ----------------------------------------------------------------------------------

def valid_content(c):
    return (isinstance(c, dict) and isinstance(c.get("key"), str) and c["key"] and isinstance(c.get("value"), str)
            and isinstance(c.get("digest"), str) and c["digest"] and c.get("locale") in (None, "en"))


def clean(node):
    """The node with only valid content entries; the count of invalid ones is kept for the report."""
    content = node.get("translatableContent") if isinstance(node.get("translatableContent"), list) else []
    good = [c for c in content if valid_content(c)]
    trans = [t for t in (node.get("translations") or []) if isinstance(t, dict) and isinstance(t.get("key"), str)]
    return {"resourceId": node.get("resourceId"), "translatableContent": good, "translations": trans, "invalid": len(content) - len(good)}


class Live:
    """Translatable resources fetched once per type or id, with the locale's current translations."""

    def __init__(self, admin, locale):
        self.admin, self.locale = admin, locale
        self.by_type, self.by_id, self.product_fields, self.metaobjects = {}, {}, {}, {}
        self.notes = []

    def of_type(self, rtype):
        if rtype not in self.by_type:
            nodes = [clean(n) for n in self.admin.pages(Q_LIST, {"type": rtype, "locale": self.locale}, "translatableResources")]
            self.by_type[rtype] = [n for n in nodes if isinstance(n["resourceId"], str)]
            for node in self.by_type[rtype]:
                self.by_id[node["resourceId"]] = node
        return self.by_type[rtype]

    def by_ids(self, ids, fresh=False):
        missing = [i for i in ids if fresh or i not in self.by_id]
        for start in range(0, len(missing), 100):
            for node in self.admin.pages(Q_IDS, {"ids": missing[start:start + 100], "locale": self.locale}, "translatableResourcesByIds"):
                node = clean(node)
                if isinstance(node["resourceId"], str):
                    self.by_id[node["resourceId"]] = node
        return [self.by_id[i] for i in ids if i in self.by_id]

    def by_handle(self, rtype, handle):
        handle = handle.split("/")[-1]
        hits = [n for n in self.of_type(rtype) if any(c["key"] == "handle" and c["value"] == handle for c in n["translatableContent"])]
        return hits

    def fields_of(self, product_handle):
        """The product's metafields: {gid: (namespace, key, type, value)}."""
        if product_handle not in self.product_fields:
            hits = self.by_handle("PRODUCT", product_handle)
            out = {}
            if len(hits) == 1:
                for m in self.admin.pages(Q_METAFIELDS, {"id": hits[0]["resourceId"]}, "product.metafields"):
                    if isinstance(m.get("id"), str):
                        out[m["id"]] = (m.get("namespace"), m.get("key"), m.get("type") or "", m.get("value") or "")
            self.product_fields[product_handle] = out
        return self.product_fields[product_handle]

    def metaobject(self, gid=None, type_=None, handle=None):
        """A metaobject's fields (needs read_metaobjects); None when access is denied or it does not exist."""
        key = gid or (type_, handle)
        if key not in self.metaobjects:
            if gid:
                data = self.admin.query(Q_METAOBJECT, {"id": gid}, allow_denied=True)
                obj = data and data.get("metaobject")
            else:
                data = self.admin.query(Q_METAOBJECT_HANDLE, {"type": type_, "handle": handle}, allow_denied=True)
                obj = data and data.get("metaobjectByHandle")
            if data is None:
                self.notes.append("metaobject fields not readable: the token lacks read_metaobjects (APP-SETUP.md step 2)")
            self.metaobjects[key] = obj if isinstance(obj, dict) else None
        return self.metaobjects[key]


def gids_in(value):
    return re.findall(r"gid://shopify/Metaobject/\d+", value or "")


def gid_type(rid):
    m = re.match(r"gid://shopify/([A-Za-z]+)/", rid or "")
    return m.group(1) if m else ""


def theme_owned(rid, theme_id, name):
    """True only if the GID names this template or group and carries the published theme's ID."""
    if not theme_id:
        return False
    parsed = urllib.parse.urlparse(rid)
    if parsed.path.rstrip("/").split("/")[-1] != name:
        return False
    params = urllib.parse.parse_qs(parsed.query)
    return any("theme" in k.lower() and str(theme_id) in v for k, v in params.items())


def key_tokens(key):
    return set(t for t in re.split(r"[.:/\[\]]+", key) if t)


def protected(rid, content):
    """Targets that must never get a translation from this runner."""
    tokens = key_tokens(content["key"])
    return (gid_type(rid) in LOOP_GIDS or any(k in tokens for k in NEVER_KEYS) or "selling_plan" in content["key"]
            or content["value"].strip() in NEVER_VALUES)


def current(node, key):
    for t in node["translations"]:
        if t["key"] == key:
            return {"present": True, "value": t.get("value"), "outdated": bool(t.get("outdated"))}
    return {"present": False, "value": None, "outdated": False}


# ---- resolution ----------------------------------------------------------------------------------

class Scope:
    """The live resources an item may live in, with the identity rule its candidates must pass."""

    def __init__(self, nodes=(), reason=None, rule=None):
        self.nodes, self.reason, self.rule = list(nodes), reason, rule


def scope_for(live, res, theme_id):
    rtype, owner = res["shopify_type"], res["owner"]
    if rtype in UNPROVEN_TYPES:
        return Scope(reason="owner not proven: " + UNPROVEN_TYPES[rtype])
    if rtype in THEME_TYPES:
        if not theme_id:
            return Scope(reason="theme content needs --theme-id (the published theme's ID)")
        name = os.path.basename(owner)[: -len(".json")] if owner.endswith(".json") else owner
        nodes = [n for n in live.of_type(rtype) if theme_owned(n["resourceId"], theme_id, name)]
        return Scope(nodes, None if nodes else "no %s resource proves theme %s and template %s" % (rtype, theme_id, name), "theme")
    if owner.startswith("gid://"):
        nodes = live.by_ids([owner])
        return Scope(nodes, None if nodes else "no live resource %s" % owner, "key")
    if rtype in HANDLE_TYPES:
        hits = live.by_handle(rtype, owner)
        if len(hits) != 1:
            return Scope(reason="%d %s resources with handle %s" % (len(hits), rtype, owner))
        return Scope(hits, None, "key")
    if rtype == "SHOP":
        nodes = live.of_type("SHOP")
        return Scope(nodes, None if len(nodes) == 1 else "%d SHOP resources" % len(nodes), "key")
    if rtype == "METAFIELD":
        return Scope(reason=None, rule="metafield", nodes=[])
    if rtype == "METAOBJECT":
        return Scope(reason=None, rule="metaobject", nodes=[])
    return Scope(reason="type %s not supported" % rtype)


def metafield_nodes(live, owner, field):
    """Translatable metafield resources of the product whose namespace.key matches the field family."""
    family = re.sub(r"#\d+$", "", field)
    ns, _, pattern = family.partition(".")
    fields = live.fields_of(owner)
    ids = [gid for gid, (n, k, _, _) in fields.items() if n == ns and fnmatch.fnmatchcase(k or "", pattern)]
    return live.by_ids(ids), family


def metaobject_nodes(live, owner, field):
    """Metaobjects proven to belong to the item: referenced by the product's metafield, or a shop metaobject by handle."""
    m = re.match(r"^shop\.metaobjects\.([a-z0-9_]+):([a-z0-9_-]+)\.([a-z0-9_]+)$", field)
    if m:
        obj = live.metaobject(type_=m.group(1), handle=m.group(2))
        if not obj:
            return [], "shop metaobject %s:%s not readable or absent" % (m.group(1), m.group(2)), m.group(3)
        return live.by_ids([obj["id"]]), None, m.group(3)
    chain = re.sub(r"#\d+$", "", field).split("|")
    ns, _, key = chain[0].partition(".")
    refs = [g for (n, k, _, v) in live.fields_of(owner).values() if n == ns and k == key for g in gids_in(v)]
    for step in chain[1:]:
        mm = re.match(r"^shop\.metaobjects\.([a-z0-9_]+)$", step)
        if not mm:
            return [], "unknown reference step %s" % step, None
        nxt = []
        for gid in refs:
            obj = live.metaobject(gid=gid)
            if obj is None:
                return [], "nested metaobject fields not readable (read_metaobjects)", None
            for f in obj.get("fields") or []:
                for g in gids_in(f.get("value")):
                    sub = live.metaobject(gid=g)
                    if sub and sub.get("type") == mm.group(1):
                        nxt.append(g)
        refs = nxt
    if not refs:
        return [], "no metaobject referenced by %s on %s" % (chain[0], owner), None
    return live.by_ids(sorted(set(refs))), None, None


def leaves(tree, path=(), parent=None):
    """(path, string, parent key) for every string value in a JSON tree; object keys are never leaves."""
    if isinstance(tree, dict):
        for k, v in tree.items():
            yield from leaves(v, path + (k,), k)
    elif isinstance(tree, list):
        for i, v in enumerate(tree):
            yield from leaves(v, path + (i,), parent)
    elif isinstance(tree, str):
        yield path, tree, parent


def set_path(tree, path, value):
    for p in path[:-1]:
        tree = tree[p]
    tree[path[-1]] = value


def translate_json(value, by_en):
    """The translated JSON text, or (None, blockers). by_en: EN -> list of plan items (any status)."""
    try:
        tree = json.loads(value)
    except ValueError:
        return None, ["the live value is not valid JSON"]
    blockers, mapped = [], 0
    new = json.loads(value)
    for path, text, parent in leaves(tree):
        if parent in STRUCTURAL_KEYS or text.strip() in NEVER_VALUES:
            continue
        items = by_en.get(text, [])
        if not items:
            if not STRUCTURAL_VALUE.match(text):
                blockers.append("text with no plan item: %r" % text)
            continue
        if any(i["hold"] or i["gates"] for i in items):
            blockers.append("held segment: %r (%s)" % (text, "; ".join(sorted(set(h for i in items for h in i["hold"] + i["gates"])))))
            continue
        values = set(i["value"] for i in items)
        if len(values) > 1:
            blockers.append("conflicting translations for %r: %s" % (text, sorted(values)))
            continue
        set_path(new, path, values.pop())
        mapped += 1
    if blockers:
        return None, blockers
    if not mapped:
        return None, ["no text leaf maps to a plan item"]
    compact = ": " not in value and ", " not in value
    out = json.dumps(new, ensure_ascii=False, separators=(",", ":") if compact else None)
    json.loads(out)
    return out, []


def build(plan, live, theme_id, remove_never):
    """The approval snapshot's targets, and a row for every first-wave item."""
    targets, rows = {}, []

    def want(node, content, item_ids, value, how):
        key = (node["resourceId"], content["key"])
        t = targets.setdefault(key, {"action": "register", "resource": node["resourceId"], "key": content["key"],
                                     "en": content["value"], "en_digest": content["digest"],
                                     "current": current(node, content["key"]), "values": {}, "how": how})
        t["values"].setdefault(value, []).extend(item_ids)

    def row(item, res, result, why=None, node=None, content=None):
        r = {"id": item["id"], "type": res["shopify_type"], "result": result, "en": item["en"], "value": item["value"]}
        if why:
            r["why"] = why
        if node is not None:
            r["resource"], r["key"] = node["resourceId"], content["key"] if content else None
        rows.append(r)

    for res in plan["resources"]:
        wave = [i for i in res["items"] if not i["hold"] and not i["gates"]]
        if res["shopify_type"] in LOOP_TYPES:
            for item in wave:
                row(item, res, "skipped", "Loop owns selling-plan translations")
            continue
        if not wave:
            continue
        scope = scope_for(live, res, theme_id)
        if scope.reason:
            for item in wave:
                row(item, res, "not written", scope.reason)
            continue
        if scope.rule == "metafield":
            families = {}
            for item in res["items"]:
                families.setdefault(re.sub(r"#\d+$", "", item["field"]), []).append(item)
            for family, items in families.items():
                if not any(i in wave for i in items):
                    continue
                nodes, _ = metafield_nodes(live, res["owner"], family)
                by_en = {}
                for i in items:
                    by_en.setdefault(i["en"], []).append(i)
                used = set()
                for node in nodes:
                    for content in node["translatableContent"]:
                        if content["key"] != "value" or protected(node["resourceId"], content):
                            continue
                        exact = [i for i in by_en.get(content["value"], [])]
                        if exact:
                            if any(i["hold"] or i["gates"] for i in exact) or len(set(i["value"] for i in exact)) > 1:
                                for i in exact:
                                    if i in wave:
                                        row(i, res, "not written", "held or conflicting items share this value", node, content)
                                    used.add(i["id"])
                                continue
                            want(node, content, [i["id"] for i in exact], exact[0]["value"], "whole value")
                            used.update(i["id"] for i in exact)
                            continue
                        if not (content["value"][:1] in "[{" or (content.get("type") or "").upper() == "JSON"):
                            continue
                        new, blockers = translate_json(content["value"], by_en)
                        try:
                            texts = set(t for _, t, _ in leaves(json.loads(content["value"])))
                        except ValueError:
                            texts = set()
                        in_field = [i for i in items if i["en"] in texts]
                        if blockers:
                            for i in in_field:
                                if i in wave:
                                    row(i, res, "not written", "JSON field kept whole: " + "; ".join(blockers[:5]) +
                                        (" (+%d more)" % (len(blockers) - 5) if len(blockers) > 5 else ""), node, content)
                            used.update(i["id"] for i in in_field)
                            continue
                        want(node, content, [i["id"] for i in in_field if i in wave], new, "JSON field, every text leaf mapped")
                        used.update(i["id"] for i in in_field)
                for i in wave:
                    if i["field"].startswith(family) and i["id"] not in used:
                        row(i, res, "stale", "EN found in no metafield %s of %s (whole value or JSON text)" % (family, res["owner"]))
            continue
        if scope.rule == "metaobject":
            groups = {}
            for item in wave:
                groups.setdefault(item["field"] if item["field"].startswith("shop.") else re.sub(r"#\d+$", "", item["field"]), []).append(item)
            for field, items in groups.items():
                nodes, reason, fixed_key = metaobject_nodes(live, res["owner"], field)
                if reason:
                    for item in items:
                        row(item, res, "not written", "owner not proven: " + reason)
                    continue
                for item in items:
                    cands = [(n, c) for n in nodes for c in n["translatableContent"]
                             if (fixed_key is None or c["key"] == fixed_key) and not protected(n["resourceId"], c)]
                    exact = [(n, c) for n, c in cands if hashlib.sha1(c["value"].encode("utf-8")).hexdigest() == item["en_sha1"]]
                    if len(exact) == 1:
                        want(exact[0][0], exact[0][1], [item["id"]], item["value"], "metaobject field, owner proven")
                    elif not exact:
                        row(item, res, "stale", "EN in no field of the proven metaobjects")
                    else:
                        row(item, res, "ambiguous", "%d fields of the proven metaobjects carry this EN: not written" % len(exact))
            continue
        for item in wave:
            if item["kind"] == "assemble":
                continue
            cands = []
            for node in scope.nodes:
                for content in node["translatableContent"]:
                    if scope.rule == "theme":
                        if not all(h in key_tokens(content["key"]) for h in item.get("hint") or [None]):
                            continue
                    elif item.get("key") and content["key"] != item["key"]:
                        continue
                    elif not item.get("key"):
                        continue
                    cands.append((node, content))
            safe = [(n, c) for n, c in cands if not protected(n["resourceId"], c)]
            if len(cands) != len(safe):
                row(item, res, "not written", "the target is protected (never translate / Loop)")
                continue
            if not safe:
                row(item, res, "missing", "no live key with this identity (%s)" % ("hints " + ", ".join(item.get("hint") or []) if scope.rule == "theme" else "key " + str(item.get("key"))))
            elif len(safe) > 1:
                row(item, res, "ambiguous", "%d live keys pass the identity check: not written" % len(safe))
            elif hashlib.sha1(safe[0][1]["value"].encode("utf-8")).hexdigest() != item["en_sha1"]:
                row(item, res, "stale", "the live EN of this key differs from the plan", safe[0][0], safe[0][1])
            else:
                want(safe[0][0], safe[0][1], [item["id"]], item["value"], "identity, then EN sha1")
        fields = {}
        for item in wave:
            if item["kind"] == "assemble":
                fields.setdefault(item["field"].split("#")[0], []).append(item)
        for field, blocks in fields.items():
            info = res.get("assembled_field") or {}
            ckey = BODY_KEYS.get(field)
            node = scope.nodes[0] if len(scope.nodes) == 1 else None
            content = next((c for c in node["translatableContent"] if c["key"] == ckey), None) if node and ckey else None
            if info.get("missing_or_held") or info.get("gated") or len(blocks) != info.get("blocks", len(blocks)):
                why = "the field has held or missing blocks"
            elif content is None:
                why = "no live key %s" % ckey
            else:
                out, pos, why = content["value"], 0, None
                for b in blocks:
                    at = out.find(b["en"], pos)
                    if at < 0:
                        why = "block %s not in the live value" % b["id"]
                        break
                    out = out[:at] + b["value"] + out[at + len(b["en"]):]
                    pos = at + len(b["value"])
                if not why:
                    want(node, content, [b["id"] for b in blocks], out, "body assembled from %d blocks" % len(blocks))
                    continue
            for b in blocks:
                row(b, res, "stale" if "live" in why else "not written", why)

    ops = []
    for (rid, key), t in sorted(targets.items()):
        if len(t["values"]) > 1:
            for value, ids in t["values"].items():
                for iid in ids:
                    rows.append({"id": iid, "result": "conflict", "resource": rid, "key": key, "value": value,
                                 "why": "%d plan items want different values on this key: not written" % len(t["values"])})
            continue
        value, ids = next(iter(t["values"].items()))
        same = t["current"]["present"] and t["current"]["value"] == value and not t["current"]["outdated"]
        for iid in ids:
            rows.append({"id": iid, "result": "same" if same else ("overwrite" if t["current"]["present"] else "new"),
                         "resource": rid, "key": key, "value": value})
        if not same:
            ops.append({"action": "register", "resource": rid, "key": key, "en": t["en"], "en_digest": t["en_digest"],
                        "current": t["current"], "value": value, "items": sorted(ids), "how": t["how"]})
    removals = []
    scan = list(live.of_type("METAOBJECT"))
    if theme_id:
        for rtype in THEME_TYPES:
            scan += [n for n in live.of_type(rtype) if theme_owned(n["resourceId"], theme_id, urllib.parse.urlparse(n["resourceId"]).path.split("/")[-1])]
    for node in scan:
        for content in node["translatableContent"]:
            exact_key = content["key"] in NEVER_KEYS if gid_type(node["resourceId"]) == "Metaobject" else any(k in key_tokens(content["key"]) for k in NEVER_KEYS)
            if not (exact_key or content["value"].strip() in NEVER_VALUES):
                continue
            cur = current(node, content["key"])
            if cur["present"]:
                removals.append({"action": "remove", "resource": node["resourceId"], "key": content["key"], "en": content["value"],
                                 "en_digest": content["digest"], "current": cur, "value": None, "items": [], "how": "never translate"})
    reg_targets = {(o["resource"], o["key"]) for o in ops}
    if reg_targets & {(o["resource"], o["key"]) for o in removals}:
        raise RunnerError("Internal check failed: a target is in both the register and the remove set.")
    if any(protected(o["resource"], {"key": o["key"], "value": o["en"]}) for o in ops):
        raise RunnerError("Internal check failed: a protected target is in the register set.")
    return ops + (removals if remove_never else []), removals, rows


def plan_hash(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def snapshot(locale, theme_id, plan_sha, remove_never, ops):
    return {"store": SHOP, "api": API_VERSION, "locale": locale, "theme_id": theme_id, "plan_sha256": plan_sha,
            "remove_never": remove_never, "ops": [{k: o[k] for k in ("action", "resource", "key", "en_digest", "current", "value")} for o in ops]}


def checksum(snap):
    canon = json.dumps(snap, ensure_ascii=False, sort_keys=True)
    return hashlib.sha256(canon.encode("utf-8")).hexdigest()[:16]


# ---- report --------------------------------------------------------------------------------------

def block(text):
    """A fenced block that shows text literally, whatever backticks it holds."""
    text = "" if text is None else text
    fence = "`" * max(3, max((len(m) for m in re.findall(r"`+", text)), default=0) + 1)
    return "%stext\n%s\n%s" % (fence, text, fence)


def cell(text):
    return (text or "").replace("\\", "\\\\").replace("|", "\\|").replace("<", "&lt;").replace("\n", " ")


def report(locale, theme_id, remove_never, ops, removals, rows, check, notes):
    counts = {}
    for r in rows:
        counts[r["result"]] = counts.get(r["result"], 0) + 1
    regs = [o for o in ops if o["action"] == "register"]
    lines = ["# Live dry run · %s" % locale.upper(), "",
             "Read only: nothing was written. Store %s, API %s, theme %s, %s." % (SHOP, API_VERSION, theme_id or "not in scope (no --theme-id)",
                                                                              time.strftime("%Y-%m-%d %H:%M %Z")),
             "NL and FR are published: an approved write is live at once.", "",
             "| Item result | Items |", "|---|---:|"] + ["| %s | %d |" % (k, v) for k, v in sorted(counts.items())]
    lines += ["", "**Mutations in this approval:** %d register, %d remove%s. **Checksum `%s`.**" % (
        len(regs), sum(o["action"] == "remove" for o in ops),
        "" if remove_never or not removals else " (%d removals proposed, not approved: rerun with --remove-never)" % len(removals), check), "",
        "To write exactly this:", "", "```sh",
        "python3 docs/localization/registration/register.py --lang %s%s%s --write --approve %s" % (
            locale, " --theme-id %s" % theme_id if theme_id else "", " --remove-never" if remove_never else "", check), "```", ""]
    for note in sorted(set(notes)):
        lines += ["> %s" % note, ""]
    lines += ["## Mutations (%d)" % len(ops), ""]
    for n, o in enumerate(ops, 1):
        cur = o["current"]
        lines += ["### %d. %s `%s` · `%s`" % (n, o["action"], o["resource"], o["key"]), "",
                  "- Plan items: %s" % (", ".join("`%s`" % i for i in o["items"]) or "none (never-translate key)"),
                  "- How: %s; EN digest `%s`" % (o["how"], o["en_digest"]),
                  "- Current %s: %s" % (locale.upper(), "none" if not cur["present"] else ("present, outdated" if cur["outdated"] else "present")), "",
                  "<details><summary>EN</summary>", "", block(o["en"]), "", "</details>", ""]
        if cur["present"]:
            lines += ["<details><summary>Current %s (replaced)</summary>" % locale.upper(), "", block(cur["value"]), "", "</details>", ""]
        lines += (["<details open><summary>New %s</summary>" % locale.upper(), "", block(o["value"]), "", "</details>", ""]
                  if o["action"] == "register" else ["Removed: the %s translation of this key goes; the EN shows." % locale.upper(), ""])
    if removals and not remove_never:
        lines += ["## Proposed removals, not in this approval (%d)" % len(removals), "",
                  "| Resource | Key | EN | Current |", "|---|---|---|---|"]
        lines += ["| `%s` | `%s` | %s | %s |" % (o["resource"], o["key"], cell(o["en"]), cell(o["current"]["value"])) for o in removals]
        lines.append("")
    for title, results in (("Not written: stale, missing, ambiguous, conflict or unproven", ("stale", "missing", "ambiguous", "conflict", "not written")),
                           ("Already equal to the plan", ("same",)), ("Skipped: Loop", ("skipped",))):
        sel = [r for r in rows if r["result"] in results]
        if not sel:
            continue
        lines += ["## %s (%d)" % (title, len(sel)), "", "| Item | Result | Resource · key | EN | Why |", "|---|---|---|---|---|"]
        lines += ["| `%s` | %s | %s | %s | %s |" % (r["id"], r["result"], cell("%s · %s" % (r.get("resource") or "—", r.get("key") or "—")),
                                                  cell(r.get("en")), cell(r.get("why"))) for r in sel]
        lines.append("")
    return "\n".join(lines)


# ---- write ---------------------------------------------------------------------------------------

class Journal:
    """Appends one scrubbed JSON line per event and flushes it at once, so a crash keeps what happened."""

    def __init__(self, path, run_id):
        self.path, self.run_id = path, run_id

    def log(self, **event):
        line = json.dumps(scrub(dict(event, run=self.run_id, at=time.strftime("%Y-%m-%dT%H:%M:%S%z"))), ensure_ascii=False)
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(line + "\n")
            f.flush()


def preconditions_hold(live, ops):
    """Re-read each resource and compare EN digest and current translation of every op."""
    fresh = {n["resourceId"]: n for n in live.by_ids(sorted(set(o["resource"] for o in ops)), fresh=True)}
    for o in ops:
        node = fresh.get(o["resource"])
        content = next((c for c in node["translatableContent"] if c["key"] == o["key"]), None) if node else None
        if not content or content["digest"] != o["en_digest"] or current(node, o["key"]) != o["current"]:
            return False, "%s %s changed since the dry run" % (o["resource"], o["key"])
        if o["action"] == "register" and protected(o["resource"], content):
            return False, "%s %s is protected" % (o["resource"], o["key"])
    return True, None


def write(admin, live, locale, ops, journal):
    """Mutations per resource in chunks; stops at the first precondition failure, rejection or unknown outcome."""
    by_res = {}
    for o in ops:
        by_res.setdefault((o["resource"], o["action"]), []).append(o)
    accepted = 0
    for (resource, action), items in sorted(by_res.items()):
        size = REGISTER_CHUNK if action == "register" else REMOVE_CHUNK
        for start in range(0, len(items), size):
            chunk = items[start:start + size]
            ok, why = preconditions_hold(live, chunk)
            if not ok:
                journal.log(event="stopped", reason=why)
                raise RunnerError("Stopped before writing %s: %s. Run the dry run again." % (resource, why))
            if action == "register" and any(not o["en_digest"] for o in chunk):
                raise RunnerError("Refused: an operation on %s has no EN digest." % resource)
            keys = [o["key"] for o in chunk]
            journal.log(event="attempt", action=action, resource=resource, keys=keys)
            if action == "register":
                state, data = admin.mutate(M_REGISTER, {"id": resource, "translations": [
                    {"key": o["key"], "locale": locale, "value": o["value"], "translatableContentDigest": o["en_digest"]} for o in chunk]})
                payload = (data.get("translationsRegister") or {}) if state == "confirmed" else {}
            else:
                state, data = admin.mutate(M_REMOVE, {"id": resource, "keys": keys, "locales": [locale]})
                payload = (data.get("translationsRemove") or {}) if state == "confirmed" else {}
            done = sorted(t.get("key") for t in (payload.get("translations") or []) if isinstance(t, dict))
            errors = safe_errors(payload.get("userErrors") or []) if state == "confirmed" else data.get("errors", [data.get("error")])
            journal.log(event="result", action=action, resource=resource, state=state, requested=keys, confirmed=done, errors=errors)
            accepted += len(done)
            if state != "confirmed" or errors:
                raise RunnerError("%s on %s: %s (%d keys confirmed so far; see the journal). Run the dry run again before retrying."
                                  % (action, resource, "outcome unknown" if state == "unknown" else "rejected", accepted))
    return accepted


def main(argv=None, transport=None, credentials=None, out=LIVE, plans=PLAN):
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--lang", choices=("nl", "fr", "both"), default="both")
    parser.add_argument("--theme-id", help="the published theme's numeric ID; theme content is out of scope without it")
    parser.add_argument("--remove-never", action="store_true", help="include removals of never-translate translations")
    parser.add_argument("--write", action="store_true", help="write; needs --approve")
    parser.add_argument("--approve", help="the checksum of the dry run Victor approved")
    args = parser.parse_args(argv)
    try:
        if args.write and (args.lang == "both" or not args.approve):
            raise RunnerError("--write needs one --lang and --approve <checksum> from that language's dry run.")
        client_id, secret = credentials() if credentials else keychain_credentials()
        admin = Admin(transport or HttpTransport(), client_id, secret)
        if args.write and (admin.scopes is None or "write_translations" not in admin.scopes):
            raise RunnerError("The token does not show the write_translations scope (APP-SETUP.md step 2); nothing written.")
        os.makedirs(out, exist_ok=True)
        for locale in (("nl", "fr") if args.lang == "both" else (args.lang,)):
            path = plans % locale
            plan = json.load(open(path, encoding="utf-8"))
            live = Live(admin, locale)
            ops, removals, rows = build(plan, live, args.theme_id, args.remove_never)
            snap = snapshot(locale, args.theme_id, plan_hash(path), args.remove_never, ops)
            check = checksum(snap)
            if not args.write:
                write_text(os.path.join(out, "dry-run-%s.md" % locale), report(locale, args.theme_id, args.remove_never, ops, removals, rows, check, live.notes) + "\n")
                write_json(os.path.join(out, "dry-run-%s.json" % locale), {"checksum": check, "snapshot": snap, "ops": ops, "rows": rows})
                say("%s: %d register, %d remove in this approval; checksum %s; report %s/dry-run-%s.md" % (
                    locale, sum(o["action"] == "register" for o in ops), sum(o["action"] == "remove" for o in ops), check, out, locale))
                continue
            if check != args.approve:
                raise RunnerError("%s: the live store, the plan or the options changed since the approved dry run (checksum %s, approved %s). "
                                  "Nothing written; run the dry run again." % (locale, check, args.approve))
            journal = Journal(os.path.join(out, "journal-%s.jsonl" % locale), "%s-%s" % (time.strftime("%Y%m%dT%H%M%S"), check))
            journal.log(event="start", checksum=check, ops=len(ops))
            accepted = write(admin, live, locale, ops, journal)
            journal.log(event="end", confirmed=accepted)
            say("%s: %d keys confirmed; journal %s/journal-%s.jsonl" % (locale, accepted, out, locale))
    except RunnerError as err:
        print(str(err), file=sys.stderr)
        sys.exit(2)
    except Exception as err:  # noqa: BLE001 - an unexpected failure prints only its scrubbed type and message
        print(scrub("Internal error (%s): %s" % (type(err).__name__, err))[:500], file=sys.stderr)
        sys.exit(3)


if __name__ == "__main__":
    main()
