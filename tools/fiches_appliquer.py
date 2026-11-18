"""Applique les sorties de la moulinette aux fiches : python3 tools/fiches_appliquer.py <dossier_source> <verif1.json> [...] [--out dossier]
Écrit les fiches validées dans docs/contenu/fiches/FR/. Retire aussi le préfixe « Sans regarder la fiche : »."""
import json,sys,re,glob,os
from pathlib import Path
R=Path(__file__).resolve().parent.parent;OUT=R/'docs/contenu/fiches/FR'
if '--out' in sys.argv:i=sys.argv.index('--out');OUT=Path(sys.argv[i+1]);del sys.argv[i:i+2]
OUT.mkdir(parents=True,exist_ok=True)
src=Path(sys.argv[1]);corr={};suppr=set();vraies=[]
for v in sys.argv[2:]:
    for x in json.load(open(v,encoding='utf-8')).get('fiches',[]):
        if x.get('action')=='supprimer':suppr.add(x['id'])
        elif x.get('corrections'):corr[x['id']]=x['corrections']
        if x.get('action')!='ok' and 'Sans regarder' not in x.get('note','')[:60]:vraies.append((x['id'],x.get('note','')))
PRE=re.compile(r'^\s*Sans regarder la fiche\s*:\s*',re.I)
n=0
for f in sorted(glob.glob(str(src/'REV-*.json'))):
    d=json.load(open(f,encoding='utf-8'));ex=OUT/os.path.basename(f)
    keep=[]
    for x in d['fiches']:
        if x['id'] in suppr:continue
        x.update(corr.get(x['id'],{}))
        for q in x.get('quiz',[]):q['q']=PRE.sub('',q['q']);q['q']=q['q'][:1].upper()+q['q'][1:]
        keep.append(x);n+=1
    d['fiches']=keep;json.dump(d,open(ex,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
print(n,'fiches écrites,',len(suppr),'supprimées,',len(corr),'corrigées')
