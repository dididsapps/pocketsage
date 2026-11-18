"""Enveloppe de volume des MP3 de l'onglet Nuit (pour la veilleuse qui suit la voix).
Pour chaque MP3 audio/nuit/{ID}[_EN].mp3 sans enveloppe (ou plus récent qu'elle) : télécharge, calcule le volume
toutes les 100 ms (0-9), envoie audio/nuit/env/{ID}[_EN].json = {"hz":10,"v":"0123…"} sur R2.
  python3 tools/nuit_env.py
"""
import json, os, subprocess, sys, tempfile
from pathlib import Path
import numpy as np, requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nuit_tts import items, CDN  # noqa: E402


def enveloppe(mp3, hz=10):
    raw = subprocess.run(['ffmpeg', '-v', 'quiet', '-i', str(mp3), '-f', 's16le', '-ac', '1', '-ar', '8000', '-'], capture_output=True, check=True).stdout
    x = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
    n = 8000 // hz; m = len(x) // n
    rms = np.sqrt((x[:m * n].reshape(m, n) ** 2).mean(1) + 1e-12)
    db = 20 * np.log10(rms)
    voix = db[db > -45]
    hi = np.percentile(voix, 95) if len(voix) else -10
    lv = np.clip((db - (hi - 30)) / 30, 0, 1)          # 30 dB de dynamique sous le pic de voix
    return ''.join(str(int(round(v * 9))) for v in lv)


def main():
    import boto3
    from botocore.config import Config
    s3 = boto3.client('s3', endpoint_url='https://8ea67fd06083effd6f76efdefb92092f.r2.cloudflarestorage.com',
                      aws_access_key_id=os.environ['R2_ACCESS_KEY'].strip(), aws_secret_access_key=os.environ['R2_SECRET_KEY'].strip(),
                      config=Config(region_name='auto'))
    tmp = Path(tempfile.mkdtemp()); n = 0
    vus = set()
    for base, lang, _, _ in items():
        k = base + ('' if lang == 'FR' else '_' + lang)
        if k in vus: continue
        vus.add(k)
        m = requests.head(f'{CDN}/audio/nuit/{k}.mp3', timeout=20)
        if m.status_code != 200: continue
        e = requests.head(f'{CDN}/audio/nuit/env/{k}.json', timeout=20)
        if e.status_code == 200 and e.headers.get('x-amz-meta-src') == m.headers.get('etag', '').strip('"'): continue
        f = tmp / 'a.mp3'; f.write_bytes(requests.get(f'{CDN}/audio/nuit/{k}.mp3', timeout=120).content)
        v = enveloppe(f)
        j = tmp / 'e.json'; j.write_text(json.dumps({'hz': 10, 'v': v}, separators=(',', ':')))
        s3.upload_file(str(j), 'pocketsage-audio', f'audio/nuit/env/{k}.json',
                       ExtraArgs={'ContentType': 'application/json', 'CacheControl': 'public, max-age=3600',
                                  'Metadata': {'src': m.headers.get('etag', '').strip('"')}})
        n += 1; print('  ✓', k, len(v) // 10, 's')
    print(f'✅ {n} enveloppes')


if __name__ == '__main__':
    main()
