#!/usr/bin/env python3
"""
PocketSage TTS Generator — Google Cloud Text-to-Speech
Génère les MP3 pour les classes CE2 → Lycée + toutes les langues vivantes
Usage: python3 generate_tts_google.py
"""

import re, json, os, time, base64
from pathlib import Path

# ══════════════════════════════════════════
# CONFIGURATION
# ══════════════════════════════════════════
INDEX_HTML    = Path("index.html")
OUTPUT_DIR    = Path("audio/fr")
MANIFEST_FILE = Path("audio/manifest_google.json")

# Classes ciblées par Google TTS
TARGET_CLASSES = ("CE2", "CM1", "CM2", "6ème", "5ème", "4ème", "3ème", "Lycée")

# Voix par langue (Neural2 = meilleure qualité dans le quota gratuit)
VOICE_MAP = {
    "FR": {"languageCode": "fr-FR", "name": "fr-FR-Neural2-D"},   # Algieba
    "EN": {"languageCode": "en-GB", "name": "en-GB-Neural2-B"},   # Achird
    "ES": {"languageCode": "es-ES", "name": "es-ES-Neural2-B"},
    "DE": {"languageCode": "de-DE", "name": "de-DE-Neural2-B"},
    "IT": {"languageCode": "it-IT", "name": "it-IT-Neural2-C"},
    "PT": {"languageCode": "pt-BR", "name": "pt-BR-Neural2-B"},
    "AR": {"languageCode": "ar-XA", "name": "ar-XA-Neural2-B"},
    "ZH": {"languageCode": "cmn-CN", "name": "cmn-CN-Neural2-B"},
}

# Correspondance préfixe module → langue TTS
MODULE_LANG = {
    "AN": "EN", "ES": "ES", "DE": "DE", "IT": "IT",
    "PT": "PT", "AR": "AR", "ZH": "ZH",
    # Tout le reste (LG, MA, SC, GE, HI, FR, CG, DF) → français
}
# ══════════════════════════════════════════

try:
    import requests
except ImportError:
    os.system("pip3 install requests -q --break-system-packages")
    import requests


def detect_lang(question_id: str) -> str:
    """Détermine la langue TTS à partir du préfixe d'ID (ex: AN-CE2-001 → EN)"""
    prefix = question_id.split("-")[0]
    return MODULE_LANG.get(prefix, "FR")


def text_to_speech_google(text: str, lang_code: str, api_key: str, output_path: Path) -> bool:
    """Génère un MP3 via Google Cloud TTS"""
    voice_cfg = VOICE_MAP.get(lang_code, VOICE_MAP["FR"])
    payload = {
        "input": {"text": text},
        "voice": {
            "languageCode": voice_cfg["languageCode"],
            "name": voice_cfg["name"],
        },
        "audioConfig": {
            "audioEncoding": "MP3",
            "speakingRate": 0.9,
            "pitch": 0.0,
        }
    }
    url = f"https://texttospeech.googleapis.com/v1/text:synthesize?key={api_key}"
    try:
        r = requests.post(url, json=payload, timeout=30)
        if r.status_code == 200:
            audio_b64 = r.json().get("audioContent", "")
            if audio_b64:
                output_path.parent.mkdir(parents=True, exist_ok=True)
                output_path.write_bytes(base64.b64decode(audio_b64))
                return True
        print(f"  ERREUR {r.status_code}: {r.text[:120]}")
        return False
    except Exception as e:
        print(f"  EXCEPTION: {e}")
        return False


def extract_questions(html_path: Path, classes: tuple) -> list:
    """Extrait les questions des classes ciblées"""
    content = html_path.read_text(encoding="utf-8")
    pattern = r'\{id:"([^"]+)",classe:"([^"]+)",cat:"[^"]*",(?:type:"[^"]*",)?enonce:"([^"]*)",rep:"([^"]*)",choix:\[([^\]]+)\]'
    items = re.findall(pattern, content)
    result = []
    for qid, classe, enonce, rep, choix_raw in items:
        if classe not in classes:
            continue
        choix_list = re.findall(r'"([^"]*)"', choix_raw)
        result.append({
            "id": qid,
            "classe": classe,
            "enonce": enonce,
            "rep": rep,
            "choix": choix_list,
            "lang": detect_lang(qid),
        })
    return result


