-- CHANGELOG v1.0 · 2026-09-29 — 단일 전신 프레임의 윤곽·천 주름 직접 수정 idle
local root='P:/github-repository/pixelart-design/projects/pixelart-character/'
local base=root..'source/arctic-fox/'
local pc=app.pixelColor
local ms={260,200,260,200}
local function read(path)
 local s=app.open(path);local im=Image(s.spec);im:drawSprite(s,1);s:close();return im
end
local function save(im,path)
 local s=Sprite(im.width,im.height,ColorMode.RGB);s.cels[1].image=im;app.activeSprite=s;s:saveAs(path);s:close()
end
local all={}
for _,side in ipairs({'left','right'}) do
 local source=read(base..'image-confirmed/180/view/side_'..side..'_v010.png')
 local function sx(u) return side=='left' and u or 179-u end
 local function get(u,y) return source:getPixel(sx(u),y) end
 local dir=base..'image-undecided/180/anim-idle/'..side..'/'
 local s=Sprite(180,180,ColorMode.RGB);s.layers[1].name='full_frame'
 local sheet=Image(720,180,ColorMode.RGB);all[side]={}
 for f=1,4 do
  local im=Image(source)
  local function put(u,y,c) im:drawPixel(sx(u),y,c) end
  -- 파츠를 이동하지 않고 해당 프레임의 바깥선과 바로 안쪽 색면만 다시 찍습니다.
  local function edge(y0,y1,lo,hi,outward)
   for y=y0,y1 do
    local boundary=nil
    if outward<0 then
     for u=lo,hi do if pc.rgbaA(get(u,y))>0 then boundary=u;break end end
    else
     for u=hi,lo,-1 do if pc.rgbaA(get(u,y))>0 then boundary=u;break end end
    end
    if boundary then
     local line=get(boundary,y);local fill=get(boundary-outward,y)
     for step=1,3 do
      local sample=get(boundary-outward*step,y)
      if pc.rgbaA(sample)>0 and pc.rgbaR(sample)>150 then fill=sample;break end
     end
     put(boundary+outward,y,line);put(boundary,y,fill)
    end
   end
  end
  if f==2 then
   edge(67,75,74,87,-1)
  elseif f==3 then
   edge(65,80,74,87,-1)
   edge(80,88,100,111,1)
  end
  -- 소매 안쪽 접힘의 밝은 면을 두 단계로 바꿔 호흡에 따른 천의 긴장을 표현합니다.
  if f==2 or f==3 then
   for y=73,78 do
    local u=89
    if pc.rgbaR(get(u,y))>150 and pc.rgbaR(get(u+1,y))>150 then put(u,y,get(u+1,y)) end
   end
  end
  -- 꼬리 뒤쪽 털과 뒷머리 끝은 가슴 변화보다 한 프레임 늦게 반응합니다.
  if f==3 then edge(135,146,118,145,1) end
  if f==4 then edge(130,151,118,145,1);edge(47,50,104,115,1) end
  if f>1 then s:newEmptyFrame() end
  s.frames[f].duration=ms[f]/1000;s:newCel(s.layers[1],f,im,Point(0,0))
  all[side][f]=im;sheet:drawImage(im,Point((f-1)*180,0))
  save(im,dir..string.format('frame-%02d_v003.png',f-1))
 end
 local tag=s:newTag(1,4);tag.name='idle';tag.aniDir=AniDir.FORWARD
 app.activeSprite=s;s:saveAs(root..'sprites/arctic-fox/idle_'..side..'_v003.aseprite')
 app.command.SaveFileAs{ui=false,filename=dir..'preview_v003.gif'};s:close()
 save(sheet,dir..'sheet_v003.png')
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
app.activeSprite=preview;app.command.SaveFileAs{ui=false,filename=base..'work/idle-fullframe-preview_v001.gif'};preview:close()
save(contact,base..'work/idle-fullframe-contact_v001.png')
print('IDLE_4_FRAMES_BOTH_DIRECTIONS_EXPORTED')
