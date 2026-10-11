"""Round-7 curation engine: builds the sheet spec for build_r7.py and a metrics JSON for the summary report.

Inputs (read-only): R6 workbook, catalogs (02:00 repo copy, 10:03 and 10:39 R7 snapshots), markup forensics,
stream findings W1-W7 + V7, curated knowledge (curate_r7_data.py).
Usage: python3 curate_r7.py <r6_workbook.xlsx> <r7_dir> <out_spec.json> <out_metrics.json> [repo_root]
"""
import copy, collections, json, re, sys, os
from decimal import Decimal
from openpyxl import load_workbook

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from curate_r7_base import load_json, words, tool_label, implied, DATE  # noqa: E402
import curate_r7_data as D  # noqa: E402

R6WB, R7DIR, OUT_SPEC, OUT_MET = sys.argv[1:5]
REPO = sys.argv[5] if len(sys.argv) > 5 else os.path.dirname(os.path.abspath(R6WB))  # repo root (for data/catalog)
STREAMS = ['W1', 'W2', 'W3', 'W4', 'W5', 'W6', 'W7', 'V7']
STREAM_NAMES = {'W1': 'Website & infrastructure forensics', 'W2': 'IMEI numbered sources', 'W3': 'Code-GSM / UnlocksPro',
                'W4': 'Tool chains (Chimera, Sigma, EFT, UMT ...)', 'W5': 'Long-tail vendor sweep (205 groups)',
                'W6': 'Catalog genealogy (28 servers)', 'W7': 'Digital goods', 'V7': 'Lead verification & Phase-5 re-checks'}
CONF_ORDER = ['CONFIRMED', 'STRONG', 'LIKELY', 'DISPUTED', 'UNKNOWN']

# ------------------------------------------------------------------ R6 workbook (read-only)
wb = load_workbook(R6WB, read_only=True)


def sheet(name):
    rows = list(wb[name].iter_rows(values_only=True))
    hi = next(i for i, r in enumerate(rows) if sum(1 for c in r if c not in (None, '')) >= 3)
    hdr = [str(h) if h is not None else '' for h in rows[hi]]
    out = []
    for r in rows[hi + 1:]:
        if all(c in (None, '') for c in r):
            continue
        out.append({h: ('' if v is None else v) for h, v in zip(hdr, r)})
    return hdr, out


_, R6_SVC = sheet('All Services')
_, R6_GRP = sheet('Service Groups')
_, R6_EV = sheet('Evidence Register')
_, R6_VEN = sheet('Original Vendors')
_, R6_REL = sheet('Supply Chain Relationships')
_, R6_GAP = sheet('Research Gaps')
_, R6_DASH = sheet('Dashboard')
_, R6_TOOL = sheet('MCP Tool Log')
VEN_BY_ID = {v['Vendor ID']: v for v in R6_VEN}

# ------------------------------------------------------------------ findings
F, ORDER, NEGS, TOOLS = {}, [], [], []
for s in STREAMS:
    d = load_json(f'{R7DIR}/findings/{s}.json')
    for f in d['findings']:
        f = copy.deepcopy(f)
        f['_stream'] = s
        F[f['tid']] = f
        ORDER.append(f['tid'])
    for n in d.get('negative_findings', []):
        NEGS.append((s, n))
    for t in d.get('tool_log', []):
        TOOLS.append((s, t))
EV = {tid: f'EV-{267 + i:03d}' for i, tid in enumerate(ORDER)}
NEG_ID = [f'NEG-{i + 1:03d}' for i in range(len(NEGS))]


def ev(tids, with_tid=True):
    out = []
    for t in tids:
        if t in EV:
            out.append(f'{EV[t]} ({t})' if with_tid else EV[t])
    return '; '.join(out)


# Phase-5 corrections (curated copy only)
P5NOTE = collections.defaultdict(list)
P5CONF = {}
for c in D.CORRECTIONS:
    f = F[c['tid']]
    fld = c['field']
    orig = f.get(fld, '') or ''
    if 'new' in c:
        f[fld] = c['new']
    elif 'replace' in c:
        old, new = c['replace']
        assert old in orig, (c['tid'], fld, old)
        f[fld] = orig.replace(old, new)
    elif 'append' in c:
        f[fld] = orig + c['append']
    if c.get('conf'):
        P5CONF[c['tid']] = c['conf']
    P5NOTE[c['tid']].append(f"[{fld}] {c['reason']}")
VERIFIED_BY = {'W2-09': 'V7-10', 'W3-09': 'V7-11', 'W6-06': 'V7-11', 'W1-07': 'V7-12', 'W4-01': 'V7-13', 'W2-02': 'V7-14',
               'W4-07': 'V7-15', 'W5-69': 'V7-17', 'W7-05': 'V7-18', 'W6-09': 'V7-19', 'W6-04': 'V7-20', 'W6-11': 'V7-21',
               'W4-10': 'V7-16', 'W4-09': 'V7-07', 'W3-03': 'V7-08', 'W2-08': 'V7-08', 'W6-01': 'V7-23', 'W6-02': 'V7-24',
               'W6-15': 'V7-25', 'W7-01': 'V7-26', 'W4-04': 'V7-27', 'W4-22': 'W1-16'}
for t, v in VERIFIED_BY.items():
    P5NOTE[t].append(f'Second-tool re-check: {EV[v]} ({v}) - {words(F[v]["supports_or_contradicts"], 18)}')


def conf_after(tid):
    return P5CONF.get(tid, F[tid].get('confidence', ''))


# ------------------------------------------------------------------ catalogs
def cat_rows(path, catalog):
    d = load_json(path)
    return [dict(catalog=catalog, group=s['group'], service=s['service'], price_raw=s['price_raw'].replace('$', '').strip(),
                 price=s['price_usd'], delivery=s['delivery'].replace('<br>', ' ')) for s in d['services']]


C02 = cat_rows(f'{REPO}/data/catalog/server_catalog.json', 'Server') + cat_rows(f'{REPO}/data/catalog/imei_catalog.json', 'IMEI')
C10 = cat_rows(f'{R7DIR}/raw/server_catalog_1003.json', 'Server') + cat_rows(f'{R7DIR}/raw/imei_catalog_1003.json', 'IMEI')
C39 = cat_rows(f'{R7DIR}/raw/imei_catalog_1039.json', 'IMEI')
key = lambda r: (r['catalog'], r['group'], r['service'])  # noqa: E731
P02 = collections.defaultdict(list)
for r in C02:
    P02[key(r)].append(r['price_raw'])
P39 = {key(r): r['price_raw'] for r in C39}
MK = {}
for fn in ('markup_server.json', 'markup_imei.json'):
    m = load_json(f'{R7DIR}/raw/{fn}')
    for g in m['groups']:
        MK[g['group']] = g
MROWS = {}
for fn, catn in (('markup_server.json', 'Server'), ('markup_imei.json', 'IMEI')):
    for r in load_json(f'{R7DIR}/raw/{fn}')['rows']:
        MROWS[(catn, r['group'], r['service'], r['price'])] = r

# R6 SVC id lookup
SVC = collections.defaultdict(list)
for r in R6_SVC:
    rid = str(r.get('Research ID', ''))
    if not re.match(r'SVC-\d{4}$', rid):
        continue
    SVC[(r['Catalog'], r['Group'], r['Service Name (as listed)'])].append((str(r['Price (USD)']), rid))
RENAMED = {('Server', 'Cerberus Tool Pro', '$59.99'): 'Cerberus Tool Pro Activation [12 Months - 1 Pc]',
           ('Server', 'Cerberus Tool Pro', '$24.99'): 'Cerberus Tool Pro Activation [3 Months - 1 Pc]',
           ('Server', 'Cerberus Tool Pro', '$39.99'): 'Cerberus Tool Pro Activation [6 Months - 1 Pc]'}


def svc_id(r):
    cands = SVC.get(key(r), [])
    if len(cands) == 1:
        return cands[0][1], ''
    for p, rid in cands:
        try:
            if abs(float(p) - float(r['price'])) < 1e-9:
                return rid, ''
        except Exception:
            pass
    old = RENAMED.get((r['catalog'], r['group'], '$' + r['price_raw']))
    if old:
        c2 = SVC.get((r['catalog'], r['group'], old), [])
        if c2:
            return c2[0][1], old
    return '', ''


# ------------------------------------------------------------------ group assessment
W5 = load_json(f'{R7DIR}/findings/W5.json')
W5GS = {g['group_id']: g for g in W5['group_status']}
W5LABEL = {'NO_PUBLIC_LIST_OR_NOT_RENDERED': 'no public list / list not rendered', 'VENDOR_NOT_FOUND': 'vendor site not found',
           'UNREACHABLE': 'vendor site down or parked', 'ABSENT': 'HalabTech absent from vendor list'}


def r6_route(g):
    c, conf = str(g['Candidate Upstream / Intermediary'] or ''), g['Upstream Confidence']
    cl = c.lower()
    if 'in-house' in cl or 'internal test' in cl:
        return 'IN'
    if cl.startswith('direct from hunter') or cl.startswith('direct from q-unlocker') or cl.startswith('direct from xtp') \
            or 'exclusive distributor' in cl or 'gsmeasy or gsmserver' in cl:
        return 'VR'
    if cl.startswith('via a named distributor') or cl.startswith('one of:') or 'sales arm' in cl or 'dhru' in cl:
        return 'LC'
    if 'sole official' in cl or 'sole distributor' in cl:
        return 'NI'
    if cl.startswith('direct') or 'direct from' in cl:
        return 'VD'
    if 'unnamed' in cl or 'source' in cl and conf == 'UNKNOWN':
        return 'NS'
    return 'UK' if conf in ('UNKNOWN', '') else 'VD'


def listing_label(claim):
    m = re.search(r'lists HalabTech as:\s*(.*)$', claim or '')
    return (m.group(1) if m else claim or '').strip().rstrip('.')


