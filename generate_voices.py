#!/usr/bin/env python3
"""
PocketSage — Générateur de voix unifié
=======================================
Détecte automatiquement les nouveaux contenus dans index.html et génère
les MP3 manquants via ElevenLabs ou Google TTS selon la règle suivante :

  ElevenLabs  → GS, CP + modules Prononciation (FR/EN/DE)
    • FR  : Olivier       GFj5Qf6cNQ3Lgp8VKBwc
    • EN  : Mr Claus      uDsPstFWFBUXjIBimV7s
    • DE  : Nicholas      CP1kYQLB8eBoe8TavZvQ
    Post-traitement ffmpeg : atempo=0.9, asetrate×0.93 (plus grave + lent)

  Google TTS  → CE2→Lycée + ES/IT/PT/AR/ZH
    • FR  : fr-FR-Neural2-A (Algenib) — speakingRate 0.85, pitch -2.0
    • EN  : en-GB-Neural2-B — même réglages
    • ES  : es-ES-Neural2-B
    • DE  : de-DE-Neural2-B
    • IT  : it-IT-Neural2-C
    • PT  : pt-BR-Neural2-B
    • AR  : ar-XA-Neural2-B
    • ZH  : cmn-CN-Neural2-B

Usage :
  cd ~/pocketsage
  GOOGLE_TTS_API_KEY=<clé> python3 generate_voices.py
  # La clé ElevenLabs est lue depuis elevenlabs/eleven_api_key.txt
  # ou la variable ELEVEN_API_KEY.
"""

import base64, json, os, re, subprocess, sys, tempfile, time
import env_loader  # noqa: F401  (charge le fichier .env)
from pathlib import Path

# ─── Chemins ───────────────────────────────────────────────────────────────
ROOT         = Path(__file__).parent
INDEX_HTML   = ROOT / "index.html"
AUDIO_FR     = ROOT / "audio" / "fr"
AUDIO_EN     = ROOT / "audio" / "en"
AUDIO_DE     = ROOT / "audio" / "de"
AUDIO_ES     = ROOT / "audio" / "es"
MANIFEST_11  = ROOT / "audio" / "manifest.json"          # ElevenLabs
MANIFEST_G   = ROOT / "audio" / "manifest_google.json"   # Google TTS

for d in [AUDIO_FR, AUDIO_EN, AUDIO_DE, AUDIO_ES]:
    d.mkdir(parents=True, exist_ok=True)

# ─── Clés API ───────────────────────────────────────────────────────────────
def get_eleven_key():
    key = os.environ.get("ELEVEN_API_KEY", "").strip()
    if key:
        return key
    p = ROOT / "elevenlabs" / "eleven_api_key.txt"
    if p.exists():
        return p.read_text().strip()
    sys.exit("❌ Clé ElevenLabs manquante : définis ELEVEN_API_KEY dans le fichier .env (voir .env.example).")

def get_google_key():
    key = os.environ.get("GOOGLE_TTS_API_KEY", "").strip()
    if not key:
        sys.exit("❌ Clé Google manquante : définis GOOGLE_TTS_API_KEY dans le fichier .env (voir .env.example).")
    return key

ELEVEN_KEY = get_eleven_key()
GOOGLE_KEY = None   # chargé plus tard si nécessaire

# ─── Voix ElevenLabs ────────────────────────────────────────────────────────
VOICE_ELEVEN = {
    "FR": "GFj5Qf6cNQ3Lgp8VKBwc",   # Olivier
    "EN": "uDsPstFWFBUXjIBimV7s",   # Mr Claus
    "DE": "CP1kYQLB8eBoe8TavZvQ",   # Nicholas Santa
}

# ─── Voix Google TTS ────────────────────────────────────────────────────────
VOICE_GOOGLE = {
    "FR": {"languageCode": "fr-FR", "name": "fr-FR-Neural2-A"},   # Algenib
    "EN": {"languageCode": "en-GB", "name": "en-GB-Neural2-B"},
    "ES": {"languageCode": "es-ES", "name": "es-ES-Neural2-B"},
    "DE": {"languageCode": "de-DE", "name": "de-DE-Neural2-B"},
    "IT": {"languageCode": "it-IT", "name": "it-IT-Neural2-C"},
    "PT": {"languageCode": "pt-BR", "name": "pt-BR-Neural2-B"},
    "AR": {"languageCode": "ar-XA", "name": "ar-XA-Neural2-B"},
    "ZH": {"languageCode": "cmn-CN", "name": "cmn-CN-Neural2-B"},
}

