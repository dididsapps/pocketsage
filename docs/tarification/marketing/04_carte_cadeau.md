# Carte cadeau PocketSage — idée marketing (18/11/2026)

## Le principe
« **Offrez un an de PocketSage** » : une belle carte (PDF à imprimer ou e-carte) avec un **code** qui débloque l'abonnement Famille. Cible : grands-parents, parrains/marraines, oncles et tantes — ceux qui cherchent un cadeau « utile » et culpabilisent d'offrir encore un jouet ou un écran.

## Pourquoi ça marche pour nous
- Les **grands-parents** sont les premiers acheteurs de cadeaux éducatifs, et ils ne payent pas l'abonnement à la place des parents sans support physique : la carte fait le lien.
- Le cadeau **vient avec la promesse** : « du temps d'écran dont on n'a pas à se sentir coupable » → l'acheteur se sent bien.
- **Pas de pub vers les enfants** : on vend à des adultes, pour des adultes. Conforme.
- Chaque carte = une famille qui découvre l'appli **sans passer par l'essai** → meilleure conversion, et le renouvellement se fait au bout d'un an.

## Formats
| Format | Contenu | Prix indicatif* |
|---|---|---|
| 🎁 Carte « 1 an Famille » | code 12 mois Famille (4 profils) | 59,99 € |
| 🎁 Carte « 3 mois découverte » | code 3 mois Famille | 19,99 € |
| 💎 Carte « À vie » (édition fondateurs, quantité limitée réelle) | accès à vie | 179 € |
| 🏫 Pack écoles / associations | lot de codes à prix réduit | sur devis |
*prix à caler sur la grille de `02_offres_tunnel_vente.md`.

## La carte elle-même
- Recto : le Senseï + « Un an pour apprendre, bouger et rêver » + prénom de l'enfant.
- Verso : code, **QR code qui ouvre directement l'appli**, 3 étapes pour l'activer **par le parent**, rappel « pas de pub, pas de compte, données sur le téléphone ».
- Option : petit livret « 10 défis en famille » à imprimer avec (contenu déjà dans l'appli → coût nul).

## Calendrier
- **Noël** (pic : 1er-22 décembre) — e-carte instantanée pour les retardataires jusqu'au 24 au soir.
- **Anniversaires** (toute l'année), **Pâques**, **fin d'année scolaire** (cadeau aux maîtres/maîtresses ? → non : pas de démarchage via l'école), **rentrée**.

## Comment le faire techniquement (à valider avant de coder)
- **Apple** : codes d'offre d'abonnement (« offer codes ») générés dans App Store Connect, distribuables par nos propres canaux ; le parent les échange dans l'App Store. ⚠️ Vérifier les règles 3.1.1 / 3.1.3 sur la **vente** de ces codes hors de l'appli (site web) avant de lancer.
- **Google Play** : codes promo d'abonnement (Play Console), même logique ; mêmes vérifications.
- **Site pocketsage.org** : page « Offrir » (paiement Stripe ou boutique), envoi de la carte PDF par e-mail à l'acheteur. ⚠️ TVA (Monaco/UE), CGV, droit de rétractation, durée de validité du code (au moins 1 an), conditions claires sur la carte.

## Messages (adultes uniquement)
- « Le cadeau qui ne finit pas au fond d'un placard. »
- « Un an d'histoires du soir, de langues et de défis — pour toute la famille. »
- « Offrez du temps d'écran dont personne n'a à se sentir coupable. »
À faire relire (claims) avant publication : pas de promesse de résultats scolaires ni d'effet santé.

## Mesure
Codes vendus / codes activés (taux d'activation), renouvellement à 12 mois, familles « offertes » qui parrainent ensuite.
