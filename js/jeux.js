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
function isDailyFull(gameId){return getDailyMs(gameId)>=JEUX_DAILY_MAX;}

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
    const dailyMs=getDailyMs(g.id);
    const pct=Math.min(100,Math.round(dailyMs/JEUX_DAILY_MAX*100));
    const card=document.createElement('button');
    card.className='jeu-card'+(locked?' locked':'');
    card.innerHTML=`<span class="je">${g.emoji}</span>
      <span class="jt">${g.title}</span>
      <span class="js">${g.desc}</span>
      ${hs>0?`<span class="jhs">🏆 Record : ${hs}</span>`:''}
      ${locked?`<span class="jeu-lock-badge">🔒 ${g.min_score}⭐</span>`:''}
      <div class="jeu-daily-bar-wrap"><div class="jeu-daily-bar" style="width:${pct}%"></div></div>`;
    if(!locked){
      if(isDailyFull(g.id)){
        card.disabled=true;
        card.querySelector('.js').textContent='Limite atteinte (réinitialise à minuit)';
      } else {
        card.onclick=()=>{sndTap();startGame(g.id);};
      }
    }
    grid.appendChild(card);
  });
  // Daily banner
  const banner=document.getElementById('jeux-daily-banner');
  const totalLeft=JEUX_CFG.reduce((a,g)=>a+Math.max(0,JEUX_DAILY_MAX-getDailyMs(g.id)),0);
  if(totalLeft<60000){if(banner){banner.style.display='block';banner.textContent='⏰ Limite de jeu atteinte pour aujourd\'hui ! Revenez demain.';}}
  else if(banner)banner.style.display='none';
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
function _gClearAll(){_gTos.forEach(clearTimeout);_gTos=[];_gInts.forEach(clearInterval);_gInts=[];if(typeof GAME==='object'&&GAME){if(GAME.timerInt)clearInterval(GAME.timerInt);if(GAME.sessionInt)clearInterval(GAME.sessionInt);}}
function startGame(id){
  _gClearAll();
  if(isDailyFull(id)){toast('⏰ Limite quotidienne atteinte !');return;}
  GAME={id,score:0,startMs:Date.now(),timerInt:null,sessionInt:null};
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
    taquin:buildTaquin,hanoi:buildHanoi,g2048:build2048}[id];
  if(fn)fn();
}

function updateGameDailyLeft(id){
  const left=Math.max(0,JEUX_DAILY_MAX-getDailyMs(id));
  const mins=Math.floor(left/60000);
  document.getElementById('game-daily-left').textContent=mins>0?`${mins} min restantes aujourd\'hui`:'Dernière partie !';
}

function updateGameScore(s){
  GAME.score=s;
  document.getElementById('game-score').textContent=s;
}

