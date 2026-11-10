# Étude de tarification PocketSage (dossier ouvert le 10/11/2026)

Dossier de travail : idées de prix, de formules d'abonnement, et coûts associés à chaque fonctionnalité. Rien n'est décidé tant que ce n'est pas marqué ✅.

## 1. Repères marché (voir `docs/flash/01_concurrents_antiscroll.md`)

- Applis « anti-scroll » adultes (Deepstash, Headway, Imprint, Blinkist…) : 70 à 240 $/an **par personne**.
- Plainte n°1 des utilisateurs : facturation agressive, annulation difficile.
- Piste notée : **abonnement famille** sous le prix individuel des concurrents (ex. 5-7 €/mois ou 40-50 €/an, à tester), annulation en 1 clic, pas d'essai piège.

## 2. Formules envisagées (brouillon)

| Formule | Contenu | Prix (à tester) |
|---|---|---|
| Gratuite | Découverte : quelques modules / limite quotidienne | 0 € |
| Famille | Tous les modules, 4 profils, hors-ligne, fiches PDF | ~5-7 €/mois |
| Famille+ (premium) | Famille + **prononciation évaluée précisément** (voir §3) + futurs services coûteux | à définir |

## 3. Fonctionnalité premium candidate : évaluation précise de la prononciation

- **Aujourd'hui (gratuit)** : reconnaissance vocale du téléphone (Google/Apple). Améliorée le 10/11/2026 (mots courts, homophones, nombres, accents), mais elle devine le mot au lieu de noter l'accent → précision limitée.
- **Option premium** : Microsoft Azure Pronunciation Assessment (note par mot et par son, comme les applis de langues spécialisées).
  - Coût indicatif : ~1 $ par heure d'audio (≈ 1 € pour 1 000 essais de 3 s). Petit volume gratuit mensuel. **Tarif à reconfirmer** sur la page de prix Azure avant décision.
  - Mise en place : clé gardée sur un petit serveur Cloudflare (Worker), activé uniquement pour les abonnés premium. Les autres gardent la version gratuite.
  - Vie privée : la voix part chez Microsoft (région Europe) → à mentionner aux parents.
  - Décision 10/11/2026 : **coût jugé trop élevé pour l'instant** ; à prévoir comme option des abonnements plus chers.

## 4. Coûts récurrents connus (à compléter)

| Poste | Fournisseur | Remarque |
|---|---|---|
| Hébergement site | Cloudflare Pages | gratuit au volume actuel |
| Stockage MP3/PDF | Cloudflare R2 | faible (pas de frais de sortie) |
| Voix enfants (MP3 pré-générés) | ElevenLabs | forfait mensuel en crédits |
| Voix + traductions | Google TTS / Translate | quelques centimes par génération |
| Domaine | OVH | annuel |
| Publication stores | Google Play 25 $ (une fois), App Store 99 $/an | |

## 5. À faire

- [ ] Choisir ce qui reste gratuit vs payant.
- [ ] Estimer l'usage moyen de la prononciation par enfant et par mois → coût premium par abonné.
- [ ] Tester 2-3 prix auprès des parents bêta (questionnaire).
