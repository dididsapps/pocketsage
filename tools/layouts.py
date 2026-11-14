"""Plans des intérieurs de Mon Monde -> data/interieurs.json
Repère : c = colonne (vers le bas-droite), r = ligne (vers le bas-gauche). Murs du fond : r=0 (haut-droit) et c=0 (haut-gauche).
rot : 0 = face vers +r (bas-gauche), 1 = face vers +c (bas-droite), 2 = face vers −r, 3 = face vers −c.
Préfixes : shop: = Mini Shop, food: = Food Kit, sinon Furniture Kit.
"""
import json
def I(m, c, r, rot=0, z=0, act=None, deco=False, flat=False):
    d = {'m': m, 'c': c, 'r': r, 'rot': rot}
    if z: d['z'] = z
    if act: d['act'] = act
    if deco: d['deco'] = 1
    if flat: d['flat'] = 1
    return d
SOFA = {'t': 'Se détendre sur le canapé 🛋️', 'j': 15, 'e': 5, 'pose': 'sit', 'dur': 3}
TV = {'t': 'Regarder la télé 📺', 'j': 20, 'pose': 'sit', 'dur': 3}
FRIDGE = {'t': 'Prendre un goûter 🍎', 'f': 20, 'pose': 'eat', 'dur': 2.5}
STOVE = {'t': 'Cuisiner un bon plat 🍳', 'f': 30, 'pose': 'idle', 'dur': 3}
EAT = {'t': 'Manger à table 🍽️', 'f': 35, 'pose': 'eat', 'dur': 3}
BED = {'t': 'Faire dodo 😴', 'e': 60, 'pose': 'sleep', 'dur': 4}
DESK = {'t': 'Faire une activité ✏️', 'j': 10, 'pose': 'sit', 'dur': 2, 'module': 1}
READ = {'t': 'Lire un livre 📚', 'j': 12, 'pose': 'idle', 'dur': 3}
BATH = {'t': 'Prendre un bain 🛁', 'j': 10, 'e': 10, 'pose': 'idle', 'dur': 3}
WC = {'t': 'Passer aux toilettes 🚽', 'j': 3, 'pose': 'idle', 'dur': 1.5}
WASH = {'t': 'Se laver les mains 🧼', 'j': 3, 'pose': 'idle', 'dur': 1.5}
TOY = {'t': 'Jouer avec le nounours 🧸', 'j': 18, 'pose': 'jump', 'dur': 2.5}
MUSIC = {'t': 'Danser en musique 🎵', 'j': 15, 'e': -5, 'pose': 'jump', 'dur': 3}

L = {}
# ── Maison (salon, cuisine, chambre, salle de bain) ──────────────────────
L['maison'] = {
    'nom': 'Ma maison', 'deco': 1, 'w': 8, 'h': 7, 'mur': '#f4efe6', 'murHaut': '#e2a56b', 'porte': [0, 2],
    'sols': [[0, 0, 4, 4, 'bois'], [4, 0, 8, 4, 'carreau'], [0, 4, 4, 7, 'moquette'], [4, 4, 8, 7, 'carreauBleu']],
    'cloisons': [['c', 4, 0, 4, [2]], ['r', 4, 0, 8, [2, 6]], ['c', 4, 4, 7, []]],
    'pieces': [['Salon', 2, 2], ['Cuisine', 6, 1.5], ['Chambre', 2, 5.5], ['Salle de bain', 6, 5.5]],
    'items': [
        I('rugRound', 1, 1, flat=True),
        I('loungeSofa', 1, 0, 0, act=SOFA), I('tableCoffee', 1, 1), I('pottedPlant', 0, 0), I('lampRoundFloor', 3, 0),
        I('bookcaseOpen', 0, 1, 1, act=READ), I('loungeChair', 3, 1, 3, act=SOFA),
        I('cabinetTelevision', 0, 3, 2), I('televisionModern', 0, 3, 2, z=0.53, deco=True, act=TV), I('speaker', 3, 3, 2, act=MUSIC),
        I('kitchenFridgeLarge', 4, 0, 0, act=FRIDGE), I('kitchenCabinetDrawer', 5, 0), I('kitchenStove', 6, 0, 0, act=STOVE), I('kitchenSink', 7, 0, 0, act=WASH),
        I('kitchenCoffeeMachine', 5, 0, 0, z=0.77, deco=True), I('hoodModern', 6, 0, 0, z=1.6, deco=True),
        I('table', 5, 2, 0, act=EAT), I('chair', 5, 1, 0), I('chair', 6, 3, 2), I('chair', 7, 2, 3),
        I('food:bowl-cereal', 5, 2, 0, z=0.56, deco=True),
        I('bedSingle', 0, 4, 0, act=BED), I('cabinetBedDrawer', 1, 4), I('lampSquareTable', 1, 4, 0, z=0.44, deco=True),
        I('rugRounded', 1, 5, 0, flat=True), I('bear', 1, 6, 0, act=TOY),
        I('desk', 3, 5, 3, act=DESK), I('chairDesk', 2, 5, 1), I('laptop', 3, 5, 3, z=0.65, deco=True), I('bookcaseClosed', 3, 4, 0, act=READ),
        I('bathtub', 4, 4, 0, act=BATH), I('showerRound', 7, 4, 0, act=BATH), I('toilet', 4, 5, 1, act=WC),
        I('bathroomSinkSquare', 4, 6, 1, act=WASH), I('washer', 7, 6, 3), I('plantSmall1', 7, 5, 0),
    ]}
