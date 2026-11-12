# PROCESS — TTS, Traductions & UI i18n pour PocketSage

Référence complète pour ajouter du nouveau contenu audio et des traductions d'interface.

---

## 1. Architecture des fichiers audio

```
audio/
├── fr/          ← TTS français (ElevenLabs ou Google Neural2)
├── en/          ← TTS anglais
├── de/          ← TTS allemand
├── it/          ← TTS italien
├── pt/          ← TTS portugais
├── ru/          ← TTS russe
├── uk/          ← TTS ukrainien
├── ar/          ← TTS arabe
├── zh/          ← TTS chinois
└── maternelle/  ← TTS langues maternelles (questions GS→CE2)
    ├── DE/      ← {ID}_enonce.mp3, {ID}_rep.mp3, {ID}_choix_N.mp3
    ├── RU/
    ├── UK/
    ├── AR/
    ├── ZH/
    ├── IT/
    └── PT/

CDN : https://audio.pocketsage.org  (Cloudflare R2, bucket: pocketsage-audio)
Sync : rclone sync audio/ r2:pocketsage-audio/audio/ --progress
```

---

## 2. Voix utilisées

### Google TTS (Neural2 / Wavenet)
API : `https://texttospeech.googleapis.com/v1/text:synthesize?key=KEY`

| Langue | Code   | Voix                  | Type     |
|--------|--------|-----------------------|----------|
| FR     | fr-FR  | fr-FR-Neural2-B       | Neural2  |
| EN     | en-US  | en-US-Neural2-D       | Neural2  |
| DE     | de-DE  | de-DE-Neural2-B       | Neural2  |
| IT     | it-IT  | it-IT-Neural2-C       | Neural2  |
| PT     | pt-BR  | pt-BR-Neural2-B       | Neural2  |
| RU     | ru-RU  | ru-RU-Wavenet-B       | Wavenet* |
| UK     | uk-UA  | uk-UA-Wavenet-A       | Wavenet* |
| AR     | ar-XA  | ar-XA-Wavenet-B       | Wavenet* |
| ZH     | zh-CN  | cmn-CN-Wavenet-B      | Wavenet* |

*Neural2 non disponible pour ces langues → Wavenet obligatoire

Paramètres audio : `speakingRate: 0.85`, `pitch: -2.0`, `audioEncoding: MP3`

### ElevenLabs (voix premium, si utilisé)
- API : `https://api.elevenlabs.io/v1/text-to-speech/{voice_id}`
- Utiliser pour voix FR/EN de haute qualité si budget disponible
- Format de sortie : MP3, 44100Hz

---

## 3. Scripts de génération TTS

### `generate_tts_langues.py`
**But** : Génère les MP3 pour les 7 langues vivantes (DE/IT/PT/RU/UK/AR/ZH)
**Source** : `data/{lang}.json` (ex: `data/de.json`)
**Sortie** : `audio/{lang}/{ID}_enonce.mp3`, `_rep.mp3`, `_choix_N.mp3`
**Manifest** : `audio/manifest_langues.json` (reprise automatique si crash)

```bash
python3 generate_tts_langues.py
# Reprend là où il s'est arrêté grâce au manifest
```

### `generate_tts_maternelle.py`
**But** : Traduit les questions GS→CE2 non-langues dans les 7 langues maternelles + génère MP3
**Source** : `data/maternelle_source_fr.json` (2710 questions extraites de index.html)
**Cache traductions** : `data/maternelle_translated/{lang}.json`
**Sortie** : `audio/maternelle/{LANG}/{ID}_enonce.mp3`, `_rep.mp3`, `_choix_N.mp3`
**Manifest** : `audio/manifest_maternelle.json`

```bash
python3 generate_tts_maternelle.py
```

### Upload R2 après génération
```bash
# Upload langues vivantes
rclone sync audio/de/ r2:pocketsage-audio/audio/de/ --progress
rclone sync audio/it/ r2:pocketsage-audio/audio/it/ --progress
# ... etc pour chaque langue

# Upload maternelle (tout d'un coup)
rclone sync audio/maternelle/ r2:pocketsage-audio/audio/maternelle/ --progress
```

