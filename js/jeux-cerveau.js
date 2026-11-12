// PocketSage — Jeux de réflexion (créés le 12/11/2026)
// Simon Sensei, Grille mémoire, Réflexes, Table de Schulte, Couleurs piégées (Stroop),
// Sudoku junior, Labyrinthe, Mots mêlés.
// Chargé après js/jeux.js : utilise _gTimeout/_gInterval/_gPad/endGame/updateGameScore.
(function(){
'use strict';
const AGE=()=>((typeof P==='function'&&P()&&P().age)||8);
const $=id=>document.getElementById(id);
const inner=()=>$('game-inner');
const shuffle=a=>{for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]];}return a;};
const tone=(f,d)=>{try{beep(f,d||.18,'sine',.22);}catch(e){}};
const hideTimer=()=>{const t=$('game-timer-disp');if(t)t.style.display='none';};
const info=(html)=>`<p class="g-info">${html}</p>`;

JEUX_CFG.push(
  {id:'simon',   emoji:'🎵', title:'Simon Sensei',      desc:'Répète la suite de couleurs',   min_score:0},
  {id:'grille',  emoji:'🟦', title:'Grille mémoire',    desc:'Retrouve les cases allumées',   min_score:0},
  {id:'reflexes',emoji:'⚡', title:'Réflexes',          desc:'Touche dès que ça passe au vert',min_score:0},
  {id:'schulte', emoji:'🔢', title:'Table de Schulte',  desc:'Touche les nombres dans l\'ordre',min_score:0},
  {id:'stroop',  emoji:'🎨', title:'Couleurs piégées',  desc:'La couleur de l\'encre, pas le mot !',min_score:0},
  {id:'sudoku',  emoji:'🧮', title:'Sudoku junior',     desc:'Chaque chiffre une fois par ligne',min_score:0},
  {id:'laby',    emoji:'🌀', title:'Labyrinthe',        desc:'Trouve la sortie',               min_score:0},
  {id:'motsmeles',emoji:'🔎',title:'Mots mêlés',        desc:'Retrouve les mots anglais cachés',min_score:0}
);
window.JEUX_EXTRA=window.JEUX_EXTRA||{};

// ── 1. SIMON SENSEI ─────────────────────────────────────────────
JEUX_EXTRA.simon=function(){
  const C=[{c:'#06D6A0',f:392},{c:'#FF5C8A',f:330},{c:'#FFD166',f:262},{c:'#3A86FF',f:196}];
  inner().innerHTML=info('Regarde, écoute… puis répète la suite !')+
    `<p class="g-big" id="sm-msg">Prêt ?</p><div class="simon">${C.map((x,i)=>`<button class="simon-b" id="sm${i}" style="--c:${x.c}" data-i="${i}"></button>`).join('')}</div>`;
  let seq=[],pos=0,listen=false,score=0;
  const light=i=>{const b=$('sm'+i);if(!b)return;b.classList.add('on');tone(C[i].f,.28);_gTimeout(()=>b&&b.classList.remove('on'),300);};
  function play(){
    listen=false;pos=0;$('sm-msg').textContent='Regarde…';
    seq.push(Math.floor(Math.random()*4));
    const gap=AGE()<7?750:AGE()<11?620:520;
    seq.forEach((v,k)=>_gTimeout(()=>light(v),600+k*gap));
    _gTimeout(()=>{listen=true;const m=$('sm-msg');if(m)m.textContent='À toi ! ('+seq.length+')';},600+seq.length*gap);
  }
  document.querySelectorAll('.simon-b').forEach(b=>b.addEventListener('pointerdown',e=>{
    e.preventDefault();if(!listen)return;const i=+b.dataset.i;light(i);
    if(i!==seq[pos]){listen=false;sndKO();$('sm-msg').textContent='Oups ! Suite de '+(seq.length-1);_gTimeout(()=>endGame(score),900);return;}
    pos++;if(pos===seq.length){listen=false;score+=10*seq.length;updateGameScore(score);sndOK();_gTimeout(play,700);}
  }));
  hideTimer();_gTimeout(play,500);
};

