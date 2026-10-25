/* kc-practitioner-request.js: the practitioner request form in the PDP FAQ
   (snippets/kc-practitioner-request.liquid, R76).

   - Finds the trigger link in the answer text of the FAQ item that holds the form (href contains
     data-trigger-url, else text contains data-trigger-text) and swaps it for a button with the same
     content that shows and hides the form. No link found: the form stays visible, as without
     JavaScript.
   - Checks the fields before the post: name, profession, email, at least one of evidence pack and
     samples, and the practice address when samples is ticked. Messages come from the settings.
   - Shopify reloads the page after the post. Success: the item is already open (Liquid), the
     thank-you is announced, focused and scrolled into view. Shopify refused it: the alert is
     focused and the fields Shopify does not give back are restored from this tab's sessionStorage,
     which is cleared again at once. */

(function () {
  'use strict';

  var STORE_KEY = 'kc-practitioner-request';
  var EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  var RESTORED = ['profession', 'pack', 'samples', 'address', 'name', 'phone', 'body'];

  function store(action, value) {
    try {
      if (action === 'set') window.sessionStorage.setItem(STORE_KEY, JSON.stringify(value));
      if (action === 'get') return JSON.parse(window.sessionStorage.getItem(STORE_KEY) || 'null');
      if (action === 'clear') window.sessionStorage.removeItem(STORE_KEY);
    } catch (e) {
      /* private window or storage blocked: nothing to restore */
    }
    return null;
  }

  function findTrigger(root) {
    var item = root.closest('.kc-faq-item');
    var answer = item && item.querySelector('.kc-faq-description');
    if (!answer) return null;
    var links = Array.prototype.slice.call(answer.querySelectorAll('a'));
    var url = root.getAttribute('data-trigger-url') || '';
    var text = (root.getAttribute('data-trigger-text') || '').toLowerCase();
    var found = null;
    if (url) {
      found = links.filter(function (a) {
        return (a.getAttribute('href') || '').indexOf(url) !== -1;
      })[0];
    }
    if (!found && text) {
      found = links.filter(function (a) {
        return a.textContent.toLowerCase().indexOf(text) !== -1;
      })[0];
    }
    return found || null;
  }

  function init(root) {
    var form = root.querySelector('form');
    if (!form) return;
    var state = root.querySelector('[data-kc-pr-state]');
    var stateName = state ? state.getAttribute('data-kc-pr-state') : '';
    var link = findTrigger(root);

    if (link) {
      var button = document.createElement('button');
      button.type = 'button';
      button.className = 'kc-pr-trigger';
      button.innerHTML = link.innerHTML;
      button.setAttribute('aria-controls', root.id);
      link.replaceWith(button);
      root.classList.add('kc-pr--js');
      setOpen(!!stateName);
      button.addEventListener('click', function () {
        setOpen(root.hidden);
      });
    }

    function setOpen(open) {
      root.hidden = !open;
      if (button) button.setAttribute('aria-expanded', open ? 'true' : 'false');
    }

    if (stateName === 'success') {
      store('clear');
      var live = root.querySelector('[data-kc-pr-live]');
      if (live) {
        /* re-set the text so screen readers announce the live region after the reload */
        var message = live.textContent;
        live.textContent = '';
        window.setTimeout(function () {
          live.textContent = message;
        }, 150);
      }
      reveal(state);
      return;
    }

    form.noValidate = true;
    var fields = {};
    Array.prototype.forEach.call(form.querySelectorAll('[data-kc-pr-field]'), function (el) {
      fields[el.getAttribute('data-kc-pr-field')] = el;
    });
    var group = form.querySelector('[data-kc-pr-group="wants"]');

    if (stateName === 'error') {
      var saved = store('get');
      store('clear');
      if (saved) {
        RESTORED.forEach(function (key) {
          var el = fields[key];
          if (!el || !(key in saved)) return;
          if (el.type === 'checkbox') el.checked = !!saved[key];
          else if (!el.value) el.value = saved[key];
        });
      }
      reveal(state);
    } else {
      store('clear');
    }

    function syncAddress() {
      var needed = fields.samples && fields.samples.checked;
      if (!fields.address) return;
      fields.address.required = !!needed;
      fields.address.setAttribute('aria-required', needed ? 'true' : 'false');
      if (!needed) showError(fields.address, '');
    }

    function errorFor(el) {
      var describedBy = (el.getAttribute('aria-describedby') || '').split(/\s+/);
      for (var i = 0; i < describedBy.length; i++) {
        if (/-error$/.test(describedBy[i])) return document.getElementById(describedBy[i]);
      }
      return null;
    }

    function showError(el, message) {
      var box = errorFor(el);
      if (message) el.setAttribute('aria-invalid', 'true');
      else el.removeAttribute('aria-invalid');
      if (!box) return;
      box.textContent = message;
      box.hidden = !message;
    }

    function check(key) {
      var el = fields[key];
      if (!el) return '';
      var value = el.value.trim();
      if (key === 'email') {
        if (!value) return el.getAttribute('data-error-required');
        if (!EMAIL_RE.test(value)) return el.getAttribute('data-error-format');
        return '';
      }
      if (key === 'address' && !(fields.samples && fields.samples.checked)) return '';
      return value ? '' : el.getAttribute('data-error-required');
    }

    function checkGroup() {
      var ok = (fields.pack && fields.pack.checked) || (fields.samples && fields.samples.checked);
      return ok ? '' : group.getAttribute('data-error-required');
    }

    function validate() {
      var firstBad = null;
      ['name', 'profession', 'email'].forEach(function (key) {
        var message = check(key);
        showError(fields[key], message);
        if (message && !firstBad) firstBad = fields[key];
      });
      var groupMessage = checkGroup();
      showError(group, groupMessage);
      if (groupMessage && !firstBad) firstBad = fields.pack;
      var addressMessage = check('address');
      showError(fields.address, addressMessage);
      if (addressMessage && !firstBad) firstBad = fields.address;
      return firstBad;
    }

    if (fields.samples) fields.samples.addEventListener('change', syncAddress);
    syncAddress();

    /* once a message shows, it updates as the visitor fixes the field */
    ['name', 'profession', 'email', 'address'].forEach(function (key) {
      var el = fields[key];
      if (!el) return;
      el.addEventListener('input', function () {
        if (el.getAttribute('aria-invalid') === 'true') showError(el, check(key));
      });
    });
    [fields.pack, fields.samples].forEach(function (el) {
      if (!el) return;
      el.addEventListener('change', function () {
        if (group.getAttribute('aria-invalid') === 'true') showError(group, checkGroup());
      });
    });

    form.addEventListener('submit', function (event) {
      var firstBad = validate();
      if (firstBad) {
        event.preventDefault();
        firstBad.focus();
        return;
      }
      var snapshot = {};
      RESTORED.forEach(function (key) {
        var el = fields[key];
        if (!el) return;
        snapshot[key] = el.type === 'checkbox' ? el.checked : el.value;
      });
      store('set', snapshot);
    });
  }

  function reveal(el) {
    if (!el) return;
    el.focus({ preventScroll: true });
    el.scrollIntoView({ block: 'center' });
  }

  Array.prototype.forEach.call(document.querySelectorAll('[data-kc-pr]'), init);
})();
