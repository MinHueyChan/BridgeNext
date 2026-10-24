"""Import a small, traceable subset; no observed value is invented."""
import csv,io,json,urllib.request,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
URL='https://huggingface.co/datasets/Anthropic/EconomicIndex/resolve/main/release_2026_06_26/data/aei_claude_ai_2026-06-26.csv'
METRICS={'collaboration_bucket_automation_pct','collaboration_bucket_augmentation_pct','pct'}
WORDS=('invoice','reconcil','financial','accounting','spreadsheet','payroll','payment','compliance','budget','data analysis','financial report')
def fetch():
 rows=[];size=0;started=time.time()
 with urllib.request.urlopen(URL,timeout=45) as r:
  reader=csv.DictReader(io.TextIOWrapper(r,encoding='utf-8-sig'))
  for n,row in enumerate(reader):
   if n==0:print('Source columns:',','.join(row),flush=True)
   if row.get('geo_id')!='GLOBAL' or row.get('category_name')!='onet' or row.get('hierarchy_level')!='0':continue
   if row.get('metric_id') not in METRICS:continue
   if any(w in row.get('node_name','').lower() for w in WORDS):rows.append(row)
   if time.time()-started>150:raise TimeoutError('Import exceeded 150 seconds; keep prior snapshot')
 out={'source_url':URL,'release':'2026-06-26','retrieved_at':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'source_kind':'claude_ai','rows':rows}
 (ROOT/'data/aei_subset.json').write_text(json.dumps(out,indent=2))
 print('Saved',len(rows),'source rows in',round(time.time()-started,1),'seconds',flush=True)
 for name in list(dict.fromkeys(x['node_name'] for x in rows))[:35]:print(name,flush=True)
 return out
if __name__=='__main__':fetch()
