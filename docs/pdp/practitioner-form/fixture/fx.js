/* Professionals page v1 preview helper (render.mjs puts it at the end of every page).
   - ?mode=day|night forces the theme mode.
   - Every submit the form's own script lets through is stopped and recorded in window.__fxPosted:
     nothing reaches the store. Calls to klaviyo.com are stubbed (202) and recorded.
   - PROTOTYPE of the phase 2 "Opened from" (decision D5): ?from=<slug> fills the hidden
     contact[Opened from], when the slug is one of the known entry points.
   - fxRun() returns the checks for this variant. */
(function () {
  var params = new URLSearchParams(location.search);
  var mode = params.get('mode') || 'day';
  function applyMode() {
    if (!document.body.classList.contains(mode + '-mode')) {
      document.body.classList.remove('day-mode', 'night-mode');
      document.body.classList.add(mode + '-mode');
    }
  }
  applyMode();
  new MutationObserver(applyMode).observe(document.body, { attributes: true, attributeFilter: ['class'] });

  window.__fxPosted = null;
  document.addEventListener('submit', function (e) {
    if (e.defaultPrevented) return;
    e.preventDefault();
    window.__fxPosted = Array.from(new FormData(e.target).entries());
  });
  window.__fxKlaviyo = [];
  var realFetch = window.fetch;
  window.fetch = function (url, init) {
    if (String(url).indexOf('klaviyo.com') !== -1) {
      window.__fxKlaviyo.push({ url: String(url), body: init && init.body });
      return Promise.resolve(new Response('', { status: 202 }));
    }
    return realFetch.apply(this, arguments);
  };
  // ?modal=throw|missing replaces showModal before the theme script (deferred) runs
  if (params.get('modal') === 'throw') HTMLDialogElement.prototype.showModal = function () { throw new DOMException('fixture: showModal throws', 'InvalidStateError'); };
  if (params.get('modal') === 'missing') HTMLDialogElement.prototype.showModal = undefined;
  // page errors of the theme and inline code; cross-origin scripts only report "Script error."
  window.__fxErrors = [];
  window.addEventListener('error', function (e) {
    if (e.message === 'Script error.' && !e.filename) return;
    // a browser notice, not an error: the page's own ResizeObservers (kc-marquee, kc-navigation,
    // kc-gallery, global.js) see the layout move when the inline form unfolds in the FAQ
    if (/^ResizeObserver loop/.test(e.message)) return;
    window.__fxErrors.push(e.message + ' @ ' + (e.filename || 'inline').split('/').pop() + ':' + e.lineno);
  });

  var FROM = ['pdp-faq-kpni', 'pdp-faq-dentists', 'pdp-trusted', 'home-trusted', 'header'];
  var from = params.get('from');
  if (from && FROM.indexOf(from) !== -1) {
    var hidden = document.querySelector('input[type=hidden][name="contact[Opened from]"]');
    if (hidden) hidden.value = from;
  }

  var V = window.FX_VARIANT || '';
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var visible = function (el) { return !!el && el.getClientRects().length > 0 && getComputedStyle(el).visibility !== 'hidden'; };

  window.fxRun = function () {
    var checks = [];
    var ok = function (name, pass, detail) { checks.push({ name: name, pass: !!pass, detail: detail === undefined ? '' : String(detail) }); };
    var vw = document.documentElement.clientWidth;
    ok('no horizontal page overflow', document.documentElement.scrollWidth <= vw + 1, document.documentElement.scrollWidth + ' / ' + vw);
    if (/^page/.test(V)) {
      var form = $('.kc-pr__form');
      ok('one H1, the page title', document.querySelectorAll('h1').length === 1 && /Profession/.test($('h1').textContent), $('h1') && $('h1').textContent.trim());
      ok('no dialog on the page', !$('dialog.kc-pr-dialog'));
      ok('no trigger buttons', !$('.kc-pr-trigger'));
      if (/success/.test(V)) {
        ok('thank-you visible', visible($('.kc-pr__success')));
      } else {
        ok('form inline and visible', visible(form));
        ok('7 profession radios', document.querySelectorAll('[data-kc-pr-profession]').length === 7);
        ok('every option has its label text', Array.from(document.querySelectorAll('.kc-pr__check span')).every(function (s) { return s.textContent.trim().length > 0; }));
        var col = $('.kc-professionals__inner');
        var r = col.getBoundingClientRect();
        ok('column at most 720px, 20px gutter', r.width <= 720.5 && Math.round(parseFloat(getComputedStyle(col).paddingLeft)) === 20, Math.round(r.width) + 'px');
        if (/error/.test(V)) ok('error alert visible', visible($('.kc-pr__alert')));
        if (!/nojs/.test(V)) {
          ok('JS: novalidate set', form.noValidate);
          ok('Opened from follows ?from (prototype)', !from || ($('input[name="contact[Opened from]"]') || {}).value === from, from);
        } else {
          ok('no-JS: native required on name', $('#KcPr-name').required);
        }
      }
    }
    if (V === 'pdp-after') {
      ok('PDP: no form panel', !$('#KcPractitionerRequest-panel') && !$('[data-kc-pr]'));
      ok('PDP: no form assets', !document.querySelector('script[src*="kc-practitioner-request"], link[href*="kc-practitioner-request"]'));
      var dent = $('.kc-faq-section-content a.rda-link');
      ok('PDP: dentists link goes to the page', dent && /page-en\.html\?from=pdp-faq-dentists/.test(dent.getAttribute('href')), dent && dent.getAttribute('href'));
      var kpni = Array.from(document.querySelectorAll('.kc-faq-description a')).filter(function (a) { return /evidence pack/i.test(a.textContent); })[0];
      ok('PDP: kPNI link goes to the page', kpni && /from=pdp-faq-kpni/.test(kpni.getAttribute('href')), kpni && kpni.getAttribute('href'));
      var cta = Array.from(document.querySelectorAll('a.karmicare__btn-secondary')).filter(function (a) { return /PRACTITIONER SAMPLE/.test(a.textContent); })[0];
      ok('PDP: Trusted CTA is a link to the page', cta && /from=pdp-trusted/.test(cta.getAttribute('href')) && !cta.classList.contains('kc-coming-soon'), cta && cta.getAttribute('href'));
    }
    var pass = checks.every(function (c) { return c.pass; });
    return { variant: V, mode: mode, width: vw, pass: pass, failed: checks.filter(function (c) { return !c.pass; }), checks: checks };
  };

  // fxShow('faq'): open the kPNI and dentists FAQ items and scroll the FAQ into view (PDP shots)
  window.fxShow = function (part) {
    if (part === 'faq') {
      var items = Array.from(document.querySelectorAll('.kc-faq-item'));
      var dent = items.filter(function (d) { return /dentists/i.test(d.textContent.slice(0, 200)); })[0];
      if (dent) dent.open = true;
      var target = dent || items[0];
      if (target) window.scrollTo(0, target.getBoundingClientRect().top + scrollY - 20);
      return dent ? 'dentists open' : 'no faq';
    }
    if (part === 'form') {
      var f = $('.kc-pr') || document.body;
      window.scrollTo(0, f.getBoundingClientRect().top + scrollY - 20);
      return 'form';
    }
    return 'top';
  };
})();
