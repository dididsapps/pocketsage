# Flash Savant — état des lieux

Module « anti-scroll » de PocketSage : des cartes courtes (titre + idée) qu'on fait défiler à la place des réseaux sociaux.

## 1. Ce qui existe dans l'app (à jour du 10/11/2026)

- Contenu : **`data/flash/fr.json`** (source unique, 201 cartes) + traductions automatiques `data/flash/{lang}.json`. Format et procédure : `03_procedures_mp3_traductions.md`.
- Code : `index.html`, bloc « FLASH SAVANT » : `loadFlash()`, `_FLASH_TABS`, `renderFlashCard()`, `renderFlashReview()`, `flashListen()`.
- Module **Flash** en tête de l'accueil (`HOME_MODS`, description courte en 8 langues : clés `m_flash` / `m_flash_d`) + bouton ⚡ dans la barre du bas.
- Chaque carte : titre, idée, **« Essaie aujourd'hui »**, **question de rappel**, **source**, âge minimum.
- **Révision espacée** (Leitner) par profil : J+2 → J+7 → J+21 → ancrée ; bouton orange « 🧠 N à réviser » ; compteur 🌱 ancrées ; +1 étoile par bonne réponse.
- **Audio** : MP3 R2 dans la langue du profil (`?v=<empreinte>`), voix du téléphone en secours tant que le MP3 n'existe pas.
- **Traduction** : texte affiché dans la langue maternelle du profil (FR, EN, DE, ES, IT, PT, AR, ZH, RU, UK), repli FR.
- Hors-ligne : le service worker garde `data/flash/*.json` en cache après la première ouverture.

| Clé `cat` | Préfixe | Cartes | Âges | Onglet |
|---|---|---|---|---|
| petits | PT | 18 | 4-6 | Curiosités |
| enfants | EN | 15 | 8-9 | Curiosités |
| curiosites | CU | 21 | 6-10 | Curiosités |
| ados | AD | 15 | 13-14 | Curiosités |
| psycho | PS | 14 | 8-13 | Psycho |
| motivationJeune | MJ | 17 | 5-7 | Motivation |
| motivation | MO | 24 | 10-13 | Motivation |
| confiance | CF | 13 | 10-13 | Confiance |
| emotionsJeune | EJ | 17 | 4-6 | Émotions |
| emotions | EM | 21 | 9-13 | Émotions |
| sagesse | SA | 26 | 6-13 | Sagesse |

## 2. Limites restantes

1. **Traductions et MP3 pas encore générés** : il faut d'abord ajouter les 3 secrets GitHub (voir `03` §4), puis lancer l'Action une fois. D'ici là : texte en français, voix du téléphone.
2. **Volume** : 201 cartes, objectif 1000+ (`02_sources_contenu.md`, `04_plan_action.md`).
3. Pas encore de favoris/collections, de série quotidienne ni de bilan parent (voir `04`).
4. La révision est stockée sur l'appareil (pas de synchronisation entre téléphones).

## 2bis. Journal du 10/11/2026

- Recherche concurrents (`01`) et sources libres (`02`), plan d'action (`04`).
- Cartes sorties de `index.html` vers `data/flash/fr.json` ; 50 nouvelles cartes sourcées ; question de rappel + action + source ajoutées aux 151 existantes ; 120 cartes corrigées (faits faux ou non sourcés : CF-001 power pose, EN-004 bactéries, CU-013 renouvellement des cellules, CU-014 éclairs, citations mal attribuées SA/MO…).
- Révision espacée, audio/traductions par langue, module Flash sur l'accueil.
- `generate_flash_tts.py` réécrit (empreintes, clés via environnement) + GitHub Action `flash-tts.yml`.
- Guide parents : nouvelle page « 5. Flash Savant », émojis retirés (carrés noirs), sommaire et mise en page corrigés, adresse pocketsage.org.

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

## 4. Restes à faire

- [ ] **Secrets GitHub** + premier lancement de l'Action (traductions + ~2 000 MP3).
- [ ] Régénérer les 35 fiches FR, les relire, les envoyer sur R2 dans `fiches/FR/`, puis ajouter FI-031 à FI-035 dans la liste des fiches de `index.html`.
- [ ] Le générateur de fiches écrit dans `~/mnt/pocketsage/fiches/{LANG}/` (dossier de ton ordinateur). Le dossier `fiches/` du repo contient d'anciennes versions à plat (FI-001 à FI-030).
- [x] Clés retirées du code (10/11).
- [ ] **Révoquer les anciennes clés et en créer de nouvelles** (Google, ElevenLabs, R2), puis secrets GitHub + `.env`.