GA = {}
for g in R6_GRP:
    gid = g['Group ID']
    ven = VEN_BY_ID.get(str(g['Vendor ID'] or ''), {})
    a = dict(gid=gid, catalog=g['Catalog'], name=g['Group Name'], skus=int(g['Services'] or 0),
             dev=str(g['Original Vendor / Brand'] or ''), dev_url=str(ven.get('Website', '') or ''),
             status=str(g['HalabTech Status at Vendor'] or ''), cand=str(g['Candidate Upstream / Intermediary'] or ''),
             route=r6_route(g), conf=g['Upstream Confidence'], tids=[], note='', r6conf=g['Upstream Confidence'],
             r6cand=str(g['Candidate Upstream / Intermediary'] or ''), r6ev=str(g['Evidence IDs'] or ''), r7checked=False,
             r6status=str(g['HalabTech Status at Vendor'] or ''), neg_ids=[], issuer_known=False,
             vendor_lists=None)
    if a['dev_url'] and not a['dev_url'].startswith('http') and a['dev_url'] not in ('—', 'None'):
        a['dev_url'] = 'https://' + a['dev_url']
    if a['dev_url'] in ('—', 'None'):
        a['dev_url'] = ''
    st = a['status'].lower()
    if any(k in st for k in ('distributor', 'reseller', 'agent', 'seller', 'listed (tab', 'our resellers', 'partner')) and 'not listed' not in st \
            and 'self-claim' not in st and not st.startswith('product of') and not st.startswith('platform'):
        a['vendor_lists'] = True
    if 'not listed' in st:
        a['vendor_lists'] = False
    w = W5GS.get(gid)
    if w:
        a['r7checked'] = True
        s5 = w['halabtech_on_vendor_list']
        if s5.startswith('LISTED'):
            f = F[w['finding']]
            a['dev'] = re.sub(r'\s*\(.*$', '', f['entity']) if not s5.endswith('A1-10)') else 'Octoplus Box team'
            a['dev_url'] = w['vendor_url'] or f.get('entity_website', '') or a['dev_url']
            lab = listing_label(f['claim'])
            a['status'] = lab if not s5.endswith('A1-10)') else 'Official reseller (R6 A1-10)'
            a['cand'] = 'Vendor direct (developer lists HalabTech; fulfilment route not proven)'
            a['route'] = 'VD'
            lconf = conf_after(w['finding'])
            a['conf'] = 'LIKELY' if lconf in ('CONFIRMED', 'STRONG', 'LIKELY') else 'UNKNOWN'
            a['tids'] = [w['finding']]
            a['vendor_lists'] = True
            if lconf != 'CONFIRMED':
                a['note'] = f'Listing itself {lconf} (identification indirect).'
        elif s5 == 'ABSENT':
            a['dev_url'] = w['vendor_url'] or a['dev_url']
            a['status'] = 'Not listed (vendor list checked in R7)'
            a['vendor_lists'] = False
            assert gid in D.GROUP_OVR, gid
        else:
            a['dev_url'] = w['vendor_url'] or a['dev_url']
            a['status'] = f'Not determinable (R7: {W5LABEL[s5]})'
            a['cand'] = 'Unidentified'
            a['route'] = 'UK'
            a['conf'] = 'UNKNOWN'
    o = D.GROUP_OVR.get(gid)
    if o:
        for k, v in o.items():
            if k == 'tids':
                a['tids'] = list(dict.fromkeys(a['tids'] + v))
            elif k == 'note':
                a['note'] = (a['note'] + ' ' + v).strip()
            elif k == 'ev_extra':
                a['r6ev'] = '; '.join(x for x in [a['r6ev'] if a['r6ev'] not in ('', 'None') else '', v] if x)
            else:
                a[k] = v
        a['r7checked'] = a['r7checked'] or bool(o.get('tids')) or 'cand' in o
    for t in F:  # any finding naming the group exactly
        pass
    GA[gid] = a

# W5 negative checks carry '[HalabTech group: X]' tags -> link NEG ids to groups
_w5names = {GA[g]['name']: g for g in GA}
for (s_, nf), nid in zip(NEGS, NEG_ID):
    if s_ != 'W5':
        continue
    ent = nf.get('entity', '')
    i0 = ent.find('[HalabTech group')
    if i0 < 0:
        continue
    body = ent[ent.find(':', i0) + 1: ent.rfind(']')]
    for gname in [x.strip() for x in body.split(';')]:
        if gname in _w5names:
            GA[_w5names[gname]]['neg_ids'].append(nid)
# groups referenced by R7 findings (exact name match) -> evidence + 'checked'
NAME2GID = collections.defaultdict(list)
_norm = lambda s: re.sub(r'\s+', ' ', str(s).replace('\\', '')).strip().lower()  # noqa: E731
for gid, a in GA.items():
    NAME2GID[_norm(a['name'])].append(gid)
ALIAS = {'build your server dhru service': 'build your server dhru services', 'halabtech single file': 'halabtech',
         'halabtech [reseller/ distributor package]': 'halabtech'}
GROUP_TIDS = collections.defaultdict(list)
for tid in ORDER:
    for gname in F[tid].get('halabtech_groups_affected') or []:
        n = _norm(gname)
        n = ALIAS.get(n, n)
        for gid in NAME2GID.get(n, []):
            GROUP_TIDS[gid].append(tid)
for gid, tl in GROUP_TIDS.items():
    a = GA[gid]
    a['all_tids'] = list(dict.fromkeys(a['tids'] + tl))
    a['r7checked'] = True
for gid, a in GA.items():
    a.setdefault('all_tids', list(a['tids']))
    if a['r6conf'] != a['conf']:
        a['change'] = f"{a['r6conf']} -> {a['conf']}"
    elif a['cand'] != a['r6cand']:
        a['change'] = 'same confidence; candidate updated' if a['r6cand'] else 'checked in R7; no upstream found'
    elif a['r7checked']:
        a['change'] = 'no change (evidence added)'
    else:
        a['change'] = 'no change'

# ------------------------------------------------------------------ SKU inventory
INV, SKU_A = [], []
ROUTE_TXT = D.ROUTES
next_new = 1490
for r in C10:
    gid = next((g for g in NAME2GID.get(_norm(r['group']), []) if GA[g]['catalog'] == r['catalog']), '')
    a = dict(GA[gid]) if gid else {}
    for (og, sub, fields) in D.SKU_OVR:
        if og == gid and sub in r['service']:
            a.update({k: v for k, v in fields.items() if k != 'tids'})
            a['tids'] = fields['tids']
            a['all_tids'] = list(dict.fromkeys(fields['tids']))
            a['change'] = f"{a['r6conf']} -> {a['conf']} (SKU-level)"
    rid, oldname = svc_id(r)
    if not rid:
        rid = f'SVC-{next_new}'
        next_new += 1
    p02 = P02.get(key(r)) or ([] if not oldname else P02.get((r['catalog'], r['group'], oldname), []))
    p02s = p02[0] if len(p02) == 1 else (r['price_raw'] if r['price_raw'] in p02 else '; '.join(p02))
    p39 = P39.get(key(r), '') if r['catalog'] == 'IMEI' else 'n/a (not re-captured)'
    mr = MROWS.get((r['catalog'], r['group'], r['service'], r['price_raw'].replace(',', '')))
    comp = bool(mr and mr['decimals'] >= 3)
    mg = MK.get(r['group'], {})
    mult = mg.get('best_multiplier') or ''
    imp = implied(r['price_raw'], mult) if (comp and mult) else ''
    chg = ''
    if p02s and p02s != r['price_raw']:
        chg = f'{p02s} -> {r["price_raw"]}'
    if oldname:
        chg = (chg + '; ' if chg else '') + 'renamed between 02:00 and 10:03 UTC (same price)'
    row = {
        'Inventory ID': rid, 'Catalog': r['catalog'], 'Group ID': gid, 'Group': r['group'], 'Service Name (10:03 UTC)': r['service'],
        'Name at 02:00 UTC (if renamed)': oldname, 'Price 02:00 (USD)': p02s, 'Price 10:03 (USD)': r['price_raw'],
        'Price 10:39 (USD, IMEI only)': p39, 'Price Change': chg, 'Delivery': r['delivery'],
        'Computed Price (>=3 dec.)': 'Yes' if comp else 'No', 'Group Multiplier (inferred)': mult if comp else '',
        'Implied Upstream Cost (USD)': imp, 'Original Developer / Issuer': a.get('dev', ''), 'Developer Website': a.get('dev_url', ''),
        'HalabTech Status at Developer': a.get('status', ''), 'Candidate Upstream / Chain (R7)': a.get('cand', ''),
        'Route Type': ROUTE_TXT.get(a.get('route', 'UK'), ''), 'Upstream Confidence (R6)': a.get('r6conf', ''),
        'Upstream Confidence (R7)': a.get('conf', ''), 'Change R6 -> R7': a.get('change', ''), 'Evidence (R1-R6)': a.get('r6ev', ''),
        'Evidence (R7)': '; '.join(x for x in [ev(a.get('all_tids', [])), '; '.join(a.get('neg_ids', []))] if x), 'Notes (R7)': a.get('note', ''),
    }
    INV.append(row)
    SKU_A.append((row, a))

# ------------------------------------------------------------------ metrics
N_SKU = len(INV)
N_GRP = len(GA)
cnt_g = collections.Counter(a['conf'] for a in GA.values())
cnt_g6 = collections.Counter(a['r6conf'] for a in GA.values())
cnt_s = collections.Counter(row['Upstream Confidence (R7)'] for row, a in SKU_A)
cnt_s6 = collections.Counter(row['Upstream Confidence (R6)'] for row, a in SKU_A)
route_s = collections.Counter(a.get('route', 'UK') for row, a in SKU_A)
route_conf_s = collections.Counter((a.get('route', 'UK'), row['Upstream Confidence (R7)']) for row, a in SKU_A)


