#!/usr/bin/env python3
"""R7-01: is the wide fluid layer continuous at any computed root? (docs/utopia/REPORT.md "R7 fix")

Exact computation: reads the generated CSS as committed, resolves each wide property the way
the cascade does with kc_fluid_type and kc_fluid_type_wide on (kc-tokens.css, its 750 px
block, kc-fluid.css, kc-fluid-wide.css with or without its media query), and evaluates the
calc()/clamp() text at a computed root R px and a viewport width w px (rem = R, vw = w/100).
  old = kc-fluid-wide.css of 01e7828 (A3b, @media min-width 1440px)
  new = kc-fluid-wide.css in the working tree (base ramp plus step, no media query)

  python3 docs/utopia/tools/r7_continuity.py bundles
      writes docs/utopia/data/r7/inject/<old|new>-root<R>.css for the browser helper: the
      fluid-on-wide bundle of that version, a computed-root override (none at 10) and probe
      rules that hand custom-property values to hidden head elements, so `metrics` can read
      them as computed font-size / line-height.
  python3 docs/utopia/tools/r7_continuity.py
      writes docs/utopia/TABLES-R7.md: exact tables, plus the helper metrics found in
      docs/utopia/data/r7/<page>-<version>-root<R>-<width>.json, each checked against the
      exact value.

Run from the repo root.
"""
import functools
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DATA = ROOT / "docs/utopia/data/r7"
OUT = ROOT / "docs/utopia/TABLES-R7.md"
OLD_REV = "01e7828"
ROOTS = (10, 12, 20)
DESKTOP_W, WIDE_W = 1440, 1920
MC = ".kc-mission-card"

# Probes: hidden head elements carry two values each into computed font-size / line-height.
PROBES = [
    ('head > meta[charset]', "--kc-responsive-h1-text-size", "--kc-responsive-h2-text-size"),
    ('head > title', "--kc-responsive-spacing-section-md", "--kc-fluid-container-max"),
    ('head > meta[name="viewport"]', "--kc-responsive-body-sm-text-size", "--kc-responsive-h6-line-height"),
]
PROBE_SELECTOR = "html, " + ", ".join(p[0] for p in PROBES)
CARD_SELECTOR = ".kc-mission-card-motto, .kc-mission-card-text"


def git_show(rev, path):
    return subprocess.run(["git", "show", f"{rev}:{path}"], cwd=ROOT, capture_output=True,
                          text=True, check=True).stdout


def declarations(css):
    """(media min-width or None, selector, name, value) for each custom property."""
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    out, stack, buf = [], [], ""
    for ch in css:
        if ch == "{":
            stack.append(" ".join(buf.split()))
            buf = ""
        elif ch == "}":
            if buf.strip():
                add(out, stack, buf)
            buf = ""
            stack.pop()
        elif ch == ";":
            add(out, stack, buf)
            buf = ""
        else:
            buf += ch
    return out


def add(out, stack, text):
    name, _, value = text.strip().partition(":")
    if not name.startswith("--"):
        return
    media = next((int(m.group(1)) for s in stack if (m := re.search(r"min-width:\s*(\d+)px", s))), None)
    selector = next((s for s in reversed(stack) if not s.startswith("@")), "")
    out.append((media, selector, name.strip(), value.strip()))


TOKEN = re.compile(r"\s*(?:(\d+\.?\d*|\.\d+)(rem|vw|px)?|var\((--[\w-]+)\)|([a-z]+)\(|([-+*/(),]))")


