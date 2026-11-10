#!/usr/bin/env python3
"""
Génère les 30 fiches PDF dans les 14 langues PocketSage.
Utilise Google Translate API pour les traductions.
Sortie : <repo>/fiches/{LANG}/FI-XXX.pdf  (ou $FICHES_OUT) — à envoyer sur R2 : rclone copy fiches/FR r2:pocketsage-audio/fiches/FR
"""
import os, json, requests, time
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas

# ── Config ──────────────────────────────────────────────────────────────────
# Clés : variables d'environnement ou fichier .env à la racine du repo (jamais dans le code — repo public)
import os as _os, pathlib as _pl
for _p in (_pl.Path(__file__).resolve().parent / ".env", _pl.Path(__file__).resolve().parent.parent / ".env"):
    if _p.exists():
        for _l in _p.read_text(encoding="utf-8").splitlines():
            if "=" in _l and not _l.strip().startswith("#"):
                _k, _v = _l.split("=", 1)
                _os.environ.setdefault(_k.strip(), _v.strip().strip('"').strip("'"))

API_KEY = _os.environ.get("GOOGLE_TTS_API_KEY", "")
TRANSLATE_URL = f"https://translation.googleapis.com/language/translate/v2?key={API_KEY}"

HOME = os.path.expanduser("~")
OUT_BASE = os.environ.get("FICHES_OUT", os.path.join(os.path.dirname(os.path.abspath(__file__)), "fiches"))

W, H = A4

# Langues cibles + codes Google Translate
LANGS = {
    "FR": "fr", "EN": "en", "DE": "de", "ES": "es", "IT": "it", "PT": "pt",
    "RU": "ru", "UK": "uk", "AR": "ar", "ZH": "zh", "PL": "pl",
    "RO": "ro", "HU": "hu", "TR": "tr",
}

PAL = {
    "cerveau": ("#6C63FF", "#EDE9FF"),
    "dessin":  ("#FF6B6B", "#FFF0F0"),
    "reflexe": ("#06D6A0", "#E8FFF8"),
    "jeu":     ("#FF9F1C", "#FFF5E6"),
    "mandala": ("#E040FB", "#FBE9FF"),
    "yoga":    ("#00BCD4", "#E0F7FA"),
}

# Traduction label "FICHE" et "Âge"
UI_KEYS = {
    "FR": {"fiche":"FICHE", "age_label":"Âge"},
    "EN": {"fiche":"SHEET", "age_label":"Age"},
    "DE": {"fiche":"BLATT", "age_label":"Alter"},
    "ES": {"fiche":"FICHA", "age_label":"Edad"},
    "IT": {"fiche":"SCHEDA","age_label":"Età"},
    "PT": {"fiche":"FICHA", "age_label":"Idade"},
    "RU": {"fiche":"ЛИСТ",  "age_label":"Возраст"},
    "UK": {"fiche":"АРКУШ","age_label":"Вік"},
    "AR": {"fiche":"بطاقة", "age_label":"العمر"},
    "ZH": {"fiche":"工作表","age_label":"年龄"},
    "PL": {"fiche":"ARKUSZ","age_label":"Wiek"},
    "RO": {"fiche":"FIȘĂ", "age_label":"Vârstă"},
    "HU": {"fiche":"LAP",  "age_label":"Kor"},
    "TR": {"fiche":"SAYFA","age_label":"Yaş"},
}

FOOTER_TEXT = {
    "FR": "🧠 PocketSage Academy — pocketsage.org — Fiche imprimable gratuite",
    "EN": "🧠 PocketSage Academy — pocketsage.org — Free printable worksheet",
    "DE": "🧠 PocketSage Academy — pocketsage.org — Kostenlose Arbeitsblatt",
    "ES": "🧠 PocketSage Academy — pocketsage.org — Ficha imprimible gratuita",
    "IT": "🧠 PocketSage Academy — pocketsage.org — Scheda stampabile gratuita",
    "PT": "🧠 PocketSage Academy — pocketsage.org — Ficha imprimível gratuita",
    "RU": "🧠 PocketSage Academy — pocketsage.org — Бесплатный рабочий лист",
    "UK": "🧠 PocketSage Academy — pocketsage.org — Безкоштовний робочий аркуш",
    "AR": "🧠 PocketSage Academy — pocketsage.org — ورقة عمل مجانية للطباعة",
    "ZH": "🧠 PocketSage Academy — pocketsage.org — 免费可打印工作表",
    "PL": "🧠 PocketSage Academy — pocketsage.org — Darmowy arkusz do druku",
    "RO": "🧠 PocketSage Academy — pocketsage.org — Fișă de lucru gratuită",
    "HU": "🧠 PocketSage Academy — pocketsage.org — Ingyenes nyomtatható lap",
    "TR": "🧠 PocketSage Academy — pocketsage.org — Ücretsiz yazdırılabilir çalışma sayfası",
}

# ── Cache de traductions ─────────────────────────────────────────────────────
CACHE_PATH = "/tmp/fiches_translate_cache.json"
if os.path.exists(CACHE_PATH):
    with open(CACHE_PATH) as f:
        CACHE = json.load(f)
else:
    CACHE = {}

def save_cache():
    with open(CACHE_PATH, "w") as f:
        json.dump(CACHE, f, ensure_ascii=False, indent=2)

def translate_texts(texts, target_lang):
    """Traduit une liste de textes vers target_lang via Google Translate API."""
    if target_lang == "FR":
        return texts
    results = []
    batch = []
    batch_indices = []
    for i, text in enumerate(texts):
        key = f"{target_lang}::{text}"
        if key in CACHE:
            results.append((i, CACHE[key]))
        else:
            batch.append(text)
            batch_indices.append(i)
    # API call pour les non-cachés
    if batch:
        # Batch max 128 strings par appel
        for chunk_start in range(0, len(batch), 100):
            chunk = batch[chunk_start:chunk_start+100]
            chunk_idx = batch_indices[chunk_start:chunk_start+100]
            try:
                r = requests.post(TRANSLATE_URL, json={
                    "q": chunk, "source": "fr", "target": LANGS[target_lang], "format": "text"
                }, timeout=30)
                r.raise_for_status()
                translated = [t["translatedText"] for t in r.json()["data"]["translations"]]
                for idx, orig, trans in zip(chunk_idx, chunk, translated):
                    key = f"{target_lang}::{orig}"
                    CACHE[key] = trans
                    results.append((idx, trans))
                save_cache()
                time.sleep(0.3)  # rate limit gentil
            except Exception as e:
                print(f"  ⚠️ Translate error {target_lang}: {e}")
                for idx, orig in zip(chunk_idx, chunk):
                    results.append((idx, orig))  # fallback = texte original
    # Reconstituer dans l'ordre
    results.sort(key=lambda x: x[0])
    return [r[1] for r in results]

# ── Fonctions de dessin ──────────────────────────────────────────────────────
def hex_color(h):
    return HexColor(h)

def wrap_text(text, max_chars=70):
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

def draw_header(c, title, subtitle, cat, age_label, fiche_num, lang):
    # N&B : bordure noire fine, hauteur réduite à 3.0cm
    ui = UI_KEYS.get(lang, UI_KEYS["FR"])
    c.setStrokeColor(colors.black)
    c.setLineWidth(1.5)
    c.roundRect(1*cm, H-3.6*cm, W-2*cm, 3.0*cm, 10, fill=0, stroke=1)
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(1.5*cm, H-1.1*cm, f"{ui['fiche']} #{fiche_num:02d}")
    c.setFont("Helvetica", 9)
    c.drawRightString(W-1.5*cm, H-1.1*cm, f"{age_label} ans")
    title_short = title if len(title) <= 45 else title[:42] + "..."
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(W/2, H-2.1*cm, title_short)
    sub_short = subtitle if len(subtitle) <= 90 else subtitle[:87] + "..."
    c.setFont("Helvetica", 9)
    c.drawCentredString(W/2, H-3.0*cm, sub_short)

def draw_badge(c, x, y, text, main_col):
    # Remplace ⭐ par * pour compatibilité Helvetica
    text_clean = text.replace("⭐", "*").replace("✏️", "").replace("📋", "").replace("🧠", "").replace("💡", "")
    text_clean = text_clean.strip()
    text_short = text_clean[:30] if len(text_clean) > 30 else text_clean
    bw = len(text_short)*0.19*cm + 0.6*cm
    c.setFillColor(colors.white)
    c.setStrokeColor(colors.black)
    c.setLineWidth(0.8)
    c.roundRect(x, y-0.35*cm, bw, 0.6*cm, 6, fill=1, stroke=1)
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(x+0.3*cm, y-0.15*cm, text_short)

def clean_text(t):
    """Supprime les emojis non supportés par Helvetica."""
    replacements = {"⭐":"*","✏️":"","📋":"","🧠":"","💡":"","⏱":"",
                    "🍎":"","🌟":"","🎯":"","🏆":"","🌈":"","🦋":"","🎨":"",
                    "🔵":"","🔴":"","🟢":"","🟡":"","🎭":"","🎲":"","🃏":"",
                    "🌸":"","🎵":"","🧩":"","🔮":"","🌀":""}
    for k,v in replacements.items():
        t = t.replace(k, v)
    return t.strip()

def draw_section(c, y, title, main_col, bg_col):
    # N&B : fond gris très clair, texte noir gras
    title_s = clean_text(title)
    title_s = title_s[:50] if len(title_s)>50 else title_s
    c.setFillColor(HexColor("#F0F0F0"))
    c.setStrokeColor(colors.black)
    c.setLineWidth(0.5)
    c.roundRect(1*cm, y-0.1*cm, W-2*cm, 0.75*cm, 6, fill=1, stroke=1)
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(1.5*cm, y+0.1*cm, title_s)
    return y - 0.95*cm

def draw_steps(c, y, steps, main_col):
    for i, step in enumerate(steps, 1):
        if y < 2.5*cm:
            break
        # Cercle numéroté N&B
        c.setFillColor(colors.black)
        c.circle(1.7*cm, y+0.15*cm, 0.28*cm, fill=1, stroke=0)
        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 10)
        c.drawCentredString(1.7*cm, y+0.08*cm, str(i))
        c.setFillColor(colors.black)
        c.setFont("Helvetica", 10)
        lines = wrap_text(step, 72)
        for j, line in enumerate(lines):
            if y - j*0.42*cm < 2*cm:
                break
            c.drawString(2.3*cm, y - j*0.42*cm, line)
        y -= len(lines)*0.42*cm + 0.4*cm
    return y

