#!/usr/bin/env python3
"""Fixture for the footer legal labels (guarantee, withdrawal) without a Liquid engine.

Resolves each label the way sections/footer.liquid does:
  label = section setting (sections/footer-group.json) | default: t('kc.footer.<key>') per locale
and checks the schema (blank defaults, info naming the key, visibility checkboxes default true),
the saved settings (no EN label stored) and the three storefront locales. Exit 1 on any failure.
Run from the repo root: python3 -I docs/global-footer/legal-labels-fixture.py
Written for the landing desk brief of 25 Oct (Victor, "ja codefix voor labels").
"""
import json
import re
import sys

ROOT = "."
EXPECT = {
    "legal_guarantee": {
        "en.default": "Your legal guarantee rights",
        "nl": "Je wettelijke garantierechten",
        "fr": "Vos droits à la garantie légale",
    },
    "legal_withdrawal": {
        "en.default": "Withdraw from contract here",
        "nl": "Hier de overeenkomst herroepen",
        "fr": "Renoncer au contrat ici",
    },
}
problems = []

liquid = open(ROOT + "/sections/footer.liquid", encoding="utf-8").read()
schema = json.loads(re.search(r"{% schema %}(.*){% endschema %}", liquid, re.S).group(1))
settings = {s.get("id"): s for s in schema["settings"] if "id" in s}

for key in ("legal_guarantee", "legal_withdrawal"):
    label = settings.get(key + "_label")
    show = settings.get("show_" + key)
    if label is None or "default" in label:
        problems.append("%s_label: missing or still has a schema default" % key)
    elif "kc.footer.%s" % key not in label.get("info", ""):
        problems.append("%s_label: info does not name the locale key" % key)
    if show is None or show.get("type") != "checkbox" or show.get("default") is not True:
        problems.append("show_%s: missing, not a checkbox or not default true" % key)
    if "'kc.footer.%s' | t" % key not in liquid:
        problems.append("footer.liquid does not read 'kc.footer.%s' | t" % key)
    if "section.settings.%s_label | default: %s_default" % (key, key) not in liquid:
        problems.append("footer.liquid does not fall back from %s_label to the locale default" % key)
    if "section.settings.show_%s and" % key not in liquid:
        problems.append("footer.liquid does not gate the %s link on its checkbox" % key)

group = json.loads(re.sub(r"^/\*.*?\*/", "", open(ROOT + "/sections/footer-group.json", encoding="utf-8").read(), flags=re.S))
saved = group["sections"]["footer"]["settings"]
for key in ("legal_guarantee_label", "legal_withdrawal_label"):
    if key in saved:
        problems.append("footer-group.json still saves %s = %r (would override the locale default)" % (key, saved[key]))

for lang in ("en.default", "nl", "fr"):
    text = open(ROOT + "/locales/%s.json" % lang, encoding="utf-8").read()
    text = re.sub(r"^/\*.*?\*/", "", text, flags=re.S)
    kc = json.loads(text).get("kc", {}).get("footer", {})
    for key in ("legal_guarantee", "legal_withdrawal"):
        # Liquid: setting | default: t(key). The setting is not saved, so the locale value is the label.
        resolved = saved.get(key + "_label") or kc.get(key)
        want = EXPECT[key][lang]
        status = "ok" if resolved == want else "MISMATCH"
        if resolved != want:
            problems.append("%s: %s resolves to %r, expected %r" % (lang, key, resolved, want))
        print("%-10s %-17s %-40r %s" % (lang, key, resolved, status))

if problems:
    print("\n".join(problems))
    sys.exit(1)
print("fixture ok: both labels resolve per locale, schema and saved settings as required")
