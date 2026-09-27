# CHANGELOG v1.0 · 2026-09-27 — 대표 시안 승인과 기존 파일 해시 보존
"""승인된 대표 시안의 범위와 파일 해시를 기록합니다."""
from pathlib import Path
import json
from datetime import datetime
from zoneinfo import ZoneInfo

root = Path(__file__).resolve().parents[2]
source = Path(__file__).resolve().parent
assert not (source / 'representative-approval.json').exists(), '이미 승인 기록이 있습니다. 중복 실행하지 않습니다.'
stamp = datetime.now(ZoneInfo('Asia/Seoul')).strftime('%Y-%m-%d %H:%M')
def read(path):
    return json.loads(path.read_text(encoding='utf-8'))
def write(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

catalog_path = root / 'spec/design/recordtales-icon-catalog.json'
catalog = read(catalog_path)
catalog['revision'] = '1.1'
catalog['revision_note'] = '2026-09-27: 대표 6종 스타일 승인과 나머지 60종 제작 착수'
catalog['art_status'] = 'remaining_60_in_production'
for item in catalog['items']:
    if item['representative']:
        item['approval'] = 'approved'
        item['status'] = 'style_approved'
    else:
        item['status'] = 'in_production'
write(catalog_path, catalog)
prior = read(root / 'export/representatives-v1/validation.json')
write(source / 'representative-approval.json', {
    'revision': '1.0', 'recorded_at': stamp,
    'basis': '대표 6종을 기준으로 나머지 60종을 진행하겠다는 안내에 사용자가 네 진행해주세요라고 답했습니다.',
    'scope': '대표 6종 v1 스타일 승인과 동일 방식의 나머지 제작 승인',
    'excluded': '새 60종의 개별 외형 승인·공용 등록·UE 연결',
    'assets': [{'id': a['id'], 'files': a['files']} for a in prior['assets']]
})
rules_path = root / 'rules/icon-production.md'
rules = rules_path.read_text(encoding='utf-8')
rules = '<!-- CHANGELOG v1.2 · 2026-09-27 — 대표 6종 승인 스타일을 후속 제작 기준으로 반영 -->\n' + rules
rules = rules.replace('팔레트·외곽선 두께·여백은 첫 아이콘 계열을 승인할 때 확정합니다.', '대표 6종 v1의 표현 밀도와 색상 방식을 후속 제작 기준으로 사용합니다. 개별 사물의 새 팔레트와 외형은 전체 검토에서 확인합니다.')
rules = rules.replace('첫 시안은 원본 격자에서 사방 1px 이상 여백과 제한된 팔레트를 후보로 비교하며, 이 후보를 아직 전체 계열의 확정 스타일로 보지 않습니다.', '대표 6종 v1은 사용자 승인한 스타일 기준입니다. 원본 격자에서 사방 1px 이상 투명 여백을 유지하고, 유색 아이콘은 대표 시안의 짙은 윤곽과 제한된 명암을 따릅니다. 승인 근거와 파일 해시는 source/production-v1/representative-approval.json에 보존합니다.')
rules_path.write_text(rules, encoding='utf-8')
log_path = root / 'pixelart-icon-change-log.md'
log = log_path.read_text(encoding='utf-8')
log = '<!-- CHANGELOG v1.2 · 2026-09-27 — 대표 6종 스타일 승인과 후속 제작 착수 -->\n' + log
log = log.replace('**66종 범위와 대표 6종 검토 절차를 승인받았습니다. 대표 6종 v1의 실제 16px 원본과 네 크기 검토본을 제작했습니다. 스타일·최종 리소스 승인은 별도입니다.**', '**대표 6종 v1 스타일을 승인받아 같은 방식으로 나머지 60종을 제작하고 있습니다. 새 60종의 외형 승인과 최종 리소스 등록은 별도입니다.**')
log = log.replace('| `rules/icon-production.md` | 1.1 |', '| `rules/icon-production.md` | 1.2 |').replace('| `spec/design/recordtales-icon-catalog.json` | 1.0 |', '| `spec/design/recordtales-icon-catalog.json` | 1.1 |')
entry = f'### {stamp} — 대표 6종 스타일 승인과 나머지 60종 제작 착수\n\n사용자 진행 승인에 따라 대표 6종 v1을 후속 스타일 기준으로 기록했습니다. 기존 네 출력의 해시를 보존하고 새 작업을 source/production-v1과 sprites/production-v1로 분리했습니다. 공용 등록과 UE 적용 승인은 포함하지 않습니다.\n\n'
log = log.replace('## 변경 이력 (최신이 위)\n\n', '## 변경 이력 (최신이 위)\n\n' + entry)
log_path.write_text(log, encoding='utf-8')
queue_path = root / 'pixelart-icon-remaining-work.md'
queue = queue_path.read_text(encoding='utf-8')
queue = '<!-- CHANGELOG v1.2 · 2026-09-27 — 대표 승인 완료와 나머지 60종 제작 진행 -->\n' + queue
queue = queue.replace('1. **대표 6종 검수와 승인** — cmd_settings·sym_close·icon_book·tpl_idea·order_restaurant·act_cook을 16·32·48·64px와 밝고 어두운 배경에서 확인합니다. 산출물: 승인된 스타일·파일·버전 기록.\n2. **전체 아이콘 제작** — 대표 시안 승인 후', '1. **나머지 60종 제작과 전체 검토** — 대표 6종 승인 완료. 동일한 스타일로')
queue = queue.replace('3. **최종 등록**', '2. **최종 등록**').replace('4. **UE 연결**', '3. **UE 연결**')
queue = queue.replace('- 대표 6종의 외형·팔레트·외곽선·여백 승인. 제작 범위와 배율 규격은 승인 완료입니다.', '- 새 60종의 개별 외형 승인 — 전체 비교판을 만든 뒤 확인합니다. 대표 6종 스타일과 제작 범위·배율은 승인 완료입니다.')
queue_path.write_text(queue, encoding='utf-8')
print('대표 6종 승인 기록·해시 보존·현행 기준과 큐 갱신 완료')
