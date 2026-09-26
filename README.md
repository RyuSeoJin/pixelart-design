# pixelart-design

등신대 픽셀 아트 캐릭터를 같은 비율 · 같은 선 · 같은 색 규칙으로 만들고, 한 Spine 뼈대에 스킨만 갈아
끼워 움직이게 하는 작업 저장소입니다.

## 구성

| 자리 | 무엇 |
|---|---|
| `core/` | 중앙 저장소에서 받은 규칙 사본 — 이 저장소에서 고치지 않습니다 |
| `projects/` | 프로젝트 폴더. 프로젝트마다 change-log · remaining-work · 사양 파일을 둡니다 |
| `repo-change-log.md` · `repo-remaining-work.md` | 저장소 설정 · 중앙 받기 이력과 할 일 |

## 쓰는 모듈

| 모듈 | 무엇 |
|---|---|
| `pixel-art` | 스타일 규칙 · 그림 → 픽셀 변환 절차 · 검수 · 공유 Spine 뼈대 (프로젝트마다 켭니다) |
| `aseprite` | Aseprite 배치 실행 · MCP 연결 점검 (호스트 모듈 — 켜지 않고 점검만 합니다) |

## 중앙 규칙 다시 받기

```bash
python core/base/scripts/sync_core.py --from https://github.com/RyuSeoJin/rsj-centralized-control --check
python core/base/scripts/sync_core.py --from https://github.com/RyuSeoJin/rsj-centralized-control
```