// ── 2. GRILLE MÉMOIRE ───────────────────────────────────────────
JEUX_EXTRA.grille=function(){
  const N=AGE()<7?3:AGE()<11?4:5;let k=AGE()<7?2:3,lives=3,score=0,phase='show',targets=[],found=0;
  inner().innerHTML=info('Mémorise les cases bleues, puis touche-les !')+
    `<p class="g-big" id="gr-msg"></p><div class="mgrid" id="gr" style="grid-template-columns:repeat(${N},1fr)"></div><p class="g-info" id="gr-lives"></p>`;
  function round(){
    phase='show';found=0;targets=shuffle([...Array(N*N).keys()]).slice(0,Math.min(k,N*N-1));
    $('gr-msg').textContent=k+' cases';$('gr-lives').textContent='❤️'.repeat(lives);
    $('gr').innerHTML=[...Array(N*N).keys()].map(i=>`<button class="mcell${targets.includes(i)?' lit':''}" data-i="${i}"></button>`).join('');
    _gTimeout(()=>{document.querySelectorAll('.mcell').forEach(c=>c.classList.remove('lit'));phase='play';},900+k*250);
    document.querySelectorAll('.mcell').forEach(c=>c.addEventListener('pointerdown',e=>{
      e.preventDefault();if(phase!=='play'||c.classList.contains('ok'))return;
      if(targets.includes(+c.dataset.i)){c.classList.add('ok');tone(523,.1);found++;
        if(found===targets.length){phase='done';score+=10*k;updateGameScore(score);sndOK();k++;_gTimeout(round,700);}}
      else{c.classList.add('ko');sndKO();lives--;phase='done';
        targets.forEach(t=>document.querySelector(`.mcell[data-i="${t}"]`).classList.add('lit'));
        if(lives<=0){_gTimeout(()=>endGame(score),1000);}else{k=Math.max(2,k-1);_gTimeout(round,1200);}}
    }));
  }
  hideTimer();round();
};

// ── 3. RÉFLEXES ─────────────────────────────────────────────────
JEUX_EXTRA.reflexes=function(){
  const ROUNDS=5;let r=0,state='wait',t0=0,times=[],score=0;
  inner().innerHTML=info('Attends que le rond devienne <b>vert</b>, puis touche-le le plus vite possible !')+
    `<button class="refl" id="rf"><span id="rf-t">Touche pour commencer</span></button><p class="g-info" id="rf-res"></p>`;
  const b=$('rf'),txt=$('rf-t');
  function arm(){state='red';b.className='refl red';txt.textContent='Attends…';
    _gTimeout(()=>{if(state!=='red')return;state='green';b.className='refl green';txt.textContent='VAS-Y !';t0=performance.now();},1200+Math.random()*2600);}
  b.addEventListener('pointerdown',e=>{e.preventDefault();
    if(state==='wait'||state==='next'){arm();return;}
    if(state==='red'){state='next';b.className='refl';txt.textContent='Trop tôt ! Touche pour recommencer';sndKO();return;}
    if(state==='green'){const ms=Math.round(performance.now()-t0);times.push(ms);r++;
      score+=Math.max(5,Math.round(60-ms/10));updateGameScore(score);tone(660,.1);
      $('rf-res').textContent=times.map(t=>t+' ms').join(' · ');
      if(r>=ROUNDS){state='end';b.className='refl';const avg=Math.round(times.reduce((a,c)=>a+c,0)/times.length);
        txt.textContent='Moyenne : '+avg+' ms';sndOK();_gTimeout(()=>endGame(score),1600);}
      else{state='next';b.className='refl';txt.textContent=ms+' ms — touche pour la suite ('+r+'/'+ROUNDS+')';}}
  });
  hideTimer();
};

// ── 4. TABLE DE SCHULTE ─────────────────────────────────────────
JEUX_EXTRA.schulte=function(){
  const N=AGE()<6?3:AGE()<9?4:5,M=N*N;let next=1,t0=0,iv;
  const nums=shuffle([...Array(M)].map((_,i)=>i+1));
  inner().innerHTML=info('Touche les nombres de <b>1 à '+M+'</b> dans l\'ordre, le plus vite possible.')+
    `<p class="g-big" id="sc-msg">Cherche : 1</p><div class="mgrid schulte" style="grid-template-columns:repeat(${N},1fr)">${nums.map(n=>`<button class="mcell num" data-n="${n}">${n}</button>`).join('')}</div><p class="g-info" id="sc-t">0,0 s</p>`;
  document.querySelectorAll('.schulte .mcell').forEach(c=>c.addEventListener('pointerdown',e=>{
    e.preventDefault();const n=+c.dataset.n;
    if(n!==next){c.classList.add('ko');_gTimeout(()=>c.classList.remove('ko'),250);sndKO();return;}
    if(next===1){t0=performance.now();iv=_gInterval(()=>{const el=$('sc-t');if(el)el.textContent=((performance.now()-t0)/1000).toFixed(1).replace('.',',')+' s';},100);}
    c.classList.add('ok');tone(440+n*12,.07);next++;
    if(next>M){clearInterval(iv);const sec=(performance.now()-t0)/1000;const sc=Math.max(10,Math.round(M*8-sec*4));updateGameScore(sc);sndOK();
      $('sc-msg').textContent='Bravo ! '+sec.toFixed(1).replace('.',',')+' s';_gTimeout(()=>endGame(sc),1400);}
    else $('sc-msg').textContent='Cherche : '+next;
  }));
  hideTimer();
};

