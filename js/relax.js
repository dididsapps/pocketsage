// ═══ 🌿 Relaxation — méditations guidées par âge, respirations, ambiances sonores ═══
// Données : data/relax.json (généré par tools/relax_build.py depuis docs/contenu/relaxation/meditations.json, vérifié).
// Voix : voix du téléphone, pauses réglables ; MP3 audio/relax/<id>.mp3 prévu (Google, à partir du 1er décembre).
// Ambiances : sons générés par le téléphone (Web Audio) : aucun fichier, aucun coût, marche hors ligne.
// Règle : aucune promesse de santé ; les tonalités sont seulement nommées par leur fréquence.
(function(){
  const V=((document.currentScript&&document.currentScript.src.match(/[?&]v=(\d+)/))||[])[1]||'';
  let DATA_RX=null,vue=null,dureeK=1,ageTout=false,session=null;
  const esc=s=>String(s||'').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
  const DUREES=[['Court',1],['Moyen',1.8],['Long',2.6]];

  // ───────── Sons (Web Audio) ─────────
  let ac=null,master=null,amb=null,ambId=null,ambTimer=null,vol=0.5,minuterie=0;
  function ctx(){if(!ac){const C=window.AudioContext||window.webkitAudioContext;if(!C)return null;ac=new C();master=ac.createGain();master.gain.value=vol;master.connect(ac.destination);}
    if(ac.state==='suspended')ac.resume();return ac;}
  function bruit(type){const a=ctx(),n=a.sampleRate*4,b=a.createBuffer(1,n,a.sampleRate),d=b.getChannelData(0);let l=0,b0=0,b1=0,b2=0;
    for(let i=0;i<n;i++){const w=Math.random()*2-1;
      if(type==='brun'){l=(l+0.02*w)/1.02;d[i]=l*3.5;}
      else{b0=0.99765*b0+w*0.099046;b1=0.963*b1+w*0.2965164;b2=0.57*b2+w*1.0526913;d[i]=(b0+b1+b2+w*0.1848)*0.11;}}
    const s=a.createBufferSource();s.buffer=b;s.loop=true;return s;}
  function lfo(a,f,min,max,cible){const o=a.createOscillator(),g=a.createGain();o.frequency.value=f;g.gain.value=(max-min)/2;cible.value=(max+min)/2;o.connect(g);g.connect(cible);o.start();return o;}
  function frappe(a,out,base,dec,force){const t=a.currentTime;[[1,1],[2.76,.45],[5.4,.22],[8.9,.1]].forEach(([k,v],i)=>{
      [0,1.6].forEach(det=>{const o=a.createOscillator(),g=a.createGain();o.type='sine';o.frequency.value=base*k+det*(i+1)*0.5;
        g.gain.setValueAtTime(0,t);g.gain.linearRampToValueAtTime(v*force*0.5,t+0.02);g.gain.exponentialRampToValueAtTime(0.0001,t+dec/(1+i*0.6));
        o.connect(g);g.connect(out);o.start(t);o.stop(t+dec+0.1);});});}
  window.relaxCloche=function(){const a=ctx();if(!a)return;frappe(a,master,523.25,6,0.9);};
  function stopAmb(fade){if(!amb)return;const x=amb;amb=null;ambId=null;clearInterval(ambTimer);ambTimer=null;
    try{const t=ac.currentTime;x.g.gain.cancelScheduledValues(t);x.g.gain.setValueAtTime(x.g.gain.value,t);x.g.gain.linearRampToValueAtTime(0,t+(fade||1.2));
      setTimeout(()=>{x.nodes.forEach(n=>{try{n.stop();}catch(e){}try{n.disconnect();}catch(e){}});try{x.g.disconnect();}catch(e){}},(fade||1.2)*1000+200);}catch(e){}
    majAmb();}
  function jouerAmb(id){const a=ctx();if(!a)return;stopAmb(0.6);
    const g=a.createGain();g.gain.value=0;g.connect(master);const nodes=[];let bol=null;
    if(id==='pluie'){const s=bruit('rose'),h=a.createBiquadFilter(),l=a.createBiquadFilter();h.type='highpass';h.frequency.value=500;l.type='lowpass';l.frequency.value=7000;
      s.connect(h);h.connect(l);l.connect(g);s.start();nodes.push(s,lfo(a,0.3,0.85,1,g.gain));}
    else if(id==='vagues'){const s=bruit('brun'),l=a.createBiquadFilter(),gg=a.createGain();l.type='lowpass';l.frequency.value=900;
      s.connect(l);l.connect(gg);gg.connect(g);s.start();nodes.push(s,lfo(a,0.085,0.12,1,gg.gain),lfo(a,0.085,500,1300,l.frequency));}
    else if(id==='vent'){const s=bruit('brun'),b=a.createBiquadFilter();b.type='bandpass';b.Q.value=0.8;
      s.connect(b);b.connect(g);s.start();nodes.push(s,lfo(a,0.05,250,900,b.frequency));}
    else if(id==='bol'){bol=()=>frappe(a,g,196,9,1);bol();}
    else if(id==='f432'||id==='f528'){const f=id==='f432'?432:528;[[f,0.16],[f/2,0.08]].forEach(([fr,v])=>{const o=a.createOscillator(),og=a.createGain();o.type='sine';o.frequency.value=fr;og.gain.value=v;o.connect(og);og.connect(g);o.start();nodes.push(o);});}
    g.gain.linearRampToValueAtTime(1,a.currentTime+2);
    amb={g,nodes};ambId=id;if(bol)ambTimer=setInterval(()=>{if(amb&&ambId==='bol')bol();},10000);
    if(minuterie){const me=amb;setTimeout(()=>{if(amb===me)stopAmb(4);},minuterie*60000);}
    majAmb();}
  window.relaxStopSons=()=>stopAmb(0.8);

  function ambHTML(){const L=(DATA_RX&&DATA_RX.ambiances)||[];
    return `<div class="rx-amb"><div class="rx-at">🎧 Ambiance sonore <small>(au choix, pendant ou sans méditation)</small></div>
      <div class="rx-chips">${L.map(x=>`<button class="rx-chip" data-a="${x.id}">${x.emoji} ${esc(x.nom)}</button>`).join('')}</div>
      <div class="rx-ctl"><label>🔉 <input type="range" min="0" max="100" value="${Math.round(vol*100)}" class="rx-vol"></label>
      <select class="rx-min"><option value="0">Sans arrêt auto</option><option value="10">Arrêt après 10 min</option><option value="20">Arrêt après 20 min</option><option value="30">Arrêt après 30 min</option></select></div></div>`;}
  function brancherAmb(el){el.querySelectorAll('.rx-chip').forEach(b=>b.onclick=()=>{try{sndTap();}catch(e){}b.dataset.a===ambId?stopAmb():jouerAmb(b.dataset.a);});
    const v=el.querySelector('.rx-vol');if(v)v.oninput=()=>{vol=v.value/100;if(master)master.gain.value=vol;};
    const m=el.querySelector('.rx-min');if(m){m.value=String(minuterie);m.onchange=()=>{minuterie=+m.value;if(ambId)jouerAmb(ambId);};}
    majAmb();}
  function majAmb(){document.querySelectorAll('.rx-chip').forEach(b=>b.classList.toggle('on',b.dataset.a===ambId));}

  // ───────── Voix ─────────
  let wake=null;
  function dire(t,cb){if(APP&&APP.silent){setTimeout(cb,600);return;}
    try{speechSynthesis.cancel();const u=new SpeechSynthesisUtterance(typeof _ttsParle==='function'?_ttsParle(t,'FR'):t);u.lang='fr-FR';
      u.rate=Math.max(0.7,(typeof _ttsRate!=='undefined'?_ttsRate:1)*0.85);u.pitch=1;try{if(_ttsVoices&&_ttsVoices.FR)u.voice=_ttsVoices.FR;}catch(e){}
      let fini=false;const f=()=>{if(fini)return;fini=true;cb();};u.onend=f;u.onerror=e=>{if(e.error==='interrupted'||e.error==='canceled')return;f();};
      speechSynthesis.speak(u);}catch(e){setTimeout(cb,t.length*70);}}
  function arreter(){if(session){session.stop=true;clearTimeout(session.to);session=null;}try{speechSynthesis.cancel();}catch(e){}try{if(wake){wake.release();wake=null;}}catch(e){}}
  window.relaxArreter=arreter;

  // ───────── Écrans ─────────
  async function charger(){if(DATA_RX)return DATA_RX;try{DATA_RX=await (await fetch('data/relax.json?v='+V)).json();}catch(e){DATA_RX={meditations:[],ambiances:[]};}return DATA_RX;}
  const ageP=()=>{try{return typeof _getSliderAge==='function'?_getSliderAge():parseInt(P().age)||8;}catch(e){return 8;}};
  const ok=a=>ageTout||(typeof _ageMatch==='function'?_ageMatch(a,ageP(),false):true);
  const minutes=m=>Math.max(1,Math.round(m.etapes.reduce((s,e)=>s+e.p*dureeK+(e.t==='[CLOCHE]'?0:e.t.length/13),0)/60));

  window.openRelax=async function(){arreter();vue=null;document.querySelectorAll('.nb').forEach(b=>b.classList.remove('active'));show('relax');await rendre();};
  async function rendre(){
    const c=document.getElementById('relax-c');if(!c)return;await charger();
    if(vue)return rendreSeance(c);
    c.innerHTML='';const D=DATA_RX,meds=D.meditations.filter(m=>ok(m.age)),court=((typeof DATA!=='undefined'&&DATA.meditation)||[]).filter(m=>ok(m.age));
    const resp=((typeof DATA!=='undefined'&&DATA.defis)||[]).filter(d=>d.cat==='respiration'&&ok(d.age));
    c.insertAdjacentHTML('beforeend',`<div class="rx-hero"><div class="rx-he">🌿</div><div><b>Relaxation</b><span>Quelques minutes pour se poser, respirer et revenir au calme. À faire souvent, même très court : c'est la régularité qui compte.</span></div></div>`);
    c.insertAdjacentHTML('beforeend',ambHTML());brancherAmb(c);
    c.insertAdjacentHTML('beforeend',`<label class="rx-tout"><input type="checkbox" ${ageTout?'checked':''}> Voir les séances de tous les âges</label>`);
    c.querySelector('.rx-tout input').onchange=e=>{ageTout=e.target.checked;rendre();};
    const sec=(t)=>c.insertAdjacentHTML('beforeend',`<div class="rx-sec">${t}</div>`);
    const p=P()||{},faits=p.relax||{};
    if(meds.length){sec('🧘 Méditations guidées');meds.forEach(m=>{const b=document.createElement('button');b.className='rx-card';
      b.innerHTML=`<span class="rx-ce">${esc(m.emoji)}</span><span class="rx-ct"><b>${esc(m.titre)}</b><small>${esc(m.moment)} · ${minutes(m)} min · ${esc(m.age)} ans</small></span><span class="rx-cs">${faits[m.id]?'✓ '+faits[m.id]:'▶'}</span>`;
      b.onclick=()=>{try{sndTap();}catch(e){}vue={type:'rx',m};rendre();};c.appendChild(b);});}
    if(court.length){sec('✨ Méditations courtes');court.forEach(m=>{const b=document.createElement('button');b.className='rx-card';
      b.innerHTML=`<span class="rx-ce">${esc((m.titre.match(/\p{Emoji_Presentation}/u)||['🧘'])[0])}</span><span class="rx-ct"><b>${esc(m.titre.replace(/\p{Emoji_Presentation}/gu,'').trim())}</b><small>${Math.ceil((m.dur||60)/60)} min · ${esc(m.age)} ans</small></span><span class="rx-cs">▶</span>`;
      b.onclick=()=>{try{sndTap();}catch(e){}vue={type:'rx',m:{id:m.id,titre:m.titre.replace(/\p{Emoji_Presentation}/gu,'').trim(),emoji:(m.titre.match(/\p{Emoji_Presentation}/u)||['🧘'])[0],age:m.age,moment:'Méditation courte',technique:'',
        etapes:m.texte.split(/(?<=[.!?…])\s+/).filter(Boolean).map(t=>({t,p:/inspire|expire|souffle|retiens|respir|répète/i.test(t)?6:2.5}))}};rendre();};c.appendChild(b);});}
    if(resp.length){sec('🌬️ Respirations');resp.forEach((d,i)=>{const b=document.createElement('button');b.className='rx-card';
      b.innerHTML=`<span class="rx-ce">🌬️</span><span class="rx-ct"><b>${esc(d.nom)}</b><small>${d.dur||30} s · ${esc(d.age||'')} ans</small></span><span class="rx-cs">▶</span>`;
      b.onclick=()=>{try{sndTap();}catch(e){}APP._retRelax=true;startDefi(d,i,resp);};c.appendChild(b);});}
    const y=document.createElement('button');y.className='rx-lien';y.innerHTML='🧘 Envie de bouger en douceur ? Le <b>yoga</b> et le <b>yoga en famille</b> sont dans Sport ›';
    y.onclick=()=>{try{sndTap();}catch(e){}(APP.tabKey=APP.tabKey||{}).defis='yoga';openMod('defis');};c.appendChild(y);
    c.insertAdjacentHTML('beforeend',`<p class="rx-note">Ces exercices sont des moments de calme et d'attention, pas un soin. En cas de difficulté qui dure, parlez-en à l'enseignant ou au médecin.</p>`);
  }

  function rendreSeance(c){
    const m=vue.m;c.innerHTML='';
    const w=document.createElement('div');w.className='rx-seance';
    w.innerHTML=`<button class="rx-back">‹ Relaxation</button>
      <div class="rx-st"><span>${esc(m.emoji)}</span>${esc(m.titre)}</div>
      <div class="rx-sm">${m.technique?esc(m.technique)+' · ':''}${esc(m.moment)} · ${esc(m.age)} ans</div>
      <div class="rx-dur">${DUREES.map(([l,k])=>`<button data-k="${k}" class="${k===dureeK?'on':''}">${l}</button>`).join('')}<span class="rx-min2">≈ ${minutes(m)} min</span></div>
      <div class="rx-txt">Installe-toi confortablement. Appuie sur Commencer quand tu es prêt.</div>
      <div class="rx-prog"><div></div></div>
      <button class="rx-go">▶ Commencer</button>
      ${ambHTML()}`;
    c.appendChild(w);brancherAmb(w);
    w.querySelector('.rx-back').onclick=()=>{arreter();vue=null;rendre();};
    w.querySelectorAll('.rx-dur button').forEach(b=>b.onclick=()=>{if(session)return;dureeK=+b.dataset.k;rendreSeance(c);});
    const go=w.querySelector('.rx-go'),txt=w.querySelector('.rx-txt'),bar=w.querySelector('.rx-prog div');
    go.onclick=async()=>{
      if(session){arreter();go.textContent='▶ Recommencer';txt.textContent='Séance arrêtée. Tu peux recommencer quand tu veux.';return;}
      try{sndTap();}catch(e){}ctx();try{if(typeof _ttsUnlock==='function')_ttsUnlock();}catch(e){}
      try{if(navigator.wakeLock)wake=await navigator.wakeLock.request('screen');}catch(e){}
      const S=session={stop:false,to:null};go.textContent='⏹ Arrêter';let i=0;const n=m.etapes.length;
      const suite=()=>{if(S.stop)return;if(i>=n){fin();return;}const e=m.etapes[i++];bar.style.width=Math.round(i*100/n)+'%';
        const apres=()=>{if(S.stop)return;S.to=setTimeout(suite,Math.round(e.p*dureeK*1000));};
        if(e.t==='[CLOCHE]'){txt.textContent='🔔';relaxCloche();apres();}else{txt.textContent=e.t;dire(e.t,apres);}};
      const fin=()=>{session=null;try{if(wake){wake.release();wake=null;}}catch(e){}relaxCloche();go.textContent='▶ Refaire';
        txt.textContent='Terminé. Prends un moment avant de reprendre tes activités. 🌿';
        try{const p=P();if(p){p.relax=p.relax||{};p.relax[m.id]=(p.relax[m.id]||0)+1;saveApp();}}catch(e){}};
      suite();};
  }
})();
