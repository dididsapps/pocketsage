"""Génère les prompts ChatGPT/Codex des fiches de révision (docs/contenu/gpt/fiches_revision/)."""
from pathlib import Path
D=Path(__file__).resolve().parent.parent/'docs/contenu/gpt/fiches_revision'
# code fichier, nom, classe dans l'appli, âge
CLASSES=[('GS','Grande section (maternelle)','GS','5-6'),('CP','CP','CP','6-7'),('CE1','CE1','CE1','7-8'),('CE2','CE2','CE2','8-9'),
 ('CM1','CM1','CM1','9-10'),('CM2','CM2','CM2','10-11'),('6E','6e','6ème','11-12'),('5E','5e','5ème','12-13'),('4E','4e','4ème','13-14'),
 ('3E','3e (brevet)','3ème','14-15'),('2DE','Seconde générale','Lycée','15-16'),('1RE','Première générale (bac de français, spécialités)','Lycée','16-17'),
 ('TLE','Terminale générale (baccalauréat)','Lycée','17-18')]
C={'Français':'FR','Mathématiques':'MA','Questionner le monde':'QM','Sciences et technologie':'SC','SVT':'SVT','Physique-chimie':'PC',
 'Technologie':'TE','Histoire':'HI','Géographie':'GE','SES':'SES','Anglais':'AN','Espagnol LV2':'ES','Enseignement scientifique':'ESC',
 'Philosophie':'PHI','HGGSP (spécialité)':'HGG','Mathématiques (spécialité)':'MA','Physique-chimie (spécialité)':'PC','SVT (spécialité)':'SVT','SES (spécialité)':'SES',
 'Langage et premiers pas vers la lecture':'FR','Nombres et formes':'MA','Explorer le monde':'QM','Anglais (éveil)':'AN'}
B=['Français','Mathématiques','Questionner le monde','Anglais']; M=['Français','Mathématiques','Sciences et technologie','Histoire','Géographie','Anglais']
K=['Français','Mathématiques','SVT','Physique-chimie','Technologie','Histoire','Géographie','Anglais','Espagnol LV2']
SPE=['Mathématiques (spécialité)','Physique-chimie (spécialité)','SVT (spécialité)','SES (spécialité)','HGGSP (spécialité)']
MAT={'GS':['Langage et premiers pas vers la lecture','Nombres et formes','Explorer le monde','Anglais (éveil)'],'CP':B,'CE1':B,'CE2':B,'CM1':M,'CM2':M,'6E':M,
 '5E':K,'4E':K,'3E':K,'2DE':['Français','Mathématiques','SVT','Physique-chimie','Histoire','Géographie','SES','Anglais','Espagnol LV2'],
 '1RE':['Français','Histoire','Géographie','Enseignement scientifique','Anglais','Espagnol LV2']+SPE,
 'TLE':['Philosophie','Histoire','Géographie','Enseignement scientifique','Anglais','Espagnol LV2']+SPE}
NOMMAGE="""NOMMAGE (obligatoire, pour que chaque fiche soit retrouvée automatiquement)
- Fichier : REV-<code matière>-<code classe>.json (ex. REV-MA-CM1.json, REV-HGG-TLE.json).
- Fiche : "id" = REV-<code matière>-<code classe>-NN, NN = 01, 02… dans l'ordre du programme.
- "axe" = le nom EXACT du grand axe (thème, chapitre ou partie) tel qu'écrit dans le programme officiel ;
  toutes les fiches d'un même axe portent exactement le même texte d'axe."""
PEDAGO="""PÉDAGOGIE (la fiche doit faire COMPRENDRE, pas seulement réviser) — appuie-toi sur les techniques d'apprentissage dont l'efficacité est la mieux établie par la recherche :
- Expliquer le pourquoi et le comment (élaboration) : chaque fiche dit pourquoi la règle marche ou d'où vient la notion, avec une comparaison ou une image tirée de la vie de l'élève.
- Partir de ce que l'élève sait déjà et faire le lien avec la notion nouvelle.
- Exemple résolu pas à pas (exemple travaillé) avant de laisser l'élève essayer.
- Peu d'informations à la fois (charge mentale) : une seule idée par phrase, l'essentiel d'abord.
- Mots + image mentale (double codage) : décrire un schéma ou une image simple qui aide à retenir.
- Se tester plutôt que relire (récupération active) : le quiz vient APRÈS, sans regarder la fiche ; une question au moins doit faire réfléchir, pas seulement reconnaître.
- Mélanger (pratique entrelacée) : une question du quiz peut reprendre une fiche précédente du même axe.
- Le piège : nommer l'idée fausse la plus courante et montrer pourquoi elle est fausse.
- Ton encourageant, jamais culpabilisant ; aucune promesse de résultat."""
REGLES="""RÈGLES (toutes obligatoires)
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
Vérifie toi-même avant de répondre : JSON valide, 3 questions par fiche, "rep" présent dans "choix"."""
def liste():
    out=[]
    for cl,nom,app,age in CLASSES:
        out.append(f"- {cl} = {nom}, {age} ans, classe appli « {app} » : "+' ; '.join(f"{m} → {C[m]}" for m in MAT[cl]))
    return '\n'.join(out)
LOTS=[('1',['GS','CP','CE1','CE2'],'Très élevé'),('2',['CM1','CM2','6E','5E'],'Très élevé (Ultra si le quota le permet)'),
 ('3',['4E','3E','2DE','1RE'],'Ultra'),('4',['TLE'],'Ultra')]
