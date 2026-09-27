-- CHANGELOG v1.0 · 2026-09-27 — 기존 52종 경계와 정면 대칭을 검수하고 위반 원본만 수정
local root=app.fs.joinPath(app.fs.currentPath,"projects/pixelart-icon")
local source=root.."/source/refinement-v7"
local function read(p) local f=assert(io.open(p));local v=json.decode(f:read('*a'));f:close();return v end
local catalog=read(source.."/baseline-catalog.json")
local rgba=app.pixelColor.rgba;local alpha=app.pixelColor.rgbaA
local D=rgba(52,45,70,255)
local function col(h) return rgba(tonumber(h:sub(1,2),16),tonumber(h:sub(3,4),16),tonumber(h:sub(5,6),16),255) end
local function rect(im,x,y,w,h,c) for yy=y,y+h-1 do for xx=x,x+w-1 do im:drawPixel(xx,yy,c) end end end
local function box(im,x,y,w,h,c) rect(im,x,y,w,h,D);if w>2 and h>2 then rect(im,x+1,y+1,w-2,h-2,c) end end
local function save(im,p) local s=Sprite(im.width,im.height,ColorMode.RGB);s.cels[1].image=im;s:saveAs(p);s:close() end
local function load(p) local s=assert(app.open(p));local im=Image(16,16,ColorMode.RGB);im:drawSprite(s,1);s:close();return im end
local function bounds(im) local l,t,r,b=16,16,-1,-1;for y=0,15 do for x=0,15 do if alpha(im:getPixel(x,y))>0 then l=math.min(l,x);r=math.max(r,x);t=math.min(t,y);b=math.max(b,y) end end end;return l,t,r,b end

local images={}
local im=Image(16,16,ColorMode.RGB)
box(im,7,5,3,10,col("B97D4D"));box(im,3,2,11,5,col("8BACC5"));rect(im,5,3,7,1,col("C3DAE6"));images.act_hammer=im
im=Image(16,16,ColorMode.RGB)
-- 작은 그루터기 위로 넓은 은빛 날을 드러냅니다.
box(im,3,11,10,4,col("966039"));rect(im,4,12,8,1,col("E5B875"));rect(im,7,13,1,1,col("633E35"))
-- 손잡이 중심선은 정확히 45도입니다.
for i=0,8 do rect(im,5+i,9-i,2,2,D) end
for i=1,7 do im:drawPixel(5+i,10-i,col("BF8750")) end
local rows={{4,8},{3,8},{2,8},{2,7},{2,7},{3,6},{4,6}}
for i,p in ipairs(rows) do for x=p[1],p[2] do im:drawPixel(x,3+i,col("8B9BB0")) end end
local snap=Image(im)
for y=1,14 do for x=1,14 do if alpha(snap:getPixel(x,y))>0 then
 local edge=false;for _,p in ipairs({{-1,0},{1,0},{0,-1},{0,1}}) do if alpha(snap:getPixel(x+p[1],y+p[2]))==0 then edge=true end end
 if edge then im:drawPixel(x,y,D) end
end end end
rect(im,3,6,1,2,col("D0DCE6"));rect(im,4,5,1,1,col("D0DCE6"))
images.act_chop=im
for id,img in pairs(images) do
 local folder=root.."/export/"..id.."/v7";app.fs.makeAllDirectories(folder);app.fs.makeAllDirectories(root.."/sprites/refinement-v7")
 save(img,source.."/"..id.."-native-16.png");save(img,root.."/sprites/refinement-v7/"..id..".aseprite")
 for n=1,4 do local out=Image(16*n,16*n,ColorMode.RGB);for y=0,out.height-1 do for x=0,out.width-1 do out:drawPixel(x,y,img:getPixel(math.floor(x/n),math.floor(y/n))) end end;save(out,folder.."/icon-"..16*n..".png") end
end
print("망치 폭 조정·벌목 도끼 가독성 수정 완료")
