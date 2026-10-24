"""Saved pathway collection, snapshot ownership and legacy migration."""
import copy,sys,tempfile,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from fastapi.testclient import TestClient
from backend import main as server

class SavedPathways(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
    cls.temp=tempfile.TemporaryDirectory();cls.original=server.DB;server.DB=Path(cls.temp.name)/'paths.sqlite';cls.one=TestClient(server.app);cls.one.__enter__();cls.two=TestClient(server.app);cls.guest=TestClient(server.app)
    for client,name in [(cls.one,'one'),(cls.two,'two')]:assert client.post('/api/auth/signup',json={'email':name+'@paths.test','password':'synthetic-learning-42','name':name}).status_code==200
    cls.cat=cls.one.get('/api/catalogue').json()
 @classmethod
 def tearDownClass(cls):cls.one.__exit__(None,None,None);server.DB=cls.original;cls.temp.cleanup()
 def setUp(self):
    with server.db_connection() as c:
        for table in ['plans','saved_pathways','achievements']:c.execute('DELETE FROM '+table)
 def payload(self,goal='future'):
    return {'profile':copy.deepcopy(self.cat['personas']['mei']),'selected':'financial','month':'2026-05','scenario':'moderate','completed':[],'learningGoal':goal}
 def test_authorization_and_record_ownership(self):
    body=self.payload();self.assertEqual(self.guest.get('/api/saved-pathways').status_code,401);self.assertEqual(self.guest.post('/api/saved-pathways',json=body,headers={'x-session-mode':'demo'}).status_code,401)
    self.assertEqual(self.one.post('/api/saved-pathways',json=body,headers={'origin':'https://untrusted.example'}).status_code,403)
    record=self.one.post('/api/saved-pathways',json=body).json()['pathway'];self.assertEqual(self.two.get('/api/saved-pathways').json()['pathways'],[])
    body['savedPathId']=record['id'];self.assertEqual(self.two.post('/api/saved-pathways',json=body).status_code,404);self.assertEqual(self.two.delete('/api/saved-pathways/'+record['id']).status_code,404)
 def test_multiple_goals_and_upsert_preserve_initial_date(self):
    body=self.payload();first=self.one.post('/api/saved-pathways',json=body).json()['pathway'];body['profile']['hours']=8
    updated=self.one.post('/api/saved-pathways',json=body).json()['pathway'];self.assertEqual(updated['id'],first['id']);self.assertEqual(updated['savedAt'],first['savedAt']);self.assertEqual(updated['plan']['profile']['hours'],8)
    self.one.post('/api/saved-pathways',json=self.payload('current'));self.assertEqual(len(self.one.get('/api/saved-pathways').json()['pathways']),2)
 def test_snapshot_progress_and_badge_are_independent_of_current_recommendations(self):
    body=self.payload();record=self.one.post('/api/saved-pathways',json=body).json()['pathway'];body['savedPathId']=record['id'];body['profile']['mastery']={s['id']:1 for s in self.cat['skills']};body['profile']['hours']=9;body['completed']=[r['id'] for r in record['resources']]
    saved=self.one.post('/api/saved-pathways',json=body).json()['pathway'];self.assertEqual(saved['resources'],record['resources']);self.assertEqual(saved['plan']['profile']['mastery'],record['plan']['profile']['mastery']);self.assertEqual(saved['plan']['profile']['hours'],9)
    self.assertEqual(self.two.post('/api/achievements',json={**body,'reflection':'I reviewed original sources and checked the results.','attested':True}).status_code,404)
    result=self.one.post('/api/achievements',json={**body,'reflection':'I reviewed original sources and checked the results.','attested':True});self.assertEqual(result.status_code,200);self.assertEqual(result.json()['achievement']['pathKey'],record['pathKey'])
    self.assertEqual(self.one.delete('/api/saved-pathways/'+record['id']).status_code,200);self.assertEqual(len(self.one.get('/api/achievements').json()['achievements']),1)
 def test_invalid_empty_plans_and_resources_rejected(self):
    body=self.payload();body['profile']['mastery']={s['id']:1 for s in self.cat['skills']};self.assertEqual(self.one.post('/api/saved-pathways',json=body).status_code,422)
    body=self.payload();body['resources']=[];self.assertEqual(self.one.post('/api/saved-pathways',json=body).status_code,422)
    body=self.payload();body['completed']=['invented'];self.assertEqual(self.one.post('/api/saved-pathways',json=body).status_code,422)
 def test_old_single_plan_migrates_once_without_resurrection_after_remove(self):
    self.one.put('/api/plan',json=self.payload())
    with server.db_connection() as c:c.execute('DROP TABLE saved_pathways')
    server.init_db();records=self.one.get('/api/saved-pathways').json()['pathways'];self.assertEqual(len(records),1)
    self.one.delete('/api/saved-pathways/'+records[0]['id']);server.init_db();self.assertEqual(self.one.get('/api/saved-pathways').json()['pathways'],[]);self.assertEqual(self.one.get('/api/plan').status_code,200)

if __name__=='__main__':unittest.main(verbosity=2)
