-- CHANGELOG v1.0 · 2026-09-27 — 서류·단일 인물·전경 망치·직선 톱니의 16px 원본
local root=app.fs.joinPath(app.fs.currentPath,"projects/pixelart-icon")
local source=app.fs.joinPath(root,"source/ui-consistency-v4")
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
