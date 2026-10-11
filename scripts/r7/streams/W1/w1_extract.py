"""W1 web-infra extractor. Usage: python3 -I w1_extract.py <firecrawl_json_or_html> [label]
Prints meta tags, JSON-LD, generator, external hosts for script/link/iframe/img, analytics/tag IDs,
URLs found inside inline scripts, and a host frequency table."""
import json, re, sys, collections
from html.parser import HTMLParser
from urllib.parse import urlparse

fn = sys.argv[1]
label = sys.argv[2] if len(sys.argv) > 2 else fn
raw = open(fn, encoding='utf-8', errors='replace').read()
html = raw
try:
    d = json.loads(raw)
    if isinstance(d, dict) and 'rawHtml' in d:
        html = d['rawHtml']
except Exception:
    pass

class P(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.metas = []; self.tags = collections.defaultdict(list); self.scripts = []; self._in_script = None
        self.ldjson = []; self.forms = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'meta':
            self.metas.append(a)
        if tag == 'script':
            self._in_script = a
            if a.get('src'):
                self.tags['script'].append(a['src'])
        if tag == 'link' and a.get('href'):
            self.tags['link:' + (a.get('rel') or '')].append(a['href'])
        if tag == 'iframe' and a.get('src'):
            self.tags['iframe'].append(a['src'])
        if tag in ('img', 'source') and (a.get('src') or a.get('data-src')):
            self.tags['img'].append(a.get('src') or a.get('data-src'))
        if tag == 'a' and a.get('href'):
            self.tags['a'].append(a['href'])
        if tag == 'form':
            self.forms.append(a)
    def handle_endtag(self, tag):
        if tag == 'script':
            self._in_script = None
    def handle_data(self, data):
        if self._in_script is not None:
            if (self._in_script.get('type') or '').lower() == 'application/ld+json':
                self.ldjson.append(data.strip())
            elif data.strip():
                self.scripts.append(data)

p = P(); p.feed(html)
print('#####', label, 'html_len', len(html))
print('--- META')
for m in p.metas:
    k = m.get('name') or m.get('property') or m.get('http-equiv') or m.get('itemprop') or m.get('charset')
    if k:
        print('  ', k, '=>', (m.get('content') or '')[:220])
print('--- JSON-LD blocks', len(p.ldjson))
for j in p.ldjson:
    print('  ', j[:1500].replace('\n', ' '))
print('--- FORMS')
for f in p.forms:
    print('  ', f)

def host(u):
    if u.startswith('//'):
        u = 'https:' + u
    try:
        return urlparse(u).netloc.lower()
    except Exception:
        return ''

for t in sorted(p.tags):
    if t == 'a':
        continue
    vals = p.tags[t]
    ext = [v for v in vals if host(v)]
    print('--- TAG', t, 'total', len(vals), 'absolute', len(ext))
    seen = set()
    for v in vals:
        if v in seen:
            continue
        seen.add(v)
        if t.startswith('link') or t in ('script', 'iframe'):
            print('    ', v[:200])
    if t == 'img':
        print('     img hosts:', collections.Counter(host(v) or '(relative)' for v in vals).most_common(30))

ahosts = collections.Counter(host(v) or '(relative)' for v in p.tags['a'])
print('--- <a> hosts', ahosts.most_common(80))
print('--- <a> external hrefs (non-halabtech)')
seen = set()
for v in p.tags['a']:
    h = host(v)
    if h and 'halabtech' not in h and v not in seen:
        seen.add(v); print('    ', v[:220])

allinline = '\n'.join(p.scripts)
print('--- inline scripts', len(p.scripts), 'chars', len(allinline))
ID_PATTERNS = {
    'GA4': r'\bG-[A-Z0-9]{6,12}\b', 'UA': r'\bUA-\d{4,10}-\d{1,4}\b', 'GTM': r'\bGTM-[A-Z0-9]{4,9}\b',
    'AW': r'\bAW-\d{6,12}\b', 'adsense': r'ca-pub-\d{10,20}', 'fbpixel': r"fbq\(\s*['\"]init['\"]\s*,\s*['\"](\d+)",
    'yandex': r'ym\(\s*(\d{5,10})', 'clarity': r'clarity\.ms/tag/([a-z0-9]+)|clarity["\']\s*,\s*["\']script["\']\s*,\s*["\']([a-z0-9]+)',
    'tawk': r'embed\.tawk\.to/([0-9a-f]{24})/([0-9a-z]+)', 'crisp': r'CRISP_WEBSITE_ID\s*=\s*["\']([0-9a-f-]{36})',
    'hotjar': r'hjid\s*:\s*(\d+)', 'tiktok': r"ttq\.load\(['\"]([A-Z0-9]+)", 'recaptcha': r'recaptcha/api\.js\?render=([\w-]+)|data-sitekey=["\']([\w-]+)',
    'onesignal': r'appId\s*:\s*["\']([0-9a-f-]{36})', 'tidio': r'code\.tidio\.co/([a-z0-9]+)\.js', 'livechat': r'__lc\.license\s*=\s*(\d+)',
    'smartsupp': r"_smartsupp\.key\s*=\s*['\"]([0-9a-f]+)", 'jivo': r'code\.jivosite\.com/widget/([\w]+)', 'zoho': r'salesiq\.zoho\.com/widget\?wc=([\w]+)',
    'statcounter': r'sc_project\s*=\s*(\d+)', 'cloudflare_beacon': r'"token"\s*:\s*"([0-9a-f]{32})"', 'firebase': r'apiKey\s*:\s*["\'](AIza[\w-]{30,})',
    'whatsapp': r'wa\.me/(\d+)|api\.whatsapp\.com/send\?phone=(\d+)', 'telegram': r't\.me/([\w+]+)', 'pusher': r'Pusher\(\s*["\']([0-9a-f]+)',
}
print('--- ID PATTERNS (whole html)')
for k, rx in ID_PATTERNS.items():
    found = set()
    for m in re.finditer(rx, html):
        found.add(m.group(0)[:120])
    if found:
        print('  ', k, sorted(found)[:40])

print('--- URLs inside inline scripts')
urls = set(re.findall(r'https?://[^\s"\'<>\\)]+', allinline))
for u in sorted(urls):
    print('    ', u[:200])
print('--- relative endpoints in inline JS (url:, fetch(, $.post/$.get/ajax)')
eps = set()
for rx in [r'url\s*:\s*["\']([^"\']+)["\']', r'fetch\(\s*["\']([^"\']+)["\']', r'\$\.(?:post|get|getJSON)\(\s*["\']([^"\']+)["\']', r'action\s*=\s*["\']([^"\']+)["\']', r'\.open\(\s*["\'](?:GET|POST)["\']\s*,\s*["\']([^"\']+)']:
    for m in re.finditer(rx, allinline):
        eps.add(m.group(1)[:200])
for e in sorted(eps):
    print('    ', e)
print('--- ALL HOSTS (any absolute URL in html)')
hc = collections.Counter(host(u) for u in re.findall(r'(?:https?:)?//[A-Za-z0-9.-]+\.[A-Za-z]{2,}[^\s"\'<>]*', html))
print('   ', hc.most_common(120))
gens = re.findall(r'<meta[^>]+name=["\']generator["\'][^>]*>', html, re.I)
print('--- generator tags', gens)
cm = re.findall(r'<!--(.{0,200}?)-->', html, re.S)
print('--- HTML comments (first 40)')
for c in cm[:40]:
    c = c.strip().replace('\n', ' ')
    if c:
        print('    ', c[:200])
