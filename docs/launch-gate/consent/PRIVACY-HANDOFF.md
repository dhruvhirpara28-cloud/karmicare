# Privacy page: wording handoff to gate-legal (R61b and R61c, 24 Oct 2026)

From lane gate-consent, after Astra's R61 review (N1) and R61b recheck (B1 and the publication follow-ups). The lane did not touch the privacy template, the policy record or any locale; gate-legal applies this. Source of the current text: `docs/localization/nl/batch-04-legal.json` and `docs/localization/fr/batch-04-legal.json`, resource `admin:policy:privacy-policy`, items `body#b127` (section 9.2) and `body#b082` (section 5, "Analytics and optimisation"). The same text is live at `/pages/privacy-policy` (EN, NL; FR as published).

## Why

The live privacy page promises, for everyone, "No non-essential cookies or tracking scripts run before you opt in." Since R61 the theme loads Hotjar by region, following Shopify's Customer Privacy defaults: in the regions where the cookie banner is active (EU/EEA, UK, and Switzerland once it is in the region list) only after Accept; elsewhere by default, unless the visitor opts out of data sale/sharing through "Your privacy choices" or a Global Privacy Control signal. Withdrawal stops Hotjar from the next page view; the page already open keeps recording until it is left. The text below says exactly that. Nothing else in the loader changed what the page says about Google, Meta or Triple Whale (those stay consent-gated by Shopify everywhere the banner is active and run by default elsewhere, which the same new wording covers).

Conditions the wording depends on, for Victor to confirm in Settings → Customer privacy (see `ADMIN-STEPS.md` §2.1 and §2.3):

- The region list contains the EU/EEA, the UK **and Switzerland**. If CH is not in the list, drop "Switzerland"/"Zwitserland"/"Suisse" from the texts below.
- The **Data Sharing Opt-Out Page** is on, with the intended opt-out regions, **and verified** before publication (Astra R61b B1; the verification step is `ADMIN-STEPS.md` §2.3 "Before deployment"): the "Your privacy choices" link is visible in the footer and Shopify reports `sale_of_data` as denied for a visitor with a GPC signal in those regions. Only then may the texts promise the link **and** GPC handling. The loader never reads the raw browser GPC signal; it reads only the permission Shopify derives from it, and Shopify derives it only where the opt-out page is active. If the page is off at publication, drop **both** the "Your privacy choices" clause and the GPC clause: the second sentence then ends after "may run by default" (NL "standaard actief zijn", FR "actives par défaut"). The other way to keep today's universal sentence is to make the banner apply to all regions.

## 1. Section 9.2 "Your consent choices", second paragraph (`body#b127`)

### Current

- EN: No non-essential cookies or tracking scripts run before you opt in. You can change or withdraw your choice at any time through the “Cookie settings” link in our footer.
- NL: Er worden geen niet-essentiële cookies of trackingscripts uitgevoerd voordat je daarmee instemt. Je kunt je keuze op elk moment wijzigen of intrekken via de link “Cookie-instellingen” in de footer van onze website.
- FR: Aucun cookie non essentiel ni script de suivi ne s’exécute avant que vous n’y consentiez. Vous pouvez modifier ou retirer votre choix à tout moment via le lien “Préférences en matière de cookies” de notre pied de page.

### Replacement

