#!/usr/bin/env python3
"""
Génère le guide parents PocketSage Academy en PDF
Inclut la section Ateliers sans écran avec mention des fiches imprimables.
"""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY

W, H = A4
HOME = os.path.expanduser("~")
OUT = os.environ.get("GUIDE_OUT", os.path.join(HOME, "mnt", "pocketsage", "guide_parents.pdf"))

import re as _re
_EMOJI = _re.compile("[\U0001F000-\U0001FAFF\u2600-\u27BF\u2B00-\u2BFF\uFE0F\u200D]")
def _clean(t):
    """Helvetica n'affiche pas les émojis (carrés noirs) : on les retire."""
    return _re.sub(r"\s{2,}", " ", _EMOJI.sub("", str(t))).strip()

class CleanCanvas(canvas.Canvas):
    def drawString(self, x, y, text, *a, **k):        return super().drawString(x, y, _clean(text), *a, **k)
    def drawCentredString(self, x, y, text, *a, **k): return super().drawCentredString(x, y, _clean(text), *a, **k)
    def drawRightString(self, x, y, text, *a, **k):   return super().drawRightString(x, y, _clean(text), *a, **k)

# ── Couleurs ─────────────────────────────────────────────────────────────────
PRIMARY   = HexColor("#6C63FF")
SECONDARY = HexColor("#06D6A0")
ACCENT1   = HexColor("#FF6B6B")
ACCENT2   = HexColor("#FF9F1C")
PURPLE    = HexColor("#8B5CF6")
DARK      = HexColor("#1A1A2E")
GRAY      = HexColor("#64748B")
LIGHT_BG  = HexColor("#F8F7FF")
WHITE     = colors.white

def hex_color(h):
    return HexColor(h)

def wrap_text(text, max_chars=80):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        if len(cur) + len(w) + 1 <= max_chars:
            cur = (cur + " " + w).strip()
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    return lines or [""]

def draw_page_bg(c, pagenum):
    # Fond dégradé léger en haut
    c.setFillColor(LIGHT_BG)
    c.rect(0, H-6*cm, W, 6*cm, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.rect(0, 0, W, H-6*cm, fill=1, stroke=0)
    # Numéro de page
    c.setFillColor(GRAY)
    c.setFont("Helvetica", 9)
    c.drawCentredString(W/2, 0.6*cm, f"PocketSage Academy — Guide Parents — p.{pagenum}")
    c.line(1.5*cm, 0.9*cm, W-1.5*cm, 0.9*cm)

def draw_cover(c):
    # Fond coloré
    c.setFillColor(PRIMARY)
    c.rect(0, H*0.45, W, H*0.55, fill=1, stroke=0)
    c.setFillColor(SECONDARY)
    c.roundRect(0, H*0.44, W, 1.5*cm, 0, fill=1, stroke=0)

    # Titre
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 32)
    c.drawCentredString(W/2, H*0.72, "🧠 PocketSage Academy")
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(W/2, H*0.65, "Guide pour les parents")
    c.setFont("Helvetica", 13)
    c.drawCentredString(W/2, H*0.59, "Comment accompagner votre enfant")
    c.drawCentredString(W/2, H*0.55, "dans son apprentissage avec l'application")

    # Sous-section bas de couverture
    c.setFillColor(DARK)
    y = H*0.4
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(W/2, y, "pocketsage.org")

    # Sections de la table des matières
    c.setFillColor(DARK)
    sections = [
        ("1.", "Comment fonctionne PocketSage", "p.2"),
        ("2.", "Paramétrer le profil de votre enfant", "p.3"),
        ("3.", "Les langues maternelles et le multilingue", "p.4"),
        ("4.", "Ateliers sans écran", "p.5"),
        ("5.", "Flash Savant : le scroll qui rend plus malin", "p.6"),
        ("6.", "Questions fréquentes", "p.7"),
    ]
    y = H*0.33
    for num, title, page in sections:
        c.setFillColor(HexColor("#EDE9FF"))
        c.roundRect(2*cm, y-0.1*cm, W-4*cm, 0.65*cm, 8, fill=1, stroke=0)
        c.setFillColor(PRIMARY)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(2.4*cm, y+0.1*cm, num)
        c.setFillColor(DARK)
        c.setFont("Helvetica", 11)
        c.drawString(3.2*cm, y+0.1*cm, title)
        c.setFillColor(GRAY)
        c.setFont("Helvetica", 10)
        c.drawRightString(W-2.3*cm, y+0.1*cm, page)
        y -= 0.8*cm

    # Footer couverture
    c.setFillColor(GRAY)
    c.setFont("Helvetica", 8)
    c.drawCentredString(W/2, 0.6*cm, "© 2024 PocketSage Academy — Confidentiel — Pour usage familial uniquement")

