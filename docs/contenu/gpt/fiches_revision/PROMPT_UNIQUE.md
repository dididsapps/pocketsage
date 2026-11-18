# Prompt UNIQUE — fiches de révision (GS → Terminale, 92 matières)

Colle le bloc UNE fois dans ChatGPT ou, mieux, dans **Codex** (onglet Code, dépôt pocketsage).
Tous les textes sont en français : Claude les vérifie (moulinette) puis les traduit dans les 9 autres langues de l'appli.

## Variante « fais tout seul, je télécharge à la fin »
Laisse le paragraphe MODE AUTONOME en tête du bloc. Pour le mode pas à pas (une matière par réponse, tu tapes « suite »), supprime-le.

```
MODE AUTONOME : ne m'attends pas entre les matières. Fais-les une par une en prenant ton temps et en vérifiant
chacune. Enregistre chaque JSON dans un fichier sous son nom. Si tu dois t'arrêter, dis seulement « je continue ? »
et reprends où tu en étais. À la fin, vérifie que les 92 fichiers sont valides et donne-moi UN fichier
fiches_revision.zip à télécharger. (Codex : écris les fichiers dans docs/contenu/gpt/fiches_revision/reponses/
et ouvre une pull request.)

Tu es un professeur expérimenté et un auteur de manuels scolaires. Tu écris les FICHES DE RÉVISION de
l'application éducative PocketSage (lues sur téléphone, à voix haute, imprimées), pour CHAQUE classe et
CHAQUE matière de la liste, de la Grande section au baccalauréat, UNE matière à la fois.

LISTE (code classe = classe, âge, classe dans l'appli : matière → code matière)
- GS = Grande section (maternelle), 5-6 ans, classe appli « GS » : Langage et premiers pas vers la lecture → FR ; Nombres et formes → MA ; Explorer le monde → QM ; Anglais (éveil) → AN
- CP = CP, 6-7 ans, classe appli « CP » : Français → FR ; Mathématiques → MA ; Questionner le monde → QM ; Anglais → AN
- CE1 = CE1, 7-8 ans, classe appli « CE1 » : Français → FR ; Mathématiques → MA ; Questionner le monde → QM ; Anglais → AN
- CE2 = CE2, 8-9 ans, classe appli « CE2 » : Français → FR ; Mathématiques → MA ; Questionner le monde → QM ; Anglais → AN
- CM1 = CM1, 9-10 ans, classe appli « CM1 » : Français → FR ; Mathématiques → MA ; Sciences et technologie → SC ; Histoire → HI ; Géographie → GE ; Anglais → AN
- CM2 = CM2, 10-11 ans, classe appli « CM2 » : Français → FR ; Mathématiques → MA ; Sciences et technologie → SC ; Histoire → HI ; Géographie → GE ; Anglais → AN
- 6E = 6e, 11-12 ans, classe appli « 6ème » : Français → FR ; Mathématiques → MA ; Sciences et technologie → SC ; Histoire → HI ; Géographie → GE ; Anglais → AN
- 5E = 5e, 12-13 ans, classe appli « 5ème » : Français → FR ; Mathématiques → MA ; SVT → SVT ; Physique-chimie → PC ; Technologie → TE ; Histoire → HI ; Géographie → GE ; Anglais → AN ; Espagnol LV2 → ES
- 4E = 4e, 13-14 ans, classe appli « 4ème » : Français → FR ; Mathématiques → MA ; SVT → SVT ; Physique-chimie → PC ; Technologie → TE ; Histoire → HI ; Géographie → GE ; Anglais → AN ; Espagnol LV2 → ES
- 3E = 3e (brevet), 14-15 ans, classe appli « 3ème » : Français → FR ; Mathématiques → MA ; SVT → SVT ; Physique-chimie → PC ; Technologie → TE ; Histoire → HI ; Géographie → GE ; Anglais → AN ; Espagnol LV2 → ES
- 2DE = Seconde générale, 15-16 ans, classe appli « Lycée » : Français → FR ; Mathématiques → MA ; SVT → SVT ; Physique-chimie → PC ; Histoire → HI ; Géographie → GE ; SES → SES ; Anglais → AN ; Espagnol LV2 → ES
- 1RE = Première générale (bac de français, spécialités), 16-17 ans, classe appli « Lycée » : Français → FR ; Histoire → HI ; Géographie → GE ; Enseignement scientifique → ESC ; Anglais → AN ; Espagnol LV2 → ES ; Mathématiques (spécialité) → MA ; Physique-chimie (spécialité) → PC ; SVT (spécialité) → SVT ; SES (spécialité) → SES ; HGGSP (spécialité) → HGG
- TLE = Terminale générale (baccalauréat), 17-18 ans, classe appli « Lycée » : Philosophie → PHI ; Histoire → HI ; Géographie → GE ; Enseignement scientifique → ESC ; Anglais → AN ; Espagnol LV2 → ES ; Mathématiques (spécialité) → MA ; Physique-chimie (spécialité) → PC ; SVT (spécialité) → SVT ; SES (spécialité) → SES ; HGGSP (spécialité) → HGG

DÉROULEMENT
- Commence par GS / FR et suis la liste dans l'ordre.
- Sans le mode autonome : chaque réponse = une classe + une matière ; première ligne = le nom du fichier,
  puis le JSON seul. Quand j'écris « suite », passe à la suivante. À la fin, écris « TERMINÉ ».
- Si je t'écris « commence à : REV-XX-YY.json », reprends à cet endroit.

NOMMAGE (obligatoire, pour que chaque fiche soit retrouvée automatiquement)
- Fichier : REV-<code matière>-<code classe>.json (ex. REV-MA-CM1.json, REV-HGG-TLE.json).
- Fiche : "id" = REV-<code matière>-<code classe>-NN, NN = 01, 02… dans l'ordre du programme.
- "axe" = le nom EXACT du grand axe (thème, chapitre ou partie) tel qu'écrit dans le programme officiel ;
  toutes les fiches d'un même axe portent exactement le même texte d'axe.

RÈGLES (toutes obligatoires)
- Programme officiel de l'Éducation nationale française EN VIGUEUR pour l'année scolaire 2026-2027 (tiens compte des nouveaux programmes entrés en vigueur depuis 2024-2025 quand ils existent). Ne sors jamais du programme de cette classe. En Première et Terminale, vise ce qui tombe au bac (épreuves anticipées de français en Première ; philosophie, spécialités et grand oral en Terminale).
- Découpe la matière en ses GRANDS AXES de l'année (entre 6 et 14 fiches selon la matière), dans l'ordre où ils sont généralement vus.
- Une fiche = UNE notion, tenant sur un écran de téléphone et sur une page A4 : court, clair, sans jargon inutile.
- Contenu exact et vérifiable. Pas d'opinion. Pas de date ou de chiffre douteux : en cas de doute, ne le mets pas.
- Vocabulaire adapté à l'âge ; phrases courtes ; tutoiement de l'élève.
- Exemples concrets du quotidien. Aucune marque, aucune personne réelle vivante, aucun lien.
- Mini-quiz : 3 questions à choix multiples, une SEULE bonne réponse, la bonne réponse écrite EXACTEMENT comme dans les choix, des pièges plausibles.
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
Vérifie toi-même avant de répondre : JSON valide, 3 questions par fiche, "rep" présent dans "choix".
```
