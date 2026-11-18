"""Parcours de la semaine : docs/parcours/PC-*.json (vérifiés) → js/parcours-data.js + fiches PDF « Mon programme de la semaine ».
  python3 tools/parcours_build.py [--pdf]
"""
import html, json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
ORDRE = ['PC-CONC', 'PC-MEM', 'PC-CALME', 'PC-EMO', 'PC-PERS']
COUL = {'PC-CONC': '#3B82F6', 'PC-MEM': '#8B5CF6', 'PC-CALME': '#EF4444', 'PC-EMO': '#F59E0B', 'PC-PERS': '#10B981'}


def charger():
    return [json.loads((ROOT / f'docs/parcours/{i}.json').read_text(encoding='utf-8')) for i in ORDRE if (ROOT / f'docs/parcours/{i}.json').exists()]


def fiche_html(pc):
    e = html.escape; c = COUL.get(pc['id'], '#6C63FF')
    lignes = ''.join(f"""<tr><td class="j">{e(j['jour'])}</td><td><b>{e(j['activite']['titre'])}</b><div class="s">+ jeu « {e(j['jeu']['id'])} » et un moment calme</div></td>
      <td class="c"><div class="box"></div></td></tr>""" for j in pc['jours'])
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
@page{{size:A4;margin:14mm}}body{{font-family:'Nunito','Helvetica',Arial,sans-serif;color:#222;margin:0}}
.top{{background:{c};color:#fff;border-radius:18px;padding:18px 22px}}h1{{margin:0;font-size:26px}}.sub{{font-size:14px;margin-top:6px;opacity:.95}}
.nom{{margin:18px 4px;font-size:17px}}table{{width:100%;border-collapse:separate;border-spacing:0 10px}}
td{{background:#F6F6FB;padding:14px 12px;font-size:16px;vertical-align:middle}}td:first-child{{border-radius:12px 0 0 12px}}td:last-child{{border-radius:0 12px 12px 0}}
.j{{font-weight:900;color:{c};width:95px}}.s{{font-size:12px;color:#666;margin-top:3px}}.c{{width:56px;text-align:center}}
.box{{width:34px;height:34px;border:3px solid {c};border-radius:10px;margin:auto}}
.bonus{{margin-top:14px;border:3px dashed {c};border-radius:16px;padding:14px 16px;font-size:15px;line-height:1.5}}
.pied{{margin-top:22px;font-size:11.5px;color:#888;display:flex;justify-content:space-between}}
.etoiles{{font-size:30px;letter-spacing:6px;margin-top:10px;text-align:center;color:{c}}}
</style></head><body><div class="top"><h1>{e(pc['nom_enfant'])}</h1><div class="sub">{e(pc['fiche']['titre'])} — 10 minutes par jour</div></div>
<div class="nom">Mon prénom : ________________________ &nbsp;&nbsp; Semaine du : ____________</div>
<table>{lignes}</table>
<div class="bonus">🎉 <b>Défi bonus du week-end (sans écran) :</b> {e(pc['fiche']['defi_bonus'])} <span style="float:right"><span class="box" style="display:inline-block;vertical-align:middle"></span></span></div>
<div class="etoiles">☆ ☆ ☆ ☆ ☆</div><div style="text-align:center;font-size:13px;color:#555">Colorie une étoile à chaque jour réussi. Les essais comptent aussi !</div>
<div class="pied"><span>PocketSage Academy · pocketsage.org</span><span>Pour le parent : {e(pc['accroche_parent'])}</span></div></body></html>"""


def main():
    ps = charger()
    out = ROOT / 'js/parcours-data.js'
    out.write_text('// Généré par tools/parcours_build.py depuis docs/parcours/*.json — ne pas modifier à la main\nwindow.PARCOURS=' +
                   json.dumps(ps, ensure_ascii=False, separators=(',', ':')) + ';\n', encoding='utf-8')
    print(len(ps), 'parcours →', out)
    if '--pdf' in sys.argv:
        from playwright.sync_api import sync_playwright
        (ROOT / 'fiches/FR').mkdir(parents=True, exist_ok=True)
        with sync_playwright() as p:
            b = p.chromium.launch(); pg = b.new_page()
            for pc in ps:
                pg.set_content(fiche_html(pc)); pg.pdf(path=str(ROOT / f"fiches/FR/{pc['id']}.pdf"), format='A4', print_background=True)
                print('  🖨️', pc['id'])
            b.close()


if __name__ == '__main__':
    main()
