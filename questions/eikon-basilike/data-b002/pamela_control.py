"""Strata B-002 positive control: does phrase matching find the 'Prayer in time of Captivity' (1687 Works, TCP A31771) in Sidney's Arcadia (1590, A12229)?"""
import re, json, sys, collections
sys.path.insert(0,'/home/claude/strata-casket/data-b002')
from corpora import raw, clean, norm_tokens
t=clean(raw('A31771')); s=t.index('O Powerful and eternal God, to whom nothing is so great')
prayer=t[s:s+2600]
P=norm_tokens(prayer)
D=json.load(open('corpora.json'))
SOURCES={'Sidney, Arcadia (1590)':clean(raw('A12229')),'Gauden (all works)':' '.join(D['gauden'].values()),
 'Taylor (all works)':' '.join(D['taylor'].values()),'Milton, Eikonoklastes':' '.join(D['milton'].values()),'Eikon chapters (first issue)':' '.join(t for _,t in D['eikon'])}
def grams(tok,n): return set(tuple(tok[i:i+n]) for i in range(len(tok)-n+1))
print(f'Prayer: {len(P)} words')
for n in (4,6):
    pg=grams(P,n)
    for name,txt in SOURCES.items():
        g=grams(norm_tokens(txt),n); print(f'  {n}-word phrases shared with {name:30s}: {len(pg&g):3d} of {len(pg)}  ({len(pg&g)/len(pg):.0%})')
# longest shared run with Arcadia
A=norm_tokens(SOURCES['Sidney, Arcadia (1590)']); Aset={tuple(A[i:i+8]):i for i in range(len(A)-8)}
hits=[i for i in range(len(P)-8) if tuple(P[i:i+8]) in Aset]
print('8-word runs found in Arcadia starting at prayer word positions:',hits[:40])
