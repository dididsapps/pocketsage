// PocketSage — compléments de questions (chargé après index.html)
// 1) Remet à leur place des questions rangées dans le mauvais tableau (ex. des questions de
//    français ou d'espagnol dans le module Anglais).
// 2) Ajoute les nouvelles questions (collège / lycée…), toutes passées par la vérification
//    indépendante (« moulinette ») avant d'être ajoutées ici.
(function(){
  if(typeof DATA==='undefined')return;
  const DEST={MA:'maths',SC:'sciences',HI:'histoire',GE:'geo',LG:'suites',FR:'francais'};
  const LANG_DE={AN:'EN',ES:'ES',FLE:'FR'};
  function ranger(it){const p=(it.id||'').split('-')[0];
    if(DEST[p]&&Array.isArray(DATA[DEST[p]])){DATA[DEST[p]].push(it);return true;}
    if(LANG_DE[p]&&DATA.langues&&Array.isArray(DATA.langues[LANG_DE[p]])){DATA.langues[LANG_DE[p]].push(it);return true;}
    return false;}
  try{ // 1) questions mal rangées dans les tableaux de langues
    const L=DATA.langues||{};
    for(const k in L){const arr=L[k];if(!Array.isArray(arr))continue;const garde=[];
      arr.forEach(it=>{const p=(it&&it.id||'').split('-')[0];const bon=LANG_DE[p]===k;if(!bon&&(DEST[p]||LANG_DE[p])&&ranger(it))return;garde.push(it);});
      L[k]=garde;}
  }catch(e){console.warn('questions-plus: rangement',e);}
  try{ // 2) nouvelles questions
    const deja=new Set();for(const k in DEST){(DATA[DEST[k]]||[]).forEach(i=>i&&i.id&&deja.add(i.id));}
    (window.QUESTIONS_PLUS||[]).forEach(it=>{if(it&&it.id&&!deja.has(it.id))ranger(it);});
  }catch(e){console.warn('questions-plus: ajout',e);}
})();
