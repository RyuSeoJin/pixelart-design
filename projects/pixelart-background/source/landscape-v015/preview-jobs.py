# CHANGELOG v1.0 · 2026-10-08 — 시간대·천체·효과 미리보기 좌표를 준비합니다.
from pathlib import Path
import json,sys,math
from PIL import Image
import numpy as np
ROOT=Path(__file__).resolve().parent;PKG=ROOT/'unreal-full';sys.path.insert(0,str(PKG))
from layer_layout import *
m=json.loads((PKG/'manifest.json').read_text(encoding='utf-8'))
# 그림에서 실제 밝은 머리 위치를 찾습니다. 게임이 이 점을 이동 기준으로 사용합니다.
for f in m['fx']:
 if f['id'] in ('meteor','meteor_big'):
  a=np.array(Image.open(PKG/f['file']).convert('RGBA')); l=a[:,:,:3]@np.array([.2126,.7152,.0722]);l[a[:,:,3]==0]=-1
  l[:,:a.shape[1]//2]=-1
  ys,xs=np.where(l==l.max());f['head_px']=[int(round(xs.mean())),int(round(ys.mean()))]
(PKG/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def weights(hour):
 h=hour%24
 for boundary,prev,nxt in [(4,'night','dawn'),(7,'dawn','day'),(17,'day','dusk'),(20,'dusk','night')]:
  distance=(h-boundary+12)%24-12
  if -.25<=distance<=.25:
   t=(distance+.25)/.5;return [(prev,1-t),(nxt,t)]
 return [(('dawn' if h<7 else 'day' if h<17 else 'dusk' if h<20 else 'night') if h>=4 else 'night',1)]
jobs=[]
def make(region,zoom,hour,name,viewport=(1920,1080),overlay=False,fx=False):
 ws=weights(hour);dark=sum(DARKNESS[p]*w for p,w in ws);items=[]
 for layer in m['render_order']:
  k=layer['id']
  if k in ('sun','moon'):
   center=body_center(k,hour)
   if center is None:continue
   a=next(a for a in m['assets'] if a['layer']==k)
   x,y=world_to_screen((center[0]-96,center[1]-96),zoom,parallax=(0,1),viewport=viewport);s=192*zoom*viewport[1]/1080
   items.append(dict(file=a['file'],rects=[[round(x),round(y),round(s),round(s)]],opacity=1 if k=='sun' else .35+.65*dark,body=k))
  elif k.startswith('stars_') or k=='window_lights':
   opacity=dark if k=='window_lights' else min(1,max(0,(dark-layer['appear_darkness'])/.2))
   if opacity==0:continue
   a=next(a for a in m['assets'] if a['layer']==k and a['region']==region)
   items.append(dict(file=a['file'],rects=rectangles(k,a['size'],zoom,0,viewport),opacity=opacity))
  else:
   assets=[next(a for a in m['assets'] if a['layer']==k and a['region']==region and a['phase']==p) for p,w in ws]
   a=assets[0];item=dict(file=a['file'],rects=rectangles(k,a['size'],zoom,0,viewport),opacity=1)
   if len(ws)==2:item.update(blend_file=assets[1]['file'],mix=ws[1][1])
   items.append(item)
  if k=='stars_c' and fx:
   # fx는 별 바로 앞, 해·달·구름·산 뒤에 놓습니다.
   for i,f in enumerate(m['fx']):
    pos=([260,580,0,1450][i],150 if zoom==1 else -1300)
    if f['id']=='meteor_big_glow':
     big=next(f for f in m['fx'] if f['id']=='meteor_big')
     pos=(580+big['head_px'][0]*4-128,(150 if zoom==1 else -1300)+big['head_px'][1]*4-128)
    x,y=world_to_screen(pos,zoom,parallax=(0,1),viewport=viewport)
    w,h=[s*4*zoom*viewport[1]/1080 for s in f['size']]
    items.append(dict(file=f['file'],rects=[[round(x),round(y),max(1,round(w)),max(1,round(h))]],opacity=1,additive=f['blend']=='additive'))
 j=dict(name=name,width=viewport[0],height=viewport[1],layers=items,hour=hour,region=region,zoom=zoom)
 if overlay:
  points=[]
  for i in range(0,151,3):
   p=body_center('sun',4.5+i/10);points.append([round(v) for v in world_to_screen(p,zoom,parallax=(0,1),viewport=viewport)])
  j['orbit']=points;j['body_rects']=[i['rects'][0] for i in items if 'body' in i]
 jobs.append(j)
for region in m['regions']:
 for phase in PHASES:
  for zoom in (1,.25):
   name=f'{region}_{phase}_zoom_{int(zoom*100)}'
   make(region,zoom,FIXED_HOURS[phase],name+'.png')
   make(region,zoom,FIXED_HOURS[phase],name+'_orbit.png',overlay=True)
 for hour in range(4,29):make(region,.25,hour,f'{region}_timeline_{hour:02}.png',(480,270))
 for zoom in (1,.25):make(region,zoom,0,f'{region}_fx_zoom_{int(zoom*100)}.png',fx=True)
def lua(v):
 if isinstance(v,dict):return '{'+','.join('['+lua(k)+']='+lua(x) for k,x in v.items())+'}'
 if isinstance(v,(list,tuple)):return '{'+','.join(map(lua,v))+'}'
 if isinstance(v,bool):return 'true' if v else 'false'
 return json.dumps(v,ensure_ascii=False)
(ROOT/'render-jobs.lua').write_text('return '+lua(jobs),encoding='utf-8')
(ROOT/'render-jobs.json').write_text(json.dumps(jobs,ensure_ascii=False,indent=2),encoding='utf-8')
print(len(jobs))
