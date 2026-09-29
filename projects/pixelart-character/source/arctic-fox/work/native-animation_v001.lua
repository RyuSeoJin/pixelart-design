-- CHANGELOG v1.0 · 2026-09-28 — 확정 좌우 도트를 공통 관절 이동으로 애니메이션화
local root='P:/github-repository/pixelart-design/projects/pixelart-character/'
local base=root..'source/arctic-fox/'
local pc=app.pixelColor
local function rgba(h) return pc.rgba(tonumber(h:sub(1,2),16),tonumber(h:sub(3,4),16),tonumber(h:sub(5,6),16),255) end
local white,shadow,blue,dark=rgba('F4F7FA'),rgba('C3CCD8'),rgba('8C97AD'),rgba('5B637F')
local function blank() return Image(180,180,ColorMode.RGB) end
local function round(n) return math.floor(n+0.5) end
local function read(path) local s=app.open(path);local im=Image(s.spec);im:drawSprite(s,1);s:close();return im end
local function mirrorCoords(im,right)
 local out=blank();for y=0,179 do for x=0,179 do out:drawPixel(x,y,im:getPixel(right and 179-x or x,y)) end end;return out
end
local function stamp(dst,src,dx,dy,far)
 for y=0,179 do for x=0,179 do local c=src:getPixel(x,y)
 if pc.rgbaA(c)>0 then
  if far then if c==white then c=shadow elseif c==shadow then c=blue elseif c==blue then c=dark end end
  local xx,yy=x+dx,y+dy;if xx>=0 and xx<180 and yy>=0 and yy<180 then dst:drawPixel(xx,yy,c) end
 end end end
end
local function armPixel(x,y)
 if y<61 or y>112 then return false end
 local edge= y<86 and 85 or (y<103 and 84 or 88)
 return x>=edge and x<=102
end
local function parts(im)
 local torso,arm,leg,tail=blank(),blank(),blank(),blank()
 for y=0,179 do for x=0,179 do local c=im:getPixel(x,y)
  if pc.rgbaA(c)>0 then
   if y>=100 and x>=99 then tail:drawPixel(x,y,c)
   elseif y>=112 then leg:drawPixel(x,y,c)
   elseif armPixel(x,y) then arm:drawPixel(x,y,c)
   else torso:drawPixel(x,y,c) end
  end
 end end
 -- 팔이 가린 튜닉 면만 기존 팔레트로 연결합니다.
 for y=65,109 do for x=84,94 do
  if armPixel(x,y) then torso:drawPixel(x,y,y>=102 and blue or white) end
 end end
 return torso,arm,leg,tail
end
local function armWarp(src,offset,bob)
 local im=blank();for y=0,179 do for x=0,179 do local c=src:getPixel(x,y)
 if pc.rgbaA(c)>0 then local dx=round(offset*math.max(0,(y-61)/51));im:drawPixel(x+dx,y+bob,c) end
 end end;return im
end
local function tailWarp(src,offset,bob)
 local im=blank();for y=0,179 do for x=0,179 do local c=src:getPixel(x,y)
 if pc.rgbaA(c)>0 then local dx=round(offset*math.max(0,(y-100)/47));im:drawPixel(x+dx,y+bob,c) end
 end end;return im
end
local function legWarp(src,footX,lift,bob)
 local im=blank();local hx,hy=90,100+bob;local ax,ay=89+footX,160-lift
 local dx,dy=ax-hx,ay-hy;local dist=math.sqrt(dx*dx+dy*dy)
 local bend=math.sqrt(math.max(0,30.5*30.5-dist*dist/4))
 local kx,ky=(hx+ax)/2-dy/dist*bend,(hy+ay)/2+dx/dist*bend
 local startY=112+bob;local startX=hx+(kx-hx)*(startY-hy)/(ky-hy)
 local dstY={startY,ky,ay-14,ay+10};local srcY={112,133,146,170};local centers={startX,kx,ax,ax}
 for seg=1,3 do
  for y=round(dstY[seg]),round(dstY[seg+1]) do
   local t=(y-dstY[seg])/(dstY[seg+1]-dstY[seg]);t=math.max(0,math.min(1,t))
   local sy=round(srcY[seg]+t*(srcY[seg+1]-srcY[seg]));local cx=centers[seg]+t*(centers[seg+1]-centers[seg])
   for x=68,110 do local sx=round(x-(cx-89));if sx>=0 and sx<180 then
    local c=src:getPixel(sx,sy);if pc.rgbaA(c)>0 and y>=0 and y<180 then im:drawPixel(x,y,c) end
   end end
  end
 end
 return im,{hip={hx,hy},knee={kx,ky},ankle={ax,ay},sole=170-lift}
