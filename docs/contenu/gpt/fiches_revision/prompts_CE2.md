# Prompts fiches de révision — CE2

## CE2 (8-9 ans)
### Français — fichier `REV-FR-CE2.json`

```
Tu es un professeur expérimenté de CE2 et un auteur de manuels. Écris les FICHES DE RÉVISION de **Français** pour la classe de **CE2** (8-9 ans), pour l'application éducative PocketSage (lues sur téléphone, à voix haute, imprimées).
Valeurs à mettre : classe = CE2, niveau_appli = CE2, age = 8-9, matiere = Français, code = FR.

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
- Découpe la matière en ses GRANDS AXES de l'année (entre 6 et 14 fiches selon la matière), dans l'ordre où ils sont généralement vus.
- Une fiche = UNE notion, tenant sur un écran de téléphone et sur une page A4 : court, clair, sans jargon inutile.
- Contenu exact et vérifiable. Pas d'opinion. Pas de date ou de chiffre douteux : en cas de doute, ne le mets pas.
- Vocabulaire adapté à l'âge ; phrases courtes ; tutoiement de l'élève. En GS et CP, la fiche est écoutée ou lue par un adulte : phrases très courtes (10 mots environ), quiz possible à l'oral.
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
### Mathématiques — fichier `REV-MA-CE2.json`

```
Tu es un professeur expérimenté de CE2 et un auteur de manuels. Écris les FICHES DE RÉVISION de **Mathématiques** pour la classe de **CE2** (8-9 ans), pour l'application éducative PocketSage (lues sur téléphone, à voix haute, imprimées).
Valeurs à mettre : classe = CE2, niveau_appli = CE2, age = 8-9, matiere = Mathématiques, code = MA.

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
- Découpe la matière en ses GRANDS AXES de l'année (entre 6 et 14 fiches selon la matière), dans l'ordre où ils sont généralement vus.
- Une fiche = UNE notion, tenant sur un écran de téléphone et sur une page A4 : court, clair, sans jargon inutile.
- Contenu exact et vérifiable. Pas d'opinion. Pas de date ou de chiffre douteux : en cas de doute, ne le mets pas.
- Vocabulaire adapté à l'âge ; phrases courtes ; tutoiement de l'élève. En GS et CP, la fiche est écoutée ou lue par un adulte : phrases très courtes (10 mots environ), quiz possible à l'oral.
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
### Questionner le monde — fichier `REV-QM-CE2.json`

```
Tu es un professeur expérimenté de CE2 et un auteur de manuels. Écris les FICHES DE RÉVISION de **Questionner le monde** pour la classe de **CE2** (8-9 ans), pour l'application éducative PocketSage (lues sur téléphone, à voix haute, imprimées).
Valeurs à mettre : classe = CE2, niveau_appli = CE2, age = 8-9, matiere = Questionner le monde, code = QM.

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
- Découpe la matière en ses GRANDS AXES de l'année (entre 6 et 14 fiches selon la matière), dans l'ordre où ils sont généralement vus.
- Une fiche = UNE notion, tenant sur un écran de téléphone et sur une page A4 : court, clair, sans jargon inutile.
- Contenu exact et vérifiable. Pas d'opinion. Pas de date ou de chiffre douteux : en cas de doute, ne le mets pas.
- Vocabulaire adapté à l'âge ; phrases courtes ; tutoiement de l'élève. En GS et CP, la fiche est écoutée ou lue par un adulte : phrases très courtes (10 mots environ), quiz possible à l'oral.
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
### Anglais — fichier `REV-AN-CE2.json`

```
Tu es un professeur expérimenté de CE2 et un auteur de manuels. Écris les FICHES DE RÉVISION de **Anglais** pour la classe de **CE2** (8-9 ans), pour l'application éducative PocketSage (lues sur téléphone, à voix haute, imprimées).
Valeurs à mettre : classe = CE2, niveau_appli = CE2, age = 8-9, matiere = Anglais, code = AN.

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
- Découpe la matière en ses GRANDS AXES de l'année (entre 6 et 14 fiches selon la matière), dans l'ordre où ils sont généralement vus.
- Une fiche = UNE notion, tenant sur un écran de téléphone et sur une page A4 : court, clair, sans jargon inutile.
- Contenu exact et vérifiable. Pas d'opinion. Pas de date ou de chiffre douteux : en cas de doute, ne le mets pas.
- Vocabulaire adapté à l'âge ; phrases courtes ; tutoiement de l'élève. En GS et CP, la fiche est écoutée ou lue par un adulte : phrases très courtes (10 mots environ), quiz possible à l'oral.
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