# ── Restaurant ─────────────────────────────────────────────────────────
RESTO = {'t': 'Manger au restaurant 🍔', 'f': 45, 'j': 5, 'c': 10, 'pose': 'eat', 'dur': 3}
JUS = {'t': 'Boire un jus au comptoir 🥤', 'f': 10, 'j': 10, 'c': 3, 'pose': 'sit', 'dur': 2}
L['resto'] = {
    'nom': 'Le restaurant', 'w': 8, 'h': 6, 'mur': '#f7e3c6', 'murHaut': '#b5472f', 'porte': [0, 4],
    'sols': [[0, 0, 8, 2, 'carreau'], [0, 2, 8, 6, 'boisFonce']],
    'cloisons': [],
    'pieces': [['Cuisine', 5.5, 0.6], ['Salle', 3, 3.5]],
    'items': [
        I('kitchenStove', 4, 0), I('kitchenStove', 5, 0), I('kitchenFridgeLarge', 7, 0), I('kitchenSink', 6, 0), I('hoodModern', 4, 0, 0, z=1.6, deco=True), I('hoodModern', 5, 0, 0, z=1.6, deco=True),
        I('kitchenBar', 4, 1, 2), I('kitchenBar', 5, 1, 2), I('kitchenBar', 6, 1, 2), I('kitchenBar', 7, 1, 2),
        I('food:burger', 5, 1, 0, z=0.71, deco=True), I('food:fries', 6, 1, 0, z=0.71, deco=True),
        I('stoolBar', 4, 2, 2, act=JUS), I('stoolBar', 5, 2, 2, act=JUS), I('stoolBar', 6, 2, 2, act=JUS),
        I('shop:character-employee', 1, 0, 0, deco=False), I('shop:cash-register', 2, 0, 0),
        I('tableCloth', 1, 3, 0, act=RESTO), I('chair', 1, 2, 0), I('chair', 2, 4, 2), I('food:pizza', 1, 3, 0, z=0.56, deco=True),
        I('tableCloth', 4, 4, 0, act=RESTO), I('chair', 4, 3, 0), I('chair', 5, 5, 2), I('food:burger-cheese', 4, 4, 0, z=0.56, deco=True),
        I('tableRound', 7, 3, 0, act=RESTO), I('chair', 6, 3, 1), I('chair', 6, 4, 1), I('food:cake', 7, 3, 0, z=0.17, deco=True),
        I('pottedPlant', 0, 5), I('pottedPlant', 7, 5), I('rugDoormat', 0, 4, 1, flat=True),
    ]}
# ── Boutique de vêtements ──────────────────────────────────────────────
HABITS = {'t': 'Essayer des vêtements 👕', 'j': 20, 'c': 12, 'pose': 'wave', 'dur': 2.5}
L['boutique'] = {
    'nom': 'La boutique', 'w': 7, 'h': 6, 'mur': '#fdf1f4', 'murHaut': '#e06c9f', 'porte': [0, 4],
    'sols': [[0, 0, 7, 6, 'clair']], 'cloisons': [], 'pieces': [['Vêtements', 3, 2.5]],
    'items': [
        I('shop:mannequin', 0, 0), I('shop:clothing-rack', 1, 0, act=HABITS), I('shop:clothing-rack', 2, 0, act=HABITS), I('shop:clothing-rack', 4, 0, act=HABITS), I('shop:mannequin', 6, 0),
        I('shop:clothing-table', 2, 2, act=HABITS), I('shop:clothing-table', 4, 2, act=HABITS), I('shop:clothing-rack', 0, 2, 1, act=HABITS),
        I('shop:display-small', 6, 2), I('coatRackStanding', 6, 3), I('shop:cash-register', 5, 4, 3), I('shop:character-employee', 6, 4, 3),
        I('loungeChair', 2, 5, 2, act=SOFA), I('pottedPlant', 0, 5), I('rugRound', 3, 3, flat=True),
    ]}
