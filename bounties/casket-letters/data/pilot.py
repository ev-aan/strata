import re, unicodedata, math, collections
def norm(t):
    t=unicodedata.normalize('NFKD',t.lower()); t=''.join(c for c in t if not unicodedata.combining(c))
    t=t.replace('y','i').replace('ç','c')
    t=re.sub(r"[^a-z' ]+"," ",t.replace('-\n','').replace('\n',' '))
    t=re.sub(r"s(?=[bcdfgjklmnpqrtv])","",t)   # estant->etant, estoit->etoit
    t=re.sub(r"\b(\w+?)(oye|ois|oit)\b",r"\1ai",t) # avois/avoye ~ avai
    return re.sub(r"\s+"," ",t).strip()
Q="Estant party du lieu ou j'avois laissé mon cœur il se peult aysement juger quelle estoit ma contenance, veu ce que peut un corps sans cœur"
q=norm(Q); qw=q.split()
def grams(ws,n=3): return set(tuple(ws[i:i+n]) for i in range(len(ws)-n+1))
def cg(s,n=4): s=' '+s+' '; return collections.Counter(s[i:i+n] for i in range(len(s)-n+1))
def cos(a,b):
    num=sum(a[k]*b.get(k,0) for k in a); return num/math.sqrt(sum(v*v for v in a.values())*sum(v*v for v in b.values()) or 1)
qc=cg(q); qg=grams(qw)
res=[]
for vol in ['lettresinstructi01mary','lettresinstructi02maryuoft']:
    raw=open(vol+'.txt',errors='ignore').read()
    lines=raw.split('\n')
    # map word index -> line number
    words=[];lineof=[]
    for i,l in enumerate(lines):
        for w in norm(l).split(): words.append(w); lineof.append(i)
    W=len(qw)
    for s in range(0,len(words)-W,3):
        win=words[s:s+W+6]; t=' '.join(win)
        sc=cos(qc,cg(t)); sh=len(qg & grams(win))
        res.append((sc,sh,vol,lineof[s],t))
res.sort(reverse=True)
seen=[]
for r in res:
    if any(r[2]==x[2] and abs(r[3]-x[3])<40 for x in seen): continue
    seen.append(r)
    if len(seen)>=12: break
for sc,sh,vol,ln,t in seen: print(f"{sc:.3f} shared3grams={sh} {vol}:{ln}  {t[:150]}")
import statistics
allsc=[r[0] for r in res]; print('n windows',len(allsc),'mean',round(statistics.mean(allsc),3),'sd',round(statistics.pstdev(allsc),3))