# Classes ElevenLabs (GS → CE2 inclus)
ELEVEN_CLASSES = {"GS", "CP", "CE1", "CE2"}

# Préfixe module → langue
MODULE_LANG = {
    "AN": "EN", "ES": "ES", "DE": "DE", "IT": "IT",
    "PT": "PT", "AR": "AR", "ZH": "ZH",
}

def detect_lang(qid: str) -> str:
    return MODULE_LANG.get(qid.split("-")[0], "FR")

def audio_dir(lang: str) -> Path:
    dirs = {"FR": AUDIO_FR, "EN": AUDIO_EN, "DE": AUDIO_DE, "ES": AUDIO_ES}
    d = dirs.get(lang, ROOT / "audio" / lang.lower())
    d.mkdir(parents=True, exist_ok=True)
    return d

# ─── ffmpeg post-traitement ElevenLabs ──────────────────────────────────────
FFMPEG_OK = None

def has_ffmpeg() -> bool:
    global FFMPEG_OK
    if FFMPEG_OK is None:
        try:
            FFMPEG_OK = subprocess.run(
                ["ffmpeg", "-version"], capture_output=True).returncode == 0
        except FileNotFoundError:
            FFMPEG_OK = False
    return FFMPEG_OK

def apply_voice_fx(src: Path) -> None:
    """Rend Olivier plus grave (-7% fréquence) et 10% plus lent, en place.
    Appelé uniquement pour la voix FR (Olivier)."""
    if not has_ffmpeg():
        return
    tmp = src.with_suffix(".tmp.mp3")
    r = subprocess.run([
        "ffmpeg", "-y", "-i", str(src),
        "-af", "atempo=0.9,asetrate=44100*0.93,aresample=44100",
        str(tmp)
    ], capture_output=True)
    if r.returncode == 0 and tmp.exists():
        tmp.replace(src)
    elif tmp.exists():
        tmp.unlink()

# ─── Génération ElevenLabs ──────────────────────────────────────────────────
import requests

def gen_eleven(text: str, lang: str, out_path: Path) -> bool:
    if out_path.exists():
        return True   # déjà généré
    voice_id = VOICE_ELEVEN.get(lang, VOICE_ELEVEN["FR"])
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {"xi-api-key": ELEVEN_KEY, "Content-Type": "application/json"}
    body = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.75,
                           "style": 0.1, "use_speaker_boost": True}
    }
    r = requests.post(url, headers=headers, json=body, timeout=30)
    if r.status_code == 200:
        out_path.write_bytes(r.content)
        if lang == "FR":   # ffmpeg uniquement sur Olivier
            apply_voice_fx(out_path)
        return True
    print(f"    ✗ ElevenLabs {r.status_code}: {r.text[:80]}")
    return False

# ─── Génération Google TTS ──────────────────────────────────────────────────
def gen_google(text: str, lang: str, out_path: Path) -> bool:
    global GOOGLE_KEY
    if out_path.exists():
        return True
    if not GOOGLE_KEY:
        GOOGLE_KEY = get_google_key()
    cfg = VOICE_GOOGLE.get(lang, VOICE_GOOGLE["FR"])
    payload = {
        "input": {"text": text},
        "voice": {"languageCode": cfg["languageCode"], "name": cfg["name"]},
        "audioConfig": {"audioEncoding": "MP3", "speakingRate": 0.85, "pitch": -2.0}
    }
    url = f"https://texttospeech.googleapis.com/v1/text:synthesize?key={GOOGLE_KEY}"
    r = requests.post(url, json=payload, timeout=30)
    if r.status_code == 200:
        audio = r.json().get("audioContent", "")
        if audio:
            out_path.write_bytes(base64.b64decode(audio))
            return True
    print(f"    ✗ Google TTS {r.status_code}: {r.text[:80]}")
    return False

# ─── Extraction contenus de index.html ──────────────────────────────────────
def extract_questions(html: str) -> list:
    """Extrait toutes les questions {id, classe, enonce, lang}."""
    pat = r'\{id:"([^"]+)",classe:"([^"]+)",cat:"[^"]*",(?:type:"[^"]*",)?enonce:"([^"]*)",rep:"[^"]*",choix:\[([^\]]*)\]'
    items = []
    for qid, classe, enonce, choix_raw in re.findall(pat, html):
        choix = re.findall(r'"([^"]*)"', choix_raw)
        items.append({"id": qid, "classe": classe, "enonce": enonce,
                      "choix": choix, "lang": detect_lang(qid)})
    return items

