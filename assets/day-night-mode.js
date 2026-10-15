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

  function refresh() {
    clearTimeout(timer);
    if (manualMode) {
      applyMode(manualMode);
      return;
    }
    var automatic = sun.state();
    applyMode(automatic.mode);
    if (!document.hidden) {
      timer = setTimeout(refresh, Math.max(100, automatic.nextChange - Date.now() + 50));
    }
  }

  document.addEventListener('click', function (event) {
    if (!event.target || !event.target.closest) return;
    var control = event.target.closest(explicit);
    if (!control || control.matches(':disabled, [aria-disabled="true"]')) return;
    event.preventDefault();
    manualMode = control.classList.contains('kc_day') ? 'day' : 'night';
    refresh();
  });

  document.addEventListener('visibilitychange', function () {
    if (document.hidden) clearTimeout(timer);
    else refresh();
  });
  window.addEventListener('focus', refresh);
  window.addEventListener('pagehide', function () {
    manualMode = null;
    clearTimeout(timer);
    applyMode(sun.state().mode);
  });
  window.addEventListener('pageshow', function (event) {
    if (event.persisted) manualMode = null;
    refresh();
  });
  document.addEventListener('shopify:section:load', refresh);
  refresh();
})();
