# CHANGELOG v1.0 · 2026-09-27 — 색상과 기호별 도형 출력 규격을 현재 사양에 반영
"""요청한 메뉴·기호 변경을 사양·목록·이력에 반영합니다."""
from pathlib import Path
from datetime import datetime
import json
root=Path(__file__).resolve().parents[2]
source=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
catp=root/'spec/design/recordtales-icon-catalog.json';cat=read(catp)
assert cat['revision']=='1.2','이 갱신은 v1.2 목록에서 한 번만 실행합니다.'
write(source/'catalog-before-v2.json',cat)
design=read(source/'design.json');designs={a['id']:a for a in design['assets']}
for a in cat['items']:
    a['render_mode']='pixel_native_16'
    if a['id'] in designs:
        a.update(color_mode='color',version='v2',status='review_pending',approval='pending',output_directory=f'export/{a["id"]}/v2',runtime_tint=False)
        a['render_mode']=designs[a['id']]['render_mode']
        geometric=a['render_mode']=='geometry_per_size'
        a['editable_file']=f'source/color-geometry-v2/{a["id"]}.svg' if geometric else f'sprites/color-geometry-v2/{a["id"]}-16.aseprite'
        a.pop('native_file',None)
        if not geometric:a['native_file']=f'source/color-geometry-v2/{a["id"]}-native-16.png'
        else:a['geometry_file']=f'source/color-geometry-v2/{a["id"]}.svg'
