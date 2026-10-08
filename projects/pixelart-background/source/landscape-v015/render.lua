-- CHANGELOG v1.0 · 2026-10-08 — 4시간대·천체 궤도·별똥별을 같은 카메라로 합성합니다.
local root='P:/github-repository/pixelart-design/projects/pixelart-background/source/landscape-v015/'
local pkg=root..'unreal-full/';local pc=app.pixelColor
local function save(im,path)local s=Sprite(im.width,im.height,ColorMode.RGB);s.cels[1].image=im;s:saveAs(path);s:close() end
local cache={}
local function load(path)if not cache[path] then cache[path]=Image{fromFile=pkg..path} end;return cache[path] end
local function lerp(a,b,t)return math.floor(a+(b-a)*t+.5) end
local function mark(im,x,y,color)if x>=0 and y>=0 and x<im.width and y<im.height then im:drawPixel(x,y,color) end end
for _,job in ipairs(dofile(root..'render-jobs.lua')) do
 local out=Image(job.width,job.height,ColorMode.RGB)
 for _,item in ipairs(job.layers) do
  local src=load(item.file);local other=item.blend_file and load(item.blend_file)
  for _,rect in ipairs(item.rects) do
   local left,top=math.max(0,rect[1]),math.max(0,rect[2]);local right,bottom=math.min(job.width,rect[1]+rect[3]),math.min(job.height,rect[2]+rect[4])
   if right>left and bottom>top then
    local crop=Image(right-left,bottom-top,ColorMode.RGB)
    for y=top,bottom-1 do for x=left,right-1 do
     local sx,sy=(x-rect[1])*src.width//rect[3],(y-rect[2])*src.height//rect[4];local p=src:getPixel(sx,sy)
     if pc.rgbaA(p)>0 then
      local r,g,b=pc.rgbaR(p),pc.rgbaG(p),pc.rgbaB(p)
      if other then local q=other:getPixel(sx,sy);r,g,b=lerp(r,pc.rgbaR(q),item.mix),lerp(g,pc.rgbaG(q),item.mix),lerp(b,pc.rgbaB(q),item.mix) end
      if item.additive then local q=out:getPixel(x,y);r,g,b=math.min(255,r+pc.rgbaR(q)),math.min(255,g+pc.rgbaG(q)),math.min(255,b+pc.rgbaB(q)) end
      crop:drawPixel(x-left,y-top,pc.rgba(r,g,b,math.floor(pc.rgbaA(p)*item.opacity+.5)))
     end
    end end
    out:drawImage(crop,Point(left,top))
   end
  end
 end
 if job.orbit then
  for _,p in ipairs(job.orbit) do for dx=-1,1 do mark(out,p[1]+dx,p[2],pc.rgba(236,209,149,255)) end end
  for _,r in ipairs(job.body_rects) do
   for x=r[1],r[1]+r[3] do mark(out,x,r[2],pc.rgba(255,236,166,255));mark(out,x,r[2]+r[4],pc.rgba(255,236,166,255)) end
   for y=r[2],r[2]+r[4] do mark(out,r[1],y,pc.rgba(255,236,166,255));mark(out,r[1]+r[3],y,pc.rgba(255,236,166,255)) end
  end
 end
 save(out,pkg..'Preview/'..job.name)
end
local glyphs={['0']={'111','101','101','101','111'},['1']={'010','110','010','010','111'},['2']={'111','001','111','100','111'},['3']={'111','001','111','001','111'},['4']={'101','101','111','001','001'},['5']={'111','100','111','001','111'},['6']={'111','100','111','101','111'},['7']={'111','001','001','001','001'},['8']={'111','101','111','101','111'},['9']={'111','101','111','001','111'},[':']={'0','1','0','1','0'}}
local board=Image(12000,584,ColorMode.RGB)
for ri,region in ipairs({'forest','snow'}) do
 local row=Image(12000,292,ColorMode.RGB)
 for hour=4,28 do
  local im=load('Preview/'..region..'_timeline_'..string.format('%02d',hour)..'.png');local x=(hour-4)*480;row:drawImage(im,Point(x,22))
  local label=string.format('%02d:00',hour%24)
  for i=1,#label do local g=glyphs[label:sub(i,i)];for y,line in ipairs(g) do for xx=1,#line do if line:sub(xx,xx)=='1' then for dy=0,1 do for dx=0,1 do row:drawPixel(x+8+(i-1)*8+(xx-1)*2+dx,5+(y-1)*2+dy,pc.rgba(225,230,243,255)) end end end end end end
 end
 save(row,pkg..'Preview/'..region..'_daynight_timeline.png');board:drawImage(row,Point(0,(ri-1)*292))
end
save(board,pkg..'Preview/daynight_timeline.png')
for _,region in ipairs({'forest','snow'}) do
 local board=Image(1920,1080,ColorMode.RGB)
 for i,phase in ipairs({'dawn','day','dusk','night'}) do
  local src=load('Preview/'..region..'_'..phase..'_zoom_100.png');local im=Image(960,540,ColorMode.RGB)
  for y=0,539 do for x=0,959 do im:drawPixel(x,y,src:getPixel(x*2,y*2)) end end
  board:drawImage(im,Point(((i-1)%2)*960,((i-1)//2)*540))
 end
 save(board,pkg..'Preview/'..region..'_four_phases.png')
end
print('시간대·궤도·하루 흐름·효과 미리보기 저장 완료')