- EN: In the European Economic Area, the United Kingdom and Switzerland, no non-essential cookies or tracking scripts run before you opt in. Elsewhere, analytics and advertising technologies may run by default; where the law gives you a right to opt out of the sale or sharing of your data, you can use the “Your privacy choices” link in our footer or a Global Privacy Control signal in your browser, and we honour it. You can change or withdraw your choice at any time through the “Cookie preferences” link in our footer. For Hotjar, a withdrawal takes effect from the next page you open; the page you are on keeps recording until you leave it.
- NL: In de Europese Economische Ruimte, het Verenigd Koninkrijk en Zwitserland worden geen niet-essentiële cookies of trackingscripts uitgevoerd voordat je daarmee instemt. Elders kunnen analyse- en advertentietechnologieën standaard actief zijn; waar de wet je het recht geeft om je te verzetten tegen de verkoop of het delen van je gegevens, kun je de link “[NL-label van Shopify voor Your privacy choices]” in onze footer of een Global Privacy Control-signaal in je browser gebruiken, en dat respecteren wij. Je kunt je keuze op elk moment wijzigen of intrekken via de link “Cookievoorkeuren” in onze footer. Voor Hotjar geldt een intrekking vanaf de volgende pagina die je opent; de pagina waarop je je bevindt, blijft opnemen tot je die verlaat.
- FR: Dans l’Espace économique européen, au Royaume-Uni et en Suisse, aucun cookie non essentiel ni script de suivi ne s’exécute avant que vous n’y consentiez. Ailleurs, des technologies d’analyse et de publicité peuvent être actives par défaut ; lorsque la loi vous donne le droit de vous opposer à la vente ou au partage de vos données, vous pouvez utiliser le lien “[libellé FR de Shopify pour Your privacy choices]” de notre pied de page ou un signal Global Privacy Control dans votre navigateur, et nous le respectons. Vous pouvez modifier ou retirer votre choix à tout moment via le lien “Préférences en matière de cookies” de notre pied de page. Pour Hotjar, un retrait prend effet à partir de la page suivante que vous ouvrez ; la page sur laquelle vous vous trouvez continue d’enregistrer jusqu’à ce que vous la quittiez.

Notes for gate-legal:

- Footer link labels are Shopify's own policy titles and cannot be edited in the theme: EN "Cookie preferences", NL "Cookievoorkeuren" (both verified live on 24 Oct). Verify the FR label on the live FR footer before publishing; "Préférences en matière de cookies" is the FR translation already in the batch. The current EN/NL texts say "Cookie settings"/"Cookie-instellingen", which do not match the real links; the batch note on `body#b127` already asks for this alignment.
- "Your privacy choices" is Shopify's link text for the data-sharing opt-out page; Shopify translates it per storefront language. The NL and FR texts above carry a bracketed placeholder for that label on purpose: on 24 Oct (checked ~17:30 UTC) the live footer has no such link yet, so the localised labels cannot be read. Once the page is on (`ADMIN-STEPS.md` §2.3 "Before deployment", step 2), replace the placeholders with the labels Shopify renders in the NL and FR footers.
- FR typography: the FR lines in this file carry the no-break space (U+00A0) before ";" and ":" as in the FR batch; keep them when pasting.

## 2. Section 5, processor list, the "Analytics and optimisation" item (`body#b082`), Hotjar part only

### Current (Hotjar clause inside the item)

- EN: … · Hotjar Ltd. (Malta), heatmaps and session analysis, with your consent and keystroke masking · …
- NL: … · Hotjar Ltd. (Malta), heatmaps en sessieanalyse, met je toestemming en maskering van toetsaanslagen · …
- FR: … · Hotjar Ltd. (Malte), cartes de chaleur et analyse de sessions, avec votre consentement et masquage des frappes · …

### Replacement (only this clause; the rest of the item stays)

- EN: · Hotjar Ltd. (Malta), heatmaps and session analysis, with keystroke masking; in the EEA, the UK and Switzerland only with your consent, elsewhere by default unless you opt out ·
- NL: · Hotjar Ltd. (Malta), heatmaps en sessieanalyse, met maskering van toetsaanslagen; in de EER, het Verenigd Koninkrijk en Zwitserland alleen met je toestemming, elders standaard tenzij je je afmeldt ·
- FR: · Hotjar Ltd. (Malte), cartes de chaleur et analyse de sessions, avec masquage des frappes ; dans l’EEE, au Royaume-Uni et en Suisse uniquement avec votre consentement, ailleurs par défaut sauf si vous vous y opposez ·

