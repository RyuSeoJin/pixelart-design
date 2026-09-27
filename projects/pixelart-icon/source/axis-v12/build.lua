-- CHANGELOG v1.0 · 2026-09-28 — 중심선에서 도구 7종을 재구성합니다.
local root=app.fs.joinPath(app.fs.currentPath,"projects/pixelart-icon")
local source=root.."/source/axis-v12"
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
-- 자루는 x-y=5, 결합부 (11,6), 노출 끝 (13,8)로 한 직선입니다.
box(im,3,10,11,5,wood);rect(im,4,11,9,2,col("E5B875"));rect(im,6,13,1,1,col("966039"))
shaft(im,{7,2},{13,8},wood)
polygon(im,{{11,4},{14,7},{11,11},{7,11},{7,8}},steel)
segment(im,{8,9},{10,7},0,light)
-- 결합부를 통과한 자루 끝은 같은 축에서 노출됩니다.
rect(im,12,7,3,3,D);im:drawPixel(13,8,wood)
-- 절삭 날의 하단을 나무 앞면에 가립니다.
rect(im,7,11,3,1,steel);rect(im,7,12,4,1,D);rect(im,8,12,3,1,wood)
add("act_chop",im,{7,2},{11,6},{13,8})
im=Image(16,16,ColorMode.RGB)
shaft(im,{3,13},{11,5},wood)
-- 곡괭이 날은 결합부를 중심으로 대칭인 45도 직선, 끝만 기능상 좁아집니다.
shaft(im,{6,2},{13,9},steel);im:drawPixel(10,6,light)
add("act_mine",im,{3,13},{10,6},{11,5},"날 양끝의 테이퍼")
im=Image(16,16,ColorMode.RGB)
shaft(im,{3,13},{12,4},steel);segment(im,{3,13},{5,11},0,wood)
shaft(im,{4,8},{8,12},col("EDB547"));segment(im,{7,9},{12,4},0,light)
add("order_blacksmith",im,{3,13},{6,10},{12,4},"검 끝은 같은 축에서 좁아집니다.")
im=Image(16,16,ColorMode.RGB)
box(im,2,3,11,12,col("FFF0CD"))
shaft(im,{4,12},{12,4},col("EDB547"));im:drawPixel(4,12,D);im:drawPixel(11,5,light)
add("icon_write",im,{4,12},{8,8},{12,4},"종이와 연필은 서로 다른 물체입니다.")
im=Image(16,16,ColorMode.RGB)
shaft(im,{3,13},{11,5},wood);segment(im,{6,10},{11,5},0,col("60BDA9"))
-- 낚싯대는 직선, 줄과 바늘만 부품 예외입니다.
segment(im,{12,5},{12,11},0,D);im:drawPixel(11,12,D);im:drawPixel(10,11,D)
add("act_fish",im,{3,13},{7,9},{11,5},"낚싯줄은 수직으로 내려가고 바늘 끝은 굽습니다.")
im=Image(16,16,ColorMode.RGB)
box(im,1,5,5,7,wood);rect(im,2,7,2,3,0)
box(im,5,5,10,5,steel);rect(im,6,6,7,1,light)
for x=6,12,2 do im:drawPixel(x,10,D) end
add("act_saw",im,{3,7},{5,7},{13,7},"톱니와 손잡이 구멍은 기능상 비대칭입니다.")
im=Image(16,16,ColorMode.RGB)
polygon(im,{{2,10},{6,6},{11,11},{7,14},{2,14}},col("4F91CF"))
shaft(im,{3,3},{12,12},col("EDB547"))
for i=1,7,2 do im:drawPixel(3+i,2+i,D) end
add("act_measure",im,{3,3},{8,8},{12,12},"천은 유연한 물체이며 눈금은 자의 내부 표시입니다.")
local function save(im,p) local s=Sprite(im.width,im.height,ColorMode.RGB);s.cels[1].image=im;s:saveAs(p);s:close() end
app.fs.makeAllDirectories(root.."/sprites/axis-v12")
for id,img in pairs(images) do
 local folder=root.."/export/"..id.."/v12";app.fs.makeAllDirectories(folder)
 save(img,source.."/"..id.."-native-16.png");save(img,root.."/sprites/axis-v12/"..id..".aseprite")
 for n=1,4 do local out=Image(n*16,n*16,ColorMode.RGB);for y=0,out.height-1 do for x=0,out.width-1 do out:drawPixel(x,y,img:getPixel(math.floor(x/n),math.floor(y/n))) end end;save(out,folder.."/icon-"..16*n..".png") end
end
local f=assert(io.open(source.."/axes.json","w"));f:write(json.encode(axes));f:close()
print("기준축을 공유하는 도구 7종 출력 완료")