function endGame(finalScore){
  _gClearAll();
  // Record time played
  const elapsed=Date.now()-GAME.startMs;
  addDailyMs(GAME.id,elapsed);
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
    <button class="go-btn" style="background:var(--v);color:#fff" onclick="startGame('${GAME.id}')">🔄 Rejouer</button>
    <button class="go-btn" style="background:var(--bg);color:var(--tl)" onclick="openJeux()">← Jeux</button>
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
  // Terrain plus grand, cellules plus grandes
  const W=22,H=20,CELL=16;
  const CW=W*CELL,CH=H*CELL;
  const inner=document.getElementById('game-inner');
  inner.innerHTML=`
    <div style="position:relative;display:inline-block;border-radius:18px;overflow:hidden;box-shadow:0 8px 32px rgba(0,0,0,.4);margin:0 auto;display:block;width:${CW}px;max-width:100%">
      <canvas id="snake-canvas" width="${CW}" height="${CH}" style="touch-action:none;display:block;width:100%;height:auto"></canvas>
      <!-- 4 tap zones invisible overlaid on canvas -->
      <div id="sn-top"    style="position:absolute;top:0;left:25%;width:50%;height:33%;cursor:pointer;z-index:2" onclick="snDir(0,-1)"></div>
      <div id="sn-bot"    style="position:absolute;bottom:0;left:25%;width:50%;height:33%;cursor:pointer;z-index:2" onclick="snDir(0,1)"></div>
      <div id="sn-left"   style="position:absolute;top:0;left:0;width:25%;height:100%;cursor:pointer;z-index:2" onclick="snDir(-1,0)"></div>
      <div id="sn-right"  style="position:absolute;top:0;right:0;width:25%;height:100%;cursor:pointer;z-index:2" onclick="snDir(1,0)"></div>
    </div>
    <div class="snake-q" id="snake-q" style="display:none"></div>`;
  const canvas=document.getElementById('snake-canvas');const ctx=canvas.getContext('2d');
  let snake=[{x:5,y:10}],dir={x:1,y:0},nextDir={x:1,y:0};
  let food={x:16,y:10},score=0,loop,paused=false;
  let curQ=null,foodIsQ=false;
  const QUESTIONS=[...QUIZ_DATA].sort(()=>Math.random()-.5);let qIdx=0;
  function getQ(){return QUESTIONS[qIdx%QUESTIONS.length];}
  function placeFood(){food={x:Math.floor(Math.random()*(W-2))+1,y:Math.floor(Math.random()*(H-2))+1};foodIsQ=Math.random()>.4;}
  function draw(){
    // Fond sombre avec grille subtile
    ctx.fillStyle='#0d1117';ctx.fillRect(0,0,CW,CH);
    ctx.strokeStyle='rgba(255,255,255,0.04)';ctx.lineWidth=1;
    for(let x=0;x<=W;x++){ctx.beginPath();ctx.moveTo(x*CELL,0);ctx.lineTo(x*CELL,CH);ctx.stroke();}
    for(let y=0;y<=H;y++){ctx.beginPath();ctx.moveTo(0,y*CELL);ctx.lineTo(CW,y*CELL);ctx.stroke();}
    // Indicateurs directionnels (quarts)
    const qs=[
      {x:CW/2,y:CH*0.17,t:'▲'},{x:CW/2,y:CH*0.83,t:'▼'},
      {x:CW*0.125,y:CH/2,t:'◀'},{x:CW*0.875,y:CH/2,t:'▶'}
    ];
    ctx.font='bold 16px sans-serif';ctx.textAlign='center';ctx.textBaseline='middle';
    ctx.fillStyle='rgba(255,255,255,0.12)';
    qs.forEach(q=>ctx.fillText(q.t,q.x,q.y));
    // Snake
    snake.forEach((s,i)=>{
      const r=CELL-2,rad=i===0?6:4;
      const gx=s.x*CELL+1,gy=s.y*CELL+1;
      const g=ctx.createLinearGradient(gx,gy,gx+r,gy+r);
      g.addColorStop(0,i===0?'#8B7CFF':'#6C63FF');
      g.addColorStop(1,i===0?'#6C63FF':'#4A43CC');
      ctx.fillStyle=g;
      ctx.beginPath();ctx.roundRect(gx,gy,r,r,rad);ctx.fill();
      if(i===0){
        ctx.fillStyle='rgba(255,255,255,0.9)';ctx.font='9px sans-serif';
        ctx.textBaseline='middle';ctx.textAlign='center';
        ctx.fillText('👾',gx+r/2,gy+r/2);
      }
    });
    // Nourriture
    const fx=food.x*CELL+2,fy=food.y*CELL+2,fs=CELL-4;
    ctx.fillStyle=foodIsQ?'#FFD166':'#06D6A0';
    ctx.beginPath();ctx.roundRect(fx,fy,fs,fs,5);ctx.fill();
    ctx.fillStyle='#fff';ctx.font=`${CELL-4}px sans-serif`;
    ctx.textAlign='center';ctx.textBaseline='middle';
    ctx.fillText(foodIsQ?'❓':'🍎',fx+fs/2,fy+fs/2);
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
      if(v===curQ.a){sndOK();score+=15;updateGameScore(score);placeFood();}else{sndKO();snake.pop();}
      qDiv.style.display='none';paused=false;
    };
  }
  window.snDir=function(x,y){if(dir.x===-x&&dir.y===-y)return;nextDir={x,y};};
  // Swipe sur le canvas (fallback)
  let _stx,_sty;
  canvas.addEventListener('touchstart',e=>{_stx=e.touches[0].clientX;_sty=e.touches[0].clientY;e.preventDefault();},{passive:false});
  canvas.addEventListener('touchend',e=>{
    const dx=e.changedTouches[0].clientX-_stx,dy=e.changedTouches[0].clientY-_sty;
    if(Math.abs(dx)>Math.abs(dy)&&Math.abs(dx)>20){snDir(dx>0?1:-1,0);}
    else if(Math.abs(dy)>20){snDir(0,dy>0?1:-1);}
    e.preventDefault();
  },{passive:false});
  placeFood();draw();loop=_gInterval(step,190);
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