def has_dev(a):
    # developer identified = official site/page on record (R6 VEN or R7 vendor URL), in-house, or a named issuer brand
    return bool(a.get('dev_url')) or a.get('route') == 'IN' or bool(a.get('issuer_known'))


ev_r6 = lambda a: bool(a['r6ev'] and a['r6ev'] not in ('None', ''))  # noqa: E731
NOT_INV = ('Not checked', '', 'n/a (IMEI service)', 'n/a', 'None')
inv_g6 = {gid for gid, a in GA.items() if ev_r6(a) or a['r6status'] not in NOT_INV}
inv_g = inv_g6 | {gid for gid, a in GA.items() if a['r7checked'] or a['neg_ids']}
inv_g_r7 = {gid for gid, a in GA.items() if a['r7checked']}
sk = lambda gids: sum(GA[g]['skus'] for g in gids)  # noqa: E731
listed_g = {gid for gid, a in GA.items() if a.get('vendor_lists') is True}
dev_g = {gid for gid, a in GA.items() if has_dev(a) and a['catalog'] == 'Server'}
imei_g = {gid for gid, a in GA.items() if a['catalog'] == 'IMEI'}
ge_likely = {gid for gid, a in GA.items() if a['conf'] in ('CONFIRMED', 'STRONG', 'LIKELY')}
inhouse_conf = {gid for gid, a in GA.items() if a['route'] == 'IN' and a['conf'] == 'CONFIRMED'}
third_ge_likely = ge_likely - {gid for gid, a in GA.items() if a['route'] == 'IN'}
named_ge_likely = {gid for gid in third_ge_likely if GA[gid]['route'] in ('VR', 'VD', 'VA', 'NI', 'FP')}
strong_third = {gid for gid in third_ge_likely if GA[gid]['conf'] == 'STRONG'}
unknown_g = {gid for gid, a in GA.items() if a['conf'] == 'UNKNOWN'}
disputed_g = {gid for gid, a in GA.items() if a['conf'] == 'DISPUTED'}
ev_any = {gid for gid, a in GA.items() if ev_r6(a) or a['all_tids'] or a['neg_ids']}
ev_pos = {gid for gid, a in GA.items() if ev_r6(a) or a['all_tids']}
r6_unknown = {gid for gid, a in GA.items() if a['r6conf'] == 'UNKNOWN'}
r6_ge_likely = {gid for gid, a in GA.items() if a['r6conf'] in ('CONFIRMED', 'STRONG', 'LIKELY')}
# SKU-level (with SKU overrides)
s_ge_likely = sum(1 for row, a in SKU_A if row['Upstream Confidence (R7)'] in ('CONFIRMED', 'STRONG', 'LIKELY'))
s_r6_ge_likely = sum(1 for row, a in SKU_A if row['Upstream Confidence (R6)'] in ('CONFIRMED', 'STRONG', 'LIKELY'))
s_inhouse_conf = sum(1 for row, a in SKU_A if a.get('route') == 'IN' and row['Upstream Confidence (R7)'] == 'CONFIRMED')
s_inhouse_all = sum(1 for row, a in SKU_A if a.get('route') == 'IN')
s_third_ge_likely = sum(1 for row, a in SKU_A if a.get('route') != 'IN' and row['Upstream Confidence (R7)'] in ('CONFIRMED', 'STRONG', 'LIKELY'))
s_named = sum(1 for row, a in SKU_A if a.get('route') in ('VR', 'VD', 'VA', 'NI', 'FP') and row['Upstream Confidence (R7)'] in ('CONFIRMED', 'STRONG', 'LIKELY'))
s_channel = sum(1 for row, a in SKU_A if a.get('route') == 'LC' and row['Upstream Confidence (R7)'] in ('STRONG', 'LIKELY'))
s_strong = sum(1 for row, a in SKU_A if a.get('route') != 'IN' and row['Upstream Confidence (R7)'] == 'STRONG')
s_unknown = sum(1 for row, a in SKU_A if row['Upstream Confidence (R7)'] == 'UNKNOWN')
s_disputed = sum(1 for row, a in SKU_A if row['Upstream Confidence (R7)'] == 'DISPUTED')
s_listed = sum(1 for row, a in SKU_A if a.get('vendor_lists') is True)
s_dev = sum(1 for row, a in SKU_A if has_dev(a) and row['Catalog'] == 'Server')
s_inv = sum(1 for row, a in SKU_A if row['Group ID'] in inv_g)
s_inv6 = sum(1 for row, a in SKU_A if row['Group ID'] in inv_g6)
s_evpos = sum(1 for row, a in SKU_A if row['Group ID'] in ev_pos)
s_inv_r7 = sum(1 for row, a in SKU_A if row['Group ID'] in inv_g_r7)
s_ev = sum(1 for row, a in SKU_A if row['Group ID'] in ev_any)
s_comp = sum(1 for row, a in SKU_A if row['Computed Price (>=3 dec.)'] == 'Yes')
pct = lambda a_, b_: f'{100.0 * a_ / b_:.1f}%' if b_ else '-'  # noqa: E731

# vendor listing counts (developers that officially list HalabTech)
r6_listing_vendors = sum(1 for v in R6_VEN if str(v.get('Confidence (R6)', '')).startswith(('CONFIRMED', 'STRONG'))
                         and v['Vendor ID'] != 'VEN-000' and not str(v.get('Confidence (R6)', '')).startswith('CONFIRMED (absence)')
                         and 'NOT LISTED' not in str(v.get('Relationship with HalabTech', '')).upper()
                         and 'Platform' not in str(v.get('Relationship with HalabTech', '')))
w5_pos = [t for t in ORDER if F[t]['_stream'] == 'W5' and "official reseller/distributor page lists HalabTech as" in (F[t].get('claim') or '')]
w5_pos_conf = [t for t in w5_pos if conf_after(t) == 'CONFIRMED']
CONFIRMING_V7 = {'V7-10', 'V7-11', 'V7-12', 'V7-13', 'V7-14', 'V7-15', 'V7-17', 'V7-18', 'V7-19', 'V7-20', 'V7-23', 'V7-24', 'V7-25', 'V7-26', 'V7-27', 'W1-16'}
r7_strong_conf = [t for t in ORDER if conf_after(t) in ('CONFIRMED', 'STRONG') and F[t]['_stream'] in ('W2', 'W3', 'W4', 'W6', 'W7')]
second_tool = [t for t in r7_strong_conf if VERIFIED_BY.get(t) in CONFIRMING_V7 or (';' in str(F[t].get('tool', '')))]

M = dict(
    n_sku=N_SKU, n_grp=N_GRP, n_server_grp=sum(1 for a in GA.values() if a['catalog'] == 'Server'), n_imei_grp=len(imei_g),
    inv_g=len(inv_g), inv_s=s_inv, inv_g_r7=len(inv_g_r7), inv_s_r7=s_inv_r7,
    dev_g=len(dev_g), dev_s=s_dev, listed_g=len(listed_g), listed_s=s_listed,
    ge_likely_g=len(ge_likely), ge_likely_s=s_ge_likely, third_ge_likely_g=len(third_ge_likely), third_ge_likely_s=s_third_ge_likely,
    named_g=len(named_ge_likely), named_s=s_named, channel_s=s_channel, strong_third_g=len(strong_third), strong_third_s=s_strong,
    inhouse_conf_g=len(inhouse_conf), inhouse_conf_s=s_inhouse_conf, inhouse_all_s=s_inhouse_all,
    verified_third_party_s=0, unknown_g=len(unknown_g), unknown_s=s_unknown, disputed_g=len(disputed_g), disputed_s=s_disputed,
    ev_g=len(ev_any), ev_s=s_ev, comp_s=s_comp, r6_unknown_g=len(r6_unknown), r6_ge_likely_g=len(r6_ge_likely), r6_ge_likely_s=s_r6_ge_likely,
    conf_g=dict(cnt_g), conf_g6=dict(cnt_g6), conf_s=dict(cnt_s), conf_s6=dict(cnt_s6), route_s=dict(route_s),
    w5_pos=len(w5_pos), w5_pos_conf=len(w5_pos_conf), inv_g6=len(inv_g6), inv_s6=s_inv6, ev_pos_g=len(ev_pos), ev_pos_s=s_evpos,
    r7_findings=len(ORDER), r7_negs=len(NEGS), r7_calls=len(TOOLS),
    r7_strong_conf=len(r7_strong_conf), second_tool=len(second_tool),
    groups_changed=sum(1 for a in GA.values() if a['r6conf'] != a['conf']),
    up=sum(1 for a in GA.values() if CONF_ORDER.index(a['conf']) < CONF_ORDER.index(a['r6conf']) and a['r6conf'] != 'DISPUTED'),
    down=sum(1 for a in GA.values() if a['r6conf'] in ('CONFIRMED', 'STRONG', 'LIKELY') and a['conf'] in ('UNKNOWN', 'DISPUTED')),
)

# ------------------------------------------------------------------ sheets
SHEETS = []


def add(title, header, rows, note='', conf_cols=(), url_cols=(), widths=None):
    SHEETS.append(dict(title=title, header=header, rows=rows, note=note, conf_cols=list(conf_cols), url_cols=list(url_cols), widths=widths or {}))


# 1. Research Progress Dashboard -------------------------------------------------------------------------------
def r6dash(metric_prefix):
    for r in R6_DASH:
        if str(r.get('Metric', '')).startswith(metric_prefix):
            return r
    return {}


