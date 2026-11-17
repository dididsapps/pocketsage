"""Planches isométriques des avatars (3 × 2 cases de 512 px) → bandes 6 × 256 px pour Mon Monde.
  python3 tools/iso_avatars.py DOSSIER_PLANCHES
Sortie : assets/interieur/av/{avatar-NN_tranche}_{walk_front|walk_back|poses}.webp
Pieds alignés (y = 245), personnage centré, même échelle pour les 3 planches d'un avatar.
Taille selon l'âge : les petits sont plus petits que les ados et les adultes.
"""
import glob, json, os, sys
import numpy as np
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'assets/interieur/av')
HAUT = {'4-8-ans': 178, '9-13-ans': 202, '14-18-ans': 224, '18-et-plus': 238}   # hauteur debout (px sur 256)
PLANCHES = {'walk_front': 'marche_bas-gauche_1536', 'walk_back': 'marche_haut-gauche_vue-dos', 'poses': '6-poses_actions'}


def cases(path):
    im = np.array(Image.open(path).convert('RGBA'))
    im[im[..., 3] < 48] = 0                       # voile alpha presque invisible → transparent
    return [im[r * 512:(r + 1) * 512, c * 512:(c + 1) * 512] for r in range(2) for c in range(3)]


def bbox(c):
    ys, xs = np.nonzero(c[..., 3] > 24)
    return (xs.min(), ys.min(), xs.max(), ys.max()) if len(xs) else None


def bande(cs, s, bas=None):
    out = Image.new('RGBA', (1536, 256))
    for i, c in enumerate(cs):
        b = bbox(c)
        if not b: continue
        x0, y0, x1, y1 = b
        crop = Image.fromarray(c[y0:y1 + 1, x0:x1 + 1])
        k = s
        if (x1 - x0 + 1) * k > 250: k = 250 / (x1 - x0 + 1)    # allongé : ne pas déborder de la case
        w, h = max(1, round((x1 - x0 + 1) * k)), max(1, round((y1 - y0 + 1) * k))
        crop = crop.resize((w, h), Image.LANCZOS)
        yb = (bas[i] if bas else 245)
        out.alpha_composite(crop, (i * 256 + 128 - w // 2, max(0, yb - h + 1)))
    return out


def main():
    src = sys.argv[1]; os.makedirs(OUT, exist_ok=True); liste = []
    for tr, cible in HAUT.items():
        for d in sorted(glob.glob(os.path.join(src, tr, 'avatar-*'))):
            num = os.path.basename(d); aid = f'{num}_{tr}'
            f = {k: (glob.glob(os.path.join(d, f'*{v}*.png')) or [None])[0] for k, v in PLANCHES.items()}
            if not all(f.values()): print('⚠️ incomplet', aid); continue
            cw = cases(f['walk_front'])
            hs = sorted(bbox(c)[3] - bbox(c)[1] + 1 for c in cw if bbox(c))
            s = cible / hs[len(hs) // 2]                # échelle d'après la hauteur médiane de marche
            for k in PLANCHES:
                cs = cw if k == 'walk_front' else cases(f[k])
                b = bande(cs, s, [245, 245, 245, 245, 245, 236] if k == 'poses' else None)
                b.save(os.path.join(OUT, f'{aid}_{k}.webp'), 'WEBP', quality=88, method=6)
            liste.append(aid)
    json.dump(sorted(liste), open(os.path.join(OUT, 'liste.json'), 'w'))
    print(len(liste), 'avatars')


if __name__ == '__main__':
    main()
