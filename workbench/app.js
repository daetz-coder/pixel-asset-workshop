'use strict';
const copyEN = {
 '逐帧提取并挑选':'Extract every frame and choose',
 '保留所选时段的所有原始帧，并自动初选一段播放序列。预览从 10 fps 开始。':'Keep all source frames in the time range and suggest an editable sequence. Preview starts at 10 fps.',
 '点击「加入」选帧，拖动卡片调整播放顺序，用右侧预览逐帧检查。完成后在下载菜单选择「下载选中 PNG」。':'Click Add to choose frames, drag cards to set their playback order, and step through the preview on the right. Choose Download selected PNGs from the download menu when ready.',
 '请至少选择一帧后再导出':'Choose at least one frame before exporting.',
 '不支持的采样方式':'Unsupported sampling mode.',
 '所选时间范围内没有视频帧':'The selected time range contains no video frames.',
 '逐帧':'SpriteFrame','逐帧 · 序列帧提取':'SpriteFrame · Frame Extraction','逐帧 · 像素素材工作台':'SpriteFrame · Workbench',
 '工作台':'Workspace','界面语言':'Interface language','逐帧工作台':'Frame Studio','序列帧提取':'Frame extraction',
 '导入格位 JSON':'Import crop layout','清除格位文件':'Clear layout file','格位文件无效':'Invalid crop layout file.',
 '已清除格位文件。当前裁框可继续编辑。':'Layout file cleared. The current crops can still be edited.',
 '提取期间无法更换格位。':'Wait for extraction to finish before changing the layout.',
 '提取':'Extract','筛帧':'Curate','导入素材':'Import media','从视频或图片中提取独立的透明 PNG 序列。':'Extract individual transparent PNG frames from a video or image.',
 '素材与区域设置':'Source and crop settings','素材与区域':'Source and crops','素材':'Media','来源':'Source','尚未选择文件':'No file selected',
 '素材在本机处理。':'Files are processed locally.','识别区域':'Detect crops','当前画面':'Current frame','自动识别区域':'Auto-detect crops',
 '识别容差':'Detection tolerance','框外余量':'Padding','从当前帧识别并替换区域。可拖动画框或编辑坐标。':'Detect crops from the current frame. Drag a new box or edit its coordinates.',
 '扫描动作范围':'Scan motion bounds',
 '取消扫描':'Cancel scan',
 '请检查扫描时间范围。':'Check the time range for the motion scan.',
 '扫描期间裁框已变更，请重新扫描。':'The crops changed during scanning. Run the scan again.',
 '所选时段无法可靠识别底色，请检查背景和识别容差。':'Could not identify the background reliably. Check the background and detection tolerance.',
 '没有区域需要扩大。':'The existing crops cover the detected motion.',
 '重叠的裁框保留原尺寸，请分别检查。':'Overlapping crops kept their original sizes. Inspect them separately.',
 '动作触及扫描边界。点击时间查看，必要时单独裁出特效。':'Motion reached a scan boundary. Click a time to inspect it or crop the effect separately.',
 '自定义网格':'Custom grid','列数':'Columns','行数':'Rows','按网格划分':'Apply grid','区域列表':'Crops','可编辑坐标':'Editable coordinates','清空':'Clear',
 '识别或手动画框后':'Detected or manually drawn','区域会显示在这里':'crops appear here.','素材画布与预览':'Canvas and preview','画布':'Canvas','尚未导入素材':'No media loaded',
 '拖动框边或角可调整大小':'Drag a crop edge or corner to resize','战锤兵示例像素角色':'Warhammer infantry sample','导入待拆分的素材':'Import media to extract frames',
 '选择或拖入一段视频或一张图片。':'Choose or drop a video or image.','选择本地素材':'Choose file','素材画布，可绘制区域框或拖动框边调整大小':'Media canvas. Draw crop boxes or drag their edges to resize.',
 '时间轴':'Timeline','视频采样':'Video sampling','▶ 播放原视频':'▶ Play source','Ⅱ 暂停':'Ⅱ Pause','时间位置':'Position','开始时间':'Start','结束时间':'End','秒':'sec',
 '提取帧率':'Sample rate','默认 10 fps':'Default 10 fps','按时间均匀采样。提高帧率可保留更短的动作。':'Frames are sampled evenly. A higher rate can capture shorter motions.',
 '导入视频后可选择时间范围与帧率':'Import a video to set the time range and frame rate.','区域预览':'Crop previews','检查当前帧的选区和透明边缘':'Inspect the crops and transparent edges.',
 '吸取背景色':'Sample background','点击画布选择颜色':'Click canvas to sample','创建区域后，预览会显示在这里':'Crop previews appear here.',
 '背景与导出设置':'Background and export settings','输出设置':'Output settings','背景处理':'Background removal','快速提取':'Quick extract','去除背景色':'Remove background color',
 '背景颜色':'Background color','颜色容差':'Color tolerance','仅去除与边缘连通的背景':'Remove only background connected to the edges',
 '清理洋红和绿幕残色':'Clean up magenta and green spill',
 '角色也有底色时，可仅去除与框边连通的背景。':'When the sprite shares the key color, limit removal to background connected to the crop edges.',
 '这里已经透明，请点击有颜色的底色。':'This area is already transparent. Click a colored background.',
 '已吸取背景色，预览已更新。':'Background sampled and preview updated.',
 '导出 PNG':'Export PNGs','序列帧':'Sequence','按区域分别输出透明 PNG，并记录坐标与采样信息。':'Export transparent PNGs by crop with coordinates and sampling information.',
 '提取并下载 PNG':'Extract and download PNGs','ZIP 压缩包':'ZIP archive','高级抠像与筛帧':'Advanced keying and curation','检查中':'Checking…',
 '处理完成后，可在本页筛选、排序和编辑帧。':'Select, reorder, and edit frames here after extraction.',
 '背景类型':'Key color','自动检测':'Auto-detect','洋红':'Magenta','绿色':'Green','白色':'White','使用 sprite-gen 提取':'Extract with sprite-gen','进入筛帧':'Open curation',
 '上方容差仅用于快速提取。高级提取会标记并保留主体贴边的帧，可在筛帧界面检查裁切。':'The tolerance above applies to quick extraction. Advanced extraction keeps and flags frames that touch crop edges.',
 '处理状态':'Status','等待导入素材':'Waiting for media','取消提取':'Cancel extraction','筛帧工作区':'Frame curation workspace','筛帧与编辑':'Curate and edit frames',
 '下载原始 PNG':'Download raw PNGs','重试加载':'Retry loading','sprite-gen 筛帧编辑器':'sprite-gen frame editor',
 '区域名称':'Crop name','删除区域':'Remove crop','宽':'W','高':'H','暂无区域，请拖动画框':'No crops. Drag on the canvas to draw one.',
 '划分有效区域后，在这里检查画面与透明边缘':'Create a valid crop to inspect its transparent edges here.',
 '已就绪':'Ready','未安装':'Not installed','需要本地服务':'Local server required','错误：':'Error: ',
 '视频定位超时，浏览器可能不支持此文件':'Seeking timed out. The browser may not support this video.',
 '无法读取视频帧':'Could not read the video frame.','正在读取素材…':'Loading media…','无法读取视频，请尝试 MP4 或 WebM':'Could not read video. Try MP4 or WebM.',
 '请选择视频或图片':'Choose a video or image.','请一次导入一份素材':'Import one file at a time.','原格位无法映射到该视频尺寸，已尝试识别当前帧。':'The reference grid does not fit this video. Tried detecting crops in the current frame.',
 '无法确定背景：请检查画面四角、调整识别容差，或手动画框':'Could not detect the background. Check the corners, adjust the tolerance, or draw crops.',
 '画面噪点过多，请调整识别容差或手动画框':'Too much image noise. Adjust the tolerance or draw crops manually.',
 '没有识别到区域；请调整识别容差或手动画框':'No crops detected. Adjust the tolerance or draw crops manually.',
 'PNG 编码失败':'PNG encoding failed.','正在取消…':'Canceling…','已取消':'Canceled.','区域坐标超出画面':'A crop lies outside the canvas.',
 '请检查时间范围和帧率（0.1–60）':'Check the time range and frame rate (0.1–60).','请检查时间范围和帧率':'Check the time range and frame rate.',
 '单次最多导出 10000 张图，请缩短时间或减少区域':'A single export can contain at most 10,000 images. Shorten the time range or use fewer crops.',
 '正在发送素材到本地引擎…':'Sending media to the local engine…','无法启动引擎':'Could not start the engine.','无法读取任务状态':'Could not read job status.',
 '正在准备帧筛选界面…':'Preparing the frame editor…','已收到素材，准备处理':'Media received. Preparing extraction.',
 '筛帧界面加载超时，请重试。':'The frame editor timed out. Please retry.','无法加载筛帧界面':'Could not load the frame editor.',
 '正在载入已生成视频…':'Loading the saved video…','无效的视频任务编号':'Invalid video job ID.','视频不存在或尚未生成':'The video is unavailable.',
 '导入对应的成片':'Import the matching video','导入后会自动沿用角色名、格位和背景色。':'The video will use the saved names, grid, and key color.',
 '等待导入对应的本地视频':'Waiting for the matching local video.',
 '无法播放视频：':'Could not play video: ',
 '任务不存在或尚未完成':'The job does not exist or has not finished.',
 '帧筛选界面启动失败':'Could not start the frame editor.','帧筛选界面启动超时':'The frame editor timed out.',
 '文件大小须在 512 MB 以内':'The file must be under 512 MB.',
 'sprite-gen 引擎或 FFmpeg 未安装':'sprite-gen or FFmpeg is unavailable.',
 '上传未完成':'The upload did not finish.',
 '时间、帧率或区域数量超出范围':'The time range, frame rate, or crop count is out of range.',
 '不支持的素材或背景类型':'Unsupported media or key color.',
 '素材尺寸超出范围':'The media dimensions are out of range.',
 '图片尺寸与请求不一致':'The image dimensions did not match.',
 '区域超出画面':'A crop lies outside the canvas.',
 '引擎没有输出帧':'The engine did not produce any frames.',
 '请先打开帧筛选界面':'Open the frame editor first.',
 '正在导出筛选后的帧…':'Exporting selected frames…','筛选后的帧已导出':'Selected frames exported.',
 '无法导出筛选后的帧':'Could not export the selected frames.',
 '视频尺寸或结束时间不匹配':'The video dimensions or end time did not match.'
};
let language = 'en';
try { if (localStorage.getItem('zhuzhen-language') === 'zh') language = 'zh'; } catch {}
const copyAttributes = ['aria-label','alt','title','placeholder'];
const originalText = [];
const originalAttributes = [];
const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, {
 acceptNode(node) {
   return node.parentElement.closest('script, style') || !Object.hasOwn(copyEN,node.data.trim())
     ? NodeFilter.FILTER_REJECT : NodeFilter.FILTER_ACCEPT;
 }
});
while (walker.nextNode()) originalText.push([walker.currentNode,walker.currentNode.data]);
document.querySelectorAll(copyAttributes.map(attr => '['+attr+']').join(',')).forEach(el => {
 for (const attr of copyAttributes) if (Object.hasOwn(copyEN,el.getAttribute(attr))) originalAttributes.push([el,attr,el.getAttribute(attr)]);
});

