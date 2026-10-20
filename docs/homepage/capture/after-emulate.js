// A1 after-evidence: DOM emulation of the branch's Liquid markup and settings changes on the
// live page. It is evidence for the layout only; the real Liquid still needs the preview gate.
(() => {
  const widthUrl = (src, w) => {
    const u = new URL(src, location.href);
    u.searchParams.set('width', w);
    return u.href;
  };
  const srcset = (img, widths) => widths.map((w) => `${widthUrl(img.currentSrc || img.src, w)} ${w}w`).join(', ');

  // 2124ebb, templates/index.json: featured-product benefits_layout "stacked"
  document.querySelectorAll('.featured-product--benefits-inline').forEach((el) => {
    el.classList.replace('featured-product--benefits-inline', 'featured-product--benefits-stacked');
  });

  // bf5d314, snippets/research-card.liquid: a chip without a study URL is a plain label
  document.querySelectorAll('a.research-card__source').forEach((a) => {
    if ((a.getAttribute('href') || '#') !== '#') return;
    const span = document.createElement('span');
    span.className = a.className;
    span.appendChild(a.querySelector('.research-card__source-text').cloneNode(true));
    a.replaceWith(span);
  });

  // 7ff0562, sections/care-comes-back.liquid: markers are empty rings
  document.querySelectorAll('.care-comes-back__marker').forEach((m) => { m.textContent = ''; });

  // 1506cab, sections/hero-karmicare.liquid: badge anchor on this template; avatar srcset
  document.querySelectorAll('a.hero-karmicare__badge').forEach((a) => {
    const href = a.getAttribute('href') || '';
    const hero = a.closest('.shopify-section');
    if (href.includes('#shopify-section-template--') && hero) {
      const tpl = hero.id.replace('shopify-section-', '').split('__')[0];
      a.setAttribute('href', `#shopify-section-${tpl}__${href.split('__').pop()}`);
    }
  });
  document.querySelectorAll('img.hero-karmicare__badge-avatar').forEach((img) => {
    img.srcset = srcset(img, [56, 112, 168]);
    img.sizes = '56px';
    img.height = 72;
  });

  // 39a00a8, sections/two-formulas-karmicare.liquid: tube srcset up to 780, sizes 220/260
  document.querySelectorAll('img.two-formulas__image').forEach((img) => {
    img.srcset = srcset(img, [220, 260, 330, 440, 520, 660, 780]);
    img.sizes = '(min-width: 990px) 260px, 220px';
    img.removeAttribute('width');
    img.removeAttribute('height');
  });

  // 174997e, sections/km-faq-accordion.liquid: filter chips are buttons
  document.querySelectorAll('span.km-faq__filter-btn').forEach((s) => {
    const b = document.createElement('button');
    b.type = 'button';
    b.className = s.className;
    b.dataset.filter = s.dataset.filter;
    b.setAttribute('aria-pressed', s.classList.contains('active') ? 'true' : 'false');
    b.textContent = s.textContent;
    s.replaceWith(b);
  });
  const faqStyle = document.createElement('style');
  faqStyle.textContent = '.km-faq__filter-btn{-webkit-appearance:none;appearance:none;margin:0;font:inherit;letter-spacing:inherit;font-size:var(--kc-responsive-label-sm-text-size)}';
  document.body.appendChild(faqStyle);

  // Capture hygiene: hide any fixed cookie-consent panel, whatever its id
  document.querySelectorAll('body *').forEach((el) => {
    if (getComputedStyle(el).position === 'fixed' && /cookie consent/i.test(el.textContent || '') && el.textContent.length < 2000) {
      el.style.setProperty('display', 'none', 'important');
    }
  });
})();
