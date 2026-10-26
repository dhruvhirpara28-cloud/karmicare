#!/bin/zsh
# Professionals page v1 preview checks: every variant at 390 and 1440, Day and Night.
# Needs the preview server (python3 -I -m http.server 9376 --bind 127.0.0.1 --directory out)
# and an Orca tab in the isolated anonymous profile: checks.sh <browserPageId>
P=${1:?browserPageId}
B=http://127.0.0.1:9376
HERE=${0:a:h}
mkdir -p $HERE/results
for v in "page-en?from=pdp-faq-kpni" page-en-success page-en-error page-nl page-fr page-en-nojs pdp-after; do
  for w in 390 1440; do
    for m in day night; do
      url="$B/${v%%\?*}.html?mode=$m"; [[ $v == *\?* ]] && url="$url&${v#*\?}"
      orca goto --page $P --url "$url" --json >/dev/null 2>&1
      orca wait --page $P --load networkidle --json >/dev/null 2>&1
      orca exec --page $P --command "set viewport $w 900" --json >/dev/null 2>&1
      orca screenshot --page $P --json >/dev/null 2>&1
      orca eval --page $P --expression "JSON.stringify((r => ({ v: r.variant, m: r.mode, w: r.width, pass: r.pass, n: r.checks.length, failed: r.failed.map(c => c.name + ' (' + c.detail + ')') }))(window.fxRun()))" --json 2>/dev/null \
        | python3 -I -c 'import json,sys; d=json.load(sys.stdin); print(d.get("result",{}).get("result") or d.get("error"))'
    done
  done
done
