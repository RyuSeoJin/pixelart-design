# repo-change-log — 이 저장소의 설정 변경과 중앙 규칙 받기 이력

저장소 설정(`workspace.json` · 진입점)의 변경과, 중앙 저장소에서 `core/`를 받은 기록을 남깁니다.
프로젝트 안의 변경은 각 프로젝트의 change-log에 적습니다. 작성 규칙은
`core/base/rules/change-log-writing.md`입니다.

---

## 변경 이력 (최신이 위)

### 2026-09-27 08:24 — 중앙 저장소 템플릿 사본을 받는 저장소로 전환

이 저장소는 GitHub에서 중앙 저장소를 템플릿으로 삼아 만들어, 중앙 저장소의 이름표 · 진입점 ·
이력 · 게이트까지 그대로 들고 있었습니다. 그대로 두면 이 저장소에서 `core/`를 고쳐도 되는 것처럼
읽히고, 중앙 게이트가 `projects/` 아래 파일을 막아 프로젝트를 올릴 수 없습니다(사용자 결정으로 전환).

- `workspace.json`을 이 저장소 값(`pixelart-design` · 공개)으로 바꿨습니다.
- `CLAUDE.md`를 받는 저장소 서식으로, `README.md`를 이 저장소 소개로 바꿨습니다.
- 중앙 이력(`center-change-log.md` · `center-remaining-work.md` · `archive/`)과 중앙 게이트
  (`.github/workflows/central-gate.yml`)를 지웠습니다. 원본은 중앙 저장소에 그대로 있습니다.
- `repo-change-log.md` · `repo-remaining-work.md`를 새로 두었습니다.
