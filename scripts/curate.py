"""Curate Round 4-6 findings into curated.json for build_workbook.py.

Usage: python3 curate.py <scratchpad_dir> <out_curated.json>
Reads raw/{server,imei}_catalog.json, raw/prior_sheets.json and findings/{OWN,A1,A2,B,C,D,V}.json.
All judgements (IDs, roles, confidence) are explicit in this file so they can be reviewed.
"""
import json, sys, re, collections

S, OUT = sys.argv[1], sys.argv[2]
DATE = '2026-10-11'
STREAMS = ['OWN', 'A1', 'A2', 'B', 'C', 'D', 'V']
ROUND = {'OWN': 'R4', 'A1': 'R4', 'A2': 'R4', 'B': 'R5', 'C': 'R5', 'D': 'R5', 'V': 'R6'}
F = {s: json.load(open(f'{S}/findings/{s}.json')) for s in STREAMS}
server = json.load(open(f'{S}/raw/server_catalog.json'))
imei = json.load(open(f'{S}/raw/imei_catalog.json'))
prior = json.load(open(f'{S}/raw/prior_sheets.json'))
SG = {g['num']: g['name'] for g in server['groups']}          # display number -> server group name
IG = {i: g['name'] for i, g in enumerate(imei['groups'])}      # index -> IMEI group name


def words(t, n=25):
    w = str(t).split()
    return ' '.join(w[:n]) + (' …' if len(w) > n else '')


def tool_label(t):
    t = t or ''
    m = {'firecrawl_scrape': 'Firecrawl scrape', 'firecrawl_search': 'Firecrawl search', 'web_search_exa': 'Exa search',
         'web_fetch_exa': 'Exa fetch', 'Parallel_Search__web_search': 'Parallel search', 'Parallel_Search__web_fetch': 'Parallel fetch'}
    for k, v in m.items():
        if k in t:
            return v
    if t.endswith('web_search'):
        return 'Parallel search'
    if t.endswith('web_fetch'):
        return 'Parallel fetch'
    return t


# ------------------------------------------------------------------ evidence register
evidence, tid2ev = [], {}
n = 52
VERIFIED_BY = {'A1-08': 'V-01', 'A2-14': 'V-02', 'C-01': 'V-03', 'A1-21': 'V-03', 'D-05': 'V-04 (reclassified)', 'B-03': 'V-05', 'B-04': 'V-05',
               'D-01': 'V-06', 'B-01': 'V-07 (partly disputed)', 'D-03': 'V-08', 'A1-05': 'V-09', 'C-06': 'V-10', 'C-07': 'V-10'}


def strength(f):
    st, acc, conf = f.get('source_type', ''), f.get('access', ''), f.get('confidence', '')
    if conf == 'DISPUTED':
        return 'Medium (disputed)'
    if 'full' in acc and any(k in st for k in ('Vendor', 'HalabTech', 'Archive')):
        return 'High'
    if 'full' in acc:
        return 'Medium'
    return 'Medium' if conf in ('CONFIRMED', 'STRONG') else 'Low'


for s in STREAMS:
    for f in F[s]['findings']:
        n += 1
        eid = f'EV-{n:03d}'
        tid2ev[f['tid']] = eid
        groups = f.get('halabtech_groups_affected') or []
        evidence.append({
            'EV ID': eid, 'Service': '; '.join(g.replace('\\#', '#') for g in groups[:6]) or '—',
            'Source URL': f['source_url'], 'Type': f.get('source_type', ''), 'Pub. Date': f.get('pub_date', ''),
            'Excerpt (≤20 words)': words(f.get('excerpt', ''), 25), 'Strength': strength(f),
            'S/C': f.get('supports_or_contradicts', ''), 'Record Origin': ROUND[s],
            'Entity': f.get('entity', ''), 'Role Indicated': f.get('role_for_halabtech', ''),
            'Confidence': f.get('confidence', ''), 'Tool': tool_label(f.get('tool', '')), 'Access': f.get('access', ''),
            'Access Date': DATE, 'Finding Ref': f['tid'], 'R6 Verification': VERIFIED_BY.get(f['tid'], ''),
            'Notes': f.get('notes', ''),
        })
for s in STREAMS:
    for i, g in enumerate(F[s]['negative_findings'], 1):
        n += 1
        eid = f'EV-{n:03d}'
        ref = f'{s}-NEG{i:02d}'
        tid2ev[ref] = eid
        evidence.append({
            'EV ID': eid, 'Service': '—', 'Source URL': g.get('url', '') or '—', 'Type': 'Negative check',
            'Pub. Date': '', 'Excerpt (≤20 words)': words(g.get('result', ''), 25), 'Strength': 'Medium',
            'S/C': 'Negative: ' + words(g.get('what_was_checked', ''), 15), 'Record Origin': ROUND[s], 'Entity': g.get('entity', ''),
            'Role Indicated': 'Not listed / not found', 'Confidence': 'CONFIRMED (absence)' if 'ABSENT' in g.get('result', '').upper() or 'not listed' in g.get('result', '').lower() else 'UNKNOWN',
            'Tool': tool_label(g.get('tool', '')), 'Access': 'full page' if g.get('url') else 'n/a', 'Access Date': DATE,
            'Finding Ref': ref, 'R6 Verification': '', 'Notes': '',
        })
NEG = {}  # entity keyword -> EV id for negatives
for e in evidence:
    if e['Type'] == 'Negative check':
        NEG[e['Entity']] = e['EV ID']


def ev(*tids):
    out = []
    for t in tids:
        if t in tid2ev:
            out.append(tid2ev[t])
        elif t.startswith('EV-'):
            out.append(t)
        else:
            for k, v in NEG.items():
                if t.lower() in k.lower():
                    out.append(v)
                    break
    return ', '.join(dict.fromkeys(out))


