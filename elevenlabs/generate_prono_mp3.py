#!/usr/bin/env python3
"""
PocketSage — Génération MP3 Prononciation
==========================================
GS/CP/CE1/CE2  → ElevenLabs (EN: Charlie Horse, ES/DE: voix multilingual)
CM1+ (niv 3-4) → Google Cloud TTS Neural2

Langues : EN (audio/en/), ES (audio/es/), DE (audio/de/)
Fichiers : PR-EN-001.mp3, PR-ES-001.mp3, PR-DE-001.mp3 ...

Usage :
    cd ~/pocketsage
    pip3 install requests boto3
    python3 elevenlabs/generate_prono_mp3.py
    # Pour niveaux 3-4 Google TTS (CM1+) :
    GOOGLE_TTS_API_KEY=xxx python3 elevenlabs/generate_prono_mp3.py
"""

import re, json, os, time, base64
from pathlib import Path

# ═══════════════════════════════════════════════════
# CONFIG — clés & voix
# ═══════════════════════════════════════════════════
EL_API_KEY   = "sk_e920c195b03adac355923ab26527d2d48af72105260a0c00"
EL_VOICE_EN  = "9mF01VTvwaxuBPjm0hMu"   # Charlie Horse (EN)
EL_VOICE_ES  = "jsCqWAovK2LkecY7zXl4"   # Liam — multilingual (ES/DE fallback)
EL_VOICE_DE  = "jsCqWAovK2LkecY7zXl4"   # idem

# Google TTS Neural2 — mêmes réglages que generate_tts_google.py
GOOGLE_VOICE = {
    "EN": {"languageCode": "en-GB", "name": "en-GB-Neural2-B"},
    "ES": {"languageCode": "es-ES", "name": "es-ES-Neural2-B"},
    "DE": {"languageCode": "de-DE", "name": "de-DE-Neural2-B"},
}

R2_ACCESS_KEY = "de8421ae8c94c53e50ffcea2febc93e8"
R2_SECRET_KEY = "727932fe1e71c86c9e249479ce2207063867960858be8b3241ac515990a2ca28"
R2_ENDPOINT   = "https://8ea67fd06083effd6f76efdefb92092f.r2.cloudflarestorage.com"
R2_BUCKET     = "pocketsage-audio"

# GS/CP/CE1/CE2 → ElevenLabs ; CM1+ → Google TTS
EL_CLASSES = {"GS", "CP", "CE1", "CE2"}

LANG_DIR   = {"EN": "audio/en", "ES": "audio/es", "DE": "audio/de"}
EL_VOICE   = {"EN": EL_VOICE_EN, "ES": EL_VOICE_ES, "DE": EL_VOICE_DE}

# Chemin relatif à la racine du repo (ce script est dans elevenlabs/)
REPO_ROOT  = Path(__file__).parent.parent
INDEX_HTML = REPO_ROOT / "index.html"
OUTPUT_DIR = REPO_ROOT / "audio" / "prono"   # dossier temporaire local
MANIFEST   = REPO_ROOT / "elevenlabs" / "manifest_prono.json"

# ═══════════════════════════════════════════════════
# IMPORTS
# ═══════════════════════════════════════════════════
try:
    import requests
except ImportError:
    os.system("pip3 install requests -q"); import requests
try:
    import boto3
    from botocore.config import Config
except ImportError:
    os.system("pip3 install boto3 -q"); import boto3; from botocore.config import Config

# ═══════════════════════════════════════════════════
# EXTRACTION items depuis index.html
# ═══════════════════════════════════════════════════
def extract_items():
    content = INDEX_HTML.read_text(encoding="utf-8")
    # Pattern : {id:"PR-EN-001",classe:"GS",niveau:1,mot:"apple",...,lang:"EN"}
    pattern = r'\{id:"(PR-(?:EN|ES|DE)-\d+)",classe:"(\w+)",niveau:(\d+),mot:"([^"]+)",trad:"[^"]*",phonetique:"[^"]*",hint:"[^"]*",lang:"([^"]+)"\}'
    items = []
    for m in re.finditer(pattern, content):
        id_, classe, niveau, mot, lang = m.groups()
        items.append({"id": id_, "classe": classe, "niveau": int(niveau), "mot": mot, "lang": lang})
    return items

# ═══════════════════════════════════════════════════
# R2
# ═══════════════════════════════════════════════════
def get_r2():
    return boto3.client("s3", endpoint_url=R2_ENDPOINT,
        aws_access_key_id=R2_ACCESS_KEY, aws_secret_access_key=R2_SECRET_KEY,
        config=Config(region_name="auto", retries={"max_attempts": 3, "mode": "adaptive"}))

def r2_exists(s3, key):
    try: s3.head_object(Bucket=R2_BUCKET, Key=key); return True
    except: return False

def r2_upload(s3, local_path, key):
    s3.upload_file(str(local_path), R2_BUCKET, key,
        ExtraArgs={"ContentType": "audio/mpeg", "CacheControl": "public, max-age=31536000"})

