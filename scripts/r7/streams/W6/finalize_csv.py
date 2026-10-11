"""Add capture metadata + classification to genealogy_metrics.csv (pairwise server-vs-HalabTech metrics)."""
import csv, json, sys
W6 = sys.argv[1]
rows = list(csv.DictReader(open(W6 + '/genealogy_metrics.csv')))
fp = json.load(open(W6 + '/implied_cost_matches.json'))['summary'] if __import__('os').path.exists(W6 + '/implied_cost_matches.json') else {}
fam = json.load(open(W6 + '/fmi_family_pairs.json'))
META = {
 'reunlocker.com': ('Exa 10:11 (cache age unknown)', 'DOWNSTREAM of HalabTech (API mirror)', 'STRONG', 'HalabTech-internal SKUs (API test: TEST API IMEI; API TEST SERVICE QNT; TEST API CODE; testttttt) + HALABTECH membership group + 5 stale HalabTech White Friday bundles'),
 'mwunlocker.com': ('Exa 10:11 (600k cap; cache age unknown)', 'DOWNSTREAM of HalabTech (API mirror)', 'STRONG', "HalabTech Point group ('From Your Account on Point.halabtech.com To Server.Halabtech.com') + HALABTECH groups + 4 stale White Friday bundles; 85.5% of HT IMEI names"),
 'gsmtiger.com': ('Exa 10:11 (600k cap; cache age unknown)', 'DOWNSTREAM of HalabTech (direct + via an intermediary with #45xx IDs)', 'STRONG', 'API test SKUs + HalabTech Point + HALABTECH group twice (unprefixed and #4562-#4571 prefixed) + 5 stale White Friday bundles'),
 'univgsm.com': ('Exa 10:10 (cache age unknown)', 'DOWNSTREAM of HalabTech (API mirror, priced)', 'STRONG', 'TEST API IMEI priced 10800 = HalabTech 10000 x 1.08; [BY EDL Binary] group 29/29 SKUs = HT x 1.022; 1351#/1352# Moldova = HT x 1.0143; HalabTech Point'),
 'saudi-gsm.com': ('Exa 10:11 (cache age unknown)', 'DOWNSTREAM of HalabTech (server catalog mirror)', 'STRONG', 'HalabTech Point, API Test (TEST API CODE 0.11 = HT 0.10 x 1.1), HalabTech Syriatel/MTN/Turkcell top-up groups, HALABTECH memberships'),
 'unlockspro.com': ('Exa 10:10 (prices hidden)', 'DOWNSTREAM of HalabTech for server items (+ likely for MDM Source 1# group); IMEI direction partly unresolved', 'STRONG (HalabTech-proprietary items) / LIKELY (IMEI)', 'HTD #23459-61, HALABTECH #22876-87, DHRU SERVICE #22207-17, CDMA YEMEN #24203-07, Infinix Tecno Itel MDM Source 1# [Premium] #25579-83 (same 5 SKUs as HT)'),
 'code-gsm.com': ('Firecrawl live maxAge0 10:29 (listing rounds to $1)', 'UPSTREAM candidate / sibling (no HT branding, cheaper)', 'LIKELY', 'Same Xiaomi {{{Country}}} names incl. HT brace typos {{Kenya}}}/{{Nicaragua}}}; cheaper on 52/57 shared SKUs; FMI OFF model-matched cheaper 38/40; = GSM Nigeria + $2.00 on 45/47 shared SKUs'),
 'code-gsm.com(exa-cache)': ('Exa 10:10 (stale: Honduras $17 vs live $54)', 'superseded by live capture', '', ''),
 'gsmnigeria.com': ('Firecrawl live maxAge0 10:29 (prices in credits)', 'UPSTREAM candidate for tool-activation SKUs (or sibling); also HalabTech-credit distributor', 'LIKELY', '140 exact HT server names cheaper on 142/150 (median 0.90); equals HT implied cost for Alseery 0.68, F-KEY 1.08, Fast Unlocker 0.56-0.57; shares group typo Hydra Digital Actiavtion'),
 'gsmnigeria.com(exa-cache)': ('Exa 10:21 (cache age unknown)', 'superseded by live capture', '', ''),
 'best4unlock.us': ('Exa 10:10 (cache age unknown)', 'SIBLING (shares Apple-check source incl. Prheck typo)', 'LIKELY', '33 Apple Check Service names incl. Blacklist Prheck; prices mixed (cheaper 22/dearer 41)'),
 'gxunlocker.com': ('Exa 10:21 (prices hidden)', 'DOWNSTREAM (of HalabTech or a HalabTech mirror) - probable', 'LIKELY', '13 HT IMEI group names incl. [NEW JDM V4 V5]/[V4 V5] SAMSUNG Repair Netowrk/Demo/Unlock (typo), Altice Dominican Republic x10 names'),
 'adunlocker.com': ('Exa 10:21 (prices shown as $0)', 'SIBLING/DOWNSTREAM (EDL Binary names) - unresolved', 'UNKNOWN', '28 exact HT IMEI names (EDL repair model lists, Apple checks); no branding'),
 'gsmfather.com': ('Exa 10:28 (prices hidden) + store/product pages', 'UPSTREAM origin of HT Moldova Network names (NNNN# IDs)', 'LIKELY', 'HT 1351#/1352# Orange Moldova = GSMFATHER service IDs 1351/1352 (own-ID naming); only 4 HT names shared overall'),
 'tinunlock.com': ('Exa 10:21 (prices hidden)', 'SIBLING via a different NNNN# upstream (T-Mobile Clean & Paid Off 3277#-3281#)', 'UNKNOWN', 'T-Mobile Clean & Paid Off names identical to HT/Code-GSM but prefixed 3277#-3281#'),
}
for r in rows:
    m = META.get(r['server'])
    if not m:
        if int(r.get('halabtech_branded_items') or 0) > 0:
            m = ('Exa (cache age unknown)', 'DOWNSTREAM reseller of HalabTech products (memberships/credits); otherwise unrelated catalog', 'STRONG' if int(r['halabtech_branded_items']) >= 5 else 'LIKELY', 'HalabTech-branded membership/credit SKUs; few HT IMEI names')
        else:
            m = ('Exa (cache age unknown)', 'UNRELATED / insufficient overlap', 'UNKNOWN', 'low overlap')
    r['capture'] = m[0]; r['classification'] = m[1]; r['confidence'] = m[2]; r['key_basis'] = m[3]
    s = fp.get(r['server'], {})
    r['implied_cost_equal_hits'] = s.get('equals_implied_cost', 0)
    fpairs = fam.get(r['server'], [])
    r['fmi_family_matched'] = len(fpairs)
    r['fmi_family_cheaper'] = sum(1 for p in fpairs if p[2] < p[1] - 0.005)
fields = list(rows[0].keys())
with open(W6 + '/genealogy_metrics.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); [w.writerow(r) for r in rows]
print(len(rows), 'rows;', fields)
