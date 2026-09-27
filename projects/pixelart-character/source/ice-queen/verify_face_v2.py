# CHANGELOG v1.0 · 2026-09-27 — 얼굴 마스크 밖 불변·팔레트 검사와 비교 미리보기
"""얼굴 보정 결과를 검사하고 수정 전후를 정수배로 비교합니다."""
from pathlib import Path
import json
from PIL import Image, ImageChops

root=Path(__file__).resolve().parents[2]
out=root/'export/ice-queen'
src=root/'source/ice-queen'
base=Image.open(out/'ice-queen-still-320x320-v1.png').convert('RGBA')
final=Image.open(out/'ice-queen-still-320x320-v2.png').convert('RGBA')
mask=Image.open(src/'face-mask-320-v2.png').convert('RGBA')
layer=Image.open(src/'face-retouch-320-v2.png').convert('RGBA')
assert base.size==final.size==mask.size==layer.size==(320,320)
assert ImageChops.difference(Image.alpha_composite(base,layer),final).getbbox(alpha_only=False) is None
changed=[]
for y in range(320):
    for x in range(320):
        if base.getpixel((x,y))!=final.getpixel((x,y)):
            assert mask.getpixel((x,y))[3]==255
            changed.append([x,y])
assert ImageChops.difference(base.getchannel('A'),final.getchannel('A')).getbbox() is None
spec=json.loads((root/'spec/design/pixel-spec-field.json').read_text(encoding='utf-8'))
palette={tuple(bytes.fromhex(c[1:])) for c in [spec['palette']['outline']]+[c for ramp in spec['palette']['ramps'].values() for c in ramp]}
colors={p[:3] for p in final.get_flattened_data() if p[3]>0}
assert colors<=palette and len(colors)<=64 and min(min(c) for c in colors)>=10
preview=Image.new('RGB',(488,264),(78,88,106))
for i,im in enumerate([base,final]):
    face=im.crop((140,62,178,102)).resize((228,240),Image.Resampling.NEAREST)
    preview.paste(face,(8+i*244,12),face)
preview.save(out/'ice-queen-face-before-after-v2.png')
report={'stage':'2단계 정지 디자인','status':'사용자 승인 대기','file':'ice-queen-still-320x320-v2.png','size':[320,320],
        'changed_pixels':len(changed),'outside_face_mask_changed_pixels':0,'alpha_unchanged':True,
        'visible_colors':len(colors),'visible_rgb_channel_min':min(min(c) for c in colors),
        'palette_pass':True,'layer_recomposition_pass':True,
        'editable_source':'sprites/ice-queen-still-v2.aseprite','changed_coordinates':changed}
(out/'ice-queen-still-320x320-v2.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k!='changed_coordinates'},ensure_ascii=False))
