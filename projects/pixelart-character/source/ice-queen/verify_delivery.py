# CHANGELOG v1.0 · 2026-09-27 — 프레임 검증과 배포 묶음 생성
from pathlib import Path
import json, zipfile
from PIL import Image, ImageChops
root=Path(__file__).resolve().parents[2]
out=root/'export/ice-queen'
allowed={tuple(bytes.fromhex(c[1:])) for c in [json.loads((root/'spec/design/pixel-spec-field.json').read_text(encoding='utf-8'))['palette']['outline']]+[c for ramp in json.loads((root/'spec/design/pixel-spec-field.json').read_text(encoding='utf-8'))['palette']['ramps'].values() for c in ramp]}
checks=[]
for tag,n,duration in [('idle',4,920),('walk',8,800)]:
 g=Image.open(out/f'{tag}-preview.gif')
 total=0
 for f in range(g.n_frames):
  g.seek(f);total+=g.info['duration']
 assert g.n_frames==n and total==duration
 for f in range(n):
  p=out/f'{tag}-{f:02d}-320.png'
  im=Image.open(p).convert('RGBA')
  base=Image.open(out/f'{tag}-{f:02d}-160.png').convert('RGBA')
  assert ImageChops.difference(im,base.resize((320,320),Image.Resampling.NEAREST)).getbbox(alpha_only=False) is None
  visible=[v for v in im.get_flattened_data() if v[3]>0]
  assert all(min(v[:3])>=10 and v[:3] in allowed for v in visible)
  assert im.getchannel('A').crop((0,304,320,320)).getbbox(alpha_only=False) is None
  checks.append({'frame':p.name,'visible_colors':len({v[:3] for v in visible}),'min_rgb_channel':min(min(v[:3]) for v in visible),'grid_2x2':True,'below_ground_pixels':0})
report={'검사':'12프레임의 팔레트·검정 제한·2배 격자·지면 아래 픽셀·GIF 타이밍 통과','frames':checks,'전체_일러스트_규칙_통과':False}
(out/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
prompt={'도구':'내장 image_gen','요청':'기존 얼음여왕 외형과 픽셀 밀도·꼬리 외곽선을 보존하며 배경과 바닥 그림자·떠 있는 마법 효과를 실제 알파로 제거합니다. 흰 옷·머리·꼬리는 보존하고 가시 RGB 각 채널은 10 이상입니다.','후처리':'160 작업 격자 배치·알파 정리·승인 팔레트 매핑·공통 보행 위상에 파츠 조립·최근접 2배 출력','상태':'동작 검토용 초안'}
(root/'source/ice-queen/generation.json').write_text(json.dumps(prompt,ensure_ascii=False,indent=2),encoding='utf-8')
with zipfile.ZipFile(out/'ice-queen-animations-v1.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in out.iterdir():
  if p.suffix in ('.png','.gif','.json'): z.write(p,p.name)
 z.write(root/'sprites/ice-queen-v1.aseprite','ice-queen-v1.aseprite')
print('완료: 12프레임 검증, 배포 묶음')
