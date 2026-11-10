#!/usr/bin/env python3
"""
PocketSage — Tutos origami pas à pas (annexe de la fiche FI-029)
3 pages : grenouille sauteuse, bateau en papier, grue traditionnelle.
Schémas dessinés par PocketSage (modèles traditionnels, libres de droits).

Sortie : fiches/FR/FI-029-tutos.pdf   (puis rclone copy fiches/FR r2:pocketsage-audio/fiches/FR)
"""
import math, os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas

W, H = A4
GREY = "#CFCFCF"      # face colorée du papier (gris clair : économie d'encre)
WHITE = "#FFFFFF"     # face blanche
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fiches", "FR", "FI-029-tutos.pdf")


# ─── Outils de dessin ────────────────────────────────────────────────────────
class Box:
    """Transforme des coordonnées (0..1, 0..1) en points dans une case carrée."""
    def __init__(self, x, y, s):
        self.x, self.y, self.s = x, y, s
    def __call__(self, u, v):
        return (self.x + u*self.s, self.y + v*self.s)

def poly(c, B, pts, fill=GREY, lw=1.2):
    p = c.beginPath(); p.moveTo(*B(*pts[0]))
    for q in pts[1:]: p.lineTo(*B(*q))
    p.close()
    c.setStrokeColor(colors.black); c.setLineWidth(lw)
    if fill: c.setFillColor(HexColor(fill))
    c.drawPath(p, fill=1 if fill else 0, stroke=1)

def valley(c, B, a, b):
    """Pli vallée (on plie vers soi) : tirets."""
    c.setStrokeColor(colors.black); c.setLineWidth(0.9); c.setDash([4, 3])
    c.line(*B(*a), *B(*b)); c.setDash([])

def mountain(c, B, a, b):
    """Pli montagne (on plie vers l'arrière) : tiret-point."""
    c.setStrokeColor(colors.black); c.setLineWidth(0.9); c.setDash([6, 2, 1, 2])
    c.line(*B(*a), *B(*b)); c.setDash([])

def crease(c, B, a, b):
    """Pli déjà marqué : trait fin."""
    c.setStrokeColor(HexColor("#777777")); c.setLineWidth(0.5)
    c.line(*B(*a), *B(*b))

def arrow(c, B, a, b, bend=0.25, color="#D62828"):
    """Flèche courbe de a vers b (sens du pli)."""
    (x1, y1), (x2, y2) = B(*a), B(*b)
    mx, my = (x1+x2)/2, (y1+y2)/2
    dx, dy = x2-x1, y2-y1
    cx, cy = mx - dy*bend, my + dx*bend
    c.setStrokeColor(HexColor(color)); c.setFillColor(HexColor(color)); c.setLineWidth(1.3)
    p = c.beginPath(); p.moveTo(x1, y1); p.curveTo(cx, cy, cx, cy, x2, y2)
    c.drawPath(p, fill=0, stroke=1)
    ang = math.atan2(y2-cy, x2-cx); L = 6
    h = c.beginPath(); h.moveTo(x2, y2)
    h.lineTo(x2 - L*math.cos(ang-0.4), y2 - L*math.sin(ang-0.4))
    h.lineTo(x2 - L*math.cos(ang+0.4), y2 - L*math.sin(ang+0.4)); h.close()
    c.drawPath(h, fill=1, stroke=0)

def turn_over(c, B, u=0.84, v=0.08):
    """Symbole « retourne la feuille »."""
    x, y = B(u, v)
    c.setStrokeColor(HexColor("#1D70B8")); c.setFillColor(HexColor("#1D70B8")); c.setLineWidth(1.2)
    c.circle(x, y, 9, fill=0, stroke=1)
    c.setFont("Helvetica-Bold", 6.5); c.drawCentredString(x, y-2.3, "180°")

