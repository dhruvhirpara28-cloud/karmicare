# Homepage capture tools (A1 evidence)

Headless Chrome over the DevTools protocol, no dependencies (Node ≥ 22). `cap.mjs` loads a page per viewport and does the following:
- emulates the device: DPR, touch and hover media;
- scrolls through so lazy images and reveal observers fire;
- forces Day and Night through the theme's `.kc_day` / `.kc_night` switch;
- writes one PNG per section, `<section>-<vw>-<mode>-<tag>.png`, plus `page-<vw>-<mode>-<tag>.png` overviews (≤720 px wide);
- writes layout metrics from `metrics.js`: content extent, overflow, clipped boxes, smallest text, tap targets, image pixels needed vs served.

Chrome is DNS-limited to the store, cdn.shopify.com and Typekit (`--host-resolver-rules` in `cdp.mjs`, COMMON-RULES §4).

## Configs

| Config | What it captures |
|---|---|
| `before` (already run, 19 Oct) | Live homepage. The merged benefits CSS (6aa0e71) is served in place of the live file, and its index.json veil is emulated. |
| `after.json` | Live homepage with the branch's changed `section-*.css` files served in place of the live ones (`overrides`, CDP Fetch). Settings and inline-style changes are emulated in `after-emulate.css`; Liquid markup changes in `after-emulate.js` (DOM emulation, layout evidence only: real Liquid still needs the preview gate). |
| `pdp-before.json` / `pdp-after.json` | The five shared sections on the Duo PDP, before and after. |

## Run

```sh
node docs/homepage/capture/cap.mjs docs/homepage/capture/after.json
```

Chrome cannot start inside the Claude Code Seatbelt sandbox: it fails to bind its ProcessSingleton socket. The `before` run used the sandbox-disabled route, before the orchestrator froze that route. The `after` and PDP runs are **pending the orchestrator's browser route**. Any route that can (1) serve the listed asset overrides or inject the changed CSS, and (2) run `after-emulate.css` and `after-emulate.js` on the live page at the six widths can produce the same evidence.

Known artefact: the `before` shots still show Shopify's cookie panel at desktop widths in the hero. `after-emulate.js` hides it by content.
