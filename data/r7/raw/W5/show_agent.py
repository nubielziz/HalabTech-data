import json,sys
d=json.load(open(sys.argv[1]))
print(d['status'], d.get('stopReason'), d.get('usage'), d.get('costDollars'))
o=d['output']
print('TEXT:',o['text'][:1500])
rows=o['structured']['rows']
print('ROWS',len(rows))
for r in rows:
    print('##',r['group'],'| vendor:',r['vendor'],'| site:',r['official_site'],'| rp:',r['reseller_page_url'])
    print('   HT:',r['halabtech_listed'],'|',r['halabtech_role_wording'],'| only_dist:',r['sells_only_via_distributors'],'| api:',r['own_reseller_api_or_panel'])
    print('   dist:',r['distributors'][:300])
    print('   ev:',r['evidence_url'],'|',r['evidence_excerpt'][:300].replace('\n',' / '))
    print('   fam:',r['family_note'][:300])
