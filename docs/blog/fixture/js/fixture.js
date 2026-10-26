/* Fixture only, not for the theme. URL parameters:
   mode=day|night   sets body.day-mode / body.night-mode (the classes assets/day-night-mode.js sets)
   labels=site      eyebrows and buttons in the site's Nunito uppercase (decision D2)
   y=<px>           scrolls there once loaded (screenshots of one viewport at a time)
   noimage=1        drops the featured image, to show an article without one
   fluid=1          loads kc-fluid.css (the "Fluid type (preview)" setting) */
(function () {
  var q = new URLSearchParams(location.search);
  var mode = q.get('mode') || 'day';
  document.body.classList.remove('day-mode', 'night-mode');
  document.body.classList.add(mode === 'night' ? 'night-mode' : 'day-mode');
  if (q.get('labels') === 'site') document.documentElement.setAttribute('data-kc-labels', 'site');
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
    ['mode', 'labels', 'fluid'].forEach(function (k) {
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
