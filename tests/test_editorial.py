import copy,datetime as dt,json,pathlib,sys,tempfile,unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]/'scripts'))
from editorial import digest,validate,CHECKS
from publish_next import run,save

class Editorial(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.r=pathlib.Path(self.tmp.name)
  (self.r/'content/cola').mkdir(parents=True);(self.r/'content/entries').mkdir()
  save(self.r/'editorial/config.json',{'paused':False});save(self.r/'editorial/publications.json',{})
  self.d={'id':'CHG-A-9999','slug':'prueba-controlada','topic_key':'prueba-controlada','title':'PRUEBA SINTÉTICA NO HISTÓRICA','category':'Acciones militares','period':'Antigüedad','era':'prueba','date':'prueba','location':'prueba','summary':'prueba','facts':[['Tipo','Prueba']], 'sections':[{'heading':str(i),'paragraphs':[('prueba '*380)+' [1][2]']} for i in range(8)],'sources':[{'n':i,'name':'Fuente sintética de prueba','kind':'Prueba','url':'https://example.org/'+str(i),'verified_at':'2026-10-27','verification_note':'Dato sintético, nunca publicar en producción'} for i in range(1,6)],'editorial_note':'Prueba local','keywords':[],'eyebrow':'Prueba','related':[],'chronology':0,'status':'revisado'}
  self.approve(self.d);self.now=dt.datetime(2026,10,27,9,tzinfo=dt.timezone.utc)
 def approve(self,d):
  d['approval']={'reviewer':'REVISOR SINTÉTICO DE TEST','date':'2026-10-27','notes':'Solo simulación','checks':dict.fromkeys(CHECKS,True),'content_sha256':digest(d)}
 def queue(self,d=None):save(self.r/'content/cola/test.json',d or self.d)
 def test_empty(self):self.assertEqual(run(self.r,'09:17',self.now)['result'],'empty_or_held')
 def test_publish_and_repeat(self):
  self.queue();self.assertEqual(run(self.r,'09:17',self.now)['result'],'published');self.assertEqual(run(self.r,'09:17',self.now)['result'],'already_published');self.assertTrue((self.r/'content/entries/CHG-A-9999.json').exists())
 def test_changed_after_approval(self):
  self.d['title']='Cambio';self.queue();self.assertEqual(run(self.r,'09:17',self.now)['result'],'empty_or_held')
 def test_wrong_category(self):
  self.queue();self.assertEqual(run(self.r,'15:17',self.now+dt.timedelta(hours=8))['result'],'empty_or_held')
 def test_dry_run(self):
  self.queue();self.assertEqual(run(self.r,'09:17',self.now,True)['result'],'would_publish');self.assertTrue((self.r/'content/cola/test.json').exists());self.assertEqual(list((self.r/'content/entries').glob('*')),[])
 def test_duplicate_topic(self):
  save(self.r/'editorial/inventory.json',[{'topic_key':self.d['topic_key']}]);self.queue();self.assertEqual(run(self.r,'09:17',self.now)['result'],'empty_or_held')
 def test_pause(self):
  save(self.r/'editorial/config.json',{'paused':True});self.queue();self.assertEqual(run(self.r,'09:17',self.now)['result'],'paused')
 def test_invalid_json(self):
  (self.r/'content/cola/test.json').write_text('{');self.assertEqual(run(self.r,'09:17',self.now)['result'],'empty_or_held')
 def test_one_per_day_even_across_slots(self):
  self.queue()
  self.assertEqual(run(self.r,'09:17',self.now)['result'],'published')
  later=dt.datetime(2026,10,27,21,0,tzinfo=dt.timezone.utc)
  self.assertEqual(run(self.r,'21:17',later)['result'],'already_published')
 def test_evening_accepts_any_category(self):
  self.queue()
  now=dt.datetime(2026,10,27,21,0,tzinfo=dt.timezone.utc)
  self.assertEqual(run(self.r,'21:17',now,True)['result'],'would_publish')
 def test_minimum_length(self):
  self.d['sections']=self.d['sections'][:3]
  self.approve(self.d);self.queue()
  result=run(self.r,'09:17',self.now)
  self.assertEqual(result['result'],'empty_or_held')
  self.assertTrue(result['held'])
 def test_minimum_sources(self):
  self.d['sources']=self.d['sources'][:2]
  self.approve(self.d);self.queue()
  self.assertEqual(run(self.r,'09:17',self.now)['result'],'empty_or_held')
 def test_missing_verification(self):
  del self.d['sources'][0]['verification_note'];self.approve(self.d);self.assertFalse(validate(self.d)[0])
 def test_summer_winter(self):
  self.queue()
  for month,hour in ((7,7),(12,8)):
   before=dt.datetime(2026,month,15,hour,16,tzinfo=dt.timezone.utc)
   after=before+dt.timedelta(minutes=1)
   self.assertEqual(run(self.r,'09:17',before,True)['result'],'not_due')
   self.assertEqual(run(self.r,'09:17',after,True)['result'],'would_publish')
 def test_future(self):
  self.d['not_before']='2027-01-01';self.approve(self.d);self.queue();self.assertEqual(run(self.r,'09:17',self.now)['result'],'empty_or_held')
 def test_not_reviewed(self):
  self.d['status']='borrador';self.queue();self.assertEqual(run(self.r,'09:17',self.now)['result'],'empty_or_held')
if __name__=='__main__':unittest.main()
