// R67 · render the Research Behind System section with liquidjs, three ways:
//   old  = section + snippet at b0bb4fb (read with git show), cards from the section's blocks
//   new  = this checkout's section + snippet, cards from the blocks (must equal old)
//   meta = this checkout's section + snippet, cards from stubbed research_card metaobject entries
// Then write the file:// fixture (out/fixture.html) that shows "new" and "meta" side by side,
// and out/frame-390.html / out/frame-1440.html, which load it in an iframe of that width.
// Usage, from this folder: npm install --no-save liquidjs@10.21.0 && node render.mjs
import { Liquid } from 'liquidjs';
import { readFileSync, writeFileSync, mkdirSync, mkdtempSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import { fileURLToPath } from 'node:url';
import { tmpdir } from 'node:os';
import { dirname, join, resolve, relative } from 'node:path';

const HERE = dirname(fileURLToPath(import.meta.url));
const THEME = resolve(HERE, '../../..');
const BASE = 'b0bb4fb';
const OUT = join(HERE, 'out');
// The old copies live outside the theme root: Theme Check would otherwise lint them as orphans
const OLD = mkdtempSync(join(tmpdir(), 'r67-old-'));
mkdirSync(join(OUT, 'img'), { recursive: true });
mkdirSync(join(OLD, 'sections'), { recursive: true });
mkdirSync(join(OLD, 'snippets'), { recursive: true });
for (const f of ['sections/research-behind-system.liquid', 'snippets/research-card.liquid']) {
  writeFileSync(join(OLD, f), execFileSync('git', ['-C', THEME, 'show', `${BASE}:${f}`]));
}
const ASSETS = relative(OUT, join(THEME, 'assets')); // relative, so the fixture works from any checkout

const stripComment = (s) => s.replace(/^\s*\/\*[\s\S]*?\*\/\s*/, '');
const readJson = (p) => JSON.parse(stripComment(readFileSync(p, 'utf8')));
const home = readJson(join(THEME, 'templates/index.json')).sections.research_behind_system_EkjATL;
const pdp = readJson(join(THEME, 'templates/product.subscription-item.json')).sections.research_behind_system_EkjATL;
const locale = readJson(join(THEME, 'locales/en.default.json'));

// ---- placeholder images (the real files live in Shopify Files, not in the repo)
const svg = (label, w, h, fill) =>
  `<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h}" viewBox="0 0 ${w} ${h}"><rect width="${w}" height="${h}" fill="${fill}"/><text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle" font-family="sans-serif" font-size="${Math.round(h / 12)}" fill="#fffbf6">${label}</text></svg>`;
const images = {};
function imageFor(ref) {
  if (!ref) return null;
  if (!images[ref]) {
    const name = ref.replace('shopify://shop_images/', '').replace(/\.png$/i, '');
    const isLogo = /^Logo/.test(name);
    const file = `img/${name.toLowerCase()}.svg`;
    writeFileSync(join(OUT, file), isLogo ? svg(name, 200, 64, '#2c3a60') : svg(name, 800, 960, '#4f6a8f'));
    images[ref] = { src: file, alt: '', width: isLogo ? 200 : 800, height: isLogo ? 64 : 960 };
  }
  return images[ref];
}

// ---- liquidjs engines (one per source tree), with Shopify filters stubbed
function engine(root) {
  // The old tree holds only the two files that changed; every other snippet comes from the checkout
  const liquid = new Liquid({
    root: [join(root, 'sections')],
    partials: [join(root, 'snippets'), join(THEME, 'snippets')],
    extname: '.liquid',
    strictFilters: true,
    jsTruthy: false,
  });
  const named = (args) => Object.fromEntries((args || []).filter(Array.isArray));
  liquid.registerFilter('asset_url', (name) => `${ASSETS}/${name}`);
  liquid.registerFilter('stylesheet_tag', (url) => `<link rel="stylesheet" href="${url}">`);
  liquid.registerFilter('inline_asset_content', (name) => readFileSync(join(THEME, 'assets', name), 'utf8').trim());
  liquid.registerFilter('t', (key) => key.split('.').reduce((o, k) => (o ? o[k] : undefined), locale) ?? key);
  liquid.registerFilter('image_url', (img) => img);
  liquid.registerFilter('image_tag', (img, ...args) => {
    const a = named(args);
    const attrs = [`src="${img.src}"`];
    if (a.sizes) attrs.push(`sizes="${a.sizes}"`);
    if (a.widths) attrs.push(`srcset="${img.src} ${img.width}w"`);
    attrs.push(`width="${img.width}"`, `height="${img.height}"`, `alt="${img.alt}"`);
    if (a.loading) attrs.push(`loading="${a.loading}"`);
    if (a.class) attrs.push(`class="${a.class}"`);
    return `<img ${attrs.join(' ')}>`;
  });
  // {% schema %} prints nothing; {% style %} prints a <style> element
  liquid.registerTag('schema', {
    parse(tagToken, remainTokens) {
      const stream = this.liquid.parser.parseStream(remainTokens);
      stream.on('tag:endschema', () => stream.stop()).on('end', () => { throw new Error('endschema not found'); });
      stream.start();
    },
    * render() { return ''; },
  });
  liquid.registerTag('style', {
    parse(tagToken, remainTokens) {
      this.templates = [];
      const stream = this.liquid.parser.parseStream(remainTokens);
      stream.on('template', (tpl) => this.templates.push(tpl))
        .on('tag:endstyle', () => stream.stop())
        .on('end', () => { throw new Error('endstyle not found'); });
      stream.start();
    },
    * render(ctx, emitter) {
      emitter.write('<style>');
      yield this.liquid.renderer.renderTemplates(this.templates, ctx, emitter);
      emitter.write('</style>');
    },
  });
  return liquid;
}
const oldLiquid = engine(OLD);
const newLiquid = engine(THEME);

// ---- contexts
// A sixth card checks the two edge cases the task names: a "#" URL (plain label) and no image.
const FIXTURE_BLOCK = {
  type: 'card',
  settings: {
    subheading: 'FIXTURE · PLAIN LABEL',
    heading: 'A card without a study URL and without an image.',
    subtext: 'Checks the plain source chip · no new-tab icon',
    result_label: 'RESULT',
    result_text: 'One line of result text (a text setting cannot hold a line break)',
    method_label: 'METHOD',
    method_text: 'Fixture only, not for the store.',
    link_label: 'Fixture et al. · 2026',
    link_url: '#',
    image_badge: 'NO IMAGE SO NO BADGE',
  },
};

function blocks(section, withFixture) {
  const list = section.block_order.map((id) => ({
    id,
    type: section.blocks[id].type,
    settings: { ...section.blocks[id].settings, logo: imageFor(section.blocks[id].settings.logo), image: imageFor(section.blocks[id].settings.image) },
    shopify_attributes: '',
  }));
  if (withFixture) list.push({ id: 'card_fixture', ...FIXTURE_BLOCK, settings: { ...FIXTURE_BLOCK.settings, logo: null, image: null }, shopify_attributes: '' });
  return list;
}

// The HTML an inline_richtext / text setting holds is what the metaobject author types as plain text
const decode = (s) => (s ?? '').replace(/&nbsp;/g, ' ').replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/<[^>]+>/g, '');
const sl = (v) => ({ type: 'single_line_text_field', value: v == null || v === '' ? null : decode(v) });
const ml = (v) => ({ type: 'multi_line_text_field', value: v == null || v === '' ? null : decode(v) });
const rt = (v) => ({ type: 'rich_text_field', value: v ? { type: 'root', children: [{ type: 'paragraph', children: [{ type: 'text', value: decode(v) }] }] } : null });
const file = (img) => ({ type: 'file_reference', value: img || null });
const url = (v) => ({ type: 'url', value: v || null });

