"""Build HalabTech_Complete_Supply_Chain_Research.xlsx.

Inputs (all JSON):
  prior_sheets.json  - Rounds 1-3 tables reconstructed from the Markdown report (preserved verbatim)
  server_catalog.json, imei_catalog.json - Firecrawl scrape of the public pricing pages (Round 4)
  curated.json       - Round 4-6 findings curated from the research agents and own verification
Usage: python3 build_workbook.py <raw_dir> <curated.json> <out.xlsx>
"""
import json, sys, collections, re, os
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.table import Table, TableStyleInfo

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from classify import categorise, delivery_model  # noqa: E402

RAW, CURATED, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
prior = json.load(open(os.path.join(RAW, 'prior_sheets.json')))
server = json.load(open(os.path.join(RAW, 'server_catalog.json')))
imei = json.load(open(os.path.join(RAW, 'imei_catalog.json')))
cur = json.load(open(CURATED))
VERIFIED = cur['meta']['verification_date']

HDR_FILL = PatternFill('solid', fgColor='1F3864')
HDR_FONT = Font(bold=True, color='FFFFFF')
PRIOR_FILL = PatternFill('solid', fgColor='F2F2F2')
CONF_FILLS = {
    'CONFIRMED': 'C6EFCE', 'STRONG': 'DDEBF7', 'STRONG EVIDENCE': 'DDEBF7', 'LIKELY': 'FFF2CC',
    'UNKNOWN': 'FCE4D6', 'DISPUTED': 'F4B6C2',
}
THIN = Side(style='thin', color='BFBFBF')
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
WRAP = Alignment(wrap_text=True, vertical='top')

wb = Workbook()
wb.remove(wb.active)
table_names = set()


def conf_fill(val):
    if not isinstance(val, str):
        return None
    up = val.upper()
    for k, c in CONF_FILLS.items():
        if up.startswith(k):
            return PatternFill('solid', fgColor=c)
    return None


def write_sheet(name, header, rows, widths=None, conf_cols=(), prior_flag_col=None, url_cols=(), freeze='B2', note=None):
    ws = wb.create_sheet(name[:31])
    start = 1
    if note:
        ws.cell(row=1, column=1, value=note).font = Font(italic=True, color='595959')
        start = 2
    for ci, h in enumerate(header, 1):
        c = ws.cell(row=start, column=ci, value=h)
        c.fill, c.font, c.alignment, c.border = HDR_FILL, HDR_FONT, Alignment(wrap_text=True, vertical='center'), BORDER
    for ri, r in enumerate(rows, start + 1):
        is_prior = prior_flag_col and str(r.get(prior_flag_col, '')).startswith('R1-3')
        for ci, h in enumerate(header, 1):
            v = r.get(h, '')
            if isinstance(v, (list, tuple)):
                v = '; '.join(str(x) for x in v)
            c = ws.cell(row=ri, column=ci, value=v)
            c.alignment, c.border = WRAP, BORDER
            if is_prior:
                c.fill = PRIOR_FILL
            if h in conf_cols:
                f = conf_fill(v)
                if f:
                    c.fill = f
            if h in url_cols and isinstance(v, str) and v.startswith('http') and ' ' not in v and ';' not in v:
                c.hyperlink = v
                c.font = Font(color='0563C1', underline='single')
    for ci, h in enumerate(header, 1):
        w = (widths or {}).get(h)
        if w is None:
            sample = [len(str(h))] + [len(str(r.get(h, ''))) for r in rows[:200]]
            w = min(max(10, int(sorted(sample)[int(len(sample) * 0.9)] * 0.9) + 2), 60)
        ws.column_dimensions[get_column_letter(ci)].width = w
    ws.freeze_panes = ws.cell(row=start + 1, column=2) if freeze else None
    if rows:
        ref = f"A{start}:{get_column_letter(len(header))}{start + len(rows)}"
        tname = re.sub(r'[^A-Za-z0-9]', '', name)[:30] or 'T'
        while tname in table_names:
            tname += 'x'
        table_names.add(tname)
        t = Table(displayName=tname, ref=ref)
        t.tableStyleInfo = TableStyleInfo(name='TableStyleLight1', showRowStripes=False)
        ws.add_table(t)
    return ws


def tag_prior(rows, extra=None):
    out = []
    for r in rows:
        r2 = {'Record Origin': 'R1-3 (preserved)'}
        r2.update(r)
        if extra:
            r2.update(extra.get(r.get(list(r.keys())[0]), {}))
        out.append(r2)
    return out


# ---------------------------------------------------------------- group + service tables
group_map = cur['group_map']            # group name -> overrides
vendor_by_group = cur['vendor_by_group']  # group name -> [brand, VEN-id or '']

