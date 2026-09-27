# CHANGELOG v1.0 · 2026-09-28 — 접지·얼굴 마스크·색·512 포장을 검사합니다.
"""사막여우 정지본의 기술 검수와 비교 미리보기를 저장합니다."""
from pathlib import Path
import json
import numpy as np
from PIL import Image

SOURCE=Path(__file__).resolve().parent
PROJECT=SOURCE.parents[1]
OUT=PROJECT/'export/desert-fox'
native=Image.open(SOURCE/'desert-fox-working-160x160-draft-v1.png').convert('RGBA')
base=Image.open(OUT/'desert-fox-base-320x320-v1.png').convert('RGBA')
final=Image.open(OUT/'desert-fox-still-320x320-v1.png').convert('RGBA')
mask=Image.open(SOURCE/'face-mask-320-v1.png').convert('RGBA')
overlay=Image.open(SOURCE/'face-retouch-320-v1.png').convert('RGBA')
assert base.tobytes()==native.resize((320,320),Image.Resampling.NEAREST).tobytes()
assert Image.alpha_composite(base,overlay).tobytes()==final.tobytes()
a,b,m=np.array(final),np.array(base),np.array(mask)
changed=np.any(a!=b,axis=2)
assert not np.any(changed & (m[:,:,3]==0))
assert np.array_equal(a[:,:,3],b[:,:,3])
spec=json.loads((PROJECT/'spec/design/pixel-spec-field.json').read_text(encoding='utf-8'))
palette={tuple(bytes.fromhex(c[1:])) for c in [spec['palette']['outline']]+[c for ramp in spec['palette']['ramps'].values() for c in ramp]}
colors={p[:3] for p in final.get_flattened_data() if p[3]}
assert colors<=palette and len(colors)<=64 and min(min(c) for c in colors)>=10
assert set(np.unique(a[:,:,3]))=={0,255}
# 꼬리와 옷단을 제외한 발 영역에서만 접지를 확인합니다.
feet=final.crop((120,270,210,320)).getbbox()
sole=270+feet[3]-1
assert sole==303
delivery=Image.new('RGBA',(512,512));delivery.paste(final,(96,96))
assert delivery.crop((96,96,416,416)).tobytes()==final.tobytes()
delivery.save(OUT/'desert-fox-delivery-512x512-v1.png')
# 원래 크기와 정수배 비교용이며 배포 이미지에는 배경을 넣지 않습니다.
preview=Image.new('RGB',(640,640),(75,84,103));large=final.resize((640,640),Image.Resampling.NEAREST);preview.paste(large,(0,0),large);preview.save(OUT/'desert-fox-preview-v1.png')
face=Image.new('RGB',(880,440),(75,84,103))
for i,im in enumerate([base,final]):
 crop=im.crop((136,58,180,102)).resize((440,440),Image.Resampling.NEAREST);face.paste(crop,(440*i,0),crop)
face.save(OUT/'desert-fox-face-comparison-v1.png')
report={'status':'정지 디자인 사용자 검토 대기','sizes':{'native':[160,160],'still':[320,320],'delivery':[512,512]},'visible_colors':len(colors),'palette_pass':True,'alpha_binary':True,'body_nearest_2x_pass':True,'face_changed_pixels':int(changed.sum()),'outside_face_mask_changed':0,'layer_recomposition_pass':True,'sole_y_320':sole,'sole_y_512':sole+96,'ground_alignment':{'native_offset':[0,0],'output_offset':[0,0],'reason':'작업 단계에서 접지 행 151에 배치됨','per_frame_alignment':False},'delivery_padding_pass':True,'engine_review':'미실시','animation':'미제작','visual_review_pending':['6등신과 관절 기준선','왼쪽 진행 방향과 양 발끝','도트 밀도와 손·옷의 연결','꼬리 외곽선','얼굴 보정 인상'],'all_style_rules_passed':False}
(OUT/'validation-v1.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,ensure_ascii=False))
