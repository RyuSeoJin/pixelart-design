-- CHANGELOG v1.0 · 2026-09-27 — 서류·단일 인물·전경 망치·직선 톱니의 16px 원본
local root=app.fs.joinPath(app.fs.currentPath,"projects/pixelart-icon")
local source=app.fs.joinPath(root,"source/menu-v3")
local rgba=app.pixelColor.rgba
local function hex(h) return rgba(tonumber(h:sub(1,2),16),tonumber(h:sub(3,4),16),tonumber(h:sub(5,6),16),255) end
local D=hex("342D46");local B=hex("4F91CF");local L=hex("8DCDF0")
local G=hex("EDB547");local H=hex("FFE29A");local C=hex("FFF0CD");local S=hex("E6C897")
local function rect(im,x,y,w,h,c) for yy=y,y+h-1 do for xx=x,x+w-1 do im:drawPixel(xx,yy,c) end end end
local function box(im,x,y,w,h,c) rect(im,x,y,w,h,D);rect(im,x+1,y+1,w-2,h-2,c) end
local function maskpoly(points)
 local mask={}
 for y=0,15 do mask[y]={};for x=0,15 do
  local px,py=x+.5,y+.5;local hit=false;local j=#points
  for i=1,#points do local a,b=points[i],points[j]
   if (a[2]>py)~=(b[2]>py) and px<(b[1]-a[1])*(py-a[2])/(b[2]-a[2])+a[1] then hit=not hit end;j=i
  end
  mask[y][x]=hit
 end end
 return mask
end
local function drawmask(im,m,top,bottom)
 for y=1,14 do for x=1,14 do if m[y][x] then
  local border=not m[y-1][x] or not m[y+1][x] or not m[y][x-1] or not m[y][x+1]
  im:drawPixel(x,y,border and D or (y<8 and top or bottom))
 end end end
end
local function polygon(im,p,t,b) drawmask(im,maskpoly(p),t,b or t) end
local images={}
-- 서류는 종이 외곽, 작은 인물, 정보 세 줄을 분리합니다.
local im=Image(16,16,ColorMode.RGB)
box(im,3,1,10,14,C)
box(im,5,3,4,4,S)
rect(im,5,7,5,2,B);rect(im,6,7,3,1,L)
rect(im,5,10,6,1,D);rect(im,5,12,6,1,D);rect(im,8,13,3,1,G)
images.cmd_recruit=im
-- 인물은 한 명이며 머리·어깨를 각진 팔각형과 사다리꼴로 잡습니다.
im=Image(16,16,ColorMode.RGB)
polygon(im,{{6,1},{10,1},{12,3},{12,6},{10,8},{6,8},{4,6},{4,3}},C,S)
polygon(im,{{5,8},{11,8},{14,11},{14,15},{2,15},{2,11}},L,B)
rect(im,7,8,2,2,S)
images.cmd_roster=im
-- 집을 먼저 그리고 망치를 마지막에 그려 겹침이 전경으로 드러납니다.
im=Image(16,16,ColorMode.RGB)
box(im,3,6,9,8,B)
polygon(im,{{1,8},{7,2},{13,8}},H,G)
box(im,5,10,4,4,C)
polygon(im,{{5,13},{7,15},{13,7},{11,5}},H,G)
box(im,7,4,8,5,L);rect(im,8,7,6,1,B)
images.cmd_edit=im
-- 원 위의 방사형 점 대신 직선 톱니를 격자에 배치합니다.
im=Image(16,16,ColorMode.RGB)
local m=maskpoly({{5,3},{11,3},{13,5},{13,11},{11,13},{5,13},{3,11},{3,5}})
local function add(x,y,w,h) for yy=y,y+h-1 do for xx=x,x+w-1 do m[yy][xx]=true end end end
add(6,1,4,4);add(6,11,4,4);add(1,6,4,4);add(11,6,4,4)
add(2,2,3,3);add(11,2,3,3);add(2,11,3,3);add(11,11,3,3)
drawmask(im,m,L,B)
box(im,5,5,6,6,G);rect(im,6,6,4,2,H)
images.cmd_settings=im
local function save(im,path) local s=Sprite(im.width,im.height,ColorMode.RGB);s.cels[1].image=im;s:saveAs(path);s:close() end
local function scale(im,n)
 local out=Image(16*n,16*n,ColorMode.RGB)
 for y=0,out.height-1 do for x=0,out.width-1 do out:drawPixel(x,y,im:getPixel(math.floor(x/n),math.floor(y/n))) end end
 return out
end
app.fs.makeAllDirectories(app.fs.joinPath(root,"sprites/menu-v3"))
for id,img in pairs(images) do
 local folder=app.fs.joinPath(root,"export/"..id.."/v3");app.fs.makeAllDirectories(folder)
 save(img,app.fs.joinPath(source,id.."-native-16.png"))
 save(img,app.fs.joinPath(root,"sprites/menu-v3/"..id..".aseprite"))
 for n=1,4 do save(scale(img,n),app.fs.joinPath(folder,"icon-"..16*n..".png")) end
end
-- 위는 v2, 아래는 v3입니다. 이미지 뷰어 축소와 무관하게 비교하기 위해 6배 표시합니다.
local board=Image(512,280,ColorMode.RGB);board:clear(rgba(224,225,231,255))
local ids={"cmd_recruit","cmd_roster","cmd_edit","cmd_settings"}
local function put(img,x0,y0) for y=0,img.height-1 do for x=0,img.width-1 do local c=img:getPixel(x,y);if app.pixelColor.rgbaA(c)>0 then board:drawPixel(x0+x,y0+y,c) end end end end
for i,id in ipairs(ids) do
 local s=app.open(app.fs.joinPath(root,"export/"..id.."/v2/icon-16.png"));local old=Image(16,16,ColorMode.RGB);old:drawSprite(s,1);s:close()
 put(scale(old,6),(i-1)*128+16,14);put(scale(images[id],6),(i-1)*128+16,150)
end
app.fs.makeAllDirectories(app.fs.joinPath(root,"export/collection-v3"))
save(board,app.fs.joinPath(root,"export/collection-v3/menu-before-after.png"))
print("메뉴 4종 v3 원본·16개 출력·전후 비교판 생성 완료")
