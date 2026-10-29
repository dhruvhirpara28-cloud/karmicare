// Professionals page v1, phase 1 preview (docs/pdp/practitioner-form/PROFESSIONALS-V1-PROPOSAL.md).
// Renders the prototype page section (proto/kc-professionals-page.liquid.proto) with the theme's own
// request-form snippet through liquidjs, into a saved live page of the legal family
// (live/withdrawal-*.html), and builds the PDP "before" (live as is) and "after" (form gone, the
// entry links pointing at the page) from live/pdp-en.html. Nothing posts to the store: every form
// action points at this localhost server and fx.js stops every submit.
// Usage, from this folder: node render.mjs   (then serve out/ on 127.0.0.1:9376)
import { Liquid } from 'liquidjs';
import { readFileSync, writeFileSync, mkdirSync, symlinkSync, existsSync, lstatSync, unlinkSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = dirname(fileURLToPath(import.meta.url));
const THEME = join(HERE, '../../../..');
const OUT = join(HERE, 'out');
const LIVE = join(HERE, 'live');
const PORT = 9376;
const STORE = 'https://www.karmicare.com';
const BLOCKED = `http://127.0.0.1:${PORT}/__blocked-contact-post`;
const STAMP = Date.now();
mkdirSync(OUT, { recursive: true });
for (const [link, target] of [['assets', join(THEME, 'assets')], ['proto', join(HERE, 'proto')]]) {
  // only ever remove the symlink itself, never what it points at (the theme's assets)
  let stat = null;
  try {
    stat = lstatSync(join(OUT, link));
  } catch (e) {
    /* not there yet */
  }
  if (stat && !stat.isSymbolicLink()) throw new Error(`out/${link} exists and is not a symlink; remove it by hand`);
  if (stat) unlinkSync(join(OUT, link));
  symlinkSync(target, join(OUT, link));
}

// ---- live DOM: absolute URLs, no posts to the store
const absolute = (html) =>
  html
    .replace(/(href|src|srcset|data-src|poster)="\/(?!\/)/g, `$1="${STORE}/`)
    .replace(/([ ,(])\/cdn\//g, `$1${STORE}/cdn/`)
    .replace(/action="(?:https?:)?(?:\/\/(?:www\.)?karmicare\.com|\/\/karmicares\.myshopify\.com)?\/[^"]*"/g, `action="${BLOCKED}"`);

function balanced(html, start) {
  // the element that opens at `start` (a <div>), up to its matching </div>
  let i = html.indexOf('>', start) + 1;
  let depth = 1;
  const re = /<div\b|<\/div>/g;
  re.lastIndex = i;
  let m;
  while ((m = re.exec(html))) {
    depth += m[0] === '</div>' ? -1 : 1;
    if (depth === 0) return { start, end: m.index + 6 };
  }
  throw new Error('unbalanced div at ' + start);
}

// ---- settings: the product template values (what moves to the page section), schema defaults
const stripComment = (s) => s.replace(/^\s*\/\*[\s\S]*?\*\/\s*/, '');
const tpl = JSON.parse(stripComment(readFileSync(join(THEME, 'templates/product.json'), 'utf8')));
const faqBlock = Object.values(tpl.sections.main.blocks).find((b) => b.type === 'product_faq');
const sec = readFileSync(join(THEME, 'sections/main-product.liquid'), 'utf8');
const schema = JSON.parse(sec.slice(sec.indexOf('{% schema %}') + 12, sec.indexOf('{% endschema %}')));
const defaults = {};
for (const s of schema.blocks.find((b) => b.type === 'product_faq').settings) if (s.id) defaults[s.id] = s.default;
// Since R76k the form's texts live in sections/practitioner-group.json (schema defaults in
// sections/kc-practitioner-request.liquid); the FAQ block keeps only its link triggers
const groupSrc = readFileSync(join(THEME, 'sections/kc-practitioner-request.liquid'), 'utf8');
const groupSchema = JSON.parse(groupSrc.slice(groupSrc.indexOf('{% schema %}') + 12, groupSrc.indexOf('{% endschema %}')));
const groupDefaults = {};
for (const s of groupSchema.settings) if (s.id) groupDefaults[s.id] = s.default;
const groupValues = Object.values(JSON.parse(stripComment(readFileSync(join(THEME, 'sections/practitioner-group.json'), 'utf8'))).sections)[0].settings;
const EN = { ...defaults, ...faqBlock.settings, ...groupDefaults, ...groupValues };
// The PDP intro points at "the studies referenced above"; on the page that sentence has no "above".
// The preview drops it and keeps the two other existing sentences (decision D4 in the proposal).
EN.request_intro = 'Tell us about your practice and what you need. A person reads every request and replies by email.';
EN.eyebrow = 'PROFESSIONAL PARTNERS'; // existing copy: the Trusted Professionals subheading

// NL / FR: the values live today (Translate & Adapt), matched to their key through the EN value;
// keys with no live translation stay English, as they would on the page
const liveTexts = JSON.parse(readFileSync(join(LIVE, 'form-texts-live.json'), 'utf8'));
function translated(lang) {
  const out = { ...EN };
  const en = liveTexts['pdp-en'];
  const other = liveTexts['pdp-' + lang];
  for (const [key, value] of Object.entries(EN)) {
    if (typeof value !== 'string' || !value) continue;
    const i = en.indexOf(value);
    if (i >= 0 && other[i] && other[i] !== value) out[key] = other[i];
  }
  // the page intro and eyebrow have no live translation yet
  return out;
}
const SETTINGS = { en: EN, nl: translated('nl'), fr: translated('fr') };
writeFileSync(join(OUT, 'settings-carried.json'), JSON.stringify({ nl: diff(SETTINGS.nl), fr: diff(SETTINGS.fr) }, null, 1));
function diff(s) {
  const o = {};
  for (const k of Object.keys(EN)) if (k.startsWith('request_') && typeof EN[k] === 'string') o[k] = s[k] === EN[k] ? null : s[k];
  return o;
}

// ---- liquidjs with Shopify bits stubbed
const LOCALES = Object.fromEntries(
  ['en', 'nl', 'fr'].map((l) => [l, JSON.parse(stripComment(readFileSync(join(THEME, `locales/${l === 'en' ? 'en.default' : l}.json`), 'utf8')))])
);
const FORMS = {
  default: { posted_successfully_q: false, errors: null },
  success: { posted_successfully_q: true, errors: null },
  error: (() => {
    const errors = ['email'];
    errors.messages = { email: 'is invalid' };
    errors.translated_fields = { email: 'Email' };
    return { posted_successfully_q: false, errors, name: 'Dr. An Peeters', email: 'an.peeters@praktijk', phone: '', body: 'Fixture message kept after the error.' };
  })(),
};
function engine(formState, globals) {
  const read = (f) => readFileSync(f, 'utf8').replace(/posted_successfully\?/g, 'posted_successfully_q');
  const liquid = new Liquid({
    globals,
    root: [join(THEME, 'snippets'), join(THEME, 'sections'), join(HERE, 'proto')],
    extname: '.liquid',
    strictFilters: true,
    jsTruthy: false,
    fs: {
      readFileSync: read,
      readFile: async (f) => read(f),
      existsSync,
      exists: async (f) => existsSync(f),
      // the prototype is kc-professionals-page.liquid.proto, so Theme Check (which scans every
      // .liquid file, docs/ too) leaves it alone; snippet names get .liquid as usual
      resolve: (root, file, ext) => join(root, /\.(liquid|proto)$/.test(file) ? file : file + ext),
      contains: () => true,
      sep: '/',
      dirname,
    },
  });
  // section files: {% schema %} renders nothing, {% style %} a <style> element
  liquid.registerTag('schema', {
    parse(tagToken, remainTokens) {
      const stream = this.liquid.parser.parseStream(remainTokens);
      stream.on('tag:endschema', () => stream.stop()).on('template', () => {}).on('end', () => {
        throw new Error('endschema not found');
      });
      stream.start();
    },
    *render() {},
  });
  liquid.registerTag('style', {
    parse(tagToken, remainTokens) {
      this.templates = [];
      const stream = this.liquid.parser.parseStream(remainTokens);
      stream.on('template', (t) => this.templates.push(t)).on('tag:endstyle', () => stream.stop()).on('end', () => {
        throw new Error('endstyle not found');
      });
      stream.start();
    },
    *render(ctx, emitter) {
      emitter.write('<style>');
      yield this.liquid.renderer.renderTemplates(this.templates, ctx, emitter);
      emitter.write('</style>');
    },
  });
  liquid.registerFilter('image_url', (src) => String(src || ''));
  liquid.registerFilter('image_tag', (src) => `<img src="${STORE}/cdn/shop/files/placeholder.png" alt="" data-fixture-src="${src}">`);
  liquid.registerFilter('placeholder_svg_tag', () => '<svg aria-hidden="true"></svg>');
  liquid.registerFilter('asset_url', (name) => `assets/${name}?v=${STAMP}`);
  liquid.registerFilter('stylesheet_tag', (url) => `<link href="${url}" rel="stylesheet" type="text/css" media="all" />`);
  liquid.registerFilter('inline_asset_content', (name) => readFileSync(join(THEME, 'assets', name), 'utf8').trim());
  liquid.registerFilter('t', (key) => key.split('.').reduce((o, k) => (o ? o[k] : undefined), LOCALES[globals.request.locale.iso_code]) ?? key);
  liquid.registerTag('form', {
    parse(tagToken, remainTokens) {
      this.args = tagToken.args;
      this.templates = [];
      const stream = this.liquid.parser.parseStream(remainTokens);
      stream
        .on('template', (t) => this.templates.push(t))
        .on('tag:endform', () => stream.stop())
        .on('end', () => {
          throw new Error('endform not found');
        });
      stream.start();
    },
    *render(ctx, emitter) {
      const arg = (k) => (this.args.match(new RegExp(`${k}:\\s*'([^']*)'`)) || [])[1] || '';
      emitter.write(`<form method="post" action="${BLOCKED}" id="${arg('id')}" accept-charset="UTF-8" class="${arg('class')}" data-kc-pr-form="true"><input type="hidden" name="form_type" value="contact" /><input type="hidden" name="utf8" value="✓" />`);
      ctx.push({ form: formState });
      yield this.liquid.renderer.renderTemplates(this.templates, ctx, emitter);
      ctx.pop();
      emitter.write('</form>');
    },
  });
  return liquid;
}

