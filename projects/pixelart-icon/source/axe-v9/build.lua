-- CHANGELOG v1.1 · 2026-09-28 — 날을 그루터기 윗면에 매입하고 파인 틈 표현
-- CHANGELOG v1.0 · 2026-09-28 — 한쪽 날 도끼와 그루터기
-- CHANGELOG v1.0 · 2026-09-27 — 기존 52종 경계와 정면 대칭을 검수하고 위반 원본만 수정
local root=app.fs.joinPath(app.fs.currentPath,"projects/pixelart-icon")
local source=root.."/source/axe-v9"
local function read(p) local f=assert(io.open(p));local v=json.decode(f:read('*a'));f:close();return v end

local rgba=app.pixelColor.rgba;local alpha=app.pixelColor.rgbaA
local D=rgba(52,45,70,255)
local function col(h) return rgba(tonumber(h:sub(1,2),16),tonumber(h:sub(3,4),16),tonumber(h:sub(5,6),16),255) end
local function rect(im,x,y,w,h,c) for yy=y,y+h-1 do for xx=x,x+w-1 do im:drawPixel(xx,yy,c) end end end
local function box(im,x,y,w,h,c) rect(im,x,y,w,h,D);if w>2 and h>2 then rect(im,x+1,y+1,w-2,h-2,c) end end
local function save(im,p) local s=Sprite(im.width,im.height,ColorMode.RGB);s.cels[1].image=im;s:saveAs(p);s:close() end
local function load(p) local s=assert(app.open(p));local im=Image(16,16,ColorMode.RGB);im:drawSprite(s,1);s:close();return im end
local function bounds(im) local l,t,r,b=16,16,-1,-1;for y=0,15 do for x=0,15 do if alpha(im:getPixel(x,y))>0 then l=math.min(l,x);r=math.max(r,x);t=math.min(t,y);b=math.max(b,y) end end end;return l,t,r,b end


local im=Image(16,16,ColorMode.RGB)
-- 그루터기 윗면을 날 뒤까지 올리고 앞면을 두껍게 유지합니다.
rect(im,4,9,9,6,D);rect(im,3,11,11,4,D)
rect(im,5,10,7,3,col("E5B875"));rect(im,4,11,9,2,col("E5B875"))
rect(im,4,13,9,1,col("966039"));rect(im,6,13,1,1,col("BF8750"));rect(im,10,13,1,1,col("633E35"))
-- 손잡이는 왼쪽 위에서 도끼 머리로 이어지는 45도 축.
for i=0,6 do rect(im,2+i,1+i,3,3,D) end
for i=0,6 do im:drawPixel(3+i,2+i,col("BF8750")) end
-- 짧은 뒷머리와 오른쪽으로만 넓어지는 단일 날.
local rows={{8,10},{7,13},{8,13},{9,13},{9,12},{10,12}}
for i,p in ipairs(rows) do for x=p[1],p[2] do im:drawPixel(x,4+i,col("8B9BB0")) end end
-- 날이 나무 윗면 안으로 들어가고, 앞쪽 나무가 그 아래를 가립니다.
rect(im,10,10,2,2,col("8B9BB0"))
rect(im,9,11,1,1,D);rect(im,10,12,2,1,D)
rect(im,12,10,1,3,col("E5B875"));rect(im,11,12,2,1,col("BF8750"))
local snap=Image(im)
for y=1,14 do for x=1,14 do if alpha(snap:getPixel(x,y))>0 then
 local edge=false;for _,d in ipairs({{-1,0},{1,0},{0,-1},{0,1}}) do if alpha(snap:getPixel(x+d[1],y+d[2]))==0 then edge=true end end
 if edge then im:drawPixel(x,y,D) end
end end end
rect(im,11,7,2,1,col("D0DCE6"));rect(im,11,8,1,1,col("D0DCE6"))
local folder=root.."/export/act_chop/v9";app.fs.makeAllDirectories(folder);app.fs.makeAllDirectories(root.."/sprites/axe-v9")
save(im,source.."/act_chop-native-16.png");save(im,root.."/sprites/axe-v9/act_chop.aseprite")
for n=1,4 do local out=Image(16*n,16*n,ColorMode.RGB);for y=0,out.height-1 do for x=0,out.width-1 do out:drawPixel(x,y,im:getPixel(math.floor(x/n),math.floor(y/n))) end end;save(out,folder.."/icon-"..16*n..".png") end
-- 원본 격자 확인용 확대판. 납품 파일은 위의 네 크기입니다.
local preview=Image(256,256,ColorMode.RGB);preview:clear(col("E0E1E7"))
for y=0,15 do for x=0,15 do local c=im:getPixel(x,y);if alpha(c)>0 then rect(preview,x*16,y*16,16,16,c) end end end
save(preview,folder.."/preview.png")
print("한쪽 날 도끼 v9 네 크기 출력 완료")
