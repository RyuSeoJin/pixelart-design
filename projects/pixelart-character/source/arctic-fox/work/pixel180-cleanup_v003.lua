-- CHANGELOG v1.0 · 2026-09-28 — 피부 기본색과 바지 내부 명암 조각을 정리하며 좌표·알파를 보존합니다.
local root = 'P:/github-repository/pixelart-design/projects/pixelart-character/'
local work = root .. 'source/arctic-fox/work/'
local output = root .. 'source/arctic-fox/image-undecided/180/view/'
local native = root .. 'sprites/arctic-fox/'
app.fs.makeAllDirectories(output)
app.fs.makeAllDirectories(native)
local pc = app.pixelColor
local function fromhex(h)
 return pc.rgba(tonumber(h:sub(1,2),16),tonumber(h:sub(3,4),16),tonumber(h:sub(5,6),16),255)
end
-- 같은 명암 역할에 섞였던 온색·회보라색을 회청색 단계로 통일합니다.
local replacements={FAF6F0='F4F7FA',E3DCD8='C3CCD8',BCB0BC='C3CCD8',
 ['8A7D97']='5B637F',['5A506E']='383C55'}
local results={}
for _,side in ipairs({'left','right'}) do
 local s=app.open(native..'three-quarter_'..side..'_v002.aseprite')
 local dst=s.cels[1].image
 -- 얼굴과 손의 가장 밝은 피부 면을 동일한 기본색으로 통일합니다.
 for it in dst:pixels() do
  if it()==fromhex('FFF1E4') then it(fromhex('F6D2BC')) end
 end
 local base,shade,light=fromhex('8C97AD'),fromhex('5B637F'),fromhex('C3CCD8')
 local function cloth(c) return c==base or c==shade end
 -- 바지 내부에서만 작은 밝은 점을 정리합니다. 실루엣과 짙은 경계선은 보존합니다.
 for pass=1,2 do
  local before=Image(dst)
  for y=104,139 do for x=73,107 do
   local c=before:getPixel(x,y)
   local nb,ns=0,0
   for dy=-1,1 do for dx=-1,1 do
    local v=before:getPixel(x+dx,y+dy)
    if v==base then nb=nb+1 elseif v==shade then ns=ns+1 end
   end end
   if c==light and nb+ns>=5 then dst:drawPixel(x,y,nb>=ns and base or shade)
   elseif cloth(c) and nb+ns>=7 then
    if nb>=6 then dst:drawPixel(x,y,base) elseif ns>=6 then dst:drawPixel(x,y,shade) end
   end
  end end
 end
 local newcolors={'221A26','FFF1E4','F6D2BC','E2A895','B87574','7A4A58',
 'F4F7FA','C3CCD8','8C97AD','5B637F','383C55','7FD0E0','3E8FB8','2A4F80'}
 local pal=Palette(#newcolors+1)
 pal:setColor(0,Color{r=0,g=0,b=0,a=0})
 for i,h in ipairs(newcolors) do local c=fromhex(h);pal:setColor(i,Color{r=pc.rgbaR(c),g=pc.rgbaG(c),b=pc.rgbaB(c),a=255}) end
 s:setPalette(pal)
 local name='three-quarter_'..side..'_v003'
 s:saveAs(native..name..'.aseprite')
 app.command.SaveFileAs{ui=false,filename=output..name..'.png'}
 results[#results+1]=Image(dst)
 s:close()
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
app.command.SaveFileAs{ui=false,filename=work..'pixel180-comparison_v003.png'}
print('PIXEL180_OK')
