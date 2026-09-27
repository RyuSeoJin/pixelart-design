# CHANGELOG v1.0 · 2026-09-28 — 개별 시안의 실제 크기·알파·색상 하한을 확인합니다.
"""사막여우 삼면도 묶음의 기술 검사 결과를 저장합니다."""
from pathlib import Path
from PIL import Image
import hashlib
import json

root=Path(__file__).resolve().parent
report={'version':'v3','stage':'1024 시안·삼면도 검토','approval':'사용자 확인 대기','files':[]}
files=sorted(root.glob('*1024x1024-v3.png'))
assert len(files)==8, '대표 2장과 삼면도 6장이 필요합니다.'
for f in files:
    im=Image.open(f).convert('RGBA')
    assert im.size==(1024,1024)
    alpha=im.getchannel('A')
    # 시안은 생성 알파를 보존합니다. 0/255 이진화는 160 도트 단계의 검사입니다.
    assert alpha.getextrema()[0]==0 and alpha.getextrema()[1]>=254
    minimum=min(min(c[:3]) for c in im.get_flattened_data() if c[3]>0)
    assert minimum>=10
    # 생성 알파의 미세한 흔적과 실제 캐릭터 외곽을 구분해 기록합니다.
    bbox=alpha.point(lambda a:255 if a>=128 else 0).getbbox()
    assert bbox[0]>0 and bbox[1]>0 and bbox[2]<1024 and bbox[3]<1024
    report['files'].append({'file':f.name,'size':list(im.size),'visible_rgb_min':minimum,'alpha_extrema':list(alpha.getextrema()),'alpha128_bbox':list(bbox)})
for original,copy in [('desert-fox-concept-1024x1024-v1.png','desert-fox-concept-front-1024x1024-v3.png'),('desert-fox-concept-1024x1024-v2.png','desert-fox-concept-three-quarter-1024x1024-v3.png')]:
    assert hashlib.sha256((root.parent/original).read_bytes()).digest()==hashlib.sha256((root/copy).read_bytes()).digest()
report['representatives_unchanged']=True
report['pixel_grid_validation']='160·320 단계 전이며 전체 도트 규칙 통과가 아닙니다.'
report['pending']=['삼면도 후면 구조 채택','시점별 세부 비례·겹침 검토','160·320 네 종류 준비 그림','애니메이션']
(root/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,ensure_ascii=False))
