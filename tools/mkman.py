import json
S=__import__("os").environ.get("TMPDIR","/tmp")+"/"
d=json.load(open(S+'stale.json'))
def norm(t):
    import re,unicodedata
    t=t.encode().decode('unicode_escape').encode('latin1').decode('utf-8') if '\\' in t else t
    t=unicodedata.normalize('NFC',t).lower().replace('’',"'")
    return re.sub(r'\s+',' ',t).strip()
def h(t):
    a=0x811c9dc5;b=5381
    for ch in t:
        c=ord(ch);a=((a^c)*0x01000193)&0xffffffff;b=((b*33)^c)&0xffffffff
    return format(a,'x')+format(b,'x')
out={}
for k,t in d['ok'].items():
    lang,key=k.split('/',1)
    out.setdefault(lang,{}).setdefault(h(norm(t)),key)
json.dump(out,open('/home/claude/pocketsage/data/audio_textes.json','w'),separators=(',',':'),ensure_ascii=False)
print({k:len(v) for k,v in out.items()})
print(norm("Comment s'appelle le continent des kangourous et koalas ?"),h(norm("Comment s'appelle le continent des kangourous et koalas ?")))
