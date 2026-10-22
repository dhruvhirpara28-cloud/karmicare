# Loop cancellation flow: NL and FR proposals

Read on 21 Oct 2026 in Loop > Settings > Multilingual content > Cancellation flow (read-only). In both NL and FR, 42 fields with English text are empty, so customers see English when they cancel. These are proposals for Victor to approve. Nobody has entered them in Loop.

Rules used:
- NL uses *je*; FR uses *vous*. Verbs follow the approved plan texts: NL "Schenken, pauzeren of opzeggen", FR "Offrir, suspendre ou résilier".
- `{{…}}` tokens stay exactly as they are.
- No "discount", "cashback" or "points" for Care Credit. "Offer" becomes NL *aanbod*, FR *offre*.
- FR avoids `:` `!` `?` where it can. They need a no-break space before them, and that space gets lost when the text is copied.
- Empty in English as well, so left out: "Cancellation instructions (HTML supported)".

Already filled in both languages and not reviewed here: the reasons (11–20, for example "I'm not seeing results yet") and "Karmicare membership benefits" (9–10). Their texts make claims ("Nano-hydroxyapatiet herbouwt het glazuur…") and need a claims check by source-copy before launch.

## Minimum orders criteria

| Field | EN | NL | FR |
|---|---|---|---|
| Title | Cancel subscription | Abonnement opzeggen | Résilier l’abonnement |
| Body | Your cancellation request cannot be completed as you are still {{min_orders_left}} orders away from fulfilling the minimum orders requirement. | Je kunt je abonnement nog niet opzeggen. Er zijn nog {{min_orders_left}} bestellingen nodig om het minimumaantal te halen. | Vous ne pouvez pas encore résilier votre abonnement. Il reste {{min_orders_left}} commandes avant d’atteindre le nombre minimum requis. |
| Button text | Cancel | Annuleren | Annuler |

## Cancellation instructions page

| Field | EN | NL | FR |
|---|---|---|---|
| Pop-up title | Cancel subscription | Abonnement opzeggen | Résilier l’abonnement |
| Button text | Close | Sluiten | Fermer |

## Minimum installment orders criteria

| Field | EN | NL | FR |
|---|---|---|---|
| Title | Cancel subscription | Abonnement opzeggen | Résilier l’abonnement |
| Body (HTML) | You will be able to cancel your subscription once {{installments_left}} more installments have been paid in this cycle. | Je kunt je abonnement opzeggen zodra in deze cyclus nog {{installments_left}} termijnen betaald zijn. | Vous pourrez résilier votre abonnement une fois que {{installments_left}} échéances supplémentaires auront été payées sur ce cycle. |
| Button text | Close | Sluiten | Fermer |

## General drawer text

| Field | EN | NL | FR |
|---|---|---|---|
| Drawer header | Cancel subscription | Abonnement opzeggen | Résilier l’abonnement |
| Keep subscription button text | Keep subscription | Abonnement behouden | Garder mon abonnement |
| Apply cancellation offer success message | Offer applied successfully. | Het aanbod is toegepast. | L’offre a bien été appliquée. |

## Cancellation reason texts

| Field | EN | NL | FR |
|---|---|---|---|
| Reason help text when selection is mandatory | Select a reason for cancelling your subscription? | Kies waarom je je abonnement opzegt. | Choisissez la raison de votre résiliation. |
| Proceed cancellation button text | Proceed to cancel | Verder met opzeggen | Continuer la résiliation |
| Reason help text | Select a reason for cancelling your subscription (optional)? | Kies waarom je je abonnement opzegt (optioneel). | Choisissez la raison de votre résiliation (facultatif). |

## Alternative actions flow

| Field | EN | NL | FR |
|---|---|---|---|
| Delay action button text | Delay | Uitstellen | Reporter |
| Skip action button text | Skip | Overslaan | Passer |
| Swap action button text | Swap | Wisselen | Échanger |
| Pause action button text | Pause | Pauzeren | Suspendre |
| Continue to cancel text | I still want to cancel my subscription | Ik wil mijn abonnement toch opzeggen | Je souhaite quand même résilier mon abonnement |
| Swap action drawer header | Swap products | Wisselen | Échanger |
| Swap action confirm button text | Confirm | Bevestigen | Confirmer |
| Swap action cancel button text | Close | Sluiten | Fermer |
| Swap action info text | Swapped with: | Gewisseld voor: | Remplacé par |
| Change frequency action text | Update delivery frequency | Leveringsfrequentie aanpassen | Modifier la fréquence de livraison |
| Swap action success message | Products have been swapped successfully. | Je wissel is gelukt. | L’échange a bien été effectué. |
| Reschedule subscription button text | Reschedule | Andere datum kiezen | Changer la date |
| Open support chat button text | Open support chat | Chat met ons openen | Ouvrir le chat d’assistance |
| Gift order button text | Gift order | Bestelling schenken | Offrir la commande |
| Redeem loyalty points button text (Loop Loyalty) | Redeem points | **Victor**: Care Credit gebruiken | **Victor**: Utiliser mon Care Credit |
| Redeem loyalty points button text (Rivo, Bubblehouse, Influence, Yotpo, Rise.ai, Okendo, Friendbuy) | Redeem points | **Victor**: Punten inwisselen | **Victor**: Utiliser mes points |

The loyalty rows are for Victor to decide. If Care Credit runs through Loop Loyalty, the Loop Loyalty button should name Care Credit and never say "points". The other integrations only show if they are switched on. Rivo is installed in the admin, so its row is the one to check.

"Swap products" is shortened to *Wisselen* / *Échanger* because the brand rules keep "product" out of customer copy.

## Available offers drawer

| Field | EN | NL | FR |
|---|---|---|---|
| Header text | Cancel subscription | Abonnement opzeggen | Résilier l’abonnement |
| Drawer body text (HTML) | Hey {{customer_first_name}}, we would hate to see you go! How about we change your mind with one of these offers? | Hoi {{customer_first_name}}, we zien je niet graag gaan. Misschien past een van deze aanbiedingen beter bij je. | Bonjour {{customer_first_name}}, nous serions désolés de vous voir partir. L’une de ces offres pourrait peut-être mieux vous convenir. |
| Show available offers button text | Show available offers | Aanbiedingen bekijken | Voir les offres |

## Cancellation remarks texts

| Field | EN | NL | FR |
|---|---|---|---|
| Cancellation remarks text | Any remarks or suggestions to help us provide you better subscription experience next time? | Heb je nog opmerkingen of tips waarmee we je abonnement beter kunnen maken? | Partagez une remarque ou une suggestion pour nous aider à améliorer votre abonnement. |
| Confirm subscription cancellation button text | Cancel subscription | Abonnement opzeggen | Résilier l’abonnement |
| Cancel subscription success message | Subscription has been cancelled. | Je abonnement is opgezegd. | Votre abonnement est résilié. |

## Entering them

In Loop, choose the language, open Cancellation flow, open each block in the left column and fill the Dutch or French column. Then press **Update** before opening the next block: switching blocks drops unsaved changes. Do not press **AI translate**.
