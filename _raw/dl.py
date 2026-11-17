import sys,os,subprocess,urllib.parse
from concurrent.futures import ThreadPoolExecutor
def get(a):
    u,p=a
    os.makedirs(os.path.dirname(p),exist_ok=True)
    if os.path.exists(p) and os.path.getsize(p)>0: return p,'skip'
    q=urllib.parse.quote(u,safe=':/%?=&')
    r=subprocess.run(['curl','-sL','--max-time','90','-A','Mozilla/5.0','-o',p,'-w','%{http_code}',q],capture_output=True,text=True)
    if r.stdout!='200': 
        if os.path.exists(p): os.remove(p)
        return p,'ERR '+r.stdout
    return p,os.path.getsize(p)
items=[l.split('\t') for l in open(sys.argv[1]).read().split('\n') if l]
with ThreadPoolExecutor(8) as ex:
    for p,r in ex.map(get,items):
        if isinstance(r,str) and r!='skip': print(p,r)
