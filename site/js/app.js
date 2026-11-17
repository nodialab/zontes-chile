var B=document.documentElement.dataset.base||'';
(()=>{
const $=(s,r=document)=>r.querySelector(s),$$=(s,r=document)=>[...r.querySelectorAll(s)];
const rm=matchMedia('(prefers-reduced-motion:reduce)').matches;

/* ---- menú móvil ---- */
const burger=$('#burger'),nav=$('#nav'),scrim=$('#scrim');
function menu(open){burger.setAttribute('aria-expanded',open);burger.setAttribute('aria-label',open?'Cerrar menú':'Abrir menú');nav.classList.toggle('is-open',open);scrim.hidden=!open;document.body.style.overflow=open?'hidden':''}
burger?.addEventListener('click',()=>menu(burger.getAttribute('aria-expanded')!=='true'));
scrim?.addEventListener('click',()=>menu(false));
nav?.addEventListener('click',e=>{if(e.target.closest('a'))menu(false)});
addEventListener('keydown',e=>{if(e.key==='Escape')menu(false)});
matchMedia('(min-width:1121px)').addEventListener('change',e=>{if(e.matches)menu(false)});

/* ---- doble buffer de imagen (sin saltos) ---- */
function Buffer(a,b){let cur=a,nxt=b;
 return{set(url,alt){if(cur.getAttribute('src')===url)return;nxt.src=url;nxt.alt=alt||'';(nxt.decode?nxt.decode():Promise.resolve()).catch(()=>{}).then(()=>{nxt.classList.add('is-on');cur.classList.remove('is-on');[cur,nxt]=[nxt,cur]})},
 raw(url){cur.src=url}}}

/* ---- visor de moto: 360° o color estático ---- */
const st=$('#stage');
if(st&&window.MODEL){
 const M=window.MODEL,slug=st.dataset.slug,N=M.frames,imgs=$$('.stage__img',st),buf=Buffer(imgs[0],imgs[1]);
 let color=M.colors[0],frame=color.start||0,cache={};
 const url=(c,i)=>`${B}/img/${slug}/360/${c}/${String(((i%N)+N)%N).padStart(2,'0')}.webp`;
 const preload=c=>{if(!N||cache[c])return;cache[c]=[...Array(N)].map((_,i)=>{const im=new Image();im.src=url(c,i);return im})};
 const name=$('#color-name');
 function setColor(c){color=M.colors.find(x=>x.id===c);frame=color.start||0;name.textContent=color.name;
  $$('.sw').forEach(s=>s.setAttribute('aria-pressed',s.dataset.color===c));
  buf.set(N?url(c,frame):`${B}/img/${slug}/stage/${c}.webp`,`${M.name} color ${color.name}`);
  if(N)preload(c)}
 $$('.sw').forEach(s=>s.addEventListener('click',()=>setColor(s.dataset.color)));
 if(N){
  const hint=$('.stage__hint',st);let drag=null,fl=frame;
  const go=f=>{fl=f;const i=Math.round(f);if(i!==frame){frame=i;buf.raw(url(color.id,i))}};
  const idle=window.requestIdleCallback||(f=>setTimeout(f,600));idle(()=>preload(color.id));
  st.addEventListener('pointerdown',e=>{drag={x:e.clientX,f:fl};st.setPointerCapture(e.pointerId);preload(color.id);hint?.classList.add('is-gone')});
  st.addEventListener('pointermove',e=>{if(!drag)return;go(drag.f-(e.clientX-drag.x)/st.clientWidth*N*1.1)});
  const end=()=>{drag=null};st.addEventListener('pointerup',end);st.addEventListener('pointercancel',end);
  st.addEventListener('keydown',e=>{if(e.key==='ArrowLeft'){go(fl+1);e.preventDefault()}if(e.key==='ArrowRight'){go(fl-1);e.preventDefault()}hint?.classList.add('is-gone')});
  st.addEventListener('dragstart',e=>e.preventDefault());
 }
}

/* ---- inicio: modelo destacado ---- */
const hs=$('#home-stage');
if(hs&&window.HOME){
 const imgs=$$('.stage__img',hs),buf=Buffer(imgs[0],imgs[1]),hero=$('#hero'),cap=$('#home-cap');
 let cd=null,slug0=null,frame=0,fl=0,cache={},drag=null;
 const fu=i=>{const N=cd.frames;return B+'/img/'+slug0+'/360/'+cd.cid+'/'+String(((i%N)+N)%N).padStart(2,'0')+'.webp'};
 const pre=()=>{if(!cd.frames||cache[slug0])return;cache[slug0]=[...Array(cd.frames)].map((_,i)=>{const im=new Image();im.src=fu(i);return im})};
 const show=b=>{const d=window.HOME[b.dataset.home],p=d.pal;cd=d;slug0=b.dataset.home;frame=fl=d.start||0;drag=null;
  $$('[data-home]').forEach(x=>x.setAttribute('aria-pressed',x===b));
  buf.set(B+d.img,'Zontes '+d.name);
  for(const[k,v]of Object.entries({panel:p.panel,ink:p.ink,acc:p.acc,ill1:p.ill1,ill2:p.ill2,ill3:p.ill3}))hero.style.setProperty('--'+k,v);
  cap.innerHTML=`<strong>${d.name}</strong> · ${d.tag} — <a href="${B}/modelos/${b.dataset.home}/">ver modelo</a>${d.v360?` <span class="badge360 badge360--in">360° · arrastra la moto para girar</span>`:''}`};
 hs.addEventListener('pointerdown',e=>{if(!cd||!cd.frames)return;drag={x:e.clientX,f:fl};stop();hs.setPointerCapture(e.pointerId);pre()});
 hs.addEventListener('pointermove',e=>{if(!drag)return;fl=drag.f-(e.clientX-drag.x)/hs.clientWidth*cd.frames*1.1;const i=Math.round(fl);if(i!==frame){frame=i;buf.raw(fu(i))}});
 const dend=()=>{drag=null};hs.addEventListener('pointerup',dend);hs.addEventListener('pointercancel',dend);hs.addEventListener('dragstart',e=>e.preventDefault());
 hs.addEventListener('pointerenter',()=>{if(cd&&cd.frames)pre()});
 const chips=$$('[data-home]');let auto=null,idx=Math.max(0,chips.findIndex(x=>x.getAttribute('aria-pressed')==='true'));
 const stop=()=>{if(auto){clearInterval(auto);auto=null}};
 cd=window.HOME[chips[idx].dataset.home];slug0=chips[idx].dataset.home;frame=fl=cd.start||0;
 chips.forEach((b,i)=>b.addEventListener('click',()=>{stop();idx=i;show(b)}));
 if(!rm){const go=()=>{idx=(idx+1)%chips.length;show(chips[idx])};
  let hold=false;const zone=hs.closest('.hero__moto');
  zone.addEventListener('pointerenter',()=>hold=true);zone.addEventListener('pointerleave',()=>hold=false);
  zone.addEventListener('focusin',()=>hold=true);zone.addEventListener('focusout',()=>hold=false);
  auto=setInterval(()=>{if(!hold&&!document.hidden)go()},4500)}
}

/* ---- pestañas accesibles ---- */
function tabs(list,onSel){const t=$$('[role=tab]',list);
 const sel=x=>{t.forEach(y=>{const on=y===x;y.setAttribute('aria-selected',on);y.tabIndex=on?0:-1;const p=document.getElementById(y.getAttribute('aria-controls'));if(p&&t.every(z=>z.getAttribute('aria-controls')!==p.id||z===y||true)&&!onSel)p.hidden=!on});onSel&&onSel(x)};
 t.forEach((x,i)=>{x.addEventListener('click',()=>sel(x));x.addEventListener('keydown',e=>{let n=null;if(e.key==='ArrowRight')n=t[(i+1)%t.length];if(e.key==='ArrowLeft')n=t[(i-1+t.length)%t.length];if(e.key==='Home')n=t[0];if(e.key==='End')n=t[t.length-1];if(n){e.preventDefault();n.focus();sel(n)}})});
 return sel}
const gtabs=$('.tabs[aria-label=Galería]');
if(gtabs)tabs(gtabs);

/* ---- carrusel ---- */
const car=$('#car');
if(car){const slides=$$('.slide',car),dots=$('#dots');let cur=0;
 slides.forEach((s,i)=>{const b=document.createElement('button');b.setAttribute('aria-label','Foto '+(i+1));b.onclick=()=>slides[i].scrollIntoView({behavior:rm?'auto':'smooth',inline:'center',block:'nearest'});dots.append(b)});
 const upd=i=>{cur=i;$$('button',dots).forEach((b,j)=>b.toggleAttribute('aria-current',j===i))};
 new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting)upd(slides.indexOf(e.target))}),{root:car,threshold:.6}).observe&&slides.forEach(s=>new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting)upd(slides.indexOf(e.target))}),{root:car,threshold:.6}).observe(s));
 upd(0);
 $$('[data-car]').forEach(b=>b.addEventListener('click',()=>{const n=Math.max(0,Math.min(slides.length-1,cur+ +b.dataset.car));slides[n].scrollIntoView({behavior:rm?'auto':'smooth',inline:'center',block:'nearest'})}));
 car.addEventListener('keydown',e=>{if(e.key==='ArrowRight')$('[data-car="1"]').click();if(e.key==='ArrowLeft')$('[data-car="-1"]').click()});
}

