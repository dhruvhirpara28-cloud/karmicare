/**
 * The (i) tooltips on a phone (Victor, 27 Nov): a tap opens the tooltip's text in a small sheet from the
 * bottom, in body text size, with the words next to the (i) as its heading; a tap outside it (or Esc)
 * slides it away and focus goes back to the (i). Every `.info-tip` with an `.info-tip-popover` on the
 * page: the plan cards' pills (Loop's plan descriptions), the receipt rows, the comparison tables, the
 * Year's side panel. From 750 px the hover popovers stay as they are. Styles: assets/kc-info-sheet.css.
 *
 * window.KCSheet.close(dialog) closes a bottom sheet after its slide down: the dialog's CSS gives
 * `.is-closing` its animation (a phone, motion allowed), else it closes at once. The side panel uses it
 * too (assets/loop-widget.js).
 */
(function () {
  'use strict';

  var phone = window.matchMedia('(max-width: 749px)');
  var closeLabel = (document.currentScript && document.currentScript.dataset.closeLabel) || 'Close';
  var sheet = null;

  function closeSheet(dialog) {
    if (!dialog.open || dialog.classList.contains('is-closing')) return;
    var inner = dialog.firstElementChild;
    var done = false;
    function finish() {
      if (done) return;
      done = true;
      dialog.classList.remove('is-closing');
      dialog.close();
    }
    // A closing animation is one that .is-closing starts: the opening one (the side panel from the
    // right on wider screens) does not count
    var before = inner ? getComputedStyle(inner).animationName : 'none';
    dialog.classList.add('is-closing');
    var after = inner ? getComputedStyle(inner).animationName : 'none';
    if (after === 'none' || after === before) {
      finish();
      return;
    }
    inner.addEventListener('animationend', function onEnd(event) {
      if (event.target !== inner) return;
      inner.removeEventListener('animationend', onEnd);
      finish();
    });
    // Never left open if the animation does not run to its end
    setTimeout(finish, 400);
  }

  window.KCSheet = { close: closeSheet };

  // The words next to the (i): a pill's text, a receipt row's or a table row's label
  function labelOf(tip) {
    var host = tip.closest('.kc-return_care') || tip.parentElement;
    if (!host) return '';
    var words = host.cloneNode(true);
    words.querySelectorAll('.info-tip').forEach(function (el) { el.remove(); });
    var text = words.textContent.replace(/\s+/g, ' ').trim();
    return text.length <= 120 ? text : '';
  }

  function sheetElement() {
    if (sheet) return sheet;
    sheet = document.createElement('dialog');
    sheet.className = 'kc-info-sheet';
    // A click on the sheet itself is a click outside its content
    sheet.addEventListener('click', function (event) {
      if (event.target === sheet) closeSheet(sheet);
    });
    sheet.addEventListener('cancel', function (event) {
      event.preventDefault();
      closeSheet(sheet);
    });
    sheet.addEventListener('close', function () {
      // Opened again before this event came: that one keeps the lock and its (i)
      if (sheet.open) return;
      document.documentElement.classList.remove('kc-info-sheet-open');
      if (sheet.kcOpener && sheet.kcOpener.isConnected && document.activeElement !== sheet.kcOpener) {
        sheet.kcOpener.focus({ preventScroll: true });
      }
    });
    document.body.appendChild(sheet);
    return sheet;
  }

  function open(tip) {
    var popover = tip.querySelector('.info-tip-popover');
    var dialog = sheetElement();
    dialog.kcOpener = tip;
    var inner = document.createElement('div');
    inner.className = 'kc-info-sheet__inner';
    // Focus lands on the text, so a screen reader reads it first; the close button is the next stop
    inner.tabIndex = -1;
    inner.setAttribute('autofocus', '');
    var handle = document.createElement('span');
    handle.className = 'kc-info-sheet__handle';
    handle.setAttribute('aria-hidden', 'true');
    // For keyboards and screen readers: shown only when it has keyboard focus
    var close = document.createElement('button');
    close.type = 'button';
    close.className = 'kc-info-sheet__close';
    close.textContent = closeLabel;
    close.addEventListener('click', function () { closeSheet(dialog); });
    inner.append(handle, close);
    var label = labelOf(tip);
    if (label) {
      var heading = document.createElement('p');
      heading.className = 'kc-info-sheet__heading';
      heading.id = 'kc-info-sheet-heading';
      heading.textContent = label;
      inner.appendChild(heading);
      dialog.setAttribute('aria-labelledby', heading.id);
    } else {
      dialog.removeAttribute('aria-labelledby');
    }
    var text = document.createElement('div');
    text.className = 'kc-info-sheet__text';
    var paragraphs = popover.querySelectorAll('p');
    if (paragraphs.length) {
      paragraphs.forEach(function (p) { text.appendChild(p.cloneNode(true)); });
    } else {
      var p = document.createElement('p');
      p.textContent = popover.textContent.replace(/\s+/g, ' ').trim();
      text.appendChild(p);
    }
    inner.appendChild(text);
    dialog.replaceChildren(inner);
    dialog.classList.remove('is-closing');
    document.documentElement.classList.add('kc-info-sheet-open');
    // The (i) has focus when the sheet opens, so the browser gives it back on closing
    decorateTip(tip);
    if (document.activeElement !== tip) tip.focus({ preventScroll: true });
    if (!dialog.open) dialog.showModal();
  }

  function tipOf(target) {
    var tip = target && target.closest ? target.closest('.info-tip') : null;
    return tip && tip.querySelector('.info-tip-popover') && !(sheet && sheet.contains(tip)) ? tip : null;
  }

  // Before the page's own handlers (the comparison tables' tap toggle, Loop's plan card click): on a
  // phone a tap on an (i) only opens its sheet
  document.addEventListener('click', function (event) {
    if (!phone.matches) return;
    var tip = tipOf(event.target);
    if (!tip) return;
    event.preventDefault();
    event.stopPropagation();
    open(tip);
  }, true);

  document.addEventListener('keydown', function (event) {
    if (!phone.matches || (event.key !== 'Enter' && event.key !== ' ')) return;
    var tip = tipOf(event.target);
    if (!tip || event.target !== tip) return;
    event.preventDefault();
    event.stopPropagation();
    open(tip);
  }, true);

  // On a phone each (i) is a button named after its words; Loop and the receipt add theirs later, so
  // new ones are picked up as they come. From 750 px they are plain again.
  function decorateTip(tip) {
    if (tip.hasAttribute('data-kc-sheet')) return;
    tip.setAttribute('data-kc-sheet', '');
    tip.setAttribute('role', 'button');
    tip.setAttribute('tabindex', '0');
    tip.setAttribute('aria-haspopup', 'dialog');
    var label = labelOf(tip);
    if (label) tip.setAttribute('aria-label', label);
  }

  function decorate() {
    document.querySelectorAll('.info-tip').forEach(function (tip) {
      if (!tip.querySelector('.info-tip-popover')) return;
      if (phone.matches) {
        decorateTip(tip);
      } else if (tip.hasAttribute('data-kc-sheet')) {
        ['data-kc-sheet', 'role', 'tabindex', 'aria-haspopup', 'aria-label'].forEach(function (name) {
          tip.removeAttribute(name);
        });
      }
    });
  }

  var queued = false;
  function queueDecorate() {
    if (queued) return;
    queued = true;
    setTimeout(function () {
      queued = false;
      decorate();
    }, 250);
  }

  document.documentElement.classList.add('kc-info-sheets');
  decorate();
  new MutationObserver(function () {
    if (phone.matches) queueDecorate();
  }).observe(document.body, { childList: true, subtree: true });
  phone.addEventListener('change', function () {
    if (!phone.matches && sheet && sheet.open) sheet.close();
    decorate();
  });
})();