def legend(c, y):
    c.setFont("Helvetica", 8.5); c.setFillColor(colors.black)
    x = 1.4*cm
    c.setLineWidth(0.9); c.setDash([4, 3]); c.line(x, y+3, x+1.2*cm, y+3); c.setDash([])
    c.drawString(x+1.4*cm, y, "pli vallée (vers toi)")
    x += 5.0*cm
    c.setDash([6, 2, 1, 2]); c.line(x, y+3, x+1.2*cm, y+3); c.setDash([])
    c.drawString(x+1.4*cm, y, "pli montagne (vers l'arrière)")
    x += 6.0*cm
    c.setStrokeColor(HexColor("#1D70B8")); c.circle(x+0.3*cm, y+3, 8, fill=0, stroke=1)
    c.setFillColor(HexColor("#1D70B8")); c.setFont("Helvetica-Bold", 6.5); c.drawCentredString(x+0.3*cm, y+0.8, "180°")
    c.setFillColor(colors.black); c.setFont("Helvetica", 8.5); c.drawString(x+0.8*cm, y, "retourne la feuille")
    c.setStrokeColor(colors.black)

def page(c, title, level, paper, steps):
    """Une page = en-tête + 9 cases (3×3)."""
    c.setStrokeColor(colors.black); c.setLineWidth(1.2)
    c.roundRect(1*cm, H-3.2*cm, W-2*cm, 2.4*cm, 10, fill=0, stroke=1)
    c.setFillColor(colors.black); c.setFont("Helvetica-Bold", 9)
    c.drawString(1.5*cm, H-1.35*cm, "FICHE #29 — TUTO")
    c.drawRightString(W-1.5*cm, H-1.35*cm, level)
    c.setFont("Helvetica-Bold", 18); c.drawCentredString(W/2, H-2.15*cm, title)
    c.setFont("Helvetica", 9.5); c.drawCentredString(W/2, H-2.8*cm, paper)
    legend(c, H-3.9*cm)
    cols, rows = 3, 3
    gx = 0.35*cm
    cw = (W - 2*cm - (cols-1)*gx) / cols
    top = H - 4.4*cm
    ch = (top - 1.6*cm) / rows
    pic = min(cw - 0.8*cm, ch - 2.0*cm)
    for i, (txt, fn) in enumerate(steps[:9]):
        r, k = divmod(i, cols)
        x = 1*cm + k*(cw + gx); y = top - (r+1)*ch
        c.setStrokeColor(HexColor("#AAAAAA")); c.setLineWidth(0.6)
        c.roundRect(x, y+0.15*cm, cw, ch-0.3*cm, 8, fill=0, stroke=1)
        c.setFillColor(colors.black); c.circle(x+0.45*cm, y+ch-0.6*cm, 0.27*cm, fill=1, stroke=0)
        c.setFillColor(colors.white); c.setFont("Helvetica-Bold", 9)
        c.drawCentredString(x+0.45*cm, y+ch-0.69*cm, str(i+1))
        B = Box(x + (cw-pic)/2, y + 1.35*cm, pic)
        fn(c, B)
        c.setFillColor(colors.black); c.setFont("Helvetica", 8.3)
        for j, line in enumerate(wrap(txt, 44)[:3]):
            c.drawString(x+0.3*cm, y+1.0*cm - j*0.36*cm, line)
    c.setFont("Helvetica-Oblique", 7.5); c.setFillColor(HexColor("#888888"))
    c.drawCentredString(W/2, 0.9*cm, "PocketSage Academy — pocketsage.org — Schémas PocketSage, modèle traditionnel libre de droits")
    c.showPage()

def wrap(t, n):
    out, cur = [], ""
    for w in t.split():
        if len(cur) + len(w) + 1 > n:
            out.append(cur); cur = w
        else:
            cur = (cur + " " + w).strip()
    if cur: out.append(cur)
    return out


# ─── GRENOUILLE SAUTEUSE (rectangle 1 × 2) ───────────────────────────────────
# Rectangle dessiné de x=.3 à .7 (largeur .4), y=.05 à .85 (hauteur .8)
X0, X1, Y0, Y1 = .3, .7, .05, .85
YM = Y1 - .4                       # bas du carré du haut
YC = Y1 - .2                       # centre du X

