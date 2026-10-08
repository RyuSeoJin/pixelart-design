-- CHANGELOG v1.0 · 2026-10-08 — 4시간대·천체 궤도·별똥별을 같은 카메라로 합성합니다.
local root='P:/github-repository/pixelart-design/projects/pixelart-background/source/landscape-v015/'
local pkg=root..'unreal-full/';local pc=app.pixelColor
local function save(im,path)local s=Sprite(im.width,im.height,ColorMode.RGB);s.cels[1].image=im;s:saveAs(path);s:close() end
local cache={}
local function load(path)if not cache[path] then cache[path]=Image{fromFile=pkg..path} end;return cache[path] end
local function lerp(a,b,t)return math.floor(a+(b-a)*t+.5) end
local function mark(im,x,y,color)if x>=0 and y>=0 and x<im.width and y<im.height then im:drawPixel(x,y,color) end end
local pending={};for _,j in ipairs(dofile(root..'render-jobs.lua')) do if j.name:match('_fx_') then table.insert(pending,j) end end;for _,job in ipairs(pending) do
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