function entry(handle, s, logo, image) {
  return {
    system: { handle, type: 'research_card' },
    subheading: sl(s.subheading), heading: rt(s.heading), subtext: ml(s.subtext),
    result_label: sl(s.result_label), result_text: ml(s.result_text),
    method_label: sl(s.method_label), method_text: ml(s.method_text),
    link_label: sl(s.link_label), link_url: url(s.link_url),
    logo: file(logo), image: file(image), image_badge: sl(s.image_badge),
  };
}
function entries(section, withFixture) {
  const list = section.block_order.map((id) => {
    const s = section.blocks[id].settings;
    return entry(id, s, imageFor(s.logo), imageFor(s.image));
  });
  if (withFixture) list.push(entry('fixture', FIXTURE_BLOCK.settings, null, null));
  return list;
}

function render(liquid, id, settings, blockList, cards) {
  const section = { id, settings: { ...settings, cards }, blocks: blockList };
  return liquid.renderFileSync('research-behind-system', { section });
}

const norm = (html) => html.replace(/>\s+</g, '><').replace(/\s+/g, ' ').replace(/ >/g, '>').trim();
const unescape = (html) => html.replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&#39;/g, "'").replace(/&nbsp;/g, ' ');

function diffAt(a, b) {
  let i = 0;
  while (i < a.length && a[i] === b[i]) i++;
  return `first difference at ${i}:\n  A: …${a.slice(Math.max(0, i - 80), i + 120)}\n  B: …${b.slice(Math.max(0, i - 80), i + 120)}`;
}

