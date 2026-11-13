"""PocketSage — « écoute » les MP3 à risque (symboles, fractions, %, unités) avec Whisper
et écrit un rapport : texte affiché | ce que la voix dit vraiment (transcription).

Lancé par .github/workflows/verif-voix.yml (pip install faster-whisper), rapport en artefact.
  python3 tools/verif_voix.py [--max N]
"""
import argparse, csv, json, os, re, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'tools'))
from parle import empreinte  # noqa: E402

CDN = 'https://pub-8cdc5500f1ab4785ba254b7335f7a68a.r2.dev'
RISQUE = re.compile(r'[×÷≠≤≥√²³⁴−±≈%½¼¾]|\d\s*[x*/:]\s*\d|\d\s*[=+<>-]\s*[\d?_]|\d+(?:[.,]\d+)?\s*(?:km|cm|mm|kg|m|g|l|h|°)\b')
CODES = {'fr': 'fr', 'en': 'en', 'es': 'es', 'de': 'de', 'it': 'it', 'pt': 'pt', 'ru': 'ru', 'uk': 'uk', 'ar': 'ar', 'zh': 'zh'}


def js_str(x):
    return json.loads('"' + x.replace('\\\'', "'").replace('"', '\\"') + '"') if '\\' in x else x


def cibles():
    out = []
    # 1) Questions / réponses du quiz (index.html) qui ont un enregistrement
    man = json.loads((ROOT / 'data/audio_textes.json').read_text())
    for f, m in json.loads((ROOT / 'data/audio_maths.json').read_text()).items():
        man.setdefault(f, {}).update(m)
    src = (ROOT / 'index.html').read_text(encoding='utf-8')
    vus = set()
    for m in re.finditer(r'\{id:["\']([A-Z0-9]+(?:-[A-Za-z0-9]+)+)["\'],[^\n]*', src):
        line = m.group(0)
        txts = [js_str(x) for x in re.findall(r'enonce:"((?:[^"\\]|\\.)*)"', line)]
        c = re.search(r'choix:\[([^\]]*)\]', line)
        if c:
            txts += [js_str(a or b) for a, b in re.findall(r'"((?:[^"\\]|\\.)*)"|\'((?:[^\'\\]|\\.)*)\'', c.group(1))]
        for t in txts:
            if not RISQUE.search(t) or t in vus:
                continue
            h = empreinte(t)
            for lang in ('fr', 'en', 'es'):
                k = man.get(lang, {}).get(h)
                if k:
                    vus.add(t); out.append(('quiz', lang, k, t, f'{CDN}/audio/{lang}/{k}.mp3')); break
    # 2) Cartes Flash (toutes les langues)
    for f in sorted((ROOT / 'data/flash').glob('*.json')):
        lang = f.stem
        if lang not in CODES:
            continue
        d = json.loads(f.read_text(encoding='utf-8'))
        cards = d if isinstance(d, list) else d.get('cards', [])
        for c in cards if isinstance(cards, list) else []:
            t = ' '.join(str(c.get(k, '')) for k in ('titre', 'texte', 'action'))
            if RISQUE.search(t):
                out.append(('flash', lang, c.get('id'), t, f"{CDN}/audio/flash/{lang}/{c.get('id')}_{lang.upper()}.mp3"))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--max', type=int, default=0)
    ap.add_argument('--liste', action='store_true')
    a = ap.parse_args()
    cs = cibles()
    if a.max:
        cs = cs[:a.max]
    from collections import Counter
    print(len(cs), Counter((c[0], c[1]) for c in cs))
    if a.liste:
        return
    import requests
    from faster_whisper import WhisperModel
    model = WhisperModel(os.environ.get('WHISPER_MODEL', 'small'), device='cpu', compute_type='int8')
    tmp = Path(tempfile.mkdtemp())
    out = ROOT / 'rapport_voix.csv'
    with open(out, 'w', newline='', encoding='utf-8') as fh:
        w = csv.writer(fh)
        w.writerow(['source', 'langue', 'cle', 'texte_affiche', 'voix_entendue'])
        for i, (srcn, lang, k, t, url) in enumerate(cs):
            r = requests.get(url, timeout=30)
            if r.status_code != 200 and srcn == 'flash':   # ancien nommage sans suffixe langue
                r = requests.get(url.replace(f'_{lang.upper()}.mp3', '.mp3'), timeout=30)
            if r.status_code != 200:
                w.writerow([srcn, lang, k, t, f'<<MP3 absent {r.status_code}>>']); continue
            p = tmp / 'a.mp3'; p.write_bytes(r.content)
            segs, _ = model.transcribe(str(p), language=CODES[lang], beam_size=5, vad_filter=False,
                                       initial_prompt=None, condition_on_previous_text=False)
            w.writerow([srcn, lang, k, t, ' '.join(s.text.strip() for s in segs)])
            if i % 50 == 0:
                print(f'{i + 1}/{len(cs)}', flush=True)
    print('✅', out)


if __name__ == '__main__':
    main()
