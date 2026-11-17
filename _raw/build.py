import os,json,shutil,html,re,sys
sys.path.insert(0,os.path.dirname(__file__))
from data import *
R='/Users/ansokbeatz/Documents/AI Projects/Zontes/'
S=R+'site/'
MEDIA=json.load(open(R+'data/media.json'))
E=html.escape
BYSLUG={m['slug']:m for m in M}
ORDER=['zt368t-e','zt368t-g','zt703-rr','zt703-f','zt350-gk','zt350-t2','zt200-z2','zt350t-e','zt350t-m','zt200-g1','zt200-u1']
M=[BYSLUG[s] for s in ORDER]

def w(path,content):
    p=S+path; os.makedirs(os.path.dirname(p),exist_ok=True); open(p,'w').write(content)

# ---------- ilustraciones de fondo (sin motos), por categoría ----------
def ill(kind):
    a='<svg class="ill" viewBox="0 0 1600 900" preserveAspectRatio="xMidYMid slice" aria-hidden="true" focusable="false">'
    sky='<rect width="1600" height="900" fill="var(--l1)"/>'
    if kind=='sport':  # pista: pianos y líneas de velocidad
        b=sky+'<path d="M0 640 L1600 520 L1600 900 L0 900Z" fill="var(--l2)"/>'
        b+='<path d="M0 640 L1600 520 L1600 548 L0 672Z" fill="var(--l3)" opacity=".55"/>'
        for i in range(22):
            x=i*80; col='var(--l3)' if i%2==0 else '#ffffff'
            b+=f'<path d="M{x} {640-i*5.5:.0f} l80 -6 l0 28 l-80 6Z" fill="{col}" opacity=".35"/>'
        for i in range(9):
            y=120+i*70; b+=f'<rect x="{(i*173)%900+500}" y="{y}" width="{260+(i*61)%240}" height="3" rx="2" fill="#fff" opacity=".12"/>'
        b+='<circle cx="1280" cy="260" r="150" fill="var(--l3)" opacity=".25"/>'
    elif kind in('adv','adv2','adv3'): # montañas
        b=sky+'<circle cx="1180" cy="250" r="120" fill="var(--l3)" opacity=".45"/>'
        b+='<path d="M0 620 L240 380 L420 540 L640 300 L900 600 L1120 420 L1380 620 L1600 480 L1600 900 L0 900Z" fill="var(--l2)"/>'
        b+='<path d="M0 720 L300 520 L560 700 L820 500 L1100 720 L1360 560 L1600 700 L1600 900 L0 900Z" fill="var(--l3)" opacity=".55"/>'
        b+='<path d="M0 800 L400 700 L800 790 L1200 690 L1600 780 L1600 900 L0 900Z" fill="#000" opacity=".28"/>'
    elif kind=='scooter': # ciudad
        b=sky+'<rect y="520" width="1600" height="380" fill="var(--l2)"/>'
        import random; random.seed(7); x=0
        while x<1600:
            bw=random.randint(70,150); bh=random.randint(160,420)
            b+=f'<rect x="{x}" y="{560-bh}" width="{bw}" height="{bh+40}" fill="var(--l3)" opacity=".45"/>'
            for yy in range(560-bh+18,540,34):
                for xx in range(x+12,x+bw-14,26):
                    if random.random()>.55: b+=f'<rect x="{xx}" y="{yy}" width="10" height="14" fill="#fff" opacity=".22"/>'
            x+=bw+random.randint(6,24)
        b+='<rect y="720" width="1600" height="180" fill="#000" opacity=".3"/>'+''.join(f'<rect x="{i*190+30}" y="800" width="100" height="8" rx="4" fill="#fff" opacity=".18"/>' for i in range(9))
    elif kind in('street','street2'): # sol + calle + ladrillo
        b=sky+'<circle cx="1220" cy="430" r="230" fill="var(--l3)" opacity=".55"/><circle cx="1220" cy="430" r="150" fill="var(--l2)" opacity=".8"/>'
        b+='<rect y="610" width="1600" height="290" fill="var(--l2)"/>'
        for i in range(0,1600,64):
            for j in range(0,4):
                b+=f'<rect x="{i+(32 if j%2 else 0)}" y="{610+j*8}" width="0" height="0"/>'
        b+=''.join(f'<path d="M{i*140-60} 900 L{i*140+40} 610 L{i*140+54} 610 L{i*140-30} 900Z" fill="#fff" opacity=".07"/>' for i in range(14))
    else: # trail: dunas
        b=sky+'<circle cx="1100" cy="240" r="110" fill="var(--l3)" opacity=".5"/>'
        b+='<path d="M0 640 Q260 480 560 600 T1100 560 T1600 600 L1600 900 L0 900Z" fill="var(--l2)"/>'
        b+='<path d="M0 760 Q300 640 640 740 T1200 700 T1600 740 L1600 900 L0 900Z" fill="var(--l3)" opacity=".5"/>'
        b+=''.join(f'<circle cx="{(i*227)%1500+40}" cy="{(i*131)%260+640}" r="{3+i%4}" fill="#fff" opacity=".14"/>' for i in range(40))
    return a+b+'</svg>'

