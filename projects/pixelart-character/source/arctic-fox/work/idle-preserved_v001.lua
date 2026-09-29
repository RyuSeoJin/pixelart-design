-- CHANGELOG v1.0 · 2026-09-29 — v010 파츠 원형을 유지하는 좌우 호흡 idle
local root='P:/github-repository/pixelart-design/projects/pixelart-character/'
local base=root..'source/arctic-fox/'
local pc=app.pixelColor
local ms={260,200,260,200}
local bob={0,1,2,1}
local function read(path)
 local s=app.open(path);local im=Image(s.spec);im:drawSprite(s,1);s:close();return im
end
local function save(im,path)
 local s=Sprite(im.width,im.height,ColorMode.RGB);s.cels[1].image=im;app.activeSprite=s;s:saveAs(path);s:close()
end
local all={}
for _,side in ipairs({'left','right'}) do
 local names={'tail','foot_near','shin_near','thigh_near','torso_hood','head','sleeve_near','hand_near'}
 local parts={};for _,name in ipairs(names) do parts[name]=read(base..'work/parts-'..side..'/'..name..'_v008.png') end
 -- 손끝이 하체 파츠에 포함되지 않도록 실제 피부 픽셀의 소속을 복원합니다.
 local original=read(base..'image-undecided/180/view/side_'..side..'_v010.png')
 for y=98,112 do for u=90,100 do
  local x=side=='left' and u or 179-u;local c=original:getPixel(x,y)
  local r,g,b=pc.rgbaR(c),pc.rgbaG(c),pc.rgbaB(c)
  if pc.rgbaA(c)>0 and r>g+15 and r>b+15 then
   for _,name in ipairs(names) do parts[name]:drawPixel(x,y,pc.rgba(0,0,0,0)) end
   parts.hand_near:drawPixel(x,y,c)
  end
 end end
 -- 부츠 뒤쪽 외곽선이 꼬리 파츠에 섞여 아래로 움직이지 않게 합니다.
 for y=146,179 do for u=74,110 do
  local x=side=='left' and u or 179-u;local c=original:getPixel(x,y)
  if pc.rgbaA(c)>0 then
   for _,name in ipairs(names) do parts[name]:drawPixel(x,y,pc.rgba(0,0,0,0)) end
   parts.foot_near:drawPixel(x,y,c)
  end
 end end
 local partDir=base..'work/idle-parts-'..side..'/'
 app.fs.makeAllDirectories(partDir)
 for _,name in ipairs(names) do save(parts[name],partDir..name..'_v001.png') end
 local dir=base..'image-undecided/180/anim-idle/'..side..'/'
 app.fs.makeAllDirectories(dir)
 local s=Sprite(180,180,ColorMode.RGB)
 local layers={};for i,name in ipairs(names) do local l=i==1 and s.layers[1] or s:newLayer();l.name=name;layers[name]=l end
 local sheet=Image(720,180,ColorMode.RGB);all[side]={}
 for f=1,4 do
  if f>1 then s:newEmptyFrame() end
  s.frames[f].duration=ms[f]/1000
  for _,name in ipairs(names) do
   local dy=(name=='foot_near' or name=='shin_near' or name=='thigh_near') and 0 or bob[f]
   s:newCel(layers[name],f,parts[name],Point(0,dy))
  end
  local im=Image(180,180,ColorMode.RGB);im:drawSprite(s,f);all[side][f]=im
  sheet:drawImage(im,Point((f-1)*180,0))
  save(im,dir..string.format('frame-%02d_v002.png',f-1))
 end
 local tag=s:newTag(1,4);tag.name='idle';tag.aniDir=AniDir.FORWARD
 app.activeSprite=s;s:saveAs(root..'sprites/arctic-fox/idle_'..side..'_v002.aseprite')
 app.command.SaveFileAs{ui=false,filename=dir..'preview_v002.gif'};s:close()
 save(sheet,dir..'sheet_v002.png')
end
-- 미리보기만 3배로 확대하며 게임용 프레임은 180 격자를 유지합니다.
local preview=Sprite(1080,540,ColorMode.RGB)
local contact=Image(1440,720,ColorMode.RGB)
for f=1,4 do
 if f>1 then preview:newEmptyFrame() end
 preview.frames[f].duration=ms[f]/1000
 local im=Image(1080,540,ColorMode.RGB)
 for y=0,539 do for x=0,1079 do local v=(math.floor(x/18)+math.floor(y/18))%2==0 and 220 or 236;im:drawPixel(x,y,pc.rgba(v,v,v,255)) end end
 for n,side in ipairs({'left','right'}) do
  for y=0,179 do for x=0,179 do local c=all[side][f]:getPixel(x,y)
   for yy=0,1 do for xx=0,1 do
    local dstx=(f-1)*360+x*2+xx;local dsty=(n-1)*360+y*2+yy
    local bg=n==1 and pc.rgba(238,238,242,255) or pc.rgba(45,48,60,255)
    contact:drawPixel(dstx,dsty,pc.rgbaA(c)>0 and c or bg)
   end end
   if pc.rgbaA(c)>0 then for yy=0,2 do for xx=0,2 do im:drawPixel((n-1)*540+x*3+xx,y*3+yy,c) end end end
  end end
 end
 preview:newCel(preview.layers[1],f,im,Point(0,0))
end
app.activeSprite=preview;app.command.SaveFileAs{ui=false,filename=base..'work/idle-preserved-preview_v001.gif'};preview:close()
save(contact,base..'work/idle-preserved-contact_v001.png')
print('IDLE_4_FRAMES_BOTH_DIRECTIONS_EXPORTED')
