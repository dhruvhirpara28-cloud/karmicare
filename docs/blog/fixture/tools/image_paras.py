"""List the body paragraphs that hold an image, and whether they also hold text.

usage: python3 -I image_paras.py <live.json>
"""
import html, json, re, sys

d = json.load(open(sys.argv[1]))
for handle, a in d["articles"].items():
    for m in re.finditer(r"<(p|div)\b[^>]*>(?:(?!</\1>).)*?<img\b(?:(?!</\1>).)*?</\1>", a["content"], re.S):
        block = m.group(0)
        text = html.unescape(re.sub(r"<[^>]+>", "", block)).strip()
        src = re.search(r'src="([^"]+)"', block).group(1).split("/files/")[-1]
        print(f"{handle[:40]:40} <{m.group(1)}> text={len(text):3} {src}")
