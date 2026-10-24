"""Synthetic CSV fixtures test future-release handling; they are never application evidence."""
import copy,csv,io,json,sys,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from backend import signals
from backend import main as server
from fastapi.testclient import TestClient
CAT=json.loads((Path(__file__).resolve().parents[1]/'data/catalogue.json').read_text())
SHA='a'*40

def fixture():
    rows=[]
    for task in CAT['tasks']:
        for month in ['2026-07','2026-08']:
            for metric,value in [('collaboration_bucket_automation_pct',60),('collaboration_bucket_augmentation_pct',40),('pct',.1)]:
                rows.append(dict(date_start=month+'-01',date_end='2026-08-01' if month=='2026-07' else '2026-09-01',geo_id='GLOBAL',geo_level='global',category_name='onet',hierarchy_level='0',metric_id=metric,value=str(value),node_external_id=task['node_id'],node_name=task['source_task']))
    return rows

def parse(rows):
    stream=io.StringIO();writer=csv.DictWriter(stream,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows);stream.seek(0)
    return signals.parse_stream(stream,CAT,'2026-09-30','https://huggingface.co/datasets/Anthropic/EconomicIndex/resolve/'+SHA+'/fixture.csv',SHA)

class SignalChecks(unittest.TestCase):
 def test_compatible_new_periods_keep_old_history(self):
    updated,changes=parse(fixture());self.assertEqual(updated['evidence']['months'],['2026-04','2026-05','2026-07','2026-08']);self.assertTrue(changes)
    self.assertEqual(updated['tasks'][0]['observations']['2026-05'],CAT['tasks'][0]['observations']['2026-05'])
    self.assertEqual(updated['evidence']['period_sources']['2026-04']['release'],'2026-06-26')
    self.assertEqual(updated['evidence']['period_sources']['2026-08']['release'],'2026-09-30')
 def test_nan_range_duplicate_and_period_rejected(self):
    for value in ['nan','inf','101','-1']:
        rows=fixture();rows[0]['value']=value
        with self.assertRaises(ValueError):parse(rows)
    rows=fixture();rows.append(rows[0])
    with self.assertRaises(ValueError):parse(rows)
    rows=fixture();rows[0]['date_end']='2026-10-01'
    with self.assertRaises(ValueError):parse(rows)
 def test_schema_coverage_and_incomplete_metrics_rejected(self):
    with self.assertRaises(ValueError):signals.parse_stream(io.StringIO('wrong,schema\n1,2'),CAT,'2026-09-30','test',SHA)
    rows=fixture()
    with self.assertRaises(ValueError):parse(rows[:6])
    with self.assertRaises(ValueError):parse([r for r in rows if r['metric_id']!='collaboration_bucket_augmentation_pct'])
 def test_discovery_selects_new_compatible_release(self):
    updated,changes=parse(fixture());release='2026-09-30';path='release_2026_09_30/data/aei_claude_ai_2026-09-30.csv'
    with patch.object(signals,'discover',return_value=(SHA,{release:[path]})),patch.object(signals,'download',return_value=(updated,changes)):
        result,report=signals.refresh_catalogue(CAT)
    self.assertEqual(report['status'],'updated');self.assertEqual(result['evidence']['release'],release)
 def test_incompatible_release_retains_last_valid_catalogue(self):
    with patch.object(signals,'discover',return_value=(SHA,{'2026-09-30':['unknown.csv']})):
        result,report=signals.refresh_catalogue(CAT)
    self.assertEqual(result,CAT);self.assertEqual(report['status'],'review_required');self.assertTrue(report['review_required'])
 def test_unchanged_does_not_claim_new_data(self):
    path='release_2026_06_26/data/aei_claude_ai_2026-06-26.csv'
    with patch.object(signals,'discover',return_value=(SHA,{'2026-06-26':[path]})),patch.object(signals,'download',return_value=(copy.deepcopy(CAT),[])):
        _,report=signals.refresh_catalogue(CAT)
    self.assertEqual(report['status'],'unchanged');self.assertEqual(report['changes'],[])
 def test_api_new_month_matching_save_history_and_failure_retention(self):
    with tempfile.TemporaryDirectory() as temp:
        original=server.DB;server.DB=Path(temp)/'signals.sqlite'
        try:
            with TestClient(server.app) as client:
                updated,changes=parse(fixture());report={'status':'updated','checked_at':signals.now(),'active_release':'2026-09-30','changes':changes,'review_required':[]}
                server.last_refresh=0
                with patch.object(signals,'refresh_catalogue',return_value=(updated,report)):
                    self.assertEqual(client.post('/api/evidence/refresh').status_code,200)
                self.assertEqual(client.get('/api/evidence/status').json()['history'][0]['status'],'updated')
                profile=CAT['personas']['mei'];self.assertEqual(client.post('/api/matches',json={'profile':profile,'month':'2026-08','scenario':'moderate'}).status_code,200)
                client.post('/api/auth/signup',json={'email':'signal@example.test','password':'synthetic-signal-pass','name':'Signal Test'})
                payload={'profile':profile,'selected':'financial','month':'2026-08','scenario':'moderate','completed':[],'learningGoal':'current'}
                self.assertEqual(client.put('/api/plan',json=payload).status_code,200);self.assertEqual(client.get('/api/plan').json()['learningGoal'],'current')
                payload['learningGoal']='invented';self.assertEqual(client.put('/api/plan',json=payload).status_code,422)
                server.last_refresh=0
                with patch.object(signals,'refresh_catalogue',side_effect=ValueError('Synthetic failure')):
                    self.assertEqual(client.post('/api/evidence/refresh').status_code,502)
                self.assertEqual(client.get('/api/catalogue').json(),updated);self.assertEqual(client.get('/api/evidence/status').json()['history'][0]['status'],'failed')
        finally:server.DB=original;server.last_refresh=0

if __name__=='__main__':unittest.main(verbosity=2)
