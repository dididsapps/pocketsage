# Consigne — « Parcours de la semaine » PocketSage (super-pouvoirs)

Tu écris UN parcours de 5 jours (lundi → vendredi), 10 minutes par jour, pour enfants de 4 à 12 ans (avec variantes petits 4-6 / grands 7-12). Français, tutoiement pour l'enfant, vouvoiement dans les textes parents.

Chaque jour = 3 temps :
1. **Un jeu de l'appli** (existant) choisi dans la liste ci-dessous, avec une phrase « pourquoi ce jeu aujourd'hui » pour le parent.
2. **Une activité SANS écran, guidée à la voix** (c'est le cœur du parcours) : 2 à 4 minutes, jouable dans une chambre ou un salon, sans matériel ou avec du matériel de maison (papier, crayon, coussin…). Le téléphone est posé, la voix guide. Écris le **script lu par la voix** : consignes courtes, concrètes, joyeuses, avec des pauses `[P2]` `[P3]` `[P5]` (secondes) quand l'enfant agit. Jeux de type « s'arrêter au signal », imitation, mémoire, attention, nommer ses émotions, recommencer… Variante petits / grands en une phrase chacune.
3. **Un moment calme** : référence à un contenu existant (méditation, histoire respirée) OU un mini-script de respiration de 30-60 s.

## Contenus existants utilisables
Jeux : memory (paires), calcul (calcul mental), quiz (quiz rapidité), mastermind (code), anagrammes, motcache (mot caché), sort (classer), taquin (puzzle coulissant), hanoi (tour de Hanoï), blocs (type Tetris), simon (Simon : répéter une suite de couleurs), grille (grille mémoire : retrouver les cases allumées), reflexes (toucher dès que c'est vert), schulte (table de Schulte : nombres dans l'ordre), stroop (couleurs piégées : couleur de l'encre et pas le mot), sudoku (sudoku junior), laby (labyrinthe).
Calme : MED-001 Respiration de la fleur (4-8), MED-002 Voyage dans les nuages (4-10), MED-003 Respiration du lion (4-12), HR-001 Le Jardin Secret, HR-002 Voyage sous les étoiles, HR-003 La Baleine Bleue, HR-004 La Forêt Enchantée, HR-005 La Neige Douce (histoires respirées 1-2 min).

## Règles (non négociables)
- AUCUNE promesse de santé ou de résultat (pas de « soigne », « guérit », « TDAH », « dys », « système nerveux », « cerveau réparé », « prouvé »). On dit « s'entraîner à… », « jouer à… ».
- Activités sûres : pas de course dans la maison près des meubles, pas de yeux bandés en hauteur, pas d'objets à mettre en bouche, pas d'obscurité, rien d'humiliant. Toujours réussissable, l'erreur est drôle et on recommence.
- Variété : 5 activités sans écran DIFFÉRENTES, noms courts et donnant envie (ex. « La statue musicale », « Le robot télécommandé »).
- Le parent peut jouer avec (1 phrase « Pour jouer à deux » par activité, facultatif).
- Phrases simples (les petits écoutent seuls), pas d'emoji dans les scripts, pas de symboles.

## Sortie
JSON dans le fichier indiqué :
{"id":"…","nom_enfant":"emoji + nom de super-pouvoir","nom_parent":"…","accroche_parent":"1-2 phrases honnêtes pour le parent","pour_qui":"4-12 ans",
 "jours":[{"jour":"Lundi","theme":"…","jeu":{"id":"…","pourquoi":"…"},
   "activite":{"id":"<ID>-J1","titre":"…","duree_min":3,"materiel":"aucun|…","script":"…","petits":"…","grands":"…","a_deux":"…"},
   "calme":{"ref":"MED-003"} ou {"script":"…"}} … 5 jours],
 "fiche":{"titre":"Mon programme de la semaine — …","defi_bonus":"un petit défi pour le week-end, sans écran"}}
Vérifie le JSON avec Python. Ne modifie aucun autre fichier. Réponds en français : titre du parcours + liste des 5 activités en une ligne chacune.
