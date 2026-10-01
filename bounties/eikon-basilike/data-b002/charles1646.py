"""Extract Charles I's own 1646 letters from Bruce (ed.), Charles I in 1646 (Camden Society, 1856), IA: charlesiinlette00chargoog."""
import re, json, sys
L=open('charlesiinlette00chargoog.txt',errors='ignore').read().split('\n')
start=next(i for i,l in enumerate(L) if re.match(r'Dear(e)? ?[Hh]eart',l.strip()))-3
end=next((i for i,l in enumerate(L) if i>start and re.match(r'^(APPENDIX|INDEX)\b',l.strip())),len(L))
out=[];infoot=False
for l in L[start:end]:
    s=l.strip()
    if re.match(r'^(\*|t|J|§|\|\|)\s',s) and len(s)>20: infoot=True   # footnote start
    if s=='' : infoot=False; continue
    if infoot: continue
    if re.search(r'CHARLES I\. IN 1646|CAMD\. SOC|^Digitized|by Google',s): continue
    if re.fullmatch(r'[\dA-Z ]{1,6}',s): continue
    out.append(s)
txt=' '.join(out)
print(len(txt.split()),'words'); print(txt[:400]); print('...'); print(txt[-300:])
json.dump({'charles1646':txt},open('charles1646.json','w'))
