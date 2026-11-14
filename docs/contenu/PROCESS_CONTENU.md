# Ajout de contenu — la « moulinette » (obligatoire à chaque ajout)

Toute question nouvelle ou modifiée passe par ces étapes AVANT d'être publiée :

1. **Écriture** (agent rédacteur) selon `consigne` : programmes officiels, une seule bonne réponse,
   distracteurs plausibles, indice + explication (`expl`).
2. **Relecture indépendante** (autre agent, qui n'a pas écrit les questions) : exactitude (calculs
   refaits, faits vérifiés), unicité de la bonne réponse, cohérence réponse/choix/indice/explication,
   **niveau / tranche d'âge** conforme à la classe. Il corrige ou supprime.
3. **Contrôles automatiques** : `python3 tools/verif_questions.py` (réponse ∈ choix, ids uniques,
   choix non dupliqués) — rejoué par GitHub à chaque push (`verif-contenu.yml`).
4. **Voix** : les MP3 manquants sont créés automatiquement (`maths-tts.yml` → `tools/maths_tts.py`),
   symboles maths lus en mots ; contrôle d'écoute possible avec `verif-voix.yml` (Whisper).
5. **Après la bêta** : compteur anonyme d'erreurs + avis « trop facile / trop dure / pas claire »
   (`/api/stats`) pour reclasser ce qui est mal placé.

Les nouvelles questions vont dans `js/questions-plus-data.js` (chargé après `index.html`).
