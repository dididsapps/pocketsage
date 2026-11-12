// PocketSage — Mini-jeux (sorti de index.html le 12/11/2026)
// Chargé avant le script principal (variables et fonctions globales partagées).
// Contient : configuration + limites quotidiennes, moteur de jeu, les 12 mini-jeux.
// ════════════════════════════════════════════
// JEUX — CONFIG & DAILY LIMITS
// ════════════════════════════════════════════
const JEUX_CFG=[
  {id:'memory',     emoji:'🃏', title:'Memory',        desc:'Retourne les paires',    min_score:0},
  {id:'calcul',     emoji:'⚡', title:'Calcul Éclair',  desc:'Calcul mental rapide',   min_score:0},
  {id:'quiz',       emoji:'🧩', title:'Quiz Rapidité',  desc:'Réponds vite !',         min_score:0},
  {id:'mastermind', emoji:'🎯', title:'Mastermind',     desc:'Déchiffre le code',      min_score:0},
  {id:'paires',     emoji:'🔗', title:'Paires FR↔Ang',  desc:'Associe les traductions',min_score:0},
  {id:'anagrammes', emoji:'🔤', title:'Anagrammes',     desc:'Retrouve le mot',        min_score:0},
  {id:'motcache',   emoji:'🔍', title:'Mot Caché',      desc:'Cherche les mots',       min_score:0},
  {id:'snake',      emoji:'🐍', title:'Snake QCM',      desc:'Mange les bonnes réponses',min_score:0},
  {id:'sort',       emoji:'✨', title:'Magic Sort',     desc:'Classe les éléments',    min_score:0},
  {id:'taquin',     emoji:'🧩', title:'Puzzle coulissant',desc:'Remets dans l\'ordre', min_score:0},
  {id:'hanoi',      emoji:'🗼', title:'Tour de Hanoï',  desc:'Déplace les disques',    min_score:0},
  {id:'blocs',      emoji:'🧱', title:'Blocs Sensei',   desc:'Complète des lignes avec les blocs qui tombent',min_score:0},
  {id:'g2048',      emoji:'💣', title:'Bombe de Mots',  desc:'Trouve le mot avant l\'explosion !',min_score:0},
];
const JEUX_DAILY_MAX=20*60*1000; // 20 min en ms
const JEUX_KEY='psa3_jeux';

function getJeuxState(){
  try{return JSON.parse(localStorage.getItem(JEUX_KEY)||'{}');}catch(e){return{};}
}
function saveJeuxState(st){localStorage.setItem(JEUX_KEY,JSON.stringify(st));}

function getJeuxProfile(){
  const p=P();if(!p)return null;
  const st=getJeuxState();
  const pid=APP.cur;
  if(!st[pid])st[pid]={hs:{},daily:{},date:''};
  const today=new Date().toISOString().slice(0,10);
  if(st[pid].date!==today){st[pid].daily={};st[pid].date=today;saveJeuxState(st);}
  return {st,pid,today};
}

function getHighscore(gameId){
  const jp=getJeuxProfile();if(!jp)return 0;
  const {st,pid}=jp;
  return (st[pid]&&st[pid].hs&&st[pid].hs[gameId])||0;
}
function setHighscore(gameId,score){
  const jp=getJeuxProfile();if(!jp)return;
  const {st,pid}=jp;
  if(!st[pid].hs)st[pid].hs={};
  if(score>(st[pid].hs[gameId]||0)){st[pid].hs[gameId]=score;saveJeuxState(st);}
}
function getDailyMs(gameId){
  const jp=getJeuxProfile();if(!jp)return 0;
  const {st,pid}=jp;
  return (st[pid]&&st[pid].daily&&st[pid].daily[gameId])||0;
}
function addDailyMs(gameId,ms){
  const jp=getJeuxProfile();if(!jp)return;
  const {st,pid}=jp;
  if(!st[pid].daily)st[pid].daily={};
  st[pid].daily[gameId]=(st[pid].daily[gameId]||0)+ms;
  saveJeuxState(st);
}
// ── Limite de jeu TOTALE (tous jeux confondus) ─────────────────────
// Offre gratuite : 15 min/jour (fixe). Abonnés : 45 min par défaut, réglable par le parent (jusqu'à illimité).
// Tant que les abonnements n'existent pas (bêta), tout le monde est traité comme abonné.
function psaPlan(){try{return localStorage.getItem('psa3_plan')||'famille';}catch(e){return 'famille';}}
function isFreePlan(){return psaPlan()==='gratuit';}
function jeuxLimitMin(){if(isFreePlan())return 15;const p=P();const v=p&&p.jeuxMin;return (v===0||v>0)?v:45;} // 0 = illimité
function jeuxLimitMs(){const m=jeuxLimitMin();return m===0?Infinity:m*60000;}
function totalDailyMs(){const jp=getJeuxProfile();if(!jp)return 0;const d=(jp.st[jp.pid]&&jp.st[jp.pid].daily)||{};
  let t=Object.values(d).reduce((a,c)=>a+(+c||0),0);if(GAME&&GAME.startMs&&GAME.id)t+=Date.now()-GAME.startMs;return t;}