const FX = readFileSync(join(HERE, 'fx.js'), 'utf8');
const fxTag = (variant) => `<script>window.FX_VARIANT=${JSON.stringify(variant)};</script><script>${FX}</script>`;
const TITLES = { en: 'Professionals', nl: 'Professionals', fr: 'Professionnels' }; // the header menu's own labels
const results = [];

// ---- the professionals page, in the withdrawal page's frame
for (const [name, lang, state] of [
  ['page-en', 'en', 'default'],
  ['page-en-success', 'en', 'success'],
  ['page-en-error', 'en', 'error'],
  ['page-nl', 'nl', 'default'],
  ['page-fr', 'fr', 'default'],
  ['page-en-nojs', 'en', 'default'],
]) {
  const prefix = lang === 'en' ? '' : '/' + lang;
  const liquid = engine(FORMS[state], {
    pages: { 'privacy-policy': { url: `${STORE}${prefix}/pages/privacy-policy` } },
    shop: {},
    page: { title: TITLES[lang] },
    stamp: STAMP,
    request: { locale: { iso_code: lang }, origin: STORE, path: `${prefix}/pages/professionals` },
  });
  const html = await liquid.renderFile('kc-professionals-page.liquid.proto', { section: { id: 'professionals', settings: SETTINGS[lang] } });
  let dom = absolute(readFileSync(join(LIVE, `withdrawal-${lang}.html`), 'utf8'));
  // the page's one template section (a <section class="shopify-section">, no nested sections)
  const at = dom.search(/<section id="shopify-section-template--[^"]*__withdrawal"/);
  if (at < 0) throw new Error('withdrawal section not found in ' + lang);
  const end = dom.indexOf('</section>', at) + '</section>'.length;
  dom = dom.slice(0, at) + `<section id="shopify-section-template--professionals__main" class="shopify-section section">${html}</section>` + dom.slice(end);
  dom = dom.replace(/<title>[\s\S]*?<\/title>/, `<title>${TITLES[lang]} – KARMICARE (preview)</title>`);
  if (name.endsWith('nojs')) dom = dom.replace(/<script\b[\s\S]*?<\/script>/g, '').replace('<html class="js"', '<html class="no-js"');
  dom = dom.replace('</body>', fxTag(name) + '</body>');
  writeFileSync(join(OUT, `${name}.html`), dom);
  results.push(`${name}: form ${html.includes('KcPractitionerRequest') ? 'in' : 'absent'}`);
}

