location.protocol.indexOf('http') !== 0 ? 'BLANK' : (function () {
  // End CTA animation state: is the element defined, which mode panel shows, is a video in place.
  var el = document.querySelector('kc-hero-animation');
  if (!el) return JSON.stringify({ error: 'no kc-hero-animation' });
  el.scrollIntoView();
  var modes = Array.prototype.map.call(el.querySelectorAll('[data-kc-mode]'), function (m) {
    var v = m.querySelector('video');
    return { mode: m.dataset.kcMode, visible: getComputedStyle(m).display !== 'none', video: !!v, paused: v ? v.paused : null, readyState: v ? v.readyState : null, img: (m.querySelector('img') || {}).currentSrc };
  });
  return JSON.stringify({ defined: !!customElements.get('kc-hero-animation'), bodyMode: document.body.className.match(/(day|night)-mode/), reduce: matchMedia('(prefers-reduced-motion: reduce)').matches, modes: modes });
})()
