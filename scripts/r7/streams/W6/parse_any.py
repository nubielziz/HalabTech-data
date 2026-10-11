"""Generic parser for Dhru-style reseller pricing pages captured as markdown/text (Exa, Firecrawl).
Handles:
  A  '| Group | | Delivery Time | Price |' + '| | name | delivery | $ p |'   (price optional, extra cols allowed)
  B  '0|##### Group' + '|Delivery Time|' + '|name| delivery|'                (ReUnlocker theme)
  D  '##### Group' + paragraphs name/delivery + '| Delivery Time | Price |' rows '| delivery | $ p |'  (cleanunlocker theme)
  E  '##### Group' + '| Delivery Time | Price |' + '| name | delivery | $ p |'                         (rgsmrio theme)
  F  Firecrawl '| ##### Group | Delivery Time | Price |' + '| ![](icon) | name<br>delivery | delivery | $ p |' (HalabTech theme)
  C  Code-GSM GSM-Tool listing: '#### $ P' / name line / '$ P.000'
Usage: python3 -I parse_any.py <capture_file> <out_json> [--split-urls]
Output: {pages:[{url, kind(imei/server/other), services:[{group, service, delivery, price_raw, price, icon}]}]}
"""
import re, json, sys, html

PRICE_RE = re.compile(r'^(?:[A-Z]{0,3}\s*\$|\$|USD|EUR|SAR|JOD|INR)?\s*([0-9][0-9,]*(?:\.[0-9]+)?)\s*(?:USD|JOD|SAR|EUR|INR|\$)?\s*$')
DELIV_HINT = re.compile(r'(minut|miniut|hour|day|instant|week|month|min\b|sec|hrs|days|^\d+\s*-\s*\d+)', re.I)


def clean_name(s):
    s = html.unescape(s)
    s = s.replace('\\[', '[').replace('\\]', ']').replace('\\|', '|').replace('│', '|').replace('\\#', '#').replace('\\_', '_').replace('\\*', '*')
    s = re.sub(r'!\[[^\]]*\]\([^)]*\)', '', s)
    s = re.sub(r'<br\s*/?>.*$', '', s)
    s = re.sub(r'\s*\|\s*', ' | ', s)
    s = re.sub(r'\s+', ' ', s).strip()
    s = s.strip('*').strip()
    return s


def parse_price(c):
    c = c.strip().replace(',', '')
    m = PRICE_RE.match(c)
    if m:
        try:
            return float(m.group(1))
        except Exception:
            return None
    return None


def split_pages(text):
    idx = [m.start() for m in re.finditer(r'^URL: ', text, re.M)]
    if not idx:
        return [('', text)]
    pages = []
    for i, s in enumerate(idx):
        e = idx[i + 1] if i + 1 < len(idx) else len(text)
        seg = text[s:e]
        url = seg.split('\n', 1)[0][5:].strip()
        pages.append((url, seg))
    return pages


def parse_codegsm(seg):
    out = []
    lines = [l.strip() for l in seg.split('\n')]
    group = ''
    i = 0
    while i < len(lines):
        l = lines[i]
        mg = re.match(r'^##\s+(.+)$', l)
        if mg and not l.startswith('###'):
            # '## Group' headings (also used for service detail titles); keep last seen
            group = mg.group(1).strip()
        m = re.match(r'^####\s*\$\s*([0-9.,]+)\s*$', l)
        if m:
            # next non-empty line(s): optional '##### DELIVERY TIME : x', then name, then '$ x.000'
            j = i + 1; deliv = ''
            name = None
            while j < len(lines) and j < i + 8:
                if not lines[j]:
                    j += 1; continue
                md = re.match(r'^#####\s*DELIVERY TIME\s*:\s*(.+)$', lines[j], re.I)
                if md:
                    deliv = md.group(1); j += 1; continue
                name = lines[j]; break
            if name:
                k = j + 1
                p2 = None
                while k < len(lines) and k < j + 4:
                    mm = re.match(r'^\$\s*([0-9.,]+)$', lines[k])
                    if mm:
                        p2 = mm.group(1); break
                    k += 1
                price = float(m.group(1).replace(',', ''))
                if p2:
                    try:
                        price = float(p2.replace(',', ''))
                    except Exception:
                        pass
                out.append({'group': group, 'service': clean_name(name), 'delivery': deliv, 'price_raw': '$ ' + m.group(1), 'price': price, 'icon': ''})
            i = j
        i += 1
    return out


