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
- theme content only in resources whose GID names the template and carries the supplied --theme-id in a
  THEME_PARAMS parameter, with every hint as an exact token of the key; without --theme-id it is out of scope.
  The ID must be numeric and proven published: by themes(roles: MAIN) when the token may read themes, or by
  --theme-attested "<today> <name>" from the operator; the proof is part of the approval and is checked again
  when writing;
- direct items only on their own key; product metafields only by namespace and key; metaobjects only
  through the product's metafield references (nested references need read_metaobjects), and only on a field
  the inventory names or that a reviewed bindings.json binds; the dry run proposes bindings, never writes them;
- menu links and shop policies have no proven owner route yet and are never written.
The report ends with the API contract the run saw (scopes, sample GIDs and keys, invalid content).
Exactly one target is written. None is stale or missing, several are ambiguous, and two plan items that
want different values on one target are a conflict: none of these is written. Protected targets
(selling plans and groups, handle_item, selling_plan_id, the Subscription Name values) are never
registered; existing translations on them are proposed for removal, which is part of the approval only
with --remove-never. A JSON field is written only when every text leaf maps to an approved item.

Approval binds a snapshot: store, API version, theme and its proof, plan file, bindings file, removal choice,
and per target the live EN digest, the current NL/FR (present, value, outdated) and the new value. Write
rebuilds the snapshot and writes only if its checksum is the approved one, re-reads each resource right
before its mutation (a resource the re-read omits fails), and stops at the first difference. A mutation
counts as confirmed only with its expected payload, no user errors and exactly the requested keys; anything
else is unknown and stops the run. A translation edited between that re-read and the mutation is not
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
import shlex
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

SHOP = "karmicares.myshopify.com"
API_VERSION = "2026-10"
FORM = "application/x-www-form-urlencoded"
KEYCHAIN_SERVICE = "karmicare-translations"
PLAN = "docs/localization/registration/plan-%s.json"
LIVE = "docs/localization/registration/live"
LOOP_TYPES = ("SELLING_PLAN", "SELLING_PLAN_GROUP")
LOOP_GIDS = ("SellingPlan", "SellingPlanGroup")
NEVER_KEYS = ("handle_item", "selling_plan_id")
NEVER_VALUES = ("60-Day Supply", "Year Supply")
THEME_TYPES = ("ONLINE_STORE_THEME_JSON_TEMPLATE", "ONLINE_STORE_THEME_SECTION_GROUP")
# The GID query parameter that carries the theme ID; confirm against the first read-only run's contract section.
THEME_PARAMS = ("theme_id",)
BINDINGS = "docs/localization/registration/bindings.json"
HANDLE_TYPES = ("PRODUCT", "PAGE", "ARTICLE", "BLOG", "COLLECTION")
UNPROVEN_TYPES = {"LINK": "menu links: no verified owner route (menu -> link) yet",
                  "SHOP_POLICY": "shop policies: no verified owner route (policy type -> resource) yet"}
BODY_KEYS = {"body_html": "body_html", "summary_html": "summary_html", "body": "body_html"}
RICH_TEXT_TYPES = {"root", "paragraph", "heading", "list", "list-item", "link", "text"}
RICH_TEXT_FIELDS = {"type", "url", "target", "listType", "level"}
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
Q_MAIN_THEME = """query { themes(first: 2, roles: [MAIN]) { nodes { id } } }"""
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


