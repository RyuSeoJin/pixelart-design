-- CHANGELOG v1.0 · 2026-09-29 — 승인 우향 원본으로 우향 보행을 제작하고 좌향 승인 리듬을 적용합니다.
local root='P:/github-repository/pixelart-design/projects/pixelart-character/source/arctic-fox/'
local pc=app.pixelColor
local function read(p) local s=app.open(root..p);local im=Image(s.spec);im:drawSprite(s,1);s:close();return im end
local function save(im,p) local s=Sprite(im.width,im.height,ColorMode.RGB);s.cels[1].image=im;app.activeSprite=s;s:saveAs(root..p);s:close() end
local function dark(c) return pc.rgbaA(c)>0 and pc.rgbaR(c)<112 and pc.rgbaB(c)<160 end
local function round(x) return math.floor(x+0.5) end
local function lerp(a,b,t) return a+(b-a)*t end
local original=read('image-confirmed/180/view/side_right_v010.png')
-- 관절 계산만 진행 방향으로 정규화합니다. 외형 픽셀은 우향 승인 원본에서 가져옵니다.
local function flip(im)
 local out=Image(180,180,ColorMode.RGB)
 for y=0,179 do for x=0,179 do out:drawPixel(179-x,y,im:getPixel(x,y)) end end
 return out
end
local src=flip(original)
local outline=pc.rgba(64,64,104,255)
local bob={0,1,0,-1,0,1,0,-1}
local bx={81,86,91,96,101,98,90,82}
local by={170,170,170,170,170,164,161,165}
local kx={85,87,89,92,94,90,81,79}
local ky={131,132,131,130,130,129,128,130}
-- 꼬리 왼쪽을 고정 열로 자르지 않고 승인 원본의 실제 윤곽을 따라 추출합니다.
local tailstart={}
for y=98,160 do
 local lower=y>=140 and 108 or (y>=138 and 106 or (y>=134 and 105 or 99))
 local first=nil
 for x=lower,149 do local c=src:getPixel(x,y)
  if pc.rgbaA(c)>0 and (y>=134 or pc.rgbaR(c)>=192) then first=x;break end
 end
 if first then tailstart[y]=y>=134 and first or first-2 end
