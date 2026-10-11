"""Shared helpers for Round-7 curation (imported by curate_r7.py)."""
import json, re, collections
from decimal import Decimal

DATE = '2026-10-11'


def load_json(p):
    return json.load(open(p))


def words(t, n=25):
    w = str(t or '').split()
    return ' '.join(w[:n]) + (' …' if len(w) > n else '')


def tool_label(t):
    t = t or ''
    for k, v in (('firecrawl_scrape', 'Firecrawl scrape'), ('firecrawl_search', 'Firecrawl search'), ('firecrawl_developer_search', 'Firecrawl developer search'),
                 ('web_search_exa', 'Exa search'), ('web_fetch_exa', 'Exa fetch'), ('agent_run', 'Exa agent'),
                 ('Parallel_Search__web_search', 'Parallel search'), ('Parallel_Search__web_fetch', 'Parallel fetch')):
        if k in t:
            return v
    tl = t.lower()
    if 'parallel' in tl and 'fetch' in tl:
        return 'Parallel fetch'
    if 'parallel' in tl:
        return 'Parallel search'
    if 'exa' in tl and 'agent' in tl:
        return 'Exa agent'
    if 'exa' in tl and 'fetch' in tl:
        return 'Exa fetch'
    if 'exa' in tl:
        return 'Exa search'
    if 'firecrawl' in tl and 'developer' in tl:
        return 'Firecrawl developer search'
    if 'firecrawl' in tl and 'search' in tl:
        return 'Firecrawl search'
    if 'firecrawl' in tl:
        return 'Firecrawl scrape'
    if t.endswith('web_search'):
        return 'Parallel search'
    if t.endswith('web_fetch'):
        return 'Parallel fetch'
    return t


MCP_PREFIX = ('Firecrawl', 'Parallel', 'Exa')


def catalog_rows(path, catalog):
    d = load_json(path)
    out = []
    for s in d['services']:
        out.append({'catalog': catalog, 'group': s['group'], 'service': s['service'], 'price': s['price_usd'],
                    'price_raw': s['price_raw'].replace('$', '').strip(), 'delivery': s['delivery'].replace('<br>', ' ')})
    return d['groups'], out


def implied(price_raw, mult):
    try:
        return str((Decimal(price_raw.replace(',', '')) / Decimal(mult)).quantize(Decimal('0.01')))
    except Exception:
        return ''
