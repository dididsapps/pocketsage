# Lot 4 — fiches de révision : Terminale générale (baccalauréat) (11 matières)

Où : **ChatGPT Work**, modèle **GPT-6.1** (Sol si disponible, sinon Terra), réflexion **Ultra**.
Colle le bloc tel quel. À la fin : dépose les JSON dans `docs/contenu/gpt/fiches_revision/reponses/` (ou envoie-les à Claude).
Si le quota coupe : nouvelle tâche, même bloc, en ajoutant à la fin « commence à : REV-XX-YY.json ».

```
MODE AUTONOME : ne m'attends pas entre les matières. Fais-les une par une, en prenant ton temps et en vérifiant
chacune. Enregistre chaque JSON dans un fichier à son nom. Si tu dois t'arrêter, dis seulement « je continue ? »
et reprends où tu en étais. À la fin, vérifie que les 11 fichiers sont valides et donne-moi UN fichier
fiches_revision_lot4.zip à télécharger.

Tu es un professeur expérimenté et un auteur de manuels scolaires. Tu écris les FICHES DE RÉVISION de
l'application éducative PocketSage (lues sur téléphone, écoutées, imprimées) pour les classes et matières
ci-dessous UNIQUEMENT, une matière à la fois, dans l'ordre de la liste.

LISTE (code classe = classe, âge, classe dans l'appli : matière → code matière)
- TLE = Terminale générale (baccalauréat), 17-18 ans, classe appli « Lycée » : Philosophie → PHI ; Histoire → HI ; Géographie → GE ; Enseignement scientifique → ESC ; Anglais → AN ; Espagnol LV2 → ES ; Mathématiques (spécialité) → MA ; Physique-chimie (spécialité) → PC ; SVT (spécialité) → SVT ; SES (spécialité) → SES ; HGGSP (spécialité) → HGG

NOMMAGE (obligatoire, pour que chaque fiche soit retrouvée automatiquement)
- Fichier : REV-<code matière>-<code classe>.json (ex. REV-MA-CM1.json, REV-HGG-TLE.json).
- Fiche : "id" = REV-<code matière>-<code classe>-NN, NN = 01, 02… dans l'ordre du programme.
- "axe" = le nom EXACT du grand axe (thème, chapitre ou partie) tel qu'écrit dans le programme officiel ;
  toutes les fiches d'un même axe portent exactement le même texte d'axe.

PÉDAGOGIE (la fiche doit faire COMPRENDRE, pas seulement réviser) — appuie-toi sur les techniques d'apprentissage dont l'efficacité est la mieux établie par la recherche :
- Expliquer le pourquoi et le comment (élaboration) : chaque fiche dit pourquoi la règle marche ou d'où vient la notion, avec une comparaison ou une image tirée de la vie de l'élève.
- Partir de ce que l'élève sait déjà et faire le lien avec la notion nouvelle.
- Exemple résolu pas à pas (exemple travaillé) avant de laisser l'élève essayer.
- Peu d'informations à la fois (charge mentale) : une seule idée par phrase, l'essentiel d'abord.
- Mots + image mentale (double codage) : décrire un schéma ou une image simple qui aide à retenir.
- Se tester plutôt que relire (récupération active) : le quiz vient APRÈS, sans regarder la fiche ; une question au moins doit faire réfléchir, pas seulement reconnaître.
- Mélanger (pratique entrelacée) : une question du quiz peut reprendre une fiche précédente du même axe.
- Le piège : nommer l'idée fausse la plus courante et montrer pourquoi elle est fausse.
- Ton encourageant, jamais culpabilisant ; aucune promesse de résultat.

RÈGLES (toutes obligatoires)
- Programme officiel de l'Éducation nationale française EN VIGUEUR pour l'année scolaire 2026-2027 (tiens compte des nouveaux programmes entrés en vigueur depuis 2024-2025 quand ils existent). Ne sors jamais du programme de cette classe. En Première et Terminale, vise ce qui tombe au bac (épreuves anticipées de français en Première ; philosophie, spécialités et grand oral en Terminale).
- Couvre TOUT le programme de l'année : avant d'écrire, liste pour toi les attendus de fin d'année de cette classe, puis donne une fiche à CHAQUE notion importante (en général 10 à 16 fiches par matière), rangées par grand axe dans l'ordre où ils sont vus.
- Ne recopie jamais une fiche d'une autre classe : chaque fiche est écrite pour SA classe.
- Une fiche = UNE notion, tenant sur un écran de téléphone et sur une page A4 : court, clair, sans jargon inutile.
- Contenu exact et vérifiable. Pas d'opinion. Pas de date ou de chiffre douteux : en cas de doute, ne le mets pas.
- Vocabulaire adapté à l'âge ; phrases courtes ; tutoiement de l'élève. En GS et CP, la fiche est écoutée ou lue par un adulte : phrases très courtes (10 mots environ), quiz possible à l'oral.
- Exemples concrets du quotidien. Aucune marque, aucune personne réelle vivante, aucun lien.
- Mini-quiz (sans préfixe du type « Sans regarder la fiche ») : 3 questions à choix multiples, une SEULE bonne réponse, la bonne réponse écrite EXACTEMENT comme dans les choix, des pièges plausibles.
- Écris TOUT en français (c'est la langue de référence ; l'application traduira ensuite dans ses autres langues). Pour l'anglais et l'espagnol : explications en français, exemples dans la langue étudiée avec leur traduction.
- Pas d'emoji dans les textes (sauf le champ "emoji"), pas de mise en forme Markdown dans les valeurs JSON.

FORMAT DE SORTIE : UNIQUEMENT un JSON valide, exactement de cette forme :
{
  "classe": "<code classe>", "niveau_appli": "<classe dans l'appli>", "age": "<âge>",
  "matiere": "<matière>", "code": "<code matière>", "langue": "fr",
  "fiches": [
    {
      "id": "REV-<code matière>-<code classe>-01",
      "axe": "nom exact du grand axe du programme",
      "titre": "titre court de la fiche",
      "emoji": "un seul emoji",
      "en_une_phrase": "l'idée clé en une seule phrase",
      "comprendre": "2 à 5 phrases qui expliquent le pourquoi / le comment, avec une comparaison de la vie courante, en partant de ce que l'élève connaît déjà",
      "essentiel": ["3 à 6 phrases courtes : ce qu'il faut retenir"],
      "image_mentale": "un schéma ou une image simple à se représenter (1 à 2 phrases), vide si sans objet",
      "regle_ou_methode": "la règle, la formule ou la méthode en 1 à 3 phrases (vide si sans objet)",
      "exemples": ["2 ou 3 exemples concrets et corrigés, le premier résolu pas à pas"],
      "piege": "l'erreur la plus fréquente et comment l'éviter, en 1 ou 2 phrases",
      "astuce_memoire": "un moyen mnémotechnique ou une image pour retenir (vide si rien de pertinent)",
      "quiz": [
        {"q": "question", "choix": ["A", "B", "C"], "rep": "la bonne réponse, identique à un des choix", "expl": "pourquoi, en 1 phrase"}
      ]
    }
  ]
}
Vérifie toi-même avant de répondre : JSON valide, 3 questions par fiche, "rep" présent dans "choix".
```
