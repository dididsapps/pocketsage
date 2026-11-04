#!/usr/bin/env python3
"""
Génère les MP3 Google TTS pour les 6 questions Politesse (PO-001 à PO-006).
Ces questions utilisent le champ 'situation' (pas 'enonce').

Usage : python3 generate_po_mp3.py
Les MP3 sont générés dans : audio/fr/
Puis uploader avec : python3 upload_r2.py
"""

import requests, os, urllib.parse, time

# Google TTS (pas d'API key nécessaire, endpoint public)
GOOGLE_TTS_URL = "https://translate.google.com/translate_tts"
OUT_FR = os.path.join(os.path.dirname(__file__), "../audio/fr")

# Les 6 questions Politesse avec leur texte (champ 'situation')
PO_QUESTIONS = [
    ("PO-001", "Ton ami te prête son jouet. Que dis-tu ?"),
    ("PO-002", "Tu veux un gâteau. Comment demandes-tu ?"),
    ("PO-003", "Tu arrives à l'école. La maîtresse est là."),
    ("PO-004", "Tu as renversé le verre de ton ami."),
    ("PO-005", "Ton camarade pleure dans la cour."),
    ("PO-006", "Tu joues et tu perds."),
]

os.makedirs(OUT_FR, exist_ok=True)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://translate.google.com/",
}

errors = []
for qid, text in PO_QUESTIONS:
    filename = f"{qid}_enonce.mp3"
    filepath = os.path.join(OUT_FR, filename)
    if os.path.exists(filepath):
        print(f"  SKIP {filename}")
        continue

    params = {
        "ie": "UTF-8",
        "q": text,
        "tl": "fr",
        "client": "tw-ob",
        "ttsspeed": "0.85",
    }
    url = GOOGLE_TTS_URL + "?" + urllib.parse.urlencode(params)
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        if resp.status_code == 200 and len(resp.content) > 1000:
            with open(filepath, 'wb') as f:
                f.write(resp.content)
            print(f"  ✓ {filename} ({len(resp.content)} bytes)")
        else:
            errors.append((qid, resp.status_code, len(resp.content)))
            print(f"  ✗ {qid}: HTTP {resp.status_code}, {len(resp.content)} bytes")
    except Exception as e:
        errors.append((qid, str(e), 0))
        print(f"  ✗ {qid}: {e}")
    time.sleep(0.5)

print(f"\n✅ Terminé — {len(PO_QUESTIONS)-len(errors)}/{len(PO_QUESTIONS)} générés dans audio/fr/")
if errors:
    print(f"⚠️  {len(errors)} erreurs : {errors}")
    print("\nAlternative : utiliser ElevenLabs avec generate_new_cp_mp3.py modifié")