// ---- the PDP before (live as is) and after (form gone, links to the page)
const pdpLive = absolute(readFileSync(join(LIVE, 'pdp-en.html'), 'utf8'));
writeFileSync(join(OUT, 'pdp-before.html'), pdpLive.replace('</body>', fxTag('pdp-before') + '</body>'));
let after = pdpLive;
const panelAt = after.indexOf('<div\n  class="kc-pr"') >= 0 ? after.indexOf('<div\n  class="kc-pr"') : after.search(/<div\s+class="kc-pr"\s/);
if (panelAt < 0) throw new Error('form panel not found in the live PDP');
const panel = balanced(after, panelAt);
after = after.slice(0, panel.start) + after.slice(panel.end);
after = after
  .replace(/<link[^>]*kc-practitioner-request\.css[^>]*>/g, '')
  .replace(/<script[^>]*kc-practitioner-request\.js[^>]*><\/script>/g, '');
const pageUrl = (from) => `page-en.html?from=${from}`;
// the two FAQ links (the metafield's anchors), by the same text match the form uses today
after = after.replace(/<a class="rda-link" data-scroll="[^"]*" href="#">/, `<a class="rda-link" href="${pageUrl('pdp-faq-dentists')}">`);
after = after.replace(/<a href="#">(Practitioner evidence pack and samples available)/, `<a href="${pageUrl('pdp-faq-kpni')}">$1`);
// the Trusted Professionals CTA: the "Coming soon" button becomes a link
// (the shared kc-coming-soon snippet: an <a role="link" aria-disabled> with a tooltip span)
const cta = after.search(/<a\s+id="TrustedProfessionalsCta-[^"]*"\s+class="karmicare__btn-secondary kc-coming-soon"/);
if (cta >= 0) {
  const end = after.indexOf('</a>', cta) + '</a>'.length;
  const svg = (after.slice(cta, end).match(/<svg[\s\S]*?<\/svg>/) || [''])[0];
  after = after.slice(0, cta) + `<a href="${pageUrl('pdp-trusted')}" class="karmicare__btn-secondary">REQUEST A PRACTITIONER SAMPLE${svg}</a>` + after.slice(end);
}
writeFileSync(join(OUT, 'pdp-after.html'), after.replace('</body>', fxTag('pdp-after') + '</body>'));
results.push(`pdp-after: panel removed ${!after.includes('KcPractitionerRequest')}, CTA link ${cta >= 0}`);

