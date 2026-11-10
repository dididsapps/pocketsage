# 02 — Sources de contenu pour les cartes Flash

> Objectif : passer de **151 cartes** à **1000+** sans copier le contenu protégé de qui que ce soit, en restant utilisable dans une **appli payante**.
> Recherche faite le 10/11/2026. **Ce document n'est pas un avis juridique** : en cas de doute sur une source, demander à un juriste ou écrire à l'ayant droit.

Catégories Flash actuelles (d'après `index.html`) :

| Code | Clé `FLASH_DATA` | Onglet app | Âges réels | Nb actuel |
|---|---|---|---|---|
| PT | petits | Curiosités | 4-6 | 12 |
| EJ | emotionsJeune | Émotions | 4-6 | 12 |
| MJ | motivationJeune | Motivation | 5-7 | 12 |
| CU | curiosites | Curiosités | 6-10 | 15 |
| EN | enfants | Curiosités | 8-9 | 10 |
| SA | sagesse | Sagesse | 6-13 | 22 |
| MO | motivation | Motivation | 10-13 | 20 |
| CF | confiance | Confiance | 10-13 | 10 |
| EM | emotions | Émotions | 9-13 | 18 |
| PS | psycho | Psycho | 8-13 | 10 |
| AD | ados | Curiosités | 13-14 | 10 |

Note : `EN` = enfants et `AD` = ados dans l'app (pas « Nature » ni « Adultes »). Les exemples de cartes « nature/espace » ci-dessous vont dans `EN` (curiosités 8+), ceux sur les biais dans `AD` (ados) ; leur version adulte pourra alimenter une future catégorie adultes.

---|---|---|---|
| PT | Petits curieux (animaux, monde) | 4+ | 12 |
| EJ | Émotions jeunes | 5-9 | 12 |
| MJ | Mindset jeunes | 6-10 | 12 |
| CU | Curiosités / sciences fun | 7+ | 15 |
| EN | Nature, Terre, espace | 8+ | 10 |
| SA | Sagesse (citations d'auteurs) | 10+ | 22 |
| MO | Motivation, habitudes | 10+ | 20 |
| CF | Confiance en soi | 12+ | 10 |
| EM | Émotions ados/adultes | 10+ | 18 |
| PS | Psychologie / cerveau | 8+ | 10 |
| AD | Adultes (biais, comportement) | 14+ | 10 |

---

## 1. Règles juridiques simples

**Une idée ou un fait est libre ; un texte ne l'est pas.** En droit français, « les idées sont de libre parcours » : seule la *forme originale* est protégée (ex. CA Paris, 16/10/2013, RG 12/06709). Dire que « Vénus tourne plus lentement sur elle-même qu'autour du Soleil » est libre. Recopier ou paraphraser de près le paragraphe d'un livre ou d'un site ne l'est pas.

**Méthode sûre pour chaque carte :**
1. On part d'un **fait ou d'un résultat d'étude**, vérifié dans au moins une source fiable.
2. On écrit le texte **soi-même**, sans avoir le texte source sous les yeux (ou on le fait générer par Claude à partir du fait seul, pas d'un texte collé).
3. On **cite la source** dans le champ `source` (crédibilité, et obligation si la licence est CC BY).
4. Les citations d'auteurs : uniquement des auteurs **morts depuis plus de 70 ans**, et **traduites par nous** depuis la langue originale (ou via une traduction dont le traducteur est lui aussi mort depuis plus de 70 ans). Une traduction moderne de Marc Aurèle ou de Sénèque est protégée même si l'œuvre originale ne l'est pas.

**Les licences en une ligne :**

| Licence | Usage commercial | Ce qu'on doit faire |
|---|---|---|
| Domaine public / CC0 | Oui | Rien (citer quand même, c'est plus pro) |
| CC BY | Oui | Créditer l'auteur + lien vers la licence |
| Licence Ouverte Etalab 2.0 | Oui | Citer l'administration source + date de mise à jour ; compatible CC BY |
| CC BY-SA | Oui | Créditer + **le texte adapté doit être republié sous CC BY-SA** (donc copiable par un concurrent) |
| CC BY-NC / BY-NC-SA | **Non** | Inutilisable dans une appli payante |
| Tous droits réservés | Non | Seulement citer le fait, jamais reprendre le texte |

**Interdit / à éviter :**
- Les résumés de livres récents (*Atomic Habits*, *Mindset*, etc.) : on peut citer l'idée et l'auteur, pas reprendre leurs formules. ⚠️ La carte actuelle **MO-001** (« Chaque petit choix vote pour qui tu deviens ») reprend presque mot pour mot une formule de James Clear → à réécrire.
- Les cartes de Deepstash, Headway, Imprint, Blinkist, Nibble : contenu protégé, même reformulé de près.
- Les marques : « Pomodoro® » est une marque déposée de Francesco Cirillo → écrire « la méthode des 25 minutes (dite Pomodoro) », ne jamais en faire un nom de module.
- Le logo NASA, les photos d'astronautes en exercice, et toute formulation qui suggère un partenariat (NASA, ESA, Smithsonian, OMS…).

---

## 2. Tableau des sources

| Source | Licence | Commercial OK ? | Attribution | Catégories | Volume | URL / accès |
|---|---|---|---|---|---|---|
| **Wikidata** | CC0 | ✅ | Non requise | CU, EN, PT, SA (dates, chiffres, auteurs) | > 100 M éléments | wikidata.org, API SPARQL `query.wikidata.org` |
| **Wikipedia** (texte) | CC BY-SA 4.0 | ✅ mais ShareAlike | Oui + même licence si on adapte le texte | Toutes, pour **vérifier** les faits | Des millions d'articles, toutes langues | API REST Wikimedia |
| **Wikisource / Project Gutenberg** (textes du domaine public) | Domaine public | ✅ (vérifier la date de mort du traducteur) | Non (ne pas utiliser le nom « Project Gutenberg » commercialement) | SA | Des dizaines de milliers d'œuvres | fr.wikisource.org, gutenberg.org |
| **Smithsonian Open Access** | CC0 | ✅ | Non requise | CU, EN, PT (images + fiches objets) | ≥ 2,8 M images (2020), en croissance | si.edu/openaccess (téléchargement en masse) |
| **NASA** (images, faits) | Pas de copyright aux USA en général | ✅ sans logo, sans suggérer d'endorsement | Créditer « NASA » | EN, CU | Énorme (images.nasa.gov, science.nasa.gov) | images-api.nasa.gov |
| **NOAA** (fiches animaux, océan) | Gouvernement US, domaine public en général | ✅ (vérifier les images de tiers) | Créditer « NOAA » | PT, EN, CU | Des milliers de fiches | fisheries.noaa.gov, oceanservice.noaa.gov |
| **ESA** | CC BY-SA 3.0 IGO **seulement quand c'est indiqué** | ✅ si indiqué | « ESA/… – CC BY-SA 3.0 IGO » + lien licence | EN, CU | Variable | esa.int/ESA_Multimedia |
| **Our World in Data** | CC BY 4.0 (graphiques, textes, données propres) | ✅ | « Our World in Data » + source primaire | EN, CU, AD (chiffres monde) | Des milliers de graphiques | ourworldindata.org (CSV par graphique) |
| **data.gouv.fr** (Etalab 2.0) | Licence Ouverte 2.0 | ✅ | Nom de l'administration + date | CU, EN (chiffres France) | Des dizaines de milliers de jeux | data.gouv.fr/api |
| **Europeana** | Métadonnées CC0 ; objets : licence au cas par cas | ✅ seulement objets CC0 / PDM / CC BY | Selon l'objet | SA, CU (art, histoire) | Des dizaines de millions d'objets | api.europeana.eu, filtre `reusability=open` |
| **Tatoeba** (phrases multilingues) | CC BY 2.0 FR (une partie en CC0) ; audio : licence par contributeur | ✅ | Oui pour CC BY | SA, PT (phrases simples traduites) | Des millions de phrases, 400+ langues | tatoeba.org/downloads |
| **Open Trivia DB** | CC BY-SA 4.0 | ✅ mais ShareAlike | Oui + même licence | CU (quiz de rappel) | Quelques milliers de questions, **anglais** | opentdb.com/api.php |
| Proverbes traditionnels (FR, EN, DE, ES, IT, PT, AR, ZH) | Domaine public (anonymes, anciens) | ✅ | — | SA, MJ, EJ | Illimité | **Attention** : les recueils et traductions modernes sont protégés → traduire nous-mêmes |
| Gallica (BnF) | Réutilisation commerciale **soumise à licence/redevance** (au moins historiquement) | ⚠️ | — | SA | — | Préférer Wikisource pour les mêmes textes |
| OpenStax | **CC BY-NC-SA** (vérifié : *Biology 2e*, *American Government*) | ❌ | — | — | — | Citer comme source de vérification uniquement |
| CK-12 | CC BY-NC 3.0 | ❌ | — | — | — | Idem |
| Khan Academy | CC BY-NC-SA | ❌ | — | — | — | Idem |
| OMS (WHO) | CC BY-NC-SA 3.0 IGO ; usage commercial sur autorisation | ❌ sans permission | — | — | — | Citer le fait, ne pas reprendre le texte |
| APA, INSERM, Santé publique France | Tous droits réservés / licence non claire | ❌ pour le texte | — | EM, PS, MJ | — | Citer le fait + lien, écrire notre propre texte |
| Numbers API | Aucune licence trouvée | ⚠️ à éviter | — | — | — | — |

**En pratique, 4 piliers suffisent :** Wikidata (faits bruts, CC0), NASA/NOAA (sciences et animaux, domaine public), Smithsonian Open Access (images CC0 pour illustrer), Wikisource (citations du domaine public). On complète avec **études scientifiques citées** (les résultats ne sont pas protégés, seul le texte de l'article l'est) pour PS, AD, EM, CF, MO, MJ, EJ.

---

## 3. Par catégorie : sources + exemples de cartes originales

Format proposé pour chaque carte :
**Titre** / **Idée** (2-3 phrases) / **Essaie aujourd'hui** / **Question de rappel** (posée 2-3 jours plus tard) / **Source**.

### PT — Petits curieux (4+)
Sources : NOAA Fisheries (fiches espèces), Smithsonian Open Access (photos CC0), Wikidata (taille, poids, durée de vie), NASA Kids Club (faits).

1. **Les loutres de mer se tiennent la main pour dormir**
   - *Version 4-6 ans* : Quand elles dorment sur l'eau, les loutres se tiennent par la patte. Comme ça, la vague ne les sépare pas. Parfois elles s'enroulent aussi dans des algues, comme dans une couverture !
   - *Version adulte* : Les loutres de mer dorment en surface, souvent regroupées en « radeaux » ; elles s'agrippent entre elles ou s'enroulent dans le varech pour ne pas dériver avec le courant.
   - Essaie aujourd'hui : Fais un câlin de « loutre » à quelqu'un de ta famille avant de dormir.
   - Rappel : Pourquoi les loutres se tiennent-elles la patte ? (pour ne pas partir avec l'eau / pour jouer / pour manger)
   - Source : NOAA Fisheries, fiche *Sea Otter*.
2. **L'étoile de mer n'a pas de cerveau**
   - Idée : Elle n'a ni cerveau ni sang ! Des nerfs dans chacun de ses bras l'aident à bouger, et elle respire avec de l'eau de mer.
   - Essaie aujourd'hui : Dessine une étoile de mer et compte ses bras (souvent 5).
   - Rappel : Qu'est-ce que l'étoile de mer n'a pas ? (un cerveau / des bras / une couleur)
   - Source : NOAA Ocean Service, *Are starfish fish?*
3. **Le cœur de la crevette est dans sa tête**
   - Idée : Chez la crevette, le cœur se trouve juste derrière les yeux, dans la partie qu'on appelle la tête. Son corps n'est pas rangé comme le nôtre !
   - Essaie aujourd'hui : Pose ta main sur ton cœur. Est-il dans ta tête ? Non, dans ta poitrine !
   - Rappel : Où est le cœur de la crevette ?
   - Source : Wikipedia *Shrimp* (anatomie) — fait vérifié, texte original.

### EJ — Émotions jeunes (4-6)
Sources : études sur l'étiquetage des émotions (Lieberman et al., 2007), respiration lente (littérature sur la cohérence cardiaque — texte original), proverbes traditionnels.

1. **Dire « je suis en colère » la rend plus petite**
   - *Version 6-9 ans* : Quand une grosse émotion arrive, dis son nom tout haut : « Je suis en colère », « J'ai peur ». Le simple fait de la nommer aide ton cerveau à se calmer.
   - *Version adulte* : Mettre un mot sur une émotion (« affect labeling ») réduit l'activité de l'amygdale mesurée en IRM et augmente celle du cortex préfrontal, qui régule.
   - Essaie aujourd'hui : Ce soir, dis à quelqu'un une émotion que tu as eue dans la journée.
   - Rappel : Que faire quand une grosse émotion arrive ? (lui donner un nom / la cacher / crier)
   - Source : Lieberman M. et al., *Psychological Science*, 2007.
2. **La respiration carrée**
   - Idée : Inspire en comptant jusqu'à 4, garde l'air 4, souffle 4, attends 4. Tu dessines un carré avec ton souffle et ton corps ralentit.
   - Essaie aujourd'hui : Fais 3 carrés avant de t'endormir.
   - Rappel : Combien de côtés a la respiration carrée ?
   - Source : technique de respiration rythmée d'usage courant (pas d'auteur protégé).
3. **La peur est un garde du corps**
   - Idée : La peur n'est pas méchante : elle sert à te protéger du danger. Parfois elle se trompe et sonne pour rien, comme une alarme trop sensible.
   - Essaie aujourd'hui : Pense à une peur et demande-toi : « Est-ce un vrai danger ou une fausse alarme ? »
   - Rappel : À quoi sert la peur ?
   - Source : principe de base de la psychologie des émotions (texte original).

### MJ — Motivation jeunes (5-7)
Sources : Dweck (idée de l'état d'esprit de croissance — citer, ne pas paraphraser), Roediger & Karpicke 2006 (se tester), recherches sur le sommeil et la mémoire, apprentissage par l'enseignement.

1. **Le mot magique : « pas encore »**
   - *Version 6-9 ans* : Au lieu de dire « je n'y arrive pas », dis « je n'y arrive **pas encore** ». Ce petit mot rappelle à ton cerveau qu'il est en train d'apprendre.
   - *Version adulte* : Les travaux de Carol Dweck sur l'état d'esprit de croissance suggèrent que considérer ses capacités comme développables favorise la persévérance ; les effets mesurés dans les grandes études restent modestes mais réels chez les élèves en difficulté.
   - Essaie aujourd'hui : Repère une phrase « je n'y arrive pas » et ajoute « pas encore ».
   - Rappel : Quel petit mot transforme « je n'y arrive pas » ?
   - Source : Dweck C., travaux sur le *growth mindset* ; Yeager et al., *Nature*, 2019.
2. **Ton cerveau range tes leçons pendant que tu dors**
   - Idée : La nuit, ton cerveau trie ce que tu as appris dans la journée et le range dans ta mémoire. Bien dormir, c'est réviser sans rien faire !
   - Essaie aujourd'hui : Relis ta leçon juste avant de dormir, puis redis-la au réveil.
   - Rappel : Que fait ton cerveau avec tes leçons pendant la nuit ?
   - Source : consolidation de la mémoire pendant le sommeil (Inserm, dossier Sommeil — fait cité, texte original).
3. **Expliquer, c'est apprendre deux fois**
   - Idée : Quand tu expliques quelque chose à quelqu'un, tu le comprends mieux toi-même. C'est pour ça que les profs apprennent beaucoup !
   - Essaie aujourd'hui : Explique à un parent une chose apprise aujourd'hui.
   - Rappel : Que se passe-t-il quand tu expliques une leçon à quelqu'un ?
   - Source : Fiorella & Mayer, *Contemporary Educational Psychology*, 2013 (*learning by teaching*).

### CU — Curiosités (7+)
Sources : NASA (planètes), Wikidata (chiffres), Smithsonian Open Access (objets/images), data.gouv.fr (curiosités France).

1. **Sur Vénus, un jour dure plus longtemps qu'une année**
   - *Version 7-10 ans* : Vénus tourne très lentement sur elle-même. Elle fait le tour du Soleil (une année) avant d'avoir fini un tour sur elle-même (un jour) !
   - *Version adulte* : Vénus met environ 243 jours terrestres pour une rotation sidérale et environ 225 pour une révolution autour du Soleil ; elle tourne en plus dans le sens rétrograde.
   - Essaie aujourd'hui : Ce soir, cherche Vénus : c'est souvent le point le plus brillant après le coucher du Soleil.
   - Rappel : Sur Vénus, qu'est-ce qui est plus long : le jour ou l'année ?
   - Source : NASA Science, *Venus Facts*.
2. **Le miel peut se garder des milliers d'années**
   - Idée : Le miel contient très peu d'eau et il est un peu acide : les microbes n'y survivent presque pas. Des archéologues ont trouvé du miel ancien encore comestible dans des tombes égyptiennes.
   - Essaie aujourd'hui : Regarde la date sur un pot de miel et devine pourquoi elle est si lointaine.
   - Rappel : Pourquoi le miel ne pourrit-il presque jamais ?
   - Source : Wikipedia *Honey* (propriétés) — fait vérifié, texte original.
3. **La Tour Eiffel grandit l'été**
   - Idée : Le métal se dilate avec la chaleur. Par forte chaleur, la tour prend quelques centimètres, et le sommet penche même légèrement à l'opposé du Soleil.
   - Essaie aujourd'hui : Observe un pont ou une route : vois-tu des joints de dilatation ?
   - Rappel : Pourquoi la Tour Eiffel grandit-elle en été ?
   - Source : site officiel toureiffel.paris (chiffre exact à vérifier avant publication).

### EN — Enfants : nature, Terre, espace (8+)
Sources : NOAA Ocean Service, NASA, Our World in Data, ESA (images CC BY-SA quand indiqué).

1. **Une respiration sur deux vient de l'océan**
   - *Version 8-11 ans* : De minuscules plantes qui flottent dans la mer, le phytoplancton, fabriquent environ la moitié de l'oxygène de la Terre. Une respiration sur deux, tu la dois à l'océan !
   - *Version adulte* : On estime qu'environ 50 % de la production d'oxygène terrestre vient de l'océan, principalement du phytoplancton ; une seule espèce de cyanobactérie, *Prochlorococcus*, y contribue fortement.
   - Essaie aujourd'hui : Prends 2 grandes respirations et dis « merci l'océan » pour la deuxième.
   - Rappel : Qui fabrique la moitié de l'oxygène ? (le phytoplancton / les arbres / les volcans)
   - Source : NOAA Ocean Service, *How much oxygen comes from the ocean?*
2. **La lumière du Soleil a 8 minutes de retard**
   - Idée : La lumière met environ 8 minutes et 20 secondes pour venir du Soleil jusqu'à nous. Le Soleil que tu vois, c'est celui d'il y a 8 minutes.
   - Essaie aujourd'hui : Mets un minuteur de 8 minutes : c'est le temps du voyage de la lumière.
   - Rappel : Combien de temps la lumière du Soleil met-elle pour arriver ?
   - Source : NASA.
3. **Les abeilles dansent pour donner l'adresse des fleurs**
   - Idée : En rentrant à la ruche, l'abeille fait une danse en forme de 8. L'angle de la danse indique la direction des fleurs et sa durée indique la distance.
   - Essaie aujourd'hui : Invente une danse pour indiquer à quelqu'un où est caché un objet.
   - Rappel : Que dit la danse de l'abeille ?
   - Source : travaux de Karl von Frisch (prix Nobel 1973) — fait cité, texte original.

### SA — Sagesse (10+)
Sources : Wikisource / Gutenberg (Sénèque, Épictète, Marc Aurèle, Montaigne, La Fontaine, La Rochefoucauld), proverbes traditionnels. **Toujours traduire nous-mêmes depuis l'original** ou vérifier que le traducteur est mort depuis plus de 70 ans.

1. **Le temps n'est pas court, on le gaspille**
   - Idée : Sénèque écrit, il y a 2000 ans : « Nous n'avons pas peu de temps, nous en perdons beaucoup. » La vie est assez longue si on sait à quoi on l'emploie.
   - Essaie aujourd'hui : Note une activité qui t'a « mangé » du temps sans plaisir.
   - Rappel : Selon Sénèque, le problème est-il le manque de temps ou le temps perdu ?
   - Source : Sénèque, *De la brièveté de la vie*, I (traduction PocketSage depuis le latin : *Non exiguum temporis habemus, sed multum perdidimus*).
2. **Ce qui dépend de toi, et ce qui n'en dépend pas**
   - *Version 10-12 ans* : Épictète, un ancien esclave devenu philosophe, disait : certaines choses dépendent de toi (tes efforts, tes mots), d'autres non (la météo, ce que pensent les autres). Mets ton énergie dans les premières.
   - *Version adulte* : La première phrase du *Manuel* d'Épictète distingue ce qui est « en notre pouvoir » (jugements, désirs, actions) de ce qui ne l'est pas ; c'est la base de la pensée stoïcienne et de nombreuses approches de gestion du stress.
   - Essaie aujourd'hui : Fais deux colonnes : « dépend de moi » / « ne dépend pas de moi » pour un souci du moment.
   - Rappel : Selon Épictète, où mettre son énergie ?
   - Source : Épictète, *Manuel*, 1 (traduction PocketSage depuis le grec).
3. **Rien ne sert de courir**
   - Idée : « Rien ne sert de courir ; il faut partir à point. » Dans la fable de La Fontaine, la tortue gagne parce qu'elle commence tôt et ne s'arrête pas.
   - Essaie aujourd'hui : Commence aujourd'hui un petit bout d'un travail prévu pour plus tard.
   - Rappel : Pourquoi la tortue gagne-t-elle ?
   - Source : La Fontaine, *Le Lièvre et la Tortue* (1668, domaine public).

### MO — Motivation, habitudes (10+)
Sources : Gollwitzer & Sheeran 2006 (intentions de mise en œuvre), Amabile & Kramer 2011 (principe de progrès), méthode des 25 minutes.

1. **La phrase « Si… alors… » qui fait passer à l'action**
   - *Version 10-13 ans* : Au lieu de « je vais réviser », dis « **Si** je finis de goûter, **alors** j'ouvre mon cahier ». Ton cerveau sait exactement quand démarrer.
   - *Version adulte* : Les « intentions de mise en œuvre » (si situation X, alors action Y) augmentent nettement l'atteinte des objectifs : une méta-analyse de 94 études trouve un effet moyen à fort (d ≈ 0,65).
   - Essaie aujourd'hui : Écris une phrase « Si…, alors… » pour une chose que tu repousses.
   - Rappel : Quelle petite phrase aide à démarrer ?
   - Source : Gollwitzer & Sheeran, *Advances in Experimental Social Psychology*, 2006.
2. **Voir ses progrès donne de l'élan**
   - Idée : Une étude sur des journaux de bord de salariés montre que les meilleures journées sont celles où l'on sent qu'on avance, même un peu. Noter ses petits progrès entretient la motivation.
   - Essaie aujourd'hui : Ce soir, écris une chose où tu as avancé aujourd'hui.
   - Rappel : Qu'est-ce qui rend une journée motivante ?
   - Source : Amabile & Kramer, *The Progress Principle*, 2011 (idée citée, texte original).
3. **La méthode des 25 minutes**
   - Idée : Travaille 25 minutes sans téléphone, puis fais 5 minutes de pause. Découper un gros travail en petites tranches le rend moins effrayant (méthode dite Pomodoro).
   - Essaie aujourd'hui : Fais une tranche de 25 minutes sur un devoir ou une tâche.
   - Rappel : Combien dure une tranche de travail, et la pause ?
   - Source : Francesco Cirillo (marque Pomodoro® — ne pas utiliser comme nom de fonction).

### CF — Confiance en soi (12+)
Sources : Kross et al. 2014 (se parler à la 2e/3e personne), Brooks 2014 (recadrer le stress), Gilovich et al. 2000 (effet projecteur).

1. **Les autres te regardent moins que tu ne le crois**
   - *Version 12-14 ans* : Tu as l'impression que tout le monde remarque ta coiffure ratée ? Une expérience a montré qu'on surestime environ de moitié le nombre de gens qui nous remarquent. Chacun est trop occupé avec lui-même !
   - *Version adulte* : L'« effet projecteur » : des étudiants portant un T-shirt embarrassant estimaient qu'environ la moitié de la salle l'avait remarqué ; en réalité, moins d'un quart.
   - Essaie aujourd'hui : Fais une petite chose qui te gêne un peu (lever la main, poser une question).
   - Rappel : Les gens nous remarquent-ils plus ou moins qu'on le pense ?
   - Source : Gilovich, Medvec & Savitsky, *JPSP*, 2000.
2. **Dis « je suis excité », pas « je suis calme »**
   - Idée : Avant un oral, essayer de se calmer marche mal. Se dire « je suis excité » transforme le trac en énergie, et les participants d'une étude ont mieux réussi leurs discours.
   - Essaie aujourd'hui : Avant un moment stressant, dis-toi : « Mon cœur bat vite parce que je suis prêt. »
   - Rappel : Quelle phrase aide le plus avant un oral ?
   - Source : Brooks A. W., *Journal of Experimental Psychology: General*, 2014.
3. **Parle-toi comme à un ami**
   - Idée : Se parler en utilisant son prénom (« Léa, tu peux le faire ») plutôt que « je » aide à prendre du recul et réduit l'anxiété.
   - Essaie aujourd'hui : Encourage-toi une fois aujourd'hui avec ton prénom.
   - Rappel : Quel mot utiliser pour se parler avec recul ?
   - Source : Kross et al., *JPSP*, 2014.

### EM — Émotions ados/adultes (10+)
Sources : Pennebaker (écriture expressive), Yoo et al. 2007 (sommeil et amygdale), Seligman et al. 2005 (lettre de gratitude).

1. **Écrire ce qui pèse allège**
   - *Version 10-13 ans* : Quand quelque chose te tracasse, écris-le pendant 10 minutes sur une feuille, sans faire attention à l'orthographe. Puis tu peux la jeter. Ta tête se sent plus légère.
   - *Version adulte* : Les études d'écriture expressive (15-20 minutes sur un vécu difficile, 3-4 jours de suite) montrent des bénéfices modestes mais répétés sur l'humeur et parfois la santé.
   - Essaie aujourd'hui : 10 minutes d'écriture libre sur ce qui te prend la tête.
   - Rappel : Combien de temps écrire pour se vider la tête ?
   - Source : Pennebaker J. W., travaux sur l'écriture expressive (1986 et suivants).
2. **Une nuit blanche rend les émotions plus fortes**
   - Idée : Après une nuit sans sommeil, la zone du cerveau qui réagit aux émotions (l'amygdale) réagit environ 60 % plus fort. Ce n'est pas toi qui es « trop sensible » : c'est la fatigue.
   - Essaie aujourd'hui : Ce soir, couche-toi 20 minutes plus tôt.
   - Rappel : Que fait le manque de sommeil aux émotions ?
   - Source : Yoo et al., *Current Biology*, 2007.
3. **La lettre de merci**
   - Idée : Écrire puis lire une lettre de remerciement à quelqu'un qui a compté augmente le bien-être. L'effet est fort sur le moment et s'estompe en quelques semaines, d'où l'intérêt de recommencer.
   - Essaie aujourd'hui : Envoie un message de merci précis à quelqu'un.
   - Rappel : Combien de temps dure l'effet d'une lettre de gratitude ?
   - Source : Seligman et al., *American Psychologist*, 2005.

### PS — Psychologie, cerveau (8+)
Sources : Roediger & Karpicke 2006, Zajonc 1968, Wason 1960.

1. **Se tester bat relire**
   - *Version 8-11 ans* : Relire sa leçon donne l'impression de la savoir. Mais essayer de la redire sans regarder la fait vraiment entrer dans la tête.
   - *Version adulte* : L'« effet de test » : des étudiants qui se testaient retenaient nettement plus une semaine plus tard que ceux qui relisaient, même s'ils se sentaient moins sûrs d'eux sur le moment.
   - Essaie aujourd'hui : Cache ta leçon et redis 3 choses dont tu te souviens.
   - Rappel : Qu'est-ce qui fait mieux retenir : relire ou se tester ? *(C'est justement ce que fait cette question !)*
   - Source : Roediger & Karpicke, *Psychological Science*, 2006.
2. **On aime ce qu'on voit souvent**
   - Idée : Plus on voit quelque chose, plus on a tendance à l'aimer, même sans s'en rendre compte. C'est pour ça que les pubs se répètent.
   - Essaie aujourd'hui : Repère une chanson que tu aimes maintenant mais pas la première fois.
   - Rappel : Pourquoi les publicités se répètent-elles ?
   - Source : Zajonc R., *JPSP*, 1968 (effet de simple exposition).
3. **Notre cerveau cherche à avoir raison**
   - Idée : On cherche plus facilement les preuves qui confirment ce qu'on croit déjà que celles qui le contredisent. C'est le biais de confirmation.
   - Essaie aujourd'hui : Cherche un argument contre une idée à laquelle tu tiens.
   - Rappel : Comment s'appelle ce biais ?
   - Source : Wason P., *Quarterly Journal of Experimental Psychology*, 1960.

### AD — Ados : biais et comportement (13+)
Sources : Tversky & Kahneman 1974, Johnson & Goldstein 2003, Buehler et al. 1994.

1. **Le premier chiffre entendu nous piège**
   - *Version 14-17 ans* : Si un vendeur dit d'abord « 200 € », 120 € te semblera une affaire, même si l'objet en vaut 60. Le premier chiffre sert d'ancre à ton cerveau.
   - *Version adulte* : Dans l'expérience classique, un nombre tiré d'une roue de loterie influençait l'estimation du pourcentage de pays africains à l'ONU : l'ancrage marche même quand l'ancre est visiblement arbitraire.
   - Essaie aujourd'hui : Avant de regarder un prix, décide combien tu es prêt à payer.
   - Rappel : Comment s'appelle ce biais ?
   - Source : Tversky & Kahneman, *Science*, 1974.
2. **L'option par défaut décide souvent pour nous**
   - Idée : Dans les pays où il faut refuser explicitement le don d'organes, l'accord déclaré est bien plus élevé que là où il faut s'inscrire. On suit souvent ce qui est déjà coché.
   - Essaie aujourd'hui : Vérifie un abonnement ou un réglage « par défaut » que tu n'as jamais choisi.
   - Rappel : Pourquoi les cases précochées sont-elles si efficaces ?
   - Source : Johnson & Goldstein, *Science*, 2003.
3. **On sous-estime toujours le temps nécessaire**
   - Idée : Des étudiants ont estimé le temps pour finir leur mémoire : la plupart ont dépassé même leur estimation « si tout va mal ». C'est l'erreur de planification.
   - Essaie aujourd'hui : Prends ta prochaine estimation et ajoute 50 %.
   - Rappel : Comment s'appelle cette erreur ?
   - Source : Buehler, Griffin & Ross, *JPSP*, 1994.

### Cartes existantes à revoir (fiabilité)
- **CF-001** (power pose → cortisol/testostérone) : l'effet hormonal **n'a pas été répliqué** (Ranehill et al., 2015). Garder éventuellement l'effet ressenti, retirer les hormones.
- **MO-001** : formule trop proche de James Clear (voir §1).
- **EJ-001** (« la colère dure 90 secondes ») : chiffre issu d'un livre grand public, pas d'étude solide → reformuler sans chiffre.
- **EM-002** (cortisol dans les larmes), **PS-002** (sourire forcé → joie) : résultats discutés → nuancer (« certaines études suggèrent »).

---

## 4. Pipeline de production proposé

1. **Collecte** : une liste de faits/études par catégorie dans `data/flash/sources_{CAT}.csv` (fait brut, URL, licence). Wikidata via SPARQL pour les faits chiffrés ; liste manuelle d'études pour PS/AD/EM/CF/MO/MJ/EJ.
2. **Génération par lots avec Claude** : 25 cartes par lot et par catégorie, à partir des **faits uniquement** (jamais coller un texte source). Prompt imposant le format Titre / Idée / Essaie aujourd'hui / Rappel (QCM 3 choix) / Source + une version enfant et une version adulte quand c'est pertinent.
3. **Relecture humaine** : vérifier le fait dans la source, le ton, l'âge. Champ `statut: "relu"` + `verifie_le`.
4. **JSON** : sortir les cartes de `index.html` vers un fichier `data/flash/fr.json`, par exemple :
   ```json
   {"id":"EN-011","cat":"EN","age":"8+",
    "titre":"Une respiration sur deux vient de l'océan",
    "idee":"…","idee_adulte":"…",
    "action":"…",
    "rappel":{"q":"Qui fabrique la moitié de l'oxygène ?","choix":["le phytoplancton","les arbres","les volcans"],"ok":0},
    "source":{"nom":"NOAA Ocean Service","url":"https://oceanservice.noaa.gov/facts/ocean-oxygen.html","licence":"domaine public US"},
    "statut":"relu","verifie_le":"2026-11-10"}
   ```
   ⚠️ `generate_flash_tts.py` lit aujourd'hui les cartes dans `index.html` par expression régulière : il faudra l'adapter pour lire ce JSON.
5. **Traduction** : Google Translate depuis le FR (cache existant `data/flash_translations/{lang}.json`) ; relecture rapide des citations SA, qui doivent être traduites depuis l'original et non depuis le français si possible.
6. **TTS** : `generate_flash_tts.py` → R2 `audio/flash/{lang}/`. Pour qu'une carte **modifiée** soit régénérée, stocker un hash du texte dans le manifest au lieu du seul identifiant.
7. **Rythme réaliste** : 25 cartes × 11 catégories = 275 cartes par cycle ; 4 cycles ≈ 1100 cartes. La relecture humaine est le goulot d'étranglement (≈ 1-2 min par carte).

---

## 5. Sources

- [Licence Ouverte 2.0 — data.gouv.fr](https://www.data.gouv.fr/pages/legal/licences/etalab-2.0)
- [Our World in Data — FAQ (licence CC BY)](https://ourworldindata.org/faqs)
- [Smithsonian — 2,8 millions d'images en CC0](https://www.si.edu/newsdesk/releases/smithsonian-releases-28-million-free-images-broader-public-use)
- [NASA — Images and Media guidelines](https://nasa.gov/nasa-brand-center/images-and-media)
- [ESA — Licence CC BY-SA 3.0 IGO](https://www.esa.int/Services/Creative_Commons_Attribution-ShareAlike_3.0_IGO_CC_BY-SA_3.0_IGO_licence)
- [Project Gutenberg — Permissions](https://gutenberg.org/policy/permission)
- [Tatoeba — Téléchargements et licences](https://tatoeba.org/ca/downloads)
- [Open Trivia DB — API (CC BY-SA 4.0)](https://opentdb.com/api_config.php)
- [Europeana — Rights statements FAQ](https://pro.europeana.eu/page/rights-statements-faq)
- [OpenStax — Commercial use under the Creative Commons License](https://help.openstax.org/s/article/Commercial-use-under-the-Creative-Commons-License)
- [OpenStax — Biology 2e, préface (CC BY-NC-SA)](https://openstax.org/books/biology-2e/pages/preface)
- [CK-12 FlexBook — Wikipedia](https://en.wikipedia.org/wiki/FlexBook)
- [Khan Academy — Can I use Khan Academy's materials?](https://support.khanacademy.org/hc/en-us/articles/202262954-Can-I-use-Khan-Academy-s-videos-name-materials-links-)
- [OMS — Copyright, licensing and permissions](https://www.who.int/copyright)
- [Assemblée nationale — Question écrite sur la réutilisation commerciale de Gallica](https://www.assemblee-nationale.fr/dyn/14/questions/QANR5L14QE23878.pdf)
- [CA Paris 16/10/2013 — idées non protégeables (Lettre des réseaux)](https://www.lettredesreseaux.com/?p=6154)
- [Ranehill et al. 2015 — Power posing, réplication (PDF)](https://www.zne.uzh.ch/dam/jcr:e5fc4c3c-d50e-4aa9-96ab-4389e426d20d/Psychological%20Science-2015-Ranehill-0956797614553946.pdf)
- [Pomodoro Technique — Wikipedia](https://www.wikipedia.org/wiki/Pomodoro_timer)

Références scientifiques citées dans les cartes (à vérifier en DOI avant publication) : Lieberman et al. 2007 ; Yeager et al. 2019 ; Roediger & Karpicke 2006 ; Fiorella & Mayer 2013 ; Gollwitzer & Sheeran 2006 ; Amabile & Kramer 2011 ; Gilovich et al. 2000 ; Brooks 2014 ; Kross et al. 2014 ; Pennebaker 1986 ; Yoo et al. 2007 ; Seligman et al. 2005 ; Zajonc 1968 ; Wason 1960 ; Tversky & Kahneman 1974 ; Johnson & Goldstein 2003 ; Buehler et al. 1994.
