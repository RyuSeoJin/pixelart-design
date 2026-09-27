# CHANGELOG v1.0 · 2026-09-27 — (추가) 사용자 요청에 따른 160·320 해상도 비교
"""확정 사양을 바꾸지 않고 이그프리트의 160·320 픽셀 비교본을 만듭니다."""
from pathlib import Path
import sys
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT / 'core/modules/pixel-art/scripts'))
import spec
import pixelize

def main():
    original = Image.open(HERE / 'igfrit-320.png').convert('RGBA')
    sp = spec.load(str(ROOT / 'projects/pixelart-character/spec/design/pixel-spec-portrait.json'))
    # 비교용 메모리 값입니다. 프로젝트 JSON 사양은 저장하거나 수정하지 않습니다.
    sp.width = sp.height = 160
    sp.center_x = 80
    sp.anchors = {k: v // 2 for k, v in sp.anchors.items()}
    small = pixelize.pixelize(original, sp, height=134, edge='none', keep_singles=True)
    small.save(HERE / 'igfrit-160-study.png')

    board = Image.new('RGB', (1040, 930), '#F2F0EB')
    draw = ImageDraw.Draw(board)
    title = ImageFont.truetype('C:/Windows/Fonts/malgun.ttf', 27)
    font = ImageFont.truetype('C:/Windows/Fonts/malgun.ttf', 19)
    draw.text((36, 24), '320과 160 · 같은 표시 크기로 비교', font=title, fill='#252633')
    draw.text((36, 68), '현재 그림의 축소 실험입니다. 160용으로 새로 그린 결과는 아닙니다.', font=font, fill='#505362')
    draw.text((105, 112), '320×320 원본 · 1배 표시', font=font, fill='#252633')
    draw.text((610, 112), '160×160 변환 · 2배 표시', font=font, fill='#252633')
    board.paste(original, (95, 150), original)
    enlarged = small.resize((320, 320), Image.Resampling.NEAREST)
    board.paste(enlarged, (610, 150), enlarged)
    draw.line((36, 497, 1004, 497), fill='#CDC9C0', width=1)
    draw.text((36, 518), '얼굴 확대 · 양쪽의 화면상 크기를 맞췄습니다', font=font, fill='#252633')
    crop = (122, 46, 186, 104)
    left = original.crop(crop).resize((384, 348), Image.Resampling.NEAREST)
    right = small.crop(tuple(v // 2 for v in crop)).resize((384, 348), Image.Resampling.NEAREST)
    board.paste(left, (62, 565), left)
    board.paste(right, (580, 565), right)
    board.save(HERE / 'igfrit-160-vs-320.png')
    print('320 comparison:', original.size, '160 study:', small.size)

if __name__ == '__main__':
    main()
