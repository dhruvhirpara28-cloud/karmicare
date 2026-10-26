location.protocol.indexOf('http') !== 0 ? 'BLANK' : (function () {
  // Type audit: for each text role on this page, the rendered font size and line height, and
  // which design token (kc-tokens.css) or theme font variable has exactly that value here.
  var TOKENS = [];
  ['display', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'body-lg', 'body-md', 'body-sm', 'label-lg', 'label-sm', 'extra-small'].forEach(function (n) {
    TOKENS.push(['--kc-responsive-' + n + '-text-size', 'size']);
    TOKENS.push(['--kc-responsive-' + n + '-line-height', 'lh']);
  });
  ['--font-body-small-size', '--font-body-size-mobile', '--font-body-size-desktop', '--size-xl-desktop', '--font-body-medium-size-desktop',
   '--font-h1-size-desktop', '--font-h2-size-desktop', '--font-h3-size-desktop', '--font-h4-size-desktop', '--font-h5-size-desktop',
   '--font-h1-size-mobile', '--font-h2-size-mobile', '--font-h5-size-mobile'].forEach(function (n) { TOKENS.push([n, 'size']); });
  var probe = document.createElement('div');
  probe.style.cssText = 'position:absolute;visibility:hidden;line-height:normal';
  document.body.appendChild(probe);
  var values = {};
  TOKENS.forEach(function (t) {
    probe.style.fontSize = 'var(' + t[0] + ')';
    var v = getComputedStyle(probe).fontSize;
    if (getComputedStyle(document.documentElement).getPropertyValue(t[0]).trim()) values[t[0]] = [parseFloat(v), t[1]];
  });
  probe.remove();
  function match(px, kind) {
    var hits = Object.keys(values).filter(function (k) { return Math.abs(values[k][0] - px) < 0.3 && (kind === 'any' || values[k][1] === kind); });
    return hits.map(function (k) { return k.replace('--kc-responsive-', '').replace('-text-size', '').replace('-line-height', ' lh'); }).join(', ') || 'NO TOKEN';
  }
  var ROLES = {
    // blog fixture
    'eyebrow': '.kc-blog-d__eyebrow, .kc-blog__eyebrow',
    'title (h1)': 'h1.kc-blog__title, .article-template__title',
    'standfirst': '.kc-blog__standfirst',
    'meta / date': '.kc-blog-d__bar .kc-blog__meta li, .kc-blog__meta li',
    'share': '.kc-blog-d__share',
    'body text': '.kc-blog__body > p:not(:has(img)), .article-template__content p',
    'body list item': '.kc-blog__body li',
    'quote': '.kc-blog__body blockquote p',
    'section heading': '.kc-blog__body:has(h1) > h1, .kc-blog__body:not(:has(h1)) > h2, .article-template__content h2',
    'sub-heading': '.kc-blog__body:has(h1) > h2, .kc-blog__body:not(:has(h1)) > h3',
    'contents eyebrow': '.kc-blog-d-toc__eyebrow, .legal-toc__eyebrow',
    'contents link': '.kc-blog-d-toc__link, .legal-toc__nav-link',
    'sources heading': '.kc-blog-sources__heading',
    'sources title': '.kc-blog-sources__title',
    'sources publisher': '.kc-blog-sources__host',
    'keep reading heading': '.kc-blog__section-heading',
    'row title': '.kc-blog-a-row__title',
    'row excerpt': '.kc-blog-a-row__excerpt',
    // homepage and legal page, for comparison
    'home eyebrow': '.kc-caption-subheading',
    'home section heading': '.two-formulas__heading, .product-benefits h2, .research-behind-system__heading',
    'home body text': '.product-benefits__left p, .two-formulas p',
    'legal title': '.policy-banner h1, .shopify-policy__title h1',
    'legal clause title': '.legal-toc__title',
    'legal body': '.legal-toc__body p',
    'button': '.karmicare__btn-primary, .featured-product .button',
  };
  var out = { page: location.pathname, w: innerWidth, rows: [] };
  Object.keys(ROLES).forEach(function (role) {
    var el = Array.prototype.find.call(document.querySelectorAll(ROLES[role]), function (e) { return e.getBoundingClientRect().width > 0 || e.offsetParent; });
    if (!el) return;
    var c = getComputedStyle(el);
    var fs = parseFloat(c.fontSize);
    var lh = c.lineHeight === 'normal' ? 'normal' : parseFloat(c.lineHeight);
    out.rows.push([role, fs, match(fs, 'size'), lh, lh === 'normal' ? '(normal)' : match(lh, 'lh') + (lh ? ' (' + (lh / fs).toFixed(2) + ')' : ''), c.fontFamily.split(',')[0].replace(/"/g, ''), c.fontWeight]);
  });
  return JSON.stringify(out);
})()
