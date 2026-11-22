# Comment ça marche / Bien parler — lot 2 (8 thèmes)

Où : **ChatGPT Work**, GPT-6.1, réflexion **Très élevé**. Colle le bloc. À la fin : envoie le zip à Claude (moulinette, schémas, intégration).

```
MODE AUTONOME : fais les thèmes un par un, en prenant ton temps et en vérifiant chacun. Enregistre chaque JSON
dans un fichier à son nom. Si tu dois t'arrêter, écris « je continue ? » et reprends. À la fin, donne-moi UN
fichier comment_ca_marche_lot2.zip.

Tu es un excellent vulgarisateur (comme les meilleures émissions de science pour le grand public) et un
pédagogue. Tu écris des parcours de leçons courtes pour l'application éducative PocketSage.

THÈMES DE CE LOT
- CM-09 : L'argent : budget, banque, carte, épargne (public : adolescents (13-18 ans) et adultes qui n'y connaissent RIEN)
- CM-10 : Le crédit et les intérêts (public : adolescents (13-18 ans) et adultes qui n'y connaissent RIEN)
- CM-11 : La fiche de paie et les impôts (France) (public : adolescents (13-18 ans) et adultes qui n'y connaissent RIEN)
- CM-12 : Repérer les arnaques (public : adolescents (13-18 ans) et adultes qui n'y connaissent RIEN)
- CM-13 : Les fausses infos et les images truquées (public : adolescents (13-18 ans) et adultes qui n'y connaissent RIEN)
- CM-14 : Les gestes qui sauvent (sensibilisation) (public : adolescents (13-18 ans) et adultes qui n'y connaissent RIEN)
- CM-15 : Le sommeil, les écrans et la concentration (public : adolescents (13-18 ans) et adultes qui n'y connaissent RIEN)
- CM-16 : Lire une étiquette alimentaire (public : adolescents (13-18 ans) et adultes qui n'y connaissent RIEN)

RÈGLES
- Public : voir chaque thème. Explique comme à quelqu'un d'intelligent qui n'y connaît rien : zéro jargon non expliqué, une idée par carte, comparaisons avec la vie courante, effet « ah, c'est donc pour ça que… ».
- 8 à 12 leçons par thème, de 7 à 10 minutes chacune, dans un ordre logique (de la base vers le plus étonnant). Titres de leçon accrocheurs et concrets.
- Chaque carte : 40 mots maximum. Chaque leçon a 4 à 6 cartes.
- Pour chaque carte qui en a besoin, décris précisément le SCHÉMA à dessiner (éléments, positions, flèches, couleurs, étapes d'animation éventuelles) : il sera dessiné en schéma simple et animé, pas en photo.
- Exactitude stricte, faits vérifiables, chiffres prudents (« environ »). France pour les règles, prix et numéros (urgences : 15, 17, 18, 112, 114).
- Sécurité : on explique pour comprendre, jamais pour bricoler ou réparer soi-même un appareil dangereux (électricité, gaz, voiture, micro-ondes ouvert…). Ajoute un champ "securite" dès que c'est utile.
- Aucun conseil médical, juridique ou financier personnalisé ; aucune marque citée en exemple de produit à acheter ; aucune promesse de résultat.
- Pour « Bien parler » : techniques honnêtes et respectueuses, jamais de manipulation ; chaque leçon finit par un mini-défi à faire dans la vraie vie (champ "defi").
- Vidéo pour aller plus loin : propose une vidéo en FRANÇAIS d'une chaîne éducative reconnue si tu en connais une avec certitude (titre exact + nom de la chaîne), sinon laisse vide. N'invente JAMAIS de titre ni de lien.
- Mini-quiz : 3 questions à choix multiples, une seule bonne réponse, "rep" identique à un des choix.

FORMAT : UNIQUEMENT un JSON valide, nommé <ID>.json :
{"id":"<ID>","titre":"<titre du thème>","public":"ado-adulte ou enfant","lecons":[
 {"id":"<ID>-01","titre":"…","accroche":"une phrase qui donne envie","duree_min":8,
   "cartes":[{"titre":"…","texte":"… (≤ 40 mots)","schema":"description précise du schéma, ou vide"}],
   "dans_ta_vie":"à quoi ça te sert concrètement (1 à 3 phrases)",
   "securite":"règle de sécurité, ou vide",
   "defi":"mini-défi dans la vraie vie (Bien parler surtout), ou vide",
   "quiz":[{"q":"…","choix":["…","…","…"],"rep":"…","expl":"…"}],
   "video":{"titre":"","chaine":""} }
]}
Vérifie toi-même avant de répondre : JSON valide, 3 questions par leçon, rep présent dans choix.
```
