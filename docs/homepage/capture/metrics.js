(vw, dpr, mode) => {
  const sy = window.scrollY;
  const r = (el) => { const b = el.getBoundingClientRect(); return { x: Math.round(b.left), y: Math.round(b.top + sy), w: Math.round(b.width), h: Math.round(b.height), right: Math.round(b.right) }; };
  const visible = (el) => {
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden' || +cs.opacity === 0) return false;
    const b = el.getBoundingClientRect();
    return b.width > 0 && b.height > 0;
  };
  const clipAncestor = (el, stop) => {
    for (let a = el.parentElement; a && a !== document.documentElement; a = a.parentElement) {
      const cs = getComputedStyle(a);
      if (cs.overflowX !== 'visible' || cs.contain.includes('paint')) return a;
      if (a === stop) { /* keep walking above the section too */ }
    }
    return null;
  };
  const desc = (el) => {
    let s = el.tagName.toLowerCase();
    if (el.id) s += '#' + el.id.slice(0, 40);
    const c = [...el.classList].slice(0, 3).join('.');
    if (c) s += '.' + c;
    return s;
  };
  const textOf = (el) => (el.innerText || '').trim().replace(/\s+/g, ' ').slice(0, 60);
  const fname = (u) => { try { return decodeURIComponent(new URL(u, location.href).pathname.split('/').pop()); } catch (e) { return u; } };
  const wparam = (u) => { try { return +new URL(u, location.href).searchParams.get('width') || null; } catch (e) { return null; } };

  const secs = [...document.querySelectorAll('.shopify-section')].filter((s) => s.offsetParent !== null || getComputedStyle(s).position === 'fixed');
  const out = {
    vw, dpr, mode, bodyClass: document.body.className,
    docScrollWidth: document.documentElement.scrollWidth,
    bodyScrollWidth: document.body.scrollWidth,
    docHeight: document.documentElement.scrollHeight,
    sections: [],
  };
  for (const s of secs) {
    const b = r(s);
    const cs = getComputedStyle(s);
    const first = s.firstElementChild;
    let bg = cs.backgroundColor;
    // Effective background: walk down the first two levels for a painted background.
    const bgs = [];
    for (const el of [s, first, first && first.firstElementChild].filter(Boolean)) {
      const c = getComputedStyle(el);
      bgs.push({ el: desc(el), bg: c.backgroundColor, img: c.backgroundImage.slice(0, 80), pt: c.paddingTop, pb: c.paddingBottom, pl: c.paddingLeft, pr: c.paddingRight, mw: c.maxWidth });
    }
    const all = [...s.querySelectorAll('*')].filter(visible);
    // Content horizontal extent from text-bearing leaves and media.
    let minL = Infinity, maxR = -Infinity;
    const leaves = all.filter((el) => (el.children.length === 0 && (el.innerText || '').trim()) || /^(IMG|VIDEO|PICTURE|SVG|CANVAS|BUTTON|A)$/i.test(el.tagName));
    for (const el of leaves) {
      const bb = el.getBoundingClientRect();
      if (bb.right < 0 || bb.left > vw) continue;
      if (clipAncestor(el) && (bb.right > vw || bb.left < 0)) continue;
      minL = Math.min(minL, bb.left); maxR = Math.max(maxR, bb.right);
    }
    // Overflow offenders.
    const offenders = [];
    for (const el of all) {
      const bb = el.getBoundingClientRect();
      if (bb.right > vw + 1 || bb.left < -1) {
        const clip = clipAncestor(el);
        if (!clip) offenders.push({ el: desc(el), left: Math.round(bb.left), right: Math.round(bb.right), text: textOf(el).slice(0, 30) });
      }
    }
    // Text clipping inside overflow-hidden boxes.
    const clipped = [];
    for (const el of all) {
      const c = getComputedStyle(el);
      if (!(c.overflow.includes('hidden') || c.overflow.includes('clip'))) continue;
      if (!(el.innerText || '').trim()) continue;
      const clamp = c.webkitLineClamp && c.webkitLineClamp !== 'none';
      if (el.scrollHeight > el.clientHeight + 2 || el.scrollWidth > el.clientWidth + 2) {
        clipped.push({ el: desc(el), sw: el.scrollWidth, cw: el.clientWidth, sh: el.scrollHeight, ch: el.clientHeight, clamp: clamp ? c.webkitLineClamp : null, text: textOf(el).slice(0, 40) });
      }
    }
    // Smallest visible text.
    let minFont = Infinity, minFontEl = null;
    for (const el of leaves) {
      if (!(el.innerText || '').trim()) continue;
      const fs = parseFloat(getComputedStyle(el).fontSize);
      if (fs < minFont) { minFont = fs; minFontEl = desc(el) + ' "' + textOf(el).slice(0, 30) + '"'; }
    }
    // Images.
    const imgs = [];
    for (const img of s.querySelectorAll('img')) {
      if (!visible(img)) continue;
      const bb = img.getBoundingClientRect();
      const need = Math.round(bb.width * dpr);
      const cur = img.currentSrc || img.src;
      imgs.push({
        file: fname(cur), rw: Math.round(bb.width), rh: Math.round(bb.height), need,
        natural: img.naturalWidth, reqW: wparam(cur), sizes: img.getAttribute('sizes'), srcset: !!img.getAttribute('srcset'),
        loading: img.getAttribute('loading'), cur,
      });
    }
    // Videos.
    const vids = [...s.querySelectorAll('video')].filter(visible).map((v) => ({ src: fname(v.currentSrc), rw: Math.round(v.getBoundingClientRect().width), vw: v.videoWidth, vh: v.videoHeight, paused: v.paused }));
    // Small tap targets (touch only).
    const taps = [];
    if (dpr >= 2 && vw <= 768) {
      for (const el of s.querySelectorAll('a, button, [role="button"], summary, input, select')) {
        if (!visible(el)) continue;
        const bb = el.getBoundingClientRect();
        if (bb.width < 40 || bb.height < 40) taps.push({ el: desc(el), w: Math.round(bb.width), h: Math.round(bb.height), text: textOf(el).slice(0, 24) || el.getAttribute('aria-label') });
      }
    }
    // Headings for orientation.
    const heads = [...s.querySelectorAll('h1,h2,h3')].filter(visible).slice(0, 6).map((h) => {
      const c = getComputedStyle(h);
      const bb = h.getBoundingClientRect();
      return { tag: h.tagName, text: textOf(h).slice(0, 50), fs: c.fontSize, lh: c.lineHeight, ff: c.fontFamily.split(',')[0], fw: c.fontWeight, color: c.color, x: Math.round(bb.left), w: Math.round(bb.width), align: c.textAlign };
    });
    out.sections.push({
      id: s.id, top: b.y, height: b.h, bgs,
      content: { left: Math.round(minL), right: Math.round(maxR), width: Math.round(maxR - minL), leftGap: Math.round(minL), rightGap: Math.round(vw - maxR) },
      offenders: offenders.slice(0, 12), offenderCount: offenders.length,
      clipped: clipped.slice(0, 12), clippedCount: clipped.length,
      minFont, minFontEl, imgs, vids, taps: taps.slice(0, 15), tapCount: taps.length, heads,
    });
  }
  // True pixel size of each downloaded file (naturalWidth is density-corrected under srcset).
  const cache = {};
  const px = (u) => cache[u] || (cache[u] = new Promise((res) => { const i = new Image(); i.onload = () => res(i.naturalWidth); i.onerror = () => res(null); i.src = u; }));
  return Promise.all(out.sections.flatMap((s) => s.imgs.map(async (im) => {
    if (/\.svg$/i.test(im.file)) { im.under = false; im.actual = null; return; }
    im.actual = await px(im.cur);
    im.under = im.actual != null && im.actual < im.need * 0.95;
    delete im.cur;
  }))).then(() => JSON.stringify(out));
}
