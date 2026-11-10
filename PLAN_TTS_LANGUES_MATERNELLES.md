# Plan TTS — Langues Maternelles GS→CE2
_Créé le 2026-11-06 — À déclencher quand prêt_

## Objectif
Générer les MP3 TTS pour les matières non-langues (Maths, Logique, Sciences, Histoire, Géo...)
uniquement pour les classes GS → CE2, dans toutes les nouvelles langues maternelles.
Les enfants jusqu'au CE2 ne savent pas encore lire → nécessaire pour qu'ils entendent
les énoncés dans leur langue maternelle.

## Ce qui est déjà fait ✅
- FR, EN, ES → toutes classes, tous MP3 (generate_tts_google.py + generate_en_tts.py)
- DE, IT, PT, RU, UK, AR, ZH → langues VIVANTES (generate_tts_langues.py — script prêt)

## Ce qu'il reste à faire
### Langues maternelles nouvelles à couvrir (GS→CE2 uniquement)
| Code | Langue     | Voix Google TTS         |
|------|------------|-------------------------|
| DE   | Allemand   | de-DE-Neural2-B         |
| IT   | Italien    | it-IT-Neural2-C         |
| PT   | Portugais  | pt-BR-Neural2-B         |
| RU   | Russe      | ru-RU-Neural2-B         |
| UK   | Ukrainien  | uk-UA-Standard-A        |
| AR   | Arabe      | ar-XA-Neural2-B         |
| ZH   | Chinois    | cmn-CN-Neural2-B        |
| PL   | Polonais   | pl-PL-Neural2-B         |
| RO   | Roumain    | ro-RO-Standard-A        |
| BG   | Bulgare    | bg-BG-Standard-A        |
| CS   | Tchèque    | cs-CZ-Standard-A        |
| SK   | Slovaque   | sk-SK-Standard-A        |
| HR   | Croate     | hr-HR-Standard-A        |
| SR   | Serbe      | sr-RS-Standard-A        |
| HU   | Hongrois   | hu-HU-Standard-A        |
| TR   | Turc       | tr-TR-Neural2-B         |
| FA   | Persan     | fa-IR-Standard-B        |

### Classes ciblées : GS, CP, CE1, CE2 uniquement
### Modules ciblés : tout SAUF les langues vivantes (AN/ES/DE/IT/PT/AR/ZH/RU/UK)
Préfixes à inclure : LG (Logique), MA (Maths), SC (Sciences), GE (Géo), HI (Histoire),
                     CG (Culture Générale), DF (Défis)

## Architecture des fichiers
```
audio/
  maternelle/
    DE/
      MA-GS-001_enonce.mp3
      MA-GS-001_rep.mp3
      MA-GS-001_choix_0.mp3
      ...
    RU/
    UK/
    ...
  manifest_maternelle.json
```

## Étapes du script à créer : generate_tts_maternelle.py

### Étape 1 — Extraction
- Lire index.html
- Extraire toutes les questions GS/CP/CE1/CE2 (regex sur DATA.langues inline)
- Filtrer les modules non-langues (exclure préfixes AN/ES/DE/IT/PT/AR/ZH/RU/UK)
- Résultat : ~800-1200 questions × (enonce + rep + 3 choix) = ~4000-6000 textes FR

### Étape 2 — Traduction via Google Translate API
- API : https://translation.googleapis.com/language/translate/v2
- Clé : même clé Google ((dans .env : GOOGLE_TTS_API_KEY)) — vérifier quota
- Tarif : $20 / 1M caractères → ~500K chars × 17 langues ≈ $170 total (ou ~$50 pour 7 langues)
- Batch par 128 textes max (limite API)
- Sauvegarder les traductions dans data/maternelle/{lang}.json avant TTS
  (pour ne pas re-traduire si le script est relancé)

### Étape 3 — Génération MP3
- Même logique que generate_tts_langues.py
- speakingRate: 0.85, pitch: -2.0
- Upload R2 dans audio/maternelle/{LANG}/

### Étape 4 — Intégration index.html
- Lazy-load depuis R2 : _MATERNELLE_CDN / loadMaternelleAudio(lang, classe)
- Bouton TTS sur chaque question GS→CE2 non-langue charge audio/maternelle/{LANG}/

