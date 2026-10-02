"""Strata B-002 F9: is the Gauden profile an 'attractor' for any learned 1640s prose? Score 8 divines not in the model."""
import sys
exec(open('/home/claude/strata-casket/data-b002/genre_matched.py').read().split("print('\\nGENRE-MATCHED")[0])
from corpora import raw, clean
full={b:profile(b) for b in AUTH}
def zrow(tok): return [(v-m)/s for v,m,s in zip(freqs(tok),mu,sd)]
CONTROLS={'A45397':'Hammond 1655','A57134':'Reynolds 1642','A01344':'Fuller 1640','A02549':'Hall 1641','A64646':'Ussher 1643','A62025':'Sanderson 1647','A26864':'Baxter 1654','A31927':'Calamy 1652'}
cands=['charles_formal','henderson','gauden','taylor','milton']
tally={}
print('CONTROL DIVINES (not in model), 2,000-word samples x up to 3 per work:')
for id,name in CONTROLS.items():
    tok=norm_tokens(clean(raw(id)))
    for s in range(0,min(len(tok)-2000,6000)+1,2000):
        z=zrow(tok[s:s+2000]); d={b:delta(z,full[b]) for b in cands}; best=min(d,key=d.get)
        tally[best]=tally.get(best,0)+1
        print(f'  {name:15s} @{s:5d}: -> {best:15s} '+' '.join(f'{b[:6]}={d[b]:.3f}' for b in cands))
print('tally:',tally)
