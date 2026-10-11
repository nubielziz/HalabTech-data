"""Infer upstream cost and markup from HalabTech prices.
A price with >=3 decimals is almost certainly computed (cost x multiplier) by Dhru's pricing rules.
For each such SKU, find multipliers m (common Dhru percentage steps) for which cost = price/m has <=2 decimals.
Within a group, a multiplier shared by all 3-decimal SKUs is the group's inferred markup.
"""
import json, sys, collections
from decimal import Decimal, ROUND_HALF_UP
cat = json.load(open(sys.argv[1])); out = sys.argv[2]
MULTS = [Decimal(str(round(1 + i / 1000, 3))) for i in range(5, 301, 5)]   # 1.005 .. 1.300
rows = []
by_group = collections.defaultdict(list)
for s in cat['services']:
    p = s['price_usd']
    if p is None or p == 0:
        continue
    raw = s['price_raw'].replace('$', '').replace(',', '').strip()
    dec = len(raw.split('.')[1]) if '.' in raw else 0
    P = Decimal(raw)
    cands = []
    if dec >= 3:
        for m in MULTS:
            c = P / m
            if c == c.quantize(Decimal('0.01')):
                cands.append((str(m), str(c.quantize(Decimal('0.01')))))
    rows.append({'group': s['group'], 'service': s['service'], 'price': raw, 'decimals': dec, 'candidates': cands})
    by_group[s['group']].append(rows[-1])
summary = []
for g, items in by_group.items():
    three = [r for r in items if r['decimals'] >= 3]
    if not three:
        summary.append({'group': g, 'skus': len(items), 'computed_skus': 0, 'shared_multipliers': [], 'implied_costs': {}})
        continue
    sets = [set(m for m, _ in r['candidates']) for r in three]
    shared = sorted(set.intersection(*sets), key=float) if all(sets) else []
    implied = {}
    if shared:
        # prefer the multiplier giving the most "round" costs (integers / .x0 / .x5)
        def roundness(m):
            sc = 0
            for r in three:
                c = Decimal(r['price']) / Decimal(m)
                if c == c.quantize(Decimal('1')): sc += 3
                elif (c * 20) == (c * 20).quantize(Decimal('1')): sc += 2
                elif (c * 10) == (c * 10).quantize(Decimal('1')): sc += 1
            return sc
        best = max(shared, key=lambda m: (roundness(m), -abs(float(m) - 1.1)))
        implied = {r['service']: str((Decimal(r['price']) / Decimal(best)).quantize(Decimal('0.01'))) for r in three}
    else:
        best = None
    summary.append({'group': g, 'skus': len(items), 'computed_skus': len(three), 'shared_multipliers': shared[:12], 'best_multiplier': best, 'implied_costs': implied})
json.dump({'rows': rows, 'groups': summary}, open(out, 'w'), ensure_ascii=False, indent=1)
tot = len(rows); comp = sum(1 for r in rows if r['decimals'] >= 3)
print('SKUs with price', tot, '| computed (>=3 decimals)', comp)
g_with = [s for s in summary if s['computed_skus']]
print('groups with computed SKUs', len(g_with), '| groups with a shared multiplier', sum(1 for s in g_with if s.get('best_multiplier')))
mc = collections.Counter(s.get('best_multiplier') for s in g_with if s.get('best_multiplier'))
print('best multipliers:', mc.most_common(12))
