// ═══ 📄 Fiches de révision — par classe, matière et grand axe du programme ═══
// Données : data/fiches/<LANG>/<CL>.json (générées par tools/fiches_build.py depuis docs/contenu/fiches/FR/*.json, vérifiés).
// Chargement à la demande (une classe à la fois). Voix : MP3 audio/fiches/<id>.mp3 (GS→CE2), sinon voix du téléphone.
(function(){
  const V=((document.currentScript&&document.currentScript.src.match(/[?&]v=(\d+)/))||[])[1]||'';
  const CDN=()=>(window.AUDIO_CDN||'https://pub-8cdc5500f1ab4785ba254b7335f7a68a.r2.dev');
  const MAT={FR:['📝','Français','#E8590C'],MA:['🔢','Maths','#3B82F6'],QM:['🌱','Questionner le monde','#10B981'],SC:['🔬','Sciences','#10B981'],
    SVT:['🧬','SVT','#16A34A'],PC:['⚗️','Physique-chimie','#0EA5E9'],TE:['⚙️','Technologie','#64748B'],HI:['📜','Histoire','#B45309'],GE:['🌍','Géographie','#0D9488'],
    SES:['📈','SES','#7C3AED'],ESC:['🔭','Ens. scientifique','#0891B2'],PHI:['💭','Philosophie','#9333EA'],HGG:['🗺️','HGGSP','#A16207'],AN:['🇬🇧','Anglais','#DC2626'],ES:['🇪🇸','Espagnol','#D97706']};
  const ORDRE=['FR','MA','QM','SC','SVT','PC','TE','HI','GE','HGG','SES','ESC','PHI','AN','ES'];
  const APP2FI={'GS':['GS'],'CP':['CP'],'CE1':['CE1'],'CE2':['CE2'],'CM1':['CM1'],'CM2':['CM2'],'6ème':['6E'],'5ème':['5E'],'4ème':['4E'],'3ème':['3E'],'Lycée':['2DE','1RE','TLE'],'Sup':['TLE']};
  const NOMCL={GS:'Grande section',CP:'CP',CE1:'CE1',CE2:'CE2',CM1:'CM1',CM2:'CM2','6E':'6e','5E':'5e','4E':'4e','3E':'3e','2DE':'Seconde','1RE':'Première',TLE:'Terminale'};
  const PETITS=['GS','CP','CE1','CE2'];
  const cache={};let index=null,cl=null,mat=null,fiche=null,audio=null;
  const esc=s=>String(s||'').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
  const lang=()=>{try{return String(APP.lang||'FR').toUpperCase();}catch(e){return 'FR';}};

  async function getIndex(){if(index)return index;try{index=await (await fetch('data/fiches/index.json?v='+V)).json();}catch(e){index={};}return index;}
  async function charger(c){const L=lang(),k=L+'/'+c;if(cache[k])return cache[k];
    for(const l of (L==='FR'?['FR']:[L,'FR'])){try{const r=await fetch(`data/fiches/${l}/${c}.json?v=`+V);if(r.ok){cache[k]=await r.json();return cache[k];}}catch(e){}}
    return cache[k]={};}
  function etat(){const p=P();if(!p)return{};return p.fiches=p.fiches||{};}
  function stopVoix(){try{if(audio){audio.pause();audio=null;}}catch(e){}try{ttsStop();}catch(e){}document.querySelectorAll('.fi-voix').forEach(b=>b.classList.remove('on'));}
  // même ordre que fiche_lue() dans tools/fiches_build.py (MP3 + surlignage)
  function morceaux(f){return [f.titre,f.en_une_phrase,f.comprendre,...(f.essentiel||[]),f.image_mentale,f.regle_ou_methode,...(f.exemples||[]),f.piege,f.astuce_memoire].filter(x=>x&&String(x).trim());}
  function lire(f,btn){if(btn.classList.contains('on')){stopVoix();return;}stopVoix();btn.classList.add('on');
    const fin=()=>{btn.classList.remove('on');try{_hlStop();}catch(e){}},L=lang();
    const txt=morceaux(f).map(x=>/[.!?…:]$/.test(x.trim())?x:x+'.').join(' ');
    const device=()=>{audio=null;try{ttsSpeak(txt,L);}catch(e){}setTimeout(fin,1500);};
    if(L==='FR'&&PETITS.includes(cl)&&mat!=='AN'){const a=new Audio(`${CDN()}/audio/fiches/${f.id}.mp3`);audio=a;a.onended=fin;
      a.play().then(()=>{try{if(_hlWanted('FR'))_hlGet('fiches/'+f.id).then(st=>{if(audio===a&&st)_hlStart([...document.querySelectorAll('#fiches-c .fi-lu')],st,()=>(audio===a&&!a.ended)?a.currentTime:null,true);});}catch(e){}}).catch(device);}
    else device();}

  window.openFiches=async function(code,classeApp){
    document.querySelectorAll('.nb').forEach(b=>b.classList.remove('active'));
    const ca=classeApp||(typeof _selClasse==='function'?_selClasse():'CP');
    const choix=APP2FI[ca]||['CP'];if(!cl||!choix.includes(cl)||classeApp)cl=choix[0];
    mat=code||mat;fiche=null;show('fiches');await rendre();
  };
  window.fichesDispo=async function(classeApp,code){const ix=await getIndex();return (APP2FI[classeApp]||[]).some(c=>(ix[c]||[]).includes(code));};

  async function rendre(){
    const c=document.getElementById('fiches-c');if(!c)return;stopVoix();c.innerHTML='<p class="fi-vide">Chargement…</p>';
    const ix=await getIndex();
    if(fiche)return rendreFiche(c);
    const data=await charger(cl);c.innerHTML='';
    // classes
    const ca=Object.keys(APP2FI).find(k=>APP2FI[k].includes(cl)&&k!=='Sup');
    const bar=document.createElement('div');bar.className='fi-cls';
    const tous=['GS','CP','CE1','CE2','CM1','CM2','6E','5E','4E','3E','2DE','1RE','TLE'];
    tous.forEach(k=>{const b=document.createElement('button');const ok=(ix[k]||[]).length;b.className='fi-cl'+(k===cl?' on':'')+(ok?'':' off');b.textContent=NOMCL[k];
      b.onclick=()=>{if(!ok){toast('Fiches bientôt disponibles pour cette classe','info');return;}try{sndTap();}catch(e){}cl=k;mat=null;rendre();};bar.appendChild(b);});
    c.appendChild(bar);setTimeout(()=>{const o=bar.querySelector('.on');if(o)o.scrollIntoView({inline:'center',block:'nearest'});},0);
    const codes=ORDRE.filter(k=>data[k]);
    if(!codes.length){c.insertAdjacentHTML('beforeend','<p class="fi-vide">Les fiches de cette classe arrivent bientôt. 📄</p>');return;}
    if(!mat||!data[mat])mat=codes[0];
    const tb=document.createElement('div');tb.className='fi-mats';
    codes.forEach(k=>{const m=MAT[k]||['📄',k,'#6C63FF'];const b=document.createElement('button');b.className='fi-mat'+(k===mat?' on':'');b.style.setProperty('--fc',m[2]);
      b.textContent=m[0]+' '+m[1];b.onclick=()=>{try{sndTap();}catch(e){}mat=k;rendre();};tb.appendChild(b);});
    c.appendChild(tb);
    const d=data[mat],m=MAT[mat]||['📄',mat,'#6C63FF'],st=etat();
    const fs=d.fiches||[],nbOk=fs.filter(f=>st[f.id]&&st[f.id].s===3).length;
    const h=document.createElement('div');h.className='fi-head';h.style.setProperty('--fc',m[2]);
    h.innerHTML=`<div class="fi-h1">${m[0]} ${esc(d.matiere||m[1])} · ${esc(NOMCL[cl])}</div><div class="fi-h2">${fs.length} fiches · ${nbOk} réussies sans faute</div>
      <div class="fi-prog"><div style="width:${fs.length?Math.round(nbOk*100/fs.length):0}%"></div></div>
      <div class="fi-row"><a class="fi-btn2" href="${CDN()}/fiches/${lang()==='FR'?'FR':lang()}/REV-${mat}-${cl}.pdf" target="_blank" rel="noopener">🖨️ PDF à imprimer</a></div>`;
    c.appendChild(h);
    const axes=[];fs.forEach(f=>{let a=axes.find(x=>x.n===f.axe);if(!a)axes.push(a={n:f.axe,l:[]});a.l.push(f);});
    axes.forEach(a=>{const s=document.createElement('div');s.className='fi-axe';s.innerHTML=`<div class="fi-axt">${esc(a.n)}</div>`;
      a.l.forEach(f=>{const r=st[f.id];const b=document.createElement('button');b.className='fi-card';b.style.setProperty('--fc',m[2]);
        b.innerHTML=`<span class="fi-ce">${esc(f.emoji||'📄')}</span><span class="fi-ct"><b>${esc(f.titre)}</b><small>${esc(f.en_une_phrase)}</small></span><span class="fi-cs">${r?(r.s===3?'⭐':r.s+'/3'):'›'}</span>`;
        b.onclick=()=>{try{sndTap();}catch(e){}fiche=f.id;rendre();};s.appendChild(b);});
      c.appendChild(s);});
  }

  function bloc(t,cls,html){return html?`<div class="fi-b ${cls||''}"><div class="fi-bt">${t}</div>${html}</div>`:'';}
  async function rendreFiche(c){
    const data=await charger(cl),d=data[mat]||{},fs=d.fiches||[],i=fs.findIndex(x=>x.id===fiche),f=fs[i];
    if(!f){fiche=null;return rendre();}
    const m=MAT[mat]||['📄',mat,'#6C63FF'];c.innerHTML='';
    const w=document.createElement('div');w.className='fi-fiche';w.style.setProperty('--fc',m[2]);
    const li=a=>(a&&a.length)?'<ul>'+a.map(x=>`<li class="fi-lu">${esc(x)}</li>`).join('')+'</ul>':'';const pp=x=>x?`<p class="fi-lu">${esc(x)}</p>`:'';
    w.innerHTML=`<button class="fi-back">‹ ${esc(m[1])} · ${esc(f.axe)}</button>
      <div class="fi-ft"><span>${esc(f.emoji||'📄')}</span><span class="fi-lu">${esc(f.titre)}</span></div>
      <div class="fi-cle fi-lu">${esc(f.en_une_phrase)}</div>
      <button class="fi-btn fi-voix">🔊 Écouter la fiche</button>
      ${bloc('💡 Comprendre','',pp(f.comprendre))}
      ${bloc('📌 À retenir','fi-ret',li(f.essentiel))}
      ${bloc('🖼️ Image pour retenir','',pp(f.image_mentale))}
      ${bloc('📐 Règle ou méthode','fi-reg',pp(f.regle_ou_methode))}
      ${bloc('✏️ Exemples','',li(f.exemples))}
      ${bloc('⚠️ Le piège','fi-pie',pp(f.piege))}
      ${bloc('🧠 Astuce','',pp(f.astuce_memoire))}
      <div class="fi-quiz"></div>
      <div class="fi-nav">${i>0?'<button class="fi-btn2b" data-n="-1">‹ Fiche précédente</button>':'<span></span>'}${i<fs.length-1?'<button class="fi-btn2b" data-n="1">Fiche suivante ›</button>':''}</div>`;
    c.appendChild(w);c.scrollTop=0;try{document.querySelector('#scr-fiches .sc').scrollTop=0;}catch(e){}
    w.querySelector('.fi-back').onclick=()=>{fiche=null;rendre();};
    w.querySelector('.fi-voix').onclick=e=>lire(f,e.currentTarget);
    w.querySelectorAll('[data-n]').forEach(b=>b.onclick=()=>{fiche=fs[i+ +b.dataset.n].id;rendre();});
    quiz(w.querySelector('.fi-quiz'),f);
  }

  function quiz(el,f){
    const qs=f.quiz||[];let n=0,ok=0;
    const intro=()=>{el.innerHTML=`<div class="fi-qt">🎯 Je me teste</div><p class="fi-qi">Cache la fiche dans ta tête et réponds sans regarder : c’est comme ça qu’on retient le mieux !</p><button class="fi-btn">C’est parti (3 questions)</button>`;
      el.querySelector('button').onclick=()=>{try{stopVoix();}catch(e){}q();};};
    const q=()=>{const x=qs[n];if(!x)return fin();const ch=[...x.choix].sort(()=>Math.random()-.5);
      el.innerHTML=`<div class="fi-qt">🎯 Question ${n+1}/${qs.length}</div><div class="fi-qq">${esc(x.q)}</div><div class="fi-ch"></div><div class="fi-ex"></div>`;
      const box=el.querySelector('.fi-ch');
      ch.forEach(v=>{const b=document.createElement('button');b.textContent=v;b.onclick=()=>{
        const bon=v===x.rep;if(bon)ok++;try{bon?sndOk():sndBad();}catch(e){}
        box.querySelectorAll('button').forEach(z=>{z.disabled=true;if(z.textContent===x.rep)z.classList.add('ok');else if(z===b)z.classList.add('ko');});
        el.querySelector('.fi-ex').innerHTML=`<p><b>${bon?'Bravo !':'Pas tout à fait.'}</b> ${esc(x.expl)}</p><button class="fi-btn">${n<qs.length-1?'Question suivante':'Voir mon résultat'}</button>`;
        el.querySelector('.fi-ex button').onclick=()=>{n++;q();};};box.appendChild(b);});};
    const fin=()=>{const st=etat(),av=st[f.id];st[f.id]={s:Math.max(ok,av?av.s:0),d:Date.now()};try{saveApp();}catch(e){}
      try{if(ok&&typeof addScore==='function')addScore(ok);}catch(e){}
      el.innerHTML=`<div class="fi-qt">${ok===qs.length?'⭐ Parfait !':'💪 Résultat'}</div><p class="fi-qi">${ok}/${qs.length} bonnes réponses. ${ok===qs.length?'Tu maîtrises cette fiche.':'Relis la partie « À retenir » puis réessaie demain : revoir après une nuit aide à mieux retenir.'}</p><button class="fi-btn">Recommencer</button>`;
      el.querySelector('button').onclick=()=>{n=0;ok=0;q();};};
    if(qs.length)intro();
  }
  // Entrée depuis Savoirs : onglet « 📄 Fiches » et bandeau en haut des onglets Maths / Géo / Sciences / Histoire
  const TAB2={maths:['MA'],geo:['GE','QM'],sci:['QM','SC','SVT','PC','ESC'],hist:['HI','QM']};
  window.fichesEntree=async function(el){
    const ca=typeof _selClasse==='function'?_selClasse():'CP',ix=await getIndex();
    const cls=(APP2FI[ca]||[]).filter(c=>(ix[c]||[]).length);
    el.innerHTML='';const w=document.createElement('div');w.className='fi-entree';
    if(!cls.length){w.innerHTML='<div class="fi-h1">📄 Fiches de révision</div><p>Les fiches de cette classe arrivent bientôt.</p>';el.appendChild(w);return;}
    w.innerHTML='<div class="fi-h1">📄 Fiches de révision</div><p>Lis, écoute, puis teste-toi sans regarder. Version PDF à imprimer.</p><div class="fi-mats"></div>';
    const box=w.querySelector('.fi-mats');
    cls.forEach(c=>ORDRE.filter(k=>(ix[c]||[]).includes(k)).forEach(k=>{const m=MAT[k]||['📄',k,'#6C63FF'];const b=document.createElement('button');b.className='fi-mat';b.style.setProperty('--fc',m[2]);
      b.textContent=m[0]+' '+m[1]+(cls.length>1?' · '+NOMCL[c]:'');b.onclick=()=>{try{sndTap();}catch(e){}cl=c;mat=k;fiche=null;document.querySelectorAll('.nb').forEach(x=>x.classList.remove('active'));show('fiches');rendre();};box.appendChild(b);}));
    el.appendChild(w);};
  window.fichesBanniere=async function(el,k){
    try{const ca=_selClasse(),ix=await getIndex();let hit=null;
      for(const c of (APP2FI[ca]||[]))for(const code of (TAB2[k]||[]))if(!hit&&(ix[c]||[]).includes(code))hit=[c,code];
      if(!hit||el.querySelector('.fi-ban'))return;const m=MAT[hit[1]];
      const b=document.createElement('button');b.className='fi-ban';b.style.setProperty('--fc',m[2]);
      b.innerHTML=`<span>📄</span><span><b>Fiches de révision · ${esc(m[1])}</b><small>Comprendre, retenir, se tester · PDF</small></span><span>›</span>`;
      b.onclick=()=>{try{sndTap();}catch(e){}cl=hit[0];mat=hit[1];fiche=null;document.querySelectorAll('.nb').forEach(x=>x.classList.remove('active'));show('fiches');rendre();};
      el.prepend(b);}catch(e){}};
})();
