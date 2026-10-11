"""Emit the Round-6 supply-chain graph as Mermaid (.mmd) and PNG.

Usage: python3 graph.py <out_dir>
Edge confidence → style: CONFIRMED solid, STRONG thick, LIKELY dashed, UNKNOWN dotted grey.
"""
import sys, os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib.lines import Line2D

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)

# id: (label, column, row, kind)
N = {
    'SIG': ('Sigma / Sigma Plus\n(VEN-020)', 0, 9.0, 'vendor'),
    'CHI': ('ChimeraTool\n(VEN-002)', 0, 7.6, 'vendor'),
    'OMIT': ('8 vendors OMIT HalabTech\nFurious Gold · UMT/NCK · Avengers · UFI\nSamKey · AMT · MH Unlocker · EFT', 0, 5.9, 'vendor'),
    'SOLE': ('Sole-distributor vendors\nT-Tool Pro · CellTool · Panda', 0, 4.5, 'vendor'),
    'HQ': ('Hunter Unlocker · Q-Unlocker\n(distributors-only)  ·  XTP', 0, 3.3, 'vendor'),
    'LIST': ('62 vendors LIST HalabTech\nDFT · Octoplus · Hydra · Z3X · Infinity #7\nDC-Unlocker · TSM · UAT · RapidFlash · Ameer …', 0, 1.9, 'vendor'),
    'IRM': ('iRemove (iCloud FMI OFF)\n(VEN-079)', 0, 0.6, 'vendor'),
    'GSV': ('GsmServer\n(SUP-001)', 1, 9.0, 'inter'),
    'GEZ': ('GsmEasy\n(SUP-012)', 1, 7.6, 'inter'),
    'UEU': ('Unlock.eu\n(SUP-013)', 1, 6.7, 'inter'),
    'POOL': ('Distributor pool\nGsmServer · GsmEasy · Martview · Fast Unlocking\nSimSim · SharkGSM · GSM-Sources · ADY · Easy-Firmware', 1, 5.4, 'inter'),
    'SOLED': ('GSM T-Tool · Smart Tool WW · ADY', 1, 4.3, 'inter'),
    'CODE': ('Code-GSM\n(SUP-014)', 1, 2.9, 'imei'),
    'UPRO': ('UnlocksPro\n(SUP-015)', 1, 1.9, 'imei'),
    'SRC': ('Unnamed IMEI sources\nSource #1 / #2 / #3\n"Server Direct"', 1, 0.8, 'imei'),
    'DHRU': ('Dhru Fusion (platform)\njoudiSoft Real Easy Store', 2, 9.4, 'platform'),
    'HT': ('HalabTech\nserver / support / news\n383 groups · 1,455 SKUs', 2, 5.0, 'hub'),
    'DOWN': ('35+ downstream stores\n(API clients / resellers)', 3, 7.0, 'down'),
    'AG': ('29 World Agents', 3, 5.6, 'down'),
    'GSVD': ('GsmServer (resells HalabTech\nsince 14.10.2022)', 3, 4.2, 'down'),
    'CHID': ('ChimeraTool\n"HalabTech Add-On" content', 3, 2.8, 'down'),
}
# (src, dst, label, confidence)
E = [
    ('SIG', 'GSV', 'exclusive distributor', 'CONFIRMED'),
    ('CHI', 'GSV', 'contracted distributor', 'CONFIRMED'),
    ('CHI', 'GEZ', 'contracted distributor', 'CONFIRMED'),
    ('CHI', 'UEU', '3rd "Distributor" card', 'UNKNOWN'),
    ('OMIT', 'POOL', 'named distributors', 'CONFIRMED'),
    ('SOLE', 'SOLED', 'sole distributor', 'CONFIRMED'),
    ('GSV', 'HT', 'Sigma credits (vendor rule)', 'STRONG'),
    ('GEZ', 'HT', 'Chimera: GsmEasy OR GsmServer', 'STRONG'),
    ('GSV', 'HT', '"GsmServer Products" 2022-24', 'LIKELY'),
    ('UEU', 'HT', 'Chimera alt.', 'UNKNOWN'),
    ('POOL', 'HT', 'identity unknown', 'LIKELY'),
    ('SOLED', 'HT', 'or direct', 'LIKELY'),
    ('HQ', 'HT', 'direct (vendor rule / main seller)', 'STRONG'),
    ('LIST', 'HT', 'authorised channel (status only)', 'CONFIRMED'),
    ('IRM', 'HT', 'channel unknown', 'UNKNOWN'),
    ('CODE', 'HT', 'T-Mobile Clean & Paid Off', 'LIKELY'),
    ('UPRO', 'HT', '36 identical IMEI items', 'LIKELY'),
    ('SRC', 'HT', 'existence confirmed, names hidden', 'CONFIRMED'),
    ('DHRU', 'HT', 'platform', 'CONFIRMED'),
    ('HT', 'DOWN', 'resale / API', 'CONFIRMED'),
    ('HT', 'AG', 'agents', 'CONFIRMED'),
    ('HT', 'GSVD', 'downstream resale', 'CONFIRMED'),
    ('HT', 'CHID', 'content supply', 'CONFIRMED'),
]