function jeuxLeftMs(){return Math.max(0,jeuxLimitMs()-totalDailyMs());}
function isDailyFull(gameId){return jeuxLeftMs()<=0;}
function setJeuxMin(v){const p=P();if(!p)return;p.jeuxMin=+v;saveApp();try{_showParentPanel();}catch(e){}}
function _jeuxWarnedToday(set){const jp=getJeuxProfile();if(!jp)return true;const o=jp.st[jp.pid];if(set){o.warned=jp.today;saveJeuxState(jp.st);}return o.warned===jp.today;}
function _jeuxWatch(){ // toutes les 5 s pendant une partie
  const left=jeuxLeftMs();if(left===Infinity)return;
  if(left<=5*60000&&left>0&&!_jeuxWarnedToday()){_jeuxWarnedToday(true);try{toast('⏰ Plus que 5 minutes de jeu aujourd\'hui !');}catch(e){}try{sndStar();}catch(e){}}
  if(left<=0){GAME.timeUp=true;endGame(GAME.score||0);}
  else{const el=document.getElementById('game-daily-left');if(el){const m=Math.ceil(left/60000);el.textContent=m+' min de jeu restantes aujourd\'hui';}}
}
// Écran « temps écoulé » : fiche PDF toujours ; histoire et QCM si l'offre le permet.
function jeuxTimeUpHTML(){
  const free=isFreePlan();
  return `<div class="jeux-timeup">
    <div style="font-size:42px">⏰</div>
    <h3>C'est fini pour les jeux aujourd'hui !</h3>
    <p>Tu as bien joué. Et si on continuait autrement ?</p>
    <button class="go-btn tu-pdf" onclick="openAteliers()">🖨️ Une fiche à imprimer (atelier)</button>
    ${free?`<p class="tu-free">📚 Histoires et questions en plus : avec l'abonnement Famille.</p>`:
      `<button class="go-btn tu-story" onclick="openNuit()">🌙 Écouter une histoire</button>
       <button class="go-btn tu-qcm" onclick="startAdventure()">🗺️ Une aventure de questions</button>`}
    <button class="go-btn" style="background:var(--bg);color:var(--tl)" onclick="goHome()">🏠 Accueil</button>
  </div>`;
}

function openJeux(){
  try{
  show('jeux');
  const hsc=document.getElementById('jeux-hsc');if(hsc)hsc.textContent='⭐ '+(P()?P().score:0);
  try{buildProfBar('jeux-pb');}catch(e){}
  const score=P()?P().score:0;
  const grid=document.getElementById('jeux-grid');grid.innerHTML='';
  JEUX_CFG.forEach(g=>{
    const locked=score<g.min_score;
    const hs=getHighscore(g.id);
    const pct=0;
    const card=document.createElement('button');
    card.className='jeu-card'+(locked?' locked':'');
    card.innerHTML=`<span class="je">${g.emoji}</span>
      <span class="jt">${g.title}</span>
      <span class="js">${g.desc}</span>
      ${hs>0?`<span class="jhs">🏆 Record : ${hs}</span>`:''}
      ${locked?`<span class="jeu-lock-badge">🔒 ${g.min_score}⭐</span>`:''}
      `;
    if(!locked){
      if(isDailyFull(g.id)){
        card.disabled=true;
        card.querySelector('.js').textContent='Temps de jeu terminé (revient à minuit)';
      } else {
        card.onclick=()=>{sndTap();startGame(g.id);};
      }
    }
    grid.appendChild(card);
  });
  // Daily banner
  const banner=document.getElementById('jeux-daily-banner');
  const totalLeft=jeuxLeftMs();
  if(banner){
    if(totalLeft<=0){banner.style.display='block';banner.innerHTML='⏰ Temps de jeu terminé pour aujourd\'hui ! <button class="tu-inline" onclick="startGame(\'memory\')">Que faire maintenant ?</button>';}
    else if(totalLeft!==Infinity){banner.style.display='block';banner.textContent='⏱ '+Math.ceil(totalLeft/60000)+' min de jeu restantes aujourd\'hui'+(isFreePlan()?' (offre gratuite : 15 min)':'');}
    else banner.style.display='none';
  }
  }catch(e){console.error('openJeux:',e);toast('Erreur jeux: '+e.message,'err');}
}

// buildProfBar est défini plus haut (version unifiée, accepte containerId optionnel)

// ════════════════════════════════════════════
// GAME ENGINE
// ════════════════════════════════════════════
let GAME={id:'',score:0,startMs:0,timerInt:null,sessionInt:null};

// Minuteurs des mini-jeux : tous arrêtés quand on quitte le jeu, qu'on en lance un autre ou qu'on change d'écran
let _gInts=[];
function _gInterval(fn,ms){const id=setInterval(fn,ms);_gInts.push(id);return id;}
let _gTos=[];
function _gTimeout(fn,ms){const id=setTimeout(fn,ms);_gTos.push(id);return id;}
function _gClearAll(){window._gKeyFn=null;_gTos.forEach(clearTimeout);_gTos=[];_gInts.forEach(clearInterval);_gInts=[];if(typeof GAME==='object'&&GAME){if(GAME.timerInt)clearInterval(GAME.timerInt);if(GAME.sessionInt)clearInterval(GAME.sessionInt);}}

// Clavier (tablette avec clavier, ordinateur) — une seule écoute, fonction remplacée par jeu
document.addEventListener('keydown',e=>{if(window._gKeyFn){if(window._gKeyFn(e)!==false)e.preventDefault();}});
// Pavé tactile géant : la zone de jeu est coupée en 4 triangles (haut/bas/gauche/droite)
// + option un rond central (pivot). Grosses flèches transparentes qui s'éclairent au toucher.
// opts : {center:true|false, on:fn(z) avec z='u'|'d'|'l'|'r'|'m', repeat:['l','r','d'], swipe:true}
function _gPad(wrap,opts){
  const ov=document.createElement('div');ov.className='gpad';
  ov.innerHTML='<span class="gp gp-u">▲</span><span class="gp gp-d">▼</span><span class="gp gp-l">◀</span><span class="gp gp-r">▶</span>'+(opts.center?'<span class="gp gp-m">↻</span>':'');
  wrap.appendChild(ov);
  const el={};ov.querySelectorAll('.gp').forEach(x=>{el[x.className.split('gp-')[1]]=x;});
  function flash(z){const x=el[z];if(!x)return;x.classList.add('on');_gTimeout(()=>x.classList.remove('on'),160);}
  function zone(e){const r=ov.getBoundingClientRect();const x=(e.clientX-r.left)/r.width-.5,y=(e.clientY-r.top)/r.height-.5;
    if(opts.center&&Math.hypot(x*r.width,y*r.height)<Math.min(r.width,r.height)*0.2)return 'm';
    return Math.abs(x)>Math.abs(y)?(x<0?'l':'r'):(y<0?'u':'d');}
  let rep=null,rep0=null,sx=0,sy=0,first=null;
  function stop(){if(rep0){clearTimeout(rep0);rep0=null;}if(rep){clearInterval(rep);rep=null;}}
  ov.addEventListener('pointerdown',e=>{e.preventDefault();sx=e.clientX;sy=e.clientY;const z=zone(e);first=z;flash(z);opts.on(z);
    if(opts.repeat&&opts.repeat.includes(z)){stop();rep0=_gTimeout(()=>{rep=_gInterval(()=>opts.on(z),z==='d'?55:85);},230);}});
  ov.addEventListener('pointerup',e=>{stop();
    if(opts.swipe){const dx=e.clientX-sx,dy=e.clientY-sy;if(Math.max(Math.abs(dx),Math.abs(dy))>35){const z=Math.abs(dx)>Math.abs(dy)?(dx<0?'l':'r'):(dy<0?'u':'d');if(z!==first){flash(z);opts.on(z);}}}});
  ov.addEventListener('pointercancel',stop);ov.addEventListener('pointerleave',stop);
  ov.addEventListener('contextmenu',e=>e.preventDefault());
  return ov;
}
function startGame(id){
  _gClearAll();
  if(isDailyFull(id)){show('game');document.getElementById('game-title').textContent='⏰ Jeux';document.getElementById('game-inner').innerHTML=jeuxTimeUpHTML();return;}
  GAME={id,score:0,startMs:Date.now(),timerInt:null,sessionInt:null};
  GAME.sessionInt=setInterval(_jeuxWatch,5000);
  const cfg=JEUX_CFG.find(g=>g.id===id);
  document.getElementById('game-title').textContent=cfg?cfg.emoji+' '+cfg.title:'Jeu';
  document.getElementById('game-score').textContent='0';
  document.getElementById('game-hsc').textContent='⭐ '+(P()?P().score:0);
  updateGameDailyLeft(id);
  show('game');
  // Dispatch to game builder
  const fn={memory:buildMemory,calcul:buildCalcul,quiz:buildQuizRapid,
    mastermind:buildMastermind,paires:buildPaires,anagrammes:buildAnagrammes,
    motcache:buildMotCache,snake:buildSnake,sort:buildSort,
    taquin:buildTaquin,hanoi:buildHanoi,g2048:build2048,blocs:buildBlocs}[id]||(window.JEUX_EXTRA&&JEUX_EXTRA[id]);
  if(fn)fn();
}

function updateGameDailyLeft(id){
  const left=jeuxLeftMs();
  document.getElementById('game-daily-left').textContent=left===Infinity?'Temps de jeu illimité':`${Math.ceil(left/60000)} min de jeu restantes aujourd\'hui`;
}

function updateGameScore(s){
  GAME.score=s;
  document.getElementById('game-score').textContent=s;
}

function endGame(finalScore){
  _gClearAll();
  // Record time played
  const elapsed=GAME.startMs?Date.now()-GAME.startMs:0;
  addDailyMs(GAME.id,elapsed);GAME.startMs=0;
  if(isDailyFull()){const dl=document.getElementById('game-daily-left');if(dl)dl.textContent='Temps de jeu terminé';}
  // Highscore
  const prevHs=getHighscore(GAME.id);
  setHighscore(GAME.id,finalScore);
  const isNew=finalScore>prevHs&&prevHs>0;
  // Award stars
  const starsEarned=Math.floor(finalScore/10);
  if(starsEarned>0&&P()){P().score+=starsEarned;saveApp();}
  if(GAME.timerInt)clearInterval(GAME.timerInt);
  if(GAME.sessionInt)clearInterval(GAME.sessionInt);
  // Show game over
  const inner=document.getElementById('game-inner');
  inner.innerHTML=`<div class="game-over">
    <div class="go-emoji">${finalScore>=50?'🏆':'🎮'}</div>
    <h2>${finalScore>=50?'Excellent !':'Bien joué !'}</h2>
    <div class="go-score">Score : ${finalScore}</div>
    <div class="go-hs">${isNew?'🎉 Nouveau record !':'Record : '+getHighscore(GAME.id)}</div>
    ${starsEarned>0?`<div style="color:var(--y);font-weight:800;margin-bottom:12px">+${starsEarned} ⭐</div>`:''}
    ${isDailyFull()?jeuxTimeUpHTML():`<button class="go-btn" style="background:var(--v);color:#fff" onclick="startGame('${GAME.id}')">🔄 Rejouer</button>
    <button class="go-btn" style="background:var(--bg);color:var(--tl)" onclick="openJeux()">← Jeux</button>`}
  </div>`;
  if(finalScore>=50){celebrate();sndStar();senseiDance();}
}

function quitGame(){
  _gClearAll();
  if(GAME.timerInt)clearInterval(GAME.timerInt);
  if(GAME.sessionInt)clearInterval(GAME.sessionInt);
  const elapsed=Date.now()-(GAME.startMs||Date.now());
  if(elapsed>3000)addDailyMs(GAME.id,elapsed);
  openJeux();
}

function setGameTimer(seconds,onEnd){
  document.getElementById('game-timer-disp').style.display='';
  document.getElementById('game-timer-val').textContent=seconds;
  GAME.timerInt=setInterval(()=>{
    seconds--;
    document.getElementById('game-timer-val').textContent=seconds;
    if(seconds<=0){clearInterval(GAME.timerInt);onEnd();}
  },1000);
}

// ════════════════════════════════════════════
// GAME 1 — MEMORY
// ════════════════════════════════════════════
function buildMemory(){
  const age=P()?P().age:8;
  const pairs=age<7?4:age<11?6:8;
  const emojis=['🐶','🐱','🐭','🐹','🐰','🦊','🐻','🐼','🦁','🐯','🐸','🐧','🦋','🌸','🍕','🎸','🚀','🌈','⚡','🎯'].slice(0,pairs);
  const cards=[...emojis,...emojis].sort(()=>Math.random()-.5);
  let flipped=[],matched=[],moves=0,score=0,busy=false;
  const cols=pairs<=4?3:pairs<=6?4:5;
  const inner=document.getElementById('game-inner');
  inner.innerHTML=`<p style="text-align:center;font-size:13px;color:var(--tl);font-weight:700;margin-bottom:6px">Paires : <span id="mem-pairs">0</span>/${pairs} · Coups : <span id="mem-moves">0</span></p>
  <div class="mem-grid" style="grid-template-columns:repeat(${cols},1fr)">
  ${cards.map((e,i)=>`<div class="mem-card" id="mc${i}" onclick="memClick(${i})">
    <div class="mem-card-front"></div>
    <div class="mem-card-back">${e}</div>
  </div>`).join('')}
  </div>`;

  window.memClick=function(i){
    if(busy||flipped.length>=2||flipped.includes(i)||matched.includes(i))return;
    const el=document.getElementById('mc'+i);
    el.classList.add('flipped');flipped.push(i);sndTap();
    if(flipped.length===2){
      busy=true;
      moves++;document.getElementById('mem-moves').textContent=moves;
      const [a,b]=flipped;
      if(cards[a]===cards[b]){
        matched.push(a,b);sndOK();
        _gTimeout(()=>{
          document.getElementById('mc'+a).classList.add('matched');
          document.getElementById('mc'+b).classList.add('matched');
        },200);
        score+=10;updateGameScore(score);
        document.getElementById('mem-pairs').textContent=matched.length/2;
        flipped=[];busy=false;
        if(matched.length===cards.length)_gTimeout(()=>endGame(score),700);
      } else {
        _gTimeout(()=>{
          document.getElementById('mc'+a).classList.remove('flipped');
          document.getElementById('mc'+b).classList.remove('flipped');
          flipped=[];sndKO();busy=false;
        },1000);
      }
    }
  };
  document.getElementById('game-timer-disp').style.display='none';
}