# ------------------------------------------------------------------ vendors (new)
# (VEN, vendor, website, server group numbers / IMEI names, role wording, refs, scope, sales model, named distributors, confidence)
V = [
    ('VEN-016', 'Hydra Tool (Hydra Dongle team)', 'hydradongle.com', [59, 193, 278], 'Dongle Agent (Syria, Turkey); License Agent (Iraq, Jordan, Sudan, Syria, Turkey)', ['A1-01', 'A1-02'], 'SY, TR, IQ, JO, SD', 'Regional agents + worldwide licence agents', 'GsmServer, Martview, FAST PROVISION (worldwide licence agents)', 'CONFIRMED'),
    ('VEN-017', 'Z3X Team (Samsung Tool Pro / Pandora / Easy-JTAG)', 'z3x-team.com', [168, 241, 271, 274, 310, 311, 101], 'Reseller (Syria, Turkey, Lebanon, Germany)', ['A1-03', 'A1-04'], 'SY, TR, LB, DE', 'Single reseller tier; replacement cards ONLY via GsmServer', 'GsmServer (cards)', 'CONFIRMED'),
    ('VEN-018', 'Infinity-Box team (CM2 / BEST)', 'infinity-box.com', [179, 249, 298], '7. Distributor (World, W. Asia, N. Africa, SY, TR)', ['A1-05', 'V-09'], 'World', 'Numbered distributor list', 'SimSim (#1), GsmEasy (#8), Easy-Unlocker, others', 'CONFIRMED'),
    ('VEN-019', 'DC-Unlocker (incl. HCU / DC-Phoenix)', 'dc-unlocker.com', [243, 317, 318], 'Reseller (credits & dongles) Syria/Turkey – WORLDWIDE', ['A1-06'], 'SY, TR, WW', 'Dealer map', 'GsmServer (HK/UA), SimSim (AE/IN), Martview (CN)', 'CONFIRMED'),
    ('VEN-020', 'SigmaKey team (Sigma / Sigma Plus)', 'sigmakey.com', [72, 252], 'Reseller (Worldwide; Turkey)', ['A1-07', 'A1-08', 'V-01'], 'WW, TR', 'EXCLUSIVE distributor GsmServer; resellers buy credits on gsmserver.com', 'GsmServer (exclusive)', 'CONFIRMED'),
    ('VEN-021', 'Cheetah Tool', 'cheetah-tool.com', [253], 'Reseller (11 countries) – NOT distributor', ['A1-09'], 'EG, IQ, JO, LB, LY, MA, SA, SD, SY, TR, US', 'Distributors + resellers', 'GSMserver, GsmGenesis, ADY, Gsmfastest, Gsm Africa, Unlock UA, 3GSM, Esim unlocker', 'CONFIRMED'),
    ('VEN-022', 'Griffin-Unlocker Pro', 'griffin-unlocker.com', [308], 'Reseller (Turkey/Syria · Worldwide)', ['A1-11'], 'TR, SY, WW', 'Only through authorised agents', '—', 'CONFIRMED'),
    ('VEN-023', 'EME Mobile Tool (EMT)', 'emegsm.com', [255], 'Distributors / Turkey ("Distributor And Reseller")', ['A1-12', 'C-15'], 'WW / TR', 'Distributors + resellers', 'GsmEasy, GSM-Sources, GsmGenesis/MyGSM24', 'CONFIRMED'),
    ('VEN-024', 'XinZhiZao (XZZ)', 'zh.wmdang.com', [304], 'Middle east Statewide Distributor', ['A1-18'], 'Middle East', 'Abroad general agent + state distributors', 'MasterXu Brand (abroad general agent)', 'CONFIRMED'),
    ('VEN-025', 'DZKJ PhoneRepair Tools / Schematics', 'dzkj16888.com', [211], 'Reseller strip (GsmServer, HalabTech, ADYunlocker, IRAQ Server)', ['A1-19'], '—', 'Resellers', 'GsmServer listed alongside', 'CONFIRMED'),
    ('VEN-026', 'MWorker-Tool (Moto-Key)', 'mworker-tool.com', [217], 'Distributor And Reseller', ['A1-20'], 'WW', 'Resellers', '—', 'CONFIRMED'),
    ('VEN-027', 'Borneo Schematics', 'borneoseller.com', [208], 'Seller (Turkey, Sudan, Syria)', ['A1-17'], 'TR, SD, SY', 'Seller directory (ownership unverified)', '—', 'LIKELY'),
    ('VEN-028', 'Furious Gold (FuriousTeam)', 'furiousgold.com', [248, 279], 'NOT LISTED', ['A1-13'], '—', 'Buy only from official distributors (also direct web shop)', 'GSM Server, GsmEasy, GsmFastest, ADYunlocker, HACK3R2K, Click-Unlocker, acellsorios', 'CONFIRMED (absence)'),
    ('VEN-029', 'Ultimate Multi Tool (UMT) / NCK', 'umt-pro.com', [244, 104, 314, 52], 'NOT LISTED', ['A1-14'], '—', 'Worldwide distributors', 'Fast Unlocking, GsmServer, GsmEasy, Martview, GSM Sources, SharkGSM, SimSim', 'CONFIRMED (absence)'),
    ('VEN-030', 'Avengers Box', 'avengersbox.com', [313], 'NOT LISTED', ['A1-15'], '—', 'Distributors', 'Fast Unlocking, GsmServer, GSM-Sources, GsmEasy, GsmSalman, Smart Unlock Mobile, Gsm Africa', 'CONFIRMED (absence)'),
    ('VEN-031', 'UFI Box', 'ufi-box.com', [219], 'NOT LISTED', ['A1-16'], '—', 'Worldwide distributor + resellers', 'Martview (worldwide distributor)', 'CONFIRMED (absence)'),
    ('VEN-032', 'HW-Key Tool', 'hwkey.com', [169], 'Distributor (listed first)', ['A2-01', 'D-13'], 'WW', 'Resellers', '—', 'CONFIRMED'),
    ('VEN-033', 'DeviceSavior Tool', 'devicesavior.com', [56], 'World Wide Distributor/Reseller (listed first)', ['A2-02'], 'WW', '—', '—', 'CONFIRMED'),
    ('VEN-034', 'SK Unlocker', 's-k-unlocer.com', [50], 'Reseller network – HalabTech Syria (listed first)', ['A2-03'], 'SY', '—', '—', 'CONFIRMED'),
    ('VEN-035', 'OumseGsm Tool Pro', 'oumsegsm.com', [27], 'Distributor (1 of 2, with GsmGenesis)', ['A2-04'], 'WW', '2 distributors + 37 resellers', 'GsmGenesis', 'CONFIRMED'),
    ('VEN-036', 'TSM Tool / TSM Tool Pro', 'tsm-tool.com', [112], 'Official Distributor (Syria/Middle East/Algeria/Morocco/WW)', ['A2-05', 'D-09'], 'SY, ME, DZ, MA, WW', 'Distributors', '—', 'CONFIRMED'),
    ('VEN-037', 'Phoenix Service Tool', 'phoenixservicetool.com', [97], 'Official Reseller (1 of 2, listed first)', ['A2-06'], 'WW', '2 resellers', '—', 'CONFIRMED'),
    ('VEN-038', 'Global Unlocker Pro', 'global-unlocker-pro.com', [218, 259], 'Reseller', ['A2-07'], 'WW', 'Only through authorised agents', 'Global Store, ADY Unlocker, Hali Unlock, GsmServer, Fast Provision', 'CONFIRMED'),
    ('VEN-039', 'TR Tools Pro', 'trtools.pro', [301], 'Listed (tab Reseller/Distributor unclear)', ['A2-08'], 'ALL', '—', '—', 'CONFIRMED'),
    ('VEN-040', 'Pragmafix Schematics', 'pragmafix.net', [222], 'DISTRIBUTOR (after GsmEasy)', ['A2-09'], 'WW', 'Distributors', 'GsmEasy', 'CONFIRMED'),
    ('VEN-041', 'KEY-Tool', 'key-tool.com', [272], 'Our Resellers', ['A2-10'], 'WW', 'Resellers (HalabTech sells KEY-Tool distributor packs)', 'Hali-Unlock (Yemen family)', 'CONFIRMED'),
    ('VEN-042', 'MobileSea Service Tool (MST)', 'mobileseaservice.net', [223], 'Distributor (Turkey · Syria · Arabic Countries / WW)', ['A2-11'], 'TR, SY, Arab', '—', '—', 'CONFIRMED'),
    ('VEN-043', 'UNI-Android Tool (UAT PRO)', 'uni-android.com', [212], 'Distributor (listed first)', ['A2-12'], 'WW', 'Buy only from official distributors/resellers', '—', 'CONFIRMED'),
    ('VEN-044', 'T-Tool Pro', 't-tool-pro.net', [224], '#2 Worldwide Reseller', ['A2-13'], 'WW', 'One official worldwide distributor', 'GSM T-Tool (Iraq) – sole', 'CONFIRMED'),
    ('VEN-045', 'Hunter Unlocker Pro', 'hunter-unlocker.com', [264], 'WorldWide Distributor (1 of 3)', ['A2-14', 'V-02'], 'WW', 'NO direct sales to agents – distributors only', 'HalabTech + 2 others (incl. Hali-Unlock)', 'CONFIRMED'),
    ('VEN-046', 'Q-Unlocker Pro', 'q-unlocker.com', [182], 'WorldWide Distributor (1 of 3)', ['A2-15'], 'WW', 'NO direct sales to agents – distributors only', 'HalabTech + 2 others', 'CONFIRMED'),
    ('VEN-047', 'Scorpion Tool Pro', 'scptool.com', [99], 'Official Reseller ("Distributor/Reseller")', ['A2-16'], 'WW / ME / Africa', '—', '—', 'CONFIRMED'),
    ('VEN-048', 'RTC Tool', 'rtc-tool.com', [285], 'Distributor WorldWide', ['A2-17'], 'WW', '—', '—', 'CONFIRMED'),
    ('VEN-049', 'KG Killer Tool', 'kgkiller.com', [51], 'Distributor/Reseller Worldwide', ['A2-18'], 'WW', '—', 'FRP King Server (BIG distributor)', 'CONFIRMED'),
    ('VEN-050', 'Galaxy Multi Tool', 'galaxymultitool.com', [4], 'WorldWide – Distributor', ['A2-19'], 'WW', '—', '—', 'CONFIRMED'),
    ('VEN-051', 'Hello AIO Tool', 'helloaiotool.com', [176], 'Authorized Distributor', ['A2-20'], 'WW', '—', '—', 'CONFIRMED'),
    ('VEN-052', 'AndroidWinTool (AWT)', 'androidwintool.com', [88], 'Reseller', ['A2-21'], 'WW', 'Main resellers', 'Hiunlock, adyunlocker', 'CONFIRMED'),
    ('VEN-053', 'CellTool (SamsungTool.us)', 'samsungtool.us', [165], 'Authorized reseller', ['A2-22'], 'WW', 'One official distributor', 'Smart Tool Worldwide – sole', 'CONFIRMED'),
    ('VEN-054', 'Xiaomi Pro Tool (GautamGreat)', 'xiaomiprotool.com', [155], 'Distributor (name match to "Mi Pro Tool" group)', ['A2-23'], 'WW', '—', '—', 'CONFIRMED'),
    ('VEN-055', 'Global Auth Tool', 'globalauthtool.com', [75], 'DISTRIBUTOR (Worldwide)', ['A2-24'], 'WW', '—', '—', 'STRONG'),
    ('VEN-056', 'Piranha Tool', 'piranhatool.com', [128], 'Official Distributor (listed before GsmServer)', ['A2-25'], 'WW', 'Distributors', 'GsmServer', 'CONFIRMED'),
    ('VEN-057', 'MG Unlocker Pro', 'mgunlocker.com', [45], 'Official Distributor', ['A2-26'], 'WW', '—', '—', 'CONFIRMED'),
    ('VEN-058', 'FlexUnlock Tool', 'flexunlock.com', [167], 'BIG Distributor', ['A2-27'], 'WW', '—', '—', 'CONFIRMED'),
    ('VEN-059', 'M-PRO Tool', 'm-protool.net', [187], 'Reseller', ['A2-28'], 'WW', '—', '—', 'CONFIRMED'),
    ('VEN-060', 'Flame Auth Tool', 'flameauthtool.cloud', [117], 'Distributor/Reseller WorldWide (reseller list)', ['A2-29'], 'WW', '—', '—', 'CONFIRMED'),
    ('VEN-061', 'KGFRP Tool', 'kgfrptool.com', [145], '[Distributor]', ['A2-30'], 'WW', '—', '—', 'CONFIRMED'),
    ('VEN-062', 'GPT-PRO Tool', 'gpt-tool.com', [127], 'Reseller WorldWide', ['A2-31'], 'WW', '—', '—', 'CONFIRMED'),
    ('VEN-063', 'S-Finder app', 'sfinder.app', [129], 'Distributor (Sudan number)', ['A2-32'], 'WW', '—', '—', 'STRONG'),
    ('VEN-064', 'Ghost Auth Tool', 'ghostauthtool.com', [82], 'Distributor WorldWide', ['A2-33'], 'WW', '—', '—', 'CONFIRMED'),
    ('VEN-065', 'WorldWideAuth (Xiaomi)', 'worldwideauth.com', [281], 'Distributor for All Country (Worldwide)', ['A2-34'], 'WW', '—', '—', 'CONFIRMED'),
    ('VEN-066', 'Xiaomi BD Auth Tool', 'xiaomibdteam.net', [108], 'Distributors & Resellers list', ['A2-35'], 'WW', '—', '—', 'STRONG'),
    ('VEN-067', 'Panda Tools', 'panda-tools.net', [306], 'Reseller', ['A2-36'], 'WW', 'One distributor', 'ADY Unlocker – sole', 'CONFIRMED'),
    ('VEN-068', 'Ameer Tool (GSMUNBRICK, Syria)', 'gsmunbrick.com', [67], 'Distributor/Reseller WorldWide', ['A2-37', 'C-12'], 'WW', '—', '—', 'CONFIRMED'),
    ('VEN-069', 'SamKey', 'samkey.org', [235], 'NOT LISTED', ['A2-NEG01'], '—', 'Worldwide distributors', 'GsmEasy, SiRoYa (Dubai)', 'CONFIRMED (absence)'),
    ('VEN-070', 'Android Multi Tool (AMT)', 'androidmultitool.com', [284], 'NOT LISTED', ['A2-NEG02'], '—', '3 distributors', 'GSM Credit, GsmGenesis, Ady Unlocker', 'CONFIRMED (absence)'),
    ('VEN-071', 'MH Unlocker Pro', 'mhunlocker.com', [286], 'NOT LISTED', ['A2-NEG03'], '—', 'Super distributor + distributors', 'iUnlocking Store (super), GsmFastest, Gsm Africa, Leope-Gsm, Infinity-Box', 'CONFIRMED (absence)'),
    ('VEN-072', 'XTP – Xiaomi Tool Pro', 'xiaomitoolpro.com', [189], '"Official Main Seller" + worldwide distributor (listed first)', ['D-07'], 'WW', 'Main seller', 'HalabTech (main seller)', 'CONFIRMED'),
    ('VEN-073', 'AnonySHU Tool', 'anonyshu.com', [79], 'Distributor (worldwide)', ['D-11'], 'WW', '—', '—', 'STRONG'),
    ('VEN-074', 'FRP Service Tool', 'frpservice.com', [], 'Distributor/Reseller WorldWide', ['D-12'], 'WW', '—', '—', 'STRONG'),
    ('VEN-075', 'OnlineFRPTool (OFT)', '—', [20], 'Self-claim "Official Distributor" (HalabTech Telegram)', ['D-08'], '—', '—', '—', 'LIKELY'),
    ('VEN-076', 'iRemoval PRO', 'iremovalpro.com', [], 'Self-claim "Official Distributor" (~2025); 2023 exclusive partner @iBoCloud', ['D-06'], '—', 'Exclusive partner model (2023)', 'iBoCloud (2023)', 'LIKELY'),
    ('VEN-077', 'Sultankoo Store (iOS plus-apps, Qatar)', 'sultankoo.net', [315], 'Product sold by HalabTech; vendor has distributor panel', ['D-14'], '—', 'Distributor panel', '—', 'LIKELY'),
    ('VEN-078', 'Zeus / Hermes / Scylla / Kratos (iOS tools)', 'scyllatool.com', [], 'Resold on HalabTech server in 2023 (historical)', ['V-04', 'D-05'], '—', '—', '—', 'CONFIRMED (historical)'),
    ('VEN-079', 'iRemove Software (iRemove.Tools)', 'iremove.tools', ['iPads WIFI Only (iCloud Remove)', 'iWatch WIFI Only (iCloud Remove)'], 'No public reseller list; partner programme over DHRU API', ['B-13'], '—', 'Partner programme (login-only)', '—', 'UNKNOWN'),
    ('VEN-080', 'Signal Labs Technology (vendor unidentified)', '—', ['Signal Labs Technology Service'], 'Not identified', ['B-15'], '—', '—', '—', 'UNKNOWN'),
]

vend_hdr = ['Vendor ID', 'Vendor', 'Website', 'Products', 'Relationship with HalabTech', 'Evidence', 'Record Origin', 'Countries / Scope',
            'Vendor Sales Model', 'Named Distributors', 'Confidence (R6)', 'R6 Update', 'Last Verified']
vend_rows = []
vendor_by_group = {}
group_ev = collections.defaultdict(list)
for vid, name, site, groups, role, refs, scope, model, dists, conf in V:
    gnames = [SG[g] if isinstance(g, int) else g for g in groups]
    vend_rows.append({'Vendor ID': vid, 'Vendor': name, 'Website': site, 'Products': '; '.join(gnames) or '(no current SKU)',
                      'Relationship with HalabTech': role, 'Evidence': ev(*refs), 'Record Origin': 'R4-6 (new)', 'Countries / Scope': scope,
                      'Vendor Sales Model': model, 'Named Distributors': dists, 'Confidence (R6)': conf, 'R6 Update': '', 'Last Verified': DATE})
    for g in gnames:
        vendor_by_group[g] = [name, vid]
        group_ev[g].append(ev(*refs))

prior_vendor_updates = {
    'VEN-000': {'Confidence (R6)': 'CONFIRMED', 'R6 Update': 'Own products: memberships, credits, Sharing Box (in-house hardware), file requests; Telegram claims "direct source" for Premium Tecno/iTel/Infinix MDM', 'Evidence': 'EV-020, EV-027–031, EV-046; ' + ev('OWN-02', 'OWN-05', 'V-08')},
    'VEN-001': {'Confidence (R6)': 'CONFIRMED', 'R6 Update': 'Re-confirmed via Wayback 2022-05-11 & 2024-01-19 and Telegram 2026-10-01; HalabTech sold "DFT Agent Panel (2000 credits)" in 2022-24', 'Vendor Sales Model': 'Distributors + resellers'},
    'VEN-002': {'Confidence (R6)': 'CONFIRMED (Reseller only)', 'R6 Update': 'CORRECTION: HalabTech card has no Distributor label (2023 capture: "HALABTECH (reseller)"). Vendor rule: resellers can ONLY buy credits from GsmEasy or GsmServer', 'Vendor Sales Model': 'Distributor-only (GsmEasy, GsmServer; 3rd card Unlock.eu)', 'Named Distributors': 'GsmEasy, GsmServer, Unlock.eu'},
    'VEN-003': {'Confidence (R6)': 'CONFIRMED', 'R6 Update': 'Re-confirmed (octoplusbox.com/en/buynow); no distributor tier named'},
    'VEN-007': {'Confidence (R6)': 'STRONG', 'R6 Update': 'Third-party mirror downloadunlocktool.com repeats "HALABTECH RESELLER PAKISTAN – WORLDWIDE"; vendor page still bot-blocked'},
    'VEN-011': {'Confidence (R6)': 'CONFIRMED (listing) / no SKU', 'R6 Update': 'No AuthFlash group or SKU in the 2026-10-11 catalog'},
    'VEN-012': {'Confidence (R6)': 'CONFIRMED', 'R6 Update': 'Footer "Powered by Dhru Fusion" (fromaid=server.halabtech.com) captured with Firecrawl - LIKELY → CONFIRMED'},
    'VEN-013': {'Confidence (R6)': 'CONFIRMED (absence)', 'R6 Update': 'Full EFT list (modified 2022-12-16) read: HalabTech NOT listed; 9 worldwide distributors', 'Named Distributors': 'Easy-Firmware/Easy-Unlocker, SimSim, GsmServer, GSM-Sources, SharkGSM, GsmEasy, GsmFastest, KhaledGsm, Yemen contact'},
    'VEN-014': {'Confidence (R6)': 'CONFIRMED', 'R6 Update': 'rapidflashtool.com/reseller.php lists "HalabTech – Distributor (Worldwide)" first; developer name not on page ("Baba Tools" unconfirmed)'},
}
prior_vendor_updates['VEN-001']['Evidence'] = 'EV-009, EV-010, ' + ev('C-16', 'D-10')
prior_vendor_updates['VEN-002']['Evidence'] = 'EV-011…015, ' + ev('C-01', 'C-03', 'C-04', 'C-05', 'A1-21', 'V-03')
prior_vendor_updates['VEN-003']['Evidence'] = 'EV-016, ' + ev('A1-10')
prior_vendor_updates['VEN-011']['Evidence'] = 'EV-026, ' + ev('OWN-07')
prior_vendor_updates['VEN-012']['Evidence'] = 'EV-006, EV-034…036, ' + ev('OWN-01', 'D-29')
prior_vendor_updates['VEN-013']['Evidence'] = 'EV-037, ' + ev('C-10', 'C-19')
prior_vendor_updates['VEN-014']['Evidence'] = 'EV-041, EV-042, ' + ev('C-11')
# prior vendors -> groups
for g, vid in ((213, 'VEN-001'), (242, 'VEN-002'), (170, 'VEN-003'), (206, 'VEN-003'), (215, 'VEN-003'), (251, 'VEN-003'), (288, 'VEN-003'),
               (289, 'VEN-003'), (290, 'VEN-003'), (291, 'VEN-003'), (295, 'VEN-004'), (228, 'VEN-005'), (132, 'VEN-006'), (258, 'VEN-007'),
               (105, 'VEN-008'), (231, 'VEN-009'), (207, 'VEN-010'), (214, 'VEN-012'), (240, 'VEN-013'), (151, 'VEN-014'),
               (247, 'VEN-000'), (93, 'VEN-000'), (92, 'VEN-000'), (236, 'VEN-000')):
    pv = {r['Vendor ID']: r['Vendor'] for r in prior['Original Vendors']['rows']}
    vendor_by_group[SG[g]] = [pv[vid], vid]

