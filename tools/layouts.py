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
    'nom': 'Ma maison', 'w': 8, 'h': 7, 'mur': '#f4efe6', 'murHaut': '#e2a56b', 'porte': [0, 2],
    'sols': [[0, 0, 4, 4, 'bois'], [4, 0, 8, 4, 'carreau'], [0, 4, 4, 7, 'moquette'], [4, 4, 8, 7, 'carreauBleu']],
    'cloisons': [['c', 4, 0, 4, [2]], ['r', 4, 0, 8, [2, 6]], ['c', 4, 4, 7, []]],
    'pieces': [['Salon', 2, 2], ['Cuisine', 6, 1.5], ['Chambre', 2, 5.5], ['Salle de bain', 6, 5.5]],
    'items': [
        I('rugRound', 1, 1, flat=True),
        I('loungeDesignSofa', 1, 0, 0, act=SOFA), I('tableCoffee', 1, 1), I('pottedPlant', 0, 0), I('lampRoundFloor', 3, 0),
        I('bookcaseOpen', 0, 1, 1, act=READ), I('loungeChair', 3, 1, 3, act=SOFA),
        I('cabinetTelevision', 1, 3, 2), I('televisionModern', 1, 3, 2, z=0.31, deco=True, act=TV), I('speaker', 3, 3, 2, act=MUSIC),
        I('kitchenFridgeLarge', 4, 0, 0, act=FRIDGE), I('kitchenCabinetDrawer', 5, 0), I('kitchenStove', 6, 0, 0, act=STOVE), I('kitchenSink', 7, 0, 0, act=WASH),
        I('kitchenCoffeeMachine', 5, 0, 0, z=0.45, deco=True), I('hoodModern', 6, 0, 0, z=0.95, deco=True),
        I('table', 5, 2, 0, act=EAT), I('chair', 5, 1, 0), I('chair', 5, 3, 2), I('chair', 6, 2, 3),
        I('food:bowl-cereal', 5, 2, 0, z=0.33, deco=True), I('food:apple', 5, 2, 0, z=0.33, deco=True),
        I('bedSingle', 0, 4, 0, act=BED), I('cabinetBedDrawer', 1, 4), I('lampSquareTable', 1, 4, 0, z=0.26, deco=True),
        I('rugRounded', 1, 5, 0, flat=True), I('bear', 1, 6, 0, act=TOY),
        I('desk', 3, 5, 3, act=DESK), I('chairDesk', 2, 5, 1), I('laptop', 3, 5, 3, z=0.38, deco=True), I('bookcaseClosed', 3, 4, 0, act=READ),
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
        I('kitchenStove', 4, 0), I('kitchenStove', 5, 0), I('kitchenFridgeLarge', 7, 0), I('kitchenSink', 6, 0), I('hoodModern', 4, 0, 0, z=0.95, deco=True), I('hoodModern', 5, 0, 0, z=0.95, deco=True),
        I('kitchenBar', 4, 1, 2), I('kitchenBar', 5, 1, 2), I('kitchenBar', 6, 1, 2), I('kitchenBar', 7, 1, 2),
        I('food:burger', 5, 1, 0, z=0.42, deco=True), I('food:fries', 6, 1, 0, z=0.42, deco=True),
        I('stoolBar', 4, 2, 2, act=JUS), I('stoolBar', 5, 2, 2, act=JUS), I('stoolBar', 6, 2, 2, act=JUS),
        I('shop:character-employee', 1, 0, 0, deco=False), I('shop:cash-register', 2, 0, 0),
        I('tableCloth', 1, 3, 0, act=RESTO), I('chair', 1, 2, 0), I('chair', 1, 4, 2), I('food:pizza', 1, 3, 0, z=0.33, deco=True),
        I('tableCloth', 3, 4, 0, act=RESTO), I('chair', 3, 3, 0), I('chair', 3, 5, 2), I('food:burger-cheese', 3, 4, 0, z=0.33, deco=True),
        I('tableRound', 6, 4, 0, act=RESTO), I('chair', 5, 4, 1), I('chair', 7, 4, 3), I('food:cake', 6, 4, 0, z=0.1, deco=True),
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
        I('deskCorner', 1, 1, 0, act=ACCUEIL), I('computerScreen', 1, 1, 0, z=0.38, deco=True), I('chairDesk', 1, 0, 0), I('shop:character-employee', 2, 0, 0),
        I('benchCushion', 0, 3, 1, act=SOFA), I('benchCushion', 0, 4, 1, act=SOFA), I('pottedPlant', 3, 0), I('shop:gacha-machine', 3, 6),
        I('bedSingle', 4, 0, 0, act=SOIN), I('sideTable', 5, 0), I('bedSingle', 6, 0, 0, act=SOIN), I('sideTable', 7, 0), I('bedSingle', 8, 0, 0, act=SOIN),
        I('lampSquareTable', 5, 0, 0, z=0.38, deco=True), I('food:apple', 7, 0, 0, z=0.38, deco=True),
        I('bedSingle', 4, 4, 0, act=SOIN), I('computerScreen', 5, 4, 0), I('desk', 7, 4, 0), I('chairDesk', 7, 5, 2), I('bathroomSinkSquare', 8, 4, 0, act=WASH),
    ]}
