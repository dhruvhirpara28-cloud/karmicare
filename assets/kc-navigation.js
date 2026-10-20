// The floating navigation's controller (assets/kc-navigation.css): measures the announcement bar and
// the navigation for the page clearance, hides the bar on scroll down and brings it back after 10px of
// scrolling up where data-hide-on-scroll is true (product pages). Replaces Dawn's StickyHeader and keeps
// its contract: preventHide (menus), the preventHeaderReveal event (media gallery), --header-height and
// --header-bottom-position(-desktop).
if (!customElements.get('sticky-header')) {
  customElements.define('sticky-header', class extends HTMLElement {
    connectedCallback() {
      this.section = this.closest('.section-header');
      this.bar = this.querySelector('.header');
      if (!this.section || !this.bar) return;
      this.abort = new AbortController();
      this.lastY = this.scrollPosition();
      this.climbed = 0;
      this.preventReveal = false;
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
      // Not clamped at 0: once the announcement bar has scrolled away the value goes negative and
      // kc-navigation.css takes the larger of it and --kc-navigation-floor
      let announcementBottom = null;
      const scrollsWithPage = this.dataset.stickyType === 'none' && this.dataset.hideOnScroll !== 'true';
      this.announcements.forEach(element => {
        if (element.isConnected) {
          const bottom = element.getBoundingClientRect().bottom + (scrollsWithPage ? y : 0);
          announcementBottom = announcementBottom === null ? bottom : Math.max(announcementBottom, bottom);
        }
      });
      // No announcement bar: the top of the page, which scrolls away like the bar would (0 when the
      // navigation scrolls with the page itself)
      if (announcementBottom === null) announcementBottom = scrollsWithPage ? 0 : -y;
      const root = document.documentElement.style;
      root.setProperty('--kc-navigation-top', `${Math.ceil(announcementBottom)}px`);
      const height = Math.ceil(this.section.offsetHeight);
      root.setProperty('--kc-navigation-clearance', `${height}px`);
      root.setProperty('--header-height', `${height}px`);

      if (this.dataset.hideOnScroll === 'true') {
        if (y <= 10) {
          this.shouldHide = false;
          this.climbed = 0;
        } else if (delta > 0 && !this.preventHide && !this.querySelector('predictive-search')?.isOpen) {
          this.shouldHide = true;
          this.climbed = 0;
        } else if (delta < 0) {
          this.climbed -= delta;
          if (this.climbed >= 10 && !this.preventReveal) this.shouldHide = false;
        }
      }
      this.section.classList.toggle('kc-header-autohide--hidden', this.shouldHide);
      this.section.classList.add('kc-header-autohide--ready');
      this.section.classList.toggle('scrolled-past-header', y > height);
      const bottom = Math.max(0, Math.ceil(this.section.getBoundingClientRect().bottom));
      root.setProperty('--header-bottom-position', `${bottom}px`);
      root.setProperty('--header-bottom-position-desktop', `${bottom}px`);
    }

    disconnectedCallback() {
      this.abort?.abort();
      this.observer?.disconnect();
      clearTimeout(this.revealTimer);
      cancelAnimationFrame(this.frame);
      this.frame = 0;
      if (!document.querySelector('sticky-header')) {
        const root = document.documentElement.style;
        ['--kc-navigation-top', '--kc-navigation-clearance', '--header-height',
          '--header-bottom-position', '--header-bottom-position-desktop']
          .forEach(name => root.removeProperty(name));
      }
    }
  });
}
