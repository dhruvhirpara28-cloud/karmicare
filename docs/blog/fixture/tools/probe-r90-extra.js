location.protocol.indexOf('http') !== 0 ? 'BLANK' : (function () {
  // R90 N1 and N2 on a theme render. N1: a legacy 560x315 iframe and an 80x40 picture added to the
  // body in memory. N2: activate the third contents link and see where focus goes.
  var r = Math.round;
  var body = document.querySelector('.kc-blog__body');
  var p1 = document.createElement('p');
  p1.innerHTML = '<iframe width="560" height="315" title="test" src="about:blank"></iframe>';
  var p2 = document.createElement('p');
  p2.innerHTML = '<img width="80" height="40" alt="" src="data:image/gif;base64,R0lGODlhAQABAAAAACw=">';
  body.insertBefore(p1, body.children[3]);
  body.insertBefore(p2, body.children[4]);
  var main = document.querySelector('.kc-blog__main').getBoundingClientRect();
  var f = p1.querySelector('iframe').getBoundingClientRect();
  var s = p2.querySelector('img').getBoundingClientRect();
  var out = {
    w: innerWidth,
    iframe: [r(f.left), r(f.right), r(f.width), r(f.height)],
    iframeInside: f.left >= main.left - 0.5 && f.right <= main.right + 0.5,
    smallImg: [r(s.width), r(s.height)],
  };
  p1.remove();
  p2.remove();
  var links = document.querySelectorAll('.kc-blog-toc__link');
  if (links[2]) {
    links[2].click();
    var a = document.activeElement;
    out.focusAfterJump = a.tagName + ' "' + a.textContent.trim().slice(0, 30) + '" tabindex=' + a.getAttribute('tabindex');
    out.hash = location.hash;
  }
  return JSON.stringify(out);
})()
