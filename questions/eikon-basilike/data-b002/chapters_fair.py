"""Strata B-002 G-07 fairness check: Charles's formal papers vs a profile built from his letters only (no shared source or genre)."""
import sys, random, statistics as st
exec(open('/home/claude/strata-casket/data-b002/chapters.py').read().split("print(f'{\"chapter\"")[0])
LET=cent([Z[j] for j,c in enumerate(chunks) if c[0]=='charles_letters'])
form=CTOK[('charles_formal','newcastle')]
for L in (1000,1500):
    own=[delta(zrow(form[s:s+L]),LET) for s in range(0,len(form)-L,250)]
    ch=[delta(zrow(norm_tokens(t)[:L]),LET) for _,t in D['eikon'] if len(norm_tokens(t))>=L]
    oth=[delta(zrow(p),LET) for k,p in draws(CTRL,L,60)]
    print(f'L={L}: Charles formal papers vs letters-only profile: median {st.median(own):.3f} (max {max(own):.3f}, n={len(own)} overlapping windows)')
    print(f'       Eikon chapters: median {st.median(ch):.3f} (min {min(ch):.3f}, n={len(ch)});  other clergy: median {st.median(oth):.3f}')
    print(f'       chapters closer than the FARTHEST Charles formal window: {sum(x<=max(own) for x in ch)} of {len(ch)}')
