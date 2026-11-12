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
| **Blocs Sensei** (pas « Tetris », marque déposée) | blocs qui tombent, lignes à compléter ; option : un bloc spécial = une question | logique spatiale, anticipation | 6+ | ~1 session |
| Simon Sensei | répéter une suite de couleurs/sons qui s'allonge | mémoire de travail | 4+ | petit |
| Grille mémoire | des cases s'allument, les retrouver | mémoire visuelle | 5+ | petit |
| Réflexes | toucher quand ça devient vert, pas avant | vitesse de réaction, inhibition | 4+ | petit |
| Table de Schulte | toucher 1→25 le plus vite possible | attention, regard | 8+ | petit |
| Stroop couleurs | dire la couleur de l'encre, pas le mot | concentration | 7+ | petit |
| Sudoku junior | 4×4 puis 6×6 | logique | 6+ | moyen |
| Tangram | reconstituer une forme avec 7 pièces | géométrie | 6+ | moyen |
| Labyrinthe | sortir d'un labyrinthe généré | planification | 4+ | petit |
| Mots mêlés | retrouver des mots (dans la langue apprise !) | vocabulaire | 7+ | petit |

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
- ⏳ Lot 2 proposé : Snake (fond noir vide), Mastermind, Anagrammes/Bombe de mots, Mot caché.
