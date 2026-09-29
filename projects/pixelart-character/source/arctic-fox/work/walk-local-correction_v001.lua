-- CHANGELOG v1.0 · 2026-09-29 — sprite-gen 하체 동작과 승인 원본을 대조하는 국소 수정 시험
local root='P:/github-repository/pixelart-design/projects/pixelart-character/source/arctic-fox/'
local pc=app.pixelColor
local function read(path) local s=app.open(path);local im=Image(s.spec);im:drawSprite(s,1);s:close();return im end
local function save(im,path) local s=Sprite(im.width,im.height,ColorMode.RGB);s.cels[1].image=im;app.activeSprite=s;s:saveAs(path);s:close() end
local src=read(root..'image-confirmed/180/view/side_left_v010.png')
local palette={};local seen={}
for y=0,179 do for x=0,179 do local c=src:getPixel(x,y)
 if pc.rgbaA(c)>0 and not seen[c] then palette[#palette+1]=c;seen[c]=true end
end end
local mapped={}
local function recolor(c)
 if pc.rgbaA(c)==0 then return 0 end
 if mapped[c] then return mapped[c] end
 local r,g,b=pc.rgbaR(c),pc.rgbaG(c),pc.rgbaB(c)
 -- 하체만 적용: 피부·눈 색을 제외하고 원본의 천·바지·부츠·외곽색과 비교합니다.
 local best,dist=nil,1e12
 for _,v in ipairs(palette) do local rr,gg,bb=pc.rgbaR(v),pc.rgbaG(v),pc.rgbaB(v)
  if not (rr>gg+12) and not (gg-rr>20 or bb-rr>65) then
   local d=(rr-r)^2+(gg-g)^2+(bb-b)^2
   if d<dist then dist=d;best=v end
  end
 end
 mapped[c]=best;return best
end
local dy={0,1,0,-1,0,1,0,-1}
local arm={2,1,0,-1,-2,-1,0,1}
local contact=Image(1440,180,ColorMode.RGB)
for i=0,7 do
 local gen=read(root..'work/spritegen-walk-left-scaled-ref/frames/walk/frame-'..i..'.png')
 local out=Image(180,180,ColorMode.RGB)
 -- 원본 꼬리를 먼저 그리고 상반신은 하나의 연속 격자에서 소매 쪽만 작게 변형합니다.
 for y=0,179 do for x=0,179 do local c=src:getPixel(x,y)
  local tail=y>=110 and x>=107
  if tail and pc.rgbaA(c)>0 then out:drawPixel(x,y+dy[i+1],c) end
 end end
 for y=0,111 do for x=0,179 do
  local shift=0
  if y>=70 and x>=86 then shift=math.floor(arm[i+1]*math.min(1,(y-70)/30)+0.5) end
  local sx=x-shift
  if sx>=0 and sx<180 then local c=src:getPixel(sx,y)
   if pc.rgbaA(c)>0 then out:drawPixel(x,y+dy[i+1],c) end
  end
 end end
 -- 하체에 공통 변환을 적용하며 프레임별 경계 상자 맞춤은 사용하지 않습니다.
 for y=111,170 do
  local sy=math.floor(98+(y-111)*72/59+0.5)
  for x=35,125 do
   local gx=x-11
   local maxx=sy<140 and (94+(sy-98)*0.32) or (sy<154 and 115 or 140)
   local minx=sy<110 and 68 or 0
   if gx>=minx and gx<=maxx then
    local c=gen:getPixel(gx,sy)
    if pc.rgbaA(c)>0 then out:drawPixel(x,y,recolor(c)) end
   end
  end
 end
 -- 승인 원본 손을 하체 앞에 다시 놓아 피부와 외곽선 연결을 보존합니다.
 for y=98,113 do for x=90,101 do local c=src:getPixel(x,y)
  if pc.rgbaA(c)>0 then out:drawPixel(x+arm[i+1],y+dy[i+1],c) end
 end end
 save(out,root..'work/walk-corrected-left/frame-'..string.format('%02d',i)..'_v001.png')
 contact:drawImage(out,Point(i*180,0))
end
save(contact,root..'work/walk-local-correction-contact_v001.png')
print('LOCAL_CORRECTION_EXPERIMENT_COMPLETE')
