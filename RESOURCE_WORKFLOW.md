<!-- CHANGELOG v1.2 · 2026-09-28 — (변경) 캐릭터 320 무패딩 배포·방향별 동작 등록 -->
<!-- CHANGELOG v1.1 · 2026-09-27 — (추가) 캐릭터 512 배포와 패딩·기준점 검수 연결 -->
<!-- CHANGELOG v1.0 · 2026-09-27 — 최종 리소스 등록·사용 규칙과 등록서 형식 -->
# 최종 그래픽 리소스 관리

`projects/pixelart-character/`와 `projects/pixelart-icon/`은 제작 자리입니다. 다른 프로젝트는
저장소 루트의 `resources/`만 가져갑니다. 이 폴더에는 승인과 필수 검수를 마친 배포 파일만 둡니다.
공통 배포 폴더는 이 저장소가 소유하며, 제작 원본은 각 프로젝트가 소유합니다.

## 제작과 등록

1. `source/`에서 시안·작업본을 관리하고, `sprites/`에 편집 원본을 보존합니다.
2. `export/`로 정지 PNG·애니메이션 시트를 출력합니다. 비교 이미지와 미리보기도 여기에 둘 수 있습니다.
3. 실제 내보낼 파일을 대상으로 사용자의 최종 승인과 프로젝트별 필수 검수를 완료합니다.
4. 프로젝트 `releases/`에 등록서를 작성합니다. 파일의 SHA-256, 승인자·날짜·근거와 외형·프로젝트 사양·권리 검수를 기록합니다.
5. `tools/resource_pack.py register`로 먼저 검사하고, 통과한 등록서에 `--publish`를 붙여 실제 등록합니다.
6. `tools/resource_pack.py check`로 최종 폴더를 검사합니다.

승인 문구를 임의로 작성하거나 폴더 이름만으로 최종본을 판단하지 않습니다. 도구는 기록의 완결성과
파일 해시를 검사하지만, 기록이 실제 사용자 승인인지 또는 그림의 외형이 좋은지 판단하지 못합니다.
승인 근거는 실제 대화·검수 기록을 가리켜야 합니다. 체크를 모두 true로 만드는 것이 검수를 대신하지 않습니다.
공개 저장소이므로 자작 여부·출처·사용 권리 검수도 등록 전에 완료합니다.

## 파일과 버전

- 식별자는 `characters.ice-queen`, `icons.items.ice-crystal`처럼 종류와 이름을 점으로 구분합니다.
- 버전은 `v1`, `v2`처럼 증가시킵니다. 등록한 버전은 덮어쓰거나 직접 수정하지 않습니다.
- 경로는 식별자의 점을 `/`로 바꾼 뒤 버전을 붙입니다. 예: `icons/items/ice-crystal/v1/`.
- `manifest.json`은 식별자·버전·종류·`asset.json` 상대 경로를 나열합니다. 자동으로 최신 버전을 고르지 않습니다.
- `asset.json`의 파일 경로는 해당 `asset.json` 폴더 기준입니다. 파일 크기·해시·표시 방식과 필요한 동작 정보를 포함합니다.
- PNG 이름에는 작업 단계나 제작 버전 대신 `still.png`, `icon-32.png`, `walk.png`처럼 사용 목적을 씁니다. 배포 버전은 폴더가 담당합니다.
- 등록서는 제작 프로젝트에 남깁니다. 최종 폴더에는 파일의 소비에 필요한 정보만 들어가며 제작 경로·개인 컴퓨터 절대 경로는 넣지 않습니다.
- 미리보기 GIF, 비교 이미지, Lua·Python, 편집 원본은 최종 폴더에 넣지 않습니다.

PNG는 실제 투명 배경·알파 0/255·가시 RGB 각 채널 10 이상을 지킵니다. 투명한 픽셀의 RGB는
색상 하한 검사에서 제외합니다. 전체 외형·팔레트·격자·얼굴 마스크·접지처럼 종류별 검사는
해당 제작 프로젝트에서 마친 뒤 `review`에 근거를 남깁니다.

## 캐릭터 배포 규격

캐릭터는 프로젝트 규칙서 v1.13과 두 사양 JSON의 `delivery`를 따릅니다. 160 작업에서 만든
320 그림을 추가 패딩 없이 실제 320×320 투명 PNG로 배포합니다. `default_file`은 승인된 320
정지 파일이며 `pivot`은 왼쪽 위 픽셀 경계 기준 [160,304]입니다. 애니메이션 `frame_size`도
[320,320]이고 `rect`는 시트 안의 320 프레임 영역입니다. 시트 전체 크기에 2의 거듭제곱을 강제하지 않습니다.

좌향·우향 idle·walk는 별도 검수·승인한 파일을 사용합니다. 동작 식별자와 파일명에 방향을 포함하고
단순 반전을 최종 리소스로 등록하지 않습니다. 기본 `facing`은 기본 정지 그림의 방향을 나타내며
모든 동작의 방향을 대신하지 않습니다. 소비 프로젝트의 방향별 동작 매핑도 등록 전에 확인합니다.

