#!/usr/bin/env python3
"""
PocketSage — Flash Savant : traductions + MP3 + upload R2 (automatique)
======================================================================
Source unique : data/flash/fr.json  (on n'édite QUE ce fichier)

Pour chaque carte, une empreinte `h` est calculée sur le texte FR
(titre, texte, action, rappel). Seules les cartes NOUVELLES ou MODIFIÉES
sont retraduites et revocalisées :

  data/flash/fr.json            ← champ `h` ajouté/mis à jour
  data/flash/{lang}.json        ← cartes traduites (en, de, es, it, pt, ar, zh, ru, uk)
  data/flash/audio_manifest.json← {"CU-001_FR": "<h>", ...} MP3 déjà publiés
  R2 audio/flash/{lang}/{ID}_{LANG}.mp3  (l'app ajoute ?v=<h> pour vider le cache)

Lancé automatiquement par .github/workflows/flash-tts.yml à chaque push
qui modifie data/flash/fr.json. Lancement manuel possible :

  python3 generate_flash_tts.py                 # tout ce qui a changé
  python3 generate_flash_tts.py --langs FR,EN   # sous-ensemble
  python3 generate_flash_tts.py --dry-run       # affiche ce qui changerait, sans appel API
  python3 generate_flash_tts.py --no-upload     # génère sans envoyer sur R2
  python3 generate_flash_tts.py --no-audio      # traductions seulement

Clés : variables d'environnement (ou fichier .env non commité)
  GOOGLE_TTS_API_KEY   (TTS + Translation)   GOOGLE_TRANSLATE_KEY (optionnel)
  R2_ACCESS_KEY, R2_SECRET_KEY, R2_ENDPOINT (optionnel)
"""

import base64, hashlib, json, os, sys, time, tempfile
from pathlib import Path

ROOT      = Path(__file__).parent
FLASH_DIR = ROOT / "data" / "flash"
SRC       = FLASH_DIR / "fr.json"
AUDIO_MAN = FLASH_DIR / "audio_manifest.json"
AUDIO_DIR = ROOT / "audio" / "flash"          # copie locale (ignorée par git)

# ─── .env optionnel ──────────────────────────────────────────────────────────
_env = ROOT / ".env"
if _env.exists():
    for line in _env.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

GOOGLE_KEY    = os.environ.get("GOOGLE_TTS_API_KEY", "")
TRANSLATE_KEY = os.environ.get("GOOGLE_TRANSLATE_KEY", GOOGLE_KEY)
R2_BUCKET     = os.environ.get("R2_BUCKET", "pocketsage-audio")
R2_ENDPOINT   = os.environ.get("R2_ENDPOINT", "https://8ea67fd06083effd6f76efdefb92092f.r2.cloudflarestorage.com")
R2_ACCESS     = os.environ.get("R2_ACCESS_KEY", "")
R2_SECRET     = os.environ.get("R2_SECRET_KEY", "")

# ─── Langues ─────────────────────────────────────────────────────────────────
VOICE_CONFIG = {
    "FR": {"languageCode": "fr-FR",  "name": "fr-FR-Neural2-A"},
    "EN": {"languageCode": "en-GB",  "name": "en-GB-Neural2-B"},
    "DE": {"languageCode": "de-DE",  "name": "de-DE-Neural2-B"},
    "ES": {"languageCode": "es-ES",  "name": "es-ES-Neural2-B"},
    "IT": {"languageCode": "it-IT",  "name": "it-IT-Neural2-C"},
    "PT": {"languageCode": "pt-BR",  "name": "pt-BR-Neural2-B"},
    "AR": {"languageCode": "ar-XA",  "name": "ar-XA-Wavenet-B"},
    "ZH": {"languageCode": "cmn-CN", "name": "cmn-CN-Wavenet-B"},
    "RU": {"languageCode": "ru-RU",  "name": "ru-RU-Wavenet-B"},
    "UK": {"languageCode": "uk-UA",  "name": "uk-UA-Wavenet-A"},
}
TRANSLATE_CODES = {"EN": "en", "DE": "de", "ES": "es", "IT": "it", "PT": "pt",
                   "AR": "ar", "ZH": "zh-CN", "RU": "ru", "UK": "uk"}
LANGS_DEFAULT = list(VOICE_CONFIG)

# Champs copiés tels quels / champs traduits
COPY_FIELDS = ["id", "cat", "emoji", "age", "couleur", "source"]
TEXT_FIELDS = ["titre", "texte", "tag", "action"]


# ─── Utilitaires ─────────────────────────────────────────────────────────────
def load_json(p: Path, default):
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else default

def save_json(p: Path, data) -> None:
    p.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

