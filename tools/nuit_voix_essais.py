"""Échantillons de voix pour les séances d'endormissement (Google TTS) → R2 audio/nuit/essais/.
  python3 tools/nuit_voix_essais.py
"""
import base64, os, subprocess, tempfile
from pathlib import Path
import requests, boto3
from botocore.config import Config

KEY = os.environ.get('GOOGLE_TTS_API_KEY', '').strip()
TXT = ("Installe-toi confortablement. Laisse ton corps s'enfoncer doucement dans le lit. "
       "Tu n'as rien à faire. Rien à réussir. Juste écouter ma voix. "
       "Inspire tout doucement par le nez… et souffle lentement… encore plus lentement. "
       "À chaque souffle, tes épaules deviennent un peu plus lourdes… un peu plus calmes. "
       "Tes bras se posent… tes mains se reposent… et tout ton corps devient lourd, chaud, tranquille.")
SSML = '<speak>' + TXT.replace('… ', '<break time="1200ms"/> ').replace('. ', '.<break time="900ms"/> ') + '</speak>'
VOIX = [
    ('1_neural2D_grave', 'fr-FR-Neural2-D', 0.78, -5.0, True, False),
    ('2_wavenetD_grave', 'fr-FR-Wavenet-D', 0.78, -4.0, True, False),
    ('3_studioD', 'fr-FR-Studio-D', 0.80, None, True, False),
    ('4_chirp_charon', 'fr-FR-Chirp3-HD-Charon', 0.85, None, False, False),
    ('5_chirp_iapetus', 'fr-FR-Chirp3-HD-Iapetus', 0.85, None, False, False),
    ('6_chirp_algenib', 'fr-FR-Chirp3-HD-Algenib', 0.85, None, False, False),
    ('7_neural2D_grave_doux', 'fr-FR-Neural2-D', 0.80, -3.0, True, True),
]
s3 = boto3.client('s3', endpoint_url='https://8ea67fd06083effd6f76efdefb92092f.r2.cloudflarestorage.com',
                  aws_access_key_id=os.environ['R2_ACCESS_KEY'].strip(), aws_secret_access_key=os.environ['R2_SECRET_KEY'].strip(),
                  config=Config(region_name='auto'))
tmp = Path(tempfile.mkdtemp())
for nom, voix, rate, pitch, ssml, filtre in VOIX:
    cfg = {'audioEncoding': 'MP3', 'speakingRate': rate}
    if pitch is not None: cfg['pitch'] = pitch
    inp = {'ssml': SSML} if ssml else {'text': TXT}
    r = requests.post(f'https://texttospeech.googleapis.com/v1/text:synthesize?key={KEY}',
                      json={'input': inp, 'voice': {'languageCode': 'fr-FR', 'name': voix}, 'audioConfig': cfg}, timeout=120)
    if r.status_code != 200 and 'speakingRate' in r.text:
        cfg.pop('speakingRate'); r = requests.post(f'https://texttospeech.googleapis.com/v1/text:synthesize?key={KEY}',
                      json={'input': inp, 'voice': {'languageCode': 'fr-FR', 'name': voix}, 'audioConfig': cfg}, timeout=120)
    if r.status_code != 200:
        print('✗', nom, r.status_code, r.text[:200]); continue
    f = tmp / f'{nom}.mp3'; f.write_bytes(base64.b64decode(r.json()['audioContent']))
    if filtre:  # plus feutré : légère baisse de hauteur + aigus adoucis + petite réverbération
        g = tmp / f'{nom}_f.mp3'
        subprocess.run(['ffmpeg', '-y', '-v', 'quiet', '-i', str(f), '-af',
                        'asetrate=24000*0.94,aresample=24000,atempo=1.0,lowpass=f=6500,aecho=0.8:0.7:40:0.15', str(g)], check=True)
        f = g
    s3.upload_file(str(f), 'pocketsage-audio', f'audio/nuit/essais/{nom}.mp3', ExtraArgs={'ContentType': 'audio/mpeg', 'CacheControl': 'no-cache'})
    print('✓', nom)
