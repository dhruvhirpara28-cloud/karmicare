# Brief: practitioner form moves to a professionals page (v1)

**Created**: 2026-10-26 · from the landing desk to the practitioner-form lane

## Victor's ask (26 Oct, verbatim)

"I think we should direct all entry links to the professional page and simply have the form there for v1 before we build out the whole professional page. PDP should stay clean for quick high conversion"

## Goal

- **PDP:** no form and no dialog. The PDP keeps only plain links that go to the professionals page.
- **Professionals page v1:** a short intro plus the existing request form, inline: the same fields, the same Klaviyo event, the same inbox mail. The full professionals page (Figma page `3810:3`) comes later. v1 must not block it.
- **Entry links:** every place that opens the form today, or talks about the evidence pack, samples or professionals, links to that page. In NL and FR the links keep their language (`/nl/...`, `/fr/...`).

## Phase 1: audit and proposal (no code)

1. **Entry links.** List every entry point, at least:
   - the PDP FAQ kPNI answer ("evidence pack");
   - the "For dentists" section-content link (`a.rda-link`);
   - anything on the homepage, footer, header or other templates that mentions professionals, practitioners, the evidence pack or samples.

   For each one, record the template, section and setting, and the current URL and text.
2. **The page.** Check in an anonymous browser whether the live store already has a professionals page, and under which handle (`/pages/professionals` returns 404 via curl). Propose the handle and a template `templates/page.professionals.json` with one section.
   - Victor creates the page in the Admin himself. That is a store write, so you write the exact steps for him.
   - Until the page exists, the links must not break: build them from the page object, with a fallback, the same way the footer's withdrawal link works.
3. **Settings and translations.** Map out how the form moves:
   - the `request_*` settings move from `product_faq_block` in both product templates to the new page section;
   - say which keys source-copy then translates. Source-copy is on hold for these keys;
   - say what can be removed from the product templates and the PDP assets. `kc-practitioner-request.js` and `.css` must no longer load on the PDP.
4. **"Opened from".** Without the dialog, how does the request still say where it came from? For example a `?from=pdp-faq-kpni` parameter on the link, read on the page and sent as the hidden field and as Klaviyo `opened_from`. No personal data in the URL.
5. **Preview.** Build a localhost preview of v1 on KC tokens:
   - in the same family as the legal and policy pages (`assets/kc-policy-page.css`);
   - at 390 and 1440, in Day and Night;
   - plus the PDP before and after, at the FAQ.
6. **Report.** Write `docs/pdp/practitioner-form/PROFESSIONALS-V1-PROPOSAL.md` with the decisions for Victor in words, each with your recommendation. Tell Victor in your terminal and send the landing desk `status` "Practitioner: professionals page v1 proposal ready".

## Phase 2: build (only after Victor's yes)

- **Build:** the page template and section, the PDP clean-up, and the link changes. Make pathspec commits.
- **Checks:**
  - Theme Check: 0 errors, baseline 19 warnings;
  - all fixture suites green: success, error, no-JS, Klaviyo abort, NL/FR, long labels;
  - the PDP renders without the form, and the PDP purchase controls and the Loop widget are untouched.
- **Merge-ready:** send `merge_ready` "NEEDS REVIEW: professionals page v1 over <base>..<head>".

## Notes

- **Your fixture harness is gone.** The reboot wiped your scratchpad (`render.mjs`, the saved live PDP DOM, the suites). Rebuild it **inside this worktree**: under `docs/pdp/practitioner-form/fixture/`, or in a gitignored folder. Never in `/private/tmp` again.
- **Merge `karmicare/soft-launch` first.** It is now at 9a34a45, which includes your R76h.

## Rules (unchanged)

- No subagents. No push.
- No reset, amend, rebase or stash. Never merge merchant-edit or main into your branch.
- Never touch `config/settings_data.json`, `snippets/loop-widget-standard.liquid`, `assets/loop-widget.js` or `locales/*`.
- No store or Admin writes and no Klaviyo changes. Victor does those.
- Only theme files ever land. Your docs and fixture stay in `docs/`.