function ui(text) {
 if (language !== 'en') return text;
 if (Object.hasOwn(copyEN,text)) return copyEN[text];
 const translate = [
   [/^错误：(.*)$/s,(_,v)=>'Error: '+ui(v)],
   [/^无法播放视频：(.*)$/s,(_,v)=>'Could not play video: '+ui(v)],
   [/^自动识别到 (\d+) 个区域，请检查并调整动作余量$/,(_,n)=>`Detected ${n} crops. Check their motion clearance.`],
   [/^正在扫描动作 (\d+) \/ (\d+) 帧$/,(_,i,n)=>`Scanning motion frame ${i} of ${n}`],
   [/^已扩大 (\d+) 个区域。$/,(_,n)=>`Expanded ${n} crops.`],
   [/^(.+) · (\d+\.\d+) 秒$/,(_,name,time)=>`${regionLabel(name)} · ${time}s`],
   [/^正在提取 (\d+) \/ (\d+) 帧 · (\d+) 个区域$/,(_,i,n,r)=>`Extracting frame ${i} of ${n} · ${r} crops`],
   [/^完成：(\d+) 个区域，共 (\d+) 张 PNG$/,(_,r,n)=>`Done: ${r} crops · ${n} PNGs`],
   [/^正在处理 (\d+)\/(\d+)：(.*)$/,(_,i,n,r)=>`Processing ${i}/${n}: ${regionLabel(r)}`],
   [/^(.+) 有帧贴边，正在保留贴边帧并复查背景…$/,(_,r)=>`${regionLabel(r)}: keeping frames that touch the edge and checking the background…`],
   [/^完成：(\d+) 个区域(?:。(.+)有主体贴边，已保留这些帧，可打开筛帧检查裁切。)?$/,(_,n,edge)=>`Done: ${n} crops.`+(edge?` Check edge contact in ${regionLabel(edge).replace(/（(\d+) 帧）/g,' ($1 frames)').replace(/等 (\d+) 个区域/,' and other crops ($1 total)')}.`:'')],
   [/^已载入原参考图的 (\d+) 个格位。视频宽高比有变化，请检查是否补边并校正裁框。$/,(_,n)=>`Loaded ${n} saved crops. The video aspect ratio changed. Check for padding and adjust the crops.`],
   [/^已载入原参考图的 (\d+) 个格位。可沿时间轴检查武器和动作余量。$/,(_,n)=>`Loaded ${n} saved crops. Scrub the timeline to check motion clearance.`],
   [/^已准备 (\d+) 个角色格位，选择对应的本地视频后自动套用。$/,(_,n)=>`${n} saved crops will apply when you import the matching video.`],
   [/^(.+) 有帧未能去除背景。请选择与原视频一致的背景类型。$/,(_,r)=>`${regionLabel(r)}: background removal failed in some frames. Choose the source video's key color.`],
   [/^(.+) 的裁框边缘仍有底色残留。请检查背景类型，或沿时间轴检查并调整裁框。$/,(_,r)=>`${regionLabel(r)}: background remains at the crop edge. Check the key color or adjust the crop.`]
 ];
 for (const [pattern,replace] of translate) if (pattern.test(text)) return text.replace(pattern,replace);
 return text;
}
function regionLabel(name) {
 return language === 'en' ? name.replace(/(?:^|(?<=[_、]))区域_(\d+)/g,'Crop $1').replace(/^角色_(\d+_\d+)$/,'Crop $1') : name;
}
function localizedText(element, text) {
 element.dataset.sourceCopy = text;
 element.textContent = ui(text);
}
function paintLanguage() {
 document.documentElement.lang = language === 'zh' ? 'zh-CN' : 'en';
 document.title = ui('逐帧 · 像素素材工作台');
 document.getElementById('language').value = language;
 for (const [node,source] of originalText) node.data = source.replace(source.trim(),ui(source.trim()));
 for (const [el,attr,source] of originalAttributes) el.setAttribute(attr,ui(source));
 document.querySelectorAll('[data-source-copy]').forEach(el => { el.textContent = ui(el.dataset.sourceCopy); });
}
paintLanguage();

