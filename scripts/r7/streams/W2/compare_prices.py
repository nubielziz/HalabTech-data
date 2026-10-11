import json, re, sys
cat = json.load(open(sys.argv[1]))
cg = json.load(open(sys.argv[2]))
out = {}
# iPad FMI OFF: HalabTech vs GsmUnlockingStore (Exa capture 2026-10-11 ~10:40Z) vs iRemove public (from B-13 notes)
gus_ipad = {'iPad11,6':61.5,'iPad11,3':71.5,'iPad11,1':61.5,'iPad8,1':76.5,'iPad8,2':76.5,'iPad8,5':86.5,'iPad8,6':86.5,'iPad8,9':86.5,'iPad8,11':91.5,'iPad12,1':91.5,'iPad13,1':101.5,'iPad13,18':101.5,'iPad14,1':96.5,'iPad13,4':115,'iPad13,8':101.5,'iPad13,16':106.5,'iPad14,3':116.5,'iPad14,5':111.5,'iPad14,8':116.5,'iPad14,10':130,'iPad15,3':126.5,'iPad15,5':106.5,'iPad15,7':135,'iPad16,1':135,'iPad16,3':151.5,'iPad16,5':151.5,'iPad16,8':151.5,'iPad16,10':161.5,'iPad17,1':230,'iPad17,3':241.5}
iremove_pub = {'iPad13,18':100,'iPad12,1':95,'iPad8,1':80,'iPad14,3':115,'iPad15,7':110,'iPad16,5':170}
rows=[]
for s in cat['services']:
    if s['group']=='iPads WIFI Only (iCloud Remove)':
        m = re.search(r'\[(iPad[0-9]+,[0-9]+)\]', s['service']) or re.search(r'(iPad[0-9]+,[0-9]+)', s['service'])
        if not m: continue
        k = m.group(1)
        g = gus_ipad.get(k)
        rows.append({'model':k,'ht':s['price_usd'],'gus':g,'ht_minus_gus':(round(s['price_usd']-g,2) if g else None),'iremove_public':iremove_pub.get(k)})
out['ipad_fmi'] = rows
# Mi Account: HalabTech vs Code-GSM (Exa capture)
def norm(n):
    n = n.lower()
    n = re.sub(r'source2 #cheaper|server direct|direct source|working 100%|\(rocket super fast\)', lambda m: m.group(0), n)
    n = re.sub(r'[^a-z0-9{}]+',' ', n).strip()
    return n
cgmap = {}
for p in cg:
    if 'mi account' in p['name'].lower():
        cgmap[norm(p['name'])] = p['price']
mi=[]
for s in cat['services']:
    if s['group']=='Xiaomi Mi Account':
        n = norm(s['service'])
        best=None
        for k,v in cgmap.items():
            if k==n or k.startswith(n[:60]) or n.startswith(k[:60]):
                best=(k,v); break
        mi.append({'ht_name':s['service'][:90],'ht':s['price_usd'],'cg':(best[1] if best else None)})
out['mi_account']=mi
matched=[r for r in mi if r['cg'] is not None]
out['mi_summary']={'ht_skus':len(mi),'matched':len(matched),'ht_gt_cg':sum(1 for r in matched if r['ht']>r['cg']),'ht_lt_cg':sum(1 for r in matched if r['ht']<r['cg']),'ht_eq_cg':sum(1 for r in matched if r['ht']==r['cg'])}
json.dump(out, open(sys.argv[3],'w'), ensure_ascii=False, indent=1)
print(json.dumps(out['mi_summary']))
for r in rows: print(r)