const results = [];
function compare(label, a, b, fn = (x) => x) {
  const na = norm(fn(a)), nb = norm(fn(b)); // decode first: norm folds a NBSP into a space
  const ok = na === nb;
  results.push(`${ok ? 'PASS' : 'FAIL'} ${label}${ok ? '' : '\n' + diffAt(na, nb)}`);
  return ok;
}
const sha256 = (s) => createHash('sha256').update(s).digest('hex');

// ---- R67-B1 gate: with the setting empty, the real five-card sections must be byte-identical
// to b0bb4fb. Raw UTF-8 comparison, no decoding, no whitespace normalisation, for every way the
// setting can be empty (absent, null, empty string, empty list) and for the three layouts.
const GRID = { ...home.settings, marquee: false }; // slider_mobile + slider_desktop stay on: the <li> gets slider__slide
const PLAIN = { ...GRID, slider_mobile: false, slider_tablet: false, slider_laptop: false, slider_desktop: false };
for (const [label, settings, tpl] of [['homepage marquee', home.settings, home], ['pdp marquee', pdp.settings, pdp], ['homepage grid/slider', GRID, home], ['pdp grid/slider', { ...pdp.settings, marquee: false }, pdp], ['homepage plain grid', PLAIN, home]]) {
  const before = render(oldLiquid, 'research_behind_system_EkjATL', settings, blocks(tpl, false), undefined);
  for (const [empty, cards] of [['absent', undefined], ['null', null], ['empty string', ''], ['empty list', []]]) {
    const after = render(newLiquid, 'research_behind_system_EkjATL', settings, blocks(tpl, false), cards);
    const ok = before === after;
    results.push(`${ok ? 'PASS' : 'FAIL'} raw bytes, ${label}, cards ${empty}: ${Buffer.byteLength(before)} bytes at ${BASE}, ${Buffer.byteLength(after)} now, sha256 ${sha256(before).slice(0, 16)} vs ${sha256(after).slice(0, 16)}${ok ? '' : '\n' + diffAt(before, after)}`);
  }
}
const variants = [
  ['homepage marquee', 'home', home.settings, home],
  ['pdp marquee', 'pdp', pdp.settings, pdp],
  ['homepage grid/slider', 'grid', GRID, home],
];
const pages = {};
for (const [label, id, settings, tpl] of variants) {
  const oldHtml = render(oldLiquid, id, settings, blocks(tpl, true), undefined);
  const newHtml = render(newLiquid, id, settings, blocks(tpl, true), undefined);
  const metaHtml = render(newLiquid, id, settings, blocks(tpl, true), entries(tpl, true));
  const emptyHtml = render(newLiquid, id, settings, blocks(tpl, true), []);
  compare(`${label}: new section with blocks == old section (${BASE})`, oldHtml, newHtml);
  compare(`${label}: cards from metaobject entries == cards from blocks (entities decoded)`, newHtml, metaHtml, unescape);
  compare(`${label}: an empty cards setting renders the blocks`, newHtml, emptyHtml);
  // Guard: the metaobject path must escape, and the "#" URL must be a plain label
  if (!/Lei &amp; Hu/.test(metaHtml)) results.push(`FAIL ${label}: metaobject text is not escaped`);
  if ((metaHtml.match(/<span class="research-card__source">/g) || []).length !== 1) results.push(`FAIL ${label}: expected exactly one plain-label chip`);
  if ((metaHtml.match(/target="_blank" rel="noopener"/g) || []).length !== 5) results.push(`FAIL ${label}: expected five new-tab study links`);
  pages[id] = { newHtml, metaHtml };
}

