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
  moquetteBeige:['#e8d9bf','#e0cfb2'],marbre:['#f2f0ec','#e2ded6'],clair:['#f3ece2','#ebe2d5'],lino:['#e3e7ea','#d6dce0'],blancBleu:['#eef5fb','#e0ebf5']};
function load(){if(DATA)return Promise.resolve();
  return Promise.all([fetch('data/interieurs.json?v='+VER).then(r=>r.json()),fetch('assets/interieur/sprites.json?v='+VER).then(r=>r.json())]).then(([d,s])=>{DATA=d;SPR=s;});}
function img(n){if(!IMG[n]){const i=new Image();i.onload=()=>{i.ok=1;};i.src='assets/interieur/'+n+'.webp?v='+VER;IMG[n]=i;}return IMG[n];}
const W3=()=>window.__w3&&window.__w3.W3;
function has(id){return !!(DATA&&DATA.batiments[id]);}
// ── géométrie ──
function P(u,v,z){return [(u-v)*TW/2,(u+v)*TH/2-(z||0)];}
function poly(c,pts,fill,stroke,lw){c.beginPath();pts.forEach((p,i)=>i?c.lineTo(p[0],p[1]):c.moveTo(p[0],p[1]));c.closePath();if(fill){c.fillStyle=fill;c.fill();}if(stroke){c.strokeStyle=stroke;c.lineWidth=lw||1;c.stroke();}}
function key(c,r){return c+','+r;}
function build(L){
  const S={L,items:[],block:{},seats:{},walls:new Set(),w:L.w,h:L.h};
  L.items.forEach((it,i)=>{const sp=SPR[it.m+'|'+it.rot];if(!sp)return;const o={...it,sp,fw:sp[3],fh:sp[4],i};S.items.push(o);img(sp[0]);
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
function open(bid){
  return load().then(()=>{
    const lid=DATA.batiments[bid];if(!lid)return false;const L=DATA.interieurs[lid];
    const S=build(L);const p=L.porte||[0,0];
    ST={S,bid,lid,pos:{c:p[0],r:p[1]},path:[],t:0,dir:[0,1],walk:0,busy:null,floats:[],cam:{x:0,y:0,z:1},sel:null};
    ui();fit();loop();return true;});
}
function close(){if(!ST)return;ST=null;const o=document.getElementById('int-ov');if(o)o.remove();try{window.__w3.save();window.__w3.hud();}catch(e){}}
function ui(){
  let o=document.getElementById('int-ov');if(o)o.remove();
  o=document.createElement('div');o.id='int-ov';
  const L=ST.S.L;
  o.innerHTML=`<div class="int-top"><button class="int-out" id="int-out">⬅ Sortir</button><b class="int-nom">${L.nom}</b><span class="int-coins" id="int-coins"></span></div>
  <div class="int-bars" id="int-bars"></div>
  <div class="int-rooms" id="int-rooms"><button data-room="-1" class="on">🏠 Tout</button>${(L.pieces||[]).map((p,i)=>`<button data-room="${i}">${p[0]}</button>`).join('')}</div>
  <canvas id="int-cv"></canvas>
  <div class="int-tip" id="int-tip">Touche un meuble pour agir 👆 ou le sol pour te déplacer</div>`;
  document.body.appendChild(o);
  o.querySelector('#int-out').onclick=close;
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
function itemAt(sx,sy){ // priorité : objet dessiné sous le doigt (le plus en avant)
  const x=(sx-ST.cam.x)/ST.cam.z,y=(sy-ST.cam.y)/ST.cam.z;let best=null;
  ST.S.items.forEach(o=>{if(!o.act||o.flat)return;const sp=o.sp,im=IMG[sp[0]];if(!im||!im.ok)return;const p=P(o.c,o.r,(o.z||0)*VZ),x0=p[0]-sp[1]/2,y0=p[1]-sp[2]/2,w=im.width/2,h=im.height/2;
    if(x>=x0&&x<=x0+w&&y>=y0&&y<=y0+h){const d=o.c+o.r+(o.fw+o.fh)/2+(o.deco?.5:0);if(!best||d>best.d)best={o,d};}});
  return best&&best.o;}
function tap(sx,sy){
  if(!ST||ST.busy)return;
  const o=itemAt(sx,sy);
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
  c.save();c.fillStyle='rgba(0,0,0,.22)';c.beginPath();c.ellipse(x,y,10,4.5,0,0,7);c.fill();c.restore();
  if(useSprites()){const sheet=pose==='walkF'?avSheet('walk_front'):pose==='walkB'?avSheet('walk_back'):avSheet('poses');
    const fi=pose==='walkF'||pose==='walkB'?frameIdx%6:{idle:0,sit:1,sleep:2,eat:3,wave:4,jump:5}[pose]||0;
    if(sheet.ok){const s=pose==='sleep'?AV*1.25:AV;c.save();c.translate(x,y-(lift||0));if(flip)c.scale(-1,1);c.drawImage(sheet,fi*256,0,256,256,-s/2,-s*246/256,s,s);c.restore();return;}}
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
    else if(pose==='sleep'&&/bed/i.test(b.m)){ax=b.c+b.fw/2+.1;ay=b.r+b.fh/2+.1;lift=5;dk=b.c+b.r+(b.fw+b.fh)/2-1+.2;}
    else if((pose==='sit'||pose==='eat')&&ST.S.seats[key(ST.pos.c,ST.pos.r)]){const ch=ST.S.seats[key(ST.pos.c,ST.pos.r)];pose='sit';lift=9;dk=ch.c+ch.r-1+.25;}
    else if(pose==='sit')pose='idle';
    if(pose==='jump')lift=Math.abs(Math.sin(performance.now()/180))*8;}
  const fr=Math.floor(ST.walk);
  D.push([dk,()=>{const p=P(ax,ay);drawAvatar(c,p[0],p[1],pose,fr,flip,lift);
    if(ST.busy){const k=Math.min(1,(performance.now()-ST.busy.t0)/ST.busy.dur);const q=[p[0],p[1]-AV-14];c.fillStyle='rgba(255,255,255,.92)';c.beginPath();c.roundRect(q[0]-22,q[1]-7,44,9,4);c.fill();
      c.fillStyle='#2b9348';c.beginPath();c.roundRect(q[0]-20,q[1]-5,40*k,5,3);c.fill();}}]);
  D.sort((a,b)=>a[0]-b[0]).forEach(d=>d[1]());
  // textes flottants
  ST.floats.forEach(f=>{c.globalAlpha=Math.min(1,f.life/40);c.font='bold 9px sans-serif';c.textAlign='center';c.lineWidth=3;c.strokeStyle='rgba(0,0,0,.55)';c.strokeText(f.text,f.x,f.y);c.fillStyle='#fff';c.fillText(f.text,f.x,f.y);c.globalAlpha=1;});
}
function sprite(c,o){const sp=o.sp,im=IMG[sp[0]];if(!im||!im.ok)return;const p=P(o.c,o.r,(o.z||0)*VZ);c.drawImage(im,p[0]-sp[1]/2,p[1]-sp[2]/2,im.width/2,im.height/2);}
function wallBack(c,L,S){
  const H=WALL,col=L.mur||'#f4efe6',top=L.murHaut||'#e2a56b';
  // mur le long de r=0 (haut-droit) et c=0 (haut-gauche)
  poly(c,[P(0,0),P(S.w,0),P(S.w,0,H),P(0,0,H)],shade(col,-6));
  poly(c,[P(0,0),P(0,S.h),P(0,S.h,H),P(0,0,H)],col);
  // plinthes
  poly(c,[P(0,0),P(S.w,0),P(S.w,0,4),P(0,0,4)],shade(col,-30));poly(c,[P(0,0),P(0,S.h),P(0,S.h,4),P(0,0,4)],shade(col,-24));
  // fenêtres sur le mur du fond
  for(let k=1;k<S.w-1;k+=3){if(L.tableau&&k>=2&&k<=5)continue;const a=k+.25,b=k+1.25;poly(c,[P(a,0,22),P(b,0,22),P(b,0,48),P(a,0,48)],'#ffffff');poly(c,[P(a+.06,0,24),P(b-.06,0,24),P(b-.06,0,46),P(a+.06,0,46)],'#9fd3f0');
    c.strokeStyle='#fff';c.lineWidth=1.2;c.beginPath();const m1=P((a+b)/2,0,24),m2=P((a+b)/2,0,46);c.moveTo(m1[0],m1[1]);c.lineTo(m2[0],m2[1]);c.stroke();}
  // tableau de l'école
  if(L.tableau){poly(c,[P(2.3,0,16),P(5.7,0,16),P(5.7,0,46),P(2.3,0,46)],'#8d6e63');poly(c,[P(2.4,0,18),P(5.6,0,18),P(5.6,0,44),P(2.4,0,44)],'#2d6a4f');
    const o=P(4,0,33);c.save();c.transform(.894,.447,0,1,o[0],o[1]);c.font='bold 7px sans-serif';c.fillStyle='rgba(255,255,255,.9)';c.textAlign='center';c.fillText('2 + 3 = 5   Bonjour !',0,0);c.restore();}
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
window.w3IntHas=id=>has(id);window.w3IntOpen=open;window.w3IntClose=close;window.w3IntLoad=load;
window.__int={get ST(){return ST;},tap:(x,y)=>tap(x,y),goItem:i=>ST&&goItem(ST.S.items[i])};
load().catch(()=>{});['walk_front','walk_back','poses'].forEach(avSheet);
})();
