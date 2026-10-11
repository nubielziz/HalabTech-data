import re, json, sys
src, out = sys.argv[1], sys.argv[2]
md = open(src).read()
lines = md.split('\n')
groups = []; cur=None; pending_num=None
rows=[]
for ln in lines:
    s = ln.strip().replace('\\|', '│')
    if re.fullmatch(r'\d{1,3}', s):
        pending_num = int(s); continue
    m = re.match(r'^\|\s*#####\s*(.*?)\s*\|\s*Delivery Time\s*\|\s*Price\s*\|', s)
    if m:
        cur = {'num': pending_num, 'name': m.group(1).strip().replace('\\[','[').replace('\\]',']').replace('│','|')}
        groups.append(cur); pending_num=None; continue
    if cur and s.startswith('|') and not s.startswith('| ---'):
        cells = [c.strip() for c in s.strip('|').split('|')]
        if len(cells) >= 4:
            icon = re.search(r'\((https?://[^)]+)\)', cells[0])
            name_cell = cells[1]
            name = re.split(r'<br>', name_cell)[0].strip().replace('│','|')
            name = re.sub(r'!\[\]\([^)]*\)','',name).replace('\\[','[').replace('\\]',']').strip()
            rows.append({'group_num': cur['num'], 'group': cur['name'], 'service': name,
                         'delivery': cells[2], 'price_raw': cells[3],
                         'icon': icon.group(1) if icon else ''})
for r in rows:
    p = re.sub(r'[^0-9.]', '', r['price_raw'].replace(',', ''))
    try: r['price_usd'] = float(p) if p else None
    except: r['price_usd'] = None
json.dump({'groups': groups, 'services': rows}, open(out,'w'), ensure_ascii=False, indent=1)
print('groups', len(groups), 'services', len(rows))
nums=[g['num'] for g in groups]; print('num range', min(x for x in nums if x is not None), max(x for x in nums if x is not None), 'None nums', nums.count(None))
missing=[i for i in range(0,max(x for x in nums if x is not None)+1) if i not in nums]; print('missing nums', missing[:50])
