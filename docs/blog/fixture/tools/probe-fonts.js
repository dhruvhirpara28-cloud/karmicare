location.protocol.indexOf('http') !== 0 ? 'BLANK' : (async () => {
  // Which font each part of the page renders in, and whether the kit's fonts loaded.
  await document.fonts.ready;
  const pick = {
    title: 'h1',
    body: '.kc-blog__body p, .article-template__content p',
    heading: '.kc-blog__body h1, .kc-blog__body h2, .article-template__content h2',
    kicker: '.kc-blog-d__kicker time, .article-template time',
    toc: '.kc-blog-d-toc__link',
    nav: '.header__menu-item, .header a',
    cta: '.featured-product .button, .karmicare__btn-primary, product-form button',
  };
  const out = { url: location.pathname };
  for (const [k, sel] of Object.entries(pick)) {
    const el = document.querySelector(sel);
    if (!el) { out[k] = null; continue; }
    const c = getComputedStyle(el);
    out[k] = [c.fontFamily.slice(0, 60), c.fontSize, c.fontWeight, c.textTransform];
  }
  out.loaded = Array.from(document.fonts).filter((f) => f.status === 'loaded').map((f) => f.family + ' ' + f.weight).filter((v, i, a) => a.indexOf(v) === i);
  out.proxima = document.fonts.check('16px proxima-nova');
  out.nunito = document.fonts.check('16px Nunito');
  return JSON.stringify(out);
})()