ICON_WA='<svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm5.8 14.2c-.2.7-1.4 1.3-2 1.4-.5.1-1.2.1-3.7-.9-3-1.3-4.9-4.3-5-4.5-.1-.2-1.2-1.6-1.2-3s.8-2.1 1-2.4c.3-.3.6-.3.8-.3h.6c.2 0 .5-.1.7.5l1 2.3c.1.2.1.4 0 .6l-.4.6-.4.5c-.1.2-.3.3-.1.6.2.3.8 1.3 1.7 2.1 1.1 1 2 1.3 2.3 1.4.3.1.5.1.6-.1l.9-1.1c.2-.3.4-.2.6-.1l2 1c.3.1.5.2.5.4.1.2.1.8-.2 1.5Z"/></svg>'
ARROW='<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'

def head(title,desc,path='/',extra_style='',body_cls=''):
    return f'''<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title)}</title><meta name="description" content="{E(desc)}">
<meta name="theme-color" content="#f4f3ee">
<link rel="icon" href="/img/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:ital,wght@0,600;0,700;0,800;1,700;1,800&family=Barlow:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/css/style.css">
<style>{extra_style}</style></head>
<body class="{body_cls}"><a class="skip" href="#main">Saltar al contenido</a>'''

NAV=[('/','Inicio'),('/modelos/','Modelos'),('/distribuidores/','Distribuidores'),('/mantenciones/','Mantenciones'),('/nosotros/','Nosotros'),('/contacto/','Contacto')]
def header(cur):
    items=''.join(f'<li><a href="{h}"{" aria-current=\"page\"" if h==cur or (h!="/" and cur.startswith(h)) else ""}>{n}</a></li>' for h,n in NAV)
    return f'''<header class="hdr" id="top"><div class="wrap hdr__in">
<a class="logo" href="/" aria-label="Zontes Chile, inicio"><img src="/img/logo-zontes.png" width="147" height="26" alt="Zontes"><em>Chile</em></a>
<nav class="nav" id="nav" aria-label="Principal"><ul>{items}</ul>
<a class="btn btn--acc nav__cta" href="/modelos/#cotizar-rapido">Cotizar</a></nav>
<button class="burger" id="burger" aria-expanded="false" aria-controls="nav" aria-label="Abrir menú"><span></span><span></span><span></span></button>
</div></header><div class="scrim" id="scrim" hidden></div><main id="main">'''

def footer():
    links=''.join(f'<li><a href="/modelos/{m["slug"]}/">{m["name"]}</a></li>' for m in M)
    return f'''</main><footer class="ftr"><div class="wrap ftr__grid">
<div><a class="logo" href="/"><img src="/img/logo-zontes.png" width="147" height="26" alt="Zontes"><em>Chile</em></a><p>Motocicletas Zontes en Chile, importadas y distribuidas por Importadora Imoto S.A.</p>
<p class="muted">Los datos técnicos pueden modificarse según los requisitos de producción y del mercado. Todas las imágenes son referenciales.</p></div>
<div><h3>Modelos</h3><ul>{links}</ul></div>
<div><h3>Sitio</h3><ul><li><a href="/distribuidores/">Distribuidores</a></li><li><a href="/mantenciones/">Mantenciones y garantía</a></li><li><a href="/nosotros/">Nosotros</a></li><li><a href="/contacto/">Contacto</a></li><li><a href="/derechos/">Derechos del consumidor</a></li></ul></div>
<div><h3>Contacto</h3><ul><li><a href="mailto:contacto@imoto.cl">contacto@imoto.cl</a></li><li>Venta de repuestos: +56 2 2916 7889</li><li><a href="https://wa.me/56966893098" rel="noopener">WhatsApp +56 9 6689 3098</a></li><li>Casa matriz: Argomedo 363, Santiago</li></ul></div>
</div><div class="wrap ftr__bar"><span>© Zontes Chile · Sitio de demostración basado en zontes.cl y zontes.com</span><a href="#top">Volver arriba ↑</a></div></footer>
<script src="/js/app.js" defer></script></body></html>'''

def price_html(m):
    t=''
    if m.get('price_tag'): t+=f'<span class="chip chip--tag">{m["price_tag"]}</span>'
    if m.get('price'):
        old=f'<s>{m["price_old"]}</s> ' if m.get('price_old') else ''
        t+=f'<span class="price">{old}<strong>{m["price"]}</strong></span>'
    return t

def card(m):
    return f'''<article class="mcard" style="--acc:{m["pal"]["acc"]};--panel:{m["pal"]["panel"]}">
<a class="mcard__img" href="/modelos/{m["slug"]}/" aria-label="Ver {m["name"]}"><img src="/img/{m["slug"]}/cut.png" alt="{m["name"]}" loading="lazy" width="900" height="500"></a>
<div class="mcard__b"><span class="chip">{m["tag"]}</span><h3><a href="/modelos/{m["slug"]}/">{m["name"]}</a></h3>
<p>{E(" · ".join(x for x in (m["motor"][1],m["motor"][3]) if x) or m["cat"])}</p><div class="mcard__p">{price_html(m)}</div>
<div class="mcard__a"><a class="btn btn--line" href="/modelos/{m["slug"]}/">Ver modelo</a><a class="btn btn--acc" data-cotizar="{m["slug"]}" href="/modelos/{m["slug"]}/?cotizar=1#cotizar">Cotizar {m["name"]}</a></div></div></article>'''

def model_options(sel=None):
    return '<option value="">Elige un modelo</option>'+''.join(f'<option value="{m["slug"]}"{" selected" if m["slug"]==sel else ""}>{m["name"]}</option>' for m in M)

