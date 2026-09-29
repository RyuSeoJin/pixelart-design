-- 좌우 공통 윤곽에 방향별 채색을 맞추고 같은 180 격자에서 정리합니다.
local root='P:/github-repository/pixelart-design/projects/pixelart-character/'
local work=root..'source/arctic-fox/work/'
local out=root..'source/arctic-fox/image-undecided/180/view/'
local pc=app.pixelColor
local function rgb(h) return pc.rgba(tonumber(h:sub(1,2),16),tonumber(h:sub(3,4),16),tonumber(h:sub(5,6),16),255) end
local function solid(im,x,y) return x>=0 and y>=0 and x<180 and y<180 and pc.rgbaA(im:getPixel(x,y))>0 end
local sprites={};local imgs={}
for i,side in ipairs({'left','right'}) do
 local s=app.open(out..'side_'..side..'_v002.png');sprites[i]=s
 local im=Image(s.spec);im:drawSprite(s,1);imgs[i]=im
end
local left=imgs[1];local original=Image(left)
-- 꼬리 아래쪽만 공통 계획 높이로 줄이고 몸체·얼굴의 좌표는 유지합니다.
for y=103,170 do for x=100,179 do left:drawPixel(x,y,0) end end
for y=103,147 do for x=100,179 do
 local sy=103+math.floor((y-103)*59/44+0.5)
 if solid(original,x,sy) then left:drawPixel(x,y,original:getPixel(x,sy)) end
end end
-- 원래 꼬리 끝 아래의 독립 잔여 픽셀은 남기지 않습니다.
local function runs(im,y)
 local r={};local start=nil
 for x=0,180 do
  local on=x<180 and solid(im,x,y)
  if on and not start then start=x end
  if not on and start then r[#r+1]={start,x-1};start=nil end
 end
 return r
end
local right=Image(180,180,ColorMode.RGB)
-- 반전은 구조 가이드에만 적용합니다. 채색은 우측면 입력을 재배치합니다.
for y=0,170 do
 local guide=runs(left,y);local actual=runs(imgs[2],y)
 for n,run in ipairs(guide) do
  local lo,hi=179-run[2],179-run[1]
  local a=actual[#actual-n+1]
  for x=lo,hi do
   local c=rgb('F4F7FA')
   if a then
    local sx=a[1]+math.floor((x-lo)*(a[2]-a[1])/math.max(1,hi-lo)+0.5)
    c=imgs[2]:getPixel(sx,y)
   end
   right:drawPixel(x,y,c)
  end
 end
end
-- 꼬리의 방향별 조명은 같은 화면 광원으로 다시 정리합니다.
for i,im in ipairs({left,right}) do
 for y=105,147 do
  local minX,maxX=180,-1
  for x=0,179 do
   local istail=i==1 and x>=100 or i==2 and x<=79
   if istail and solid(im,x,y) then minX=math.min(minX,x);maxX=math.max(maxX,x) end
  end
  if maxX>=minX then
   for x=minX,maxX do if solid(im,x,y) then
    local boundary=not solid(im,x-1,y) or not solid(im,x+1,y) or not solid(im,x,y+1) or not solid(im,x,y-1)
    if boundary then im:drawPixel(x,y,rgb('383C55'))
    else
     local t=(x-minX)/math.max(1,maxX-minX)
     im:drawPixel(x,y,rgb(t>0.72 and 'C3CCD8' or 'F4F7FA'))
    end
   end end
  end
 end
end
-- 홍채 크기와 윗눈꺼풀은 양쪽 같은 목표값입니다. 고해상도 보정 없이 원 격자에 그립니다.
for i,im in ipairs({left,right}) do
 local function dot(x,y,h) if i==2 then x=179-x end;im:drawPixel(x,y,rgb(h)) end
 for x=81,84 do dot(x,42,'221A26') end
 dot(82,43,'2A4F80');dot(83,43,'3E8FB8')
 dot(82,44,'3E8FB8');dot(83,44,'7FD0E0')
 dot(82,45,'7FD0E0');dot(83,45,'7FD0E0')
 -- 작은 다문 입을 같은 높이에 둡니다.
 dot(79,49,'B87574');dot(80,49,'E2A895')
end
-- 바지에는 각 방향에서 다른 큰 접힘을 남겨 직물 구조를 표현합니다.
local function poly(im,points,h)
 for y=112,143 do for x=75,104 do
  local inside=false;local j=#points
  for k=1,#points do
   local a,b=points[k],points[j]
   if (a[2]>y)~=(b[2]>y) and x<(b[1]-a[1])*(y-a[2])/(b[2]-a[2])+a[1] then inside=not inside end
   j=k
  end
  if inside and solid(im,x,y) then
   local c=im:getPixel(x,y)
   if c==rgb('8C97AD') or c==rgb('5B637F') then im:drawPixel(x,y,rgb(h)) end
  end
 end end
end
poly(left,{{85,116},{98,129},{96,134},{87,123}},'5B637F')
poly(right,{{87,117},{97,127},{94,135},{91,126}},'5B637F')
for i,side in ipairs({'left','right'}) do
 local s=sprites[i];local im=i==1 and left or right
 s.cels[1].image=im
 s.layers[1].name='native-180'
 s:saveAs(root..'sprites/arctic-fox/side_'..side..'_v002.aseprite')
 app.command.SaveFileAs{ui=false,filename=out..'side_'..side..'_v002.png'}
 s:close()
end
print('PAIR_REFINED')
