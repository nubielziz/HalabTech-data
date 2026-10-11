import re, json, sys

md = open(sys.argv[1]).read()


def cells(line):
    line = line.strip().replace('\\|', '│')
    if line.startswith('|'):
        line = line[1:]
    if line.endswith('|'):
        line = line[:-1]
    return [c.strip().replace('│', '|') for c in line.split('|')]


def table_rows(lines, hdr):
    rows = []
    for l in lines[2:]:
        c = cells(l)
        if len(c) > len(hdr):
            c = c[:len(hdr) - 1] + [' | '.join(c[len(hdr) - 1:])]
        c += [''] * (len(hdr) - len(c))
        rows.append(dict(zip(hdr, c)))
    return rows


sheets = {}
for block in re.split(r'\n(?=### )', md):
    m = re.match(r'### 3\.(\d+) Sheet (\d+) — ([^\n(]+)', block)
    if not m:
        continue
    name = m.group(3).strip()
    block = block.split('\n## ')[0]  # stop at next top-level section
    lines = [l for l in block.split('\n') if l.strip().startswith('|')]
    if not lines:
        continue
    hdr = cells(lines[0])
    sheets[name] = {'header': hdr, 'rows': table_rows(lines, hdr)}

pc = re.search(r'## 4\. Price Cross-Store Comparison[^\n]*\n((?:\|[^\n]*\n)+)', md)
if pc:
    pl = [l for l in pc.group(1).split('\n') if l.startswith('|')]
    hdr = ['Product', 'HalabTech', 'Other stores']
    sheets['Price Comparison'] = {'header': hdr, 'rows': table_rows(pl, hdr)}

json.dump(sheets, open(sys.argv[2], 'w'), ensure_ascii=False, indent=1)
for k, v in sheets.items():
    print(k, len(v['rows']))