/* ---- lightbox (<dialog> nativo: foco atrapado y Esc) ---- */
if(window.MODEL){
 const M=window.MODEL,dlg=document.createElement('dialog');dlg.className='lb';dlg.setAttribute('aria-label','Visor de fotos');
 dlg.innerHTML='<button class="iconbtn lb__x" aria-label="Cerrar">✕</button><img alt=""><div class="lb__bar"><button class="iconbtn" data-d="-1" aria-label="Anterior">←</button><span class="lb__n"></span><button class="iconbtn" data-d="1" aria-label="Siguiente">→</button></div>';
 document.body.append(dlg);let list=[],i=0,opener=null;
 const show=()=>{const it=list[i];$('img',dlg).src=`${B}/img/${M.slug||(location.pathname.match(/modelos\/([^/]+)/)||[])[1]}/g/${it}.webp`;$('img',dlg).alt=M.name+' '+(i+1);$('.lb__n',dlg).textContent=`${i+1} / ${list.length}`};
 const slug=(location.pathname.match(/modelos\/([^/]+)/)||[])[1];M.slug=slug;
 const open=(l,n,el)=>{list=l;i=n;opener=el;show();dlg.showModal()};
 const step=d=>{i=(i+d+list.length)%list.length;show()};
 document.addEventListener('click',e=>{const b=e.target.closest('[data-lb]');if(!b)return;
  if(b.classList.contains('slide__b'))open(M.carousel,+b.dataset.i,b);
  else{const l=M[b.dataset.tab];open(l,l.indexOf(b.dataset.id),b)}});
 dlg.addEventListener('click',e=>{if(e.target.closest('.lb__x')||e.target===dlg)dlg.close();const d=e.target.closest('[data-d]');if(d)step(+d.dataset.d)});
 dlg.addEventListener('keydown',e=>{if(e.key==='ArrowRight')step(1);if(e.key==='ArrowLeft')step(-1)});
 dlg.addEventListener('close',()=>opener?.focus());
 let sx=null;dlg.addEventListener('touchstart',e=>sx=e.touches[0].clientX,{passive:true});dlg.addEventListener('touchend',e=>{if(sx===null)return;const dx=e.changedTouches[0].clientX-sx;if(Math.abs(dx)>50)step(dx<0?1:-1);sx=null});
}

