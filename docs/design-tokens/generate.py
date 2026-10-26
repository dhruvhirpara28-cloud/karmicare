#!/usr/bin/env python3
"""Generate assets/kc-tokens.css from docs/design-tokens/kc-tokens.json.

Run from the repo root:  python3 docs/design-tokens/generate.py
Never edit assets/kc-tokens.css by hand: fix the value in Figma, re-export
kc-tokens.json (see export.md), run this script, commit both files.

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
SRC = ROOT / "docs/design-tokens/kc-tokens.json"
OUT = ROOT / "assets/kc-tokens.css"
BREAKPOINT = "750px"  # Dawn's own breakpoint, mirrors Figma desktop/mobile (D8)

FONT_STACKS = {
    # The Adobe Fonts kit family first, so a locally installed "Proxima Nova" (another build)
    # never takes over from the web font (Victor, 26 Oct; docs/global-type/CRISPNESS-REPORT.md)
    "Proxima Nova": '"proxima-nova", "Proxima Nova", sans-serif',
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
    # P12/P13: capitals in Nunito read calmer with about 0.08em of tracking (was 1.25px / 1.7px;
    # Victor, 26 Oct, docs/global-type/CRISPNESS-REPORT.md)
    "--kc-responsive-caption-letter-spacing": ("0.8px", "P12"),  # Figma 1.7px | 1.2px
    "--kc-responsive-Nunito-letter-spacing": ("1px", "P13"),  # no Figma path; caption is 1.7px | 1.2px
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
    """Every --kc-* name declared (`--kc-x:`) in tracked theme files."""
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


if __name__ == "__main__":
    sys.exit(main())
