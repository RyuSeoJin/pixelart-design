# CHANGELOG v1.0 · 2026-09-29 — 국소 보정 실험의 파일·머리·색상 검사를 기록합니다.
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
for i, path in enumerate(sorted((work / 'walk-corrected-left').glob('frame-*_v001.png'))):
    a = np.array(Image.open(path).convert('RGBA'))
    mask = a[:, :, 3] > 0
    y, x = np.where(mask)
    dy = shifts[i]
    imported = work / f'walk-corrected-left-run/frames/walk/frame-{i}.png'
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
gif = work / 'walk-corrected-left-run/qa/walk.gif'
im = Image.open(gif)
durations = []
for i in range(im.n_frames):
    im.seek(i)
    durations.append(im.info.get('duration'))
report = {
    'version': 1, 'source': source.relative_to(root).as_posix(),
    'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
    'status': '부분 기술 검사 완료·보행 미통과',
    'frames': records,
    'gif': {'file': gif.relative_to(root).as_posix(), 'sha256': hashlib.sha256(gif.read_bytes()).hexdigest(),
            'frame_count': im.n_frames, 'durations_ms': durations, 'loop': im.info.get('loop')},
    'limits': ['최하단 불투명 픽셀은 발의 접촉점 판정이 아닙니다.',
               '원본 팔레트에 포함되어도 재질 위치가 올바르다는 뜻은 아닙니다.',
               '머리 검사는 지정 영역과 알려진 정수 이동량에 한정됩니다.',
               'GIF 파일 검사는 실제 반복 재생 관찰을 대신하지 않습니다.'],
}
(work / 'walk-measure_v001.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print(json.dumps({'frames': len(records), 'durations_ms': durations, 'report': 'work/walk-measure_v001.json'}, ensure_ascii=False))
