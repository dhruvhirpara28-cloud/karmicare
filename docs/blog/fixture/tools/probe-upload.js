location.protocol !== 'https:' ? 'BLANK' : (async () => {
  // Find the URL Shopify gave the file Victor uploaded to Files (26 Oct) and its size.
  const base = 'kc-research-nhap-dentinal-tubule-occlusion-2000';
  const names = [];
  [' copy', '_copy', '-copy', '%20copy', ''].forEach((s) => ['.png', '.jpg', '.webp'].forEach((e) => names.push(base + s + e)));
  const size = (src) => new Promise((res) => {
    const i = new Image();
    i.onload = () => res([i.naturalWidth, i.naturalHeight]);
    i.onerror = () => res(null);
    i.src = src;
  });
  const out = {};
  for (const n of names) {
    const r = await size('https://www.karmicare.com/cdn/shop/files/' + n);
    if (r) out[n] = r;
  }
  return JSON.stringify(out);
})()
