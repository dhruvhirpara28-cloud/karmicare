/* Fixture only, not for the theme. URL parameters:
   mode=day|night   sets body.day-mode / body.night-mode (the classes assets/day-night-mode.js sets)
   labels=site      eyebrows and buttons in the site's Nunito uppercase (decision D2)
   y=<px>           scrolls there once loaded (screenshots of one viewport at a time)
   noimage=1        drops the featured image, to show an article without one
   fluid=1          loads kc-fluid.css (the "Fluid type (preview)" setting)
   tokens=next      the global lane's coming token values (solid body/caption text, font order)
   soft=muted       secondary text on --kc-mapped-text-primary-default-muted (decision D23) */
(function () {
  var q = new URLSearchParams(location.search);
  var mode = q.get('mode') || 'day';
  document.body.classList.remove('day-mode', 'night-mode');
  document.body.classList.add(mode === 'night' ? 'night-mode' : 'day-mode');
  if (q.get('labels') === 'site') document.documentElement.setAttribute('data-kc-labels', 'site');
  // tokens=next: the global lane's kc-tokens.css change (not landed, 26 Oct;
  // docs/blog/NOTE-GLOBAL-TOKEN-CHANGES.md), copied from its diff: body and caption text solid,
  // proxima-nova first in the font stacks. soft=muted: secondary text on the solid, softer
  // --kc-mapped-text-primary-default-muted (decision D23).
  var css = '';
  if (q.get('tokens') === 'next') {
    css += ':root{--kc-font-role-backbone:"proxima-nova","Proxima Nova",sans-serif;' +
      '--kc-font-use-heading:"proxima-nova","Proxima Nova",sans-serif;' +
      '--kc-font-use-body:"proxima-nova","Proxima Nova",sans-serif;' +
      '--kc-font-use-ui:"proxima-nova","Proxima Nova",sans-serif}' +
      ':root,body.day-mode{--kc-mapped-text-default-body:#191f38;--kc-mapped-text-default-body-rgb:25,31,56;' +
      '--kc-mapped-text-default-caption:#191f38;--kc-mapped-text-default-caption-rgb:25,31,56}' +
      'body.night-mode{--kc-mapped-text-default-body:#fffbf6;--kc-mapped-text-default-body-rgb:255,251,246;' +
      '--kc-mapped-text-default-caption:#fffbf6;--kc-mapped-text-default-caption-rgb:255,251,246}';
  }
  if (q.get('soft') === 'muted') css += '.kc-blog{--kc-blog-soft-text:var(--kc-mapped-text-primary-default-muted)}';
  if (css) {
    var st = document.createElement('style');
    st.setAttribute('data-fixture-tokens', '');
    st.textContent = css;
    document.head.appendChild(st);
  }
  if (q.get('noimage')) {
    document.querySelectorAll('[data-kc-featured]').forEach(function (el) {
      el.remove();
    });
  }
  if (q.get('fluid')) {
    var l = document.createElement('link');
    l.rel = 'stylesheet';
    l.href = '/assets/kc-fluid.css';
    document.head.appendChild(l);
  }
  // Fixture links keep the parameters
  document.querySelectorAll('a[data-fixture-link]').forEach(function (a) {
    var u = new URL(a.href, location.href);
    ['mode', 'labels', 'fluid', 'tokens', 'soft'].forEach(function (k) {
      if (q.get(k)) u.searchParams.set(k, q.get(k));
    });
    a.href = u.pathname + u.search;
  });
  // y=<px> or at=<css selector> (lands 96px under the floating bar); re-applied after a resize,
  // because the screenshot tool sets the viewport after the page has loaded
  var y = parseInt(q.get('y') || '0', 10);
  var at = q.get('at');
  function place() {
    document.documentElement.style.scrollBehavior = 'auto';
    if (at) {
      var el = document.querySelector(at);
      if (el) window.scrollTo(0, el.getBoundingClientRect().top + window.scrollY - 96);
    } else if (y) {
      window.scrollTo(0, y);
    }
  }
  if (y || at) {
    window.addEventListener('load', place);
    window.addEventListener('resize', place);
  }
})();
