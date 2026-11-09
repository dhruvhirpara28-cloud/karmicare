# Kim Verlot quote · EN and FR transcreation

**Approved** by Victor on 8 Nov 2026 in the source-copy session: "ik keur EN en FR goed". His brief: translate as well as possible, not literally, so that it reads fluently in each language.

Kim wrote the quote in Dutch. The Dutch stays exactly as she wrote it. The current live EN (`0c2979d`, 29 Oct) is a literal translation; it is replaced by the EN below.

## Texts

| | Text |
|---|---|
| NL (Kim's original) | Mijn bioritme ondersteunen is voor mij belangrijk. Tandenpoetsen met Karmicare past in mijn dagelijks ritueel om mijn zenuwstelsel te helpen schakelen tussen dag en nacht. Daarnaast ervaar ik dat het me enorm helpt mijn teruggetrokken tandvlees onder controle te houden. |
| EN (new) | Living in sync with my biorhythm matters to me. Brushing with Karmicare is part of the daily ritual that helps my nervous system switch between day and night. I also find it makes a huge difference in keeping my receding gums in check. |
| FR (new) | Respecter mon biorythme me tient à cœur. Me brosser les dents avec Karmicare fait partie du rituel quotidien qui aide mon système nerveux à basculer entre le jour et la nuit. Je constate aussi que cela m’aide énormément à contenir le recul de mes gencives. |
| EN (old, live) | Supporting my biorhythm is important to me. Brushing my teeth with Karmicare fits into my daily ritual to help my nervous system transition between day and night. I also find that it helps me enormously to keep my receding gums under control. |
| FR (old, never registered) | Soutenir mon biorythme est important pour moi. Me brosser les dents avec Karmicare s’inscrit dans mon rituel quotidien pour aider mon système nerveux à passer du jour à la nuit et inversement. Je constate également que cela m’aide énormément à garder ma récession gingivale sous contrôle. |

Choices, against the Dutch:
- "ondersteunen" → "living in sync with", "me tient à cœur": reads as people say it, not as "supporting" or "soutenir".
- "schakelen" → "switch", "basculer": keeps the image of switching over.
- As in the Dutch, it is the ritual that helps, not a direct product claim.
- "teruggetrokken tandvlees onder controle" → "receding gums in check", "contenir le recul de mes gencives": everyday words; "récession gingivale" read as clinical.
- No colons, semicolons or dashes, no new claims, nothing softened.

## Values for the theme and the payloads

Same markup as the other professional cards: `<p>“…”</p>`, curly quotes in all three languages.

| Field | Value |
|---|---|
| `templates/index.json` and `templates/product.subscription-item.json` · `sections.trusted_professionals_HAqYth.blocks.card_qAPajg.settings.hover_text` | `<p>“Living in sync with my biorhythm matters to me. Brushing with Karmicare is part of the daily ritual that helps my nervous system switch between day and night. I also find it makes a huge difference in keeping my receding gums in check.”</p>` |
| new EN sha1 | `6ca4ebace868a0d0bfc7e28f5b92f2b86eba59e0` (live EN now `622a488d7104dc54f5e67bf9032e7c04697514d5`) |
| NL | `<p>“Mijn bioritme ondersteunen is voor mij belangrijk. Tandenpoetsen met Karmicare past in mijn dagelijks ritueel om mijn zenuwstelsel te helpen schakelen tussen dag en nacht. Daarnaast ervaar ik dat het me enorm helpt mijn teruggetrokken tandvlees onder controle te houden.”</p>` |
| FR | `<p>“Respecter mon biorythme me tient à cœur. Me brosser les dents avec Karmicare fait partie du rituel quotidien qui aide mon système nerveux à basculer entre le jour et la nuit. Je constate aussi que cela m’aide énormément à contenir le recul de mes gencives.”</p>` |

## Steps

1. **EN in the theme**: done. On 9 Nov the new EN is live on the homepage and the PDP (www.karmicare.com, Orca same-origin fetch) and on local main (merchant-edit `83d060e`); sha1 matches.
2. **Claims approved** by Victor on 9 Nov 2026 in the source-copy session: "de claims zijn goedgekeurd". This covers "help my nervous system switch between day and night" and "keeping my receding gums in check" (and their NL/FR), flagged in the 29 Oct handoff (`kim-verlot` `81d3a59`, REPORT.md). So no hold.
3. **Source-copy** (9 Nov, after the 6 Nov write): the two EN rows are in `en-source.json` and batches 01/02, NL and FR in the payloads, plans rebuilt (`live/tools/apply_kim_kris_rating.py`). The same round carries Kris's title (`REQUEST-2026-11-02-kris-title.md`).
4. Next: dry run, desk review, Victor writes, check /nl and /fr on www.karmicare.com.
