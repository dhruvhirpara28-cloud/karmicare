// Phase 2 check: render the theme's real blog Liquid (sections/main-article.liquid, sections/main-blog.liquid,
// snippets/kc-blog-row.liquid, snippets/share-button.liquid, snippets/pagination.liquid) with liquidjs, the
// Shopify filters stubbed, and the live articles from data/live.json. Writes data/rendered/*.html, which
// build.py puts into the live page shell as site/theme-*.html.
//
// Usage, from the repo root:
//   node docs/blog/fixture/render-liquid.mjs [path/to/liquidjs/dist/liquid.node.mjs]
// liquidjs 10.21.0 (as docs/research-metaobjects/fixture); the default path is the research lane's install.
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const HERE = dirname(fileURLToPath(import.meta.url));
const THEME = resolve(HERE, '../../..');
const LIQUIDJS = process.argv[2] || resolve(THEME, '../research-metaobjects/docs/research-metaobjects/fixture/node_modules/liquidjs/dist/liquid.node.mjs');
const { Liquid } = await import(pathToFileURL(LIQUIDJS).href);

const stripComment = (s) => s.replace(/^\s*\/\*[\s\S]*?\*\/\s*/, '');
const readJson = (p) => JSON.parse(stripComment(readFileSync(p, 'utf8')));
const data = readJson(join(HERE, 'data/live.json'));
// KC_LANG=nl or fr renders with that locale (file names get the suffix -nl / -fr)
const LANG = process.env.KC_LANG || '';
const locale = readJson(join(THEME, `locales/${LANG || 'en.default'}.json`));
// The four keys source-copy is adding (landing desk, 26 Oct); used only when the file has none yet
const PENDING = { on_this_page: 'On this page', sources: 'Sources', keep_reading: 'Keep reading', reading_time: '{{ minutes }} min read' };
for (const [k, v] of Object.entries(PENDING)) locale.blogs.article[k] ??= v;

// Shopify's images['name'] (files in this store's Files): the sizes measured by tools/probe-bodyimgs.js
const bodyImgs = readJson(join(HERE, 'data/bodyimgs.json'));
const images = Object.fromEntries(Object.entries(bodyImgs).filter(([, v]) => v.ownFiles).map(([n, v]) => [n, {
  src: `https://www.karmicare.com/cdn/shop/files/${n}`, width: v.ownFiles[0], height: v.ownFiles[1], alt: '',
}]));

const MONTHS = 'January February March April May June July August September October November December'.split(' ');
const named = (args) => Object.fromEntries((args || []).filter(Array.isArray));

const liquid = new Liquid({
  root: [join(THEME, 'sections')],
  partials: [join(THEME, 'snippets')],
  extname: '.liquid',
  strictFilters: true,
  jsTruthy: false,
});
liquid.registerFilter('asset_url', (name) => `/assets/${name}`);
liquid.registerFilter('stylesheet_tag', (url) => `<link rel="stylesheet" href="${url}">`);
liquid.registerFilter('inline_asset_content', (name) => readFileSync(join(THEME, 'assets', name), 'utf8').trim());
liquid.registerFilter('t', (key, ...args) => {
  let v = key.split('.').reduce((o, k) => (o ? o[k] : undefined), locale);
  if (typeof v !== 'string') return `translation missing: en.${key}`;
  for (const [k, val] of Object.entries(named(args))) v = v.replaceAll(`{{ ${k} }}`, String(val));
  return v;
});
// Shopify's split is Ruby's String#split: a single space splits on runs of whitespace and drops empty
// pieces; liquidjs's is JavaScript's, which would count every double space as an extra word
liquid.registerFilter('split', (s, sep) => (sep === ' ' ? String(s).trim().split(/\s+/).filter(Boolean) : String(s).split(sep)));
liquid.registerFilter('structured_data', (a) => JSON.stringify({ '@context': 'http://schema.org', '@type': 'BlogPosting', headline: a.title }));
liquid.registerFilter('time_tag', (iso) => {
  const [y, m, d] = iso.slice(0, 10).split('-');
  return `<time datetime="${iso}">${MONTHS[+m - 1]} ${+d}, ${y}</time>`;
});
const cdn = (src, w) => {
  const s = (src.startsWith('//') ? 'https:' + src : src).replace(/([?&])width=\d+&?/, '$1').replace(/[?&]$/, '');
  return s + (s.includes('?') ? '&' : '?') + `width=${w}`;
};
liquid.registerFilter('image_url', (img, ...args) => ({ ...img, requested: named(args).width }));
liquid.registerFilter('image_tag', (img, ...args) => {
  const a = named(args);
  const widths = String(a.widths || img.requested || img.width).split(',').map((x) => +x.trim()).filter((w) => w <= img.width);
  if (!widths.length) widths.push(img.width);
  const attrs = [`src="${cdn(img.src, Math.min(img.requested || img.width, img.width))}"`, `srcset="${widths.map((w) => `${cdn(img.src, w)} ${w}w`).join(', ')}"`];
  if (a.sizes) attrs.push(`sizes="${a.sizes}"`);
  attrs.push(`width="${img.width}"`, `height="${img.height}"`, `alt="${a.alt ?? img.alt ?? ''}"`);
  if (a.loading) attrs.push(`loading="${a.loading}"`);
  if (a.fetchpriority) attrs.push(`fetchpriority="${a.fetchpriority}"`);
  if (a.decoding) attrs.push(`decoding="${a.decoding}"`);
  return `<img ${attrs.join(' ')}>`;
});
liquid.registerTag('schema', {
  parse(tagToken, remainTokens) {
    const stream = this.liquid.parser.parseStream(remainTokens);
    stream.on('tag:endschema', () => stream.stop()).on('end', () => { throw new Error('endschema not found'); });
    stream.start();
  },
  * render() { return ''; },
});
// {% form %} (the comment form, Dawn's, unchanged): skipped unparsed, since liquidjs cannot read
// form.posted_successfully?; the fixture renders with comments off
liquid.registerTag('form', {
  parse(tagToken, remainTokens) {
    let depth = 1;
    while (remainTokens.length) {
      const t = remainTokens.shift();
      if (t.name === 'form') depth++;
      if (t.name === 'endform' && --depth === 0) return;
    }
    throw new Error('endform not found');
  },
  * render() { return ''; },
});
// {% paginate %}: the blog's eight articles on one page of 12, as the store would print them
liquid.registerTag('paginate', {
  parse(tagToken, remainTokens) {
    this.templates = [];
    const stream = this.liquid.parser.parseStream(remainTokens);
    stream.on('template', (tpl) => this.templates.push(tpl)).on('tag:endpaginate', () => stream.stop()).on('end', () => { throw new Error('endpaginate not found'); });
    stream.start();
  },
  * render(ctx, emitter) {
    ctx.push({ paginate: { pages: 1, current_page: 1, parts: [] } });
    yield this.liquid.renderer.renderTemplates(this.templates, ctx, emitter);
    ctx.pop();
  },
});

