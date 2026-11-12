#!/usr/bin/env python3
"""
PocketSage — Politesse & Savoir-vivre : traductions + MP3 automatiques
======================================================================
Source unique : data/politesse/fr.json  (on ajoute/modifie le contenu ICI, en français)
1. Empreinte (h) de chaque élément FR.
2. Traduit les éléments nouveaux/modifiés vers EN, DE, ES, IT, PT, AR, ZH, RU, UK → data/politesse/{lang}.json
3. Génère les MP3 manquants → R2 audio/politesse/{lang}/{id}.mp3
   Voix : FR = ElevenLabs Olivier, EN = ElevenLabs Mr Claus, autres langues = Google TTS (mêmes voix que Flash).
4. data/politesse/audio_manifest.json : {"POL-M-001_FR": "h", …} utilisé par l'appli.
Lancé par .github/workflows/politesse-tts.yml à chaque modification de data/politesse/fr.json.
Manuel : python3 gen_politesse.py [--dry-run] [--langs FR,EN]
"""
import hashlib, json, sys, tempfile, time
from pathlib import Path
import generate_flash_tts as F          # traduction Google, voix Google, R2, utilitaires
import gen_sport_mp3 as S               # voix ElevenLabs (réglages énergiques, débit 0,95)

ROOT = Path(__file__).resolve().parent
DIR = ROOT / "data" / "politesse"
SRC = DIR / "fr.json"
MAN = DIR / "audio_manifest.json"
EL_VOICES = {"FR": "GFj5Qf6cNQ3Lgp8VKBwc", "EN": "uDsPstFWFBUXjIBimV7s"}  # Olivier, Mr Claus
LANGS = list(F.VOICE_CONFIG)  # FR + 9 langues
TEXT = ["titre", "texte"]
COPY = ["id", "tab", "a", "icon"]


def h_of(it):
    return hashlib.sha1(json.dumps({k: it.get(k, "") for k in TEXT}, ensure_ascii=False, sort_keys=True).encode()).hexdigest()[:8]


def speech(it):
    parts = [it.get("titre", ""), it.get("texte", "")]
    return " ".join(p.strip().rstrip(".") + "." for p in parts if p and p.strip())


def translate(items, lang):
    slots, texts = [], []
    for i, it in enumerate(items):
        for k in TEXT:
            if it.get(k):
                slots.append((i, k)); texts.append(it[k])
    tr = F.translate_batch(texts, lang) if texts else []
    out = [{**{k: it[k] for k in COPY if k in it}, "h": it["h"]} for it in items]
    for (i, k), v in zip(slots, tr):
        out[i][k] = v
    return out


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--langs", default=",".join(LANGS))
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    langs = [l for l in a.langs.upper().split(",") if l in F.VOICE_CONFIG]
    src = F.load_json(SRC, None)
    items = src["items"]
    ids = [it["id"] for it in items]
    if len(ids) != len(set(ids)):
        sys.exit("❌ id en double dans data/politesse/fr.json")
    ch = 0
    for it in items:
        h = h_of(it)
        if it.get("h") != h:
            it["h"] = h; ch += 1
    print(f"Politesse : {len(items)} éléments, {ch} empreinte(s) mise(s) à jour")
    if ch and not a.dry_run:
        F.save_json(SRC, src)
    by_id = {it["id"]: it for it in items}

    failed = []
    for lang in langs:
        if lang == "FR":
            continue
        p = DIR / f"{lang.lower()}.json"
        old = {x["id"]: x for x in F.load_json(p, {"items": []}).get("items", [])}
        todo = [it for it in items if old.get(it["id"], {}).get("h") != it["h"]]
        gone = [i for i in old if i not in by_id]
        print(f"  {lang} : {len(todo)} à traduire, {len(gone)} supprimé(s)")
        if a.dry_run or (not todo and not gone):
            continue
        try:
            new = {x["id"]: x for x in translate(todo, lang)} if todo else {}
        except Exception as e:
            print(f"  ❌ {lang} : {e}"); failed.append(lang); continue
        F.save_json(p, {"version": 1, "lang": lang, "items": [new.get(i) or old[i] for i in ids]})

    man = F.load_json(MAN, {})
    s3 = None if a.dry_run else F.r2_client()
    tmp = Path(tempfile.mkdtemp()); ok = err = 0
    for lang in langs:
        lst = items if lang == "FR" else F.load_json(DIR / f"{lang.lower()}.json", {"items": []})["items"]
        todo = [x for x in lst if x.get("h") and man.get(f"{x['id']}_{lang}") != x["h"]]
        print(f"  MP3 {lang} : {len(todo)} à générer ({'ElevenLabs' if lang in EL_VOICES else 'Google'})")
        if a.dry_run:
            continue
        for x in todo:
            fid = f"{x['id']}_{lang}"; out = tmp / lang.lower() / f"{x['id']}.mp3"
            out.parent.mkdir(parents=True, exist_ok=True)
            if lang in EL_VOICES:
                data = S.el_tts(speech(x), EL_VOICES[lang])
                good = bool(data)
                if good: out.write_bytes(data)
            else:
                good = F.gen_tts(speech(x), lang, out)
            if not good:
                err += 1; continue
            try:
                s3.upload_file(str(out), F.R2_BUCKET, f"audio/politesse/{lang.lower()}/{x['id']}.mp3",
                               ExtraArgs={"ContentType": "audio/mpeg", "CacheControl": "public, max-age=31536000"})
            except Exception as e:
                print("    ✗ R2", fid, e); err += 1; continue
            man[fid] = x["h"]; ok += 1
            if ok % 25 == 0: F.save_json(MAN, man)
            time.sleep(0.1)
        F.save_json(MAN, man)
    print(f"Terminé : {ok} MP3, {err} erreur(s)")
    if err or failed:
        sys.exit(2)


if __name__ == "__main__":
    main()