# ------------------------------------------------------------------ group-level supply mapping
GM = {}


def gm(key, status, cand, conf, refs=(), prio='', notes='', model=None, api='None identified'):
    name = SG[key] if isinstance(key, int) else key
    d = {'status_at_vendor': status, 'candidate_upstream': cand, 'upstream_confidence': conf, 'evidence': ev(*refs), 'priority': prio, 'notes': notes, 'confirmed_api_supplier': api}
    if model:
        d['fulfilment_model'] = model
    GM[name] = d


DIRECT_LIKELY = 'Direct from vendor (vendor lists HalabTech; no API evidence)'
for vid, name, site, groups, role, refs, scope, model, dists, conf in V:
    for g in groups:
        if role.startswith('NOT LISTED'):
            gm(g, 'Not listed (full list checked)', f'Via a named distributor: {dists}', 'LIKELY', refs, 'High', 'Vendor list omits HalabTech; at least one intermediary likely')
        elif conf in ('UNKNOWN',):
            gm(g, role, '—', 'UNKNOWN', refs, 'High')
        else:
            gm(g, role, DIRECT_LIKELY if not dists or dists == '—' else f'{DIRECT_LIKELY}; alternative: {dists}', 'LIKELY', refs)
# overrides with stronger / specific evidence
gm(72, 'Reseller (Worldwide; Turkey)', 'GsmServer – Sigma\'s EXCLUSIVE distributor; resellers buy Sigma Plus credits on gsmserver.com', 'STRONG', ['A1-07', 'A1-08', 'V-01'], 'High', 'Vendor rule, not an observed order/API')
gm(252, 'Reseller (Worldwide; Turkey)', 'GsmServer – Sigma\'s EXCLUSIVE distributor', 'STRONG', ['A1-07', 'A1-08', 'V-01'], 'High', 'Vendor rule, not an observed order/API')
gm(242, 'Reseller (no distributor label; 2023 "(reseller)")', 'GsmEasy OR GsmServer – Chimera: "resellers can only buy credits from them"', 'STRONG', ['C-01', 'C-03', 'C-04', 'C-06', 'A1-21', 'V-03', 'V-10'], 'High', 'Which of the two is unknown; Unlock.eu card is a 3rd possibility; HalabTech sold 20,000-credit packs in 2022')
gm(264, 'WorldWide Distributor (1 of 3)', 'Direct from Hunter Unlocker (vendor: no direct sales to agents; distributors only)', 'STRONG', ['A2-14', 'V-02'], '', 'Strongest public indication of a direct vendor→HalabTech supply line')
gm(182, 'WorldWide Distributor (1 of 3)', 'Direct from Q-Unlocker (vendor: distributors only)', 'STRONG', ['A2-15'], '')
gm(189, '"Official Main Seller" + distributor', 'Direct from XTP vendor (HalabTech is its main seller)', 'STRONG', ['D-07'], '')
gm(224, '#2 Worldwide Reseller', 'GSM T-Tool (Iraq) – sole official worldwide distributor; or direct', 'LIKELY', ['A2-13'], 'Medium')
gm(165, 'Authorized reseller', 'Smart Tool Worldwide – sole official distributor; or direct', 'LIKELY', ['A2-22'], 'Medium')
gm(306, 'Reseller', 'ADY Unlocker – sole distributor; or direct', 'LIKELY', ['A2-36'], 'Medium')
gm(218, 'Reseller', 'One of: Global Store, ADY Unlocker, Hali Unlock, GsmServer, Fast Provision (only via authorised agents)', 'LIKELY', ['A2-07'], 'Medium')
gm(259, 'Reseller', 'One of: Global Store, ADY Unlocker, Hali Unlock, GsmServer, Fast Provision', 'LIKELY', ['A2-07'], 'Medium')
gm(253, 'Reseller (not distributor)', 'Direct, or a Cheetah distributor (GSMserver, GsmGenesis, ADY, Gsmfastest, Gsm Africa, Unlock UA, 3GSM, Esim unlocker)', 'UNKNOWN', ['A1-09'], 'Medium')
gm(240, 'Not listed (full EFT list, 2022-12-16)', 'Easy-Firmware/Easy-Unlocker sales arm or one of 9 WW distributors (SimSim, GsmServer, GSM-Sources, SharkGSM, GsmEasy, GsmFastest, KhaledGsm…)', 'LIKELY', ['C-10', 'C-19'], 'High', 'Intermediary likely; identity unknown')
gm(151, 'Distributor (Worldwide) – listed first', DIRECT_LIKELY, 'LIKELY', ['C-11'], '')
gm(67, 'Distributor/Reseller WorldWide', DIRECT_LIKELY + ' (GSMUNBRICK, Syria)', 'LIKELY', ['A2-37', 'C-12'], '')
gm(213, 'Distributor And Reseller', DIRECT_LIKELY + '; HalabTech sold DFT Agent Panels 2022-24', 'LIKELY', ['C-16', 'D-10'], '')
gm(258, 'Reseller (PAKISTAN – WORLDWIDE)', 'Direct (reseller) or via UnlockTool distributors (e.g. GsmGenesis/MyGSM24)', 'LIKELY', [], 'Medium')
gm(304, 'Middle east Statewide Distributor', 'Direct from XZZ, or via MasterXu Brand (abroad general agent)', 'LIKELY', ['A1-18'], 'Low')
gm(214, 'Platform customer (Dhru footer)', 'Dhru (licence resale self-claimed)', 'LIKELY', ['OWN-01', 'D-29'], 'Low')
for g in (247, 93, 92, 236):
    gm(g, 'Own product', 'In-house (HalabTech)', 'CONFIRMED', ['OWN-05'], '', model='In-house', api='HalabTech (self)')
gm(303, 'n/a', 'In-house – remote sharing of boxes HalabTech owns', 'LIKELY', ['OWN-05'], 'Low', model='In-house (likely)')
gm(254, 'n/a', 'Physical stock; hardware distributors (e.g. Martview for UFI, GsmServer for Z3X cards) – not evidenced', 'UNKNOWN', ['OWN-05', 'A1-04', 'A1-16'], 'Low', model='Physical hardware (stock source unknown)')
gm(315, 'Product of sultankoo.net', 'Direct from Sultankoo (distributor panel) – not evidenced', 'LIKELY', ['D-14'], 'Low')
for g in (80, 81, 85, 86, 87):
    gm(g, 'n/a', 'Unidentified telecom top-up provider (Syria/Turkey)', 'UNKNOWN', ['D-30'], 'Medium')
for g in (204, 220, 221, 237, 238, 230, 256, 257):
    gm(g, 'n/a', 'Unidentified gift-card / game top-up wholesaler ("AUTO API" on PUBG)', 'UNKNOWN', [], 'Medium')
for g in (172, 9, 186):
    gm(g, 'n/a', 'Unidentified digital-subscription reseller', 'UNKNOWN', [], 'Medium')
gm(309, 'n/a', 'EC Store (iOS signing) – operator unidentified', 'UNKNOWN', ['D-15'], 'Low')
for g in (102, 297):
    gm(g, 'n/a', 'Yemeni tool vendor – unidentified', 'UNKNOWN', ['D-16'], 'Low')
# IMEI groups
gm(IG[18], 'n/a (IMEI)', 'Code-GSM (code-gsm.com, self-styled "Wholesale Supplier") – identical names; detail-page prices $1-3 below HalabTech for Till 15/16/17', 'LIKELY', ['B-01', 'B-02', 'V-07'], 'High', 'DISPUTED for lower tiers: Code-GSM listing shows Till 11/12 $45, 13/14 $60 vs HalabTech Till 12/14 $38.99')
gm(IG[8], 'n/a (IMEI)', 'Unnamed premium source', 'UNKNOWN', [], 'High')
gm(IG[12], 'n/a (IMEI)', 'HalabTech self-claims "direct source" (Premium Source #1); UnlocksPro carries the identical group name', 'LIKELY', ['D-03', 'V-08', 'B-03', 'OWN-03'], 'High', 'Direction between HalabTech and UnlocksPro unproven')
gm(IG[23], 'n/a (IMEI)', 'Unnamed "Source #2" and "Source #3"', 'UNKNOWN', ['OWN-03', 'V-08', 'D-04'], 'High', 'Existence of multiple sources CONFIRMED; identities unknown')
gm(IG[17], 'n/a (IMEI)', 'Unnamed "Source 3"', 'UNKNOWN', ['OWN-03', 'D-04'], 'High')
gm(IG[21], 'n/a (IMEI)', 'Unnamed "Source 2#"; resold downstream with HalabTech\'s Arabic wording', 'UNKNOWN', ['OWN-03', 'B-12'], 'High')
gm(IG[0], 'n/a (IMEI)', 'UnlocksPro (identical items #26234/#26235/#26267/#26268); vendor "Signal Labs" unidentified', 'LIKELY', ['B-03', 'B-15', 'V-05'], 'Medium')
gm(IG[48], 'n/a (IMEI)', 'UnlocksPro (identical JDM V4/V5 #22343-22349 incl. "Patch 1.7.2023")', 'LIKELY', ['B-05', 'V-05'], 'High')
gm(IG[54], 'n/a (IMEI)', 'UnlocksPro "US Reseller Flex Policy [DIRECT SOURCE]"', 'LIKELY', ['B-06'], 'High', 'Code-GSM Reseller Flex names differ')
gm(IG[36], 'n/a (IMEI)', 'Multiple unnamed sources ("Server Direct", "Direct Source", "Source2 #Cheaper"); UnlocksPro has the "Rocket Super Fast" pair', 'UNKNOWN', ['OWN-03', 'B-03'], 'High', '62 SKUs across ~20 countries')
gm(IG[13], 'n/a (IMEI)', 'UnlocksPro lists the Keylock checker ("Keylock" = lock-code field, not a vendor)', 'LIKELY', ['B-03'], 'Low')
gm(IG[40], 'n/a (IMEI)', 'Unnamed source whose catalogue numbers (#225, #33225) survive in names', 'UNKNOWN', ['OWN-04', 'B-10', 'B-11'], 'Medium', 'sickw.com ruled out')
gm(IG[9], 'n/a (IMEI)', 'Unknown; Best4unlock carries ~33 identical names (sibling, not shown to be supplier)', 'UNKNOWN', ['B-07', 'B-09'], 'Medium')
gm(IG[20], 'n/a (IMEI)', 'iRemove (original vendor; partner programme over DHRU API) directly or via a partner; HalabTech prices $25-70 above iRemove public prices', 'UNKNOWN', ['B-13', 'B-14'], 'High')
gm(IG[19], 'n/a (IMEI)', 'iRemove (original vendor) directly or via a partner', 'UNKNOWN', ['B-13'], 'High')
gm(IG[47], 'n/a (IMEI)', 'Unknown; Best4unlock advertised the same EDL services on GSM-Forum 2023-25', 'UNKNOWN', ['B-08', 'B-16', 'B-17'], 'High')
for i in (50, 51, 56):
    gm(IG[i], 'n/a (IMEI)', 'Unknown CPID operator (IN-GSM / cpidserver.com run own CPID servers; names differ)', 'UNKNOWN', ['B-16', 'B-17'], 'Medium')
gm(IG[31], 'n/a', 'Internal test service', 'CONFIRMED', [], '', model='In-house', api='HalabTech (self)')
gm(SG[234], 'n/a', 'Internal test service', 'CONFIRMED', [], '', model='In-house', api='HalabTech (self)')

# ------------------------------------------------------------------ suppliers / distributors
sup_hdr = ['Supplier ID', 'Company', 'Role', 'Distribution Status', 'Relationship with HalabTech', 'Evidence', 'Confidence', 'Record Origin',
           'Candidate For (HalabTech groups)', 'Basis', 'Confidence (R6)', 'R6 Update', 'Last Verified']
