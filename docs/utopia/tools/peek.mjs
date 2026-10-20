#!/usr/bin/env node
// Quick terminal view of one measure.mjs result: node docs/utopia/tools/peek.mjs <data.json> <width> [texts|sections|grids|media|attr]
import { readFileSync } from 'node:fs';

const [file, width, what = 'sections'] = process.argv.slice(2);
const data = JSON.parse(readFileSync(file, 'utf8'));
const vp = data.viewports.find((v) => String(v.vw) === String(width));
if (!vp) throw new Error('no viewport ' + width);
const rows = {
  sections: () => vp.sections.map((s) => [s.name, s.top, s.height, s.textLeft, s.textRight, s.mediaLeft, s.mediaRight,
    s.containers.map((c) => `${c.sel}:${c.maxWidth}/${c.width}@${c.left}`).join(' ')]),
  texts: () => vp.texts.filter((t) => !t.offscreen).map((t) => [t.i, t.section, t.sel, t.fs, t.lh, t.fw, t.ff, t.lines, t.cplActual, t.cplCapacity, t.text.slice(0, 40)]),
  grids: () => vp.grids.map((g) => [g.section, g.sel, g.display, g.width, g.left, g.columns, g.gap, g.childWidths.join('/')]),
  media: () => vp.media.map((m) => [m.section, m.sel, m.src, m.w, m.h, m.left, m.natural, m.maxSrc, m.upscale, m.fullBleed]),
  attr: () => vp.texts.filter((t) => !t.offscreen).map((t) => {
    const a = (vp.attribution || {})[t.i] || {};
    const fs = a['font-size'] || {};
    return [t.i, t.section, t.sel, t.fs, fs.value, fs.file, fs.line, fs.inheritedDepth, (fs.selector || '').slice(0, 60)];
  }),
}[what]();
for (const r of rows) console.log(r.join(' | '));
console.log(`-- ${rows.length} rows; vw ${vp.vw}, doc ${vp.docHeight}, overflow ${vp.horizontalOverflow}, root ${vp.rootFontSize}px, mode ${vp.bodyMode}`);