# W5 listings already in the R6 vendor register (Deep Unlocker VEN-006, General Unlocker VEN-009, TFM VEN-010, MDMFix VEN-008, E-GSM VEN-005, Xiaomi King VEN-004)
W5_OVERLAP = {'W5-03', 'W5-06', 'W5-26', 'W5-31', 'W5-38', 'W5-65'}
_w5_new_conf = [t for t in w5_pos if t not in W5_OVERLAP and conf_after(t) == 'CONFIRMED']
_w5_new_strong = [t for t in w5_pos if t not in W5_OVERLAP and conf_after(t) == 'STRONG']
_w5_new_likely = [t for t in w5_pos if t not in W5_OVERLAP and conf_after(t) == 'LIKELY']
M.update(w5_new_conf=len(_w5_new_conf), w5_new_strong=len(_w5_new_strong), w5_new_likely=len(_w5_new_likely))
dash = []
DR = lambda **k: dash.append(k)  # noqa: E731
DR(Section='Scope', Metric='Public catalog (snapshot used for R7)', Definition='server.halabtech.com /resellerpricing/server + /imei, Firecrawl 10:03 UTC (IMEI re-captured 10:39 UTC: no changes)',
   R3='>=240 groups seen (page truncated)', R6='383 groups / 1,455 SKUs (02:00 UTC)', R7=f'{N_GRP} groups / {N_SKU} SKUs', Change='2 price changes, 3 renamed SKUs (Cerberus)')
DR(Section='Investigation', Metric='Groups investigated (cumulative R1-R7)', Definition='groups with >=1 group-specific evidence item or a completed vendor/route check (R6 status not "Not checked", R6 evidence IDs, W5 status, or an R7 finding naming the group) / all groups',
   R3='-', R6=f'{len(inv_g6)} / {N_GRP} = {pct(len(inv_g6), N_GRP)} (recomputed with the same rule)', R7=f'{len(inv_g)} / {N_GRP} = {pct(len(inv_g), N_GRP)}',
   Change=f'{len(inv_g) - len(inv_g6):+d} groups')
DR(Section='Investigation', Metric='Services (SKUs) in investigated groups', Definition='SKUs whose group is investigated / all SKUs', R3='34 records', R6=f'{s_inv6} / {N_SKU} = {pct(s_inv6, N_SKU)}', R7=f'{s_inv} / {N_SKU} = {pct(s_inv, N_SKU)}', Change=f'{s_inv - s_inv6:+d} SKUs')
DR(Section='Investigation', Metric='Groups touched in Round 7', Definition='groups named by >=1 R7 finding or with a W5 vendor-list status', R3='-', R6='-', R7=f'{len(inv_g_r7)} groups / {s_inv_r7} SKUs', Change='new')
DR(Section='Developers', Metric='Server SKUs linked to an identified original developer', Definition='Server-catalog SKUs whose group has a developer with an official site/page on record (R6 vendor register or R7 vendor URL), a named issuer brand, or is in-house; IMEI services are carrier/OEM services with no tool-developer layer',
   R3='-', R6='-', R7=f'{s_dev} of {sum(1 for row, a in SKU_A if row["Catalog"] == "Server")} Server SKUs ({len(dev_g)} groups)', Change='')
DR(Section='Developers', Metric='SKUs whose developer officially lists HalabTech (authorised channel)', Definition='SKUs in groups where the developer\'s own page names HalabTech as distributor/reseller/agent (CONFIRMED status; NOT proof of the fulfilment route)',
   R3='11 vendors', R6='62 vendors (CONFIRMED/STRONG)', R7=f'{62 + len(_w5_new_conf) + len(_w5_new_strong)} vendors (CONFIRMED/STRONG) + {len(_w5_new_likely)} LIKELY; {s_listed} SKUs / {len(listed_g)} groups',
   Change=f'+{len(_w5_new_conf)} new CONFIRMED, +{len(_w5_new_strong)} STRONG (W5 read {M["w5_pos"]} pages; {len(W5_OVERLAP)} were already in the R6 register)')
DR(Section='Upstream', Metric='SKUs with a defensible upstream (>=LIKELY, incl. in-house)', Definition='SKUs whose R7 upstream confidence is CONFIRMED, STRONG or LIKELY / all SKUs',
   R3='-', R6=f'{s_r6_ge_likely} / {N_SKU} = {pct(s_r6_ge_likely, N_SKU)}', R7=f'{s_ge_likely} / {N_SKU} = {pct(s_ge_likely, N_SKU)}', Change=f'{s_ge_likely - s_r6_ge_likely:+d} SKUs')
DR(Section='Upstream', Metric='... of which third-party (not in-house)', Definition='as above, excluding HalabTech in-house products', R3='-', R6='-', R7=f'{s_third_ge_likely} SKUs ({len(third_ge_likely)} groups)', Change='')
DR(Section='Upstream', Metric='... of which a named upstream entity', Definition='route = vendor rule / vendor direct / vendor API / named intermediary / named fingerprint candidate', R3='-', R6='-', R7=f'{s_named} SKUs ({len(named_ge_likely)} groups)', Change='')
DR(Section='Upstream', Metric='... of which only the vendor\'s channel is known (member unnamed)', Definition="route = vendor's listed channel", R3='-', R6='-', R7=f'{s_channel} SKUs', Change='')
DR(Section='Upstream', Metric='SKUs with a STRONG third-party upstream', Definition='vendor rule (Sigma, Chimera, Hunter, Q-Unlocker, XTP)', R3='-', R6='-', R7=f'{s_strong} SKUs ({len(strong_third)} groups)', Change='')
DR(Section='Verified', Metric='SKUs with a VERIFIED (CONFIRMED) direct supplier - third party', Definition='a primary source documents the specific supplier of the specific service', R3='0', R6='0', R7='0', Change='none proven')
DR(Section='Verified', Metric='SKUs with a VERIFIED source - in-house', Definition='HalabTech\'s own products and internal SKUs (CONFIRMED)', R3='-', R6='-', R7=f'{s_inhouse_conf} SKUs ({len(inhouse_conf)} groups)', Change='')
DR(Section='Unknown', Metric='UNKNOWN groups remaining', Definition='groups with R7 upstream confidence UNKNOWN', R3='-', R6=f'{len(r6_unknown)}', R7=f'{len(unknown_g)} groups / {s_unknown} SKUs', Change=f'{len(unknown_g) - len(r6_unknown):+d} groups')
DR(Section='Unknown', Metric='DISPUTED groups', Definition='conflicting evidence on the candidate or direction', R3='-', R6=f"{cnt_g6.get('DISPUTED', 0)}", R7=f"{len(disputed_g)} groups / {s_disputed} SKUs", Change='')
DR(Section='Evidence', Metric='Evidence coverage (positive or negative evidence)', Definition='groups with >=1 evidence ID (EV or NEG, R1-R7) / all groups; SKUs in those groups / all SKUs', R3='-', R6=f"{sum(1 for a in GA.values() if ev_r6(a))} groups",
   R7=f'{len(ev_any)} / {N_GRP} groups = {pct(len(ev_any), N_GRP)}; {s_ev} / {N_SKU} SKUs = {pct(s_ev, N_SKU)}', Change='')
DR(Section='Evidence', Metric='Evidence coverage (positive evidence only)', Definition='groups with >=1 EV item (R1-R7) / all groups', R3='-', R6=f"{sum(1 for a in GA.values() if ev_r6(a))} groups",
   R7=f'{len(ev_pos)} / {N_GRP} groups = {pct(len(ev_pos), N_GRP)}; {s_evpos} / {N_SKU} SKUs = {pct(s_evpos, N_SKU)}', Change='')
DR(Section='Evidence', Metric='Evidence items', Definition='Evidence Registry rows', R3='54 (R1-3 sources)', R6='EV-001...EV-266 (+EV-020b)', R7=f'+{len(ORDER)} findings (EV-267...{EV[ORDER[-1]]}) + {len(NEGS)} negative checks (NEG-001...{NEG_ID[-1]})', Change='')
DR(Section='Evidence', Metric='STRONG/CONFIRMED findings (streams W2-W4, W6, W7) re-checked with a second tool', Definition='confirmed by a V7 re-fetch with a different tool, or captured with two tools by the stream itself; W5 re-read its own 70 listing pages; W1 = infrastructure facts',
   R3='-', R6='-', R7=f'{len(second_tool)} / {len(r7_strong_conf)}', Change='')
DR(Section='Evidence', Metric='Computed (3-decimal) prices fingerprinted', Definition='SKUs whose price = cost x Dhru markup (>=3 decimals); groups with one shared multiplier', R3='-', R6='-', R7=f'{s_comp} SKUs; 73 groups with a shared multiplier', Change='new method')
for c_ in CONF_ORDER:
    DR(Section='Confidence (groups)', Metric=f'Groups - {c_}', Definition='upstream confidence per group', R3='-', R6=str(cnt_g6.get(c_, 0)), R7=str(cnt_g.get(c_, 0)), Change=f'{cnt_g.get(c_, 0) - cnt_g6.get(c_, 0):+d}')
for c_ in CONF_ORDER:
    DR(Section='Confidence (SKUs)', Metric=f'SKUs - {c_}', Definition='upstream confidence per SKU (group value; SKU overrides applied)', R3='-', R6=str(cnt_s6.get(c_, 0)), R7=str(cnt_s.get(c_, 0)), Change=f'{cnt_s.get(c_, 0) - cnt_s6.get(c_, 0):+d}')
for rk in ['IN', 'VR', 'VD', 'VA', 'NI', 'FP', 'LC', 'NS', 'DS', 'UK']:
    DR(Section='Route type (SKUs)', Metric=D.ROUTES[rk], Definition='how the SKU is (probably) fulfilled', R3='-', R6='-', R7=str(route_s.get(rk, 0)), Change='')
