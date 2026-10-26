"""Print part of one article body from live.json. usage: python3 -I show_html.py <live.json> <handle> <pattern> [chars]"""
import json, re, sys

d = json.load(open(sys.argv[1]))
body = d["articles"][sys.argv[2]]["content"]
n = int(sys.argv[4]) if len(sys.argv) > 4 else 1500
for m in list(re.finditer(sys.argv[3], body))[:3]:
    print("-----", m.start())
    print(body[max(0, m.start() - 200): m.start() + n])
