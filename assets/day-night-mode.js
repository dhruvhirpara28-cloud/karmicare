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

  // The theme switch (Victor, 24 Oct, "sun out of the toggle"): on a click the new theme's colour
  // grows as a circle from the centre of the pressed toggle (Awake rises like a sunrise, Asleep
  // settles like dusk); once it covers the screen the theme changes beneath it, the hero time
  // rolls to 07:00 or 22:00, and the layer fades away. The sun's own switch, also when it is
  // noticed on return to the tab, dips through the new colour in 1s; reduced motion in 0.3s.
  // The layer is one fixed element without pointer events, so every click and key reaches the
  // page, and focus stays where it is (R54 B1: a root View Transition swallowed real clicks).
  // While the theme changes the site's own colour transitions are off, so nothing fades twice;
  // the time roll keeps its own. A new request replaces a running one, and the last one wins.
  // Without Web Animations the theme changes as before.
  try {
    var sheet = new CSSStyleSheet();
    sheet.replaceSync(
      'html.kc-theme-switching *:not(.kc-roll__strip), html.kc-theme-switching *::before, html.kc-theme-switching *::after { transition: none !important; }'
    );
    document.adoptedStyleSheets = document.adoptedStyleSheets.concat(sheet);
  } catch (error) {
    // Without constructed stylesheets the site's colour transitions run beneath the layer
  }
  var root = document.documentElement;
  var canAnimate = typeof root.animate === 'function';
  var reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  // Each mode's page colour and the glow at the circle's centre (brand colours, the same in
  // both modes, so the layer can show the new theme before the page has it)
  var colours = {
    day: {
      page: 'var(--kc-brand-original-off-white)',
      glow: 'color-mix(in srgb, var(--kc-brand-original-light-blue-accent) 20%, var(--kc-brand-original-off-white))',
    },
    night: { page: 'var(--kc-brand-original-dark-blue)', glow: 'var(--kc-brand-original-middle-blue-1)' },
  };
  var shown = null; // the mode on the page
  var effect = null; // the running switch: { layer, mode, switched }
  var generation = 0; // a callback of an older switch changes nothing (R54 N1)

  function fadeAway(layer, duration) {
    layer.animate({ opacity: [getComputedStyle(layer).opacity, 0] }, { duration: duration, fill: 'forwards' }).finished.then(
      function () {
        layer.remove();
      },
      function () {
        layer.remove();
      }
    );
  }

  // Stops a running switch: its layer fades in 0.15s and switches nothing more
  function cancel() {
    generation += 1;
    if (effect) {
      fadeAway(effect.layer, 150);
      effect = null;
    }
    root.classList.remove('kc-theme-switching');
  }

  function start(mode, origin) {
    var token = (generation += 1);
    var circle = origin !== 'sun' && !reducedMotion.matches;
    var dip = reducedMotion.matches ? 150 : 500;
    var layer = document.createElement('div');
    layer.className = 'kc-theme-sun';
    layer.setAttribute('aria-hidden', 'true');
    var style = layer.style;
    style.position = 'fixed';
    style.inset = '0';
    style.zIndex = '2147483647';
    style.pointerEvents = 'none';
    style.background = colours[mode].page;
    var cover;
    effect = { layer: layer, mode: mode, switched: false };
    if (circle) {
      var box = origin.getBoundingClientRect();
      var x = box.left + box.width / 2;
      var y = box.top + box.height / 2;
      var radius = Math.hypot(Math.max(x, window.innerWidth - x), Math.max(y, window.innerHeight - y));
      var at = ' at ' + x + 'px ' + y + 'px';
      style.backgroundImage = 'radial-gradient(circle' + at + ', ' + colours[mode].glow + ', ' + colours[mode].page + ' ' + radius * 0.6 + 'px)';
      style.clipPath = 'circle(0px' + at + ')';
      document.body.append(layer);
      cover = layer.animate(
        { clipPath: ['circle(0px' + at + ')', 'circle(' + radius + 'px' + at + ')'] },
        {
          duration: 500,
          easing: mode === 'day' ? 'cubic-bezier(0.22, 1, 0.36, 1)' : 'cubic-bezier(0.65, 0, 0.35, 1)',
          fill: 'forwards',
        }
      );
    } else {
      style.opacity = '0';
      document.body.append(layer);
      cover = layer.animate({ opacity: [0, 1] }, { duration: dip, easing: 'ease-in', fill: 'forwards' });
    }
    cover.finished.then(function () {
      if (token !== generation) return;
      root.classList.add('kc-theme-switching');
      applyMode(mode);
      shown = mode;
      effect.switched = true;
      layer
        .animate({ opacity: [1, 0] }, { duration: circle ? 350 : dip, easing: 'ease-out', fill: 'forwards' })
        .finished.then(function () {
          if (token !== generation) return;
          layer.remove();
          effect = null;
          root.classList.remove('kc-theme-switching');
        }, stopped);
    }, stopped);
    function stopped() {
      if (token === generation) cancel();
    }
  }

  // origin: the pressed toggle, 'sun' for a switch without a click, null for none (first paint,
  // leaving the page, a hidden tab)
  function show(mode, origin) {
    if (effect && origin && effect.mode === mode) return; // already on its way
    if (effect) cancel();
    if (shown === null || !origin || !canAnimate || document.hidden || mode === shown) {
      applyMode(mode);
      shown = mode;
      return;
    }
    start(mode, origin);
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
    if (document.hidden) {
      clearTimeout(timer);
      // A switch on its way finishes at once, out of sight
      if (effect) show(effect.mode, null);
    } else {
      refresh('sun');
    }
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
