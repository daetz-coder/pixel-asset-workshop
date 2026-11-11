"""Local Wan Prime task storage and API adapter. Credentials are never persisted."""
import base64, io, json, math, os, re, shutil, subprocess, sys, tempfile, threading, uuid
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from PIL import Image

ROOT=Path(__file__).resolve().parent
DATA=ROOT/'data'/'wan'
LOCK=threading.RLock()
MODEL='wan3.0-video-prime'
class APIRejected(Exception): pass

def connection(require_key=True):
    workspace=os.environ.get('DASHSCOPE_WORKSPACE','').strip()
    region=os.environ.get('DASHSCOPE_REGION','cn-beijing')
    if not workspace:
        if require_key: raise ValueError('请设置 DASHSCOPE_WORKSPACE 为你的百炼工作空间 ID')
        return None,'',None,region
    if not re.fullmatch(r'ws-[a-z0-9]+',workspace) or not re.fullmatch(r'[a-z0-9-]+',region): raise ValueError('百炼工作空间或地域格式无效')
    api_key=os.environ.get('DASHSCOPE_API_KEY','').strip()
    if not api_key and sys.platform=='darwin':
        try:
            p=subprocess.run(['/usr/bin/security','find-generic-password','-a','codex','-s',f'codex.wan-prime-video.{workspace}','-w'],capture_output=True,text=True,timeout=15)
            if p.returncode==0: api_key=p.stdout.strip()
        except (OSError,subprocess.SubprocessError): pass
    if require_key and not api_key: raise ValueError('未找到百炼密钥：设置 DASHSCOPE_API_KEY 或配置 Wan Prime 的 macOS 钥匙串')
    return f'https://{workspace}.{region}.maas.aliyuncs.com/api/v1',api_key,workspace,region

def api(path,payload=None):
    base,key,_,_=connection();headers={};body=None
    if payload is not None: headers={'Content-Type':'application/json','X-DashScope-Async':'enable'};body=json.dumps(payload,ensure_ascii=False).encode()
    req=Request(base+path,data=body,headers=headers);req.add_unredirected_header('Authorization','Bearer '+key)
    try:
        with urlopen(req,timeout=60) as res: return json.load(res)
    except HTTPError as exc:
        try: error=json.load(exc)
        except (ValueError,OSError): error={}
        safe=(str(error.get('code',''))+' '+str(error.get('message',''))).replace(key,'[redacted]')[:400]
        raise APIRejected(f'百炼返回 HTTP {exc.code}: {safe}') from None

def _path(local_id):
    if not re.fullmatch(r'[0-9a-f]{32}',local_id): raise ValueError('任务编号无效')
    return DATA/local_id

def _read(local_id):
    p=_path(local_id)/'task.json'
    if not p.exists(): raise ValueError('任务不存在')
    return json.loads(p.read_text(encoding='utf-8'))

def _write(local_id,task):
    p=_path(local_id);p.mkdir(parents=True,exist_ok=True,mode=0o700);os.chmod(p,0o700);os.chmod(DATA,0o700);temp=p/'task.json.tmp';temp.write_text(json.dumps(task,ensure_ascii=False,indent=2),encoding='utf-8');os.chmod(temp,0o600);os.replace(temp,p/'task.json')

def info():
    _,key,workspace,region=connection(False)
    return {'configured':bool(key),'workspace':workspace,'region':region,'model':MODEL}

def listing():
    if not DATA.exists(): return []
    rows=[]
    for p in DATA.glob('*/task.json'):
        try: rows.append(json.loads(p.read_text(encoding='utf-8')))
        except (OSError,ValueError): continue
    return sorted(rows,key=lambda x:x.get('created',''),reverse=True)


def recover_interrupted():
    """Do not retry an interrupted submission whose acceptance is unknown."""
    with LOCK:
        for task in listing():
            if task.get('state')=='SUBMITTING':
                task.update(state='UNCERTAIN',message='上次提交中断，结果不明；请先在百炼控制台核对，避免重复计费')
                _write(task['id'],task)

