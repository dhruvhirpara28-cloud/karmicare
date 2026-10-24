// Hero animation fit (Victor, 24 Oct: "zo groot als past, tot 1,5"; R51 formula). The whole-animation
// alpha union on the 540x480 canvas, as fractions of the fitted media height H (the 9:8 media fills the
// frame's height from 750 px, centred): x 51 to 485 and y 28 to 420, with the floor shadow reference at
// 87.1% landing 1rem (10px) below the frame (B).
const KC_HERO_UNION = {
  left: (0.5 - 51 / 540) * 1.125, // 0.45625
  right: (485 / 540 - 0.5) * 1.125, // 215/480
  top: 0.871 - 28 / 480,
  bottom: 420 / 480 - 0.871,
  landedTop: 0.871 - 80 / 480 // the last frame's top, which must stay below the header
};
const KC_HERO_CLEARANCE = 16;
const KC_HERO_MIN = 1.2;
const KC_HERO_MAX = 1.5;

if (!customElements.get('kc-gallery-sizing')) {
  customElements.define('kc-gallery-sizing', class extends HTMLElement {
    connectedCallback() {
      this.gallery = this.closest('media-gallery');
      this.anchor = this.gallery.parentElement;
      this.thumbnails = this.gallery.querySelector('[id^="GalleryThumbnails"]');
      this.viewer = this.gallery.querySelector('[id^="GalleryViewer"]');
      this.header = document.querySelector('.section-header');
      this.headerGroup = [...document.querySelectorAll('.shopify-section-group-header-group')];
      this.info = this.gallery.closest('.product')?.querySelector('.product__info-container');
      this.hero = this.gallery.querySelector('.product__media-item kc-hero-animation');
      this.desktop = window.matchMedia('(min-width: 750px)');
      this.schedule = () => {
        cancelAnimationFrame(this.frame);
        this.frame = requestAnimationFrame(() => this.measure());
      };
      this.observer = new ResizeObserver(this.schedule);
      [this.anchor, this.viewer, this.thumbnails, this.info, ...this.headerGroup]
        .filter(Boolean).forEach((element) => this.observer.observe(element));
      window.addEventListener('resize', this.schedule);
      document.fonts?.ready.then(this.schedule);
      this.schedule();
    }

    disconnectedCallback() {
      this.observer.disconnect();
      window.removeEventListener('resize', this.schedule);
      cancelAnimationFrame(this.frame);
    }

    measure() {
      if (!this.desktop.matches) {
        this.write('--kc-hero-scale', null);
        this.gallery.toggleAttribute('data-kc-hero-fit', false);
        return;
      }
      // Read everything first, then write only what changed
      const gap = parseFloat(getComputedStyle(this.gallery).getPropertyValue('--kc-gallery-gap')) || 16;
      const stickyTop = (this.header?.getBoundingClientRect().height || 0) + gap;
      const anchorTop = this.anchor.getBoundingClientRect().top + window.scrollY;
      const start = Math.max(anchorTop, stickyTop);
      const thumbnailsHeight = this.thumbnails?.getBoundingClientRect().height || 0;
      const viewerRect = this.viewer.getBoundingClientRect();
      const scale = this.hero ? this.heroScale(viewerRect, anchorTop) : null;

      this.write('--kc-gallery-start', `${Math.ceil(start)}px`);
      this.write('--kc-gallery-sticky-top', `${Math.ceil(stickyTop)}px`);
      this.write('--kc-gallery-thumbnails-height', `${Math.ceil(thumbnailsHeight)}px`);
      this.write('--kc-gallery-media-height', `${viewerRect.height}px`);
      this.write('--kc-hero-scale', scale);
      this.gallery.toggleAttribute('data-kc-hero-fit', scale !== null);
    }

    // The largest scale up to 1.5 at which the whole animation keeps 16px clear of the viewport's four
    // edges and the buybox content box. The top is the viewport's, not the header's: the intro may
    // pass briefly behind the header, the landed frame stays below it (Victor, 24 Oct). Measured on the
    // static layout at scroll 0: page positions, not the sticky pin. Below 1.2 there is no scale, and
    // the CSS keeps the R50 pose inside the frame.
    heroScale(viewerRect, anchorTop) {
      const m = KC_HERO_CLEARANCE;
      const H = viewerRect.height;
      if (!(H > 0)) return null;
      const galleryTop = this.gallery.getBoundingClientRect().top;
      const frameTop = anchorTop + (viewerRect.top - galleryTop);
      const B = frameTop + H + 10;
      const C = viewerRect.left + viewerRect.width / 2;
      const viewportWidth = document.documentElement.clientWidth;
      const viewportHeight = document.documentElement.clientHeight;
      const headerBottom = this.headerGroup.reduce((sum, section) => sum + section.getBoundingClientRect().height, 0);
      let buyboxLeft = viewportWidth;
      if (this.info) {
        const style = getComputedStyle(this.info);
        buyboxLeft = this.info.getBoundingClientRect().left + parseFloat(style.paddingLeft) + parseFloat(style.borderLeftWidth);
      }
      const fit = Math.min(
        (C - m) / (KC_HERO_UNION.left * H),
        (Math.min(buyboxLeft, viewportWidth) - m - C) / (KC_HERO_UNION.right * H),
        (B - m) / (KC_HERO_UNION.top * H),
        (B - headerBottom) / (KC_HERO_UNION.landedTop * H),
        (viewportHeight - m - B) / (KC_HERO_UNION.bottom * H)
      );
      // A small margin under the mathematical maximum, on a 0.01 step so subpixel resizes write nothing
      const scale = Math.min(KC_HERO_MAX, Math.floor((fit - 0.005) * 100) / 100);
      return scale >= KC_HERO_MIN ? scale.toFixed(2) : null;
    }

    write(property, value) {
      const current = this.gallery.style.getPropertyValue(property);
      if (value === null) {
        if (current) this.gallery.style.removeProperty(property);
      } else if (current !== value) {
        this.gallery.style.setProperty(property, value);
      }
    }
  });
}
