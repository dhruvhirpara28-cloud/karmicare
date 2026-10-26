"""Take a set of fixture screenshots into docs/blog/shots/.

usage: python3 -I shots.py <browserPageId> <set> [filter]

Sets:
  review   a quick look per direction (390 and 1440, Day)
  matrix   article and index tops at 390, 750, 1100, 1440 in Day and Night, plus the article's parts
           (body, sources, CTA, related) at 390 and 1440 in Day and Night
filter: only shots whose file name contains it.
Names: <direction>-<page>-<part>-<width>-<mode>.png
"""
import os, subprocess, sys
from urllib.parse import quote

page, which = sys.argv[1], sys.argv[2]
flt = sys.argv[3] if len(sys.argv) > 3 else ""
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
OUT = os.path.join(ROOT, "docs", "blog", "shots")
BASE = "http://127.0.0.1:9390/docs/blog/fixture/site/"
HEIGHT = {390: 844, 750: 900, 1100: 900, 1440: 900}  # taller than Orca's pane (~940) tiles the frame

PARTS = {
    "body": ".kc-blog__body blockquote",
    "image": ".kc-blog__body img",
    "sources": ".kc-blog-sources",
    "cta": ".kc-blog-cta__heading, .featured-product, [id*=featured_product]",
    "related": ".kc-blog__section-heading",
}


def plan():
    shots = []
    if which == "review":
        for d in "abc":
            for w in (390, 1440):
                shots.append((f"{d}-article-top-{w}-day", f"{d}-article.html", w, ""))
                shots.append((f"{d}-blog-top-{w}-day", f"{d}-blog.html", w, ""))
                for part, sel in PARTS.items():
                    shots.append((f"{d}-article-{part}-{w}-day", f"{d}-article.html", w, "at=" + sel))
    elif which == "matrix":
        for d in "dabc":
            for mode in ("day", "night"):
                for w in (390, 750, 1100, 1440):
                    shots.append((f"{d}-article-top-{w}-{mode}", f"{d}-article.html", w, f"mode={mode}"))
                    shots.append((f"{d}-blog-top-{w}-{mode}", f"{d}-blog.html", w, f"mode={mode}"))
                for w in (390, 1440):
                    for part, sel in PARTS.items():
                        shots.append((f"{d}-article-{part}-{w}-{mode}", f"{d}-article.html", w, f"mode={mode}&at={sel}"))
    return [s for s in shots if flt in s[0]]


for name, path, w, q in plan():
    url = BASE + path + ("?" + q if q else "")
    if "at=" in q or "y=" in q:
        # scrolled views go through frame.html: Orca paints a scrolled page only inside an iframe
        url = "http://127.0.0.1:9390/docs/blog/fixture/frame.html?src=" + quote(url, safe="")
    out = os.path.join(OUT, name + ".png")
    r = subprocess.run(["python3", "-I", os.path.join(HERE, "shoot.py"), page, out, url, str(w), str(HEIGHT[w]), "--settle", "2"],
                       capture_output=True, text=True)
    print(name, (r.stdout or r.stderr).strip().split("\n")[-1][-60:])
