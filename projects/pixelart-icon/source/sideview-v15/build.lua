-- CHANGELOG v1.0 · 2026-09-28 — 사이드뷰 도끼·곡괭이와 금속 내부 면
local root=app.fs.joinPath(app.fs.currentPath,"projects/pixelart-icon")
local source=root.."/source/sideview-v15"
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
-- 옆에서 본 도끼: 수평 자루와 아래쪽 한 날, 평평한 그루터기 앞면입니다.
box(im,6,10,9,5,wood)
rect(im,7,11,7,1,col("E5B875"));rect(im,9,13,1,1,col("966039"))
shaft(im,{2,5},{12,5},wood)
rect(im,9,3,3,6,steel)
rect(im,8,7,5,3,steel)
rect(im,7,9,7,2,steel)
rect(im,9,6,1,3,light);rect(im,8,9,4,1,light)
-- 같은 수평축의 노출 나무 끝을 금속 바깥으로 한 칸 드러냅니다.
rect(im,11,4,3,3,D);im:drawPixel(12,5,wood)
-- 나무 앞면이 절삭 날 하단 일부를 가립니다.
rect(im,7,11,7,1,D);rect(im,9,11,5,1,col("E5B875"))
add("act_chop",im,{2,5},{10,5},{12,5})
im=Image(16,16,ColorMode.RGB)
shaft(im,{7,13},{7,2},wood)
-- 양 날은 x=7 반사 대칭이며 내부 금속 면을 확보한 뒤 끝만 좁힙니다.
local spans={{3,4,10},{4,2,12},{5,2,12},{6,1,5},{6,9,13},{7,1,3},{7,11,13},{8,1,1},{8,13,13}}
for _,r in ipairs(spans) do rect(im,r[2],r[1],r[3]-r[2]+1,1,steel) end
rect(im,4,4,7,1,light)
im:drawPixel(7,2,wood)
add("act_mine",im,{7,13},{7,4},{7,2},"곡괭이 양 날만 아래로 굽고 끝이 좁아집니다. 자루는 수직입니다.")
local function save(im,p) local s=Sprite(im.width,im.height,ColorMode.RGB);s.cels[1].image=im;s:saveAs(p);s:close() end
app.fs.makeAllDirectories(root.."/sprites/sideview-v15")
for id,img in pairs(images) do
 local folder=root.."/export/"..id.."/v15";app.fs.makeAllDirectories(folder)
 save(img,source.."/"..id.."-native-16.png");save(img,root.."/sprites/sideview-v15/"..id..".aseprite")
 for n=1,4 do local out=Image(n*16,n*16,ColorMode.RGB);for y=0,out.height-1 do for x=0,out.width-1 do out:drawPixel(x,y,img:getPixel(math.floor(x/n),math.floor(y/n))) end end;save(out,folder.."/icon-"..16*n..".png") end
end
local f=assert(io.open(source.."/axes.json","w"));f:write(json.encode(axes));f:close()
print("기준축을 공유하는 도구 2종 출력 완료")