def region_options():
    return '<option value="">Región</option>'+''.join(f'<option>{r}</option>' for r in REGIONS)

def quote_section(sel,img):
    return f'''<section class="sec sec--quote" id="cotizar"><div class="wrap quote">
<div class="quote__head"><span class="chip">Cotización</span><h2>Cotiza tu {E(BYSLUG[sel]["name"]) if sel in BYSLUG else "Zontes"}</h2>
{f'<img class="quote__moto" src="{img}" alt="{E(BYSLUG[sel]["name"])}" width="900" height="500" loading="lazy">' if img else ''}</div>
<form class="form" id="quote-form" data-fixed="{sel or ""}" novalidate>
<label>Nombre<input name="nombre" autocomplete="name" required></label>
<label>Correo<input name="correo" type="email" autocomplete="email" required></label>
<label>Teléfono<input name="telefono" type="tel" autocomplete="tel" required></label>
<label>Región<select name="region" required>{region_options()}</select></label>
<label>Modelo<select name="modelo" id="quote-model" required>{model_options(sel)}</select></label>
<label>Mensaje (opcional)<textarea name="mensaje" rows="3"></textarea></label>
<button class="btn btn--acc btn--lg" type="submit">Enviar cotización</button>
<p class="form__note" role="status" aria-live="polite" id="quote-status">Se abrirá tu aplicación de correo con la solicitud dirigida a contacto@imoto.cl.</p>
</form></div></section>'''

def spec_table(title,labels,vals):
    rows=''.join(f'<tr><th scope="row">{l}</th><td>{E(v)}</td></tr>' for l,v in zip(labels,vals) if v)
    if not rows: return ''
    return f'<div class="spec"><h3>{title}</h3><table>{rows}</table></div>'

