// ═══ Illustrations animées des exercices de sport (assets/sport/<ID>-<n>.webp, data/sport_illus.json) ═══
(function(){
  const V=((document.currentScript&&document.currentScript.src.match(/[?&]v=(\d+)/))||[])[1]||'';
  let IX=null,timer=null;
  fetch('data/sport_illus.json?v='+V).then(r=>r.ok?r.json():{}).then(j=>{IX=j||{};}).catch(()=>{IX={};});
  window.sportIllusN=id=>(IX&&IX[id])||0;
  window.sportIllusStop=()=>{if(timer){clearInterval(timer);timer=null;}};
  // Remplit el avec les étapes animées en fondu ; renvoie true si une illustration existe.
  window.sportIllus=function(el,id,pas){
    sportIllusStop();const n=sportIllusN(id);if(!el||!n)return false;
    el.innerHTML='';el.classList.add('df-ill');
    const imgs=[];for(let i=1;i<=n;i++){const im=new Image();im.src=`assets/sport/${id}-${i}.webp?v=${V}`;im.alt='';im.className=i===1?'on':'';el.appendChild(im);imgs.push(im);}
    if(n>1){const dots=document.createElement('div');dots.className='df-ill-dots';dots.innerHTML=imgs.map((_,i)=>`<i class="${i?'':'on'}"></i>`).join('');el.appendChild(dots);
      let k=0;const reduit=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
      timer=setInterval(()=>{if(!document.body.contains(el)){sportIllusStop();return;}imgs[k].className='';dots.children[k].className='';k=(k+1)%n;imgs[k].className='on';dots.children[k].className='on';},(pas||1600)*(reduit?2:1));}
    return true;
  };
})();
