/* Preview only (/copy/ variant, docs/buybox-ab/PLAN.md 4b): the Year card's "€59 per Duo, billed once a
   year" line in its sub-row, between "6 Duos a year …" and the per-brushing line. Not theme code: if
   Victor keeps it, it becomes a kc.receipt key and a line in assets/loop-widget.js. */
(function () {
  var YEAR_GROUP = 'ab8930cda8d5182e7420ef18797bb86a2f9ae26c';
  var DUOS = 6;

  function apply() {
    var box = document.querySelector('.kc-buybox');
    if (!box) return;
    box.querySelectorAll('.loop-subscription-group').forEach(function (group) {
      var radio = group.querySelector('.loop-subscription-group-radio');
      if (!radio || radio.dataset.id !== YEAR_GROUP) return;
      var sub = group.querySelector('.kc-plan-subrow');
      var price = group.querySelector('.loop-subscription-group-price-amount');
      if (!sub || !price || typeof loopFormatMoney !== 'function') return;
      var euros = parseFloat(price.textContent.replace(/[^\d.,]/g, '').replace(',', '.'));
      if (!euros) return;
      var text = loopFormatMoney(Math.round((euros * 100) / DUOS), true) + ' per Duo, billed once a year';
      var line = sub.querySelector('.kc-copy-per-duo');
      if (line && line.textContent === text && sub.children[1] === line) return;
      if (!line) {
        line = document.createElement('div');
        line.className = 'kc-copy-per-duo';
      }
      line.textContent = text;
      sub.insertBefore(line, sub.children[1] || null);
    });
  }

  new MutationObserver(apply).observe(document.documentElement, { childList: true, subtree: true, characterData: true });
  apply();
})();
