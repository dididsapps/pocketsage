#!/usr/bin/env python3
"""
PocketSage — Génération MP3 ElevenLabs pour l'onglet Nuit
Histoires du soir (HS-*), mini-histoires (HC-*), méditations (MED-*)

Usage:
  python3 generate_nuit.py

Les MP3 sont uploadés directement sur R2 dans audio/nuit/
"""

import re, os, sys, json
from pathlib import Path

# ── CONFIG ────────────────────────────────────────────────────────────────────
# Clés : variables d'environnement ou fichier .env à la racine du repo (jamais dans le code — repo public)
import os as _os, pathlib as _pl
for _p in (_pl.Path(__file__).resolve().parent / ".env", _pl.Path(__file__).resolve().parent.parent / ".env"):
    if _p.exists():
        for _l in _p.read_text(encoding="utf-8").splitlines():
            if "=" in _l and not _l.strip().startswith("#"):
                _k, _v = _l.split("=", 1)
                _os.environ.setdefault(_k.strip(), _v.strip().strip('"').strip("'"))

API_KEY    = _os.environ.get("ELEVENLABS_API_KEY", "")
VOICE_ID   = "GFj5Qf6cNQ3Lgp8VKBwc"   # Olivier (FR)
BUCKET     = "pocketsage-audio"
ENDPOINT   = "https://8ea67fd06083effd6f76efdefb92092f.r2.cloudflarestorage.com"
R2_ACCESS  = _os.environ.get("R2_ACCESS_KEY", "")
R2_SECRET  = _os.environ.get("R2_SECRET_KEY", "")
OUTPUT_DIR = Path("audio/nuit")
INDEX_HTML = Path("index.html")
CDN_BASE   = "https://pub-8cdc5500f1ab4785ba254b7335f7a68a.r2.dev"
# ─────────────────────────────────────────────────────────────────────────────

try:
    import requests
except ImportError:
    os.system("pip3 install requests -q")
    import requests

try:
    import boto3
    from botocore.config import Config
except ImportError:
    os.system("pip3 install boto3 -q")
    import boto3
    from botocore.config import Config


def extract_nuit_items(html_path):
    """Extrait histoires et méditations depuis index.html"""
    txt = html_path.read_text(encoding='utf-8')
    items = []

    # Méditations (double quotes)
    med_pat = r'\{id:"(MED-\d+)",titre:"([^"]+)",texte:"((?:[^"\\]|\\.)*)"'
    for id_, titre, texte in re.findall(med_pat, txt):
        real = texte.replace('\\"', '"').replace('\\n', '\n').replace("\\'", "'")
        items.append({'id': id_, 'titre': titre, 'texte': real, 'type': 'med'})

    # Histoires longues + courtes (simple quotes)
    hs_pat = r"\{id:'((?:HS|HC)-\d+)',titre:'([^']+)',texte:'((?:[^'\\]|\\.)*)'"
    for id_, titre, texte in re.findall(hs_pat, txt):
        real = texte.replace("\\'", "'").replace('\\n', '\n')
        items.append({'id': id_, 'titre': titre, 'texte': real, 'type': 'hs'})

    return items


def elevenlabs_tts(text, output_path):
    """Génère un MP3 via ElevenLabs"""
    r = requests.post(
        f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}",
        headers={"xi-api-key": API_KEY, "Content-Type": "application/json"},
        json={
            "text": text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {
                "stability": 0.45,
                "similarity_boost": 0.75,
                "style": 0.25,
                "use_speaker_boost": True
            }
        },
        timeout=60
    )
    if r.status_code == 200:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_bytes(r.content)
        return True
    else:
        print(f"  ❌ ElevenLabs {r.status_code}: {r.text[:120]}")
        return False


def get_r2_client():
    return boto3.client(
        "s3",
        endpoint_url=ENDPOINT,
        aws_access_key_id=R2_ACCESS,
        aws_secret_access_key=R2_SECRET,
        config=Config(region_name="auto", retries={"max_attempts": 3, "mode": "adaptive"})
    )


def list_r2_nuit(s3):
    existing = set()
    paginator = s3.get_paginator("list_objects_v2")
    for page in paginator.paginate(Bucket=BUCKET, Prefix="audio/nuit/"):
        for obj in page.get("Contents", []):
            existing.add(obj["Key"])
    return existing


def upload_to_r2(s3, local_path, r2_key):
    try:
        s3.upload_file(str(local_path), BUCKET, r2_key,
                       ExtraArgs={"ContentType": "audio/mpeg"})
        return True
    except Exception as e:
        print(f"  ❌ Upload R2: {e}")
        return False


def main():
    print("═" * 60)
    print("  PocketSage Nuit — Génération ElevenLabs + Upload R2")
    print("═" * 60)

    # Extraire les contenus
    print("\n1. Extraction des histoires et méditations...")
    items = extract_nuit_items(INDEX_HTML)
    total_chars = sum(len(it['texte']) + len(it['titre']) + 2 for it in items)
    print(f"   ✅ {len(items)} items ({total_chars:,} caractères)")
    for it in items:
        print(f"      {it['id']}: {len(it['texte'])+len(it['titre'])} chars — {it['titre'][:45]}")

    # Connexion R2
    print("\n2. Connexion R2...")
    s3 = get_r2_client()
    try:
        s3.head_bucket(Bucket=BUCKET)
        print(f"   ✅ Bucket accessible")
    except Exception as e:
        print(f"   ❌ {e}"); sys.exit(1)

    existing = list_r2_nuit(s3)
    print(f"   ✅ {len(existing)} fichiers nuit déjà sur R2")

    # Déterminer ce qui manque
    todo = []
    for it in items:
        fname = f"{it['id']}.mp3"
        r2key = f"audio/nuit/{fname}"
        if r2key not in existing:
            todo.append({**it, 'fname': fname, 'r2key': r2key})

    if not todo:
        print("\n   ✅ Tous les MP3 nuit sont déjà sur R2 !")
        print(f"\n   CDN: {CDN_BASE}/audio/nuit/")
        return

    print(f"\n3. À générer + uploader: {len(todo)} fichiers")
    print(f"   Crédits ElevenLabs estimés: ~{total_chars:,} chars")
    ans = input("   Continuer? (o/n): ").strip().lower()
    if ans not in ('o', 'oui', 'y', 'yes'):
        print("   Annulé."); return

    # Générer et uploader
    print(f"\n4. Génération + upload...")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    ok = 0; errors = 0

    for i, it in enumerate(todo):
        local = OUTPUT_DIR / it['fname']
        # Texte = titre + ". " + texte (pour une lecture naturelle)
        full_text = f"{it['titre']}. {it['texte']}"
        print(f"   [{i+1:2}/{len(todo)}] {it['id']:<8} {it['titre'][:42]}", end=' ', flush=True)

        if elevenlabs_tts(full_text, local):
            if upload_to_r2(s3, local, it['r2key']):
                print(f"✅ ({local.stat().st_size//1024}KB)")
                ok += 1
            else:
                print("⚠️  généré, upload échoué")
                errors += 1
        else:
            errors += 1

    print(f"\n{'═'*60}")
    print(f"  ✅ {ok} fichiers générés et uploadés")
    if errors: print(f"  ❌ {errors} erreurs")
    print(f"  📡 CDN: {CDN_BASE}/audio/nuit/")
    print(f"\n  Prochaine étape: mettre à jour index.html pour utiliser")
    print(f"  les MP3 R2 (audio/nuit/HS-001.mp3 etc.) à la place de l'API")
    print("═" * 60)


if __name__ == "__main__":
    main()
