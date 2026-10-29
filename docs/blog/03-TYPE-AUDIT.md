# Blog lane · 03 · Type audit: blog D against the tokens and the site

Victor (26 Oct): "make sure you use font sizes from our tokens so it is consistent throughout the website; if they differ now, show the differences first". Nothing has been changed for this yet. This page shows the differences and the options.

**How it was measured:** `fixture/tools/type_audit.py` runs `probe-type.js` on the blog fixture (direction D), the live article, the live homepage and the live legal page (`/pages/terms-and-conditions-1`) at 390 and 1440 px. For every text role it reads the rendered size and line height and lists every token in `assets/kc-tokens.css` (`--kc-responsive-*`), or theme font variable, that has exactly that value on that page. Raw output: `fixture/data/type-audit.json`.

## 1. Sizes: every blog size is a token value

| Role | Blog D 390 / 1440 | Token (390 / 1440) | Same role elsewhere on the site |
|---|---|---|---|
| Eyebrow ("NEWS") | 12 / 14 Nunito 700 | label-sm / label-lg (via the theme's `--font-body-small-size`) | homepage eyebrows: **identical** |
| Title | 32 / 52 | h1 | live article title: identical |
| Standfirst | 18 / 20 | body-lg | — |
| Date, reading time | 13 / 14 | label-lg | — |
| **Body text** | **18 / 18** | **body-lg on phones, body-md from 750** (two tokens) | homepage and legal body: **14 / 18** (theme settings `--font-body-size-mobile` and `--size-xl-desktop`, not a token pair). The token pair for body text is **body-md 16 / 18** |
| **Section heading in the article** | **24 / 28** | **h3 on phones, h4 from 750** (two tokens) | homepage section headings: **28 / 44** (h2). Legal clause titles: **20 / 24** (h5) |
| Sub-heading | 20 / 24 | h5 | legal clause titles: identical |
| Sources heading, Keep reading row titles | 20 / 24 | h5 | — |
| **"Keep reading" heading** | **24 / 36** | h3 | homepage section headings: **28 / 44** (h2) |
| Sources link titles | 16 / 18 | body-md | — |
| Contents eyebrow and links | 12 / 14 Nunito 700 | label-sm / label-lg | legal pages: **identical** |
| Button (end CTA) | 12 / 14 Nunito 700 | label-sm / label-lg | homepage: identical (the same section) |

## 2. Line heights: three blog values have no token

| Role | Blog D | Token for that size | Site today |
|---|---|---|---|
| Title | 1.16 (37 / 60 px) | h1 lh: 36 / 52 px (1.13 / 1.0) | live title 1.10 (Dawn) |
| Standfirst | 1.6 | body-lg lh: 26 / 28 px (1.44 / 1.4) | — |
| Body text | **meant to be 1.6 (D22), but the nano article renders `normal`**: Dawn's `base.css` sets `p, li { line-height: normal }`, which beats the value on the wrapper. The seven 2024 articles do get 1.6 (their inline styles go through the blog's `[style]` reset). **A bug, not yet fixed** | body-lg lh 26 / 28; body-md lh 24 / 24 | homepage and legal: `normal` |
| Section heading | 1.3 | h3 lh 28 (1.17), h4 lh 32 (1.14) | homepage h2 1.10 (Dawn) |
| Sub-heading, row titles, Sources heading | token (h5 lh 24 / 28) | — | legal clause title: identical |
| "Keep reading" heading | token (h3 lh 28 / 36) | — | — |

## 3. What would make it fully token-consistent

| # | Change | Options | Recommendation |
|---|---|---|---|
| T1 | Body text size | **a.** body-md token pair 16 / 18 · **b.** body-lg pair 18 / 20 · **c.** the site's 14 / 18 (theme setting, not a token pair) · **d.** keep 18 / 18 (two tokens) | **a. body-md 16 / 18.** It is the token pair for body text and matches the homepage and legal pages from 750 px. On phones it is 2 px larger than the site's 14 px, which is not a token pair. That is a site-wide point for another lane |
| T2 | Section heading in the article | **a.** h3 pair 24 / 36 · **b.** h4 pair 20 / 28 (on phones the same size as the sub-heading h5, 20 px) · **c.** keep 24 / 28 (h3 then h4) | **a. h3 24 / 36**: one token pair, and a clear step above the sub-heading (h5 20 / 24) at both widths. "Keep reading" is already h3, so section headings and "Keep reading" match |
| T3 | Line heights | **a.** the tokens' own line heights everywhere (title h1 lh, headings h3 lh, standfirst and body body-lg/md lh) · **b.** keep the reference's 1.16 / 1.3 / 1.6 and add them to the KC library as tokens (D22) | **a for title and headings, b for body text and standfirst.** The airy 1.6 body line is what the reference is about, and no token gives it, so it should become a long-form line-height token in the library |
| T4 | The nano body line-height bug | fix whichever T3 answer: the line height set on `p` and `li` inside the blog body, not only on the wrapper | **Fix** |
| T5 | Off-token values elsewhere on the site (not this lane) | homepage, legal and the current article print body text at 14 px on phones (theme setting) and headings at Dawn's 1.10 line height | **Note for the landing desk** |
