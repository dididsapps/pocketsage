#!/usr/bin/env python3
"""
PocketSage TTS Generator — ElevenLabs
Génère les MP3 pour toutes les questions GS+CP+CE1
Usage: python3 generate_tts.py
"""

import re, json, os, time, hashlib
from pathlib import Path

# ══════════════════════════════════════════
# CONFIGURATION — modifie ces valeurs
# ══════════════════════════════════════════
API_KEY = "sk_f30727c3dcfbab65149ebe22296dad06a81aa89c8ad2fd93"
VOICE_ID_FR = "GFj5Qf6cNQ3Lgp8VKBwc"   # Olivier (FR)
VOICE_ID_EN = "9mF01VTvwaxuBPjm0hMu"   # Charlie Horse (EN)
OUTPUT_DIR = Path("audio/fr")
MANIFEST_FILE = Path("audio/manifest.json")
INDEX_HTML = Path("index.html")
# ══════════════════════════════════════════

try:
    import requests
except ImportError:
    print("Installation de requests...")
    os.system("pip3 install requests -q")
    import requests

def get_voices():
    """Liste toutes les voix disponibles"""
    r = requests.get(
        "https://api.elevenlabs.io/v1/voices",
        headers={"xi-api-key": API_KEY}
    )
    r.raise_for_status()
    return r.json()["voices"]

def find_voice(voices, name):
    """Cherche une voix par nom"""
    for v in voices:
        if name.lower() in v["name"].lower():
            return v
    return None

def text_to_speech(text, voice_id, output_path):
    """Génère un MP3 via ElevenLabs"""
    r = requests.post(
        f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
        headers={
            "xi-api-key": API_KEY,
            "Content-Type": "application/json"
        },
        json={
            "text": text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.75,
                "style": 0.3,
                "use_speaker_boost": True
            }
        }
    )
    if r.status_code == 200:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_bytes(r.content)
        return True
    else:
        print(f"  ERREUR {r.status_code}: {r.text[:100]}")
        return False

def extract_questions(html_path, classes=("GS", "CP", "CE1")):
    """Extrait les questions des classes ciblées"""
    content = html_path.read_text(encoding="utf-8")
    pattern = r'\{id:"([^"]+)",classe:"([^"]+)",cat:"[^"]*",enonce:"([^"]*)",rep:"([^"]*)",choix:\[([^\]]+)\]'
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
            "choix": choix_list
        })
    return result

def main():
    print("═" * 55)
    print("  PocketSage TTS Generator — ElevenLabs")
    print("═" * 55)

    # Vérifier la clé API
    print("\n1. Vérification de la clé API...")
    try:
        voices = get_voices()
        print(f"   ✅ Connecté — {len(voices)} voix disponibles")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return

    # Trouver la voix Algieba
    print("\n2. Recherche de la voix Algieba...")
    algieba = find_voice(voices, "algieba")
    if algieba:
        print(f"   ✅ Algieba trouvée: {algieba['voice_id']}")
        voice_id = algieba["voice_id"]
    elif VOICE_ID_FR:
        print(f"   ℹ️  Utilisation de l'ID fourni: {VOICE_ID_FR}")
        voice_id = VOICE_ID_FR
    else:
        print("\n   Voix disponibles:")
        for v in voices[:20]:
            print(f"   - {v['name']:30} | {v['voice_id']}")
        print("\n   ❌ Algieba non trouvée. Copie l'ID voulu ci-dessus dans VOICE_ID_FR")
        return

    # Extraire les questions
    print("\n3. Extraction des questions GS+CP+CE1...")
    questions = extract_questions(INDEX_HTML)
    print(f"   ✅ {len(questions)} questions trouvées")

    # Charger le manifest existant
    if MANIFEST_FILE.exists():
        manifest = json.loads(MANIFEST_FILE.read_text(encoding="utf-8"))
    else:
        manifest = {}

    # Construire la liste à générer
    todo = []
    for q in questions:
        # Énoncé
        fid = f"{q['id']}_enonce"
        if fid not in manifest:
            todo.append({"id": fid, "text": q["enonce"], "file": f"{q['id']}_enonce.mp3"})
        # Choix
        for i, c in enumerate(q["choix"]):
            fid = f"{q['id']}_choix_{i}"
            if fid not in manifest:
                todo.append({"id": fid, "text": c, "file": f"{q['id']}_choix_{i}.mp3"})

    total_chars = sum(len(t["text"]) for t in todo)
    print(f"\n4. À générer: {len(todo)} fichiers ({total_chars:,} caractères)")
    print(f"   Déjà générés: {len(manifest)} fichiers")

    if not todo:
        print("   ✅ Tout est déjà généré !")
        return

    # Confirmer
    print(f"\n   Crédits estimés utilisés: ~{total_chars:,}")
    answer = input("   Continuer ? (o/n) : ").strip().lower()
    if answer not in ("o", "oui", "y", "yes"):
        print("   Annulé.")
        return

    # Générer
    print(f"\n5. Génération en cours...")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    ok = 0
    errors = 0

    for i, item in enumerate(todo):
        out = OUTPUT_DIR / item["file"]
        print(f"   [{i+1:4}/{len(todo)}] {item['id'][:50]:<50}", end=" ", flush=True)

        success = text_to_speech(item["text"], voice_id, out)
        if success:
            manifest[item["id"]] = item["file"]
            print("✅")
            ok += 1
        else:
            print("❌")
            errors += 1

        # Sauvegarder le manifest toutes les 10 générations
        if (i + 1) % 10 == 0:
            MANIFEST_FILE.parent.mkdir(parents=True, exist_ok=True)
            MANIFEST_FILE.write_text(json.dumps(manifest, ensure_ascii=False, indent=2))

        # Pause pour éviter le rate limiting
        time.sleep(0.3)

    # Sauvegarder le manifest final
    MANIFEST_FILE.write_text(json.dumps(manifest, ensure_ascii=False, indent=2))

    print(f"\n═" * 55)
    print(f"  ✅ {ok} fichiers générés")
    if errors:
        print(f"  ❌ {errors} erreurs")
    print(f"  📁 Fichiers dans: {OUTPUT_DIR}/")
    print(f"  📋 Manifest: {MANIFEST_FILE}")
    print(f"\n  Prochaine étape: git add audio/ && git push")
    print("═" * 55)

if __name__ == "__main__":
    main()
