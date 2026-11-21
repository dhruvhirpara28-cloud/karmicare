// The floating navigation's controller (assets/kc-navigation.css): measures the announcement bar and
// the navigation for the page clearance, hides the bar 2s after a scroll down began and brings it back
// after 10px of scrolling up where data-hide-on-scroll is true (product pages). Replaces Dawn's
// StickyHeader and keeps its contract: preventHide (menus), the preventHeaderReveal event (media
// gallery), --header-height and --header-bottom-position(-desktop). It does not place the bar:
// position: sticky does, in step with the scroll. What it publishes on the root stays the same while
// the page scrolls, and a value is only written when it changed, so a scroll frame does not restyle
// the page.
if (!customElements.get('sticky-header')) {
  // The bar stays this long after a scroll down began, then slides away (Victor, 21 Nov)
  const HIDE_DELAY_MS = 2000;

  customElements.define('sticky-header', class extends HTMLElement {
    connectedCallback() {
      this.section = this.closest('.section-header');
      this.bar = this.querySelector('.header');
      if (!this.section || !this.bar) return;
      this.abort = new AbortController();
      this.lastY = this.scrollPosition();
      this.climbed = 0;
      this.preventReveal = false;
      this.hiddenTop = -1;
      this.shouldHide = this.dataset.hideOnScroll === 'true' && this.lastY > 10;
      this.schedule = () => {
        if (!this.frame) this.frame = requestAnimationFrame(() => this.update());
      };
      const options = { signal: this.abort.signal, passive: true };
      window.addEventListener('scroll', this.schedule, options);
      window.addEventListener('resize', this.schedule, options);
      window.addEventListener('pageshow', this.schedule, options);
      document.addEventListener('shopify:section:load', () => this.observeSizes(), options);
      document.addEventListener('shopify:section:unload', this.schedule, options);
      this.section.addEventListener('focusin', this.schedule, options);
      this.section.addEventListener('focusout', this.schedule, options);
      this.section.addEventListener('toggle', this.schedule, { signal: this.abort.signal, capture: true });
      // Keep the gallery's existing programmatic-scroll contract.
      this.addEventListener('preventHeaderReveal', () => {
        this.preventReveal = true;
        this.releaseReveal();
      }, options);
      this.section.classList.toggle('kc-header-autohide--hidden', this.shouldHide);
      this.observeSizes();
    }

    scrollPosition() {
      return Math.min(
        Math.max(window.scrollY, 0),
        Math.max(document.documentElement.scrollHeight - window.innerHeight, 0)
      );
    }

    releaseReveal() {
      clearTimeout(this.revealTimer);
      this.revealTimer = setTimeout(() => {
        this.preventReveal = false;
      }, 66);
    }

    // A menu or the search is open: the bar stays
    held() {
      return this.preventHide || this.section.classList.contains('menu-open') ||
        this.querySelector('predictive-search')?.isOpen;
    }

    // One timer per scroll down: later frames of the same scroll do not restart it
    startHide() {
      if (this.shouldHide || this.hideTimer) return;
      this.hideTimer = setTimeout(() => {
        this.hideTimer = 0;
        if (this.held()) return;
        this.shouldHide = true;
        this.schedule();
      }, HIDE_DELAY_MS);
    }

    cancelHide() {
      clearTimeout(this.hideTimer);
      this.hideTimer = 0;
    }

    observeSizes() {
      this.observer?.disconnect();
      this.announcements = Array.from(document.querySelectorAll('.announcement-bar-section'));
      if (window.ResizeObserver) {
        this.observer = new ResizeObserver(this.schedule);
        [this, this.bar, ...this.announcements].forEach(element => this.observer.observe(element));
      }
      this.schedule();
    }

    update() {
      this.frame = 0;
      const y = this.scrollPosition();
      const delta = y - this.lastY;
      this.lastY = y;
      if (this.preventReveal && delta !== 0) this.releaseReveal();
      // The announcement bar's bottom edge on the page, not on screen, so it is its height and the
      // scroll does not change it (0 without a bar, or with an empty one that Dawn hides)
      let announcementBottom = 0;
      this.announcements.forEach(element => {
        const rect = element.getBoundingClientRect();
        if (element.isConnected && rect.height > 0) {
          announcementBottom = Math.max(announcementBottom, rect.bottom + window.scrollY);
        }
      });
      const root = document.documentElement.style;
      const publish = (name, value) => {
        if (root.getPropertyValue(name) !== value) root.setProperty(name, value);
      };
      publish('--kc-navigation-top', `${Math.ceil(announcementBottom)}px`);
      const height = Math.ceil(this.section.offsetHeight);
      publish('--kc-navigation-clearance', `${height}px`);
      publish('--header-height', `${height}px`);

      if (this.dataset.hideOnScroll === 'true') {
        if (y <= 10) {
          this.cancelHide();
          this.shouldHide = false;
          this.climbed = 0;
        } else if (delta > 0 && !this.held()) {
          this.startHide();
          this.climbed = 0;
        } else if (delta < 0) {
          this.cancelHide();
          this.climbed -= delta;
          if (this.climbed >= 10 && !this.preventReveal) this.shouldHide = false;
        }
      }
      // How far from the top of the screen the section sits as it hides: the bar slides that far and
      // its own height (kc-navigation.css). Written when a hide begins, so the slide's end does not
      // move during the slide, and again only if the hidden section has moved further down.
      if (this.shouldHide) {
        const top = Math.max(0, Math.ceil(this.section.offsetTop - window.scrollY));
        const hiding = !this.section.classList.contains('kc-header-autohide--hidden');
        if (hiding || top > this.hiddenTop) {
          this.hiddenTop = top;
          this.section.style.setProperty('--kc-navigation-y', `${top}px`);
        }
      }
      this.section.classList.toggle('kc-header-autohide--hidden', this.shouldHide);
      this.section.classList.add('kc-header-autohide--ready');
      this.section.classList.toggle('scrolled-past-header', y > height);
      const bottom = Math.max(0, Math.ceil(this.section.getBoundingClientRect().bottom));
      publish('--header-bottom-position', `${bottom}px`);
      publish('--header-bottom-position-desktop', `${bottom}px`);
    }

    disconnectedCallback() {
      this.abort?.abort();
      this.observer?.disconnect();
      clearTimeout(this.revealTimer);
      this.cancelHide();
      cancelAnimationFrame(this.frame);
      this.frame = 0;
      this.section?.style.removeProperty('--kc-navigation-y');
      if (!document.querySelector('sticky-header')) {
        const root = document.documentElement.style;
        ['--kc-navigation-top', '--kc-navigation-clearance', '--header-height',
          '--header-bottom-position', '--header-bottom-position-desktop']
          .forEach(name => root.removeProperty(name));
      }
    }
  });
}
