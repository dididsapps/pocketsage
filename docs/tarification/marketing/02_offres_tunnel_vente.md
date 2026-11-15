# Offres, tunnel de vente et fuites de ventes : PocketSage Academy (15/11/2026)

> Document de travail pour compléter `docs/tarification/README.md`. **Rien n'est décidé ni codé** : les prix sont des propositions à tester, et ce document ne remplace pas la relecture d'un juriste, déjà prévue au README §7 et §8.
> Il tient compte de `00_contexte.md`, de `docs/jeux/economie.md`, de la compétence marketing-pocketsage, de la notice parents (`guide_parents.pdf` / `docs/parents/notice_parents.html`) et de la présentation `Mon_Monde_presentation.pdf`.
> Objectif de Mario : **ne pas louper une vente, légalement.** Le fil conducteur : on vend au **parent**, au bon moment, avec un prix clair, et on ne perd aucun acheteur pour une raison technique.

---

## 0. Résumé en 10 lignes

1. **Grille proposée (FR/UE/Monaco, TTC)** : Gratuit (option B : Aventure du jour, 5 min de découverte, jeux 15 min, sport et fiches libres). **Solo** 5,99 €/mois ou 39,99 €/an. **Famille** (4 profils) 9,99 €/mois ou **59,99 €/an, soit « 5 € par mois pour toute la famille »**. **Premium** 13,99 €/mois ou 99,99 €/an. **Famille à vie** 179 €.
2. **Fondateurs (bêta-testeurs réels)** : Famille annuelle à **39,99 €/an, prix garanti tant que l'abonnement reste actif**, ou Famille à vie à 119 €. Liste fermée et date limite réelle.
3. Essai : **7 jours** sur l'abonnement Famille. Test prévu contre 14 jours, car les essais longs convertissent mieux (voir §1.4). L'essai doit rester **disponible plus tard** : en Éducation, environ 1 essai sur 4 démarre plus de 30 jours après l'installation.
4. Tunnel : 1ʳᵉ ouverture « À faire par un adulte » → écran d'offre avec un bouton **« Continuer en gratuit »** bien visible → l'offre revient ensuite **uniquement dans l'Espace Parents**, au moment où elle sert (limite atteinte, bilan hebdomadaire, réglage verrouillé).
5. Fuites n°1 à 5 : pas de **restauration d'achat** et pas de **partage entre les appareils de la famille** ; **échecs de paiement** sans période de grâce (31 % des résiliations Google Play) ; **essai proposé une seule fois** ; **pas d'offre annuelle** (ou annuelle mal mise en avant) ; **abonné bloqué hors ligne**.
6. Bloquant juridique n°1 : **aucune sollicitation d'achat côté enfant**, notifications comprises ; barrière parentale avant tout écran d'achat ou lien externe (Apple 1.3, Google Familles, directive 2005/29/CE annexe I point 28).
7. Bloquant juridique n°2 : **écran d'offre et essai transparents**. Il doit indiquer le montant facturé, la durée, le renouvellement automatique, la date du premier prélèvement et comment annuler. Interdits : faux prix barré et fausse urgence (annexe I point 7). Vente sur le web : renonciation expresse au droit de rétractation, bouton « résilier » en 3 clics et rappel avant la reconduction annuelle (L215-1).
8. Bloquant juridique n°3 : **SDK et données**. La brique d'abonnement ne doit envoyer ni identifiant publicitaire ni identifiant d'appareil (règles Familles/Kids). Il faut aussi un contrat de traitement (DPA), une mise à jour de la politique de confidentialité et de la notice (aujourd'hui « données sur le téléphone »), et COPPA avant tout lancement aux États-Unis.
9. Mesures : uniquement des **compteurs agrégés anonymes** (vues d'offre par emplacement, essais, achats, restaurations…). La conversion et le churn viennent des stores et de RevenueCat, jamais d'un profil d'enfant.
10. À coder en priorité : enveloppe **Capacitor** pour les stores, puis **RevenueCat** (ou facturation native), une **couche de droits avec cache hors ligne**, l'**écran d'offre** derrière la barrière parentale, la **restauration** et le **lien « Gérer mon abonnement »**, et les limites du gratuit. Environ 15 à 25 jours de travail pour la version vendable (§5).

---

## 1. Repères marché et benchmarks (sources §7)

### 1.1 Prix des concurrents (TTC, relevés 2026, à revérifier avant toute communication chiffrée)

| Appli | Mensuel | Annuel | Profils / cible | Remarque |
|---|---|---|---|---|
| Kartable (FR, soutien scolaire) | 14,99 € (1 enfant), 24,99 € (3 enfants) | 119,99 € (1 enfant), 179,99 € (3 enfants) | CP → Terminale | Tarifs par nombre d'enfants : c'est la référence « soutien scolaire » des parents FR |
| Lingokids Plus | 14,99 $ | ≈ 72-90 $ (doc concurrents) | 2-8 ans | Cher, réservé aux petits |
| Super Duolingo Famille | ≈ 10,25 € | 122,99 € | 6 comptes | Le benchmark « famille » |
| Bayam (Bayard) | 5,99 € | 49,99 € | 3-10 ans | Marque jeunesse FR, prix bas |
| Whisperies | 5,99 € | 59 € | enfants | Histoires |
| Audible Kids / Sybel | 9,95-9,99 € | — | | Audio |
| Khan Academy Kids | gratuit | gratuit | 2-8 ans | Concurrent « gratuit » à neutraliser par l'argument 4-18 ans + multilingue |
| Applis anti-scroll adultes (Headway, Imprint, Nibble…) | 12-20 $ | 70-240 $ **par personne** | adultes | voir `docs/flash/01_concurrents_antiscroll.md` |

**Lecture** : avec 9,99 €/mois et 59,99 €/an pour 4 profils, PocketSage est **moins cher que Kartable pour un seul enfant** (119,99 €/an) et **moins cher que Duolingo Famille** (122,99 €/an), tout en couvrant plus de matières et l'audio en ≈ 20 langues. Cela respecte la piste du README §1 : « abonnement famille sous le prix individuel des concurrents ».

### 1.2 Benchmarks de conversion (catégorie Éducation sauf mention contraire)

| Indicateur | Valeur | Source |
|---|---|---|
| Prix médian annuel Éducation | **44,99 $** (le plus élevé de toutes les catégories) | RevenueCat SOSA 2026 |
| Prix médian mensuel Éducation | **9,99 $** | RevenueCat SOSA 2026 |
| Prix médians mondiaux Éducation | 7,48 $/semaine, 12,99 $/mois, 38,42 $/an | Adapty SOIS 2026 |
| Téléchargement → essai (J30) | 6,5 % (RevenueCat) ; installation → essai 10,9 % (Adapty) | RC 2026, Adapty 2026 |
| Téléchargement → payant (J35, iOS) | **3,1 %** médian Éducation ; 12-14 % pour les meilleurs | RevenueCat 2026 |
| Essai → payant | 25,6 % (moyenne Adapty Éducation) | Adapty 2026 |
| Essais démarrés le jour de l'installation | 78,5 % (RC), 71,3 % (Adapty) : **le plus bas de toutes les catégories** | RC, Adapty |
| Essais démarrés **plus de 31 jours** après l'installation | **23,5 %**, le plus haut de toutes les catégories | Adapty 2026 |
| Durée d'essai la plus fréquente | 5-9 jours (50,3 %) ; beaucoup de conversions vers J7 | RevenueCat 2026 |
| Essais longs vs courts (toutes catégories) | 17-32 jours : 42,5 % de conversion ; moins de 4 jours : 25,5 % | RevenueCat 2026 |
| Annulations d'un essai de 3 jours le jour même | 55,4 % | RevenueCat 2026 |
| Valeur sur 12 mois avec ou sans essai | Les utilisateurs passés par un essai rapportent **+50,4 %** | Adapty 2026 |
| Part du « paiement unique » (à vie) dans les revenus Éducation | 17 % en 2025 (6 % en 2023) | Adapty 2026 |
| Annulations d'annuels au 1er mois | ≈ 30 % des annulations annuelles en Éducation (35 % toutes catégories) | RevenueCat 2026 |
| Résiliations dues à un **échec de paiement** | **Google Play 31 %**, App Store 14 % | RevenueCat 2026 |
| Paywall strict vs freemium (toutes catégories) | Conversion J35 de 10,7 % contre 2,1 % ; revenu par installation à J60 de 3,09 $ contre 0,38 $ ; **rétention annuelle identique** (27 % contre 28 %) | RevenueCat 2026 |
| Europe vs Amérique du Nord | L'Europe facture 29 à 39 % plus cher | Adapty 2026 |

**Conséquences pour PocketSage**
- Un freemium sans offre visible convertit très mal (2,1 %). Il faut une **offre d'essai forte à la 1ʳᵉ ouverture** (le parent est là), tout en gardant un vrai gratuit, conformément aux engagements « sans pression ».
- Les parents décident lentement en Éducation : **ne jamais retirer l'essai** à ceux qui ont dit « plus tard ».
- L'**annuel** est le cœur du modèle : c'est l'Éducation qui vend le plus d'annuels, et ce sont eux qui retiennent le mieux.
- Le **premier mois** d'un abonné annuel est décisif : bilan hebdomadaire, conseils, « 1ʳᵉ semaine réussie ».

### 1.3 Ordre de grandeur (simulation, pas une prévision)

| Pour 10 000 installations | Prudent | Médian | Bon |
|---|---|---|---|
| Parents qui terminent la 1ʳᵉ ouverture | 50 % | 65 % | 80 % |
| Essais démarrés (J0 + plus tard) | 6 % | 11 % | 18 % |
| Essai → payant | 25 % | 35 % | 45 % |
| **Abonnés payants** | **150** | **385** | **810** |
| Revenu brut annuel (panier moyen ≈ 55 €) | ≈ 8 k€ | ≈ 21 k€ | ≈ 45 k€ |
| Net après commission store de 15 % (Small Business Program Apple, abonnements Google) | ≈ 7 k€ | ≈ 18 k€ | ≈ 38 k€ |

### 1.4 Durée d'essai
- **Démarrer avec 7 jours.** C'est cohérent avec l'Éducation, et un bilan hebdomadaire tombe juste avant la fin de l'essai.
- **Test n°1 : 7 jours contre 14 jours.** Le parent voit alors 2 bilans et la ville a le temps de grandir. Les données RevenueCat montrent que les essais longs convertissent mieux. Comme on rappelle l'échéance au parent, l'essai long n'est pas un « piège ».
- Jamais d'essai de 3 jours : il produit beaucoup d'annulations le jour même et donne une impression de piège.

---

## 2. Grille d'offres recommandée

### 2.1 Les formules

| Formule | Contenu | Mensuel | Annuel | À vie | Fourchette à tester |
|---|---|---|---|---|---|
| **Gratuit** | Option B du README §6 : **Aventure du jour** (10/15/20 min selon l'âge) + **5 min/jour de découverte** de n'importe quel module + **jeux 15 min/jour** + **sport et fiches PDF libres**. Tous les profils (jusqu'à 4), pour que la fratrie essaie. Mon Monde accessible avec les pièces gagnées. Prononciation standard (reconnaissance du téléphone). | 0 € | 0 € | — | A/B : option A (module du jour) contre option B |
| **Solo** | Tout PocketSage **pour 1 profil** (les autres profils restent en gratuit), hors-ligne complet, jeux 45 min réglables, bilan hebdomadaire | **5,99 €** | **39,99 €** (−44 %) | — | 4,99-6,99 € / 34,99-49,99 € |
| **Famille** ⭐ (mise en avant) | Tout PocketSage pour **4 profils** (le maximum actuel de l'appli), partage entre les appareils de la famille (Partage familial Apple + « Code Famille », voir §5) | **9,99 €** | **59,99 €** (−50 %, « 5 €/mois pour toute la famille ») | **179 €** | 7,99-10,99 € / 49,99-79,99 € / 149-249 € |
| **Premium** (ex-« Famille+ ») | Famille + **prononciation évaluée précisément** (note par mot et par son, README §3) + futurs services coûteux (dialogues Sensei avancés…) | **13,99 €** | **99,99 €** | — (pas d'à vie : coût récurrent par usage) | 11,99-14,99 € / 89,99-119,99 € |

**Justification**
- **Solo à 5,99 € et Famille à 9,99 €** (« un peu sous le double ») respectent le brief de `00_contexte.md`. L'écart annuel est volontairement faible (39,99 € contre 59,99 €) pour que la Famille soit le choix évident : c'est un effet de contraste assumé, avec deux offres réelles.
- L'**annuel à −50 %** pousse vers la formule qui retient le mieux, et le message « 5 € par mois pour toute la famille » est simple et vrai.
- Le **Premium** sert d'**ancre haute réelle** et finance le coût Azure. Le README §3 a jugé ce coût trop élevé pour l'instant : on ne l'ouvre que quand le coût par abonné est mesuré (README §5). **Avant cela, ne pas afficher de Premium « bientôt »** au prix fixé.
- La **Famille à vie à 179 €** (≈ 3 ans d'annuel) correspond à une demande réelle en Éducation (17 % des revenus en paiement unique) et rassure les parents allergiques aux abonnements. Elle exclut les services à coût variable (Premium). Les conditions doivent être claires : « à vie » = tant que l'appli est exploitée, mises à jour de contenu incluses, Premium non inclus. Sur Apple, c'est un achat « non-consumable » partageable en famille.
- **Pas de formule hebdomadaire.** Elle rapporte beaucoup ailleurs (Adapty), mais elle est perçue comme agressive : on joue la confiance, c'est la plainte n°1 contre les concurrents.

### 2.2 Prix d'ancrage (légaux)

| Ancre | Formulation | Légalité |
|---|---|---|
| Mensuel × 12 contre annuel | « 59,99 €/an, soit 5 €/mois au lieu de 9,99 € en mensuel (−50 %) » | ✅ Compare deux offres **réellement vendues**. Le montant facturé (59,99 €) doit rester l'élément de prix **le plus visible** (exigence Apple pour les abonnements). |
| Premium affiché à côté | Présentation en 3 colonnes, Famille au centre | ✅ À condition que le Premium soit réellement achetable |
| Comparaison concurrents | « Moins cher qu'un soutien scolaire pour un seul enfant » | ⚠️ Possible (publicité comparative, L122-1 code conso) seulement si elle est **objective, vérifiable et datée**. Plutôt dans le marketing que dans l'appli. |
| Prix barré fictif (« ~~149 €~~ 59,99 € ») | — | ❌ Interdit si ce prix n'a jamais été pratiqué : pratique trompeuse (L121-2, directive 2005/29/CE), et Apple 2.3.1 sur les faux prix. En cas de vraie promotion, prendre par prudence comme prix de référence **le plus bas des 30 derniers jours** (règle « Omnibus » L112-1-1, écrite pour les biens, mais la DGCCRF regarde les réductions de prix de près). |
| Prix par jour | « 0,16 €/jour pour toute la famille » | ⚠️ Autorisé si exact et **secondaire** par rapport au montant facturé |

### 2.3 Prix de lancement « Membres fondateurs » (bêta-testeurs réels)

| Offre | Prix | Mécanique | Conditions de légalité |
|---|---|---|---|
| **Famille fondateur annuel** (recommandé) | **39,99 €/an, prix garanti tant que l'abonnement reste actif** | Produit séparé « famille_fondateur_annuel », accessible par **code d'offre** (Apple offer codes / codes promo Google) ou lien dans l'Espace Parents des testeurs | Liste fermée et réelle (familles ayant testé la bêta), date limite d'activation réelle (ex. 31/01/2027). Le prix garanti est **écrit** dans les conditions. Ne jamais l'appeler « dernière chance » si l'offre est rouverte ensuite. |
| Famille fondateur à vie (option) | 119 € | Achat unique par code | Même chose. Nombre de places réel si on l'annonce (« 100 places » = 100). |
| Bonus fondateur | Badge « Fondateur » dans l'Espace Parents (côté parent, pas un avantage de jeu pour l'enfant) | Local | Pas d'avantage payant visible par l'enfant dans Mon Monde |

**Prix de lancement public** (option) : « Famille 49,99 € la 1ʳᵉ année jusqu'au 31/03/2027 » via une offre d'introduction (Apple « introductory offer », Google « offre de bienvenue »). C'est légal **si la date est vraie** et si le prix normal (59,99 €) est clairement indiqué pour le renouvellement. Il faut choisir entre essai gratuit et prix d'introduction (Apple : une seule offre d'introduction par groupe d'abonnements). **Recommandation : garder l'essai gratuit, plus fort, et réserver les réductions aux fondateurs, au parrainage et à la reconquête.**

**Engagement à afficher** : « **Votre prix ne bougera pas tant que vous restez abonné.** » Cela crée la confiance et évite les hausses de prix, qui demandent l'accord de l'abonné dans de nombreux pays.

### 2.4 Pays, devises et parité de pouvoir d'achat

| Zone | Pays (exemples) | Famille mensuel / annuel | Règle |
|---|---|---|---|
| **Base** | France, **Monaco**, Belgique, Luxembourg, Suisse (≈ 9,90 CHF / 59 CHF), Allemagne, Autriche, Pays-Bas, Irlande, pays nordiques, Royaume-Uni (≈ 8,99 £ / 54,99 £) | 9,99 € / 59,99 € | Prix fixés à la main, terminaisons propres (,99) |
| **Amérique du Nord / Océanie** | États-Unis, Canada, Australie | 9,99 $ / 59,99 $ (CA et AU dans leur devise) | **États-Unis seulement après conformité COPPA** (règle modifiée en vigueur, mise en conformité au 22/04/2026) |
| **Europe du Sud et de l'Est** | Espagne, Italie, Portugal, Grèce, Pologne, Tchéquie, pays baltes, Roumanie… | −20 à −30 % (≈ 7,99 € / 44,99 €) | Les stores convertissent automatiquement : on ajuste à la main |
| **Pouvoir d'achat faible** | Maghreb, Turquie, Ukraine, Brésil, Mexique, Inde, Asie du Sud-Est, Égypte, pays du Golfe à part | −50 à −70 % | Utiliser les suggestions de prix locaux de Google Play et l'égalisation d'Apple, puis vérifier. Les familles expatriées ou bilingues paient dans le pays de leur compte store. |
| **Exclus** | **Russie, Chine** (règle non négociable), plus les pays sous sanctions | — | Décocher dans App Store Connect et la Play Console |

- **Monaco** : même prix que la France. La TVA française (20 %) s'applique à Monaco, et ce sont les stores qui la collectent et la reversent. Vérifier que Monaco est coché comme pays de distribution (il n'a pas toujours de vitrine distincte : beaucoup de Monégasques ont un compte store français).
- **Droit applicable** : Mario est installé à Monaco, mais si l'on vise des consommateurs de l'UE, c'est **le droit de la consommation de leur pays** qui protège ces clients (règlement Rome I, art. 6). On applique donc le **standard FR/UE partout**. Pour la loi monégasque (loi n° 1.565 du 3/12/2024 sur les données, autorité APDP, amendes jusqu'à 10 M€), faire valider la conformité par un avocat local.

---

## 3. Tunnel de vente étape par étape

**Principes transversaux**, valables à chaque étape :
- (a) **Côté enfant : jamais d'offre, de prix, de cadenas « payant », ni de « demande à tes parents ».**
- (b) Toute offre passe **derrière la barrière parentale** (déjà codée pour le « Code oublié ? »).
- (c) **Pas plus d'une offre proactive par visite** de l'Espace Parents, et au maximum une tous les 3 jours. Google se réserve de retirer les applis aux « tactiques commerciales trop agressives ».
- (d) Toujours un bouton **« Continuer en gratuit » / « Plus tard »** aussi lisible que le bouton d'achat.
- (e) Cohérence avec la présentation Mon Monde : **aucun minuteur payant, aucun coffre, aucune pièce vendue contre de l'argent réel**, et l'abonnement n'accélère jamais la ville.

| # | Point de contact | Ce qu'on fait (pour ne pas louper la vente) | ✅ Autorisé | ❌ Interdit, et pourquoi |
|---|---|---|---|---|
| 1 | **Page store** (fiche Google Play / App Store) | Captures orientées parents (« Le temps d'écran dont tu n'as pas à te sentir coupable »), mention claire « Gratuit avec abonnement facultatif, essai 7 jours », les 4 profils, sans pub, hors-ligne | Décrire honnêtement les achats intégrés | Faux avis ou notes achetées (compétence marketing, Apple 3.2.2(x)) ; promesses médicales ou diagnostics (TDAH/dys) ; nom des fournisseurs techniques |
| 2 | **1ʳᵉ ouverture : « À faire par un adulte (2 min) »** | Barrière parentale → code PIN → profils → **écran d'offre** (Famille annuel présélectionné, essai 7 jours) → « Continuer en gratuit » → email facultatif pour le bilan, avec une **case séparée non cochée** pour les offres | Présélectionner un plan **dans un choix entre plans** ; expliquer ce que débloque l'abonnement | Exiger un email ou cocher la case « offres » pour utiliser le gratuit (RGPD art. 7 §4, README §8) ; cacher le bouton « gratuit » ou le rendre gris pâle (dark pattern, futur Digital Fairness Act) ; enchaîner 25 écrans avant l'offre |
| 3 | **Écran d'offre** (paywall, voir détail §3.1) | 3 formules max, bascule mensuel/annuel, bénéfices concrets (« 4 enfants, toutes les matières, hors-ligne »), **date du 1er prélèvement en clair**, « Annulable à tout moment depuis votre compte Google/Apple », bouton **Restaurer mes achats**, liens Conditions et Confidentialité | Mettre en avant l'annuel ; un vrai témoignage de testeur (autorisation écrite) | Fausse urgence (« offre expire dans 10:00 » si faux : directive 2005/29/CE annexe I pt 7) ; faux prix barré ; montant facturé moins visible que le « prix par mois » (règle Apple) ; culpabilisation (« Vous ne voulez pas que votre enfant réussisse ? ») = confirmshaming, interdit par le futur DFA et par les règles Familles de Google sur les tactiques émotionnellement manipulatrices |
| 4 | **Pendant l'essai** | J1 : « Premiers pas » dans l'Espace Parents. J3 : astuce « faites-vous visiter la ville ». J6 : **bilan hebdomadaire** (in-app + email si donné) | Informer des progrès (donnée calculée sur le téléphone) | Messages visibles par l'enfant sur l'essai ou le paiement |
| 5 | **Rappel avant fin d'essai (J-2)** | Bandeau dans l'Espace Parents : « Votre essai se termine le **jj/mm**. Ensuite 59,99 €/an. [Garder Famille] [Gérer / annuler] ». Email de **service** si le parent a donné son email (information sur le contrat, pas de la prospection). Notification locale **neutre** seulement si le parent l'a activée : « Information pour le parent : ouvrez l'Espace Parents ». | Rappel transactionnel ; lien direct vers la gestion de l'abonnement | Notification promotionnelle sans accord explicite (Apple 4.5.4) ; texte de notification lisible par l'enfant parlant d'argent |
| 6 | **Fin d'essai non convertie** | Retour au gratuit **sans perte de données** : progrès, ville et décorations restent. Message parent : « Vous êtes repassé en version gratuite. Tout est conservé. » L'offre reste accessible dans l'Espace Parents. | | Menacer de supprimer la ville ou les progrès (manipulation émotionnelle, chantage affectif via l'enfant) ; relances quotidiennes |
| 7 | **Limite gratuite atteinte (côté enfant)** | Enfant : « Bravo, séance terminée ! Montre à tes parents ce que tu as appris aujourd'hui. À demain ! » (formule validée au README §8). Parent, à sa prochaine visite de l'Espace Parents : « Léa a atteint la limite gratuite 3 fois cette semaine. » + [Voir les formules] | Compter les limites atteintes **sur le téléphone** | « Demande à tes parents de débloquer » (annexe I pt 28) ; cadenas « Premium » sur les modules ou bâtiments côté enfant ; vendre des minutes supplémentaires |
| 8 | **Réglage verrouillé dans l'Espace Parents** | Ex. « Jeux 45 min / illimité », « 2ᵉ langue », « Fiches illimitées » → petite fiche « Inclus dans Famille » + bouton vers l'offre | Mini-offre contextuelle (le moment où le parent veut la fonction) | |
| 9 | **Bilan hebdomadaire** (Espace Parents + email facultatif) | Progrès réels + une ligne neutre « Ce que Famille ajouterait : … » + lien vers l'Espace Parents | Mention neutre dans un email de service (README §7) | Bilan transformé en email publicitaire sans la case « offres » cochée (prospection par email sans accord préalable : L34-5 CPCE / CNIL) |
| 10 | **Abonné mensuel → annuel** | Après le 2ᵉ ou 3ᵉ renouvellement mensuel : carte « Passez à l'annuel : 59,99 € au lieu de 119,88 € par an ». Changement de formule dans le même groupe d'abonnements, pris en charge par le store, sans double facturation. | Offre promotionnelle aux abonnés existants (Apple promotional offers / Google) | Faire souscrire deux formules en même temps par erreur (Apple 3.1.2(b)) |
| 11 | **Annulation** (gérée par le store) | Détection du « ne sera pas renouvelé » → dans l'Espace Parents : « Votre abonnement s'arrête le jj/mm, vous gardez tout jusque-là. » Proposer **sans bloquer** : passer en Solo, ou mini-question anonyme « Pourquoi ? » (facultative). Sur Google : offres de rétention dans le parcours d'annulation du Play Store (annoncées en 09/2026). | Offre de rétention ou passage à une formule moins chère | Compliquer l'annulation (plainte n°1 contre les concurrents ; pour la vente web, L215-1-1 « résiliation en 3 clics ») ; questionnaire obligatoire |
| 12 | **Reconquête (abonnement expiré)** | **Offres de reconquête natives** : Apple « win-back offers » (affichées par l'App Store et dans l'appli) et Google « winback offers ». Ex. « Revenez : 3 mois à 50 % ». Email uniquement si case « offres » cochée. Périodes clés : rentrée (fin août), avant le Brevet ou le Bac, vacances (mode voiture). | Offres natives des stores, ciblées sur le statut d'abonnement (pas sur l'enfant) | Email de relance à ceux qui n'ont pas consenti aux offres ; « Ton enfant est triste » |
| 13 | **Offrir un abonnement / carte cadeau** | (a) **Dans l'appli** (Espace Parents, barrière parentale) : achat d'un « Pass Famille 12 mois cadeau » non renouvelable → code à offrir. (b) **Sur le site** pocketsage.org : vente web de codes cadeaux (Noël, anniversaires, grands-parents). (c) **Cartes physiques** (salons, librairies). Activation du code dans l'Espace Parents. | Apple 3.1.1 autorise le cadeau d'éléments achetables en IAP ; les cartes cadeaux **physiques** peuvent être vendues hors IAP. Vente web + utilisation dans l'appli possible (3.1.3(b), multiplateforme) si l'offre existe aussi en IAP. | Outre les États-Unis : **lien ou bouton dans l'appli vers l'achat web** (Apple 3.1.1(a)) ; vendre une carte cadeau numérique *dans l'appli* hors IAP |
| 14 | **Parrainage famille** | Espace Parents → « Offrez 1 mois à une famille amie » : **le parent partage lui-même** un code via la feuille de partage du téléphone (barrière parentale). Le filleul reçoit 1 mois Famille, le parrain 1 mois offert à la 1ʳᵉ conversion du filleul (droits promotionnels accordés par RevenueCat, valables sur les deux stores). | Parrainage d'adulte à adulte ; récompense **en plus** de ce qui a été payé | « Invite tes copains » côté enfant (annexe I pt 28, Apple 1.3) ; collecter l'email de l'ami pour lui écrire (prospection sans consentement) ; conditionner l'accès payé à une tâche (Apple 3.1.2(a)) ; faux parrainages |
| 15 | **Écoles, enseignants, orthophonistes (B2B)** | Licence vendue **hors appli, sur devis ou facture** et activée par **code d'établissement**. Pistes : enseignant 39 € TTC/an (mode classe sur une tablette ou au vidéoprojecteur) ; école 2-3 €/élève/an (minimum 99 €) ; **orthophoniste ou cabinet 79 €/an** (« mode séance » sans enregistrer de nom de patient). Public : plus tard via le **GAR** (accès aux ressources numériques de l'Éducation nationale). Google : vente de « places » multiples (achat multi-quantités annoncé en 09/2026). | Apple 3.1.3(c) : un service vendu à une organisation pour ses élèves ou employés peut se payer hors IAP | Faire recommander l'abonnement payant aux parents par l'enseignant en école publique (principe de **neutralité commerciale** de l'école, à vérifier avec un juriste) ; pour les orthophonistes, toute allégation thérapeutique (« traite la dyslexie ») : rester sur « support ludique de prononciation et de vocabulaire » ; prénoms de patients enregistrés, qui deviennent des données de santé indirectes |
| 16 | **Soutien scolaire / examens** | **« Pass Révisions 3 mois »** non renouvelable (ex. 19,99 €) pour Brevet, Bac ou contrôles : c'est pour les parents qui refusent tout abonnement. Message saisonnier dans l'Espace Parents (avril-juin). | Offre non renouvelable (Apple « non-renewing subscription », Google « forfait prépayé ») | Annoncer un **crédit d'impôt de 50 %** : il est réservé aux cours **à domicile**, pas aux applis ; promettre « +2 points de moyenne » sans preuve |
| 17 | **Vente sur le web** (PWA actuelle, phase 2) | Paiement web (RevenueCat Web Billing/Stripe, ou un intermédiaire « marchand de référence » comme Paddle qui gère la TVA UE) pour les familles qui utilisent la PWA, sans commission store. Droits partagés avec l'appli via le Code Famille. | Communiquer **hors de l'appli** (site, réseaux, email consenti) sur l'achat web (Apple 3.1.3) | Dans l'appli store hors États-Unis : bouton ou lien vers le paiement web (Apple 3.1.1(a), Google Payments). Sur le web : oublier le **bouton « Résilier »** (L215-1-1), la **renonciation expresse au droit de rétractation** de 14 jours pour un accès immédiat (L221-28 13°), le **rappel 1 à 3 mois avant la reconduction annuelle** (L215-1) |

### 3.1 Détail de l'écran d'offre (contenu obligatoire)

| Élément | Exigence | Source |
|---|---|---|
| Nom et durée de chaque formule, **montant facturé** par période | Obligatoire, montant facturé le plus visible | Apple 3.1.2(c) + annexe 2 du contrat développeur ; Google règles abonnements ; L221-5 code conso |
| Durée de l'essai, **date et montant du 1er prélèvement** | Obligatoire | Apple 3.1.2(a), Google, futur DFA (confirmation active envisagée) |
| Renouvellement automatique + « annulable à tout moment dans Google Play / l'App Store » + lien d'aide | Obligatoire | Apple, Google, L221-5 |
| **Restaurer mes achats** | Obligatoire en pratique (Apple 3.1.1 : « restore mechanism ») | Apple |
| Liens Conditions d'utilisation et Politique de confidentialité | Obligatoire | Apple, Google |
| Ce que contient la formule, concrètement | Obligatoire | Apple 3.1.2(c) |
| Bouton « Continuer en gratuit » visible | Choix libre (pas de dark pattern) | DFA, 2005/29 |
| Langue du parent (≈ 20 langues de l'appli) | Fortement recommandé (conversion) | — |
| Prix **localisés** fournis par le store (ne jamais écrire « 9,99 € » en dur) | Indispensable : le prix affiché doit être celui que le store facturera | Apple, Google |

---

## 4. Liste des « fuites de ventes » et parades

Classement : **impact** (🔴 fort, 🟠 moyen, 🟡 faible) × fréquence chez les applis d'abonnement.

| # | Fuite | Impact | Parade PocketSage |
|---|---|---|---|
| 1 | **Pas de « Restaurer mes achats »** : nouveau téléphone ou réinstallation → le parent croit devoir repayer, demande un remboursement ou met 1★ | 🔴 | Bouton sur l'écran d'offre + dans l'Espace Parents ; restauration automatique silencieuse au démarrage (RevenueCat) |
| 2 | **Appareils de la famille non couverts** : l'enfant a sa tablette, sur un compte Google enfant (Family Link) ou un autre identifiant Apple → l'abonnement « Famille » ne marche pas chez lui | 🔴 | Activer le **Partage familial Apple** sur les produits (⚠️ irréversible une fois activé). Côté Android, pas d'équivalent fiable pour les abonnements, donc **« Code Famille »** : QR code affiché dans l'Espace Parents de l'appareil payeur, scanné sur l'autre appareil, qui lie un identifiant anonyme (sans email ni compte). Limiter à 5 appareils. |
| 3 | **Échec de paiement** (carte expirée) → résiliation involontaire : 31 % des résiliations sur Google Play | 🔴 | Activer la **période de grâce** (Apple, à activer dans App Store Connect ; Google, par défaut, plus la « suspension de compte ») ; bandeau parent « Mettez à jour votre moyen de paiement » (Google In-App Messaging API, Apple message de facturation) ; accès maintenu pendant la grâce |
| 4 | **Essai proposé une seule fois** (à l'onboarding) : en Éducation, 23,5 % des essais démarrent après 31 jours | 🔴 | Essai disponible en permanence dans l'Espace Parents tant que le compte store y a droit ; déclencheurs §3 (limite atteinte, bilan, réglage verrouillé) |
| 5 | **Pas d'annuel, ou annuel mal mis en avant** | 🔴 | Annuel présélectionné, économie en % vraie, puis offre annuelle aux mensuels (§3 #10) |
| 6 | **Abonné bloqué hors ligne** (voiture, avion : c'est l'usage même du mode voiture) → frustration, remboursement | 🔴 | Droits mis en cache sur le téléphone avec la date d'expiration ; tolérance hors ligne de 7 jours après expiration avant de repasser en gratuit ; jamais de vérification réseau bloquante au démarrage |
| 7 | **Paywall mal placé** : trop tôt (avant d'avoir vu l'appli) ou nulle part (freemium à 2 %) | 🔴 | Offre au moment où le parent est présent (fin de la 1ʳᵉ ouverture, après création des profils), puis offres contextuelles dans l'Espace Parents |
| 8 | **Parent absent** : l'enfant ouvre l'appli seul, le parent ne voit jamais l'offre | 🟠 | Message côté enfant autorisé (« Montre à tes parents ce que tu as appris ») ; bilan hebdomadaire par email (si donné) ; badge discret « 1 information pour le parent » sur l'icône de l'Espace Parents |
| 9 | **Pas de rappel avant fin d'essai** → prélèvement « surprise », remboursements, avis 1★ (cf. 22 % d'avis 1★ chez Headway) | 🟠 | Rappel J-2 (§3 #5). Paradoxalement, le rappel **augmente** la confiance et l'essai suivant |
| 10 | **Prix non localisés ou incohérents** (prix en dur, € affiché à un Suisse) | 🟠 | Toujours afficher `priceString` venant du store ; grille par zone §2.4 |
| 11 | **Écran d'offre non traduit** dans la langue du parent (familles expatriées) | 🟠 | Traduire l'écran d'offre dans les ≈ 20 langues de l'appli ; libellés validés |
| 12 | **Annulations le jour même** de l'essai (55 % pour les essais de 3 jours) | 🟠 | Essai de 7-14 jours ; dire « Vous pouvez annuler, vous gardez l'essai jusqu'au bout » (vrai sur les stores) |
| 13 | **1er mois de l'abonné annuel négligé** (≈ 30 % des annulations annuelles) | 🟠 | Parcours « 1ʳᵉ semaine » côté parent, bilan dès J7, conseils de la notice parents (Aventure, Flash, visite de la ville) |
| 14 | **Pas de reconquête** | 🟠 | Win-back natifs Apple/Google configurés dès le lancement (pas de code complexe) |
| 15 | **Barrière parentale trop dure ou bugguée** → le parent abandonne | 🟠 | Barrière actuelle (nombre en lettres, réponse en chiffres) ; mesurer le taux d'échec (compteur anonyme) ; question dans la langue du parent |
| 16 | **Achat bloqué par le contrôle parental du store** (« Demander l'autorisation », Family Link) : la demande part, puis rien | 🟡 | Gérer l'état « en attente » (achat différé / pending) : message « Demande envoyée à l'organisateur de la famille », et déblocage automatique à l'approbation |
| 17 | **Pas de cadeau à Noël ni d'offre pour les grands-parents** | 🟡 | Codes cadeaux (§3 #13), campagne en novembre-décembre |
| 18 | **Parents qui refusent tout abonnement** | 🟡 | Famille à vie, Pass Révisions non renouvelable |
| 19 | **B2B non traité** (enseignants ou orthophonistes qui écrivent et n'ont pas de réponse) | 🟡 | Page « Pros » + formulaire + codes d'établissement |
| 20 | **Utilisateurs web (PWA) qui ne peuvent pas payer** | 🟡 → 🟠 | Phase 2 : paiement web + Code Famille |
| 21 | **Changement de prix mal géré** → abonnés perdus | 🟡 | Prix garanti aux abonnés existants (§2.3) |
| 22 | **Rejet au store** (règles Familles/Kids, SDK) → zéro vente pendant des semaines | 🔴 | Liste de contrôle §6 avant soumission ; tests de pré-lancement Google ; aucun SDK publicitaire ni d'analyse |

---

## 5. Ce qu'il faut coder (ordre de priorité, effort estimé)

Hypothèse : Mario + Claude, application PWA existante (`index.html`, `js/`, `sw.js`, Cloudflare Pages + Functions). Les efforts sont en **jours de travail effectif**, tests compris.

### 5.1 Choix techniques

| Sujet | Recommandation | Pourquoi / alternative |
|---|---|---|
| Publication stores | **Capacitor** (un seul code web, enveloppe Android + iOS, fichiers embarqués pour le hors-ligne) | La TWA (Bubblewrap) suffit pour Android avec la Digital Goods API de Play Billing, mais **iOS exige une appli native** et Apple rejette les « simples sites emballés » (règle 4.2) : Capacitor couvre les deux. |
| Gestion des abonnements | **RevenueCat** (`@revenuecat/purchases-capacitor`) : validation des reçus, droits multi-stores, période de grâce, offres de reconquête, droits promotionnels (parrainage), tests A/B d'écrans d'offre, paiement web plus tard | Gratuit jusqu'à un certain revenu mensuel puis environ 1 % (barème à reconfirmer). **Conditions Familles/Kids** : identifiant utilisateur **anonyme et aléatoire**, aucun attribut personnel, **retirer la permission `AD_ID`** du manifeste Android, ne pas activer la collecte d'identifiants d'appareil, signer le DPA, déclarer « historique d'achat » dans la fiche Data safety. ⚠️ Un développeur a signalé un appel à l'identifiant publicitaire depuis le SDK : **vérifier avec les tests de pré-lancement Google avant soumission**. **Alternative** : facturation native (`cordova-plugin-purchase` + StoreKit 2 + Play Billing) et validation sur un Worker Cloudflare : aucun tiers, mais 5 à 8 jours de plus et plus d'entretien. |
| Droits hors ligne | Couche locale `droits.js` : `{formule, expire_le, source, verifie_le}` en cache, tolérance de 7 jours | Indispensable pour le mode voiture |
| Partage famille | Partage familial Apple + **Code Famille** (identifiant aléatoire partagé par QR, sans email) | Respecte « pas de compte, pas d'email obligatoire » |
| Compteurs anonymes | Worker Cloudflare (même logique que le compteur de réponses existant) | §6 |

### 5.2 Ordre de priorité

| Prio | Tâche | Effort | Dépend de |
|---|---|---|---|
| **P0** | Enveloppe Capacitor Android (fichiers embarqués, icônes, service worker adapté) | 3-4 j | — |
| **P0** | Comptes développeur, produits dans les consoles (Solo, Famille, mensuel/annuel, essai 7 j, groupe d'abonnements unique), pays exclus, prix par zone | 1-2 j | — |
| **P0** | Intégration RevenueCat (ou native) : achat, restauration silencieuse, écoute des changements de statut | 2-3 j | P0 précédents |
| **P0** | **Couche de droits** + cache hors ligne + branchement des limites du gratuit (option B) dans les modules | 2-3 j | — |
| **P0** | **Écran d'offre** derrière la barrière parentale (3 formules, bascule mensuel/annuel, mentions §3.1, prix localisés, traduction) | 2-3 j | intégration |
| **P0** | **Restaurer mes achats** + **« Gérer mon abonnement »** (lien direct vers la gestion Google Play ; `showManageSubscriptions` sur iOS) | 0,5 j | intégration |
| **P0** | Onboarding « À faire par un adulte » avec l'offre et « Continuer en gratuit » | 1-2 j | écran d'offre |
| **P0** | Gestion des achats en attente (contrôle parental du store) et des erreurs | 0,5 j | intégration |
| **P0** | Textes : conditions générales (abonnement, essai, à vie), politique de confidentialité mise à jour (prestataire d'abonnement, identifiant anonyme), fiche Data safety, questionnaire « App Privacy » Apple → **relecture juriste** | 2 j + juriste | — |
| **P0** | Tests en bac à sable (achat, essai, renouvellement accéléré, annulation, grâce, restauration, hors ligne) | 2 j | tout |
| **P1** | Compteurs anonymes de vente (§6) | 1 j | — |
| **P1** | Rappel de fin d'essai J-2 dans l'Espace Parents (+ email de service si email donné) | 1-2 j | droits |
| **P1** | Bandeau échec de paiement / période de grâce | 0,5 j | intégration |
| **P1** | **Code Famille** (QR, identifiant anonyme, 5 appareils max) + Partage familial Apple | 2 j | intégration |
| **P1** | Offres contextuelles Espace Parents (limite atteinte, réglage verrouillé, bilan) avec plafond de fréquence | 1-2 j | écran d'offre |
| **P1** | Codes fondateurs (codes d'offre Apple / promo Google) + produit « fondateur » | 1 j | consoles |
| **P1** | Offre annuelle aux mensuels + offres de reconquête natives (configuration) | 0,5-1 j | intégration |
| **P1** | Enveloppe iOS (Capacitor, StoreKit, validation App Review Kids ou Éducation) | 3-5 j | P0 |
| **P2** | Codes cadeaux (vente in-app non renouvelable + activation de code ; vente web) | 2-3 j | Code Famille |
| **P2** | Parrainage (code partagé, droits promotionnels RevenueCat) | 2 j | intégration |
| **P2** | Licences B2B (codes d'établissement, facturation, mode classe ou séance) | 2-3 j | droits |
| **P2** | Paiement web pour la PWA (RevenueCat Web Billing / Stripe ou Paddle) + bouton « Résilier » 3 clics, rappel L215-1, renonciation à la rétractation | 3-5 j + juriste | Code Famille |
| **P2** | Famille à vie, Pass Révisions | 1 j | consoles |
| **P3** | Premium (prononciation Azure via un Worker, réservé aux abonnés Premium) | 3-5 j | mesure du coût (README §5) |
| **P3** | Tests A/B d'écrans d'offre (variantes de prix, durée d'essai) | 0,5 j | trafic suffisant |

**Version minimale vendable (P0)** : environ **16 à 22 jours**, plus la relecture juriste. Avec P1 (dont iOS) : **+11 à 15 jours**.

---

## 6. Mesures à suivre (sans données personnelles sur l'enfant)

### 6.1 Ce qu'on lit chez les stores et RevenueCat (aucun code)
Essais démarrés, conversion essai → payant, revenu mensuel récurrent, part de l'annuel, churn par mois, remboursements, résiliations involontaires et récupérées (grâce), reconquêtes, revenus par pays. Ces chiffres sont rattachés à un **identifiant d'achat anonyme**, jamais à un profil d'enfant.

### 6.2 Compteurs anonymes à ajouter (Worker Cloudflare)
**Règles** : on incrémente un **compteur agrégé** `(jour, événement, plateforme, version, pays du store, variante A/B)` ; **aucun identifiant**, aucune IP conservée (pas de journaux détaillés), aucune donnée de profil (ni prénom, ni âge précis, ni progrès individuels). C'est un traitement de 1ʳᵉ partie, compatible avec Apple 1.3 et 5.1.4 et avec Google Familles. À mentionner dans la politique de confidentialité.

| Compteur | Sert à mesurer |
|---|---|
| `onboarding_parent_debut` / `_fin` | Abandon de la 1ʳᵉ ouverture |
| `barriere_ok` / `barriere_echec` | Barrière trop dure (fuite #15) |
| `offre_vue_<emplacement>` (onboarding, limite, reglage, bilan, annuel, reconquete) | Quel moment vend |
| `offre_formule_choisie_<solo/famille/premium>_<mois/an>` | Mix des formules |
| `achat_lance` / `achat_ok` / `achat_annule_par_utilisateur` / `achat_erreur` / `achat_en_attente` | Fuites au moment du paiement |
| `essai_demarre_<J0/plus_tard>` | Valide la fuite #4 |
| `continuer_gratuit` | Taux de refus de l'offre |
| `restauration_tentee` / `_ok` | Fuite #1 |
| `limite_gratuite_atteinte` (compte total, sans profil) | Pression réelle du gratuit |
| `espace_parents_ouvert` | Présence du parent |
| `code_famille_lie` | Usage multi-appareils |
| `droits_hors_ligne_utilises` | Fuite #6 |
| `rappel_fin_essai_affiche` / `gerer_abonnement_ouvert` | Transparence |
| `cadeau_active` / `parrainage_partage` / `parrainage_active` / `code_pro_active` | Canaux secondaires |
| `raison_arret_<prix/peu_utilise/contenu/technique/autre>` (facultatif) | Comprendre le churn |

**Taux à suivre chaque semaine** (une métrique par test, selon la compétence marketing) : fin de la 1ʳᵉ ouverture / installations ; essais / onboarding terminés ; `achat_ok / offre_vue` par emplacement ; essai → payant ; part de l'annuel ; récupération des échecs de paiement ; échecs de barrière / tentatives. **Tests A/B** : variante tirée au hasard **sur le téléphone**, compteurs par variante. Avec peu de trafic, tester l'un après l'autre (2 semaines par variante) plutôt qu'en parallèle.

---

## 7. Les 3 points juridiques bloquants (avant toute vente)

1. **Zéro sollicitation commerciale côté enfant.** Pas d'offre, de prix, de cadenas « payant » ni de « demande à tes parents », y compris dans les notifications et dans Mon Monde. Barrière parentale avant tout écran d'achat, lien externe ou partage. Aucune monnaie virtuelle vendue (déjà le cas : `economie.md` « Rien à acheter avec de l'argent réel » ; le futur DFA veut désactiver par défaut les monnaies virtuelles pour les mineurs). Sources : Apple 1.3, Google Familles (tactiques manipulatrices), directive 2005/29/CE annexe I pt 28, principes CPC 2025 sur les monnaies virtuelles.
2. **Transparence de l'abonnement et de l'essai.** Écran d'offre complet (§3.1), rappel avant la fin de l'essai, annulation facile et expliquée, pas de faux prix barré ni de fausse urgence, prix fondateurs et de lancement vrais et datés. Pour la vente web : bouton de résiliation en 3 clics (L215-1-1), information avant reconduction annuelle (L215-1, 3 mois à 1 mois avant l'échéance), renonciation expresse au droit de rétractation (L221-28 13°). Le DFA (proposition du 11/11/2026, pas encore en vigueur) prévoit une confirmation active avant la conversion d'un essai : **concevoir dès maintenant le rappel J-2 pour s'y préparer**.
3. **Données et SDK.** Brique d'abonnement sans identifiant publicitaire ni identifiant d'appareil, identifiant anonyme, DPA, fiches Data safety et App Privacy exactes. Mise à jour de la **notice parents**, qui dit aujourd'hui « Pas de compte… Les profils et les progrès restent sur le téléphone » : ajouter que l'achat est géré par Google/Apple et le prestataire d'abonnement avec un identifiant anonyme, sans donnée sur l'enfant. Email jamais obligatoire, case « offres » séparée et non cochée. COPPA avant un lancement aux États-Unis. Loi monégasque 1.565 à valider localement.

**Aussi à faire valider par le juriste** : conditions de la Famille à vie (« à vie » = durée d'exploitation), parrainage, licences B2B (neutralité commerciale à l'école, mode orthophoniste sans données de patients), vente web depuis Monaco (TVA, marchand de référence).

### Cohérence avec ce qui est déjà publié aux parents
La notice et la présentation Mon Monde promettent : **sans pub, pas de coffres surprises, pas de minuteurs à payer, pas de séries culpabilisantes, achats protégés par code, données sur le téléphone**. Le tunnel ci-dessus respecte ces promesses à condition :
- que la limite quotidienne du gratuit ne soit **jamais présentée à l'enfant comme achetable** ;
- que l'abonnement n'**accélère pas** la production de la ville ;
- que les séries (streaks de `economie.md`) ne servent jamais d'argument de vente (« ne perds pas ta série, abonne-toi ») ;
- que la notice soit mise à jour (point 3).

Ce sont aussi les **meilleurs arguments de vente**, à reprendre sur l'écran d'offre : « Sans pub. Sans achat surprise. Annulable en 1 clic. Vos données restent sur le téléphone. »

---

## 8. Sources

**Benchmarks**
- RevenueCat, *State of Subscription Apps 2026*, catégorie Éducation : https://www.revenuecat.com/state-of-subscription-apps-2026-education
- RevenueCat, rapport général 2026 : https://www.revenuecat.com/state-of-subscription-apps-2026/
- RevenueCat, synthèse tendances et benchmarks 2026 : https://www.revenuecat.com/blog/growth/subscription-app-trends-benchmarks-2026.md
- RevenueCat, durée des essais gratuits : https://www.revenuecat.com/blog/growth/free-trial-length
- Adapty, *State of In-App Subscriptions 2026* : https://adapty.io/state-of-in-app-subscriptions-report/
- Adapty, benchmarks applis Éducation : https://adapty.io/blog/education-app-subscription-benchmarks/
- Adapty, partage familial des achats : https://adapty.io/blog/app-purchases-family-sharing

**Prix concurrents**
- Kartable, App Store FR (achats intégrés) : https://apps.apple.com/fr/app/kartable-cours-et-r%C3%A9visions/id825500330
- Lingokids, prix Plus : https://help.lingokids.com/hc/en-us/articles/9522217000209-How-much-does-Plus-subscription-cost
- Duolingo Famille (Spliiit, 11/2026) : https://www.spliiit.com/en/blog/duolingo-prix-famille
- Abonnements enfants 2026 (Bayam, Whisperies…) (Spliiit) : https://www.spliiit.com/blog/histoire-du-soir-5-abonnements-pour-enfants-a-connaitre-en-2026-et-combien-ca-coute-vraiment
- Concurrents anti-scroll : `docs/flash/01_concurrents_antiscroll.md`

**Règles stores**
- Apple, App Review Guidelines (1.3 Kids, 3.1.1, 3.1.2, 3.1.3, 5.1.4) : https://developer.apple.com/support/downloads/terms/app-review-guidelines/App-Review-Guidelines-English-UK.pdf
- Apple, offres de reconquête (win-back) : https://developer.apple.com/news/?id=8utnewzk
- Apple, codes d'offre : https://developer.apple.com/documentation/storekit/implementing-offer-codes-in-your-app.md
- Apple, mensuel avec engagement 12 mois (04/2026) : https://ppc.land/apple-adds-monthly-12-month-commitment-plan-to-app-store-subscriptions/
- Google Play, règles Familles : https://support.google.com/googleplay/android-developer/answer/9893335?hl=en
- Google Play, comprendre les abonnements : https://support.google.com/googleplay/android-developer/answer/12154973?hl=en
- Google Play, nouveautés abonnements (29/09/2026 : grâce dynamique, offres de rétention, winback, achats multi-quantités) : https://android-developers.googleblog.com/2026/09/unlocking-Google-play-subscription-growth.html
- Google Play, transparence des abonnements (2020) : https://android-developers.googleblog.com/2020/04/building-user-trust-through-more.html
- RevenueCat, forum : SDK et règles Familles (AD_ID) : https://community.revenuecat.com/sdks-51/data-practices-of-google-families-policy-on-kids-app-2402
- RevenueCat, PWA, Capacitor et paiement web : https://community.revenuecat.com/general-questions-7/how-do-you-handle-in-app-purchases-with-an-pwa-google-store-5894 et https://www-docs.revenuecat.com/docs/getting-started/installation/capacitor.md

**Droit UE / FR / Monaco / États-Unis**
- Digital Fairness Act, proposition du 11/11/2026 (Lewis Silkin) : https://www.lewissilkin.com/insights/2026/11/11/european-commission-publishes-long-awaited-digital-fairness-act-102o9b5
- Lignes directrices DSA art. 28 sur la protection des mineurs : https://digital-strategy.ec.europa.eu/en/library/commission-publishes-guidelines-protection-minors et https://www.osborneclarke.com/insights/new-european-guidelines-issued-protect-minors-digital-environment
- Réseau CPC, principes sur les monnaies virtuelles (03/2025) : https://lewissilkin.com/insights/2025/03/26/eu-bodies-act-against-gaming-companies-to-protect-children-from-in-game-purchase-102k658
- Résiliation en 3 clics (L215-1-1, D215-1 à D215-3) : https://www.donneespersonnelles.fr/resiliation-en-trois-clics
- Reconduction tacite (L215-1), INC : https://www.inc-conso.fr/content/reconduction-tacite-du-contrat ; Légifrance : https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000034072591/
- Annonces de réduction de prix (L112-1-1) : https://donneespersonnelles.fr/annonce-reduction-prix ; DGCCRF affichage des prix : https://www.economie.gouv.fr/entreprises/professionnels-quelles-sont-vos-obligations-en-matiere-daffichage-des-prix
- Directive 2005/29/CE (pratiques commerciales déloyales), annexe I points 7 et 28 : https://eur-lex.europa.eu/legal-content/FR/TXT/?uri=CELEX:32005L0029
- Monaco, loi n° 1.565 du 3/12/2024 (CMS) : https://cms.law/fr/mco/publication/nouvelle-loi-monegasque-sur-la-protection-des-donnees-personnelles
- COPPA, règle modifiée (Federal Register, 22/04/2025) : https://www.federalregister.gov/documents/2025/04/22/2025-05904/childrens-online-privacy-protection-rule
- Documents internes : `docs/tarification/README.md` (§6-8), `docs/jeux/economie.md`, notice parents, présentation Mon Monde.

*Points non vérifiés sur source primaire, à reconfirmer : barème RevenueCat, quotas de codes promo Google, existence d'une vitrine App Store « Monaco », exceptions B2B de la politique Paiements Google Play, application de la règle de neutralité commerciale à l'école, absence de partage familial des abonnements sur Google Play.*
