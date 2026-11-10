# Flash Savant — état des lieux (10/11/2026)

Module « anti-scroll » de PocketSage : des cartes courtes (titre + idée) qu'on fait défiler à la place des réseaux sociaux.

## 1. Ce qui existe dans l'app

- Code : `index.html`, objet `FLASH_DATA` (~ligne 12558), onglets `_FLASH_TABS` (~ligne 12736), rendu `renderFlashCard()` (~ligne 12769).
- Format d'une carte :
  ```js
  {id:'CU-001', emoji:'🧠', titre:'…', texte:'…', tag:'Neurosciences', age:'8+', couleur:'#…'}
  ```
- **151 cartes**, en français uniquement dans l'app :

| Clé `FLASH_DATA` | Préfixe | Cartes | Âges | Onglet |
|---|---|---|---|---|
| petits | PT | 12 | 4-6 | Curiosités |
| enfants | EN | 10 | 8-9 | Curiosités |
| curiosites | CU | 15 | 6-10 | Curiosités |
| ados | AD | 10 | 13-14 | Curiosités |
| psycho | PS | 10 | 8-13 | Psycho |
| motivationJeune | MJ | 12 | 5-7 | Motivation |
| motivation | MO | 20 | 10-13 | Motivation |
| confiance | CF | 10 | 10-13 | Confiance |
| emotionsJeune | EJ | 12 | 4-6 | Émotions |
| emotions | EM | 18 | 9-13 | Émotions |
| sagesse | SA | 22 | 6-13 | Sagesse |

Onglet « Mix » : toutes les cartes mélangées.

## 2. Limites actuelles (à traiter)

1. **Le bouton « Écouter » utilise la voix du téléphone** (`ttsSpeak`, Web Speech API), pas les MP3. Les MP3 générés par `generate_flash_tts.py` ne seront entendus qu'une fois `renderFlashCard()` branché sur `_playMp3()` avec l'URL `audio/flash/{lang}/{ID}_{LANG}.mp3` et la voix du téléphone en secours.
2. **Pas de traduction affichée** : les traductions de `generate_flash_tts.py` vont dans `data/flash_translations/{LANG}.json` mais l'app ne les lit pas encore.
3. **Peu de contenu** : 151 cartes, tout lu en 1 à 2 semaines. Il en faut 1000+ (voir `02_sources_contenu.md`).
4. **Pas de sauvegarde ni de rappel** : pas de favoris, de collections ou de question de rappel quelques jours plus tard. C'est là que PocketSage peut faire mieux que les concurrents (voir `01_concurrents_antiscroll.md`).
5. **Âge** : la carte a un champ `age` mais les onglets ne filtrent pas encore selon le profil.

## 3. Journal du 09/11/2026 (hier)

Flash Savant :
- `60f91c29` : création du module Flash Savant (7 onglets, 60+ cartes).
- `01731f12`, `d9623446` : extension à 151 cartes (4-7, 8-10, 13-18 ; motivation et émotions jeunes).
- `f47cc68e`, `b4c4b59d` : script `generate_flash_tts.py` (traduction + MP3 Google TTS + envoi R2, 8 langues).
- `91e11dc9` : test de connexion R2 corrigé (`list_objects_v2`).

Fiches imprimables (ateliers sans écran) :
- `553f2a93`, `24bed5c6` : téléchargement PDF qui reste dans l'app (fetch + Blob, URL r2.dev).
- `1cd8edcc` → `8a1e767a` : passage noir et blanc (économie d'encre), en-tête réduit, émojis retirés (Helvetica ne les affiche pas), zones de dessin pleine page, sous-titres à 90 caractères.
- `589771f6` : FI-006 Stroop avec mots en couleurs discordantes, FI-007 labyrinthes générés par algorithme (Recursive Backtracker, toujours solubles), **5 nouvelles fiches FI-031 à FI-035** (Intrus, Rotation mentale, Touche la bonne couleur, Détective de patterns, Mémoire photographique). Option `--lang` / `--ids` ajoutée au générateur.

## 4. Restes à faire (repris d'hier)

- [ ] Lancer `generate_flash_tts.py` pour les 8 langues : aucun `audio/flash/` ni `audio/manifest_flash.json` dans ce repo, donc pas encore fait **ici** (à vérifier sur ton ordinateur).
- [ ] Brancher les MP3 Flash et les traductions dans l'app (point 2.1 et 2.2).
- [ ] Régénérer les 35 fiches FR, les relire, puis les envoyer sur R2 dans `fiches/FR/`.
- [ ] Ajouter FI-031 à FI-035 dans la liste des fiches de `index.html` (~ligne 9883) : elles n'y sont pas encore.
- [ ] Le générateur de fiches écrit dans `~/mnt/pocketsage/fiches/{LANG}/` (dossier de ton ordinateur). Le dossier `fiches/` du repo contient d'anciennes versions à plat (FI-001 à FI-030).
- [ ] **Sécurité, urgent** : voir `03_procedures_mp3_traductions.md` §6.
