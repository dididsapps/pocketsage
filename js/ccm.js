// ═══ 🛠️ Comment ça marche ? — parcours de leçons courtes (cartes + schémas animés + quiz) ═══
// Données : data/ccm/<LANG>/index.json et data/ccm/<LANG>/<ID>.json (tools/ccm_build.py, depuis docs/contenu/ccm/FR, vérifiés).
// Schémas : assets/ccm/<lecon>-<n>.svg. Vidéos « pour aller plus loin » : lien externe (YouTube), vérifiées, désactivables par le parent.
(function(){
  const V=((document.currentScript&&document.currentScript.src.match(/[?&]v=(\d+)/))||[])[1]||'';
  const esc=s=>String(s||'').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
  const lang=()=>{try{return String(APP.lang||'FR').toUpperCase();}catch(e){return 'FR';}};
  let IDX=null;const cache={};let theme=null,lecon=null,carte=0,retour=null;
  const estBP=t=>/^BP-/.test(t.id||t);
  async function j(u){try{const r=await fetch(u+'?v='+V);if(r.ok)return await r.json();}catch(e){}return null;}
  async function index(){if(IDX)return IDX;IDX=(await j(`data/ccm/${lang()}/index.json`))||(await j('data/ccm/FR/index.json'))||{themes:[]};return IDX;}
  async function charger(id){if(cache[id])return cache[id];return cache[id]=(await j(`data/ccm/${lang()}/${id}.json`))||(await j(`data/ccm/FR/${id}.json`));}
  const etat=()=>{const p=P();if(!p)return{};return p.ccm=p.ccm||{};};
  const age=()=>{try{return _getSliderAge();}catch(e){return 14;}};
  const pourMoi=t=>t.public==='enfant'?age()<=12:age()>=12;
  const videosOk=()=>{try{const p=P();return !(p&&p.ccmVideosOff);}catch(e){return true;}};

  window.openCCM=async function(id,from){document.querySelectorAll('.nb').forEach(b=>b.classList.remove('active'));theme=id||null;lecon=null;retour=from||null;show('ccm');await rendre();};
  // Thèmes « Bien parler » (BP-*) : affichés dans l'onglet Bien parler de Politesse, pas dans la liste principale.
  window.ccmBienParler=async function(){const ix=await index();return {pourMoi:ix.themes.filter(t=>estBP(t)&&pourMoi(t)),autres:ix.themes.filter(t=>estBP(t)&&!pourMoi(t)),fait:t=>(t.lecons||[]).filter(id=>etat()[id]).length};};
  async function rendre(){
    const c=document.getElementById('ccm-c');if(!c)return;try{ttsStop();}catch(e){}
    if(lecon)return rendreLecon(c);if(theme)return rendreTheme(c);
    const ix=await index(),st=etat();c.innerHTML='';
    c.insertAdjacentHTML('beforeend',`<div class="cc-hero"><div class="cc-he">🛠️</div><div><b>Comment ça marche ?</b><span>Des leçons de quelques minutes pour comprendre les objets et la vie de tous les jours. « Ah, c'est donc pour ça ! »</span></div></div>`);
    const TH=ix.themes.filter(t=>!estBP(t)),L=TH.filter(pourMoi),autres=TH.filter(t=>!pourMoi(t));
    const grille=(arr,titre)=>{if(!arr.length)return;c.insertAdjacentHTML('beforeend',`<div class="cc-sec">${titre}</div>`);const g=document.createElement('div');g.className='cc-grid';
      arr.forEach(t=>{const fait=(t.lecons||[]).filter(id=>st[id]).length,n=(t.lecons||[]).length;const b=document.createElement('button');b.className='cc-tile';b.style.setProperty('--cc',t.couleur||'#3B82F6');
        b.innerHTML=`<span class="cc-te">${esc(t.emoji||'🛠️')}</span><b>${esc(t.titre)}</b><small>${n} leçons${fait?` · ${fait} faites`:''}</small><i style="width:${n?Math.round(fait*100/n):0}%"></i>`;
        b.onclick=()=>{try{sndTap();}catch(e){}theme=t.id;rendre();};g.appendChild(b);});c.appendChild(g);};
    grille(L,'Pour toi');grille(autres,'Autres thèmes');
    if(!TH.length)c.insertAdjacentHTML('beforeend','<p class="cc-vide">Les premiers thèmes arrivent très bientôt.</p>');
  }
  async function rendreTheme(c){
    const d=await charger(theme),st=etat();c.innerHTML='';if(!d){theme=null;return rendre();}
    const t=(IDX&&IDX.themes.find(x=>x.id===theme))||{};
    const h=document.createElement('div');h.className='cc-head';h.style.setProperty('--cc',t.couleur||'#3B82F6');
    h.innerHTML=`<button class="cc-back">‹ ${retour==='politesse'?'Bien parler':'Tous les thèmes'}</button><div class="cc-h1">${esc(t.emoji||'🛠️')} ${esc(d.titre)}</div><div class="cc-h2">${d.lecons.length} leçons de quelques minutes</div>`;
    h.querySelector('.cc-back').onclick=()=>{if(retour==='politesse'){try{openPolitesse(3);}catch(e){}return;}theme=null;rendre();};c.appendChild(h);
    d.lecons.forEach((l,i)=>{const r=st[l.id];const b=document.createElement('button');b.className='cc-lec';b.style.setProperty('--cc',t.couleur||'#3B82F6');
      b.innerHTML=`<span class="cc-num">${r?'✓':i+1}</span><span class="cc-lt"><b>${esc(l.titre)}</b><small>${esc(l.accroche||'')}</small></span><span class="cc-min">${l.duree_min||8} min</span>`;
      b.onclick=()=>{try{sndTap();}catch(e){}lecon=l.id;carte=0;rendre();};c.appendChild(b);});
  }
  function schema(lid,n){return `<div class="cc-sch"><img src="assets/ccm/${lid}-${n}.svg?v=${V}" alt="" onerror="this.parentNode.classList.add('vide')"></div>`;}
  async function rendreLecon(c){
    const d=await charger(theme),l=d&&d.lecons.find(x=>x.id===lecon);if(!l){lecon=null;return rendre();}
    const t=(IDX&&IDX.themes.find(x=>x.id===theme))||{},col=t.couleur||'#3B82F6',N=l.cartes.length;
    c.innerHTML='';const w=document.createElement('div');w.className='cc-lecon';w.style.setProperty('--cc',col);c.appendChild(w);
    const etape=()=>{
      try{ttsStop();}catch(e){}
      const dots=Array.from({length:N+1},(_,i)=>`<i class="${i===carte?'on':i<carte?'ok':''}"></i>`).join('');
      if(carte<N){const k=l.cartes[carte];
        w.innerHTML=`<button class="cc-back">‹ ${esc(d.titre)}</button><div class="cc-dots">${dots}</div>
          <div class="cc-card">${k.schema?schema(l.id,carte+1):''}<div class="cc-ct">${esc(k.titre)}</div><p>${esc(k.texte)}</p>
          <button class="cc-voix">🔊 Écouter</button></div>
          <div class="cc-nav">${carte>0?'<button class="cc-b2" data-d="-1">‹ Précédent</button>':'<span></span>'}<button class="cc-b1" data-d="1">${carte<N-1?'Suivant ›':'Je résume ›'}</button></div>`;
        w.querySelector('.cc-voix').onclick=()=>{try{ttsSpeak(k.titre+'. '+k.texte,lang());}catch(e){}};
      }else{
        const v=l.video&&l.video.titre&&videosOk();
        w.innerHTML=`<button class="cc-back">‹ ${esc(d.titre)}</button><div class="cc-dots">${dots}</div>
          <div class="cc-box cc-vie"><div class="cc-bt">💡 Dans ta vie</div><p>${esc(l.dans_ta_vie)}</p></div>
          ${l.securite?`<div class="cc-box cc-sec2"><div class="cc-bt">⚠️ Sécurité</div><p>${esc(l.securite)}</p></div>`:''}
          ${l.defi?`<div class="cc-box"><div class="cc-bt">🎯 Ton défi</div><p>${esc(l.defi)}</p></div>`:''}
          <div class="cc-quiz"></div>
          ${v?`<a class="cc-video" href="https://www.youtube.com/results?search_query=${encodeURIComponent(l.video.titre+' '+(l.video.chaine||''))}" target="_blank" rel="noopener">🎬 Pour aller plus loin : « ${esc(l.video.titre)} »${l.video.chaine?' · '+esc(l.video.chaine):''}</a>`:''}
          <div class="cc-nav"><button class="cc-b2" data-d="-1">‹ Revoir les cartes</button><span></span></div>`;
        quiz(w.querySelector('.cc-quiz'),l);
      }
      w.querySelector('.cc-back').onclick=()=>{lecon=null;rendre();};
      w.querySelectorAll('[data-d]').forEach(b=>b.onclick=()=>{try{sndTap();}catch(e){}carte=Math.max(0,Math.min(N,carte+ +b.dataset.d));etape();window.scrollTo(0,0);try{document.querySelector('#scr-ccm .sc').scrollTop=0;}catch(e){}});
    };
    etape();
  }
  function quiz(el,l){
    const qs=l.quiz||[];let n=0,ok=0;
    const q=()=>{const x=qs[n];if(!x)return fin();const ch=[...x.choix].sort(()=>Math.random()-.5);
      el.innerHTML=`<div class="cc-qt">🎯 Question ${n+1}/${qs.length}</div><div class="cc-qq">${esc(x.q)}</div><div class="cc-ch"></div><div class="cc-ex"></div>`;
      const box=el.querySelector('.cc-ch');
      ch.forEach(v=>{const b=document.createElement('button');b.textContent=v;b.onclick=()=>{const bon=v===x.rep;if(bon)ok++;try{bon?sndOk():sndBad();}catch(e){}
        box.querySelectorAll('button').forEach(z=>{z.disabled=true;if(z.textContent===x.rep)z.classList.add('ok');else if(z===b)z.classList.add('ko');});
        el.querySelector('.cc-ex').innerHTML=`<p><b>${bon?'Bravo !':'Pas tout à fait.'}</b> ${esc(x.expl)}</p><button class="cc-b1">${n<qs.length-1?'Question suivante':'Voir mon résultat'}</button>`;
        el.querySelector('.cc-ex button').onclick=()=>{n++;q();};};box.appendChild(b);});};
    const fin=()=>{const st=etat();st[l.id]=Math.max(ok,st[l.id]||0)||1;try{saveApp();}catch(e){}try{if(ok&&typeof addScore==='function')addScore(ok);}catch(e){}
      el.innerHTML=`<div class="cc-qt">${ok===qs.length?'⭐ Parfait !':'💪 Leçon terminée'}</div><p>${ok}/${qs.length} bonnes réponses.</p><button class="cc-b1">Leçon suivante ›</button>`;
      el.querySelector('button').onclick=async()=>{const d=await charger(theme),i=d.lecons.findIndex(x=>x.id===l.id);lecon=d.lecons[i+1]?d.lecons[i+1].id:null;carte=0;rendre();};};
    if(qs.length)q();
  }
})();
