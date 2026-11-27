#!/usr/bin/env python3
"""Avatar livré en planches GPT (3 × 2 cases de 512 px) → fichiers de l'appli.
  python3 tools/avatar_planches.py DOSSIER_ZIP AVATAR_ID NOM
    AVATAR_ID ex. avatar-17_9-13-ans ; NOM ex. garcon_peau-claire_cheveux-blonds-boucles_teddy-marine_3d
Entrées : 00_reference.png, 01_marche_face.png, 02_marche_dos.png, 03_poses.png,
          04..NN_<humeur>_<geste>.png  (humeur : content, super_content, pas_bien, pas_bien_du_tout)
Sorties : avatars/<id>_<nom>_neutre.png, avatars/<id>_<nom>_<humeur>_<geste>.gif (288×320, 6 images),
          assets/interieur/av/<id>_{walk_front,walk_back,poses}.webp (+ liste.json),
          et la liste des GIF par humeur (à coller dans GIF_MAP).
"""
import glob, json, os, re, sys
import numpy as np
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import iso_avatars as iso

HUMEURS = [('super_content', 'superContent', 'super-content'), ('pas_bien_du_tout', 'pasBienDuTout', 'pas-bien-du-tout'),
           ('pas_bien', 'pasBien', 'pas-bien'), ('content', 'content', 'content')]


def gif(path, out, W=288, H=320, ms=160):
    cs = iso.cases(path)
    bs = [iso.bbox(c) for c in cs]
    bs = [b for b in bs if b]
    x0, y0 = min(b[0] for b in bs), min(b[1] for b in bs)
    x1, y1 = max(b[2] for b in bs), max(b[3] for b in bs)
    k = min((W - 12) / (x1 - x0 + 1), (H - 8) / (y1 - y0 + 1))
    frames = []
    for c in cs:
        im = Image.fromarray(c[y0:y1 + 1, x0:x1 + 1]).resize((round((x1 - x0 + 1) * k), round((y1 - y0 + 1) * k)), Image.LANCZOS)
        fr = Image.new('RGBA', (W, H)); fr.alpha_composite(im, ((W - im.width) // 2, H - 4 - im.height))
        a = fr.getchannel('A')
        p = fr.convert('RGB').quantize(255, method=Image.Quantize.MEDIANCUT)
        p.paste(255, mask=a.point(lambda v: 255 if v < 128 else 0)); p.info['transparency'] = 255
        frames.append(p)
    frames[0].save(out, save_all=True, append_images=frames[1:], duration=ms, loop=0, transparency=255, disposal=2)


def main():
    src, aid, nom = sys.argv[1:4]
    base = f'{aid}_{nom}'
    av = os.path.join(ROOT, 'avatars')
    ref = Image.open(os.path.join(src, '00_reference.png')).convert('RGBA')
    ref.save(os.path.join(av, f'{base}_neutre.png'), optimize=True)
    gm = {}
    for f in sorted(glob.glob(os.path.join(src, '[0-9][0-9]_*.png'))):
        n = os.path.basename(f)[3:-4]
        for cle, js, slug in HUMEURS:
            if n.startswith(cle + '_'):
                geste = n[len(cle) + 1:].replace('_', '-')
                out = f'{base}_{slug}_{geste}.gif'
                gif(f, os.path.join(av, out)); gm.setdefault(js, []).append('avatars/' + out)
                break
    # Mon monde : 3 bandes, même méthode que tools/iso_avatars.py
    tr = aid.split('_', 1)[1]
    cw = iso.cases(os.path.join(src, '01_marche_face.png'))
    hs = sorted(iso.bbox(c)[3] - iso.bbox(c)[1] + 1 for c in cw if iso.bbox(c))
    s = iso.HAUT[tr] / hs[len(hs) // 2]
    for k, f in (('walk_front', '01_marche_face.png'), ('walk_back', '02_marche_dos.png'), ('poses', '03_poses.png')):
        cs = cw if k == 'walk_front' else iso.cases(os.path.join(src, f))
        iso.bande(cs, s, [245, 245, 245, 245, 245, 236] if k == 'poses' else None).save(
            os.path.join(iso.OUT, f'{aid}_{k}.webp'), 'WEBP', quality=88, method=6)
    lp = os.path.join(iso.OUT, 'liste.json'); L = json.load(open(lp))
    if aid not in L: L.append(aid); json.dump(sorted(L), open(lp, 'w'))
    print(json.dumps({'f': f'avatars/{base}_neutre.png', 'gif': gm}, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()
