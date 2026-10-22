#!/usr/bin/env python3
"""Register the NL/FR plans in Shopify through the Admin GraphQL API (B4 access path A).

Reads docs/localization/registration/plan-<lang>.json and the live store, and writes per language:

  docs/localization/registration/live/dry-run-<lang>.md    what a write would do, for Victor
  docs/localization/registration/live/dry-run-<lang>.json  the same operations, machine-readable
  docs/localization/registration/live/written-<lang>.json  after a write: what Shopify accepted

Run from the repo root:

  python3 docs/localization/registration/register.py [--lang nl|fr|both]            dry run (read only)
  python3 docs/localization/registration/register.py --lang nl --write --approve <checksum>

Dry run (the default) sends only queries. For every first-wave item it fetches the live translatable
content (key, value, digest) and the current translation, matches the item on its EN sha1 (or, for a
split body, on each block's EN inside the live value), and classifies it: new, overwrite (the current
NL/FR is shown), same, stale (the live EN differs: skipped), ambiguous or missing. Selling plans and
selling-plan groups are skipped: Loop owns their translations. Translations that exist on
never-translate keys (handle_item, selling_plan_id, the Subscription Name values) are listed for
removal. The report ends with a checksum over every operation.

Write needs --approve with that checksum. The runner rebuilds the operations from the live store and
writes only if the checksum is the same, so it writes exactly what Victor approved; if anything
changed it stops. Removals run only with --remove-never as well. NL and FR are published: a
registered translation is live at once.

Credentials (APP-SETUP.md): the client ID and secret come from the macOS Keychain item
"karmicare-translations", read inside this process; the 24 h token from client_credentials lives in
memory only. Nothing prints or stores the secret or the token.
"""
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request

SHOP = "karmicares.myshopify.com"
API_VERSION = "2026-10"
KEYCHAIN_SERVICE = "karmicare-translations"
PLAN = "docs/localization/registration/plan-%s.json"
LIVE = "docs/localization/registration/live"
LOOP_TYPES = ("SELLING_PLAN", "SELLING_PLAN_GROUP")
SEGMENT_TYPES = ("METAFIELD", "METAOBJECT")
NEVER_KEYS = ("handle_item", "selling_plan_id")
NEVER_VALUES = ("60-Day Supply", "Year Supply")
HANDLE_TYPES = ("PRODUCT", "PAGE", "ARTICLE", "BLOG", "COLLECTION")
LIST_TYPES = ("ONLINE_STORE_THEME_JSON_TEMPLATE", "ONLINE_STORE_THEME_SECTION_GROUP", "METAOBJECT", "LINK",
              "SHOP", "SHOP_POLICY")
REGISTER_CHUNK = 50

CONTENT = "resourceId translatableContent { key value digest locale type } translations(locale: $locale) { key value outdated }"
Q_LIST = """query($type: TranslatableResourceType!, $after: String, $locale: String!) {
  translatableResources(first: 100, after: $after, resourceType: $type) {
    nodes { %s } pageInfo { hasNextPage endCursor } } }""" % CONTENT
Q_IDS = """query($ids: [ID!]!, $after: String, $locale: String!) {
  translatableResourcesByIds(first: 100, after: $after, resourceIds: $ids) {
    nodes { %s } pageInfo { hasNextPage endCursor } } }""" % CONTENT
Q_METAFIELDS = """query($id: ID!, $after: String) {
  product(id: $id) { metafields(first: 250, after: $after) { nodes { id namespace key } pageInfo { hasNextPage endCursor } } } }"""
M_REGISTER = """mutation($id: ID!, $translations: [TranslationInput!]!) {
  translationsRegister(resourceId: $id, translations: $translations) {
    translations { key locale value } userErrors { field message code } } }"""
M_REMOVE = """mutation($id: ID!, $keys: [String!]!, $locales: [String!]!) {
  translationsRemove(resourceId: $id, translationKeys: $keys, locales: $locales) {
    translations { key locale } userErrors { field message code } } }"""


def sha1(text):
    return hashlib.sha1(text.encode("utf-8")).hexdigest()


class Secret:
    """Holds a credential without ever showing it in a repr, a traceback or a log line."""

    def __init__(self, value):
        self._value = value

    def reveal(self):
        return self._value

    def __repr__(self):
        return "Secret(***)"

    __str__ = __repr__


