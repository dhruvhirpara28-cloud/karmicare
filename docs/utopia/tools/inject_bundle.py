#!/usr/bin/env python3
"""Write the CSS the theme loads with fluid type on, for injection into the live pages.

The approved browser helper injects one local CSS file (.orca/mission-runtime/browser.py css).
With the theme setting kc_fluid_type on, layout/theme.liquid loads kc-fluid.css, then
kc-fluid-wide.css when kc_fluid_type_wide is on too, then the style block that
snippets/kc-fluid-bridge.liquid renders. This script joins the same pieces in the same
order and renders the bridge the way the snippet does for the current
config/settings_data.json (read only). It mirrors the Liquid; the snippet itself is
checked by Theme Check, and its rendered output stays pending the preview gate.

  docs/utopia/inject/fluid-on.css        kc_fluid_type on
  docs/utopia/inject/fluid-on-wide.css   kc_fluid_type and kc_fluid_type_wide on

Run from the repo root:  python3 docs/utopia/tools/inject_bundle.py
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "docs/utopia"))
from generate import DAWN_BRIDGE, MOBILE_W, DESKTOP_W, ROOT_PX  # noqa: E402
from adoption_preview import settings  # noqa: E402

OUT = ROOT / "docs/utopia/inject"
FIGMA = json.loads((ROOT / "docs/utopia/kc-tokens.json").read_text())["collections"]["responsive"]["vars"]


def liquid_float(value):
    """Liquid prints `n | divided_by: 10.0` like Ruby: 2.2, 2.0."""
    return repr(float(value))


def bridge(get):
    start_rem = f"{MOBILE_W / ROOT_PX:g}"
    lines = ["/* snippets/kc-fluid-bridge.liquid, rendered for config/settings_data.json */"]
    for selector, prop, key, role, scaled in DAWN_BRIDGE:
        mb, dk = get(f"{key}_mobile"), get(f"{key}_desktop")
        figma_dk, figma_mb = FIGMA[f"{role}/text size"]
        token = (mb, dk) == (figma_mb, figma_dk) and (not scaled or get("heading_scale") == get("body_scale"))
        if token:
            value = f"var(--kc-responsive-{role}-text-size)"
        else:
            value = (f"clamp({liquid_float(min(mb, dk) / 10)}rem, {liquid_float(mb / 10)}rem + {dk - mb} * "
                     f"(100vw - {start_rem}rem) / {DESKTOP_W - MOBILE_W}, {liquid_float(max(mb, dk) / 10)}rem)")
            if scaled:
                value = f"calc(var(--font-heading-scale) * {value})"
        lines.append(f"{selector} {{ {prop}: {value}; }} /* setting {mb}/{dk}, Figma {role} {figma_mb}/{figma_dk} */")
    return "\n".join(lines + [""])


def main():
    OUT.mkdir(exist_ok=True)
    fluid = (ROOT / "assets/kc-fluid.css").read_text()
    wide = (ROOT / "assets/kc-fluid-wide.css").read_text()
    dawn = bridge(settings())
    for name, parts in (("fluid-on.css", [fluid, dawn]), ("fluid-on-wide.css", [fluid, wide, dawn])):
        (OUT / name).write_text("\n".join(parts))
        print(f"wrote {(OUT / name).relative_to(ROOT)}")
    print(dawn)


if __name__ == "__main__":
    main()
