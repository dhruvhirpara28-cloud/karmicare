# Rating fixture (R95)

Renders the hero professionals badge (`sections/hero-karmicare.liquid`, block
`testimonial_badge`) and the PDP category strip (`snippets/product-category-strip.liquid`)
with liquidjs, from the values in `templates/index.json` and
`templates/product.subscription-item.json`, then lays them out under the theme's own CSS in
a `file://` page. No Shopify store is involved.

liquidjs cannot prove Shopify objects: `product.metafields`, `request.locale`, `image_url`,
`image_tag`, `placeholder_svg_tag`, `inline_asset_content`, `asset_url` and `t` are stubbed in
`render.mjs`. A Liquid error that only Shopify would raise is not caught here; the live check
after landing is `grep "Liquid error"` on the rendered pages.

```sh
cd docs/reviews/fixture
npm install --no-save liquidjs@10.21.0       # or LIQUIDJS=<path to an installed liquidjs>
node render.mjs                               # PASS/FAIL lines, exit 1 on any FAIL, then out/
```

Then open `out/frame-1440.html` (add `?mode=night` for Night), or
`out/frame-multi.html?frames=390:day,390:night,320:day,320:night&h=560` for several widths on
one page. Each frame loads `out/fixture.html` in an iframe of that width, runs the layout
checks on load and prints them above the frame: badge rating text on one line and the whole
badge still a link, strip rating on the artwork row, the text per locale, the accessible
name, the colours in Day and Night, and what the strip row needs in width with the new and
the old text.

`out/` and `node_modules/` are generated and stay out of git.