SUP = [
    ('SUP-012', 'GsmEasy (imei.us / gsmeasyshop.com, Guangzhou)', 'Global distributor', 'Chimera (1 of 2 contracted distributors), UMT, Infinity (#8), Furious Gold, Avengers, SamKey, EME, Pragmafix', 'Candidate intermediate supplier', ['A1-21', 'C-01', 'C-18', 'A1-13', 'A1-14', 'A1-15', 'V-03'], 'Chimera Activation; SamKey Services; UMT/NCK; Furious Gold; Avengers Box', 'Vendor distributor-only rules', 'STRONG (Chimera, shared with GsmServer); LIKELY-shared (others)'),
    ('SUP-013', 'Unlock.eu', 'Chimera "Distributor" card (API Upgrade and Extend)', 'Chimera (card contradicts "two distributors" text)', 'Possible Chimera credit source', ['A1-21', 'C-03'], 'Chimera Activation', 'Vendor reseller page', 'UNKNOWN'),
    ('SUP-014', 'Code-GSM (code-gsm.com; Wajih Boukadida, Canada/Tunisia)', 'IMEI wholesale supplier (self-styled)', '—', 'Candidate direct API supplier for T-Mobile "Clean & Paid Off"', ['B-01', 'B-02', 'V-07'], 'T-MOBILE | SPRINT | METROPCS POLICY USA (Clean & Paid Off Only)', 'Identical names + $1-3 markup on Till 15/16/17 detail prices', 'LIKELY (price evidence partly DISPUTED)'),
    ('SUP-015', 'UNLOCKSPRO Premium Server (unlockspro.com)', 'IMEI/server "Main/Direct Source" (Dhru tiers DISTRIBUTORS/WEB OWNER/RESELLER)', '—', 'Candidate upstream or sibling for several IMEI groups', ['B-03', 'B-04', 'B-05', 'B-06', 'V-05'], 'Infinix Tecno Itel MDM Source 1#; Signal Labs; NEW JDM V4 V5; USA Reseller Flex; Xiaomi Mi Account (Rocket pair); Xiaomi Checker', '36 exact name matches incl. internal numbers', 'LIKELY (direction unproven)'),
    ('SUP-016', 'Best4unlock (best4unlock.us)', 'IMEI server ("Source Since 2013")', '—', 'Sibling: ~33 identical Apple-check names', ['B-07', 'B-08'], 'Apple Check Service; [BY EDL Binary] SAMSUNG', 'Name overlap only; mixed prices', 'UNKNOWN'),
    ('SUP-017', 'Fast Unlocking (fastunlocking.com, Jordan)', 'UMT worldwide distributor (listed first); Avengers distributor', 'UMT/NCK, Avengers', 'Candidate intermediary', ['A1-14', 'A1-15'], 'UMT Products; UMT ACTIVATION FOR NCK USERS; NCK Products; NCK Online Digital; Avengers Box', '1 of 7 listed distributors', 'UNKNOWN'),
    ('SUP-018', 'ADY Unlocker (adyunlocker, Jordan)', 'Distributor (FG Jordan, Cheetah, Panda sole, AMT, Global Unlocker); HalabTech World Agent', 'Multiple', 'Peer + candidate intermediary', ['A1-13', 'A2-36', 'D-17'], 'Panda Tools (LIKELY); Furious Gold; AMT; Global Unlocker; Cheetah', 'Sole Panda distributor; HalabTech lists ADY as its agent (two-way)', 'LIKELY (Panda); UNKNOWN (others)'),
    ('SUP-019', 'GSM T-Tool (Iraq)', 'Sole official worldwide distributor of T-Tool Pro', 'T-Tool Pro', 'Candidate intermediary', ['A2-13'], 'T-TOOL PRO', 'Vendor page', 'LIKELY'),
    ('SUP-020', 'Smart Tool Worldwide', 'Sole official distributor of CellTool (samsungtool.us)', 'CellTool', 'Candidate intermediary', ['A2-22'], 'SamsungTool.us CellTool', 'Vendor page', 'LIKELY'),
    ('SUP-021', 'iUnlocking Store', 'MH Unlocker Pro super distributor', 'MH Unlocker', 'Candidate intermediary', ['A2-NEG03'], 'MH Unlocker Pro', '1 of 5 distributors', 'UNKNOWN'),
    ('SUP-022', 'SiRoYa (Dubai)', 'SamKey worldwide distributor', 'SamKey', 'Candidate intermediary', ['A2-NEG01'], 'SamKey Services', '1 of 2 distributors (with GsmEasy)', 'UNKNOWN'),
    ('SUP-023', 'Hali-Unlock (Yemen)', 'Distributor across Yemen tool family (Hunter, Q-Unlocker, Global Unlocker, KEY-Tool, Tira)', 'Yemen tools', 'Co-distributor / peer', ['A2-07'], 'Global Unlocker; KEY-Tool; Tira unlocker', 'Shared distributor lists', 'UNKNOWN'),
    ('SUP-024', 'FAST PROVISION (fastprovision.com)', 'Hydra worldwide licence agent; Global Unlocker distributor; EFT "[Official Distributor]" store', 'Hydra, Global Unlocker, EFT', 'Candidate intermediary', ['A1-01'], 'Hydra; Global Unlocker; EFT', 'Vendor pages', 'UNKNOWN'),
    ('SUP-025', 'Easy-Firmware / Easy-Unlocker (Iraq, +9647511889867)', 'EFT "official distributor in the world" (vendor sales arm); Infinity distributor', 'EFT, Infinity', 'Candidate EFT source', ['C-10', 'V-09'], 'EFT', 'HalabTech absent from EFT list', 'LIKELY (one of EFT channels)'),
    ('SUP-026', 'MasterXu Brand', 'XZZ "ABROAD GENERAL AGENT"', 'XinZhiZao', 'Possible layer between XZZ and HalabTech', ['A1-18'], 'XinZhiZao - XZZ', 'Vendor page', 'UNKNOWN'),
    ('SUP-027', 'iBoCloud (@iBoCloud)', 'iRemoval PRO exclusive partner (2023)', 'iRemoval PRO', 'Possible historical source', ['D-06'], '(historical iRemoval PRO services)', 'Relayed Telegram post', 'UNKNOWN'),
    ('SUP-028', 'Downstream stores added R4-6 (WARD Server, IDUnlocker, MR Unlockers, GSMUnlockInfo, GsmUnlockingStore, GSM Manager, SuperUnlockMx, gsmexpertzone, sourceforunlock, fix4gsm, axiomunlocker, mwunlocker, gsmtiger, univgsm, reunlocker, eagleunlocker, khulnaunlock, ssteamunlocker, akgsmsolutions…)', 'Downstream resellers', '—', 'Buy from HalabTech (several carry HalabTech text verbatim; HalabTech advertises "Connect API NOW")', ['C-14', 'OWN-08', 'OWN-09', 'D-19', 'D-20', 'D-21', 'D-22', 'D-23', 'D-24', 'B-11', 'B-12', 'B-19', 'C-13'], 'HALABTECH, IMEI groups', 'Store pages', 'CONFIRMED (sell); LIKELY (API clients)'),
    ('SUP-029', 'HalabTech World Agents (29 entries)', 'Downstream agents', '—', 'Listed by HalabTech as its agents', ['D-17', 'D-18'], 'All', 'support.halabtech.com world-agents', 'CONFIRMED'),
    ('SUP-030', 'LexusyPay (lexusypay.com)', 'Payment platform', '—', 'Auto top-up of server balance', ['D-27'], '—', 'Telegram', 'CONFIRMED (platform, not supplier)'),
]
sup_rows = []
for sid, comp, role, dist, rel, refs, cand, basis, conf in SUP:
    sup_rows.append({'Supplier ID': sid, 'Company': comp, 'Role': role, 'Distribution Status': dist, 'Relationship with HalabTech': rel,
                     'Evidence': ev(*refs), 'Confidence': conf.split(' ')[0], 'Record Origin': 'R4-6 (new)', 'Candidate For (HalabTech groups)': cand,
                     'Basis': basis, 'Confidence (R6)': conf, 'R6 Update': '', 'Last Verified': DATE})
prior_sup_updates = {
    'SUP-001': {'Confidence (R6)': 'STRONG (Sigma); STRONG-shared (Chimera); LIKELY ("GsmServer Products" 2022-24); no API evidence', 'R6 Update': 'Sigma names GsmServer its EXCLUSIVE distributor; Chimera credits only via GsmEasy/GsmServer; HalabTech catalog had a "GsmServer Products" group (Boot-Loader 2.0, GB Key, Smart Clip) 2022-2024; GsmServer launched DHRU Fusion Pro supplier API 2026-09-09', 'Candidate For (HalabTech groups)': 'Sigma Plus Digital; Sigma Activation; Chimera Activation; (historical) GsmServer Products', 'Evidence': 'EV-014, EV-027…029, ' + ev('A1-08', 'V-01', 'C-01', 'C-07', 'V-10', 'C-08')},
    'SUP-005': {'Confidence (R6)': 'LIKELY (UFI)', 'R6 Update': 'Martview = UFI worldwide distributor, Hydra WW agent, UMT WW distributor; HalabTech not on UFI list', 'Candidate For (HalabTech groups)': 'UFI; Box & Dongle (UFI hardware)', 'Evidence': 'EV-030, ' + ev('A1-16', 'A1-01', 'A1-14')},
    'SUP-006': {'Confidence (R6)': 'UNKNOWN', 'R6 Update': 'SimSim also UMT (UAE), Infinity (#1), DC-Unlocker (AE/IN) distributor', 'Evidence': 'EV-037, ' + ev('C-19')},
    'SUP-007': {'Confidence (R6)': 'UNKNOWN', 'R6 Update': 'SharkGSM / GSM-Sources also UMT, EME, Avengers distributors', 'Evidence': 'EV-037, ' + ev('C-19')},
    'SUP-008': {'Confidence (R6)': 'UNKNOWN', 'R6 Update': 'GsmGenesis and MyGSM24 are the same operator (Mukesh Raj); OumseGsm co-distributor with HalabTech; HalabTech "Distributor USA" agent link points to mygsm24.com'},
    'SUP-009': {'Confidence (R6)': 'CONFIRMED', 'R6 Update': 'Extended by SUP-028 (19+ further stores)'},
}

# ------------------------------------------------------------------ relationships
rel_hdr = ['Rel ID', 'Source', 'Target', 'Service', 'Type', 'Evidence', 'Confidence', 'Record Origin', 'Source Name', 'Target Name',
           'Direct API Shown?', 'Confidence (R6)', 'R6 Update']
rels = []
rn = 22


def rel(src, srcn, tgt, tgtn, svc, typ, refs, conf, api='No'):
    global rn
    rn += 1
    rels.append({'Rel ID': f'REL-{rn:03d}', 'Source': src, 'Target': tgt, 'Service': svc, 'Type': typ, 'Evidence': ev(*refs),
                 'Confidence': conf, 'Record Origin': 'R4-6 (new)', 'Source Name': srcn, 'Target Name': tgtn, 'Direct API Shown?': api,
                 'Confidence (R6)': conf, 'R6 Update': ''})
    return f'REL-{rn:03d}'


rel('VEN-012', 'Dhru', 'VEN-000', 'HalabTech', 'server.halabtech.com platform', 'Platform (footer)', ['OWN-01'], 'CONFIRMED')
rel('VEN-002', 'ChimeraTool', 'SUP-001 / SUP-012', 'GsmServer / GsmEasy', 'Chimera credits', 'Exclusive distribution contract', ['C-01', 'V-03', 'C-05'], 'CONFIRMED')
rel('SUP-001 / SUP-012', 'GsmServer or GsmEasy', 'VEN-000', 'HalabTech', 'Chimera Activation', 'Intermediate supplier (vendor rule; which one unknown)', ['C-01', 'C-06', 'V-10', 'A1-21'], 'STRONG')
rel('VEN-020', 'SigmaKey', 'SUP-001', 'GsmServer', 'Sigma Plus licences/credits', 'Exclusive distributor', ['A1-08', 'V-01'], 'CONFIRMED')
rel('SUP-001', 'GsmServer', 'VEN-000', 'HalabTech', 'Sigma Plus Digital; Sigma Activation', 'Intermediate supplier (vendor rule)', ['A1-08', 'V-01', 'A1-07'], 'STRONG')
rel('SUP-001', 'GsmServer', 'VEN-000', 'HalabTech', '"GsmServer Products" (Boot-Loader 2.0, GB Key, Smart Clip) 2022-2024', 'Supply of GsmServer-branded products', ['C-07', 'V-10'], 'LIKELY')
for vid, name, site, groups, role, refs, scope, model, dists, conf in V:
    if role.startswith('NOT LISTED') or vid in ('VEN-078', 'VEN-079', 'VEN-080'):
        continue
    typ = 'Distributor authorisation' if 'istribut' in role.lower() or 'main seller' in role.lower() else 'Reseller authorisation'
    if vid in ('VEN-075', 'VEN-076'):
        typ = 'Self-claimed distributorship (HalabTech Telegram)'
    if vid == 'VEN-077':
        typ = 'Product resale'
    rel(vid, name, 'VEN-000', 'HalabTech', '; '.join(SG[g] if isinstance(g, int) else g for g in groups) or '—', typ, refs, conf if conf != 'CONFIRMED (absence)' else 'CONFIRMED')
rel('VEN-045 / VEN-046', 'Hunter Unlocker / Q-Unlocker', 'VEN-000', 'HalabTech', 'Hunter Unlocker; Q-UNLOCKER Tool', 'Direct vendor supply (vendors sell to agents only via 3 distributors incl. HalabTech)', ['A2-14', 'A2-15', 'V-02'], 'STRONG')
rel('VEN-072', 'XTP – Xiaomi Tool Pro', 'VEN-000', 'HalabTech', 'XTP – Xiaomi Tool Pro', 'Direct vendor supply ("Official Main Seller")', ['D-07'], 'STRONG')
for vid, name, dists, refs, grp in (('VEN-028', 'Furious Gold', 'GSM Server / GsmEasy / GsmFastest / ADYunlocker / HACK3R2K / Click-Unlocker / acellsorios', ['A1-13'], 'Furious Gold Credits; Furious Gold Packages'),
                                     ('VEN-029', 'UMT / NCK', 'Fast Unlocking / GsmServer / GsmEasy / Martview / GSM Sources / SharkGSM / SimSim', ['A1-14'], 'UMT Products; UMT ACTIVATION FOR NCK USERS; NCK Products; NCK Online Digital'),
                                     ('VEN-030', 'Avengers Box', 'Fast Unlocking / GsmServer / GSM-Sources / GsmEasy / GsmSalman / Smart Unlock Mobile / Gsm Africa', ['A1-15'], 'Avengers Box'),
                                     ('VEN-031', 'UFI Box', 'Martview', ['A1-16'], 'UFI; Box & Dongle (UFI)'),
                                     ('VEN-069', 'SamKey', 'GsmEasy / SiRoYa', ['A2-NEG01'], 'SamKey Services'),
                                     ('VEN-070', 'AMT', 'GSM Credit / GsmGenesis / Ady Unlocker', ['A2-NEG02'], 'Android Multi Tool - AMT'),
                                     ('VEN-071', 'MH Unlocker Pro', 'iUnlocking Store / GsmFastest / Gsm Africa / Leope-Gsm / Infinity-Box', ['A2-NEG03'], 'MH Unlocker Pro'),
                                     ('VEN-013', 'EFT (Easy-Firmware)', 'Easy-Firmware arm / SimSim / GsmServer / GSM-Sources / SharkGSM / GsmEasy / GsmFastest / KhaledGsm', ['C-10', 'C-19'], 'EFT')):
    rel(f'{vid} → [{dists}]', f'{name} distributors', 'VEN-000', 'HalabTech', grp, 'Intermediate supplier (vendor omits HalabTech; identity unknown)', refs, 'LIKELY')
