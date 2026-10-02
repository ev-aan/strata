"""Strata B-002 F10: authorship VERIFICATION. Compare Eikon samples' distance to Gauden with (a) Gauden's own held-out works and (b) 8 other divines.
Same for Charles. All samples 2,000 words. Profiles exclude the work being tested."""
import sys, statistics as st
exec(open('/home/claude/strata-casket/data-b002/genre_matched.py').read().split("print('\\nGENRE-MATCHED")[0])
from corpora import raw, clean
def zrow(tok): return [(v-m)/s for v,m,s in zip(freqs(tok),mu,sd)]
def prof_excl(author,work):
    rows=[Z[j] for j,c in enumerate(chunks) if c[0]==author and c[1]!=work]; return cent(rows)
def samples(tok,n=2000,maxs=4): return [tok[s:s+n] for s in range(0,len(tok)-n+1,n)][:maxs]
CONTROLS=['A45397','A57134','A01344','A02549','A64646','A62025','A26864','A31927']
G=prof_excl('gauden',None); C=cent([Z[j] for j,c in enumerate(chunks) if c[0] in('charles_formal','charles_letters')])
groups={'Gauden own works (held out)':[], 'Other divines':[], 'Eikon Basilike':[], 'Charles own (held out)':[]}
gC={k:[] for k in groups}
for w,txt in D2['gauden'].items():
    Pw=prof_excl('gauden',w)
    for s in samples(norm_tokens(txt),maxs=2): groups['Gauden own works (held out)'].append(delta(zrow(s),Pw)); gC['Gauden own works (held out)'].append(delta(zrow(s),C))
for id in CONTROLS:
    for s in samples(norm_tokens(clean(raw(id)))): groups['Other divines'].append(delta(zrow(s),G)); gC['Other divines'].append(delta(zrow(s),C))
etok=norm_tokens(' '.join(t for _,t in D['eikon']))
for s in samples(etok,maxs=40): groups['Eikon Basilike'].append(delta(zrow(s),G)); gC['Eikon Basilike'].append(delta(zrow(s),C))
for a,w in [('charles_formal','newcastle'),('charles_letters','A31932'),('charles_letters','charles1646')]:
    Pc=cent([Z[j] for j,c in enumerate(chunks) if c[0] in('charles_formal','charles_letters') and not (c[0]==a and c[1]==w)])
    for s in samples(norm_tokens(D2[a][w]),maxs=6): gC['Charles own (held out)'].append(delta(zrow(s),Pc)); groups['Charles own (held out)'].append(delta(zrow(s),G))
def q(v,p): v=sorted(v); return v[int(p*(len(v)-1))]
print('Distance to GAUDEN profile (lower = closer), 2,000-word samples:')
for k,v in groups.items(): print(f'  {k:30s} n={len(v):3d}  median {st.median(v):.3f}   middle half {q(v,.25):.3f}-{q(v,.75):.3f}')
print('\nDistance to CHARLES profile (letters + formal papers):')
for k,v in gC.items(): print(f'  {k:30s} n={len(v):3d}  median {st.median(v):.3f}   middle half {q(v,.25):.3f}-{q(v,.75):.3f}')