def validate_layout(layout, width, height):
    """Validate the reference layout kept locally, never send it to the provider."""
    if layout is None: return None
    if not isinstance(layout,dict) or layout.get('version')!=1: raise ValueError('组合布局格式无效')
    rows,cols=layout.get('rows'),layout.get('cols')
    if type(rows) is not int or type(cols) is not int or not 1<=rows<=8 or not 1<=cols<=8: raise ValueError('组合布局的行列无效')
    if layout.get('width')!=width or layout.get('height')!=height: raise ValueError('组合布局与参考图尺寸不一致')
    baseline=layout.get('baseline')
    if not isinstance(baseline,(int,float)) or isinstance(baseline,bool) or not math.isfinite(baseline) or not 0<=baseline<=1: raise ValueError('组合布局的脚底位置无效')
    action=layout.get('action','')
    if action not in ('idle','walk','run','attack','vfx'): raise ValueError('动作类型无效')
    color=layout.get('color')
    if color is not None and (not isinstance(color,str) or not re.fullmatch(r'#[0-9a-fA-F]{6}',color)): raise ValueError('组合布局的背景色无效')
    cells=layout.get('cells')
    if not isinstance(cells,list) or not 1<=len(cells)<=rows*cols: raise ValueError('组合布局的角色数量无效')
    result=[];seen=set()
    for cell in cells:
        if not isinstance(cell,dict): raise ValueError('组合布局格位无效')
        row,col=cell.get('row'),cell.get('col');name=cell.get('name');motion=cell.get('motion','')
        if type(row) is not int or type(col) is not int or not 0<=row<rows or not 0<=col<cols or (row,col) in seen: raise ValueError('组合布局格位无效或重复')
        if not isinstance(name,str) or not name.strip() or len(name)>80 or not isinstance(motion,str) or len(motion)>4000: raise ValueError('角色名称或动作描述无效')
        cell_action=cell.get('action',action)
        if cell_action not in ('idle','walk','run','attack','vfx') or (cell_action=='vfx')!=(action=='vfx'):
            raise ValueError('角色动作与组合布局不兼容')
        seen.add((row,col))
        result.append({'row':row,'col':col,'name':name.strip(),'motion':motion,'action':cell_action})
    return {'version':1,'rows':rows,'cols':cols,'width':width,'height':height,'baseline':baseline,
            'action':action,'color':color.lower() if color else None,'cells':result}

def get_task(local_id):
    with LOCK: return _read(local_id)

def submit(data):
    from datetime import datetime,timezone
    image=data.get('image','');prompt=str(data.get('prompt','')).strip();resolution=data.get('resolution');duration=data.get('duration');ratio=data.get('ratio','adaptive')
    if not isinstance(image,str) or not image.startswith('data:image/png;base64,'): raise ValueError('需要 PNG 首帧')
    if not 1<=len(prompt)<=20000: raise ValueError('提示词须为 1–20000 字符')
    if resolution not in ('480P','720P','1080P') or not isinstance(duration,int) or isinstance(duration,bool) or not 2<=duration<=30 or ratio!='adaptive': raise ValueError('视频参数无效')
    try: raw=base64.b64decode(image.split(',',1)[1],validate=True)
    except Exception: raise ValueError('首帧图片编码无效') from None
    if len(raw)>20_000_000: raise ValueError('首帧图片超过 20 MB')
    with Image.open(io.BytesIO(raw)) as img:
        if img.format!='PNG': raise ValueError('首帧须为 PNG')
        w,h=img.size
        if min(w,h)<240 or max(w,h)>8000 or max(w,h)>8*min(w,h): raise ValueError('首帧边长须在 240–8000，宽高比不超过 8:1')
        img.load()
        if 'A' in img.getbands() and img.getchannel('A').getextrema()[0] < 255: raise ValueError('首帧不能有透明区域，请使用纯色背景合图')
        buf=io.BytesIO();img.convert('RGB').save(buf,format='PNG');raw=buf.getvalue()
        if len(raw)>20_000_000: raise ValueError('处理后的首帧超过 20 MB')
        image='data:image/png;base64,'+base64.b64encode(raw).decode('ascii')
    layout=validate_layout(data.get('layout'),w,h)
    _,_,workspace,region=connection()
    local_id=uuid.uuid4().hex;folder=_path(local_id);folder.mkdir(parents=True,exist_ok=False,mode=0o700);os.chmod(DATA,0o700)
    (folder/'reference.png').write_bytes(raw);(folder/'prompt.txt').write_text(prompt,encoding='utf-8')
    os.chmod(folder/'reference.png',0o600);os.chmod(folder/'prompt.txt',0o600)
    task={'id':local_id,'task_id':None,'state':'SUBMITTING','message':'正在提交','created':datetime.now(timezone.utc).isoformat(),'workspace':workspace,'region':region,'model':MODEL,'resolution':resolution,'duration':duration,'has_video':False,'layout':layout}
    with LOCK: _write(local_id,task)
    payload={'model':MODEL,'input':{'prompt':prompt,'media':[{'type':'first_frame','url':image}]},'parameters':{'resolution':resolution,'ratio':ratio,'duration':duration,'audio':False,'prompt_extend':False,'watermark':False}}
    try:
        result=api('/services/aigc/video-generation/video-synthesis',payload);task_id=str(uuid.UUID(result['output']['task_id']));task.update(task_id=task_id,state='PENDING',message='已提交，等待百炼处理')
    except APIRejected as exc:
        task.update(state='ERROR',message=str(exc));_write(local_id,task);raise ValueError(str(exc)) from None
    except (URLError,TimeoutError,KeyError,OSError,TypeError,ValueError) as exc:
        task.update(state='UNCERTAIN',message='提交结果不明，请先在百炼控制台核对，避免重复计费');_write(local_id,task);raise ValueError(task['message']) from None
    with LOCK: _write(local_id,task)
    return task

