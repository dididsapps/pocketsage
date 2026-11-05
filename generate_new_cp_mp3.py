#!/usr/bin/env python3
"""
Génère les MP3 ElevenLabs pour les 110 nouvelles questions CP.
Lance depuis le dossier pocketsage/ : python3 generate_new_cp_mp3.py
"""
import requests, os, time

API_KEY  = "sk_e920c195b03adac355923ab26527d2d48af72105260a0c00"
VOICE_FR = "GFj5Qf6cNQ3Lgp8VKBwc"
VOICE_EN = "9mF01VTvwaxuBPjm0hMu"

FR_QUESTIONS = [
    ("LG-CP-072", "Quel est l'intrus ? Pomme, poire, banane, carotte"),
    ("LG-CP-073", "Quelle forme a 4 c\u00f4t\u00e9s \u00e9gaux ?"),
    ("LG-CP-074", "Quel est l'intrus ? Rouge, bleu, chien, vert"),
    ("LG-CP-075", "Qu'est-ce qui vient apr\u00e8s 2, 4, 6 ?"),
    ("LG-CP-076", "Quel est l'intrus ? V\u00e9lo, voiture, moto, chapeau"),
    ("LG-CP-077", "Qu'est-ce qui vient apr\u00e8s 5, 10, 15 ?"),
    ("LG-CP-078", "Quel est l'intrus ? Lundi, mardi, mars, jeudi"),
    ("LG-CP-079", "Le chien est \u00e0 la niche. La voiture est au... ?"),
    ("LG-CP-080", "Quel est l'intrus ? Piano, guitare, violon, pinceau"),
    ("LG-CP-081", "Qu'est-ce qui vient apr\u00e8s 10, 9, 8 ?"),
    ("LG-CP-082", "Quel est l'intrus ? Chat, chien, lapin, table"),
    ("LG-CP-083", "Si A=1 et B=2, que vaut C ?"),
    ("LG-CP-084", "Quel est l'intrus ? Manteau, pantalon, g\u00e2teau, chapeau"),
    ("LG-CP-085", "Qu'est-ce qui vient apr\u00e8s \ud83d\udd34\ud83d\udd35\ud83d\udd34\ud83d\udd35 ?"),
    ("LG-CP-086", "Quel est l'intrus ? Stylo, crayon, r\u00e8gle, chaussure"),
    ("LG-CP-087", "La vache donne du lait. La poule donne des... ?"),
    ("LG-CP-088", "Quel est l'intrus ? Janvier, f\u00e9vrier, lundi, avril"),
    ("LG-CP-089", "Qu'est-ce qui vient apr\u00e8s 1, 3, 5, 7 ?"),
    ("LG-CP-090", "Quel est l'intrus ? Lion, tigre, \u00e9l\u00e9phant, hibou"),
    ("LG-CP-091", "Le jour c'est le soleil, la nuit c'est la... ?"),
    ("LG-CP-092", "Quel est l'intrus ? Rose, tulipe, cerise, marguerite"),
    ("LG-CP-093", "Qu'est-ce qui vient apr\u00e8s 20, 18, 16 ?"),
    ("LG-CP-094", "Quel est l'intrus ? Natation, football, lecture, tennis"),
    ("LG-CP-095", "Le poussin est \u00e0 la poule. Le chaton est au... ?"),
    ("LG-CP-096", "Quel est l'intrus ? Cuill\u00e8re, fourchette, couteau, stylo"),
    ("LG-CP-097", "Qu'est-ce qui vient apr\u00e8s \u2b1b\u2b1c\u2b1b\u2b1c ?"),
    ("LG-CP-098", "Quel est l'intrus ? Pain, beurre, lait, verre"),
    ("LG-CP-099", "Le papa de papa, c'est mon... ?"),
    ("LG-CP-100", "Quel est l'intrus ? Marteau, tournevis, scie, ballon"),
    ("LG-CP-101", "Qu'est-ce qui vient apr\u00e8s 3, 6, 9 ?"),
    ("MA-CP-082", "Combien font 8 + 5 ?"),
    ("MA-CP-083", "Combien font 10 - 3 ?"),
    ("MA-CP-084", "J'ai 6 bonbons, j'en mange 2. Combien en reste-t-il ?"),
    ("MA-CP-085", "Quel nombre est entre 7 et 9 ?"),
    ("MA-CP-086", "Combien font 4 + 4 + 4 ?"),
    ("MA-CP-087", "Quelle forme a 3 c\u00f4t\u00e9s ?"),
    ("MA-CP-088", "Combien font 9 + 9 ?"),
    ("MA-CP-089", "J'ai 12 crayons, j'en donne 5. Combien en reste-t-il ?"),
    ("MA-CP-090", "Quel nombre vient juste apr\u00e8s 19 ?"),
    ("MA-CP-091", "Combien y a-t-il de roues sur un v\u00e9lo ?"),
    ("MA-CP-092", "Combien font 7 + 6 ?"),
    ("MA-CP-093", "Quel est le double de 5 ?"),
    ("MA-CP-094", "Combien font 15 - 7 ?"),
    ("MA-CP-095", "J'ach\u00e8te un pain \u00e0 2\u20ac et une pomme \u00e0 1\u20ac. Je paye ?"),
    ("MA-CP-096", "Combien y a-t-il de c\u00f4t\u00e9s dans un rectangle ?"),
    ("MA-CP-097", "Quel est le double de 8 ?"),
    ("MA-CP-098", "Combien font 11 + 4 ?"),
    ("MA-CP-099", "J'ai 20 billes, j'en perds 8. Combien en reste-t-il ?"),
    ("MA-CP-100", "Quel nombre est plus grand : 14 ou 17 ?"),
    ("MA-CP-101", "Combien y a-t-il de pattes sur 2 chiens ?"),
    ("MA-CP-102", "Combien font 6 + 7 ?"),
    ("MA-CP-103", "La moiti\u00e9 de 10, c'est ?"),
    ("MA-CP-104", "Combien font 18 - 9 ?"),
    ("MA-CP-105", "J'ai 3 sacs avec 4 billes chacun. Combien de billes ?"),
    ("MA-CP-106", "Combien y a-t-il de doigts sur 2 mains ?"),
    ("MA-CP-107", "Quel est le nombre juste avant 16 ?"),
    ("MA-CP-108", "Combien font 13 + 5 ?"),
    ("MA-CP-109", "J'ai 10\u20ac. J'ach\u00e8te un jouet \u00e0 6\u20ac. Il me reste ?"),
    ("MA-CP-110", "Combien font 5 + 5 + 5 ?"),
    ("MA-CP-111", "Quel nombre est entre 11 et 13 ?"),
    ("FR-CP-101", "Quel son entends-tu dans 'soleil' ?"),
    ("FR-CP-102", "Quel mot rime avec 'chat' ?"),
    ("FR-CP-103", "Quel est le contraire de 'grand' ?"),
    ("FR-CP-104", "Combien de syllabes dans 'mai-son' ?"),
    ("FR-CP-105", "Quel son entends-tu dans 'beau' ?"),
    ("FR-CP-106", "Quel mot rime avec 'maman' ?"),
    ("FR-CP-107", "Combien de syllabes dans 'pa-pa-lon' ?"),
    ("FR-CP-108", "Quel est le contraire de 'chaud' ?"),
    ("FR-CP-109", "Quel son entends-tu au d\u00e9but de 'girafe' ?"),
    ("FR-CP-110", "Quel mot d\u00e9signe plusieurs chats ?"),
    ("FR-CP-111", "Quel son entends-tu dans 'train' ?"),
    ("FR-CP-112", "Quel mot rime avec 'fleur' ?"),
    ("FR-CP-113", "Combien de syllabes dans 'pa-pi-llon' ?"),
    ("FR-CP-114", "Quel est le contraire de 'vite' ?"),
    ("FR-CP-115", "Quel son entends-tu dans 'genou' ?"),
    ("FR-CP-116", "Quel mot est un pr\u00e9nom ?"),
    ("FR-CP-117", "Quel est le contraire de 'dur' ?"),
    ("FR-CP-118", "Combien de syllabes dans 'chat' ?"),
    ("FR-CP-119", "Quel son entends-tu au d\u00e9but de 'cerise' ?"),
    ("FR-CP-120", "Quel mot d\u00e9signe une seule \u00e9toile ?"),
    ("FR-CP-121", "Quel mot rime avec 'bateau' ?"),
    ("FR-CP-122", "Combien de syllabes dans 'ca-na-pe' ?"),
    ("FR-CP-123", "Quel est le contraire de 'propre' ?"),
    ("FR-CP-124", "Quel son entends-tu dans 'lion' ?"),
    ("FR-CP-125", "Quel mot est un verbe (une action) ?"),
    ("FR-CP-126", "Quel mot rime avec 'chapeau' ?"),
    ("FR-CP-127", "Combien de syllabes dans 'e-le-phant' ?"),
    ("FR-CP-128", "Quel est le contraire de 'plein' ?"),
    ("FR-CP-129", "Quel mot contient le son 'oin' ?"),
    ("FR-CP-130", "Quel mot est un adjectif (une description) ?"),
]

