# Brief: clock readout, make the knob → text link obvious (landing desk, 26 Oct)

Victor (26 Oct): putting the text and the label above the orb is not user-friendly either. He wants something balanced, where the UX makes it clear that the knob changes the text.

The current state is landed as landing 79 (097a6e2 + 129ac80): readout (time, state copy, hint pill) above the dial.

## The problem to solve

When you drag the dot, the eye stays on the dot and the dial. Text that changes above or below the dial, at a distance, is easy to miss, so the cause (knob) and the effect (text) feel unrelated.

## Three variants to preview (no theme commit until Victor picks)

Build them as localhost previews of the live homepage with the branch CSS and JS, like your preview at 9360. Show each at 390 and 1440, in Day and Night, in EN/NL/FR (the copy lengths differ).

1. **A · Readout inside the orb (my recommendation to test first).**
   - The time and the window's short name (e.g. "07:30 · Morning activation") sit centred inside the dial/orb, and update live while dragging, like a watch face.
   - The longer explanation goes directly **under** the dial, with its height reserved (no jump) and a short crossfade on change.
   - The "Drag the dot" pill sits right under the dial, close to where the dot starts, and fades out after the first drag.
   - Check contrast of text over the orb and sun glow in Day and Night (4.5:1 for small text, 3:1 for large). Reduced motion means no crossfade.
2. **B · Label that travels with the dot.**
   - A small time badge rides along next to the dot while dragging, showing the time.
   - The explanation sits under the dial, height reserved.
   - The pill sits under the dial.
   - It must not clip at the dial's edge on 360px phones.
3. **C · The previous layout, with a visual link.**
   - The readout goes back under the dial, as before 097a6e2.
   - It is visibly tied to the dot: a thin connector or highlight, the copy block briefly highlighting on change, and the pill directly under the dial.

For each variant:
- one screenshot at rest and one mid-drag;
- the layout-shift check (the dial must not move while dragging);
- a note on touch: a swipe over the dial still scrolls the page (R91).

Write a short comparison in `docs/homepage/CLOCK-READOUT-OPTIONS.md` with pros, cons and your recommendation. Then show Victor here, with the preview URLs.

## The PDP footer line

Victor's answer was "PDP regel ook wel onder de klok". I am confirming with him whether that means remove it on the PDP too. Wait for my message before changing `templates/product.subscription-item.json`.

## Rules

- Same as before. Keep files in this worktree, never in `/private/tmp`.
- Build the chosen variant only after Victor's yes. Then: pathspec commit, Theme Check, merge_ready.
- No push.
