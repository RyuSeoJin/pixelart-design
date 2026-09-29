# CHANGELOG v1.0 · 2026-09-29 — 다리 연결 수정본의 실제 출력과 지정 검사 범위를 기록합니다.
from pathlib import Path
import hashlib
import json
import numpy as np
from PIL import Image

root = Path(__file__).resolve().parent.parent
work = root / 'work'
source = root / 'image-confirmed/180/view/side_left_v010.png'
src = np.array(Image.open(source).convert('RGBA'))
palette = set(map(tuple, src[src[:, :, 3] > 0, :3]))
shifts = [0, 1, 0, -1, 0, 1, 0, -1]
records = []
for i, path in enumerate(sorted((work / 'walk-corrected-left').glob('frame-*_v002.png'))):
    a = np.array(Image.open(path).convert('RGBA'))
    mask = a[:, :, 3] > 0
    y, x = np.where(mask)
    dy = shifts[i]
    imported = work / f'walk-continuity-run/frames/walk/frame-{i}.png'
    records.append({
        'frame': i, 'file': path.relative_to(root).as_posix(),
        'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
        'canvas': list(Image.open(path).size),
        'bbox_xyxy': [int(x.min()), int(y.min()), int(x.max()+1), int(y.max()+1)],
        'alpha_values': np.unique(a[:, :, 3]).tolist(),
        'new_colors': len(set(map(tuple, a[mask, :3])) - palette),
        'minimum_visible_channel': int(a[mask, :3].min()),
        'head_roi_source_xyxy': [65, 15, 115, 65], 'head_translation_xy': [0, dy],
        'head_changed_pixels': int(np.any(src[15:65, 65:115] != a[15+dy:65+dy, 65:115], axis=2).sum()),
        'bottommost_visible_row': int(y.max()),
        'row_170_opaque_x': np.where(mask[170])[0].tolist(),
        'spritegen_import_pixels_equal': bool(np.array_equal(a, np.array(Image.open(imported).convert('RGBA')))),
        'foot_identity_and_contact': '미판정',
    })
    seen = set()
    components = []
    for yy, xx in zip(*np.where(mask)):
        if (xx, yy) in seen:
            continue
        queue = [(xx, yy)]
        seen.add((xx, yy))
        count = 0
        while queue:
            px, py = queue.pop()
            count += 1
            for dx in (-1, 0, 1):
                for dy2 in (-1, 0, 1):
                    nx, ny = px+dx, py+dy2
                    if 0 <= nx < 180 and 0 <= ny < 180 and mask[ny, nx] and (nx, ny) not in seen:
                        seen.add((nx, ny))
                        queue.append((nx, ny))
        components.append(count)
    records[-1]['opaque_component_sizes_8_connected'] = sorted(components, reverse=True)
gif = work / 'walk-continuity-run/qa/walk.gif'
im = Image.open(gif)
durations = []
for i in range(im.n_frames):
    im.seek(i)
    durations.append(im.info.get('duration'))
report = {
    'version': 1, 'source': source.relative_to(root).as_posix(),
    'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
    'status': '다리 연결 보정·부분 기술 검사 완료·실제 재생 미검수',
    'frames': records,
    'planned_motion': {
        'near_boot_anchor_x': [81,86,91,96,101,98,90,82],
        'near_boot_base_row': [170,170,170,170,170,164,161,165],
        'far_phase_offset_frames': 4,
        'far_x_offset': 2,
        'coordinate_kind': '보정 스크립트 설계값·실제 접촉점 실측과 구분',
    },
    'gif': {'file': gif.relative_to(root).as_posix(), 'sha256': hashlib.sha256(gif.read_bytes()).hexdigest(),
            'frame_count': im.n_frames, 'durations_ms': durations, 'loop': im.info.get('loop')},
    'limits': ['최하단 불투명 픽셀은 발의 접촉점 판정이 아닙니다.',
               '원본 팔레트에 포함되어도 재질 위치가 올바르다는 뜻은 아닙니다.',
               '머리 검사는 지정 영역과 알려진 정수 이동량에 한정됩니다.',
               'GIF 파일 검사는 실제 반복 재생 관찰을 대신하지 않습니다.',
               '연결 성분 검사는 관절 구조·보행의 자연스러움을 판정하지 않습니다.'],
}
(work / 'walk-measure_v002.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print(json.dumps({'frames': len(records), 'durations_ms': durations, 'report': 'work/walk-measure_v002.json'}, ensure_ascii=False))