DR(Section='Completeness', Metric='A. Coverage completeness', Definition='investigated groups / all groups (every group checked at least once)', R3='-', R6='-', R7=pct(len(inv_g), N_GRP), Change='')
DR(Section='Completeness', Metric='B. Attribution completeness', Definition='SKUs with an upstream at >=LIKELY (incl. in-house) / all SKUs', R3='-', R6=pct(s_r6_ge_likely, N_SKU), R7=pct(s_ge_likely, N_SKU), Change='')
DR(Section='Completeness', Metric='C. Verification completeness', Definition='SKUs with a CONFIRMED immediate source / all SKUs (in-house only; third-party = 0)', R3='-', R6='-', R7=pct(s_inhouse_conf, N_SKU), Change='')
_mcp = [t for s_, t in TOOLS if tool_label(str(t.get('tool', ''))).startswith(('Firecrawl', 'Parallel', 'Exa'))]
DR(Section='Process', Metric='MCP calls in R7', Definition='Firecrawl / Parallel / Exa calls logged by streams W1-W7 + V7 (non-MCP log entries excluded)', R3='0 (MCP not available)', R6='see MCP Tool Log (R4-R6)',
   R7=f"{len(_mcp)} calls ({sum(1 for t in _mcp if not t.get('ok'))} failed); {len(TOOLS) - len(_mcp)} non-MCP log entries", Change='')
DR(Section='Process', Metric='Confidence changes logged', Definition='Confidence Change Log rows (CL-022+)', R3='-', R6='CL-001...CL-021', R7=f'{len(D.CHANGES)} entries; {M["groups_changed"]} groups changed ({M["up"]} up, {M["down"]} down/disputed)', Change='')
add('Research Progress Dashboard', ['Section', 'Metric', 'Definition', 'R3', 'R6', 'R7', 'Change'], dash,
    note=f'Round 7 (verification date {DATE}). Every percentage states its numerator/denominator; probable (LIKELY/STRONG) is never counted as CONFIRMED. '
         'Unit of analysis: the 10:03 UTC public catalog.', widths={'Section': 16, 'Metric': 46, 'Definition': 70, 'R3': 16, 'R6': 26, 'R7': 40, 'Change': 26})

# 2. Complete Service Inventory --------------------------------------------------------------------------------
INV_H = list(INV[0].keys())
add('Complete Service Inventory', INV_H, INV, note='One row per public SKU (10:03 UTC). Inventory ID = R6 SVC ID (renamed SKUs keep their ID). Implied upstream cost = price / inferred group multiplier '
    '(fingerprint, not a fact). Upstream confidence is per group unless a SKU override applies.', conf_cols=['Upstream Confidence (R6)', 'Upstream Confidence (R7)'], url_cols=['Developer Website'],
    widths={'Service Name (10:03 UTC)': 48, 'Group': 28, 'Candidate Upstream / Chain (R7)': 55, 'Evidence (R7)': 34, 'Notes (R7)': 40, 'Original Developer / Issuer': 28, 'HalabTech Status at Developer': 30})


# 3. Supplier Intelligence ---------------------------------------------------------------------------------------
def gnames(gids):
    return '; '.join(f"{g} {GA[g]['name']}" for g in gids if g in GA)


SI = []
for e in D.ENTITIES:
    gids = [g for g in e['groups'] if g in GA]
    SI.append({'Entity ID': e['id'], 'Entity': e['name'], 'Website': e['url'], 'Type / Chain Layer': e['type'], 'Relationship with HalabTech (R7)': e['rel'],
               'Direction': e['direction'], 'HalabTech Groups': gnames(gids), 'Groups (#)': len(gids), 'SKUs (#)': sum(GA[g]['skus'] for g in gids),
               'Confidence (R6)': e['r6'], 'Confidence (R7)': e['r7'], 'Evidence (R7)': ev(e['tids']), 'Alternative Explanations': e.get('alt', ''),
               'Contradicting Evidence': e.get('contra', ''), 'What Would Confirm': e.get('confirm', ''), 'What Would Reject': e.get('reject', '')})
add('Supplier Intelligence', list(SI[0].keys()), SI, note='Upstream candidates, intermediaries, platforms and downstream customers. Role and direction are stated separately: '
    'an official listing proves an authorised channel, not an API connection.', conf_cols=['Confidence (R7)'], url_cols=['Website'],
    widths={'Entity': 34, 'Relationship with HalabTech (R7)': 70, 'HalabTech Groups': 40, 'Evidence (R7)': 36, 'Direction': 30})

# 4. Confirmed Supply Chains -------------------------------------------------------------------------------------
CC = []
inh = [g for g in GA if GA[g]['route'] == 'IN' and GA[g]['conf'] == 'CONFIRMED']
CC.append({'Chain ID': 'CH-C01', 'Chain': 'HalabTech (developer/owner) -> server.halabtech.com -> customers, dealers and API clients', 'Original Developer': 'HalabTech',
           'Distributor / Intermediary': '-', 'Customer side (examples)': 'GsmServer, Code-GSM, UnlocksPro, HOS Unlocker, WARD, MrUnlockers, ReUnlocker, MW Unlocker, GSM Tiger, univgsm, Saudi-GSM',
           'HalabTech Groups': gnames(inh), 'SKUs (#)': sum(GA[g]['skus'] for g in inh), 'What Is Confirmed': 'HalabTech is the source of its own memberships/credits/points/test SKUs; downstream sellers documented on their own pages',
           'What Is NOT Confirmed': 'Whether each downstream buys directly or via a HalabTech dealer', 'Evidence': ev(['W4-22', 'W1-16', 'W3-06', 'V7-11', 'V7-18', 'W6-15', 'W6-01', 'V7-20']),
           'Source URL': 'https://gsmserver.com/en/credits-and-activations/manufacturer/halabtech', 'Retrieved (UTC)': '2026-10-11T10:18Z', 'Evidence Type': 'vendor page; catalog genealogy',
           'Direction': 'HalabTech -> downstream', 'Confidence': 'CONFIRMED'})
CC.append({'Chain ID': 'CH-C02', 'Chain': 'GsmServer (reseller) <- HalabTech memberships ("Halabtech" brand page, 10 products)', 'Original Developer': 'HalabTech', 'Distributor / Intermediary': 'GsmServer',
           'Customer side (examples)': 'GsmServer shop customers', 'HalabTech Groups': gnames(['GRP-S-247']), 'SKUs (#)': GA['GRP-S-247']['skus'],
           'What Is Confirmed': "GsmServer sells HalabTech's own products ('Intended for support.halabtech.com only')", 'What Is NOT Confirmed': '-',
           'Evidence': ev(['W4-22', 'W1-16']), 'Source URL': 'https://gsmserver.com/en/credits-and-activations/manufacturer/halabtech', 'Retrieved (UTC)': '2026-10-11T10:18Z',
           'Evidence Type': 'vendor page', 'Direction': 'HalabTech -> GsmServer', 'Confidence': 'CONFIRMED'})
CC.append({'Chain ID': 'CH-C03', 'Chain': 'Dhru Cloud (platform) -> server.halabtech.com (Dhru Fusion)', 'Original Developer': 'Dhru Cloud Pvt Ltd', 'Distributor / Intermediary': '-',
           'Customer side (examples)': 'HalabTech; server builders buying Dhru licences from HalabTech', 'HalabTech Groups': gnames(['GRP-S-214']), 'SKUs (#)': GA['GRP-S-214']['skus'],
           'What Is Confirmed': "Platform ('Powered by Dhru Fusion'); HalabTech resells Dhru licences/add-ons", 'What Is NOT Confirmed': 'Whether HalabTech buys licences from Dhru or a Dhru distributor',
           'Evidence': ev(['W7-17', 'W1-11']) + '; R6 EV-053, EV-188', 'Source URL': 'https://server.halabtech.com/', 'Retrieved (UTC)': '2026-10-11T10:03Z', 'Evidence Type': 'public HTML',
           'Direction': 'Dhru -> HalabTech', 'Confidence': 'CONFIRMED'})
# authorised-channel chains: R6 relationships + R7 W5 listings
n = 3
seen_dev = set()
for rr in R6_REL:
    t = str(rr.get('Type', ''))
    c6 = str(rr.get('Confidence (R6)', '') or rr.get('Confidence', ''))
    if ('authoris' in t.lower() or 'authoriz' in t.lower()) and c6.startswith(('CONFIRMED', 'STRONG')) and str(rr.get('Target', '')) == 'VEN-000':
        vid = str(rr['Source'])
        v = VEN_BY_ID.get(vid, {})
        gids = [g for g, a in GA.items() if str(next((x['Vendor ID'] for x in R6_GRP if x['Group ID'] == g), '')) == vid]
        n += 1
        seen_dev.add(_norm(v.get('Vendor', '')))
        fr = next((c for c in GA.values() if c['gid'] in gids), None)
        CC.append({'Chain ID': f'CH-A{n - 3:03d}', 'Chain': f"{v.get('Vendor', vid)} -> HalabTech ({t.split('(')[0].strip()}) -> HalabTech customers", 'Original Developer': f"{v.get('Vendor', '')} ({vid})",
                   'Distributor / Intermediary': '-', 'Customer side (examples)': 'HalabTech clients', 'HalabTech Groups': gnames(gids), 'SKUs (#)': sum(GA[g]['skus'] for g in gids),
                   'What Is Confirmed': f"Developer documents HalabTech as {v.get('Relationship with HalabTech', '')} ({rr['Rel ID']})",
                   'What Is NOT Confirmed': 'That HalabTech\'s SKUs are fulfilled through this account (route graded in Suspected Supply Chains)',
                   'Evidence': f"R6 {rr.get('Evidence', '')}", 'Source URL': f"https://{v.get('Website', '')}" if v.get('Website') and not str(v.get('Website')).startswith('http') else str(v.get('Website', '')),
                   'Retrieved (UTC)': 'R4-R6 (2026-10-11)', 'Evidence Type': 'vendor page (authorisation)', 'Direction': 'developer -> HalabTech', 'Confidence': 'CONFIRMED' if c6.startswith('CONFIRMED') else 'STRONG'})
