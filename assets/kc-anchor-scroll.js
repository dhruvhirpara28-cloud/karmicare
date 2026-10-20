/* In-page anchor links (href="#section" on this page) glide to their section with a calm
   ease-in-out instead of jumping (Victor, 20 Oct). The landing spot clears the sticky header,
   the hash still updates, and the target takes focus for keyboard and screen reader users.
   A wheel, touch or key during the glide hands control back to the visitor. With
   prefers-reduced-motion the page jumps, as before. Loaded once from layout/theme.liquid. */
(() => {
  if (window.kcAnchorScrollBound) return;
  window.kcAnchorScrollBound = true;

  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const easeInOutCubic = (t) => (t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2);
  let frame = null;

  // Room for the sticky header, when it sticks, plus a little air under it
  const headerOffset = () => {
    const header = document.querySelector('.section-header');
    if (!header) return 0;
    const position = getComputedStyle(header).position;
    if (position !== 'sticky' && position !== 'fixed') return 0;
    return header.getBoundingClientRect().height + 16;
  };

  const stop = () => {
    if (frame === null) return;
    cancelAnimationFrame(frame);
    frame = null;
  };

  ['wheel', 'touchstart', 'keydown'].forEach((type) => {
    window.addEventListener(type, stop, { passive: true });
  });

  const glide = (to) => {
    stop();
    const from = window.scrollY;
    const distance = to - from;
    if (Math.abs(distance) < 2) return;
    // Longer trips take a little longer, within a calm 0.7-1.2s
    const duration = Math.min(1200, Math.max(700, Math.abs(distance) * 0.35));
    let start = null;

    const step = (time) => {
      if (start === null) start = time;
      const progress = Math.min((time - start) / duration, 1);
      window.scrollTo(0, from + distance * easeInOutCubic(progress));
      frame = progress < 1 ? requestAnimationFrame(step) : null;
    };
    frame = requestAnimationFrame(step);
  };

  document.addEventListener('click', (event) => {
    if (event.defaultPrevented || event.button !== 0) return;
    if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;

    const link = event.target.closest('a[href*="#"]');
    if (!link || link.getAttribute('aria-disabled') === 'true') return;

    const url = new URL(link.href, window.location.href);
    if (url.origin !== window.location.origin || url.pathname !== window.location.pathname) return;
    if (url.search !== window.location.search || url.hash.length < 2) return;

    let target = null;
    try {
      target = document.getElementById(decodeURIComponent(url.hash.slice(1)));
    } catch (error) {
      return;
    }
    if (!target) return;

    event.preventDefault();
    const top = Math.max(0, target.getBoundingClientRect().top + window.scrollY - headerOffset());
    history.pushState(null, '', url.hash);

    if (!target.hasAttribute('tabindex')) target.setAttribute('tabindex', '-1');
    target.focus({ preventScroll: true });

    if (reducedMotion.matches) {
      stop();
      window.scrollTo(0, top);
    } else {
      glide(top);
    }
  });
})();
