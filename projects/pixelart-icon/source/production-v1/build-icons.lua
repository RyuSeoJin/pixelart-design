-- CHANGELOG v1.0 · 2026-09-27 — 나머지 60종의 실제 16px 정리와 네 출력 생성
-- 실행 위치는 저장소 루트입니다. 이미 승인된 대표 6종에는 쓰지 않습니다.
local root=app.fs.joinPath(app.fs.currentPath,"projects/pixelart-icon")
local source=app.fs.joinPath(root,"source/production-v1")
local function read(path) local f=assert(io.open(path,"r"));local s=f:read("*a");f:close();return json.decode(s) end
local plan=read(app.fs.joinPath(source,"generation.json"))
local rgba=app.pixelColor.rgba
local red,green,blue,alpha=app.pixelColor.rgbaR,app.pixelColor.rgbaG,app.pixelColor.rgbaB,app.pixelColor.rgbaA
local function color(h) return rgba(tonumber(h:sub(1,2),16),tonumber(h:sub(3,4),16),tonumber(h:sub(5,6),16),255) end
local function nearest(c,pal)
 local best,dist=pal[1],math.huge
 for _,v in ipairs(pal) do
  local d=(red(c)-red(v))^2+(green(c)-green(v))^2+(blue(c)-blue(v))^2
  if d<dist then best,dist=v,d end
 end
 return best
end
local function scale(im,n)
 local out=Image(16*n,16*n,ColorMode.RGB)
 for y=0,out.height-1 do for x=0,out.width-1 do out:drawPixel(x,y,im:getPixel(math.floor(x/n),math.floor(y/n))) end end
 return out
end
local function save(im,path)
 local s=Sprite(im.width,im.height,ColorMode.RGB);s.cels[1].image=im;s:saveAs(path);s:close()
end
local report={revision="1.0",method="Aseprite에서 알파 범위의 블록별 색상 투표·팔레트 정리 후 16px 원본 생성; 출력은 최근접 정수배",assets={},pending={}}
app.fs.makeAllDirectories(app.fs.joinPath(root,"sprites/production-v1"))
local overrides={}
local overridePath=app.fs.joinPath(source,"native-overrides.json")
if app.fs.isFile(overridePath) then overrides=read(overridePath).assets end
local facePath=app.fs.joinPath(source,"face-refinements.json")
local faceAdjustments=app.fs.isFile(facePath) and read(facePath).assets or {}
for _,a in ipairs(plan.assets) do
 local id=a.id
 local path=app.fs.joinPath(source,id.."-concept.png")
 if app.fs.isFile(path) then
  local s=assert(app.open(path));assert(s.colorMode==ColorMode.RGB)
  local raw=Image(s.width,s.height,ColorMode.RGB);raw:drawSprite(s,1)
  local minx,miny,maxx,maxy=raw.width,raw.height,-1,-1
  for y=0,raw.height-1 do for x=0,raw.width-1 do
   if alpha(raw:getPixel(x,y))>=240 then minx=math.min(minx,x);maxx=math.max(maxx,x);miny=math.min(miny,y);maxy=math.max(maxy,y) end
  end end
  assert(maxx>=minx,id)
  local w,h=maxx-minx+1,maxy-miny+1
  local dw=math.max(1,math.floor(14*w/math.max(w,h)+0.5));local dh=math.max(1,math.floor(14*h/math.max(w,h)+0.5))
  local ox,oy=math.floor((16-dw)/2),math.floor((16-dh)/2)
  local native=Image(16,16,ColorMode.RGB);local pal={};local paletteCopy={}
  -- JSON에서 읽은 배열은 userdata이므로 보고서에는 Lua 배열로 복사합니다.
  for _,v in ipairs(a.palette) do pal[#pal+1]=color(v);paletteCopy[#paletteCopy+1]=v end
  for y=0,dh-1 do for x=0,dw-1 do
   local votes,coverage={},0
   for sy=0,6 do for sx=0,6 do
    local rx=math.min(maxx,math.floor(minx+(x+(sx+0.5)/7)*w/dw))
    local ry=math.min(maxy,math.floor(miny+(y+(sy+0.5)/7)*h/dh))
    local c=raw:getPixel(rx,ry)
    if alpha(c)>=128 then coverage=coverage+1;local q=nearest(c,pal);votes[q]=(votes[q] or 0)+1 end
   end end
   if coverage>=25 then
    local best,n=pal[1],-1
    for _,q in ipairs(pal) do if (votes[q] or 0)>n then best,n=q,votes[q] or 0 end end
    native:drawPixel(ox+x,oy+y,best)
   end
  end end
  s:close()
  -- 시각 검수에서 지정한 보정은 16px 원본에만 반영합니다.
  local adjustment=faceAdjustments[id] or overrides[id]
  if adjustment then
   if adjustment.rows then
    native:clear()
    for y,row in ipairs(adjustment.rows) do for x=1,#row do
     local ch=row:sub(x,x)
     if ch~="." then native:drawPixel(x-1,y-1,color(adjustment.colors[ch])) end
    end end
   end
   for _,p in ipairs(adjustment.pixels or {}) do native:drawPixel(p[1],p[2],p[3]=="transparent" and 0 or color(p[3])) end
  end
  local folder=app.fs.joinPath(root,"export/"..id.."/v1");app.fs.makeAllDirectories(folder)
  save(native,app.fs.joinPath(root,"sprites/production-v1/"..id..".aseprite"))
  save(native,app.fs.joinPath(source,id.."-native-16.png"))
  for n=1,4 do save(scale(native,n),app.fs.joinPath(folder,"icon-"..(16*n)..".png")) end
  report.assets[#report.assets+1]={id=id,source_size={raw.width,raw.height},source_bounds={minx,miny,w,h},native_content_area={ox,oy,dw,dh},palette=paletteCopy,native_adjustment=adjustment and adjustment.reason or nil}
 else report.pending[#report.pending+1]=id end
end
local f=assert(io.open(app.fs.joinPath(source,"build-report.json"),"w"));f:write(json.encode(report));f:close()
print("16px 정리 완료: "..#report.assets.."종 / 생성 대기: "..#report.pending.."종")
