# Illustrations des exercices sportifs — prompt pour ChatGPT (Work / images)

95 exercices, chacun décomposé en **2 à 4 images** (les étapes du mouvement). Colle d'abord le bloc « STYLE »
ci-dessous, puis demande les images par paquets (par exemple « fais les 5 exercices suivants de la liste »).
Chaque image est nommée `<id>-<étape>.png` (ex. `YF-012-1.png`, `YF-012-2.png`), et ChatGPT tient à jour
un fichier `legendes.json` avec une courte légende par image. À la fin, mets tout dans un zip et envoie-le à Claude : il vérifie chaque dessin
(posture conforme à la consigne, sécurité), les allège et les intègre dans l'appli + les cartes PDF.

```
STYLE (à respecter pour TOUTES les images, pour qu'elles forment une collection cohérente)
- Dessin d'illustration jeunesse façon crayon de couleur : trait de crayon graphite visible, remplissage doux
  au crayon de couleur / aquarelle légère, couleurs pastel chaleureuses (vert sauge, bleu ciel, jaune doux, corail).
- Fond blanc uni, sans décor, sans sol dessiné (juste une petite ombre douce sous le personnage), sans texte,
  sans lettre, sans chiffre, sans logo.
- Format carré 1024 × 1024, personnage centré, entier, avec une marge autour.
- PERSONNAGES RÉCURRENTS (toujours identiques d'une image à l'autre) :
  • L'enfant « Sami » : environ 7 ans, cheveux châtains bouclés courts, t-shirt vert sauge, legging gris clair, pieds nus.
  • L'adulte « Lou » : cheveux bruns attachés en queue de cheval basse, haut bleu marine, pantalon beige souple, pieds nus.
  • Exercices seuls : Sami seul. Exercices « Yoga en famille » : Sami ET Lou ensemble.
- Visages simples et souriants (ou yeux fermés pour la respiration et la relaxation), proportions réalistes
  pour que la posture soit EXACTE et facile à imiter : bras, jambes, dos et tête placés exactement comme la consigne.
- DÉCOMPOSITION EN ÉTAPES : chaque exercice = 2 à 4 images qui montrent les étapes clés, dans l'ordre :
  • posture tenue (ex. l'arbre) : 2 images = entrée dans la posture, puis posture finale ;
  • mouvement aller-retour (ex. le ballon, le chat et la vache) : 2 ou 3 images = position de départ, position haute, position basse ;
  • enchaînement (ex. le salut au soleil) : 4 images maximum, les positions les plus importantes ;
  • exercice avec changement de côté : la dernière image peut montrer l'autre côté.
  Les images d'un même exercice ont exactement le même cadrage, la même taille de personnage et le même angle de vue,
  pour qu'on puisse les faire défiler comme un petit dessin animé.
- DUO ADULTE + ENFANT : tiens compte de la différence de taille. Si l'enfant ne peut pas atteindre l'adulte
  (mains jointes, bras levés ensemble), l'adulte se met à genoux ou s'assoit pour être à sa hauteur.
- Sécurité : aucun porté, aucun enfant debout sur l'adulte, aucune acrobatie ; dos et nuque dans une position naturelle.
- Style original : ne copie aucune marque, aucun personnage ni aucun jeu de cartes existant.

Je vais te donner une liste « identifiant — nom de l'exercice : consigne ». Pour chaque exercice :
1. décide du nombre d'étapes (2 à 4) ;
2. crée les images `<id>-1.png`, `<id>-2.png`… qui montrent exactement la consigne ;
3. ajoute dans `legendes.json` une légende courte par image (8 mots maximum, tutoiement pour un enfant seul,
   vouvoiement pour un duo), au format {"YF-012-1": "Face à face, l'adulte à genoux, mains jointes", ...}.
Fais-les dans l'ordre, en vérifiant à chaque fois que chaque posture correspond à la consigne.
À la fin de chaque paquet, donne-moi un zip avec les images ET legendes.json à jour.
```

## Liste des 95 exercices (identifiant — nom : consigne)