def draw_note_box(c, y, text, main_col, bg_col, icon=""):
    if y < 2.0*cm:
        return y
    text_clean = clean_text(text)
    lines = wrap_text(text_clean, 75)
    box_h = max(1.0*cm, len(lines)*0.38*cm + 0.45*cm)
    if y - box_h < 1.8*cm:
        box_h = y - 1.8*cm
    if box_h < 0.5*cm:
        return y
    # Préfixe icône dessiné (petit carré coloré à gauche)
    c.setFillColor(colors.white)
    c.setStrokeColor(colors.black)
    c.setLineWidth(0.8)
    c.roundRect(1*cm, y-box_h, W-2*cm, box_h, 8, fill=1, stroke=1)
    # Carré coloré indicateur à gauche
    icon_colors = {"🧠": "#6C63FF", "💡": "#FF9F1C"}
    sq_col = icon_colors.get(icon, main_col)
    c.setFillColor(HexColor(sq_col))
    c.roundRect(1.2*cm, y-box_h+0.15*cm, 0.3*cm, box_h-0.3*cm, 3, fill=1, stroke=0)
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(1.8*cm, y-0.42*cm, lines[0])
    c.setFont("Helvetica", 10)
    for j, line in enumerate(lines[1:], 1):
        c.drawString(1.8*cm, y-0.42*cm - j*0.38*cm, line)
    return y - box_h - 0.3*cm

def draw_zone(c, y, label, h, main_col, bg_col):
    """Zone de dessin/activité : s'étend jusqu'en bas de page."""
    h = max(h, y - 1.8*cm)
    if h < 1*cm:
        return y
    # N&B : fond blanc, bordure pointillée noire
    c.setFillColor(colors.white)
    c.roundRect(1*cm, y-h, W-2*cm, h, 10, fill=1, stroke=0)
    c.setStrokeColor(colors.black)
    c.setLineWidth(0.8)
    c.setDash([4, 4])
    c.roundRect(1*cm, y-h, W-2*cm, h, 10, fill=0, stroke=1)
    c.setDash([])
    # Label : toutes les lignes, en haut à gauche, petit, gris
    c.setFillColor(HexColor("#888888"))
    c.setFont("Helvetica-Oblique", 8)
    all_lines = (label or "").split("\n")
    for li, line in enumerate(all_lines[:4]):  # max 4 lignes
        c.drawString(1.5*cm, y - 0.4*cm - li*0.35*cm, line[:90])
    return y - h - 0.3*cm

def draw_footer(c, lang):
    text = FOOTER_TEXT.get(lang, FOOTER_TEXT["FR"])
    # Fallback : sans emojis pour les langues non-latin (evite artefacts)
    if lang in ("AR","ZH"):
        text = "PocketSage Academy — pocketsage.org"
    c.setFillColor(hex_color("#AAAAAA"))
    c.setFont("Helvetica", 7)
    c.drawCentredString(W/2, 0.8*cm, text)
    c.line(1*cm, 1.1*cm, W-1*cm, 1.1*cm)