# ── Supermarché ───────────────────────────────────────────────────────
COURSES = {'t': 'Faire les courses 🛒', 'f': 35, 'c': 8, 'pose': 'idle', 'dur': 2.5}
FRUITS = {'t': 'Acheter des fruits 🍎', 'f': 25, 'c': 5, 'pose': 'eat', 'dur': 2}
GLACE = {'t': 'Choisir une glace 🍦', 'f': 10, 'j': 12, 'c': 3, 'pose': 'eat', 'dur': 2}
L['supermarche'] = {
    'nom': 'Le supermarché', 'w': 9, 'h': 7, 'mur': '#eef6ee', 'murHaut': '#2b9348', 'porte': [0, 5],
    'sols': [[0, 0, 9, 7, 'lino']], 'cloisons': [], 'pieces': [['Rayons', 4, 2.5], ['Caisses', 6.5, 5.6]],
    'items': [
        I('shop:freezers-standing', 1, 0, act=GLACE), I('shop:freezers-standing', 2, 0, act=GLACE), I('shop:freezers-standing', 3, 0, act=GLACE),
        I('shop:display-cans', 5, 0, act=COURSES), I('shop:display-cans', 6, 0, act=COURSES), I('shop:shelf-end', 8, 0, 3),
        I('shop:shelf-boxes', 2, 2, act=COURSES), I('shop:shelf-bags', 3, 2, act=COURSES), I('shop:shelf-boxes', 4, 2, act=COURSES), I('shop:shelf-bags', 5, 2, act=COURSES),
        I('shop:shelf-bags', 2, 3, 2, act=COURSES), I('shop:shelf-boxes', 3, 3, 2, act=COURSES), I('shop:shelf-bags', 4, 3, 2, act=COURSES), I('shop:shelf-boxes', 5, 3, 2, act=COURSES),
        I('shop:display-fruit', 1, 5, act=FRUITS), I('shop:display-bread', 2, 5, act=FRUITS), I('shop:display-flowers', 3, 6),
        I('shop:freezer', 7, 2, 3, act=GLACE),
        I('shop:cash-register', 6, 5, 3), I('shop:cash-register', 8, 5, 3), I('shop:character-employee', 7, 5, 3),
        I('shop:shopping-cart', 1, 6, 1), I('shop:shopping-cart', 0, 6, 1), I('shop:shopping-basket', 5, 6, 0),
    ]}
# ── Hôpital ───────────────────────────────────────────────────────────
SOIN = {'t': 'Se faire soigner 🩺', 'e': 40, 'j': 5, 'pose': 'sleep', 'dur': 4}
ACCUEIL = {'t': "Parler à l'accueil 💬", 'j': 5, 'pose': 'wave', 'dur': 1.5}
L['hopital'] = {
    'nom': "L'hôpital", 'w': 9, 'h': 7, 'mur': '#ffffff', 'murHaut': '#4ea8de', 'porte': [0, 5],
    'sols': [[0, 0, 4, 7, 'lino'], [4, 0, 9, 7, 'blancBleu']],
    'cloisons': [['c', 4, 0, 7, [4]], ['r', 3, 4, 9, [6]]],
    'pieces': [['Accueil', 2, 3], ['Chambres', 6.5, 1.3], ['Soins', 6.5, 5]],
    'items': [
        I('deskCorner', 1, 1, 0, act=ACCUEIL), I('computerScreen', 1, 1, 0, z=0.65, deco=True), I('chairDesk', 1, 0, 0), I('shop:character-employee', 2, 0, 0),
        I('benchCushion', 0, 3, 1, act=SOFA), I('benchCushion', 0, 4, 1, act=SOFA), I('pottedPlant', 3, 0), I('shop:gacha-machine', 3, 6),
        I('bedSingle', 4, 0, 0, act=SOIN), I('sideTable', 5, 0), I('bedSingle', 6, 0, 0, act=SOIN), I('sideTable', 7, 0), I('bedSingle', 8, 0, 0, act=SOIN),
        I('lampSquareTable', 5, 0, 0, z=0.65, deco=True), I('food:apple', 7, 0, 0, z=0.65, deco=True),
        I('bedSingle', 5, 5, 0, act=SOIN), I('desk', 7, 3, 0), I('computerScreen', 7, 3, 0, z=0.65, deco=True), I('chairDesk', 7, 4, 2), I('bathroomSinkSquare', 8, 3, 0, act=WASH),
    ]}
