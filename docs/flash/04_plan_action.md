# Flash : plan d'action (10/11/2026)

Synthèse de `01_concurrents_antiscroll.md` et `02_sources_contenu.md`. Cocher au fur et à mesure.

## Positionnement

**« Le scroll qui rend plus malin, pour toute la famille. »**
Les applis anti-scroll existantes (Deepstash, Headway, Imprint, Nibble, Blinkist) visent toutes l'adulte seul, à 70-240 $/an par personne, avec du swipe passif. PocketSage occupe la place libre : un fil de curiosité **par âge (4-18 ans + parents)**, **multilingue avec audio**, **sans pub, hors-ligne**, qui **vérifie qu'on retient** et qui **pousse à décrocher**.

## Étape 0 : sécurité (avant tout le reste)

- [ ] Régénérer les clés Google, ElevenLabs et R2, puis révoquer les anciennes (détail : `03_procedures_mp3_traductions.md` §6).
- [ ] Retirer les clés du code (variables d'environnement / GitHub Secrets) et ne plus appeler ElevenLabs depuis le navigateur.

## Étape 1 : rendre le Flash « produit » (environ 1 semaine)

Par ordre d'impact :
1. [ ] **Sortir les cartes de `index.html`** vers `data/flash/fr.json` (lazy-load, comme les langues). C'est la condition pour passer à 1000+ cartes sans alourdir l'app.
2. [ ] **Nouveau format de carte** : titre / idée / *Essaie aujourd'hui* / question de rappel (QCM 3 choix) / source (nom + URL + licence) / âge. Une version enfant et une version adulte quand c'est utile.
3. [ ] **Filtre par âge du profil** (le champ `age` existe déjà).
4. [ ] **Swipe vertical plein écran** + tap pour l'audio.
5. [ ] **Audio MP3 R2** dans `renderFlashCard()`, voix du téléphone en secours, et **affichage traduit** selon la langue du profil.
6. [ ] **Favoris / collections**, gratuits (contrairement au paywall Deepstash).
7. [ ] **Rappel espacé** : les cartes vues reviennent sous forme de question à J+2, J+7 et J+21, avec points et réaction de l'avatar. C'est notre principal différenciateur.
8. [ ] **Fin de session volontaire** : après 10 cartes, « Tu as appris 10 choses, défi physique ou pause ? ». C'est le design non addictif, à mettre en avant (DSA).
9. [ ] **Série quotidienne + ligue familiale** entre profils (mécanique Duolingo/Mimo).
10. [ ] **Bilan parent** : ce que chaque enfant a vu et retenu cette semaine, plus une question à lui poser au dîner.

## Étape 2 : contenu (de 151 à 1000+ cartes)

- [ ] Corriger les cartes signalées : CF-001 (power pose : l'effet hormonal n'a pas été reproduit), MO-001 (trop proche de James Clear), EJ-001, EM-002, PS-002 (à nuancer).
- [ ] Ajouter le champ `source` aux 151 cartes existantes.
- [ ] Cycles de 275 cartes (25 × 11 catégories) générées par lots **à partir de faits sourcés**, puis relues (1-2 min par carte). 4 cycles ≈ 1100 cartes.
- [ ] Nouvelles catégories à envisager : **Parents** (éducation, sommeil, écrans, sans avis médical), **Adultes** (biais, histoire, sciences), **Langues** (une expression par jour, en lien avec le module Langues).
- [ ] Sources prioritaires : Wikidata (CC0), NASA/NOAA (domaine public US), Smithsonian Open Access (CC0), Wikisource/Gutenberg (citations du domaine public), études scientifiques citées (fait libre, texte réécrit).
- [ ] À éviter : OpenStax, CK-12, Khan Academy, OMS (pas d'usage commercial) ; copier un texte Wikipedia (ShareAlike) ; résumés de livres récents ; cartes Deepstash.
- [ ] Après chaque lot : `generate_flash_tts.py` (adapté pour lire le JSON + empreinte du texte), puis push.

## Étape 3 : communication

- [ ] Page d'accueil / store : « Le scroll qui rend plus malin », « Un abonnement, toute la famille, 7 langues », « Pas de pub. Pas d'algorithme. Une vraie fin. » (10 accroches dans `01` §6).
- [ ] Prix : **un abonnement famille** sous le prix individuel des concurrents (ex. 5-7 €/mois ou 40-50 €/an, à tester), avec annulation en 1 clic et sans essai piège. Ce sont les plaintes n°1 contre Headway et Deepstash.
- [ ] Actualité : loi « réseaux sociaux < 15 ans » (statut à vérifier), recommandations de la commission écrans, DSA. Communiqué « l'alternative éducative au scroll ».
- [ ] Canaux : groupes de parents, Instagram parentalité, écoles et APE (avec les fiches PDF imprimables comme produit d'appel), orthophonistes et pharmacies, défis « 7 jours sans TikTok » avec des créateurs ados.
- [ ] Partenariats : bloqueurs (one sec, ScreenZen, Jomo) et contrôle parental, en mode « bloquez, puis ouvrez PocketSage ».
- [ ] SEO multilingue : « alternative à TikTok pour enfant », « quoi faire au lieu de scroller », « appli éducative famille sans pub ».
