# pixelart-design

등신대 픽셀 아트 캐릭터의 규칙을 설계하고, 그 규칙으로 캐릭터를 만들어 Spine으로 보내는 작업
저장소입니다. 이 파일은 모든 작업이 따르는 규칙의 진입점입니다.

## 중앙 규칙

규칙의 정본은 `core/`이며 **중앙 저장소에서 받아 온 사본입니다**(받은 기록: `core/.source.json`).
이 저장소에서 `core/`를 고치지 않습니다 — 고칠 것은 `repo-remaining-work.md`의 「중앙에 되돌려
보낼 것」에 적고 중앙 저장소에서 고칩니다(`core/base/rules/central-sync.md`).

- 문서 제작 요청 → `core/base/doc-playbook.md`를 처음부터 끝까지 따릅니다. **확인 ① · ②를 받기
  전에는 본문을 쓰지 않습니다.**
- 요청 범위 밖의 수정은 제안만 합니다(`core/base/rules/change-scope.md`).
- 코드를 보여 줄 때(채팅 포함) → `core/base/rules/code-example.md`.
- 커밋 · push는 요청과 승인이 있을 때만 합니다(`core/base/rules/git-rules.md`).

## 이 저장소

| 자리 | 무엇 |
|---|---|
| `workspace.json` | 저장소 이름표 — 공개 범위 · 프로젝트를 찾을 자리 · 저장소 전체 모듈 |
| `repo-change-log.md` · `repo-remaining-work.md` | 저장소 설정과 중앙 받기의 이력 · 할 일 |
| `projects/` | 픽셀 아트 프로젝트들. 캐릭터 규칙 · 제작은 `pixel-art` 모듈을 켜서 합니다 |
| `RESOURCE_WORKFLOW.md` | 캐릭터·아이콘 최종본의 승인·등록·사용 절차 |
| `resources/` | 다른 프로젝트가 읽는 공용 최종 리소스와 목록 |

<!-- CHANGELOG v1.0 · 2026-09-27 — 공용 최종 리소스 절차와 폴더 진입점 추가 -->

## 이 저장소만의 규칙

- **응답 언어** — 사용자에게 보내는 모든 설명 · 보고 · 질문은 한국어로 씁니다. 코드 · 명령 · 경로 ·
  에러 원문만 원문 그대로 둡니다.

## 참조 규칙

<!-- gen:read-gates -->
| 경로 | 규칙 |
|---|---|
| `core/modules/` | **기본 참조 금지.** 프로젝트 모듈은 그 프로젝트의 `{폴더}-modules.json`에 켜져 있을 때만, 워크스페이스 모듈은 `workspace.json`의 `modules`에 있을 때만 읽습니다. `scope: host` 모듈은 그 컴퓨터의 환경을 다룰 때만 읽습니다 |
| 프로젝트의 change-log | 작업 전 **항상 먼저 읽습니다** — 「현행 기준」 블록이 현재 정본 · 용어 · 상시 규칙입니다. 작성 규칙은 `core/base/rules/change-log-writing.md` |
| 프로젝트의 remaining-work | 작업 전 **항상 먼저 읽습니다** — 할 일의 정본(다음 작업 큐 · 결정 대기 · 백로그). 규칙은 `core/base/rules/remaining-work.md` |
| `{폴더}-structure.json` | 등록된 자료의 경로 · 역할 · 참조 · 생성 관계의 정본입니다. 아래 기본 자리는 설정이 없는 프로젝트의 기본안입니다 |
| `spec/design/` | **참조 자유.** 확정 사양 — 기대값과 판정 기준은 여기서만 가져옵니다 |
| `spec/rationale/` | **참조 자유.** 판단 기록 — 확정안이 아니므로 기대값으로 쓰지 않습니다 |
| `spec/archive/` · 구조 설정의 archive 역할 | **기본 참조 금지.** 지나간 상태입니다. 사용자가 특정 기능의 행방 · 이력을 물을 때만 열어 「언제 삭제 · 수정되어 현재 미사용」 형태로 답합니다 |
| `analysis/` · `reference/` | 조사 자료입니다. 수치는 아직 남의 값이거나 미확정 값이라 기대값으로 쓰지 않습니다 — 확정되면 `spec/`으로 옮깁니다 |
| `core/.source.json` | 중앙 규칙을 받은 기록입니다. 손으로 고치지 않습니다 — `sync_core.py`가 씁니다 |
<!-- /gen:read-gates -->