// A multi-line field keeps its line breaks as <br>, and an empty field prints nothing
const twoLine = entries(home, true)[5];
twoLine.result_text = ml('Line one\nLine two');
twoLine.subtext = ml(null);
const twoLineHtml = newLiquid.renderFileSync('../snippets/research-card', { card: twoLine });
results.push(`${/Line one<br \/>\nLine two/.test(twoLineHtml) ? 'PASS' : 'FAIL'} research-card: a multi-line entry field prints <br> between its lines`);
results.push(`${!/research-card__subtext/.test(twoLineHtml) ? 'PASS' : 'FAIL'} research-card: an empty entry field prints no element`);

// Rich text formatting through the walker on its own: bold, italic, a link, two paragraphs, a list
const rich = {
  type: 'rich_text_field',
  value: { type: 'root', children: [
    { type: 'paragraph', children: [
      { type: 'text', value: 'Nano-HAp sealed ' }, { type: 'text', value: '98%', bold: true }, { type: 'text', value: ' of open ' },
      { type: 'link', url: 'https://example.com/a?b=1&c=2', title: 'Study & more', children: [{ type: 'text', value: 'dentine', italic: true }] },
      { type: 'text', value: ' tubules <3' },
    ] },
    { type: 'heading', level: 2, children: [{ type: 'text', value: 'Second line', bold: true, italic: true }] },
    { type: 'list', listType: 'unordered', children: [
      { type: 'list-item', children: [{ type: 'text', value: 'one' }] },
      { type: 'list-item', children: [{ type: 'text', value: 'two' }] },
    ] },
  ] },
};
const richOut = newLiquid.renderFileSync('../snippets/kc-rich-text-inline', { field: rich });
const richWant = 'Nano-HAp sealed <strong>98%</strong> of open <a href="https://example.com/a?b=1&amp;c=2" title="Study &amp; more"><em>dentine</em></a> tubules &lt;3<br><strong><em>Second line</em></strong><br>onetwo';
results.push(`${richOut.trim() === richWant ? 'PASS' : 'FAIL'} rich text walker: bold, italic, link, paragraphs, list\n  got:  ${richOut.trim()}\n  want: ${richWant}`);