def draw_section_header(c, y, title, color=PRIMARY, icon=""):
    c.setFillColor(color)
    c.roundRect(1.5*cm, y-0.15*cm, W-3*cm, 0.9*cm, 10, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(2*cm, y+0.1*cm, f"{icon}  {title}" if icon else title)
    return y - 1.1*cm

def draw_text_block(c, y, lines, font="Helvetica", size=11, color=DARK, indent=2*cm, lh=0.5*cm):
    c.setFillColor(color)
    c.setFont(font, size)
    for line in lines:
        if y < 2*cm:
            return y
        c.drawString(indent, y, line)
        y -= lh
    return y - 0.2*cm

def draw_bullet(c, y, text, col=PRIMARY, indent=2.2*cm, max_chars=72):
    lines = wrap_text(text, max_chars)
    c.setFillColor(col)
    c.circle(indent - 0.4*cm, y + 0.1*cm, 0.12*cm, fill=1, stroke=0)
    c.setFillColor(DARK)
    c.setFont("Helvetica", 11)
    for j, line in enumerate(lines):
        c.drawString(indent, y - j*0.45*cm, line)
    return y - len(lines)*0.45*cm - 0.25*cm

def draw_info_box(c, y, title, lines, col=PRIMARY, bg=None):
    if bg is None:
        bg = HexColor(col.hexval().replace("#","") + "22") if hasattr(col,'hexval') else LIGHT_BG
    total_h = (len(lines)+1) * 0.5*cm + 0.6*cm
    c.setFillColor(LIGHT_BG)
    c.roundRect(1.5*cm, y-total_h, W-3*cm, total_h, 12, fill=1, stroke=0)
    c.setStrokeColor(col)
    c.setLineWidth(2)
    c.roundRect(1.5*cm, y-total_h, W-3*cm, total_h, 12, fill=0, stroke=1)
    c.setFillColor(col)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(2*cm, y-0.45*cm, title)
    c.setFillColor(DARK)
    c.setFont("Helvetica", 11)
    for i, line in enumerate(lines):
        c.drawString(2.3*cm, y-0.9*cm - i*0.45*cm, line)
    return y - total_h - 0.4*cm

# ════════════════════════════════════════════════════════════════════════════
c = CleanCanvas(OUT, pagesize=A4)

# ── PAGE 1 : COUVERTURE ───────────────────────────────────────────────────────
draw_cover(c)
c.showPage()

# ── PAGE 2 : COMMENT ÇA FONCTIONNE ───────────────────────────────────────────
draw_page_bg(c, 2)
y = H - 1.5*cm

c.setFillColor(PRIMARY)
c.setFont("Helvetica-Bold", 22)
c.drawString(1.5*cm, y, "1. Comment fonctionne PocketSage")
y -= 0.5*cm
c.setFillColor(GRAY)
c.line(1.5*cm, y, W-1.5*cm, y)
y -= 0.6*cm

y = draw_section_header(c, y, "Une application d'apprentissage par niveaux scolaires", PRIMARY, "📚")
bullets_p2a = [
    "PocketSage couvre les niveaux de la Grande Section (5-6 ans) au Brevet (14-15 ans)",
    "Chaque session dure 10 à 15 minutes — adaptée à l'attention de votre enfant",
    "Les questions s'ajustent automatiquement au niveau et aux progrès",
    "Un système de points et de médailles motive sans créer de dépendance",
    "Les réponses correctes sont toujours expliquées pour vraiment apprendre",
]
for b in bullets_p2a:
    y = draw_bullet(c, y, b)

y -= 0.3*cm
y = draw_section_header(c, y, "Les matières disponibles", SECONDARY, "🎯")
matières = [
    ("📖 Lecture / Français", "Phonétique, vocabulaire, conjugaison, grammaire"),
    ("🔢 Mathématiques", "Calcul, numération, géométrie, problèmes"),
    ("🌍 Géographie & Histoire", "France, Europe, monde, chronologie"),
    ("🔬 Sciences", "Corps humain, animaux, planètes, physique"),
    ("🌐 Langues vivantes", "Anglais, Allemand, Espagnol, Italien, Portugais"),
    ("🎨 Culture générale", "Art, musique, sports, inventions"),
]
for mat, desc in matières:
    c.setFillColor(HexColor("#EDE9FF"))
    c.roundRect(1.5*cm, y-0.65*cm, W-3*cm, 0.65*cm, 8, fill=1, stroke=0)
    c.setFillColor(DARK)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(2*cm, y-0.42*cm, mat)
    c.setFillColor(GRAY)
    c.setFont("Helvetica", 10)
    c.drawRightString(W-1.8*cm, y-0.42*cm, desc)
    y -= 0.75*cm

y -= 0.2*cm
y = draw_info_box(c, y, "💡 Notre philosophie",
    ["PocketSage n'est pas là pour remplacer l'école — mais pour rendre l'apprentissage",
     "ludique, régulier et ancré dans la vie de famille. 10 minutes par jour",
     "valent mieux qu'1 heure le week-end !"],
    ACCENT2)

c.showPage()

# ── PAGE 3 : PROFIL ───────────────────────────────────────────────────────────
draw_page_bg(c, 3)
y = H - 1.5*cm

c.setFillColor(PRIMARY)
c.setFont("Helvetica-Bold", 22)
c.drawString(1.5*cm, y, "2. Paramétrer le profil de votre enfant")
y -= 0.5*cm
c.setFillColor(GRAY)
c.line(1.5*cm, y, W-1.5*cm, y)
y -= 0.6*cm

y = draw_section_header(c, y, "Les 4 informations essentielles du profil", PRIMARY, "👤")
infos = [
    ("Prénom", "Pour personnaliser les messages d'encouragement"),
    ("Âge / Classe", "Pour adapter le niveau des questions automatiquement"),
    ("Langue maternelle", "Pour les consignes et l'interface (14 langues disponibles)"),
    ("Langues à apprendre", "Les langues étrangères que l'enfant étudie"),
]
for label, desc in infos:
    c.setFillColor(PRIMARY)
    c.roundRect(1.5*cm, y-0.65*cm, 3.5*cm, 0.65*cm, 6, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(1.5*cm + 1.75*cm, y-0.38*cm, label)
    c.setFillColor(DARK)
    c.setFont("Helvetica", 11)
    c.drawString(5.5*cm, y-0.38*cm, desc)
    y -= 0.8*cm

y -= 0.2*cm
y = draw_section_header(c, y, "Jusqu'à 5 profils par famille", SECONDARY, "👨‍👩‍👧‍👦")
bullets_profils = [
    "Chaque enfant a son propre profil — progression et historique séparés",
    "Les parents peuvent créer et gérer les profils depuis l'accueil",
    "Pas de compte email requis — tout est stocké sur l'appareil",
    "Les profils se sélectionnent en 1 touche au lancement de l'app",
]
for b in bullets_profils:
    y = draw_bullet(c, y, b, SECONDARY)

y -= 0.3*cm
y = draw_section_header(c, y, "Le système de progression", ACCENT1, "📈")
bullets_prog = [
    "⭐ Score : points gagnés à chaque bonne réponse",
    "🏆 Médailles : Bronze (100 pts), Argent (500 pts), Or (2000 pts), Platine (10 000 pts)",
    "📊 Statistiques : matières préférées, taux de réussite, temps de session",
    "🔥 Série : nombre de jours consécutifs de pratique — encourage la régularité",
    "✅ Séances terminées : accessible dans le profil pour suivre la progression",
]
for b in bullets_prog:
    y = draw_bullet(c, y, b, ACCENT1)

c.showPage()

# ── PAGE 4 : LANGUES MATERNELLES ─────────────────────────────────────────────
draw_page_bg(c, 4)
y = H - 1.5*cm

c.setFillColor(PRIMARY)
c.setFont("Helvetica-Bold", 22)
c.drawString(1.5*cm, y, "3. Les langues maternelles et le multilingue")
y -= 0.5*cm
c.setFillColor(GRAY)
c.line(1.5*cm, y, W-1.5*cm, y)
y -= 0.6*cm

y = draw_section_header(c, y, "Pourquoi la langue maternelle ?", PRIMARY, "🌍")
bullets_lm = [
    "Un enfant apprend mieux quand les consignes sont dans sa langue du cœur",
    "Les 14 langues maternelles couvrent les principales communautés de France :",
    "FR · EN · DE · ES · IT · PT · RU · UK · AR · ZH · PL · RO · HU · TR",
    "Pour les autres langues, l'interface est en français (fallback)",
    "La langue peut être changée à tout moment dans les réglages du profil",
]
for b in bullets_lm:
    y = draw_bullet(c, y, b)

y -= 0.3*cm
y = draw_section_header(c, y, "Langues vivantes disponibles", SECONDARY, "🗣️")
langs_vivantes = [
    "🇬🇧 Anglais (EN)", "🇩🇪 Allemand (DE)", "🇮🇹 Italien (IT)",
    "🇵🇹 Portugais (PT)", "🇷🇺 Russe (RU)", "🇺🇦 Ukrainien (UK)",
    "🇸🇦 Arabe (AR)", "🇨🇳 Chinois (ZH)",
]
# Grille 2 colonnes
for i in range(0, len(langs_vivantes), 2):
    c.setFillColor(HexColor("#E8FFF8"))
    c.roundRect(1.5*cm, y-0.55*cm, (W-3.3*cm)/2, 0.55*cm, 6, fill=1, stroke=0)
    c.setFillColor(DARK)
    c.setFont("Helvetica", 11)
    c.drawString(1.9*cm, y-0.35*cm, langs_vivantes[i])
    if i+1 < len(langs_vivantes):
        c.setFillColor(HexColor("#E8FFF8"))
        c.roundRect(1.5*cm + (W-3.3*cm)/2 + 0.3*cm, y-0.55*cm, (W-3.3*cm)/2, 0.55*cm, 6, fill=1, stroke=0)
        c.setFillColor(DARK)
        c.drawString(1.9*cm + (W-3.3*cm)/2 + 0.3*cm, y-0.35*cm, langs_vivantes[i+1])
    y -= 0.65*cm

y -= 0.3*cm
y = draw_section_header(c, y, "Les boutons audio", ACCENT2, "🔊")
bullets_audio = [
    "Pour les CP à CE2 : chaque question est lue à voix haute dans la langue maternelle",
    "Pour les langues vivantes : les mots étrangers sont toujours prononcés",
    "Les voix utilisées sont des voix synthétiques naturelles (Google TTS Neural)",
    "Le bouton 🔊 est disponible sur chaque question — l'enfant peut réécouter autant",
    "que nécessaire avant de répondre",
]
for b in bullets_audio:
    y = draw_bullet(c, y, b, ACCENT2)

y -= 0.2*cm
y = draw_info_box(c, y, "🌟 Pour les familles bilingues",
    ["PocketSage est idéal pour les enfants qui apprennent le français à l'école mais",
     "parlent une autre langue à la maison. Les consignes dans leur langue maternelle",
     "réduisent l'anxiété et augmentent la confiance. Résultats constatés : +30% de",
     "sessions complétées chez les enfants allophones !"],
    SECONDARY)

c.showPage()

# ── PAGE 5 : ATELIERS SANS ÉCRAN ─────────────────────────────────────────────
draw_page_bg(c, 5)
y = H - 1.5*cm

c.setFillColor(PRIMARY)
c.setFont("Helvetica-Bold", 22)
c.drawString(1.5*cm, y, "4. Ateliers sans écran")
y -= 0.5*cm
c.setFillColor(GRAY)
c.line(1.5*cm, y, W-1.5*cm, y)
y -= 0.6*cm

y = draw_section_header(c, y, "Équilibrer apprentissage digital et activités manuelles", PRIMARY, "🎨")
intro_lines = wrap_text(
    "PocketSage n'est pas seulement une application — c'est un système d'apprentissage "
    "complet. La section Ateliers propose des activités créatives, scientifiques et "
    "artistiques sans écran, pour stimuler le cerveau autrement.", 78)
for line in intro_lines:
    c.setFillColor(DARK)
    c.setFont("Helvetica", 11)
    c.drawString(1.5*cm, y, line)
    y -= 0.45*cm
y -= 0.8*cm

y = draw_section_header(c, y, "Les 5 catégories d'ateliers", SECONDARY, "🗂️")
cats = [
    ("🦋 Origami", "Pliage de papier — motricité fine, géométrie, patience"),
    ("🔬 Sciences", "Volcans, cristaux, expériences avec des ingrédients simples"),
    ("🔨 Bricolage", "Constructions créatives avec matériaux recyclés"),
    ("🎨 Peinture", "Techniques artistiques guidées étape par étape"),
    ("📄 Fiches imprimables", "Exercices cérébraux, dessin à 2 mains, jeux sans écran"),
]
for cat, desc in cats:
    c.setFillColor(HexColor("#EDE9FF"))
    c.roundRect(1.5*cm, y-0.65*cm, W-3*cm, 0.65*cm, 8, fill=1, stroke=0)
    c.setFillColor(DARK)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(2*cm, y-0.42*cm, cat)
    c.setFillColor(GRAY)
    c.setFont("Helvetica", 10)
    c.drawRightString(W-1.8*cm, y-0.42*cm, desc)
    y -= 0.75*cm

y -= 0.8*cm

# ── SECTION FICHES IMPRIMABLES (mention principale) ──────────────────────────
c.setFillColor(PURPLE)
c.roundRect(1.5*cm, y-0.15*cm, W-3*cm, 0.9*cm, 10, fill=1, stroke=0)
c.setFillColor(WHITE)
c.setFont("Helvetica-Bold", 14)
c.drawString(2*cm, y+0.1*cm, "📄  Les fiches imprimables — Nouveauté !")
y -= 1.1*cm

fiches_lines = wrap_text(
    "PocketSage propose désormais 30 fiches d'activités à imprimer et à faire en famille, "
    "SANS aucun écran. Ces fiches sont disponibles directement dans l'application, "
    "dans la section Ateliers → Fiches.", 78)
for line in fiches_lines:
    c.setFillColor(DARK)
    c.setFont("Helvetica", 11)
    c.drawString(1.5*cm, y, line)
    y -= 0.45*cm
y -= 0.8*cm

y = draw_section_header(c, y, "Ce que contiennent les fiches", PURPLE, "📋")
fiches_cats = [
    ("✏️ Dessin à 2 mains", "5 fiches", "Coordination cerveau-mains, motricité bilatérale"),
    ("🧠 Exercices cérébraux", "8 fiches", "Mémoire, logique, calcul mental, illusions"),
    ("⚡ Réflexes et réactivité", "6 fiches", "Jonglage, test de réaction, jeux de doigts"),
    ("🌀 Mandalas et Op Art",   "5 fiches", "Coloriage thérapeutique, art optique, Zentangle"),
    ("🎮 Jeux sans écran",      "5 fiches", "Escape game, codes secrets, théâtre d'ombres"),
    ("🧘 Yoga et bien-être",    "1 fiche",  "Routine de 5 min, respiration, visualisation"),
]
for cat, nb, desc in fiches_cats:
    c.setFillColor(HexColor("#F3EEFF"))
    c.roundRect(1.5*cm, y-0.6*cm, W-3*cm, 0.6*cm, 6, fill=1, stroke=0)
    c.setFillColor(PURPLE)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(2*cm, y-0.37*cm, cat)
    c.setFillColor(HexColor("#8B5CF6"))
    c.drawString(7.5*cm, y-0.37*cm, nb)
    c.setFillColor(GRAY)
    c.setFont("Helvetica", 10)
    c.drawString(9*cm, y-0.37*cm, desc)
    y -= 0.68*cm

y -= 0.2*cm

y = draw_info_box(c, y, "🌍 Fiches dans la langue maternelle de l'enfant",
    ["Chaque fiche est générée automatiquement dans la langue maternelle du profil.",
     "Un enfant russophone recevra la fiche en russe, un enfant arabophone en arabe,",
     "etc. — pour 14 langues maternelles. L'apprentissage dans sa propre langue",
     "renforce la compréhension et l'engagement."],
    PURPLE)

y -= 0.1*cm
c.setFillColor(DARK)
c.setFont("Helvetica-Bold", 11)
c.drawString(1.5*cm, y, "Comment accéder aux fiches :")
y -= 0.5*cm
steps_fiches = [
    "1. Ouvrez l'application PocketSage",
    "2. Allez dans la section Ateliers",
    "3. Sélectionnez la catégorie Fiches",
    "4. Choisissez une fiche et touchez 📥 Télécharger la fiche PDF",
    "5. Imprimez et profitez !",
]
for s in steps_fiches:
    c.setFillColor(DARK)
    c.setFont("Helvetica", 11)
    c.drawString(2*cm, y, s)
    y -= 0.45*cm

c.showPage()

# ── PAGE 6 : FLASH SAVANT ────────────────────────────────────────────────────
draw_page_bg(c, 6)
y = H - 1.5*cm
c.setFillColor(PRIMARY)
c.setFont("Helvetica-Bold", 22)
c.drawString(1.5*cm, y, "5. Flash Savant : le scroll qui rend plus malin")
y -= 0.5*cm
c.setFillColor(GRAY)
c.line(1.5*cm, y, W-1.5*cm, y)
y -= 0.6*cm

y = draw_section_header(c, y, "Remplacer le scroll par la curiosité", ACCENT2)
for b in [
    "Des cartes d'une minute : une découverte, une idée, un geste à essayer dans la journée",
    "Contenu adapté à l'âge de chaque profil, de 4 ans à l'adulte",
    "7 thèmes : Curiosités, Psycho, Motivation, Confiance, Émotions, Sagesse, Mix",
    "Lu à voix haute dans la langue de l'enfant, chaque fait est accompagné de sa source",
]:
    y = draw_bullet(c, y, b, ACCENT2)

y -= 0.7*cm
y = draw_section_header(c, y, "La révision qui ancre les connaissances", PRIMARY)
y = draw_text_block(c, y, [
    "Chaque carte vue revient plus tard sous forme de petite question à 3 choix.",
    "Se tester fait mieux retenir que relire, et espacer les rappels ancre durablement.",
], size=10.5, lh=0.45*cm)
# Schéma des boîtes
labels = [("Carte vue", "boîte 1"), ("Rappel", "après 2 jours"), ("Rappel", "après 7 jours"), ("Rappel", "après 21 jours"), ("Ancrée", "compteur vert")]
bw, gap = 2.9*cm, 0.55*cm
x0 = (W - (5*bw + 4*gap)) / 2
yb = y - 1.5*cm
for i, (a, b) in enumerate(labels):
    x = x0 + i*(bw+gap)
    col = SECONDARY if i == 4 else (ACCENT2 if i == 0 else PRIMARY)
    c.setFillColor(col)
    c.roundRect(x, yb, bw, 1.3*cm, 8, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 10)
    c.drawCentredString(x + bw/2, yb + 0.75*cm, a)
    c.setFont("Helvetica", 8.5)
    c.drawCentredString(x + bw/2, yb + 0.35*cm, b)
    if i < 4:
        c.setStrokeColor(GRAY); c.setFillColor(GRAY); c.setLineWidth(1.5)
        ax = x + bw + 0.08*cm
        c.line(ax, yb + 0.65*cm, ax + gap - 0.16*cm, yb + 0.65*cm)
        p = c.beginPath(); p.moveTo(ax + gap - 0.16*cm, yb + 0.65*cm)
        p.lineTo(ax + gap - 0.36*cm, yb + 0.8*cm); p.lineTo(ax + gap - 0.36*cm, yb + 0.5*cm); p.close()
        c.drawPath(p, fill=1, stroke=0)
c.setFillColor(GRAY)
c.setFont("Helvetica-Oblique", 9)
c.drawCentredString(W/2, yb - 0.45*cm, "Bonne réponse : la carte passe à l'étape suivante.  Erreur : elle revient le lendemain, sans pénalité.")
y = yb - 1.7*cm

y = draw_section_header(c, y, "Comment l'utiliser en famille", SECONDARY)
for b in [
    "Proposez Flash à la place des réseaux : trajet, salle d'attente, avant les devoirs",
    "5 à 10 cartes suffisent, puis on fait autre chose",
    "Le bouton orange « à réviser » : 1 à 2 minutes par jour pour garder les acquis",
    "Faites ensemble le geste « Essaie aujourd'hui » de la carte",
    "Au dîner : « Quelle carte t'a le plus surpris aujourd'hui ? »",
]:
    y = draw_bullet(c, y, b, SECONDARY)

y -= 0.4*cm
y = draw_info_box(c, y, "Un écran pensé pour qu'on le pose",
    ["Pas de pub, pas de réseau social, pas d'algorithme qui pousse à rester.",
     "Le compteur montre ce que votre enfant a retenu, pas le temps passé."],
    PRIMARY)
c.showPage()
# ── PAGE 7 : FAQ ──────────────────────────────────────────────────────────────
draw_page_bg(c, 7)
y = H - 1.5*cm

c.setFillColor(PRIMARY)
c.setFont("Helvetica-Bold", 22)
c.drawString(1.5*cm, y, "6. Questions fréquentes")
y -= 0.5*cm
c.setFillColor(GRAY)
c.line(1.5*cm, y, W-1.5*cm, y)
y -= 0.6*cm

faqs = [
    ("Combien de temps par jour est recommandé ?",
     "10 à 15 minutes quotidiennes, idéalement au même moment de la journée. "
     "La régularité est plus importante que la durée. Évitez juste avant le coucher."),
    ("L'application fonctionne-t-elle sans internet ?",
     "Oui, les questions et la progression sont disponibles hors ligne. "
     "La connexion est nécessaire uniquement pour les nouveaux contenus audio et les fiches PDF."),
    ("Mon enfant peut-il tricher en cherchant les réponses ?",
     "Le mode sécurisé masque le texte de la question après l'écoute audio. "
     "Mais l'objectif est l'apprentissage, pas le score — une 'bonne réponse' par hasard "
     "n'aide pas à progresser."),
    ("Peut-on utiliser l'application sur plusieurs appareils ?",
     "Les profils sont stockés sur l'appareil. Vous pouvez utiliser l'application sur "
     "plusieurs appareils indépendamment — une synchronisation cloud est prévue."),
    ("Les fiches sont-elles adaptées aux enfants avec des difficultés d'apprentissage ?",
     "Oui ! Les fiches sont conçues pour être accessibles. Chaque fiche indique sa "
     "difficulté (⭐ à ⭐⭐⭐) et son public (5-16 ans). Commencez par les fiches ⭐."),
    ("Comment savoir si mon enfant progresse ?",
     "Dans le profil, les statistiques montrent le score total, les séances complétées, "
     "les matières favorites et le temps moyen par session."),
]

for question, reponse in faqs:
    # Question
    q_lines = wrap_text(question, 72)
    c.setFillColor(HexColor("#EDE9FF"))
    c.roundRect(1.5*cm, y-len(q_lines)*0.4*cm-0.3*cm, W-3*cm, len(q_lines)*0.4*cm+0.4*cm, 8, fill=1, stroke=0)
    c.setFillColor(PRIMARY)
    c.setFont("Helvetica-Bold", 11)
    for j, l in enumerate(q_lines):
        c.drawString(2*cm, y-0.1*cm - j*0.4*cm, l)
    y -= len(q_lines)*0.4*cm + 0.5*cm
    # Réponse
    r_lines = wrap_text(reponse, 76)
    c.setFillColor(DARK)
    c.setFont("Helvetica", 10)
    for l in r_lines:
        c.drawString(2*cm, y, l)
        y -= 0.4*cm
    y -= 0.3*cm

# Contact
y -= 0.2*cm
c.setFillColor(PRIMARY)
c.roundRect(1.5*cm, y-1.8*cm, W-3*cm, 1.8*cm, 12, fill=1, stroke=0)
c.setFillColor(WHITE)
c.setFont("Helvetica-Bold", 13)
c.drawCentredString(W/2, y-0.5*cm, "📬 Une question ? Un problème ?")
c.setFont("Helvetica", 11)
c.drawCentredString(W/2, y-0.95*cm, "contact@pocketsage.org")
c.drawCentredString(W/2, y-1.4*cm, "pocketsage.org — Application disponible sur iOS et Android")

c.showPage()
c.save()
print(f"✅ Guide parents généré : {OUT}")