def extract_prono(html: str) -> list:
    """Extrait PRONO_DATA {id, mot, phonetique, lang}."""
    pat = r'\{id:"(PR-[^"]+)",classe:"[^"]*",niveau:\d+,mot:"([^"]*)",trad:"[^"]*",phonetique:"([^"]*)",hint:"[^"]*",lang:"([^"]*)"\}'
    items = []
    for pid, mot, phon, lang in re.findall(pat, html):
        items.append({"id": pid, "mot": mot, "phonetique": phon, "lang": lang})
    return items


def extract_nuit(html: str) -> list:
    """Extrait les histoires/méditations/contes de nuit {id, titre, texte}.
    Seules les versions EN et DE sont à générer (FR déjà faite avec Olivier).
    Les textes longs sont découpés en chunks de 350 mots max pour ElevenLabs."""
    # Pattern pour HS-/HC-/MED- avec texte
    pat = r"\{id:'((?:HS|HC|MED)-\d+)',titre:'[^']*',texte:'((?:[^'\\]|\\.|'')*)',dur:"
    items = []
    for nid, texte in re.findall(pat, html):
        # Nettoyer les échappements JS
        texte = texte.replace("\\'", "'").replace('\\n', '\n').replace('\\\\', '\\')
        items.append({"id": nid, "texte": texte})
    return items


def chunk_text(text: str, max_words: int = 350) -> list:
    """Découpe un texte long en morceaux (même logique que _elChunks JS)."""
    paras = [p.strip() for p in text.split('\n') if p.strip()]
    chunks, cur, wcount = [], [], 0
    for p in paras:
        w = len(p.split())
        if wcount + w > max_words and cur:
            chunks.append('\n'.join(cur))
            cur, wcount = [], 0
        cur.append(p)
        wcount += w
    if cur:
        chunks.append('\n'.join(cur))
    return chunks or [text]

# ─── Chargement manifests ────────────────────────────────────────────────────
def load_manifest(path: Path) -> dict:
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {}