# ── Hôtel (suite) ─────────────────────────────────────────────────────
ROOM = {'t': 'Room service 🍽️', 'f': 40, 'j': 10, 'c': 8, 'pose': 'eat', 'dur': 3}
L['hotel'] = {
    'nom': 'La suite de l’hôtel', 'w': 8, 'h': 7, 'mur': '#f5efe4', 'murHaut': '#c9a227', 'porte': [0, 2],
    'sols': [[0, 0, 5, 7, 'moquetteBeige'], [5, 0, 8, 7, 'marbre']],
    'cloisons': [['c', 5, 0, 7, [3]]],
    'pieces': [['Suite', 2.5, 3.5], ['Salle de bain', 6.5, 3.5]],
    'items': [
        I('bedDouble', 1, 0, 0, act=BED), I('cabinetBedDrawer', 0, 0), I('cabinetBedDrawer', 3, 0), I('lampSquareTable', 0, 0, 0, z=0.44, deco=True), I('lampSquareTable', 3, 0, 0, z=0.44, deco=True),
        I('rugRectangle', 1, 3, 0, flat=True), I('loungeSofa~bleu', 1, 5, 2, act=SOFA), I('tableCoffeeGlass', 1, 4, 0, act=ROOM), I('food:cake', 1, 4, 0, z=0.39, deco=True),
        I('cabinetTelevision', 4, 4, 3), I('televisionModern', 4, 4, 3, z=0.53, deco=True, act=TV), I('loungeChairRelax', 0, 4, 1, act=SOFA), I('pottedPlant', 4, 6), I('pottedPlant', 0, 6),
        I('bathtub', 5, 0, 0, act=BATH), I('showerRound', 7, 1, 3, act=BATH), I('bathroomSinkSquare', 5, 5, 1, act=WASH), I('toilet', 7, 5, 3, act=WC), I('plantSmall2', 7, 6),
    ]}
# ── École ─────────────────────────────────────────────────────────────
PROF = {'t': 'Parler à Sensei 🥋', 'j': 8, 'pose': 'wave', 'dur': 2}
L['ecole'] = {
    'nom': "L'école", 'w': 8, 'h': 7, 'mur': '#fff8e7', 'murHaut': '#f4a261', 'porte': [0, 1], 'tableauAvant': [2, 6],
    'sols': [[0, 0, 8, 7, 'bois']], 'cloisons': [], 'pieces': [['Classe', 4, 3.5]],
    'items': [
        I('chairDesk', 2, 1, 0), I('desk', 2, 2, 0, act=DESK), I('chairDesk', 4, 1, 0), I('desk', 4, 2, 0, act=DESK), I('chairDesk', 6, 1, 0), I('desk', 6, 2, 0, act=DESK),
        I('chairDesk', 2, 3, 0), I('desk', 2, 4, 0, act=DESK), I('chairDesk', 4, 3, 0), I('desk', 4, 4, 0, act=DESK), I('chairDesk', 6, 3, 0), I('desk', 6, 4, 0, act=DESK),
        I('laptop', 4, 2, 0, z=0.65, deco=True), I('food:apple', 2, 4, 0, z=0.65, deco=True),
        I('desk', 5, 6, 2, act=PROF), I('shop:character-employee', 5, 5, 0), I('food:apple', 5, 6, 0, z=0.65, deco=True),
        I('bookcaseOpen', 0, 3, 1, act=READ), I('bookcaseOpen', 0, 4, 1, act=READ), I('bookcaseClosedWide', 0, 5, 1, act=READ), I('pottedPlant', 7, 0), I('shop:gacha-machine', 0, 0, 1),
    ]}
# ── Pharmacie ─────────────────────────────────────────────────────────
VITA = {'t': 'Acheter des vitamines 💊', 'e': 10, 'j': 5, 'c': 5, 'pose': 'idle', 'dur': 2}
L['pharmacie'] = {
    'nom': 'La pharmacie', 'w': 6, 'h': 5, 'mur': '#f1fbf4', 'murHaut': '#2a9d8f', 'porte': [0, 3],
    'sols': [[0, 0, 6, 5, 'blancBleu']], 'cloisons': [], 'pieces': [['Pharmacie', 3, 2.5]],
    'items': [
        I('shop:shelf-boxes', 1, 0, act=VITA), I('shop:shelf-boxes', 2, 0, act=VITA), I('shop:shelf-bags', 3, 0, act=VITA), I('shop:shelf-boxes', 4, 0, act=VITA),
        I('kitchenBar', 2, 2, 0), I('kitchenBar', 3, 2, 0), I('shop:cash-register', 4, 2, 0), I('shop:character-employee', 4, 1, 0),
        I('shop:display-small', 5, 4, 3, act=VITA), I('benchCushion', 1, 4, 2, act=SOFA), I('pottedPlant', 0, 0),
    ]}
