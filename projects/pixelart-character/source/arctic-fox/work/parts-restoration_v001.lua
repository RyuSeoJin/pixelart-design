-- CHANGELOG v1.0 · 2026-09-28 — 사용자 지정 원본의 공통 배율 복원과 무손실 파츠 분리
local root='P:/github-repository/pixelart-design/projects/pixelart-character/'
local base=root..'source/arctic-fox/'
local pc=app.pixelColor
local srcSprite=app.open(base..'work/design-restoration-reference_v001.png')
local src=Image(srcSprite.spec);src:drawSprite(srcSprite,1);srcSprite:close()
local function valid(c)
 local r,g,b,a=pc.rgbaR(c),pc.rgbaG(c),pc.rgbaB(c),pc.rgbaA(c)
 return a>=220 and not (b>150 and b>r*1.6 and g<100)
end
local function color(r,g,b) return pc.rgba(math.max(10,r),math.max(10,g),math.max(10,b),255) end
local histogram={}
for y=0,886 do for x=0,1773 do local c=src:getPixel(x,y);if valid(c) then
 local r=math.min(255,math.floor(pc.rgbaR(c)/8+0.5)*8)
 local g=math.min(255,math.floor(pc.rgbaG(c)/8+0.5)*8)
 local b=math.min(255,math.floor(pc.rgbaB(c)/8+0.5)*8)
 local q=color(r,g,b);histogram[q]=(histogram[q] or 0)+1
end end end
local ranked={};for c,n in pairs(histogram) do ranked[#ranked+1]={c=c,n=n} end
table.sort(ranked,function(a,b) if a.n==b.n then return a.c<b.c end;return a.n>b.n end)
local palette={};for i=1,48 do palette[#palette+1]=ranked[i].c end
for _,rgb in ipairs({{246,210,188},{226,168,149},{184,117,116},{122,74,88},{127,208,224},{62,143,184},{42,79,128},{34,26,38}}) do palette[#palette+1]=color(table.unpack(rgb)) end
local function quant(c)
 local r,g,b=pc.rgbaR(c),pc.rgbaG(c),pc.rgbaB(c);local best,dist=palette[1],1e30
 for _,p in ipairs(palette) do local rr,gg,bb=pc.rgbaR(p),pc.rgbaG(p),pc.rgbaB(p)
 local v=(r-rr)^2+(g-gg)^2+(b-bb)^2
 if (r>g+10 and r>b+10)~=(rr>gg+10 and rr>bb+10) then v=v+2000 end
 if v<dist then dist=v;best=p end end
 return best
end
local scale=156/862
local function save(im,path)
 local s=Sprite(im.width,im.height,ColorMode.RGB);s.cels[1].image=im;app.command.SaveFileAs{ui=false,filename=path};s:close()
end
local function inside(x,y,poly)
 local hit=false;local j=#poly
 for i=1,#poly do local a,b=poly[i],poly[j]
 if (a[2]>y)~=(b[2]>y) and x<(b[1]-a[1])*(y-a[2])/(b[2]-a[2])+a[1] then hit=not hit end;j=i end
 return hit
end
local overview=Image(1080,540,ColorMode.RGB)
for y=0,539 do for x=0,1079 do local v=(math.floor(x/18)+math.floor(y/18))%2==0 and 228 or 242;overview:drawPixel(x,y,color(v,v,v)) end end
for n,side in ipairs({'left','right'}) do
 local foot=n==1 and 559.45765 or 1214.36783
 local im=Image(180,180,ColorMode.RGB)
 for y=0,179 do for x=0,179 do
  local sx=math.floor(foot+(x-90)/scale+0.5);local sy=math.floor(876+(y-170)/scale+0.5)
  if sx>=(n-1)*887 and sx<n*887 and sy>=0 and sy<887 then local c=src:getPixel(sx,sy);if valid(c) then im:drawPixel(x,y,quant(c)) end end
 end end
 save(im,base..'image-undecided/180/view/side_'..side..'_v003.png')
 local folder=base..'work/parts-'..side..'/'
 app.fs.makeAllDirectories(folder)
 local names={'tail','foot_near','shin_near','thigh_near','torso_hood','head','sleeve_near','hand_near'}
 local parts={};for _,name in ipairs(names) do parts[name]=Image(180,180,ColorMode.RGB) end
 for y=0,179 do for x=0,179 do local c=im:getPixel(x,y);if pc.rgbaA(c)>0 then
  local u=n==1 and x or 179-x;local name='torso_hood'
  if y<=55 then name='head'
  elseif y>=99 and u>=102 then name='tail'
  elseif y>=146 then name='foot_near'
  elseif y>=132 then name='shin_near'
  elseif y>=111 then name='thigh_near'
  elseif inside(u,y,{{91,102},{102,100},{102,109},{95,113},{91,109}}) then name='hand_near'
  elseif inside(u,y,{{88,61},{98,65},{103,84},{110,98},{102,103},{88,108},{87,94}}) then name='sleeve_near' end
  parts[name]:drawPixel(x,y,c)
 end end end
 local s=Sprite(180,180,ColorMode.RGB);local recombined=Image(180,180,ColorMode.RGB)
 for i,name in ipairs(names) do
  local l=i==1 and s.layers[1] or s:newLayer();l.name=name;s:newCel(l,1,parts[name],Point(0,0));recombined:drawImage(parts[name],Point(0,0))
 end
 local hidden=s:newLayer();hidden.name='hidden_restoration_PENDING';hidden.isVisible=false
 s:saveAs(root..'sprites/arctic-fox/parts_'..side..'_v002.aseprite');s:close()
 for _,name in ipairs(names) do save(parts[name],folder..name..'_v001.png') end
 save(recombined,folder..'recombined_v001.png')
 local difference=Image(180,180,ColorMode.RGB);local mismatches=0
 for y=0,179 do for x=0,179 do if im:getPixel(x,y)~=recombined:getPixel(x,y) then mismatches=mismatches+1;difference:drawPixel(x,y,color(255,30,30)) end end end
 save(difference,folder..'difference_v001.png')
 assert(mismatches==0,'재합성 픽셀 불일치')
 for y=0,179 do for x=0,179 do local c=im:getPixel(x,y);if pc.rgbaA(c)>0 then
 for yy=0,2 do for xx=0,2 do overview:drawPixel((n-1)*540+x*3+xx,y*3+yy,c) end end end end end
end
save(overview,base..'work/parts-restoration-comparison_v001.png')
print('PARTITION_RECOMPOSITION_MATCHES_BOTH_DIRECTIONS')
