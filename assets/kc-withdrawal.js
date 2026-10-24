/* kc-withdrawal.js: the two-step withdrawal statement (sections/kc-withdrawal.liquid).
   Step 1 validates the fields and shows them back; step 2 carries the one "Confirm withdrawal"
   button (the confirmation function of Art. VI.61/2 §3 WER). On confirm: the submission time is
   stamped into the form, one event goes to Klaviyo's client endpoint when the section carries a
   public API key (its transactional flow emails the acknowledgement of receipt with the content,
   date and time), then the form posts natively to Shopify's contact endpoint for the store inbox
   copy. Whether the event was accepted is kept in sessionStorage for the success view that Shopify
   renders after its redirect. No cookies, no analytics, no other request. */
(() => {
  'use strict';

  const KEY = 'kc-withdrawal-ack';
  const KLAVIYO_EVENTS = 'https://a.klaviyo.com/client/events/';
  const KLAVIYO_REVISION = '2026-10-15';
  const EMAIL = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

  const form = document.querySelector('[data-kc-withdrawal]');
  if (!form) return;
  form.classList.add('kc-wd-js');

  const read = () => {
    try {
      const raw = sessionStorage.getItem(KEY);
      if (!raw) return null;
      sessionStorage.removeItem(KEY);
      return JSON.parse(raw);
    } catch (error) {
      return null;
    }
  };

  const remember = (status, email) => {
    try {
      sessionStorage.setItem(KEY, JSON.stringify({ status, email, at: new Date().toISOString() }));
    } catch (error) {
      /* private mode: the default success line shows */
    }
  };

  // After Shopify's redirect: which acknowledgement line to show
  const success = form.querySelector('[data-kc-wd-success]');
  if (success) {
    const record = read();
    const sent = success.querySelector('[data-kc-wd-ack-sent]');
    const fallback = success.querySelector('[data-kc-wd-ack-default]');
    if (record && record.status === 'sent' && sent && record.email) {
      sent.textContent = (sent.dataset.template || '').replace('[email]', record.email);
      sent.hidden = false;
      if (fallback) fallback.hidden = true;
    }
    return;
  }

  form.setAttribute('novalidate', '');

  const fields = Array.from(form.querySelectorAll('[data-kc-wd-field]'));
  const byName = (name) => fields.find((field) => field.dataset.kcWdField === name);
  const steps = {
    1: form.querySelector('[data-kc-wd-step="1"]'),
    2: form.querySelector('[data-kc-wd-step="2"]'),
  };
  const markers = Array.from(form.querySelectorAll('[data-kc-wd-step-marker]'));
  const review = form.querySelector('[data-kc-wd-next]');
  const edit = form.querySelector('[data-kc-wd-edit]');
  const confirm = form.querySelector('[data-kc-wd-confirm]');
  const submittedAt = form.querySelector('[data-kc-wd-submitted-at]');
  const body = form.querySelector('[data-kc-wd-body]');
  const live = form.querySelector('[data-kc-wd-live]');
  if (!steps[1] || !steps[2] || !confirm) return;

  const value = (field) => (field ? field.value.trim() : '');

  const validateField = (field) => {
    const text = value(field);
    let message = '';
    if (field.required && !text) message = field.dataset.errorRequired || '';
    else if (text && field.type === 'email' && !EMAIL.test(text)) message = field.dataset.errorFormat || '';
    const error = document.getElementById(field.id + '-error');
    if (error) {
      error.textContent = message;
      error.hidden = !message;
    }
    field.setAttribute('aria-invalid', message ? 'true' : 'false');
    return !message;
  };

  const validateAll = () => {
    let first = null;
    fields.forEach((field) => {
      if (!validateField(field) && !first) first = field;
    });
    if (first) {
      showStep(1, first);
      if (live) live.textContent = first.dataset.errorRequired || first.dataset.errorFormat || '';
    }
    return !first;
  };

  const showStep = (n, focusTarget) => {
    Object.keys(steps).forEach((key) => {
      steps[key].hidden = key !== String(n);
    });
    markers.forEach((marker) => {
      if (marker.dataset.kcWdStepMarker === String(n)) marker.setAttribute('aria-current', 'step');
      else marker.removeAttribute('aria-current');
    });
    const target = focusTarget || steps[n].querySelector('[data-kc-wd-step-title]');
    if (target) target.focus();
  };

  const fillReview = () => {
    fields.forEach((field) => {
      const out = form.querySelector('[data-kc-wd-review="' + field.dataset.kcWdField + '"]');
      if (!out) return;
      const text = value(field);
      out.textContent = text;
      const row = out.closest('[data-kc-wd-review-row]');
      if (row) row.hidden = !text;
    });
  };

  fields.forEach((field) => {
    field.addEventListener('blur', () => {
      if (field.getAttribute('aria-invalid') === 'true') validateField(field);
    });
    field.addEventListener('input', () => {
      if (field.getAttribute('aria-invalid') === 'true') validateField(field);
    });
  });

  if (review) {
    review.addEventListener('click', () => {
      if (!validateAll()) return;
      fillReview();
      showStep(2);
    });
  }

  if (edit) {
    edit.addEventListener('click', () => showStep(1, fields[0]));
  }

  // The submission time, in the shop's time zone and in UTC, for both copies
  const stamp = (now) => {
    const timeZone = form.dataset.kcTimezone || 'Europe/Brussels';
    let local = '';
    try {
      local = new Intl.DateTimeFormat(form.dataset.kcLocale || 'en', {
        dateStyle: 'long',
        timeStyle: 'short',
        timeZone,
      }).format(now);
    } catch (error) {
      local = now.toUTCString();
    }
    return { local, timeZone, utc: now.toISOString() };
  };

  const uid = () => {
    if (window.crypto && typeof window.crypto.randomUUID === 'function') return window.crypto.randomUUID();
    return String(Date.now()) + '-' + Math.random().toString(16).slice(2);
  };

  // One event to Klaviyo's public endpoint; its transactional flow sends the acknowledgement
  const sendAcknowledgement = (now, when, content) => {
    const company = (form.dataset.kcKlaviyoCompany || '').trim();
    if (!company || typeof window.fetch !== 'function') return Promise.resolve(false);
    const metric = (form.dataset.kcKlaviyoMetric || '').trim() || 'Withdrawal statement submitted';
    const nameParts = content.name.split(/\s+/);
    const payload = {
      data: {
        type: 'event',
        attributes: {
          metric: { data: { type: 'metric', attributes: { name: metric } } },
          profile: {
            data: {
              type: 'profile',
              attributes: {
                email: content.email,
                first_name: nameParts[0] || '',
                last_name: nameParts.slice(1).join(' '),
              },
            },
          },
          properties: {
            statement: content.statement,
            name: content.name,
            order_number: content.order,
            email: content.email,
            items: content.items,
            submitted_at_local: when.local,
            submitted_at_utc: when.utc,
            timezone: when.timeZone,
            language: form.dataset.kcLocale || '',
            page: window.location.origin + window.location.pathname,
          },
          time: when.utc,
          unique_id: uid(),
        },
      },
    };
    const controller = typeof AbortController === 'function' ? new AbortController() : null;
    const timer = controller ? setTimeout(() => controller.abort(), 8000) : null;
    return fetch(KLAVIYO_EVENTS + '?company_id=' + encodeURIComponent(company), {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', revision: KLAVIYO_REVISION },
      body: JSON.stringify(payload),
      signal: controller ? controller.signal : undefined,
      keepalive: true,
    })
      .then((response) => response.ok)
      .catch(() => false)
      .finally(() => {
        if (timer) clearTimeout(timer);
      });
  };

  let sending = false;

  form.addEventListener('submit', (event) => {
    if (sending) return;
    event.preventDefault();
    if (!validateAll()) return;
    if (steps[2].hidden) {
      // Enter in a step 1 field: show the statement back first
      fillReview();
      showStep(2);
      return;
    }

    sending = true;
    confirm.disabled = true;
    confirm.setAttribute('aria-disabled', 'true');
    confirm.classList.add('loading');
    if (edit) edit.disabled = true;

    const now = new Date();
    const when = stamp(now);
    const content = {
      statement: form.dataset.kcStatement || '',
      name: value(byName('name')),
      order: value(byName('order')),
      email: value(byName('email')),
      items: value(byName('items')),
    };
    if (submittedAt) submittedAt.value = when.local + ' (' + when.timeZone + ') · ' + when.utc;
    if (body) {
      body.value = [
        content.statement,
        'Name: ' + content.name,
        'Order number: ' + content.order,
        'Email: ' + content.email,
        content.items ? 'Items: ' + content.items : '',
        'Submitted at: ' + when.local + ' (' + when.timeZone + ') · ' + when.utc,
      ]
        .filter(Boolean)
        .join('\n');
    }

    sendAcknowledgement(now, when, content)
      .then((ok) => remember(ok ? 'sent' : 'failed', content.email))
      .catch(() => remember('failed', content.email))
      .then(() => {
        // Native submit: Shopify records the statement in the store inbox and redirects back here
        HTMLFormElement.prototype.submit.call(form);
      });
  });
})();