---

## 4. Ajouter un nouveau module de contenu (questions)

### Étape 1 — Ajouter les questions dans `index.html`
Format dans le tableau `DATA` :
```js
{id:'MA-CE1-150', classe:'CE1', enonce:'...', rep:'...', choix:['...','...','...'], diff:1, lang:'fr', hint:'...'}
```

### Étape 2 — Générer les MP3 français
```bash
python3 generate_tts_langues.py  # relancer, le manifest skip ce qui existe déjà
```

### Étape 3 — Générer les MP3 langues maternelles (si classe ≤ CE2 et module non-langue)
1. Mettre à jour `data/maternelle_source_fr.json` avec les nouvelles questions
2. Relancer `generate_tts_maternelle.py` (le manifest skip ce qui existe)

### Étape 4 — Upload R2
```bash
rclone sync audio/ r2:pocketsage-audio/audio/ --progress
```

---

## 5. Traductions Google API

API : `https://translation.googleapis.com/language/translate/v2?key=KEY`

**Clé** : "Clé API 1 text to speech" (dans Google Cloud Console)
→ Doit avoir les 2 APIs autorisées : Cloud Text-to-Speech + Cloud Translation API

```python
# Exemple d'appel batch (100 textes max par requête)
import requests
texts = ["Bonjour", "Au revoir"]
r = requests.post(
    f"https://translation.googleapis.com/language/translate/v2?key={KEY}",
    json={"q": texts, "source": "fr", "target": "de", "format": "text"}
)
translated = [t["translatedText"] for t in r.json()["data"]["translations"]]
```

**Codes de langue** : `de`, `it`, `pt`, `ru`, `uk`, `ar`, `zh`, `pl`, `ro`, `hu`, `tr`, `bg`, `cs`, `sk`, `hr`, `sr`, `fa`

---

## 6. Système UI i18n — `TRANSLATIONS` + `applyLang()`

Inséré dans `index.html` juste avant `function loadApp()`.

### Ajouter une nouvelle clé de traduction

1. Ajouter la clé dans `TRANSLATIONS.FR` (référence)
2. Ajouter la même clé dans toutes les autres langues (FR/EN/DE/ES/IT/PT/RU/UK/AR/ZH/PL/RO/HU/TR)
3. Utiliser dans le HTML ou JS :

```html
<!-- HTML statique -->
<button data-t="ma_cle">Texte FR par défaut</button>

<!-- Template JS (template literal) -->
`<button>${T('ma_cle')}</button>`

<!-- Dans du JS classique -->
el.textContent = T('ma_cle');
```

### Langues couvertes
FR · EN · DE · ES · IT · PT · RU · UK · AR · ZH · PL · RO · HU · TR
+ Fallback FR pour : BG · CS · SK · HR · SR · FA

### Déclenchement
`applyLang()` est appelé automatiquement dans `buildHome()` à chaque changement de profil.
Pour un rechargement manuel : `applyLang()` dans la console.

---

## 7. Structure du profil utilisateur

```js
{
  name: "Emma",
  age: 7,              // 4–18
  native: "FR",        // langue maternelle → code IETF (FR/EN/DE/RU/UK/AR/ZH/IT/PT/...)
  langs: ["EN","DE"],  // langues vivantes à apprendre
  score: 0,
  done: {},
  avatarId: 3
}
```

- `P()` → profil courant
- `P().native` → langue maternelle (clé dans TRANSLATIONS)
- `APP.cur` → index du profil courant

---

## 8. TTS dans l'app — Règles de boutons

| Classe     | Boutons TTS matières | Boutons TTS langues vivantes |
|------------|---------------------|------------------------------|
| GS → CE2   | ✅ Oui (maternelle) | ✅ Oui (toujours)             |
| CM1 → 3e   | ❌ Non (savent lire) | ✅ Oui (toujours)             |

