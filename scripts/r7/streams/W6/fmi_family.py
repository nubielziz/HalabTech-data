"""Model-key matching for iPad/iWatch FMI OFF families (names differ in decoration across servers)."""
import json, re, sys, statistics
W6, R7 = sys.argv[1], sys.argv[2]
def key(n):
    s = n.lower()
    if 'fmi off' not in s: return None
    s = re.sub(r'\[[^\]]*\]', ' ', s); s = s.replace('iremove', ' ')
    s = re.sub(r'wi-?fi( model)?( only)?|\(wi-fi only\)', ' ', s)
    s = s.replace('for iwatch', 'iwatch').replace('iwatch series se', 'iwatch se').replace('series ', '')
    s = re.sub(r'(\d)(st|nd|rd|th) ?gen(eration)?', r'\1', s)
    s = re.sub(r'\bgen(eration)?\b', ' ', s)
    s = re.sub(r'ipad15,5 - ', '', s)
    s = re.sub(r'[^a-z0-9]+', ' ', s).strip()
    s = s.replace('fmi off ', '').replace(' model only', '').replace(' only', '')
    s = re.sub(r'\s+', ' ', s).replace('ipad pro 11 a16', 'ipad 11 a16').replace('ipad air 11 m3 ', 'ipad air 11 inch m3 ')
    s = s.replace('ipad air 11 m3', 'ipad air 11 inch m3').replace('ipad air 13 m3', 'ipad air 13 inch m3')
    s = s.replace('ipad mini 7 a17 pro', 'ipad mini 7 a17 pro')
    return s.strip()
ht = {}
for s in json.load(open(R7 + '/imei_catalog_1003.json'))['services']:
    k = key(s['service'])
    if k and s.get('price_usd'):
        ht.setdefault(k, (s['service'], s['price_usd']))
out = {}
for label, f, idx in [('code-gsm.com', 'codegsm_live_fc.json', 0), ('gsmnigeria.com', 'fc_gsmnigeria_live.json', 0), ('univgsm.com', 'b3_tiger_univ_exa.json', 2), ('cleanunlocker.com', 'b6_clean_ua_exa.json', 0), ('dmunlocker.com', 'b7_dm_rgsm_exa.json', 0), ('saudi-gsm.com', 'b5_idunl_saudi_exa.json', 2)]:
    pg = json.load(open(W6 + '/parsed/' + f))['pages'][idx]
    pairs = []
    seen = set()
    for s in pg['services']:
        k = key(s['service'])
        if not k or k not in ht or not s.get('price') or k in seen: continue
        seen.add(k)
        h = ht[k]
        pairs.append((k, h[1], s['price'], round(h[1] - s['price'], 2), round(s['price'] / h[1], 3)))
    out[label] = pairs
    if pairs:
        diffs = [p[3] for p in pairs]
        print(label, 'matched', len(pairs), 'HT-other diff median', statistics.median(diffs), 'cheaper_than_HT', sum(1 for p in pairs if p[2] < p[1] - 0.005), 'diff counts', sorted(__import__('collections').Counter(diffs).items())[:12])
json.dump(out, open(W6 + '/fmi_family_pairs.json', 'w'), indent=1)
for p in out['code-gsm.com']: print('  CG', p)
