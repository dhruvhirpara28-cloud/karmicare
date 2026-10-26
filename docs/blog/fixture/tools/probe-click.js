location.protocol.indexOf('http') !== 0 ? 'BLANK' : (function () {
  // Step 1 (?step=click): click the third contents link. Step 2 (any other run): report where the
  // heading is, the scroll margin it should land on, the current link and the #fragment.
  // Orca's tab only draws (and animates) per screenshot, so take screenshots between the steps.
  const links = Array.from(document.querySelectorAll('.kc-blog-d-toc__link'));
  const a = links[2];
  if (!a) return JSON.stringify({ error: 'no link', count: links.length });
  const target = document.getElementById(a.getAttribute('href').slice(1));
  if (!window.__kcClicked) {
    window.__kcClicked = true;
    window.__kcScrolls = [];
    window.addEventListener('scroll', () => window.__kcScrolls.push(Math.round(scrollY)), { passive: true });
    a.click();
    return JSON.stringify({ clicked: a.textContent, scrollY: Math.round(scrollY), hash: location.hash });
  }
  return JSON.stringify({
    link: a.textContent,
    scrollY: Math.round(scrollY),
    scrollSteps: window.__kcScrolls.length,
    firstSteps: window.__kcScrolls.slice(0, 8),
    headingTop: Math.round(target.getBoundingClientRect().top),
    scrollMarginTop: getComputedStyle(target).scrollMarginTop,
    current: (document.querySelector('.kc-blog-d-toc__link[aria-current="true"]') || {}).textContent,
    hash: location.hash,
  });
})()