@functools.lru_cache(maxsize=None)
def compile_value(expr):
    """CSS calc()/clamp() text -> fn(R, w, env) in px. var(--x) evaluates env[--x] (text)."""
    toks, pos, text = [], 0, expr.strip()
    while pos < len(text):
        m = TOKEN.match(text, pos)
        if not m:
            raise ValueError(f"cannot read {text[pos:]!r} in {expr!r}")
        toks.append(m.groups())
        pos = m.end()
    toks.append((None, None, None, None, "$"))
    i = 0

    def take():
        nonlocal i
        i += 1
        return toks[i - 1]

    def atom():
        num, unit, var, fn, op = take()
        if op == "-":
            inner = atom()
            return lambda R, w, env: -inner(R, w, env)
        if op == "(":
            inner = additive()
            assert take()[4] == ")", expr
            return inner
        if num is not None:
            n = float(num)
            if unit == "rem":
                return lambda R, w, env: n * R
            if unit == "vw":
                return lambda R, w, env: n * w / 100
            return lambda R, w, env: n
        if var:
            return lambda R, w, env: compile_value(env[var])(R, w, env)
        if fn in ("calc", "clamp"):
            args = [additive()]
            while toks[i][4] == ",":
                take()
                args.append(additive())
            assert take()[4] == ")", expr
            if fn == "calc":
                return args[0]
            lo, mid, hi = args
            return lambda R, w, env: max(lo(R, w, env), min(mid(R, w, env), hi(R, w, env)))
        raise ValueError(f"unexpected {op or fn!r} in {expr!r}")

    def binary(sub, ops):
        def parse():
            left = sub()
            while toks[i][4] in ops:
                op, right = take()[4], sub()
                left = {"+": lambda a, b: lambda R, w, e: a(R, w, e) + b(R, w, e),
                        "-": lambda a, b: lambda R, w, e: a(R, w, e) - b(R, w, e),
                        "*": lambda a, b: lambda R, w, e: a(R, w, e) * b(R, w, e),
                        "/": lambda a, b: lambda R, w, e: a(R, w, e) / b(R, w, e)}[op](left, right)
            return left
        return parse

    term = binary(atom, ("*", "/"))
    additive = binary(term, ("+", "-"))
    result = additive()
    assert toks[i][4] == "$", f"trailing text in {expr!r}"
    return result


class Layer:
    """The custom properties the page gets from kc-tokens.css, kc-fluid.css and a wide file."""

    def __init__(self, wide_css):
        files = [(ROOT / "assets/kc-tokens.css").read_text(), (ROOT / "assets/kc-fluid.css").read_text()]
        if wide_css is not None:
            files.append(wide_css)
        self.decls = [d for css in files for d in declarations(css)]
        self.media = sorted({m for m, *_ in self.decls if m is not None})
        self.envs = {}

    def env(self, w, selector):
        """name -> value text at width w for :root, then :root <selector>; later rules win."""
        key = (tuple(w >= m for m in self.media), selector)
        if key not in self.envs:
            env = {}
            for scope in (":root", f":root {selector}" if selector != ":root" else None):
                for media, sel, name, value in self.decls:
                    if sel == scope and (media is None or w >= media):
                        env[name] = value
            self.envs[key] = env
        return self.envs[key]

    def value(self, name, R, w, selector=":root"):
        env = self.env(w, selector)
        return compile_value(env[name])(R, w, env)


def wide_names(css):
    seen = []
    for _, sel, name, _ in declarations(css):
        key = (sel.replace(":root", "").strip() or ":root", name)
        if key not in seen:
            seen.append(key)
    return seen


def fmt(v, digits=2):
    return f"{v:.{digits}f}"


def bundles():
    out = DATA / "inject"
    out.mkdir(parents=True, exist_ok=True)
    versions = {"old": git_show(OLD_REV, "docs/utopia/inject/fluid-on-wide.css"),
                "new": (ROOT / "docs/utopia/inject/fluid-on-wide.css").read_text()}
    for version, css in versions.items():
        for R in ROOTS:
            lines = [css, "/* R7 verification only (docs/utopia/tools/r7_continuity.py), not theme CSS. */"]
            if R != 10:
                lines.append(f"html {{ font-size: {R}px; }} /* computed root {R}px, as with a {R * 1.6:g}px browser default */")
            for sel, a, b in PROBES:
                lines.append(f"{sel} {{ font-size: var({a}); line-height: var({b}); }}")
            path = out / f"{version}-root{R}.css"
            path.write_text("\n".join(lines) + "\n")
            print(f"wrote {path.relative_to(ROOT)}")


