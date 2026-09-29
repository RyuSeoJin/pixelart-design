-- CHANGELOG v1.0 · 2026-09-29 — 가슴 돌출·호흡 윤곽·꼬리 안쪽의 가시를 다듬습니다.
local root='P:/github-repository/pixelart-design/projects/pixelart-character/source/arctic-fox/'
local pc=app.pixelColor
local function read(p) local s=app.open(root..p);local im=Image(s.spec);im:drawSprite(s,1);s:close();return im end
local function save(im,p) local s=Sprite(im.width,im.height,ColorMode.RGB);s.cels[1].image=im;app.activeSprite=s;s:saveAs(root..p);s:close() end
local function dark(c) return pc.rgbaA(c)>0 and pc.rgbaR(c)<112 and pc.rgbaB(c)<160 end
local result={}
for _,cfg in ipairs({{'idle','left',6,0.25},{'idle','right',6,0.25},{'walk','left',8,0.1}}) do
 local motion,side,count,duration=table.unpack(cfg);local key=motion..'-'..side;result[key]={}
 local native=Sprite(180,180,ColorMode.RGB);native.layers[1].name='full_frame'
 local sheet=Image(180*count,180,ColorMode.RGB)
 for i=0,count-1 do
  local im=read('image-undecided/180/anim-'..motion..'/'..side..'/frame-'..string.format('%02d',i)..'_v006.png')
  local function xx(x) return side=='left' and x or 179-x end
  -- 가슴 앞쪽의 짧은 돌출과 불필요한 안쪽 꺾임을 한 줄의 윤곽으로 연결합니다.
  for y=65,84 do
   local edge=nil
   for x=73,88 do if pc.rgbaA(im:getPixel(xx(x),y))>0 then edge=x;break end end
   if edge and edge<=81 then
    local target=80
    local border=im:getPixel(xx(edge),y)
    if not dark(border) then border=pc.rgba(64,64,104,255) end
    local interior=nil
    for x=math.max(edge,target)+1,math.max(edge,target)+7 do local c=im:getPixel(xx(x),y)
     if pc.rgbaA(c)>0 and pc.rgbaR(c)>=184 then interior=c;break end
    end
    interior=interior or pc.rgba(232,232,248,255)
    for x=math.min(edge,target),target-1 do im:drawPixel(xx(x),y,0) end
    im:drawPixel(xx(target),y,border)
    for x=target+1,target+3 do
     local c=im:getPixel(xx(x),y)
     if pc.rgbaA(c)==0 or dark(c) then im:drawPixel(xx(x),y,interior) else break end
    end
   end
  end
  -- 꼬리의 움푹한 안쪽 곡선에 붙은 짧은 가지를 제거합니다.
  local bottom=0
  for y=130,166 do for x=114,148 do if pc.rgbaA(im:getPixel(xx(x),y))>0 then bottom=math.max(bottom,y) end end end
  local dy=bottom-160
  local rightedge=0
  for x=110,149 do if pc.rgbaA(im:getPixel(xx(x),140+dy))>0 then rightedge=x end end
  local dx=rightedge-141
  local shape={[144]=117,[145]=118,[146]=120,[147]=121,[148]=122,[149]=123,[150]=123,[151]=123}
  for y=144,151 do
   local yy=y+dy;local target=shape[y]+dx
   local edge=nil
   for x=110,140 do if pc.rgbaA(im:getPixel(xx(x),yy))>0 then edge=x;break end end
   if edge and edge<target then
    local border=im:getPixel(xx(edge),yy)
    if not dark(border) then border=pc.rgba(64,64,104,255) end
    for x=edge,target-1 do im:drawPixel(xx(x),yy,0) end
    if pc.rgbaA(im:getPixel(xx(target),yy))>0 then im:drawPixel(xx(target),yy,border) end
   end
  end
  local stem='image-undecided/180/anim-'..motion..'/'..side..'/'
  save(im,stem..'frame-'..string.format('%02d',i)..'_v007.png')
  result[key][i+1]=im;sheet:drawImage(im,Point(i*180,0))
  if i==0 then native.cels[1].image=im else local f=native:newEmptyFrame();native:newCel(native.layers[1],f,im,Point(0,0)) end
  native.frames[i+1].duration=duration
 end
 local tag=native:newTag(1,count);tag.name=motion..'_'..side
 app.activeSprite=native;native:saveAs(root..'work/'..key..'_v007.aseprite');native:saveAs(root..'image-undecided/180/anim-'..motion..'/'..side..'/preview_v007.gif');native:close()
 save(sheet,'image-undecided/180/anim-'..motion..'/'..side..'/sheet_v007.png')
end
for _,motion in ipairs({'idle','walk'}) do
 local sides=motion=='idle' and {'left','right'} or {'left'};local count=motion=='idle' and 6 or 8
 local s=Sprite(540*#sides,540,ColorMode.RGB)
 local contact=Image(540*4,540*math.ceil(count/4),ColorMode.RGB)
 for i=1,count do
  local out=Image(540*#sides,540,ColorMode.RGB)
  for n,side in ipairs(sides) do local im=result[motion..'-'..side][i]
   for y=0,179 do for x=0,179 do local c=im:getPixel(x,y)
    if pc.rgbaA(c)==0 then local tone=((math.floor(x/6)+math.floor(y/6))%2==0) and 238 or 222;c=pc.rgba(tone,tone,tone,255) end
    for yy=0,2 do for xx=0,2 do out:drawPixel((n-1)*540+x*3+xx,y*3+yy,c) end end
   end end
  end
  if motion=='walk' then contact:drawImage(out,Point(((i-1)%4)*540,math.floor((i-1)/4)*540)) end
  if i==1 then s.cels[1].image=out else local f=s:newEmptyFrame();s:newCel(s.layers[1],f,out,Point(0,0)) end
  s.frames[i].duration=motion=='idle' and 0.25 or 0.1
 end
 app.activeSprite=s;s:saveAs(root..'work/'..motion..'-contour-preview_v007.gif');s:close()
 if motion=='walk' then save(contact,'work/walk-contour-contact_v007.png') end
end
print('CONTOUR_CLEANUP_V007')