def model_page(m):
    slug=m['slug']; md=MEDIA[slug]; pal=m['pal']
    cols=md['colors']; frames=md.get('frames',0)
    style=f':root{{--panel:{pal["panel"]};--ink:{pal["ink"]};--acc:{pal["acc"]};--ill1:{pal["ill1"]};--ill2:{pal["ill2"]};--ill3:{pal["ill3"]}}}'
    swatches=''.join(f'<button type="button" class="sw" data-color="{c["id"]}" data-start="{c.get("start",0)}" style="--c:{c["hex"]}" aria-label="{c["name"]}" aria-pressed="{"true" if i==0 else "false"}"><span></span></button>' for i,c in enumerate(cols))
    first=cols[0]
    pdf=f'<a class="btn btn--line-ink" href="/fichas/{m["pdf"]}" download>Ficha técnica PDF</a>' if m['pdf'] else '<a class="btn btn--line-ink" href="#ficha">Ver ficha técnica</a>'
    hero=f'''<section class="hero" id="hero">{ill(m["kind"])}<div class="wrap hero__grid">
<div class="hero__txt"><span class="chip chip--ink">{m["tag"]}</span><h1>{m["name"]}</h1><p class="hero__lead">{E(m["lead"])}</p>
<div class="hero__price">{price_html(m)}</div>
<div class="hero__cta"><a class="btn btn--ink" data-cotizar="{slug}" href="#cotizar">Cotizar {m["name"]}</a>{pdf}</div></div>
<div class="hero__moto"><div class="stage" id="stage" data-slug="{slug}" data-frames="{frames}" tabindex="{0 if frames else -1}" aria-label="{'Visor 360° de la '+m["name"]+'. Arrastra o usa las flechas para girar.' if frames else m["name"]}">
<img class="stage__img stage__img--a is-on" src="/img/{slug}/stage/{first["id"]}.webp" alt="{m["name"]} color {first["name"]}" width="1280" height="720" fetchpriority="high" draggable="false">
<img class="stage__img stage__img--b" alt="" width="1280" height="720" draggable="false">
<div class="stage__shadow"></div>
{'<span class="chip chip--glass stage__hint">360° · arrastra para girar</span>' if frames else ''}</div>
<div class="swatches" role="group" aria-label="Color"><span class="swatches__lbl" id="color-name">{first["name"]}</span>{swatches}</div></div></div></section>'''
    # carrusel
    fotos=md['fotos'][:8]+ (md['detalle'][:max(0,5-len(md['fotos']))])
    slides=''.join(f'<figure class="slide" id="s{i}"><button class="slide__b" data-lb="{slug}" data-i="{i}" aria-label="Ampliar foto {i+1}"><img src="/img/{slug}/g/{f["id"]}.webp" alt="{m["name"]}, foto {i+1}" loading="lazy" width="{f["w"]}" height="{f["h"]}"></button></figure>' for i,f in enumerate(fotos))
    carousel=f'''<section class="sec" id="carrusel"><div class="wrap"><div class="sec__h"><h2>{m["name"]} en imágenes</h2>
<div class="car__ctl"><button class="iconbtn" data-car="-1" aria-label="Anterior">←</button><button class="iconbtn" data-car="1" aria-label="Siguiente">→</button></div></div>
<div class="car" id="car" tabindex="0" aria-roledescription="carrusel" aria-label="Fotos de {m["name"]}">{slides}</div><div class="dots" id="dots"></div></div></section>''' if fotos else ''
    # ficha
    ex=''
    if m['extra']:
        ex='<div class="spec"><h3>Datos adicionales</h3><table>'+''.join(f'<tr><th scope="row">{l}</th><td>{E(v)}{"<sup><a href=\"#nota-g\" aria-label=\"Nota\">1</a></sup>" if l.startswith("Altura libre") else ""}</td></tr>' for l,v in m['extra'])+'</table></div>'
    feats=''
    if m['feats']:
        feats='<div class="feats"><h3>Características principales</h3><ul>'+''.join(f'<li>{E(f)}</li>' for f in m['feats'])+'</ul></div>'
    notes='<p class="note">Los datos técnicos pueden modificarse según los requisitos de producción y del mercado. Las especificaciones están sujetas a cambios sin previo aviso. Los datos pueden variar según las condiciones de medición. Todas las imágenes son referenciales.</p>'
    if any(l.startswith('Altura libre') for l,_ in m['extra']): notes+=f'<p class="note" id="nota-g"><sup>1</sup> {GLOBAL_NOTE}</p>'
    if not m['dims'][1] and any(m['dims']): notes+='<p class="note">La altura de asiento no figura en zontes.cl ni en las fichas disponibles de este modelo, por eso se omite.</p>'
    src=f'<p class="note">{E(m["src_note"])} {E(m["media_note"])}</p>' if m.get('src_note') else '<p class="note">Fuente de datos: '+('ficha técnica PDF oficial de zontes.cl y página del modelo.' if m['pdf'] else 'página del modelo en zontes.cl (no hay ficha PDF publicada).')+f' {E(m["media_note"])}</p>'
    ficha=f'''<section class="sec" id="ficha"><div class="wrap"><div class="sec__h"><h2>Especificaciones</h2>{pdf.replace("btn--line-ink","btn--line") if m["pdf"] else ""}</div>
<div class="specs">{spec_table("Motor",MOTOR,m["motor"])}{spec_table("Chasis",CHASIS,m["chasis"])}{spec_table("Dimensiones",DIMS,m["dims"])}{ex}</div>{feats}{notes}{src}</div></section>'''
    # galería
    def grid(items,tab):
        return ''.join(f'<button class="gi" data-lb="{slug}" data-tab="{tab}" data-id="{f["id"]}" data-w="{f["w"]}" data-h="{f["h"]}"><img src="/img/{slug}/g/{f["id"]}_t.webp" alt="{m["name"]} {tab} {j+1}" loading="lazy" width="640" height="{round(640*f["h"]/f["w"])}"></button>' for j,f in enumerate(items))
    nf,nd=len(md['fotos']),len(md['detalle'])
    gal=f'''<section class="sec" id="galeria"><div class="wrap"><div class="sec__h"><h2>Galería {m["name"]}</h2></div>
<div class="tabs" role="tablist" aria-label="Galería"><button role="tab" id="t-fotos" aria-controls="p-fotos" aria-selected="true">Fotos <small>{nf}</small></button><button role="tab" id="t-detalle" aria-controls="p-detalle" aria-selected="false" tabindex="-1">Detalle <small>{nd}</small></button></div>
<div class="gal" id="p-fotos" role="tabpanel" aria-labelledby="t-fotos">{grid(md["fotos"],"fotos") or '<p class="muted">Sin fotos en esta categoría.</p>'}</div>
<div class="gal" id="p-detalle" role="tabpanel" aria-labelledby="t-detalle" hidden>{grid(md["detalle"],"detalle") or '<p class="muted">Sin fotos de detalle disponibles.</p>'}</div></div></section>'''
    others=''.join(f'<a class="mini" href="/modelos/{o["slug"]}/"><img src="/img/{o["slug"]}/cut.png" alt="" loading="lazy" width="900" height="500"><span>{o["name"]}</span></a>' for o in M if o['slug']!=slug)
    more=f'<section class="sec sec--tight"><div class="wrap"><div class="sec__h"><h2>Otros Zontes</h2></div><div class="minis">{others}</div></div></section>'
    gjson=json.dumps({'fotos':[f['id'] for f in md['fotos']],'detalle':[f['id'] for f in md['detalle']],'carousel':[f['id'] for f in fotos],'colors':cols,'frames':frames,'name':m['name']})
    html_=head(f'{m["name"]} · {m["tag"]} · Zontes Chile',m['lead'],extra_style=style,body_cls='model')+header('/modelos/')+hero+carousel+ficha+gal+quote_section(slug,f'/img/{slug}/cut.png')+more+footer().replace('<script src="/js/app.js" defer></script>',f'<script>window.MODEL={gjson}</script><script src="/js/app.js" defer></script>')
    w(f'modelos/{slug}/index.html',html_)