def f1(c, B):
    poly(c, B, [(.1, .25), (.9, .25), (.9, .65), (.1, .65)])
    valley(c, B, (.5, .25), (.5, .65)); arrow(c, B, (.82, .45), (.18, .45), .3)
def f2(c, B):
    poly(c, B, [(X0, Y0), (X1, Y0), (X1, Y1), (X0, Y1)])
    valley(c, B, (X0, Y1), (X1, YM)); valley(c, B, (X1, Y1), (X0, YM))
    arrow(c, B, (X1-.02, Y1), (X0+.02, YM+.03), -.3); arrow(c, B, (X0+.02, Y1), (X1-.02, YM+.03), .3)
def f3(c, B):
    poly(c, B, [(X0, Y0), (X1, Y0), (X1, Y1), (X0, Y1)])
    crease(c, B, (X0, Y1), (X1, YM)); crease(c, B, (X1, Y1), (X0, YM))
    mountain(c, B, (X0-.05, YC), (X1+.05, YC)); turn_over(c, B)
def f4(c, B):
    poly(c, B, [(X0, Y0), (X1, Y0), (X1, YM), (X0, YM)])
    poly(c, B, [(X0, YM), (X1, YM), (.5, YC)])
    arrow(c, B, (X0-.12, YC+.08), (X0+.06, YM+.06), .25); arrow(c, B, (X1+.12, YC+.08), (X1-.06, YM+.06), -.25)
def f5(c, B):
    poly(c, B, [(X0, Y0), (X1, Y0), (X1, YM), (X0, YM)])
    poly(c, B, [(X0, YM), (X1, YM), (.5, YC)])
    valley(c, B, (.4, YM), (.5, YC)); valley(c, B, (.6, YM), (.5, YC))
    arrow(c, B, (X0+.01, YM+.01), (.47, YC-.02), -.35); arrow(c, B, (X1-.01, YM+.01), (.53, YC-.02), .35)
def _house_legs(c, B):
    poly(c, B, [(X0, Y0), (X1, Y0), (X1, YM), (X0, YM)])
    poly(c, B, [(X0, YM), (X1, YM), (.5, YC)])
    poly(c, B, [(.4, YM), (.5, YC), (.43, YC+.12)], WHITE); poly(c, B, [(.6, YM), (.5, YC), (.57, YC+.12)], WHITE)
def f6(c, B):
    _house_legs(c, B)
    valley(c, B, (.4, Y0), (.4, YM)); valley(c, B, (.6, Y0), (.6, YM))
    arrow(c, B, (X0+.01, .2), (.48, .2), .3); arrow(c, B, (X1-.01, .2), (.52, .2), -.3)
def f7(c, B):
    poly(c, B, [(.4, Y0), (.6, Y0), (.6, YM), (.4, YM)])
    poly(c, B, [(X0, YM), (X1, YM), (.5, YC)])
    poly(c, B, [(.4, YM), (.5, YC), (.43, YC+.12)], WHITE); poly(c, B, [(.6, YM), (.5, YC), (.57, YC+.12)], WHITE)
    yf = (Y0 + YM) / 2
    valley(c, B, (.35, yf), (.65, yf)); arrow(c, B, (.5, Y0+.01), (.5, YM-.02), .45)
def f8(c, B):
    yf = (Y0 + YM) / 2
    poly(c, B, [(.4, yf), (.6, yf), (.6, YM), (.4, YM)])
    poly(c, B, [(X0, YM), (X1, YM), (.5, YC)])
    poly(c, B, [(.4, YM), (.5, YC), (.43, YC+.12)], WHITE); poly(c, B, [(.6, YM), (.5, YC), (.57, YC+.12)], WHITE)
    poly(c, B, [(.42, yf+.02), (.24, yf-.16), (.46, yf+.06)], WHITE, 1.4); poly(c, B, [(.58, yf+.02), (.76, yf-.16), (.54, yf+.06)], WHITE, 1.4)
    yz = yf + (YM - yf) / 2
    mountain(c, B, (.33, yz), (.67, yz)); arrow(c, B, (.72, yf+.02), (.72, yz+.02), -.6)
