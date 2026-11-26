#!/usr/bin/env python3
"""Animations de l'avatar vectoriel articulé (SVG à groupes : avatar, leg-l/shin-l, leg-r/shin-r, arm-l/forearm-l, arm-r/forearm-r, torso, head).
Chaque animation = expression du visage + images clés (rotations en degrés, décalages en px), interpolées en douceur.
Sortie : GIF transparents 320×360 (24 images, 80 ms) + PNG neutre.
  python3 tools/avatar_anim.py SVG_NEUTRE DOSSIER_SORTIE PREFIXE
Angles : bras gauche (à gauche de l'écran) + = lever vers l'extérieur ; bras droit − = lever vers l'extérieur.
"""
import io, math, re, sys
from PIL import Image

N, MS = 24, 80

# ── visages : remplacent la bouche (+ sourcils, larmes) du SVG neutre ──
SOUR_OK = ('<path d="M-19 -36 q6 -5 12 0" {s}/>', '<path d="M7 -36 q6 -5 12 0" {s}/>')
SOUR_KO = ('<path d="M-19 -36 q6 5 12 0" {s}/>', '<path d="M7 -36 q6 5 12 0" {s}/>')
ST = 'fill="none" stroke="#59483e" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"'
BOUCHES = {
    'sourire': '<path d="M-10 -8 Q0 0 10 -8" fill="none" stroke="#59483e" stroke-width="2.5" stroke-linecap="round"/>',
    'rire': '<path d="M-14 -10 Q0 -3 14 -10 Q10 8 0 7 Q-10 8 -14 -10Z" fill="#713e3b" stroke="#59483e" stroke-width="2" stroke-linejoin="round"/>'
            '<path d="M-11 -8 Q0 -3 11 -8 L9 -3 Q0 0 -9 -3Z" fill="#fff"/>',
    'triste': '<path d="M-11 -5 Q0 -15 11 -5" fill="none" stroke="#59483e" stroke-width="2.5" stroke-linecap="round"/>',
    'oh': '<ellipse cx="0" cy="-7" rx="5" ry="6" fill="#713e3b" stroke="#59483e" stroke-width="2"/>',
    'moue': '<path d="M-9 -6 Q-3 -9 0 -6 Q4 -3 9 -7" fill="none" stroke="#59483e" stroke-width="2.5" stroke-linecap="round"/>',
}
LARMES = '<ellipse cx="-14" cy="-17" rx="2" ry="5" fill="#72c6ec"/><ellipse cx="14" cy="-17" rx="2" ry="5" fill="#72c6ec"/>'
YEUX_FERMES = ('<path d="M-17 -28 q4 3 8 0" {s}/>', '<path d="M9 -28 q4 3 8 0" {s}/>')


def visage(svg, bouche, sourcils='ok', larmes=False, rire_yeux=False):
    s = svg
    s = re.sub(r'<path d="M-9 -7 Q0 -3 9 -7"[^>]*/>', BOUCHES[bouche] + (LARMES if larmes else ''), s)
    so = SOUR_KO if sourcils == 'ko' else SOUR_OK
    s = re.sub(r'<path d="M-19 -36 q6 -5 12 0"[^>]*/>', so[0].format(s=ST), s)
    s = re.sub(r'<path d="M7 -36 q6 -5 12 0"[^>]*/>', so[1].format(s=ST), s)
    if rire_yeux:   # yeux plissés de joie
        s = re.sub(r'<ellipse cx="-13" cy="-28" rx="4" ry="5"[^>]*/><ellipse cx="-12" cy="-30"[^>]*/>', YEUX_FERMES[0].format(s=ST), s)
        s = re.sub(r'<ellipse cx="13" cy="-28" rx="4" ry="5"[^>]*/><ellipse cx="14" cy="-30"[^>]*/>', YEUX_FERMES[1].format(s=ST), s)
    return s


BASE = {}   # id -> (tx, ty) d'origine


def pose(svg, p):
    """p : {id: rot} ou {id: (rot, dx, dy)} ; 'avatar' accepte aussi sx (écrasement)."""
    def rep(m):
        gid, tx, ty = m.group(1), float(m.group(2)), float(m.group(3))
        r, dx, dy, sx, sy = norm(p.get(gid, 0))
        sc = f' scale({sx:.3f} {sy:.3f})' if gid == 'avatar' else ''
        return f'<g id="{gid}" transform="translate({tx + dx:.2f} {ty + dy:.2f}) rotate({r:.2f}){sc}">'
    return re.sub(r'<g id="([\w-]+)" transform="translate\(([-\d.]+) ([-\d.]+)\) rotate\([-\d.]+\)(?: scale\([^)]*\))?">', rep, svg)


