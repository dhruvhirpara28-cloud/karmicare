// Clock readout options for Victor (26 Oct). Preview only, loaded by index*.html. Runs before the
// deferred clock script: it moves the readout under the dial and adds the variant's pieces, then
// follows the clock script's output (time, copy, knob position) with MutationObservers.
(() => {
  const variant = new URLSearchParams(location.search).get('variant');
  if (!['a', 'b', 'c', 'd', 'e'].includes(variant)) return;
  document.documentElement.dataset.kcVariant = variant;
  if (new URLSearchParams(location.search).has('veil')) document.documentElement.dataset.kcVeil = '';
  if (new URLSearchParams(location.search).has('nolabels')) document.documentElement.dataset.kcNolabels = '';

  const section = document.querySelector('.chronobiology-clock');
  if (!section) return;
  const readout = section.querySelector('.readout');
  const stage = section.querySelector('.stage');
  const dial = section.querySelector('.dial');
  const knob = section.querySelector('.knob');
  const time = section.querySelector('.clock-time');
  const caption = section.querySelector('.clock-caption');
  const copy = section.querySelector('.state-copy');
  const hint = section.querySelector('.hint');

  // Under the dial, the pill first, then the time and the copy
  stage.after(readout);
  readout.prepend(hint);

  // Drag state for B and C, and "taken" for A's pill
  knob.addEventListener('pointerdown', () => section.classList.add('kc-dragging', 'kc-taken'));
  knob.addEventListener('keydown', () => section.classList.add('kc-taken'));
  ['pointerup', 'pointercancel'].forEach(type =>
    document.addEventListener(type, () => section.classList.remove('kc-dragging'), true));

  // A and C: mark the copy when its window changes (not on the clock script's height probes)
  let shownCopy = '';
  new MutationObserver(() => {
    if (copy.textContent === shownCopy) return;
    const first = shownCopy === '';
    shownCopy = copy.textContent;
    if (first) return;
    copy.classList.remove('kc-changed');
    void copy.offsetWidth;
    copy.classList.add('kc-changed');
  }).observe(copy, { childList: true, characterData: true, subtree: true });

  // D (Victor's pick, 26 Oct): the time line and the copy themselves move into the orb, no panel;
  // the pill stays under the dial. The clock script keeps updating and measuring them in place.
  if (variant === 'd' || variant === 'e') {
    const face = document.createElement('div');
    face.className = 'kc-orb-text';
    face.append(section.querySelector('.time-line'), copy);
    dial.append(face);
    // Victor (26 Oct): the pill goes above the orb
    stage.before(readout);
    // E on phones: the label and copy sit right under the orb instead of inside it
    if (variant === 'e') {
      const phone = matchMedia('(max-width: 749px)');
      const timeline = section.querySelector('.timeline');
      const place = () => {
        if (phone.matches) timeline.after(face);
        else dial.append(face);
      };
      place();
      phone.addEventListener('change', place);
    }
  }

  if (variant === 'a') {
    const face = document.createElement('div');
    face.className = 'kc-face';
    face.setAttribute('aria-hidden', 'true');
    face.innerHTML = '<span class="kc-face__time"></span><span class="kc-face__caption"></span>';
    dial.append(face);
    const sync = () => {
      face.firstChild.textContent = time.textContent;
      face.lastChild.textContent = caption.textContent.replace(/:\s*$/, '');
    };
    sync();
    const watch = new MutationObserver(sync);
    watch.observe(time, { childList: true, characterData: true, subtree: true });
    watch.observe(caption, { childList: true, characterData: true, subtree: true });
  }

  // E (Victor, 26 Oct): D's text in the orb without the time, and B's time badge on the knob,
  // shown at all times
  if (variant === 'b' || variant === 'e') {
    const badge = document.createElement('div');
    badge.className = 'kc-badge';
    badge.setAttribute('aria-hidden', 'true');
    dial.append(badge);
    // Inside the ring, towards the centre, so it never clips at the dial edge on phones. E keeps it
    // close to the knob, clear of the centred copy.
    const inner = (variant === 'e' ? 178 - 34 : 178 - 46) / 604 * 100;
    const place = () => {
      const angle = +(knob.dataset.angle || 0) * Math.PI / 180;
      badge.style.left = (50 + inner * Math.sin(angle)) + '%';
      badge.style.top = (50 - inner * Math.cos(angle)) + '%';
      badge.textContent = time.textContent;
    };
    place();
    const watch = new MutationObserver(place);
    watch.observe(knob, { attributes: true, attributeFilter: ['style', 'data-angle'] });
    watch.observe(time, { childList: true, characterData: true, subtree: true });
  }
})();