// ---- data: the live articles as Liquid objects
const order = data.index.map((i) => i.handle);
const excerpts = Object.fromEntries(data.index.map((i) => [i.handle, i.excerpt]));
const blog = { title: 'News', url: '/blogs/news', comments_enabled: false };
const article = (handle, n, image) => {
  const a = data.articles[handle];
  return {
    id: 1000 + n, handle, url: `/blogs/news/${handle}`, title: a.title, author: 'KARMICARE',
    published_at: a.published_at, content: a.content, excerpt: excerpts[handle] || '',
    image: image === undefined ? a.image : image,
  };
};
blog.articles = order.map((h, n) => article(h, n));

const tpl = readJson(join(THEME, 'templates/article.json')).sections.main;
const blocks = tpl.block_order.map((id) => ({ id, type: tpl.blocks[id].type, settings: tpl.blocks[id].settings, shopify_attributes: '' }));
const OUT = join(HERE, 'data/rendered');
mkdirSync(OUT, { recursive: true });

const DECIDED = { src: '//www.karmicare.com/cdn/shop/files/kc-research-nhap-dentinal-tubule-occlusion-2000_copy.png?v=1', width: 2000, height: 2000, alt: 'Illustration of open and filled dentine tubules' };
const pages = [
  ['article-nano', article('nano-hydroxyapatite', 7, DECIDED)],
  ['article-short', article('morning-and-night-time-brushing-why-timing-matters', 3)],
  ['article-noimage', article('headaches-and-tooth-pain-understanding-the-connection', 6, null)],
  ['article-wellness', article('how-oral-health-impacts-your-overall-wellness', 5)], // opens with an h5 (R90 B3)
];
for (const [name, a] of pages) {
  const section = { id: 'template--kc-blog__main', blocks, settings: tpl.settings };
  const html = liquid.renderFileSync('main-article', { article: a, blog, section, images, request: { origin: 'https://www.karmicare.com' } }, { globals: { section, images } });
  writeFileSync(join(OUT, `${name}${LANG ? '-' + LANG : ''}.html`), html);
  console.log('rendered', name, LANG, html.length);
}
if (LANG) process.exit(0);
const blogSection = { id: 'template--kc-blog__main', blocks: [], settings: readJson(join(THEME, 'templates/blog.json')).sections.main.settings };
for (const [name, list] of [['blog-many', blog.articles], ['blog-one', blog.articles.slice(0, 1)], ['blog-two', blog.articles.slice(0, 2)]]) {
  const html = liquid.renderFileSync('main-blog', { blog: { ...blog, articles: list }, section: blogSection }, { globals: { section: blogSection } });
  writeFileSync(join(OUT, `${name}.html`), html);
  console.log('rendered', name, html.length);
}
