-- v1.0: 머리 윤곽 수정본 출력 및 비교용 머리 확대
local root='P:/github-repository/pixelart-design/projects/pixelart-character/source/nightmare-witch/'
local s=app.open(root..'work/front-generated_v017.png')
app.activeSprite=s
app.command.SpriteSize{ui=false,width=1024,height=1024,method='bilinear'}
for it in s.cels[1].image:pixels() do if app.pixelColor.rgbaA(it())<=32 then it(0) end end
s:saveAs(root..'work/front-hair_v001.aseprite')
s:saveAs(root..'image-undecided/1024/view/front_v016.png')
s:close()
for _,v in ipairs({'015','016'}) do
 local a=app.open(root..'image-undecided/1024/view/front_v'..v..'.png')
 app.activeSprite=a
 app.command.CanvasSize{ui=false,left=-395,right=-419,top=-85,bottom=-784}
 app.command.SpriteSize{ui=false,width=840,height=620,method='nearest-neighbor'}
 a:saveAs(root..'work/hair-detail-front_v'..v..'.png')
 a:close()
end