/* ---- cotización: el botón fija SIEMPRE el modelo ---- */
const sel=$('#quote-model');
function fix(slug){if(!sel||!slug)return;sel.value=slug;sel.dispatchEvent(new Event('change'));const q=$('#cotizar');q?.scrollIntoView({behavior:rm?'auto':'smooth',block:'start'});setTimeout(()=>$('#quote-form input')?.focus({preventScroll:true}),400)}
document.addEventListener('click',e=>{const b=e.target.closest('[data-cotizar]');if(!b||!sel)return;e.preventDefault();fix(b.dataset.cotizar);history.replaceState(null,'','#cotizar')});
if(window.MODEL){const c=$('.nav__cta');if(c){c.href='#cotizar';c.dataset.cotizar=(location.pathname.match(/modelos\/([^/]+)/)||[])[1]}}
if(sel&&/cotizar=1/.test(location.search)){const f=$('#quote-form').dataset.fixed;if(f)fix(f)}
const form=$('#quote-form');
form?.addEventListener('submit',e=>{e.preventDefault();const st=$('#quote-status');let ok=true;
 $$('[required]',form).forEach(f=>{const bad=!f.value.trim()||(f.type==='email'&&!/^\S+@\S+\.\S+$/.test(f.value));f.setAttribute('aria-invalid',bad);if(bad)ok=false});
 if(!ok){st.className='form__note err';st.textContent='Revisa los campos marcados.';$('[aria-invalid=true]',form).focus();return}
 const d=Object.fromEntries(new FormData(form)),mod=sel.options[sel.selectedIndex].text;
 const body=`Modelo: ${mod}\nNombre: ${d.nombre}\nCorreo: ${d.correo}\nTeléfono: ${d.telefono}\nRegión: ${d.region}\n\n${d.mensaje||''}`;
 st.className='form__note ok';st.textContent='Abriendo tu correo con la solicitud lista para enviar a contacto@imoto.cl…';
 location.href=`mailto:contacto@imoto.cl?subject=${encodeURIComponent('Cotización '+mod)}&body=${encodeURIComponent(body)}`});