# What Shopify may say in an error, by allowlist only (R18g: fail closed). A code, a field-path element or a
# message outside these is shown as "withheld (n chars)"; nothing from a response is decoded or searched.
ERROR_CODES = frozenset((
    # TranslationErrorCode (translationsRegister / translationsRemove userErrors)
    "BLANK", "INVALID", "INVALID_CODE", "INVALID_FORMAT", "INVALID_KEY_FOR_MODEL", "INVALID_LOCALE_FOR_SHOP",
    "INVALID_TRANSLATABLE_CONTENT", "INVALID_VALUE_FOR_HANDLE_TRANSLATION", "RESOURCE_NOT_FOUND",
    "RESOURCE_NOT_MARKET_CUSTOMIZABLE", "RESOURCE_NOT_TRANSLATABLE", "TOO_MANY_KEYS_FOR_RESOURCE",
    "FAILS_RESOURCE_VALIDATION", "INVALID_MARKET_LOCALIZABLE_CONTENT", "MARKET_CUSTOM_CONTENT_NOT_ALLOWED",
    "MARKET_DOES_NOT_EXIST", "MARKET_LOCALE_CREATION_FAILED",
    # GraphQL top-level error extensions
    "ACCESS_DENIED", "THROTTLED", "MAX_COST_EXCEEDED", "INTERNAL_SERVER_ERROR", "BAD_USER_INPUT",
    "GRAPHQL_VALIDATION_FAILED", "SHOP_INACTIVE", "NOT_FOUND",
))
FIELD_PARTS = frozenset(("translations", "keys", "key", "value", "locale", "resourceId", "id", "marketId",
                         "translatableContentDigest", "input", "translationKeys", "locales"))
ERROR_MESSAGES = frozenset((
    "Translation key is invalid", "Value can't be blank", "Key is invalid", "Locale is invalid",
    "Locale is not enabled for this shop", "Translatable content hash is invalid", "Translatable content is invalid",
    "Resource does not exist", "Resource is not translatable", "Too many keys for resource", "Access denied",
    "Throttled", "Internal error", "Internal error. Looks like something went wrong on our end.",
    "response is not JSON", "no data", "server error",
))
MAX_ERROR_TEXT = 300


def _allowed(value, allowed):
    """value itself when it is a short string in the allowlist; otherwise only its length."""
    if isinstance(value, str) and len(value) <= MAX_ERROR_TEXT and value in allowed:
        return value
    size = len(value) if isinstance(value, str) else len(str(type(value).__name__))
    return "withheld (%d chars)" % size


def _field_part(part):
    if isinstance(part, int) and not isinstance(part, bool) and 0 <= part < 100000:
        return str(part)
    if isinstance(part, str) and len(part) <= 5 and part.isdigit():
        return part
    return _allowed(part, FIELD_PARTS)


def safe_errors(errors):
    """Code, field path and message of each API error, each shown only when it is in our allowlist (R18g)."""
    out = []
    for e in (errors if isinstance(errors, list) else [errors])[:20]:
        if isinstance(e, dict):
            code = (e.get("extensions") or {}).get("code") if isinstance(e.get("extensions"), dict) else None
            code = code or e.get("code")
            field = e.get("field") if isinstance(e.get("field"), list) else None
            out.append({"code": _allowed(code, ERROR_CODES) if code else None,
                        "field": [_field_part(f) for f in field[:10]] if field is not None else None,
                        "message": _allowed(e.get("message", ""), ERROR_MESSAGES)})
        else:
            out.append({"code": None, "field": None, "message": _allowed(e, ERROR_MESSAGES)})
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
        headers = dict({"Content-Type": "application/json"}, **headers)
        form = headers["Content-Type"] == FORM
        data = urllib.parse.urlencode(body) if form else json.dumps(body)
        req = urllib.request.Request("https://%s%s" % (SHOP, path), data=data.encode("utf-8"), headers=headers, method="POST")
        try:  # one boundary for the request, both response reads and the parse (R18h-2)
            try:
                with urllib.request.urlopen(req, timeout=60) as resp:
                    status, raw, retry = resp.status, resp.read(), resp.headers.get("Retry-After")
            except urllib.error.HTTPError as err:
                status, raw, retry = err.code, err.read(), err.headers.get("Retry-After") if err.headers else None
            return int(status), self._json(raw), retry
        except Exception as err:  # noqa: BLE001 - every transport failure becomes a fixed, data-free error
            raise TransportError(type(err).__name__) from None

    @staticmethod
    def _json(raw):
        try:
            return json.loads(raw.decode("utf-8"))
        except (ValueError, UnicodeDecodeError):
            # Never reflect a response body: an echoed credential can arrive encoded or cut (R18e-1). Only a known
            # OAuth code is kept, as our own constant.
            out = {"errors": [{"message": "response is not JSON"}]}
            m = re.search(rb"oauth error ([a-z_]{1,64})", raw[:65536], re.I)  # bounded, linear
            code = m.group(1).decode("ascii").lower() if m else None
            if code in OAUTH_ERRORS:
                out["oauth_error"] = code
            return out


