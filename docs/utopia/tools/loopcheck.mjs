#!/usr/bin/env node
// Loop widget exposure: compare computed font size and line height of every text element
// inside the Loop widget markup between two runs. node docs/utopia/tools/loopcheck.mjs [afterLabel]
import { readFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../..');
const label = process.argv[2] || 'after';
const load = (l) => JSON.parse(readFileSync(path.join(ROOT, 'docs/utopia/data', `pdp-${l}.json`), 'utf8'));
const before = load('before');
const after = load(label);
const isLoop = (t) => /loop|purchase-option|selling-plan|subscription/i.test(t.sel);
for (const vb of before.viewports) {
  const va = after.viewports.find((v) => v.vw === vb.vw);
  const bl = vb.texts.filter(isLoop);
  const al = va.texts.filter(isLoop);
  let changed = 0;
  const diffs = [];
  bl.forEach((t, n) => {
    const a = al[n];
    if (!a || a.sel !== t.sel) return;
    if (a.fs !== t.fs || a.lh !== t.lh) {
      changed++;
      diffs.push(`${t.sel} "${t.text.slice(0, 24)}" ${t.fs}/${t.lh} -> ${a.fs}/${a.lh}`);
    }
  });
  console.log(`${vb.vw}: ${bl.length} Loop texts, ${changed} changed`);
  for (const d of diffs.slice(0, 8)) console.log('   ', d);
}