Note: "with keystroke masking" stays only if Victor confirms it in Hotjar for site 1364127 (`ADMIN-STEPS.md` §2.3, still open). If masking is off, remove the clause rather than keep a promise.

## 3. Section 9.1 "Cookie categories": the two bullets with the universal promise (R61c, Astra follow-up)

Both bullets end in "Active only after your explicit consent", which contradicts the regional rule 9.2 now carries. Same change in both; the rest of each bullet stays. The text lives in the theme page section (`page.privacy-policy:legal_toc_section_gYznx3/content_section_CDtWCV/content`) and in the admin policy copy (`admin:policy:privacy-policy`); apply to both.

### Current ending of each bullet

- EN: Active only after your explicit consent.
- NL: Actief alleen na je uitdrukkelijke toestemming.
- FR: Actifs uniquement après votre consentement explicite.

### Replacement ending

- EN: In the European Economic Area, the United Kingdom and Switzerland active only after your explicit consent; elsewhere by default unless you opt out (see 9.2).
- NL: In de Europese Economische Ruimte, het Verenigd Koninkrijk en Zwitserland alleen actief na je uitdrukkelijke toestemming; elders standaard, tenzij je je afmeldt (zie 9.2).
- FR: Dans l’Espace économique européen, au Royaume-Uni et en Suisse actifs uniquement après votre consentement explicite ; ailleurs par défaut, sauf si vous vous y opposez (voir 9.2).

The "unless you opt out" clause depends on the same verification as 9.2 (Data Sharing Opt-Out Page on and verified); if it is off at publication, end the sentence after "elsewhere by default" / "elders standaard" / "ailleurs par défaut".

## 4. Also affected, not rewritten here (gate-legal's call)

- Processor list completeness from R60 (`REPORT.md` §6): TikTok, Klaviyo (web pixel), Judge.me, Loop Subscriptions and, if kept, UpPromote are missing.
- Not a certification: this handoff makes the text match what the code does and what Shopify documents. The lawful basis for default analytics outside banner regions and the "page already open keeps recording" limitation are for gate-legal and the lawyer to assess (Astra R61b).

## 5. Shopify Network Intelligence (Victor, 24 Oct: keep it enabled and say so in the privacy policy)

Settings → Customer privacy shows **Shopify Network Intelligence: Enabled** (screenshot from Victor, 24 Oct). Victor's decision is to keep it on and cover it in the privacy policy; this belongs in the privacy policy, not in the Terms, because it is a processing of personal data. New paragraph, to go in section 5 directly after the item that names Shopify as our shop platform (or as the last item of the processor list if Shopify is not named yet).

What the feature does, in Shopify's words (help.shopify.com, Customer privacy settings, and shopify.com/legal/terms-faq, both read 24 Oct 2026): "Shopify will securely use your customer data together with customer data from other merchants to generate insights" that power "advanced features, known as Enhanced Services": "Improved products and personalization for your store and customers", "Improved store performance", "Better ad targeting". "No other merchant can access your data." Apps that require it: Shopify Audiences, Shop channel, Shopify Email, Shopify Collabs, Shopify Search & Discovery. Consent is respected: customers who decline non-essential cookies or opt out of sale/sharing are excluded from its advertising and other non-essential uses. Shopify also asks that the cookie banner names Shopify (ours does: "We and our partners, including Shopify") and that our privacy policy links to the Shopify Consumer Privacy Policy.

### Text

