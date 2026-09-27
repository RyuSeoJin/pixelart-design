# CHANGELOG v1.0 · 2026-09-27 — 128·256 격자, 얼굴 보정 범위, 팔레트와 알파를 검사합니다.
"""얼음여왕 256 정지본의 규격과 얼굴 레이어를 검증합니다."""
from pathlib import Path
import json, hashlib
from PIL import Image, ImageChops

root=Path(__file__).resolve().parents[2]
src=root/'source/ice-queen'
out=root/'export/ice-queen'
def load(p): return Image.open(p).convert('RGBA')
native=load(src/'ice-queen-working-128x128-v1.png')
base=load(src/'ice-queen-base-256x256-v1.png')
final=load(out/'ice-queen-still-256x256-v1.png')
mask=load(src/'face-mask-256-v1.png')
overlay=load(src/'face-retouch-256-v1.png')
assert native.size==(128,128)
assert base.size==final.size==mask.size==overlay.size==(256,256)
assert ImageChops.difference(native.resize((256,256),Image.Resampling.NEAREST),base).getbbox(alpha_only=False) is None
assert ImageChops.difference(Image.alpha_composite(base,overlay),final).getbbox(alpha_only=False) is None
changed=[]
for y in range(256):
 for x in range(256):
  if base.getpixel((x,y))!=final.getpixel((x,y)):
   assert mask.getpixel((x,y))[3]==255
   changed.append([x,y])
assert ImageChops.difference(base.getchannel('A'),final.getchannel('A')).getbbox() is None
spec=json.loads((root/'spec/design/pixel-spec-portrait.json').read_text(encoding='utf-8'))
palette={tuple(bytes.fromhex(c[1:])) for c in [spec['palette']['outline']]+[c for ramp in spec['palette']['ramps'].values() for c in ramp]}
colors={p[:3] for p in final.get_flattened_data() if p[3]}
assert colors<=palette and len(colors)<=64
assert min(min(c) for c in colors)>=10
assert set(final.getchannel('A').get_flattened_data())=={0,255}
assert final.getchannel('A').crop((0,244,256,256)).getbbox() is None
report={'size':[256,256],'native_size':[128,128],'scale':2,'grid_pass':True,
 'outside_face_mask_changed_pixels':0,'face_changed_pixels':len(changed),'palette_pass':True,
 'visible_colors':len(colors),'visible_rgb_channel_min':min(min(c) for c in colors),'alpha_values':[0,255],
 'layer_recomposition_pass':True,'ground_pass':True,'status':'정지본 사용자 승인 대기',
 'concept_sha256':hashlib.sha256((src/'ice-queen-concept-1024x1024-v1.png').read_bytes()).hexdigest(),
 'note':'시안 승인과 최종 정지본 승인은 별개입니다. 가려진 관절의 기준선은 시안 관찰에 따른 배치이며 애니메이션 제작 전 확인이 필요합니다.'}
(out/'ice-queen-still-256x256-v1.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,ensure_ascii=False))
