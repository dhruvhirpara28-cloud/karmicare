# Rework for R90: blog layout (from the landing desk, 26 Oct)

Astra's report is `docs/runtime-review/R90-BLOG-LAYOUT-ASTRA.md`. The verdict is REWORK, with three blockers.

## Blockers

1. **B1: wide body images are clipped.**
   - **Cause:** the paragraph reset `.kc-blog__body :is(p, ul, ol, blockquote, table, div[style])` has specificity 0,2,1 (because of `div[style]`). With `!important` it beats the breakout margins on `p:has(img)`. The image starts at the text column and is clipped on the right by `overflow-x: clip` (20px at 360).
   - **Fix:** fix the cascade, for example a lower-specificity reset (`:where()`) or a matching specificity for the breakout. Do not hide the overflow. Verify the actual left and right edges at 360, 390, 750, 990 and 1440, not only the document width.
2. **B2: body images shift the layout while loading.**
   - **Cause:** the body transformation adds lazy loading and new URLs, but no `width`/`height` or aspect ratio.
   - **Fix:** reserve space from the source image's real dimensions. Shopify CDN image URLs and `image_url`/`image_tag` can give you these when you resolve them, or read them where available. Then the contents script needs no corrective scrolling.
3. **B3: six `h1`s in the nano article.**
   - **Fix:** normalise in the renderer. Keep the article title as the only `h1`, and demote the body headings by one level (body h1 → h2, h2 → h3 and so on, capped at h4).
   - Keep the wording. Update the contents discovery so "On this page" still lists the sections.
   - Check with and without JS.

## Also, in the same round if cheap

- **N1:** a responsive rule for embeds such as iframes (aspect-ratio box, max-width 100%), and don't stretch small images beyond their natural size.
- **N2:** after a contents jump, move focus to the target heading (`tabindex="-1"` plus `focus({preventScroll:true})`).

## Then

Make pathspec commits, run Theme Check, rerun the targeted checks for B1–B3, and send merge_ready `NEEDS REVIEW: blog layout R90b over 14d2590..<head>`.

The landing order still holds: the blog lands after the global text-token change.

No push.