# ------------------------------------------------------------------ Mermaid
arrow = {'CONFIRMED': '-->', 'STRONG': '==>', 'LIKELY': '-.->', 'UNKNOWN': '-.->'}
color = {'CONFIRMED': '#2e7d32', 'STRONG': '#1565c0', 'LIKELY': '#ef6c00', 'UNKNOWN': '#9e9e9e'}
lines = ['%% HalabTech supply chain - Rounds 1-6 (verified 2026-10-11)',
         '%% solid = CONFIRMED, thick = STRONG, dashed orange = LIKELY, dashed grey = UNKNOWN',
         'graph LR']
for k, (lab, *_rest) in N.items():
    shape = ('((', '))') if k == 'HT' else ('[', ']')
    lines.append(f'  {k}{shape[0]}"{lab.replace(chr(10), "<br/>")}"{shape[1]}')
for i, (s, d, lab, c) in enumerate(E):
    lines.append(f'  {s} {arrow[c]}|"{lab} ({c})"| {d}')
for i, (s, d, lab, c) in enumerate(E):
    w = '3px' if c == 'STRONG' else '1.5px'
    lines.append(f'  linkStyle {i} stroke:{color[c]},stroke-width:{w}')
lines += ['  classDef vendor fill:#fff8e1,stroke:#8d6e63', '  classDef inter fill:#e3f2fd,stroke:#1565c0',
          '  classDef imei fill:#fce4ec,stroke:#ad1457', '  classDef down fill:#e8f5e9,stroke:#2e7d32',
          '  classDef hub fill:#263238,color:#ffffff,stroke:#000', '  classDef platform fill:#ede7f6,stroke:#5e35b1']
for kind in ('vendor', 'inter', 'imei', 'down', 'hub', 'platform'):
    ids = [k for k, v in N.items() if v[3] == kind]
    lines.append(f'  class {",".join(ids)} {kind}')
mmd = '\n'.join(lines) + '\n'
open(os.path.join(OUT, 'supply_chain_graph_R6.mmd'), 'w').write(mmd)

# ------------------------------------------------------------------ PNG
FILL = {'vendor': '#fff8e1', 'inter': '#e3f2fd', 'imei': '#fce4ec', 'down': '#e8f5e9', 'hub': '#263238', 'platform': '#ede7f6'}
EDGE = {'vendor': '#8d6e63', 'inter': '#1565c0', 'imei': '#ad1457', 'down': '#2e7d32', 'hub': '#000000', 'platform': '#5e35b1'}
# explicit layout: id -> (x, y, w, h)
POS = {
    'SIG': (1.6, 9.3, 3.0, 0.8), 'CHI': (1.6, 8.0, 3.0, 0.8), 'OMIT': (1.6, 6.6, 3.2, 1.0), 'SOLE': (1.6, 5.3, 3.0, 0.8),
    'HQ': (1.6, 3.85, 3.0, 0.8), 'LIST': (1.6, 2.6, 3.2, 1.0), 'IRM': (1.6, 1.1, 3.0, 0.8),
    'GSV': (6.3, 9.3, 2.6, 0.75), 'GEZ': (6.3, 8.25, 2.6, 0.75), 'UEU': (6.3, 7.4, 2.6, 0.6), 'POOL': (6.3, 6.35, 3.6, 1.0), 'SOLED': (6.3, 5.42, 2.9, 0.5),
    'DHRU': (10.6, 9.4, 2.8, 0.75), 'HT': (10.6, 5.6, 2.8, 1.5),
    'CODE': (8.75, 2.3, 1.55, 0.8), 'UPRO': (10.6, 2.3, 1.55, 0.8), 'SRC': (12.5, 2.3, 1.85, 0.95),
    'DOWN': (15.0, 8.0, 2.6, 0.8), 'AG': (15.0, 6.7, 2.6, 0.6), 'GSVD': (15.0, 5.4, 2.6, 0.8), 'CHID': (15.0, 4.0, 2.6, 0.8),
}
fig, ax = plt.subplots(figsize=(19, 11.5), dpi=130)
ax.set_xlim(-0.2, 16.6); ax.set_ylim(0.0, 10.4); ax.axis('off')
for k, (lab, col, row, kind) in N.items():
    x, y, w, h = POS[k]
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle='round,pad=0.04,rounding_size=0.12', fc=FILL[kind], ec=EDGE[kind], lw=1.4, zorder=3))
    ax.text(x, y, lab, ha='center', va='center', fontsize=8.4 if k != 'HT' else 10.5, color='white' if kind == 'hub' else '#212121',
            fontweight='bold' if k == 'HT' else 'normal', zorder=4)
