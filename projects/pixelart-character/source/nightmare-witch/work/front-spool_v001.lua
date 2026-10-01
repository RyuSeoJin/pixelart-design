-- v1.0: 실감개 색상 수정본 출력
local root='P:/github-repository/pixelart-design/projects/pixelart-character/source/nightmare-witch/'
local s=app.open(root..'work/front-generated_v020.png')
app.activeSprite=s
app.command.SpriteSize{ui=false,width=1024,height=1024,method='bilinear'}
for it in s.cels[1].image:pixels() do if app.pixelColor.rgbaA(it())<=32 then it(0) end end
s:saveAs(root..'work/front-spool_v001.aseprite')
s:saveAs(root..'image-undecided/1024/view/front_v019.png')
s:close()
