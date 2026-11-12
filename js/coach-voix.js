// PocketSage — Voix du Coach Sportif + mode « Mains libres » (12/11/2026)
// - Toutes les phrases du coach sont construites ici (mêmes textes pour l'appli ET pour le
//   générateur de MP3 tools/sport_texts.js → gen_sport_mp3.py).
// - coachSay() joue le MP3 Google (voix énergique) s'il existe, sinon la voix du téléphone.
// - hfListen() écoute « GO », « NEXT », « RÉPÈTE » (mode mains libres, micro autorisé par le parent).
(function(root){
'use strict';
const clean=s=>String(s||'').replace(/[\p{Extended_Pictographic}️‍]/gu,'').replace(/\s+/g,' ').trim();
const T={
  intro:(plan,n)=>`Séance pour ${plan.label} ! ${n} exercices. Prépare-toi !`,
  first:'Premier exercice !',
  phase:lbl=>clean(lbl)+' !',
  nom:item=>clean(item.nom)+'.',
  consigne:item=>clean(item.consigne),
  count:['Un !','Deux !','Trois !'],
  bravo:'Bravo ! Super !',
  sayGo:'Dis GO quand tu es prêt !',
  sayNext:"Dis NEXT pour l'exercice suivant.",
  sayNextLast:'Dis NEXT pour terminer la séance.',
  end:n=>`Bravo ! Séance complète terminée ! ${n} exercices réussis comme un champion !`,
  left:n=>`Encore ${n} secondes !`,
  dayEnd:"Bravo, séance terminée ! Montre à tes parents ce que tu as appris aujourd'hui. À demain !"
};
function allTexts(defis,plans,phases,msgs){
  const out=new Set([T.first,T.bravo,T.sayGo,T.sayNext,T.sayNextLast,T.dayEnd,...T.count]);
  for(let n=10;n<=120;n+=10)out.add(T.left(n));
  Object.values(plans).forEach(p=>{out.add(T.intro(p,p.pattern.length));out.add(T.end(p.pattern.length));});
  Object.values(phases).forEach(a=>a.forEach(l=>out.add(T.phase(l))));
  Object.values(msgs).forEach(a=>a.forEach(m=>out.add(clean(m))));
  defis.forEach(d=>{out.add(T.nom(d));out.add(T.consigne(d));});
  return [...out].filter(Boolean).sort();
}
root.COACH_TXT=T;root.coachClean=clean;root.coachAllTexts=allTexts;
if(typeof module!=='undefined'&&module.exports)module.exports={T,clean,allTexts};
if(typeof window==='undefined')return;

// ── Lecture : MP3 Google si dispo, sinon voix du téléphone ─────────────────
let _man=null,_manP=null,_aud=null,_sayTok=0;
function loadMan(){if(_man)return Promise.resolve(_man);if(_manP)return _manP;
  _manP=fetch('data/sport/fr.audio.json',{cache:'no-cache'}).then(r=>r.ok?r.json():{}).catch(()=>({})).then(m=>(_man=m||{}));return _manP;}
function coachStopVoice(){_sayTok++;try{if(_aud){_aud.pause();_aud=null;}}catch(e){}try{ttsStop();}catch(e){}}
function coachSay(text,done){
  const tok=++_sayTok;const fin=()=>{if(tok===_sayTok&&done)done();};
  text=clean(text);
  if(!text||(typeof APP!=='undefined'&&APP&&APP.silent)){setTimeout(fin,150);return;}
  loadMan().then(m=>{
    if(tok!==_sayTok)return;
    const h=m[text];
    const phone=()=>{try{ttsSpeak(text,'fr-FR');}catch(e){}setTimeout(fin,Math.min(9000,700+text.length*62));};
    if(!h){phone();return;}
    try{
      const base=(typeof AUDIO_CDN!=='undefined'?AUDIO_CDN:'https://audio.pocketsage.org');
      const a=new Audio(`${base}/audio/sport/fr/${h}.mp3`);_aud=a;
      let ended=false;const end=()=>{if(ended)return;ended=true;fin();};
      a.onended=end;a.onerror=()=>{if(!ended){ended=true;phone();}};
      const p=a.play();if(p&&p.catch)p.catch(()=>{if(!ended){ended=true;phone();}});
    }catch(e){phone();}
  });
}
function coachSayList(list,done){const l=list.filter(Boolean);let i=0;const nx=()=>{if(i>=l.length){done&&done();return;}coachSay(l[i++],nx);};nx();}

// ── Mains libres : écoute de « GO », « NEXT », « RÉPÈTE » ──────────────────
const HF_WORDS={
  go:['go','gogo','partez','c est parti','cest parti','top depart','vas y','on y va'],
  next:['next','nexte','suivant','suivante','continue','continuer','exercice suivant'],
  repeat:['repete','repeter','repetes','encore une fois','redis']
};
function hfMatch(t){
  const s=' '+String(t).toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g,'').replace(/[^a-z ]/g,' ').replace(/\s+/g,' ').trim()+' ';
  for(const k in HF_WORDS)if(HF_WORDS[k].some(w=>s.includes(' '+w+' ')))return k;
  return null;
}
let _hf=null;
function hfBadge(label,onTap){
  let b=document.getElementById('hf-badge');
  if(!label){if(b)b.remove();return;}
  if(!b){b=document.createElement('button');b.id='hf-badge';document.body.appendChild(b);}
  b.innerHTML='<span class="hf-dot"></span>🎤 '+label;b.onclick=onTap||null;
}
function hfStop(){if(_hf){_hf.stopped=true;try{_hf.rec&&_hf.rec.abort();}catch(e){}_hf=null;}hfBadge(null);}
function hfAvailable(){const SR=window.SpeechRecognition||window.webkitSpeechRecognition;return !!SR&&(typeof micAllowed!=='function'||micAllowed());}
// cmds : {go:fn, next:fn, repeat:fn} ; label : texte du badge ; tap : action si on touche le badge
function hfListen(cmds,label,tap){
  hfStop();
  const SR=window.SpeechRecognition||window.webkitSpeechRecognition;
  if(!hfAvailable())return false;
  const st={stopped:false};_hf=st;hfBadge(label,tap?()=>{hfStop();tap();}:null);
  const run=()=>{
    if(st.stopped)return;
    let rec;try{rec=new SR();}catch(e){return;}
    st.rec=rec;rec.lang='fr-FR';rec.continuous=true;rec.interimResults=true;rec.maxAlternatives=3;
    try{if('processLocally' in rec&&typeof _micLocal!=='undefined'&&_micLocal['fr-FR']==='available')rec.processLocally=true;}catch(e){}
    rec.onresult=e=>{
      for(let i=e.resultIndex;i<e.results.length;i++)for(let k=0;k<e.results[i].length;k++){
        const c=hfMatch(e.results[i][k].transcript);
        if(c&&cmds[c]){st.stopped=true;try{rec.abort();}catch(_){}if(_hf===st)_hf=null;hfBadge(null);try{sndTap();}catch(_){}cmds[c]();return;}
      }
    };
    rec.onerror=e=>{if(e.error==='not-allowed'||e.error==='service-not-allowed'){st.stopped=true;hfBadge(null);try{toast('🎤 Micro non autorisé : utilise les boutons.');}catch(_){}}};
    rec.onend=()=>{if(!st.stopped)setTimeout(run,250);};
    try{rec.start();}catch(e){setTimeout(run,600);}
  };
  run();return true;
}
Object.assign(window,{coachSay,coachSayList,coachStopVoice,hfListen,hfStop,hfAvailable,hfMatch});
})(typeof window!=='undefined'?window:globalThis);
