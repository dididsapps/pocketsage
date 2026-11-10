# PocketSage — ElevenLabs TTS : état complet & guide de mise à jour

> Ce dossier centralise tout ce qui concerne la génération et la gestion des MP3 ElevenLabs pour PocketSage.
> **Lis ce fichier en premier** avant d'ajouter du contenu, une langue ou un niveau.

---

## 🔑 Credentials & endpoints

| Clé | Valeur |
|-----|--------|
| ElevenLabs API Key | `(dans .env : ELEVENLABS_API_KEY)` |
| Voix FR | `GFj5Qf6cNQ3Lgp8VKBwc` (Olivier) |
| Voix EN | `9mF01VTvwaxuBPjm0hMu` (Charlie Horse) |
| R2 Bucket | `pocketsage-audio` |
| R2 Endpoint | `https://8ea67fd06083effd6f76efdefb92092f.r2.cloudflarestorage.com` |
| R2 Access Key | `6af471e11db12cb768c57df351e9a6fd` |
| R2 Secret Key | `4e7b9ad69ef6072024954beb7891fe710f1008719bfbf923341bdb35e1ed4f94` |
| CDN public | `https://pub-8cdc5500f1ab4785ba254b7335f7a68a.r2.dev` |

---

## 🗂️ Structure R2 (bucket `pocketsage-audio`)

```
audio/
  fr/          ← Questions FR GS/CP/CE1 (ElevenLabs, voix Olivier)
  en/          ← Questions EN GS/CP/CE1 (ElevenLabs, voix Charlie Horse)
  nuit/        ← Histoires du soir + méditations (ElevenLabs, voix Olivier)
avatars/       ← Avatars SVG
```

---

## 📊 Ce qui est couvert (état au 02/11/2026)

### Questions éducatives FR — `audio/fr/`

| Niveau | Voix | Modules couverts | Fichiers R2 |
|--------|------|-----------------|-------------|
| **GS** | ElevenLabs Olivier | LG, SC, MA, GE, ES, FR, HI-GS, CG (tous sous-modules), AN-GS | ✅ ~1 100 fichiers |
| **CP** | ElevenLabs Olivier | LG, SC, MA, GE, ES, FR, AN-CP | ✅ ~788 fichiers |
| **CE1** | ElevenLabs Olivier | LG, SC, MA, GE, ES, FR, AN-CE1 | ✅ ~759 fichiers |
| CE2 | Google TTS | tous modules | ✅ ~1 119 fichiers (manifest_google.json) |
| CM1 | Google TTS | tous modules | ✅ ~1 107 fichiers |
| CM2 | Google TTS | tous modules | ✅ ~245 fichiers |
| 6ème→Lycée | Google TTS | tous modules | ✅ ~734 fichiers |

**Format fichiers FR :** `audio/fr/{ID}_enonce.mp3`
**Cas spécial LG- :** le préfixe `LG-` est remplacé par `FR-` sur R2 (ex. `LG-GS-001` → `FR-GS-001_enonce.mp3`)

### Questions éducatives EN (Anglais) — `audio/en/`

| Niveau | Voix | Fichiers R2 |
|--------|------|-------------|
| **AN-GS** | ElevenLabs Charlie Horse | ✅ ~140 fichiers |
| **AN-CP** | ElevenLabs Charlie Horse | ✅ ~120 fichiers |
| **AN-CE1** | ElevenLabs Charlie Horse | ✅ ~120 fichiers |
| AN-CE2 | Google TTS | ✅ ~460 fichiers (manifest_google.json) |
| AN-CM1 | Google TTS | ✅ ~455 fichiers |
| AN-CM2 | Google TTS | ✅ ~99 fichiers |
| AN-6E→LY | Google TTS | ✅ ~208 fichiers |

⚠️ **AN-CE2 à AN-LY** : Google TTS uniquement — ElevenLabs non encore généré pour ces niveaux.

**Format fichiers EN :** `audio/en/{ID}.mp3` (pas de suffixe `_enonce`)

### Onglet Nuit — `audio/nuit/`

| Contenu | Voix | Fichiers R2 |
|---------|------|-------------|
| Méditations MED-001 à MED-005 | ElevenLabs Olivier | ✅ 5 fichiers |
| Histoires longues HS-001 à HS-008 | ElevenLabs Olivier | ✅ 8 fichiers |
| Mini-histoires HC-001/002/003/005 | ElevenLabs Olivier | ✅ 4 fichiers |

**Format fichiers Nuit :** `audio/nuit/{ID}.mp3`
Les histoires Nuit ne sont **pas** dans manifest.json — elles sont servies depuis R2 via `elPlayNuit()` dans index.html, avec fallback ElevenLabs API si le fichier n'existe pas encore.

---

## ⚙️ Comment `_playMp3()` décide quelle voix utiliser (index.html)

```
Question reçue (ex: LG-GS-042)
  │
  ├─ isEN ? (lang='en' ou ID commence par AN-)
  │     └─ → audio/en/{ID}.mp3  (ElevenLabs Charlie Horse)
  │
  └─ isFR ? (GS, CP ou CE1, tous modules FR)
        ├─ OUI → audio/fr/{ID.replace('LG-','FR-')}_enonce.mp3  (ElevenLabs Olivier)
        └─ NON → Web Speech API (Google TTS via navigateur)
```

