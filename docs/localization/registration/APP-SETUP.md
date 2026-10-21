# App "Karmicare translations" · stappen voor Victor

Met deze app registreert `register.py` de NL- en FR-vertalingen via de Admin API (toegangspad A uit `docs/localization/B4-REPORT.md`). Jij maakt de app aan en zet het geheim in je Keychain. Niemand anders ziet het geheim, ook Claude niet. Duur: ongeveer 10 minuten.

## Vooraf: Translate & Adapt

Niet nagekeken in de echte app of de officiële documentatie. Dit komt uit de notities van de PDP-lane van 21 oktober: Shopify's „Translate now” zette op 20 oktober machinevertalingen in de winkeldata, ook op `handle_item`.

1. Open in Admin **Apps > Translate & Adapt** en kijk of er een instelling voor automatisch vertalen bestaat (de PDP-lane noemt die **Auto-sync**). Staat die aan voor NL of FR, zet hem dan uit.
2. Gebruik na de registratie geen **Translate now** meer. Volgens die notities zet het dan opnieuw machinevertalingen neer.

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

`read_metaobjects` komt er alleen bij als het rapport van de dry-run dat met zoveel woorden vraagt („metaobject fields not readable: the token lacks read_metaobjects”). Shopify heeft die metaobjectvelden dan expliciet geweigerd. Zonder die scope schrijft de runner de geneste metaobjecten (zoals de compare-tabel) niet. Met die scope maak je een nieuwe versie met de vierde scope en keur je die op de winkel goed.

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

- Hij leest het geheim met `security find-generic-password -s karmicare-translations -w` binnen zijn eigen proces. Of macOS daarbij om toestemming vraagt, hangt af van de Keychain-instelling van het item. Vraagt het, kies dan **Allow**, niet **Always Allow**.
- Hij ruilt Client ID en secret voor een Admin-token (`client_credentials`, 24 uur geldig) en houdt dat alleen in het geheugen. Elke melding, elk rapport en elke journaalregel gaat door een filter dat geheim en token verwijdert. Foutteksten van Shopify gaan alleen als code, veld en ingekorte melding naar buiten. De zelftest bewijst dat met nepwaarden. Of het ook met echte Shopify-fouten klopt, toont pas de eerste echte run.
- Eerst draait hij een **dry-run**, die alleen leest. Per mutatie toont het rapport de resource, de sleutel, de volledige Engelse tekst, de huidige NL/FR en de nieuwe tekst, zonder inkorten. Verder lijst het alles wat hij niet schrijft, met de reden: verouderd, ontbrekend, dubbelzinnig, conflict of eigenaar niet bewezen.
- De goedkeuring geldt voor die momentopname, inclusief de huidige vertalingen. Is daar intussen iets aan veranderd, dan schrijft hij niets. Vlak vóór elke mutatie leest hij de resource opnieuw. Wat iemand in de seconde daarna nog wijzigt, kan hij niet zien.
- Hij schrijft pas na jouw expliciete **ja** op dat rapport. NL en FR zijn al gepubliceerd, dus wat hij schrijft staat meteen live op `/nl` en `/fr`. Elke poging en elk resultaat komt in `live/journal-<taal>.jsonl`, ook als de run halverwege stopt.
- Loop-verkoopplannen blijven in Loop. Vertaalde `handle_item`-, `selling_plan_id`- en Subscription Name-waarden verwijdert hij alleen als de dry-run én de write allebei `--remove-never` hebben.

## Zelf draaien

Pas na de her-review van R18. Gebruik bij voorkeur je eigen Terminal, vanuit de map van de repo. `--theme-id` is de ID van het gepubliceerde thema (Online Store > Themes). Zonder die ID schrijft hij geen themateksten.

```sh
python3 docs/localization/registration/register.py --theme-id <thema-id>
```

Dat is de dry-run voor NL en FR. Het rapport staat daarna in `docs/localization/registration/live/dry-run-nl.md` en `dry-run-fr.md`, met bovenaan een controlesom en de opdracht om precies dat te schrijven. Schrijf pas als je het rapport hebt goedgekeurd, met dezelfde opties als de dry-run:

```sh
python3 docs/localization/registration/register.py --lang nl --theme-id <thema-id> --write --approve <controlesom>
```

Is de winkel, het plan of een optie intussen veranderd, dan stopt hij zonder te schrijven: draai dan eerst opnieuw de dry-run.

## Intrekken

- **Geheim gelekt:** maak in **Settings** een nieuwe client secret aan en zet die in de Keychain. Gebruik `-U` om het oude te overschrijven, met `-w` als laatste: dan vraagt de Terminal om de waarde en komt die niet in je opdrachtregel.

  ```sh
  security add-generic-password -U -s karmicare-translations -a <client id> -w
  ```

- **App niet meer nodig:** verwijder hem in Admin onder **Settings > Apps**. Het token werkt dan niet meer.