for t in w5_pos:
    f = F[t]
    if conf_after(t) != 'CONFIRMED':
        continue
    gids = [g for g, a in GA.items() if t in a['tids'] and W5GS.get(g, {}).get('finding') == t]
    n += 1
    name = re.sub(r'\s*\(.*$', '', f['entity'])
    CC.append({'Chain ID': f'CH-A{n - 3:03d}', 'Chain': f"{name} -> HalabTech ({listing_label(f['claim'])[:60]}) -> HalabTech customers", 'Original Developer': f['entity'],
               'Distributor / Intermediary': '-', 'Customer side (examples)': 'HalabTech clients', 'HalabTech Groups': gnames(gids), 'SKUs (#)': sum(GA[g]['skus'] for g in gids),
               'What Is Confirmed': f"Developer page lists HalabTech: {listing_label(f['claim'])}", 'What Is NOT Confirmed': "That HalabTech's SKUs are fulfilled through this account",
               'Evidence': ev([t]), 'Source URL': f.get('source_url', ''), 'Retrieved (UTC)': f.get('retrieved_utc', ''), 'Evidence Type': 'vendor page (authorisation)',
               'Direction': 'developer -> HalabTech', 'Confidence': 'CONFIRMED'})
add('Confirmed Supply Chains', list(CC[0].keys()), CC, note='Only links documented by a primary source. CH-A rows confirm the AUTHORISATION (developer names HalabTech); the fulfilment route '
    'for those SKUs is graded separately in Suspected Supply Chains. No third-party API supplier of a specific HalabTech service is documented.',
    conf_cols=['Confidence'], url_cols=['Source URL'], widths={'Chain': 60, 'Original Developer': 30, 'HalabTech Groups': 45, 'What Is Confirmed': 50, 'What Is NOT Confirmed': 40})

# 5. Suspected Supply Chains ---------------------------------------------------------------------------------------
SC = []
covered = set()
for c in D.CHAINS:
    gids = [g for g in c['groups'] if g in GA]
    covered.update(gids)
    lk = '; '.join(f'{a_}: {b_}' for a_, b_ in c['links'])
    chain = ' -> '.join(x for x in [c['dev'], c['md'] if c['md'] != '-' else '', c['api'] if c['api'] != '-' else '', f"HalabTech [{c['ht']}]", c['cust']] if x)
    f0 = F.get(c['tids'][0]) if c['tids'] else None
    SC.append({'Chain ID': c['id'], 'Chain (Developer -> Distributor -> API Supplier -> HalabTech -> Customer)': chain, 'Original Developer': c['dev'], 'Master Distributor': c['md'],
               'API / Intermediate Supplier': c['api'], 'HalabTech Role': c['ht'], 'Customer Side': c['cust'], 'HalabTech Groups': gnames(gids), 'SKUs (#)': sum(GA[g]['skus'] for g in gids),
               'Link Confidence': lk, 'Chain Confidence (weakest link)': c['conf'], 'Evidence Type': c['etype'], 'Evidence': ev(c['tids']),
               'Primary URL': (f0 or {}).get('source_url', '') if f0 else '', 'Retrieved (UTC)': (f0 or {}).get('retrieved_utc', '') if f0 else '',
               'Direction Evidence': c['direction'], 'Alternatives': c['alt'], 'Contradictions': c['contra'], 'What Would Confirm': c['confirm'], 'What Would Reject': c['reject']})
# automatic per-developer chains for remaining graded groups
auto = collections.OrderedDict()
for gid, a in GA.items():
    if gid in covered or a['conf'] not in ('STRONG', 'LIKELY', 'DISPUTED') or a['route'] == 'IN':
        continue
    k_ = (a['dev'], a['cand'], a['route'], a['conf'])
    auto.setdefault(k_, []).append(gid)
for i, ((dev, cand, route, conf), gids) in enumerate(auto.items(), 1):
    a = GA[gids[0]]
    tids = list(dict.fromkeys(t for g in gids for t in GA[g]['all_tids']))
    r6e = '; '.join(sorted({GA[g]['r6ev'] for g in gids if GA[g]['r6ev'] not in ('', 'None')}))
    mid = cand if route in ('NI', 'LC', 'FP') else '-'
    SC.append({'Chain ID': f'CH-V{i:03d}', 'Chain (Developer -> Distributor -> API Supplier -> HalabTech -> Customer)': f"{dev} -> {mid + ' -> ' if mid != '-' else ''}HalabTech [{a['status'][:60]}] -> HalabTech clients",
               'Original Developer': dev, 'Master Distributor': mid if route in ('NI', 'LC') else '-', 'API / Intermediate Supplier': cand if route in ('VA', 'FP') else '-',
               'HalabTech Role': a['status'], 'Customer Side': 'HalabTech clients', 'HalabTech Groups': gnames(gids), 'SKUs (#)': sum(GA[g]['skus'] for g in gids),
               'Link Confidence': f"{'developer -> HalabTech' if route in ('VD', 'VA', 'VR') else 'channel -> HalabTech'}: {conf}", 'Chain Confidence (weakest link)': conf,
               'Evidence Type': 'vendor page' + ('; price fingerprint' if route == 'FP' else ''), 'Evidence': '; '.join(x for x in [ev(tids), ('R6 ' + r6e) if r6e else ''] if x),
               'Primary URL': a['dev_url'], 'Retrieved (UTC)': '2026-10-11', 'Direction Evidence': ROUTE_TXT[route], 'Alternatives': 'Another distributor/reseller account; peer exchange',
               'Contradictions': a['note'] if 'contradict' in a['note'].lower() else '', 'What Would Confirm': 'SKU-name/ID sync with the vendor API; vendor statement naming HalabTech\'s account route',
               'What Would Reject': 'HalabTech SKU strings/prices matching another distributor\'s catalogue'})
add('Suspected Supply Chains', list(SC[0].keys()), SC, note='Every chain with at least one link below CONFIRMED. CH-S = curated STRONG/LIKELY, CH-D = DISPUTED, CH-U = UNKNOWN (fingerprint known, '
    'supplier unnamed), CH-V = per-developer chains generated from the group assessment.', conf_cols=['Chain Confidence (weakest link)'], url_cols=['Primary URL'],
    widths={'Chain (Developer -> Distributor -> API Supplier -> HalabTech -> Customer)': 70, 'HalabTech Groups': 45, 'Evidence': 40, 'Alternatives': 36, 'Contradictions': 36})

# 6. Website & Public API Findings -------------------------------------------------------------------------------------
WEB = []
web_tids = [t for t in ORDER if F[t]['_stream'] == 'W1'] + ['W4-09', 'V7-07', 'W4-14', 'W3-11', 'W3-12', 'W7-17', 'V7-21', 'V7-22', 'W2-07']
REL_TXT = {'W1-01': 'None (infrastructure)', 'W1-02': 'Indirect (hosting provider; candidate for resold hosting only)', 'W1-03': 'Indirect (store platform; HTD plans resold)',
           'W1-04': 'None (chat is in-house)', 'W1-05': 'None', 'W1-06': 'Downstream (HalabTech hosts chat for other servers)', 'W1-07': 'Direct (historical GsmServer label)',
           'W1-08': 'Direct (numbered unnamed sources since 2020)', 'W1-09': 'Direct (HalabTech sells API access; most services automated)', 'W1-10': 'Context (HalabTech recruits sources)',
           'W1-11': 'Context (platform history)', 'W1-12': 'Context (developer domains in SKU names)', 'W1-13': 'Content credits (in-house tool)', 'W1-14': 'None', 'W1-15': 'Downstream (2019 agents)',
           'W1-16': 'Downstream (GsmServer resells HalabTech)', 'W1-17': 'None (no shared infrastructure with candidates)', 'W1-18': 'None (no supplier-named subdomain)', 'W1-19': 'None (support platform)',
           'W4-09': 'Rejected marker', 'V7-07': 'Rejects store-field hypothesis', 'W4-14': 'Content source (news copied from a seller)', 'W3-11': 'Direction test (UnlocksPro ids are native)',
           'W3-12': 'No shared identity', 'W7-17': 'Dhru licences resold', 'V7-21': 'Redirect/404 limits evidence', 'V7-22': 'Downstream (AI bot product)', 'W2-07': 'Self-disclosure (reseller, not developer)'}
for t in web_tids:
    f = F[t]
    WEB.append({'Ref': f'{EV[t]} ({t})', 'Asset / URL': f.get('source_url', ''), 'Method': f.get('evidence_type', ''), 'Observation': f.get('claim', ''),
                'Interpretation': f.get('alternative_explanations', '') and ('Alternative: ' + f['alternative_explanations']) or '', 'Supply-Chain Relevance': REL_TXT.get(t, ''),
                'Confidence': conf_after(t), 'Limits (what it does not prove)': f.get('what_would_confirm', '') and ('Would need: ' + f['what_would_confirm']) or '', 'Tool': tool_label(f.get('tool', '')),
                'Retrieved (UTC)': f.get('retrieved_utc', '')})
for (s, nf), nid in zip(NEGS, NEG_ID):
    if s != 'W1':
        continue
    WEB.append({'Ref': nid, 'Asset / URL': nf.get('url', ''), 'Method': 'negative check', 'Observation': f"{nf.get('what_was_checked', '')}: {nf.get('result', '')}", 'Interpretation': '',
                'Supply-Chain Relevance': 'None found', 'Confidence': 'CONFIRMED (negative)', 'Limits (what it does not prove)': 'Absence on public assets only', 'Tool': tool_label(nf.get('tool', '')), 'Retrieved (UTC)': '2026-10-11'})
for name, url, txt, t in D.API_DOCS:
    WEB.append({'Ref': f'{EV[t]} ({t})', 'Asset / URL': url, 'Method': 'documented public API / integration statement', 'Observation': f'{name}: {txt}',
                'Interpretation': 'Vendor publishes an API/panel route for sellers - a plausible fulfilment channel', 'Supply-Chain Relevance': 'Route available (not proof HalabTech uses it)',
                'Confidence': 'CONFIRMED (statement exists)', 'Limits (what it does not prove)': "HalabTech's use of the API is not shown", 'Tool': tool_label(F[t].get('tool', '')), 'Retrieved (UTC)': F[t].get('retrieved_utc', '')})
