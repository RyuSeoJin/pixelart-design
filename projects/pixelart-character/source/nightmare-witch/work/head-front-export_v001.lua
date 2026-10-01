local root='P:/github-repository/pixelart-design/projects/pixelart-character/source/nightmare-witch/'
local s=app.open(root..'work/view-three-quarter-head_front-generated_v001.png')
app.activeSprite=s
app.command.SpriteSize{ui=false,width=1024,height=1024,method='bilinear'}
s:saveAs(root..'work/view-three-quarter-head_front_v001.aseprite')
s:saveAs(root..'image-undecided/1024/view/view-three-quarter-head_front_v001.png')
s:close()
for _,b in ipairs({{'white',245},{'dark',45}}) do
 local board=Sprite(2048,1024,ColorMode.RGB)
 local im=Image(2048,1024,ColorMode.RGB)
 im:clear(app.pixelColor.rgba(b[2],b[2],b[2],255))
 local faces=Sprite(1200,700,ColorMode.RGB)
 local fi=Image(1200,700,ColorMode.RGB)
 fi:clear(app.pixelColor.rgba(b[2],b[2],b[2],255))
 for k,path in ipairs({'image-confirmed/1024/view/view-three-quarter-front.png','image-undecided/1024/view/view-three-quarter-head_front_v001.png'}) do
  local a=app.open(root..path)
  im:drawImage(a.cels[1].image,Point((k-1)*1024,0))
  local crop=Image(480,350,ColorMode.RGB)
  crop:clear(app.pixelColor.rgba(b[2],b[2],b[2],255))
  crop:drawImage(a.cels[1].image,Point(-330,0))
  local cs=Sprite(480,350,ColorMode.RGB)
  cs.cels[1].image=crop
  app.activeSprite=cs
  app.command.SpriteSize{ui=false,width=600,height=438,method='nearest'}
  fi:drawImage(cs.cels[1].image,Point((k-1)*600,80))
  cs:close()
  a:close()
 end
 board.cels[1].image=im
 board:saveAs(root..'work/head-front-compare-'..b[1]..'_v001.png')
 board:close()
 faces.cels[1].image=fi
 faces:saveAs(root..'work/head-front-face-'..b[1]..'_v001.png')
 faces:close()
end
print('머리 정면 전신 및 비교표 저장 완료')