rel('SUP-019', 'GSM T-Tool', 'VEN-000', 'HalabTech', 'T-TOOL PRO', 'Possible intermediary (sole distributor)', ['A2-13'], 'LIKELY')
rel('SUP-020', 'Smart Tool Worldwide', 'VEN-000', 'HalabTech', 'SamsungTool.us CellTool', 'Possible intermediary (sole distributor)', ['A2-22'], 'LIKELY')
rel('SUP-018', 'ADY Unlocker', 'VEN-000', 'HalabTech', 'Panda Tools', 'Possible intermediary (sole distributor)', ['A2-36'], 'LIKELY')
rel('SUP-014', 'Code-GSM', 'VEN-000', 'HalabTech', 'T-MOBILE | SPRINT | METROPCS POLICY USA (Clean & Paid Off Only)', 'Candidate direct API supplier', ['B-01', 'B-02', 'V-07'], 'LIKELY')
rel('SUP-015', 'UnlocksPro', 'VEN-000', 'HalabTech', 'MDM Source 1#; Signal Labs; JDM V4 V5; Reseller Flex; Mi Account', 'Candidate upstream or sibling (direction unproven)', ['B-03', 'B-04', 'B-05', 'B-06', 'V-05'], 'LIKELY')
rel('Unnamed Source #1/#2/#3, "Server Direct", "Direct Source"', 'Unnamed IMEI sources', 'VEN-000', 'HalabTech', 'MDM / ID / FRP / Mi Account', 'Direct API suppliers (existence only)', ['OWN-03', 'D-04', 'V-08'], 'CONFIRMED (existence)', api='Yes (unnamed)')
rel('VEN-000', 'HalabTech', 'VEN-000', 'HalabTech', 'Premium Tecno/iTel/Infinix MDM (Source #1)', 'Self-claimed direct source', ['D-03', 'V-08'], 'LIKELY', api='Self-claim')
rel('VEN-079', 'iRemove', 'VEN-000', 'HalabTech', 'iPads/iWatch WIFI Only (iCloud Remove)', 'Original vendor; channel unknown', ['B-13'], 'UNKNOWN')
rel('VEN-078', 'Zeus/Hermes/Scylla/Kratos', 'VEN-000', 'HalabTech', 'iOS tool services (2023)', 'Historical product resale', ['V-04', 'D-05'], 'CONFIRMED (historical)')
rel('VEN-000', 'HalabTech', 'SUP-028', 'Downstream stores', 'HalabTech credits, memberships, IMEI services', 'Downstream resale / API clients', ['C-14', 'OWN-08', 'OWN-09', 'D-19', 'D-20', 'D-21', 'D-22', 'D-24', 'B-12', 'B-19'], 'CONFIRMED')
rel('VEN-000', 'HalabTech', 'SUP-029', 'World Agents (29)', 'All', 'Agent network', ['D-17'], 'CONFIRMED')
rel('VEN-000', 'HalabTech', 'Firmware brands (BLU, ZTE, Meizu, ASUS, Huawei)', 'Content sources', 'Firmware portal', 'HalabTech seeks to BUY official firmware-source access', ['D-25', 'B-18'], 'CONFIRMED')
prior_rel_updates = {
    'REL-002': {'Confidence (R6)': 'CONFIRMED (Reseller)', 'R6 Update': 'HalabTech is a plain reseller; credits must come from GsmEasy/GsmServer – see REL-024/025'},
    'REL-014': {'Confidence (R6)': 'STRONG (Sigma) / LIKELY (GsmServer Products)', 'R6 Update': 'See REL-027/028; still no observed API link'},
    'REL-015': {'Confidence (R6)': 'CONFIRMED', 'R6 Update': 'Full EFT list read (C-10)'},
    'REL-016': {'Confidence (R6)': 'LIKELY', 'R6 Update': 'HalabTech absent from full EFT list ⇒ an EFT channel sits between vendor and HalabTech; identity unknown'},
    'REL-017': {'Confidence (R6)': 'CONFIRMED', 'R6 Update': 'Footer "Powered by Dhru Fusion" (REL-023)'},
    'REL-022': {'Confidence (R6)': 'CONFIRMED (status)', 'R6 Update': 'RapidFlashTool lists HalabTech "Distributor (Worldwide)"'},
    'REL-008': {'Confidence (R6)': 'STRONG', 'R6 Update': 'Third-party mirror repeats listing; vendor page still blocked'},
}

# ------------------------------------------------------------------ unknown suppliers (ranked)
unk_hdr = ['Rank', 'Service', 'Original Vendor', 'Suspected', 'Missing Evidence', 'Reason', 'Priority', 'Next Action', 'Record Origin', 'SKUs', 'Confidence (R6)']
U = [
    ('IMEI carrier unlocks (T-Mobile/Sprint, Reseller Flex, AT&T, Spectrum, XFINITY, EU/Japan networks)', 'Carriers', 'Code-GSM (T-Mobile Clean), UnlocksPro (Reseller Flex), unnamed premium sources', 'Any page naming HalabTech as client; consistent price snapshots', 'Dhru routing is private; identical names shared by many servers', 54, 'LIKELY (2 candidates)'),
    ('Tecno/iTel/Infinix MDM & ID removal (Source #1/#2/#3)', 'Transsion', 'HalabTech itself (Source #1 claim), UnlocksPro; Source #2/#3 unnamed', 'Identity of Source #2/#3', 'HalabTech labels sources by number only', 18, 'CONFIRMED multi-source / UNKNOWN identities'),
    ('Samsung network repair / CPID (EDL Binary, JDM V4/V5, V1-V3)', 'Samsung (exploit operators)', 'UnlocksPro (JDM V4/V5), Best4unlock (EDL), IN-GSM, cpidserver', 'Origin operator', 'Grey-market CPID servers do not publish resellers', 61, 'LIKELY (JDM) / UNKNOWN (EDL, V1-V3)'),
    ('iCloud FMI OFF – iPad/iWatch WiFi (iREMOVE)', 'iRemove Software', 'iRemove partner programme (DHRU API) or an iRemove partner', 'Partner list; price path (HalabTech $25-70 above iRemove public)', 'Partner area login-only', 60, 'UNKNOWN'),
    ('Xiaomi Mi Account (62 SKUs, ~20 countries)', 'Xiaomi (grey market)', '"Server Direct", "Direct Source", "Source2 #Cheaper"; UnlocksPro (Rocket pair)', 'Any named source', 'Multiple unnamed sources', 62, 'UNKNOWN'),
    ('Chimera credits/licences', 'ChimeraTool', 'GsmEasy OR GsmServer (vendor rule); Unlock.eu card', 'Which distributor', 'Vendor rule proves an intermediary, not which', 5, 'STRONG (intermediary) / UNKNOWN (identity)'),
    ('EFT Dongle / EFT Pro', 'Easy-Firmware team', 'Easy-Firmware arm or 9 WW distributors', 'Which EFT channel', 'HalabTech absent from EFT list', 7, 'LIKELY (intermediary) / UNKNOWN (identity)'),
    ('UMT / NCK / Avengers', 'UMT team', 'Fast Unlocking, GsmServer, GsmEasy, Martview, GSM Sources, SharkGSM, SimSim', 'Which distributor', 'HalabTech absent from vendor lists', 13, 'LIKELY (intermediary)'),
    ('Furious Gold', 'FuriousTeam', 'GSM Server, GsmEasy, GsmFastest, ADYunlocker, HACK3R2K, Click-Unlocker, acellsorios (or FG web shop)', 'Which distributor', 'HalabTech absent from FG list', 30, 'LIKELY (intermediary)'),
    ('Sigma / Sigma Plus', 'SigmaKey', 'GsmServer (exclusive distributor)', 'Order/API evidence', 'Vendor rule only', 5, 'STRONG'),
    ('GSX / Apple checkers (132 SKUs)', 'Apple data brokers', 'Unnamed source with #225/#33225 numbering; Best4unlock sibling', 'Origin server', 'Names copied across 15+ servers', 132, 'UNKNOWN'),
    ('Gift cards & game top-ups (iTunes, Google Play, PlayStation, PUBG, Free Fire)', 'Apple/Google/Sony/Tencent/Garena', '—', 'Any', 'Not researched beyond catalog', 63, 'UNKNOWN'),
    ('Telecom top-ups (Syriatel, MTN Syria, Turkcell, Türk Telekom, PayCell)', 'Operators', '—', 'Any', 'No other store uses the same names', 18, 'UNKNOWN'),
    ('AI / digital subscriptions (ChatGPT, Claude, Cursor, Grok…)', 'AI vendors', '—', 'Any', 'Not researched', 38, 'UNKNOWN'),
    ('SamKey / AMT / MH Unlocker', 'Respective vendors', 'GsmEasy/SiRoYa; GSM Credit/GsmGenesis/ADY; iUnlocking Store et al.', 'Which distributor', 'HalabTech absent from vendor lists', 9, 'LIKELY (intermediary)'),
    ('Cheetah Tool', 'Cheetah', 'Direct or 8 named distributors (incl. GSMserver)', 'Channel', 'HalabTech is reseller, not distributor', 6, 'UNKNOWN'),
    ('Long tail: ~150 small auth/FRP tool groups not yet checked', 'Various', 'Direct from vendor (pattern) or Thai/Yemen tool families\' distributors', 'Vendor lists', 'Budget', 330, 'UNKNOWN'),
    ('Schematics/hardware software without public lists (ZXW, JCID, Refox, Orion, FCL, Zhizhen, YCS, Lanrui, W2R, Setool, Nemesis)', 'Various', '—', 'Vendor lists', 'No public list found', 40, 'UNKNOWN'),
    ('Physical hardware (Box & Dongle, 40 SKUs)', 'Box makers', 'Hardware distributors (Martview, GsmServer…)', 'Any', 'Not researched', 40, 'UNKNOWN'),
]
unk_rows = []
for i, (svc, ov, sus, miss, reason, skus, conf) in enumerate(U, 1):
    prio = 'Critical' if i <= 5 else ('High' if i <= 11 else 'Medium')
    unk_rows.append({'Rank': i, 'Service': svc, 'Original Vendor': ov, 'Suspected': sus, 'Missing Evidence': miss, 'Reason': reason,
                     'Priority': prio, 'Next Action': 'See Next Research Plan', 'Record Origin': 'R4-6 (new)', 'SKUs': skus, 'Confidence (R6)': conf})
prior_unk_updates = {
    'SVC-024 T-Mobile Policy': {'Confidence (R6)': 'LIKELY (Code-GSM)', 'Rank': 1},
    'SVC-025 iREMOVE': {'Confidence (R6)': 'UNKNOWN (iRemove partner programme)', 'Rank': 4},
    'SVC-026 Mi Account': {'Confidence (R6)': 'UNKNOWN', 'Rank': 5},
    'SVC-013/014 EFT': {'Confidence (R6)': 'LIKELY intermediary (HalabTech absent from EFT list)', 'Rank': 7},
    'SVC-012 RapidFlash': {'Confidence (R6)': 'RESOLVED status: Distributor (Worldwide)'},
    'SVC-018/019 Dhru': {'Confidence (R6)': 'Platform CONFIRMED; licence channel LIKELY Dhru'},
    'SVC-027 Ameer Tool': {'Confidence (R6)': 'RESOLVED: GSMUNBRICK lists HalabTech as Distributor/Reseller WW'},
    'SVC-028–033': {'Confidence (R6)': 'Partly resolved (Hydra, Z3X, CM2 listings); PUBG/telecom/AI UNKNOWN'},
}