def card_hash(c: dict) -> str:
    """Empreinte du contenu traduisible/vocalisé de la carte FR."""
    payload = {k: c.get(k, "") for k in TEXT_FIELDS}
    payload["rappel"] = c.get("rappel") or {}
    raw = json.dumps(payload, ensure_ascii=False, sort_keys=True)
    return hashlib.sha1(raw.encode("utf-8")).hexdigest()[:8]

def speech_text(c: dict) -> str:
    parts = [c.get("titre", ""), c.get("texte", ""), c.get("action", "")]
    return " ".join(p.strip().rstrip(".") + "." for p in parts if p and p.strip())

def validate(cards: list) -> list:
    errs, seen = [], set()
    for i, c in enumerate(cards):
        cid = c.get("id")
        if not cid:
            errs.append(f"carte n°{i} : pas d'id"); continue
        if cid in seen: errs.append(f"{cid} : id en double")
        seen.add(cid)
        for k in ("cat", "titre", "texte"):
            if not c.get(k): errs.append(f"{cid} : champ '{k}' manquant")
        r = c.get("rappel")
        if r is not None:
            ch = r.get("choix", [])
            if not r.get("q") or len(ch) < 2 or not (0 <= r.get("ok", -1) < len(ch)):
                errs.append(f"{cid} : rappel invalide (q, choix ≥2, ok)")
    return errs


# ─── Google Translate ────────────────────────────────────────────────────────
def translate_batch(texts: list, lang: str) -> list:
    import requests
    url = f"https://translation.googleapis.com/language/translate/v2?key={TRANSLATE_KEY}"
    out = []
    for i in range(0, len(texts), 100):
        batch = texts[i:i + 100]
        for attempt in range(6):  # erreurs temporaires Google (429/5xx) : on réessaie
            try:
                r = requests.post(url, json={"q": batch, "source": "fr",
                                             "target": TRANSLATE_CODES[lang], "format": "text"}, timeout=60)
            except requests.RequestException as e:
                r = None; err = str(e)
            if r is not None and r.status_code == 200:
                break
            code = r.status_code if r is not None else "réseau"
            if r is not None and code not in (429, 500, 502, 503, 504):
                raise RuntimeError(f"Translate {lang} HTTP {code}: {r.text[:200]}")
            wait = 5 * 2 ** attempt
            print(f"    ⏳ Translate {lang} {code}, nouvel essai dans {wait}s")
            time.sleep(wait)
        else:
            raise RuntimeError(f"Translate {lang} : échec après 6 essais")
        out.extend(t["translatedText"] for t in r.json()["data"]["translations"])
        time.sleep(0.1)
    return out

def translate_cards(cards: list, lang: str, translator=translate_batch) -> list:
    """Traduit les champs texte + rappel d'une liste de cartes FR (un seul lot d'appels)."""
    slots, texts = [], []
    for ci, c in enumerate(cards):
        for k in TEXT_FIELDS:
            if c.get(k):
                slots.append((ci, k, None)); texts.append(c[k])
        r = c.get("rappel")
        if r:
            slots.append((ci, "rappel.q", None)); texts.append(r["q"])
            for j, ch in enumerate(r["choix"]):
                slots.append((ci, "rappel.choix", j)); texts.append(ch)
    tr = translator(texts, lang) if texts else []
    res = []
    for c in cards:
        t = {k: c[k] for k in COPY_FIELDS if k in c}
        t["h"] = c["h"]
        if c.get("rappel"):
            t["rappel"] = {"q": "", "choix": [""] * len(c["rappel"]["choix"]), "ok": c["rappel"]["ok"]}
        res.append(t)
    for (ci, k, j), val in zip(slots, tr):
        if k == "rappel.q": res[ci]["rappel"]["q"] = val
        elif k == "rappel.choix": res[ci]["rappel"]["choix"][j] = val
        else: res[ci][k] = val
    return res


# ─── Google TTS ──────────────────────────────────────────────────────────────
def gen_tts(text: str, lang: str, out_path: Path) -> bool:
    import requests
    cfg = VOICE_CONFIG[lang]
    payload = {"input": {"text": text},
               "voice": {"languageCode": cfg["languageCode"], "name": cfg["name"]},
               "audioConfig": {"audioEncoding": "MP3", "speakingRate": 0.85, "pitch": -2.0}}
    for attempt in range(5):
        try:
            r = requests.post(f"https://texttospeech.googleapis.com/v1/text:synthesize?key={GOOGLE_KEY}",
                              json=payload, timeout=60)
        except requests.RequestException:
            time.sleep(5 * 2 ** attempt); continue
        if r.status_code in (429, 500, 502, 503, 504):
            time.sleep(5 * 2 ** attempt); continue
        break
    else:
        print(f"    ✗ TTS {lang} : échec après 5 essais"); return False
    if r.status_code == 200 and r.json().get("audioContent"):
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_bytes(base64.b64decode(r.json()["audioContent"]))
        return True
    print(f"    ✗ TTS {lang} {r.status_code}: {r.text[:120]}")
    return False