## Coûts estimés
| Service         | Volume             | Coût estimé |
|-----------------|--------------------|-------------|
| Google Translate| ~500K chars × 7L   | ~$7         |
| Google Translate| ~500K chars × 17L  | ~$17        |
| Google TTS      | ~3M chars (Neural2)| ~$12        |
| Google TTS      | ~7M chars (17L)    | ~$28        |
| **Total 7L**    |                    | **~$19**    |
| **Total 17L**   |                    | **~$45**    |

## Clés API disponibles
- Google Cloud (TTS + Translate) : (dans .env : GOOGLE_TTS_API_KEY)
  → Vérifier que l'API Cloud Translation est activée dans la console Google Cloud
  → Console : https://console.cloud.google.com/apis/library/translate.googleapis.com

## Commande pour déclencher
```bash
cd ~/pocketsage
# D'abord vérifier que Cloud Translation API est activée
python3 generate_tts_maternelle.py
```

## Notes importantes
- FR/EN/ES déjà couverts pour TOUTES les classes → ne pas re-générer
- Les langues vivantes (DE apprenant l'allemand) → MP3 dans la langue APPRISE, pas maternelle
- Pour PL/RO/BG/CS/SK/HR/SR/HU/TR/FA : vérifier dispo voix sur https://cloud.google.com/text-to-speech/docs/voices
- Certaines langues n'ont que Standard (pas Neural2) → qualité légèrement inférieure mais acceptable

---

## ✅ RÉALISÉ — Novembre 2026

### Corrections voix (Neural2 inexistantes → Wavenet)
| Code | Voix CORRIGÉE (finale)  | Note                        |
|------|-------------------------|-----------------------------|
| DE   | de-DE-Neural2-B         | ✅ Neural2 OK               |
| IT   | it-IT-Neural2-C         | ✅ Neural2 OK               |
| PT   | pt-BR-Neural2-B         | ✅ Neural2 OK               |
| RU   | ru-RU-Wavenet-B         | ⚠️ Neural2 inexistant → Wavenet |
| UK   | uk-UA-Wavenet-A         | ⚠️ Neural2 inexistant → Wavenet |
| AR   | ar-XA-Wavenet-B         | ⚠️ Neural2 inexistant → Wavenet |
| ZH   | cmn-CN-Wavenet-B        | ⚠️ Neural2 inexistant → Wavenet |

### Résultats generate_tts_maternelle.py
- **14 325 questions** × (enonce + rep + 3 choix) × 7 langues
- **99 268 MP3 générés** (133 erreurs réseau récupérables)
- Uploadés sur R2 : `rclone sync audio/maternelle/ r2:pocketsage-audio/audio/maternelle/`
- Durée sync : 1h27min, 253 fichiers transférés

### Clés API utilisées
- **Google TTS + Translate** : `(dans .env : GOOGLE_TTS_API_KEY)`
  - APIs activées dans la console : Cloud Text-to-Speech + Cloud Translation API
  - Console credentials : https://console.cloud.google.com/apis/credentials

### Paramètres audio définitifs
```python
speakingRate: 0.85
pitch: -2.0
audioEncoding: "MP3"
```

### Reprise après crash
Les deux scripts utilisent un manifest JSON pour reprendre sans re-générer :
```bash
python3 generate_tts_maternelle.py   # reprend depuis audio/manifest_maternelle.json
python3 generate_tts_langues.py      # reprend depuis audio/manifest_langues.json
```

### Upload R2 (commandes finales)
```bash
# Upload par langue vivante
rclone sync audio/de/ r2:pocketsage-audio/audio/de/ --progress
# Upload maternelle complet
rclone sync audio/maternelle/ r2:pocketsage-audio/audio/maternelle/ --progress
```

### UI i18n — TRANSLATIONS + applyLang()
Implémenté dans `index.html` juste avant `function loadApp()` :
- 14 langues : FR EN DE ES IT PT RU UK AR ZH PL RO HU TR
- Fallback FR pour : BG CS SK HR SR FA
- `applyLang()` appelé dans `buildHome()` à chaque changement de profil
- Helper `T('key')` disponible partout dans le JS

→ Voir **`PROCESS_TTS_TRADUCTIONS.md`** pour le process complet de mise à jour.
