"""Contract and failure tests for the working prototype, using synthetic profiles."""
import copy,json,sqlite3,sys,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from fastapi.testclient import TestClient
import backend.main as server
from backend.engine import calculate

class BackendContract(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.tmp=tempfile.TemporaryDirectory();server.DB=Path(cls.tmp.name)/'test.sqlite';cls.client=TestClient(server.app);cls.client.__enter__();cls.cat=cls.client.get('/api/catalogue').json()
 @classmethod
 def tearDownClass(cls):cls.client.__exit__(None,None,None);cls.tmp.cleanup()
 def request(self,p=None,month='2026-05',scenario='moderate'):
  return self.client.post('/api/matches',json={'profile':p or self.cat['personas']['mei'],'month':month,'scenario':scenario})
 def test_service_and_storage(self):
  self.assertIn('explicitly saved',self.client.get('/api/health').json()['stores_profiles'])
  with server.db_connection() as c:
   self.assertEqual(c.execute('SELECT count(*) FROM source_observations').fetchone()[0],12)
   self.assertEqual({r[0] for r in c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")},{'catalogue','source_observations','users','sessions','plans','evidence_updates','achievements','saved_pathways'})
 def test_account_isolation_and_logout(self):
  one=TestClient(server.app);two=TestClient(server.app)
  self.assertEqual(one.get('/api/plan').status_code,401)
  self.assertEqual(one.post('/api/auth/signup',json={'email':'one@example.test','password':'synthetic-pass-42','name':'Synthetic One'}).status_code,200)
  self.assertEqual(two.post('/api/auth/signup',json={'email':'two@example.test','password':'synthetic-pass-43','name':'Synthetic Two'}).status_code,200)
  payload={'profile':self.cat['personas']['mei'],'selected':'financial','scenario':'moderate','month':'2026-05','completed':[]}
  self.assertEqual(one.put('/api/plan',json=payload).status_code,200)
  self.assertEqual(one.get('/api/plan').json()['profile']['name'],'Mei')
  self.assertEqual(two.get('/api/plan').status_code,404)
  self.assertEqual(one.put('/api/plan',json=payload,headers={'origin':'https://untrusted.example'}).status_code,403)
  with server.db_connection() as c:
   self.assertNotIn('synthetic-pass-42',str(c.execute('SELECT * FROM users').fetchall()))
   self.assertEqual(len(c.execute('SELECT token_hash FROM sessions').fetchone()[0]),64)
  cookie=one.cookies.get('bn_session')
  self.assertEqual(one.post('/api/auth/logout').status_code,200)
  self.assertEqual(one.get('/api/plan').status_code,401)
  one.cookies.set('bn_session',cookie)
  self.assertEqual(one.get('/api/plan').status_code,401)
 def test_avatar_contract_and_legacy_migration(self):
  p=copy.deepcopy(self.cat['personas']['mei'])
  self.assertEqual(server.Profile.model_validate(p).avatarId,1)
  p['title']='Procurement assistant'
  self.assertEqual(server.Profile.model_validate(p).avatarId,0)
  for avatar in range(6):
   p['avatarId']=avatar
   self.assertEqual(self.request(p).status_code,200)
  p['title']='Accountant';p['avatarId']=0
  self.assertEqual(server.Profile.model_validate(p).avatarId,0)
  for avatar in [-1,6,1.5,'1',True]:
   p['avatarId']=avatar
   self.assertEqual(self.request(p).status_code,422)
 def test_avatar_account_roundtrip_and_demo_not_authorized(self):
  client=TestClient(server.app)
  p={**self.cat['personas']['aaron'],'title':'Custom occupation','avatarId':0}
  payload={'profile':p,'selected':'financial','scenario':'moderate','month':'2026-05','completed':[]}
  self.assertEqual(client.put('/api/plan',json=payload,headers={'x-session-mode':'demo'}).status_code,401)
  self.assertEqual(client.post('/api/auth/signup',json={'email':'avatar@example.test','password':'synthetic-pass-avatar','name':'Avatar Test'}).status_code,200)
  self.assertEqual(client.put('/api/plan',json=payload).status_code,200)
  self.assertEqual(client.get('/api/plan').json()['profile']['avatarId'],0)
  p['avatarId']=6
  self.assertEqual(client.put('/api/plan',json=payload).status_code,422)
  # Simulate a plan stored before the avatar field existed.
  p.pop('avatarId');p['title']='Administrative assistant'
  with server.db_connection() as c:c.execute('UPDATE plans SET payload=? WHERE user_id=(SELECT id FROM users WHERE email=?)',(json.dumps(payload),'avatar@example.test'))
  self.assertEqual(client.get('/api/plan').json()['profile']['avatarId'],3)
 def test_formula_and_scenario_bounds(self):
  result=self.request().json()['matches']
  for r in result:self.assertAlmostEqual(r['score'],.7*r['baseline']+.2*r['interest']+.1*r['trend'],delta=.11)
  for sc in ['moderate','fast']:
   p=copy.deepcopy(self.cat['personas']['mei']);p['mastery']={k:1 for k in p['mastery']};p['interests']=['finance','data','analysis','people','sustainability']
   for r in self.request(p,scenario=sc).json()['matches']:self.assertAlmostEqual(r['score'],100,delta=.11)
 def test_real_observations(self):
  ts={t['id']:t for t in self.cat['tasks']}
  self.assertIsNone(ts['invoices']['observations']['2026-04']['automation'])
  self.assertEqual(ts['reconcile']['observations']['2026-05']['automation'],59.83)
 def test_end_to_end_matching(self):
  mei=self.request().json()['matches'];aaron=self.request(self.cat['personas']['aaron']).json()['matches']
  self.assertEqual(mei[0]['role']['id'],'financial')
  self.assertNotEqual([r['score'] for r in mei],[r['score'] for r in aaron])
  for r in mei:self.assertTrue(0<=r['score']<=100);self.assertAlmostEqual(sum(r['weights'].values()),1)
 def test_evidence_and_scenario_are_inputs(self):
  def scores(**kw):return {r['role']['id']:r['score'] for r in self.request(**kw).json()['matches']}
  self.assertNotEqual(scores(),scores(month='2026-04'))
  self.assertNotEqual(scores(),scores(scenario='fast'))
 def test_invalid_inputs_rejected(self):
  for changes in [{'hours':0},{'mastery':{'invented':1}},{'mastery':{'excel':1.1}},{'tasks':['unknown']},{'confirmed':False}]:
   p=copy.deepcopy(self.cat['personas']['mei']);p.update(changes);self.assertEqual(self.request(p).status_code,422)
  self.assertEqual(self.request(month='2028-01').status_code,422)
 def test_missing_evidence_fallback(self):
  cat=copy.deepcopy(self.cat)
  for t in cat['tasks']:
   for o in t['observations'].values():o['automation']=None
  result=calculate(cat,cat['personas']['mei'],'2026-05','fast')
  self.assertTrue(all(not r['hasTrend'] for r in result))
  for r in result:self.assertAlmostEqual(r['score'],100*(.7*r['baseline']/100+.2*r['interest']/100)/.9,delta=.11)
 def test_extraction_consent_and_no_credentials(self):
  self.assertEqual(self.client.post('/api/profile/extract',json={'description':'I check invoices.'}).status_code,422)
  with patch.dict('os.environ',{'AI_INTEGRATIONS_GEMINI_API_KEY':'','AI_INTEGRATIONS_GEMINI_BASE_URL':''}):
   d=self.client.post('/api/profile/extract',json={'description':'I check invoices.','consent':True}).json()
   self.assertEqual(d['mode'],'unconfigured');self.assertEqual(d['skill_ids'],[])
 def test_source_failure_retains_snapshot(self):
  before=self.client.get('/api/catalogue').json();server.last_refresh=0
  with patch('backend.signals.refresh_catalogue',side_effect=ValueError('Source unavailable')):
   self.assertEqual(self.client.post('/api/evidence/refresh').status_code,502)
  self.assertEqual(before,self.client.get('/api/catalogue').json())

if __name__=='__main__':unittest.main(verbosity=2)
