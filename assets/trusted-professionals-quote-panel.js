/*
  Trusted Professionals — KC/Professional quote panel.

  On mobile each card shows its quote capped at five lines (desktop shows the
  whole quote in the card, so nothing is cut there). When the quote does not
  fit ("Long quote" in the KC library), the card's eye button appears; it
  opens the section's side panel with the portrait, name, title and the full
  quote.
  The panel is a modal <dialog>: focus moves to its close button and returns
  to the eye button on close; Escape, the close button and a click on the
  scrim close it.

  Marquee clones carry data-block-id, so a clone shows the same eye as its
  original and opens the same quote.
*/
if (!customElements.get('trusted-professionals-quotes')) {
  customElements.define(
    'trusted-professionals-quotes',
    class TrustedProfessionalsQuotes extends HTMLElement {
      connectedCallback() {
        this.panel = this.querySelector('.trusted-professionals__panel');
        if (!this.panel || typeof this.panel.showModal !== 'function') return;

        this.panelMedia = this.panel.querySelector('[data-quote-panel-media]');
        this.panelName = this.panel.querySelector('[data-quote-panel-name]');
        this.panelTitle = this.panel.querySelector('[data-quote-panel-title]');
        this.panelQuote = this.panel.querySelector('[data-quote-panel-quote]');

        this.onClick = this.onClick.bind(this);
        this.onPanelClick = this.onPanelClick.bind(this);
        this.onPanelClose = this.onPanelClose.bind(this);
        this.addEventListener('click', this.onClick);
        this.panel.addEventListener('click', this.onPanelClick);
        this.panel.addEventListener('close', this.onPanelClose);

        // Re-check which quotes are cut when a card changes width (breakpoints,
        // fonts loading) or the marquee rebuilds its clones.
        this.resizeObserver = new ResizeObserver(() => this.scheduleMeasure());
        this.originals().forEach((card) => {
          const text = card.querySelector('.trusted-professionals__card-quote-text');
          if (text) this.resizeObserver.observe(text);
        });
        const track = this.querySelector('.trusted-professionals__track');
        if (track) {
          this.mutationObserver = new MutationObserver(() => this.scheduleMeasure());
          this.mutationObserver.observe(track, { childList: true });
        }
        if (document.fonts) document.fonts.ready.then(() => this.scheduleMeasure());
        this.scheduleMeasure();
      }

      disconnectedCallback() {
        this.resizeObserver?.disconnect();
        this.mutationObserver?.disconnect();
        cancelAnimationFrame(this.measureFrame);
        if (this.panel?.open) this.panel.close();
      }

      originals() {
        return Array.from(this.querySelectorAll('.trusted-professionals__card[data-block-id]:not([data-marquee-clone])'));
      }

      scheduleMeasure() {
        cancelAnimationFrame(this.measureFrame);
        this.measureFrame = requestAnimationFrame(() => this.measure());
      }

      /* A quote is long when the five-line clamp hides part of it. The text
         keeps its clamped layout while the holder is folded, so it can be
         measured before the card is hovered. */
      measure() {
        this.originals().forEach((card) => {
          const text = card.querySelector('.trusted-professionals__card-quote-text');
          if (!text) return;
          const long = text.scrollHeight > text.clientHeight + 1;
          this.querySelectorAll(`.trusted-professionals__card[data-block-id="${card.dataset.blockId}"]`).forEach((match) => {
            match.toggleAttribute('data-long-quote', long);
          });
        });
      }

      onClick(event) {
        const eye = event.target.closest('.trusted-professionals__card-eye');
        if (!eye || !this.contains(eye) || this.panel.contains(eye)) return;
        event.preventDefault();
        this.open(eye);
      }

      open(eye) {
        const card = eye.closest('.trusted-professionals__card');
        const text = card?.querySelector('.trusted-professionals__card-quote-text');
        if (!card || !text) return;

        const portrait = card.querySelector('.trusted-professionals__card-image img');
        this.panelMedia.replaceChildren();
        if (portrait) {
          const image = portrait.cloneNode();
          image.removeAttribute('loading');
          image.removeAttribute('id');
          image.alt = '';
          image.sizes = '(min-width: 750px) 384px, 100vw';
          this.panelMedia.append(image);
        }
        this.panelName.textContent = card.querySelector('.trusted-professionals__card-name')?.textContent.trim() || '';
        this.panelTitle.textContent = card.querySelector('.trusted-professionals__card-title')?.textContent.trim() || '';
        this.panelQuote.replaceChildren(...Array.from(text.childNodes, (node) => node.cloneNode(true)));

        this.opener = eye;
        eye.setAttribute('aria-expanded', 'true');
        document.body.classList.add('overflow-hidden');
        this.panel.scrollTop = 0;
        this.panel.showModal();
      }

      close() {
        if (this.panel.open) this.panel.close();
      }

      /* The panel fills the dialog box, so a click that lands on the dialog
         itself is a click on the scrim. */
      onPanelClick(event) {
        if (event.target === this.panel || event.target.closest('[data-quote-panel-close]')) this.close();
      }

      onPanelClose() {
        document.body.classList.remove('overflow-hidden');
        if (this.opener) {
          this.opener.setAttribute('aria-expanded', 'false');
          this.opener.focus({ preventScroll: true });
          this.opener = null;
        }
      }
    }
  );
}
