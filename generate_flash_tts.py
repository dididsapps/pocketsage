#!/usr/bin/env python3
"""
PocketSage — Génération TTS Flash Savant (7 langues)
======================================================
Extrait les cartes Flash (MO/SA/EM/CF/CU/PS/MJ/EJ/PT/EN/AD) depuis index.html,
traduit titre+texte via Google Translate, génère les MP3 Google TTS
et uploade vers Cloudflare R2 dans audio/flash/{lang}/.

Usage :
  python3 generate_flash_tts.py
  GOOGLE_TTS_API_KEY=xxx python3 generate_flash_tts.py
  python3 generate_flash_tts.py --langs FR,EN,DE   # subset de langues

Langues disponibles : FR EN DE ES IT PT AR ZH
"""

import base64, json, os, re, sys, time
from pathlib import Path

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

# ─── Chemins ─────────────────────────────────────────────────────────────────
ROOT       = Path(__file__).parent
INDEX_HTML = ROOT / "index.html"
AUDIO_DIR  = ROOT / "audio" / "flash"
DATA_DIR   = ROOT / "data" / "flash_translations"
MANIFEST   = ROOT / "audio" / "manifest_flash.json"

AUDIO_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(parents=True, exist_ok=True)

# ─── Clés API ────────────────────────────────────────────────────────────────
GOOGLE_KEY    = os.environ.get("GOOGLE_TTS_API_KEY", "AIzaSyDv7OHs9VsWEsJ1loUT2IUfv2OxMs5Vpz0")
TRANSLATE_KEY = os.environ.get("GOOGLE_TRANSLATE_KEY", GOOGLE_KEY)

# ─── R2 ──────────────────────────────────────────────────────────────────────
R2_BUCKET   = "pocketsage-audio"
R2_ENDPOINT = "https://8ea67fd06083effd6f76efdefb92092f.r2.cloudflarestorage.com"
R2_ACCESS   = os.environ.get("R2_ACCESS_KEY", "de8421ae8c94c53e50ffcea2febc93e8")
R2_SECRET   = os.environ.get("R2_SECRET_KEY", "727932fe1e71c86c9e249479ce2207063867960858be8b3241ac515990a2ca28")

# ─── Voix Google TTS ─────────────────────────────────────────────────────────
VOICE_CONFIG = {
    "FR": {"languageCode": "fr-FR", "name": "fr-FR-Neural2-A"},
    "EN": {"languageCode": "en-GB", "name": "en-GB-Neural2-B"},
    "DE": {"languageCode": "de-DE", "name": "de-DE-Neural2-B"},
    "ES": {"languageCode": "es-ES", "name": "es-ES-Neural2-B"},
    "IT": {"languageCode": "it-IT", "name": "it-IT-Neural2-C"},
    "PT": {"languageCode": "pt-BR", "name": "pt-BR-Neural2-B"},
    "AR": {"languageCode": "ar-XA", "name": "ar-XA-Neural2-B"},
    "ZH": {"languageCode": "cmn-CN", "name": "cmn-CN-Neural2-B"},
}

# Codes Google Translate (source: FR)
TRANSLATE_CODES = {
    "EN": "en", "DE": "de", "ES": "es",
    "IT": "it", "PT": "pt", "AR": "ar", "ZH": "zh-CN",
}

LANGS_DEFAULT = ["FR", "EN", "DE", "ES", "IT", "PT", "AR", "ZH"]

# ─── Extraction Flash depuis index.html ──────────────────────────────────────
def extract_flash(html: str) -> list:
    pat = r"\{id:'((?:MO|SA|EM|CF|CU|PS|MJ|EJ|PT|EN|AD)-\d+)',emoji:'[^']*',titre:'((?:[^'\\]|\\.)*)',texte:'((?:[^'\\]|\\.)*)',tag:"
    items = []
    for fid, titre, texte in re.findall(pat, html):
        def unescape(s):
            try:
                return s.encode('raw_unicode_escape').decode('unicode_escape')
            except Exception:
                return s
        items.append({"id": fid, "titre": unescape(titre), "texte": unescape(texte)})
    return items

# ─── Traduction Google Translate ─────────────────────────────────────────────
def translate_batch(texts: list, target_lang: str) -> list:
    """Traduit une liste de textes vers target_lang. Retourne la liste traduite."""
    url = f"https://translation.googleapis.com/language/translate/v2?key={TRANSLATE_KEY}"
    # Batch par 128 textes max (limite API)
    results = []
    for i in range(0, len(texts), 128):
        batch = texts[i:i+128]
        payload = {"q": batch, "source": "fr", "target": TRANSLATE_CODES[target_lang], "format": "text"}
        r = requests.post(url, json=payload, timeout=30)
        if r.status_code == 200:
            translations = r.json()["data"]["translations"]
            results.extend(t["translatedText"] for t in translations)
        else:
            print(f"  ❌ Translate error {r.status_code}: {r.text[:100]}")
            results.extend(batch)   # fallback: texte FR
        time.sleep(0.1)
    return results

def load_translations(lang: str) -> dict:
    p = DATA_DIR / f"{lang}.json"
    if p.exists():
        return json.loads(p.read_text(encoding="utf-8"))
    return {}

def save_translations(lang: str, data: dict) -> None:
    p = DATA_DIR / f"{lang}.json"
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