EN_QUESTIONS = [
    ("AN-CP-122", "How do you say 'rouge' in English?"),
    ("AN-CP-123", "How do you say 'chien' in English?"),
    ("AN-CP-124", "How many is 'three' ?"),
    ("AN-CP-125", "How do you say 'maman' in English?"),
    ("AN-CP-126", "What color is grass?"),
    ("AN-CP-127", "How do you say 'oiseau' in English?"),
    ("AN-CP-128", "How do you say '\u00e9cole' in English?"),
    ("AN-CP-129", "How many is 'five' ?"),
    ("AN-CP-130", "How do you say 'bleu' in English?"),
    ("AN-CP-131", "How do you say 'maison' in English?"),
    ("AN-CP-132", "How do you say 'pomme' in English?"),
    ("AN-CP-133", "How do you say 'papa' in English?"),
    ("AN-CP-134", "What color is the sun?"),
    ("AN-CP-135", "How do you say 'livre' in English?"),
    ("AN-CP-136", "How many is 'ten' ?"),
    ("AN-CP-137", "How do you say 'eau' in English?"),
    ("AN-CP-138", "How do you say 'chat' in English?"),
    ("AN-CP-139", "How do you say 'banane' in English?"),
    ("AN-CP-140", "How do you say 'fr\u00e8re' in English?"),
    ("AN-CP-141", "What do you say when you meet someone?"),
]


