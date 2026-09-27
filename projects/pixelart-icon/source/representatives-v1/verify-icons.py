# CHANGELOG v1.0 · 2026-09-27 — 대표 6종의 크기·알파·색·여백·최근접 출력 일치를 검사합니다.
"""대표 아이콘 원본과 네 배율 출력의 기술 규격을 검사합니다."""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageChops

project = Path(__file__).resolve().parents[2]
source = Path(__file__).resolve().parent
catalog = json.loads((project / 'spec/design/recordtales-icon-catalog.json').read_text(encoding='utf-8'))
build = json.loads((source / 'build-report.json').read_text(encoding='utf-8'))
palettes = {a['id']: {tuple(bytes.fromhex(c)) for c in a['palette']} for a in build['assets']}
items = {a['id']: a for a in catalog['items']}
assert len(items) == 66
assert sum(a['color_mode'] == 'white_tint' for a in items.values()) == 23
assert len(catalog['representative_order']) == 6
report = {'revision': '1.0', 'status': 'passed', 'art_approval': 'pending',
          'ue_runtime_validation': 'pending', 'assets': []}
for name in catalog['representative_order']:
    path = source / f'{name}-native-16.png'
    base = Image.open(path).convert('RGBA')
    assert base.size == (16, 16), name
    colors = set(base.get_flattened_data())
    assert {c[3] for c in colors} <= {0, 255}, name
    visible = {c[:3] for c in colors if c[3]}
    assert visible and visible <= palettes[name], name
    assert min(min(c) for c in visible) >= 10, name
    if items[name]['color_mode'] == 'white_tint':
        assert visible == {(255, 255, 255)}, name
    bbox = base.getchannel('A').getbbox()
    assert bbox and bbox[0] >= 1 and bbox[1] >= 1 and bbox[2] <= 15 and bbox[3] <= 15, name
    assert (project / f'sprites/representatives-v1/{name}.aseprite').is_file(), name
    files = []
    for size in (16, 32, 48, 64):
        output = project / f'export/{name}/v1/icon-{size}.png'
        actual = Image.open(output).convert('RGBA')
        assert actual.size == (size, size), str(output)
        expected = base.resize((size, size), Image.Resampling.NEAREST)
        assert ImageChops.difference(expected, actual).getbbox(alpha_only=False) is None, str(output)
        files.append({'path': output.relative_to(project).as_posix(), 'size': [size, size],
                      'sha256': hashlib.sha256(output.read_bytes()).hexdigest()})
    report['assets'].append({'id': name, 'visible_colors': len(visible), 'native_bbox': bbox,
                            'nearest_rgba_match': True, 'binary_alpha': True, 'files': files})
output = project / 'export/representatives-v1/validation.json'
output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print('대표 6종·24개 PNG: 크기·최근접 RGBA 일치·색상 하한·단색·알파·여백 검사 통과')
print('외형 사용자 승인과 UE 화면 검수는 별도 대기입니다.')
