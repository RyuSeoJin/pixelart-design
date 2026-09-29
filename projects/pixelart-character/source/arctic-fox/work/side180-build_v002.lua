-- CHANGELOG v1.0 · 2026-09-28 — 측면 원형을 180 격자·소재별 공통 팔레트로 정리합니다.
local root = 'P:/github-repository/pixelart-design/projects/pixelart-character/'
local work = root .. 'source/arctic-fox/work/'
local output = root .. 'source/arctic-fox/image-undecided/180/view/'
local native = root .. 'sprites/arctic-fox/'
app.fs.makeAllDirectories(output)
app.fs.makeAllDirectories(native)
local pc = app.pixelColor
local colors = {'221A26','F6D2BC','E2A895','B87574','7A4A58',
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
  local warm=(r-g>12 and r-b>17 and g>70)
  local skin=(p[1]-p[2]>12 and p[1]-p[3]>17)
  local d=(r-p[1])^2+(g-p[2])^2+(b-p[3])^2
  if warm~=skin then d=d+1000000 end
  if d<dist then best,dist=p,d end
 end
 return pc.rgba(best[1],best[2],best[3],255)
end

local src=app.open(work..'side-pair-generated_v002.png')
local raw=Image(src.spec);raw:drawSprite(src,1)
local results={}
for i,side in ipairs({'left','right'}) do
 local s=Sprite(180,180,ColorMode.RGB)
 s.layers[1].name='native-180'
 local dst=s.cels[1].image
 local center=i==1 and 580 or 1194
 -- 좌우 모두 같은 신체 배율을 사용하며 귀·꼬리 경계로 따로 맞추지 않습니다.
 for y=0,179 do for x=0,179 do
  local sx=math.floor(center+(x-89.5)/0.145+0.5)
  local sy=math.floor(94+(y-29)/ (142/782)+0.5)
  if sx>=(i-1)*887 and sx<i*887 and sy>=0 and sy<raw.height and y<=170 then
   local c=raw:getPixel(sx,sy)
   if valid(c) then dst:drawPixel(x,y,quantize(c)) end
  end
 end end
 local pal=Palette(#palette+1);pal:setColor(0,Color{r=0,g=0,b=0,a=0})
 for k,p in ipairs(palette) do pal:setColor(k,Color{r=p[1],g=p[2],b=p[3],a=255}) end
 s:setPalette(pal)
 local name='side_'..side..'_v002'
 s:saveAs(native..name..'.aseprite')
 app.command.SaveFileAs{ui=false,filename=output..name..'.png'}
 results[i]=Image(dst);s:close()
end
src:close()
local preview=Sprite(1480,760,ColorMode.RGB);local im=preview.cels[1].image
for y=0,759 do for x=0,1479 do
 local v=((math.floor(x/24)+math.floor(y/24))%2==0) and 226 or 238
 im:drawPixel(x,y,pc.rgba(v,v,v,255))
end end
for i,sp in ipairs(results) do for y=0,179 do for x=0,179 do
 local c=sp:getPixel(x,y)
 if pc.rgbaA(c)>0 then for dy=0,3 do for dx=0,3 do
 im:drawPixel(20+(i-1)*720+x*4+dx,20+y*4+dy,c)
 end end end
end end end
app.command.SaveFileAs{ui=false,filename=work..'side180-comparison_v002.png'}
print('PAIR_DRAFT_SAVED')


