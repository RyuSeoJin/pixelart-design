# CHANGELOG v1.0 · 2026-10-08 — 4시간대와 천체·효과 패키지를 준비합니다.
from pathlib import Path
import json,shutil,copy
ROOT=Path(__file__).resolve().parent; REF=ROOT/'incoming/to_chatgpt/02_current_v014'; PKG=ROOT/'unreal-full'
for d in ['Textures','Source','Preview','checks']: (PKG/d).mkdir(parents=True,exist_ok=True)
m=json.loads((REF/'manifest.json').read_text(encoding='utf-8'))
old=copy.deepcopy(m)
m.update(version=15,destination='/Game/Art/PixelLandscape_v015',phases=['dawn','day','dusk','night'],status='4시간대와 천체 효과 제작 중')
m['assets']=[a for a in m['assets'] if a['layer']!='stars']
for a in m['assets']:shutil.copy2(REF/a['file'],PKG/a['file'])
for a in list(m['assets']):
 if a['phase']!='day':continue
 for phase in ['dawn','dusk']:
  b=copy.deepcopy(a);b['phase']=phase;b['name']=a['name'].replace('_Day','_'+phase.title());b['file']='Textures/'+b['name']+'.png';b.pop('sha256',None);m['assets'].append(b)
for a in old['assets']:
 if a['layer']!='stars':continue
 for letter in 'ABC':
  b=copy.deepcopy(a);b.update(layer='stars_'+letter.lower(),label='별 '+letter,name=a['name']+letter,file=a['file'].replace('.png',letter+'.png'));b.pop('sha256',None);m['assets'].append(b)
for body in ['sun','moon']:
 name='T_'+body.title();m['assets'].append(dict(name=name,file='Textures/'+name+'.png',region='shared',layer=body,label='해' if body=='sun' else '달',phase='all',size=[48,48],world_rect=[-96,-96,192,192],ratio=[0,1],period=None,anchor='world',bind=None,texel_grid=1,world_units_per_texel=4))
neworder=[old['render_order'][0]]
for letter,threshold,period in [('a',.2,2.3),('b',.5,3.1),('c',.8,4.3)]:neworder.append(dict(id='stars_'+letter,label='별 '+letter.upper(),ratio=[0,1],appear_darkness=threshold,twinkle_period_s=period))
for body in ['sun','moon']:neworder.append(dict(id=body,label='해' if body=='sun' else '달',ratio=[0,1],body=body))
for layer in old['render_order'][2:]:
 if layer['id'] in ['clouds','clouds_high']:layer['drift_px']=6 if layer['id']=='clouds' else 3
 neworder.append(layer)
m['render_order']=neworder
m['fx']=[]
for id_,name,size in [('meteor','Meteor',[24,6]),('meteor_big','MeteorBig',[160,32]),('meteor_big_glow','MeteorGlow',[64,64]),('meteor_big_spark','MeteorSpark',[64,16])]:
 f=dict(id=id_,name='T_'+name,file='Textures/T_'+name+'.png',region='shared',size=size,world_units_per_texel=4,blend='additive' if id_=='meteor_big_glow' else 'normal')
 if id_ in ('meteor','meteor_big'):f.update(direction='down_right',head_px=[size[0]-3,size[1]-2])
 if id_=='meteor_big_spark':f.update(frames=4,frame_size=[16,16])
 m['fx'].append(f)
m['native_files']=['Source/'+x+'.aseprite' for x in ['forest','snow','forest_ground','snow_ground','celestial_fx']]
m['native_layout']['scene_layers']=40
m['request_source']='00_REQUEST.md · to_chatgpt (3).zip'
m['preview_policy']={'phases':m['phases'],'zooms':[1,.25],'viewport':[1920,1080],'camera_x':0,'timeline_hours':list(range(4,29)),'transition_halfwidth_game_hours':.25,'orbit_overlay':True,'fx_preview':True}
m['import_instructions']='RecordTales 에디터에서 import_landscape.py로 텍스처94장과 스프라이트94개를 가져옵니다. manifest의 assets90개·fx4개를 연결합니다.'
(PKG/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
shutil.copy2(ROOT/'incoming/to_chatgpt/01_rules/00_RULES.md',PKG/'00_RULES.md')
shutil.copy2(ROOT/'incoming/to_chatgpt/00_REQUEST.md',PKG/'00_REQUEST.md')
t=(REF/'layer_layout.py').read_text(encoding='utf-8')
t=t.replace("'stars':(0,1)","'stars_a':(0,1), 'stars_b':(0,1), 'stars_c':(0,1), 'sun':(0,1), 'moon':(0,1)")
t=t.replace("('sky','stars','clouds_high')","('sky','stars_a','stars_b','stars_c','clouds_high')")
t=t.replace('    width, height = texture_size','    if layer in (\'sun\',\'moon\'):\n        return (-96, -96, 192, 192)\n    width, height = texture_size')
t=t.replace('from math import ceil, floor, isfinite','from math import ceil, floor, isfinite, sin, cos, pi')
t+='''

PHASES = ('dawn', 'day', 'dusk', 'night')
FIXED_HOURS = {'dawn': 5.5, 'day': 12, 'dusk': 18.5, 'night': 0}
DARKNESS = {'dawn': .5, 'day': 0, 'dusk': .5, 'night': 1}

def body_center(body, game_hour):
    """指定された15時間の天体軌道を計算します。"""
    if body not in ('sun', 'moon') or not isfinite(game_hour):
        raise ValueError('유효한 천체와 게임 시각이 필요합니다.')
    elapsed=(game_hour-(4.5 if body=='sun' else 16.5))%24
    if elapsed>15: return None
    theta=pi*elapsed/15
    return (960-800*cos(theta), 560-440*max(0,sin(theta))**.5)
'''.replace('指定された15時間の天体軌道を計算します。','지정된15시간 천체 궤도를 계산합니다.')
(PKG/'layer_layout.py').write_text('# CHANGELOG v6.0 · 2026-10-08 — 별3층과 천체 궤도·4시간대를 추가합니다.\n'+t,encoding='utf-8')
t=(REF/'import_landscape.py').read_text(encoding='utf-8').replace('v014','v015')
t=t.replace('    specs = {item["name"]: item for item in config["assets"]}', '    entries = config["assets"] + config["fx"]\n    if len(config["assets"]) != 90 or len(config["fx"]) != 4:\n        raise RuntimeError("자산90개와 효과4개를 확인해주세요.")\n    specs = {item["name"]: item for item in entries}')
t=t.replace('for item in config["assets"]]', 'for item in entries]').replace('44','94')
(PKG/'import_landscape.py').write_text('# CHANGELOG v1.2 · 2026-10-08 — 90개 자산과4개 효과를 가져옵니다.\n'+t,encoding='utf-8')
def lua(v):
 if isinstance(v,dict):return '{'+','.join('['+lua(k)+']='+lua(x) for k,x in v.items())+'}'
 if isinstance(v,(tuple,list)):return '{'+','.join(map(lua,v))+'}'
 if v is None:return 'nil'
 return json.dumps(v,ensure_ascii=False)
(ROOT/'assets.lua').write_text('return '+lua(m['assets']+m['fx']),encoding='utf-8')
print('v015 설정90자산+4효과 준비 완료')