# ── Hôtel (suite) ─────────────────────────────────────────────────────
ROOM = {'t': 'Room service 🍽️', 'f': 40, 'j': 10, 'c': 8, 'pose': 'eat', 'dur': 3}
L['hotel'] = {
    'nom': 'La suite de l’hôtel', 'w': 8, 'h': 7, 'mur': '#f5efe4', 'murHaut': '#c9a227', 'porte': [0, 2],
    'sols': [[0, 0, 5, 7, 'moquetteBeige'], [5, 0, 8, 7, 'marbre']],
    'cloisons': [['c', 5, 0, 7, [3]]],
    'pieces': [['Suite', 2.5, 3.5], ['Salle de bain', 6.5, 3.5]],
    'items': [
        I('bedDouble', 1, 0, 0, act=BED), I('cabinetBedDrawer', 0, 0), I('cabinetBedDrawer', 3, 0), I('lampSquareTable', 0, 0, 0, z=0.26, deco=True), I('lampSquareTable', 3, 0, 0, z=0.26, deco=True),
        I('rugRectangle', 1, 3, 0, flat=True), I('loungeDesignSofa', 1, 5, 2, act=SOFA), I('tableCoffeeGlass', 1, 4, 0, act=ROOM), I('food:cake', 1, 4, 0, z=0.23, deco=True),
        I('cabinetTelevision', 4, 3, 3), I('televisionModern', 4, 3, 3, z=0.31, deco=True, act=TV), I('loungeChairRelax', 0, 4, 1, act=SOFA), I('pottedPlant', 4, 6), I('pottedPlant', 0, 6),
        I('bathtub', 5, 0, 0, act=BATH), I('showerRound', 7, 1, 3, act=BATH), I('bathroomSinkSquare', 5, 5, 1, act=WASH), I('toilet', 7, 5, 3, act=WC), I('plantSmall2', 7, 6),
    ]}
# ── École ─────────────────────────────────────────────────────────────
PROF = {'t': 'Parler à Sensei 🥋', 'j': 8, 'pose': 'wave', 'dur': 2}
L['ecole'] = {
    'nom': "L'école", 'w': 8, 'h': 7, 'mur': '#fff8e7', 'murHaut': '#f4a261', 'porte': [0, 5], 'tableau': 1,
    'sols': [[0, 0, 8, 7, 'bois']], 'cloisons': [], 'pieces': [['Classe', 4, 3.5]],
    'items': [
        I('desk', 3, 1, 0, act=PROF), I('chairDesk', 3, 0, 0),
        I('desk', 2, 3, 2, act=DESK), I('chairDesk', 2, 4, 2), I('desk', 4, 3, 2, act=DESK), I('chairDesk', 4, 4, 2), I('desk', 6, 3, 2, act=DESK), I('chairDesk', 6, 4, 2),
        I('desk', 2, 5, 2, act=DESK), I('chairDesk', 2, 6, 2), I('desk', 4, 5, 2, act=DESK), I('chairDesk', 4, 6, 2), I('desk', 6, 5, 2, act=DESK), I('chairDesk', 6, 6, 2),
        I('laptop', 2, 3, 2, z=0.38, deco=True), I('food:apple', 3, 1, 0, z=0.38, deco=True),
        I('bookcaseOpen', 0, 0, 1, act=READ), I('bookcaseOpen', 0, 1, 1, act=READ), I('bookcaseClosedWide', 0, 2, 1, act=READ), I('pottedPlant', 7, 0), I('shop:gacha-machine', 7, 6, 3),
    ]}
# ── Pharmacie ─────────────────────────────────────────────────────────
VITA = {'t': 'Acheter des vitamines 💊', 'e': 10, 'j': 5, 'c': 5, 'pose': 'idle', 'dur': 2}
L['pharmacie'] = {
    'nom': 'La pharmacie', 'w': 6, 'h': 5, 'mur': '#f1fbf4', 'murHaut': '#2a9d8f', 'porte': [0, 3],
    'sols': [[0, 0, 6, 5, 'blancBleu']], 'cloisons': [], 'pieces': [['Pharmacie', 3, 2.5]],
    'items': [
        I('shop:shelf-boxes', 1, 0, act=VITA), I('shop:shelf-boxes', 2, 0, act=VITA), I('shop:shelf-bags', 3, 0, act=VITA), I('shop:shelf-boxes', 4, 0, act=VITA),
        I('kitchenBar', 2, 2, 0), I('kitchenBar', 3, 2, 0), I('shop:cash-register', 4, 2, 0), I('shop:character-employee', 3, 1, 0),
        I('shop:display-small', 5, 3, 3, act=VITA), I('benchCushion', 1, 4, 2, act=SOFA), I('pottedPlant', 5, 0),
    ]}
# bâtiments de la ville -> intérieur
BAT = {'house1': 'maison', 'house2': 'maison', 'house3': 'maison', 'apt3': 'maison', 'tower10': 'maison', 'tower_mod': 'maison', 'castle': 'maison',
       'resto': 'resto', 'shop': 'boutique', 'supermarket': 'supermarche', 'hospital': 'hopital', 'pharmacy': 'pharmacie', 'school': 'ecole',
       'hotel_lagoon': 'hotel', 'hotel_sail': 'hotel', 'hotel_atlantis': 'hotel', 'burj': 'hotel'}
if __name__ == '__main__':
    import sys
    json.dump({'interieurs': L, 'batiments': BAT}, open(sys.argv[1], 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    print('ok', len(L))