// ════════════════════════════════════════════
// GAME 2 — CALCUL ÉCLAIR
// ════════════════════════════════════════════
function buildCalcul(){
  const age=P()?P().age:8;
  let score=0,streak=0,total=15;
  const inner=document.getElementById('game-inner');
  function genQ(){
    const ops=age<7?['+']:age<10?['+','-']:['+',' -','×'];
    const op=ops[Math.floor(Math.random()*ops.length)];
    let a,b,ans;
    if(op==='+'){a=Math.floor(Math.random()*(age<7?6:age<10?20:50))+1;b=Math.floor(Math.random()*(age<7?6:age<10?20:50))+1;ans=a+b;}
    else if(op==='-'||op===' -'){a=Math.floor(Math.random()*30)+10;b=Math.floor(Math.random()*a)+1;ans=a-b;}
    else{a=Math.floor(Math.random()*9)+2;b=Math.floor(Math.random()*9)+2;ans=a*b;}
    const wrong=[ans-1,ans+1,ans+2,ans-2].filter(x=>x!==ans&&x>0);
    const choices=[ans,...wrong.slice(0,3)].sort(()=>Math.random()-.5);
    return{label:`${a} ${op} ${b} = ?`,ans,choices};
  }
  let q=genQ();let remaining=total;let canClick=true;
  function render(){
    inner.innerHTML=`<div class="calc-big">${q.label}</div>
      <p class="calc-streak">🔥 Série : ${streak} · Restant : ${remaining}</p>
      <div class="calc-input-row">${q.choices.map(c=>`<button class="calc-btn" onclick="calcAns(${c})">${c}</button>`).join('')}</div>`;
    window.calcAns=function(v){
      if(!canClick)return;canClick=false;
      const btns=document.querySelectorAll('.calc-btn');
      btns.forEach(b=>{if(Number(b.textContent)===q.ans)b.classList.add('ok');});
      if(v===q.ans){sndOK();streak++;score+=10+Math.min(streak,5)*2;updateGameScore(score);}
      else{sndKO();streak=0;btns.forEach(b=>{if(Number(b.textContent)===v)b.classList.add('ko');});}
      remaining--;
      _gTimeout(()=>{canClick=true;if(remaining<=0)endGame(score);else{q=genQ();render();}},700);
    };
  }
  render();
  document.getElementById('game-timer-disp').style.display='none';
}

// ════════════════════════════════════════════
// GAME 3 — QUIZ RAPIDITÉ
// ════════════════════════════════════════════
const QUIZ_DATA=[
  {q:'Combien font 7 × 8 ?',a:'56',c:['56','48','54','63']},
  {q:'Capitale de France ?',a:'Paris',c:['Paris','Lyon','Marseille','Nice']},
  {q:'Combien de planètes dans le système solaire ?',a:'8',c:['8','9','7','10']},
  {q:'Quel animal est le plus grand ?',a:'Baleine bleue',c:['Éléphant','Girafe','Baleine bleue','Requin baleine']},
  {q:'Combien font 15 + 27 ?',a:'42',c:['42','41','43','40']},
  {q:'Quelle est la couleur du ciel ?',a:'Bleu',c:['Vert','Bleu','Rouge','Jaune']},
  {q:'Combien de côtés a un hexagone ?',a:'6',c:['5','6','7','8']},
  {q:'Quel est le plus grand océan ?',a:'Pacifique',c:['Atlantique','Indien','Pacifique','Arctique']},
  {q:'Combien font 12 × 12 ?',a:'144',c:['144','132','148','140']},
  {q:'Où se trouve la Tour Eiffel ?',a:'Paris',c:['Rome','Paris','Londres','Madrid']},
  {q:'Combien font 100 ÷ 4 ?',a:'25',c:['20','25','30','22']},
  {q:'Quel gaz respirons-nous ?',a:'Oxygène',c:['Azote','CO2','Oxygène','Hydrogène']},
  {q:'Combien de jours dans une année ?',a:'365',c:['364','365','366','360']},
  {q:'Quel est le fleuve le plus long du monde ?',a:'Nil',c:['Amazone','Nil','Congo','Yangtsé']},
  {q:'Combien font 9 × 9 ?',a:'81',c:['81','72','88','80']},
];
function buildQuizRapid(){
  const qs=[...QUIZ_DATA].sort(()=>Math.random()-.5).slice(0,10);
  let idx=0,score=0,canAns=true;
  const inner=document.getElementById('game-inner');
  let barInt;
  function renderQ(){
    if(barInt)clearInterval(barInt);
    if(idx>=qs.length){endGame(score);return;}
    const q=qs[idx];let t=10,canClick=true;
    inner.innerHTML=`<div class="quiz-timer-bar-wrap"><div class="quiz-timer-bar" id="qtbar" style="width:100%"></div></div>
      <p style="text-align:center;font-size:12px;color:var(--tl);font-weight:700">${idx+1}/${qs.length}</p>
      <div class="quiz-q">${q.q}</div>
      <div class="quiz-choices">${q.c.map(ch=>`<button class="quiz-btn" onclick="qAns('${ch}')">${ch}</button>`).join('')}</div>`;
    window.qAns=function(v){
      if(!canClick)return;canClick=false;clearInterval(barInt);
      document.querySelectorAll('.quiz-btn').forEach(b=>{
        if(b.textContent===q.a)b.classList.add('correct');
        else if(b.textContent===v&&v!==q.a)b.classList.add('wrong');
      });
      if(v===q.a){sndOK();score+=10+Math.max(0,t)*1;updateGameScore(score);}else{sndKO();}
      _gTimeout(()=>{idx++;renderQ();},900);
    };
    barInt=_gInterval(()=>{t--;const _qb=document.getElementById('qtbar');if(!_qb){clearInterval(barInt);return;}_qb.style.width=(t/10*100)+'%';if(t<=0){clearInterval(barInt);if(canClick){canClick=false;sndKO();_gTimeout(()=>{idx++;renderQ();},700);}}},1000);
  }
  renderQ();
  document.getElementById('game-timer-disp').style.display='none';
}

// ════════════════════════════════════════════
// GAME 4 — MASTERMIND
// ════════════════════════════════════════════
function buildMastermind(){
  const COLORS=['🔴','🔵','🟡','🟢','🟠','🟣'];
  const CODE=Array.from({length:4},()=>COLORS[Math.floor(Math.random()*COLORS.length)]);
  let curRow=0,curSlot=0,selected=COLORS[0];
  const maxRows=8;const grid=Array.from({length:maxRows},()=>Array(4).fill(''));
  const inner=document.getElementById('game-inner');
  let score=80;
  const HELP=`<div style="background:var(--vl);border-radius:12px;padding:10px 14px;margin-bottom:10px;font-size:12px;line-height:1.6;color:var(--t)">
    <b>🎯 Comment jouer ?</b><br>
    Trouve le code secret de 4 couleurs en 8 essais.<br>
    1️⃣ Sélectionne une couleur en haut → clique <b>Placer</b> → répète 4×<br>
    2️⃣ Clique <b>Valider</b> pour voir les indices :<br>
    <span style="background:#333;border-radius:50%;display:inline-block;width:10px;height:10px"></span> Bonne couleur, bonne position &nbsp;
    <span style="background:#aaa;border-radius:50%;display:inline-block;width:10px;height:10px"></span> Bonne couleur, mauvaise position
  </div>`;
  function render(){
    inner.innerHTML=`${curRow===0?HELP:''}
    <div class="mm-colors">${COLORS.map(c=>`<div class="mm-color-btn${c===selected?' cur':''}" onclick="mmSel('${c}')">${c}</div>`).join('')}</div>
    <div id="mm-rows">${renderRows()}</div>
    <div style="display:flex;gap:8px;justify-content:center;margin-top:8px">
      <button class="adv-continue-btn" style="padding:12px 24px;font-size:14px" onclick="mmPlace()">Placer</button>
      <button class="adv-continue-btn" style="padding:12px 24px;font-size:14px;background:var(--c)" onclick="mmCheck()">Valider</button>
    </div>`;
    window.mmSel=function(c){selected=c;render();};
    window.mmPlace=function(){
      if(curSlot>=4)return;
      grid[curRow][curSlot]=selected;curSlot++;
      document.getElementById('mm-rows').innerHTML=renderRows();
    };
    window.mmCheck=function(){
      if(curSlot<4){toast('🎯 Remplis tous les slots !');return;}
      const row=grid[curRow];
      let black=0,white=0;
      const codeCopy=[...CODE],rowCopy=[...row];
      for(let i=0;i<4;i++){if(rowCopy[i]===codeCopy[i]){black++;codeCopy[i]=null;rowCopy[i]=null;}}
      for(let i=0;i<4;i++){if(rowCopy[i]){const j=codeCopy.indexOf(rowCopy[i]);if(j>=0){white++;codeCopy[j]=null;}}}
      if(black===4){updateGameScore(score);endGame(score);return;}
      score=Math.max(0,score-8);updateGameScore(score);
      curRow++;curSlot=0;
      if(curRow>=maxRows){
        inner.innerHTML+=`<div style="text-align:center;padding:12px;font-size:14px;font-weight:700;color:var(--c)">Code : ${CODE.join(' ')}</div>`;
        endGame(score);return;
      }
      render();
    };
  }
  function renderRows(){
    return grid.map((row,ri)=>{
      const isActive=ri===curRow;const isDone=ri<curRow;
      let hints='';
      if(isDone){
        const codeCopy=[...CODE],rowCopy=[...row];let b=0,w=0;
        for(let i=0;i<4;i++){if(rowCopy[i]===codeCopy[i]){b++;codeCopy[i]=null;rowCopy[i]=null;}}
        for(let i=0;i<4;i++){if(rowCopy[i]){const j=codeCopy.indexOf(rowCopy[i]);if(j>=0){w++;codeCopy[j]=null;}}}
        const hArr=[...Array(b).fill('black'),...Array(w).fill('white'),...Array(4-b-w).fill('')];
        hints=`<div class="mm-hints">${hArr.map(h=>`<div class="mm-hint ${h}"></div>`).join('')}</div>`;
      }
      return `<div class="mm-row" style="opacity:${isActive||isDone?1:.4}">
        ${row.map((c,si)=>`<div class="mm-slot${isActive&&si===curSlot-1?' selected':''}" style="${c?'':'background:var(--bg)'}">${c||''}</div>`).join('')}
        ${hints}
      </div>`;
    }).join('');
  }
  render();
  document.getElementById('game-timer-disp').style.display='none';
}

