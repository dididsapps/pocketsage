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

## 8. ✅ Fait le 13/11/2026 (suite)
- **Manèges animés** sur une place pavée : grande roue (nacelles qui restent droites, ampoules qui clignotent), carrousel (toit rayé qui tourne, chevaux qui montent et descendent), 3 grands 8 avec un vrai petit train qui suit les rails (8 à bosses ; ovale avec looping ; montée lente puis spirale), toboggans aquatiques (glisseurs + éclaboussures).
- **Ponts hauts** : tablier surélevé avec rampes d'accès, piles en pierre, arche, garde-corps et lampadaire. Les bateaux passent dessous ; voitures et avatar montent dessus.
- **Cultures variées** (Production) : salades, carottes, blé, tomates, fraises, citrouilles, pommier (+ maïs = ancien « Potager »). Elles poussent pendant le cycle de récolte et sont mûres quand le 💰 apparaît. Actions et missions « Ma vie » associées.
- Correctif : après rechargement de la page, les revenus reprenaient seulement après un long moment (compteur de temps remis à zéro) → corrigé.

## 9. ✅ Fait le 13/11/2026 (grands bâtiments + enclos)
- **Bâtiments sur plusieurs cases** (vraiment occupées, effet 3D droit) : Château 2×2 (nouveau, 500 🪙, +75), Villa californienne 2×1 (toits plats, baies vitrées, piscine, palmiers), Hôpital 3×2 (héliport, auvent, ambulance), Cinéma 3×2 (marquise lumineuse, affiches, enseigne verticale, projecteurs), Supermarché 3×2 (nouveau, auvent rayé, caddies).
- Pose : la case touchée est mise au centre du bâtiment ; s'il manque de la place → « Il faut 3×2 cases libres ». La gomme efface tout le bâtiment ; l'avatar y entre par la case la plus proche.
- Anciennes sauvegardes : une villa/hôpital/cinéma déjà posé prend sa nouvelle taille si les cases autour sont libres, sinon il garde son ancien dessin sur 1 case.
- **Enclos vaches et poulaillers reliés** : les cases posées côte à côte forment un seul enclos, la clôture fait le tour du groupe (comme les routes qui se raccordent), avec une botte de foin (vaches) ou une cabane (poules) au milieu.
- **Zoo 10×10** (1000 🪙, +150) : prairie, étang avec flamants roses, rochers, arbres, chemin de sable, clôture tout autour avec portail « ZOO » ; lions, girafes, éléphants, zèbres, flamants qui se promènent.
- **Immeubles 3×3** (Habitat) : Immeuble 3 étages (briques, balcons, toit en pente — 300 🪙), Immeuble 10 étages (réservoir d'eau, antenne — 700 🪙), Tour moderne vitrée rectangulaire avec reflets (900 🪙), Burj Khalifa ~4× plus haut, à étages en retrait, flèche et fontaine (3000 🪙, +400).
- **Hôtels** (nouvel onglet) : Hôtel lagon 10×10 (bungalows sur pilotis reliés par un ponton, lagon turquoise, lodge au toit de paille, piscine, palmiers, parasols, kayak — 2500 🪙), Hôtel Voile 3×3 (gratte-ciel en forme de voile sur son île, héliport — 2000 🪙), Hôtel Atlantis 5×5 (2 tours roses reliées par une arche, dômes dorés, ailes basses, piscine, plage — 3500 🪙).
- **Sport** (nouvel onglet) : Tennis 2×1 et Padel 2×1 (grillage autour de chaque terrain, vitres au fond du padel, échange animé), Terrain de foot 4×2 avec tribune et spectateurs, Grand stade 6×6 type Stade de France (gradins bleu-blanc-rouge, toit, match en cours), Baseball 4×4 (losange, monticule, lancer animé), Piste d'athlétisme 4×3 (6 couloirs, coureurs).

## 10. ✅ Intérieurs (13/11/2026) — « 3 couches » : ville → bâtiment en coupe → pièce
- En mode « Ma vie », toucher une maison/immeuble, le resto, la boutique, le supermarché, l'hôpital, la pharmacie, l'école ou un hôtel : l'avatar y va et **entre**. Vue en coupe façon Les Sims (murs du fond, cloisons coupées), boutons de pièces pour zoomer (Salon, Cuisine, Chambre…), pincer/glisser pour zoomer/déplacer.
- Meubles : Kenney Furniture Kit, Mini Shop, Food Kit (CC0) **rendus en isométrique par notre propre script** (`render3d.py`, scratchpad) à partir des modèles 3D → `assets/interieur/*.webp` (~200 Ko) + `sprites.json` (ancre, emprise). Recolorable à volonté.
- Plans + actions : `data/interieurs.json` (généré par `layouts.py`). Chaque meuble peut avoir une action (faim/énergie/joie/pièces, pose, durée). Le bureau et les pupitres proposent d'ouvrir une activité (Maths, Sciences, Langues, Politesse).
- Avatar Andrew : planches ChatGPT découpées (fond retiré, pieds alignés) → `assets/interieur/andrew_walk_front|walk_back|poses.webp`, 4 directions par miroir, poses assis/dodo/manger/coucou/saut. Utilisé aussi dans la ville. Les autres avatars : image fixe en attendant leurs planches.
- Moteur : `js/monde-interieur.js`.
- **Mode Déco** (maison) : bouton 🛋️ Déco → catalogue (Salon, Cuisine, Chambre, Salle de bain ; ~50 meubles), 5 couleurs pour canapés/fauteuils/lits/tapis, poser au sol ou SUR un meuble (télé sur le meuble TV, ordinateur sur le bureau, lampe sur la table de nuit…), ↻ tourner, ✋ déplacer, 🗑️ vendre (moitié du prix). La déco est gardée par maison (dans la sauvegarde de la ville).
- Toucher un bâtiment : en mode 🏗️ Construire = ramasser l'argent ; en mode 🚶 Ma vie = Andrew y va et entre (l'argent est ramassé automatiquement en entrant).
- École : les élèves regardent le tableau (tableau transparent sur le mur avant, côté bas-gauche).
- **Fiche bâtiment** : 1er toucher = surbrillance + fiche (rapport par récolte et par minute, gains depuis la construction, à récolter, meubles ajoutés) avec 💰 Récolter / 🚪 Entrer / 🚶 Y aller / ⭐ C'est ma maison / ✏️ Nom ; 2e toucher = récolter (mode Construire) ou y aller et entrer (mode Ma vie). Badges ⭐ (ma maison, Andrew y va dormir) et 🛋️ (décorée). Liste « 🏘️ Mes bâtiments » dans le 📊 avec bouton 👁️ Voir. Compteur de gains par bâtiment à partir du 13/11/2026.
- **Intérieurs de luxe** : Villa (blanc/noir/or, baies vitrées, piano, piscine intérieure, palmier), Suite royale des hôtels Voile/Burj (marbre noir veiné d'or, velours, lustres en cristal, vue mer), Palais des mers de l'Atlantis (baroque : papier peint damassé, damier, colonnes, cheminée, tableaux, miroir doré, **aquarium géant animé**), Château (baroque bleu royal, parquet en chevrons, cheminée, bibliothèques dorées ; décorable), Bungalow du lagon (teck, rotin, baies sur le lagon, **plancher de verre avec poissons**). Styles de matières : or, blanc, noir, velours, royal, rotin (recoloration des modèles 3D).

## 11. ✅ Jeux dans la ville (13/11/2026) — `js/monde-plus.js`
- Boutons sur la carte (à droite) : 📋 Commandes · 📖 Album · 👨‍👩‍👧 Famille · 🐾 Animal · 📸 Photo.
- **Stock** : chaque récolte de champ/enclos donne des produits (🌽🌾🥕🍅🥬🍓🎃🍎🥛🥚).
- **Commandes à livrer** (style Hay Day) : 3 clients, livrer puis répondre à « Combien vaut la commande ? » (≥7 ans : prix × quantités ; <7 ans : nombre d'objets) → bonus.
- **Fabrication** (fiche du bâtiment → 🏭) : moulin (farine), boulangerie (pain, croissant, gâteau), laiterie (beurre, fromage), pizzeria (pizza), glacier (glace), popcorn. Minuteurs de 20 à 60 s, ⏳/✅ au-dessus du bâtiment.
- **Nouveaux commerces** : Boulangerie, Laiterie, Pizzeria, Fleuriste ; décor de saison : Sapin de Noël, Lanternes.
- **Ateliers-métiers** (fiche → 🎯 Travailler, salaire) : Pizzaïolo (pizza vue de dessus, compter les garnitures), Cuisinier (burger dans l'ordre), Pâtissier (bougies = âge du client), Glacier (boules), Fleuriste (bouquet), Caissier (rendre la monnaie). Difficulté selon l'âge, bouton 🔊 pour écouter la commande.
- **Album** : pêche (toucher l'eau en Ma vie, tirer quand ça mord), insectes et fleurs trouvés en marchant dans l'herbe ; noms en 5 langues avec 🔊 ; onglet 📸 Photos (6 dernières).
- **Saisons / météo / jour-nuit** : heure réelle (soir orangé, nuit bleutée), pluie ou neige du jour (neige en hiver), sol légèrement blanchi en hiver.
- **Animal** : chien ou chat nommé, suit Andrew, à nourrir/caresser/jouer ; 🦴 quand il a faim.
- **Famille** (5 max) : rôle + prénom + image d'avatar ; ils se promènent autour de la maison ⭐ ; toucher = câlin / bonjour / aider.
- **Niveaux** : XP comptée en silence, interrupteur `LEVELS_ON=false` (à activer avant TestFlight).
- Reste à faire : planches des autres avatars, étages pour immeubles/hôtels, économie recalibrée, un monde par profil, renommer les lieux réels avant les stores.
