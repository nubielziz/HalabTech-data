"""Pairwise sibling analysis among priced servers on HalabTech-named SKUs (loose-normalised names)."""
import json, re, sys, html, statistics, csv
from collections import defaultdict, OrderedDict
W6, R7, GEN = sys.argv[1], sys.argv[2], sys.argv[3]
ns = {}
code = open(GEN).read()
pre = code.split('# ---- other servers')[0]
exec(pre, ns)   # defines SOURCES, ex, lo, ht_svcs ...
SOURCES, ex, lo, ht_svcs = ns['SOURCES'], ns['ex'], ns['lo'], ns['ht_svcs']
ht = {}
for s in ht_svcs:
    if s['price']:
        ht.setdefault(lo(s['service']), s['price'])
prices = OrderedDict([('HALABTECH', ht)])
for name, refs in SOURCES.items():
    m = {}; cnt = defaultdict(int)
    for f, idx in refs:
        try: d = json.load(open(W6 + '/parsed/' + f))
        except Exception: continue
        if idx >= len(d['pages']): continue
        for s in d['pages'][idx]['services']:
            nm = ex(s['service']); dl = ex(s.get('delivery', ''))
            if dl and nm.endswith(' ' + dl): nm = nm[:-len(dl) - 1]
            k = lo(nm)
            if k not in ht or not s.get('price'): continue
            cnt[k] += 1; m[k] = float(s['price'])
    m = {k: v for k, v in m.items() if cnt[k] == 1}
    if len(m) >= 5: prices[name] = m
names = list(prices)
rows = []
for i, a in enumerate(names):
    for b in names[i + 1:]:
        sh = set(prices[a]) & set(prices[b])
        if len(sh) < 5: continue
        r = sorted(prices[b][k] / prices[a][k] for k in sh)
        med = statistics.median(r)
        w3 = sum(1 for x in r if abs(x / med - 1) <= 0.03)
        b_cheaper = sum(1 for x in r if x < 0.995)
        rows.append({'a': a, 'b': b, 'shared_ht_skus': len(sh), 'median_ratio_b_over_a': round(med, 4), 'within3pct': w3, 'within3pct_frac': round(w3 / len(r), 3), 'b_cheaper': b_cheaper, 'b_cheaper_frac': round(b_cheaper / len(r), 3)})
rows.sort(key=lambda x: (-x['shared_ht_skus']))
with open(W6 + '/pairwise_price_ratios.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); [w.writerow(r) for r in rows]
for r in rows: print(r)
