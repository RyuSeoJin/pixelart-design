-- CHANGELOG v1.0 · 2026-09-28 — 동작 확대 검수본
local root='P:/github-repository/pixelart-design/projects/pixelart-character/'
local work=root..'source/arctic-fox/work/'
local pc=app.pixelColor
for _,motion in ipairs({'idle','walk'}) do
 local count=motion=='idle' and 4 or 8
 local sheet=Sprite(360*count,720,ColorMode.RGB);local im=sheet.cels[1].image
 for y=0,719 do for x=0,360*count-1 do local v=(math.floor(x/20)+math.floor(y/20))%2==0 and 228 or 242;im:drawPixel(x,y,pc.rgba(v,v,v,255)) end end
 for d,side in ipairs({'left','right'}) do
  for f=0,count-1 do
   local s=app.open(root..'source/arctic-fox/image-undecided/180/anim-'..motion..'/'..side..string.format('/frame-%02d_v001.png',f))
   local src=Image(s.spec);src:drawSprite(s,1);s:close()
   for y=0,179 do for x=0,179 do local c=src:getPixel(x,y);if pc.rgbaA(c)>0 then
    for yy=0,1 do for xx=0,1 do im:drawPixel(f*360+x*2+xx,(d-1)*360+y*2+yy,c) end end
   end end end
  end
 end
 app.activeSprite=sheet;app.command.SaveFileAs{ui=false,filename=work..'native-'..motion..'-contact_v001.png'};sheet:close()
 local preview=Sprite(720,360,ColorMode.RGB)
 for f=0,count-1 do
  if f>0 then preview:newEmptyFrame() end
  local dst=Image(720,360,ColorMode.RGB)
  for y=0,359 do for x=0,719 do local v=(math.floor(x/20)+math.floor(y/20))%2==0 and 228 or 242;dst:drawPixel(x,y,pc.rgba(v,v,v,255)) end end
  for d,side in ipairs({'left','right'}) do
   local srcSprite=app.open(root..'source/arctic-fox/image-undecided/180/anim-'..motion..'/'..side..string.format('/frame-%02d_v001.png',f))
   local src=Image(srcSprite.spec);src:drawSprite(srcSprite,1);srcSprite:close()
   for y=0,179 do for x=0,179 do local c=src:getPixel(x,y);if pc.rgbaA(c)>0 then
    for yy=0,1 do for xx=0,1 do dst:drawPixel((d-1)*360+x*2+xx,y*2+yy,c) end end
   end end end
  end
  preview:newCel(preview.layers[1],f+1,dst,Point(0,0));preview.frames[f+1].duration=motion=='idle' and ({0.26,0.20,0.26,0.20})[f+1] or 0.1
 end
 app.activeSprite=preview;app.command.SaveFileAs{ui=false,filename=work..'native-'..motion..'-preview_v001.gif'};preview:close()
end
