# CHANGELOG v1.0 · 2026-10-08 — v014 보존과4시간대·별·천체·효과 계약을 검사합니다.
from pathlib import Path
import json,hashlib,sys,struct,importlib.util,ast
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parent;PKG=ROOT/'unreal-full';REF=ROOT/'incoming/to_chatgpt/02_current_v014'
sys.path.insert(0,str(PKG));from layer_layout import *
m=json.loads((PKG/'manifest.json').read_text(encoding='utf-8'));old=json.loads((REF/'manifest.json').read_text(encoding='utf-8'))
results=[]
def check(name,ok):results.append({'검사':name,'통과':bool(ok)})
def rgba(file):return np.asarray(Image.open(file).convert('RGBA'))
def sha(file):return hashlib.sha256(file.read_bytes()).hexdigest()
check('manifest 개수',len(m['assets'])==90 and len(m['fx'])==4 and len(m['render_order'])==16)
check('Textures94개',len(list((PKG/'Textures').glob('*.png')))==94)
check('옛 별 파일 제거',not list((PKG/'Textures').glob('*_Stars.png')))
check('시간대와목적지',m['version']==15 and m['phases']==list(PHASES) and m['destination']=='/Game/Art/PixelLandscape_v015')
for key in ['zoom_policy','ground_y','canvas','regions','depth_order_front_to_back']:check(key+' 보존',m[key]==old[key])
kept=[]
for a in old['assets']:
 if a['layer']=='stars':continue
 b=next(x for x in m['assets'] if x['name']==a['name'])
 check(a['name']+' SHA256 보존',sha(PKG/b['file'])==sha(REF/a['file'])==a['sha256'])
 check(a['name']+' 배치 보존',all(b[k]==a[k] for k in ['name','size','world_rect','ratio','period','anchor','bind']))
 kept.append(a['file'])
for a in m['assets']+m['fx']:
 p=PKG/a['file'];ar=rgba(p)
 check(a['name']+' 픽셀 크기',list(ar.shape[1::-1])==a['size'])
 check(a['name']+' 이진 알파',set(np.unique(ar[:,:,3]))<={0,255})
 check(a['name']+' 내용 존재',np.any(ar[:,:,3]))
 if 'world_rect' in a:
  check(a['name']+' 월드4배',a['world_rect'][2:]==[x*4 for x in a['size']])
  check(a['name']+' 기하 일치',list(world_geometry(a['layer'],a['size']))==a['world_rect'])
 if a.get('period'):
  check(a['name']+' 좌우 경계',np.array_equal(ar[:,0],ar[:,-1]))
 if a.get('phase') in ['dawn','dusk']:
  day=next(x for x in m['assets'] if x['region']==a['region'] and x['layer']==a['layer'] and x['phase']=='day');dar=rgba(PKG/day['file'])
  check(a['name']+' 낮판 알파 일치',np.array_equal(ar[:,:,3],dar[:,:,3]))
  check(a['name']+' 낮판 배치 일치',all(a[k]==day[k] for k in ['size','world_rect','ratio','period','anchor','bind']))
 if a.get('layer')=='sky':
  check(a['name']+' 하늘 불투명',np.all(ar[:,:,3]==255))
  check(a['name']+' 세로 색만·천체 없음',np.all(ar==ar[:,:1]))
 rp=PKG/'checks'/p.name
 check(a['name']+' 원본 왕복',rp.exists() and np.array_equal(ar,rgba(rp)))
 a['sha256']=sha(p)
star_summary={}
for region in ['Forest','Snow']:
 masks=[rgba(PKG/f'Textures/T_{region}_Stars{x}.png')[:,:,3]>0 for x in 'ABC'];union=np.logical_or.reduce(masks);baseline=rgba(REF/f'Textures/T_{region}_Stars.png')[:,:,3]>0
 check(region+' 별3층 겹침0',np.max(sum(x.astype(int) for x in masks))==1)
 check(region+' 기존별 모두보존',np.all(union[baseline]))
 counts=[int(x.sum()) for x in masks];check(region+' 별개수 A<B<C',0<counts[0]<counts[1]<counts[2])
 star_summary[region]={'pixels_abc':counts,'old_pixels':int(baseline.sum()),'new_pixels':int(union.sum())}
 for layer in ['Sky','Clouds','MountainsFar','MountainsNear','TreesBack','Buildings','TreesFront','StreetTile','LowerBase','CloudsHigh']:
  means=[]
  for phase in ['Dawn','Dusk']:
   ar=rgba(PKG/f'Textures/T_{region}_{layer}_{phase}.png');means.append(float((ar[:,:,:3][ar[:,:,3]>0]@np.array([.2126,.7152,.0722])).mean()))
  check(region+layer+' 새벽·저녁 밝기 차20이하',abs(means[0]-means[1])<=20)
