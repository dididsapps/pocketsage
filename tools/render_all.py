import json,os,sys
from render3d import render
from PIL import Image
S='/tmp/claude-0/-home-claude/a8977e66-ea58-56a5-906f-95854358b7d4/scratchpad/'
OUT=sys.argv[1];os.makedirs(OUT,exist_ok=True)
d=json.load(open(S+'interieurs.json'))
need=set()
for L in d['interieurs'].values():
    for it in L['items']:need.add((it['m'],it['rot']))
man={}
for m,rot in sorted(need):
    if m.startswith('shop:'):p=S+'packs/kenney_mini-shop_2.1/Models/OBJ format/'+m[5:]+'.obj';org='center';sc=1
    elif m.startswith('food:'):p=S+'packs/kenney_food-kit/Models/OBJ format/'+m[5:]+'.obj';org='center';sc=0.7
    else:p=S+'packs/kenney_furniture-kit/Models/OBJ format/'+m+'.obj';org='corner';sc=1
    name=m.replace(':','_')+'_'+str(rot)
    info=render(p,OUT+'/'+name+'.png',org,rot,R=2,SS=3,scale=sc)
    im=Image.open(OUT+'/'+name+'.png');im.save(OUT+'/'+name+'.webp',quality=88,method=6,lossless=False);os.remove(OUT+'/'+name+'.png')
    man[m+'|'+str(rot)]=[name,info['ax'],info['ay'],info['fw'],info['fh']]
json.dump(man,open(OUT+'/sprites.json','w'),separators=(',',':'))
tot=sum(os.path.getsize(OUT+'/'+f) for f in os.listdir(OUT));print(len(man),'sprites',tot//1024,'Ko')
