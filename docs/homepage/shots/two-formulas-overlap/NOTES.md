# Two formulas: tubes over the feature headings (Victor, 25 Oct)

Victor's phone shot: `docs/two-formulas-mobile-overlap-victor-2026-10-25.png` (NL, iOS). The tubes cover "'s Morgens…" and "'s Nachts…".

## Cause

The duo file `kc-two-formulas-duo.png` is 1600 × 1956. Its opaque tubes span rows 145 to 1763, measured from the alpha channel. Below 990 the file is drawn 449 px wide and 549 px high. With its −0.09 / −0.07 margins, it takes about 477 px. Below 1080 its box is `aspect-ratio: 1 / 1` with a 360 px cap.

- **Chromium** grows the square box to the picture's height (automatic minimum size), so nothing overlaps.
- **iOS Safari** keeps the box square, so the picture spills out about 58 px at the top and the bottom. The headings then start about 25 px above the tube base, which matches Victor's shot.

## Fix

`assets/section-two-formulas-karmicare.css`: below 990, where the section stacks, `.two-formulas__image-wrap { aspect-ratio: auto }`. The box takes the picture's height in every engine. From 990 (side by side) nothing changes.

## Evidence (live www.karmicare.com, Orca Chromium tab, 26 Oct)

Measured with `docs/homepage/capture/two-formulas-shots.py`; raw rows are in `docs/homepage/capture/two-formulas-shots.log`. The `gap` columns are in CSS px.

| Shot | Box height | Tube base → heading | Header → tube top |
|---|---|---|---|
| 360 Day EN, live (`…-before.png`) | 476.9 | +32.7 | +30.3 |
| 360 Day EN, live + fix | 477.0 | +32.7 | +30.3 |
| 360 Day EN, live with the box held square (`…-square.png`, Safari emulation) | 330 | −40.7 | −43.2 |

- **With the fix:** in Chromium the layout is the same as live, so the change is a no-op there. Its shot is missing because the page jumped to the top before the frame.
- **Square emulation:** it reproduces Victor's overlap.
- **Not captured:** the full matrix (360–1080, Day/Night, EN/NL/FR). On 26 Oct, after the Mac restart, Orca closed four tabs in a row in the middle of the run, so the landing desk said to stop retrying. Astra checks the iOS-like behaviour in review.
