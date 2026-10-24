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
const KC_HERO_CLEARANCE = 16; // sides, buybox and bottom
const KC_HERO_TOP_CLEARANCE = 16; // the intro's distance from the viewport's top edge
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
      // At once, not in a frame: the CSS keeps the hero hidden from 750 until data-kc-hero-ready,
      // so the first pose it shows is the final one (R52 B1)
      this.measure();
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
        this.gallery.toggleAttribute('data-kc-hero-ready', true);
        return;
      }
      // Sizing first: read, then write only what changed
      const gap = parseFloat(getComputedStyle(this.gallery).getPropertyValue('--kc-gallery-gap')) || 16;
      const stickyTop = (this.header?.getBoundingClientRect().height || 0) + gap;
      const anchorTop = this.anchor.getBoundingClientRect().top + window.scrollY;
      const start = Math.max(anchorTop, stickyTop);
      const thumbnailsHeight = this.thumbnails?.getBoundingClientRect().height || 0;
      const viewerHeight = this.viewer.getBoundingClientRect().height;
      this.write('--kc-gallery-start', `${Math.ceil(start)}px`);
      this.write('--kc-gallery-sticky-top', `${Math.ceil(stickyTop)}px`);
      this.write('--kc-gallery-thumbnails-height', `${Math.ceil(thumbnailsHeight)}px`);
      this.write('--kc-gallery-media-height', `${viewerHeight}px`);
      // Then the fit, on the viewer those values give, in the same pass: no second correction (R52 B1)
      const scale = this.hero ? this.heroScale(this.viewer.getBoundingClientRect(), anchorTop, stickyTop) : null;
      // A script later than the CSS's 1s reveal finds the hero shown in the R50 pose: it fades out,
      // takes the fit while hidden and fades back, rather than jumping
      const late = !this.gallery.hasAttribute('data-kc-hero-ready') && scale !== null && this.hero &&
        parseFloat(getComputedStyle(this.hero).opacity) > 0.5;
      this.gallery.toggleAttribute('data-kc-hero-ready', true);
      if (late) {
        this.gallery.setAttribute('data-kc-hero-swap', '');
        setTimeout(() => {
          this.write('--kc-hero-scale', scale);
          this.gallery.toggleAttribute('data-kc-hero-fit', true);
          this.gallery.removeAttribute('data-kc-hero-swap');
        }, 260);
        return;
      }
      if (this.gallery.hasAttribute('data-kc-hero-swap')) return;
      this.write('--kc-hero-scale', scale);
      this.gallery.toggleAttribute('data-kc-hero-fit', scale !== null);
    }

    // The largest scale up to 1.5 at which the whole animation keeps 16px clear of the viewport's four
    // edges and the buybox content box. The top is the viewport's, not the header's: the intro may
    // pass briefly behind the header, the landed frame stays below it (Victor, 24 Oct). Measured on
    // page positions, not the current scroll, for both the gallery's place at scroll 0 and its sticky
    // pin, whichever sits higher, so the scale holds while scrolling (R52 B2). Below 1.2 there is no
    // scale, and the CSS keeps the R50 pose inside the frame.
    heroScale(viewerRect, anchorTop, stickyTop) {
      const m = KC_HERO_CLEARANCE;
      const H = viewerRect.height;
      if (!(H > 0)) return null;
      const viewerOffset = viewerRect.top - this.gallery.getBoundingClientRect().top;
      const B = anchorTop + viewerOffset + H + 10; // the shadow reference at scroll 0
      const pinnedB = stickyTop + viewerOffset + H + 10; // the same, pinned
      const highestB = Math.min(B, pinnedB);
      const C = viewerRect.left + viewerRect.width / 2;
      const viewportWidth = document.documentElement.clientWidth;
      const viewportHeight = document.documentElement.clientHeight;
      const headerGroupBottom = this.headerGroup.reduce((sum, section) => sum + section.getBoundingClientRect().height, 0);
      const headerBottom = this.header?.getBoundingClientRect().height || 0; // the sticky header alone, when pinned
      let buyboxLeft = viewportWidth;
      if (this.info) {
        const style = getComputedStyle(this.info);
        buyboxLeft = this.info.getBoundingClientRect().left + parseFloat(style.paddingLeft) + parseFloat(style.borderLeftWidth);
      }
      const fit = Math.min(
        (C - m) / (KC_HERO_UNION.left * H),
        (Math.min(buyboxLeft, viewportWidth) - m - C) / (KC_HERO_UNION.right * H),
        (highestB - KC_HERO_TOP_CLEARANCE) / (KC_HERO_UNION.top * H),
        (B - headerGroupBottom) / (KC_HERO_UNION.landedTop * H),
        (pinnedB - headerBottom) / (KC_HERO_UNION.landedTop * H),
        (viewportHeight - m - Math.max(B, pinnedB)) / (KC_HERO_UNION.bottom * H)
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
