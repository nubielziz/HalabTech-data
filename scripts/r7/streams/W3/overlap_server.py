import json, re, sys
up_md = open(sys.argv[1]).read()
ht = json.load(open(sys.argv[2]))
# UnlocksPro groups and services
groups = re.findall(r'^\| ([^|\n]+?) \| \| Delivery Time \|', up_md, re.M)
rows = re.findall(r'^\| \| (.+?) \| [^|]*\|$', up_md, re.M)
def norm(s):
    s = re.sub(r'^#\d+\s*', '', s.strip())
    s = re.sub(r'\s+(Miniutes|Minutes|Instant|Hours|\d+-\d+ Miniutes|0 Instant|0-3 Hours|1-5 Miniutes)$', '', s)
    return re.sub(r'\s+', ' ', s).strip().lower()
up_names = {norm(r) for r in rows}
ht_groups = {g['name'].strip().lower() for g in ht['groups']}
ht_names = {re.sub(r'\s+',' ',s['service']).strip().lower() for s in ht['services']}
gov = sorted(g for g in groups if g.strip().lower() in ht_groups)
sov = sorted(n for n in up_names if n in ht_names)
print('UnlocksPro server groups:', len(groups), ' services:', len(rows))
print('HalabTech server groups:', len(ht_groups), ' services:', len(ht_names))
print('Exact group-name overlap:', len(gov))
print('Exact service-name overlap (after stripping #ID and delivery):', len(sov))
for g in gov: print('  G:', g)
print('--- sample service overlaps')
for n in sov[:60]: print('  S:', n)
ids = [int(x) for x in re.findall(r'^\| \| #(\d+) ', up_md, re.M)]
print('ID range', min(ids), max(ids), 'count', len(ids))
