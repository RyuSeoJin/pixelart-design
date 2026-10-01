local root='P:/github-repository/pixelart-design/projects/pixelart-character/source/nightmare-witch/'
local s=app.open(root..'work/side_left-generated_v001.png')
app.activeSprite=s
app.command.SpriteSize{ui=false,width=1024,height=1024,method='bilinear'}
for it in s.cels[1].image:pixels() do if app.pixelColor.rgbaA(it())<=32 then it(0) end end
s:saveAs(root..'work/side_left_v001.aseprite')
s:saveAs(root..'image-undecided/1024/view/side_left_v001.png')
local fg=Image(s.cels[1].image)
s:close()
for _,v in ipairs({{'white',245},{'dark',45}}) do
 local a=Sprite(1024,1024,ColorMode.RGB)
 local im=Image(1024,1024,ColorMode.RGB)
 im:clear(app.pixelColor.rgba(v[2],v[2],v[2],255))
 im:drawImage(fg,Point(0,0))
 a.cels[1].image=im
 a:saveAs(root..'work/side_left-'..v[1]..'_v001.png')
 a:close()
end