def keychain_credentials(run=subprocess.run):
    """Client ID (the item's account, not secret) and client secret, from the Keychain item."""
    attrs = run(["security", "find-generic-password", "-s", KEYCHAIN_SERVICE], capture_output=True, text=True)
    if attrs.returncode != 0:
        sys.exit("No Keychain item '%s'. Follow docs/localization/registration/APP-SETUP.md step 4." % KEYCHAIN_SERVICE)
    m = re.search(r'"acct"<blob>="([^"]+)"', attrs.stdout)
    if not m:
        sys.exit("The Keychain item '%s' has no account (client ID)." % KEYCHAIN_SERVICE)
    secret = run(["security", "find-generic-password", "-s", KEYCHAIN_SERVICE, "-w"], capture_output=True, text=True)
    if secret.returncode != 0 or not secret.stdout.strip():
        sys.exit("macOS did not release the secret of '%s' (denied, or empty)." % KEYCHAIN_SERVICE)
    return m.group(1), Secret(secret.stdout.strip())


class HttpTransport:
    """POSTs to the store over HTTPS. Error messages carry the status and Shopify's message only."""

    def post(self, path, body, headers):
        req = urllib.request.Request("https://%s%s" % (SHOP, path), data=json.dumps(body).encode("utf-8"),
                                     headers=dict(headers, **{"Content-Type": "application/json"}), method="POST")
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                return resp.status, json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as err:
            try:
                return err.code, json.loads(err.read().decode("utf-8"))
            except ValueError:
                return err.code, {"errors": "HTTP %d" % err.code}


class Admin:
    def __init__(self, transport, client_id, secret):
        self.transport = transport
        status, data = transport.post("/admin/oauth/access_token", {
            "client_id": client_id, "client_secret": secret.reveal(), "grant_type": "client_credentials"}, {})
        if status != 200 or "access_token" not in data:
            sys.exit("Token request refused (HTTP %d). Check that the app is installed on %s." % (status, SHOP))
        self._token = Secret(data["access_token"])
        self.scopes = set((data.get("scope") or "").split(","))

    def __repr__(self):
        return "Admin(%s)" % SHOP

    def graphql(self, query, variables):
        for attempt in range(5):
            status, data = self.transport.post("/admin/api/%s/graphql.json" % API_VERSION,
                                               {"query": query, "variables": variables},
                                               {"X-Shopify-Access-Token": self._token.reveal()})
            errors = data.get("errors")
            if status == 429 or (errors and "THROTTLED" in json.dumps(errors)):
                time.sleep(2 + 2 * attempt)
                continue
            if status != 200 or errors:
                text = json.dumps(errors or data)[:500]
                hint = " (add the scope read_metaobjects, APP-SETUP.md step 2)" if "metaobject" in text.lower() else ""
                sys.exit("Admin API error, HTTP %d: %s%s" % (status, text, hint))
            throttle = (data.get("extensions") or {}).get("cost", {}).get("throttleStatus") or {}
            if throttle.get("currentlyAvailable", 1000) < 200:
                time.sleep((200 - throttle["currentlyAvailable"]) / max(throttle.get("restoreRate", 50), 1))
            return data["data"]
        sys.exit("Admin API kept throttling; try again in a minute.")

    def pages(self, query, variables, field):
        after = None
        while True:
            data = self.graphql(query, dict(variables, after=after))
            for part in field.split("."):
                data = data[part]
            for node in data["nodes"]:
                yield node
            if not data["pageInfo"]["hasNextPage"]:
                return
            after = data["pageInfo"]["endCursor"]


class Live:
    """Translatable resources fetched once per type or id, with the locale's current translations."""

    def __init__(self, admin, locale):
        self.admin, self.locale = admin, locale
        self.by_type, self.by_id, self.metafields = {}, {}, {}

    def of_type(self, rtype):
        if rtype not in self.by_type:
            self.by_type[rtype] = list(self.admin.pages(Q_LIST, {"type": rtype, "locale": self.locale}, "translatableResources"))
            for node in self.by_type[rtype]:
                self.by_id[node["resourceId"]] = node
        return self.by_type[rtype]

    def by_ids(self, ids):
        missing = [i for i in ids if i not in self.by_id]
        for start in range(0, len(missing), 100):
            for node in self.admin.pages(Q_IDS, {"ids": missing[start:start + 100], "locale": self.locale}, "translatableResourcesByIds"):
                self.by_id[node["resourceId"]] = node
        return [self.by_id[i] for i in ids if i in self.by_id]

    def by_handle(self, rtype, handle):
        handle = handle.split("/")[-1]
        for node in self.of_type(rtype):
            if any(c["key"] == "handle" and c["value"] == handle for c in node["translatableContent"]):
                return node
        return None

    def product_metafields(self, handle):
        if handle not in self.metafields:
            product = self.by_handle("PRODUCT", handle)
            ids = [] if not product else [m["id"] for m in self.admin.pages(Q_METAFIELDS, {"id": product["resourceId"]}, "product.metafields")]
            self.metafields[handle] = self.by_ids(ids)
        return self.metafields[handle]