def main():
    if sys.argv[1:] == ["bundles"]:
        return bundles()
    old_css = git_show(OLD_REV, "assets/kc-fluid-wide.css")
    new_css = (ROOT / "assets/kc-fluid-wide.css").read_text()
    layers = {"off": Layer(None), "old": Layer(old_css), "new": Layer(new_css)}
    props = wide_names(new_css)
    assert props == wide_names(old_css), "old and new wide files set different properties"

    def f(version, prop, R, w):
        sel, name = prop
        return layers[version].value(name, R, w, sel)

    md = ["# R7-01 · wide layer continuity (exact computation and helper metrics)", "",
          "Generated by `docs/utopia/tools/r7_continuity.py` from the committed CSS: `old` is",
          f"`assets/kc-fluid-wide.css` of {OLD_REV} (A3b, `@media (min-width: 1440px)`), `new` is the R7 fix",
          "(base ramp plus step, no media query), `off` is the wide setting off (kc-fluid.css on).",
          "Both settings on. Values in px; `1439.999 → 1440` is the value just below and at the old",
          "media-query width. R is the computed root font size (rem) in px.", ""]

    md += ["## 1. The review's table, recomputed", "",
           "| Root | Property | old 1439.999 → 1440 | new 1439.999 → 1440 | new at 1440·R/10 − / + | new at 1920·R/10 |",
           "|---|---|---|---|---|---|"]
    review = [((":root", "--kc-responsive-h1-text-size"), "H1"), ((":root", "--kc-responsive-h2-text-size"), "H2"),
              ((":root", "--kc-responsive-spacing-section-md"), "Section-md")]
    for R in ROOTS:
        for prop, label in review:
            start, end = DESKTOP_W * R / 10, WIDE_W * R / 10
            md.append(f"| {R}px | {label} | {fmt(f('old', prop, R, 1439.999))} → {fmt(f('old', prop, R, 1440))} | "
                      f"{fmt(f('new', prop, R, 1439.999))} → {fmt(f('new', prop, R, 1440))} | "
                      f"{fmt(f('new', prop, R, start - 0.001))} / {fmt(f('new', prop, R, start + 0.001))} | "
                      f"{fmt(f('new', prop, R, end))} |")

    md += ["", "## 2. Every wide property: largest jump", "",
           "Jump = |value(w) − value(w − 0.001 px)| at the places where a value can change course: the",
           "750 and 1440 px media queries and the scaled ends 393·R/10, 1440·R/10 and 1920·R/10.",
           "A continuous value moves at most 0.001 × its slope there (< 0.001 px).", "",
           "| Property | old R=10 | old R=12 | old R=20 | new R=10 | new R=12 | new R=20 |",
           "|---|---|---|---|---|---|---|"]
    worst = {}
    for prop in props:
        cells = []
        for version in ("old", "new"):
            for R in ROOTS:
                points = (750, DESKTOP_W, 393 * R / 10, DESKTOP_W * R / 10, WIDE_W * R / 10)
                jump = max(abs(f(version, prop, R, x) - f(version, prop, R, x - 0.001)) for x in points)
                worst[(version, R)] = max(worst.get((version, R), 0), jump)
                cells.append(f"**{fmt(jump)}**" if jump > 0.01 else fmt(jump, 4))
        label = prop[1] if prop[0] == ":root" else f"{prop[0]} {prop[1]}"
        md.append(f"| `{label}` | " + " | ".join(cells) + " |")
    md.append("| **largest** | " + " | ".join(fmt(worst[(v, R)], 4) for v in ("old", "new") for R in ROOTS) + " |")

    md += ["", "## 3. Sweep 320–3840 px, every 0.5 px", "",
           "Largest change between neighbouring widths, over all wide properties, against the largest",
           "change the steepest ramp allows in 0.5 px (container step 31.6667vw: 0.158 px). Then the",
           "largest difference from `old` at a 10px root, and from `off` up to 1440·R/10.", "",
           "| Root | old: largest 0.5 px change | new: largest 0.5 px change | new − old at R=10, all widths | new − off, w ≤ 1440·R/10 |",
           "|---|---|---|---|---|"]
    widths = [320 + 0.5 * k for k in range(int((3840 - 320) / 0.5) + 1)]
    for R in ROOTS:
        step = {"old": 0.0, "new": 0.0}
        vs_old, vs_off = 0.0, 0.0
        for prop in props:
            series = {v: [f(v, prop, R, w) for w in widths] for v in ("old", "new", "off")}
            for v in ("old", "new"):
                s = series[v]
                step[v] = max(step[v], max(abs(b - a) for a, b in zip(s, s[1:])))
            if R == 10:
                vs_old = max(vs_old, max(abs(a - b) for a, b in zip(series["new"], series["old"])))
            vs_off = max(vs_off, max(abs(a - b) for w, a, b in zip(widths, series["new"], series["off"])
                                     if w <= DESKTOP_W * R / 10))
        md.append(f"| {R}px | {fmt(step['old'], 3)} | {fmt(step['new'], 3)} | "
                  f"{fmt(vs_old, 4) if R == 10 else '–'} | {fmt(vs_off, 4)} |")

    md += ["", "## 4. 10 px root: endpoints and the old proposal", "",
           "| Property | 1440 old / new | 1920 old / new | 2560 old / new |", "|---|---|---|---|"]
    for prop in props:
        label = prop[1] if prop[0] == ":root" else f"{prop[0]} {prop[1]}"
        md.append(f"| `{label}` | " + " | ".join(
            f"{fmt(f('old', prop, 10, w), 3)} / {fmt(f('new', prop, 10, w), 3)}" for w in (1440, 1920, 2560)) + " |")

    md += helper_tables(f)
    OUT.write_text("\n".join(md) + "\n")
    print(f"wrote {OUT.relative_to(ROOT)}")
    for (v, R), j in sorted(worst.items()):
        print(f"  largest jump {v} R={R}: {j:.4f} px")


