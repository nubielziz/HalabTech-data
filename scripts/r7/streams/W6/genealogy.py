"""Catalog genealogy metrics: each captured server vs HalabTech (10:03 UTC snapshot).
python3 -I genealogy.py <W6 raw dir> <r7 raw dir>
Writes: <W6>/genealogy_metrics.csv, <W6>/genealogy_detail.json
"""
import json, re, sys, csv, html, statistics
from collections import Counter, defaultdict, OrderedDict

W6, R7 = sys.argv[1], sys.argv[2]
P = W6 + '/parsed/'

SOURCES = OrderedDict([
    ('unlockspro.com',      [('b1_unlockspro_codegsm_exa.json', 0), ('b1_unlockspro_codegsm_exa.json', 1)]),
    ('code-gsm.com',        [('codegsm_live_fc.json', 0)]),
    ('code-gsm.com(exa-cache)', [('b1_unlockspro_codegsm_exa.json', 2)]),
    ('best4unlock.us',      [('best4unlock_exa.json', 0), ('best4unlock_exa.json', 1)]),
    ('mwunlocker.com',      [('b2_mw_axiom_exa.json', 0), ('b2_mw_axiom_exa.json', 1)]),
    ('gsmtiger.com',        [('b8_fix4_tiger_exa.json', 2), ('b8_fix4_tiger_exa.json', 3)]),
    ('univgsm.com',         [('b3_tiger_univ_exa.json', 2), ('b3_tiger_univ_exa.json', 3)]),
    ('reunlocker.com',      [('b4_reunl_mrunl_exa.json', 0), ('b4_reunl_mrunl_exa.json', 1)]),
    ('mrunlockers.com',     [('b4_reunl_mrunl_exa.json', 2), ('b4_reunl_mrunl_exa.json', 3)]),
    ('gsmunlockinfo.com',   [('gsmunlockinfo_exa.json', 0), ('gsmunlockinfo_exa.json', 1)]),
    ('wardserver.com',      [('wardserver_exa.json', 0), ('wardserver_exa.json', 1)]),
    ('idunlocker.com',      [('b5_idunl_saudi_exa.json', 0), ('b5_idunl_saudi_exa.json', 1)]),
    ('saudi-gsm.com',       [('b5_idunl_saudi_exa.json', 2), ('b5_idunl_saudi_exa.json', 3)]),
    ('cleanunlocker.com',   [('b6_clean_ua_exa.json', 0), ('b6_clean_ua_exa.json', 1)]),
    ('unlock-ua.com',       [('b6_clean_ua_exa.json', 2), ('b6_clean_ua_exa.json', 3)]),
    ('dmunlocker.com',      [('b7_dm_rgsm_exa.json', 0), ('b7_dm_rgsm_exa.json', 1)]),
    ('rgsmrio.in',          [('b7_dm_rgsm_exa.json', 2), ('b7_dm_rgsm_exa.json', 3)]),
    ('fix4gsm.com',         [('b8_fix4_tiger_exa.json', 0), ('b8_fix4_tiger_exa.json', 1)]),
])
EXTRA = json.load(open(W6 + '/extra_sources.json')) if __import__('os').path.exists(W6 + '/extra_sources.json') else {}
for k, v in EXTRA.items():
    SOURCES[k] = [tuple(x) for x in v]


def fixmoji(s):
    if re.search(r'[Â-ð][\u0080-¿]', s or ''):
        for enc in ('latin-1', 'cp1252'):
            try:
                return s.encode(enc).decode('utf-8')
            except Exception:
                pass
    return s


def ex(s):
    s = fixmoji(html.unescape(s or '')).replace('﻿', '').replace('​', '')
    s = s.replace('\\[', '[').replace('\\]', ']').replace('\\#', '#').replace('\\|', '|')
    s = re.sub(r'\s*\|\s*', ' | ', s)
    return re.sub(r'\s+', ' ', s).strip()


IDPFX = re.compile(r'^(?:#\s*\d{2,6}\s*[-:|]?\s*|\d{2,6}\s*#\s*[-:|]?\s*|\d{3,6}\s*[-:|]\s+)')