add('Website & Public API Findings', list(WEB[0].keys()), WEB, note='HTML, metadata, public JS, DNS/RDAP/CT, Wayback, redirects and vendor-published API statements. No private endpoints were enumerated; '
    'shared hosting/CDN/templates are never treated as proof of supply.', conf_cols=['Confidence'], url_cols=['Asset / URL'],
    widths={'Observation': 70, 'Interpretation': 45, 'Limits (what it does not prove)': 40, 'Asset / URL': 45})

# 7. Evidence Registry -----------------------------------------------------------------------------------------------
ER = []
for r in R6_EV:
    ER.append({'EV ID': r.get('EV ID', ''), 'Round': 'R1-R6 (copied unchanged)', 'Stream / Finding Ref': r.get('Finding Ref', '') or r.get('Record Origin', ''), 'Entity': r.get('Entity', ''),
               'Role Indicated': r.get('Role Indicated', ''), 'Claim / Excerpt': r.get('Excerpt (≤20 words)', ''), 'Source URL': r.get('Source URL', ''), 'Evidence Type': r.get('Type', ''),
               'Retrieved (UTC)': r.get('Access Date', ''), 'Pub. Date': r.get('Pub. Date', ''), 'Access': r.get('Access', ''), 'Tool': r.get('Tool', ''),
               'Confidence (as reported)': r.get('Confidence', '') or r.get('Strength', ''), 'Confidence (after Phase 5)': r.get('Confidence', '') or r.get('Strength', ''),
               'Phase 5 Note': ('R6 verification: ' + str(r.get('R6 Verification'))) if r.get('R6 Verification') not in ('', None, 'None') else '',
               'Groups / Services Affected': r.get('Service', ''), 'Supports / Contradicts': r.get('S/C', '')})
for t in ORDER:
    f = F[t]
    ex = f.get('excerpt', '')
    ER.append({'EV ID': EV[t], 'Round': 'R7', 'Stream / Finding Ref': f'{t} ({STREAM_NAMES[f["_stream"]]})', 'Entity': f.get('entity', ''), 'Role Indicated': f.get('role_for_halabtech', ''),
               'Claim / Excerpt': f"{f.get('claim', '')}" + (f' | Excerpt: "{ex}"' if ex else ''), 'Source URL': f.get('source_url', ''), 'Evidence Type': f.get('evidence_type', ''),
               'Retrieved (UTC)': f.get('retrieved_utc', ''), 'Pub. Date': f.get('pub_date', ''), 'Access': f.get('access', ''), 'Tool': tool_label(str(f.get('tool', '')).split(';')[0]) + (' + 2nd tool' if ';' in str(f.get('tool', '')) else ''),
               'Confidence (as reported)': f.get('confidence', ''), 'Confidence (after Phase 5)': conf_after(t), 'Phase 5 Note': ' | '.join(P5NOTE.get(t, [])),
               'Groups / Services Affected': '; '.join(f.get('halabtech_groups_affected') or []), 'Supports / Contradicts': f.get('supports_or_contradicts', '')})
for (s, nf), nid in zip(NEGS, NEG_ID):
    ER.append({'EV ID': nid, 'Round': 'R7', 'Stream / Finding Ref': f'{s} negative check', 'Entity': nf.get('entity', ''), 'Role Indicated': '', 'Claim / Excerpt': f"Checked: {nf.get('what_was_checked', '')} -> {nf.get('result', '')}",
               'Source URL': nf.get('url', ''), 'Evidence Type': 'negative check', 'Retrieved (UTC)': '2026-10-11', 'Pub. Date': '', 'Access': '', 'Tool': tool_label(nf.get('tool', '')),
               'Confidence (as reported)': 'CONFIRMED (negative)', 'Confidence (after Phase 5)': 'CONFIRMED (negative)', 'Phase 5 Note': '', 'Groups / Services Affected': '', 'Supports / Contradicts': ''})
add('Evidence Registry', list(ER[0].keys()), ER, note=f'R1-R6 evidence copied unchanged (EV-001...EV-266, EV-020b) + R7 findings {EV[ORDER[0]]}...{EV[ORDER[-1]]} + negative checks NEG-001...{NEG_ID[-1]}. '
    "Phase-5 corrections are recorded in 'Phase 5 Note'; raw stream files are kept unmodified in the repository.", conf_cols=['Confidence (as reported)', 'Confidence (after Phase 5)'], url_cols=['Source URL'],
    widths={'Claim / Excerpt': 80, 'Entity': 30, 'Phase 5 Note': 50, 'Source URL': 40})

# 8. Unresolved Cases -----------------------------------------------------------------------------------------------
UR = []
for u in D.UNRESOLVED:
    gids = [g for g in u['groups'] if g in GA]
    UR.append(dict(u, _skus=sum(GA[g]['skus'] for g in gids), _gids=gids))
prio_rank = {'High': 0, 'Medium': 1, 'Low': 2}
UR.sort(key=lambda u: (u['status'].startswith('Resolved'), prio_rank.get(u['prio'], 3), -u['_skus']))
URR = []
for i, u in enumerate(UR, 1):
    URR.append({'Rank': i, 'Case ID': u['id'], 'Question': u['q'], 'HalabTech Groups': gnames(u['_gids']), 'SKUs (#)': u['_skus'], 'Current Best Hypothesis': u['best'],
                'Confidence': u['conf'], 'Status (R7)': u['status'], 'Missing Evidence': u['missing'], 'What Would Confirm': u['confirm'], 'What Would Reject': u['reject'],
                'Suggested R8 Method (public, lawful)': u['method'], 'Priority': u['prio']})
# largest UNKNOWN groups not covered by a curated case
covered_u = {g for u in UR for g in u['_gids']}
big_unknown = sorted([a for g, a in GA.items() if a['conf'] == 'UNKNOWN' and g not in covered_u], key=lambda a: -a['skus'])
for a in big_unknown:
    if a['skus'] < 4:
        break
    URR.append({'Rank': len(URR) + 1, 'Case ID': f"UNK-{a['gid']}", 'Question': f"Who supplies '{a['name']}'?", 'HalabTech Groups': f"{a['gid']} {a['name']}", 'SKUs (#)': a['skus'],
                'Current Best Hypothesis': a['cand'] or 'none', 'Confidence': 'UNKNOWN', 'Status (R7)': a['status'] or 'Not checked', 'Missing Evidence': 'Any vendor list, fingerprint or ID artefact',
                'What Would Confirm': 'Developer list naming HalabTech or its distributor; implied-cost match', 'What Would Reject': '-', 'Suggested R8 Method (public, lawful)': 'Vendor/Telegram/Wayback check; price fingerprint',
                'Priority': 'Medium' if a['skus'] >= 8 else 'Low'})
add('Unresolved Cases', list(URR[0].keys()), URR, note='Ranked: open cases first by priority then by SKUs affected; followed by the largest remaining UNKNOWN groups (>=4 SKUs) not covered by a case. '
    'GAP-001...GAP-022 statuses carried from R6 where re-examined.', conf_cols=['Confidence'], widths={'Question': 55, 'HalabTech Groups': 45, 'Current Best Hypothesis': 45, 'Suggested R8 Method (public, lawful)': 45})

# 9. Confidence Change Log -------------------------------------------------------------------------------------------
CL = []
for i, c in enumerate(D.CHANGES):
    tids = c['tids']
    if c['obj'].startswith('72 never-checked'):
        tids = [W5GS[g]['finding'] for g in W5GS if W5GS[g]['halabtech_on_vendor_list'] == 'LISTED']
        c = dict(c, obj=f"{len(tids)} never-checked groups whose developer lists HalabTech (W5 LISTED)")
    CL.append({'Change ID': f'CL-{22 + i:03d}', 'Object': c['obj'], 'Level': c['level'], 'Before (R6 / stream)': c['before'], 'After (R7)': c['after'], 'Reason': c['why'],
               'Evidence': ev(tids[:12]) + (f' (+{len(tids) - 12} more)' if len(tids) > 12 else ''), 'Date': DATE})
add('Confidence Change Log', list(CL[0].keys()), CL, note='Every R7 change of a prior conclusion or stream-reported confidence. Earlier sheets are not edited; their values remain as the R6 record.',
    conf_cols=['Before (R6 / stream)', 'After (R7)'], widths={'Object': 50, 'Reason': 80, 'Evidence': 40})

# 10. R7 Price Forensics -------------------------------------------------------------------------------------------------
PF = []
for catn, fn in (('Server', 'markup_server.json'), ('IMEI', 'markup_imei.json')):
    for g in load_json(f'{R7DIR}/raw/{fn}')['groups']:
        if not g.get('computed_skus'):
            continue
        gid = next((x for x in NAME2GID.get(_norm(g['group']), []) if GA[x]['catalog'] == catn), '')
        ic = g.get('implied_costs') or {}
        PF.append({'Row': f'PF-{len(PF) + 1:03d}', 'Type': 'Implied cost (group multiplier)', 'Group ID': gid, 'Group': g['group'], 'SKUs / Computed': f"{g['skus']} / {g['computed_skus']}",
                   'Inferred Multiplier': g.get('best_multiplier') or 'none shared', 'Implied Upstream Costs (USD)': '; '.join(f'{words(k, 8)} = {v}' for k, v in list(ic.items())[:8]),
                   'Compared With': '', 'Their Price(s)': '', 'Result': 'fingerprint only' if g.get('best_multiplier') else 'no single multiplier fits all computed SKUs',
                   'Confidence': '', 'Evidence': ev(['V7-03'])})