### Cardio

- **DF-001** — La Statue : Fais la statue : ne bouge plus du tout jusqu'au bip !
- **DF-002** — Le Saut : Saute sur le pied droit, puis sur le pied gauche quand le coach dit de changer !
- **DF-003** — Le Pingouin : Marche comme un pingouin : bras collés, pieds en V, jusqu'au bip !
- **DF-004** — La Fusée : Accroupis-toi puis saute le plus haut possible ! Recommence jusqu'au bip !
- **DF-005** — Le Crabe : Position crabe, ventre vers le haut : avance et recule jusqu'au bip !
- **DF-006** — L'Avion : Sur un pied, penche le corps, bras en ailes ! Change de pied quand le coach le dit.
- **DF-007** — Les Grenouilles : Accroupis-toi et saute comme une grenouille en criant coâ, jusqu'au bip !
- **DF-008** — La Danse Robot : Danse comme un robot jusqu'au bip : mouvements saccadés !
- **DF-012** — Sprint des Héros : Cours sur place le plus vite possible, genoux bien hauts, jusqu'au bip !
- **DF-013** — Les Squats Rigolos : Pieds écartés, descends en gardant le dos droit, comme pour t'asseoir sur une chaise invisible. Enchaîne les squats jusqu'au bip !
- **DF-017** — Les Jumping Jacks ⭐ : Pieds joints, bras le long du corps. Saute en écartant pieds et bras en même temps, comme une étoile ! Enchaîne jusqu'au bip !
- **DF-019** — Le Mountain Climber : En position de pompe, ramène un genou puis l'autre vers ta poitrine, le plus vite possible, jusqu'au bip !
- **DF-020** — Les Burpees Faciles : Debout, mains au sol, tends les jambes, reviens, puis saute les bras en l'air ! Enchaîne à ton rythme jusqu'au bip.
- **DF-021** — Les Pompes Genoux : À quatre pattes, genoux au sol. Descends la poitrine vers le sol en pliant les coudes, puis remonte. Enchaîne jusqu'au bip !
- **DF-022** — Course de Canards : Accroupis-toi bas et avance sans te relever, jambes fléchies. Fais des allers-retours jusqu'au bip !
- **DF-023** — Les Fentes : Fais un grand pas en avant, le genou arrière descend sans toucher le sol, puis reviens debout. Alterne les jambes jusqu'au bip !
- **DF-024** — Le Saut du Lapin : Saute vers l'avant à pieds joints, le plus loin possible ! Fais demi-tour et recommence jusqu'au bip !
- **DF-025** — Le Boxeur : Debout, pieds écartés. Frappe l'air en alternant les bras et souffle fort à chaque coup : hop ! Jusqu'au bip !
- **DF-026** — L'Ourson Marcheur : Sur les mains et les pieds (pas les genoux !), marche comme un ours, aller-retour, jusqu'au bip.
- **DF-057** — Le Nageur : Debout, fais le crawl avec tes bras, le plus vite possible, en restant bien droit. Jusqu'au bip !
- **DF-058** — Pompes au mur : Mains contre un mur, corps bien droit. Plie les coudes pour approcher le nez du mur, puis pousse. Enchaîne jusqu'au bip !
- **DF-059** — Les Moulins à vent : Bras tendus, fais de grands cercles rapides vers l'avant, puis vers l'arrière, jusqu'au bip !

### Gainage