def main():
    print("═" * 60)
    print("  PocketSage TTS Generator — Google Cloud")
    print("═" * 60)

    # Clé API
    api_key = os.environ.get("GOOGLE_TTS_API_KEY", "").strip()
    if not api_key:
        api_key = input("\nColle ta clé API Google Cloud TTS : ").strip()
    if not api_key:
        print("❌ Clé API manquante. Abandonne.")
        return

    # Test de la clé
    print("\n1. Test de la clé API...")
    test_url = f"https://texttospeech.googleapis.com/v1/voices?languageCode=fr-FR&key={api_key}"
    r = requests.get(test_url, timeout=10)
    if r.status_code != 200:
        print(f"   ❌ Clé invalide ou API non activée: {r.status_code} {r.text[:100]}")
        return
    print(f"   ✅ Connecté — {len(r.json().get('voices',[]))} voix fr-FR disponibles")

    # Extraire les questions
    print(f"\n2. Extraction des questions {TARGET_CLASSES}...")
    questions = extract_questions(INDEX_HTML, TARGET_CLASSES)
    print(f"   ✅ {len(questions)} questions trouvées")

    # Manifest existant
    if MANIFEST_FILE.exists():
        manifest = json.loads(MANIFEST_FILE.read_text(encoding="utf-8"))
    else:
        manifest = {}

    # Liste à générer
    todo = []
    for q in questions:
        # Énoncé
        fid = f"{q['id']}_enonce"
        if fid not in manifest:
            todo.append({"id": fid, "text": q["enonce"], "lang": q["lang"],
                         "file": f"{q['id']}_enonce.mp3"})
        # Choix (uniquement pour modules langue)
        if q["lang"] != "FR":
            for i, ch in enumerate(q["choix"]):
                fid2 = f"{q['id']}_choix_{i}"
                if fid2 not in manifest:
                    todo.append({"id": fid2, "text": ch, "lang": q["lang"],
                                 "file": f"{q['id']}_choix_{i}.mp3"})

    total_chars = sum(len(t["text"]) for t in todo)
    print(f"\n3. À générer : {len(todo)} fichiers ({total_chars:,} caractères)")
    print(f"   Déjà générés : {len(manifest)} fichiers")
    if total_chars > 0:
        print(f"   Coût estimé : gratuit si < 1M chars/mois (tu en as {total_chars:,})")

    if not todo:
        print("   ✅ Tout est déjà généré !")
        return

    answer = input("\n   Continuer ? (o/n) : ").strip().lower()
    if answer not in ("o", "oui", "y", "yes"):
        print("   Annulé.")
        return

    # Générer
    print(f"\n4. Génération en cours...")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    ok_count = errors = 0

    for i, item in enumerate(todo):
        out = OUTPUT_DIR / item["file"]
        lang_label = item["lang"]
        print(f"   [{i+1:4}/{len(todo)}] [{lang_label}] {item['id'][:45]:<45}", end=" ", flush=True)

        success = text_to_speech_google(item["text"], item["lang"], api_key, out)
        if success:
            manifest[item["id"]] = item["file"]
            print("✅")
            ok_count += 1
        else:
            print("❌")
            errors += 1

        # Sauvegarde manifest toutes les 20 générations
        if (i + 1) % 20 == 0:
            MANIFEST_FILE.parent.mkdir(parents=True, exist_ok=True)
            MANIFEST_FILE.write_text(json.dumps(manifest, ensure_ascii=False, indent=2))

        time.sleep(0.15)  # ~6 req/s, bien en dessous des limites Google

    MANIFEST_FILE.write_text(json.dumps(manifest, ensure_ascii=False, indent=2))

    print(f"\n{'═'*60}")
    print(f"  ✅ {ok_count} fichiers générés")
    if errors:
        print(f"  ❌ {errors} erreurs")
    print(f"  📁 Fichiers dans : {OUTPUT_DIR}/")
    print(f"  📋 Manifest : {MANIFEST_FILE}")
    print(f"\n  Prochaine étape :")
    print(f"  git add audio/ && git commit -m 'Add Google TTS audio' && git push")
    print("═" * 60)


if __name__ == "__main__":
    main()