# Known OAuth error codes and our own explanation. A refused token request shows nothing else from the response.
OAUTH_ERRORS = {
    "shop_not_permitted": "client credentials are not allowed on this store: the app and the store must belong to "
                          "the same Shopify organization (Dev Dashboard > Stores)",
    "application_cannot_be_found": "Shopify knows no app with this client ID: check the account of the Keychain item "
                                   "(APP-SETUP.md step 4)",
    "invalid_client": "client ID or client secret rejected: check the Keychain item (APP-SETUP.md step 4)",
    "invalid_request": "Shopify could not read the token request",
    "unauthorized_client": "this app may not use the client credentials grant",
    "unsupported_grant_type": "the client credentials grant is not accepted for this app",
    "invalid_scope": "the requested scopes are not granted to this app",
}


def oauth_error(data):
    """A known OAuth error code with our own explanation, or a fixed line; never text from the response."""
    code = None
    if isinstance(data, dict):
        for field in ("error", "oauth_error"):
            value = data.get(field)
            if isinstance(value, str) and value in OAUTH_ERRORS:
                code = value
                break
    return ": %s (%s)" % (code, OAUTH_ERRORS[code]) if code else ": no known OAuth error code in the response"


class Admin:
    def __init__(self, transport, client_id, secret):
        self.transport = transport
        client_id = Secret(client_id)  # scrubbed from every output like the secret (R18e-2)
        try:
            # The token endpoint takes a form-encoded body (Dev Dashboard docs); JSON gets a non-JSON 400.
            status, data, _ = transport.post("/admin/oauth/access_token", {
                "client_id": client_id.reveal(), "client_secret": secret.reveal(), "grant_type": "client_credentials"},
                {"Content-Type": FORM})
        except TransportError as err:
            raise RunnerError("Token request failed: network error (%s)." % err) from None
        token = data.get("access_token") if isinstance(data, dict) else None
        if status != 200 or not isinstance(token, str) or not token:
            raise RunnerError("Token request refused (HTTP %d)%s. Check that the app is installed on %s." % (
                status, oauth_error(data), SHOP))
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
            self.by_type[rtype] = [n for n in nodes if valid_gid(n["resourceId"])]
            for node in self.by_type[rtype]:
                self.by_id[node["resourceId"]] = node
        return self.by_type[rtype]

    def by_ids(self, ids):
        missing = [i for i in ids if i not in self.by_id]
        for start in range(0, len(missing), 100):
            for node in self.admin.pages(Q_IDS, {"ids": missing[start:start + 100], "locale": self.locale}, "translatableResourcesByIds"):
                node = clean(node)
                if valid_gid(node["resourceId"]):
                    self.by_id[node["resourceId"]] = node
        return [self.by_id[i] for i in ids if i in self.by_id]

    def reread(self, ids):
        """Fresh nodes for ids, from this request only: {id: node}; ids the API omits or repeats are absent."""
        seen = {}
        for start in range(0, len(ids), 100):
            for node in self.admin.pages(Q_IDS, {"ids": ids[start:start + 100], "locale": self.locale}, "translatableResourcesByIds"):
                node = clean(node)
                rid = node["resourceId"]
                if isinstance(rid, str) and rid in ids:
                    seen.setdefault(rid, []).append(node)
        return {rid: nodes[0] for rid, nodes in seen.items() if len(nodes) == 1}

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


GID = re.compile(r"gid://shopify/[A-Za-z]{1,64}/[A-Za-z0-9.\-]{1,128}(\?[a-z_]{1,32}=[0-9]{1,20})?")


