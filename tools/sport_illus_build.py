#!/usr/bin/env python3
"""Construit les illustrations des exercices de sport à partir du manifeste.

Lit docs/contenu/sport/illustrations/manifeste.json :
  {"<ID>": [{"src": "cases/xxx.png", "box": [x0,y0,x1,y1], "miroir": false,
             "blanc": [[x0,y0,x1,y1], ...],   # optionnel : zones à effacer (coord. source)
             "retouche": [[x0,y0,x1,y1], ...],# optionnel : zones remplacées par le reflet de la zone du dessous
             "echelle": 1.0},                  # optionnel : facteur de taille source
            ...], "_notes": [...]}
Produit assets/sport/<ID>-<n>.webp (480x480, fond blanc, même échelle pour toutes
les étapes d'un exercice, personnage centré et posé en bas avec 6 % de marge)
et data/sport_illus.json = {"<ID>": nombre d'étapes}.
"""
import json
import os
import sys

import numpy as np
from PIL import Image
from scipy import ndimage as ndi

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ILLUS = os.path.join(RACINE, 'docs/contenu/sport/illustrations')
MANIFESTE = os.path.join(ILLUS, 'manifeste.json')
SORTIE = os.path.join(RACINE, 'assets/sport')
COMPTES = os.path.join(RACINE, 'data/sport_illus.json')

TAILLE = 480
MARGE_BAS = 0.06
MARGE_HAUT = 0.05
MARGE_COTES = 0.04
INSET = 10          # pixels rognés à l'intérieur du cadre
QUALITE = 82

_cache = {}


def charger(src):
    if src not in _cache:
        _cache[src] = np.asarray(Image.open(os.path.join(ILLUS, src)).convert('RGB')).copy()
    return _cache[src]


def blanchir_presque_blanc(a):
    mn = a.min(axis=2).astype(int)
    mx = a.max(axis=2).astype(int)
    m = (mn >= 226) & (mx - mn <= 34)
    a[m] = 255
    return a


def effacer_traits(a, k=6, long_min=120):
    """Efface les traits fins et longs entourés de blanc (restes de cadres)."""
    g = a.min(axis=2)
    dark = g < 215
    white = g > 240
    H, W = g.shape

    def dec(m, dy, dx):
        o = np.ones_like(m)
        ys = slice(max(dy, 0), H + min(dy, 0)); yd = slice(max(-dy, 0), H + min(-dy, 0))
        xs = slice(max(dx, 0), W + min(dx, 0)); xd = slice(max(-dx, 0), W + min(-dx, 0))
        o[ys, xs] = m[yd, xd]
        return o

    hm = dark & dec(white, k, 0) & dec(white, -k, 0)
    vm = dark & dec(white, 0, k) & dec(white, 0, -k)
    hm = ndi.binary_closing(hm, structure=np.ones((1, 9)))
    vm = ndi.binary_closing(vm, structure=np.ones((9, 1)))
    trait = np.zeros_like(dark)
    for m, axe in ((hm, 1), (vm, 0)):
        lab, n = ndi.label(m, structure=np.ones((3, 3)))
        for i, sl in enumerate(ndi.find_objects(lab), 1):
            h = sl[0].stop - sl[0].start
            w = sl[1].stop - sl[1].start
            longueur, epaisseur = (w, h) if axe == 1 else (h, w)
            if longueur >= long_min and epaisseur <= 14:
                trait[sl] |= lab[sl] == i
    trait = ndi.binary_dilation(trait, iterations=3) & (g < 250)
    # ne garder que la partie du trait réellement claire autour (pas les contours du personnage)
    a[trait] = 255
    return a