group_rows, service_rows = [], []
gid_by_name = {}
svc_counter = 34
prior_links = cur.get('prior_service_links', {})  # catalog key -> SVC-0xx
for catalog, data, prefix in (('Server', server, 'GRP-S'), ('IMEI', imei, 'GRP-I')):
    by = collections.defaultdict(list)
    for s in data['services']:
        by[s['group']].append(s)
    for gi, g in enumerate(data['groups']):
        name = g['name']
        gid = f"{prefix}-{gi:03d}"
        gid_by_name[(catalog, name)] = gid
        svcs = by[name]
        prices = [s['price_usd'] for s in svcs if s['price_usd'] is not None]
        cat = categorise(catalog, name)
        model, model_note = delivery_model(name, svcs)
        brand, ven = vendor_by_group.get(name, [re.sub(r'\s+', ' ', name).strip(), ''])
        ov = group_map.get(name, {})
        status = ov.get('status_at_vendor', 'Not checked' if catalog == 'Server' else 'n/a (IMEI service)')
        row = {
            'Group ID': gid, 'Catalog': catalog, 'Display #': g['num'] if g['num'] is not None else gi,
            'Group Name': name, 'Services': len(svcs),
            'Min Price (USD)': min(prices) if prices else None, 'Max Price (USD)': max(prices) if prices else None,
            'Category': cat, 'Original Vendor / Brand': brand, 'Vendor ID': ven,
            'HalabTech Status at Vendor': status,
            'Fulfilment Model': ov.get('fulfilment_model', model),
            'Candidate Upstream / Intermediary': ov.get('candidate_upstream', ''),
            'Upstream Confidence': ov.get('upstream_confidence', 'UNKNOWN'),
            'Confirmed Direct API Supplier': ov.get('confirmed_api_supplier', 'None identified'),
            'Evidence IDs': ov.get('evidence', ''),
            'Priority': ov.get('priority', ''),
            'Notes': '; '.join(x for x in [model_note, ov.get('notes', '')] if x),
            'Last Verified': VERIFIED,
        }
        group_rows.append(row)
        for s in svcs:
            svc_counter += 1
            key = f"{catalog}|{name}|{s['service']}"
            service_rows.append({
                'Research ID': f"SVC-{svc_counter:04d}", 'Record Origin': 'R4 (catalog)', 'Catalog': catalog,
                'Group ID': gid, 'Group': name, 'Service Name (as listed)': s['service'], 'Category': cat,
                'Price (USD)': s['price_usd'], 'Delivery': s['delivery'].replace('<br>', ' '),
                'Public Service ID': cur.get('public_pids', {}).get(key, ''),
                'Source URL': f"https://server.halabtech.com/resellerpricing/{'server' if catalog == 'Server' else 'imei'}",
                'Orig. Vendor': brand, 'Vendor ID': ven,
                'HalabTech Status at Vendor': status,
                'Fulfilment Model': row['Fulfilment Model'],
                'Actual Supplier': ov.get('confirmed_api_supplier', '') if ov.get('confirmed_api_supplier', 'None identified') != 'None identified' else '',
                'Potential Suppliers': row['Candidate Upstream / Intermediary'],
                'Confidence (R6)': row['Upstream Confidence'],
                'Status': ov.get('svc_status', 'Open' if row['Upstream Confidence'] in ('UNKNOWN', 'LIKELY') else 'Partial'),
                'Evidence': row['Evidence IDs'], 'Prior Record': prior_links.get(key, ''),
                'First Seen': VERIFIED, 'Last Verified': VERIFIED,
            })

# prior 34 records, preserved, with R6 update columns
prior_svc_updates = cur.get('prior_service_updates', {})
prior_svc_rows = []
for r in prior['All Services']['rows']:
    u = prior_svc_updates.get(r['Research ID'], {})
    prior_svc_rows.append({
        'Research ID': r['Research ID'], 'Record Origin': 'R1-3 (preserved)', 'Catalog': 'IMEI' if 'imei' in r['Notes'].lower() else 'Server',
        'Group ID': u.get('group_id', ''), 'Group': u.get('group', ''),
        'Service Name (as listed)': r['Service Name (as listed)'], 'Category': r['Category'],
        'Price (USD)': r['Price'], 'Delivery': r['Delivery'], 'Public Service ID': u.get('pid', ''),
        'Source URL': u.get('url', 'https://server.halabtech.com/resellerpricing/server'),
        'Orig. Vendor': r['Orig. Vendor'], 'Vendor ID': r['Orig. Vendor'],
        'HalabTech Status at Vendor': u.get('status_at_vendor', ''),
        'Fulfilment Model': u.get('fulfilment_model', ''),
        'Actual Supplier': r['Actual Supplier'], 'Potential Suppliers': r['Potential'],
        'Confidence (R1-3)': r['Confidence'], 'Confidence (R6)': u.get('confidence', r['Confidence']),
        'Status': u.get('status', r['Status']), 'Evidence': u.get('evidence', ''),
        'Prior Record': '', 'Notes': '; '.join(x for x in [r['Notes'], u.get('note', '')] if x),
        'First Seen': '2026-10-11 (R1-3)', 'Last Verified': VERIFIED,
    })

