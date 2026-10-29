"""Run `orca eval` until it reaches the real page instead of Orca's blank frame.

usage: python3 -I oeval.py <browserPageId> <expression-file> <out-file> [tries]

Orca's eval sometimes runs in an about:blank context (often the first call after the tab
sat idle). The expression must return the string 'BLANK' when location.protocol is not
http(s); this script then retries. The result string is written to <out-file>.
"""
import json, subprocess, sys, time

page, expr_file, out_file = sys.argv[1:4]
tries = int(sys.argv[4]) if len(sys.argv) > 4 else 12
expr = open(expr_file).read().strip()

for n in range(1, tries + 1):
    p = subprocess.run(
        ["orca", "eval", "--page", page, "--expression", expr, "--json"],
        capture_output=True, text=True, timeout=600,
    )
    try:
        data = json.loads(p.stdout)
    except Exception:
        print(f"try {n}: unparsable output: {p.stdout[:300]} {p.stderr[-300:]}")
        time.sleep(0.5)
        continue
    if not data.get("ok"):
        print(f"try {n}: error {json.dumps(data.get('error'))[:500]}")
        sys.exit(1)
    res = data["result"]["result"]
    if res in ("BLANK", "about:blank"):
        print(f"try {n}: blank frame")
        time.sleep(0.3)
        continue
    open(out_file, "w").write(res if isinstance(res, str) else json.dumps(res))
    print(f"try {n}: ok, {len(str(res))} chars -> {out_file}")
    sys.exit(0)
sys.exit("gave up: blank frame every time")
