/* kc-practitioner-request.js: the practitioner request form in the PDP FAQ
   (snippets/kc-practitioner-request.liquid, R76; popup R76b; fallback R76c).

   - Finds the trigger link in the answer text of the FAQ item that holds the form (href contains
     data-trigger-url, else text contains data-trigger-text) and swaps it for a button with the same
     content. The form panel moves into a modal <dialog> on body (a dialog inside a closed <details>
     would not render), which that button opens. No link found, or no showModal(): the form stays
     inline, as without JavaScript. If showModal() throws when it is called, the panel, the link
     and the inline form come back in the FAQ item and the page is not locked.
   - The dialog, as the professionals quote panel: showModal, scrim, close button, Escape and a
     click on the scrim close it, body.overflow-hidden locks the page. Focus goes to the form title
     (no keyboard popping up on phones), Tab wraps inside the dialog, and on close focus returns to
     the button.
   - Checks the fields before the post: name, profession, email, at least one of evidence pack and
     samples, and the practice address when samples is ticked. Messages come from the settings.
   - Shopify reloads the page after the post. The item is already open (Liquid); the dialog opens
     again with the thank-you (announced) or the alert, and focus goes there. On an error the fields
     Shopify does not give back are restored from this tab's sessionStorage, which is cleared again
     at once.
   - With the Klaviyo key set (data-klaviyo-company), the thank-you reload sends one event with the
     request from that same sessionStorage snapshot to Klaviyo's public endpoint; Klaviyo's flow
     emails the confirmation and the team alert. Only after Shopify accepted the post, so a refused
     or stopped post confirms nothing. No snapshot (storage blocked): no event, the request itself
     still arrives in the store inbox. */