const $=id=>document.getElementById(id), canvas=$('canvas'), ctx=canvas.getContext('2d',{willReadFrequently:true}), video=$('video');
let source=null, currentFile=null, kind='', regions=[], fileUrl='', cropDrag=null, sampling=false, busy=false, cancelled=false, engineReady=false, lastEngineJob=null;
let sourceLayout = null, loading = false;
const controls=['grid','detect','clear','export','sample'];
function status(s){localizedText($('status'),s)}
function error(s){status('错误：'+s)}
function validRegion(r){return r.w>0&&r.h>0&&r.x>=0&&r.y>=0&&r.x+r.w<=canvas.width&&r.y+r.h<=canvas.height}
function buttons() {
 controls.forEach(id => $(id).disabled = !source || busy);
 $('export').disabled = !source || busy || !regions.length || regions.some(r => !validRegion(r));
 $('engineExport').disabled = !engineReady || $('export').disabled;
 $('nativeExtract').disabled = !engineReady || $('export').disabled || kind !== 'video';
 $('scanMotion').disabled = $('export').disabled || kind !== 'video';
 $('regions').inert = busy;
 for (const id of ['play','seek','start','end']) $(id).disabled = busy;
}
function seekVideo(t){return new Promise((resolve,reject)=>{if(Math.abs(video.currentTime-t)<0.00001&&video.readyState>=2){resolve();return} let timer=setTimeout(()=>{cleanup();reject(Error('视频定位超时，浏览器可能不支持此文件'))},10000);function cleanup(){clearTimeout(timer);video.removeEventListener('seeked',ok);video.removeEventListener('error',bad)}function ok(){cleanup();resolve()}function bad(){cleanup();reject(Error('无法读取视频帧'))}video.addEventListener('seeked',ok);video.addEventListener('error',bad);video.currentTime=t})}
async function loadFile(file, layout = null) {
 if (!file || busy || loading) return;
 loading = true;
 cropDrag = null;
 motionStatus('');
 canvas.style.cursor = '';
 sourceLayout = null;
 $('workflowInfo').hidden = true;
 video.pause();
 currentFile=file;showWorkspace(false);if(fileUrl)URL.revokeObjectURL(fileUrl);fileUrl=URL.createObjectURL(file);source=null;regions=[];buttons();status('正在读取素材…');try{if(file.type.startsWith('video/')){kind='video';video.src=fileUrl;video.load();await new Promise((ok,fail)=>{video.onloadedmetadata=ok;video.onerror=()=>fail(Error('无法读取视频，请尝试 MP4 或 WebM'))});source=video;canvas.width=video.videoWidth;canvas.height=video.videoHeight;await seekVideo(0);$('timeLabel').textContent='0.00s';$('seek').max=video.duration;$('seek').value=0;$('start').value=0;$('end').value=video.duration.toFixed(3);$('videoControls').hidden=false;$('timelineEmpty').hidden=true;showSourceInfo(); }else if(file.type.startsWith('image/')){kind='image';const img=new Image();img.src=fileUrl;await img.decode();source=img;canvas.width=img.naturalWidth;canvas.height=img.naturalHeight;$('videoControls').hidden=true;$('timelineEmpty').hidden=false;showSourceInfo()}else throw Error('请选择视频或图片');$('dimensions').textContent=`${canvas.width} × ${canvas.height} px`;$('empty').hidden=true;$('canvasWrap').hidden=false;
 if (layout && kind === 'video') applyLayout(layout);
 else detectRegions();
 } catch(e) { source=null; error(e.message); }
 finally { loading=false; buttons(); }
}
function selectFile(event) {
 const file = event.target.files[0];
 if (!file) return;
 event.target.value = '';
 loadFile(file, file.type.startsWith('video/') ? pendingLayout : null);
}
$('file').onchange = $('file2').onchange = selectFile;
const assetDrop = $('assetDrop');
assetDrop.ondragover = event => {
 if (!event.dataTransfer.types.includes('Files')) return;
 event.preventDefault();
 assetDrop.classList.add('is-drop-target');
};
assetDrop.ondragleave = event => {
 if (!assetDrop.contains(event.relatedTarget)) assetDrop.classList.remove('is-drop-target');
};
assetDrop.ondrop = event => {
 event.preventDefault();
 assetDrop.classList.remove('is-drop-target');
 const files = event.dataTransfer.files;
 if (files.length > 1) { error('请一次导入一份素材'); return; }
 if (files.length) loadFile(files[0], files[0].type.startsWith('video/') ? pendingLayout : null);
};

function applyLayout(layout) {
 const planned = SpriteLayout.regions(layout, canvas.width, canvas.height);
 if (!planned.length || planned.some(region => !validRegion(region))) {
   detectRegions();
   status('原格位无法映射到该视频尺寸，已尝试识别当前帧。');
   return;
 }
 sourceLayout = layout;
 regions = planned;
 motionStatus('');
 $('cols').value = layout.cols;
 $('rows').value = layout.rows;
 if (layout.color) {
   $('keyColor').value = layout.color;
   $('keyEnabled').checked = true;
   $('edgeOnly').checked = false;
   const engineKeys = {'#ff00ff':'magenta','#00ff00':'green','#ffffff':'white'};
   $('engineKey').value = engineKeys[layout.color] || 'auto';
 }
 const changedRatio = Math.abs(canvas.width * layout.height / (canvas.height * layout.width) - 1) > 0.02;
 const message = `已载入原参考图的 ${regions.length} 个格位` +
   (changedRatio ? '。视频宽高比有变化，请检查是否补边并校正裁框。' : '。可沿时间轴检查武器和动作余量。');
 localizedText($('workflowInfo'),message);
 $('workflowInfo').hidden = false;
 refresh();
 status(message);
}

function exportRegion(region) {
 const {anchor, ...rest} = region;
 if (!anchor) return rest;
 return {...rest, anchor:{x:anchor.x - region.x,y:anchor.y - region.y}};
}
function referenceInfo() {
 if (!sourceLayout || !regions.some(region => region.cell)) return undefined;
 const {width,height,rows,cols,color} = sourceLayout;
 return {width,height,rows,cols,color};
}
function draw() {
 if (!source) return;
 ctx.clearRect(0,0,canvas.width,canvas.height);
 ctx.drawImage(source,0,0,canvas.width,canvas.height);
 ctx.lineWidth=Math.max(2,canvas.width/450);
 ctx.font=`bold ${Math.max(13,canvas.width/55)}px sans-serif`;
 const handleWidth=7*canvas.width/(canvas.clientWidth || canvas.width);
 const handleHeight=7*canvas.height/(canvas.clientHeight || canvas.height);
 for (const region of regions) {
   const resizing=cropDrag?.region===region;
   const {x,y,w,h}=resizing ? cropDrag.rect : region;
   ctx.strokeStyle=resizing ? '#fff' : validRegion(region) ? '#60efbf' : '#ff6d73';
   ctx.strokeRect(x+.5,y+.5,w-1,h-1);
   if (w>14 && h>=29) {
     const label=regionLabel(region.name);
     ctx.fillStyle='#0c332acc';
     ctx.fillRect(x+4,y+4,Math.min(w-8,ctx.measureText(label).width+14),25);
     ctx.fillStyle='#aaffdf';
     ctx.fillText(label,x+10,y+22,w-14);
   }
   if (!validRegion(region)) continue;
   const cornerWidth=Math.min(handleWidth,w/2);
   const cornerHeight=Math.min(handleHeight,h/2);
   ctx.fillStyle=ctx.strokeStyle;
   for (const left of [x,x+w-cornerWidth]) {
     for (const top of [y,y+h-cornerHeight]) {
       ctx.fillRect(left,top,cornerWidth,cornerHeight);
     }
   }
 }
 if (cropDrag && !cropDrag.region) {
   const {x,y,w,h}=cropDrag.rect;
   ctx.strokeStyle='#fff';
   ctx.setLineDash([7,4]);
   ctx.strokeRect(x,y,w,h);
   ctx.setLineDash([]);
 }
}
function makeGrid(){if(!source)return;let cols=Math.max(1,Math.min(20,parseInt($('cols').value)||1)),rows=Math.max(1,Math.min(20,parseInt($('rows').value)||1));$('cols').value=cols;$('rows').value=rows;regions=[];for(let y=0;y<rows;y++)for(let x=0;x<cols;x++){let x0=Math.round(x*canvas.width/cols),x1=Math.round((x+1)*canvas.width/cols),y0=Math.round(y*canvas.height/rows),y1=Math.round((y+1)*canvas.height/rows);regions.push({name:`角色_${y+1}_${x+1}`,x:x0,y:y0,w:x1-x0,h:y1-y0})}refresh()}
function foregroundMask(data,width,height,tolerance,cleanup=false) {
 const corners=[0,width-1,(height-1)*width,width*height-1].map(index=>data.subarray(index*4,index*4+4));
 const transparent=corners.filter(pixel=>pixel[3]<32).length>=2;
 const [red,green,blue]=[0,1,2].map(channel=>corners.map(pixel=>pixel[channel]).sort((a,b)=>a-b)[1]);
 const preset=cleanup ? backgroundPreset(red,green,blue) : 'auto';
 const colorKey=preset==='green'||preset==='magenta';
 const threshold=tolerance**2;
 const minTint=Math.max(36,125-tolerance);
 const mask=new Uint8Array(width*height);
 let foreground=0;
 for (let index=0;index<mask.length;index++) {
   const offset=index*4;
   if (data[offset+3]<32) continue;
   const r=data[offset],g=data[offset+1],b=data[offset+2];
   const distance=(r-red)**2+(g-green)**2+(b-blue)**2;
   if (transparent || (distance>threshold && !(colorKey && keyTint(r,g,b,preset)>=minTint))) {
     mask[index]=1;
     foreground++;
   }
 }
 return {mask,foreground};
}