// ════════════════════════════════════════════
// GAME 5 — PAIRES FR↔ANG
// ════════════════════════════════════════════
const PAIRES_DATA=[
  ['Chien','Dog'],['Chat','Cat'],['Maison','House'],['Pomme','Apple'],['Livre','Book'],
  ['École','School'],['Voiture','Car'],['Eau','Water'],['Soleil','Sun'],['Lune','Moon'],
  ['Arbre','Tree'],['Fleur','Flower'],['Table','Table'],['Chaise','Chair'],['Porte','Door'],
];
function buildPaires(){
  const pairs=PAIRES_DATA.sort(()=>Math.random()-.5).slice(0,6);
  const fr=pairs.map(p=>p[0]).sort(()=>Math.random()-.5);
  const en=pairs.map(p=>p[1]).sort(()=>Math.random()-.5);
  let selFr=null,score=0,matched=[];
  const inner=document.getElementById('game-inner');
  function render(){
    inner.innerHTML=`<div class="pairs-grid">
      <div><h4>🇫🇷 Français</h4>${fr.map((w,i)=>`<button class="pair-btn${matched.includes('fr'+i)?' matched':''}" id="pfr${i}" onclick="pairSel('fr',${i})">${w}</button>`).join('')}</div>
      <div><h4>🇬🇧 Anglais</h4>${en.map((w,i)=>`<button class="pair-btn${matched.includes('en'+i)?' matched':''}" id="pen${i}" onclick="pairSel('en',${i})">${w}</button>`).join('')}</div>
    </div>`;
    window.pairSel=function(lang,i){
      if(matched.includes(lang+i))return;
      const el=document.getElementById(`p${lang}${i}`);
      if(lang==='fr'){
        if(selFr!==null)document.getElementById(`pfr${selFr}`).classList.remove('selected');
        selFr=i;el.classList.add('selected');
      } else {
        if(selFr===null)return;
        const frWord=fr[selFr],enWord=en[i];
        const match=pairs.find(p=>p[0]===frWord&&p[1]===enWord);
        if(match){
          sndOK();score+=15;updateGameScore(score);
          matched.push('fr'+selFr,'en'+i);
          document.getElementById(`pfr${selFr}`).className='pair-btn matched';
          el.className='pair-btn matched';selFr=null;
          if(matched.length===pairs.length*2)_gTimeout(()=>endGame(score),500);
          else render();
        } else {
          sndKO();el.classList.add('wrong');
          document.getElementById(`pfr${selFr}`).className='pair-btn';
          selFr=null;
          _gTimeout(()=>{el.classList.remove('wrong');render();},600);
        }
      }
    };
  }
  render();
  document.getElementById('game-timer-disp').style.display='none';
}

// ════════════════════════════════════════════
// GAME 6 — ANAGRAMMES CHRONO
// ════════════════════════════════════════════
const ANA_WORDS=[
  {w:'CHIEN',h:'Animal qui aboie'},
  {w:'MAISON',h:'On y habite'},
  {w:'SOLEIL',h:'Étoile du jour'},
  {w:'FLEUR',h:'Pousse dans le jardin'},
  {w:'ECOLE',h:'On y apprend'},
  {w:'LAPIN',h:'Animal à longues oreilles'},
  {w:'TABLE',h:'Meuble pour manger'},
  {w:'LIVRE',h:'On le lit'},
  {w:'ARBRE',h:'Il a des feuilles'},
  {w:'LUNE',h:'Satellite de la Terre'},
];
function buildAnagrammes(){
  const words=[...ANA_WORDS].sort(()=>Math.random()-.5).slice(0,5);
  let idx=0,score=0;
  const inner=document.getElementById('game-inner');
  function nextWord(){
    if(idx>=words.length){endGame(score);return;}
    const word=words[idx].w;const hint=words[idx].h;
    const shuffled=[...word].sort(()=>Math.random()-.5);
    let answer=[];let usedIdx=[];
    function render(){
      inner.innerHTML=`<p style="text-align:center;font-size:12px;color:var(--tl);font-weight:700">Mot ${idx+1}/${words.length} · Indice : ${hint}</p>
        <div class="ana-answer" id="ana-ans">${answer.map((l,i)=>`<div class="ana-slot filled" onclick="anaRemove(${i})">${l}</div>`).join('')}${Array(word.length-answer.length).fill('<div class="ana-slot"></div>').join('')}</div>
        <div class="ana-word">${shuffled.map((l,i)=>`<div class="ana-letter${usedIdx.includes(i)?' used':''}" onclick="anaAdd(${i},'${l}')">${l}</div>`).join('')}</div>
        <div style="display:flex;gap:8px;justify-content:center">
          <button class="adv-continue-btn" style="padding:10px 20px;font-size:14px" onclick="anaValidate()">✓ Valider</button>
          <button class="adv-continue-btn" style="padding:10px 20px;font-size:14px;background:var(--tl)" onclick="anaClear()">✕ Effacer</button>
        </div>`;
      window.anaAdd=function(i,l){if(usedIdx.includes(i)||answer.length>=word.length)return;usedIdx.push(i);answer.push(l);render();};
      window.anaRemove=function(i){if(i>=answer.length)return;usedIdx.splice(usedIdx.findIndex((_,j)=>j>=i),1);answer.splice(i,1);render();};
      window.anaClear=function(){answer=[];usedIdx=[];render();};
      window.anaValidate=function(){
        if(answer.join('')===word){sndOK();score+=20;updateGameScore(score);celebrate();idx++;_gTimeout(nextWord,600);}
        else{sndKO();inner.querySelectorAll('.ana-slot.filled').forEach(e=>e.style.color='var(--c)');_gTimeout(()=>{answer=[];usedIdx=[];render();},800);}
      };
    }
    render();
  }
  nextWord();
  setGameTimer(60,()=>endGame(score));
}

