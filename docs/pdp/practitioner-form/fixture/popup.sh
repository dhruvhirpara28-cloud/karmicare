#!/bin/zsh
# R76k: one practitioner form for the site (sections/practitioner-group.json, rendered by the
# layout on the homepage and product pages). The PDP FAQ links and the Trusted Professionals
# button open it in the popup, on the homepage as well. popup.sh <browserPageId> [width, 390]
# Klaviyo calls are stubbed by fx.js; nothing posts to the store.
P=${1:?browserPageId}
W=${2:-390}
B=http://127.0.0.1:9376
N=$(date +%s)
go() { orca goto --page $P --url "$B/$1" --json >/dev/null 2>&1; orca wait --page $P --load networkidle --json >/dev/null 2>&1; orca exec --page $P --command "set viewport $W 900" --json >/dev/null 2>&1; orca screenshot --page $P --json >/dev/null 2>&1; }
ev() { orca eval --page $P --expression "$1" --json 2>/dev/null | python3 -I -c 'import json,sys; d=json.load(sys.stdin); print(d.get("result",{}).get("result") or d.get("error"))'; }
H="const cta = () => document.querySelector('.trusted-professionals a[data-kc-pr-open]'); const dent = () => document.querySelector('.kc-faq-section-content a[data-kc-pr-open]'); const kpni = () => document.querySelector('.kc-faq-description a[data-kc-pr-open]'); const dlg = () => document.querySelector('dialog.kc-pr-dialog'); const host = () => document.querySelector('[data-kc-pr-host]'); const from = () => (document.querySelector('[name=\"contact[Opened from]\"]') || {}).value; const settle = () => document.querySelectorAll('dialog').forEach(d => d.getAnimations().forEach(a => { try { a.finish(); } catch (e) {} })); const focusName = () => { const a = document.activeElement; return a === cta() ? 'the button' : a === dent() ? 'the dentists link' : a === kpni() ? 'the kPNI link' : a.tagName + (a.className ? '.' + String(a.className).split(' ')[0] : ''); }; const fill = () => { const f = document.querySelector('[data-kc-pr] form'); f.querySelector('#KcPr-name').value = 'Dr. An Peeters'; f.querySelector('[data-kc-pr-profession]').click(); f.querySelector('#KcPr-practice').value = 'Praktijk Peeters'; f.querySelector('#KcPr-email').value = 'an@example.com'; f.querySelector('#KcPr-pack').checked = true; return f; };"

echo "== 1 PDP: three links open the one popup; the form is not on the page"
go "pdp-current.html?n=$N"
ev "(() => { $H const o = Array.from(document.querySelectorAll('a[data-kc-pr-open]')); return 'openers ' + o.length + ' | all to #KcPractitionerRequest-panel ' + o.every(a => a.getAttribute('href') === '#KcPractitionerRequest-panel') + ' | aria ' + o.every(a => a.getAttribute('aria-haspopup') === 'dialog' && a.getAttribute('aria-controls') === 'KcPractitionerRequest-dialog') + ' | panel in dialog ' + !!(dlg() && dlg().querySelector('[data-kc-pr]')) + ' | host shown ' + (getComputedStyle(host()).display !== 'none') + ' | form inside the FAQ ' + !!document.querySelector('.kc-faq-item [data-kc-pr]') + ' | errors ' + window.__fxErrors.length; })()"

echo "== 2 PDP: the button, then the two FAQ links"
ev "(() => { $H const out = []; const c = cta(); if (c && c.checkVisibility()) { c.click(); settle(); out.push('button: open ' + dlg().open + ', focus ' + document.activeElement.className + ', from ' + from()); dlg().querySelector('[data-kc-pr-close]').click(); out.push('close -> ' + focusName()); } else { out.push('button hidden at this width (mobile-only on the PDP)'); } dent().closest('.kc-faq-item').open = true; dent().click(); settle(); out.push('dentists: open ' + dlg().open + ', from ' + from()); dlg().querySelector('[data-kc-pr-close]').click(); out.push('close -> ' + focusName()); kpni().closest('.kc-faq-item').open = true; kpni().click(); settle(); out.push('kPNI: open ' + dlg().open + ', from ' + from()); dlg().querySelector('[data-kc-pr-close]').click(); out.push('close -> ' + focusName() + ', unlocked ' + !document.body.classList.contains('overflow-hidden') + ', url ' + location.hash); return out.join(' | '); })()"

