import json,os,sys
from render3d import render
from PIL import Image
S='/tmp/claude-0/-home-claude/a8977e66-ea58-56a5-906f-95854358b7d4/scratchpad/'
OUT=sys.argv[1];os.makedirs(OUT,exist_ok=True)
d=json.load(open(S+'interieurs.json'))
need=set()
for L in d['interieurs'].values():
    for it in L['items']:need.add((it['m'],it['rot']))
for m,nom,prix,cat,o in d['catalogue']:
    for rot in range(4):
        need.add((m,rot))
        if o.get('c'):
            for k in d['couleurs']:need.add((m+'~'+k,rot))
def hexc(h):return tuple(int(h[i:i+2],16)/255 for i in (1,3,5))
man={}
for m,rot in sorted(need):
    base,_,col=m.partition('~');rc=None
    if col:c=hexc(d['couleurs'][col]);rc={'carpet':c,'carpetDarker':tuple(x*.68 for x in c)}
    if m.startswith('shop:'):p=S+'packs/kenney_mini-shop_2.1/Models/OBJ format/'+m[5:]+'.obj';org='center';sc=1
    elif m.startswith('food:'):p=S+'packs/kenney_food-kit/Models/OBJ format/'+m[5:]+'.obj';org='center';sc=0.7
    else:p=S+'packs/kenney_furniture-kit/Models/OBJ format/'+base+'.obj';org='corner';sc=1
    name=m.replace(':','_').replace('~','-')+'_'+str(rot)
    info=render(p,OUT+'/'+name+'.png',org,rot,R=2,SS=3,scale=sc,recolor=rc)
    top=max(float(l.split()[2]) for l in open(p) if l.startswith('v '))*sc
    im=Image.open(OUT+'/'+name+'.png');im.save(OUT+'/'+name+'.webp',quality=88,method=6,lossless=False);os.remove(OUT+'/'+name+'.png')
    man[m+'|'+str(rot)]=[name,info['ax'],info['ay'],info['fw'],info['fh'],round(top,2)]
json.dump(man,open(OUT+'/sprites.json','w'),separators=(',',':'))
tot=sum(os.path.getsize(OUT+'/'+f) for f in os.listdir(OUT));print(len(man),'sprites',tot//1024,'Ko')
