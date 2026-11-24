/* Preview only (/copy/ variant, docs/buybox-ab/PLAN.md 4b): the copy proposals that the theme draws
   itself, per selected plan, over the whole buybox: the Year's "per Duo" line, the receipt (rows, total
   sub-line, a shipping row), the CTA for Try once and the trust row under the CTA. Not theme code: what
   Victor keeps becomes kc.* keys, block settings and lines in assets/loop-widget.js. Writes only what
   differs, so the theme's own updates and this observer settle. */
(function () {
  var ONCE = 'loop-one-time-purchase';
  var RHYTHM = 'cd1642b170e8d8908d90eaf39d58957e5a4ae5ac';
  var YEAR = 'ab8930cda8d5182e7420ef18797bb86a2f9ae26c';
  var YEAR_DUOS = 6;

  var COPY = {
    creditTitle: 'Care Credit back, to spend on more care',
    creditTip: 'Care Credit is Karmicare credit in euros, to spend on member products and accessories. It lands in your account with your plan, so caring for your teeth pays you back.',
    checkupTitle: 'After a dental check-up from month 6',
    kitTemplate: 'Welcome Kit with your first order ([value] value)',
    shipping: 'Shipping',
    shippingFree: 'Free',
    // "+ shipping" right after the per-brushing price, no sentence of its own (Victor, 24 Nov)
    onceSub: '[price] per brushing + shipping',
    rhythmSub: 'Then [price] every 60 days. Pause or stop anytime.',
    yearSub: 'Then [price] once a year. Stop anytime before your renewal.',
    // Victor's own text (24 Nov), in place of the VOORSTEL "Begin your first Duo"
    onceCta: 'Try once, purchase now',
    trust: {
      // Shipping is already in the card and the receipt: two items for Try once
      once: ['14-day money-back guarantee', 'One Duo, no renewal'],
      rhythm: ['60-day money-back guarantee', 'Pause or stop anytime', 'Free shipping'],
      year: ['60-day money-back guarantee', 'Stop anytime before renewal', 'Free shipping'],
    },
  };

  function set(el, text) {
    if (el && el.textContent !== text) el.textContent = text;
  }

  function cents(text) {
    var euros = parseFloat(String(text).replace(/[^\d.,]/g, '').replace(',', '.'));
    return euros ? Math.round(euros * 100) : 0;
  }

  function yearPerDuo(box) {
    box.querySelectorAll('.loop-subscription-group').forEach(function (group) {
      var radio = group.querySelector('.loop-subscription-group-radio');
      if (!radio || radio.dataset.id !== YEAR) return;
      var sub = group.querySelector('.kc-plan-subrow');
      var price = group.querySelector('.loop-subscription-group-price-amount');
      var total = price && cents(price.textContent);
      if (!sub || !total) return;
      var text = loopFormatMoney(Math.round(total / YEAR_DUOS), true) + ' per Duo, billed once a year';
      var line = sub.querySelector('.kc-copy-per-duo');
      if (line && line.textContent === text && sub.children[1] === line) return;
      if (!line) {
        line = document.createElement('div');
        line.className = 'kc-copy-per-duo';
      }
      line.textContent = text;
      sub.insertBefore(line, sub.children[1] || null);
    });
  }

  function receipt(box, plan) {
    var summary = box.querySelector('.kc-pricing-summary[id^="kc-pricing-summary-"]');
    if (!summary) return;
    set(summary.querySelector('.kc-care-credit-row > div > span:first-child'), COPY.creditTitle);
    set(summary.querySelector('.kc-care-credit-row .info-tip-popover'), COPY.creditTip);
    set(summary.querySelector('.kc-checkup-reward-row > div > span:first-child'), COPY.checkupTitle);

    var kit = summary.querySelector('.kc-welcome-kit-row');
    var kitLabel = kit && kit.querySelector('.kc-welcome-kit-label');
    if (kitLabel) {
      var value = (kitLabel.textContent.match(/€\s?[\d.,]+|[\d.,]+\s?€/) || [''])[0];
      if (kitLabel.dataset.template !== COPY.kitTemplate) kitLabel.dataset.template = COPY.kitTemplate;
      if (value) set(kitLabel, COPY.kitTemplate.replace('[value]', value));
    }

    // Members ship free: a row of its own, after the Welcome Kit, as the receipt's other rows
    var rewards = summary.querySelector('.kc-pricing-summary__rewards');
    var shipping = summary.querySelector('.kc-copy-shipping-row');
    if (rewards && kit && !shipping) {
      shipping = kit.cloneNode(true);
      shipping.className = 'kc-reward-row kc-copy-shipping-row';
      shipping.removeAttribute('style');
      shipping.querySelector('.kc-welcome-kit-label').className = 'kc-copy-shipping-label';
      shipping.querySelector('.kc-welcome-kit-value').className = 'kc-copy-shipping-value';
      rewards.appendChild(shipping);
    }
    if (shipping) {
      set(shipping.querySelector('.kc-copy-shipping-label'), COPY.shipping);
      // The same word as the Welcome Kit's value ("FREE"), so the two rows read alike
      var kitValue = kit.querySelector('.kc-welcome-kit-value');
      set(shipping.querySelector('.kc-copy-shipping-value'), (kitValue && kitValue.textContent.trim()) || COPY.shippingFree);
      var display = plan === ONCE ? 'none' : 'flex';
      if (shipping.style.display !== display) shipping.style.display = display;
    }

    var price = summary.querySelector('.kc-pricing-summary__price');
    var sub = summary.querySelector('.kc-pricing-summary__per-brushing');
    var interval = summary.querySelector('.kc-pricing-summary__interval');
    var total = price ? price.textContent.trim() : '';
    if (plan === ONCE && total) {
      // One Duo is 120 brushings, as the card
      set(sub, COPY.onceSub.replace('[price]', loopFormatMoney(Math.round(cents(total) / 120), true)));
    } else if (plan === RHYTHM && total) {
      set(sub, COPY.rhythmSub.replace('[price]', total));
      set(interval, '');
    } else if (plan === YEAR && total) {
      set(sub, COPY.yearSub.replace('[price]', total));
      set(interval, '');
    }
  }

  function cta(box, plan) {
    if (plan !== ONCE) return;
    set(box.querySelector('.product-form__custom-submit .kc-cta-label'), COPY.onceCta);
  }

  function trust(box, plan) {
    var lines = plan === ONCE ? COPY.trust.once : plan === YEAR ? COPY.trust.year : plan === RHYTHM ? COPY.trust.rhythm : null;
    if (!lines) return;
    box.querySelectorAll('.icon-with-text__item .inline-richtext').forEach(function (el, i) {
      if (lines[i]) set(el, lines[i]);
      var item = el.closest('.icon-with-text__item');
      var display = lines[i] ? '' : 'none';
      if (item && item.style.display !== display) item.style.display = display;
    });
  }

  function apply() {
    var box = document.querySelector('.kc-buybox');
    if (!box || typeof loopFormatMoney !== 'function') return;
    var checked = box.querySelector('input[name="loop_purchase_option"]:checked');
    var plan = checked ? checked.dataset.id : '';
    yearPerDuo(box);
    receipt(box, plan);
    cta(box, plan);
    trust(box, plan);
  }

  new MutationObserver(apply).observe(document.documentElement, { childList: true, subtree: true, characterData: true });
  document.addEventListener('change', function () { setTimeout(apply, 0); }, true);
  apply();
})();
