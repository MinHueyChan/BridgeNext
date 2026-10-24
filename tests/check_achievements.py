"""Synthetic self-reported milestones: authorization, completeness and history isolation."""
import copy,sys,tempfile,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from fastapi.testclient import TestClient
from backend import main as server
from backend.achievements import resources_for

class Achievements(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
    cls.temp=tempfile.TemporaryDirectory();cls.original=server.DB;server.DB=Path(cls.temp.name)/'test.sqlite'
    cls.one=TestClient(server.app);cls.one.__enter__();cls.two=TestClient(server.app);cls.guest=TestClient(server.app)
    for client,name in [(cls.one,'one'),(cls.two,'two')]:
        response=client.post('/api/auth/signup',json={'email':name+'@achievements.test','password':'synthetic-learning-42','name':name})
        assert response.status_code==200
    cls.cat=cls.one.get('/api/catalogue').json()
 @classmethod
 def tearDownClass(cls):
    cls.one.__exit__(None,None,None);server.DB=cls.original;cls.temp.cleanup()
 def setUp(self):
    with server.db_connection() as c:c.execute('DELETE FROM achievements');c.execute('DELETE FROM plans')
 def payload(self,goal='future',selected='financial'):
    profile=copy.deepcopy(self.cat['personas']['mei'])
    resources=resources_for(self.cat,profile,selected,'2026-05','moderate',goal)
    return {'profile':profile,'selected':selected,'month':'2026-05','scenario':'moderate','learningGoal':goal,'completed':[r['id'] for r in resources],'reflection':'I practised checking sources before trusting an AI report.','attested':True}
 def test_protected_and_origin_checked(self):
    self.assertEqual(self.guest.get('/api/achievements').status_code,401)
    self.assertEqual(self.guest.post('/api/achievements',json=self.payload(),headers={'x-session-mode':'demo'}).status_code,401)
    self.assertEqual(self.one.post('/api/achievements',json=self.payload(),headers={'origin':'https://untrusted.example'}).status_code,403)
 def test_record_snapshot_isolated_and_deduplicated(self):
    payload=self.payload();response=self.one.post('/api/achievements',json=payload);self.assertEqual(response.status_code,200)
    record=response.json()['achievement'];self.assertTrue(record['selfReported']);self.assertEqual(record['resourceIds'],payload['completed']);self.assertTrue(record['resources']);self.assertEqual(record['estimatedHours'],sum(r['hours'] for r in record['resources']))
    payload['reflection']='A different reflection must not duplicate the same milestone.'
    again=self.one.post('/api/achievements',json=payload).json();self.assertEqual(again['status'],'already_recorded');self.assertEqual(again['achievement'],record)
    self.assertEqual(len(self.one.get('/api/achievements').json()['achievements']),1);self.assertEqual(self.two.get('/api/achievements').json()['achievements'],[])
    self.assertEqual(self.two.post('/api/achievements',json=payload).status_code,200)
 def test_incomplete_empty_and_invalid_claims_rejected(self):
    for update in [{'completed':[]},{'reflection':' ' * 15},{'attested':False},{'completed':['invented']},{'estimatedHours':999}]:
        payload=self.payload();payload.update(update);self.assertEqual(self.one.post('/api/achievements',json=payload).status_code,422)
    payload=self.payload();payload['profile']['mastery']={s['id']:1 for s in self.cat['skills']};self.assertEqual(self.one.post('/api/achievements',json=payload).status_code,422)
 def test_history_survives_plan_change_and_goals_are_distinct(self):
    first=self.one.post('/api/achievements',json=self.payload()).json()['achievement']
    current=self.one.post('/api/achievements',json=self.payload('current'));self.assertEqual(current.status_code,200)
    new_plan=self.payload(selected='bi');new_plan.pop('reflection');new_plan.pop('attested');self.assertEqual(self.one.put('/api/plan',json=new_plan).status_code,200)
    rows=self.one.get('/api/achievements').json()['achievements'];self.assertEqual(len(rows),2);self.assertIn(first,rows)
    with server.db_connection() as c:c.execute('DELETE FROM plans')
    self.assertEqual(len(self.one.get('/api/achievements').json()['achievements']),2)

if __name__=='__main__':unittest.main(verbosity=2)
