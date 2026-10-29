"""Build Kim-only plans with the existing source-copy builder, without network.

Usage: python3 docs/kim-verlot/build-offline-plans.py /path/to/source-copy-checkout
This writes only beside this script. It does not edit the source-copy checkout.
"""
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

here = Path(__file__).resolve().parent
builder = Path(sys.argv[1]) / 'docs/localization/registration/build_payloads.py'
spec = importlib.util.spec_from_file_location('builder', builder)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
sources = {e['id']: e for e in json.loads((here / 'source-additions.json').read_text())['entries']}
holds = {eid: 'Kim Verlot: nervous-system and receding-gum claims require review before public marketing; source cb09296, 29 Oct 2026.' for eid in sources}
for lang in ['nl', 'fr']:
    payload = {e['id']: e for e in json.loads((here / f'payload-{lang}.json').read_text())['entries']}
    resources, skipped = module.build(lang, payload, sources, holds=holds)
    items = [i for r in resources.values() for i in r['items']]
    assert len(items) == 2 and not skipped
    assert all(i['hold'] and i['gates'] for i in items)
    assert all(i['en_sha1'] == hashlib.sha1(i['en'].encode()).hexdigest() for i in items)
    doc = dict(lang=lang, status='offline only; no live keys/digests resolved; not registered',
               builder_sha256=hashlib.sha256(builder.read_bytes()).hexdigest(),
               resources=list(resources.values()), skipped=skipped)
    (here / f'offline-plan-{lang}.json').write_text(json.dumps(doc, ensure_ascii=False, indent=2) + '\n')
    print(f'{lang}: 2 resources, 2 full quotes, 2 held, 0 write eligible; no Shopify requests')