- **DF-014** — La Planche : Appuie-toi sur tes coudes et la pointe des pieds, corps bien droit comme une planche. Tiens jusqu'au bip ! Pose les genoux si c'est trop dur.
- **DF-027** — Planche Latérale ↔ : Allonge-toi sur le côté, appuie-toi sur le coude et lève les hanches : corps en ligne droite. Change de côté quand le coach le dit !
- **DF-028** — Planche Latérale Gauche ⬇ : Même exercice sur le côté gauche ! Corps droit, appuyé sur le coude gauche. Tiens jusqu'au bip !
- **DF-029** — Le Superman : Allonge-toi sur le ventre, bras tendus devant. Lève ensemble le bras droit et la jambe gauche, puis repose-les. Ensuite le bras gauche et la jambe droite. Le coach te dit quand changer !
- **DF-030** — La Table : Assieds-toi, mains au sol derrière toi. Pousse les hanches vers le haut, comme une table renversée. Tiens jusqu'au bip !
- **DF-031** — Crunch Simple : Allongé sur le dos, genoux fléchis, bras croisés sur la poitrine. Lève les épaules du sol en serrant le ventre, puis redescends. Enchaîne jusqu'au bip !
- **DF-032** — Le Pont : Allongé sur le dos, genoux fléchis, pieds à plat. Pousse les hanches vers le haut en serrant les fesses. Tiens, redescends doucement, et recommence jusqu'au bip !
- **DF-033** — La Planche sur Mains : Position de pompe, bras tendus, corps bien droit. Tiens sans bouger jusqu'au bip !
- **DF-034** — Dead Bug : Sur le dos, bras et jambes en l'air. Descends le bras droit et la jambe gauche sans toucher le sol, remonte. Puis l'autre côté. Le coach te dit quand changer !

### Étirements

- **DF-009** — Étirement du Cobra : Allonge-toi sur le ventre. Pose les mains sous les épaules. Pousse pour lever doucement la tête et le buste. Reste 20s. Redescends lentement. Répète 3 fois.
- **DF-010** — Étirement Papillon : Assieds-toi par terre. Colle tes pieds ensemble, genoux écartés. Tiens tes pieds avec tes mains. Balance doucement tes genoux comme des ailes. 30 secondes.
- **DF-011** — Étirement Chat-Vache : À quatre pattes. Dos rond comme un chat fâché, tête baissée — 5s. Puis dos creusé, tête levée — 5s. Alterne 8 fois lentement.
- **DF-015** — Yoga de l'Arbre : Pose le pied droit sur ta cheville ou ta cuisse gauche. Joins les mains devant toi. Équilibre-toi comme un arbre dans le vent — 20 secondes par pied.
- **DF-016** — Étirement des Épaules : Lève le bras droit, coude plié derrière la tête. Pousse doucement avec la main gauche. Tiens 20s. Change de côté. Répète 2 fois.
- **DF-035** — L'Enfant Sage : À genoux, assieds-toi sur tes talons. Penche-toi en avant, bras tendus devant. Front au sol (ou proche). Reste 30 secondes. Respire.
- **DF-036** — Étirement des Ischio : Assieds-toi, jambes tendues devant toi. Penche doucement le buste vers l'avant, mains vers les pieds. Tiens 20s sans forcer.
- **DF-037** — Le Pigeon : Mets le genou droit plié devant toi, jambe gauche tendue derrière. Reste penché en avant. 20s de chaque côté.
- **DF-038** — Rotation du Torse : Assieds-toi, jambes croisées. Pose la main droite sur le genou gauche et tourne le buste vers la gauche. 15s. Change de côté.
- **DF-039** — Le Guerrier 1 : Grand pas en avant pied droit. Genou droit fléchi. Jambe gauche tendue. Bras levés vers le ciel. Tiens 20s. Change de côté.
- **DF-040** — Étirement du Cou : Assieds-toi droit. Penche lentement la tête vers l'épaule droite. Tiens 10s. Centre. Penche vers la gauche. 10s. 2 fois de chaque côté.

### Respiration