등록 전 승인된 320 원본과 배포 파일의 RGBA 일치·기준점·방향·프로젝트 검수 근거를 기록합니다.
얼굴 마스크·보정 레이어·편집 원본은 제작 폴더에 보존합니다. 엔진에서는 NoMipmaps·Nearest·
Never Stream·추가 패딩 없음을 기준으로 실제 표시를 검수합니다. 기존 도구의 자동 적용이나 엔진
검수 완료를 의미하지 않습니다. 실제 파일의 승인·해시를 기록한 뒤 등록하며 이전 512 결과는 이력으로 보존합니다.

## 등록서 형식

파일 자리는 `projects/{프로젝트}/releases/{식별자}-{버전}.json`입니다.
아래는 형식 설명이며 실제 승인이나 실제 리소스를 뜻하지 않습니다. 제공하는 예제 파일
`tools/examples/icon-release.pending.json`은 pending 상태이므로 등록되지 않습니다.
이 예제를 소유 프로젝트의 `releases/`에 복사한 뒤 실제 파일과 승인·검수 기록으로 채웁니다.

| 필드 | 내용 |
|---|---|
| `schema_version` | 현재 1 |
| `project` | 소유 프로젝트 폴더 이름 |
| `id`, `version`, `kind` | 고정 식별자, v1 형식, character 또는 icon |
| `default_file` | 기본으로 사용할 등록 파일 이름 |
| `files` | source·name·role·size·sha256을 담은 배열 |
| `files[].source` | 소유 프로젝트 기준 `export/` 안의 상대 경로 |
| `files[].name`, `role` | 배포 PNG 이름, still·icon·sheet 중 하나 |
| `files[].size` | 예상 가로·세로 크기 배열. 실제 PNG와 다르면 실패 |
| `files[].sha256` | 사용자가 검토한 파일 바이트의 SHA-256 |
| `approval` | status=approved, by, at, evidence. 실제 승인 근거 필수 |
| `review` | status=passed, by, at, evidence, checks |
| `review.checks` | visual·project_spec·rights를 포함하여 모든 항목이 true |
| `facing`, `pivot` | 캐릭터 필수. left·right·front와 기본 그림의 왼쪽 위 기준 [x,y] 픽셀 기준점 |
| `animations` | 동작 이름별 file·frame_size·loop·frames. 각 프레임은 rect=[x,y,w,h], duration_ms |

아이콘은 16 작업본을 16·32·48·64px로 최근접 확대해 각각 등록하고 `icon-32.png`를 기본 파일로
지정합니다. 요청한 표시 크기의 파일을 선택하여 다시 소수배 확대하지 않습니다. 고해상도 화면의
배율과 최종 화면 픽셀 정렬은 소비하는 UI가 함께 관리해야 합니다.

## 실행

Python과 Pillow 13 이상이 필요합니다. 아래 명령은 저장소 루트에서 실행합니다.
`tools/resource_pack.py`의 명령행 사용 예이며, 등록서는 실제 승인·검수 후 작성한 파일을 지정합니다.

```powershell
# tools/resource_pack.py — 검사만 수행하며 파일을 등록하지 않습니다.
python tools/resource_pack.py register projects/pixelart-icon/releases/ice-crystal-v1.json
# 같은 등록서를 확인한 뒤 로컬 최종 폴더에 등록합니다. 원격 전송은 없습니다.
python tools/resource_pack.py register projects/pixelart-icon/releases/ice-crystal-v1.json --publish
# 최종 폴더의 목록·파일·해시·크기·색상·시트 범위를 검사합니다.
python tools/resource_pack.py check
```

동시에 두 등록을 실행하면 잠금으로 한쪽이 중단됩니다. 강제 종료 후 `.publish.lock`이 남았다면
등록 프로세스가 끝났는지 확인하고 남은 임시 파일·목록 일관성을 점검한 뒤 재시도합니다.
등록 중 실패는 새 버전을 정리하며 기존 버전은 건드리지 않습니다.

## 다른 프로젝트에서 사용

`resources/` 전체를 복사하고 `manifest.json`에서 원하는 식별자와 **정확한 버전**을 찾습니다.
목록의 상대 경로로 `asset.json`을 읽은 뒤 기본 PNG 또는 원하는 크기·동작 파일을 읽습니다.
이미지는 최근접 방식으로 표시하고 PNG 알파를 사용합니다. 캐릭터는 pivot과 facing을 적용합니다.
애니메이션은 frame_size와 각 rect·duration_ms·loop를 사용합니다. 이 과정에 `projects/` 접근은 필요하지 않습니다.

현재 최종 목록은 비어 있습니다. 기존 얼음여왕 v2는 디자인 선택 상태이며 전체 프로젝트 검수와
배포 대상 파일 승인이 완료되기 전까지 자동 등록하지 않습니다. 기존 파일은 이동하지 않습니다.
