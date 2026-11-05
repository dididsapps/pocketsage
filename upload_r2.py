#!/usr/bin/env python3
"""
PocketSage R2 Uploader
Upload tous les MP3 depuis audio/fr/ et audio/en/ vers Cloudflare R2

Usage:
  python3 upload_r2.py --access-key TON_ACCESS_KEY --secret-key TON_SECRET_KEY

Les clés R2 se trouvent dans Cloudflare Dashboard → R2 → Manage R2 API Tokens
"""

import os, sys, json, argparse, concurrent.futures
from pathlib import Path

BUCKET = "pocketsage-audio"
ENDPOINT = "https://8ea67fd06083effd6f76efdefb92092f.r2.cloudflarestorage.com"
AUDIO_DIR = Path(__file__).parent / "audio"

try:
    import boto3
    from botocore.config import Config
except ImportError:
    print("Installation de boto3...")
    os.system("pip3 install boto3 -q")
    import boto3
    from botocore.config import Config

def get_s3_client(access_key, secret_key):
    return boto3.client(
        "s3",
        endpoint_url=ENDPOINT,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        config=Config(
            region_name="auto",
            retries={"max_attempts": 3, "mode": "adaptive"}
        )
    )

def list_r2_files(s3, prefix="audio/"):
    """Liste tous les fichiers déjà sur R2"""
    existing = set()
    paginator = s3.get_paginator("list_objects_v2")
    for page in paginator.paginate(Bucket=BUCKET, Prefix=prefix):
        for obj in page.get("Contents", []):
            existing.add(obj["Key"])
    return existing

def collect_local_files():
    """Collecte tous les MP3 locaux avec leur chemin R2 cible"""
    files = []
    for lang in ["fr", "en", "de", "es", "nuit"]:
        lang_dir = AUDIO_DIR / lang
        if lang_dir.exists():
            for mp3 in sorted(lang_dir.glob("*.mp3")):
                r2_key = f"audio/{lang}/{mp3.name}"
                files.append((mp3, r2_key))
    return files

def upload_file(s3, local_path, r2_key):
    try:
        s3.upload_file(
            str(local_path),
            BUCKET,
            r2_key,
            ExtraArgs={"ContentType": "audio/mpeg"}
        )
        return True
    except Exception as e:
        print(f"\n  ❌ {r2_key}: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Upload MP3s vers Cloudflare R2")
    parser.add_argument("--access-key", help="R2 Access Key ID")
    parser.add_argument("--secret-key", help="R2 Secret Access Key")
    parser.add_argument("--workers", type=int, default=8, help="Nombre de threads parallèles (défaut: 8)")
    parser.add_argument("--dry-run", action="store_true", help="Simulation sans upload")
    args = parser.parse_args()

    access_key = args.access_key or os.environ.get("R2_ACCESS_KEY", "").strip()
    secret_key = args.secret_key or os.environ.get("R2_SECRET_KEY", "").strip()

    if not access_key:
        access_key = input("R2 Access Key ID : ").strip()
    if not secret_key:
        secret_key = input("R2 Secret Access Key : ").strip()

    print("═" * 60)
    print("  PocketSage R2 Uploader")
    print("═" * 60)

    s3 = get_s3_client(access_key, secret_key)

    print("\n1. Connexion à R2...")
    try:
        s3.head_bucket(Bucket=BUCKET)
        print(f"   ✅ Bucket '{BUCKET}' accessible")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        sys.exit(1)

    print("\n2. Inventaire des fichiers locaux...")
    local_files = collect_local_files()
    print(f"   ✅ {len(local_files)} fichiers MP3 trouvés")
    fr_count = sum(1 for _, k in local_files if "/fr/" in k)
    en_count = sum(1 for _, k in local_files if "/en/" in k)
    print(f"   FR: {fr_count}  EN: {en_count}")

    print("\n3. Inventaire des fichiers sur R2...")
    existing = list_r2_files(s3)
    print(f"   ✅ {len(existing)} fichiers déjà sur R2")

    todo = [(lp, rk) for lp, rk in local_files if rk not in existing]
    skip = len(local_files) - len(todo)
    print(f"   À uploader: {len(todo)}  Déjà présents: {skip}")

    if not todo:
        print("\n   ✅ Tout est déjà sur R2 !")
        return

    if args.dry_run:
        print(f"\n   [DRY RUN] {len(todo)} fichiers à uploader")
        for lp, rk in todo[:10]:
            print(f"   → {rk}")
        if len(todo) > 10:
            print(f"   ... et {len(todo)-10} autres")
        return

    print(f"\n4. Upload de {len(todo)} fichiers ({args.workers} threads)...")
    ok = 0
    errors = 0

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {executor.submit(upload_file, s3, lp, rk): rk for lp, rk in todo}
        for i, future in enumerate(concurrent.futures.as_completed(futures)):
            rk = futures[future]
            success = future.result()
            if success:
                ok += 1
            else:
                errors += 1
            if (i + 1) % 50 == 0 or (i + 1) == len(todo):
                pct = (i + 1) / len(todo) * 100
                print(f"   [{i+1:4}/{len(todo)}] {pct:5.1f}% — ✅ {ok}  ❌ {errors}", end="\r")

    print(f"\n\n═" * 60)
    print(f"  ✅ {ok} fichiers uploadés")
    if errors:
        print(f"  ❌ {errors} erreurs")
    print("═" * 60)
    print("\n  Prochaine étape: vider le cache Cloudflare si nécessaire")

if __name__ == "__main__":
    main()
