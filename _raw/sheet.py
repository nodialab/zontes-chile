import sys,os,glob
from PIL import Image,ImageDraw
Image.MAX_IMAGE_PIXELS=None
d=sys.argv[1]; out=sys.argv[2]
fs=sorted(f for f in glob.glob(d+'/**/*',recursive=True) if f.lower().endswith(('.jpg','.jpeg','.png','.gif','.webp')))
T=300; cols=5
rows=(len(fs)+cols-1)//cols
S=Image.new('RGB',(cols*T,rows*(T+18)),'#888')
dr=ImageDraw.Draw(S)
for i,f in enumerate(fs):
    try:
        im=Image.open(f); sz=im.size
        im=im.convert('RGBA'); im.thumbnail((T-6,T-6))
        bg=Image.new('RGBA',im.size,'#cccccc'); bg.alpha_composite(im)
        S.paste(bg.convert('RGB'),((i%cols)*T+3,(i//cols)*(T+18)))
    except Exception as e: sz=str(e)[:20]
    dr.text(((i%cols)*T+3,(i//cols)*(T+18)+T),f"{os.path.basename(f)[:28]} {sz}",fill='white')
S.save(out,quality=80); print(out,len(fs))
