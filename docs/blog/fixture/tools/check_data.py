"""Print a summary of docs/blog/fixture/data/live.json. usage: python3 -I check_data.py <live.json>"""
import json, sys

d = json.load(open(sys.argv[1]))
print("fetched", d["fetched"], "| shells", {k: len(v) for k, v in d["shell"].items()})
print("index", len(d["index"]))
for i in d["index"]:
    a = d["articles"].get(i["handle"], {})
    img = a.get("image") or {}
    print(f'  {i["handle"][:50]:50} {a.get("published_at")} img {img.get("width")}x{img.get("height")} body {len(a.get("content", ""))} | {i["excerpt"][:60]}')
p = d["product"]
print("product", p and (p["title"], p["featured_image"], len(p["images"])))
