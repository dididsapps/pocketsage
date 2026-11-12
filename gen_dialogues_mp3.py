#!/usr/bin/env python3
"""
PocketSage — Dialogues avec Sensei : vérification + MP3 (voix de Sensei)
=======================================================================
Source : data/dialogues/{lang}.json  (scénarios en arbre, répliques pré-écrites)

1. Vérifie chaque scénario (nœuds existants, sorties, aide présente…) → échec si erreur.
2. Rassemble TOUTES les répliques de Sensei (questions, variantes, réactions, relances, aides, fillers).
3. Génère uniquement les MP3 nouveaux (nom = empreinte du texte + voix) → R2 audio/dialogues/{lang}/{hash}.mp3
4. Écrit data/dialogues/{lang}.audio.json  →  {"texte exact": "hash"} utilisé par l'app.

Lancé par .github/workflows/dialogues-tts.yml à chaque modification de data/dialogues/*.json.
Manuel : python3 gen_dialogues_mp3.py [--check] (vérification seule, sans clé)
"""
import base64, hashlib, json, os, sys, tempfile, time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
_env = ROOT / ".env"
if _env.exists():
    for _l in _env.read_text(encoding="utf-8").splitlines():
        if "=" in _l and not _l.strip().startswith("#"):
            _k, _v = _l.split("=", 1)
            os.environ.setdefault(_k.strip(), _v.strip().strip('"').strip("'"))

EL_KEY     = os.environ.get("ELEVENLABS_API_KEY", "").strip()
GOOGLE_KEY = os.environ.get("GOOGLE_TTS_API_KEY", "").strip()
R2_ACCESS  = os.environ.get("R2_ACCESS_KEY", "").strip()
R2_SECRET  = os.environ.get("R2_SECRET_KEY", "").strip()
R2_ENDPOINT = os.environ.get("R2_ENDPOINT", "https://8ea67fd06083effd6f76efdefb92092f.r2.cloudflarestorage.com")
R2_BUCKET  = "pocketsage-audio"
DLG_DIR    = ROOT / "data" / "dialogues"

# Voix de Sensei par langue (même voix pour tout le scénario = un vrai personnage)
SENSEI_EL  = {"EN": "uDsPstFWFBUXjIBimV7s", "DE": "CP1kYQLB8eBoe8TavZvQ"}
SENSEI_G   = {"EN": ("en-GB", "en-GB-Neural2-B"), "ES": ("es-ES", "es-ES-Neural2-B"), "DE": ("de-DE", "de-DE-Neural2-B")}


def check(d):
    errs = []
    for sc in d["scenarios"]:
        nodes = sc["nodes"]; sid = sc["id"]
        if sc["start"] not in nodes: errs.append(f"{sid}: start inconnu")
        for nid, n in nodes.items():
            if not n.get("say"): errs.append(f"{sid}/{nid}: 'say' vide")
            outs = [i for i in n.get("intents", [])] + ([n["any"]] if n.get("any") else [])
            if not outs and not n.get("next") and not n.get("end"):
                errs.append(f"{sid}/{nid}: aucune sortie")
            for o in outs:
                if not o.get("end") and o.get("next") not in nodes:
                    errs.append(f"{sid}/{nid}: next '{o.get('next')}' inexistant")
                if not o.get("reply"): errs.append(f"{sid}/{nid}: réaction vide")
            for it in n.get("intents", []):
                if not it.get("keys"): errs.append(f"{sid}/{nid}: intent sans mots-clés")
            if outs and not n.get("help"): errs.append(f"{sid}/{nid}: pas de phrase d'aide")
            if outs and not n.get("fr"): errs.append(f"{sid}/{nid}: pas de traduction FR")
    return errs


def lines(d):
    """Toutes les répliques de Sensei → {texte: True si niveau Débutant (voix ElevenLabs)}.
    Règle (12/11/2026) : niveau Débutant = ElevenLabs (plus vivant pour les petits) ; autres niveaux = Google TTS.
    Les phrases communes (relances, fillers) sont aussi entendues par les débutants → ElevenLabs."""
    out = {}
    def add(t, beg):
        if t and t.strip(): out[t] = out.get(t, False) or beg
    for t in d.get("fillers", []): add(t, True)
    g = d.get("global", {})
    for k in ("retry", "silence", "move_on", "dontknow"):
        for t in g.get(k, []): add(t, True)
    for sc in d["scenarios"]:
        beg = sc.get("niveau", "debutant") == "debutant"
        for n in sc["nodes"].values():
            for t in n.get("say", []): add(t, beg)
            add(n.get("help"), beg)
            for o in n.get("intents", []) + ([n["any"]] if n.get("any") else []):
                for t in o.get("reply", []): add(t, beg)
    return out