**Préfixes FR qui déclenchent ElevenLabs :**
- GS : `LG-GS-`, `SC-GS-`, `HI-GS-`, `MA-GS-`, `GE-GS-`, `ES-GS-`, `CG-`, `FR-GS-`
- CP : `LG-CP-`, `SC-CP-`, `MA-CP-`, `GE-CP-`, `ES-CP-`, `FR-CP-`
- CE1 : `LG-CE1-`, `SC-CE1-`, `MA-CE1-`, `GE-CE1-`, `ES-CE1-`, `FR-CE1-`

---

## 📜 Manifests

| Fichier | Contenu | Usage |
|---------|---------|-------|
| `audio/manifest.json` | 3 223 entrées ElevenLabs FR+EN GS/CP/CE1 | Référence pour savoir si un fichier existe |
| `audio/manifest_google.json` | 4 918 entrées Google TTS CE2+ | Référence niveaux supérieurs |

Les manifests **ne contiennent pas** les fichiers Nuit (HS/HC/MED) — ces MP3 existent directement sur R2 sans entrée manifest.

---

## 🚀 Ajouter du nouveau contenu

### Cas 1 : Nouvelles questions FR GS/CP/CE1

1. Ajouter les questions dans `index.html` avec le bon préfixe
2. Lancer `python3 generate_tts.py` (génère + ajoute au manifest)
3. Lancer `python3 upload_r2.py` (uploade les nouveaux fichiers)
4. `git add audio/ && git push`

### Cas 2 : Nouvelles questions EN GS/CP/CE1

1. Ajouter les questions dans `index.html` avec préfixe `AN-GS-`, `AN-CP-`, `AN-CE1-`
2. Lancer `python3 generate_en_tts.py`
3. Lancer `python3 upload_r2.py`

### Cas 3 : Étendre ElevenLabs à AN-CE2, AN-CM1, etc.

Actuellement ces niveaux utilisent Google TTS (manifest_google.json).
Pour les passer à ElevenLabs Charlie Horse :
1. Modifier `generate_en_tts.py` pour inclure CE2/CM1/CM2/6E etc.
2. Modifier `_playMp3()` dans index.html : ajouter `id.startsWith('AN-CE2-')||...` dans le bloc `isEN`
   (actuellement `isEN` se déclenche déjà pour tout `AN-` — vérifier que les fichiers existent bien sur R2 avant)
3. Générer + uploader

### Cas 4 : Nouvelles histoires/méditations dans l'onglet Nuit

1. Ajouter dans `DATA.histoires` ou `DATA.meditation` dans index.html
2. Lancer `python3 generate_nuit.py` (génère + uploade sur R2)
3. Commit + push → Cloudflare Pages redéploie automatiquement

### Cas 5 : Ajouter une nouvelle langue (ex: Espagnol, Allemand)

Structure suggérée :
- R2 : `audio/es/`, `audio/de/` etc.
- Voix à choisir sur elevenlabs.io → ajouter dans ce README
- Créer `generate_es_tts.py` sur le modèle de `generate_tts.py`
- Dans `_playMp3()` : ajouter la détection du préfixe de langue (`ES-` déjà utilisé pour Enseignement Scientifique → choisir un autre préfixe ex: `ESP-`)

---

## 🛠️ Scripts disponibles

| Script | Rôle |
|--------|------|
| `generate_tts.py` | Génère MP3 ElevenLabs FR (questions GS/CP/CE1) |
| `generate_en_tts.py` | Génère MP3 ElevenLabs EN (questions AN-GS/CP/CE1) |
| `generate_tts_google.py` | Génère MP3 Google TTS FR (CE2 et plus) |
| `generate_nuit.py` | Génère MP3 ElevenLabs pour onglet Nuit (HS/HC/MED) |
| `upload_r2.py` | Upload tous les MP3 locaux vers R2 (audio/fr + audio/en) |

---

## 📱 Architecture TTS dans l'app

```
Bouton audio pressé
  │
  ├─ Questions éducatives → _playMp3(id, fallback, lang)
  │     ├─ Cherche MP3 sur R2 (fetch + AudioContext)
  │     └─ Fallback : ttsSpeak() → Web Speech API
  │
  ├─ Onglet Nuit (histoires/méditations) → elPlayNuit(id, texte)
  │     ├─ 1. Cherche MP3 sur R2 (audio/nuit/{id}.mp3) — GRATUIT si pré-généré
  │     ├─ 2. Fallback : elSpeak() → ElevenLabs API temps réel (texte chunké)
  │     └─ 3. Fallback : Web Speech API si API indisponible
  │
  └─ Autres (CE2+, conseils, etc.) → ttsSpeak() → Web Speech API
```

✅ **Implémenté (02/11/2026) :** `elPlayNuit(id, txt)` vérifie d'abord `audio/nuit/{id}.mp3` sur R2 avant d'appeler l'API. Les 17 MP3 pré-générés sont servis gratuitement depuis R2 — zéro crédit pour les écoutes répétées.

---

## 💰 Crédits ElevenLabs utilisés (au 02/11/2026)

- **Généré** : ~34 452 / 131 000 crédits mensuel
- **Restant** : ~96 548 crédits
- Histoires nuit : ~9 000 chars (17 fichiers) — négligeable

---

*Dossier créé le 02/11/2026 — mettre à jour à chaque ajout de contenu*
