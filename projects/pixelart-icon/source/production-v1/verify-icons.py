# CHANGELOG v1.0 · 2026-09-27 — 전체 66종과 승인 대표 보존을 검사합니다.
"""전체 아이콘의 원본·네 출력·편집 파일·승인 파일 해시를 검사합니다."""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageChops

root = Path(__file__).resolve().parents[2]
source = Path(__file__).resolve().parent
def read(path):
    return json.loads(path.read_text(encoding='utf-8'))
catalog = read(root / 'spec/design/recordtales-icon-catalog.json')
items = catalog['items']
assert len(items) == len({a['id'] for a in items}) == 66
assert sum(a['color_mode'] == 'white_tint' for a in items) == 23
builds = [read(root / f'source/{group}/build-report.json') for group in ('representatives-v1', 'production-v1')]
palettes = {a['id']: {tuple(bytes.fromhex(c)) for c in a['palette']} for build in builds for a in build['assets']}
assert set(palettes) == {a['id'] for a in items}
report = {'revision': '1.0', 'status': 'passed', 'native_count': 66, 'output_count': 264,
          'representative_approval': 'approved', 'remaining_60_art_approval': 'pending',
          'ue_runtime_validation': 'pending', 'assets': []}
for item in items:
    name = item['id']
    group = 'representatives-v1' if item['representative'] else 'production-v1'
    path = root / f'source/{group}/{name}-native-16.png'
    base = Image.open(path).convert('RGBA')
    assert base.size == (16, 16), name
    colors = set(base.get_flattened_data())
    assert {c[3] for c in colors} <= {0, 255}, name
    visible = {c[:3] for c in colors if c[3]}
    assert visible and visible <= palettes[name], name
    assert min(min(c) for c in visible) >= 10, name
    if item['color_mode'] == 'white_tint':
        assert visible == {(255, 255, 255)}, name
    bbox = base.getchannel('A').getbbox()
    assert bbox and bbox[0] >= 1 and bbox[1] >= 1 and bbox[2] <= 15 and bbox[3] <= 15, name
    ase = root / f'sprites/{group}/{name}.aseprite'
    assert ase.is_file() and ase.stat().st_size > 128, name
    # Aseprite 헤더도 실제 16px RGB 편집 파일인지 확인합니다.
    header = ase.read_bytes()[:16]
    assert int.from_bytes(header[4:6], 'little') == 0xA5E0, name
    assert int.from_bytes(header[8:10], 'little') == 16, name
    assert int.from_bytes(header[10:12], 'little') == 16, name
    assert int.from_bytes(header[12:14], 'little') == 32, name
    files = []
    for size in (16, 32, 48, 64):
        output = root / f'export/{name}/v1/icon-{size}.png'
        actual = Image.open(output).convert('RGBA')
        assert actual.size == (size, size), str(output)
        expected = base.resize((size, size), Image.Resampling.NEAREST)
        assert ImageChops.difference(expected, actual).getbbox(alpha_only=False) is None, str(output)
        files.append({'path': output.relative_to(root).as_posix(), 'size': [size, size],
                      'sha256': hashlib.sha256(output.read_bytes()).hexdigest()})
    report['assets'].append({'id': name, 'visible_colors': len(visible), 'native_bbox': bbox,
                            'nearest_rgba_match': True, 'binary_alpha': True, 'files': files})
approval = read(source / 'representative-approval.json')
for asset in approval['assets']:
    for file in asset['files']:
        assert hashlib.sha256((root / file['path']).read_bytes()).hexdigest() == file['sha256'], asset['id']
report['representative_files_unchanged'] = True
def native(name):
    return Image.open(source / f'{name}-native-16.png').convert('RGBA')
for original, target, operation in [
    ('sym_prev', 'sym_next', Image.Transpose.FLIP_LEFT_RIGHT),
    ('sym_prev', 'sym_up', Image.Transpose.ROTATE_270),
    ('sym_prev', 'sym_down', Image.Transpose.ROTATE_90),
    ('sym_fold_closed', 'sym_fold_open', Image.Transpose.ROTATE_270),
]:
    assert ImageChops.difference(native(original).transpose(operation), native(target)).getbbox(alpha_only=False) is None, target
assert native('emote_happy').tobytes() != native('emote_unhappy').tobytes()
report['direction_pairs_match'] = True
(root / 'export/collection-v1/validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print('66종 원본·편집 파일, PNG 264개: 크기·RGBA 최근접 일치·팔레트·알파·여백 검사 통과')
print('승인 대표 6종의 기존 출력 해시 일치. 새 60종 외형 승인과 UE 화면 검수는 별도입니다.')