- **DF-018** — Respiration Carrée : Inspire 4s → retiens 4s → expire 4s → vide 4s. Répète 4 cycles. Ferme les yeux si tu veux.
- **DF-041** — Le Ballon : Gonfle ton ventre comme un ballon quand tu inspires (4s). Puis dégonfle-le doucement en expirant (6s). Fais 5 respirations profondes.
- **DF-042** — La Respiration du Lion : Inspire par le nez. Puis expire très fort par la bouche, langue sortie, yeux grands ouverts — comme un lion qui rugit ! 5 fois.
- **DF-043** — Cohérence Cardiaque : Inspire lentement par le nez pendant 5 secondes. Expire lentement par la bouche pendant 5 secondes. Répète 6 fois de suite (1 minute).
- **DF-044** — La Respiration 4-7-8 : Inspire par le nez pendant 4s. Retiens ta respiration 7s. Expire très lentement par la bouche pendant 8s. Répète 3 fois.
- **DF-045** — La Respiration du Vent : Debout, bras le long du corps. Inspire en levant les bras au-dessus de la tête (3s). Expire en les redescendant (5s). 6 cycles.
- **DF-046** — Le Nettoyage du Cerveau : Inspire par le nez — remplis le ventre d'abord, puis la poitrine (4s). Retiens 1s. Expire fort par la bouche en faisant WHOOSH (6s). 4 fois.
- **DF-047** — La Respiration Alternée : Bouche ton narine droite avec le pouce. Inspire par la gauche (4s). Bouche la gauche avec l'index. Expire par la droite (4s). Alterne 4 cycles.
- **DF-048** — Respiration des Super-Héros : Inspire fort et lève les bras comme tu décoles. Retiens 3s, poings fermés. Expire PUISSAMMENT en ramenant les poings vers toi. 5 fois !

### Échauffement

- **DF-049** — Cercles de bras : Bras tendus sur les côtés, fais des petits cercles, puis des grands. À la moitié, change de sens.
- **DF-050** — Rotation du buste : Debout, pieds écartés, mains sur les hanches. Tourne doucement le haut du corps vers la droite, puis vers la gauche.
- **DF-051** — Cercles de hanches : Mains sur les hanches, dessine de grands cercles avec ton bassin, dans un sens puis dans l'autre.
- **DF-052** — Montées de genoux : Marche sur place en levant les genoux bien haut, sans courir. Balance les bras.
- **DF-053** — Talons-fesses : Trottine doucement sur place en ramenant les talons vers les fesses.
- **DF-054** — Balancier des jambes ↔ : Pieds bien écartés, plie doucement une jambe puis l'autre, en passant ton poids d'un côté à l'autre.
- **DF-055** — Chevilles et poignets : Fais tourner une cheville, puis l'autre, et fais tourner tes poignets en même temps.
- **DF-056** — Épaules qui roulent : Fais rouler tes épaules vers l'arrière, puis vers l'avant, bien lentement.

### Yoga