os.makedirs('audio/fr', exist_ok=True)
os.makedirs('audio/en', exist_ok=True)
errors = []

def gen(questions, voice, folder, is_en):
    for i, (qid, text) in enumerate(questions):
        file_id = qid.replace('LG-CP-', 'FR-CP-') if not is_en else qid
        fname   = f"{file_id}.mp3" if is_en else f"{file_id}_enonce.mp3"
        fpath   = os.path.join(folder, fname)
        if os.path.exists(fpath):
            print(f"  SKIP {fname}")
            continue
        resp = requests.post(
            f"https://api.elevenlabs.io/v1/text-to-speech/{voice}",
            headers={"xi-api-key": API_KEY, "Content-Type": "application/json"},
            json={"text": text, "model_id": "eleven_multilingual_v2",
                  "voice_settings": {"stability": 0.5, "similarity_boost": 0.8}},
            timeout=30)
        if resp.status_code == 200:
            with open(fpath, 'wb') as f: f.write(resp.content)
            print(f"  [{i+1}/{len(questions)}] OK {fname}")
        else:
            errors.append((qid, resp.status_code))
            print(f"  [{i+1}/{len(questions)}] ERR {qid}: {resp.status_code}")
        time.sleep(0.25)

print("=== FR (Olivier) ===")
gen(FR_QUESTIONS, VOICE_FR, 'audio/fr', False)
print("=== EN (Charlie Horse) ===")
gen(EN_QUESTIONS, VOICE_EN, 'audio/en', True)
print(f"\nTerminé. Erreurs: {len(errors)}")
if errors:
    for e in errors: print(f"  {e}")
