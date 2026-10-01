"""Strata B-002: build corpora from EEBO-TCP transcriptions (github.com/textcreationpartnership/<ID>)."""
import re, unicodedata, json
def raw(id):
    t=open(f'{id}/{id}.xml',encoding='utf-8').read()
    return t.split('<text',1)[1]
def clean(x):
    x=re.sub(r'<note.*?</note>',' ',x,flags=re.S)
    x=re.sub(r'<(head|figure|signed|closer|trailer)[^>]*>.*?</\1>',' ',x,flags=re.S)
    x=re.sub(r'<[^>]+>',' ',x)
    x=x.replace('ſ','s').replace('&amp;','and')
    x=re.sub(r'[•〈〉…◊▪]',' ',x)
    return re.sub(r'\s+',' ',x).strip()
def norm_tokens(x):
    x=unicodedata.normalize('NFKD',x.lower()); x=''.join(c for c in x if not unicodedata.combining(c))
    x=x.replace('vv','w').replace('v','u').replace('j','i')
    toks=re.findall(r"[a-z]+",x)
    out=[]
    for w in toks:
        if len(w)>3 and w.endswith('e'): w=w[:-1]
        w=re.sub(r'(.)\1',r'\1',w)
        w=w.replace('y','i')
        out.append(w)
    return out
# --- Charles: own letters in The Kings Cabinet Opened (A31932) ---
c=raw('A31932'); letters=re.findall(r'(<div[^>]*type="letter"[^>]*>.*?</div>)',c,flags=re.S)
KEEP=list(range(0,19))+[21,22,23,34,35,36,37]
def strip_attest(s): return re.split(r'(This is a true Cop|This a true Cop|A true Cop|A True Copy)',s)[0]
charles=[strip_attest(clean(letters[i])) for i in KEEP]
# --- Eikon chapters (A38258, first issue) ---
e=raw('A38258'); parts=re.findall(r'(<div[^>]*type="part"[^>]*>.*?)(?=<div[^>]*type="part"|</body>)',e,flags=re.S)
eikon=[]
for p in parts:
    h=re.search(r'<head>(.*?)</head>',p,flags=re.S); eikon.append((clean(h.group(1)) if h else '?', clean(p)))
GAUDEN=['A42489','A42498','A42492','A42483','A42487','A42490','A42495','A42475','A42477','A42491','A42496','A42479','A42476']
TAYLOR=['A13414','A27805','A63653','A63711']
MILTON=['A50898']
def works(ids,cap=60000):
    return {i:' '.join(clean(raw(i)).split()[:cap]) for i in ids}
data={'charles':{'A31932':' '.join(charles)},'gauden':works(GAUDEN),'taylor':works(TAYLOR),'milton':works(MILTON),'eikon':eikon}
json.dump(data,open('corpora.json','w'))
for a in ['charles','gauden','taylor','milton']:
    print(a,{k:len(v.split()) for k,v in data[a].items()})
print('eikon parts',len(eikon),[len(t.split()) for _,t in eikon])
