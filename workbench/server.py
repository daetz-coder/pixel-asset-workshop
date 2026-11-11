#!/usr/bin/env python3
"""Local-only bridge to the bundled sprite-gen engine."""
import atexit, http.server, json, math, os, pathlib, re, shutil, socket, subprocess, tempfile, threading, time, urllib.request, uuid, zipfile
from urllib.parse import urlparse, unquote
import wan_api

ROOT=pathlib.Path(__file__).resolve().parent
ENGINE=ROOT/'vendor'/'sprite-gen'
PYTHON=ROOT/'.venv'/'bin'/'python'
JOBS={}
MAX_BYTES=512*1024*1024
MAX_FRAMES=10_000

def command(args):
    p=subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=900)
    if p.returncode:
        raise RuntimeError((p.stderr or p.stdout or '引擎执行失败')[-4000:])
    return p.stdout

def key_video_region(clip, work, key, name, job):
    """Keep the engine's normal checks, retrying only a subject-edge refusal."""
    args=[str(PYTHON),'-m','sprite_gen.cli','video-frames','--clip',str(clip),'--out-dir',str(work),'--key',key]
    report_path=work/'frames.report.json'
    for flags in ([],['--allow-subject-edge-contact']):
        try:
            command([*args,*flags])
        except RuntimeError:
            if not report_path.is_file():
                raise
            reason=json.loads(report_path.read_text()).get('error','')
            if not flags and reason.startswith('video-frames: the subject touches the frame edge'):
                job['message']=f'{name} 有帧贴边，正在保留贴边帧并复查背景…'
                continue
            if reason.startswith('video-frames: leftover chroma background'):
                raise ValueError(f'{name} 的裁框边缘仍有底色残留。请检查背景类型，或沿时间轴检查并调整裁框。') from None
            if 'keyed to 0% transparency' in reason:
                raise ValueError(f'{name} 有帧未能去除背景。请选择与原视频一致的背景类型。') from None
            raise
        else:
            break
    report=json.loads(report_path.read_text())
    contacts=[contact for contact in report.get('edge_contacts',[]) if contact.get('subject',0)>0]
    if not contacts:
        return None
    first=re.fullmatch(r'frame-(\d+)\.png',contacts[0]['frame'])
    return {'frameCount':len(contacts),
            'firstFrameIndex':int(first[1])-1 if first else None,
            'sides':[side for side in ('top','left','right') if any(c.get(side,0)>0 for c in contacts)]}

