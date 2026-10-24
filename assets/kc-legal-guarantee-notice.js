/* kc-legal-guarantee-notice.js: the viewer for the EU harmonised notice on the legal guarantee
   (snippets/kc-legal-guarantee-notice.liquid). The line "Your legal guarantee rights" opens a
   native dialog that holds the Commission's unedited notice at a readable width (Astra R58 B2);
   the dialog traps focus, Esc and the close button close it, focus returns to the line. Without
   this script the details element opens the same scrolling region in place. The image is lazy;
   pointing at or focusing the line starts its load so the viewer opens filled. */
(() => {
  'use strict';

  const init = (root) => {
    if (root.dataset.kcLgnReady === '1') return;
    const summary = root.querySelector('[data-kc-lgn-open]');
    const details = root.querySelector('[data-kc-lgn-details]');
    const dialog = root.querySelector('[data-kc-lgn-dialog]');
    const body = root.querySelector('[data-kc-lgn-dialog-body]');
    const figure = root.querySelector('[data-kc-lgn-figure]');
    if (!summary || !details || !dialog || !body || !figure) return;
    if (typeof dialog.showModal !== 'function') return;
    root.dataset.kcLgnReady = '1';

    // The figure lives in the viewer from now on; the dialog body is the one scrolling region
    body.appendChild(figure);
    const scroller = figure.querySelector('[data-kc-lgn-scroller]');
    if (scroller) {
      body.setAttribute('tabindex', '0');
      body.setAttribute('role', 'region');
      body.setAttribute('aria-label', scroller.getAttribute('aria-label') || '');
      scroller.removeAttribute('tabindex');
      scroller.removeAttribute('role');
      scroller.removeAttribute('aria-label');
    }
    details.removeAttribute('open');
    root.classList.add('kc-lgn--viewer');

    const image = figure.querySelector('.kc-lgn__image');
    const preload = () => {
      if (image && image.getAttribute('loading') === 'lazy') image.setAttribute('loading', 'eager');
    };

    const open = (event) => {
      event.preventDefault();
      preload();
      if (!dialog.open) dialog.showModal();
      body.scrollTop = 0;
      body.scrollLeft = 0;
    };

    summary.addEventListener('pointerenter', preload);
    summary.addEventListener('focus', preload);
    summary.addEventListener('click', open);
    summary.addEventListener('keydown', (event) => {
      if (event.key === 'Enter' || event.key === ' ') open(event);
    });

    const close = root.querySelector('[data-kc-lgn-close]');
    if (close) close.addEventListener('click', () => dialog.close());
    // A click on the backdrop lands on the dialog element itself
    dialog.addEventListener('click', (event) => {
      if (event.target === dialog) dialog.close();
    });
    dialog.addEventListener('close', () => summary.focus());
  };

  const initAll = (scope) => {
    scope.querySelectorAll('[data-kc-legal-guarantee-notice]').forEach(init);
  };

  initAll(document);
  document.addEventListener('shopify:section:load', (event) => initAll(event.target));
})();
