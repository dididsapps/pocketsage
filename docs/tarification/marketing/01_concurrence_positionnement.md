# Concurrence, manques du marché et positionnement — PocketSage Academy

*Recherche web du 15/11/2026. Chaque prix est daté et sourcé (section 7). Les prix des stores varient selon le pays, la plateforme et les promotions : **revérifier sur le store du pays visé avant toute communication chiffrée**. « (source concurrente) » = chiffre publié par un acteur qui vend une offre rivale. « Non vérifié » = pas trouvé sur une source primaire.*

Documents internes pris en compte : `00_contexte.md`, `tarification/README.md`, `flash/01_concurrents_antiscroll.md`, `docs/parents/notice_parents.html` (et sa version PDF `guide_parents.pdf`), `docs/jeux/presentation/Mon_Monde_presentation.pdf`, compétence marketing-pocketsage.

---

## 0. L'essentiel en 10 lignes

1. Le marché est **découpé par âge** : 0-8 ans (Khan Kids, Lingokids, Duolingo ABC, Adibou, Holy Owly), scolaire collège-lycée (Kartable, SchoolMouv, Lumni, Brainly), adultes (Duolingo, Blinkist, Deepstash). **Personne ne suit un enfant de 4 ans jusqu'à l'âge adulte dans la même appli, avec un seul abonnement famille.**
2. Les **gratuits de qualité** (Khan Academy Kids, Duolingo ABC, Lumni) fixent la barre : 4,8★ et 133 k notes pour Khan Kids. Pour être payant, PocketSage doit offrir ce qu'ils n'ont pas : le français scolaire, les ados, la famille entière et le mouvement.
3. Les payants enfants coûtent **60 à 180 €/an** (Lingokids 71,99-89,99 €, Kartable 119,99 € et 179,99 € pour 3 enfants, Prodigy 74,95-118,95 $). Une formule Famille à 40-50 €/an est **nettement sous le marché**.
4. Les plaintes n°1 des parents portent sur **l'argent** : achats intégrés, essais pièges, renouvellements surprises, « gratuit épuisé » brutal. Viennent ensuite la **pression à payer côté enfant** (cas Prodigy), les bugs et pertes de progression, et le contenu qui s'épuise.
5. La **reconnaissance vocale** est critiquée partout (Holy Owly « trop permissive », Duolingo ABC). Ne pas promettre une « correction de l'accent » tant qu'elle n'est pas précise.
6. **Ce que PocketSage a déjà et qui est rare** : 4 ans → adulte, langue maternelle et 9 langues, pauses physiques intégrées, Flash anti-scroll avec révision espacée, pas de pub, pas de compte, pas de coffres ni de séries culpabilisantes, et des fiches papier.
7. **Les trois manques à combler avant de vendre** : un bilan parent lisible (« ce qu'il a appris cette semaine »), une séance « contrôle de demain » choisie par le parent, et la sauvegarde/transfert des progrès sans compte.
8. La promesse mère est **validée sur le fond**. Je recommande de la passer au **vouvoiement** côté parents (le « tu » peut se lire comme adressé à l'enfant) et de l'adosser à une preuve concrète.
9. Le **risque n°1 du lancement n'est pas marketing mais store** : une PWA empaquetée peut être refusée comme « simple webview » (Google Familles) ou pour fonctionnalité minimale (Apple 4.2). Le choix de catégorie Apple Kids ou non conditionne aussi le vocabulaire autorisé.
10. Les allégations à bannir : tout chiffre d'efficacité (« +X % en maths »), « cliniquement prouvé », toute allusion au TDAH ou aux dys, « rend bilingue », « approuvé par l'Éducation nationale ». Lumosity a payé 2 M$ à la FTC pour moins que ça.

---

## 1. Veille concurrentielle

### 1.1 Tableau de synthèse

| Appli | Âges | Prix (date de la source) | Essai / gratuit | Points forts | Plaintes principales | Positionnement |
|---|---|---|---|---|---|---|
| **Khan Academy Kids** | 2-8 ans | **Gratuit**, sans pub ni abonnement (App Store US, consulté le 15/11/2026) | 100 % gratuit | 4,8★ (133 k notes), contenu soigné, COPPA | Bugs/plantages, hors-ligne limité, **contenu insuffisant pour les plus âgés** (Unstar, 06/2026). **Pas de français** sur la fiche (anglais, livres lus en EN/ES) | ONG « éducation gratuite pour tous » |
| **Duolingo** (langues + maths + musique + échecs) | Ados/adultes | Super Family ≈ **119,99 $/an pour 6** ; Max Family ≈ 240 $/an (duolingoguides, 10/2026, **à vérifier**, Max peut-être retiré) | Freemium | Maths et musique intégrées à l'appli principale depuis le 11/10/2023 ; rétention record (84 % à J+1, T2 2026) | Mécaniques de séries culpabilisantes, pubs en gratuit (voir `01_concurrents_antiscroll.md`) | « Apprendre comme un jeu » |
| **Duolingo ABC** | 3-8 ans | **Gratuit**, sans pub ni achat (Marlvel, 29/03/2026) | Gratuit | Marque, apprentissage de la lecture | **Anglais uniquement**, reconnaissance vocale peu fiable, bugs, perte de progression, pubs vers l'appli principale (Unstar 06/2026, Marlvel) | Lecture en anglais |
| **Lalilo** (Renaissance) | Maternelle-CE1 | **Plus de version gratuite depuis le 12/11/2025** ; licence classe en ligne, licence école sur devis (aide Lalilo, 30/03/2026) | Non | Référence enseignants pour la lecture, adaptatif | Pas d'offre parent publique ; 60 min/jour max | Outil de classe, B2B |
| **Kahoot!+ Kids** | 3-12 ans | Bronze **9 $/mois ou 36 $/an**, Gold 25 $/mois ou 108 $/an, 5 profils (page Kahoot!, prix **Black Friday jusqu'au 27/11**) | Formule gratuite Kahoot! Go | Bouquet d'applis (maths, lecture, échecs, code), 5 profils | Pas d'essai mentionné ; prix promo vs prix réel peu lisible | Bouquet ludo-éducatif |
| **Prodigy Math/English** | 6-14 ans | Level Up 9,95 $/mois ou 74,95 $/an ; Ultimate 14,95 $/mois ou 99,95 $/an ; Ultra (2 jeux) 118,95 $/an (ThePricer, 04/03/2026) | Gratuit avec avantages membres | Jeu de rôle très engageant | **Pression à payer côté enfant** : Fairplay a compté 16 pubs pour l'abonnement contre 4 problèmes de maths en 19 min ; plainte à la FTC (02/2021) ; inégalités entre membres et non-membres ; remboursements restreints | « Jeu gratuit pour l'école », monétisé par la frustration |
| **Adibou par Wiloki** | 4-7 ans | Gratuit + univers à **9,99 € à 14,99 €** l'unité (App Store FR, 15/11/2026) | Partie gratuite | Marque nostalgique des parents, sans pub | « Payer pour continuer à jouer » (avis 07/2025, 11/2025), fonctions de l'original manquantes | Nostalgie + petits |
| **Holy Owly** | 3-11 ans (fiche : 0-5) | Achats de **9,99 € à 95,99 €**, solo/famille, périodes non indiquées (App Store FR, 15/11/2026) | Essai (non détaillé) | 5 min/jour d'anglais/espagnol, concept simple | 4,2★ (922) ; **reconnaissance vocale « beaucoup trop permissive »** ; impression des images retirée | « Bilingue en 5 min/jour » |
| **Mathador Flash & Plato** (Canopé) | 8 ans + | Gratuit + version complète **1,99 €** (App Store FR, 15/11/2026) | Oui | Caution Réseau Canopé, calcul mental | 7 notes seulement, jeu à plusieurs peu clair | Niche calcul mental |
| **Lumni** (France TV + INA) | Primaire-lycée | **Gratuit, sans pub**, service public (communiqué du 04/05/2026) | Gratuit | Vidéos, 800+ contenus brevet/bac, crédibilité publique | Pas de parcours personnel, pas de progression ni de profils, peu ludique | Médiathèque éducative publique |
| **SchoolMouv** | CP-Terminale | Prix catalogue non affichés ; promos « jusqu'à -60 % » (site, 15/11/2026). Ancienne promo Veepee : 99 €/an au lieu de 199,99 € (2022, **daté**) | Contenus gratuits limités | 3 M d'élèves inscrits revendiqués, cours + quiz, chat prof (Premium) | Prix réel opaque (promos permanentes) | Soutien scolaire en ligne |
| **Kartable** | CP-Terminale | **14,99 €/mois, 119,99 €/an** ; 3 enfants **24,99 €/mois ou 179,99 €/an** (App Store FR, 15/11/2026 ; la description annonce 13,99 €/109,99 €, incohérence) | « Contenu gratuit épuisé » | 4,5★ (20 k), cours complets | Fin brutale du gratuit, **prix jugé élevé**, audio des cours retiré, demande de mini-quiz | Cours et révisions du programme |
| **Brainly** (Nosdevoirs.fr) | Collège-lycée | Plus **9,99 $/mois ou 39,99 $/an** ; Tutor 29 $/mois ou 96 $/an (Fast.io, 28/06/2026) | Essai 7 jours ; gratuit avec pubs | Réponse rapide aux devoirs (IA + communauté) | Exactitude variable hors maths, **usage pour tricher**, pubs | Aide aux devoirs |
| **Lingokids** | 2-8 ans | **14,99 €/mois ; 71,99-89,99 €/an** (App Store FR, 15/11/2026) | Version gratuite | 4,3★ (21 k), Trustpilot 4,7 (164 avis) | « Yearly subscription feels predatory » (18/10/2026), « extrêmement chère » | Anglais ludique pour petits |
| **Speak / Speakup** (anglais par IA) | Ados/adultes | **Non vérifié** (fiche App Store inaccessible le 15/11/2026) | — | Conversation orale par IA | — | Oral en anglais pour adultes |
| **Blinkist** (angle anti-scroll) | Adultes | **79,99 €/an ou 12,99 €/mois** (blog Blinkist, 06/2023, **à revérifier**) | Essai 7 jours | Catalogue de résumés | Prix, lecture passive (voir doc Flash) | Résumés de livres |
| **Deepstash** (angle anti-scroll) | Adultes | 12,99-19,99 $/mois ; 50-120 $/an (voir `01_concurrents_antiscroll.md`, 10/11/2026) | Freemium avec pubs | Cartes d'idées à swiper | Paywall sur la sauvegarde, renouvellements surprises, « AI slop » | Collection d'idées |
| **Simply Piano** (type Yousician) | 6 ans + | Individuel 119,99 $/an ; **Famille 179,99 $/an, 5 profils** (ThePricer, 05/2026) | Essai 7 jours (Google Play) | Plan famille, feedback en temps réel | Annulation liée au store, prix | Musique par app |
| **Kiupe** | — | **Non trouvé** lors de la recherche du 15/11/2026 (nom exact à confirmer) | — | — | — | — |

### 1.2 Ce que disent les avis négatifs (toutes applis enfants confondues)

Analyse Unstar (16/04/2026, « milliers » d'avis 1 à 3★ d'applis enfants et parents, méthode peu détaillée) :

| Rang | Plainte | Ce que PocketSage en fait |
|---|---|---|
| 1 | **Pubs et achats intégrés** : environ 35 % des avis 1★ de la catégorie (ex. « le bouton acheter ressemble au bouton jouer ») | Argument : aucune pub, aucun achat côté enfant, achats derrière barrière parentale et code |
| 2 | **Abonnements pièges** : essai avec carte, renouvellement sans rappel, remboursement refusé | Argument : prix clair, rappel avant la fin de l'essai, page « Comment annuler » |
| 3 | Contenu inapproprié malgré les filtres, messagerie avec des inconnus | Argument : tout le contenu est rédigé pour PocketSage, aucun chat, aucune recommandation automatique |
| 4 | Vie privée, permissions excessives | Argument : sans compte, données sur le téléphone, micro réglable par enfant |
| 5 | Design qui pousse au temps d'écran (lecture auto, notifications, séries, FOMO) | Argument : fin de séance naturelle, **pas de séries culpabilisantes** (engagement Mon Monde) |
| 6 | Contrôle parental faible (PIN facile, minuteur qui tourne en arrière-plan) | Vérifier : code par défaut 1234 à forcer au changement, minuteur de jeu qui ne décompte qu'au premier plan |
| 7 | Niveau inadapté à l'âge | Argument : niveau scolaire réglable + barre « Réviser / Ma classe / En avance » |
| 8 | Plantages sur vieux appareils | Tester sur Android d'entrée de gamme avant lancement |

Spécifique à chaque appli : **contenu qui s'épuise ou trop court pour les plus grands** (Khan Kids, Duolingo ABC, Homer), **perte de progression** (Duolingo ABC), **reconnaissance vocale trop permissive** (Holy Owly, Duolingo ABC), **fin brutale du gratuit** (Kartable).

### 1.3 Ce que disent les sondages (à citer avec prudence)

- 73 % des parents américains jugent le temps d'écran interactif meilleur que le passif ; 71 % pensent qu'il peut être enrichissant (Lingokids, 2 000 parents US d'enfants de 2-8 ans, 28/07/2026, **source concurrente**).
- Trois quarts des parents veulent des **limites quotidiennes** de temps d'écran, et seulement 1 % veulent zéro écran à l'école (National Parents Union, 1 527 parents, sondage du 28/05 au 01/06/2026, Education Week 26/06/2026).
- Lecture : les parents ne rejettent pas l'écran, ils veulent un **écran actif, limité et utile**. C'est exactement la promesse de PocketSage.

### 1.4 Contexte réglementaire porteur (angle RP)

- **Loi « réseaux sociaux < 15 ans » définitivement adoptée** par le Parlement (Blog du Modérateur, 22/07/2026). Les répertoires éducatifs et encyclopédies sont exclus. Saisine du Conseil constitutionnel annoncée, **date d'entrée en vigueur à vérifier**. PocketSage n'est pas un réseau social : aucun chat, aucun partage entre inconnus.
- Lignes directrices DSA sur les mineurs (14/07/2025) contre le design addictif : voir le doc Flash.

---

## 2. Manques du marché

### 2.a Ce que PocketSage a déjà et qui est rare (à mettre en avant)

| Atout | Qui d'autre le fait ? | Force de l'argument |
|---|---|---|
| **De 4 ans à l'adulte, 4 profils, un seul prix** | Personne : Khan Kids et ABC s'arrêtent à 8 ans, Adibou à 7, Kartable ne fait que du scolaire | Très forte (fratrie d'âges différents + parents) |
| **Langue maternelle de l'enfant + 9 langues** (interface, Flash et fiches dans sa langue) | Khan Kids : anglais/espagnol. Les FR sont monolingues | Très forte pour les familles bilingues/expatriées, peu de concurrence |
| **Pauses physiques intégrées** (défi toutes les 5 questions dans l'Aventure, rythme selon l'âge) + **coach sportif** guidé à la voix | Personne dans l'éducatif | Forte, très visuelle en vidéo |
| **Flash anti-scroll pour enfants** avec source, geste « Essaie aujourd'hui » et **révision espacée** (2, 7, 21 jours) | Les anti-scroll visent les adultes et sont passifs | Forte (angle « brain rot », loi < 15 ans) |
| **Récompense constructive sans pression** : Mon Monde (ville, petits métiers qui font calculer), **pas de coffres surprises, pas de séries culpabilisantes, pas de minuteur payant** | Contre-modèle exact de Prodigy | Forte auprès des parents informés |
| **Sans pub, sans compte, données sur le téléphone, l'essentiel hors-ligne** | Khan Kids et Lumni sont sans pub, mais avec compte ou en ligne | Moyenne à forte (attendu, mais rare chez les payants) |
| **Fiches PDF à imprimer** (35) + ateliers sans écran | Rare (Holy Owly a retiré l'impression, et ça lui a été reproché) | Moyenne, excellent produit d'appel enseignants et orthophonistes |
| **Mode voiture tout audio, mode nuit** (histoires, méditations), écran retourné | Rare dans une même appli | Moyenne, bon pour les vidéos « mise en situation » |
| **Programme français GS → Lycée**, ~7 900 questions vérifiées, indices = mini-leçons, voix sur chaque question | Kartable et SchoolMouv (cours, pas de jeu), Lumni (vidéos) | Moyenne à forte (le « vérifié » est une preuve contre l'IA non relue) |
| **Parler avec Sensei** (mini-conversations en anglais) | Speak et Duolingo Max pour adultes, payants | Moyenne (à ne pas survendre) |

### 2.b Fonctionnalités manquantes, classées par impact sur les ventes et par effort

Effort pour une petite équipe : **F** = faible (≤ 1 semaine), **M** = moyen (2-4 semaines), **É** = élevé (> 1 mois).

| Priorité | Fonctionnalité | Pourquoi (signal marché) | Impact ventes | Effort |
|---|---|---|---|---|
| **P0** | **Transparence de l'abonnement** : prix TTC affiché avant l'essai, rappel J-2 avant la fin de l'essai (natif store + message dans l'Espace Parents), page « Gérer / annuler » à 1 tap qui ouvre l'abonnement du store | Plainte n°2 du marché ; résiliation en 3 clics obligatoire en France depuis le 01/06/2023 (le store gère, mais il faut un lien clair) | Fort (avis 5★, moins de remboursements) | F |
| **P0** | **Bilan parent « Cette semaine »** lisible dans l'Espace Parents : modules faits, réussites, 2 points à retravailler, 1 question à poser au dîner. Puis la version email facultative déjà prévue | Le parent paie ce qu'il voit. Les stats actuelles (activité par profil) ne disent pas *ce qui a été appris* | Très fort (c'est le moment de conversion) | M |
| **P0** | **Séance « Contrôle de demain »** : le parent choisit matière + thème (ex. fractions CM1, verbes irréguliers 4e) et lance une séance ciblée de 10 min | Kartable et SchoolMouv vendent « le programme ». Rejoint l'option A de l'offre gratuite (module choisi par le parent) | Fort | M (dépend du balisage par thème des 7 900 questions) |
| **P1** | **Sauvegarde et transfert sans compte** : export vers un fichier ou un QR code, import sur le nouveau téléphone | Perte de progression = plainte récurrente ; « pas de compte » ne doit pas vouloir dire « tout perdu au changement de téléphone » | Moyen à fort (rétention) | M |
| **P1** | **Défi famille sur un même téléphone** : parent contre enfant, ou fratrie, 5 questions chacun à son niveau, score équitable | Prouve le « pour toute la famille », génère des vidéos naturelles | Fort (viralité) | M |
| **P1** | **Carte « Bravo » à partager par le parent** (image ou diplôme PDF : « Léo a ancré 20 cartes Flash ») depuis l'Espace Parents, jamais côté enfant | Bouche-à-oreille sans réseau social ni données | Moyen | F |
| **P1** | **Confort de lecture** : taille du texte, police plus espacée, lecture audio systématique (déjà là) | Demande fréquente des parents d'enfants qui lisent lentement. **Communiquer « confort de lecture », jamais « pour les dys »** | Moyen | F |
| **P1** | **Compteur de contenu et rythme de nouveautés visible** (« +150 questions ce mois-ci ») | « Contenu qui s'épuise » est la plainte des applis 2-8 ans ; rassure les familles d'ados | Moyen | F (affichage) + continu (contenu) |
| **P2** | **Évaluation précise de la prononciation** (premium, déjà étudiée) | Holy Owly et Duolingo ABC sont critiqués pour une reconnaissance trop permissive : c'est un vrai trou | Moyen (argument premium) | M + coût par usage |
| **P2** | **Code classe léger** : l'enseignant projette un défi ou distribue les fiches, sans compte élève | Lalilo n'a plus de gratuit depuis 11/2025 : place pour un outil d'appoint gratuit qui fait connaître l'appli aux parents | Moyen à fort à moyen terme | É |
| **P2** | **Apprentissage de la lecture en français (GS-CP)** | Le grand trou du marché grand public : Duolingo ABC est en anglais, Lalilo est réservé aux classes. Mais c'est un chantier pédagogique lourd | Fort | É : à ne lancer qu'avec un enseignant référent |
| **À ne pas faire** | Séries quotidiennes avec perte, ligues publiques, coffres, monnaie achetable, notifications insistantes | Contredit l'engagement Mon Monde et les lignes DSA, et c'est la plainte n°5 | — | — |

> Ajustement par rapport au doc Flash : il proposait de « copier la série quotidienne de Duolingo ». Pour rester cohérent avec la présentation Mon Monde (« pas de séries culpabilisantes »), on garde au mieux une **série douce** : jours comptés sans perte, sans rappel culpabilisant, rien ne se « casse ».

---

## 3. Positionnement et messages

### 3.1 Promesse mère

**Actuelle** : « Le temps d'écran dont tu n'as pas à te sentir coupable. »

**Verdict : on la garde sur le fond.** Elle nomme le vrai sentiment du parent (la culpabilité), elle n'est pas « une appli qui fait tout », et aucun concurrent ne l'occupe : ils promettent tous « apprendre en s'amusant ». Trois réserves :
1. Le **« tu »** peut se lire comme adressé à l'enfant, ce qui est une zone sensible (exhortation des enfants, directive 2005/29/CE). Côté stores et parents, mieux vaut le **vouvoiement**.
2. Elle dit le bénéfice émotionnel mais pas **le mécanisme**. Il faut une ligne de preuve juste en dessous.
3. Elle n'inclut pas les adultes. Ce n'est pas grave : les adultes sont une cible secondaire, servie par des messages dédiés.

**Proposition :**
- **Promesse (store, site, vidéos parents)** : « Le temps d'écran dont vous n'avez pas à vous sentir coupable. »
- **Ligne de preuve** : « On apprend, on bouge, puis on pose le téléphone. De 4 ans à l'âge adulte, un seul abonnement pour toute la famille. »
- **Variante à tester en A/B** (une semaine, métrique : taux de clic vers le store) : « L'écran qui sait s'arrêter. »

### 3.2 Trois piliers de preuve

| Pilier | Ce qu'on dit | Preuves concrètes (déjà dans l'appli) |
|---|---|---|
| **1. Ça apprend vraiment** | « Des questions vérifiées, au bon niveau scolaire, qui reviennent pour être retenues. » | ~7 900 questions vérifiées GS → Lycée (chiffre à dater), indice-leçon à chaque question, voix sur chaque question, révision espacée Flash 2/7/21 jours, petits métiers de Mon Monde qui font calculer |
| **2. Ça fait bouger et ça s'arrête** | « Un défi physique toutes les quelques questions, puis une vraie fin de séance. » | Pauses selon l'âge (toutes les 3 à 8 questions), Coach sport, fin « Bravo, à demain ! », pas de séries culpabilisantes, pas de coffres, pas de pub, mode nuit écran retourné |
| **3. Toute la famille, vos données chez vous** | « Quatre profils, de 4 ans à l'adulte, dans la langue de chacun. Sans compte. » | 4 profils, langue maternelle + 9 langues, sans compte, données sur le téléphone, l'essentiel hors-ligne, Espace Parents protégé par code |

### 3.3 Nous contre eux, version honnête

| Critère | PocketSage | Khan Academy Kids | Duolingo | Kartable / SchoolMouv | Lingokids / Holy Owly | Prodigy |
|---|---|---|---|---|---|---|
| Âges couverts | **4 ans → adulte** | 2-8 ans | Ados/adultes (+ ABC 3-8, anglais) | CP-Terminale | 2-8 ans | 6-14 ans |
| Programme scolaire français | Oui (quiz) | Non | Non | **Oui, cours complets** (meilleur que nous) | Non | Non |
| Profondeur en langues | 9 langues, niveau découverte à intermédiaire | Non | **Très supérieure** | Non | Anglais (et espagnol) | Non |
| Langue maternelle de l'enfant | **Oui (~10 + « Autre »)** | EN/ES | Interface multilingue | FR | Variable | EN |
| Mouvement physique intégré | **Oui** | Non | Non | Non | Un peu (Lingokids) | Non |
| Pub / pression d'achat côté enfant | **Aucune** | Aucune | Pubs en gratuit | Aucune pub, fin du gratuit brutale | Aucune pub | **Forte** |
| Compte obligatoire | **Non** | Oui | Oui | Oui | Oui | Oui |
| Prix famille / an | **~40-50 € visé** (non décidé) | **0 €** | ~120 $ (6 pers.) | 179,99 € (3 enfants, Kartable) | 72-90 € (Lingokids) | 75-119 $ par enfant |
| Maturité, notes, preuves | **Bêta, 0 avis store, aucune étude** | 4,8★, 133 k notes | Leader mondial | 4,5★, 20 k (Kartable) | 4,3★, 21 k (Lingokids) | Très installé |
| Vidéos / cours explicatifs | Peu (vidéos sélectionnées) | Oui | Non | **Oui** | Oui | Non |

**Lecture** : on ne gagne pas « meilleur en tout ». On gagne sur **largeur d'âge, famille, langues maternelles, mouvement, absence de pression** et **prix famille**. On perd sur la profondeur (cours, langues), la maturité et les preuves sociales : il ne faut pas se battre sur ces terrains.

### 3.4 Messages par cible (une vidéo = un angle = un public)

| Cible | Ce qu'elle vit | Message principal | Preuve à montrer | Canal | Appel à l'action | À éviter |
|---|---|---|---|---|---|---|
| **Parents épuisés** | « Je donne le téléphone pour souffler et je culpabilise. » | « 15 minutes pour vous. 15 minutes utiles pour lui. » | Aventure de 20 étapes ≈ 15 min, défi physique, fin « à demain » | Reels/TikTok parents, groupes Facebook | « Essai gratuit 7 jours, sans pub » | Promettre « l'enfant sage », « baby-sitter », tout ce qui suggère un trouble |
| **Parents « culture »** | « Il scrolle des vidéos idiotes, je voudrais qu'il soit curieux. » | « Le scroll qui rend plus malin. » | Carte Flash avec source + question 2 jours après | Instagram, newsletters parentalité, SEO « alternative à TikTok enfant » | « 10 cartes par jour, essayez ce soir » | « Rend intelligent », « augmente le QI » |
| **Familles bilingues / expatriées** | « Je veux qu'il garde ma langue et apprenne celle de l'école. » | « Chaque enfant apprend dans sa langue, et découvre les autres. » | Interface en arabe/ukrainien/portugais + quiz du programme français + prononciation | Groupes d'expatriés, lycées français à l'étranger, associations, Facebook communautaire | « Choisissez sa langue maternelle à l'installation » | « Rend bilingue », « remplace l'école » |
| **Ados (15 ans et +)** | « Je m'ennuie, je scrolle, mais je veux pas d'appli de bébé. » | « Le défi culture : bats ton record, sans réseau social. » | Flash Chrono, Flash cartes psychologie/motivation, défi famille | TikTok/Shorts **créateurs adultes** ; les mineurs ne sont visés qu'en organique, jamais en pub ciblée | « Teste-toi en 2 minutes » (sans incitation à faire acheter) | Cibler les moins de 15 ans en pub, « demande à tes parents » |
| **Adultes (parents eux-mêmes)** | « Je veux apprendre une langue / me cultiver sans payer 100 €/an pour moi seul. » | « Votre abonnement famille vous inclut aussi. » | Profil adulte : Flash, langues, sport 40 min, méditations | Facebook, LinkedIn perso, bouche-à-oreille | « Créez aussi votre profil » | Se comparer frontalement à Duolingo (on perd sur la profondeur) |

---

## 4. Audit des arguments

### 4.1 Affirmations autorisées, avec la preuve à garder au dossier

| Affirmation | OK ? | Preuve à garder (dossier daté) | Formulation conseillée |
|---|---|---|---|
| « Sans publicité » | Oui | Capture de l'appli, absence de SDK pub, formulaire Data safety et étiquette Apple | « Aucune publicité. » |
| « Sans compte » | Oui, tant que c'est vrai | Parcours d'installation filmé | « Pas de compte à créer. » Si l'email bilan arrive : « email facultatif » |
| « Données sur le téléphone » | Oui avec nuance | Architecture, politique de confidentialité | « Les profils et progrès restent sur votre téléphone. Le micro, si vous l'activez, passe par la reconnaissance vocale du téléphone (Google ou Apple). » |
| « Hors connexion » | **Nuancer** | Test en mode avion | « L'essentiel fonctionne sans Internet (sauf vidéos et voix). » Jamais « 100 % hors ligne » (la compétence le dit, mais la notice parents dit l'inverse pour vidéos et micro) |
| « De 4 ans à l'âge adulte », « 4 profils » | Oui | Fonctionnalité | Tel quel |
| « ~7 900 questions vérifiées » | Oui si daté et comptable | Export du nombre + procédure de vérification (moulinette) | « Plus de 7 800 questions vérifiées (novembre 2026) » : arrondir **en dessous** |
| « Par niveau scolaire, de la GS au lycée » | Oui | Tableau questions par niveau | Préférer à « conforme aux programmes » |
| « Conforme au programme de l'Éducation nationale » | **Seulement** avec une correspondance documentée par thème | Tableau thème ↔ programme (Eduscol), relu par un enseignant | « Inspiré des programmes officiels » ; jamais de logo ni de suggestion d'agrément du ministère |
| « 9 langues », « dans la langue de l'enfant » | Oui | Liste | **Harmoniser** : la notice dit « 10 langues » en couverture et « 9 langues » au module Langues, le contexte parle de ~20 langues maternelles. Choisir une formule unique : « 9 langues à apprendre, l'appli dans 10 langues et plus » |
| « 13 modules » | **À corriger** | — | La notice annonce 13 modules et en liste 14 (avec l'Espace Parents) : dire « 13 activités + un Espace Parents » |
| « Un défi physique toutes les 5 questions » | Oui avec précision | Réglage | « Une pause active toutes les 3 à 8 questions selon l'âge » |
| « Révision espacée : les cartes reviennent après 2, 7 et 21 jours » | Oui (description de la fonction) | Code | Ne pas ajouter « retenez 2× plus » |
| « Essai gratuit 7 jours » | Oui avec conditions | Écran d'offre | Prix après essai, renouvellement auto et moyen d'annuler **sur le même écran** |
| « Résiliable à tout moment » | Oui | Lien vers l'abonnement du store | « Annulation à tout moment depuis votre compte Google Play ou App Store », plutôt que « en 1 clic » si ce n'est pas littéral |
| « Moins cher que X » | Possible (publicité comparative, art. L122-1 Code conso) mais risqué | Capture datée du prix concurrent, même périmètre | **Éviter de nommer des concurrents au lancement.** Dire plutôt « un seul prix pour toute la famille » |
| « Conçu pour respecter le RGPD » | Oui | Registre, politique relue par juriste | Jamais « certifié RGPD » ni « 100 % sécurisé » |
| Témoignage de parent bêta | Oui | Accord écrit daté, texte exact, **mention si contrepartie** (accès gratuit = avantage) | Prénom + ville + âge de l'enfant, avec accord ; jamais reformulé au point d'en changer le sens |
| Vidéo avec un enfant | Oui avec précautions | **Accord écrit des deux titulaires de l'autorité parentale** ; loi n° 2020-1266 si l'activité devient régulière et rémunérée | Visage non obligatoire (mains, écran, voix) |
| Créateur partenaire | Oui | Contrat, brief conformité | Mention « Publicité » ou « Collaboration commerciale » (loi n° 2023-451 du 9/06/2023) |

### 4.2 Affirmations à NE PAS faire

| Interdit | Pourquoi | Alternative |
|---|---|---|
| « Améliore les notes de 30 % », « +2 points en maths », « augmente le QI ou la concentration » | Allégation d'efficacité sans étude = pratique commerciale trompeuse (art. L121-2 Code conso). Précédent : **Lumosity, 2 M$ à la FTC (05/01/2016)** pour des allégations non prouvées | « Des séances courtes au bon niveau, avec un indice pour comprendre » |
| « Cliniquement prouvé », « validé par les neurosciences », « recommandé par les orthophonistes » | Aucune étude ni caution écrite | Faire une **étude pilote réelle** (ex. 30 familles, avant/après), puis communiquer *exactement* ce qu'elle montre |
| Toute allusion au TDAH, aux dys, à l'autisme, à l'anxiété, aux « troubles de l'attention » ; « votre enfant n'arrive pas à se concentrer ? » | Allégation de santé + politique Meta « attributs personnels » + règle interne | « Des séances courtes, des pauses qui font bouger, un mode calme le soir » |
| « Soigne l'addiction aux écrans », « détox digitale » | Vocabulaire médical | « Une alternative au scroll », « l'écran qui sait s'arrêter » |
| « Rend bilingue », « parle anglais en 30 jours » | Résultat non prouvé | « Découvrir 9 langues et entendre la bonne prononciation » |
| « Corrige votre accent » | La reconnaissance actuelle devine le mot, elle ne note pas l'accent | « Un retour immédiat : Parfait, Presque, Réessaie » |
| « Remplace le soutien scolaire / le professeur » | Trompeur, et dévalorise les éducateurs (ARPP Enfant 2.3) | « Un complément de 15 minutes, à la maison ou en voiture » |
| « Approuvé par les enseignants », « Teacher Approved » | Seulement si le programme Google l'a effectivement accordé | Candidater (section 5), puis afficher le badge officiel |
| « N°1 », « la meilleure appli éducative » | Superlatif invérifiable | Faits mesurables |
| « Gratuit » seul | L'essentiel est payant | « Gratuit chaque jour, avec une limite quotidienne », « essai gratuit 7 jours » |
| « Plus que 24 h », compte à rebours, « offre réservée » permanente | Fausse urgence (pratique trompeuse ; ARPP Enfant 7.2) | Vraies promos datées uniquement |
| Côté enfant : « Demande à tes parents… », « Débloque tout ! », « Tes amis ont déjà le premium » | Interdit : directive 2005/29/CE, annexe I point 28 ; ARPP Enfant 7.1 et 7.4 ; règles stores | « Bravo, séance terminée ! Montre à tes parents ce que tu as appris. À demain ! » |
| Pubs ciblant les moins de 15 ans, ou personnalisées pour des mineurs | DSA art. 28, politique Google Familles, plateformes | Viser les parents (adultes). Les ados viennent par l'organique |
| Faux avis, avis achetés, comptes fictifs, avis de l'équipe non signalés | Pratique trompeuse (dont la directive Omnibus), bannissement des stores | Bêta-testeurs réels, demande d'avis native côté parent |
| Citer ElevenLabs, Google, Microsoft, etc. dans les pitchs | Règle interne | « Voix Sensei », « Voix Narrateur » |
| Montrer ou commercialiser en Russie et en Chine | Règle interne (langues RU/ZH = contenu, pas des marchés) | Exclure ces pays dans les consoles stores |

### 4.3 Points de vigilance stores (à relire sur les textes officiels avant soumission)

- **Apple, catégorie Enfants (règle 1.3)** : pas de publicité ni d'analytics tiers, **barrière parentale** avant tout lien externe, achat ou demande d'avis, tranche d'âge à choisir (5 ans et moins, 6-8 ou 9-11). D'après ma lecture de la règle, une appli **hors** catégorie Enfants ne doit pas utiliser « pour enfants » dans ses métadonnées. **Texte officiel inaccessible depuis cet environnement : à revérifier.** Conséquence : décider *avant* la fiche si l'appli va en catégorie Enfants (tranche 6-8 ou 9-11, alors qu'elle couvre aussi les adultes) ou en Éducation générale avec un vocabulaire « famille ».
- **Google Play Familles** : SDK certifiés Familles uniquement, aucun identifiant publicitaire (AAID) ni localisation précise pour un public enfant, pas de pub personnalisée, déclaration exacte du public cible et du formulaire Sécurité des données, et **« ne pas être une simple webview »**. Point critique pour une PWA : empaqueter avec une vraie valeur native (hors-ligne, audio, notifications parent, achats in-app).
- **Compteur anonyme de réponses** : vérifier qu'il n'envoie aucun identifiant d'appareil et qu'il est déclaré (Apple : « données non liées à l'identité » ; Google : formulaire Sécurité des données).
- **Achats in-app** obligatoires via les stores, déclenchés **uniquement** dans l'Espace Parents après barrière parentale.
- **CNIL** : en France, l'enfant consent seul à partir de 15 ans ; en dessous, accord parental (recommandations du 01/06/2021). La case « offres » doit être séparée et non cochée (déjà prévu dans le README).

---

## 5. Checklist de préparation au lancement

### P0 : bloquant avant la soumission

**Stores et conformité**
- [ ] Choisir le mode d'empaquetage (TWA pour Android, Capacitor ou équivalent pour iOS) et lister les fonctions natives qui écartent le refus « webview » ou « fonctionnalité minimale »
- [ ] Décider : Apple catégorie Enfants (quelle tranche ?) ou Éducation ; Google « public cible » (avec ou sans adultes, donc audience mixte avec écran d'âge neutre)
- [ ] Remplir Sécurité des données (Google) et étiquette de confidentialité (Apple), cohérentes avec la politique de confidentialité et avec le micro
- [ ] Questionnaire IARC et classification d'âge
- [ ] Exclure Russie et Chine des pays de distribution
- [ ] Abonnements configurés : Famille mensuel et annuel, essai 7 jours, prix TTC par pays, période de grâce, page « Gérer mon abonnement »
- [ ] Barrière parentale avant achat, lien externe, demande d'avis et email
- [ ] Code parent par défaut (1234) dont le changement est forcé au premier passage dans l'Espace Parents
- [ ] Politique de confidentialité, CGU/CGV, mentions légales **relues par un juriste** (déjà noté dans le README)
- [ ] Test sur un Android d'entrée de gamme et un vieil iPhone (plantages = plainte n°8)

**Fiche store / ASO (FR d'abord, puis EN, ES, DE, IT, PT, AR)**
- [ ] **Titre** (30 caractères) : piste « PocketSage : apprendre en famille »
- [ ] **Sous-titre Apple / description courte Google** (30 / 80 caractères) : « Quiz, langues, sport. Sans pub. » / « Le temps d'écran sans culpabilité : quiz GS-lycée, 9 langues, sport, sans pub »
- [ ] **Mots-clés Apple** (100 caractères), à tester : révision, tables de multiplication, anglais, culture générale, quiz, CP, CE1, CM2, collège, sans pub, famille, langues. Pas de noms de concurrents (interdit)
- [ ] **Description longue** : promesse, 3 piliers, liste des modules, encadré « Ce que nous ne ferons jamais » (pub, coffres, séries culpabilisantes, chat), prix et conditions de l'essai
- [ ] **Captures (6 à 8, portrait)**, chacune avec un bénéfice en gros titre :
  1. Promesse + senseï (« Le temps d'écran dont vous n'avez pas à vous sentir coupable »)
  2. Aventure + défi physique (« On apprend, on bouge »)
  3. Flash avec la source et la question de révision (« Le scroll qui rend plus malin »)
  4. Langues + choix de la langue maternelle (« Dans la langue de chaque enfant »)
  5. Mon Monde (« Sa ville grandit quand il apprend. Sans coffres, sans pub »)
  6. Espace Parents + bilan (« Vous voyez ce qu'il a appris »)
  7. 4 profils de 4 ans à l'adulte (« Un abonnement pour toute la famille »)
  8. Fiches PDF / mode nuit (« Et quand l'écran s'éteint… »)
- [ ] **Vidéo d'aperçu** 15-30 s, captation de l'appli uniquement (Apple l'exige), sous-titrée
- [ ] Captures sans fausse note : aucun faux score 5★, aucun faux avis dans les visuels

### P1 : avant d'ouvrir la vente au public

**Page web (pocketsage.org)**
- [ ] Page parents : promesse, 3 piliers, démo vidéo, prix clair, FAQ (données, micro, annulation, hors-ligne)
- [ ] Page « Comment annuler » (Google Play / App Store, pas à pas)
- [ ] Page « Nos engagements » (reprendre les 8 engagements de Mon Monde, étendus à toute l'appli)
- [ ] Notice parents PDF téléchargeable (déjà prête ; corriger les incohérences « 10 / 9 langues » et « 13 modules »)
- [ ] Kit presse : fondateur, chiffres datés, captures, angle loi < 15 ans et DSA
- [ ] SEO : 5 articles (« alternative à TikTok pour enfant », « appli éducative famille sans pub », « réviser les tables de multiplication », « appli pour enfant expatrié qui garde sa langue », « que faire au lieu de scroller »)

**Preuves sociales réelles**
- [ ] Recueillir 10-20 **témoignages écrits signés** de familles bêta (accord daté, contrepartie mentionnée)
- [ ] 1 ou 2 **enseignants testeurs** nommés, avec leur accord, sur les fiches PDF
- [ ] Demande d'avis **native** (SKStoreReviewController / In-App Review API) déclenchée **uniquement dans l'Espace Parents**, après un moment positif (bilan de la semaine), jamais côté enfant
- [ ] Candidature **Google Play Teacher Approved** dès la conformité Familles
- [ ] Étudier l'éligibilité au label ministériel « Reconnu d'intérêt pédagogique » (à vérifier) et à un référencement Canopé
- [ ] **Étude pilote honnête** : 30 familles pendant 4 semaines, mesure simple (ex. cartes Flash ancrées, ressenti du parent). Publier la méthode et les limites. C'est la seule voie vers une allégation d'efficacité

### P2 : premières semaines

- [ ] Test A/B de la promesse (« sans culpabilité » contre « qui sait s'arrêter ») : une métrique, une semaine
- [ ] Suivi des avis stores chaque semaine, réponse à 100 % des avis négatifs (Lingokids le fait, et ça se voit)
- [ ] Partenariats bloqueurs et contrôle parental (voir doc Flash)
- [ ] Créateurs parents micro (1-50 k), brief de conformité, mention « Collaboration commerciale »

---

## 6. Top 3 : synthèse pour décision

| Manques du marché | Arguments différenciants | Risques |
|---|---|---|
| 1. **Une appli qui suit l'enfant de 4 ans à l'âge adulte** avec un prix famille (tous s'arrêtent à 8 ans ou ne font que du scolaire) | 1. **4 ans → adulte, 4 profils, un abonnement**, dans la langue maternelle de chaque enfant | 1. **Refus store** de la PWA (webview / fonctionnalité minimale) et choix de catégorie Apple Kids, qui conditionne le vocabulaire |
| 2. **Un bilan parent qui dit ce qui a été appris** (les concurrents montrent du temps passé, pas du savoir retenu) ; à construire chez nous | 2. **On apprend, on bouge, puis on pose le téléphone** : pauses physiques, fin de séance, pas de coffres ni de séries culpabilisantes (le contre-modèle de Prodigy) | 2. **Allégations éducatives ou santé non prouvées** (efficacité, TDAH/dys, « bilingue », « conforme au programme ») et incohérences de chiffres (9/10 langues, 13/14 modules, « 100 % hors-ligne ») |
| 3. **Une reconnaissance vocale juste pour enfants** et un **apprentissage de la lecture en français à la maison** (Lalilo sans gratuit, Duolingo ABC en anglais) | 3. **Zéro pub, zéro compte, données sur le téléphone**, avec un abonnement transparent, face à la plainte n°1 du marché (argent et essais pièges) | 3. **Concurrence gratuite de haute qualité** (Khan Kids, Lumni, Duolingo ABC) + 0 avis au lancement : sans preuve sociale réelle et sans une offre gratuite qui donne vraiment envie, la conversion sera faible |

---

## 7. Sources

**Concurrents : prix, notes, avis**
- [Khan Academy Kids — App Store (consulté le 15/11/2026)](https://apps.apple.com/app/khan-academy-kids-learning/id1378467217)
- [5 Kids Learning Apps Ranked by 1-Star Reviews (Unstar, 16/06/2026)](https://unstar.app/blog/abcmouse-khan-academy-kids-duolingo-abc-homer-outschool-learning-apps-ranked-2026)
- [Kids & parenting app reviews: what parents complain about (Unstar, 16/04/2026)](https://unstar.app/blog/kids-parenting-app-reviews-what-parents-complain-about-2026)
- [Duolingo Max / Super Family Plan Price 2026 (duolingoguides, 10/2026)](https://duolingoguides.com/?p=7322)
- [Duolingo : new subjects, maths et musique (blog Duolingo, 11/10/2023)](https://blog.duolingo.com/new-subjects/)
- [Learn to Read – Duolingo ABC, rapport (Marlvel, 29/03/2026)](https://marlvel.ai/intel-report/education/learn-to-read-duolingo-abc)
- [Duolingo T2 2026 results (GlobeNewswire)](https://www.globenewswire.com/de/news-release/2026/08/05/3339653/0/en/duolingo-reports-second-quarter-2026-results.html)
- [Lalilo : différences et tarifs (aide Lalilo, 30/03/2026)](https://intercom.help/lalilo/en/articles/5676123-lalilo-differences-and-pricing)
- [Lalilo : utiliser Lalilo à la maison (aide Lalilo)](https://intercom.help/lalilo/en/articles/2285320-utiliser-lalilo-a-la-maison)
- [Kahoot!+ Kids — tarifs (Kahoot!, consulté le 15/11/2026, promo Black Friday)](https://kahoot.com/register/pricing-kahoot-kids/)
- [How Much Does Prodigy Membership Cost? (ThePricer, 04/03/2026)](https://www.thepricer.org/how-much-does-prodigy-membership-cost/)
- [7 reasons to say no to Prodigy (Fairplay, mis à jour le 10/04/2025)](https://fairplayforkids.org/?p=26304)
- [Prodigy target of complaint to FTC (Education Week, 02/2021)](https://www.edweek.org/technology/popular-interactive-math-game-prodigy-is-target-of-complaint-to-federal-trade-commission/2021/02)
- [Adibou par Wiloki — App Store FR (15/11/2026)](https://apps.apple.com/FR/app/id1599757063)
- [Holy Owly — App Store FR (15/11/2026)](https://apps.apple.com/FR/app/id1189063739)
- [Mathador Flash & Plato — App Store FR (15/11/2026)](https://apps.apple.com/fr/app/mathador-flash-plato-jeux-de-calcul-mental-pour-la-famille/id998841218)
- [Lumni, communiqué France Télévisions (04/05/2026)](https://www.francetvpro.fr/contenu-de-presse/76977586)
- [SchoolMouv — site (15/11/2026)](https://www.schoolmouv.fr/)
- [Abonnement SchoolMouv pas cher (Bons Plans Malins, mis à jour le 12/04/2022)](https://www.bons-plans-malins.com/abonnement-schoolmouv-pas-cher-accompagnement-scolaire-en-ligne-du-college-et-lycee/)
- [Kartable — App Store FR (15/11/2026)](https://apps.apple.com/FR/app/id825500330)
- [Brainly AI Review 2026 (Fast.io, 28/06/2026)](https://fast.io/resources/brainly-ai-review-2026/)
- [Lingokids — App Store FR (15/11/2026)](https://apps.apple.com/FR/app/id1002043426)
- [Lingokids — Trustpilot FR (15/11/2026)](https://fr.trustpilot.com/review/lingokids.com)
- [Blinkist Premium prices (blog Blinkist, 06/2023)](https://www.blinkist.com/magazine/posts/how-much-do-blinkists-premium-subscriptions-cost)
- [How much does Simply Piano cost (ThePricer, 05/2026)](https://www.thepricer.org/how-much-does-simply-piano-cost/)
- Anti-scroll (Deepstash, Headway, Imprint, Nibble…) : voir les sources de `docs/flash/01_concurrents_antiscroll.md`

**Sondages parents**
- [Parents say kids' screentime should be interactive (Lingokids, 28/07/2026, source concurrente)](https://lingokids.com/press/parents-say-their-kids-screentime-should-be-interactive-not-passive)
- [Parents don't hate ed tech, they want balanced use (Education Week, 26/06/2026)](https://www.edweek.org/technology/parents-dont-hate-ed-tech-they-just-want-more-balanced-use/2026/06)

**Réglementation et allégations**
- [Lumosity to pay $2 million to settle FTC deceptive advertising charges (FTC, 05/01/2016)](https://ftc.gov/news-events/press-releases/2016/01/lumosity-pay-2-million-settle-ftc-deceptive-advertising-charges)
- [Recommandation Enfant (ARPP, version 2004)](https://www.arpp.org/IMG/pdf/Reco_Enfant.pdf)
- [La CNIL publie 8 recommandations pour la protection des mineurs en ligne (CNIL, 01/06/2021)](https://www.cnil.fr/la-cnil-publie-8-recommandations-pour-renforcer-la-protection-des-mineurs-en-ligne)
- [Résiliation en trois clics : obligations (donneespersonnelles.fr)](https://www.donneespersonnelles.fr/resiliation-en-trois-clics)
- [Google Play Families policy (aide Play Console)](https://support.google.com/googleplay/android-developer/answer/9893335?hl=en)
- [Apple App Store Review Guidelines, règle 1.3 Kids Category (à relire sur le texte officiel)](https://developer.apple.com/app-store/review/guidelines/)
- [Loi réseaux sociaux < 15 ans définitivement adoptée (Blog du Modérateur, 22/07/2026)](https://www.blogdumoderateur.com/france-loi-bannit-mineurs-moins-15-ans-reseaux-sociaux/)
- [Lignes directrices DSA pour les mineurs (e-Enfance)](https://e-enfance.org/en/the-new-dsa-guidelines-to-protect-children-on-the-internet/)

*Cités de mémoire, à faire vérifier par le juriste : directive 2005/29/CE annexe I point 28 ; art. L121-2 et L122-1 du Code de la consommation ; loi n° 2020-1266 du 19/10/2020 (image des enfants de moins de 16 ans) ; loi n° 2023-451 du 9/06/2023 (influenceurs) ; DSA art. 28.*

---

## Ajout du 18/11/2026 — Tikino (tikino.fr)

**Ce que c'est** : pas une appli éducative, mais un **petit projecteur pour enfants de 3 à 10 ans** qui projette au mur des histoires animées (400+ titres : contes, documentaires, animations, musique classique). L'appli ne sert qu'aux parents (connexion du projecteur, catalogue, bibliothèque). Créé par trois mamans, soutenu par Bpifrance, CNC, Paris&Co, Wilco.

**Positionnement** : « l'alternative à l'écran » — lumière douce indirecte, pas de lumière bleue directe, pas de pub, pas d'algorithme, animation lente, visionnage partagé en famille. Catalogues par âge (3 ans / 4-5 ans / 6+), chaque histoire avec âge, résumé et « mot de l'équipe ».

**Modèle** : vente du projecteur + histoires (prix non publiés sur les pages consultées), boutique avec **carte cadeau**, parrainage, fidélité, **sélection écoles**.

**Ce qu'on en retient pour PocketSage**
| Idée | Statut |
|---|---|
| Mode « écran noir » le soir : la voix seule, écran éteint (un tap rallume) | ✅ fait le 18/11 (v74) |
| Envoi du son sur enceinte / TV (AirPlay, Chromecast) | ✅ fait le 18/11 (v74) |
| Nuit relookée lisible : texte crème chaud, aucun bloc clair éblouissant | ✅ fait le 18/11 (v74) |
| « Mot de l'équipe » + âge + bénéfice sur chaque histoire | à faire (peu coûteux, rassure les parents) |
| Mode famille sur la TV (quiz / histoire en grand via recopie d'écran) | à faire |
| Carte cadeau, sélection écoles, parrainage | voir `04_carte_cadeau.md` |
| Raconter l'histoire du fondateur (papa à Monaco + enfants bêta-testeurs) | à intégrer aux vidéos |

**Non concurrent direct** (matériel, 3-10 ans, pas de quiz ni de langues) mais **même cible de parents** « moins d'écran, plus de qualité » → **partenariat possible** plus tard (offre croisée, coffret Noël).

Message utilisable (honnête) : « Le soir, l'écran s'éteint : seule la voix reste. » — ne pas promettre d'effet santé (lumière bleue, sommeil) sans source solide.

Sources : [Tikino — App Store](https://apps.apple.com/mx/app/tikino/id1568435696) · [Tikino — notre histoire](https://tikino.fr/en/pages/notre-histoire)
