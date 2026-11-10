# Kim Verlot · websitevoorbereiding · 29 oktober 2026

Status bijgewerkt 30 oktober 2026: Victor heeft de preview goedgekeurd (“ziet er goed uit”). De onafhankelijke Astra-review is **APPROVE voor technische voorbereiding**. Lokale implementatie en eigen unpublished preview zijn gereed; publieke vrijgave blijft open. Actuele status: Victor bevestigde op 30 oktober dat de claimreview is geaccepteerd. Het Figma-portret is op zijn expliciete verzoek geüpload. NL/FR wachten op de nieuwe EN-bron in het gepubliceerde theme; zie het laatste vervolg hieronder. Oudere secties beschrijven de voorbereiding vóór deze besluiten.

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

## Uitgevoerde lokale merchant-landing · 30 oktober 2026

Victor gaf expliciet opdracht: “commit en merge naar merchant”. Daarmee is de lokale merge nu toegestaan en uitgevoerd. Kim-lane `62381f4` is via theme-only landingcommit `61a0944` geland. Tijdens de uitvoering rondde een andere lane merchant-landing `7d4607f` (rating weight 600) af. Beide lijnen zijn zonder conflicten samengevoegd in `ff95f83`; `merchant-edit` is daarna succesvol met `--ff-only` naar `ff95f83` gebracht.

Ten opzichte van merchant `7d4607f` wijzigen uitsluitend de twee volledige EN `hover_text`-velden. Alle overige templatewaarden zijn structureel identiek en de gelijktijdige rating-CSS is byte-identiek behouden. Docs zijn uit de landingtree gehouden en blijven op deze lane. Theme Check op de uiteindelijke landingtree: exit 0, 0 errors, 19 warnings. Geen nieuwe themecode na Astra buiten de reeds afzonderlijk gelande rating-CSS; de Kim-delta blijft exact de beoordeelde quote.

Geen push, PR, main-merge, publicatie of Admin-write uitgevoerd. Bestaande ongetrackte `.claude/` in merchant ongemoeid gelaten. De lokale merge heft de publieke claimhold niet op. Nieuwe foto en NL/FR-registratie blijven voorbereid, niet uitgevoerd. De bestaande Shopify-foto blijft gekoppeld.

## Claimakkoord en echte foto-upload · 30 oktober 2026

Victor bevestigde expliciet “claimreview is geaccepteerd”; `claim-decision.json` registreert dit als eigenaarsbesluit voor precies Kims twee quotevelden, zonder zelfstandige klinische validatie te claimen. De vier locale-payloadregels en EN-bronregistratie zijn bijgewerkt; de Kim-only builder houdt nu nul items tegen. De volledige EN/NL/FR-tekst is ongewijzigd.

Victor vroeg vervolgens de foto in Shopify te uploaden en zette Orca open op Files. Via die pagina is uitsluitend `kc-professional-kim-verlot.png` geüpload. Shopify bevestigde de upload, de naam zonder suffix en 1086 × 1448. MediaImage `70092619088253`; de originele CDN-URL antwoordde 200. `portrait-manifest.json` bevat de URL. Beide bestaande template-imagevelden verwijzen nu naar `shopify://shop_images/kc-professional-kim-verlot.png`; hero en mobiel paneel volgen die kaartbron. Geen andere Admin-content gewijzigd.

De read-only registratiecheck bevestigt MAIN `187295564157`, maar meldt voor beide quotes in beide talen `missing`: geen live key met de vereiste section/block/hover_text-identiteit. Dit is de resterende registratieafhankelijkheid; de claimhold is opgeheven. `dry-run.py` hergebruikt de bestaande registratierunner met uitsluitend Kims templateplannen en lege, expliciete template-only bindings. Zo worden geen niet-gerelateerde metaobjectbindings meegenomen. Geen vertalingen geschreven. Na publicatie van de EN-bron moet de dry-run opnieuw uitgevoerd en het nieuwe concrete checksum-resultaat beoordeeld worden; de huidige nul-operaties zijn geen uitvoerbare registratiegoedkeuring.

Victor vroeg “als je klaar bent commit en merge naar merchant”. De fotowijziging wordt daarom lokaal gecommit en via de theme-only landingroute naar merchant gebracht; geen push/main-merge/publicatie.

