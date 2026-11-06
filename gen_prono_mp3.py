#!/usr/bin/env python3
"""
PocketSage — Génération MP3 Prononciation (ElevenLabs + R2)
Génère les MP3 pour les 269 items PR-EN/ES/DE et les uploade sur R2.

Usage:
    pip3 install requests boto3
    python3 gen_prono_mp3.py
    # Pour niveaux 3-4 (Google TTS):
    GOOGLE_TTS_API_KEY=xxx python3 gen_prono_mp3.py

Les MP3 sont uploadés dans audio/en/, audio/es/, audio/de/ sur R2
"""

import re, json, os, time
from pathlib import Path

from env_loader import get  # clés lues dans .env (jamais dans le code)
API_KEY       = get("ELEVEN_API_KEY")
VOICE_EN = "uDsPstFWFBUXjIBimV7s"   # Mr Claus (EN) — tel quel
VOICE_ES = "GFj5Qf6cNQ3Lgp8VKBwc"   # Olivier (FR) — fallback, à remplacer par voix ES
VOICE_DE = "CP1kYQLB8eBoe8TavZvQ"   # Nicholas Santa (DE) — tel quel

R2_ACCESS_KEY  = get("R2_ACCESS_KEY_ID")
R2_SECRET_KEY  = get("R2_SECRET_ACCESS_KEY")
R2_ENDPOINT    = "https://8ea67fd06083effd6f76efdefb92092f.r2.cloudflarestorage.com"
R2_BUCKET      = "pocketsage-audio"

OUTPUT_DIR = Path("audio/prono")
INDEX_HTML = Path("index.html")

# GS/CP/CE1/CE2 → ElevenLabs ; CM1+ → Google TTS
EL_CLASSES = {"GS", "CP", "CE1", "CE2"}
GOOGLE_LANG = {"EN": "en-US", "ES": "es-ES", "DE": "de-DE"}

try:
    import requests
except ImportError:
    os.system("pip3 install requests -q"); import requests

try:
    import boto3
    from botocore.config import Config
except ImportError:
    os.system("pip3 install boto3 -q"); import boto3; from botocore.config import Config


def extract_items():
    content = open(INDEX_HTML, encoding="utf-8").read()
    pattern = r'\{id:"(PR-(?:EN|ES|DE)-\d+)",classe:"(\w+)",niveau:(\d+),mot:"([^"]+)",trad:"[^"]*",phonetique:"[^"]*",hint:"[^"]*",lang:"([^"]+)"\}'
    items = []
    for m in re.finditer(pattern, content):
        id_, classe, niveau, mot, lang = m.groups()
        items.append({"id": id_, "classe": classe, "niveau": int(niveau), "mot": mot, "lang": lang})
    return items


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


def elevenlabs_tts(text, voice_id, out_path):
    r = requests.post(
        f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
        headers={"xi-api-key": API_KEY, "Content-Type": "application/json"},
        json={"text": text, "model_id": "eleven_multilingual_v2",
              "voice_settings": {"stability": 0.65, "similarity_boost": 0.80, "style": 0.1, "use_speaker_boost": True}},
        timeout=30)
    if r.status_code == 200:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_bytes(r.content)
        return True
    print(f"  EL error {r.status_code}: {r.text[:100]}")
    return False


def google_tts(text, lang_bcp, out_path):
    api_key = get("GOOGLE_TTS_API_KEY", required=False)
    if not api_key:
        print("  ⚠️  GOOGLE_TTS_API_KEY manquant — skip")
        return False
    r = requests.post(
        f"https://texttospeech.googleapis.com/v1/text:synthesize?key={api_key}",
        json={"input": {"text": text}, "voice": {"languageCode": lang_bcp, "ssmlGender": "NEUTRAL"},
              "audioConfig": {"audioEncoding": "MP3", "speakingRate": 0.85}},
        timeout=20)
    if r.status_code == 200:
        import base64
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_bytes(base64.b64decode(r.json()["audioContent"]))
        return True
    print(f"  Google error {r.status_code}: {r.text[:100]}")
    return False


def main():
    items = extract_items()
    print(f"📚 {len(items)} items prono trouvés")

    s3 = get_r2()

    existing = set()
    for pfx in ["audio/en", "audio/es", "audio/de"]:
        try:
            pag = s3.get_paginator("list_objects_v2")
            for page in pag.paginate(Bucket=R2_BUCKET, Prefix=pfx + "/PR-"):
                for obj in page.get("Contents", []):
                    existing.add(Path(obj["Key"]).stem)
        except Exception as e:
            print(f"  Warning listing {pfx}: {e}")

    print(f"✅ Déjà sur R2: {len(existing)}")
    todo = [i for i in items if i["id"] not in existing]
    print(f"🔄 À générer: {len(todo)}\n")

    lang_dir = {"EN": "audio/en", "ES": "audio/es", "DE": "audio/de"}
    voice    = {"EN": VOICE_EN,   "ES": VOICE_ES,   "DE": VOICE_DE}
    ok = skip = err = 0

    for i, item in enumerate(todo):
        id_, mot, lang, classe = item["id"], item["mot"], item["lang"], item["classe"]
        r2_key = f"{lang_dir[lang]}/{id_}.mp3"
        local  = OUTPUT_DIR / lang / f"{id_}.mp3"
        use_el = classe in EL_CLASSES

        print(f"[{i+1}/{len(todo)}] {id_} — {repr(mot)} ({classe})", end=" ")

        success = False
        if local.exists():
            print("(local)", end=" "); success = True
        elif use_el:
            success = elevenlabs_tts(mot, voice[lang], local)
            if success: print("✅ EL", end=" ")
            time.sleep(0.3)
        else:
            success = google_tts(mot, GOOGLE_LANG[lang], local)
            if success: print("✅ Google", end=" ")

        if success:
            try:
                r2_upload(s3, local, r2_key)
                print("→ R2 ✓"); ok += 1
            except Exception as e:
                print(f"→ R2 ✗ {e}"); err += 1
        else:
            print("→ skip"); skip += 1

    print(f"\n{'='*50}")
    print(f"✅ OK: {ok}  ⏭️  skip: {skip}  ❌ err: {err}")

if __name__ == "__main__":
    main()
