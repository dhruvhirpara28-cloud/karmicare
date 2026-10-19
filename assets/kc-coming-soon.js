/* "Coming soon" links (snippets/kc-coming-soon.liquid): a tap toggles the tooltip (touch has no
   hover), a tap elsewhere closes it, Escape hides it until the pointer or focus leaves the link.
   Several sections load this file; it binds its document listeners once. */
(() => {
  if (window.kcComingSoonBound) return;
  window.kcComingSoonBound = true;

  const items = () => document.querySelectorAll('.kc-coming-soon');

  document.addEventListener('click', (event) => {
    const item = event.target.closest('.kc-coming-soon');
    items().forEach((other) => {
      if (other !== item) other.classList.remove('is-open');
    });
    if (item) {
      item.classList.remove('is-dismissed');
      item.classList.toggle('is-open');
    }
  });

  document.addEventListener('keydown', (event) => {
    if (event.key !== 'Escape') return;
    items().forEach((item) => {
      item.classList.remove('is-open');
      if (item.matches(':hover, :focus-visible')) item.classList.add('is-dismissed');
    });
  });

  const undismiss = (event) => {
    const item = event.target.closest && event.target.closest('.kc-coming-soon');
    if (item && !item.contains(event.relatedTarget)) item.classList.remove('is-dismissed');
  };
  document.addEventListener('pointerout', undismiss);
  document.addEventListener('focusout', undismiss);
})();
