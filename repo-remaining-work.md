# repo-remaining-work — 이 저장소의 설정 · 구조에 남은 일

끝난 항목은 지웁니다. 규칙은 `core/base/rules/remaining-work.md`입니다.

---

## 다음 작업 큐

1. **첫 프로젝트 만들기** — `new_project.py`로 골격을 세우고 `pixel-art` 모듈을 켭니다. 지금까지의 작업
   (치비 실험 · 레퍼런스 보드 분석 · 규칙 전환 판단)을 그 프로젝트의 이력 · 분석 · 판단 기록으로
   옮깁니다. 산출물: 프로젝트 폴더 · 프로젝트 change-log

## 중앙에 되돌려 보낼 것

받아 쓰다 발견한 중앙 규칙의 문제입니다. 이 저장소의 `core/`는 고치지 않고, 중앙 저장소에서 고친 뒤
다시 받습니다(`core/base/rules/central-sync.md` §3).

아직 없습니다.

## 사용자 결정 대기

- **push 때 검사** — 중앙 받기 확인은 매일 돌지만, push할 때 규칙 검사(`check_rules.py`) · 모듈
  점검을 돌리는 워크플로는 아직 없습니다. 둘지 정합니다.

## 백로그

- **Actions가 PR을 만들 수 있게 허용** — 저장소 Settings ▸ Actions ▸ General ▸ Workflow permissions의
  「Allow GitHub Actions to create and approve pull requests」가 꺼져 있으면 받기 PR 단계가 실패합니다.
  첫 수동 실행(Actions ▸ central-sync ▸ Run workflow)으로 확인합니다.
- **예약 실행 정지** — 공개 저장소는 60일 동안 활동이 없으면 GitHub이 예약 워크플로를 멈춥니다.
  멈추면 Actions 탭에서 다시 켭니다.
- 루트 구조도 — 프로젝트 구조가 잡힌 뒤 만듭니다(중앙 이력 2026-09-27 23:30 태그 ③).
