# Mon Monde — conception v2 (12/11/2026)

## 1. Visuels (demandes du 12/11)
- Bâtiments en vrai volume 3D façon packs Kenney, **posés pile sur leur case** (pas de travers). 3-4 styles de maisons (maisonnette, maison, villa + immeuble).
- Enseignes lisibles : petite plaque/icône au-dessus de la porte (croix verte pharmacie, cintre magasin, fourchette resto, H hôpital…).
- Nouveaux bâtiments : **hôpital, ferme (grange), école, garage mécanique, parking**.
- Manèges dessinés et **animés** pour être distinctifs : grande roue qui tourne, carrousel à chevaux, grand 8 (wagon qui roule sur les rails), chaises volantes, bateau pirate, autos tamponneuses.
- Voitures : utiliser le dessin qui correspond au sens de la route (8 directions dans le pack) → fini les voitures « en crabe ».
- Ferme : clôtures + bottes de foin pour enclos vaches et poulailler ; **champs sans clôture** ; cultures variées : maïs, carottes, salades, tomates, arbres fruitiers.
- Ponts hauts : bateaux dessous, voitures et piétons dessus.
- ⚠️ Casino : à renommer (ex. « salle d'arcade ») — un casino dans une appli enfants pose problème pour les catégories Familles / Enfants des stores.

## 2. Mode « Ma vie » (avatar) — proposition
- Deux modes : **Maire** (construire, actuel) et **Ma vie** (l'avatar vit dans la ville). Zoom au doigt, caméra qui suit l'avatar.
- Déplacement : on touche un bâtiment → l'avatar y va à pied par les trottoirs. Si c'est loin : **taxi/bus** (coûte des jetons) ou **sa voiture** (achetée au garage).
- 3 jauges simples : 😋 faim, ⚡ énergie, 😊 joie. Courses → faim ; maison → énergie ; parc, bateau, manèges → joie. Hôpital si les jauges tombent trop bas.
- Famille : l'avatar a des enfants à emmener à l'école le matin et à rechercher le soir (cycle jour/nuit : 1 journée de jeu ≈ 10 min réelles).
- Qui décide ? Le joueur choisit ; s'il ne fait rien, option **« quartier libre »** : l'avatar vit seul des activités gratuites.
- Comment le joueur sait quoi faire : **3 missions du jour proposées par Sensei** (bulle au-dessus de l'avatar + « ! » sur les bâtiments concernés). Toucher un bâtiment affiche ce qu'on peut y faire et le prix.

## 3. Économie
- Jetons gagnés **uniquement en apprenant** (QCM, Flash, jeux, dialogues).
- Investir : construire → chaque bâtiment rapporte des jetons dans le temps (affichage « rentabilisé en X jours »).
- Dépenser : vie de l'avatar (courses, taxi, manèges, bateau…).
- Pas d'achat de jetons avec de l'argent réel (règles stores enfants) ; limites quotidiennes cohérentes avec l'esprit anti-scroll.

## 4. Découpage proposé (estimation crédits)
| Phase | Contenu | Coût |
|---|---|---|
| 1 | Bâtiments 3D calés + enseignes + nouveaux bâtiments + voitures orientées + ferme/cultures | ~1 à 1,5 session |
| 2 | Manèges animés + ponts hauts | ~1 session |
| 3 | Mode « Ma vie » : déplacement, taxi, jauges, missions, jour/nuit, enfants | ~2 à 3 sessions |
| 4 | Réglage de l'économie (gains / prix / rentabilité) | ~0,5 session |

## 5. Groupe familial (demande du 12/11) — 5 personnages max
- Le joueur gère **un groupe de 1 à 5 personnages** : son avatar + jeunes enfants + adultes / grands.
- **Activités à plusieurs** : parc d'attractions, bateau, cinéma, plage, restaurant → le prix est **par personne** (sortir à 5 coûte plus cher → intérêt de construire et d'investir).
- **Activités seul** : un adulte ou un grand peut partir **travailler / récolter** seul (ferme, magasin, garage…) → il rapporte un bonus de récolte sur ce bâtiment.
- Règle simple et logique : **un jeune enfant ne sort jamais seul** — il faut un adulte ou un grand avec lui (école, parc, hôpital).
- On sélectionne qui part (touche les portraits en bas de l'écran), puis on touche la destination.
- Recrutement : 1 personnage au départ ; les suivants se débloquent avec la maison (Maison = 3 places, Villa = 5).

## 6. ⚠️ Constat technique (12/11)
- Le monde est enregistré sous une seule clé (`psa3_world3`) → **tous les profils enfants du téléphone partagent la même ville et les mêmes jetons**. À corriger : un monde par profil.
- Aujourd'hui les gains sont déséquilibrés : l'apprentissage ne rapporte que **1 🪙 par bonne réponse d'aventure** (rien pour Flash, mini-jeux, dialogues), alors que les bâtiments produisent **toutes les 8 secondes** tant que le monde est ouvert (une maisonnette de 20 🪙 est remboursée en moins d'une minute). Voir l'économie recalibrée dans `economie.md`.

## 7. ✅ Fait le 13/11/2026 (phase 1 + mode « Ma vie » sans famille)
- Dessins Kenney posés pile sur la case (`assets/monde/*.png`, composés par script depuis les packs) : maisonnette, maison, villa (toits en pente), magasin, restaurant, pharmacie, école, cinéma, salle d'arcade, **hôpital, garage** (nouveaux), potager, poulailler, enclos vaches (animaux animés par-dessus). Panneaux lisibles (✚ pharmacie verte, ✚ hôpital rouge, 🔧, 🎬, 🕹️, 👗, 🍔, P).
- **Parking** (nouveau), **routes** avec marquage pointillé dans le sens de la route, **voitures orientées** (taxi, police, ambulance — plus de voitures « en crabe »).
- Casino → **Salle d'arcade 🕹️**.
- Image nette sur écran haute densité ; la barre d'outils n'est plus cachée par la barre du bas.
- **Mode « 🚶 Ma vie »** (bouton en haut) : l'avatar du profil vit dans la ville. Toucher un bâtiment → il y va (plus court chemin à pied, par les routes et l'herbe) et fait l'action : repas (−10 🪙, faim), dodo (énergie), manèges/cinéma/zoo (joie, payant), récolte/traite/œufs (« travailler » : récolte +25 %), soins…
- **3 jauges** faim / énergie / joie qui baissent doucement ; sous 30 → bulle d'envie au-dessus de l'avatar + bouton « J'ai faim ! Aller manger ».
- **3 missions de Sensei par jour** choisies parmi les bâtiments construits (+20 🪙 chacune, +30 🪙 bonus les 3) ; s'il manque des bâtiments : « Construis… ».
- **Quartier libre** : l'avatar choisit seul où aller (en priorité selon ses envies).
- La caméra suit l'avatar (on peut quand même déplacer la vue au doigt).
- Reste à faire : manèges plus distinctifs et animés, ponts hauts (bateaux dessous), cultures variées (carottes, salades, tomates, arbres fruitiers), familles (5 personnages), économie recalibrée, un monde par profil.
