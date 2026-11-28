// Visual alignment per visible card, px from the card top: the radio's centre, and the ink centre of the
// capitals (cap height over the baseline) of the plan name, the price and the struck price. Offsets are
// against the name's cap centre and should be 0. Font metrics from canvas measureText.
(() => {
  const canvas = document.createElement('canvas').getContext('2d');
  const capCentre = (el) => {
    const cs = getComputedStyle(el);
    canvas.font = `${cs.fontWeight} ${cs.fontSize} ${cs.fontFamily}`;
    const m = canvas.measureText('H');
    const ascent = m.fontBoundingBoxAscent;
    const descent = m.fontBoundingBoxDescent;
    const range = document.createRange();
    range.selectNodeContents(el);
    const rect = Array.from(range.getClientRects()).filter((r) => r.height > 0)[0] || el.getBoundingClientRect();
    const lineHeight = parseFloat(cs.lineHeight) || rect.height;
    // The line box of the first line: its top is rect.top minus the half-leading of an inline box
    const half = (lineHeight - (ascent + descent)) / 2;
    const inlineTop = rect.top + rect.height / 2 - (ascent + descent) / 2;
    const baseline = inlineTop + ascent;
    return { centre: baseline - m.actualBoundingBoxAscent / 2, cap: m.actualBoundingBoxAscent, half };
  };
  const box = document.querySelector('.kc-buybox');
  const cards = Array.from(box.querySelectorAll('.loop-one-time-purchase-option-position, .loop-subscription-group')).filter((c) => c.checkVisibility());
  return JSON.stringify(cards.map((card) => {
    const top = card.getBoundingClientRect().top;
    const radio = card.querySelector('input[type=radio]').getBoundingClientRect();
    const name = capCentre(card.querySelector('.loop-one-time-purchase-option-label, .loop-subscription-group-label'));
    const price = capCentre(card.querySelector('.loop-one-time-purchase-option-price-amount, .loop-subscription-group-price-amount'));
    const compare = card.querySelector('.kc-plan-compare');
    const out = {
      card: card.querySelector('.loop-one-time-purchase-option-label, .loop-subscription-group-label').textContent.trim().slice(0, 14),
      nameCap: +(name.centre - top).toFixed(1),
      capHeight: +name.cap.toFixed(1),
      radio: +((radio.top + radio.height / 2) - name.centre).toFixed(1),
      price: +(price.centre - name.centre).toFixed(1),
    };
    if (compare) out.compare = +(capCentre(compare).centre - name.centre).toFixed(1);
    return out;
  }));
})()
