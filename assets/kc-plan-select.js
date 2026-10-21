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
 * - KCPlanSelect.nestKit(lines) / kitLines(productId) / repairKit(): the cart and checkout order, the plan
 *   line on top with Morning Toothbrush, Evening Toothbrush, Floss nested under it (KIT_ORDER): every add
 *   of a plan with its Welcome Kit sends its lines through nestKit; kitLines gives the kit lines a plan
 *   product's subscription brings; repairKit puts a missing or loose kit under the plan line.
 * - KCPlanSelect.units(planId) / quantityFor(productId, planId, formQuantity): the Duos per delivery of a
 *   plan (snippets/kc-plan-type.liquid; year plans follow the theme setting "Year plans: Duos per
 *   delivery"), which is the cart quantity. Every add-to-cart path adds that quantity for a
 *   subscription, and every price shown for a plan is Shopify's price per quantity x quantity, which is
 *   what the checkout charges. For a year plan that is Shopify's year price per quantity x quantity
 *   (€118 x 3 = €354): a year price, never a per-Duo price.
 * - Allowlist: the groups without a public plan stay hidden and unselectable in every Loop widget and
 *   the sticky bar; a non-public plan selected in the buybox is replaced by the first public one.
 * - KCPlanSelect.buy(productId, planId, title, groupId, button): that public plan straight to checkout,
 *   through karmiAddToCart as a fixed offer with the buybox form; a plan the page cannot sell is chosen
 *   in the buybox instead.
 * - Comparison table buttons (sections/product-compare-plans.liquid, sections/comparison-table.liquid)
 *   carry data-kc-plan-choose: "plan" (with data-selling-plan-id, data-selling-plan-group-id: buy) or
 *   "once" (tryOnce).
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
  // Cart and checkout order (Victor, 16 Oct): the plan line on top, then Morning Toothbrush, Evening
  // Toothbrush, Floss. The kit lines are nested under the plan line (Shopify nested cart lines: parent_id
  // in the same add, parent_line_key later). Shopify lists nested lines right after their parent in the
  // order they were added, checkout shows them indented under it, and removing the plan line removes
  // them. So every add sends the plan line, then the kit lines in this order (see nestKit). This is the
  // one place of that rule: a kit line's place comes from its product handle (kitHandles,
  // snippets/kc-plan-config.liquid), never from the order of the Welcome Kit theme setting. A kit line it
  // cannot place goes under them.
  const KIT_ORDER = ['morning', 'evening', 'floss'];

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
        (products[productId] = {
          id: productId,
          widgets: [],
          plans: {},
          groups: {},
          publicCount: 0,
          kitVariantIds: [],
          kitHandles: {},
          welcomeKit: false,
        });
      if (!product.shopCurrency && config.shopCurrency) product.shopCurrency = config.shopCurrency;
      (config.kitVariantIds || []).forEach((id) => {
        if (!product.kitVariantIds.includes(String(id))) product.kitVariantIds.push(String(id));
      });
      Object.keys(config.kitHandles || {}).forEach((id) => {
        product.kitHandles[String(id)] = String(config.kitHandles[id]);
      });
      if (config.welcomeKit === true) product.welcomeKit = true;
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
    return Promise.resolve(window.karmiAddToCart(form, button || null, { oneTime: true })).then(
      () => true
    );
  }

  // A comparison table plan button buys its plan straight to checkout (Victor, 20 Oct): the buybox
  // form's variant on that plan, through karmiAddToCart as a fixed offer (like the end CTA), so the add
  // is the buybox's own: Duos per delivery, Welcome Kit nested under the plan line, "Subscription Name",
  // one purchase choice. A plan this page cannot sell buys nothing: it is selected in the buybox instead.
  function buy(productId, planId, title, groupId, button) {
    readConfigs();
    const label = '"' + (title || 'plan') + '"';
    const id = String(planId == null ? '' : planId).trim();
    const product = products[String(productId)];
    const widget = product && buyboxOf(product);
    const form = widget && formOf(widget);
    const plan = product && /^\d+$/.test(id) ? product.plans[id] : null;
    let problem = '';
    if (!form) {
      problem = 'no buybox form for product ' + productId;
    } else if (typeof window.karmiAddToCart !== 'function') {
      problem = 'karmiAddToCart is not loaded';
    } else if (!plan) {
      problem = '"' + id + '" is not a selling plan ID of this product';
    } else if (enforced(product) && !plan.public) {
      problem = 'selling plan ' + id + ' (' + plan.groupName + ') is not public';
    } else if (groupId && groupId !== plan.groupId) {
      problem = 'selling plan ' + id + ' belongs to group ' + plan.groupId + ', not ' + groupId;
    } else if (allocated(product, currentVariantId(product, widget, containerOf(widget)), id) === false) {
      problem = 'selling plan ' + id + ' (' + plan.groupName + ') is not offered for the selected variant';
    }
    if (problem) {
      warn(label + ': ' + problem + '; nothing bought, choosing it in the buybox instead');
      return choose(productId, id, title, groupId);
    }
    const kit = kitLines(productId);
    return Promise.resolve(
      window.karmiAddToCart(form, button || null, {
        sellingPlanId: id,
        isBundleProduct: kit.length > 0,
        welcomeKitVariantIds: kit.map((line) => String(line.id)),
      })
    ).then(() => true);
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

  const checkedTotals = {};

  function euros(cents) {
    return (cents / 100).toFixed(2);
  }

  // While year plans are more than 1 Duo per delivery, each year plan must cost its expected year total
  // (snippets/kc-plan-type.liquid) at checkout: Shopify's year price per quantity x quantity. Warn when
  // it does not, e.g. a year price per quantity in Loop that is still the full year (€354 x 3 = €1,062
  // instead of €354). Prices in another currency than the shop's are not checked.
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
          'year plan ' + entry.id + ' (' + entry.groupName + ', variant ' + variant.id + "): Shopify's year " +
          'price per quantity ' + euros(allocation.price) + ' x quantity ' + count + ' = ' + euros(total);
        if (entry.expectedTotal == null) {
          warn(what + ', and snippets/kc-plan-type.liquid has no expected total for it');
        } else if (total !== entry.expectedTotal) {
          warn(what + ', expected ' + euros(entry.expectedTotal) + ': the checkout charges ' + euros(total) + '; check the year price per quantity in Loop');
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

  // A Welcome Kit line: the _welcome_kit property, a configured kit variant or the earlier kit's toothbrushes
  function isKitLine(line) {
    if (!line) return false;
    if (line.properties && line.properties._welcome_kit === 'true') return true;
    const id = String(line.id);
    return (
      LEGACY_KIT_VARIANT_IDS.includes(id) ||
      Object.keys(products).some((productId) => products[productId].kitVariantIds.includes(id))
    );
  }

  // A kit line's place in KIT_ORDER by its product handle; KIT_ORDER.length when it has none
  function kitRank(line) {
    const id = String(line.id);
    const owner = Object.keys(products).find((productId) => products[productId].kitHandles[id]);
    const handle = owner ? products[owner].kitHandles[id] : '';
    const rank = KIT_ORDER.findIndex((word) => handle.includes(word));
    return rank === -1 ? KIT_ORDER.length : rank;
  }

  // The lines of one /cart/add.js call ({ id: variant ID, … }) in cart order (KIT_ORDER): the other lines
  // (the plan line) as given, then the kit lines, each nested under the plan line (parent_id: its variant
  // ID; the subscription line when there are several). Without a line to nest under, kit lines stay as
  // they are. Every add of a plan with its kit goes through this.
  function nestKit(lines) {
    readConfigs();
    const list = Array.isArray(lines) ? lines : [];
    const others = list.filter((line) => !isKitLine(line));
    const parent = others.find((line) => line.selling_plan) || others[0];
    const kit = list
      .filter(isKitLine)
      .sort((a, b) => kitRank(a) - kitRank(b))
      .map((line) => (parent ? Object.assign({}, line, { parent_id: Number(parent.id) }) : line));
    return others.concat(kit);
  }

  // The Welcome Kit lines a subscription of a plan product brings in its own add (kc-plan-config: a Welcome
  // Kit bundle product, for a customer who has not received the kit yet), in KIT_ORDER; [] otherwise
  function kitLines(productId) {
    readConfigs();
    const product = products[String(productId)];
    if (!product || !product.welcomeKit) return [];
    return product.kitVariantIds
      .map((id) => ({ id: Number(id), quantity: 1, properties: { _welcome_kit: 'true' } }))
      .sort((a, b) => kitRank(a) - kitRank(b));
  }

  // One purchase choice of a plan product in the cart (Victor, 15 Oct: the cart held a 60-day and a Year
  // membership after a switch). Before a new choice of the product is added, one update call removes
  // every line of the product (any plan or one time) and every Welcome Kit line, and sets
  // "Subscription Name" for the coming choice (cleared for one time). The caller then adds the choice as
  // one line (quantityFor: the plan's Duos per delivery, 1 for Try Once), with one kit set for a
  // subscription nested under it (nestKit). Kit lines: isKitLine. Resolves false for a product without a plan
  // config (nothing changed), else what it removed (recoverChoice puts it back after a failed add); rejects when the cart
  // could not be updated. Callers go through replaceChoice().
  async function clearPurchaseChoice(productId, sellingPlanId) {
    readConfigs();
    const product = products[String(productId)];
    if (!product) return false;
    const headers = { 'Content-Type': 'application/json', 'X-Karmi-Sync': 'false' };
    const cart = await fetch('/cart.js', { headers: headers }).then((response) => response.json());
    const updates = {};
    const removed = [];
    (cart.items || []).forEach((item) => {
      const isKit = isKitLine({ id: item.variant_id, properties: item.properties });
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
        // In cart order (nestKit): the earlier plan line back, its kit nested under it
        const added = await fetch('/cart/add.js', {
          method: 'POST',
          headers: headers,
          body: JSON.stringify({ items: nestKit(removed.lines) }),
        });
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
  // The comparison table attempt whose add call is starting (set by attempt() around its call)
  let tableAttempt = null;
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
    // A comparison table attempt (attempt()) learns that its own add failed before karmiAddToCart, which
    // awaits this result, writes the error: registered first, this runs first
    const owner = tableAttempt;
    if (owner) {
      result.then(
        (response) => {
          if (!response.ok) owner.failed();
        },
        (error) => {
          if (!(error && error.kcSkipped)) owner.failed();
        }
      );
    }
    return result;
  }

  // true for a product with a plan config on this page (its choice goes through replaceChoice)
  function manages(productId) {
    readConfigs();
    return Boolean(products[String(productId)]);
  }

  // A plan subscription in the cart without exactly its Welcome Kit under it: each kit line of kitLines
  // once, its quantity, in KIT_ORDER, nested under the plan line (a cart from outside the theme or from
  // before the kit was nested; every add of the theme brings the kit in its own add). On a page that sells
  // the plan product (kitLines), the kit lines in the cart go out and the whole kit goes in under the plan
  // line (parent_line_key; a kit line added on its own would land under the others). The plan line, its
  // quantity and its properties stay as they are; "Subscription Name" follows its plan
  // (syncCartSubscriptionName). It runs in the purchase queue, after every choice asked for before it, and
  // reads the cart in its own turn; it is no shopper's choice (choicesRequested stays), and once the page
  // goes to checkout it leaves the cart alone. When a request is refused, fails or loses its answer, the
  // cart as it is then decides: the kit in place counts as done, kit lines still there stay, and a cart
  // left without kit lines gets the earlier ones back as they were. Resolves true when the kit is in place
  // after a change. snippets/welcome-kit.liquid calls it for every cart with a Welcome Kit subscription.
  function repairKit() {
    const run = async () => {
      if (navigating) return false;
      readConfigs();
      // Off the pages that sell a plan product with a kit: no cart read at all
      if (!Object.keys(products).some((productId) => products[productId].welcomeKit)) return false;
      const headers = { 'Content-Type': 'application/json', 'X-Karmi-Sync': 'false' };
      const post = (url, body) => fetch(url, { method: 'POST', headers: headers, body: JSON.stringify(body) });
      const readCart = () => fetch('/cart.js', { headers: headers }).then((response) => (response.ok ? response.json() : null));
      const kitItemsOf = (cart) =>
        (cart.items || []).filter((item) => isKitLine({ id: item.variant_id, properties: item.properties }));
      const cart = await readCart();
      if (!cart) return false;
      const planItem = (cart.items || []).find((item) => item.selling_plan_allocation && kitLines(item.product_id).length);
      if (!planItem) return false;
      const kit = kitLines(planItem.product_id);
      const inPlace = (kitItems) =>
        kitItems.length === kit.length &&
        kitItems.every(
          (item, index) =>
            item.variant_id === kit[index].id &&
            item.quantity === kit[index].quantity &&
            item.parent_relationship &&
            item.parent_relationship.parent_key === planItem.key
        );
      const kitItems = kitItemsOf(cart);
      if (inPlace(kitItems)) return false;
      let done = false;
      try {
        if (kitItems.length) {
          const updates = {};
          kitItems.forEach((item) => {
            updates[item.key] = 0;
          });
          // Refused: nothing was removed
          if (!(await post('/cart/update.js', { updates: updates })).ok) return false;
        }
        const added = await post('/cart/add.js', {
          items: kit.map((line) => Object.assign({}, line, { parent_line_key: planItem.key })),
        });
        done = added.ok;
      } catch (error) {
        done = false;
      }
      if (!done) {
        // The cart as it is now decides: a lost answer may have come with the change made
        const now = await readCart().catch(() => null);
        if (!now) {
          warn('the Welcome Kit repair failed and the cart could not be read; the kit may be missing');
          return false;
        }
        const kitNow = kitItemsOf(now);
        if (!inPlace(kitNow)) {
          if (kitNow.length || !kitItems.length) {
            warn('the Welcome Kit could not be put under the plan line; the cart is left as it is');
            return false;
          }
          const restored = await post('/cart/add.js', {
            items: kitItems.map((item) => {
              const line = { id: item.variant_id, quantity: item.quantity, properties: item.properties };
              if (item.parent_relationship) line.parent_line_key = item.parent_relationship.parent_key;
              return line;
            }),
          }).catch(() => null);
          warn(
            restored && restored.ok
              ? 'the Welcome Kit could not be put under the plan line; the earlier kit lines are back'
              : 'the Welcome Kit could not be put under the plan line, and the earlier kit lines could not be put back'
          );
          return false;
        }
      }
      await syncCartSubscriptionName(planItem.selling_plan_allocation.selling_plan.id).catch(() => {});
      return true;
    };
    const result = purchaseQueue.then(run, run);
    purchaseQueue = result.catch(() => {});
    return result;
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

  // Comparison table buttons on their way to checkout (R14): aria-busy and a loading status while the
  // attempt runs, a cart error shown at the table (its data-kc-plan-feedback), and the buttons usable
  // again when Back restores the page from the bfcache. The cart and the redirect stay karmiAddToCart's.
  const busyButtons = new Set();

  function feedbackOf(button) {
    const scope = button.closest('[data-kc-plan-feedback-scope]');
    return scope ? scope.querySelector('[data-kc-plan-feedback]') : null;
  }

  function release(button) {
    busyButtons.delete(button);
    button.removeAttribute('aria-busy');
    const feedback = feedbackOf(button);
    const status = feedback && feedback.querySelector('[data-kc-plan-status]');
    if (status) status.textContent = '';
  }

  // The error line karmiAddToCart writes for this product's form (the buybox's): hidden at the start of
  // every attempt, shown only when the cart rejected it
  function cartErrorOf(productId) {
    readConfigs();
    const product = products[String(productId)];
    const widget = product && buyboxOf(product);
    const form =
      (widget && formOf(widget)) ||
      document.querySelector('form[data-loop-product-id="' + String(productId).replace(/\D/g, '') + '"]');
    if (!form) return null;
    return (form.closest('product-form') || document).querySelector('.product-form__error-message-wrapper');
  }

  function attempt(button, run) {
    const feedback = feedbackOf(button);
    const error = feedback && feedback.querySelector('[data-kc-plan-error]');
    const errorText = error && error.querySelector('[data-kc-plan-error-text]');
    const status = feedback && feedback.querySelector('[data-kc-plan-status]');
    if (error) error.hidden = true;
    if (errorText) errorText.textContent = '';
    busyButtons.add(button);
    button.setAttribute('aria-busy', 'true');
    if (status) status.textContent = status.dataset.loadingText || '';
    // One announcement of a failure (R14c, R14d): only when this attempt's own add failed (replaceChoice
    // tells owner.failed() just before karmiAddToCart writes the buybox error line) is that line made
    // non-live, for that one write; done() hides it again, shows the message in the table alert and gives
    // the role back. Other paths' failures and other attempts keep the line as it is.
    const cartError = cartErrorOf(button.dataset.kcPlanProduct);
    const owner = { muted: false, role: null };
    owner.failed = () => {
      if (!cartError || !error || !errorText || owner.muted) return;
      owner.muted = true;
      owner.role = cartError.getAttribute('role');
      cartError.removeAttribute('role');
    };
    const done = () => {
      let message = '';
      if (owner.muted) {
        const line = cartError.querySelector('.product-form__error-message');
        message = !cartError.hidden && line ? line.textContent : '';
        cartError.hidden = true;
        if (owner.role) cartError.setAttribute('role', owner.role);
        owner.muted = false;
      }
      // karmiAddToCart leaves the button disabled only while the page goes to checkout
      if (button.disabled) return;
      release(button);
      if (!message) return;
      errorText.textContent = message;
      error.hidden = false;
    };
    // run() starts in this turn (karmiAddToCart disables the button at once, and its replaceChoice call,
    // made before its first await, takes this attempt as its owner)
    tableAttempt = owner;
    let started;
    try {
      started = new Promise((resolve) => resolve(run()));
    } finally {
      tableAttempt = null;
    }
    return started
      .then(done, (err) => {
        done();
        warn('"' + (button.dataset.kcPlanTitle || 'plan') + '": ' + (err && err.message ? err.message : err));
      });
  }

  window.addEventListener('pageshow', (event) => {
    if (!event.persisted) return;
    busyButtons.forEach((button) => {
      button.disabled = false;
      button.removeAttribute('disabled');
      button.removeAttribute('aria-disabled');
      button.classList.remove('loading');
      const spinner = button.querySelector('.loading__spinner');
      if (spinner) spinner.classList.add('hidden');
      release(button);
    });
  });

  document.addEventListener('click', (event) => {
    const button = event.target.closest && event.target.closest('[data-kc-plan-choose]');
    if (!button) return;
    event.preventDefault();
    const productId = button.dataset.kcPlanProduct;
    // Outside the comparison tables (the sticky bar's Try Once) as before: no busy state, no table feedback
    if (!button.closest('[data-kc-plan-feedback-scope]')) {
      if (button.dataset.kcPlanChoose === 'once') {
        tryOnce(productId, button);
        return;
      }
      choose(productId, button.dataset.sellingPlanId, button.dataset.kcPlanTitle, button.dataset.sellingPlanGroupId);
      return;
    }
    // A click on a button already on its way to checkout does nothing (karmiAddToCart disables it)
    if (button.disabled || button.classList.contains('loading') || busyButtons.has(button)) return;
    if (button.dataset.kcPlanChoose === 'once') {
      attempt(button, () => tryOnce(productId, button));
      return;
    }
    attempt(button, () =>
      buy(productId, button.dataset.sellingPlanId, button.dataset.kcPlanTitle, button.dataset.sellingPlanGroupId, button)
    );
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
    buy: buy,
    subscriptionName: subscriptionName,
    syncCartSubscriptionName: syncCartSubscriptionName,
    replaceChoice: replaceChoice,
    manages: manages,
    productIdOfVariant: productIdOfVariant,
    plan: plan,
    units: units,
    quantityFor: quantityFor,
    nestKit: nestKit,
    kitLines: kitLines,
    repairKit: repairKit,
    selectedPlanId: selectedPlanId,
    selectedVariantId: selectedVariantId,
    allowed: allowed,
    refresh: init,
  };
})();
