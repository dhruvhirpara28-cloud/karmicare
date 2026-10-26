"""R90 targeted checks: run probe-r90.js on the theme renders at the five widths and print a table.

usage: python3 -I r90_check.py <browserPageId> <out.json>
B1: every body picture inside the page (left >= 0, right <= page width), centred at the expected
width; B2: each picture's box has its final height before the file loads (attrs set, height > 0 while
not complete); B3: one h1; plus the contents links and no sideways scroll.
"""
import json, os, subprocess, sys

page, out = sys.argv[1], sys.argv[2]
HERE = os.path.dirname(os.path.abspath(__file__))
BASE = "http://127.0.0.1:9390/docs/blog/fixture/site/"
results = []


def orca(*args):
    return subprocess.run(["orca", *args, "--page", page, "--json"], capture_output=True, text=True, timeout=180)


for name in ("theme-article-nano", "theme-article-short", "theme-article-noimage", "theme-article-nano-nl", "theme-article-nano-fr"):
    for w in (360, 390, 750, 990, 1440):
        orca("goto", "--url", f"{BASE}{name}.html?tokens=next")
        orca("exec", "--command", f"set viewport {w} 900")
        orca("screenshot")
        tmp = os.path.join(HERE, "..", "data", "r90-tmp.json")
        subprocess.run(["python3", "-I", os.path.join(HERE, "oeval.py"), page, os.path.join(HERE, "probe-r90.js"), tmp], capture_output=True)
        if not os.path.exists(tmp):
            print(name, w, "no result")
            continue
        d = json.load(open(tmp))
        os.remove(tmp)
        d.update(name=name, target=w)
        results.append(d)
        imgs = d["imgs"]
        edges = " ".join(f"{i['left']}→{i['right']}" for i in imgs)
        bad = [i for i in imgs if i["clipped"] or i["h"] < 50]
        unloaded = sum(1 for i in imgs if not i["complete"])
        print(f"{name:24} {w:5} vw={d['clientWidth']:5} scroll={d['scrollWidth']:5} h1={d['h1']} toc={len(d['toc'])} "
              f"imgs={len(imgs)} unloaded={unloaded} problems={len(bad)} | {edges}")
json.dump(results, open(out, "w"), indent=1)
