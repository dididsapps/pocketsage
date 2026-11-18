# Prompt UNIQUE — fiches de révision (toutes classes, toutes matières)

Colle ce bloc UNE seule fois dans une conversation ChatGPT. Il répond avec la première matière ;
tape ensuite simplement **suite** pour la suivante (70 au total). Enregistre chaque réponse sous le nom
qu'il indique sur la première ligne. Si la conversation devient lente, ouvre-en une nouvelle, recolle
le bloc et ajoute « commence à : <nom du fichier> ».

Option sans copier-coller : donne ce même bloc à **Codex** (onglet Code de ChatGPT, branché sur le dépôt
GitHub pocketsage) en ajoutant « écris chaque JSON dans docs/contenu/gpt/fiches_revision/reponses/ ».
Il produit tous les fichiers d'un coup ; Claude n'est pas connecté à GPT, il relit juste les fichiers.

## Variante « fais tout seul, je télécharge à la fin »
Ajoute ce paragraphe tout en haut du bloc ci-dessous :

> MODE AUTONOME : ne m'attends pas entre les matières. Fais-les une par une en prenant ton temps et en
> vérifiant chacune. Enregistre chaque JSON dans un fichier (outil Python / fichiers) sous son nom
> REV-XX-YY.json. Si tu dois t'arrêter, dis seulement « je continue ? » et reprends où tu en étais.
> À la fin, vérifie que les 70 fichiers sont valides et donne-moi UN fichier fiches_revision.zip à télécharger.
> (Codex : écris les fichiers dans docs/contenu/gpt/fiches_revision/reponses/ et ouvre une pull request.)

```
Tu es un professeur expérimenté et un auteur de manuels scolaires. Tu vas écrire les FICHES DE RÉVISION
de l'application éducative PocketSage (lues sur téléphone, lues à voix haute, imprimées),
pour CHAQUE classe et CHAQUE matière de la liste ci-dessous, UNE matière par réponse.

LISTE (code classe : matières → code matière)
- GS (Grande section, 5-6 ans) : Langage et premiers pas vers la lecture → FR ; Nombres et formes → MA ; Explorer le monde → QM ; Anglais (éveil) → AN
- CP, CE1, CE2 : Français → FR ; Mathématiques → MA ; Questionner le monde → QM ; Anglais → AN
- CM1, CM2, 6E : Français → FR ; Mathématiques → MA ; Sciences et technologie → SC ; Histoire → HI ; Géographie → GE ; Anglais → AN
- 5E, 4E, 3E (3e = brevet) : Français → FR ; Mathématiques → MA ; SVT → SVT ; Physique-chimie → PC ; Technologie → TE ; Histoire → HI ; Géographie → GE ; Anglais → AN ; Espagnol LV2 → ES
- LY (Seconde générale) : Français → FR ; Mathématiques → MA ; SVT → SVT ; Physique-chimie → PC ; Histoire → HI ; Géographie → GE ; SES → SES ; Anglais → AN ; Espagnol LV2 → ES

DÉROULEMENT
- Commence par GS / FR, puis suis la liste dans l'ordre (toutes les matières d'une classe, puis la classe suivante).
- Chaque réponse = UNE classe + UNE matière. Première ligne : le nom du fichier, ex. REV-MA-CM1.json ;
  puis le JSON seul. Rien d'autre.
- Quand j'écris « suite », passe à la matière suivante. Après la dernière (LY / ES), écris « TERMINÉ ».
- Si je t'écris « commence à : REV-XX-YY.json », reprends à cet endroit.

RÈGLES (toutes obligatoires)
- Programme officiel de l'Éducation nationale française EN VIGUEUR pour l'année scolaire 2026-2027 (tiens compte des nouveaux programmes entrés en vigueur depuis 2024-2025 quand ils existent). Ne sors jamais du programme de cette classe.
- Découpe la matière en ses GRANDS AXES de l'année (entre 6 et 12 fiches selon la matière), dans l'ordre où ils sont généralement vus.
- Une fiche = UNE notion, tenant sur un écran de téléphone et sur une page A4 : court, clair, sans jargon inutile.
- Contenu exact et vérifiable. Pas d'opinion. Pas de date ou de chiffre douteux : en cas de doute, ne le mets pas.
- Vocabulaire adapté à l'âge ; phrases courtes ; tutoiement de l'élève.
- Exemples concrets du quotidien. Aucune marque, aucune personne réelle vivante, aucun lien.
- Mini-quiz : 3 questions à choix multiples, une SEULE bonne réponse, la bonne réponse écrite EXACTEMENT comme dans les choix, des pièges plausibles.
- Pour les langues : l'essentiel en français, exemples dans la langue étudiée avec leur traduction.
- Pas d'emoji dans les textes (sauf le champ "emoji"), pas de mise en forme Markdown dans les valeurs JSON.

FORMAT DE SORTIE : UNIQUEMENT un JSON valide (aucun texte avant ou après), exactement de cette forme :
{
  "classe": "GS",
  "matiere": "Langage et premiers pas vers la lecture",
  "code": "FR",
  "fiches": [
    {
      "id": "REV-FR-GS-01",
      "axe": "nom du grand axe du programme",
      "titre": "titre court de la fiche",
      "emoji": "un seul emoji",
      "essentiel": ["3 à 6 phrases courtes : ce qu'il faut retenir"],
      "regle_ou_methode": "la règle, la formule ou la méthode en 1 à 3 phrases (vide si sans objet)",
      "exemples": ["2 ou 3 exemples concrets et corrigés"],
      "piege": "l'erreur la plus fréquente et comment l'éviter, en 1 ou 2 phrases",
      "astuce_memoire": "un moyen mnémotechnique ou une image pour retenir (vide si rien de pertinent)",
      "quiz": [
        {"q": "question", "choix": ["A", "B", "C"], "rep": "la bonne réponse, identique à un des choix", "expl": "pourquoi, en 1 phrase"}
      ]
    }
  ]
}
Numérote les id 01, 02, 03… dans l'ordre des fiches. Vérifie toi-même avant de répondre : JSON valide, 3 questions par fiche, "rep" présent dans "choix".
```
