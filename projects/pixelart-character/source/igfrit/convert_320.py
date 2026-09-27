# CHANGELOG v1.0 · 2026-09-27 — 사용자 승인 후 생성 원본을 기준선에 맞추고 기존 도구로 픽셀 변환
"""이그프리트 생성 원본의 비율을 보정하고 320×320 픽셀 변환본을 만듭니다."""
from pathlib import Path
import sys
import json
from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT / 'core/modules/pixel-art/scripts'))
import pixelize
import spec
import lint

# 원본에서 눈으로 확인한 머리·얼굴 위치와 옷 아래 추정 관절을 구분해 기록합니다.
# 무릎·가랑이는 가려져 있으므로 아래 매핑은 배치 보조이며 해부학 검수 통과의 근거가 아닙니다.
LANDMARKS = [(36, 66), (52, 120), (76, 200), (94, 258), (106, 330),
             (148, 530), (178, 660), (236, 940), (292, 1160), (304, 1212)]

def source_y(y):
    for (dy0, sy0), (dy1, sy1) in zip(LANDMARKS, LANDMARKS[1:]):
        if dy0 <= y <= dy1:
            return sy0 + (y - dy0) * (sy1 - sy0) / (dy1 - dy0)
    return 0 if y < LANDMARKS[0][0] else 1254

def main():
    sp = spec.load(str(ROOT / 'projects/pixelart-character/spec/design/pixel-spec-portrait.json'))
    original = Image.open(HERE / 'igfrit-generated-v2.png').convert('RGBA')
    # 가는 얼굴을 세로로만 늘리지 않도록 머리 영역의 가로 배율도 함께 보정합니다.
    # 목부터 몸통까지 연속적으로 배율을 줄여 띠 경계를 만들지 않습니다.
    aligned = Image.new('RGBA', (1280, 1280))
    for y in range(36, 304):
        blend = max(0.0, min(1.0, (y - 82) / 50))
        scale_x = .285 * (1 - blend) + .195 * blend
        source_center = 610 * (1 - blend) + 660 * blend
        x0 = source_center - 160 / scale_x
        x1 = source_center + 160 / scale_x
        strip = original.transform((1280, 4), Image.Transform.EXTENT,
                                   (x0, source_y(y), x1, source_y(y + 1)),
                                   resample=Image.Resampling.BICUBIC)
        aligned.paste(strip, (0, y * 4))
    # 구성 보정 뒤 공용 변환기의 팔레트 정규화·실루엣 처리·접지를 적용합니다.
    # 재질의 점 노이즈를 정리하되 눈·입의 작은 표현은 정리 전 결과에서 복원합니다.
    detailed = pixelize.pixelize(aligned, sp, height=268, edge='selout', keep_singles=True)
    out = pixelize.pixelize(aligned, sp, height=268, edge='selout', keep_singles=False)
    face_box = (132, 68, 170, 94)
    out.paste(detailed.crop(face_box), face_box[:2])
    out.save(HERE / 'igfrit-320.png')
    out.resize((1280, 1280), Image.Resampling.NEAREST).save(HERE / 'igfrit-preview-4x.png')
    colors, failures, warnings = lint.lint(out, sp)
    report = {
        'size': list(out.size), 'opaque_bbox_exclusive': out.getbbox(),
        'used_colors': colors, 'alpha_values': sorted(set(out.getchannel('A').get_flattened_data())),
        'failures': failures, 'warnings': warnings,
        'landmark_mapping_target_to_source': LANDMARKS,
        'note': '머리 기준점은 시각 관찰값이며 옷 아래 관절은 추정입니다. 불꽃 손 위치는 원본대로 남았습니다.'
    }
    (HERE / 'conversion-report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False))

if __name__ == '__main__':
    main()
