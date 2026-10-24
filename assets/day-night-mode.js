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

  // The theme switch (Victor, 24 Oct, "soft sun glow"): a click changes the theme at once, so the
  // hero time rolls to 07:00 or 22:00 and the video starts again with it, while a soft see-through
  // glow grows as a circle from the centre of the pressed toggle and fades (Awake: warm light, like
  // a sunrise; Asleep: a soft indigo dusk); the page stays readable beneath it. The sun's own
  // switch, also when it is noticed on return to the tab, changes at once too, with the same glow
  // from the top centre of the screen, where the sun would be. Reduced motion changes at once
  // without a glow. Text and its background always change together, never through a blend of the
  // two (R54c B1: a crossfade made the hero text unreadable halfway). The glow is a fixed layer
  // without pointer events, so every click and key reaches the page and focus stays where it is
  // (R54 B1), and it sets its own display, as Dawn hides empty divs (R54b B1).
  // Quick clicks are merged (R54b N2, WCAG 2.3.1): the theme changes at most once every 0.4s, so
  // never more than three times in a second, the last request wins, and one glow runs at a time;
  // a switch during a glow lets it run out. While the theme changes the site's own colour
  // transitions are off, so nothing fades twice; the time roll and the hero video keep their own.
  // Without Web Animations the theme changes as before.
  var gap = 400;
  var own = ':not(.kc-roll__strip):not(.kc-hero-animation__mode)';
  try {
    var sheet = new CSSStyleSheet();
    sheet.replaceSync(
      'html.kc-theme-switching *' + own + ', html.kc-theme-switching *::before, html.kc-theme-switching *::after { transition: none !important; }'
    );
    document.adoptedStyleSheets = document.adoptedStyleSheets.concat(sheet);
  } catch (error) {
    // Without constructed stylesheets the site's own colour transitions run
  }
  var root = document.documentElement;
  var canAnimate = typeof root.animate === 'function';
  var reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  // Each mode's glow in brand colours: a core at its origin, a halo halfway out, nothing at the
  // edge. Awake: the warm off-white at 35% with a faint light-blue sky; Asleep: the light blue at
  // 20%. The layer fades in to that and out again, so the page's luminance under the glow moves
  // by less than 0.1 (no flash in WCAG terms).
  var sky = 'var(--kc-brand-original-light-blue-accent-rgb)';
  var glows = {
    day: 'rgba(var(--kc-brand-original-off-white-rgb), 0.35), rgba(' + sky + ', 0.08) 45%, rgba(' + sky + ', 0)',
    night: 'rgba(' + sky + ', 0.2), rgba(' + sky + ', 0.07) 45%, rgba(' + sky + ', 0)',
  };
  var shown = null; // the mode on the page
  var pending = null; // a request that waits for the gap: { mode, origin }
  var pendingTimer;
  var lastSwitch = -Infinity;
  var glow = null; // the running glow: { layer, animations }
  var generation = 0; // a callback of an older switch changes nothing (R54 N1)

  function removeGlow(running) {
    running.animations.forEach(function (animation) {
      animation.cancel();
    });
    running.layer.remove();
    if (glow === running) glow = null;
  }

  // origin: the pressed toggle, or 'sun' for the top centre of the screen
  function glowFrom(origin, mode) {
    if (glow) return;
    var x = window.innerWidth / 2;
    var y = 0;
    if (origin !== 'sun') {
      if (!origin.isConnected) return;
      var box = origin.getBoundingClientRect();
      x = box.left + box.width / 2;
      y = box.top + box.height / 2;
    }
    var radius = Math.hypot(Math.max(x, window.innerWidth - x), Math.max(y, window.innerHeight - y));
    var layer = document.createElement('div');
    layer.className = 'kc-theme-glow';
    layer.setAttribute('aria-hidden', 'true');
    layer.style.cssText = 'display:block;position:fixed;inset:0;overflow:hidden;z-index:2147483647;pointer-events:none;';
    var circle = document.createElement('div');
    circle.style.cssText =
      'display:block;position:absolute;border-radius:50%;opacity:0;' +
      'left:' + (x - radius) + 'px;top:' + (y - radius) + 'px;width:' + 2 * radius + 'px;height:' + 2 * radius + 'px;' +
      'background:radial-gradient(closest-side, ' + glows[mode] + ');';
    layer.append(circle);
    document.body.append(layer);
    var running = {
      layer: layer,
      animations: [
        circle.animate(
          { transform: ['scale(0.08)', 'scale(1)'] },
          { duration: 850, easing: mode === 'day' ? 'cubic-bezier(0.22, 1, 0.36, 1)' : 'cubic-bezier(0.65, 0, 0.35, 1)', fill: 'forwards' }
        ),
        circle.animate([{ opacity: 0 }, { opacity: 1, offset: 0.25 }, { opacity: 0 }], { duration: 850, fill: 'forwards' }),
      ],
    };
    glow = running;
    running.animations[1].finished.then(
      function () {
        removeGlow(running);
      },
      function () {
        removeGlow(running);
      }
    );
  }

  // Ends whatever is on its way: a waiting request, the glow
  function settle() {
    generation += 1;
    clearTimeout(pendingTimer);
    pending = null;
    root.classList.remove('kc-theme-switching');
    if (glow) removeGlow(glow);
  }

  function switchTo(mode, origin) {
    generation += 1;
    lastSwitch = Date.now();
    root.classList.add('kc-theme-switching');
    applyMode(mode);
    shown = mode;
    // The new colours are in place before the transitions come back, so none of them runs
    void document.body.offsetWidth;
    root.classList.remove('kc-theme-switching');
    if (!reducedMotion.matches) glowFrom(origin, mode);
  }

  // origin: the pressed toggle, 'sun' for a switch without a click, null for none (first paint,
  // leaving the page, a hidden tab)
  function show(mode, origin) {
    if (shown === null || !origin || !canAnimate || document.hidden) {
      settle();
      applyMode(mode);
      shown = mode;
      return;
    }
    if (pending && pending.mode === mode) return; // already on its way
    clearTimeout(pendingTimer);
    pending = null;
    if (mode === shown) return; // back to the mode on the page before the wait was over
    var wait = lastSwitch + gap - Date.now();
    if (wait <= 0) {
      switchTo(mode, origin);
      return;
    }
    var token = generation;
    pending = { mode: mode, origin: origin };
    pendingTimer = setTimeout(function () {
      if (token !== generation || !pending) return;
      var request = pending;
      pending = null;
      switchTo(request.mode, request.origin);
    }, wait);
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
      if (shown !== null) show(pending ? pending.mode : shown, null);
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