- **YG-001** — La Montagne : Debout, pieds serrés, bras le long du corps. Grandis-toi comme une montagne et respire calmement par le nez.
- **YG-002** — L'Arbre : Debout sur un pied, pose l'autre pied contre ta cheville ou ton mollet, jamais sur le genou. Lève les bras comme des branches. Change de pied quand le coach le dit.
- **YG-003** — Le Chat et la Vache : À quatre pattes. Inspire en creusant le dos et en levant la tête, comme une vache. Souffle en arrondissant le dos, comme un chat. Continue tout doucement.
- **YG-004** — Le Chien tête en bas : Mains et pieds au sol, lève les fesses vers le ciel pour faire un grand V à l'envers. Laisse ta tête pendre. Tu peux plier un peu les genoux.
- **YG-005** — Le Cobra : Allongé sur le ventre, mains sous les épaules. Soulève doucement la poitrine, coudes un peu pliés, et siffle comme un serpent.
- **YG-006** — La Petite Graine : À genoux, assieds-toi sur tes talons et pose le front au sol, bras le long du corps. Tu es une petite graine qui se repose sous la terre.
- **YG-007** — Le Papillon : Assis, colle tes plantes de pieds l'une contre l'autre, genoux ouverts. Tiens tes pieds et bats doucement des ailes avec tes genoux.
- **YG-008** — Le Guerrier : Écarte grand les jambes et tourne un pied vers l'extérieur. Plie ce genou au-dessus de la cheville, bras tendus à l'horizontale, et regarde la main du côté du genou plié.
- **YG-009** — L'Étoile ⭐ : Debout, écarte grand les jambes et les bras pour faire une étoile à cinq branches. Étire-toi du bout des doigts jusqu'aux orteils.
- **YG-010** — Le Bateau : Assis, genoux pliés, penche-toi un peu en arrière et décolle les pieds du sol. Bras tendus devant toi, garde le dos bien droit.
- **YG-011** — Le Pont : Allongé sur le dos, genoux pliés, pieds à plat. Pousse sur tes pieds et soulève les fesses pour faire un pont. Redescends tout doucement.
- **YG-012** — La Grenouille : Accroupis-toi, pieds écartés, mains au sol entre les genoux. Fais un petit saut de grenouille et reviens en douceur. Recommence plusieurs fois, tranquillement.
- **YG-013** — Le Lion : Assis sur les talons, mains sur les genoux. Inspire par le nez, puis ouvre grand la bouche, tire la langue et souffle fort comme un lion qui rugit.
- **YG-014** — Le Flamant rose : Debout sur une jambe, lève l'autre genou devant toi et ouvre les bras comme des ailes. Change de jambe quand le coach le dit.
- **YG-015** — La Chaise : Pieds serrés, plie les genoux comme pour t'asseoir sur une chaise invisible, et lève les bras vers le ciel. Garde le poids sur les talons.
- **YG-016** — Le Bébé heureux : Allongé sur le dos, ramène tes genoux vers ton ventre et attrape tes pieds par l'extérieur, plantes de pieds vers le plafond. Balance-toi doucement de droite à gauche.
- **YG-017** — L'Étoile de mer : Allongé sur le dos, bras et jambes un peu écartés, yeux fermés. Laisse ton corps devenir tout lourd et écoute ta respiration.
- **YG-018** — Le Salut au soleil : Enchaîne lentement : montagne, bras au ciel, penche-toi en avant, planche, pose-toi au sol, cobra, chien tête en bas, marche vers tes mains, remonte bras au ciel. Une respiration par mouvement.
- **YG-019** — La Pince : Assis, jambes tendues devant toi. Grandis-toi en levant les bras, puis penche-toi doucement en avant et pose les mains là où elles arrivent, sur les jambes ou les pieds.
- **YG-020** — La Torsion allongée : Allongé sur le dos, genoux pliés, bras ouverts en croix. Laisse tomber doucement tes genoux d'un côté et tourne la tête de l'autre côté. Au bip, change de côté.
- **YG-021** — Le Triangle : Jambes écartées, pied avant tourné vers l'extérieur, bras ouverts. Penche-toi sur le côté vers ta jambe avant, pose la main sur le bas de ta jambe et lève l'autre bras vers le ciel. Au bip, change de côté.

### Yoga en famille (adulte + enfant)

