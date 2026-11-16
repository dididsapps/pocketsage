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
        pat = r"\{id:%s((?:HS|HC|HR|MED|SD)(?:-EN)?-\d+)%s,titre:%s((?:[^%s\\]|\\.)*)%s,texte:%s((?:[^%s\\]|\\.)*)%s" % ((q,) * 8)
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


# ── Voyages du sommeil (SD-xxx) : voix Google grave et posée (choix de Mario : échantillon n°1) ──
GVOIX = ('fr-FR', 'fr-FR-Neural2-D', 0.78, -5.0)


def ssml_morceaux(titre, texte, maxb=4200):
    import html
    t = re.sub(r'[\U0001F300-\U0001FAFF\u2600-\u27BF]', '', titre).strip() + '. [P3]\n\n' + texte
    paras, out, cur = [p for p in re.split(r'\n\s*\n', t) if p.strip()], [], ''
    def conv(p):
        p = html.escape(p.strip(), quote=False)
        p = re.sub(r'\[P(\d+)\]', lambda m: f'<break time="{int(m.group(1))}s"/>', p)
        p = re.sub(r'…|\.\.\.', '<break time="1s"/>', p)
        return p + '<break time="2s"/>'
    for p in paras:
        c = conv(p)
        if len((cur + c).encode()) > maxb and cur:
            out.append(cur); cur = ''
        cur += c + ' '
    if cur: out.append(cur)
    return ['<speak>' + m + '</speak>' for m in out]


def google_sd(titre, texte, dest):
    import base64, subprocess
    gk = os.environ.get('GOOGLE_TTS_API_KEY', '').strip()
    lc, name, rate, pitch = GVOIX
    parts = []
    for i, ss in enumerate(ssml_morceaux(titre, texte)):
        r = requests.post(f'https://texttospeech.googleapis.com/v1/text:synthesize?key={gk}', timeout=180,
                          json={'input': {'ssml': ss}, 'voice': {'languageCode': lc, 'name': name},
                                'audioConfig': {'audioEncoding': 'MP3', 'speakingRate': rate, 'pitch': pitch, 'sampleRateHertz': 24000}})
        if r.status_code != 200:
            print('  ✗ Google', r.status_code, r.text[:200]); return False
        f = dest.parent / f'part{i}.mp3'; f.write_bytes(base64.b64decode(r.json()['audioContent'])); parts.append(f)
    lst = dest.parent / 'liste.txt'; lst.write_text(''.join(f"file '{p}'\n" for p in parts))
    brut = dest.parent / 'brut.mp3'
    subprocess.run(['ffmpeg', '-y', '-v', 'quiet', '-f', 'concat', '-safe', '0', '-i', str(lst), '-c', 'copy', str(brut)], check=True)
    dur = float(subprocess.run(['ffprobe', '-v', 'quiet', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(brut)], capture_output=True, text=True).stdout or 0)
    # fondu final sur les 40 dernières secondes puis 30 s de silence (pas de fin brutale qui réveille)
    subprocess.run(['ffmpeg', '-y', '-v', 'quiet', '-i', str(brut), '-af', f'afade=t=out:st={max(0, dur - 40):.1f}:d=40,apad=pad_dur=30',
                    '-b:a', '64k', str(dest)], check=True)
    print(f'  ⏱ {dur / 60:.1f} min')
    return True


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--dry-run', action='store_true'); ap.add_argument('--max', type=int, default=30)
    a = ap.parse_args()
    import hashlib
    todo = []
    for base, lang, ti, tx in items():
        if base.startswith('SD-') and lang != 'FR':
            continue
        key = f"audio/nuit/{base}{'' if lang == 'FR' else '_' + lang}.mp3"
        h = hashlib.md5((ti + tx).encode()).hexdigest()[:12]
        try:
            rh = requests.head(f'{CDN}/{key}', timeout=20)
            ok = rh.status_code == 200 and (not base.startswith('SD-') or rh.headers.get('x-amz-meta-h') == h)
        except requests.RequestException:
            ok = False
        if not ok:
            todo.append((key, lang, (ti, tx, h) if base.startswith('SD-') else parle(ti, tx)))
    print(f'{len(todo)} MP3 nuit manquants :', [t[0] for t in todo])
    todo = todo[:a.max]
    if a.dry_run or not todo:
        for k, l, t in todo[:2]: print(k, '→', (ssml_morceaux(t[0], t[1])[0] if isinstance(t, tuple) else t)[:400])
        return
    key = os.environ.get('ELEVENLABS_API_KEY', '').strip()
    if not key and any(not isinstance(t[2], tuple) for t in todo): sys.exit('❌ ELEVENLABS_API_KEY manquante')
    import boto3
    from botocore.config import Config
    s3 = boto3.client('s3', endpoint_url='https://8ea67fd06083effd6f76efdefb92092f.r2.cloudflarestorage.com',
                      aws_access_key_id=os.environ.get('R2_ACCESS_KEY', '').strip(), aws_secret_access_key=os.environ.get('R2_SECRET_KEY', '').strip(),
                      config=Config(region_name='auto'))
    tmp = Path(tempfile.mkdtemp()); n = 0
    for k, lang, txt in todo:
        if isinstance(txt, tuple):   # voyage du sommeil → Google
            d = tmp / k.split('/')[-1].replace('.mp3', ''); d.mkdir(exist_ok=True); f = d / 'final.mp3'
            if google_sd(txt[0], txt[1], f):
                s3.upload_file(str(f), 'pocketsage-audio', k, ExtraArgs={'ContentType': 'audio/mpeg', 'CacheControl': 'public, max-age=3600', 'Metadata': {'h': txt[2]}})
                n += 1; print('  ✓', k, f.stat().st_size // 1024, 'Ko')
            continue
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
