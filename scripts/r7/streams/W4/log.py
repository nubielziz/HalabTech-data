import json,sys,datetime
# usage: python3 -I log.py <tool> <input> <ok:1/0> <note>
p='/tmp/claude-0/-home-user-HalabTech-data/460d51b4-a7e0-54d7-a8d8-d39eebe19c6d/scratchpad/r7/raw/W4/tool_log.jsonl'
t,i,ok,n=sys.argv[1:5]
with open(p,'a') as f:
    f.write(json.dumps({"tool":t,"input":i,"ok":ok=='1',"note":n,"utc":datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%MZ')})+'\n')
