(() => {
    const enhanced = new WeakSet();
    const opened = new WeakSet();

    const enhance = (dialog, banner, expanded) => {
        if (enhanced.has(dialog)) return;

        const header = dialog.querySelector('header');
        const actions = dialog.querySelector('.shopify-pc__prefs__header-actions');
        const options = dialog.querySelector('.shopify-pc__prefs__scrollable');
        const save = dialog.querySelector('#shopify-pc__prefs__header-save');
        const sourceManage = banner?.querySelector('#shopify-pc__banner__btn-manage-prefs');
        const sourceCopy = banner?.querySelector('.shopify-pc__banner__body p');
        if (!header || !actions || !options || !save || !sourceManage || !sourceCopy) return;

        enhanced.add(dialog);
        dialog.classList.add('kc-cookie-panel');
        dialog.setAttribute('aria-modal', 'false');
        const copy = sourceCopy.cloneNode(true);
        copy.querySelectorAll('[id]').forEach((element) => element.removeAttribute('id'));
        header.appendChild(copy);
        dialog.querySelector('h2').textContent = banner.querySelector('h2').textContent;

        ['accept', 'decline'].forEach((action) => {
            const source = banner.querySelector(`#shopify-pc__banner__btn-${action}`);
            const target = dialog.querySelector(`#shopify-pc__prefs__header-${action}`);
            if (source && target) target.textContent = source.textContent;
        });

        const manage = document.createElement('button');
        manage.type = 'button';
        manage.className = 'kc-cookie-manage';
        manage.textContent = sourceManage.textContent;
        manage.id = sourceManage.id;
        sourceManage.removeAttribute('id');
        options.id = 'kc-cookie-options';
        manage.setAttribute('aria-controls', options.id);
        const setExpanded = (value) => {
            manage.setAttribute('aria-expanded', String(value));
            options.hidden = !value;
            save.hidden = !value;
        };
        manage.addEventListener('click', () => setExpanded(manage.getAttribute('aria-expanded') !== 'true'));
        actions.insertBefore(manage, save);
        dialog.appendChild(actions);
        setExpanded(expanded);

        dialog.addEventListener('keydown', (event) => {
            if (event.key !== 'Tab') return;
            event.stopImmediatePropagation();
        }, true);
        banner.style.display = 'none';
        document.body.style.removeProperty('overflow');
    };

    const sync = () => {
        const banner = document.querySelector('#shopify-pc__banner');
        const dialog = document.querySelector('#shopify-pc__prefs__dialog');
        if (dialog) {
            enhance(dialog, banner, !opened.has(banner));
            if (enhanced.has(dialog) && banner?.style.display !== 'none') banner.style.display = 'none';
            return;
        }
        if (!banner || opened.has(banner) || getComputedStyle(banner).display === 'none') return;
        const manage = banner.querySelector('#shopify-pc__banner__btn-manage-prefs');
        if (!manage) return;
        opened.add(banner);
        const previousFocus = document.activeElement;
        manage.click();
        const panel = document.querySelector('#shopify-pc__prefs__dialog');
        if (panel) enhance(panel, banner, false);
        if (previousFocus === document.body) document.activeElement?.blur();
        else previousFocus?.focus({ preventScroll: true });
    };

    new MutationObserver((mutations) => {
        if (mutations.some((mutation) => mutation.type === 'childList' ||
            ['shopify-pc__banner', 'shopify-pc__prefs'].includes(mutation.target.id))) sync();
    }).observe(document.body, { childList: true, subtree: true, attributes: true, attributeFilter: ['style'] });
    sync();
})();
