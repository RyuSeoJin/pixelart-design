local root='P:/github-repository/pixelart-design/projects/pixelart-character/source/nightmare-witch/'
local s=app.open(root..'work/behind-outline-generated_v001.png')
app.activeSprite=s
app.command.SpriteSize{ui=false,width=992,height=992,method='bilinear'}
local fg=Image(1024,1024,ColorMode.RGB)
fg:drawImage(s.cels[1].image,Point(16,16))
s:close()
for it in fg:pixels() do if app.pixelColor.rgbaA(it())<=32 then it(0) end end
local out=Sprite(1024,1024,ColorMode.RGB)
out.cels[1].image=fg
out:saveAs(root..'work/behind_v002.aseprite')
out:saveAs(root..'image-undecided/1024/view/behind_v002.png')
out:close()
for _,v in ipairs({{'white',245},{'dark',45}}) do
 local a=Sprite(1024,1024,ColorMode.RGB)
 local im=Image(1024,1024,ColorMode.RGB)
 im:clear(app.pixelColor.rgba(v[2],v[2],v[2],255))
 im:drawImage(fg,Point(0,0))
 a.cels[1].image=im
 a:saveAs(root..'work/behind-'..v[1]..'_v002.png')
 a:close()
end
