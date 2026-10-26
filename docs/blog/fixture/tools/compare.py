"""Write docs/blog/fixture/site/compare.html: the screenshots in docs/blog/shots side by side.

usage: python3 -I compare.py
Open http://127.0.0.1:9390/docs/blog/fixture/site/compare.html (fixture server running).
"""
import html, os

HERE = os.path.dirname(os.path.abspath(__file__))
SHOTS = os.path.abspath(os.path.join(HERE, "..", "..", "shots"))
OUT = os.path.abspath(os.path.join(HERE, "..", "site", "compare.html"))
names = {"d": "D · Editorial (reference)", "a": "A · Quiet column", "b": "B · Editorial with a reading rail", "c": "C · Research notebook"}
rows = [
    ("Article · top", "article-top"),
    ("Article · body and quote", "article-body"),
    ("Article · body image", "article-image"),
    ("Article · sources", "article-sources"),
    ("Article · CTA", "article-cta"),
    ("Article · related", "article-related"),
    ("Index · top", "blog-top"),
]
files = set(os.listdir(SHOTS))

out = ["""<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Blog directions · compare</title>
<style>
:root{--bg:#fffbf6;--ink:#191f38;--muted:rgba(25,31,56,.68);--rule:rgba(25,31,56,.12)}
body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 "proxima-nova",system-ui,sans-serif}
header{position:sticky;top:0;z-index:2;display:flex;flex-wrap:wrap;gap:12px 24px;align-items:center;padding:12px 16px;background:var(--bg);border-bottom:1px solid var(--rule)}
h1{font-size:18px;margin:0;font-weight:600}
fieldset{border:0;margin:0;padding:0;display:flex;gap:8px;align-items:center}
legend{float:left;margin-right:6px;color:var(--muted)}
label{display:inline-flex;gap:4px;align-items:center;cursor:pointer}
section{padding:16px;border-bottom:1px solid var(--rule)}
h2{font-size:16px;margin:0 0 12px;font-weight:600}
.grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px}
.cell h3{font-size:13px;font-weight:600;color:var(--muted);margin:0 0 6px}
.cell img{display:block;width:100%;height:auto;border:1px solid var(--rule);border-radius:8px;background:#fff}
.cell a{color:inherit}
.missing{color:var(--muted);font-size:13px}
@media (max-width:900px){.grid{grid-template-columns:1fr}}
</style>
<header><h1>Blog directions · compare</h1>
<fieldset><legend>Mode</legend><label><input type="radio" name="mode" value="day" checked> Day</label><label><input type="radio" name="mode" value="night"> Night</label></fieldset>
<fieldset><legend>Width</legend>"""]
for w in (390, 750, 1100, 1440):
    out.append(f'<label><input type="radio" name="w" value="{w}"{" checked" if w == 390 else ""}> {w}</label>')
out.append('</fieldset><a href="index.html">Live fixture pages</a></header>')
for title, key in rows:
    out.append(f"<section><h2>{html.escape(title)}</h2><div class='grid'>")
    for d in "dabc":
        out.append(f"<div class='cell'><h3>{names[d]}</h3>")
        for mode in ("day", "night"):
            for w in (390, 750, 1100, 1440):
                f = f"{d}-{key}-{w}-{mode}.png"
                if f in files:
                    out.append(f'<a href="../../shots/{f}" data-mode="{mode}" data-w="{w}"><img loading="lazy" src="../../shots/{f}" alt="{names[d]}, {title}, {w}px, {mode}"></a>')
        out.append("<p class='missing' hidden>No shot at this width.</p></div>")
    out.append("</div></section>")
out.append("""<script>
function show(){var m=document.querySelector('[name=mode]:checked').value,w=document.querySelector('[name=w]:checked').value;
document.querySelectorAll('.cell').forEach(function(c){var any=false;c.querySelectorAll('a[data-mode]').forEach(function(a){var on=a.dataset.mode===m&&a.dataset.w===w;a.hidden=!on;any=any||on});c.querySelector('.missing').hidden=any});}
document.querySelectorAll('input').forEach(function(i){i.addEventListener('change',show)});show();
</script></html>""")
open(OUT, "w").write("".join(out))
print("wrote", OUT)
