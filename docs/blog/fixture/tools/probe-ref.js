location.protocol !== 'https:' ? 'BLANK' : (function () {
  // Reference article (openai.com/index/…): measures type, column, images and the contents list.
  var px = function (n) { return Math.round(n); };
  var st = function (el) {
    if (!el) return null;
    var c = getComputedStyle(el), r = el.getBoundingClientRect();
    return {
      tag: el.tagName, cls: (el.className && el.className.baseVal === undefined ? el.className : '').slice(0, 80),
      text: (el.textContent || '').trim().slice(0, 60),
      x: px(r.left), y: px(r.top + scrollY), w: px(r.width), h: px(r.height),
      fs: c.fontSize, lh: c.lineHeight, fw: c.fontWeight, ls: c.letterSpacing, ff: c.fontFamily.slice(0, 40),
      color: c.color, mt: c.marginTop, mb: c.marginBottom, pos: c.position, top: c.top,
    };
  };
  var out = { w: innerWidth, h: innerHeight, docH: document.documentElement.scrollHeight };
  out.h1 = st(document.querySelector('h1'));
  var ps = Array.from(document.querySelectorAll('main p, article p')).filter(function (p) { return p.textContent.trim().length > 120; });
  out.p = st(ps[0]);
  out.p2 = st(ps[3]);
  out.h2 = Array.from(document.querySelectorAll('main h2, article h2')).slice(0, 3).map(st);
  out.h3 = Array.from(document.querySelectorAll('main h3, article h3')).slice(0, 3).map(st);
  out.h4 = Array.from(document.querySelectorAll('main h4, article h4')).slice(0, 2).map(st);
  out.lists = Array.from(document.querySelectorAll('main ul li, article ul li')).slice(0, 2).map(st);
  out.imgs = Array.from(document.querySelectorAll('main img, article img, main figure, main video')).filter(function (i) { return i.getBoundingClientRect().width > 200; }).slice(0, 8).map(function (i) {
    var s = st(i), f = i.closest('figure');
    s.radius = getComputedStyle(i).borderRadius;
    s.caption = f && f.querySelector('figcaption') ? st(f.querySelector('figcaption')) : null;
    return s;
  });
  out.tables = Array.from(document.querySelectorAll('main table')).slice(0, 2).map(st);
  out.code = st(document.querySelector('main pre'));
  out.blockquote = st(document.querySelector('main blockquote'));
  // Contents list: links to in-page anchors outside the body column
  var anchors = Array.from(document.querySelectorAll('a[href^="#"]')).filter(function (a) { return a.textContent.trim().length > 3; });
  out.tocLinks = anchors.slice(0, 12).map(st);
  var tocBox = anchors[0] && (anchors[0].closest('nav, aside, ol, ul') || anchors[0].parentElement);
  out.tocBox = st(tocBox);
  if (tocBox) {
    var p = tocBox, chain = [];
    for (var i = 0; i < 6 && p; i++) { var c = getComputedStyle(p); chain.push(p.tagName + '.' + String(p.className).slice(0, 50) + ' pos=' + c.position + ' top=' + c.top + ' w=' + px(p.getBoundingClientRect().width) + ' disp=' + c.display); p = p.parentElement; }
    out.tocChain = chain;
  }
  out.meta = Array.from(document.querySelectorAll('time')).slice(0, 2).map(st);
  out.colors = { bg: getComputedStyle(document.body).backgroundColor, text: getComputedStyle(document.body).color };
  return JSON.stringify(out);
})()
