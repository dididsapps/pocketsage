#!/usr/bin/env python3
"""Cartes d'exercices à imprimer (sport) : 3 exercices par page A4, étapes dessinées à la suite.

Sources : défis DF-* (tableau DATA.defis d'index.html), yoga YG-*/YF-* (docs/contenu/sport/yoga.json),
          illustrations assets/sport/<ID>-<n>.webp (tools/sport_illus_build.py).
Sorties : sport/cartes/<rubrique>.pdf (une par catégorie) et sport/cartes/<SEANCE>.pdf (séances de yoga),
          data/sport_cartes.json = {"cat": {"<cat>": "fichier"}, "seance": {"<id>": "fichier"}}
  python3 tools/sport_cartes.py
"""
import base64, html, json, re, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'sport/cartes'
E = lambda s: html.escape(str(s or ''))
RUBRIQUES = {'echauffement': ('🔥 Échauffement', '#F59E0B'), 'cardio': ('❤️ Cardio', '#EF4444'), 'gainage': ('💪 Gainage', '#8B5CF6'),
             'stretching': ('🤸 Stretching', '#06B6D4'), 'respiration': ('🌬️ Respiration', '#3B82F6'),
             'yoga': ('🧘 Yoga', '#10B981'), 'yogafam': ('👨‍👩‍👧 Yoga à deux', '#EC4899')}


def exercices():
    js = ("const s=require('fs').readFileSync(process.argv[1],'utf8');const out=[];"
          "s.split('\\n').forEach(l=>{l=l.trim();if(/^\\{id:\"DF-\\d+\"/.test(l))out.push(eval('('+l.replace(/,$/,'')+')'));});"
          "console.log(JSON.stringify(out));")
    df = json.loads(subprocess.check_output(['node', '-e', js, str(ROOT / 'index.html')]))
    yg = json.loads((ROOT / 'docs/contenu/sport/yoga.json').read_text(encoding='utf-8'))
    return {x['id']: x for x in df + yg['postures']}, yg['seances']


def img(id_, n):
    p = ROOT / f'assets/sport/{id_}-{n}.webp'
    if not p.exists(): return None
    from io import BytesIO
    from PIL import Image
    b = BytesIO(); Image.open(p).convert('RGB').resize((360, 360), Image.LANCZOS).save(b, 'JPEG', quality=80, optimize=True)
    return 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()


def nom(x):
    return re.sub(r'\s*[\U0001F000-\U0001FFFF\u2600-\u27BF\uFE0F\u200D]+', '', x['nom']).strip()


def emoji(x):
    m = re.findall(r'[\U0001F000-\U0001FFFF\u2600-\u27BF][\uFE0F\u200D\U0001F000-\U0001FFFF]*', x['nom'])
    return m[0] if m else '🏃'


def carte(x, comptes, coul):
    n = comptes.get(x['id'], 0)
    ims = [img(x['id'], i) for i in range(1, n + 1)]
    etapes = ''.join(f"<div class='et'><img src='{u}'><span>{i + 1}</span></div>" for i, u in enumerate(ims) if u) \
        or f"<div class='emo'>{emoji(x)}</div>"
    age = x.get('age', '4-18').replace('-', ' à ') + ' ans'
    diff = ['', 'Facile', 'Intermédiaire', 'Avancé'][x.get('diff') or 1]
    return (f"<div class='c' style='--c:{coul}'><div class='h'><b>{emoji(x)} {E(nom(x))}</b>"
            f"<small>{E(age)} · {diff} · ⏱ {x.get('dur', 30)} s</small></div>"
            f"<div class='ets n{min(len([u for u in ims if u]) or 1, 8)}'>{etapes}</div>"
            f"<p class='co'>{E(x.get('consigne'))}</p>"
            + (f"<p class='as'>💡 {E(x.get('hint'))}</p>" if x.get('hint') else '') + "</div>")


CSS = """@page{size:A4;margin:10mm}*{box-sizing:border-box}body{margin:0;font-family:'Nunito','DejaVu Sans',Arial,sans-serif;color:#1F2937}
.pg{height:277mm;display:flex;flex-direction:column;gap:4mm;break-after:page}.pg:last-child{break-after:auto}
.top{display:flex;justify-content:space-between;align-items:baseline;font-size:9pt;color:#6B7280;height:5mm}.top b{font-size:12pt;color:#111}
.c{flex:0 0 84mm;border:2px solid var(--c);border-radius:5mm;padding:3mm 5mm;display:flex;flex-direction:column;overflow:hidden}
.h{display:flex;justify-content:space-between;align-items:baseline;border-bottom:1.5px dashed var(--c);padding-bottom:1.5mm}
.h b{font-size:15pt;color:var(--c)}.h small{font-size:9pt;color:#6B7280;white-space:nowrap}
.ets{flex:1;display:flex;gap:2mm;align-items:center;justify-content:center;min-height:0;padding:1.5mm 0}
.et{position:relative;flex:0 1 50mm;min-width:0;aspect-ratio:1}.et img{width:100%;height:100%;object-fit:contain}
.et span{position:absolute;top:1mm;left:1mm;width:6mm;height:6mm;border-radius:50%;background:var(--c);color:#fff;font-size:9pt;font-weight:800;display:flex;align-items:center;justify-content:center}
.emo{font-size:40pt}.co{margin:0;font-size:10.5pt;line-height:1.3}.as{margin:1mm 0 0;font-size:9pt;color:#4B5563}
.pied{font-size:7.5pt;color:#9CA3AF;text-align:center;margin-top:auto}"""


def doc(titre, liste, comptes, coul):
    pages = []
    for i in range(0, len(liste), 3):
        cs = ''.join(carte(x, comptes, coul) for x in liste[i:i + 3])
        pages.append(f"<div class='pg'><div class='top'><b>{E(titre)}</b><span>PocketSage · page {i // 3 + 1}/{(len(liste) + 2) // 3}</span></div>{cs}"
                     "<div class='pied'>On va doucement, on respire, et un exercice ne doit jamais faire mal. pocketsage.org</div></div>")
    return f"<html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{''.join(pages)}</body></html>"


def main():
    ex, seances = exercices()
    comptes = json.loads((ROOT / 'data/sport_illus.json').read_text())
    OUT.mkdir(parents=True, exist_ok=True)
    jobs, idx = [], {'cat': {}, 'seance': {}}
    for cat, (lab, coul) in RUBRIQUES.items():
        L = sorted((x for x in ex.values() if x.get('cat') == cat), key=lambda x: x['id'])
        if L: jobs.append((f'{cat}.pdf', f'Cartes {lab}', L, coul)); idx['cat'][cat] = f'{cat}.pdf'
    for s in seances:
        L = [ex[i] for i in s['ids'] if i in ex]
        jobs.append((f"{s['id']}.pdf", f"Séance {s['nom']}", L, RUBRIQUES[s['cat']][1])); idx['seance'][s['id']] = f"{s['id']}.pdf"
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        b = pw.chromium.launch(); pg = b.new_page()
        for f, t, L, c in jobs:
            pg.set_content(doc(t, L, comptes, c), wait_until='load')
            pg.pdf(path=str(OUT / f), format='A4', print_background=True, margin={k: '10mm' for k in ('top', 'bottom', 'left', 'right')})
            print(f, len(L), 'exercices', (OUT / f).stat().st_size // 1024, 'Ko')
        b.close()
    (ROOT / 'data/sport_cartes.json').write_text(json.dumps(idx, separators=(',', ':')))


if __name__ == '__main__':
    main()
