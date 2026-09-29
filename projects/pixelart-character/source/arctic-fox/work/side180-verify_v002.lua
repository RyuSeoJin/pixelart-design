
local root='P:/github-repository/pixelart-design/projects/pixelart-character/'
local work=root..'source/arctic-fox/work/'
local out=root..'source/arctic-fox/image-undecided/180/view/'
local pc=app.pixelColor
for _,side in ipairs({'left','right'}) do
 local s=app.open(root..'sprites/arctic-fox/side_'..side..'_v002.aseprite')
 local a=Image(s.spec);a:drawSprite(s,1)
 local png=app.open(out..'side_'..side..'_v002.png');local b=Image(png.spec);b:drawSprite(png,1)
 for y=0,179 do for x=0,179 do assert(a:getPixel(x,y)==b:getPixel(x,y),'ASE_PNG_MISMATCH') end end
 s:close();png:close();print(side..': ASE_PNG_IDENTICAL')
end
-- 실제 교대 파일의 각 프레임을 해석하여 같은 캔버스에서 재생될 내용을 확인합니다.
local g=app.open(work..'side180-direction-toggle_v002.gif')
assert(#g.frames==2)
app.command.ChangePixelFormat{format='rgb'}
for i=1,2 do
 app.activeSprite=g;app.activeFrame=g.frames[i]
 local im=Image(g.spec);im:drawSprite(g,i)
 local s=Sprite(180,180,ColorMode.RGB);s.cels[1].image=im
 app.command.SaveFileAs{ui=false,filename=work..'side180-toggle-frame-'..i..'_v002.png'};s:close()
end
print('GIF_2_FRAMES_VERIFIED')

