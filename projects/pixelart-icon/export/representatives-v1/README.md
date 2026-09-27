<!-- CHANGELOG v1.1 · 2026-09-27 — 대표 스타일 승인과 전체 검토본 연결 -->
<!-- CHANGELOG v1.0 · 2026-09-27 — 대표 6종 비교판과 검토 파일 안내 -->
# 대표 아이콘 6종 v1 검토

이 파일들은 승인된 대표 6종 v1입니다. 승인 근거와 기존 출력 해시는 `source/production-v1/representative-approval.json`에 보존했습니다. 전체 66종 검토본은 `export/collection-v1/README.md`에서 확인합니다. 경로는 아이콘 프로젝트 루트 기준입니다. Unreal Engine 실제 화면 검수와 공용 resources 등록은 별도입니다.

## 비교판 읽기

`comparison.png`의 열은 왼쪽부터 아래 순서입니다.

| 열 | 파일 식별자 | 의미 |
|---|---|---|
| 1 | cmd_settings | 환경 설정 |
| 2 | sym_close | 닫기 |
| 3 | icon_book | 책·공부 |
| 4 | tpl_idea | 아이디어 |
| 5 | order_restaurant | 음식 주문 |
| 6 | act_cook | 요리 행동 |

위 두 줄은 16px 원본을 6배 확대한 96px 보기입니다. 어두운 배경과 밝은 배경을 비교합니다.
첫 두 단색 아이콘은 게임에서 색을 입히는 상황을 보여 주려고 금색·짙은 회색으로 표시했습니다.
실제 단색 PNG는 흰색입니다. 아래 네 줄은 차례로 16·32·48·64px 출력입니다.
비교판 자체를 이미지 뷰어가 확대·축소하면 화면상의 실측 크기는 달라집니다.

## 원본과 출력

16px 원본은 `source/representatives-v1/{식별자}-native-16.png`, 편집 원본은
`sprites/representatives-v1/{식별자}.aseprite`입니다. 경로는 아이콘 프로젝트 루트 기준입니다.
네 출력은 `export/{식별자}/v1/icon-16.png`, `icon-32.png`, `icon-48.png`, `icon-64.png`입니다.
내장 image_gen으로 생성한 고해상도 시안·요청문과 Aseprite 정리 Lua는 source/representatives-v1에 보존했습니다.

`validation.json`은 크기·색상 하한·단색·알파·여백·최근접 RGBA 일치 검사와 파일 해시를 담습니다.
이곳의 검사 JSON은 최초 시안 제작 시점의 기록입니다. 이후 대표 6종은 스타일 승인을 받았으며, 최신 전체 검사와 검토 상태는 `export/collection-v1/validation.json` 및 제작 목록에 기록했습니다.
