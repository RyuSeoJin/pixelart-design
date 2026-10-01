-- v1.0: 부츠 명암·입구·끈 마감 수정 시안
local root='P:/github-repository/pixelart-design/projects/pixelart-character/source/nightmare-witch/'
local s=app.open(root..'work/front-generated_v019.png')
app.activeSprite=s
app.command.SpriteSize{ui=false,width=1024,height=1024,method='bilinear'}
for it in s.cels[1].image:pixels() do if app.pixelColor.rgbaA(it())<=32 then it(0) end end
s:saveAs(root..'work/front-boots_v001.aseprite')
s:saveAs(root..'image-undecided/1024/view/front_v018.png')
app.command.CanvasSize{ui=false,left=-435,right=-409,top=-825,bottom=-4}
app.command.SpriteSize{ui=false,width=540,height=585,method='nearest-neighbor'}
s:saveAs(root..'work/boots-detail_v001.png')
s:close()
