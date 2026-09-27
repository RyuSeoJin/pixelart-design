# CHANGELOG v1.0 · 2026-09-27 — 160 작업본에서 승인 검토용 320 정지 이미지를 내보냅니다.
"""기존 얼음여왕 작업본을 정수배 확대하고 크기·색상·투명도를 검사합니다."""
from pathlib import Path
import json
from PIL import Image, ImageChops

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent.parent
OUT = PROJECT / 'export/ice-queen'
OUT.mkdir(exist_ok=True, parents=True)
native = Image.open(HERE / 'base-160.png').convert('RGBA')
assert native.size == (160, 160)
working = HERE / 'ice-queen-working-160x160-v1.png'
native.save(working)
still = native.resize((320, 320), Image.Resampling.NEAREST)
target = OUT / 'ice-queen-still-320x320-v1.png'
still.save(target)
actual = Image.open(target).convert('RGBA')
assert actual.size == (320, 320)
assert ImageChops.difference(actual, still).getbbox(alpha_only=False) is None
spec = json.loads((PROJECT / 'spec/design/pixel-spec-field.json').read_text(encoding='utf-8'))
palette = {tuple(bytes.fromhex(c[1:])) for c in [spec['palette']['outline']] +
           [c for ramp in spec['palette']['ramps'].values() for c in ramp]}
visible = [p for p in actual.get_flattened_data() if p[3] > 0]
colors = {p[:3] for p in visible}
assert colors <= palette and len(colors) <= 64
assert all(min(p[:3]) >= 10 for p in visible)
assert set(actual.getchannel('A').get_flattened_data()) == {0, 255}
assert actual.getchannel('A').crop((0, 304, 320, 320)).getbbox() is None
report = {
    'stage': '2단계 — 게임용 정지 디자인', 'status': '사용자 승인 대기',
    'file': target.name, 'actual_size': list(actual.size),
    'working_file': working.name, 'working_size': [160, 160],
    'scale': 2, 'resampling': 'nearest', 'visible_colors': len(colors),
    'visible_rgb_channel_min': min(min(p[:3]) for p in visible),
    'pure_black_visible_pixels': 0, 'alpha_values': [0, 255],
    'palette_check': True, 'grid_check': True,
    'note': '기존 작업본의 외형을 보존한 정지 디자인입니다. 기계 검사는 사용자 외형 승인이나 전체 R01~R30 통과를 대신하지 않습니다.'
}
(OUT / 'ice-queen-still-320x320-v1.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(report, ensure_ascii=False))
