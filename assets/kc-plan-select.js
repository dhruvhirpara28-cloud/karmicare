/*
 * Plan selection on the product page, by Shopify selling plan ID only: renaming or translating a
 * plan never changes what is selected, and an unknown or non-public ID selects nothing.
 *
 * snippets/kc-plan-config.liquid writes one <script data-kc-plan-config> per Loop widget: its role
 * ("buybox" in main-product, "end-cta" in featured-product), its section and form, and every selling
 * plan of the product with its group and whether it is public (set on a compare plan).
 *
 * - KCPlanSelect.choose(productId, planId, title, groupId): selects that public plan in the buybox
 *   widget (never the end CTA widget, which has the same element ids), then checks the buybox form.
 * - KCPlanSelect.tryOnce(productId, button): this product's current variant as a one-time purchase
 *   (no selling plan), straight to checkout. Used by the buybox Try Once (loop-widget.js) and the
 *   compare plans Try Once.
 * - KCPlanSelect.subscriptionName(planId): the "Subscription Name" order attribute Loop Loyalty needs
 *   for Care Credit, by plan ID. Every add-to-cart path (loop-widget.js, karmi-add-to-cart.js,
 *   product-form.js) reads it here; syncCartSubscriptionName() keeps the cart's value in line with
 *   the subscription lines in it.
 * - KCPlanSelect.replaceChoice(productId, planId, add): one purchase choice of a plan product in the
 *   cart; every add-to-cart path adds the product through it (clearPurchaseChoice, then the add, one
 *   at a time on the page; the earlier choice comes back when the add is rejected). manages(productId)
 *   tells which products it handles.
 * - KCPlanSelect.plan(planId): type, interval, deliveries, Check-up Reward, Duos per delivery, duos,
 *   brushings and Return on Care of a plan, by ID: the pricing summary, the plan cards, the Welcome Kit
 *   and the sticky bar read plans here instead of by name. selectedPlanId() and allowed() serve the
 *   sticky bar and karmi-add-to-cart.js.
 * - KCPlanSelect.units(planId) / quantityFor(productId, planId, formQuantity): the Duos per delivery of a
 *   plan (snippets/kc-plan-type.liquid; year plans follow the theme setting "Year plans: Duos per
 *   delivery"). Every add-to-cart path adds that quantity for a subscription, and every price shown for
 *   a plan is Shopify's allocation price x units, which is what the checkout charges. yearDuos(planId,
 *   variantId): the year plan line shown next to the price while that setting is 3.
 * - Allowlist: the groups without a public plan stay hidden and unselectable in every Loop widget and
 *   the sticky bar; a non-public plan selected in the buybox is replaced by the first public one.
 * - Compare plan buttons (sections/product-compare-plans.liquid) carry data-kc-plan-choose: "plan"
 *   (with data-selling-plan-id, data-selling-plan-group-id) or "once".
 */
