# Practitioner form fixture (professionals page v1, phase 1 preview)

A local preview of the proposal in `../PROFESSIONALS-V1-PROPOSAL.md`. It never touches the store:
every form posts to this localhost server and `fx.js` stops the submit; Klaviyo calls are stubbed.
It replaces the scratchpad harness that the 26 Oct reboot wiped, and it lives in the worktree.

| File | What it does |
|---|---|
| `fetch-live.sh` | Anonymous snapshots of the live homepage, PDP and withdrawal page (EN/NL/FR) into `live/` (gitignored) |
| `live/form-texts-live.json` | The live EN/NL/FR texts of today's PDP form, side by side (kept: the source for carrying translations over) |
| `proto/kc-professionals-page.liquid` + `.css` | PROTOTYPE of the page section (phase 2 turns it into `sections/kc-professionals-request.liquid`) |
| `render.mjs` | liquidjs render of the prototype with the theme's own `snippets/kc-practitioner-request.liquid` into the live withdrawal page; PDP before and after |
| `fx.js` | Day/Night (`?mode=`), submit stop, the `?from=` prototype, `fxRun()` checks, `fxShow()` |
| `checks.sh <pageId>` | Every variant at 390 and 1440, Day and Night, through an Orca tab; results in `results/` |
| `shots.sh <pageId>` | Screenshots through `out/frame.html` into `shots/` |

Run:

```sh
cd docs/pdp/practitioner-form/fixture
npm install --cache "$TMPDIR/npm-cache"      # liquidjs 10.21.0, once
zsh fetch-live.sh                             # once, or to refresh
node render.mjs
python3 -I -m http.server 9376 --bind 127.0.0.1 --directory out
# then open http://127.0.0.1:9376/page-en.html (add ?mode=night, ?from=pdp-faq-kpni)
```

Variants: `page-en`, `page-en-success`, `page-en-error`, `page-nl`, `page-fr`, `page-en-nojs`, `pdp-before`, `pdp-after`.
