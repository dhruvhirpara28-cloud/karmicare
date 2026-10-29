"""Run probe-type.js on a set of pages at 390 and 1440 and print one table per page and width.

usage: python3 -I type_audit.py <browserPageId> <out.json>
"""
import json, os, subprocess, sys

page, out = sys.argv[1], sys.argv[2]
HERE = os.path.dirname(os.path.abspath(__file__))
PAGES = [
    ("blog D", "http://127.0.0.1:9390/docs/blog/fixture/site/d-article.html"),
    ("live article", "https://www.karmicare.com/blogs/news/nano-hydroxyapatite"),
    ("homepage", "https://www.karmicare.com/"),
    ("legal page", "https://www.karmicare.com/pages/terms-and-conditions-1"),
]
results = []


def orca(*args):
    return subprocess.run(["orca", *args, "--page", page, "--json"], capture_output=True, text=True, timeout=180)


for name, url in PAGES:
    for w, h in ((390, 844), (1440, 900)):
        orca("goto", "--url", url)
        orca("exec", "--command", f"set viewport {w} {h}")
        orca("screenshot")
        tmp = os.path.join(HERE, "..", "data", "type-tmp.json")
        r = subprocess.run(["python3", "-I", os.path.join(HERE, "oeval.py"), page, os.path.join(HERE, "probe-type.js"), tmp], capture_output=True, text=True)
        if not os.path.exists(tmp):
            print(name, w, "failed", r.stdout, r.stderr)
            continue
        d = json.load(open(tmp))
        os.remove(tmp)
        d["name"] = name
        results.append(d)
        print(f"\n== {name} @ {d['w']} ({d['page']})")
        for role, fs, ftok, lh, ltok, ff, fw in d["rows"]:
            print(f"  {role:22} {fs:5.1f}px  {ftok:38} lh {str(lh):6} {ltok:34} {ff} {fw}")
json.dump(results, open(out, "w"), indent=1)
