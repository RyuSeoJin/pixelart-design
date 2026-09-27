# CHANGELOG v1.0 · 2026-09-27 — UI 대칭·홀수 얼굴·각도 기준을 정본과 목록에 반영
"""UI 제작의 재사용 기준과 수정본의 현재 경로를 기록합니다."""
from pathlib import Path
import json
from datetime import datetime
root=Path(__file__).resolve().parents[2];src=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
c=read(src/'constraints.json');geo=set(c['geometry_ids']);pixels=set(c['faces'])|{'cmd_edit'};changed=geo|pixels
cp=root/'spec/design/recordtales-icon-catalog.json';cat=read(cp);assert cat['revision']=='1.4'
for a in cat['items']:
    a['ui_geometry_review']='pending'
    if a['id'] not in changed:continue
    name=a['id'];a.update(version='v4',status='review_pending',approval='pending',output_directory=f'export/{name}/v4',ui_geometry_review='automated_checks_pending')
    if name in geo:
        a.update(geometry_file=f'source/ui-consistency-v4/{name}.svg',editable_file=f'source/ui-consistency-v4/{name}.svg')
        a['ui_geometry']={'symmetry_mode':'horizontal' if name in ['sym_prev','sym_next','sym_play','sym_fold_closed'] else 'vertical','axis':16,'coordinate_space':32,'diagonal_degrees':45,'tip_degrees':90}
    else:
        a.update(native_file=f'source/ui-consistency-v4/{name}-native-16.png',editable_file=f'sprites/ui-consistency-v4/{name}.aseprite')
        a['ui_geometry']={'symmetry_mode':'vertical' if name in c['faces'] else 'components','coordinate_space':16}
        if name in c['faces']:a['ui_geometry'].update(axis=c['reflection_axes'][name],face_region=c['faces'][name])
        else:a['ui_geometry'].update(asymmetry_reason='집과 앞쪽 망치가 겹친 복합 아이콘입니다. 망치 자체는 직립·대칭입니다.',hammer=c['hammer'])
cat.update(revision='1.5',revision_note='2026-09-27: 홀수 얼굴·일자 망치·직각 기호 12종 v4와 UI 검사 상태',art_status='mixed_v4_review_pending');write(cp,cat)
sp=root/'spec/design/pixel-spec-icon.json';s=read(sp);s.update(revision='1.4',revision_note='2026-09-27: 좌우 대칭 우선·홀수 원형 얼굴·0/45/90도 방향과 검수 기준')
s['ui_geometry']={
 'symmetry_default':'vertical','symmetry_target':'외곽·주요 구조; 방향성 명암은 별도 판정',
 'require_axis_before_drawing':True,'native_axis_options':['integer_pixel_center','between_pixel_centers'],
 'face':{'native_width':'odd','native_height':'equal_to_width_for_round_face','shared_axis_for_head_neck_shoulders':True,'crop_reflection_match_required':True,'odd_requirement_applies_to':'native_grid','unequal_canvas_padding_max_native_px':1},
 'angles':{'primary_axes_degrees':[0,90],'diagonal_degrees':45,'chevron_tip_degrees':90,'arrow_triangle_tip_degrees':90,'direction_variants':'90度 회전 또는 반사로 생성'},
 'hammer_default':{'head':'horizontal','handle':'vertical','axes_intersection_degrees':90},
 'asymmetry_exception_requires':['semantic_reason','component_axes','review_note'],
 'new_asset_required_metadata':['symmetry_mode','axis_and_coordinate_space','face_regions_if_present','angle_constraints_if_present','asymmetry_reason_if_applicable'],
 'checks':['외곽 반사 일치','얼굴 홀수 지름·정사각 경계','기준 좌표의 직각 내적 0','사선 dx 절댓값=dy 절댓값','방향별 회전·반사 일치','16/32/48/64 실물 확인'],
 'legacy_status':'기존 전체를 새 기준으로 통과했다고 간주하지 않습니다. 목록별 ui_geometry_review를 확인합니다.'}
