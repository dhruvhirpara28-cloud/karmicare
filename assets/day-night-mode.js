(function () {
  'use strict';

  var sun = window.KCDayNight;
  if (!sun) return;
  var manualMode = null;
  var timer;
  var explicit = '.kc_day, .kc_night';

  function applyMode(mode) {
    document.body.classList.remove('day-mode', 'night-mode');
    document.body.classList.add(mode + '-mode');
    document.querySelectorAll(explicit).forEach(function (button) {
      var selected = button.classList.contains(mode === 'day' ? 'kc_day' : 'kc_night');
      button.classList.toggle('active', selected);
      button.setAttribute('aria-pressed', String(selected));
    });
  }

  // The theme switch (Victor, 24 Oct, "sun out of the toggle"): on a click the new theme grows
  // as a circle from the centre of the pressed toggle in 0.7s (Awake rises like a sunrise, Asleep
  // settles like dusk), while the hero time rolls to 07:00 or 22:00. The sun's own switch, also
  // when it is noticed on return to the tab, crossfades in 1s; reduced motion crossfades in 0.3s.
  // It is a View Transition of the whole page, so nothing is added to the page: the old page is
  // a still snapshot under the live new one, and clicks pass through to the page. While it runs
  // the site's own colour transitions are off, so nothing fades twice; the time roll keeps its
  // own. A new switch skips a running one to its end. Without the API the theme changes as before.
  var styles = [
    '::view-transition { pointer-events: none; }',
    'html.kc-theme-switching *:not(.kc-roll__strip), html.kc-theme-switching *::before, html.kc-theme-switching *::after { transition: none !important; }',
    'html.kc-vt-circle::view-transition-old(root), html.kc-vt-circle::view-transition-new(root) { animation: none; mix-blend-mode: normal; }',
    'html.kc-vt-slow::view-transition-old(root), html.kc-vt-slow::view-transition-new(root) { animation-duration: 1s; }',
    'html.kc-vt-short::view-transition-old(root), html.kc-vt-short::view-transition-new(root) { animation-duration: 0.3s; }',
  ];
  var canTransition = false;
  if (document.startViewTransition && 'adoptedStyleSheets' in document) {
    try {
      var sheet = new CSSStyleSheet();
      styles.forEach(function (rule) {
        try {
          sheet.insertRule(rule, sheet.cssRules.length);
        } catch (error) {
          // A browser without one of these selectors keeps the others
        }
      });
      document.adoptedStyleSheets = document.adoptedStyleSheets.concat(sheet);
      canTransition = true;
    } catch (error) {
      canTransition = false;
    }
  }
  var reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  var root = document.documentElement;
  var shown = null; // the mode on the page
  var generation = 0;

  // origin: the pressed toggle, 'sun' for a switch without a click, null for none (first paint,
  // leaving the page)
  function show(mode, origin) {
    var change = shown !== null && mode !== shown;
    shown = mode;
    if (!change || !origin || !canTransition || document.hidden) {
      applyMode(mode);
      return;
    }
    var circle = origin !== 'sun' && !reducedMotion.matches;
    var kind = circle ? 'kc-vt-circle' : origin === 'sun' && !reducedMotion.matches ? 'kc-vt-slow' : 'kc-vt-short';
    var token = (generation += 1);
    root.classList.remove('kc-vt-circle', 'kc-vt-slow', 'kc-vt-short');
    root.classList.add(kind);
    var transition = document.startViewTransition(function () {
      root.classList.add('kc-theme-switching');
      applyMode(mode);
    });
    function done() {
      if (token !== generation) return;
      root.classList.remove('kc-theme-switching', kind);
    }
    transition.finished.then(done, done);
    transition.ready.then(
      function () {
        if (!circle) return;
        var box = origin.getBoundingClientRect();
        var x = box.left + box.width / 2;
        var y = box.top + box.height / 2;
        var radius = Math.hypot(Math.max(x, window.innerWidth - x), Math.max(y, window.innerHeight - y));
        root.animate(
          { clipPath: ['circle(0px at ' + x + 'px ' + y + 'px)', 'circle(' + radius + 'px at ' + x + 'px ' + y + 'px)'] },
          {
            duration: 700,
            easing: mode === 'day' ? 'cubic-bezier(0.22, 1, 0.36, 1)' : 'cubic-bezier(0.65, 0, 0.35, 1)',
            pseudoElement: '::view-transition-new(root)',
          }
        );
      },
      function () {
        // Skipped by a newer switch, or a hidden tab: the theme is already applied
      }
    );
  }

  function refresh(origin) {
    clearTimeout(timer);
    if (manualMode) {
      show(manualMode, origin);
      return;
    }
    var automatic = sun.state();
    show(automatic.mode, origin);
    if (!document.hidden) {
      timer = setTimeout(function () {
        refresh('sun');
      }, Math.max(100, automatic.nextChange - Date.now() + 50));
    }
  }
  function refreshBySun() {
    refresh('sun');
  }

  document.addEventListener('click', function (event) {
    if (!event.target || !event.target.closest) return;
    var control = event.target.closest(explicit);
    if (!control || control.matches(':disabled, [aria-disabled="true"]')) return;
    event.preventDefault();
    manualMode = control.classList.contains('kc_day') ? 'day' : 'night';
    refresh(control);
  });

  document.addEventListener('visibilitychange', function () {
    if (document.hidden) clearTimeout(timer);
    else refresh('sun');
  });
  window.addEventListener('focus', refreshBySun);
  window.addEventListener('pagehide', function () {
    manualMode = null;
    clearTimeout(timer);
    show(sun.state().mode, null);
  });
  window.addEventListener('pageshow', function (event) {
    if (event.persisted) manualMode = null;
    refresh(event.persisted ? null : 'sun');
  });
  document.addEventListener('shopify:section:load', refreshBySun);
  refresh(null);
})();
