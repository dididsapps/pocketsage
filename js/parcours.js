// ═══ 💪 Mes super-pouvoirs — parcours de la semaine (concentration, mémoire, contrôle de soi, émotions, persévérance) ═══
// Données : js/parcours-data.js (window.PARCOURS), générées par tools/parcours_build.py depuis docs/parcours/*.json (vérifiés).
// Chaque jour : 1 jeu de l'appli + 1 activité SANS écran guidée à la voix + 1 moment calme. Progression mémorisée par enfant et par semaine.
(function(){
  const JOURS=['Lundi','Mardi','Mercredi','Jeudi','Vendredi'];
  const COUL={'PC-CONC':'#3B82F6','PC-MEM':'#8B5CF6','PC-CALME':'#EF4444','PC-EMO':'#F59E0B','PC-PERS':'#10B981'};
  const NOM_JEU={memory:'🃏 Memory',calcul:'⚡ Calcul éclair',quiz:'🧩 Quiz rapidité',mastermind:'🎯 Mastermind',anagrammes:'🔤 Anagrammes',motcache:'🔍 Mot caché',sort:'✨ Magic Sort',
    taquin:'🧩 Puzzle coulissant',hanoi:'🗼 Tour de Hanoï',blocs:'🧱 Blocs Sensei',simon:'🎵 Simon Sensei',grille:'🟦 Grille mémoire',reflexes:'⚡ Réflexes',schulte:'🔢 Table de Schulte',
    stroop:'🎨 Couleurs piégées',sudoku:'🧮 Sudoku junior',laby:'🌀 Labyrinthe'};
  const CDN=()=>(window.AUDIO_CDN||'https://pub-8cdc5500f1ab4785ba254b7335f7a68a.r2.dev');
  let onglet=null,jourOuvert=null,audio=null;

  const L=()=>window.PARCOURS||[];
  const age=()=>{try{return ageNum(P().age);}catch(e){return 8;}};
  function semaine(){const d=new Date();d.setHours(0,0,0,0);d.setDate(d.getDate()-((d.getDay()+6)%7));return d.toISOString().slice(0,10);}
  function etat(){const p=P();if(!p)return{};p.parcours=p.parcours||{};const s=semaine();if(p.parcours.sem!==s){p.parcours.sem=s;p.parcours.fait={};}return p.parcours;}
  function fait(pid,j){return !!(etat().fait||{})[pid+'|'+j];}
  function marquer(pid,j,v){const e=etat();e.fait=e.fait||{};e.fait[pid+'|'+j]=v;try{saveApp();}catch(x){}}
  function aujourd(){const d=(new Date().getDay()+6)%7;return d<5?d:-1;}   // -1 = week-end
  const esc=s=>String(s||'').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
  const propre=s=>esc(String(s||'').replace(/\s*\[P\d+\]\s*/g,' ').trim());

  function stopVoix(){try{if(audio){audio.pause();audio=null;}}catch(e){}try{ttsStop();}catch(e){}document.querySelectorAll('.pc-voix').forEach(b=>b.classList.remove('on'));}
  // Voix : MP3 enregistré (audio/parcours/<clé>.mp3), sinon voix du téléphone
  function voix(cle,texte,btn){stopVoix();if(btn)btn.classList.add('on');
    const fin=()=>{if(btn)btn.classList.remove('on');};
    const a=new Audio(`${CDN()}/audio/parcours/${cle}.mp3`);audio=a;a.onended=fin;
    a.play().catch(()=>{audio=null;try{ttsSpeak(String(texte).replace(/\s*\[P\d+\]\s*/g,' … '),'FR');}catch(e){}setTimeout(fin,1500);});}

  window.openParcours=function(id){
    document.querySelectorAll('.nb').forEach(b=>b.classList.remove('active'));
    const p=P();if(!onglet)onglet=id||(p&&p.parcoursReco)||'PC-CONC';if(id)onglet=id;
    show('parcours');rendre();
    if(p&&!p.parcoursQuizVu){p.parcoursQuizVu=1;try{saveApp();}catch(e){}setTimeout(()=>parcoursQuiz(),400);}
  };

  function rendre(){
    const c=document.getElementById('parcours-c');if(!c)return;stopVoix();c.innerHTML='';
    const tabs=document.createElement('div');tabs.className='pc-tabs';
    [...L().map(x=>({id:x.id,t:x.nom_enfant})),{id:'MIX',t:'⚡ Mix'}].forEach(o=>{const b=document.createElement('button');b.className='pc-tab'+(o.id===onglet?' on':'');
      b.textContent=o.t;if(COUL[o.id])b.style.setProperty('--pc',COUL[o.id]);b.onclick=()=>{try{sndTap();}catch(e){}onglet=o.id;jourOuvert=null;rendre();};tabs.appendChild(b);});
    c.appendChild(tabs);
    if(onglet==='MIX')return rendreMix(c);
    const pc=L().find(x=>x.id===onglet)||L()[0];if(!pc)return;onglet=pc.id;
    const col=COUL[pc.id]||'#6C63FF',auj=aujourd(),nb=JOURS.filter((j,i)=>fait(pc.id,i)).length;
    const h=document.createElement('div');h.className='pc-head';h.style.setProperty('--pc',col);
    h.innerHTML=`<div class="pc-h1">${esc(pc.nom_enfant)}</div><div class="pc-h2">${esc(pc.accroche_parent)}</div>
      <div class="pc-prog"><div style="width:${nb*20}%"></div></div><div class="pc-h3">${nb}/5 cette semaine${nb===5?' — bravo, super-pouvoir débloqué ! 🏆':''}</div>
      <div class="pc-row"><button class="pc-btn2" data-a="fiche">🖨️ Fiche de la semaine</button><button class="pc-btn2" data-a="quiz">❓ Quel parcours choisir ?</button></div>`;
    h.querySelector('[data-a=fiche]').onclick=()=>ficheSemaine(pc);h.querySelector('[data-a=quiz]').onclick=()=>parcoursQuiz();
    c.appendChild(h);
    if(auj<0){const w=document.createElement('div');w.className='pc-we';w.innerHTML=`<b>🎉 C’est le week-end !</b><br>Défi bonus, sans écran : ${esc(pc.fiche&&pc.fiche.defi_bonus)}`;c.appendChild(w);}
    (pc.jours||[]).forEach((j,i)=>c.appendChild(carteJour(pc,j,i,i===auj,col)));
  }

  function carteJour(pc,j,i,estAuj,col){
    const ouvert=jourOuvert===i||(jourOuvert===null&&estAuj);
    const d=document.createElement('div');d.className='pc-day'+(estAuj?' auj':'')+(fait(pc.id,i)?' fait':'');d.style.setProperty('--pc',col);
    const a=j.activite||{},A=age();
    d.innerHTML=`<button class="pc-dh"><span class="pc-dn">${fait(pc.id,i)?'✅':(estAuj?'👉':'○')} ${esc(j.jour||JOURS[i])}</span><span class="pc-dt">${esc(a.titre||j.theme)}</span><span class="pc-chev">${ouvert?'▲':'▼'}</span></button>`;
    d.querySelector('.pc-dh').onclick=()=>{jourOuvert=ouvert?-1:i;rendre();};
    if(!ouvert)return d;
    const b=document.createElement('div');b.className='pc-db';
    const jeu=Object.assign({},j.jeu||{});if(A<=5&&{stroop:1,schulte:1}[jeu.id]){jeu.id=jeu.id==='stroop'?'memory':'simon';jeu.pourquoi='Version des petits : un jeu sans lecture, pour s’entraîner pareil.';}
    b.innerHTML=`
      <div class="pc-step"><div class="pc-sn">1</div><div class="pc-sc"><b>Jeu de l’appli : ${esc(NOM_JEU[jeu.id]||jeu.id)}</b><div class="pc-small">${esc(jeu.pourquoi)}</div>
        <button class="pc-btn" data-a="jeu">▶ Jouer</button></div></div>
      <div class="pc-step"><div class="pc-sn">2</div><div class="pc-sc"><b>Sans écran : ${esc(a.titre)}</b> <span class="pc-small">· ${a.duree_min||3} min${a.materiel&&a.materiel!=='aucun'?' · '+esc(a.materiel):''}</span>
        <div class="pc-small">Pose le téléphone, écoute la voix et joue !</div>
        <button class="pc-btn pc-voix" data-a="act">🔊 Écouter et jouer</button>
        <details class="pc-det"><summary>Lire les consignes</summary><p>${propre(a.script).replace(/\n+/g,'</p><p>')}</p></details>
        <div class="pc-var">${A<=6&&a.petits?'🧸 <b>Petits :</b> '+esc(a.petits):a.grands&&A>=7?'🚀 <b>Grands :</b> '+esc(a.grands):''}${a.a_deux?'<br>👨‍👧 <b>À deux :</b> '+esc(a.a_deux):''}</div></div></div>
      <div class="pc-step"><div class="pc-sn">3</div><div class="pc-sc"><b>Moment calme</b><div class="pc-small">${j.calme&&j.calme.ref?esc(titreCalme(j.calme.ref)):'Petite respiration guidée (1 min)'}</div>
        <button class="pc-btn" data-a="calme">🌬️ Respirer</button></div></div>
      <label class="pc-ok"><input type="checkbox" ${fait(pc.id,i)?'checked':''}> J’ai fait mon super-pouvoir du jour !</label>`;
    b.querySelector('[data-a=jeu]').onclick=()=>{stopVoix();try{if(typeof startGame==='function')startGame(jeu.id);else openJeux();}catch(e){openJeux();}};
    const bv=b.querySelector('[data-a=act]');bv.onclick=()=>{if(bv.classList.contains('on'))return stopVoix();voix(a.id,a.script,bv);};
    b.querySelector('[data-a=calme]').onclick=e=>{const c=j.calme||{};
      if(c.ref){const it=(DATA.meditation||[]).concat(DATA.histoires||[]).find(x=>x.id===c.ref);if(it){stopVoix();openReader(it,c.ref.startsWith('MED')?'meditation':'audio');return;}}
      voix(`${pc.id}-J${i+1}-calme`,c.script||'Inspire doucement par le nez… et souffle lentement par la bouche. Encore une fois…',e.currentTarget);};
    b.querySelector('input').onchange=e=>{marquer(pc.id,i,e.target.checked);if(e.target.checked){try{sndOK();}catch(x){}toast('🏆 Super-pouvoir du jour : fait !');}rendre();};
    d.appendChild(b);return d;
  }
  function titreCalme(ref){const it=(DATA.meditation||[]).concat(DATA.histoires||[]).find(x=>x.id===ref);return it?it.titre:ref;}

  // ⚡ Mix : l'activité du jour de chaque parcours, pour varier
  function rendreMix(c){const auj=Math.max(0,aujourd());
    const h=document.createElement('div');h.className='pc-head';h.style.setProperty('--pc','#6C63FF');
    h.innerHTML=`<div class="pc-h1">⚡ Le mix du jour</div><div class="pc-h2">Une activité sans écran de chaque super-pouvoir. Choisis celle qui te fait envie !</div>`;c.appendChild(h);
    L().forEach(pc=>{const j=(pc.jours||[])[auj];if(!j)return;const a=j.activite||{};
      const d=document.createElement('div');d.className='pc-day';d.style.setProperty('--pc',COUL[pc.id]||'#6C63FF');
      d.innerHTML=`<div class="pc-mix"><div><div class="pc-small">${esc(pc.nom_enfant)}</div><b>${esc(a.titre)}</b> <span class="pc-small">· ${a.duree_min||3} min</span></div><button class="pc-btn pc-voix">🔊 Jouer</button></div>`;
      const bv=d.querySelector('.pc-voix');bv.onclick=()=>{if(bv.classList.contains('on'))return stopVoix();voix(a.id,a.script,bv);};c.appendChild(d);});}

  // ❓ Mini-quiz parent : 5 affirmations → parcours conseillé
  const QZ=[['PC-CONC','Il ou elle a du mal à rester sur une activité, se laisse vite distraire.'],['PC-MEM','Les consignes s’oublient vite (« j’ai oublié ce que je devais faire »).'],
    ['PC-CALME','Agit avant de réfléchir, a du mal à attendre son tour.'],['PC-EMO','Les grosses émotions débordent vite (colère, larmes, peur).'],['PC-PERS','Abandonne vite quand c’est difficile, a peur de se tromper.']];
  window.parcoursQuiz=function(){const rep={};const m=document.createElement('div');m.className='ps-modal';
    const draw=()=>{m.innerHTML=`<div class="pm-box" style="text-align:left;max-height:88vh;overflow:auto"><div class="pm-t" style="text-align:center">❓ Quel super-pouvoir en premier ?</div>
      <div class="pm-x" style="text-align:center">Pour le parent · 1 minute. Ces derniers temps, chez votre enfant :</div>
      ${QZ.map(([id,q],k)=>`<div class="pc-q"><div>${q}</div><div class="pc-qr">${['Souvent','Parfois','Rarement'].map((l,v)=>`<button data-k="${k}" data-v="${2-v}" class="${rep[k]===2-v?'on':''}">${l}</button>`).join('')}</div></div>`).join('')}
      <button class="pm-a" ${Object.keys(rep).length<5?'disabled style="opacity:.5"':''}>Voir le parcours conseillé</button><button class="pm-b">Plus tard</button>
      <div style="font-size:11px;color:#888;margin-top:8px;line-height:1.4">Un simple point de départ pour choisir un jeu, pas un bilan. Tous les parcours conviennent à tous les enfants. Rien n’est envoyé.</div></div>`;
      m.querySelectorAll('[data-k]').forEach(b=>b.onclick=()=>{rep[b.dataset.k]=+b.dataset.v;draw();});
      m.querySelector('.pm-b').onclick=()=>m.remove();
      m.querySelector('.pm-a').onclick=()=>{if(Object.keys(rep).length<5)return;let best=0;QZ.forEach((x,k)=>{if(rep[k]>rep[best])best=k;});
        const id=QZ[best][0],p=P();if(p){p.parcoursReco=id;try{saveApp();}catch(e){}}m.remove();onglet=id;jourOuvert=null;
        const pc=L().find(x=>x.id===id);toast('👉 Parcours conseillé : '+(pc?pc.nom_enfant:id));if(document.getElementById('scr-parcours').classList.contains('on'))rendre();else openParcours(id);};};
    draw();document.body.appendChild(m);};

  // 🖨️ Fiche « Mon programme de la semaine » (PDF prêt sur le CDN, sinon version imprimable générée ici)
  function ficheSemaine(pc){const url=`${CDN()}/fiches/FR/${pc.id}.pdf`;
    fetch(url,{method:'HEAD'}).then(r=>{if(r.ok){window.open(url,'_blank');return;}throw 0;}).catch(()=>{
      const w=window.open('','_blank');if(!w){toast('Autorise l’ouverture de fenêtre pour imprimer');return;}
      w.document.write(`<html><head><meta charset="utf-8"><title>${esc(pc.fiche&&pc.fiche.titre)}</title><style>body{font-family:Arial,sans-serif;padding:24px}h1{font-size:22px}td{border:2px solid #333;padding:10px;font-size:15px}table{border-collapse:collapse;width:100%}.c{width:40px;text-align:center;font-size:22px}</style></head><body>
        <h1>${esc(pc.fiche&&pc.fiche.titre)}</h1><p>Prénom : ____________________</p><table>${(pc.jours||[]).map(j=>`<tr><td><b>${esc(j.jour)}</b></td><td>${esc((j.activite||{}).titre)}</td><td class="c">☐</td></tr>`).join('')}
        <tr><td><b>Week-end</b></td><td>Défi bonus : ${esc(pc.fiche&&pc.fiche.defi_bonus)}</td><td class="c">☐</td></tr></table><p style="margin-top:30px">PocketSage Academy · pocketsage.org</p></body></html>`);w.document.close();});}
})();
