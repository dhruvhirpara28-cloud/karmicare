# Privacy page: wording handoff to gate-legal (R61b, 24 Oct 2026)

From lane gate-consent, after Astra's R61 review (N1). The lane did not touch the privacy template, the policy record or any locale; gate-legal applies this. Source of the current text: `docs/localization/nl/batch-04-legal.json` and `docs/localization/fr/batch-04-legal.json`, resource `admin:policy:privacy-policy`, items `body#b127` (section 9.2) and `body#b082` (section 5, "Analytics and optimisation"). The same text is live at `/pages/privacy-policy` (EN, NL; FR as published).

## Why

The live privacy page promises, for everyone, "No non-essential cookies or tracking scripts run before you opt in." Since R61 the theme loads Hotjar by region, following Shopify's Customer Privacy defaults: in the regions where the cookie banner is active (EU/EEA, UK, and Switzerland once it is in the region list) only after Accept; elsewhere by default, unless the visitor opts out of data sale/sharing through "Your privacy choices" or a Global Privacy Control signal. Withdrawal stops Hotjar from the next page view; the page already open keeps recording until it is left. The text below says exactly that. Nothing else in the loader changed what the page says about Google, Meta or Triple Whale (those stay consent-gated by Shopify everywhere the banner is active and run by default elsewhere, which the same new wording covers).

Conditions the wording depends on, for Victor to confirm in Settings → Customer privacy (see `ADMIN-STEPS.md` §2.1 and §2.3):

- The region list contains the EU/EEA, the UK **and Switzerland**. If CH is not in the list, drop "Switzerland"/"Zwitserland"/"Suisse" from the texts below.
- The **Data Sharing Opt-Out Page** is on for the opt-out regions (US states). If it is off, drop the "Your privacy choices" clause and keep only the GPC clause, or make the banner apply to all regions and keep today's universal sentence instead.

## 1. Section 9.2 "Your consent choices", second paragraph (`body#b127`)

### Current

- EN: No non-essential cookies or tracking scripts run before you opt in. You can change or withdraw your choice at any time through the “Cookie settings” link in our footer.
- NL: Er worden geen niet-essentiële cookies of trackingscripts uitgevoerd voordat je daarmee instemt. Je kunt je keuze op elk moment wijzigen of intrekken via de link “Cookie-instellingen” in de footer van onze website.
- FR: Aucun cookie non essentiel ni script de suivi ne s’exécute avant que vous n’y consentiez. Vous pouvez modifier ou retirer votre choix à tout moment via le lien “Préférences en matière de cookies” de notre pied de page.

### Replacement

- EN: In the European Economic Area, the United Kingdom and Switzerland, no non-essential cookies or tracking scripts run before you opt in. Elsewhere, analytics and advertising technologies may run by default; where the law gives you a right to opt out of the sale or sharing of your data, you can use the “Your privacy choices” link in our footer or a Global Privacy Control signal in your browser, and we honour it. You can change or withdraw your choice at any time through the “Cookie preferences” link in our footer. A withdrawal takes effect from the next page you open; the page you are on keeps running until you leave it.
- NL: In de Europese Economische Ruimte, het Verenigd Koninkrijk en Zwitserland worden geen niet-essentiële cookies of trackingscripts uitgevoerd voordat je daarmee instemt. Elders kunnen analyse- en advertentietechnologieën standaard actief zijn; waar de wet je het recht geeft om je te verzetten tegen de verkoop of het delen van je gegevens, kun je de link “Your privacy choices” in onze footer of een Global Privacy Control-signaal in je browser gebruiken, en dat respecteren wij. Je kunt je keuze op elk moment wijzigen of intrekken via de link “Cookievoorkeuren” in onze footer. Een intrekking geldt vanaf de volgende pagina die je opent; de pagina waarop je je bevindt, blijft actief tot je die verlaat.
- FR: Dans l’Espace économique européen, au Royaume-Uni et en Suisse, aucun cookie non essentiel ni script de suivi ne s’exécute avant que vous n’y consentiez. Ailleurs, des technologies d’analyse et de publicité peuvent être actives par défaut ; lorsque la loi vous donne le droit de vous opposer à la vente ou au partage de vos données, vous pouvez utiliser le lien “Your privacy choices” de notre pied de page ou un signal Global Privacy Control dans votre navigateur, et nous le respectons. Vous pouvez modifier ou retirer votre choix à tout moment via le lien “Préférences en matière de cookies” de notre pied de page. Un retrait prend effet à partir de la page suivante que vous ouvrez ; la page sur laquelle vous vous trouvez reste active jusqu’à ce que vous la quittiez.

Notes for gate-legal:

- Footer link labels are Shopify's own policy titles and cannot be edited in the theme: EN "Cookie preferences", NL "Cookievoorkeuren" (both verified live on 24 Oct). Verify the FR label on the live FR footer before publishing; "Préférences en matière de cookies" is the FR translation already in the batch. The current EN/NL texts say "Cookie settings"/"Cookie-instellingen", which do not match the real links; the batch note on `body#b127` already asks for this alignment.
- "Your privacy choices" is Shopify's link text for the data-sharing opt-out page; Shopify translates it per storefront language. If the NL/FR footer shows a translated label once the page is on, use that label in the NL/FR texts.
- FR typography: when applying, insert the usual no-break spaces before ";" and ":" (the FR batch convention); this Markdown file carries plain spaces.

## 2. Section 5, processor list, the "Analytics and optimisation" item (`body#b082`), Hotjar part only

### Current (Hotjar clause inside the item)

- EN: … · Hotjar Ltd. (Malta), heatmaps and session analysis, with your consent and keystroke masking · …
- NL: … · Hotjar Ltd. (Malta), heatmaps en sessieanalyse, met je toestemming en maskering van toetsaanslagen · …
- FR: … · Hotjar Ltd. (Malte), cartes de chaleur et analyse de sessions, avec votre consentement et masquage des frappes · …

### Replacement (only this clause; the rest of the item stays)

- EN: · Hotjar Ltd. (Malta), heatmaps and session analysis, with keystroke masking; in the EEA, the UK and Switzerland only with your consent, elsewhere by default unless you opt out ·
- NL: · Hotjar Ltd. (Malta), heatmaps en sessieanalyse, met maskering van toetsaanslagen; in de EER, het Verenigd Koninkrijk en Zwitserland alleen met je toestemming, elders standaard tenzij je je afmeldt ·
- FR: · Hotjar Ltd. (Malte), cartes de chaleur et analyse de sessions, avec masquage des frappes ; dans l’EEE, au Royaume-Uni et en Suisse uniquement avec votre consentement, ailleurs par défaut sauf si vous vous y opposez ·

Note: "with keystroke masking" stays only if Victor confirms it in Hotjar for site 1364127 (`ADMIN-STEPS.md` §2.3, still open). If masking is off, remove the clause rather than keep a promise.

## 3. Also affected, not rewritten here (gate-legal's call)

- Section 9.1 bullets "Performance and analytics … Active **only after your explicit consent**" and "Marketing and advertising … Active **only after your explicit consent**" carry the same universal promise. Either qualify them with "in the regions named in 9.2" or leave 9.2 to carry the regional rule.
- Processor list completeness from R60 (`REPORT.md` §6): TikTok, Klaviyo (web pixel), Judge.me, Loop Subscriptions and, if kept, UpPromote are missing.
