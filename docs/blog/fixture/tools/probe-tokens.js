location.protocol.indexOf('http') !== 0 ? 'BLANK' : (function () {
  // Rendered colour and font of the blog's text roles, to check the tokens=next / soft=muted override.
  var roles = {
    title: 'h1.kc-blog__title', body: '.kc-blog__body > p:not(:has(img))', standfirst: '.kc-blog__standfirst',
    meta: '.kc-blog-d__bar .kc-blog__meta li', publisher: '.kc-blog-sources__host', heading: '.kc-blog__body > h1, .kc-blog__body > h2',
  };
  var out = { url: location.search, override: !!document.querySelector('style[data-fixture-tokens]') };
  Object.keys(roles).forEach(function (k) {
    var el = document.querySelector(roles[k]);
    if (!el) return;
    var c = getComputedStyle(el);
    out[k] = [c.color, c.fontFamily.split(',')[0]];
  });
  return JSON.stringify(out);
})()
