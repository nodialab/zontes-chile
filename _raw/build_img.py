import os,glob,json,sys,re
from concurrent.futures import ProcessPoolExecutor
from PIL import Image,ImageChops
Image.MAX_IMAGE_PIXELS=None
R='/Users/ansokbeatz/Documents/AI Projects/Zontes/'
OUT=R+'site/img/'
C360={ # slug -> (gl360 dir, {colorid:(name,hex)})
 'zt703-rr':('703rr',{'red':('Rojo','#c8102e'),'black':('Negro brillante','#16171a'),'silver':('Plata brillante','#c9ccd1')}),
 'zt703-f':('703f',{'silver':('Plata brillante','#c9ccd1'),'pianoblack':('Negro piano / gris','#2b2e33')}),
 'zt368t-e':('368e',{'pianoblack':('Negro piano','#17181b'),'mechgrey':('Gris mecánico','#9aa0a6')}),
}
STATIC={ # slug -> {colorid:(name,hex,path)}
 'zt368t-g':{'black':('Negro','#17181b','_src/gl/368g/Car202509081712555025.png'),'mechgrey':('Gris mecánico','#aeb4ba','_src/gl/368g/Car202509081715245562.png'),'green':('Verde','#4c5a45','_src/gl/368g/Car202509081717134969.png'),'brown':('Café mate','#9b8a73','_src/gl/368g/Car202509081711167894.png')},
 'zt350-t2':{'orange':('Naranja','#e8601c','_raw/cut/_src__cl__zt350-t2__ZONTES-T350X-NARANJA-4.png'),'black':('Negro','#17181b','_raw/cut/_src__cl__zt350-t2__ZONTES-T350X-Negro-4.png')},
 'zt200-u1':{'bluorange':('Azul / naranja','#1f5f86','_raw/cut/_src__cl__zt200-u1__ZT200-U1_blue_Orange7.png'),'silver':('Plata','#c5c9cc','_raw/cut/_src__cl__zt200-u1__ZT200-U1_silver5.png')},
 'zt350-gk':{'silver':('Plata / naranja','#c9ccd1','_raw/cut/_src__cl__zt350-gk__4B0A4849.png'),'blue':('Negro / azul','#1c3f8f','_raw/cut/_src__cl__zt350-gk__4B0A6330.png')},
 'zt350t-e':{'white':('Blanco','#e9eaec','_raw/cut/_clean__zt350t-e.png')},
 'zt350t-m':{'blue':('Azul','#2f5d8a','_raw/cut/_src__imoto__zt350t-m__main.png')},
 'zt200-z2':{'grey':('Gris / azul','#4a5866','_raw/cut/_src__imoto__zt200-z2__grey.png')},
 'zt200-g1':{'blue':('Azul mate','#3a5a73','_src/cl/zt200-g1/辐条轮磨砂古蓝-4.png'),'gold':('Negro / dorado','#2a2620','_src/cl/zt200-g1/辐条轮黑金-1.png')},
}
def PC(slug,c):
    return 9 if (slug,c)==('zt703-rr','silver') else POSTER.get(slug,9)
POSTER=json.load(open(R+'data/poster.json')) if os.path.exists(R+'data/poster.json') else {}
CL={'zt703-rr':'zt703-rr-super-sport','zt703-f':'zt703-f','zt368t-e':'zt368t-e','zt368t-g':'zt368t-g-scooter-adv','zt350-t2':'zt350-t2','zt200-u1':'zt200-u1','zt200-g1':'zt200-g1','zt350-gk':'zt350-gk','zt350t-e':'zt350t-e','zt350t-m':'../ext/zt350t-m','zt200-z2':'../ext/zt200-z2'}
GL={'zt703-rr':'703rr','zt703-f':'703f','zt368t-e':'368e','zt368t-g':None,'zt350-t2':None,'zt200-u1':None,'zt200-g1':None,'zt350-gk':None,'zt350t-e':None,'zt350t-m':None,'zt200-z2':None}
BAD=re.compile(r'(SALTO|升仕|pista|PORTADA|recorte|Gemini|Captura|Carrusel|^Car\d|TH3|Rain|Rider|Road|hig_deep|light|mvbg|Point|mv703|YB\d|MS\d|^BLB|brembo|703FJLY|FJLY|CG2\.jpg|^CG2-1|703FBS|BGYG5|BGY|^CG5)',re.I)
def norm_frame(args):
    src,dst,box=args
    im=Image.open(src).convert('RGBA').crop(box).resize((1280,720),Image.LANCZOS)
    im.save(dst,'WEBP',quality=78,method=4)
