import re,subprocess,sys,urllib.parse
base='https://www.zontes.com/EN/Products/ProductsList.aspx'
def curl(args): return subprocess.run(['curl','-sL','-A','Mozilla/5.0','-c','cj.txt','-b','cj.txt']+args,capture_output=True).stdout.decode('utf-8','ignore')
h=curl([base])
def fields(h):
    d={}
    for n in ['__VIEWSTATE','__VIEWSTATEGENERATOR','__EVENTVALIDATION','__VIEWSTATEENCRYPTED']:
        m=re.search(r'id="%s" value="([^"]*)"'%n,h)
        if m: d[n]=m.group(1)
    return d
out={}
for ctl in sys.argv[1:]:
    d=fields(h); d['__EVENTTARGET']=ctl; d['__EVENTARGUMENT']=''
    r=curl(['-X','POST','--data',urllib.parse.urlencode(d),base])
    open(f'gl/pb_{ctl.split("$")[2]}.html','w').write(r)
    names=re.findall(r'ModelsDetailed\.aspx\?Cid=(\w+)',r)
    print(ctl,len(r),len(names),names[:8])
