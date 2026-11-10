#!/usr/bin/env python3
"""
PocketSage — MP3 de l'atelier Prononciation (PR-EN / PR-ES / PR-DE)
====================================================================
Lit les items dans index.html, (re)génère UNIQUEMENT les MP3 dont le texte ou la voix
a changé, les envoie sur R2 (audio/{en,es,de}/{ID}.mp3) et tient à jour
data/prono_audio_manifest.json  →  {"PR-EN-001": "<empreinte>", ...}
L'app ajoute ?v=<empreinte> à l'URL : jamais d'ancien audio servi après une correction.

Voix (natives uniquement, pas d'accent français) :
  EN/DE, GS → CE2 : ElevenLabs (Mr Claus EN, Nicholas Santa DE)
  ES (tous niveaux) et EN/DE CM1+ : Google TTS Neural2 (en-GB, es-ES, de-DE)

Lancé automatiquement par .github/workflows/prono-tts.yml (push sur index.html).
Manuel :  python3 gen_prono_mp3.py [--dry-run] [--force]
Clés : .env ou variables d'environnement — GOOGLE_TTS_API_KEY, ELEVENLABS_API_KEY, R2_ACCESS_KEY, R2_SECRET_KEY
"""
import base64, hashlib, json, os, re, sys, tempfile, time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
_env = ROOT / ".env"
if _env.exists():
    for _l in _env.read_text(encoding="utf-8").splitlines():
        if "=" in _l and not _l.strip().startswith("#"):
            _k, _v = _l.split("=", 1)
            os.environ.setdefault(_k.strip(), _v.strip().strip('"').strip("'"))

EL_KEY     = os.environ.get("ELEVENLABS_API_KEY", "").strip().strip('"').strip("'")
GOOGLE_KEY = (os.environ.get("GOOGLE_TTS_API_KEY", "") or os.environ.get("GOOGLE_API_KEY", "")).strip()
R2_ACCESS  = os.environ.get("R2_ACCESS_KEY", "").strip()
R2_SECRET  = os.environ.get("R2_SECRET_KEY", "").strip()
R2_ENDPOINT = os.environ.get("R2_ENDPOINT", "https://8ea67fd06083effd6f76efdefb92092f.r2.cloudflarestorage.com")
R2_BUCKET  = "pocketsage-audio"

INDEX    = ROOT / "index.html"
MANIFEST = ROOT / "data" / "prono_audio_manifest.json"

EL_VOICE  = {"EN": "uDsPstFWFBUXjIBimV7s", "DE": "CP1kYQLB8eBoe8TavZvQ"}       # voix natives
EL_CLASSES = {"GS", "CP", "CE1", "CE2"}
G_VOICE   = {"EN": ("en-GB", "en-GB-Neural2-B"), "ES": ("es-ES", "es-ES-Neural2-B"), "DE": ("de-DE", "de-DE-Neural2-B")}
DIR       = {"EN": "en", "ES": "es", "DE": "de"}

ITEM_RE = re.compile(r'\{id:"(PR-(?:EN|ES|DE)-\d+)",classe:"([^"]+)",niveau:(\d+),mot:"((?:[^"\\]|\\.)+)"[^}]*?lang:"(EN|ES|DE)"')


def items():
    s = INDEX.read_text(encoding="utf-8")
    out = [{"id": m[0], "classe": m[1], "mot": m[3].replace('\\"', '"'), "lang": m[4]} for m in ITEM_RE.findall(s)]
    all_ids = re.findall(r'\{id:"(PR-(?:EN|ES|DE)-\d+)"', s)
    dup = {i for i in all_ids if all_ids.count(i) > 1}
    if dup:
        sys.exit(f"❌ IDs en double (un même son servirait deux phrases) : {sorted(dup)}")
    if len(out) != len(all_ids):
        missing = sorted(set(all_ids) - {o['id'] for o in out})
        sys.exit(f"❌ Items mal formés (champ classe/mot/lang ?) : {missing}")
    return out


def voice_of(it):
    if it["lang"] in EL_VOICE and it["classe"] in EL_CLASSES:
        return ("el", EL_VOICE[it["lang"]])
    return ("google", G_VOICE[it["lang"]][1])


