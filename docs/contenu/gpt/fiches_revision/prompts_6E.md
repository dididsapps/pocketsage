# Prompts fiches de révision — 6e (11-12 ans)

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
