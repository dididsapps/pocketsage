import re,json
def js(x):
    try:return json.loads('"'+x.replace("\\'","'")+'"')
    except Exception:return x
def arr(l,key):
    """lit le tableau key:[...] en respectant les chaînes"""
    i=l.find(key+':[')
    if i<0:return None
    j=i+len(key)+2;out=[];
    while j<len(l):
        ch=l[j]
        if ch==']':return out
        if ch in '"\'':
            q=ch;k=j+1;buf=''
            while k<len(l) and l[k]!=q:
                if l[k]=='\\':buf+=l[k:k+2];k+=2;continue
                buf+=l[k];k+=1
            out.append(js(buf) if q=='"' else buf.replace("\\'","'"));j=k+1;continue
        j+=1
    return out
def field(l,key):
    m=re.search(key+r':"((?:[^"\\]|\\.)*)"',l)
    return js(m.group(1)) if m else None
def items(s):
    for m in re.finditer(r'\{id:"([A-Z]{2}-[A-Z0-9]+-\d+)",([^\n]*)',s):
        yield m.group(1),m.group(2),m.start(),m.end()

import os as _os
_ROOT=_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
SOURCES=['index.html','js/questions-plus-data.js']
def texte_questions():
    """Toutes les sources de questions (index.html + compléments)."""
    return '\n'.join(open(_os.path.join(_ROOT,f),encoding='utf-8').read() for f in SOURCES if _os.path.exists(_os.path.join(_ROOT,f)))