// ---- the PDP as this branch builds it (R76g popup + the Trusted button, 26 Oct), and the homepage
// with the real trusted-professionals section. The FAQ items come from the live PDP's DOM; the
// product_faq block and trusted section settings from the branch's templates.
function innerOf(html, openTag, from) {
  const start = html.indexOf(openTag, from);
  if (start < 0) return null;
  const box = balanced(html, start);
  return { inner: html.slice(start + openTag.length, box.end - 6), start, end: box.end };
}
const subTpl = JSON.parse(stripComment(readFileSync(join(THEME, 'templates/product.subscription-item.json'), 'utf8')));
const homeTpl = JSON.parse(stripComment(readFileSync(join(THEME, 'templates/index.json'), 'utf8')));
const subFaq = Object.values(subTpl.sections.main.blocks).find((b) => b.type === 'product_faq');
const FAQ_SETTINGS = { ...defaults, ...subFaq.settings };
const sectionOf = (tplJson, type) => {
  const [id, s] = Object.entries(tplJson.sections).find(([, v]) => v.type === type);
  const order = s.block_order || Object.keys(s.blocks || {});
  return { id, settings: { ...s.settings }, blocks: order.map((bid) => ({ id: bid, ...s.blocks[bid], shopify_attributes: '' })) };
};
const liveItems = (dom) => {
  const faq = innerOf(dom, '<div class="kc-faq-block pdp">', 0);
  const items = [];
  for (const chunk of faq.inner.split(/<details\s+class="kc-faq-item"/).slice(1)) {
    const html = '<details' + chunk;
    const title = (html.match(/<summary class="kc-faq-summary">\s*<span>([\s\S]*?)<\/span>/) || [])[1];
    const d = innerOf(html, '<div class="kc-faq-description">', 0);
    const c = innerOf(html, '<div class="kc-faq-section-content">', 0);
    items.push({ title, description: d ? { html: d.inner.trim() } : null, section_content: c ? c.inner.trim() : '' });
  }
  return { faq, items };
};
const replaceSection = (dom, idPart, html) => {
  const at = dom.search(new RegExp(`<section id="shopify-section-template--[^"]*__${idPart}"`));
  if (at < 0) throw new Error('section not found: ' + idPart);
  const open = dom.slice(at, dom.indexOf('>', at) + 1);
  const end = dom.indexOf('</section>', at) + '</section>'.length;
  return dom.slice(0, at) + open + html + '</section>' + dom.slice(end);
};
// The practitioner group (R76k): layout/theme.liquid renders sections/practitioner-group.json
// between <main> and the footer group on the homepage and product pages. The section file is
// rendered from its source (its own name would resolve to the snippet of the same name).
const GROUP = JSON.parse(stripComment(readFileSync(join(THEME, 'sections/practitioner-group.json'), 'utf8')));
const GROUP_SECTION = Object.entries(GROUP.sections)[0];
async function renderGroup(liquid) {
  const src = readFileSync(join(THEME, 'sections/kc-practitioner-request.liquid'), 'utf8').replace(/posted_successfully\?/g, 'posted_successfully_q');
  const html = await liquid.parseAndRender(src, { section: { id: GROUP_SECTION[0], settings: GROUP_SECTION[1].settings } });
  return `<div id="shopify-section-sections--fixture__${GROUP_SECTION[0]}" class="shopify-section shopify-section-group-practitioner-group">${html}</div>`;
}
const beforeFooter = (dom, html) => {
  const at = dom.search(/<[a-z]+ id="shopify-section-sections--[^"]*__footer"/);
  if (at < 0) throw new Error('footer group not found');
  return dom.slice(0, at) + html + dom.slice(at);
};
const pdpSrc = absolute(readFileSync(join(LIVE, 'pdp-en.html'), 'utf8'));
const { faq: liveFaq, items: ITEMS } = liveItems(pdpSrc);
const faqScriptEnd = pdpSrc.indexOf('</script>', liveFaq.end) + '</script>'.length;
for (const [name, state] of [
  ['pdp-current', 'default'],
  ['pdp-current-success', 'success'],
]) {
  const globals = {
    pages: { 'privacy-policy': { url: `${STORE}/pages/privacy-policy` } },
    shop: {},
    stamp: STAMP,
    request: { locale: { iso_code: 'en' }, origin: STORE, path: '/products/karmicare-biorhythmic-oral-care-system', page_type: 'product' },
    product: { url: 'pdp-current.html', metafields: { custom: { product_faq: { value: ITEMS } } } },
  };
  const liquid = engine(FORMS[state], globals);
  liquid.registerFilter('metafield_tag', (m) => (m && m.html) || '');
  const faqHtml = await liquid.renderFile('product-faq', { block: { settings: FAQ_SETTINGS }, product: globals.product });
  const trusted = await liquid.renderFile('trusted-professionals', { section: sectionOf(subTpl, 'trusted-professionals'), product: globals.product });
  let dom = pdpSrc.slice(0, liveFaq.start) + faqHtml + pdpSrc.slice(faqScriptEnd);
  dom = replaceSection(dom, 'trusted_professionals_HAqYth', trusted);
  // the live page still carries the R76f form inside the FAQ item: drop its assets, then add the group
  dom = dom.replace(/<link[^>]*cdn\/shop[^>]*kc-practitioner-request\.css[^>]*>/g, '').replace(/<script[^>]*cdn\/shop[^>]*kc-practitioner-request\.js[^>]*><\/script>/g, '');
  // R94 B1: the same page with the form's section hidden or removed in the editor
  if (state === 'default') writeFileSync(join(OUT, 'pdp-nogroup.html'), dom.replace('</body>', fxTag('pdp-nogroup') + '</body>'));
  dom = beforeFooter(dom, await renderGroup(liquid));
  writeFileSync(join(OUT, `${name}.html`), dom.replace('</body>', fxTag(name) + '</body>'));
  results.push(`${name}: triggers by text ${FAQ_SETTINGS.request_trigger_text}, trusted CTA ${/data-kc-pr-open/.test(trusted) ? 'opens the form' : 'no opener'}`);
}
for (const [name, state] of [
  ['home-current', 'default'],
  ['home-current-success', 'success'],
  ['home-current-error', 'error'],
]) {
  const liquid = engine(FORMS[state], {
    pages: { 'privacy-policy': { url: `${STORE}/pages/privacy-policy` } },
    shop: {},
    stamp: STAMP,
    request: { locale: { iso_code: 'en' }, origin: STORE, path: '/', page_type: 'index' },
  });
  const section = sectionOf(homeTpl, 'trusted-professionals');
  const trusted = await liquid.renderFile('trusted-professionals', { section });
  let dom = replaceSection(absolute(readFileSync(join(LIVE, 'home-en.html'), 'utf8')), 'trusted_professionals_HAqYth', trusted);
  if (state === 'default') writeFileSync(join(OUT, 'home-nogroup.html'), dom.replace('</body>', fxTag('home-nogroup') + '</body>'));
  dom = beforeFooter(dom, await renderGroup(liquid));
  writeFileSync(join(OUT, `${name}.html`), dom.replace('</body>', fxTag(name) + '</body>'));
  if (name === 'home-current') results.push(`home-current: trusted CTA href ${(trusted.match(/href="([^"]*)"[^>]*data-kc-pr-open/) || [])[1]}`);
}
// the PDP without JavaScript: the links jump to the form at the end of the page
{
  const src = readFileSync(join(OUT, 'pdp-current.html'), 'utf8');
  writeFileSync(
    join(OUT, 'pdp-current-nojs.html'),
    src.replace(/<script\b(?![^>]*>window\.FX_VARIANT)[\s\S]*?<\/script>/g, '').replace('<html class="js"', '<html class="no-js"').replace(/window\.FX_VARIANT="pdp-current"/, 'window.FX_VARIANT="pdp-current-nojs"')
  );
}

// ---- the frame page: loads a variant in an iframe of a given size (scrolled captures stay drawn)
writeFileSync(
  join(OUT, 'frame.html'),
  `<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>frame</title>
<style>html,body{margin:0;background:#888}iframe{border:0;display:block}</style>
<script>const p=new URLSearchParams(location.search);document.write('<iframe id="f" src="'+p.get('src')+'" width="'+(p.get('w')||390)+'" height="'+(p.get('h')||900)+'"></iframe>');</script>`
);
console.log(results.join('\n'));