# ═══════════════════════════════════════════════════
# ElevenLabs TTS — mêmes réglages que generate_tts.py
# ═══════════════════════════════════════════════════
def el_tts(text, voice_id, out_path):
    r = requests.post(
        f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
        headers={"xi-api-key": EL_API_KEY, "Content-Type": "application/json"},
        json={
            "text": text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.75,
                "style": 0.3,
                "use_speaker_boost": True
            }
        },
        timeout=30
    )
    if r.status_code == 200:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_bytes(r.content)
        return True
    print(f"  EL {r.status_code}: {r.text[:80]}")
    return False

# ═══════════════════════════════════════════════════
# Google TTS — mêmes réglages que generate_tts_google.py
# ═══════════════════════════════════════════════════
def google_tts(text, lang, api_key, out_path):
    cfg = GOOGLE_VOICE[lang]
    r = requests.post(
        f"https://texttospeech.googleapis.com/v1/text:synthesize?key={api_key}",
        json={
            "input": {"text": text},
            "voice": {"languageCode": cfg["languageCode"], "name": cfg["name"]},
            "audioConfig": {"audioEncoding": "MP3", "speakingRate": 0.9, "pitch": 0.0}
        },
        timeout=20
    )
    if r.status_code == 200:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_bytes(base64.b64decode(r.json()["audioContent"]))
        return True
    print(f"  Google {r.status_code}: {r.text[:80]}")
    return False

# ═══════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════
def main():
    print("═" * 60)
    print("  PocketSage — Génération MP3 Prononciation")
    print("═" * 60)

    items = extract_items()
    print(f"\n📚 {len(items)} items prono dans index.html")

    # Manifest local (ce qui a déjà été généré+uploadé)
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8")) if MANIFEST.exists() else {}

    # R2 — vérifier ce qui existe déjà
    print("🔍 Vérification R2...")
    s3 = get_r2()
    r2_existing = set()
    for pfx in ["audio/en", "audio/es", "audio/de"]:
        try:
            pag = s3.get_paginator("list_objects_v2")
            for page in pag.paginate(Bucket=R2_BUCKET, Prefix=pfx + "/PR-"):
                for obj in page.get("Contents", []):
                    r2_existing.add(Path(obj["Key"]).stem)
        except Exception as e:
            print(f"  Warning: {e}")

    # Google API key
    google_key = os.environ.get("GOOGLE_TTS_API_KEY", "").strip()

    # Calculer todo
    todo_el = []
    todo_google = []
    for item in items:
        if item["id"] in manifest and item["id"] in r2_existing:
            continue
        if item["classe"] in EL_CLASSES:
            todo_el.append(item)
        else:
            todo_google.append(item)

    print(f"✅ Déjà sur R2: {len(r2_existing)}")
    print(f"🔊 ElevenLabs à générer : {len(todo_el)}")
    print(f"🌐 Google TTS à générer : {len(todo_google)}")
    if todo_google and not google_key:
        print(f"   ⚠️  GOOGLE_TTS_API_KEY non défini → {len(todo_google)} items niv3-4 ignorés")
        print(f"   Relancer avec : GOOGLE_TTS_API_KEY=xxx python3 elevenlabs/generate_prono_mp3.py")

    todo = todo_el + (todo_google if google_key else [])
    if not todo:
        print("\n✅ Tout est déjà généré !")
        return

    print(f"\n🚀 Lancement ({len(todo)} fichiers)...\n")
    ok = skip = err = 0

    for i, item in enumerate(todo):
        id_   = item["id"]
        mot   = item["mot"]
        lang  = item["lang"]
        classe = item["classe"]
        use_el = classe in EL_CLASSES

        r2_key = f"{LANG_DIR[lang]}/{id_}.mp3"
        local  = OUTPUT_DIR / lang / f"{id_}.mp3"

        engine = "EL" if use_el else "Google"
        print(f"[{i+1:3}/{len(todo)}] {id_} {repr(mot):25s} ({classe}) [{engine}]", end=" ", flush=True)

        # Générer si pas en local
        success = False
        if local.exists():
            print("(local)", end=" "); success = True
        elif use_el:
            success = el_tts(mot, EL_VOICE[lang], local)
            if success: print("✅", end=" ")
            time.sleep(0.3)
        else:
            success = google_tts(mot, lang, google_key, local)
            if success: print("✅", end=" ")
            time.sleep(0.15)

        if success:
            try:
                r2_upload(s3, local, r2_key)
                manifest[id_] = r2_key
                print("→ R2 ✓"); ok += 1
            except Exception as e:
                print(f"→ R2 ✗ {e}"); err += 1
        else:
            print("→ skip"); skip += 1

        # Sauvegarde manifest toutes les 20
        if (i + 1) % 20 == 0:
            MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2))

    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2))

    print(f"\n{'═'*60}")
    print(f"  ✅ OK: {ok}  ⏭️  skip: {skip}  ❌ err: {err}")
    print(f"  📋 Manifest : {MANIFEST}")
    print("═" * 60)

if __name__ == "__main__":
    main()
