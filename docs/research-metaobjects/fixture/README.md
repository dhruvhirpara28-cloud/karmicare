# Research cards fixture (R67)

Proves that `sections/research-behind-system.liquid` and `snippets/research-card.liquid`
print the same HTML from the section's blocks as from `research_card` metaobject entries,
and that the block path still prints what it printed at b0bb4fb. No Shopify store is
involved: liquidjs renders the Liquid locally with the Shopify filters stubbed, and the
browser part runs from `file://`.

```sh
cd docs/research-metaobjects/fixture
npm install --no-save liquidjs@10.21.0     # node_modules/ only, nothing is saved to the repo
node render.mjs                            # 14 PASS lines, then out/
```

`render.mjs` renders the section three ways (old code at b0bb4fb with blocks, new code with
blocks, new code with stubbed entries) for the homepage marquee, the PDP marquee and a
grid/slider variant, compares them, and checks the rich text walker on its own. Results go
to `out/liquid-results.txt`.

Then open `out/frame-1440.html` and `out/frame-390.html` (add `?mode=night` for Night) in a
browser. Each loads `out/fixture.html` in an iframe of that width; the page runs its checks
on load and prints them above the iframe. Inside the fixture, `fxRun()` re-runs the checks,
`fxFocusPrep()` focuses the second entry card's link so a real Tab key reaches the third,
and `fxFocusCheck()` reports whether the marquee revealed that card and held still.

Images are SVG placeholders written to `out/img/`: the store's files are not in the repo.
`out/` and `node_modules/` are generated and stay out of git.
