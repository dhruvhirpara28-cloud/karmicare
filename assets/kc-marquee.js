/*
  KC marquee — calm infinite band, shared by the Trusted Professionals cards
  (sections/trusted-professionals.liquid) and the Research Behind System
  cards (sections/research-behind-system.liquid).

  The track ([data-marquee-track]) drifts left at a slow, constant speed.
  Instead of stopping dead, the speed eases towards its target: hovering (or
  focusing) a card glides the band to a halt so the card can be read, leaving
  lets it drift off again. Cards can be dragged; on release the band keeps
  the drag momentum and settles back to its cruising speed. Off-screen, the
  loop sleeps. With prefers-reduced-motion the band does not move and
  scrolls natively.

  Options on the element:
    data-speed        cruising speed in px per second (default 24)
    data-wheel        a horizontal trackpad swipe or Shift + wheel moves the
                      band the same way as a drag (professionals)
    data-align-start  start with the first card on the page content's left
                      edge, as in Figma (research)
    data-keys         the focused band takes Left/Right (one card), Home and
                      End, so every card can be reached by keyboard (stats)
*/
if (!customElements.get('kc-marquee')) {
  customElements.define(
    'kc-marquee',
    class KcMarquee extends HTMLElement {
      connectedCallback() {
        this.track = this.querySelector('[data-marquee-track]');
        if (!this.track || this.track.children.length === 0) return;

        this.reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
        if (this.reducedMotion.matches) {
          this.classList.add('is-static');
          return;
        }
        // Sections may scroll natively until this class clips the row for the drift
        this.classList.add('is-running');

        this.originals = Array.from(this.track.children);
        this.speed = Number(this.dataset.speed) || 24; // px per second
        this.velocity = 0; // start still, ease in once visible
        this.target = this.speed;
        this.offset = 0;
        this.hovered = false;
        this.focused = false;
        this.touchHold = false;
        this.drag = null;
        this.resumeTimer = null;
        this.wheelPending = 0; // px still to apply from the wheel
        this.wheelAxis = null;
        this.wheelTime = 0;

        this.fill();
        if (this.hasAttribute('data-align-start')) {
          this.offset = this.wrap(-this.contentInset());
          this.render();
        }
        this.bindEvents();

        this.resizeObserver = new ResizeObserver(() => this.fill());
        this.resizeObserver.observe(this);

        this.intersectionObserver = new IntersectionObserver(([entry]) => {
          entry.isIntersecting ? this.start() : this.stop();
        });
        this.intersectionObserver.observe(this);
      }

      disconnectedCallback() {
        this.stop();
        this.resizeObserver?.disconnect();
        this.intersectionObserver?.disconnect();
        clearTimeout(this.resumeTimer);
      }

      /* Clone the set until the track covers the viewport twice, so the
         wrap point is never visible. Clones are hidden from assistive tech. */
      fill() {
        this.track.querySelectorAll('[data-marquee-clone]').forEach((clone) => clone.remove());

        const gap = parseFloat(getComputedStyle(this.track).columnGap) || 0;
        const first = this.originals[0];
        const last = this.originals[this.originals.length - 1];
        this.setWidth = last.offsetLeft + last.offsetWidth - first.offsetLeft + gap;
        if (this.setWidth <= 0) return;

        const copies = Math.ceil((this.offsetWidth * 2) / this.setWidth);
        for (let i = 0; i < copies; i++) {
          this.originals.forEach((card) => {
            const clone = card.cloneNode(true);
            clone.removeAttribute('id');
            // aria-hidden only: `inert` would also block hover, and after a
            // swipe the cards under the cursor are often clones.
            clone.setAttribute('aria-hidden', 'true');
            if (clone.hasAttribute('tabindex')) clone.setAttribute('tabindex', '-1');
            clone.querySelectorAll('a, button, [tabindex]').forEach((el) => el.setAttribute('tabindex', '-1'));
            clone.dataset.marqueeClone = '';
            this.track.appendChild(clone);
          });
        }
        this.offset = this.wrap(this.offset);
      }

      /* Distance from the band's left edge to the page content (the .page-width
         padding box this full-bleed band breaks out of). */
      contentInset() {
        const content = this.parentElement;
        if (!content) return 0;
        const padding = parseFloat(getComputedStyle(content).paddingLeft) || 0;
        return content.getBoundingClientRect().left + padding - this.getBoundingClientRect().left;
      }

      bindEvents() {
        this.addEventListener('pointerenter', (event) => {
          if (event.pointerType !== 'mouse') return;
          this.hovered = true;
          this.updateTarget();
        });
        this.addEventListener('pointerleave', (event) => {
          if (event.pointerType !== 'mouse') return;
          this.hovered = false;
          this.updateTarget();
        });
        this.addEventListener('focusin', () => {
          this.focused = true;
          this.updateTarget();
        });
        this.addEventListener('focusout', () => {
          this.focused = false;
          this.updateTarget();
        });

        this.addEventListener('pointerdown', (event) => this.onPointerDown(event));
        this.addEventListener('pointermove', (event) => this.onPointerMove(event));
        this.addEventListener('pointerup', (event) => this.onPointerUp(event));
        this.addEventListener('pointercancel', (event) => this.onPointerUp(event));
        if (this.hasAttribute('data-wheel')) {
          this.addEventListener('wheel', (event) => this.onWheel(event), { passive: false });
        }
        if (this.hasAttribute('data-keys')) {
          this.addEventListener('keydown', (event) => this.onKeyDown(event));
        }
        this.addEventListener('dragstart', (event) => event.preventDefault());
        this.addEventListener(
          'click',
          (event) => {
            if (this.suppressClick) {
              event.preventDefault();
              event.stopPropagation();
              this.suppressClick = false;
            }
          },
          true
        );
      }

      /* Touch has no hover: a tap holds the band still for a few seconds
         so the card can be read, then it drifts on. */
      updateTarget() {
        clearTimeout(this.resumeTimer);
        this.target = this.hovered || this.focused || this.touchHold ? 0 : this.speed;
      }

      onPointerDown(event) {
        if (event.button !== 0) return;
        this.suppressClick = false;
        this.drag = { id: event.pointerId, x: event.clientX, lastX: event.clientX, lastT: event.timeStamp, moved: false, v: 0 };
        if (event.pointerType !== 'mouse') {
          this.touchHold = true;
          this.updateTarget();
        }
      }

      onPointerMove(event) {
        const drag = this.drag;
        if (!drag || drag.id !== event.pointerId) return;
        if (!drag.moved && Math.abs(event.clientX - drag.x) < 6) return;

        if (!drag.moved) {
          drag.moved = true;
          this.wheelPending = 0;
          this.setPointerCapture(event.pointerId);
          this.classList.add('is-dragging');
        }

        const dx = event.clientX - drag.lastX;
        const dt = Math.max(event.timeStamp - drag.lastT, 1) / 1000;
        this.offset = this.wrap(this.offset - dx);
        drag.v = -dx / dt; // px/s, positive = leftward like the drift
        drag.lastX = event.clientX;
        drag.lastT = event.timeStamp;
        this.render();
      }

      onPointerUp(event) {
        const drag = this.drag;
        if (!drag || drag.id !== event.pointerId) return;
        this.drag = null;
        this.classList.remove('is-dragging');

        if (drag.moved) {
          this.suppressClick = true;
          // Carry the throw, capped so a flick never turns frantic.
          const cap = this.speed * 30;
          this.velocity = Math.max(-cap, Math.min(cap, drag.v));
        }

        if (event.pointerType !== 'mouse') {
          this.resumeTimer = setTimeout(() => {
            this.touchHold = false;
            this.updateTarget();
          }, drag.moved ? 1200 : 4000);
        }
      }

      /* Each wheel gesture locks to the axis it starts on: a vertical page
         scroll that strays sideways is never caught, and a horizontal swipe
         is kept from the browser's back/forward swipe. */
      onWheel(event) {
        if (event.ctrlKey) return; // pinch zoom
        let dx = event.deltaX;
        let dy = event.deltaY;
        if (event.shiftKey && dx === 0) [dx, dy] = [dy, 0];

        if (event.timeStamp - this.wheelTime > 200) this.wheelAxis = null;
        this.wheelTime = event.timeStamp;
        if (!this.wheelAxis) {
          if (dx === 0 && dy === 0) return;
          this.wheelAxis = Math.abs(dx) > Math.abs(dy) ? 'x' : 'y';
        }
        // A clear vertical move hands the gesture back to the page, so a
        // swipe's trailing momentum never blocks the next scroll down.
        if (this.wheelAxis === 'x' && Math.abs(dy) > Math.abs(dx) * 2) this.wheelAxis = 'y';
        if (this.wheelAxis !== 'x' || this.drag?.moved) return;

        event.preventDefault();
        const unit = event.deltaMode === 1 ? 16 : event.deltaMode === 2 ? this.offsetWidth : 1;
        this.wheelPending += dx * unit;
        this.velocity = 0;
      }

      /* Focus already holds the band still. Left/Right line the previous or
         next card up with the page content's left edge, Home brings the first
         card there and End the last card to the right edge. The distance
         glides in through the wheel path. */
      onKeyDown(event) {
        if (event.altKey || event.ctrlKey || event.metaKey || event.shiftKey) return;
        if (!['ArrowLeft', 'ArrowRight', 'Home', 'End'].includes(event.key)) return;
        event.preventDefault();

        const inset = this.contentInset();
        const position = this.offset + this.wheelPending; // where the band is heading
        let target;
        if (event.key === 'Home') {
          target = -inset;
        } else if (event.key === 'End') {
          const last = this.originals[this.originals.length - 1];
          target = last.offsetLeft + last.offsetWidth - (this.offsetWidth - inset);
        } else {
          const starts = Array.from(this.track.children, (card) => card.offsetLeft - inset);
          if (event.key === 'ArrowRight') {
            target = starts.find((start) => start > position + 1);
          } else {
            // Before the first card, look one set further on, where the clones repeat it
            const base = starts.some((start) => start < position - 1) ? position : position + this.setWidth;
            target = starts.filter((start) => start < base - 1).pop() - (base - position);
          }
          if (target === undefined || Number.isNaN(target)) return;
        }

        // Home and End take the shorter way round the loop
        let delta = target - position;
        if (event.key === 'Home' || event.key === 'End') {
          delta = this.wrap(delta);
          if (delta > this.setWidth / 2) delta -= this.setWidth;
        }
        this.velocity = 0;
        this.wheelPending += delta;
      }

      start() {
        if (this.frame) return;
        this.lastTime = performance.now();
        this.frame = requestAnimationFrame((time) => this.tick(time));
      }

      stop() {
        cancelAnimationFrame(this.frame);
        this.frame = null;
      }

      tick(time) {
        const dt = Math.min((time - this.lastTime) / 1000, 0.1);
        this.lastTime = time;

        if (!this.drag || !this.drag.moved) {
          // Exponential easing towards the target speed: a soft glide to a
          // halt on hover (~1s), and an unhurried pick-up afterwards.
          const easing = this.target === 0 ? 3.2 : 1.1;
          this.velocity += (this.target - this.velocity) * (1 - Math.exp(-easing * dt));
          if (Math.abs(this.velocity) < 0.05 && this.target === 0) this.velocity = 0;
          // Wheel distance eases in over a few frames, so a notched mouse
          // wheel glides instead of jumping a card at a time. Without
          // data-wheel nothing is pending and this adds 0.
          let wheel = this.wheelPending * (1 - Math.exp(-20 * dt));
          if (Math.abs(this.wheelPending) < 0.5) wheel = this.wheelPending;
          this.wheelPending -= wheel;
          this.offset = this.wrap(this.offset + this.velocity * dt + wheel);
          this.render();
        }

        this.frame = requestAnimationFrame((t) => this.tick(t));
      }

      wrap(value) {
        if (!this.setWidth) return 0;
        return ((value % this.setWidth) + this.setWidth) % this.setWidth;
      }

      render() {
        this.track.style.transform = `translate3d(${-this.offset}px, 0, 0)`;
      }
    }
  );
}
