"""Strata B-002 DT-B1b: genre-matched test. Adds Charles's own formal papers and Henderson's replies (Newcastle, 1646; TCP A78958)."""
import re, json, random, statistics as st, collections, sys
sys.path.insert(0,'/home/claude/strata-casket/data-b002')
from corpora import raw, clean, norm_tokens
random.seed(11)
D=json.load(open('corpora.json')); D['charles'].update(json.load(open('charles1646.json')))
b=raw('A78958')
divs=re.findall(r'<div[^>]*type="([^"]+)"[^>]*>(.*?)(?=<div[^>]*type=|</body>)',b,flags=re.S)
king=[];hend=[]
for t,content in divs:
    w=clean(content)
    if len(w.split())<300: continue
    (king if re.search(r'<signed>\s*C\.\s*R\.',content) else hend).append(w)
D2={'charles_letters':D['charles'],'charles_formal':{'newcastle':' '.join(king)},'henderson':{'newcastle':' '.join(hend)},
    'gauden':D['gauden'],'taylor':D['taylor'],'milton':D['milton']}
AUTH=list(D2); CH=1000; NMFW=150
chunks=[]
for a in AUTH:
    for w,txt in D2[a].items():
        t=norm_tokens(txt)
        for i in range(0,len(t)-CH+1,CH): chunks.append((a,w,i//CH,t[i:i+CH]))
print('chunks per author:',collections.Counter(c[0] for c in chunks))
cnt=collections.Counter(x for c in chunks for x in c[3]); MFW=[w for w,_ in cnt.most_common(NMFW)]
def freqs(tok): c=collections.Counter(tok); n=len(tok); return [c[f]/n for f in MFW]
F=[freqs(c[3]) for c in chunks]
mu=[st.mean(col) for col in zip(*F)]; sd=[st.pstdev(col) or 1e-9 for col in zip(*F)]
Z=[[(v-m)/s for v,m,s in zip(r,mu,sd)] for r in F]
def cent(rows): return [st.mean(c) for c in zip(*rows)]
def delta(a,b): return st.mean(abs(x-y) for x,y in zip(a,b))
def profile(b,excl_k=None):
    k0=chunks[excl_k] if excl_k is not None else None
    rows=[Z[j] for j,c in enumerate(chunks) if c[0]==b and not (k0 and c[1]==k0[1] and c[0]==k0[0] and len({x[1] for x in chunks if x[0]==b})>1)
          and not (k0 and c[0]==k0[0] and c[1]==k0[1] and abs(c[2]-k0[2])<=1)]
    return cent(rows)
print('\nGENRE-MATCHED CALIBRATION: Charles formal papers vs Henderson (same pamphlet), 1,000-word held-out chunks')
for k,c in enumerate(chunks):
    if c[0] not in ('charles_formal','henderson'): continue
    d={b:delta(Z[k],profile(b,k)) for b in AUTH}
    rank=sorted(d,key=d.get)
    print(f'  {c[0]:15s} chunk {c[2]}: nearest {rank[0]:15s} then {rank[1]:15s} | C-formal {d["charles_formal"]:.3f}  Henderson {d["henderson"]:.3f}  C-letters {d["charles_letters"]:.3f}  Gauden {d["gauden"]:.3f}')
def zrow(tok): return [(v-m)/s for v,m,s in zip(freqs(tok),mu,sd)]
full={b:profile(b) for b in AUTH}
print('\nWHOLE TEXTS vs profiles (lower = closer):')
whole=norm_tokens(' '.join(t for _,t in D['eikon'])); dz=zrow(whole)
print('  EIKON (whole)        ',{b:round(delta(dz,full[b]),3) for b in AUTH})
for name,t in [('Charles formal (self)',D2['charles_formal']['newcastle']),('Henderson (self)',D2['henderson']['newcastle'])]:
    z=zrow(norm_tokens(t)); print(f'  {name:21s}',{b:round(delta(z,full[b]),3) for b in AUTH})
print('\nEIKON CHAPTERS, nearest among Charles-formal / Henderson / Gauden / Taylor / Milton (letters profile excluded as genre-mismatched):')
cands=['charles_formal','henderson','gauden','taylor','milton']; tally=collections.Counter(); out=[]
for head,txt in D['eikon']:
    tok=norm_tokens(txt)
    if len(tok)<800: continue
    z=zrow(tok); d={b:delta(z,full[b]) for b in cands}; best=min(d,key=d.get); tally[best]+=1
    out.append((head[:50],len(tok),{b:round(v,3) for b,v in d.items()},best))
    print(f'  {head[:42]:42s} {len(tok):5d}w ' + ' '.join(f'{b[:6]}={d[b]:.3f}' for b in cands) + f'  -> {best}')
print('tally:',dict(tally))
json.dump({'mfw':MFW,'chapters':out},open('dtb1b_results.json','w'))
