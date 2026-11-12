#!/usr/bin/env python3
"""
PocketSage — Coach Sportif : MP3 des phrases du coach (voix Google énergique, débit normal)
=========================================================================================
1. `node tools/sport_texts.js` → toutes les phrases (consignes, encouragements, phases, GO/NEXT…)
2. Génère seulement les MP3 nouveaux → R2 audio/sport/fr/{hash}.mp3
3. Écrit data/sport/fr.audio.json  →  {"texte exact": "hash"} (lu par js/coach-voix.js)

Voix (12/11/2026) : ElevenLabs pour le français (Olivier) et l'anglais (Mr Claus) — plus drôle et vivant
pour tous les âges ; Google TTS pour les autres langues. Réglages énergiques, débit 0,95.
Relecture automatique avant génération (js/coach-voix.js → lint) : les phrases à risque (abréviations,
MAJUSCULES, mots anglais, « Dis next »…) ne sont PAS générées et sont listées dans
docs/jeux/sport_textes_a_corriger.md (l'appli utilise alors la voix du téléphone pour elles).
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
EL_KEY = os.environ.get("ELEVENLABS_API_KEY", "").strip()
EL_VOICES = {"FR": "GFj5Qf6cNQ3Lgp8VKBwc", "EN": "uDsPstFWFBUXjIBimV7s"}  # Olivier, Mr Claus
REPORT = ROOT / "docs" / "jeux" / "sport_textes_a_corriger.md"
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


def el_tts(text, vid):
    import requests
    vs = {"stability": 0.4, "similarity_boost": 0.8, "style": 0.45, "use_speaker_boost": True, "speed": 0.95}
    for a in range(5):
        r = requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{vid}",
                          headers={"xi-api-key": EL_KEY, "Content-Type": "application/json"},
                          json={"text": text, "model_id": "eleven_multilingual_v2", "voice_settings": vs}, timeout=60)
        if r.status_code == 200:
            return r.content
        if r.status_code == 422 and "speed" in vs:
            vs.pop("speed"); continue  # réglage de vitesse non accepté : on réessaie sans
        if r.status_code in (429, 500, 502, 503):
            time.sleep(5 * 2 ** a); continue
        print(f"    ✗ ElevenLabs {r.status_code}: {r.text[:150]}")
        return None
    return None


def lint_texts():
    out = subprocess.run(["node", str(ROOT / "tools" / "sport_texts.js"), "--lint"], capture_output=True, text=True)
    bad, cur = {}, None
    for line in out.stderr.splitlines():
        if line.startswith("⚠️"):
            cur = line[2:].strip()
        elif line.strip().startswith("«") and cur:
            bad[line.strip()[1:-1].strip()] = cur
    return bad


def main():
    texts = json.loads(subprocess.check_output(["node", str(ROOT / "tools" / "sport_texts.js")], text=True))
    man = json.loads(MAN.read_text(encoding="utf-8")) if MAN.exists() else {}
    print(f"{len(texts)} phrases du coach")
    if "--check" in sys.argv:
        print(f"{sum(1 for t in texts if t not in man)} sans MP3"); return
    bad = lint_texts()
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("# Phrases du coach à corriger avant génération de la voix\n\n" + (
        "\n".join(f"- {why} : « {t} »" for t, why in sorted(bad.items())) if bad else "✅ Aucune (dernière vérification automatique).") + "\n", encoding="utf-8")
    if bad:
        print(f"⚠️ {len(bad)} phrase(s) à corriger, non générées (voir {REPORT.name})")
    texts_ok = [t for t in texts if t not in bad]
    if not EL_KEY:
        print("❌ ELEVENLABS_API_KEY manquante"); sys.exit(2)
    v, cfg = "eleven:" + EL_VOICES["FR"], {"model": "eleven_multilingual_v2", "style": 0.45, "speed": 0.95}
    print(f"voix : {v} {cfg} — {len(todo)} MP3 à générer ({sum(map(len, todo))} caractères)")
    if todo:
        import boto3
        from botocore.config import Config
        s3 = boto3.client("s3", endpoint_url=R2_ENDPOINT, aws_access_key_id=R2_ACCESS, aws_secret_access_key=R2_SECRET,
                          config=Config(region_name="auto", retries={"max_attempts": 3, "mode": "adaptive"}))
        tmp = Path(tempfile.mkdtemp()); err = 0
        for t in todo:
            data = el_tts(t, EL_VOICES["FR"])
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