def norm(v):
    v = tuple(v) if isinstance(v, tuple) else (v,)
    return v + (0, 0, 0, 1, 1)[len(v):]


def ease(t):
    return 0.5 - 0.5 * math.cos(math.pi * t)


def interp(keys, t):
    """keys : liste de poses (cycle) ; t ∈ [0,1[."""
    n = len(keys); x = t * n; i = int(x) % n; f = ease(x - int(x)); a, b = keys[i], keys[(i + 1) % n]
    out = {}
    for k in set(a) | set(b):
        ta, tb = norm(a.get(k, 0)), norm(b.get(k, 0))
        out[k] = tuple(ta[j] + (tb[j] - ta[j]) * f for j in range(5))
    return out


# ── animations ── (chaque liste = images clés d'un cycle)
UP_L, UP_R = 155, -155
ANIMS = {
    # CONTENT
    'content_bras-en-v': dict(face=('rire', 'ok', False, True), keys=[
        {'arm-l': 20, 'arm-r': -20, 'leg-l': 0, 'shin-l': 0, 'avatar': (0, 0, 8)},
        {'arm-l': UP_L, 'arm-r': UP_R, 'forearm-l': -10, 'forearm-r': 10, 'avatar': (0, 0, -34), 'leg-l': 6, 'leg-r': -6},
        {'arm-l': UP_L, 'arm-r': UP_R, 'forearm-l': -10, 'forearm-r': 10, 'avatar': (0, 0, -30), 'leg-l': 6, 'leg-r': -6},
        {'arm-l': 30, 'arm-r': -30, 'avatar': (0, 0, 6)}]),
    'content_poing-leve': dict(face=('rire', 'ok', False, False), keys=[
        {'arm-r': -40, 'forearm-r': -100, 'arm-l': 8, 'head': 4},
        {'arm-r': -150, 'forearm-r': -20, 'arm-l': 10, 'head': -4, 'avatar': (0, 0, -6)},
        {'arm-r': -40, 'forearm-r': -110, 'arm-l': 8, 'head': 4, 'avatar': (0, 0, 2)},
        {'arm-r': -150, 'forearm-r': -20, 'arm-l': 10, 'head': -4, 'avatar': (0, 0, -6)}]),
    'content_sautille': dict(face=('sourire', 'ok', False, False), keys=[
        {'avatar': (0, 0, 4), 'arm-l': 25, 'arm-r': -10, 'forearm-l': -30, 'forearm-r': 30, 'shin-l': 6, 'shin-r': -6},
        {'avatar': (0, 0, -16), 'arm-l': 10, 'arm-r': -25, 'forearm-l': -30, 'forearm-r': 30, 'head': 5},
        {'avatar': (0, 0, 4), 'arm-l': 10, 'arm-r': -25, 'forearm-l': -30, 'forearm-r': 30, 'shin-l': 6, 'shin-r': -6},
        {'avatar': (0, 0, -16), 'arm-l': 25, 'arm-r': -10, 'forearm-l': -30, 'forearm-r': 30, 'head': -5}]),
    'content_coucou': dict(face=('rire', 'ok', False, True), keys=[
        {'arm-l': 140, 'forearm-l': 20, 'arm-r': -140, 'forearm-r': 20, 'head': -4},
        {'arm-l': 140, 'forearm-l': -20, 'arm-r': -140, 'forearm-r': -20, 'head': 4}]),
    'super-content_danse': dict(face=('rire', 'ok', False, False), keys=[
        {'avatar': (6, -8, 4), 'arm-l': 120, 'forearm-l': -40, 'arm-r': -30, 'forearm-r': -60, 'leg-l': 12, 'shin-l': -18, 'head': 8, 'torso': 4},
        {'avatar': (0, 0, -6), 'arm-l': 30, 'arm-r': -30, 'head': 0},
        {'avatar': (-6, 8, 4), 'arm-r': -120, 'forearm-r': 40, 'arm-l': 30, 'forearm-l': 60, 'leg-r': -12, 'shin-r': 18, 'head': -8, 'torso': -4},
        {'avatar': (0, 0, -6), 'arm-l': 30, 'arm-r': -30, 'head': 0}]),
    'super-content_saut-etoile': dict(face=('rire', 'ok', False, True), keys=[
        {'avatar': (0, 0, 10), 'leg-l': 0, 'leg-r': 0, 'shin-l': 8, 'shin-r': -8, 'arm-l': 10, 'arm-r': -10},
        {'avatar': (0, 0, -40), 'arm-l': 130, 'arm-r': -130, 'leg-l': 28, 'leg-r': -28},
        {'avatar': (0, 0, -36), 'arm-l': 135, 'arm-r': -135, 'leg-l': 30, 'leg-r': -30},
        {'avatar': (0, 0, 6), 'leg-l': 0, 'leg-r': 0, 'shin-l': 6, 'shin-r': -6, 'arm-l': 15, 'arm-r': -15}]),
    # PAS BIEN
    'pas-bien_epaules-tombantes': dict(face=('triste', 'ko', False, False), keys=[
        {'head': (4, 0, 0), 'arm-l': 4, 'arm-r': -4, 'avatar': (0, 0, -2)},
        {'head': (24, 0, 8), 'arm-l': -6, 'arm-r': 6, 'torso': 3, 'avatar': (0, 0, 9)},
        {'head': (22, 0, 7), 'arm-l': -6, 'arm-r': 6, 'torso': 3, 'avatar': (0, 0, 8)}]),
    'pas-bien_oh-non': dict(face=('oh', 'ko', False, False), keys=[
        {'arm-l': 35, 'forearm-l': 75, 'arm-r': -35, 'forearm-r': -75, 'head': 0, 'avatar': (0, 0, 0)},
        {'arm-l': 50, 'forearm-l': 85, 'arm-r': -50, 'forearm-r': -85, 'head': -8, 'avatar': (0, 0, -4)},
        {'arm-l': 35, 'forearm-l': 75, 'arm-r': -35, 'forearm-r': -75, 'head': 8, 'avatar': (0, 0, 0)}]),
    'pas-bien_secoue-la-tete': dict(face=('moue', 'ko', False, False), keys=[
        {'head': -18, 'arm-l': 8, 'arm-r': -4, 'torso': -2}, {'head': 18, 'arm-l': 4, 'arm-r': -8, 'torso': 2}]),
    'pas-bien-du-tout_tape-du-pied': dict(face=('triste', 'ko', False, False), keys=[
        {'head': (14, 0, 4), 'arm-l': -3, 'arm-r': 3, 'leg-r': 0, 'shin-r': 0},
        {'head': (16, 0, 5), 'arm-l': -3, 'arm-r': 3, 'leg-r': -22, 'shin-r': 30, 'avatar': (0, 0, 0)},
        {'head': (14, 0, 4), 'arm-l': -3, 'arm-r': 3, 'leg-r': 0, 'shin-r': 0}]),
    'pas-bien-du-tout_pleure': dict(face=('triste', 'ko', True, False), keys=[
        {'arm-l': -6, 'arm-r': 6, 'head': (14, 0, 5), 'avatar': (0, 0, 5)},
        {'arm-l': -4, 'arm-r': 4, 'head': (8, 0, 3), 'avatar': (0, 0, 2)},
        {'arm-l': -6, 'arm-r': 6, 'head': (14, 0, 5), 'avatar': (0, 0, 5)},
        {'arm-l': -4, 'arm-r': 4, 'head': (10, 0, 4), 'avatar': (0, 0, 3)}]),
}


