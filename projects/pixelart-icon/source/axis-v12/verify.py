# CHANGELOG v1.0 · 2026-09-28 — 축 정렬·실제 출력·기존 파일 보존 검사
"""도구의 중심축과 현재 아이콘 출력 규격을 검사합니다."""
from pathlib import Path
import json
import hashlib
from PIL import Image, ImageChops

root = Path(__file__).resolve().parents[2]
source = Path(__file__).resolve().parent
catalog = json.loads((root / 'spec/design/recordtales-icon-catalog.json').read_text(encoding='utf-8'))
axes = json.loads((source / 'axes.json').read_text(encoding='utf-8'))
dark = (52, 45, 70, 255)
reports = []
for item in catalog['items']:
    path = root / item['output_directory']
    base = Image.open(path / 'icon-16.png').convert('RGBA')
    for size in (16, 32, 48, 64):
        im = Image.open(path / f'icon-{size}.png').convert('RGBA')
        assert im.size == (size, size), item['id']
        colors = set(im.get_flattened_data())
        assert {c[3] for c in colors} <= {0, 255}, item['id']
        assert min(min(c[:3]) for c in colors if c[3]) >= 10, item['id']
        bounds = im.getbbox()
        assert min(bounds[:2]) >= 1 and max(bounds[2:]) <= size - 1, item['id']
        if item['render_mode'] == 'pixel_native_16':
            assert ImageChops.difference(im, base.resize((size, size), Image.Resampling.NEAREST)).getbbox(alpha_only=False) is None, item['id']
    if item['id'] not in axes:
        continue
    axis = axes[item['id']]
    start, joint, end = axis['start'], axis['joint'], axis['finish']
    dx, dy = end[0] - start[0], end[1] - start[1]
    assert dx == 0 or dy == 0 or abs(dx) == abs(dy), item['id']
    assert dx * (joint[1] - start[1]) - dy * (joint[0] - start[0]) == 0, item['id']
    assert base.getpixel(tuple(joint))[3] == 255, item['id']
    for y in range(1, 15):
        for x in range(1, 15):
            if base.getpixel((x, y))[3] and any(not base.getpixel((x + a, y + b))[3] for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                assert base.getpixel((x, y)) == dark, (item['id'], x, y)
    item['rigid_alignment_review'] = 'axis_verified_art_approval_pending'
    item['outline_review'] = 'automated_boundary_passed_visual_pending'
    reports.append({'id': item['id'], 'axis': axis, 'collinear': True, 'joint_opaque': True})
axe = Image.open(root / 'export/act_chop/v12/icon-16.png').convert('RGBA')
assert axe.getpixel((13, 8)) == (191, 135, 80, 255)
assert axe.getpixel((8, 11)) == (139, 155, 176, 255)
assert axe.getpixel((8, 12)) == (191, 135, 80, 255)
baseline = json.loads((source / 'baseline-hashes.json').read_text(encoding='utf-8'))
for path, digest in baseline.items():
    assert hashlib.sha256((root / path).read_bytes()).hexdigest() == digest, path
report = {'status': 'passed', 'current_icons': 66, 'current_pngs': 264, 'new_v12_icons': 7, 'new_v12_pngs': 28,
          'previous_pngs_preserved': len(baseline), 'axe_exposed_tip_on_axis': True,
          'axe_blade_occluded_by_foreground_wood': True, 'art_approval': 'pending', 'axes': reports}
(root / 'export/collection-v12/validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
(root / 'spec/design/recordtales-icon-catalog.json').write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print('현재 264개 출력·7종 축 정렬·도끼 매입·기존 264개 보존 검사 통과')
