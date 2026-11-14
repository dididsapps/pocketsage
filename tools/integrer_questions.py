"""Ajoute un lot de questions VÉRIFIÉES (sortie de la relecture indépendante) dans js/questions-plus-data.js.
  python3 tools/integrer_questions.py verif_XX.json [...]
Ignore les questions marquées "supprimer", retire les champs de relecture, refuse les ids déjà présents."""
import json, os, sys, re
sys.path.insert(0, os.path.dirname(__file__))
from qparse import items, texte_questions
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F = os.path.join(ROOT, 'js/questions-plus-data.js')
CLES = ['id', 'classe', 'cat', 'type', 'enonce', 'rep', 'choix', 'diff', 'hint', 'expl']
deja = {i for i, *_ in items(texte_questions())}
lignes, n, sup, dbl = [], 0, 0, 0
for f in sys.argv[1:]:
    for q in json.load(open(f, encoding='utf-8')):
        if q.get('verif') == 'supprimer' or q.get('supprimer'): sup += 1; continue
        if q['id'] in deja: dbl += 1; continue
        assert q['rep'] in q['choix'], q['id']
        parts = [f'{k}:{json.dumps(q[k], ensure_ascii=False)}' for k in CLES if k in q and q[k] not in (None, '')]
        lignes.append('{' + ','.join(parts) + '},'); deja.add(q['id']); n += 1
s = open(F, encoding='utf-8').read()
s = s.rstrip().rstrip('];').rstrip() + '\n' + '\n'.join(lignes) + '\n];\n'
open(F, 'w', encoding='utf-8').write(s)
print(f'{n} ajoutées, {sup} supprimées par la relecture, {dbl} déjà présentes')
