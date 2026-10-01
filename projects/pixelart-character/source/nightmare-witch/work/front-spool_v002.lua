-- v1.0: 진한 보라 실과 허리 지지끈 수정 시안 출력
local root='P:/github-repository/pixelart-design/projects/pixelart-character/source/nightmare-witch/'
local s=app.open(root..'work/front-generated_v021.png')
app.activeSprite=s
app.command.SpriteSize{ui=false,width=1024,height=1024,method='bilinear'}
for it in s.cels[1].image:pixels() do if app.pixelColor.rgbaA(it())<=32 then it(0) end end
s:saveAs(root..'work/front-spool_v002.aseprite')
s:saveAs(root..'image-undecided/1024/view/front_v020.png')
app.command.CanvasSize{ui=false,left=-390,right=-399,top=-365,bottom=-504}
app.command.SpriteSize{ui=false,width=705,height=465,method='nearest-neighbor'}
s:saveAs(root..'work/spool-detail_v002.png')
s:close()