# ------------------------------------------------------------------ gaps
gap_hdr = ['Gap ID', 'Question', 'Related', 'Missing', 'Suggested Queries', 'Priority', 'Status', 'Record Origin', 'Status (R6)', 'R6 Outcome']
prior_gap_updates = {
    'GAP-001': {'Status (R6)': 'Narrowed', 'R6 Outcome': 'Multi-source routing CONFIRMED (Source #1/#2/#3); Code-GSM and UnlocksPro LIKELY; no named supplier proven'},
    'GAP-002': {'Status (R6)': 'Resolved', 'R6 Outcome': 'Full EFT list read: HalabTech absent (→ GAP-012)'},
    'GAP-003': {'Status (R6)': 'Resolved', 'R6 Outcome': 'RapidFlashTool lists HalabTech "Distributor (Worldwide)"'},
    'GAP-004': {'Status (R6)': 'Partly resolved', 'R6 Outcome': 'STRONG for Sigma (exclusive distributor); STRONG-shared for Chimera; LIKELY for "GsmServer Products" 2022-24; no API evidence'},
    'GAP-005': {'Status (R6)': 'Open', 'R6 Outcome': 'Vendor page still bot-blocked; third-party mirror repeats listing'},
    'GAP-006': {'Status (R6)': 'Resolved', 'R6 Outcome': 'Footer "Powered by Dhru Fusion" captured'},
    'GAP-007': {'Status (R6)': 'Resolved', 'R6 Outcome': 'WARD = downstream; GSMMUNNA/DZGSM/FirmwareDrive/FirmwareWorld = peers, no link; Ameer Tool = GSMUNBRICK (HalabTech distributor)'},
    'GAP-008': {'Status (R6)': 'Resolved (for 65 vendors)', 'R6 Outcome': '51 additional vendors list HalabTech (62 in total, CONFIRMED/STRONG); 8 checked vendor lists omit it'},
    'GAP-009': {'Status (R6)': 'Partly resolved', 'R6 Outcome': 'Wayback captures 2021-11 … 2024-09 read (catalog sizes, Chimera package, DFT listing)'},
    'GAP-010': {'Status (R6)': 'Partly resolved', 'R6 Outcome': 'Many stores copy HalabTech text verbatim (LIKELY API clients); HalabTech advertises "Connect API NOW"'},
}
G = [
    ('GAP-011', 'Which Chimera distributor (GsmEasy, GsmServer or Unlock.eu) supplies HalabTech?', 'Chimera Activation', 'Order/API trace; price parity at 20k-credit tier', '"HalabTech" GsmEasy chimera; gsmeasy reseller list; chimera credit price gsmserver vs gsmeasy', 'High'),
    ('GAP-012', 'Which EFT channel (Easy-Firmware arm vs a WW distributor) supplies HalabTech?', 'EFT', 'Any linkage', 'eftprodongle.com country pages; "EFT" "halabtech" telegram', 'High'),
    ('GAP-013', 'Which UMT/NCK/Avengers/Furious Gold distributor supplies HalabTech?', 'UMT, NCK, Avengers, Furious Gold', 'Price back-calculation vs distributor price lists', 'fastunlocking.com UMT price; gsmeasy UMT; furiousgold credits price distributors', 'High'),
    ('GAP-014', 'Is Code-GSM upstream of HalabTech (or a sibling)? Resolve listing vs detail price conflict', 'T-Mobile Clean & Paid Off', 'Same-day snapshot of all tiers on both sites', 'code-gsm.com servicedtl till-12/14, till-xs, till-17', 'High'),
    ('GAP-015', 'Direction HalabTech ↔ UnlocksPro (who copies whom; any API)', 'MDM Source 1#, JDM, Signal Labs, Reseller Flex', 'Dated first-appearance of identical services', 'Wayback unlockspro.com/resellerpricing/imei; t.me/halabtech2 first-post dates', 'High'),
    ('GAP-016', 'Is HalabTech an iRemove partner, or does it buy via another partner?', 'iPads/iWatch WIFI Only', 'Partner list or iRemove announcement', 'iremove partners DHRU list; "iRemove" "HalabTech"', 'High'),
    ('GAP-017', 'Public Service IDs (Dhru pid) for all 1,455 SKUs', 'All services', 'JS-rendered cart pages', 'Firecrawl actions/waitFor on /cart/group/<id>', 'Medium'),
    ('GAP-018', '~150 long-tail tool vendors and 11 schematic/hardware vendors without public lists', 'Long tail', 'Vendor reseller pages', '"<tool> resellers" + "halabtech"', 'Medium'),
    ('GAP-019', 'Gift-card / game / telecom / AI-subscription suppliers', '63 + 18 + 38 SKUs', 'Any named wholesaler', 'Syriatel API wholesale; PUBG UC API supplier dhru', 'Medium'),
    ('GAP-020', 'Markup fingerprinting: do 3-decimal prices (cost × 1.10) match a candidate\'s public cost?', 'All AUTO API groups', 'Candidate price lists', 'compare 15.125/1.1=13.75 etc. with GsmServer/GsmEasy/Fast Unlocking', 'Medium'),
    ('GAP-021', 'Why did the catalog shrink (Dec 2022: 385 groups/1,705 SKUs → 2026: 321/985; IMEI 660 → 470)? Lost suppliers?', 'Catalog history', 'Diff of dropped groups', 'Wayback 2023-2025 captures', 'Medium'),
    ('GAP-022', 'Legal entity / beneficial owner of HalabTech', 'VEN-000', 'Registry record', 'Turkish/Syrian/US registries; "Hosam" "HalabTech"', 'Low'),
]
gap_rows = [{'Gap ID': a, 'Question': b, 'Related': c, 'Missing': d, 'Suggested Queries': e, 'Priority': f, 'Status': 'Open',
             'Record Origin': 'R4-6 (new)', 'Status (R6)': 'Open', 'R6 Outcome': ''} for a, b, c, d, e, f in G]

# ------------------------------------------------------------------ tool log / counts
tool_counts = collections.Counter()
tool_fail = collections.Counter()
per_stream = []
for s in STREAMS:
    c = collections.Counter(); fl = collections.Counter()
    for t in F[s]['tool_log']:
        k = tool_label(t['tool'])
        c[k] += 1
        if not t.get('ok', True):
            fl[k] += 1
    tool_counts.update(c); tool_fail.update(fl)
    per_stream.append((s, c, fl))
mcp_total = sum(v for k, v in tool_counts.items() if k.split(' ')[0] in ('Firecrawl', 'Parallel', 'Exa'))

# ------------------------------------------------------------------ research history
hist_hdr = ['Round', 'Topic', 'Tools', 'Example Queries', 'New Findings', 'Confidence Changes', 'Remaining', 'Record Origin']


def tools_of(*ss):
    c = collections.Counter()
    for s in ss:
        for t in F[s]['tool_log']:
            c[tool_label(t['tool'])] += 1
    return '; '.join(f'{k} ×{v}' for k, v in sorted(c.items()))


hist_rows = [
    {'Round': '4', 'Topic': 'Discovery: MCP tests, full catalog, vendor-list sweep (majors + long tail)', 'Tools': tools_of('OWN', 'A1', 'A2'),
     'Example Queries': 'Firecrawl scrape /resellerpricing/server & /imei; "<tool> official resellers distributors"; "server.halabtech.com" resellers; hwkey/devicesavior/oumsegsm resellers',
     'New Findings': '383 groups / 1,455 SKUs; Dhru footer; 47 new vendor listings; Sigma exclusive distributor GsmServer; Hunter/Q-Unlocker distributors-only; 7 vendors omit HalabTech',
     'Confidence Changes': 'Dhru LIKELY→CONFIRMED; GsmServer upstream UNKNOWN→STRONG (Sigma)', 'Remaining': 'IMEI sources; which Chimera/EFT/UMT distributor', 'Record Origin': 'R4-6 (new)'},
    {'Round': '5', 'Topic': 'Deep investigation: IMEI fingerprints, intermediaries, Wayback history, HalabTech Telegram/news, downstream', 'Tools': tools_of('B', 'C', 'D'),
     'Example Queries': '"#33225" "Case History Check"; "Signal Labs Technology Tool"; chimeratool resellers-sales-system; web.archive.org/web/2022/server.halabtech.com; t.me/s/halabtech2?q=source',
     'New Findings': 'Code-GSM & UnlocksPro candidates; Chimera rule full page; 2022 Chimera 20k-credit packs; "GsmServer Products" group 2022-24; RapidFlash & Ameer Tool listings; Source #1/#2/#3 posts; 29 world agents; 19+ downstream stores',
     'Confidence Changes': 'Chimera supply → STRONG intermediary; EFT → LIKELY intermediary; RapidFlash → CONFIRMED status', 'Remaining': 'Supplier identities behind numbered sources', 'Record Origin': 'R4-6 (new)'},
    {'Round': '6', 'Topic': 'Independent verification & challenge (second tool on key claims)', 'Tools': tools_of('V'),
     'Example Queries': 'Re-fetch sigmakey 15258, hunter-unlocker, chimera doc, code-gsm detail/listing, t.me/s/halabtech2?before=25390 & 39432, infinity-box.com/buy, unlockspro index, news.halabtech.com',
     'New Findings': 'All vendor quotes re-confirmed; Zeus reclassified as iOS tool brand; Code-GSM price conflict found',
     'Confidence Changes': 'D-05 Zeus "API supplier" → original tool vendor (historical); B-01 Code-GSM LIKELY with DISPUTED lower tiers', 'Remaining': 'See Next Research Plan', 'Record Origin': 'R4-6 (new)'},
]

# ------------------------------------------------------------------ website inventory
inv_hdr = ['URL', 'Category', 'Crawl Status', 'Extraction', 'Record Origin', 'Tool', 'Last Checked']
seen = set(r['URL'] for r in prior['Website Inventory']['rows'])
inv_rows = []
for e in evidence:
    u = e['Source URL']
    if not u.startswith('http') or u in seen:
        continue
    seen.add(u)
    cat = e['Type'] or 'Other'
    inv_rows.append({'URL': u, 'Category': cat, 'Crawl Status': 'Fetched' if 'full' in e['Access'] else ('Snippet' if 'snippet' in e['Access'] else e['Access']),
                     'Extraction': 'Full' if 'full' in e['Access'] else 'Partial', 'Record Origin': e['Record Origin'], 'Tool': e['Tool'], 'Last Checked': DATE})
for u, cat, st, ex in (('https://server.halabtech.com/viewrss', 'HalabTech official', 'Fetched', 'Empty feed'),
                       ('https://server.halabtech.com/cart/group/250/service/server/groupname/Furious-Gold', 'HalabTech official', 'Fetched', 'Client-side products (none rendered)'),
                       ('https://digital.halabtech.com / https://course.halabtech.com', 'HalabTech subdomains', 'Blocked', 'HTTP 403')):
    if u not in seen:
        inv_rows.append({'URL': u, 'Category': cat, 'Crawl Status': st, 'Extraction': ex, 'Record Origin': 'R4-6 (new)', 'Tool': 'Firecrawl scrape', 'Last Checked': DATE})

# ------------------------------------------------------------------ conflicts & corrections
cl_hdr = ['Claim', 'Previous Conclusion', 'New Evidence', 'Updated Conclusion', 'Evidence', 'Resolution', 'Record Origin']
CL = [
    ('CL-009', 'Chimera: HalabTech "distributor/reseller" (working brief)', 'HalabTech card unlabeled; 2023 "(reseller)"; vendor: only GsmEasy/GsmServer distributors; HalabTech sold 20k-credit packs in 2022', 'HalabTech = Chimera RESELLER buying via GsmEasy or GsmServer (STRONG)', ['C-01', 'C-03', 'C-04', 'C-06', 'V-03', 'V-10'], 'Corrected'),
    ('CL-010', 'Catalog size ≥240 groups (truncated at 239)', 'Full Firecrawl scrape: 321 server + 62 IMEI groups; 985 + 470 SKUs. Dec 2022: 385 groups / 1,705 SKUs', '383 groups / 1,455 SKUs today; catalog shrank since 2022', ['OWN-02', 'C-17'], 'Resolved'),
    ('CL-011', 'Public Service ID "not exposed publicly"', 'Product URLs carry ?pid= (e.g. 4113); only 3 indexed; cart pages render client-side', 'IDs exist per product page; bulk extraction needs JS rendering', ['OWN-06'], 'Corrected'),
    ('CL-012', 'Zeus = named upstream API supplier (stream D, LIKELY)', 'Same-day posts: "ZeusTool Auto Plist Reader", "Hermes Tool Auto Plist Reader", Scylla/Kratos tool links', 'Zeus/Hermes/Scylla/Kratos are iOS tool brands HalabTech resold in 2023 – original vendors, not wholesale suppliers', ['D-05', 'V-04'], 'Corrected'),
    ('CL-013', 'Code-GSM supplies T-Mobile Clean & Paid Off (stream B, LIKELY)', 'Detail pages $43.99/$63.45 (HalabTech $44.99/$66.45) but listing shows $45/$60/$58 for lower tiers (> HalabTech $36.99/$38.99)', 'LIKELY for Till 15/16/17 only; lower tiers contradict', ['B-01', 'V-07'], 'Disputed'),
    ('CL-014', 'GsmServer → HalabTech upstream UNKNOWN (R1-3)', 'Sigma exclusive distributor; Chimera 1 of 2; "GsmServer Products" group 2022-24', 'STRONG for Sigma; STRONG-shared for Chimera; LIKELY historical; still no API evidence', ['A1-08', 'V-01', 'C-07', 'V-10'], 'Partly resolved'),
    ('CL-015', 'Cheetah lists HalabTech as distributor (Exa snippet near "Distributor GSMserver")', 'Full page: HalabTech labelled Reseller', 'Reseller, not distributor', ['A1-09'], 'Corrected'),
    ('CL-016', 'Scorpion Tool: cached copy omits HalabTech', 'Live Firecrawl scrape lists HalabTech under Official Resellers', 'Listed (live page authoritative)', ['A2-16'], 'Resolved'),
    ('CL-017', 'HalabTech "We are only a reseller" (news template)', 'Telegram 2026-10-05: "We are the direct source for Premium Services"', 'Template text is generic; self-claimed direct source applies to Premium Tecno/iTel/Infinix MDM only', ['D-01', 'V-06', 'D-03', 'V-08'], 'Documented'),
    ('CL-018', '"Amir Tech" ≈ "Ameer Tool" (name match only)', 'Ameer Tool is made by GSMUNBRICK (Syria); lists HalabTech as Distributor/Reseller WW', 'Ameer Tool resolved; "Amir Tech" unrelated/unknown', ['A2-37', 'C-12'], 'Resolved'),
    ('CL-019', 'AuthFlash official seller (R1-3)', 'No AuthFlash SKU in today\'s catalog', 'Listing possibly stale', ['OWN-07'], 'Documented'),
    ('CL-020', 'EME page', 'https returns 404; http lists "HALABTECH | Distributors / Turkey"; Turkey filter view empty', 'Listed (http page)', ['A1-12', 'C-15'], 'Documented'),
    ('CL-021', 'Chimera "two distributors" vs 3 Distributor cards', 'Live page shows 3rd card Unlock.eu', 'Vendor text and page differ; Unlock.eu kept as candidate', ['A1-21', 'C-03'], 'Open'),
]
cl_rows = [{'Claim': a, 'Previous Conclusion': b, 'New Evidence': c, 'Updated Conclusion': d, 'Evidence': ev(*e), 'Resolution': f, 'Record Origin': 'R4-6 (new)'} for a, b, c, d, e, f in CL]
prior_cl_updates = {'CL-001': {'Resolution': 'Partly resolved (see CL-014)'}, 'CL-003': {'Resolution': 'Resolved – CONFIRMED (Dhru footer)'}, 'CL-005': {'Resolution': 'Open (vendor page still blocked)'}}