def models_index():
    cards=''.join(card(m) for m in M)
    opts=''.join(f'<option value="{m["slug"]}">{m["name"]}</option>' for m in M)
    pdfs=''.join(f'<li><span>{m["name"]} <small>{m["tag"]}</small></span><a class="btn btn--line btn--sm" href="/fichas/{m["pdf"]}" download>Descargar PDF</a></li>' for m in M if m['pdf'])
    nopdf=', '.join(m['name'] for m in M if not m['pdf'])
    data=json.dumps([{ 'slug':m['slug'],'name':m['name'],'rows':[('Cilindrada',m['motor'][1] or '—'),('Potencia máxima',m['motor'][3] or '—'),('Torque máximo',m['motor'][4] or '—'),('Transmisión',m['motor'][9] or '—'),('Peso en orden de marcha',m['dims'][3] or '—'),('Depósito de combustible',m['dims'][4] or '—'),('Altura del asiento',m['dims'][1] or '—'),('Distancia entre ejes',m['dims'][2] or '—'),('Largo / ancho / alto (mm)',m['dims'][0] or '—'),('Precio',(m.get('price') or m.get('price_tag') or 'Consultar'))]} for m in M],ensure_ascii=False)
    body=f'''<section class="page-h"><div class="wrap"><span class="chip">Línea 2026</span><h1>Modelos</h1><p class="lead">Ocho Zontes con ficha técnica, galería y cotización individual. Compáralos lado a lado o descarga la ficha PDF oficial.</p></div></section>
<section class="sec sec--tight"><div class="wrap"><div class="mgrid">{cards}</div></div></section>
<section class="sec" id="comparador"><div class="wrap"><div class="sec__h"><h2>Compara hasta 3 modelos</h2></div>
<div class="cmp__sel"><label>Modelo 1<select data-cmp>{opts}</select></label><label>Modelo 2<select data-cmp><option value="">—</option>{opts}</select></label><label>Modelo 3<select data-cmp><option value="">—</option>{opts}</select></label></div>
<div class="cmp__wrap"><table class="cmp" id="cmp"></table></div><p class="note">Datos de las fichas oficiales y de zontes.cl. “—” indica dato no disponible en las fuentes.</p></div></section>
<section class="sec" id="fichas"><div class="wrap"><div class="sec__h"><h2>Fichas técnicas oficiales</h2></div><ul class="pdfs">{pdfs}</ul>
<p class="note">Las fichas de ZT200-Z2, ZT350T-E y ZT350T-M son del importador Imoto (imoto.cl); las demás, de zontes.cl. {nopdf}: no hay ficha PDF publicada; sus datos están en la página de cada modelo.</p></div></section>
<section class="sec sec--tight" id="cotizar-rapido"><div class="wrap"><div class="sec__h"><h2>¿Cuál te interesa?</h2></div><div class="qpick">{''.join(f'<a class="btn btn--line" data-cotizar="{m["slug"]}" href="/modelos/{m["slug"]}/?cotizar=1#cotizar">Cotizar {m["name"]}</a>' for m in M)}</div></div></section>'''
    w('modelos/index.html',head('Modelos · Zontes Chile','Línea de motocicletas Zontes en Chile: ficha técnica, comparador y cotización.')+header('/modelos/')+body+footer().replace('<script src="/js/app.js" defer></script>',f'<script>window.CMP={data}</script><script src="/js/app.js" defer></script>'))

def home():
    feat=['zt703-rr','zt368t-e','zt350-t2','zt200-u1']
    chips=''.join(f'<button type="button" class="chip chip--btn" data-home="{s}" aria-pressed="{"true" if i==0 else "false"}">{BYSLUG[s]["name"]}</button>' for i,s in enumerate(feat))
    hdata=json.dumps({s:{'name':BYSLUG[s]['name'],'tag':BYSLUG[s]['tag'],'lead':BYSLUG[s]['lead'],'img':f'/img/{s}/stage/{MEDIA[s]["colors"][0]["id"]}.webp','pal':BYSLUG[s]['pal'],'kind':BYSLUG[s]['kind']} for s in feat},ensure_ascii=False)
    p=BYSLUG['zt703-rr']['pal']
    cards=''.join(card(m) for m in M)
    hero=f'''<section class="hero hero--home" id="hero" style="--panel:{p["panel"]};--ink:{p["ink"]};--acc:{p["acc"]};--ill1:{p["ill1"]};--ill2:{p["ill2"]};--ill3:{p["ill3"]}">{ill("sport")}<div class="wrap hero__grid">
<div class="hero__txt"><span class="chip chip--ink">Motocicletas en Chile</span><h1>Zontes. Diseño y tecnología para cada ruta.</h1>
<p class="hero__lead">Scooters, adventure, scrambler y súper sport con motores de 198 a 699 cc. Elige tu modelo, mira sus fichas y cotiza con un distribuidor autorizado.</p>
<div class="hero__cta"><a class="btn btn--ink" href="/modelos/">Ver modelos</a><a class="btn btn--line-ink" href="/distribuidores/">Encuentra un distribuidor</a></div></div>
<div class="hero__moto"><div class="stage stage--home" id="home-stage"><img class="stage__img stage__img--a is-on" src="/img/zt703-rr/stage/red.webp" alt="Zontes ZT703-RR" width="1280" height="720" fetchpriority="high" draggable="false"><img class="stage__img stage__img--b" alt="" width="1280" height="720" draggable="false"><div class="stage__shadow"></div></div>
<div class="swatches swatches--chips" role="group" aria-label="Modelo destacado">{chips}</div>
<p class="stage__cap" id="home-cap"><strong>ZT703-RR</strong> · Súper Sport — <a href="/modelos/zt703-rr/">ver modelo</a></p></div></div></section>'''
    cats=[('Maxiscooter y ADV','zt368t-e','Dos scooters de 367,6 cc con 40 Nm de torque.'),('Adventure','zt703-f','Del 350 cc al 699 cc de tres cilindros.'),('Scrambler y 198 cc','zt350-gk','ZT350-GK, ZT200-U1 y ZT200-G1.'),('Súper Sport','zt703-rr','ZT703-RR con Quickshift y doble disco.')]
    sec_models=f'''<section class="sec"><div class="wrap"><div class="sec__h"><h2>Elige tu Zontes</h2><a class="link" href="/modelos/">Ver todos {ARROW}</a></div><div class="mgrid">{cards}</div></div></section>'''
    why=f'''<section class="sec sec--alt"><div class="wrap split"><div><span class="chip">Respaldo</span><h2>Garantía y servicio en Chile</h2>
<p>Importadora Imoto S.A. ofrece garantía voluntaria de 12 meses o 10.000 km y de 24 meses o 20.000 km, según la pieza, lo que se cumpla primero. Revisa los valores de mantención por kilometraje y los puntos de servicio.</p>
<div class="cta-row"><a class="btn btn--acc" href="/mantenciones/">Mantenciones y garantía</a><a class="btn btn--line" href="/distribuidores/#servicio">Servicio técnico</a></div></div>
<ul class="ticks"><li>Motores con inyección electrónica BOSCH</li><li>Llave digital inteligente y conectividad Bluetooth en los modelos mayores</li><li>ABS y control de tracción según modelo</li><li>Fichas técnicas oficiales en PDF para cada modelo con ficha publicada</li></ul></div></section>'''
    near=f'''<section class="sec"><div class="wrap"><div class="sec__h"><h2>De Antofagasta a Punta Arenas</h2></div>
<p class="lead">Distribuidores autorizados desde la región de Antofagasta hasta Magallanes. Filtra por región y contacta directamente.</p>
<div class="regions">{''.join(f'<a class="chip chip--btn" href="/distribuidores/?region={E(r)}">{r}</a>' for r in REGIONS)}</div></div></section>'''
    cta=f'''<section class="sec sec--cta"><div class="wrap cta"><h2>¿Listo para cotizar?</h2><p>Elige un modelo y deja tus datos: te contactamos con valores y disponibilidad.</p><a class="btn btn--acc btn--lg" href="/modelos/#cotizar-rapido">Cotizar ahora</a></div></section>'''
    w('index.html',head('Zontes Chile · Motocicletas','Zontes en Chile: scooters, adventure, scrambler y súper sport. Fichas técnicas, galerías y cotización.',body_cls='home')+header('/')+hero+sec_models+why+near+cta+footer().replace('<script src="/js/app.js" defer></script>',f'<script>window.HOME={hdata}</script><script src="/js/app.js" defer></script>'))

