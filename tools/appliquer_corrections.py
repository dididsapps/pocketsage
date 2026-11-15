"""Applique des corrections de questions (sortie d'un agent de correction/vérification) aux sources.
  python3 tools/appliquer_corrections.py res1.json [...]
Chaque entrée : {"id", "action": "ok"|"corriger"|"supprimer", enonce?, choix?, rep?, hint?}.
Les fichiers modifiés : index.html et js/questions-plus-data.js (là où se trouve la question)."""
import json, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FICHIERS = ['index.html', 'js/questions-plus-data.js']
src = {f: open(os.path.join(ROOT, f), encoding='utf-8').read() for f in FICHIERS}
enc = lambda v: json.dumps(v, ensure_ascii=False)
def ligne(i):
    for f, s in src.items():
        m = re.search(r'(?m)^[ \t]*\{id:"%s",[^\n]*\n' % re.escape(i), s)
        if m: return f, m
    return None, None
def champ(l, k, v):
    if k == 'choix':
        m = re.search(r'choix:\[', l); j = m.end(); q = None; d = 1
        while j < len(l):
            c = l[j]
            if q:
                if c == '\\': j += 2; continue
                if c == q: q = None
            elif c in '"\'': q = c
            elif c == ']': break
            j += 1
        return l[:m.start()] + 'choix:' + enc(v) + l[j + 1:]
    m = re.search(k + r':"((?:[^"\\]|\\.)*)"', l)
    if m: return l[:m.start()] + f'{k}:{enc(v)}' + l[m.end():]
    return l.rstrip().rstrip('},').rstrip('}') + f',{k}:{enc(v)}' + '},\n'
n = {'ok': 0, 'corriger': 0, 'supprimer': 0, 'introuvable': 0}
for fic in sys.argv[1:]:
    for c in json.load(open(fic, encoding='utf-8')):
        a = c.get('action') or c.get('verif') or 'ok'
        a = {'corrigée': 'corriger', 'corrige': 'corriger'}.get(a, a)
        if a == 'ok': n['ok'] += 1; continue
        f, m = ligne(c['id'])
        if not m: n['introuvable'] += 1; continue
        s = src[f]; l = m.group(0)
        if a == 'supprimer': src[f] = s[:m.start()] + s[m.end():]; n['supprimer'] += 1; continue
        for k in ('enonce', 'choix', 'rep', 'hint', 'classe'):
            if c.get(k) not in (None, ''): l = champ(l, k, c[k])
        src[f] = s[:m.start()] + l + s[m.end():]; n['corriger'] += 1
for f, s in src.items(): open(os.path.join(ROOT, f), 'w', encoding='utf-8').write(s)
print(n)
