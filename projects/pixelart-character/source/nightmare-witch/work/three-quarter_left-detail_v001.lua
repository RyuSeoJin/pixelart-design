local root='P:/github-repository/pixelart-design/projects/pixelart-character/source/nightmare-witch/work/'
for _,bg in ipairs({'white','dark'}) do
 local s=app.open(root..'three-quarter_left-'..bg..'_v001.png')
 for _,q in ipairs({{'head',320,16,380,250},{'hands',340,460,430,285},{'boots',350,770,300,240}}) do
  local a=Sprite(q[4],q[5],ColorMode.RGB)
  local im=Image(q[4],q[5],ColorMode.RGB)
  im:drawImage(s.cels[1].image,Point(-q[2],-q[3]))
  a.cels[1].image=im
  app.activeSprite=a
  app.command.SpriteSize{ui=false,width=q[4]*2,height=q[5]*2,method='nearest'}
  a:saveAs(root..'three-quarter_left-detail-'..q[1]..'-'..bg..'_v001.png')
  a:close()
 end
 s:close()
end