def nettoyer_bords(a):
    """Retire les petites taches et les morceaux de cadre qui touchent le bord."""
    g = a.min(axis=2)
    ink = g < 236
    lab, n = ndi.label(ink, structure=np.ones((3, 3)))
    H, W = g.shape
    for i, sl in enumerate(ndi.find_objects(lab), 1):
        h = sl[0].stop - sl[0].start
        w = sl[1].stop - sl[1].start
        comp = lab[sl] == i
        aire = comp.sum()
        touche = sl[0].start <= 1 or sl[1].start <= 1 or sl[0].stop >= H - 1 or sl[1].stop >= W - 1
        if aire < 40 or (touche and (h <= 16 or w <= 16)) or (touche and aire < 300):
            a[sl][comp] = 255
    return a


def extraire(etape):
    a = charger(etape['src']).copy()
    for x0, y0, x1, y1 in etape.get('blanc', []):
        a[y0:y1, x0:x1] = 255
    for x0, y0, x1, y1 in etape.get('retouche', []):
        # reflet vertical de la zone située juste en dessous (garde la texture de l'ombre)
        a[y0:y1, x0:x1] = a[y1:y1 + (y1 - y0), x0:x1][::-1]
    if 'box' in etape:
        x0, y0, x1, y1 = etape['box']
        H, W = a.shape[:2]
        x0 = max(0, x0 + INSET); y0 = max(0, y0 + INSET)
        x1 = min(W, x1 - INSET); y1 = min(H, y1 - INSET)
        a = a[y0:y1, x0:x1].copy()
    a = effacer_traits(a)
    a = blanchir_presque_blanc(a)
    a = nettoyer_bords(a)
    ink = a.min(axis=2) < 245
    ys, xs = np.where(ink)
    if len(ys) == 0:
        raise ValueError(f"case vide : {etape}")
    a = a[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    im = Image.fromarray(a)
    if etape.get('miroir'):
        im = im.transpose(Image.FLIP_LEFT_RIGHT)
    return im


def construire(ident, etapes):
    images = [extraire(e) for e in etapes]
    facteurs = [float(e.get('echelle', 1.0)) for e in etapes]
    larg_max = TAILLE * (1 - 2 * MARGE_COTES)
    haut_max = TAILLE * (1 - MARGE_BAS - MARGE_HAUT)
    echelle = min(min(larg_max / (im.width * f), haut_max / (im.height * f))
                  for im, f in zip(images, facteurs))
    sol = round(TAILLE * (1 - MARGE_BAS))
    chemins = []
    for n, (im, f) in enumerate(zip(images, facteurs), 1):
        s = echelle * f
        w = max(1, round(im.width * s)); h = max(1, round(im.height * s))
        r = im.resize((w, h), Image.LANCZOS)
        toile = Image.new('RGB', (TAILLE, TAILLE), (255, 255, 255))
        toile.paste(r, ((TAILLE - w) // 2, sol - h))
        chemin = os.path.join(SORTIE, f'{ident}-{n}.webp')
        toile.save(chemin, 'WEBP', quality=QUALITE, method=6)
        chemins.append(chemin)
    return chemins


def main(ids=None):
    manifeste = json.load(open(MANIFESTE, encoding='utf-8'))
    os.makedirs(SORTIE, exist_ok=True)
    comptes = {}
    for ident, etapes in manifeste.items():
        if ident.startswith('_'):
            continue
        comptes[ident] = len(etapes)
        if ids and ident not in ids:
            continue
        # supprime d'anciennes étapes en trop
        n = len(etapes) + 1
        while os.path.exists(os.path.join(SORTIE, f'{ident}-{n}.webp')):
            os.remove(os.path.join(SORTIE, f'{ident}-{n}.webp'))
            n += 1
        construire(ident, etapes)
    os.makedirs(os.path.dirname(COMPTES), exist_ok=True)
    with open(COMPTES, 'w', encoding='utf-8') as f:
        json.dump(comptes, f, ensure_ascii=False, indent=1)
    total = sum(os.path.getsize(os.path.join(SORTIE, x)) for x in os.listdir(SORTIE) if x.endswith('.webp'))
    print(f'{len(comptes)} exercices, {sum(comptes.values())} images, {total / 1024:.0f} Ko')


if __name__ == '__main__':
    main(sys.argv[1:] or None)