// ════════════════════════════════════════════
// GAME 7 — MOT CACHÉ
// ════════════════════════════════════════════
const MOTCACHE_DATA=[
  {words:['CHAT','CHIEN','LAPIN','VACHE','POULE'],theme:'Animaux'},
  {words:['ROUGE','BLEU','VERT','JAUNE','NOIR'],theme:'Couleurs'},
  {words:['POMME','POIRE','CERISE','RAISIN','BANANE'],theme:'Fruits'},
];
function buildMotCache(){
  const data=MOTCACHE_DATA[Math.floor(Math.random()*MOTCACHE_DATA.length)];
  const SIZE=10;const words=data.words;
  const grid=Array.from({length:SIZE},()=>Array(SIZE).fill(''));
  const placed=[];
  const dirs=[[0,1],[1,0],[1,1],[0,-1],[-1,0]];
  function placeWord(word){
    for(let t=0;t<50;t++){
      const dir=dirs[Math.floor(Math.random()*dirs.length)];
      const r=Math.floor(Math.random()*SIZE);const c=Math.floor(Math.random()*SIZE);
      let ok=true;const cells=[];
      for(let i=0;i<word.length;i++){
        const nr=r+dir[0]*i,nc=c+dir[1]*i;
        if(nr<0||nr>=SIZE||nc<0||nc>=SIZE){ok=false;break;}
        if(grid[nr][nc]&&grid[nr][nc]!==word[i]){ok=false;break;}
        cells.push([nr,nc]);
      }
      if(ok){cells.forEach(([nr,nc],i)=>{grid[nr][nc]=word[i];});placed.push({word,cells});return true;}
    }
    return false;
  }
  words.forEach(placeWord);
  const ALPHA='ABCDEFGHIJKLMNOPQRSTUVWXYZ';
  for(let r=0;r<SIZE;r++)for(let c=0;c<SIZE;c++)if(!grid[r][c])grid[r][c]=ALPHA[Math.floor(Math.random()*ALPHA.length)];
  let selecting=false,selStart=null,selCells=[],foundWords=[],foundCells=[];
  let score=0;
  const inner=document.getElementById('game-inner');
  function render(){
    inner.innerHTML=`<div class="wg-wrap">
      <div class="wg-grid" style="grid-template-columns:repeat(${SIZE},1fr)" id="wg">
      ${grid.map((row,r)=>row.map((c,col)=>{
        const idx2=r*SIZE+col;const isSel=selCells.some(([a,b])=>a===r&&b===col);
        const isFound=foundCells.some(([a,b])=>a===r&&b===col);
        return `<div class="wg-cell${isSel?' selecting':''}${isFound?' found':''}" data-r="${r}" data-c="${col}" onpointerdown="wgDown(event,${r},${col})" onpointermove="wgMove(event,${r},${col})" onpointerup="wgUp()">${c}</div>`;
      }).join('')).join('')}
      </div>
    </div>
    <div class="wg-words">${words.map(w=>`<span class="wg-word${foundWords.includes(w)?' found':''}">${w}</span>`).join('')}</div>`;
    window.wgDown=function(e,r,c){e.preventDefault();selecting=true;selStart=[r,c];selCells=[[r,c]];render();};
    window.wgMove=function(e,r,c){
      if(!selecting)return;e.preventDefault();
      if(!selStart)return;
      const dr=r-selStart[0],dc=c-selStart[1];
      const len=Math.max(Math.abs(dr),Math.abs(dc));
      if(len===0){selCells=[[r,c]];render();return;}
      const sr=Math.sign(dr),sc=Math.sign(dc);
      if(dr!==0&&dc!==0&&Math.abs(dr)!==Math.abs(dc)){return;}
      selCells=[];for(let i=0;i<=len;i++)selCells.push([selStart[0]+sr*i,selStart[1]+sc*i]);
      render();
    };
    window.wgUp=function(){
      if(!selecting)return;selecting=false;
      const word=selCells.map(([r,c])=>grid[r][c]).join('');
      const rword=word.split('').reverse().join('');
      const match=placed.find(p=>p.word===word||p.word===rword);
      if(match&&!foundWords.includes(match.word)){
        foundWords.push(match.word);foundCells.push(...match.cells);
        score+=20;updateGameScore(score);sndOK();
        if(foundWords.length===words.length)_gTimeout(()=>endGame(score),600);
      }else{sndKO();}
      selCells=[];render();
    };
  }
  render();
  document.getElementById('game-timer-disp').style.display='none';
}

// ════════════════════════════════════════════
// GAME 8 — SNAKE QCM
// ════════════════════════════════════════════
function buildSnake(){
  const W=22,H=20,CELL=16;
  const CW=W*CELL,CH=H*CELL;
  const inner=document.getElementById('game-inner');
  inner.innerHTML=`
    <div id="sn-wrap" class="g-board" style="width:${CW}px">
      <canvas id="snake-canvas" width="${CW}" height="${CH}" style="display:block;width:100%;height:auto"></canvas>
    </div>
    <p class="g-help">Touche le haut, le bas, la gauche ou la droite du terrain pour tourner (ou glisse le doigt).</p>
    <div class="snake-q" id="snake-q" style="display:none"></div>`;
  const canvas=document.getElementById('snake-canvas');const ctx=canvas.getContext('2d');
  let snake=[{x:5,y:10},{x:4,y:10},{x:3,y:10}],dir={x:1,y:0},nextDir={x:1,y:0};
  let food={x:16,y:10},score=0,loop,paused=false;
  let curQ=null,foodIsQ=false;
  const QUESTIONS=[...QUIZ_DATA].sort(()=>Math.random()-.5);let qIdx=0;
  function getQ(){return QUESTIONS[qIdx%QUESTIONS.length];}
  function placeFood(){do{food={x:Math.floor(Math.random()*(W-2))+1,y:Math.floor(Math.random()*(H-2))+1};}while(snake.some(s=>s.x===food.x&&s.y===food.y));foodIsQ=Math.random()>.4;}
  function draw(){
    const night=document.body.classList.contains('night');
    if(night){
      ctx.fillStyle='#0d1117';ctx.fillRect(0,0,CW,CH);
      ctx.strokeStyle='rgba(255,255,255,0.05)';ctx.lineWidth=1;
      for(let x=0;x<=W;x++){ctx.beginPath();ctx.moveTo(x*CELL,0);ctx.lineTo(x*CELL,CH);ctx.stroke();}
      for(let y=0;y<=H;y++){ctx.beginPath();ctx.moveTo(0,y*CELL);ctx.lineTo(CW,y*CELL);ctx.stroke();}
    }else{
      // Herbe en damier + bordure de sable
      for(let y=0;y<H;y++)for(let x=0;x<W;x++){
        const edge=x===0||y===0||x===W-1||y===H-1;
        ctx.fillStyle=edge?((x+y)%2?'#F2D49B':'#EBC985'):((x+y)%2?'#8FD16A':'#83C85E');
        ctx.fillRect(x*CELL,y*CELL,CELL,CELL);
      }
      ctx.fillStyle='rgba(255,255,255,.18)';
      for(let i=0;i<14;i++){const gx=((i*97)%(W-2)+1)*CELL+4,gy=((i*53)%(H-2)+1)*CELL+5;ctx.fillRect(gx,gy,2,5);ctx.fillRect(gx+4,gy+1,2,4);}
    }
    // Serpent
    snake.forEach((s,i)=>{
      const gx=s.x*CELL+1,gy=s.y*CELL+1,r=CELL-2;
      ctx.fillStyle=i===0?'#5A52D5':(i%2?'#7B73FF':'#6C63FF');
      ctx.beginPath();ctx.roundRect(gx,gy,r,r,i===0?7:5);ctx.fill();
      if(i===0){
        const ex=dir.x,ey=dir.y,cx=gx+r/2,cy=gy+r/2;
        [[-1],[1]].forEach(([k])=>{const px=cx+ex*3+(ey?k*3:0),py=cy+ey*3+(ex?k*3:0);
          ctx.fillStyle='#fff';ctx.beginPath();ctx.arc(px,py,2.6,0,7);ctx.fill();
          ctx.fillStyle='#1b1b2f';ctx.beginPath();ctx.arc(px+ex,py+ey,1.3,0,7);ctx.fill();});
      }
    });
    // Nourriture
    const fx=food.x*CELL+CELL/2,fy=food.y*CELL+CELL/2;
    ctx.fillStyle=foodIsQ?'rgba(255,209,102,.45)':'rgba(255,255,255,.35)';
    ctx.beginPath();ctx.arc(fx,fy,CELL*0.62,0,7);ctx.fill();
    ctx.font=`${CELL-1}px sans-serif`;ctx.textAlign='center';ctx.textBaseline='middle';
    ctx.fillText(foodIsQ?'❓':'🍎',fx,fy+1);
  }
  function step(){
    if(paused)return;
    dir={...nextDir};const head={x:snake[0].x+dir.x,y:snake[0].y+dir.y};
    if(head.x<0||head.x>=W||head.y<0||head.y>=H||snake.some(s=>s.x===head.x&&s.y===head.y)){clearInterval(loop);endGame(score);return;}
    snake.unshift(head);
    if(head.x===food.x&&head.y===food.y){
      if(foodIsQ){paused=true;showSnakeQ();}
      else{score+=5;updateGameScore(score);placeFood();}
    } else {snake.pop();}
    draw();
  }
  function showSnakeQ(){
    curQ=getQ();qIdx++;
    const qDiv=document.getElementById('snake-q');qDiv.style.display='block';
    qDiv.innerHTML=`<p>${curQ.q}</p><div class="snake-choices">${curQ.c.map(c=>`<button class="snake-choice" onclick="snAns('${c}')">${c}</button>`).join('')}</div>`;
    window.snAns=function(v){
      if(v===curQ.a){sndOK();score+=15;updateGameScore(score);placeFood();}else{sndKO();if(snake.length>1)snake.pop();placeFood();}
      qDiv.style.display='none';paused=false;
    };
  }
  window.snDir=function(x,y){if(dir.x===-x&&dir.y===-y)return;nextDir={x,y};};
  const D={u:[0,-1],d:[0,1],l:[-1,0],r:[1,0]};
  _gPad(document.getElementById('sn-wrap'),{center:false,swipe:true,on:z=>{if(D[z])snDir(...D[z]);}});
  window._gKeyFn=e=>{const m={ArrowUp:'u',ArrowDown:'d',ArrowLeft:'l',ArrowRight:'r'}[e.key];if(!m)return false;snDir(...D[m]);};
  placeFood();draw();loop=_gInterval(step,190);
  document.getElementById('game-timer-disp').style.display='none';
}