def valid_gid(rid):
    """A Shopify GID of the shapes this runner uses: type, a plain ID or handle, at most one numeric parameter (R18h-2)."""
    return isinstance(rid, str) and len(rid) <= 256 and GID.fullmatch(rid) is not None


def gid_type(rid):
    m = re.match(r"gid://shopify/([A-Za-z]+)/", rid or "")
    return m.group(1) if m else ""


def theme_owned(rid, theme_id, name):
    """True only if the GID names this template or group and one of THEME_PARAMS holds exactly the supplied theme ID."""
    if not theme_id or not valid_gid(rid):
        return False
    parsed = urllib.parse.urlparse(rid)
    if parsed.path.rstrip("/").split("/")[-1] != name:
        return False
    params = urllib.parse.parse_qs(parsed.query)
    return any(params.get(p) == [str(theme_id)] for p in THEME_PARAMS)


def published_theme(admin):
    """The MAIN theme's numeric ID if the token may read themes, else None (then an operator attestation is needed)."""
    data = admin.query(Q_MAIN_THEME, {}, allow_denied=True)
    nodes = ((data or {}).get("themes") or {}).get("nodes") or []
    if len(nodes) != 1 or not isinstance(nodes[0].get("id"), str):
        return None
    m = re.match(r"^gid://shopify/OnlineStoreTheme/(\d+)$", nodes[0]["id"])
    return m.group(1) if m else None


def theme_proof(admin, theme_id, attested):
    """How the supplied theme ID is known to be published, or a RunnerError."""
    if theme_id is None:
        return None
    if not re.match(r"^\d+$", str(theme_id)):
        raise RunnerError("--theme-id must be the theme's numeric ID.")
    main = published_theme(admin)
    if main is not None:
        if main != str(theme_id):
            raise RunnerError("--theme-id %s is not the published theme (Shopify reports %s)." % (theme_id, main))
        return "read: themes(roles: MAIN)"
    today = time.strftime("%Y-%m-%d")
    if not attested or not re.match(r"^%s \S.*$" % today, attested):
        raise RunnerError("The token cannot read themes: confirm the published theme yourself and pass "
                          "--theme-attested '%s <your name>' (today's date, a space, a name)." % today)
    return "operator: " + attested


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


def leaves(tree, path=(), parent=None, holder=None):
    """(path, string, parent key, containing object) for every string value; object keys are never leaves."""
    if isinstance(tree, dict):
        for k, v in tree.items():
            yield from leaves(v, path + (k,), k, tree)
    elif isinstance(tree, list):
        for i, v in enumerate(tree):
            yield from leaves(v, path + (i,), parent, None)
    elif isinstance(tree, str):
        yield path, tree, parent, holder


def structural(parent, holder):
    """Never translated: never-translate keys anywhere, and the node fields of Shopify rich text."""
    if parent in NEVER_KEYS:
        return True
    return isinstance(holder, dict) and holder.get("type") in RICH_TEXT_TYPES and parent in RICH_TEXT_FIELDS


def set_path(tree, path, value):
    """The tree with the value at path; an empty path replaces the root."""
    if not path:
        return value
    node = tree
    for p in path[:-1]:
        node = node[p]
    node[path[-1]] = value
    return tree


def translate_json(value, by_en):
    """(translated JSON text, [], applied EN texts), or (None, blockers, set()). by_en: EN -> plan items (any status).

    Order per leaf: an explicitly held or gated plan item vetoes the whole field, whatever the leaf's key; so do
    plan items that propose different values for it; then structural leaves and the Subscription Name values
    stay as they are (their plan items are not applied); then the one approved translation replaces the leaf;
    a leaf with no item that is not a URL, GID or number blocks the field."""
    try:
        tree = json.loads(value)
    except ValueError:
        return None, ["the live value is not valid JSON"], set()
    blockers, applied = [], set()
    new = json.loads(value)
    for path, text, parent, holder in leaves(tree):
        items = by_en.get(text, [])
        if any(i["hold"] or i["gates"] for i in items):
            blockers.append("held segment: %r (%s)" % (text, "; ".join(sorted(set(h for i in items for h in i["hold"] + i["gates"])))))
            continue
        values = set(i["value"] for i in items)
        if len(values) > 1:
            blockers.append("conflicting translations for %r: %s" % (text, sorted(values)))
            continue
        if structural(parent, holder) or text.strip() in NEVER_VALUES:
            continue
        if not items:
            if not STRUCTURAL_VALUE.match(text):
                blockers.append("text with no plan item: %r" % text)
            continue
        new = set_path(new, path, values.pop())
        applied.add(text)
    if blockers:
        return None, blockers, set()
    if not applied:
        return None, ["no text leaf maps to a plan item"], set()
    compact = ": " not in value and ", " not in value
    out = json.dumps(new, ensure_ascii=False, separators=(",", ":") if compact else None)
    json.loads(out)
    return out, [], applied


