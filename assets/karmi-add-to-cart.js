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
      const variantIdInput = form.querySelector('[name="id"]');
      const variantId = variantIdInput ? variantIdInput.value : null;
      if (!variantId) throw new Error('No variant ID found');

      const sellingPlanInput = form.querySelector('[name="selling_plan"]');
      const sellingPlanId = sellingPlanInput ? sellingPlanInput.value : null;

      const quantityInput = form.querySelector('[name="quantity"]');
      const quantity = quantityInput ? parseInt(quantityInput.value) || 1 : 1;

      const mainItem = { id: parseInt(variantId), quantity: quantity };
      if (sellingPlanId && !isNaN(parseInt(sellingPlanId))) {
        mainItem.selling_plan = parseInt(sellingPlanId);
      }

      const items = [mainItem];

      if (options && options.isBundleProduct && !options.customerAlreadyReceivedFreeProduct && options.welcomeKitVariantIds && options.welcomeKitVariantIds.length > 0) {
        let cartItems = [];
        try {
          const cartRes = await fetch('/cart.js');
          const cartData = await cartRes.json();
          cartItems = cartData.items || [];
        } catch (e) { }

        for (const vid of options.welcomeKitVariantIds) {
          const alreadyInCart = cartItems.some(item => item.variant_id === parseInt(vid));
          if (!alreadyInCart) {
            items.push({
              id: parseInt(vid),
              quantity: 1,
              properties: { '_welcome_kit': 'true' }
            });
          }
        }
      }

      const selectedLoopOption = document.querySelector('input[name="loop_purchase_option"]:checked');
      let cartAttributes = null;
      if (selectedLoopOption && selectedLoopOption.dataset.name && sellingPlanId && !isNaN(parseInt(sellingPlanId))) {
        cartAttributes = { 'Subscription Name': selectedLoopOption.dataset.name };
      }

      const addRes = await fetch('/cart/add.js', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-Karmi-Sync': 'false' },
        body: JSON.stringify({ items: items }),
      });
      if (!addRes.ok) throw new Error('Cart add failed');

      if (cartAttributes) {
        try {
          await fetch('/cart/update.js', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'X-Karmi-Sync': 'false' },
            body: JSON.stringify({ attributes: cartAttributes })
          });
        } catch (e) { console.error('Cart attributes update failed', e); }
      }

      if (items.length > 1) {
        try {
          await fetch('/cart/update.js', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'X-Karmi-Sync': 'false' },
            body: JSON.stringify({ discount: 'Welcome Kit' })
          });
        } catch (e) { console.error('Cart discount update failed', e); }
      }

      if (typeof window.karmiWelcomeKitSync === 'function') {
        await window.karmiWelcomeKitSync();
      }

      if (options && options.redirectToCheckout) {
        window.location.href = '/checkout';
      } else {
        if (buttonElement) {
          buttonElement.disabled = false;
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
      console.error('[KarmiAddToCart] Checkout redirect failed:', err);
      if (buttonElement) {
        buttonElement.disabled = false;
        buttonElement.classList.remove('loading');
        const customSpinner = buttonElement.querySelector('.loading__spinner');
        if (customSpinner) customSpinner.classList.add('hidden');
      }
    }
  };
})();