def lo(s):
    s = ex(s).lower()
    s = IDPFX.sub('', s)
    return re.sub(r'[\W_]+', '', s)


def load_ht():
    out = {}
    for kind, f in (('imei', 'imei_catalog_1003.json'), ('server', 'server_catalog_1003.json')):
        d = json.load(open(R7 + '/' + f))
        out[kind] = d
    return out


HT = load_ht()
ht_svcs = []
for kind in ('imei', 'server'):
    for i, s in enumerate(HT[kind]['services']):
        ht_svcs.append({'kind': kind, 'pos': i, 'group': ex(s['group']), 'service': ex(s['service']), 'price': s.get('price_usd'), 'icon': s.get('icon', '')})
ht_groups = {k: list(OrderedDict.fromkeys(ex(g['name']) for g in HT[k]['groups'])) for k in ('imei', 'server')}

# ---- other servers
servers = OrderedDict()
for name, refs in SOURCES.items():
    svcs = []
    urls = []
    for f, idx in refs:
        try:
            d = json.load(open(P + f))
        except Exception as e:
            print('missing', f, e); continue
        if idx >= len(d['pages']):
            continue
        pg = d['pages'][idx]
        urls.append(pg['url'])
        for j, s in enumerate(pg['services']):
            nm = ex(s['service']); dl = ex(s.get('delivery', ''))
            if dl and nm.endswith(' ' + dl) and len(nm) > len(dl) + 3:
                nm = nm[:-len(dl) - 1].rstrip()
            svcs.append({'kind': pg['kind'], 'pos': j, 'group': ex(s['group']), 'service': nm, 'price': s.get('price'), 'icon': s.get('icon', ''), 'delivery': dl})
    servers[name] = {'urls': urls, 'services': svcs}

# ---- typo detector (data-driven): HalabTech tokens with edit distance <=2 to a 10x more frequent corpus token
corpus = Counter()
for nm, sv in servers.items():
    for s in sv['services']:
        for t in set(re.findall(r'[A-Za-z]{5,}', s['service'] + ' ' + s['group'])):
            corpus[t.lower()] += 1
for s in ht_svcs:
    for t in set(re.findall(r'[A-Za-z]{5,}', s['service'] + ' ' + s['group'])):
        corpus[t.lower()] += 1


def ed(a, b, cap=2):
    if abs(len(a) - len(b)) > cap:
        return cap + 1
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i] + [0] * len(b)
        for j, cb in enumerate(b, 1):
            cur[j] = min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb))
            if i > 1 and j > 1 and ca == b[j - 2] and a[i - 2] == cb:
                cur[j] = min(cur[j], prev[j - 2] + 1 if False else cur[j])
        prev = cur
    return prev[-1]


ht_tokens = Counter()
for s in ht_svcs:
    for t in set(re.findall(r'[A-Za-z]{5,}', s['service'] + ' ' + s['group'])):
        ht_tokens[t.lower()] += 1
common = [u for u, c in corpus.items() if c >= 25]
typo_candidates = {}
for t in ht_tokens:
    ft = corpus[t]
    if ft > 400:
        continue
    for u in common:
        if u == t or corpus[u] < 10 * ft or len(u) < 5:
            continue
        if u.startswith(t) or t.startswith(u):
            continue
        d = ed(t, u)
        if d <= (1 if len(t) < 7 else 2):
            typo_candidates[t] = (u, ft, corpus[u])
            break

CURATED = ['netowrk', 'miniutes', 'sevice', 'prheck', 'انتببه', 'byass', 'actiavtion', 'sliver', 'eligibilty', 'netwotk', 'bussiness',
           'degits', 'sucess', 'permenant', 'distirbutor', 'premuim', 'genirc', 'untethred', 'lisence', 'unvirsal', 'premiume', 'infinitry']


def has_tok(text, tok):
    if re.search(r'[؀-ۿ]', tok):
        return tok in text
    return re.search(r'(?<![a-z])' + re.escape(tok) + r'(?![a-z])', text.lower()) is not None


