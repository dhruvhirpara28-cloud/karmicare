#!/usr/bin/env node
// Side-by-side crop of two screenshots, labelled, for reviewing before/after.
//   node docs/utopia/tools/compose.mjs <a.png> <b.png> <x,y,w,h> <out.png> [labelA] [labelB]
// Renders a local HTML page in headless Chrome (--screenshot); no network.
import { spawnSync } from 'node:child_process';
import { mkdtempSync, writeFileSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import path from 'node:path';

const CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const [a, b, crop, out, la = 'before', lb = 'after'] = process.argv.slice(2);
const [x, y, w, h] = crop.split(',').map(Number);
const gap = 24;
const head = 36;
const dir = mkdtempSync(path.join(tmpdir(), 'utopia-compose-'));
const cell = (src, label) => `<figure><figcaption>${label}</figcaption>
  <div style="width:${w}px;height:${h}px;overflow:hidden;position:relative">
    <img src="file://${path.resolve(src)}" style="position:absolute;left:${-x}px;top:${-y}px">
  </div></figure>`;
writeFileSync(path.join(dir, 'c.html'), `<!doctype html><meta charset="utf-8"><style>
  body{margin:0;background:#888;display:flex;gap:${gap}px;padding:0 ${gap / 2}px;font:600 20px system-ui}
  figure{margin:0} figcaption{height:${head}px;line-height:${head}px;color:#fff}
</style>${cell(a, la)}${cell(b, lb)}`);
const r = spawnSync(CHROME, ['--headless=new', '--disable-breakpad', '--hide-scrollbars', `--user-data-dir=${path.join(dir, 'p')}`,
  `--window-size=${2 * w + 2 * gap},${h + head}`, '--allow-file-access-from-files', `--screenshot=${path.resolve(out)}`,
  `file://${path.join(dir, 'c.html')}`], { stdio: 'ignore' });
rmSync(dir, { recursive: true, force: true, maxRetries: 5 });
console.log(r.status === 0 ? `wrote ${out}` : `chrome exited ${r.status}`);