def run_job(job, params, source):
    try:
        from PIL import Image
        regions=params['regions']; kind=params['kind']; key=params['key']; fps=float(params['fps']); start=float(params['start']); end=float(params['end'])
        if kind not in ('image','video') or key not in ('auto','magenta','green','white'): raise ValueError('不支持的素材或背景类型')
        mode=params.get('samplingMode','uniform')
        if mode not in ('uniform','native') or (mode=='native' and kind!='video'):
            raise ValueError('不支持的采样方式')
        native=mode=='native'
        if (
            not 1<=len(regions)<=100 or not 0.1<=fps<=60
            or not math.isfinite(start) or start<0
            or (kind=='video' and (
                not math.isfinite(end) or end<=start
                or (not native and (end-start)*fps*len(regions)>MAX_FRAMES)
            ))
        ):
            raise ValueError('时间、帧率或区域数量超出范围')
        w=int(params['width']); h=int(params['height'])
        if w<1 or h<1 or w*h>100_000_000: raise ValueError('素材尺寸超出范围')
        folder=source.parent; result=folder/'result'; result.mkdir()
        info={'engine':'sprite-gen','sourceType':kind,'sampling':{'start':start,'end':end,'mode':mode,'fps':None if native else fps},'background':key,'regions':[]}
        if params.get('referenceLayout'):
            info['referenceLayout']=params['referenceLayout']
        edge_regions=[]
        if kind=='image':
            img=Image.open(source); img.load()
            if img.size!=(w,h): raise ValueError('图片尺寸与请求不一致')
        else:
            probe=json.loads(command(['ffprobe','-v','error','-select_streams','V:0','-show_entries','stream=width,height:format=duration','-of','json',str(source)]))
            stream=probe['streams'][0]
            if (stream['width'],stream['height'])!=(w,h) or end>float(probe['format']['duration'])+0.05: raise ValueError('视频尺寸或结束时间不匹配')
        for i,r in enumerate(regions):
            x,y,rw,rh=(int(r[k]) for k in ('x','y','w','h'))
            if x<0 or y<0 or rw<1 or rh<1 or x+rw>w or y+rh>h: raise ValueError('区域超出画面')
            name=re.sub(r'[\\/:*?"<>|\x00-\x1f]','_',str(r.get('name','区域')))[:80].strip(' .') or '区域'
            name=f'{i+1:02d}_{name}'; out=result/name; out.mkdir()
            job['message']=f'正在处理 {i+1}/{len(regions)}：{name}'
            edge_contact=None
            if kind=='video':
                clip=folder/f'clip-{i}.mkv'
                crop_filter=f'crop={rw}:{rh}:{x}:{y}:exact=1'
                limit=MAX_FRAMES//len(regions)
                args=['ffmpeg','-nostdin','-v','error','-y','-i',str(source),'-map','0:V:0']
                if native:
                    args += ['-vf',f'trim=start={start}:end={end},{crop_filter},setpts=PTS-STARTPTS',
                             '-fps_mode','passthrough','-enc_time_base','1/1000000','-frames:v',str(limit+1)]
                else:
                    args += ['-ss',str(start),'-t',str(end-start),'-vf',f'{crop_filter},fps={fps}']
                command([*args,'-an','-c:v','ffv1','-pix_fmt','yuv444p',str(clip)])
                if native and i==0:
                    try:
                        packets=command(['ffprobe','-v','error','-select_streams','v:0','-count_packets',
                                         '-show_entries','stream=nb_read_packets','-of','csv=p=0',str(clip)]).strip()
                    except RuntimeError:
                        raise ValueError('所选时间范围内没有视频帧') from None
                    if not packets.isdigit():
                        raise ValueError('所选时间范围内没有视频帧')
                    if int(packets)>limit:
                        raise ValueError('单次最多导出 10000 张图，请缩短时间或减少区域')
                work=folder/f'engine-{i}'
                edge_contact=key_video_region(clip,work,key,name,job)
                frames=sorted((work/'keyed').glob('*.png'))
                if not frames: raise ValueError('引擎没有输出帧')
                for j,p in enumerate(frames): shutil.copy2(p,out/f'{j:04d}.png')
                if (work/'frames.report.json').exists(): shutil.copy2(work/'frames.report.json',out/'sprite-gen-report.json')
                count=len(frames)
            else:
                crop=folder/f'crop-{i}.png';img.crop((x,y,x+rw,y+rh)).save(crop)
                command([str(PYTHON),'-m','sprite_gen.cli','cutout',str(crop),'--out',str(out/'0000.png'),'--key',key,'--decontam','auto'])
                count=1
            region_info={'name':name,'x':x,'y':y,'width':rw,'height':rh,'frames':count}
            if edge_contact:
                region_info['edgeContact']=edge_contact
                edge_regions.append((name,edge_contact['frameCount']))
            for field in ('cell','action','anchor'):
                if field in r:
                    region_info[field]=r[field]
            info['regions'].append(region_info)
        (result/'manifest.json').write_text(json.dumps(info,ensure_ascii=False,indent=2))
        target=folder/'sprite-gen-result.zip'
        with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED) as z:
            for p in result.rglob('*'):
                if p.is_file(): z.write(p,p.relative_to(result).as_posix())
        message=f'完成：{len(regions)} 个区域'
        if edge_regions:
            affected='、'.join(f'{name}（{count} 帧）' for name,count in edge_regions[:2])
            if len(edge_regions)>2:
                affected+=f'等 {len(edge_regions)} 个区域'
            message+=f'。{affected}有主体贴边，已保留这些帧，可打开筛帧检查裁切。'
        job.update(state='done', message=message, result=str(target), result_dir=str(result), folder=str(folder))
    except Exception as e: job.update(state='error',message=str(e))