def resources_for(live, res):
    """The live resources an item of this plan resource can live in."""
    rtype, owner = res["shopify_type"], res["owner"]
    if owner.startswith("gid://"):
        return live.by_ids([owner])
    if rtype == "METAFIELD":
        return live.product_metafields(owner)
    if rtype in HANDLE_TYPES:
        node = live.by_handle(rtype, owner)
        return [node] if node else []
    return live.of_type(rtype)


def owner_hint(res):
    """For theme content: the template or group name that its resourceId is expected to contain."""
    if res["shopify_type"].startswith("ONLINE_STORE_THEME"):
        return os.path.basename(res["owner"])[: -len(".json")] if res["owner"].endswith(".json") else res["owner"]
    return None


def narrow(cands, item, res):
    hint = owner_hint(res)
    if hint and len(cands) > 1:
        cands = [c for c in cands if hint in c[0]["resourceId"]] or cands
    if item.get("key") and len(cands) > 1:
        cands = [c for c in cands if c[1]["key"] == item["key"]] or cands
    for part in item.get("hint") or []:
        if len(cands) > 1:
            cands = [c for c in cands if part in c[1]["key"]] or cands
    return cands


def escaped(text):
    return json.dumps(text, ensure_ascii=False)[1:-1]


def is_json(content):
    return (content.get("type") or "").upper() == "JSON" or content["value"][:1] in "[{"


def assemble(value, blocks, as_json):
    """Replace each block's EN by its translation inside the live value, in order; None if one is missing."""
    out, pos = value, 0
    for item in blocks:
        en, tr = (escaped(item["en"]), escaped(item["value"])) if as_json else (item["en"], item["value"])
        at = out.find(en, pos)
        if at < 0:
            return None
        out = out[:at] + tr + out[at + len(en):]
        pos = at + len(tr)
    return out


def quoted(text):
    return json.dumps(text, ensure_ascii=False)


def replace_strings(value, items):
    """Replace JSON string values that equal an item's EN exactly (a quoted string, never part of one)."""
    out = value
    for item in sorted(items, key=lambda i: -len(i["en"])):
        out = out.replace(quoted(item["en"]), quoted(item["value"]))
    return out


def existing(node, key):
    for t in node.get("translations") or []:
        if t["key"] == key:
            return t
    return None


def classify(node, content, value):
    cur = existing(node, content["key"])
    if cur is None:
        return "new", None
    if cur["value"] == value and not cur.get("outdated"):
        return "same", cur["value"]
    return "overwrite", cur["value"]


