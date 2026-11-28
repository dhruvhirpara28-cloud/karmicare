"""Single-units audit (27 Nov), read only: fetch live storefront URLs same-origin from an isolated Orca tab
on www.karmicare.com (no preview cookie; the sandbox proxy rate-limits direct curl) and save the bodies.
Usage: python3 -I su_fetch.py <page-id> <out-dir> <path> [path ...]   (path like /products.json)"""
import json
import re
import subprocess
import sys
from pathlib import Path

PAGE, OUT = sys.argv[1], Path(sys.argv[2])
OUT.mkdir(parents=True, exist_ok=True)


def ev(expr):
    out = subprocess.run(['orca', 'eval', '--expression', expr, '--page', PAGE, '--json'], capture_output=True, text=True, timeout=120)
    return json.loads(out.stdout)['result']['result']


for path in sys.argv[3:]:
    expr = ("fetch(" + json.dumps(path) + ", { credentials: 'omit', cache: 'no-store' })"
            ".then(async (r) => JSON.stringify({ status: r.status, url: r.url, body: await r.text() }))")
    raw = ev(expr)
    data = json.loads(raw)
    name = re.sub(r'[^a-zA-Z0-9._-]+', '_', path.strip('/')) or 'root'
    (OUT / name).write_text(data['body'])
    print(path, data['status'], data['url'].replace('https://www.karmicare.com', ''), len(data['body']))
