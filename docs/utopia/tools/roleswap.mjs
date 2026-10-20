#!/usr/bin/env node
// Find rules that switch a --kc-responsive-* type role inside a media query, e.g. h2 on
// mobile and h4 from 750px. Today both ends meet at the 750px step; with fluid tokens the
// two roles differ at the boundary and the text jumps. node docs/utopia/tools/roleswap.mjs
import { readFileSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../..');
const files = execFileSync('git', ['ls-files', 'assets/*.css', 'assets/*.css.liquid', 'sections/*.liquid', 'snippets/*.liquid', 'layout/*.liquid'],
  { cwd: ROOT, encoding: 'utf8' }).trim().split('\n')
  .filter((f) => !/kc-tokens\.css|kc-fluid\.css|loop-widget/.test(f));
const ROLE = /var\(--kc-responsive-([a-z0-9-]+?)-(text-size|line-height)\b/;
const PROPS = /^\s*(font-size|line-height|--[a-zA-Z0-9_-]+)\s*:\s*([^;]+);/;

for (const f of files) {
  const lines = readFileSync(path.join(ROOT, f), 'utf8').split('\n');
  const stack = [];
  const seen = new Map(); // selector|prop -> [{media, role, line}]
  let pendingSel = '';
  lines.forEach((text, i) => {
    const prop = text.match(PROPS);
    if (prop && stack.length) {
      const role = prop[2].match(ROLE);
      const sel = stack.filter((s) => !s.startsWith('@')).at(-1) || '';
      const media = stack.filter((s) => s.startsWith('@media')).join(' ');
      if (role && sel) {
        const k = `${sel}|${prop[1]}`;
        if (!seen.has(k)) seen.set(k, []);
        seen.get(k).push({ media, role: role[1], line: i + 1 });
      }
    }
    for (const ch of text) {
      if (ch === '{') {
        stack.push((pendingSel + text.split('{')[0]).trim().replace(/\s+/g, ' '));
        pendingSel = '';
      } else if (ch === '}') stack.pop();
    }
    if (!text.includes('{') && !text.includes('}') && !prop && /[,]\s*$/.test(text)) pendingSel += text.trim() + ' ';
    else if (!text.includes('{')) pendingSel = '';
  });
  for (const [k, uses] of seen) {
    const roles = new Set(uses.map((u) => u.role));
    if (roles.size < 2) continue;
    const [sel, prop] = k.split('|');
    console.log(`${f} | ${sel.slice(0, 70)} | ${prop} | ${uses.map((u) => `${u.role}${u.media ? ' @' + u.media.replace(/@media (only )?screen and /, '') : ''} (:${u.line})`).join(' ; ')}`);
  }
}