def f9(c, B):
    poly(c, B, [(.25, .25), (.75, .25), (.62, .55), (.5, .68), (.38, .55)])
    poly(c, B, [(.38, .55), (.24, .78), (.46, .62)], WHITE); poly(c, B, [(.62, .55), (.76, .78), (.54, .62)], WHITE)
    poly(c, B, [(.25, .25), (.12, .10), (.36, .2)], WHITE); poly(c, B, [(.75, .25), (.88, .10), (.64, .2)], WHITE)
    c.setFillColor(colors.black); c.circle(*B(.45, .6), 2.2, fill=1); c.circle(*B(.55, .6), 2.2, fill=1)
    arrow(c, B, (.5, .95), (.5, .42), 0)

FROG = [
    ("Prends un carré et plie-le en deux pour obtenir un rectangle (ou une fiche bristol).", f1),
    ("Dans le carré du haut, plie le bord du haut sur chaque côté : un X. Déplie.", f2),
    ("Retourne. Plie à l'horizontale au centre du X, puis déplie. Retourne à nouveau.", f3),
    ("Rentre les côtés le long des plis : le haut s'aplatit en triangle.", f4),
    ("Plie les 2 coins du bas du triangle vers la pointe : les pattes avant.", f5),
    ("Plie les 2 côtés du rectangle vers le milieu (sous le triangle).", f6),
    ("Plie le bas vers le haut jusqu'à la base du triangle.", f7),
    ("Tire les coins vers l'extérieur (pattes arrière), puis replie le bas en deux vers le bas : le ressort.", f8),
    ("Retourne : appuie sur le derrière et lâche… elle saute !", f9),
]


# ─── BATEAU EN PAPIER (A4 portrait) ──────────────────────────────────────────
def b1(c, B):
    poly(c, B, [(.29, .05), (.71, .05), (.71, .95), (.29, .95)], WHITE)
    valley(c, B, (.25, .5), (.75, .5)); arrow(c, B, (.62, .9), (.62, .1), -.15)
def _rect(c, B):   # A4 plié en deux : 1 × .707
    poly(c, B, [(.12, .25), (.88, .25), (.88, .79), (.12, .79)], WHITE)
def b2(c, B):
    _rect(c, B); valley(c, B, (.5, .2), (.5, .84)); arrow(c, B, (.84, .52), (.16, .52), .3)
    c.setFont("Helvetica", 7); c.setFillColor(HexColor("#555555")); c.drawCentredString(*B(.5, .12), "pli en haut")
def b3(c, B):
    _rect(c, B); crease(c, B, (.5, .25), (.5, .79))
    valley(c, B, (.5, .79), (.12, .41)); valley(c, B, (.5, .79), (.88, .41))
    arrow(c, B, (.15, .76), (.46, .5), -.3); arrow(c, B, (.85, .76), (.54, .5), .3)
def _house(c, B):
    poly(c, B, [(.12, .25), (.88, .25), (.88, .41), (.5, .79), (.12, .41)], WHITE)
    c.setLineWidth(0.6); c.line(*B(.12, .41), *B(.88, .41))
def b4(c, B):
    _house(c, B); valley(c, B, (.1, .41), (.9, .41)); arrow(c, B, (.5, .27), (.5, .5), .5); turn_over(c, B, .88, .9)
def b5(c, B):
    poly(c, B, [(.12, .25), (.88, .25), (.88, .41), (.5, .79), (.12, .41)], WHITE)
    poly(c, B, [(.12, .25), (.88, .25), (.88, .41), (.12, .41)], GREY)
    valley(c, B, (.22, .25), (.22, .41)); valley(c, B, (.78, .25), (.78, .41))
    arrow(c, B, (.14, .33), (.3, .33), .5); arrow(c, B, (.86, .33), (.7, .33), -.5)