// ── 5. COULEURS PIÉGÉES (Stroop) ────────────────────────────────
JEUX_EXTRA.stroop=function(){
  const C=[{n:'ROUGE',c:'#E63946'},{n:'BLEU',c:'#3A86FF'},{n:'VERT',c:'#06A77D'},{n:'JAUNE',c:'#F4B400'}];
  let score=0,streak=0,left=30,cur;
  inner().innerHTML=info('Touche la couleur de l\'<b>encre</b>, pas le mot écrit !')+
    `<p class="g-info" id="st-t">⏱ 30 s</p><div class="stroop-w" id="st-w"></div><div class="stroop-c">${C.map((x,i)=>`<button class="stroop-b" data-i="${i}" style="background:${x.c}" aria-label="${x.n}"></button>`).join('')}</div>`;
  function nextW(){const w=Math.floor(Math.random()*4);let ink;do{ink=Math.floor(Math.random()*4);}while(ink===w&&Math.random()<.8);
    cur=ink;const el=$('st-w');if(el){el.textContent=C[w].n;el.style.color=C[ink].c;}}
  document.querySelectorAll('.stroop-b').forEach(b=>b.addEventListener('pointerdown',e=>{
    e.preventDefault();if(left<=0)return;
    if(+b.dataset.i===cur){streak++;score+=10+Math.min(streak,5)*2;tone(660,.08);}else{streak=0;sndKO();}
    updateGameScore(score);nextW();
  }));
  _gInterval(()=>{left--;const t=$('st-t');if(t)t.textContent='⏱ '+left+' s';if(left===0){sndOK();_gTimeout(()=>endGame(score),500);}},1000);
  hideTimer();nextW();
};

// ── 6. SUDOKU JUNIOR (4×4 ou 6×6) ───────────────────────────────
JEUX_EXTRA.sudoku=function(){
  const N=AGE()<9?4:6,BR=N===4?2:2,BC=N===4?2:3;
  // grille résolue par motif puis mélange (lignes dans bandes, chiffres)
  let g=[...Array(N)].map((_,r)=>[...Array(N)].map((_,c)=>((r%BR)*BC+Math.floor(r/BR)+c)%N+1));
  const map=shuffle([...Array(N)].map((_,i)=>i+1));g=g.map(r=>r.map(v=>map[v-1]));
  for(let b=0;b<N/BR;b++){const idx=[...Array(BR)].map((_,i)=>b*BR+i);const cp=shuffle(idx.map(i=>g[i]));idx.forEach((ri,k)=>g[ri]=cp[k]);}
  const sol=g.map(r=>[...r]);const holes=N===4?(AGE()<7?5:7):14;
  const cells=shuffle([...Array(N*N).keys()]).slice(0,holes);
  const cur=sol.map(r=>[...r]);cells.forEach(i=>cur[Math.floor(i/N)][i%N]=0);
  let sel=null,errors=0,t0=Date.now();
  inner().innerHTML=info('Chaque chiffre <b>une seule fois</b> par ligne, par colonne et par bloc.')+
    `<div class="sudoku" id="sd" style="grid-template-columns:repeat(${N},1fr)"></div><div class="sd-pad">${[...Array(N)].map((_,i)=>`<button class="sd-n" data-v="${i+1}">${i+1}</button>`).join('')}</div>`;
  function render(){
    $('sd').innerHTML=cur.map((row,r)=>row.map((v,c)=>{const fixed=!cells.includes(r*N+c);
      const cls=['sd-c',fixed?'fx':'',sel===r*N+c?'sel':'',(c+1)%BC===0&&c<N-1?'br':'',(r+1)%BR===0&&r<N-1?'bb':''].join(' ');
      return `<button class="${cls}" data-i="${r*N+c}">${v||''}</button>`;}).join('')).join('');
    document.querySelectorAll('.sd-c:not(.fx)').forEach(b=>b.addEventListener('pointerdown',e=>{e.preventDefault();sel=+b.dataset.i;tone(440,.04);render();}));
  }
  document.querySelectorAll('.sd-n').forEach(b=>b.addEventListener('pointerdown',e=>{
    e.preventDefault();if(sel===null)return;const r=Math.floor(sel/N),c=sel%N,v=+b.dataset.v;
    if(sol[r][c]===v){cur[r][c]=v;tone(587,.08);cells.splice(cells.indexOf(sel),1);sel=null;render();
      if(!cells.length){const sec=(Date.now()-t0)/1000;const sc=Math.max(20,(N===4?80:150)-errors*10-Math.floor(sec/10));updateGameScore(sc);sndOK();try{celebrate();}catch(_){}_gTimeout(()=>endGame(sc),1200);}}
    else{errors++;sndKO();const el=document.querySelector(`.sd-c[data-i="${sel}"]`);if(el){el.classList.add('ko');_gTimeout(()=>el.classList.remove('ko'),400);}}
  }));
  hideTimer();render();
};

