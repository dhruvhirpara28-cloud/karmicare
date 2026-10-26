# Note from the landing desk: global colour and font token changes (26 Oct)

The soft-launch global lane ("Karmicare global elements lane") is changing `assets/kc-tokens.css`. Victor wants this; the change is not landed yet. That lane's session starts in `karmicare-soft-launch-global`, but it edits the theme in its build worktree `global-klaviyo-on`. That folder name is historical: this has nothing to do with Klaviyo.

## The changes

- **Text colour is solid instead of transparent.** This follows the crispness report: the alpha made the text look soft.
  - Day: `--kc-mapped-text-default-body` and `--kc-mapped-text-default-caption` go from navy `rgba(25,31,56,0.76)` to solid `#191f38`. New `-rgb` companions are `25,31,56`.
  - Night: both go from cream `rgba(255,251,246,0.68)` to solid `#fffbf6` (`255,251,246`).
  - The placeholder colour keeps its alpha.
- **Font stack order.** `proxima-nova` (the Typekit name) now comes first in `--kc-font-role-backbone` and `--kc-font-use-heading/body/ui`.
- **Possible follow-ups from the crispness report.** These still wait for Victor's yes:
  - removing the unused Montserrat preloads and the Gotham TTF;
  - antialiased smoothing in Day.

## What this means for the blog

1. **Use the tokens, never literal colours.** Take body and secondary text from `--kc-mapped-text-default-body` and `-caption`, never from a hard-coded alpha. Check your CSS and fixture for literal `rgba(25,31,56,…)`, `rgba(255,251,246,…)` or "68%/76% of the heading colour" values. That includes the long-form body you took from `kc-policy-page.css`.
2. **Set font families through the `--kc-font-use-*` tokens.** Never name a font directly.
3. **Preview both states.** Show the previews in the current state and with the new values: add the new token values as an override in the fixture. Note any place where solid body text changes the hierarchy, for example meta rows or captions that relied on being softer. If something needs a deliberately softer tone, propose a token for it rather than a literal.
4. **Order of landing.** If the token change lands before the blog, you inherit it for free. If the blog lands first, it must not lock in the old alpha values.

No reply is needed unless something in your proposal changes. Mention it in your report to Victor.
