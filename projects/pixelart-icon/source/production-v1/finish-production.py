# CHANGELOG v1.0 · 2026-09-27 — 검사 통과 파일의 목록·요청문·검토 안내·진행 상태를 동기화합니다.
"""완성된 검토본의 목록과 제작 기록을 정리합니다."""
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import json

root = Path(__file__).resolve().parents[2]
source = Path(__file__).resolve().parent
review = root / 'export/collection-v1'
def read(path):
    return json.loads(path.read_text(encoding='utf-8'))
def write(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
validation = read(review / 'validation.json')
assert validation['status'] == 'passed' and len(validation['assets']) == 66
catalog_path = root / 'spec/design/recordtales-icon-catalog.json'
catalog = read(catalog_path)
catalog['revision'] = '1.2'
catalog['revision_note'] = '2026-09-27: 전체 66종 검토본·264개 출력·기술 검사와 대표 보존 완료'
catalog['art_status'] = 'full_set_review_pending'
for item in catalog['items']:
    group = 'representatives-v1' if item['representative'] else 'production-v1'
    item.update(version='v1', native_file=f'source/{group}/{item["id"]}-native-16.png',
                editable_file=f'sprites/{group}/{item["id"]}.aseprite',
                output_directory=f'export/{item["id"]}/v1')
    item['status'] = 'style_approved' if item['representative'] else 'review_pending'
write(catalog_path, catalog)
generation = read(source / 'generation.json')
for asset in generation['assets']:
    provenance = read(source / f'{asset["id"]}-provenance.json')
    assert provenance['status'] == 'generated'
    asset.update(provenance)
generation['status'] = 'generated_and_native_processed'
write(source / 'generation.json', generation)
groups = {'menu':'메뉴', 'symbol':'기호', 'category':'분류', 'ticket':'티켓',
          'emotion':'감정', 'order':'주문', 'action':'행동'}
lines = [
    '<!-- CHANGELOG v1.0 · 2026-09-27 — 전체 66종 검토본·배율·식별자·검사 근거 안내 -->',
    '# RecordTales 아이콘 66종 v1 검토', '',
    '대표 6종은 스타일 승인한 기존 파일을 유지했습니다. 새 60종은 외형 검토 대기이며, 전체 66종의 16px 원본과 16·32·48·64px 출력 264개는 기술 검사를 통과했습니다. 공용 resources 등록과 UE 화면 검수는 별도입니다.', '',
    '## 비교판', '',
    '- `all-64-dark.png`와 `all-64-light.png`: 8열, 왼쪽부터 오른쪽·위에서 아래 순서입니다. 아이콘은 64px로 표시합니다.',
    '- `all-32-dark.png`: 기본 제공 크기인 32px 비교판입니다.',
    '- `all-16-dark.png`: 최소 지원 크기인 16px 비교판입니다.',
    '- `{계열}-scales.png`: 한 행에 동일 아이콘을 16·32·48·64px 순서로 배치했습니다.',
    '- 밝은 배경 비교판에서 흰색 단색 아이콘은 짙은 회색으로 색을 입혔습니다. 실제 PNG는 흰색입니다.',
    '- 뷰어가 비교판을 축소하면 실제 화면 크기가 달라집니다. 크기를 판정할 때는 이미지를 100%로 봅니다.', '',
    '## 파일 규격과 위치', '',
    '프로젝트 루트 기준 `export/{식별자}/v1/icon-{크기}.png`를 사용합니다. 32px를 기본 크기로 정했으며, 50·100·150·200%는 각각 16·32·48·64px 파일에 대응합니다. 배율별 출력은 16px 원본의 정확한 최근접 정수배이고 확대 후 보정은 없습니다.', '',
    '편집 파일은 `sprites/representatives-v1/`의 6개와 `sprites/production-v1/`의 60개입니다. 모두 실제 16×16 RGB Aseprite 파일입니다.', '',
    '## 제작과 검사 근거', '',
    '내장 image_gen으로 각 아이콘을 따로 생성한 구상 시안·요청문은 source의 두 버전 폴더에 보관했습니다. 생성 결과의 큰 해상도를 도트 원본으로 취급하지 않습니다. Aseprite에서 내용 영역을 16px 격자에 정리하고 제한 팔레트와 이진 알파로 출력했습니다. 필요한 보정도 16px 원본에만 적용했습니다.', '',
    '`source/production-v1/generation.json`은 새 60종 요청문과 생성 출처입니다. `build-report.json`에는 실제 생성 크기·내용 경계·팔레트가 있습니다. `native-overrides.json`과 `face-refinements.json`은 원본 보정 이유와 도트 배치를 담습니다.', '',
    '`validation.json`은 66종·264개 PNG의 크기, 최근접 RGBA 일치, 알파 0/255, 가시 RGB 각 채널 10 이상, 단색 방식, 최소 1px 여백, Aseprite 헤더 및 승인 대표 6종의 해시 보존 검사입니다. 기술 검사 통과가 새 60종의 사용자 외형 승인을 뜻하지는 않습니다.', '',
    '## 번호와 의미', '',
    '| 비교판 번호 | 식별자 | 계열 | 의미 | 외형 상태 |',
    '|---|---|---|---|---|'
]
for i,a in enumerate(catalog['items'],1):
    lines.append(f'| {i:02} | {a["id"]} | {groups[a["group"]]} | {a["label"]} | {"대표 승인" if a["representative"] else "검토 대기"} |')
(review / 'README.md').write_text('\n'.join(lines)+'\n', encoding='utf-8')
log_path = root / 'pixelart-icon-change-log.md'
log = log_path.read_text(encoding='utf-8')
assert '전체 66종 검토본과 264개 출력 제작 완료' not in log, '완료 이력이 이미 있습니다.'
stamp = datetime.now(ZoneInfo('Asia/Seoul')).strftime('%Y-%m-%d %H:%M')
log = '<!-- CHANGELOG v1.3 · 2026-09-27 — 전체 66종 검토본과 264개 출력 제작 완료 -->\n' + log
log = log.replace('**대표 6종 v1 스타일을 승인받아 같은 방식으로 나머지 60종을 제작하고 있습니다. 새 60종의 외형 승인과 최종 리소스 등록은 별도입니다.**', '**승인 대표 6종을 보존하고 새 60종을 제작하여 전체 66종 검토본과 264개 출력을 완성했습니다. 기술 검사는 통과했으며 새 60종 외형 승인·공용 등록·UE 검수는 별도입니다.**')
log = log.replace('| `spec/design/recordtales-icon-catalog.json` | 1.1 |', '| `spec/design/recordtales-icon-catalog.json` | 1.2 |')
entry = f'### {stamp} — 전체 66종 검토본과 264개 출력 제작 완료\n\n승인 스타일로 후속 60종을 내장 image_gen에서 개별 생성하고 Aseprite의 실제 16px 원본으로 정리했습니다. 네 크기 PNG 총 264개와 편집 원본 66개, 전체·계열별 비교판, 요청문과 출처·검사 기록을 보존했습니다. 크기·색·알파·여백·최근접 일치와 대표 6종 출력 해시 보존 검사를 통과했습니다. 새 60종은 검토 대기이며 UE 파일과 resources에는 반영하지 않았습니다.\n\n'
log = log.replace('## 변경 이력 (최신이 위)\n\n', '## 변경 이력 (최신이 위)\n\n'+entry)
log_path.write_text(log,encoding='utf-8')
queue_path = root / 'pixelart-icon-remaining-work.md'
queue = queue_path.read_text(encoding='utf-8')
queue = '<!-- CHANGELOG v1.3 · 2026-09-27 — 제작 완료에 따라 전체 외형 검토를 다음 순서로 갱신 -->\n' + queue
start = queue.index('1. **나머지 60종 제작과 전체 검토**')
end = queue.index('\n2. **최종 등록**', start)
queue = queue[:start] + '1. **전체 66종 외형 검토** — 대표 6종은 승인 완료, 새 60종은 검토 대기입니다. export/collection-v1의 전체·배율별 비교판에서 식별성과 계열 간 일관성을 확인합니다. 수정은 16px 원본에서 진행합니다.' + queue[end:]
queue = queue.replace('전체 비교판을 만든 뒤 확인합니다.', 'export/collection-v1/README.md와 비교판에서 확인합니다.')
queue_path.write_text(queue,encoding='utf-8')
print('66종 목록·출처·검토 안내·현행 기준·작업 큐 갱신 완료')