def b6(c, B):
    poly(c, B, [(.5, .92), (.18, .5), (.5, .08), (.82, .5)], WHITE)
    c.setLineWidth(0.6); c.line(*B(.5, .08), *B(.5, .92))
    arrow(c, B, (.1, .25), (.3, .45), .3); arrow(c, B, (.9, .25), (.7, .45), -.3)
def b7(c, B):
    poly(c, B, [(.5, .92), (.18, .5), (.5, .08), (.82, .5)], WHITE)
    valley(c, B, (.18, .5), (.82, .5)); arrow(c, B, (.5, .1), (.5, .86), .45); turn_over(c, B, .88, .9)
def b8(c, B):
    poly(c, B, [(.12, .3), (.88, .3), (.5, .78)], WHITE)
    arrow(c, B, (.12, .2), (.4, .2), .3); arrow(c, B, (.88, .2), (.6, .2), -.3)
    c.setFont("Helvetica", 7); c.setFillColor(HexColor("#555555")); c.drawCentredString(*B(.5, .08), "ouvre par le bas, aplatis en losange")
def b9(c, B):
    poly(c, B, [(.5, .88), (.3, .45), (.7, .45)], WHITE)
    poly(c, B, [(.05, .48), (.95, .48), (.78, .25), (.22, .25)], GREY)
    c.line(*B(.5, .88), *B(.5, .48))
    arrow(c, B, (.18, .62), (.04, .62), .2); arrow(c, B, (.82, .62), (.96, .62), -.2)

BOAT = [
    ("Feuille A4 en hauteur : plie-la en deux, le haut sur le bas.", b1),
    ("Plie en deux de gauche à droite pour marquer le milieu, puis déplie.", b2),
    ("Plie les 2 coins du haut vers le milieu : une maison.", b3),
    ("Remonte la bande du bas sur le triangle. Retourne et fais pareil de l'autre côté : un chapeau !", b4),
    ("Rabats les petits coins qui dépassent derrière, des deux côtés.", b5),
    ("Ouvre le chapeau par le bas et aplatis-le : il devient un losange.", b6),
    ("Plie la pointe du bas vers le haut. Retourne et fais pareil : un triangle.", b7),
    ("Ouvre encore par le bas et aplatis en losange.", b8),
    ("Tire doucement les 2 pointes du haut vers l'extérieur… ton bateau est prêt !", b9),
]


# ─── GRUE TRADITIONNELLE (carré) ─────────────────────────────────────────────
# Base carrée (losange) : T(.5,.95) L(.2,.55) R(.8,.55) Bm(.5,.15)
T, L_, R_, Bm = (.5, .95), (.2, .55), (.8, .55), (.5, .15)
KL, KR = (.315, .704), (.685, .704)  # bissectrice en Bm coupant les bords hauts (calcul exact)
def c1(c, B):
    poly(c, B, [(.12, .12), (.88, .12), (.88, .88), (.12, .88)])
    valley(c, B, (.12, .12), (.88, .88)); valley(c, B, (.12, .88), (.88, .12))
    arrow(c, B, (.86, .86), (.15, .15), .25)
def c2(c, B):
    poly(c, B, [(.12, .12), (.88, .12), (.88, .88), (.12, .88)], WHITE)
    crease(c, B, (.12, .12), (.88, .88)); crease(c, B, (.12, .88), (.88, .12))
    valley(c, B, (.5, .12), (.5, .88)); valley(c, B, (.12, .5), (.88, .5))
    arrow(c, B, (.5, .86), (.5, .14), -.35); turn_over(c, B, .9, .04)
def c3(c, B):
    poly(c, B, [T, L_, Bm, R_])
    c.setLineWidth(0.6); c.line(*B(*T), *B(*Bm))
    c.setFont("Helvetica", 7); c.setFillColor(HexColor("#555555")); c.drawCentredString(*B(.5, .05), "côté ouvert en bas")
def c4(c, B):
    poly(c, B, [T, L_, Bm, R_])
    valley(c, B, Bm, KL); valley(c, B, Bm, KR)
    arrow(c, B, (.24, .5), (.46, .45), -.3); arrow(c, B, (.76, .5), (.54, .45), .3)
