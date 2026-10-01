do
local root='P:/github-repository/pixelart-design/projects/pixelart-character/source/nightmare-witch/'
local s=app.open(root..'work/front-boot-color-generated_v031.png')
app.activeSprite=s
app.command.SpriteSize{ui=false,width=992,height=992,method='bilinear'}
local fg=Image(1024,1024,ColorMode.RGB)
fg:drawImage(s.cels[1].image,Point(16,16))
s:close()
local out=Sprite(1024,1024,ColorMode.RGB)
out.cels[1].image=fg
out:saveAs(root..'work/front_v031.aseprite')
out:saveAs(root..'image-undecided/1024/view/front_v031.png')
out:close()
for _,v in ipairs({{'white',245},{'dark',45}}) do
 local a=Sprite(1024,1024,ColorMode.RGB)
 local im=Image(1024,1024,ColorMode.RGB)
 im:clear(app.pixelColor.rgba(v[2],v[2],v[2],255))
 im:drawImage(fg,Point(0,0))
 a.cels[1].image=im
 a:saveAs(root..'work/front-'..v[1]..'_v031.png')
 a:close()
end

end
do
local root='P:/github-repository/pixelart-design/projects/pixelart-character/source/nightmare-witch/'
local s=app.open(root..'work/side_left-boot-color-generated_v005.png')
app.activeSprite=s
app.command.SpriteSize{ui=false,width=992,height=992,method='bilinear'}
local fg=Image(1024,1024,ColorMode.RGB)
fg:drawImage(s.cels[1].image,Point(16,16))
s:close()
local out=Sprite(1024,1024,ColorMode.RGB)
out.cels[1].image=fg
out:saveAs(root..'work/side_left_v005.aseprite')
out:saveAs(root..'image-undecided/1024/view/side_left_v005.png')
out:close()
for _,v in ipairs({{'white',245},{'dark',45}}) do
 local a=Sprite(1024,1024,ColorMode.RGB)
 local im=Image(1024,1024,ColorMode.RGB)
 im:clear(app.pixelColor.rgba(v[2],v[2],v[2],255))
 im:drawImage(fg,Point(0,0))
 a.cels[1].image=im
 a:saveAs(root..'work/side_left-'..v[1]..'_v005.png')
 a:close()
end

end
do
local root='P:/github-repository/pixelart-design/projects/pixelart-character/source/nightmare-witch/'
local s=app.open(root..'work/side_right-boot-color-generated_v003.png')
app.activeSprite=s
app.command.SpriteSize{ui=false,width=992,height=992,method='bilinear'}
local fg=Image(1024,1024,ColorMode.RGB)
fg:drawImage(s.cels[1].image,Point(16,16))
s:close()
local out=Sprite(1024,1024,ColorMode.RGB)
out.cels[1].image=fg
out:saveAs(root..'work/side_right_v003.aseprite')
out:saveAs(root..'image-undecided/1024/view/side_right_v003.png')
out:close()
for _,v in ipairs({{'white',245},{'dark',45}}) do
 local a=Sprite(1024,1024,ColorMode.RGB)
 local im=Image(1024,1024,ColorMode.RGB)
 im:clear(app.pixelColor.rgba(v[2],v[2],v[2],255))
 im:drawImage(fg,Point(0,0))
 a.cels[1].image=im
 a:saveAs(root..'work/side_right-'..v[1]..'_v003.png')
 a:close()
end

end
do
local root='P:/github-repository/pixelart-design/projects/pixelart-character/source/nightmare-witch/'
local s=app.open(root..'work/behind-boot-color-generated_v004.png')
app.activeSprite=s
app.command.SpriteSize{ui=false,width=992,height=992,method='bilinear'}
local fg=Image(1024,1024,ColorMode.RGB)
fg:drawImage(s.cels[1].image,Point(16,16))
s:close()
local out=Sprite(1024,1024,ColorMode.RGB)
out.cels[1].image=fg
out:saveAs(root..'work/behind_v004.aseprite')
out:saveAs(root..'image-undecided/1024/view/behind_v004.png')
out:close()
for _,v in ipairs({{'white',245},{'dark',45}}) do
 local a=Sprite(1024,1024,ColorMode.RGB)
 local im=Image(1024,1024,ColorMode.RGB)
 im:clear(app.pixelColor.rgba(v[2],v[2],v[2],255))
 im:drawImage(fg,Point(0,0))
 a.cels[1].image=im
 a:saveAs(root..'work/behind-'..v[1]..'_v004.png')
 a:close()
end

end