Uitgevoerd: fotocommit `857cb9a`, bewijs/claimbesluit `3e93bf6`, theme-only landing en merchant HEAD `fd3ef8f`. De merge bevat uitsluitend de twee imagewaarden ten opzichte van `ff95f83`; docs-conflicten zijn volgens de landingafspraak opgelost door docs buiten de landingtree te houden. Acht echte previewcontroles (homepage/PDP × 393/1440 × Day/Night) bevestigen geladen nieuwe CDN-foto, volledige quote, naam/credentials, mobiel paneel en focusherstel. Beide Theme Checks (lane en uiteindelijke landingtree) exit 0. NL/FR live dry-run: 0 registraties, 0 removals, 0 stale bindings; beide quotevelden ontbreken nog live.

## Portretuitsnede gecorrigeerd · 30 oktober 2026

Victor meldde dat Kims hoofdpositie afweek van de overige professionals. Visuele vergelijking met Kris en Sietske toont extra hoofdruimte in Kims bron. Commit `004894d` schaalt uitsluitend haar kaart- en paneelfoto 1.12 rond de rechteronderhoek. Daardoor komt haar hoofd hoger en meer centraal; de bestaande containers knippen de overhang af. Geen beeldbestand, quote, layout of andere professional gewijzigd. Hero blijft zijn bestaande vierkante uitsnede behouden.

Echte branch-preview: acht staten geslaagd (homepage/PDP, 393/1440, Day/Night), plus visuele controle van de volledige mobiele Night-dialog na de animatie. Computed transform bevestigt de echte stylesheetregel. Theme Check: exit 0, 19 warnings. Screenshots `shots/crop-before.png`, `shots/crop-after-desktop.png`, `shots/crop-after-mobile.png`.

## Shopify Files opruiming en releasecontrole · 9 november 2026

Op Victors verzoek vier oudere bestanden via Shopify Admin verplaatst naar map `Ambassadeurs - oudere versies nog in gebruik`: `kc-professional-kim-verlot.png` (70092619088253), `Kim_Verlot.png` (69746924061053), `kc-professional-kris-sienaert.jpg` (70106633896317), `Dr._Kris_Sienaert.png` (69746924028285). Niets verwijderd of hernoemd. Alle vier oorspronkelijke CDN-URLs na het verplaatsen HTTP 200; de twee Kim- en twee Kris-locaties in Admin bevestigd. Nieuwe v2-bestanden bleven in Files. Mappenorganisatie volgens Shopify Help: https://help.shopify.com/en/manual/shopify-admin/productivity-tools/file-uploads .

Reden bewaren: live homepage gebruikt nog de oude kc-professional PNG/JPG. Legacy Kim heeft 6 verwijzingen (5 themes plus kim-verlot metaobject); legacy Kris 7 (6 themes plus dr-kris-sienaert metaobject). De Files-tabel toont voor de live Kris-JPG geen referentie, maar de live HTML bewijst gebruik; daarom is alleen die tabel geen grond voor verwijdering.

Remote main `e1d9703`, remote merchant `e274fc1`, lokale merchant `c0d2d4b`. Drie lokale commits wachten nog op push: Kris v2 `9a39749`, Kim v2 `eccfca8`, Engelse quote `c0d2d4b`. In-memory merge-tree met main `f2e2d64203ff3b51ab65142dac95b7fcdc2a40db` is conflictvrij; delta versus main alleen de twee templates en verwijderen van de Kim zoom-CSS. Theme Check op die geexporteerde merge-tree: exit 0, 236 files, 19 warnings. Geen branches gewijzigd, geen push/main-publicatie uitgevoerd.

Releasevolgorde: drie merchant-commits pushen, gecombineerde preview/review afronden, dan merchant naar main via bestaande eigenaarprocedure. Dit publiceert Kris v2, niet de lokale Kris v3-proef; v3 heeft eerst beeldakkoord en integratie nodig. Daarna live EN opnieuw vastleggen en actuele NL/FR dry-run/registratie uitvoeren. Nieuwe quote wijzigt de EN-hash: oudere Kim-plannen niet hergebruiken. Source-copy/KIM-VERLOT-QUOTE.md noemt nog een open claimhold, maar Victor bevestigde in deze sessie op 30 oktober claimreview geaccepteerd (claim-decision.json); die status moet bij de actuele registratie worden verzoend, geen nieuw klinisch bewijs verondersteld.


## 9 November — closer framing of current v2

Victor requested a larger face relative to Sietske, Stephanie and Mariama in the supplied screenshot. The current v2 JPG card image is scaled 1.2 around 50% 23%, keeping the eye line fixed. Source pixels and face remain unchanged; no AI generation or Files upload. Applies to the existing homepage and product cards, with existing clipping and quote interaction preserved.

