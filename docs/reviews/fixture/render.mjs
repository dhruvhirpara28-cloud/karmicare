// R95 · render the hero professionals badge (sections/hero-karmicare.liquid, block
// testimonial_badge) and the PDP category strip (snippets/product-category-strip.liquid)
// with liquidjs, then write a file:// fixture page and frame pages per viewport width.
//
// liquidjs cannot prove Shopify objects: product.metafields, request.locale, the image
// filters and the t filter are stubbed here. What this proves is the Liquid logic of the
// two files and the layout of the printed markup under the theme's own CSS.
//
// Usage, from this folder:
//   npm install --no-save liquidjs@10.21.0     (or point LIQUIDJS at an existing install)
//   node render.mjs                             PASS/FAIL lines, exit 1 on any FAIL, then out/
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { dirname, join, resolve, relative } from 'node:path';
import { createRequire } from 'node:module';

const HERE = dirname(fileURLToPath(import.meta.url));
const THEME = resolve(HERE, '../../..');
const OUT = join(HERE, 'out');
mkdirSync(OUT, { recursive: true });

const require = createRequire(import.meta.url);
const liquidPkg = process.env.LIQUIDJS ? join(process.env.LIQUIDJS, 'dist/liquid.node.mjs') : require.resolve('liquidjs/dist/liquid.node.mjs');
const { Liquid } = await import(pathToFileURL(liquidPkg).href);

const stripComment = (s) => s.replace(/^\s*\/\*[\s\S]*?\*\/\s*/, '');
const readJson = (p) => JSON.parse(stripComment(readFileSync(p, 'utf8')));
const locales = {
  en: readJson(join(THEME, 'locales/en.default.json')),
  nl: readJson(join(THEME, 'locales/nl.json')),
  fr: readJson(join(THEME, 'locales/fr.json')),
};
const lookup = (obj, key) => key.split('.').reduce((o, k) => (o ? o[k] : undefined), obj);
// Absolute file URL: a relative url() inside the --kc-category-logo custom property would be
// resolved against the stylesheet that uses it (assets/kc-category-strip.css), not the page
const ASSETS = pathToFileURL(join(THEME, 'assets')).href;

// ---- the theme's own values
const index = readJson(join(THEME, 'templates/index.json'));
const pdp = readJson(join(THEME, 'templates/product.subscription-item.json'));
const heroKey = Object.keys(index.sections).find((k) => index.sections[k].type === 'hero-karmicare');
const heroSection = index.sections[heroKey];
const badgeKey = Object.keys(heroSection.blocks).find((k) => heroSection.blocks[k].type === 'testimonial_badge');
const badgeBlock = heroSection.blocks[badgeKey];
const stripBlock = pdp.sections.main.blocks.category_strip_block;
const SECTION_ID = `template--27582179377533__${heroKey}`;

// ---- liquidjs engine per locale, Shopify filters stubbed
function engine(iso) {
  const liquid = new Liquid({
    root: [join(THEME, 'snippets'), join(THEME, 'sections')],
    partials: [join(THEME, 'snippets')],
    extname: '.liquid',
    strictFilters: true,
    jsTruthy: false,
  });
  const named = (args) => Object.fromEntries((args || []).filter(Array.isArray));
  liquid.registerFilter('asset_url', (name) => `${ASSETS}/${name}`);
  liquid.registerFilter('stylesheet_tag', (url) => `<link rel="stylesheet" href="${url}">`);
  liquid.registerFilter('inline_asset_content', (name) => readFileSync(join(THEME, 'assets', name), 'utf8').trim());
  liquid.registerFilter('t', (key, ...args) => {
    let s = lookup(locales[iso], key) ?? lookup(locales.en, key) ?? key;
    for (const [k, v] of Object.entries(named(args))) s = s.replace(new RegExp(`{{\\s*${k}\\s*}}`, 'g'), String(v));
    return s;
  });
  liquid.registerFilter('image_url', (img) => img);
  liquid.registerFilter('image_tag', (img, ...args) => {
    const a = named(args);
    const attrs = [`src="${img.src}"`, `width="${a.width || img.width}"`, `height="${a.height || img.height}"`, `alt="${a.alt || ''}"`];
    if (a.class) attrs.push(`class="${a.class}"`);
    return `<img ${attrs.join(' ')}>`;
  });
  liquid.registerFilter('placeholder_svg_tag', () => '<svg class="placeholder-svg"></svg>');
  // Shopify's image_tag returns an HTML-safe string that a later escape leaves alone (verified on
  // the live homepage: the badge <img> prints as an element); plain text is escaped as usual
  const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#39;');
  liquid.registerFilter('escape', (s) => (s == null ? '' : /^<img /.test(String(s)) ? String(s) : esc(s)));
  return liquid;
}
const engines = { en: engine('en'), nl: engine('nl'), fr: engine('fr') };

