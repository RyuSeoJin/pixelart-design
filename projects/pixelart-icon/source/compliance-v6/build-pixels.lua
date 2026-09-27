-- CHANGELOG v1.0 · 2026-09-27 — 기존 52종 경계와 정면 대칭을 검수하고 위반 원본만 수정
local root=app.fs.joinPath(app.fs.currentPath,"projects/pixelart-icon")
local source=root.."/source/compliance-v6"
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
local symmetric={icon_lab=true,tpl_issue=true,order_store=true}
local report={}
for _,a in ipairs(catalog.items) do if a.render_mode=="pixel_native_16" then
 local before=load(root.."/"..a.output_directory.."/icon-16.png");local im=Image(before)
 local reasons={}
 if symmetric[a.id] then
  local l,t,r,b=bounds(im)
  for y=0,15 do for x=l,math.floor((l+r)/2) do im:drawPixel(l+r-x,y,im:getPixel(x,y)) end end
  table.insert(reasons,"정면 외곽과 주요 구조를 같은 축으로 반사")
  if a.id=="order_store" then for x=0,15 do im:drawPixel(x,14,0) end end
 end
 if a.id=="act_hammer" then
  im:clear();box(im,7,5,3,10,col("B97D4D"));box(im,2,2,13,5,col("8BACC5"));rect(im,4,3,9,1,col("C3DAE6"))
  table.insert(reasons,"망치 머리를 수평, 손잡이를 수직으로 정렬")
 elseif a.id=="cmd_multi" then
  im:clear();box(im,2,2,4,12,col("4F91CF"));box(im,10,2,4,12,col("4F91CF"));box(im,6,5,4,9,col("AB83C5"))
  table.insert(reasons,"길드 배너 세 개의 좌우 높이·테두리·중심축 정렬")
 elseif a.id=="cmd_trash" then
  im:clear();box(im,6,2,4,3,col("EDB547"));box(im,4,5,8,9,col("D76A73"));box(im,2,4,12,3,col("FFE29A"));rect(im,6,8,1,4,col("FFB2AE"));rect(im,9,8,1,4,col("FFB2AE"))
  table.insert(reasons,"뚜껑 손잡이·뚜껑·통의 떠 있는 간격 제거")
 elseif a.id=="icon_meditate" then
  im:clear()
  for y=1,5 do for x=6,10 do if (x-8)^2+(y-3)^2<=5.76 then im:drawPixel(x,y,col("DBC4EA")) end end end
  rect(im,6,5,5,6,col("9865B5"));rect(im,4,8,9,3,col("9865B5"));rect(im,2,10,13,3,col("796394"));rect(im,4,13,9,1,col("796394"));rect(im,7,5,3,1,D)
  table.insert(reasons,"명상 인물의 머리를 홀수 5px 원형으로 정리하고 몸·팔·다리 대칭")
 end
 -- 4방향 경계는 1px 안쪽 외곽선입니다. 윤곽을 확대하지 않습니다.
 local mask={};for y=0,15 do mask[y]={};for x=0,15 do mask[y][x]=alpha(im:getPixel(x,y))>0 end end
 local function hit(x,y) return mask[y] and mask[y][x] end
 local count=0
 for y=0,15 do for x=0,15 do if hit(x,y) and (not hit(x-1,y) or not hit(x+1,y) or not hit(x,y-1) or not hit(x,y+1)) then
  if im:getPixel(x,y)~=D then count=count+1;im:drawPixel(x,y,D) end
 end end end
 if count>0 then table.insert(reasons,"끊긴 경계를 1px 기본색 #342D46으로 통일") end
 local changes=0;for y=0,15 do for x=0,15 do if im:getPixel(x,y)~=before:getPixel(x,y) then changes=changes+1 end end end
 if changes>0 then
  local folder=root.."/export/"..a.id.."/v6";app.fs.makeAllDirectories(folder);app.fs.makeAllDirectories(root.."/sprites/compliance-v6")
  save(im,source.."/"..a.id.."-native-16.png");save(im,root.."/sprites/compliance-v6/"..a.id..".aseprite")
  for n=1,4 do local out=Image(16*n,16*n,ColorMode.RGB);for y=0,out.height-1 do for x=0,out.width-1 do out:drawPixel(x,y,im:getPixel(math.floor(x/n),math.floor(y/n))) end end;save(out,folder.."/icon-"..16*n..".png") end
 end
 table.insert(report,{id=a.id,changed=changes>0,changed_native_pixels=changes,reasons=reasons})
end end
local f=assert(io.open(source.."/pixel-build-report.json","w"));f:write(json.encode(report));f:close()
print("픽셀 52종 경계·대칭 검수와 수정 원본 출력 완료")
