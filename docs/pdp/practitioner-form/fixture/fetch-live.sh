#!/bin/zsh
# Anonymous snapshots of the live store pages the fixture builds on (no cookies, no login).
# Writes live/*.html; run from anywhere. The store's primary domain is www.karmicare.com.
HERE=${0:a:h}
mkdir -p $HERE/live
for p in "/:home-en" "/nl:home-nl" "/fr:home-fr" \
  "/products/karmicare-biorhythmic-oral-care-system:pdp-en" \
  "/nl/products/karmicare-biorhythmic-oral-care-system:pdp-nl" \
  "/fr/products/karmicare-biorhythmic-oral-care-system:pdp-fr" \
  "/pages/withdrawal:withdrawal-en" "/nl/pages/withdrawal:withdrawal-nl" "/fr/pages/withdrawal:withdrawal-fr"; do
  curl -s -L -m 30 -A "Mozilla/5.0" -o "$HERE/live/${p##*:}.html" -w "${p##*:} %{http_code}\n" "https://www.karmicare.com${p%%:*}"
done
