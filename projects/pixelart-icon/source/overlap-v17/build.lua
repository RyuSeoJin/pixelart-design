-- CHANGELOG v1.0 · 2026-09-28 — 도끼와 그루터기의 개별 외곽선 및 겹침 경계
local root=app.fs.joinPath(app.fs.currentPath,"projects/pixelart-icon")
local source=root.."/source/overlap-v17"
local rgba=app.pixelColor.rgba;local alpha=app.pixelColor.rgbaA
local function col(h) return rgba(tonumber(h:sub(1,2),16),tonumber(h:sub(3,4),16),tonumber(h:sub(5,6),16),255) end
local D=col("342D46");local wood=col("BF8750");local steel=col("8B9BB0");local light=col("D0DCE6")
local function rect(im,x,y,w,h,c) for yy=y,y+h-1 do for xx=x,x+w-1 do im:drawPixel(xx,yy,c) end end end
local function box(im,x,y,w,h,c) rect(im,x,y,w,h,D);rect(im,x+1,y+1,w-2,h-2,c) end
local function segment(im,a,b,r,c)
 local dx,dy=b[1]-a[1],b[2]-a[2];local n=math.max(math.abs(dx),math.abs(dy))
 for i=0,n do local x=a[1]+dx*i/n;local y=a[2]+dy*i/n;rect(im,x-r,y-r,2*r+1,2*r+1,c) end
end
local function shaft(im,a,b,c) segment(im,a,b,1,D);segment(im,a,b,0,c) end
local function polygon(im,p,c)
 for y=1,14 do for x=1,14 do local hit=false;local j=#p
  for i=1,#p do local a,b=p[i],p[j];if (a[2]>y+.5)~=(b[2]>y+.5) and x+.5<(b[1]-a[1])*(y+.5-a[2])/(b[2]-a[2])+a[1] then hit=not hit end;j=i end
  if hit then im:drawPixel(x,y,c) end
 end end
end
local function outline(im)
 local src=Image(im)
 for y=1,14 do for x=1,14 do if alpha(src:getPixel(x,y))>0 then
  for _,q in ipairs({{-1,0},{1,0},{0,-1},{0,1}}) do if alpha(src:getPixel(x+q[1],y+q[2]))==0 then im:drawPixel(x,y,D);break end end
 end end end
end
local images,axes={},{}
local function add(id,im,a,j,b,exceptions)
 outline(im);images[id]=im;axes[id]={start=a,joint=j,finish=b,curve_exception=exceptions or "없음"}
end
local im=Image(16,16,ColorMode.RGB)
-- 45도 자루와 한쪽 날을 같은 옆모습 평면에 배치합니다.
box(im,3,10,11,5,wood)
rect(im,4,11,9,1,col("E5B875"));rect(im,6,13,1,1,col("966039"))
local stump=im
im=Image(16,16,ColorMode.RGB)
shaft(im,{2,2},{10,10},wood)
polygon(im,{{8,5},{12,9},{8,12},{4,11},{4,9}},steel)
segment(im,{5,9},{7,7},0,light)
rect(im,9,9,3,3,D);im:drawPixel(10,10,wood)
outline(im)
local axe=im
im=stump
for y=0,15 do for x=0,15 do local c=axe:getPixel(x,y);if alpha(c)>0 then im:drawPixel(x,y,c) end end end
-- 그루터기의 앞쪽 입구는 날 하단을 가리되 경계 한 줄을 유지합니다.
rect(im,4,12,9,1,wood)
add("act_chop",im,{2,2},{8,8},{10,10})
local function save(im,p) local s=Sprite(im.width,im.height,ColorMode.RGB);s.cels[1].image=im;s:saveAs(p);s:close() end
app.fs.makeAllDirectories(root.."/sprites/overlap-v17")
for id,img in pairs(images) do
 local folder=root.."/export/"..id.."/v17";app.fs.makeAllDirectories(folder)
 save(img,source.."/"..id.."-native-16.png");save(img,root.."/sprites/overlap-v17/"..id..".aseprite")
 for n=1,4 do local out=Image(n*16,n*16,ColorMode.RGB);for y=0,out.height-1 do for x=0,out.width-1 do out:drawPixel(x,y,img:getPixel(math.floor(x/n),math.floor(y/n))) end end;save(out,folder.."/icon-"..16*n..".png") end
end
local f=assert(io.open(source.."/axes.json","w"));f:write(json.encode(axes));f:close()
print("기준축을 공유하는 도구 2종 출력 완료")

local pair=Image(512,256,ColorMode.RGB);pair:clear(rgba(224,225,231,255))
for i,v in ipairs({"v16","v17"}) do
 local sp=app.open(root.."/export/act_chop/"..v.."/icon-16.png");local im=Image(16,16,ColorMode.RGB);im:drawSprite(sp,1);sp:close()
 for y=0,255 do for x=0,255 do local c=im:getPixel(math.floor(x/16),math.floor(y/16));if alpha(c)>0 then pair:drawPixel((i-1)*256+x,y,c) end end end
end
save(pair,root.."/export/collection-v17/axe-before-after.png")
