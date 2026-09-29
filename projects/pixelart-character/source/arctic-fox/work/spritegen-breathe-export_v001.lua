-- CHANGELOG v1.0 · 2026-09-29 — sprite-gen 호흡 아틀라스의 원본 픽셀 그대로 내보내기
local root='P:/github-repository/pixelart-design/projects/pixelart-character/'
local base=root..'source/arctic-fox/'
local opened=app.open(base..'work/spritegen-breathe-run/sprite-sheet-alpha.png')
local atlas=Image(opened.spec);atlas:drawSprite(opened,1);opened:close()
local all={}
local function save(im,path)
 local s=Sprite(im.width,im.height,ColorMode.RGB);s.cels[1].image=im;app.activeSprite=s;s:saveAs(path);s:close()
end
for row,side in ipairs({'left','right'}) do
 local s=Sprite(180,180,ColorMode.RGB);s.layers[1].name='sprite_gen_breathe';all[side]={}
 local strip=Image(1080,180,ColorMode.RGB)
 for i=0,5 do
  local im=Image(180,180,ColorMode.RGB);im:drawImage(atlas,Point(-i*180,-(row-1)*180))
  all[side][i+1]=im;strip:drawImage(im,Point(i*180,0))
  if i>0 then s:newEmptyFrame() end
  s.frames[i+1].duration=0.25;s:newCel(s.layers[1],i+1,im,Point(0,0))
  save(im,base..'image-undecided/180/anim-idle/'..side..string.format('/frame-%02d_v004.png',i))
 end
 local tag=s:newTag(1,6);tag.name='idle';tag.aniDir=AniDir.FORWARD
 app.activeSprite=s;s:saveAs(root..'sprites/arctic-fox/idle_'..side..'_v004.aseprite');s:close()
 save(strip,base..'image-undecided/180/anim-idle/'..side..'/sheet_v004.png')
end
local s=Sprite(1080,540,ColorMode.RGB)
for i=1,6 do
 local im=Image(1080,540,ColorMode.RGB)
 for y=0,539 do for x=0,1079 do
  local v=(math.floor(x/18)+math.floor(y/18))%2==0 and 220 or 236
  im:drawPixel(x,y,app.pixelColor.rgba(v,v,v,255))
 end end
 for n,side in ipairs({'left','right'}) do
  for y=0,179 do for x=0,179 do
   local c=all[side][i]:getPixel(x,y)
   if app.pixelColor.rgbaA(c)>0 then
    for yy=0,2 do for xx=0,2 do im:drawPixel((n-1)*540+x*3+xx,y*3+yy,c) end end
   end
  end end
 end
 if i>1 then s:newEmptyFrame() end
 s.frames[i].duration=0.25;s:newCel(s.layers[1],i,im,Point(0,0))
end
app.activeSprite=s;app.command.SaveFileAs{ui=false,filename=base..'work/spritegen-breathe-preview_v001.gif'};s:close()
print('SPRITE_GEN_BREATHE_EXPORT_COMPLETE')