def px(value):
    return float(value[:-2])


def helper_tables(f):
    files = sorted(DATA.glob("*.json"))
    if not files:
        return ["", "## 5. Browser helper metrics", "", "No helper metrics found in docs/utopia/data/r7/."]
    md = ["", "## 5. Browser helper metrics (live pages, CSS injection)", "",
          "`python3 .orca/mission-runtime/browser.py` on the live storefront, isolated anonymous page.",
          "Injected: `docs/utopia/data/r7/inject/<version>-root<R>.css` (see `bundles` above): the fluid-on-wide",
          "bundle of that version, `html { font-size: R px }` for 12 and 20 (10 is the theme's own root), and",
          "probe rules that give hidden head elements the token values as font-size / line-height. Nothing",
          "visible is hidden. `Δ` is the largest |helper − exact| in the row, the exact value coming from",
          "the evaluator of sections 1–4 at the same root and width.", ""]
    home = [p for p in files if p.name.startswith("home-")]
    card = [p for p in files if p.name.startswith("pdp-")]
    if home:
        md += ["### Homepage probes", "",
               "| Version | Root (measured) | Width | H1 | H2 | Section-md | Container max | Body-sm | H6 line height | Δ |",
               "|---|---|---|---|---|---|---|---|---|---|"]
        for path in sorted(home, key=key):
            _, version, root, width = path.stem.split("-")
            R, w = int(root[4:]), int(width)
            data = json.loads(path.read_text())
            assert data["viewport"]["width"] == w, path
            rows = data["rows"]
            html = rows[0]
            assert html["tag"] == "HTML", path
            probe = {r["tag"]: r for r in rows[1:]}
            meta = [r for r in rows[1:] if r["tag"] == "META"]
            got = [px(meta[0]["fontSize"]), px(meta[0]["lineHeight"]), px(probe["TITLE"]["fontSize"]),
                   px(probe["TITLE"]["lineHeight"]), px(meta[1]["fontSize"]), px(meta[1]["lineHeight"])]
            names = [PROBES[0][1], PROBES[0][2], PROBES[1][1], PROBES[1][2], PROBES[2][1], PROBES[2][2]]
            exact = [f(version, (":root", n), R, w) for n in names]
            delta = max(abs(a - b) for a, b in zip(got, exact))
            md.append(f"| {version} | {html['fontSize']} | {w} | " + " | ".join(fmt(g) for g in got) + f" | {fmt(delta, 3)} |")
    if card:
        md += ["", "### Duo PDP mission card (real elements)", "",
               "| Version | Root | Width | Motto size | Text size | Text line height | Δ |", "|---|---|---|---|---|---|---|"]
        for path in sorted(card, key=key):
            _, version, root, width = path.stem.split("-")
            R, w = int(root[4:]), int(width)
            data = json.loads(path.read_text())
            assert data["viewport"]["width"] == w, path
            motto = next(r for r in data["rows"] if "Marlide" in r["fontFamily"])
            text = next(r for r in data["rows"] if "Marlide" not in r["fontFamily"])
            got = [px(motto["fontSize"]), px(text["fontSize"]), px(text["lineHeight"])]
            exact = [f(version, (MC, n), R, w) for n in
                     ("--kc-mission-card-motto-size", "--kc-mission-card-text-size", "--kc-mission-card-text-line-height")]
            delta = max(abs(a - b) for a, b in zip(got, exact))
            md.append(f"| {version} | {R}px | {w} | " + " | ".join(fmt(g) for g in got) + f" | {fmt(delta, 3)} |")
    return md


def key(path):
    _, version, root, width = path.stem.split("-")
    return (version != "old", int(root[4:]), int(width))


if __name__ == "__main__":
    main()
