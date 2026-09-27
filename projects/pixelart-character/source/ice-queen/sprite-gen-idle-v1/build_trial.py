# CHANGELOG v1.0 · 2026-09-28 — sprite-gen 호흡과 얼굴 보정 보존 시험
"""sprite-gen의 실제 호흡 출력에 프로젝트 얼굴 보정과 배포 여백을 적용합니다."""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import sys

import numpy as np
from PIL import Image, ImageChops
from sprite_gen.curate.curation import load_curation, stamp_curation
from sprite_gen.effects.breathe import recommended_breathe_frames

SOURCE = Path(__file__).resolve().parent
PROJECT = SOURCE.parents[2]
RUN = SOURCE / 'run'
OUT = PROJECT / 'export/ice-queen/sprite-gen-idle-v1'
PIN = 'b725baa5aad026f183e2083275b441f2db225c48'


def write_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--reuse-run', action='store_true')
    args = parser.parse_args()
    native_path = PROJECT / 'source/ice-queen/ice-queen-working-160x160-v1.png'
    still_path = PROJECT / 'export/ice-queen/ice-queen-still-320x320-v2.png'
    base = Image.open(native_path).convert('RGBA')
    face = Image.open(PROJECT / 'source/ice-queen/face-retouch-320-v2.png').convert('RGBA')
    mask = Image.open(PROJECT / 'source/ice-queen/face-mask-320-v2.png').convert('RGBA')
    still = Image.open(still_path).convert('RGBA')
    assert ImageChops.difference(Image.alpha_composite(base.resize((320, 320), Image.Resampling.NEAREST), face), still).getbbox(alpha_only=False) is None

    logs = []
    def cli(*cmd):
        proc = subprocess.run([sys.executable, '-m', 'sprite_gen.cli', *cmd], capture_output=True, text=True, encoding='utf-8')
        logs.append({'command': list(cmd), 'stdout': proc.stdout, 'stderr': proc.stderr, 'exit_code': proc.returncode})
        if proc.returncode:
            raise RuntimeError(proc.stderr)

    if not args.reuse_run:
        cli('unpack-atlas', '--atlas', str(native_path), '--grid', '1x1', '--states', 'idle', '--out-dir', str(RUN), '--force')
        request_path = RUN / 'sprite-request.json'
        request = json.loads(request_path.read_text(encoding='utf-8'))
        request['states']['idle']['fps'] = 4
        write_json(request_path, request)
        breathe = {'depth': .02, 'depth_x': 0, 'breaths': 1, 'lag': .1}
        n = recommended_breathe_frames(breathe)
        curation = load_curation(RUN) or {'version': 1, 'kind': 'sprite-gen-curation', 'states': {}}
        curation['states']['idle'] = {'selected': list(range(n)), 'order': list(range(n)), 'clones': {str(i): 0 for i in range(1, n)}, 'breathe': breathe}
        write_json(RUN / 'curation.json', stamp_curation(RUN, curation))
        cli('compose-atlas', '--run-dir', str(RUN))

    manifest = json.loads((RUN / 'manifest.json').read_text(encoding='utf-8'))
    atlas = Image.open(RUN / manifest['game_input']).convert('RGBA')
    row = manifest['animation']['rows']['idle']
    rects = manifest['frame_layout']['rows']['idle']
    assert len(rects) == 6
    for name in ('native-160', 'frames-320', 'frames-512', 'face-masks-320'):
        (OUT / name).mkdir(parents=True, exist_ok=True)
    source_hashes = {str(p.relative_to(PROJECT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in (native_path, still_path)}
    frames, reports = [], []
    head_box = (60, 12, 103, 50)
    head = base.crop(head_box)
    for i, rect in enumerate(rects):
        x, y, w, h = (rect[k] for k in ('x', 'y', 'w', 'h'))
        frame = atlas.crop((x, y, x+w, y+h))
        # 얼굴을 새로 그리지 않고 원래 머리와 RGBA가 같은 정수 이동만 허용합니다.
        shifts = [dy for dy in range(-8, 9) if frame.crop((60, 12+dy, 103, 50+dy)).tobytes() == head.tobytes()]
        assert len(shifts) == 1, ('머리 형태 변경', i, shifts)
        dy = shifts[0] * 2
        assert frame.crop((0, 140, 160, 160)).tobytes() == base.crop((0, 140, 160, 160)).tobytes(), ('발 영역 변경', i)
        scaled = frame.resize((320, 320), Image.Resampling.NEAREST)
        overlay = Image.new('RGBA', (320, 320)); overlay.paste(face, (0, dy))
        moved_mask = Image.new('RGBA', (320, 320)); moved_mask.paste(mask, (0, dy))
        final = Image.alpha_composite(scaled, overlay)
        changed = np.any(np.asarray(final) != np.asarray(scaled), axis=2)
        assert not np.any(changed & (np.asarray(moved_mask)[:, :, 3] == 0))
        assert final.crop((120, 24+dy, 206, 100+dy)).tobytes() == still.crop((120, 24, 206, 100)).tobytes()
        colors = set(final.get_flattened_data())
        assert all(c[3] in (0, 255) and (not c[3] or min(c[:3]) >= 10) for c in colors)
        assert len({c[:3] for c in colors if c[3]}) <= 64
        delivery = Image.new('RGBA', (512, 512)); delivery.paste(final, (96, 96))
        assert delivery.crop((96, 96, 416, 416)).tobytes() == final.tobytes()
        frame.save(OUT / f'native-160/{i:02}.png')
        final.save(OUT / f'frames-320/{i:02}.png')
        delivery.save(OUT / f'frames-512/{i:02}.png')
        moved_mask.save(OUT / f'face-masks-320/{i:02}.png')
        frames.append(final)
        reports.append({'index': i, 'head_offset_320': [0, dy], 'face_exact': True, 'outside_face_mask_changed': 0, 'feet_exact': True, 'source_rect_512': [96, 96, 320, 320]})

    # 엔진용 후보는 512칸 4×2 배치로 묶고, 원래 320 그림을 늘리지 않습니다.
    sheet = Image.new('RGBA', (2048, 1024))
    for i, frame in enumerate(frames):
        sheet.paste(frame, ((i % 4)*512+96, (i // 4)*512+96))
    sheet.save(OUT / 'idle-atlas-512-trial.png')
    # 공통 팔레트를 고정해 GIF에서 색이 프레임마다 바뀌지 않게 합니다.
    palette = sorted({p[:3] for f in frames for p in f.get_flattened_data() if p[3]})
    color_index = {c: i+1 for i, c in enumerate(palette)}
    pal = [0, 0, 0] + [v for c in palette for v in c]
    indexed = []
    for frame in frames:
        im = Image.new('P', frame.size); im.putpalette(pal + [0]*(768-len(pal)))
        im.putdata([color_index[p[:3]] if p[3] else 0 for p in frame.get_flattened_data()]); indexed.append(im)
    indexed[0].save(OUT / 'idle-320-trial.gif', save_all=True, append_images=indexed[1:], duration=row['durations_ms'], loop=0, transparency=0, disposal=2, optimize=False)
    # 밝은 배경의 비교판과 재생본은 검토용이며 원본 알파와 별도입니다.
    previews = []
    contact = Image.new('RGB', (960, 640), (75, 84, 103))
    for i, frame in enumerate(frames):
        preview = Image.new('RGB', (320, 320), (75, 84, 103)); preview.paste(frame, (0, 0), frame)
        previews.append(preview); contact.paste(preview, ((i % 3)*320, (i // 3)*320))
    previews[0].save(OUT / 'idle-preview.gif', save_all=True, append_images=previews[1:], duration=row['durations_ms'], loop=0)
    contact.save(OUT / 'contact-sheet.png')
    source_sole = base.getbbox()[3]*2-1
    report = {'tool': 'sprite-gen', 'version': '2.11.0', 'commit': PIN, 'status': 'experimental_visual_review_pending', 'scope': '로컬 idle 호흡 시험; 생성 API 사용 없음', 'source_hashes': source_hashes, 'frames': reports, 'durations_ms': row['durations_ms'], 'upstream_breathe': row['breathe'], 'source_sole_y': source_sole, 'required_sole_y': 303, 'sole_spec_pass': source_sole == 303, 'native_grid_and_face_preservation_pass': True, 'delivery_padding_pass': True, 'blinking': '미제작', 'tail_outline_visual_review': '사용자 검토 대기', 'engine_review': '미실시', 'global_idle_four_frame_spec_changed': False, 'notes': ['6프레임은 실험 설정이며 공통 idle 4프레임 사양을 대체하지 않습니다.', '원본 가져오기 후 fps 변경으로 upstream heal이 raw 부재 경고를 냅니다. 가져온 160 원본 일치와 최종 프레임은 별도 검증합니다.', '기존 원본 발바닥 위치 불일치를 숨기거나 자동 이동하지 않습니다.']}
    write_json(OUT / 'validation.json', report)
    write_json(OUT / 'runtime-trial.json', {'status': 'trial_not_release', 'atlas': 'idle-atlas-512-trial.png', 'frame_size': [512, 512], 'pivot': [256, 400], 'loop': True, 'frames': [{'rect': [(i%4)*512, (i//4)*512, 512, 512], 'duration_ms': row['durations_ms'][i]} for i in range(len(frames))]})
    write_json(SOURCE / 'execution.json', {'tool_commit': PIN, 'python': sys.version, 'commands': logs})
    assert all(hashlib.sha256((PROJECT / name).read_bytes()).hexdigest() == value for name, value in source_hashes.items())
    print(json.dumps({'frames': len(frames), 'face_preserved': True, 'feet_preserved': True, 'source_sole_y': source_sole, 'output': str(OUT)}, ensure_ascii=False))


if __name__ == '__main__':
    main()