# ------------------------------------------------------------------ next research plan
plan_hdr = ['Priority', 'Question', 'Candidates', 'Tools', 'Queries', 'Completion Criteria', 'Record Origin', 'Status (R6)']
prior_plan_updates = {'1': {'Status (R6)': 'Done (narrowed)'}, '2': {'Status (R6)': 'Done'}, '3': {'Status (R6)': 'Done'}, '4': {'Status (R6)': 'Done for 65 vendors'}, '5': {'Status (R6)': 'Done (8 captures)'}}
P = [
    ('R7-1', 'Which Chimera distributor serves HalabTech? (GAP-011)', 'GsmEasy, GsmServer, Unlock.eu', 'Parallel, Exa, Firecrawl', '"GsmEasy" "HalabTech"; site:gsmeasyshop.com chimera; chimeratool.com/en/resellers?featured=1 distributor prices', 'Named distributor with primary-source link'),
    ('R7-2', 'Code-GSM vs HalabTech same-day price snapshot (GAP-014)', 'Code-GSM', 'Firecrawl (maxAge 0)', 'code-gsm.com servicedtl till-xs, till-12/14, till-15, till-16, till-17', 'All 6 tiers compared on one date'),
    ('R7-3', 'UnlocksPro ↔ HalabTech direction (GAP-015)', 'UnlocksPro', 'Firecrawl (Wayback), Exa', 'web.archive.org/web/2024*/unlockspro.com/resellerpricing/imei; t.me/s/halabtech2?q=JDM', 'Earliest dated appearance on each side'),
    ('R7-4', 'iRemove partner channel (GAP-016)', 'iRemove, GsmServer (sells iRemove iPad)', 'Parallel, Exa', '"iRemove" partner DHRU list; gsmserver iRemove FMI OFF price vs HalabTech', 'Partner identified or ruled out'),
    ('R7-5', 'Price back-calculation (GAP-020)', 'GsmServer, GsmEasy, Fast Unlocking, Martview', 'Firecrawl', 'UMT/NCK/FG/Sigma/EFT price pages of candidates', 'Cost × markup match for ≥3 products'),
    ('R7-6', 'EFT channel (GAP-012)', 'Easy-Firmware, FAST PROVISION, GsmServer…', 'Firecrawl', 'eftprodongle.com resellers country pages; fastprovision.com EFT', 'HalabTech found/not found on each'),
    ('R7-7', 'Bulk public pids (GAP-017)', '—', 'Firecrawl actions', '/cart/group/<id>/viewmode/grid/service/product/', '≥80% SKUs with pid'),
    ('R7-8', 'Long-tail vendor lists (GAP-018)', '~150 tools', 'Exa batch, Parallel', '"<tool> resellers" halabtech', 'Top 50 by SKU count checked'),
    ('R7-9', 'Catalog shrinkage diff (GAP-021)', '—', 'Firecrawl (Wayback)', 'web.archive.org/web/2023/2025 server.halabtech.com/resellerpricing/server', 'List of dropped groups with dates'),
]
plan_rows = [{'Priority': a, 'Question': b, 'Candidates': c, 'Tools': d, 'Queries': e, 'Completion Criteria': f, 'Record Origin': 'R4-6 (new)', 'Status (R6)': 'Planned'} for a, b, c, d, e, f in P]

# ------------------------------------------------------------------ price comparison
price_hdr = ['Product', 'HalabTech', 'Other stores', 'Record Origin', 'Interpretation', 'Evidence']
price_rows = [
    {'Product': 'T-Mobile/Sprint/MetroPCS Policy – iPhone Till 15 [Clean & Paid Off]', 'HalabTech': '$44.99', 'Other stores': 'Code-GSM detail $43.99 (listing $58)', 'Interpretation': '+$1.00 vs detail page', 'Evidence': ev('B-01', 'V-07')},
    {'Product': '… Till 16 [Clean & Paid Off]', 'HalabTech': '$66.45', 'Other stores': 'Code-GSM detail $63.45 (listing $63)', 'Interpretation': '+$3.00', 'Evidence': ev('B-01', 'V-07')},
    {'Product': '… Till 17 [Clean & Paid Off]', 'HalabTech': '$82.49', 'Other stores': 'Code-GSM $79.49 (listing $79)', 'Interpretation': '+$3.00', 'Evidence': ev('B-01', 'V-07')},
    {'Product': '… Till 12/14 vs Code-GSM Till 13/14 & 11/12', 'HalabTech': '$38.99', 'Other stores': 'Code-GSM listing $60 / $45', 'Interpretation': 'HalabTech BELOW Code-GSM – contradicts Code-GSM as source for these tiers', 'Evidence': ev('V-07')},
    {'Product': 'iREMOVE FMI OFF – iPad (10th gen) WiFi [iPad13,18]', 'HalabTech': '$150', 'Other stores': 'iRemove public $100', 'Interpretation': 'HalabTech +$50 over vendor public price', 'Evidence': ev('B-13')},
    {'Product': 'Chimera credits (reseller package, min 20,000)', 'HalabTech': '$0.112 (2022-01) / $0.101 (2022-12)', 'Other stores': 'HalabTech retail $0.11 today (NOT FOR WEB OWNER)', 'Interpretation': 'Distributor-tier volume sold by a non-distributor ⇒ upstream GsmEasy/GsmServer', 'Evidence': ev('C-06', 'V-10')},
    {'Product': 'Sigma Plus credits (reseller cost)', 'HalabTech': 'Sigma Plus 12M $59.40; Digital 3M $60.26', 'Other stores': 'gsmserver.com reseller credits $0.83-0.87 (min 1,000)', 'Interpretation': 'Credit-per-licence ratio not public; test pending (GAP-020)', 'Evidence': ev('A1-08')},
]
for r in price_rows:
    r['Record Origin'] = 'R4-6 (new)'

# ------------------------------------------------------------------ prior service updates & links
ps = {}


def psu(svc, catalog, gname, conf, status, note='', pid='', status_at_vendor=None, fm=None, evs=''):
    gid_note = gname
    ps[svc] = {'group': gname, 'confidence': conf, 'status': status, 'note': note, 'pid': pid, 'evidence': evs,
               'status_at_vendor': status_at_vendor if status_at_vendor is not None else GM.get(gname, {}).get('status_at_vendor', ''),
               'fulfilment_model': fm or '', 'url': f'https://server.halabtech.com/resellerpricing/{"imei" if catalog == "IMEI" else "server"}'}


psu('SVC-001', 'S', SG[258], 'LIKELY', 'Partial'); psu('SVC-002', 'S', SG[258], 'LIKELY', 'Partial')
psu('SVC-003', 'S', SG[213], 'LIKELY', 'Partial', evs=ev('C-16', 'D-10'))
psu('SVC-004', 'S', SG[213], 'LIKELY', 'Partial', 'Public pid 4113 = [New Users] 2 Year', pid='4113', evs=ev('OWN-06'))
psu('SVC-005', 'S', SG[242], 'STRONG', 'Partial', 'Credits must come from GsmEasy or GsmServer (vendor rule)', evs=ev('C-01', 'V-03'))
psu('SVC-006', 'S', SG[215], 'LIKELY', 'Partial'); psu('SVC-007', 'S', SG[206], 'LIKELY', 'Partial')
psu('SVC-008', 'S', SG[295], 'LIKELY', 'Partial'); psu('SVC-009', 'S', SG[228], 'LIKELY', 'Partial'); psu('SVC-010', 'S', SG[228], 'LIKELY', 'Partial')
psu('SVC-011', 'S', SG[132], 'LIKELY', 'Partial')
psu('SVC-012', 'S', SG[151], 'LIKELY', 'Partial', 'Vendor lists HalabTech Distributor (Worldwide)', evs=ev('C-11'))
psu('SVC-013', 'S', SG[240], 'LIKELY (intermediary)', 'Open', 'HalabTech absent from full EFT list', evs=ev('C-10'))
psu('SVC-014', 'S', SG[240], 'LIKELY (intermediary)', 'Open', 'HalabTech absent from full EFT list', evs=ev('C-10'))
psu('SVC-015', 'S', SG[105], 'LIKELY', 'Partial'); psu('SVC-016', 'S', SG[231], 'LIKELY', 'Partial'); psu('SVC-017', 'S', SG[207], 'LIKELY', 'Partial')
psu('SVC-018', 'S', SG[214], 'LIKELY', 'Partial', 'Dhru platform CONFIRMED', evs=ev('OWN-01'))
psu('SVC-019', 'S', SG[214], 'LIKELY', 'Partial', 'Dhru platform CONFIRMED', evs=ev('OWN-01'))
psu('SVC-020', 'S', SG[247], 'CONFIRMED', 'Resolved', fm='In-house'); psu('SVC-021', 'S', SG[247], 'CONFIRMED', 'Resolved', fm='In-house')
psu('SVC-022', 'S', '', 'CONFIRMED', 'Resolved', 'Reseller packages (2,500/5,000/10,000 credits) seen 2024-09; none in 2026 catalog', fm='In-house', evs=ev('C-17'))
psu('SVC-023', 'S', '', 'CONFIRMED', 'Resolved', fm='In-house')
psu('SVC-024', 'IMEI', IG[18], 'LIKELY', 'Partial', 'Candidate Code-GSM (price conflict on lower tiers)', evs=ev('B-01', 'V-07'))
psu('SVC-025', 'IMEI', IG[20], 'UNKNOWN', 'Open', 'Original vendor iRemove; channel unknown; today $150 (was $160)', evs=ev('B-13'))
psu('SVC-026', 'IMEI', IG[36], 'UNKNOWN', 'Open', '"Server Direct" – unnamed source', evs=ev('OWN-03'))
psu('SVC-027', 'S', SG[67], 'LIKELY', 'Partial', 'Ameer Tool = GSMUNBRICK; HalabTech Distributor/Reseller WW', evs=ev('A2-37', 'C-12'))
psu('SVC-028', 'S', SG[193], 'LIKELY', 'Partial', 'Hydra lists HalabTech as agent', evs=ev('A1-01', 'A1-02'))
psu('SVC-029', 'S', SG[168], 'LIKELY', 'Partial', 'Z3X lists HalabTech as reseller', evs=ev('A1-03'))
psu('SVC-030', 'S', SG[179], 'LIKELY', 'Partial', 'Infinity lists HalabTech as Distributor #7', evs=ev('A1-05', 'V-09'))
psu('SVC-031', 'S', SG[238], 'UNKNOWN', 'Open'); psu('SVC-032', 'S', SG[80], 'UNKNOWN', 'Open'); psu('SVC-033', 'S', SG[172], 'UNKNOWN', 'Open')
psu('SVC-034', 'S', '', 'UNKNOWN', 'Open', 'No AuthFlash SKU in 2026-10-11 catalog', evs=ev('OWN-07'))
# group id lookup for prior updates
gid = {}
for i, g in enumerate(server['groups']):
    gid[g['name']] = f'GRP-S-{i:03d}'
for i, g in enumerate(imei['groups']):
    gid[g['name']] = f'GRP-I-{i:03d}'
for k, v in ps.items():
    v['group_id'] = gid.get(v['group'], '')

LINKS = {'SVC-001': ('Server', SG[258], 'UnlockTool 12 months'), 'SVC-002': ('Server', SG[258], 'UnlockTool 3 months'),
         'SVC-003': ('Server', SG[213], 'DFT PRO TOOL ACTIVATION [New Users] 1 Year'), 'SVC-004': ('Server', SG[213], 'DFT PRO TOOL ACTIVATION [New Users] 2 Year'),
         'SVC-005': ('Server', SG[242], 'Chimera Tool Basic'), 'SVC-008': ('Server', SG[295], 'Xiaomi King Tool'),
         'SVC-012': ('Server', SG[151], 'Rapid Flash Tool'), 'SVC-013': ('Server', SG[240], '[1 Year] New User'), 'SVC-014': ('Server', SG[240], 'EFT Dongle 1 Year'),
         'SVC-015': ('Server', SG[105], '1 Year 1 Pc'), 'SVC-018': ('Server', SG[214], 'New License for Wholesale Server'), 'SVC-019': ('Server', SG[214], 'Supplier panel'),
         'SVC-020': ('Server', SG[247], 'Platinum 12 Months'), 'SVC-021': ('Server', SG[247], 'HalabTech Credits Any Quantity'),
         'SVC-024': ('IMEI', IG[18], 'Till 17'), 'SVC-025': ('IMEI', IG[20], 'iPad13,18'), 'SVC-026': ('IMEI', IG[36], 'JAPAN'),
         'SVC-027': ('Server', SG[67], '[1 PC - 1 Year] Digital'), 'SVC-028': ('Server', SG[193], '(100 Credits)'), 'SVC-030': ('Server', SG[179], '1 Month')}
links, pids = {}, {}
for svc, (cat, g, sub) in LINKS.items():
    data = server if cat == 'Server' else imei
    for s in data['services']:
        if s['group'] == g and sub.lower() in s['service'].lower():
            links[f"{cat}|{g}|{s['service']}"] = svc
            break
for s in server['services']:
    if s['group'] == SG[213] and s['service'] == 'DFT PRO TOOL ACTIVATION [New Users] 2 Year':
        pids[f"Server|{SG[213]}|{s['service']}"] = '4113'

