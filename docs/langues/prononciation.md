# Atelier Prononciation (PR-EN / PR-ES / PR-DE)

## Contenu
- Items dans `index.html` : `{id:"PR-EN-001",classe:"GS",niveau:1,mot:"apple",…,lang:"EN"}`.
- **Chaque ID doit être unique** : sinon deux phrases jouent le même son (bug corrigé le 10/11/2026 : 37 doublons renumérotés). Le script refuse de tourner s'il trouve un doublon.

## Audio (automatique)
- Modifier/ajouter un item dans `index.html` puis pousser : l'Action **« Prononciation — MP3 automatiques »** (`.github/workflows/prono-tts.yml`) régénère uniquement les MP3 dont le texte ou la voix a changé (`gen_prono_mp3.py`), les envoie sur R2 (`audio/{en,es,de}/{ID}.mp3`) et met à jour `data/prono_audio_manifest.json`.
- L'app ajoute `?v=<empreinte>` à l'URL : jamais d'ancien son après une correction.
- Voix **natives uniquement** : EN/DE GS→CE2 ElevenLabs (Mr Claus, Nicholas Santa) ; ES tous niveaux et EN/DE CM1+ Google Neural2 (en-GB, es-ES, de-DE).

## Reconnaissance vocale (gratuite, téléphone)
- `sttListen()` : garde les résultats partiels (mots courts), réécoute une 2e fois si rien capté, micro ouvert après la fin du son modèle.
- `sttScore()` : meilleure des 5 propositions du moteur, homophones/nombres (EN/ES/DE), accents, Unicode.
- Limite : le téléphone devine le mot, il ne note pas l'accent. Version précise = option premium Azure (voir `docs/tarification/`).

## Micro et vie privée (RGPD mineurs)
- Réglage par enfant dans l'Espace Parents (`P().mic = {on, date}`), message clair sur la destination de la voix.
- `MIC_OPT_IN=false` pendant la bêta (micro autorisé par défaut). **Au lancement public : passer `MIC_OPT_IN` à `true`** → micro coupé tant qu'un parent n'a pas coché (case non pré-cochée).
- Reconnaissance **100 % sur l'appareil** (`processLocally`) quand le navigateur le permet : le parent clique « Vérifier » dans l'Espace Parents, peut télécharger la langue ; résultat mémorisé (`psa3_micLocal`). Vérification jamais automatique (elle fait planter le Chromium de test sans ce service).
- Micro coupé → `sttListen` renvoie `mic_off` : l'enfant répond avec les boutons.