COUL = {'bleu': '#3a6ea5', 'vert': '#52b788', 'jaune': '#f4c430', 'rose': '#f78fb3'}
CATALOGUE = [
  # [modèle, nom, prix, catégorie, options]
  ['loungeSofa', 'Canapé', 40, 'Salon', {'c': 1}], ['loungeSofaCorner', 'Canapé d’angle', 60, 'Salon', {'c': 1}], ['loungeChair', 'Fauteuil', 25, 'Salon', {'c': 1}],
  ['loungeChairRelax', 'Fauteuil relax', 35, 'Salon', {'c': 1}], ['tableCoffee', 'Table basse', 15, 'Salon', {}], ['tableCoffeeGlass', 'Table basse verre', 20, 'Salon', {}],
  ['cabinetTelevision', 'Meuble TV', 20, 'Salon', {}], ['televisionModern', 'Télé', 50, 'Salon', {'s': 1}], ['televisionVintage', 'Vieille télé', 30, 'Salon', {'s': 1}],
  ['bookcaseOpen', 'Étagère', 25, 'Salon', {}], ['bookcaseClosedWide', 'Bibliothèque', 35, 'Salon', {}], ['lampRoundFloor', 'Lampadaire', 12, 'Salon', {}],
  ['speaker', 'Enceinte', 20, 'Salon', {}], ['radio', 'Radio', 10, 'Salon', {'s': 1}], ['pottedPlant', 'Grande plante', 8, 'Salon', {}], ['plantSmall1', 'Petite plante', 4, 'Salon', {'s': 1}],
  ['rugRound', 'Tapis rond', 10, 'Salon', {'c': 1, 'flat': 1}], ['rugRectangle', 'Grand tapis', 15, 'Salon', {'c': 1, 'flat': 1}], ['bear', 'Nounours', 10, 'Salon', {}],
  ['kitchenFridgeLarge', 'Grand frigo', 50, 'Cuisine', {}], ['kitchenFridge', 'Frigo', 40, 'Cuisine', {}], ['kitchenStove', 'Cuisinière', 35, 'Cuisine', {}],
  ['kitchenSink', 'Évier', 25, 'Cuisine', {}], ['kitchenCabinetDrawer', 'Meuble de cuisine', 15, 'Cuisine', {}], ['kitchenBar', 'Comptoir', 15, 'Cuisine', {}],
  ['kitchenCoffeeMachine', 'Machine à café', 12, 'Cuisine', {'s': 1}], ['kitchenMicrowave', 'Micro-ondes', 12, 'Cuisine', {'s': 1}], ['table', 'Table', 25, 'Cuisine', {}],
  ['tableRound', 'Table ronde', 25, 'Cuisine', {}], ['chair', 'Chaise', 8, 'Cuisine', {}], ['chairCushion', 'Chaise coussin', 10, 'Cuisine', {'c': 1}], ['stoolBar', 'Tabouret', 8, 'Cuisine', {}],
  ['bedSingle', 'Lit', 40, 'Chambre', {'c': 1}], ['bedDouble', 'Grand lit', 70, 'Chambre', {'c': 1}], ['bedBunk', 'Lits superposés', 60, 'Chambre', {'c': 1}],
  ['cabinetBedDrawer', 'Table de nuit', 12, 'Chambre', {}], ['lampSquareTable', 'Lampe de chevet', 6, 'Chambre', {'s': 1}], ['desk', 'Bureau', 25, 'Chambre', {}],
  ['chairDesk', 'Chaise de bureau', 15, 'Chambre', {}], ['laptop', 'Ordinateur portable', 30, 'Chambre', {'s': 1}], ['computerScreen', 'Écran', 25, 'Chambre', {'s': 1}],
  ['bookcaseClosed', 'Armoire', 25, 'Chambre', {}], ['coatRackStanding', 'Portemanteau', 8, 'Chambre', {}],
  ['bathtub', 'Baignoire', 50, 'Salle de bain', {}], ['showerRound', 'Douche', 45, 'Salle de bain', {}], ['toilet', 'Toilettes', 20, 'Salle de bain', {}],
  ['bathroomSinkSquare', 'Lavabo', 15, 'Salle de bain', {}], ['washer', 'Lave-linge', 30, 'Salle de bain', {}], ['dryer', 'Sèche-linge', 30, 'Salle de bain', {}], ['trashcan', 'Poubelle', 4, 'Salle de bain', {}],
]
SURFACES = ['tableCoffee', 'tableCoffeeGlass', 'cabinetTelevision', 'kitchenCabinetDrawer', 'kitchenCabinet', 'kitchenBar', 'table', 'tableRound', 'tableCloth', 'cabinetBedDrawer', 'cabinetBed', 'desk', 'deskCorner', 'sideTable']
# ── Styles de matières (recoloration des modèles 3D) ──────────────────
STYLES = {
  'or':      {'wood': '#d4af37', 'woodDark': '#8a6d1f', 'metal': '#e8c766', 'metalDark': '#b8932f', 'metalMedium': '#cfae4f', 'metalLight': '#f0d98a', 'carpet': '#f7f3ea', 'carpetBlue': '#f7f3ea'},
  'blanc':   {'wood': '#f4f1ea', 'woodDark': '#2b2b2b', 'carpet': '#f2f2f0', 'carpetBlue': '#e8e8e6', 'metal': '#c9a227', 'metalDark': '#1f1f1f'},
  'noir':    {'wood': '#1f1f22', 'woodDark': '#111114', 'carpet': '#2b2b30', 'carpetWhite': '#f5f5f5', 'carpetBlue': '#2b2b30', 'metal': '#d4af37', 'metalDark': '#b8932f', 'metalMedium': '#d4af37', 'metalLight': '#e8c766'},
  'velours': {'carpet': '#7b1e3a', 'carpetBlue': '#7b1e3a', 'carpetWhite': '#f8f0dc', 'wood': '#c9a227', 'woodDark': '#5a2d0c', 'metal': '#d4af37', 'metalDark': '#b8932f'},
  'royal':   {'carpet': '#1d3a7a', 'carpetBlue': '#1d3a7a', 'carpetWhite': '#f8f0dc', 'wood': '#d4af37', 'woodDark': '#6b4a12', 'metal': '#d4af37', 'metalDark': '#b8932f'},
  'rotin':   {'wood': '#d9b98c', 'woodDark': '#a5794a', 'carpet': '#f5efe3', 'carpetBlue': '#7fd3d8', 'carpetWhite': '#fffdf6', 'metal': '#c9b38a'},
}
BAIN = {'t': 'Piquer une tête dans la piscine 🏊', 'j': 25, 'e': -5, 'pose': 'jump', 'dur': 3}
PIANO = {'t': 'Jouer du piano 🎹', 'j': 20, 'pose': 'sit', 'dur': 3}
FEU = {'t': 'Se réchauffer au coin du feu 🔥', 'j': 12, 'e': 10, 'pose': 'sit', 'dur': 3}
AQUA = {'t': 'Admirer les poissons 🐠', 'j': 20, 'pose': 'wave', 'dur': 3}
COCKTAIL = {'t': 'Un cocktail de fruits 🍹', 'f': 15, 'j': 15, 'c': 6, 'pose': 'eat', 'dur': 2.5}
def P_(m, c, r, fw=1, fh=1, act=None, **k):
    d = {'m': '@' + m, 'c': c, 'r': r, 'rot': 0, 'fw': fw, 'fh': fh}
    if act: d['act'] = act
    d.update(k); return d
