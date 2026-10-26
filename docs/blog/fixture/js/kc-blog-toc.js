/* kc-blog-toc.js: the "On this page" list for Direction B (docs/blog/02-PROPOSAL.md).
   Reads the article's section headings (the highest level the body uses: h1 in the nano article,
   h2 elsewhere), gives each an id, and fills every [data-kc-blog-toc] list. The heading being
   read gets aria-current. Fewer than three sections: the list removes itself. No scrolling of its
   own: links are plain #fragments, so kc-navigation.css's scroll-margin and the reader's
   reduced-motion setting apply. */
(function () {
  var body = document.querySelector('.kc-blog__body');
  var tocs = document.querySelectorAll('[data-kc-blog-toc]');
  if (!body || !tocs.length) return;

  var level = ['h1', 'h2', 'h3'].find(function (tag) {
    return body.querySelector(tag);
  });
  var headings = level ? Array.prototype.slice.call(body.querySelectorAll(level)) : [];
  headings = headings.filter(function (h) {
    return h.textContent.trim();
  });

  if (headings.length < 3) {
    tocs.forEach(function (toc) {
      var box = toc.closest('[data-kc-blog-toc-box]');
      (box || toc).remove();
    });
    return;
  }

  var used = {};
  headings.forEach(function (h) {
    if (!h.id) {
      var base = h.textContent.trim().toLowerCase().replace(/[^\p{L}\p{N}]+/gu, '-').replace(/^-|-$/g, '').slice(0, 60) || 'section';
      var id = base;
      var n = 2;
      while (used[id] || document.getElementById(id)) id = base + '-' + n++;
      used[id] = true;
      h.id = id;
    }
  });

  var links = [];
  tocs.forEach(function (toc) {
    headings.forEach(function (h) {
      var li = document.createElement('li');
      var a = document.createElement('a');
      a.className = 'kc-blog-toc__link';
      a.href = '#' + h.id;
      a.textContent = h.textContent.trim();
      li.appendChild(a);
      toc.appendChild(li);
      links.push(a);
    });
  });

  function mark(id) {
    links.forEach(function (a) {
      if (a.getAttribute('href') === '#' + id) a.setAttribute('aria-current', 'true');
      else a.removeAttribute('aria-current');
    });
  }

  // The current section: the last heading above 30% of the viewport
  function update() {
    var line = window.innerHeight * 0.3;
    var current = headings[0];
    for (var i = 0; i < headings.length; i++) {
      if (headings[i].getBoundingClientRect().top <= line) current = headings[i];
    }
    mark(current.id);
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

  // The rail is open from 990px; the phone disclosure starts closed
  var wide = window.matchMedia('(min-width: 990px)');
  function sync() {
    document.querySelectorAll('.kc-blog-b__rail details.kc-blog-toc').forEach(function (d) {
      d.open = wide.matches;
    });
  }
  wide.addEventListener('change', sync);
  sync();
})();