def rendu(svg_base, nom, a, pg):
    f = visage(svg_base, *a['face'])
    frames = []
    for i in range(N):
        s = pose(f, interp(a['keys'], i / N))
        pg.set_content(f'<html><body style="margin:0;background:transparent">{s}</body></html>')
        png = pg.locator('svg').screenshot(omit_background=True)
        frames.append(Image.open(io.BytesIO(png)).convert('RGBA'))
    return frames


def gif(frames, path):
    pal = []
    for fr in frames:
        a = fr.getchannel('A')
        p = fr.convert('RGB').quantize(255, method=Image.Quantize.MEDIANCUT)
        p.paste(255, mask=a.point(lambda v: 255 if v < 110 else 0))
        p.info['transparency'] = 255
        pal.append(p)
    pal[0].save(path, save_all=True, append_images=pal[1:], duration=MS, loop=0, transparency=255, disposal=2, optimize=False)


def main():
    src, out, pre = sys.argv[1], sys.argv[2], sys.argv[3]
    svg = open(src, encoding='utf-8').read()
    from playwright.sync_api import sync_playwright
    import os
    os.makedirs(out, exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 320, 'height': 360})
        for nom, a in ANIMS.items():
            fr = rendu(svg, nom, a, pg)
            gif(fr, f'{out}/{pre}_{nom}.gif'); print(nom)
        pg.set_content(f'<html><body style="margin:0;background:transparent">{visage(svg, "sourire")}</body></html>')
        pg.locator('svg').screenshot(path=f'{out}/{pre}_neutre.png', omit_background=True)
        b.close()


if __name__ == '__main__':
    main()
