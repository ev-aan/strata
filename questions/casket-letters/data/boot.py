exec(open('compare.py').read().split("results={}")[0])
import collections
k=3; B=30
print('equal-size corpora per resample:',n,'chunks ≈',n*60,'words')
names=list(C)
R=collections.defaultdict(list); shared=collections.defaultdict(collections.Counter)
for b in range(B):
    Ms=random.sample(M,n); Ks=random.sample(K,n)
    Mi=index(Ms,k); Ki=index(Ks,k)
    for nm in names:
        g=ngr(norm(C[nm]),k)
        m=len(g&Mi)/len(g); c=len(g&Ki)/len(g)
        R[nm].append((m+1e-3)/(c+1e-3))
        for x in g&Mi: shared[nm][' '.join(x)]+=1
def q(v,p): v=sorted(v); return v[int(p*(len(v)-1))]
for nm in names:
    v=R[nm]; print(f'{nm:8s} median ratio {st.median(v):.2f}  90% range {q(v,.05):.2f}–{q(v,.95):.2f}')
cal={'Mary':[],'Catherine':[]}
for who,src in (('Mary',M),('Catherine',K)):
    for t in range(60):
        j=random.randrange(20,len(src)-30); held=sum(src[j:j+7],[])
        rest=src[:j-15]+src[j+22:]; other=K if who=='Mary' else M
        sm=random.sample(rest if who=='Mary' else other, n-40); sk=random.sample(other if who=='Mary' else rest, n-40)
        g=ngr(held,k); m=len(g&index(sm,k))/len(g); c=len(g&index(sk,k))/len(g)
        cal[who].append((m+1e-3)/(c+1e-3))
for who,v in cal.items():
    right=sum((x>1) if who=='Mary' else (x<1) for x in v)
    print(f'calibration {who:9s}: median {st.median(v):.2f}, 90% range {q(v,.05):.2f}–{q(v,.95):.2f}, correct {right}/60, ratio>=3: {sum(x>=3 for x in v)}/60')
for nm in ['III','VI','IV']:
    print(nm,'most frequent phrases shared with Mary:',[p for p,_ in shared[nm].most_common(8)])
