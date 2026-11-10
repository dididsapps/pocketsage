# Flash : ajouter/modifier des cartes, traductions et MP3 automatiques

Depuis le 10/11/2026, **tout est automatique** : on modifie un seul fichier, on pousse sur GitHub, et les traductions + MP3 se font seuls.

Référence générale TTS/i18n du reste de l'app : `PROCESS_TTS_TRADUCTIONS.md` (racine) et `elevenlabs/README.md`.

## 1. Où est le contenu

| Fichier | Rôle | Qui l'écrit |
|---|---|---|
| `data/flash/fr.json` | **Source unique** des cartes (français) | Toi / Claude |
| `data/flash/{en,de,es,it,pt,ar,zh,ru,uk}.json` | Cartes traduites | Automatique, ne pas éditer à la main |
| `data/flash/audio_manifest.json` | MP3 déjà publiés + empreinte | Automatique |
| R2 `audio/flash/{lang}/{ID}_{LANG}.mp3` | Audio des cartes | Automatique |

L'app charge `data/flash/fr.json` + le fichier de la langue maternelle du profil (repli FR si une carte n'est pas encore traduite).

## 2. Format d'une carte (`data/flash/fr.json` → `cards`)

```json
{"id":"CU-016","cat":"curiosites","emoji":"🐙","titre":"…","texte":"2-3 phrases","tag":"Biologie",
 "age":"8+","couleur":"#118AB2",
 "action":"Essaie aujourd’hui : …",
 "rappel":{"q":"Question courte ?","choix":["bonne réponse","faux 1","faux 2"],"ok":0},
 "source":{"nom":"NOAA Ocean Service","url":"https://…"},
 "h":"(calculé automatiquement)"}
```

- `cat` : `petits`, `enfants`, `curiosites`, `ados`, `psycho`, `motivationJeune`, `motivation`, `confiance`, `emotionsJeune`, `emotions`, `sagesse` (détermine l'onglet).
- `id` : préfixe de la catégorie + numéro suivant, jamais réutilisé (`PT`, `EN`, `CU`, `AD`, `PS`, `MJ`, `MO`, `CF`, `EJ`, `EM`, `SA`).
- `age` : âge minimum (`"8+"`), filtré par le curseur d'âge.
- `rappel` : obligatoire pour que la carte entre dans la révision espacée. `ok` = index de la bonne réponse (l'app mélange les choix).
- `h` : ne pas remplir, le script le calcule.

## 3. Ajouter ou modifier des cartes : la procédure

1. Éditer `data/flash/fr.json` (ajout, correction, suppression).
2. `git commit` + `git push` sur `main`.
3. La GitHub Action **« Flash — traductions + MP3 automatiques »** (`.github/workflows/flash-tts.yml`) se lance :
   - vérifie le fichier (id en double, champs manquants, rappel invalide → échec visible dans l'onglet Actions) ;
   - calcule l'empreinte `h` de chaque carte ;
   - **retraduit et revocalise uniquement les cartes nouvelles ou modifiées**, dans 9 langues + FR ;
   - envoie les MP3 sur R2 ;
   - recommite `data/flash/*.json` → Cloudflare Pages redéploie l'app.
4. Suivi : GitHub → repo → onglet **Actions**. Relancer à la main : bouton « Run workflow ».

Durée : quelques minutes pour quelques cartes. Coût Google négligeable (une carte ≈ 300 caractères × 10 langues).

L'app ajoute `?v=<h>` à l'URL des MP3 : une carte corrigée n'est jamais servie avec l'ancien audio en cache.

## 4. Mise en route (une seule fois)

Dans GitHub → repo `dididsapps/pocketsage` → Settings → Secrets and variables → Actions → **New repository secret** :

| Nom | Valeur |
|---|---|
| `GOOGLE_TTS_API_KEY` | clé Google Cloud (APIs Text-to-Speech + Translation activées) |
| `R2_ACCESS_KEY` | jeton R2 (Access Key ID) avec écriture sur `pocketsage-audio` |
| `R2_SECRET_KEY` | jeton R2 (Secret Access Key) |

Tant que ces secrets manquent, l'Action s'arrête proprement avec un avertissement (rien n'est cassé).

Puis lancer une première fois « Run workflow » : elle traduit et vocalise les cartes existantes (≈ 200 cartes × 10 langues ≈ 2 000 MP3, une quinzaine de minutes).

## 5. Lancer à la main (optionnel)

```bash
cd ~/pocketsage
# clés dans un fichier .env (ignoré par git) :
#   GOOGLE_TTS_API_KEY=…
#   R2_ACCESS_KEY=…
#   R2_SECRET_KEY=…
python3 generate_flash_tts.py --dry-run          # voir ce qui changerait, sans appel API
python3 generate_flash_tts.py                    # tout ce qui a changé, 10 langues
python3 generate_flash_tts.py --langs FR,EN      # sous-ensemble
python3 generate_flash_tts.py --no-audio         # traductions seulement
python3 generate_flash_tts.py --no-upload        # MP3 en local dans audio/flash/ (ignoré par git)
```

Voix : FR `fr-FR-Neural2-A`, EN `en-GB-Neural2-B`, DE `de-DE-Neural2-B`, ES `es-ES-Neural2-B`, IT `it-IT-Neural2-C`, PT `pt-BR-Neural2-B`, AR `ar-XA-Wavenet-B`, ZH `cmn-CN-Wavenet-B`, RU `ru-RU-Wavenet-B`, UK `uk-UA-Wavenet-A`. Paramètres : `speakingRate 0.85`, `pitch -2.0`. Texte lu : titre + texte + action.

## 6. Révision espacée (rappel de fonctionnement)

Stockée par profil dans `APP.profiles[i].flashL` (`{id: {b: boîte, d: jour du rappel}}`), sur l'appareil :
- carte vue (avec `rappel`) → boîte 1, question à J+2 ;
- bonne réponse → boîte 2 (J+7) → boîte 3 (J+21) → boîte 4 = **ancrée** (compteur 🌱) ; +1 étoile par bonne réponse ;
- mauvaise réponse → boîte 1, question le lendemain.
Bouton orange « 🧠 N à réviser » en tête des onglets Flash quand des rappels sont dus.

## 7. Sécurité des clés

**10/11/2026 : toutes les clés ont été retirées du code** (scripts, docs, `index.html`, `elevenlabs/r2_credentials.txt` supprimé). Les scripts lisent les clés dans les variables d'environnement ou dans un fichier `.env` à la racine (modèle : `.env.example`, `.env` ignoré par git). L'app n'appelle plus ElevenLabs depuis le navigateur : l'onglet Nuit lit les MP3 pré-générés sur R2, sinon la voix du téléphone.

Les anciennes clés restent visibles dans l'**historique git** public : elles doivent être **révoquées** et remplacées (Google Cloud, ElevenLabs, Cloudflare R2), puis les nouvelles mises **uniquement** dans les secrets GitHub (§4) et le `.env` local. Ne jamais recoller une clé dans un fichier du repo.
