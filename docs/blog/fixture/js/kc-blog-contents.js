/* kc-blog-contents.js: Direction D's contents (docs/blog/02-PROPOSAL.md), the legal pages' menu.
   Reads the body's section headings (the highest level it uses: h1 in the nano article, h2
   elsewhere), gives each an id and fills [data-kc-blog-contents] with one link per section, then
   the headings marked [data-kc-blog-toc-extra] (Sources). The link of the section being read gets
   aria-current (full colour and the 2px rule, as on the legal pages). While a wide body picture
   passes the sticky sidebar, the sidebar gets .is-covered and fades out, as on the reference.
   Fewer than three sections: the contents remove themselves. A click eases to the section as on
   the legal pages (smooth scroll, a jump with reduced motion, #fragment in the address bar). */
(function () {
  var body = document.querySelector('.kc-blog__body');
  var box = document.querySelector('[data-kc-blog-contents-box]');
  var list = document.querySelector('[data-kc-blog-contents]');
  if (!body || !box || !list) return;

  var level = ['h1', 'h2', 'h3', 'h4'].find(function (tag) {
    return body.querySelector(tag);
  });
  var heads = level ? Array.prototype.slice.call(body.querySelectorAll(level)).filter(function (h) {
    return h.textContent.trim();
  }) : [];
  if (heads.length < 3) {
    box.remove();
    return;
  }
  heads = heads.concat(Array.prototype.slice.call(document.querySelectorAll('[data-kc-blog-toc-extra]')));

  var used = {};
  var links = heads.map(function (h) {
    if (!h.id) {
      var base = h.textContent.trim().toLowerCase().replace(/[^\p{L}\p{N}]+/gu, '-').replace(/^-|-$/g, '').slice(0, 60) || 'section';
      var id = base;
      var n = 2;
      while (used[id] || document.getElementById(id)) id = base + '-' + n++;
      used[id] = true;
      h.id = id;
    }
    var li = document.createElement('li');
    var a = document.createElement('a');
    a.className = 'kc-blog-d-toc__link subtitle-item opacity-xl';
    a.href = '#' + h.id;
    a.textContent = h.textContent.trim().replace(/:$/, '');
    li.appendChild(a);
    list.appendChild(li);
    return a;
  });

  var wide = Array.prototype.slice.call(body.querySelectorAll('p')).filter(function (p) {
    return p.querySelector('img');
  });
  var sticky = window.matchMedia('(min-width: 641px)');

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
    var covered = false;
    if (sticky.matches) {
      var r = box.getBoundingClientRect();
      covered = wide.some(function (p) {
        var w = p.getBoundingClientRect();
        return w.top < r.bottom && w.bottom > r.top;
      });
    }
    box.classList.toggle('is-covered', covered);
  }

  // A click scrolls as on the legal pages (legal-toc-section.liquid): the link is marked at once,
  // the page eases there with the browser's smooth scroll (a jump with reduced motion), and the
  // #fragment goes into the address bar. The landing line is the scroll margin kc-navigation.css
  // gives headings with an id: under the floating bar with 16px to spare (resolved in px).
  // The body pictures have no width and height in the article HTML (02-PROPOSAL D7), so pictures
  // that load during the scroll push the heading down. When the scroll ends (scrollend, or 1s for
  // browsers without it) the heading is checked and aimed at again, at most three times.
  function aim(target, tries) {
    var margin = parseFloat(getComputedStyle(target).scrollMarginTop) || 0;
    var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    window.scrollTo({ top: target.getBoundingClientRect().top + window.scrollY - margin, behavior: reduce ? 'auto' : 'smooth' });
    if (tries >= 3) return;
    var done = false;
    function check() {
      if (done) return;
      done = true;
      window.removeEventListener('scrollend', check);
      if (Math.abs(target.getBoundingClientRect().top - margin) > 2) aim(target, tries + 1);
    }
    window.addEventListener('scrollend', check);
    if (!('onscrollend' in window)) setTimeout(check, 1000);
  }

  links.forEach(function (a, i) {
    a.addEventListener('click', function (e) {
      var target = heads[i];
      if (!target) return;
      e.preventDefault();
      links.forEach(function (l) {
        if (l === a) l.setAttribute('aria-current', 'true');
        else l.removeAttribute('aria-current');
      });
      aim(target, 0);
      if (history.pushState) history.pushState(null, '', '#' + target.id);
    });
  });

  var ticking = false;
  function onScroll() {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(function () {
      ticking = false;
      update();
    });
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll);
  update();
})();
