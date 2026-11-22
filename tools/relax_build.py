"""Relaxation : docs/contenu/relaxation/meditations.json (vérifié) → data/relax.json lu par js/relax.js.
  python3 tools/relax_build.py"""
import json
from pathlib import Path
R=Path(__file__).resolve().parent.parent
d=json.loads((R/'docs/contenu/relaxation/meditations.json').read_text(encoding='utf-8'))
out={'meditations':d['meditations'],'ambiances':d['ambiances']}
(R/'data/relax.json').write_text(json.dumps(out,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
print(len(out['meditations']),'méditations')
