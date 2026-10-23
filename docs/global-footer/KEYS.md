# Footer newsletter → Klaviyo: locale keys for the source-copy lane

**Created**: 2026-10-23 · global-footer worker. Theme Check (`TranslationKeyExists`) fails on a key the theme reads but `en.default.json` lacks, so the two **new** keys were added the repo way in the build commit: rows in `docs/localization/theme-keys.json` (area `footer`, `nl`/`fr` null with a `*_hold`) and `python3 docs/localization/theme_keys.py write --area footer`, which put the EN text in all 31 storefront locales, as the clock lane did for `kc.clock.help` (e1411e2). Left for the lanes through this file: the NL and FR values of those two keys, and the **changed** `kc.footer.consent_html` (EN, NL, FR together, so `/nl` and `/fr` never show a half-English footer).

Victor's decisions (23 Oct, "ja op alles"): D4 = the new consent text (a), replacing the terms bundling.

## Keys

| Key | Where it is read | EN |
|-----|------------------|----|
| `kc.footer.consent_html` (changed) | `sections/footer.liquid`, the note under the form, `id="FooterNewsletterEmail-note"` | Occasional emails from KARMICARE about Awake & Asleep, the Dental Check-up Reward and member offers. Unsubscribe any time with the link in every email. `<a>Privacy Policy</a>`. |
| `kc.footer.check_inbox` (new) | `data-msg-success` on `#FooterNewsletter`; shown in the `role="status"` region after Klaviyo answers 202 | Check your inbox to confirm your subscription. |
| `kc.footer.email_invalid` (new) | `data-msg-invalid` on `#FooterNewsletter`; shown in the `role="alert"` region when Klaviyo rejects the address (4xx) | Check the email address. |

For the source-copy lane: the two new rows carry `ids: []` and the tool's own hold `not in the B1a inventory [NEEDS APPROVED COPY]`, so `theme_keys.py check` passes while the inventory catches up. To close the loop: inventory them as `locale:kc.footer.check_inbox` and `locale:kc.footer.email_invalid` in `docs/source-copy/en-source.json` and the batch file (sha1 = sha1(en), status approved, Victor 23 Oct), add the NL and FR payload entries, put the ids on the rows and run `refresh` + `write`.

Notes for the writer:
- `kc.footer.consent_html` keeps one `<a>` only: `href="{{ privacy_url }}"`. The theme still passes `terms_url` to the `t` filter, so an older translation with two links keeps working until it is replaced. Drop `terms_url` from `href` in the map row.
- The two new strings are placed in HTML attributes (escaped by Liquid): plain text, no tags.
- Brand rules checked: Awake before Asleep; no commodity words; no claims; Care Credit not mentioned. The notice names who sends (KARMICARE), what (news about the kit, the Check-up Reward, member offers), that unsubscribing is possible any time, and links the privacy policy; it no longer says "you agree to the Terms".
- Shorter EN variant if the column is tight (Victor's call): "Occasional emails from KARMICARE: Awake & Asleep news, the Check-up Reward, member offers. Unsubscribe any time. <a>Privacy Policy</a>."
- When the consent text changes again, bump `data-consent-version` in `sections/footer.liquid` (now `footer-2026-10`): Klaviyo stores it per profile as `consent_text_version`.

## Rows in the shape of `docs/localization/theme-keys.json`

```json
{
 "key": "kc.footer.consent_html",
 "area": "footer",
 "ids": ["liquid:sections/footer.liquid"],
 "en": "Occasional emails from KARMICARE about Awake & Asleep, the Dental Check-up Reward and member offers. Unsubscribe any time with the link in every email. <a>Privacy Policy</a>.",
 "nl": null,
 "nl_hold": null,
 "fr": null,
 "fr_hold": null,
 "href": ["privacy_url"],
 "note": "The payload's single <a> tag gets href=\"{{ privacy_url }}\". Replaces the 'you agree to the Terms' line (Victor, 23 Oct, D4).",
 "nl_review": null,
 "fr_review": "legal-review"
},
{
 "key": "kc.footer.check_inbox",
 "area": "footer",
 "ids": ["liquid:sections/footer.liquid"],
 "en": "Check your inbox to confirm your subscription.",
 "nl": null,
 "nl_hold": null,
 "fr": null,
 "fr_hold": null,
 "nl_review": null,
 "fr_review": null
},
{
 "key": "kc.footer.email_invalid",
 "area": "footer",
 "ids": ["liquid:sections/footer.liquid"],
 "en": "Check the email address.",
 "nl": null,
 "nl_hold": null,
 "fr": null,
 "fr_hold": null,
 "nl_review": null,
 "fr_review": null
}
```

NL and FR values are for the NL and FR lanes (the global coordinator routes this file). The `ids` line numbers are left out on purpose: the writer's `refresh` fills them from the source inventory.
