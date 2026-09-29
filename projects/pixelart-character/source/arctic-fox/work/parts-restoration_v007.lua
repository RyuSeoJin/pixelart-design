-- CHANGELOG v1.0 · 2026-09-29 — 양쪽 손 경계 외곽선 연결
local root='P:/github-repository/pixelart-design/projects/pixelart-character/'
local base=root..'source/arctic-fox/'
local pc=app.pixelColor
local function color(r,g,b) return pc.rgba(r,g,b,255) end
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
 local input=app.open(base..'image-undecided/180/view/side_'..side..'_v008.png')
 local im=Image(input.spec);im:drawSprite(input,1);input:close()
 local function put(u,y,c) local x=n==1 and u or 179-u;assert(pc.rgbaA(im:getPixel(x,y))==255);im:drawPixel(x,y,c) end
 local outlinePoints={{95,99},{98,99},{93,100},{98,100},{93,101},{99,101},{93,102},{99,102},{92,103},{99,103},{92,104},{99,104},{91,105},{99,105},{91,106},{99,106},{91,107},{99,107},{92,108},{93,108},{99,108},{98,109},{97,110},{93,111},{95,111},{94,112}}
 outlinePoints[#outlinePoints+1]={side=='left' and 92 or 93,109}
 outlinePoints[#outlinePoints+1]={side=='left' and 92 or 93,110}
 local handEdge={}
 for _,pt in ipairs(outlinePoints) do put(pt[1],pt[2],color(64,64,104));handEdge[pt[1]..','..pt[2]]=true end
 save(im,base..'image-undecided/180/view/side_'..side..'_v009.png')
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
  if handEdge[u..','..y] then name='hand_near' end
  parts[name]:drawPixel(x,y,c)
 end end end
 local s=Sprite(180,180,ColorMode.RGB);local recombined=Image(180,180,ColorMode.RGB)
 for i,name in ipairs(names) do
  local l=i==1 and s.layers[1] or s:newLayer();l.name=name;s:newCel(l,1,parts[name],Point(0,0));recombined:drawImage(parts[name],Point(0,0))
 end
 local hidden=s:newLayer();hidden.name='hidden_restoration_PENDING';hidden.isVisible=false
 s:saveAs(root..'sprites/arctic-fox/parts_'..side..'_v008.aseprite');s:close()
 for _,name in ipairs(names) do save(parts[name],folder..name..'_v007.png') end
 save(recombined,folder..'recombined_v007.png')
 local difference=Image(180,180,ColorMode.RGB);local mismatches=0
 for y=0,179 do for x=0,179 do if im:getPixel(x,y)~=recombined:getPixel(x,y) then mismatches=mismatches+1;difference:drawPixel(x,y,color(255,30,30)) end end end
 save(difference,folder..'difference_v007.png')
 assert(mismatches==0,'재합성 픽셀 불일치')
 for y=0,179 do for x=0,179 do local c=im:getPixel(x,y);if pc.rgbaA(c)>0 then
 for yy=0,2 do for xx=0,2 do overview:drawPixel((n-1)*540+x*3+xx,y*3+yy,c) end end end end end
end
save(overview,base..'work/parts-restoration-comparison_v007.png')
print('PARTITION_RECOMPOSITION_MATCHES_BOTH_DIRECTIONS')
