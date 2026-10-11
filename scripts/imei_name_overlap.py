import re,sys
def norm(s):
    s=s.lower()
    s=re.sub(r'^#\d+\s*','',s.strip())
    s=s.replace('{','[').replace('}',']')
    s=re.sub(r'[^a-z0-9]+','',s)
    return s
ht=[l.split(' | ') for l in open(sys.argv[1]) if l.strip()]
htn={}
for p in ht:
    if len(p)>=4:
        name=' | '.join(p[1:-2])
        htn[norm(name)[:60]]=(p[0],name)
other=open(sys.argv[2]).read()
names=[]
for line in other.splitlines():
    cells=[c.strip() for c in line.split('|')]
    cells=[c for c in cells if c]
    if len(cells)>=2 and cells[-1] not in ('Delivery Time','---'):
        names.append(' | '.join(cells[:-1]))
on={norm(n)[:60]:n for n in names}
hits=[(htn[k][0],htn[k][1],on[k]) for k in htn if k in on]
print('HalabTech names:',len(htn),'other names:',len(on),'exact-prefix matches:',len(hits))
from collections import Counter
c=Counter(h[0] for h in hits)
for g,n in c.most_common(): print(n,g)
if len(sys.argv)>3:
    for h in hits: print(' -',h[0],'||',h[2][:110])