def fingerprint(it):
    v = voice_of(it)
    return hashlib.sha1(f'{it["mot"]}|{v[0]}:{v[1]}'.encode()).hexdigest()[:8]


def tts_el(text, voice, out):
    import requests
    for a in range(4):
        r = requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{voice}",
                          headers={"xi-api-key": EL_KEY, "Content-Type": "application/json"},
                          json={"text": text, "model_id": "eleven_multilingual_v2",
                                "voice_settings": {"stability": 0.65, "similarity_boost": 0.8, "style": 0.1, "use_speaker_boost": True}},
                          timeout=60)
        if r.status_code == 200:
            out.write_bytes(r.content); return True
        if r.status_code in (429, 500, 502, 503): time.sleep(5 * 2 ** a); continue
        print(f"    ✗ ElevenLabs {r.status_code}: {r.text[:120]}"); return False
    return False


def tts_google(text, lang, out):
    import requests
    code, name = G_VOICE[lang]
    for a in range(4):
        r = requests.post(f"https://texttospeech.googleapis.com/v1/text:synthesize?key={GOOGLE_KEY}",
                          json={"input": {"text": text}, "voice": {"languageCode": code, "name": name},
                                "audioConfig": {"audioEncoding": "MP3", "speakingRate": 0.85}}, timeout=60)
        if r.status_code == 200:
            out.write_bytes(base64.b64decode(r.json()["audioContent"])); return True
        if r.status_code in (429, 500, 502, 503): time.sleep(5 * 2 ** a); continue
        print(f"    ✗ Google {r.status_code}: {r.text[:120]}"); return False
    return False


def main():
    dry = "--dry-run" in sys.argv; force = "--force" in sys.argv
    its = items()
    man = {} if force or not MANIFEST.exists() else json.loads(MANIFEST.read_text(encoding="utf-8"))
    todo = [it for it in its if man.get(it["id"]) != fingerprint(it)]
    print(f"Prononciation : {len(its)} items, {len(todo)} à (re)générer")
    if dry:
        for it in todo[:20]: print("  ", it["id"], voice_of(it)[0], repr(it["mot"]))
        return
    if todo and not (GOOGLE_KEY and EL_KEY and R2_ACCESS and R2_SECRET):
        sys.exit("❌ Clés manquantes (GOOGLE_TTS_API_KEY, ELEVENLABS_API_KEY, R2_ACCESS_KEY, R2_SECRET_KEY)")
    import boto3
    from botocore.config import Config
    s3 = boto3.client("s3", endpoint_url=R2_ENDPOINT, aws_access_key_id=R2_ACCESS, aws_secret_access_key=R2_SECRET,
                      config=Config(region_name="auto", retries={"max_attempts": 3, "mode": "adaptive"}))
    tmp = Path(tempfile.mkdtemp()); ok = err = 0
    for i, it in enumerate(todo, 1):
        out = tmp / f'{it["id"]}.mp3'
        kind, voice = voice_of(it)
        good = tts_el(it["mot"], voice, out) if kind == "el" else tts_google(it["mot"], it["lang"], out)
        if good:
            try:
                s3.upload_file(str(out), R2_BUCKET, f'audio/{DIR[it["lang"]]}/{it["id"]}.mp3',
                               ExtraArgs={"ContentType": "audio/mpeg", "CacheControl": "public, max-age=31536000"})
                man[it["id"]] = fingerprint(it); ok += 1
            except Exception as e:
                print(f"    ✗ R2 {it['id']}: {e}"); err += 1
        else:
            err += 1
        if i % 20 == 0:
            MANIFEST.parent.mkdir(parents=True, exist_ok=True)
            MANIFEST.write_text(json.dumps(man, indent=1, sort_keys=True) + "\n", encoding="utf-8")
            print(f"  {i}/{len(todo)}")
        time.sleep(0.2)
    # nettoyer les entrées d'items supprimés
    ids = {it["id"] for it in its}
    man = {k: v for k, v in man.items() if k in ids}
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(json.dumps(man, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Terminé : {ok} MP3 publiés, {err} erreur(s)")
    if err: sys.exit(2)


if __name__ == "__main__":
    main()
