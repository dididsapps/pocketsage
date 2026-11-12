#!/usr/bin/env python3
"""
PocketSage — Coach Sportif : MP3 des phrases du coach (voix Google énergique, débit normal)
=========================================================================================
1. `node tools/sport_texts.js` → toutes les phrases (consignes, encouragements, phases, GO/NEXT…)
2. Génère seulement les MP3 nouveaux → R2 audio/sport/fr/{hash}.mp3
3. Écrit data/sport/fr.audio.json  →  {"texte exact": "hash"} (lu par js/coach-voix.js)

Voix : on essaie d'abord une voix Google « Chirp 3 HD » enjouée (Puck), débit 0,95 ;
si elle n'est pas disponible, voix Neural2 masculine, débit 0,95, un peu plus aiguë (plus dynamique).
Lancé par .github/workflows/sport-tts.yml. Manuel : python3 gen_sport_mp3.py [--check]
"""
import base64, hashlib, json, os, subprocess, sys, tempfile, time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
_env = ROOT / ".env"
if _env.exists():
    for _l in _env.read_text(encoding="utf-8").splitlines():
        if "=" in _l and not _l.strip().startswith("#"):
            _k, _v = _l.split("=", 1)
            os.environ.setdefault(_k.strip(), _v.strip().strip('"').strip("'"))

GOOGLE_KEY = os.environ.get("GOOGLE_TTS_API_KEY", "").strip()
R2_ACCESS = os.environ.get("R2_ACCESS_KEY", "").strip()
R2_SECRET = os.environ.get("R2_SECRET_KEY", "").strip()
R2_ENDPOINT = os.environ.get("R2_ENDPOINT", "https://8ea67fd06083effd6f76efdefb92092f.r2.cloudflarestorage.com")
R2_BUCKET = "pocketsage-audio"
MAN = ROOT / "data" / "sport" / "fr.audio.json"

VOICES = [  # (nom, réglages audio) — la 1re qui marche sert pour toute la séance
    ("fr-FR-Chirp3-HD-Puck", {"audioEncoding": "MP3", "speakingRate": 0.95}),
    ("fr-FR-Chirp3-HD-Puck", {"audioEncoding": "MP3"}),
    ("fr-FR-Neural2-B", {"audioEncoding": "MP3", "speakingRate": 0.95, "pitch": 2.0}),
]


def tts(text, voice, cfg):
    import requests
    for a in range(4):
        r = requests.post(f"https://texttospeech.googleapis.com/v1/text:synthesize?key={GOOGLE_KEY}",
                          json={"input": {"text": text}, "voice": {"languageCode": "fr-FR", "name": voice},
                                "audioConfig": cfg}, timeout=60)
        if r.status_code == 200:
            return base64.b64decode(r.json()["audioContent"])
        if r.status_code in (429, 500, 502, 503):
            time.sleep(5 * 2 ** a); continue
        return None
    return None


def main():
    texts = json.loads(subprocess.check_output(["node", str(ROOT / "tools" / "sport_texts.js")], text=True))
    man = json.loads(MAN.read_text(encoding="utf-8")) if MAN.exists() else {}
    print(f"{len(texts)} phrases du coach")
    if "--check" in sys.argv:
        print(f"{sum(1 for t in texts if t not in man)} sans MP3"); return
    # choisir la voix (test sur une phrase courte)
    chosen = None
    for v, cfg in VOICES:
        if tts("C'est parti !", v, cfg):
            chosen = (v, cfg); break
        print(f"  voix {v} {cfg.get('speakingRate','')} indisponible, essai suivant")
    if not chosen:
        print("❌ aucune voix Google disponible"); sys.exit(2)
    v, cfg = chosen
    vid = v + ":" + json.dumps(cfg, sort_keys=True)
    fp = lambda t: hashlib.sha1(f"{t}|{vid}".encode()).hexdigest()[:12]
    todo = [t for t in texts if man.get(t) != fp(t)]
    print(f"voix : {v} {cfg} — {len(todo)} MP3 à générer ({sum(map(len, todo))} caractères)")
    if todo:
        import boto3
        from botocore.config import Config
        s3 = boto3.client("s3", endpoint_url=R2_ENDPOINT, aws_access_key_id=R2_ACCESS, aws_secret_access_key=R2_SECRET,
                          config=Config(region_name="auto", retries={"max_attempts": 3, "mode": "adaptive"}))
        tmp = Path(tempfile.mkdtemp()); err = 0
        for t in todo:
            data = tts(t, v, cfg)
            if not data:
                err += 1; print("  ✗", t[:60]); continue
            h = fp(t); f = tmp / f"{h}.mp3"; f.write_bytes(data)
            try:
                s3.upload_file(str(f), R2_BUCKET, f"audio/sport/fr/{h}.mp3",
                               ExtraArgs={"ContentType": "audio/mpeg", "CacheControl": "public, max-age=31536000, immutable"})
                man[t] = h
            except Exception as e:
                err += 1; print("  ✗ R2", e)
            time.sleep(0.15)
    man = {t: man[t] for t in texts if t in man}
    MAN.parent.mkdir(parents=True, exist_ok=True)
    MAN.write_text(json.dumps(man, ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    print(f"→ {len(man)}/{len(texts)} phrases ont leur MP3")


if __name__ == "__main__":
    main()
