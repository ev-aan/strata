import re, json, random, unicodedata, statistics as st
random.seed(7)
C=json.load(open('casket_fr.json'))
C['III']=C['III'].split('Monsieur si',1)[1]
C['IV']=C['IV'].split("J' AY",1)[1].split('[Endorsed')[0]
C['V']=C['V'].split('Mun coeur',1)[1].split('puis avoir, si vous Tacoeptez')[0]
C['VI']=C['VI'].split('Monsieur, helas',1)[1].split('[Endorsed')[0]
C['II-open']="Estant party du lieu ou j'avois laissé mon cœur il se peult aysement juger quelle estoit ma contenance veu ce que peut un corps sans cœur"
def norm(t):
    t=re.sub(r"-\s*\n\s*","",t)
    t=unicodedata.normalize('NFKD',t.lower()); t=''.join(c for c in t if not unicodedata.combining(c))
    t=t.replace('y','i').replace('j','i').replace('v','u')
    t=re.sub(r"[^a-z' ]+"," ",t.replace("'"," "))
    t=re.sub(r"s(?=[bcdfgklmnpqrtu])","",t)      # estre/etre, mesme/meme (after v->u merge)
    t=re.sub(r"(?<=[aeiou])c(?=t)","",t)          # faict->fait
    t=re.sub(r"(oi|oie|oit|oient|ois)\b",lambda m:'ai'+m.group(1)[2:],t)
    t=re.sub(r"h","",t)
    t=re.sub(r"(.)\1",r"\1",t)                    # collapse doubles
    return t.split()
FW=set(norm("de la le les que qui ie vous ne pas et en du des mon ma mes est a au il elle me ce se sa son pour sans avec auec plus mais ou si nous lui moi tout tant comme un une par sur dont ia y bien fait faire")) 
OLD=re.compile(r"\b(estre|estoit|estant|mesme|faict|avecques|aultre|scavoir|sçavoir|ledict|ladicte|ceste|icelle|nostre|vostre|escript|moy|luy|aussy|ay|cy|faulte|doncques)\b",re.I)
def corpus(files):
    raw=' '.join(open(f,errors='ignore').read() for f in files)
    toks=raw.split()
    keep=[]
    for i in range(0,len(toks),60):
        w=toks[i:i+60]
        if len(OLD.findall(' '.join(w)))>=2: keep.append(norm(' '.join(w)))
    return keep  # list of chunks
M=corpus(['lettresinstructi01mary.txt','lettresinstructi02maryuoft.txt'])
K=corpus(['lettresdecatheri02cathuoft.txt','lettresdecatheri03cathuoft.txt'])
print('chunks kept: Mary',len(M),'Catherine',len(K))
n=min(len(M),len(K)); 
def ngr(ws,k): return set(tuple(ws[i:i+k]) for i in range(len(ws)-k+1) if not all(x in FW for x in ws[i:i+k]))
def index(chunks,k):
    s=set()
    for c in chunks: s|=ngr(c,k)
    return s
def score(text_tokens,Mi,Ki,k):
    g=ngr(text_tokens,k)
    if not g: return None
    m=len(g&Mi)/len(g); c=len(g&Ki)/len(g)
    return m,c
results={}
for k in (3,4):
    # equalise size: subsample to n chunks each
    Ms=random.sample(M,n); Ks=random.sample(K,n)
    Mi=index(Ms,k); Ki=index(Ks,k)
    print(f'\n== n={k}  (equal corpora: {n} chunks ≈ {n*60} words each)')
    for name,t in C.items():
        m,c=score(norm(t),Mi,Ki,k)
        print(f'{name:8s} words={len(norm(t)):4d}  shared-with-Mary={m:.3f}  shared-with-Catherine={c:.3f}  ratio={(m+1e-3)/(c+1e-3):.2f}')
    # calibration: hold out contiguous 7-chunk (~420 words) passages
    calib={'Mary':[], 'Catherine':[]}
    for who,src in (('Mary',M),('Catherine',K)):
        for t in range(40):
            j=random.randrange(20,len(src)-30)
            held=sum(src[j:j+7],[])
            rest=src[:j-15]+src[j+22:]   # exclude neighbourhood
            other=K if who=='Mary' else M
            sm=random.sample(rest if who=='Mary' else other, n-40)
            sk=random.sample(other if who=='Mary' else rest, n-40)
            r=score(held,index(sm,k),index(sk,k),k)
            calib[who].append((r[0]+1e-3)/(r[1]+1e-3))
    for who,v in calib.items():
        right = sum((x>1) if who=='Mary' else (x<1) for x in v)
        print(f'calibration {who:9s}: median ratio {st.median(v):.2f}; correctly assigned {right}/40')
    results[k]=calib
