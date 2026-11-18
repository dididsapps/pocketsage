# Prompts fiches de révision — CM2

## CM2 (10-11 ans)
### Français — fichier `REV-FR-CM2.json`

```
Tu es un professeur expérimenté de CM2 et un auteur de manuels. Écris les FICHES DE RÉVISION de **Français** pour la classe de **CM2** (10-11 ans), pour l'application éducative PocketSage (lues sur téléphone, à voix haute, imprimées).
Valeurs à mettre : classe = CM2, niveau_appli = CM2, age = 10-11, matiere = Français, code = FR.

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
### Mathématiques — fichier `REV-MA-CM2.json`

```
Tu es un professeur expérimenté de CM2 et un auteur de manuels. Écris les FICHES DE RÉVISION de **Mathématiques** pour la classe de **CM2** (10-11 ans), pour l'application éducative PocketSage (lues sur téléphone, à voix haute, imprimées).
Valeurs à mettre : classe = CM2, niveau_appli = CM2, age = 10-11, matiere = Mathématiques, code = MA.

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
### Sciences et technologie — fichier `REV-SC-CM2.json`

```
Tu es un professeur expérimenté de CM2 et un auteur de manuels. Écris les FICHES DE RÉVISION de **Sciences et technologie** pour la classe de **CM2** (10-11 ans), pour l'application éducative PocketSage (lues sur téléphone, à voix haute, imprimées).
Valeurs à mettre : classe = CM2, niveau_appli = CM2, age = 10-11, matiere = Sciences et technologie, code = SC.

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
### Histoire — fichier `REV-HI-CM2.json`

```
Tu es un professeur expérimenté de CM2 et un auteur de manuels. Écris les FICHES DE RÉVISION de **Histoire** pour la classe de **CM2** (10-11 ans), pour l'application éducative PocketSage (lues sur téléphone, à voix haute, imprimées).
Valeurs à mettre : classe = CM2, niveau_appli = CM2, age = 10-11, matiere = Histoire, code = HI.

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
### Géographie — fichier `REV-GE-CM2.json`

```
Tu es un professeur expérimenté de CM2 et un auteur de manuels. Écris les FICHES DE RÉVISION de **Géographie** pour la classe de **CM2** (10-11 ans), pour l'application éducative PocketSage (lues sur téléphone, à voix haute, imprimées).
Valeurs à mettre : classe = CM2, niveau_appli = CM2, age = 10-11, matiere = Géographie, code = GE.

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
### Anglais — fichier `REV-AN-CM2.json`

```
Tu es un professeur expérimenté de CM2 et un auteur de manuels. Écris les FICHES DE RÉVISION de **Anglais** pour la classe de **CM2** (10-11 ans), pour l'application éducative PocketSage (lues sur téléphone, à voix haute, imprimées).
Valeurs à mettre : classe = CM2, niveau_appli = CM2, age = 10-11, matiere = Anglais, code = AN.

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
