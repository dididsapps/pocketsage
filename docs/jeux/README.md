# Dossier Jeux PocketSage (ouvert le 12/11/2026)

Pour ne pas perdre le fil : idées, priorités, décisions. Rien n'est codé tant que ce n'est pas marqué ✅.

- `mon_monde.md` — Mon Monde v2 : visuels, mode « Ma vie », groupe familial (5 max), phases.
- `economie.md` — gains et dépenses de jetons recalibrés.

## 1. Mini-jeux existants (12, dans `js/jeux.js`)
memory, calcul, quiz, mastermind, paires, anagrammes, motcache, snake, sort (tri de couleurs), taquin, hanoi, 2048.
- ✅ 12/11 : minuteurs réparés (Quiz Rapide faisait planter les autres jeux).
- ✅ 12/11 : jeux sortis de index.html dans `js/jeux.js` (économie de crédits).
- ✅ 12/11 : lot 1 embelli (voir §4).

## 2. Nouveaux jeux proposés
| Jeu | Principe | Ce que ça travaille | Âge | Coût |
|---|---|---|---|---|
| ✅ **Blocs Sensei** (pas « Tetris », marque déposée) | blocs qui tombent, lignes à compléter ; option : un bloc spécial = une question | logique spatiale, anticipation | 6+ | ~1 session |
| ✅ Simon Sensei | répéter une suite de couleurs/sons qui s'allonge | mémoire de travail | 4+ | petit |
| ✅ Grille mémoire | des cases s'allument, les retrouver | mémoire visuelle | 5+ | petit |
| ✅ Réflexes | toucher quand ça devient vert, pas avant | vitesse de réaction, inhibition | 4+ | petit |
| ✅ Table de Schulte | toucher 1→25 le plus vite possible | attention, regard | 8+ | petit |
| ✅ Couleurs piégées (Stroop) | dire la couleur de l'encre, pas le mot | concentration | 7+ | petit |
| ✅ Sudoku junior | 4×4 puis 6×6 | logique | 6+ | moyen |
| Tangram | reconstituer une forme avec 7 pièces | géométrie | 6+ | moyen |
| ✅ Labyrinthe | sortir d'un labyrinthe généré | planification | 4+ | petit |
| ✅ Mots mêlés | retrouver des mots (dans la langue apprise !) | vocabulaire | 7+ | petit |

- ✅ 12/11 : les 8 jeux ci-dessus créés dans `js/jeux-cerveau.js` (adaptés à l'âge : taille de grille, vitesse). Tangram reporté (déplacer/tourner des pièces au doigt = plus long).
- ✅ 12/11 — **Limite de jeu TOTALE** (tous jeux confondus), par profil :
  - Offre **gratuite : 15 min/jour** (fixe). **Abonnés : 45 min par défaut**, réglable par le parent dans l'Espace Parents (15, 30, 45, 60, 90, 120 min ou illimité).
  - Message « Plus que 5 minutes » une fois par jour ; la partie en cours s'arrête quand le temps est écoulé.
  - Écran de fin : **fiche PDF à imprimer dans tous les cas** ; **histoire** et **aventure de questions** si l'abonnement le permet (gratuit : message « avec l'abonnement Famille »).
  - Tant que les abonnements n'existent pas (bêta), tout le monde est traité comme abonné (`psaPlan()` lit `psa3_plan`, défaut « famille »). À brancher sur le vrai abonnement au lancement.
  - Bug corrigé : le temps d'une partie était compté deux fois si on quittait après l'écran de fin.

## 3. Ordre conseillé
1. Embellir les jeux existants (par lots de 3-4) ← en cours
2. Blocs Sensei
3. Mon Monde phase 1 (visuels)
4. 2-3 petits jeux de réflexion (Simon, Réflexes, Grille mémoire)
5. Mon Monde phases 2-4 (manèges, « Ma vie », économie)
6. Hors ligne + images allégées : **le jour de la préparation des stores**

## 4. Embellissement des jeux — suivi
(mis à jour au fil des lots)
- ✅ **Lot 1 (12/11)** — Memory (cartes dos étoilé + retournement, paire trouvée qui brille), Calcul Éclair (tableau noir + boutons bonbons), Quiz Rapidité (carte question + 4 réponses colorées, barre de temps vert→rouge), Paires (cartes FR/langue avec bandes de couleur, ✓ sur les paires trouvées). Jour et nuit. Fichier `css/jeux.css`.
- ✅ Bug corrigé : quitter un jeu juste après une réponse faisait réapparaître l'ancien jeu par-dessus le suivant (minuteries de 0,5-1 s non annulées).
- ✅ **12/11** — Snake : terrain herbe + bordure de sable (jour), fond noir (nuit), yeux qui regardent où il va ; **pavé tactile géant** : le terrain est coupé en 4 triangles (toucher n'importe où vers le haut/bas/gauche/droite), grosses flèches transparentes qui s'éclairent au toucher, glisser le doigt marche aussi, flèches du clavier.
- ✅ **12/11 — Blocs Sensei créé** (13ᵉ jeu) : même pavé + rond central = tourner ; côtés = déplacer (appui long = continue) ; bas = descendre vite ; haut = tout en bas ; ombre de la pièce, pièce suivante, niveaux, vitesse selon l'âge ; **question bonus toutes les 4 lignes** (+20). Marche sur téléphone et tablette (taille calculée selon l'écran).
- ⏳ Lot 2 proposé : Mastermind, Anagrammes, Bombe de mots, Mot caché.

## 5. Sport — Coach Sportif (12/11/2026)
- ✅ Option **🙌 Mains libres** dans la fenêtre « Mode Coach Sportif » (si le micro est autorisé par le parent) : le coach annonce l'exercice, puis on dit **« GO »** (ou « c'est parti », « partez ») pour lancer, **« NEXT »** (ou « suivant », « continue ») pour passer au suivant, **« RÉPÈTE »** pour réentendre. Pastille rouge « 🎤 Dis « GO » » en haut (on peut aussi la toucher). La réussite est notée automatiquement.
- ✅ Pendant l'exercice : **petit bip chaque seconde** (plus aigu sur 3-2-1), le coach annonce **« Encore 20 secondes ! »** toutes les 10 s, puis 3, 2, 1.
- ✅ Phrases du coach en **MP3 voix Google énergique, débit un peu lent (0,95)** : `js/coach-voix.js` (textes) → `tools/sport_texts.js` → `gen_sport_mp3.py` (workflow `sport-tts.yml`, voix Chirp 3 HD « Puck », sinon Neural2-B) → `data/sport/fr.audio.json`. Tant que les MP3 ne sont pas générés : voix du téléphone.
- ✅ Phrase de fin dite à voix haute (écran « temps de jeu terminé ») : « Bravo, séance terminée ! Montre à tes parents ce que tu as appris aujourd'hui. À demain ! »
- Limite : sur Android, le micro fait parfois un petit « bip » quand l'écoute redémarre (comportement du téléphone).
