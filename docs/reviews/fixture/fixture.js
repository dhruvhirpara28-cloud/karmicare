(function () {
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));
  const report = $('#fx-report');
  const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
  const px = (n) => Math.round(n * 10) / 10;

  const params = new URLSearchParams(location.search);
  if (params.get('mode') === 'night') { document.body.classList.remove('day-mode'); document.body.classList.add('night-mode'); }
  if (parent !== window) document.body.classList.add('fx-framed'); // the frame page shows the report
  $('#fx-toggle').addEventListener('click', () => { document.body.classList.toggle('night-mode'); document.body.classList.toggle('day-mode'); run(); });
  $('#fx-run').addEventListener('click', () => run());

  async function run() {
    if (document.fonts && document.fonts.ready) await document.fonts.ready;
    const lines = [];
    const mode = document.body.classList.contains('night-mode') ? 'night' : 'day';
    lines.push(`viewport ${innerWidth}x${innerHeight} · ${mode}`);

    // Hero badge: one line for the rating text, the badge hidden under 750 (D-3, 20 Oct)
    for (const v of $$('.fx-hero-variant')) {
      const wrap = $('.hero-karmicare__badge-wrapper', v);
      const shown = getComputedStyle(wrap).display !== 'none';
      if (!shown) { lines.push(`PASS hero ${v.dataset.variant}: badge wrapper display none at ${innerWidth} (phones have no badge, D-3 of 20 Oct)`); continue; }
      const text = $('.hero-karmicare__badge-rating-text', v);
      const badge = $('.hero-karmicare__badge', v);
      const r = text.getBoundingClientRect();
      const lh = parseFloat(getComputedStyle(text).lineHeight);
      const oneLine = r.height <= lh * 1.5;
      const heading = $('.hero-karmicare__badge-heading', v).getBoundingClientRect();
      const cs = getComputedStyle(badge);
      lines.push(`${oneLine ? 'PASS' : 'FAIL'} hero ${v.dataset.variant}: "${text.textContent}" on one line (text ${px(r.width)}x${px(r.height)}, line-height ${px(lh)}, font ${cs.fontFamily.split(',')[0]} ${getComputedStyle(text).fontSize}), badge ${px(badge.getBoundingClientRect().width)}x${px(badge.getBoundingClientRect().height)}, heading ${px(heading.width)}x${px(heading.height)}, colour ${cs.color}, link ${badge.tagName === 'A'}`);
    }

    // Strip: artwork and rating on the same row, rating on one line, text and accessible name
    for (const v of $$('.fx-strip')) {
      const strip = $('.kc-category-strip', v);
      const brand = $('.kc-category-strip__brand', v);
      const rating = $('.kc-category-strip__rating', v);
      const box = $('.fx-buybox', v).getBoundingClientRect();
      if (!rating) { lines.push(`PASS strip ${v.dataset.variant}: no rating span (artwork only, ${px(brand.getBoundingClientRect().width)} wide in a ${px(box.width)} column)`); continue; }
      const rb = brand.getBoundingClientRect();
      const rr = rating.getBoundingClientRect();
      const score = $('.kc-category-strip__score', v);
      const sr = score.getBoundingClientRect();
      const sameRow = Math.abs((rb.top + rb.height / 2) - (rr.top + rr.height / 2)) < rb.height;
      const oneLine = sr.height <= parseFloat(getComputedStyle(score).fontSize) * 1.6;
      const cs = getComputedStyle(score);
      lines.push(`${sameRow && oneLine ? 'PASS' : 'FAIL'} strip ${v.dataset.variant}: "${score.textContent.replace(/\s+/g, ' ').trim()}" ${sameRow ? 'on the artwork row' : 'WRAPPED under the artwork'}, score ${px(sr.width)}x${px(sr.height)} (${cs.fontFamily.split(',')[0]} ${cs.fontSize} ${cs.fontWeight} ${cs.textTransform} tracking ${cs.letterSpacing}), rating ${px(rr.width)} wide, artwork ${px(rb.width)} wide, strip ${px(strip.getBoundingClientRect().width)}x${px(strip.getBoundingClientRect().height)} in a ${px(box.width)} column · aria "${rating.getAttribute('aria-label')}" · colours ${cs.color} / ${getComputedStyle($('.kc-category-strip__count', v)).color} / star ${getComputedStyle($('.kc-icon--star', v)).color}`);
    }
    // What the row needs with the old and the new text: artwork + gap + star + gap + score
    const first = $('.fx-strip[data-variant="fixed-en"]');
    if (first && $('.kc-category-strip__score', first)) {
      const strip = $('.kc-category-strip', first);
      const gap = parseFloat(getComputedStyle(strip).columnGap || getComputedStyle(strip).gap);
      const brandW = $('.kc-category-strip__brand', first).getBoundingClientRect().width;
      const scoreEl = $('.kc-category-strip__score', first);
      const ratingW = $('.kc-category-strip__rating', first).getBoundingClientRect().width;
      const scoreW = scoreEl.getBoundingClientRect().width;
      const probe = scoreEl.cloneNode(false); probe.textContent = '4.8 (234)'; probe.style.position = 'absolute'; probe.style.visibility = 'hidden'; scoreEl.parentNode.appendChild(probe);
      const oldScoreW = probe.getBoundingClientRect().width; probe.remove();
      const col = $('.fx-buybox', first).getBoundingClientRect().width;
      const need = (s) => px(brandW + gap + (ratingW - scoreW) + s);
      lines.push(`INFO strip row needs ${need(scoreW)} with "4.7/5 (110)" and ${need(oldScoreW)} with the old "4.8 (234)" (artwork ${px(brandW)} + gap ${gap} + star and gap ${px(ratingW - scoreW)} + score); column here ${px(col)}; the row wraps below a ${px(need(scoreW) + (innerWidth - col))} viewport now, ${px(need(oldScoreW) + (innerWidth - col))} before`);
    }
    const text = lines.join('\n');
    report.textContent = text;
    document.title = 'R95 fixture · ' + (text.includes('FAIL') ? 'FAIL' : 'done');
    if (parent !== window) parent.postMessage({ fxReport: text }, '*');
    return text;
  }
  window.fxRun = run;
  window.addEventListener('message', (e) => {
    if (!e.data) return;
    if (e.data.fxMode) { document.body.classList.toggle('night-mode', e.data.fxMode === 'night'); document.body.classList.toggle('day-mode', e.data.fxMode !== 'night'); run(); }
  });
  window.addEventListener('load', async () => { await sleep(1200); await run(); });
})();
