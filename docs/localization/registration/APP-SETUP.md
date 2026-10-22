# App "Karmicare translations" · stappen voor Victor

Met deze app registreert `register.py` de NL- en FR-vertalingen via de Admin API (toegangspad A uit `docs/localization/B4-REPORT.md`). Jij maakt de app aan en zet het geheim in je Keychain. Niemand anders ziet het geheim, ook Claude niet. Duur: ongeveer 10 minuten.

## Vooraf: Translate & Adapt

1. Open in Admin **Apps > Translate & Adapt**.
2. Zet **Auto-sync** (automatisch vertalen) uit voor NL en FR.
3. Gebruik vanaf nu geen **Translate now** meer. Anders overschrijft Shopify de goedgekeurde vertalingen weer met machinevertalingen.

## 1. App aanmaken

1. Ga naar [dev.shopify.com/dashboard](https://dev.shopify.com/dashboard) en log in met je Karmicare-account.
2. Kies de organisatie **Karmicare**.
3. **Apps > Create app**, kies **Start from Dev Dashboard** en noem de app **Karmicare translations**.

De namen van knoppen kunnen iets afwijken. De volgorde blijft: app maken, versie met scopes, release, installeren.

## 2. Versie met scopes

1. Open **Versions** en maak een nieuwe versie.
2. Zet bij **Access scopes** precies deze drie:
   - `read_translations`
   - `write_translations`
   - `read_products`
3. De app heeft geen eigen pagina's. Vraagt het formulier een App URL, laat dan de voorgestelde waarde staan.
4. Klik **Release**.

`read_metaobjects` komt er alleen bij als de eerste dry-run meldt dat hij metaobjecten niet kan lezen. Dan maak je een nieuwe versie met die vierde scope en keur je die op de winkel goed.

## 3. Installeren op de winkel

1. Open de app en klik **Install app**.
2. Kies **karmicares.myshopify.com** en keur de drie scopes goed.

## 4. Geheim in de Keychain

1. Open in de app **Settings** (of **Credentials**) en kopieer de **Client ID**. Die is niet geheim.
2. Open de Terminal-app van je Mac. Gebruik niet de Claude-sessie of `!`: het geheim mag niet in een transcript belanden.
3. Typ, met je eigen Client ID in plaats van `<client id>`:

   ```sh
   security add-generic-password -s karmicare-translations -a <client id> -w
   ```

4. De Terminal vraagt twee keer om het wachtwoord. Plak daar de **Client secret** uit het Dev Dashboard. Je ziet niets verschijnen, dat is normaal.
5. Controleer, zonder het geheim te tonen:

   ```sh
   security find-generic-password -s karmicare-translations
   ```

   Je ziet `"svce"<blob>="karmicare-translations"` en je Client ID bij `"acct"`. Het wachtwoord zelf staat er niet bij.
6. Meld aan de desk: "app klaar". Stuur het geheim nooit mee.

## Wat de runner daarna doet

- Hij leest het geheim met `security find-generic-password -s karmicare-translations -w` binnen zijn eigen proces. macOS kan je vragen dat toe te staan: kies **Allow**, niet **Always Allow**.
- Hij ruilt Client ID en secret voor een Admin-token (`client_credentials`, 24 uur geldig) en houdt dat alleen in het geheugen. Hij print en bewaart geen geheim of token.
- Eerst draait hij een **dry-run**, die alleen leest. Het rapport laat zien wat nieuw is, wat overschreven wordt (met de huidige NL/FR ernaast) en wat hij overslaat.
- Hij schrijft pas na jouw expliciete **ja** op dat rapport. NL en FR zijn al gepubliceerd, dus wat hij schrijft staat meteen live op `/nl` en `/fr`.
- Loop-verkoopplannen blijven in Loop. Vertaalde `handle_item`- en `selling_plan_id`-waarden verwijdert hij alleen na jouw ja.

## Zelf draaien (als Claude's sandbox Keychain of netwerk blokkeert)

Vanuit de map van de repo, in je eigen Terminal of in de Claude-sessie met `!` ervoor (de runner print geen geheimen):

```sh
python3 docs/localization/registration/register.py
```

Dat is de dry-run voor NL en FR. Het rapport staat daarna in `docs/localization/registration/live/dry-run-nl.md` en `dry-run-fr.md`, met onderaan een controlesom en de opdracht om precies dat te schrijven. Schrijf pas als je het rapport hebt goedgekeurd:

```sh
python3 docs/localization/registration/register.py --lang nl --write --approve <controlesom>
```

Is de winkel intussen veranderd, dan stopt hij zonder te schrijven: draai dan eerst opnieuw de dry-run.

## Intrekken

- **Geheim gelekt:** maak in **Settings** een nieuwe client secret aan en zet die met dezelfde opdracht in de Keychain (voeg `-U` toe om te overschrijven).
- **App niet meer nodig:** verwijder hem in Admin onder **Settings > Apps**. Het token werkt dan niet meer.
