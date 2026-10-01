"""Strata B-002 DT-B1: Burrows' Delta, leave-one-work-out calibration, chapter scoring, feature bootstrap. Seed fixed."""
import json, random, statistics as st, collections, sys
sys.path.insert(0,'/home/claude/strata-casket/data-b002')
from corpora import norm_tokens
random.seed(11)
D=json.load(open('corpora.json')); D['charles'].update(json.load(open('charles1646.json')))
AUTH=['charles','gauden','taylor','milton']; CH=1500; NMFW=150
chunks=[]  # (author, work, idx, tokens)
for a in AUTH:
    for w,txt in D[a].items():
        t=norm_tokens(txt)
        for i in range(0,len(t)-CH+1,CH): chunks.append((a,w,i//CH,t[i:i+CH]))
cnt=collections.Counter(x for c in chunks for x in c[3])
MFW=[w for w,_ in cnt.most_common(NMFW)]
def freqs(tok,feat):
    c=collections.Counter(tok); n=len(tok); return [c[f]/n for f in feat]
def build(feat):
    F=[freqs(c[3],feat) for c in chunks]
    mu=[st.mean(col) for col in zip(*F)]; sd=[st.pstdev(col) or 1e-9 for col in zip(*F)]
    Z=[[(v-m)/s for v,m,s in zip(r,mu,sd)] for r in F]
    return Z,mu,sd
def centroid(rows): return [st.mean(c) for c in zip(*rows)]
def delta(a,b): return st.mean(abs(x-y) for x,y in zip(a,b))
Z,mu,sd=build(MFW)
# calibration
res=collections.defaultdict(lambda:[0,0]); conf=collections.Counter()
for k,(a,w,i,_) in enumerate(chunks):
    cents={}
    for b in AUTH:
        rows=[Z[j] for j,(bb,ww,ii,_) in enumerate(chunks) if bb==b and not (ww==w) ]
        if b==a and not rows:  # single-work author: drop neighbourhood only
            rows=[Z[j] for j,(bb,ww,ii,_) in enumerate(chunks) if bb==b and ww==w and abs(ii-i)>2]
        cents[b]=centroid(rows)
    pred=min(AUTH,key=lambda b:delta(Z[k],cents[b]))
    res[a][0]+=pred==a; res[a][1]+=1; conf[(a,pred)]+=1
print('CALIBRATION (held-out 1,500-word chunks; same-work chunks never used to build the true author profile)')
for a in AUTH: print(f'  {a:8s} {res[a][0]}/{res[a][1]} correct')
print('  confusions:',{f'{a}->{p}':n for (a,p),n in conf.items() if a!=p})
tot=sum(v[0] for v in res.values()); n=sum(v[1] for v in res.values()); print(f'  overall {tot}/{n} = {tot/n:.0%}')
# cross-source check for Charles
cents={b:centroid([Z[j] for j,c in enumerate(chunks) if c[0]==b]) for b in AUTH}
# Eikon chapters
E=D['eikon']
print('\nEIKON CHAPTERS (nearest author by Delta; bootstrap share over 200 resamples of 100 of 150 words)')
summary=collections.Counter(); rows_out=[]
fullcents={b:centroid([Z[j] for j,c in enumerate(chunks) if c[0]==b]) for b in AUTH}
def zrow(tok,feat,mu,sd): return [(v-m)/s for v,m,s in zip(freqs(tok,feat),mu,sd)]
boots=[]
for _ in range(200):
    idx=sorted(random.sample(range(NMFW),100)); boots.append(idx)
for head,txt in E:
    tok=norm_tokens(txt)
    if len(tok)<800: continue
    z=zrow(tok,MFW,mu,sd)
    d={b:delta(z,fullcents[b]) for b in AUTH}
    best=min(d,key=d.get)
    share=collections.Counter()
    for idx in boots:
        dd={b:st.mean(abs(z[i]-fullcents[b][i]) for i in idx) for b in AUTH}
        share[min(dd,key=dd.get)]+=1
    summary[best]+=1
    rows_out.append((head[:48],len(tok),{b:round(v,3) for b,v in d.items()},best,dict(share)))
    print(f'  {head[:44]:44s} {len(tok):5d}w  C={d["charles"]:.3f} G={d["gauden"]:.3f} T={d["taylor"]:.3f} M={d["milton"]:.3f}  -> {best:7s} boot {dict(share)}')
whole=norm_tokens(' '.join(t for _,t in E)); z=zrow(whole,MFW,mu,sd)
print('\nWHOLE BOOK:',{b:round(delta(z,fullcents[b]),3) for b in AUTH})
print('chapters by nearest author:',dict(summary))
json.dump({'mfw':MFW,'chapters':rows_out},open('dtb1_results.json','w'))
