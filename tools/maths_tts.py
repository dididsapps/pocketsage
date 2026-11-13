"""PocketSage — réenregistre les questions/réponses qui contiennent des symboles maths
(×, ÷, ≠, ², √…) avec les symboles dits en mots (« 2 fois 3 égale combien ? »).

- Lit les questions dans index.html (enonce + choix), garde celles avec symboles.
- Texte prononcé = tools/parle.py (même règles que _ttsParle dans l'appli).
- Google TTS (mêmes voix que les autres questions), upload R2 : audio/{fr|en|es}/m/{ID}_{partie}.mp3
- Écrit data/audio_maths.json : {langue: {empreinte_du_texte_affiché: "m/ID_partie"}}
  + data/audio_maths_etat.json (ce qui est déjà fait, pour ne refaire que le nouveau/modifié).

Clés : GOOGLE_TTS_API_KEY, R2_ACCESS_KEY, R2_SECRET_KEY (env, .env ou secrets GitHub).
  python3 tools/maths_tts.py [--dry-run] [--no-upload]
"""
import argparse, base64, json, os, re, sys, tempfile, time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'tools'))
from parle import parle, empreinte, REDIRE as SYMB  # noqa: E402

_env = ROOT / '.env'
if _env.exists():
    for line in _env.read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if line and not line.startswith('#') and '=' in line:
            k, v = line.split('=', 1)
            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

GOOGLE_KEY = os.environ.get('GOOGLE_TTS_API_KEY', '')
R2_BUCKET = os.environ.get('R2_BUCKET', 'pocketsage-audio')
R2_ENDPOINT = os.environ.get('R2_ENDPOINT', 'https://8ea67fd06083effd6f76efdefb92092f.r2.cloudflarestorage.com')
VOIX = {'fr': ('fr-FR', 'fr-FR-Neural2-D'), 'en': ('en-GB', 'en-GB-Neural2-B'), 'es': ('es-ES', 'es-ES-Neural2-B')}
MAN = ROOT / 'data' / 'audio_maths.json'
ETAT = ROOT / 'data' / 'audio_maths_etat.json'


def js_str(x):
    return json.loads('"' + x.replace('\\\'', "'").replace('"', '\\"') + '"') if '\\' in x else x


def questions():
    src = (ROOT / 'index.html').read_text(encoding='utf-8')
    vus = set()
    for m in re.finditer(r'\{id:["\']([A-Z0-9]+(?:-[A-Za-z0-9]+)+)["\'],[^\n]*', src):
        iid, line = m.group(1), m.group(0)
        if iid in vus:
            continue
        vus.add(iid)
        e = re.search(r'enonce:"((?:[^"\\]|\\.)*)"', line) or re.search(r"enonce:'((?:[^'\\]|\\.)*)'", line)
        c = re.search(r'choix:\[([^\]]*)\]', line)
        parts = []
        if e:
            parts.append(('enonce', js_str(e.group(1))))
        if c:
            for i, (a, b) in enumerate(re.findall(r'"((?:[^"\\]|\\.)*)"|\'((?:[^\'\\]|\\.)*)\'', c.group(1))):
                parts.append((f'choix_{i}', js_str(a or b)))
        lang = 'en' if iid.startswith('AN-') else 'es' if re.match(r'ES-(GS|CP|CE|CM|\d|LY)', iid) else 'fr'
        for p, t in parts:
            if t and SYMB.search(t):
                yield iid, p, t, lang


def tts(text, lang, out):
    import requests
    lc, name = VOIX[lang]
    payload = {'input': {'text': text}, 'voice': {'languageCode': lc, 'name': name},
               'audioConfig': {'audioEncoding': 'MP3', 'speakingRate': 0.85}}
    for k in range(5):
        try:
            r = requests.post(f'https://texttospeech.googleapis.com/v1/text:synthesize?key={GOOGLE_KEY}', json=payload, timeout=60)
        except requests.RequestException:
            time.sleep(5 * 2 ** k); continue
        if r.status_code in (429, 500, 502, 503, 504):
            time.sleep(5 * 2 ** k); continue
        break
    else:
        return False
    if r.status_code == 200 and r.json().get('audioContent'):
        out.write_bytes(base64.b64decode(r.json()['audioContent'])); return True
    print('  ✗', r.status_code, r.text[:120]); return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--no-upload', action='store_true')
    a = ap.parse_args()
    etat = json.loads(ETAT.read_text()) if ETAT.exists() else {}
    todo, man = [], {}
    for iid, part, txt, lang in questions():
        key = f'm/{iid}_{part}'
        h = empreinte(txt)
        man.setdefault(lang, {})[h] = key
        if etat.get(f'{lang}/{key}') != h:
            todo.append((iid, part, txt, lang, key, h))
    print(f'{sum(len(v) for v in man.values())} textes avec symboles, {len(todo)} à (ré)enregistrer')
    if a.dry_run:
        for t in todo[:20]:
            print(' ', t[0], t[1], '→', parle(t[2], t[3].upper()))
        return
    if todo and not GOOGLE_KEY:
        sys.exit('❌ GOOGLE_TTS_API_KEY manquante')
    s3 = None
    if todo and not a.no_upload:
        import boto3
        from botocore.config import Config
        s3 = boto3.client('s3', endpoint_url=R2_ENDPOINT, aws_access_key_id=os.environ.get('R2_ACCESS_KEY', ''),
                          aws_secret_access_key=os.environ.get('R2_SECRET_KEY', ''),
                          config=Config(region_name='auto', retries={'max_attempts': 3, 'mode': 'adaptive'}))
    tmp = Path(tempfile.mkdtemp())
    ok = 0
    for i, (iid, part, txt, lang, key, h) in enumerate(todo):
        out = tmp / f'{iid}_{part}.mp3'
        if not tts(parle(txt, lang.upper()), lang, out):
            man[lang].pop(h, None); continue
        if s3:
            s3.upload_file(str(out), R2_BUCKET, f'audio/{lang}/{key}.mp3',
                           ExtraArgs={'ContentType': 'audio/mpeg', 'CacheControl': 'public, max-age=31536000'})
        etat[f'{lang}/{key}'] = h; ok += 1
        if i % 25 == 0:
            print(f'  {i + 1}/{len(todo)}')
    # ne publier dans le manifeste que ce qui est réellement enregistré
    for lang in man:
        man[lang] = {h: k for h, k in man[lang].items() if etat.get(f'{lang}/{k}') == h}
    MAN.write_text(json.dumps(man, ensure_ascii=False, separators=(',', ':')), encoding='utf-8')
    ETAT.write_text(json.dumps(etat, ensure_ascii=False, indent=0, sort_keys=True), encoding='utf-8')
    print(f'✅ {ok} enregistrés')


if __name__ == '__main__':
    main()
