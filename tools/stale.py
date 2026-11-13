import re,subprocess,json,os,sys
S=__import__("os").environ.get("TMPDIR","/tmp")+"/"
os.chdir('/home/claude/pocketsage')
# fichier -> commit le plus récent qui l'a ajouté/modifié
last={};cur=None
for l in open(S+'mp3log.txt'):
    l=l.strip()
    if l.startswith('C '):cur=l[2:];continue
    if l and l not in last:last[l]=cur
item_re=re.compile(r'\{id:"([A-Z]+-[A-Za-z0-9]+-\d+)",(.*?)\}(?=,\s*\n|\s*\])',re.S)
def items(src):
    d={}
    for m in re.finditer(r'\{id:["\']([A-Z0-9]+(?:-[A-Za-z0-9]+)+)["\'],[^\n]*',src):
        line=m.group(0);i=m.group(1)
        e=re.search(r'enonce:"((?:[^"\\]|\\.)*)"',line) or re.search(r"enonce:'((?:[^'\\]|\\.)*)'",line)
        c=re.search(r'choix:\[([^\]]*)\]',line)
        ch=re.findall(r'"((?:[^"\\]|\\.)*)"|\'((?:[^\'\\]|\\.)*)\'',c.group(1)) if c else []
        d.setdefault(i,{'e':e.group(1) if e else None,'c':[a or b for a,b in ch]})
    return d
now=items(open('index.html',encoding='utf-8').read())
cache={}
def at(h):
    if h not in cache:cache[h]=items(subprocess.run(['git','show',h+':index.html'],capture_output=True,text=True).stdout)
    return cache[h]
ok={};stale=[];noitem=0
for f,h in last.items():
    if not os.path.exists(f):continue
    b=os.path.basename(f)[:-4]
    m=re.match(r'(.+?)_(enonce|choix_(\d))$',b)
    if not m:
        continue
    fid,kind,n=m.group(1),m.group(2),m.group(3)
    lang=f.split('/')[1]
    cand=[fid]+([ 'LG-'+fid[3:]] if fid.startswith('FR-') else [])
    iid=next((x for x in cand if x in now),None)
    if not iid:noitem+=1;continue
    old=at(h).get(iid)
    key=lambda d:(d['e'] if kind=='enonce' else (d['c'][int(n)] if int(n)<len(d['c']) else None)) if d else None
    a,bb=key(now[iid]),key(old)
    if a is not None and a==bb: ok[lang+'/'+b]=a
    else: stale.append((lang+'/'+b,bb,a))
print('ok',len(ok),'stale',len(stale),'noitem',noitem)
for s in stale[:15]:print(s)
json.dump({'ok':ok,'stale':[s[0] for s in stale]},open(S+'stale.json','w'),ensure_ascii=False)
