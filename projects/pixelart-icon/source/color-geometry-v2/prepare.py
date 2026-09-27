# CHANGELOG v1.0 · 2026-09-27 — 메뉴 색상과 기호 도형 원본 정의
"""메뉴·기호 23종의 색과 도형을 정의하고 기호 SVG를 저장합니다."""
from pathlib import Path
import json, math, hashlib

source=Path(__file__).resolve().parent
root=source.parents[1]
D='342D46'
gold=('EDB547','FFE29A'); blue=('4F91CF','8DCDF0'); green=('95C83E','B9E567')
red=('DF656A','F69591'); purple=('9869BB','C4A0DA'); cream=('E6C897','FFF0CD')
assets=[]
def poly(points,colors,stroke=1.8):
    return {'points':points,'fill':colors[0],'highlight':colors[1],'outline':D,'stroke':stroke}
def rect(x,y,w,h,colors,stroke=1.8):
    return poly([[x,y],[x+w,y],[x+w,y+h],[x,y+h]],colors,stroke)
def ellipse(x,y,rx,ry,colors,stroke=1.8):
    return poly([[round(x+rx*math.cos(i*math.pi/16),4),round(y+ry*math.sin(i*math.pi/16),4)] for i in range(32)],colors,stroke)
def add(name,shapes,mode):
    assets.append({'id':name,'render_mode':mode,'shapes':shapes})
def menu(name,shapes):add(name,shapes,'pixel_native_16')
def symbol(name,points,colors):add(name,[poly(points,colors)],'geometry_per_size')
menu('cmd_edit',[poly([[3,15],[11,7],[19,15]],gold),rect(5,15,12,12,blue),rect(9,20,4,7,cream,1),poly([[17,27],[14,24],[23,13],[26,16]],cream),poly([[20,7],[25,4],[30,10],[25,14]],gold)])
menu('cmd_monument',[poly([[12,5],[16,2],[20,5],[22,25],[10,25]],blue),rect(7,25,18,4,gold),rect(14,11,4,9,gold,1)])
menu('cmd_recruit',[poly([[3,28],[3,21],[7,17],[14,17],[18,21],[18,28]],blue),ellipse(10.5,11,5,6,cream),rect(23,9,4,14,green,1),rect(18,14,14,4,green,1)])
menu('cmd_roster',[poly([[2,28],[2,21],[6,17],[12,17],[16,21],[16,28]],blue),ellipse(9,11,5,6,cream),poly([[17,28],[17,21],[21,17],[26,17],[30,21],[30,28]],purple),ellipse(24,11,5,6,cream)])
menu('cmd_ticket',[poly([[3,8],[29,8],[29,13],[26,15],[26,17],[29,19],[29,24],[3,24],[3,19],[6,17],[6,15],[3,13]],gold),rect(21,10,1,3,cream,0),rect(21,15,1,3,cream,0),rect(21,20,1,2,cream,0)])
menu('cmd_multi',[rect(4,5,2,23,cream,1),rect(6,5,7,9,blue,1),rect(14,10,2,18,cream,1),rect(16,10,7,9,purple,1),rect(24,3,2,25,cream,1),rect(26,3,4,9,green,1)])
gear=[]
for i in range(32):
    a=(i+.5)*math.pi/16;r=13 if i%4 in (0,1) else 10
    gear.append([16+r*math.cos(a),16+r*math.sin(a)])
menu('cmd_settings',[poly(gear,blue),ellipse(16,16,5,5,gold)])
menu('cmd_trash',[poly([[7,9],[25,9],[23,28],[9,28]],red),rect(5,7,22,4,gold),rect(12,3,8,4,gold),rect(12,14,2,10,cream,1),rect(18,14,2,10,cream,1)])
menu('cmd_guide',[ellipse(11,7,5,4,purple),ellipse(21,7,5,4,purple),rect(5,14,22,15,purple),rect(3,10,26,6,gold),rect(14,10,4,19,gold,1)])
symbol('sym_edit',[[5,22],[22,5],[28,11],[11,28],[3,29]],gold)
symbol('sym_close',[[7,3],[16,12],[25,3],[29,7],[20,16],[29,25],[25,29],[16,20],[7,29],[3,25],[12,16],[3,7]],red)
symbol('sym_play',[[9,4],[27,16],[9,28]],green)
symbol('sym_stop',[[7,7],[25,7],[25,25],[7,25]],red)
left=[[21,3],[26,8],[16,16],[26,24],[21,29],[6,16]]
symbol('sym_prev',left,blue)
symbol('sym_next',[[32-x,y] for x,y in left],blue)
symbol('sym_up',[[y,x] for x,y in left],blue)
symbol('sym_down',[[y,32-x] for x,y in left],blue)
symbol('sym_expand',[[13,4],[19,4],[19,13],[28,13],[28,19],[19,19],[19,28],[13,28],[13,19],[4,19],[4,13],[13,13]],green)
symbol('sym_collapse',[[5,13],[27,13],[27,19],[5,19]],gold)
symbol('sym_check',[[3,15],[7,11],[13,17],[25,4],[29,8],[13,26]],green)
closed=[[12,8],[23,16],[12,24]]
symbol('sym_fold_closed',closed,blue)
symbol('sym_fold_open',[[32-y,x] for x,y in closed],blue)
star=[]
for i in range(10):
    a=-math.pi/2+i*math.pi/5;r=13 if i%2==0 else 6
    star.append([16+r*math.cos(a),16+r*math.sin(a)])
symbol('sym_star',star,gold)
# 가장자리를 자르지 않도록 사람 추가 기호를 캔버스 여백 안으로 옮깁니다.
assets[2]['shapes'][-1]=rect(19,14,11,4,green,1)
data={'revision':'1.0','basis':'사용자가 회색 아이콘 색상 추가와 예시처럼 도형 기반 체크·X 개선 요청','reference_policy':'첨부 이미지는 형태 참고만 사용하며 파일을 복제하지 않습니다.','coordinates':[32,32],'alpha':[0,255],'assets':assets}
(source/'design.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for a in assets:
    if a['render_mode']!='geometry_per_size':continue
    s=a['shapes'][0];points=' '.join(f'{x:.4f},{y:.4f}' for x,y in s['points'])
    svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32">
<!-- CHANGELOG v1.0 · 2026-09-27 — 색상과 일정한 획을 가진 기호 도형 원본 -->
<defs><linearGradient id="color" x1="0" y1="0" x2="0" y2="32" gradientUnits="userSpaceOnUse"><stop offset="50%" stop-color="#{s['highlight']}"/><stop offset="50%" stop-color="#{s['fill']}"/></linearGradient></defs>
<polygon points="{points}" fill="url(#color)" stroke="#{D}" stroke-width="{s['stroke']}" stroke-linejoin="round"/>
</svg>
'''
    (source/(a['id']+'.svg')).write_text(svg,encoding='utf-8')
# v1 결과를 다시 쓰지 않았다는 검증 기준을 제작 시작 전에 기록합니다.
baseline=source/'v1-baseline.json'
if not baseline.exists():
    paths=list((root/'export').glob('*/v1/icon-*.png'))
    baseline.write_text(json.dumps({p.relative_to(root).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},indent=2)+'\n',encoding='utf-8')
print('메뉴 9종·기호 14종 설계와 도형 SVG·v1 보존 해시 저장')