- EN: **Shopify Network Intelligence.** Our shop runs on Shopify. We have enabled Shopify Network Intelligence, which means Shopify uses customer and device data from our shop together with data from other Shopify shops to generate aggregated insights that power Shopify's enhanced services: improved products and personalisation, shop performance, and advertising and discovery tools such as Shopify Audiences, the Shop app, Shopify Email, Shopify Collabs and Search & Discovery. No other merchant can access our customer data. Your choices on our site apply here too: if you decline non-essential cookies or opt out of data sharing, your data is not used for Shopify Network Intelligence's advertising or other non-essential purposes. Shopify describes this processing in the <a href="https://www.shopify.com/legal/privacy/consumers">Shopify Consumer Privacy Policy</a> and offers its own opt-out for marketing based on your interactions with Shopify shops at <a href="https://privacy.shopify.com">privacy.shopify.com</a>.
- NL: **Shopify Network Intelligence.** Onze shop draait op Shopify. We hebben Shopify Network Intelligence ingeschakeld. Dat betekent dat Shopify klant- en apparaatgegevens uit onze shop samen met gegevens van andere Shopify-shops gebruikt om geaggregeerde inzichten te maken voor de uitgebreide diensten van Shopify: betere producten en personalisatie, prestaties van de shop, en advertentie- en ontdekkingstools zoals Shopify Audiences, de Shop-app, Shopify Email, Shopify Collabs en Search & Discovery. Geen enkele andere handelaar kan onze klantgegevens inzien. Je keuzes op onze site gelden ook hier: als je niet-essentiële cookies weigert of je afmeldt voor het delen van gegevens, worden je gegevens niet gebruikt voor advertenties of andere niet-essentiële doelen van Shopify Network Intelligence. Shopify beschrijft deze verwerking in het <a href="https://www.shopify.com/legal/privacy/consumers">Shopify Consumer Privacy Policy</a> en biedt op <a href="https://privacy.shopify.com">privacy.shopify.com</a> een eigen afmelding voor marketing op basis van je interacties met Shopify-shops.
- FR: **Shopify Network Intelligence.** Notre boutique fonctionne sur Shopify. Nous avons activé Shopify Network Intelligence : Shopify utilise les données clients et les données d’appareil de notre boutique, avec celles d’autres boutiques Shopify, pour produire des analyses agrégées qui alimentent ses services avancés : amélioration des produits et de la personnalisation, performance de la boutique, et outils publicitaires et de découverte tels que Shopify Audiences, l’application Shop, Shopify Email, Shopify Collabs et Search & Discovery. Aucun autre marchand ne peut accéder à nos données clients. Vos choix sur notre site s’appliquent ici aussi : si vous refusez les cookies non essentiels ou vous opposez au partage de vos données, vos données ne sont pas utilisées à des fins publicitaires ni à d’autres fins non essentielles de Shopify Network Intelligence. Shopify décrit ce traitement dans sa <a href="https://www.shopify.com/legal/privacy/consumers">politique de confidentialité pour les consommateurs</a> et propose sur <a href="https://privacy.shopify.com">privacy.shopify.com</a> son propre mécanisme de refus du marketing fondé sur vos interactions avec les boutiques Shopify.

### For gate-legal and the lawyer before publishing

- **Shopify's role.** Neither the help page nor the terms FAQ says whether Shopify acts as processor or as independent controller for Enhanced Services; the Terms of Service and Data Processing Addendum update of 25 July 2025 should. The text above avoids both words on purpose. If the terms make Shopify an independent controller, add "Shopify is responsible for this processing" and our duty is transparency; if Shopify stays our processor, we need our own legal basis (legitimate interest, with a balancing test) and it must be named in section 4 of the policy.
- **Link to the Shopify Consumer Privacy Policy** is a Shopify requirement when the feature is on; if the policy does not link it yet, this paragraph adds it.
- **Consent dependency.** The promise "your choices on our site apply here too" holds only where the cookie banner is active (verify the 23-region list, `ADMIN-STEPS.md` §2.3) and, for the "opt out of data sharing" half, only once the Data Sharing Opt-Out Page is on and verified (same "Before deployment" step). Until then keep only the cookie half of that sentence.
- **Alternative.** Disabling the feature removes the sentence but also uninstalls Shopify Search & Discovery and cuts access to Shop channel, Shopify Email, Collabs and Audiences, immediately and without automatic restore. That is why Victor keeps it on.