Validation: Theme Check exit 0 (261 files, 19 warnings, zero errors). The current-source capture harness passed all eight homepage/product × mobile/desktop × Day/Night cases, including mobile panel image loading and full current EN quote. Browser computed style confirms matrix(1.2, 0, 0, 1.2, 0, 0), origin 166px 110.17px on the 332×479 desktop card. Orca screenshot rendering returned blank/repeated viewport content, so screenshots do not establish visual approval. Victor can review the actual preview at http://127.0.0.1:17145 or preview theme 190213947773. This follow-up is locally committed for preview; not published or pushed. Previous Astra approval does not cover this new crop.

## 9 November — Kris v3 and Kim v3 in Shopify Files and the theme

Victor compared the seven cards in Figma ("website asset ambassadors" 4185:24) and asked for Kris and Kim to match the rest, then approved the result: "mooi dat ziet er al beter uit. kan je de fotos in shopify files updaten, en ze ook correct in de ambassadeur locatie plaatsen".

- Kris: the ChatGPT-worker outpaint of 6 Nov (`docs/kim-verlot/kris/`), exported as `kc-professional-kris-sienaert-v3.jpg` (1328 × 1916, JPEG q82), MediaImage 70228401914237. Face AI re-rendered, not pixel-identical with v2.
- Kim: v2 zoomed 1.2× around (50%, 23%), the same framing as the CSS override from dacc90e, now baked into `kc-professional-kim-verlot-v3.jpg` (808 × 1166, JPEG q82, no AI), MediaImage 70228401881469. The `kim-verlot-v2` CSS override is removed: with v3 nothing matches its selector (`git grep kim-verlot-v2 -- assets sections snippets templates` is empty).
- Both uploaded via Claude in Chrome with the v2 alt texts; CDN URLs return 200 at the expected sizes. v2 files stay in Files.
- `templates/index.json` and `templates/product.subscription-item.json`: card_Ah46TM → Kris v3, card_qAPajg → Kim v3.
- Figma Ambassadors: photo-3 frames 4190:3 (Kris) and 4190:4 (Kim), status lines 4142:20 and 4123:19 updated; card fills in 4185:24 use the uploaded files.
- Archive with hashes: `kc-ai-master/assets/website-media/professionals/{kris-sienaert-2026-10-31,kim-verlot-2026-11-09}/README.txt`.

Measured in the 332:479 card (hair / eyes / chin): Kris v3 ~7 / 22 / 37%, Kim v3 ~9 / 22 / 34%; group 5–12 / 21–26 / 33–39%.

Validation: Theme Check `--fail-level error` 261 files, 19 warnings, zero errors. Not pushed or published; live after landing and DH's ship of main.

## 10 November — alt texts, Files cleanup, lane closed

Live since main `5a7c278` (9 Nov, merchant-edit `9d52110`): EN, NL and FR show Kris v3 and Kim v3 on the homepage and the oral-care PDP.

Shopify Files, folder "Ambassadors" (Victor had it renamed from "Ambassadeurs - oudere versies nog in gebruik"):

- Victor deleted the four unused files on 9 Nov after I selected them in his Chrome: `kc-professional-kim-verlot-v2.jpg`, `kc-professional-kris-sienaert-v2.jpg`, `kc-professional-kris-sienaert.jpg` (Kris v1) and `kc-professional-kim-verlot.png` (Kim v1). Shopify counted 0 references for each and the live EN/NL/FR pages did not load them. The originals stay in the kc-ai-master archive.
- Alt texts written through the Orca browser for the five other professionals, in the same pattern as Kim and Kris (name, then what the photo shows): Stephanie 69927109427581, Mariama 70007068033405, Leen 69927109460349, Iveta 69927109394813, Sietske 69927109493117. Each one read back after saving. All seven files in the folder now have alt text.
- `Kim_Verlot.png` (69746924061053) and `Dr._Kris_Sienaert.png` (69746924028285) from 26 Sept showed other, AI-generated faces, so they got no alt text with the real names. Victor has since deleted both (gone on 10 Nov). The `kim-verlot` and `dr-kris-sienaert` Professional Testimonial metaobjects now have an empty Image field and still the placeholder quote. They render only through the PDP `professional_testimonials` block, which is `"disabled": true` in `templates/product.subscription-item.json` on main, so nothing live shows them.

`DH/Development`, `karmicare/soft-launch-landing` and `karmicare/soft-launch-pdp` still name the deleted v1 files in their templates. Published unchanged, those cards would show no photo.

Landing: the theme changes are on merchant-edit and main (above). The lane branch carries merchant-edit and main merges, which delete 480 integration docs files and bring theme changes from other lanes, so it is not merged into `karmicare/soft-launch` as a branch. `docs/kim-verlot/` lands there as one docs-only commit taken from the lane tip.
