<!-- CHANGELOG v1.0 · 2026-09-27 — 전체 66종 검토본·배율·식별자·검사 근거 안내 -->
# RecordTales 아이콘 66종 v1 검토

대표 6종은 스타일 승인한 기존 파일을 유지했습니다. 새 60종은 외형 검토 대기이며, 전체 66종의 16px 원본과 16·32·48·64px 출력 264개는 기술 검사를 통과했습니다. 공용 resources 등록과 UE 화면 검수는 별도입니다.

## 비교판

- `all-64-dark.png`와 `all-64-light.png`: 8열, 왼쪽부터 오른쪽·위에서 아래 순서입니다. 아이콘은 64px로 표시합니다.
- `all-32-dark.png`: 기본 제공 크기인 32px 비교판입니다.
- `all-16-dark.png`: 최소 지원 크기인 16px 비교판입니다.
- `{계열}-scales.png`: 한 행에 동일 아이콘을 16·32·48·64px 순서로 배치했습니다.
- 밝은 배경 비교판에서 흰색 단색 아이콘은 짙은 회색으로 색을 입혔습니다. 실제 PNG는 흰색입니다.
- 뷰어가 비교판을 축소하면 실제 화면 크기가 달라집니다. 크기를 판정할 때는 이미지를 100%로 봅니다.

## 파일 규격과 위치

프로젝트 루트 기준 `export/{식별자}/v1/icon-{크기}.png`를 사용합니다. 32px를 기본 크기로 정했으며, 50·100·150·200%는 각각 16·32·48·64px 파일에 대응합니다. 배율별 출력은 16px 원본의 정확한 최근접 정수배이고 확대 후 보정은 없습니다.

편집 파일은 `sprites/representatives-v1/`의 6개와 `sprites/production-v1/`의 60개입니다. 모두 실제 16×16 RGB Aseprite 파일입니다.

## 제작과 검사 근거

내장 image_gen으로 각 아이콘을 따로 생성한 구상 시안·요청문은 source의 두 버전 폴더에 보관했습니다. 생성 결과의 큰 해상도를 도트 원본으로 취급하지 않습니다. Aseprite에서 내용 영역을 16px 격자에 정리하고 제한 팔레트와 이진 알파로 출력했습니다. 필요한 보정도 16px 원본에만 적용했습니다.

`source/production-v1/generation.json`은 새 60종 요청문과 생성 출처입니다. `build-report.json`에는 실제 생성 크기·내용 경계·팔레트가 있습니다. `native-overrides.json`과 `face-refinements.json`은 원본 보정 이유와 도트 배치를 담습니다.

`validation.json`은 66종·264개 PNG의 크기, 최근접 RGBA 일치, 알파 0/255, 가시 RGB 각 채널 10 이상, 단색 방식, 최소 1px 여백, Aseprite 헤더 및 승인 대표 6종의 해시 보존 검사입니다. 기술 검사 통과가 새 60종의 사용자 외형 승인을 뜻하지는 않습니다.

## 번호와 의미