// ---- the badge block's two fragments, read from the section as it is in this checkout
const heroSrc = readFileSync(join(THEME, 'sections/hero-karmicare.liquid'), 'utf8');
function fragment(nth) {
  let from = -1;
  for (let i = 0; i <= nth; i++) from = heroSrc.indexOf("{%- when 'testimonial_badge' -%}", from + 1);
  const start = from + "{%- when 'testimonial_badge' -%}".length;
  const end = heroSrc.indexOf('{%- endcase -%}', start);
  return heroSrc.slice(start, end);
}
const badgeStyle = fragment(0);
const badgeMarkup = fragment(1);

const avatar = { src: 'avatar.svg', width: 56, height: 72 };
writeFileSync(join(OUT, 'avatar.svg'), '<svg xmlns="http://www.w3.org/2000/svg" width="56" height="72" viewBox="0 0 56 72"><rect width="56" height="72" fill="#4f6a8f"/></svg>');

function renderBadge(iso, ratingText) {
  const block = { id: badgeKey, type: 'testimonial_badge', shopify_attributes: '', settings: { ...badgeBlock.settings, image: avatar, rotate_professionals: false, rating_text: ratingText } };
  const ctx = { block, section: { id: SECTION_ID } };
  const style = engines[iso].parseAndRenderSync(badgeStyle, ctx);
  const html = engines[iso].parseAndRenderSync(badgeMarkup, ctx);
  return `<style>${style}</style><div id="shopify-section-${SECTION_ID}" class="fx-hero"><div class="hero-karmicare">${html}</div></div>`;
}

function renderStrip(iso, settings, metafields) {
  const block = { id: 'category_strip_block', type: 'category_strip', shopify_attributes: '', settings };
  const product = { metafields: { reviews: metafields || {} } };
  return engines[iso].renderFileSync('product-category-strip', { block, product, request: { locale: { iso_code: iso } } });
}

// ---- Liquid checks
const results = [];
const check = (ok, label, detail = '') => results.push(`${ok ? 'PASS' : 'FAIL'} ${label}${detail ? '\n  ' + detail : ''}`);
const norm = (html) => html.replace(/>\s+</g, '><').replace(/\s+/g, ' ').trim();
const score = (html) => { const m = norm(html).match(/<span class="kc-category-strip__score" aria-hidden="true">(.*?)<\/span><\/span>/); return m ? m[1].replace(/<[^>]+>/g, '').trim() : null; };
const aria = (html) => { const m = html.match(/class="kc-category-strip__rating"\s+role="img"\s+aria-label="([^"]*)"/); return m ? m[1] : null; };