def structure_changes(en_value, current_value):
    """Paths whose untranslated (structural) value differs between the live EN and the current translation."""
    try:
        en, cur = json.loads(en_value), json.loads(current_value)
    except (ValueError, TypeError):
        return ["the current translation is not JSON: the whole field is replaced"] if current_value else []

    def get(tree, path):
        for p in path:
            try:
                tree = tree[p]
            except (KeyError, IndexError, TypeError):
                return None
        return tree
    return ["%s: current %r, new %r" % ("/".join(map(str, path)), get(cur, path), text)
            for path, text, parent, holder in leaves(en) if (structural(parent, holder) or STRUCTURAL_VALUE.match(text))
            and get(cur, path) != text]


def build(plan, live, theme_id, remove_never, bindings=None, proposals=None):
    """The approval snapshot's targets, and a row for every first-wave item.

    bindings: reviewed {item id: {resource, key, en_sha1}} for metaobject items whose field the inventory does not
    name; proposals collects a binding for each unbound item that has exactly one EN match, for review."""
    targets, rows = {}, []
    bindings = bindings or {}
    proposals = {} if proposals is None else proposals

    def want(node, content, item_ids, value, how, notes=()):
        key = (node["resourceId"], content["key"])
        t = targets.setdefault(key, {"action": "register", "resource": node["resourceId"], "key": content["key"],
                                     "en": content["value"], "en_digest": content["digest"],
                                     "current": current(node, content["key"]), "values": {}, "how": how, "notes": []})
        t["values"].setdefault(value, []).extend(item_ids)
        t["notes"].extend(notes)

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
                        new, blockers, applied = translate_json(content["value"], by_en)
                        try:
                            texts = set(leaf[1] for leaf in leaves(json.loads(content["value"])))
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
                        cur = current(node, content["key"])
                        want(node, content, [i["id"] for i in in_field if i in wave and i["en"] in applied], new,
                             "JSON field, every text leaf mapped",
                             structure_changes(content["value"], cur["value"]) if cur["present"] else [])
                        for i in in_field:
                            if i in wave and i["en"] not in applied:
                                row(i, res, "not written", "its text is a structural value in this field and stays as the EN", node, content)
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
                    sha = lambda c: hashlib.sha1(c["value"].encode("utf-8")).hexdigest()
                    bound = bindings.get(item["id"]) if fixed_key is None else None
                    if fixed_key is not None or bound:
                        rid = bound["resource"] if bound else None
                        key = bound["key"] if bound else fixed_key
                        if bound and bound.get("en_sha1") != item["en_sha1"]:
                            row(item, res, "not written", "the binding in bindings.json was made for another EN")
                            continue
                        cands = [(n, c) for n in nodes for c in n["translatableContent"]
                                 if c["key"] == key and (rid is None or n["resourceId"] == rid)]
                        if len(cands) != 1:
                            row(item, res, "missing" if not cands else "ambiguous",
                                "%d proven metaobject fields with key %s%s" % (len(cands), key, " on %s" % rid if rid else ""))
                        elif protected(cands[0][0]["resourceId"], cands[0][1]):
                            row(item, res, "not written", "the target is protected (never translate / Loop)")
                        elif sha(cands[0][1]) != item["en_sha1"]:
                            row(item, res, "stale", "the live EN of the bound field differs from the plan", cands[0][0], cands[0][1])
                        else:
                            want(cands[0][0], cands[0][1], [item["id"]], item["value"],
                                 "metaobject field %s" % ("bound in bindings.json" if bound else "named in the inventory"))
                        continue
                    exact = [(n, c) for n in nodes for c in n["translatableContent"]
                             if sha(c) == item["en_sha1"] and not protected(n["resourceId"], c)]
                    if len(exact) == 1:
                        proposals[item["id"]] = {"resource": exact[0][0]["resourceId"], "key": exact[0][1]["key"],
                                                 "en_sha1": item["en_sha1"], "en": item["en"]}
                        row(item, res, "not written", "field identity not bound: proposed binding in the report (review it into "
                            "bindings.json)", exact[0][0], exact[0][1])
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
                        "current": t["current"], "value": value, "items": sorted(ids), "how": t["how"], "notes": t["notes"]})
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
                                 "en_digest": content["digest"], "current": cur, "value": None, "items": [], "how": "never translate", "notes": []})
    reg_targets = {(o["resource"], o["key"]) for o in ops}
    if reg_targets & {(o["resource"], o["key"]) for o in removals}:
        raise RunnerError("Internal check failed: a target is in both the register and the remove set.")
    if any(protected(o["resource"], {"key": o["key"], "value": o["en"]}) for o in ops):
        raise RunnerError("Internal check failed: a protected target is in the register set.")
    return ops + (removals if remove_never else []), removals, rows


