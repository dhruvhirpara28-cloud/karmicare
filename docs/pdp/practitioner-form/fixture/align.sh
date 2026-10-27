#!/bin/zsh
# Radios and checkboxes: the vertical offset between each control's centre and the centre of the
# first line of its label, at 390 and 1440 (Day); on pages with the popup it is opened first.
# align.sh <browserPageId> [variant ...]
P=${1:?browserPageId}; shift
VARIANTS=(${@:-page-en page-nl pdp-before})
B=http://127.0.0.1:9376
MEASURE="(() => {
  const opener = document.querySelector('a[data-kc-pr-open]');
  if (opener && document.querySelector('dialog.kc-pr-dialog')) { opener.click(); document.querySelectorAll('dialog').forEach(d => d.getAnimations().forEach(a => { try { a.finish(); } catch (e) {} })); }
  const out = [];
  let worst = 0;
  document.querySelectorAll('.kc-pr__check').forEach(lab => {
    const input = lab.querySelector('input');
    const span = lab.querySelector('span');
    if (!input || !span) return;
    const r = document.createRange(); r.selectNodeContents(span);
    const lines = Array.from(r.getClientRects());
    if (!lines.length || !input.getClientRects().length) return;
    const first = lines[0];
    const ic = input.getBoundingClientRect();
    const off = Math.round(((ic.top + ic.height / 2) - (first.top + first.height / 2)) * 10) / 10;
    worst = Math.max(worst, Math.abs(off));
    out.push(span.textContent.trim().slice(0, 18) + ' ' + off);
  });
  const s = document.querySelector('.kc-pr__check span');
  const cs = s && getComputedStyle(s);
  return 'worst ' + worst + 'px | font ' + (cs && cs.fontSize + '/' + cs.lineHeight) + ' | ' + out.join(' ; ');
})()"
for v in $VARIANTS; do
  for w in 390 1440; do
    orca goto --page $P --url "$B/$v.html?mode=day&n=$(date +%s)" --json >/dev/null 2>&1
    orca wait --page $P --load networkidle --json >/dev/null 2>&1
    orca exec --page $P --command "set viewport $w 900" --json >/dev/null 2>&1
    for i in 1 2; do orca screenshot --page $P --json >/dev/null 2>&1; done
    print -n "$v $w: "
    orca eval --page $P --expression "$MEASURE" --json 2>/dev/null | python3 -I -c 'import json,sys; d=json.load(sys.stdin); print(d.get("result",{}).get("result") or d.get("error"))'
  done
done
