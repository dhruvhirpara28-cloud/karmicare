/* kc-practitioner-request.js: the practitioner request form in the PDP FAQ
   (snippets/kc-practitioner-request.liquid, R76; popup R76b; fallback R76c).

   - Finds the trigger links in the FAQ (answers and section content of every item, so also the
     "For dentists" note; href contains data-trigger-url, else text contains data-trigger-text) and
     swaps each for a button with the same content and classes. The form panel moves into a modal
     <dialog> on body (a dialog inside a closed <details> would not render), which every button
     opens; contact[Opened from] gets the FAQ question above the button used. No link found, or no
     showModal(): the form stays inline, as without JavaScript. If showModal() throws when it is
     called, the panel, the links and the inline form come back in the FAQ item and the page is
     not locked.
   - The dialog, as the professionals quote panel: showModal, scrim, close button, Escape and a
     click on the scrim close it, body.overflow-hidden locks the page. Focus goes to the form title
     (no keyboard popping up on phones), Tab wraps inside the dialog, and on close focus returns to
     the button.
   - Checks the fields before the post: name, a profession (and its text when "Other" is chosen;
     that field shows only then), practice name, email, at least one of evidence pack and samples,
     and the practice address when samples is ticked. Messages come from the settings.
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
  var RESTORED = ['profession_other', 'practice', 'pack', 'samples', 'address', 'name', 'phone', 'body'];
  var OTHER = 'Other';
  var KLAVIYO_EVENTS = 'https://a.klaviyo.com/client/events/';
  var KLAVIYO_REVISION = '2026-10-15';
  var KLAVIYO_METRIC = 'Practitioner Request Submitted';
  var KLAVIYO_TIMEOUT = 8000;

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

  /* Every trigger link in the FAQ: the answers and the section content of all items (the kPNI
     answer, the "For dentists" note), by URL first, else by text. They all open the one form. */
  function findTriggers(root) {
    var faq = root.closest('.kc-faq-block') || root.closest('.kc-faq-item');
    if (!faq) return [];
    var links = Array.prototype.slice.call(
      faq.querySelectorAll('.kc-faq-description a, .kc-faq-section-content a')
    );
    var url = root.getAttribute('data-trigger-url') || '';
    var text = (root.getAttribute('data-trigger-text') || '').toLowerCase();
    var found = [];
    if (url) {
      found = links.filter(function (a) {
        return (a.getAttribute('href') || '').indexOf(url) !== -1;
      });
    }
    if (!found.length && text) {
      found = links.filter(function (a) {
        return a.textContent.toLowerCase().indexOf(text) !== -1;
      });
    }
    return found;
  }

  /* The FAQ question above a trigger, for "Opened from" in the inbox and in Klaviyo */
  function itemTitle(el) {
    var item = el && el.closest('.kc-faq-item');
    var summary = item && item.querySelector('.kc-faq-summary');
    return summary ? summary.textContent.trim() : '';
  }

  function init(root) {
    var form = root.querySelector('form');
    if (!form) return;
    var state = root.querySelector('[data-kc-pr-state]');
    var stateName = state ? state.getAttribute('data-kc-pr-state') : '';
    var links = findTriggers(root);
    var dialog = null;
    var buttons = [];
    /* the button the visitor opened the form with; focus returns there */
    var button = null;
    var home = null;
    var openedFrom = form.querySelector('input[type=hidden][name="contact[Opened from]"]');
    var pending = stateName ? store('get') : null;

    if (links.length && typeof document.createElement('dialog').showModal === 'function') {
      /* marks the panel's place in the FAQ item, for the inline fallback */
      home = document.createComment('kc-practitioner-request');
      root.parentNode.insertBefore(home, root);
      dialog = buildDialog(root, stateName, afterClose);
      buttons = links.map(function (link) {
        var trigger = document.createElement('button');
        trigger.type = 'button';
        /* the link's own classes keep its look (the dentists note styles .rda-link) */
        trigger.className = (link.className ? link.className + ' ' : '') + 'kc-pr-trigger';
        trigger.innerHTML = link.innerHTML;
        trigger.setAttribute('aria-haspopup', 'dialog');
        trigger.setAttribute('aria-controls', dialog.id);
        link.replaceWith(trigger);
        trigger.addEventListener('click', function () {
          use(trigger);
          show(null);
        });
        return trigger;
      });
      /* after a post: the button the request was opened with, and its item open behind */
      var before = pending && buttons[pending.opener];
      use(before || buttons[0]);
      if (before) {
        var beforeItem = before.closest('.kc-faq-item');
        if (beforeItem) beforeItem.open = true;
      }
      dialog.addEventListener('close', afterClose);
    }

    function use(trigger) {
      button = trigger;
      if (openedFrom) openedFrom.value = itemTitle(trigger);
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
      buttons.forEach(function (trigger, i) {
        trigger.replaceWith(links[i]);
      });
      dialog.removeEventListener('close', afterClose);
      dialog.remove();
      dialog = null;
      buttons = [];
      button = null;
      if (openedFrom) openedFrom.value = '';
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
    var professionGroup = form.querySelector('[data-kc-pr-group="profession"]');
    var professions = Array.prototype.slice.call(form.querySelectorAll('[data-kc-pr-profession]'));
    var otherBox = form.querySelector('[data-kc-pr-other]');

    function profession() {
      var checked = professions.filter(function (el) {
        return el.checked;
      })[0];
      return checked || null;
    }

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
        professions.forEach(function (el) {
          el.checked = el.value === saved.profession;
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

    /* The text field for another profession shows only with "Other" (without JavaScript it stays) */
    function syncOther() {
      var chosen = profession();
      var needed = !!chosen && chosen.value === OTHER;
      if (otherBox) otherBox.hidden = !needed;
      if (!fields.profession_other) return;
      fields.profession_other.required = needed;
      fields.profession_other.setAttribute('aria-required', needed ? 'true' : 'false');
      if (!needed) showError(fields.profession_other, '');
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
      if (key === 'profession_other' && !(profession() && profession().value === OTHER)) return '';
      return value ? '' : el.getAttribute('data-error-required');
    }

    function checkGroup() {
      var ok = (fields.pack && fields.pack.checked) || (fields.samples && fields.samples.checked);
      return ok ? '' : group.getAttribute('data-error-required');
    }

    function checkProfession() {
      if (!professionGroup || profession()) return '';
      return professionGroup.getAttribute('data-error-required');
    }

    function validate() {
      var firstBad = null;
      function note(key) {
        var message = check(key);
        showError(fields[key], message);
        if (message && !firstBad) firstBad = fields[key];
      }
      note('name');
      var professionMessage = checkProfession();
      if (professionGroup) showError(professionGroup, professionMessage);
      if (professionMessage && !firstBad) firstBad = professions[0];
      ['profession_other', 'practice', 'email'].forEach(note);
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
    professions.forEach(function (el) {
      el.addEventListener('change', function () {
        syncOther();
        if (professionGroup.getAttribute('aria-invalid') === 'true') showError(professionGroup, checkProfession());
      });
    });
    syncOther();

    /* once a message shows, it updates as the visitor fixes the field */
    ['name', 'profession_other', 'practice', 'email', 'address'].forEach(function (key) {
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
      var chosen = profession();
      snapshot.profession = chosen ? chosen.value : '';
      /* for the Klaviyo event on the thank-you reload: the profession as the visitor read it */
      snapshot.profession_label = chosen ? chosen.parentNode.textContent.trim() : '';
      snapshot.email = fields.email ? fields.email.value.trim() : '';
      snapshot.opener = buttons.indexOf(button);
      snapshot.opened_from = openedFrom ? openedFrom.value : '';
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
            profession_other: saved.profession === OTHER ? (saved.profession_other || '').trim() : '',
            profession_label:
              saved.profession === OTHER ? (saved.profession_other || '').trim() : saved.profession_label || '',
            practice_name: (saved.practice || '').trim(),
            email: saved.email,
            phone: saved.phone || '',
            evidence_pack: !!saved.pack,
            samples: !!saved.samples,
            practice_address: saved.samples ? saved.address || '' : '',
            message: saved.body || '',
            language: saved.language || '',
            page: saved.page || '',
            opened_from: saved.opened_from || '',
          },
          time: saved.at,
          unique_id: saved.id || uid(),
        },
      },
    };
    /* as the withdrawal page: the call is aborted after 8 s, and the timer goes when it settles */
    var controller = typeof AbortController === 'function' ? new AbortController() : null;
    var timer = controller
      ? window.setTimeout(function () {
          controller.abort();
        }, KLAVIYO_TIMEOUT)
      : null;
    var done = function () {
      if (timer) window.clearTimeout(timer);
    };
    window
      .fetch(KLAVIYO_EVENTS + '?company_id=' + encodeURIComponent(company), {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', revision: KLAVIYO_REVISION },
        body: JSON.stringify(payload),
        signal: controller ? controller.signal : undefined,
        keepalive: true,
      })
      .then(done, function () {
        /* offline, blocked, refused or aborted: no retry, and nothing of the request stays in the
           tab (the snapshot was consumed before the call; cleared again in case) */
        done();
        store('clear');
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