cat.update(revision='1.3',revision_note='2026-09-27: 사용자 요청으로 메뉴·기호 23종 색상 v2와 기호 도형별 직접 출력 적용',art_status='mixed_v2_review_pending')
write(catp,cat)
sp=root/'spec/design/pixel-spec-icon.json';spec=read(sp)
spec.update(revision='1.2',revision_note='2026-09-27: 전체 유색 제공, 기호 14종은 도형 원본에서 크기별 직접 출력',native_size_scope='pixel_native_16',resampling='per_render_mode')
spec['color_modes']={'color':{'groups':['menu','symbol','category','ticket','emotion','order','action'],'runtime_tint':False}}
spec['render_modes']={
 'pixel_native_16':{'groups':['menu','category','ticket','emotion','order','action'],'native_size':[16,16],'resampling':'nearest','post_scale_retouch':False},
 'geometry_per_size':{'groups':['symbol'],'source':'SVG 도형과 동일 좌표의 design.json','coordinate_space':[32,32],'outputs':[16,32,48,64],'method':'각 크기에서 도형을 직접 래스터화','alpha_values':[0,255],'antialias':False,'nearest_from_16_required':False,'stroke_width_at_32':1.8}
}
spec['representative_gate']['note']='v1 대표 승인 기록입니다. 수정된 cmd_settings·sym_close의 v2 외형 승인은 별도입니다.'
write(sp,spec)
rp=root/'rules/icon-production.md';s=rp.read_text(encoding='utf-8')
s='<!-- CHANGELOG v1.3 · 2026-09-27 — 전체 유색 제공과 기호 도형 원본·크기별 직접 출력 -->\n'+s
s=s.replace('실제 도트 작업 격자는 16×16입니다.','사물·메뉴의 실제 도트 작업 격자는 16×16입니다. 기호는 도형 원본을 사용합니다.')
s=s.replace('3. 16×16 작업본을 최근접 보간으로 1·2·3·4배 출력합니다.','3. 사물·메뉴는 16×16 작업본을 최근접 보간으로 1·2·3·4배 출력합니다. 기호는 도형 원본에서 16·32·48·64px를 각각 직접 출력합니다.')
s=s.replace('수정은 16×16 원본에 반영하고 모두 다시 출력합니다.','사물·메뉴 수정은 16×16 원본에, 기호 수정은 도형 원본에 반영하고 모두 다시 출력합니다.')
s=s.replace('확대본은 16px 원본의 최근접 확대와\n   RGBA가 같아야 합니다.','사물·메뉴 확대본은 16px 원본의 최근접 확대와\n   RGBA가 같아야 합니다. 기호는 크기별 직접 출력이므로 이 일치 조건을 적용하지 않습니다.')
s=s.replace('메뉴·기호 23종은 흰색 한 색과 투명으로 제작하여 게임에서 색을 입힙니다. 나머지 43종은 제작한 색을 그대로 사용합니다.','전체 66종은 색을 포함한 PNG로 제공합니다. 메뉴 9종은 사물에 맞는 색과 명암을, 기호 14종은 의미별 색과 일정한 외곽선을 사용합니다. 기본 사용 시 런타임 색상 곱은 흰색으로 두어 원래 색을 보존합니다.')
s=s.replace('## 화면 표시와 UE 연결','## 기호 도형 제작\n\n체크·X·이동 화살표·재생·정지·접기·펼치기·별·수정 기호는 32×32 좌표계의 도형 원본으로 설계합니다. 체크는 짧은 왼쪽 획과 긴 오른쪽 획, X는 중심과 양팔의 대칭을 유지합니다. 원본 외곽선은 32px 기준 1.8px이며 각 크기에서 비례 적용합니다.\n\n16px 확대의 불규칙한 모양을 피하려고 네 크기를 도형에서 직접 출력합니다. PNG 가장자리는 알파 0/255로 유지합니다. SVG 편집 화면의 가장자리 처리는 뷰어마다 다를 수 있으므로 게임 검수 기준은 출력 PNG입니다. 예시 이미지는 형태 참고이며 복제하지 않습니다. 원본은 source/color-geometry-v2/design.json과 SVG에 보존합니다.\n\n## 화면 표시와 UE 연결')
rp.write_text(s,encoding='utf-8')
lp=root/'pixelart-icon-change-log.md';s=lp.read_text(encoding='utf-8')
s='<!-- CHANGELOG v1.4 · 2026-09-27 — 메뉴·기호 색상 v2와 도형 출력 예외 -->\n'+s
s=s.replace('**승인 대표 6종을 보존하고 새 60종을 제작하여 전체 66종 검토본과 264개 출력을 완성했습니다. 기술 검사는 통과했으며 새 60종 외형 승인·공용 등록·UE 검수는 별도입니다.**','**메뉴·기호 23종을 색상 v2로 수정했습니다. 현재 검토본은 v2 23종과 기존 유색 v1 43종입니다. 기호 14종은 도형에서 크기별 직접 출력하며, 사물·메뉴는 16px 정수배 방식을 유지합니다. 외형 승인·공용 등록·UE 검수는 별도입니다.**')
s=s.replace('| `spec/design/pixel-spec-icon.json` | 1.1 |','| `spec/design/pixel-spec-icon.json` | 1.2 |').replace('| `rules/icon-production.md` | 1.2 |','| `rules/icon-production.md` | 1.3 |').replace('| `spec/design/recordtales-icon-catalog.json` | 1.2 |','| `spec/design/recordtales-icon-catalog.json` | 1.3 |')
s=s.replace('32×32를 기본으로 제공합니다. 최종 승인','32×32를 기본으로 제공합니다. 기호 14종은 도형 원본에서 네 크기를 직접 출력합니다. 최종 승인')
s=s.replace('확대 후 추가 도트 보정은 하지 않습니다. 원본을 수정한 뒤 네 크기를 다시 출력합니다.','확대 후 추가 도트 보정은 하지 않습니다. 사물·메뉴는 16px 원본, 기호는 도형 원본을 수정한 뒤 네 크기를 다시 출력합니다.')
s=s.replace('메뉴·기호 23종은 흰색 단색, 나머지 43종은 원래 색으로 제작합니다.','전체 66종은 유색 제공입니다. 메뉴·기호의 흰색 단색·런타임 착색 방식은 v2에서 대체했습니다.')
stamp=datetime.now().strftime('%Y-%m-%d %H:%M')
entry=f'### {stamp} — 메뉴·기호 색상과 도형 v2 반영\n\n회색 아이콘에 색을 넣고 체크·X를 예시처럼 도형으로 표현해 달라는 사용자 요청에 따라 메뉴 9종을 유색 16px로, 기호 14종을 유색 도형 원본으로 수정했습니다. v2 PNG 92개와 전후 비교판을 저장하고 기존 v1 파일은 보존했습니다. 크기별 직접 출력 예외를 사양·규칙·목록에 반영했습니다. 첨부 이미지는 형태만 참고했고 저장소에 복제하지 않았습니다.\n\n'
s=s.replace('## 변경 이력 (최신이 위)\n\n','## 변경 이력 (최신이 위)\n\n'+entry)
lp.write_text(s,encoding='utf-8')
qp=root/'pixelart-icon-remaining-work.md';s=qp.read_text(encoding='utf-8')
s='<!-- CHANGELOG v1.4 · 2026-09-27 — 메뉴·기호 v2와 크기별 도형 검수 반영 -->\n'+s
start=s.index('1. **전체 66종 외형 검토**');end=s.index('\n2. **최종 등록**',start)
s=s[:start]+'1. **현재 66종 외형 검토** — 메뉴·기호 v2 23종과 유색 v1 43종을 export/collection-v2에서 확인합니다. 기존 승인 6종 중 수정된 cmd_settings·sym_close는 v2 재승인이 필요합니다. 기호는 도형 원본, 나머지는 16px 원본에서 수정합니다.'+s[end:]
s=s.replace('- 새 60종의 개별 외형 승인 — export/collection-v1/README.md와 비교판에서 확인합니다. 대표 6종 스타일과 제작 범위·배율은 승인 완료입니다.','- 메뉴·기호 v2 23종 및 아직 승인하지 않은 유색 v1 39종의 외형 승인. 기존 유색 대표 4종은 승인 상태를 유지합니다.')
s=s.replace('최종 화면 DPI·필터·정수 정렬 검수,','최종 화면 DPI·필터·정수 정렬 검수, 유색 파일의 런타임 색상 곱 흰색 적용,')
qp.write_text(s,encoding='utf-8')
print('사양 1.2·규칙 1.3·목록 1.3·현행 기준·작업 큐 갱신 완료')
