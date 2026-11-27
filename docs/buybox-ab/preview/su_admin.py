"""Single-units audit (27 Nov), read only: the admin product page's text for each product ID (status,
publishing: sales channels and markets, collections, tags), from Victor's logged-in Orca admin tab.
Only reads innerText; never clicks or saves. Usage: python3 -I su_admin.py <page-id> <out.json> <id> [id ...]"""
import json
import subprocess
import sys
import time
from pathlib import Path

PAGE, OUT = sys.argv[1], Path(sys.argv[2])


def orca(*args):
    out = subprocess.run(['orca', *args, '--page', PAGE, '--json'], capture_output=True, text=True, timeout=120)
    return json.loads(out.stdout)


result = {}
for pid in sys.argv[3:]:
    orca('goto', '--url', f'https://admin.shopify.com/store/karmicares/products/{pid}')
    for _ in range(4):
        orca('screenshot')
        time.sleep(2)
    text = orca('eval', '--expression', "(document.querySelector('main') || document.body).innerText")['result']['result']
    result[pid] = text
    print('==', pid, len(text))
OUT.write_text(json.dumps(result, indent=1, ensure_ascii=False))
