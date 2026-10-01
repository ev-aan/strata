import re
L=open('henderson.txt',errors='ignore').read().split('\n')
sections={'III':(10011,10372),'IV':(10372,10968),'V':(10968,11160),'VI':(11160,11571)}
fr=set("de la le les que qui je vous ne pas et en du des mon ma mes est a au il me ce se sa son pour sans avec plus mais ou si luy moy tout tant comme".split())
sc=set("the and of to that is my zour zow ye yat quhilk it in be with for his he not sa ane gif bot or this".split())
la=set("quod ut ad cum non sed tibi mihi ego quae eius esse".split())
def lang(line):
    w=re.findall(r"[a-zà-ÿ']+",line.lower())
    if len(w)<2: return None
    f=sum(x in fr for x in w); s=sum(x in sc for x in w); l=sum(x in la for x in w)
    if f>s and f>l: return 'fr'
    if s>f: return 'sc'
    if l>f: return 'la'
    return None
out={}
for k,(a,b) in sections.items():
    seg=L[a:b]
    # split into pages on 'Digitized'
    pages=[];cur=[]
    for l in seg:
        if 'Digitized' in l: pages.append(cur);cur=[]
        else: cur.append(l)
    pages.append(cur)
    orig=[]
    for pg in pages:
        # blocks separated by >=2 blank lines
        blocks=[];bl=[];blank=0
        for l in pg:
            if l.strip()=='' : blank+=1
            else:
                if blank>=2 and bl: blocks.append(bl);bl=[]
                blank=0; bl.append(l)
        if bl: blocks.append(bl)
        frb=[blk for blk in blocks if sum(lang(x)=='fr' for x in blk)>=max(2,len(blk)//2)]
        if not frb: continue
        if k=='III': chosen=frb
        else: chosen=frb[:1] if len(frb)>=2 else frb  # first French column = original
        for blk in chosen: orig+= [x for x in blk if lang(x)=='fr' or (lang(x) is None and len(x.strip())>3)]
    txt=' '.join(orig).replace('- ','')
    out[k]=txt
    print('=====',k,len(txt.split()),'words'); print(txt[:600]); print('...'); print(txt[-300:])
import json; json.dump(out,open('casket_fr.json','w'),ensure_ascii=False)
