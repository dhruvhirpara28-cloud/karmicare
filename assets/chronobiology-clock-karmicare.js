/**
 * Karmicare Chronobiology 24-Hour Clock
 * Interactive circular slider and real-time biological rhythm visualizer
 */
(() => {
  'use strict';

  // The seven windows of the specification, start-inclusive/end-exclusive (in minutes from midnight),
  // with the final window wrapping midnight. Each message is the section's data-window-N (locale keys).
  const windows = [
    [300, 480, 1],
    [480, 660, 2],
    [660, 840, 3],
    [840, 1020, 4],
    [1020, 1200, 5],
    [1200, 1380, 6],
    [1380, 1740, 7]
  ];

  function initClock(sectionEl) {
    if (!sectionEl || sectionEl._chronoInit) return;
    sectionEl._chronoInit = true;

    const knob = sectionEl.querySelector('.knob');
    const orbit = sectionEl.querySelector('.orbit');
    const readout = sectionEl.querySelector('.readout');
    const timeOut = sectionEl.querySelector('.clock-time');
    const copyOut = sectionEl.querySelector('.clock-copy');
    const caption = sectionEl.querySelector('.clock-caption');
    const hint = sectionEl.querySelector('.hint');

    if (!knob || !orbit || !readout || !timeOut || !copyOut || !caption) return;

    // Theme synchronization with site-wide Day / Night mode
    function syncTheme(mode) {
      if (!mode) mode = document.body.classList.contains('night-mode') ? 'night' : 'day';
      sectionEl.dataset.theme = mode;
    }

    syncTheme();

    // Watch for global site theme toggle on <body>
    const bodyObserver = new MutationObserver(() => {
      const isNight = document.body.classList.contains('night-mode');
      syncTheme(isNight ? 'night' : 'day');
    });
    bodyObserver.observe(document.body, { attributes: true, attributeFilter: ['class'] });

    // Until the visitor first takes the knob (once per visit), the knob waits two hours early and
    // runs to the current time when the dial comes into view; then its halo pulses (.is-inviting)
    // until the knob is taken (Victor, 26 Oct)
    const exploredKey = 'kc-clock-explored';
    let explored = false;
    try { explored = sessionStorage.getItem(exploredKey) === '1'; } catch (_) { }

    function markExplored() {
      if (explored) return;
      explored = true;
      sectionEl.classList.remove('is-inviting');
      try { sessionStorage.setItem(exploredKey, '1'); } catch (_) { }
    }

    let pointerId = null;
    let heldKey = null;
    let selected = 0;
    let displayedMinutes = 0;
    let returnFrame = null;
    let timer = null;

    const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');
    const previewOffset = -120;
    let previewPending = false;
    let previewObserver = null;

    const normalize = minutes => ((minutes % 1440) + 1440) % 1440;
    const format = minutes => String(Math.floor(minutes / 60)).padStart(2, '0') + ':' + String(minutes % 60).padStart(2, '0');
    const minutesNow = (now = new Date()) => now.getHours() * 60 + now.getMinutes();
    const angleFor = minutes => ((((minutes / 60) + 12) % 24) / 24) * 360;

    function positionKnob(minutes) {
      displayedMinutes = normalize(minutes);
      const angle = angleFor(displayedMinutes);
      const radians = angle * Math.PI / 180;
      // Percentage positioning preserves the exact 178/604 radius at any viewport width
      knob.style.left = (50 + (178 / 604) * 100 * Math.sin(radians)) + '%';
      knob.style.top = (50 - (178 / 604) * 100 * Math.cos(radians)) + '%';
      knob.dataset.angle = String(angle);
    }

    function draw(minutes, preview = false) {
      positionKnob(minutes);
      selected = normalize(Math.round(minutes));
      const time = format(selected);
      const awake = selected >= 400 && selected < 1320;
      const windowEntry = windows.find(([start, end]) =>
        (selected >= start && selected < end) ||
        (selected + 1440 >= start && selected + 1440 < end)
      );
      const message = windowEntry ? readout.getAttribute('data-window-' + windowEntry[2]) || '' : '';
      timeOut.textContent = time;
      timeOut.dateTime = time;
      copyOut.textContent = message;
      caption.textContent = (preview ? readout.dataset.captionPreview : readout.dataset.captionLive) || '';
      readout.dataset.mode = preview ? 'preview' : 'live';
      knob.setAttribute('aria-valuenow', String(selected));
      knob.setAttribute('aria-valuetext', time + ' — ' + (awake ? 'Awake' : 'Asleep') + ' — ' + message + ((preview ? readout.dataset.valuetextPreview : readout.dataset.valuetextLive) || ''));
    }

    function live() {
      const now = minutesNow();
      draw(now, false);
      if (previewPending) positionKnob(now + previewOffset);
    }

    function stopPreview() {
      previewPending = false;
      if (previewObserver) previewObserver.disconnect();
      previewObserver = null;
    }

    function stopReturn() {
      if (returnFrame !== null) cancelAnimationFrame(returnFrame);
      returnFrame = null;
    }

    function reset(animate = true, duration = 800) {
      const previousPointer = pointerId;
      pointerId = null;
      heldKey = null;
      knob.classList.remove('is-active');
      knob.classList.add('is-resting');
      if (previousPointer !== null && knob.hasPointerCapture(previousPointer)) {
        try { knob.releasePointerCapture(previousPointer); } catch (_) { }
      }
      stopPreview();
      stopReturn();
      const from = displayedMinutes;
      // Interpolate time around the shortest arc, including across midnight
      const distance = normalize(minutesNow() - from + 720) - 720;
      live();
      if (!animate || reducedMotion.matches || Math.abs(distance) < 0.5) return;
      positionKnob(from);
      const started = performance.now();
      function step(now) {
        const progress = Math.min(1, (now - started) / duration);
        const eased = 1 - Math.pow(1 - progress, 3);
        positionKnob(from + distance * eased);
        if (progress < 1) {
          returnFrame = requestAnimationFrame(step);
        } else {
          stopReturn();
          live();
        }
      }
      returnFrame = requestAnimationFrame(step);
    }

    // The knob runs from two hours early to now, easing in and out; the readout stays live
    function arrive() {
      if (!previewPending) return;
      stopPreview();
      const from = displayedMinutes;
      const distance = normalize(minutesNow() - from + 720) - 720;
      const started = performance.now();
      const duration = 1800;
      function step(now) {
        const progress = Math.min(1, (now - started) / duration);
        const eased = progress < .5 ? 4 * Math.pow(progress, 3) : 1 - Math.pow(-2 * progress + 2, 3) / 2;
        positionKnob(from + distance * eased);
        if (progress < 1) {
          returnFrame = requestAnimationFrame(step);
        } else {
          stopReturn();
          live();
          if (!explored) sectionEl.classList.add('is-inviting');
        }
      }
      returnFrame = requestAnimationFrame(step);
    }

    knob.addEventListener('pointerdown', event => {
      if (!event.isPrimary || event.button !== 0 || pointerId !== null) return;
      event.preventDefault();
      markExplored();
      stopPreview();
      stopReturn();
      knob.focus({ preventScroll: true });
      heldKey = null;
      pointerId = event.pointerId;
      try { knob.setPointerCapture(pointerId); } catch (_) { }
      knob.classList.remove('is-resting');
      knob.classList.add('is-active');
      draw(displayedMinutes, true);
    });

    knob.addEventListener('pointerenter', () => {
      if (returnFrame === null) knob.classList.remove('is-resting');
    });

    document.addEventListener('pointermove', event => {
      if (pointerId === null) return;
      event.preventDefault(); // Prevents touch scrolling while dragging
      const bounds = orbit.parentElement.getBoundingClientRect(); // Use .dial bounds
      const dx = event.clientX - (bounds.left + bounds.width / 2);
      const dy = event.clientY - (bounds.top + bounds.height / 2);
      if (Math.hypot(dx, dy) < 8) return;
      const angle = (Math.atan2(dx, -dy) * 180 / Math.PI + 360) % 360;
      const rawMinutes = (angle * 4 + 720) % 1440;
      draw(Math.round(rawMinutes / 5) * 5, true);
    }, { capture: true, passive: false });

    ['pointerup', 'pointercancel'].forEach(type => {
      document.addEventListener(type, event => {
        if (pointerId !== null) reset();
      }, { capture: true });
    });

    const deltas = { ArrowRight: 5, ArrowUp: 5, ArrowLeft: -5, ArrowDown: -5, PageUp: 60, PageDown: -60 };
    knob.addEventListener('keydown', event => {
      if (event.key === 'Escape') {
        event.preventDefault();
        reset();
        return;
      }
      if (!(event.key in deltas) && event.key !== 'Home' && event.key !== 'End') return;
      event.preventDefault();
      if (pointerId !== null) return;
      markExplored();
      const wasReturning = returnFrame !== null;
      stopPreview();
      stopReturn();
      if (wasReturning) selected = normalize(Math.round(displayedMinutes));
      if (!heldKey && !wasReturning) selected = Math.min(1435, Math.round(minutesNow() / 5) * 5);
      heldKey = event.key;
      knob.classList.remove('is-resting');
      knob.classList.add('is-active');
      if (event.key === 'Home') draw(0, true);
      else if (event.key === 'End') draw(1439, true);
      else draw(Math.max(0, Math.min(1439, selected + deltas[event.key])), true);
    });

    knob.addEventListener('keyup', event => {
      if (event.key === heldKey) reset();
    });

    knob.addEventListener('blur', () => {
      if (pointerId !== null || heldKey) reset();
    });

    window.addEventListener('blur', () => {
      if (!previewPending) reset();
    });

    if (hint) {
      hint.addEventListener('click', () => knob.focus({ preventScroll: true }));
    }

    function startTimer() {
      clearInterval(timer);
      timer = setInterval(() => {
        if (pointerId === null && !heldKey && returnFrame === null) live();
      }, 30000);
    }

    document.addEventListener('visibilitychange', () => {
      if (document.hidden) {
        if (!previewPending) reset(false);
      } else if (pointerId === null && !heldKey && returnFrame === null) {
        live();
      }
    });

    window.addEventListener('pagehide', () => {
      stopReturn();
      clearInterval(timer);
    });

    window.addEventListener('pageshow', event => {
      if (event.persisted && !previewPending) reset(false);
      startTimer();
    });

    reducedMotion.addEventListener('change', event => {
      if (event.matches) reset(false);
    });

    // The run starts once half the dial is in view (on phones the clipped dial shows about two
    // thirds at most). Not the empty .orbit: base.css hides div:empty, so it never intersects.
    // With reduced motion or without an observer the knob stays on now and only the halo is set.
    if (!explored && !reducedMotion.matches && 'IntersectionObserver' in window) {
      previewPending = true;
      previewObserver = new IntersectionObserver(entries => {
        if (!entries.some(entry => entry.isIntersecting)) return;
        previewObserver.disconnect();
        setTimeout(arrive, 250);
      }, { threshold: 0.5 });
      previewObserver.observe(orbit.parentElement);
    } else if (!explored) {
      sectionEl.classList.add('is-inviting');
    }

    live();
    startTimer();
  }

  function setupAllClocks() {
    document.querySelectorAll('.chronobiology-clock').forEach(initClock);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', setupAllClocks);
  } else {
    setupAllClocks();
  }

  document.addEventListener('shopify:section:load', event => {
    const clock = event.target.querySelector('.chronobiology-clock') || (event.target.classList.contains('chronobiology-clock') ? event.target : null);
    if (clock) initClock(clock);
  });
})();