# ── Villa californienne (moderne, blanc / noir / or) ──
L['villa'] = {
    'nom': 'La villa', 'deco': 1, 'w': 9, 'h': 7, 'mur': '#fbfbf8', 'murHaut': '#2b2b2b', 'porte': [0, 2],
    'sols': [[0, 0, 9, 4, 'marbreBlanc'], [0, 4, 5, 7, 'moquetteBeige'], [5, 4, 9, 7, 'tek']],
    'cloisons': [['r', 4, 0, 5, [2]], ['c', 5, 4, 7, [4]]],
    'pieces': [['Salon', 2.5, 2], ['Cuisine', 7.2, 1.5], ['Chambre', 2.5, 5.5], ['Piscine', 7, 5.5]],
    'murDeco': [['baie', 'r', 1, 8.6, {}], ['tableau', 'c', 4.4, 5.8, {'z0': 22, 'z1': 44}]],
    'lustres': [[2.5, 2, 'moderne'], [7.2, 2, 'moderne']],
    'items': [
        I('rugRectangle~noir', 1, 1, flat=True),
        I('loungeSofa~blanc', 1, 0, 2, act=SOFA), I('loungeSofa~blanc', 3, 0, 2, act=SOFA),
        I('tableCoffeeGlass', 2, 1, 0, act=COCKTAIL), I('food:cocktail', 2, 1, 0, z=0.39, deco=True), I('loungeChairRelax~noir', 4, 1, 3, act=SOFA),
        I('cabinetTelevision~noir', 0, 3, 2), I('televisionModern', 0, 3, 2, z=0.53, deco=True, act=TV), I('lampSquareFloor~or', 0, 0), I('pottedPlant', 0, 1),
        P_('piano', 4, 2, act=PIANO),
        I('kitchenSink~noir', 6, 0, 0, act=WASH), I('kitchenStove~noir', 7, 0, 0, act=STOVE), I('kitchenFridgeLarge', 8, 0, 0, act=FRIDGE), I('hoodModern~noir', 7, 0, 0, z=1.6, deco=True),
        I('kitchenBar~noir', 6, 2, 2, act=EAT), I('kitchenBar~noir', 7, 2, 2, act=EAT), I('kitchenBar~noir', 8, 2, 2), I('food:pineapple', 7, 2, 0, z=0.71, deco=True), I('food:cocktail', 6, 2, 0, z=0.71, deco=True),
        I('stoolBar~or', 6, 3, 2), I('stoolBar~or', 7, 3, 2), I('stoolBar~or', 8, 3, 2),
        I('bedDouble~blanc', 0, 4, 0, act=BED), I('cabinetBedDrawer~blanc', 0, 6), I('lampSquareTable~or', 0, 6, 0, z=0.44, deco=True),
        I('rugRound~noir', 2, 5, flat=True), I('desk~blanc', 4, 6, 3, act=DESK), I('chairDesk', 3, 6, 1), I('laptop', 4, 6, 3, z=0.65, deco=True), I('bookcaseClosed~blanc', 3, 4, 0, act=READ),
        P_('piscine', 5, 5, 3, 2, act=BAIN), I('loungeChairRelax~blanc', 6, 4, 0, act=SOFA), I('loungeChairRelax~blanc', 7, 4, 0, act=SOFA), P_('palmier', 8, 4),
    ]}
