"""Fiches de révision : données de l'appli + PDF à imprimer.
Source (vérifiée par la moulinette) : docs/contenu/fiches/<LANG>/REV-<CODE>-<CL>.json
Sorties : data/fiches/<LANG>/<CL>.json  ({code: {matiere, fiches:[…]}}), data/fiches/index.json ({CL: [codes]})
          fiches/<LANG>/REV-<CODE>-<CL>.pdf  (avec --pdf)
  python3 tools/fiches_build.py [--pdf]
"""
import html, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / 'docs/contenu/fiches'
PETITS = ('GS', 'CP', 'CE1', 'CE2')
NOMCL = {'GS': 'Grande section', 'CP': 'CP', 'CE1': 'CE1', 'CE2': 'CE2', 'CM1': 'CM1', 'CM2': 'CM2', '6E': '6e', '5E': '5e', '4E': '4e',
         '3E': '3e', '2DE': 'Seconde', '1RE': 'Première', 'TLE': 'Terminale'}
COUL = {'FR': '#E8590C', 'MA': '#3B82F6', 'QM': '#10B981', 'SC': '#10B981', 'SVT': '#16A34A', 'PC': '#0EA5E9', 'TE': '#64748B', 'HI': '#B45309',
        'GE': '#0D9488', 'SES': '#7C3AED', 'ESC': '#0891B2', 'PHI': '#9333EA', 'HGG': '#A16207', 'AN': '#DC2626', 'ES': '#D97706'}


def fiche_lue(f):
    """Morceaux lus à voix haute, dans l'ordre exact de l'affichage (js/fiches.js, éléments .fi-lu)."""
    out = [f.get('titre'), f.get('en_une_phrase'), f.get('comprendre'), *f.get('essentiel', []), f.get('image_mentale'),
           f.get('regle_ou_methode'), *f.get('exemples', []), f.get('piege'), f.get('astuce_memoire')]
    return [x.strip() for x in out if x and x.strip()]


def fichiers(lang='FR'):
    for p in sorted((SRC / lang).glob('REV-*.json')):
        d = json.loads(p.read_text(encoding='utf-8'))
        yield p, d


def donnees():
    index = {}
    for ld in sorted(x for x in SRC.iterdir() if x.is_dir()):
        par = {}
        for p, d in fichiers(ld.name):
            _, code, cl = p.stem.split('-')
            par.setdefault(cl, {})[code] = {'matiere': d.get('matiere'), 'fiches': d['fiches']}
            if ld.name == 'FR': index.setdefault(cl, []).append(code)
        out = ROOT / 'data/fiches' / ld.name; out.mkdir(parents=True, exist_ok=True)
        for cl, v in par.items():
            (out / f'{cl}.json').write_text(json.dumps(v, ensure_ascii=False, separators=(',', ':')), encoding='utf-8')
    (ROOT / 'data/fiches/index.json').write_text(json.dumps(index, separators=(',', ':')))
    print('données :', sum(len(v) for v in index.values()), 'matières,', len(index), 'classes')


E = lambda s: html.escape(str(s or ''))