// ════════════════════════════════════════════
// GAME 13 — BLOCS SENSEI (blocs qui tombent ; pas « Tetris », marque déposée)
// Centre = tourner · gauche/droite = déplacer · bas = descendre vite · haut = chute directe
// Toutes les 4 lignes : une petite question bonus.
// ════════════════════════════════════════════
function buildBlocs(){
  const COLS=10,ROWS=18;
  const inner=document.getElementById('game-inner');
  const availW=Math.max(200,Math.min((inner.clientWidth||340)-8,420));
  const availH=Math.max(260,window.innerHeight-300);
  const CELL=Math.max(14,Math.floor(Math.min(availW/COLS,availH/ROWS)));
  const BW=COLS*CELL,BH=ROWS*CELL;
  inner.innerHTML=`
    <div class="blocs-hud">
      <div><b id="bl-lines">0</b><span>lignes</span></div>
      <div><b id="bl-level">1</b><span>niveau</span></div>
      <div class="blocs-next"><canvas id="bl-next" width="64" height="44"></canvas><span>suivant</span></div>
    </div>
    <div id="bl-wrap" class="g-board" style="width:${BW}px"><canvas id="bl-canvas" width="${BW}" height="${BH}" style="display:block;width:100%;height:auto"></canvas></div>
    <p class="g-help">Rond du milieu : tourner · côtés : déplacer · bas : descendre · haut : tout en bas</p>
    <div class="snake-q" id="bl-q" style="display:none"></div>`;
  const cv=document.getElementById('bl-canvas'),ctx=cv.getContext('2d');
  const nx=document.getElementById('bl-next').getContext('2d');
  const SH={I:[[0,0],[1,0],[2,0],[3,0]],O:[[0,0],[1,0],[0,1],[1,1]],T:[[0,0],[1,0],[2,0],[1,1]],
    S:[[1,0],[2,0],[0,1],[1,1]],Z:[[0,0],[1,0],[1,1],[2,1]],J:[[0,0],[0,1],[1,1],[2,1]],L:[[2,0],[0,1],[1,1],[2,1]]};
  const COL={I:'#3ABEF9',O:'#FFD166',T:'#9B5DE5',S:'#06D6A0',Z:'#FF5C8A',J:'#3A86FF',L:'#FF9F1C'};
  const grid=Array.from({length:ROWS},()=>Array(COLS).fill(null));
  const age=(P()&&P().age)||8;
  let score=0,lines=0,level=1,paused=false,over=false,bag=[];
  function rnd(){if(!bag.length)bag=Object.keys(SH).sort(()=>Math.random()-.5);return bag.pop();}
  function mk(t){return{t,c:SH[t].map(p=>[...p]),x:3,y:0};}
  let cur=mk(rnd()),nxt=mk(rnd());
  function fits(c,dx,dy){return c.every(([x,y])=>{const X=x+dx,Y=y+dy;return X>=0&&X<COLS&&Y<ROWS&&(Y<0||!grid[Y][X]);});}
  function rotate(){
    if(cur.t==='O')return;
    const cx=cur.c[1][0],cy=cur.c[1][1];
    const r=cur.c.map(([x,y])=>[cx-(y-cy),cy+(x-cx)]);
    for(const k of [0,-1,1,-2,2]){if(fits(r,cur.x+k,cur.y)){cur.c=r;cur.x+=k;sndTapSafe();return;}}
  }
  function sndTapSafe(){try{if(typeof sndTap==='function')sndTap();}catch(e){}}
  function move(dx){if(fits(cur.c,cur.x+dx,cur.y))cur.x+=dx;}
  function down(){if(fits(cur.c,cur.x,cur.y+1)){cur.y++;return true;}lock();return false;}
  function drop(){let n=0;while(fits(cur.c,cur.x,cur.y+1)){cur.y++;n++;}score+=Math.floor(n/2);lock();}
  function lock(){
    cur.c.forEach(([x,y])=>{const Y=y+cur.y;if(Y>=0)grid[Y][x+cur.x]=COL[cur.t];});
    let cleared=0;
    for(let y=ROWS-1;y>=0;y--){if(grid[y].every(Boolean)){grid.splice(y,1);grid.unshift(Array(COLS).fill(null));cleared++;y++;}}
    if(cleared){
      score+=[0,10,30,60,100][cleared]*level;const before=lines;lines+=cleared;
      level=1+Math.floor(lines/8);sndOK();
      document.getElementById('bl-lines').textContent=lines;document.getElementById('bl-level').textContent=level;
      restart();
      if(Math.floor(lines/4)>Math.floor(before/4))askQ();
    }
    updateGameScore(score);
    cur=nxt;cur.x=3;cur.y=0;nxt=mk(rnd());drawNext();
    if(!fits(cur.c,cur.x,cur.y)){over=true;clearInterval(loop);draw();_gTimeout(()=>endGame(score),600);}
  }
  const QS=[...QUIZ_DATA].sort(()=>Math.random()-.5);let qi=0;
  function askQ(){
    paused=true;const q=QS[qi++%QS.length];const d=document.getElementById('bl-q');d.style.display='block';
    d.innerHTML=`<p>⭐ Question bonus : ${q.q}</p><div class="snake-choices">${q.c.map(c=>`<button class="snake-choice" onclick="blAns(this,'${String(c).replace(/'/g,"\\'")}')">${c}</button>`).join('')}</div>`;
    window.blAns=function(btn,v){if(v===q.a){sndOK();score+=20;updateGameScore(score);}else sndKO();d.style.display='none';paused=false;};
  }
  function cell(c,x,y,col,a){
    const g=c===ctx?CELL:11;const px=x*g,py=y*g;
    c.globalAlpha=a||1;c.fillStyle=col;c.fillRect(px+1,py+1,g-2,g-2);
    c.fillStyle='rgba(255,255,255,.35)';c.fillRect(px+1,py+1,g-2,Math.max(2,g*.18));c.fillRect(px+1,py+1,Math.max(2,g*.18),g-2);
    c.fillStyle='rgba(0,0,0,.18)';c.fillRect(px+1,py+g-1-Math.max(2,g*.16),g-2,Math.max(2,g*.16));
    c.globalAlpha=1;
  }
  function draw(){
    const night=document.body.classList.contains('night');
    ctx.fillStyle=night?'#0d1117':'#F1EFFF';ctx.fillRect(0,0,BW,BH);
    ctx.strokeStyle=night?'rgba(255,255,255,.05)':'rgba(108,99,255,.10)';ctx.lineWidth=1;
    for(let x=1;x<COLS;x++){ctx.beginPath();ctx.moveTo(x*CELL+.5,0);ctx.lineTo(x*CELL+.5,BH);ctx.stroke();}
    for(let y=1;y<ROWS;y++){ctx.beginPath();ctx.moveTo(0,y*CELL+.5);ctx.lineTo(BW,y*CELL+.5);ctx.stroke();}
    grid.forEach((row,y)=>row.forEach((c,x)=>{if(c)cell(ctx,x,y,c);}));
    if(!over){
      let gy=cur.y;while(fits(cur.c,cur.x,gy+1))gy++;
      cur.c.forEach(([x,y])=>{if(y+gy>=0)cell(ctx,x+cur.x,y+gy,COL[cur.t],.22);});
      cur.c.forEach(([x,y])=>{if(y+cur.y>=0)cell(ctx,x+cur.x,y+cur.y,COL[cur.t]);});
    }
  }
  function drawNext(){nx.clearRect(0,0,64,44);const xs=nxt.c.map(p=>p[0]),ys=nxt.c.map(p=>p[1]);
    const ox=(64/11-(Math.max(...xs)+1))/2,oy=(44/11-(Math.max(...ys)+1))/2;
    nxt.c.forEach(([x,y])=>cell(nx,x+ox,y+oy,COL[nxt.t]));}
  function tick(){if(paused||over)return;down();draw();}
  let loop;
  function speed(){const base=age<7?950:age<11?800:650;return Math.max(140,base-(level-1)*70);}
  function restart(){if(loop)clearInterval(loop);loop=_gInterval(tick,speed());}
  function act(z){if(paused||over)return;
    if(z==='m')rotate();else if(z==='l')move(-1);else if(z==='r')move(1);else if(z==='d')down();else if(z==='u')drop();
    draw();}
  _gPad(document.getElementById('bl-wrap'),{center:true,repeat:['l','r','d'],on:act});
  window._gKeyFn=e=>{const m={ArrowLeft:'l',ArrowRight:'r',ArrowDown:'d',ArrowUp:'m',' ':'u'}[e.key];if(!m)return false;act(m);};
  drawNext();draw();restart();
  document.getElementById('game-timer-disp').style.display='none';
}

