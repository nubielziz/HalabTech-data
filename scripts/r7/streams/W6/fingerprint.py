"""Match HalabTech implied upstream costs (markup_*.json) against other servers' public prices for the same SKU."""
import json, re, sys, html
from collections import defaultdict, Counter
W6, R7 = sys.argv[1], sys.argv[2]
sys.path.insert(0, '')
def ex(s):
    s = html.unescape(s or '')
    s = re.sub(r'\s*\|\s*', ' | ', s); return re.sub(r'\s+', ' ', s).strip()
IDP = re.compile(r'^(?:#\s*\d{2,6}\s*[-:|]?\s*|\d{2,6}\s*#\s*[-:|]?\s*)')
def lo(s):
    s = ex(s).lower(); s = IDP.sub('', s); return re.sub(r'[\W_]+', '', s)
fp = {}
for f in ('markup_imei.json', 'markup_server.json'):
    d = json.load(open(R7 + '/' + f))
    best = {}
    for g in d['groups']:
        for svc, cost in (g.get('implied_costs') or {}).items():
            best[lo(svc)] = (g.get('best_multiplier'), float(cost))
    for r in d['rows']:
        k = lo(r['service'])
        fp[k] = {'service': r['service'], 'group': r['group'], 'ht_price': float(r['price']), 'cands': [(float(m), float(c)) for m, c in r.get('candidates', [])], 'best': best.get(k), 'kind': f.split('_')[1][:-5]}
print('HalabTech computed-price SKUs with fingerprints:', len(fp))
# load all parsed other-server catalogs via genealogy SOURCES
import importlib.util
G = json.load(open(W6 + '/genealogy_detail.json'))
src = {}
exec(open(sys.argv[3]).read().split('# ---- other servers')[0].split("W6, R7 = sys.argv[1], sys.argv[2]")[1].split('def ex(')[0], {'OrderedDict': __import__('collections').OrderedDict, 'json': json, 'W6': W6, '__import__': __import__}, src)
SOURCES = src['SOURCES']
hits = []
summary = defaultdict(Counter)
for name, refs in SOURCES.items():
    for f, idx in refs:
        try:
            d = json.load(open(W6 + '/parsed/' + f))
        except Exception:
            continue
        if idx >= len(d['pages']): continue
        for s in d['pages'][idx]['services']:
            nm = ex(s['service']); dl = ex(s.get('delivery', ''))
            if dl and nm.endswith(' ' + dl): nm = nm[:-len(dl) - 1]
            k = lo(nm)
            if k not in fp or s.get('price') in (None, 0): continue
            F = fp[k]; p = float(s['price'])
            summary[name]['compared'] += 1
            match = None
            for m, c in ([F['best']] if F['best'] else []) + F['cands']:
                if m is None: continue
                if abs(p - c) <= max(0.011, 0.005 * c):
                    match = (m, c); break
            rel = 'equal_HT' if abs(p - F['ht_price']) <= 0.005 * F['ht_price'] else ('below_HT' if p < F['ht_price'] else 'above_HT')
            summary[name][rel] += 1
            if match:
                summary[name]['equals_implied_cost'] += 1
                hits.append({'server': name, 'service': F['service'], 'group': F['group'], 'ht_price': F['ht_price'], 'server_price': p, 'implied_cost': match[1], 'ht_multiplier': match[0], 'kind': F['kind']})
for n, c in summary.items():
    print(n, dict(c))
json.dump({'hits': hits, 'summary': {k: dict(v) for k, v in summary.items()}}, open(W6 + '/implied_cost_matches.json', 'w'), ensure_ascii=False, indent=1)
for h in hits: print(' HIT', h['server'], '|', h['group'][:30], '|', h['service'][:70], '| HT', h['ht_price'], '| srv', h['server_price'], '| cost', h['implied_cost'], 'x', h['ht_multiplier'])
