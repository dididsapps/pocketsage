// PocketSage — Mon Monde : intérieurs des bâtiments (13/11/2026)
// 3 couches : la ville → le bâtiment en coupe (plan entier) → une pièce (zoom).
// Meubles : Kenney Furniture Kit / Mini Shop / Food Kit (CC0), rendus en isométrique par script (assets/interieur).
// Données : data/interieurs.json (plans, meubles, actions). L'avatar marche (BFS), s'assoit, dort, mange…
(function(){
'use strict';
const TW=64,TH=32,VZ=39.19,WALL=58,CUT=20,AV=46; // px (zoom 1) : case, hauteur d'une unité, mur du fond, cloison coupée, taille avatar
const VER=(document.querySelector('script[src*="monde-interieur"]')||{src:''}).src.split('v=')[1]||'1';
let DATA=null,SPR=null;const IMG={};let ST=null;
const SOLS={bois:['#d9a066','#cf955a'],boisFonce:['#8c5a3c','#7d4f34'],carreau:['#ece6da','#d8d0c0'],carreauBleu:['#d4ecf3','#bfe0ea'],moquette:['#b9c7ea','#b0bee2'],
  moquetteBeige:['#e8d9bf','#e0cfb2'],marbreBlanc:['#f6f4f0','#ece8e0'],marbreNoir:['#2a2a30','#34343b'],damier:['#f3efe6','#2c2a2a'],parquetChevron:['#b9824f','#a8723f'],tek:['#d8b98e','#ccab7e'],verre:['#7fd3e0','#6cc6d6'],marbre:['#f2f0ec','#e2ded6'],clair:['#f3ece2','#ebe2d5'],lino:['#e3e7ea','#d6dce0'],blancBleu:['#eef5fb','#e0ebf5']};
function load(){if(DATA)return Promise.resolve();
  return Promise.all([fetch('data/interieurs.json?v='+VER).then(r=>r.json()),fetch('assets/interieur/sprites.json?v='+VER).then(r=>r.json())]).then(([d,s])=>{DATA=d;SPR=s;});}
function img(n){if(!IMG[n]){const i=new Image();i.onload=()=>{i.ok=1;};i.src='assets/interieur/'+n+'.webp?v='+VER;IMG[n]=i;}return IMG[n];}
const W3=()=>window.__w3&&window.__w3.W3;
function has(id){return !!(DATA&&DATA.batiments[id]);}
// ── géométrie ──
function P(u,v,z){return [(u-v)*TW/2,(u+v)*TH/2-(z||0)];}
function poly(c,pts,fill,stroke,lw){c.beginPath();pts.forEach((p,i)=>i?c.lineTo(p[0],p[1]):c.moveTo(p[0],p[1]));c.closePath();if(fill){c.fillStyle=fill;c.fill();}if(stroke){c.strokeStyle=stroke;c.lineWidth=lw||1;c.stroke();}}
function key(c,r){return c+','+r;}
const ACT_RULES=[[/Sofa|loungeChair|bench/i,'SOFA'],[/^bed/i,'BED'],[/Fridge/i,'FRIDGE'],[/Stove/i,'STOVE'],[/^table(?!Coffee)/i,'EAT'],[/television/i,'TV'],[/^bookcase/i,'READ'],
  [/^desk/i,'DESK'],[/bathtub|shower/i,'BATH'],[/^toilet/i,'WC'],[/Sink/i,'WASH'],[/^bear/i,'TOY'],[/speaker|radio/i,'MUSIC'],[/laptop|computerScreen/i,'DESK']];
function autoAct(m){const b=m.split('~')[0];for(const [re,k] of ACT_RULES)if(re.test(b))return DATA.actions[k];return null;}
function build(L,list){
  const S={L,items:[],block:{},seats:{},walls:new Set(),w:L.w,h:L.h,list};
  list.forEach((it,i)=>{let sp=SPR[it.m+'|'+it.rot];if(!sp&&it.m[0]==='@')sp=[null,0,0,it.fw||1,it.fh||1,.5];if(!sp)return;const o={...it,act:it.act||(it.buy?autoAct(it.m):null),sp,fw:sp[3],fh:sp[4],i};S.items.push(o);if(sp[0])img(sp[0]);
    o.seat=/^(chair|stool)/i.test(it.m);if(o.seat)S.seats[key(it.c,it.r)]=o;
    if(!it.flat&&!it.deco&&!o.seat&&!/^plantSmall/.test(it.m))for(let a=0;a<o.fw;a++)for(let b=0;b<o.fh;b++)S.block[key(it.c+a,it.r+b)]=o;});
  (L.cloisons||[]).forEach(([ax,k,f,t,doors])=>{for(let x=f;x<t;x++){if(doors.includes(x))continue;
    if(ax==='c')S.walls.add(key(k-1,x)+'|'+key(k,x));else S.walls.add(key(x,k-1)+'|'+key(x,k));}});
  return S;}
function wallBetween(S,a,b){return S.walls.has(key(a[0],a[1])+'|'+key(b[0],b[1]))||S.walls.has(key(b[0],b[1])+'|'+key(a[0],a[1]));}
function free(S,c,r){return c>=0&&r>=0&&c<S.w&&r<S.h&&!S.block[key(c,r)];}
function bfs(S,from,goal){ // goal(c,r) -> bool
  const q=[[from.c,from.r]],prev={};prev[key(from.c,from.r)]=null;
  while(q.length){const [c,r]=q.shift();if(goal(c,r)){const path=[];let k=key(c,r);while(prev[k]!==null&&prev[k]!==undefined){const [a,b]=k.split(',').map(Number);path.unshift({c:a,r:b});k=prev[k];}return path;}
    for(const [dc,dr] of [[1,0],[-1,0],[0,1],[0,-1]]){const n=[c+dc,r+dr],nk=key(n[0],n[1]);if(nk in prev||!free(S,n[0],n[1])||wallBetween(S,[c,r],n))continue;prev[nk]=key(c,r);q.push(n);}}
  return null;}
// ── ouverture / fermeture ──
// Maisons de l'enfant : au départ seulement l'essentiel (lit, cuisine, salle de bain, canapé, table…)
// pour laisser de la place à SA déco. Les bâtiments « métier » (hôtels, magasins…) restent meublés.
const MAISONS_LEGERES=['maison','villa','chateau'];
function leger(list){
  const ESS=/^(@piscine|kitchenSink|hood|toilet|bathtub|shower|bathroomSink|chair|stool)/;
  const keep=list.filter(x=>x.act||ESS.test(x.m));
  // garder le meuble-support sous un objet conservé (ex. meuble télé sous la télé)
  keep.filter(x=>x.z).forEach(t=>{const b=list.find(y=>!y.z&&y.c===t.c&&y.r===t.r);if(b&&!keep.includes(b))keep.push(b);});
  return list.filter(x=>keep.includes(x));}
function open(bid,bk){
  return load().then(()=>{
    const lid=DATA.batiments[bid];if(!lid)return false;const L=DATA.interieurs[lid];
    const W=W3(),cell=bk&&W&&W.grid[bk];
    let list=(L.deco&&cell&&Array.isArray(cell.deco))?cell.deco.map(x=>({...x})):L.items.map(x=>({...x}));
    if(L.deco&&!(cell&&Array.isArray(cell.deco))&&MAISONS_LEGERES.includes(lid))list=leger(list);
    const S=build(L,list);const p=L.porte||[0,0];
    ST={S,bid,lid,bk,cell,pos:{c:p[0],r:p[1]},path:[],t:0,dir:[0,1],walk:0,busy:null,floats:[],cam:{x:0,y:0,z:1},sel:null,deco:false,pick:null,moving:false};
    ui();fit();loop();return true;});
}
function close(){if(!ST)return;ST=null;const o=document.getElementById('int-ov');if(o)o.remove();try{window.__w3.save();window.__w3.hud();}catch(e){}}
function ui(){
  let o=document.getElementById('int-ov');if(o)o.remove();
  o=document.createElement('div');o.id='int-ov';
  const L=ST.S.L;
  o.innerHTML=`<div class="int-top"><button class="int-out" id="int-out">⬅ Sortir</button><b class="int-nom">${L.nom}</b><span class="int-coins" id="int-coins"></span>${L.deco?'<button class="int-deco" id="int-deco">🛋️ Déco</button>':''}</div>
  <div class="int-bars" id="int-bars"></div>
  <div class="int-rooms" id="int-rooms"><button data-room="-1" class="on">🏠 Tout</button>${(L.pieces||[]).map((p,i)=>`<button data-room="${i}">${p[0]}</button>`).join('')}</div>
  <canvas id="int-cv"></canvas>
  <div class="int-tip" id="int-tip">Touche un meuble pour agir 👆 ou le sol pour te déplacer</div>`;
  document.body.appendChild(o);
  o.querySelector('#int-out').onclick=close;
  const db=o.querySelector('#int-deco');if(db)db.onclick=()=>decoMode(!ST.deco);
  o.querySelectorAll('[data-room]').forEach(b=>b.onclick=()=>{o.querySelectorAll('[data-room]').forEach(x=>x.classList.remove('on'));b.classList.add('on');const i=+b.dataset.room;if(i<0)fit();else zoomRoom(L.pieces[i]);});
  const cv=o.querySelector('#int-cv');ST.cv=cv;resize();
  let down=null,moved=false,pinch=null;
  cv.addEventListener('pointerdown',e=>{down={x:e.clientX,y:e.clientY,cx:ST.cam.x,cy:ST.cam.y};moved=false;cv.setPointerCapture(e.pointerId);});
  cv.addEventListener('pointermove',e=>{if(!down||pinch)return;const dx=e.clientX-down.x,dy=e.clientY-down.y;if(Math.abs(dx)+Math.abs(dy)>8)moved=true;if(moved){ST.cam.x=down.cx+dx;ST.cam.y=down.cy+dy;}});
  cv.addEventListener('pointerup',e=>{if(down&&!moved&&!pinch){const r=cv.getBoundingClientRect();tap(e.clientX-r.left,e.clientY-r.top);}down=null;});
  cv.addEventListener('touchstart',e=>{if(e.touches.length===2){const d=Math.hypot(e.touches[0].clientX-e.touches[1].clientX,e.touches[0].clientY-e.touches[1].clientY);pinch={d,z:ST.cam.z};}},{passive:true});
  cv.addEventListener('touchmove',e=>{if(pinch&&e.touches.length===2){const d=Math.hypot(e.touches[0].clientX-e.touches[1].clientX,e.touches[0].clientY-e.touches[1].clientY);zoomAt(Math.max(.6,Math.min(3.2,pinch.z*d/pinch.d)));}},{passive:true});
  cv.addEventListener('touchend',()=>{setTimeout(()=>{pinch=null;},50);});
  cv.addEventListener('wheel',e=>{e.preventDefault();zoomAt(Math.max(.6,Math.min(3.2,ST.cam.z*(e.deltaY<0?1.1:0.9))));},{passive:false});
  window.addEventListener('resize',resize);
  bars();
}
function resize(){if(!ST||!ST.cv)return;const cv=ST.cv,dpr=Math.min(2,window.devicePixelRatio||1),w=cv.clientWidth,h=cv.clientHeight;cv.width=w*dpr;cv.height=h*dpr;ST.dpr=dpr;}
function bounds(u0,v0,u1,v1){const pts=[P(u0,v0,WALL),P(u1,v0,WALL),P(u0,v1,WALL),P(u1,v1,0),P(u0,v1,0),P(u1,v0,0)];
  return [Math.min(...pts.map(p=>p[0])),Math.min(...pts.map(p=>p[1])),Math.max(...pts.map(p=>p[0])),Math.max(...pts.map(p=>p[1]))];}
function frame(b,maxZ){const cv=ST.cv,w=cv.clientWidth,h=cv.clientHeight;const z=Math.max(.6,Math.min(maxZ||2.4,Math.min((w-24)/(b[2]-b[0]),(h-24)/(b[3]-b[1]))));
  ST.cam.z=z;ST.cam.x=w/2-(b[0]+b[2])/2*z;ST.cam.y=h/2-(b[1]+b[3])/2*z;}
function fit(){frame(bounds(0,0,ST.S.w,ST.S.h),2);}
function zoomRoom(p){const u=p[1],v=p[2];frame(bounds(Math.max(0,u-2),Math.max(0,v-2),Math.min(ST.S.w,u+2),Math.min(ST.S.h,v+2)),3);}
function zoomAt(z){const cv=ST.cv,w=cv.clientWidth/2,h=cv.clientHeight/2;const wx=(w-ST.cam.x)/ST.cam.z,wy=(h-ST.cam.y)/ST.cam.z;ST.cam.z=z;ST.cam.x=w-wx*z;ST.cam.y=h-wy*z;}
// ── écran → case ──
function toCell(sx,sy){const x=(sx-ST.cam.x)/ST.cam.z,y=(sy-ST.cam.y)/ST.cam.z;const u=(x/(TW/2)+y/(TH/2))/2,v=(y/(TH/2)-x/(TW/2))/2;return {c:Math.floor(u),r:Math.floor(v),u,v};}
function itemAt(sx,sy,any){ // priorité : objet dessiné sous le doigt (le plus en avant)
  const x=(sx-ST.cam.x)/ST.cam.z,y=(sy-ST.cam.y)/ST.cam.z;let best=null;
  ST.S.items.forEach(o=>{if((!o.act&&!any)||o.flat)return;const sp=o.sp,im=IMG[sp[0]];if(!im||!im.ok)return;const p=P(o.c,o.r,(o.z||0)*VZ),x0=p[0]-sp[1]/2,y0=p[1]-sp[2]/2,w=im.width/2,h=im.height/2;
    if(x>=x0&&x<=x0+w&&y>=y0&&y<=y0+h){const d=o.c+o.r+(o.fw+o.fh)/2+(o.deco?.5:0);if(!best||d>best.d)best={o,d};}});
  return best&&best.o;}
function tap(sx,sy){
  if(!ST||ST.busy)return;
  if(ST.deco){decoTap(sx,sy);return;}
  let o=itemAt(sx,sy);
  if(!o){const q=toCell(sx,sy),b=ST.S.block[key(q.c,q.r)];if(b&&b.act)o=b;}
  if(o){goItem(o);return;}
  const {c,r}=toCell(sx,sy);if(!free(ST.S,c,r))return;
  const p=bfs(ST.S,ST.pos,(a,b)=>a===c&&b===r);if(p){ST.path=p;ST.t=0;ST.target=null;}
}
function goItem(o){
  const base=o.deco?(ST.S.block[key(o.c,o.r)]||o):o;
  const cells=new Set();for(let a=0;a<base.fw;a++)for(let b=0;b<base.fh;b++)cells.add(key(base.c+a,base.r+b));
  const near=(c,r)=>[[1,0],[-1,0],[0,1],[0,-1]].some(([dc,dr])=>cells.has(key(c+dc,r+dr))&&!wallBetween(ST.S,[c,r],[c+dc,r+dr]));
  let p=null;const wantSeat=o.act&&(o.act.pose==='sit'||o.act.pose==='eat');
  if(wantSeat)p=bfs(ST.S,ST.pos,(c,r)=>!!ST.S.seats[key(c,r)]&&near(c,r));
  if(!p)p=bfs(ST.S,ST.pos,near);
  if(!p){msg('Je ne peux pas aller jusque-là 🤔');return;}
  ST.path=p;ST.t=0;ST.target={o,base};
  if(!p.length)arrive();
}
function arrive(){
  const T=ST.target;ST.target=null;if(!T)return;const a=T.o.act,W=W3();const L=W&&W.life;
  if(a.c&&W&&W.coins<a.c){msg('Pas assez de 🪙 pour : '+a.t+' ('+a.c+'🪙)');return;}
  // se tourner vers le meuble
  const b=T.base,cx=b.c+b.fw/2,cy=b.r+b.fh/2;const dx=cx-(ST.pos.c+.5),dy=cy-(ST.pos.r+.5);ST.dir=Math.abs(dx)>Math.abs(dy)?[Math.sign(dx),0]:[0,Math.sign(dy)];
  ST.busy={a,o:b,t0:performance.now(),dur:(a.dur||2)*1000,pose:a.pose||'idle'};
  setTip(a.t+'…');
}
function finish(){
  const B=ST.busy;ST.busy=null;const a=B.a,W=W3();const L=W&&W.life;
  if(W){if(a.c)W.coins-=a.c;const cl=v=>Math.max(0,Math.min(100,v));if(L){if(a.f)L.faim=cl(L.faim+a.f);if(a.e)L.energie=cl(L.energie+a.e);if(a.j)L.joie=cl(L.joie+a.j);}}
  const p=P(ST.pos.c+.5,ST.pos.r+.5,AV+8);
  const parts=[];if(a.f)parts.push((a.f>0?'+':'')+a.f+' 🍔');if(a.e)parts.push((a.e>0?'+':'')+a.e+' ⚡');if(a.j)parts.push((a.j>0?'+':'')+a.j+' 😊');if(a.c)parts.push('−'+a.c+'🪙');
  ST.floats.push({x:p[0],y:p[1],text:parts.join('  '),life:110});
  try{sndStar();}catch(e){}
  bars();setTip('Bravo ! Touche un autre meuble 👆');
  try{window.__w3.save();window.__w3.hud();window.__w3.panel();}catch(e){}
  if(a.module){setTimeout(()=>{if(!ST)return;showModuleChoice();},400);}
}
function showModuleChoice(){
  const o=document.getElementById('int-ov');if(!o)return;let m=o.querySelector('.int-mod');if(m)m.remove();
  m=document.createElement('div');m.className='int-mod';
  m.innerHTML=`<b>✏️ Quelle activité ?</b><div><button data-m="maths">🔢 Maths</button><button data-m="savoirs">🔬 Sciences</button><button data-m="langues">🌍 Langues</button><button data-m="politesse">🌸 Politesse</button></div><button class="int-x">Plus tard</button>`;
  o.appendChild(m);m.querySelector('.int-x').onclick=()=>m.remove();
  m.querySelectorAll('[data-m]').forEach(b=>b.onclick=()=>{const k=b.dataset.m;close();try{if(k==='maths'){(APP.tabKey=APP.tabKey||{}).savoirs='maths';openMod('savoirs');}else openMod(k);}catch(e){}});
}
function msg(t){try{window.__w3.msg(t);}catch(e){}setTip(t);}
function setTip(t){const el=document.getElementById('int-tip');if(el)el.textContent=t;}
function bars(){const W=W3();const L=W&&W.life;const el=document.getElementById('int-bars');if(!el)return;
  const b=(ic,v,col)=>`<span class="ib"><i>${ic}</i><span><em style="width:${Math.round(v||0)}%;background:${col}"></em></span></span>`;
  el.innerHTML=L?b('🍔',L.faim,'#f4a261')+b('⚡',L.energie,'#4cc9f0')+b('😊',L.joie,'#ffd166'):'';
  const c=document.getElementById('int-coins');if(c&&W)c.textContent='🪙 '+Math.floor(W.coins);}
// ── avatar ──
const AVS={};function avSheet(n){if(!AVS[n]){const i=new Image();i.onload=()=>{i.ok=1;};i.src='assets/interieur/andrew_'+n+'.webp?v='+VER;AVS[n]=i;}return AVS[n];}
function useSprites(){try{const p=window.P&&window.P();return !p||!p.avatarId||p.avatarId==='boy1';}catch(e){return true;}}
let FALL=null;function fallback(){if(FALL)return FALL;const i=new Image();try{const p=window.P();let src=null;if(p&&p.avatarId){if(p.avatarId==='boy1')src=IMG_AVATAR_BOY1;else{const a=PNG_AVATARS.find(x=>x.id===p.avatarId);if(a)src=_GH+a.f;}}if(src){i.onload=()=>{i.ok=1;};i.src=src;}}catch(e){}FALL=i;return i;}
function drawAvatar(c,x,y,pose,frameIdx,flip,lift){
  if(pose!=='sleep'){c.save();c.fillStyle='rgba(0,0,0,.22)';c.beginPath();c.ellipse(x,y,10,4.5,0,0,7);c.fill();c.restore();}
  if(useSprites()){const sheet=pose==='walkF'?avSheet('walk_front'):pose==='walkB'?avSheet('walk_back'):avSheet('poses');
    const fi=pose==='walkF'||pose==='walkB'?frameIdx%6:{idle:0,sit:1,sleep:2,eat:3,wave:4,jump:5}[pose]||0;
    if(sheet.ok){if(pose==='sleep'){const s=AV*.9;c.save();c.translate(x,y-(lift||0));if(flip)c.scale(-1,1);c.drawImage(sheet,fi*256,0,256,256,-s*128/256,-s*160/256,s,s);c.restore();return;}
      c.save();c.translate(x,y-(lift||0));if(flip)c.scale(-1,1);c.drawImage(sheet,fi*256,0,256,256,-AV/2,-AV*246/256,AV,AV);c.restore();return;}}
  const f=fallback();if(f.ok){const h=AV*.95,w=h*f.width/f.height;c.save();c.translate(x,y-(lift||0)-Math.abs(Math.sin(frameIdx*1.05))*2);if(flip)c.scale(-1,1);c.drawImage(f,-w/2,-h,w,h);c.restore();}
  else{c.font='26px serif';c.textAlign='center';c.fillStyle='#000';c.fillText('🧒',x,y-(lift||0));}
}
// ── boucle ──
let raf=0;
function loop(){cancelAnimationFrame(raf);const step=()=>{if(!ST)return;update();draw();raf=requestAnimationFrame(step);};raf=requestAnimationFrame(step);}
function update(){
  if(ST.busy){if(performance.now()-ST.busy.t0>ST.busy.dur)finish();}
  else if(ST.path.length){ST.t+=0.055;ST.walk+=0.18;const n=ST.path[0];ST.dir=[n.c-ST.pos.c,n.r-ST.pos.r];
    if(ST.t>=1){ST.t=0;ST.pos=ST.path.shift();if(!ST.path.length&&ST.target)arrive();}}
  ST.floats.forEach(f=>{f.life--;f.y-=.35;});ST.floats=ST.floats.filter(f=>f.life>0);
  if(ST.n===undefined||++ST.n%60===0)bars();
}
function floorCol(L,c,r){let t='bois';(L.sols||[]).forEach(([u0,v0,u1,v1,k])=>{if(c>=u0&&c<u1&&r>=v0&&r<v1)t=k;});const s=SOLS[t]||SOLS.bois;return {t,col:s[(c+r)%2]};}
function draw(){
  const cv=ST.cv,c=cv.getContext('2d'),S=ST.S,L=S.L,dpr=ST.dpr||1;
  c.setTransform(1,0,0,1,0,0);c.fillStyle='#1d2433';c.fillRect(0,0,cv.width,cv.height);
  c.setTransform(dpr*ST.cam.z,0,0,dpr*ST.cam.z,dpr*ST.cam.x,dpr*ST.cam.y);
  // sol
  for(let r=0;r<S.h;r++)for(let k=0;k<S.w;k++){const f=floorCol(L,k,r);poly(c,[P(k,r),P(k+1,r),P(k+1,r+1),P(k,r+1)],f.col);
    if(f.t.startsWith('bois')){c.strokeStyle='rgba(90,50,20,.18)';c.lineWidth=.6;c.beginPath();for(let q=1;q<4;q++){const a=P(k,r+q/4),b=P(k+1,r+q/4);c.moveTo(a[0],a[1]);c.lineTo(b[0],b[1]);}c.stroke();}
    else if(f.t==='verre'){const t=performance.now()/1000,q=P(k+.5,r+.5);c.save();c.font='9px serif';c.textAlign='center';c.globalAlpha=.8;c.fillText(['🐠','🐟','🐡'][(k+r)%3],q[0]+Math.sin(t+k)*10,q[1]+Math.cos(t*.8+r)*4);c.restore();
      poly(c,[P(k,r),P(k+1,r),P(k+1,r+1),P(k,r+1)],'rgba(255,255,255,.18)','rgba(255,255,255,.7)',1);}
    else if(f.t==='parquetChevron'){c.strokeStyle='rgba(70,35,10,.22)';c.lineWidth=.6;c.beginPath();for(let q=0;q<4;q++){const a=P(k+q/4,r),b=P(k+q/4+.25,r+.5),d=P(k+q/4,r+1);c.moveTo(a[0],a[1]);c.lineTo(b[0],b[1]);c.lineTo(d[0],d[1]);}c.stroke();}
    else if(f.t==='marbreBlanc'||f.t==='marbreNoir'||f.t==='damier'){poly(c,[P(k,r),P(k+1,r),P(k+1,r+1),P(k,r+1)],null,f.t==='marbreBlanc'?'rgba(212,175,55,.35)':'rgba(212,175,55,.55)',.8);
      c.strokeStyle='rgba(255,255,255,.12)';c.lineWidth=.5;c.beginPath();const a=P(k+.2,r+.3),b=P(k+.7,r+.6);c.moveTo(a[0],a[1]);c.quadraticCurveTo((a[0]+b[0])/2+4,(a[1]+b[1])/2,b[0],b[1]);c.stroke();}
    else if(f.t.startsWith('carreau')||f.t==='marbre'){c.strokeStyle='rgba(0,0,0,.07)';c.lineWidth=.6;poly(c,[P(k,r),P(k+1,r),P(k+1,r+1),P(k,r+1)],null,'rgba(0,0,0,.08)',.6);}}
  // bord avant (épaisseur du plancher)
  poly(c,[P(0,S.h),P(S.w,S.h),P(S.w,S.h,-8),P(0,S.h,-8)],'#6b4f3a');poly(c,[P(S.w,0),P(S.w,S.h),P(S.w,S.h,-8),P(S.w,0,-8)],'#57402f');
  // murs du fond
  wallBack(c,L,S);
  // tapis
  S.items.filter(o=>o.flat).forEach(o=>sprite(c,o));
  // noms des pièces (discrets, au sol)
  (L.pieces||[]).forEach(p=>{const q=P(p[1],p[2]);c.font='bold 8px sans-serif';c.fillStyle='rgba(0,0,0,.22)';c.textAlign='center';c.fillText(p[0].toUpperCase(),q[0],q[1]);});
  // objets triés + cloisons + avatar
  const D=[];
  S.items.forEach(o=>{if(!o.flat)D.push([o.c+o.r+(o.fw+o.fh)/2-1+(o.deco?.3+(o.z||0)*.01:0),()=>sprite(c,o)]);});
  (L.cloisons||[]).forEach(([ax,k,f,t,doors])=>{for(let x=f;x<t;x++){if(doors.includes(x))continue;if(ax==='c')D.push([k+x-.5+.02,()=>cut(c,[k,x],[k,x+1],'c')]);else D.push([x+k-.5+.02,()=>cut(c,[x,k],[x+1,k],'r')]);}});
  // avatar
  let ax=ST.pos.c+.5,ay=ST.pos.r+.5,pose='idle',lift=0,flip=false;
  if(ST.path.length&&!ST.busy){ax+=(ST.path[0].c-ST.pos.c)*ST.t;ay+=(ST.path[0].r-ST.pos.r)*ST.t;}
  const [dc,dr]=ST.dir;const back=dc<0||dr<0;flip=dc>0||dr<0;
  if(ST.path.length&&!ST.busy)pose=back?'walkB':'walkF';
  let dk=ax+ay-1+.15;
  if(ST.busy){pose=ST.busy.pose;const b=ST.busy.o;
    if(pose==='sit'&&/Sofa|Chair|bench|stool|chair/i.test(b.m)){ax=b.c+b.fw/2;ay=b.r+b.fh/2;lift=11;dk=b.c+b.r+(b.fw+b.fh)/2-1+.2;flip=b.rot===1||b.rot===2;}
    else if(pose==='sleep'&&/bed/i.test(b.m)){ax=b.c+b.fw/2;ay=b.r+b.fh/2;lift=(b.sp[5]||.38)*VZ-2;flip=b.rot===1||b.rot===3;dk=b.c+b.r+(b.fw+b.fh)/2-1+.2;}
    else if((pose==='sit'||pose==='eat')&&ST.S.seats[key(ST.pos.c,ST.pos.r)]){const ch=ST.S.seats[key(ST.pos.c,ST.pos.r)];pose='sit';lift=9;dk=ch.c+ch.r-1+.25;flip=ch.rot===1;}
    else if(pose==='sit')pose='idle';
    if(pose==='jump')lift=Math.abs(Math.sin(performance.now()/180))*8;}
  const fr=Math.floor(ST.walk);
  D.push([dk,()=>{const p=P(ax,ay);drawAvatar(c,p[0],p[1],pose,fr,flip,lift);
    if(ST.busy){const k=Math.min(1,(performance.now()-ST.busy.t0)/ST.busy.dur);const q=[p[0],p[1]-AV-14];c.fillStyle='rgba(255,255,255,.92)';c.beginPath();c.roundRect(q[0]-22,q[1]-7,44,9,4);c.fill();
      c.fillStyle='#2b9348';c.beginPath();c.roundRect(q[0]-20,q[1]-5,40*k,5,3);c.fill();}}]);
  D.sort((a,b)=>a[0]-b[0]).forEach(d=>d[1]());
  // tableau de classe « fantôme » sur le mur avant (on voit au travers)
  if(L.tableauAvant){const [a,b]=L.tableauAvant,hh=S.h;c.globalAlpha=.42;poly(c,[P(a,hh,14),P(b,hh,14),P(b,hh,48),P(a,hh,48)],'#1b4332','#8d6e63',2);c.globalAlpha=1;
    const o=P((a+b)/2,hh,33);c.save();c.transform(.894,.447,0,1,o[0],o[1]);c.font='bold 8px sans-serif';c.fillStyle='rgba(255,255,255,.85)';c.textAlign='center';c.fillText('2 + 3 = 5   Bonjour !',0,0);c.restore();}
  lustres(c,L);
  if(ST.deco)decoDraw(c);
  // textes flottants
  ST.floats.forEach(f=>{c.globalAlpha=Math.min(1,f.life/40);c.font='bold 9px sans-serif';c.textAlign='center';c.lineWidth=3;c.strokeStyle='rgba(0,0,0,.55)';c.strokeText(f.text,f.x,f.y);c.fillStyle='#fff';c.fillText(f.text,f.x,f.y);c.globalAlpha=1;});
}
function sprite(c,o){if(o.m[0]==='@'){const f=PROC[o.m.slice(1)];if(f)f(c,o);return;}const sp=o.sp,im=IMG[sp[0]];if(!im||!im.ok)return;const p=P(o.c,o.r,(o.z||0)*VZ);c.drawImage(im,p[0]-sp[1]/2,p[1]-sp[2]/2,im.width/2,im.height/2);}
function wallBack(c,L,S){
  const H=WALL,col=L.mur||'#f4efe6',top=L.murHaut||'#e2a56b';
  // mur le long de r=0 (haut-droit) et c=0 (haut-gauche)
  poly(c,[P(0,0),P(S.w,0),P(S.w,0,H),P(0,0,H)],shade(col,-6));
  poly(c,[P(0,0),P(0,S.h),P(0,S.h,H),P(0,0,H)],col);
  // plinthes
  poly(c,[P(0,0),P(S.w,0),P(S.w,0,4),P(0,0,4)],shade(col,-30));poly(c,[P(0,0),P(0,S.h),P(0,S.h,4),P(0,0,4)],shade(col,-24));
  wallMotif(c,L,S);
  // fenêtres sur le mur du fond (sauf si le décor mural est défini)
  if(!L.murDeco)for(let k=1;k<S.w-1;k+=3){if(L.tableau&&k>=2&&k<=5)continue;const a=k+.25,b=k+1.25;poly(c,[P(a,0,22),P(b,0,22),P(b,0,48),P(a,0,48)],'#ffffff');poly(c,[P(a+.06,0,24),P(b-.06,0,24),P(b-.06,0,46),P(a+.06,0,46)],'#9fd3f0');
    c.strokeStyle='#fff';c.lineWidth=1.2;c.beginPath();const m1=P((a+b)/2,0,24),m2=P((a+b)/2,0,46);c.moveTo(m1[0],m1[1]);c.lineTo(m2[0],m2[1]);c.stroke();}
  // tableau de l'école
  if(L.tableau){poly(c,[P(2.3,0,16),P(5.7,0,16),P(5.7,0,46),P(2.3,0,46)],'#8d6e63');poly(c,[P(2.4,0,18),P(5.6,0,18),P(5.6,0,44),P(2.4,0,44)],'#2d6a4f');
    const o=P(4,0,33);c.save();c.transform(.894,.447,0,1,o[0],o[1]);c.font='bold 7px sans-serif';c.fillStyle='rgba(255,255,255,.9)';c.textAlign='center';c.fillText('2 + 3 = 5   Bonjour !',0,0);c.restore();}
  murDeco(c,L);
  // porte d'entrée sur le mur c=0
  const pr=(L.porte||[0,0])[1];poly(c,[P(0,pr+.15),P(0,pr+.85),P(0,pr+.85,40),P(0,pr+.15,40)],'#8d5a3b');poly(c,[P(0,pr+.2),P(0,pr+.8),P(0,pr+.8,37),P(0,pr+.2,37)],'#a86b45');
  const kn=P(0,pr+.72,20);c.fillStyle='#ffd166';c.beginPath();c.arc(kn[0],kn[1],1.4,0,7);c.fill();
  // chaperon
  poly(c,[P(0,0,H),P(S.w,0,H),P(S.w,-.12,H+2),P(-.12,-.12,H+2)],top);poly(c,[P(0,0,H),P(0,S.h,H),P(-.12,S.h,H+2),P(-.12,-.12,H+2)],shade(top,10));
}
function cut(c,a,b,ax){ // cloison coupée (style « vue en coupe »)
  const t=.06,h=CUT,col=ST.S.L.mur||'#f4efe6',top=ST.S.L.murHaut||'#e2a56b';
  if(ax==='c'){const u=a[0];poly(c,[P(u-t,a[1],0),P(u-t,b[1],0),P(u-t,b[1],h),P(u-t,a[1],h)],col);poly(c,[P(u-t,b[1],0),P(u+t,b[1],0),P(u+t,b[1],h),P(u-t,b[1],h)],shade(col,-18));
    poly(c,[P(u-t,a[1],h),P(u+t,a[1],h),P(u+t,b[1],h),P(u-t,b[1],h)],top);}
  else{const v=a[1];poly(c,[P(a[0],v+t,0),P(b[0],v+t,0),P(b[0],v+t,h),P(a[0],v+t,h)],col);poly(c,[P(b[0],v-t,0),P(b[0],v+t,0),P(b[0],v+t,h),P(b[0],v-t,h)],shade(col,-18));
    poly(c,[P(a[0],v-t,h),P(b[0],v-t,h),P(b[0],v+t,h),P(a[0],v+t,h)],top);}
}
function shade(hex,d){const n=parseInt(hex.slice(1),16);const f=x=>Math.max(0,Math.min(255,x+d));return 'rgb('+f(n>>16)+','+f((n>>8)&255)+','+f(n&255)+')';}
// utilisé aussi par la ville (mode Ma vie) : renvoie false si les sprites ne sont pas prêts
window.w3DrawAvatar=(c,x,y,pose,fr,flip)=>{if(!useSprites())return false;const sh=pose==='walkF'?avSheet('walk_front'):pose==='walkB'?avSheet('walk_back'):avSheet('poses');if(!sh.ok)return false;
  const fi=pose==='walkF'||pose==='walkB'?fr%6:0;c.save();c.translate(x,y);if(flip)c.scale(-1,1);c.drawImage(sh,fi*256,0,256,256,-AV/2,-AV*246/256,AV,AV);c.restore();return true;};
// ── Mode déco (maison) : acheter, placer, tourner, déplacer, vendre ──
function decoMode(on){ST.deco=on;ST.pick=null;ST.sel=null;ST.moving=false;ST.path=[];
  const b=document.getElementById('int-deco');if(b){b.textContent=on?'✅ Terminé':'🛋️ Déco';b.classList.toggle('on',on);}
  let p=document.getElementById('int-dp');if(p)p.remove();
  if(on){p=document.createElement('div');p.id='int-dp';p.className='int-dp';document.getElementById('int-ov').appendChild(p);ST.dcat=ST.dcat||'Salon';decoPanel();setTip('Choisis un meuble puis touche le sol pour le poser');}
  else setTip('Touche un meuble pour agir 👆 ou le sol pour te déplacer');}
function decoPanel(){
  const p=document.getElementById('int-dp');if(!p)return;const cats=[...new Set(DATA.catalogue.map(x=>x[3]))];
  if(ST.sel!=null){const o=ST.S.items[ST.sel];const it=DATA.catalogue.find(x=>x[0]===o.m.split('~')[0]);
    p.innerHTML=`<div class="dp-sel"><b>${it?it[1]:'Meuble'}</b><button data-a="rot">↻ Tourner</button><button data-a="move">✋ Déplacer</button><button data-a="sell">🗑️ Vendre (+${Math.ceil((it?it[2]:10)/2)}🪙)</button><button data-a="x">✖</button></div>`;
    p.querySelectorAll('[data-a]').forEach(b=>b.onclick=()=>decoAction(b.dataset.a));return;}
  const col=ST.dcol||'';
  p.innerHTML=`<div class="dp-cats">${cats.map(k=>`<button data-c="${k}" class="${k===ST.dcat?'on':''}">${k}</button>`).join('')}</div>
   <div class="dp-cols">🎨 ${['','bleu','vert','jaune','rose'].map(k=>`<button data-col="${k}" class="${k===col?'on':''}" style="background:${k?DATA.couleurs[k]:'#e5534b'}"></button>`).join('')}</div>
   <div class="dp-items">${DATA.catalogue.filter(x=>x[3]===ST.dcat).map(x=>{const m=x[4].c&&col?x[0]+'~'+col:x[0];const sp=SPR[m+'|0'];
     return `<button data-m="${m}" class="${ST.pick===m?'on':''}"><img src="assets/interieur/${sp?sp[0]:''}.webp?v=${VER}" alt=""><span>${x[1]}</span><em>${x[2]}🪙</em></button>`;}).join('')}</div>`;
  p.querySelectorAll('[data-c]').forEach(b=>b.onclick=()=>{ST.dcat=b.dataset.c;decoPanel();});
  p.querySelectorAll('[data-col]').forEach(b=>b.onclick=()=>{ST.dcol=b.dataset.col;if(ST.pick){const base=ST.pick.split('~')[0];const it=DATA.catalogue.find(x=>x[0]===base);ST.pick=it&&it[4].c&&ST.dcol?base+'~'+ST.dcol:base;}decoPanel();});
  p.querySelectorAll('[data-m]').forEach(b=>b.onclick=()=>{ST.pick=ST.pick===b.dataset.m?null:b.dataset.m;ST.sel=null;ST.ghost=null;decoPanel();setTip(ST.pick?'Touche le sol (ou un meuble pour poser dessus) 👇':'Choisis un meuble');});
}
function catOf(m){return DATA.catalogue.find(x=>x[0]===m.split('~')[0]);}
function fits(m,rot,c,r,ignore){const sp=SPR[m+'|'+rot];if(!sp)return null;const fw=sp[3],fh=sp[4],flat=!!(catOf(m)||[0,0,0,0,{}])[4].flat;
  const door=(ST.S.L.porte||[-1,-1]);
  for(let a=0;a<fw;a++)for(let b=0;b<fh;b++){const cc=c+a,rr=r+b;if(cc<0||rr<0||cc>=ST.S.w||rr>=ST.S.h)return null;if(cc===door[0]&&rr===door[1])return null;
    if(!flat){const bl=ST.S.block[key(cc,rr)];if(bl&&bl.i!==ignore)return null;if(cc===ST.pos.c&&rr===ST.pos.r)return null;}
    if(a>0&&wallBetween(ST.S,[cc-1,rr],[cc,rr]))return null;if(b>0&&wallBetween(ST.S,[cc,rr-1],[cc,rr]))return null;}
  return {fw,fh,flat};}
function rebuild(){const list=ST.S.items.map(o=>{const x={m:o.m,c:o.c,r:o.r,rot:o.rot};if(o.z)x.z=o.z;if(o.deco)x.deco=1;if(o.flat)x.flat=1;if(o.buy)x.buy=1;if(o.act&&!o.buy)x.act=o.act;return x;});
  ST.S=build(ST.S.L,list);if(ST.cell){ST.cell.deco=list;try{window.__w3.save();}catch(e){}}bars();}
function decoTap(sx,sy){
  const W=W3();const {c,r}=toCell(sx,sy);
  if(ST.moving&&ST.sel!=null){const o=ST.S.items[ST.sel];if(fits(o.m,o.rot,c,r,o.i)){const dc=c-o.c,dr=r-o.r;ST.S.items.forEach(x=>{if(x.deco&&x.c===o.c&&x.r===o.r&&x!==o){x.c+=dc;x.r+=dr;}});o.c=c;o.r=r;ST.moving=false;rebuild();ST.sel=null;decoPanel();setTip('Déplacé ! ✨');}else setTip('Pas de place ici 🙅');return;}
  if(ST.pick){const m=ST.pick,it=catOf(m);if(!it)return;if(W&&W.coins<it[2]){setTip('Pas assez de 🪙 ('+it[2]+'🪙)');return;}
    let x=null;
    if(it[4].s){const base=surfaceAt(sx,sy,c,r);if(base)x={m,c:base.c,r:base.r,rot:base.rot,z:base.sp[5]||.4,deco:1,buy:1};}
    if(!x&&fits(m,0,c,r,-1)){x={m,c,r,rot:0,buy:1};if(it[4].flat)x.flat=1;}
    // 1er toucher = aperçu (vert = ok, rouge = pas de place) ; 2e toucher au même endroit = on pose
    const g=ST.ghost,same=g&&g.m===m&&x&&g.ok&&g.c===x.c&&g.r===x.r&&!!g.z===!!x.z;
    if(!same){ST.ghost=x?{...x,ok:true,sp:SPR[x.m+'|'+x.rot]}:{m,c,r,ok:false};if(ST.ghost.sp)img(ST.ghost.sp[0]);
      setTip(x?(x.z?'Sur le meuble 👍 Touche encore pour poser ✅':'Touche encore ici pour poser ✅ (ou touche une autre case)'):(it[4].s?'Touche un meuble (table, meuble télé…) ou une case libre 🙅':'Pas de place ici 🙅 (les cases bleues sont libres)'));return;}
    ST.ghost=null;
    if(W)W.coins-=it[2];ST.S.items.push({...x,sp:SPR[x.m+'|'+x.rot],i:ST.S.items.length});rebuild();try{sndTap();}catch(e){}
    const p=P(x.c+.5,x.r+.5,30);ST.floats.push({x:p[0],y:p[1],text:'−'+it[2]+'🪙',life:70});setTip('✅ '+it[1]+' : c\'est posé ! Touche-le pour le tourner ou le déplacer');return;}
  const o=itemAtCell(c,r)||itemAt(sx,sy,true);if(o){ST.sel=o.i;ST.moving=false;decoPanel();setTip('Que veux-tu faire avec ce meuble ?');}
}
// Meuble-support sous le doigt (table, meuble télé…) : on regarde d'abord le dessin touché,
// puis la case et ses voisines (le dessus d'un meuble est dessiné plus haut que sa case au sol)
function surfaceAt(sx,sy,c,r){
  const isS=o=>o&&!o.deco&&DATA.surfaces.includes(o.m.split('~')[0])&&!ST.S.items.some(x=>x.deco&&x.c===o.c&&x.r===o.r);
  const x=(sx-ST.cam.x)/ST.cam.z,y=(sy-ST.cam.y)/ST.cam.z;let best=null;
  ST.S.items.forEach(o=>{if(!isS(o))return;const sp=o.sp,im=IMG[sp[0]];if(!im||!im.ok)return;const p=P(o.c,o.r,(o.z||0)*VZ),x0=p[0]-sp[1]/2,y0=p[1]-sp[2]/2;
    if(x>=x0&&x<=x0+im.width/2&&y>=y0&&y<=y0+im.height/2){const d=o.c+o.r;if(!best||d>best.d)best={o,d};}});
  if(best)return best.o;
  for(const [dc,dr] of [[0,0],[1,0],[0,1],[1,1]]){const b=ST.S.block[key(c+dc,r+dr)];const o=b&&ST.S.items.find(z=>z.c===b.c&&z.r===b.r&&!z.deco);if(isS(o))return o;}
  return null;}
function itemAtCell(c,r){let best=null;ST.S.items.forEach(o=>{if(c>=o.c&&c<o.c+o.fw&&r>=o.r&&r<o.r+o.fh){if(!best||(o.deco&&!best.deco)||(best.flat&&!o.flat))best=o;}});return best;}
function decoAction(a){const o=ST.S.items[ST.sel];if(!o)return;const W=W3();
  if(a==='x'){ST.sel=null;ST.moving=false;decoPanel();return;}
  if(a==='rot'){for(let k=1;k<4;k++){const nr=(o.rot+k)%4;if(SPR[o.m+'|'+nr]&&fits(o.m,nr,o.c,o.r,o.i)){o.rot=nr;ST.S.items.forEach(x=>{if(x.deco&&x.c===o.c&&x.r===o.r&&x!==o&&SPR[x.m+'|'+nr])x.rot=nr;});rebuild();ST.sel=ST.S.items.findIndex(x=>x.c===o.c&&x.r===o.r&&x.m===o.m);decoPanel();return;}}setTip('Pas la place pour le tourner 🙅');return;}
  if(a==='move'){ST.moving=true;setTip('Touche la case où le mettre 👇');return;}
  if(a==='sell'){const it=catOf(o.m);const back=Math.ceil((it?it[2]:10)/2);if(W)W.coins+=back;
    ST.S.items=ST.S.items.filter(x=>x!==o&&!(x.deco&&!o.deco&&x.c===o.c&&x.r===o.r));rebuild();ST.sel=null;decoPanel();setTip('Vendu ! +'+back+'🪙');}
}
function decoDraw(c){
  const o=ST.sel!=null?ST.S.items[ST.sel]:null;
  if(o){c.save();c.setLineDash([4,3]);poly(c,[P(o.c,o.r),P(o.c+o.fw,o.r),P(o.c+o.fw,o.r+o.fh),P(o.c,o.r+o.fh)],'rgba(255,209,102,.25)','#ffd166',2);c.restore();}
  const g=ST.pick&&ST.ghost;
  if(g){c.save();const fw=g.sp?g.sp[3]:1,fh=g.sp?g.sp[4]:1,z=(g.z||0)*VZ;
    poly(c,[P(g.c,g.r,z),P(g.c+fw,g.r,z),P(g.c+fw,g.r+fh,z),P(g.c,g.r+fh,z)],g.ok?'rgba(6,214,160,.35)':'rgba(239,71,111,.35)',g.ok?'#06d6a0':'#ef476f',2);
    if(g.ok&&g.sp){c.globalAlpha=.7;try{sprite(c,g);}catch(e){}}c.restore();}
  if(ST.pick||ST.moving){c.save();c.globalAlpha=.25;for(let r=0;r<ST.S.h;r++)for(let k=0;k<ST.S.w;k++)if(!ST.S.block[key(k,r)])poly(c,[P(k+.08,r+.08),P(k+.92,r+.08),P(k+.92,r+.92),P(k+.08,r+.92)],null,'#4cc9f0',1);c.restore();}
}
// ── Objets dessinés à la main (luxe) ──
const GOLD='#d4af37',GOLD2='#b8932f';
function box(c,u0,u1,v0,v1,z0,z1,top,l,r){poly(c,[P(u0,v1,z0),P(u1,v1,z0),P(u1,v1,z1),P(u0,v1,z1)],l);poly(c,[P(u1,v1,z0),P(u1,v0,z0),P(u1,v0,z1),P(u1,v1,z1)],r);if(top)poly(c,[P(u0,v0,z1),P(u1,v0,z1),P(u1,v1,z1),P(u0,v1,z1)],top);}
function cyl(c,u,v,rad,z0,z1,cl,cd){const a=P(u,v,z0),b=P(u,v,z1),rx=rad*TW/2*Math.SQRT2,ry=rx/2;const g=c.createLinearGradient(a[0]-rx,0,a[0]+rx,0);g.addColorStop(0,cl);g.addColorStop(1,cd);
  c.beginPath();c.moveTo(a[0]-rx,b[1]);c.lineTo(a[0]-rx,a[1]);c.ellipse(a[0],a[1],rx,ry,0,Math.PI,0,true);c.lineTo(a[0]+rx,b[1]);c.closePath();c.fillStyle=g;c.fill();c.fillStyle=cl;c.beginPath();c.ellipse(b[0],b[1],rx,ry,0,0,7);c.fill();}
const PROC={
  colonne(c,o){const u=o.c+.5,v=o.r+.5;box(c,u-.3,u+.3,v-.3,v+.3,0,5,GOLD,GOLD2,'#9c7a22');cyl(c,u,v,.2,5,WALL-6,'#fbf8f1','#cfc6b6');
    c.strokeStyle='rgba(0,0,0,.06)';c.lineWidth=1;for(let k=-1;k<=1;k++){const a=P(u+k*.08,v-k*.08,6),b=P(u+k*.08,v-k*.08,WALL-7);c.beginPath();c.moveTo(a[0],a[1]);c.lineTo(b[0],b[1]);c.stroke();}
    box(c,u-.3,u+.3,v-.3,v+.3,WALL-6,WALL,GOLD,GOLD2,'#9c7a22');},
  piscine(c,o){const u0=o.c,v0=o.r,u1=o.c+o.fw,v1=o.r+o.fh;poly(c,[P(u0,v0),P(u1,v0),P(u1,v1),P(u0,v1)],'#ffffff');
    poly(c,[P(u0+.12,v0+.12,-1),P(u1-.12,v0+.12,-1),P(u1-.12,v1-.12,-1),P(u0+.12,v1-.12,-1)],'#2fb5d6');
    poly(c,[P(u0+.12,v0+.12,-1),P(u1-.12,v0+.12,-1),P(u1-.12,v0+.12,-7),P(u0+.12,v0+.12,-7)],'#1d8fb0');
    c.strokeStyle='rgba(255,255,255,.55)';c.lineWidth=1;const t=performance.now()/900;for(let k=0;k<5;k++){const a=P(u0+.3+((k*.7+t)%(o.fw-.6)),v0+.3+k*.3,-1),b=P(u0+.3+((k*.7+t)%(o.fw-.6))+.35,v0+.3+k*.3,-1);c.beginPath();c.moveTo(a[0],a[1]);c.lineTo(b[0],b[1]);c.stroke();}
    const l=P(u1-.3,v0+.15);c.strokeStyle='#c0c0c0';c.lineWidth=1.4;c.beginPath();c.moveTo(l[0],l[1]);c.lineTo(l[0],l[1]-9);c.moveTo(l[0]+5,l[1]+2);c.lineTo(l[0]+5,l[1]-7);c.stroke();},
  cheminee(c,o){const u=o.c,v=o.r;box(c,u,u+.55,v+.05,v+.95,0,30,'#e9e2d3','#d8cfbd','#bfb4a0');poly(c,[P(u+.55,v+.3,0),P(u+.55,v+.7,0),P(u+.55,v+.7,15),P(u+.55,v+.3,15)],'#2b1d14');
    const f=P(u+.56,v+.5,2),t=performance.now()/120;for(let k=0;k<3;k++){const h=8+3*Math.sin(t+k*2);c.fillStyle=k===1?'#ffd166':'#f77f00';c.beginPath();c.moveTo(f[0]-6+k*4,f[1]);c.quadraticCurveTo(f[0]-5+k*4,f[1]-h,f[0]-3+k*4,f[1]-h-3);c.quadraticCurveTo(f[0]-1+k*4,f[1]-h,f[0]+k*4,f[1]);c.fill();}
    box(c,u-.02,u+.62,v,v+1,30,33,GOLD,GOLD2,'#9c7a22');},
  piano(c,o){const u=o.c+.1,v=o.r+.15;for(const [a,b] of [[.1,.1],[.75,.1],[.4,.7]]){const p=P(u+a,v+b,0),q=P(u+a,v+b,12);c.strokeStyle='#111';c.lineWidth=2;c.beginPath();c.moveTo(p[0],p[1]);c.lineTo(q[0],q[1]);c.stroke();}
    box(c,u,u+.85,v,v+.75,12,19,'#1a1a1a','#0d0d0d','#050505');poly(c,[P(u,v+.75,16),P(u+.85,v+.75,16),P(u+.85,v+.9,16),P(u,v+.9,16)],'#fafafa');
    c.strokeStyle='#222';c.lineWidth=.5;c.beginPath();for(let k=1;k<12;k++){const a=P(u+k*.07,v+.75,16),b=P(u+k*.07,v+.9,16);c.moveTo(a[0],a[1]);c.lineTo(b[0],b[1]);}c.stroke();
    poly(c,[P(u+.05,v+.05,19),P(u+.8,v+.05,19),P(u+.45,v+.1,34)],'#222');},
  statue(c,o){const u=o.c+.5,v=o.r+.5;box(c,u-.25,u+.25,v-.25,v+.25,0,14,'#f3efe6','#e2dccf','#c9c0ae');const b=P(u,v,14);
    const g=c.createLinearGradient(b[0]-8,0,b[0]+8,0);g.addColorStop(0,'#f6e27a');g.addColorStop(1,GOLD2);c.fillStyle=g;c.beginPath();c.ellipse(b[0],b[1]-10,5,9,0,0,7);c.fill();c.beginPath();c.arc(b[0],b[1]-22,4,0,7);c.fill();
    c.beginPath();c.ellipse(b[0]+5,b[1]-14,2,6,.6,0,7);c.fill();c.beginPath();c.ellipse(b[0]-5,b[1]-14,2,6,-.6,0,7);c.fill();},
  palmier(c,o){const b=P(o.c+.5,o.r+.5,0);box(c,o.c+.3,o.c+.7,o.r+.3,o.r+.7,0,9,'#8d6e63','#a1887f','#795548');const h=40,t=[b[0]+2,b[1]-9-h],sw=Math.sin(performance.now()/1200+o.c)*1.5;
    c.strokeStyle='#8d6e4f';c.lineWidth=3;c.beginPath();c.moveTo(b[0],b[1]-9);c.quadraticCurveTo(b[0]+5,b[1]-9-h/2,t[0],t[1]);c.stroke();c.strokeStyle='#2d9c55';c.lineWidth=2.6;c.beginPath();
    [[-14,4],[14,5],[-10,-5],[11,-4],[0,-10],[-16,-1],[16,1]].forEach(([dx,dy])=>{c.moveTo(t[0],t[1]);c.quadraticCurveTo(t[0]+dx*.6,t[1]+dy-5,t[0]+dx+sw,t[1]+dy+3);});c.stroke();},
};
// décor des murs : baie vitrée, aquarium, tableau, miroir
function wallPts(m,a,b,z0,z1){return m==='r'?[P(a,0,z0),P(b,0,z0),P(b,0,z1),P(a,0,z1)]:[P(0,a,z0),P(0,b,z0),P(0,b,z1),P(0,a,z1)];}
function wallXf(c,m,a,z){const o=m==='r'?P(a,0,z):P(0,a,z);if(m==='r')c.transform(.894,.447,0,1,o[0],o[1]);else c.transform(-.894,.447,0,1,o[0],o[1]);} // 1 unité ≈ 35.8 px le long du mur
function murDeco(c,L){
  (L.murDeco||[]).forEach(([t,m,a,b,o])=>{o=o||{};const len=(b-a)*35.78;
    if(t==='baie'){const z0=4,z1=WALL-3;c.save();c.beginPath();wallPts(m,a,b,z0,z1).forEach((p,i)=>i?c.lineTo(p[0],p[1]):c.moveTo(p[0],p[1]));c.closePath();c.clip();
      wallXf(c,m,a,z0);const g=c.createLinearGradient(0,-(z1-z0),0,0);g.addColorStop(0,'#8fd3ff');g.addColorStop(.55,'#d8f1ff');
      g.addColorStop(.56,o.lagon?'#3cc8d0':o.mer?'#1f7fb8':'#7cc0e8');g.addColorStop(1,o.lagon?'#7fe3e0':o.mer?'#3a9ad0':'#b9e2f5');c.fillStyle=g;c.fillRect(0,-(z1-z0),len,z1-z0);
      c.fillStyle='rgba(255,255,255,.9)';c.beginPath();c.arc(len*.75,-(z1-z0)*.8,5,0,7);c.fill();
      c.restore();poly(c,wallPts(m,a,b,z0,z1),null,'#f5f5f5',2);c.strokeStyle='rgba(255,255,255,.9)';c.lineWidth=1.5;c.beginPath();for(let k=a+1;k<b;k++){const p=wallPts(m,k,k,z0,z1);c.moveTo(p[0][0],p[0][1]);c.lineTo(p[3][0],p[3][1]);}c.stroke();}
    if(t==='aquarium'){const z0=4,z1=WALL-2;c.save();c.beginPath();wallPts(m,a,b,z0,z1).forEach((p,i)=>i?c.lineTo(p[0],p[1]):c.moveTo(p[0],p[1]));c.closePath();c.clip();wallXf(c,m,a,z0);
      const g=c.createLinearGradient(0,-(z1-z0),0,0);g.addColorStop(0,'#1fa3d6');g.addColorStop(1,'#063d6b');c.fillStyle=g;c.fillRect(0,-(z1-z0),len,z1-z0);
      const tt=performance.now()/1000;c.fillStyle='rgba(255,255,255,.35)';for(let k=0;k<10;k++){const x=(k*37)%len,y=-((tt*12+k*13)%(z1-z0));c.beginPath();c.arc(x,y,1.3,0,7);c.fill();}
      c.fillStyle='#2d6a4f';for(let k=0;k<len;k+=18){c.beginPath();c.moveTo(k,0);c.quadraticCurveTo(k+4+Math.sin(tt+k)*3,-14,k+2,-22);c.quadraticCurveTo(k+6,-12,k+7,0);c.fill();}
      c.font='11px serif';c.textAlign='center';c.textBaseline='middle';['🐠','🐟','🐡','🐠','🦈','🐟','🐢'].forEach((f,k)=>{const sp=8+k*3,dir=k%2?1:-1,x=((tt*sp*dir+k*53)%len+len)%len,y=-(10+((k*11)%(z1-z0-18)));
        c.save();c.translate(x,y+Math.sin(tt*2+k)*2);if(dir>0)c.scale(-1,1);c.fillText(f,0,0);c.restore();});
      c.restore();poly(c,wallPts(m,a,b,z0,z1),null,GOLD,3);}
    if(t==='tableau'){const z0=o.z0||22,z1=o.z1||46;poly(c,wallPts(m,a,b,z0,z1),GOLD,'#8a6d1f',1);const i=.08;c.save();c.beginPath();wallPts(m,a+i,b-i,z0+3,z1-3).forEach((p,k)=>k?c.lineTo(p[0],p[1]):c.moveTo(p[0],p[1]));c.closePath();c.clip();
      wallXf(c,m,a,z0);const W=len,H=z1-z0,seed=Math.round(a*7+b*3);const hue=[200,30,140,260][seed%4];c.fillStyle=`hsl(${hue},55%,78%)`;c.fillRect(0,-H,W,H);
      c.fillStyle=`hsl(${(hue+60)%360},45%,45%)`;c.beginPath();c.moveTo(0,-H*.25);c.quadraticCurveTo(W*.3,-H*.65,W*.6,-H*.35);c.quadraticCurveTo(W*.8,-H*.2,W,-H*.45);c.lineTo(W,0);c.lineTo(0,0);c.fill();
      c.fillStyle='#ffd166';c.beginPath();c.arc(W*.72,-H*.72,H*.12,0,7);c.fill();c.restore();}
    if(t==='miroir'){const z0=o.z0||14,z1=o.z1||50;c.save();wallXf(c,m,a,z0);const W=len,H=z1-z0;c.fillStyle=GOLD;c.beginPath();c.ellipse(W/2,-H/2,W/2,H/2,0,0,7);c.fill();
      const g=c.createLinearGradient(0,-H,W,0);g.addColorStop(0,'#e9f2f7');g.addColorStop(.5,'#b8c9d4');g.addColorStop(1,'#eef5f9');c.fillStyle=g;c.beginPath();c.ellipse(W/2,-H/2,W/2-3,H/2-3,0,0,7);c.fill();
      c.fillStyle=GOLD;c.beginPath();c.arc(W/2,-H-2,4,0,7);c.fill();c.restore();}
  });}
function wallMotif(c,L,S){if(L.lambris){poly(c,[P(0,0),P(S.w,0),P(S.w,0,16),P(0,0,16)],shade(L.lambris,-8));poly(c,[P(0,0),P(0,S.h),P(0,S.h,16),P(0,0,16)],L.lambris);
    c.strokeStyle=GOLD;c.lineWidth=1.2;c.beginPath();let a=P(0,0,16),b=P(S.w,0,16);c.moveTo(a[0],a[1]);c.lineTo(b[0],b[1]);a=P(0,0,16);b=P(0,S.h,16);c.moveTo(a[0],a[1]);c.lineTo(b[0],b[1]);c.stroke();}
  if(L.motif==='damas'){c.fillStyle='rgba(212,175,55,.28)';for(let u=.25;u<S.w;u+=.5)for(let z=24;z<WALL-4;z+=9){const q=P(u,0,z+((u*2)%2?4.5:0));c.beginPath();c.moveTo(q[0],q[1]-3);c.lineTo(q[0]+2,q[1]);c.lineTo(q[0],q[1]+3);c.lineTo(q[0]-2,q[1]);c.fill();}
    for(let v=.25;v<S.h;v+=.5)for(let z=24;z<WALL-4;z+=9){const q=P(0,v,z+((v*2)%2?4.5:0));c.beginPath();c.moveTo(q[0],q[1]-3);c.lineTo(q[0]+2,q[1]);c.lineTo(q[0],q[1]+3);c.lineTo(q[0]-2,q[1]);c.fill();}}}
function lustres(c,L){(L.lustres||[]).forEach(([u,v,t])=>{const z=WALL+4,p=P(u,v,z),sw=Math.sin(performance.now()/1500+u)*1.2;c.strokeStyle=GOLD2;c.lineWidth=1;c.beginPath();c.moveTo(p[0],p[1]-60);c.lineTo(p[0]+sw,p[1]);c.stroke();
  const x=p[0]+sw,y=p[1];const gl=c.createRadialGradient(x,y+6,2,x,y+6,38);gl.addColorStop(0,'rgba(255,236,170,.35)');gl.addColorStop(1,'rgba(255,236,170,0)');c.fillStyle=gl;c.beginPath();c.arc(x,y+6,38,0,7);c.fill();
  if(t==='moderne'){c.fillStyle='#1f1f1f';c.beginPath();c.ellipse(x,y+4,14,4,0,0,7);c.fill();c.fillStyle='#ffe9a8';c.beginPath();c.ellipse(x,y+6,12,2.5,0,0,Math.PI);c.fill();return;}
  c.strokeStyle=GOLD;c.lineWidth=1.6;c.beginPath();c.ellipse(x,y+6,14,5,0,0,7);c.stroke();c.beginPath();c.ellipse(x,y+12,8,3,0,0,7);c.stroke();
  for(let k=0;k<8;k++){const a=k/8*Math.PI*2,cx=x+Math.cos(a)*14,cy=y+6+Math.sin(a)*5;c.fillStyle='#fff8e1';c.fillRect(cx-.8,cy-6,1.6,6);c.fillStyle='#ffd166';c.beginPath();c.arc(cx,cy-7,1.6,0,7);c.fill();
    c.fillStyle='rgba(220,240,255,.85)';c.beginPath();c.moveTo(cx,cy+1);c.lineTo(cx+1.5,cy+4);c.lineTo(cx,cy+7);c.lineTo(cx-1.5,cy+4);c.fill();}
  c.fillStyle='rgba(220,240,255,.9)';c.beginPath();c.moveTo(x,y+14);c.lineTo(x+3,y+19);c.lineTo(x,y+24);c.lineTo(x-3,y+19);c.fill();});}
window.w3IntHas=id=>has(id);window.w3IntOpen=open;window.w3IntClose=close;window.w3IntLoad=load;
window.__int={get ST(){return ST;},tap:(x,y)=>tap(x,y),P:(u,v,z)=>P(u,v,z),goItem:i=>ST&&goItem(ST.S.items[i])};
load().catch(()=>{});['walk_front','walk_back','poses'].forEach(avSheet);
})();