s['ui_geometry']['angles']['direction_variants']='90도 회전 또는 반사로 생성'
write(sp,s)
rp=root/'rules/icon-production.md';rules=rp.read_text(encoding='utf-8');rules='<!-- CHANGELOG v1.5 · 2026-09-27 — 공통 중심축·홀수 얼굴·직각·예외·검수 기준 -->\n'+rules
section='''## 공통 UI 형태 기준

이 절은 이후 제작·수정하는 모든 아이콘에 적용합니다. 그림을 시작할 때 제작 목록에 대칭 방식, 중심축과 좌표계, 얼굴 영역, 각도 조건을 기록합니다. 비대칭 구성에는 이유도 기록합니다. 수치 정본은 `pixel-spec-icon.json`의 `ui_geometry`입니다.

### 중심축과 대칭

정면 인물, 정면 사물, 기계 및 기호는 좌우 대칭을 기본으로 설계합니다. 먼저 중심축을 정하고 한쪽을 반사해 다른 쪽을 만듭니다. 외곽뿐 아니라 목·어깨·손잡이·구멍 등 주요 구조의 중심도 맞춥니다. 명암이나 재질의 빛 방향은 외곽 대칭과 별도로 판정합니다.

정수 픽셀의 중심축과 두 픽셀 사이의 중심축을 구분합니다. 홀수 폭은 가운데 한 픽셀, 짝수 폭은 가운데 두 픽셀 사이를 축으로 삼습니다. 대칭을 맞추려고 한쪽만 늘리거나 가로·세로 비율을 따로 조정하지 않습니다.

### 인물 얼굴

인물 얼굴과 감정 얼굴은 작업 원본에서 5·7·9·13px처럼 홀수 폭을 사용합니다. 둥근 얼굴의 가로·세로 지름은 같게 두고, 원형 도트 마스크의 좌우와 위아래를 반사해 확인합니다. 눈은 축 양쪽에 같은 간격으로, 코·입의 중심은 같은 축에 놓습니다. 인물의 머리·목·어깨도 축을 공유합니다. 표정에 필요한 비대칭은 이유를 기록합니다.

16px처럼 짝수 캔버스에 홀수 얼굴을 넣으면 좌우 바깥 여백이 1px 다를 수 있습니다. 이 경우 얼굴 자체의 대칭을 우선합니다. 홀수 조건은 원본 격자 기준이며 2배 확대에서 7px가 14px가 되는 것은 정상입니다. 확대 후 홀수로 되돌리려고 픽셀을 추가하지 않습니다.

### 직선과 각도

수평은 0도, 수직은 90도, 대각선은 45도를 기본으로 사용합니다. 45도 선은 가로와 세로 이동량의 절댓값이 같습니다. 망치는 수평 머리와 수직 손잡이를 기본으로 하고 두 축은 90도로 만납니다. 복합 아이콘에서도 망치 자체를 임의로 기울이지 않습니다.

꺾쇠형 방향 기호는 두 45도 사선이 정확히 90도로 만나게 만듭니다. 방향 삼각형도 진행 방향의 꼭짓점을 90도로 맞춥니다. 다른 방향은 같은 원본의 90도 회전 또는 반사로 생성하며, 방향마다 따로 그리지 않습니다. 체크는 의미상 비대칭인 두 팔을 유지하고 X는 중심 대칭과 같은 획 두께를 유지합니다.

### 의미상 필요한 비대칭

책의 옆면, 한 방향을 향하는 신발·도구, 체크의 짧고 긴 팔, 집과 망치의 겹침처럼 비대칭이 의미를 전달할 때만 예외로 둡니다. 제작 목록에 사유와 각 구성요소의 축을 기록합니다. 기존 그림이 비대칭이라는 사실만으로 예외를 자동 인정하지 않습니다.

### 제작과 검수 순서

1. 용도·표시 크기와 대칭 가능 여부를 정하고 축·얼굴 지름·각도·예외 사유를 기록합니다.
2. 색을 넣기 전에 실루엣을 만들고 반사·회전으로 구조를 확인합니다.
3. 얼굴·몸·도구의 축을 맞춘 뒤 색과 명암을 넣습니다. 얼굴을 가로 또는 세로로만 리사이즈하지 않습니다.
4. 원본과 네 출력에서 반사 일치, 얼굴 홀수 지름, 화살표 직각, 획 두께 및 가독성을 검사합니다. 기호는 크기별 직접 출력, 사물·메뉴는 최근접 확대라는 기존 구분을 유지합니다.
5. 검사 결과와 외형 승인 상태를 분리해 기록합니다. 이전 아이콘은 새 규칙이 생겼다는 이유만으로 통과 처리하지 않고 개별 검수 상태를 남깁니다.

'''
rules=rules.replace('## 메뉴의 형태와 겹침',section+'## 메뉴의 형태와 겹침');rp.write_text(rules,encoding='utf-8')
lp=root/'pixelart-icon-change-log.md';s=lp.read_text(encoding='utf-8');s='<!-- CHANGELOG v1.6 · 2026-09-27 — 공통 UI 대칭 규칙과 12종 v4 반영 -->\n'+s
start=s.index('**현재 검토본');end=s.index('**',start+2)+2
s=s[:start]+'**현재 검토본은 v4 12종·v3 1종·v2 12종·v1 41종입니다. 얼굴 4종은 홀수 원형, EDIT는 일자 망치, 방향 기호 7종은 직각으로 수정했습니다. 좌우 대칭 우선·중심축·각도·예외 기록을 공통 UI 기준으로 적용합니다. 기존 나머지 아이콘의 새 기준 검토는 별도입니다.**'+s[end:]
for old,new in [('pixel-spec-icon.json` | 1.3','pixel-spec-icon.json` | 1.4'),('icon-production.md` | 1.4','icon-production.md` | 1.5'),('recordtales-icon-catalog.json` | 1.4','recordtales-icon-catalog.json` | 1.5')]:s=s.replace(old,new)
stamp=datetime.now().strftime('%Y-%m-%d %H:%M')
entry=f'### {stamp} — 홀수 얼굴·일자 망치·직각 방향과 공통 UI 기준\n\n사용자 요청을 반복 적용할 수 있도록 중심축·홀수 원형 얼굴·좌우 대칭 우선·0/45/90도 각도·비대칭 예외 기록·검수 절차를 사양과 제작 규칙에 반영했습니다. RECRUIT·ROSTER·감정 얼굴 2종, EDIT, 방향 기호 7종을 v4로 수정했습니다. 기존 파일은 보존하며 나머지 아이콘의 새 대칭 기준 검수 상태는 대기로 명시했습니다.\n\n'
s=s.replace('## 변경 이력 (최신이 위)\n\n','## 변경 이력 (최신이 위)\n\n'+entry);lp.write_text(s,encoding='utf-8')
qp=root/'pixelart-icon-remaining-work.md';s=qp.read_text(encoding='utf-8');s='<!-- CHANGELOG v1.6 · 2026-09-27 — v4 외형과 기존 UI 대칭 기준 검토 -->\n'+s
start=s.index('1. **현재 66종');end=s.index('\n2. **최종 등록**',start)
s=s[:start]+'1. **현재 66종 외형 및 공통 UI 기준 검토** — export/collection-v4에서 v4 12종·v3 1종·v2 12종·v1 41종을 확인합니다. 이번 수정 12종은 새 기준을 검사하며 나머지 54종은 목록의 ui_geometry_review 대기 항목을 검토합니다. 각 예외 사유도 확인합니다.'+s[end:]
start=s.index('- 메뉴 v3');end=s.index('\n',start)
s=s[:start]+'- 최신 수정본과 미승인 아이콘의 외형 승인. 기존 유색 대표 4종의 승인은 유지하지만 새 공통 UI 기준 검토는 별도입니다.'+s[end:]
qp.write_text(s,encoding='utf-8')
print('공통 UI 규칙·수치 사양·목록·현재 이력·검토 큐 갱신 완료')
