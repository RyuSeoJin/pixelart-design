local root='P:/github-repository/pixelart-design/projects/pixelart-character/source/nightmare-witch/'
do
 local s=app.open(root..'work/side_left-hat-generated_v004.png')
 app.activeSprite=s
 app.command.SpriteSize{ui=false,width=992,height=992,method='bilinear'}
 local fg=Image(1024,1024,ColorMode.RGB)
 fg:drawImage(s.cels[1].image,Point(16,16))
 s:close()
 for it in fg:pixels() do if app.pixelColor.rgbaA(it())<=32 then it(0) end end
 local out=Sprite(1024,1024,ColorMode.RGB)
 out.cels[1].image=fg
 out:saveAs(root..'work/side_left_v004.aseprite')
 out:saveAs(root..'image-undecided/1024/view/side_left_v004.png')
 out:close()
 for _,bg in ipairs({{'white',245},{'dark',45}}) do
  local a=Sprite(1024,1024,ColorMode.RGB)
  local im=Image(1024,1024,ColorMode.RGB)
  im:clear(app.pixelColor.rgba(bg[2],bg[2],bg[2],255))
  im:drawImage(fg,Point(0,0))
  a.cels[1].image=im
  a:saveAs(root..'work/side_left-'..bg[1]..'_v004.png')
  a:close()
  local z=Sprite(530,260,ColorMode.RGB)
  local zi=Image(530,260,ColorMode.RGB)
  zi:drawImage(im,Point(-250,-0))
  z.cels[1].image=zi
  app.activeSprite=z
  app.command.SpriteSize{ui=false,width=1060,height=520,method='nearest'}
  z:saveAs(root..'work/side_left-hat-detail-'..bg[1]..'_v004.png')
  z:close()
 end
end
do
 local s=app.open(root..'work/side_right-hat-generated_v002.png')
 app.activeSprite=s
 app.command.SpriteSize{ui=false,width=992,height=992,method='bilinear'}
 local fg=Image(1024,1024,ColorMode.RGB)
 fg:drawImage(s.cels[1].image,Point(16,16))
 s:close()
 for it in fg:pixels() do if app.pixelColor.rgbaA(it())<=32 then it(0) end end
 local out=Sprite(1024,1024,ColorMode.RGB)
 out.cels[1].image=fg
 out:saveAs(root..'work/side_right_v002.aseprite')
 out:saveAs(root..'image-undecided/1024/view/side_right_v002.png')
 out:close()
 for _,bg in ipairs({{'white',245},{'dark',45}}) do
  local a=Sprite(1024,1024,ColorMode.RGB)
  local im=Image(1024,1024,ColorMode.RGB)
  im:clear(app.pixelColor.rgba(bg[2],bg[2],bg[2],255))
  im:drawImage(fg,Point(0,0))
  a.cels[1].image=im
  a:saveAs(root..'work/side_right-'..bg[1]..'_v002.png')
  a:close()
  local z=Sprite(530,260,ColorMode.RGB)
  local zi=Image(530,260,ColorMode.RGB)
  zi:drawImage(im,Point(-250,-0))
  z.cels[1].image=zi
  app.activeSprite=z
  app.command.SpriteSize{ui=false,width=1060,height=520,method='nearest'}
  z:saveAs(root..'work/side_right-hat-detail-'..bg[1]..'_v002.png')
  z:close()
 end
end
do
 local s=app.open(root..'work/behind-hat-generated_v003.png')
 app.activeSprite=s
 app.command.SpriteSize{ui=false,width=992,height=992,method='bilinear'}
 local fg=Image(1024,1024,ColorMode.RGB)
 fg:drawImage(s.cels[1].image,Point(16,16))
 s:close()
 for it in fg:pixels() do if app.pixelColor.rgbaA(it())<=32 then it(0) end end
 local out=Sprite(1024,1024,ColorMode.RGB)
 out.cels[1].image=fg
 out:saveAs(root..'work/behind_v003.aseprite')
 out:saveAs(root..'image-undecided/1024/view/behind_v003.png')
 out:close()
 for _,bg in ipairs({{'white',245},{'dark',45}}) do
  local a=Sprite(1024,1024,ColorMode.RGB)
  local im=Image(1024,1024,ColorMode.RGB)
  im:clear(app.pixelColor.rgba(bg[2],bg[2],bg[2],255))
  im:drawImage(fg,Point(0,0))
  a.cels[1].image=im
  a:saveAs(root..'work/behind-'..bg[1]..'_v003.png')
  a:close()
  local z=Sprite(530,260,ColorMode.RGB)
  local zi=Image(530,260,ColorMode.RGB)
  zi:drawImage(im,Point(-250,-0))
  z.cels[1].image=zi
  app.activeSprite=z
  app.command.SpriteSize{ui=false,width=1060,height=520,method='nearest'}
  z:saveAs(root..'work/behind-hat-detail-'..bg[1]..'_v003.png')
  z:close()
 end
end