# ── Données source (FR) ──────────────────────────────────────────────────────
FICHES_FR = [
{"id":"FI-001","cat":"dessin","age_range":"7-14","titre":"Dessin à 2 mains — Papillon",
 "sous":"Dessine un papillon en miroir, les deux mains ensemble !",
 "steps":["Prends un crayon dans CHAQUE main.",
          "Place les deux mains au centre de la feuille.",
          "Dessine une aile gauche et une aile droite EN MÊME TEMPS.",
          "Commence par les grandes courbes, puis les détails.",
          "Colorie en miroir : même couleur à gauche et à droite !"],
 "note":"Ton cerveau travaille des deux côtés en même temps — c'est de la gym neuronale !",
 "zone":"Zone de dessin — Feuille A4 paysage recommandee",
 "astuce":"Ferme les yeux 10 secondes en imaginant le papillon avant de commencer.",
 "duree":"10 min","difficulte":"⭐⭐"},

{"id":"FI-002","cat":"dessin","age_range":"7-14","titre":"Dessin à 2 mains — Étoile",
 "sous":"Trace une étoile parfaite avec tes deux mains simultanément !",
 "steps":["Place les deux crayons au centre en haut de la feuille.",
          "Trace deux lignes diagonales en même temps (vers le bas-gauche et bas-droite).",
          "Sans lever les crayons, remonte vers le haut.",
          "Croise au centre, puis termine les deux derniers côtés.",
          "Colorie l'intérieur d'une couleur vive !"],
 "note":"Commence lentement — la synchronisation vient avec la pratique.",
 "zone":"✏️ Zone de dessin",
 "astuce":"Respire profondément, garde les deux crayons à la même vitesse.",
 "duree":"8 min","difficulte":"⭐⭐⭐"},

{"id":"FI-003","cat":"dessin","age_range":"6-12","titre":"Dessin à 2 mains — Maison miroir",
 "sous":"Construis deux maisons identiques en même temps !",
 "steps":["Trace une ligne verticale au milieu de ta feuille.",
          "Place un crayon de chaque côté de la ligne.",
          "Dessine le toit en triangle des deux côtés simultanément.",
          "Ajoute les murs, la porte et les fenêtres en miroir.",
          "Dessine la cheminée et la fumée des deux côtés !"],
 "note":"Si c'est trop difficile, essaie d'abord juste des cercles ou des zigzags.",
 "zone":"✏️ Zone de dessin — Feuille A4 paysage",
 "astuce":"Commence par des formes simples (cercle, carré) avant la maison.",
 "duree":"12 min","difficulte":"⭐⭐"},

{"id":"FI-004","cat":"dessin","age_range":"9-16","titre":"Griffonnage miroir avancé",
 "sous":"Crée une forme abstraite symétrique — laisse ton imagination s'exprimer !",
 "steps":["Sans réfléchir, pose les deux crayons et dessine en même temps.",
          "Fais des courbes, des spirales, des zigzags... sans t'arrêter.",
          "Ne cherche pas à faire quelque chose de précis — c'est de l'art !",
          "Au bout de 2 minutes, arrête et regarde ce que tu as créé.",
          "Repasse en couleur les formes qui te plaisent."],
 "note":"Cet exercice stimule la créativité et détend le cerveau.",
 "zone":"✏️ Zone de griffonnage libre",
 "astuce":"Mets de la musique douce pendant l'exercice.",
 "duree":"5 min","difficulte":"⭐"},

{"id":"FI-005","cat":"dessin","age_range":"8-14","titre":"Alphabet en miroir",
 "sous":"Écris les lettres A B C avec les deux mains en même temps !",
 "steps":["Sur la ligne centrale, place tes deux crayons.",
          "Trace le A avec les deux mains : les deux diagonales ensemble, puis la barre.",
          "Essaie le B, le C, le O et le X — ce sont les plus faciles.",
          "Note ton score : combien de lettres lisibles en 3 minutes ?",
          "Essaie avec des chiffres : 0, 1, 2, 3, 8..."],
 "note":"Record mondial de défi : 26 lettres lisibles. Quel est ton record ?",
 "zone":"Lignes d'entraînement : _ _ _ _ _ _ _ _ _ _ _ _ _ _ _",
 "astuce":"Les lettres symétriques (A, H, M, O, T, U, V, W, X, Y) sont les plus faciles !",
 "duree":"5 min","difficulte":"⭐⭐⭐"},

{"id":"FI-006","cat":"cerveau","age_range":"6-14","titre":"Test Stroop — Couleur vs Mot",
 "sous":"Lis la COULEUR de l'encre, pas le mot écrit !",
 "steps":["Regarde les mots ci-dessous, un par un.",
          "Pour chaque mot, dis à voix haute la COULEUR de l'encre.",
          "Exemple : si BLEU est écrit en rouge, dis ROUGE.",
          "Chronomètre-toi ! Essaie de faire les 20 mots en moins de 30 secondes.",
          "Compare avec un ami ou un parent — qui est le plus rapide ?"],
 "note":"Ce test montre que lire est automatique pour le cerveau — mais il peut apprendre à l'ignorer !",
 "zone":"ROUGE  BLEU  VERT  JAUNE  ROUGE\nBLEU  VERT  JAUNE  ROUGE  BLEU\nVERT  ROUGE  BLEU  VERT  JAUNE",
 "astuce":"Plus tu pratiques, plus ton cerveau devient rapide à gérer les conflits d'info.",
 "duree":"5 min","difficulte":"⭐⭐⭐"},

{"id":"FI-007","cat":"cerveau","age_range":"7-15","titre":"Labyrinthes cérébraux",
 "sous":"Résous 3 labyrinthes de difficulté croissante !",
 "steps":["Niveau 1 : Trace le chemin sans lever le crayon.",
          "Niveau 2 : Essaie de trouver le chemin des yeux AVANT de tracer.",
          "Niveau 3 : Fais-le en 30 secondes chrono !",
          "Bonus : Essaie à REBOURS (de la sortie vers l'entrée).",
          "Super bonus : Fais-le de la main non-dominante !"],
 "note":"Les labyrinthes entraînent la planification, l'attention et la résolution de problèmes.",
 "zone":"[Labyrinthe 1 — Facile]  [Labyrinthe 2 — Moyen]  [Labyrinthe 3 — Difficile]",
 "astuce":"Crée ton propre labyrinthe au dos et fais-le résoudre à quelqu'un !",
 "duree":"10 min","difficulte":"⭐⭐"},

{"id":"FI-008","cat":"cerveau","age_range":"8-16","titre":"Mémoire visuelle — Kim",
 "sous":"Mémorise les objets en 30 secondes, puis retrouve-les de mémoire !",
 "steps":["Regarde la grille d'objets pendant EXACTEMENT 30 secondes.",
          "Retourne la feuille ou couvre la grille.",
          "Écris tous les objets dont tu te souviens dans la zone prévue.",
          "Découvre combien tu en as mémorisé.",
          "Rejoue : est-ce que tu fais mieux la 2e fois ?"],
 "note":"Le cerveau peut mémoriser 7 (± 2) éléments en mémoire immédiate. C'est la règle de Miller !",
 "zone":"Grille : 🍎 🚗 🌟 🎸  🐶 🌈 🎃 🍕  🚀 🦋 🎩 🌸  ⚽ 🎀 🌙 🍀\nTa liste : _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _",
 "astuce":"Crée des petites histoires folles pour relier les objets — ça aide à les retenir !",
 "duree":"5 min","difficulte":"⭐⭐"},

{"id":"FI-009","cat":"cerveau","age_range":"9-16","titre":"Suite logique — Trouve l'intrus",
 "sous":"Repère l'élément qui ne suit pas la logique de la suite !",
 "steps":["Observe chaque suite de nombres ou de formes.",
          "Trouve la règle qui relie les éléments.",
          "Entoure l'intrus — l'élément qui brise la règle.",
          "Explique ta règle en une phrase.",
          "Invente ta propre suite logique pour challenger tes amis !"],
 "note":"Les suites logiques entraînent le raisonnement mathématique et la pensée abstraite.",
 "zone":"1) 2·4·6·9·10·12  Intrus:___   2) 1·1·2·3·5·8·12  Intrus:___\n3) Lundi·Mardi·Jeudi·Mercredi·Vendredi  Intrus:___",
 "astuce":"Suite 2 : c'est la suite de Fibonacci ! Chaque nombre = les 2 précédents additionnés.",
 "duree":"8 min","difficulte":"⭐⭐⭐"},

{"id":"FI-010","cat":"cerveau","age_range":"6-12","titre":"Ping-Pong des mots",
 "sous":"Alterne rapidement entre 2 catégories sans répéter ni hésiter !",
 "steps":["Avec un partenaire, choisissez 2 catégories.",
          "Exemple : Animaux / Fruits",
          "Le joueur 1 dit un animal, le joueur 2 dit un fruit, puis ré-échange.",
          "On ne peut PAS répéter un mot déjà dit.",
          "Le premier qui répète, hésite plus de 3 secondes ou se trompe a perdu !"],
 "note":"Ce jeu entraîne la fluidité verbale, la mémoire de travail et la rapidité mentale.",
 "zone":"Catégories : Animaux/Couleurs · Prénoms/Pays · Sports/Aliments · Métiers/Objets",
 "astuce":"Variante : interdire une lettre ! Pas de mot avec la lettre S.",
 "duree":"5 min","difficulte":"⭐"},

{"id":"FI-011","cat":"cerveau","age_range":"8-15","titre":"Calcul mental éclair",
 "sous":"50 opérations en 3 minutes — le cerveau à fond !",
 "steps":["Lance le chronomètre.",
          "Fais les calculs UN PAR UN sans calculatrice.",
          "Écris la réponse directement, ne t'attarde pas.",
          "Si tu bloques, passe et reviens à la fin.",
          "Corrige avec un parent ou un ami."],
 "note":"L'objectif n'est pas d'être parfait — c'est de travailler la rapidité et la concentration !",
 "zone":"7+8=  12-5=  3×4=  15÷3=  9+6=  14-7=  5×3=  20÷4=  8+9=  13-6=\n4×6=  18÷3=  7+5=  11-4=  6×3=  16÷4=  8+7=  15-8=  2×9=  21÷7=",
 "astuce":"50 réponses correctes en moins de 3 min = génie du calcul mental !",
 "duree":"5 min","difficulte":"⭐⭐⭐"},

{"id":"FI-012","cat":"cerveau","age_range":"7-13","titre":"Carte mentale — Mon univers",
 "sous":"Crée la carte de tout ce que TU aimes, sais et rêves !",
 "steps":["Écris ton prénom au centre du grand cercle.",
          "Dessine 5 branches : Ce que j'aime / Ce que je sais faire / Mes rêves / Mes amis / Ma famille.",
          "Sur chaque branche, ajoute 3 à 5 petites branches avec des mots.",
          "Colorie chaque branche d'une couleur différente.",
          "Montre ta carte à quelqu'un et explique-la !"],
 "note":"Les cartes mentales (mind maps) aident à organiser ses idées et à mieux mémoriser.",
 "zone":"[Grand cercle central + 5 branches principales à compléter]",
 "astuce":"Tu peux aussi faire une carte mentale pour réviser une leçon d'école !",
 "duree":"15 min","difficulte":"⭐"},

{"id":"FI-013","cat":"cerveau","age_range":"10-16","titre":"Défi illusions optiques",
 "sous":"Regarde ces illusions et explique ce que tu vois réellement !",
 "steps":["Observe chaque image pendant au moins 10 secondes.",
          "Décris ce que tu vois en premier.",
          "Cherche l'autre image cachée — tu la verras d'un coup !",
          "Essaie de passer d'une perception à l'autre volontairement.",
          "Explique à quelqu'un comment basculer entre les deux images."],
 "note":"Les illusions montrent que le cerveau INTERPRÈTE — il ne se contente pas de voir !",
 "zone":"Vase ou visages ?  /  Vieille femme ou jeune femme ?  /  Canard ou lapin ?",
 "astuce":"Crée ta propre illusion : dessine un cube en perspective — il peut pointer vers toi ou l'extérieur !",
 "duree":"10 min","difficulte":"⭐⭐"},

{"id":"FI-014","cat":"reflexe","age_range":"6-14","titre":"Test de la règle — Réflexes éclair",
 "sous":"Attrape la règle avant qu'elle tombe ! Mesure ta vitesse de réaction.",
 "steps":["Demande à quelqu'un de tenir une règle de 30 cm verticalement.",
          "Place le pouce et l'index à hauteur du zéro.",
          "Sans te prévenir, l'autre personne lâche la règle.",
          "Attrape-la le plus vite possible.",
          "Note le chiffre en cm là où tu as attrapé — plus c'est bas, plus tu es rapide !"],
 "note":"Conversion : 5cm=100ms, 10cm=143ms, 15cm=175ms, 20cm=202ms",
 "zone":"Essai 1: ___cm  Essai 2: ___cm  Essai 3: ___cm  Mon record: ___cm",
 "astuce":"Les sportifs de haut niveau ont des temps de réaction sous 150ms. Entraîne-toi !",
 "duree":"5 min","difficulte":"⭐"},

{"id":"FI-015","cat":"reflexe","age_range":"7-14","titre":"Jeu des 7 erreurs express",
 "sous":"Repère les 7 différences entre les deux images en moins de 2 minutes !",
 "steps":["Regarde les deux dessins côte à côte.",
          "Lance le chronomètre.",
          "Entoure chaque différence que tu trouves.",
          "Vérifie avec la correction au bas de la feuille.",
          "Essaie de battre ton record la prochaine fois !"],
 "note":"Ce jeu entraîne l'attention visuelle sélective — une compétence clé à l'école et dans la vie.",
 "zone":"[Dessine deux versions légèrement différentes d'une scène simple]",
 "astuce":"Crée tes propres 7 erreurs et fais-les trouver à ta famille !",
 "duree":"5 min","difficulte":"⭐⭐"},

{"id":"FI-016","cat":"reflexe","age_range":"8-15","titre":"Simon dit — Version papier",
 "sous":"Teste ta mémoire de séquence et ta concentration !",
 "steps":["Découpe les 16 cartes de couleur.",
          "Un joueur crée une séquence de couleurs.",
          "L'autre joueur reproduit la séquence dans l'ordre.",
          "Ajoutez une couleur à chaque tour.",
          "Le joueur qui se trompe ou oublie a perdu !"],
 "note":"La mémoire de séquence est entraînable — plus tu joues, plus ta mémoire de travail s'améliore !",
 "zone":"Cartes à découper : ROUGE  BLEU  VERT  JAUNE (x4 chaque)\nRecord: ___ couleurs mémorisées",
 "astuce":"Variante : utilise des sons (frappe la table, siffle, tape des mains).",
 "duree":"10 min","difficulte":"⭐⭐"},

{"id":"FI-017","cat":"reflexe","age_range":"9-16","titre":"Jonglage avec 2 balles — Débutant",
 "sous":"Apprends les bases du jonglage en 15 minutes !",
 "steps":["Commence avec UNE SEULE balle : lance-la d'une main à l'autre, arc de cercle.",
          "Entraîne-toi 50 fois sans faire tomber.",
          "Ajoute la 2e balle : lance la 1ère, dès qu'elle atteint son sommet, lance la 2ème.",
          "Le mot clé : Lance-lance, attrape-attrape en rythme.",
          "Record : combien d'échanges sans faire tomber ?"],
 "note":"Le jonglage développe la coordination oeil-main, la concentration et la patience.",
 "zone":"Jour 1: ___  Jour 3: ___  Jour 7: ___  Record: ___ échanges",
 "astuce":"Jongle au-dessus d'un lit — les balles rebondiront et tu éviteras de te baisser.",
 "duree":"15 min","difficulte":"⭐⭐"},

{"id":"FI-018","cat":"reflexe","age_range":"7-14","titre":"Duel des doigts",
 "sous":"5 jeux de doigts pour entraîner ta coordination !",
 "steps":["La vague : vague des doigts de la main gauche, puis droite, puis ensemble.",
          "Pouce/auriculaire : touche chaque doigt avec le pouce le plus vite possible.",
          "Rock Paper Scissors express : 10 parties en 20 secondes avec un ami.",
          "Tape la table : index G, annulaire G, index D, annulaire D... en alternance.",
          "OK/Poing alterné : main droite fait OK, main gauche fait poing — puis échange !"],
 "note":"Ces exercices activent les deux hémisphères cérébraux simultanément.",
 "zone":"Jeu 1: ___sec  Jeu 2: ___sec  Jeu 4: ___ battements en 10sec",
 "astuce":"Jeu 5 : c'est beaucoup plus dur qu'il n'y paraît ! Le cerveau adore ce genre de défi.",
 "duree":"8 min","difficulte":"⭐⭐⭐"},

{"id":"FI-019","cat":"reflexe","age_range":"8-15","titre":"Obstacle course dans ta maison",
 "sous":"Crée un parcours du combattant intérieur et bats ton chrono !",
 "steps":["Choisis 6 stations dans ta maison.",
          "Définis un défi à chaque station : 10 sauts, ramper sous une chaise...",
          "Chronomètre le parcours complet.",
          "Essaie de battre ton record 3 fois.",
          "Inverse le sens du parcours pour un défi supplémentaire !"],
 "note":"15 min d'activité physique = 2h de concentration améliorée !",
 "zone":"Station 1: ____  Station 2: ____  Station 3: ____\nStation 4: ____  Station 5: ____  Station 6: ____\nRecord: ___:___ (min:sec)",
 "astuce":"Ajoute des défis cérébraux : réciter les tables de 7, épeler un mot à l'envers...",
 "duree":"20 min","difficulte":"⭐"},

{"id":"FI-020","cat":"mandala","age_range":"5-16","titre":"Mandala des émotions",
 "sous":"Colorie ce mandala en choisissant des couleurs selon ton humeur !",
 "steps":["Choisis une couleur pour chaque émotion que tu ressens aujourd'hui.",
          "Colorie les pétales du centre (le plus important) vers l'extérieur.",
          "Il n'y a pas de mauvaises couleurs — c'est ton ressenti !",
          "Montre ton mandala à quelqu'un et explique pourquoi tu as choisi ces couleurs.",
          "Garde tes mandalas pour voir comment ton humeur change."],
 "note":"Le coloriage de mandalas réduit le stress et aide à identifier ses émotions.",
 "zone":"[Mandala à colorier : cercles concentriques avec 12 pétales]\nMon humeur: ___________  Date: ___________",
 "astuce":"Cherche 'mandala à imprimer enfant gratuit' sur internet pour plus de modèles.",
 "duree":"15 min","difficulte":"⭐"},

{"id":"FI-021","cat":"mandala","age_range":"7-16","titre":"Coloriage anti-stress — Zentangle",
 "sous":"Remplis les formes avec des motifs répétitifs pour entrer dans la zone !",
 "steps":["Trace 5 à 8 formes aléatoires qui se croisent sur ta feuille.",
          "Dans chaque forme, dessine UN seul motif répété.",
          "Chaque forme = un motif différent.",
          "Pas besoin de couleur — le jeu de noir/blanc est magnifique.",
          "Ou colorie chaque zone d'une nuance différente de la même couleur."],
 "note":"Le Zentangle est utilisé en thérapie pour réduire l'anxiété.",
 "zone":"Espace de création Zentangle\nMotifs : /// ... ~~~ ooo ### +++",
 "astuce":"Il n'y a pas d'erreurs en Zentangle — tout ce que tu fais est parfait !",
 "duree":"20 min","difficulte":"⭐"},

{"id":"FI-022","cat":"mandala","age_range":"6-14","titre":"Coloriage par numéros — Crée le tien !",
 "sous":"Invente un coloriage numéroté que tes amis devront résoudre !",
 "steps":["Dessine une scène simple (paysage, animal, personnage).",
          "Découpe ta scène en 10 zones minimum.",
          "Assigne un numéro à chaque zone.",
          "Crée la légende : 1=rouge, 2=bleu, 3=vert...",
          "Donne le dessin non colorié à quelqu'un et regarde-le colorier !"],
 "note":"Créer un coloriage est BEAUCOUP plus difficile que de le remplir — tu travailles la planification !",
 "zone":"Zone de dessin\nLégende : 1=___ 2=___ 3=___ 4=___ 5=___ 6=___ 7=___ 8=___",
 "astuce":"Partage ton coloriage sur une feuille séparée pour que quelqu'un d'autre puisse le colorier.",
 "duree":"15 min","difficulte":"⭐⭐"},

{"id":"FI-023","cat":"mandala","age_range":"8-16","titre":"Illusion de profondeur — Op Art",
 "sous":"Crée une illusion 3D avec seulement des lignes !",
 "steps":["Dessine une forme simple au centre (étoile, main, cœur).",
          "Trace des lignes parallèles dans TOUT le fond de la feuille.",
          "À l'intérieur de la forme, courbe les lignes vers le haut (comme une bosse).",
          "À l'extérieur, garde les lignes droites.",
          "Alterne deux couleurs en remplissant les bandes."],
 "note":"C'est de l'Op Art (art optique) ! Vasarely et Bridget Riley étaient maîtres dans cet art.",
 "zone":"Espace de création Op Art — A4 recommandé\nMon objet central choisi : ____________",
 "astuce":"Plus les lignes sont serrées, plus l'effet 3D est saisissant. Essaie avec 3mm d'espacement.",
 "duree":"25 min","difficulte":"⭐⭐⭐"},

{"id":"FI-024","cat":"mandala","age_range":"6-12","titre":"Coloriage ombre et lumière",
 "sous":"Apprends à donner du volume à tes dessins en 4 étapes !",
 "steps":["Dessine une sphère, un cube et un cylindre.",
          "Décide d'où vient la lumière (note une flèche).",
          "La zone face à la lumière = la plus claire.",
          "La zone opposée à la lumière = la plus foncée.",
          "Gradiente doucement du clair au foncé — voilà le volume !"],
 "note":"Ce principe de lumière/ombre est utilisé par tous les artistes depuis la Renaissance.",
 "zone":"[Cercle, carré et rectangle à ombrer]  Direction de la lumière : ☀️",
 "astuce":"Essaie avec seulement un crayon à papier : appuie fort pour le foncé, léger pour le clair.",
 "duree":"15 min","difficulte":"⭐⭐"},

{"id":"FI-025","cat":"jeu","age_range":"6-14","titre":"Escape Game dans ta chambre",
 "sous":"Crée (ou résous) un mini escape game de 15 minutes !",
 "steps":["Prépare 5 indices : chaque indice mène au suivant.",
          "Exemple : 'Regarde sous la chose où tu poses tes chaussures.'",
          "Cache les indices dans ta chambre ou dans la maison.",
          "Le dernier indice mène à une récompense.",
          "Chronomètre le joueur — peut-il résoudre en moins de 15 min ?"],
 "note":"Créer un escape game est un exercice de logique, de créativité et de mise en scène !",
 "zone":"Indices : 1→___ 2→___ 3→___ 4→___ 5→___\nRécompense: ___________",
 "astuce":"Ajoute un code à déchiffrer (lettres → chiffres) pour plus de fun !",
 "duree":"20 min","difficulte":"⭐⭐"},

{"id":"FI-026","cat":"jeu","age_range":"7-15","titre":"Bingo mental — Sans carton !",
 "sous":"Un bingo où tu mémorises ta carte dans ta tête !",
 "steps":["Chaque joueur CHOISIT mentalement 5 nombres entre 1 et 20.",
          "Un joueur pioche les nombres à voix haute.",
          "Le premier qui a ses 5 nombres piochés crie BINGO !",
          "Variante : choisir 5 animaux, 5 pays, 5 couleurs...",
          "Le truc : te souvenir de tes 5 choix pendant tout le jeu !"],
 "note":"Ce jeu entraîne la mémoire de travail — garder des infos en tête tout en faisant autre chose.",
 "zone":"Variantes : 5 fruits / 5 animaux / 5 pays / 5 prénoms / 5 mots commençant par S\nRecord de joueurs simultanés: ___",
 "astuce":"Commence par 3 éléments si 5 est trop difficile — augmente progressivement !",
 "duree":"10 min","difficulte":"⭐⭐"},

{"id":"FI-027","cat":"jeu","age_range":"8-16","titre":"Codes secrets et chiffrement",
 "sous":"Envoie et décode des messages secrets comme un vrai espion !",
 "steps":["Code César : chaque lettre avance de 3 (A→D, B→E, C→F...).",
          "Chiffre ce message avec le code César : JE SUIS UN ESPION.",
          "Invente ton propre code (substitution de symboles).",
          "Écris un message secret à quelqu'un et donne-lui la clé.",
          "Défi : décode le message sans avoir la clé — c'est de la cryptanalyse !"],
 "note":"Les codes secrets sont utilisés depuis Jules César. La cryptographie protège tes données internet !",
 "zone":"ALPHABET : A B C D E F G H I J K L M N O P Q R S T U V W X Y Z\nMON CODE :  _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _",
 "astuce":"Message à déchiffrer : NMJ FIJZ LE FZLHI  (Clé : César +5)",
 "duree":"15 min","difficulte":"⭐⭐⭐"},

{"id":"FI-028","cat":"jeu","age_range":"6-12","titre":"Théâtre des ombres",
 "sous":"Crée des personnages magiques avec tes mains et une lampe de poche !",
 "steps":["Dans une pièce sombre, place une lampe de poche face à un mur blanc.",
          "Mets tes mains entre la lampe et le mur.",
          "Essaie les formes de base : lapin, canard, chien, aigle.",
          "Crée une histoire courte avec au moins 3 personnages.",
          "Enregistre ton spectacle avec le téléphone (posé, sans le tenir) !"],
 "note":"Le théâtre développe la créativité, l'expression et la coordination fine des mains.",
 "zone":"Lapin : index et annulaire = oreilles\nCanard : pouce et 4 doigts = bec qui s'ouvre\nAigle : mains croisées, pouces croisés = corps",
 "astuce":"Variante : utilise des découpages en carton sur des bâtonnets — des marionnettes d'ombres !",
 "duree":"15 min","difficulte":"⭐"},

{"id":"FI-029","cat":"jeu","age_range":"7-15","titre":"Concours de pliage — Origami défi",
 "sous":"3 défis d'origami du facile au difficile — qui réussit le plus vite ?",
 "steps":["Niveau 1 — La grenouille sauteuse : feuille carrée, 8 plis. Lance-la !",
          "Niveau 2 — Le bateau à voile : feuille A4, 10 plis. Teste-le dans l'eau !",
          "Niveau 3 — La grue traditionnelle : feuille carrée, 20 plis.",
          "Chronomètre chaque pliage.",
          "Organisez un concours : grenouille la plus loin, bateau le plus stable, grue la plus belle !"],
 "note":"L'origami développe la motricité fine, la patience et la compréhension spatiale.",
 "zone":"Record grenouille: ___ cm de saut\nRecord bateau flotté: ___ min",
 "astuce":"100 grues en papier = un vœu qui se réalise selon la tradition japonaise (Senbazuru) !",
 "duree":"20 min","difficulte":"⭐⭐"},

{"id":"FI-030","cat":"yoga","age_range":"5-16","titre":"5 minutes pour se recentrer",
 "sous":"Une routine rapide pour calmer le cerveau et recharger ton énergie !",
 "steps":["1 min — Respiration 4-4-4 : inspire 4 sec, retiens 4 sec, expire 4 sec. Répète 4 fois.",
          "1 min — Étirement du cou : penche la tête à gauche 30 sec, à droite 30 sec.",
          "1 min — Posture de l'arbre : un pied sur la cheville, bras tendus. 30 sec chaque côté.",
          "1 min — Secousse : secoue les mains, bras, jambes — libère les tensions !",
          "1 min — Visualisation : ferme les yeux, imagine un endroit où tu te sens bien."],
 "note":"Ces 5 minutes augmentent la concentration pendant 1 à 2 heures. À faire avant les devoirs !",
 "zone":"Avant: ___/10  Après: ___/10",
 "astuce":"Fais cette routine tous les jours au même moment — le cerveau adore la régularité !",
 "duree":"5 min","difficulte":"⭐"},

{"id":"FI-031","cat":"cerveau","age_range":"6-14","titre":"L'Intrus — Trouve le Different",
 "sous":"Repere l'element qui ne ressemble pas aux autres dans chaque groupe !",
 "steps":["Regarde chaque groupe de 4 elements (mots, formes ou chiffres).",
          "Trouve celui qui ne respecte pas la meme regle que les 3 autres.",
          "Entoure l'intrus et ecris en une phrase pourquoi il est different.",
          "Niveau bonus : trouve une DEUXIEME raison qui fait de chaque element un intrus !",
          "Invente ton propre groupe de 4 avec un intrus cache."],
 "note":"Ce jeu entraine la categorisation, la pensee logique et l'attention aux details.",
 "zone":"1) Chien  Chat  Dauphin  Pierre  — Intrus: ___  Raison: ___\n2) 2  4  7  8  — Intrus: ___  Raison: ___\n3) Triangle  Carre  Cercle  Pyramide  — Intrus: ___  Raison: ___\n4) Pomme  Banane  Carotte  Cerise  — Intrus: ___  Raison: ___",
 "astuce":"Il peut y avoir plusieurs bonnes reponses ! L'important est de justifier sa logique.",
 "duree":"8 min","difficulte":"⭐⭐"},

{"id":"FI-032","cat":"cerveau","age_range":"8-16","titre":"Rotation mentale — Tourne dans ta tete",
 "sous":"Visualise la forme tournee et devine ce qu'elle donne !",
 "steps":["Regarde la forme de depart a gauche.",
          "Imagine-la tourner de 90 degres vers la droite — sans toucher.",
          "Choisis parmi les 4 options celle qui correspond au resultat.",
          "Niveau 2 : rotation de 180 degres.",
          "Niveau 3 : rotation en 3D — imagine la forme vue de l'autre cote !"],
 "note":"La rotation mentale est une des competences spatiales les plus utiles en maths, sciences et architecture.",
 "zone":"Forme modele : [L] apres 90deg = ?\nA) [J]  B) [r]  C) [L]  D) [7]\nReponds sans tourner la feuille !\nMes reponses : 1.___ 2.___ 3.___ 4.___",
 "astuce":"Les joueurs de Tetris ameliorent leur rotation mentale de 30% en 90 jours !",
 "duree":"10 min","difficulte":"⭐⭐⭐"},

{"id":"FI-033","cat":"reflexe","age_range":"5-12","titre":"Touche la bonne couleur — Defi des doigts",
 "sous":"Pose tes doigts sur les cercles en suivant les instructions !",
 "steps":["Pose ta feuille a plat sur une table.",
          "Un ami dit une couleur et un doigt (ex: Index gauche sur Rouge).",
          "Pose ce doigt sans enlever les autres.",
          "Continue : chaque nouveau doigt sur une nouvelle couleur.",
          "Essaie d'avoir 5 doigts sur 5 cercles en meme temps sans te tromper !"],
 "note":"Cet exercice entraine la coordination bilaterale, l'attention selective et la motricite fine.",
 "zone":"[6 cercles a dessiner de differentes couleurs : Rouge, Bleu, Vert, Jaune, Orange, Violet]\nScore : ___ doigts places correctement en meme temps",
 "astuce":"Version solo : utilise des des ou des cartes pour tirer les commandes au hasard !",
 "duree":"5 min","difficulte":"⭐"},

{"id":"FI-034","cat":"cerveau","age_range":"9-16","titre":"Detective de patterns — Suite a completer",
 "sous":"Decouvre la regle cachee et complete les series !",
 "steps":["Observe attentivement la suite de nombres ou de symboles.",
          "Cherche la difference entre chaque terme (+, x, alternance, Fibonacci...).",
          "Ecris le prochain terme et explique ta regle.",
          "Verifie en appliquant ta regle a toute la serie depuis le debut.",
          "Invente ta propre suite mysterieuse pour challenger tes amis."],
 "note":"Trouver des patterns est la base de l'algebre, de la programmation et de la musique !",
 "zone":"1) 1, 3, 6, 10, 15, ___ (regle : ___)\n2) 2, 6, 18, 54, ___ (regle : ___)\n3) A, C, F, J, ___ (regle : ___)\n4) 1, 1, 2, 3, 5, 8, ___ (regle : ___)\n5) 3, 1, 4, 1, 5, 9, ___ (regle : ___)",
 "astuce":"Suite 4 = Fibonacci (chaque terme = somme des 2 precedents). Suite 5 = decimales de Pi !",
 "duree":"10 min","difficulte":"⭐⭐⭐"},

{"id":"FI-035","cat":"cerveau","age_range":"7-15","titre":"Memoire photographique — Scan eclair",
 "sous":"Memorise une scene en 20 secondes puis reponds aux questions !",
 "steps":["Regarde l'image (ou la liste) pendant EXACTEMENT 20 secondes.",
          "Retourne la feuille — ne regarde plus !",
          "Reponds aux questions sans aide.",
          "Retourne la feuille et compte tes bonnes reponses.",
          "Rejoue avec quelqu'un : l'un pose les questions, l'autre memorise."],
 "note":"La memoire photographique peut s'entrainer ! Les champions de memoire utilisent des techniques de visualisation.",
 "zone":"Scene a memoriser : imagine 10 objets ranges sur une etagere\nBalle rouge  Livre bleu  Tasse jaune  Cle verte  Montre noire\nPomme rouge  Stylo violet  Caillou gris  Fleur rose  Bougie blanche\nQuestions : 1) Quelle couleur est le livre ? ___  2) Combien d'objets de couleur rouge ? ___\n3) Quel objet est entre la tasse et la cle ? ___  4) Cite 5 objets sans regarder : ___",
 "astuce":"Technique des champions : imagine une histoire bizarre qui relie tous les objets !",
 "duree":"8 min","difficulte":"⭐⭐"},
]

