"""Vérifie les plans d'intérieurs (data/interieurs.json + sprites) :
chevauchements, sorties du plan, porte bouchée, objets posés sans meuble dessous,
meubles à action inaccessibles depuis la porte.
  python3 tools/verif_interieurs.py [sprites.json]
"""
import json, sys, os
from collections import deque
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = json.load(open(os.path.join(ROOT, 'data/interieurs.json'), encoding='utf-8'))
SPR = json.load(open(sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, 'assets/interieur/sprites.json')))
SURF = set(D['surfaces'])
tot = 0
for lid, L in D['interieurs'].items():
    pb = []
    w, h = L['w'], L['h']
    walls = set()
    for ax, k, f, t, doors in L.get('cloisons', []):
        for x in range(f, t):
            if x in doors: continue
            walls.add(((k - 1, x), (k, x)) if ax == 'c' else ((x, k - 1), (x, k)))
    wb = lambda a, b: (a, b) in walls or (b, a) in walls
    block, items = {}, []
    for it in L['items']:
        m = it['m']
        if m[0] == '@': fw, fh = it.get('fw', 1), it.get('fh', 1); top = .5
        else:
            sp = SPR.get(f"{m}|{it['rot']}")
            if not sp: pb.append(f"pas d'image : {m} rot {it['rot']}"); continue
            fw, fh, top = sp[3], sp[4], sp[5]
        o = dict(it, fw=fw, fh=fh, top=top); items.append(o)
        seat = m.split('~')[0].startswith(('chair', 'stool'))
        if it.get('flat') or it.get('deco') or seat or m.startswith('plantSmall'): continue
        for a in range(fw):
            for b in range(fh):
                c, r = it['c'] + a, it['r'] + b
                if not (0 <= c < w and 0 <= r < h): pb.append(f'{m} ({it["c"]},{it["r"]}) sort du plan')
                if (c, r) in block: pb.append(f'{m} ({it["c"]},{it["r"]}) chevauche {block[(c, r)]["m"]} ({block[(c, r)]["c"]},{block[(c, r)]["r"]})')
                if a and wb((c - 1, r), (c, r)) or b and wb((c, r - 1), (c, r)): pb.append(f'{m} ({it["c"]},{it["r"]}) traverse une cloison')
                block[(c, r)] = o
    door = tuple(L.get('porte', [-1, -1]))
    if door in block: pb.append(f'porte {door} bouchée par {block[door]["m"]}')
    for o in items:
        if o.get('z') and o.get('deco') and not o['m'].startswith('ceiling'):
            b = block.get((o['c'], o['r']))
            if not b or b['m'].split('~')[0] not in SURF and not b['m'].startswith('kitchen'):
                pb.append(f'{o["m"]} ({o["c"]},{o["r"]}) posé sans meuble dessous ({b["m"] if b else "rien"})')
    # accessibilité depuis la porte
    seen = {door}; q = deque([door])
    while q:
        c, r = q.popleft()
        for dc, dr in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            n = (c + dc, r + dr)
            if n in seen or not (0 <= n[0] < w and 0 <= n[1] < h) or n in block or wb((c, r), n): continue
            seen.add(n); q.append(n)
    for o in items:
        if not o.get('act'): continue
        cells = [(o['c'] + a, o['r'] + b) for a in range(o['fw']) for b in range(o['fh'])]
        ok = any((x + dc, y + dr) in seen and not wb((x, y), (x + dc, y + dr)) for x, y in cells for dc, dr in ((1, 0), (-1, 0), (0, 1), (0, -1)))
        if o.get('deco') and o.get('z'): ok = True if any(n in seen for n in [(o['c'] + 1, o['r']), (o['c'] - 1, o['r']), (o['c'], o['r'] + 1), (o['c'], o['r'] - 1)]) else ok
        if not ok: pb.append(f'{o["m"]} ({o["c"]},{o["r"]}) inaccessible')
    libre = w * h - len(block)
    print(f'{lid:14s} {w}x{h}  {len(items)} objets  {libre} cases libres  {"OK" if not pb else str(len(pb)) + " problème(s)"}')
    for p in pb: print('   -', p)
    tot += len(pb)
sys.exit(1 if tot else 0)