def prepare_curation(job, run):
    from sprite_gen.curate.curation import empty_curation, write_curation_atomic
    from sprite_gen.spec.runio import load_request, write_request, publish_guard

    command([str(PYTHON),'-m','sprite_gen.cli','unpack-atlas','--pngs-dir',job['result_dir'],'--out-dir',str(run),'--force'])
    info=json.loads((pathlib.Path(job['result_dir'])/'manifest.json').read_text())
    sampling=info['sampling']
    if info['sourceType']!='video':
        return
    with publish_guard(run):
        request=load_request(run)
        native=sampling.get('mode')=='native'
        fps=10 if native else min(30,max(1,round(sampling['fps'])))
        for state in request['states'].values():
            state['fps']=fps
        write_request(run,request)
        if native:
            curation=empty_curation()
            curation['states']={name:{'selected':[],'selection_explicit':True} for name in request['states']}
            write_curation_atomic(run,curation)

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self,*args,**kwargs): super().__init__(*args,directory=str(ROOT),**kwargs)
    def allowed(self):
        host=self.headers.get('Host',''); origin=self.headers.get('Origin','')
        return host in ('127.0.0.1:8766','localhost:8766') and (not origin or origin in ('http://127.0.0.1:8766','http://localhost:8766'))
    def send_json(self,code,obj):
        b=json.dumps(obj,ensure_ascii=False).encode();self.send_response(code);self.send_header('Content-Type','application/json; charset=utf-8');self.send_header('Content-Length',str(len(b)));self.send_header('Cache-Control','no-store');self.end_headers();self.wfile.write(b)
    def do_GET(self):
        if not self.allowed(): self.send_error(403);return
        path=urlparse(self.path).path
        if path=='/api/wan/info':
            try: self.send_json(200,wan_api.info())
            except Exception as e: self.send_json(400,{'error':str(e)})
            return
        if path=='/api/wan/tasks': self.send_json(200,{'tasks':wan_api.listing()});return
        if re.fullmatch(r'/api/wan/tasks/[0-9a-f]{32}',path):
            try: self.send_json(200,wan_api.get_task(path.rsplit('/',1)[1]))
            except ValueError: self.send_error(404)
            return
        if path.startswith('/api/wan/tasks/') and path.endswith('/video'):
            try:
                local_id=path.split('/')[4];target=wan_api.video_path(local_id);size=target.stat().st_size
                self.send_response(200);self.send_header('Content-Type','video/mp4');self.send_header('Content-Length',str(size));self.send_header('Cache-Control','no-store');self.end_headers()
                with target.open('rb') as f: shutil.copyfileobj(f,self.wfile,1024*1024)
            except (ValueError,OSError): self.send_error(404)
            return
        if path=='/api/status': self.send_json(200,{'available':PYTHON.exists() and (ENGINE/'sprite_gen').exists() and bool(shutil.which('ffmpeg')),'engine':'sprite-gen'});return
        if path.startswith('/api/jobs/'):
            parts=path.split('/');job=JOBS.get(parts[3]) if len(parts)>3 else None
            if not job: self.send_error(404);return
            if len(parts)==5 and parts[4] in ('download','curated') and job.get('state')=='done':
                target=pathlib.Path(job['result']) if parts[4]=='download' else pathlib.Path(job['folder'])/'curated.zip'
                if not target.exists(): self.send_error(404);return
                b=target.read_bytes();self.send_response(200);self.send_header('Content-Type','application/zip');self.send_header('Content-Disposition',f'attachment; filename="{"sprite-gen-frames.zip" if parts[4]=="download" else "sprite-gen-curated.zip"}"');self.send_header('Content-Length',str(len(b)));self.end_headers();self.wfile.write(b);return
            self.send_json(200,{k:v for k,v in job.items() if k in ('state','message')});return
        if path not in ('/','/index.html','/style.css','/app.js','/favicon.ico','/assets/warhammer-preview.png','/assets/zhuzhen.svg','/assets/icons.svg','/assets/InterVariable.woff2','/studio.html','/studio.css','/studio.js','/layout.js'):
            self.send_error(404);return
        return super().do_GET()
    def do_POST(self):
        if not self.allowed() or self.headers.get('X-Sprite-Studio')!='1': self.send_error(403);return
        try:
            parts=urlparse(self.path).path.split('/')
            if self.path=='/api/wan/import':
                length=int(self.headers.get('Content-Length','0'))
                if not 0<length<=1024: raise ValueError('请求大小无效')
                task=wan_api.import_task(json.loads(self.rfile.read(length)).get('task_id'));self.send_json(201,task);return
            if self.path=='/api/wan/submit':
                length=int(self.headers.get('Content-Length','0'))
                if not 0<length<=30_000_000: raise ValueError('请求大小无效')
                task=wan_api.submit(json.loads(self.rfile.read(length)));self.send_json(201,task);return
            if len(parts)==6 and parts[1:4]==['api','wan','tasks'] and parts[5]=='refresh':
                task=wan_api.refresh(parts[4]);self.send_json(200,task);return
            if len(parts)==5 and parts[1:3]==['api','jobs'] and parts[4] in ('curation','export-curated'):
                job=JOBS.get(parts[3]); action=parts[4]
                if not job or job.get('state')!='done': raise ValueError('任务不存在或尚未完成')
                with job.setdefault('curation_lock',threading.Lock()):
                    run=pathlib.Path(job['folder'])/'curation-run'
                    if action=='curation':
                        proc=job.get('curation_process')
                        if proc and proc.poll() is None: self.send_json(200,{'url':job['curation_url']}); return
                        if not run.exists():
                            try: prepare_curation(job,run)
                            except Exception:
                                shutil.rmtree(run,ignore_errors=True)
                                raise
                        with socket.socket() as sock:
                            sock.bind(('127.0.0.1',0));port=sock.getsockname()[1]
                        proc=subprocess.Popen([str(PYTHON),'-m','sprite_gen.cli','curation','--run-dir',str(run),'--host','127.0.0.1','--port',str(port),'--no-open'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                        url=f'http://127.0.0.1:{port}/'
                        for _ in range(60):
                            if proc.poll() is not None: raise ValueError('帧筛选界面启动失败')
                            try:
                                local=urllib.request.build_opener(urllib.request.ProxyHandler({}))
                                with local.open(url,timeout=0.2) as response:
                                    if response.status==200: break
                            except Exception: time.sleep(0.1)
                        else: proc.terminate();raise ValueError('帧筛选界面启动超时')
                        job['curation_process']=proc;job['curation_url']=url;self.send_json(200,{'url':url});return
                    if not run.exists(): raise ValueError('请先打开帧筛选界面')
                    dest=pathlib.Path(job['folder'])/'curated-output'
                    if dest.exists(): shutil.rmtree(dest)
                    exported=json.loads(command([str(PYTHON),'-m','sprite_gen.cli','export-pngs','--run-dir',str(run),'--out-dir',str(dest),'--selected-only']))
                    if not exported['count']:
                        raise ValueError('请至少选择一帧后再导出')
                    info=json.loads((pathlib.Path(job['result_dir'])/'manifest.json').read_text())
                    archive_names={}
                    if info['sampling'].get('mode')=='native':
                        actions={region['name']:region.get('action') for region in info['regions']}
                        for animation in exported['animations']:
                            folder=pathlib.PurePosixPath(animation['name'])
                            action=actions.get(animation['name'])
                            if isinstance(action,str) and re.fullmatch(r'[a-zA-Z0-9][a-zA-Z0-9_-]{0,39}',action):
                                folder=folder/action
                            for index, frame in enumerate(animation['frames']):
                                filename=(folder/f'{index:04d}.png').as_posix()
                                archive_names[frame['file']]=filename
                                frame['file']=filename
                    (dest/'manifest.json').write_text(json.dumps({
                        'version':1,'source':info,'cell':exported['cell'],
                        'animations':exported['animations']
                    },ensure_ascii=False,indent=2))
                    sidecar=run/'curation.json'
                    if sidecar.exists(): shutil.copy2(sidecar,dest/'curation.json')
                    target=pathlib.Path(job['folder'])/'curated.zip'
                    with zipfile.ZipFile(target.with_suffix('.tmp'),'w',zipfile.ZIP_DEFLATED) as z:
                        for p in dest.rglob('*'):
                            if p.is_file():
                                name=p.relative_to(dest).as_posix()
                                z.write(p,archive_names.get(name,name))
                    os.replace(target.with_suffix('.tmp'),target)
                    self.send_json(200,{'url':f'/api/jobs/{parts[3]}/curated'});return
            if self.path!='/api/jobs': raise ValueError('未知请求')
            length=int(self.headers.get('Content-Length','0'))
            if not 0<length<=MAX_BYTES: raise ValueError('文件大小须在 512 MB 以内')
            if not PYTHON.exists() or not (ENGINE/'sprite_gen').exists() or not shutil.which('ffmpeg'): raise ValueError('sprite-gen 引擎或 FFmpeg 未安装')
            params=json.loads(unquote(self.headers.get('X-Options','%7B%7D')));folder=pathlib.Path(tempfile.mkdtemp(prefix='sprite-studio-')); source=folder/'source'
            with source.open('wb') as out:
                remaining=length
                while remaining:
                    chunk=self.rfile.read(min(1024*1024,remaining))
                    if not chunk: raise ValueError('上传未完成')
                    out.write(chunk);remaining-=len(chunk)
            id=uuid.uuid4().hex;job={'state':'running','message':'已收到素材，准备处理','folder':str(folder)};JOBS[id]=job
            threading.Thread(target=run_job,args=(job,params,source),daemon=True).start();self.send_json(202,{'id':id})
        except Exception as e: self.send_json(400,{'error':str(e)})

def cleanup():
    for job in JOBS.values():
        proc=job.get('curation_process')
        if proc and proc.poll() is None: proc.terminate()
        folder=job.get('folder')
        if folder: shutil.rmtree(folder,ignore_errors=True)
atexit.register(cleanup)

if __name__=='__main__':
    wan_api.recover_interrupted()
    print('SpriteFrame workbench: http://127.0.0.1:8766',flush=True)
    http.server.ThreadingHTTPServer(('127.0.0.1',8766),Handler).serve_forever()
