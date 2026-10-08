-- CHANGELOG v1.0 · 2026-10-08 — GPT 천체·효과 원화를 실제 픽셀 격자와 팔레트로 정리합니다.
local root='P:/github-repository/pixelart-design/projects/pixelart-background/source/landscape-v015/'
local pkg=root..'unreal-full/';local pc=app.pixelColor
local function save(im,path)local s=Sprite(im.width,im.height,ColorMode.RGB);s.cels[1].image=im;s:saveAs(path);s:close() end
local blue={{58,88,148},{80,124,183},{108,159,208},{145,191,228},{185,220,242},{222,244,253},{250,254,255}}
local warm={{229,141,54},{249,174,66},{255,198,85},{255,219,115},{255,236,159},{255,247,201},{255,252,229}}
local moon={{114,161,213},{151,190,225},{184,216,239},{214,237,250},{239,250,255}}
local function closest(p,pal)
 local r,g,b=pc.rgbaR(p),pc.rgbaG(p),pc.rgbaB(p);local best,d=pal[1],1e12
 for _,c in ipairs(pal) do local v=(r-c[1])^2+(g-c[2])^2+(b-c[3])^2;if v<d then best,d=c,v end end
 return pc.rgba(best[1],best[2],best[3],255)
end
for _,s in ipairs({{'sun','Sun',48,48},{'moon','Moon',48,48},{'meteor','Meteor',24,6},{'meteor_big','MeteorBig',160,32},{'glow','MeteorGlow',64,64},{'spark','MeteorSpark',64,16}}) do
 local src=Image{fromFile=root..'input/'..s[1]..'.png'};local w,h=s[3],s[4];local im=Image(w,h,ColorMode.RGB)
 for y=0,h-1 do for x=0,w-1 do
  local sx,sy=(x+.5)*src.width/w,(y+.5)*src.height/h
  if s[1]=='sun' or s[1]=='moon' then
   local step=s[1]=='sun' and 800/28 or 605/24
   sx,sy=src.width/2+(x-23.5)*step,src.height/2+(y-23.5)*step
  end
  if sx>=0 and sy>=0 and sx<src.width and sy<src.height then
   local p=src:getPixel(math.floor(sx),math.floor(sy));local keep=pc.rgbaA(p)>=160
   -- 작은 효과는 셀 내부 표본을 더 살펴 가는 점이 축소 중 사라지지 않게 합니다.
   if s[1]=='meteor' or s[1]=='spark' then
    local best,score=0,-1
    for iy=0,4 do for ix=0,4 do
     local q=src:getPixel(math.min(src.width-1,math.floor((x+(ix+.5)/5)*src.width/w)),math.min(src.height-1,math.floor((y+(iy+.5)/5)*src.height/h)))
     local l=pc.rgbaR(q)+pc.rgbaG(q)+pc.rgbaB(q)
     if pc.rgbaA(q)>=160 and l>score then best,score=q,l end
    end end
    p=best;keep=score>=0
   end
   local noise=((x*37+y*71+x*y*13)%101)/100
   if s[1]=='meteor_big' then keep=keep and (x>w*.68 or noise<.3+.7*x/w) end
   if s[1]=='glow' then local r=math.sqrt((x-31.5)^2+(y-31.5)^2)/32;keep=keep and noise<math.max(.06,1-r*.85) end
   if keep then im:drawPixel(x,y,closest(p,s[1]=='sun' and warm or (s[1]=='moon' and moon or blue))) end
  end
 end end
 if s[1]=='spark' then
  for _,frame in ipairs({0,3}) do
   for y=0,15 do for x=frame*16,frame*16+15 do im:drawPixel(x,y,0) end end
   im:drawPixel(frame*16+8,8,frame==0 and pc.rgba(239,250,255,255) or pc.rgba(145,191,228,255))
  end
 end
 save(im,pkg..'Textures/T_'..s[2]..'.png')
end
-- 밝기를 기준으로 기존 별 픽셀을 서로 배타적인 세 층으로 나눕니다.
for _,region in ipairs({'Forest','Snow'}) do
 local src=Image{fromFile=root..'incoming/to_chatgpt/02_current_v014/Textures/T_'..region..'_Stars.png'}
 local ims={Image(src.width,src.height,ColorMode.RGB),Image(src.width,src.height,ColorMode.RGB),Image(src.width,src.height,ColorMode.RGB)}
 for y=0,src.height-1 do for x=0,src.width-1 do
  local p=src:getPixel(x,y)
  if pc.rgbaA(p)>0 then
   local l=pc.rgbaR(p)*.2126+pc.rgbaG(p)*.7152+pc.rgbaB(p)*.0722
   local index=l>=195.34486 and 1 or (l>=183.59965 and 2 or 3)
   ims[index]:drawPixel(x,y,p)
  end
 end end
 local n=0;math.randomseed(151015)
 while n<100 do
  local x,y=math.random(2,src.width-3),math.random(2,src.height-3)
  if pc.rgbaA(src:getPixel(x,y))==0 and pc.rgbaA(ims[3]:getPixel(x,y))==0 then
   ims[3]:drawPixel(x,y,pc.rgba(119,145,196,255));n=n+1
  end
 end
 for i,letter in ipairs({'A','B','C'}) do save(ims[i],pkg..'Textures/T_'..region..'_Stars'..letter..'.png') end
end
print('천체2장·효과4장·별6장 저장 완료')
