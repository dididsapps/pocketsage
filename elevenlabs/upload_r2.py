#!/usr/bin/env python3
"""
Upload les MP3 locaux (audio/fr/ et audio/en/) vers R2.
Usage : python3 upload_r2.py
"""

import boto3, os

R2_ENDPOINT   = "https://8ea67fd06083effd6f76efdefb92092f.r2.cloudflarestorage.com"
R2_ACCESS_KEY = "6af471e11db12cb768c57df351e9a6fd"
R2_SECRET_KEY = "4e7b9ad69ef6072024954beb7891fe710f1008719bfbf923341bdb35e1ed4f94"
BUCKET        = "pocketsage-audio"

BASE = os.path.join(os.path.dirname(__file__), "..")

s3 = boto3.client(
    "s3",
    endpoint_url=R2_ENDPOINT,
    aws_access_key_id=R2_ACCESS_KEY,
    aws_secret_access_key=R2_SECRET_KEY,
    region_name="auto",
)

uploaded = 0
for lang_dir, r2_prefix in [("audio/fr", "audio/fr"), ("audio/en", "audio/en")]:
    local_dir = os.path.join(BASE, lang_dir)
    if not os.path.isdir(local_dir):
        continue
    for fname in sorted(os.listdir(local_dir)):
        if not fname.endswith(".mp3"):
            continue
        local_path = os.path.join(local_dir, fname)
        r2_key = f"{r2_prefix}/{fname}"
        try:
            s3.upload_file(local_path, BUCKET, r2_key,
                           ExtraArgs={"ContentType": "audio/mpeg"})
            print(f"  ✓ {r2_key}")
            uploaded += 1
        except Exception as e:
            print(f"  ✗ {r2_key}: {e}")

print(f"\n✅ {uploaded} fichiers uploadés sur R2")
