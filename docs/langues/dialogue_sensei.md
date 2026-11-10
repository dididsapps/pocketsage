# 💬 Parler avec Sensei — dialogue prédictif

Langues → onglet **💬 Parler avec Sensei**. L'enfant a une vraie petite conversation : Sensei pose une question à voix haute, écoute, et **réagit à ce que l'enfant a dit**. Tout est pré-écrit et pré-enregistré (sûr, sans IA générative, sans surprise), mais organisé pour paraître spontané.

## Le principe « prédictif »
Pour chaque question, on **anticipe les réponses probables** (6 à 10) et on enregistre une réaction propre à chacune :
« What's your favourite colour? » → *blue* → « Blue! Like the sky and the sea. I love blue! » ; *pink* → « Pink! Like a flamingo… ».
Réponse non prévue : question **ouverte** (`"open": true`, ex. le prénom) → réaction générique ; question **fermée** → Sensei redemande d'abord, accepte au 2e essai.

## Ce qui rend la conversation naturelle
- **Variantes** : 2-3 formulations par phrase, jamais deux fois la même d'affilée.
- **Temps de réflexion** : 250-600 ms aléatoires avant que Sensei parle ; petits « Mm-hmm! / Oh! » de temps en temps.
- **Réaction instantanée** : les MP3 des réponses possibles sont préchargés pendant que l'enfant parle.
- **Sensei vivant** : GIF « parle » / « réfléchit » (écoute) / « bravo » / « oups ».
- **Écoute automatique** dès que Sensei a fini (pas besoin d'appuyer), micro 🎤 en secours.
- **Jamais bloqué** : 1er raté → « Sorry? Can you say that again? » ; 2e → Sensei propose la phrase modèle + boutons de réponse ; 3e → « Good try! Let's continue. » et on avance.
- **Demandes spontanées comprises partout** : « again / repeat / pardon » → Sensei répète ; « I don't know / je sais pas » → Sensei aide ; « je comprends pas / français » → traduction affichée.

## Petits vs grands
- `petits: true` (4-8 ans) : traduction FR affichée, **boutons-réponses toujours visibles** (on peut toucher OU dire), réponses d'un mot.
- Grands (9 ans +) : boutons cachés tant qu'il n'y a pas de raté, phrases complètes, scénarios à embranchements (le week-end → sport / famille / film…).
- Étoiles : 2 par réponse du premier coup, 1 après une relance ; ajoutées au score du profil.

## Contenu (v1, anglais)
| ID | Scénario | Âge |
|---|---|---|
| EN-D01 | Bonjour Sensei ! (prénom, humeur, couleur, animal, au revoir) | 4-8 |
| EN-D02 | L'heure du goûter (faim, choisir, boire, merci) | 5-10 |
| EN-D03 | Mon week-end (activités à embranchements, école) | 9-15 |
| EN-D04 | Au café à Londres (commander, taille, sur place, payer) | 11+ |

## Ajouter / modifier un scénario
1. Éditer `data/dialogues/en.json` (format : `nodes` → `say`, `fr`, `choices`, `intents[{keys, reply, next|end}]`, `any`, `open`, `help`).
2. Pousser sur GitHub : l'Action **« Dialogues Sensei — vérification + MP3 »** vérifie le scénario (nœuds manquants, aide absente…), génère la voix de Sensei pour les nouvelles phrases uniquement (ElevenLabs, voix anglaise native) et met à jour `data/dialogues/en.audio.json`.
3. Autres langues : créer `data/dialogues/es.json` / `de.json` (mots-clés à écrire dans la langue, pas de traduction automatique).
