# CHANGELOG v1.0 · 2026-09-27 — 얼음여왕 입력을 작업 격자와 공통 동작에 맞춰 내보냅니다.
"""생성한 원화를 팔레트·격자로 변환하고 공통 몸체 동작으로 미리보기를 만듭니다."""
from pathlib import Path
import json
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent.parent
SPEC = json.loads((PROJECT / 'spec/design/pixel-spec-field.json').read_text(encoding='utf-8'))
SOURCE = Image.open(HERE / 'generated-cutout.png').convert('RGBA')
SCALE = 125 / (1518 - 140)
OX, OY = 80 - 450 * SCALE, 26 - 140 * SCALE

def point(x, y):
    return round(x * SCALE + OX), round(y * SCALE + OY)

def native():
    # 원본의 정수리와 발바닥을 정본 기준선에 배치합니다. 알파의 희미한 배경 잔여물은 제외합니다.
    im = SOURCE.transform((160, 160), Image.Transform.AFFINE,
        (1/SCALE, 0, -OX/SCALE, 0, 1/SCALE, -OY/SCALE), Image.Resampling.NEAREST)
    # 투명화 입력에서 누락된 왕관 보석만 원래 사용자가 채택한 그림의 픽셀로 복원합니다.
    ref=Image.open(HERE/'tail-outline-reference.png').convert('RGBA')
    ref=ref.transform((160,160),Image.Transform.AFFINE,
        (1/SCALE,0,-OX/SCALE,0,1/SCALE,-OY/SCALE),Image.Resampling.NEAREST)
    x0,y0=point(403,55)
    x1,y1=point(455,129)
    for y in range(y0,y1+1):
        for x in range(x0,x1+1):
            c=ref.getpixel((x,y))
            if c[0]>95 and c[1]>140 and c[2]>180:
                im.putpixel((x,y),(*c[:3],255))
    colors = [SPEC['palette']['outline']] + [c for ramp in SPEC['palette']['ramps'].values() for c in ramp]
    rgb = [tuple(bytes.fromhex(c[1:])) for c in colors]
    cache = {}
    for y in range(160):
        for x in range(160):
            p = im.getpixel((x,y))
            if p[3] < 200:
                im.putpixel((x,y), (0,0,0,0))
                continue
            if p[:3] not in cache:
                cache[p[:3]] = min(rgb, key=lambda c: sum((c[i]-p[i])**2 for i in range(3)))
            im.putpixel((x,y), (*cache[p[:3]],255))
    im.save(HERE / 'base-160.png')
    im.resize((640,640), Image.Resampling.NEAREST).save(HERE / 'base-review.png')
    return im

def cut(im, polygon):
    mask = Image.new('L',im.size)
    ImageDraw.Draw(mask).polygon([point(x,y) for x,y in polygon], fill=255)
    out = Image.new('RGBA',im.size)
    out.paste(im,(0,0),mask)
    return out

def split(im):
    # 겹침 아래를 보충할 수 있도록 파츠 마스크는 관절에서 서로 겹칩니다.
    parts = {}
    parts['tail'] = cut(im, [(678,555),(730,495),(1024,495),(1024,1200),(705,1200),(634,1050),(665,995),(680,950),(696,890),(760,835),(727,720),(670,693),(650,630)])
    parts['thigh_L'] = cut(im, [(190,1000),(450,1000),(473,1290),(450,1536),(180,1536)])
    parts['thigh_R'] = cut(im, [(450,1000),(658,1000),(715,1285),(710,1536),(472,1536),(473,1290)])
    parts['head'] = cut(im, [(0,0),(1024,0),(1024,335),(0,335)])
    parts['upperarm_L'] = cut(im, [(313,530),(340,530),(308,667),(300,770),(264,837),(250,910),(165,910),(140,755),(216,690),(251,590)])
    parts['upperarm_R'] = cut(im, [(510,440),(585,439),(633,543),(665,651),(695,711),(744,805),(754,842),(700,884),(687,959),(621,959),(617,908),(565,898),(543,803),(543,672),(514,583)])
    parts['torso'] = im.copy()
    # 몸통에서 다른 파츠를 지운 뒤 소매 아래의 숨은 천 3도트만 같은 행의 옷 색으로 연장합니다.
    for y in range(160):
        for x in range(160):
            if any(parts[n].getpixel((x,y))[3] for n in parts if n!='torso'):
                parts['torso'].putpixel((x,y),(0,0,0,0))
    torso = parts['torso']
    for y in range(point(0,450)[1],point(0,980)[1]):
        xs=[x for x in range(160) if torso.getpixel((x,y))[3]]
        if not xs: continue
        for side in (-1,1):
            edge=min(xs) if side<0 else max(xs)
            color=torso.getpixel((min(xs)+2 if side<0 else max(xs)-2,y))
            for d in range(1,4):
                xx=edge+side*d
                if 0<=xx<160: torso.putpixel((xx,y),color)
    # 다리 윗부분은 옷단 뒤에 가려지는 겹침 영역을 갖습니다.
    for n in ('thigh_L','thigh_R'):
        leg=parts[n]
        top=point(0,1015)[1]
        for y in range(top-5,top):
            for x in range(160):
                c=leg.getpixel((x,top+2))
                if c[3]: leg.putpixel((x,y),c)
    directory=HERE/'parts160'
    directory.mkdir(exist_ok=True)
    for name,p in parts.items(): p.save(directory/f'{name}.png')
    return parts

def shifted(part,dx=0,dy=0):
    out=Image.new('RGBA',(160,160))
    out.paste(part,(dx,dy))
    return out

