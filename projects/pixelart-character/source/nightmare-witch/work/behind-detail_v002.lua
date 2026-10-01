local root='P:/github-repository/pixelart-design/projects/pixelart-character/source/nightmare-witch/work/'
for _,bg in ipairs({'white','dark'}) do
 local s=app.open(root..'behind-'..bg..'_v002.png')
 for _,q in ipairs({{'head',310,16,395,235},{'hands',275,460,485,285},{'boots',425,810,195,205}}) do
  local a=Sprite(q[4],q[5],ColorMode.RGB)
  local im=Image(q[4],q[5],ColorMode.RGB)
  im:drawImage(s.cels[1].image,Point(-q[2],-q[3]))
  a.cels[1].image=im
  app.activeSprite=a
  app.command.SpriteSize{ui=false,width=q[4]*2,height=q[5]*2,method='nearest'}
  a:saveAs(root..'behind-detail-'..q[1]..'-'..bg..'_v002.png')
  a:close()
 end
 s:close()
end
