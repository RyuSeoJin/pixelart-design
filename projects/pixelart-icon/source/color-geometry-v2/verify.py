# CHANGELOG v1.0 · 2026-09-27 — 현재 혼합 버전 66종과 도형 출력 예외 검증
"""현재 66종의 출력과 v1 보존, 기호 대칭을 검사합니다."""
from pathlib import Path
import json, hashlib
import xml.etree.ElementTree as ET
from PIL import Image, ImageChops
root=Path(__file__).resolve().parents[2];source=Path(__file__).resolve().parent
cat=json.loads((root/'spec/design/recordtales-icon-catalog.json').read_text(encoding='utf-8'))
items=cat['items'];assert len(items)==66
assert sum(a['version']=='v2' for a in items)==23
assert sum(a['render_mode']=='geometry_per_size' for a in items)==14
report={'revision':'1.0','status':'passed','current_icons':66,'current_pngs':264,'new_v2_pngs':92,'geometry_icons':14,'pixel_icons':52,'art_approval':'pending','assets':[]}
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
        if a['version']=='v2':assert len(visible)>=2,a['id']
        path=root/a['output_directory']/f'icon-{size}.png'
        files.append({'path':path.relative_to(root).as_posix(),'size':size,'visible_colors':len(visible),'nearest_from_16_match':equal,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
    report['assets'].append({'id':a['id'],'version':a['version'],'render_mode':a['render_mode'],'files':files})
lookup={a['id']:a for a in items}
for size in (16,32,48,64):
    def alpha(name):return image(lookup[name],size).getchannel('A')
    for x,y,op in [('sym_prev','sym_next',Image.Transpose.FLIP_LEFT_RIGHT),('sym_prev','sym_up',Image.Transpose.ROTATE_270),('sym_prev','sym_down',Image.Transpose.ROTATE_90),('sym_fold_closed','sym_fold_open',Image.Transpose.ROTATE_270)]:
        assert ImageChops.difference(alpha(x).transpose(op),alpha(y)).getbbox() is None,(size,y)
    assert ImageChops.difference(alpha('sym_close').transpose(Image.Transpose.ROTATE_90),alpha('sym_close')).getbbox() is None,size
old=json.loads((source/'v1-baseline.json').read_text(encoding='utf-8'))
assert len(old)==264
for p,digest in old.items():assert hashlib.sha256((root/p).read_bytes()).hexdigest()==digest,p
report.update(v1_264_files_preserved=True,directional_symmetry=True,x_symmetry=True,binary_alpha=True,minimum_channel=10)
(root/'export/collection-v2/validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('현재 66종·264개 PNG 통과: 52종 최근접 확대, 기호 14종 크기별 도형 출력, 색·알파·여백·대칭')
print('신규 v2 92개, 기존 v1 264개 해시 보존 확인')