def leg_frame(part, step, lift, bob):
    # 공통 보행 이동을 정수 행 이동으로 적용합니다. 보간·회전으로 새 색이 생기지 않습니다.
    out=Image.new('RGBA',(160,160))
    top=point(0,1000)[1]
    knee=118
    for y in range(top-5,152):
        t=max(0,min(1,(y-top)/(145-top)))
        dx=round(step*t)
        dy=lift
        row=part.crop((0,y,160,y+1))
        out.paste(row,(dx,y+dy))
    return out

def animate(parts):
    outdir=PROJECT/'export/ice-queen'
    outdir.mkdir(parents=True,exist_ok=True)
    # 원래 320 격자의 공통 이동을 정수 160 격자로 반올림합니다. 기존 사양은 덮어쓰지 않습니다.
    offsets={tag:{n:[[round(x/2),round(y/2)] for x,y in seq] for n,seq in a['offsets'].items()}
        for tag,a in SPEC['animations'].items()}
    order=['tail','thigh_L','thigh_R','torso','head','upperarm_L','upperarm_R']
    animations={}
    all_layers=[]
    for tag,a in SPEC['animations'].items():
        frames=[]
        for f in range(a['frames']):
            dx,bob=offsets[tag]['body'][f]
            phase=[0,1,2,1,0,-1,-2,-1][f] if tag=='walk' else 0
            step=round(phase*2.5)
            lift=2 if tag=='walk' and f in (1,5) else 0
            layers={}
            for name in order:
                if name.startswith('thigh'):
                    sign=-1 if name.endswith('_L') else 1
                    footlift=-lift if step*sign<0 else 0
                    layers[name]=leg_frame(parts[name],step*sign,footlift,bob) if tag=='walk' else parts[name]
                else:
                    ox,oy=dx,bob
                    if name=='head': ox,oy=offsets[tag]['head'][f]
                    if name.startswith('upperarm'):
                        ox,oy=offsets[tag]['hand_'+name[-1]][f]
                    if name=='tail':
                        ox=[0,1,1,0][f] if tag=='idle' else [0,0,1,1,0,0,-1,-1][f]
                        oy=bob+([0,0,0,1][f] if tag=='idle' else 0)
                    layers[name]=shifted(parts[name],ox,oy)
            frame=Image.new('RGBA',(160,160))
            for name in order: frame.alpha_composite(layers[name])
            frames.append(frame)
            all_layers.append(layers)
            frame.save(outdir/f'{tag}-{f:02d}-160.png')
            frame.resize((320,320),Image.Resampling.NEAREST).save(outdir/f'{tag}-{f:02d}-320.png')
        durations=a['ms'] if isinstance(a['ms'],list) else [a['ms']]*a['frames']
        sheet=Image.new('RGBA',(320*len(frames),320))
        previews=[]
        for f,frame in enumerate(frames):
            large=frame.resize((320,320),Image.Resampling.NEAREST)
            sheet.paste(large,(f*320,0))
            bg=Image.new('RGB',(320,320),(78,88,106))
            bg.paste(large,(0,0),large)
            previews.append(bg)
        previews[0].save(outdir/f'{tag}-preview.gif',save_all=True,append_images=previews[1:],duration=durations,loop=0,disposal=2,optimize=False)
        sheet.save(outdir/f'{tag}-sheet.png')
        right=Image.new('RGBA',sheet.size)
        for f,frame in enumerate(frames):
            right.paste(frame.transpose(Image.Transpose.FLIP_LEFT_RIGHT).resize((320,320),Image.Resampling.NEAREST),(f*320,0))
        right.save(outdir/f'{tag}-sheet-right.png')
        animations[tag]={'frames':len(frames),'durations_ms':durations,'loop':True,'frame_size':[320,320]}
    # 레이어·태그·타이밍을 보존하는 Aseprite 원본 제작용 데이터입니다.
    data_dir=HERE/'animation-layers'
    data_dir.mkdir(exist_ok=True)
    for f,layers in enumerate(all_layers):
        for name,im in layers.items(): im.save(data_dir/f'{f:02d}-{name}.png')
    lua=['-- CHANGELOG v1.0 · 2026-09-27 — 얼음여왕 애니메이션 원본 조립',
         'local s=Sprite(160,160,ColorMode.RGB)', 'local initial=s.layers[1]',
         'for i=2,12 do s:newEmptyFrame() end']
    for name in order:
        lua += [f'local l=s:newLayer(); l.name="{name}"']
        for f in range(12):
            path=(data_dir/f'{f:02d}-{name}.png').as_posix()
            lua += [f's:newCel(l,{f+1},Image{{fromFile="{path}"}},Point(0,0))']
    lua += ['s:deleteLayer(initial)']
    for f,d in enumerate([260,200,260,200]+[100]*8): lua += [f's.frames[{f+1}].duration={d/1000}']
    lua += ['local idle=s:newTag(1,4); idle.name="idle"', 'local walk=s:newTag(5,12); walk.name="walk"',
        f's:saveAs("{(PROJECT / "sprites/ice-queen-v1.aseprite").as_posix()}")', 'print("완료: 12프레임, 7레이어")']
    (HERE/'build-animation.lua').write_text('\n'.join(lua),encoding='utf-8')
    manifest={'status':'동작 검토용 초안','source':'generated-cutout.png','native_size':[160,160],
        'output_scale':2,'resampling':'nearest','facing':'left','animations':animations,
        'visible_rgb_min':10,'transparent_alpha':0,'common_motion_source':'source/_body6/body6.py의 보행 위상과 필드 사양의 앵커 이동',
        'native_offsets':offsets,'limitations':['관절과 가려진 옷의 보완은 초안입니다.','전체 일러스트 규칙 통과를 선언하지 않습니다.']}
    (outdir/'animation.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')

if __name__ == '__main__':
    animate(split(native()))
