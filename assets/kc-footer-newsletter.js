/* Footer newsletter: progressive enhancement of Shopify's native customer form.
 * With a Klaviyo public key, list ID and retry message on the wrapper, submit posts the
 * address to Klaviyo's client subscriptions endpoint (public key only, no cookie, no script).
 * Without them, or with JS off, the native Shopify form submits. Once a request has gone out
 * the native form is never submitted as well: an unclear outcome keeps the address and asks
 * for a retry, so one signup never reaches both backends (R46-B4, Victor option a).
 * The only network call lives inside the submit handler. */
(() => {
  const wrap = document.getElementById('FooterNewsletter');
  const form = document.getElementById('FooterNewsletterForm');
  if (!wrap || !form) return;
  const config = wrap.dataset;
  const key = (config.klaviyoKey || '').trim();
  const list = (config.klaviyoList || '').trim();
  if (!key || !list || !config.msgRetry) return;

  const input = form.querySelector('input[type="email"]');
  const button = form.querySelector('button[type="submit"]');
  const status = document.getElementById('FooterNewsletterEmail-status');
  const alert = document.getElementById('FooterNewsletterEmail-error');
  const noteId = 'FooterNewsletterEmail-note';
  if (!input || !button || !status || !alert) return;

  const endpoint = `https://a.klaviyo.com/client/subscriptions?company_id=${encodeURIComponent(key)}`;
  const revision = '2026-10-15';
  const timeoutMs = 8000;
  let pending = false;

  const describe = (...ids) => input.setAttribute('aria-describedby', ids.filter(Boolean).join(' '));

  const reset = () => {
    status.textContent = '';
    alert.textContent = '';
    input.removeAttribute('aria-invalid');
    describe(noteId);
  };

  const setBusy = (value) => {
    pending = value;
    form.setAttribute('aria-busy', String(value));
    button.disabled = value;
    // Read-only while pending, so the address on screen is the one that was sent.
    input.readOnly = value;
  };

  const showStatus = (text) => {
    status.textContent = text;
    describe(status.id, noteId);
  };

  // Focus first, fill the alert a frame later: the error is spoken once, by the alert, and not
  // a second time as the description read out on focus (R46-B2).
  const showError = (text) => {
    input.setAttribute('aria-invalid', 'true');
    if (document.activeElement !== input) input.focus();
    requestAnimationFrame(() => {
      alert.textContent = text;
      describe(alert.id, noteId);
    });
  };

  // Unclear outcome (429, 5xx, network, timeout, any other answer): Klaviyo may have taken the
  // signup, so nothing else is sent. The address stays in the field for a retry.
  const showRetry = () => {
    setBusy(false);
    alert.textContent = config.msgRetry;
    describe(alert.id, noteId);
  };

  const payload = () => ({
    data: {
      type: 'subscription',
      attributes: {
        custom_source: config.source || 'Footer newsletter',
        profile: {
          data: {
            type: 'profile',
            attributes: {
              email: input.value.trim(),
              locale: config.locale || 'en',
              properties: {
                signup_path: window.location.pathname,
                consent_text_version: config.consentVersion || '',
              },
              subscriptions: {
                email: { marketing: { consent: 'SUBSCRIBED' } },
              },
            },
          },
        },
      },
      relationships: {
        list: { data: { type: 'list', id: list } },
      },
    },
  });

  form.addEventListener('submit', (event) => {
    if (pending) {
      event.preventDefault();
      return;
    }
    if (!input.checkValidity()) return;
    event.preventDefault();
    reset();
    setBusy(true);

    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), timeoutMs);

    fetch(endpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/vnd.api+json', revision },
      body: JSON.stringify(payload()),
      credentials: 'omit',
      signal: controller.signal,
    })
      .then((response) => {
        clearTimeout(timer);
        if (response.status === 202) {
          input.value = '';
          setBusy(false);
          showStatus(config.msgSuccess || '');
          return;
        }
        // 400 is Klaviyo's answer to an address it rejects; key, list or permission errors
        // (401/403/404) are not the visitor's fault and get the retry message instead.
        if (response.status === 400) {
          setBusy(false);
          showError(config.msgInvalid || '');
          return;
        }
        showRetry();
      })
      .catch(() => {
        clearTimeout(timer);
        showRetry();
      });
  });
})();