# ------------------------------------------------------------------ metrics, dashboard, progress
listing_vendors_new = [v for v in V if not v[4].startswith('NOT LISTED') and v[9] in ('CONFIRMED', 'STRONG')]
self_claim = [v for v in V if v[9] == 'LIKELY']
not_listed = [v for v in V if v[4].startswith('NOT LISTED')] + [('VEN-013',)]
strong_inter = [r for r in rels if r['Confidence'] == 'STRONG' and 'suppl' in r['Type'].lower()]
likely_up = [r for r in rels if r['Confidence'] == 'LIKELY' and r['Target'] == 'VEN-000' and ('suppl' in r['Type'].lower() or 'intermediary' in r['Type'].lower() or 'upstream' in r['Type'].lower())]
groups_with_cand = sum(1 for k, v in GM.items() if v['upstream_confidence'] in ('CONFIRMED', 'STRONG', 'LIKELY'))
in_house = sum(1 for k, v in GM.items() if 'In-house' in v['candidate_upstream'] or 'in-house' in v.get('fulfilment_model', '').lower())
dash = [
    {'Metric': 'Service groups in public catalog', 'Rounds 1-3': '≥240 (page truncated at #239)', 'Rounds 4-6 (now)': '383 (321 Server + 62 IMEI)', 'Change / Comment': 'Full Firecrawl scrape; Dec-2022 Wayback: 385 server groups'},
    {'Metric': 'Service records (SKUs)', 'Rounds 1-3': '34 representative', 'Rounds 4-6 (now)': '1,455 SKUs (985 Server + 470 IMEI) + 34 preserved', 'Change / Comment': '+1,455'},
    {'Metric': 'Vendors officially listing HalabTech', 'Rounds 1-3': '11', 'Rounds 4-6 (now)': f'{11 + len(listing_vendors_new)} (+{len(listing_vendors_new)} new: CONFIRMED/STRONG)', 'Change / Comment': f'+{len(self_claim)} LIKELY (self-claims / unverified ownership)'},
    {'Metric': 'Vendor lists checked that OMIT HalabTech', 'Rounds 1-3': '1 (EFT, snippet)', 'Rounds 4-6 (now)': str(len(not_listed)), 'Change / Comment': 'FG, UMT/NCK, Avengers, UFI, SamKey, AMT, MH Unlocker, EFT ⇒ intermediaries likely'},
    {'Metric': 'Confirmed direct API suppliers (named)', 'Rounds 1-3': '0', 'Rounds 4-6 (now)': '0', 'Change / Comment': 'Existence of ≥3 numbered unnamed sources CONFIRMED (HalabTech\'s own labels)'},
    {'Metric': 'STRONG supply relationships', 'Rounds 1-3': '0', 'Rounds 4-6 (now)': str(len(strong_inter)), 'Change / Comment': 'Sigma via GsmServer; Chimera via GsmEasy/GsmServer; Hunter & Q-Unlocker direct; XTP direct'},
    {'Metric': 'LIKELY upstream / intermediary relationships', 'Rounds 1-3': '4 (direct-from-vendor)', 'Rounds 4-6 (now)': str(len(likely_up)), 'Change / Comment': 'Code-GSM, UnlocksPro, EFT/UMT/FG/Avengers/UFI/SamKey/AMT/MH channels, T-Tool, CellTool, Panda'},
    {'Metric': 'Catalog groups with a candidate upstream (≥ LIKELY)', 'Rounds 1-3': '~15', 'Rounds 4-6 (now)': f'{groups_with_cand} of 383', 'Change / Comment': 'Group-level mapping in "Service Groups"'},
    {'Metric': 'Groups fulfilled in-house (own product or likely)', 'Rounds 1-3': '4', 'Rounds 4-6 (now)': str(in_house), 'Change / Comment': 'Memberships, credits, Sharing Box, file requests, test services'},
    {'Metric': 'Evidence records', 'Rounds 1-3': '53', 'Rounds 4-6 (now)': str(53 + len(evidence)), 'Change / Comment': f'+{len(evidence)} (incl. negatives)'},
    {'Metric': 'MCP tool calls logged', 'Rounds 1-3': '0 (Firecrawl/Parallel/Exa not available)', 'Rounds 4-6 (now)': str(mcp_total), 'Change / Comment': '; '.join(f'{k} ×{v}' for k, v in sorted(tool_counts.items()) if k.split(' ')[0] in ('Firecrawl', 'Parallel', 'Exa')) + ' (non-MCP, not counted: 1 blocked curl, 1 local re-read of saved captures)'},
    {'Metric': 'Rounds completed', 'Rounds 1-3': '3', 'Rounds 4-6 (now)': '6', 'Change / Comment': 'R4 discovery, R5 deep investigation, R6 verification'},
    {'Metric': 'Last verification', 'Rounds 1-3': '2026-10-11', 'Rounds 4-6 (now)': DATE, 'Change / Comment': ''},
]
prog = [
    {'Area': 'Catalog coverage', 'Round 3 state': '≥240 groups, 34 records', 'Round 6 state': '383 groups, 1,455 SKUs, group-level vendor mapping', 'Change': 'Complete public catalog', 'Confidence (R6)': 'CONFIRMED'},
    {'Area': 'Platform', 'Round 3 state': 'Dhru LIKELY; Real Easy Store CONFIRMED', 'Round 6 state': 'Dhru CONFIRMED (footer)', 'Change': 'Upgraded', 'Confidence (R6)': 'CONFIRMED'},
    {'Area': 'Official vendor listings', 'Round 3 state': '11 vendors', 'Round 6 state': f'{11 + len(listing_vendors_new)} vendors', 'Change': f'+{len(listing_vendors_new)}', 'Confidence (R6)': 'CONFIRMED/STRONG'},
    {'Area': 'GsmServer upstream', 'Round 3 state': 'UNKNOWN', 'Round 6 state': 'STRONG for Sigma (exclusive distributor); STRONG-shared for Chimera; LIKELY historical "GsmServer Products"', 'Change': 'Upgraded', 'Confidence (R6)': 'STRONG'},
    {'Area': 'Chimera', 'Round 3 state': 'Listed reseller; distributor rule seen as snippet', 'Round 6 state': 'Reseller only; must buy from GsmEasy or GsmServer (full page, re-verified)', 'Change': 'Corrected + upgraded', 'Confidence (R6)': 'STRONG'},
    {'Area': 'EFT', 'Round 3 state': 'UNKNOWN', 'Round 6 state': 'HalabTech absent from full EFT list → intermediary LIKELY', 'Change': 'Upgraded', 'Confidence (R6)': 'LIKELY'},
    {'Area': 'IMEI / iCloud / Mi Account', 'Round 3 state': 'No candidate', 'Round 6 state': 'Numbered sources CONFIRMED; Code-GSM & UnlocksPro LIKELY; iRemove channel UNKNOWN', 'Change': 'Narrowed', 'Confidence (R6)': 'LIKELY / UNKNOWN'},
    {'Area': 'RapidFlashTool', 'Round 3 state': 'UNKNOWN', 'Round 6 state': 'Distributor (Worldwide)', 'Change': 'Resolved', 'Confidence (R6)': 'CONFIRMED'},
    {'Area': 'Prior leads (WARD, GSMMUNNA, DZGSM, FirmwareDrive, FirmwareWorld, Amir/Ameer)', 'Round 3 state': 'Not investigated', 'Round 6 state': 'All classified', 'Change': 'Resolved', 'Confidence (R6)': 'CONFIRMED/UNKNOWN'},
    {'Area': 'History', 'Round 3 state': 'No archive data', 'Round 6 state': '8 Wayback captures 2021-2024 analysed', 'Change': 'New', 'Confidence (R6)': 'CONFIRMED'},
    {'Area': 'Downstream network', 'Round 3 state': '15 stores', 'Round 6 state': '35+ stores + 29 world agents; HalabTech sells API access', 'Change': 'Expanded', 'Confidence (R6)': 'CONFIRMED'},
    {'Area': 'Direct API suppliers (named, proven)', 'Round 3 state': '0', 'Round 6 state': '0', 'Change': 'Unchanged – no public source names one', 'Confidence (R6)': 'UNKNOWN'},
]
tool_rows = [{'Stream': s, 'Round': ROUND[s], 'Firecrawl scrape': c.get('Firecrawl scrape', 0), 'Firecrawl search': c.get('Firecrawl search', 0),
              'Parallel search': c.get('Parallel search', 0), 'Parallel fetch': c.get('Parallel fetch', 0), 'Exa search': c.get('Exa search', 0),
              'Exa fetch': c.get('Exa fetch', 0), 'Other': sum(v for k, v in c.items() if k.split(' ')[0] not in ('Firecrawl', 'Parallel', 'Exa')),
              'Failed calls': '; '.join(f'{k} ×{v}' for k, v in fl.items()) or '0'} for s, c, fl in per_stream]
tool_rows.append({'Stream': 'TOTAL', 'Round': 'R4-6', 'Firecrawl scrape': tool_counts['Firecrawl scrape'], 'Firecrawl search': tool_counts['Firecrawl search'],
                  'Parallel search': tool_counts['Parallel search'], 'Parallel fetch': tool_counts['Parallel fetch'], 'Exa search': tool_counts['Exa search'],
                  'Exa fetch': tool_counts['Exa fetch'], 'Other': sum(v for k, v in tool_counts.items() if k.split(' ')[0] not in ('Firecrawl', 'Parallel', 'Exa')),
                  'Failed calls': '; '.join(f'{k} ×{v}' for k, v in tool_fail.items())})
tool_rows += [
    {'Stream': 'MCP smoke test', 'Round': 'R4', 'Firecrawl scrape': 'PASS (server.halabtech.com/pages/DISTRIBUTOR)', 'Parallel search': 'PASS (EFT distributor list)', 'Exa search': 'PASS (vendor pages listing HalabTech)', 'Failed calls': 'curl blocked by proxy (403) – not an MCP'},
    {'Stream': 'Notes', 'Round': '', 'Firecrawl scrape': 'Shared limit 18 req/min caused rate-limit failures; retried with Parallel/Exa', 'Parallel search': 'session_id reused on every call', 'Exa search': 'Some JS pages returned empty shells; re-scraped with Firecrawl'},
]

cur = {
    'meta': {'verification_date': DATE},
    'dashboard': dash,
    'group_map': GM, 'vendor_by_group': vendor_by_group,
    'prior_service_links': links, 'public_pids': pids, 'prior_service_updates': ps,
    'sheets': {
        'vendors': {'header': vend_hdr, 'rows': vend_rows, 'prior_updates': prior_vendor_updates, 'widths': {'Vendor': 30, 'Products': 40, 'Relationship with HalabTech': 40, 'Vendor Sales Model': 36, 'Named Distributors': 40, 'R6 Update': 50}},
        'suppliers': {'header': sup_hdr, 'rows': sup_rows, 'prior_updates': prior_sup_updates, 'widths': {'Company': 36, 'Relationship with HalabTech': 40, 'Candidate For (HalabTech groups)': 40, 'R6 Update': 50}},
        'relationships': {'header': rel_hdr, 'rows': rels, 'prior_updates': prior_rel_updates, 'widths': {'Source': 26, 'Service': 40, 'Type': 36, 'Source Name': 28, 'R6 Update': 44}},
        'evidence': {'header': ['EV ID', 'Service', 'Source URL', 'Type', 'Pub. Date', 'Excerpt (≤20 words)', 'Strength', 'S/C', 'Record Origin', 'Entity', 'Role Indicated', 'Confidence', 'Tool', 'Access', 'Access Date', 'Finding Ref', 'R6 Verification', 'Notes'],
                     'rows': evidence, 'widths': {'Source URL': 48, 'Excerpt (≤20 words)': 60, 'S/C': 40, 'Service': 30, 'Notes': 36},
                     'note': 'EV-001…052 (+EV-020b) preserved from Rounds 1-3 (access 2026-10-11). EV-053+ added in Rounds 4-6; "Finding Ref" links to the stream JSON in data/findings/.'},
        'unknown': {'header': unk_hdr, 'rows': unk_rows, 'prior_updates': prior_unk_updates, 'note': 'Ranked by importance (1 = most important). Preserved R1-3 rows carry their R6 status.'},
        'gaps': {'header': gap_hdr, 'rows': gap_rows, 'prior_updates': prior_gap_updates},
        'history': {'header': hist_hdr, 'rows': hist_rows},
        'inventory': {'header': inv_hdr, 'rows': inv_rows, 'widths': {'URL': 70}},
        'conflicts': {'header': cl_hdr, 'rows': cl_rows, 'prior_updates': prior_cl_updates},
        'plan': {'header': plan_hdr, 'rows': plan_rows, 'prior_updates': prior_plan_updates},
        'prices': {'header': price_hdr, 'rows': price_rows, 'note': 'Price parity is a lead, never proof of supply.'},
        'tool_log': {'title': 'MCP Tool Log', 'header': ['Stream', 'Round', 'Firecrawl scrape', 'Firecrawl search', 'Parallel search', 'Parallel fetch', 'Exa search', 'Exa fetch', 'Other', 'Failed calls'], 'rows': tool_rows,
                     'note': 'Counts come from each stream\'s logged calls (data/findings/*.json). Only tools actually invoked are counted.'},
        'progress': {'title': 'Progress R3 vs R6', 'header': ['Area', 'Round 3 state', 'Round 6 state', 'Change', 'Confidence (R6)'], 'rows': prog, 'widths': {'Round 3 state': 40, 'Round 6 state': 60}},
    },
    'stats': {'new_listing_vendors': len(listing_vendors_new), 'self_claim': len(self_claim), 'not_listed': len(not_listed), 'strong': len(strong_inter),
              'likely_up': len(likely_up), 'groups_with_cand': groups_with_cand, 'in_house': in_house, 'evidence_new': len(evidence), 'mcp_total': mcp_total,
              'tool_counts': dict(tool_counts), 'tool_fail': dict(tool_fail)},
}
json.dump(cur, open(OUT, 'w'), ensure_ascii=False, indent=1)
print(json.dumps(cur['stats'], ensure_ascii=False))