- **YF-001** — L'Arbre à deux (duo adulte + enfant) : Côte à côte, tenez-vous par la taille ou par l'épaule. Chacun pose le pied extérieur contre sa cheville ou son mollet, jamais sur le genou, et lève le bras libre. Au bip, changez de place. (Astuce : Appuyez-vous un peu l'un sur l'autre. L'adulte tient l'enfant par l'épaule, l'enfant tient l'adulte par la taille.)
- **YF-002** — Le Bateau à deux (duo adulte + enfant) : Assis face à face, genoux pliés, tenez-vous les mains. Collez vos plantes de pieds, puis levez les jambes ensemble pour faire un bateau. Gardez le dos droit. (Astuce : L'adulte plie davantage les genoux. Si c'est trop dur, gardez une seule jambe levée chacun.)
- **YF-003** — Dos à dos qui respire (duo adulte + enfant) : Assis en tailleur, dos contre dos. Fermez les yeux et sentez le dos de l'autre bouger quand il respire. Essayez de respirer au même rythme. (Astuce : Respirez lentement par le nez.)
- **YF-004** — La Torsion à deux (duo adulte + enfant) : Assis en tailleur, dos à dos. Tournez-vous tous les deux vers votre droite : main gauche sur votre genou droit, main droite sur le genou de votre partenaire. Au bip, tournez vers la gauche. (Astuce : Tournez doucement en grandissant le dos, sans forcer. Si votre main n'atteint pas le genou de l'autre, posez-la sur le sol à côté.)
- **YF-005** — La Chaise dos à dos (duo adulte + enfant) : Debout dos contre dos, accrochez vos bras. Avancez un peu les pieds et pliez les genoux en même temps, à mi-hauteur seulement, comme deux chaises qui se tiennent. Remontez ensemble doucement. (Astuce : Sur un sol qui ne glisse pas, avec deux partenaires de taille proche.)
- **YF-006** — Le Tunnel (duo adulte + enfant) : L'adulte fait le chien tête en bas, bien solide. L'enfant passe à quatre pattes sous le tunnel, puis fait demi-tour et repasse. (Astuce : L'adulte reste immobile pendant que l'enfant passe.)
- **YF-007** — Le Lézard sur le rocher (duo adulte + enfant) : L'adulte se met en petite graine, front au sol. L'enfant s'assoit sur le bas du dos de l'adulte, près des fesses, puis s'allonge doucement en arrière, dos contre dos, bras ouverts. (Astuce : Seulement avec un enfant léger et un adulte sans mal de dos. L'adulte dit stop s'il est gêné. Pour descendre, l'enfant roule doucement sur le côté.)
- **YF-008** — La Balançoire (duo adulte + enfant) : Assis face à face, jambes écartées. L'adulte plie un peu les genoux. L'enfant pose ses pieds contre les chevilles de l'adulte. Tenez-vous les mains et penchez-vous l'un après l'autre, doucement, comme une balançoire. (Astuce : Allez lentement et ne tirez pas fort sur les bras.)
- **YF-009** — Les Papillons jumeaux (duo adulte + enfant) : Assis face à face, chacun fait le papillon, plantes de pieds collées. Approchez-vous jusqu'à ce que vos orteils se touchent, tenez-vous les mains et battez des ailes ensemble. (Astuce : Si vos mains ne se touchent pas, reculez un peu les pieds ou tenez un foulard.)
- **YF-010** — Le Miroir (duo adulte + enfant) : Debout face à face. L'un fait des postures très lentement, l'autre l'imite comme un miroir. Changez de chef quand le coach le dit. (Astuce : Plus c'est lent, plus le miroir est parfait.)
- **YF-011** — Le Double chien (duo adulte + enfant) : Dos à dos, un grand pas l'un de l'autre, faites le chien tête en bas en même temps. Regardez-vous entre vos jambes et faites une grimace ! (Astuce : Pliez un peu les genoux si l'arrière des jambes tire.)
- **YF-012** — Le Ballon à deux (duo adulte + enfant) : Face à face, mains jointes. L'adulte se met à genoux, assis sur les talons, l'enfant reste debout. Inspirez en levant les bras ensemble, comme un ballon qui gonfle. Soufflez en redescendant les bras. (Astuce : Gardez le même rythme que votre partenaire.)
- **YF-013** — Le Guerrier à deux (duo adulte + enfant) : Côte à côte, regardez dans la même direction. Chacun fait le guerrier vers l'extérieur, pieds arrière presque collés. Tenez-vous par la main du milieu. Au bip, changez de place. (Astuce : Le genou plié reste au-dessus de la cheville. L'adulte écarte davantage les pieds pour descendre et baisse son bras vers la main de l'enfant.)
- **YF-014** — Les Étoiles de mer à deux (duo adulte + enfant) : Allongés sur le dos, tête contre tête, tenez-vous les mains. Fermez les yeux et laissez tout votre corps se relâcher. (Astuce : Écoutez la respiration de l'autre.)
- **YF-015** — Le Triangle à deux (duo adulte + enfant) : Dos à dos, jambes écartées. Tournez un pied vers le même mur et penchez-vous tous les deux de ce côté. Une main glisse sur votre jambe, l'autre se lève et attrape celle du partenaire. Au bip, changez de côté. (Astuce : Restez dos contre dos et penchez-vous en même temps, doucement. L'adulte écarte davantage les pieds et descend son bras levé pour attraper la main de l'enfant.)