// ── 7. LABYRINTHE ───────────────────────────────────────────────
JEUX_EXTRA.laby=function(){
  let lvl=0,score=0;const base=AGE()<7?6:AGE()<11?8:10;
  inner().innerHTML=`<p class="g-big" id="lb-msg"></p><div id="lb-wrap" class="g-board"><canvas id="lb-c"></canvas></div><p class="g-help">Touche vers le haut, le bas, la gauche ou la droite (ou glisse) pour avancer jusqu'au 🏁.</p>`;
  let N,maze,me,t0,C,ctx;
  function gen(n){const w=[...Array(n)].map(()=>[...Array(n)].map(()=>({u:1,d:1,l:1,r:1,v:0})));
    const st=[[0,0]];w[0][0].v=1;
    while(st.length){const [x,y]=st[st.length-1];const nb=shuffle([[0,-1,'u','d'],[0,1,'d','u'],[-1,0,'l','r'],[1,0,'r','l']]).filter(([dx,dy])=>{const X=x+dx,Y=y+dy;return X>=0&&Y>=0&&X<n&&Y<n&&!w[Y][X].v;});
      if(!nb.length){st.pop();continue;}const [dx,dy,a,b]=nb[0];w[y][x][a]=0;w[y+dy][x+dx][b]=0;w[y+dy][x+dx].v=1;st.push([x+dx,y+dy]);}
    return w;}
  function start(){N=base+lvl*2;maze=gen(N);me={x:0,y:0};t0=Date.now();
    const avail=Math.min((inner().clientWidth||340)-8,420,window.innerHeight-250);C=Math.floor(avail/N);
    const cv=$('lb-c');cv.width=cv.height=C*N;$('lb-wrap').style.width=C*N+'px';ctx=cv.getContext('2d');
    $('lb-msg').textContent='Labyrinthe '+(lvl+1)+'/3';draw();}
  function draw(){const night=document.body.classList.contains('night');
    ctx.fillStyle=night?'#0d1117':'#F3F1FF';ctx.fillRect(0,0,C*N,C*N);
    ctx.strokeStyle=night?'#C8A040':'#5A52D5';ctx.lineWidth=Math.max(2,C/7);ctx.lineCap='round';ctx.beginPath();
    maze.forEach((row,y)=>row.forEach((c,x)=>{const X=x*C,Y=y*C;
      if(c.u){ctx.moveTo(X,Y);ctx.lineTo(X+C,Y);}if(c.l){ctx.moveTo(X,Y);ctx.lineTo(X,Y+C);}
      if(y===N-1&&c.d){ctx.moveTo(X,Y+C);ctx.lineTo(X+C,Y+C);}if(x===N-1&&c.r){ctx.moveTo(X+C,Y);ctx.lineTo(X+C,Y+C);}}));
    ctx.stroke();ctx.font=Math.floor(C*.7)+'px sans-serif';ctx.textAlign='center';ctx.textBaseline='middle';
    ctx.fillText('🏁',(N-.5)*C,(N-.5)*C);ctx.fillText('🐱',(me.x+.5)*C,(me.y+.5)*C+1);}
  function go(z){const d={u:[0,-1],d:[0,1],l:[-1,0],r:[1,0]}[z];if(!d||!maze[me.y][me.x]||maze[me.y][me.x][z])return;
    me.x+=d[0];me.y+=d[1];tone(500,.03);draw();
    if(me.x===N-1&&me.y===N-1){const sec=(Date.now()-t0)/1000;score+=30+Math.max(0,Math.round(40-sec));updateGameScore(score);sndOK();lvl++;
      if(lvl>=3)_gTimeout(()=>endGame(score),900);else _gTimeout(start,900);}}
  _gPad($('lb-wrap'),{center:false,swipe:true,repeat:['u','d','l','r'],on:go});
  window._gKeyFn=e=>{const m={ArrowUp:'u',ArrowDown:'d',ArrowLeft:'l',ArrowRight:'r'}[e.key];if(!m)return false;go(m);};
  hideTimer();start();
};

