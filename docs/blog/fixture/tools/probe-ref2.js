location.protocol !== 'https:' ? 'BLANK' : (function () {
  var px = Math.round;
  // 1. The visible contents list: the element with that text that has a box, and its ancestors
  var all = Array.from(document.querySelectorAll('a, button, li, span, p'));
  var hits = all.filter(function (e) {
    var r = e.getBoundingClientRect();
    return e.textContent.trim() === 'A simplified primer on Azure Cosmos DB containers' && r.width > 0 && r.left < 400;
  });
  var toc = null;
  if (hits.length) {
    var e = hits[0], chain = [];
    for (var i = 0; i < 8 && e; i++) {
      var c = getComputedStyle(e), r = e.getBoundingClientRect();
      chain.push({ tag: e.tagName, cls: String(e.className).slice(0, 90), pos: c.position, top: c.top, x: px(r.left), y: px(r.top + scrollY), w: px(r.width), h: px(r.height), fs: c.fontSize, lh: c.lineHeight, color: c.color, gap: c.gap, pad: c.padding, border: c.borderLeft, opacity: c.opacity });
      e = e.parentElement;
    }
    toc = chain;
    var list = hits[0].closest('ul, ol, nav');
    toc.items = list ? Array.from(list.querySelectorAll('a, button')).slice(0, 14).map(function (a) {
      var c = getComputedStyle(a), r = a.getBoundingClientRect();
      return [a.textContent.trim().slice(0, 40), px(r.left), px(r.top), px(r.height), c.fontSize, c.lineHeight, c.color, c.paddingLeft, getComputedStyle(a.parentElement).paddingLeft];
    }) : null;
  }
  // 2. The body column's block rhythm: top-level blocks with their gaps
  var first = Array.from(document.querySelectorAll('main p')).filter(function (p) { return p.textContent.trim().length > 120; })[0];
  var col = first ? first.parentElement : null;
  for (var k = 0; k < 3 && col && col.children.length < 6; k++) col = col.parentElement;
  var rhythm = [];
  if (col) {
    var kids = Array.from(col.querySelectorAll('h2, h3, p, figure, ul, ol, blockquote, table, pre')).filter(function (n) { var r = n.getBoundingClientRect(); return r.width > 300; });
    var prev = null;
    kids.slice(0, 40).forEach(function (n) {
      var r = n.getBoundingClientRect();
      rhythm.push([n.tagName, (n.textContent || '').trim().slice(0, 30), px(r.left), px(r.width), px(r.top + scrollY), px(r.height), prev === null ? null : px(r.top + scrollY - prev)]);
      prev = r.bottom + scrollY;
    });
  }
  // 3. Figure parts: header text styles
  var fig = document.querySelector('main figure');
  var figParts = fig ? Array.from(fig.querySelectorAll('*')).filter(function (n) { return n.children.length === 0 && n.textContent.trim(); }).slice(0, 4).map(function (n) {
    var c = getComputedStyle(n);
    return [n.textContent.trim().slice(0, 40), c.fontSize, c.lineHeight, c.fontWeight, c.color, c.fontFamily.slice(0, 20), c.textTransform];
  }) : null;
  return JSON.stringify({ w: innerWidth, toc: toc, tocItems: toc && toc.items, rhythm: rhythm, figParts: figParts });
})()
