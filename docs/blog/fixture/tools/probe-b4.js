location.protocol.indexOf('http') !== 0 ? 'BLANK' : (async () => {
  // R90b B4: every body picture of the test article must load (naturalWidth > 0) and decode.
  const imgs = Array.from(document.querySelectorAll('.kc-blog__body img'));
  const out = [];
  for (const i of imgs) {
    i.loading = 'eager';
    let decoded = 'ok';
    try { await i.decode(); } catch (e) { decoded = String(e.name); }
    out.push({ alt: i.alt, src: i.getAttribute('src').slice(-60), natural: [i.naturalWidth, i.naturalHeight], attrs: [i.getAttribute('width'), i.getAttribute('height')], decoded });
  }
  return JSON.stringify(out);
})()
