"""Fusionne des fiches complémentaires (déjà passées par fiches_appliquer.py dans un dossier) avec docs/contenu/fiches/FR.
Chaque nouvelle fiche est placée après la dernière fiche de son axe (axe nouveau → à la fin). Les id ne changent pas.
  python3 tools/fiches_fusion.py <dossier_complement>"""
import json,sys,glob,os
from pathlib import Path
R=Path(__file__).resolve().parent.parent;DST=R/'docs/contenu/fiches/FR'
n=0
for f in sorted(glob.glob(os.path.join(sys.argv[1],'REV-*.json'))):
    nv=json.load(open(f,encoding='utf-8'))['fiches'];p=DST/os.path.basename(f)
    d=json.load(open(p,encoding='utf-8'));L=d['fiches'];ids={x['id'] for x in L}
    for x in nv:
        if x['id'] in ids:continue
        pos=max([i for i,y in enumerate(L) if y['axe']==x['axe']],default=len(L)-1)+1
        L.insert(pos,x);ids.add(x['id']);n+=1
    json.dump(d,open(p,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
print(n,'fiches ajoutées')
