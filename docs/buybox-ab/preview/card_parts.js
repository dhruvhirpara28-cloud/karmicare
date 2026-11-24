// Height of each visible card and of its parts (px): padding, sub-row, chips row, badge row
(() => {
  const h = (el) => (el && el.checkVisibility() ? Math.round(el.getBoundingClientRect().height) : 0);
  const box = document.querySelector('.kc-buybox');
  const cards = Array.from(box.querySelectorAll('.loop-one-time-purchase-option-position, .loop-subscription-group')).filter((c) => c.checkVisibility());
  const head = box.querySelector('.loop-purchase-options-label').getBoundingClientRect();
  const trust = box.querySelector('.icon-with-text').getBoundingClientRect();
  return JSON.stringify({
    plansHeaderToTrustRow: Math.round(trust.bottom - head.top),
    cards: cards.map((card) => {
      const inner = card.matches('.loop-subscription-group') ? card : card.querySelector('.loop-one-time-purchase-option');
      const cs = getComputedStyle(inner);
      return {
        card: card.querySelector('.loop-one-time-purchase-option-label, .loop-subscription-group-label').textContent.trim().slice(0, 18),
        total: h(card),
        padding: Math.round(parseFloat(cs.paddingTop) + parseFloat(cs.paddingBottom)),
        subRow: h(card.querySelector('.kc-plan-subrow')),
        chips: h(card.querySelector('.kc-return_care-tooltip')),
        badgeRow: h(card.querySelector('.kc-plan-badge')) || h(card.querySelector('.kc-bottom_label')),
      };
    }),
  });
})()