const WITH = { rating: { value: { rating: 4.6, scale_max: 5 } }, rating_count: { value: 12 } };
const strips = {};
const variants = [
  ['fixed-en', 'en', stripBlock.settings, null, '4.7/5 (110)', '4.7 out of 5 stars, 110 total reviews'],
  ['fixed-nl', 'nl', stripBlock.settings, null, '4,7/5 (110)', '4,7 van de 5 sterren, 110 totaal aantal recensies'],
  ['fixed-fr', 'fr', stripBlock.settings, null, '4,7/5 (110)', '4,7 sur 5 étoiles, 110 total des critiques'],
  ['metafield-en', 'en', { ...stripBlock.settings, rating_source: 'metafield' }, WITH, '4.6/5 (12)', '4.6 out of 5 stars, 12 total reviews'],
  ['metafield-nl', 'nl', { ...stripBlock.settings, rating_source: 'metafield' }, WITH, '4,6/5 (12)', '4,6 van de 5 sterren, 12 totaal aantal recensies'],
  ['metafield-empty-en', 'en', { ...stripBlock.settings, rating_source: 'metafield' }, null, null, null],
  ['fixed-count-0-en', 'en', { ...stripBlock.settings, rating_count: 0 }, null, null, null],
  ['fixed-off-en', 'en', { ...stripBlock.settings, show_rating: false }, null, null, null],
];
for (const [name, iso, settings, meta, wantScore, wantAria] of variants) {
  const html = renderStrip(iso, settings, meta);
  strips[name] = html;
  const gotScore = score(html);
  const gotAria = aria(html);
  check(gotScore === wantScore && gotAria === wantAria, `strip ${name}: score ${JSON.stringify(gotScore)}, accessible name ${JSON.stringify(gotAria)}`, gotScore === wantScore && gotAria === wantAria ? '' : `want ${JSON.stringify(wantScore)} / ${JSON.stringify(wantAria)}`);
  check(!/<a[\s>]/.test(html), `strip ${name}: no link in the strip`);
  check(/class="kc-category-strip__brand"\s+role="img"/.test(html), `strip ${name}: the artwork keeps role="img" and its label`);
  if (wantScore) check(/class="kc-category-strip__rating"\s+role="img"/.test(html) && /kc-icon--star/.test(html) && /kc-category-strip__count/.test(html), `strip ${name}: rating span has role="img", the star icon and the count span`);
}
check(stripBlock.settings.rating_source === 'fixed' && stripBlock.settings.rating_value === '4.7' && stripBlock.settings.rating_count === 110 && stripBlock.settings.show_rating === true, `template product.subscription-item.json category_strip_block: ${JSON.stringify(stripBlock.settings)}`);
check(badgeBlock.settings.rating_text === '4.7/5 (110)', `template index.json ${badgeKey} rating_text: ${JSON.stringify(badgeBlock.settings.rating_text)}`);
const schemaDefault = heroSrc.match(/"id": "rating_text",[\s\S]*?"default": "([^"]*)"/);
check(schemaDefault && schemaDefault[1] === '4.7/5 (110)', `hero schema default rating_text: ${JSON.stringify(schemaDefault && schemaDefault[1])}`);