// R67-B2 gate: a link becomes an <a> only for http, https, mailto, tel and scheme-less relative,
// query or anchor URLs; anything else prints the text without a link. Attributes are escaped.
const linkField = (url, extra = {}) => ({ type: 'rich_text_field', value: { type: 'root', children: [
  { type: 'paragraph', children: [{ type: 'link', url, ...extra, children: [{ type: 'text', value: 'probe', bold: true }] }] },
] } });
const linkCases = [
  // [label, url, expected output]
  ['https', 'https://example.com/x', '<a href="https://example.com/x"><strong>probe</strong></a>'],
  ['http upper case', 'HTTP://EXAMPLE.COM/', '<a href="HTTP://EXAMPLE.COM/"><strong>probe</strong></a>'],
  ['https with surrounding whitespace', '  https://example.com/x \n', '<a href="https://example.com/x"><strong>probe</strong></a>'],
  ['mailto', 'mailto:hello@example.com', '<a href="mailto:hello@example.com"><strong>probe</strong></a>'],
  ['tel', 'tel:+3212345678', '<a href="tel:+3212345678"><strong>probe</strong></a>'],
  ['root-relative', '/pages/science', '<a href="/pages/science"><strong>probe</strong></a>'],
  ['root-relative with a colon in the query', '/search?q=a:b', '<a href="/search?q=a:b"><strong>probe</strong></a>'],
  ['anchor', '#research', '<a href="#research"><strong>probe</strong></a>'],
  ['query', '?variant=1', '<a href="?variant=1"><strong>probe</strong></a>'],
  ['dot-relative', '../pages/science', '<a href="../pages/science"><strong>probe</strong></a>'],
  ['bare relative path', 'pages/science', '<a href="pages/science"><strong>probe</strong></a>'],
  // liquidjs escapes a double quote as &#34;, Shopify as &quot;: the same character for the browser
  ['title and target escaped, rel added', 'https://example.com/?a=1&b="2"', '<a href="https://example.com/?a=1&amp;b=&#34;2&#34;" title="A &#34;title&#34; &amp; more" target="_blank" rel="noopener"><strong>probe</strong></a>', { title: 'A "title" & more', target: '_blank' }],
  ['target other than _blank is dropped', 'https://example.com/', '<a href="https://example.com/"><strong>probe</strong></a>', { target: '_top" onclick="x' }],
  ['javascript', 'javascript:alert(1)', '<strong>probe</strong>'],
  ['javascript mixed case', 'JavaScript:alert(1)', '<strong>probe</strong>'],
  ['javascript with leading whitespace', ' \t\n javascript:alert(1)', '<strong>probe</strong>'],
  ['javascript with a tab inside the scheme', 'java\tscript:alert(1)', '<strong>probe</strong>'],
  ['javascript with a newline inside the scheme', 'java\nscript:alert(1)', '<strong>probe</strong>'],
  ['javascript with a null byte', 'java\u0000script:alert(1)', '<strong>probe</strong>'],
  ['javascript with a leading control character', '\u0001javascript:alert(1)', '<strong>probe</strong>'],
  ['data', 'data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg==', '<strong>probe</strong>'],
  ['data mixed case', 'DATA:text/html,<script>alert(1)</script>', '<strong>probe</strong>'],
  ['vbscript', 'vbscript:MsgBox(1)', '<strong>probe</strong>'],
  ['file', 'file:///etc/passwd', '<strong>probe</strong>'],
  ['unknown scheme', 'ftp://example.com/', '<strong>probe</strong>'],
  ['empty', '', '<strong>probe</strong>'],
  ['whitespace only', '   ', '<strong>probe</strong>'],
  ['missing url', undefined, '<strong>probe</strong>'],
];
for (const [label, url, want, extra] of linkCases) {
  const got = newLiquid.renderFileSync('../snippets/kc-rich-text-inline', { field: linkField(url, extra) }).trim();
  results.push(`${got === want ? 'PASS' : 'FAIL'} rich text link ${label}: ${JSON.stringify(url)}${got === want ? '' : `\n  got:  ${got}\n  want: ${want}`}`);
}
// Entity-obfuscated schemes stay text: the "&" is escaped, so the browser never sees a colon
const colonEntity = newLiquid.renderFileSync('../snippets/kc-rich-text-inline', { field: linkField('javascript&colon;alert(1)') }).trim();
results.push(`${colonEntity === '<a href="javascript&amp;colon;alert(1)"><strong>probe</strong></a>' ? 'PASS' : 'FAIL'} rich text link javascript&colon; stays a harmless relative path (escaped &)\n  got: ${colonEntity}`);
const multi = newLiquid.renderFileSync('../snippets/kc-rich-text-inline', { field: { type: 'multi_line_text_field', value: 'Plain <b>heading</b>\nsecond line' } });
results.push(`${multi.trim() === 'Plain &lt;b&gt;heading&lt;/b&gt;<br />\nsecond line' ? 'PASS' : 'FAIL'} rich text walker: multi-line fallback escapes and breaks lines\n  got: ${JSON.stringify(multi.trim())}`);
const empty = newLiquid.renderFileSync('../snippets/kc-rich-text-inline', { field: null });
results.push(`${empty.trim() === '' ? 'PASS' : 'FAIL'} rich text walker: a missing field prints nothing (${JSON.stringify(empty)})`);

