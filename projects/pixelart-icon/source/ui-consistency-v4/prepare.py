# CHANGELOG v1.0 · 2026-09-27 — 홀수 얼굴·일자 망치·직각 방향 기호 정의
"""대칭 기준을 적용한 아이콘 원본과 재생성 스크립트를 준비합니다."""
from pathlib import Path
import json,hashlib
src=Path(__file__).resolve().parent;root=src.parents[1]
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
cat=json.loads((root/'spec/design/recordtales-icon-catalog.json').read_text(encoding='utf-8'))
if not (src/'previous-catalog.json').exists():
    write(src/'previous-catalog.json',cat)
    write(src/'previous-hashes.json',{f'{a["output_directory"]}/icon-{n}.png':hashlib.sha256((root/a['output_directory']/f'icon-{n}.png').read_bytes()).hexdigest() for a in cat['items'] for n in [16,32,48,64]})
old=json.loads((root/'source/color-geometry-v2/design.json').read_text(encoding='utf-8'))
left=[[21,3],[26,8],[18,16],[26,24],[21,29],[8,16]]
shapes={'sym_prev':left,'sym_next':[[32-x,y] for x,y in left],'sym_up':[[y,x] for x,y in left],'sym_down':[[y,32-x] for x,y in left],'sym_play':[[10,4],[22,16],[10,28]],'sym_fold_closed':[[12,8],[20,16],[12,24]],'sym_fold_open':[[24,12],[16,20],[8,12]]}
assets=[]
for a in old['assets']:
    if a['id'] not in shapes:continue
    a['shapes'][0]['points']=shapes[a['id']];assets.append(a)
    s=a['shapes'][0];points=' '.join(f'{x},{y}' for x,y in s['points'])
    (src/(a['id']+'.svg')).write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32">\n<!-- CHANGELOG v1.0 · 2026-09-27 — 45도 사선·90도 꼭짓점 -->\n<defs><linearGradient id="c" x1="0" y1="0" x2="0" y2="32" gradientUnits="userSpaceOnUse"><stop offset="50%" stop-color="#{s["highlight"]}"/><stop offset="50%" stop-color="#{s["fill"]}"/></linearGradient></defs>\n<polygon points="{points}" fill="url(#c)" stroke="#{s["outline"]}" stroke-width="{s["stroke"]}" stroke-linejoin="round"/>\n</svg>\n',encoding='utf-8')
write(src/'design.json',{'revision':'1.0','assets':assets,'angle_rule':'사선 절댓값 dx=dy, 화살촉과 꺾쇠 꼭짓점 90도'})
lua=(root/'source/color-geometry-v2/build.lua').read_text(encoding='utf-8').replace('color-geometry-v2','ui-consistency-v4').replace('/v2','/v4').replace('메뉴 9종·기호 14종 v2: PNG 92개 생성 완료','방향 기호 7종 v4: PNG 28개 생성 완료')
(src/'build-geometry.lua').write_text(lua,encoding='utf-8')
oldlua=(root/'source/menu-v3/build.lua').read_text(encoding='utf-8')
prefix=oldlua[:oldlua.index('local images={}')].replace('menu-v3','ui-consistency-v4')
body='''local images={}
local faces={}
local function circle(cx,cy,n)
 local m={};local r=n/2-.1
 for y=0,15 do m[y]={};for x=0,15 do m[y][x]=(x-cx)^2+(y-cy)^2<=r*r end end
 return m
end
local function face(im,id,cx,cy,n,t,b)
 local m=circle(cx,cy,n);drawmask(im,m,t,b)
 local mask=Image(16,16,ColorMode.RGB)
 for y=0,15 do for x=0,15 do if m[y][x] then mask:drawPixel(x,y,rgba(255,255,255,255)) end end end
 faces[id]=mask
end
local im=Image(16,16,ColorMode.RGB)
box(im,2,1,11,14,C)
face(im,"cmd_recruit",7,5,5,C,S)
rect(im,4,8,7,2,B);rect(im,5,8,5,1,L)
rect(im,4,11,7,1,D);rect(im,6,13,3,1,G)
images.cmd_recruit=im
im=Image(16,16,ColorMode.RGB)
local m={};for y=0,15 do m[y]={};for x=0,15 do m[y][x]=false end end
local widths={7,9,11,13,13,13}
for i,w in ipairs(widths) do for x=8-(w-1)/2,8+(w-1)/2 do m[8+i][x]=true end end
drawmask(im,m,L,B);rect(im,7,8,3,2,S)
face(im,"cmd_roster",8,4,7,C,S)
images.cmd_roster=im
im=Image(16,16,ColorMode.RGB)
box(im,3,6,9,8,B);polygon(im,{{1,8},{7,2},{13,8}},H,G);box(im,5,10,3,4,C)
-- 집 위 전경에 수직 손잡이와 수평 머리를 놓습니다.
box(im,10,6,3,9,G);box(im,8,4,7,4,L)
images.cmd_edit=im
for _,id in ipairs({"emote_happy","emote_unhappy"}) do
 im=Image(16,16,ColorMode.RGB);face(im,id,8,8,13,H,G)
 rect(im,5,6,1,2,D);rect(im,11,6,1,2,D)
 local mid=id=="emote_happy" and 11 or 10;local side=id=="emote_happy" and 10 or 11
 rect(im,6,mid,5,1,D);rect(im,5,side,1,1,D);rect(im,11,side,1,1,D)
 images[id]=im
end
local function save(im,path) local s=Sprite(im.width,im.height,ColorMode.RGB);s.cels[1].image=im;s:saveAs(path);s:close() end
local function scale(im,n)
 local out=Image(16*n,16*n,ColorMode.RGB)
 for y=0,out.height-1 do for x=0,out.width-1 do out:drawPixel(x,y,im:getPixel(math.floor(x/n),math.floor(y/n))) end end
 return out
end
app.fs.makeAllDirectories(app.fs.joinPath(root,"sprites/ui-consistency-v4"))
for id,img in pairs(images) do
 local folder=app.fs.joinPath(root,"export/"..id.."/v4");app.fs.makeAllDirectories(folder)
 save(img,app.fs.joinPath(source,id.."-native-16.png"));save(img,app.fs.joinPath(root,"sprites/ui-consistency-v4/"..id..".aseprite"))
 if faces[id] then save(faces[id],app.fs.joinPath(source,id.."-face-mask.png")) end
 for n=1,4 do save(scale(img,n),app.fs.joinPath(folder,"icon-"..16*n..".png")) end
end
print("홀수 얼굴 4종·일자 망치 v4: PNG 20개 생성 완료")
'''
(src/'build-pixels.lua').write_text(prefix+body,encoding='utf-8')
write(src/'constraints.json',{'revision':'1.0','faces':{'cmd_recruit':{'center':[7,5],'diameter':5},'cmd_roster':{'center':[8,4],'diameter':7},'emote_happy':{'center':[8,8],'diameter':13},'emote_unhappy':{'center':[8,8],'diameter':13}},'reflection_axes':{'cmd_recruit':7,'cmd_roster':8,'emote_happy':8,'emote_unhappy':8},'hammer':{'head':[8,4,7,4],'handle':[10,6,3,9]},'geometry_ids':list(shapes),'basis':'사용자 지정 홀수 얼굴·좌우 대칭 우선·일자 망치·직각 화살표'})
print('v4 원본 정의·도형 SVG·이전 파일 보존 해시 준비 완료')
