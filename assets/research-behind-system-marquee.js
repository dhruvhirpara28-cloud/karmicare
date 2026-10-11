/*
  Research Behind System — calm infinite marquee (same behaviour as
  assets/trusted-professionals-marquee.js on the professional cards).

  The track drifts left at a slow, constant speed. Instead of stopping dead,
  the speed eases towards its target: hovering (or focusing) a card glides the
  band to a halt so the study can be read, leaving lets it drift off again.
  Cards can be dragged; on release the band keeps the drag momentum and
  settles back to its cruising speed. Off-screen, the loop sleeps.
  With prefers-reduced-motion the band does not move and scrolls natively.
*/
if (!customElements.get('research-behind-system-marquee')) {
  customElements.define(
    'research-behind-system-marquee',
    class ResearchBehindSystemMarquee extends HTMLElement {
      connectedCallback() {
        this.track = this.querySelector('.research-behind-system__track');
        if (!this.track || this.track.children.length === 0) return;

        this.reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
        if (this.reducedMotion.matches) {
          this.classList.add('is-static');
          return;
        }

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

        this.fill();
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
            clone.querySelectorAll('a, button').forEach((el) => el.setAttribute('tabindex', '-1'));
            clone.dataset.marqueeClone = '';
            this.track.appendChild(clone);
          });
        }
        this.offset = this.wrap(this.offset);
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
         so the quote can be read, then it drifts on. */
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
          this.offset = this.wrap(this.offset + this.velocity * dt);
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
