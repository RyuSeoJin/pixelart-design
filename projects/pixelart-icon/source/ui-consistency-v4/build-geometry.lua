-- CHANGELOG v1.0 · 2026-09-27 — 메뉴의 16px 도트와 기호의 크기별 도형 렌더링
local root=app.fs.joinPath(app.fs.currentPath,"projects/pixelart-icon")
local source=app.fs.joinPath(root,"source/ui-consistency-v4")
local function read(p) local f=assert(io.open(p,"r"));local v=json.decode(f:read("*a"));f:close();return v end
local design=read(app.fs.joinPath(source,"design.json"))
local rgba=app.pixelColor.rgba
local function color(h) return rgba(tonumber(h:sub(1,2),16),tonumber(h:sub(3,4),16),tonumber(h:sub(5,6),16),255) end
local function save(im,p) local s=Sprite(im.width,im.height,ColorMode.RGB);s.cels[1].image=im;s:saveAs(p);s:close() end
local function distance(x,y,a,b)
 local dx,dy=b[1]-a[1],b[2]-a[2]
 local t=math.max(0,math.min(1,((x-a[1])*dx+(y-a[2])*dy)/(dx*dx+dy*dy)))
 return math.sqrt((x-a[1]-t*dx)^2+(y-a[2]-t*dy)^2)
end
local function contains(x,y,points)
 local inside=false;local dist=math.huge;local j=#points
 for i=1,#points do
  local a,b=points[i],points[j]
  if (a[2]>y)~=(b[2]>y) and x<(b[1]-a[1])*(y-a[2])/(b[2]-a[2])+a[1] then inside=not inside end
  dist=math.min(dist,distance(x,y,a,b));j=i
 end
 return inside,dist
end
local function render(a,size)
 local im=Image(size,size,ColorMode.RGB)
 for y=0,size-1 do for x=0,size-1 do
  local px,py=(x+.5)*32/size,(y+.5)*32/size
  for _,s in ipairs(a.shapes) do
   local inside,dist=contains(px,py,s.points);local half=s.stroke/2
   if dist<=half and half>0 then im:drawPixel(x,y,color(s.outline))
   elseif inside then im:drawPixel(x,y,color(py<16 and s.highlight or s.fill)) end
  end
 end end
 return im
end
local function nearest(im,size)
 local out=Image(size,size,ColorMode.RGB);local n=size/im.width
 for y=0,size-1 do for x=0,size-1 do out:drawPixel(x,y,im:getPixel(math.floor(x/n),math.floor(y/n))) end end
 return out
end
app.fs.makeAllDirectories(app.fs.joinPath(root,"sprites/ui-consistency-v4"))
for _,a in ipairs(design.assets) do
 local folder=app.fs.joinPath(root,"export/"..a.id.."/v4");app.fs.makeAllDirectories(folder)
 local native=render(a,16)
 for _,size in ipairs({16,32,48,64}) do
  local im=a.render_mode=="pixel_native_16" and nearest(native,size) or render(a,size)
  save(im,app.fs.joinPath(folder,"icon-"..size..".png"))
  if size==16 or (size==32 and a.render_mode=="geometry_per_size") then
   save(im,app.fs.joinPath(root,"sprites/ui-consistency-v4/"..a.id.."-"..size..".aseprite"))
  end
 end
 if a.render_mode=="pixel_native_16" then save(native,app.fs.joinPath(source,a.id.."-native-16.png")) end
end
print("방향 기호 7종 v4: PNG 28개 생성 완료")