def c5(c, B):
    poly(c, B, [T, KL, Bm, KR])
    valley(c, B, KL, KR); arrow(c, B, (.5, .93), (.5, .6), .5)
    c.setFont("Helvetica-Bold", 7); c.setFillColor(HexColor("#D62828")); c.drawCentredString(*B(.5, .03), "puis déplie les 3 plis")
def c6(c, B):
    poly(c, B, [T, L_, Bm, R_])
    crease(c, B, Bm, KL); crease(c, B, Bm, KR); crease(c, B, KL, KR)
    arrow(c, B, (.5, .18), (.5, 1.0), -.15)
    arrow(c, B, (.22, .56), (.42, .6), .2); arrow(c, B, (.78, .56), (.58, .6), -.2)
def _bird_base(c, B):
    poly(c, B, [(.5, .97), (.36, .55), (.5, .05), (.64, .55)])
    c.setLineWidth(0.6); c.line(*B(.5, .97), *B(.5, .05)); c.line(*B(.36, .55), *B(.64, .55))
def c7(c, B):
    _bird_base(c, B); turn_over(c, B, .85, .85)
    c.setFont("Helvetica-Bold", 8); c.setFillColor(HexColor("#D62828")); c.drawCentredString(*B(.2, .5), "x 2")
def c8(c, B):
    _bird_base(c, B)
    valley(c, B, (.5, .05), (.42, .55)); valley(c, B, (.5, .05), (.58, .55))
    arrow(c, B, (.38, .45), (.47, .3), -.3); arrow(c, B, (.62, .45), (.53, .3), .3)
    c.setFont("Helvetica-Bold", 7); c.setFillColor(HexColor("#D62828")); c.drawCentredString(*B(.2, .1), "des 2 côtés")
def c9(c, B):
    P = B
    poly(c, P, [(.30, .84), (.50, .42), (.40, .40)], GREY)
    poly(c, P, [(.72, .86), (.50, .42), (.62, .40)], GREY)
    poly(c, P, [(.36, .40), (.50, .48), (.64, .40), (.50, .24)], WHITE)
    poly(c, P, [(.38, .36), (.10, .60), (.14, .62), (.42, .40)], WHITE)
    poly(c, P, [(.10, .60), (.03, .54), (.14, .62)], GREY)
    poly(c, P, [(.62, .36), (.94, .62), (.58, .40)], WHITE)

CRANE = [
    ("Carré, face colorée dessus : plie les 2 diagonales, déplie.", c1),
    ("Retourne. Plie en deux dans les 2 sens, déplie.", c2),
    ("Rapproche les plis : le carré se replie en un petit losange (base carrée).", c3),
    ("Plie les bords du bas de la couche du dessus vers le milieu : un cerf-volant.", c4),
    ("Plie le triangle du haut vers le bas, marque bien. Déplie ces 3 plis.", c5),
    ("Soulève la pointe du bas vers le haut : les côtés rentrent le long des plis.", c6),
    ("Retourne et refais les étapes 4 à 6 : c'est la base de l'oiseau.", c7),
    ("Affine les 2 pointes du bas en pliant les bords vers le milieu, des 2 côtés.", c8),
    ("Plie les 2 pointes vers le haut entre les ailes (cou, queue), plie la tête, ouvre les ailes !", c9),
]


def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    c = canvas.Canvas(OUT, pagesize=A4)
    c.setTitle("PocketSage — Tutos origami (fiche 29)")
    page(c, "Niveau 1 — Grenouille sauteuse", "7-15 ans", "Papier : un carré de 15 cm (ou une fiche bristol 10 × 15 cm)", FROG)
    page(c, "Niveau 2 — Bateau en papier", "6-15 ans", "Papier : une feuille A4 (plus elle est grande, plus le bateau est grand)", BOAT)
    page(c, "Niveau 3 — Grue traditionnelle", "9-15 ans", "Papier : un carré de 15 cm, fin (papier origami idéal)", CRANE)
    c.save()
    print("✅", OUT)

if __name__ == "__main__":
    main()
