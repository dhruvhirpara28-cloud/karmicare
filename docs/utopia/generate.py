#!/usr/bin/env python3
"""Generate assets/kc-tokens.css and the fluid type layer from docs/utopia/kc-tokens.json.

A3 prototype (docs/utopia/REPORT.md): a copy of docs/design-tokens/generate.py as of
98ef34f (18 Oct) with one addition, emit_fluid() at the end, which writes
assets/kc-fluid.css, assets/kc-fluid-wide.css and snippets/kc-fluid-bridge.liquid. The
kc-tokens.css part is unchanged and must reproduce the committed file byte for byte;
kc-tokens.json is the 18 Oct export from 98ef34f. layout/theme.liquid loads the fluid
layer only when the theme setting kc_fluid_type is on (A3b).

Run from the repo root:  python3 docs/utopia/generate.py
Never edit assets/kc-tokens.css, assets/kc-fluid*.css or snippets/kc-fluid-bridge.liquid
by hand: fix the value in Figma, re-export kc-tokens.json (see export.md), run this
script, commit the files.

Additive rule: any --kc-* name the theme already defines (a `--kc-x:`
declaration outside docs/ and this generated file) is NOT emitted. Those names
keep their current source until a later step moves them here on purpose. The
header of the generated file lists them. Names the theme only reads are emitted:
reading a generated token is what the file is for.

Names moved here from hand-typed CSS whose Figma value differs from what the
site renders today are emitted from HELD_AT_OLD_VALUE below, not from Figma
(RUNBOOK section 1 rule 6: no unapproved visual change). COMPAT_ALIASES carries
the old names that have no Figma path of their own.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "docs/utopia/kc-tokens.json"
OUT = ROOT / "assets/kc-tokens.css"
FLUID_OUT = ROOT / "assets/kc-fluid.css"
WIDE_OUT = ROOT / "assets/kc-fluid-wide.css"
BRIDGE_OUT = ROOT / "snippets/kc-fluid-bridge.liquid"
BREAKPOINT = "750px"  # Dawn's own breakpoint, mirrors Figma desktop/mobile (D8)

FONT_STACKS = {
    "Proxima Nova": '"Proxima Nova", "proxima-nova", sans-serif',
    "Nunito": '"Nunito", sans-serif',
    "Marlide Display": '"Marlide Display", "marlide-display-variable", serif',
    "Space Grotesk": '"Space Grotesk", sans-serif',
    "Geist Mono": '"Geist Mono", monospace',
    "Noto Serif": '"Noto Serif", serif',
}


# Compatibility / held-at-old-value map (RUNBOOK section 1 rule 6, PLAN Steps 2-4).
# Each name below was hand-typed in layout/theme.liquid (or, for None, only read
# by the theme). Its Figma value would change what the site renders, so it keeps
# the exact value it had in docs/design-tokens/baseline/computed-before.json, on
# :root, the same in Day and Night. A held colour also gets its -rgb twin, computed
# from the held value (not from Figma), so the hex and the triplet always agree.
# Each entry is a proposal for Victor in docs/design-tokens/baseline/proposals.md.
# To accept a proposal: delete its line, regenerate, review the delta, commit.
# Each value is (old value, proposal id):
#   str  -> emitted with that value
#   None -> not emitted at all: the theme reads it with a var() fallback today,
#           and defining it would replace the fallback
HELD_AT_OLD_VALUE = {
    # Step 2: mapped colours. Figma Day | Night in the comment.
    "--kc-mapped-text-primary-default": ("#FFFBF6", "P1"),  # #191f38 | #fffbf6
    "--kc-mapped-surface-primary-default": ("#191F38", "P2"),  # #fffbf6 | #191f38
    "--kc-mapped-surface-secondary-default": ("#212A49", "P3"),  # #ffffff | #212a49
    "--kc-mapped-surface-tertiery-default": ("#DDDBD9", "P4"),  # surface/tertiary/default #dddbd9 | #2c3a60 (Loop widget spelling)
    "--kc-mapped-bg-primary-default": ("#2C3A60", "P5"),  # no Figma path; surface/page is #fffbf6 | #191f38
    # Step 2: read with a fallback, never defined. Figma mobile | desktop in the comment.
    "--kc-responsive-spacing-section-sm": (None, "P6"),  # 48px | 80px; research section renders its 2rem fallback
    # Step 4: responsive, hand-typed with one value for every width. Figma desktop | mobile in the comment.
    "--kc-responsive-h1-letter-spacing": ("-1.25px", "P7"),  # -2px | -1.25px
    "--kc-responsive-h2-letter-spacing": ("-1px", "P8"),  # -1.5px | -1px
    "--kc-responsive-h3-letter-spacing": ("-1px", "P9"),  # -1px | -0.5px
    "--kc-responsive-h4-letter-spacing": ("-1px", "P10"),  # -1px | -0.25px
    "--kc-responsive-h5-letter-spacing": ("-0.5px", "P11"),  # -0.5px | -0.25px; nothing reads it
    "--kc-responsive-caption-letter-spacing": ("1.25px", "P12"),  # 1.7px | 1.2px
    "--kc-responsive-Nunito-letter-spacing": ("1.7px", "P13"),  # no Figma path; caption is 1.7px | 1.2px
    "--kc-responsive-h4-letter-spacing-sm": ("-0.25px", "P14"),  # no Figma path; h4 is -1px | -0.25px
    "--kc-responsive-caption-sm-letter-spacing": ("1px", "P15"),  # no Figma path; nothing reads it
    "--kc-responsive-all-letter-spacing": ("0.5px", "P16"),  # no Figma path
    "--kc-responsive-body-line-height": ("20px", "P17"),  # no Figma path; body-md is 24px | 20px
    # --kc-responsive-label-sm-text-size (P18) stays in layout/theme.liquid: it follows the
    # theme setting body_small_font_size_all, which a held literal here would cut off.
}

# Old names with no Figma path of their own. Each points at the generated token
# with the same meaning and the same value in Day and Night. Each also gets an -rgb
# alias to the target's -rgb twin.
COMPAT_ALIASES = {
    "--kc-mapped-surface-accent-soft": "var(--kc-mapped-surface-accent-default-subtle)",  # #c4dfff | #c4dfff
    "--kc-white-surface-primary-default": "var(--kc-brand-fixed-white)",                  # #ffffff
}


def slug(path):
    s = path.lower().replace("/", "-")
    s = re.sub(r"[^a-z0-9-]+", "-", s)
    return re.sub(r"-+", "-", s).strip("-")


def num(v):
    return ("%g" % v) if isinstance(v, (int, float)) else str(v)


def px(v):
    return "0" if v == 0 else num(v) + "px"


def rgb_triplet(color):
    if color.startswith("#") and len(color) == 7:
        return ",".join(str(int(color[i:i + 2], 16)) for i in (1, 3, 5))
    return None  # rgba values carry their own alpha: no triplet


def theme_defined_names():
    """Every --kc-* name declared (`--kc-x:`) in tracked theme files.

    assets/kc-fluid.css and kc-fluid-wide.css are generated here too and redefine
    --kc-responsive-* names on purpose, so they are excluded like kc-tokens.css.
    docs/design-tokens/generate.py needs the same exclusion once they land, or it would
    hold those names back.
    """
    out = subprocess.run(
        ["git", "grep", "-ohE", "-e", r"--kc-[a-zA-Z0-9_-]+\s*:", "--", ".",
         ":!docs", ":!assets/kc-tokens.css", ":!assets/kc-fluid.css", ":!assets/kc-fluid-wide.css"],
        cwd=ROOT, capture_output=True, text=True, check=True).stdout
    return {n.rstrip(":").strip() for n in out.split() if n != ":"}


def main():
    data = json.loads(SRC.read_text())
    cols = data["collections"]
    defined = theme_defined_names()
    compat_names = set(HELD_AT_OLD_VALUE) | set(COMPAT_ALIASES)
    compat_names |= {n + "-rgb" for n in compat_names}
    clash = sorted(defined & compat_names)
    if clash:
        sys.exit("still defined in the theme, remove the hand-typed line first: " + ", ".join(clash))
    taken = defined | compat_names
    held, emitted = [], []

    def decl(name, value, block):
        if name in taken:
            if name in defined:
                held.append(name)
            return
        emitted.append(name)
        block.append(f"  {name}: {value};")

    root, day, night, desktop = [], [], [], []

    for path, val in cols["brand"]["vars"].items():
        name = f"--kc-brand-{slug(path)}"
        value = px(val) if isinstance(val, (int, float)) else val
        decl(name, value, root)
        if isinstance(val, str) and rgb_triplet(val):
            decl(name + "-rgb", rgb_triplet(val), root)

    for path, val in cols["shape"]["vars"].items():
        name = f"--kc-shape-{slug(path)}"
        decl(name, num(val / 100) if path.startswith("opacity/") else px(val), root)

    for path, val in cols["font"]["vars"].items():
        if path.startswith("weight/"):
            continue
        decl(f"--kc-font-{slug(path)}", FONT_STACKS.get(val, f'"{val}", sans-serif'), root)

    for path, (dk, mb) in cols["responsive"]["vars"].items():
        if path.startswith(("size/testimonial/", "visibility/")):
            continue
        name = f"--kc-responsive-{slug(path)}"
        decl(name, px(mb), root)
        if dk != mb and name not in taken:
            desktop.append(f"    {name}: {px(dk)};")

    for eff in data["effects"]:
        if not eff["name"].startswith("elevation/"):
            continue
        shadows, blur = [], None
        for typ, color, x, y, radius, spread in eff["e"]:
            if typ == "DROP_SHADOW":
                shadows.append(f"{px(x)} {px(y)} {px(radius)} {px(spread or 0)} {color}")
            elif typ == "INNER_SHADOW":
                shadows.append(f"inset {px(x)} {px(y)} {px(radius)} {px(spread or 0)} {color}")
            elif typ == "BACKGROUND_BLUR":
                blur = radius
        base = f"--kc-{slug(eff['name'])}"
        if shadows:
            decl(base, ", ".join(shadows), root)
        if blur is not None:
            decl(base + "-backdrop-blur", px(blur), root)

    for path, (d, n) in cols["mapped"]["vars"].items():
        name = f"--kc-mapped-{slug(path)}"
        decl(name, d, day)
        if name in taken:
            continue
        night.append(f"  {name}: {n};")
        if rgb_triplet(d):
            decl(name + "-rgb", rgb_triplet(d), day)
            if rgb_triplet(n):
                night.append(f"  {name}-rgb: {rgb_triplet(n)};")

    compat = []
    for name, (value, pid) in HELD_AT_OLD_VALUE.items():
        if value is None:
            compat.append(f"  /* {name}: not emitted, held at its var() fallback ({pid}) */")
        else:
            compat.append(f"  {name}: {value}; /* held at old value ({pid}) */")
            if rgb_triplet(value):
                compat.append(f"  {name}-rgb: {rgb_triplet(value)}; /* the held value as a triplet ({pid}) */")
    for name, value in COMPAT_ALIASES.items():
        compat.append(f"  {name}: {value};")
        target = re.fullmatch(r"var\((--kc-[a-z0-9-]+)\)", value)
        if target and target.group(1) + "-rgb" in emitted:
            compat.append(f"  {name}-rgb: var({target.group(1)}-rgb);")
        elif target:
            sys.exit(f"{name}: {target.group(1)} has no -rgb twin to alias")

    src = data["source"]
    held_sorted = sorted(set(held))
    lines = [
        f"/* GENERATED from {src['file']} (Figma {src['fileKey']}) on {src['exported']}. DO NOT EDIT.",
        "   Source: docs/design-tokens/kc-tokens.json. Regenerate: python3 docs/design-tokens/generate.py",
        "   Naming: --kc-<collection>-<figma path, '/' and spaces to '-'>. Opaque colours also ship as -rgb triplets.",
        "   Mapped colours: Day on :root and body.day-mode, Night on body.night-mode (the class assets/day-night-mode.js sets).",
        f"   Responsive: mobile values on :root, desktop values from {BREAKPOINT}.",
        f"   Held back ({len(held_sorted)}): these names already exist in the theme and keep their current source",
        "   until a later step moves them here on purpose:",
    ]
    lines += [f"     {n}" for n in held_sorted]
    lines += ["*/", "", ":root {"] + root + ["}", "", ":root,", "body.day-mode {"] + day + ["}", "",
              "body.night-mode {"] + night + ["}", "",
              f"@media screen and (min-width: {BREAKPOINT}) {{", "  :root {"] + desktop + ["  }", "}", ""]
    lines += ["/* Compatibility: names the theme read before they came from Figma (generate.py",
              "   HELD_AT_OLD_VALUE and COMPAT_ALIASES). Same value in Day and Night. Held values are",
              "   proposals for Victor: docs/design-tokens/baseline/proposals.md */",
              ":root {"] + compat + ["}", ""]
    OUT.write_text("\n".join(lines))
    print(f"wrote {OUT.relative_to(ROOT)}: {len(emitted)} declarations "
          f"(+{len(night)} night, +{len(desktop)} desktop), {len(held_sorted)} held back, "
          f"{len(compat)} compatibility, {OUT.stat().st_size} bytes")
    for n in held_sorted:
        print("  held:", n)
    emit_fluid(data, taken)


# Fluid layer (A3, docs/utopia/REPORT.md). Route A: each responsive pair whose mobile and
# desktop values differ becomes one clamp() from the 393 px mobile frame to the 1440 px
# desktop frame, under the same name, so every place that reads the token turns fluid
# and the 750 px step of kc-tokens.css disappears for it. Then a proposed wide step from
# 1440 to 1920 px, and layout tokens for wide screens that nothing reads yet.
ROOT_PX = 10  # html { font-size: calc(var(--font-body-scale) * 62.5%) }, body_scale 100
MOBILE_W, DESKTOP_W, WIDE_W = 393, 1440, 1920  # Figma mobile and desktop frames; wide anchor
# Proposal, not Figma: at 1920 the desktop ramp moves one body step up (18 -> 20 px), so
# every text size and line height grows by 20/18, rounded to even px. Labels, controls,
# icons and component spacing keep their desktop value: buttons and pills have fixed
# heights. Section spacing grows by the same factor, rounded to the 8 px grid.
WIDE_FACTOR = 20 / 18
WIDE_TYPE_ROLES = ("display", "h1", "h2", "h3", "h4", "h5", "h6", "body-lg", "body-md", "body-sm")
WIDE_TYPE_PROPS = ("text size", "line height")
WIDE_SPACING = "spacing/section/"
# Layout sizes, not values on a ramp: interpolating 353 -> 1376 or 361 -> 332 px means
# nothing. They keep their 750 px step; --kc-fluid-container replaces the container.
NOT_FLUID = ("size/grid/", "spacing/page/container", "size/testimonial/", "visibility/")
CONTAINER_PATH = "spacing/page/container"
GUTTER_PATH = "spacing/page/gutter"
# Reading measure for body copy (brief: no body line longer than ~75 characters). In
# Proxima Nova one ch (the width of "0") holds 1.36 average characters of running text
# (measured on the live pages, docs/utopia/data chRatio), so 50ch keeps lines near 68
# characters and 32ch near 44.
MEASURE, MEASURE_NARROW = "50ch", "32ch"

# Callers that switch type role at 750 px: one role's mobile value below, another role's
# desktop value from 750 (docs/utopia/tools/roleswap.mjs). The stepped tokens met at 750;
# fluid ones do not, so the text would jump there. Each becomes one ramp from the mobile
# role at 393 to the desktop role at 1440, then follows the desktop role (wide step).
# :root in the selector outranks the caller's own rule, which loads later in the page.
# (selector, custom property the caller sets, mobile role, desktop role, caller file:lines)
ROLE_SWAPS = [
    (".kc-mission-card", "--kc-mission-card-motto-size", "h2/text size", "h4/text size",
     "assets/mission-card.css:37/49"),
    (".kc-mission-card", "--kc-mission-card-text-size", "body-md/text size", "body-sm/text size",
     "assets/mission-card.css:39/50"),
    (".kc-mission-card", "--kc-mission-card-text-line-height", "body-md/line height", "body-sm/line height",
     "assets/mission-card.css:40/51"),
]

# Dawn's settings-driven sizes: rules that read the setting's mobile variable below 750 px
# and its desktop variable from 750 (assets/base.css:340-501, layout/theme.liquid:372-385).
# The bridge snippet restates each rule with one continuous size. A setting equal to its
# Figma role at both ends uses that --kc-responsive token, so Dawn and token text of one
# role share one ramp and the wide step. Any other setting keeps its own two values on the
# same 393 -> 1440 ramp: no change at 393 or 1440, the editor stays in charge (coordinator,
# 19 Oct: option A). The -mobile/-desktop variables themselves stay as they are: some
# callers read one of them at every width (section-product-benefits-karmicare.css:58/275,
# button-styles.liquid:16). body-small has no Figma twin; label-lg is the nearest.
# (selector, property, settings id stem, Figma role, scaled by heading_scale)
DAWN_BRIDGE = [
    ("h1, .h1", "font-size", "h1_font_size", "h1", True),
    ("h2, .h2", "font-size", "h2_font_size", "h2", True),
    ("h3, .h3", "font-size", "h3_font_size", "h3", True),
    ("h4, .h4", "font-size", "h4_font_size", "h4", True),
    ("h5, .h5", "font-size", "h5_font_size", "h5", True),
    ("h6, .h6", "font-size", "h6_font_size", "h6", True),
    (".text-xl", "font-size", "xl_font_size", "body-lg", False),
    ("body, .text-body", "font-size", "body_font_size", "body-md", False),
    (":root", "--font-body-small-size", "body_small_font_size", "label-lg", False),
]


def rem(px_value):
    return f"{fmt(px_value / ROOT_PX)}rem"


def fmt(value):
    s = f"{value:.4f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


def clamp(a, b, lo_w, hi_w):
    """a px at lo_w to b px at hi_w, held outside; Utopia's clamp(), rem-based."""
    slope = (b - a) / (hi_w - lo_w)
    intercept = a - slope * lo_w
    if intercept < 0:
        preferred = f"{fmt(slope * 100)}vw - {rem(-intercept)}"
    elif slope < 0:
        preferred = f"{rem(intercept)} - {fmt(-slope * 100)}vw"
    else:
        preferred = f"{rem(intercept)} + {fmt(slope * 100)}vw"
    return f"clamp({rem(min(a, b))}, {preferred}, {rem(max(a, b))})"


