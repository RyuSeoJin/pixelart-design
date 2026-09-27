# CHANGELOG v1.0 · 2026-09-27 — 메뉴 4종 v3 구성 변경과 직선 기준 기록
"""메뉴 수정본의 현재 경로와 검토 상태를 기록합니다."""
from pathlib import Path
import json, hashlib
from datetime import datetime
root=Path(__file__).resolve().parents[2];source=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
cp=root/'spec/design/recordtales-icon-catalog.json';cat=read(cp)
assert cat['revision']=='1.3','이미 반영한 갱신은 다시 실행하지 않습니다.'
write(source/'catalog-before-v3.json',cat)
baseline={}
for a in cat['items']:
    for size in (16,32,48,64):
        p=root/a['output_directory']/f'icon-{size}.png'
        baseline[p.relative_to(root).as_posix()]=hashlib.sha256(p.read_bytes()).hexdigest()
write(source/'previous-current-hashes.json',baseline)
changes={'cmd_recruit':'인물과 정보 줄이 있는 서류','cmd_roster':'단일 인물의 머리와 어깨','cmd_edit':'집 뒤 레이어와 전경 망치의 겹침','cmd_settings':'직선 톱니·사각 중심·좌우상하 대칭'}
for a in cat['items']:
    if a['id'] in changes:
        a.update(version='v3',status='review_pending',approval='pending',output_directory=f'export/{a["id"]}/v3',editable_file=f'sprites/menu-v3/{a["id"]}.aseprite',native_file=f'source/menu-v3/{a["id"]}-native-16.png')
cat.update(revision='1.4',revision_note='2026-09-27: 사용자 요청한 메뉴 4종의 구성·직선 톱니 v3 적용',art_status='mixed_v3_review_pending');write(cp,cat)
write(source/'provenance.json',{'revision':'1.0','method':'Aseprite 16px 직접 도트 수정과 정수배 출력','changes':changes,'reference_use':'사용자 첨부는 구성 참고만 사용하고 복제하지 않았습니다.','palette':['342D46','4F91CF','8DCDF0','EDB547','FFE29A','FFF0CD','E6C897'],'layers_cmd_edit':['집 몸체','지붕','문','망치 손잡이','망치 머리'],'approval':'pending'})
sp=root/'spec/design/pixel-spec-icon.json';v=read(sp);v['revision']='1.3';v['revision_note']='2026-09-27: 수정 대표의 승인 대상을 최신 버전으로 명시, 크기·출력 규격 유지';v['representative_gate']['note']='v1 대표 승인 기록입니다. 수정된 대표 아이콘은 최신 버전의 외형 승인을 별도로 받습니다.';write(sp,v)
rp=root/'rules/icon-production.md';s=rp.read_text(encoding='utf-8');s='<!-- CHANGELOG v1.4 · 2026-09-27 — 메뉴의 직선·대칭·도구 겹침 기준 -->\n'+s
s=s.replace('## 기호 도형 제작','## 메뉴의 형태와 겹침\n\n메뉴는 수평·수직 면과 일정한 계단 대각선을 기본으로 구성합니다. 톱니바퀴처럼 기계적인 형태는 곧은 톱니와 좌우·상하 대칭을 유지합니다. 작은 곡률을 잘게 나누기보다 읽히는 면과 모서리를 먼저 정합니다.\n\n도구와 사물은 의미가 명확하도록 겹쳐 배치할 수 있습니다. EDIT는 집을 뒤에, 망치를 앞에 두고 짙은 외곽선으로 두 형태를 구분합니다. RECRUIT는 인물 정보가 있는 서류, ROSTER는 한 명의 인물로 표현합니다.\n\n## 기호 도형 제작')
rp.write_text(s,encoding='utf-8')
lp=root/'pixelart-icon-change-log.md';s=lp.read_text(encoding='utf-8');s='<!-- CHANGELOG v1.5 · 2026-09-27 — 메뉴 4종 v3와 직선 형태 반영 -->\n'+s
s=s.replace('**메뉴·기호 23종을 색상 v2로 수정했습니다. 현재 검토본은 v2 23종과 기존 유색 v1 43종입니다. 기호 14종은 도형에서 크기별 직접 출력하며, 사물·메뉴는 16px 정수배 방식을 유지합니다. 외형 승인·공용 등록·UE 검수는 별도입니다.**','**현재 검토본은 메뉴 v3 4종·v2 19종·유색 v1 43종입니다. RECRUIT는 서류, ROSTER는 단일 인물, EDIT는 전경 망치, SETTINGS는 직선 톱니로 수정했습니다. 기호 14종은 크기별 도형 출력, 나머지는 16px 정수배 방식입니다. 외형 승인·공용 등록·UE 검수는 별도입니다.**')
s=s.replace('| `spec/design/pixel-spec-icon.json` | 1.2 |','| `spec/design/pixel-spec-icon.json` | 1.3 |').replace('| `rules/icon-production.md` | 1.3 |','| `rules/icon-production.md` | 1.4 |').replace('| `spec/design/recordtales-icon-catalog.json` | 1.3 |','| `spec/design/recordtales-icon-catalog.json` | 1.4 |')
stamp=datetime.now().strftime('%Y-%m-%d %H:%M')
entry=f'### {stamp} — 메뉴 4종의 서류·인물·겹침·직선 톱니 수정\n\n사용자 요청에 따라 RECRUIT는 서류, ROSTER는 한 명, EDIT는 집 위에 망치를 겹친 구성, SETTINGS는 직선 톱니로 바꿨습니다. Aseprite의 16px 원본과 4배율 v3 출력 16개를 저장했습니다. 기존 버전은 보존하고 직선·대칭·도구 겹침 기준을 제작 규칙에 기록했습니다. 첨부 참고 이미지는 복제하지 않았습니다.\n\n'
s=s.replace('## 변경 이력 (최신이 위)\n\n','## 변경 이력 (최신이 위)\n\n'+entry);lp.write_text(s,encoding='utf-8')
qp=root/'pixelart-icon-remaining-work.md';s=qp.read_text(encoding='utf-8');s='<!-- CHANGELOG v1.5 · 2026-09-27 — 메뉴 4종 v3 검토 대상으로 갱신 -->\n'+s
s=s.replace('메뉴·기호 v2 23종과 유색 v1 43종을 export/collection-v2에서 확인합니다.','메뉴 v3 4종·v2 19종·유색 v1 43종을 export/collection-v3에서 확인합니다.').replace('cmd_settings·sym_close는 v2 재승인','cmd_settings v3·sym_close v2는 재승인').replace('메뉴·기호 v2 23종 및','메뉴 v3 4종·v2 19종 및')
qp.write_text(s,encoding='utf-8')
print('메뉴 4종 v3 경로·구성 기준·이력·검토 큐 갱신 완료')