def r2_client():
    import boto3
    from botocore.config import Config
    return boto3.client("s3", endpoint_url=R2_ENDPOINT, aws_access_key_id=R2_ACCESS,
                        aws_secret_access_key=R2_SECRET,
                        config=Config(region_name="auto", retries={"max_attempts": 3, "mode": "adaptive"}))


# ─── MAIN ────────────────────────────────────────────────────────────────────
def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--langs", default=",".join(LANGS_DEFAULT))
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--no-upload", action="store_true")
    ap.add_argument("--no-audio", action="store_true")
    a = ap.parse_args()
    langs = [l.strip().upper() for l in a.langs.split(",") if l.strip().upper() in VOICE_CONFIG]

    src = load_json(SRC, None)
    if not src or "cards" not in src:
        sys.exit(f"❌ {SRC} introuvable ou sans clé 'cards'")
    cards = src["cards"]
    errs = validate(cards)
    if errs:
        print("❌ fr.json invalide :"); [print("   -", e) for e in errs]; sys.exit(1)

    # 1) Empreintes FR
    changed_h = 0
    for c in cards:
        h = card_hash(c)
        if c.get("h") != h:
            c["h"] = h; changed_h += 1
    print(f"Flash : {len(cards)} cartes, {changed_h} empreinte(s) mise(s) à jour")
    if not a.dry_run and changed_h:
        save_json(SRC, src)
    by_id = {c["id"]: c for c in cards}

    need_keys = not a.dry_run
    if need_keys and not GOOGLE_KEY:
        sys.exit("❌ GOOGLE_TTS_API_KEY manquante (variable d'environnement ou .env)")

    # 2) Traductions
    failed_langs = []
    for lang in langs:
        if lang == "FR": continue
        p = FLASH_DIR / f"{lang.lower()}.json"
        old = {c["id"]: c for c in load_json(p, {"cards": []}).get("cards", [])}
        todo = [c for c in cards if old.get(c["id"], {}).get("h") != c["h"]]
        removed = [i for i in old if i not in by_id]
        print(f"  {lang} : {len(todo)} à traduire, {len(removed)} supprimée(s)")
        if a.dry_run or (not todo and not removed): continue
        try:
            new = {t["id"]: t for t in translate_cards(todo, lang)} if todo else {}
        except Exception as e:
            print(f"  ❌ {lang} : {e} — langue ignorée, sera reprise au prochain lancement")
            failed_langs.append(lang); continue
        merged = [new.get(c["id"]) or old[c["id"]] for c in cards]
        save_json(p, {"version": 1, "lang": lang, "cards": merged})

    if a.no_audio:
        print("Audio ignoré (--no-audio)"); return

    # 3) MP3 + upload
    man = load_json(AUDIO_MAN, {})
    s3 = None
    if not a.dry_run and not a.no_upload:
        if not (R2_ACCESS and R2_SECRET):
            sys.exit("❌ R2_ACCESS_KEY / R2_SECRET_KEY manquantes (ou utiliser --no-upload)")
        s3 = r2_client()
    tmp = Path(tempfile.mkdtemp())
    total_ok = total_err = 0
    for lang in langs:
        lang_cards = cards if lang == "FR" else load_json(FLASH_DIR / f"{lang.lower()}.json", {"cards": []})["cards"]
        todo = [c for c in lang_cards if c.get("h") and man.get(f"{c['id']}_{lang}") != c["h"]]
        print(f"  MP3 {lang} : {len(todo)} à générer")
        if a.dry_run: continue
        for c in todo:
            fid = f"{c['id']}_{lang}"
            out = (AUDIO_DIR if a.no_upload else tmp) / lang.lower() / f"{fid}.mp3"
            if not gen_tts(speech_text(c), lang, out):
                total_err += 1; continue
            if s3:
                try:
                    s3.upload_file(str(out), R2_BUCKET, f"audio/flash/{lang.lower()}/{fid}.mp3",
                                   ExtraArgs={"ContentType": "audio/mpeg", "CacheControl": "public, max-age=31536000"})
                except Exception as e:
                    print(f"    ✗ R2 {fid}: {e}"); total_err += 1; continue
            man[fid] = c["h"]; total_ok += 1
            if total_ok % 25 == 0: save_json(AUDIO_MAN, man)
            time.sleep(0.1)
        save_json(AUDIO_MAN, man)
    print(f"Terminé : {total_ok} MP3 publiés, {total_err} erreur(s)")
    if failed_langs: print(f"Langues à reprendre : {', '.join(failed_langs)}")
    if total_err or failed_langs: sys.exit(2)


if __name__ == "__main__":
    main()