LS = {'CONFIRMED': ('-', 1.6), 'STRONG': ('-', 3.4), 'LIKELY': ('--', 1.7), 'UNKNOWN': (':', 1.8)}
into_ht = [e for e in E if e[1] == 'HT' and POS[e[0]][0] < POS['HT'][0] - 1]
slot = {e[:2] + (e[2],): i for i, e in enumerate(sorted(into_ht, key=lambda e: -POS[e[0]][1]))}
for s, d, lab, c in E:
    sx, sy, sw, sh = POS[s]; dx, dy, dw, dh = POS[d]
    rad = 0.0
    if abs(sx - dx) < 0.5 or (d == 'HT' and sy < dy - dh / 2 and abs(sx - dx) < 2.5):      # vertical (IMEI row / platform)
        if sy < dy:
            start, end = (sx, sy + sh / 2), (min(max(sx, dx - dw / 2 + 0.3), dx + dw / 2 - 0.3), dy - dh / 2)
        else:
            start, end = (sx, sy - sh / 2), (dx, dy + dh / 2)
        t = 0.5
    else:
        start = (sx + sw / 2, sy) if dx > sx else (sx - sw / 2, sy)
        if d == 'HT':
            i = slot[(s, d, lab)]
            end = (dx - dw / 2, dy + dh / 2 - 0.12 - i * (dh - 0.24) / max(1, len(slot) - 1))
            t = 0.3 if sx < 4 else 0.45
        elif s == 'HT':
            start = (sx + sw / 2, sy + (dy - sy) * 0.15)
            end = (dx - dw / 2, dy)
            t = 0.55
        else:
            end = (dx - dw / 2, dy)
            t = 0.5
        if (s, d) == ('GSV', 'HT') and c == 'LIKELY':
            rad = -0.25
    ls, lw = LS[c]
    ax.add_patch(FancyArrowPatch(start, end, arrowstyle='-|>', mutation_scale=12, lw=lw, ls=ls, color=color[c],
                                 connectionstyle=f'arc3,rad={rad}', zorder=2, shrinkA=2, shrinkB=2))
    mx, my = start[0] + (end[0] - start[0]) * t, start[1] + (end[1] - start[1]) * t + 0.13
    if rad:
        mx, my = mx + 0.35, my + 0.35
    ax.text(mx, my, lab, fontsize=6.9, ha='center', va='center', color=color[c],
            bbox=dict(fc='white', ec='none', alpha=0.9, pad=0.3), zorder=5)
for x, title in ((1.6, 'Original vendors'), (6.3, 'Intermediaries / distributors'), (10.6, 'HalabTech'), (15.0, 'Downstream')):
    ax.text(x, 10.2, title, ha='center', fontsize=11, fontweight='bold', color='#37474f')
ax.text(10.6, 1.55, 'IMEI / iCloud / MDM sources', ha='center', fontsize=9.5, fontweight='bold', color='#ad1457')
handles = [Line2D([0], [0], color=color[c], lw=LS[c][1], ls=LS[c][0], label=c) for c in ('CONFIRMED', 'STRONG', 'LIKELY', 'UNKNOWN')]
ax.legend(handles=handles, loc='lower right', fontsize=9, title='Relationship confidence', frameon=True)
ax.text(0, 0.15, 'HalabTech supply chain after Round 6 (2026-10-11). Vendor→HalabTech "authorised channel" edges prove sales status only, not an API connection. '
        'No named direct API supplier is proven; IMEI sources are hidden behind numbers.', fontsize=8, color='#455a64')
plt.tight_layout()
fig.savefig(os.path.join(OUT, 'supply_chain_graph_R6.png'), bbox_inches='tight')
print('wrote', OUT)