def get_translations(items: list, lang: str) -> dict:
    """Retourne {id: 'titre. texte'} traduit pour la langue donnée."""
    if lang == "FR":
        return {item["id"]: f"{item['titre']}. {item['texte']}" for item in items}

    cache = load_translations(lang)
    missing = [item for item in items if item["id"] not in cache]

    if missing:
        print(f"  Traduction {lang} : {len(missing)} nouvelles cartes…")
        texts = [f"{item['titre']}. {item['texte']}" for item in missing]
        translated = translate_batch(texts, lang)
        for item, trad in zip(missing, translated):
            cache[item["id"]] = trad
        save_translations(lang, cache)
        print(f"  ✅ {len(missing)} traductions sauvegardées → data/flash_translations/{lang}.json")
    else:
        print(f"  ✅ {lang} : {len(cache)} traductions en cache")

    return cache

# ─── Génération MP3 Google TTS ───────────────────────────────────────────────
def gen_tts(text: str, lang: str, out_path: Path) -> bool:
    if out_path.exists():
        return True
    cfg = VOICE_CONFIG[lang]
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
    print(f"    ✗ TTS {lang} {r.status_code}: {r.text[:80]}")
    return False

# ─── R2 Upload ───────────────────────────────────────────────────────────────
def get_r2_client():
    return boto3.client(
        "s3",
        endpoint_url=R2_ENDPOINT,
        aws_access_key_id=R2_ACCESS,
        aws_secret_access_key=R2_SECRET,
        config=Config(region_name="auto", retries={"max_attempts": 3, "mode": "adaptive"})
    )

def upload_to_r2(s3, local_path: Path, r2_key: str) -> bool:
    try:
        s3.upload_file(str(local_path), R2_BUCKET, r2_key,
                       ExtraArgs={"ContentType": "audio/mpeg"})
        return True
    except Exception as e:
        print(f"    ✗ R2 upload {r2_key}: {e}")
        return False

# ─── MAIN ────────────────────────────────────────────────────────────────────
def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--langs", default=",".join(LANGS_DEFAULT),
                        help="Langues séparées par virgule (ex: FR,EN,DE)")
    parser.add_argument("--no-upload", action="store_true", help="Générer sans uploader sur R2")
    parser.add_argument("--dry-run", action="store_true", help="Simulation complète sans générer")
    args = parser.parse_args()

    langs = [l.strip().upper() for l in args.langs.split(",") if l.strip()]

    print("═" * 62)
    print("  PocketSage — Flash Savant TTS (7 langues)")
    print("═" * 62)
    print(f"  Langues : {' '.join(langs)}")

    html = INDEX_HTML.read_text(encoding="utf-8")
    items = extract_flash(html)
    print(f"  Cartes Flash extraites : {len(items)}")
    if not items:
        print("  ❌ Aucune carte trouvée — vérifier le pattern d'extraction")
        sys.exit(1)

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8")) if MANIFEST.exists() else {}

    s3 = None
    if not args.no_upload and not args.dry_run:
        try:
            s3 = get_r2_client()
            s3.list_objects_v2(Bucket=R2_BUCKET, MaxKeys=1)
            print("  R2 : ✅ connecté")
        except Exception as e:
            print(f"  R2 : ⚠️  non connecté ({e}) — génération locale uniquement")
            s3 = None

    total_ok = total_err = total_skip = 0

    for lang in langs:
        if lang not in VOICE_CONFIG:
            print(f"\n⚠️  Langue '{lang}' non configurée — ignorée")
            continue

        print(f"\n{'─'*62}")
        print(f"  🌐 {lang}")

        # Traductions
        if args.dry_run:
            print(f"  [dry-run] traduction {lang} ignorée")
            continue

        translations = get_translations(items, lang)

        lang_dir = AUDIO_DIR / lang.lower()
        lang_dir.mkdir(parents=True, exist_ok=True)

        ok = err = skip = 0
        to_upload = []

        for item in items:
            fid  = item["id"]
            text = translations.get(fid, f"{item['titre']}. {item['texte']}")
            file_id = f"{fid}_{lang}"
            out = lang_dir / f"{file_id}.mp3"
            r2_key = f"audio/flash/{lang.lower()}/{file_id}.mp3"

            if file_id in manifest:
                skip += 1
                continue

            print(f"  [{ok+err+skip+1}/{len(items)}] {file_id:<20}", end=" ", flush=True)

            if out.exists():
                print("⏭ local")
                manifest[file_id] = r2_key
                to_upload.append((out, r2_key))
                skip += 1
                continue

            success = gen_tts(text, lang, out)
            if success:
                manifest[file_id] = r2_key
                to_upload.append((out, r2_key))
                print("✅")
                ok += 1
            else:
                print("❌")
                err += 1
            time.sleep(0.15)

        # Upload R2
        if s3 and to_upload:
            print(f"\n  ☁️  Upload R2 : {len(to_upload)} fichiers…")
            u_ok = u_err = 0
            for local, key in to_upload:
                if upload_to_r2(s3, local, key):
                    u_ok += 1
                else:
                    u_err += 1
            print(f"  Upload : ✅ {u_ok}  ❌ {u_err}")

        # Sauvegarde manifest
        MANIFEST.parent.mkdir(parents=True, exist_ok=True)
        MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

        total_ok  += ok
        total_err += err
        total_skip += skip
        print(f"  Résultat {lang} : ✅ {ok} générés  ⏭ {skip} déjà faits  ❌ {err} erreurs")

    print(f"\n{'═'*62}")
    print(f"  ✅ {total_ok} générés  ⏭ {total_skip} déjà faits  ❌ {total_err} erreurs")
    print(f"  Manifest : {MANIFEST}")
    print(f"  Audio    : {AUDIO_DIR}")
    print("═" * 62)

if __name__ == "__main__":
    main()
