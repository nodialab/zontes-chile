import numpy as np, sys
from PIL import Image, ImageFilter
from collections import deque
T=int(sys.argv[1])
src='_raw/cut/_src__cl__zt350t-e__foto1.png'
im=Image.open(src).convert('RGBA'); a=np.array(im).astype(int)
H,W,_=a.shape
r,g,b,al=a[...,0],a[...,1],a[...,2],a[...,3]
yy,xx=np.mgrid[0:H,0:W]
# zona de la escalera: sobre la recta (150,260)->(750,0) en coords completas, salvo espejo y manubrio
line_y=260-(xx-150)*(260/600.0)
zone=(yy<line_y+40)&(xx<760)&(yy<330)
mirror=(xx>520)&(xx<650)&(yy<130)
import numpy as _n
orig=np.array(Image.open('_src/cl/zt350t-e/foto1.jpg').convert('RGB')).astype(int)
mx=orig.max(axis=2)
dark=mx<52
d_line=np.abs((xx-610)*(124-68)-(yy-68)*(658-610))/np.hypot(124-68,658-610)
stalk=(d_line<11)&(xx>600)&(xx<672)&(yy>55)&(yy<135)
mirrorbox=(xx>=543)&(xx<=634)&(yy<=70)
A=(xx<517)&(yy<300)&dark
B=(xx>=517)&(xx<720)&(yy<122)&dark&~stalk&~mirrorbox
R2=(xx>=517)&(xx<545)&(yy<122)
top=np.interp(xx,[195,232,300,400,517],[238,258,255,255,118])
R1=(xx>=195)&(xx<517)&(yy<top)
R3=(xx>=545)&(xx<603)&(yy>=72)&(yy<122)
R4=(xx>=636)&(xx<735)&(yy<82)
R5=(xx>=517)&(xx<590)&(yy>=150)&(yy<215)
R6=(xx>=517)&(xx<545)&(yy<215)
R7=(xx>=530)&(xx<=640)&(yy<=75)&((orig[...,0]-orig[...,2])>2)&(mx<150)
stalk2=(d_line<12)&(xx>598)&(xx<675)&(yy>55)&(yy<135)
R8=(xx>=618)&(xx<700)&(yy>=66)&(yy<115)&~stalk2
R9=(xx>=632)&(xx<642)&(yy<76)&~stalk2
R10=(xx>=538)&(xx<615)&(yy<9)
brown=((A|B|R2|R1|R3|R4|R5|R6|R7|R8|R9|R10)&(al>0))|(((r-b)>T)&zone&~mirror&(al>0)&(xx<517))
print('removed',brown.sum())
al2=al.copy(); al2[brown]=0
# quitar píxeles oscuros no marrones muy dentro de la zona y lejos de la moto: se resuelve con componentes
m=al2>40
seen=np.zeros((H,W),bool); comps=[]
for sy in range(H):
    for sx in range(W):
        if m[sy,sx] and not seen[sy,sx]:
            q=deque([(sy,sx)]); seen[sy,sx]=True; comp=[]
            while q:
                y,x=q.popleft(); comp.append((y,x))
                for dy,dx in((1,0),(-1,0),(0,1),(0,-1)):
                    ny,nx=y+dy,x+dx
                    if 0<=ny<H and 0<=nx<W and m[ny,nx] and not seen[ny,nx]: seen[ny,nx]=True;q.append((ny,nx))
            comps.append(comp)
comps.sort(key=len,reverse=True)
keep=np.zeros((H,W),bool)
for c in comps:
    if len(c)>=0.01*len(comps[0]):
        ys,xs=zip(*c); keep[ys,xs]=True
al2[~keep]=0
alpha=Image.fromarray(al2.astype('uint8')).filter(ImageFilter.GaussianBlur(0.8))
res=Image.fromarray(a.astype('uint8'),'RGBA'); res.putalpha(alpha)
res.save('_raw/cut/_src__cl__zt350t-e__foto1_clean.png')
bg=Image.new('RGBA',res.size,(212,214,208,255)); bg.alpha_composite(res); bg.convert('RGB').resize((W//2,H//2)).save('/private/tmp/claude-501/te_clean.jpg')