# ---------------------------------------------------------------- sheets
dash = cur['dashboard']
write_sheet('Dashboard', ['Metric', 'Rounds 1-3', 'Rounds 4-6 (now)', 'Change / Comment'], dash, widths={'Metric': 48, 'Rounds 1-3': 22, 'Rounds 4-6 (now)': 22, 'Change / Comment': 80}, freeze=None,
            note=f"HalabTech supply-chain research workbook - Rounds 1-6 - verification date {VERIFIED}. Grey rows = preserved Rounds 1-3 content.")

svc_hdr = ['Research ID', 'Record Origin', 'Catalog', 'Group ID', 'Group', 'Service Name (as listed)', 'Category', 'Price (USD)', 'Delivery',
           'Public Service ID', 'Source URL', 'Orig. Vendor', 'Vendor ID', 'HalabTech Status at Vendor', 'Fulfilment Model',
           'Actual Supplier', 'Potential Suppliers', 'Confidence (R1-3)', 'Confidence (R6)', 'Status', 'Evidence', 'Prior Record',
           'Notes', 'First Seen', 'Last Verified']
write_sheet('All Services', svc_hdr, prior_svc_rows + service_rows,
            widths={'Service Name (as listed)': 60, 'Group': 28, 'Source URL': 24, 'Potential Suppliers': 40, 'Notes': 40, 'HalabTech Status at Vendor': 30},
            conf_cols=('Confidence (R1-3)', 'Confidence (R6)'), prior_flag_col='Record Origin', url_cols=('Source URL',),
            note='SVC-001..034 = Rounds 1-3 representative records (preserved). SVC-0035+ = every public SKU scraped with Firecrawl in Round 4. Public Service ID (Dhru "pid") only where seen on a public product URL.')

write_sheet('Service Groups', list(group_rows[0].keys()), group_rows,
            widths={'Group Name': 34, 'Original Vendor / Brand': 26, 'HalabTech Status at Vendor': 34, 'Candidate Upstream / Intermediary': 44, 'Notes': 50, 'Evidence IDs': 22},
            conf_cols=('Upstream Confidence',),
            note='One row per public catalog group (321 Server + 62 IMEI). "HalabTech Status at Vendor" = authorised-channel status only; "Confirmed Direct API Supplier" requires explicit evidence.')

for sheet, key in (('Original Vendors', 'vendors'), ('Suppliers and Distributors', 'suppliers'), ('Supply Chain Relationships', 'relationships'),
                   ('Evidence Register', 'evidence'), ('Unknown Suppliers', 'unknown'), ('Research Gaps', 'gaps'),
                   ('Research History', 'history'), ('Website Inventory', 'inventory'), ('Conflicts and Corrections', 'conflicts'),
                   ('Next Research Plan', 'plan'), ('Price Comparison', 'prices')):
    spec = cur['sheets'][key]
    hdr = spec['header']
    rows = tag_prior(prior[sheet]['rows'], spec.get('prior_updates')) if sheet in prior else []
    rows += spec['rows']
    for r in rows:
        r.setdefault('Record Origin', 'R4-6 (new)')
    conf = tuple(h for h in hdr if 'Confidence' in h or h in ('Strength', 'Resolution', 'Status (R6)'))
    write_sheet(sheet, hdr, rows, widths=spec.get('widths'), conf_cols=conf, prior_flag_col='Record Origin',
                url_cols=tuple(h for h in hdr if 'URL' in h or h == 'Website'), note=spec.get('note'))

for key in ('tool_log', 'progress'):
    spec = cur['sheets'][key]
    write_sheet(spec['title'], spec['header'], spec['rows'], widths=spec.get('widths'), note=spec.get('note'),
                conf_cols=tuple(h for h in spec['header'] if 'Confidence' in h))

src_rows = []
for m in re.finditer(r'^(\d+)\. \[(.*?)\]\((https?://[^)]+)\)', open(os.path.join(RAW, 'prior_report_r1-3.md')).read(), re.M):
    src_rows.append({'Ref #': int(m.group(1)), 'Title': m.group(2).replace('\\[', '[').replace('\\]', ']'), 'URL': m.group(3), 'Record Origin': 'R1-3 (preserved)'})
write_sheet('R1-3 Sources', ['Ref #', 'Title', 'URL', 'Record Origin'], src_rows, widths={'Title': 70, 'URL': 80}, url_cols=('URL',), prior_flag_col='Record Origin',
            note='Numbered source list of the Rounds 1-3 report ([1]…[48]), preserved verbatim.')

wb.save(OUT)
print('saved', OUT, 'sheets:', wb.sheetnames, 'services:', len(prior_svc_rows) + len(service_rows), 'groups:', len(group_rows))
