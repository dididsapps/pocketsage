#!/usr/bin/env python3
"""
PocketSage Academy - ElevenLabs TTS Generator (English)
Génère les MP3 pour les questions GS→CE2 type Anglais
Voix: Olivier EN (9mF01VTvwaxuBPjm0hMu)

Usage:
  python3 generate_en_tts.py

Requires:
  pip install requests
  index.html dans le même dossier (ou modifier INDEX_PATH)
"""

import re
import os
import time
import requests

# ── Configuration ──────────────────────────────────────────────────────────────
ELEVENLABS_API_KEY = "sk_e920c195b03adac355923ab26527d2d48af72105260a0c00"
VOICE_ID = "9mF01VTvwaxuBPjm0hMu"  # Olivier EN
OUTPUT_DIR = "audio/en"
INDEX_PATH = "index.html"

# Classes ciblées (comme pour le FR : GS → CE2)
TARGET_CLASSES = {"GS", "CP", "CE1", "CE2"}

# ElevenLabs TTS settings
MODEL_ID = "eleven_multilingual_v2"
VOICE_SETTINGS = {
    "stability": 0.5,
    "similarity_boost": 0.75,
    "style": 0.0,
    "use_speaker_boost": True
}

# ── Extract questions ──────────────────────────────────────────────────────────
print("📖 Lecture de index.html...")
content = open(INDEX_PATH, encoding="utf-8").read()

pattern = r'\{id:"(AN-([A-Z0-9]+)-\d+)"[^}]*?enonce:"((?:[^"\\]|\\.)*?)"'
all_matches = re.findall(pattern, content)

# Filtrer GS → CE2
matches = [(qid, enonce) for qid, classe, enonce in all_matches if classe in TARGET_CLASSES]
print(f"✅ {len(matches)} questions Anglais trouvées (GS → CE2)")

from collections import Counter
classes_count = Counter(m[0].split('-')[1] for m in matches)
for k, v in sorted(classes_count.items()):
    print(f"   {k}: {v}")

# ── Create output directory ────────────────────────────────────────────────────
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ── Generate TTS ──────────────────────────────────────────────────────────────
url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
headers = {
    "xi-api-key": ELEVENLABS_API_KEY,
    "Content-Type": "application/json"
}

total = len(matches)
skipped = 0
generated = 0
errors = []

for i, (qid, enonce) in enumerate(matches, 1):
    out_path = os.path.join(OUTPUT_DIR, f"{qid}.mp3")

    # Skip if already generated
    if os.path.exists(out_path) and os.path.getsize(out_path) > 1000:
        skipped += 1
        print(f"  ⏭️  [{i}/{total}] {qid} (déjà généré)")
        continue

    # Clean text
    text = enonce.replace("\\'", "'").replace('\\"', '"').replace("\\n", " ").strip()
    if not text:
        print(f"  ⚠️  [{i}/{total}] {qid} - texte vide, ignoré")
        continue

    print(f"  🎙️  [{i}/{total}] {qid}: {text[:60]}...")

    payload = {
        "text": text,
        "model_id": MODEL_ID,
        "voice_settings": VOICE_SETTINGS
    }

    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=30)

        if resp.status_code == 200:
            with open(out_path, "wb") as f:
                f.write(resp.content)
            generated += 1
            print(f"         ✅ {len(resp.content)//1024}KB")
        elif resp.status_code == 429:
            print(f"         ⏳ Rate limit - pause 60s...")
            time.sleep(60)
            resp = requests.post(url, json=payload, headers=headers, timeout=30)
            if resp.status_code == 200:
                with open(out_path, "wb") as f:
                    f.write(resp.content)
                generated += 1
                print(f"         ✅ Retry OK")
            else:
                errors.append(qid)
                print(f"         ❌ {resp.status_code}")
        else:
            errors.append(qid)
            print(f"         ❌ {resp.status_code} - {resp.text[:100]}")
    except Exception as e:
        errors.append(qid)
        print(f"         ❌ {e}")

    time.sleep(0.5)

# ── Summary ────────────────────────────────────────────────────────────────────
print(f"\n{'='*50}")
print(f"✅ Générés  : {generated}")
print(f"⏭️  Ignorés  : {skipped}")
if errors:
    print(f"❌ Erreurs  : {len(errors)} — {', '.join(errors)}")
else:
    print(f"🎉 Aucune erreur !")

print(f"\n🚀 Upload sur R2 :")
print(f"   rclone copy audio/en r2:pocketsage-audio/audio/en --progress")