def dealers_page():
    st=json.load(open(R+'_raw/st_rows.json'))
    reg_map={'ANTOFAGASTA (II)':'Antofagasta','ATACAMA (III)':'Atacama','COQUIMBO (IV)':'Coquimbo','VALPARAISO (V)':'Valparaíso','METROPOLITANA (RM)':'Metropolitana','O´HIGGINS (VI)':'O’Higgins','MAULE (VII)':'Maule','ÑUBLE (XVI)':'Ñuble','BIO BIO (VIII)':'Biobío','ARAUCANIA (IX)':'Araucanía','LOS RIOS (XIV)':'Los Ríos','LOS LAGOS (X)':'Los Lagos','AYSEN (XI)':'Aysén'}
    svc=[];reg=None
    for r in st[1:]:
        if r[1] in reg_map: reg=reg_map[r[1]]; continue
        if r[1]=='Megamoto': r[1],r[2]='Macul','Megamoto'
        svc.append((reg,r[1],r[2],r[3],'',r[4] if r[4]!='-' else '',r[5]))
    d=lambda L:[dict(region=a,comuna=b,nombre=c,dir=dd,tel=e,cel=f,mail=g) for a,b,c,dd,e,f,g in L]
    data=json.dumps({'dealers':d(DEALERS),'service':d(svc),'regions':REGIONS},ensure_ascii=False)
    body=f'''<section class="page-h"><div class="wrap"><span class="chip">Red Zontes</span><h1>Distribuidores</h1><p class="lead">Distribuidores autorizados 2026 y servicios técnicos autorizados. Filtra por región.</p></div></section>
<section class="sec sec--tight"><div class="wrap">
<div class="tabs" role="tablist" aria-label="Tipo"><button role="tab" id="t-dist" aria-controls="p-list" aria-selected="true">Distribuidores</button><button role="tab" id="t-svc" aria-controls="p-list" aria-selected="false" tabindex="-1">Servicio técnico</button></div>
<div class="filters"><label>Región<select id="f-region">{region_options().replace("<option value=\"\">Región</option>","<option value=\"\">Todas las regiones</option>")}</select></label>
<label>Buscar<input id="f-q" type="search" placeholder="Comuna o nombre"></label><button class="btn btn--line" id="f-reset" type="button">Limpiar</button></div>
<div class="zones" id="zones" role="group" aria-label="Zona"><button class="chip chip--btn" data-zone="" aria-pressed="true">Todo Chile</button><button class="chip chip--btn" data-zone="Norte" aria-pressed="false">Norte</button><button class="chip chip--btn" data-zone="Centro" aria-pressed="false">Centro</button><button class="chip chip--btn" data-zone="Sur" aria-pressed="false">Sur</button></div>
<p class="count" id="f-count" role="status" aria-live="polite"></p><div class="dgrid" id="p-list" role="tabpanel"></div>
<p class="note">Datos de “Distribuidores Autorizados Motocicletas 2026” y “Servicios Técnicos Autorizados” de zontes.cl (la lista de distribuidores se publica como imagen y fue transcrita). Verifica horarios y stock directamente con cada punto.</p></div></section>'''
    w('distribuidores/index.html',head('Distribuidores · Zontes Chile','Distribuidores autorizados y servicios técnicos Zontes en Chile, con filtro por región.')+header('/distribuidores/')+body+footer().replace('<script src="/js/app.js" defer></script>',f'<script>window.DEAL={data}</script><script src="/js/app.js" defer></script>'))

