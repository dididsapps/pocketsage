"""Texte affiché -> texte à prononcer (symboles maths en mots) + empreinte du texte.
Même logique que _ttsParle / _atxHash dans index.html : garder les deux synchronisés."""
import re, unicodedata

SYMB = re.compile(r'[×÷≠≤≥√²³−±≈]')
# Textes à réenregistrer : symboles, trous « ___ » (lus « tiret bas »), soustraction « 7 - 4 » (le « - » est muet)
REDIRE = re.compile(r'[×÷≠≤≥√²³−±≈]|_{2,}|(?<=[\w)])\s+-\s+(?=[\w(])')

MOTS = {
    'FR': {'×': ' fois ', '÷': ' divisé par ', '≠': ' différent de ', '≤': ' inférieur ou égal à ', '≥': ' supérieur ou égal à ',
           '±': ' plus ou moins ', '≈': ' environ ', '−': ' moins ', '=': ' égale ', '+': ' plus ', '<': ' inférieur à ', '>': ' supérieur à ',
           '²': ' au carré', '³': ' au cube', '√': 'racine carrée de ', '%': ' pour cent', 'km²': ' kilomètres carrés', 'm²': ' mètres carrés',
           'cm²': ' centimètres carrés', 'm³': ' mètres cubes', 'cm³': ' centimètres cubes', '?': 'combien', '___': 'combien'},
    'EN': {'×': ' times ', '÷': ' divided by ', '≠': ' is not equal to ', '≤': ' is less than or equal to ', '≥': ' is greater than or equal to ',
           '±': ' plus or minus ', '≈': ' about ', '−': ' minus ', '=': ' equals ', '+': ' plus ', '<': ' is less than ', '>': ' is greater than ',
           '²': ' squared', '³': ' cubed', '√': 'the square root of ', '%': ' percent', 'km²': ' square kilometres', 'm²': ' square metres',
           'cm²': ' square centimetres', 'm³': ' cubic metres', 'cm³': ' cubic centimetres', '?': 'what', '___': 'what'},
    'ES': {'×': ' por ', '÷': ' dividido entre ', '≠': ' distinto de ', '≤': ' menor o igual que ', '≥': ' mayor o igual que ',
           '±': ' más o menos ', '≈': ' aproximadamente ', '−': ' menos ', '=': ' igual a ', '+': ' más ', '<': ' menor que ', '>': ' mayor que ',
           '²': ' al cuadrado', '³': ' al cubo', '√': 'la raíz cuadrada de ', '%': ' por ciento', 'km²': ' kilómetros cuadrados', 'm²': ' metros cuadrados',
           'cm²': ' centímetros cuadrados', 'm³': ' metros cúbicos', 'cm³': ' centímetros cúbicos', '?': 'cuánto', '___': 'cuánto'},
}

def parle(t: str, lang: str = 'FR') -> str:
    if not t or not (REDIRE.search(t) or re.search(r'\d\s*[=+<>]\s*[\d?_]', t)):
        return t
    M = MOTS.get((lang or 'FR')[:2].upper(), MOTS['FR'])
    s = t
    s = re.sub(r'(\d)\s*(km|cm|m)([²³])', lambda m: m.group(1) + M[m.group(2) + m.group(3)], s)
    maths = bool(re.search(r'\d|=', s))
    s = re.sub(r'_{2,}', (' ' + M['___'] + ' ') if maths else ' … ', s)   # trou : « combien » en calcul, sinon une pause
    s = re.sub(r'=\s*\?', ' ' + M['='].strip() + ' ' + M['?'] + ' ?', s)        # « = ? » -> « égale combien ? »
    s = re.sub(r'√\s*\(?([\w]+)\)?', lambda m: M['√'] + m.group(1), s)
    for k in ('×', '÷', '≠', '≤', '≥', '±', '≈', '−', '²', '³'):
        s = s.replace(k, M[k])
    s = re.sub(r'(?<=[\w)])\s*=\s*', M['='], s)
    s = re.sub(r'(?<=[\w)²])\s*\+\s*(?=[\w(])', M['+'], s)
    s = re.sub(r'(?<=[\w)²])\s+-\s+(?=[\w(])', M['−'], s)   # « 3-8-1-20 » (code) reste tel quel
    s = re.sub(r'(?<=[\w)])\s*<\s*(?=[\w(])', M['<'], s)
    s = re.sub(r'(?<=[\w)])\s*>\s*(?=[\w(])', M['>'], s)
    s = re.sub(r'(?<=\d)\s*%', M['%'], s)
    return re.sub(r'\s+', ' ', s).strip()

def norm(t: str) -> str:
    t = unicodedata.normalize('NFC', t).lower().replace('’', "'").replace('‘', "'")
    return re.sub(r'\s+', ' ', t).strip()

def empreinte(t: str) -> str:
    a = 0x811c9dc5; b = 5381
    for ch in norm(t):
        c = ord(ch); a = ((a ^ c) * 0x01000193) & 0xffffffff; b = ((b * 33) ^ c) & 0xffffffff
    return format(a, 'x') + format(b, 'x')

if __name__ == '__main__':
    for x in ["2 × 3 = ? (Attention : ≠ 2 + 3 !)", "Complète : 3 × 7 = ___", "Résous : √x = 5", "200 000 km²",
              "Si x = 3, quelle est la valeur de 2x² - 3x + 1 ?", "10² × 10³", "12 ÷ 4 = ?", "Quel est le plus grand entier n tel que n² < 200 ?",
              "Combien font 10 - 5 ?", "Complète : 'Je ___ à l'école.'", "Complète : ___ + 45 = 100", "Si le code de CHAT est 3-8-1-20"]:
        print(x, '→', parle(x))