(function () {
  'use strict';

  if (window.KCPlanSelect) return;

  const ONE_TIME_ID = 'loop-one-time-purchase';
  const RADIO = 'input[name="loop_purchase_option"]';
  const PLAN_SELECT = 'select.loop-selling-plan-selector';
  const PLAN_CONTROLS = '.loop-subscription-container, .sc-dd-option, #scTrigger';
  const READY_TIMEOUT_MS = 5000;
  // Loop's own default selection runs 300 to 500 ms after it shows the widget
  const LOOP_DEFAULT_SETTLE_MS = 800;
  // How long a compare choice is kept against Loop's own late default selection, counted from the end
  // of Loop's background step
  const INTENT_GUARD_MS = 3000;
  // How long the guard polls for Loop's background step before it relies on enforce() alone
  const INTENT_POLL_MAX_MS = 60000;
  const MAX_FIXES = 5;
  // Toothbrush variants of the earlier Welcome Kit, still in some carts: kit lines too
  const LEGACY_KIT_VARIANT_IDS = ['42732468142262', '42732468076726'];

  // What a plan type means (snippets/kc-plan-type.liquid gives each selling plan ID its type). Plan
  // logic reads these by ID, never the plan name: billing interval, deliveries per billing (Loop's own
  // prepaid data wins when loaded) and the €40 Dental Check-up Reward of the Year plans.
  const PLAN_TYPES = {
    '60-day': { intervalUnit: 'day', intervalCount: 60, deliveries: 1, checkupReward: false },
    year: { intervalUnit: 'year', intervalCount: 1, deliveries: 2, checkupReward: true },
  };

  // Rebuilt from the config scripts in the page whenever a section is added, replaced or removed
  const products = {};
  // Per product, kept across rebuilds: failed fixes in a row, the compare choice being guarded
  const runtime = {};
  let configSignature = '';
  let configCounter = 0;
  // Last real pointer or key press on a plan control (Loop widgets, sticky bar) by the shopper
  let lastPlanControlAt = 0;

  function warn(message) {
    console.warn('[KC plans] ' + message);
  }

  function runtimeOf(productId) {
    return runtime[productId] || (runtime[productId] = { fixes: 0, intent: null });
  }

  function readConfigs() {
    const scripts = Array.from(document.querySelectorAll('script[data-kc-plan-config]'));
    const signature = scripts.map((s) => s.dataset.kcPlanKey || (s.dataset.kcPlanKey = String(++configCounter))).join(',');
    if (signature === configSignature) return;
    configSignature = signature;
    Object.keys(products).forEach((productId) => delete products[productId]);

    const configs = [];
    scripts.forEach((element) => {
      try {
        configs.push(JSON.parse(element.textContent));
      } catch (error) {
        warn('unreadable plan config: ' + error.message);
      }
    });
    // The buybox config first: its plan data wins over the end CTA's
    configs.sort((a, b) => (a.role === 'buybox' ? 0 : 1) - (b.role === 'buybox' ? 0 : 1));

    configs.forEach((config) => {
      const productId = String(config.productId);
      const product =
        products[productId] ||
        (products[productId] = { id: productId, widgets: [], plans: {}, groups: {}, publicCount: 0, kitVariantIds: [] });
      if (!product.shopCurrency && config.shopCurrency) product.shopCurrency = config.shopCurrency;
      (config.kitVariantIds || []).forEach((id) => {
        if (!product.kitVariantIds.includes(String(id))) product.kitVariantIds.push(String(id));
      });
      if (!product.widgets.find((w) => w.sectionId === config.sectionId && w.role === config.role)) {
        product.widgets.push({
          role: config.role,
          sectionId: config.sectionId,
          formId: config.formId,
          defaultToSubscription: config.defaultToSubscription === true,
        });
      }
      (config.plans || []).forEach((entry) => {
        const id = String(entry.id);
        if (product.plans[id]) return;
        const isPublic = entry.public === true;
        product.plans[id] = {
          id: id,
          groupId: entry.groupId,
          groupName: entry.groupName,
          public: isPublic,
          type: entry.type || '',
          loyaltyKey: entry.loyaltyKey || '',
          duos: entry.duos || null,
          units: entry.units,
          careCreditPercent: Number(entry.careCreditPercent) || 0,
          expectedTotal: typeof entry.expectedTotal === 'number' ? entry.expectedTotal : null,
          yearDuos: entry.yearDuos || {},
        };
        const group = product.groups[entry.groupId] || (product.groups[entry.groupId] = { public: false });
        if (isPublic) {
          group.public = true;
          product.publicCount += 1;
        }
      });
    });
  }

  // With no valid public plan ID configured, Loop's own visibility applies (never an empty buybox).
  function enforced(product) {
    return product.publicCount > 0;
  }

  function buyboxOf(product) {
    return product.widgets.find((w) => w.role === 'buybox') || null;
  }

  function containerOf(widget) {
    const info = document.getElementById('ProductInfo-' + widget.sectionId);
    return info ? info.querySelector('.loop-subscription-container') : null;
  }

  function formOf(widget) {
    return document.getElementById(widget.formId);
  }

  function formPlanId(widget) {
    const form = formOf(widget);
    const input = form && form.querySelector('input[name="selling_plan"]');
    return input ? input.value : '';
  }

  // Loop's functions act on the first widget of the product in the page
  function loopDrives(product, container) {
    return (
      typeof window.getLoopSubscriptionContainer === 'function' &&
      window.getLoopSubscriptionContainer(product.id) === container
    );
  }

  function loopReady(product, container) {
    const props = window.loopProps && window.loopProps[product.id];
    return Boolean(
      props &&
        props.variantToSellingPlans &&
        typeof window.changeInSellingPlanGroupLoop === 'function' &&
        !container.classList.contains('loop-display-none') &&
        container.querySelector(RADIO)
    );
  }

  // Ready, and Loop's background step (excluded plans, which selects its first plan again) has run
  function loopSettled(product, container) {
    const props = window.loopProps && window.loopProps[product.id];
    return loopReady(product, container) && Array.isArray(props.storefrontExcludedSPGS);
  }

  function waitFor(test, container) {
    return new Promise((resolve) => {
      if (test()) {
        resolve(true);
        return;
      }
      let done = false;
      let observer = null;
      const finish = (ok) => {
        if (done) return;
        done = true;
        clearInterval(poll);
        clearTimeout(timer);
        if (observer) observer.disconnect();
        resolve(ok);
      };
      const check = () => {
        if (test()) finish(true);
      };
      const poll = setInterval(check, 100);
      const timer = setTimeout(() => finish(test()), READY_TIMEOUT_MS);
      if (container && window.MutationObserver) {
        observer = new MutationObserver(check);
        observer.observe(container, { attributes: true, childList: true, subtree: true });
      }
    });
  }

  function currentVariantId(product, widget, container) {
    const props = window.loopProps && window.loopProps[product.id];
    if (loopDrives(product, container) && props && props.selectedVariantId) return String(props.selectedVariantId);
    const form = formOf(widget);
    const input = form && form.querySelector('[name="id"]');
    return input && input.value ? String(input.value) : '';
  }

  // true / false when Loop's product data tells whether the variant offers the plan, null when unknown
  function allocated(product, variantId, planId) {
    const props = window.loopProps && window.loopProps[product.id];
    const variants = props && props.product && props.product.variants;
    if (!variants || !variantId) return null;
    const variant = variants.find((v) => String(v.id) === String(variantId));
    if (!variant) return false;
    return (variant.selling_plan_allocations || []).some((a) => String(a.selling_plan_id) === planId);
  }

  function groupWrapper(radio) {
    return radio.closest('[id^="loop-selling_plan_group-"]') || radio.closest('.loop-subscription-group');
  }

  function shownByLoop(radio) {
    const wrapper = groupWrapper(radio);
    return !wrapper || !wrapper.classList.contains('loop-display-none');
  }

  function selectable(product, radio) {
    const groupId = radio.dataset.id;
    if (!groupId || groupId === ONE_TIME_ID) return false;
    if (enforced(product)) return Boolean(product.groups[groupId] && product.groups[groupId].public);
    return Boolean(product.groups[groupId]) && shownByLoop(radio);
  }

  // The group's radio of this variant only; another variant's radio never stands in
  function groupRadio(container, groupId, variantId) {
    const radios = Array.from(container.querySelectorAll(RADIO)).filter((r) => r.dataset.id === groupId);
    if (variantId && radios.some((r) => r.dataset.variantId)) {
      return radios.find((r) => r.dataset.variantId === String(variantId)) || null;
    }
    return radios[0] || null;
  }

  // To the top of the buybox widget (its plan cards), below the sticky header
  function scrollToBuybox(widget) {
    const container = containerOf(widget);
    const shown = (element) => Boolean(element && element.getClientRects().length);
    const target = [
      container && container.querySelector('.loop-purchase-options-label'),
      container,
      document.getElementById('ProductInfo-' + widget.sectionId),
    ].find(shown);
    if (!target) return;
    const header = document.querySelector('.section-header');
    const offset = (header ? header.offsetHeight : 0) + 16;
    const top = target.getBoundingClientRect().top + window.scrollY - offset;
    window.scrollTo({ top: Math.max(0, top), behavior: 'smooth' });
  }

  function selectGroup(product, container, radio) {
    if (loopDrives(product, container) && typeof window.changeInSellingPlanGroupLoop === 'function') {
      radio.checked = true;
      window.changeInSellingPlanGroupLoop({ target: radio });
    } else {
      radio.click();
    }
    // The sticky bar and the end CTA price listen for change
    radio.dispatchEvent(new Event('change', { bubbles: true }));
  }

  // A group can offer several plans (its select); set the exact one
  function selectExactPlan(product, container, radio, planId) {
    const group = radio.closest('.loop-subscription-group');
    const select = group && group.querySelector(PLAN_SELECT);
    if (!select) return;
    const props = window.loopProps && window.loopProps[product.id];
    if (select.value === planId && props && String(props.sellingPlanId) === planId) return;
    select.value = planId;
    if (select.value !== planId) return;
    if (loopDrives(product, container) && typeof window.changeInDeliveryOptionLoop === 'function') {
      window.changeInDeliveryOptionLoop({ target: select });
    } else {
      select.dispatchEvent(new Event('change', { bubbles: true }));
    }
  }

  function verify(widget, plan, label) {
    const actual = formPlanId(widget);
    if (actual === plan.id) return true;
    warn(label + ': the buybox form holds selling plan "' + actual + '", expected ' + plan.id + ' (' + plan.groupName + ')');
    return false;
  }

  function select(product, widget, container, plan, label) {
    const variantId = currentVariantId(product, widget, container);
    if (allocated(product, variantId, plan.id) === false) {
      warn(label + ': selling plan ' + plan.id + ' (' + plan.groupName + ') is not offered for variant ' + variantId + '; nothing selected');
      return false;
    }
    const radio = groupRadio(container, plan.groupId, variantId);
    if (!radio) {
      warn(label + ': the buybox has no option for selling plan ' + plan.id + ' (' + plan.groupName + '); nothing selected');
      return false;
    }
    if (!selectable(product, radio)) {
      warn(label + ': selling plan ' + plan.id + ' (' + plan.groupName + ') is not shown in the buybox; nothing selected');
      return false;
    }
    const previous = { radio: container.querySelector(RADIO + ':checked'), planId: formPlanId(widget) };
    selectGroup(product, container, radio);
    selectExactPlan(product, container, radio, plan.id);
    if (verify(widget, plan, label)) return true;
    // Never leave the form without the plan the widget shows: put the previous choice back
    if (previous.radio && previous.radio !== radio) {
      selectGroup(product, container, previous.radio);
      if (previous.planId) selectExactPlan(product, container, previous.radio, previous.planId);
      warn(label + ': restored the previous selection (' + (previous.planId || 'one time') + ')');
    }
    return false;
  }

  function choose(productId, planId, title, groupId) {
    readConfigs();
    const label = '"' + (title || 'plan') + '"';
    const id = String(planId == null ? '' : planId).trim();
    const product = products[String(productId)];
    const widget = product && buyboxOf(product);
    if (!widget) {
      warn(label + ': no buybox for product ' + productId + '; selling plan ID "' + id + '" not selected');
      return Promise.resolve(false);
    }
    scrollToBuybox(widget);

    const plan = /^\d+$/.test(id) ? product.plans[id] : null;
    if (!plan) {
      warn(label + ': "' + id + '" is not a selling plan ID of this product; nothing selected');
      return Promise.resolve(false);
    }
    if (enforced(product) && !plan.public) {
      warn(label + ': selling plan ' + id + ' (' + plan.groupName + ') is not public; nothing selected');
      return Promise.resolve(false);
    }
    if (groupId && groupId !== plan.groupId) {
      warn(label + ': selling plan ' + id + ' belongs to group ' + plan.groupId + ', not ' + groupId + '; nothing selected');
      return Promise.resolve(false);
    }
    const container = containerOf(widget);
    if (!container) {
      warn(label + ': the buybox Loop widget is missing; selling plan ' + id + ' not selected');
      return Promise.resolve(false);
    }
    const startedAt = Date.now();
    return waitFor(() => loopSettled(product, container), container).then((ready) => {
      if (lastPlanControlAt > startedAt) {
        warn(label + ': the shopper picked a plan in the buybox meanwhile; left as it is');
        return false;
      }
      if (!ready) warn(label + ': the buybox Loop widget was not ready after 5 s; selecting anyway');
      const ok = select(product, widget, container, plan, label);
      if (ok) guardIntent(product, widget, plan, label);
      return ok;
    });
  }

  // Loop may still run its own default selection (300-500 ms timers, and its background step, which
  // selects its first plan again and can arrive many seconds late) after a compare choice. The choice is
  // guarded until Loop's background step has run and INTENT_GUARD_MS more have passed, however long
  // that takes: if Loop (not the shopper) switches the plan, it is put back. A newer shopper choice
  // ends the guard. Then the form is checked once more.
  function guardIntent(product, widget, plan, label) {
    const state = runtimeOf(product.id);
    const intent = { planId: plan.id, label: label, at: Date.now(), until: 0, restores: 0 };
    state.intent = intent;
    const check = () => {
      if (state.intent !== intent) return;
      if (lastPlanControlAt > intent.at) {
        state.intent = null;
        return;
      }
      const current = products[product.id];
      startGuardWindow(current, intent);
      if (!intent.until || Date.now() < intent.until) {
        // Without Loop's background step the guard stays on (enforce() keeps it); only the polling stops
        if (Date.now() - intent.at < INTENT_POLL_MAX_MS) setTimeout(check, 250);
        return;
      }
      state.intent = null;
      const buybox = current ? buyboxOf(current) : null;
      if (buybox && formPlanId(buybox) !== plan.id) {
        warn(label + ': the buybox moved from selling plan ' + plan.id + ' to "' + formPlanId(buybox) + '" without the shopper');
      }
    };
    setTimeout(check, 250);
  }

  // The guard window starts once Loop's background step has run
  function startGuardWindow(product, intent) {
    if (intent.until || !product) return;
    const widget = buyboxOf(product);
    const container = widget && containerOf(widget);
    if (container && loopSettled(product, container)) intent.until = Date.now() + INTENT_GUARD_MS;
  }

  function keepIntent(product) {
    const state = runtimeOf(product.id);
    const intent = state.intent;
    if (!intent) return false;
    startGuardWindow(product, intent);
    if ((intent.until && Date.now() > intent.until) || lastPlanControlAt > intent.at) {
      state.intent = null;
      return false;
    }
    const widget = buyboxOf(product);
    const container = widget && containerOf(widget);
    const plan = product.plans[intent.planId];
    if (!container || !plan || formPlanId(widget) === intent.planId) return false;
    if (intent.restores >= MAX_FIXES) return false;
    intent.restores += 1;
    select(product, widget, container, plan, intent.label + ' (put back after Loop changed it)');
    return true;
  }

  function tryOnce(productId, button) {
    readConfigs();
    const product = products[String(productId)];
    const widget = product && buyboxOf(product);
    const form =
      (widget && formOf(widget)) ||
      document.querySelector('form[data-loop-product-id="' + String(productId).replace(/\D/g, '') + '"]');
    if (!form) {
      warn('Try Once: no product form for product ' + productId);
      return Promise.resolve(false);
    }
    if (typeof window.karmiAddToCart !== 'function') {
      warn('Try Once: karmiAddToCart is not loaded');
      return Promise.resolve(false);
    }
    return Promise.resolve(window.karmiAddToCart(form, button || null, { oneTime: true, redirectToCheckout: true })).then(
      () => true
    );
  }

  function productOfPlan(id) {
    return Object.keys(products)
      .map((productId) => products[productId])
      .find((p) => p.plans[id]);
  }

  // Everything plan logic needs about one selling plan, by its ID: type, interval, deliveries,
  // Dental Check-up Reward, Care Credit name, and the duos / brushings / Return on Care on its Loop
  // plan option in the buybox (by ID when the duos metaobject has plan IDs, see applyPlanData).
  // null for an unknown ID.
  function plan(planId) {
    readConfigs();
    const id = String(planId == null ? '' : planId).trim();
    if (!/^\d+$/.test(id)) return null;
    const product = productOfPlan(id);
    if (!product) return null;
    const entry = product.plans[id];
    const typeInfo = PLAN_TYPES[entry.type] || null;
    const props = window.loopProps && window.loopProps[product.id];
    const prepaid = props && props.prepaidSellingPlans && props.prepaidSellingPlans[id];
    const widget = buyboxOf(product);
    const container = widget && containerOf(widget);
    const option = container
      ? Array.from(container.querySelectorAll(PLAN_SELECT + ' option')).find((o) => o.value === id)
      : null;
    const fromOption = (name, fallback) => {
      const value = option && parseInt(option.dataset[name], 10);
      return Number.isFinite(value) ? value : fallback;
    };
    return {
      id: id,
      groupId: entry.groupId,
      type: entry.type,
      public: entry.public,
      loyaltyKey: entry.loyaltyKey,
      intervalUnit: typeInfo ? typeInfo.intervalUnit : '',
      intervalCount: typeInfo ? typeInfo.intervalCount : 0,
      deliveries: (prepaid && prepaid.deliveriesPerBillingCycle) || (typeInfo ? typeInfo.deliveries : 1),
      checkupReward: Boolean(typeInfo && typeInfo.checkupReward),
      units: units(id),
      careCreditPercent: entry.careCreditPercent,
      duos: fromOption('duos', entry.duos ? entry.duos.duos : 1),
      brushings: fromOption('brushings', entry.duos ? entry.duos.brushings : 120),
      returnOnCare: fromOption('returnOnCare', entry.duos ? entry.duos.returnOnCare : 0),
    };
  }

  const warnedUnits = {};

  // Duos per delivery of a selling plan (snippets/kc-plan-type.liquid): 60-day plans 1, year plans the
  // theme setting "Year plans: Duos per delivery". A plan of a plan product that is not in that table
  // gets 1 and one warning; a plan of any other product 1.
  function units(planId) {
    readConfigs();
    const id = String(planId == null ? '' : planId).trim();
    if (!/^\d+$/.test(id)) return 1;
    const product = productOfPlan(id);
    if (!product) return 1;
    const entry = product.plans[id];
    if (!entry.type && !warnedUnits[id]) {
      warnedUnits[id] = true;
      warn('selling plan ' + id + ' (' + entry.groupName + ') is not in snippets/kc-plan-type.liquid; 1 Duo per delivery');
    }
    const count = parseInt(entry.units, 10);
    return Number.isFinite(count) && count > 0 ? count : 1;
  }

  // The quantity to add for a purchase choice: a plan product's subscription gets its plan's Duos per
  // delivery (the shopper cannot change it in the cart); one time (Try Once) and every other product
  // keep the form's quantity.
  function quantityFor(productId, planId, formQuantity) {
    readConfigs();
    const parsed = parseInt(formQuantity, 10);
    const fallback = Number.isFinite(parsed) && parsed > 0 ? parsed : 1;
    const id = String(planId == null ? '' : planId).trim();
    if (!products[String(productId)] || !id) return fallback;
    return units(id);
  }

  // The line a year plan shows next to its price for a variant ("6 duos · 3 now, 3 in month 6 · €59 per
  // duo", snippets/kc-plan-year-duos.liquid), or '' (not a year plan, or year plans are 1 Duo per delivery)
  function yearDuos(planId, variantId) {
    readConfigs();
    const id = String(planId == null ? '' : planId).trim();
    const product = /^\d+$/.test(id) ? productOfPlan(id) : null;
    if (!product) return '';
    return product.plans[id].yearDuos[String(variantId)] || '';
  }

  const checkedTotals = {};

  function euros(cents) {
    return (cents / 100).toFixed(2);
  }

  // While year plans are more than 1 Duo per delivery, each year plan must cost its expected year total
  // (snippets/kc-plan-type.liquid) at checkout: Shopify's allocation price x Duos. Warn when it does
  // not, e.g. Loop still prices the whole year instead of one Duo. Prices in another currency than the
  // shop's are not checked.
  function checkTotals(product) {
    const props = window.loopProps && window.loopProps[product.id];
    const variants = props && props.product && props.product.variants;
    if (!Array.isArray(variants)) return;
    const active = window.Shopify && window.Shopify.currency && window.Shopify.currency.active;
    if (product.shopCurrency && active && active !== product.shopCurrency) return;
    variants.forEach((variant) => {
      (variant.selling_plan_allocations || []).forEach((allocation) => {
        // Every year plan, also those the page does not sell (legacy plans renew through Loop at this price)
        const entry = product.plans[String(allocation.selling_plan_id)];
        if (!entry || entry.type !== 'year') return;
        const count = units(entry.id);
        if (count <= 1) return;
        const total = Number(allocation.price) * count;
        const key = variant.id + ':' + entry.id + ':' + total;
        if (checkedTotals[key]) return;
        checkedTotals[key] = true;
        const what =
          'year plan ' + entry.id + ' (' + entry.groupName + ', variant ' + variant.id + '): allocation price ' +
          euros(allocation.price) + ' x ' + count + ' Duos = ' + euros(total);
        if (entry.expectedTotal == null) {
          warn(what + ', and snippets/kc-plan-type.liquid has no expected total for it');
        } else if (total !== entry.expectedTotal) {
          warn(what + ', expected ' + euros(entry.expectedTotal) + ': the checkout charges ' + euros(total) + '; check the plan price in Loop');
        }
      });
    });
  }

  // The selling plan the buybox form will buy ('' for one time)
  function selectedPlanId(productId) {
    readConfigs();
    const product = products[String(productId)];
    const widget = product && buyboxOf(product);
    return widget ? formPlanId(widget) : '';
  }

  // The variant the buybox form will buy ('' when unknown); the sticky bar submits this one
  function selectedVariantId(productId) {
    readConfigs();
    const product = products[String(productId)];
    const widget = product && buyboxOf(product);
    const form = widget && formOf(widget);
    const input = form && form.querySelector('[name="id"]');
    return input && input.value ? String(input.value) : '';
  }

  // false for a selling plan this page must not sell (a legacy plan while the allowlist is on)
  function allowed(planId) {
    readConfigs();
    const id = String(planId == null ? '' : planId).trim();
    const product = productOfPlan(id);
    if (!product || !enforced(product)) return true;
    return product.plans[id].public;
  }

  // Duos, brushings and Return on Care by plan ID onto the Loop plan options (data-duos,
  // data-brushings, data-return-on-care), in every widget of the product. Loop's widget matches them
  // by plan name; where the duos metaobject lists plan IDs these values win.
  function applyPlanData(product) {
    product.widgets.forEach((widget) => {
      const container = containerOf(widget);
      if (!container) return;
      container.querySelectorAll(PLAN_SELECT + ' option').forEach((option) => {
        const entry = product.plans[option.value];
        if (!entry || !entry.duos) return;
        const values = {
          duos: String(entry.duos.duos),
          brushings: String(entry.duos.brushings),
          returnOnCare: String(entry.duos.returnOnCare),
        };
        Object.keys(values).forEach((name) => {
          if (option.dataset[name] !== values[name]) option.dataset[name] = values[name];
        });
      });
    });
  }

  const warnedLoyalty = {};

  // The "Subscription Name" order attribute for a selling plan: Loop Loyalty awards Care Credit by this
  // exact value. It comes from the plan ID (snippets/kc-plan-loyalty.liquid), never from visible text.
  // A plan without one gets no attribute.
  function subscriptionName(planId) {
    readConfigs();
    const id = String(planId == null ? '' : planId).trim();
    if (!/^\d+$/.test(id)) return '';
    const product = productOfPlan(id);
    const entry = product && product.plans[id];
    if (entry && entry.loyaltyKey) return entry.loyaltyKey;
    if (!warnedLoyalty[id]) {
      warnedLoyalty[id] = true;
      warn(
        'selling plan ' + id + (entry ? ' (' + entry.groupName + ') has no Subscription Name' : ' is not in a plan config on this page') +
          '; the order gets no "Subscription Name" attribute and no Care Credit'
      );
    }
    return '';
  }

  // Cart attributes outlive the lines they were set for. After an add, set "Subscription Name" to the
  // subscription now in the cart (the just added plan first), or clear it when none is left, so a
  // one-time order never carries an earlier subscription's value.
  async function syncCartSubscriptionName(preferredPlanId) {
    const headers = { 'Content-Type': 'application/json', 'X-Karmi-Sync': 'false' };
    const cart = await fetch('/cart.js', { headers: headers }).then((response) => response.json());
    const planIds = (cart.items || [])
      .map((item) => item.selling_plan_allocation && item.selling_plan_allocation.selling_plan)
      .filter(Boolean)
      .map((sellingPlan) => String(sellingPlan.id));
    const preferred = preferredPlanId != null ? String(preferredPlanId) : '';
    const ordered = planIds.includes(preferred) ? [preferred].concat(planIds) : planIds;
    const wanted = ordered.map(subscriptionName).find(Boolean) || '';
    const current = (cart.attributes && cart.attributes['Subscription Name']) || '';
    if (current !== wanted) {
      await fetch('/cart/update.js', {
        method: 'POST',
        headers: headers,
        body: JSON.stringify({ attributes: { 'Subscription Name': wanted } }),
      });
    }
    return wanted;
  }

  // The product a variant belongs to, from Loop's product data on the page ('' when unknown)
  function productIdOfVariant(variantId) {
    const id = String(variantId == null ? '' : variantId);
    const props = window.loopProps || {};
    return (
      Object.keys(props).find((productId) => {
        const variants = props[productId] && props[productId].product && props[productId].product.variants;
        return Array.isArray(variants) && variants.some((v) => String(v.id) === id);
      }) || ''
    );
  }

  // One purchase choice of a plan product in the cart (Victor, 15 Oct: the cart held a 60-day and a Year
  // membership after a switch). Before a new choice of the product is added, one update call removes
  // every line of the product (any plan or one time) and every Welcome Kit line, and sets
  // "Subscription Name" for the coming choice (cleared for one time). The caller then adds the choice as
  // one line (quantityFor: the plan's Duos per delivery, 1 for Try Once), with one kit set for a
  // subscription. Kit lines: the _welcome_kit property, the configured kit
  // variants, or the earlier kit's toothbrush variants. Resolves false for a product without a plan
  // config (nothing changed), else what it removed (recoverChoice puts it back after a failed add); rejects when the cart
  // could not be updated. Callers go through replaceChoice().
  async function clearPurchaseChoice(productId, sellingPlanId) {
    readConfigs();
    const product = products[String(productId)];
    if (!product) return false;
    const headers = { 'Content-Type': 'application/json', 'X-Karmi-Sync': 'false' };
    const cart = await fetch('/cart.js', { headers: headers }).then((response) => response.json());
    const kitVariantIds = product.kitVariantIds.concat(LEGACY_KIT_VARIANT_IDS);
    const updates = {};
    const removed = [];
    (cart.items || []).forEach((item) => {
      const isKit =
        (item.properties && item.properties._welcome_kit === 'true') || kitVariantIds.includes(String(item.variant_id));
      if (String(item.product_id) !== product.id && !isKit) return;
      updates[item.key] = 0;
      const line = { id: item.variant_id, quantity: item.quantity };
      if (item.selling_plan_allocation) line.selling_plan = item.selling_plan_allocation.selling_plan.id;
      if (item.properties && Object.keys(item.properties).length) line.properties = item.properties;
      removed.push(line);
    });
    const body = { attributes: { 'Subscription Name': sellingPlanId ? subscriptionName(sellingPlanId) : '' } };
    if (Object.keys(updates).length) body.updates = updates;
    const response = await fetch('/cart/update.js', { method: 'POST', headers: headers, body: JSON.stringify(body) });
    if (!response.ok) throw new Error('could not remove the earlier choice from the cart');
    return { lines: removed, subscriptionName: (cart.attributes && cart.attributes['Subscription Name']) || '' };
  }

  // Puts back what clearPurchaseChoice removed (the earlier choice, its kit lines, "Subscription Name"),
  // after a failed add. A failed request may still have added the new choice (a lost response): when the
  // cart holds the product again, that choice stays and nothing is put back. When the cart cannot be read,
  // nothing is put back either (it could double the choice). Resolves 'kept', 'restored', 'lost' (the
  // earlier choice could not be put back) or 'unknown' (the cart could not be read).
  async function recoverChoice(productId, removed) {
    const headers = { 'Content-Type': 'application/json', 'X-Karmi-Sync': 'false' };
    let cart = null;
    try {
      const response = await fetch('/cart.js', { headers: headers });
      const data = response.ok ? await response.json() : null;
      if (data && Array.isArray(data.items)) cart = data;
    } catch (error) {
      cart = null;
    }
    if (!cart) {
      warn('the add failed and the cart could not be read; the earlier choice was not put back');
      return 'unknown';
    }
    try {
      if (cart.items.some((item) => String(item.product_id) === String(productId))) {
        warn('the add reported a failure but the cart holds a choice of the product; left as it is');
        return 'kept';
      }
      let ok = true;
      if (removed.lines.length) {
        const added = await fetch('/cart/add.js', { method: 'POST', headers: headers, body: JSON.stringify({ items: removed.lines }) });
        ok = added.ok;
      }
      if (ok) {
        const updated = await fetch('/cart/update.js', {
          method: 'POST',
          headers: headers,
          body: JSON.stringify({ attributes: { 'Subscription Name': removed.subscriptionName } }),
        });
        ok = updated.ok;
      }
      if (ok) {
        warn('the new choice was not added to the cart; the earlier choice is back');
        return 'restored';
      }
      warn('the new choice was not added and the earlier choice could not be put back');
    } catch (error) {
      warn('the new choice was not added and the earlier choice could not be put back: ' + error.message);
    }
    // "Subscription Name" was set for the choice that did not arrive: match it to what the cart holds
    await syncCartSubscriptionName().catch(() => {});
    return 'lost';
  }

  let purchaseQueue = Promise.resolve();
  let choicesRequested = 0;
  // Set once a replacement sends the page to checkout: later replacements leave the cart as it is
  let navigating = false;
  window.addEventListener('pageshow', (event) => {
    if (event.persisted) navigating = false;
  });

  // Replaces the purchase choice of a plan product: clearPurchaseChoice, then add() (the caller's cart
  // add, resolving its fetch Response), then finish() (optional), all in one turn of a queue: one
  // replacement at a time on the page, whichever path started it (buybox, compare, sticky bar, end CTA,
  // Try Once, product-form.js, Loop's bundle add), so two quick clicks never both add and leave 6 Duos or
  // two choices. finish({ superseded }) runs after a successful add (e.g. the Subscription Name sync) and
  // may return a URL to go to: the queue sends the page there itself, only when no later replacement is
  // waiting (superseded false); a replacement asked for after that rejects at once with kcSkipped, the
  // cart untouched (the queue stays free, also after Back). When Shopify rejects the add or it fails,
  // recoverChoice() runs. Resolves add()'s Response, marked kcSuperseded / kcNavigating / kcRecovery.
  function replaceChoice(productId, sellingPlanId, add, finish) {
    const ticket = ++choicesRequested;
    const run = async () => {
      // The page is on its way to checkout: changing the cart now could empty it under that checkout
      if (navigating) {
        const skipped = new Error('the page is going to checkout; this choice was not added');
        skipped.kcSkipped = true;
        throw skipped;
      }
      const removed = await clearPurchaseChoice(productId, sellingPlanId);
      let response;
      try {
        response = await add();
      } catch (error) {
        if (removed) error.kcRecovery = await recoverChoice(productId, removed);
        throw error;
      }
      if (!response.ok) {
        if (removed) response.kcRecovery = await recoverChoice(productId, removed);
        return response;
      }
      const superseded = ticket !== choicesRequested;
      response.kcSuperseded = superseded;
      if (finish) {
        const url = await finish({ superseded: superseded });
        if (url && !superseded && ticket === choicesRequested) {
          navigating = true;
          response.kcNavigating = true;
          window.location.href = url;
        }
      }
      return response;
    };
    const result = purchaseQueue.then(run, run);
    purchaseQueue = result.catch(() => {});
    return result;
  }

  // true for a product with a plan config on this page (its choice goes through replaceChoice)
  function manages(productId) {
    readConfigs();
    return Boolean(products[String(productId)]);
  }

  // Hidden or disabled by this script (marked), so it can be undone when a plan becomes public again
  function hide(element) {
    if (!element) return;
    if (element.dataset.kcPlanHidden !== 'true') element.dataset.kcPlanHidden = 'true';
    if (!element.classList.contains('kc-plan-hidden')) element.classList.add('kc-plan-hidden');
    if (!element.hidden) element.hidden = true;
    if (element.getAttribute('aria-hidden') !== 'true') element.setAttribute('aria-hidden', 'true');
    if (element.style.getPropertyValue('display') !== 'none' || element.style.getPropertyPriority('display') !== 'important') {
      element.style.setProperty('display', 'none', 'important');
    }
  }

  function unhide(element) {
    if (!element || element.dataset.kcPlanHidden !== 'true') return;
    delete element.dataset.kcPlanHidden;
    element.classList.remove('kc-plan-hidden');
    element.hidden = false;
    element.removeAttribute('aria-hidden');
    element.style.removeProperty('display');
  }

  function disable(control) {
    if (control.dataset.kcPlanDisabled !== 'true') control.dataset.kcPlanDisabled = 'true';
    if (!control.disabled) control.disabled = true;
  }

  function enable(control) {
    if (control.dataset.kcPlanDisabled !== 'true') return;
    delete control.dataset.kcPlanDisabled;
    control.disabled = false;
  }

  function firstSelectablePlan(product, widget, container) {
    const variantId = currentVariantId(product, widget, container);
    const radio = Array.from(container.querySelectorAll(RADIO)).find(
      (r) => selectable(product, r) && (!variantId || r.dataset.variantId === variantId)
    );
    if (!radio) return null;
    const select = radio.closest('.loop-subscription-group') && radio.closest('.loop-subscription-group').querySelector(PLAN_SELECT);
    const ids = select ? Array.from(select.options).map((o) => o.value) : Object.keys(product.plans);
    const plans = ids
      .map((id) => product.plans[id])
      .filter((entry) => entry && entry.groupId === radio.dataset.id && (entry.public || !enforced(product)));
    if (select && !enforced(product)) {
      const current = plans.find((entry) => entry.id === select.value);
      if (current) return current;
    }
    return plans[0] || null;
  }

  // A non-public plan selected in the buybox (Loop's default, a forced click): select the first public one
  function keepPublicSelection(product) {
    const widget = buyboxOf(product);
    const container = widget && containerOf(widget);
    if (!container || !loopReady(product, container)) return;

    const state = runtimeOf(product.id);
    const checked = container.querySelector(RADIO + ':checked');
    const checkedGroup = checked && checked.dataset.id !== ONE_TIME_ID ? product.groups[checked.dataset.id] : null;
    const formPlan = product.plans[formPlanId(widget)];
    const wrong = (checkedGroup && !checkedGroup.public) || (formPlan && !formPlan.public);
    if (!wrong) {
      state.fixes = 0;
      return;
    }
    // Stop after a few failed fixes in a row instead of fighting the widget forever
    if (state.fixes >= MAX_FIXES) return;
    state.fixes += 1;
    const first = firstSelectablePlan(product, widget, container);
    if (!first) return;
    warn('a non-public plan was selected in the buybox; selecting ' + first.id + ' (' + first.groupName + ')');
    select(product, widget, container, first, '"' + first.groupName + '"');
  }

  function enforce(product) {
    if (!product) return;
    const on = enforced(product);

    let stolen = false;
    product.widgets.forEach((widget) => {
      const container = containerOf(widget);
      if (!container) return;
      container.querySelectorAll(RADIO).forEach((radio) => {
        const groupId = radio.dataset.id;
        if (!groupId || groupId === ONE_TIME_ID || !product.groups[groupId]) return;
        if (!on || product.groups[groupId].public) {
          unhide(groupWrapper(radio));
          enable(radio);
          return;
        }
        hide(groupWrapper(radio));
        disable(radio);
        // All Loop radios share one name outside any form, so they are one radio group across the
        // page: a non-public radio checked in another widget unchecks the buybox. Undo that.
        if (radio.checked && widget.role !== 'buybox') {
          radio.checked = false;
          stolen = true;
        }
      });
      container.querySelectorAll(PLAN_SELECT + ' option').forEach((option) => {
        const entry = product.plans[option.value];
        if (!entry) return;
        if (!on || entry.public) {
          unhide(option);
          enable(option);
        } else {
          hide(option);
          disable(option);
        }
      });
    });

    document.querySelectorAll('.sc-dd-option[data-selling-plan-group-id]').forEach((option) => {
      const group = product.groups[option.dataset.sellingPlanGroupId];
      if (!group) return;
      if (!on || group.public) unhide(option);
      else hide(option);
    });

    allowExpressCheckout(product);
    if (!on) return;
    if (stolen) recheckBuybox(product);
    if (keepIntent(product)) return;
    keepPublicSelection(product);
  }

  // Shopify's dynamic checkout button ("Buy it now", "Buy with Shop Pay") in a widget's form buys the
  // form's selling plan at quantity 1, never the plan's Duos per delivery. kc-plan-config hides it from
  // first paint; it shows (kc-express-allowed) only while the form holds no selling plan (one time).
  function allowExpressCheckout(product) {
    product.widgets.forEach((widget) => {
      const form = formOf(widget);
      if (!form) return;
      // Only the buybox: the end CTA's button buys its fixed offer, which its form does not hold, so
      // express checkout there could buy something else than the offer shown
      const oneTime = widget.role === 'buybox' && formPlanId(widget) === '';
      if (form.classList.contains('kc-express-allowed') !== oneTime) form.classList.toggle('kc-express-allowed', oneTime);
    });
  }

  // Check the buybox radio of the group Loop has selected again (Loop's state did not change)
  function recheckBuybox(product) {
    const widget = buyboxOf(product);
    const container = widget && containerOf(widget);
    const props = window.loopProps && window.loopProps[product.id];
    if (!container || !props || !props.sellingPlanGroupId) return;
    if (container.querySelector(RADIO + ':checked')) return;
    const radio = groupRadio(container, props.sellingPlanGroupId, currentVariantId(product, widget, container));
    if (radio && (radio.dataset.id === ONE_TIME_ID || selectable(product, radio))) radio.checked = true;
  }

  function watch(productId, container) {
    if (container.dataset.kcPlanWatched) return;
    container.dataset.kcPlanWatched = 'true';

    let scheduled = false;
    const schedule = () => {
      if (scheduled) return;
      scheduled = true;
      setTimeout(() => {
        scheduled = false;
        readConfigs();
        enforce(products[productId]);
      }, 0);
    };
    new MutationObserver(schedule).observe(container, {
      attributes: true,
      attributeFilter: ['class', 'style', 'hidden', 'disabled'],
      childList: true,
      subtree: true,
    });
    container.addEventListener('change', schedule, true);
    container.addEventListener('click', schedule, true);
  }

  // Replaces the Loop block's "default to subscription" script: start on the first public plan
  function startOnSubscription(productId, container) {
    let touched = false;
    const touch = () => {
      touched = true;
    };
    container.addEventListener('pointerdown', touch, true);
    container.addEventListener('keydown', touch, true);

    const settled = () => {
      const product = products[productId];
      return Boolean(product) && loopSettled(product, container);
    };
    waitFor(settled, container).then((ready) => {
      if (!ready) {
        warn('the buybox Loop widget of product ' + productId + ' was not ready after 5 s');
        return;
      }
      setTimeout(() => {
        readConfigs();
        const product = products[productId];
        const widget = product && buyboxOf(product);
        if (!widget) return;
        enforce(product);
        checkTotals(product);
        if (!widget.defaultToSubscription || touched || runtimeOf(productId).intent) return;
        const checked = container.querySelector(RADIO + ':checked');
        if (checked && checked.dataset.id !== ONE_TIME_ID) return;
        const first = firstSelectablePlan(product, widget, container);
        if (first) select(product, widget, container, first, '"' + first.groupName + '" (default)');
      }, LOOP_DEFAULT_SETTLE_MS);
    });
  }

  function init() {
    readConfigs();
    Object.keys(products).forEach((productId) => {
      const product = products[productId];
      applyPlanData(product);
      enforce(product);
      product.widgets.forEach((widget) => {
        const container = containerOf(widget);
        if (!container || container.dataset.kcPlanWatched) return;
        watch(productId, container);
        if (widget.role === 'buybox') startOnSubscription(productId, container);
      });
    });
  }

  // A shopper's own plan choice: pointer or keyboard input only. Loop's defaults call radio.click(), and
  // the change event that follows is trusted too, so click and change cannot tell Loop from the shopper.
  const markPlanControl = (event) => {
    if (!event.isTrusted || !event.target || !event.target.closest) return;
    if (event.target.closest(PLAN_CONTROLS)) lastPlanControlAt = Date.now();
  };
  document.addEventListener('pointerdown', markPlanControl, true);
  document.addEventListener('keydown', markPlanControl, true);

  document.addEventListener('click', (event) => {
    const button = event.target.closest && event.target.closest('[data-kc-plan-choose]');
    if (!button) return;
    event.preventDefault();
    const productId = button.dataset.kcPlanProduct;
    if (button.dataset.kcPlanChoose === 'once') {
      tryOnce(productId, button);
      return;
    }
    choose(productId, button.dataset.sellingPlanId, button.dataset.kcPlanTitle, button.dataset.sellingPlanGroupId);
  });

  // Theme editor: a section added, replaced or removed brings its own config; re-read and re-apply
  document.addEventListener('shopify:section:load', init);
  document.addEventListener('shopify:section:unload', () => setTimeout(init, 0));
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  window.KCPlanSelect = {
    choose: choose,
    tryOnce: tryOnce,
    subscriptionName: subscriptionName,
    syncCartSubscriptionName: syncCartSubscriptionName,
    replaceChoice: replaceChoice,
    manages: manages,
    productIdOfVariant: productIdOfVariant,
    plan: plan,
    units: units,
    quantityFor: quantityFor,
    yearDuos: yearDuos,
    selectedPlanId: selectedPlanId,
    selectedVariantId: selectedVariantId,
    allowed: allowed,
    refresh: init,
  };
})();
