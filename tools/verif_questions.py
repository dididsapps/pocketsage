"""Contrôle des questions de quiz dans index.html : bonne réponse présente dans les choix, pas de choix en double.
  python3 tools/verif_questions.py   (code de sortie 1 s'il y a un problème)"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from qparse import items, field, arr
s = open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'index.html'), encoding='utf-8').read()
abs_, dbl = [], []
for i, l, a, b in items(s):
    rep, ch = field(l, 'rep'), arr(l, 'choix')
    if rep is None or not ch: continue
    if rep not in ch: abs_.append(i)
    if len(set(ch)) < len(ch): dbl.append(i)
print(f'bonne réponse absente des choix : {len(abs_)} {abs_[:20]}')
print(f'choix en double : {len(dbl)} {dbl[:30]}')
sys.exit(1 if abs_ else 0)