def voice(lang, beginner=True):
    if beginner and lang in SENSEI_EL:
        return ("el", SENSEI_EL[lang])
    return ("google", SENSEI_G[lang][1])


def fp(text, lang, beginner=True):
    v = voice(lang, beginner)
    return hashlib.sha1(f"{text}|{v[0]}:{v[1]}".encode()).hexdigest()[:12]


def tts(text, lang, out, beginner=True):
    import requests
    kind, vid = voice(lang, beginner)
    for a in range(4):
        if kind == "el":
            r = requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{vid}",
                              headers={"xi-api-key": EL_KEY, "Content-Type": "application/json"},
                              json={"text": text, "model_id": "eleven_multilingual_v2",
                                    "voice_settings": {"stability": 0.5, "similarity_boost": 0.8, "style": 0.25, "use_speaker_boost": True}},
                              timeout=60)
            if r.status_code == 200: out.write_bytes(r.content); return True
        else:
            code, name = SENSEI_G[lang]
            r = requests.post(f"https://texttospeech.googleapis.com/v1/text:synthesize?key={GOOGLE_KEY}",
                              json={"input": {"text": text}, "voice": {"languageCode": code, "name": name},
                                    "audioConfig": {"audioEncoding": "MP3", "speakingRate": 0.9}}, timeout=60)
            if r.status_code == 200: out.write_bytes(base64.b64decode(r.json()["audioContent"])); return True
        if r.status_code in (429, 500, 502, 503): time.sleep(5 * 2 ** a); continue
        print(f"    ✗ {kind} {r.status_code}: {r.text[:120]}"); return False
    return False


def main():
    only_check = "--check" in sys.argv
    files = sorted(p for p in DLG_DIR.glob("*.json") if not p.name.endswith(".audio.json"))
    total_err = 0
    for f in files:
        d = json.loads(f.read_text(encoding="utf-8"))
        lang = d["lang"]
        errs = check(d)
        if errs:
            print(f"❌ {f.name} :"); [print("   -", e) for e in errs]; sys.exit(1)
        L = lines(d)
        amap_path = DLG_DIR / f"{lang.lower()}.audio.json"
        amap = json.loads(amap_path.read_text(encoding="utf-8")) if amap_path.exists() else {}
        todo = [t for t in L if amap.get(t) != fp(t, lang, L[t])]
        print(f"{f.name} : {len(d['scenarios'])} scénarios, {len(L)} répliques, {len(todo)} MP3 à générer "
              f"({sum(len(t) for t in todo)} caractères)")
        if only_check or not todo:
            amap = {t: amap[t] for t in L if t in amap}
            if not only_check: amap_path.write_text(json.dumps(amap, ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8")
            continue
        import boto3
        from botocore.config import Config
        s3 = boto3.client("s3", endpoint_url=R2_ENDPOINT, aws_access_key_id=R2_ACCESS, aws_secret_access_key=R2_SECRET,
                          config=Config(region_name="auto", retries={"max_attempts": 3, "mode": "adaptive"}))
        tmp = Path(tempfile.mkdtemp())
        for i, t in enumerate(todo, 1):
            h = fp(t, lang, L[t]); out = tmp / f"{h}.mp3"
            if tts(t, lang, out, L[t]):
                try:
                    s3.upload_file(str(out), R2_BUCKET, f"audio/dialogues/{lang.lower()}/{h}.mp3",
                                   ExtraArgs={"ContentType": "audio/mpeg", "CacheControl": "public, max-age=31536000, immutable"})
                    amap[t] = h
                except Exception as e:
                    print(f"    ✗ R2 : {e}"); total_err += 1
            else:
                total_err += 1
            time.sleep(0.2)
        amap = {t: amap[t] for t in L if t in amap}
        amap_path.write_text(json.dumps(amap, ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8")
        print(f"  → {len(amap)}/{len(L)} répliques ont leur MP3")
    if total_err: sys.exit(2)


if __name__ == "__main__":
    main()