# ── Suite royale (hôtel Voile / Burj) : noir, or, velours ──
L['hotel_luxe'] = {
    'nom': 'La suite royale', 'w': 8, 'h': 7, 'mur': '#2b2731', 'murHaut': '#d4af37', 'porte': [0, 3], 'lambris': '#1d1a22',
    'sols': [[0, 0, 5, 7, 'marbreNoir'], [5, 0, 8, 7, 'marbreBlanc']],
    'cloisons': [['c', 5, 0, 7, [3]]],
    'pieces': [['Suite', 2.5, 3.5], ['Salle de bain', 6.5, 3.5]],
    'murDeco': [['baie', 'r', 0.4, 4.7, {'mer': 1}], ['miroir', 'r', 5.6, 7.4, {}], ['tableau', 'c', 4.2, 5.8, {'z0': 20, 'z1': 46}]],
    'lustres': [[2.5, 2.5, 'cristal'], [6.5, 3.5, 'cristal']],
    'items': [
        I('rugRound~velours', 1, 4, flat=True),
        I('bedDouble~or', 1, 0, 0, act=BED), I('cabinetBedDrawer~noir', 0, 0), I('cabinetBedDrawer~noir', 3, 0), I('lampSquareTable~or', 0, 0, 0, z=0.44, deco=True), I('lampSquareTable~or', 3, 0, 0, z=0.44, deco=True),
        I('loungeSofa~velours', 1, 6, 2, act=SOFA), I('tableCoffeeGlass', 1, 5, 0, act=COCKTAIL), I('food:cocktail', 1, 5, 0, z=0.39, deco=True),
        I('loungeChairRelax~velours', 3, 2, 3, act=SOFA), I('cabinetTelevision~noir', 4, 4, 3), I('televisionModern', 4, 4, 3, z=0.53, deco=True, act=TV),
        P_('piano', 4, 0, act=PIANO), P_('statue', 4, 6), I('pottedPlant', 0, 6),
        I('bathtub~or', 5, 0, 0, act=BATH), I('showerRound', 7, 2, 3, act=BATH), I('bathroomSinkSquare~or', 5, 5, 1, act=WASH), I('toilet', 7, 5, 3, act=WC), P_('palmier', 7, 6),
    ]}
# ── Palais baroque avec aquarium géant (hôtel des mers) ──
L['hotel_baroque'] = {
    'nom': 'Le palais des mers', 'w': 9, 'h': 7, 'mur': '#7b1e3a', 'murHaut': '#d4af37', 'motif': 'damas', 'lambris': '#4a0f22', 'porte': [0, 3],
    'sols': [[0, 0, 9, 7, 'damier']],
    'cloisons': [],
    'pieces': [['Chambre', 1.8, 1.5], ['Salon', 6, 3], ['Coin du feu', 1.5, 5]],
    'murDeco': [['aquarium', 'r', 4.2, 8.7, {}], ['miroir', 'r', 1.2, 2.6, {}], ['tableau', 'c', 0.6, 2.2, {'z0': 20, 'z1': 46}], ['tableau', 'c', 5.2, 6.6, {'z0': 22, 'z1': 44}]],
    'lustres': [[2, 2, 'cristal'], [6.5, 3.5, 'cristal']],
    'items': [
        I('rugRectangle~velours', 5, 4, flat=True),
        I('bedDouble~velours', 1, 0, 0, act=BED), I('cabinetBedDrawer~or', 0, 0), I('cabinetBedDrawer~or', 3, 0), I('lampSquareTable~or', 0, 0, 0, z=0.44, deco=True), I('lampSquareTable~or', 3, 0, 0, z=0.44, deco=True),
        I('loungeSofa~velours', 5, 3, 2, act=AQUA), I('loungeSofa~velours', 7, 3, 2, act=AQUA), I('tableCoffee~or', 6, 2, 0, act=COCKTAIL), I('food:cocktail', 6, 2, 0, z=0.39, deco=True),
        I('loungeChairRelax~velours', 4, 5, 2, act=SOFA), I('loungeChairRelax~velours', 8, 5, 2, act=SOFA),
        P_('cheminee', 0, 5, act=FEU), I('loungeChair~velours', 1, 4, 1, act=FEU), I('loungeChair~velours', 1, 6, 1, act=FEU),
        P_('colonne', 4, 0), P_('colonne', 3, 3), P_('colonne', 8, 6), P_('piano', 3, 6, act=PIANO), P_('statue', 8, 0),
    ]}
