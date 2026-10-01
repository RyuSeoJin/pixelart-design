-- v1.0: 해짐 단순화 시안 출력 및 저알파 마감
local root='P:/github-repository/pixelart-design/projects/pixelart-character/source/nightmare-witch/'
local s=app.open(root..'work/front-generated_v013.png')
app.activeSprite=s
app.command.SpriteSize{ui=false,width=1024,height=1024,method='bilinear'}
for it in s.cels[1].image:pixels() do if app.pixelColor.rgbaA(it())<=32 then it(0) end end
s:saveAs(root..'work/front-embroidery_v001.aseprite')
s:saveAs(root..'image-undecided/1024/view/front_v012.png')
s:close()
