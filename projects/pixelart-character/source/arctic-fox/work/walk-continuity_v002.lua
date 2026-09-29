-- CHANGELOG v1.0 · 2026-09-29 — 다리 정체성을 고정하고 승인 도트로 보행 하체를 다시 수정합니다.
local root='P:/github-repository/pixelart-design/projects/pixelart-character/source/arctic-fox/'
local pc=app.pixelColor
local function read(path) local s=app.open(path);local im=Image(s.spec);im:drawSprite(s,1);s:close();return im end
local function save(im,path) local s=Sprite(im.width,im.height,ColorMode.RGB);s.cels[1].image=im;app.activeSprite=s;s:saveAs(path);s:close() end
local src=read(root..'image-confirmed/180/view/side_left_v010.png')
local bx={81,86,91,96,101,98,90,82}
local by={170,170,170,170,170,164,161,165}
local kx={85,87,89,92,94,90,81,79}
local ky={131,132,131,130,130,129,128,130}
local bob={0,1,0,-1,0,1,0,-1}
local arm={2,1,0,-1,-2,-1,0,1}
local outline=src:getPixel(83,129)
-- 팔레트 안의 짙은 청회색을 외곽선으로 선택합니다.
local best=1e12
for y=110,169 do for x=75,103 do local c=src:getPixel(x,y)
 if pc.rgbaA(c)>0 then local d=(pc.rgbaR(c)-64)^2+(pc.rgbaG(c)-64)^2+(pc.rgbaB(c)-96)^2
  if d<best then best=d;outline=c end
 end
end end
local function lerp(a,b,t) return a+(b-a)*t end
local function leg(frame,far,bodydy)
 local q=far and ((frame+4)%8+1) or (frame+1)
 local hipx=far and 94 or 89
 local footx=bx[q]+(far and 2 or 0)
 local sole=by[q];local cuff=sole-25
 local kneex=kx[q]+(far and 2 or 0);local kneey=ky[q]+bodydy
 local im=Image(180,180,ColorMode.RGB)
 local top=108+bodydy
 for y=top,cuff+2 do
  local upper=y<=kneey
  local t=upper and (y-top)/(kneey-top) or (y-kneey)/(cuff+2-kneey)
  local cx=upper and lerp(hipx,kneex,t) or lerp(kneex,footx,t)
  local sy=math.floor((upper and lerp(110,132,t) or lerp(132,145,t))+0.5)
  local scx=upper and lerp(91,94,t) or lerp(94,94,t)
  for x=math.floor(cx-13),math.ceil(cx+12) do
   local sx=math.floor(scx+x-cx+0.5)
   if sx>=80 and sx<=103 then local c=src:getPixel(sx,sy)
    -- 꼬리의 흰색이 바지로 따라 들어오지 않도록 재질 영역을 제한합니다.
    if pc.rgbaA(c)>0 and pc.rgbaR(c)<190 and pc.rgbaG(c)<190 then im:drawPixel(x,y,c) end
   end
  end
 end
 -- 부츠는 같은 승인 도트를 정수 이동하여 발 길이와 흰 접힌 단을 유지합니다.
 for y=144,170 do for x=75,103 do local c=src:getPixel(x,y)
  local roll=0
  if y>=151 and q==1 then roll=-math.max(0,math.min(2,math.floor((94-x)/7))) end
  if y>=151 and q==5 then roll=-math.max(0,math.min(2,math.floor((x-84)/7))) end
  if pc.rgbaA(c)>0 then im:drawPixel(x+footx-94,y+sole-170+roll,c) end
 end end
 -- 겹치는 다리의 가림이 읽히도록 외측 경계만 같은 팔레트의 1px로 정리합니다.
 local final=Image(im)
 for y=top+2,170 do for x=40,125 do local c=im:getPixel(x,y)
  if pc.rgbaA(c)>0 and y<144+sole-170 then
   if pc.rgbaA(im:getPixel(x-1,y))==0 or pc.rgbaA(im:getPixel(x+1,y))==0 then final:drawPixel(x,y,outline) end
  end
 end end
 return final
end
local contact=Image(1440,180,ColorMode.RGB)
for i=0,7 do
 local out=Image(180,180,ColorMode.RGB);local dy=bob[i+1]
 for y=108,179 do for x=105,179 do local c=src:getPixel(x,y)
  local old_pants_edge=(x==105 and (y==138 or y==139))
  if pc.rgbaA(c)>0 and not old_pants_edge then out:drawPixel(x,y+dy,c) end
 end end
 out:drawImage(leg(i,true,dy),Point(0,0))
 out:drawImage(leg(i,false,dy),Point(0,0))
 for y=0,113 do for x=0,179 do
  local shift=0
  if y>=70 and x>=86 then shift=math.floor(arm[i+1]*math.min(1,(y-70)/30)+0.5) end
  local sx=x-shift
  if sx>=0 and sx<180 then local c=src:getPixel(sx,y)
   if pc.rgbaA(c)>0 then out:drawPixel(x,y+dy,c) end
  end
 end end
 save(out,root..'work/walk-corrected-left/frame-'..string.format('%02d',i)..'_v002.png')
 contact:drawImage(out,Point(i*180,0))
end
save(contact,root..'work/walk-continuity-contact_v002.png')
print('WALK_CONTINUITY_V002')
