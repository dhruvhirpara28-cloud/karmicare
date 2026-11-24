// The visible buybox below the plan cards, block by block: receipt rows, CTA, and what follows, in order
(() => {
  const box = document.querySelector('.kc-buybox');
  const fieldset = box.querySelector('#loop-selling-plan-fieldset');
  const container = fieldset.closest('.loop-subscription-container');
  const out = [];
  let after = false;
  const walk = (el) => {
    Array.from(el.children).forEach((child) => {
      if (child === container || child.contains(container)) {
        if (child === container) {
          after = true;
          return;
        }
        walk(child);
        return;
      }
      if (!after || !child.checkVisibility()) return;
      const text = child.innerText.replace(/[ \t]+/g, ' ').replace(/\n\s*\n+/g, '\n').trim();
      if (text) out.push('[' + (child.id || String(child.className).split(' ').slice(0, 2).join('.') || child.tagName) + ']\n' + text);
    });
  };
  walk(box);
  return out.join('\n---\n');
})()
