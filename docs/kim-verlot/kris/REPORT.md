→ lane kim-verlot-testimonial · Kris

# Dr. Kris Sienaert — v3 proef, 6 november 2026

Status: lokale AI-outpaintingproef voor Victors beeldreview. Geen Shopify-, theme- of Figma-wijzigingen; geen commits of push. Kim blijft afzonderlijk op akkoord wachten.

Update 9 november: Victor keurde v3 goed in de Figma-rij met ambassadeurs. Live als `kc-professional-kris-sienaert-v3.jpg` sinds main `5a7c278`; zie `../REPORT.md`. De PNG's in deze map staan in `.gitignore`; de v3-bron en de originelen zitten in het kc-ai-master-archief (`assets/website-media/professionals/kris-sienaert-2026-10-31/`).

## Bestanden

- `kc-professional-kris-sienaert-v3.png`: 1328 × 1916 px, exact 332:479.
- `kris-v3-kaartvergelijking.png`: v3 naast Stephanie, Mariama en Sietske; gelijke 332 × 479 kaarten, lijnen op 23% en 36%.
- Dit verslag.

## Bron en techniek

Bron: `dr-kris-sienaert-v2-original.png`, 1086 × 1448, SHA-256 `fd9c9af9abc184fc8487244085dcb2e92d06ac464149ff3850522b8e30f4a775`. V1 niet gebruikt voor generatie.

Model/tool: ingebouwde `image_gen.imagegen`. De tool rapporteert geen onderliggende model-ID; daarom geen modelnaam of versie verzonnen. Eén generatie met v2 als enige beeldreferentie.

Native resultaat: 917 × 1716 px, opgeslagen op `/Users/iamvictorious/.codex/generated_images/01a18805-1afa-7b12-ad8c-1fb188610071/exec-19d68ddd-feae-496d-8cf6-f6dcb488b9ba.png`. De tool volgde de gevraagde exportmaat niet. Voor de oplevering met `sips` bijgesneden tot 917 × 1323 vanaf x=0, y=87, daarna geëxporteerd op 1328 × 1916. Dit is opgeschaald, geen native 1328px detail. De verhoudingsafronding bedraagt minder dan 0,04%; geen afzonderlijke geometrische vervorming van gezichtsonderdelen toegepast.

## Meetwaarden

Visueel afgelezen landmarks, afgerond; indicatieve tolerantie ±0,5 procentpunt. De percentages zijn ten opzichte van de volledige afbeelding, vanaf boven, vóór naam/credentials-overlay.

| Landmark | Pixel in 1916px export (circa) | Werkelijk | Brief |
|---|---:|---:|---:|
| Bovenkant haar | 136 | 7,1% | ~7% |
| Ogen, gemiddelde pupilhoogte | 431 | 22,5% | ~23% |
| Onderkant kin/baard | 720 | 37,6% | ~36% |
| Haar tot onderkant baard | 584 | 30,5% | ~30% |
| Hoofdbreedte, inclusief oren | 383 | 28,8% van breedte | ~30% |
| Midden gezicht | 675 | 50,8% van breedte | ~50% |

Ogen–kin circa 15,1% tegenover ~17% in v2; dit blijft iets groter dan de ~13% uit de brief. Kin ligt 1,6 procentpunt onder het doel, binnen de opgegeven groepsband 34–38%. Geen gezicht vervormd om de drie landmarks onafhankelijk exact op de doellijnen te forceren.

## Wat AI heeft aangevuld / beperkingen

Ruimte rondom schouders en bovenlichaam, doorlopende navy blazer met revers, lichtblauw gestreept open hemd en extra warme kantoorachtergrond met het bestaande venster links en donker scherm rechts. Geen nieuwe tekst/logo’s of handen toegevoegd. Het eindbeeld toont meer bovenlichaam dan een strikte uitsnede op midden borst; dat staat expliciet ter beoordeling naast de doelverhouding.

Prompt vroeg uitdrukkelijk geen retouche van gezicht, haar, baard, blik, huid of belichting. **Het gegenereerde gezicht is niet aantoonbaar pixelidentiek aan de bron**: er was geen hard beschermd gezichtsmasker. Dit bestand is daarom een proef ter beoordeling, geen bevestiging dat de eis “gezicht ongewijzigd” technisch volledig gehaald is. Vergelijk met de bron vóór goedkeuring; voor gegarandeerd behoud is een afgeschermde compositie met de originele gezichtspixels nodig. Geen zelfstandige publicatiegoedkeuring gegeven.

Contactblad: Stephanie en Sietske uit de lokale `kc-ai-master/assets/website-media/professionals/t3-portraits-2026-10-13/` exports. Mariama uit de onderste referentiekaart van de meegeleverde `kris-hoofdpositie-vergelijking.jpg` (200 × 289; daarom zachter dan de andere drie). Haar bestaande hulplijnen vallen vrijwel op dezelfde 23/36%-lijnen; labels zijn voor leesbaarheid afgedekt en opnieuw getekend. Referentiegezichten niet aangepast. Geen externe bronnen opgevraagd.

## Generatieprompt

OUTPAINT AND REFRAME ONLY the supplied real photograph of Dr. Kris Sienaert for an ambassador portrait card. Preserve his photographed face unchanged: exact identity, eyes and gaze, mouth/expression, skin texture and wrinkles, hair and individual gray strands, beard, age and lighting. Do not retouch, beautify or reinterpret his face. Keep the photographed head as a single uniformly scaled, unwarped unit. Only extend the surroundings and existing clothing beyond the source edges. Output ONE 1328 x 1916 pixel portrait (aspect ratio 332:479), no text or guides. The face must be SMALLER and HIGHER in the frame than the source: top of hair around y=134 (7% height), eye line y=441 (23%), bottom of chin including beard y=690 (36%); face centered horizontally x=664, overall head width approximately 398 pixels (30% width). These are approximate composition guides; maintaining the exact original face and natural proportions takes priority over independently moving facial landmarks. Include shoulders and upper torso with a natural middle-chest/upper-body crop, NO hands, no legs. Preserve navy blazer and lapels, light-blue finely striped open-collar shirt. Extend the same softly blurred warm office background, window to the left and dark monitor on the right. No new objects, no logos, no furniture additions, no text. Do not enlarge the face to fill the frame: hair-to-bottom-of-beard should occupy only around 30% of total image height. Treat this as extending canvas and repositioning the original photograph, not photographing a new pose.
