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

4. **Fiches de révision** (nouveau, 18/11) : prompts prêts (GS → Terminale) dans `docs/contenu/gpt/fiches_revision/`
   (une conversation ChatGPT par classe × matière). Déposer chaque JSON dans `reponses/`, Claude fait la
   moulinette puis l'intégration (onglet « 📄 Fiches » dans chaque matière + PDF).

## Fait par Claude (15/11)
- Correction des erreurs des anciennes questions (`docs/contenu/problemes_questions.csv`).
- Niveau « Adulte / Université » (classe `Sup`) : questions universitaires vérifiées + les plus difficiles du lycée.

## Plus tard
- Doublons restants (236 signalés) et niveaux à affiner avec les vrais chiffres du compteur
  (`/api/stats`, base D1 `STATS` à lier dans Cloudflare + secret `STATS_TOKEN`).
- Retirer l'avis bêta (BETA_AVIS) et renommer les lieux réels (Burj, Atlantis…) avant les stores.

## Idées « École sereine » (pas urgent, 18/11) — voir le rapport Claude Doc
Règle : aucun conseil de spécialiste, aucun diagnostic, aucune promesse de santé. Seule phrase autorisée
pour orienter : « En cas de doute, parlez-en à l'enseignant ou au médecin. »
- [ ] Minuteur de devoirs (petits blocs + pause, réglable par le parent)
- [ ] « Contrôle de demain » : révision express ciblée sur une notion choisie
- [ ] Quiz parent élargi (orienter vers le bon parcours « Mes super-pouvoirs »)
- [ ] Journal des progrès (ce qui a été fait cette semaine, sans note ni comparaison)
- [ ] Fiche de liaison parent ↔ enseignant à imprimer (ce qu'on travaille à la maison)
- [ ] Communication : parler d'organisation, de routine et de confiance, jamais de cerveau ni de troubles

## Voix, traductions et coûts Google (21/11)
Constat novembre (1-21) : 74,67 € — Translate 42,99 € (ateliers + flashcards, 6-10/11), Text-to-Speech 31,68 € (voyages du sommeil surtout ; gratuit Neural2 dépassé).
- [ ] **Côté utilisateur :** alerte budget Google Cloud (Facturation → Budgets et alertes) : 80 € pour novembre, puis 10 €/mois dès décembre
- [ ] **Aucune nouvelle voix avant le 1er décembre** (Neural2 payant ce mois-ci)
- [ ] **1er décembre :** MP3 français de TOUTES les fiches de révision (GS → Terminale, ~1 M caractères, Neural2-D, dans le gratuit) + surlignage
- [ ] Fiches de révision traduites dans les 9 langues **par Claude** (pas d'API Translate), relues par un agent ; bouton « FR / ma langue » sur chaque fiche
- [ ] MP3 des autres langues en **WaveNet** (4 M gratuits/mois, puis 4 $/M), étalés sur ~3 mois ; d'abord les langues les plus utilisées (statistiques)
- [ ] Décider : couper l'appel Google Translate du workflow flashcards (flash-tts.yml)
- [ ] Recevoir et passer à la moulinette les lots 3 (4e → Première) et 4 (Terminale)
- [ ] **1er décembre :** MP3 des méditations de Relaxation (RX-001 à 015, Google Neural2-D posée, pauses en SSML) → audio/relax/<id>.mp3, et branchement dans js/relax.js (mode « Court »)

## Comment ça marche ? + Bien parler (validé 23/11 : les 32 thèmes)
- [ ] Prompts GPT prêts : docs/contenu/gpt/comment_ca_marche/LOT_1..4.md (CM-01..22, BP-23..32)
- [ ] Pilote : CM-01 Électricité de la maison (rédigé + schémas animés par Claude) pour valider le format
- [ ] Module appli : tuile « 🛠️ Comment ça marche ? », parcours de leçons, cartes + schémas SVG animés, quiz, « dans ta vie », vidéo « pour aller plus loin » (youtube-nocookie, réglage parent, coupé le soir)
- [ ] « Bien parler » dans Politesse, avec mini-défis
- [ ] Vidéos : liste vérifiée par la moulinette (FR d'abord, EN + sous-titres FR sinon)

## Fiches de révision dans les autres langues (discussion 23/11)
Principe : les fiches suivent le PROGRAMME FRANÇAIS. Public visé : enfants scolarisés en France (ou dans une école française à l'étranger) dont la langue maternelle n'est pas le français.
- [ ] Phase 1 — Traduire toutes les fiches vérifiées dans les 9 langues (Claude + relecture agent), bouton « FR / ma langue », mention « Programme scolaire français »
  - Maths, PC, SVT, ESC, techno : traduction simple + adapter l'écriture des nombres (virgule/point décimal), unités, dates
  - Anglais / espagnol (LV) : traduire les explications, garder les exemples ; masquer les fiches d'anglais quand l'appli est en anglais (idem espagnol)
  - Français (matière) : explications traduites, exemples et règles gardés en français
  - Histoire-géo, SES, HGGSP, philo : traduction fidèle (c'est le programme français) + petit glossaire des mots du cours
- [ ] Glossaire bilingue « les mots du contrôle » par matière et par classe
- [ ] Phase 2 (seulement si les statistiques montrent des élèves scolarisés hors système français) : programmes locaux par pays, en commençant par le plus utilisé ; table d'équivalence des classes (CP = Year 2, 1.º Primaria…) ; maths/sciences réutilisables, histoire-géo et langue nationale à réécrire