def build(plan, live):
    """Every operation a write would send, and a report row for every first-wave item."""
    ops, rows, claimed = [], [], set()
    for res in plan["resources"]:
        if res["shopify_type"] in LOOP_TYPES:
            for item in res["items"]:
                rows.append({"id": item["id"], "type": res["shopify_type"], "result": "skipped", "why": "Loop owns selling-plan translations"})
            continue
        wave = [i for i in res["items"] if not i["hold"] and not i["gates"]]
        if not wave:
            continue
        nodes = resources_for(live, res)
        if not nodes:
            for item in wave:
                rows.append({"id": item["id"], "type": res["shopify_type"], "result": "missing", "why": "no live resource for %s" % res["owner"]})
            continue
        groups, segments = {}, []
        for item in wave:
            if item["kind"] == "assemble":
                groups.setdefault(item["field"].split("#")[0], []).append(item)
                continue
            cands = [(n, c) for n in nodes for c in n["translatableContent"]
                     if sha1(c["value"]) == item["en_sha1"] and (n["resourceId"], c["key"]) not in claimed]
            cands = narrow(cands, item, res)
            if not cands:
                if res["shopify_type"] in SEGMENT_TYPES:
                    segments.append(item)
                else:
                    rows.append({"id": item["id"], "type": res["shopify_type"], "result": "stale",
                                 "why": "no live value with this EN sha1", "en": item["en"]})
                continue
            for node, content in cands:
                claimed.add((node["resourceId"], content["key"]))
                result, before = classify(node, content, item["value"])
                rows.append({"id": item["id"], "type": res["shopify_type"], "resource": node["resourceId"], "key": content["key"],
                             "result": result if len(cands) == 1 else result + " (one of %d matches)" % len(cands),
                             "en": item["en"], "before": before, "after": item["value"]})
                if result != "same":
                    ops.append({"op": "register", "resource": node["resourceId"], "key": content["key"],
                                "digest": content["digest"], "value": item["value"]})
        found = {}
        for item in segments:
            for node in nodes:
                for content in node["translatableContent"]:
                    if (node["resourceId"], content["key"]) not in claimed and is_json(content) and quoted(item["en"]) in content["value"]:
                        found.setdefault((node["resourceId"], content["key"]), (node, content, []))[2].append(item)
        hit = {i["id"] for _, _, items in found.values() for i in items}
        for node, content, items in found.values():
            claimed.add((node["resourceId"], content["key"]))
            new = replace_strings(content["value"], items)
            result, before = classify(node, content, new)
            for item in items:
                rows.append({"id": item["id"], "type": res["shopify_type"], "resource": node["resourceId"], "key": content["key"],
                             "result": result + " (segment of a JSON value, %d segments)" % len(items), "en": item["en"], "after": item["value"]})
            rows[-1]["before"] = before
            if result != "same":
                ops.append({"op": "register", "resource": node["resourceId"], "key": content["key"],
                            "digest": content["digest"], "value": new})
        for item in segments:
            if item["id"] not in hit:
                rows.append({"id": item["id"], "type": res["shopify_type"], "result": "stale",
                             "why": "EN found neither as a whole value nor as a JSON string", "en": item["en"]})
        for field, blocks in groups.items():
            done = False
            for node in nodes:
                for content in node["translatableContent"]:
                    if (node["resourceId"], content["key"]) in claimed:
                        continue
                    new = assemble(content["value"], blocks, is_json(content))
                    if new is None or new == content["value"]:
                        continue
                    claimed.add((node["resourceId"], content["key"]))
                    result, before = classify(node, content, new)
                    for item in blocks:
                        rows.append({"id": item["id"], "type": res["shopify_type"], "resource": node["resourceId"], "key": content["key"],
                                     "result": result + " (assembled, %d blocks)" % len(blocks), "en": item["en"], "after": item["value"]})
                    rows[-1]["before"] = before
                    if result != "same":
                        ops.append({"op": "register", "resource": node["resourceId"], "key": content["key"],
                                    "digest": content["digest"], "value": new})
                    done = True
                    break
                if done:
                    break
            if not done:
                for item in blocks:
                    rows.append({"id": item["id"], "type": res["shopify_type"], "result": "stale",
                                 "why": "the live EN no longer matches (sha1 or block text)", "en": item["en"]})
    for rtype in ("METAOBJECT", "ONLINE_STORE_THEME_JSON_TEMPLATE"):
        for node in live.of_type(rtype):
            for content in node["translatableContent"]:
                never = content["key"].split(".")[-1].split(":")[0] in NEVER_KEYS or content["value"] in NEVER_VALUES
                cur = existing(node, content["key"]) if never else None
                if cur:
                    rows.append({"id": node["resourceId"] + " " + content["key"], "type": rtype, "resource": node["resourceId"],
                                 "key": content["key"], "result": "remove (never translate)", "en": content["value"], "before": cur["value"]})
                    ops.append({"op": "remove", "resource": node["resourceId"], "key": content["key"]})
    return ops, rows


def checksum(ops, locale):
    canon = json.dumps({"locale": locale, "ops": sorted(ops, key=lambda o: (o["op"], o["resource"], o["key"]))},
                       ensure_ascii=False, sort_keys=True)
    return hashlib.sha256(canon.encode("utf-8")).hexdigest()[:16]


def report(locale, ops, rows, check):
    counts = {}
    for r in rows:
        base = r["result"].split(" (")[0]
        counts[base] = counts.get(base, 0) + 1
    lines = ["# Live dry run · %s" % locale.upper(), "",
             "Read only: nothing was written. Store %s, API %s, %s." % (SHOP, API_VERSION, time.strftime("%Y-%m-%d %H:%M %Z")),
             "NL and FR are published: an approved write is live at once.", "",
             "| Result | Items |", "|---|---:|"]
    lines += ["| %s | %d |" % (k, v) for k, v in sorted(counts.items())]
    lines += ["", "Operations: %d register, %d remove. **Checksum `%s`**: to write exactly this, run" % (
        sum(o["op"] == "register" for o in ops), sum(o["op"] == "remove" for o in ops), check), "",
        "```sh", "python3 docs/localization/registration/register.py --lang %s --write --approve %s%s" % (
            locale, check, " --remove-never" if any(o["op"] == "remove" for o in ops) else ""), "```", ""]
    for title, keep in (("Overwritten (current %s → new)" % locale.upper(), "overwrite"), ("Removed: never-translate keys", "remove"),
                        ("New", "new"), ("Stale, missing or ambiguous: not written", None)):
        sel = [r for r in rows if (r["result"].startswith(keep) if keep else
                                   r["result"].split(" (")[0] in ("stale", "missing") or "matches" in r["result"])]
        if not sel:
            continue
        lines += ["## %s (%d)" % (title, len(sel)), "", "| Item | EN | Current | New | Note |", "|---|---|---|---|---|"]
        for r in sel:
            cell = lambda s: (s or "").replace("|", "\\|").replace("\n", " ")[:160]
            lines.append("| `%s` | %s | %s | %s | %s |" % (r["id"], cell(r.get("en")), cell(r.get("before")), cell(r.get("after")),
                                                          cell(r.get("why") or r["result"])))
        lines.append("")
    skipped = [r for r in rows if r["result"] == "skipped"]
    if skipped:
        lines += ["## Skipped (%d)" % len(skipped), "", "Selling plans and groups: Loop owns their translations.", ""]
    return "\n".join(lines)