// Connected foreground components are merged by proximity; results are proposals, not tracked objects.
function detectRegions(){
 if(!source||busy)return;if(kind==='video'){video.pause();$('play').textContent=ui('▶ 播放原视频')}
 motionStatus('');
 const W=canvas.width,H=canvas.height,scale=Math.min(1,1000/Math.max(W,H)),w=Math.max(1,Math.round(W*scale)),h=Math.max(1,Math.round(H*scale));
 const tmp=document.createElement('canvas');tmp.width=w;tmp.height=h;const c=tmp.getContext('2d',{willReadFrequently:true});c.imageSmoothingEnabled=false;c.drawImage(source,0,0,w,h);
 const tolerance=clamp(Number($('detectTolerance').value)||55,5,200);
 const {mask,foreground}=foregroundMask(c.getImageData(0,0,w,h).data,w,h,tolerance);
 if(foreground>w*h*0.65){refresh();status('无法确定背景：请检查画面四角、调整识别容差，或手动画框');return}
 const stack=new Int32Array(w*h),parts=[];
 for(let i=0;i<mask.length;i++){if(!mask[i])continue;let n=0;stack[n++]=i;mask[i]=0;let x0=w,y0=h,x1=0,y1=0,area=0;while(n){const p=stack[--n],x=p%w,y=(p/w)|0;area++;x0=Math.min(x0,x);x1=Math.max(x1,x);y0=Math.min(y0,y);y1=Math.max(y1,y);for(let yy=Math.max(0,y-1);yy<=Math.min(h-1,y+1);yy++)for(let xx=Math.max(0,x-1);xx<=Math.min(w-1,x+1);xx++){const q=yy*w+xx;if(mask[q]){mask[q]=0;stack[n++]=q}}}if(area>=3)parts.push({x0,y0,x1,y1,area});if(parts.length>400){refresh();status('画面噪点过多，请调整识别容差或手动画框');return}}
 // A modest source-pixel gap rejoins disconnected hands, feet and held equipment.
 const gap=Math.max(3,Math.round(16*scale));let merged=true;
 while(merged){merged=false;outer:for(let i=0;i<parts.length;i++)for(let j=i+1;j<parts.length;j++){const a=parts[i],b=parts[j],dx=Math.max(0,a.x0-b.x1-1,b.x0-a.x1-1),dy=Math.max(0,a.y0-b.y1-1,b.y0-a.y1-1);if(dx<=gap&&dy<=gap){a.x0=Math.min(a.x0,b.x0);a.y0=Math.min(a.y0,b.y0);a.x1=Math.max(a.x1,b.x1);a.y1=Math.max(a.y1,b.y1);a.area+=b.area;parts.splice(j,1);merged=true;break outer}}}
 const minArea=Math.max(6,Math.round(18*scale*scale)),padding=Math.max(0,Math.min(500,Math.round(Number($('detectPadding').value)||0)));
 let found=parts.filter(p=>p.area>=minArea).map(p=>{const x=Math.max(0,Math.floor(p.x0/scale)-padding),y=Math.max(0,Math.floor(p.y0/scale)-padding),right=Math.min(W,Math.ceil((p.x1+1)/scale)+padding),bottom=Math.min(H,Math.ceil((p.y1+1)/scale)+padding);return{x,y,w:right-x,h:bottom-y,cx:(p.x0+p.x1)/2,cy:(p.y0+p.y1)/2}});
 // Group roughly horizontal rows before ordering left-to-right.
 found.sort((a,b)=>a.cy-b.cy);const rows=[];for(const p of found){let row=rows.find(r=>Math.abs(r.cy-p.cy)<Math.max(12,Math.min(p.h*scale,r.height)*0.45));if(!row){row={cy:p.cy,height:p.h*scale,items:[]};rows.push(row)}row.items.push(p)}
 if(!found.length){refresh();status('没有识别到区域；请调整识别容差或手动画框');return}regions=rows.flatMap(r=>r.items.sort((a,b)=>a.cx-b.cx)).map((p,i)=>({name:`区域_${i+1}`,x:p.x,y:p.y,w:p.w,h:p.h}));refresh();status(`自动识别到 ${regions.length} 个区域，请检查并调整动作余量`);
}
$('detect').onclick=detectRegions;
$('grid').onclick=()=>{motionStatus('');makeGrid()};
$('clear').onclick=()=>{regions=[];motionStatus('');refresh()};

function motionStatus(summary,warning='',contacts=[]) {
 $('motionStatus').hidden=!summary && !warning;
 localizedText($('motionSummary'),summary);
 localizedText($('motionWarning'),warning);
 const list=$('motionContacts');
 list.replaceChildren();
 for (const {name,time} of contacts) {
   const button=document.createElement('button');
   button.type='button';
   button.className='textbtn';
   localizedText(button,`${name} · ${time.toFixed(2)} 秒`);
   button.onclick=()=>{
     if (busy || kind!=='video') return;
     $('seek').value=time;
     $('seek').dispatchEvent(new Event('input'));
   };
   list.append(button);
 }
}

function motionEnvelopes(crops,width,height) {
 return crops.map(crop=>{
   const bounds={left:0,top:0,right:width,bottom:height,overlap:false};
   for (const other of crops) {
     if (other===crop) continue;
     const gapX=Math.max(other.x-crop.x-crop.w,crop.x-other.x-other.w);
     const gapY=Math.max(other.y-crop.y-crop.h,crop.y-other.y-other.h);
     // Share the space between each pair without growing across the dividing line.
     if (gapX<0 && gapY<0) {
       bounds.overlap=true;
     } else if (gapX>=gapY) {
       if (crop.x<other.x) bounds.right=Math.min(bounds.right,crop.x+crop.w+Math.floor(gapX/2));
       else bounds.left=Math.max(bounds.left,crop.x-Math.ceil(gapX/2));
     } else {
       if (crop.y<other.y) bounds.bottom=Math.min(bounds.bottom,crop.y+crop.h+Math.floor(gapY/2));
       else bounds.top=Math.max(bounds.top,crop.y-Math.ceil(gapY/2));
     }
   }
   return bounds;
 });
}

function scanForeground(mask,width,window,extent) {
 const {left,top,right,bottom}=window;
 let touchesBoundary=false;
 for (let y=top;y<bottom;y++) {
   for (let x=left;x<right;x++) {
     const index=y*width+x;
     if (!mask[index]) continue;
     // Ignore isolated compression specks while retaining thin, connected lines.
     if (!(x>0 && mask[index-1]) && !(x<width-1 && mask[index+1])
         && !mask[index-width] && !mask[index+width]) continue;
     extent.left=Math.min(extent.left,x);
     extent.top=Math.min(extent.top,y);
     extent.right=Math.max(extent.right,x+1);
     extent.bottom=Math.max(extent.bottom,y+1);
     if (x-left<=1 || right-x<=2 || y-top<=1 || bottom-y<=2) touchesBoundary=true;
   }
 }
 return touchesBoundary;
}

