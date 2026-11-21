"""Injecte docs/contenu/sport/yoga.json (vérifié) dans index.html : postures dans DATA.defis, séances dans YOGA_SEANCES.
  python3 tools/yoga_build.py"""
import json,re
from pathlib import Path
R=Path(__file__).resolve().parent.parent;H=R/'index.html'
y=json.loads((R/'docs/contenu/sport/yoga.json').read_text(encoding='utf-8'))
s=H.read_text(encoding='utf-8')
A,B='// ── YOGA (généré par tools/yoga_build.py depuis docs/contenu/sport/yoga.json) ──','// ── FIN YOGA ──'
s=re.sub(r',\n'+re.escape(A)+r'[\s\S]*?'+re.escape(B),'',s)
bloc=',\n'+A+'\n'+',\n'.join(json.dumps(d,ensure_ascii=False) for d in y['postures'])+'\n'+B
m=re.search(r'\ndefis:\[[\s\S]*?\n\]',s);end=m.end()-2
s=s[:end]+bloc+s[end:]
s=re.sub(r'const YOGA_SEANCES=\[.*?\];\n','',s)
s=s.replace('// 🧘 Séances de yoga enchaînées','const YOGA_SEANCES='+json.dumps(y['seances'],ensure_ascii=False)+';\n// 🧘 Séances de yoga enchaînées',1)
H.write_text(s,encoding='utf-8');print(len(y['postures']),'postures,',len(y['seances']),'séances')
