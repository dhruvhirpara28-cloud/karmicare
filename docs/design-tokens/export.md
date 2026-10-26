# Exporting the KC library into the theme

`assets/kc-tokens.css` is generated. Never edit it by hand. A wrong value is fixed in Figma, then exported and regenerated.

## The two commands

1. **Export** (in a Claude session with the Figma MCP connected): read file `gcWcgYxS1nmheciKYOjOGx` (KC | Brand Design Library) with `use_figma`, read-only, and write the result to `docs/design-tokens/kc-tokens.json`. The script used on 12 Oct 2026, one call per collection because a call returns at most 20 KB:
   - `figma.variables.getLocalVariableCollectionsAsync()`, then for each variable of `mapped`, `responsive`, `shape`, `font`, `brand`: every mode's value, with each `VARIABLE_ALIAS` resolved recursively (same mode id if the target collection has it, else the mode with the same name, else the target's default mode).
   - Colours as `#rrggbb`, or `rgba(r,g,b,a)` when alpha is below 1.
   - `shape`: only `radius`, `stroke`, `opacity`, `blur`. `brand`: only `original`, `fixed`, `glass`. `getLocalEffectStylesAsync()` for the shadows.
2. **Generate**: `python3 docs/design-tokens/generate.py` from the repo root. It prints how many tokens it wrote and which names it held back.

Commit `kc-tokens.json` and `assets/kc-tokens.css` together. The JSON diff shows what changed in Figma; the CSS diff shows what changes on the site.

## Mapping rules

| Figma | CSS |
|---|---|
| `mapped/surface/page` (Day, Night) | `--kc-mapped-surface-page` on `:root, body.day-mode`, Night value on `body.night-mode`; opaque colours also get `--kc-mapped-surface-page-rgb: 255,251,246` for Dawn's `rgb(var(...))` pattern |
| `responsive/h1/text size` (desktop, mobile) | `--kc-responsive-h1-text-size`: mobile value on `:root`, desktop value inside `@media (min-width: 750px)` |
| `shape/radius/md` | `--kc-shape-radius-md: 12px`; `shape/opacity/30` becomes `0.3` |
| `font/role/backbone` | `--kc-font-role-backbone` with a fallback stack; `font/weight/*` not exported |
| `brand/original/dark blue` | `--kc-brand-original-dark-blue` (+ `-rgb`) |
| effect style `elevation/md` | `--kc-elevation-md` as a `box-shadow` value; `artwork/*` styles not exported |
| skipped | `responsive/size/testimonial/*`, `responsive/visibility/*`, the collections `alias`, `alias-tone`, `Primitives`, `backdrop` |

## Held-back names

The generator never emits a `--kc-*` name the theme already **defines** (a `--kc-x:` declaration found by `git grep` outside `docs/`). Those names keep their current source, so a regeneration can never silently restyle the Loop widget or a section. The list is printed by the script and written into the header of the CSS file. Names the theme only **reads** are emitted: that is what the file is for. (Until 13 Oct the rule also held back names that were only read; on a branch whose sections read the generated tokens, a regeneration would have dropped them.)

Moving a name into the generated file is a deliberate, separate commit: remove its hand-typed definition, regenerate, and review the visual delta. The generator refuses to run while a name it carries in the compatibility block is still hand-typed somewhere, so a name never has two sources.

## Compatibility block: held at old value, and aliases

The last block of `assets/kc-tokens.css` carries the names the theme read before they came from Figma. It is written from two maps at the top of `generate.py`:

- `HELD_AT_OLD_VALUE`: names whose Figma value would change what the site renders. Each keeps the exact value it had in `baseline/computed-before.json`, the same in Day and Night, and is a proposal for Victor in `baseline/proposals.md` (P-number in the CSS comment). A value of `None` means the name stays undefined because the theme reads it with a `var()` fallback. To accept a proposal: delete the line, regenerate, check the pages the proposal lists, commit. A held colour ships with its `-rgb` twin like every other colour (PLAN §1 guardrail 8); the triplet is computed from the held value, not from Figma, so hex and triplet always agree (`--kc-mapped-text-primary-default: #FFFBF6` and `--kc-mapped-text-primary-default-rgb: 255,251,246`).
- `COMPAT_ALIASES`: old names with no Figma path of their own, pointed at the generated token with the same meaning and value (`--kc-mapped-surface-accent-soft` → `surface/accent/default-subtle`, `--kc-white-surface-primary-default` → `brand/fixed/white`). Each alias also gets an `-rgb` alias to its target's twin (`--kc-mapped-surface-accent-soft-rgb: var(--kc-mapped-surface-accent-default-subtle-rgb)`); the generator stops if a target has no twin.

## Checking that a regeneration changes nothing visible

`capture.py computed` and `capture.py styles` record the computed token values and the computed styles of every element on the homepage, the product page and a legal page, Day and Night, 1440 and 390 px; `computed_diff.py` and `styles_diff.py` compare them with the baseline in `baseline/`. Both exit 1 on any change. The purchase smoke test is in `smoke-test.md`.