def plan_hash(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest() if os.path.exists(path) else None


def load_bindings(path):
    if not os.path.exists(path):
        return {}
    data = json.load(open(path, encoding="utf-8"))
    out = data.get("bindings") if isinstance(data, dict) else None
    if not isinstance(out, dict) or not all(isinstance(b, dict) and {"resource", "key", "en_sha1"} <= set(b) for b in out.values()):
        raise RunnerError("%s is not {\"bindings\": {item id: {resource, key, en_sha1}}}." % path)
    return out


def snapshot(locale, theme_id, theme_proof_text, plan_sha, bindings_sha, remove_never, ops):
    return {"store": SHOP, "api": API_VERSION, "locale": locale, "theme_id": theme_id, "theme_proof": theme_proof_text,
            "plan_sha256": plan_sha, "bindings_sha256": bindings_sha, "remove_never": remove_never,
            "ops": [{k: o[k] for k in ("action", "resource", "key", "en_digest", "current", "value")} for o in ops]}


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


def contract(live, admin):
    """What the read-only run saw of the API's shapes: scopes, resource GIDs and key formats, invalid content."""
    lines = ["## API contract seen in this run", "",
             "For the review of key formats and ownership (R18b): samples only, no translations.", "",
             "- Token scopes: %s" % (", ".join(sorted(admin.scopes)) if admin.scopes is not None else "not reported by Shopify"), ""]
    lines += ["| Type | Resources | Sample GIDs | Sample keys | Invalid content entries |", "|---|---:|---|---|---:|"]
    for rtype, nodes in sorted(live.by_type.items()):
        gids = ", ".join("`%s`" % n["resourceId"] for n in nodes[:3])
        keys = ", ".join("`%s`" % c["key"] for c in (nodes[0]["translatableContent"][:5] if nodes else []))
        lines.append("| %s | %d | %s | %s | %d |" % (rtype, len(nodes), cell(gids), cell(keys), sum(n.get("invalid", 0) for n in nodes)))
    by_id_only = [n for rid, n in live.by_id.items() if not any(n is m for ns in live.by_type.values() for m in ns)]
    lines.append("| (by ID) | %d | %s | %s | %d |" % (len(by_id_only), cell(", ".join("`%s`" % n["resourceId"] for n in by_id_only[:3])),
                                                  cell(", ".join("`%s`" % c["key"] for c in (by_id_only[0]["translatableContent"][:5] if by_id_only else []))),
                                                  sum(n.get("invalid", 0) for n in by_id_only)))
    return lines + [""]


def write_argv(locale, theme_id, attested, remove_never, check):
    argv = ["--lang", locale]
    if theme_id:
        argv += ["--theme-id", str(theme_id)]
    if attested:
        argv += ["--theme-attested", attested]
    if remove_never:
        argv.append("--remove-never")
    return argv + ["--write", "--approve", check]


def write_command(locale, theme_id, attested, remove_never, check):
    """The write command, each argument shell-quoted, so copying it passes exactly the same options."""
    return shlex.join(["python3", "docs/localization/registration/register.py"] + write_argv(locale, theme_id, attested, remove_never, check))


def report(locale, theme_id, theme_proof_text, attested, remove_never, ops, removals, rows, check, notes, proposals=None, contract_lines=()):
    counts = {}
    for r in rows:
        counts[r["result"]] = counts.get(r["result"], 0) + 1
    regs = [o for o in ops if o["action"] == "register"]
    lines = ["# Live dry run · %s" % locale.upper(), "",
             "Read only: nothing was written. Store %s, API %s, %s." % (SHOP, API_VERSION, time.strftime("%Y-%m-%d %H:%M %Z")),
             "Theme: %s." % ("supplied ID %s, published per %s" % (theme_id, theme_proof_text) if theme_id else "not in scope (no --theme-id)"),
             "NL and FR are published: an approved write is live at once.", "",
             "| Item result | Items |", "|---|---:|"] + ["| %s | %d |" % (k, v) for k, v in sorted(counts.items())]
    lines += ["", "**Mutations in this approval:** %d register, %d remove%s. **Checksum `%s`.**" % (
        len(regs), sum(o["action"] == "remove" for o in ops),
        "" if remove_never or not removals else " (%d removals proposed, not approved: rerun with --remove-never)" % len(removals), check), "",
        "To write exactly this (an operator attestation must carry the date of the write):", "", "```sh",
        write_command(locale, theme_id, attested, remove_never, check), "```", ""]
    for note in sorted(set(notes)):
        lines += ["> %s" % note, ""]
    lines += ["## Mutations (%d)" % len(ops), ""]
    for n, o in enumerate(ops, 1):
        cur = o["current"]
        lines += ["### %d. %s `%s` · `%s`" % (n, o["action"], o["resource"], o["key"]), "",
                  "- Plan items: %s" % (", ".join("`%s`" % i for i in o["items"]) or "none (never-translate key)"),
                  "- How: %s; EN digest `%s`" % (o["how"], o["en_digest"]),
                  "- Current %s: %s" % (locale.upper(), "none" if not cur["present"] else ("present, outdated" if cur["outdated"] else "present")), ""]
        if o.get("notes"):
            lines += ["- **Whole-field change beyond the translated text:** the current %s differs in untranslated values, "
                      "which return to the EN:" % locale.upper()] + ["  - %s" % cell(x) for x in o["notes"]] + [""]
        lines += ["<details><summary>EN</summary>", "", block(o["en"]), "", "</details>", ""]
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
    if proposals:
        lines += ["## Proposed metaobject bindings, not written (%d)" % len(proposals), "",
                  "The inventory names the metaobject family, not the field. Each item below has exactly one field with its EN in the "
                  "proven metaobjects. After review, copy the reviewed entries into `docs/localization/registration/bindings.json` "
                  "(`live/bindings-proposed-<lang>.json` has them in that format); only bound items are written.", "",
                  "| Item | Resource · key | EN |", "|---|---|---|"]
        lines += ["| `%s` | %s | %s |" % (iid, cell("%s · %s" % (p["resource"], p["key"])), cell(p["en"])) for iid, p in sorted(proposals.items())]
        lines.append("")
    return "\n".join(lines + list(contract_lines))


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
    fresh = live.reread(sorted(set(o["resource"] for o in ops)))
    for o in ops:
        node = fresh.get(o["resource"])
        if node is None:
            return False, "%s was not returned (once) by the re-read" % o["resource"]
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
            else:
                state, data = admin.mutate(M_REMOVE, {"id": resource, "keys": keys, "locales": [locale]})
            state, done, errors = confirmation(state, data, action, keys, locale)
            journal.log(event="result", action=action, resource=resource, state=state, requested=keys, confirmed=done, errors=errors)
            accepted += len(done)
            if state != "confirmed":
                raise RunnerError("%s on %s: %s (%d keys confirmed so far; see the journal). Run the dry run again before retrying."
                                  % (action, resource, "outcome unknown" if state == "unknown" else "rejected", accepted))
    return accepted


def confirmation(state, data, action, keys, locale):
    """(state, confirmed keys, errors). Confirmed only if the payload has its expected shape, no user errors, and
    exactly the requested keys in this locale; user errors make it rejected; any other shape is unknown."""
    if state != "confirmed":
        return state, [], data.get("errors", [data.get("error")])
    payload = data.get("translationsRegister" if action == "register" else "translationsRemove")
    if not isinstance(payload, dict) or not isinstance(payload.get("translations"), list) or not isinstance(payload.get("userErrors"), list):
        return "unknown", [], [{"code": None, "field": None, "message": "the mutation returned no %s payload" % action}]
    errors = safe_errors(payload["userErrors"])
    entries = payload["translations"]
    valid = all(isinstance(t, dict) and isinstance(t.get("key"), str) and t.get("locale") == locale for t in entries)
    returned = sorted(t["key"] for t in entries if isinstance(t, dict) and isinstance(t.get("key"), str)) if valid else []
    # Returned keys are only compared, never kept: the confirmed list is our own requested keys, and only when the
    # receipt matches them exactly; otherwise it is empty (R18h-1).
    if errors:
        return "rejected", [], errors
    if not valid:
        return "unknown", [], [{"code": None, "field": None, "message": "a returned entry lacks a string key or the exact locale %s" % locale}]
    if returned != sorted(keys) or len(set(returned)) != len(returned):
        return "unknown", [], [{"code": None, "field": None, "message": "returned keys are not exactly the requested keys, once each"}]
    return "confirmed", sorted(keys), []


def main(argv=None, transport=None, credentials=None, out=LIVE, plans=PLAN, bindings_path=BINDINGS):
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--lang", choices=("nl", "fr", "both"), default="both")
    parser.add_argument("--theme-id", help="the published theme's numeric ID; theme content is out of scope without it")
    parser.add_argument("--theme-attested", help="'YYYY-MM-DD name': the operator checked today that --theme-id is the published "
                                                 "theme (needed when the token cannot read themes)")
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
        proof = theme_proof(admin, args.theme_id, args.theme_attested)
        bindings = load_bindings(bindings_path)
        os.makedirs(out, exist_ok=True)
        for locale in (("nl", "fr") if args.lang == "both" else (args.lang,)):
            path = plans % locale
            plan = json.load(open(path, encoding="utf-8"))
            live = Live(admin, locale)
            proposals = {}
            ops, removals, rows = build(plan, live, args.theme_id, args.remove_never, bindings, proposals)
            snap = snapshot(locale, args.theme_id, proof, plan_hash(path), plan_hash(bindings_path), args.remove_never, ops)
            check = checksum(snap)
            if not args.write:
                write_text(os.path.join(out, "dry-run-%s.md" % locale),
                           report(locale, args.theme_id, proof, args.theme_attested, args.remove_never, ops, removals, rows, check,
                                  live.notes, proposals, contract(live, admin)) + "\n")
                write_json(os.path.join(out, "dry-run-%s.json" % locale), {"checksum": check, "snapshot": snap, "ops": ops, "rows": rows})
                write_json(os.path.join(out, "bindings-proposed-%s.json" % locale), {"bindings": proposals})
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
        raise SystemExit(2) from None
    except Exception as err:  # noqa: BLE001 - an unexpected failure prints only its type, never its text
        print("Internal error (%s); no details are shown. Nothing after this point was written." % type(err).__name__, file=sys.stderr)
        raise SystemExit(3) from None  # no implicit __context__ for a caller that formats the SystemExit (R18i-1)


if __name__ == "__main__":
    main()
