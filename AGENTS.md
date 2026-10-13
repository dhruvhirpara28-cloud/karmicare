# Rules for agents in this repo

These rules bind every coding agent (Claude Code, Codex, any other) working in this repo. `CLAUDE.md` imports this file, so both read the same text. Start with `README.md` for what the theme is, the branches and how to preview. If your task comes with a runbook (for example `docs/pdp/RUNBOOK.md`), its limits apply as well as these.

## 1. No pushes, no admin writes

- No `git push`, no pull requests, no merges into `main` or `DH/Development`. Commit on your own branch only. Victor pushes; DH ships `main` to the live theme.
- No Shopify admin writes of any kind: products, metafields, discounts, theme settings, Loop admin, Files.
- Never run `shopify theme push`, `publish`, `delete` or `share` unless Victor asks for it in your session. Preview with `shopify theme dev` on your own unpublished dev theme (see `README.md`).
- No payment details anywhere. Never type into Shopify checkout.

## 2. Off-limits files

Do not edit these unless your task names them:

- `config/settings_data.json`: the settings saved from the theme editor.
- The Loop subscription widget: `assets/loop-widget.js`, `assets/loop-widget.css`, `snippets/loop-widget*.liquid`. The purchase flow runs through them.

## 3. Brand rules for customer-facing copy

Verbatim from `docs/pdp/RUNBOOK.md` §1 rule 7:

> **Brand rules**: Awake before Asleep; no commodity words in customer copy beyond first mention ("toothpaste" once, never "product/tube/buy/use"); Care Credit in €, never "discount" or "cashback"; EU cosmetic claim wording only ("helps", "supports"), never "cures/treats/prevents".

Copy comes only from the Figma frames or from text already in the repo or on the site. No new claims, numbers, studies, quotes or testimonials (`docs/pdp/RUNBOOK.md` §1 rule 4). If something needs copy that does not exist yet, stop and report it as blocked.

## 4. Design token contract

Full rules: `docs/design-tokens/PLAN.md` §1.

- **Names**: `--kc-<collection>-<path>`, with each `/` in the Figma path turned into `-` (spaces too). Example: `--kc-mapped-surface-accent-default`.
- **Colours ship twice**: a hex value and an `-rgb` triplet, for Dawn's `rgb(var(...))` pattern.
- **`assets/kc-tokens.css` is generated. Never edit it by hand.** Fix the value in Figma, re-export `docs/design-tokens/kc-tokens.json` (see `docs/design-tokens/export.md`), run `python3 docs/design-tokens/generate.py` from the repo root, and commit both files.
- **`--kc-mapped-*` names read by the Loop widget are a contract.** Keep each one defined with the same meaning. Today `snippets/loop-widget.css.liquid` reads these eight: `--kc-mapped-bg-primary-default`, `--kc-mapped-border-focus-default`, `--kc-mapped-surface-accent-default`, `--kc-mapped-surface-primary-default`, `--kc-mapped-surface-secondary-default`, `--kc-mapped-surface-tertiery-default` (the misspelling is part of the contract), `--kc-mapped-text-accent-default`, `--kc-mapped-text-primary-default`. Re-check with `grep -ohE 'var\(--kc-mapped-[a-z0-9-]+' assets/loop-widget.* snippets/loop-widget*.liquid | sort | uniq -c`.
- Never remove a `--kc-*` name that any file still reads.

## 5. Theme Check must not add errors

Run this from the repo root before every commit that touches theme files:

```sh
shopify theme check --fail-level error
```

It must exit 0. `.theme-check.yml` holds a baseline for the errors that already existed (19 `MatchingTranslations` in schema locales, 1 `MissingTemplate`), so any error it reports is new. Fix it. Do not add a new ignore to `.theme-check.yml` to hide it. When you fix a baselined error, delete its line from `.theme-check.yml`. Warnings are reported but do not fail the run. The same check runs on every pull request (`.github/workflows/theme-check.yml`).
