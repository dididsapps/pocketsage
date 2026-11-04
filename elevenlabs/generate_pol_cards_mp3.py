#!/usr/bin/env python3
"""
Génère les MP3 ElevenLabs pour les cartes Politesse (Manières/Dictons/Conseils).
FR : voix Olivier | EN : voix Charlie Horse
IDs : POC-M-001 (manières), POC-D-001 (dictons), POC-CS-001 (conseils)
"""

import os, requests, time

ELEVEN_API_KEY = open(os.path.join(os.path.dirname(__file__), "eleven_api_key.txt")).read().strip()
VOICE_FR = "GFj5Qf6cNQ3Lgp8VKBwc"   # Olivier
VOICE_EN = "9mF01VTvwaxuBPjm0hMu"   # Charlie Horse
MODEL    = "eleven_multilingual_v2"

BASE = os.path.join(os.path.dirname(__file__), "..")
OUT_FR = os.path.join(BASE, "audio", "fr")
OUT_EN = os.path.join(BASE, "audio", "en")
os.makedirs(OUT_FR, exist_ok=True)
os.makedirs(OUT_EN, exist_ok=True)

# ── Données extraites de POLITESSE_DATA ──────────────────────────────────────

MANIERES = [
    ("POC-M-001", "À table : Attends que tout le monde soit servi avant de commencer. Dis toujours s'il te plaît et merci.",
                  "At the table: Wait until everyone is served before you start eating. Always say please and thank you."),
    ("POC-M-002", "Saluer : Regarde la personne dans les yeux quand tu la salues. Un sourire sincère vaut mille mots.",
                  "Greeting: Look the person in the eyes when you greet them. A sincere smile is worth a thousand words."),
    ("POC-M-003", "Écouter : N'interromps pas quand quelqu'un parle. Écouter vraiment, c'est offrir un cadeau.",
                  "Listening: Don't interrupt when someone is speaking. Truly listening is a gift."),
    ("POC-M-004", "Téléphone : Range ton téléphone lors des repas et conversations. Ta présence est ton plus beau cadeau.",
                  "Phone: Put your phone away during meals and conversations. Your presence is your greatest gift."),
    ("POC-M-005", "Remercier : Un merci sincère et spontané crée un lien fort. N'attends pas qu'on te le rappelle.",
                  "Thanking: A sincere and spontaneous thank-you creates a strong bond. Don't wait to be reminded."),
    ("POC-M-006", "S'excuser : S'excuser sincèrement demande du courage. Je suis désolé dit avec le cœur répare beaucoup.",
                  "Apologizing: Apologizing sincerely takes courage. 'I'm sorry' said from the heart can repair a lot."),
]

DICTONS = [
    ("POC-D-001", "La politesse est l'art de choisir parmi ses pensées. — Germaine de Staël",
                  "Politeness is the art of choosing among one's thoughts. — Germaine de Staël"),
    ("POC-D-002", "Le secret du succès, c'est la constance dans le but. — Benjamin Disraeli",
                  "The secret of success is constancy of purpose. — Benjamin Disraeli"),
    ("POC-D-003", "Peu importe la vitesse à laquelle tu avances, l'important est de ne pas s'arrêter. — Confucius",
                  "It does not matter how slowly you go as long as you do not stop. — Confucius"),
    ("POC-D-004", "Traite les autres comme tu aimerais être traité. — Règle d'or universelle",
                  "Treat others as you would like to be treated. — The Golden Rule"),
    ("POC-D-005", "Le respect de soi est le commencement de la sagesse. — Proverbe écossais",
                  "Self-respect is the beginning of wisdom. — Scottish Proverb"),
    ("POC-D-006", "Un sourire ne coûte rien et vaut pourtant beaucoup. — Proverbe français",
                  "A smile costs nothing and is worth a great deal. — French Proverb"),
    ("POC-D-007", "Les grandes choses ne se font pas par impulsion, mais par une série de petites choses. — Van Gogh",
                  "Great things are not done by impulse, but by a series of small things brought together. — Van Gogh"),
    ("POC-D-008", "La gratitude transforme ce que nous avons en suffisamment. — Proverbe amérindien",
                  "Gratitude turns what we have into enough. — Native American Proverb"),
]

CONSEILS = [
    ("POC-CS-001", "Fixe un objectif : Écris ton objectif sur papier. Il devient beaucoup plus probable de le réaliser !",
                   "Set a goal: Write your goal on paper. It becomes much more likely to come true!"),
    ("POC-CS-002", "Découpe en petites étapes : Un grand rêve plus petites actions quotidiennes égale résultats certains. Commence par 5 minutes par jour.",
                   "Break it into small steps: A big dream plus small daily actions equals certain results. Start with 5 minutes a day."),
    ("POC-CS-003", "Célèbre tes progrès : Chaque pas compte. Félicite-toi pour les petites victoires — elles construisent la grande.",
                   "Celebrate your progress: Every step counts. Congratulate yourself for small wins — they build the big one."),
    ("POC-CS-004", "Entoure-toi bien : Tu deviens la moyenne des 5 personnes que tu côtoies le plus. Choisis des gens qui t'élèvent.",
                   "Surround yourself well: You become the average of the 5 people you spend the most time with. Choose people who lift you up."),
    ("POC-CS-005", "La persévérance : Tous les experts ont été des débutants. La différence ? Ils n'ont pas abandonné.",
                   "Perseverance: All experts were once beginners. The difference? They didn't give up."),
    ("POC-CS-006", "Sois curieux : Pose des questions, lis, explore. La curiosité est le moteur de tous les grands accomplissements.",
                   "Be curious: Ask questions, read, explore. Curiosity is the engine of all great achievements."),
]

ALL_ITEMS = MANIERES + DICTONS + CONSEILS

def generate(text, voice_id, out_path):
    if os.path.exists(out_path):
        print(f"  ⏭ déjà présent : {os.path.basename(out_path)}")
        return True
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {"xi-api-key": ELEVEN_API_KEY, "Content-Type": "application/json"}
    body = {"text": text, "model_id": MODEL,
            "voice_settings": {"stability": 0.5, "similarity_boost": 0.75}}
    r = requests.post(url, headers=headers, json=body, timeout=30)
    if r.status_code == 200:
        with open(out_path, "wb") as f:
            f.write(r.content)
        print(f"  ✓ {os.path.basename(out_path)} ({len(r.content)//1024}KB)")
        return True
    else:
        print(f"  ✗ {os.path.basename(out_path)} : {r.status_code} {r.text[:100]}")
        return False

print(f"🎙 Génération de {len(ALL_ITEMS)} items × 2 langues = {len(ALL_ITEMS)*2} MP3\n")
ok = 0
for item_id, txt_fr, txt_en in ALL_ITEMS:
    print(f"[{item_id}]")
    if generate(txt_fr, VOICE_FR, os.path.join(OUT_FR, f"{item_id}_enonce.mp3")): ok += 1
    time.sleep(0.3)
    if generate(txt_en, VOICE_EN, os.path.join(OUT_EN, f"{item_id}.mp3")): ok += 1
    time.sleep(0.3)

print(f"\n✅ {ok}/{len(ALL_ITEMS)*2} MP3 générés")
