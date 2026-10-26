location.protocol !== 'https:' ? 'BLANK' : (async () => {
  // The 7 old Webflow paths after Victor's redirect import (26 Oct): status and where each ends up.
  const paths = [
    '/en/product/biorhythmic-oral-care-duo', '/en/why-use-hydroxyapatite-toothpaste', '/en/why-stop-using-fluoride-toothpaste',
    '/en/articles/nano-hydroxyapatite', '/en/article/nano-hydroxyapatite', '/en/articles/benefits-of-nootropics', '/en/articles/sls-free-toothpaste',
  ];
  const out = {};
  for (const p of paths) {
    try {
      const r = await fetch(p + '?kc=' + Date.now(), { redirect: 'follow', cache: 'no-store' });
      out[p] = [r.status, r.url.replace(location.origin, '').split('?')[0]];
    } catch (e) { out[p] = String(e); }
  }
  return JSON.stringify(out);
})()
