# Clock readout options (homepage lane, 26 Oct)

Brief: `docs/homepage/BRIEF-CLOCK-READOUT-UX.md`. Victor finds the readout above the orb (landed 097a6e2) not user-friendly. He wants a balanced layout where it is obvious that the knob changes the text.

He asked for A and C, skipped B, and then chose a new **D**: the time and the explanation inside the orb, without a panel.

## Previews

Local copies of the live homepage with the branch's clock CSS and JS. The readout is moved by `preview-clock/variants.js`. Served from `docs/homepage/preview-clock` on port 9360.

| Variant | EN | NL | FR |
|---|---|---|---|
| D (with a soft veil) | http://127.0.0.1:9360/index.html?variant=d&veil#klok | http://127.0.0.1:9360/index-nl.html?variant=d&veil#klok | http://127.0.0.1:9360/index-fr.html?variant=d&veil#klok |
| D without a veil | `?variant=d` | | |
| A | `?variant=a` | | |
| C | `?variant=c` | | |

The bar at the bottom of each page switches variants. **Opnieuw afspelen** replays the knob arrival.

Shots are local and gitignored:
- `docs/homepage/shots/clock-variant-d/` holds D with the veil: EN, NL and FR at 390 and 1440, Day and Night, each at rest and mid-drag (07:30).
- `docs/homepage/shots/clock-variants/` holds A and C at 390, Day and Night, EN only. That run was stopped when Victor chose D.

## D: time and explanation inside the orb

The real `.time-line` and `.state-copy` elements move into a block centred on the orb. The clock script keeps updating them and reserves the copy's height there.

The Awake and Asleep words on the orb are hidden, because they would sit on the time and the copy. The pill stays under the dial.

**Contrast, measured on real pixels.** `preview-clock/contrast-sample.py` makes the text transparent, captures the frame, and compares every orb pixel under each text line with the text colour #191f38. It uses the longest window message per language.

| Setting | Small text (needs 4.5:1), worst | Time (large, needs 3:1), worst |
|---|---|---|
| No panel, no shadow | 1.96 (FR 360 Night) to 6.7 | 8.8 or more everywhere |
| Light text halo only | 2.6 to 5.0, fails on phones and at Night | 8.8 or more |
| Halo plus a soft radial veil behind the text (fades out, no edge) | **4.68 (FR 1440 Night) to 7.6**, passes everywhere | 9.3 or more |

The lower lines of the long explanations reach the dark base of the orb. In both modes the orb is the same light-top, dark-base artwork. Without help those lines fail, so D only passes with the veil.

**Fit at 360.** The block is 138 × 143 px with FR window 7, the longest message at 157 characters. Its corners sit at 0.96 of the orb's radius, so nothing clips. The text is 11 px on phones and 13 px at 1440.

**No shift.** In every combination of EN/NL/FR × 390/1440 × Day/Night (12), the dial top stayed on the same pixel while dragging through all seven windows. There was no horizontal overflow.

**Touch.** The orb text has `pointer-events: none`, and only the knob holds the touch (R91). A swipe over the dial therefore still scrolls. The Orca browser has no touch input, so this needs a phone check.

## A and C (for the record)

- **A** puts the time and the caption in a frosted page-colour disc inside the orb (8.9:1 worst case), with the explanation under the dial. It reads clearly, but Victor does not want the panel.
- **C** puts the readout back under the dial, with an accent connector line, an accent dot on the time, and a flash on change. It has no contrast issues, but the text is still away from where the eye is while dragging.

## Knob arrival (Victor, 26 Oct, in the D preview)

The change is uncommitted, in `assets/chronobiology-clock-karmicare.js`.

- **Before the run:** the knob waits hidden, two hours early.
- **Run:** once 15% of the section is in view, it runs to now in **2.4 s**, easing in and out. Over the first half it fades from 0 to 1. Its icon turns 360° on its own axis.
- **After landing:** the halo pulses until the knob is taken.
- **Unchanged:** drag or arrow keys cancel the run, the readout stays live, it plays once per visit, and with reduced motion the knob shows on now with no motion.

Measured at 390, 16:27 → 18:27:

| Time | Knob opacity | Icon rotation |
|---|---|---|
| 0.7 s | 0.56 | 32° |
| 1.65 s | 1 | 332° |
| 2.6 s | landed, halo on | |

On a phone, 15% of this tall section shows before the dial does. A visitor who stops at the heading misses most of the run; one who keeps scrolling meets the dial while the knob is moving. Starting on the dial itself (for example 10% of `.dial`) would guarantee it is seen.

## Recommendation

- **Layout:** D with the soft veil. It is Victor's choice, and it is the only form of D that meets 4.5:1 for the explanation.
- **Arrival:** 2.4 s, with the start tied to the dial rather than the section on phones.
- **Before building:** wait for Victor's yes on D with the veil, and on the trigger.
