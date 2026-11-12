# Étude de tarification PocketSage (dossier ouvert le 10/11/2026)

Dossier de travail : idées de prix, de formules d'abonnement, et coûts associés à chaque fonctionnalité. Rien n'est décidé tant que ce n'est pas marqué ✅.

## 1. Repères marché (voir `docs/flash/01_concurrents_antiscroll.md`)

- Applis « anti-scroll » adultes (Deepstash, Headway, Imprint, Blinkist…) : 70 à 240 $/an **par personne**.
- Plainte n°1 des utilisateurs : facturation agressive, annulation difficile.
- Piste notée : **abonnement famille** sous le prix individuel des concurrents (ex. 5-7 €/mois ou 40-50 €/an, à tester), annulation en 1 clic, pas d'essai piège.

## 2. Formules envisagées (brouillon)

| Formule | Contenu | Prix (à tester) |
|---|---|---|
| Gratuite | Découverte : quelques modules / limite quotidienne ; **jeux : 15 min/jour** ; fin de jeu → fiche PDF seulement | 0 € |
| Famille | Tous les modules, 4 profils, hors-ligne, fiches PDF ; **jeux : 45 min/jour par défaut, réglable par le parent jusqu'à illimité** ; fin de jeu → fiche, histoire ou aventure | ~5-7 €/mois |
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