# ── Champs à traduire par fiche ─────────────────────────────────────────────
def collect_texts(fiche):
    """Retourne liste ordonnée de textes à traduire."""
    texts = [
        fiche["titre"],    # 0
        fiche["sous"],     # 1
    ] + fiche["steps"]    # 2..N
    # note, zone, astuce, duree labels
    texts += [
        fiche["note"],     # N+1
        fiche["zone"],     # N+2
        fiche["astuce"],   # N+3
        "⏱ " + fiche["duree"],  # N+4
    ]
    return texts

def rebuild_fiche(fiche, translated_texts):
    n_steps = len(fiche["steps"])
    new = dict(fiche)
    new["titre"]   = translated_texts[0]
    new["sous"]    = translated_texts[1]
    new["steps"]   = translated_texts[2:2+n_steps]
    new["note"]    = translated_texts[2+n_steps]
    new["zone"]    = translated_texts[3+n_steps]
    new["astuce"]  = translated_texts[4+n_steps]
    new["duree"]   = translated_texts[5+n_steps].lstrip("⏱ ")
    return new

# ── Génération PDF ───────────────────────────────────────────────────────────
def generate_pdf(fiche, lang, outdir):
    num = int(fiche["id"].split("-")[1])
    fname = f"{fiche['id']}.pdf"
    fpath = os.path.join(outdir, fname)
    os.makedirs(outdir, exist_ok=True)

    c = canvas.Canvas(fpath, pagesize=A4)
    main_col, bg_col = PAL.get(fiche["cat"], ("#6C63FF","#EDE9FF"))

    age_label = fiche["age_range"]
    draw_header(c, fiche["titre"], fiche["sous"], fiche["cat"], age_label, num, lang)

    # Badges sous le header
    y = H - 4.2*cm
    draw_badge(c, 1.2*cm, y, f"⏱ {fiche['duree']}", main_col)
    draw_badge(c, 4.5*cm, y, fiche["difficulte"], main_col)
    y -= 1.1*cm

    # Titre section Étapes — traduit
    section_labels = {
        "FR":"📋 Étapes","EN":"📋 Steps","DE":"📋 Schritte","ES":"📋 Pasos",
        "IT":"📋 Passi","PT":"📋 Passos","RU":"📋 Шаги","UK":"📋 Кроки",
        "AR":"📋 الخطوات","ZH":"📋 步骤","PL":"📋 Kroki","RO":"📋 Pași",
        "HU":"📋 Lépések","TR":"📋 Adımlar",
    }
    y = draw_section(c, y, section_labels.get(lang,"📋 Étapes"), main_col, bg_col)
    y = draw_steps(c, y, fiche["steps"], main_col)
    y -= 0.2*cm

    y = draw_note_box(c, y, fiche["note"], main_col, bg_col, "🧠")
    y = draw_note_box(c, y, fiche["astuce"], main_col, bg_col, "💡")

    # Pour les fiches dessin : exemple visuel
    if fiche["cat"] == "dessin" and fiche["id"] == "FI-001":
        y = draw_butterfly_example(c, y, main_col, bg_col, lang)

    # FI-007 : labyrinthes dans la zone
    if fiche["id"] == "FI-007":
        y = draw_maze_zone(c, y, lang)
        draw_footer(c, lang)
        c.save()
        return

    # FI-033 : cercles de couleur ; FI-035 : objets à mémoriser
    if fiche["id"] == "FI-033":
        draw_color_dots_zone(c, y, lang)
        draw_footer(c, lang); c.save(); return
    if fiche["id"] == "FI-035":
        draw_memory_zone(c, y, fiche["zone"], lang)
        draw_footer(c, lang); c.save(); return

    # FI-006 : mots Stroop en couleur discordante
    if fiche["id"] == "FI-006":
        zone_h = max(y - 1.8*cm, 0)
        if zone_h > 1*cm:
            draw_stroop_zone(c, y, zone_h, lang)
        draw_footer(c, lang)
        c.save()
        return

    zone_label = fiche["zone"]
    # Ajouter mention "verso" pour plus d'espace
    verso_hints = {
        "FR": " — ou dessine au dos pour plus grand !",
        "EN": " — or draw on the back for more space!",
        "DE": " — oder auf der Rückseite für mehr Platz!",
        "ES": " — ¡o dibuja al dorso para más espacio!",
        "IT": " — o disegna sul retro per più spazio!",
        "PT": " — ou desenha no verso para mais espaço!",
    }
    if fiche["cat"] == "dessin":
        zone_label = zone_label + verso_hints.get(lang, "")

    zone_h = max(y - 1.8*cm, 0)
    if zone_h > 0.8*cm:
        y = draw_zone(c, y, zone_label, zone_h, main_col, bg_col)

    draw_footer(c, lang)
    c.save()