def trim_fit(im,W=1600,H=900,maxw=0.88,maxh=0.74,base=0.88):
    bb=im.getchannel('A').point(lambda v:255 if v>20 else 0).getbbox(); im=im.crop(bb)
    s=min(W*maxw/im.width,H*maxh/im.height); im=im.resize((round(im.width*s),round(im.height*s)),Image.LANCZOS)
    c=Image.new('RGBA',(W,H),(0,0,0,0)); c.paste(im,((W-im.width)//2,round(H*base)-im.height),im); return c
def sil(f):
    return list(Image.open(f).convert('RGBA').getchannel('A').resize((64,36)).getdata())
def align(g,cols):
    ref=list(cols)[0]
    S={c:[sil(f) for f in sorted(glob.glob(f'{R}_src/gl360/{g}/{c}/*.png'))] for c in cols}
    order={ref:list(range(37))}
    for c in cols:
        if c==ref: continue
        if c=='silver' and g=='703rr': order[c]=list(range(37)); continue
        best=None
        for rev in (1,-1):
            for sft in range(37):
                idx=[(rev*i+sft)%37 for i in range(37)]
                e=sum(sum(abs(a-b) for a,b in zip(S[ref][i],S[c][idx[i]])) for i in range(0,37,3))
                if best is None or e<best[0]: best=(e,idx)
        order[c]=best[1]
    return order
def main():
    meta={}
    ex=ProcessPoolExecutor(8)
    # 360
    for slug,(g,cols) in C360.items():
        d=OUT+slug; os.makedirs(d+'/stage',exist_ok=True)
        ubox=None
        for c in cols:
            for f in sorted(glob.glob(f'{R}_src/gl360/{g}/{c}/*.png')):
                bb=Image.open(f).convert('RGBA').getchannel('A').point(lambda v:255 if v>20 else 0).getbbox()
                ubox=bb if ubox is None else (min(ubox[0],bb[0]),min(ubox[1],bb[1]),max(ubox[2],bb[2]),max(ubox[3],bb[3]))
        w=ubox[2]-ubox[0]; w=int(w*1.06); h=round(w*9/16)
        cx=(ubox[0]+ubox[2])//2; cy=(ubox[1]+ubox[3])//2
        box=(cx-w//2,cy-h//2,cx+w//2,cy+h//2)
        order=align(g,cols); jobs=[]
        for c in cols:
            os.makedirs(f'{d}/360/{c}',exist_ok=True)
            fl=sorted(glob.glob(f'{R}_src/gl360/{g}/{c}/*.png'))
            for i,k in enumerate(order[c]):
                jobs.append((fl[k],f'{d}/360/{c}/{i:02d}.webp',box))
        list(ex.map(norm_frame,jobs))
        for c in cols:
            im=Image.open(f'{d}/360/{c}/{PC(slug,c):02d}.webp'); im.save(f'{d}/stage/{c}.webp','WEBP',quality=85)
        meta[slug]={'frames':37,'colors':[{'id':c,'name':n,'hex':h,'start':PC(slug,c)} for c,(n,h) in cols.items()]}
        # PNG for quote
        im=Image.open(f'{d}/360/{list(cols)[0]}/{PC(slug,list(cols)[0]):02d}.webp').convert('RGBA'); im=im.crop(im.getchannel('A').point(lambda v:255 if v>20 else 0).getbbox())
        im.thumbnail((900,900)); im.save(f'{d}/cut.png',optimize=True)
        print(slug,'360 ok',box)
    for slug,cols in STATIC.items():
        d=OUT+slug; os.makedirs(d+'/stage',exist_ok=True)
        for c,(n,h,p) in cols.items():
            im=Image.open(R+p).convert('RGBA'); im.thumbnail((2400,2400))
            trim_fit(im).save(f'{d}/stage/{c}.webp','WEBP',quality=88)
        first=list(cols)[0]
        im=Image.open(R+list(cols.values())[0][2]).convert('RGBA'); im.thumbnail((2000,2000)); im=im.crop(im.getchannel('A').point(lambda v:255 if v>20 else 0).getbbox()); im.thumbnail((900,900)); im.save(f'{d}/cut.png',optimize=True)
        meta.setdefault(slug,{})['frames']=0; meta[slug]['colors']=[{'id':c,'name':n,'hex':h} for c,(n,h,p) in cols.items()]
    # gallery
    for slug in CL:
        d=OUT+slug; os.makedirs(d+'/g',exist_ok=True)
        cands=[]
        for base in [f'{R}_src/cl/{CL[slug]}']+([f'{R}_src/gl/{GL[slug]}'] if GL[slug] else []):
            for f in glob.glob(base+'/*'):
                n=os.path.basename(f)
                if not n.lower().endswith('.jpg') or BAD.search(n): continue
                try: im=Image.open(f)
                except: continue
                if im.width<480 or im.width/im.height<1.0 and False: continue
                cands.append((f,im.width,im.height))
        cands.sort(key=lambda x:-x[1]*x[2])
        kept=[];hashes=[]
        for f,w,h in cands:
            im=Image.open(f).convert('L'); t=im.resize((24,14))
            if any(sum(abs(a-b) for a,b in zip(t.getdata(),o))/336<7 for o in hashes): continue
            hashes.append(list(t.getdata())); kept.append(f)
        fotos=[];det=[]
        for i,f in enumerate(kept):
            im=Image.open(f).convert('RGB'); top=im.resize((40,40)).crop((0,0,40,10)); lum=sum(top.convert('L').getdata())/400
            tag='f' if lum>105 else 'd'
            im.thumbnail((2000,2000)); name=f'{i:02d}'
            im.save(f'{d}/g/{name}.webp','WEBP',quality=80)
            t=im.copy(); t.thumbnail((640,640)); t.save(f'{d}/g/{name}_t.webp','WEBP',quality=72)
            (fotos if tag=='f' else det).append({'id':name,'w':im.width,'h':im.height,'src':os.path.basename(f)})
        meta.setdefault(slug,{})['fotos']=fotos; meta[slug]['detalle']=det
        print(slug,len(fotos),len(det))
    json.dump(meta,open(R+'data/media.json','w'),ensure_ascii=False,indent=1)
if __name__=='__main__': main()