console.log(results.join('\n'));
writeFileSync(join(OUT, 'liquid-results.txt'), results.join('\n') + '\n');

// ---- the fixture page
const fixtureCss = readFileSync(join(HERE, 'fixture.css'), 'utf8');
const fixtureJs = readFileSync(join(HERE, 'fixture.js'), 'utf8');
const sectionWrap = (title, html) => `<div class="fx-variant"><p class="fx-title">${title}</p>${html}</div>`;
const page = `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>R67 research cards fixture</title>
<link rel="stylesheet" href="https://use.typekit.net/kss0igj.css">
<link rel="stylesheet" href="${ASSETS}/base.css">
<link rel="stylesheet" href="${ASSETS}/kc-tokens.css">
<link rel="stylesheet" href="${ASSETS}/kc-surface.css">
<style>${fixtureCss}</style>
</head>
<body class="gradient">
<div class="fx-bar">
  <strong>R67 fixture</strong> · first of each pair: section blocks (today) · second: research_card metaobject entries (stubbed)
  <button type="button" id="fx-toggle">Toggle Night</button>
  <button type="button" id="fx-run">Run checks</button>
</div>
<pre id="fx-report" class="fx-report">waiting…</pre>
<div class="fx-pair" data-fx-pair="marquee">
${sectionWrap('Marquee · blocks', pages.home.newHtml)}
${sectionWrap('Marquee · metaobject entries', pages.home.metaHtml)}
</div>
<div class="fx-pair" data-fx-pair="grid">
${sectionWrap('Grid/slider · blocks', pages.grid.newHtml)}
${sectionWrap('Grid/slider · metaobject entries', pages.grid.metaHtml)}
</div>
<script>${fixtureJs}</script>
</body>
</html>
`;
writeFileSync(join(OUT, 'fixture.html'), page);
for (const w of [390, 1440]) {
  writeFileSync(join(OUT, `frame-${w}.html`), `<!doctype html><html><head><meta charset="utf-8"><title>R67 fixture at ${w}</title>
<style>html,body{margin:0;background:#888}iframe{display:block;border:0;width:${w}px;height:${w < 750 ? 844 : 900}px}pre{margin:0;padding:8px;font:12px/1.4 monospace;background:#fff;color:#000;white-space:pre-wrap}</style></head>
<body><pre id="report">waiting for the frame…</pre><iframe id="frame" title="fixture"></iframe>
<script>
document.getElementById('frame').src = 'fixture.html' + location.search; // ?mode=night opens the frame in Night
window.fxSend = (data) => document.getElementById('frame').contentWindow.postMessage(data, '*'); // {fxScroll: selector} or {fxMode: 'night'|'day'}
window.addEventListener('message', (e) => { if (e.data && e.data.fxReport) { document.getElementById('report').textContent = e.data.fxReport; document.title = 'R67 fixture at ${w} · ' + (e.data.fxReport.includes('FAIL') ? 'FAIL' : 'done'); } });
</script></body></html>`);
}
console.log('fixture written to', OUT);
if (results.some((r) => r.startsWith('FAIL'))) process.exitCode = 1;
