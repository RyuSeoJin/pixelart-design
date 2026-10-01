local root='P:/github-repository/pixelart-design/projects/pixelart-character/source/nightmare-witch/'
local s=app.open(root..'work/front-generated_v025.png')
app.activeSprite=s
app.command.SpriteSize{ui=false,width=1024,height=1024,method='bilinear'}
for it in s.cels[1].image:pixels() do
  if app.pixelColor.rgbaA(it())<=32 then it(0) end
end
s:saveAs(root..'work/front-detail_v001.aseprite')
s:saveAs(root..'image-undecided/1024/view/front_v024.png')
s:close()
for _,v in ipairs({'023','024'}) do
  local a=app.open(root..'image-undecided/1024/view/front_v'..v..'.png')
  app.activeSprite=a
  app.command.CanvasSize{ui=false,left=-390,right=-394,top=-85,bottom=-769}
  app.command.SpriteSize{ui=false,width=720,height=510,method='nearest-neighbor'}
  a:saveAs(root..'work/head-detail_v'..v..'.png')
  a:close()
end
