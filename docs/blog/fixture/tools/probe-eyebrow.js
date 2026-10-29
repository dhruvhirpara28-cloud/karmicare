location.protocol !== 'https:' ? 'BLANK' : JSON.stringify(Array.from(document.querySelectorAll('.kc-caption-subheading, .subtitle-item')).filter((e) => e.getBoundingClientRect().width > 0).slice(0, 8).map((e) => {
  // The homepage's section eyebrows as they render: classes, font, size, spacing, colour, opacity
  const c = getComputedStyle(e);
  const next = e.nextElementSibling || (e.parentElement && e.parentElement.nextElementSibling);
  return {
    text: e.textContent.trim().slice(0, 40),
    cls: String(e.className).slice(0, 80),
    section: (e.closest('.shopify-section') || {}).id,
    ff: c.fontFamily.slice(0, 30), fs: c.fontSize, lh: c.lineHeight, fw: c.fontWeight, ls: c.letterSpacing, tt: c.textTransform,
    color: c.color, opacity: c.opacity, mb: c.marginBottom,
    gapToNext: next ? Math.round(next.getBoundingClientRect().top - e.getBoundingClientRect().bottom) : null,
  };
}))