PT = [
    ('T-Mobile Premium (2 SKUs)', '120.175 / 130.625 (10:03); 121.90 / 132.50 (02:00)', 'x1.045 (10:03), x1.06 (02:00)', '115.00 / 125.00', 'GSMUnlockUSA; GsmUnlockingStore; GSMFATHER 4002#', '108.95/114.95/149.95; $90-96; $127', 'No public match', 'UNKNOWN', ['V7-01', 'W2-04', 'W2-05']),
    ('Chimera licences (999/1,499/1,899 CRD) and credits', '$99.99 / $149 / $189; $0.11', 'x1.080-1.088; x1.196', '$0.092 per credit', 'GsmEasy, GsmServer, Unlock.eu reseller tier', '$0.092', 'Match (non-discriminating among 3)', 'STRONG', ['W4-01', 'W4-02', 'V7-13']),
    ('Sigma Plus panel licences', '$8.99 / $36.66 / $60.26', '-', '$8.29-8.69 / $32.37-33.93 / $57.27-60.03', 'GsmServer panel credits', '$0.87/0.85/0.83 per credit', 'Consistent (margin 0.4-13%)', 'STRONG', ['W4-04']),
    ('Sigma activations', '$59.40 / $44.55', 'x1.10', '$54.00 / $40.50', 'GsmServer retail; GsmEasy', '$69/$49; $44.00 (6M renew)', 'GsmServer retail excluded; GsmEasy near', 'UNKNOWN', ['W4-05']),
    ('UMT / NCK / AVB', 'UMT 22.85; AVB 21.89; NCK 23.24; NCK Online 24.786/15.125/39.94', '-', '-', 'Fast Unlocking', 'UMT 20; AVB 20; NCK 22; NCK Online 25/15/40', 'Closest public prices (at/below HalabTech)', 'LIKELY', ['W4-07', 'V7-15']),
    ('Furious Gold credit', '$0.878', '-', '-', 'GsmServer; gsmfather; fmifix; centerunlock; unlockresellers', '$1.00; $0.88; $0.907; $0.96; $0.97', 'HalabTech undercuts all public offers', 'UNKNOWN', ['W4-08']),
    ('Deep Unlocker credits / 1-year', '$0.572 / $57.20', 'x1.04', '$0.55 / $55.00', 'Vendor retail', '100 CRD $95; 1000 CRD $900; annual $60', 'No public source at cost', 'UNKNOWN', ['W4-11']),
    ('Global Unlocker credit', '$0.779', 'x1.025', '$0.76', 'GsmServer; gsmserver.al', '$0.80; $0.75/0.757', 'GsmServer excluded; unpublished tier', 'UNKNOWN', ['W4-13']),
    ('Octoplus credits', '$0.107', 'x1.07', '$0.10', 'Octoplus retail; alltimeunlocker', '$0.14; $0.105 (= $0.10 x1.05)', 'Shared reseller cost $0.10', 'LIKELY', ['W4-15']),
    ('TSM / TFM credits', 'TSM computed; TFM computed', 'x1.30 / x1.11', '$0.75 / $0.90', "'Direct Source' sellers", 'TSM $0.92; TFM $0.87-0.924', 'No match', 'UNKNOWN', ['W4-19']),
    ('Signal Labs (5 SKUs)', '20.643 / 22.438 / 5.625 / 27.438 / 6.913', 'x1.15-1.25', '17.95 / 4.50 / 21.95 / ~5.53', '-', '-', 'No priced candidate found', 'UNKNOWN', ['W3-13']),
    ('Alseery Unlocker; F-KEY V.7', '$0.748; $1.134', 'x1.10; x1.05', '$0.68; $1.08', 'GSM Nigeria', '$0.68; $1.08', 'Exact match (4 SKUs, two tools)', 'LIKELY', ['W6-09', 'V7-19']),
    ('T-Mobile Clean & Paid Off (5 tiers)', '44.99 / 66.45 / 82.49 ...', 'whole-dollar offsets', '-', 'Code-GSM', '43.99 / 63.45 / 79.49 ...', 'HalabTech = Code-GSM + $1/$1/$3/$3 (identical cents)', 'DISPUTED', ['W3-01', 'V7-08']),
    ("T-Mobile 'Fully Paid / Eligible' tiers", '-', '-', '-', 'gsmunlockers.com', '29.70/35.10/55.35/76.95 = x1.35 of 22/26/41/57', 'Unnamed upstream fingerprint', 'UNKNOWN', ['V7-09']),
    ('PUBG 60 UC (AUTO API)', '$0.927', 'x1.03', '$0.90', 'FazerCards wholesale', '$0.80', 'No match (FazerCards 11-16% below)', 'UNKNOWN', ['W7-11']),
    ('Google Play Turkey (6 SKUs)', 'face TL x 0.021174', 'FX-linked', '47.227 TRY/USD', 'Market FX', '49.18-49.26 TRY/USD', 'Face-value-linked TRY source', 'UNKNOWN', ['W7-13']),
    ('iTunes UAE', '3-decimal prices', 'per-SKU', '$27.80/100 AED; $13.90/50 AED', '-', '-', 'Implied 0.278 USD/AED', 'UNKNOWN', ['W7-14']),
    ('Cerberus (3 SKUs)', '$24.99 / $39.99 / $59.99', '-', '-', 'Cerberus public prices', 'Tool Pro $50/yr; Tool Box $30/yr', 'Not one markup (contradiction)', 'LIKELY', ['W5-72']),
    ('Downstream calibration', 'HalabTech list', '-', '-', 'HOS; Eagle Unlocker; Ariqisoft; Fast Unlock; univgsm; unlockresellers; gsmlegion; Code-GSM<-GSM Nigeria',
     'x0.875-0.972; x1.05; x1.035; +$3.00; x1.08/x1.0217/x1.0143; x1.125; x0.94; +$2.00', 'Dealers undercut list by 2.8-12.5%: "cheaper" is not "upstream"', 'STRONG', ['V7-18', 'W7-06', 'W7-07', 'W7-08', 'V7-20', 'W6-17', 'W4-12', 'W6-10']),
]
for p in PT:
    PF.append({'Row': f'PF-{len(PF) + 1:03d}', 'Type': 'Fingerprint test', 'Group ID': '', 'Group': p[0], 'SKUs / Computed': p[1], 'Inferred Multiplier': p[2], 'Implied Upstream Costs (USD)': p[3],
               'Compared With': p[4], 'Their Price(s)': p[5], 'Result': p[6], 'Confidence': p[7], 'Evidence': ev(p[8])})
add('R7 Price Forensics', list(PF[0].keys()), PF, note='Dhru computes prices as cost x a percentage markup, so >=3-decimal prices expose cost x multiplier (multipliers tested x1.005-1.300). '
    'Implied costs are fingerprints to compare with candidates\' PUBLIC prices at matching timestamps; dealer tiers (2.8-12.5% below list) limit "cheaper = upstream" readings.',
    conf_cols=['Confidence'], widths={'Group': 34, 'Implied Upstream Costs (USD)': 60, 'Compared With': 34, 'Their Price(s)': 34, 'Result': 40})

# 11. R7 MCP Tool Log ------------------------------------------------------------------------------------------------------
TL = []
for i, (s, t) in enumerate(TOOLS, 1):
    TL.append({'#': i, 'Stream': f'{s} - {STREAM_NAMES[s]}', 'Tool': tool_label(str(t.get('tool', ''))), 'Raw Tool Name': t.get('tool', ''), 'Input': str(t.get('input', ''))[:500],
               'OK': 'yes' if t.get('ok') else 'no', 'Note': str(t.get('note', ''))[:400]})
add('R7 MCP Tool Log', list(TL[0].keys()), TL, note='Every tool call logged by the R7 streams (W1-W7) and the lead verifier (V7). Sandbox curl/browser egress was blocked by policy and not worked around.',
    widths={'Input': 60, 'Note': 60, 'Stream': 30})
tool_sum = collections.Counter((s, tool_label(str(t.get('tool', '')))) for s, t in TOOLS)
tool_fail = collections.Counter((s, tool_label(str(t.get('tool', '')))) for s, t in TOOLS if not t.get('ok'))

# order: dashboard first ... matches the requested list, then supporting sheets
order = ['Research Progress Dashboard', 'Complete Service Inventory', 'Supplier Intelligence', 'Confirmed Supply Chains', 'Suspected Supply Chains',
         'Website & Public API Findings', 'Evidence Registry', 'Unresolved Cases', 'Confidence Change Log', 'R7 Price Forensics', 'R7 MCP Tool Log']
SHEETS.sort(key=lambda s: order.index(s['title']))
json.dump({'sheets': SHEETS}, open(OUT_SPEC, 'w'), ensure_ascii=False)
M['tool_sum'] = {f'{s}|{t}': v for (s, t), v in tool_sum.items()}
M['tool_fail'] = {f'{s}|{t}': v for (s, t), v in tool_fail.items()}
M['ev_first'], M['ev_last'], M['neg_last'] = EV[ORDER[0]], EV[ORDER[-1]], NEG_ID[-1]
M['ev_map'] = EV
M['sheet_rows'] = {s['title']: len(s['rows']) for s in SHEETS}
M['n_confirmed_chains'] = len(CC)
M['n_suspected_chains'] = len(SC)
M['n_unresolved'] = len(URR)
M['unknown_top'] = [(a['gid'], a['name'], a['skus']) for a in sorted([a for a in GA.values() if a['conf'] == 'UNKNOWN'], key=lambda a: -a['skus'])[:15]]
M['changed_groups'] = [(a['gid'], a['name'], a['r6conf'], a['conf']) for a in GA.values() if a['r6conf'] != a['conf']]
json.dump(M, open(OUT_MET, 'w'), ensure_ascii=False, indent=1)
print('sheets:', {s['title']: len(s['rows']) for s in SHEETS})
print(json.dumps({k: v for k, v in M.items() if not isinstance(v, (dict, list))}, indent=0))
