# Screenshot labels (A3 / A3b)

The PNGs are gitignored and stay on Victor's machine. The labels are tracked: this file and the JSON sidecars.

| Folder | Captured | Route | Hidden in the picture | States |
|---|---|---|---|---|
| `home/`, `pdp/` | 19 Oct, 19:12–20:10 | `docs/utopia/tools/measure.mjs`: headless Chrome **outside the sandbox**, read-only public GETs, before the no-unsandboxed rule (REPORT §0) | **Yes**: `#shopify-pc__banner`, `#shopify-pc__prefs__dialog`, `#stickyCta`, `.sticky-cta` (`display: none`). No consent banner or sticky buy bar in any shot. | `-before` live; `-after` with A3 `kc-fluid.css`; `-preview` with `adoption-preview.css` too |
| `compare/` | 19 Oct, from the A3 shots above | `docs/utopia/tools/compose.mjs` crops | Same as above | – |
| `a3b/home/`, `a3b/pdp/` | 19 Oct, 22:07–22:20 | Approved Orca browser helper `.orca/mission-runtime/browser.py` (isolated anonymous page, sandboxed caller) | **Nothing.** The consent banner shows in its first-visit state; the sticky bar shows after scrolling. | `-before` = setting off (live page); `-after` = `docs/utopia/inject/fluid-on.css`; `-after-wide` = `fluid-on-wide.css`; `-a3alone` = A3 `kc-fluid.css` of f176627 |

Each `a3b/` PNG has a sidecar `.json` written by the helper: URL, actual viewport, body classes (Day/Night), whether CSS was injected and the file path. The homepage is in Day mode via its own `.kc_day` control. The PDP is in Night by the visitor clock, because it has no mode control the helper may click; type sizes do not depend on the mode.
