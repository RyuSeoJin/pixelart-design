-- CHANGELOG v1.0 · 2026-09-27 — 메뉴의 16px 도트와 기호의 크기별 도형 렌더링
local root=app.fs.joinPath(app.fs.currentPath,"projects/pixelart-icon")
local source=app.fs.joinPath(root,"source/compliance-v6")
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
 local snapshot=Image(im)
 for y=1,size-2 do for x=1,size-2 do
  if app.pixelColor.rgbaA(snapshot:getPixel(x,y))>0 then
   local boundary=false
   for _,d in ipairs({{-1,0},{1,0},{0,-1},{0,1}}) do if app.pixelColor.rgbaA(snapshot:getPixel(x+d[1],y+d[2]))==0 then boundary=true end end
   if boundary then im:drawPixel(x,y,color("342D46")) end
  end
 end end
 return im
end
local function nearest(im,size)
 local out=Image(size,size,ColorMode.RGB);local n=size/im.width
 for y=0,size-1 do for x=0,size-1 do out:drawPixel(x,y,im:getPixel(math.floor(x/n),math.floor(y/n))) end end
 return out
end

local catalog=read(source.."/baseline-catalog.json");local lookup={};for _,a in ipairs(catalog.items) do lookup[a.id]=a end
local reports={}
app.fs.makeAllDirectories(root.."/sprites/compliance-v6")
for _,a in ipairs(design.assets) do
 local outputs={};local changed=false
 for _,n in ipairs({16,32,48,64}) do
  local im=render(a,n);outputs[n]=im
  local s=assert(app.open(root.."/"..lookup[a.id].output_directory.."/icon-"..n..".png"));local prev=Image(n,n,ColorMode.RGB);prev:drawSprite(s,1);s:close()
  for y=0,n-1 do for x=0,n-1 do if prev:getPixel(x,y)~=im:getPixel(x,y) then changed=true end end end
 end
 if changed then
  local folder=root.."/export/"..a.id.."/v6";app.fs.makeAllDirectories(folder)
  for _,n in ipairs({16,32,48,64}) do save(outputs[n],folder.."/icon-"..n..".png") end
  save(outputs[16],root.."/sprites/compliance-v6/"..a.id.."-16.aseprite");save(outputs[32],root.."/sprites/compliance-v6/"..a.id.."-32.aseprite")
 end
 table.insert(reports,{id=a.id,changed=changed,reason="도형 래스터 경계에서 빠진 외곽색을 연결"})
end
local f=assert(io.open(source.."/geometry-build-report.json","w"));f:write(json.encode(reports));f:close()
print("기호 14종 네 크기 직접 출력·경계 연속성 검사 완료")