for phase,expected in [('dawn',{'sun':(177,359),'moon':(1691,279)}),('day',{'sun':(960,120),'moon':None}),('dusk',{'sun':(1743,359),'moon':(229,279)}),('night',{'sun':None,'moon':(960,120)})]:
 for body,xy in expected.items():
  got=body_center(body,FIXED_HOURS[phase]);check(phase+body+' 궤도 검산',(got is None and xy is None) or (got is not None and tuple(round(v) for v in got)==xy))
check('달 자정 연속',body_center('moon',0)==body_center('moon',24))
spec=importlib.util.spec_from_file_location('old',REF/'layer_layout.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
for zoom in [.25,.5,.75,1]:
 for camera in [-15360,-7680,-123,0,777,7680,15360]:
  good=True
  for a in m['assets']:
   if a['layer'] in ['sun','moon']:continue
   k='stars' if a['layer'].startswith('stars_') else a['layer'];r=rectangles(a['layer'],a['size'],zoom,camera)
   good &= r==mod.rectangles(k,a['size'],zoom,camera)
   good &= all(r[i][0]+r[i][2]==r[i+1][0] for i in range(len(r)-1))
  check(f'배율{zoom} 카메라{camera} 공통 기하',good)
check('지면208',m['ground_y']==832 and m['ground_y_texel']==208)
for f in m['fx']:
 if 'head_px' in f:
  ar=rgba(PKG/f['file']);x,y=f['head_px'];check(f['id']+' 오른쪽 아래 머리',x>=ar.shape[1]*.75 and y>=ar.shape[0]*.6 and ar[y,x,3]==255)
 if f['id']=='meteor_big_spark':
  ar=rgba(PKG/f['file']);counts=[int((ar[:,i*16:(i+1)*16,3]>0).sum()) for i in range(4)]
  check('반짝임4칸 순서',0<counts[0]<counts[1]<counts[2] and 0<counts[3]<counts[1])
check('구름 흐름값',[(a['id'],a.get('drift_px')) for a in m['render_order'] if a['id'] in ['clouds_high','clouds']]==[('clouds_high',3),('clouds',6)])
for a in m['render_order']:
 if a['id'].startswith('stars_'):
  i='abc'.index(a['id'][-1]);check(a['id']+' 등장·반짝임',a['appear_darkness']==[.2,.5,.8][i] and a['twinkle_period_s']==[2.3,3.1,4.3][i])
for name,size in [('forest',(1920,894)),('snow',(1920,894)),('forest_ground',(120,30)),('snow_ground',(120,30)),('celestial_fx',(160,64))]:
 data=(PKG/'Source'/f'{name}.aseprite').read_bytes();check(name+' 원본크기',struct.unpack_from('<HH',data,8)==size)
for region in m['regions']:
 for phase in PHASES:
  for zoom in [25,100]:
   for suffix in ['','_orbit']:
    p=PKG/'Preview'/f'{region}_{phase}_zoom_{zoom}{suffix}.png';check(p.name+' 화면',p.exists() and Image.open(p).size==(1920,1080))
 for zoom in [25,100]:
  p=PKG/'Preview'/f'{region}_fx_zoom_{zoom}.png';check(p.name+' 화면',p.exists() and Image.open(p).size==(1920,1080))
check('하루 흐름25시각·2지역',(PKG/'Preview/daynight_timeline.png').exists() and Image.open(PKG/'Preview/daynight_timeline.png').size==(12000,584))
ast.parse((PKG/'import_landscape.py').read_text(encoding='utf-8'))
check('가져오기94개·0.25',(PKG/'import_landscape.py').read_text(encoding='utf-8').count('94')>=4 and '"pixels_per_unreal_unit", 0.25' in (PKG/'import_landscape.py').read_text(encoding='utf-8'))
report={'version':15,'passed':all(x['통과'] for x in results),'checks':len(results),'preserved_files':len(kept),'stars':star_summary,'engine_executed':False,'pixel_grid_note':'PNG의 실제 한 픽셀이 작업 격자입니다. 같은 색이 이어지는 면을 금지하는 의미가 아닙니다.','failures':[x for x in results if not x['통과']],'details':results}
(PKG/'package-validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
m['status']='4시간대·천체·효과 파일 검수 완료 · 미술 및 UE 실행 검수 대기' if report['passed'] else '검수 보완 중'
(PKG/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k!='details'},ensure_ascii=True));sys.exit(0 if report['passed'] else 1)
