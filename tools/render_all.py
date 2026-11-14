"""Rend tous les meubles (modèles Kenney) en sprites isométriques -> assets/interieur/*.webp + sprites.json
  python3 tools/render_all.py assets/interieur [--force]
Les packs Kenney (OBJ) sont attendus dans $KENNEY (par défaut le dossier de travail de la session).
Échelle : 1 case = ECH unités Kenney (les meubles remplissent mieux leurs cases).
"""
import json, os, sys
os.environ.setdefault('RENDER_TOL', '0.3')
sys.path.insert(0, os.path.dirname(__file__))
from render3d import render
from PIL import Image
K = os.environ.get('KENNEY', '/tmp/claude-0/-home-claude/a8977e66-ea58-56a5-906f-95854358b7d4/scratchpad/packs/')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = sys.argv[1]; FORCE = '--force' in sys.argv; os.makedirs(OUT, exist_ok=True)
ECH = {'furniture': 1.7, 'shop': 1.25, 'food': 1.0}
ECH_MODELE = {}
d = json.load(open(os.path.join(ROOT, 'data/interieurs.json'), encoding='utf-8'))
need = set()
for L in d['interieurs'].values():
    for it in L['items']:
        if not it['m'].startswith('@'): need.add((it['m'], it['rot']))
for m, nom, prix, cat, o in d['catalogue']:
    for rot in range(4):
        need.add((m, rot))
        if o.get('c'):
            for k in d['couleurs']: need.add((m + '~' + k, rot))
def hexc(h): return tuple(int(h[i:i + 2], 16) / 255 for i in (1, 3, 5))
old = {} if FORCE or not os.path.exists(OUT + '/sprites.json') else json.load(open(OUT + '/sprites.json'))
man = {}
for m, rot in sorted(need):
    base, _, col = m.partition('~'); rc = None
    if col in d['couleurs']: c = hexc(d['couleurs'][col]); rc = {'carpet': c, 'carpetDarker': tuple(x * .68 for x in c)}
    elif col: rc = {k: hexc(v) for k, v in d['styles'][col].items()}; rc.setdefault('carpetDarker', tuple(x * .68 for x in rc.get('carpet', (0.6, 0.3, 0.3))))
    if m.startswith('shop:'): p = K + 'kenney_mini-shop_2.1/Models/OBJ format/' + m[5:] + '.obj'; sc = ECH['shop']
    elif m.startswith('food:'): p = K + 'kenney_food-kit/Models/OBJ format/' + m[5:] + '.obj'; sc = ECH['food']
    else: p = K + 'kenney_furniture-kit/Models/OBJ format/' + base + '.obj'; sc = ECH['furniture']
    sc = ECH_MODELE.get(base.split(':')[-1], sc)
    name = m.replace(':', '_').replace('~', '-') + '_' + str(rot)
    k = m + '|' + str(rot)
    if k in old and os.path.exists(OUT + '/' + name + '.webp'): man[k] = old[k]; continue
    # (rot+2) : les modèles Kenney regardent vers −z ; ainsi rot 0 = face vers +r comme dans layouts.py
    info = render(p, OUT + '/' + name + '.png', 'center', (rot + 2) % 4, R=2, SS=3, scale=sc, recolor=rc)
    top = max(float(l.split()[2]) for l in open(p) if l.startswith('v ')) * sc
    im = Image.open(OUT + '/' + name + '.png'); im.save(OUT + '/' + name + '.webp', quality=88, method=6, lossless=False); os.remove(OUT + '/' + name + '.png')
    man[k] = [name, info['ax'], info['ay'], info['fw'], info['fh'], round(top, 2)]
json.dump(man, open(OUT + '/sprites.json', 'w'), separators=(',', ':'))
tot = sum(os.path.getsize(OUT + '/' + f) for f in os.listdir(OUT)); print(len(man), 'sprites', tot // 1024, 'Ko')
