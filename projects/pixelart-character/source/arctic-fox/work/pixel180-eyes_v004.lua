-- CHANGELOG v1.0 · 2026-09-28 — 승인된 이동용 시점을 기준으로 같은 180 격자에서 눈매를 정리합니다.
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
 local s=app.open(native..'three-quarter_'..side..'_v003.aseprite')
 local dst=s.cels[1].image
 -- 승인된 이동용 3/4의 얇은 눈꺼풀·세로 홍채를 180 원래 격자에 옮깁니다.
 local ink={D='383C55',K='221A26',W='F4F7FA',i='2A4F80',e='3E8FB8',c='7FD0E0',s='F6D2BC'}
 local x=side=='left' and 84 or 88
 local rows=side=='left' and {'sDDDK','DieWW','WecWs','sccss'} or {'KDDss','WWiDD','sWecW','ssccs'}
 if side=='left' then dst:drawPixel(83,37,fromhex('F6D2BC'))
 else dst:drawPixel(87,38,fromhex('F6D2BC')) end
 for j,row in ipairs(rows) do for i=1,#row do dst:drawPixel(x+i-1,36+j,fromhex(ink[row:sub(i,i)])) end end
 -- 승인 8종의 귀 안쪽은 밝은 회청색입니다. 이전 피부색 정리에서 남은 귀의 살색을 제거합니다.
 for y=11,27 do for x=0,179 do
  local v=dst:getPixel(x,y)
  if v==fromhex('F6D2BC') or v==fromhex('E2A895') or v==fromhex('B87574') or v==fromhex('7A4A58') then dst:drawPixel(x,y,fromhex('C3CCD8')) end
 end end
 local newcolors={'221A26','FFF1E4','F6D2BC','E2A895','B87574','7A4A58',
 'F4F7FA','C3CCD8','8C97AD','5B637F','383C55','7FD0E0','3E8FB8','2A4F80'}
 local pal=Palette(#newcolors+1)
 pal:setColor(0,Color{r=0,g=0,b=0,a=0})
 for i,h in ipairs(newcolors) do local c=fromhex(h);pal:setColor(i,Color{r=pc.rgbaR(c),g=pc.rgbaG(c),b=pc.rgbaB(c),a=255}) end
 s:setPalette(pal)
 local name='three-quarter_'..side..'_v004'
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
app.command.SaveFileAs{ui=false,filename=work..'pixel180-comparison_v004.png'}
print('PIXEL180_OK')