$('scanMotion').onclick=async()=>{
 if (busy || loading || !source || kind!=='video' || $('scanMotion').disabled) return;
 const start=Number($('start').value);
 const end=Number($('end').value);
 if (!Number.isFinite(start) || !Number.isFinite(end) || start<0 || end<=start || end>video.duration+0.001) {
   motionStatus('请检查扫描时间范围。');
   return;
 }

 const originalTime=video.currentTime;
 const original=regions;
 const width=canvas.width;
 const height=canvas.height;
 const envelopes=motionEnvelopes(original,width,height);
 const overlapWarning='重叠的裁框保留原尺寸，请分别检查。';
 if (envelopes.every(bounds=>bounds.overlap)) {
   motionStatus(overlapWarning);
   return;
 }
 const analysis=document.createElement('canvas');
 const scale=Math.min(1,720/Math.max(width,height));
 analysis.width=Math.max(1,Math.round(width*scale));
 analysis.height=Math.max(1,Math.round(height*scale));
 const scaleX=analysis.width/width;
 const scaleY=analysis.height/height;
 const context=analysis.getContext('2d',{willReadFrequently:true});
 context.imageSmoothingEnabled=false;
 const windows=envelopes.map(bounds=>({
   left:Math.round(bounds.left*scaleX),right:Math.round(bounds.right*scaleX),
   top:Math.round(bounds.top*scaleY),bottom:Math.round(bounds.bottom*scaleY),
 }));
 const extents=envelopes.map(()=>({left:Infinity,top:Infinity,right:-Infinity,bottom:-Infinity}));
 const tolerance=clamp(Number($('detectTolerance').value)||55,5,200);
 const samples=Math.min(600,Math.ceil((end-start)*30));
 const margin=Math.min(6,Math.max(0,Math.round(Number($('detectPadding').value)||0)));
 const contacts=new Map();

 video.pause();
 $('play').textContent=ui('▶ 播放原视频');
 busy=true;
 cancelled=false;
 buttons();
 localizedText($('cancel'),'取消扫描');
 $('cancel').hidden=false;
 try {
   for (let index=0;index<samples;index++) {
     if (cancelled) throw Error('已取消');
     if (index%8===0) motionStatus(`正在扫描动作 ${index+1} / ${samples} 帧`);
     const time=start+(index+0.5)*(end-start)/samples;
     await seekVideo(Math.min(time,video.duration-0.00001));
     context.drawImage(video,0,0,analysis.width,analysis.height);
     const pixels=context.getImageData(0,0,analysis.width,analysis.height);
     const {mask,foreground}=foregroundMask(pixels.data,analysis.width,analysis.height,tolerance,true);
     if (foreground>mask.length*0.65) throw Error('所选时段无法可靠识别底色，请检查背景和识别容差。');
     windows.forEach((window,regionIndex)=>{
       if (envelopes[regionIndex].overlap) return;
       const touches=scanForeground(mask,analysis.width,window,extents[regionIndex]);
       if (touches && !contacts.has(regionIndex)) contacts.set(regionIndex,{name:original[regionIndex].name,time});
     });
   }
   if (cancelled) throw Error('已取消');
   if (regions!==original) throw Error('扫描期间裁框已变更，请重新扫描。');

   let changed=0;
   regions=original.map((region,index)=>{
     const bounds=envelopes[index];
     const extent=extents[index];
     if (bounds.overlap || !Number.isFinite(extent.left)) return region;
     const x=Math.max(bounds.left,Math.min(region.x,Math.floor(extent.left/scaleX)-margin));
     const y=Math.max(bounds.top,Math.min(region.y,Math.floor(extent.top/scaleY)-margin));
     const right=Math.min(bounds.right,Math.max(region.x+region.w,Math.ceil(extent.right/scaleX)+margin));
     const bottom=Math.min(bounds.bottom,Math.max(region.y+region.h,Math.ceil(extent.bottom/scaleY)+margin));
     const w=right-x;
     const h=bottom-y;
     if (x===region.x && y===region.y && w===region.w && h===region.h) return region;
     changed++;
     return {...region,x,y,w,h};
   });
   const warning=contacts.size ? '动作触及扫描边界。点击时间查看，必要时单独裁出特效。'
     : envelopes.some(bounds=>bounds.overlap) ? overlapWarning : '';
   motionStatus(changed ? `已扩大 ${changed} 个区域。` : '没有区域需要扩大。',warning,contacts.values());
 } catch (failure) {
   motionStatus(failure.message);
 } finally {
   try { await seekVideo(originalTime); } catch {}
   busy=false;
   $('cancel').hidden=true;
   localizedText($('cancel'),'取消提取');
   refresh();
 }
};

function refresh(){draw();renderRegions();renderPreviews();buttons()}
function renderRegions(){const el=$('regions');el.replaceChildren();if(!regions.length){el.textContent=ui('暂无区域，请拖动画框');return}regions.forEach((r,i)=>{const box=document.createElement('div');box.className='region';const top=document.createElement('div');top.className='region-top';const name=document.createElement('input');name.type='text';name.value=regionLabel(r.name);name.setAttribute('aria-label',ui('区域名称'));name.oninput=()=>{r.name=name.value;draw();renderPreviews()};const del=document.createElement('button');del.textContent='×';del.title=ui('删除区域');del.onclick=()=>{regions.splice(i,1);refresh()};top.append(name,del);box.append(top);const coord=document.createElement('div');coord.className='coords';[['x','X'],['y','Y'],['w','宽'],['h','高']].forEach(([key,label])=>{const l=document.createElement('label');l.textContent=ui(label);const n=document.createElement('input');n.type='number';n.value=r[key];n.min=key==='w'||key==='h'?1:0;n.onchange=()=>{r[key]=Math.round(Number(n.value));refresh()};l.append(n);coord.append(l)});box.append(coord);el.append(box)})}
function clamp(value,min,max) {
 return Math.max(min,Math.min(max,value));
}

function canvasPoint(event) {
 const bounds=canvas.getBoundingClientRect();
 const scaleX=bounds.width/canvas.width;
 const scaleY=bounds.height/canvas.height;
 return {x:(event.clientX-bounds.left)/scaleX,y:(event.clientY-bounds.top)/scaleY,scaleX,scaleY};
}

function resizeTarget({x,y,scaleX,scaleY}) {
 const hitRadius=8;
 let nearest=null;
 let bestDistance=Infinity;
 for (const region of regions) {
   if (!validRegion(region)) continue;
   const right=region.x+region.w;
   const bottom=region.y+region.h;
   const horizontal=x-region.x<=right-x ? 'w' : 'e';
   const vertical=y-region.y<=bottom-y ? 'n' : 's';
   const dx=Math.abs(x-(horizontal==='w' ? region.x : right))*scaleX;
   const dy=Math.abs(y-(vertical==='n' ? region.y : bottom))*scaleY;
   const insideX=x>=region.x && x<=right;
   const insideY=y>=region.y && y<=bottom;
   if ((!insideX && dx>hitRadius) || (!insideY && dy>hitRadius)) continue;
   const xSide=dx<=hitRadius ? horizontal : '';
   const ySide=dy<=hitRadius ? vertical : '';
   if (!xSide && !ySide) continue;
   // In a shared gutter, prefer the box on the pointer's side of the border.
   const distance=Math.max(xSide ? dx : 0,ySide ? dy : 0)+(insideX && insideY ? 0 : hitRadius);
   if (distance>bestDistance) continue;
   nearest={region,xSide,ySide,cursor:`${ySide}${xSide}-resize`};
   bestDistance=distance;
 }
 return nearest;
}

function updateCropDrag(point) {
 const {region,start,xSide,ySide}=cropDrag;
 if (region) {
   const dx=Math.round(point.x-start.x);
   const dy=Math.round(point.y-start.y);
   const right=region.x+region.w;
   const bottom=region.y+region.h;
   const x=xSide==='w' ? clamp(region.x+dx,0,right-1) : region.x;
   const y=ySide==='n' ? clamp(region.y+dy,0,bottom-1) : region.y;
   const endX=xSide==='e' ? clamp(right+dx,x+1,canvas.width) : right;
   const endY=ySide==='s' ? clamp(bottom+dy,y+1,canvas.height) : bottom;
   cropDrag.rect={x,y,w:endX-x,h:endY-y};
 } else {
   const x=clamp(Math.round(point.x),0,canvas.width);
   const y=clamp(Math.round(point.y),0,canvas.height);
   const startX=clamp(Math.round(start.x),0,canvas.width);
   const startY=clamp(Math.round(start.y),0,canvas.height);
   cropDrag.rect={x:Math.min(x,startX),y:Math.min(y,startY),w:Math.abs(x-startX),h:Math.abs(y-startY)};
 }
}

