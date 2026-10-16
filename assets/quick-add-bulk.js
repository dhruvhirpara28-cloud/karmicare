if (!customElements.get('quick-add-bulk')) {
  customElements.define(
    'quick-add-bulk',
    class QuickAddBulk extends BulkAdd {
      constructor() {
        super();
        this.quantity = this.querySelector('quantity-input');

        const debouncedOnChange = debounce((event) => {
          if (parseInt(event.target.value) === 0) {
            this.startQueue(event.target.dataset.index, parseInt(event.target.value));
          } else {
            this.validateQuantity(event);
          }
        }, ON_CHANGE_DEBOUNCE_TIMER);

        // A changed quantity counts as pending from the change on, through the debounce, until it is sent
        // (updateMultipleQty), so an earlier request does not go on to checkout without it (as quick-order-list.js)
        this.addEventListener('change', (event) => {
          this.hasPendingQuantityUpdate = true;
          debouncedOnChange(event);
        });
        this.listenForActiveInput();
        this.listenForKeydown();
        this.lastActiveInputId = null;
      }

      connectedCallback() {
        this.cartUpdateUnsubscriber = subscribe(PUB_SUB_EVENTS.cartUpdate, (event) => {
          if (
            event.source === 'quick-add' ||
            (event.cartData.items && !event.cartData.items.some((item) => item.id === parseInt(this.dataset.index))) ||
            (event.cartData.variant_id && !(event.cartData.variant_id === parseInt(this.dataset.index)))
          ) {
            return;
          }
          // If its another section that made the update
          this.onCartUpdate().then(() => {
            this.listenForActiveInput();
            this.listenForKeydown();
          });
        });
      }

      disconnectedCallback() {
        if (this.cartUpdateUnsubscriber) {
          this.cartUpdateUnsubscriber();
        }
      }

      get input() {
        return this.querySelector('quantity-input input');
      }

      selectProgressBar() {
        return this.querySelector('.progress-bar-container');
      }

      listenForActiveInput() {
        if (!this.classList.contains('hidden')) {
          this.input?.addEventListener('focusin', (event) => event.target.select());
        }
        this.isEnterPressed = false;
      }

      listenForKeydown() {
        this.input?.addEventListener('keydown', (event) => {
          if (event.key === 'Enter') {
            this.input?.blur();
            this.isEnterPressed = true;
          }
        });
      }

      cleanErrorMessageOnType(event) {
        event.target.addEventListener(
          'keypress',
          () => {
            event.target.setCustomValidity('');
          },
          { once: true }
        );
      }

      get sectionId() {
        if (!this._sectionId) {
          this._sectionId = this.closest('.collection-quick-add-bulk').dataset.id;
        }

        return this._sectionId;
      }

      onCartUpdate() {
        return new Promise((resolve, reject) => {
          fetch(`${this.getSectionsUrl()}?section_id=${this.sectionId}`)
            .then((response) => response.text())
            .then((responseText) => {
              const html = new DOMParser().parseFromString(responseText, 'text/html');
              const sourceQty = html.querySelector(`#quick-add-bulk-${this.dataset.index}-${this.sectionId}`);
              if (sourceQty) {
                this.innerHTML = sourceQty.innerHTML;
              }
              resolve();
            })
            .catch((e) => {
              console.error(e);
              reject(e);
            });
        });
      }

      getSectionsUrl() {
        const pageParams = new URLSearchParams(window.location.search);
        const pageNumber = decodeURIComponent(pageParams.get('page') || '');

        return `${window.location.pathname}${pageNumber ? `?page=${pageNumber}` : ''}`;
      }

      updateMultipleQty(items) {
        if (this.queue.length === 0) this.hasPendingQuantityUpdate = false;
        this.selectProgressBar().classList.remove('hidden');

        const ids = Object.keys(items);
        const linesUpdate = this.startCartLinesUpdate(items);
        const body = JSON.stringify({
          updates: items,
          sections: this.getSectionsToRender().map((section) => section.section),
          sections_url: this.getSectionsUrl(),
        });

        fetch(`${routes.cart_update_url}`, { ...fetchConfig(), ...{ body } })
          .then((response) => response.json())
          .then((parsedState) => {
            if (parsedState.errors) {
              throw Object.assign(new Error(parsedState.errors), { code: 'INVALID' });
            }

            linesUpdate?.resolve(parsedState);
            this.renderSections(parsedState, ids);
            publish(PUB_SUB_EVENTS.cartUpdate, { source: 'quick-add', cartData: parsedState });
            // No theme cart (Victor, 16 Oct; layout/theme.liquid): once no quantity is waiting (queued or still
            // in its debounce), on to /cart, which sends a cart with lines to checkout and an empty one to the
            // product page (sections/kc-cart-redirect.liquid)
            if (this.queue.length === 0 && !this.hasPendingQuantityUpdate) window.location.href = routes.cart_url;
          })
          .catch((e) => {
            if (e.code !== 'INVALID') console.error(e);
            this.dispatchCartErrorEvent(
              e.code === 'INVALID' ? e.message : window.cartStrings.error,
              e.code || 'SERVICE_UNAVAILABLE'
            );
            linesUpdate?.reject(e);
            // Commented out for now and will be fixed when BE issue is done https://github.com/Shopify/shopify/issues/440605
            // e.target.setCustomValidity(error);
            // e.target.reportValidity();
            // this.resetQuantityInput(ids[index]);
            // this.selectProgressBar().classList.add('hidden');
            // e.target.select();
            // this.cleanErrorMessageOnType(e);
          })
          .finally(() => {
            this.selectProgressBar().classList.add('hidden');
            this.setRequestStarted(false);
          });
      }

      getSectionsToRender() {
        return [
          {
            id: `quick-add-bulk-${this.dataset.index}-${this.sectionId}`,
            section: this.sectionId,
            selector: `#quick-add-bulk-${this.dataset.index}-${this.sectionId}`,
          },
        ];
      }

      renderSections(parsedState, ids) {
        const intersection = this.queue.filter((element) => ids.includes(element.id));
        if (intersection.length !== 0) return;
        this.getSectionsToRender().forEach((section) => {
          const sectionElement = document.getElementById(section.id);
          const elementToReplace =
            sectionElement && sectionElement.querySelector(section.selector)
              ? sectionElement.querySelector(section.selector)
              : sectionElement;
          if (elementToReplace) {
            elementToReplace.innerHTML = this.getSectionInnerHTML(
              parsedState.sections[section.section],
              section.selector
            );
          }
        });

        if (this.isEnterPressed) {
          this.querySelector(`#Quantity-${this.lastActiveInputId}`).select();
        }

        this.listenForActiveInput();
        this.listenForKeydown();
      }
    }
  );
}
