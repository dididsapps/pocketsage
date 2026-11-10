#!/usr/bin/env python3
"""
Génère les MP3 ElevenLabs pour les 110 nouvelles questions CP
(après renommage des doublons).

Usage : python3 generate_new_cp_mp3.py
Les MP3 sont générés dans :
  audio/fr/  ← LG-CP-072..101, MA-CP-082..111, FR-CP-101..130
  audio/en/  ← AN-CP-122..141

Puis uploader avec : python3 upload_r2.py
"""

import re, json, requests, os, time

# ─── Config ────────────────────────────────────────────────────────────────────
# Clés : variables d'environnement ou fichier .env à la racine du repo (jamais dans le code — repo public)
import os as _os, pathlib as _pl
for _p in (_pl.Path(__file__).resolve().parent / ".env", _pl.Path(__file__).resolve().parent.parent / ".env"):
    if _p.exists():
        for _l in _p.read_text(encoding="utf-8").splitlines():
            if "=" in _l and not _l.strip().startswith("#"):
                _k, _v = _l.split("=", 1)
                _os.environ.setdefault(_k.strip(), _v.strip().strip('"').strip("'"))

API_KEY  = _os.environ.get("ELEVENLABS_API_KEY", "")
VOICE_FR = "GFj5Qf6cNQ3Lgp8VKBwc"  # Olivier
VOICE_EN = "9mF01VTvwaxuBPjm0hMu"  # Charlie Horse
INDEX    = os.path.join(os.path.dirname(__file__), "../index.html")
OUT_FR   = os.path.join(os.path.dirname(__file__), "../audio/fr")
OUT_EN   = os.path.join(os.path.dirname(__file__), "../audio/en")

# IDs à générer (les nouveaux IDs après renommage)
NEW_FR_PREFIXES = ('LG-CP-072', 'LG-CP-073', 'LG-CP-074', 'LG-CP-075',
                   'LG-CP-076', 'LG-CP-077', 'LG-CP-078', 'LG-CP-079',
                   'LG-CP-080', 'LG-CP-081', 'LG-CP-082', 'LG-CP-083',
                   'LG-CP-084', 'LG-CP-085', 'LG-CP-086', 'LG-CP-087',
                   'LG-CP-088', 'LG-CP-089', 'LG-CP-090', 'LG-CP-091',
                   'LG-CP-092', 'LG-CP-093', 'LG-CP-094', 'LG-CP-095',
                   'LG-CP-096', 'LG-CP-097', 'LG-CP-098', 'LG-CP-099',
                   'LG-CP-100', 'LG-CP-101',
                   'MA-CP-082', 'MA-CP-083', 'MA-CP-084', 'MA-CP-085',
                   'MA-CP-086', 'MA-CP-087', 'MA-CP-088', 'MA-CP-089',
                   'MA-CP-090', 'MA-CP-091', 'MA-CP-092', 'MA-CP-093',
                   'MA-CP-094', 'MA-CP-095', 'MA-CP-096', 'MA-CP-097',
                   'MA-CP-098', 'MA-CP-099', 'MA-CP-100', 'MA-CP-101',
                   'MA-CP-102', 'MA-CP-103', 'MA-CP-104', 'MA-CP-105',
                   'MA-CP-106', 'MA-CP-107', 'MA-CP-108', 'MA-CP-109',
                   'MA-CP-110', 'MA-CP-111',
                   'FR-CP-101', 'FR-CP-102', 'FR-CP-103', 'FR-CP-104',
                   'FR-CP-105', 'FR-CP-106', 'FR-CP-107', 'FR-CP-108',
                   'FR-CP-109', 'FR-CP-110', 'FR-CP-111', 'FR-CP-112',
                   'FR-CP-113', 'FR-CP-114', 'FR-CP-115', 'FR-CP-116',
                   'FR-CP-117', 'FR-CP-118', 'FR-CP-119', 'FR-CP-120',
                   'FR-CP-121', 'FR-CP-122', 'FR-CP-123', 'FR-CP-124',
                   'FR-CP-125', 'FR-CP-126', 'FR-CP-127', 'FR-CP-128',
                   'FR-CP-129', 'FR-CP-130')

NEW_EN_PREFIXES = ('AN-CP-122', 'AN-CP-123', 'AN-CP-124', 'AN-CP-125',
                   'AN-CP-126', 'AN-CP-127', 'AN-CP-128', 'AN-CP-129',
                   'AN-CP-130', 'AN-CP-131', 'AN-CP-132', 'AN-CP-133',
                   'AN-CP-134', 'AN-CP-135', 'AN-CP-136', 'AN-CP-137',
                   'AN-CP-138', 'AN-CP-139', 'AN-CP-140', 'AN-CP-141')

ALL_NEW = set(NEW_FR_PREFIXES) | set(NEW_EN_PREFIXES)

# ─── Extraction des textes depuis index.html ────────────────────────────────
print("Lecture de index.html...")
with open(INDEX, 'r', encoding='utf-8') as f:
    content = f.read()

questions = re.findall(r'\{[^{}]*?id:"([^"]+)"[^{}]*?enonce:"([^"]+)"[^{}]*?\}', content)
new_q = [(qid, txt) for qid, txt in questions if qid in ALL_NEW]
print(f"{len(new_q)} questions à générer")

# ─── Génération ─────────────────────────────────────────────────────────────
os.makedirs(OUT_FR, exist_ok=True)
os.makedirs(OUT_EN, exist_ok=True)

errors = []
for i, (qid, text) in enumerate(new_q):
    is_en = qid.startswith('AN-')
    voice  = VOICE_EN if is_en else VOICE_FR
    folder = OUT_EN if is_en else OUT_FR

    # LG-CP- → FR-CP- sur R2
    file_id  = qid.replace('LG-CP-', 'FR-CP-') if not is_en else qid
    filename = f"{file_id}.mp3" if is_en else f"{file_id}_enonce.mp3"
    filepath = os.path.join(folder, filename)

    if os.path.exists(filepath):
        print(f"  SKIP {filename}")
        continue

    url  = f"https://api.elevenlabs.io/v1/text-to-speech/{voice}"
    hdrs = {"xi-api-key": API_KEY, "Content-Type": "application/json"}
    body = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.8}
    }

    resp = requests.post(url, headers=hdrs, json=body, timeout=30)
    if resp.status_code == 200:
        with open(filepath, 'wb') as f:
            f.write(resp.content)
        lang = "EN" if is_en else "FR"
        print(f"  [{i+1}/{len(new_q)}] ✓ {lang} {filename}")
    else:
        errors.append((qid, resp.status_code, resp.text[:120]))
        print(f"  [{i+1}/{len(new_q)}] ✗ {qid}: {resp.status_code} {resp.text[:60]}")

    time.sleep(0.25)

print(f"\n✅ Terminé — FR: {len(os.listdir(OUT_FR))} fichiers, EN: {len(os.listdir(OUT_EN))} fichiers")
if errors:
    print(f"⚠️  {len(errors)} erreurs :")
    for e in errors:
        print(f"  {e}")
