if (!customElements.get('kc-gallery-sizing')) {
  customElements.define('kc-gallery-sizing', class extends HTMLElement {
    connectedCallback() {
      this.gallery = this.closest('media-gallery');
      this.anchor = this.gallery.parentElement;
      this.thumbnails = this.gallery.querySelector('[id^="GalleryThumbnails"]');
      this.viewer = this.gallery.querySelector('[id^="GalleryViewer"]');
      this.header = document.querySelector('.section-header');
      this.desktop = window.matchMedia('(min-width: 750px)');
      this.schedule = () => {
        cancelAnimationFrame(this.frame);
        this.frame = requestAnimationFrame(() => this.measure());
      };
      this.observer = new ResizeObserver(this.schedule);
      [this.anchor, this.viewer, this.thumbnails, ...document.querySelectorAll('.shopify-section-group-header-group')]
        .filter(Boolean).forEach((element) => this.observer.observe(element));
      window.addEventListener('resize', this.schedule);
      this.schedule();
    }

    disconnectedCallback() {
      this.observer.disconnect();
      window.removeEventListener('resize', this.schedule);
      cancelAnimationFrame(this.frame);
    }

    measure() {
      if (!this.desktop.matches) return;
      const gap = parseFloat(getComputedStyle(this.gallery).getPropertyValue('--kc-gallery-gap')) || 16;
      const stickyTop = (this.header?.getBoundingClientRect().height || 0) + gap;
      const start = Math.max(this.anchor.getBoundingClientRect().top + window.scrollY, stickyTop);
      this.gallery.style.setProperty('--kc-gallery-start', `${Math.ceil(start)}px`);
      this.gallery.style.setProperty('--kc-gallery-sticky-top', `${Math.ceil(stickyTop)}px`);
      this.gallery.style.setProperty('--kc-gallery-thumbnails-height', `${Math.ceil(this.thumbnails?.getBoundingClientRect().height || 0)}px`);
      this.gallery.style.setProperty('--kc-gallery-media-height', `${this.viewer.getBoundingClientRect().height}px`);
    }
  });
}
