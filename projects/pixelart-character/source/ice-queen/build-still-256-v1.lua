-- CHANGELOG v1.0 · 2026-09-27 — 승인 시안을 128 격자·공통 기준선·팔레트로 정리합니다.
local root='P:/github-repository/pixelart-design/projects/pixelart-character/'
local src=root..'source/ice-queen/'
local out=root..'export/ice-queen/'
local input=Image{fromFile=src..'ice-queen-concept-1024x1024-v1.png'}
local spec=json.decode(io.open(root..'spec/design/pixel-spec-portrait.json'):read('*a'))
local colors={}
local function rgb(h)
 h=h:gsub('#',''); return app.pixelColor.rgba(tonumber(h:sub(1,2),16),tonumber(h:sub(3,4),16),tonumber(h:sub(5,6),16),255)
end
for _,key in ipairs({'SKIN','CLOTH_A','CLOTH_B','METAL','EYE'}) do
 for _,h in ipairs(spec.palette.ramps[key]) do table.insert(colors,rgb(h)) end
end
table.insert(colors,rgb(spec.palette.outline))
local function quant(p)
 local r,g,b=app.pixelColor.rgbaR(p),app.pixelColor.rgbaG(p),app.pixelColor.rgbaB(p)
 local best,dist=colors[1],math.huge
 for _,c in ipairs(colors) do
  local dr,dg,db=r-app.pixelColor.rgbaR(c),g-app.pixelColor.rgbaG(c),b-app.pixelColor.rgbaB(c)
  local d=dr*dr+dg*dg+db*db
  if d<dist then best,dist=c,d end
 end
 return best
end
-- 시안의 관찰 기준선을 새 사양의 정수 작업 격자에 대응합니다.
local ys={{0,-78},{20,95},{30,187},{37,241},{42,286},{59,458},{71,658},{94,815},{117,949},{122,1014},{128,1070}}
local function sy(y)
 for i=1,#ys-1 do
  if y>=ys[i][1] and y<ys[i+1][1] then
   local a,b=ys[i],ys[i+1]; return a[2]+(y-a[1])*(b[2]-a[2])/(b[1]-a[1])
  end
 end
 return -1
end
local native=Image(128,128,ColorMode.RGB)
for y=0,121 do for x=0,127 do
 local sx=500+(x+0.5-64)/0.115
 local yy=sy(y+0.5)
 local votes={}; local best,count=0,0
 for dy=-2,2,2 do for dx=-2,2,2 do
  local xx,iy=math.floor(sx+dx),math.floor(yy+dy)
  local c=0
  if xx>=0 and xx<1024 and iy>=0 and iy<1024 then
   local p=input:getPixel(xx,iy)
   if app.pixelColor.rgbaA(p)>=128 then c=quant(p) end
  end
  votes[c]=(votes[c] or 0)+1
  if votes[c]>count then best,count=c,votes[c] end
 end end
 native:drawPixel(x,y,best)
end end
-- 꼬리·귀·의상까지 가시 실루엣 안쪽 한 도트에 연속 외곽선을 둡니다.
local clean=Image(native)
for y=1,126 do for x=1,126 do
 if app.pixelColor.rgbaA(native:getPixel(x,y))>0 then
  for _,d in ipairs({{1,0},{-1,0},{0,1},{0,-1}}) do
   if app.pixelColor.rgbaA(native:getPixel(x+d[1],y+d[2]))==0 then clean:drawPixel(x,y,rgb(spec.palette.outline)); break end
  end
 end
end end
native=clean
-- 축소에서 빠진 두 홍채와 작은 입을 기본 격자에서 복원합니다.
for _,p in ipairs({{57,30,'7FD0E0'},{57,31,'3E8FB8'},{58,30,'FFF1E4'},
 {62,29,'7FD0E0'},{63,29,'FFFFFF'},{62,30,'3E8FB8'},{63,30,'7FD0E0'},
 {62,31,'7FD0E0'},{63,31,'F6D2BC'},{61,35,'B87574'},{62,35,'B87574'}}) do
 native:drawPixel(p[1],p[2],rgb(p[3]))
end
native:saveAs(src..'ice-queen-working-128x128-v1.png')
local ns=Sprite(128,128,ColorMode.RGB)
ns.layers[1].name='native_128'; ns:newCel(ns.layers[1],1,native,Point(0,0))
ns:saveAs(root..'sprites/ice-queen-working-128-v1.aseprite')
local base=Image(256,256,ColorMode.RGB)
for y=0,255 do for x=0,255 do base:drawPixel(x,y,native:getPixel(x//2,y//2)) end end
base:saveAs(src..'ice-queen-base-256x256-v1.png')
local final=Image(base)
local mask=Image(256,256,ColorMode.RGB)
local overlay=Image(256,256,ColorMode.RGB)
-- 피부와 눈 내부의 편집 픽셀만 승인 범위로 표시합니다. 윤곽·머리·귀는 제외합니다.
local function retouch(x,y,h)
 mask:drawPixel(x,y,rgb('FFFFFF'))
 overlay:drawPixel(x,y,rgb(h))
 final:drawPixel(x,y,rgb(h))
end
for x=122,125 do retouch(x,71,'F6D2BC') end
retouch(122,70,'E2A895'); retouch(123,70,'B87574');retouch(124,70,'B87574');retouch(125,70,'E2A895')
retouch(121,65,'E2A895');retouch(122,65,'FFF1E4')
retouch(114,60,'FFFFFF');retouch(115,61,'7FD0E0');retouch(115,63,'2A4F80')
retouch(124,58,'FFFFFF');retouch(125,59,'7FD0E0');retouch(125,61,'2A4F80')
mask:saveAs(src..'face-mask-256-v1.png');overlay:saveAs(src..'face-retouch-256-v1.png')
local fs=Sprite(256,256,ColorMode.RGB)
fs.layers[1].name='base_2x';fs:newCel(fs.layers[1],1,base,Point(0,0))
local face=fs:newLayer();face.name='face_retouch_1px';fs:newCel(face,1,overlay,Point(0,0))
local scope=fs:newLayer();scope.name='face_mask';fs:newCel(scope,1,mask,Point(0,0));scope.isVisible=false
fs:saveAs(root..'sprites/ice-queen-still-256-v1.aseprite')
final:saveAs(out..'ice-queen-still-256x256-v1.png')
local preview=Image(768,768,ColorMode.RGB)
for y=0,767 do for x=0,767 do preview:drawPixel(x,y,final:getPixel(x//3,y//3)) end end
preview:saveAs(out..'ice-queen-review-768-v1.png')
