import sys,os
from rembg import remove,new_session
from PIL import Image
Image.MAX_IMAGE_PIXELS=None
s=new_session('isnet-general-use')
for p in sys.argv[1:]:
    im=Image.open(p).convert('RGB'); im.thumbnail((2000,2000))
    out=remove(im,session=s)
    n=p.replace('/','__')
    out.save('_raw/cut/'+os.path.splitext(n)[0]+'.png'); print(n,out.size)
