/**
 * Karmicare Chronobiology 24-Hour Clock
 * Interactive circular slider and real-time biological rhythm visualizer
 */
(() => {
  'use strict';

  // Exact seven source messages from specification:
  // Start-inclusive/end-exclusive (in minutes from midnight), with the final window wrapping midnight.
  const windows = [
    [300, 480, 'saliva is only now picking up after the night, and the enamel is least protected before your first drink'],
    [480, 660, 'breakfast and coffee dropped the pH within minutes — saliva spends the next half hour bringing it back'],
    [660, 840, 'lunch restarts the cycle: every eating occasion opens a fresh acid window, whatever its size'],
    [840, 1020, 'grazing hours — the most frequent acid challenge of the day, and it is how often, not how much'],
    [1020, 1200, 'the last big acid window of the day; after this, saliva starts winding down'],
    [1200, 1380, 'melatonin is rising and salivary flow is dropping — what is left on the enamel now stays for hours'],
    [1380, 1740, 'saliva is near its minimum and clearance has almost stopped: the longest unguarded stretch, and the repair window']
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

    const currentSiteTheme = document.body.classList.contains('night-mode') ? 'night' : (
      document.body.classList.contains('day-mode') ? 'day' : (
        localStorage.getItem('theme') || (matchMedia('(prefers-color-scheme: dark)').matches ? 'night' : 'day')
      )
    );
    syncTheme(currentSiteTheme);

    // Watch for global site theme toggle on <body>
    const bodyObserver = new MutationObserver(() => {
      const isNight = document.body.classList.contains('night-mode');
      syncTheme(isNight ? 'night' : 'day');
    });
    bodyObserver.observe(document.body, { attributes: true, attributeFilter: ['class'] });

    let pointerId = null;
    let heldKey = null;
    let selected = 0;
    let displayedMinutes = 0;
    let returnFrame = null;
    let timer = null;

    const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');
    let introPending = false; // Disabled: intro animation unreliable in Shopify (observer may not fire)
    let introObserver = null;

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
      const message = windowEntry ? windowEntry[2] : '';
      timeOut.textContent = time;
      timeOut.dateTime = time;
      copyOut.textContent = message;
      caption.textContent = preview ? 'your mouth at this hour:' : 'your mouth right now:';
      readout.dataset.mode = preview ? 'preview' : 'live';
      knob.setAttribute('aria-valuenow', String(selected));
      knob.setAttribute('aria-valuetext', time + ' — ' + (awake ? 'Awake' : 'Asleep') + ' — ' + message + (preview ? '. Release to return to now.' : '. Current local time.'));
    }

    function live() {
      const now = minutesNow();
      draw(now, false);
      if (introPending) positionKnob(now - 180);
    }

    function finishIntro() {
      introPending = false;
      if (introObserver) introObserver.disconnect();
      introObserver = null;
    }

    function stopReturn() {
      if (returnFrame !== null) cancelAnimationFrame(returnFrame);
      returnFrame = null;
      knob.classList.remove('is-introducing');
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
      finishIntro();
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

    function introduceClock() {
      if (!introPending) return;
      // One clockwise sweep teaches circular path
      reset(true, 1600);
      if (returnFrame !== null) knob.classList.add('is-introducing');
    }

    knob.addEventListener('pointerdown', event => {
      if (!event.isPrimary || event.button !== 0 || pointerId !== null) return;
      event.preventDefault();
      finishIntro();
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
      const wasReturning = returnFrame !== null;
      finishIntro();
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
      if (!introPending) reset();
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
        if (!introPending) reset(false);
      } else if (pointerId === null && !heldKey && returnFrame === null) {
        live();
      }
    });

    window.addEventListener('pagehide', () => {
      stopReturn();
      clearInterval(timer);
    });

    window.addEventListener('pageshow', event => {
      if (event.persisted && !introPending) reset(false);
      startTimer();
    });

    reducedMotion.addEventListener('change', event => {
      if (event.matches) reset(false);
    });

    live();
    startTimer();

    if (introPending && 'IntersectionObserver' in window) {
      introObserver = new IntersectionObserver(entries => {
        if (entries.some(entry => entry.isIntersecting && entry.intersectionRatio >= 0.1)) {
          introduceClock();
        }
      }, { threshold: 0.1 });
      introObserver.observe(orbit);
    } else if (introPending) {
      reset(false);
    }
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
