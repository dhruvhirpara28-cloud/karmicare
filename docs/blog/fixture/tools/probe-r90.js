location.protocol.indexOf('http') !== 0 ? 'BLANK' : (function () {
  // R90 checks on a theme render: B1 picture edges, B2 reserved height before load, B3 headings,
  // the contents list, and the page width (no sideways scroll).
  var r = Math.round;
  var vw = document.documentElement.clientWidth;
  var imgs = Array.prototype.slice.call(document.querySelectorAll('.kc-blog__body p img'));
  var main = document.querySelector('.kc-blog__main');
  return JSON.stringify({
    w: innerWidth,
    clientWidth: vw,
    scrollWidth: document.documentElement.scrollWidth,
    h1: document.querySelectorAll('h1').length,
    bodyHeadings: Array.prototype.map.call(document.querySelectorAll('.kc-blog__body :is(h1,h2,h3,h4,h5,h6)'), function (h) { return h.tagName; }).join(''),
    toc: Array.prototype.map.call(document.querySelectorAll('.kc-blog-toc__link'), function (a) { return a.textContent.slice(0, 18); }),
    imgs: imgs.map(function (i) {
      var b = i.getBoundingClientRect(), p = i.parentElement.closest('p').getBoundingClientRect();
      var m = main.getBoundingClientRect();
      var clipped = b.left < m.left - 0.5 || b.right > m.right + 0.5;
      return { left: r(b.left), right: r(b.right), w: r(b.width), h: r(b.height), pLeft: r(p.left), pRight: r(p.right), attrs: i.getAttribute('width') + 'x' + i.getAttribute('height'), complete: i.complete && i.naturalWidth > 0, clipped: clipped };
    }),
  });
})()
