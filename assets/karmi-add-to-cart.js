(function () {
  'use strict';

  window.karmiAddToCart = async function (form, buttonElement, options) {
    if (!form) return;

    if (buttonElement) {
      buttonElement.disabled = true;
      buttonElement.classList.add('loading');
      const customSpinner = buttonElement.querySelector('.loading__spinner');
      if (customSpinner) customSpinner.classList.remove('hidden');
    }

    try {
      const previousError = (form.closest('product-form') || document).querySelector('.product-form__error-message-wrapper');
      if (previousError) previousError.hidden = true;

      const variantIdInput = form.querySelector('[name="id"]');
      const variantId = variantIdInput ? variantIdInput.value : null;
      if (!variantId) throw new Error('No variant ID found');

      // Try Once (assets/kc-plan-select.js) buys one time, whatever the page's Loop widget has selected.
      const isFixedOneTime = Boolean(options && options.oneTime);

      // A fixed offer (the end CTA) passes the plan it shows and buys exactly that plan,
      // whatever the page's Loop widget has selected.
      const fixedSellingPlanId = !isFixedOneTime && options && options.sellingPlanId ? String(options.sellingPlanId) : null;

      const sellingPlanInput = form.querySelector('[name="selling_plan"]') || document.querySelector('input[name="selling_plan"]');
      let sellingPlanId = fixedSellingPlanId || (sellingPlanInput ? sellingPlanInput.value : null);

      // Check Loop selection: if One-Time purchase is selected, ensure sellingPlanId is cleared
      const selectedLoopOption = (isFixedOneTime || fixedSellingPlanId) ? null :
                                 document.querySelector('input[name="loop_purchase_option"]:checked') ||
                                 document.querySelector('#loop-selling-plan-fieldset input[type="radio"]:checked');
      // By Loop's one-time ID, not by name: a plan renamed to contain "one time" stays a subscription
      const isLoopOneTime = isFixedOneTime || selectedLoopOption && (
        selectedLoopOption.dataset.id === 'loop-one-time-purchase' ||
        selectedLoopOption.classList.contains('loop-one-time-purchase-option-radio')
      );

      if (isLoopOneTime) {
        sellingPlanId = null;
      }

      const isSubscription = Boolean(!isLoopOneTime && sellingPlanId && !isNaN(parseInt(sellingPlanId)) && parseInt(sellingPlanId) > 0);

      // Never the wrong plan (assets/kc-plan-select.js): a subscription is selected but the form lost its
      // plan, or the plan is one this page must not sell (a legacy plan). Buy nothing rather than that.
      if (selectedLoopOption && !isLoopOneTime && !isSubscription) {
        throw new Error('a subscription is selected but the form holds no selling plan');
      }
      if (isSubscription && window.KCPlanSelect && !window.KCPlanSelect.allowed(sellingPlanId)) {
        throw new Error('selling plan ' + sellingPlanId + ' is not offered on this page');
      }

      const productId = form.dataset.loopProductId || (window.KCPlanSelect ? window.KCPlanSelect.productIdOfVariant(variantId) : '');

      // A plan product's subscription adds its plan's Duos per delivery (year plans: theme setting "Year
      // plans: Duos per delivery"); one time (Try Once) and other products keep the form's quantity
      const quantityInput = form.querySelector('[name="quantity"]');
      const formQuantity = quantityInput ? parseInt(quantityInput.value) || 1 : 1;
      const quantity = window.KCPlanSelect
        ? window.KCPlanSelect.quantityFor(productId, isSubscription ? sellingPlanId : '', formQuantity)
        : formQuantity;

      const mainItem = { id: parseInt(variantId), quantity: quantity };
      if (isSubscription) {
        mainItem.selling_plan = parseInt(sellingPlanId);
      }

      const items = [mainItem];

      // One purchase choice per plan product (assets/kc-plan-select.js replaceChoice): the product's earlier
      // lines (any plan or one time) and every Welcome Kit line go first, so switching plans or to Try
      // Once never leaves two memberships or two kit sets in the cart
      const replacesChoice = Boolean(window.KCPlanSelect && productId && window.KCPlanSelect.manages(productId));

      // Free Welcome Kit product is ONLY added for subscriptions
      if (isSubscription && options && options.isBundleProduct && !options.customerAlreadyReceivedFreeProduct && options.welcomeKitVariantIds && options.welcomeKitVariantIds.length > 0) {
        // After the clear above the cart holds no kit line: add exactly one set
        const existingDrawerVariants = replacesChoice ? [] : Array.from(document.querySelectorAll('cart-drawer [data-variant-id], cart-items [data-variant-id]')).map(el => parseInt(el.dataset.variantId)).filter(Boolean);

        for (const vid of options.welcomeKitVariantIds) {
          const pVid = parseInt(vid);
          if (!existingDrawerVariants.includes(pVid)) {
            items.push({
              id: pVid,
              quantity: 1,
              properties: { '_welcome_kit': 'true' }
            });
          }
        }
      }

      // Cart and checkout order: the plan line on top of its kit (assets/kc-plan-select.js addOrder sends the
      // kit lines first, the plan line last)
      const addPayload = { items: window.KCPlanSelect ? window.KCPlanSelect.addOrder(items) : items.slice().reverse() };

      if (isSubscription) {
        // Loop Loyalty awards Care Credit by this exact value ("60-Day Supply", "Year Supply"): from the
        // selling plan ID (assets/kc-plan-select.js), never from the visible plan name
        const subTitle = window.KCPlanSelect ? window.KCPlanSelect.subscriptionName(sellingPlanId) : '';
        if (subTitle) {
          addPayload.attributes = { 'Subscription Name': subTitle };
        }
      }

      const addToCart = () => fetch('/cart/add.js', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-Karmi-Sync': 'false' },
        body: JSON.stringify(addPayload),
      });
      const redirect = Boolean(options && options.redirectToCheckout);
      const checkoutUrl = (isSubscription && items.length > 1) ? '/checkout?discount=Welcome%20Kit' : '/checkout';

      // The cart's "Subscription Name" follows the subscriptions now in it: a one-time order never keeps
      // an earlier subscription's value (assets/kc-plan-select.js)
      const syncSubscriptionName = async () => {
        if (!window.KCPlanSelect) return;
        try {
          await window.KCPlanSelect.syncCartSubscriptionName(isSubscription ? sellingPlanId : null);
        } catch (e) { console.warn('[KarmiAddToCart] Subscription Name sync failed', e); }
      };

      // One replacement at a time (assets/kc-plan-select.js replaceChoice): the sync and the way to
      // checkout run in the same turn, only the last of several quick choices goes to checkout, and a
      // failed add puts the earlier choice back
      const addRes = replacesChoice
        ? await window.KCPlanSelect.replaceChoice(productId, isSubscription ? sellingPlanId : '', addToCart, async () => {
            await syncSubscriptionName();
            return redirect ? checkoutUrl : null;
          })
        : await addToCart();
      if (!addRes.ok) {
        const rejection = await addRes.json().catch(() => ({}));
        const error = new Error('Cart add failed');
        // Shopify's own message for the shopper ("only 2 left", …), else the theme's cart error
        error.shopperMessage = rejection.description || rejection.message || '';
        throw error;
      }
      if (addRes.kcNavigating) return;
      if (!replacesChoice) await syncSubscriptionName();

      if (redirect) {
        if (!replacesChoice) {
          window.location.href = checkoutUrl;
          return;
        }
        // A later choice came in meanwhile: that one goes to checkout, this one stops here
        if (buttonElement) {
          buttonElement.disabled = false;
          buttonElement.removeAttribute('disabled');
          buttonElement.removeAttribute('aria-disabled');
          buttonElement.classList.remove('loading');
          const customSpinner = buttonElement.querySelector('.loading__spinner');
          if (customSpinner) customSpinner.classList.add('hidden');
        }
      } else {
        if (items.length > 1) {
          try {
            await fetch('/cart/update.js', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json', 'X-Karmi-Sync': 'false' },
              body: JSON.stringify({ discount: 'Welcome Kit' })
            });
          } catch (e) { console.error('Cart discount update failed', e); }
        }

        if (buttonElement) {
          buttonElement.disabled = false;
          buttonElement.removeAttribute('disabled');
          buttonElement.removeAttribute('aria-disabled');
          buttonElement.classList.remove('loading');
          const customSpinner = buttonElement.querySelector('.loading__spinner');
          if (customSpinner) customSpinner.classList.add('hidden');
        }

        if (typeof window.refreshDawnCartUI === 'function') {
          await window.refreshDawnCartUI();
          const cartIcon = document.getElementById('cart-icon-bubble');
          if (cartIcon) {
            cartIcon.click();
          } else {
            const cartDrawer = document.querySelector('cart-drawer');
            if (cartDrawer && typeof cartDrawer.open === 'function') cartDrawer.open();
          }
        } else {
          window.location.reload();
        }
      }
    } catch (err) {
      // Skipped because the page is already going to checkout (assets/kc-plan-select.js): nothing to tell
      const skipped = Boolean(err && err.kcSkipped);
      if (!skipped) console.error('[KarmiAddToCart] Checkout redirect failed:', err);
      // Tell the shopper (the earlier choice is back in the cart): Shopify's message, else the theme's
      // cart error, in the product form's error line (the buybox's for the sticky bar)
      const errorWrapper =
        (form.closest('product-form') || document).querySelector('.product-form__error-message-wrapper');
      const errorText = (err && err.shopperMessage) || (window.cartStrings && window.cartStrings.error) || '';
      if (!skipped && errorWrapper && errorText) {
        const errorMessage = errorWrapper.querySelector('.product-form__error-message');
        if (errorMessage) errorMessage.textContent = errorText;
        errorWrapper.hidden = false;
      }
      if (buttonElement) {
        buttonElement.disabled = false;
        buttonElement.removeAttribute('disabled');
        buttonElement.removeAttribute('aria-disabled');
        buttonElement.classList.remove('loading');
        const customSpinner = buttonElement.querySelector('.loading__spinner');
        if (customSpinner) customSpinner.classList.add('hidden');
      }
    }
  };
})();
