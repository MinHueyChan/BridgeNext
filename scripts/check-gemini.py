"""Run in Replit Shell after enabling Gemini; --live makes two billable calls."""
import argparse,asyncio,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from backend import gemini,explanations
parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--live',action='store_true');args=parser.parse_args()
info=gemini.status();print(json.dumps(info));
if not args.live:
 print('Configuration presence only. Run python scripts/check-gemini.py --live to verify two synthetic requests.');sys.exit(0)
if not info['configured']:
 print('Gemini is not configured. Enable the Google Gemini Replit AI Integration; no key should be pasted into this script.');sys.exit(2)
async def check():
 cat=json.loads((Path(__file__).resolve().parents[1]/'data/catalogue.json').read_text())
 p={'name':'Synthetic check','title':'','experience':'','hours':4,'interests':['finance'],'tasks':['spreadsheets'],'mastery':{'excel':.6},'confirmed':True}
 extracted=await explanations.extract_skills(cat,'I use Excel spreadsheets to check financial records.')
 explained=await explanations.explain(cat,p,'financial',cat['evidence']['months'][-1],'moderate','future','en')
 print(json.dumps({'extraction_mode':extracted['mode'],'extraction_reason':extracted.get('reason'),'skill_ids':extracted['skill_ids'],'explanation_mode':explained['mode'],'explanation_reason':explained.get('reason'),'score_from_rules':explained['facts']['score'],'source_release':explained['facts']['release']}))
 return extracted['mode']=='gemini' and bool(extracted['skill_ids']) and explained['mode']=='gemini'
sys.exit(0 if asyncio.run(check()) else 1)