def import_task(remote_id):
    from datetime import datetime,timezone
    try: remote_id=str(uuid.UUID(str(remote_id)))
    except (TypeError,ValueError,AttributeError): raise ValueError('任务 ID 格式无效') from None
    _,_,workspace,region=connection()
    with LOCK:
        for item in listing():
            if item.get('task_id')==remote_id and item.get('workspace')==workspace and item.get('region')==region: return item
        local_id=uuid.uuid4().hex
        task={'id':local_id,'task_id':remote_id,'state':'PENDING','message':'已导入任务 ID，请查询状态','created':datetime.now(timezone.utc).isoformat(),'workspace':workspace,'region':region,'model':MODEL,'resolution':'未知','duration':'?','has_video':False}
        _write(local_id,task);return task

def refresh(local_id):
    with LOCK:
        task=_read(local_id)
        if not task.get('task_id'): raise ValueError('该记录没有任务 ID；请先在百炼控制台核对')
        _,key,workspace,region=connection()
        if (workspace,region)!=(task['workspace'],task['region']): raise ValueError('当前工作空间或地域与任务不一致')
        result=api('/tasks/'+str(uuid.UUID(task['task_id'])));out=result['output'];state=out.get('task_status','UNKNOWN')
        if state not in ('PENDING','RUNNING','SUCCEEDED','FAILED','CANCELED','UNKNOWN'): state='UNKNOWN'
        task['state']=state;task['message']=str(out.get('message','')).replace(key,'[redacted]')[:400]
        if state=='SUCCEEDED' and not task.get('has_video'):
            url=out.get('video_url','')
            if not isinstance(url,str) or not url.startswith('https://'): raise ValueError('任务成功但没有有效视频链接')
            folder=_path(local_id);dest=folder/'video.mp4'
            with tempfile.NamedTemporaryFile(mode='w+b',dir=folder,delete=False) as tmp:
                try:
                    with urlopen(url,timeout=120) as response: shutil.copyfileobj(response,tmp,1024*1024)
                    tmp.flush();tmp.seek(0)
                    if tmp.read(8)[4:8]!=b'ftyp': raise ValueError('下载结果不是 MP4')
                    os.replace(tmp.name,dest)
                finally:
                    if os.path.exists(tmp.name): os.unlink(tmp.name)
            task['has_video']=True;task['message']='视频已保存到本机'
        _write(local_id,task);return task

def video_path(local_id):
    task=_read(local_id);path=_path(local_id)/'video.mp4'
    if not task.get('has_video') or not path.is_file(): raise ValueError('视频尚未下载')
    return path
