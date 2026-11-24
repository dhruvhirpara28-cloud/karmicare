(() => {
  const pid = '15977093923197';
  const c = document.querySelector('#loop-subscription-container-' + pid);
  const fs = c && c.querySelector('#loop-selling-plan-fieldset');
  const vis = (el) => !!el && el.checkVisibility ? el.checkVisibility() : !!(el && el.offsetParent);
  const cards = fs ? Array.from(fs.querySelectorAll('.loop-one-time-purchase-option-position, .loop-subscription-group'))
    .filter(vis)
    .map((el) => {
      const r = el.getBoundingClientRect();
      const radio = el.querySelector('input[type=radio]');
      return { cls: el.className.split(' ')[0], top: Math.round(r.top + scrollY), h: Math.round(r.height), checked: !!(radio && radio.checked),
        text: el.innerText.replace(/\s+/g, ' ').trim().slice(0, 160) };
    }) : [];
  const link = document.querySelector('#kc-try-once-container-' + pid);
  const cta = document.querySelector('.kc-buybox .kc-cta-label');
  const summary = document.querySelector('.kc-pricing-summary[id^="kc-pricing-summary-"]');
  return JSON.stringify({
    href: location.href, lang: document.documentElement.lang, mode: document.body.className.match(/(day|night)-mode/)?.[0],
    w: innerWidth, layout: link && link.dataset.kcOnceLayout, onceCardClass: !!(c && c.classList.contains('kc-once-card')),
    linkShown: vis(link), cta: cta && cta.textContent.trim(), summary: summary && vis(summary) ? summary.innerText.replace(/\s+/g, ' ').trim() : null,
    sellingPlan: document.querySelector('#product-form-' + (summary && summary.dataset.sectionId) + ' [name=selling_plan]')?.value ?? null,
    loopGroup: window.loopProps && window.loopProps[pid] && window.loopProps[pid].sellingPlanGroupId,
    sticky: (document.querySelector('[data-sc-field="title"], .sc-title') || {}).textContent || null,
    cards,
  });
})()
