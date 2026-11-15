"""PocketSage — MP3 manquants de l'onglet Nuit (histoires, histoires respirées, méditations).
Vérifie sur le CDN ce qui existe déjà (audio/nuit/{ID}.mp3 et {ID}_EN.mp3) et ne génère que le manquant.
Voix : ElevenLabs « Olivier » (FR) et « Mr Claus » (EN), comme les autres histoires du soir.
Clés : ELEVENLABS_API_KEY, R2_ACCESS_KEY, R2_SECRET_KEY (secrets GitHub ou .env) — jamais dans le code.
  python3 tools/nuit_tts.py [--dry-run] [--max N]
"""
import argparse, os, re, sys, tempfile
from pathlib import Path
import requests

ROOT = Path(__file__).resolve().parent.parent
for p in (ROOT / '.env',):
    if p.exists():
        for l in p.read_text(encoding='utf-8').splitlines():
            if '=' in l and not l.strip().startswith('#'):
                k, v = l.split('=', 1); os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))
CDN = 'https://pub-8cdc5500f1ab4785ba254b7335f7a68a.r2.dev'
VOIX = {'FR': 'GFj5Qf6cNQ3Lgp8VKBwc', 'EN': 'uDsPstFWFBUXjIBimV7s'}


def unjs(t, q):
    return t.replace('\\' + q, q).replace('\\n', '\n')


def items():
    s = (ROOT / 'index.html').read_text(encoding='utf-8')
    out = []
    for q in ("'", '"'):
        pat = r"\{id:%s((?:HS|HC|HR|MED)(?:-EN)?-\d+)%s,titre:%s((?:[^%s\\]|\\.)*)%s,texte:%s((?:[^%s\\]|\\.)*)%s" % ((q,) * 8)
        for i, ti, tx in re.findall(pat, s):
            lang = 'EN' if '-EN-' in i else 'FR'
            base = i.replace('-EN-', '-')
            out.append((base, lang, unjs(ti, q), unjs(tx, q)))
    return out


def parle(titre, texte):
    t = re.sub(r'\[(RESPIRE|BREATHE|PAUSE)\]\s*', '', texte)
    t = re.sub(r'[\U0001F300-\U0001FAFF☀-➿]', '', t)
    # comptes de respiration : « 1… 2… 3… » → vraies pauses d'environ une seconde
    t = re.sub(r'(\d)\s*…\s*', r'\1... <break time="0.9s" /> ', t)
    t = re.sub(r'\n{2,}', ' <break time="1.5s" /> ', t)
    return re.sub(r'[ \t]+', ' ', re.sub(r'[\U0001F300-\U0001FAFF]', '', titre).strip() + '. <break time="1s" /> ' + t).strip()


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--dry-run', action='store_true'); ap.add_argument('--max', type=int, default=30)
    a = ap.parse_args()
    todo = []
    for base, lang, ti, tx in items():
        key = f"audio/nuit/{base}{'' if lang == 'FR' else '_' + lang}.mp3"
        try:
            ok = requests.head(f'{CDN}/{key}', timeout=20).status_code == 200
        except requests.RequestException:
            ok = False
        if not ok:
            todo.append((key, lang, parle(ti, tx)))
    print(f'{len(todo)} MP3 nuit manquants :', [t[0] for t in todo])
    todo = todo[:a.max]
    if a.dry_run or not todo:
        for k, l, t in todo[:2]: print(k, '→', t[:300])
        return
    key = os.environ.get('ELEVENLABS_API_KEY', '')
    if not key: sys.exit('❌ ELEVENLABS_API_KEY manquante')
    import boto3
    from botocore.config import Config
    s3 = boto3.client('s3', endpoint_url='https://8ea67fd06083effd6f76efdefb92092f.r2.cloudflarestorage.com',
                      aws_access_key_id=os.environ.get('R2_ACCESS_KEY', ''), aws_secret_access_key=os.environ.get('R2_SECRET_KEY', ''),
                      config=Config(region_name='auto'))
    tmp = Path(tempfile.mkdtemp()); n = 0
    for k, lang, txt in todo:
        r = requests.post(f'https://api.elevenlabs.io/v1/text-to-speech/{VOIX[lang]}', headers={'xi-api-key': key, 'Content-Type': 'application/json'},
                          json={'text': txt, 'model_id': 'eleven_multilingual_v2',
                                'voice_settings': {'stability': 0.55, 'similarity_boost': 0.75, 'style': 0.2, 'use_speaker_boost': True}}, timeout=180)
        if r.status_code != 200:
            print('  ✗', k, r.status_code, r.text[:150]); continue
        f = tmp / 'a.mp3'; f.write_bytes(r.content)
        s3.upload_file(str(f), 'pocketsage-audio', k, ExtraArgs={'ContentType': 'audio/mpeg', 'CacheControl': 'public, max-age=86400'})
        n += 1; print('  ✓', k, len(r.content) // 1024, 'Ko')
    print(f'✅ {n} MP3 nuit générés')


if __name__ == '__main__':
    main()
