/* kc-blog-contents.js: Direction D's contents (docs/blog/02-PROPOSAL.md), after the reference.
   Reads the body's two highest heading levels (h1 + h2 in the nano article, h2 + h3 elsewhere),
   gives each an id and fills [data-kc-blog-contents] with sections and indented sub-sections, then
   the headings marked [data-kc-blog-toc-extra] (Sources). The heading being read gets
   aria-current, and the phone bar's label [data-kc-blog-toc-current] shows its text. From 1200px
   the <details> is open (the list in the left margin); below it the bar starts closed and closes
   again after a link is chosen. Fewer than three sections: the contents remove themselves. Links
   are plain #fragments: kc-navigation.css gives the headings their scroll margin, and no smooth
   scrolling is forced, so reduced motion is respected. */
(function () {
  var body = document.querySelector('.kc-blog__body');
  var box = document.querySelector('[data-kc-blog-contents-box]');
  var list = document.querySelector('[data-kc-blog-contents]');
  if (!body || !box || !list) return;

  var levels = ['h1', 'h2', 'h3', 'h4'].filter(function (tag) {
    return body.querySelector(tag);
  });
  var top = levels[0];
  var sub = levels[1];
  if (!top || body.querySelectorAll(top).length < 3) {
    box.remove();
    return;
  }

  var heads = Array.prototype.slice.call(body.querySelectorAll(sub ? top + ',' + sub : top)).filter(function (h) {
    return h.textContent.trim();
  });
  heads = heads.concat(Array.prototype.slice.call(document.querySelectorAll('[data-kc-blog-toc-extra]')));

  var used = {};
  heads.forEach(function (h) {
    if (h.id) return;
    var base = h.textContent.trim().toLowerCase().replace(/[^\p{L}\p{N}]+/gu, '-').replace(/^-|-$/g, '').slice(0, 60) || 'section';
    var id = base;
    var n = 2;
    while (used[id] || document.getElementById(id)) id = base + '-' + n++;
    used[id] = true;
    h.id = id;
  });

  var links = heads.map(function (h) {
    var li = document.createElement('li');
    li.className = 'kc-blog-d-toc__item' + (sub && h.matches(sub) && body.contains(h) ? ' kc-blog-d-toc__item--sub' : '');
    var a = document.createElement('a');
    a.className = 'kc-blog-d-toc__link';
    a.href = '#' + h.id;
    a.textContent = h.textContent.trim().replace(/:$/, '');
    li.appendChild(a);
    list.appendChild(li);
    return a;
  });

  var label = box.querySelector('[data-kc-blog-toc-current]');
  var details = box.querySelector('details');
  function update() {
    var line = window.innerHeight * 0.3;
    var current = 0;
    for (var i = 0; i < heads.length; i++) {
      if (heads[i].getBoundingClientRect().top <= line) current = i;
    }
    links.forEach(function (a, i) {
      if (i === current) a.setAttribute('aria-current', 'true');
      else a.removeAttribute('aria-current');
    });
    if (label) label.textContent = links[current].textContent;
  }
  var ticking = false;
  window.addEventListener('scroll', function () {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(function () {
      ticking = false;
      update();
    });
  }, { passive: true });
  update();

  var wide = window.matchMedia('(min-width: 1200px)');
  function sync() {
    if (details) details.open = wide.matches;
  }
  wide.addEventListener('change', sync);
  sync();
  list.addEventListener('click', function (e) {
    if (e.target.closest('a') && details && !wide.matches) details.open = false;
  });
})();
