"""피부 내부와 눈 밖의 청록색 혼입을 영역 기준으로 검사합니다."""
# CHANGELOG v1.1 · 2026-09-29 — 손 외곽선 누락 검사 추가
# CHANGELOG v1.0 · 2026-09-29 — 엄지·손·입가·청록색 재발 검사
import argparse
import hashlib
import json
from pathlib import Path
from PIL import Image


def inspect(path, side, contract):
    im = Image.open(path).convert('RGBA')
    errors = []
    skin = {tuple(c) for c in contract['skin_colors']}
    for region, rows in contract['skin_rows'].items():
        for y, lo, hi in rows:
            for u in range(lo, hi + 1):
                x = u if side == 'left' else 179 - u
                c = im.getpixel((x, y))
                if c[3] != 255 or c[:3] not in skin:
                    errors.append({'region': region, 'xy': [x, y], 'rgba': c})
    for y in range(im.height):
        for x in range(im.width):
            r, g, b, a = im.getpixel((x, y))
            u = x if side == 'left' else 179 - x
            if a and (g-r > 20 or b-r > 65) and not (83 <= u <= 86 and 41 <= y <= 44):
                errors.append({'region': 'eye_color_outside_eye', 'xy': [x, y], 'rgba': [r,g,b,a]})
    edge_path = Path(__file__).resolve().parent/'hand-outline-contract_v001.json'
    if edge_path.exists():
        edge = json.loads(edge_path.read_text(encoding='utf-8'))
        for u, y in edge['points'][side]:
            x = u if side == 'left' else 179-u
            c = im.getpixel((x,y))
            if c[3] != 255 or c[:3] != tuple(edge['rgb']):
                errors.append({'region': 'hand_outline', 'xy': [x,y], 'rgba': c})
    return {'path': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
            'errors': errors, 'pass': not errors}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--version', required=True)
    parser.add_argument('--out')
    args = parser.parse_args()
    work = Path(__file__).resolve().parent
    contract = json.loads((work/'material-region-contract_v001.json').read_text(encoding='utf-8'))
    result = {side: inspect(work.parent/f'image-undecided/180/view/side_{side}_{args.version}.png', side, contract)
              for side in ('left', 'right')}
    if args.out:
        Path(args.out).write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({s: {'pass': r['pass'], 'error_count': len(r['errors'])} for s,r in result.items()}, ensure_ascii=False))
    raise SystemExit(0 if all(r['pass'] for r in result.values()) else 1)
