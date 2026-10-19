// In-page measurement for docs/utopia/tools/measure.mjs. Evaluated as an expression
// in the live page; returns one JSON-able object per viewport. Read-only apart from a
// data-u-i index on each measured text element (measure.mjs uses it to ask the CSS
// domain which rule set the font size).
(() => {
  const vw = window.innerWidth;
  const dpr = window.devicePixelRatio || 1;
  const round = (n) => Math.round(n * 10) / 10;
  const SAMPLE = 'Karmicare supports a calm morning and evening ritual for teeth and gums every day.';
  const canvas = document.createElement('canvas');
  const ctx = canvas.getContext('2d');
  const charWidthCache = new Map();

  function avgCharWidth(cs) {
    const font = `${cs.fontStyle} ${cs.fontWeight} ${cs.fontSize} ${cs.fontFamily}`;
    if (!charWidthCache.has(font)) {
      ctx.font = font;
      charWidthCache.set(font, ctx.measureText(SAMPLE).width / SAMPLE.length);
    }
    return charWidthCache.get(font);
  }

  function sectionName(el) {
    const id = el.id.replace(/^shopify-section-/, '');
    return id.replace(/^.*__/, '').replace(/_[A-Za-z0-9]{6}$/, '') || id;
  }

  function shortSel(el) {
    const cls = [...el.classList].filter((c) => !/^(js-|scroll-trigger|animate)/.test(c)).slice(0, 2);
    return el.tagName.toLowerCase() + (el.id ? '#' + el.id : '') + (cls.length ? '.' + cls.join('.') : '');
  }

  function visible(el) {
    if (!el.checkVisibility({ checkOpacity: true, checkVisibilityCSS: true })) return false;
    const r = el.getBoundingClientRect();
    return r.width > 0 && r.height > 0;
  }

  function blockAncestor(el) {
    let b = el;
    while (b && b !== document.body && getComputedStyle(b).display.startsWith('inline')) b = b.parentElement;
    return b || el;
  }

  function contentWidth(el) {
    const cs = getComputedStyle(el);
    return el.getBoundingClientRect().width - parseFloat(cs.paddingLeft) - parseFloat(cs.paddingRight)
      - parseFloat(cs.borderLeftWidth) - parseFloat(cs.borderRightWidth);
  }

  const sectionEls = [...document.querySelectorAll('[id^="shopify-section-"]')]
    .filter((el) => !el.parentElement.closest('[id^="shopify-section-"]'));

  // How many average characters of running text one ch (the "0") holds in the body font;
  // generate.py sizes --kc-fluid-measure with it.
  const bodyCs = getComputedStyle(document.body);
  ctx.font = `${bodyCs.fontWeight} 16px ${bodyCs.fontFamily}`;
  const chRatio = ctx.measureText('0').width / (ctx.measureText(SAMPLE).width / SAMPLE.length);

  const out = {
    url: location.href,
    chRatio: Math.round(chRatio * 1000) / 1000,
    vw,
    vh: window.innerHeight,
    dpr,
    docHeight: document.documentElement.scrollHeight,
    horizontalOverflow: document.documentElement.scrollWidth - vw,
    rootFontSize: parseFloat(getComputedStyle(document.documentElement).fontSize),
    bodyMode: document.body.classList.contains('night-mode') ? 'night' : 'day',
    sections: [],
    texts: [],
    grids: [],
    media: [],
  };

  let textIndex = 0;
  for (const sec of sectionEls) {
    const name = sectionName(sec);
    const sr = sec.getBoundingClientRect();
    if (sr.height < 1) continue;
    const section = {
      name,
      id: sec.id,
      top: Math.round(sr.top + window.scrollY),
      height: Math.round(sr.height),
      textLeft: null,
      textRight: null,
      mediaLeft: null,
      mediaRight: null,
      containers: [],
    };

    // Text elements: any visible element with its own non-empty text node.
    const seen = new Set();
    const walker = document.createTreeWalker(sec, NodeFilter.SHOW_TEXT);
    while (walker.nextNode()) {
      const node = walker.currentNode;
      const txt = node.textContent.replace(/\s+/g, ' ').trim();
      if (txt.length < 2) continue;
      const el = node.parentElement;
      if (!el || seen.has(el) || el.closest('script, style, noscript, template, svg, select, option')) continue;
      seen.add(el);
      if (!visible(el)) continue;
      const r = el.getBoundingClientRect();
      const offscreen = r.right <= 0 || r.left >= vw;
      const cs = getComputedStyle(el);
      const own = [...el.childNodes].filter((n) => n.nodeType === 3).map((n) => n.textContent).join(' ')
        .replace(/\s+/g, ' ').trim();
      const tops = new Set();
      for (const n of el.childNodes) {
        if (n.nodeType !== 3 || !n.textContent.trim()) continue;
        const range = document.createRange();
        range.selectNodeContents(n);
        for (const cr of range.getClientRects()) if (cr.width > 1) tops.add(Math.round(cr.top / 3));
      }
      const lines = Math.max(1, tops.size);
      const blk = blockAncestor(el);
      const measureWidth = contentWidth(blk);
      const fs = parseFloat(cs.fontSize);
      const lh = cs.lineHeight === 'normal' ? null : parseFloat(cs.lineHeight);
      const i = textIndex++;
      el.setAttribute('data-u-i', String(i));
      out.texts.push({
        i,
        section: name,
        sel: shortSel(el),
        text: own.slice(0, 60),
        chars: own.length,
        fs: round(fs),
        lh: lh === null ? 'normal' : round(lh),
        ls: cs.letterSpacing,
        fw: cs.fontWeight,
        ff: cs.fontFamily.split(',')[0].replace(/["']/g, '').trim(),
        tt: cs.textTransform,
        x: Math.round(r.left),
        w: Math.round(r.width),
        lines,
        cplActual: lines > 1 ? Math.round(own.length / lines) : null,
        cplCapacity: Math.round(measureWidth / avgCharWidth(cs)),
        measureWidth: Math.round(measureWidth),
        offscreen,
      });
      if (!offscreen) {
        section.textLeft = section.textLeft === null ? r.left : Math.min(section.textLeft, r.left);
        section.textRight = section.textRight === null ? r.right : Math.max(section.textRight, r.right);
      }
    }

    // Containers that cap the width of their content.
    for (const el of sec.querySelectorAll('*')) {
      const cs = getComputedStyle(el);
      if (cs.maxWidth === 'none' || cs.maxWidth.endsWith('%')) continue;
      if (!visible(el)) continue;
      const r = el.getBoundingClientRect();
      if (r.width < 240) continue;
      section.containers.push({ sel: shortSel(el), maxWidth: cs.maxWidth, width: Math.round(r.width), left: Math.round(r.left) });
      if (section.containers.length >= 6) break;
    }

    // Grids and wrapping rows with at least two visible children of real width.
    for (const el of sec.querySelectorAll('*')) {
      const cs = getComputedStyle(el);
      const isGrid = cs.display === 'grid' || cs.display === 'inline-grid';
      const isFlexRow = (cs.display === 'flex' || cs.display === 'inline-flex') && cs.flexDirection.startsWith('row');
      if (!isGrid && !isFlexRow) continue;
      if (!visible(el)) continue;
      const kids = [...el.children].filter((k) => visible(k) && k.getBoundingClientRect().width >= 100);
      if (kids.length < 2) continue;
      const r = el.getBoundingClientRect();
      if (r.width < 300) continue;
      const firstTop = Math.round(kids[0].getBoundingClientRect().top);
      const row = kids.filter((k) => Math.abs(Math.round(k.getBoundingClientRect().top) - firstTop) < 4);
      out.grids.push({
        section: name,
        sel: shortSel(el),
        display: cs.display,
        width: Math.round(r.width),
        left: Math.round(r.left),
        columns: isGrid ? cs.gridTemplateColumns.split(' ').length : row.length,
        template: isGrid ? cs.gridTemplateColumns : null,
        gap: cs.columnGap,
        childWidths: row.map((k) => Math.round(k.getBoundingClientRect().width)).slice(0, 8),
      });
    }

    // Images and videos: rendered size against the largest source on offer.
    for (const el of sec.querySelectorAll('img, video')) {
      if (!visible(el)) continue;
      const r = el.getBoundingClientRect();
      if (r.width < 80) continue;
      let natural = 0;
      let maxSrc = 0;
      if (el.tagName === 'IMG') {
        natural = el.naturalWidth;
        const set = el.getAttribute('srcset') || '';
        for (const part of set.split(',')) {
          const m = part.trim().match(/\s(\d+)w$/);
          if (m) maxSrc = Math.max(maxSrc, +m[1]);
        }
        const wParam = (el.currentSrc || el.src).match(/[?&]width=(\d+)/);
        if (!maxSrc && wParam) maxSrc = +wParam[1];
      } else {
        natural = el.videoWidth;
      }
      const best = Math.max(maxSrc, natural);
      out.media.push({
        section: name,
        sel: shortSel(el),
        tag: el.tagName.toLowerCase(),
        src: (el.currentSrc || el.src || '').split('/').pop().split('?')[0].slice(0, 60),
        w: Math.round(r.width),
        h: Math.round(r.height),
        left: Math.round(r.left),
        natural,
        maxSrc,
        upscale: best ? round((r.width * dpr) / best) : null,
        fullBleed: r.width >= vw - 2,
      });
      if (r.width < vw - 2) {
        section.mediaLeft = section.mediaLeft === null ? r.left : Math.min(section.mediaLeft, r.left);
        section.mediaRight = section.mediaRight === null ? r.right : Math.max(section.mediaRight, r.right);
      }
    }

    for (const k of ['textLeft', 'textRight', 'mediaLeft', 'mediaRight']) {
      if (section[k] !== null) section[k] = Math.round(section[k]);
    }
    out.sections.push(section);
  }
  return out;
})()