def page(d, code, cl):
    c = COUL.get(code, '#6C63FF')
    css = f"""@page{{size:A4;margin:12mm 12mm 14mm}}*{{box-sizing:border-box}}body{{font-family:'Nunito','DejaVu Sans',Arial,sans-serif;color:#1F2937;font-size:10.5pt;margin:0}}
h1{{font-size:20pt;margin:0;color:{c}}}.sub{{color:#6B7280;font-size:10pt;margin:2px 0 10px}}
.axe{{font-size:12pt;font-weight:800;color:#fff;background:{c};padding:5px 10px;border-radius:8px;margin:12px 0 6px;break-after:avoid}}
.f{{border:1.5px solid {c}55;border-radius:12px;padding:9px 12px;margin:0 0 9px;break-inside:avoid}}
.t{{font-size:13pt;font-weight:800;margin:0 0 4px}}.cle{{background:{c}18;border-left:4px solid {c};padding:5px 8px;border-radius:6px;font-weight:700;margin:4px 0}}
.b{{margin:5px 0}}.bt{{font-weight:800;color:{c};font-size:9.5pt;text-transform:uppercase;letter-spacing:.04em}}.b p,.b ul{{margin:2px 0}}.b ul{{padding-left:17px}}
.pie{{background:#FEF3C7;border-radius:6px;padding:4px 8px}}.q{{margin:3px 0}}.ch{{margin-left:12px}}.box{{display:inline-block;width:9px;height:9px;border:1.2px solid #555;border-radius:2px;margin-right:4px}}
.rep{{transform:rotate(180deg);font-size:8.5pt;color:#6B7280;text-align:right;margin-top:4px}}.pied{{font-size:8pt;color:#9CA3AF;text-align:center;margin-top:8px}}"""
    h = [f"<html><head><meta charset='utf-8'><style>{css}</style></head><body>",
         f"<h1>{E(d.get('matiere'))} — {E(NOMCL.get(cl, cl))}</h1><div class='sub'>Fiches de révision PocketSage · lis, cache la fiche, puis teste-toi !</div>"]
    axe = None
    for f in d['fiches']:
        if f['axe'] != axe: axe = f['axe']; h.append(f"<div class='axe'>{E(axe)}</div>")
        li = lambda a: '<ul>' + ''.join(f'<li>{E(x)}</li>' for x in a) + '</ul>' if a else ''
        bl = lambda t, x, cls='': f"<div class='b {cls}'><div class='bt'>{t}</div>{x}</div>" if x else ''
        p = lambda x: f'<p>{E(x)}</p>' if x else ''
        qs = ''.join(f"<div class='q'><b>{i + 1}.</b> {E(q['q'])}<div class='ch'>" + ' &nbsp; '.join(f"<span class='box'></span>{E(c_)}" for c_ in q['choix']) + '</div></div>'
                     for i, q in enumerate(f.get('quiz', [])))
        rep = ' · '.join(f"{i + 1}. {E(q['rep'])}" for i, q in enumerate(f.get('quiz', [])))
        h.append(f"<div class='f'><div class='t'>{E(f.get('emoji'))} {E(f['titre'])}</div><div class='cle'>{E(f.get('en_une_phrase'))}</div>"
                 + bl('Comprendre', p(f.get('comprendre'))) + bl('À retenir', li(f.get('essentiel'))) + bl('Image pour retenir', p(f.get('image_mentale')))
                 + bl('Règle ou méthode', p(f.get('regle_ou_methode'))) + bl('Exemples', li(f.get('exemples'))) + bl('Le piège', p(f.get('piege')), 'pie')
                 + bl('Astuce', p(f.get('astuce_memoire'))) + bl('Je me teste (sans regarder)', qs) + f"<div class='rep'>Réponses : {rep}</div></div>")
    h.append("<div class='pied'>pocketsage.org · fiches vérifiées · programme officiel de l'Éducation nationale</div></body></html>")
    return ''.join(h)


def pdfs():
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        b = pw.chromium.launch(); pg = b.new_page(); n = 0
        for ld in sorted(x for x in SRC.iterdir() if x.is_dir()):
            out = ROOT / 'fiches' / ld.name; out.mkdir(parents=True, exist_ok=True)
            for p, d in fichiers(ld.name):
                _, code, cl = p.stem.split('-')
                pg.set_content(page(d, code, cl), wait_until='load')
                pg.pdf(path=str(out / f'{p.stem}.pdf'), format='A4', print_background=True,
                       margin={'top': '12mm', 'bottom': '14mm', 'left': '12mm', 'right': '12mm'}); n += 1
        b.close()
    print('PDF :', n)


if __name__ == '__main__':
    donnees()
    if '--pdf' in sys.argv: pdfs()
