"""Switch OFF vs live: probe fields (cards, CTA, summary, sticky, link) and pixels (PNG -> BMP via sips,
share of differing pixels and the rows they sit in). Usage: python3 -I compare.py <shots-dir> <tmp-dir>"""
import json
import subprocess
import sys
from pathlib import Path

SHOTS, TMP = Path(sys.argv[1]), Path(sys.argv[2])
probes = json.loads((SHOTS / 'probes.json').read_text())
KEYS = ('cta', 'summary', 'sellingPlan', 'loopGroup', 'sticky', 'linkShown', 'cards')


def pixels(png):
    bmp = TMP / (png.stem + '.bmp')
    subprocess.run(['sips', '-s', 'format', 'bmp', str(png), '--out', str(bmp)], capture_output=True, check=True)
    data = bmp.read_bytes()
    offset = int.from_bytes(data[10:14], 'little')
    width = int.from_bytes(data[18:22], 'little', signed=True)
    height = int.from_bytes(data[22:26], 'little', signed=True)
    bpp = int.from_bytes(data[28:30], 'little') // 8
    row = (width * bpp + 3) // 4 * 4
    return width, abs(height), bpp, row, data[offset:], height > 0


for name in sorted(k for k in probes if k.startswith('live-')):
    other = name.replace('live-', 'off-', 1)
    a, b = probes[name], probes.get(other)
    same = {k: a.get(k) == b.get(k) for k in KEYS}
    w1, h1, bpp, row, d1, up1 = pixels(SHOTS / f'{name}.png')
    w2, h2, _, _, d2, _ = pixels(SHOTS / f'{other}.png')
    diff_rows = []
    diff = 0
    if (w1, h1) == (w2, h2):
        for y in range(h1):
            r1, r2 = d1[y * row:(y + 1) * row], d2[y * row:(y + 1) * row]
            if r1 != r2:
                x0 = 880 if w1 > 1000 else 0; yy = h1 - 1 - y if up1 else y; n = 0 if yy < 80 else sum(1 for x in range(x0, w1) if r1[x * bpp:(x + 1) * bpp] != r2[x * bpp:(x + 1) * bpp])
                diff += n
                if n: diff_rows.append(yy)
    share = diff / (w1 * h1)
    span = f'rows {min(diff_rows)}-{max(diff_rows)}' if diff_rows else 'none'
    print(f'{name} vs {other}: probe same={all(same.values())} {[k for k, v in same.items() if not v]} '
          f'size={w1}x{h1}/{w2}x{h2} pixels differing={share:.4%} ({span})')
