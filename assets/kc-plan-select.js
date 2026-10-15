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
 * - KCPlanSelect.clearPurchaseChoice(productId, planId): one purchase choice of a plan product in the
 *   cart; every add-to-cart path calls it before adding the product.
 * - KCPlanSelect.plan(planId): type, interval, deliveries, Check-up Reward, duos, brushings and Return
 *   on Care of a plan, by ID: the pricing summary, the plan cards, the Welcome Kit and the sticky bar
 *   read plans here instead of by name. selectedPlanId() and allowed() serve the sticky bar and
 *   karmi-add-to-cart.js.
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
  // How long a compare choice is kept against Loop's own late default selection
  const INTENT_GUARD_MS = 3000;
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
  // Last real click or change on a plan control (Loop widgets, sticky bar) by the shopper
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

  // Loop may still run its own default selection (300-500 ms timers, its background step) right after
  // a compare choice. For a short while, put the shopper's choice back if Loop (not the shopper)
  // switches the plan, then check the settled form once more.
  function guardIntent(product, widget, plan, label) {
    const state = runtimeOf(product.id);
    const intent = { planId: plan.id, label: label, at: Date.now(), until: Date.now() + INTENT_GUARD_MS, restores: 0 };
    state.intent = intent;
    setTimeout(() => {
      if (state.intent !== intent) return;
      state.intent = null;
      if (lastPlanControlAt > intent.at) return;
      const current = products[product.id] ? buyboxOf(products[product.id]) : null;
      if (current && formPlanId(current) !== plan.id) {
        warn(label + ': the buybox moved from selling plan ' + plan.id + ' to "' + formPlanId(current) + '" without the shopper');
      }
    }, INTENT_GUARD_MS + 100);
  }

  function keepIntent(product) {
    const state = runtimeOf(product.id);
    const intent = state.intent;
    if (!intent) return false;
    if (Date.now() > intent.until || lastPlanControlAt > intent.at) {
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
      duos: fromOption('duos', entry.duos ? entry.duos.duos : 1),
      brushings: fromOption('brushings', entry.duos ? entry.duos.brushings : 120),
      returnOnCare: fromOption('returnOnCare', entry.duos ? entry.duos.returnOnCare : 0),
    };
  }

  // The selling plan the buybox form will buy ('' for one time)
  function selectedPlanId(productId) {
    readConfigs();
    const product = products[String(productId)];
    const widget = product && buyboxOf(product);
    return widget ? formPlanId(widget) : '';
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
  // "Subscription Name" for the coming choice (cleared for one time). The caller then adds the choice,
  // with one kit set for a subscription. Kit lines: the _welcome_kit property, the configured kit
  // variants, or the earlier kit's toothbrush variants. Resolves false for a product without a plan
  // config (nothing changed); rejects when the cart could not be updated.
  async function clearPurchaseChoice(productId, sellingPlanId) {
    readConfigs();
    const product = products[String(productId)];
    if (!product) return false;
    const headers = { 'Content-Type': 'application/json', 'X-Karmi-Sync': 'false' };
    const cart = await fetch('/cart.js', { headers: headers }).then((response) => response.json());
    const kitVariantIds = product.kitVariantIds.concat(LEGACY_KIT_VARIANT_IDS);
    const updates = {};
    (cart.items || []).forEach((item) => {
      const isKit =
        (item.properties && item.properties._welcome_kit === 'true') || kitVariantIds.includes(String(item.variant_id));
      if (String(item.product_id) === product.id || isKit) updates[item.key] = 0;
    });
    const body = { attributes: { 'Subscription Name': sellingPlanId ? subscriptionName(sellingPlanId) : '' } };
    if (Object.keys(updates).length) body.updates = updates;
    const response = await fetch('/cart/update.js', { method: 'POST', headers: headers, body: JSON.stringify(body) });
    if (!response.ok) throw new Error('could not remove the earlier choice from the cart');
    return true;
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

    if (!on) return;
    if (stolen) recheckBuybox(product);
    if (keepIntent(product)) return;
    keepPublicSelection(product);
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

  const markPlanControl = (event) => {
    if (!event.isTrusted || !event.target || !event.target.closest) return;
    if (event.target.closest(PLAN_CONTROLS)) lastPlanControlAt = Date.now();
  };
  document.addEventListener('click', markPlanControl, true);
  document.addEventListener('change', markPlanControl, true);

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
    clearPurchaseChoice: clearPurchaseChoice,
    productIdOfVariant: productIdOfVariant,
    plan: plan,
    selectedPlanId: selectedPlanId,
    allowed: allowed,
    refresh: init,
  };
})();
