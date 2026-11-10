# Flash : mettre à jour cartes, traductions et MP3

Référence générale TTS/i18n de l'app : `PROCESS_TTS_TRADUCTIONS.md` (racine) et `elevenlabs/README.md`. Ce fichier ne couvre que le module Flash.

## 1. Ajouter ou modifier des cartes

1. Éditer `FLASH_DATA` dans `index.html` (format dans `00_etat_des_lieux.md`).
2. ID unique, préfixe de la catégorie, numéro suivant (ex. `CU-016`). Ne jamais réutiliser un ID supprimé.
3. Pas d'apostrophe droite `'` dans `titre`/`texte` : utiliser `’` (sinon la chaîne JS casse et l'extraction échoue).
4. Garder l'ordre des champs `id, emoji, titre, texte, tag` : `extract_flash()` dans `generate_flash_tts.py` les lit avec une regex dans cet ordre.

## 2. Générer traductions + MP3 (commande unique)

```bash
cd ~/pocketsage
export GOOGLE_TTS_API_KEY=…   # voir §6
export R2_ACCESS_KEY=… R2_SECRET_KEY=…
python3 generate_flash_tts.py                    # 8 langues : FR EN DE ES IT PT AR ZH
python3 generate_flash_tts.py --langs FR,EN      # sous-ensemble
python3 generate_flash_tts.py --no-upload        # générer sans envoyer sur R2
python3 generate_flash_tts.py --dry-run          # vérifier l'extraction seulement
```

Ce que fait le script :
- extrait les cartes de `index.html` ;
- traduit `titre. texte` depuis le FR (Google Translate) → cache `data/flash_translations/{LANG}.json` ;
- génère les MP3 (Google TTS, `speakingRate 0.85`, `pitch -2.0`) → `audio/flash/{lang}/{ID}_{LANG}.mp3` ;
- envoie sur R2 (`pocketsage-audio`, clé `audio/flash/{lang}/{ID}_{LANG}.mp3`) ;
- note ce qui est fait dans `audio/manifest_flash.json` : relancer ne régénère que les **nouvelles** cartes.

Voix : FR `fr-FR-Neural2-A`, EN `en-GB-Neural2-B`, DE `de-DE-Neural2-B`, ES `es-ES-Neural2-B`, IT `it-IT-Neural2-C`, PT `pt-BR-Neural2-B`, AR `ar-XA-Neural2-B`, ZH `cmn-CN-Neural2-B`.

Ordre de grandeur pour 151 cartes × 8 langues : ~1 200 MP3, quelques minutes, coût Google négligeable (~25 000 caractères par langue).

## 3. Piège : une carte MODIFIÉE n'est pas mise à jour

Le cache et le manifest sont indexés par **ID**, pas par contenu. Si tu corriges le texte de `CU-003`, le script garde l'ancienne traduction et l'ancien MP3.

Pour forcer la mise à jour d'une carte aujourd'hui :
1. retirer `CU-003` de chaque `data/flash_translations/{LANG}.json` ;
2. retirer les entrées `CU-003_{LANG}` de `audio/manifest_flash.json` ;
3. supprimer `audio/flash/*/CU-003_*.mp3` ;
4. relancer le script.

Correctif prévu (pas encore fait) : stocker une empreinte du texte FR (`sha1(titre+texte)[:8]`) dans le cache et le manifest. Si l'empreinte change, retraduire et régénérer automatiquement.

## 4. Automatisation complète (proposée, pas encore en place)

But : tu modifies `FLASH_DATA`, tu pousses sur GitHub, et tout se met à jour sans rien lancer.

- GitHub Action `.github/workflows/flash-tts.yml`, déclenchée sur `push` quand `index.html` change ;
- elle lance `python3 generate_flash_tts.py` avec les clés lues dans **GitHub Secrets** (jamais dans le code) ;
- le manifest et le cache des traductions sont recommités par l'action, les MP3 vont seulement sur R2 ;
- avec l'empreinte du §3, seules les cartes nouvelles ou modifiées coûtent quelque chose.

Prérequis de ton côté : ajouter `GOOGLE_TTS_API_KEY`, `R2_ACCESS_KEY` et `R2_SECRET_KEY` dans GitHub → repo → Settings → Secrets and variables → Actions.

## 5. Brancher dans l'app (pas encore fait)

Dans `renderFlashCard()` :
- bouton « Écouter » : essayer `https://pub-8cdc5500f1ab4785ba254b7335f7a68a.r2.dev/audio/flash/{lang}/{ID}_{LANG}.mp3` via `_playMp3()`, sinon `ttsSpeak()` ;
- texte : si la langue du profil n'est pas FR, charger `data/flash_translations/{LANG}.json` (lazy-load, comme les langues vivantes) et afficher la traduction. Le cache contient `"titre. texte"` en une chaîne : prévoir de stocker titre et texte séparément lors du correctif §3.

## 6. Sécurité : à faire en premier

Le repo `dididsapps/pocketsage` est **public** et contient des clés en clair (constaté le 10/11/2026) :
- **clé Google API** (TTS + Translate) : `generate_flash_tts.py`, `gen_fiches_multilingue.py`, `generate_voices.py`, `PLAN_TTS_LANGUES_MATERNELLES.md` ;
- **clés R2** (écriture sur le bucket) : `generate_flash_tts.py`, `gen_prono_mp3.py`, `elevenlabs/generate_prono_mp3.py`, `elevenlabs/r2_credentials.txt` ;
- **clé ElevenLabs** : `index.html` (donc visible par tout visiteur de pocketsage.org, l'app l'utilise pour `elSpeak()` en direct), plus `generate_tts.py`, `generate_en_tts.py`, `generate_nuit.py`, `generate_voices.py`, `gen_prono_mp3.py`, `generate_new_cp_mp3.py`, `elevenlabs/README.md`, `index.html.bak2`.

N'importe qui peut consommer tes crédits Google/ElevenLabs ou modifier/supprimer les fichiers du bucket R2. Actions :
1. **Toi** : régénérer la clé Google (Google Cloud Console → Identifiants), la clé ElevenLabs (profil → API Keys) et créer un nouveau jeton R2 (Cloudflare → R2 → Manage API Tokens), puis révoquer les anciennes. Les supprimer du code ne suffit pas : elles restent dans l'historique git public.
2. Restreindre la nouvelle clé Google aux API Text-to-Speech et Translation, et fixer un plafond de budget.
3. Scripts : lire les clés uniquement depuis l'environnement ou un `.env` listé dans `.gitignore`, sans valeur par défaut.
4. App : ne plus appeler ElevenLabs depuis le navigateur. Tout pré-générer sur R2 (déjà prévu dans la todo `elSpeak()`), ou passer par un petit Worker Cloudflare qui garde la clé côté serveur.
