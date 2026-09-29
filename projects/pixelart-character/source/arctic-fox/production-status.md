<!-- CHANGELOG v1.0 · 2026-09-29 — (추가) 현재 입력·출력과 검수 상태 분리 -->
# 북극여우 제작 상태

과거 시안을 현재 입력으로 오인하지 않도록 현재 사용할 자료만 기록합니다. 고유 디자인은 [캐릭터 설정](character.md), 다음 작업은 [프로젝트 할 일](../../pixelart-character-remaining-work.md)을 따릅니다. 경로는 별도 표기가 없으면 이 캐릭터 폴더 기준입니다. 승인 기록의 대상·해시·범위가 승인 근거이며 파일명이나 폴더 위치만으로 승인하지 않습니다.

## 적용 공통 문서

- 제작·검수: 공통 제작 규칙서 v1.38의 production-read-gates, approved-view-review, animation-common-review, walk-production-review
- 설정과 기록의 구분: 공통 설정 템플릿 v1.15
- 수치: 필드·초상화 사양 JSON. 이번 문서 정리에서 크기·관절·팔레트·시간을 바꾸지 않았습니다.

## 현재 승인 원본과 검토본

| 용도 | 현재 파일·목록 | 승인 근거·상태 |
|---|---|---|
| 1024 외형 기준 8종 | image-confirmed/1024/view, 목록·해시는 image-confirmed/approval_v004.json | 승인 완료, 정면은 front_v004, 나머지는 승인 목록 사용 |
| 일러스트·감정 | illustration-selection.json이 가리키는 front·head_front 각 4종 | image-confirmed/approval_v005.json·approval_v006.json 승인 완료 |
| 180 이동용 좌우 입력 | image-confirmed/180/view/side_left_v010.png·side_right_v010.png | image-confirmed/approval_v008.json: v010 좌우 및 포함 색상을 idle 입력으로 사용한 승인 범위. 우향 walk 입력 사용은 후속 사용자 제작 요청과 work/walk-right-review_v002.json 참조 |
| idle 좌우 | image-confirmed/180/anim-idle/left·right의 v007 | image-confirmed/approval_v009.json 승인 완료 |
| walk 좌향 | image-confirmed/180/anim-walk/left의 v007 | image-confirmed/approval_v009.json 승인 완료 |
| walk 우향 | image-undecided/180/anim-walk/right의 v002 | 사용자 승인 대기 |

동작 폴더의 frame·sheet·preview·manifest는 같은 버전을 함께 사용합니다. 승인 폴더의 manifest에 남은 미확정 표기는 제작 당시 기록입니다. 이후 승인 여부는 approval_v009.json·approval_v010.json으로 판단하며 원본 기록은 덮어쓰지 않습니다.

## 색상과 직접 비교 기준

1024에서는 승인 8종을 대조하며, 현재 동작의 직접 도트 기준은 각 방향 v010입니다. material-colors.json은 side_left/right v002에 대한 과거 색상표입니다. 이를 v010에 자동 적용하지 않습니다. v010 포함 색상 사용 근거는 approval_v008.json, 우향 동작의 팔레트 검사는 work/walk-right-review_v002.json에 있습니다. 복원 팔레트 후보 work/restoration-palette-candidate_v001.json도 독립적으로 확정된 공통 팔레트가 아닙니다.

## 검수 상태

| 대상 | 자동·파일 검사 근거 | 화면·실제 재생 | 사용자 승인 | 엔진 검수 |
|---|---|---|---|---|
| 좌우 정지 v010 | work/parts-pair-review_v007.json, 지정 영역 검사 | 실시간 좌우 전환 검수 미완료 | 입력 사용 승인 | 미완료 |
| idle 좌우 v007 | work/contour-review_v001.json, 크기·색·알파·수정 범위·시간 | 전체 반복 재생 검수 미완료 | 완료 | 미완료 |
| walk 좌향 v007 | work/contour-review_v001.json | Aseprite 비교 재생 일부 관찰, 전체 통과 아님 | 완료 | 미완료 |
| walk 우향 v002 | work/walk-right-review_v002.json, 지정 머리·색·알파·시간·합성 일치 | Aseprite 비교 재생 일부 관찰, 전체 통과 아님 | 완료 | 미완료 |

2026-09-29 대화에서 work/walk-both-preview_v001.gif를 Aseprite로 열어 기본 속도와 0.25배속 재생 상태·다른 포즈를 확인했습니다. 간격을 둔 화면 관찰이므로 모든 연속 프레임·마지막→첫 프레임의 순간 변화와 실제 방향 전환은 미검수입니다. 이는 이번 문서 정리 중 새 재생 검사를 실시했다는 뜻이 아닙니다. 관찰된 자세에서는 꼬리·옷단 분리가 보이지 않았지만 전체 주기 통과로 확대하지 않습니다.

자동 검사 통과는 해당 보고서에 명시된 부위·파일·해시에 한정됩니다. 원본 이미지 승인, 실제 보행 품질, 사용자 승인, 엔진 결과를 서로 대신하지 않습니다. resources 등록은 미완료입니다.

## 작업 자료 연결

- 좌향 보행 설계: work/walk-cadence-plan_v004.md, work/walk-production-plan_v004.json. 제작 당시 계획이며 승인 출력은 위 표가 정합니다.
- 우향 재현 절차: work/walk-right-build_v002.lua, 편집본 work/walk-right_v002.aseprite
- 현재 좌우 비교: work/walk-both-preview_v001.gif
- 이전 설정·작업 상태: work/document-history_v001.md. 특정 이력 확인 때만 읽으며 현행 기준으로 사용하지 않습니다.