def maint_page():
    heads=['1.000 km','5.000 km','10.000 km','15.000 km','20.000 km']; months=['3 meses','6 meses','12 meses','18 meses','24 meses']
    th=''.join(f'<th scope="col">{h}<small>{mm}</small></th>' for h,mm in zip(heads,months))
    rows=''.join(f'<tr><th scope="row">{n}</th>'+''.join(f'<td data-l="{h}">{v}</td>' for v,h in zip(vs,heads))+'</tr>' for n,vs in MANT)
    body=f'''<section class="page-h"><div class="wrap"><span class="chip">Postventa</span><h1>Mantenciones y garantía</h1><p class="lead">Realiza las mantenciones periódicas por tiempo o kilometraje, lo que se cumpla primero: es indispensable para mantener vigente la garantía de fábrica.</p></div></section>
<section class="sec sec--tight"><div class="wrap"><div class="sec__h"><h2>Valores de mantención por tiempo y kilometraje</h2></div>
<div class="tablewrap"><table class="mtable"><thead><tr><th scope="col">Modelo</th>{th}</tr></thead><tbody>{rows}</tbody></table></div>
<p class="note">Los valores de cada mantención son referenciales, incluyen IVA y pueden variar según el concesionario que visites. Fuente: tabla de valores de mantención de zontes.cl.</p></div></section>
<section class="sec"><div class="wrap"><div class="sec__h"><h2>Garantía extendida o voluntaria</h2></div>
<p class="lead">Importadora Imoto S.A. la ofrece como complemento a la garantía legal y garantiza la motocicleta por 12 meses o 10.000 km y por 24 meses o 20.000 km de uso, lo que se cumpla primero, contados desde la fecha de la factura de venta. No considera el cambio de la motocicleta, sólo el cambio o reparación de partes y piezas según la póliza.</p>
<div class="acc"><details open><summary>12 meses o 10.000 km</summary><p>Batería, bocina, asientos, cable del acelerador, cable del embrague, cable de bloqueo del asiento, cable de bloqueo del depósito de combustible, cable de carga USB, cargador, sellos o retenes.</p></details>
<details><summary>24 meses o 20.000 km · eléctrico y carrocería</summary><p>Foco principal, luces intermitentes, luz de freno, luz de patente, tablero, rectificador, relés, comandos, cerraduras electrónicas, controlador PKE (incluidas las llaves con chip), controlador de parabrisas, motor de parabrisas, espejos retrovisores, depósito de refrigerante, radiador, termostato, mangueras y tuberías.</p></details>
<details><summary>24 meses o 20.000 km · motor y chasis</summary><p>Cárter, tapas de motor, culata, tapa de culata, cigüeñal, válvulas, eje de leva, balancín, ejes principal y secundario, estator, volante, embrague (excluye discos y separadores), bomba de aceite, engranajes y cadena de distribución, cilindro, pistón, anillos de pistón, pasador de pistón, motor de arranque, chasis, silenciador, llantas delantera y trasera, pedalines, torre de dirección, horquilla delantera, amortiguador trasero, discos de freno, depósito de combustible, depósito de aceite, ECU, componentes del cuerpo de aceleración, sensores del sistema de inyección electrónica, bomba de combustible.</p></details></div>
<div class="cta-row"><a class="btn btn--acc" href="/distribuidores/#servicio">Servicio técnico autorizado</a><a class="btn btn--line" href="/derechos/">Derechos y garantías del consumidor</a></div></div></section>'''
    w('mantenciones/index.html',head('Mantenciones y garantía · Zontes Chile','Valores de mantención por kilometraje y condiciones de garantía de las motos Zontes en Chile.')+header('/mantenciones/')+body+footer())

def about():
    body='''<section class="page-h"><div class="wrap"><span class="chip">Marca</span><h1>Nosotros</h1><p class="lead">Zontes es una marca china de motocicletas que llega a Chile de la mano de Importadora Imoto S.A.</p></div></section>
<section class="sec sec--tight"><div class="wrap split"><div><span class="chip">La marca</span><h2>Zontes y Tayo</h2>
<p>Zontes es una de las marcas de Guangdong Tayo Motorcycle Technology Co., Ltd., una empresa conjunta sino-extranjera fundada en 2003 y con certificación aduanera AEO de nivel superior. Se dedica a motocicletas de mediana y gran cilindrada y a minicarros.</p>
<p>Su tesis de desarrollo es la invención y la innovación: cuenta con 256 patentes de apariencia, 121 de modelos de utilidad y 36 de invención, y ha recibido tres veces el Premio de Innovación Tecnológica de Guangdong.</p>
<p class="note">Fuente: “Company profile” en zontes.com (sitio global, versión en inglés), resumido y traducido.</p></div>
<div><span class="chip">En Chile</span><h2>Importadora Imoto S.A.</h2>
<p>En Chile, Zontes es importada y respaldada por Importadora Imoto S.A., que ofrece la garantía extendida o voluntaria.</p>
<p>Casa matriz: Argomedo 363, Santiago. Sucursales en Carmen 754 y Lira 669, Santiago.</p>
<div class="cta-row"><a class="btn btn--acc" href="/distribuidores/">Red de distribuidores</a><a class="btn btn--line" href="/contacto/">Contacto</a></div></div></div></section>
<section class="sec sec--alt"><div class="wrap"><div class="sec__h"><h2>ZONTES SMART</h2></div>
<p class="lead">La app ZONTES SMART permite controlar la moto desde el teléfono, según el modelo. Los modelos mayores incorporan llave inteligente, conectividad Bluetooth y Screen Mirroring.</p>
<p class="note">Fuente: ficha del ZT703-RR en zontes.com y fichas PDF de zontes.cl. La disponibilidad de funciones varía por modelo; revisa la ficha de cada uno.</p></div></section>'''
    w('nosotros/index.html',head('Nosotros · Zontes Chile','Quién es Zontes y quién la importa y respalda en Chile.')+header('/nosotros/')+body+footer())

