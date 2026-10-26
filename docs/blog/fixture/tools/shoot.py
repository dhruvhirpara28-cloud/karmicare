"""Screenshot fixture pages in Orca's tab, one viewport at a time.

usage: python3 -I shoot.py <browserPageId> <out.png> <url> <width> <height> [--settle N]

goto -> set viewport W H -> a throwaway screenshot (the tab only draws a frame per screenshot,
so the page's resize and load handlers run) -> the real screenshot.
"""
import base64, json, subprocess, sys, struct

page, out, url, w, h = sys.argv[1:6]
settle = int(sys.argv[sys.argv.index("--settle") + 1]) if "--settle" in sys.argv else 1


def orca(*args):
    p = subprocess.run(["orca", *args, "--page", page, "--json"], capture_output=True, text=True, timeout=180)
    try:
        return json.loads(p.stdout)
    except Exception:
        sys.exit(f"orca {args[0]}: {p.stdout[:300]} {p.stderr[-300:]}")


r = orca("goto", "--url", url)
if not r.get("ok"):
    sys.exit(f"goto failed: {r.get('error')}")
orca("exec", "--command", f"set viewport {w} {h}")
for _ in range(settle):
    orca("screenshot")
r = orca("screenshot")
if not r.get("ok"):
    sys.exit(f"screenshot failed: {r.get('error')}")
raw = base64.b64decode(r["result"]["data"])
open(out, "wb").write(raw)
pw, ph = struct.unpack(">II", raw[16:24])
print(f"{out} {pw}x{ph} {len(raw)} bytes")
