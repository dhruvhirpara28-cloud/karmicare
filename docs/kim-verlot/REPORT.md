# Kim Verlot · websitevoorbereiding · 29 oktober 2026

Status bijgewerkt 30 oktober 2026: Victor heeft de preview goedgekeurd (“ziet er goed uit”). De onafhankelijke Astra-review is **APPROVE voor technische voorbereiding**. Lokale implementatie en eigen unpublished preview zijn gereed; publieke vrijgave blijft open. De nieuwe foto wacht op Files-upload en de claims wachten op beoordeling. Geen claimvrijgave afgeleid uit het websiteverzoek.

Themecommit: `a380ad5` — `feat(professionals): add Kim Verlot full source testimonial` (twee templates, lokaal).

## Opdracht en bron

- Victor antwoordde volgens deze overdracht **“ok”** op de oplevering met NL/EN/FR en vroeg aansluitend: **“ok kan je aansluitend een lane maken om het toe te voegen aan onze shopify website?”** Dat vervolg is hier vastgelegd als akkoord voor de websitevoorbereiding met de aangeleverde vertalingen. Het is geen klinische claimvalidatie of bewijs van nieuwe toestemming van Kim. Tijdens deze uitvoering vroeg Victor bovendien eerst een Shopify- of localhostpreview vóór een merge.
- Bron rechtstreeks gelezen in `kc-ai-master`, commit `cb09296`: `work/reviews/karmicare-direct-feedback.md` (Kim Verlot) en `work/2026-10-29/01-kim-verlot-testimonial.md`. Niet gecherry-pickt en niet gewijzigd.
- [Figma-bron](https://www.figma.com/design/gcWcgYxS1nmheciKYOjOGx/?node-id=4123-3), Ambassadors `3947:17082`; portret `4123:6`, origineel `4121:42`. Figma-export en screenshot opgehaald en visueel vergeleken.

## Preflight en werkwijze

- Eigen branch `karmicare/kim-verlot-testimonial`, schone start op `43fb547`. Codex/GPT-6; sessiepermissies `danger-full-access`, approval `never`; geen instellingen aangepast. Orca runtime ready/reachable.
- `AGENTS.md` gelezen. `README.md` ontbreekt in deze checkout en in de actuele integratiecheckout. Het gearchiveerde exemplaar gelezen in `kc-ai-master/assets/website-v2/theme-docs/pdp-run-2026-10/_theme-repo-root/README.md`.
- Actuele vervangende regels: `work/2026-10-19/soft-launch/briefs/COMMON-RULES.md` verklaart expliciet dat README/runbook niet meer in de themerepo staan. Ook landingdocument, `assets/website-v2/SHOPIFY-SITE-STATE.md`, source-copy `registration/DRY-RUN.md`, `ROUND6.md`, `ROUND7.md`, builder en registratierunner gelezen. Historische schrijfautorisaties voor andere lanes zijn niet overgenomen voor Files of vertalingen.
- Shopify-, Figma design-to-code- en Orca-skills gebruikt. Geen andere agents gestart. Alleen eigen branch gewijzigd; geen git push, PR, merge of live/Admin-contentwrites.

## Concrete themewijziging

In beide templates uitsluitend dit veld ingevuld:

| Bestand | Veld |
|---|---|
| `templates/index.json` | `sections.trusted_professionals_HAqYth.blocks.card_qAPajg.settings.hover_text` |
| `templates/product.subscription-item.json` | `sections.trusted_professionals_HAqYth.blocks.card_qAPajg.settings.hover_text` |

Volledige EN-brontekst, zonder inkorting of herformulering. Alleen de bestaande kaartconventie `<p>“…”</p>` toegevoegd. Naam **Kim Verlot** en credentials **Breathing Coach, Heart Coherence Specialist** waren al correct. Kaartvolgorde, verborgen secties, instellingen, CSS en gedrag blijven gelijk. Structurele vergelijking tegen HEAD bevestigt dat alleen de twee `hover_text`-waarden verschillen.

Alle actuele tekstverwijzingen naar Kim gecontroleerd in templates, section groups, snippets, scripts en settings. Er zijn twee bestaande kaarten, geen derde professional toegevoegd. Hero `hero-karmicare.liquid` leest de afbeeldingen van de bestaande kaarten voor de roterende badge (vanaf regel 542), inclusief Kim; geen aparte hardcoded Kim-link. Het mobiele citaatpaneel kopieert eveneens de kaartfoto.

## Preview

- [Shopify homepage](https://karmicares.myshopify.com/?preview_theme_id=190213947773)
- [Shopify PDP](https://karmicares.myshopify.com/products/karmicare-biorhythmic-oral-care-system?preview_theme_id=190213947773)
- [Localhost homepage](http://127.0.0.1:17145/) en [PDP](http://127.0.0.1:17145/products/karmicare-biorhythmic-oral-care-system)
- Theme `190213947773`, **KC preview icare-kim-verlot-testimonial 37413173**, rol `unpublished` geverifieerd in de gerenderde pagina. Gestart met de beschermde branch-preview `dev`-helper uit de actuele previewwerkwijze; die maakte de eigen unpublished theme aan. Orca terminal `term_708a3194-71a7-4df0-a44b-f59ac371ae31`; localhost vereist dat deze blijft draaien.
- De echte preview toont de volledige EN-quote met de **bestaande Shopify-foto**. NL/FR en het nieuwe portret zijn afzonderlijke lokale layoutfixtures, niet geregistreerde/publieke resultaten.
- [Lokaal reviewoverzicht met nieuw portret en EN/NL/FR-beelden](http://127.0.0.1:17146/review.html). Dit overzicht bevat gelabelde screenshots en de volledige bronteksten; de links bovenaan openen de echte interactieve themepreview. Server in Orca-terminal `term_a0824f4c-6369-45a5-a74e-793ea714a469` (`python3 -m http.server 17146 --bind 127.0.0.1 --directory docs/kim-verlot`).

## Foto: bestand en exacte koppeling gereed

Shopify `Kim_Verlot.png` is de oudere foto met bril, 332 × 479. Figma bevat de aangeleverde foto in zwarte blouse, 1086 × 1448 (3:4). Deze is lokaal ongewijzigd opgeslagen als `docs/kim-verlot/kc-professional-kim-verlot.png`; afmetingen, SHA-256 en bestemming staan in `portrait-manifest.json`. Binaries onder docs zijn volgens de repoafspraak niet gecommit.

Na expliciet toegestane upload door Victor/de bevoegde eigenaar:

1. Upload dat bestand in Shopify Files. Controleer de daadwerkelijk toegekende bestandsnaam/URI; niet stilzwijgend aannemen dat er geen suffix is toegevoegd.
2. Verwachte URI: `shopify://shop_images/kc-professional-kim-verlot.png`. Als die exact klopt, pas `portrait-after-upload.patch` toe op deze branch. De patch wijzigt alleen `image` in de twee bovenstaande kaarten; `git apply --check` slaagt. Bij afwijkende URI beide waarden aanpassen aan de echte URI.
3. Herhaal previewcontrole van kaart, mobiel paneel en hero-badge. De badge volgt vanzelf de kaartbron; geen aparte upload of wijziging aan de hero nodig. De bestaande kaartcrop blijft `object-fit: cover`.
4. Run Theme Check vóór de themecommit. Tot dan blijft de bestaande werkende foto gekoppeld; geen verwijzing naar een nog niet bestaand Files-object.

## NL/FR: registratie voorbereid, niet uitgevoerd

- `testimonials.json`: volledige NL-, EN- en FR-bron; Nederlands exact behouden.
- `source-additions.json`: twee EN-inventarisregels met exacte velden en SHA-1.
- `payload-nl.json` / `payload-fr.json`: twee volledige richtextwaarden per taal, hetzelfde schema als de bestaande locale batches.
- `offline-plan-nl.json` / `offline-plan-fr.json`: gebouwd met de **bestaande** `build_payloads.py` uit de source-copy-lane. Per taal 2 resources, 2 items op hold, **0 schrijfbare items**. Geen verzonnen Shopify-resource-ID, key of live digest.
- `build-offline-plans.py` reproduceert deze controle zonder netwerk en zonder een andere checkout te wijzigen. De expliciete per-item claimhold blijft gelden, ook als de algemene `pending-claim-review`-gate elders is vrijgegeven.

Overdracht aan source-copy: voeg de twee EN-regels toe aan `docs/source-copy/en-source.json` en hun batches 01/02, en de locale regels aan de overeenkomstige NL/FR-batches. Registreer de per-item holds in `registration/holds.json`, herbereken batchdigests met de bestaande workflow en bouw opnieuw. Geen locale-JSON-sleutel of browservertaling als productieroute toevoegen.

Pas **na claimbesluit en publicatie van deze EN-bron** de live EN opnieuw vastleggen, de holds op een gedateerd besluit aanpassen, en `register.py --lang both --theme-id 187295564157` als read-only dry-run uitvoeren vanuit de actuele source-copy-checkout. Verifieer eerst dat dit nog de MAIN theme is. De runner moet de template-identiteit, drie key-hints en EN-hash bewijzen; de actuele dry-run-checksum gaat naar review. Alleen de bevoegde eigenaar voert daarna de goedgekeurde registratie uit. De huidige offlineplannen zijn geen live dry-run of schrijfgoedkeuring. Na registratie homepage/PDP in `/nl` en `/fr` controleren; NL/FR zijn volgens de locale workflow al gepubliceerd, zodat registreren direct publiek effect heeft.

## Concrete claimbevindingen voor review

| Passage | Bevinding uit bron en tekstvergelijking |
|---|---|
| Bioritme ondersteunen / dagelijks ritueel | Kims persoonlijke motivatie; hier geen onafhankelijk bewijs van werking geregistreerd. |
| “mijn zenuwstelsel te helpen schakelen” | De bron markeert dit als fysiologische effectclaim vóór publieke marketing te toetsen. EN “help my nervous system transition” en FR “aider mon système nerveux…” behouden dat effect. “Helpen” of het feit dat het een testimonial is, is in deze overdracht geen claimvrijgave. |
| “teruggetrokken tandvlees onder controle” | De bron markeert dit als klinische effectclaim. EN “receding gums under control” en FR “récession gingivale sous contrôle” behouden de claim. Deze testimonial onderbouwt op zichzelf geen werkzaamheid bij tandvleesrecessie; er is in deze bronnen geen claimvalidatie of productonderzoek bijgevoegd. |

Geen stilzwijgende afzwakking, excerpt of nieuwe claim gemaakt. De reviewer moet beide effectclaims en hun onderbouwing/toelaatbaarheid beoordelen vóór publieke marketing. Victors vertaal- en websitevervolgakkoord vervangt dat niet. Bij benodigde herformulering of excerpt terug naar de bron-/toestemmingswerkwijze.

## Validatie en landing

- `shopify theme check --fail-level error`: exit 0; 241 files, 0 errors, 19 warnings; geen nieuwe ignores.
- Shopify-skillvalidator geprobeerd voor beide templates; tool kon niet starten door ontbrekend pakket `@shopify/theme-check-common` in de plugin. De rechtstreeks uitgevoerde Theme Check hierboven slaagt.
- Gerichte JSON-vergelijking: uitsluitend twee quotevelden gewijzigd; volledige bron, naam, credentials, kaartvolgorde en disabled-flags geverifieerd. Bestaande quote-panel- en Day/Night-JS slagen voor `node --check`.
- Browserresultaten en screenshots: zie `qa-preview.json`, `qa-fixture.json` en `shots/`. `check-preview.py` controleert volledige quote, unieke originele kaart, foto geladen, credentials, overflow en mobiel paneel/focusterugkeer. De homepage gebruikt de echte Day/Night-knoppen; de PDP heeft geen toggle en gebruikt uitsluitend voor de CSS-controle een tijdelijke body-modeklasse. Orca offscreen RAF wordt door screenshots geactiveerd; productiecode is daarvoor niet aangepast.
- EN: 24 controles geslaagd (homepage/PDP × 393/768/1024/1440/1920/2560 × Day/Night). NL/FR met nieuw portret: 16 lokale layoutcontroles (homepage/PDP × 393/1440 × Day/Night × NL/FR). Credentials in deze fixtures blijven EN; er is geen nieuwe vertaling daarvan geschreven of geregistreerd.
- Landing pas na Victors previewreview en expliciet claimbesluit. Themecommit met de twee templates via de bestaande landing/integratieprocedure laten landen; docs blijven reviewmateriaal en worden niet naar het live theme meegenomen. Fotovervolg en locale registratie zoals hierboven. Victor pusht, DH publiceert via main; deze sessie doet geen merge/push/PR.

## Afronding 30 oktober 2026

- Victor vroeg na zijn previewakkoord om de standaard Astra-review; deze is uitgevoerd met `gpt-6-astra`, effort `xhigh`, via Orca orchestration. Task `task_bb88c8f1fc89`, dispatch `ctx_275573bfe8f0`; beoordeelde HEAD `81d3a59380a4ba8adfa0ff10f25dc0eb78890162`. Resultaat: **APPROVE voor technische voorbereiding**, geen geïntroduceerde technische blockers. Volledig lokaal rapport: `docs/runtime-review/KIM-VERLOT-ASTRA.md` (runtime-review is gitignored).
- Onafhankelijke controle: brongetrouwheid alle talen, exact twee velden gewijzigd, 20 browserstaten inclusief 320px en de 749/750px-grens, keyboard/open/close/focusherstel, pointer-hover, hero-rotatie, vier lokale foto/locale-fixtures. Theme Check: 0 errors, 19 warnings. Bestaande paginaoverflow bij 320px is geïsoleerd als niet door Kim veroorzaakt; kaart en paneel passen.
- Victors vervolg “kan je die afwerken” is vastgelegd. De eerdere expliciete beperkingen voor Admin-writes en de open claimbeoordeling zijn niet als vervallen beschouwd. Er is specifiek toestemming gevraagd voor de foto-upload en vier vertaalvelden, en gevraagd naar een claimbesluit; op dit moment is geen antwoord of claimbewijs geregistreerd.
- `landing-check.json` legt een conflictvrije in-memory Git-merge tegen lokale `merchant-edit` `98e1f1f` vast. Structurele vergelijking bewijst dat uitsluitend Kims twee quotevelden veranderen ten opzichte van die merchant-versie; recentere rating- en andere templatewijzigingen blijven behouden. `merchant-landing.patch` is de concrete theme-only delta voor die basis. Dit is een voorbereidingscontrole, geen uitgevoerde merge of remote-statuscontrole. Controleer de basis opnieuw als merchant vooruitgaat.
- Themecommits blijven `a380ad5` en de voorbereidingsdocumentatie `81d3a59`; deze afronding wijzigt alleen documentatie. Geen nieuwe theme-implementatie na Astra. Geen push, PR, merge, Files-upload of registratie uitgevoerd.
- Open uitvoering: upload na specifiek akkoord en verifieer URI; pas portrait-patch toe en test echte preview; registreer locale-rows met expliciete holds in source-copy; release pas na gedateerd claimbesluit, daarna actuele live dry-run en bevoegde registratie. De EN-quote mag eveneens niet voortijdig publiek landen: locale-holds verbergen geen Engelse templatecopy.