def save_manifest(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

# ─── MAIN ────────────────────────────────────────────────────────────────────
def main():
    if not INDEX_HTML.exists():
        print(f"❌ index.html introuvable dans {ROOT}")
        sys.exit(1)

    print("═" * 62)
    print("  PocketSage — Générateur de voix unifié")
    print("═" * 62)
    print(f"  ffmpeg disponible : {'✅' if has_ffmpeg() else '⚠️  non — post-traitement désactivé'}")

    html = INDEX_HTML.read_text(encoding="utf-8")
    questions = extract_questions(html)
    prono     = extract_prono(html)
    print(f"  Questions trouvées : {len(questions)}")
    print(f"  Mots Prononciation : {len(prono)}")

    nuit_items = extract_nuit(html)
    print(f"  Histoires de nuit  : {len(nuit_items)}")

    man11 = load_manifest(MANIFEST_11)
    manG  = load_manifest(MANIFEST_G)

    todo_11 = []   # (file_id, text, lang, out_path)
    todo_g  = []

    # ── Histoires de nuit EN + DE (FR déjà générée) ──
    AUDIO_NUIT = ROOT / "audio" / "nuit"
    AUDIO_NUIT.mkdir(parents=True, exist_ok=True)
    for item in nuit_items:
        nid   = item["id"]
        texte = item["texte"]
        for lang in ("EN", "DE"):
            # Fichier unique si texte court (< 350 mots), sinon chunks numérotés
            chunks = chunk_text(texte)
            if len(chunks) == 1:
                fid = f"{nid}_{lang}"
                out = AUDIO_NUIT / f"{fid}.mp3"
                if fid not in man11:
                    todo_11.append((fid, texte, lang, out))
            else:
                for i, chunk in enumerate(chunks):
                    fid = f"{nid}_{lang}_p{i+1}"
                    out = AUDIO_NUIT / f"{fid}.mp3"
                    if fid not in man11:
                        todo_11.append((fid, chunk, lang, out))

    # ── Questions ──
    for q in questions:
        qid    = q["id"]
        classe = q["classe"]
        lang   = q["lang"]
        enonce = q["enonce"]
        use_11 = classe in ELEVEN_CLASSES and lang in VOICE_ELEVEN

        # Énoncé
        fid = f"{qid}_enonce"
        fname = f"{fid}.mp3"
        out = audio_dir(lang) / fname
        if use_11:
            if fid not in man11:
                todo_11.append((fid, enonce, lang, out))
        else:
            if fid not in manG:
                todo_g.append((fid, enonce, lang, out))

        # Choix (modules langues vivantes uniquement)
        if lang != "FR":
            for i, ch in enumerate(q["choix"]):
                fid2 = f"{qid}_choix_{i}"
                out2 = audio_dir(lang) / f"{fid2}.mp3"
                if use_11:
                    if fid2 not in man11:
                        todo_11.append((fid2, ch, lang, out2))
                else:
                    if fid2 not in manG:
                        todo_g.append((fid2, ch, lang, out2))

    # ── Prononciation (toujours ElevenLabs) ──
    for p in prono:
        lang = p["lang"]
        if lang not in VOICE_ELEVEN:
            continue   # ES, ZH etc. → pas de voix eleven configurée pour prono
        fid = f"{p['id']}_mot"
        out = audio_dir(lang) / f"{fid}.mp3"
        if fid not in man11:
            todo_11.append((fid, p["mot"], lang, out))
        # Phonétique en FR (description du son)
        if p["phonetique"]:
            fid_ph = f"{p['id']}_ph"
            out_ph = AUDIO_FR / f"{fid_ph}.mp3"
            if fid_ph not in man11:
                todo_11.append((fid_ph, p["phonetique"], "FR", out_ph))

    already_11 = len(man11)
    already_g  = len(manG)
    print(f"\n  Déjà générés : {already_11} ElevenLabs / {already_g} Google TTS")
    print(f"  À générer    : {len(todo_11)} ElevenLabs / {len(todo_g)} Google TTS")

    if not todo_11 and not todo_g:
        print("\n  ✅ Tout est déjà à jour !")
        return

    total = len(todo_11) + len(todo_g)
    print(f"\n  Total : {total} MP3 à créer\n")

    ok = err = 0

    # ── ElevenLabs ──
    if todo_11:
        print(f"🎙  ElevenLabs ({len(todo_11)} fichiers)")
        for i, (fid, text, lang, out) in enumerate(todo_11):
            label = f"[{i+1}/{len(todo_11)}] [{lang}] {fid}"
            print(f"  {label:<55}", end=" ", flush=True)
            if out.exists():
                print("⏭ déjà présent")
                man11[fid] = out.name
                ok += 1
                continue
            success = gen_eleven(text, lang, out)
            if success:
                man11[fid] = out.name
                print("✅")
                ok += 1
            else:
                print("❌")
                err += 1
            if (i + 1) % 10 == 0:
                save_manifest(MANIFEST_11, man11)
            time.sleep(0.3)
        save_manifest(MANIFEST_11, man11)

    # ── Google TTS ──
    if todo_g:
        global GOOGLE_KEY
        print(f"\n🗣  Google TTS ({len(todo_g)} fichiers)")
        # Vérifier la clé
        if not GOOGLE_KEY:
            GOOGLE_KEY = get_google_key()
        # Test rapide
        test = requests.get(
            f"https://texttospeech.googleapis.com/v1/voices?languageCode=fr-FR&key={GOOGLE_KEY}",
            timeout=10)
        if test.status_code != 200:
            print(f"  ❌ Clé Google invalide ({test.status_code})")
        else:
            print(f"  ✅ Clé Google OK\n")
            for i, (fid, text, lang, out) in enumerate(todo_g):
                label = f"[{i+1}/{len(todo_g)}] [{lang}] {fid}"
                print(f"  {label:<55}", end=" ", flush=True)
                if out.exists():
                    print("⏭ déjà présent")
                    manG[fid] = out.name
                    ok += 1
                    continue
                success = gen_google(text, lang, out)
                if success:
                    manG[fid] = out.name
                    print("✅")
                    ok += 1
                else:
                    print("❌")
                    err += 1
                if (i + 1) % 20 == 0:
                    save_manifest(MANIFEST_G, manG)
                time.sleep(0.15)
            save_manifest(MANIFEST_G, manG)

    print(f"\n{'═'*62}")
    print(f"  ✅ {ok} générés  |  ❌ {err} erreurs")
    print(f"  ElevenLabs manifest : {MANIFEST_11}")
    print(f"  Google TTS manifest : {MANIFEST_G}")
    if ok > 0:
        print(f"\n  Prochaine étape :")
        print(f"  git add audio/ && git commit -m 'feat: add {ok} new TTS voices' && git push")
    print("═" * 62)


if __name__ == "__main__":
    main()
