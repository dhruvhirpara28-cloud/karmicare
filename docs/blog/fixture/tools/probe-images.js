location.protocol !== 'https:' ? 'BLANK' : (async () => {
  // Natural size of candidate featured pictures that are already live (Files), for the nano article.
  const names = [
    'Benefit_card_01_Nano-hydroxyapatite_Hover.png',
    'kc-two-formulas-duo.png',
    'kc-hero-kit.png',
    'karmicare-duo-pack-transparent.png',
    'karmicare-awake-morning-asleep-evening-toothpaste.png',
    'kc-anim-am-hero-1080x960-poster-landed-v1.webp',
    'kc-anim-pm-hero-1080x960-poster-landed-v1.webp',
    'Benefit_image_1.png',
    'Benefit_image_2.png',
    'Benefit_image_3.png',
    'kc-research-nhap-tubules-2000x2400-v1.jpg',
  ];
  const size = (src) => new Promise((res) => {
    const i = new Image();
    i.onload = () => res([i.naturalWidth, i.naturalHeight]);
    i.onerror = () => res(null);
    i.src = src;
  });
  const out = {};
  for (const n of names) out[n] = await size('https://www.karmicare.com/cdn/shop/files/' + n);
  return JSON.stringify(out);
})()