def even(px_value):
    return 2 * round(px_value / 2)


def grid8(px_value):
    return 8 * round(px_value / 8)


def emit_fluid(data, taken):
    rows = data["collections"]["responsive"]["vars"]
    fluid, wide, notes = [], [], []

    def wide_value(path, dk):
        role, _, prop = path.partition("/")
        if role in WIDE_TYPE_ROLES and prop == "text size":
            return even(dk * WIDE_FACTOR)
        if role in WIDE_TYPE_ROLES and prop == "line height":
            size_d = rows[f"{role}/text size"][0]
            return even(even(size_d * WIDE_FACTOR) * dk / size_d)
        if path.startswith(WIDE_SPACING):
            return grid8(dk * WIDE_FACTOR)
        return None

    for path, (dk, mb) in rows.items():
        if path.startswith(NOT_FLUID) or isinstance(dk, bool):
            continue
        name = f"--kc-responsive-{slug(path)}"
        if name in taken:
            if dk != mb:
                notes.append(f"{name} ({mb} -> {dk} px): defined in the theme or held at its old value")
            continue
        if dk != mb:
            fluid.append(f"  {name}: {clamp(mb, dk, MOBILE_W, DESKTOP_W)}; /* {px(mb)} @{MOBILE_W} -> {px(dk)} @{DESKTOP_W} */")
        wd = wide_value(path, dk)
        if wd is not None and wd != dk:
            wide.append(f"    {name}: {clamp(dk, wd, DESKTOP_W, WIDE_W)}; /* {px(dk)} -> {px(wd)} @{WIDE_W} */")

    container_d = rows[CONTAINER_PATH][0]
    container_w = grid8(container_d * WIDE_FACTOR)
    gutter = f"--kc-responsive-{slug(GUTTER_PATH)}"

    swaps, swaps_wide = {}, {}
    for sel, prop, mobile_role, desktop_role, where in ROLE_SWAPS:
        mb, dk = rows[mobile_role][1], rows[desktop_role][0]
        value = rem(mb) if mb == dk else clamp(mb, dk, MOBILE_W, DESKTOP_W)
        m_role, d_role = mobile_role.split("/")[0], desktop_role.split("/")[0]
        swaps.setdefault(sel, []).append(
            f"  {prop}: {value}; /* {m_role} {px(mb)} @{MOBILE_W} -> {d_role} {px(dk)} @{DESKTOP_W}; {where} */")
        swaps_wide.setdefault(sel, []).append(f"    {prop}: var(--kc-responsive-{slug(desktop_role)});")

    src = data["source"]
    generated = f"/* GENERATED from {src['file']} (Figma {src['fileKey']}), export {src['exported']}. DO NOT EDIT."
    regenerate = "   Source: docs/utopia/kc-tokens.json. Regenerate: python3 docs/utopia/generate.py"
    lines = [
        generated, regenerate,
        "   A3 prototype, docs/utopia/REPORT.md. layout/theme.liquid loads it right after kc-tokens.css,",
        "   only while the theme setting \"Fluid type (preview)\" (kc_fluid_type) is on. Off by default.",
        f"   1. Fluid ramp (Route A): every responsive pair whose mobile and desktop values differ,",
        f"      interpolated from the {MOBILE_W} px mobile frame to the {DESKTOP_W} px desktop frame and held",
        "      outside it. Same names as kc-tokens.css, so this replaces its 750px step for them.",
        f"      rem = {ROOT_PX}px (theme root 62.5% x body_scale 100), so browser text zoom still applies.",
        "   2. Layout tokens for wide screens (--kc-fluid-*): nothing reads them yet; page owners adopt.",
        "   3. Callers that switch type role at 750 px, made continuous (generate.py ROLE_SWAPS).",
        "   Dawn's settings-driven sizes: snippets/kc-fluid-bridge.liquid. Wide step: kc-fluid-wide.css.",
    ]
    lines += [f"   Not emitted: {n}" for n in notes]
    lines += ["*/", "", ":root {"] + fluid + ["}", ""]
    lines += [
        ":root {",
        f"  /* Content column: the Figma container ({px(container_d)} at {DESKTOP_W}), page gutters below it. */",
        f"  --kc-fluid-container-max: {rem(container_d)};",
        f"  --kc-fluid-container: min(100% - 2 * var({gutter}), var(--kc-fluid-container-max));",
        "  /* Reading measure for running text; use as max-inline-size on the text box. */",
        f"  --kc-fluid-measure: {MEASURE};",
        f"  --kc-fluid-measure-narrow: {MEASURE_NARROW};",
        "  /* Grid gap between cards: the Figma page gutter, fluid. */",
        f"  --kc-fluid-grid-gap: var({gutter});",
        "  /* Full-bleed media stop growing at the wide anchor and centre in the section. */",
        f"  --kc-fluid-media-max: {rem(WIDE_W)};",
        "}",
        "",
    ]
    for sel, decls in swaps.items():
        lines += [f":root {sel} {{"] + decls + ["}", ""]
    FLUID_OUT.write_text("\n".join(lines))
    print(f"wrote {FLUID_OUT.relative_to(ROOT)}: {len(fluid)} fluid, {len(ROLE_SWAPS)} role-swap, "
          f"{len(notes)} not emitted, {FLUID_OUT.stat().st_size} bytes")
    for n in notes:
        print("  not emitted:", n)

    lines = [
        generated, regenerate,
        "   A3 wide step: a proposal, not Figma (D8 option B, docs/utopia/REPORT.md). layout/theme.liquid",
        "   loads it after kc-fluid.css, only while \"Fluid type: wide screens (preview)\"",
        "   (kc_fluid_type_wide) is on as well. Off by default.",
        f"   From {DESKTOP_W} to {WIDE_W} px text sizes, line heights and section spacing grow x{fmt(WIDE_FACTOR)}, the",
        f"   content column {px(container_d)} -> {px(container_w)}. Labels, controls and component spacing keep",
        "   their desktop value. Callers made continuous in kc-fluid.css follow their desktop role.",
        "*/",
        "",
        f"@media screen and (min-width: {DESKTOP_W}px) {{",
        "  :root {",
    ]
    lines += wide
    lines += [
        f"    --kc-fluid-container-max: {clamp(container_d, container_w, DESKTOP_W, WIDE_W)}; /* {px(container_d)} -> {px(container_w)} @{WIDE_W} */",
        "  }",
    ]
    for sel, decls in swaps_wide.items():
        lines += ["", f"  :root {sel} {{"] + decls + ["  }"]
    lines += ["}", ""]
    WIDE_OUT.write_text("\n".join(lines))
    print(f"wrote {WIDE_OUT.relative_to(ROOT)}: {len(wide)} wide-step, {WIDE_OUT.stat().st_size} bytes")

    emit_bridge(rows, src)