echo "== 3 PDP: post from the dentists link, then the thank-you reload"
ev "(() => { $H sessionStorage.clear(); dent().closest('.kc-faq-item').open = true; dent().click(); const f = fill(); f.requestSubmit(); const posted = (window.__fxPosted || []).filter(p => p[0] === 'contact[Opened from]').map(p => p[1]); const s = JSON.parse(sessionStorage.getItem('kc-practitioner-request') || 'null'); return 'posted Opened from: ' + posted.join(',') + ' | snapshot opener ' + (s && s.opener); })()"
go "pdp-current-success.html?n=$N"
ev "new Promise(r => setTimeout(r, 400)).then(() => { $H settle(); const k = window.__fxKlaviyo[0]; const props = k && JSON.parse(k.body).data.attributes.properties; const d = dlg(); const r = 'thank-you dialog ' + d.open + ' | dentists item open ' + dent().closest('.kc-faq-item').open + ' | klaviyo opened_from: ' + (props && props.opened_from); d.querySelector('[data-kc-pr-close]').click(); return r + ' | close -> ' + focusName() + ' | errors ' + window.__fxErrors.length; })"

echo "== 4 homepage: the button opens the popup right there"
go "home-current.html?n=$N"
ev "(() => { $H const c = cta(); const r0 = 'form hidden before ' + (getComputedStyle(host()).display === 'none' || !host().querySelector('[data-kc-pr]')) + ' | href ' + c.getAttribute('href'); const path = location.pathname; c.click(); settle(); const r = r0 + ' | open ' + dlg().open + ' | same page ' + (location.pathname === path) + ' | focus ' + document.activeElement.className + ' | from ' + from(); dlg().querySelector('[data-kc-pr-close]').click(); return r + ' | close -> ' + focusName() + ', unlocked ' + !document.body.classList.contains('overflow-hidden') + ' | errors ' + window.__fxErrors.length; })()"

echo "== 5 homepage: post, then the thank-you and the error reloads"
ev "(() => { $H sessionStorage.clear(); cta().click(); const f = fill(); f.querySelector('#KcPr-body').value = 'Hello from the homepage'; f.requestSubmit(); const s = JSON.parse(sessionStorage.getItem('kc-practitioner-request') || 'null'); return 'snapshot from ' + (s && s.opened_from) + ' opener ' + (s && s.opener); })()"
go "home-current-success.html?n=$N"
ev "new Promise(r => setTimeout(r, 400)).then(() => { $H settle(); const k = window.__fxKlaviyo[0]; const props = k && JSON.parse(k.body).data.attributes.properties; const d = dlg(); const r = 'thank-you dialog ' + d.open + ' | focus ' + document.activeElement.className + ' | klaviyo opened_from: ' + (props && props.opened_from); d.querySelector('[data-kc-pr-close]').click(); return r + ' | close -> ' + focusName(); })"
go "home-current.html?n=${N}b"
ev "(() => { $H sessionStorage.clear(); cta().click(); const f = fill(); f.querySelector('#KcPr-body').value = 'Kept after the error'; f.requestSubmit(); return 'saved'; })()"
go "home-current-error.html?n=$N"
ev "new Promise(r => setTimeout(r, 400)).then(() => { $H settle(); const d = dlg(); return 'error dialog ' + d.open + ' | alert focused ' + document.activeElement.matches('.kc-pr__alert') + ' | practice restored ' + document.querySelector('#KcPr-practice').value + ' | radio restored ' + !!document.querySelector('[data-kc-pr-profession]:checked') + ' | from ' + from() + ' | klaviyo calls ' + window.__fxKlaviyo.length; })"

echo "== 6 PDP: arriving with #KcPractitionerRequest-panel opens the popup"
go "pdp-current.html?n=$N#KcPractitionerRequest-panel"
ev "new Promise(r => setTimeout(r, 500)).then(() => { $H settle(); const d = dlg(); const r = 'open on arrival ' + d.open + ' | from ' + from() + ' | hash after ' + JSON.stringify(location.hash); d.querySelector('[data-kc-pr-close]').click(); return r + ' | close -> ' + focusName(); })"

echo "== 7 showModal throws: the links bring the form inline at the end of the page"
go "home-current.html?modal=throw&n=$N"
ev "new Promise(r => setTimeout(r, 300)).then(() => { $H cta().click(); const h = host(); return 'dialog ' + !!dlg() + ' | host shown ' + (getComputedStyle(h).display !== 'none') + ' | form in host ' + !!h.querySelector('[data-kc-pr] form') + ' | focus ' + document.activeElement.className + ' | locked ' + document.body.classList.contains('overflow-hidden') + ' | errors ' + window.__fxErrors.length; })"

echo "== 8 no JavaScript: the form is hidden until a link jumps to it"
go "pdp-current-nojs.html?n=$N"
ev "(() => { $H const before = getComputedStyle(host()).display; return 'host before ' + before + ' | FAQ links ' + document.querySelectorAll('.kc-faq-body a[href=\"#KcPractitionerRequest-panel\"]').length; })()"
go "pdp-current-nojs.html?n=${N}c#KcPractitionerRequest-panel"
ev "(() => { $H const h = host(); return 'after the jump: host ' + getComputedStyle(h).display + ' | form visible ' + (h.querySelector('form').getClientRects().length > 0); })()"
