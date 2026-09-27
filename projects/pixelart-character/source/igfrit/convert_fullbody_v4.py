# CHANGELOG v1.0 · 2026-09-27 — (추가) 동작 제작용 전신의 기준선 보정·좌우 버전·비교 그림
"""이그프리트 전신 기본 자세를 320픽셀 좌우 버전으로 변환합니다."""
from pathlib import Path
import json
import shutil
from PIL import Image, ImageOps, ImageDraw, ImageFont
from convert_320 import pixelize, spec, lint, ROOT

HERE = Path(__file__).resolve().parent
SOURCE = Path('C:/Users/meeho/.codex/generated_images/01a0e10f-15a2-76f2-bd6d-5b1965357b75/exec-75e258a0-dbc2-4f53-b9ad-ff46c44d20da.png')
# 원본을 보고 잰 근사 위치입니다. 가랑이는 앞자락에 가려 추정한 값입니다.
LANDMARKS = [(30,23),(52,120),(76,220),(94,302),(106,380),(148,630),
             (178,800),(236,1060),(292,1350),(304,1466)]

def source_y(y):
    for (a,b),(c,d) in zip(LANDMARKS,LANDMARKS[1:]):
        if a <= y <= c:
            return b+(y-a)*(d-b)/(c-a)
    return 1466

def main():
    target=HERE/'igfrit-fullbody-generated-v4.png'
    if not target.exists():
        shutil.copyfile(SOURCE,target)
    raw=Image.open(target).convert('RGBA')
    aligned=Image.new('RGBA',(1280,1280))
    for y in range(30,304):
        blend=max(0,min(1,(y-85)/45))
        sx=.23*(1-blend)+.18*blend
        cx=500*(1-blend)+530*blend
        strip=raw.transform((1280,4),Image.Transform.EXTENT,
                            (cx-160/sx,source_y(y),cx+160/sx,source_y(y+1)),
                            resample=Image.Resampling.BICUBIC)
        aligned.paste(strip,(0,y*4))
    sp=spec.load(str(HERE.parents[1]/'spec/design/pixel-spec-portrait.json'))
    # 불꽃까지 중앙 정렬하면 몸이 밀리므로 변환 후 원래 몸 배치로 복원합니다.
    detailed=pixelize.pixelize(aligned,sp,height=274,edge='selout',keep_singles=True)
    clean=pixelize.pixelize(aligned,sp,height=274,edge='selout',keep_singles=False)
    box=(125,65,182,96)
    clean.paste(detailed.crop(box),box[:2])
    expected=aligned.getchannel('A').point(lambda a:255 if a>=128 else 0).getbbox()
    actual=clean.getbbox()
    dx=round(expected[0]/4)-actual[0]
    left=Image.new('RGBA',(320,320))
    left.paste(clean,(dx,0))
    right=ImageOps.mirror(left)
    for label,im in [('left',left),('right',right)]:
        im.save(HERE/f'igfrit-base-{label}-320-v4.png')
    comparison=Image.new('RGB',(1280,700),'#EAE7E1')
    draw=ImageDraw.Draw(comparison)
    font=ImageFont.truetype('C:/Windows/Fonts/malgun.ttf',24)
    for x,im,title in [(0,left,'왼쪽 방향 · 기본 자세'),(640,right,'오른쪽 방향 · 좌우 반전')]:
        draw.text((x+175,15),title,font=font,fill='#302A32')
        big=im.resize((640,640),Image.Resampling.NEAREST)
        comparison.paste(big,(x,50),big)
    comparison.save(HERE/'igfrit-base-directions-v4.png')
    colors,failures,warnings=lint.lint(left,sp)
    report={'size':list(left.size),'colors':colors,'alpha':sorted(set(left.getchannel('A').get_flattened_data())),
            'bbox':left.getbbox(),'failures':failures,'warnings':warnings,'landmarks':LANDMARKS,
            'right_is_exact_mirror':right.tobytes()==ImageOps.mirror(left).tobytes(),
            'status':'정지 전신 초안입니다. 파츠 미분리, 가려진 관절과 외곽선 추가 검수가 필요합니다.'}
    (HERE/'fullbody-report-v4.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k!='warnings'},ensure_ascii=False))

if __name__=='__main__':
    main()