def bridge_row(selector, prop, key, role, scaled, rows):
    dk, mb = rows[f"{role}/text size"]
    return f"{selector}|{prop}|{key}|{role}|{num(mb)}|{num(dk)}|{1 if scaled else 0}"


def emit_bridge(rows, src):
    """snippets/kc-fluid-bridge.liquid: Dawn's settings-driven sizes, continuous (DAWN_BRIDGE)."""
    table = ";".join(bridge_row(*b, rows) for b in DAWN_BRIDGE)
    start_rem, span = fmt(MOBILE_W / ROOT_PX), DESKTOP_W - MOBILE_W
    ramp = (f"clamp({{{{ low }}}}rem, {{{{ start }}}}rem + {{{{ rise }}}} * (100vw - {start_rem}rem) / {span}, "
            "{{ high }}rem)")
    lines = [
        "{%- comment -%}",
        f"  GENERATED from {src['file']} (Figma {src['fileKey']}), export {src['exported']}. DO NOT EDIT.",
        "  Source: docs/utopia/kc-tokens.json. Regenerate: python3 docs/utopia/generate.py",
        "  Dawn bridge for fluid type (A3b, docs/utopia/REPORT.md). layout/theme.liquid renders it after",
        "  base.css and kc-fluid.css, only while the theme setting kc_fluid_type is on.",
        "  Dawn sizes headings, XL, body and body-small text from theme settings: a rule reads the mobile",
        "  value below 750 px and the desktop value from 750 px (assets/base.css, layout/theme.liquid).",
        "  Each rule is restated here with one continuous size, later in the page, so it wins at every width:",
        "  - a setting equal to its Figma role at both ends (and heading_scale = body_scale) uses the",
        "    --kc-responsive token itself, so Dawn and token text of one role share one ramp;",
        f"  - any other setting keeps its own mobile and desktop values, interpolated {MOBILE_W} -> {DESKTOP_W} px",
        "    like kc-fluid.css: no change at either end, and the theme editor values still apply.",
        "  The --font-*-mobile/-desktop variables stay as set: some callers read one at every width.",
        "  Row: selector|property|setting id|Figma role|Figma mobile px|Figma desktop px|heading scale",
        "{%- endcomment -%}",
        "{%- liquid",
        f"  assign rows = '{table}' | split: ';'",
        "-%}",
        "{% style %}",
        "  {%- for row in rows -%}",
        "    {%- liquid",
        "      assign f = row | split: '|'",
        "      assign mobile_id = f[2] | append: '_mobile'",
        "      assign desktop_id = f[2] | append: '_desktop'",
        "      assign mobile = settings[mobile_id]",
        "      assign desktop = settings[desktop_id]",
        "      assign figma_mobile = f[4] | plus: 0",
        "      assign figma_desktop = f[5] | plus: 0",
        "      assign token = false",
        "      if mobile == figma_mobile and desktop == figma_desktop",
        "        if f[6] == '0' or settings.heading_scale == settings.body_scale",
        "          assign token = true",
        "        endif",
        "      endif",
        "      assign low = mobile | at_most: desktop | divided_by: 10.0",
        "      assign high = mobile | at_least: desktop | divided_by: 10.0",
        "      assign start = mobile | divided_by: 10.0",
        "      assign rise = desktop | minus: mobile",
        "    -%}",
        "    {%- if token %}",
        "  {{ f[0] }} { {{ f[1] }}: var(--kc-responsive-{{ f[3] }}-text-size); }",
        "    {%- elsif f[6] == '1' %}",
        f"  {{{{ f[0] }}}} {{ {{{{ f[1] }}}}: calc(var(--font-heading-scale) * {ramp}); }}",
        "    {%- else %}",
        f"  {{{{ f[0] }}}} {{ {{{{ f[1] }}}}: {ramp}; }}",
        "    {%- endif %}",
        "  {%- endfor %}",
        "{% endstyle %}",
        "",
    ]
    BRIDGE_OUT.write_text("\n".join(lines))
    print(f"wrote {BRIDGE_OUT.relative_to(ROOT)}: {len(DAWN_BRIDGE)} Dawn rules, {BRIDGE_OUT.stat().st_size} bytes")


if __name__ == "__main__":
    sys.exit(main())
