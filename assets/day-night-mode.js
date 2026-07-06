/**
 * KARMICARE Day/Night Mode — WEBFLOW CUSTOM CODE
 * ─────────────────────────────────────────────────────────────────────────────
 * WHERE TO PASTE THIS:
 *   Webflow → Site Settings → Custom Code → Footer Code  (before </body>)
 *   OR: Webflow → Page Settings → Before </body> tag
 *
 * HOW IT WORKS:
 *   1. On load: detects visitor timezone via IP → gets local sunrise/sunset
 *      → auto-sets Day or Night mode.
 *   2. Manual toggle: clicking the sun/moon pill always works immediately.
 *   3. Cross-tab sync: mode syncs across all open browser tabs.
 *   4. New session (15 min gap): resets manual override → re-detects from geo.
 *
 * WHAT IT CONTROLS:
 *   - Adds `day-mode` or `night-mode` class to <body>
 *   - Syncs all `.day-mode` / `.night-mode` Webflow elements to match body
 *   - Toggle pill slides correctly (sun/moon position)
 * ─────────────────────────────────────────────────────────────────────────────
 */

(function () {
  'use strict';

  var BODY = document.body;
  var SESSION_TIMEOUT_MS = 15 * 60 * 1000; // 15 minutes

  /* ══════════════════════════════════════════════════════════════════════════
     CORE: Apply a mode to the entire page
     ══════════════════════════════════════════════════════════════════════════ */
  function applyMode(mode) {
    if (!mode || (mode !== 'day' && mode !== 'night')) return;

    // 1. Apply to <body>
    BODY.classList.remove('day-mode', 'night-mode');
    BODY.classList.add(mode + '-mode');

    // 2. Sync ALL Webflow elements that carry day-mode / night-mode class
    document.querySelectorAll('.day-mode, .night-mode').forEach(function (el) {
      el.classList.remove('day-mode', 'night-mode');
      el.classList.add(mode + '-mode');
    });

    // 3. Active states for explicit kc_day / kc_night buttons (if any)
    var dayBtn = document.querySelector('.kc_day');
    var nightBtn = document.querySelector('.kc_night');
    if (dayBtn) dayBtn.classList.toggle('active', mode === 'day');
    if (nightBtn) nightBtn.classList.toggle('active', mode === 'night');

    // 4. Persist to localStorage
    localStorage.setItem('theme', mode);
  }

  /* ══════════════════════════════════════════════════════════════════════════
     AUTO-DETECT: Sunrise / Sunset from visitor's real location
     ══════════════════════════════════════════════════════════════════════════ */
  function applyFallbackMode() {
    // Hour-based fallback if APIs are unavailable
    var h = new Date().getHours();
    applyMode((h >= 18 || h < 6) ? 'night' : 'day');
  }

  function applyFromSunTimes(sunriseStr, sunsetStr) {
    try {
      var tz = Intl.DateTimeFormat().resolvedOptions().timeZone;
      var sunrise = new Date(new Date(sunriseStr).toLocaleString('en-US', { timeZone: tz }));
      var sunset  = new Date(new Date(sunsetStr).toLocaleString('en-US',  { timeZone: tz }));
      var now     = new Date();

      if (isNaN(sunrise.getTime()) || isNaN(sunset.getTime())) {
        applyFallbackMode();
        return;
      }

      applyMode((now >= sunrise && now < sunset) ? 'day' : 'night');
    } catch (e) {
      applyFallbackMode();
    }
  }

  function fetchSunTimes(lat, lon) {
    fetch('https://api.sunrisesunset.io/json?lat=' + lat + '&lng=' + lon + '&formatted=0')
      .then(function (r) { return r.json(); })
      .then(function (data) {
        if (data && data.results && data.results.sunrise && data.results.sunset) {
          applyFromSunTimes(
            data.results.date + ' ' + data.results.sunrise,
            data.results.date + ' ' + data.results.sunset
          );
        } else {
          applyFallbackMode();
        }
      })
      .catch(applyFallbackMode);
  }

  function fetchIPLocation() {
    fetch('https://ipinfo.io/json')
      .then(function (r) { return r.json(); })
      .then(function (data) {
        if (data && data.loc) {
          var parts = data.loc.split(',');
          fetchSunTimes(parts[0], parts[1]);
        } else {
          applyFallbackMode();
        }
      })
      .catch(applyFallbackMode);
  }

  /* ══════════════════════════════════════════════════════════════════════════
     SESSION LOGIC
     ══════════════════════════════════════════════════════════════════════════ */
  function isNewSession() {
    var last = localStorage.getItem('lastVisit');
    if (!last) return true;
    return (Date.now() - parseInt(last, 10)) > SESSION_TIMEOUT_MS;
  }

  function initMode() {
    var newSession = isNewSession();
    localStorage.setItem('lastVisit', Date.now().toString());

    if (newSession) {
      // New session → ignore manual override, re-detect from location
      localStorage.removeItem('manualTheme');
      fetchIPLocation();
    } else {
      var manual = localStorage.getItem('manualTheme');
      if (manual) {
        applyMode(manual);
      } else {
        var stored = localStorage.getItem('theme');
        stored ? applyMode(stored) : fetchIPLocation();
      }
    }
  }

  /* ══════════════════════════════════════════════════════════════════════════
     TOGGLE WIRING — event delegation so Webflow async rendering doesn't matter
     ══════════════════════════════════════════════════════════════════════════ */
  function setManualMode(mode) {
    applyMode(mode);
    localStorage.setItem('manualTheme', mode);
    localStorage.setItem('themeChange', mode); // signal other tabs
  }

  // Single delegated listener covers ALL toggle buttons on the page
  document.addEventListener('click', function (e) {
    // Check if click is on or inside a toggle button or its wrapper
    if (
      e.target.closest('.toggle-button') ||
      e.target.closest('.menu-toggle-btn') ||
      e.target.closest('.kc-day-night-toggle')
    ) {
      var current = BODY.classList.contains('day-mode') ? 'day' : 'night';
      setManualMode(current === 'day' ? 'night' : 'day');
      return;
    }
    // Explicit day/night buttons
    if (e.target.closest('.kc_day'))   { setManualMode('day');   return; }
    if (e.target.closest('.kc_night')) { setManualMode('night'); return; }
  });

  // Keyboard support: Enter / Space on the toggle button
  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Enter' && e.key !== ' ') return;
    var btn = e.target.closest('.toggle-button, .kc-day-night-toggle');
    if (!btn) return;
    e.preventDefault();
    var current = BODY.classList.contains('day-mode') ? 'day' : 'night';
    setManualMode(current === 'day' ? 'night' : 'day');
  });

  /* ══════════════════════════════════════════════════════════════════════════
     CROSS-TAB SYNC
     ══════════════════════════════════════════════════════════════════════════ */
  window.addEventListener('storage', function (e) {
    if (e.key === 'themeChange' && e.newValue) {
      applyMode(e.newValue);
    }
  });

  /* ══════════════════════════════════════════════════════════════════════════
     FLASH PREVENTION — runs immediately before DOM is fully ready
     ══════════════════════════════════════════════════════════════════════════ */
  (function earlyApply() {
    var early = localStorage.getItem('manualTheme') || localStorage.getItem('theme');
    if (early === 'day' || early === 'night') {
      BODY.classList.remove('day-mode', 'night-mode');
      BODY.classList.add(early + '-mode');
    } else {
      // Best guess to prevent flash before API responds
      var h = new Date().getHours();
      BODY.classList.add((h >= 18 || h < 6) ? 'night-mode' : 'day-mode');
    }
  })();

  /* ══════════════════════════════════════════════════════════════════════════
     BOOT
     ══════════════════════════════════════════════════════════════════════════ */
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initMode);
  } else {
    initMode();
  }

  // After full page load, re-sync Webflow element classes
  // (Webflow renders its components after DOMContentLoaded)
  window.addEventListener('load', function () {
    var current = BODY.classList.contains('day-mode') ? 'day' : 'night';
    applyMode(current);
  });

})();
