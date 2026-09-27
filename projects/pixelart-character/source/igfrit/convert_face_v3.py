# CHANGELOG v1.0 · 2026-09-27 — (추가) 얼굴 수정안을 머리 높이 42px로 변환하고 비교 그림 생성
"""생성한 흉상을 승인 팔레트로 줄여 얼굴 각도를 비교합니다."""
from pathlib import Path
import json
import shutil
from PIL import Image, ImageDraw, ImageFont, ImageColor

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
GENERATED = Path('C:/Users/meeho/.codex/generated_images/01a0e10f-15a2-76f2-bd6d-5b1965357b75/exec-bcfb950c-36a9-46c6-80d4-a05c86e7052e.png')

def main():
    target = HERE / 'igfrit-face-generated-v3.png'
    if not target.exists():
        shutil.copyfile(GENERATED, target)
    raw = Image.open(target).convert('RGBA')
    # 시각 관찰 기준: 왕관을 제외한 정수리 y=220, 턱 y=690.
    scale = 42 / (690 - 220)
    small = raw.resize((round(raw.width * scale), round(raw.height * scale)), Image.Resampling.BOX)
    spec = json.loads((HERE.parents[1] / 'spec/design/pixel-spec-portrait.json').read_text(encoding='utf-8'))
    palette = [ImageColor.getrgb(spec['palette']['outline'])]
    palette += [ImageColor.getrgb(c) for ramp in spec['palette']['ramps'].values() for c in ramp]
    out = Image.new('RGBA', (128, 112))
    ox = (128 - small.width) // 2
    for y in range(small.height):
        for x in range(small.width):
            r, g, b, a = small.getpixel((x, y))
            if a >= 128:
                nearest = min(palette, key=lambda c: sum((v-w)**2 for v, w in zip(c, (r,g,b))))
                out.putpixel((x+ox, y), (*nearest, 255))
    out.save(HERE / 'igfrit-face-study-v3.png')
    out.resize((768, 672), Image.Resampling.NEAREST).save(HERE / 'igfrit-face-preview-v3.png')
    old = Image.open(HERE / 'igfrit-320.png').convert('RGBA').crop((96, 32, 224, 144))
    comparison = Image.new('RGB', (1340, 760), '#EAE7E1')
    draw = ImageDraw.Draw(comparison)
    font = ImageFont.truetype('C:/Windows/Fonts/malgun.ttf', 24)
    smallfont = ImageFont.truetype('C:/Windows/Fonts/malgun.ttf', 18)
    for image, x, title in [(old,20,'기존 얼굴'), (out,680,'수정안 · 양쪽 눈이 보이는 얼굴')]:
        draw.text((x,18),title,font=font,fill='#302A32')
        comparison.paste(image.resize((640,560), Image.Resampling.NEAREST),(x,65),image.resize((640,560),Image.Resampling.NEAREST))
        comparison.paste(image,(x,638),image)
        draw.text((x+145,655),'실제 픽셀 크기 · 위는 5배 확대',font=smallfont,fill='#302A32')
    comparison.save(HERE / 'igfrit-face-comparison-v3.png')
    report = {'canvas':list(out.size),'estimated_head_height':42,'source_head_landmarks':[220,690],
              'colors':len(set(p[:3] for p in out.getdata() if p[3])),
              'alpha':sorted(set(out.getchannel('A').getdata())),
              'status':'얼굴 각도 검토용 흉상입니다. 전신에 아직 합성하지 않았습니다. 기준점은 시각 추정입니다.'}
    (HERE / 'face-report-v3.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False))

if __name__ == '__main__':
    main()