end
local function saveImage(im,path)
 local s=Sprite(180,180,ColorMode.RGB);s.cels[1].image=im;app.command.SaveFileAs{ui=false,filename=path};s:close()
end
local idleMs={260,200,260,200};local bobIdle={0,1,2,1}
local stride={-10,-5,0,6,11,7,0,-7};local lift={0,0,0,0,0,4,9,6};local bobWalk={0,1,0,-1,0,1,0,-1}
for _,side in ipairs({'left','right'}) do
 local right=side=='right';local original=read(base..'image-confirmed/180/view/side_'..side..'_v002.png')
 local normalized=mirrorCoords(original,right);local torso,arm,leg,tail=parts(normalized)
 for _,motion in ipairs({'idle','walk'}) do
  local folder=base..'image-undecided/180/anim-'..motion..'/'..side..'/'
  app.fs.makeAllDirectories(folder)
  local count=motion=='idle' and 4 or 8;local s=Sprite(180,180,ColorMode.RGB)
  s.layers[1].name='꼬리';local layers={s.layers[1]}
  for _,name in ipairs({'먼 다리','먼 팔','몸통·머리','가까운 다리','가까운 팔'}) do local l=s:newLayer();l.name=name;layers[#layers+1]=l end
  local frames={}
  for i=1,count do
   if i>1 then s:newEmptyFrame() end
   local pieces={blank(),blank(),blank(),blank(),blank(),blank()}
   if motion=='idle' then
    -- 얼굴을 포함한 상체 도트를 정수 이동하고 부츠는 원본 위치에 고정합니다.
    local im=blank();local b=bobIdle[i]
    for y=0,179 do for x=0,179 do local c=normalized:getPixel(x,y)
     if pc.rgbaA(c)>0 then local off=y<112 and b or (y<146 and round(b*(146-y)/34) or 0);im:drawPixel(x,y+off,c) end
    end end
    pieces[4]=im
   else
    local j=((i+3)%8)+1;local b=bobWalk[i]
    pieces[1]=tailWarp(tail,({0,1,2,1,0,-1,-2,-1})[i],b)
    local far=legWarp(leg,stride[j],lift[j],b);stamp(pieces[2],far,0,0,true)
    local swing=round(-stride[i]*0.6)
    local farArm=armWarp(arm,-swing,b);stamp(pieces[3],farArm,-3,0,true)
    stamp(pieces[4],torso,0,b,false)
    pieces[5]=legWarp(leg,stride[i],lift[i],b)
    pieces[6]=armWarp(arm,swing,b)
   end
   local flat=blank()
   for n,p in ipairs(pieces) do
    p=mirrorCoords(p,right);s:newCel(layers[n],i,p,Point(0,0));stamp(flat,p,0,0,false)
   end
   s.frames[i].duration=(motion=='idle' and idleMs[i] or 100)/1000;frames[i]=flat
  end
  local tag=s:newTag(1,count);tag.name=motion..'_'..side
  s:saveAs(root..'sprites/arctic-fox/'..motion..'_'..side..'_v001.aseprite')
  app.command.SaveFileAs{ui=false,filename=folder..'preview_v001.gif'}
  s:close()
  local sheet=Sprite(180*count,180,ColorMode.RGB);local si=sheet.cels[1].image
  for i,im in ipairs(frames) do si:drawImage(im,Point((i-1)*180,0)) end
  app.command.SaveFileAs{ui=false,filename=folder..'sheet_v001.png'};sheet:close()
  for i,im in ipairs(frames) do saveImage(im,folder..string.format('frame-%02d_v001.png',i-1)) end
 end
end
print('NATIVE_ANIMATIONS_WRITTEN')