/* ---- comparador ---- */
const cmp=$('#cmp');
if(cmp&&window.CMP){const sels=$$('[data-cmp]');
 const draw=()=>{const ch=sels.map(s=>window.CMP.find(m=>m.slug===s.value)).filter(Boolean);
  if(!ch.length){cmp.innerHTML='<tbody><tr><td>Elige al menos un modelo.</td></tr></tbody>';return}
  cmp.innerHTML=`<thead><tr><th></th>${ch.map(m=>`<th scope="col">${m.name}</th>`).join('')}</tr></thead><tbody>${ch[0].rows.map((r,k)=>`<tr><th scope="row">${r[0]}</th>${ch.map(m=>`<td>${m.rows[k][1]}</td>`).join('')}</tr>`).join('')}</tbody>`};
 sels.forEach((s,i)=>{if(i===0)s.value=window.CMP[0].slug;if(i===1)s.value=window.CMP[2].slug;s.addEventListener('change',draw)});draw()}

/* ---- distribuidores ---- */
const list=$('#p-list');
if(list&&window.DEAL){const D=window.DEAL,rg=$('#f-region'),q=$('#f-q'),cnt=$('#f-count'),zones=$('#zones');
 const Z={Norte:['Antofagasta','Atacama','Coquimbo'],Centro:['Valparaíso','Metropolitana','O’Higgins','Maule']};
 const zoneOf=r=>Z.Norte.includes(r)?'Norte':Z.Centro.includes(r)?'Centro':'Sur';
 let mode='dealers',zone='';const norm=s=>s.normalize('NFD').replace(/[̀-ͯ]/g,'').toLowerCase();
 const esc=s=>s.replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
 const mail=m=>m.split(' / ').map(x=>/^www\./.test(x)?`<a href="https://${x}" rel="noopener">${x}</a>`:`<a href="mailto:${x}">${esc(x)}</a>`).join(' · ');
 const draw=()=>{const src=D[mode==='dealers'?'dealers':'service'],t=norm(q.value);
  const r=src.filter(d=>(!rg.value||d.region===rg.value)&&(!zone||zoneOf(d.region)===zone)&&(!t||norm(d.comuna+' '+d.nombre).includes(t)));
  cnt.textContent=`${r.length} ${r.length===1?'resultado':'resultados'}${rg.value?' en '+rg.value:''}`;
  list.innerHTML=r.map(d=>`<article class="dcard"><span class="chip">${d.region}</span><h3>${esc(d.nombre)}</h3><p class="ir"><svg class="ic ic--s" viewBox="0 0 24 24" aria-hidden="true"><use href="#i-pin"/></svg><span><strong>${esc(d.comuna)}</strong>${d.dir?' · '+esc(d.dir):''}</span></p>${d.tel?`<p class="ir"><svg class="ic ic--s" viewBox="0 0 24 24" aria-hidden="true"><use href="#i-phone"/></svg><span>Tel. ${esc(d.tel)}</span></p>`:''}${d.cel?`<p class="ir"><svg class="ic ic--s" viewBox="0 0 24 24" aria-hidden="true"><use href="#i-chat"/></svg><span>Cel. ${esc(d.cel)}</span></p>`:''}${d.mail?`<p class="ir"><svg class="ic ic--s" viewBox="0 0 24 24" aria-hidden="true"><use href="#i-mail"/></svg><span>${mail(d.mail)}</span></p>`:''}</article>`).join('')||'<p class="muted">No hay puntos con ese filtro. Prueba otra región o limpia la búsqueda.</p>'};
 const tab=tabs($('.tabs'),x=>{mode=x.id==='t-svc'?'service':'dealers';draw()});
 rg.addEventListener('change',draw);q.addEventListener('input',draw);
 zones.addEventListener('click',e=>{const b=e.target.closest('[data-zone]');if(!b)return;zone=b.dataset.zone;$$('[data-zone]',zones).forEach(x=>x.setAttribute('aria-pressed',x===b));if(zone&&rg.value&&zoneOf(rg.value)!==zone)rg.value='';draw()});
 $('#f-reset').addEventListener('click',()=>{rg.value='';q.value='';zone='';$$('[data-zone]',zones).forEach(x=>x.setAttribute('aria-pressed',!x.dataset.zone));draw()});
 const p=new URLSearchParams(location.search).get('region');if(p&&D.regions.includes(p))rg.value=p;
 if(location.hash==='#servicio')$('#t-svc').click();else draw();
}
})();

/* ---- videos: carga el reproductor solo al pulsar ---- */
document.querySelectorAll('.vid__btn').forEach(b=>b.addEventListener('click',()=>{const f=document.createElement('iframe');f.src='https://www.youtube-nocookie.com/embed/'+b.dataset.yt+'?autoplay=1&rel=0'+(+b.dataset.t?'&start='+b.dataset.t:'');f.title=b.getAttribute('aria-label').replace('Reproducir video: ','');f.allow='autoplay; encrypted-media; picture-in-picture; fullscreen';f.allowFullscreen=true;f.className='vid__fr';b.replaceWith(f)}));
