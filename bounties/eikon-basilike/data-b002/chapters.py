"""Strata B-002 G-07: does any single chapter fall inside Charles's own range?
For each chapter (length L), compare its distance to the Charles profile with held-out passages of the SAME length from
(a) Charles's own writing (profile excludes the source being tested) and (b) eight other clergy. Seed fixed."""
import sys, random, statistics as st
exec(open('/home/claude/strata-casket/data-b002/genre_matched.py').read().split("print('\\nGENRE-MATCHED")[0])
from corpora import raw, clean
random.seed(5)
def zrow(tok): return [(v-m)/s for v,m,s in zip(freqs(tok),mu,sd)]
CS=[('charles_formal','newcastle'),('charles_letters','A31932'),('charles_letters','charles1646')]
def cprof(excl=None):
    return cent([Z[j] for j,c in enumerate(chunks) if c[0] in('charles_formal','charles_letters') and (c[0],c[1])!=excl])
PROF={x:cprof(x) for x in CS}; FULL=cprof()
CTRL={id:norm_tokens(clean(raw(id))) for id in ['A45397','A57134','A01344','A02549','A64646','A62025','A26864','A31927']}
CTOK={x:norm_tokens(D2[x[0]][x[1]]) for x in CS}
def draws(src,L,n):
    out=[]
    for _ in range(n):
        k=random.choice(list(src)); t=src[k]
        if len(t)<=L: continue
        s=random.randrange(0,len(t)-L); out.append((k,t[s:s+L]))
    return out
print(f'{"chapter":44s} {"words":>5s}  {"dist":>5s}  {"within Charles own (share of his passages as far or farther)":>10s}  {"other clergy as far or farther"}')
rows=[]
for head,txt in D['eikon']:
    tok=norm_tokens(txt); L=len(tok)
    if L<800: continue
    L=min(L,2500); tok=tok[:L]
    d=delta(zrow(tok),FULL)
    own=[delta(zrow(p),PROF[k]) for k,p in draws(CTOK,L,60)]
    oth=[delta(zrow(p),FULL) for k,p in draws(CTRL,L,60)]
    p_own=sum(x>=d for x in own)/len(own); p_oth=sum(x>=d for x in oth)/len(oth)
    flag='  <-- inside Charles range' if p_own>=0.10 else ''
    rows.append((head[:44],L,round(d,3),round(p_own,2),round(p_oth,2)))
    print(f'{head[:44]:44s} {L:5d}  {d:.3f}  {p_own:10.0%}  {p_oth:10.0%}{flag}')
inside=[r for r in rows if r[3]>=0.10]
print(f'\nchapters inside Charles range (>=10% of his own passages as far or farther): {len(inside)} of {len(rows)}')