def kendall_tau(seq_a, seq_b):
    # seq_a/seq_b: same items in different orders
    pos_b = {x: i for i, x in enumerate(seq_b)}
    arr = [pos_b[x] for x in seq_a]
    n = len(arr)
    if n < 3:
        return None
    conc = disc = 0
    for i in range(n):
        for j in range(i + 1, n):
            if arr[i] < arr[j]:
                conc += 1
            else:
                disc += 1
    return (conc - disc) / (conc + disc)


def lcs_len(a, b):
    if not a or not b:
        return 0
    prev = [0] * (len(b) + 1)
    for x in a:
        cur = [0]
        for j, y in enumerate(b, 1):
            cur.append(prev[j - 1] + 1 if x == y else max(prev[j], cur[j - 1]))
        prev = cur
    return prev[-1]


ht_ex_imei = {s['service'] for s in ht_svcs if s['kind'] == 'imei'}
ht_ex_srv = {s['service'] for s in ht_svcs if s['kind'] == 'server'}
ht_lo_imei = {lo(s['service']) for s in ht_svcs if s['kind'] == 'imei'}
ht_lo_srv = {lo(s['service']) for s in ht_svcs if s['kind'] == 'server'}
ht_by_lo = defaultdict(list)
for s in ht_svcs:
    ht_by_lo[lo(s['service'])].append(s)
ht_grp_lo = {k: {lo(g) for g in v} for k, v in ht_groups.items()}

