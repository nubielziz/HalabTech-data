"""Overlap among HalabTech-mirror candidates, inside and outside HalabTech's current catalog."""
import json, sys, csv
W6, R7, GEN = sys.argv[1], sys.argv[2], sys.argv[3]
ns = {}; exec(open(GEN).read().split('# ---- other servers')[0], ns)
SOURCES, ex, lo, ht_svcs = ns['SOURCES'], ns['ex'], ns['lo'], ns['ht_svcs']
htset = {lo(s['service']) for s in ht_svcs}
sets = {}
for name in ['mwunlocker.com', 'gsmtiger.com', 'reunlocker.com', 'univgsm.com', 'saudi-gsm.com', 'unlockspro.com', 'idunlocker.com', 'gxunlocker.com', 'code-gsm.com', 'gsmnigeria.com']:
    st = set()
    for f, idx in SOURCES[name]:
        d = json.load(open(W6 + '/parsed/' + f))
        if idx >= len(d['pages']): continue
        for s in d['pages'][idx]['services']:
            nm = ex(s['service']); dl = ex(s.get('delivery', ''))
            if dl and nm.endswith(' ' + dl): nm = nm[:-len(dl) - 1]
            st.add(lo(nm))
    sets[name] = st
names = list(sets)
rows = []
for i, a in enumerate(names):
    for b in names[i + 1:]:
        A, B = sets[a], sets[b]
        inter = A & B
        rows.append({'a': a, 'b': b, 'shared_all': len(inter), 'shared_in_HT': len(inter & htset), 'shared_not_in_HT': len(inter - htset), 'jaccard_all': round(len(inter) / max(1, len(A | B)), 3)})
with open(W6 + '/mirror_cluster_overlap.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); [w.writerow(r) for r in rows]
for r in sorted(rows, key=lambda r: -r['shared_not_in_HT'])[:20]: print(r)