# ── Château (maison du joueur) : baroque bleu royal, parquet, cheminée ──
L['chateau'] = {
    'nom': 'Le château', 'deco': 1, 'w': 9, 'h': 7, 'mur': '#efe3c6', 'murHaut': '#8a6d1f', 'motif': 'damas', 'lambris': '#c9b48a', 'porte': [0, 3],
    'sols': [[0, 0, 9, 7, 'parquetChevron']],
    'cloisons': [['c', 5, 0, 7, [2, 5]]],
    'pieces': [['Grand salon', 2.5, 3.5], ['Chambre royale', 7, 3.5]],
    'murDeco': [['tableau', 'r', 0.6, 1.9, {}], ['tableau', 'r', 2.5, 3.8, {}], ['miroir', 'r', 6.2, 7.6, {}], ['tableau', 'c', 5, 6.4, {'z0': 20, 'z1': 46}]],
    'lustres': [[2.5, 3, 'cristal'], [7, 3, 'cristal']],
    'items': [
        I('rugRectangle~royal', 1, 2, flat=True),
        P_('cheminee', 0, 1, act=FEU), I('loungeSofa~royal', 1, 4, 2, act=SOFA), I('loungeChair~royal', 3, 2, 3, act=SOFA), I('tableCoffee~or', 2, 2, 0, act=COCKTAIL),
        I('bookcaseOpen~or', 1, 0, 0, act=READ), I('bookcaseOpen~or', 2, 0, 0, act=READ), P_('piano', 3, 5, act=PIANO), P_('colonne', 4, 0), P_('colonne', 4, 6), P_('statue', 0, 6),
        I('bedDouble~royal', 6, 0, 0, act=BED), I('cabinetBedDrawer~or', 5, 0), I('cabinetBedDrawer~or', 8, 0), I('lampSquareTable~or', 5, 0, 0, z=0.44, deco=True),
        I('bathtub~or', 8, 5, 3, act=BATH), I('desk~or', 8, 3, 3, act=DESK), I('chairCushion~royal', 7, 3, 1), I('pottedPlant', 8, 2), I('rugRound~royal', 6, 3, flat=True),
    ]}
# ── Bungalow sur pilotis (hôtel lagon) : bois clair, rotin, plancher de verre ──
L['hotel_lagon'] = {
    'nom': 'Le bungalow du lagon', 'w': 8, 'h': 7, 'mur': '#f3ead8', 'murHaut': '#a5794a', 'porte': [0, 2],
    'sols': [[0, 0, 8, 7, 'tek'], [3, 3, 5, 5, 'verre']],
    'cloisons': [['c', 6, 0, 7, [3]]],
    'pieces': [['Bungalow', 3, 3], ['Douche', 7, 3.5]],
    'murDeco': [['baie', 'r', 0.5, 5.6, {'lagon': 1}], ['baie', 'c', 3.6, 6.6, {'lagon': 1}]],
    'items': [
        I('bedDouble~rotin', 1, 0, 0, act=BED), I('cabinetBedDrawer~rotin', 0, 0), I('cabinetBedDrawer~rotin', 3, 0), I('lampSquareTable~or', 0, 0, 0, z=0.44, deco=True),
        I('ceilingFan', 2, 2, 0, z=2.1, deco=True),
        I('loungeSofa~rotin', 1, 5, 2, act=SOFA), I('tableCoffee~rotin', 1, 4, 0, act=COCKTAIL), I('food:coconut', 1, 4, 0, z=0.39, deco=True),
        I('loungeChairRelax~rotin', 5, 1, 3, act=SOFA), I('loungeChairRelax~rotin', 5, 5, 3, act=SOFA), P_('palmier', 0, 6), P_('palmier', 5, 0),
        I('showerRound', 7, 0, 3, act=BATH), I('bathroomSinkSquare~rotin', 6, 5, 1, act=WASH), I('toilet', 7, 6, 3, act=WC), I('plantSmall2', 7, 4),
    ]}
# bâtiments de la ville -> intérieur
BAT = {'house1': 'maison', 'house2': 'maison', 'house3': 'villa', 'apt3': 'maison', 'tower10': 'maison', 'tower_mod': 'maison', 'castle': 'chateau',
       'resto': 'resto', 'shop': 'boutique', 'supermarket': 'supermarche', 'hospital': 'hopital', 'pharmacy': 'pharmacie', 'school': 'ecole',
       'hotel_lagoon': 'hotel_lagon', 'hotel_sail': 'hotel_luxe', 'hotel_atlantis': 'hotel_baroque', 'burj': 'hotel_luxe'}
if __name__ == '__main__':
    import sys
    json.dump({'interieurs': L, 'batiments': BAT, 'catalogue': CATALOGUE, 'couleurs': COUL, 'styles': STYLES, 'surfaces': SURFACES, 'actions': {'SOFA': SOFA, 'TV': TV, 'FRIDGE': FRIDGE, 'STOVE': STOVE, 'EAT': EAT, 'BED': BED, 'DESK': DESK, 'READ': READ, 'BATH': BATH, 'WC': WC, 'WASH': WASH, 'TOY': TOY, 'MUSIC': MUSIC, 'BAIN': BAIN, 'PIANO': PIANO, 'FEU': FEU, 'AQUA': AQUA, 'COCKTAIL': COCKTAIL}}, open(sys.argv[1], 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    print('ok', len(L))
