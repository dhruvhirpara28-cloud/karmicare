/* Footer newsletter: progressive enhancement of Shopify's native customer form.
 * With a Klaviyo public key and list ID on the form, submit posts the address to
 * Klaviyo's client subscriptions endpoint (public key only, no cookie, no script).
 * Without them, or when Klaviyo cannot be reached, the native Shopify form submits.
 * The only network call lives inside the submit handler. */
(() => {
  const wrap = document.getElementById('FooterNewsletter');
  const form = document.getElementById('FooterNewsletterForm');
  if (!wrap || !form) return;
  const config = wrap.dataset;
  const key = (config.klaviyoKey || '').trim();
  const list = (config.klaviyoList || '').trim();
  if (!key || !list) return;

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
  };

  const showStatus = (text) => {
    status.textContent = text;
    describe(status.id, noteId);
  };

  const showError = (text) => {
    alert.textContent = text;
    input.setAttribute('aria-invalid', 'true');
    describe(alert.id, noteId);
    input.focus();
  };

  // Klaviyo unreachable (429, 5xx, network, timeout): let Shopify take the signup.
  const fallback = () => {
    form.submit();
  };

  const payload = () => ({
    data: {
      type: 'subscription',
      attributes: {
        custom_source: form.dataset.source || 'Footer newsletter',
        profile: {
          data: {
            type: 'profile',
            attributes: {
              email: input.value.trim(),
              locale: form.dataset.locale || 'en',
              properties: {
                signup_path: window.location.pathname,
                consent_text_version: form.dataset.consentVersion || '',
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
          showStatus(form.dataset.msgSuccess || '');
          return;
        }
        if (response.status >= 400 && response.status < 500 && response.status !== 429) {
          setBusy(false);
          showError(form.dataset.msgInvalid || '');
          return;
        }
        fallback();
      })
      .catch(() => {
        clearTimeout(timer);
        fallback();
      });
  });
})();
