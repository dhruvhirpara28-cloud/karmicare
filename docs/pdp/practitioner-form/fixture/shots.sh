#!/bin/zsh
# Screenshots for the proposal: the page at 390 and 1440 in Day and Night, the PDP before and after
# at the FAQ. Through frame.html (an iframe of the given size): scrolled direct captures come back
# blank in the Orca tab. Usage: shots.sh <browserPageId>
P=${1:?browserPageId}
B=http://127.0.0.1:9376
HERE=${0:a:h}
mkdir -p $HERE/shots
shot() { # name src w h part
  orca goto --page $P --url "$B/frame.html?src=$(python3 -I -c 'import sys,urllib.parse; print(urllib.parse.quote(sys.argv[1], safe=""))' "$2")&w=$3&h=$4" --json >/dev/null 2>&1
  orca wait --page $P --load networkidle --json >/dev/null 2>&1
  orca exec --page $P --command "set viewport $3 $4" --json >/dev/null 2>&1
  for i in 1 2 3; do orca screenshot --page $P --json >/dev/null 2>&1; done
  orca eval --page $P --expression "new Promise(r => setTimeout(r, 1500)).then(() => document.getElementById('f').contentWindow.fxShow('$5'))" --json >/dev/null 2>&1
  for i in 1 2; do orca screenshot --page $P --json >/dev/null 2>&1; done
  orca screenshot --page $P --json 2>/dev/null | python3 -I -c 'import json,sys,base64; d=json.load(sys.stdin); open(sys.argv[1],"wb").write(base64.b64decode(d["result"]["data"]))' "$HERE/shots/$1.png"
  echo "$1"
}
for m in day night; do
  shot page-390-$m "page-en.html?mode=$m&from=pdp-faq-kpni" 390 900 top
  shot page-1440-$m "page-en.html?mode=$m&from=pdp-faq-kpni" 1440 900 top
  shot page-form-390-$m "page-en.html?mode=$m" 390 900 form
done
shot pdp-before-faq-390 "pdp-before.html?mode=day" 390 900 faq
shot pdp-after-faq-390 "pdp-after.html?mode=day" 390 900 faq
shot pdp-before-faq-1440 "pdp-before.html?mode=day" 1440 900 faq
shot pdp-after-faq-1440 "pdp-after.html?mode=day" 1440 900 faq
