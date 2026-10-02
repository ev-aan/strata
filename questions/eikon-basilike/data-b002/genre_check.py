"""Strata B-002, finding F7: does the Charles profile detect Charles, or just 'letters'? Score known non-Charles letters."""
import re, json, sys
sys.path.insert(0,'/home/claude/strata-casket/data-b002')
exec(open('/home/claude/strata-casket/data-b002/delta.py').read().split('# calibration')[0])
from corpora import raw, clean, strip_attest
fullcents={b:centroid([Z[j] for j,c in enumerate(chunks) if c[0]==b]) for b in AUTH}
def score(name,txt):
    tok=norm_tokens(txt); z=[(v-m)/s for v,m,s in zip(freqs(tok,MFW),mu,sd)]
    d={b:round(delta(z,fullcents[b]),3) for b in AUTH}
    print(f'  {name:52s} {len(tok):5d}w  {d}  -> {min(d,key=d.get)}')
c=raw('A31932'); letters=re.findall(r'(<div[^>]*type="letter"[^>]*>.*?</div>)',c,flags=re.S)
queen=' '.join(strip_attest(clean(letters[i])) for i in [26,28,29,30,31,32])
others=' '.join(strip_attest(clean(letters[i])) for i in [19,20,24,25,33,38])
print('KNOWN NON-CHARLES TEXTS:')
score("Queen Henrietta Maria's letters (1645 Cabinet)",queen)
score('Other papers in the Cabinet (petitions, instructions)',others)
score('Jeremy Taylor, letter to a gentlewoman (A63729)',clean(raw('A63729')))
score("Gauden, Religious & Loyal Protestation (open letter, 1649)",D['gauden']['A42492'])
