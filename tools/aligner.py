"""Surlignage du texte pendant la lecture : heure de début de chaque mot dans les MP3 (Whisper, horodatage par mot).
Cibles : histoires de l'onglet Nuit (FR + EN) et énoncés des questions GS → CE2 (FR) [+ --langues : questions AN-/ES-].
Sortie R2 : audio/align/{clé}.json = {"s":[début du mot 1, du mot 2, …]} — un nombre par mot AFFICHÉ
(mot = suite non vide contenant une lettre ou un chiffre ; même découpage que _hlTok dans index.html).
  python3 tools/aligner.py [--shard 0 --of 4] [--langues] [--max N] [--liste]
"""
import argparse, difflib, json, os, re, subprocess, sys, tempfile, unicodedata
from pathlib import Path
import requests

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'tools'))
from parle import empreinte  # noqa: E402
from qparse import texte_questions, field  # noqa: E402
from nuit_tts import items as nuit_items, CDN  # noqa: E402

PETITS = ('GS', 'CP', 'CE1', 'CE2')


def mots(t):
    return [m for m in t.split() if re.search(r'[^\W_]', m)]


def norm(t):
    t = unicodedata.normalize('NFD', t.lower().replace('’', "'"))
    return re.sub(r'[^\w]', '', ''.join(c for c in t if unicodedata.category(c) != 'Mn'))


def nuit_affiche(titre, texte):
    t = re.sub(r'\s*\[P\d+\]\s*', ' ', texte)
    t = re.sub(r'\[(RESPIRE|BREATHE|PAUSE)\]\s*', '', t)
    return titre + ' ' + t


def cibles(langues=False):
    out = []
    for base, lang, ti, tx in nuit_items():
        k = 'nuit/' + base + ('' if lang == 'FR' else '_' + lang)
        out.append((k, f'{CDN}/audio/nuit/{k[5:]}.mp3', nuit_affiche(ti, tx), lang.lower()))
    man = json.loads((ROOT / 'data/audio_textes.json').read_text())
    for f, m in json.loads((ROOT / 'data/audio_maths.json').read_text()).items():
        man.setdefault(f, {}).update(m)
    src = texte_questions(); vus = set()
    for m in re.finditer(r'\{id:["\']([A-Z]+)-([A-Z0-9]+)-[^"\']*["\'],[^\n]*', src):
        line = m.group(0); cl = field(line, 'classe') or ''
        langue = m.group(1) in ('AN', 'ES')
        if langue and not langues: continue
        if not langue and cl not in PETITS: continue
        e = field(line, 'enonce')
        if not e or e in vus: continue
        vus.add(e); h = empreinte(e)
        for lg in (['en'] if m.group(1) == 'AN' else ['es'] if m.group(1) == 'ES' else []) + ['fr', 'en', 'es']:
            k = man.get(lg, {}).get(h)
            if k:
                out.append((f'{lg}/{k}', f'{CDN}/audio/{lg}/{k}.mp3', e, lg)); break
    return out


def aligner(model, mp3, texte, lang):
    raw = subprocess.run(['ffmpeg', '-v', 'quiet', '-i', str(mp3), '-f', 's16le', '-ac', '1', '-ar', '16000', '-'], capture_output=True, check=True).stdout
    import numpy as np
    audio = np.frombuffer(raw, np.int16).astype(np.float32) / 32768.0
    segs, _ = model.transcribe(audio, language=lang, word_timestamps=True, beam_size=5, vad_filter=False,
                               condition_on_previous_text=True, initial_prompt=texte[:220])
    ww = [(w.word.strip(), w.start, w.end) for s in segs for w in (s.words or []) if w.word.strip()]
    aff = mots(texte); da = [norm(x) for x in aff]; dw = [norm(x[0]) for x in ww]
    st = [None] * len(aff)
    for a, b, n in difflib.SequenceMatcher(None, da, dw, autojunk=False).get_matching_blocks():
        for i in range(n): st[a + i] = ww[b + i][1]
    # mots non reconnus (chiffres dits en lettres, symboles…) : interpolation entre voisins reconnus
    fin = (ww[-1][2] if ww else len(audio) / 16000)
    i = 0
    while i < len(st):
        if st[i] is None:
            j = i
            while j < len(st) and st[j] is None: j += 1
            a = st[i - 1] if i > 0 else (ww[0][1] if ww else 0)
            b = st[j] if j < len(st) else fin
            for q in range(i, j): st[q] = a + (b - a) * (q - i + (1 if i > 0 else 0)) / (j - i + (1 if i > 0 else 0))
            i = j
        else: i += 1
    for q in range(1, len(st)): st[q] = max(st[q], st[q - 1])   # toujours croissant
    ok = sum(1 for a, b, n in difflib.SequenceMatcher(None, da, dw, autojunk=False).get_matching_blocks() for _ in range(n))
    return [round(x, 2) for x in st], ok / max(1, len(aff))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--shard', type=int, default=0); ap.add_argument('--of', type=int, default=1)
    ap.add_argument('--langues', action='store_true'); ap.add_argument('--max', type=int, default=0); ap.add_argument('--liste', action='store_true')
    a = ap.parse_args()
    cs = cibles(a.langues)[a.shard::a.of]
    print(len(cs), 'cibles (part', a.shard, '/', a.of, ')')
    if a.liste:
        for c in cs[:10]: print(c)
        return
    import boto3
    from botocore.config import Config
    from faster_whisper import WhisperModel
    s3 = boto3.client('s3', endpoint_url='https://8ea67fd06083effd6f76efdefb92092f.r2.cloudflarestorage.com',
                      aws_access_key_id=os.environ['R2_ACCESS_KEY'].strip(), aws_secret_access_key=os.environ['R2_SECRET_KEY'].strip(),
                      config=Config(region_name='auto'))
    model = WhisperModel(os.environ.get('WHISPER_MODEL', 'small'), device='cpu', compute_type='int8')
    tmp = Path(tempfile.mkdtemp()); n = faits = 0; qual = []
    for k, url, texte, lang in cs:
        try:
            m = requests.head(url, timeout=20)
            if m.status_code != 200: continue
            etag = m.headers.get('etag', '').strip('"') + ':' + empreinte(texte)
            e = requests.head(f'{CDN}/audio/align/{k}.json', timeout=20)
            if e.status_code == 200 and e.headers.get('x-amz-meta-src') == etag: continue
            f = tmp / 'a.mp3'; f.write_bytes(requests.get(url, timeout=120).content)
            st, q = aligner(model, f, texte, lang); qual.append(q)
            j = tmp / 'a.json'; j.write_text(json.dumps({'s': st}, separators=(',', ':')))
            s3.upload_file(str(j), 'pocketsage-audio', f'audio/align/{k}.json',
                           ExtraArgs={'ContentType': 'application/json', 'CacheControl': 'public, max-age=3600', 'Metadata': {'src': etag}})
            faits += 1
            if faits % 50 == 0: print(f'  {faits} alignés (reconnaissance moyenne {sum(qual) / len(qual):.0%})', flush=True)
            if a.max and faits >= a.max: break
        except Exception as ex:
            print('  ✗', k, str(ex)[:120])
    print(f'✅ {faits} alignements' + (f', mots reconnus en moyenne {sum(qual) / len(qual):.0%}' if qual else ''))


if __name__ == '__main__':
    main()
