"""Applique la moulinette aux leçons « Comment ça marche » : python3 tools/ccm_appliquer.py <dossier_source> <verif.json>... [--out dossier]"""
import json,sys,glob,os
from pathlib import Path
R=Path(__file__).resolve().parent.parent;OUT=R/'docs/contenu/ccm/FR'
if '--out' in sys.argv:i=sys.argv.index('--out');OUT=Path(sys.argv[i+1]);del sys.argv[i:i+2]
OUT.mkdir(parents=True,exist_ok=True);corr={};suppr=set()
for v in sys.argv[2:]:
    for x in json.load(open(v,encoding='utf-8'))['lecons']:
        if x.get('action')=='supprimer':suppr.add(x['id'])
        elif x.get('corrections'):corr[x['id']]=x['corrections']
n=0
for f in sorted(glob.glob(os.path.join(sys.argv[1],'*.json'))):
    d=json.load(open(f,encoding='utf-8'))
    d['lecons']=[l for l in d['lecons'] if l['id'] not in suppr]
    for l in d['lecons']:l.update(corr.get(l['id'],{}));n+=1
    json.dump(d,open(OUT/os.path.basename(f),'w',encoding='utf-8'),ensure_ascii=False,indent=1)
print(n,'leçons,',len(corr),'corrigées,',len(suppr),'supprimées')
