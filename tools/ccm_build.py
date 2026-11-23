"""Comment ça marche : docs/contenu/ccm/<LANG>/*.json (vérifiés) → data/ccm/<LANG>/<ID>.json + index.json.
Un thème n'est publié que si tous ses schémas existent ET s'il est listé dans docs/contenu/ccm/valides.txt (schémas vérifiés).
  python3 tools/ccm_build.py"""
import json
from pathlib import Path
R=Path(__file__).resolve().parent.parent
DECO={'CM-01':('⚡','#F59E0B'),'CM-02':('🍳','#EF4444'),'CM-03':('🚿','#3B82F6'),'CM-04':('🌡️','#F97316'),'CM-05':('📱','#8B5CF6'),'CM-06':('🌐','#06B6D4'),
 'CM-07':('🚗','#64748B'),'CM-08':('✈️','#0EA5E9'),'CM-09':('💶','#10B981'),'CM-10':('💳','#14B8A6'),'CM-11':('🧾','#6366F1'),'CM-12':('🕵️','#DC2626'),
 'CM-13':('📰','#A855F7'),'CM-14':('🚑','#E11D48'),'CM-15':('😴','#4F46E5'),'CM-16':('🏷️','#65A30D'),'CM-17':('💡','#EAB308'),'CM-18':('🥖','#D97706'),
 'CM-19':('🛩️','#0284C7'),'CM-20':('🌦️','#0891B2'),'CM-21':('🫀','#DB2777'),'CM-22':('♻️','#16A34A'),'BP-23':('👋','#F59E0B'),'BP-24':('🤝','#10B981'),
 'BP-25':('💬','#3B82F6'),'BP-26':('👂','#8B5CF6'),'BP-27':('🖊️','#EF4444'),'BP-28':('🎤','#F97316'),'BP-29':('⚖️','#0EA5E9'),'BP-30':('💼','#334155'),'BP-31':('🛡️','#DC2626'),'BP-32':('✉️','#6366F1')}
FORCER=set()
VALIDES=set((R/'docs/contenu/ccm/valides.txt').read_text().split()) if (R/'docs/contenu/ccm/valides.txt').exists() else None
for ld in sorted(x for x in (R/'docs/contenu/ccm').iterdir() if x.is_dir()):
    out=R/'data/ccm'/ld.name;out.mkdir(parents=True,exist_ok=True);themes=[]
    for f in sorted(ld.glob('*.json')):
        d=json.loads(f.read_text(encoding='utf-8'))
        manque=[f"{l['id']}-{i}" for l in d['lecons'] for i,c in enumerate(l['cartes'],1) if c.get('schema') and not (R/'assets/ccm'/f"{l['id']}-{i}.svg").exists()]
        if manque and d['id'] not in FORCER:print(d['id'],'non publié :',len(manque),'schémas manquants');continue
        if VALIDES is not None and d['id'] not in VALIDES:print(d['id'],'non publié : schémas pas encore vérifiés');continue
        (out/f.name).write_text(json.dumps(d,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
        e,c=DECO.get(d['id'],('🛠️','#3B82F6'))
        themes.append({'id':d['id'],'titre':d['titre'],'public':'enfant' if d.get('public','').startswith('enfant') else 'ado-adulte','emoji':e,'couleur':c,'lecons':[l['id'] for l in d['lecons']]})
    (out/'index.json').write_text(json.dumps({'themes':themes},ensure_ascii=False,separators=(',',':')),encoding='utf-8')
    print(ld.name,len(themes),'thèmes publiés')