Les boutons TTS des matières (Maths/Sciences/etc.) sont générés en langue maternelle du profil (`P().native`).
Les boutons TTS des langues vivantes sont toujours présents, dans la langue cible apprise.

---

## 9. Checklist pour un nouveau déploiement contenu

- [ ] Questions ajoutées dans `index.html` (DATA array)
- [ ] `data/maternelle_source_fr.json` mis à jour si nouvelles questions GS→CE2 non-langue
- [ ] `generate_tts_langues.py` relancé → nouveau contenu généré
- [ ] `generate_tts_maternelle.py` relancé si nécessaire
- [ ] `rclone sync audio/ r2:pocketsage-audio/audio/ --progress`
- [ ] Nouvelles clés UI ajoutées dans `TRANSLATIONS` si nouveaux textes d'interface
- [ ] `git add -p && git commit && git push`

---

## 10. Résumé des volumes générés (nov. 2026)

| Contenu              | Fichiers  | Taille approx. |
|----------------------|-----------|----------------|
| TTS FR (toutes classes) | ~2200   | ~180 MB        |
| TTS EN               | ~471      | ~25 MB         |
| TTS DE/IT/PT/UK      | ~4×1600   | ~400 MB        |
| TTS RU/AR/ZH         | ~3×1600   | ~300 MB        |
| Maternelle (7 langues) | 99 268  | ~4 GB          |
| **Total R2**         | **~110 000** | **~5 GB**   |

---

## 11. Qualité des voix et des traductions par langue (noté le 12/11/2026)

À ressortir si un parent, un testeur ou un store pose la question.

### État des MP3 sur R2 (vérifié le 12/11/2026 avec `rclone check`)
- IT, PT, UK : complets (3 995 fichiers chacun) — maternelle : complète (100 275 fichiers).
- **AR et ZH : absents de R2 jusqu'au 12/11/2026** (générés sur le Mac mais jamais envoyés) → envoyés ce jour (3 995 + 3 996). Avant cette date, l'arabe et le chinois n'avaient aucune voix enregistrée.
- **RU : 1 354 fichiers manquaient** (envoi interrompu) → complétés ce jour.
- Attention : `upload_r2.py` n'envoie que fr/en/de/es/nuit/flash. Les autres langues se sont envoyées à la main avec rclone → toujours vérifier avec :
  `rclone check audio/XX r2:pocketsage-audio/audio/XX --one-way --size-only`
  et compléter avec `rclone copy … --ignore-existing` (n'écrase rien).
- **Ne jamais renvoyer `audio/prono` depuis le Mac** : les voix de prononciation sont regénérées par GitHub (`gen_prono_mp3.py`) ; les copies du Mac sont d'anciennes versions (113 différences = corrections ID en double + espagnol lu par la voix FR).

### Voix utilisées (Google TTS, voix natives — pas une voix française qui imite)
| Langue | Voix | Remarque |
|---|---|---|
| IT | it-IT-Neural2-C | très bonne |
| PT | pt-BR-Neural2-B | accent **brésilien** — option à décider : pt-PT (Portugal) pour le public européen |
| RU | ru-RU-Wavenet-B | bonne |
| UK | uk-UA-Wavenet-A | bonne, peu de voix disponibles |
| AR | ar-XA (Neural2-B dans certains scripts, Wavenet-B dans generate_flash_tts.py) | arabe standard moderne ; **à vérifier quelle voix a réellement servi** |
| ZH | cmn-CN (Neural2-B / Wavenet-B selon le script) | mandarin ; même vérification |

### Limites connues (réponse honnête si on nous en parle)
- Personne n'a encore écouté les MP3 AR / ZH / RU / UK : faire écouter 2-3 fichiers par langue.
- Le risque principal est la **traduction automatique** (phrases maladroites), plus que la voix.
- Idée : demander à un parent bêta natif de chaque langue de relire/écouter 10 minutes, et corriger les textes sources (les MP3 se regénèrent automatiquement).