const heroes = {
  en: renderBadge('en', badgeBlock.settings.rating_text),
  nl: renderBadge('nl', '4,7/5 (110)'), // the NL/FR value source-copy registers for this setting
};
for (const [iso, html] of Object.entries(heroes)) {
  const text = (html.match(/hero-karmicare__badge-rating-text">([^<]*)</) || [])[1];
  check(text === (iso === 'en' ? '4.7/5 (110)' : '4,7/5 (110)'), `hero badge ${iso}: rating text ${JSON.stringify(text)}`);
  check(/<a\s+href="#shopify-section-[^"]+"\s+class="hero-karmicare__badge /.test(html), `hero badge ${iso}: the whole badge keeps its Trusted Professionals link`);
  const ratingPart = html.slice(html.indexOf('hero-karmicare__badge-rating"'), html.indexOf('hero-karmicare__badge-heading-wrap'));
  check(!/<a[\s>]/.test(ratingPart), `hero badge ${iso}: no separate link on the rating line`);
}

console.log(results.join('\n'));
writeFileSync(join(OUT, 'liquid-results.txt'), results.join('\n') + '\n');
for (const [name, html] of Object.entries(strips)) writeFileSync(join(OUT, `strip-${name}.html`), html);
for (const [iso, html] of Object.entries(heroes)) writeFileSync(join(OUT, `hero-${iso}.html`), html);

// ---- the fixture page
const fixtureCss = readFileSync(join(HERE, 'fixture.css'), 'utf8');
const fixtureJs = readFileSync(join(HERE, 'fixture.js'), 'utf8');
const stripVariant = (name, title) => `<div class="fx-strip" data-variant="${name}"><p class="fx-title">${title}</p><div class="fx-buybox">${strips[name].replace(/<link[^>]*>/, '')}</div></div>`;
const page = `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>R95 rating fixture</title>
<link rel="stylesheet" href="https://use.typekit.net/kss0igj.css">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;500;600;700&display=swap">
<link rel="stylesheet" href="${ASSETS}/base.css">
<link rel="stylesheet" href="${ASSETS}/kc-tokens.css">
<link rel="stylesheet" href="${ASSETS}/kc-surface.css">
<link rel="stylesheet" href="${ASSETS}/section-hero-karmicare.css">
<link rel="stylesheet" href="${ASSETS}/kc-category-strip.css">
<style>${fixtureCss}</style>
</head>
<body class="gradient day-mode">
<div class="fx-bar"><strong>R95 fixture</strong> · hero badge (index.json value) and PDP strip variants from liquidjs
  <button type="button" id="fx-toggle">Toggle Night</button>
  <button type="button" id="fx-run">Run checks</button>
</div>
<pre id="fx-report" class="fx-report">waiting…</pre>
<div class="fx-heroes">
<div class="fx-hero-variant" data-variant="en"><p class="fx-title">Hero badge · EN · templates/index.json rating_text</p>${heroes.en}</div>
<div class="fx-hero-variant" data-variant="nl"><p class="fx-title">Hero badge · NL/FR · the value source-copy registers (4,7/5 (110))</p>${heroes.nl}</div>
</div>
${stripVariant('fixed-en', 'Strip · fixed · EN (template values)')}
${stripVariant('fixed-nl', 'Strip · fixed · NL')}
${stripVariant('fixed-fr', 'Strip · fixed · FR')}
${stripVariant('metafield-en', 'Strip · metafield path · EN (stubbed reviews.rating 4.6, count 12)')}
${stripVariant('metafield-nl', 'Strip · metafield path · NL')}
${stripVariant('metafield-empty-en', 'Strip · metafield path · no metafield (artwork only)')}
<script>${fixtureJs}</script>
</body>
</html>
`;
writeFileSync(join(OUT, 'fixture.html'), page);
for (const w of [320, 390, 750, 990, 1440]) {
  writeFileSync(join(OUT, `frame-${w}.html`), `<!doctype html><html><head><meta charset="utf-8"><title>R95 fixture at ${w}</title>
<style>html,body{margin:0;background:#888}iframe{display:block;border:0;width:${w}px;height:${w < 750 ? 760 : 820}px}pre{margin:0;padding:6px 8px;font:11px/1.35 monospace;background:#fff;color:#000;white-space:pre-wrap}</style></head>
<body><pre id="report">waiting for the frame…</pre><iframe id="frame" title="fixture"></iframe>
<script>
document.getElementById('frame').src = 'fixture.html' + location.search; // ?mode=night opens the frame in Night
window.addEventListener('message', (e) => { if (e.data && e.data.fxReport) { document.getElementById('report').textContent = e.data.fxReport; document.title = 'R95 fixture at ${w} · ' + (e.data.fxReport.includes('FAIL') ? 'FAIL' : 'done'); } });
</script></body></html>`);
}
// Several frames on one page: frame-multi.html?frames=390:day,390:night,320:day,320:night&h=600
writeFileSync(join(OUT, 'frame-multi.html'), `<!doctype html><html><head><meta charset="utf-8"><title>R95 fixture, several frames</title>
<style>html,body{margin:0;background:#888}#frames{display:flex;flex-wrap:wrap;gap:8px;padding:8px}figure{margin:0}figcaption{font:11px/1.4 monospace;color:#fff}iframe{display:block;border:0;background:#fff}pre{margin:0;padding:6px 8px;font:10px/1.3 monospace;background:#fff;color:#000;white-space:pre-wrap}</style></head>
<body><pre id="report">waiting for the frames…</pre><div id="frames"></div>
<script>
const q = new URLSearchParams(location.search);
const h = Number(q.get('h') || 600);
const reports = {};
const wins = new Map();
for (const spec of (q.get('frames') || '390:day,390:night').split(',')) {
  const [w, mode] = spec.split(':');
  const fig = document.createElement('figure');
  const cap = document.createElement('figcaption'); cap.textContent = w + ' · ' + mode; fig.appendChild(cap);
  const f = document.createElement('iframe'); f.width = w; f.height = h; f.src = 'fixture.html' + (mode === 'night' ? '?mode=night' : ''); fig.appendChild(f);
  document.getElementById('frames').appendChild(fig);
  wins.set(f.contentWindow, spec);
}
window.addEventListener('message', (e) => {
  if (!e.data || !e.data.fxReport) return;
  reports[wins.get(e.source) || '?'] = e.data.fxReport;
  const text = Object.entries(reports).map(([k, v]) => '## ' + k + '\\n' + v).join('\\n');
  document.getElementById('report').textContent = text;
  document.title = 'R95 fixture, several frames · ' + (text.includes('FAIL') ? 'FAIL' : 'done');
});
</script></body></html>`);
console.log('fixture written to', OUT);
if (results.some((r) => r.startsWith('FAIL'))) process.exitCode = 1;
