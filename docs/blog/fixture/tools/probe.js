location.protocol.indexOf('http') !== 0 ? 'BLANK' : JSON.stringify({
  url: location.href,
  w: innerWidth,
  h: innerHeight,
  y: scrollY,
  docH: document.documentElement.scrollHeight,
  bodyH: document.body.scrollHeight,
  bq: (function () { var e = document.querySelector('.kc-blog__body blockquote'); return e ? Math.round(e.getBoundingClientRect().top + scrollY) : null; })(),
  related: (function () { var e = document.querySelector('.kc-blog__section-heading'); return e ? Math.round(e.getBoundingClientRect().top + scrollY) : null; })(),
  overflowX: document.documentElement.scrollWidth,
  navItems: document.querySelectorAll('[data-kc-blog-toc] li').length,
  articleH: (function () { var e = document.querySelector('.kc-blog-a__body'); return e ? Math.round(e.getBoundingClientRect().height) : null; })(),
  gridCols: (function () { var e = document.querySelector('.kc-blog-a__body .kc-blog-a__grid'); return e ? getComputedStyle(e).gridTemplateColumns : null; })(),
})
