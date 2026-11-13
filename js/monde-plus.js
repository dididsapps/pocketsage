// PocketSage — Mon Monde : commandes, fabrication, ateliers-métiers, album, saisons, photo, animal, famille (13/11/2026)
// Branché sur la ville par window.__w3 (API), window.w3Hooks (dessin) et quelques crochets (w3OnHarvest, w3OnStep, w3Fish, w3TapPeople, w3CardExtra).
// Toutes les données sont dans W3.extra (sauvegardées avec la ville).
(function(){
'use strict';
const LEVELS_ON=false; // niveaux de ville : prêts, à activer avant TestFlight
const A=()=>window.__w3,W=()=>A()&&A().W3;
function X(){const w=W();if(!w.extra)w.extra={};const e=w.extra;e.inv=e.inv||{};e.orders=e.orders||[];e.prod=e.prod||{};e.album=e.album||{};e.family=e.family||[];e.xp=e.xp||0;return e;}
function save(){try{A().save();A().hud();}catch(e){}}
function toast(t){try{A().msg(t);}catch(e){}}
function age(){try{const p=window.P&&window.P();return +(p&&p.age)||8;}catch(e){return 8;}}
function rnd(n){return Math.floor(Math.random()*n);}
function pick(a){return a[rnd(a.length)];}
function say(t,l){try{ttsSpeak(t,l||'fr-FR');}catch(e){}}
function star(){try{sndStar();}catch(e){}}
function coins(n){const w=W();w.coins+=n;save();}
function joie(n){const L=W().life;if(L)L.joie=Math.max(0,Math.min(100,L.joie+n));try{A().panel();}catch(e){}}
function xp(n){X().xp+=n;if(LEVELS_ON)rail();}
window.w3Hooks=window.w3Hooks||{draw:[],overlay:[]};

// ── Produits, récoltes, recettes ────────────────────────────────────────
const G={corn:['🌽','Maïs',3],wheat:['🌾','Blé',2],carrot:['🥕','Carotte',3],tomato:['🍅','Tomate',4],salad:['🥬','Salade',3],strawberry:['🍓','Fraise',5],pumpkin:['🎃','Citrouille',6],
  apple:['🍎','Pomme',4],milk:['🥛','Lait',4],egg:['🥚','Œuf',3],flour:['🥣','Farine',6],bread:['🍞','Pain',10],croissant:['🥐','Croissant',14],cake:['🎂','Gâteau',30],
  cheese:['🧀','Fromage',12],butter:['🧈','Beurre',9],pizza:['🍕','Pizza',28],icecream:['🍦','Glace',12],corncob:['🍿','Popcorn',8]};
const HARV={farm:'corn',wheat:'wheat',carrot:'carrot',tomato:'tomato',salad:'salad',strawberry:'strawberry',pumpkin:'pumpkin',orchard:'apple',cow:'milk',chicken:'egg',barn:'wheat',silo:'corn'};
const REC={ // bâtiment -> [sortie, {entrées}, secondes]
  mill:[['flour',{wheat:2},20]],
  bakery:[['bread',{flour:1},25],['croissant',{flour:1,butter:1},35],['cake',{flour:2,egg:2,strawberry:1},60]],
  dairy:[['butter',{milk:1},20],['cheese',{milk:2},30]],
  pizzeria:[['pizza',{flour:1,tomato:2,cheese:1},45]],
  icecream:[['icecream',{milk:1,strawberry:1},25]],
  popcorn:[['corncob',{corn:2},20]]};
window.w3OnHarvest=(cell,c,r,amount)=>{const g=HARV[cell.id];if(!g)return;const e=X(),n=1+(amount>=20?1:0)+(amount>=60?1:0);e.inv[g]=(e.inv[g]||0)+n;xp(1);
  try{const p=A().toIso(c,r);W().floats.push({x:p.x,y:p.y-40,text:'+'+n+' '+G[g][0],life:80,dy:-0.4});}catch(e){}};

// ── Fenêtres (modales) ─────────────────────────────────────────────────
function modal(html,cls){const o=document.createElement('div');o.className='mp-ov';o.innerHTML=`<div class="mp-box ${cls||''}"><button class="mp-x">✖</button>${html}</div>`;document.body.appendChild(o);
  o.querySelector('.mp-x').onclick=()=>o.remove();o.addEventListener('click',e=>{if(e.target===o)o.remove();});return o;}

// ── Commandes à livrer ─────────────────────────────────────────────────
const CUST=['👵','👴','👩','👨','🧑','👧','👦','👩‍🍳','👨‍🌾','🧑‍🚒','👮','👩‍⚕️'];
function available(){const w=W(),have=new Set();Object.values(w.grid).forEach(g=>{if(HARV[g.id])have.add(HARV[g.id]);(REC[g.id]||[]).forEach(r=>have.add(r[0]));});
  const a=[...have];return a.length?a:['corn','carrot','egg'];}
function newOrder(){const av=available(),n=Math.min(av.length,age()<7?1+rnd(2):1+rnd(3)),lines={};const pool=[...av];
  for(let i=0;i<n;i++){const g=pool.splice(rnd(pool.length),1)[0];lines[g]=1+rnd(age()<7?3:5);}
  const val=Object.entries(lines).reduce((s,[g,q])=>s+q*G[g][2],0);return {who:pick(CUST),lines,val,bonus:5+Math.round(val*.2)};}
function orders(){const e=X();while(e.orders.length<3)e.orders.push(newOrder());return e.orders;}
function canDeliver(o){const inv=X().inv;return Object.entries(o.lines).every(([g,q])=>(inv[g]||0)>=q);}
function openOrders(tab){
  const e=X();orders();
  const inv=Object.entries(e.inv).filter(([g,n])=>n>0&&G[g]);
  const o=modal(`<h3>📋 Commandes & 🎒 Stock</h3><div class="mp-tabs"><button data-t="o" class="${tab!=='s'?'on':''}">📋 Commandes</button><button data-t="s" class="${tab==='s'?'on':''}">🎒 Mon stock</button></div>
    ${tab==='s'?`<div class="mp-stock">${inv.length?inv.map(([g,n])=>`<div><span>${G[g][0]}</span><b>${n}</b><small>${G[g][1]}</small></div>`).join(''):'<p>Ton stock est vide. Récolte tes champs, tes enclos, puis fabrique au moulin, à la boulangerie, à la laiterie… 🌾</p>'}</div>`:
    `<div class="mp-orders">${e.orders.map((od,i)=>`<div class="mp-ord ${canDeliver(od)?'ok':''}"><div class="who">${od.who}</div><div class="lines">${Object.entries(od.lines).map(([g,q])=>{const h=e.inv[g]||0;return `<span class="${h>=q?'have':''}">${G[g][0]} ×${q} <small>(${h})</small></span>`;}).join('')}</div>
      <div class="rew">💰 ${od.val}🪙 <small>+ bonus ${od.bonus}🪙</small></div><div class="btns"><button data-d="${i}" ${canDeliver(od)?'':'disabled'}>🚚 Livrer</button><button data-n="${i}" class="sec">🔄</button></div></div>`).join('')}</div>
    <p class="mp-hint">Livre une commande puis réponds à la question pour gagner le bonus !</p>`}`);
  o.querySelectorAll('[data-t]').forEach(b=>b.onclick=()=>{o.remove();openOrders(b.dataset.t);});
  o.querySelectorAll('[data-n]').forEach(b=>b.onclick=()=>{e.orders[+b.dataset.n]=newOrder();save();o.remove();openOrders();});
  o.querySelectorAll('[data-d]').forEach(b=>b.onclick=()=>{const i=+b.dataset.d,od=e.orders[i];if(!canDeliver(od))return;Object.entries(od.lines).forEach(([g,q])=>e.inv[g]-=q);o.remove();quizOrder(od,i);});
}
function quizOrder(od,i){
  const e=X(),young=age()<7,lines=Object.entries(od.lines);
  const right=young?lines.reduce((s,[g,q])=>s+q,0):od.val;
  const q=young?`Combien d’objets as-tu livrés en tout ?<br><big>${lines.map(([g,q])=>`${G[g][0]}×${q}`).join(' + ')}</big>`:`Combien vaut la commande ?<br><big>${lines.map(([g,q])=>`${q} ${G[g][0]} × ${G[g][2]}🪙`).join(' + ')}</big>`;
  const opts=[...new Set([right,right+1+rnd(3),Math.max(1,right-1-rnd(3)),right+5])].slice(0,3).sort(()=>Math.random()-.5);
  const o=modal(`<h3>🚚 Commande livrée à ${od.who} !</h3><p class="mp-q">${q}</p><div class="mp-opts">${opts.map(v=>`<button data-v="${v}">${v}${young?'':' 🪙'}</button>`).join('')}</div>`);
  o.querySelectorAll('[data-v]').forEach(b=>b.onclick=()=>{const ok=+b.dataset.v===right;const gain=od.val+(ok?od.bonus:0);coins(gain);xp(ok?12:8);joie(6);
    e.orders[i]=newOrder();save();if(ok)star();
    o.querySelector('.mp-box').innerHTML=`<h3>${ok?'🎉 Bravo !':'🙂 Presque !'}</h3><p class="mp-q">${ok?'C’était bien '+right+(young?'':' 🪙')+' !':'La bonne réponse était <b>'+right+'</b>.'}</p><p class="mp-q">Tu gagnes <b>${gain} 🪙</b>${ok?' (bonus compris)':''}</p><div class="mp-opts"><button class="mp-close">Super !</button></div>`;
    o.querySelector('.mp-close').onclick=()=>o.remove();});
}

// ── Fabrication (moulin, boulangerie, laiterie, pizzeria, glacier, popcorn) ─
function openFab(cell,k){
  const e=X(),rs=REC[cell.id];if(!rs)return;const cur=e.prod[k];
  const o=modal(`<h3>🏭 Fabriquer — ${(A().catalog.find(c=>c.id===cell.id)||{}).label||''}</h3><div class="mp-fab" id="mp-fab"></div>`);
  const draw=()=>{const box=o.querySelector('#mp-fab');if(!box){clearInterval(iv);return;}const p=e.prod[k];
    if(p){const r=rs[p.r],left=Math.max(0,Math.ceil((p.end-Date.now())/1000)),k2=1-left/r[2];
      box.innerHTML=left>0?`<div class="mp-run">${G[r[0]][0]} ${G[r[0]][1]} en préparation…<div class="bar"><i style="width:${Math.round(k2*100)}%"></i></div>encore ${left} s</div>`:
        `<div class="mp-run">✅ ${G[r[0]][0]} ${G[r[0]][1]} est prêt !<br><button id="mp-get">Récupérer ${G[r[0]][0]}</button></div>`;
      const gb=box.querySelector('#mp-get');if(gb)gb.onclick=()=>{e.inv[r[0]]=(e.inv[r[0]]||0)+1;delete e.prod[k];xp(4);save();star();draw();};return;}
    box.innerHTML=rs.map((r,i)=>{const ok=Object.entries(r[1]).every(([g,q])=>(e.inv[g]||0)>=q);return `<div class="mp-rec"><div class="out">${G[r[0]][0]}<small>${G[r[0]][1]}</small></div><div class="in">${Object.entries(r[1]).map(([g,q])=>`<span class="${(e.inv[g]||0)>=q?'have':''}">${G[g][0]}×${q} <small>(${e.inv[g]||0})</small></span>`).join(' + ')}<br><small>⏱️ ${r[2]} s</small></div><button data-r="${i}" ${ok?'':'disabled'}>Lancer</button></div>`;}).join('');
    box.querySelectorAll('[data-r]').forEach(b=>b.onclick=()=>{const r=rs[+b.dataset.r];Object.entries(r[1]).forEach(([g,q])=>e.inv[g]-=q);e.prod[k]={r:+b.dataset.r,end:Date.now()+r[2]*1000};save();draw();});};
  draw();const iv=setInterval(draw,1000);
}
window.w3Hooks.draw.push(ctx=>{const e=X(),now=Date.now();Object.entries(e.prod).forEach(([k,p])=>{const [c,r]=k.split(',').map(Number),q=A().toIso(c,r),done=now>=p.end;
  const y=q.y-46+Math.sin(W().t*0.08)*2;ctx.fillStyle='rgba(255,255,255,.95)';ctx.beginPath();ctx.roundRect(q.x-12,y-12,24,22,9);ctx.fill();ctx.font='14px serif';ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillStyle='#000';ctx.fillText(done?'✅':'⏳',q.x,y);});});

// ── Ateliers-métiers : pizza, gâteau, glace, bouquet, burger, caisse ───
const ATELIER={pizzeria:'pizza',resto:'burger',bakery:'gateau',icecream:'glace',florist:'bouquet',supermarket:'caisse',shop:'caisse',pharmacy:'caisse'};
const ATN={pizza:'Pizzaïolo 🍕',burger:'Cuisinier 🍔',gateau:'Pâtissier 🎂',glace:'Glacier 🍦',bouquet:'Fleuriste 💐',caisse:'Caissier 🧾'};
window.w3CardExtra=(cell,k)=>{let h='';if(REC[cell.id])h+=`<button data-a="plus:fab">🏭 Fabriquer${X().prod[k]?(Date.now()>=X().prod[k].end?' ✅':' ⏳'):''}</button>`;if(ATELIER[cell.id])h+=`<button data-a="plus:job" class="wc-main">🎯 Travailler (${ATN[ATELIER[cell.id]]})</button>`;return h;};
window.w3CardAction=(a,cell,k)=>{if(a==='fab')openFab(cell,k);if(a==='job')openAtelier(ATELIER[cell.id]);};
const ING={pizza:[['🍄','champignon'],['🫒','olive'],['🍅','tomate'],['🫑','poivron'],['🧀','fromage'],['🍍','ananas']],
  gateau:[['🕯️','bougie'],['🍓','fraise'],['🍒','cerise'],['🍫','carré de chocolat']],
  bouquet:[['🌹','rose'],['🌷','tulipe'],['🌻','tournesol'],['🌼','marguerite']],
  glace:[['#f78fb3','fraise'],['#7f5539','chocolat'],['#fff3c4','vanille'],['#95d5b2','menthe']],
  burger:[['#e9b872','pain'],['#7f3b22','steak'],['#f4c430','fromage'],['#74c69d','salade'],['#e63946','tomate'],['#d4a5e6','oignon']]};
function plural(n,w){return n>1?w.replace(/^(carré)/,'$1s').replace(/(?<!s)$/,w.endsWith('s')?'':'s'):w;}
function openAtelier(type){
  const a=age(),lvl=a<7?0:a<10?1:2,want={};let text='',seq=null,price=0,given=0;
  if(type==='caisse'){price=lvl===0?1+rnd(8):lvl===1?3+rnd(15):5+rnd(40);given=price<5?5:price<10?10:price<20?20:50;text=`Ça fait <b>${price} 🪙</b>. Le client te donne <b>${given} 🪙</b>.<br>Combien dois-tu lui rendre ?`;}
  else if(type==='burger'){const mid=ING.burger.slice(1);seq=['pain'];for(let i=0;i<(lvl===0?2:lvl===1?3:4);i++)seq.push(pick(mid)[1]);seq.push('pain');
    text=`Un burger, du bas vers le haut : <br>${seq.map(x=>'<b>'+x+'</b>').join(' → ')}`;}
  else{const pool=[...ING[type]];const n=type==='gateau'?2:Math.min(pool.length,lvl===0?1+rnd(2):lvl===1?2+rnd(2):3);
    if(type==='gateau'){const yrs=3+rnd(lvl===0?4:7);want['bougie']=yrs;want[pick(['fraise','cerise','carré de chocolat'])]=1+rnd(lvl===0?3:5);}
    else{for(let i=0;i<n;i++){const g=pool.splice(rnd(pool.length),1)[0];want[g[1]]=type==='glace'?1+rnd(lvl===0?1:2):1+rnd(lvl===0?4:lvl===1?6:9);}}
    const w=Object.entries(want).map(([k,v])=>`<b>${v}</b> ${(ING[type].find(x=>x[1]===k)||[''])[0].startsWith('#')?'boule'+(v>1?'s':'')+' '+k:(ING[type].find(x=>x[1]===k)||[''])[0]+' '+plural(v,k)}`);
    text=type==='pizza'?`Une pizza avec ${w.join(' et ')}, s’il te plaît !`:type==='gateau'?`J’ai <b>${want.bougie} ans</b> ! Un gâteau avec ${w.join(' et ')}.`:type==='glace'?`Une glace avec ${w.join(' et ')} !`:`Un bouquet avec ${w.join(' et ')}.`;}
  const cust=pick(CUST);
  const o=modal(`<h3>🎯 ${ATN[type]}</h3><div class="at-order"><span class="at-cust">${cust}</span><div class="at-bub">${text} <button class="at-say">🔊</button></div></div>
    <div class="at-stage"><div class="at-base at-${type}" id="at-base"></div></div>
    <div class="at-ings">${type==='caisse'?[1,2,5,10,20].filter(v=>v<given).map(v=>`<button data-c="${v}" class="coin">${v}🪙</button>`).join(''):ING[type].map(([e,n])=>`<button data-i="${n}">${e.startsWith('#')?`<i style="background:${e}"></i>`:e}<small>${n}</small></button>`).join('')}</div>
    <div class="at-act"><button id="at-clear" class="sec">🔄 Recommencer</button><button id="at-ok">✅ Servir</button></div>`,'mp-atelier');
  o.querySelector('.at-say').onclick=()=>say(o.querySelector('.at-bub').textContent.replace('🔊',''));
  const base=o.querySelector('#at-base'),placed=[];
  const render=()=>{base.innerHTML='';
    if(type==='glace'||type==='burger'){placed.forEach((n,i)=>{const col=(ING[type].find(x=>x[1]===n)||['#ccc'])[0];const d=document.createElement('div');d.className='at-layer';d.style.background=col;d.style.bottom=(type==='glace'?92:14)+i*(type==='glace'?30:20)+'px';
      if(type==='burger')d.textContent=n;d.onclick=()=>{placed.splice(i,1);render();};base.appendChild(d);});return;}
    if(type==='caisse'){base.innerHTML=`<div class="at-tray">${placed.map((v,i)=>`<span data-k="${i}" class="coin">${v}🪙</span>`).join('')||'<em>Pose les pièces ici</em>'}</div>`;base.querySelectorAll('[data-k]').forEach(s=>s.onclick=()=>{placed.splice(+s.dataset.k,1);render();});return;}
    placed.forEach((p,i)=>{const s=document.createElement('span');s.className='at-it';s.textContent=(ING[type].find(x=>x[1]===p.n)||['?'])[0];s.style.left=p.x+'%';s.style.top=p.y+'%';s.onclick=()=>{placed.splice(i,1);render();};base.appendChild(s);});};
  o.querySelectorAll('[data-i]').forEach(b=>b.onclick=()=>{const n=b.dataset.i;if(type==='glace'||type==='burger'){if(placed.length<10)placed.push(n);}
    else{let x,y;if(type==='pizza'){const an=Math.random()*6.283,rr=Math.sqrt(Math.random())*33;x=50+Math.cos(an)*rr;y=50+Math.sin(an)*rr;}else if(type==='gateau'){x=18+Math.random()*64;y=n==='bougie'?8+Math.random()*10:22+Math.random()*12;}else{x=22+Math.random()*56;y=8+Math.random()*30;}placed.push({n,x,y});}
    try{sndTap();}catch(e){}render();});
  o.querySelectorAll('[data-c]').forEach(b=>b.onclick=()=>{placed.push(+b.dataset.c);try{sndTap();}catch(e){}render();});
  o.querySelector('#at-clear').onclick=()=>{placed.length=0;render();};
  o.querySelector('#at-ok').onclick=()=>{
    let ok=false,why='';
    if(type==='caisse'){const s=placed.reduce((a,b)=>a+b,0),need=given-price;ok=s===need;why=s<need?`Tu rends ${s} 🪙, il manque ${need-s} 🪙.`:`Tu rends ${s} 🪙, c’est ${s-need} 🪙 de trop.`;}
    else if(type==='burger'){ok=placed.length===seq.length&&placed.every((x,i)=>x===seq[i]);why='Regarde bien l’ordre, du bas vers le haut.';}
    else{const cnt={};placed.forEach(p=>{const n=p.n||p;cnt[n]=(cnt[n]||0)+1;});const keys=new Set([...Object.keys(cnt),...Object.keys(want)]);ok=[...keys].every(k=>(cnt[k]||0)===(want[k]||0));
      const k1=[...keys].find(k=>(cnt[k]||0)!==(want[k]||0));if(k1)why=`Compte encore les ${k1}${(want[k1]||0)>1?'s':''} : il y en a ${cnt[k1]||0}, il en faut ${want[k1]||0}.`;}
    if(ok){const pay=10+lvl*5+(type==='caisse'?3:0);coins(pay);xp(10);joie(8);star();
      o.querySelector('.mp-box').innerHTML=`<h3>🎉 ${cust} est ravi !</h3><p class="mp-q">Bravo, c’est parfait ! Ton salaire : <b>${pay} 🪙</b></p><div class="mp-opts"><button class="again">🔁 Client suivant</button><button class="mp-close sec">Terminer</button></div>`;
      o.querySelector('.again').onclick=()=>{o.remove();openAtelier(type);};o.querySelector('.mp-close').onclick=()=>o.remove();}
    else{const h=o.querySelector('.at-bub');let m=o.querySelector('.at-why');if(!m){m=document.createElement('div');m.className='at-why';h.parentNode.after(m);}m.textContent='🤔 '+why;}
  };
  render();
}

// ── Album : pêche, insectes, fleurs (noms en 5 langues) ────────────────
const LANGS=[['fr','fr-FR','🇫🇷'],['en','en-GB','🇬🇧'],['es','es-ES','🇪🇸'],['de','de-DE','🇩🇪'],['it','it-IT','🇮🇹']];
const ALB={
 poissons:[['clown','🐠',['Poisson-clown','Clownfish','Pez payaso','Clownfisch','Pesce pagliaccio']],['poisson','🐟',['Poisson','Fish','Pez','Fisch','Pesce']],['globe','🐡',['Poisson-globe','Pufferfish','Pez globo','Kugelfisch','Pesce palla']],
   ['requin','🦈',['Requin','Shark','Tiburón','Hai','Squalo']],['pieuvre','🐙',['Pieuvre','Octopus','Pulpo','Oktopus','Polpo']],['crabe','🦀',['Crabe','Crab','Cangrejo','Krabbe','Granchio']],
   ['crevette','🦐',['Crevette','Shrimp','Gamba','Garnele','Gambero']],['tortue','🐢',['Tortue','Turtle','Tortuga','Schildkröte','Tartaruga']],['dauphin','🐬',['Dauphin','Dolphin','Delfín','Delfin','Delfino']],['baleine','🐳',['Baleine','Whale','Ballena','Wal','Balena']]],
 insectes:[['coccinelle','🐞',['Coccinelle','Ladybird','Mariquita','Marienkäfer','Coccinella']],['papillon','🦋',['Papillon','Butterfly','Mariposa','Schmetterling','Farfalla']],['abeille','🐝',['Abeille','Bee','Abeja','Biene','Ape']],
   ['fourmi','🐜',['Fourmi','Ant','Hormiga','Ameise','Formica']],['escargot','🐌',['Escargot','Snail','Caracol','Schnecke','Lumaca']],['scarabee','🪲',['Scarabée','Beetle','Escarabajo','Käfer','Scarabeo']],
   ['chenille','🐛',['Chenille','Caterpillar','Oruga','Raupe','Bruco']],['criquet','🦗',['Criquet','Cricket','Grillo','Grille','Grillo']]],
 fleurs:[['tulipe','🌷',['Tulipe','Tulip','Tulipán','Tulpe','Tulipano']],['rose','🌹',['Rose','Rose','Rosa','Rose','Rosa']],['tournesol','🌻',['Tournesol','Sunflower','Girasol','Sonnenblume','Girasole']],
   ['marguerite','🌼',['Marguerite','Daisy','Margarita','Gänseblümchen','Margherita']],['hibiscus','🌺',['Hibiscus','Hibiscus','Hibisco','Hibiskus','Ibisco']],['cerisier','🌸',['Fleur de cerisier','Cherry blossom','Flor de cerezo','Kirschblüte','Fiore di ciliegio']],
   ['lotus','🪷',['Lotus','Lotus','Loto','Lotus','Loto']],['trefle','🍀',['Trèfle','Clover','Trébol','Kleeblatt','Quadrifoglio']]]};
function find(cat,id){return ALB[cat].find(x=>x[0]===id);}
function gotIt(cat,item){const e=X(),k=cat+':'+item[0],first=!e.album[k];e.album[k]=(e.album[k]||0)+1;xp(first?6:2);save();
  toast(`${item[1]} ${first?'Nouveau ! ':''}${item[2][0]} (${item[2][1]})`);if(first){star();say(item[2][0]);}}
window.w3OnStep=pos=>{const w=W(),g=w.grid[A().key(pos.col,pos.row)];if(g)return;if(Math.random()<.045){const cat=Math.random()<.55?'insectes':'fleurs';gotIt(cat,pick(ALB[cat]));}};
window.w3Fish=(c,r)=>{
  const o=modal(`<h3>🎣 La pêche</h3><div class="fish-water"><div class="bob" id="bob"></div><div class="fish-msg" id="fmsg">Attends que le bouchon plonge…</div></div><div class="mp-opts"><button id="pull">🎣 Tirer !</button></div>`,'mp-fishbox');
  let state='wait',t0=0;const bob=o.querySelector('#bob'),msg=o.querySelector('#fmsg');
  const arm=setTimeout(()=>{state='bite';t0=performance.now();bob.classList.add('bite');msg.textContent='❗ Ça mord ! Vite !';try{sndTap();}catch(e){}
    setTimeout(()=>{if(state==='bite'){state='miss';bob.classList.remove('bite');msg.textContent='Oh, le poisson est parti… 🐟💨';}},950);},1500+Math.random()*2800);
  o.querySelector('#pull').onclick=()=>{if(state==='bite'){state='done';const f=Math.random()<.12?pick(ALB.poissons.slice(3)):pick(ALB.poissons.slice(0,3).concat(ALB.poissons.slice(5,8)));gotIt('poissons',f);
      msg.innerHTML=`Tu as attrapé : <b>${f[1]} ${f[2][0]}</b> !`;o.querySelector('#pull').textContent='🎣 Encore';o.querySelector('#pull').onclick=()=>{o.remove();window.w3Fish(c,r);};}
    else if(state==='wait'){clearTimeout(arm);state='miss';msg.textContent='Trop tôt ! Le poisson a eu peur 😅';o.querySelector('#pull').textContent='🎣 Réessayer';o.querySelector('#pull').onclick=()=>{o.remove();window.w3Fish(c,r);};}};
};
function photos(){try{return JSON.parse(localStorage.getItem('psa3_photos')||'[]');}catch(e){return [];}}
function openAlbum(tab){
  tab=tab||'poissons';const e=X(),tabs=[['poissons','🐠 Poissons'],['insectes','🐞 Insectes'],['fleurs','🌷 Fleurs'],['photos','📸 Photos']];
  const total=Object.values(ALB).reduce((s,a)=>s+a.length,0),found=Object.keys(e.album).length;
  const body=tab==='photos'?`<div class="alb-ph">${photos().map(p=>`<img src="${p}" alt="">`).join('')||'<p>Pas encore de photo. Appuie sur 📸 dans la ville !</p>'}</div>`:
    `<div class="alb-grid">${ALB[tab].map(it=>{const n=e.album[tab+':'+it[0]];return n?`<button data-id="${it[0]}"><span>${it[1]}</span><b>${it[2][0]}</b><small>×${n}</small></button>`:`<button class="unk"><span>❓</span><b>???</b></button>`;}).join('')}</div>
     <p class="mp-hint">${tab==='poissons'?'Touche l’eau (rivière, lac) en mode 🚶 Ma vie pour pêcher.':'Promène-toi dans l’herbe en mode 🚶 Ma vie : on trouve des petites bêtes et des fleurs !'}</p>`;
  const o=modal(`<h3>📖 Mon album <small>${found}/${total}</small></h3><div class="mp-tabs">${tabs.map(([k,l])=>`<button data-t="${k}" class="${k===tab?'on':''}">${l}</button>`).join('')}</div>${body}`,'mp-album');
  o.querySelectorAll('[data-t]').forEach(b=>b.onclick=()=>{o.remove();openAlbum(b.dataset.t);});
  o.querySelectorAll('[data-id]').forEach(b=>b.onclick=()=>{const it=find(tab,b.dataset.id);const d=modal(`<div class="alb-big">${it[1]}</div><div class="alb-names">${LANGS.map(([l,code,fl],i)=>`<button data-l="${code}" data-w="${it[2][i]}">${fl} ${it[2][i]} 🔊</button>`).join('')}</div>`);
    d.querySelectorAll('[data-l]').forEach(x=>x.onclick=()=>say(x.dataset.w,x.dataset.l));say(it[2][0]);});
}

// ── Saisons, météo, jour / nuit ─────────────────────────────────────────
const WX={day:null,kind:'sun',parts:[]};
function weather(){const d=new Date(),key=d.toISOString().slice(0,10);if(WX.day!==key){WX.day=key;let h=0;for(const ch of key)h=(h*31+ch.charCodeAt(0))%1000;const m=d.getMonth(),winter=m===11||m<=1;
  WX.kind=winter&&h%100<45?'snow':(!winter&&h%100<22)?'rain':'sun';WX.parts=[];}return WX.kind;}
window.w3Hooks.overlay.push((ctx,cv)=>{if(!cv)return;const k=weather(),w=cv.width,h=cv.height,hr=new Date().getHours(),m=new Date().getMonth();
  ctx.save();ctx.setTransform(1,0,0,1,0,0);
  if(m===11||m<=1){ctx.fillStyle='rgba(255,255,255,.10)';ctx.fillRect(0,0,w,h);}
  if(k!=='sun'){if(WX.parts.length<(k==='rain'?110:90))WX.parts.push({x:Math.random()*w,y:-10,s:k==='rain'?9+Math.random()*6:1+Math.random()*1.5,r:1+Math.random()*2.2});
    ctx.strokeStyle='rgba(180,210,255,.6)';ctx.fillStyle='rgba(255,255,255,.9)';ctx.lineWidth=1.3;
    WX.parts.forEach(p=>{p.y+=p.s;p.x+=k==='rain'?-1.5:Math.sin(p.y/30)*.6;if(p.y>h){p.y=-10;p.x=Math.random()*w;}
      if(k==='rain'){ctx.beginPath();ctx.moveTo(p.x,p.y);ctx.lineTo(p.x-3,p.y+12);ctx.stroke();}else{ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,7);ctx.fill();}});}
  const night=hr>=21||hr<6,evening=hr>=18&&hr<21,dawn=hr>=6&&hr<8;
  if(night){ctx.fillStyle='rgba(12,20,60,.42)';ctx.fillRect(0,0,w,h);}else if(evening){ctx.fillStyle='rgba(255,120,40,.13)';ctx.fillRect(0,0,w,h);}else if(dawn){ctx.fillStyle='rgba(255,190,120,.10)';ctx.fillRect(0,0,w,h);}
  ctx.restore();});

// ── Photo ──────────────────────────────────────────────────────────────
function snap(){const cv=W()&&W().canvas;if(!cv)return;let url='';try{url=cv.toDataURL('image/jpeg',.9);}catch(e){toast('Photo impossible ici 😕');return;}
  try{const im=new Image();im.onload=()=>{const sc=Math.min(1,720/im.width),c2=document.createElement('canvas');c2.width=im.width*sc;c2.height=im.height*sc;c2.getContext('2d').drawImage(im,0,0,c2.width,c2.height);
    const ph=photos();ph.unshift(c2.toDataURL('image/jpeg',.72));while(ph.length>6)ph.pop();try{localStorage.setItem('psa3_photos',JSON.stringify(ph));}catch(e){}};im.src=url;}catch(e){}
  const fl=document.createElement('div');fl.className='mp-flash';document.body.appendChild(fl);setTimeout(()=>fl.remove(),400);try{sndTap();}catch(e){}
  const o=modal(`<h3>📸 Belle photo !</h3><img class="mp-photo" src="${url}" alt=""><div class="mp-opts"><a class="mp-dl" download="ma-ville.jpg" href="${url}">💾 Enregistrer</a><button class="mp-close sec">Fermer</button></div><p class="mp-hint">Elle est aussi rangée dans 📖 Album → 📸 Photos.</p>`);
  o.querySelector('.mp-close').onclick=()=>o.remove();}

// ── Animal de compagnie ────────────────────────────────────────────────
const PET={pos:null,dir:1};
function pet(){return X().pet;}
function petDecay(){const p=pet();if(!p)return;const now=Date.now(),d=(now-(p.last||now))/60000;if(d>=1){p.faim=Math.max(0,p.faim-2*d);p.joie=Math.max(0,p.joie-1.5*d);p.last=now;}}
function openPet(){
  const p=pet();
  if(!p){const o=modal(`<h3>🐾 Adopter un compagnon</h3><div class="mp-opts big"><button data-p="chien">🐕<small>Un chien</small></button><button data-p="chat">🐈<small>Un chat</small></button></div><input class="mp-in" id="pn" maxlength="16" placeholder="Son nom (ex. Caramel)">`);
    o.querySelectorAll('[data-p]').forEach(b=>b.onclick=()=>{X().pet={type:b.dataset.p,name:(o.querySelector('#pn').value.trim()||(b.dataset.p==='chien'?'Rex':'Minou')),faim:80,joie:80,last:Date.now()};save();o.remove();star();toast('🐾 Bienvenue à '+X().pet.name+' !');openPet();});return;}
  petDecay();const em=p.type==='chien'?'🐕':'🐈';
  const o=modal(`<h3>${em} ${p.name}</h3><div class="pet-big">${em}</div>
    <div class="pet-bars"><span>🍖 Faim <i><em style="width:${Math.round(p.faim)}%"></em></i></span><span>❤️ Bonheur <i><em style="width:${Math.round(p.joie)}%;background:#f72585"></em></i></span></div>
    <div class="mp-opts"><button data-a="feed">🍖 Nourrir (2🪙)</button><button data-a="pet">🤗 Caresser</button><button data-a="walk">🦮 Jouer</button></div><p class="mp-hint">${p.name} te suit partout en mode 🚶 Ma vie !</p>`);
  o.querySelectorAll('[data-a]').forEach(b=>b.onclick=()=>{const a=b.dataset.a;if(a==='feed'){if(W().coins<2){toast('Pas assez de 🪙');return;}W().coins-=2;p.faim=Math.min(100,p.faim+35);}
    if(a==='pet'){p.joie=Math.min(100,p.joie+15);joie(5);}if(a==='walk'){p.joie=Math.min(100,p.joie+25);p.faim=Math.max(0,p.faim-5);joie(8);}
    p.last=Date.now();save();star();o.remove();openPet();});
}
function avatarCR(){const L=W().life;if(!L)return null;let c=L.pos.col,r=L.pos.row;if(L.path&&L.path.length&&L.t>0){c+=(L.path[0].col-L.pos.col)*L.t;r+=(L.path[0].row-L.pos.row)*L.t;}return {c,r};}
function homeCR(){const w=W(),k=Object.keys(w.grid).find(x=>w.grid[x].home);if(!k)return null;const [c,r]=k.split(',').map(Number);return {c:c+.5,r:r+1.2};}
function drawEmoji(ctx,x,y,em,size,flip){ctx.save();ctx.translate(x,y);if(flip)ctx.scale(-1,1);ctx.font=size+'px serif';ctx.textAlign='center';ctx.textBaseline='bottom';ctx.fillStyle='#000';ctx.fillText(em,0,0);ctx.restore();}
window.w3Hooks.draw.push(ctx=>{const p=pet();if(!p)return;petDecay();const w=W();
  const tgt=w.mode==='life'?avatarCR():homeCR();if(!tgt)return;
  if(!PET.pos)PET.pos={c:tgt.c+.6,r:tgt.r+.6};const dx=tgt.c+.55-PET.pos.c,dy=tgt.r+.55-PET.pos.r,d=Math.hypot(dx,dy);
  if(d>.25){const sp=Math.min(.06,d*.05);PET.pos.c+=dx/d*sp;PET.pos.r+=dy/d*sp;PET.dir=(dx-dy)>0?1:-1;}
  const q=A().toIso(PET.pos.c,PET.pos.r),hop=d>.3?Math.abs(Math.sin(w.t*.35))*3:0;
  ctx.fillStyle='rgba(0,0,0,.2)';ctx.beginPath();ctx.ellipse(q.x,q.y+16,7,3,0,0,7);ctx.fill();
  drawEmoji(ctx,q.x,q.y+17-hop,p.type==='chien'?'🐕':'🐈',17,PET.dir>0);
  if(p.faim<30){ctx.fillStyle='#fff';ctx.beginPath();ctx.roundRect(q.x+4,q.y-14,18,16,6);ctx.fill();ctx.font='11px serif';ctx.textBaseline='middle';ctx.fillText('🦴',q.x+13,q.y-6);}});

// ── Famille (5 personnes maximum) ──────────────────────────────────────
const ROLES=['Papa','Maman','Frère','Sœur','Papi','Mamie','Bébé','Ami(e)'];
const FAM=[];const FIMG={};
function famImg(av){if(!FIMG[av]){const i=new Image();i.onload=()=>{i.ok=1;};try{const a=(window.PNG_AVATARS||[]).find(x=>x.id===av);if(a)i.src=_GH+a.f;}catch(e){}FIMG[av]=i;}return FIMG[av];}
function openFamily(){
  const e=X();let role=ROLES[0],av=null;
  const avs=(window.PNG_AVATARS||[]).slice(0,40);
  const o=modal(`<h3>👨‍👩‍👧 Ma famille <small>${e.family.length}/5</small></h3>
    <div class="fam-list">${e.family.map((m,i)=>`<div><b>${m.name}</b> <small>${m.role}</small><button data-del="${i}">✖</button></div>`).join('')||'<p>Personne pour l’instant. Ajoute ta famille : elle vivra dans ta ville !</p>'}</div>
    ${e.family.length<5?`<div class="fam-add"><b>Ajouter :</b><div class="fam-roles">${ROLES.map(r=>`<button data-r="${r}" class="${r===role?'on':''}">${r}</button>`).join('')}</div>
      <input class="mp-in" id="fname" maxlength="16" placeholder="Prénom">
      <div class="fam-avs">${avs.map(a=>`<button data-av="${a.id}"><img src="${_GH+a.f}" alt="" loading="lazy" onerror="this.replaceWith(document.createTextNode('🙂'))"></button>`).join('')}</div>
      <button id="fadd" class="mp-main">➕ Ajouter à ma famille</button></div>`:''}`,'mp-fam');
  o.querySelectorAll('[data-del]').forEach(b=>b.onclick=()=>{e.family.splice(+b.dataset.del,1);FAM.length=0;save();o.remove();openFamily();});
  o.querySelectorAll('[data-r]').forEach(b=>b.onclick=()=>{role=b.dataset.r;o.querySelectorAll('[data-r]').forEach(x=>x.classList.toggle('on',x===b));});
  o.querySelectorAll('[data-av]').forEach(b=>b.onclick=()=>{av=b.dataset.av;o.querySelectorAll('[data-av]').forEach(x=>x.classList.toggle('on',x===b));});
  const add=o.querySelector('#fadd');if(add)add.onclick=()=>{if(!av){toast('Choisis une image 🙂');return;}const n=o.querySelector('#fname').value.trim()||role;e.family.push({role,name:n,av});FAM.length=0;save();star();o.remove();openFamily();};
}
function famSpawn(){const e=X();if(FAM.length===e.family.length)return;FAM.length=0;const base=homeCR()||avatarCR()||{c:10,r:10};
  e.family.forEach((m,i)=>FAM.push({m,pos:{col:Math.round(base.c)+(i%3)-1,row:Math.round(base.r)+1+(i>2?1:0)},path:[],t:0,idle:60+i*40,dir:1}));}
window.w3Hooks.draw.push(ctx=>{const e=X();if(!e.family.length)return;famSpawn();const w=W(),api=A();
  FAM.forEach(f=>{if(f.path.length){f.t+=.03;if(f.t>=1){f.t=0;f.pos=f.path.shift();}}else if(--f.idle<=0){f.idle=200+rnd(300);const h=homeCR()||{c:f.pos.col,r:f.pos.row};
      for(let k=0;k<8;k++){const tc=Math.round(h.c)+rnd(13)-6,tr=Math.round(h.r)+rnd(13)-6;try{if(api.walk(tc,tr)){const p=api.path({col:f.pos.col,row:f.pos.row},{col:tc,row:tr});if(p&&p.length&&p.length<30){f.path=p;break;}}}catch(err){}}}
    let c=f.pos.col,r=f.pos.row;if(f.path.length&&f.t>0){c+=(f.path[0].col-f.pos.col)*f.t;r+=(f.path[0].row-f.pos.row)*f.t;f.dir=((f.path[0].col-f.pos.col)-(f.path[0].row-f.pos.row))>0?1:-1;}
    const q=api.toIso(c+.5,r+.5),im=famImg(f.m.av),h=f.m.role==='Bébé'?26:38,bob=f.path.length?Math.abs(Math.sin(w.t*.3))*2:0;
    ctx.fillStyle='rgba(0,0,0,.22)';ctx.beginPath();ctx.ellipse(q.x,q.y,8,3.5,0,0,7);ctx.fill();
    if(im.ok){const ww=h*im.width/im.height;ctx.save();ctx.translate(q.x,q.y-bob);if(f.dir<0)ctx.scale(-1,1);ctx.drawImage(im,-ww/2,-h,ww,h);ctx.restore();}
    else drawEmoji(ctx,q.x,q.y-bob,{Papa:'👨',Maman:'👩',Frère:'👦',Sœur:'👧',Papi:'👴',Mamie:'👵',Bébé:'👶'}[f.m.role]||'🧑',22,f.dir<0);
    ctx.font='bold 8px sans-serif';ctx.textAlign='center';ctx.textBaseline='top';ctx.lineWidth=2.5;ctx.strokeStyle='rgba(0,0,0,.6)';ctx.strokeText(f.m.name,q.x,q.y+3);ctx.fillStyle='#fff';ctx.fillText(f.m.name,q.x,q.y+3);});});
window.w3TapPeople=(c,r)=>{const hit=FAM.find(f=>Math.abs(f.pos.col-c)<=0&&Math.abs(f.pos.row-r)<=0);
  if(hit){const m=hit.m;const o=modal(`<h3>${m.name} <small>${m.role}</small></h3><div class="mp-opts"><button data-a="hug">🤗 Faire un câlin</button><button data-a="hi">👋 Dire bonjour</button><button data-a="help">🧹 L’aider (+5🪙)</button></div>`);
    o.querySelectorAll('[data-a]').forEach(b=>b.onclick=()=>{const a=b.dataset.a;if(a==='hug'){joie(12);toast('❤️ Un gros câlin avec '+m.name+' !');}if(a==='hi'){say('Bonjour '+m.name+' !');joie(4);}if(a==='help'){coins(5);joie(6);toast('🧹 Merci de m’avoir aidé ! +5🪙');}star();o.remove();});return true;}
  if(pet()&&PET.pos&&Math.round(PET.pos.c-.5)===c&&Math.round(PET.pos.r-.5)===r){openPet();return true;}
  return false;};

// ── Niveaux (prêts, désactivés) ─────────────────────────────────────────
function level(x){return Math.floor(Math.sqrt((x||0)/40))+1;}
window.w3Level=()=>({on:LEVELS_ON,xp:X().xp,level:level(X().xp),next:Math.pow(level(X().xp),2)*40});

// ── Barre de boutons sur la carte ──────────────────────────────────────
function rail(){const wrap=document.getElementById('world3-wrap');if(!wrap)return;let r=document.getElementById('mp-rail');
  if(!r){r=document.createElement('div');r.id='mp-rail';wrap.appendChild(r);}
  const e=X(),ready=orders().some(canDeliver),lv=window.w3Level();
  r.innerHTML=(LEVELS_ON?`<div class="mp-lvl">Niv. ${lv.level}</div>`:'')+
   `<button data-r="orders" title="Commandes">📋${ready?'<i></i>':''}</button><button data-r="album" title="Album">📖</button><button data-r="family" title="Famille">👨‍👩‍👧</button><button data-r="pet" title="Animal">${e.pet?(e.pet.type==='chien'?'🐕':'🐈'):'🐾'}</button><button data-r="photo" title="Photo">📸</button>`;
  r.querySelectorAll('[data-r]').forEach(b=>b.onclick=ev=>{ev.stopPropagation();const k=b.dataset.r;if(k==='orders')openOrders();if(k==='album')openAlbum();if(k==='family')openFamily();if(k==='pet')openPet();if(k==='photo')snap();});}
let railT=0;window.w3Hooks.draw.push(()=>{if(++railT%90===1||!document.getElementById('mp-rail'))rail();});
window.__plus={openOrders,openAlbum,openFamily,openPet,openAtelier,snap,X};
})();
