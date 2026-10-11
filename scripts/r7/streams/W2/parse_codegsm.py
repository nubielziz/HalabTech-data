import re, json, sys
path = sys.argv[1]
lines = open(path, encoding='utf-8').read().split('\n')
pairs = []
for i, l in enumerate(lines):
    m = re.match(r'^\s*\$\s*([0-9]+\.[0-9]{3})\s*$', l)
    if m:
        # find previous non-empty line
        j = i - 1
        while j >= 0 and not lines[j].strip():
            j -= 1
        name = lines[j].strip()
        # delivery: next non-empty line
        k = i + 1
        while k < len(lines) and not lines[k].strip():
            k += 1
        deliv = lines[k].strip() if k < len(lines) else ''
        pairs.append({'name': name, 'price': float(m.group(1)), 'delivery': deliv, 'line': i + 1})
json.dump(pairs, open(sys.argv[2], 'w'), ensure_ascii=False, indent=1)
print(len(pairs))