def draw_butterfly_example(c, y, main_col, bg_col, lang):
    """Dessine un exemple simplifié de papillon symétrique."""
    if y < 5*cm:
        return y
    h = 4.2*cm
    # Fond N&B
    c.setFillColor(colors.white)
    c.setStrokeColor(colors.black)
    c.setLineWidth(0.8)
    c.roundRect(1*cm, y-h, W-2*cm, h, 10, fill=1, stroke=1)

    # Label "Exemple"
    ex_labels = {"FR":"Exemple","EN":"Example","DE":"Beispiel","ES":"Ejemplo","IT":"Esempio","PT":"Exemplo","AR":"مثال","ZH":"示例"}
    c.setFillColor(HexColor(main_col))
    c.setFont("Helvetica-Bold", 9)
    c.drawString(1.5*cm, y-0.45*cm, ex_labels.get(lang,"Exemple"))

    # Dessin papillon centré (bezier curves)
    cx = W/2
    cy = y - h/2 - 0.1*cm
    s = 0.6  # scale factor en cm

    c.setStrokeColor(colors.black)
    c.setLineWidth(1.5)
    c.setFillColor(HexColor("#E8E8E8"))

    # Aile gauche haute
    p = c.beginPath()
    p.moveTo(cx, cy)
    p.curveTo(cx - 2.2*s*cm, cy + 2.0*s*cm,
              cx - 4.0*s*cm, cy + 1.0*s*cm,
              cx - 2.5*s*cm, cy - 0.5*s*cm)
    p.curveTo(cx - 1.5*s*cm, cy - 0.8*s*cm, cx, cy, cx, cy)
    c.drawPath(p, fill=1, stroke=1)

    # Aile droite haute (symétrique)
    p = c.beginPath()
    p.moveTo(cx, cy)
    p.curveTo(cx + 2.2*s*cm, cy + 2.0*s*cm,
              cx + 4.0*s*cm, cy + 1.0*s*cm,
              cx + 2.5*s*cm, cy - 0.5*s*cm)
    p.curveTo(cx + 1.5*s*cm, cy - 0.8*s*cm, cx, cy, cx, cy)
    c.drawPath(p, fill=1, stroke=1)

    # Aile gauche basse
    p = c.beginPath()
    p.moveTo(cx, cy)
    p.curveTo(cx - 1.8*s*cm, cy - 0.5*s*cm,
              cx - 2.8*s*cm, cy - 1.8*s*cm,
              cx - 1.2*s*cm, cy - 1.5*s*cm)
    p.curveTo(cx - 0.5*s*cm, cy - 1.2*s*cm, cx, cy, cx, cy)
    c.drawPath(p, fill=1, stroke=1)

    # Aile droite basse
    p = c.beginPath()
    p.moveTo(cx, cy)
    p.curveTo(cx + 1.8*s*cm, cy - 0.5*s*cm,
              cx + 2.8*s*cm, cy - 1.8*s*cm,
              cx + 1.2*s*cm, cy - 1.5*s*cm)
    p.curveTo(cx + 0.5*s*cm, cy - 1.2*s*cm, cx, cy, cx, cy)
    c.drawPath(p, fill=1, stroke=1)

    # Corps (ovale central)
    c.setFillColor(colors.black)
    c.ellipse(cx - 0.18*cm, cy - 1.3*s*cm, cx + 0.18*cm, cy + 0.9*s*cm, fill=1, stroke=0)

    # Axe symétrie (tirets)
    c.setStrokeColor(HexColor("#AAAAAA"))
    c.setLineWidth(0.5)
    c.setDash([3, 3])
    c.line(cx, y - 0.6*cm, cx, y - h + 0.3*cm)
    c.setDash([])

    # Flèches ← → pour indiquer les 2 mains
    c.setFillColor(colors.black)
    c.setFont("Helvetica", 8)
    c.drawRightString(cx - 0.4*cm, cy + 1.6*s*cm, "✏️ ←")
    c.drawString(cx + 0.4*cm, cy + 1.6*s*cm, "→ ✏️")

    return y - h - 0.3*cm

