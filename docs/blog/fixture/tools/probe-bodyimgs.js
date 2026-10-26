location.protocol !== 'https:' ? 'BLANK' : (async () => {
  // B2: can the theme know each body picture's size? Check whether the file also lives in this
  // store's Files (/cdn/shop/files/<name>, what Liquid's images['<name>'] resolves) and its size.
  const names = [
    'charcoal-toothbrushes.jpg', 'woman-holds-orange.jpg', 'man-with-toothache.jpg', 'woman-meditating.jpg',
    'Untitled_image_2.jpg', 'morning_brushing_3.jpg', 'NOOTROPICS_2.jpg', 'nootropic_3_1.jpg', 'SLS_2.jpg', 'SLS_3.jpg',
    'Untitled_image_1.jpg', 'FLUORIDE_FREE_3.jpg', 'depression.jpg', 'OVERALL_HEALTH_1.jpg', 'TOP_NATURAL_WHITENING_2.jpg', 'HEADACHES_3.jpg',
  ];
  const size = (src) => new Promise((res) => { const i = new Image(); i.onload = () => res([i.naturalWidth, i.naturalHeight]); i.onerror = () => res(null); i.src = src; });
  const out = {};
  for (const n of names) {
    out[n] = {
      ownFiles: await size('https://www.karmicare.com/cdn/shop/files/' + n),
      otherStore: n.includes('_') && !/^(charcoal|woman|man)/.test(n) ? null : await size('https://cdn.shopify.com/s/files/1/0765/7586/7189/files/' + n),
    };
  }
  return JSON.stringify(out);
})()
