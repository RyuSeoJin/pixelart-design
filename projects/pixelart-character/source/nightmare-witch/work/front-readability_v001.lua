-- v1.0: 1024 가독성 재작화 출력과 배경별 비교
local root='P:/github-repository/pixelart-design/projects/pixelart-character/source/nightmare-witch/'
local s=app.open(root..'work/front-generated_v018.png')
app.activeSprite=s
app.command.SpriteSize{ui=false,width=1024,height=1024,method='bilinear'}
for it in s.cels[1].image:pixels() do if app.pixelColor.rgbaA(it())<=32 then it(0) end end
s:saveAs(root..'work/front-readability_v001.aseprite')
s:saveAs(root..'image-undecided/1024/view/front_v017.png')
local foreground=Image(s.cels[1].image)
s:close()
for _,bg in ipairs({{'white',255},{'dark',48}}) do
 local out=Sprite(1024,1024,ColorMode.RGB)
 local im=Image(1024,1024,ColorMode.RGB)
 im:clear(app.pixelColor.rgba(bg[2],bg[2],bg[2],255))
 im:drawImage(foreground,Point(0,0))
 out.cels[1].image=im
 out:saveAs(root..'work/front-readability-'..bg[1]..'_v001.png')
 out:close()
end
local d=app.open(root..'image-undecided/1024/view/front_v017.png')
app.activeSprite=d
app.command.CanvasSize{ui=false,left=-395,right=-409,top=-85,bottom=-779}
app.command.SpriteSize{ui=false,width=880,height=640,method='nearest-neighbor'}
d:saveAs(root..'work/hair-detail-front_v017.png')
d:close()