def draw_one_maze(c, lx, top_y, maze_w, maze_h, walls_h, walls_v, grid):
    """
    Dessine un labyrinthe en traçant TOUS les murs de la grille,
    sauf ceux qui sont absents (passages).
    grid = (cols, rows)
    walls_h[row][col] = True  → mur horizontal entre row et row+1 à la colonne col
    walls_v[row][col] = True  → mur vertical entre col et col+1 à la ligne row
    Entrée = haut de col 0, Sortie = bas de col (cols-1)
    """
    cols, rows = grid
    cw = maze_w / cols
    ch = maze_h / rows
    lw = 1.0

    # Bordure extérieure complète sauf entrée et sortie
    c.setStrokeColor(colors.black)
    c.setLineWidth(lw)

    # Haut : toutes colonnes sauf col 0 (entrée)
    for col in range(cols):
        if col == 0:
            continue  # ouverture entrée
        c.line(lx + col*cw, top_y, lx + (col+1)*cw, top_y)

    # Bas : toutes colonnes sauf dernière (sortie)
    for col in range(cols):
        if col == cols - 1:
            continue  # ouverture sortie
        c.line(lx + col*cw, top_y - maze_h, lx + (col+1)*cw, top_y - maze_h)

    # Gauche et droite
    c.line(lx, top_y, lx, top_y - maze_h)
    c.line(lx + maze_w, top_y, lx + maze_w, top_y - maze_h)

    # Murs horizontaux intérieurs (entre row et row+1)
    # walls_h indexé 0..rows-2, row_idx = row-1 dans la liste
    for row in range(1, rows):
        for col in range(cols):
            if walls_h[row-1][col]:
                x0 = lx + col * cw
                x1 = lx + (col+1) * cw
                wy = top_y - row * ch
                c.line(x0, wy, x1, wy)

    # Murs verticaux intérieurs (entre col et col+1)
    # walls_v[row] indexé 0..cols-2, col_idx = col-1 dans la liste
    for row in range(rows):
        for col in range(1, cols):
            if walls_v[row][col-1]:
                vx = lx + col * cw
                vy0 = top_y - row * ch
                vy1 = top_y - (row+1) * ch
                c.line(vx, vy0, vx, vy1)


import random as _random

def generate_maze(rows, cols, seed=42):
    """Recursive Backtracker — génère un labyrinthe parfait garantissant une solution unique."""
    _random.seed(seed)
    walls_h = [[True]*cols for _ in range(rows-1)]
    walls_v = [[True]*(cols-1) for _ in range(rows)]
    visited = [[False]*cols for _ in range(rows)]

    def neighbors(r, c):
        result = []
        if r > 0: result.append((r-1, c, 'N'))
        if r < rows-1: result.append((r+1, c, 'S'))
        if c > 0: result.append((r, c-1, 'W'))
        if c < cols-1: result.append((r, c+1, 'E'))
        return result

    stack = [(0, 0)]
    visited[0][0] = True
    while stack:
        r, c = stack[-1]
        unvisited = [(nr, nc, d) for nr, nc, d in neighbors(r, c) if not visited[nr][nc]]
        if not unvisited:
            stack.pop()
        else:
            nr, nc, d = _random.choice(unvisited)
            if d == 'S': walls_h[r][c] = False
            elif d == 'N': walls_h[nr][c] = False
            elif d == 'E': walls_v[r][c] = False
            elif d == 'W': walls_v[r][nc] = False
            visited[nr][nc] = True
            stack.append((nr, nc))
    return walls_h, walls_v

def draw_maze_pdf(c, lx, top_y, mw, mh, rows, cols, seed=42, entry_col=0, exit_col=None):
    """Dessine un labyrinthe généré algorithmiquement (Recursive Backtracker)."""
    if exit_col is None:
        exit_col = cols - 1
    walls_h, walls_v = generate_maze(rows, cols, seed)
    cw = mw / cols
    ch_cell = mh / rows
    lw = 1.5

    c.setStrokeColor(colors.black)
    c.setLineWidth(lw)

    # Bordure extérieure complète
    c.rect(lx, top_y - mh, mw, mh, fill=0, stroke=1)

    # Effacer ouverture entrée (haut, entry_col)
    c.setFillColor(colors.white)
    c.setStrokeColor(colors.white)
    c.setLineWidth(lw + 1.5)
    ex0 = lx + entry_col * cw + cw * 0.1
    ex1 = lx + entry_col * cw + cw * 0.9
    c.line(ex0, top_y, ex1, top_y)
    # Effacer ouverture sortie (bas, exit_col)
    sx0 = lx + exit_col * cw + cw * 0.1
    sx1 = lx + exit_col * cw + cw * 0.9
    c.line(sx0, top_y - mh, sx1, top_y - mh)

    c.setStrokeColor(colors.black)
    c.setLineWidth(lw)

    # Murs intérieurs horizontaux (entre lignes r et r+1)
    for r in range(rows - 1):
        for col in range(cols):
            if walls_h[r][col]:
                x0 = lx + col * cw
                y0 = top_y - (r + 1) * ch_cell
                c.line(x0, y0, x0 + cw, y0)

    # Murs intérieurs verticaux (entre colonnes col et col+1)
    for r in range(rows):
        for col in range(cols - 1):
            if walls_v[r][col]:
                x0 = lx + (col + 1) * cw
                y0 = top_y - r * ch_cell
                c.line(x0, y0, x0, y0 - ch_cell)

    # Marqueurs Entrée (rouge) / Sortie (vert)
    c.setFillColor(HexColor("#E63946"))
    c.circle(lx + entry_col * cw + cw/2, top_y + 0.22*cm, 0.22*cm, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 7)
    c.drawCentredString(lx + entry_col * cw + cw/2, top_y + 0.15*cm, "E")

    c.setFillColor(HexColor("#4CAF50"))
    c.circle(lx + exit_col * cw + cw/2, top_y - mh - 0.22*cm, 0.22*cm, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 7)
    c.drawCentredString(lx + exit_col * cw + cw/2, top_y - mh - 0.28*cm, "S")