## 6. Idées pour l'offre gratuite (12/11/2026 — à décider, rien codé)
- **Un module par jour, 10 min** ; le lendemain un autre module (rotation automatique) → l'enfant découvre tout en environ une semaine.
- Variante proposée : le parent peut **choisir le module du jour** (ex. Langues la veille d'un contrôle d'anglais).
- **Jeux : 15 min/jour** (déjà en place, voir `docs/jeux/README.md`).
- **Toujours libres, même en gratuit** (idée à valider) : **Sport** (l'écran ne sert qu'aux consignes, l'enfant bouge) et **fiches PDF** (travail sur papier).
- Abonnés : **Sport sans limite** ; jeux 45 min réglable ; temps d'écran total en option (désactivé par défaut) — à rediscuter.

### Option B (12/11/2026) — Aventure + découverte
- **Mode Aventure** gratuit chaque jour, durée selon l'âge (ex. 4-6 ans : 10 min · 7-10 ans : 15 min · 11 ans et + : 20 min). L'Aventure mélange déjà les matières → l'enfant goûte à tout.
- **+ 5 min/jour de découverte** : l'enfant peut ouvrir n'importe quel autre module pour l'essayer.
- **+ jeux 15 min/jour** ; **sport et fiches PDF libres**.
- ⚠️ Règle stores (Google Play « Familles », Apple « Enfants ») : **ne jamais pousser l'enfant à acheter**. Côté enfant : « C'est fini pour aujourd'hui, à demain ! ». Proposition d'abonnement **uniquement côté parent** (Espace Parents protégé par PIN, ou message au parent).
- Option A (module du jour) et option B à départager au moment de créer les abonnements.

## 7. Contacter les parents (12/11/2026 — à faire au lancement, rien codé)
- Aujourd'hui : aucun compte, aucun email, tout reste sur le téléphone (atout vie privée).
- **Paiement des abonnements par Google Play / App Store** : ils gèrent le compte parent, le paiement et le contrôle parental → pas besoin de notre côté de données bancaires ni même d'email.
- **Email du parent facultatif**, demandé **dans l'Espace Parents (PIN)**, jamais à l'enfant ; usage expliqué : **bilan hebdomadaire** des progrès.
- **Bilans** : envoyés à ceux qui ont donné leur email pour ça (lien « ne plus recevoir » dans chaque email). Pas de publicité appuyée dedans (sinon = email commercial) ; une mention neutre ou un lien vers l'Espace Parents reste acceptable.
- **Offres / abonnement par email** : seulement avec une **case séparée non cochée** (« Je souhaite recevoir les nouveautés et offres »). Accord préalable obligatoire pour la prospection par email des particuliers.
- La CNIL juge qu'un simple email ne prouve pas l'accord parental (facile à contourner) → ne pas s'en servir comme « preuve de consentement ».
- Prestataire email avec données en Europe + contrat de traitement (DPA) ; droit de suppression ; mention dans la politique de confidentialité.
- Faire relire la politique de confidentialité par un juriste avant le lancement.

## 8. Parcours de vente proposé (12/11/2026 — à valider, rien codé)
- ❌ **Interdit : obliger à cocher la case « offres » pour utiliser le gratuit.** Un consentement doit être libre ; le rendre obligatoire pour accéder au service le rend invalide (RGPD art. 7 §4, sanctions CNIL). Les stores « Enfants / Familles » le refuseraient aussi.
- Vérifier que c'est « vraiment » un parent : impossible et pas demandé (on ne collecte pas de données sur l'enfant). Les stores exigent seulement une **barrière parentale** (« parental gate ») : une tâche qu'un jeune enfant ne sait pas faire (ex. question écrite en toutes lettres, chiffres à taper) avant tout achat, lien externe ou réglage.
- **1ʳᵉ ouverture = « À faire par un adulte (2 min) »** : barrière parentale → création du PIN → profils enfants → **proposition d'essai gratuit de 7 jours de l'abonnement Famille** (géré par Google/Apple, rappel avant la fin) → email facultatif pour le bilan hebdo + case séparée non cochée pour les offres. Le parent n'est présent qu'une fois.
- Côté enfant : jamais de proposition d'achat ni de « demande à tes parents d'acheter » ; message neutre « C'est fini pour aujourd'hui, à demain ! ».
- Leviers de vente légaux : essai gratuit ; bilan hebdo par email (le parent voit les progrès) ; dans l'Espace Parents, aperçu de ce que l'abonnement débloque ; prix annuel avantageux ; prix famille.
- Page web parent : pas nécessaire au départ (tout se fait dans l'appli) ; utile plus tard si comptes.
- Faire relire ce parcours par un juriste avant le lancement.
- (12/11) Enfant qui installe seul et passe la barrière parentale : acceptable — la barrière est une mesure raisonnable, pas une preuve ; aucune donnée sur l'enfant n'est collectée ; **l'achat lui-même est protégé par le store** (mot de passe / Face ID du titulaire du compte, « Demander l'autorisation d'achat » Apple, approbation Family Link Google pour les comptes enfants). Dès 15 ans en France, l'ado peut consentir seul au traitement de ses données.
- Barrière un peu plus dure pour les grands : ex. « Écris en chiffres : trois cent quarante-sept moins vingt-huit » plutôt que « quarante-huit ».
- **Bouton « S'abonner » dans l'Espace Parents, SANS exiger l'email** (le store gère le paiement ; exiger l'email = donnée non nécessaire + moins de ventes). Email proposé juste après, facultatif, pour le bilan ; case offres séparée non cochée.
- (12/11) **Barrière parentale — détails** : le nombre est écrit en lettres mais la réponse se tape **en chiffres** → les fautes d'orthographe du parent ne comptent pas. Nouvelle question à chaque essai ; après 3 erreurs, pause de 30 s (empêche l'enfant de tenter au hasard). Question affichée **dans la langue du parent** (langue maternelle choisie). Niveau visé : faisable par un ado de 15 ans et +, c'est la pratique admise (mesure raisonnable, pas une preuve).
- **PIN oublié** (n'existe pas encore dans l'appli : aujourd'hui un parent qui oublie son PIN est bloqué) : après 3-4 PIN faux → « PIN oublié ? » → nouvelle barrière parentale → nouveau PIN. Si un email a été donné : réinitialisation possible aussi par lien email (plus sûr). Les achats restent protégés par le store dans tous les cas.
- ✅ 12/11 : **« Code oublié ? » codé** dans l'Espace Parents (après 3 codes faux → barrière parentale → nouveau code ; pause 30 s après 3 réponses fausses). En français : nombre en lettres, réponse en chiffres ; autres langues : calcul (ex. 47 × 6 + 23). Le code par défaut (1234) n'est plus affiché une fois que le parent l'a changé.
- Message de fin côté enfant autorisé : « Bravo, séance terminée ! Montre à tes parents ce que tu as appris aujourd'hui. À demain ! » — **interdit** : « Demande à tes parents… » pour acheter / débloquer (incitation directe des enfants à faire acheter leurs parents : directive 2005/29/CE annexe I point 28, Code de la consommation).
