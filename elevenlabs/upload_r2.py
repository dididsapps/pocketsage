#!/usr/bin/env python3
"""
Upload les MP3 locaux (audio/fr/ et audio/en/) vers R2.
Skip les fichiers déjà présents sur R2 (même taille).
Usage : python3 upload_r2.py
"""
import boto3, os

R2_ENDPOINT   = "https://8ea67fd06083effd6f76efdefb92092f.r2.cloudflarestorage.com"
import sys; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from env_loader import get  # clés lues dans .env (jamais dans le code)
R2_ACCESS_KEY = get("R2_ACCESS_KEY_ID")
R2_SECRET_KEY = get("R2_SECRET_ACCESS_KEY")
BUCKET        = "pocketsage-audio"
BASE = os.path.join(os.path.dirname(__file__), "..")

s3 = boto3.client("s3", endpoint_url=R2_ENDPOINT,
    aws_access_key_id=R2_ACCESS_KEY, aws_secret_access_key=R2_SECRET_KEY, region_name="auto")

# Récupère la liste des fichiers déjà sur R2 avec leur taille
print("📋 Récupération de la liste R2 existante...")
existing = {}
for prefix in ["audio/fr", "audio/en"]:
    paginator = s3.get_paginator("list_objects_v2")
    for page in paginator.paginate(Bucket=BUCKET, Prefix=prefix + "/"):
        for obj in page.get("Contents", []):
            existing[obj["Key"]] = obj["Size"]
print(f"  → {len(existing)} fichiers déjà sur R2\n")

uploaded = 0
skipped = 0
errors = 0

for lang_dir, r2_prefix in [("audio/fr", "audio/fr"), ("audio/en", "audio/en")]:
    local_dir = os.path.join(BASE, lang_dir)
    if not os.path.isdir(local_dir):
        continue
    files = sorted(f for f in os.listdir(local_dir) if f.endswith(".mp3"))
    print(f"📁 {lang_dir}/ : {len(files)} fichiers locaux")
    for fname in files:
        local_path = os.path.join(local_dir, fname)
        r2_key = f"{r2_prefix}/{fname}"
        local_size = os.path.getsize(local_path)
        # Skip si déjà sur R2 avec la même taille
        if r2_key in existing and existing[r2_key] == local_size:
            skipped += 1
            continue
        try:
            s3.upload_file(local_path, BUCKET, r2_key, ExtraArgs={"ContentType": "audio/mpeg"})
            print(f"  ✓ {r2_key}")
            uploaded += 1
        except Exception as e:
            print(f"  ✗ {r2_key}: {e}")
            errors += 1

print(f"\n✅ {uploaded} uploadés | ⏭ {skipped} déjà présents | ✗ {errors} erreurs")