def draw_stroop_zone(c, y, zone_h, lang):
    """FI-006 : Affiche les mots Stroop en couleurs DISCORDANTES (effet Stroop)."""
    if zone_h < 1*cm:
        return

    # Fond blanc avec bordure
    c.setFillColor(colors.white)
    c.setStrokeColor(colors.black)
    c.setLineWidth(0.8)
    c.setDash([4, 4])
    c.roundRect(1*cm, y - zone_h, W - 2*cm, zone_h, 10, fill=1, stroke=1)
    c.setDash([])

    # Mots et leurs couleurs d'encre DISCORDANTES
    # (mot_FR, couleur_encre_hex)
    stroop_data = [
        # Ligne 1
        [("ROUGE", "#1A6EF5"), ("BLEU",  "#22A642"), ("VERT",  "#F5A623"), ("JAUNE", "#E63946")],
        # Ligne 2
        [("BLEU",  "#E63946"), ("VERT",  "#1A6EF5"), ("ROUGE", "#9B59B6"), ("ORANGE","#22A642")],
        # Ligne 3
        [("VERT",  "#F5A623"), ("JAUNE", "#9B59B6"), ("BLEU",  "#E63946"), ("ROUGE", "#1A6EF5")],
        # Ligne 4
        [("JAUNE", "#22A642"), ("ORANGE","#E63946"), ("VERT",  "#1A6EF5"), ("BLEU",  "#F5A623")],
    ]

    # Si langue non-FR, adapter les mots (traduction basique)
    word_map = {
        "EN": {"ROUGE":"RED","BLEU":"BLUE","VERT":"GREEN","JAUNE":"YELLOW","ORANGE":"ORANGE"},
        "DE": {"ROUGE":"ROT","BLEU":"BLAU","VERT":"GRÜN","JAUNE":"GELB","ORANGE":"ORANGE"},
        "ES": {"ROUGE":"ROJO","BLEU":"AZUL","VERT":"VERDE","JAUNE":"AMARILLO","ORANGE":"NARANJA"},
        "IT": {"ROUGE":"ROSSO","BLEU":"BLU","VERT":"VERDE","JAUNE":"GIALLO","ORANGE":"ARANCIO"},
        "PT": {"ROUGE":"VERMELHO","BLEU":"AZUL","VERT":"VERDE","JAUNE":"AMARELO","ORANGE":"LARANJA"},
    }
    wmap = word_map.get(lang, {})

    n_rows = len(stroop_data)
    n_cols = max(len(r) for r in stroop_data)
    row_h = zone_h / (n_rows + 0.5)
    col_w = (W - 2.2*cm) / n_cols
    font_size = min(22, row_h * 1.8)

    for ri, row in enumerate(stroop_data):
        for ci, (word_fr, color_hex) in enumerate(row):
            word = wmap.get(word_fr, word_fr)
            cx = 1.1*cm + ci * col_w + col_w / 2
            cy = y - (ri + 0.9) * row_h
            c.setFillColor(HexColor(color_hex))
            c.setFont("Helvetica-Bold", font_size)
            c.drawCentredString(cx, cy, word)


def draw_cell_maze(c, lx, top_y, mw, mh, grid_str, entry_col=0, exit_col=None):
    """
    Dessine un labyrinthe depuis une carte ASCII.
    grid_str : liste de strings, chaque char = 'X' (mur) ou ' ' (passage)
    La carte représente une grille de CELLULES avec murs intercalés.
    Format : (2*rows+1) lignes x (2*cols+1) chars
    Exemple 3x3 :
      +--+--+--+
      |        |
      +  +--+  +
      |  |     |
      +--+  +  +
      |     |  |
      +--+--+--+
    """
    rows_map = len(grid_str)
    cols_map = len(grid_str[0]) if grid_str else 0
    rows = (rows_map - 1) // 2
    cols = (cols_map - 1) // 2
    if exit_col is None:
        exit_col = cols - 1
    cw = mw / cols
    ch = mh / rows
    lw = 1.2

    c.setStrokeColor(colors.black)
    c.setLineWidth(lw)

    # Dessine tous les segments de mur depuis la carte
    for r in range(rows_map):
        for col_c in range(cols_map):
            ch_char = grid_str[r][col_c] if col_c < len(grid_str[r]) else ' '
            if ch_char not in ('-', '|', '+'):
                continue
            # Position en coordonnées PDF
            px = lx + (col_c / (cols_map - 1)) * mw
            py = top_y - (r / (rows_map - 1)) * mh

            if ch_char == '-':
                # Segment horizontal
                px0 = lx + ((col_c - 1) / (cols_map - 1)) * mw
                px1 = lx + ((col_c + 1) / (cols_map - 1)) * mw
                # Entrée : ne pas tracer le haut de la col entrée
                if r == 0 and col_c // 2 == entry_col and col_c % 2 == 1:
                    continue
                # Sortie : ne pas tracer le bas de la col sortie
                if r == rows_map - 1 and col_c // 2 == exit_col and col_c % 2 == 1:
                    continue
                c.line(px0, py, px1, py)
            elif ch_char == '|':
                py0 = top_y - ((r - 1) / (rows_map - 1)) * mh
                py1 = top_y - ((r + 1) / (rows_map - 1)) * mh
                c.line(px, py0, px, py1)


COLOR_DOTS = [("#E63946","R"),("#1D70B8","B"),("#2A9D41","V"),("#F2C200","J"),("#F77F00","O"),("#7B2CBF","Vi")]

