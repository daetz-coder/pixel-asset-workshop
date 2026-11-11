import base64, io, json, tempfile, unittest
from pathlib import Path
from unittest.mock import patch
from urllib.error import URLError
from PIL import Image
import wan_api

class FakeResponse(io.BytesIO):
    def __enter__(self): return self
    def __exit__(self,*args): self.close()

def mixed_layout():
    return {'version':1,'rows':2,'cols':3,'width':256,'height':256,'baseline':0.7,
            'action':'idle','color':'#FF00FF','cells':[
                {'row':0,'col':0,'name':'战锤兵','action':'attack','motion':'Strike to the right.'},
                {'row':1,'col':2,'name':'弩兵','action':'run','motion':'Run in place.'}
            ]}

class WanWorkflowTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(); self.root=Path(self.temp.name)
        self.patch_data=patch.object(wan_api,'DATA',self.root);self.patch_data.start()
        self.patch_conn=patch.object(wan_api,'connection',return_value=('https://example.test/api/v1','test-secret','ws-test','cn-beijing'));self.patch_conn.start()
        buf=io.BytesIO(); Image.new('RGBA',(256,256),(255,0,255,255)).save(buf,'PNG')
        self.options={'image':'data:image/png;base64,'+base64.b64encode(buf.getvalue()).decode(),'prompt':'Move in place.','resolution':'480P','duration':5,'ratio':'adaptive'}
    def tearDown(self): self.patch_conn.stop();self.patch_data.stop();self.temp.cleanup()
    def test_submit_poll_and_download_persists_task(self):
        received=[]
        def fake_api(path,payload=None):
            received.append((path,payload))
            if payload:return {'output':{'task_id':'17ed7e50-0285-4969-aea1-000000000001'}}
            return {'output':{'task_status':'SUCCEEDED','video_url':'https://example.test/video.mp4'}}
        with patch.object(wan_api,'api',side_effect=fake_api),patch.object(wan_api,'urlopen',return_value=FakeResponse(b'\x00\x00\x00\x18ftypmp42more')):
            task=wan_api.submit(self.options); self.assertEqual(task['state'],'PENDING')
            payload=received[0][1];self.assertEqual(payload['model'],'wan3.0-video-prime'); self.assertEqual(payload['input']['media'][0]['type'],'first_frame')
            image=base64.b64decode(payload['input']['media'][0]['url'].split(',')[1]);self.assertEqual(Image.open(io.BytesIO(image)).mode,'RGB')
            done=wan_api.refresh(task['id']);self.assertTrue(done['has_video']);self.assertEqual(done['state'],'SUCCEEDED')
            self.assertTrue(wan_api.video_path(task['id']).read_bytes()[4:8]==b'ftyp')
            self.assertNotIn('test-secret',json.dumps(wan_api.listing()))
    def test_uncertain_submission_preserved_without_retry(self):
        with patch.object(wan_api,'api',side_effect=URLError('timeout')) as request:
            with self.assertRaisesRegex(ValueError,'提交结果不明'):wan_api.submit(self.options)
            self.assertEqual(request.call_count,1); self.assertEqual(wan_api.listing()[0]['state'],'UNCERTAIN')
    def test_import_task_is_idempotent_and_interrupted_submission_is_not_retried(self):
        with patch.object(wan_api,'api') as remote:
            one=wan_api.import_task('17ed7e50-0285-4969-aea1-000000000003')
            two=wan_api.import_task('17ed7e50-0285-4969-aea1-000000000003')
            self.assertEqual(one['id'],two['id']);self.assertEqual(len(wan_api.listing()),1)
            one['state']='SUBMITTING';wan_api._write(one['id'],one);wan_api.recover_interrupted()
            self.assertEqual(wan_api.listing()[0]['state'],'UNCERTAIN');remote.assert_not_called()
    def test_reject_transparent_reference(self):
        b=io.BytesIO();Image.new('RGBA',(256,256),(0,0,0,0)).save(b,'PNG');self.options['image']='data:image/png;base64,'+base64.b64encode(b.getvalue()).decode()
        with self.assertRaisesRegex(ValueError,'透明区域'):wan_api.submit(self.options)
    def test_layout_rejects_duplicate_cells_and_mixed_blank_plate(self):
        layout=mixed_layout()
        layout['cells'].append(layout['cells'][0])
        with self.assertRaisesRegex(ValueError,'重复'):wan_api.validate_layout(layout,256,256)
        layout=mixed_layout()
        layout['action']='vfx'
        with self.assertRaisesRegex(ValueError,'不兼容'):wan_api.validate_layout(layout,256,256)
    def test_legacy_layout_inherits_batch_action(self):
        layout=mixed_layout()
        del layout['color']
        del layout['cells'][0]['action']
        self.assertEqual(wan_api.validate_layout(layout,256,256)['cells'][0]['action'],'idle')

if __name__=='__main__':unittest.main()

class WanHTTPTests(unittest.TestCase):
    def test_http_submission_status_and_video(self):
        import http.server, threading, urllib.request
        from server import Handler
        with tempfile.TemporaryDirectory() as folder, patch.object(wan_api,'DATA',Path(folder)), patch.object(wan_api,'connection',return_value=('https://example.test/api/v1','secret','ws-test','cn-beijing')), patch.object(Handler,'allowed',return_value=True):
            def fake_api(path,payload=None):
                if payload:
                    self.assertNotIn('layout',payload)
                    self.assertNotIn('layout',payload['input'])
                return {'output':{'task_id':'17ed7e50-0285-4969-aea1-000000000002'}} if payload else {'output':{'task_status':'SUCCEEDED','video_url':'https://example.test/video.mp4'}}
            with patch.object(wan_api,'api',side_effect=fake_api),patch.object(wan_api,'urlopen',return_value=FakeResponse(b'\x00\x00\x00\x18ftypmp42data')):
                http=http.server.ThreadingHTTPServer(('127.0.0.1',0),Handler);thread=threading.Thread(target=http.serve_forever,daemon=True);thread.start()
                try:
                    base='http://127.0.0.1:'+str(http.server_port);out=io.BytesIO();Image.new('RGB',(256,256),(255,0,255)).save(out,'PNG')
                    data={'image':'data:image/png;base64,'+base64.b64encode(out.getvalue()).decode(),'prompt':'Walk.','resolution':'480P','duration':5,'ratio':'adaptive','layout':mixed_layout()}
                    def post(path,body=b''):
                        req=urllib.request.Request(base+path,data=body,headers={'X-Sprite-Studio':'1','Content-Type':'application/json'},method='POST')
                        with urllib.request.urlopen(req) as r:return json.load(r)
                    task=post('/api/wan/submit',json.dumps(data).encode());self.assertEqual(task['state'],'PENDING')
                    task=post('/api/wan/tasks/'+task['id']+'/refresh');self.assertTrue(task['has_video'])
                    with urllib.request.urlopen(base+'/api/wan/tasks/'+task['id']) as r:
                        layout=json.load(r)['layout']
                        self.assertEqual(layout['color'],'#ff00ff')
                        self.assertEqual(layout['cells'],mixed_layout()['cells'])
                    with urllib.request.urlopen(base+'/api/wan/tasks/'+task['id']+'/video') as r:self.assertEqual(r.read()[4:8],b'ftyp')
                    with urllib.request.urlopen(base+'/api/wan/tasks') as r:self.assertEqual(len(json.load(r)['tasks']),1)
                finally: http.shutdown();http.server_close();thread.join()
