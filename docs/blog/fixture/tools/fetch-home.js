location.protocol !== 'https:' ? 'BLANK' : (async () => {
  // The homepage's end CTA (featured-product section) as the live page prints it, plus the head
  // styles it needs that an article page does not load (Loop widget styles, section CSS).
  const t = await (await fetch('/')).text();
  const d = new DOMParser().parseFromString(t, 'text/html');
  const sec = d.querySelector('[id$="featured_product_3XpDKw"]');
  const loop = d.querySelector('style.loop-style');
  const a = new DOMParser().parseFromString(await (await fetch('/blogs/news/nano-hydroxyapatite')).text(), 'text/html');
  const have = new Set(Array.from(a.querySelectorAll('link[rel=stylesheet]')).map((l) => l.getAttribute('href').split('?')[0]));
  const extra = Array.from(d.querySelectorAll('head link[rel=stylesheet]')).map((l) => l.getAttribute('href')).filter((h) => !have.has(h.split('?')[0]));
  return JSON.stringify({ section: sec ? sec.outerHTML : null, loopStyle: loop ? loop.outerHTML : null, extraHeadCss: extra });
})()
