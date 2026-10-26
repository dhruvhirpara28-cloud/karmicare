#!/bin/zsh
# R76j: the Trusted Professionals button opens the same popup as the two FAQ links (Victor, 26 Oct).
# popup.sh <browserPageId> [width, default 390]. Klaviyo calls are stubbed by fx.js; nothing posts to the store.
P=${1:?browserPageId}
B=http://127.0.0.1:9376
W=${2:-390}
go() { orca goto --page $P --url "$B/$1" --json >/dev/null 2>&1; orca wait --page $P --load networkidle --json >/dev/null 2>&1; orca exec --page $P --command "set viewport $W 900" --json >/dev/null 2>&1; orca screenshot --page $P --json >/dev/null 2>&1; }
ev() { orca eval --page $P --expression "$1" --json 2>/dev/null | python3 -I -c 'import json,sys; d=json.load(sys.stdin); print(d.get("result",{}).get("result") or d.get("error"))'; }
H="const cta = () => document.querySelector('a[data-kc-pr-open]'); const dent = () => document.querySelector('.kc-faq-section-content .kc-pr-trigger'); const kpni = () => document.querySelector('.kc-faq-description .kc-pr-trigger'); const dlg = () => document.querySelector('dialog.kc-pr-dialog'); const from = () => (document.querySelector('[name=\"contact[Opened from]\"]') || {}).value; const settle = () => document.querySelectorAll('dialog').forEach(d => d.getAnimations().forEach(a => { try { a.finish(); } catch (e) {} }));"
N=$(date +%s)

echo "== 1 PDP: the button is a third opener of the one popup"
go "pdp-current.html?n=$N"
ev "(() => { $H const c = cta(); return 'FAQ buttons ' + document.querySelectorAll('.kc-pr-trigger').length + ' | button href ' + (c && c.getAttribute('href')) + ' | aria ' + (c && c.getAttribute('aria-haspopup') + '/' + c.getAttribute('aria-controls')) + ' | coming soon left ' + !!document.querySelector('.trusted-professionals .kc-coming-soon') + ' | errors ' + window.__fxErrors.length; })()"

echo "== 2 click the button: popup, focus, Opened from; close returns focus"
ev "(() => { $H cta().click(); settle(); const d = dlg(); const r = 'open ' + d.open + ' | url hash ' + JSON.stringify(location.hash) + ' | focus ' + document.activeElement.className + ' | opened from: ' + from(); d.querySelector('[data-kc-pr-close]').click(); return r + ' | after close: focus on ' + (document.activeElement === cta() ? 'the button' : document.activeElement === kpni() ? 'the kPNI link (button hidden)' : document.activeElement.tagName) + ', locked ' + document.body.classList.contains('overflow-hidden'); })()"

echo "== 3 the FAQ links still work"
ev "(() => { $H dent().closest('.kc-faq-item').open = true; dent().click(); settle(); const a = 'dentists: open ' + dlg().open + ' from ' + from(); dlg().querySelector('[data-kc-pr-close]').click(); kpni().closest('.kc-faq-item').open = true; kpni().click(); settle(); const b = ' | kPNI: open ' + dlg().open + ' from ' + from(); dlg().querySelector('[data-kc-pr-close]').click(); return a + b + ' | focus back on kPNI ' + (document.activeElement === kpni()); })()"

echo "== 4 submit from the button, then the thank-you reload"
ev "(() => { $H sessionStorage.clear(); cta().click(); const f = document.querySelector('[data-kc-pr] form'); f.querySelector('#KcPr-name').value = 'Dr. An Peeters'; f.querySelector('[data-kc-pr-profession]').click(); f.querySelector('#KcPr-practice').value = 'Praktijk Peeters'; f.querySelector('#KcPr-email').value = 'an@example.com'; f.querySelector('#KcPr-pack').checked = true; f.requestSubmit(); const posted = (window.__fxPosted || []).filter(p => p[0] === 'contact[Opened from]').map(p => p[1]); const s = JSON.parse(sessionStorage.getItem('kc-practitioner-request') || 'null'); return 'posted Opened from: ' + posted.join(',') + ' | snapshot opener ' + (s && s.opener) + ' from ' + (s && s.opened_from); })()"
go "pdp-current-success.html?n=$N"
ev "new Promise(r => setTimeout(r, 400)).then(() => { $H settle(); const k = window.__fxKlaviyo[0]; const props = k && JSON.parse(k.body).data.attributes.properties; const d = dlg(); const r = 'thank-you dialog open ' + d.open + ' | klaviyo opened_from: ' + (props && props.opened_from); d.querySelector('[data-kc-pr-close]').click(); return r + ' | close: focus on the button ' + (document.activeElement === cta()) + ' | errors ' + window.__fxErrors.length; })"

echo "== 5 homepage: the button links to the product at the form"
go "home-current.html?n=$N"
ev "(() => { const c = document.querySelector('a[data-kc-pr-open]'); return 'href ' + (c && c.getAttribute('href')) + ' | coming soon left ' + !!document.querySelector('.trusted-professionals .kc-coming-soon') + ' | form on homepage ' + !!document.querySelector('[data-kc-pr]'); })()"

echo "== 6 arriving from the homepage: the popup opens on load"
sessionStorage_clear="sessionStorage.clear()"
go "pdp-current.html?from=home-trusted&n=$N#KcPractitionerRequest-panel"
ev "new Promise(r => setTimeout(r, 500)).then(() => { $H settle(); const d = dlg(); const r = 'open on arrival ' + d.open + ' | focus ' + document.activeElement.className + ' | opened from: ' + from() + ' | hash after ' + JSON.stringify(location.hash) + ' | locked ' + document.body.classList.contains('overflow-hidden'); d.querySelector('[data-kc-pr-close]').click(); return r + ' | close: focus on the button ' + (document.activeElement === cta()) + ', unlocked ' + !document.body.classList.contains('overflow-hidden') + ' | errors ' + window.__fxErrors.length; })"

echo "== 7 arriving with an unknown ?from: the button's own label, not the free text"
go "pdp-current.html?from=evil%3Cb%3E&n=$N#KcPractitionerRequest-panel"
ev "new Promise(r => setTimeout(r, 500)).then(() => { $H return 'open ' + dlg().open + ' | opened from: ' + from(); })"

echo "== 8 showModal throws: arriving and clicking fall back to the inline form"
go "pdp-current.html?modal=throw&n=$N#KcPractitionerRequest-panel"
ev "new Promise(r => setTimeout(r, 500)).then(() => { $H const panel = document.querySelector('[data-kc-pr]'); const inline = !!panel.closest('.kc-faq-item'); const c = cta(); return 'dialog ' + !!dlg() + ' | form inline in the FAQ ' + inline + ' | item open ' + (panel.closest('.kc-faq-item') || {}).open + ' | button still a link ' + (c && c.tagName) + ' ' + (c && c.getAttribute('href')) + ' | locked ' + document.body.classList.contains('overflow-hidden') + ' | errors ' + window.__fxErrors.length; })"