| 비교판 번호 | 식별자 | 계열 | 의미 | 외형 상태 |
|---|---|---|---|---|
| 01 | cmd_edit | 메뉴 | 영지 편집 | 검토 대기 |
| 02 | cmd_monument | 메뉴 | 기념비 | 검토 대기 |
| 03 | cmd_recruit | 메뉴 | 길드원 뽑기 | 검토 대기 |
| 04 | cmd_roster | 메뉴 | 길드원 목록 | 검토 대기 |
| 05 | cmd_ticket | 메뉴 | 티켓 | 검토 대기 |
| 06 | cmd_multi | 메뉴 | 멀티 길드 | 검토 대기 |
| 07 | cmd_settings | 메뉴 | 환경 설정 | 대표 승인 |
| 08 | cmd_trash | 메뉴 | 휴지통 | 검토 대기 |
| 09 | cmd_guide | 메뉴 | 보상 | 검토 대기 |
| 10 | sym_edit | 기호 | 이름 수정 | 검토 대기 |
| 11 | sym_close | 기호 | 닫기·지우기 | 대표 승인 |
| 12 | sym_play | 기호 | 재생·집중 시작 | 검토 대기 |
| 13 | sym_stop | 기호 | 정지 | 검토 대기 |
| 14 | sym_prev | 기호 | 이전 | 검토 대기 |
| 15 | sym_next | 기호 | 다음 | 검토 대기 |
| 16 | sym_up | 기호 | 위로 | 검토 대기 |
| 17 | sym_down | 기호 | 아래로 | 검토 대기 |
| 18 | sym_expand | 기호 | 영역 펼치기 | 검토 대기 |
| 19 | sym_collapse | 기호 | 영역 접기 | 검토 대기 |
| 20 | sym_check | 기호 | 완료 체크 | 검토 대기 |
| 21 | sym_fold_closed | 기호 | 접힌 목록 | 검토 대기 |
| 22 | sym_fold_open | 기호 | 펼친 목록 | 검토 대기 |
| 23 | sym_star | 기호 | 즐겨찾기 | 검토 대기 |
| 24 | icon_book | 분류 | 책·공부 | 대표 승인 |
| 25 | icon_code | 분류 | 코드·개발 | 검토 대기 |
| 26 | icon_run | 분류 | 달리기·운동 | 검토 대기 |
| 27 | icon_art | 분류 | 그림·미술 | 검토 대기 |
| 28 | icon_music | 분류 | 음악 | 검토 대기 |
| 29 | icon_lab | 분류 | 실험 | 검토 대기 |
| 30 | icon_write | 분류 | 글쓰기 | 검토 대기 |
| 31 | icon_folder | 분류 | 정리 | 검토 대기 |
| 32 | icon_meditate | 분류 | 명상 | 검토 대기 |
| 33 | icon_cook | 분류 | 요리 | 검토 대기 |
| 34 | tpl_issue | 티켓 | 이슈 | 검토 대기 |
| 35 | tpl_todo | 티켓 | 할 일 | 검토 대기 |
| 36 | tpl_idea | 티켓 | 아이디어 | 대표 승인 |
| 37 | tpl_retro | 티켓 | 회고 | 검토 대기 |
| 38 | tpl_ticket | 티켓 | 일반 티켓 | 검토 대기 |
| 39 | emote_happy | 감정 | 만족 | 검토 대기 |
| 40 | emote_unhappy | 감정 | 불만 | 검토 대기 |
| 41 | order_restaurant | 주문 | 음식 | 대표 승인 |
| 42 | order_stall | 주문 | 꼬치 | 검토 대기 |
| 43 | order_store | 주문 | 구매 봉투 | 검토 대기 |
| 44 | order_blacksmith | 주문 | 칼 | 검토 대기 |
| 45 | order_carpenter | 주문 | 의자 | 검토 대기 |
| 46 | order_alchemist | 주문 | 물약 | 검토 대기 |
| 47 | order_tailor | 주문 | 옷 | 검토 대기 |
| 48 | order_lumber | 주문 | 목재 | 검토 대기 |
| 49 | order_mine | 주문 | 광석 | 검토 대기 |
| 50 | order_farm | 주문 | 채소 | 검토 대기 |
| 51 | order_ranch | 주문 | 우유 | 검토 대기 |
| 52 | order_fishing | 주문 | 물고기 | 검토 대기 |
| 53 | act_cook | 행동 | 요리 | 대표 승인 |
| 54 | act_pay | 행동 | 계산 | 검토 대기 |
| 55 | act_forge | 행동 | 화로 | 검토 대기 |
| 56 | act_hammer | 행동 | 망치질 | 검토 대기 |
| 57 | act_saw | 행동 | 톱질 | 검토 대기 |
| 58 | act_brew | 행동 | 조제 | 검토 대기 |
| 59 | act_bottle | 행동 | 병입 | 검토 대기 |
| 60 | act_measure | 행동 | 재단 | 검토 대기 |
| 61 | act_sew | 행동 | 바느질 | 검토 대기 |
| 62 | act_chop | 행동 | 벌목 | 검토 대기 |
| 63 | act_mine | 행동 | 채굴 | 검토 대기 |
| 64 | act_water | 행동 | 물 주기 | 검토 대기 |
| 65 | act_feed | 행동 | 먹이 주기 | 검토 대기 |
| 66 | act_fish | 행동 | 낚시 | 검토 대기 |
