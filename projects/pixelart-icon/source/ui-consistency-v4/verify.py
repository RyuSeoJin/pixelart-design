# CHANGELOG v1.0 · 2026-09-27 — 공통 UI v4 홀수 얼굴·방향·현재 출력 검증
"""현재 66종의 출력과 v1 보존, 기호 대칭을 검사합니다."""
from pathlib import Path
import json, hashlib
import xml.etree.ElementTree as ET
from PIL import Image, ImageChops
root=Path(__file__).resolve().parents[2];source=Path(__file__).resolve().parent
cat=json.loads((root/'spec/design/recordtales-icon-catalog.json').read_text(encoding='utf-8'))
items=cat['items'];assert len(items)==66
assert sum(a['version']=='v4' for a in items)==12
assert sum(a['render_mode']=='geometry_per_size' for a in items)==14
report={'revision':'1.0','status':'passed','current_icons':66,'current_pngs':264,'new_v4_pngs':48,'geometry_icons':14,'pixel_icons':52,'art_approval':'pending','assets':[]}
def image(a,size):return Image.open(root/a['output_directory']/f'icon-{size}.png').convert('RGBA')
for a in items:
    files=[];base=image(a,16)
    assert (root/a['editable_file']).is_file(),a['id']
    if a['render_mode']=='geometry_per_size':
        svg=ET.parse(root/a['geometry_file']).getroot()
        assert svg.attrib['viewBox']=='0 0 32 32'
        assert svg.find('{http://www.w3.org/2000/svg}polygon') is not None
    for size in (16,32,48,64):
        im=image(a,size);assert im.size==(size,size),a['id']
        colors=set(im.get_flattened_data());visible={c[:3] for c in colors if c[3]}
        assert {c[3] for c in colors}<={0,255} and visible,a['id']
        assert min(min(c) for c in visible)>=10,a['id']
        bounds=im.getchannel('A').getbbox()
        assert bounds and min(bounds[:2])>=1 and max(bounds[2:])<=size-1,(a['id'],size,bounds)
        equal=ImageChops.difference(im,base.resize((size,size),Image.Resampling.NEAREST)).getbbox(alpha_only=False) is None
        if a['render_mode']=='pixel_native_16':assert equal,a['id']
        if a['id'] in ('sym_check','sym_close') and size==32:assert not equal,a['id']
        if a['version']=='v4':assert len(visible)>=2,a['id']
        path=root/a['output_directory']/f'icon-{size}.png'
        files.append({'path':path.relative_to(root).as_posix(),'size':size,'visible_colors':len(visible),'nearest_from_16_match':equal,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
    report['assets'].append({'id':a['id'],'version':a['version'],'render_mode':a['render_mode'],'files':files})
lookup={a['id']:a for a in items}
for size in (16,32,48,64):
    def alpha(name):return image(lookup[name],size).getchannel('A')
    for x,y,op in [('sym_prev','sym_next',Image.Transpose.FLIP_LEFT_RIGHT),('sym_prev','sym_up',Image.Transpose.ROTATE_270),('sym_prev','sym_down',Image.Transpose.ROTATE_90),('sym_fold_closed','sym_fold_open',Image.Transpose.ROTATE_270)]:
        assert ImageChops.difference(alpha(x).transpose(op),alpha(y)).getbbox() is None,(size,y)
    assert ImageChops.difference(alpha('sym_close').transpose(Image.Transpose.ROTATE_90),alpha('sym_close')).getbbox() is None,size
old=json.loads((source/'previous-hashes.json').read_text(encoding='utf-8'))
assert len(old)==264
for p,digest in old.items():assert hashlib.sha256((root/p).read_bytes()).hexdigest()==digest,p

constraints=json.loads((source/'constraints.json').read_text(encoding='utf-8'))
for id,rule in constraints['faces'].items():
    mask=Image.open(source/f'{id}-face-mask.png').convert('RGBA').getchannel('A')
    box=mask.getbbox();n=rule['diameter'];cx,cy=rule['center']
    assert n%2==1 and box==(cx-n//2,cy-n//2,cx+n//2+1,cy+n//2+1),(id,box)
    crop=mask.crop(box)
    for op in (Image.Transpose.FLIP_LEFT_RIGHT,Image.Transpose.FLIP_TOP_BOTTOM,Image.Transpose.ROTATE_90):
        assert ImageChops.difference(crop,crop.transpose(op)).getbbox() is None,id
    im=image(lookup[id],16);im=im.crop(im.getchannel('A').getbbox())
    assert ImageChops.difference(im,im.transpose(Image.Transpose.FLIP_LEFT_RIGHT)).getbbox(alpha_only=False) is None,id
head=constraints['hammer']['head'];handle=constraints['hammer']['handle']
assert head[0]+(head[2]-1)/2==handle[0]+(handle[2]-1)/2
assert head[2]>head[3] and handle[2]<handle[3]
design=json.loads((source/'design.json').read_text(encoding='utf-8'))
for a in design['assets']:
    pts=a['shapes'][0]['points']
    for p,q in zip(pts,pts[1:]+pts[:1]):
        dx=q[0]-p[0];dy=q[1]-p[1];assert dx==0 or dy==0 or abs(dx)==abs(dy),a['id']
    for i in ([2,5] if len(pts)==6 else [1]):
        p,q,r=pts[i-1],pts[i],pts[(i+1)%len(pts)]
        assert sum((p[j]-q[j])*(r[j]-q[j]) for j in (0,1))==0,a['id']
report.update(previous_264_files_preserved=True,directional_symmetry=True,odd_round_faces=4,face_rgba_symmetry=True,hammer_axis_coordinates=True,right_angle_geometry=7,binary_alpha=True,minimum_channel=10,remaining_geometry_reviews=54)
(root/'export/collection-v4/validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for a in items:
    if a['version']=='v4':a['ui_geometry_review']='automated_passed_visual_pending'
(root/'spec/design/recordtales-icon-catalog.json').write_text(json.dumps(cat,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('현재 66종·264개 PNG 규격 통과, v4 12종 대칭·홀수 얼굴·방향 직각 검사 통과, 이전 264개 보존 확인')