def write(admin, locale, ops, remove):
    done = []
    by_res = {}
    for o in ops:
        by_res.setdefault((o["resource"], o["op"]), []).append(o)
    for (resource, op), items in sorted(by_res.items()):
        if op == "remove":
            if not remove:
                continue
            data = admin.graphql(M_REMOVE, {"id": resource, "keys": [o["key"] for o in items], "locales": [locale]})["translationsRemove"]
            done.append({"resource": resource, "op": "remove", "keys": [o["key"] for o in items], "errors": data["userErrors"]})
            continue
        for start in range(0, len(items), REGISTER_CHUNK):
            chunk = items[start:start + REGISTER_CHUNK]
            data = admin.graphql(M_REGISTER, {"id": resource, "translations": [
                {"key": o["key"], "locale": locale, "value": o["value"], "translatableContentDigest": o["digest"]} for o in chunk]})["translationsRegister"]
            done.append({"resource": resource, "op": "register", "keys": [t["key"] for t in data["translations"] or []],
                         "errors": data["userErrors"]})
    return done


def main(argv=None, transport=None, credentials=None, out=LIVE, plans=PLAN):
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--lang", choices=("nl", "fr", "both"), default="both")
    parser.add_argument("--write", action="store_true", help="write; needs --approve")
    parser.add_argument("--approve", help="the checksum of the dry run Victor approved")
    parser.add_argument("--remove-never", action="store_true", help="also remove translations of never-translate keys")
    args = parser.parse_args(argv)
    if args.write and (args.lang == "both" or not args.approve):
        sys.exit("--write needs one --lang and --approve <checksum> from that language's dry run.")
    client_id, secret = credentials() if credentials else keychain_credentials()
    admin = Admin(transport or HttpTransport(), client_id, secret)
    if args.write and admin.scopes != {""} and "write_translations" not in admin.scopes:
        sys.exit("The app's token has no write_translations scope (APP-SETUP.md step 2).")
    os.makedirs(out, exist_ok=True)
    for locale in (("nl", "fr") if args.lang == "both" else (args.lang,)):
        plan = json.load(open(plans % locale, encoding="utf-8"))
        ops, rows = build(plan, Live(admin, locale))
        check = checksum(ops, locale)
        if not args.write:
            with open(os.path.join(out, "dry-run-%s.md" % locale), "w", encoding="utf-8") as f:
                f.write(report(locale, ops, rows, check) + "\n")
            with open(os.path.join(out, "dry-run-%s.json" % locale), "w", encoding="utf-8") as f:
                f.write(json.dumps({"locale": locale, "checksum": check, "ops": ops, "rows": rows}, ensure_ascii=False, indent=1) + "\n")
            print("%s: %d register, %d remove; checksum %s; report %s/dry-run-%s.md" % (
                locale, sum(o["op"] == "register" for o in ops), sum(o["op"] == "remove" for o in ops), check, out, locale))
            continue
        if check != args.approve:
            sys.exit("%s: the live store changed since the approved dry run (checksum %s, approved %s). Nothing written; run the dry run again."
                     % (locale, check, args.approve))
        done = write(admin, locale, ops, args.remove_never)
        with open(os.path.join(out, "written-%s.json" % locale), "w", encoding="utf-8") as f:
            f.write(json.dumps({"locale": locale, "checksum": check, "results": done}, ensure_ascii=False, indent=1) + "\n")
        errors = [e for d in done for e in d["errors"]]
        print("%s: %d calls, %d keys accepted, %d user errors; %s/written-%s.json" % (
            locale, len(done), sum(len(d["keys"]) for d in done), len(errors), out, locale))
        if errors:
            sys.exit(1)


if __name__ == "__main__":
    main()
