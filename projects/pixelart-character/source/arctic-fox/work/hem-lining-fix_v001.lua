-- CHANGELOG v1.0 · 2026-09-29 — 옆트임 안감·옷단 경계를 idle 좌우와 walk 좌향에 적용합니다.
local root='P:/github-repository/pixelart-design/projects/pixelart-character/source/arctic-fox/'
local pc=app.pixelColor
local function read(path) local s=app.open(path);local im=Image(s.spec);im:drawSprite(s,1);s:close();return im end
local function save(im,path) local s=Sprite(im.width,im.height,ColorMode.RGB);s.cels[1].image=im;app.activeSprite=s;s:saveAs(path);s:close() end
local configs={{'idle','left',6,0.25},{'idle','right',6,0.25},{'walk','left',8,0.1}}
local outline=pc.rgba(104,112,152,255)
local lining=pc.rgba(184,192,224,255)
local light=pc.rgba(208,216,240,255)
local result={}
for _,cfg in ipairs(configs) do
 local motion,side,count,duration=table.unpack(cfg)
 local key=motion..'-'..side;result[key]={}
 local native=Sprite(180,180,ColorMode.RGB);native.layers[1].name='full_frame'
 for i=0,count-1 do
  local im=read(root..'image-undecided/180/anim-'..motion..'/'..side..'/frame-'..string.format('%02d',i)..'_v004.png')
  if motion=='walk' then
   local src=read(root..'image-confirmed/180/view/side_left_v010.png')
   local bob={0,1,0,-1,0,1,0,-1};local dy=bob[i+1]
   for y=98,108 do for x=84,91 do
    local existing=im:getPixel(x,y+dy)
    if not (pc.rgbaR(existing)>pc.rgbaG(existing)+10) then im:drawPixel(x,y+dy,src:getPixel(x,y)) end
   end end
  end
  local function put(x,y,c)
   local yy=y
   if motion=='idle' then
    local shifts={0,1,1,1,-1,-2};yy=y+shifts[i+1]
    if i==4 and y>=106 then yy=y end
    if side=='right' then x=179-x end
   else
    local bob={0,1,0,-1,0,1,0,-1}
    yy=y+bob[i+1]
   end
   im:drawPixel(x,yy,c)
   if motion=='idle' and i==4 and y==105 then im:drawPixel(x,105,c) end
  end
  -- 짧은 트임의 꼭짓점과 좁은 안감, 양옆 경계를 정리합니다.
  put(86,99,lining)
  for y=100,107 do
   put(85,y,outline);put(86,y,lining);put(87,y,light);put(88,y,outline)
  end
  for x=85,88 do put(x,108,outline) end
  save(im,root..'image-undecided/180/anim-'..motion..'/'..side..'/frame-'..string.format('%02d',i)..'_v005.png')
  save(im,root..'work/hem-fix-'..key..'/frame-'..string.format('%02d',i)..'_v005.png')
  result[key][i+1]=im
  if i==0 then native.cels[1].image=im else local f=native:newEmptyFrame();native:newCel(native.layers[1],f,im,Point(0,0)) end
  native.frames[i+1].duration=duration
 end
 local tag=native:newTag(1,count);tag.name=motion..'_'..side
 app.activeSprite=native;native:saveAs(root..'work/'..motion..'-'..side..'_v005.aseprite');native:close()
end
for _,motion in ipairs({'idle','walk'}) do
 local sides=motion=='idle' and {'left','right'} or {'left'}
 local count=motion=='idle' and 6 or 8
 local s=Sprite(540*#sides,540,ColorMode.RGB)
 for i=1,count do
  local out=Image(540*#sides,540,ColorMode.RGB)
  for n,side in ipairs(sides) do local im=result[motion..'-'..side][i]
   for y=0,179 do for x=0,179 do local c=im:getPixel(x,y)
    for yy=0,2 do for xx=0,2 do out:drawPixel((n-1)*540+x*3+xx,y*3+yy,c) end end
   end end
  end
  if i==1 then s.cels[1].image=out else local f=s:newEmptyFrame();s:newCel(s.layers[1],f,out,Point(0,0)) end
  s.frames[i].duration=motion=='idle' and 0.25 or 0.1
 end
 app.activeSprite=s;s:saveAs(root..'work/'..motion..'-hem-preview_v005.gif');s:close()
end
local detail=Image(768,192,ColorMode.RGB)
for n=0,3 do
 local motion=n<2 and 'idle' or 'walk';local version=n%2==0 and '004' or '005'
 local im=read(root..'image-undecided/180/anim-'..motion..'/left/frame-00_v'..version..'.png')
 for y=0,23 do for x=0,23 do local c=im:getPixel(78+x,92+y)
  for yy=0,7 do for xx=0,7 do detail:drawPixel(n*192+x*8+xx,y*8+yy,c) end end
 end end
end
save(detail,root..'work/hem-detail_v001.png')
print('HEM_LINING_FIX_COMPLETE')