def parse_generic(seg):
    out = []
    group = None
    has_icon_col = False
    n_after = 0          # number of cells after 'Delivery Time' in header (price + extras)
    pending = []         # paragraphs (format D)
    in_table = False
    d_queue = []         # (name, delivery) for format D
    pending_row = None
    mode_alt = None
    for raw in seg.split('\n'):
        s = raw.strip()
        if not s:
            continue
        # group headers
        m = re.match(r'^\d*\|?\s*#####\s*(.+?)\s*$', s)
        if m and 'Delivery Time' not in s:
            group = clean_name(m.group(1)); pending = []; d_queue = []; in_table = False
            continue
        if s.startswith('|') and 'Delivery Time' in s:
            cells = [c.strip() for c in s.strip().strip('|').split('|')]
            if cells[:3] == ['Service', 'Price', 'Delivery Time'] or cells[:4] == ['', 'Credit', 'Type', 'Delivery Time']:
                # GSM-Tool style (xpertunlock) or productsandservices style (gsmnigeria): group = previous paragraph
                mode_alt = 'G' if cells[0] == 'Service' else 'H'
                if pending:
                    group = clean_name(pending[-1])
                pending = []
                in_table = True
                continue
            mode_alt = None
            if cells and cells[0].startswith('#####'):
                # Firecrawl HalabTech theme: | ##### Group | Delivery Time | Price |
                group = clean_name(cells[0].lstrip('#').strip())
                has_icon_col = True
                k = cells.index('Delivery Time')
                n_after = len(cells) - k - 1
                in_table = True; continue
            k = cells.index('Delivery Time') if 'Delivery Time' in cells else None
            if k is None:
                continue
            if k > 0:
                # format A: group name = cells before the empty cell preceding Delivery Time
                gcells = cells[:k]
                while gcells and gcells[-1] == '':
                    gcells = gcells[:-1]
                group = clean_name(' | '.join(gcells))
                has_icon_col = True
            else:
                has_icon_col = False
                # format D: build queue from pending paragraphs (name, delivery pairs)
                d_queue = []
                pp = [p for p in pending if not p.startswith('Show only') and not p.startswith('All Group')]
                for a in range(0, len(pp) - 1, 2):
                    d_queue.append((pp[a], pp[a + 1]))
                pending = []
            n_after = len(cells) - k - 1
            in_table = True
            continue
        if s.startswith('|') and not s.endswith('|') and len(s) > 3:
            # ReUnlocker server theme: '|Name' newline 'Delivery' newline '| Delivery|'
            pending_row = clean_name(s.lstrip('|'))
            continue
        if s.startswith('|'):
            if re.match(r'^\|\s*-{3}', s):
                continue
            cells = [c.strip() for c in s.strip().strip('|').split('|')]
            if all((c == '' or c == '**' or re.fullmatch(r'\d+', c)) for c in cells):
                continue
            if group is None:
                continue
            if mode_alt == 'G' and len(cells) >= 3:
                out.append({'group': group, 'service': clean_name(' | '.join(cells[:-2])), 'delivery': cells[-1], 'price_raw': cells[-2], 'price': parse_price(cells[-2]), 'icon': ''})
                continue
            if mode_alt == 'H' and len(cells) >= 4:
                out.append({'group': group, 'service': clean_name(' | '.join(cells[:-3])), 'delivery': cells[-1], 'price_raw': cells[-3], 'price': parse_price(cells[-3]), 'icon': ''})
                continue
            icon = ''
            if has_icon_col and cells:
                mi = re.search(r'\((https?://[^)]+)\)', cells[0])
                icon = mi.group(1) if mi else ''
                if cells[0] == '' or cells[0].startswith('!['):
                    cells = cells[1:]
            # drop trailing empty/bare-$ cells beyond expected
            tail = cells[-n_after:] if n_after else []
            body = cells[:-n_after] if n_after else cells
            price_raw = tail[0] if tail else ''
            price = parse_price(price_raw) if price_raw else None
            if not body:
                continue
            delivery = body[-1]
            namecells = body[:-1]
            if not namecells:
                if pending_row:
                    out.append({'group': group, 'service': pending_row, 'delivery': delivery, 'price_raw': price_raw, 'price': price, 'icon': icon})
                    pending_row = None
                    continue
                # format D row: | delivery | $ p |
                if d_queue:
                    nm, dl = d_queue.pop(0)
                    out.append({'group': group, 'service': clean_name(nm), 'delivery': delivery, 'price_raw': price_raw, 'price': price, 'icon': icon})
                continue
            name = ' | '.join(namecells)
            # Firecrawl theme: name<br>delivery
            out.append({'group': group, 'service': clean_name(name), 'delivery': delivery, 'price_raw': price_raw, 'price': price, 'icon': icon})
            continue
        # paragraph line
        pending.append(s)
        if len(pending) > 60:
            pending = pending[-60:]
    return out


def kind_of(url):
    u = url.lower()
    if 'imei' in u:
        return 'imei'
    if 'server' in u:
        return 'server'
    if 'remote' in u:
        return 'remote'
    return 'other'


def main():
    src, outp = sys.argv[1], sys.argv[2]
    text = open(src, encoding='utf-8', errors='replace').read()
    if src.endswith('.json'):
        try:
            d = json.loads(text)
            if isinstance(d, list):
                text = '\n'.join(x.get('text', '') for x in d if isinstance(x, dict))
            elif isinstance(d, dict) and 'markdown' in d:
                text = 'URL: ' + d.get('metadata', {}).get('sourceURL', d.get('url', '')) + '\n' + d['markdown']
        except Exception:
            pass
    pages = []
    for url, seg in split_pages(text):
        if 'code-gsm.com' in url and '#### $' in seg:
            svcs = parse_codegsm(seg)
        else:
            svcs = parse_generic(seg)
        pages.append({'url': url, 'kind': kind_of(url), 'n': len(svcs), 'chars': len(seg), 'services': svcs})
        print(url, kind_of(url), 'services', len(svcs), 'groups', len(set(s['group'] for s in svcs)), 'priced', sum(1 for s in svcs if s['price'] is not None))
    json.dump({'source': src, 'pages': pages}, open(outp, 'w'), ensure_ascii=False, indent=1)


if __name__ == '__main__':
    main()
