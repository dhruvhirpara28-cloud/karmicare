(function () {
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));
  const report = $('#fx-report');
  const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
  const norm = (html) => html.replace(/>\s+</g, '><').replace(/\s+/g, ' ').replace(/ >/g, '>').trim();

  if (new URLSearchParams(location.search).get('mode') === 'night') document.body.classList.add('night-mode');
  $('#fx-toggle').addEventListener('click', () => document.body.classList.toggle('night-mode'));
  $('#fx-run').addEventListener('click', () => run());

  const lists = (pair) => $$('.fx-variant', pair).map((v) => $('ul[role="list"]', v));
  const originals = (ul) => $$(':scope > li.research-card:not([data-marquee-clone])', ul);
  const rects = (ul) => originals(ul).map((li) => { const r = li.getBoundingClientRect(); return [Math.round(r.width), Math.round(r.height)]; });
  const colors = (ul) => {
    const li = originals(ul)[0];
    const cs = getComputedStyle(li);
    return [cs.backgroundColor, cs.color, getComputedStyle($('.research-card__source', li)).backgroundColor, getComputedStyle($('.research-card__detail', li)).color];
  };
  // The originals only (clones belong to the marquee), serialised by the browser so entities compare equal
  const serialise = (ul) => norm(originals(ul).map((li) => li.outerHTML).join(''));

  async function run() {
    const lines = [];
    const mode = document.body.classList.contains('night-mode') ? 'night' : 'day';
    lines.push(`viewport ${innerWidth}x${innerHeight} · ${mode}`);
    for (const pair of $$('.fx-pair')) {
      const name = pair.dataset.fxPair;
      const [a, b] = lists(pair);
      const sa = serialise(a), sb = serialise(b);
      let diff = '';
      if (sa !== sb) { let i = 0; while (i < sa.length && sa[i] === sb[i]) i++; diff = `\n  blocks: …${sa.slice(Math.max(0, i - 60), i + 80)}\n  entries: …${sb.slice(Math.max(0, i - 60), i + 80)}`; }
      lines.push(`${sa === sb ? 'PASS' : 'FAIL'} ${name}: DOM of blocks == DOM of metaobject entries (${originals(a).length} cards)${diff}`);
      const ra = JSON.stringify(rects(a)), rb = JSON.stringify(rects(b));
      lines.push(`${ra === rb ? 'PASS' : 'FAIL'} ${name}: card sizes equal ${ra}${ra === rb ? '' : ' vs ' + rb}`);
      const ca = JSON.stringify(colors(a)), cb = JSON.stringify(colors(b));
      lines.push(`${ca === cb ? 'PASS' : 'FAIL'} ${name}: colours equal ${ca}`);
      const media = (ul) => originals(ul).filter((li) => li.classList.contains('research-card--media')).length;
      lines.push(`${media(a) === media(b) ? 'PASS' : 'FAIL'} ${name}: wide (image) cards ${media(a)} vs ${media(b)}`);
      // Count within the originals: the marquee's clones repeat every link
      const inOriginals = (ul, sel) => originals(ul).flatMap((li) => $$(sel, li));
      const links = (ul) => inOriginals(ul, 'a.research-card__source[target="_blank"][rel="noopener"] .visually-hidden').filter((s) => s.textContent.trim() === 'Opens in a new window.').length;
      const plain = (ul) => inOriginals(ul, 'span.research-card__source').length;
      lines.push(`${links(a) === 5 && links(b) === 5 ? 'PASS' : 'FAIL'} ${name}: five new-tab study links with the screen-reader text (${links(a)}/${links(b)})`);
      lines.push(`${plain(a) === 1 && plain(b) === 1 ? 'PASS' : 'FAIL'} ${name}: one plain label for the "#" URL (${plain(a)}/${plain(b)})`);
      const slide = (ul) => originals(ul).filter((li) => li.classList.contains('slider__slide')).length;
      lines.push(`${slide(a) === slide(b) ? 'PASS' : 'FAIL'} ${name}: slider__slide on ${slide(a)} vs ${slide(b)} cards`);
    }
    const marquees = $$('kc-marquee');
    for (const [i, m] of marquees.entries()) {
      // The band sleeps off-screen (IntersectionObserver), so bring it into view first
      m.scrollIntoView({ block: 'center' });
      await sleep(900);
      const track = $('[data-marquee-track]', m);
      const clones = $$('[data-marquee-clone]', track).length;
      const t1 = track.style.transform;
      await sleep(600);
      const t2 = track.style.transform;
      const running = m.classList.contains('is-running');
      lines.push(`${running && clones > 0 && t1 !== t2 ? 'PASS' : 'FAIL'} marquee ${i + 1} (${i ? 'entries' : 'blocks'}): is-running ${running}, ${clones} clones, moved ${t1 !== t2}, reduced-motion ${matchMedia('(prefers-reduced-motion: reduce)').matches}`);
      // Keyboard order: only the originals' links are reachable; clones are aria-hidden with tabindex -1
      const cloneLinks = $$('[data-marquee-clone] a', track);
      const hiddenClones = $$('[data-marquee-clone][aria-hidden="true"]', track).length;
      const tabbable = originals(track).flatMap((li) => $$('a', li)).filter((a) => a.tabIndex === 0).length;
      lines.push(`${hiddenClones === clones && cloneLinks.every((a) => a.tabIndex === -1) && tabbable === 5 ? 'PASS' : 'FAIL'} marquee ${i + 1}: ${tabbable} tabbable study links in the originals, ${hiddenClones}/${clones} clones aria-hidden, clone links out of the tab order ${cloneLinks.every((a) => a.tabIndex === -1)}`);
    }
    scrollTo(0, 0);
    const text = lines.join('\n');
    report.textContent = text;
    document.title = 'R67 fixture · ' + (text.includes('FAIL') ? 'FAIL' : 'done');
    if (parent !== window) parent.postMessage({ fxReport: text }, '*');
    return text;
  }

  // Keyboard: focus lands on the second card's link of the entries marquee; a real Tab
  // (sent by the test driver) then moves to the third, and fxFocusCheck reads the result.
  window.fxFocusPrep = () => {
    const m = $$('kc-marquee')[1];
    const link = originals($('[data-marquee-track]', m))[1].querySelector('a.research-card__source');
    link.focus();
    return document.activeElement === link;
  };
  window.fxFocusCheck = async () => {
    const m = $$('kc-marquee')[1];
    const track = $('[data-marquee-track]', m);
    const link = originals(track)[2].querySelector('a.research-card__source');
    await sleep(1500);
    const band = m.getBoundingClientRect();
    const r = link.closest('li').getBoundingClientRect();
    const inView = r.left >= band.left - 1 && r.right <= band.right + 1;
    const t1 = track.style.transform;
    await sleep(400);
    const t2 = track.style.transform;
    const ok = document.activeElement === link && inView && t1 === t2;
    // reveal() only moves the band when a focus ring shows (:focus-visible), which needs the document to have focus
    const line = `${ok ? 'PASS' : 'FAIL'} marquee keyboard focus (entries): Tab reached the third card's link ${document.activeElement === link}, card in view ${inView}, band held still ${t1 === t2}, focus-visible ${link.matches(':focus-visible')}, document focused ${document.hasFocus()}`;
    report.textContent += '\n' + line;
    if (parent !== window) parent.postMessage({ fxReport: report.textContent }, '*');
    return line;
  };
  window.fxRun = run;
  // From the frame-*.html wrapper (another file:// origin): scroll to a selector, switch the mode
  window.addEventListener('message', (e) => {
    if (!e.data) return;
    if (e.data.fxScroll) { const el = $(e.data.fxScroll); if (el) el.scrollIntoView({ block: 'start' }); }
    if (e.data.fxMode) document.body.classList.toggle('night-mode', e.data.fxMode === 'night');
  });
  window.addEventListener('load', async () => { await sleep(1500); await run(); });
})();