canvas.onpointerdown=event=>{
 if (!source || busy || cropDrag || event.button!==0) return;
 const point=canvasPoint(event);
 if (sampling) {
   sampleBackground(point);
   return;
 }
 const target=resizeTarget(point);
 cropDrag={...target,pointerId:event.pointerId,start:point};
 updateCropDrag(point);
 canvas.style.cursor=target?.cursor || '';
 canvas.setPointerCapture(event.pointerId);
 draw();
};

canvas.onpointermove=event=>{
 if (!source || busy) return;
 const point=canvasPoint(event);
 if (cropDrag) {
   if (cropDrag.pointerId!==event.pointerId) return;
   updateCropDrag(point);
   draw();
 } else {
   canvas.style.cursor=sampling ? '' : resizeTarget(point)?.cursor || '';
 }
};

canvas.onpointerup=event=>{
 if (cropDrag?.pointerId!==event.pointerId) return;
 updateCropDrag(canvasPoint(event));
 const {region,rect}=cropDrag;
 cropDrag=null;
 if (!busy) {
   if (region && regions.includes(region)) Object.assign(region,rect);
   if (!region && rect.w>=2 && rect.h>=2) regions.push({name:`区域_${regions.length+1}`,...rect});
 }
 canvas.style.cursor='';
 refresh();
};

canvas.onpointercancel=canvas.onlostpointercapture=event=>{
 if (cropDrag?.pointerId!==event.pointerId) return;
 cropDrag=null;
 canvas.style.cursor='';
 draw();
};

$('sample').onclick=()=>{sampling=!sampling;canvas.style.cursor='';$('sample').textContent=ui(sampling?'点击画布选择颜色':'吸取背景色')};
$('play').onclick=async()=>{if(video.paused){try{await video.play();$('play').textContent=ui('Ⅱ 暂停');previewTick()}catch(e){error('无法播放视频：'+e.message)}}else{video.pause();$('play').textContent=ui('▶ 播放原视频')}};
function previewTick(){if(video.paused||busy)return;$('seek').value=video.currentTime;$('timeLabel').textContent=video.currentTime.toFixed(2)+'s';draw();renderPreviews();setTimeout(previewTick,120)}
video.onended=()=>{$('play').textContent=ui('▶ 播放原视频')};
$('seek').oninput=async e=>{if(busy)return;video.pause();$('play').textContent=ui('▶ 播放原视频');try{await seekVideo(Number(e.target.value));$('timeLabel').textContent=video.currentTime.toFixed(2)+'s';draw();renderPreviews()}catch(err){error(err.message)}};
['keyEnabled','keyColor','tolerance','edgeOnly','cleanSpill'].forEach(id=>$(id).oninput=()=>{$('tolValue').textContent=$('tolerance').value;renderPreviews()});
function keyTint(red, green, blue, key) {
 const tint = key === 'magenta' ? Math.min(red, blue) - green : green - Math.max(red, blue);
 return Math.abs(red - blue) <= Math.max(24, tint * 0.6) ? tint : 0;
}

function backgroundPreset(red, green, blue) {
 if (keyTint(red, green, blue, 'magenta') >= 72) return 'magenta';
 if (keyTint(red, green, blue, 'green') >= 72) return 'green';
 if (Math.min(red, green, blue) >= 220) return 'white';
 return 'auto';
}

function sampleBackground(point) {
 const x = clamp(Math.floor(point.x), 0, canvas.width - 1);
 const y = clamp(Math.floor(point.y), 0, canvas.height - 1);
 const left = Math.max(0, x - 3);
 const top = Math.max(0, y - 3);
 const patch = document.createElement('canvas');
 patch.width = Math.min(canvas.width, x + 4) - left;
 patch.height = Math.min(canvas.height, y + 4) - top;
 const context = patch.getContext('2d', {willReadFrequently:true});
 context.drawImage(source, left, top, patch.width, patch.height, 0, 0, patch.width, patch.height);
 const {data} = context.getImageData(0, 0, patch.width, patch.height);
 const center = ((y - top) * patch.width + x - left) * 4;
 if (data[center + 3] < 128) {
   status('这里已经透明，请点击有颜色的底色。');
   return;
 }
 const rgb = [0, 1, 2].map(channel => {
   const values = [];
   for (let offset = 0; offset < data.length; offset += 4) {
     if (data[offset + 3] >= 128) values.push(data[offset + channel]);
   }
   values.sort((a, b) => a - b);
   return values[Math.floor(values.length / 2)];
 });
 $('keyColor').value = '#' + rgb.map(channel => channel.toString(16).padStart(2, '0')).join('');
 $('engineKey').value = backgroundPreset(...rgb);
 $('keyEnabled').checked = true;
 sampling = false;
 $('sample').textContent = ui('吸取背景色');
 renderPreviews();
 status('已吸取背景色，预览已更新。');
}

function clearEdgeBackground(data, matches, width, height) {
 const queue = new Int32Array(matches.length);
 let head = 0;
 let tail = 0;
 function add(index) {
   if (matches[index] !== 1) return;
   matches[index] = 2;
   queue[tail++] = index;
 }
 for (let x = 0; x < width; x++) {
   add(x);
   add((height - 1) * width + x);
 }
 for (let y = 0; y < height; y++) {
   add(y * width);
   add(y * width + width - 1);
 }
 while (head < tail) {
   const index = queue[head++];
   const x = index % width;
   data[index * 4 + 3] = 0;
   if (x > 0) add(index - 1);
   if (x < width - 1) add(index + 1);
   if (index >= width) add(index - width);
   if (index < matches.length - width) add(index + width);
 }
}

function cleanKeyFringe(data, matches, width, key) {
 for (let index = 0; index < matches.length; index++) {
   const offset = index * 4;
   if (matches[index] || !data[offset + 3]) continue;
   const x = index % width;
   // Only adjust a one-pixel fringe next to background removed by this pass.
   if (!(x > 0 && matches[index - 1] === 2)
       && !(x < width - 1 && matches[index + 1] === 2)
       && matches[index - width] !== 2 && matches[index + width] !== 2) continue;
   const spill = keyTint(data[offset], data[offset + 1], data[offset + 2], key) - 8;
   if (spill <= 0) continue;
   if (key === 'magenta') {
     data[offset] -= spill;
     data[offset + 2] -= spill;
   } else {
     data[offset + 1] -= spill;
   }
 }
}

