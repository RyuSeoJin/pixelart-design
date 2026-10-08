-- CHANGELOG v1.0 · 2026-10-08 — 낮판 알파를 보존한 새벽·저녁 색상판을 저장합니다.
local root='P:/github-repository/pixelart-design/projects/pixelart-background/source/landscape-v015/'
local pkg=root..'unreal-full/';local pc=app.pixelColor
local function save(im,path)local s=Sprite(im.width,im.height,ColorMode.RGB);s.cels[1].image=im;s:saveAs(path);s:close() end
local function lerp(a,b,t)return a+(b-a)*t end
local function byte(v)return math.max(0,math.min(255,math.floor(v+.5))) end
for _,a in ipairs(dofile(root..'assets.lua')) do
 if a.phase=='dawn' or a.phase=='dusk' then
  local day=Image{fromFile=pkg..a.file:gsub('_Dawn','_Day'):gsub('_Dusk','_Day')}
  local out=Image(day.width,day.height,ColorMode.RGB);local dawn=a.phase=='dawn'
  for y=0,day.height-1 do for x=0,day.width-1 do
   local p=day:getPixel(x,y);local alpha=pc.rgbaA(p)
   if alpha>0 then
    local r,g,b=pc.rgbaR(p),pc.rgbaG(p),pc.rgbaB(p)
    if a.layer=='sky' then
     local top=dawn and {43,57,102} or {67,42,93};local middle=dawn and {112,120,162} or {151,84,125};local bottom=dawn and {212,171,165} or {236,160,102}
     local t=math.min(1,y/832);local c1,c2,u
     if t<.65 then c1,c2,u=top,middle,t/.65 else c1,c2,u=middle,bottom,(t-.65)/.35 end
     r,g,b=lerp(c1[1],c2[1],u),lerp(c1[2],c2[2],u),lerp(c1[3],c2[3],u)
     r,g,b=math.floor(r/2)*2,math.floor(g/2)*2,math.floor(b/2)*2
    elseif a.layer=='clouds' or a.layer=='clouds_high' then
     local l=(r*.2126+g*.7152+b*.0722)/255
     local lo=dawn and {102,111,158} or {151,76,128};local hi=dawn and {233,185,183} or {255,183,115}
     r,g,b=lerp(lo[1],hi[1],l),lerp(lo[2],hi[2],l),lerp(lo[3],hi[3],l)
    else
     local l=(r*.2126+g*.7152+b*.0722)/255
     if dawn then r,g,b=r*.68+10,g*.73+12,b*.82+24
     else r,g,b=r*.79+20+l*9,g*.60+12+l*9,b*.76+22-l*4 end
     local fog=a.layer=='mountains_far' and .23 or (a.layer=='mountains_near' and .10 or 0)
     local tint=dawn and {151,158,184} or {177,120,151}
     r,g,b=lerp(r,tint[1],fog),lerp(g,tint[2],fog),lerp(b,tint[3],fog)
     if a.layer=='street_tile' then
      local q=day:getPixel(x,y);r,g,b=lerp(r,pc.rgbaR(q),.35),lerp(g,pc.rgbaG(q),.35),lerp(b,pc.rgbaB(q),.35)
     end
    end
    out:drawPixel(x,y,pc.rgba(byte(r),byte(g),byte(b),alpha))
   end
  end end
  save(out,pkg..a.file)
 end
end
print('새벽·저녁 색상판40개 저장 완료')