// ════════════════════════════════════════════
// GAME 9 — MAGIC SORT
// ════════════════════════════════════════════
const SORT_DATA=[
  {title:'Trie par taille croissante',buckets:['Petit','Moyen','Grand'],
   items:[{t:'Fourmi',b:'Petit'},{t:'Chien',b:'Moyen'},{t:'Éléphant',b:'Grand'},{t:'Souris',b:'Petit'},{t:'Cheval',b:'Grand'},{t:'Chat',b:'Moyen'},{t:'Coccinelle',b:'Petit'},{t:'Vache',b:'Grand'}]},
  {title:'Trie par catégorie',buckets:['Fruit','Légume','Céréale'],
   items:[{t:'Pomme',b:'Fruit'},{t:'Carotte',b:'Légume'},{t:'Blé',b:'Céréale'},{t:'Poire',b:'Fruit'},{t:'Patate',b:'Légume'},{t:'Riz',b:'Céréale'},{t:'Raisin',b:'Fruit'},{t:'Maïs',b:'Céréale'}]},
  {title:'Trie chaud / froid',buckets:['Chaud','Froid'],
   items:[{t:'Soleil',b:'Chaud'},{t:'Glace',b:'Froid'},{t:'Feu',b:'Chaud'},{t:'Neige',b:'Froid'},{t:'Lave',b:'Chaud'},{t:'Banquise',b:'Froid'},{t:'Sauna',b:'Chaud'},{t:'Congélateur',b:'Froid'}]},
];
// ════════════════════════════════════════════
// MAGIC SORT — Water Sort Bottle Game
// Trie les liquides colorés pour remplir
// chaque bouteille d'une seule couleur !
// ════════════════════════════════════════════
const WS_COLORS=[
  {id:0,hex:'#FF6B6B',name:'Rouge'},
  {id:1,hex:'#FF9F1C',name:'Orange'},
  {id:2,hex:'#FFD166',name:'Jaune'},
  {id:3,hex:'#06D6A0',name:'Vert'},
  {id:4,hex:'#6C63FF',name:'Violet'},
  {id:5,hex:'#4FC3F7',name:'Bleu'},
  {id:6,hex:'#F48FB1',name:'Rose'},
  {id:7,hex:'#A5D6A7',name:'Menthe'},
];
const WS_TUBE_SIZE=4; // layers per bottle
function buildSort(){
  const inner=document.getElementById('game-inner');
  document.getElementById('game-timer-disp').style.display='none';

  const age=P()?P().age:8;
  const numColors=age<7?4:age<10?5:age<13?6:7;
  const numEmpty=2; // toujours 2 tubes vides pour manœuvrer

  function makeBottles(){
    let pool=[];
    for(let c=0;c<numColors;c++)
      for(let l=0;l<WS_TUBE_SIZE;l++) pool.push(c);
    for(let i=pool.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[pool[i],pool[j]]=[pool[j],pool[i]];}
    let b=[];
    for(let k=0;k<numColors;k++) b.push(pool.slice(k*WS_TUBE_SIZE,(k+1)*WS_TUBE_SIZE));
    for(let e=0;e<numEmpty;e++) b.push([]);
    // Reroll if any bottle is already complete (too easy start)
    if(b.some(bt=>bt.length===WS_TUBE_SIZE&&bt.every(c=>c===bt[0]))) return makeBottles();
    return b;
  }
  let bottles=makeBottles();
  let selected=null,moves=0,score=0;

  function topColor(b){const bt=bottles[b];return bt.length?bt[bt.length-1]:null;}
  function canPour(from,to){
    if(from===to||!bottles[from].length)return false;
    if(bottles[to].length>=WS_TUBE_SIZE)return false;
    if(!bottles[to].length)return true;
    return topColor(from)===topColor(to);
  }
  function isDone(bt){return bt.length===WS_TUBE_SIZE&&bt.every(c=>c===bt[0]);}
  function checkWin(){return bottles.every(bt=>bt.length===0||isDone(bt));}
  // Vérifie si le puzzle est bloqué (aucun mouvement possible)
  function isStuck(){
    for(let f=0;f<bottles.length;f++){
      for(let t=0;t<bottles.length;t++){
        if(canPour(f,t))return false;
      }
    }
    return true;
  }

  function render(){
    const tubeH=140;
    const layerH=Math.floor(tubeH/WS_TUBE_SIZE);
    const totalBottles=bottles.length;
    // Disposition : 2 rangées si beaucoup de bouteilles
    const perRow=totalBottles<=6?totalBottles:Math.ceil(totalBottles/2);
    const stuck=isStuck()&&!checkWin();

    let html=`<div class="ws-wrap">
      <div class="ws-info" style="margin-bottom:6px">
        💧 Remplis chaque tube d'une seule couleur !
        ${stuck?'<br><b style="color:var(--c)">⚠️ Bloqué — mélange relancé !</b>':''}
        <br><b>Coups : ${moves}</b>
        <button onclick="wsReset()" style="margin-left:8px;font-size:11px;padding:3px 10px;border-radius:20px;border:1.5px solid var(--v);background:var(--vl);color:var(--v);cursor:pointer;font-weight:700">🔄 Relancer</button>
      </div>
      <div class="ws-bottles" style="flex-wrap:wrap;gap:8px;justify-content:center;max-width:100%">`;

    bottles.forEach((bt,bi)=>{
      const isSel=(selected===bi);
      const done=isDone(bt);
      const doneColor=done?WS_COLORS[bt[0]%WS_COLORS.length].hex:'transparent';
      html+=`<div class="ws-bottle${isSel?' selected':''}${done?' done':''}" onclick="wsTap(${bi})" style="width:42px">
        <div class="ws-cap" style="${done?'background:'+doneColor+';opacity:.7':''}"></div>
        <div class="ws-tube" style="height:${tubeH}px;${done?'box-shadow:0 0 16px 4px '+doneColor+'88;border-color:'+doneColor:''}">`;
      const emptyLayers=WS_TUBE_SIZE-bt.length;
      for(let e=0;e<emptyLayers;e++){
        html+=`<div style="flex:0 0 ${layerH}px;background:rgba(200,200,255,0.06)"></div>`;
      }
      const layers=[...bt].reverse();
      layers.forEach((c,li)=>{
        const col=WS_COLORS[c%WS_COLORS.length];
        const isTop=(li===0);
        html+=`<div style="flex:0 0 ${layerH}px;background:${col.hex};
          ${isTop?'border-radius:0':''}
          ${li===layers.length-1?'border-radius:0 0 19px 19px':''}
          box-shadow:inset 0 ${isTop?2:-1}px 0 rgba(255,255,255,${isTop?.35:.1});
          position:relative">
          ${isTop?`<div style="position:absolute;top:2px;left:50%;transform:translateX(-50%);
            width:60%;height:3px;background:rgba(255,255,255,.4);border-radius:2px"></div>`:''}
        </div>`;
      });
      html+=`</div>`;
      html+=`<div class="ws-bottle-label">${done?'✅':''}</div>`;
      html+=`</div>`;
    });

    html+=`</div></div>`;
    inner.innerHTML=html;

    window.wsReset=function(){bottles=makeBottles();selected=null;moves=0;score=0;render();};
    window.wsTap=function(bi){
      if(checkWin())return;
      if(selected===null){
        if(!bottles[bi].length){toast('🫙 Tube vide — choisis un autre !');return;}
        if(isDone(bottles[bi])){toast('✅ Déjà complet !');return;}
        selected=bi;render();
      } else if(selected===bi){
        selected=null;render();
      } else {
        if(canPour(selected,bi)){
          const tc=topColor(selected);
          let poured=0;
          while(bottles[selected].length&&topColor(selected)===tc&&bottles[bi].length<WS_TUBE_SIZE){
            bottles[bi].push(bottles[selected].pop());poured++;
          }
          moves++;score+=poured*5;updateGameScore(score);sndOK();
          selected=null;
          _gTimeout(()=>{
            render();
            if(checkWin()){
              const fs=Math.max(50,300-moves*5);updateGameScore(fs);
              _gTimeout(()=>endGame(fs),700);
            } else if(isStuck()){
              // Relance auto si bloqué
              _gTimeout(()=>{bottles=makeBottles();selected=null;render();toast('🔄 Puzzle relancé — tu étais bloqué !');},1200);
            }
          },90);
        } else {
          sndKO();selected=null;render();
          toast('❌ Couleurs incompatibles ou tube plein');
        }
      }
    };
  }
  render();
}

// ════════════════════════════════════════════
// GAME 10 — PUZZLE COULISSANT (TAQUIN)
// ════════════════════════════════════════════
function buildTaquin(){
  const N=4;const total=N*N;
  let board=Array.from({length:total-1},(_, i)=>i+1);board.push(0);
  // Shuffle
  for(let i=0;i<200;i++){
    const z=board.indexOf(0);const moves=[];
    if(z-N>=0)moves.push(z-N);if(z+N<total)moves.push(z+N);
    if(z%N>0)moves.push(z-1);if(z%N<N-1)moves.push(z+1);
    const pick=moves[Math.floor(Math.random()*moves.length)];
    [board[z],board[pick]]=[board[pick],board[z]];
  }
  let moves=0;let score=0;
  const inner=document.getElementById('game-inner');
  function isWin(){return board.every((v,i)=>v===(i<total-1?i+1:0));}
  const TAQUIN_COLORS=['linear-gradient(135deg,#FF6B6B,#FF9F9F)','linear-gradient(135deg,#FF9F1C,#FFD166)','linear-gradient(135deg,#06D6A0,#4FC3F7)','linear-gradient(135deg,#6C63FF,#9B93FF)','linear-gradient(135deg,#F48FB1,#FF6B6B)','linear-gradient(135deg,#4FC3F7,#06D6A0)','linear-gradient(135deg,#FFD166,#FF9F1C)','linear-gradient(135deg,#9B93FF,#6C63FF)','linear-gradient(135deg,#06D6A0,#A5D6A7)'];
  function render(){
    inner.innerHTML=`<div class="taquin-wrap">
      <p style="font-size:12px;color:var(--tl);font-weight:700">Coups : ${moves} · Remets dans l'ordre !</p>
      <div class="taquin-grid" style="grid-template-columns:repeat(${N},1fr)">${board.map((v,i)=>`<div class="taquin-cell${v===0?' empty':''}" onclick="taqMove(${i})" style="${v?'background:'+TAQUIN_COLORS[(v-1)%TAQUIN_COLORS.length]:''}">${v||''}</div>`).join('')}</div>
    </div>`;
    window.taqMove=function(i){
      const z=board.indexOf(0);
      const canMove=(i===z-1&&z%N>0)||(i===z+1&&z%N<N-1)||(i===z-N)||(i===z+N);
      if(!canMove)return;
      [board[z],board[i]]=[board[i],board[z]];moves++;sndTap();render();
      if(isWin()){score=Math.max(0,200-moves*3);updateGameScore(score);_gTimeout(()=>endGame(score),400);}
    };
  }
  render();
  document.getElementById('game-timer-disp').style.display='none';
}

// ════════════════════════════════════════════
// GAME 11 — TOUR DE HANOÏ
// ════════════════════════════════════════════
function buildHanoi(){
  const age=P()?P().age:8;
  const disks=age<7?3:age<10?4:age<13?5:6;
  let pegs=[Array.from({length:disks},(_, i)=>disks-i),[],[]];
  let selected=null;let moves=0;
  // Emojis de couleurs pour chaque disque (du plus grand au plus petit)
  const DISK_COLORS=['#FF6B6B','#FF9F1C','#FFD166','#06D6A0','#6C63FF','#9B6BFF'];
  const DISK_LABELS=['🟥','🟧','🟨','🟩','🟦','🟪'];
  const inner=document.getElementById('game-inner');
  function minMoves(){return Math.pow(2,disks)-1;}
  function isWin(){return pegs[2].length===disks;}
  const PEG_NAMES=['Tour A','Tour B','Tour C'];
  function render(){
    const maxH=disks;
    let html=`
    <div style="background:var(--vl);border-radius:10px;padding:8px 12px;margin-bottom:8px;font-size:12px;color:var(--t);line-height:1.5">
      <b>🗼 But :</b> Déplace tous les disques de la <b>Tour A</b> vers la <b>Tour C</b>.<br>
      Règle : un grand disque ne peut jamais se poser sur un plus petit.<br>
      <b>Minimum : ${minMoves()} coups</b> · Coups effectués : <b>${moves}</b>
    </div>
    ${selected!==null?`<div style="text-align:center;font-size:13px;color:var(--v);font-weight:700;margin-bottom:6px">✋ Disque ${DISK_LABELS[pegs[selected][pegs[selected].length-1]-1]} sélectionné — choisis une tour destination</div>`:'<div style="text-align:center;font-size:12px;color:var(--tl);font-weight:600;margin-bottom:6px">Appuie sur une tour pour prendre le disque du dessus</div>'}
    <div style="display:flex;gap:8px;justify-content:center;align-items:flex-end;min-height:${maxH*36+60}px;padding:0 4px">`;
    pegs.forEach((peg,pi)=>{
      const isSel=selected===pi;
      html+=`<div onclick="hanoiSel(${pi})" style="flex:1;display:flex;flex-direction:column;align-items:center;cursor:pointer;
        border-radius:14px;padding:8px 4px;transition:background .15s;
        background:${isSel?'rgba(108,99,255,0.15)':'transparent'};border:2px solid ${isSel?'var(--v)':'transparent'}">
        <div style="font-size:11px;font-weight:800;color:${isSel?'var(--v)':'var(--tl)'};margin-bottom:4px">${PEG_NAMES[pi]}</div>
        <div style="flex:1;display:flex;flex-direction:column;justify-content:flex-end;align-items:center;gap:3px;min-height:${maxH*34}px">`;
      // Espaces vides
      for(let s=0;s<maxH-peg.length;s++){
        html+=`<div style="height:28px;display:flex;align-items:center;justify-content:center">
          <div style="width:4px;background:rgba(0,0,0,0.15);border-radius:2px;height:100%"></div></div>`;
      }
      // Disques (du bas vers le haut = grand au petit)
      [...peg].reverse().forEach(d=>{
        const w=Math.round(28+d*(44/disks));
        html+=`<div style="width:${w}px;height:28px;background:${DISK_COLORS[(d-1)%6]};border-radius:8px;
          display:flex;align-items:center;justify-content:center;font-size:16px;
          box-shadow:0 2px 6px rgba(0,0,0,0.2);font-weight:700;color:#fff">${DISK_LABELS[(d-1)%6]}</div>`;
      });
      html+=`</div>
        <div style="width:80%;height:6px;background:var(--tl);border-radius:3px;margin-top:4px"></div>
      </div>`;
    });
    html+=`</div>`;
    inner.innerHTML=html;
    window.hanoiSel=function(pi){
      if(selected===null){
        if(pegs[pi].length===0){toast('⚠️ Tour vide !');return;}
        selected=pi;render();
      } else if(selected===pi){
        selected=null;render();
      } else {
        const top=pegs[selected][pegs[selected].length-1];
        const dest=pegs[pi].length?pegs[pi][pegs[pi].length-1]:Infinity;
        if(top<dest){pegs[pi].push(pegs[selected].pop());moves++;sndOK();}
        else{toast('❌ Impossible — disque trop grand !');sndKO();}
        selected=null;render();
        if(isWin()){const sc=Math.max(0,400-moves*8);updateGameScore(sc);_gTimeout(()=>endGame(sc),400);}
      }
    };
  }
  render();
  document.getElementById('game-timer-disp').style.display='none';
}