(function () {
  'use strict';

  var STORE_KEY = 'kc-practitioner-request';
  var EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  var RESTORED = ['profession', 'pack', 'samples', 'address', 'name', 'phone', 'body'];
  var KLAVIYO_EVENTS = 'https://a.klaviyo.com/client/events/';
  var KLAVIYO_REVISION = '2026-10-15';
  var KLAVIYO_METRIC = 'Practitioner Request Submitted';

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
    var dialog = null;
    var button = null;
    var home = null;

    if (link && typeof document.createElement('dialog').showModal === 'function') {
      button = document.createElement('button');
      button.type = 'button';
      button.className = 'kc-pr-trigger';
      button.innerHTML = link.innerHTML;
      /* marks the panel's place in the FAQ item, for the inline fallback */
      home = document.createComment('kc-practitioner-request');
      root.parentNode.insertBefore(home, root);
      dialog = buildDialog(root, stateName, afterClose);
      button.setAttribute('aria-haspopup', 'dialog');
      button.setAttribute('aria-controls', dialog.id);
      link.replaceWith(button);
      button.addEventListener('click', function () {
        show(null);
      });
      dialog.addEventListener('close', afterClose);
    }

    /* Opens the dialog and focuses the target: the thank-you or the alert after a reload, else the
       form title. The page is locked only once showModal() has worked. If it throws, the form goes
       back inline into the FAQ item, as without JavaScript. An open dialog is not opened twice. */
    function show(target) {
      if (dialog && !dialog.open) {
        try {
          dialog.showModal();
        } catch (error) {
          backInline();
        }
      }
      var focus = target || root.querySelector('.kc-pr__title') || form.querySelector('input:not([type=hidden])');
      if (focus && !focus.hasAttribute('tabindex') && !/^(INPUT|TEXTAREA|BUTTON|A)$/.test(focus.tagName)) {
        focus.setAttribute('tabindex', '-1');
      }
      if (!dialog) {
        reveal(focus);
        return;
      }
      document.body.classList.add('overflow-hidden');
      dialog.scrollTop = 0;
      if (focus) focus.focus();
    }

    /* The inline form of R76: the panel back in its place under the answer, the original link
       back, the dialog gone, the item open */
    function backInline() {
      home.parentNode.insertBefore(root, home);
      home.remove();
      button.replaceWith(link);
      dialog.removeEventListener('close', afterClose);
      dialog.remove();
      dialog = null;
      button = null;
      var item = root.closest('.kc-faq-item');
      if (item) item.open = true;
    }

    /* The close button and the scrim call this at once; Escape reaches it through the close event,
       which the browser fires a task later */
    function afterClose() {
      if (!button || !document.body.classList.contains('overflow-hidden')) return;
      document.body.classList.remove('overflow-hidden');
      button.focus();
    }

    if (stateName === 'success') {
      var sent = store('get');
      store('clear');
      sendEvent(root, sent);
      var live = root.querySelector('[data-kc-pr-live]');
      if (live) {
        /* re-set the text so screen readers announce the live region after the reload */
        var message = live.textContent;
        live.textContent = '';
        window.setTimeout(function () {
          live.textContent = message;
        }, 150);
      }
      show(state);
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
      /* for the Klaviyo event on the thank-you reload */
      snapshot.email = fields.email ? fields.email.value.trim() : '';
      snapshot.language = hiddenValue(form, 'Language');
      snapshot.page = hiddenValue(form, 'Page');
      snapshot.at = new Date().toISOString();
      snapshot.id = uid();
      store('set', snapshot);
    });

    /* last, so the checks above are in place whatever happens when the dialog opens */
    if (stateName === 'error') show(state);
  }

  function hiddenValue(form, key) {
    var input = form.querySelector('input[type=hidden][name="contact[' + key + ']"]');
    return input ? input.value : '';
  }

  function uid() {
    if (window.crypto && typeof window.crypto.randomUUID === 'function') return window.crypto.randomUUID();
    return String(Date.now()) + '-' + Math.random().toString(16).slice(2);
  }

  /* One event to Klaviyo's public endpoint (the same call as the withdrawal page). The profile gets
     the email only: practitioners often type a title ("Dr. An Peeters"), so the flow emails greet
     with event.name as typed instead of a split first name. The request itself travels as event
     properties. Fire and forget: the thank-you is already on screen and does not depend on it. */
  function sendEvent(root, saved) {
    var company = (root.getAttribute('data-klaviyo-company') || '').trim();
    if (!company || !saved || !saved.email || typeof window.fetch !== 'function') return;
    var metric = (root.getAttribute('data-klaviyo-metric') || '').trim() || KLAVIYO_METRIC;
    var payload = {
      data: {
        type: 'event',
        attributes: {
          metric: { data: { type: 'metric', attributes: { name: metric } } },
          profile: { data: { type: 'profile', attributes: { email: saved.email } } },
          properties: {
            name: (saved.name || '').trim(),
            profession: saved.profession || '',
            email: saved.email,
            phone: saved.phone || '',
            evidence_pack: !!saved.pack,
            samples: !!saved.samples,
            practice_address: saved.samples ? saved.address || '' : '',
            message: saved.body || '',
            language: saved.language || '',
            page: saved.page || '',
          },
          time: saved.at,
          unique_id: saved.id || uid(),
        },
      },
    };
    window
      .fetch(KLAVIYO_EVENTS + '?company_id=' + encodeURIComponent(company), {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', revision: KLAVIYO_REVISION },
        body: JSON.stringify(payload),
        keepalive: true,
      })
      .catch(function () {
        /* offline or blocked: the request is in the store inbox all the same */
      });
  }

  function reveal(el) {
    if (!el) return;
    el.focus({ preventScroll: true });
    el.scrollIntoView({ block: 'center' });
  }

  function buildDialog(root, stateName, onClose) {
    var dialog = document.createElement('dialog');
    dialog.className = 'kc-pr-dialog';
    dialog.id = 'KcPractitionerRequest-dialog';
    var success = stateName === 'success';
    var label = document.getElementById(success ? 'KcPr-success-title' : 'KcPr-title');
    var description = document.getElementById(success ? 'KcPr-success-text' : 'KcPr-intro');
    if (label) dialog.setAttribute('aria-labelledby', label.id);
    if (description) dialog.setAttribute('aria-describedby', description.id);

    var bar = document.createElement('div');
    bar.className = 'kc-pr-dialog__bar';
    var closeTemplate = root.querySelector('template[data-kc-pr-dialog-close]');
    if (closeTemplate) bar.appendChild(closeTemplate.content.cloneNode(true));
    dialog.appendChild(bar);
    dialog.appendChild(root);
    document.body.appendChild(dialog);

    function closeNow() {
      dialog.close();
      onClose();
    }

    var close = dialog.querySelector('[data-kc-pr-close]');
    if (close) close.addEventListener('click', closeNow);

    /* The panel is the dialog box, so a press that starts and ends on the dialog itself, outside
       its box, is a click on the scrim (a text selection dragged out of a field is not) */
    var pressedOnScrim = false;
    function onScrim(event) {
      if (event.target !== dialog) return false;
      var box = dialog.getBoundingClientRect();
      return event.clientX < box.left || event.clientX > box.right || event.clientY < box.top || event.clientY > box.bottom;
    }
    dialog.addEventListener('pointerdown', function (event) {
      pressedOnScrim = onScrim(event);
    });
    dialog.addEventListener('click', function (event) {
      if (pressedOnScrim && onScrim(event)) closeNow();
      pressedOnScrim = false;
    });

    /* Tab and Shift+Tab wrap inside the dialog instead of leaving for the browser bar */
    dialog.addEventListener('keydown', function (event) {
      if (event.key !== 'Tab') return;
      var focusable = Array.prototype.filter.call(
        dialog.querySelectorAll('button, [href], input:not([type=hidden]), textarea, select, [tabindex]:not([tabindex="-1"])'),
        function (el) {
          return !el.disabled && el.getClientRects().length > 0;
        }
      );
      if (!focusable.length) return;
      var first = focusable[0];
      var last = focusable[focusable.length - 1];
      if (event.shiftKey && (document.activeElement === first || !dialog.contains(document.activeElement))) {
        event.preventDefault();
        last.focus();
      } else if (!event.shiftKey && document.activeElement === last) {
        event.preventDefault();
        first.focus();
      }
    });
    return dialog;
  }

  Array.prototype.forEach.call(document.querySelectorAll('[data-kc-pr]'), init);
})();