function processRegion(region) {
 const crop = document.createElement('canvas');
 const {x, y, w:width, h:height} = region;
 crop.width = width;
 crop.height = height;
 const context = crop.getContext('2d', {willReadFrequently:true});
 context.drawImage(source, x, y, width, height, 0, 0, width, height);
 if (!$('keyEnabled').checked) return crop;

 const image = context.getImageData(0, 0, width, height);
 const {data} = image;
 const color = $('keyColor').value;
 const [red, green, blue] = [1, 3, 5].map(index => parseInt(color.slice(index, index + 2), 16));
 const preset = backgroundPreset(red, green, blue);
 const cleanSpill = $('cleanSpill').checked && (preset === 'magenta' || preset === 'green');
 const tolerance = Number($('tolerance').value);
 const squaredTolerance = tolerance ** 2;
 const tintThreshold = Math.max(36, 125 - tolerance);
 const matches = new Uint8Array(width * height);
 for (let index = 0; index < matches.length; index++) {
   const offset = index * 4;
   const r = data[offset], g = data[offset + 1], b = data[offset + 2];
   const distance = (r - red) ** 2 + (g - green) ** 2 + (b - blue) ** 2;
   if (data[offset + 3] && (distance <= squaredTolerance
       || (cleanSpill && keyTint(r, g, b, preset) >= tintThreshold))) matches[index] = 1;
 }

 if ($('edgeOnly').checked) {
   clearEdgeBackground(data, matches, width, height);
 } else {
   for (let index = 0; index < matches.length; index++) {
     if (!matches[index]) continue;
     data[index * 4 + 3] = 0;
     matches[index] = 2;
   }
 }
 if (cleanSpill) cleanKeyFringe(data, matches, width, preset);
 context.putImageData(image, 0, 0);
 return crop;
}
function renderPreviews(){const el=$('previews');el.replaceChildren();const good=regions.filter(validRegion);if(!source||!good.length){el.innerHTML='<div class="preview-empty">'+ui('划分有效区域后，在这里检查画面与透明边缘')+'</div>';return}good.forEach(r=>{const box=document.createElement('div');box.className='preview-card';box.append(processRegion(r));const label=document.createElement('span');label.textContent=`${regionLabel(r.name)} · ${r.w}×${r.h}`;box.append(label);el.append(box)})}
const crcTable=(()=>{let t=new Uint32Array(256);for(let n=0;n<256;n++){let c=n;for(let k=0;k<8;k++)c=(c&1)?0xedb88320^(c>>>1):c>>>1;t[n]=c>>>0}return t})();
function crc32(bytes){let c=0xffffffff;for(const b of bytes)c=crcTable[(c^b)&255]^(c>>>8);return (c^0xffffffff)>>>0}
function record(n){return new Uint8Array(n)}function put16(a,o,n){new DataView(a.buffer).setUint16(o,n,true)}function put32(a,o,n){new DataView(a.buffer).setUint32(o,n>>>0,true)}
function zip(files){const encoder=new TextEncoder(),chunks=[],directory=[];let offset=0;for(const f of files){const name=encoder.encode(f.name),data=f.data,crc=crc32(data),h=record(30);put32(h,0,0x04034b50);put16(h,4,20);put16(h,6,0x800);put32(h,14,crc);put32(h,18,data.length);put32(h,22,data.length);put16(h,26,name.length);chunks.push(h,name,data);const d=record(46);put32(d,0,0x02014b50);put16(d,4,20);put16(d,6,20);put16(d,8,0x800);put32(d,16,crc);put32(d,20,data.length);put32(d,24,data.length);put16(d,28,name.length);put32(d,42,offset);directory.push(d,name);offset+=h.length+name.length+data.length}const centralSize=directory.reduce((a,b)=>a+b.length,0),end=record(22);put32(end,0,0x06054b50);put16(end,8,files.length);put16(end,10,files.length);put32(end,12,centralSize);put32(end,16,offset);return new Blob([...chunks,...directory,end],{type:'application/zip'})}
function png(c){return new Promise((resolve,reject)=>c.toBlob(b=>b?b.arrayBuffer().then(a=>resolve(new Uint8Array(a)),reject):reject(Error('PNG 编码失败')),'image/png'))}
function safeName(s,i){return (s.trim().replace(/[\\/:*?"<>|\x00-\x1f]/g,'_').replace(/^\.+$/,'').slice(0,80)||`region_${i+1}`)}
$('cancel').onclick=()=>{cancelled=true;status('正在取消…')};
$('export').onclick=async()=>{if(busy||!source)return;const fps=Number($('fps').value),start=Number($('start').value),end=Number($('end').value);if(regions.some(r=>!validRegion(r))){error('区域坐标超出画面');return}if(kind==='video'&&(!Number.isFinite(fps)||fps<0.1||fps>60||!Number.isFinite(start)||!Number.isFinite(end)||start<0||end>video.duration+0.001||start>=end)){error('请检查时间范围和帧率（0.1–60）');return}const count=kind==='video'?Math.ceil((end-start)*fps-1e-9):1;if(count*regions.length>10000){error('单次最多导出 10000 张图，请缩短时间或减少区域');return}if(kind==='video'){video.pause();$('play').textContent=ui('▶ 播放原视频')}busy=true;cancelled=false;buttons();$('cancel').hidden=false;const originalTime=kind==='video'?video.currentTime:0;try{const files=[],names=regions.map((r,i)=>`${String(i+1).padStart(2,'0')}_${safeName(r.name,i)}`),times=[];for(let i=0;i<count;i++){if(cancelled)throw Error('已取消');const t=kind==='video'?start+i/fps:0;if(kind==='video')await seekVideo(Math.min(t,Math.max(0,video.duration-0.00001)));times.push(t);for(let j=0;j<regions.length;j++){if(cancelled)throw Error('已取消');files.push({name:`${names[j]}/${String(i).padStart(4,'0')}.png`,data:await png(processRegion(regions[j]))})}status(`正在提取 ${i+1} / ${count} 帧 · ${regions.length} 个区域`);await new Promise(resolve=>setTimeout(resolve,0))}const manifest={version:1,source:currentFile.name,type:kind,sourceSize:{width:canvas.width,height:canvas.height},sampling:kind==='video'?{start,end,fps,frameCount:count,timestamps:times,method:'browser time seeking; exact decoded frame timestamps are not guaranteed'}:{frameCount:1},background:{enabled:$('keyEnabled').checked,color:$('keyColor').value,tolerance:Number($('tolerance').value),edgeConnectedOnly:$('edgeOnly').checked,cleanSpill:$('cleanSpill').checked},referenceLayout:referenceInfo(),regions:regions.map((r,i)=>({...exportRegion(r),folder:names[i]}))};files.push({name:'manifest.json',data:new TextEncoder().encode(JSON.stringify(manifest,null,2))});const blob=zip(files),link=document.createElement('a');link.href=URL.createObjectURL(blob);link.download='sprite-frames.zip';link.click();setTimeout(()=>URL.revokeObjectURL(link.href),60000);status(`完成：${regions.length} 个区域，共 ${count*regions.length} 张 PNG`)}catch(e){error(e.message)}finally{if(kind==='video')try{await seekVideo(originalTime)}catch(e){}busy=false;$('cancel').hidden=true;refresh()}};

async function engineStatus(){try{const res=await fetch('/api/status');if(!res.ok)throw Error();engineReady=(await res.json()).available;localizedText($('engineState'),engineReady?'已就绪':'未安装');}catch(e){engineReady=false;localizedText($('engineState'),'需要本地服务');}buttons()}
engineStatus();
function showSourceInfo() {
 if (!currentFile || !source) return;
 $('sourceInfo').textContent = kind === 'video'
   ? `${currentFile.name} · ${video.duration.toFixed(2)} ${ui('秒')}`
   : currentFile.name;
}

const curationFrame = $('curationFrame');
let curationOrigin = null, curationJob = null, curationTimeout = null;
function showWorkspace(curating) {
 $('extractionPanel').hidden = curating;
 $('curationPanel').hidden = !curating;
 $('extractTab').toggleAttribute('aria-current', !curating);
 $('curationTab').toggleAttribute('aria-current', curating);
 $(curating ? 'curationTab' : 'extractTab').setAttribute('aria-current','page');
}
function curationMessage(text, retry = false) {
 localizedText($('curationStatus'),text);
 $('retryCuration').hidden = !retry;
}
let curationDuration = 0;
function setCurationJob(id, report, duration = 0) {
 lastEngineJob = id;
 curationDuration = duration;
 $('openCuration').hidden = false;
 $('curationTab').disabled = false;
 $('rawFrames').href = `/api/jobs/${id}/download`;
 localizedText($('curationReport'),report || '');
 try {
   sessionStorage.setItem('zhuzhen-curation-job',id);
   sessionStorage.setItem('zhuzhen-curation-duration',String(duration));
 } catch {}
}
async function openCuration() {
 const id = lastEngineJob;
 if (!id) return;
 showWorkspace(true);
 if (curationJob === id) return;
 curationJob = id;
 curationOrigin = null;
 clearTimeout(curationTimeout);
 curationFrame.hidden = true;
 curationMessage('正在准备帧筛选界面…');
 try {
   const res = await fetch(`/api/jobs/${id}/curation`,{method:'POST',headers:{'X-Sprite-Studio':'1'}});
   const data = await res.json();
   if (!res.ok) throw Error(data.error || '无法加载筛帧界面');
   if (curationJob !== id) return;
   const url = new URL(data.url);
   curationOrigin = url.origin;
   url.searchParams.set('embed','1');
   url.searchParams.set('parentOrigin',location.origin);
   url.searchParams.set('lang',language);
   if (curationDuration > 0) url.searchParams.set('sourceSeconds',String(curationDuration));
   curationFrame.src = url.href;
   curationFrame.hidden = false;
   curationTimeout = setTimeout(() => {
     curationJob = null;
     curationMessage('筛帧界面加载超时，请重试。',true);
   },45000);
 } catch (e) {
   if (curationJob !== id) return;
   curationJob = null;
   curationMessage('错误：'+e.message,true);
 }
}
function syncCurationLanguage() {
 if (curationOrigin) curationFrame.contentWindow.postMessage({type:'zhuzhen:language',language},curationOrigin);
}
window.addEventListener('message',event => {
 if (event.source !== curationFrame.contentWindow || event.origin !== curationOrigin) return;
 if (event.data?.type === 'zhuzhen:curation-ready') {
   clearTimeout(curationTimeout);
   if (event.data.loaded) {
     curationMessage('');
     if (event.data.language !== language) syncCurationLanguage();
   } else {
     curationJob = null;
     curationMessage('无法加载筛帧界面',true);
   }
 } else if (event.data?.type === 'zhuzhen:export-selected' && event.ports[0]) {
   exportSelected(event.ports[0]);
 }
});
let exportingSelection = false;
async function exportSelected(port) {
 const id = curationJob;
 if (!id || id !== lastEngineJob || exportingSelection) {
   port.postMessage({ok:false,error:ui('无法导出筛选后的帧')});
   port.close();
   return;
 }
 exportingSelection = true;
 curationMessage('正在导出筛选后的帧…');
 try {
   const res = await fetch(`/api/jobs/${id}/export-curated`,{method:'POST',headers:{'X-Sprite-Studio':'1'}});
   const data = await res.json();
   if (!res.ok) throw Error(data.error || '无法导出筛选后的帧');
   const link = document.createElement('a');
   link.href = data.url;
   link.download = 'sprite-gen-curated.zip';
   link.click();
   curationMessage('筛选后的帧已导出');
   port.postMessage({ok:true});
 } catch (e) {
   curationMessage('错误：'+e.message);
   port.postMessage({ok:false,error:ui(e.message)});
 } finally {
   exportingSelection = false;
   port.close();
 }
}
$('extractTab').onclick = () => showWorkspace(false);
$('curationTab').onclick = $('openCuration').onclick = $('retryCuration').onclick = openCuration;
$('language').onchange = event => {
 language = event.target.value;
 try { localStorage.setItem('zhuzhen-language',language); } catch {}
 paintLanguage();
 if (source) {
   showSourceInfo();
   draw();
   renderRegions();
   renderPreviews();
 }
 $('play').textContent = ui(video.paused ? '▶ 播放原视频' : 'Ⅱ 暂停');
 $('sample').textContent = ui(sampling ? '点击画布选择颜色' : '吸取背景色');
 syncCurationLanguage();
};
$('importLayout').onclick = () => $('layoutFile').click();
$('layoutFile').onchange = async event => {
 const file = event.target.files[0];
 event.target.value = '';
 if (!file) return;
 if (busy || loading) { error('提取期间无法更换格位。'); return; }
 try {
   if (file.size > 1024 * 1024) throw Error();
   const layout = JSON.parse(await file.text());
   if (!SpriteLayout.valid(layout)) throw Error();
   pendingLayout = layout;
   $('clearLayout').hidden = false;
   if (source && kind === 'video') {
     video.pause();
     $('play').textContent = ui('▶ 播放原视频');
     applyLayout(layout);
   } else {
     localizedText($('workflowInfo'),`已准备 ${layout.cells.length} 个角色格位，选择对应的本地视频后自动套用。`);
     $('workflowInfo').hidden = false;
   }
 } catch { error('格位文件无效'); }
};
$('clearLayout').onclick = () => {
 if (busy || loading) { error('提取期间无法更换格位。'); return; }
 pendingLayout = null;
 $('clearLayout').hidden = true;
 $('workflowInfo').hidden = true;
 status('已清除格位文件。当前裁框可继续编辑。');
};
(async () => {
 try {
   const id = sessionStorage.getItem('zhuzhen-curation-job');
   if (!/^[a-f0-9]{32}$/.test(id || '')) return;
   const res = await fetch(`/api/jobs/${id}`);
   if (!res.ok) return;
   const job = await res.json();
   const duration = Number(sessionStorage.getItem('zhuzhen-curation-duration'));
   if (job.state === 'done' && !lastEngineJob) setCurationJob(id,job.message,duration);
 } catch {}
})();

async function extractWithEngine(mode = 'uniform') {
 if (!engineReady || !source || busy) return;
 const fps = mode === 'native' ? 10 : Number($('fps').value);
 const start = kind === 'video' ? Number($('start').value) : 0;
 const end = kind === 'video' ? Number($('end').value) : 0;
 if (!Number.isFinite(fps)||fps<0.1||fps>60||(kind==='video'&&(!Number.isFinite(start)||!Number.isFinite(end)||start<0||start>=end||end>video.duration+0.001))) {
   error('请检查时间范围和帧率');
   return;
 }
 if (kind==='video') {
   video.pause();
   $('play').textContent=ui('▶ 播放原视频');
 }
 busy=true;
 buttons();
 status('正在发送素材到本地引擎…');
 try {
   const options={kind,samplingMode:mode,key:$('engineKey').value,fps,start,end,width:canvas.width,height:canvas.height,referenceLayout:referenceInfo(),regions:regions.map(exportRegion)};
   const response=await fetch('/api/jobs',{method:'POST',headers:{'X-Sprite-Studio':'1','X-Options':encodeURIComponent(JSON.stringify(options))},body:currentFile});
   const data=await response.json();
   if (!response.ok) throw Error(data.error||'无法启动引擎');
   while (true) {
     await new Promise(resolve=>setTimeout(resolve,700));
     const res=await fetch('/api/jobs/'+data.id);
     if (!res.ok) throw Error('无法读取任务状态');
     const job=await res.json();
     status(job.message);
     if (job.state==='error') throw Error(job.message);
     if (job.state==='done') {
       setCurationJob(data.id,job.message,end-start);
       if (mode !== 'native') $('rawFrames').click();
       await openCuration();
       break;
     }
   }
 } catch (e) { error(e.message); }
 finally { busy=false; buttons(); }
}
$('engineExport').onclick = () => extractWithEngine();
$('nativeExtract').onclick = () => extractWithEngine('native');

// The styled file picker labels also support keyboard activation.
document.querySelectorAll('.upload[tabindex]').forEach(label=>label.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();label.querySelector('input[type=file]').click()}}));

// The task keeps its own reference layout even if the production graph is later edited.
let pendingLayout = null;
(async () => {
 const query = new URLSearchParams(location.search);
 if (query.has('workflow')) {
   try { pendingLayout = JSON.parse(sessionStorage.getItem(SpriteLayout.handoffKey)); }
   catch { pendingLayout = null; }
   if (pendingLayout?.cells?.length) {
     localizedText($('workflowInfo'),`已准备 ${pendingLayout.cells.length} 个角色格位，选择对应的本地视频后自动套用。`);
     $('workflowInfo').hidden = false;
     localizedText($('empty').querySelector('h2'),'导入对应的成片');
     localizedText($('empty').querySelector('p'),'导入后会自动沿用角色名、格位和背景色。');
     status('等待导入对应的本地视频');
   }
   return;
 }
 const id = query.get('wanTask');
 if (!id) return;
 if (!/^[a-f0-9]{32}$/.test(id)) { error('无效的视频任务编号'); return; }
 try {
   status('正在载入已生成视频…');
   const [meta, response] = await Promise.all([
     fetch(`/api/wan/tasks/${id}`),
     fetch(`/api/wan/tasks/${id}/video`)
   ]);
   if (!response.ok) throw Error('视频不存在或尚未生成');
   const task = meta.ok ? await meta.json() : null;
   const blob = await response.blob();
   await loadFile(new File([blob],'wan-generated.mp4',{type:'video/mp4'}), task?.layout);
 } catch (e) { error(e.message); }
})();
