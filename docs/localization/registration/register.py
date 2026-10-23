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
  through the product's reference-typed metafields and reference-typed fields (depth 3; shop-level objects only from
  the reviewed shop-objects.json, pinned to GID and selected the way the storefront selects them: for a compare
  cell, its typed plan and row references both in the table's lists, and no other object of the type with that
  selection, proven against the type's whole list), and only on a field the inventory names, an item a reviewed
  bindings.json binds (both under the same family veto, across all resource groups, and removed when the field
  route finds a held, gated or conflicting segment in the target), or a field a reviewed bindings-fields.json
  binds with unchanged evidence;
  the evidence holds the root metafield GID, every typed path found with each destination's GID, type and handle,
  the table selection (resolved plan and row, table members), the field's EN, every span and the assembled value;
  the dry run proposes field bindings, never writes them; a bound field whose evidence changed aborts the whole
  write before any mutation; every row of a family (held, gated, conflicting or bound elsewhere) vetoes a field,
  structural JSON leaves included; fields with Liquid (also behind JSON escapes or entities), markup it cannot map
  with certainty (unclosed quotes, raw-text elements, ambiguous comments), or split sentences are never proposed;
- theme keys of the shape section.<template>.json.<ids>:<hash> match the inventory's section/block/setting ids
  exactly (a section-level setting never matches its blocks' settings);
- selling plans by their GID, selling-plan groups by their exact EN name (every group with that name, as groups are
  shared by products), and on both only name, description and option1-3;
- menu links and shop policies have no proven owner route yet and are never written.
The report ends with the API contract the run saw (scopes, sample GIDs and keys, invalid content).
Exactly one target is written (selling-plan groups: every group with the EN name). None is stale or missing,
several are ambiguous, and two plan items that want different values on one target are a conflict: none of these
is written. Protected targets (handle_item, selling_plan_id, the Subscription Name values '60-Day Supply' and
'Year Supply', and selling-plan content other than name, description and options) are never registered; existing translations on them are proposed for removal, which is part of the approval only
with --remove-never. A JSON field is written only when every text leaf maps to an approved item.

Approval binds a snapshot: store, API version, theme and its proof, plan file, bindings file, removal choice,
and per target the live EN digest, the current NL/FR (present, value, outdated) and the new value. Write
rebuilds the snapshot and writes only if its checksum is the approved one, re-reads each resource right
before its mutation (a resource the re-read omits fails), and stops at the first difference. A mutation
counts as confirmed only with its expected payload, no user errors and exactly the requested keys; anything
else is unknown and stops the run. A translation edited between that re-read and the mutation is not
detected: the API digest protects the EN only. For bound metaobject fields the writer also re-reads the
provenance, uncached (references, path objects, table selection, the shop type's objects, pinned objects,
field), with the field's EN digest and current translation: before the first mutation for every reviewed field
binding, those already current included, and for each chunk right after its content re-read. A rebuild takes
several reads, not one consistent snapshot, and Shopify has no transaction across references and translations,
so a change after the relevant read is not seen. NL and FR are published: a registered translation is live at
once.

Credentials (APP-SETUP.md): client ID and secret come from the macOS Keychain item
"karmicare-translations", read inside this process; the 24 h token from client_credentials lives in
memory only. Every message, report and journal line passes a scrubber that removes both, and API error
text is reduced to an allowlist of fields.
"""
import argparse
import fnmatch
import hashlib
import html
import html.entities
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
# The only selling-plan content this runner may translate (wave 2a); Subscription Name values stay protected below.
SELLING_PLAN_KEYS = ("name", "description", "option1", "option2", "option3")
# The GID type a plan resource's owner must have (a selling-plan GID can never hide under another type).
OWNER_GID_TYPES = {"MEDIA_IMAGE": "MediaImage", "SELLING_PLAN": "SellingPlan", "SELLING_PLAN_GROUP": "SellingPlanGroup",
                   "METAFIELD": "Metafield", "METAOBJECT": "Metaobject", "PRODUCT": "Product", "PAGE": "Page",
                   "ARTICLE": "Article", "BLOG": "Blog", "COLLECTION": "Collection", "SHOP": "Shop", "LINK": "Link"}
NEVER_KEYS = ("handle_item", "selling_plan_id")
NEVER_VALUES = ("60-Day Supply", "Year Supply")
THEME_TYPES = ("ONLINE_STORE_THEME_JSON_TEMPLATE", "ONLINE_STORE_THEME_SECTION_GROUP")
# The GID query parameter that carries the theme ID; confirm against the first read-only run's contract section.
THEME_PARAMS = ("theme_id",)
BINDINGS = "docs/localization/registration/bindings.json"
# Wave 2b: reviewed field bindings (per locale) and the reviewed shop-level objects the compare table selects.
FIELD_BINDINGS = "docs/localization/registration/bindings-fields.json"
SHOP_OBJECTS = "docs/localization/registration/shop-objects.json"
REFERENCE_TYPES = ("metaobject_reference", "list.metaobject_reference")
REFERENCE_DEPTH = 3
MAX_PATHS = 16  # typed paths kept per object; an object reached more often is blocked, not silently trimmed
MAX_TYPE_PAGES = 200  # pages of 250 read for a shop type's full list; past that the list counts as unknown
# The storefront's selection of a shop-level object (sections/product-compare-plans.liquid): a compare_value cell
# shows in the table when its compare_plan is one of the table's compare_plans and its compare_row one of its
# compare_rows, both typed references; the first matching cell wins. No other shop-level type has a known selector.
SHOP_SELECTORS = {"compare_value": {"compare_plan": "compare_plans", "compare_row": "compare_rows"}}
LIQUID = re.compile(r"\{\{|\{%|\}\}|%\}")
ENTITY = re.compile(r"&(#[0-9]{1,7}|#[xX][0-9A-Fa-f]{1,6}|[A-Za-z][A-Za-z0-9]{1,31});")
TEXT_UNIT = re.compile(r"&(?:#[0-9]{1,7}|#[xX][0-9A-Fa-f]{1,6}|[A-Za-z][A-Za-z0-9]{1,31});|.", re.S)
TAG_NAME = re.compile(r"[A-Za-z][A-Za-z0-9-]*")
ATTR_NAME = re.compile(r"[^\s\"'<>/=`]+")
ATTR_UNQUOTED = re.compile(r"[^\s\"'<>=`]+")
HTML_SPACE = " \t\n\r\f"
# Elements whose content the HTML tokenizer does not read as ordinary text and tags (raw text, RCDATA, foreign content).
RAW_ELEMENTS = ("script", "style", "textarea", "title", "xmp", "iframe", "noembed", "noframes", "noscript", "plaintext", "svg", "math")
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
Q_METAOBJECTS_OF_TYPE = """query($type: String!, $after: String) {
  metaobjects(type: $type, first: 250, after: $after) { nodes { id handle } pageInfo { hasNextPage endCursor } } }"""
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

    def metaobjects_of_type(self, type_):
        """[{id, handle}] of a shop-level type, for the candidate list a reviewer turns into shop-objects.json."""
        key = ("type", type_)
        if key not in self.metaobjects:
            self.metaobjects[key] = [n for n in self.admin.pages(Q_METAOBJECTS_OF_TYPE, {"type": type_}, "metaobjects", allow_denied=True)
                                     if isinstance(n, dict) and valid_gid(n.get("id"))]
        return self.metaobjects[key]

    def all_of_type(self, type_):
        """The GIDs of every metaobject of a type, or None when the list is not known whole: a denied or malformed
        page, a hasNextPage that is not an explicit boolean (only false ends the list, R32d D2), a next page without
        a cursor, a cursor seen before, or more than MAX_TYPE_PAGES pages (R32d N1). It never loops without progress."""
        key = ("all", type_)
        if key not in self.metaobjects:
            ids, after, cursors = [], None, set()
            for _ in range(MAX_TYPE_PAGES):
                data = self.admin.query(Q_METAOBJECTS_OF_TYPE, {"type": type_, "after": after}, allow_denied=True)
                page = data.get("metaobjects") if isinstance(data, dict) else None
                info = page.get("pageInfo") if isinstance(page, dict) else None
                if not isinstance(page, dict) or not isinstance(page.get("nodes"), list) or not isinstance(info, dict) \
                        or not isinstance(info.get("hasNextPage"), bool) \
                        or not all(isinstance(n, dict) and valid_gid(n.get("id")) for n in page["nodes"]):
                    ids = None
                    break
                ids += [n["id"] for n in page["nodes"]]
                if info["hasNextPage"] is False:
                    break
                after = info.get("endCursor")
                if not isinstance(after, str) or not after or after in cursors:
                    ids = None
                    break
                cursors.add(after)
            else:
                ids = None
            self.metaobjects[key] = ids
        return self.metaobjects[key]

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


def theme_path(key):
    """The section/block/setting ids of a theme content key ('section.<template>.json.<ids>:<hash>'), or None."""
    m = re.match(r"^section\.(?:.+?)\.json\.(.+):[^:.]+$", key)
    return m.group(1).split(".") if m else None


def key_tokens(key):
    return set(t for t in re.split(r"[.:/\[\]]+", key) if t)


def protected(rid, content):
    """Targets that must never get a translation from this runner: never-translate keys and values, and on a selling
    plan or group anything but its name, description and options (Loop reads the Subscription Name values, B-01)."""
    tokens = key_tokens(content["key"])
    return ((gid_type(rid) in LOOP_GIDS and content["key"] not in SELLING_PLAN_KEYS)
            or any(k in tokens for k in NEVER_KEYS) or "selling_plan" in content["key"]
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
        if OWNER_GID_TYPES.get(rtype) and gid_type(owner) != OWNER_GID_TYPES[rtype]:
            return Scope(reason="owner %s is not a %s" % (owner, OWNER_GID_TYPES[rtype]))
        nodes = live.by_ids([owner])
        return Scope(nodes, None if nodes else "no live resource %s" % owner, "key")
    if rtype == "SELLING_PLAN_GROUP" and owner.startswith("name: "):
        # Groups are shared by products: every group with this exact EN name gets the same translation.
        nodes = [n for n in live.of_type("SELLING_PLAN_GROUP")
                 if any(c["key"] == "name" and c["value"] == owner[len("name: "):] for c in n["translatableContent"])]
        return Scope(nodes, None if nodes else "no selling-plan group named %r" % owner[len("name: "):], "every")
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


# ---- wave 2b: typed reference walk, raw-span map, field evidence --------------------------------------------

def ref_gids(type_, value):
    """The metaobject GIDs a reference-typed field holds; nothing for any other type (a GID in a text is no edge)."""
    if type_ not in REFERENCE_TYPES or not isinstance(value, str):
        return []
    if type_.startswith("list."):
        try:
            vals = json.loads(value)
        except ValueError:
            return []
        vals = vals if isinstance(vals, list) else []
    else:
        vals = [value]
    return [v for v in vals if isinstance(v, str) and re.fullmatch(r"gid://shopify/Metaobject/\d+", v)]


def shop_selection(fields, table, selector):
    """The storefront's selection of a shop object by a table, as evidence, or None. Every cell field of the selector
    must be a single metaobject reference to one of the GIDs that the table's reference-typed field lists."""
    out = []
    for cf, tf in sorted(selector.items()):
        ct, cv = fields.get(cf, (None, None))
        tt, tv = table["fields"].get(tf, (None, None))
        members = ref_gids(tt, tv)
        picked = ref_gids(ct, cv) if ct == "metaobject_reference" else []
        if len(picked) != 1 or picked[0] not in members:
            return None
        out.append({"cell_field": cf, "cell_type": ct, "value": picked[0], "table_field": tf, "table_type": tt, "table_members": members})
    return out


def reference_objects(live, owner, family, shop_objects):
    """({gid: info}, blocked GIDs, reason). Roots: the product's metafields matching the family's namespace.key whose
    declared type is a metaobject reference. Edges: reference-typed fields only, to REFERENCE_DEPTH. A later step
    shop.metaobjects.<type> adds only the reviewed shop objects of that type (shop-objects.json), pinned to their
    GID and selected the way the storefront selects them (SHOP_SELECTORS) by a table this product reaches.
    info: type, handle, fields and paths: every typed path from the product found in this walk, each edge with its
    source (the product and root metafield GID for the first), field, declared type, and the destination's GID, type
    and handle; a selection edge also carries the pinned entry and the selector's resolved GIDs and table members."""
    chain = re.sub(r"#\d+$", "", family).split("|")
    ns, _, pattern = chain[0].partition(".")
    hits = live.by_handle("PRODUCT", owner)
    pid = hits[0]["resourceId"] if len(hits) == 1 else None
    roots = [(mid, n, k, t, v) for mid, (n, k, t, v) in live.fields_of(owner).items()
             if n == ns and fnmatch.fnmatchcase(k or "", pattern) and t in REFERENCE_TYPES]
    if not roots:
        return {}, set(), "no reference-typed metafield %s on %s" % (chain[0], owner)
    objects, blocked, level = {}, set(), []
    for mid, n, k, t, v in sorted(roots):
        level += [(g, ({"from": pid, "metafield": mid, "via": "%s.%s" % (n, k), "type": t, "to": g},)) for g in ref_gids(t, v)]
    for depth in range(REFERENCE_DEPTH + 1):
        nxt = []
        for g, path in level:
            if any(e["to"] == g for e in path[:-1]):
                continue
            if g in blocked:
                # Every known direct root edge to an unreadable object stays in its evidence (R32c C3).
                if len(path) == 1 and objects.get(g, {}).get("unreadable"):
                    objects[g]["paths"].append([dict(path[0], to_unreadable=True)])
                continue
            obj = live.metaobject(gid=g)
            if obj is None:
                # A root's direct reference stays a candidate (the typed metafield proves it); nothing below it is known.
                blocked.add(g)
                if len(path) == 1:
                    objects.setdefault(g, {"type": None, "handle": None, "fields": {}, "paths": [], "unreadable": True})["paths"].append(
                        [dict(path[0], to_unreadable=True)])
                continue
            path = path[:-1] + (dict(path[-1], to_type=obj.get("type"), to_handle=obj.get("handle")),)
            fields = {f.get("key"): (f.get("type"), f.get("value")) for f in obj.get("fields") or [] if isinstance(f, dict)}
            info = objects.setdefault(g, {"type": obj.get("type"), "handle": obj.get("handle"), "fields": fields, "paths": []})
            if len(info["paths"]) >= MAX_PATHS:
                blocked.add(g)
                continue
            info["paths"].append(list(path))
            if depth < REFERENCE_DEPTH:
                nxt += [(h, path + ({"from": g, "via": fk, "type": ft, "to": h},)) for fk, (ft, fv) in sorted(fields.items()) for h in ref_gids(ft, fv)]
        level = nxt
    # Nothing below a blocked object counts: drop every object one of whose paths passes through one.
    for g in [g for g, o in objects.items() if g in blocked and not o.get("unreadable")
              or any(e["to"] in blocked for p in o["paths"] for e in p[:-1])]:
        objects.pop(g)
        blocked.add(g)
    tables = {g: o for g, o in objects.items() if not o.get("unreadable") and any(len(p) == 1 for p in o["paths"])}
    for step in chain[1:]:
        m = re.match(r"^shop\.metaobjects\.([a-z0-9_]+)$", step)
        if not m:
            return {}, blocked, "unknown reference step %s" % step
        selector = SHOP_SELECTORS.get(m.group(1))
        if selector is None:
            return {}, blocked, "no storefront selector is known for shop.metaobjects.%s" % m.group(1)
        entries = shop_objects.get(m.group(1), [])
        if not entries:
            continue
        matches = []
        for entry in entries:
            obj = live.metaobject(type_=m.group(1), handle=entry["handle"])
            if not obj or obj.get("id") != entry["gid"] or obj.get("type") != m.group(1):
                blocked.add(entry["gid"])
                continue
            fields = {f.get("key"): (f.get("type"), f.get("value")) for f in obj.get("fields") or [] if isinstance(f, dict)}
            for tg, table in sorted(tables.items()):
                sel = shop_selection(fields, table, selector)
                if sel is not None:
                    matches.append((entry, obj, fields, tg, table, sel))
        # The storefront shows the first cell of the whole type with a selection, in an order not known here: a
        # reviewed cell counts only when no other object of the type has its selection (R32c C6). Every object of the
        # type is read for this proof, never as a target; a list or object that cannot be read blocks every match.
        count, everyone = {}, live.all_of_type(m.group(1))
        others = [] if everyone is None else [live.metaobject(gid=g) for g in everyone]
        if everyone is None or any(o is None for o in others) or any(e["gid"] not in everyone for e, *_ in matches):
            blocked.update(e["gid"] for e, *_ in matches)
            continue
        for o in others:
            fields = {f.get("key"): (f.get("type"), f.get("value")) for f in o.get("fields") or [] if isinstance(f, dict)}
            for tg, table in sorted(tables.items()):
                sel = shop_selection(fields, table, selector)
                if sel is not None:
                    count.setdefault((tg, tuple(s["value"] for s in sel)), set()).add(o.get("id"))
        clash = set(e["gid"] for e, _, _, tg, _, sel in matches if len(count.get((tg, tuple(s["value"] for s in sel)), ())) != 1)
        blocked.update(clash)
        for entry, obj, fields, tg, table, sel in matches:
            if entry["gid"] in clash:
                continue
            info = objects.setdefault(entry["gid"], {"type": obj.get("type"), "handle": obj.get("handle"), "fields": fields, "paths": []})
            info["paths"] += [p + [{"from": tg, "via": "storefront selection", "type": "selection", "to": entry["gid"],
                                    "to_type": obj.get("type"), "to_handle": obj.get("handle"),
                                    "pinned": {"handle": entry["handle"], "gid": entry["gid"]}, "selector": sel}]
                              for p in table["paths"] if len(p) == 1]
    for o in objects.values():
        o["paths"].sort(key=lambda p: json.dumps(p, sort_keys=True))
    return objects, blocked, None


def scan_tag(value, i):
    """((name, end), None) for the tag that starts at value[i] == '<', or (None, reason). Quote-aware: a '>' inside a
    quoted attribute value belongs to the tag. Only `<name attr attr=v attr="v" attr='v'>` (optionally `/>`) and
    `</name>` are accepted; an unclosed quote, attributes without whitespace between them or any other shape refuse."""
    n, j = len(value), i + 1
    closing = value.startswith("/", j)
    j += closing
    m = TAG_NAME.match(value, j)
    if not m:
        return None, "malformed tag at offset %d" % i
    name, j = m.group(0).lower(), m.end()
    if closing:
        while j < n and value[j] in HTML_SPACE:
            j += 1
        return ((name, j + 1), None) if j < n and value[j] == ">" else (None, "malformed end tag at offset %d" % i)
    while True:
        start = j
        while j < n and value[j] in HTML_SPACE:
            j += 1
        if j >= n:
            return None, "unclosed tag at offset %d" % i
        if value[j] == ">":
            return (name, j + 1), None
        if value.startswith("/>", j):
            return (name, j + 2), None
        a = ATTR_NAME.match(value, j) if j > start else None
        if not a:
            return None, "malformed attribute at offset %d" % j
        j = k = a.end()
        while k < n and value[k] in HTML_SPACE:
            k += 1
        if k < n and value[k] == "=":
            k += 1
            while k < n and value[k] in HTML_SPACE:
                k += 1
            if k < n and value[k] in "\"'":
                e = value.find(value[k], k + 1)
                if e < 0:
                    return None, "unclosed attribute quote at offset %d" % k
                j = e + 1
            else:
                u = ATTR_UNQUOTED.match(value, k)
                if not u:
                    return None, "malformed attribute value at offset %d" % k
                j = u.end()


def scan_html(value):
    """([(kind, start, end)] covering the value exactly once, None) or (None, reason). Tags and comments are opaque;
    text runs between them must hold only well-formed entities. Raw-text, RCDATA and foreign elements (script, style,
    textarea, title, svg ...), declarations, processing instructions, unclosed quotes or brackets, stray '>' and
    comments the HTML tokenizer would close elsewhere (`<!-->`, `<!--->`, `--!>`) refuse."""
    spans, i, n = [], 0, len(value)
    while i < n:
        if value.startswith("<!--", i):
            if value.startswith("<!-->", i) or value.startswith("<!--->", i):
                return None, "abruptly closed comment at offset %d" % i
            j = value.find("-->", i + 4)
            if j < 0:
                return None, "unterminated comment"
            if "--!>" in value[i + 4:j + 3] or "<!--" in value[i + 4:j]:
                return None, "ambiguous comment at offset %d" % i
            spans.append(("comment", i, j + 3))
            i = j + 3
            continue
        if value.startswith("<!", i) or value.startswith("<?", i):
            return None, "declaration or processing instruction at offset %d" % i
        if value[i] == "<":
            tag, reason = scan_tag(value, i)
            if tag is None:
                return None, reason
            if tag[0] in RAW_ELEMENTS:
                return None, "%s element (its content is not ordinary text)" % tag[0]
            spans.append(("tag", i, tag[1]))
            i = tag[1]
            continue
        if value[i] == ">":
            return None, "stray '>' at offset %d" % i
        j = i
        while j < n and value[j] not in "<>":
            j += 1
        k = i
        while True:
            a = value.find("&", k, j)
            if a < 0:
                break
            m = ENTITY.match(value, a)
            if not m or m.end() > j or (not m.group(1).startswith("#") and m.group(1) + ";" not in html.entities.html5):
                return None, "bad entity at offset %d" % a
            k = m.end()
        spans.append(("text", i, j))
        i = j
    if [s for _, s, _ in spans] != [0] + [e for _, _, e in spans[:-1]] or (spans and spans[-1][2] != n):
        return None, "the spans do not cover the value exactly once"
    return spans, None


def split_space(raw):
    """(lead, middle, trail) of a raw HTML text span; whitespace is judged after decoding, so `&nbsp;`, `&#160;` and
    literal spaces at either end stay in lead/trail exactly as spelled. An all-whitespace span is all lead."""
    units = [m.group(0) for m in TEXT_UNIT.finditer(raw)]
    space = [html.unescape(u).isspace() for u in units]
    a = next((x for x, s in enumerate(space) if not s), len(units))
    b = next((x for x in range(len(units), a, -1) if not space[x - 1]), a)
    return "".join(units[:a]), "".join(units[a:b]), "".join(units[b:])


def norm_text(text):
    return re.sub(r"\s+", " ", text).strip()


def resolve_field(value, lookup):
    """(new value, span evidence, blockers, touched item ids). Every non-whitespace text span (or JSON rich-text leaf)
    must equal one plan segment exactly: letters, digits, marks, punctuation, symbols and emoji of any script count.
    The lookup holds every plan row of the family, whatever its status; a held, gated or conflicting segment vetoes.
    touched is empty when no span of the field maps to the family (the field is not ours).

    Liquid refuses in the raw value, in every decoded JSON string and object key, in the entity-decoded HTML, in each
    translation and in the assembled result. In JSON, every leaf, structural ones included, is first checked against
    the lookup: a held, gated or conflicting segment vetoes the field before a leaf counts as structural."""
    hits = lambda text: set(i["id"] for k in lookup if k and k in text for i in lookup[k])
    if LIQUID.search(value):
        return None, [], ["Liquid in the field"], hits(value)
    spans, blockers, touched, out_parts = [], [], set(), None

    def veto(key, rows):
        if any(i["hold"] or i["gates"] for i in rows):
            blockers.append("held segment: %r" % key[:80])
            return True
        if len(set(i["value"] for i in rows)) > 1:
            blockers.append("conflicting translations for %r" % key[:80])
            return True
        return False

    def map_text(text, where):
        key = norm_text(text)
        rows = lookup.get(key, [])
        if not rows:
            parts = [k for k in lookup if key and k and ((key in k) or (k in key)) and k != key]
            if parts:
                # A fragment of an approved sentence (or a sentence inside a longer text): the field is ours, but blocked.
                touched.update(i["id"] for k in parts for i in lookup[k])
                blockers.append("split sentence: %r" % key[:80])
            else:
                blockers.append("text with no plan item: %r" % key[:80])
            return None
        touched.update(i["id"] for i in rows)
        if veto(key, rows):
            return None
        value_ = rows[0]["value"]
        if LIQUID.search(value_):
            blockers.append("the translation of %r would add Liquid" % key[:80])
            return None
        spans.append(dict(where, items=sorted(i["id"] for i in rows), en=key, value=value_,
                          statuses=sorted(set(s for i in rows for s in (i["hold"] + i["gates"]) or ["approved"]))))
        return value_

    tree = None
    if value.lstrip()[:1] == '"':
        # A valid JSON string scalar is decoded for the Liquid check (R32c C4); its value is then matched as plain text.
        try:
            scalar = json.loads(value)
        except ValueError:
            scalar = None
        if isinstance(scalar, str) and LIQUID.search(scalar):
            return None, [], ["Liquid in the field (a decoded JSON string)"], hits(scalar) | hits(value)
    if value.lstrip()[:1] in ("[", "{"):
        try:
            tree = json.loads(value)
        except ValueError:
            tree = None
        if tree is not None:
            decoded = [text for _, text, _, _ in leaves(tree)] + list(json_keys(tree))
            if any(LIQUID.search(text) for text in decoded):
                return None, [], ["Liquid in the field (a decoded JSON string)"], set().union(*(hits(t) for t in decoded))
            new = json.loads(value)
            for path, text, parent, holder in leaves(tree):
                rows = lookup.get(norm_text(text), [])
                skip = structural(parent, holder) or text.strip() in NEVER_VALUES or STRUCTURAL_VALUE.match(text) or not text.strip()
                if skip:
                    if rows:
                        # Not translated, but its rows still veto (R32-2) and their bindings elsewhere still count.
                        touched.update(i["id"] for i in rows)
                        veto(norm_text(text), rows)
                    continue
                nl = map_text(text, {"path": list(path)})
                if nl is not None:
                    lead, trail = text[:len(text) - len(text.lstrip())], text[len(text.rstrip()):]
                    new = set_path(new, path, lead + nl + trail)
            compact = ": " not in value and ", " not in value
            out_parts = json.dumps(new, ensure_ascii=False, separators=(",", ":") if compact else None)
    if tree is None and ("<" in value or ">" in value):
        if LIQUID.search(html.unescape(value)):
            return None, [], ["Liquid in the field (entity-encoded)"], hits(html.unescape(value))
        scanned, reason = scan_html(value)
        if scanned is None:
            return None, [], ["markup not mapped with certainty: " + reason], hits(value)
        out = []
        for kind, s, e in scanned:
            raw = value[s:e]
            lead, middle, trail = split_space(raw) if kind == "text" else (raw, "", "")
            if not middle:
                out.append(raw)
                continue
            nl = map_text(html.unescape(middle), {"at": [s + len(lead), e - len(trail)]})
            out.append(lead + html.escape(nl, quote=False) + trail if nl is not None else raw)
        out_parts = "".join(out)
    elif tree is None:
        nl = map_text(value, {"at": [0, len(value)]})
        if nl is not None:
            lead, trail = value[:len(value) - len(value.lstrip())], value[len(value.rstrip()):]
            out_parts = lead + nl + trail
    if not touched or (not spans and not blockers):
        return None, [], [], set()
    if not blockers and LIQUID.search(out_parts or ""):
        blockers.append("the assembled value would contain Liquid")
    if blockers:
        return None, spans, blockers, touched
    return out_parts, spans, [], touched


def evidence_hash(record):
    """The proposal hash: sha256 over the evidence. The current translation is deliberately left out, so a reviewed
    binding survives a change to it; the operation snapshot (and so the approval checksum) still binds it."""
    body = {k: v for k, v in record.items() if k not in ("current", "proposal_hash")}
    return hashlib.sha256(json.dumps(body, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()


def load_field_bindings(path, locale):
    """{resource|key: {proposal_hash, evidence}} reviewed for this locale, from bindings-fields.json."""
    if not os.path.exists(path):
        return {}
    data = json.load(open(path, encoding="utf-8"))
    out = (data.get("bindings") or {}).get(locale) if isinstance(data, dict) else None
    out = {} if out is None else out
    if not isinstance(out, dict) or not all(isinstance(b, dict) and isinstance(b.get("proposal_hash"), str) and isinstance(b.get("evidence"), dict)
                                            for b in out.values()):
        raise RunnerError("%s is not {\"bindings\": {locale: {resource|key: {proposal_hash, evidence}}}}." % path)
    for fkey, b in out.items():
        if evidence_hash(b["evidence"]) != b["proposal_hash"]:
            raise RunnerError("%s: the evidence of %s does not match its proposal hash." % (path, fkey))
    return out


def load_shop_objects(path):
    """{type: [{handle, gid, match}]} from the reviewed shop-objects.json. Only types with a known storefront selector
    are accepted, and each entry's match must be exactly that selector (SHOP_SELECTORS)."""
    if not os.path.exists(path):
        return {}
    data = json.load(open(path, encoding="utf-8"))
    out = data.get("objects") if isinstance(data, dict) else None
    if not isinstance(out, dict) or not all(isinstance(v, list) and all(isinstance(e, dict) and isinstance(e.get("handle"), str)
                                                                         and valid_gid(e.get("gid")) and isinstance(e.get("match"), dict) and e["match"]
                                                                         for e in v) for v in out.values()):
        raise RunnerError("%s is not {\"objects\": {type: [{handle, gid, match}]}}." % path)
    for type_, entries in out.items():
        if type_ not in SHOP_SELECTORS or any(e["match"] != SHOP_SELECTORS[type_] for e in entries):
            raise RunnerError("%s: %s entries must use the storefront selector %s." % (
                path, type_, json.dumps(SHOP_SELECTORS.get(type_), sort_keys=True) if type_ in SHOP_SELECTORS else "(none known for this type)"))
    return out


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


def json_keys(tree):
    """Every object key of a decoded JSON tree."""
    if isinstance(tree, dict):
        for k, v in tree.items():
            yield k
            yield from json_keys(v)
    elif isinstance(tree, list):
        for v in tree:
            yield from json_keys(v)


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


def field_records(live, plan, res, family, items, bindings, shop_objects):
    """Wave 2b evidence for every field of the metaobjects the family reaches: (reason, blocked GIDs, entries).

    items: every plan row of the family, whatever its status or legacy binding (R32-2), so held, gated, conflicting
    and bound-elsewhere segments all veto. Each entry: fkey, node, content, info, touched, blockers, and record (the
    proposal evidence; None when blocked). A field a legacy bindings.json item is bound to is left to that route.
    Only reads; the write preflight calls it again on a fresh Live (R32-5)."""
    objects, blocked, reason = reference_objects(live, res["owner"], family, shop_objects)
    if reason:
        return reason, blocked, []
    lookup = {}
    for i in items:
        lookup.setdefault(norm_text(i["en"]), []).append(i)
    entries = []
    for node in live.by_ids(sorted(objects)):
        info = objects.get(node["resourceId"])
        if info is None:
            continue
        for content in node["translatableContent"]:
            if protected(node["resourceId"], content):
                continue
            new, spans, blockers, touched = resolve_field(content["value"], lookup)
            if not touched:
                continue
            target = (node["resourceId"], content["key"])
            vetoes = [b for b in blockers if b.startswith(("held segment", "conflicting translations"))]
            if any((bindings[i].get("resource"), bindings[i].get("key")) == target for i in touched if i in bindings):
                # Left to the legacy item route, but its vetoes still count there (R32d D1).
                entries.append({"fkey": "%s|%s" % target, "node": node, "content": content, "info": info, "touched": touched,
                                "blockers": blockers, "record": None, "vetoes": vetoes, "legacy": True})
                continue
            elsewhere = sorted(i for i in touched if i in bindings)
            if elsewhere:
                blockers = blockers + ["items with a reviewed item binding elsewhere: %s" % ", ".join(elsewhere)]
            record = None
            if not blockers:
                record = {"locale": plan.get("lang"), "family": family, "product": res["owner"], "en": content["value"],
                          "paths": info["paths"], "destination": {"gid": node["resourceId"], "type": info["type"], "handle": info["handle"]},
                          "field": {"key": content["key"], "en_sha1": hashlib.sha1(content["value"].encode("utf-8")).hexdigest(),
                                    "en_digest": content["digest"]},
                          "spans": spans, "assembled": new, "scope": {"complete": False}}
            entries.append({"fkey": "%s|%s" % target, "node": node, "content": content, "info": info, "touched": touched,
                            "blockers": blockers, "record": record, "vetoes": vetoes})
    return None, blocked, entries


def family_rows(plan, owner, family):
    """Every plan row of an owner's family, across all resource groups of the plan (METAFIELD and METAOBJECT alike)
    and whatever its status: the lookup and veto set of both routes (R32d D1)."""
    return [i for res in plan["resources"] if res.get("owner") == owner for i in res["items"]
            if re.sub(r"#\d+$", "", i["field"]) == family]


def family_items(plan, index, family):
    """The resource at index and the rows field_records sees for its family (family_rows, as build() passes them)."""
    res = plan["resources"][index]
    return res, family_rows(plan, res["owner"], family)


def provenance_holds(admin, locale, plan, bindings, shop_objects, ops, field_bindings=None):
    """Fresh, uncached reads of the evidence of every op that carries a field-binding hash, and, when field_bindings
    is given, of every reviewed field binding of the locale, those already current included (R32c C5): (ok, why).
    The product's references, every object on the path, the table selection, the full list of the shop type, the
    pinned shop objects and the field itself are read again and the proposal hash rebuilt; the field's fresh EN
    digest and current translation must also still be the approved op's (R32c C1). Any difference stops the write."""
    want = [o for o in ops if o.get("evidence")]
    field_bindings = field_bindings or {}
    families = set((o["provenance"]["resource_index"], o["provenance"]["family"]) for o in want)
    for fkey, b in sorted(field_bindings.items()):
        ev = b["evidence"]
        found = [(n, ev.get("family")) for n, res in enumerate(plan["resources"]) if res.get("owner") == ev.get("product")
                 and any(re.sub(r"#\d+$", "", i["field"]) == ev.get("family") for i in res["items"])]
        if not found:
            return False, "the reviewed binding %s has no family %s in the plan" % (fkey, ev.get("family"))
        families.update(found)
    if not families:
        return True, None
    live, fresh = Live(admin, locale), {}
    for index, family in sorted(families):
        res, items = family_items(plan, index, family)
        reason, _, entries = field_records(live, plan, res, family, items, bindings, shop_objects)
        if reason:
            return False, "the provenance of %s no longer holds (%s)" % (family, reason)
        fresh.update((e["fkey"], e) for e in entries if e["record"] is not None)
    for fkey, b in sorted(field_bindings.items()):
        if fkey not in fresh or evidence_hash(fresh[fkey]["record"]) != b["proposal_hash"]:
            return False, "the provenance of the reviewed field %s changed since the dry run" % fkey
    for o in want:
        fkey = "%s|%s" % (o["resource"], o["key"])
        e = fresh.get(fkey)
        if e is None or evidence_hash(e["record"]) != o["evidence"]:
            return False, "the provenance of %s changed since the dry run" % fkey
        if e["content"]["digest"] != o["en_digest"] or current(e["node"], o["key"]) != o["current"]:
            return False, "%s changed since the dry run (seen on the provenance re-read)" % fkey
    return True, None


def build(plan, live, theme_id, remove_never, bindings=None, proposals=None, field_bindings=None, fields_out=None, shop_objects=None):
    """The approval snapshot's targets, and a row for every first-wave item.

    bindings: reviewed {item id: {resource, key, en_sha1}} for metaobject items whose field the inventory does not
    name (the legacy item route). field_bindings: reviewed {resource|key: {proposal_hash, evidence}} (wave 2b); only
    those fields are written through the field route, and fields_out collects, for review, the field proposals, the
    fields not proposed and why, the stale bindings and the shop-object candidates. proposals stays empty: the item
    route no longer proposes item bindings."""
    targets, rows, vetoed = {}, [], {}
    bindings = bindings or {}
    proposals = {} if proposals is None else proposals
    field_bindings = field_bindings or {}
    shop_objects = shop_objects or {}
    fields_out = {} if fields_out is None else fields_out
    for k in ("proposals", "exceptions", "stale", "seen", "shop_candidates"):
        fields_out.setdefault(k, {} if k in ("proposals", "shop_candidates") else [] if k != "seen" else set())

    def want(node, content, item_ids, value, how, notes=(), evidence=None, provenance=None):
        key = (node["resourceId"], content["key"])
        t = targets.setdefault(key, {"action": "register", "resource": node["resourceId"], "key": content["key"],
                                     "en": content["value"], "en_digest": content["digest"],
                                     "current": current(node, content["key"]), "values": {}, "how": how, "notes": []})
        t["values"].setdefault(value, []).extend(item_ids)
        t["notes"].extend(notes)
        if evidence:
            t["evidence"], t["provenance"] = evidence, provenance

    def row(item, res, result, why=None, node=None, content=None):
        r = {"id": item["id"], "type": res["shopify_type"], "result": result, "en": item["en"], "value": item["value"]}
        if why:
            r["why"] = why
        if node is not None:
            r["resource"], r["key"] = node["resourceId"], content["key"] if content else None
        rows.append(r)

    def field_route(res, family, items, wave, used):
        """Wave 2b: the fields of the metaobjects the product's reference-typed metafields lead to. A field is written
        only through a reviewed field binding whose evidence is unchanged; otherwise the dry run proposes it with full
        evidence for review. A changed bound field is stale: a write then aborts before any mutation. Rows are made
        only for this group's items without a legacy item binding (those have their own row); the lookup holds the
        rows of every group of the owner's family. A hold, gate or conflict found in a field vetoes its target in
        every route (vetoed)."""
        reason, blocked, entries = field_records(live, plan, res, family, family_rows(plan, res["owner"], family), bindings, shop_objects)
        if reason:
            return reason
        if blocked:
            fields_out["exceptions"].append({"family": family, "field": None, "en": None,
                                             "reasons": ["not readable, not the reviewed object, reached by too many paths or "
                                                         "selected twice: %s" % ", ".join(sorted(blocked))]})
        chain = re.sub(r"#\d+$", "", family).split("|")
        for step in chain[1:]:
            m = re.match(r"^shop\.metaobjects\.([a-z0-9_]+)$", step)
            if m and m.group(1) not in fields_out["shop_candidates"]:
                fields_out["shop_candidates"][m.group(1)] = live.metaobjects_of_type(m.group(1))
        by_id = {i["id"]: i for i in items if i["id"] not in bindings}
        index = plan["resources"].index(res)
        for e in entries:
            node, content, fkey, blockers, record = e["node"], e["content"], e["fkey"], e["blockers"], e["record"]
            if e["vetoes"]:
                vetoed.setdefault((node["resourceId"], content["key"]), "; ".join(e["vetoes"][:2]))
            if e.get("legacy"):
                continue
            fields_out["seen"].add(fkey)
            in_field = [by_id[i] for i in sorted(e["touched"]) if i in by_id]
            if blockers:
                fields_out["exceptions"].append({"family": family, "field": fkey, "en": content["value"], "reasons": blockers})
                if fkey in field_bindings:
                    fields_out["stale"].append({"field": fkey, "why": "the bound field no longer maps: " + "; ".join(blockers[:2])})
                for i in in_field:
                    if i in wave:
                        row(i, res, "not written", "field kept whole: " + "; ".join(blockers[:3]), node, content)
                used.update(i["id"] for i in in_field)
                continue
            new = record["assembled"]
            h = evidence_hash(record)
            bound = field_bindings.get(fkey)
            ids = [i["id"] for i in in_field if i in wave]
            if bound and bound["proposal_hash"] == h:
                want(node, content, ids, new, "reviewed field binding (bindings-fields.json)", evidence=h,
                     provenance={"resource_index": index, "family": family})
            elif bound:
                fields_out["stale"].append({"field": fkey, "why": "the evidence differs from the reviewed baseline"})
                for i in in_field:
                    if i in wave:
                        row(i, res, "not written", "stale field binding: a write aborts", node, content)
            else:
                fields_out["proposals"][fkey] = dict(record, proposal_hash=h, current=current(node, content["key"]))
                for i in in_field:
                    if i in wave:
                        row(i, res, "not written", "field proposed for review (fields-proposed)", node, content)
            used.update(i["id"] for i in in_field)
        return None

    for res in plan["resources"]:
        wave = [i for i in res["items"] if not i["hold"] and not i["gates"]]
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
                route_reason = field_route(res, family, items, wave, used)
                for i in wave:
                    if i["field"].startswith(family) and i["id"] not in used:
                        row(i, res, "stale", "EN found in no metafield %s of %s (whole value or JSON text) and in no field of the "
                            "metaobjects it references%s" % (family, res["owner"], " (%s)" % route_reason if route_reason else ""))
            continue
        if scope.rule == "metaobject":
            groups = {}
            for item in res["items"]:
                groups.setdefault(item["field"] if item["field"].startswith("shop.") else re.sub(r"#\d+$", "", item["field"]), []).append(item)
            for field, members in groups.items():
                items = [i for i in members if i in wave]
                if not items:
                    continue
                fixed = field.startswith("shop.") and ":" in field
                unbound = [i for i in items if not fixed and not bindings.get(i["id"])]
                for item in items:
                    if item in unbound:
                        continue
                    nodes, reason, fixed_key = metaobject_nodes(live, res["owner"], field) if fixed else (None, None, None)
                    bound = bindings.get(item["id"]) if not fixed else None
                    if fixed and reason:
                        row(item, res, "not written", "owner not proven: " + reason)
                        continue
                    if not fixed:
                        nodes, reason = reference_objects(live, res["owner"], field, shop_objects)[0], None
                        nodes = live.by_ids(sorted(nodes))
                    rid = bound["resource"] if bound else None
                    key = bound["key"] if bound else fixed_key
                    if bound and bound.get("en_sha1") != item["en_sha1"]:
                        row(item, res, "not written", "the binding in bindings.json was made for another EN")
                        continue
                    # The family veto holds here too (R32c C2): any row of the owner's family, in any resource group
                    # (R32d D1), with this EN that is held, gated or translated differently stops the item, whatever its
                    # own binding. A veto inside the target's segments removes the op later (vetoed).
                    same = [m for m in family_rows(plan, res["owner"], field) if norm_text(m["en"]) == norm_text(item["en"])]
                    if any(m["hold"] or m["gates"] for m in same) or len(set(m["value"] for m in same)) > 1:
                        row(item, res, "not written", "held, gated or conflicting rows of this family share its EN")
                        continue
                    sha = lambda c: hashlib.sha1(c["value"].encode("utf-8")).hexdigest()
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
                if fixed:
                    continue
                # Also with only legacy items left: the field route's vetoes must reach their targets (R32d D1).
                used = set()
                route_reason = field_route(res, field, members, wave, used)
                for item in unbound:
                    if item["id"] not in used:
                        row(item, res, "not written" if route_reason else "stale",
                            ("owner not proven: " + route_reason) if route_reason else "EN in no field of the proven metaobjects")
            continue
        for item in wave:
            if item["kind"] == "assemble":
                continue
            cands = []
            for node in scope.nodes:
                for content in node["translatableContent"]:
                    if scope.rule == "theme":
                        # Exact ids when the key has the documented shape (a section-level setting no longer matches
                        # the same setting of its blocks); the token rule only for keys of another shape.
                        path = theme_path(content["key"])
                        if path is not None and item.get("hint") is not None:
                            if path != item["hint"]:
                                continue
                        elif not all(h in key_tokens(content["key"]) for h in item.get("hint") or [None]):
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
            elif scope.rule == "every":
                fresh = [(n, c) for n, c in safe if hashlib.sha1(c["value"].encode("utf-8")).hexdigest() == item["en_sha1"]]
                if not fresh:
                    row(item, res, "stale", "the live EN of this key differs from the plan", safe[0][0], safe[0][1])
                for n, c in fresh:
                    want(n, c, [item["id"]], item["value"], "every selling-plan group with this EN name")
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

    for fkey in sorted(set(field_bindings) - fields_out["seen"]):
        fields_out["stale"].append({"field": fkey, "why": "the bound field was not reached in this run"})
    # R32d D1: a hold, gate or conflict the field route found in a target's segments vetoes that target in every
    # route (a legacy whole-field op included), before any op is final.
    for target, why in sorted(vetoed.items()):
        t = targets.pop(target, None)
        for iid in sorted(set(i for ids in (t or {}).get("values", {}).values() for i in ids)):
            rows.append({"id": iid, "result": "not written", "resource": target[0], "key": target[1], "value": None,
                         "why": "the field's segments carry a veto: " + why})
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
            op = {"action": "register", "resource": rid, "key": key, "en": t["en"], "en_digest": t["en_digest"],
                  "current": t["current"], "value": value, "items": sorted(ids), "how": t["how"], "notes": t["notes"]}
            if t.get("evidence"):
                op["evidence"], op["provenance"] = t["evidence"], t["provenance"]
            ops.append(op)
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


def snapshot(locale, theme_id, theme_proof_text, plan_sha, bindings_sha, remove_never, ops, field_sha=None, shop_sha=None):
    return {"store": SHOP, "api": API_VERSION, "locale": locale, "theme_id": theme_id, "theme_proof": theme_proof_text,
            "plan_sha256": plan_sha, "bindings_sha256": bindings_sha, "field_bindings_sha256": field_sha,
            "shop_objects_sha256": shop_sha, "remove_never": remove_never,
            "ops": [dict({k: o[k] for k in ("action", "resource", "key", "en_digest", "current", "value")},
                         **({"evidence": o["evidence"]} if o.get("evidence") else {})) for o in ops]}


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


def path_text(path):
    """One typed path as review text: each edge with its field, declared type and the destination's identity."""
    out = []
    for e in path:
        dest = "`%s` (%s %s)" % (e["to"], e.get("to_type") or "unreadable", e.get("to_handle") or "-")
        if e["type"] == "selection":
            sel = "; ".join("%s = `%s` in %s of %d" % (s["cell_field"], s["value"], s["table_field"], len(s["table_members"]))
                            for s in e["selector"])
            out.append("selected by the storefront (%s; pinned %s) → %s" % (sel, e["pinned"]["handle"], dest))
        else:
            src = "`%s` metafield `%s` %s" % (e["from"], e["metafield"], e["via"]) if "metafield" in e else "%s" % e["via"]
            out.append("%s [%s] → %s" % (src, e["type"], dest))
    return " → ".join(out)


def field_sections(fields):
    """The wave 2b review material: proposals grouped by family, exceptions, stale bindings, shop-object candidates."""
    lines = []
    props = (fields or {}).get("proposals") or {}
    if props:
        by_family = {}
        for fkey, p in sorted(props.items()):
            by_family.setdefault(p["family"], []).append((fkey, p))
        lines += ["## Field proposals for review, by family (%d fields)" % len(props), "",
                  "Not written. Each field below is a metaobject field the product reaches through reference-typed metafields, every text "
                  "span of which maps to one plan segment. After review, the approved entries go into "
                  "`docs/localization/registration/bindings-fields.json` with their evidence (`live/fields-proposed-<lang>.json`); only "
                  "bound fields are written, and a bound field whose evidence changes stops the whole write.", ""]
        for family, entries in sorted(by_family.items()):
            lines += ["### %s (%d)" % (family, len(entries)), ""]
            for fkey, p in entries:
                dest = p["destination"]
                lines += ["#### `%s` · %s %s · `%s`" % (dest["gid"], dest["type"], dest["handle"], p["field"]["key"]), ""]
                for n, path in enumerate(p["paths"], 1):
                    lines.append("Path %d of %d: %s" % (n, len(p["paths"]), path_text(path)))
                lines += ["", "Spans: %d. Evidence scope: %s. Proposal hash `%s`." % (
                              len(p["spans"]), "complete" if p["scope"]["complete"] else "incomplete (consumers outside this walk not proven)",
                              p["proposal_hash"][:16]), "",
                          "EN:", block(p["en"]), ""]
                lines += ["Current:", block(p["current"]["value"] if p["current"]["present"] else "(none)"), "",
                          "New:", block(p["assembled"]), ""]
    exc = (fields or {}).get("exceptions") or []
    if exc:
        lines += ["## Fields not proposed (%d)" % len(exc), "", "| Family | Field | Why |", "|---|---|---|"]
        lines += ["| %s | %s | %s |" % (cell(e["family"]), cell(e["field"] or "—"), cell("; ".join(e["reasons"]))) for e in exc]
        lines.append("")
    stale = (fields or {}).get("stale") or []
    if stale:
        lines += ["## Stale field bindings: a write aborts before any mutation (%d)" % len(stale), "",
                  "| Field | Why |", "|---|---|"] + ["| %s | %s |" % (cell(s["field"]), cell(s["why"])) for s in stale] + [""]
    cands = (fields or {}).get("shop_candidates") or {}
    if any(cands.values()):
        lines += ["## Shop-object candidates (review input for shop-objects.json, not proof)", "",
                  "| Type | Handle | GID |", "|---|---|---|"]
        lines += ["| %s | %s | %s |" % (cell(ty), cell(c.get("handle")), cell(c.get("id"))) for ty, cs in sorted(cands.items()) for c in cs]
        lines.append("")
    return lines


def report(locale, theme_id, theme_proof_text, attested, remove_never, ops, removals, rows, check, notes, proposals=None, contract_lines=(), fields=None):
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
                           ("Already equal to the plan", ("same",)), ("Skipped", ("skipped",))):
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
    lines += field_sections(fields)
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


def write(admin, live, locale, ops, journal, provenance=None):
    """Mutations per resource in chunks; stops at the first precondition failure, rejection or unknown outcome.

    provenance(ops, everything) -> (ok, why) re-reads, uncached, the provenance of the ops that carry a field-binding
    hash, with their EN digest and current translation: before the first mutation for all of them plus every
    reviewed field binding (everything=True), and for a chunk's own ops right after its content re-read, just before
    its mutation. Shopify has no transaction across references and translations, and a rebuild takes several reads,
    not one consistent snapshot: a change after the relevant read cannot be seen."""
    if provenance:
        ok, why = provenance(ops, True)
        if not ok:
            journal.log(event="stopped", reason=why)
            raise RunnerError("Stopped before any write: %s. Run the dry run again." % why)
    by_res = {}
    for o in ops:
        by_res.setdefault((o["resource"], o["action"]), []).append(o)
    accepted = 0
    for (resource, action), items in sorted(by_res.items()):
        size = REGISTER_CHUNK if action == "register" else REMOVE_CHUNK
        for start in range(0, len(items), size):
            chunk = items[start:start + size]
            ok, why = preconditions_hold(live, chunk)
            if ok and provenance and any(o.get("evidence") for o in chunk):
                ok, why = provenance(chunk, False)
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


def main(argv=None, transport=None, credentials=None, out=LIVE, plans=PLAN, bindings_path=BINDINGS,
         field_bindings_path=FIELD_BINDINGS, shop_objects_path=SHOP_OBJECTS):
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
        shop_objects = load_shop_objects(shop_objects_path)
        os.makedirs(out, exist_ok=True)
        for locale in (("nl", "fr") if args.lang == "both" else (args.lang,)):
            path = plans % locale
            plan = json.load(open(path, encoding="utf-8"))
            live = Live(admin, locale)
            proposals, fields = {}, {}
            field_bindings = load_field_bindings(field_bindings_path, locale)
            ops, removals, rows = build(plan, live, args.theme_id, args.remove_never, bindings, proposals, field_bindings, fields, shop_objects)
            snap = snapshot(locale, args.theme_id, proof, plan_hash(path), plan_hash(bindings_path), args.remove_never, ops,
                            plan_hash(field_bindings_path), plan_hash(shop_objects_path))
            check = checksum(snap)
            if not args.write:
                write_text(os.path.join(out, "dry-run-%s.md" % locale),
                           report(locale, args.theme_id, proof, args.theme_attested, args.remove_never, ops, removals, rows, check,
                                  live.notes, proposals, contract(live, admin), fields) + "\n")
                write_json(os.path.join(out, "dry-run-%s.json" % locale), {"checksum": check, "snapshot": snap, "ops": ops, "rows": rows})
                write_json(os.path.join(out, "bindings-proposed-%s.json" % locale), {"bindings": proposals})
                write_json(os.path.join(out, "fields-proposed-%s.json" % locale),
                           {"locale": locale, "proposals": fields["proposals"], "exceptions": fields["exceptions"],
                            "stale": fields["stale"], "shop_candidates": fields["shop_candidates"]})
                say("%s: %d register, %d remove in this approval; checksum %s; %d field proposals, %d stale field bindings; report %s/dry-run-%s.md" % (
                    locale, sum(o["action"] == "register" for o in ops), sum(o["action"] == "remove" for o in ops), check,
                    len(fields["proposals"]), len(fields["stale"]), out, locale))
                continue
            if fields["stale"]:
                raise RunnerError("%s: %d reviewed field binding(s) no longer match the live evidence (%s). Nothing written; review "
                                  "the fields again." % (locale, len(fields["stale"]), ", ".join(s["field"] for s in fields["stale"][:5])))
            if check != args.approve:
                raise RunnerError("%s: the live store, the plan or the options changed since the approved dry run (checksum %s, approved %s). "
                                  "Nothing written; run the dry run again." % (locale, check, args.approve))
            journal = Journal(os.path.join(out, "journal-%s.jsonl" % locale), "%s-%s" % (time.strftime("%Y%m%dT%H%M%S"), check))
            journal.log(event="start", checksum=check, ops=len(ops))
            accepted = write(admin, live, locale, ops, journal,
                             lambda sub, everything: provenance_holds(admin, locale, plan, bindings, shop_objects, sub,
                                                                      field_bindings if everything else None))
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
