location.protocol !== 'https:' ? 'BLANK' : (async () => {
  // What the live article prints where the body pictures should be (after "So, What Is Nano Hydroxyapatite?").
  const t = await (await fetch('/blogs/news/nano-hydroxyapatite?kc=' + Date.now(), { cache: 'no-store' })).text();
  const out = {};
  const i = t.indexOf('So, What Is Nano Hydroxyapatite?');
  out.around = i > 0 ? t.slice(i, i + 700) : null;
  out.imgCount = (t.match(/<img/g) || []).length;
  out.charcoal = (t.match(/charcoal-toothbrushes[^"' ]*/g) || []).slice(0, 4);
  out.liquidError = (t.match(/Liquid (syntax )?error[^<]{0,200}/gi) || []).slice(0, 3);
  for (const h of ['/blogs/news/morning-and-night-time-brushing-why-timing-matters']) {
    const m = await (await fetch(h + '?kc=' + Date.now())).text();
    const b = m.indexOf('kc-blog__body');
    out.morningBodyImgs = (m.slice(b, m.indexOf('kc-blog-related', b)).match(/<img[^>]*>/g) || []).map((x) => x.slice(0, 160));
  }
  return JSON.stringify(out);
})()