// ════════════════════════════════════════════
// GAME 12 — BOMBE DE MOTS (remplace 2048)
// Trouve l'anagramme avant que la bombe explose !
// ════════════════════════════════════════════
const BOMB_WORDS=[
  'CHAT','CHIEN','MAISON','ARBRE','SOLEIL','LUNE','FLEUR','NUAGE','RIVIERE','MONTAGNE',
  'LAPIN','TIGER','ÉCOLE','LIVRE','CRAYON','JARDIN','OISEAU','CHEMIN','ÉTOILE','FORÊT',
  'ENFANT','BATEAU','VOITURE','MUSIQUE','TABLEAU','BALLON','ORANGE','BOUGIE','CERISE','CLOCHE',
];
function build2048(){
  const inner=document.getElementById('game-inner');
  let score=0,round=0,timer=null,timeLeft=0;
  const totalRounds=8;
  function shuffle(s){return s.split('').sort(()=>Math.random()-.5).join('');}
  function nextRound(){
    if(round>=totalRounds){clearInterval(timer);_gTimeout(()=>endGame(score),300);return;}
    round++;
    const word=BOMB_WORDS[Math.floor(Math.random()*BOMB_WORDS.length)];
    let scrambled=shuffle(word);
    while(scrambled===word&&word.length>2)scrambled=shuffle(word);
    timeLeft=45;
    clearInterval(timer);
    function renderRound(){
      const pct=timeLeft/45*100;
      const col=pct>60?'#06D6A0':pct>30?'#FFD166':'#FF6B6B';
      inner.innerHTML=`
        <div style="text-align:center;font-size:12px;font-weight:700;color:var(--tl);margin-bottom:4px">Manche ${round}/${totalRounds} · Score : ${score}</div>
        <div style="background:#1A1A2E;border-radius:16px;padding:20px 16px;text-align:center;margin-bottom:10px">
          <div style="font-size:11px;color:#aaa;margin-bottom:6px">Remets les lettres dans le bon ordre !</div>
          <div style="font-size:36px;font-weight:900;color:#FFD166;letter-spacing:8px;margin-bottom:12px">${scrambled}</div>
          <div style="background:#0f1923;border-radius:8px;height:10px;overflow:hidden;margin-bottom:8px">
            <div style="height:100%;width:${pct}%;background:${col};transition:width 1s linear;border-radius:8px"></div>
          </div>
          <div style="font-size:20px">💣 <span id="bomb-time" style="font-weight:900;color:${col}">${timeLeft}s</span></div>
        </div>
        <input id="bomb-inp" class="inp" placeholder="Tape le mot..." style="text-align:center;font-size:18px;font-weight:800;letter-spacing:4px" maxlength="${word.length}" autocomplete="off" autocorrect="off" autocapitalize="characters" spellcheck="false">
        <button class="adv-continue-btn" style="width:100%;margin-top:8px;font-size:16px" onclick="bombCheck()">✅ Valider</button>
        <div id="bomb-msg" style="text-align:center;font-size:13px;font-weight:700;margin-top:8px;min-height:20px"></div>`;
      const inp=document.getElementById('bomb-inp');
      if(inp){inp.focus();inp.addEventListener('keydown',e=>{if(e.key==='Enter')window.bombCheck();});}
      window.bombCheck=function(){
        const val=(document.getElementById('bomb-inp').value||'').toUpperCase().trim();
        if(val===word){
          clearInterval(timer);
          const bonus=Math.round(timeLeft*5);score+=10+bonus;updateGameScore(score);
          document.getElementById('bomb-msg').innerHTML=`<span style="color:var(--m)">✅ Bravo ! +${10+bonus} pts (bonus temps : +${bonus})</span>`;
          _gTimeout(nextRound,900);
        } else {
          document.getElementById('bomb-msg').innerHTML=`<span style="color:var(--c)">❌ Pas tout à fait…</span>`;
        }
      };
    }
    renderRound();
    timer=_gInterval(()=>{
      timeLeft--;
      const tEl=document.getElementById('bomb-time');
      if(tEl)tEl.textContent=timeLeft+'s';
      // Mise à jour barre
      const pct2=timeLeft/(Math.max(5,15-Math.floor(round/2)))*100;
      const col2=pct2>60?'#06D6A0':pct2>30?'#FFD166':'#FF6B6B';
      const bar=inner.querySelector('[style*="transition:width"]');
      if(bar){bar.style.width=pct2+'%';bar.style.background=col2;}
      if(tEl)tEl.style.color=col2;
      if(timeLeft<=0){
        clearInterval(timer);
        inner.querySelector('#bomb-msg').innerHTML=`<span style="color:var(--c)">💥 Boom ! C'était : <b>${word}</b></span>`;
        _gTimeout(nextRound,1500);
      }
    },1000);
  }
  nextRound();
  document.getElementById('game-timer-disp').style.display='none';
}