// ── 8. MOTS MÊLÉS (mots anglais de « Paires ») ──────────────────
JEUX_EXTRA.motsmeles=function(){
  const N=AGE()<8?7:9,count=AGE()<8?4:6,diag=AGE()>=10;
  const pool=shuffle(PAIRES_DATA.filter(p=>p[1].length<=N&&/^[A-Za-z]+$/.test(p[1]))).slice(0,count);
  const G=[...Array(N)].map(()=>Array(N).fill(''));const placed=[];
  const dirs=[[1,0],[0,1]].concat(diag?[[1,1]]:[]);
  pool.forEach(([fr,en])=>{const w=en.toUpperCase();
    for(let t=0;t<200;t++){const [dx,dy]=dirs[Math.floor(Math.random()*dirs.length)];
      const x=Math.floor(Math.random()*(N-dx*(w.length-1))),y=Math.floor(Math.random()*(N-dy*(w.length-1)));
      if([...w].every((ch,i)=>!G[y+dy*i][x+dx*i]||G[y+dy*i][x+dx*i]===ch)){[...w].forEach((ch,i)=>G[y+dy*i][x+dx*i]=ch);placed.push({w,fr,cells:[...w].map((_,i)=>(y+dy*i)*N+x+dx*i),f:0});break;}}});
  const AB='ABCDEFGHIJKLMNOPRSTUVWY';G.forEach(r=>r.forEach((c,i)=>{if(!c)r[i]=AB[Math.floor(Math.random()*AB.length)];}));
  let first=null,score=0;
  inner().innerHTML=info('Touche la <b>première</b> puis la <b>dernière</b> lettre d\'un mot.')+
    `<div class="mm" id="mm" style="grid-template-columns:repeat(${N},1fr)">${G.flat().map((c,i)=>`<button class="mm-c" data-i="${i}">${c}</button>`).join('')}</div>
    <div class="mm-list" id="mm-l">${placed.map((p,k)=>`<span id="mml${k}">${p.fr} → ?</span>`).join('')}</div>`;
  document.querySelectorAll('.mm-c').forEach(b=>b.addEventListener('pointerdown',e=>{
    e.preventDefault();const i=+b.dataset.i;
    if(first===null){first=i;b.classList.add('sel');tone(440,.04);return;}
    const a=first;first=null;document.querySelectorAll('.mm-c.sel').forEach(x=>x.classList.remove('sel'));
    const k=placed.findIndex(p=>!p.f&&((p.cells[0]===a&&p.cells[p.cells.length-1]===i)||(p.cells[0]===i&&p.cells[p.cells.length-1]===a)));
    if(k<0){sndKO();return;}
    const p=placed[k];p.f=1;p.cells.forEach(c=>document.querySelector(`.mm-c[data-i="${c}"]`).classList.add('f'+(k%5)));
    $('mml'+k).textContent=p.fr+' → '+p.w;$('mml'+k).classList.add('ok');score+=15;updateGameScore(score);sndOK();
    try{if(typeof speakWord==='function')speakWord(p.w.toLowerCase(),'EN');}catch(_){}
    if(placed.every(q=>q.f)){score+=20;updateGameScore(score);_gTimeout(()=>endGame(score),1200);}
  }));
  hideTimer();
};
})();
