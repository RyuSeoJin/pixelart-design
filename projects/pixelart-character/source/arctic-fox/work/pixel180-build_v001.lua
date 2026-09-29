-- CHANGELOG v1.0 · 2026-09-28 — 생성 원형을 180 격자·공통 팔레트로 정리합니다.
local root = 'P:/github-repository/pixelart-design/projects/pixelart-character/'
local work = root .. 'source/arctic-fox/work/'
local output = root .. 'source/arctic-fox/image-undecided/180/view/'
local native = root .. 'sprites/arctic-fox/'
app.fs.makeAllDirectories(output)
app.fs.makeAllDirectories(native)
local pc = app.pixelColor
local colors = {'221A26','FFF1E4','F6D2BC','E2A895','B87574','7A4A58',
 'FAF6F0','E3DCD8','BCB0BC','8A7D97','5A506E',
 'F4F7FA','C3CCD8','8C97AD','5B637F','383C55',
 '7FD0E0','3E8FB8','2A4F80'}
local palette = {}
for _,h in ipairs(colors) do
 palette[#palette+1] = {tonumber(h:sub(1,2),16),tonumber(h:sub(3,4),16),tonumber(h:sub(5,6),16)}
end
local function valid(c)
 local r,g,b,a=pc.rgbaR(c),pc.rgbaG(c),pc.rgbaB(c),pc.rgbaA(c)
 return a>=200 and not (b>150 and b>r*1.6 and g<100) and not (r>150 and b>150 and g<100)
end
local function quantize(c)
 local r,g,b=pc.rgbaR(c),pc.rgbaG(c),pc.rgbaB(c)
 local best,dist=nil,1e30
 for _,p in ipairs(palette) do
  local d=(r-p[1])^2+(g-p[2])^2+(b-p[3])^2
  if d<dist then best,dist=p,d end
 end
 return pc.rgba(best[1],best[2],best[3],255)
end
local results={}
for _,side in ipairs({'left','right'}) do
 local src=app.open(work..'pixel180-'..side..'-generated_v001.png')
 local raw=Image(src.spec)
 raw:drawSprite(src,1)
 local minY,maxY,footMin,footMax=raw.height,0,raw.width,0
 for y=0,raw.height-1 do for x=0,raw.width-1 do
  if valid(raw:getPixel(x,y)) then minY=math.min(minY,y);maxY=math.max(maxY,y) end
 end end
 -- 마지막 발 영역으로 중심을 잡아 꼬리가 중심 계산에 들어오지 않게 합니다.
 for y=maxY-70,maxY do for x=0,raw.width-1 do
  if valid(raw:getPixel(x,y)) then footMin=math.min(footMin,x);footMax=math.max(footMax,x) end
 end end
 local scale=160/(maxY-minY+1)
 local center=(footMin+footMax)/2
 local s=Sprite(180,180,ColorMode.RGB)
 s.layers[1].name='body-native-180'
 local dst=s.cels[1].image
 -- 얼굴과 몸에 같은 최근접 표본 격자를 적용합니다. 별도 얼굴 확대는 없습니다.
 for y=11,170 do for x=0,179 do
  local sx=math.floor(center+(x-90)/scale+0.5)
  local sy=math.min(maxY,math.floor(minY+(y-11+0.5)/scale))
  if sx>=0 and sx<raw.width then
   local c=raw:getPixel(sx,sy)
   if valid(c) then dst:drawPixel(x,y,quantize(c)) end
  end
 end end
 local pal=Palette(#palette+1)
 pal:setColor(0,Color{r=0,g=0,b=0,a=0})
 for i,p in ipairs(palette) do pal:setColor(i,Color{r=p[1],g=p[2],b=p[3],a=255}) end
 s:setPalette(pal)
 local name='three-quarter_'..side..'_v001'
 s:saveAs(native..name..'.aseprite')
 app.command.SaveFileAs{ui=false,filename=output..name..'.png'}
 print(side..' scale='..scale..' source_center='..center..' source_y='..minY..','..maxY)
 results[#results+1]=Image(dst)
 s:close();src:close()
end
-- 검토용 확대본만 정수 4배로 만듭니다. 실제 파일은 180 정사각형입니다.
local preview=Sprite(1480,760,ColorMode.RGB)
local im=preview.cels[1].image
for y=0,759 do for x=0,1479 do
 local v=((math.floor(x/24)+math.floor(y/24))%2==0) and 226 or 238
 im:drawPixel(x,y,pc.rgba(v,v,v,255))
end end
for i,sprite in ipairs(results) do
 for y=0,179 do for x=0,179 do
  local c=sprite:getPixel(x,y)
  if pc.rgbaA(c)>0 then for dy=0,3 do for dx=0,3 do
   im:drawPixel(20+(i-1)*720+x*4+dx,20+y*4+dy,c)
  end end end
 end end
end
app.command.SaveFileAs{ui=false,filename=work..'pixel180-comparison_v001.png'}
print('PIXEL180_OK')