def lot(num,cls,reglage):
    L=[x for x in CLASSES if x[0] in cls]; n=sum(len(MAT[c[0]]) for c in L)
    lst='\n'.join(f"- {cl} = {nom}, {age} ans, classe appli « {app} » : "+' ; '.join(f"{m} → {C[m]}" for m in MAT[cl]) for cl,nom,app,age in L)
    noms=', '.join(c[1] for c in L)
    return f"""# Lot {num} — fiches de révision : {noms} ({n} matières)

Où : **ChatGPT Work**, modèle **GPT-6.1** (Sol si disponible, sinon Terra), réflexion **{reglage}**.
Colle le bloc tel quel. À la fin : dépose les JSON dans `docs/contenu/gpt/fiches_revision/reponses/` (ou envoie-les à Claude).
Si le quota coupe : nouvelle tâche, même bloc, en ajoutant à la fin « commence à : REV-XX-YY.json ».

```
MODE AUTONOME : ne m'attends pas entre les matières. Fais-les une par une, en prenant ton temps et en vérifiant
chacune. Enregistre chaque JSON dans un fichier à son nom. Si tu dois t'arrêter, dis seulement « je continue ? »
et reprends où tu en étais. À la fin, vérifie que les {n} fichiers sont valides et donne-moi UN fichier
fiches_revision_lot{num}.zip à télécharger.

Tu es un professeur expérimenté et un auteur de manuels scolaires. Tu écris les FICHES DE RÉVISION de
l'application éducative PocketSage (lues sur téléphone, écoutées, imprimées) pour les classes et matières
ci-dessous UNIQUEMENT, une matière à la fois, dans l'ordre de la liste.

LISTE (code classe = classe, âge, classe dans l'appli : matière → code matière)
{lst}

{NOMMAGE}

{PEDAGO}

{REGLES}
```
"""
def main():
    for num,cls,rg in LOTS: (D/f'LOT_{num}.md').write_text(lot(num,cls,rg),encoding='utf-8')
    n=0; tout=["# Prompts fiches de révision — un par classe × matière (GS → Terminale)\n\nPlus simple : PROMPT_UNIQUE.md.\n"]
    for cl,nom,app,age in CLASSES:
        part=[f"\n## {nom} ({age} ans)\n"]
        for m in MAT[cl]:
            n+=1; c=C[m]
            p=(f"Tu es un professeur expérimenté de {nom} et un auteur de manuels. Écris les FICHES DE RÉVISION de **{m}** pour la classe de **{nom}** ({age} ans), "
               f"pour l'application éducative PocketSage (lues sur téléphone, à voix haute, imprimées).\n"
               f"Valeurs à mettre : classe = {cl}, niveau_appli = {app}, age = {age}, matiere = {m}, code = {c}.\n\n{NOMMAGE}\n\n{PEDAGO}\n\n{REGLES}")
            part.append(f"### {m} — fichier `REV-{c}-{cl}.json`\n\n```\n{p}\n```\n")
        (D/f'prompts_{cl}.md').write_text(f"# Prompts fiches de révision — {nom}\n"+''.join(part),encoding='utf-8'); tout+=part
    (D/'PROMPTS_TOUS.md').write_text(''.join(tout),encoding='utf-8')
    u=f"""# Prompt UNIQUE — fiches de révision (GS → Terminale, {n} matières)

Colle le bloc UNE fois dans ChatGPT ou, mieux, dans **Codex** (onglet Code, dépôt pocketsage).
Tous les textes sont en français : Claude les vérifie (moulinette) puis les traduit dans les 9 autres langues de l'appli.

## Variante « fais tout seul, je télécharge à la fin »
Laisse le paragraphe MODE AUTONOME en tête du bloc. Pour le mode pas à pas (une matière par réponse, tu tapes « suite »), supprime-le.

```
MODE AUTONOME : ne m'attends pas entre les matières. Fais-les une par une en prenant ton temps et en vérifiant
chacune. Enregistre chaque JSON dans un fichier sous son nom. Si tu dois t'arrêter, dis seulement « je continue ? »
et reprends où tu en étais. À la fin, vérifie que les {n} fichiers sont valides et donne-moi UN fichier
fiches_revision.zip à télécharger. (Codex : écris les fichiers dans docs/contenu/gpt/fiches_revision/reponses/
et ouvre une pull request.)

Tu es un professeur expérimenté et un auteur de manuels scolaires. Tu écris les FICHES DE RÉVISION de
l'application éducative PocketSage (lues sur téléphone, à voix haute, imprimées), pour CHAQUE classe et
CHAQUE matière de la liste, de la Grande section au baccalauréat, UNE matière à la fois.

LISTE (code classe = classe, âge, classe dans l'appli : matière → code matière)
{liste()}

DÉROULEMENT
- Commence par GS / FR et suis la liste dans l'ordre.
- Sans le mode autonome : chaque réponse = une classe + une matière ; première ligne = le nom du fichier,
  puis le JSON seul. Quand j'écris « suite », passe à la suivante. À la fin, écris « TERMINÉ ».
- Si je t'écris « commence à : REV-XX-YY.json », reprends à cet endroit.

{NOMMAGE}

{PEDAGO}

{REGLES}
```
"""
    (D/'PROMPT_UNIQUE.md').write_text(u,encoding='utf-8'); print(n,'matières')
main()
