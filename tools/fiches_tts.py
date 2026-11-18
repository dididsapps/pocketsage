"""Voix des fiches de révision GS → CE2 (hors anglais) → R2 audio/fiches/<id>.mp3, + envoi des PDF fiches/**/REV-*.pdf.
Google TTS fr-FR-Neural2-D. Texte lu = fiche_lue() (même ordre que l'affichage, pour le surlignage).
Ne refait que le nouveau / modifié (empreinte en métadonnée).
  python3 tools/fiches_tts.py
"""
import base64, hashlib, html, json, os, re, subprocess, sys, tempfile
from pathlib import Path
import requests
ROOT = Path(__file__).resolve().parent.parent
CDN = 'https://pub-8cdc5500f1ab4785ba254b7335f7a68a.r2.dev'


def textes():
    sys.path.insert(0, str(ROOT / 'tools'))
    from fiches_build import fiche_lue, PETITS
    for f in sorted((ROOT / 'docs/contenu/fiches/FR').glob('REV-*.json')):
        _, code, cl = f.stem.split('-')
        if cl not in PETITS or code in ('AN', 'ES'): continue
        for x in json.loads(f.read_text(encoding='utf-8'))['fiches']:
            yield x['id'], ' [P1] '.join(m if re.search(r'[.!?…:]$', m) else m + '.' for m in fiche_lue(x))


def ssml(t):
    t = html.escape(re.sub(r'[\U0001F300-\U0001FAFF☀-➿]', '', t), quote=False)
    t = re.sub(r'\[P(\d+)\]', lambda m: f'<break time="{m.group(1)}s"/>', t)
    t = re.sub(r'…', '<break time="700ms"/>', t)
    t = re.sub(r'\n\s*\n', '<break time="1200ms"/>', t)
    return t


def morceaux(t, maxb=4200):
    out, cur = [], ''
    for ph in re.split(r'(?<=[.!?])\s+', t):
        if len((cur + ph).encode()) > maxb and cur: out.append(cur); cur = ''
        cur += ph + ' '
    return out + ([cur] if cur else [])


def main():
    import boto3
    from botocore.config import Config
    gk = os.environ['GOOGLE_TTS_API_KEY'].strip()
    s3 = boto3.client('s3', endpoint_url='https://8ea67fd06083effd6f76efdefb92092f.r2.cloudflarestorage.com',
                      aws_access_key_id=os.environ['R2_ACCESS_KEY'].strip(), aws_secret_access_key=os.environ['R2_SECRET_KEY'].strip(), config=Config(region_name='auto'))
    tmp = Path(tempfile.mkdtemp()); n = 0
    for cle, t in textes():
        h = hashlib.md5(t.encode()).hexdigest()[:12]; k = f'audio/fiches/{cle}.mp3'
        r = requests.head(f'{CDN}/{k}', timeout=20)
        if r.status_code == 200 and r.headers.get('x-amz-meta-h') == h: continue
        parts = []
        for i, m in enumerate(morceaux(ssml(t))):
            r = requests.post(f'https://texttospeech.googleapis.com/v1/text:synthesize?key={gk}', timeout=120,
                              json={'input': {'ssml': '<speak>' + m + '</speak>'}, 'voice': {'languageCode': 'fr-FR', 'name': 'fr-FR-Neural2-D'},
                                    'audioConfig': {'audioEncoding': 'MP3', 'speakingRate': 0.9, 'pitch': -1.0}})
            if r.status_code != 200: print('  ✗', cle, r.text[:150]); parts = []; break
            p = tmp / f'{cle}_{i}.mp3'; p.write_bytes(base64.b64decode(r.json()['audioContent'])); parts.append(p)
        if not parts: continue
        f = tmp / f'{cle}.mp3'
        if len(parts) == 1: parts[0].rename(f)
        else:
            lst = tmp / 'l.txt'; lst.write_text(''.join(f"file '{p}'\n" for p in parts))
            subprocess.run(['ffmpeg', '-y', '-v', 'quiet', '-f', 'concat', '-safe', '0', '-i', str(lst), '-c', 'copy', str(f)], check=True)
        s3.upload_file(str(f), 'pocketsage-audio', k, ExtraArgs={'ContentType': 'audio/mpeg', 'CacheControl': 'public, max-age=3600', 'Metadata': {'h': h}})
        n += 1; print('  ✓', cle)
    # fiches PDF du dépôt → R2 (fiches/FR/…)
    for f in sorted((ROOT / 'fiches').rglob('REV-*.pdf')):
        k = 'fiches/' + str(f.relative_to(ROOT / 'fiches')); h = hashlib.md5(f.read_bytes()).hexdigest()[:12]
        r = requests.head(f'{CDN}/{k}', timeout=20)
        if r.status_code == 200 and r.headers.get('x-amz-meta-h') == h: continue
        s3.upload_file(str(f), 'pocketsage-audio', k, ExtraArgs={'ContentType': 'application/pdf', 'CacheControl': 'public, max-age=3600', 'Metadata': {'h': h}})
        print('  🖨️', k)
    print(f'✅ {n} voix de fiches')


if __name__ == '__main__':
    main()
