# Contenu — reste à faire (mis à jour le 15/11/2026)

Toute création ou modification passe par la moulinette (docs/contenu/PROCESS_CONTENU.md) :
écriture → relecture par un AUTRE modèle/agent → `tools/verif_questions.py` → MP3 automatiques.

## Prévu avec GPT (Codex / ChatGPT), relu ensuite par Claude (ou l'inverse)
1. **Anglais et Espagnol 3e + Lycée** : 10 questions seulement par niveau (viser 60). 5e/4e : 25-35 (viser 60).
2. **Culture générale** : 58 questions (GS→CE2 seulement) ; à étendre à tous les niveaux.
3. **Explications après une erreur** (`expl`) pour les 1 177 questions difficiles listées dans
   `docs/contenu/tri_explications.json` (besoin = "oui", avec ce qu'il faut expliquer et le piège probable).
   Format : 1-2 phrases (≤ 35 mots), adaptées à l'âge ; puis affichage « 💡 Pourquoi ? » + voix.
   (Les 1 059 questions ajoutées le 14-15/11 ont déjà leur `expl`.)

## Fait par Claude (15/11)
- Correction des erreurs des anciennes questions (`docs/contenu/problemes_questions.csv`).
- Niveau « Adulte / Université » (classe `Sup`) : questions universitaires vérifiées + les plus difficiles du lycée.

## Plus tard
- Doublons restants (236 signalés) et niveaux à affiner avec les vrais chiffres du compteur
  (`/api/stats`, base D1 `STATS` à lier dans Cloudflare + secret `STATS_TOKEN`).
- Retirer l'avis bêta (BETA_AVIS) et renommer les lieux réels (Burj, Atlantis…) avant les stores.