rows = []
detail = {}
for name, sv in servers.items():
    S = sv['services']
    if not S:
        rows.append({'server': name, 'note': 'no services parsed'}); continue
    ex_set = {s['service'] for s in S}
    lo_set = {lo(s['service']) for s in S}
    grp_order = list(OrderedDict.fromkeys(s['group'] for s in S))
    grp_lo = {lo(g) for g in grp_order}
    ex_imei = ht_ex_imei & ex_set
    ex_srv = ht_ex_srv & ex_set
    lo_imei = ht_lo_imei & lo_set
    lo_srv = ht_lo_srv & lo_set
    g_imei = [g for g in ht_groups['imei'] if lo(g) in grp_lo]
    g_srv = [g for g in ht_groups['server'] if lo(g) in grp_lo]
    # ordering of shared IMEI groups (HalabTech order vs server order)
    other_order = [lo(g) for g in grp_order]
    shared_imei_lo = [lo(g) for g in ht_groups['imei'] if lo(g) in grp_lo]
    seq_other = [g for g in OrderedDict.fromkeys(other_order) if g in set(shared_imei_lo)]
    tau_imei = kendall_tau(shared_imei_lo, seq_other) if len(shared_imei_lo) >= 3 else None
    lcs_imei = lcs_len(shared_imei_lo, seq_other)
    shared_srv_lo = [lo(g) for g in ht_groups['server'] if lo(g) in grp_lo]
    seq_other_s = [g for g in OrderedDict.fromkeys(other_order) if g in set(shared_srv_lo)]
    tau_srv = kendall_tau(shared_srv_lo, seq_other_s) if len(shared_srv_lo) >= 3 else None
    # branding
    branded = [s for s in S if re.search(r'halab\s*tech', s['service'] + ' ' + s['group'], re.I)]
    branded_groups = sorted({s['group'] for s in branded if re.search(r'halab\s*tech', s['group'], re.I)})
    # typos
    typo_hits = {}
    for tok in CURATED + ['exisitng', 'exisit', 'genric', 'insant', 'interet', 'monthes', 'packge', 'renewel', 'samasung', 'eligiblity', 'supper', 'bussiness', 'infomation', 'permanant', 'descriptoin']:
        n = sum(1 for s in S if has_tok(s['service'] + ' || ' + s['group'], tok))
        if n:
            typo_hits[tok] = n
    # price relationship on loose-matched SKUs (unique on both sides)
    pairs = []
    cnt_other = Counter(lo(s['service']) for s in S)
    for s in S:
        k = lo(s['service'])
        if s['price'] is None or k not in ht_by_lo or cnt_other[k] != 1 or len(ht_by_lo[k]) != 1:
            continue
        h = ht_by_lo[k][0]
        if h['price'] in (None, 0) or s['price'] == 0:
            continue
        pairs.append({'service': h['service'], 'ht_group': h['group'], 'other_group': s['group'], 'ht': h['price'], 'other': s['price'], 'ratio': round(s['price'] / h['price'], 4), 'diff': round(s['price'] - h['price'], 3), 'kind': h['kind']})
    ratios = [p['ratio'] for p in pairs]
    med = statistics.median(ratios) if ratios else None
    within2 = sum(1 for r in ratios if med and abs(r / med - 1) <= 0.02) if ratios else 0
    cheaper = sum(1 for r in ratios if r < 0.995)
    dearer = sum(1 for r in ratios if r > 1.005)
    equal = len(ratios) - cheaper - dearer
    ratio_mode = Counter(round(r, 2) for r in ratios).most_common(3)
    icons = sorted({s['icon'].rsplit('/', 1)[-1] for s in S if s.get('icon')})
    row = {
        'server': name, 'urls': ' '.join(sv['urls']),
        'n_imei': sum(1 for s in S if s['kind'] == 'imei'), 'n_server': sum(1 for s in S if s['kind'] == 'server'),
        'n_groups': len(grp_order), 'priced': sum(1 for s in S if s['price'] is not None),
        'exact_imei': len(ex_imei), 'exact_imei_pct': round(100 * len(ex_imei) / len(ht_ex_imei), 1),
        'exact_server': len(ex_srv), 'exact_server_pct': round(100 * len(ex_srv) / len(ht_ex_srv), 1),
        'loose_imei': len(lo_imei), 'loose_imei_pct': round(100 * len(lo_imei) / len(ht_lo_imei), 1),
        'loose_server': len(lo_srv), 'loose_server_pct': round(100 * len(lo_srv) / len(ht_lo_srv), 1),
        'grp_imei': len(g_imei), 'grp_imei_pct': round(100 * len(g_imei) / len(ht_groups['imei']), 1),
        'grp_server': len(g_srv), 'grp_server_pct': round(100 * len(g_srv) / len(ht_groups['server']), 1),
        'tau_imei_groups': None if tau_imei is None else round(tau_imei, 3), 'lcs_imei_groups': lcs_imei,
        'tau_server_groups': None if tau_srv is None else round(tau_srv, 3),
        'halabtech_branded_items': len(branded), 'halabtech_branded_groups': ' ; '.join(branded_groups),
        'typo_hits': json.dumps(typo_hits, ensure_ascii=False),
        'price_pairs': len(pairs), 'ratio_median': None if med is None else round(med, 4),
        'ratio_within2pct_of_median': within2, 'cheaper_than_ht': cheaper, 'equal_to_ht': equal, 'dearer_than_ht': dearer,
        'ratio_modes': json.dumps(ratio_mode), 'icons_n': len(icons), 'miniutes_in_delivery': sum(1 for s in S if 'miniutes' in (s.get('delivery') or '').lower()),
    }
    rows.append(row)
    detail[name] = {'pairs': pairs, 'g_imei': g_imei, 'g_srv': g_srv, 'ex_imei': sorted(ex_imei), 'ex_srv': sorted(ex_srv),
                    'lo_imei_only': sorted(lo_imei - {lo(x) for x in ex_imei}), 'branded': [(s['group'], s['service'], s['price']) for s in branded][:60],
                    'icons': icons, 'grp_order': grp_order[:400]}

fields = list(rows[0].keys())
with open(W6 + '/genealogy_metrics.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=fields)
    w.writeheader()
    for r in rows:
        w.writerow({k: r.get(k, '') for k in fields})
json.dump({'typo_candidates': typo_candidates, 'detail': detail}, open(W6 + '/genealogy_detail.json', 'w'), ensure_ascii=False, indent=1)
for r in rows:
    print({k: r.get(k) for k in ['server', 'n_imei', 'n_server', 'exact_imei', 'exact_imei_pct', 'loose_imei', 'exact_server', 'loose_server', 'grp_imei', 'grp_server', 'tau_imei_groups', 'halabtech_branded_items', 'price_pairs', 'ratio_median', 'ratio_within2pct_of_median', 'cheaper_than_ht', 'equal_to_ht', 'dearer_than_ht']})
print('typo candidates:', {k: v for k, v in sorted(typo_candidates.items())})
