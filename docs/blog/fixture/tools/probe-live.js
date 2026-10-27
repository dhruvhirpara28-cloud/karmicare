location.protocol !== 'https:' ? 'BLANK' : (async () => {
  // After landing: is the live blog the new layout, and are the global lane's tokens live?
  const P = new DOMParser();
  const get = async (u) => P.parseFromString(await (await fetch(u + (u.includes('?') ? '&' : '?') + 'kc=' + Date.now(), { cache: 'no-store' })).text(), 'text/html');
  const out = {};
  for (const u of ['/blogs/news/nano-hydroxyapatite', '/nl/blogs/news/nano-hydroxyapatite', '/blogs/news']) {
    const d = await get(u);
    const body = d.querySelector('.kc-blog__body');
    const imgs = body ? Array.from(body.querySelectorAll('img')) : [];
    out[u] = {
      theme: (d.documentElement.innerHTML.match(/"name":"([^"]+)","id":(\d+)[^}]*"role":"main"/) || [])[1] || null,
      newLayout: !!d.querySelector('.kc-blog'),
      h1: d.querySelectorAll('h1').length,
      bodyHeadings: body ? Array.from(body.querySelectorAll('h1,h2,h3,h4,h5,h6')).map((h) => h.tagName[1]).join('') : null,
      bodyImgs: imgs.length,
      bodyImgsSized: imgs.filter((i) => i.getAttribute('width') && i.getAttribute('height')).length,
      tocLabel: (d.querySelector('.kc-blog-toc__eyebrow') || {}).textContent,
      sources: d.querySelectorAll('.kc-blog-sources__item').length,
      keepReading: d.querySelectorAll('.kc-blog-related .kc-blog-row').length,
      endCta: !!d.querySelector('[id*="featured_product_kc_blog"]'),
      featured: ((d.querySelector('.kc-blog__figure img') || {}).getAttribute || (() => null)).call(d.querySelector('.kc-blog__figure img'), 'src'),
      indexRows: d.querySelectorAll('.kc-blog-index .kc-blog-row').length,
    };
  }
  // tokens: read the live kc-tokens.css that the page links
  const home = await get('/');
  const href = Array.from(home.querySelectorAll('link[rel=stylesheet]')).map((l) => l.getAttribute('href')).find((h) => h && h.includes('kc-tokens.css'));
  const css = href ? await (await fetch(href)).text() : '';
  out.tokens = {
    backboneProximaFirst: /--kc-font-role-backbone:\s*"proxima-nova"/.test(css),
    bodySolid: /--kc-mapped-text-default-body:\s*#191f38/.test(css),
  };
  return JSON.stringify(out);
})()