end
local function leg(i,far,dy)
 local k=((i+(far and 4 or 0))%8)+1
 local hip=far and 92 or 89;local fx=bx[k]+(far and 2 or 0)
 local sole=by[k];local cuff=sole-25
 local knee=kx[k]+(far and 2 or 0);local kny=ky[k]+dy
 local top=103+dy;local out=Image(180,180,ColorMode.RGB)
 for y=top,cuff+2 do
  local upper=y<=kny
  local t=math.max(0,math.min(1,upper and (y-top)/(kny-top) or (y-kny)/(cuff+2-kny)))
  local cx=upper and lerp(hip,knee,t) or lerp(knee,fx,t)
  local sy=round(upper and lerp(110,132,t) or lerp(132,144,t))
  local half=upper and lerp(9,9.5,t) or lerp(9.5,8,t)
  local l,r=round(cx-half),round(cx+half)
  local samples={}
  for sx=80,101 do local c=src:getPixel(sx,sy)
   if pc.rgbaA(c)>0 and pc.rgbaR(c)<190 and pc.rgbaG(c)<190 then samples[#samples+1]=c end
  end
  for x=l,r do
   local u=(x-l)/(r-l);local index=1+round(u*(#samples-1))
   local c=samples[index] or pc.rgba(128,128,168,255)
   if x==l or x==r then c=outline end
   out:drawPixel(x,y,c)
  end
 end
 local toe={2,1,0,0,0,0,0,2};local heel={0,0,0,1,2,2,1,0}
 for y=144,170 do for x=75,103 do local c=src:getPixel(x,y)
  if pc.rgbaA(c)>0 then
   local roll=0
   if y>=151 then roll=-round(math.max(math.max(0,math.min(1,(94-x)/14))*toe[k],math.max(0,math.min(1,(x-84)/14))*heel[k])) end
   out:drawPixel(x+fx-94,y+sole-170+roll,c)
  end
 end end
 return out
end
local function slit(im,motion,side,i)
 local base=Image(im)
 local shifts={0,1,1,1,-1,-2}
 local function pos(x,y)
  if motion=='idle' then
   if side=='right' then x=179-x end
   if i==4 and y>=106 then return x,y end
   return x,y+shifts[i+1]
  end
  return x,y+bob[i+1]
 end
 -- 지난 보정의 평행한 띠를 제거하고 원래 옷감으로 복원합니다.
 for y=98,108 do for x=84,89 do local xx,yy=pos(x,y)
  local c=im:getPixel(xx,yy)
  if not (pc.rgbaR(c)>pc.rgbaG(c)+10) then im:drawPixel(xx,yy,base:getPixel(xx,yy)) end
 end end
 local lining=pc.rgba(184,192,224,255)
 local edge=pc.rgba(104,112,152,255)
 for y=99,107 do
  local left=85;local right=math.min(88,85+math.floor((y-99)/2))
  for x=left,right do
   local xx,yy=pos(x,y);local old=im:getPixel(xx,yy)
   if not (pc.rgbaR(old)>pc.rgbaG(old)+10) then im:drawPixel(xx,yy,(x==left or x==right) and edge or lining) end
  end
 end
end
local result={}
for _,cfg in ipairs({{'walk','left',8,0.1}}) do
 local motion,side,count,duration=table.unpack(cfg);local key=motion..'-'..side;result[key]={}
 local native=Sprite(180,180,ColorMode.RGB);native.layers[1].name='full_frame'
 local sheet=Image(180*count,180,ColorMode.RGB)
 for i=0,count-1 do
  local previous=Image(180,180,ColorMode.RGB)
  local arms={2,1,0,-1,-2,-1,0,1}
  local dy=bob[i+1]
  for y=0,179 do for x=0,179 do
   local shift=0
   if y>=70 and x>=86 then shift=round(arms[i+1]*math.min(1,(y-70)/30)) end
   local sx=x-shift
   if sx>=0 and sx<180 and y+dy>=0 and y+dy<180 then previous:drawPixel(x,y+dy,src:getPixel(sx,y)) end
  end end
  local im=Image(previous)
  if motion=='idle' and i>=1 and i<=3 then
   if side=='right' then
    local start=i==1 and 78 or 77
    for y=start,start+3 do im:drawPixel(99,y,0) end
    im:drawPixel(102,92,0);im:drawPixel(103,97,0)
   else im:drawPixel(77,92,0);im:drawPixel(76,97,0) end
  end
  if motion=='walk' then
   im=Image(180,180,ColorMode.RGB);local dy=bob[i+1]
   for y=98,160 do if tailstart[y] then
    local sway=round(math.sin(i/8*math.pi*2-0.7)*1.5*math.max(0,math.min(1,(y-108)/53)))
    for x=tailstart[y],149 do local c=src:getPixel(x,y)
     if pc.rgbaA(c)>0 then im:drawPixel(x+sway,y+dy,c) end
    end
   end end
   im:drawImage(leg(i,true,dy));im:drawImage(leg(i,false,dy))
   for y=0,108+dy do for x=0,179 do
    local sourcey=y-dy
    if not (sourcey>=98 and tailstart[sourcey] and x>=tailstart[sourcey]) then im:drawPixel(x,y,previous:getPixel(x,y)) end
   end end
   -- 허리 아래의 손은 피부색과 그에 인접한 기존 외곽선만 보존합니다.
   for y=109+dy,115+dy do for x=86,102 do local c=previous:getPixel(x,y)
    local skin=pc.rgbaR(c)>pc.rgbaG(c)+10
    local adjacent=false
    for dx=-1,1 do for ddy=-1,1 do local n=previous:getPixel(x+dx,y+ddy)
     if pc.rgbaA(n)>0 and pc.rgbaR(n)>pc.rgbaG(n)+10 then adjacent=true end
    end end
    if skin or (adjacent and pc.rgbaR(c)<110 and pc.rgbaA(c)>0) then im:drawPixel(x,y,c) end
   end end
  end
  -- 옆트임은 몸통을 따르고 팔 변형에서 분리합니다.
  for y=98,108 do for x=84,91 do
   local c=im:getPixel(x,y+bob[i+1])
   if not (pc.rgbaR(c)>pc.rgbaG(c)+10) then im:drawPixel(x,y+bob[i+1],src:getPixel(x,y)) end
  end end
  slit(im,motion,side,i)
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

  im=flip(im)
  local stem='image-undecided/180/anim-walk/right/'
  save(im,stem..'frame-'..string.format('%02d',i)..'_v002.png')
  result[key][i+1]=im;sheet:drawImage(im,Point(i*180,0))
  if i==0 then native.cels[1].image=im else local f=native:newEmptyFrame();native:newCel(native.layers[1],f,im,Point(0,0)) end
  native.frames[i+1].duration=duration
 end
 local tag=native:newTag(1,count);tag.name='walk_right'
 app.activeSprite=native;native:saveAs(root..'work/walk-right_v002.aseprite');native:saveAs(root..'image-undecided/180/anim-walk/right/preview_v002.gif');native:close()
 save(sheet,'image-undecided/180/anim-walk/right/sheet_v002.png')
end
for _,motion in ipairs({'walk'}) do
 local sides=motion=='idle' and {'left','right'} or {'left'};local count=motion=='idle' and 6 or 8
 local s=Sprite(540*#sides,540,ColorMode.RGB)
 local contact=Image(540*4,540*2,ColorMode.RGB)
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
 app.activeSprite=s;s:saveAs(root..'work/'..motion..'-right-preview_v002.gif');s:close()
 if motion=='walk' then save(contact,'work/walk-right-contact_v002.png') end
end
print('WALK_RIGHT_V002')

local pair=Sprite(1080,540,ColorMode.RGB)
for i=0,7 do
 local out=Image(1080,540,ColorMode.RGB)
 for n,config in ipairs({{'image-confirmed/180/anim-walk/left/','v007'},{'image-undecided/180/anim-walk/right/','v002'}}) do
  local im=read(config[1]..'frame-'..string.format('%02d',i)..'_'..config[2]..'.png')
  for y=0,179 do for x=0,179 do local c=im:getPixel(x,y)
   if pc.rgbaA(c)==0 then local tone=((math.floor(x/6)+math.floor(y/6))%2==0) and 238 or 222;c=pc.rgba(tone,tone,tone,255) end
   for yy=0,2 do for xx=0,2 do out:drawPixel((n-1)*540+x*3+xx,y*3+yy,c) end end
  end end
 end
 if i==0 then pair.cels[1].image=out else local f=pair:newEmptyFrame();pair:newCel(pair.layers[1],f,out,Point(0,0)) end
 pair.frames[i+1].duration=0.1
end
app.activeSprite=pair;pair:saveAs(root..'work/walk-both-preview_v001.gif');pair:close()