def contact():
    body='''<section class="page-h"><div class="wrap"><span class="chip">Hablemos</span><h1>Contacto</h1><p class="lead">Escríbenos o visita una sucursal de Importadora Imoto en Santiago.</p></div></section>
<section class="sec sec--tight"><div class="wrap cgrid">
<article class="ccard"><h3>Venta de repuestos</h3><p><a href="mailto:contacto@imoto.cl">contacto@imoto.cl</a></p><p>WhatsApp <a href="https://wa.me/56966893098" rel="noopener">+56 9 6689 3098</a></p><p>Teléfono <a href="tel:+disabled">+56 2 2916 7889</a></p></article>
<article class="ccard"><h3>Postventa</h3><p><a href="mailto:solicitudpostventa@imoto.cl">solicitudpostventa@imoto.cl</a></p></article>
<article class="ccard"><h3>Casa matriz</h3><p>Argomedo 363, Santiago</p><p><a href="mailto:ventasargomedo363@imoto.cl">ventasargomedo363@imoto.cl</a></p><p>+562 2916 7824 / +569 6689 3025</p></article>
<article class="ccard"><h3>Sucursal Carmen</h3><p>Carmen 754, Santiago</p><p><a href="mailto:ventascarmen754@imoto.cl">ventascarmen754@imoto.cl</a></p><p>+562 2916 7894 / +569 6689 3121</p></article>
<article class="ccard"><h3>Sucursal Lira</h3><p>Lira 669, Santiago</p><p><a href="mailto:motocicletaslira1@imoto.cl">motocicletaslira1@imoto.cl</a><br><a href="mailto:richard.meneses@imoto.cl">richard.meneses@imoto.cl</a></p><p>+562 2916 7931 / +569 6907 0930</p></article>
</div></section>'''
    body=body.replace('href="tel:+disabled"','href="tel:+56229167889"')
    w('contacto/index.html',head('Contacto · Zontes Chile','Contacto de Importadora Imoto: ventas, repuestos y postventa Zontes en Chile.')+header('/contacto/')+body+quote_section(None,None).replace('Cotiza tu Zontes','Escríbenos')+footer())

def derechos():
    body='''<section class="page-h"><div class="wrap"><span class="chip">Consumidor</span><h1>Derechos y garantías del consumidor</h1><p class="lead">Resumen de lo publicado por zontes.cl. Para el texto completo consulta el sitio original y la Ley N° 19.496.</p></div></section>
<section class="sec sec--tight"><div class="wrap prose"><h2>Garantía legal</h2><p>Los consumidores pueden hacer valer la garantía legal cuando el producto es defectuoso, le faltan piezas o partes, no es apto para el uso al que fue destinado, o fue arreglado antes y las deficiencias persisten o presenta nuevas fallas. Los defectos deben ser de fábrica y no por mal uso. El cliente puede elegir entre devolución del dinero, cambio del producto o reparación gratuita.</p>
<h2>Retracto</h2><p>El derecho a retracto aplica a compras por internet u otro medio electrónico a distancia, dentro de 10 días desde la recepción, con el producto sin uso y con su embalaje original.</p>
<p class="note">Atención: en zontes.cl el plazo de la garantía legal figura como 6 meses en “Derechos y garantías” y como 3 meses en “Mantenciones”. Confirma el plazo vigente con Imoto o el distribuidor.</p>
<p><a class="btn btn--line" href="https://zontes.cl/derechos-y-garantias-del-consumidor/" rel="noopener">Ver texto original</a> <a class="btn btn--line" href="https://zontes.cl/bienes-durables/" rel="noopener">Ley de bienes durables</a></p></div></section>'''
    w('derechos/index.html',head('Derechos del consumidor · Zontes Chile','Garantía legal y derecho a retracto, según zontes.cl.')+header('/derechos/')+body+footer())

if __name__=='__main__':
    for m in M: model_page(m)
    models_index(); home(); dealers_page(); maint_page(); about(); contact(); derechos()
    os.makedirs(S+'fichas',exist_ok=True)
    for m in M:
        if m['pdf']:
            for root,_,fs in os.walk(R+'_src'):
                if m['pdf'] in fs: shutil.copy(os.path.join(root,m['pdf']),S+'fichas/'+m['pdf'])
    print('built')
