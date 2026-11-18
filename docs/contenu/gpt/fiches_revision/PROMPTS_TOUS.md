# Prompts ChatGPT — fiches de révision PocketSage
Mode d'emploi : copie UN bloc dans ChatGPT (une classe + une matière par conversation), puis enregistre la réponse JSON dans un fichier nommé comme indiqué (ex. `REV-MA-CM1.json`). Dépose les fichiers dans `docs/contenu/gpt/fiches_revision/reponses/` sur GitHub (ou envoie-les à Claude dans la conversation). Claude les passe à la moulinette (vérification indépendante : programme, exactitude, âge, quiz) puis les intègre (appli + PDF).

## Grande section (maternelle, 5-6 ans)
### Langage et premiers pas vers la lecture — fichier `REV-FR-GS.json`

```
Tu es un professeur expérimenté de Grande section (maternelle, 5-6 ans) et un auteur de manuels scolaires. Écris les FICHES DE RÉVISION de **Langage et premiers pas vers la lecture** pour la classe de **Grande section (maternelle, 5-6 ans)**, pour l'application éducative PocketSage (les fiches seront lues sur téléphone, lues à voix haute et imprimées).

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
### Nombres et formes — fichier `REV-MA-GS.json`

```
Tu es un professeur expérimenté de Grande section (maternelle, 5-6 ans) et un auteur de manuels scolaires. Écris les FICHES DE RÉVISION de **Nombres et formes** pour la classe de **Grande section (maternelle, 5-6 ans)**, pour l'application éducative PocketSage (les fiches seront lues sur téléphone, lues à voix haute et imprimées).

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
  "matiere": "Nombres et formes",
  "code": "MA",
  "fiches": [
    {
      "id": "REV-MA-GS-01",
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
### Explorer le monde (vivant, objets, temps, espace) — fichier `REV-QM-GS.json`

```
Tu es un professeur expérimenté de Grande section (maternelle, 5-6 ans) et un auteur de manuels scolaires. Écris les FICHES DE RÉVISION de **Explorer le monde (vivant, objets, temps, espace)** pour la classe de **Grande section (maternelle, 5-6 ans)**, pour l'application éducative PocketSage (les fiches seront lues sur téléphone, lues à voix haute et imprimées).

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
  "matiere": "Explorer le monde (vivant, objets, temps, espace)",
  "code": "QM",
  "fiches": [
    {
      "id": "REV-QM-GS-01",
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
### Anglais (éveil) — fichier `REV-AN-GS.json`

```
Tu es un professeur expérimenté de Grande section (maternelle, 5-6 ans) et un auteur de manuels scolaires. Écris les FICHES DE RÉVISION de **Anglais (éveil)** pour la classe de **Grande section (maternelle, 5-6 ans)**, pour l'application éducative PocketSage (les fiches seront lues sur téléphone, lues à voix haute et imprimées).

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
  "matiere": "Anglais (éveil)",
  "code": "AN",
  "fiches": [
    {
      "id": "REV-AN-GS-01",
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

## CP (6-7 ans)
### Français — fichier `REV-FR-CP.json`

```
Tu es un professeur expérimenté de CP (6-7 ans) et un auteur de manuels scolaires. Écris les FICHES DE RÉVISION de **Français** pour la classe de **CP (6-7 ans)**, pour l'application éducative PocketSage (les fiches seront lues sur téléphone, lues à voix haute et imprimées).

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
  "classe": "CP",
  "matiere": "Français",
  "code": "FR",
  "fiches": [
    {
      "id": "REV-FR-CP-01",
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
### Mathématiques — fichier `REV-MA-CP.json`

```
Tu es un professeur expérimenté de CP (6-7 ans) et un auteur de manuels scolaires. Écris les FICHES DE RÉVISION de **Mathématiques** pour la classe de **CP (6-7 ans)**, pour l'application éducative PocketSage (les fiches seront lues sur téléphone, lues à voix haute et imprimées).

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
  "classe": "CP",
  "matiere": "Mathématiques",
  "code": "MA",
  "fiches": [
    {
      "id": "REV-MA-CP-01",
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
### Questionner le monde — fichier `REV-QM-CP.json`

```
Tu es un professeur expérimenté de CP (6-7 ans) et un auteur de manuels scolaires. Écris les FICHES DE RÉVISION de **Questionner le monde** pour la classe de **CP (6-7 ans)**, pour l'application éducative PocketSage (les fiches seront lues sur téléphone, lues à voix haute et imprimées).

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
  "classe": "CP",
  "matiere": "Questionner le monde",
  "code": "QM",
  "fiches": [
    {
      "id": "REV-QM-CP-01",
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
### Anglais — fichier `REV-AN-CP.json`

```
Tu es un professeur expérimenté de CP (6-7 ans) et un auteur de manuels scolaires. Écris les FICHES DE RÉVISION de **Anglais** pour la classe de **CP (6-7 ans)**, pour l'application éducative PocketSage (les fiches seront lues sur téléphone, lues à voix haute et imprimées).

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
  "classe": "CP",
  "matiere": "Anglais",
  "code": "AN",
  "fiches": [
    {
      "id": "REV-AN-CP-01",
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

## CE1 (7-8 ans)
### Français — fichier `REV-FR-CE1.json`

```
Tu es un professeur expérimenté de CE1 (7-8 ans) et un auteur de manuels scolaires. Écris les FICHES DE RÉVISION de **Français** pour la classe de **CE1 (7-8 ans)**, pour l'application éducative PocketSage (les fiches seront lues sur téléphone, lues à voix haute et imprimées).

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
  "classe": "CE1",
  "matiere": "Français",
  "code": "FR",
  "fiches": [
    {
      "id": "REV-FR-CE1-01",
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
### Mathématiques — fichier `REV-MA-CE1.json`

```
Tu es un professeur expérimenté de CE1 (7-8 ans) et un auteur de manuels scolaires. Écris les FICHES DE RÉVISION de **Mathématiques** pour la classe de **CE1 (7-8 ans)**, pour l'application éducative PocketSage (les fiches seront lues sur téléphone, lues à voix haute et imprimées).

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
  "classe": "CE1",
  "matiere": "Mathématiques",
  "code": "MA",
  "fiches": [
    {
      "id": "REV-MA-CE1-01",
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
### Questionner le monde — fichier `REV-QM-CE1.json`

```
Tu es un professeur expérimenté de CE1 (7-8 ans) et un auteur de manuels scolaires. Écris les FICHES DE RÉVISION de **Questionner le monde** pour la classe de **CE1 (7-8 ans)**, pour l'application éducative PocketSage (les fiches seront lues sur téléphone, lues à voix haute et imprimées).

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
  "classe": "CE1",
  "matiere": "Questionner le monde",
  "code": "QM",
  "fiches": [
    {
      "id": "REV-QM-CE1-01",
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
### Anglais — fichier `REV-AN-CE1.json`

```
Tu es un professeur expérimenté de CE1 (7-8 ans) et un auteur de manuels scolaires. Écris les FICHES DE RÉVISION de **Anglais** pour la classe de **CE1 (7-8 ans)**, pour l'application éducative PocketSage (les fiches seront lues sur téléphone, lues à voix haute et imprimées).

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
  "classe": "CE1",
  "matiere": "Anglais",
  "code": "AN",
  "fiches": [
    {
      "id": "REV-AN-CE1-01",
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

## CE2 (8-9 ans)
### Français — fichier `REV-FR-CE2.json`

```
Tu es un professeur expérimenté de CE2 (8-9 ans) et un auteur de manuels scolaires. Écris les FICHES DE RÉVISION de **Français** pour la classe de **CE2 (8-9 ans)**, pour l'application éducative PocketSage (les fiches seront lues sur téléphone, lues à voix haute et imprimées).

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
  "classe": "CE2",
  "matiere": "Français",
  "code": "FR",
  "fiches": [
    {
      "id": "REV-FR-CE2-01",
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
### Mathématiques — fichier `REV-MA-CE2.json`

```
Tu es un professeur expérimenté de CE2 (8-9 ans) et un auteur de manuels scolaires. Écris les FICHES DE RÉVISION de **Mathématiques** pour la classe de **CE2 (8-9 ans)**, pour l'application éducative PocketSage (les fiches seront lues sur téléphone, lues à voix haute et imprimées).

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
  "classe": "CE2",
  "matiere": "Mathématiques",
  "code": "MA",
  "fiches": [
    {
      "id": "REV-MA-CE2-01",
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
### Questionner le monde — fichier `REV-QM-CE2.json`

```
Tu es un professeur expérimenté de CE2 (8-9 ans) et un auteur de manuels scolaires. Écris les FICHES DE RÉVISION de **Questionner le monde** pour la classe de **CE2 (8-9 ans)**, pour l'application éducative PocketSage (les fiches seront lues sur téléphone, lues à voix haute et imprimées).

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
  "classe": "CE2",
  "matiere": "Questionner le monde",
  "code": "QM",
  "fiches": [
    {
      "id": "REV-QM-CE2-01",
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
### Anglais — fichier `REV-AN-CE2.json`

```
Tu es un professeur expérimenté de CE2 (8-9 ans) et un auteur de manuels scolaires. Écris les FICHES DE RÉVISION de **Anglais** pour la classe de **CE2 (8-9 ans)**, pour l'application éducative PocketSage (les fiches seront lues sur téléphone, lues à voix haute et imprimées).

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
  "classe": "CE2",
  "matiere": "Anglais",
  "code": "AN",
  "fiches": [
    {
      "id": "REV-AN-CE2-01",
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

## CM1 (9-10 ans)
### Français — fichier `REV-FR-CM1.json`

```
Tu es un professeur expérimenté de CM1 (9-10 ans) et un auteur de manuels scolaires. Écris les FICHES DE RÉVISION de **Français** pour la classe de **CM1 (9-10 ans)**, pour l'application éducative PocketSage (les fiches seront lues sur téléphone, lues à voix haute et imprimées).

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
  "classe": "CM1",
  "matiere": "Français",
  "code": "FR",
  "fiches": [
    {
      "id": "REV-FR-CM1-01",
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
### Mathématiques — fichier `REV-MA-CM1.json`

```
Tu es un professeur expérimenté de CM1 (9-10 ans) et un auteur de manuels scolaires. Écris les FICHES DE RÉVISION de **Mathématiques** pour la classe de **CM1 (9-10 ans)**, pour l'application éducative PocketSage (les fiches seront lues sur téléphone, lues à voix haute et imprimées).

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
  "classe": "CM1",
  "matiere": "Mathématiques",
  "code": "MA",
  "fiches": [
    {
      "id": "REV-MA-CM1-01",
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
### Sciences et technologie — fichier `REV-SC-CM1.json`

```
Tu es un professeur expérimenté de CM1 (9-10 ans) et un auteur de manuels scolaires. Écris les FICHES DE RÉVISION de **Sciences et technologie** pour la classe de **CM1 (9-10 ans)**, pour l'application éducative PocketSage (les fiches seront lues sur téléphone, lues à voix haute et imprimées).

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
  "classe": "CM1",
  "matiere": "Sciences et technologie",
  "code": "SC",
  "fiches": [
    {
      "id": "REV-SC-CM1-01",
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
### Histoire — fichier `REV-HI-CM1.json`

```
Tu es un professeur expérimenté de CM1 (9-10 ans) et un auteur de manuels scolaires. Écris les FICHES DE RÉVISION de **Histoire** pour la classe de **CM1 (9-10 ans)**, pour l'application éducative PocketSage (les fiches seront lues sur téléphone, lues à voix haute et imprimées).

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
  "classe": "CM1",
  "matiere": "Histoire",
  "code": "HI",
  "fiches": [
    {
      "id": "REV-HI-CM1-01",
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
### Géographie — fichier `REV-GE-CM1.json`

```
Tu es un professeur expérimenté de CM1 (9-10 ans) et un auteur de manuels scolaires. Écris les FICHES DE RÉVISION de **Géographie** pour la classe de **CM1 (9-10 ans)**, pour l'application éducative PocketSage (les fiches seront lues sur téléphone, lues à voix haute et imprimées).

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
  "classe": "CM1",
  "matiere": "Géographie",
  "code": "GE",
  "fiches": [
    {
      "id": "REV-GE-CM1-01",
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
### Anglais — fichier `REV-AN-CM1.json`

```
Tu es un professeur expérimenté de CM1 (9-10 ans) et un auteur de manuels scolaires. Écris les FICHES DE RÉVISION de **Anglais** pour la classe de **CM1 (9-10 ans)**, pour l'application éducative PocketSage (les fiches seront lues sur téléphone, lues à voix haute et imprimées).

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
  "classe": "CM1",
  "matiere": "Anglais",
  "code": "AN",
  "fiches": [
    {
      "id": "REV-AN-CM1-01",
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

## CM2 (10-11 ans)
### Français — fichier `REV-FR-CM2.json`

```
Tu es un professeur expérimenté de CM2 (10-11 ans) et un auteur de manuels scolaires. Écris les FICHES DE RÉVISION de **Français** pour la classe de **CM2 (10-11 ans)**, pour l'application éducative PocketSage (les fiches seront lues sur téléphone, lues à voix haute et imprimées).

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
  "classe": "CM2",
  "matiere": "Français",
  "code": "FR",
  "fiches": [
    {
      "id": "REV-FR-CM2-01",
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
### Mathématiques — fichier `REV-MA-CM2.json`

```
Tu es un professeur expérimenté de CM2 (10-11 ans) et un auteur de manuels scolaires. Écris les FICHES DE RÉVISION de **Mathématiques** pour la classe de **CM2 (10-11 ans)**, pour l'application éducative PocketSage (les fiches seront lues sur téléphone, lues à voix haute et imprimées).

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
  "classe": "CM2",
  "matiere": "Mathématiques",
  "code": "MA",
  "fiches": [
    {
      "id": "REV-MA-CM2-01",
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
### Sciences et technologie — fichier `REV-SC-CM2.json`

```
Tu es un professeur expérimenté de CM2 (10-11 ans) et un auteur de manuels scolaires. Écris les FICHES DE RÉVISION de **Sciences et technologie** pour la classe de **CM2 (10-11 ans)**, pour l'application éducative PocketSage (les fiches seront lues sur téléphone, lues à voix haute et imprimées).

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
  "classe": "CM2",
  "matiere": "Sciences et technologie",
  "code": "SC",
  "fiches": [
    {
      "id": "REV-SC-CM2-01",
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
### Histoire — fichier `REV-HI-CM2.json`

```
Tu es un professeur expérimenté de CM2 (10-11 ans) et un auteur de manuels scolaires. Écris les FICHES DE RÉVISION de **Histoire** pour la classe de **CM2 (10-11 ans)**, pour l'application éducative PocketSage (les fiches seront lues sur téléphone, lues à voix haute et imprimées).

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
  "classe": "CM2",
  "matiere": "Histoire",
  "code": "HI",
  "fiches": [
    {
      "id": "REV-HI-CM2-01",
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
### Géographie — fichier `REV-GE-CM2.json`

```
Tu es un professeur expérimenté de CM2 (10-11 ans) et un auteur de manuels scolaires. Écris les FICHES DE RÉVISION de **Géographie** pour la classe de **CM2 (10-11 ans)**, pour l'application éducative PocketSage (les fiches seront lues sur téléphone, lues à voix haute et imprimées).

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
  "classe": "CM2",
  "matiere": "Géographie",
  "code": "GE",
  "fiches": [
    {
      "id": "REV-GE-CM2-01",
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
### Anglais — fichier `REV-AN-CM2.json`

```
Tu es un professeur expérimenté de CM2 (10-11 ans) et un auteur de manuels scolaires. Écris les FICHES DE RÉVISION de **Anglais** pour la classe de **CM2 (10-11 ans)**, pour l'application éducative PocketSage (les fiches seront lues sur téléphone, lues à voix haute et imprimées).

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
  "classe": "CM2",
  "matiere": "Anglais",
  "code": "AN",
  "fiches": [
    {
      "id": "REV-AN-CM2-01",
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

## 6e (11-12 ans)
### Français — fichier `REV-FR-6E.json`

```
Tu es un professeur expérimenté de 6e (11-12 ans) et un auteur de manuels scolaires. Écris les FICHES DE RÉVISION de **Français** pour la classe de **6e (11-12 ans)**, pour l'application éducative PocketSage (les fiches seront lues sur téléphone, lues à voix haute et imprimées).

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
  "classe": "6E",
  "matiere": "Français",
  "code": "FR",
  "fiches": [
    {
      "id": "REV-FR-6E-01",
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
### Mathématiques — fichier `REV-MA-6E.json`

```
Tu es un professeur expérimenté de 6e (11-12 ans) et un auteur de manuels scolaires. Écris les FICHES DE RÉVISION de **Mathématiques** pour la classe de **6e (11-12 ans)**, pour l'application éducative PocketSage (les fiches seront lues sur téléphone, lues à voix haute et imprimées).

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
  "classe": "6E",
  "matiere": "Mathématiques",
  "code": "MA",
  "fiches": [
    {
      "id": "REV-MA-6E-01",
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
### Sciences et technologie — fichier `REV-SC-6E.json`

```
Tu es un professeur expérimenté de 6e (11-12 ans) et un auteur de manuels scolaires. Écris les FICHES DE RÉVISION de **Sciences et technologie** pour la classe de **6e (11-12 ans)**, pour l'application éducative PocketSage (les fiches seront lues sur téléphone, lues à voix haute et imprimées).

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
  "classe": "6E",
  "matiere": "Sciences et technologie",
  "code": "SC",
  "fiches": [
    {
      "id": "REV-SC-6E-01",
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
### Histoire — fichier `REV-HI-6E.json`

```
Tu es un professeur expérimenté de 6e (11-12 ans) et un auteur de manuels scolaires. Écris les FICHES DE RÉVISION de **Histoire** pour la classe de **6e (11-12 ans)**, pour l'application éducative PocketSage (les fiches seront lues sur téléphone, lues à voix haute et imprimées).

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
  "classe": "6E",
  "matiere": "Histoire",
  "code": "HI",
  "fiches": [
    {
      "id": "REV-HI-6E-01",
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
### Géographie — fichier `REV-GE-6E.json`

```
Tu es un professeur expérimenté de 6e (11-12 ans) et un auteur de manuels scolaires. Écris les FICHES DE RÉVISION de **Géographie** pour la classe de **6e (11-12 ans)**, pour l'application éducative PocketSage (les fiches seront lues sur téléphone, lues à voix haute et imprimées).

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
  "classe": "6E",
  "matiere": "Géographie",
  "code": "GE",
  "fiches": [
    {
      "id": "REV-GE-6E-01",
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
### Anglais — fichier `REV-AN-6E.json`

```
Tu es un professeur expérimenté de 6e (11-12 ans) et un auteur de manuels scolaires. Écris les FICHES DE RÉVISION de **Anglais** pour la classe de **6e (11-12 ans)**, pour l'application éducative PocketSage (les fiches seront lues sur téléphone, lues à voix haute et imprimées).

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
  "classe": "6E",
  "matiere": "Anglais",
  "code": "AN",
  "fiches": [
    {
      "id": "REV-AN-6E-01",
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

## 5e (12-13 ans)
### Français — fichier `REV-FR-5E.json`

```
Tu es un professeur expérimenté de 5e (12-13 ans) et un auteur de manuels scolaires. Écris les FICHES DE RÉVISION de **Français** pour la classe de **5e (12-13 ans)**, pour l'application éducative PocketSage (les fiches seront lues sur téléphone, lues à voix haute et imprimées).

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
  "classe": "5E",
  "matiere": "Français",
  "code": "FR",
  "fiches": [
    {
      "id": "REV-FR-5E-01",
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
### Mathématiques — fichier `REV-MA-5E.json`

```
Tu es un professeur expérimenté de 5e (12-13 ans) et un auteur de manuels scolaires. Écris les FICHES DE RÉVISION de **Mathématiques** pour la classe de **5e (12-13 ans)**, pour l'application éducative PocketSage (les fiches seront lues sur téléphone, lues à voix haute et imprimées).

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
  "classe": "5E",
  "matiere": "Mathématiques",
  "code": "MA",
  "fiches": [
    {
      "id": "REV-MA-5E-01",
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
### SVT — fichier `REV-SVT-5E.json`

```
Tu es un professeur expérimenté de 5e (12-13 ans) et un auteur de manuels scolaires. Écris les FICHES DE RÉVISION de **SVT** pour la classe de **5e (12-13 ans)**, pour l'application éducative PocketSage (les fiches seront lues sur téléphone, lues à voix haute et imprimées).

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
  "classe": "5E",
  "matiere": "SVT",
  "code": "SVT",
  "fiches": [
    {
      "id": "REV-SVT-5E-01",
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
### Physique-chimie — fichier `REV-PC-5E.json`

```
Tu es un professeur expérimenté de 5e (12-13 ans) et un auteur de manuels scolaires. Écris les FICHES DE RÉVISION de **Physique-chimie** pour la classe de **5e (12-13 ans)**, pour l'application éducative PocketSage (les fiches seront lues sur téléphone, lues à voix haute et imprimées).

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
  "classe": "5E",
  "matiere": "Physique-chimie",
  "code": "PC",
  "fiches": [
    {
      "id": "REV-PC-5E-01",
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
### Technologie — fichier `REV-TE-5E.json`

```
Tu es un professeur expérimenté de 5e (12-13 ans) et un auteur de manuels scolaires. Écris les FICHES DE RÉVISION de **Technologie** pour la classe de **5e (12-13 ans)**, pour l'application éducative PocketSage (les fiches seront lues sur téléphone, lues à voix haute et imprimées).

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
  "classe": "5E",
  "matiere": "Technologie",
  "code": "TE",
  "fiches": [
    {
      "id": "REV-TE-5E-01",
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
### Histoire — fichier `REV-HI-5E.json`

```
Tu es un professeur expérimenté de 5e (12-13 ans) et un auteur de manuels scolaires. Écris les FICHES DE RÉVISION de **Histoire** pour la classe de **5e (12-13 ans)**, pour l'application éducative PocketSage (les fiches seront lues sur téléphone, lues à voix haute et imprimées).

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
  "classe": "5E",
  "matiere": "Histoire",
  "code": "HI",
  "fiches": [
    {
      "id": "REV-HI-5E-01",
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
### Géographie — fichier `REV-GE-5E.json`

```
Tu es un professeur expérimenté de 5e (12-13 ans) et un auteur de manuels scolaires. Écris les FICHES DE RÉVISION de **Géographie** pour la classe de **5e (12-13 ans)**, pour l'application éducative PocketSage (les fiches seront lues sur téléphone, lues à voix haute et imprimées).

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
  "classe": "5E",
  "matiere": "Géographie",
  "code": "GE",
  "fiches": [
    {
      "id": "REV-GE-5E-01",
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
### Anglais — fichier `REV-AN-5E.json`

```
Tu es un professeur expérimenté de 5e (12-13 ans) et un auteur de manuels scolaires. Écris les FICHES DE RÉVISION de **Anglais** pour la classe de **5e (12-13 ans)**, pour l'application éducative PocketSage (les fiches seront lues sur téléphone, lues à voix haute et imprimées).

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
  "classe": "5E",
  "matiere": "Anglais",
  "code": "AN",
  "fiches": [
    {
      "id": "REV-AN-5E-01",
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
### Espagnol (LV2, débutant) — fichier `REV-ES-5E.json`

```
Tu es un professeur expérimenté de 5e (12-13 ans) et un auteur de manuels scolaires. Écris les FICHES DE RÉVISION de **Espagnol (LV2, débutant)** pour la classe de **5e (12-13 ans)**, pour l'application éducative PocketSage (les fiches seront lues sur téléphone, lues à voix haute et imprimées).

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
  "classe": "5E",
  "matiere": "Espagnol (LV2, débutant)",
  "code": "ES",
  "fiches": [
    {
      "id": "REV-ES-5E-01",
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

## 4e (13-14 ans)
### Français — fichier `REV-FR-4E.json`

```
Tu es un professeur expérimenté de 4e (13-14 ans) et un auteur de manuels scolaires. Écris les FICHES DE RÉVISION de **Français** pour la classe de **4e (13-14 ans)**, pour l'application éducative PocketSage (les fiches seront lues sur téléphone, lues à voix haute et imprimées).

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
  "classe": "4E",
  "matiere": "Français",
  "code": "FR",
  "fiches": [
    {
      "id": "REV-FR-4E-01",
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
### Mathématiques — fichier `REV-MA-4E.json`

```
Tu es un professeur expérimenté de 4e (13-14 ans) et un auteur de manuels scolaires. Écris les FICHES DE RÉVISION de **Mathématiques** pour la classe de **4e (13-14 ans)**, pour l'application éducative PocketSage (les fiches seront lues sur téléphone, lues à voix haute et imprimées).

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
  "classe": "4E",
  "matiere": "Mathématiques",
  "code": "MA",
  "fiches": [
    {
      "id": "REV-MA-4E-01",
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
### SVT — fichier `REV-SVT-4E.json`

```
Tu es un professeur expérimenté de 4e (13-14 ans) et un auteur de manuels scolaires. Écris les FICHES DE RÉVISION de **SVT** pour la classe de **4e (13-14 ans)**, pour l'application éducative PocketSage (les fiches seront lues sur téléphone, lues à voix haute et imprimées).

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
  "classe": "4E",
  "matiere": "SVT",
  "code": "SVT",
  "fiches": [
    {
      "id": "REV-SVT-4E-01",
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
### Physique-chimie — fichier `REV-PC-4E.json`

```
Tu es un professeur expérimenté de 4e (13-14 ans) et un auteur de manuels scolaires. Écris les FICHES DE RÉVISION de **Physique-chimie** pour la classe de **4e (13-14 ans)**, pour l'application éducative PocketSage (les fiches seront lues sur téléphone, lues à voix haute et imprimées).

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
  "classe": "4E",
  "matiere": "Physique-chimie",
  "code": "PC",
  "fiches": [
    {
      "id": "REV-PC-4E-01",
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
### Technologie — fichier `REV-TE-4E.json`

```
Tu es un professeur expérimenté de 4e (13-14 ans) et un auteur de manuels scolaires. Écris les FICHES DE RÉVISION de **Technologie** pour la classe de **4e (13-14 ans)**, pour l'application éducative PocketSage (les fiches seront lues sur téléphone, lues à voix haute et imprimées).

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
  "classe": "4E",
  "matiere": "Technologie",
  "code": "TE",
  "fiches": [
    {
      "id": "REV-TE-4E-01",
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
### Histoire — fichier `REV-HI-4E.json`

```
Tu es un professeur expérimenté de 4e (13-14 ans) et un auteur de manuels scolaires. Écris les FICHES DE RÉVISION de **Histoire** pour la classe de **4e (13-14 ans)**, pour l'application éducative PocketSage (les fiches seront lues sur téléphone, lues à voix haute et imprimées).

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
  "classe": "4E",
  "matiere": "Histoire",
  "code": "HI",
  "fiches": [
    {
      "id": "REV-HI-4E-01",
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
### Géographie — fichier `REV-GE-4E.json`

```
Tu es un professeur expérimenté de 4e (13-14 ans) et un auteur de manuels scolaires. Écris les FICHES DE RÉVISION de **Géographie** pour la classe de **4e (13-14 ans)**, pour l'application éducative PocketSage (les fiches seront lues sur téléphone, lues à voix haute et imprimées).

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
  "classe": "4E",
  "matiere": "Géographie",
  "code": "GE",
  "fiches": [
    {
      "id": "REV-GE-4E-01",
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
### Anglais — fichier `REV-AN-4E.json`

```
Tu es un professeur expérimenté de 4e (13-14 ans) et un auteur de manuels scolaires. Écris les FICHES DE RÉVISION de **Anglais** pour la classe de **4e (13-14 ans)**, pour l'application éducative PocketSage (les fiches seront lues sur téléphone, lues à voix haute et imprimées).

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
  "classe": "4E",
  "matiere": "Anglais",
  "code": "AN",
  "fiches": [
    {
      "id": "REV-AN-4E-01",
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
### Espagnol (LV2) — fichier `REV-ES-4E.json`

```
Tu es un professeur expérimenté de 4e (13-14 ans) et un auteur de manuels scolaires. Écris les FICHES DE RÉVISION de **Espagnol (LV2)** pour la classe de **4e (13-14 ans)**, pour l'application éducative PocketSage (les fiches seront lues sur téléphone, lues à voix haute et imprimées).

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
  "classe": "4E",
  "matiere": "Espagnol (LV2)",
  "code": "ES",
  "fiches": [
    {
      "id": "REV-ES-4E-01",
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

## 3e (14-15 ans, brevet)
### Français — fichier `REV-FR-3E.json`

```
Tu es un professeur expérimenté de 3e (14-15 ans, brevet) et un auteur de manuels scolaires. Écris les FICHES DE RÉVISION de **Français** pour la classe de **3e (14-15 ans, brevet)**, pour l'application éducative PocketSage (les fiches seront lues sur téléphone, lues à voix haute et imprimées).

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
  "classe": "3E",
  "matiere": "Français",
  "code": "FR",
  "fiches": [
    {
      "id": "REV-FR-3E-01",
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
### Mathématiques — fichier `REV-MA-3E.json`

```
Tu es un professeur expérimenté de 3e (14-15 ans, brevet) et un auteur de manuels scolaires. Écris les FICHES DE RÉVISION de **Mathématiques** pour la classe de **3e (14-15 ans, brevet)**, pour l'application éducative PocketSage (les fiches seront lues sur téléphone, lues à voix haute et imprimées).

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
  "classe": "3E",
  "matiere": "Mathématiques",
  "code": "MA",
  "fiches": [
    {
      "id": "REV-MA-3E-01",
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
### SVT — fichier `REV-SVT-3E.json`

```
Tu es un professeur expérimenté de 3e (14-15 ans, brevet) et un auteur de manuels scolaires. Écris les FICHES DE RÉVISION de **SVT** pour la classe de **3e (14-15 ans, brevet)**, pour l'application éducative PocketSage (les fiches seront lues sur téléphone, lues à voix haute et imprimées).

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
  "classe": "3E",
  "matiere": "SVT",
  "code": "SVT",
  "fiches": [
    {
      "id": "REV-SVT-3E-01",
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
### Physique-chimie — fichier `REV-PC-3E.json`

```
Tu es un professeur expérimenté de 3e (14-15 ans, brevet) et un auteur de manuels scolaires. Écris les FICHES DE RÉVISION de **Physique-chimie** pour la classe de **3e (14-15 ans, brevet)**, pour l'application éducative PocketSage (les fiches seront lues sur téléphone, lues à voix haute et imprimées).

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
  "classe": "3E",
  "matiere": "Physique-chimie",
  "code": "PC",
  "fiches": [
    {
      "id": "REV-PC-3E-01",
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
### Technologie — fichier `REV-TE-3E.json`

```
Tu es un professeur expérimenté de 3e (14-15 ans, brevet) et un auteur de manuels scolaires. Écris les FICHES DE RÉVISION de **Technologie** pour la classe de **3e (14-15 ans, brevet)**, pour l'application éducative PocketSage (les fiches seront lues sur téléphone, lues à voix haute et imprimées).

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
  "classe": "3E",
  "matiere": "Technologie",
  "code": "TE",
  "fiches": [
    {
      "id": "REV-TE-3E-01",
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
### Histoire — fichier `REV-HI-3E.json`

```
Tu es un professeur expérimenté de 3e (14-15 ans, brevet) et un auteur de manuels scolaires. Écris les FICHES DE RÉVISION de **Histoire** pour la classe de **3e (14-15 ans, brevet)**, pour l'application éducative PocketSage (les fiches seront lues sur téléphone, lues à voix haute et imprimées).

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
  "classe": "3E",
  "matiere": "Histoire",
  "code": "HI",
  "fiches": [
    {
      "id": "REV-HI-3E-01",
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
### Géographie — fichier `REV-GE-3E.json`

```
Tu es un professeur expérimenté de 3e (14-15 ans, brevet) et un auteur de manuels scolaires. Écris les FICHES DE RÉVISION de **Géographie** pour la classe de **3e (14-15 ans, brevet)**, pour l'application éducative PocketSage (les fiches seront lues sur téléphone, lues à voix haute et imprimées).

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
  "classe": "3E",
  "matiere": "Géographie",
  "code": "GE",
  "fiches": [
    {
      "id": "REV-GE-3E-01",
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
### Anglais — fichier `REV-AN-3E.json`

```
Tu es un professeur expérimenté de 3e (14-15 ans, brevet) et un auteur de manuels scolaires. Écris les FICHES DE RÉVISION de **Anglais** pour la classe de **3e (14-15 ans, brevet)**, pour l'application éducative PocketSage (les fiches seront lues sur téléphone, lues à voix haute et imprimées).

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
  "classe": "3E",
  "matiere": "Anglais",
  "code": "AN",
  "fiches": [
    {
      "id": "REV-AN-3E-01",
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
### Espagnol (LV2) — fichier `REV-ES-3E.json`

```
Tu es un professeur expérimenté de 3e (14-15 ans, brevet) et un auteur de manuels scolaires. Écris les FICHES DE RÉVISION de **Espagnol (LV2)** pour la classe de **3e (14-15 ans, brevet)**, pour l'application éducative PocketSage (les fiches seront lues sur téléphone, lues à voix haute et imprimées).

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
  "classe": "3E",
  "matiere": "Espagnol (LV2)",
  "code": "ES",
  "fiches": [
    {
      "id": "REV-ES-3E-01",
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

## Seconde générale (15-16 ans)
### Français — fichier `REV-FR-LY.json`

```
Tu es un professeur expérimenté de Seconde générale (15-16 ans) et un auteur de manuels scolaires. Écris les FICHES DE RÉVISION de **Français** pour la classe de **Seconde générale (15-16 ans)**, pour l'application éducative PocketSage (les fiches seront lues sur téléphone, lues à voix haute et imprimées).

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
  "classe": "LY",
  "matiere": "Français",
  "code": "FR",
  "fiches": [
    {
      "id": "REV-FR-LY-01",
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
### Mathématiques — fichier `REV-MA-LY.json`

```
Tu es un professeur expérimenté de Seconde générale (15-16 ans) et un auteur de manuels scolaires. Écris les FICHES DE RÉVISION de **Mathématiques** pour la classe de **Seconde générale (15-16 ans)**, pour l'application éducative PocketSage (les fiches seront lues sur téléphone, lues à voix haute et imprimées).

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
  "classe": "LY",
  "matiere": "Mathématiques",
  "code": "MA",
  "fiches": [
    {
      "id": "REV-MA-LY-01",
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
### SVT — fichier `REV-SVT-LY.json`

```
Tu es un professeur expérimenté de Seconde générale (15-16 ans) et un auteur de manuels scolaires. Écris les FICHES DE RÉVISION de **SVT** pour la classe de **Seconde générale (15-16 ans)**, pour l'application éducative PocketSage (les fiches seront lues sur téléphone, lues à voix haute et imprimées).

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
  "classe": "LY",
  "matiere": "SVT",
  "code": "SVT",
  "fiches": [
    {
      "id": "REV-SVT-LY-01",
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
### Physique-chimie — fichier `REV-PC-LY.json`

```
Tu es un professeur expérimenté de Seconde générale (15-16 ans) et un auteur de manuels scolaires. Écris les FICHES DE RÉVISION de **Physique-chimie** pour la classe de **Seconde générale (15-16 ans)**, pour l'application éducative PocketSage (les fiches seront lues sur téléphone, lues à voix haute et imprimées).

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
  "classe": "LY",
  "matiere": "Physique-chimie",
  "code": "PC",
  "fiches": [
    {
      "id": "REV-PC-LY-01",
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
### Histoire — fichier `REV-HI-LY.json`

```
Tu es un professeur expérimenté de Seconde générale (15-16 ans) et un auteur de manuels scolaires. Écris les FICHES DE RÉVISION de **Histoire** pour la classe de **Seconde générale (15-16 ans)**, pour l'application éducative PocketSage (les fiches seront lues sur téléphone, lues à voix haute et imprimées).

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
  "classe": "LY",
  "matiere": "Histoire",
  "code": "HI",
  "fiches": [
    {
      "id": "REV-HI-LY-01",
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
### Géographie — fichier `REV-GE-LY.json`

```
Tu es un professeur expérimenté de Seconde générale (15-16 ans) et un auteur de manuels scolaires. Écris les FICHES DE RÉVISION de **Géographie** pour la classe de **Seconde générale (15-16 ans)**, pour l'application éducative PocketSage (les fiches seront lues sur téléphone, lues à voix haute et imprimées).

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
  "classe": "LY",
  "matiere": "Géographie",
  "code": "GE",
  "fiches": [
    {
      "id": "REV-GE-LY-01",
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
### SES — fichier `REV-SES-LY.json`

```
Tu es un professeur expérimenté de Seconde générale (15-16 ans) et un auteur de manuels scolaires. Écris les FICHES DE RÉVISION de **SES** pour la classe de **Seconde générale (15-16 ans)**, pour l'application éducative PocketSage (les fiches seront lues sur téléphone, lues à voix haute et imprimées).

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
  "classe": "LY",
  "matiere": "SES",
  "code": "SES",
  "fiches": [
    {
      "id": "REV-SES-LY-01",
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
### Anglais — fichier `REV-AN-LY.json`

```
Tu es un professeur expérimenté de Seconde générale (15-16 ans) et un auteur de manuels scolaires. Écris les FICHES DE RÉVISION de **Anglais** pour la classe de **Seconde générale (15-16 ans)**, pour l'application éducative PocketSage (les fiches seront lues sur téléphone, lues à voix haute et imprimées).

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
  "classe": "LY",
  "matiere": "Anglais",
  "code": "AN",
  "fiches": [
    {
      "id": "REV-AN-LY-01",
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
### Espagnol (LV2) — fichier `REV-ES-LY.json`

```
Tu es un professeur expérimenté de Seconde générale (15-16 ans) et un auteur de manuels scolaires. Écris les FICHES DE RÉVISION de **Espagnol (LV2)** pour la classe de **Seconde générale (15-16 ans)**, pour l'application éducative PocketSage (les fiches seront lues sur téléphone, lues à voix haute et imprimées).

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
  "classe": "LY",
  "matiere": "Espagnol (LV2)",
  "code": "ES",
  "fiches": [
    {
      "id": "REV-ES-LY-01",
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