def draw_color_dots_zone(c, y, lang):
    """FI-033 : grille de cercles colorés (gros comme un bout de doigt) — type Twister des doigts."""
    import random as _r
    h = y - 1.8*cm
    if h < 4*cm:
        return y
    c.setStrokeColor(colors.black); c.setLineWidth(0.8); c.setDash([4, 4])
    c.roundRect(1*cm, y-h, W-2*cm, h, 10, fill=0, stroke=1); c.setDash([])
    cols, d = 6, 2.3*cm
    rows = max(2, min(5, int((h - 1.6*cm) // (d + 0.45*cm))))
    gx = (W - 2*cm - cols*d) / (cols + 1)
    gy = (h - 1.4*cm - rows*d) / (rows + 1)
    rnd = _r.Random(33)
    seq = []
    for r in range(rows):
        row = COLOR_DOTS[:]; rnd.shuffle(row); seq.append(row)
    for r in range(rows):
        for k in range(cols):
            col, _ = seq[r][k]
            cx = 1*cm + gx*(k+1) + d*k + d/2
            cy = y - 0.6*cm - gy*(r+1) - d*r - d/2
            c.setFillColor(HexColor(col)); c.setStrokeColor(colors.black); c.setLineWidth(1)
            c.circle(cx, cy, d/2, fill=1, stroke=1)
    c.setFillColor(HexColor("#555555")); c.setFont("Helvetica-Oblique", 9)
    score = {"FR": "Score : ___ doigts places correctement en meme temps",
             "EN": "Score: ___ fingers placed correctly at the same time"}.get(lang, "Score : ___")
    c.drawString(1.5*cm, y - h + 0.4*cm, score)
    return y - h - 0.3*cm

def draw_memory_zone(c, y, zone_text, lang):
    """FI-035 : 10 objets colorés sur 2 étagères (à mémoriser), puis questions."""
    h = y - 1.8*cm
    if h < 5*cm:
        return y
    lines = [l for l in (zone_text or "").split("\n") if l.strip()]
    import re as _re
    names = []
    for l in lines[1:3]:
        names += [n.strip() for n in _re.split(r"\s{2,}", l) if n.strip()]
    names = names[:10]
    questions = lines[3:]
    pal = {"rouge":"#E63946","bleu":"#1D70B8","jaune":"#F2C200","vert":"#2A9D41","noir":"#222222",
           "violet":"#7B2CBF","gris":"#9A9A9A","rose":"#F28DB2","blanc":"#FFFFFF","orange":"#F77F00",
           "red":"#E63946","blue":"#1D70B8","yellow":"#F2C200","green":"#2A9D41","black":"#222222",
           "purple":"#7B2CBF","grey":"#9A9A9A","gray":"#9A9A9A","pink":"#F28DB2","white":"#FFFFFF"}
    c.setStrokeColor(colors.black); c.setLineWidth(0.8); c.setDash([4, 4])
    c.roundRect(1*cm, y-h, W-2*cm, h, 10, fill=0, stroke=1); c.setDash([])
    c.setFillColor(colors.black); c.setFont("Helvetica-Bold", 10)
    c.drawString(1.5*cm, y - 0.6*cm, (lines[0] if lines else "")[:90])
    shelf_w = W - 3*cm; slot = shelf_w / 5; r = 0.75*cm
    for row in range(2):
        base = y - 1.2*cm - (row+1)*3.0*cm
        c.setLineWidth(2.2); c.setStrokeColor(HexColor("#8B5A2B"))
        c.line(1.5*cm, base, 1.5*cm + shelf_w, base)
        for k in range(5):
            i = row*5 + k
            if i >= len(names): break
            nm = names[i]
            col = next((v for kk, v in pal.items() if kk in nm.lower()), "#CCCCCC")
            cx = 1.5*cm + slot*k + slot/2; cy = base + r + 0.75*cm
            c.setFillColor(HexColor(col)); c.setStrokeColor(colors.black); c.setLineWidth(1)
            c.circle(cx, cy, r, fill=1, stroke=1)
            c.setFillColor(colors.black); c.setFont("Helvetica-Bold", 9)
            c.drawCentredString(cx, base + 0.25*cm, nm[:22])
    # ligne de pliage + questions
    qy = y - 1.2*cm - 2*3.0*cm - 0.9*cm
    c.setDash([2, 3]); c.setStrokeColor(HexColor("#999999")); c.setLineWidth(0.8)
    c.line(1.2*cm, qy, W - 1.2*cm, qy); c.setDash([])
    c.setFillColor(HexColor("#777777")); c.setFont("Helvetica-Oblique", 8)
    fold = {"FR": "Plie ici : cache les objets avant de repondre", "EN": "Fold here: hide the objects before answering"}.get(lang, "")
    c.drawCentredString(W/2, qy - 0.35*cm, fold)
    c.setFillColor(colors.black); c.setFont("Helvetica", 11)
    qtxt = " ".join(questions)
    qs = [q.strip() for q in _re.split(r"(?=\b\d\)\s)", qtxt) if q.strip()]
    yy = qy - 1.1*cm
    for q in qs:
        if yy < y - h + 0.6*cm: break
        c.drawString(1.6*cm, yy, q[:95]); yy -= 1.0*cm
    return y - h - 0.3*cm

def draw_maze_zone(c, y, lang):
    """FI-007 : 3 labyrinthes algorithmiques (Recursive Backtracker), côte à côte."""
    if y < 4*cm:
        return y

    diff_labels = {
        "FR": ["Facile", "Moyen", "Difficile"],
        "EN": ["Easy",   "Medium", "Hard"],
        "DE": ["Leicht", "Mittel", "Schwer"],
        "ES": ["Facil",  "Medio",  "Dificil"],
        "IT": ["Facile", "Medio",  "Difficile"],
        "PT": ["Facil",  "Medio",  "Dificil"],
        "RU": ["Легко",  "Средне", "Сложно"],
        "UK": ["Легко",  "Середньо","Складно"],
        "PL": ["Łatwy",  "Średni", "Trudny"],
        "RO": ["Usor",   "Mediu",  "Dificil"],
        "HU": ["Könnyű", "Közepes","Nehéz"],
        "TR": ["Kolay",  "Orta",   "Zor"],
        "AR": ["سهل",    "متوسط",  "صعب"],
        "ZH": ["简单",    "中等",   "困难"],
    }
    lbls = diff_labels.get(lang, diff_labels["FR"])

    # 3 labyrinthes CARRÉS : Facile 5×5, Moyen 7×7, Difficile 9×9
    configs = [(5, 5, 1), (7, 7, 7), (9, 9, 13)]

    zone_h = max(y - 1.8*cm, 5*cm)
    gap = 0.7*cm
    side = min((W - 2.5*cm - 2*gap) / 3, zone_h - 1.6*cm)
    x0 = (W - (3*side + 2*gap)) / 2
    top_y = y - 0.8*cm

    for mi, ((rows, cols, seed), label) in enumerate(zip(configs, lbls)):
        lx = x0 + mi * (side + gap)
        c.setFont("Helvetica-Bold", 9)
        c.setFillColor(colors.black)
        c.drawCentredString(lx + side/2, top_y + 0.1*cm, label)
        draw_maze_pdf(c, lx, top_y - 0.3*cm, side, side, rows, cols, seed)

    # Espace restant : invente ton labyrinthe
    rest_top = top_y - 0.3*cm - side - 0.9*cm
    if rest_top - 1.8*cm > 2.5*cm:
        own = {"FR": "Invente ton labyrinthe ici et fais-le resoudre a quelqu'un !",
               "EN": "Invent your own maze here and challenge someone!"}.get(lang, "")
        if own:
            draw_zone(c, rest_top, own, rest_top - 1.8*cm, None, None)

    return y - zone_h - 0.2*cm


def draw_maze_example(c, y, main_col, bg_col, lang):
    """Dessine 3 labyrinthes navigables côte à côte : Facile / Moyen / Difficile."""
    if y < 5*cm:
        return y
    h = 5.2*cm

    # Fond blanc avec bordure
    c.setFillColor(colors.white)
    c.setStrokeColor(colors.black)
    c.setLineWidth(0.8)
    c.roundRect(1*cm, y-h, W-2*cm, h, 10, fill=1, stroke=1)

    # Label "Exemple"
    ex_labels = {"FR":"Exemple","EN":"Example","DE":"Beispiel","ES":"Ejemplo",
                 "IT":"Esempio","PT":"Exemplo","AR":"مثال","ZH":"示例"}
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(1.5*cm, y-0.42*cm, ex_labels.get(lang,"Exemple"))

    diff_labels = {
        "FR": ["Facile","Moyen","Difficile"],
        "EN": ["Easy","Medium","Hard"],
        "DE": ["Leicht","Mittel","Schwer"],
        "ES": ["Fácil","Medio","Difícil"],
        "IT": ["Facile","Medio","Difficile"],
        "PT": ["Fácil","Médio","Difícil"],
    }
    labels = diff_labels.get(lang, diff_labels["FR"])

    maze_w = 3.4*cm
    maze_h = 3.4*cm
    gap = (W - 2*cm - 3*maze_w) / 4
    top_y = y - 0.75*cm

    # Conventions :
    #   walls_h : liste de (rows-1) lignes, chaque ligne a `cols` booleans
    #             walls_h[r][c]=True → mur horizontal entre row r et r+1, colonne c
    #   walls_v : liste de `rows` lignes, chaque ligne a (cols-1) booleans
    #             walls_v[r][c]=True → mur vertical entre col c et c+1, ligne r

    # ── Labyrinthe FACILE (4 cols × 4 rows) ─────────────────────────────────
    # Chemin : col0 row0 → bas → col0 row3 → droite → col3 row3
    # walls_h : 3 lignes × 4 cols
    easy_h = [
        [0, 1, 1, 1],   # entre row0 et row1
        [1, 1, 1, 1],   # entre row1 et row2
        [1, 1, 1, 0],   # entre row2 et row3
    ]
    # walls_v : 4 lignes × 3 cols
    easy_v = [
        [1, 1, 1],      # row0
        [1, 1, 1],      # row1
        [1, 1, 1],      # row2
        [0, 0, 0],      # row3  (chemin horizontal libre)
    ]

    # ── Labyrinthe MOYEN (4 cols × 4 rows) ──────────────────────────────────
    # Chemin : col0 r0 → bas r0-r1 → droite → col2 r1 → bas r1-r3 → droite col3
    # walls_h : 3 × 4
    med_h = [
        [0, 1, 1, 1],   # entre row0 et row1
        [1, 1, 0, 1],   # entre row1 et row2 (passage col2)
        [1, 1, 0, 1],   # entre row2 et row3 (passage col2)
    ]
    # walls_v : 4 × 3
    med_v = [
        [1, 1, 1],      # row0
        [0, 1, 1],      # row1 (passage col0→col1)
        [1, 0, 1],      # row2 (passage col1→col2)
        [1, 1, 0],      # row3 (passage col2→col3)
    ]

    # ── Labyrinthe DIFFICILE (5 cols × 5 rows) ──────────────────────────────
    # Chemin en S : col0 r0→r1 | r1 col0→col2 | col2 r1→r3 | r3 col2→col4 | col4 r3→r4
    # walls_h : 4 × 5
    hard_h = [
        [0, 1, 1, 1, 1],  # row0→row1
        [1, 1, 0, 1, 1],  # row1→row2
        [1, 1, 0, 1, 1],  # row2→row3
        [1, 1, 1, 1, 0],  # row3→row4
    ]
    # walls_v : 5 × 4
    hard_v = [
        [1, 1, 1, 1],    # row0
        [0, 0, 1, 1],    # row1 (passages col0→1, col1→2)
        [1, 1, 1, 1],    # row2
        [1, 1, 0, 0],    # row3 (passages col2→3, col3→4)
        [1, 1, 1, 1],    # row4
    ]

    mazes = [
        (easy_h,  easy_v,  (4, 4)),
        (med_h,   med_v,   (4, 4)),
        (hard_h,  hard_v,  (5, 5)),
    ]

    for mi, (wh, wv, grid) in enumerate(mazes):
        cols, rows = grid
        lx = 1*cm + gap + mi*(maze_w + gap)
        draw_one_maze(c, lx, top_y, maze_w, maze_h, wh, wv, grid)

        cw = maze_w / cols

        # Marqueurs E / S
        c.setFillColor(colors.black)
        c.setFont("Helvetica-Bold", 7)
        c.drawCentredString(lx + cw*0.5, top_y + 0.18*cm, "E")
        c.drawCentredString(lx + maze_w - cw*0.5, top_y - maze_h - 0.22*cm, "S")

        # Label difficulté
        c.setFillColor(HexColor("#555555"))
        c.setFont("Helvetica", 8)
        c.drawCentredString(lx + maze_w/2, top_y - maze_h - 0.52*cm, labels[mi])

    return y - h - 0.3*cm


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Génère les fiches PDF PocketSage")
    parser.add_argument("--lang", default=None, help="Langue(s) séparées par virgule, ex: FR,EN")
    parser.add_argument("--ids",  default=None, help="IDs de fiches, ex: FI-006,FI-007,FI-031")
    args = parser.parse_args()

    if args.lang:
        langs_to_gen = [l.strip().upper() for l in args.lang.split(",")]
    else:
        langs_to_gen = list(LANGS.keys())

    if args.ids:
        ids_filter = set(i.strip() for i in args.ids.split(","))
        fiches_to_gen = [f for f in FICHES_FR if f["id"] in ids_filter]
    else:
        fiches_to_gen = FICHES_FR

    total = 0
    for lang in langs_to_gen:
        if lang not in LANGS and lang != "FR":
            print(f"  ⚠️ Langue inconnue : {lang}")
            continue
        print(f"\n Génération langue : {lang}")
        outdir = os.path.join(OUT_BASE, lang)
        os.makedirs(outdir, exist_ok=True)

        for fiche in fiches_to_gen:
            texts = collect_texts(fiche)
            if lang == "FR":
                translated = texts
            else:
                translated = translate_texts(texts, lang)
            fiche_t = rebuild_fiche(fiche, translated)
            generate_pdf(fiche_t, lang, outdir)
            print(f"  OK {lang}/{fiche['id']}.pdf")
            total += 1

    print(f"\nTERMINE — {total} PDF generes dans {OUT_BASE}/")

if __name__ == "__main__":
    main()
